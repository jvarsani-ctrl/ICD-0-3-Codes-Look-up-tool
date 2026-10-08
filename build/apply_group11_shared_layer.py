#!/usr/bin/env python3
"""Write the Group XI shared layer: data/shared/topography_codes.json and
data/shared/presentation_router.json (Group 11 build contract §3, task T3).

    python3 build/apply_group11_shared_layer.py          # writes both files
    python3 build/apply_group11_shared_layer.py --check  # writes nothing; exit 1 if either would change

The script is idempotent: a second run on its own output writes nothing. It reads Layer 1 and
the TREES table in build/group11_common.py, which is the single source for the sites each Group
XI tree routes (contract §4.1). No site list is written here. In a git worktree set ICD_LAYER1,
ICCC_DB and ICDO_DB first (contract §1).

What it writes, in order:

1. topography_codes.json, topography_lookup.
   * Every routed Group XI site that the lookup lacks is added (153 codes on 8 October 2026).
     The label and the three-digit REDCap code are read from Layer 1's
     `RedCap Options/Topography Redcap.md`. One repair is applied to the label: the file
     prints an "ft" ligature as "!" ("so! palate", "Le! colon"), and the label is written with
     "ft", as the lookup already carries C69.6 ("Soft tissue of orbit"). C44.4 and C48.1 are
     absent from that file, so TREES does not route them and they are not added (contract
     §3.1).
   * A new code takes the shape 56 of the 57 codes that already list Group 11 use: code,
     label, redcap_code, coarse_organ, candidate_groups, candidate_groups_advisory. Its
     candidate_groups is [11]. No other group's tree_routing rule names a code the lookup
     lacked, so no route is removed. Group X's extragonadal rule is extended in step 4 to
     name the new codes ICCC-2017 places in Xb, as Group X's own build check requires; the
     front door does not list Group X at those sites (Group 10 registrar review B2).
   * Each code is inserted beside its numeric neighbours: after the nearest lower code, or
     before the nearest higher code where only that one shares the code's three-character
     category.
   * Group 11 is appended to the candidate_groups list of every routed code that lacks it
     (57 codes). The eight codes whose candidate_groups is the string "route_by_morphology"
     (C76.0-C76.2, C76.4, C76.5, C76.7, C76.8, C80.9) are left as they are: app.js
     narrowBySite() and afterSearchSite() leave the candidates unfiltered there, so every
     group already passes.
   No other field of an existing code changes.

2. topography_codes.json, coarse_organ_crosswalk. app.js renderSite() offers only crosswalk
   rows, so every new code sits in one row. A code joins an existing row when that row's
   topography_range names the code's whole three-character category (C24.1 joins
   biliary_extrahepatic, "C24"). The rest go to the rows in NEW_ROWS, which group them by
   organ; each new row's topography_range and codes are computed from the codes it receives.
   New rows are inserted before ill_defined_sites, so the ill-defined and unknown primary
   rows stay last.

3. presentation_router.json, groups["11"], in the shape of groups["10"]: built,
   occurs_at_routed_sites, one trees[] item per TREES row with entry node
   "<prefix>document_inventory", one tree_routing rule per TREES row that has sites (the
   melanoma tree has none: design D13), the default g11_unspecified and the handoff.

4. presentation_router.json, groups["10"].tree_routing. Group X RULE 4
   (build_database.check_group10_subgroups_and_routing) requires the extragonadal rule to
   name every lookup code in ICCC-2017's Xb site ranges, so each lookup code in those ranges
   that no Group X rule names is added to it, in numeric order. Nothing is removed.

5. presentation_router.json, dual_group_rules["8158"] and ["8290"]. One branch per Group XI
   subgroup ICCC-2017 gives the code (behaviour 3), naming the lookup codes in that
   subgroup's site range: 8158 is XIa at C74.0, XIb at C73.9, XIf1 to XIf11 by site; 8290 is
   XIb at C73.9, XIc at C11, XIf1 to XIf11 by site. The existing branches (C75.1, Group III;
   C22, Group VII) and the defaults are not touched, and no kidney or gonad branch is added
   (contract §3.2). The new branches carry no `note`: app.js reads resolveGroup() only for
   `note`, the subgroup line already shows the subgroup, and a second line would cost the
   clerk attention without changing the code.

After writing, the script checks its own result and prints what it finds: both files load;
every Group 11 routing code is in the lookup and lists 11 (or is "route_by_morphology"); no
code is in two Group 11 rules; every lookup code sits in one crosswalk row, the row its
coarse_organ names; every lookup code that lists 11 is named by a rule, or is reported by name;
and the lookup codes a Group 11 case reaches only by a referral hop are listed.

Two generators compute subgroup lists from the lookup and must run after this script:

    python3 build/generate_group10_entries.py   # the 18 Group X entries' Xb topography lists
    python3 build/generate_group11_entries.py   # every Group XI entry's subgroup lists
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import group11_common as c  # noqa: E402

TOPO_PATH = REPO / "data" / "shared" / "topography_codes.json"
ROUTER_PATH = REPO / "data" / "shared" / "presentation_router.json"

GROUP = 11
GROUP_NAME = "Other Malignant Epithelial Neoplasms and Malignant Melanomas"
DEFAULT_TREE = "g11_unspecified"
DEFAULT_LABEL = "Another or unspecified site"
DUAL_RULE_CODES = ("8158", "8290")
TOPO_RE = re.compile(r"^C\d\d\.\d$")

# The organ rows a new code goes to when no existing crosswalk row takes its category.
# (organ key, clerk-facing label, ICD-O-3 three-character categories). The codes come from
# TREES; a category here only says which row a code joins.
NEW_ROWS = (
    ("lip_oral_cavity", "Lip and oral cavity", "C00-C06"),
    ("salivary_glands", "Major salivary glands", "C07-C08"),
    ("tonsil_oropharynx_hypopharynx", "Tonsil, oropharynx and hypopharynx", "C09-C10,C12-C14"),
    ("oesophagus", "Oesophagus", "C15"),
    ("stomach", "Stomach", "C16"),
    ("small_intestine", "Small intestine", "C17"),
    ("colon_appendix_rectum_anus", "Colon, appendix, rectum and anus", "C18-C21"),
    ("gallbladder", "Gallbladder", "C23"),
    ("pancreas", "Pancreas", "C25"),
    ("digestive_other", "Other and unspecified digestive organs", "C26"),
    ("larynx_trachea", "Larynx and trachea", "C32-C33"),
    ("heart_pleura_thorax", "Heart, pleura and other thoracic sites", "C38-C39"),
    ("breast", "Breast", "C50"),
    ("female_genital_adnexa", "Fallopian tube, ligaments and other female genital organs", "C57"),
    ("penis", "Penis", "C60"),
    ("urinary_tract_other", "Renal pelvis, ureter and urethra", "C65-C66,C68"),
    ("endocrine_other", "Parathyroid and other endocrine glands", "C75"),
)
NEW_ROWS_BEFORE = "ill_defined_sites"


class ApplyError(Exception):
    """The shared layer cannot be written as specified; exit 2."""


def n(code: str) -> int:
    """'C56.9' -> 569."""
    return c._topo3(code)


def category(code: str) -> int:
    return int(code[1:3])


def _categories(spec: str) -> set:
    out = set()
    for token in (t.strip() for t in spec.split(",") if t.strip()):
        ends = token.split("-")
        out.update(range(int(ends[0][1:3]), int(ends[-1][1:3]) + 1))
    return out


# ------------------------------------------------------------------------------------------
# Layer 1
# ------------------------------------------------------------------------------------------
def redcap_topography() -> dict:
    """{C-code: (three-digit code, label)} from the first fenced block of Layer 1's REDCap
    topography list, the block group11_common.redcap_topography() reads."""
    path = c._layer1_path() / "RedCap Options" / "Topography Redcap.md"
    if not path.exists():
        raise ApplyError("Layer 1's REDCap topography list is not at %s - set ICD_LAYER1" % path)
    lines = path.read_text(encoding="utf-8").splitlines()
    fences = [i for i, line in enumerate(lines) if line.strip().startswith("```")]
    if len(fences) < 2:
        raise ApplyError("%s holds no fenced code list" % path.name)
    out = {}
    for line in lines[fences[0] + 1:fences[1]]:
        m = re.match(r"(\d{3}),\s?(.*\S)\s*$", line.strip())
        if m:
            label = re.sub(r"(?<=[A-Za-z])!", "ft", m.group(2))
            out[c._c(int(m.group(1)))] = (m.group(1), label)
    if sorted(out, key=n) != sorted(c.redcap_topography(), key=n):
        raise ApplyError("the REDCap topography list read here disagrees with "
                         "group11_common.redcap_topography()")
    return out


_ICCC_ROWS: list | None = None


def iccc_rows() -> list:
    """(code, main_group, subgroup, subgroup label, spans, behaviours) for every ICCC-2017
    range a code sits in (the code_lookup view)."""
    global _ICCC_ROWS
    if _ICCC_ROWS is None:
        path = c._iccc_path()
        if not path.exists():
            raise ApplyError("ICCC-2017.sqlite not found at %s - set ICCC_DB" % path)
        con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
        try:
            _ICCC_ROWS = [
                (str(code), str(main), str(sub), str(label), c._spans(topo), str(beh), str(topo))
                for code, main, sub, label, topo, beh in con.execute(
                    "SELECT code, main_group, group_code, group_label, topography_raw, behavior "
                    "FROM code_lookup")]
        finally:
            con.close()
    return _ICCC_ROWS


def _declares_3(beh: str) -> bool:
    for part in beh.split(","):
        ends = part.strip().split("-")
        if ends[0] and int(ends[0]) <= 3 <= int(ends[-1]):
            return True
    return False


def group10_site_families() -> dict:
    """{'Xa'|'Xb'|'Xc': spans} — the union of the site ranges of every ICCC-2017 Group X range
    in each germ cell family, the way build_database._group10_iccc_ranges() reads them."""
    path = c._iccc_path()
    con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    out: dict = {"Xa": [], "Xb": [], "Xc": []}
    try:
        for sub, sites in con.execute(
                "SELECT g.group_code, cr.icdo3_primary_site_raw FROM code_ranges cr "
                "JOIN groups g ON g.group_id = cr.group_id WHERE g.main_group = 'X'"):
            if str(sub)[:2] in out:
                out[str(sub)[:2]].extend(c._spans(sites))
    finally:
        con.close()
    return out


def _in(spans, value: int) -> bool:
    return any(lo <= value <= hi for lo, hi in spans)


# ------------------------------------------------------------------------------------------
# 1-2. topography_codes.json
# ------------------------------------------------------------------------------------------
def _insert_position(keys: list, code: str) -> int:
    codes = [k for k in keys if TOPO_RE.match(k)]
    lower = max((k for k in codes if n(k) < n(code)), key=n, default=None)
    higher = min((k for k in codes if n(k) > n(code)), key=n, default=None)
    if lower is None or (higher is not None and category(higher) == category(code)
                         and category(lower) != category(code)):
        return keys.index(higher)
    return keys.index(lower) + 1


def _range_text(codes: list, redcap: dict) -> str:
    """['C00.0', ..., 'C06.9'] -> 'C00-C06'; a category the row holds only in part is written
    as runs of consecutive REDCap codes ('C57.0-C57.7, C57.9')."""
    order = sorted(redcap, key=n)
    pos = {k: i for i, k in enumerate(order)}
    held = set(codes)
    parts, cats = [], sorted({category(k) for k in codes})
    whole = [k for k in cats if {r for r in redcap if category(r) == k} <= held]
    i = 0
    while i < len(cats):
        cat = cats[i]
        if cat in whole:
            j = i
            while j + 1 < len(cats) and cats[j + 1] == cats[j] + 1 and cats[j + 1] in whole:
                j += 1
            parts.append("C%02d" % cat if i == j else "C%02d-C%02d" % (cat, cats[j]))
            i = j + 1
            continue
        mine = sorted((k for k in codes if category(k) == cat), key=n)
        run = [mine[0]]
        for k in mine[1:]:
            if pos[k] == pos[run[-1]] + 1:
                run.append(k)
            else:
                parts.append(run[0] if len(run) == 1 else "%s-%s" % (run[0], run[-1]))
                run = [k]
        parts.append(run[0] if len(run) == 1 else "%s-%s" % (run[0], run[-1]))
        i += 1
    return ", ".join(parts)


def _row_takes_category(row: dict, cat: int) -> bool:
    """True when the row's topography_range names the whole category: 'C24', 'C40-C41'."""
    for token in re.split(r"[,\s]+", str(row.get("topography_range") or "")):
        m = re.fullmatch(r"C(\d\d)(?:-C(\d\d))?", token.strip())
        if m and int(m.group(1)) <= cat <= int(m.group(2) or m.group(1)):
            return True
    return False


def apply_topography(topo: dict, trees: list, redcap: dict) -> dict:
    out = copy.deepcopy(topo)
    lookup = out["topography_lookup"]
    cross = out["coarse_organ_crosswalk"]
    routed = [s for row in trees for s in row["sites"]]

    # 1. New codes, and Group 11 on the routed codes that lack it.
    new = [s for s in routed if s not in lookup]
    for code in new:
        if code not in redcap:
            raise ApplyError("%s is routed but absent from the REDCap topography list" % code)
    row_of = {}
    for code in new:
        cat = category(code)
        row = next((r for r in cross if _row_takes_category(r, cat)), None)
        if row is None:
            hit = [spec for spec in NEW_ROWS if cat in _categories(spec[2])]
            if len(hit) != 1:
                raise ApplyError("%s: %d NEW_ROWS rows take category C%02d" % (code, len(hit), cat))
            row_of[code] = hit[0][0]
        else:
            row_of[code] = row["organ"]

    items = list(lookup.items())
    for code in sorted(new, key=n):
        rc, label = redcap[code]
        entry = {"code": code, "label": label, "redcap_code": rc, "coarse_organ": row_of[code],
                 "candidate_groups": [GROUP], "candidate_groups_advisory": True}
        items.insert(_insert_position([k for k, _v in items], code), (code, entry))
    lookup = dict(items)
    out["topography_lookup"] = lookup

    for code in routed:
        cg = lookup[code].get("candidate_groups")
        if isinstance(cg, list) and GROUP not in cg:
            cg.append(GROUP)

    # 2. Crosswalk rows.
    for row in cross:
        mine = [k for k in new if row_of[k] == row["organ"]]
        if mine:
            row["codes"] = sorted(set(row["codes"]) | set(mine), key=n)
    have = {r["organ"] for r in cross}
    added = []
    for organ, label, _cats in NEW_ROWS:
        mine = sorted((k for k in new if row_of[k] == organ), key=n)
        if organ in have or not mine:
            continue
        added.append({"organ": organ, "topography_range": _range_text(mine, redcap),
                      "codes": mine, "candidate_groups": [GROUP], "label": label})
    if added:
        at = next((i for i, r in enumerate(cross) if r.get("organ") == NEW_ROWS_BEFORE), len(cross))
        cross[at:at] = added
    return out


# ------------------------------------------------------------------------------------------
# 3-5. presentation_router.json
# ------------------------------------------------------------------------------------------
ROUTING_COMMENT = (
    "Group XI keeps one tree per organ or site family (registrar, 8 October 2026, approach 3; "
    "Group 11 build contract §0.6 and §4.1), and the Stage 1 topography picks the tree, so the "
    "clerk is asked nothing extra. build/apply_group11_shared_layer.py writes these rules from "
    "the TREES table in build/group11_common.py, whose site ranges are expanded against Layer 1's "
    "REDCap topography list; C44.4 and C48.1 are not in that list and are not routed (contract "
    "§3.1). The melanoma tree, g11_melanoma, has no rule: every tree's histology screen reaches "
    "it by a cross-tree next_node (design D13). The group is marked occurs_at_routed_sites, as "
    "Group X is: the express lane enters a term filed under Group XI alone at a site a rule "
    "names when one of the term's entries lists the site in primary_sites.")


def group11_block(trees: list, lookup: dict) -> dict:
    rules = []
    for row in trees:
        if not row["sites"]:
            continue
        missing = [s for s in row["sites"] if s not in lookup]
        if missing:
            raise ApplyError("%s routes %s, which the lookup lacks" % (row["tree_id"], missing))
        rules.append({"topography_in": list(row["sites"]), "tree_id": row["tree_id"],
                      "entry_node": row["prefix"] + "document_inventory", "label": row["label"]})
    named = {s for r in rules for s in r["topography_in"]}
    unnamed = sorted((k for k, v in lookup.items()
                      if isinstance(v.get("candidate_groups"), list)
                      and GROUP in v["candidate_groups"] and k not in named), key=n)
    reason = ("Every lookup code that lists Group 11 is named by a rule; app.js requires a "
              "default.")
    if unnamed:
        reason = ("Every lookup code that lists Group 11 is named by a rule except %s, which no "
                  "Group XI tree routes (contract §4.1) and which reaches this default; app.js "
                  "requires a default." % ", ".join(unnamed))
    default_row = c.tree_row(DEFAULT_TREE)
    entry = default_row["prefix"] + "document_inventory"
    return {
        "name": GROUP_NAME,
        "built": True,
        "occurs_at_routed_sites": True,
        "trees": [{"tree_id": row["tree_id"], "entry_node": row["prefix"] + "document_inventory"}
                  for row in trees],
        "tree_routing": {
            "_comment": ROUTING_COMMENT,
            "variable": "topography",
            "rules": rules,
            "default": {"tree_id": DEFAULT_TREE, "entry_node": entry, "label": DEFAULT_LABEL,
                        "reason": reason},
        },
        "handoff": {"group": GROUP, "tree_id": DEFAULT_TREE, "entry_node": entry},
    }


def extend_group10_xb(router: dict, lookup: dict) -> list:
    """Add to Group X's extragonadal rule every lookup code in ICCC-2017's Xb site ranges that
    no Group X rule names. Returns the codes added."""
    tr = router["groups"]["10"]["tree_routing"]
    xb_rule = [r for r in tr["rules"] if r.get("tree_id") == "g10_extragonadal"]
    if len(xb_rule) != 1:
        raise ApplyError("groups['10'].tree_routing has %d g10_extragonadal rules" % len(xb_rule))
    xb_rule = xb_rule[0]
    fam = group10_site_families()
    named = {t for r in tr["rules"] for t in r.get("topography_in") or []}
    add = []
    for code in lookup:
        if not TOPO_RE.match(code) or code in named:
            continue
        v = n(code)
        if _in(fam["Xa"], v):
            continue
        if _in(fam["Xb"], v):
            add.append(code)
    if add:
        xb_rule["topography_in"] = sorted(set(xb_rule["topography_in"]) | set(add), key=n)
    return sorted(add, key=n)


def dual_branches(code: str, lookup: dict) -> list:
    """One branch per Group XI subgroup ICCC-2017 gives (code, behaviour 3)."""
    topos = sorted((k for k in lookup if TOPO_RE.match(k)), key=n)
    out = []
    rows = sorted((r for r in iccc_rows() if r[0] == code and r[1] == c.ICCC_GROUP
                   and _declares_3(r[5])), key=lambda r: _subgroup_key(r[2]))
    for _code, _main, sub, label, spans, _beh, raw in rows:
        sites = [k for k in topos if _in(spans, n(k))]
        if not sites:
            continue
        out.append({
            "when": {"topography_in": sites},
            "result": {"group": GROUP, "subgroup": sub},
            "authoring_note": (
                "ICCC-2017 places %s at %s %s, behaviour 3, in subgroup %s, %s. Written by "
                "build/apply_group11_shared_layer.py in the Group XI build, 8 October 2026, from "
                "ICCC-2017.sqlite against topography_codes.json. The branch changes nothing on "
                "screen: app.js reads resolveGroup() only for `note`, and this branch has none."
                % (code, "sites" if re.search(r"[,-]", raw) else "site", raw, sub, label)),
        })
    return out


def _subgroup_key(sub: str):
    m = re.fullmatch(r"([IVX]+)([a-z]?)(\d*)", sub)
    return (m.group(2), int(m.group(3) or 0)) if m else (sub, 0)


def apply_router(router: dict, trees: list, lookup: dict) -> tuple:
    out = copy.deepcopy(router)
    out["groups"][str(GROUP)] = group11_block(trees, lookup)
    xb_added = extend_group10_xb(out, lookup)
    for key in DUAL_RULE_CODES:
        rule = out["dual_group_rules"][key]
        if [str(x) for x in rule.get("codes") or []] != [key]:
            raise ApplyError("dual_group_rules[%r] does not hold exactly that code" % key)
        kept = [b for b in rule.get("branches") or []
                if (b.get("result") or {}).get("group") != GROUP]
        rule["branches"] = kept + dual_branches(key, lookup)
    return out, xb_added


# ------------------------------------------------------------------------------------------
# Checks on the result
# ------------------------------------------------------------------------------------------
def verify(topo: dict, router: dict, trees: list) -> list:
    """(level, message) findings; level 'FAIL' stops the write."""
    found = []
    lookup = topo["topography_lookup"]
    g11 = router["groups"][str(GROUP)]
    rules = g11["tree_routing"]["rules"]
    seen: dict = {}
    for r in rules:
        for code in r["topography_in"]:
            if code not in lookup:
                found.append(("FAIL", "%s (%s) is not in the lookup" % (code, r["tree_id"])))
                continue
            cg = lookup[code].get("candidate_groups")
            if not (cg == "route_by_morphology" or (isinstance(cg, list) and GROUP in cg)):
                found.append(("FAIL", "%s (%s) does not list 11: %r" % (code, r["tree_id"], cg)))
            if code in seen:
                found.append(("FAIL", "%s is in two Group 11 rules: %s and %s"
                              % (code, seen[code], r["tree_id"])))
            seen[code] = r["tree_id"]
    expected = {s: row["tree_id"] for row in trees for s in row["sites"]}
    if seen != expected:
        found.append(("FAIL", "the routing rules differ from TREES"))
    in_rows = {}
    for row in topo["coarse_organ_crosswalk"]:
        for code in row["codes"]:
            in_rows.setdefault(code, []).append(row["organ"])
    for code in lookup:
        rows = in_rows.get(code, [])
        if len(rows) != 1:
            found.append(("FAIL", "%s sits in %d crosswalk rows %s" % (code, len(rows), rows)))
        if lookup[code].get("coarse_organ") not in rows:
            found.append(("FAIL", "%s: coarse_organ %r is not its crosswalk row %s"
                          % (code, lookup[code].get("coarse_organ"), rows)))
    lists11 = sorted((k for k, v in lookup.items() if isinstance(v.get("candidate_groups"), list)
                      and GROUP in v["candidate_groups"]), key=n)
    unnamed = [k for k in lists11 if k not in seen]
    strings = sorted((k for k, v in lookup.items()
                      if v.get("candidate_groups") == "route_by_morphology"), key=n)
    found.append(("OK", "%d lookup codes list 11; %d are named by a Group 11 rule" %
                  (len(lists11), len(lists11) - len(unnamed))))
    if unnamed:
        found.append(("REPORT", "lists 11 and no rule names it, so it reaches the default "
                                "%s: %s" % (DEFAULT_TREE, ", ".join(unnamed))))
    found.append(("OK", "route_by_morphology codes (every group passes; %d named by a rule): %s"
                  % (sum(1 for k in strings if k in seen), ", ".join(strings))))
    referral_only = sorted((k for k, v in lookup.items() if k not in seen
                            and isinstance(v.get("candidate_groups"), list)
                            and GROUP not in v["candidate_groups"]), key=n)
    found.append(("REPORT", "%d lookup codes neither list 11 nor are routed; a Group 11 case "
                            "reaches one only by a referral hop, into the default %s: %s"
                  % (len(referral_only), DEFAULT_TREE, ", ".join(referral_only))))
    return found


# ------------------------------------------------------------------------------------------
def dump(doc: dict) -> str:
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def run(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="write nothing; exit 1 when either file on disk would change")
    args = ap.parse_args(argv)

    trees = c.trees_table()
    redcap = redcap_topography()
    topo_text = TOPO_PATH.read_text(encoding="utf-8")
    router_text = ROUTER_PATH.read_text(encoding="utf-8")
    topo_in, router_in = json.loads(topo_text), json.loads(router_text)
    if dump(topo_in) != topo_text or dump(router_in) != router_text:
        raise ApplyError("a shared file does not round-trip through json.dumps(indent=2, "
                         "ensure_ascii=False); refusing to rewrite its formatting")

    before = set(topo_in["topography_lookup"])
    topo = apply_topography(topo_in, trees, redcap)
    router, xb_added = apply_router(router_in, trees, topo["topography_lookup"])

    findings = verify(topo, router, trees)
    for level, msg in findings:
        print("%-6s %s" % (level, msg))
    new = sorted(set(topo["topography_lookup"]) - before, key=n)
    print("lookup codes added this run: %d%s" % (len(new), (" (" + ", ".join(
        topo["topography_lookup"][k]["redcap_code"] for k in new) + ")") if new else ""))
    print("Group X extragonadal rule codes added this run: %d" % len(xb_added))
    if any(level == "FAIL" for level, _ in findings):
        print("ERROR: the result fails its own checks; nothing written", file=sys.stderr)
        return 2

    changed = [(p, t) for p, t, old in ((TOPO_PATH, dump(topo), topo_text),
                                         (ROUTER_PATH, dump(router), router_text)) if t != old]
    if args.check:
        for p, _t in changed:
            print("%s would change" % p, file=sys.stderr)
        if not changed:
            print("both shared files are up to date")
        return 1 if changed else 0
    for p, t in changed:
        p.write_text(t, encoding="utf-8")
        print("wrote %s" % p)
    if not changed:
        print("both shared files are up to date")
    return 0


def main(argv=None) -> int:
    try:
        return run(argv)
    except (ApplyError, c.TreeError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
