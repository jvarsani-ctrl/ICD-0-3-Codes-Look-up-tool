"""The ICCC-3 Group XI decision trees, as data (contract docs/group_11_build_contract.md §4).

trees() returns the trees in §4.1 order (group11_common.TREES). Each tree is built by the module
its TREES row names: build/group11_organs/<organ>.py for the organ trees and the melanoma tree,
build/group11_families/<family>.py for the family trees (one module per family, so the families are written in parallel). A module that does not exist yet is skipped, so
the build runs while the trees are written in parallel. Every module exposes build(tree_id) and
DECISIONS (group11_common's module docstring).

Cross-tree hops. A histology screen hops into the melanoma tree (D13) and a deposit of
carcinoma with no primary found continues in the unspecified tree (D10). While the target tree's
module does not exist, trees() removes that option and lists it in DEFERRED_HOPS, so the
validator does not fail on a node another task has not written; the option returns by itself
when the module lands. When the module exists and the node does not, trees() raises TreeError.

    python3 build/group11_tree.py --report               trees, node counts, picker report,
                                                         deferred hops
    python3 build/group11_tree.py --write-evidence-map   rewrite docs/evidence_documents/
                                                         group_11.json from the gates' tiers

The generator (build/generate_group11_entries.py) calls trees() and decisions().
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import group11_common as common  # noqa: E402
from group11_common import TreeError  # noqa: E402,F401  (the generator catches this class)

REPO = Path(__file__).resolve().parent.parent
EVIDENCE_MAP = REPO / "docs" / "evidence_documents" / "group_11.json"

DEFERRED_HOPS: list = []


def _module(name: str):
    """The module, or None when its file does not exist. An error inside a module that exists
    is raised, not taken for absence."""
    try:
        if importlib.util.find_spec(name) is None:
            return None
    except ModuleNotFoundError:
        return None
    return importlib.import_module(name)


def built_modules() -> dict:
    """{tree_id: module} for every TREES row whose module exists, in §4.1 order."""
    # G11_ONLY=<tree_id,...> restricts the build to those trees, so an implementer can build and walk
    # its own trees while other modules are being written. Unset, every tree is built.
    import os
    only = set(filter(None, os.environ.get("G11_ONLY", "").split(",")))
    out = {}
    for row in common.trees_table():
        if only and row["tree_id"] not in only:
            continue
        mod = _module(row["module"])
        if mod is not None:
            out[row["tree_id"]] = mod
    return out


def _resolve_hops(trees: list, mods: dict) -> None:
    """Drop the options whose cross-tree target belongs to a tree with no module yet; raise on
    a target the built tree does not hold."""
    DEFERRED_HOPS.clear()
    ids = {n["node_id"] for t in trees for n in t["nodes"]}
    tree_of_prefix = {row["prefix"]: row["tree_id"] for row in common.trees_table()}
    for t in trees:
        for nd in t["nodes"]:
            kept = []
            for o in nd.get("options") or []:
                target = o.get("next_node") if isinstance(o, dict) else None
                if not target or target in ids:
                    kept.append(o)
                    continue
                owner = tree_of_prefix.get(common.prefix_of(target))
                if owner is None:
                    raise TreeError("%s: option %r names %s, whose prefix no Group XI tree "
                                    "carries" % (nd["node_id"], o.get("label"), target))
                if owner in mods:
                    raise TreeError("%s: option %r names %s, which %s does not hold"
                                    % (nd["node_id"], o.get("label"), target, owner))
                DEFERRED_HOPS.append((nd["node_id"], o.get("label"), target, owner))
            if nd.get("options") is not None:
                nd["options"] = kept


def trees() -> list:
    """The Group XI trees in §4.1 order, as a fresh structure (a JSON round trip), so callers
    may mutate it."""
    mods = built_modules()
    out = []
    for row in common.trees_table():
        mod = mods.get(row["tree_id"])
        if mod is None:
            continue
        t = mod.build(row["tree_id"])
        if t.get("tree_id") != row["tree_id"]:
            raise TreeError("%s.build(%r) returned tree %r" % (row["module"], row["tree_id"],
                                                              t.get("tree_id")))
        out.append(t)
    _resolve_hops(out, mods)
    return json.loads(json.dumps(out))


def decisions() -> dict:
    """Every built module's DECISIONS, merged. A pair two modules annotate keeps both modules'
    D-numbers, evidence files and sentences; their overrides must agree."""
    merged: dict = {}
    seen_modules = set()
    for mod in built_modules().values():
        if mod.__name__ in seen_modules:
            continue
        seen_modules.add(mod.__name__)
        for k, d in getattr(mod, "DECISIONS", {}).items():
            if len(d) < 3:
                raise TreeError("%s DECISIONS[%s]: (D-numbers, evidence file, sentence[, "
                                "overrides])" % (mod.__name__, k))
            if k not in merged:
                merged[k] = tuple(d)
                continue
            refs, files, sentence = merged[k][:3]
            over = merged[k][3] if len(merged[k]) > 3 else {}
            new_over = d[3] if len(d) > 3 else {}
            if over and new_over and over != new_over:
                # One entry serves every tree, so list-valued overrides (the tests and the
                # markers that support the code at one site or another) are united in order;
                # any other value must agree.
                united = dict(over)
                for key, val in new_over.items():
                    old = united.get(key)
                    if isinstance(old, list) and isinstance(val, list):
                        united[key] = old + [v for v in val if v not in old]
                    elif old is None:
                        united[key] = val
                    elif old != val:
                        raise TreeError("%s: %s and an earlier module give different %s"
                                        % (k, mod.__name__, key))
                new_over = united
                over = {}
            refs_all = []
            for r in [x.strip() for x in (refs + "," + d[0]).split(",")]:
                if r and r not in refs_all:
                    refs_all.append(r)
            files_all = []
            for f in [x.strip() for x in (files + "," + d[1]).split(",")]:
                if f and f not in files_all:
                    files_all.append(f)
            text = sentence if d[2] in sentence else sentence + " " + d[2]
            merged[k] = (", ".join(refs_all), ", ".join(files_all), text) + \
                ((over or new_over,) if (over or new_over) else ())
    return merged


def write_evidence_map(ts: list) -> Path:
    EVIDENCE_MAP.write_text(json.dumps(common.evidence_mapping(ts), indent=2,
                                       ensure_ascii=False) + "\n", encoding="utf-8")
    return EVIDENCE_MAP


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    ts = trees()
    if "--write-evidence-map" in argv:
        print("wrote %s (%d gate(s))" % (write_evidence_map(ts),
                                         len(common.evidence_mapping(ts)["nodes"])))
    if "--report" in argv or not argv:
        for t in ts:
            print("%-26s %3d nodes" % (t["tree_id"], len(t["nodes"])))
        for tid, rep in common.PICKER_REPORT.items():
            print("picker %s: %d offered; partial %s; held as options %s; obsolete %s; D11 %s"
                  % (tid, len(rep["offered"]), rep["partial"] or "none",
                     rep["held_as_options"] or "none", rep["obsolete"] or "none",
                     rep["d11"] or "none"))
        for hop in DEFERRED_HOPS:
            print("deferred hop: %s %r -> %s (tree %s has no module yet)" % hop)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except TreeError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        raise SystemExit(2)
