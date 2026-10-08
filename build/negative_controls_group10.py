#!/usr/bin/env python3
"""Negative controls for the four Group 10 validation rules (build contract §5), and for the
brain marker cut-offs (check_brain_marker_cutoffs, registrar's ruling of 6 October 2026).

Each control mutates an in-memory copy of group_10_dt.json, of the router, or of the alias
list, writes the router, the topography lookup and the alias list to a throwaway repo,
runs ONE rule, and expects a FAIL whose message names the defect: a control counts as
caught only when a FAIL message carries every expected fragment, so a FAIL for another
reason is reported as WRONG REASON. The probes run each rule on the unmutated data first
and expect it to pass: a check is proved with correct data as well as broken data (Group 6
build contract §8.1). Nothing on disk is changed.

Rule 3 reads data/aliases/aliases_group_10.json. Until Task T5 writes that file, the
runner uses a small correct alias list held here; once the file exists, it uses the file.

    ICD_LAYER1=... ICDO_DB=... ICCC_DB=... python3 build/negative_controls_group10.py

Exit status 1 if any control is not caught for its reason or any probe fails.
"""
import copy, json, os, subprocess, sys, tempfile
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))
import build_database as bd
LAYER1 = Path(os.environ["ICD_LAYER1"])
DT_PATH = REPO / "data/database/group_10_dt.json"
base = json.loads(DT_PATH.read_text())
router = json.loads((REPO / "data/shared/presentation_router.json").read_text())
topography = json.loads((REPO / "data/shared/topography_codes.json").read_text())
ALIAS_PATH = REPO / "data/aliases/aliases_group_10.json"


def alias(text, *codes):
    return {"alias": text, "maps_to_morphology_codes": list(codes)}


if ALIAS_PATH.exists():
    aliases = json.loads(ALIAS_PATH.read_text())
    if isinstance(aliases, dict):
        aliases = aliases.get("aliases")
    ALIAS_SOURCE = "data/aliases/aliases_group_10.json"
else:
    # Each one is an ICD-O-3.2 term at a pair Group X emits at that behaviour only, except
    # "Teratoma", the D21 behaviour-neutral alias of 9080 and 9084.
    aliases = [alias("Germinoma", "9064"), alias("Dysgerminoma", "9060"),
               alias("Germ cell tumour, NOS", "9064"), alias("Yolk sac tumour", "9071"),
               alias("Embryonal carcinoma", "9070"), alias("Mixed germ cell tumour", "9085"),
               alias("Teratoma", "9080", "9084")]
    ALIAS_SOURCE = "an in-memory list of %d correct aliases (the file is absent)" % len(aliases)


def ctx_of(data):
    return bd.DTContext(DT_PATH, data, 10)


def node(d, nid):
    return next(n for t in d["decision_trees"] for n in t["nodes"] if n["node_id"] == nid)


def option(d, nid, starts):
    return next(o for o in node(d, nid)["options"] if o["label"].startswith(starts))


def run(check, data, alias_list=aliases, router_doc=router):
    if check in (bd.check_group10_no_pathology_codes, bd.check_brain_marker_cutoffs):
        return check(ctx_of(data))
    if check is bd.check_group10_every_gonadal_carcinoma_has_a_route:
        return check(ctx_of(data), LAYER1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        if check is bd.check_group10_picker_aliases_stay_unshared:
            # rule 8 reads every other group's alias file as well as Group 10's
            for other in (REPO / "data/aliases").glob("aliases_group_*.json"):
                if other.name != "aliases_group_10.json":
                    (tmp / "data/aliases").mkdir(parents=True, exist_ok=True)
                    (tmp / "data/aliases" / other.name).write_text(other.read_text())
        docs = [("data/shared/presentation_router.json", router_doc),
                ("data/shared/topography_codes.json", topography)]
        if alias_list is not None:
            docs.append(("data/aliases/aliases_group_10.json", alias_list))
        for rel, doc in docs:
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_text(json.dumps(doc))
        if check is bd.check_group10_picker_aliases_stay_unshared:
            return check(ctx_of(data), tmp)
        return check(ctx_of(data), LAYER1, tmp)


controls = []
RULES = (bd.check_group10_codes_fit_site, bd.check_group10_no_pathology_codes,
         bd.check_group10_alias_terms_match_icdo32, bd.check_group10_subgroups_and_routing,
         bd.check_group10_every_gonadal_carcinoma_has_a_route,
         bd.check_group10_picker_aliases_stay_unshared, bd.check_brain_marker_cutoffs)

# correct data first: every rule must pass
for chk in RULES:
    res = run(chk, copy.deepcopy(base))
    controls.append(("PROBE correct data: " + chk.__name__, None,
                     [m for l, m in res if l == bd.FAIL], res[0][1]))
res = run(bd.check_group10_alias_terms_match_icdo32, copy.deepcopy(base), alias_list=None)
controls.append(("PROBE no alias file: rule 3 returns a NOTE", None,
                 [m for l, m in res if l != bd.NOTE], res[0][1]))


def ctl(name, check, expect, mutate=None, alias_add=None, router_mutate=None, alias_swap=None):
    d = copy.deepcopy(base); a = copy.deepcopy(aliases); r = copy.deepcopy(router)
    if mutate: mutate(d)
    if alias_add: a = a + [alias_add]
    if alias_swap: a = alias_swap(a)
    if router_mutate: router_mutate(r)
    res = run(check, d, a, r)
    fails = [m for lvl, m in res if lvl == bd.FAIL]
    controls.append((name, expect, fails, res[0][1] if res else "(no finding)"))


def excl(code, beh, term):
    return {"icdo_code": code, "icdo_behaviour": beh, "icdo_term": term, "group_declares": "3",
            "reason": "Control.", "registrar_decision_required": False}


def code_branch(label, code, beh, basis=7):
    return {"label": label, "morphology_code": code, "behavior_code": beh,
            "basis_of_diagnosis": basis, "reason": "Control."}


def r1a(d):
    o = option(d, "cn_histology", "Mature teratoma")
    for k in ("morphology_code", "behavior_code", "basis_of_diagnosis"): o.pop(k)
    o["behaviour_exclusion"] = excl("9080", "0", "Teratoma, benign")
def r1b(d):
    o = option(d, "ov_teratoma", "Mature cystic teratoma")
    o.pop("behaviour_exclusion"); o.update(code_branch(o["label"], "9080", "0"))
def r1c(d): node(d, "ts_mixed")["options"].append(code_branch("Control 9086", "9086", "3"))
def r1d(d): node(d, "eg_mixed")["options"].append(code_branch("Control 9102", "9102", "3"))
def r1f(d): node(d, "ov_ihc")["nos_fallback"]["code"] = "9086"
ctl("R1-A cn_histology mature teratoma becomes excl 9080/0", bd.check_group10_codes_fit_site,
    ["excludes 9080/0", "range 95 (Xa2)", "hides a Group X code"], r1a)
ctl("R1-B ov_teratoma mature cystic teratoma emits 9080/0", bd.check_group10_codes_fit_site,
    ["g10_ovary ov_teratoma", "emits 9080/0", "no ICCC-2017 Group X range admits"], r1b)
ctl("R1-C ts_mixed gains 9086/3 (range 105, Xb6 only)", bd.check_group10_codes_fit_site,
    ["g10_testis ts_mixed", "emits 9086/3", "105 (Xb6"], r1c)
ctl("R1-D eg_mixed gains 9102/3", bd.check_group10_codes_fit_site,
    ["g10_extragonadal eg_mixed", "emits 9102/3", "110 (Xc5"], r1d)
ctl("R1-F ov_ihc nos_fallback becomes 9086/3", bd.check_group10_codes_fit_site,
    ["g10_ovary ov_ihc: nos_fallback emits 9086/3", "(C56.9)", "105 (Xb6"], r1f)


def r2a(d): option(d, "cn_markers", "Imaging shows a tumour and the report calls alpha")["morphology_code"] = "9071"
def r2b(d): option(d, "ov_document_inventory", "A histology report")["captures"]["evidence_tests"] = ["Imaging"]
def r2c(d): option(d, "eg_document_inventory", "An imaging report and")["captures"]["evidence_tests"] = ["Tumour markers"]
def r2e(d):
    node(d, "ov_markers")["options"].insert(0, code_branch(
        "Control: a placental tumour with human chorionic gonadotropin raised", "9100", "3", 4))
def r2d(d):
    o = option(d, "ts_imaging", "Imaging shows a malignant tumour")
    o["morphology_code"] = "9061"; o["behavior_code"] = "3"; o["basis_of_diagnosis"] = 2
ctl("R2-A cn_markers alpha-fetoprotein option emits 9071/3 at basis 4",
    bd.check_group10_no_pathology_codes, ["cn_markers", "emits 9071/3 at basis 4", "Table 4"], r2a)
ctl("R2-B ov_document_inventory histology captures Imaging (path, not flag)",
    bd.check_group10_no_pathology_codes, ["g10_ovary ov_histology", "evidence ['Imaging']",
                                          "at basis 7 with no histology or cytology"], r2b)
ctl("R2-C eg_document_inventory markers option captures Tumour markers only",
    bd.check_group10_no_pathology_codes, ["eg_markers", "evidence ['Tumour markers']",
                                          "without both Imaging and Tumour markers"], r2c)
ctl("R2-D ts_imaging emits 9061/3 at basis 2", bd.check_group10_no_pathology_codes,
    ["ts_imaging", "emits 9061/3 at basis 2", "rule 5"], r2d)
ctl("R2-E ov_markers gains a 9100/3 basis-4 branch (placental code outside g10_extragonadal)",
    bd.check_group10_no_pathology_codes,
    ["g10_ovary ov_markers", "emits 9100/3 at basis 4", "in g10_extragonadal only"], r2e)

ctl("R3-A alias Germinoma maps to 9060", bd.check_group10_alias_terms_match_icdo32,
    ["alias 'Germinoma' maps to 9060 Dysgerminoma"], alias_add=alias("Germinoma", "9060"))
ctl("R3-B alias Mature teratoma maps to 9080", bd.check_group10_alias_terms_match_icdo32,
    ["D21", "'Mature teratoma, NOS' at 9080/0", "emits 9080 at behaviour(s) 0, 1, 3"],
    alias_add=alias("Mature teratoma", "9080"))
ctl("R3-C alias Germ cell neoplasia in situ maps to 9064",
    bd.check_group10_alias_terms_match_icdo32,
    ["D21", "'Germ cell neoplasia in situ' at 9064/2", "emits 9064 at behaviour(s) 3"],
    alias_add=alias("Germ cell neoplasia in situ", "9064"))
# The D21 exemption covers "Teratoma" mapped to exactly 9080 and 9084; any other map is
# checked as usual.
ctl("R3-D alias Teratoma maps to 9080 alone (exemption is exact)",
    bd.check_group10_alias_terms_match_icdo32,
    ["D21", "'Teratoma, NOS' at 9080/1", "emits 9080 at behaviour(s) 0, 1, 3"],
    alias_add=alias("Teratoma", "9080"))
ctl("R3-E alias Teratoma, NOS maps to 9080 and 9084 (exemption is exact text)",
    bd.check_group10_alias_terms_match_icdo32,
    ["alias 'Teratoma, NOS'", "'Teratoma, NOS' at 9080/1", "maps to 9084"],
    alias_add=alias("Teratoma, NOS", "9080", "9084"))
# An [obs] term still names its code: Granulosa cell carcinoma is 8620/3 [obs].
ctl("R3-F alias Granulosa cell carcinoma ([obs] 8620/3) maps to 9064",
    bd.check_group10_alias_terms_match_icdo32,
    ["alias 'Granulosa cell carcinoma'", "[obs]' at 8620/3", "maps to 9064"],
    alias_add=alias("Granulosa cell carcinoma", "9064"))
# The alias text under the wrong key: every entry reads as no ICD-O-3.2 term at all.
def r3g(a):
    return [{("term" if k == "alias" else k): v for k, v in x.items()} for x in a]
ctl("R3-G every alias carries its text under the wrong key",
    bd.check_group10_alias_terms_match_icdo32,
    ["none of the", "equals an ICD-O-3.2 term, so the rule checked nothing"],
    alias_swap=r3g)


def r4a(d):
    e = next(e for e in d["morphology_entries"]
             if e["morphology_code"] == "9071" and e["behavior_code"] == "3")
    e["iccc3_subgroup_by_topography"] = [x for x in e["iccc3_subgroup_by_topography"]
                                         if x["iccc3_subgroup_id"] != "Xa4"]
def rules_of(r): return r["groups"]["10"]["tree_routing"]["rules"]
def rule_for(r, tree): return next(x for x in rules_of(r) if x["tree_id"] == tree)
def r4b(r):
    rule_for(r, "g10_testis")["topography_in"].remove("C62.0")
    rule_for(r, "g10_ovary")["topography_in"].append("C62.0")
def r4c(r): rule_for(r, "g10_extragonadal")["topography_in"].remove("C76.3")
def r4d(r):
    r["groups"]["10"]["tree_routing"]["default"].update(
        tree_id="g10_cns", entry_node="cn_document_inventory")
def r4e(r):
    for x in rules_of(r):
        if "C38.1" in x["topography_in"]:
            x["topography_in"].remove("C38.1")
# C11.0 lists groups 4, 9 and 11 and not 10, so neither the destination check (the default
# also lands in g10_extragonadal) nor the naming clause for enterable codes sees it go.
def r4f(r): rule_for(r, "g10_extragonadal")["topography_in"].remove("C11.0")
def r4g(r): rule_for(r, "g10_extragonadal")["topography_in"].append("C77.9")
ctl("R4-A 9071/3 loses its Xa rule", bd.check_group10_subgroups_and_routing,
    ["9071/3 shows subgroup 'Xc4' at C70.0", "places it in Xa4"], r4a)
ctl("R4-B C62.0 moves to the ovary routing rule", bd.check_group10_subgroups_and_routing,
    ["sends C62.0 to 'g10_ovary'", "goes to 'g10_testis'"], router_mutate=r4b)
ctl("R4-C C76.3 dropped from the extragonadal routing rule",
    bd.check_group10_subgroups_and_routing,
    ["C76.3 can enter Group X", "no groups[\"10\"].tree_routing rule names it",
     "reaches the default"], router_mutate=r4c)
ctl("R4-D the tree_routing default becomes g10_cns",
    bd.check_group10_subgroups_and_routing,
    ["tree_routing.default is 'g10_cns'", "goes to g10_extragonadal"], router_mutate=r4d)
ctl("R4-E C38.1, which lists Group 10, removed from every routing rule",
    bd.check_group10_subgroups_and_routing,
    ["C38.1 can enter Group X", "[2, 4, 10, 11]", "reaches the default"], router_mutate=r4e)
ctl("R4-F C11.0, which does not list Group 10, dropped from the Xb rule",
    bd.check_group10_subgroups_and_routing,
    ["the g10_extragonadal rule omits 1 lookup code(s) ICCC-2017 places in Xb: C11.0"],
    router_mutate=r4f)
ctl("R4-G C77.9, outside every germ cell site range, added to the Xb rule",
    bd.check_group10_subgroups_and_routing,
    ["the g10_extragonadal rule names 1 code(s) ICCC-2017 does not place in Xb: C77.9"],
    router_mutate=r4g)


# Brain marker gates (registrar's ruling, 6 October 2026). One control per gate: its cut-off
# moved (to 250 for the six marker gates; to 12 months for the age gate, the "1 year" a
# reader of Lahdenne's 17 ng/mL might pick), then the boundary convention flipped, a missing
# value read as normal, and the brain tree as it stood before the gates, pinned to commit
# PRE_GATES and never to HEAD (CLAUDE.md rule 13).
PRE_GATES = "689d610"
BRAIN = bd.check_brain_marker_cutoffs


def recut(nid, old, new):
    def mutate(d):
        for b in node(d, nid)["bands"]:
            if b["range"] in (">" + old, "<=" + old, "<" + old, ">=" + old):
                b["range"] = b["range"].replace(old, new)
    return mutate


def flip_convention(d):
    for b in node(d, "cn_afp_serum")["bands"]:
        b["range"] = {">25": ">=25", "<=25": "<25"}.get(b["range"], b["range"])


def not_documented_to_report(d):
    for b in node(d, "cn_hcg_csf")["bands"]:
        if b["range"] == "not_documented":
            b["next_node"] = "cn_markers_cutoff"


def other_unit_is_normal(d):
    for b in node(d, "cn_hcg_csf")["bands"]:
        if b["range"] == "other_unit":
            b["next_node"] = "cn_imaging_markers"


def afp_csf_not_documented_to_report(d):
    for b in node(d, "cn_afp_csf")["bands"]:
        if b["range"] == "not_documented":
            b["next_node"] = "cn_markers_cutoff"


def no_other_unit_band(d):
    n = node(d, "cn_afp_serum")
    n["bands"] = [b for b in n["bands"] if b["range"] != "other_unit"]


def at_pre_gates(d):
    old = json.loads(subprocess.run(
        ["git", "show", PRE_GATES + ":data/database/group_10_dt.json"], cwd=REPO,
        capture_output=True, text=True, check=True).stdout)
    d.clear(); d.update(old)


AFP_RAISED = "the ruling gives alpha-fetoprotein raised"
HCG_RAISED = "the ruling gives beta human chorionic gonadotropin raised"
REPORT = "the ruling gives the report question"
ctl("R5-A cn_marker_age boundary 24 -> 12 months", BRAIN,
    ["patient_age_months 23", REPORT], recut("cn_marker_age", "24", "12"))
ctl("R5-B cn_afp_serum cut-off 25 -> 250 ng/mL", BRAIN,
    ["afp_serum_ng_ml 25.01", AFP_RAISED], recut("cn_afp_serum", "25", "250"))
ctl("R5-C cn_afp_csf cut-off 25 -> 250 ng/mL", BRAIN,
    ["afp_csf_ng_ml 25.01", AFP_RAISED], recut("cn_afp_csf", "25", "250"))
ctl("R5-E cn_hcg_serum cut-off 50 -> 250 IU/L", BRAIN,
    ["hcg_serum_iu_l 50.01", HCG_RAISED], recut("cn_hcg_serum", "50", "250"))
ctl("R5-F cn_hcg_csf cut-off 50 -> 250 IU/L", BRAIN,
    ["hcg_serum_iu_l 50, hcg_csf_iu_l 50.01", "reaches cn_imaging_markers", HCG_RAISED],
    recut("cn_hcg_csf", "50", "250"))
ctl("R5-G cn_hcg_serum cut-off 50 -> 250 IU/L", BRAIN,
    ["hcg_serum_iu_l 50.01", "reaches cn_imaging_markers", HCG_RAISED],
    recut("cn_hcg_serum", "50", "250"))
ctl("R5-H cn_afp_serum reads 'at or above' 25", BRAIN,
    ["afp_serum_ng_ml 25,", "reaches cn_afp_raised", "the ruling gives"],
    flip_convention)
ctl("R5-I cn_hcg_csf sends 'not documented' to the report question (the rule before 7 October 2026)", BRAIN,
    ["hcg_csf_iu_l not entered", "reaches cn_markers_cutoff", "the ruling gives neither"], not_documented_to_report)
ctl("R5-K cn_hcg_csf reads 'in another unit or only described' as not raised", BRAIN,
    ["hcg_csf_iu_l in another unit or only described", "reaches cn_imaging_markers", REPORT],
    other_unit_is_normal)
ctl("R5-L cn_afp_csf sends 'not documented' to the report question", BRAIN,
    ["afp_csf_ng_ml not entered", "reaches cn_markers_cutoff", "the ruling gives"],
    afp_csf_not_documented_to_report)
ctl("R5-M cn_afp_serum has no 'in another unit' band", BRAIN,
    ["cn_afp_serum has no `other_unit` band"], no_other_unit_band)
# ---- rule 7 (the gonadal carcinoma picker) and rule 8 (its aliases) -----------------------
R7 = bd.check_group10_every_gonadal_carcinoma_has_a_route
R8 = bd.check_group10_picker_aliases_stay_unshared
ADENOSQ = option(base, "ov_carcinoma_other", "Adenosquamous carcinoma")["morphology_code"]


def r7_drop_option(d):
    n = node(d, "ov_carcinoma_other")
    n["options"] = [o for o in n["options"] if o["label"] != "Adenosquamous carcinoma"]


def r7_obsolete_option(d):
    """An option that records 8130/3, whose Preferred term ICD-O-3.2 marks [obs] (design D11)."""
    node(d, "ov_carcinoma_other")["options"].append(
        {"label": "Papillary urothelial carcinoma", "morphology_code": "8130", "behavior_code": "3",
         "basis_of_diagnosis": 7, "reason": "Control."})


def r7_invented_search_term(d):
    for o in node(d, "ov_carcinoma_other")["options"]:
        if o.get("search_terms"):
            o["search_terms"] = o["search_terms"] + ["Invented name for a tumour"]
            return


ctl("R7-A ov_carcinoma_other loses the option for %s/3" % ADENOSQ, R7,
    ["GROUP 10 RULE 7", "g10_ovary offers no option that records", ADENOSQ], r7_drop_option)
ctl("R7-B ov_carcinoma_other offers 8130/3, an [obs] Preferred term", R7,
    ["GROUP 10 RULE 7", "marked [obs]", "8130/3"], r7_obsolete_option)
ctl("R7-C an option's search term is no ICD-O-3.2 term of its code", R7,
    ["GROUP 10 RULE 7", "Invented name for a tumour", "not a live ICD-O-3.2 Synonym or Related term"],
    r7_invented_search_term)
ctl("R8-A a Group 10 alias on a picker-only code is also a Group VI alias", R8,
    ["GROUP 10 RULE 8", "Medullary carcinoma, NOS", "Group 6"],
    alias_add={"alias": "Medullary carcinoma, NOS", "maps_to_morphology_codes": ["8510"]})
ctl("R8-B a Group 10 alias on a picker-only code is also a Group III alias", R8,
    ["GROUP 10 RULE 8", "ACTH-producing tumor", "Group 3"],
    alias_add={"alias": "ACTH-producing tumor", "maps_to_morphology_codes": ["8158"]})
ctl("R5-J the brain tree at %s, before the gates" % PRE_GATES, BRAIN,
    ["patient_age_months 24", "reaches cn_markers", "the ruling gives neither"], at_pre_gates)

print("Rule 3 alias list: %s" % ALIAS_SOURCE)
wrong = caught = probes = 0
for name, expect, fails, first in controls:
    if expect is None:
        ok = not fails
        probes += ok
        verdict = "PASSES" if ok else "*** WRONG ***"
        msg = first if ok else fails[0]
    else:
        hit = next((m for m in fails if all(x in m for x in expect)), None)
        ok = hit is not None
        caught += ok
        verdict = "CAUGHT" if ok else ("*** WRONG REASON ***" if fails else "*** MISSED ***")
        msg = hit or (fails[0] if fails else first)
    wrong += not ok
    print("%-72s %s | %s" % (name, verdict, msg[:200]))
n_ctl = sum(1 for c in controls if c[1] is not None)
print("\n%d of %d controls caught for the expected reason; %d of %d probes pass"
      % (caught, n_ctl, probes, len(controls) - n_ctl))
sys.exit(1 if wrong else 0)
