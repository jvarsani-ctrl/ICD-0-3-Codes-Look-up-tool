#!/usr/bin/env python3
"""Negative controls for the four Group 11 validation rules (build contract §5, rules 1, 2, 3 and
5), and for the registration changes that Group 11 needed in build_database.py: the
recapture_site self-referral, the two-digit ICCC subgroup parser, the ICD-O-3.2 round trip and the
behaviour declaration.

Each control mutates an in-memory copy of group_11_dt.json or of the router, writes the router and
the topography lookup to a throwaway repo, runs ONE rule, and expects a FAIL whose message names
the defect: a control counts as caught only when a FAIL message carries every expected fragment, so
a FAIL for another reason is reported as WRONG REASON. The probes run each rule on the unmutated
data first and expect it to pass: a check is proved with correct data as well as broken data
(Group 6 build contract §8.1). Nothing on disk is changed, and nothing is pinned to a commit.

    ICD_LAYER1=... ICDO_DB=... ICCC_DB=... python3 build/negative_controls_group11.py

Exit status 1 if any control is not caught for its reason or any probe fails.
"""
import copy, json, os, re, sys, tempfile
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))
import build_database as bd
LAYER1 = Path(os.environ["ICD_LAYER1"])
DT_PATH = REPO / "data/database/group_11_dt.json"
base = json.loads(DT_PATH.read_text())
router = json.loads((REPO / "data/shared/presentation_router.json").read_text())
topography = json.loads((REPO / "data/shared/topography_codes.json").read_text())


def bd_term(code, beh):
    """The ICD-O-3.2 Preferred term of (code, behaviour), so a control's exclusion block is
    well formed in every respect but the one it breaks."""
    index, _err = bd.load_icdo32(LAYER1)
    return next(t for t, (level, _obs) in index[(code, beh)].items() if level == "Preferred")


def ctx_of(data):
    return bd.DTContext(DT_PATH, data, 11)


def node(d, nid):
    return next(n for t in d["decision_trees"] for n in t["nodes"] if n["node_id"] == nid)


def option(d, nid, starts):
    return next(o for o in node(d, nid)["options"] if o["label"].startswith(starts))


def run(check, data, router_doc=router):
    if check in (bd.check_group11_no_pathology_codes, bd.check_refer_terminals):
        return check(ctx_of(data))
    if check in (bd.check_group11_codes_fit_site, bd.check_group11_obs_never_emitted,
                 bd.check_icdo32_round_trip, bd.check_behaviour_exclusion):
        return check(ctx_of(data), LAYER1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for rel, doc in (("data/shared/presentation_router.json", router_doc),
                         ("data/shared/topography_codes.json", topography)):
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_text(json.dumps(doc))
        return check(ctx_of(data), LAYER1, tmp)


R1, R2 = bd.check_group11_codes_fit_site, bd.check_group11_no_pathology_codes
R3, R5 = bd.check_group11_obs_never_emitted, bd.check_group11_subgroups_and_routing
REFER, ROUND, BEHAV = bd.check_refer_terminals, bd.check_icdo32_round_trip, bd.check_behaviour_exclusion

controls = []

# correct data first: every rule must pass
for chk in (R1, R2, R3, R5, REFER, ROUND, BEHAV):
    res = run(chk, copy.deepcopy(base))
    controls.append(("PROBE correct data: " + chk.__name__, None,
                     [m for l, m in res if l == bd.FAIL], res[0][1]))
res = run(R5, copy.deepcopy(base))
controls.append(("PROBE rule 5 reports C75.1 as a NOTE and not a FAIL", None,
                 [m for l, m in res if l == bd.FAIL or (l == bd.NOTE and "C75.1" not in m)]
                 + ([] if any(l == bd.NOTE and "C75.1" in m for l, m in res)
                    else ["no NOTE names C75.1"]), res[-1][1]))
res = run(ROUND, copy.deepcopy(base))
warns = [m for l, m in res if l == bd.WARN and "[obs]" in m]
controls.append(("PROBE round trip: the 13 [obs] Preferred terms are WARN, no NOTE says the "
                 "names are REDCap wordings", None,
                 ([] if len(warns) == 13 else ["%d [obs] WARNs, not 13" % len(warns)])
                 + [m for l, m in res if "REDCap wordings" in m], "13 WARNs, no FAIL"))
subgroups = bd.parse_classification_subgroups(LAYER1)
g11 = subgroups.get(11, {})
controls.append(("PROBE parse_classification_subgroups files XIf10 and XIf11 apart, and Group XII "
                 "rows under group 12", None,
                 [] if ({"XIf9", "XIf10", "XIf11"} <= set(g11) and "XIIa1" not in g11
                        and "XIIa1" in subgroups.get(12, {})) else ["subgroup table: %s" % sorted(g11)],
                 "XIf10, XIf11 present; XIIa1 in group 12"))


def ctl(name, check, expect, mutate=None, router_mutate=None):
    d = copy.deepcopy(base); r = copy.deepcopy(router)
    if mutate: mutate(d)
    if router_mutate: router_mutate(r)
    res = run(check, d, r)
    fails = [m for lvl, m in res if lvl == bd.FAIL]
    controls.append((name, expect, fails, res[0][1] if res else "(no finding)"))


def code_branch(label, code, beh="3", basis=7):
    return {"label": label, "morphology_code": code, "behavior_code": beh,
            "basis_of_diagnosis": basis, "reason": "Control."}


# ---- rule 1: codes fit the site ----------------------------------------------------------
def r1a(d): node(d, "lu_picker")["options"].append(code_branch("Control 8170 in the lung", "8170"))
def r1b(d): node(d, "me_picker")["options"].append(code_branch("Control 8070 in melanoma", "8070"))
def r1c(d):
    for o in node(d, "th_not_malignant")["options"]:
        if isinstance(o.get("behaviour_exclusion"), dict):
            o["behaviour_exclusion"].update(icdo_code="8260", icdo_behaviour="3")
            return
def r1d(d): node(d, "th_ihc")["nos_fallback"]["code"] = "8170"
ctl("R1-A lu_picker gains 8170/3 (Group VII range 57 at every site)", R1,
    ["g11_lung lu_picker", "emits 8170/3", "57 (VIIb"], r1a)
ctl("R1-B me_picker gains 8070/3 (the melanoma tree takes XId only)", R1,
    ["g11_melanoma me_picker", "emits 8070/3", "no ICCC-2017 XId"], r1b)
ctl("R1-C th_not_malignant excludes 8260/3, a Group XI code at the thyroid", R1,
    ["g11_thyroid th_not_malignant", "excludes 8260/3", "hides a Group XI code"], r1c)
ctl("R1-D th_ihc nos_fallback becomes 8170/3", R1,
    ["g11_thyroid th_ihc", "nos_fallback emits 8170/3", "57 (VIIb"], r1d)


# ---- rule 2: no pathology, no specific code ----------------------------------------------
def inventory_tier(d, nid, tier, tests):
    n = 0
    for o in node(d, nid)["options"]:
        if (o.get("captures") or {}).get("basis_evidence_tier") == tier:
            o["captures"]["evidence_tests"] = tests
            n += 1
    assert n, (nid, tier)
def r2a(d): option(d, "th_imaging_markers", "Imaging shows a tumour of the thyroid")["morphology_code"] = "8260"
def r2b(d): inventory_tier(d, "th_document_inventory", "histology", ["Imaging"])
def r2c(d):
    # Registrar, 8 October 2026 (review A8): no basis-1 melanoma on the skin tree either.
    node(d, "sk_clinical")["options"].insert(0, code_branch("Control 8720 at basis 1", "8720",
                                                            basis=1))
def r2d(d): inventory_tier(d, "th_document_inventory", "markers", ["Imaging"])
ctl("R2-A th_imaging_markers medullary option emits 8260/3 at basis 4", R2,
    ["g11_thyroid th_imaging_markers", "emits 8260/3 at basis 4", "Table 4"], r2a)
ctl("R2-B th_document_inventory histology tier captures Imaging (the path, not the flag)", R2,
    ["g11_thyroid th_histology", "evidence ['Imaging']", "at basis 7 with no histology or cytology"], r2b)
ctl("R2-C an 8720/3 basis-1 branch is put back on sk_clinical", R2,
    ["g11_skin sk_clinical", "emits 8720/3 at basis 1", "child's melanoma needs tissue"], r2c)
ctl("R2-D th_document_inventory markers tier captures Imaging only", R2,
    ["g11_thyroid th_imaging_markers", "evidence ['Imaging']",
     "without both Imaging and Tumour markers"], r2d)


# ---- rule 3: no [obs] pair is emitted ------------------------------------------------------
def r3a(d): node(d, "th_picker")["options"].append(code_branch("Control 8130", "8130"))
def r3b(d): node(d, "me_picker")["options"].append(code_branch("Control 8780", "8780"))
ctl("R3-A th_picker gains 8130/3 (one of the eleven all-[obs] numbers)", R3,
    ["g11_thyroid th_picker", "emits 8130/3", "Preferred term is [obs]"], r3a)
ctl("R3-B me_picker gains 8780/3 (an [obs] Preferred term computed from icdo32.sqlite)", R3,
    ["g11_melanoma me_picker", "emits 8780/3", "Preferred term is [obs]"], r3b)


# ---- rule 5: subgroups and routing -------------------------------------------------------
def rules_of(r): return r["groups"]["11"]["tree_routing"]["rules"]
def rule_for(r, tree): return next(x for x in rules_of(r) if x["tree_id"] == tree)
def r5a(d):
    e = next(e for e in d["morphology_entries"]
             if e["morphology_code"] == "8070" and e["behavior_code"] == "3")
    e["iccc3_subgroup_by_topography"] = [x for x in e["iccc3_subgroup_by_topography"]
                                         if x["iccc3_subgroup_id"] != "XIf4"]
def r5b(r): rule_for(r, "g11_lung")["topography_in"].remove("C34.0")
def r5c(r):
    rule_for(r, "g11_lung")["topography_in"].remove("C34.0")
    rule_for(r, "g11_thyroid")["topography_in"].append("C34.0")
def r5d(r): r["groups"]["11"]["tree_routing"]["default"].update(
    tree_id="g11_lung", entry_node="lu_document_inventory")
def r5e(r): rules_of(r).append({"topography_in": ["C77.9"], "tree_id": "g11_melanoma",
                                "entry_node": "me_document_inventory", "label": "Control"})
def r5f(r): rule_for(r, "g11_adrenal")["topography_in"].append("C34.0")
ctl("R5-A 8070/3 loses its XIf4 rule", R5,
    ["8070/3 shows subgroup 'XIf10' at C34.0", "places it in XIf4"], r5a)
ctl("R5-B C34.0 dropped from the lung rule", R5,
    ["the g11_lung rule omits 1 routed site(s) TREES gives it: C34.0"], router_mutate=r5b)
ctl("R5-C C34.0 moved from the lung rule to the thyroid rule", R5,
    ["the g11_thyroid rule names 1 code(s) TREES does not route to it: C34.0"],
    router_mutate=r5c)
ctl("R5-D the tree_routing default becomes g11_lung", R5,
    ["tree_routing.default is 'g11_lung'", "g11_unspecified"], router_mutate=r5d)
ctl("R5-E a rule routes C77.9 to the melanoma tree", R5,
    ["routes to 'g11_melanoma'", "named by no rule"], router_mutate=r5e)
ctl("R5-F C34.0 also named by the first (adrenal) rule: the router sends it there", R5,
    ["the router sends C34.0 to 'g11_adrenal'", "TREES routes it to g11_lung"],
    router_mutate=r5f)


# ---- registration: the self-referral, the round trip and the behaviour declaration ---------
def reg_a(d):
    o = option(d, "th_deposit", "A carcinoma or melanoma of another organ")
    o.pop("recapture_site")
def reg_b(d): next(e for e in d["morphology_entries"]
                   if e["morphology_code"] == "8010")["morphology_name"] = "Control name"
def reg_c(d):
    for o in node(d, "th_not_malignant")["options"]:
        if isinstance(o.get("behaviour_exclusion"), dict):
            o["behaviour_exclusion"].update(icdo_code="8260", icdo_behaviour="3",
                                            icdo_term=bd_term("8260", "3"))
            return
ctl("REG-A th_deposit self-referral to Group 11 without recapture_site", REFER,
    ["th_deposit", "refer_group 11 is this group", "recapture_site referral"], reg_a)
ctl("REG-B the 8010/3 entry carries a name ICD-O-3.2 does not print", ROUND,
    ["8010/3", "Control name"], reg_b)
ctl("REG-C a behaviour_exclusion names behaviour 3, which Group XI declares", BEHAV,
    ["th_not_malignant", "icdo_behaviour '3' IS in Group XI's own declaration"], reg_c)

# The parser patterns, as written in parse_classification_subgroups: the two the build used
# before this change do not read the Group XI table, and the two it uses now do.
OLD_SUB, NEW_SUB = r"^([IVX]+[a-z]\d?)\b", r"^([IVX]+[a-z]\d{0,2})\b"
OLD_HEAD, NEW_HEAD = r"^##\s+([IVX]+)\s*:", r"^##\s+([IVX]+)(?:\s*:|\s)"
row, heading = "XIf10 Carcinomas of other specified sites", "## XII Other And Unspecified Malignant Neoplasms"
controls.append(("REG-D the old subgroup pattern misses XIf10 and the old heading pattern misses "
                 "Group XII; the new patterns read both", "pattern",
                 [] if (re.match(OLD_SUB, row) is None and re.match(OLD_HEAD, heading) is None
                        and re.match(NEW_SUB, row) and re.match(NEW_HEAD, heading)) else ["no"],
                 "old patterns fail, new patterns match"))

wrong = caught = probes = 0
for name, expect, fails, first in controls:
    if expect is None:
        ok = not fails
        probes += ok
        verdict = "PASSES" if ok else "*** WRONG ***"
        msg = first if ok else fails[0]
    elif expect == "pattern":
        ok = not fails
        caught += ok
        verdict = "CAUGHT" if ok else "*** MISSED ***"
        msg = first
    else:
        hit = next((m for m in fails if all(x in m for x in expect)), None)
        ok = hit is not None
        caught += ok
        verdict = "CAUGHT" if ok else ("*** WRONG REASON ***" if fails else "*** MISSED ***")
        msg = hit or (fails[0] if fails else first)
    wrong += not ok
    print("%-72s %s | %s" % (name, verdict, msg[:int(os.environ.get("NC_WIDTH", "200"))]))
n_ctl = sum(1 for c in controls if c[1] is not None)
print("\n%d of %d controls caught for the expected reason; %d of %d probes pass"
      % (caught, n_ctl, probes, len(controls) - n_ctl))
sys.exit(1 if wrong else 0)
