#!/usr/bin/env python3
"""
apply_evidence_documents.py — turn a group's evidence gates into document checklists.

The registrar replaced the single-choice "Evidence in file" question with seven document
checkboxes (6 Oct 2026; spec docs/superpowers/specs/2026-10-06-ux-overall-fixes-design.md,
sections 4 and 7). Each evidence gate gets a `tick_list` and each tier option gets `ticks`
rules; options that state a situation rather than a document set stay without `ticks`.
Labels, captures and routes do not change, with one exception below.

A tier whose label offers two alternatives ("flow cytometry and/or IHC") needs a rule one
`any_of` group cannot state: morphology AND (Lab Report OR IHC Report). The mapping then lists
`extra_options`: a copy of an existing option, placed straight after option `after`, with its
own rules and with the tests it may not credit removed from `captures.evidence_tests`
(`drop_tests`; an IHC report alone is not flow cytometry). The copy keeps the label, route and
every other capture, so no clinical branch is added.

Two optional fields let a copy say something its source does not, for a tier the clerk cannot
otherwise tell apart from its source. `label` replaces the copy's label. `captures_set` merges
into its captures. Together with `drop_tests` they split one gene-test tier into "karyotype or
FISH only", "PCR or sequencing only" and "both" without a new route: all three go to the same
next node, and each credits only what its label says was done. A copy with a `label` must also
say so in its rationale, since two options with different wording and the same route are
otherwise indistinguishable in the mapping.

The rules live in a mapping file, one per group, in docs/evidence_documents/group_NN.json:

  { "group": 5,
    "nodes": [ { "node_id": "rb_document_inventory",
                 "question_edit": "", "hint_edit": "",
                 "options": [ { "index": 0, "label_head": "...", "kind": "tier",
                                "requires": [], "any_of": [], "excludes": ["imaging", ...],
                                "rationale": "...", "confidence": "high" }, ... ] } ] }

Usage:
  python3 build/apply_evidence_documents.py data/database/group_05_dt.json docs/evidence_documents/group_05.json
  python3 build/apply_evidence_documents.py --check data/database/group_05_dt.json docs/evidence_documents/group_05.json

--check writes nothing and exits 1 when the file would change. The script is idempotent:
applied twice, the second run changes nothing. It refuses to touch an option whose label no
longer starts with the mapping's `label_head`, so a gate edited since the mapping was made
is reported, not mis-mapped.

A group file belonging to another branch (Group 10) takes the same two arguments after that
branch has merged this one.
"""
import json
import re
import sys
from pathlib import Path

VOCABULARY = "evidence_documents"


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def put_after(d: dict, after_key: str, key: str, value) -> dict:
    """Return d with `key` set, placed straight after `after_key` when that key exists."""
    out = {}
    placed = False
    for k, v in d.items():
        if k == key:
            continue
        out[k] = v
        if k == after_key and not placed:
            out[key] = value
            placed = True
    if not placed:
        out[key] = value
    return out


def ticks_object(opt: dict) -> dict:
    t = {}
    for f in ("requires", "any_of", "excludes"):
        if opt.get(f):
            t[f] = list(opt[f])
    return t


def extras_of(m: dict) -> list:
    return sorted(m.get("extra_options") or [], key=lambda e: e["after"])


def strip_extras(opts: list, m: dict) -> list:
    """The options without the copies an earlier run inserted, so the mapping applies twice alike."""
    ex = extras_of(m)
    if not ex or len(opts) != len(m["options"]) + len(ex):
        return opts
    drop = {e["after"] + 1 + k for k, e in enumerate(ex)}
    return [o for i, o in enumerate(opts) if i not in drop]


def apply(group_data: dict, mapping: dict) -> list:
    """Edit group_data in place; return the list of problems (empty when it applied)."""
    problems = []
    by_id = {}
    for tree in group_data.get("decision_trees", []):
        for i, node in enumerate(tree.get("nodes", [])):
            by_id[node["node_id"]] = (tree, i)
    for m in mapping["nodes"]:
        nid = m["node_id"]
        if nid not in by_id:
            problems.append("node %s is not in the group file" % nid)
            continue
        tree, pos = by_id[nid]
        node = tree["nodes"][pos]
        opts = strip_extras(node.get("options", []), m)
        if len(opts) != len(m["options"]):
            problems.append("node %s has %d options, the mapping has %d" % (nid, len(opts), len(m["options"])))
            continue
        new_opts = []
        for o, mo in zip(opts, sorted(m["options"], key=lambda x: x["index"])):
            head = squash(mo.get("label_head", ""))
            if head and not squash(o.get("label", "")).startswith(head):
                problems.append("node %s option %d: the label no longer starts %r" % (nid, mo["index"], head))
            clean = {k: v for k, v in o.items() if k != "ticks"}
            if mo["kind"] == "tier":
                clean = put_after(clean, "label", "ticks", ticks_object(mo))
            new_opts.append(clean)
        originals = list(new_opts)           # `copy_of` and `after` count the options as authored
        for k, e in enumerate(extras_of(m)):
            src = originals[e["copy_of"]]
            if "ticks" not in src:
                problems.append("node %s: extra option copies option %d, which is not a tier" % (nid, e["copy_of"]))
                continue
            copy = json.loads(json.dumps(src))
            copy["ticks"] = ticks_object(e)
            tests = (copy.get("captures") or {}).get("evidence_tests")
            if tests and e.get("drop_tests"):
                copy["captures"]["evidence_tests"] = [t for t in tests if t not in e["drop_tests"]]
            if e.get("label"):
                copy["label"] = e["label"]
            if e.get("captures_set"):
                copy["captures"] = dict(copy.get("captures") or {}, **e["captures_set"])
            new_opts.insert(e["after"] + 1 + k, copy)
        node = dict(node)
        node["options"] = new_opts
        for field in ("question", "hint"):
            edit, was = m.get(field + "_edit"), m.get(field + "_was")
            if not edit:
                continue
            now = node.get(field) or ""
            # The edit overwrites the node's text, so the text must be the one the mapping was
            # made against (or already the edit, on a second run). Anything else was written since.
            if was is not None and squash(now) not in (squash(was), squash(edit)):
                problems.append("node %s: the %s was changed since the mapping was made; applying would "
                                "overwrite it. Re-derive %s_edit from the current text" % (nid, field, field))
                continue
            node[field] = edit
        node = put_after(node, "hint" if "hint" in node else "question", "tick_list",
                         {"vocabulary": VOCABULARY, "resolve": "ask_siblings"})
        tree["nodes"][pos] = node
    return problems


def main(argv) -> int:
    check = "--check" in argv
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    group_path, map_path = Path(args[0]), Path(args[1])
    original = group_path.read_text(encoding="utf-8")
    data = json.loads(original)
    mapping = json.loads(map_path.read_text(encoding="utf-8"))
    problems = apply(data, mapping)
    if problems:
        print("NOT APPLIED to %s:" % group_path)
        for p in problems:
            print("  - " + p)
        return 1
    result = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if result == original:
        print("%s: already up to date (%d node(s))" % (group_path.name, len(mapping["nodes"])))
        return 0
    if check:
        print("%s: would change (%d node(s))" % (group_path.name, len(mapping["nodes"])))
        return 1
    group_path.write_text(result, encoding="utf-8")
    print("%s: applied %d node(s)" % (group_path.name, len(mapping["nodes"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
