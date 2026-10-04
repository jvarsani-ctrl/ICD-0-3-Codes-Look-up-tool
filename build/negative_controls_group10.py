#!/usr/bin/env python3
"""Negative controls for the four Group 10 validation rules (build contract §5).

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
import copy, json, os, sys, tempfile
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
    if check is bd.check_group10_no_pathology_codes:
        return check(ctx_of(data))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        docs = [("data/shared/presentation_router.json", router_doc),
                ("data/shared/topography_codes.json", topography)]
        if alias_list is not None:
            docs.append(("data/aliases/aliases_group_10.json", alias_list))
        for rel, doc in docs:
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            (tmp / rel).write_text(json.dumps(doc))
        return check(ctx_of(data), LAYER1, tmp)


controls = []
RULES = (bd.check_group10_codes_fit_site, bd.check_group10_no_pathology_codes,
         bd.check_group10_alias_terms_match_icdo32, bd.check_group10_subgroups_and_routing)

# correct data first: every rule must pass
for chk in RULES:
    res = run(chk, copy.deepcopy(base))
    controls.append(("PROBE correct data: " + chk.__name__, None,
                     [m for l, m in res if l == bd.FAIL], res[0][1]))
res = run(bd.check_group10_alias_terms_match_icdo32, copy.deepcopy(base), alias_list=None)
controls.append(("PROBE no alias file: rule 3 returns a NOTE", None,
                 [m for l, m in res if l != bd.NOTE], res[0][1]))


def ctl(name, check, expect, mutate=None, alias_add=None, router_mutate=None):
    d = copy.deepcopy(base); a = copy.deepcopy(aliases); r = copy.deepcopy(router)
    if mutate: mutate(d)
    if alias_add: a = a + [alias_add]
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
def r1e(d): node(d, "su_site_histology")["options"].append(code_branch("Control", "9064", "3"))
ctl("R1-A cn_histology mature teratoma becomes excl 9080/0", bd.check_group10_codes_fit_site,
    ["excludes 9080/0", "range 95 (Xa2)", "hides a Group X code"], r1a)
ctl("R1-B ov_teratoma mature cystic teratoma emits 9080/0", bd.check_group10_codes_fit_site,
    ["g10_ovary ov_teratoma", "emits 9080/0", "no ICCC-2017 Group X range admits"], r1b)
ctl("R1-C ts_mixed gains 9086/3 (range 105, Xb6 only)", bd.check_group10_codes_fit_site,
    ["g10_testis ts_mixed", "emits 9086/3", "105 (Xb6"], r1c)
ctl("R1-D eg_mixed gains 9102/3", bd.check_group10_codes_fit_site,
    ["g10_extragonadal eg_mixed", "emits 9102/3", "110 (Xc5"], r1d)
ctl("R1-E su_site_histology gains a code branch", bd.check_group10_codes_fit_site,
    ["g10_site_unstated su_site_histology", "emits nothing"], r1e)


def r2a(d): option(d, "cn_markers", "Imaging shows a tumour and the report calls alpha")["morphology_code"] = "9071"
def r2b(d): option(d, "ov_document_inventory", "A histology report")["captures"]["evidence_tests"] = ["Imaging"]
def r2c(d): option(d, "eg_document_inventory", "An imaging report and")["captures"]["evidence_tests"] = ["Tumour markers"]
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
ctl("R4-A 9071/3 loses its Xa rule", bd.check_group10_subgroups_and_routing,
    ["9071/3 shows subgroup 'Xc4' at C70.0", "places it in Xa4"], r4a)
ctl("R4-B C62.0 moves to the ovary routing rule", bd.check_group10_subgroups_and_routing,
    ["sends C62.0 to 'g10_ovary'", "goes to 'g10_testis'"], router_mutate=r4b)
ctl("R4-C C76.3 dropped from the extragonadal routing rule",
    bd.check_group10_subgroups_and_routing,
    ["sends C76.3 to 'g10_site_unstated'", "an Xb topography", "goes to 'g10_extragonadal'"],
    router_mutate=r4c)

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
