#!/usr/bin/env python3
"""Negative controls and correct-data probes for the ten Group 9 checks.

Runs each check function from build/build_database.py directly on a mutated in-memory copy
of data/database/group_09_dt.json as committed, and prints what it reports. Nothing on disk
is changed.
"""
import copy, json, subprocess, sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REPO / "build"))
import build_database as bd  # noqa: E402

PATH = REPO / "data" / "database" / "group_09_dt.json"
BASE = json.loads(PATH.read_text())
COMMIT = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                        capture_output=True, text=True).stdout.strip()


def ctx_of(data):
    return bd.DTContext(PATH, data, 9)


def nodes(d):
    return {n["node_id"]: n for n in d["decision_trees"][0]["nodes"]}


def opt(d, nid, frag):
    for o in nodes(d)[nid].get("options", []):
        if frag in (o.get("label") or o.get("finding") or ""):
            return o
    raise KeyError((nid, frag))


def rule(d, nid, code=None, refer=None):
    for r in nodes(d)[nid]["resolution_logic"]:
        if (code and r.get("morphology_code") == code) or (refer and r.get("refer_group") == refer):
            return r
    raise KeyError((nid, code, refer))


def run(check, d, *extra):
    return check(ctx_of(d), *extra)


results = []


def control(name, check, mutate, expect_fail, extra=(), contains=None):
    d = copy.deepcopy(BASE)
    if mutate:
        mutate(d)
    out = run(check, d, *extra)
    fails = [m for lvl, m in out if lvl == bd.FAIL]
    ok = bool(fails) == expect_fail and (not contains or any(contains in f for f in fails))
    results.append((name, check.__name__, expect_fail, ok, fails[:2] if fails else [m for _, m in out][:1]))


R = REPO
# ---------------------------------------------------------------- baseline (false-FAIL control)
for chk, extra in [(bd.check_group9_code_set, ()), (bd.check_group9_absent_codes, ()),
                   (bd.check_group9_ewing_code, ()), (bd.check_group9_basis_rows, ()),
                   (bd.check_group9_kaposi_hhv8, ()), (bd.check_group9_8963_site, (R,)),
                   (bd.check_group9_no_imaging_sufficient, ()), (bd.check_group9_no_flow_cytometry, ()),
                   (bd.check_group9_obs_unreachable, ()), (bd.check_group9_leaf_claims, ())]:
    control("baseline, unmodified", chk, None, False, extra)

# ---------------------------------------------------------------- RULE 1
control("1a fabricated code 8919 emitted", bd.check_group9_code_set,
        lambda d: opt(d, "st_rms", "Embryonal").__setitem__("morphology_code", "8919"), True, contains="8919")
control("1b entry deleted", bd.check_group9_code_set,
        lambda d: d["morphology_entries"].pop(0), True, contains="no morphology_entries")
control("1c entry behaviour changed to /1", bd.check_group9_code_set,
        lambda d: d["morphology_entries"][3].__setitem__("behavior_code", "1"), True)
# ---------------------------------------------------------------- RULE 2
control("2a Ewing option emits retired 9260", bd.check_group9_absent_codes,
        lambda d: opt(d, "st_round_cell", "Ewing sarcoma —").__setitem__("morphology_code", "9260"), True, contains="9260")
control("2b refer_code 9150", bd.check_group9_absent_codes,
        lambda d: opt(d, "st_cytology", "lineage not established").__setitem__("refer_code", "9150"), True, contains="9150")
control("2c nos_fallback 9367", bd.check_group9_absent_codes,
        lambda d: nodes(d)["st_round_cell_ihc"]["nos_fallback"].__setitem__("code", "9367"), True, contains="9367")
control("2p PROBE: 9260 named in a reason (prose) is not a FAIL", bd.check_group9_absent_codes,
        lambda d: opt(d, "st_round_cell", "Askin").__setitem__("reason", "Not 9260; Askin tumour is 9365/3."), False)
# ---------------------------------------------------------------- RULE 3
control("3a Ewing option emits 8803", bd.check_group9_ewing_code,
        lambda d: opt(d, "st_round_cell", "Ewing sarcoma —").__setitem__("morphology_code", "8803"), True)
control("3b CIC option emits 9364", bd.check_group9_ewing_code,
        lambda d: opt(d, "st_round_cell", "CIC-rearranged").__setitem__("morphology_code", "9364"), True)
control("3c BCOR option emits 9364", bd.check_group9_ewing_code,
        lambda d: opt(d, "st_round_cell", "BCOR").__setitem__("morphology_code", "9364"), True)
control("3d 9364 marker rule on a CIC-rearranged profile (WT1, ETV4)", bd.check_group9_ewing_code,
        lambda d: rule(d, "st_round_cell_ihc", code="9364").__setitem__("positive", ["WT1", "ETV4"]), True, contains="9364")
control("3e 9364 marker rule on CD99 alone", bd.check_group9_ewing_code,
        lambda d: rule(d, "st_round_cell_ihc", code="9364").__setitem__("positive", ["CD99"]), True, contains="NKX2.2")
control("3p PROBE: 'Ewing-like' label emitting 8803 is not a FAIL", bd.check_group9_ewing_code,
        lambda d: opt(d, "st_round_cell", "Undifferentiated round cell").__setitem__(
            "label", "Ewing-like undifferentiated round cell sarcoma"), False)
# ---------------------------------------------------------------- RULE 4
control("4a cutaneous KS basis 1 without skin capture", bd.check_group9_basis_rows,
        lambda d: opt(d, "st_clinical_alias", "Kaposi sarcoma recognised")["captures"].__setitem__("lesion_site", "non_skin"), True)
control("4b basis 1 on 8800", bd.check_group9_basis_rows,
        lambda d: opt(d, "st_imaging_report", "soft tissue sarcoma is likely").__setitem__("basis_of_diagnosis", 1), True)
control("4c basis 2 on 8910 (no Visser row)", bd.check_group9_basis_rows,
        lambda d: opt(d, "st_rms", "Embryonal").__setitem__("basis_of_diagnosis", 2), True)
control("4d basis 2 on a next_node branch", bd.check_group9_basis_rows,
        lambda d: opt(d, "st_report_contents", "Routine (H&E)").__setitem__("basis_of_diagnosis", 2), True)
control("4p PROBE: basis 2 on 9120 (a Visser row) is not a FAIL", bd.check_group9_basis_rows,
        lambda d: opt(d, "st_vascular", "Angiosarcoma").__setitem__("basis_of_diagnosis", 2), False)
# ---------------------------------------------------------------- RULE 5
control("5a KS option records HHV-8 negative", bd.check_group9_kaposi_hhv8,
        lambda d: opt(d, "st_vascular", "not tested or not reported")["captures"].__setitem__("hhv8_lana", "negative"), True)
control("5b KS marker rule keyed on the wrong marker", bd.check_group9_kaposi_hhv8,
        lambda d: rule(d, "st_spindle_ihc", code="9140").__setitem__("positive", ["Desmin"]), True)
control("5c KS marker rule with HHV-8 required negative", bd.check_group9_kaposi_hhv8,
        lambda d: rule(d, "st_spindle_ihc", code="9140").__setitem__("negative", ["HHV-8 LANA-1"]), True)
control("5p PROBE: KS 'as stated' after a negative stain (captured upstream) is not a FAIL",
        bd.check_group9_kaposi_hhv8, None, False)
# ---------------------------------------------------------------- RULE 6
def drop_cns(d):
    n = nodes(d)["st_epithelioid_ihc"]
    n["resolution_logic"] = [r for r in n["resolution_logic"] if r.get("refer_group") != 3]
control("6a CNS referral rule removed", bd.check_group9_8963_site, drop_cns, True, (R,), contains="Group 3")
def short_cns(d):
    r = rule(d, "st_epithelioid_ihc", refer=3)
    r["when"]["topography"] = ["C70.9", "C71.9", "C72.9"]
control("6b CNS referral at NOS level only", bd.check_group9_8963_site, short_cns, True, (R,), contains="missing")
def move_kidney_after(d):
    n = nodes(d)["st_epithelioid_ihc"]; rl = n["resolution_logic"]
    k = [r for r in rl if r.get("refer_group") == 6][0]; rl.remove(k); rl.append(k)
control("6c kidney referral after the 8963 rule", bd.check_group9_8963_site, move_kidney_after, True, (R,), contains="Group 6")
def direct_8963(d):
    o = opt(d, "st_uncertain", "Rhabdoid tumour")
    o.pop("next_node"); o.update({"morphology_code": "8963", "behavior_code": "3", "basis_of_diagnosis": 7})
control("6d named rhabdoid option emits 8963 directly", bd.check_group9_8963_site, direct_8963, True, (R,), contains="outside an ihc_checklist")
control("6e 8963 rule without SMARCB1 loss", bd.check_group9_8963_site,
        lambda d: rule(d, "st_epithelioid_ihc", code="8963").__setitem__("positive", ["TFE3"]), True, (R,))
def scalar_kidney(d):
    rule(d, "st_epithelioid_ihc", refer=6)["when"]["topography"] = "C64.9"
control("6p PROBE: kidney referral with a scalar topography (engine form) is not a FAIL",
        bd.check_group9_8963_site, scalar_kidney, False, (R,))
# ---------------------------------------------------------------- RULE 7-9
control("7a 8800 imaging_sufficient", bd.check_group9_no_imaging_sufficient,
        lambda d: [e for e in d["morphology_entries"] if e["morphology_code"] == "8800"][0].__setitem__("imaging_sufficient", True), True)
control("7b imaging_pathway node", bd.check_group9_no_imaging_sufficient,
        lambda d: nodes(d)["st_imaging_report"].__setitem__("node_type", "imaging_pathway"), True)
control("8a Flow cytometry in an entry", bd.check_group9_no_flow_cytometry,
        lambda d: d["morphology_entries"][0]["diagnostic_tests_required"].append("Flow cytometry"), True)
control("8b Flow cytometry in satisfies_tests", bd.check_group9_no_flow_cytometry,
        lambda d: opt(d, "st_vascular", "LANA-1) immunohistochemistry positive")["satisfies_tests"].append("Flow cytometry"), True)
control("9a tree emits 9560", bd.check_group9_obs_unreachable,
        lambda d: opt(d, "st_nerve_sheath", "Malignant perineurioma").__setitem__("morphology_code", "9560"), True)
control("9b tree emits 8853", bd.check_group9_obs_unreachable,
        lambda d: opt(d, "st_adipocytic", "Myxoid liposarcoma").__setitem__("morphology_code", "8853"), True)
# ---------------------------------------------------------------- RULE 10
control("10a leaf claimed, never emitted (9042 option recoded)", bd.check_group9_leaf_claims,
        lambda d: opt(d, "st_synovial", "Epithelioid cell").__setitem__("morphology_code", "9040"), True, contains="9042")
def emit_direct_only(d):
    opt(d, "st_rms", "Mixed embryonal").__setitem__("morphology_code", "8991")
control("10b direct-only code emitted (8991)", bd.check_group9_leaf_claims, emit_direct_only, True, contains="8991")
def note_both(d):
    e = d["morphology_entries"][0]; e["coding_note"] += " Reached by the g9_soft_tissue tree."
control("10c coding_note claims both", bd.check_group9_leaf_claims, note_both, True)

print("Group 9 negative controls against %s (HEAD %s)\n" % (PATH.relative_to(REPO), COMMIT))
bad = 0
for name, chk, expect, ok, msgs in results:
    bad += not ok
    print("%-4s %-70s %-38s expect %-4s" % ("ok" if ok else "BAD", name, chk, "FAIL" if expect else "OK"))
    for m in msgs:
        print("        " + m[:230])
print("\n%d control(s), %d not behaving as expected" % (len(results), bad))
sys.exit(1 if bad else 0)
