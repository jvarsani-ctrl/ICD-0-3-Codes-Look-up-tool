#!/usr/bin/env python3
"""Negative controls for the three Group 8 validation rules (build contract §8).

Each control mutates an in-memory copy of group_08_dt.json (or of the alias file, in a temp
directory), runs ONE rule, and expects FAIL. The three probes run each rule on the
unmutated data first and expect it to pass: a check is proved with correct data as well as
broken data (Group 6 build contract §8.1). Nothing on disk is changed.

    ICD_LAYER1=... ICDO_DB=... ICCC_DB=... python3 build/negative_controls_group08.py

Exit status 1 if any control is not caught or any probe fails.
"""
import copy, json, os, shutil, sys, tempfile
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))
import build_database as bd
LAYER1 = Path(os.environ["ICD_LAYER1"])
base = json.loads((REPO / "data/database/group_08_dt.json").read_text())
aliases = json.loads((REPO / "data/aliases/aliases_group_08.json").read_text())

def ctx_of(data):
    return bd.DTContext(REPO / "data/database/group_08_dt.json", data, 8)

def node(d, nid):
    return next(n for t in d["decision_trees"] for n in t["nodes"] if n["node_id"] == nid)

def run(check, data, alias_list=None):
    tmp = Path(tempfile.mkdtemp())
    (tmp / "data/aliases").mkdir(parents=True)
    (tmp / "data/aliases/aliases_group_08.json").write_text(json.dumps(alias_list if alias_list is not None else aliases))
    if check is bd.check_group8_no_retired_ewing_code:
        res = check(ctx_of(data), LAYER1, tmp)
    else:
        res = check(ctx_of(data))
    shutil.rmtree(tmp)
    return res

controls = []
def ctl(name, check, mutate, alias_mutate=None):
    d = copy.deepcopy(base); a = copy.deepcopy(aliases)
    mutate(d)
    if alias_mutate: alias_mutate(a)
    res = run(check, d, a)
    fails = [m for lvl, m in res if lvl == bd.FAIL]
    controls.append((name, bool(fails), fails[0][:170] if fails else res[0][1][:170]))

def m(f): return f
# correct data first: every rule must pass
for chk in (bd.check_group8_no_retired_ewing_code, bd.check_group8_no_pathology_codes, bd.check_group8_ewing_requires_partner):
    res = run(chk, copy.deepcopy(base))
    controls.append(("PROBE correct data: " + chk.__name__, any(l == bd.FAIL for l, _ in res), res[0][1][:170]))

def r1a(d): node(d, "bn_round_cell")["options"][0]["morphology_code"] = "9260"
def r1b(d): pass
def r1b_a(a): next(x for x in a if x["alias"] == "Ewing sarcoma")["maps_to_morphology_codes"] = ["9260"]
def r1c(d): next(o for o in node(d, "bn_giant_cell")["options"] if "behaviour_exclusion" in o and o["behaviour_exclusion"]["icdo_code"] == "9260")["behaviour_exclusion"]["icdo_behaviour"] = "3"
def r1d(d): node(d, "bn_round_cell_ihc")["nos_fallback"]["code"] = "9260"
ctl("R1-A a round cell option emits 9260", bd.check_group8_no_retired_ewing_code, r1a)
ctl("R1-B the 'Ewing sarcoma' alias maps to 9260", bd.check_group8_no_retired_ewing_code, r1b, r1b_a)
ctl("R1-C the aneurysmal bone cyst exclusion claims 9260/3", bd.check_group8_no_retired_ewing_code, r1c)
ctl("R1-D the round cell fallback names 9260", bd.check_group8_no_retired_ewing_code, r1d)

def r2a(d): node(d, "bn_imaging_os")["morphology_code"] = "9364"
def r2b(d): node(d, "bn_imaging_line")["options"][1]["basis_of_diagnosis"] = 7
def r2c(d): o = node(d, "bn_clinical_alias")["options"][0]; o["morphology_code"] = "9180"
def r2d(d): node(d, "bn_document_inventory")["options"][2]["captures"]["evidence_tests"] = ["Imaging"]
def r2e(d): node(d, "bn_imaging_line")["options"][1]["morphology_code"] = "9220"
ctl("R2-A the imaging node emits Ewing sarcoma 9364", bd.check_group8_no_pathology_codes, r2a)
ctl("R2-B the imaging 8000 option claims basis 7", bd.check_group8_no_pathology_codes, r2b)
ctl("R2-C the referral option emits 9180 at basis 1", bd.check_group8_no_pathology_codes, r2c)
ctl("R2-D the histology route captures Imaging only (path, not flag)", bd.check_group8_no_pathology_codes, r2d)
ctl("R2-E the imaging 8000 option emits chondrosarcoma 9220 (design D10)", bd.check_group8_no_pathology_codes, r2e)

def rule(d, code, pos_has):
    return next(r for r in node(d, "bn_round_cell_ihc")["resolution_logic"] if r.get("morphology_code") == code and any(pos_has in p for p in r["positive"]))
def r3a(d): rule(d, "9364", "NKX2-2")["positive"] = ["CD99 (strong, diffuse, membranous)"]
def r3b(d): rule(d, "9364", "FET::ETS")["positive"] = ["CD99 (strong, diffuse, membranous)"]
def r3c(d):
    for r in node(d, "bn_round_cell_ihc")["resolution_logic"]:
        if r.get("morphology_code") == "9364": r["morphology_code"] = "8803"
ctl("R3-A the CD99+NKX2-2 rule loses NKX2-2", bd.check_group8_ewing_requires_partner, r3a)
ctl("R3-B the FET::ETS rule becomes CD99 alone", bd.check_group8_ewing_requires_partner, r3b)
ctl("R3-C no marker rule emits 9364 at all", bd.check_group8_ewing_requires_partner, r3c)

wrong = 0
for name, failed, msg in controls:
    expect_fail = not name.startswith("PROBE")
    ok = failed == expect_fail
    wrong += not ok
    verdict = ("CAUGHT" if failed else "PASSES") if ok else "*** WRONG ***"
    print("%-70s %s | %s" % (name, verdict, msg))
sys.exit(1 if wrong else 0)
