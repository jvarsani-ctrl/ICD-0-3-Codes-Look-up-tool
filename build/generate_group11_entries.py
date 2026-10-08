#!/usr/bin/env python3
"""Generate data/database/group_11_dt.json for ICCC-3 Group XI, Other Malignant Epithelial
Neoplasms and Malignant Melanomas.

Group 11 build contract (docs/group_11_build_contract.md) §2: morphology_entries[] is
GENERATED from ICCC-2017.sqlite joined to icdo32.sqlite by build_inventory(), never transcribed
from the REDCap option file. The registrar ruled on 8 October 2026 that Group 11 is built
without a Diagnostic Pathway document; the evidence behind every screen is in
docs/group_11_evidence/. The hand-written content is the annotation layer in DECISIONS below.
Which tree and node emit which (code, behaviour) pair is read off the trees themselves
(emitters()), never listed by hand.

The decision trees are authored in build/group11_tree.py and written beside the entries by this
script, so one command reproduces the whole file:

    python3 build/generate_group11_entries.py          # writes group_11_dt.json
    python3 build/generate_group11_entries.py --check  # writes nothing; exit 1 if it would change
    python3 build/induce_flow.py                       # then re-induce branch_sequence

An error (an inventory that does not match the contract, a tree or note naming a pair outside
the entries, a tree emitting a pair design D3 keeps off every screen) exits 2.

induce_flow.py writes `branch_sequence` into every ihc_checklist. This script carries an
existing `branch_sequence` across when the node's rules are unchanged, so a regeneration that
changes nothing elsewhere leaves the file byte-identical; when the rules change the sequence is
dropped and induce_flow.py must be rerun, which the build enforces.

Entries. build_inventory() gives 2,183 records for group XI, which collapse to 229 (code,
behaviour) pairs, all /3. Standing rule 3 adds 8339/3 Follicular carcinoma, encapsulated,
angioinvasive, new in ICD-O-3.2 and outside every ICCC-2017 range, in XIb (design D11): 230
entries. One entry per pair. ICCC-2017 ranges 125 to 136 give one shared list of 174 pairs in
the eleven XIf subgroups, which differ only by site, and some of those pairs also sit in XIb,
XIc or XIe at those subgroups' sites. Each such entry carries `iccc3_subgroup_by_topography`,
resolved at output time by app.js subgroupFor(); its own `iccc3_subgroup_id` is the default,
XIf10.

Topography codes for the subgroup rules. The rules name every code in
data/shared/topography_codes.json that a subgroup's ICCC-2017 range covers, and also every
code in Layer 1's REDCap topography list ("RedCap Options/Topography Redcap.md") that falls in
a site-specific Group XI range. Task T3 adds the missing Group XI codes to the lookup from that
same list (contract §3.1), so the rules are the same before and after that edit. A range that
covers every code in the REDCap list (C00.0-C80.9: XIa range 119, XIb range 121, XId) is not
site-specific and adds nothing.

Layer 1 paths. This script reads ICD_LAYER1, ICCC_DB and ICDO_DB from the environment first,
the same variables build_database.py reads, because a git worktree sits two directories deeper
than the vault-relative defaults assume. It reads no REDCap option file.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVIDENCE_MAP = REPO / "docs" / "evidence_documents" / "group_11.json"
EVIDENCE_DIR = REPO / "docs" / "group_11_evidence"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_evidence_documents as evidence  # noqa: E402
import build_database as bd  # noqa: E402
import generate_group_inventory as gi  # noqa: E402
import group11_tree  # noqa: E402
from generate_group08_entries import carry_branch_sequences  # noqa: E402

OUT_PATH = REPO / "data" / "database" / "group_11_dt.json"
LOOKUP_PATH = REPO / "data" / "shared" / "topography_codes.json"
LAYER1_PATH = Path(os.environ.get("ICD_LAYER1", str(gi.DEFAULT_LAYER1)))
ICCC_PATH = Path(os.environ.get("ICCC_DB", str(gi.DEFAULT_ICCC)))
ICDO_PATH = Path(os.environ.get("ICDO_DB", str(gi.DEFAULT_ICDO)))
REDCAP_TOPOGRAPHY = LAYER1_PATH / "RedCap Options" / "Topography Redcap.md"

GROUP = 11
ICCC_GROUP = "XI"
EXPECTED_RECORDS = 2183
EXPECTED_INVENTORY_PAIRS = 229
EXPECTED_ENTRIES = 231

# Standing rule 3 (design D11): a valid ICD-O-3.2 code outside every ICCC-2017 range belongs to
# the group that offers it. {pair: subgroup}. The generator checks that ICD-O-3.2 prints the
# pair with a live Preferred term and that no ICCC-2017 range holds the code; the subgroup's
# name and site range are read from the inventory's site-specific range for that subgroup.
RULE3_ADDITIONS = {"8339/3": "XIb"}

# Rule F, the pathologist's stated behaviour (registrar, 8 October 2026, review A6, E7): a pair
# ICD-O-3.2 does not print, admitted by build_database.ICDO32_MATRIX_RULE, whose name is the
# code's Preferred term at the printed behaviour. {pair: subgroup}. The generator checks that the
# matrix rule holds the pair and that ICCC-2017 places the code in that subgroup.
RULE_F_ADDITIONS = {"8336/3": "XIb"}

# Contract §0.2 and design D3: the pairs whose every /3 term ICD-O-3.2 marks [obs]. The list is
# computed from icdo32.sqlite; this tuple is the assertion it must equal.
ALL_OBS_EXPECTED = ("8042/3", "8124/3", "8130/3", "8141/3", "8245/3", "8251/3", "8350/3",
                    "8440/3", "8450/3", "8508/3", "8512/3")

# Contract §2 item 3: a pair in the shared XIf list defaults to XIf10, carcinomas of other
# specified sites. At a specified site outside every Group XI range the output shows it too
# (design D11). Group 3's 9380 entry sets the convention for the rule list: the default
# subgroup carries no rule of its own, only the overrides do.
SHARED_DEFAULT = "XIf10"

GENERATED_NOTE = (
    "Generated by build/generate_group11_entries.py from ICCC-2017.sqlite joined to "
    "icdo32.sqlite (build_inventory, group XI), never transcribed from the REDCap option file "
    "(contract §2)."
)

# Field order is the validator's own list (Decision tree master §2).
FIELD_ORDER = bd.MORPHOLOGY_FIELDS

HISTOLOGY = ("Histology",)
HIST_IHC = ["Histology", "IHC"]


class GenerationError(Exception):
    """An input does not match the contract; main() reports it and exits 2."""


def key(code: str, behaviour: str) -> str:
    return "%s/%s" % (code, behaviour)


def note(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p)


def join_and(items: list) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


# --------------------------------------------------------------------------------------
# Which (code, behaviour) pairs each node emits, read off the trees: every branch or rule that
# carries morphology_code and behavior_code, and every node's nos_fallback. The generator fails
# when an emitted pair is absent from the entries or has no DECISIONS entry (the picker's pairs
# excepted), and when a DECISIONS entry names a pair no tree emits.
# --------------------------------------------------------------------------------------
def _emissions(obj):
    """Yield (code, behaviour, from_checklist_rule, holder) for every emission under a node.
    from_checklist_rule is True only for an ihc_checklist resolution_logic rule."""
    if isinstance(obj, dict):
        if obj.get("node_type") == "ihc_checklist":
            for rule in obj.get("resolution_logic") or []:
                if rule.get("morphology_code"):
                    yield rule["morphology_code"], rule["behavior_code"], True, rule
            fb = obj.get("nos_fallback")
            if isinstance(fb, dict) and fb.get("code"):
                yield fb["code"], fb["behavior_code"], False, fb
            for k, v in obj.items():
                if k not in ("resolution_logic", "nos_fallback"):
                    yield from _emissions(v)
            return
        if obj.get("morphology_code") and obj.get("behavior_code"):
            yield obj["morphology_code"], obj["behavior_code"], False, obj
        fb = obj.get("nos_fallback")
        if isinstance(fb, dict) and fb.get("code"):
            yield fb["code"], fb["behavior_code"], False, fb
        for k, v in obj.items():
            if k != "nos_fallback":
                yield from _emissions(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _emissions(v)


def emitters(trees: list) -> dict:
    """{pair: [(tree_id, node_id), ...]} in first-emission order."""
    out: dict = {}
    for t in trees:
        for n in t.get("nodes") or []:
            for code, beh, _from_checklist, _holder in _emissions(n):
                where = out.setdefault(key(code, beh), [])
                if (t["tree_id"], n["node_id"]) not in where:
                    where.append((t["tree_id"], n["node_id"]))
    return out


def picker_pairs(trees: list) -> set:
    """The pairs the picker nodes emit. Design D2: the picker is one histology_subclassification
    node per tree marked prefill_filter_from_search, generated from the inventory, so its pairs
    carry the templated note and need no hand-written decision."""
    return {key(code, beh)
            for t in trees for n in t.get("nodes") or []
            if n.get("prefill_filter_from_search") is True
            for code, beh, _from_checklist, _holder in _emissions(n)}


def checklist_markers(trees: list) -> dict:
    """{pair: [marker, ...]}: the positive markers of every checklist rule emitting the pair,
    in rule order. These are the pairs whose entries require IHC (Group 8 precedent)."""
    out: dict = {}
    for t in trees:
        for code, beh, from_checklist, rule in _emissions(t.get("nodes") or []):
            if not from_checklist:
                continue
            markers = out.setdefault(key(code, beh), [])
            for m in rule.get("positive") or []:
                if m not in markers:
                    markers.append(m)
    return out


def describe_emitters(where: list) -> str:
    """'g11_lung (lu_histology, lu_nut_panel) and g11_thymus (ty_histology)'."""
    by_tree: dict = {}
    for tree_id, node_id in where:
        by_tree.setdefault(tree_id, []).append(node_id)
    return join_and(["%s (%s)" % (t, ", ".join(nodes)) for t, nodes in by_tree.items()])


# --------------------------------------------------------------------------------------
# The annotation layer: DECISIONS[pair] = (design decisions, evidence file, sentence[,
# overrides]). The evidence file is the stem of a file in docs/group_11_evidence/
# ("XIf4_lung_pleura"), or several joined by ", ". The entry's coding_note is GENERATED_NOTE,
# the name and behaviour, the sentence, the evidence file and the nodes that emit the pair
# (contract §2 item 6). Sentences state what the evidence and the D-numbers decide, no more.
#
# Task T2 writes the annotations beside the trees: each tree module carries its own DECISIONS
# (build/group11_organs/*.py, build/group11_template.py), so the trees can be written in
# parallel without editing this file. run() fills DECISIONS from group11_tree.decisions(),
# which merges the modules' entries; a pair two modules annotate keeps both sentences.
#
# The optional fourth element overrides entry fields, limited to OVERRIDABLE. Every pair an
# ihc_checklist rule emits requires Histology and IHC and lists the markers of the rules that
# emit it (Group 8's 9364 precedent); check_ihc_overrides() fails the run when an override and
# the trees disagree.
# --------------------------------------------------------------------------------------
OVERRIDABLE = ("diagnostic_tests_required", "ihc_markers_required")

DECISIONS: dict[str, tuple] = {}

OBS_NOTE = (
    "In the inventory, never emitted: ICD-O-3.2 marks every term at this (code, behaviour) "
    "[obs], and an obsolete term stays off every screen (design D3). Where the WHO source "
    "names the current entity on the stem, a tree offers that entity's current code.")
OFF_TREE_NOTE = "In the inventory, not on the tree: no node of the Group XI trees emits it."


def check_ihc_overrides(markers_by_pair: dict) -> None:
    """Every pair a checklist rule emits requires Histology and IHC and lists exactly the
    markers of the rules that emit it; no other pair claims IHC or ihc_markers_required."""
    problems = []
    for k, d in DECISIONS.items():
        over = d[3] if len(d) > 3 else {}
        bad = set(over) - set(OVERRIDABLE)
        if bad:
            problems.append("%s overrides %s, which is not overridable"
                            % (k, ", ".join(sorted(bad))))
        if k in markers_by_pair:
            if over.get("diagnostic_tests_required") != HIST_IHC:
                problems.append("%s is emitted by a stain panel rule but does not require "
                                "Histology and IHC" % k)
            if over.get("ihc_markers_required") != markers_by_pair[k]:
                problems.append("%s ihc_markers_required is %r; the rules that emit it read %r"
                                % (k, over.get("ihc_markers_required"), markers_by_pair[k]))
        else:
            if "ihc_markers_required" in over:
                problems.append("%s lists ihc_markers_required but no stain panel rule emits "
                                "it" % k)
            if "IHC" in (over.get("diagnostic_tests_required") or []):
                problems.append("%s requires IHC but no stain panel rule emits it" % k)
    missing = sorted(set(markers_by_pair) - set(DECISIONS))
    if missing:
        problems.append("stain panel rule(s) emit %s, which DECISIONS does not annotate"
                        % ", ".join(missing))
    if problems:
        raise GenerationError("; ".join(problems))


def check_decision_evidence() -> None:
    """Every evidence file a DECISIONS entry names exists in docs/group_11_evidence/."""
    problems = []
    for k, d in DECISIONS.items():
        if len(d) < 3:
            problems.append("%s: a decision is (D-numbers, evidence file, sentence[, overrides])"
                            % k)
            continue
        for stem in (s.strip() for s in d[1].split(",")):
            if not (EVIDENCE_DIR / ("%s.json" % stem)).exists():
                problems.append("%s names evidence file %s, which docs/group_11_evidence/ does "
                                "not hold" % (k, stem))
    if problems:
        raise GenerationError("; ".join(problems))


# --------------------------------------------------------------------------------------
# Topography. ICCC-2017 stores topography as three-digit codes (C73.9 -> 739); the inventory
# carries each range as a display string ("C07.9–C08.9"), the REDCap list as three digits.
# --------------------------------------------------------------------------------------
def topo3(code: str) -> int:
    m = re.fullmatch(r"C(\d\d)\.(\d)", code.strip())
    if not m:
        raise ValueError("not a topography code: %r" % code)
    return int(m.group(1)) * 10 + int(m.group(2))


def span(display: str) -> tuple:
    parts = [p for p in re.split(r"[–-]", display) if p.strip()]
    return topo3(parts[0]), topo3(parts[-1])


def covers(displays: list, number: int) -> bool:
    for d in displays:
        lo, hi = span(d)
        if lo <= number <= hi:
            return True
    return False


def ascii_range(display: str) -> str:
    return display.replace("–", "-")


def subgroup_order(sid: str) -> tuple:
    """XIa, XIb, ... XIf1, XIf2, ... XIf9, XIf10, XIf11: the ICCC-3 order, not string order."""
    m = re.fullmatch(r"(\D+?)(\d*)", sid)
    return (m.group(1), int(m.group(2) or 0)) if m else (sid, 0)


def load_lookup() -> dict:
    """data/shared/topography_codes.json's topography_lookup, read once per run."""
    return json.loads(LOOKUP_PATH.read_text(encoding="utf-8"))["topography_lookup"]


def read_redcap_topography(path: Path) -> list:
    """Every code in the first fenced block of Layer 1's REDCap topography list, converted from
    the three-digit REDCap form (739) to C73.9, in file order."""
    if not path.exists():
        raise GenerationError("Layer 1's REDCap topography list is not at %s; set ICD_LAYER1"
                              % path)
    lines = path.read_text(encoding="utf-8").splitlines()
    fences = [i for i, line in enumerate(lines) if line.strip().startswith("```")]
    if len(fences) < 2:
        raise GenerationError("%s holds no fenced code list" % path.name)
    out = []
    for line in lines[fences[0] + 1:fences[1]]:
        m = re.match(r"(\d{3}),", line.strip())
        if m:
            n = int(m.group(1))
            out.append("C%02d.%d" % (n // 10, n % 10))
    if not out:
        raise GenerationError("%s lists no three-digit topography code" % path.name)
    return out


def site_specific_ranges(records: list, redcap: list) -> list:
    """Every Group XI ICCC-2017 range display that is not 'any site'. A range is 'any site' when
    it covers every code in the REDCap list."""
    out = []
    for r in records:
        for t in r["topography"]:
            if t in out:
                continue
            if all(covers([t], topo3(c)) for c in redcap):
                continue
            out.append(t)
    return out


def routing_codes(lookup: dict, redcap: list, specific: list) -> tuple:
    """(codes, additions). codes: every lookup code, plus every REDCap code a site-specific
    Group XI range covers that the lookup lacks (the additions), in numeric order."""
    additions = [c for c in redcap if c not in lookup and covers(specific, topo3(c))]
    codes = sorted(set(lookup) | set(additions), key=topo3)
    return codes, additions


# --------------------------------------------------------------------------------------
# Subgroups.
# --------------------------------------------------------------------------------------
def subgroups_of(recs: list) -> dict:
    """{subgroup_id: {"name": ..., "topography": [display, ...]}} in ICCC-3 subgroup order."""
    out: dict = {}
    for r in recs:
        sub = out.setdefault(r["iccc3_subgroup_id"],
                             {"name": r["iccc3_subgroup_name"], "topography": []})
        if sub["name"] != r["iccc3_subgroup_name"]:
            raise GenerationError("subgroup %s carries two names for %s/%s"
                                  % (r["iccc3_subgroup_id"], r["morphology_code"],
                                     r["behavior_code"]))
        for t in r["topography"]:
            if t not in sub["topography"]:
                sub["topography"].append(t)
    return dict(sorted(out.items(), key=lambda kv: subgroup_order(kv[0])))


def default_subgroup(k: str, subs: dict) -> str:
    if len(subs) == 1:
        return next(iter(subs))
    if SHARED_DEFAULT in subs:
        return SHARED_DEFAULT
    raise GenerationError("%s sits in subgroups %s and none of them is %s, the shared-list "
                          "default" % (k, ", ".join(subs), SHARED_DEFAULT))


def routing(k: str, subs: dict, default: str, codes: list) -> tuple:
    """(rules, note) for a pair that ICCC-2017 places in more than one subgroup. One rule per
    subgroup other than the default, naming every code its ranges cover. The note says where
    the default and each rule apply, and what the output shows at a code outside every range
    of the pair."""
    for c in codes:
        hits = [sid for sid, sub in subs.items() if covers(sub["topography"], topo3(c))]
        if len(hits) > 1:
            raise GenerationError("%s: ICCC-2017 places it in %s at %s; a code claimed by two "
                                  "subgroups would make rule order decide the subgroup"
                                  % (k, " and ".join(hits), c))
    rules = []
    for sid, sub in subs.items():
        if sid == default:
            continue
        listed = [c for c in codes if covers(sub["topography"], topo3(c))]
        if not listed:
            raise GenerationError("%s: subgroup %s covers no topography code" % (k, sid))
        rules.append({"topography_in": listed, "iccc3_subgroup_id": sid,
                      "iccc3_subgroup_name": sub["name"]})

    def ranges(sid):
        return ", ".join(ascii_range(t) for t in subs[sid]["topography"])

    text = ("The entry's own subgroup, %s, is the default (contract §2, design D11) and "
            "applies at its sites (%s); the ordered rules name %s, where ICCC-2017 places this "
            "(code, behaviour) instead."
            % (default, ranges(default),
               join_and(["%s at %s" % (r["iccc3_subgroup_id"], ranges(r["iccc3_subgroup_id"]))
                         for r in rules])))
    uncovered = [c for c in codes
                 if not any(covers(sub["topography"], topo3(c)) for sub in subs.values())]
    if uncovered:
        at = (uncovered[0] if len(uncovered) == 1 else
              "the %d lookup codes outside this code's site ranges (e.g. %s)"
              % (len(uncovered), uncovered[0]))
        text += (" At %s, ICCC-2017 places this code in no Group XI subgroup and the output "
                 "shows %s, the default (design D11: a specified site outside every Group XI "
                 "range)." % (at, default))
    return rules, text


# --------------------------------------------------------------------------------------
# ICD-O-3.2 status.
# --------------------------------------------------------------------------------------
def load_icdo_index() -> dict:
    """{(code, behaviour): {term: (level, obs)}} from icdo32.sqlite (build_database's reader)."""
    index, err = bd.load_icdo32(ICDO_PATH.parent.parent)
    if err:
        raise GenerationError(err)
    return index


def all_obs(index: dict, k: str) -> bool:
    terms = index.get(tuple(k.split("/")), {})
    return bool(terms) and all(obs for _level, obs in terms.values())


def preferred_obs(index: dict, k: str) -> bool:
    terms = index.get(tuple(k.split("/")), {})
    return any(level == "Preferred" and obs for level, obs in terms.values())


def live_terms(index: dict, k: str) -> list:
    """'Synonym Melanoma arising in blue nevus' for every term ICD-O-3.2 does not mark [obs]."""
    terms = index.get(tuple(k.split("/")), {})
    return ["%s %s" % (level, term) for term, (level, obs) in terms.items() if not obs]


# --------------------------------------------------------------------------------------
# Standing rule 3 additions.
# --------------------------------------------------------------------------------------
def iccc_holds(code: str) -> list:
    """Every ICCC-2017 subgroup whose ranges list the code, in any main group."""
    con = sqlite3.connect("file:%s?mode=ro" % ICCC_PATH, uri=True)
    try:
        return [r[0] for r in con.execute(
            "SELECT g.group_code FROM morphology_codes mc JOIN groups g "
            "ON g.group_id = mc.group_id WHERE mc.code = ?", (code,))]
    finally:
        con.close()


def rule3_records(records: list, specific: list, index: dict) -> dict:
    """{(code, behaviour): [record]} for RULE3_ADDITIONS. Each record is shaped like an
    inventory record: the Preferred term from icdo32.sqlite, and the subgroup's name and
    site-specific range from the inventory's records of that subgroup."""
    out = {}
    for k, sid in RULE3_ADDITIONS.items():
        code, beh = k.split("/")
        terms = index.get((code, beh), {})
        preferred = [t for t, (level, obs) in terms.items() if level == "Preferred"]
        if not preferred:
            raise GenerationError("%s: icdo32.sqlite prints no Preferred term" % k)
        if preferred_obs(index, k):
            raise GenerationError("%s: icdo32.sqlite marks the Preferred term [obs]" % k)
        held = iccc_holds(code)
        if held:
            raise GenerationError("%s: ICCC-2017 lists the code in %s, so standing rule 3 does "
                                  "not apply" % (k, ", ".join(held)))
        own = [r for r in records if r["iccc3_subgroup_id"] == sid]
        if not own:
            raise GenerationError("%s: no inventory record carries subgroup %s" % (k, sid))
        topography = []
        for r in own:
            for t in r["topography"]:
                if t in specific and t not in topography:
                    topography.append(t)
        if not topography:
            raise GenerationError("%s: subgroup %s has no site-specific ICCC-2017 range"
                                  % (k, sid))
        out[(code, beh)] = [{
            "morphology_code": code,
            "behavior_code": beh,
            "preferred_term": preferred[0],
            "iccc3_subgroup_id": sid,
            "iccc3_subgroup_name": own[0]["iccc3_subgroup_name"],
            "topography": topography,
        }]
    return out


def rule_f_records(records: list, specific: list, index: dict) -> dict:
    """{(code, behaviour): [record]} for RULE_F_ADDITIONS, shaped like rule3_records(): the name
    is the code's Preferred term at the behaviour ICD-O-3.2 prints (the matrix rule's anchor)."""
    from build_database import ICDO32_MATRIX_RULE
    out = {}
    for k, sid in RULE_F_ADDITIONS.items():
        code, beh = k.split("/")
        if index.get((code, beh)):
            raise GenerationError("%s: icdo32.sqlite prints the pair; Rule F needs no addition"
                                  % k)
        rule = ICDO32_MATRIX_RULE.get((11, code, beh))
        if not rule:
            raise GenerationError("%s: build_database.ICDO32_MATRIX_RULE does not hold the pair"
                                  % k)
        src = index.get((code, rule[0]), {})
        if src.get(rule[1], ("", ""))[0] != "Preferred":
            raise GenerationError("%s: %r is not the Preferred term at %s/%s"
                                  % (k, rule[1], code, rule[0]))
        if sid not in " ".join(iccc_holds(code)):
            raise GenerationError("%s: ICCC-2017 does not place %s in %s (it lists %s)"
                                  % (k, code, sid, iccc_holds(code)))
        own = [r for r in records if r["iccc3_subgroup_id"] == sid]
        topography = []
        for r in own:
            for t in r["topography"]:
                if t in specific and t not in topography:
                    topography.append(t)
        out[(code, beh)] = [{
            "morphology_code": code,
            "behavior_code": beh,
            "preferred_term": rule[1],
            "iccc3_subgroup_id": sid,
            "iccc3_subgroup_name": own[0]["iccc3_subgroup_name"],
            "topography": topography,
        }]
    return out


# --------------------------------------------------------------------------------------
# Entries.
# --------------------------------------------------------------------------------------
def build_entry(recs: list, index: dict, codes: list, where: dict) -> dict:
    first = recs[0]
    code, beh = first["morphology_code"], first["behavior_code"]
    k = key(code, beh)
    name = first["preferred_term"]
    if not name:
        raise GenerationError("%s has no Preferred term in icdo32.sqlite" % k)
    subs = subgroups_of(recs)
    default = default_subgroup(k, subs)

    sites = []
    for sub in subs.values():
        for t in sub["topography"]:
            t = ascii_range(t)
            if t not in sites:
                sites.append(t)

    e = {f: None for f in FIELD_ORDER}
    e.update({
        "morphology_code": code,
        "morphology_name": name,
        "iccc3_subgroup_id": default,
        "iccc3_subgroup_name": subs[default]["name"],
        "who_version": "ICD-O-3.2",
        "behavior_code": beh,
        "diagnostic_tests_required": list(HISTOLOGY),
        "imaging_sufficient": False,
        "clinical_alert": None,
        "code_neutral_molecular": True,
        "redcap_value": code,
        "primary_sites": sites,
        "topography_dependent": False,
    })
    rules = None
    if len(subs) > 1:
        rules, e["topography_routing_note"] = routing(k, subs, default, codes)
        e["topography_dependent"] = True

    origin = ("New in ICD-O-3.2 and outside every ICCC-2017 range; standing rule 3 places it "
              "in Group XI, in %s by site (design D11)." % default
              if k in RULE3_ADDITIONS else
              "ICD-O-3.2 prints this code at another behaviour only; the pathologist's stated "
              "behaviour is recorded with the code's own name (WHO coding Rule F; registrar, "
              "8 October 2026, review A6; build_database.ICDO32_MATRIX_RULE)."
              if k in RULE_F_ADDITIONS else "")
    nodes = where.get(k) or []
    if k in DECISIONS:
        refs, files, sentence = DECISIONS[k][:3]
        if len(DECISIONS[k]) > 3:
            e.update(copy.deepcopy(DECISIONS[k][3]))
        e["coding_note"] = note(
            GENERATED_NOTE,
            "ICD-O-3.2 preferred term at /%s is %r." % (beh, name),
            origin,
            sentence,
            "Evidence: %s." % ", ".join("docs/group_11_evidence/%s.json" % s.strip()
                                        for s in files.split(",")),
            "Emitted by %s (design %s)." % (describe_emitters(nodes), refs))
    elif nodes:
        # Only the picker's pairs reach here: build_entries() fails on any other emitted pair
        # that DECISIONS does not annotate.
        e["coding_note"] = note(
            GENERATED_NOTE,
            "ICD-O-3.2 preferred term %r, behaviour %s." % (name, beh),
            origin,
            "Emitted by %s (the Group XI picker, design D2)." % describe_emitters(nodes))
    elif all_obs(index, k):
        e["coding_note"] = note(
            GENERATED_NOTE,
            "ICD-O-3.2 preferred term %r, behaviour %s." % (name, beh),
            OBS_NOTE)
    elif preferred_obs(index, k):
        e["coding_note"] = note(
            GENERATED_NOTE,
            "ICD-O-3.2 preferred term %r, behaviour %s, is marked [obs]; the live term(s) on "
            "the stem: %s." % (name, beh, "; ".join(live_terms(index, k))),
            "In the inventory, not on the tree: a code whose Preferred term is [obs] is held "
            "off every screen and listed for the registrar (design D3).")
    else:
        e["coding_note"] = note(
            GENERATED_NOTE,
            "ICD-O-3.2 preferred term %r, behaviour %s." % (name, beh),
            origin,
            OFF_TREE_NOTE)

    # Group 3's 9380 entry puts the rule list straight after topography_routing_note.
    if rules is not None:
        e["iccc3_subgroup_by_topography"] = rules
    return e


def build_entries(payload: dict, index: dict, codes: list, specific: list,
                  trees: list) -> list:
    records = payload["records"]
    if len(records) != EXPECTED_RECORDS:
        raise GenerationError("the inventory holds %d (code, behaviour) records, the contract "
                              "expects %d" % (len(records), EXPECTED_RECORDS))
    grouped: dict = defaultdict(list)
    for r in records:
        grouped[(r["morphology_code"], r["behavior_code"])].append(r)
    if len(grouped) != EXPECTED_INVENTORY_PAIRS:
        raise GenerationError("the records collapse to %d (code, behaviour) pairs, the contract "
                              "expects %d" % (len(grouped), EXPECTED_INVENTORY_PAIRS))

    obs_pairs = sorted(key(c, b) for c, b in grouped if all_obs(index, key(c, b)))
    if tuple(obs_pairs) != ALL_OBS_EXPECTED:
        raise GenerationError("icdo32.sqlite marks every term [obs] at %s; the contract (§0.2, "
                              "design D3) names %s"
                              % (", ".join(obs_pairs), ", ".join(ALL_OBS_EXPECTED)))

    added = rule3_records(records, specific, index)
    if set(added) & set(grouped):
        raise GenerationError("standing rule 3 adds %s, which the inventory already holds"
                              % ", ".join(key(c, b) for c, b in sorted(set(added) & set(grouped))))
    grouped.update(added)
    added_f = rule_f_records(records, specific, index)
    if set(added_f) & set(grouped):
        raise GenerationError("Rule F adds %s, which the inventory already holds"
                              % ", ".join(key(c, b) for c, b in sorted(set(added_f) & set(grouped))))
    grouped.update(added_f)
    if len(grouped) != EXPECTED_ENTRIES:
        raise GenerationError("%d entries; the contract expects %d"
                              % (len(grouped), EXPECTED_ENTRIES))

    entries_keys = {key(c, b) for c, b in grouped}
    where = emitters(trees)
    emitted = set(where)
    picker = picker_pairs(trees)
    problems = []
    if emitted - entries_keys:
        problems.append("a tree names pair(s) outside the entries: %s"
                        % ", ".join(sorted(emitted - entries_keys)))
    if set(DECISIONS) - entries_keys:
        problems.append("annotated pair(s) absent from the entries: %s"
                        % ", ".join(sorted(set(DECISIONS) - entries_keys)))
    off_screen = sorted(p for p in emitted if p in entries_keys and preferred_obs(index, p))
    if off_screen:
        problems.append("a tree emits %s, whose Preferred term ICD-O-3.2 marks [obs]; design D3 "
                        "keeps it off every screen" % ", ".join(off_screen))
    if emitted - set(DECISIONS) - picker:
        problems.append("emitted pair(s) with no DECISIONS entry: %s"
                        % ", ".join(sorted(emitted - set(DECISIONS) - picker)))
    if set(DECISIONS) - emitted:
        problems.append("DECISIONS entry for pair(s) no tree emits: %s"
                        % ", ".join(sorted(set(DECISIONS) - emitted)))
    if problems:
        raise GenerationError("; ".join(problems))
    check_decision_evidence()
    check_ihc_overrides(checklist_markers(trees))

    return [build_entry(grouped[k], index, codes, where)
            for k in sorted(grouped, key=lambda k: (k[0], k[1] != "3", k[1]))]


def build_metadata(entries: list, summary: dict, trees: list) -> dict:
    n_nodes = sum(len(t.get("nodes") or []) for t in trees)
    shared = sum(1 for e in entries if e["topography_dependent"])
    return {
        "group_id": GROUP,
        "group_name": "Other Malignant Epithelial Neoplasms and Malignant Melanomas",
        "iccc3_version": "3rd edition",
        "icdo_version": (
            "ICD-O-3.2. morphology_entries[] is GENERATED by build/generate_group11_entries.py"
            " from ICCC-2017.sqlite joined to icdo32.sqlite (contract §2). Generator summary:"
            " ICCC range entries %d, distinct codes %d, absent from ICD-O-3.2 at a declared"
            " behaviour %d, usable %d, (code,behaviour) records %d, grouped by (code,"
            " behaviour) into %d pairs, plus %s by standing rule 3 (design D11): %d entries."
            " %d of those pairs sit in more than one subgroup by site and carry"
            " iccc3_subgroup_by_topography."
            % (summary["iccc_code_range_entries"], summary["iccc_distinct_codes"],
               len(summary["codes_absent_from_icdo32"]), summary["usable_distinct_codes"],
               summary["morphology_entry_records"], len(entries) - len(RULE3_ADDITIONS),
               join_and(sorted(RULE3_ADDITIONS)), len(entries), shared)
        ),
        "total_morphology_entries": len(entries),
        "total_decision_nodes": n_nodes,
        "decision_trees": [t["tree_id"] for t in trees],
        "basis_of_diagnosis_declarations": dict(bd.BASIS_DECLARED_GAPS),
    }


def report(entries: list, additions: list) -> None:
    by_default: dict = defaultdict(int)
    for e in entries:
        by_default[e["iccc3_subgroup_id"]] += 1
    print("entries: %d · topography-dependent: %d · default subgroup: %s"
          % (len(entries), sum(1 for e in entries if e["topography_dependent"]),
             ", ".join("%s %d" % (sid, by_default[sid])
                       for sid in sorted(by_default, key=subgroup_order))))
    print("routing codes from Layer 1's REDCap list that the lookup lacks: %d" % len(additions))


def main(argv=None) -> int:
    try:
        return run(argv)
    except GenerationError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2


def run(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="write nothing; exit 1 when the file on disk would change")
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args(argv)

    try:
        trees = group11_tree.trees()
        DECISIONS.clear()
        DECISIONS.update(group11_tree.decisions())
    except group11_tree.TreeError as exc:
        raise GenerationError(str(exc)) from None
    payload = gi.build_inventory(ICCC_PATH, ICDO_PATH, ICCC_GROUP)
    index = load_icdo_index()
    redcap = read_redcap_topography(REDCAP_TOPOGRAPHY)
    specific = site_specific_ranges(payload["records"], redcap)
    codes, additions = routing_codes(load_lookup(), redcap, specific)
    entries = build_entries(payload, index, codes, specific, trees)

    out_path = Path(args.out)
    existing = None
    if out_path.exists():
        try:
            text = out_path.read_text(encoding="utf-8")
            carry_branch_sequences(trees, json.loads(text).get("decision_trees"))
            existing = text
        except (json.JSONDecodeError, OSError) as exc:
            print("ERROR: %s exists but could not be read (%s); refusing to overwrite it"
                  % (out_path, exc), file=sys.stderr)
            return 2
    doc = {
        "metadata": build_metadata(entries, payload["summary"], trees),
        "morphology_entries": entries,
        "decision_trees": trees,
    }
    # The "Evidence in file" gates become document checklists (registrar, 6 October 2026). The
    # rules live in docs/evidence_documents/group_11.json, which the data gate compares with
    # this file, so they are applied here rather than written into the trees. Task T2 writes
    # that file with the trees; until then there is nothing to apply.
    # Under G11_ONLY (one implementer building its own trees while others are written), the
    # committed map names gates this run does not build, so the mapping is computed from the
    # trees built here instead. A full run applies the committed file, which the data gate checks.
    if os.environ.get("G11_ONLY"):
        import group11_common as _common
        problems = evidence.apply(doc, _common.evidence_mapping(trees))
        if problems:
            for p in problems:
                print("ERROR: %s" % p, file=sys.stderr)
            return 2
    elif EVIDENCE_MAP.exists():
        problems = evidence.apply(doc, json.loads(EVIDENCE_MAP.read_text(encoding="utf-8")))
        if problems:
            for p in problems:
                print("ERROR: %s" % p, file=sys.stderr)
            return 2
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        report(entries, additions)
        if existing == text:
            print("%s is up to date" % out_path)
            return 0
        print("%s would change" % out_path, file=sys.stderr)
        return 1

    out_path.write_text(text, encoding="utf-8")
    print("wrote %s (%d entries, %d node(s))"
          % (out_path, len(entries), doc["metadata"]["total_decision_nodes"]), file=sys.stderr)
    report(entries, additions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
