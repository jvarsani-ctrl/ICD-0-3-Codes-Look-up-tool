#!/usr/bin/env python3
"""Negative controls for the Group 7 checks in build/build_database.py.

Group 7 build contract §8, §9 point 3; standing rule 10. Each control copies
data/database/group_07_dt.json (and, for the alias and router checks, the files those
checks read) into memory or a scratch directory, breaks ONE thing, runs the ONE check
that should catch it, and records whether it FAILed with the expected message. The
unmodified data runs first: every check must report OK on correct data, because a
false FAIL is the more corrosive defect.

Nothing under data/ is written. Run from the repository root:

    ICD_LAYER1="<vault>/ICD coding" python3 build/negative_controls_group07.py

Exit 0 when every control is caught and the correct data passes; 1 otherwise.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))
import build_database as bd  # noqa: E402

LAYER1 = Path(os.environ.get("ICD_LAYER1", str(REPO.parents[1] / "ICD coding")))
DT = json.loads((REPO / "data" / "database" / "group_07_dt.json").read_text(encoding="utf-8"))
ALIASES = json.loads((REPO / "data" / "aliases" / "aliases_group_07.json").read_text(encoding="utf-8"))
ROUTER = json.loads((REPO / "data" / "shared" / "presentation_router.json").read_text(encoding="utf-8"))


def nodes(d):
    return {n["node_id"]: n for n in d["decision_trees"][0]["nodes"]}


def option(d, node_id, label_start):
    for o in nodes(d)[node_id].get("options") or []:
        if str(o.get("label", "")).startswith(label_start):
            return o
    raise KeyError((node_id, label_start))


def rule(d, node_id, i):
    return nodes(d)[node_id]["resolution_logic"][i]


def entry(d, code):
    return next(e for e in d["morphology_entries"] if e["morphology_code"] == code)


def ctx_of(d):
    return bd.DTContext(REPO / "data" / "database" / "group_07_dt.json", d, 7)


def scratch_repo(dt=None, aliases=None, router=None):
    root = Path(tempfile.mkdtemp(prefix="g7nc_"))
    for sub in ("data/database", "data/aliases", "data/shared"):
        (root / sub).mkdir(parents=True)
    (root / "data/database/group_07_dt.json").write_text(json.dumps(dt or DT), encoding="utf-8")
    (root / "data/aliases/aliases_group_07.json").write_text(json.dumps(aliases or ALIASES),
                                                             encoding="utf-8")
    (root / "data/shared/presentation_router.json").write_text(json.dumps(router or ROUTER),
                                                               encoding="utf-8")
    return root


CHECKS = {
    1: lambda d, r: bd.check_group7_code_set(ctx_of(d)),
    2: lambda d, r: bd.check_group7_absent_codes(ctx_of(d), r),
    3: lambda d, r: bd.check_group7_behaviour_declaration(ctx_of(d), LAYER1),
    4: lambda d, r: bd.check_group7_ini1_fork(ctx_of(d)),
    5: lambda d, r: bd.check_group7_c22_only_codes(ctx_of(d)),
    6: lambda d, r: bd.check_group7_no_tissue_codes(ctx_of(d)),
    7: lambda d, r: bd.check_group7_imaging_constellation(ctx_of(d)),
    8: lambda d, r: bd.check_group7_fibrolamellar(ctx_of(d)),
    9: lambda d, r: bd.check_group7_router_c22(r, LAYER1),
    "rt": lambda d, r: bd.check_icdo32_round_trip(ctx_of(d), LAYER1),
    "be": lambda d, r: bd.check_behaviour_exclusion(ctx_of(d), LAYER1),
}


def run(rule_no, d=None, aliases=None, router=None):
    d = d if d is not None else copy.deepcopy(DT)
    root = scratch_repo(d, aliases, router)
    try:
        return CHECKS[rule_no](d, root)
    finally:
        shutil.rmtree(root, ignore_errors=True)


# --------------------------------------------------------------------------------------
# The controls. Each: (id, rule, description, mutate(dt, aliases, router), expected text)
# --------------------------------------------------------------------------------------
def m_entry_code(d, a, r):
    entry(d, "8970")["morphology_code"] = "8971"


def m_emit_fabricated(d, a, r):
    option(d, "hp_hcc_subtype", "Scirrhous")["morphology_code"] = "8176"


def m_fallback_fabricated(d, a, r):
    nodes(d)["hp_ini1"]["nos_fallback"]["code"] = "8999"


def m_emit_8975(d, a, r):
    o = option(d, "hp_histology", "Calcifying nested")
    o.pop("behaviour_exclusion")
    o.update(morphology_code="8975", behavior_code="3", basis_of_diagnosis=7, reason="x")


def m_alias_8975(d, a, r):
    next(x for x in a if x["alias"].startswith("Calcifying nested"))["maps_to_morphology_codes"] = ["8975"]


def m_entry_fallback_9013(d, a, r):
    entry(d, "8010")["nos_fallback_code"] = "9013"


def m_group_declares(d, a, r):
    option(d, "hp_histology", "Calcifying nested")["behaviour_exclusion"]["group_declares"] = "0-1,3"


def m_exclusion_off_stem(d, a, r):
    be = option(d, "hp_histology", "Bile duct adenoma")["behaviour_exclusion"]
    be.update(icdo_code="9131", icdo_behaviour="0", icdo_term="Capillary hemangioma")


def m_exclusion_fake_pair(d, a, r):
    option(d, "hp_histology", "Calcifying nested")["behaviour_exclusion"]["icdo_behaviour"] = "3"


def m_8963_no_loss_marker(d, a, r):
    rule(d, "hp_ini1", 0)["positive"] = ["SMARCB1 (INI1) performed and RETAINED with a valid internal control"]


def m_scud_emits_8970(d, a, r):
    o = option(d, "hp_histology", "A small cell undifferentiated")
    o.pop("next_node")
    o.update(morphology_code="8970", behavior_code="3", basis_of_diagnosis=7, reason="x")


def m_8970_on_loss(d, a, r):
    rule(d, "hp_ini1", 2)["positive"] = [
        "SMARCB1 (INI1) loss (nuclear expression lost in tumour cells, internal control retained)"]


def m_ini1_fallback_8970(d, a, r):
    fb = nodes(d)["hp_ini1"]["nos_fallback"]
    fb.update(code="8970", name="Hepatoblastoma, NOS")


def m_drop_retained_rule(d, a, r):
    del nodes(d)["hp_ini1"]["resolution_logic"][2]


def m_inventory_drops_c22(d, a, r):
    option(d, "hp_document_inventory", "Histology report")["captures"].pop("primary_site")


def m_8963_no_when(d, a, r):
    rule(d, "hp_ini1", 0).pop("when")


def m_imaging_emits_8170(d, a, r):
    nodes(d)["hp_imaging_pathway"]["morphology_code"] = "8170"


def m_alias_basis1_8970(d, a, r):
    option(d, "hp_clinical_alias", "The note states")["morphology_code"] = "8970"


def m_basis4(d, a, r):
    option(d, "hp_imaging_insufficient", "An imaging report")["basis_of_diagnosis"] = 4


def m_no_afp(d, a, r):
    nodes(d)["hp_imaging_pathway"]["biochemical_questions"] = []


def m_afp_no(d, a, r):
    nodes(d)["hp_imaging_pathway"]["biochemical_questions"][0]["required_answer"] = "no"


def m_no_infant_diversion(d, a, r):
    n = nodes(d)["hp_imaging_pathway"]
    n["diversion_criteria"] = [x for x in n["diversion_criteria"] if "6 months" not in x["feature"]]


def m_hcc_imaging_sufficient(d, a, r):
    entry(d, "8170")["imaging_sufficient"] = True


def m_fusion_emits_8170(d, a, r):
    option(d, "hp_flc_molecular", "DNAJB1::PRKACA")["morphology_code"] = "8170"


def m_flc_histology_8170(d, a, r):
    o = option(d, "hp_hcc_subtype", "Fibrolamellar")
    o.pop("next_node")
    o.update(morphology_code="8170", behavior_code="3", basis_of_diagnosis=7, reason="x")


def m_untested_8170(d, a, r):
    option(d, "hp_flc_molecular", "Not tested")["morphology_code"] = "8170"


def m_no_8171(d, a, r):
    for o in nodes(d)["hp_flc_molecular"]["options"]:
        o["morphology_code"] = "8170"


def m_router_drop_8963_c22(d, a, r):
    br = r["dual_group_rules"]["8963"]["branches"]
    r["dual_group_rules"]["8963"]["branches"] = [b for b in br if b["result"]["group"] != 7]


def m_router_8991_wrong_subgroup(d, a, r):
    r["dual_group_rules"]["8991"]["branches"][0]["result"]["subgroup"] = "VIIa1"


def m_router_8170_default_11(d, a, r):
    r["dual_group_rules"]["8170"]["default"] = {"group": 11, "subgroup": None}


def m_router_drop_8000_c22(d, a, r):
    br = r["dual_group_rules"]["8000-8005"]["branches"]
    r["dual_group_rules"]["8000-8005"]["branches"] = [b for b in br if b["result"]["group"] != 7]


def m_name_redcap_string(d, a, r):
    entry(d, "8970")["morphology_name"] = "Hepatoblastoma"


def m_exclusion_synonym_term(d, a, r):
    option(d, "hp_histology", "Hepatocellular adenoma")["behaviour_exclusion"]["icdo_term"] = "Hepatocellular adenoma"


CONTROLS = [
    ("1A", 1, "an entry's code fabricated, 8970 -> 8971", m_entry_code, "morphology_entries"),
    ("1B", 1, "a node emits a fabricated 8176", m_emit_fabricated, "emits 8176"),
    ("1C", 1, "the INI1 fallback names 8999", m_fallback_fabricated, "falls back to 8999"),
    ("2A", 2, "CNSET emitted as 8975/3", m_emit_8975, "8975"),
    ("2B", 2, "the CNSET alias maps to 8975", m_alias_8975, "aliases_group_07.json"),
    ("2C", 2, "an entry's nos_fallback_code is 9013", m_entry_fallback_9013, "nos_fallback_code is 9013"),
    ("3A", 3, "group_declares copied from Group III, '0-1,3'", m_group_declares, "group_declares"),
    ("3B", 3, "a behaviour exclusion on 9131/0, no Group VII stem", m_exclusion_off_stem, "not on a Group VII stem"),
    ("3C", 3, "CNSET exclusion names 8975/3, not a real pair", m_exclusion_fake_pair, "not a real pair"),
    ("4A", 4, "the SMARCB1 8963 rule keyed on INI1 RETAINED", m_8963_no_loss_marker, "RULE 4(a)"),
    ("4B", 4, "the SCUD histology option codes 8970 directly", m_scud_emits_8970, "RULE 4(c)"),
    ("4C", 4, "the 8970 rule keyed on INI1 loss", m_8970_on_loss, "RULE 4(b)"),
    ("4D", 4, "INI1 not done falls back to 8970", m_ini1_fallback_8970, "falls back to 8970"),
    ("4E", 4, "the INI1-retained 8970 rule deleted", m_drop_retained_rule, "RULE 4(d)"),
    ("5A", 5, "the histology route no longer captures C22", m_inventory_drops_c22, "never established"),
    ("5B", 5, "an 8963 rule loses its primary_site when", m_8963_no_when, "without `when` primary_site"),
    ("6A", 6, "the imaging node codes 8170 at basis 2", m_imaging_emits_8170, "8170 at basis 2"),
    ("6B", 6, "a referral note codes 8970 at basis 1", m_alias_basis1_8970, "8970 at basis 1"),
    ("6C", 6, "no tissue, 8000 at basis 4", m_basis4, "8000 at basis 4"),
    ("7A", 7, "the alpha-fetoprotein question removed", m_no_afp, "no alpha-fetoprotein question"),
    ("7B", 7, "the alpha-fetoprotein question requires 'no'", m_afp_no, "no alpha-fetoprotein question"),
    ("7C", 7, "the under-6-months diversion removed", m_no_infant_diversion, "younger than 6 months"),
    ("7D", 7, "8170 marked imaging_sufficient", m_hcc_imaging_sufficient, "entry 8170 is imaging_sufficient"),
    ("8A", 8, "a DNAJB1::PRKACA finding codes 8170", m_fusion_emits_8170, "RULE 8(c)"),
    ("8B", 8, "the fibrolamellar histology option codes 8170", m_flc_histology_8170, "RULE 8(b)"),
    ("8C", 8, "'not tested' fibrolamellar codes 8170", m_untested_8170, "RULE 8(d)"),
    ("8D", 8, "every fibrolamellar branch codes 8170", m_no_8171, "RULE 8(a)"),
    ("9A", 9, "the router's 8963 C22 branch removed", m_router_drop_8963_c22, "8963 at C22.0"),
    ("9B", 9, "the 8991 C22 branch names VIIa1", m_router_8991_wrong_subgroup, "8991 at C22.0"),
    ("9C", 9, "the 8170 default reverted to group 11", m_router_8170_default_11, "8170 at C24.0"),
    ("9D", 9, "the 8000-8005 C22 branch removed", m_router_drop_8000_c22, "8000 at C22.0"),
    ("RT", "rt", "8970 named by REDCap's string 'Hepatoblastoma'", m_name_redcap_string, "Hepatoblastoma"),
    ("BE", "be", "the 8170/0 exclusion names its synonym", m_exclusion_synonym_term, "not the PREFERRED one"),
]


def main() -> int:
    ok = True
    print("== correct data (false-FAIL control)")
    for rule_no in CHECKS:
        findings = run(rule_no)
        fails = [m for lvl, m in findings if lvl == bd.FAIL]
        oks = [m for lvl, m in findings if lvl == bd.OK]
        status = "FAIL" if fails else ("OK" if oks else "EMPTY")
        if fails or not oks:
            ok = False
        print("  rule %-3s %s  %s" % (rule_no, status, (fails or oks or [""])[0][:150]))
    print("\n== negative controls")
    for cid, rule_no, desc, mutate, expect in CONTROLS:
        d, a, r = copy.deepcopy(DT), copy.deepcopy(ALIASES), copy.deepcopy(ROUTER)
        mutate(d, a, r)
        findings = run(rule_no, d, a, r)
        fails = [m for lvl, m in findings if lvl == bd.FAIL]
        hit = [m for m in fails if expect in m]
        caught = bool(hit)
        ok &= caught
        print("  %-3s rule %-3s %-6s %s" % (cid, rule_no, "CAUGHT" if caught else "MISSED", desc))
        print("        %s" % ((hit or fails or ["no FAIL raised"])[0][:220]))
    print("\n%s" % ("ALL CONTROLS CAUGHT, CORRECT DATA PASSES" if ok else "CONTROL FAILURES ABOVE"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
