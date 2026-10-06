"""The ICCC-3 Group X decision trees, as data.

Authored here rather than by hand in group_10_dt.json so the trees and the entries regenerate
together from one command (build/generate_group10_entries.py). Edit the trees HERE; the JSON is
the product. Architecture: docs/group_10_build_contract.md §4. Code decisions D1-D22:
docs/superpowers/specs/2026-10-04-group-10-germ-cell-code-decisions-design.md.

Four site trees share one set of node builders, parameterised by SITES, so the histotype
logic is written once: g10_cns (cn_), g10_ovary (ov_), g10_testis (ts_), g10_extragonadal
(eg_). The evidence, cytology, mixed and stain panel nodes are one builder each; every
histology node is the site's own germinoma-family and teratoma options, then the shared
germ_cell_core(), then the site's other tumour lines. The router's tree_routing picks the tree
from the captured topography. Every entry into Group X carries one: the front door records it
at Stage 1, and the express lane asks the site before it enters a group whose data reads the
site (registrar, 4 October 2026).

Clerk-facing text lives in `question`, `hint`, `label`, `reason` and `upgrade_path`.
`coding_note` is author-facing and never rendered. No clerk-facing string names a node id or a
schema field (check_no_internal_identifier_leaks). `clinical_alert` is null everywhere
(ruling 9). Every name a reason gives a code is the ICD-O-3.2 Preferred term, read from
icdo32.sqlite when the trees are built (term()), never typed.

Tree `topography` values are author-facing documentation. The validator reads them only for
Groups 3 and 4, so this file writes the Group 8 range format, converted from the ICCC-2017
range strings in TOPOGRAPHY_RAW.
"""
from __future__ import annotations

import copy
import json
import os
import sqlite3
from pathlib import Path

import generate_group_inventory as gi  # build/ is on sys.path for every caller

_PREFERRED: dict | None = None


class TreeError(Exception):
    """A tree names a (code, behaviour) ICD-O-3.2 does not carry, or Layer 1 is absent or
    unreadable. generate_group10_entries.py turns it into exit 2."""


def _icdo_path() -> Path:
    return Path(os.environ.get("ICDO_DB", str(gi.DEFAULT_ICDO))).resolve()


def term(code: str, beh: str) -> str:
    """The ICD-O-3.2 Preferred term at (code, behaviour), from icdo32.sqlite."""
    global _PREFERRED
    if _PREFERRED is None:
        path = _icdo_path()
        if not path.exists():
            raise TreeError("icdo32.sqlite not found at %s — set ICDO_DB" % path)
        index: dict = {}
        try:
            con = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
            try:
                for c, b, t in con.execute(
                        "SELECT code4, behaviour, term FROM icd_o_3_2_morphology WHERE "
                        "level = 'Preferred' AND code4 IS NOT NULL AND behaviour IS NOT NULL"):
                    key = (str(c), str(b))
                    if key in index and index[key] != t:
                        raise TreeError("icdo32.sqlite carries two Preferred terms at %s/%s"
                                        % key)
                    index[key] = str(t)
            finally:
                con.close()
        except sqlite3.Error as exc:
            raise TreeError("icdo32.sqlite at %s could not be read: %s" % (path, exc)) from None
        _PREFERRED = index
    try:
        return _PREFERRED[(code, beh)]
    except KeyError:
        raise TreeError("ICD-O-3.2 has no Preferred term at %s/%s" % (code, beh)) from None


# ------------------------------------------------------------------------------------------
# Shared wording
# ------------------------------------------------------------------------------------------
VISSER = "Visser 2023, European Network of Cancer Registries"
SIEGMUND = "Siegmund 2023"
NOT_REGISTRABLE_POSSIBLE = (
    "Cancer is only possible on this evidence. Under the European registry rules a case that "
    "is only possibly cancer is not registered without pathology (%s, rule 4)." % VISSER)
EVIDENCE_TIER = ["evidence_tests", "workup_status", "basis_evidence_tier"]
BASIS_DEFAULTS = {"ihc_counts_as": 7, "methylation_counts_as": 8}
NO_TISSUE_BASIS = (1, 2, 4, 5)

# A named germ cell type whose entry requires IHC (generate_group10_entries.py sets Histology
# and IHC on every code a checklist rule emits). On a branch where the report NAMES the type,
# the engine's automatic upgrade line would say IHC "would yield a more specific code", which
# is false there; this authored line replaces it. IHC still shows as outstanding, so the case
# does not look better evidenced than the file is (Group 7 precedent: DNAJB1::PRKACA).
IHC_CONFIRMS = ("Immunohistochemistry, where the report does not describe it, confirms the "
                "germ cell type the report names; it does not change this code.")
# The upgrade line for a terminal whose report does not determine the type. Without one, app.js
# prints "None — fully subtyped at this evidence tier" (code review, 6 October 2026).
TYPE_NOT_STATED = ("The report does not state the tumour's type. A report that names it gives "
                   "that type's own code; where this step does not list it, record it with "
                   "'Override this code'.")

BEH_TEXT = {"0": "behaviour 0, benign", "1": "behaviour 1, uncertain or borderline",
            "2": "behaviour 2, in situ"}
OUTSIDE_CNS = ("Outside the central nervous system ICCC-3 Group X registers behaviour 3 "
               "(malignant) only, so no Group X code is recorded.")
SETTLED = " Whether the registry records it elsewhere is the registrar's decision."
PENDING = " This exclusion awaits the registrar's decision."
PSTT_REASON = (
    "ICD-O-3.2 codes placental site trophoblastic tumour 9104/1, behaviour 1, uncertain or "
    "borderline. WHO 2022 prints 9104/3, a code approved after ICD-O-3.2 (Moch 2022, Table 3, "
    "pp. 464-465). The case is not recorded as a Group X cancer until the registrar rules.")

# ICCC-2017.sqlite code_ranges topography strings: range 94 (Xa), 100 (Xb), 106 (Xc).
TOPOGRAPHY_RAW = {
    "cns": "700-729,751-753",
    "ovary": "569",
    "testis": "620-629",
    "extragonadal": "000-559,570-619,630-699,739-750,754-768,809",
}


def _topo(raw: str) -> list:
    def one(n):
        n = int(n)
        return "C%02d.%d" % (n // 10, n % 10)
    out = []
    for part in raw.split(","):
        ends = part.split("-")
        out.append(one(ends[0]) if len(ends) == 1 else "%s-%s" % (one(ends[0]), one(ends[1])))
    return out


# ------------------------------------------------------------------------------------------
# Branch helpers (the Group 8 shapes)
# ------------------------------------------------------------------------------------------
def _tail(b, captures=None, note=None, negative=None, satisfies=None, upgrade=None,
          heading=None):
    """Append the optional keys every branch helper shares, in one fixed order."""
    if satisfies:
        b["satisfies_tests"] = satisfies
    if upgrade:
        b["upgrade_path"] = upgrade
    if heading:
        b["non_reportable_heading"] = heading
    if note:
        b["coding_note"] = note
    if captures:
        b["captures"] = captures
    if negative:
        b["negative"] = negative
    return b


def rec(morph: str, beh: str = "3", basis: int | None = None) -> str:
    """'Recorded as Germinoma (9064/3).' — the Preferred term, never a typed name."""
    at = " at basis of diagnosis %d" % basis if basis in NO_TISSUE_BASIS else ""
    return "Recorded as %s (%s/%s)%s." % (term(morph, beh), morph, beh, at)


def code(label, morph, beh, basis, reason, captures=None, satisfies=None, note=None,
         upgrade=None, key="label", negative=None):
    term(morph, beh)  # fail at build time on a pair ICD-O-3.2 does not carry
    b = {key: label, "morphology_code": morph, "behavior_code": beh,
         "basis_of_diagnosis": basis, "reason": reason}
    return _tail(b, captures, note, negative, satisfies, upgrade)


def go(label, node_id, captures=None, note=None):
    return _tail({"label": label, "next_node": node_id}, captures, note)


def excl(label, icdo, beh, reason, decision=False, captures=None, note=None):
    """A behaviour exclusion. icdo_term is the ICD-O-3.2 Preferred term, looked up here."""
    return _tail({"label": label,
                  "behaviour_exclusion": {"icdo_code": icdo, "icdo_behaviour": beh,
                                          "icdo_term": term(icdo, beh), "group_declares": "3",
                                          "reason": reason,
                                          "registrar_decision_required": decision}},
                 captures, note)


def excl_outside(label, what, icdo, beh, decision=False, extra="", note=None):
    """An exclusion whose reason is the standard one: the behaviour is not Group X here."""
    reason = "ICD-O-3.2 codes %s as %s (%s/%s), %s. %s%s%s" % (
        what, term(icdo, beh), icdo, beh, BEH_TEXT[beh], (extra + " ") if extra else "",
        OUTSIDE_CNS, PENDING if decision else SETTLED)
    return excl(label, icdo, beh, reason, decision=decision, note=note)


def excl_d(label, what, icdo, beh, d, decision=False, extra=""):
    """excl_outside whose author note names the design decision and whether it is open."""
    return excl_outside(label, what, icdo, beh, decision=decision, extra=extra,
                        note="%s, %s." % (d, "provisional" if decision else "settled"))


def sex_cord_excl(label, what, icdo, beh, decision=False):
    """A D11 exclusion. An open one is also D12's question: no /3 that ICD-O-3.2 does not
    print."""
    return excl_d(label, what, icdo, beh, "D11, D12" if decision else "D11", decision=decision)


def nonrep(label, reason, captures=None, note=None, heading=None):
    return _tail({"label": label, "non_reportable": True, "reason": reason}, captures, note,
                 heading=heading)


def refer(label, group, reason, captures=None, note=None):
    """A cross-group referral. No refer_code: every unspecified code a Group X referral could
    name (8000, 8001) is also a Group X entry, and check_refer_terminals fails a refer_code
    this file owns outright. The reason names the code instead."""
    return _tail({"label": label, "refer_group": group, "reason": reason}, captures, note)


def node(node_id, node_type, step, step_label, question, hint, options, captured, note,
         **extra):
    n = {"node_id": node_id, "node_type": node_type, "step_number": step,
         "step_label": step_label, "question": question, "hint": hint,
         "clinical_alert": None, "coding_note": note, "captured_variables": list(captured)}
    if options is not None:
        n["options"] = options
    n.update(extra)
    n.setdefault("nos_fallback", None)
    return n


# ------------------------------------------------------------------------------------------
# Sites
# ------------------------------------------------------------------------------------------
GONADS = ("ovary", "testis")
# One record per site tree. family / family_term: the germinoma-family code and the name the
# site's reports use for it (D3). fluid: what its cytology samples. yolk_sac /
# choriocarcinoma: the site's wording of the shared germ cell options. where: the gonad, for
# the referral wording of the other node.
SITES = {
    "cns": {
        "prefix": "cn_", "tree": "g10_cns", "family": "9064", "family_term": "germinoma",
        "fluid": "cerebrospinal fluid",
        "yolk_sac": "Yolk sac tumour (endodermal sinus tumour)",
        "choriocarcinoma": "Choriocarcinoma"},
    "ovary": {
        "prefix": "ov_", "tree": "g10_ovary", "family": "9060", "family_term": "dysgerminoma",
        "fluid": "ascitic fluid or a fine-needle aspirate", "where": "the ovary",
        "yolk_sac": "Yolk sac tumour (endodermal sinus tumour)",
        "choriocarcinoma": "Non-gestational choriocarcinoma"},
    "testis": {
        "prefix": "ts_", "tree": "g10_testis", "family": "9061", "family_term": "seminoma",
        "fluid": "a fine-needle aspirate", "where": "the testis",
        "yolk_sac": "Yolk sac tumour, prepubertal or postpubertal type",
        "yolk_sac_reason": "WHO 2022 codes both types 9071/3 (Moch 2022, Table 3, p. 464).",
        "choriocarcinoma": "Choriocarcinoma"},
    "extragonadal": {
        "prefix": "eg_", "tree": "g10_extragonadal", "family": "9064",
        "family_term": "germinoma", "fluid": "an effusion or a fine-needle aspirate",
        "yolk_sac": "Yolk sac tumour (endodermal sinus tumour)",
        "choriocarcinoma": "Choriocarcinoma, gestational or non-gestational"},
}


def nid(site: str, name: str) -> str:
    return SITES[site]["prefix"] + name


def unspecified(site, label, basis, morph, why, captures=None, note=None, after=""):
    """An unspecified malignancy (8000/3 or 8001/3) at this site. ICCC-2017 places 8000-8005 in
    Group X only at the gonads (range 117, Xe). In the central nervous system they are IIIf
    (range 42); at the extragonadal germ cell sites XIIb (range 143), except the liver (VIIc,
    range 58), the kidney (VIc, range 52) and bone (VIIIe, range 71)."""
    name = term(morph, "3")
    if site in GONADS:
        return code(label, morph, "3", basis,
                    " ".join(x for x in (rec(morph, "3", basis), why, after) if x),
                    captures=captures, note=note)
    if site == "cns":
        return refer(label, 3,
                     "%s ICCC-3 places %s (%s/3) in the brain and spinal cord in Group III, as "
                     "an unspecified intracranial or intraspinal neoplasm, not in Group X. Code "
                     "the case from the Group III (central nervous system tumours) tree."
                     % (why, name, morph), captures=captures,
                     note=note or "ICCC-2017 range 42 (IIIf): 8000-8005 at 700-729,751-753.")
    return refer(label, 12,
                 "%s ICCC-3 places %s (%s/3) in Group X only at the ovary and testis. At the "
                 "sacrococcygeal region, mediastinum and retroperitoneum it is a Group XII "
                 "(other and unspecified malignant neoplasms) code; at the liver, kidney or "
                 "bone it belongs to Group VII, VI or VIII. Code the case from that group's "
                 "tree." % (why, name, morph), captures=captures,
                 note=note or "ICCC-2017 range 143 (XIIb) admits 8000-8005 at "
                              "000-218,239-399,420-559,570-619,630-639,659-699,739-750,"
                              "754-809; ranges 58 (VIIc, 220-221), 52 (VIc, 649) and 71 "
                              "(VIIIe, 400-419) take the rest of the Xb sites.")


# ------------------------------------------------------------------------------------------
# Laboratory results (registrar, 6 October 2026: registrar review E2; DT master §3I)
# ------------------------------------------------------------------------------------------
# The laboratory screen follows the evidence checklist, and only when the clerk ticks Lab Report
# (registrar's ruling, 6 October 2026; it replaces the handover's design, in which the screen
# opened the tree and pre-ticked the box). app.js routes a lab_results node by its own next_node
# alone, so the gate carries the screen in its data: each tier a Lab Report can join has a copy
# that requires Lab Report and routes to a laboratory screen, and the screen's next_node is the
# tier's own destination; the tier itself now excludes Lab Report. The marker tier always
# requires Lab Report, so it routes to its screen directly, except in the brain tree, where it
# routes to the age gate cn_marker_age and reaches the screen only under 24 months or with no
# age (registrar's ruling of 6 October 2026, at brain_marker_nodes()). The imaging-only tier
# excludes Lab Report and has none. One screen per destination per tree (LAB_TIERS), all sharing the tree's
# test list. With Lab Report unticked the routes are the ones the gate had before. The rules are
# in docs/evidence_documents/group_10.json, applied by the generator.
#
# A row per test: the number as the report gives it, a unit from the test's closed list, or "Not
# in the file". The values are shown on the result and never choose a code: the node routes by
# next_node alone, and app.js keeps the values out of the case variables. The node carries no
# implies_ticks: the clerk has already ticked Lab Report.
#
# The tests per tree are the ones the sources tie to tumours that tree codes:
#   van Heerden J, Tjalma WA. Eur J Obstet Gynecol Reprod Biol 2019;243:103-110, Table 4,
#     p. 107: alpha-fetoprotein (yolk sac tumour, immature teratoma, embryonal carcinoma), beta
#     human chorionic gonadotropin (choriocarcinoma, embryonal carcinoma, dysgerminoma),
#     lactate dehydrogenase (dysgerminoma), CA-125 (epithelial tumours), inhibin A (granulosa
#     cell tumour), calcium (sex cord-stromal tumours), human epididymis protein 4 (malignant
#     and borderline epithelial tumours); p. 108: carcinoembryonic antigen.
#   Rajpert-De Meyts E, et al. Folia Histochem Cytobiol 2015;53:177-188, p. 177: beta human
#     chorionic gonadotropin, alpha-fetoprotein and lactate dehydrogenase are the classical
#     serum markers of germ cell tumours.
#   Group 10 Diagnostic Pathway §2C (Takami 2022): serum or cerebrospinal fluid
#     alpha-fetoprotein and beta human chorionic gonadotropin for a tumour of the brain.
# The ovary takes all eight tests; the testis and the extragonadal sites (the uterus and the
# placenta among them) the three germ cell markers; the brain the two markers in serum and in
# cerebrospinal fluid.
#
# Neither paper prints a unit. The unit lists are the registrar's closed lists (6 October
# 2026). Tourne 2019 (Bull Cancer 106:328-341) reports human chorionic gonadotropin in IU/L
# (pp. 331, 335) and alpha-fetoprotein in ng/mL (p. 335); Buza 2022 (Surg Pathol Clin,
# pp. 197-218) reports beta human chorionic gonadotropin in mIU/mL (p. 206); Coskun 2023 (J
# Pediatr Adolesc Gynecol 36:112-115, pp. 112-113) reports CA-125 in U/mL and calcium in mg/dL.
# The build cannot check that a unit is right; it refuses an empty or repeated list.
LAB_HINT = ("Enter each number as the report gives it, with its unit. Leave a test the file "
            "does not hold empty.")
AFP_UNITS = ("ng/mL", "µg/L", "IU/mL", "kU/L")
BHCG_UNITS = ("IU/L", "mIU/mL")
LDH_UNITS = ("U/L", "IU/L")


def lab(lab_id, label, units):
    return {"id": lab_id, "label": label, "units": list(units)}


GERM_CELL_LABS = (
    lab("afp", "Alpha-fetoprotein (AFP)", AFP_UNITS),
    lab("bhcg", "Beta human chorionic gonadotropin (β-hCG)", BHCG_UNITS),
    lab("ldh", "Lactate dehydrogenase (LDH)", LDH_UNITS),
)
SITE_LABS = {
    "cns": (
        lab("serum_afp", "Serum alpha-fetoprotein (AFP)", AFP_UNITS),
        lab("serum_bhcg", "Serum beta human chorionic gonadotropin (β-hCG)", BHCG_UNITS),
        lab("csf_afp", "Cerebrospinal fluid alpha-fetoprotein (AFP)", AFP_UNITS),
        lab("csf_bhcg", "Cerebrospinal fluid beta human chorionic gonadotropin (β-hCG)",
            BHCG_UNITS),
    ),
    "ovary": GERM_CELL_LABS + (
        lab("ca125", "Cancer antigen 125 (CA-125)", ("U/mL", "kU/L")),
        lab("he4", "Human epididymis protein 4 (HE4)", ("pmol/L",)),
        lab("cea", "Carcinoembryonic antigen (CEA)", ("ng/mL", "µg/L")),
        lab("inhibin_a", "Inhibin A", ("pg/mL", "ng/L")),
        lab("calcium", "Calcium", ("mmol/L", "mg/dL")),
    ),
    "testis": GERM_CELL_LABS,
    "extragonadal": GERM_CELL_LABS,
}


# The evidence tiers a ticked Lab Report can join: every tier but the imaging-only one, which
# excludes Lab Report.
LAB_TIERS = ("referral", "markers", "cytology", "histology")


def lab_node_id(site, tier):
    return nid(site, "labs_" + tier)


def n_labs(site, tier, destination):
    """The laboratory screen between the evidence checklist and one tier's destination."""
    via = ("from the age gate cn_marker_age, under 24 months or with no age in the file "
           "(registrar's ruling on the brain marker gates, 6 October 2026)"
           if (site, tier) == ("cns", "markers") else
           "from the evidence checklist only when Lab Report is ticked")
    return node(
        lab_node_id(site, tier), "lab_results", 2, "Laboratory results",
        "Which laboratory results are in the file?", LAB_HINT, None, [],
        "Registrar review E2 and the ruling of 6 October 2026: reached %s, then on to the %s "
        "tier's destination. The tests and their sources are listed above SITE_LABS in "
        "build/group10_tree.py. No value chooses a code." % (via, tier),
        labs=copy.deepcopy(list(SITE_LABS[site])), next_node=destination)


# ------------------------------------------------------------------------------------------
# The evidence front end (§4.2) — document inventory, referral, markers, imaging, cytology
# ------------------------------------------------------------------------------------------
TIER_CAPTURES = {
    "referral": {"evidence_tests": [], "workup_status": "not done",
                 "basis_evidence_tier": "referral"},
    "markers": {"evidence_tests": ["Imaging", "Tumour markers"], "workup_status": "incomplete",
                "basis_evidence_tier": "markers"},
    "imaging": {"evidence_tests": ["Imaging"], "workup_status": "incomplete",
                "basis_evidence_tier": "imaging"},
    "cytology": {"evidence_tests": ["Cytology"], "workup_status": "incomplete",
                 "basis_evidence_tier": "cytology"},
    "histology": {"evidence_tests": ["Histology"], "workup_status": "incomplete",
                  "basis_evidence_tier": "histology"},
}
TIER_LABELS = {
    "referral": "A referral letter or clinical note only — no imaging report, no marker "
                "result, no tissue",
    "markers": "An imaging report and a serum or cerebrospinal fluid alpha-fetoprotein or "
               "human chorionic gonadotropin result — no tissue",
    "imaging": "An imaging report only — no marker result, no tissue",
    "cytology": "Cytology only — cerebrospinal fluid, effusion or fine-needle aspirate; no "
                "tissue",
    "histology": "A histology report — biopsy or resection",
}
TIERS = ("referral", "markers", "imaging", "cytology", "histology")


def gate_options(targets, lab_targets):
    """The five tiers, in order. A tier a Lab Report can join comes twice, the copy that routes
    through the laboratory screen first; the marker tier, which always has Lab Report, comes once
    and routes through it. Labels and captures are the tier's own in every copy."""
    out = []
    for t in TIERS:
        if t in lab_targets:
            out.append(go(TIER_LABELS[t], lab_targets[t], copy.deepcopy(TIER_CAPTURES[t])))
        if t != "markers":
            out.append(go(TIER_LABELS[t], targets[t], copy.deepcopy(TIER_CAPTURES[t])))
    return out


def n_document_inventory(node_id, targets, lab_targets, note):
    return node(
        node_id, "document_inventory", 1, "Evidence in file",
        "What is in the file for this tumour?",
        "Pick the highest tier of evidence in the file. A radiology report counts as imaging. "
        "A pathology report on a biopsy or resection counts as histology. A biopsy or cytology "
        "report that calls the specimen inadequate or non-diagnostic counts as no tissue: pick "
        "from the other tiers.",
        gate_options(targets, lab_targets),
        EVIDENCE_TIER, note)


# The evidence a clerk has said is on file, per context. app.js capture() REPLACES
# evidence_tests, so a node reached with two different evidence sets cannot add a report with
# one static capture without erasing or inventing another. Each context therefore has its own
# node, built by the same function: evidence_tests on every path names exactly the reports the
# clerk said are on file, and never one the clerk said is absent.
CLINICAL_CONTEXTS = {
    "referral": {"suffix": "", "evidence": [], "imaging": "imaging",
                 "hint": "No imaging report, marker result or tissue report is in the file."},
    "cytology": {"suffix": "_cytology", "evidence": ["Cytology"], "imaging": "cytology",
                 "hint": "The cytology report is not diagnostic, and no imaging report, marker "
                         "result or histology report is in the file."},
}
IMAGING_CONTEXTS = {
    "imaging": {"suffix": "", "evidence": ["Imaging"],
                "question": "No tissue is in the file. What does the imaging report "
                            "conclude?"},
    "markers": {"suffix": "_markers", "evidence": ["Imaging", "Tumour markers"],
                "question": "No tissue is in the file, and the markers do not register the "
                            "tumour on their own. What does the imaging report conclude?"},
    "cytology": {"suffix": "_cytology", "evidence": ["Cytology", "Imaging"],
                 "question": "The cytology report is not diagnostic, and no histology report "
                             "is in the file. What does the imaging report conclude?"},
}


def clinical_node(site: str, ctx: str = "referral") -> str:
    return nid(site, "clinical_alias" + CLINICAL_CONTEXTS[ctx]["suffix"])


def imaging_node(site: str, ctx: str = "imaging") -> str:
    return nid(site, "imaging" + IMAGING_CONTEXTS[ctx]["suffix"])


def n_clinical_alias(site, ctx="referral"):
    c = CLINICAL_CONTEXTS[ctx]
    return node(
        clinical_node(site, ctx), "clinical_alias", 2 if ctx == "referral" else 3,
        "Referral wording",
        "What does the referral letter or clinical note say?",
        "%s A note alone never establishes a germ cell tumour's type." % c["hint"],
        [
            unspecified(site, "The note states a malignant tumour as the diagnosis, or as "
                              "probable", 1, "8000",
                        "A diagnosis resting on clinical information alone is registered "
                        "with the unspecified code (%s, rule 5)." % VISSER,
                        {"workup_status": "incomplete",
                         "basis_evidence_tier": "referral_malignant"},
                        after="Obtain the imaging, marker or pathology report and code "
                              "again."),
            nonrep("The note says only possible or suspected", NOT_REGISTRABLE_POSSIBLE,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "referral_nondiagnostic"}),
            go("An imaging report is in the file after all", imaging_node(site, c["imaging"]),
               {"evidence_tests": c["evidence"] + ["Imaging"], "workup_status": "incomplete",
                "basis_evidence_tier": "imaging"}),
        ],
        EVIDENCE_TIER,
        "Contract §4.2. Visser O, et al. Frontiers in Oncology 2023;13:1250549, rules 4 and 5, "
        "p. 03: 8000/3 at basis 1 when cancer is at least probable. 8000/3 is Group X only at "
        "the gonads (ICCC-2017 range 117); elsewhere the branch refers (D4). Evidence context "
        "%r: reached with evidence_tests %r." % (ctx, c["evidence"]))


def n_markers(site):
    opts = [
        code("Imaging shows a tumour and the report calls alpha-fetoprotein raised, with or "
             "without human chorionic gonadotropin, and the file calls it a germ cell tumour",
             "9065", "3", 4,
             "%s A germ cell tumour shown on imaging with a raised alpha-fetoprotein is "
             "registered to this code without tissue (%s, Table 4). The marker does not name "
             "the histological type; a histology report gives it." % (rec("9065", "3", 4),
                                                                     VISSER),
             {"workup_status": "incomplete", "basis_evidence_tier": "markers_afp"},
             note="D4. Visser Table 4, p. 06; rule 6, p. 05 (basis 4 needs a clinical "
                  "investigation showing the tumour). The pathway's 9071/3 for a raised "
                  "alpha-fetoprotein is not built: it records a histology no one saw."),
    ]
    if site == "extragonadal":
        opts.append(code(
            "Imaging shows a tumour of the uterus or placenta after a pregnancy, the report "
            "calls human chorionic gonadotropin raised, and the file calls it "
            "choriocarcinoma", "9100", "3", 4,
            "%s Choriocarcinoma of the placenta with a raised human chorionic gonadotropin is "
            "registered to this code without tissue (%s, Table 4)." % (rec("9100", "3", 4),
                                                                       VISSER),
            {"workup_status": "incomplete", "basis_evidence_tier": "markers_hcg_gestational"},
            note="D4, extragonadal tree only. Visser Table 4, p. 06, registers choriocarcinoma "
                 "of the placenta, so the label asks for that diagnosis: a hydatidiform mole "
                 "also raises human chorionic gonadotropin after a pregnancy."))
    opts += [
        code("Imaging shows a tumour and the report calls human chorionic gonadotropin raised; "
             "alpha-fetoprotein is normal or not measured; the file calls it a germ cell "
             "tumour", "9064", "3", 4,
             "%s ICD-O-3.2 files Germ cell tumor, NOS under this number, and a germ cell "
             "tumour with a raised human chorionic gonadotropin is registered to it without "
             "tissue (%s, Table 4). The record does not assert that a germinoma was diagnosed; "
             "a histology report gives the type." % (rec("9064", "3", 4), VISSER),
             {"workup_status": "incomplete", "basis_evidence_tier": "markers_hcg"},
             note="D2, D4. Visser Table 4, p. 06."),
        go("Imaging shows a tumour and a marker is raised, but the file does not call it a "
           "germ cell tumour or choriocarcinoma", imaging_node(site, "markers"),
           {"basis_evidence_tier": "markers_raised_no_diagnosis"},
           note="Visser Table 4 registers a marker code only for the diagnosis it names; "
                "without that diagnosis the imaging conclusion decides. evidence_tests stays "
                "Imaging and Tumour markers."),
        go("Neither marker is raised", imaging_node(site, "markers"),
           {"basis_evidence_tier": "markers_not_raised"},
           note="evidence_tests stays Imaging and Tumour markers."),
        nonrep("A marker is raised, but the imaging shows no tumour",
               "A raised tumour marker is not registered unless a clinical investigation shows "
               "the tumour (%s, rule 6)." % VISSER,
               {"workup_status": "not registrable",
                "basis_evidence_tier": "markers_no_tumour"}),
    ]
    return node(
        nid(site, "markers"), "morphology_only", 2, "Tumour markers",
        "No tissue is in the file. What do the imaging report and the marker results show?",
        "Use the report's own words. The value must be called raised against the laboratory's "
        "range for the patient's age; a newborn's alpha-fetoprotein is high without a tumour. "
        "Each coded option also needs the diagnosis it names (%s, Table 4)." % VISSER,
        opts, EVIDENCE_TIER,
        ("D4. The report's own statement against the age-specific range is read. In the brain "
         "tree this is the fallback of the marker gates (cn_marker_age onward): reached when "
         "the patient is under 24 months or the age is not in the file, when a value the "
         "decision needs is not entered, and from non-diagnostic cytology, whose values were "
         "typed on cn_labs_cytology and stay out of reach of a gate (app.js keeps lab values "
         "out of state.captured). " if site == "cns" else
         "D4. The report's own statement against the age-specific range is read; nothing is "
         "re-gated numerically. ") +
        "Visser Table 4 registers a tumour the file calls a germ cell tumour (9064/3, 9065/3) "
        "or choriocarcinoma (9100/3); each coded label states that condition.")


# ------------------------------------------------------------------------------------------
# Brain marker gates — the numbers decide "raised" (registrar's ruling, 6 October 2026)
# ------------------------------------------------------------------------------------------
# SIOP cut-offs, the same in serum and in cerebrospinal fluid, "above" being strict:
#   SIOP CNS GCT 96: alpha-fetoprotein > 25 ng/mL or beta human chorionic gonadotropin
#     > 50 IU/L in serum or cerebrospinal fluid diagnoses a malignant non-germinomatous germ
#     cell tumour without biopsy (Calaminus G, et al. Neuro Oncol 2017;19:1661-1672, Methods).
#   SIOP CNS GCT II: germinoma requires alpha-fetoprotein < 25 ng/mL and beta human chorionic
#     gonadotropin < 50 IU/L in serum and cerebrospinal fluid (Calaminus G, et al. Neuro Oncol
#     2026;28:2234-2247, Table 2 and Results).
# docs/group_10_lab_marker_evidence.md §1 holds both, with the COG and Hu cut-offs not used.
#
# Age. Serum alpha-fetoprotein is high in infancy without a tumour. The first age at which
# every published upper reference limit for term infants is at or below 25 ng/mL is 2 years:
# La'ulu 2011, 12 ng/mL (Beckman Access) and 15 ng/mL (Roche E170). Below it the limits run
# above 25: > 8 months 27 ng/mL (Lahdenne 1991), 1 year girls 41 and 38 ng/mL (La'ulu 2011),
# day 180 to day 720 up to 87 ng/mL (Blohm 1998); all from Ferraro 2019, Table 3, aop
# pp. 8-9. So the gates read a number from 24 completed months. Below that, or with no age in
# the file, the case goes to the laboratory screen and the report's own reading
# (cn_markers), as before this ruling: a 9065/9064 split needs the alpha-fetoprotein reading,
# so a beta human chorionic gonadotropin number alone cannot decide in an infant either.
# Cerebrospinal fluid alpha-fetoprotein: Coakley 2005 (abstract only) gives a 95th centile of
# 12.5 kIU/L (about 15 ng/mL at Calaminus 2026's 25 ng/mL = 20.8 kU/L) from a CORRECTED age of
# 32 days, and all values under 3 kIU/L over 2 months. The tool asks chronological age and no
# prematurity, so no separate cerebrospinal fluid boundary is built; the registrar is asked
# (docs/group_10_registrar_review.md).
#
# Each number is typed once. The gates replace cn_labs_markers on the marker tier from 24
# months; under 24 months the gates are never asked and the laboratory screen records the
# values. A gate asks only what can still change the code (Group III's md_gct_* pattern), so a
# value after the deciding one is not asked. A raised value in either compartment decides;
# "not raised" needs both compartments entered and at or below the cut-off; a value not
# entered (not in the file, or in a unit the tool does not convert) never counts as normal and
# sends the case to cn_markers. The units are ng/mL and IU/L, SIOP's. The evidence file's
# Units paragraph equates ng/mL with µg/L and IU/L with mIU/mL. Calaminus 2026 gives 25 ng/mL
# = 20.8 kU/L for alpha-fetoprotein; no unit choice is built on a gate, so a value in kU/L or
# IU/mL is left empty and goes to the report question.
BRAIN_AGE_MONTHS = 24
BRAIN_AFP_CUTOFF = 25   # ng/mL, serum and cerebrospinal fluid
BRAIN_HCG_CUTOFF = 50   # IU/L, serum and cerebrospinal fluid
SIOP_CITE = "Calaminus 2017, Methods; Calaminus 2026, Table 2"
BRAIN_MARKERS = {
    "afp": {"name": "alpha-fetoprotein", "cut": BRAIN_AFP_CUTOFF, "unit": "ng_per_ml",
            "unit_text": "ng/mL", "same": "A value in µg/L is the same number in ng/mL.",
            "other": "kU/L or IU/mL"},
    "hcg": {"name": "beta human chorionic gonadotropin (β-hCG)", "cut": BRAIN_HCG_CUTOFF,
            "unit": "iu_per_l", "unit_text": "IU/L",
            "same": "A value in mIU/mL is the same number in IU/L.", "other": "another unit"},
}
COMPARTMENTS = {"serum": "Serum", "csf": "Cerebrospinal fluid"}


def brain_gate_nos():
    """numeric_gate is a refining type, so it carries a nos_fallback (DT master §3D): the
    clerk's "Uncertain subtype - still a malignancy" escape. On this tissue-free route Group X
    rule 2 admits only a Visser Table 4 code at basis 4, and 9064/3, which ICD-O-3.2 files Germ
    cell tumor, NOS under, is the one that names no type (as cn_ihc's fallback). app.js
    escape-nos asserts no basis of its own; the basis here is for the validator's rule 2."""
    return {"code": "9064", "behavior_code": "3", "name": "Germ cell tumor, NOS",
            "basis_of_diagnosis": 4,
            "reason": "The marker values do not settle the germ cell tumour's type. %s "
                      "ICD-O-3.2 files Germ cell tumor, NOS under this number, so the record "
                      "does not assert that a germinoma was diagnosed; a histology report gives "
                      "the type." % rec("9064", "3", 4)}


def brain_gate(node_id, marker, compartment, raised, not_raised, not_entered,
               not_raised_captures=None, note=""):
    """One SIOP gate: above the cut-off -> raised; at or below -> not_raised; no value ->
    not_entered. The variable names match Group III's md_gct_* gates."""
    m = BRAIN_MARKERS[marker]
    var = "%s_%s_%s" % (marker, compartment, "ng_ml" if marker == "afp" else "iu_l")
    label = "%s %s" % (COMPARTMENTS[compartment], m["name"])
    low = {"range": "<=%d" % m["cut"], "unit": m["unit"], "next_node": not_raised}
    if not_raised_captures:
        low["captures"] = not_raised_captures
    return node(
        node_id, "numeric_gate", 2, label[0].upper() + label[1:],
        "%s, as the report gives it, in %s." % (label, m["unit_text"]),
        "A value above %d %s counts as raised, the SIOP cut-off for serum and cerebrospinal "
        "fluid alike (%s). %s If the report gives %s, leave the number empty: the tool does "
        "not convert units, and a value not entered is never read as normal."
        % (m["cut"], m["unit_text"], SIOP_CITE, m["same"], m["other"]),
        None, [var],
        "Registrar's ruling, 6 October 2026: SIOP cut-off, strict 'above' (SIOP CNS GCT 96 "
        "'> %d'; SIOP CNS GCT II requires '< %d' for germinoma). %s"
        % (m["cut"], m["cut"], note),
        variable=var, variable_label=label, unit=m["unit"],
        # A reading no band takes (none should exist) goes to the report question, never
        # throws: app.js fallbackTarget() reads insufficient_next_node first.
        insufficient_next_node=nid("cns", "markers"), nos_fallback=brain_gate_nos(),
        bands=[{"range": ">%d" % m["cut"], "unit": m["unit"], "next_node": raised},
               low,
               {"range": "not_documented", "unit": m["unit"], "next_node": not_entered}])


def n_brain_age():
    return node(
        "cn_marker_age", "numeric_gate", 2, "Age",
        "How old was the patient at diagnosis, in completed months?",
        "Alpha-fetoprotein is high in infancy without a tumour. Published normal values for "
        "serum alpha-fetoprotein fall to %d ng/mL or below by %d months (Ferraro 2019, Table "
        "3). From %d months the marker values decide; under %d months, or with no age in the "
        "file, the report's own reading decides."
        % (BRAIN_AFP_CUTOFF, BRAIN_AGE_MONTHS, BRAIN_AGE_MONTHS, BRAIN_AGE_MONTHS),
        None, ["patient_age_months"],
        "Registrar's ruling, 6 October 2026. The %d-month boundary and its sources are in the "
        "comment above BRAIN_AGE_MONTHS. Under it, and with no age, the case takes the "
        "laboratory screen and cn_markers, the route every brain marker case took before the "
        "ruling." % BRAIN_AGE_MONTHS,
        variable="patient_age_months", variable_label="Age at diagnosis", unit="months",
        insufficient_next_node=lab_node_id("cns", "markers"), nos_fallback=brain_gate_nos(),
        bands=[{"range": "<%d" % BRAIN_AGE_MONTHS, "next_node": lab_node_id("cns", "markers")},
               {"range": ">=%d" % BRAIN_AGE_MONTHS, "next_node": "cn_afp_serum"},
               {"range": "not_documented", "next_node": lab_node_id("cns", "markers")}])


def n_brain_raised(marker):
    """The marker route's own outcomes once the numbers say which marker is raised: the coded
    option, the option for a file that does not name a germ cell tumour, and the one for
    imaging that shows no tumour (n_markers' last three, unchanged)."""
    site = "cns"
    if marker == "afp":
        node_id, morph, tier = "cn_afp_raised", "9065", "markers_afp"
        question = ("Alpha-fetoprotein is above %d ng/mL. What do the imaging report and the "
                    "file show?" % BRAIN_AFP_CUTOFF)
        reason = ("%s A germ cell tumour shown on imaging with alpha-fetoprotein above "
                  "%d ng/mL, the SIOP cut-off (%s), is registered to this code without tissue "
                  "(%s, Table 4). The marker does not name the histological type; a histology "
                  "report gives it." % (rec("9065", "3", 4), BRAIN_AFP_CUTOFF, SIOP_CITE,
                                        VISSER))
        note = ("D4 and the registrar's ruling of 6 October 2026. Same code, basis and "
                "captures as cn_markers' alpha-fetoprotein option. The Diagnostic Pathway's "
                "§2C '9071' for a raised alpha-fetoprotein stays unbuilt (ruling 3, same day).")
    else:
        node_id, morph, tier = "cn_hcg_raised", "9064", "markers_hcg"
        question = ("Beta human chorionic gonadotropin (β-hCG) is above %d IU/L, and "
                    "alpha-fetoprotein is %d ng/mL or below in serum and in cerebrospinal "
                    "fluid. What do the imaging report and the file show?"
                    % (BRAIN_HCG_CUTOFF, BRAIN_AFP_CUTOFF))
        reason = ("%s ICD-O-3.2 files Germ cell tumor, NOS under this number, and a germ cell "
                  "tumour with a raised human chorionic gonadotropin is registered to it "
                  "without tissue (%s, Table 4). The record does not assert that a germinoma "
                  "was diagnosed; a histology report gives the type." % (rec("9064", "3", 4),
                                                                        VISSER))
        note = ("D2, D4. Same code, basis and captures as cn_markers' human chorionic "
                "gonadotropin option. SIOP CNS GCT 96 reads beta human chorionic gonadotropin "
                "> 50 IU/L as a secreting, malignant non-germinomatous tumour (Calaminus 2017, "
                "Methods), which ICD-O-3.2 holds as 9065/3; the tree keeps Visser Table 4's "
                "9064/3 and the registrar decides (docs/group_10_registrar_review.md).")
    return node(
        node_id, "morphology_only", 2, "Tumour markers", question,
        "Each coded option also needs the diagnosis it names (%s, Table 4)." % VISSER,
        [
            code("Imaging shows a tumour, and the file calls it a germ cell tumour", morph, "3",
                 4, reason, {"workup_status": "incomplete", "basis_evidence_tier": tier},
                 note=note),
            go("Imaging shows a tumour, but the file does not call it a germ cell tumour",
               imaging_node(site, "markers"),
               {"basis_evidence_tier": "markers_raised_no_diagnosis"},
               note="As cn_markers: without the diagnosis the imaging conclusion decides."),
            nonrep("The imaging shows no tumour",
                   "A raised tumour marker is not registered unless a clinical investigation "
                   "shows the tumour (%s, rule 6)." % VISSER,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "markers_no_tumour"}),
        ],
        EVIDENCE_TIER,
        "Registrar's ruling, 6 October 2026: reached only when the numbers decide. The options "
        "are cn_markers' own, less the marker reading the gates have made.")


def brain_marker_nodes():
    """The age gate, six marker gates and two outcome nodes of the brain marker tier, in the
    order a case meets them. Each gate's arguments are raised, not raised, not entered."""
    fallback, neither = nid("cns", "markers"), imaging_node("cns", "markers")
    return [
        n_brain_age(),
        brain_gate("cn_afp_serum", "afp", "serum", "cn_afp_raised", "cn_afp_csf",
                   "cn_afp_csf_no_serum"),
        brain_gate("cn_afp_csf", "afp", "csf", "cn_afp_raised", "cn_hcg_serum", fallback,
                   note="Serum is at or below the cut-off; not raised needs both."),
        brain_gate("cn_afp_csf_no_serum", "afp", "csf", "cn_afp_raised", fallback, fallback,
                   note="No serum value: only a raised value here decides."),
        brain_gate("cn_hcg_serum", "hcg", "serum", "cn_hcg_raised", "cn_hcg_csf",
                   "cn_hcg_csf_no_serum",
                   note="Alpha-fetoprotein is at or below the cut-off in both compartments."),
        brain_gate("cn_hcg_csf", "hcg", "csf", "cn_hcg_raised", neither, fallback,
                   not_raised_captures={"basis_evidence_tier": "markers_not_raised"},
                   note="All four values at or below the cut-offs: neither marker is raised, "
                        "as cn_markers' 'Neither marker is raised' option."),
        brain_gate("cn_hcg_csf_no_serum", "hcg", "csf", "cn_hcg_raised", fallback, fallback,
                   note="No serum value: only a raised value here decides."),
        n_brain_raised("afp"),
        n_brain_raised("hcg"),
    ]


def n_imaging(site, ctx="imaging"):
    c = IMAGING_CONTEXTS[ctx]
    return node(
        imaging_node(site, ctx), "morphology_only", 2 if ctx == "imaging" else 3,
        "Imaging conclusion", c["question"],
        "Answer from the radiologist's own conclusion. Imaging alone never establishes a germ "
        "cell tumour's type.",
        [
            unspecified(site, "Imaging shows a malignant tumour, at least probable", 2, "8000",
                        "Imaging alone does not establish a germ cell tumour (%s, rule 5)."
                        % VISSER,
                        {"workup_status": "incomplete",
                         "basis_evidence_tier": "imaging_malignant"},
                        after="A histology report gives the specific code."),
            nonrep("Imaging calls it possible only, or describes a benign lesion",
                   NOT_REGISTRABLE_POSSIBLE,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "imaging_nondiagnostic"}),
            go("A histology report is in the file", nid(site, "histology"),
               {"evidence_tests": c["evidence"] + ["Histology"], "workup_status": "incomplete",
                "basis_evidence_tier": "histology"}),
        ],
        EVIDENCE_TIER,
        "D4. Visser 2023 has no germ cell row in Table 3, so imaging alone is 8000/3 at basis 2 "
        "(rule 5, p. 03); in the central nervous system and at extragonadal sites that code is "
        "not Group X and the branch refers. Evidence context %r: every path into this node "
        "already names Imaging, so the code branch captures no evidence_tests." % ctx)


def n_cytology(site):
    fam = SITES[site]["family"]
    opts = [code("Cytology names %s" % SITES[site]["family_term"], fam, "3", 5,
                 "%s Cytology does not give a histological subtype; a histology report "
                 "confirms it." % rec(fam, "3", 5),
                 {"workup_status": "incomplete", "basis_evidence_tier": "cytology_named"},
                 note="D3: the site's own term for the germinoma family.")]
    if site in GONADS:
        opts.append(code("Cytology names germinoma", "9064", "3", 5,
                         "%s A report that uses the term germinoma is coded as written."
                         % rec("9064", "3", 5),
                         {"workup_status": "incomplete",
                          "basis_evidence_tier": "cytology_named"},
                         note="D1, settled: germinoma at any site is 9064/3. The contract's "
                              "single 'germinoma or the site's term' option is split so the "
                              "site's family code (D3) is not given to a report that says "
                              "germinoma."))
    if site == "extragonadal":
        opts.append(code("Cytology names seminoma", "9061", "3", 5,
                         "%s A report that uses the term seminoma is coded as written."
                         % rec("9061", "3", 5),
                         {"workup_status": "incomplete",
                          "basis_evidence_tier": "cytology_named"},
                         note="D3: the extragonadal tree offers germinoma and seminoma as the "
                              "report writes them, as its histology node does."))
    opts += [
        code(label, morph, "3", 5,
             "%s Cytology does not give a histological subtype; a histology report confirms "
             "it." % rec(morph, "3", 5),
             {"workup_status": "incomplete", "basis_evidence_tier": "cytology_named"},
             note="Coded as the report names it, as the histology node does.")
        for label, morph in (
            ("Cytology names a yolk sac tumour", "9071"),
            ("Cytology names embryonal carcinoma", "9070"),
            ("Cytology names choriocarcinoma", "9100"),
            ("Cytology names a non-seminomatous or non-germinomatous germ cell tumour without "
             "naming its type", "9065"))
    ] + [
        code("Cytology names a malignant germ cell tumour without naming its type", "9064",
             "3", 5,
             "%s ICD-O-3.2 files Germ cell tumor, NOS under this number, so the record does "
             "not assert that a germinoma was diagnosed." % rec("9064", "3", 5),
             {"workup_status": "incomplete", "basis_evidence_tier": "cytology_gct"},
             note="D2."),
        unspecified(site, "Malignant cells are present, with no tumour type named", 5, "8001",
                    "Cytology establishes malignant cells but no tumour type.",
                    {"workup_status": "incomplete",
                     "basis_evidence_tier": "cytology_malignant"}),
        go("No malignant cells, scant material, or a non-diagnostic report — and an imaging "
           "report and an alpha-fetoprotein or human chorionic gonadotropin result are in the "
           "file", nid(site, "markers"),
           {"evidence_tests": ["Cytology", "Imaging", "Tumour markers"],
            "workup_status": "incomplete", "basis_evidence_tier": "cytology_nondiagnostic"},
           note="Non-diagnostic cytology leaves the marker route (Visser Table 4) as the best "
                "evidence."),
        go("No malignant cells, scant material, or a non-diagnostic report — and an imaging "
           "report, with no marker result, is in the file", imaging_node(site, "cytology"),
           {"evidence_tests": ["Cytology", "Imaging"], "workup_status": "incomplete",
            "basis_evidence_tier": "cytology_nondiagnostic"},
           note="Non-diagnostic cytology leaves imaging as the best evidence."),
        go("No malignant cells, scant material, or a non-diagnostic report — and no imaging "
           "report is in the file", clinical_node(site, "cytology"),
           {"evidence_tests": ["Cytology"], "workup_status": "incomplete",
            "basis_evidence_tier": "cytology_nondiagnostic"},
           note="Non-diagnostic cytology and no imaging leave the note as the best evidence. "
                "Group 8's bn_cytology sends this case to its imaging node, whose 'no imaging "
                "report' option captures Referral only and so erases Cytology; this split "
                "keeps it."),
    ]
    return node(
        nid(site, "cytology"), "morphology_only", 2, "Cytology",
        "What does the cytology report conclude?",
        "Cytology of %s. Cytology gives basis of diagnosis 5; a histology report gives the "
        "specific code." % SITES[site]["fluid"],
        opts, EVIDENCE_TIER,
        "Basis 5 for cytology: Visser 2023 Table 1, p. 03. Family code per D3; 9064/3 for an "
        "untyped germ cell tumour per D2.")


# ------------------------------------------------------------------------------------------
# Mixed tumours (D6) and the immunohistochemistry checklist (§4.2)
# ------------------------------------------------------------------------------------------
def n_mixed(site):
    """The named-term question. A term the report itself uses wins over its components
    (registrar's rule), so it is asked first, as a plain choice. A first_match tick list cannot
    hold it: there every option carries `ticks` and the engine draws no option without them
    (app.js tickControl(), check_tick_lists), so the components go on their own screen."""
    opts = [
        code("Teratocarcinoma", "9081", "3", 7, rec("9081")),
        code("Malignant teratoma, undifferentiated or anaplastic", "9082", "3", 7, rec("9082")),
        code("Malignant teratoma, intermediate", "9083", "3", 7,
             rec("9083")),
    ]
    if site in GONADS:
        opts.append(code("Malignant teratoma, trophoblastic", "9102", "3", 7, rec("9102"),
                         note="D6. ICCC-2017 range 110 (Xc5) only: ovary and testis."))
    if site == "extragonadal":
        opts.append(code("Germ cell tumour with a haematological malignancy", "9086", "3", 7,
                         "%s The associated haematological malignancy is coded separately, "
                         "from its own group's tree." % rec("9086"),
                         note="D17. New in ICD-O-3.2; ICCC-2017 range 105 (Xb6) only."))
    opts.append(go("None of these: the report lists the components",
                   nid(site, "mixed_components")))
    return node(
        nid(site, "mixed"), "histology_subclassification", 3, "Mixed germ cell tumour",
        "Does the report call the tumour by one of these names?",
        "Choose a name only where the report itself uses it. Otherwise choose the last option "
        "and tick the components on the next screen.",
        opts, [],
        "D6. WHO 2022 (Moch 2022, Table 3, p. 464) codes every mixture 9085/3; ICD-O-3.2 keeps "
        "the specific terms, coded as written (Group 8 D8 precedent). 9102/3 is ovary and "
        "testis only (range 110); 9086/3 extragonadal only (range 105). The named terms are "
        "asked before the component checklist (registrar, 6 October 2026: the report's own "
        "term wins).")


# The components a report lists, in the report vocabulary of the EAFYA document review §7.2.
# "Another germ cell component" holds polyembryoma and any other component the list does not
# name, so "Embryonal carcinoma and teratoma only" can exclude a third component of any kind.
MIXED_ITEMS = (
    {"id": "choriocarcinoma", "label": "Choriocarcinoma"},
    {"id": "embryonal_carcinoma", "label": "Embryonal carcinoma"},
    {"id": "yolk_sac_tumour", "label": "Yolk sac tumour (endodermal sinus tumour)"},
    {"id": "teratoma", "label": "Teratoma, mature or immature"},
    {"id": "seminoma", "label": "Seminoma, germinoma or dysgerminoma"},
    {"id": "other_component", "label": "Another germ cell component, such as polyembryoma"},
)
MIXED_IDS = tuple(i["id"] for i in MIXED_ITEMS)


def n_mixed_components(site):
    """The component checklist (tick_list, resolve first_match; registrar, 6 October 2026). The
    first option in file order whose rule fits the ticked set is the destination:
      choriocarcinoma among the components            -> 9101/3
      embryonal carcinoma and teratoma, nothing else  -> 9081/3
      teratoma and the germinoma family               -> 9085/3
      anything else, or nothing ticked                -> 9085/3
    The codes, labels and reasons are those of the single-choice list this replaces; the old
    hint's reading order ("the first option that fits, reading from the top") is now the
    engine's."""
    def with_ticks(branch, ticks):
        branch["ticks"] = ticks
        return branch
    opts = [
        with_ticks(code("Choriocarcinoma", "9101", "3", 7, rec("9101")),
                   {"requires": ["choriocarcinoma"]}),
        with_ticks(code("Embryonal carcinoma and teratoma only", "9081", "3", 7,
                        "%s ICD-O-3.2 gives it the synonym Mixed embryonal carcinoma and "
                        "teratoma." % rec("9081")),
                   {"requires": ["embryonal_carcinoma", "teratoma"],
                    "excludes": [i for i in MIXED_IDS
                                 if i not in ("embryonal_carcinoma", "teratoma")]}),
        with_ticks(code("Teratoma and seminoma, germinoma or dysgerminoma", "9085", "3", 7,
                        "%s ICD-O-3.2 gives it the related term Mixed teratoma and seminoma."
                        % rec("9085")),
                   {"requires": ["teratoma", "seminoma"]}),
        with_ticks(code("Other combination, or none listed", "9085", "3", 7, rec("9085")), {}),
    ]
    return node(
        nid(site, "mixed_components"), "histology_subclassification", 4,
        "Mixed germ cell tumour",
        "Which components does the report list?",
        "The code follows from the components ticked. A component the list does not name goes "
        "under 'Another germ cell component'.",
        opts, [],
        "D6, registrar 6 October 2026. Rules: choriocarcinoma among the components -> 9101/3; "
        "exactly embryonal carcinoma and teratoma -> 9081/3; anything else -> 9085/3. The data "
        "gate enumerates all 64 ticked sets: none is stranded and every option is the first fit "
        "for at least one.",
        tick_list={"resolve": "first_match", "variable": "mixed_components",
                   "label": "Components", "prompt": "Tick every component the report lists.",
                   "items": [dict(i) for i in MIXED_ITEMS]})


IHC_MARKER_GROUPS = [
    {"group_label": "Germ cell lineage", "markers": ["SALL4", "OCT3/4"]},
    {"group_label": "Seminoma, dysgerminoma and germinoma",
     "markers": ["CD117", "SOX17", "D2-40"]},
    {"group_label": "Embryonal carcinoma", "markers": ["CD30", "SOX2"]},
    {"group_label": "Yolk sac tumour",
     "markers": ["Glypican-3", "Alpha-fetoprotein (tissue stain)", "HNF1-beta (nuclear)"]},
]


def n_ihc(site):
    fam = SITES[site]["family"]
    fam_reason = ("Dysgerminoma, seminoma and germinoma are one tumour under three names (Moch "
                  "2022, p. 464), and the name this site uses is recorded. %s" % rec(fam))
    rules = [
        code(["OCT3/4", "SOX2"], "9070", "3", 7,
             "OCT3/4 and SOX2 are positive and SOX17 is not: the embryonal carcinoma pattern "
             "(%s, p. 37). %s" % (SIEGMUND, rec("9070")),
             satisfies=["IHC"], key="positive", negative=["SOX17"],
             note="Rule 2. Siegmund 2023 p. 37 (Nonaka): diffuse SOX2 with negative SOX17 in "
                  "100% of embryonal carcinomas; diffuse SOX17 with negative SOX2 in 100% of "
                  "seminomas. SOX2 in teratoma epithelium (up to 81%) is excluded by OCT3/4, "
                  "which teratoma lacks (Table 1, p. 34). Listed first: it emits rule 1's "
                  "code, and above rule 0 it keeps SOX2 asked before rule 0 can settle."),
        code(["OCT3/4", "CD30", "CD117"], "9064", "3", 7,
             "OCT3/4, CD30 and CD117 are all positive, and SOX2 and SOX17 are not: the panel "
             "matches neither the embryonal carcinoma pattern (CD30 without CD117) nor the "
             "seminoma pattern (CD117 without CD30) (%s, p. 37), so it does not establish the "
             "germ cell tumour's type. Recorded as Germinoma (9064/3): ICD-O-3.2 files Germ "
             "cell tumor, NOS under this number, so the record does not assert that a "
             "germinoma was diagnosed." % SIEGMUND,
             satisfies=["IHC"], key="positive", negative=["SOX2", "SOX17"],
             note="Rule 0, after rule 2 and ahead of rule 1, so the flow asks CD117 before "
                  "rule 1 can settle and SOX2 before rule 0 can. The engine counts an unasked "
                  "negative marker as off and stops at the first satisfied rule, asking only "
                  "about rules above it, so without this rule a seminoma with focal CD30 and "
                  "a positive CD117 the clerk was never asked about was coded 9070/3. It "
                  "records what the node's fallback records for the same panel; SOX2 and "
                  "SOX17 negative keep rules 2 and 4 deciding when either is positive. "
                  "Siegmund 2023 p. 37: CD30+/KIT- is 100% specific for "
                  "embryonal carcinoma and CD30-/KIT+ for seminoma (Leroy)."),
        code(["OCT3/4", "CD30"], "9070", "3", 7,
             "OCT3/4 and CD30 are positive, and the seminoma markers CD117 and SOX17 are not: "
             "the embryonal carcinoma pattern (%s, p. 37). %s" % (SIEGMUND, rec("9070")),
             satisfies=["IHC"], key="positive", negative=["CD117", "SOX17"],
             note="Rule 1. Siegmund 2023 p. 37: CD30 stains embryonal carcinoma (83-100%) and "
                  "focally stains 0-50% of seminomas; CD30+/KIT- is 100% specific for "
                  "embryonal carcinoma (Leroy). OCT3/4 marks seminoma and embryonal carcinoma "
                  "(100% each, p. 37). negative CD117 and SOX17: added to the contract's rule, "
                  "so a seminoma with focal CD30 is not coded embryonal carcinoma. SOX17 is "
                  "negative in 100% of embryonal carcinomas (Nonaka, p. 37)."),
        code(["OCT3/4", "CD117"], fam, "3", 7,
             "OCT3/4 and CD117 are positive and CD30 is not: the seminoma pattern (%s, pp. "
             "36-37). %s" % (SIEGMUND, fam_reason),
             satisfies=["IHC"], key="positive", negative=["CD30"],
             note="Rule 3. Siegmund 2023 p. 36: KIT stains 88-100% of seminomas; focal "
                  "cytoplasmic KIT occurs in 32-44% of non-seminomatous tumours. p. 37: "
                  "CD30-/KIT+ is 100% specific for seminoma (Leroy). negative CD30: added to "
                  "the contract's rule for the same reason as rule 1. Family code by site, D3."),
        code(["OCT3/4", "SOX17"], fam, "3", 7,
             "OCT3/4 and SOX17 are positive: the seminoma pattern. Embryonal carcinoma does "
             "not express SOX17 (%s, p. 37). %s" % (SIEGMUND, fam_reason),
             satisfies=["IHC"], key="positive",
             note="Rule 4. Siegmund 2023 p. 37 (Nonaka): SOX17 diffuse in 100% of seminomas, "
                  "negative in 100% of embryonal carcinomas and in choriocarcinoma; variable "
                  "in yolk sac tumour and teratoma, both OCT3/4 negative (Table 1, p. 34). No "
                  "CD30 negative: a panel with OCT3/4, SOX17 and CD30 positive fires this rule "
                  "(rule 1 requires SOX17 not positive), because SOX17 is negative in every "
                  "embryonal carcinoma and CD30 focally stains up to half of seminomas "
                  "(p. 37)."),
        code(["OCT3/4", "D2-40"], fam, "3", 7,
             "OCT3/4 and D2-40 are positive and CD30 is not: the seminoma pattern (%s, pp. "
             "36-37). %s" % (SIEGMUND, fam_reason),
             satisfies=["IHC"], key="positive", negative=["CD30"],
             note="Rule 5. Siegmund 2023 p. 36: D2-40 strongly stains up to 100% of seminomas; "
                  "embryonal carcinoma stains in 0-69%, focally. negative CD30: added to the "
                  "contract's rule, so focal D2-40 in an embryonal carcinoma does not read as "
                  "seminoma. p. 37: KIT/D2-40/SOX17 mark seminoma, CD30/SOX2 embryonal "
                  "carcinoma."),
        code(["Glypican-3", "Alpha-fetoprotein (tissue stain)"], "9071", "3", 7,
             "Glypican-3 and alpha-fetoprotein both stain the tumour and OCT3/4 is not "
             "positive: the yolk sac tumour pattern (%s, p. 38; Wu 2020, Tables 1-2). %s"
             % (SIEGMUND, rec("9071")),
             satisfies=["IHC"], key="positive", negative=["OCT3/4"],
             note="Rule 6. Siegmund 2023 p. 38: glypican-3 in 100% of yolk sac tumours and "
                  "tissue alpha-fetoprotein in 55-100%; a subset of yolk sac tumours "
                  "co-expresses alpha-fetoprotein and glypican-3 (Nogales). Choriocarcinoma, "
                  "glypican-3 positive in 33-100%, is rarely alpha-fetoprotein positive (p. 38; "
                  "Table 1, p. 34). Wu P, et al. Pediatr Surg Int 2020 "
                  "(doi:10.1007/s00383-020-04652-w; the PDF prints no page numbers), Tables "
                  "1-2: alpha-fetoprotein 21/22 and glypican-3 22/22 paediatric yolk sac "
                  "tumours. OCT3/4 negative in yolk sac tumour, Table 1, p. 34."),
        code(["Glypican-3", "HNF1-beta (nuclear)"], "9071", "3", 7,
             "Glypican-3 and nuclear HNF1-beta are positive and OCT3/4 is not: the yolk sac "
             "tumour pattern (Rougemont 2018, Table 2, p. 29). %s" % rec("9071"),
             satisfies=["IHC"], key="positive", negative=["OCT3/4"],
             note="Rule 7. Rougemont AL, Tille JC. Human Pathology 2018;81:26-36: Table 2, "
                  "p. 29, glypican-3 positive in 42 of the 44 nuclear HNF1-beta positive yolk "
                  "sac components it lists; p. 34, glypican-3 positive in 43/45; p. 35, "
                  "recommends a panel combining SALL4, HNF1-beta, glypican-3 and OCT4. "
                  "Choriocarcinoma shows cytoplasmic HNF1-beta only, never nuclear (p. 26; "
                  "Table 5, p. 33), so the nuclear stain excludes it. p. 31: every yolk sac "
                  "tumour SALL4 positive and OCT4 negative."),
    ]
    return node(
        nid(site, "ihc"), "ihc_checklist", 4, "Germ cell stain panel",
        "Answer each stain as the report states it.",
        "The report calls the tumour a germ cell tumour without naming its type. Answer 'Not "
        "done or not readable' for a stain the report does not mention. A tumour with more than "
        "one germ cell component is coded at the mixed germ cell tumour step instead. One yolk "
        "sac marker alone does not establish a yolk sac tumour: glypican-3, alpha-fetoprotein "
        "and HNF1-beta each stain some teratomas (%s, p. 38; Rougemont 2018, p. 26). Human "
        "chorionic gonadotropin staining does not establish choriocarcinoma: it also stains the "
        "syncytiotrophoblastic cells found in seminoma (%s, p. 38)." % (SIEGMUND, SIEGMUND),
        None, [],
        "Contract §4.2, each rule verified against the printed page. Siegmund SE, Mehra R, "
        "Acosta AM. Human Pathology 2023;133:32-55 (online 2022): Table 1, p. 34; KIT and "
        "D2-40, p. 36; CD30, OCT3/4, SOX2 and SOX17, p. 37; glypican-3, alpha-fetoprotein, "
        "human chorionic gonadotropin and HNF1-beta, p. 38. Wu 2020, Tables 1-2. Rougemont "
        "2018, pp. 26, 29, 31, 33-35. Contract rules 1-5 are kept; rules 1, 3 and 5 carry "
        "negatives the contract's table did not, so a seminoma with focal CD30, or an "
        "embryonal carcinoma with CD117 or D2-40, does not take the other's code. With "
        "OCT3/4 positive, a positive SOX17 decides the panel for the germinoma family "
        "whatever CD30 or SOX2 show (rule 4; a panel with OCT3/4, SOX17 and CD30 fires it), "
        "because SOX17 is negative in every embryonal carcinoma (Siegmund p. 37). Without "
        "SOX17, a panel positive for CD30 and for CD117 or D2-40 is coded 9064/3 unless SOX2 "
        "settles it (rule 2): rule 0 records it for CD117, the fallback for D2-40. "
        "Contract rules 6-8 (one yolk sac marker each) are replaced by two pairs, OCT3/4 not "
        "positive in each: glypican-3 with alpha-fetoprotein, and glypican-3 with nuclear "
        "HNF1-beta. A single yolk sac marker falls to the fallback. The pair "
        "alpha-fetoprotein with HNF1-beta is not built: no source on disk reports the two "
        "stains on the same tumours (Rougemont did not stain alpha-fetoprotein, p. 28; "
        "Siegmund p. 38 compares their accuracy, not their co-expression). "
        "Residual risk, teratoma: glypican-3 stains 20-38% and tissue alpha-fetoprotein 0-27% "
        "of teratomas (Siegmund p. 38); nuclear HNF1-beta stains enteric-type teratoma glands "
        "in 11/16 (Rougemont p. 26; Table 5, p. 33); Wu Tables 1-2 found glypican-3 in 1/10 "
        "and alpha-fetoprotein in 2/10 mature teratomas, weak and in 2-3% of cells. No source "
        "reports how often a teratoma expresses both markers of a pair; one that does is "
        "coded 9071/3. Residual risk, choriocarcinoma: OCT3/4 negative and glypican-3 positive "
        "in 33-100% (Table 1, p. 34; p. 38); each pair needs a second marker the sources "
        "report choriocarcinoma rarely or never shows (alpha-fetoprotein, p. 38; nuclear "
        "HNF1-beta, Rougemont p. 26). "
        "SALL4 is declared and asked by no rule: it marks germ cell lineage, not type "
        "(Siegmund p. 36). Choriocarcinoma is not coded from immunohistochemistry (contract "
        "§4.2). Fallback 9064/3 per D2.",
        marker_groups=copy.deepcopy(IHC_MARKER_GROUPS),
        resolution_logic=rules,
        nos_fallback={
            "code": "9064", "behavior_code": "3", "name": "Germ cell tumor, NOS",
            "reason": "The stains do not establish the germ cell tumour's type. Recorded as "
                      "Germinoma (9064/3): ICD-O-3.2 files Germ cell tumor, NOS under this "
                      "number, so the record does not assert that a germinoma was diagnosed.",
        },
    )


# ------------------------------------------------------------------------------------------
# Recognition aids (registrar, 6 October 2026; spec 2026-10-06-ux-overall-fixes-design.md §5)
# ------------------------------------------------------------------------------------------
# An aid is clerk-facing: one sentence in report vocabulary, shown only under the option the
# clerk has selected. It helps a clerk recognise what a report naming that tumour describes; it
# is never grounds for the code, which stays the report's own term. The source of each aid is
# the comment above it, never the aid itself. Sources (Group 10 Papers/ and the Pathway):
#   Pathway    Group 10 Diagnostic Pathway, §1 "How it is reached" and "Diagnostic anchor"
#              columns, and §6.
#   Tourne     Tourne M, Radulescu C, Allory Y. Bull Cancer 2019;106:328-341 (testis; French,
#              translated here).
#   RDM        Rajpert-De Meyts E, et al. Folia Histochem Cytobiol 2015;53:177-188, pp. 178-179:
#              the same germ cell entities arise in the ovary and outside the gonads, and
#              dysgerminoma and germinoma are seminoma's ovarian and extragonadal counterparts.
#              This is why a description of the testicular tumour serves every site's tree.
#   Calaminus  Calaminus G, Joffe J. Prog Tumor Res 2016;43:115-127.
#   Pashankar  Pashankar F, et al. Eur J Cancer 2022;173:59-70 (ovarian immature teratoma).
#   Buza       Buza N. Surg Pathol Clin 2022, pp. 197-218 (gestational trophoblastic disease).
#   Bica       Bica O, et al. Int J Mol Sci 2024;25:6752.
#   Lim        Lim D, Oliva E. Pathology 2018;50(2):178-189 (ovarian sex cord-stromal tumours).
#   Atwi       Atwi D, et al. Pediatr Dev Pathol 2021;24(5):493-497.
#   Coskun     Coskun C, et al. J Pediatr Adolesc Gynecol 2023;36:112-115.
#   Handagala  Handagala I, et al. Gynecol Oncol Rep 2025;58:101697.
#   Li         Li et al. BMC Womens Health 2023;23:382.
# Options left without an aid, and why, are listed in docs/group_10_registrar_review.md E5.

# Pathway §1 X_1 ("sheets of large cells, lymphocytic stroma"); Tourne p. 331 (seminoma:
# clusters of fairly uniform cells in lobules divided by thin fibrous septa rich in lymphocytes);
# Bica Fig. 2, p. 3 (dysgerminoma: medium and large polygonal cells, lymphoid infiltrates in the
# stroma); RDM pp. 178-179 (dysgerminoma and germinoma are the same tumour).
AID_GERMINOMA = ("Reports describe sheets of large, uniform cells divided into lobules by thin "
                 "fibrous septa that hold lymphocytes.")
# Pathway §1 X_1, row 9062 ("Seminoma with brisk mitoses").
AID_SEMINOMA_MITOTIC = "Reports describe a seminoma with many dividing cells (mitoses)."
# Tourne p. 337: nodules of three cell types, small cells like lymphocytes, medium cells with
# round nuclei, and giant cells.
AID_SPERMATOCYTIC = ("Reports describe nodules of three kinds of cell: small cells like "
                     "lymphocytes, medium-sized round cells and giant cells.")
# Pathway §1 X_3 ("solid/papillary, pleomorphic"); Tourne p. 333 (solid, papillary, alveolar,
# tubular or pseudoglandular; atypia usually marked, prominent nucleoli, frequent mitoses).
AID_EMBRYONAL = ("Reports describe solid, papillary or gland-like growth of poorly "
                 "differentiated cells, usually markedly atypical, with prominent nucleoli and "
                 "frequent mitoses.")
# Pathway §1 X_3, row 9072 ("Embryoid bodies"); Tourne p. 336 (embryonal carcinoma and yolk sac
# tumour closely intermixed are described as polyembryoma).
AID_POLYEMBRYOMA = ("Reports describe embryoid bodies: embryonal carcinoma and yolk sac tumour "
                    "closely intermixed.")
# Pathway §1 X_4 ("Schiller-Duval bodies, reticular"); Tourne p. 335 (several patterns in one
# tumour; hyaline globules and Schiller-Duval bodies frequently seen; microcystic or reticular
# the commonest of eleven patterns) and p. 337 (the prepubertal type looks the same).
AID_YOLK_SAC = ("Reports often describe several growth patterns in one tumour, most often "
                "microcystic or reticular, with hyaline globules and Schiller-Duval bodies.")
# Pathway §6 ("syncytio/cytotrophoblast"); Tourne p. 335 (a biphasic, largely haemorrhagic
# growth of mononuclear trophoblast cells and multinucleated syncytiotrophoblast giant cells);
# Buza p. 206 (sheets of mononuclear trophoblast rimmed by multinucleated syncytiotrophoblast)
# and p. 207 (gestational and non-gestational choriocarcinoma look the same).
AID_CHORIOCARCINOMA = ("Reports describe a haemorrhagic tumour of two cell types: "
                       "single-nucleus trophoblast cells rimmed by large multinucleated "
                       "syncytiotrophoblast cells.")
# Tourne p. 336 (mixed germ cell tumours: most often more than two components, classically
# embryonal carcinoma with teratoma, seminoma or yolk sac tumour).
AID_MIXED = ("Reports list two or more germ cell components, such as embryonal carcinoma, "
             "teratoma, seminoma or yolk sac tumour.")
# Calaminus p. 118 (structures from all three germ layers: hair, squamous and mucous
# epithelium, teeth, cartilage, bone, glial or thyroid tissue); Tourne pp. 335-336.
AID_TERATOMA = ("Reports describe several kinds of tissue side by side, such as skin with "
                "hair, teeth, cartilage, bone, glands, brain (glial) tissue or thyroid.")
# Calaminus p. 118 (identifiable mature structures); Tourne p. 335 (a teratoma may consist of
# mature, well-differentiated tissue only); Pathway §6 ("≥2 lineages, all mature").
AID_MATURE_TERATOMA = ("Reports describe only mature, fully formed tissues, such as skin with "
                       "hair, cartilage, bone or glands, and no immature tissue.")
# Calaminus p. 118 (immature teratomas mostly show immature neurotubular structures);
# Pashankar Fig. 1, p. 61, and Fig. 2, p. 62 (primitive neuroectoderm forming rosettes).
AID_IMMATURE_TERATOMA = ("Reports describe teratoma tissues that include immature (primitive) "
                         "neural tissue, such as neural tubules or rosettes.")
# As above, and Pashankar p. 60: ovarian immature teratomas are graded 1 to 3 on the amount of
# immature neuroectoderm. The grade is ovarian practice, so only the ovary's aid names it.
AID_IMMATURE_TERATOMA_OVARY = ("Reports describe teratoma tissues that include immature "
                               "(primitive) neural tissue, such as neural tubules or rosettes, "
                               "and grade the tumour 1, 2 or 3.")
# Tourne p. 337 (a dermoid cyst has a fibrous wall lined by well-differentiated squamous
# epithelium with pilosebaceous adnexa); Calaminus p. 118 (hair and squamous epithelium among a
# teratoma's mature structures).
AID_DERMOID = ("Reports describe a cyst lined by skin-type (squamous) epithelium with hair "
               "follicles and sebaceous glands in its wall.")
# Tourne p. 337 (an epidermoid cyst is lined by regular squamous epithelium with no skin
# adnexa and holds layered keratin; a dermoid cyst has pilosebaceous adnexa).
AID_DERMOID_EPIDERMOID = ("Reports describe a cyst lined by skin-type (squamous) epithelium, "
                          "with hair follicles and sebaceous glands in the wall of a dermoid "
                          "cyst and none in an epidermoid cyst.")
# Tourne p. 336 (a distinct secondary component resembling a malignant somatic tumour, such as
# a carcinoma or a sarcoma); Pathway §1 X_2, row 9084 (squamous cell carcinoma in a dermoid).
AID_SOMATIC = ("Reports describe a teratoma in which a separate cancer of another tissue type "
               "has grown, such as a carcinoma or a sarcoma.")
# Pathway §1 X_2, row 9090 ("thyroid tissue"; a monodermal teratoma).
AID_STRUMA = "Reports describe a teratoma made up of thyroid tissue."
# Pathway §1 X_2, row 9091 ("Monodermal teratoma + carcinoid") with row 9090 (struma is
# thyroid tissue).
AID_STRUMAL_CARCINOID = ("Reports describe thyroid tissue (struma) mixed with a carcinoid "
                         "tumour.")
# Pathway §1 Xc7 ("germ cells + sex-cord nests"); RDM p. 178 (gonadoblastoma lies in nests of
# granulosa-like cells).
AID_GONADOBLASTOMA = ("Reports describe nests of germ cells mixed with sex cord cells that "
                      "resemble granulosa cells.")
# Tourne p. 330 (germ cell neoplasia in situ: seminiferous tubules colonised by cells like
# seminoma cells, with clear cytoplasm; intratubular seminoma fills the tubules).
AID_GCNIS = ("Reports describe cells like seminoma cells, with clear cytoplasm, lining or "
             "filling the seminiferous tubules, with no tumour outside them.")
# Tourne p. 336 (the orchidectomy usually shows only a scar with histiocytes, haemosiderin
# deposits and microcalcifications).
AID_REGRESSED = ("Reports usually describe only a scar in the testis, with histiocytes, "
                 "haemosiderin and microcalcifications.")
# Buza p. 209 (gestational: nests, cords and sheets of fairly uniform medium-sized trophoblastic
# cells with eosinophilic to clear cytoplasm).
AID_ETT = ("Reports describe nests, cords and sheets of fairly uniform, medium-sized "
           "trophoblast cells with pink to clear cytoplasm.")
# Buza p. 212 (gestational: large, mainly mononuclear intermediate trophoblast in cords and
# sheets, infiltrating between the smooth muscle fibres of the uterine wall).
AID_PSTT = ("Reports describe large trophoblast cells, most with one nucleus, in cords and "
            "sheets that spread between the muscle fibres of the uterine wall.")
# Buza p. 198 (well-developed complete mole: villous enlargement, marked hydrops, trophoblastic
# hyperplasia all round the villi; no fetal tissue).
AID_COMPLETE_MOLE = ("Reports describe enlarged, swollen (hydropic) chorionic villi with "
                     "trophoblast overgrowth all round them, and no fetal tissue.")
# Buza p. 198 (partial mole: two villous populations, large hydropic villi among small or
# normal ones; irregular scalloped outlines; mild to moderate trophoblastic hyperplasia).
AID_PARTIAL_MOLE = ("Reports describe two kinds of chorionic villi, large swollen ones among "
                    "small or normal ones, with irregular scalloped outlines and mild "
                    "trophoblast overgrowth.")
# Coskun p. 114 (generally oval hyperchromatic nuclei with minimal cytoplasm; a large cell
# variant in some cases); Atwi pp. 494 and 496 (small round blue cells in sheets, occasional
# follicle-like structures, a subset of large cells with eosinophilic cytoplasm).
AID_SCCOHT = ("Reports usually describe sheets of small round cells with dark nuclei and scant "
              "cytoplasm, sometimes with follicle-like spaces or larger cells with pink "
              "cytoplasm.")
# Handagala Fig. 3, p. 3 (papillary and micropapillary structures; small uniform cells with
# low-grade nuclei and low mitotic activity).
AID_LOW_GRADE_SEROUS = ("Reports describe papillae and micropapillae of small, uniform cells "
                        "with low-grade nuclei and few mitoses.")
# Li p. 2 (cysts filled with mucus; benign, borderline and carcinomatous areas in a continuum;
# glands with expansile growth and minimal or absent stroma).
AID_MUCINOUS_CYSTADENOCARCINOMA = ("Reports describe mucus-filled cysts with benign, borderline "
                                   "and cancerous areas side by side, the cancer forming "
                                   "crowded glands with little stroma between them.")
# Lim p. 179 (ovoid nuclei, pale chromatin, often nuclear grooves, the coffee-bean look;
# diffuse, microfollicular, trabecular and other patterns; Call-Exner bodies in the
# microfollicular pattern, absent in some tumours).
AID_ADULT_GRANULOSA = ("Reports describe granulosa cells with pale, often grooved "
                       "('coffee-bean') nuclei in sheets, cords or small follicles, sometimes "
                       "with Call-Exner bodies.")
# Lim p. 182 (nodular or diffuse growth in oedematous or myxoid stroma; follicle-like spaces
# of varying size holding secretions; round nuclei, abundant cytoplasm) and Fig. 4, p. 183
# (non-grooved nuclei).
AID_JUVENILE_GRANULOSA = ("Reports describe nodules or sheets of cells with round, ungrooved "
                          "nuclei and plentiful cytoplasm, with follicle-like spaces of "
                          "varying size that hold secretions.")
# Lim p. 183 (well differentiated: lobules of hollow or solid tubules lined by Sertoli cells,
# fibrous stroma holding Leydig cells, atypia and mitoses rare).
AID_SLCT_WELL = ("Reports describe lobules of tubules lined by Sertoli cells, with Leydig cells "
                 "in the fibrous tissue between them and little atypia.")
# Lim p. 183 (intermediate: immature Sertoli cells in nests, cords, poorly formed tubules or
# sheets, in lobules separated by oedematous stroma; Leydig cells at the edges of the lobules or
# in the stroma).
AID_SLCT_INTERMEDIATE = ("Reports describe lobules of immature Sertoli cells in nests, cords or "
                         "poorly formed tubules, with Leydig cells at their edges or in the loose "
                         "tissue between them.")
# Lim pp. 183-184 (as above; heterologous elements, most often intestinal-type mucinous
# epithelium).
AID_SLCT_INTERMEDIATE_HETEROLOGOUS = ("Reports describe an intermediate Sertoli-Leydig cell "
                                      "tumour that also holds another tissue, most often "
                                      "intestinal-type mucinous glands.")
# Lim p. 183 (poorly differentiated: diffuse or spindle-cell growth of poorly differentiated
# Sertoli cells with hyperchromatic nuclei, often brisk mitoses, Leydig cells inconspicuous).
AID_SLCT_POOR = ("Reports describe sheets or spindle-cell areas of immature Sertoli cells with "
                 "dark nuclei, often with many mitoses, and few Leydig cells.")
# Lim pp. 183-184 (as above; heterologous elements, most often intestinal-type mucinous
# epithelium, less often rhabdomyoblasts or cartilage).
AID_SLCT_POOR_HETEROLOGOUS = ("Reports describe a poorly differentiated Sertoli-Leydig cell "
                              "tumour that also holds another tissue, most often intestinal-type "
                              "mucinous glands, less often muscle (rhabdomyoblasts) or "
                              "cartilage.")
# Lim p. 183 (retiform: a network of irregularly branching, narrow slit-like tubules and cysts
# with papillary or polypoid projections).
AID_SLCT_RETIFORM = ("Reports describe a network of narrow, branching slit-like tubules and "
                     "cysts with papillary or polypoid projections.")
# Pathway §1 Xe, row 8632 ("granulosa + Sertoli-Leydig").
AID_GYNANDROBLASTOMA = ("Reports describe a tumour with both a granulosa cell component and a "
                        "Sertoli-Leydig cell component.")


def aid(branch, text):
    """Attach a recognition aid to an option and return it."""
    branch["recognition_aid"] = text
    return branch


# ------------------------------------------------------------------------------------------
# Histology (§4.3)
# ------------------------------------------------------------------------------------------
def named(label, morph, reason=None, upgrade=None, note=None):
    """A histology report naming the type, basis 7."""
    return code(label, morph, "3", 7, reason or rec(morph), upgrade=upgrade, note=note)


def germ_cell_core(site):
    """The germ cell options every site's histology node offers, in one order: embryonal
    carcinoma, polyembryoma, yolk sac tumour, choriocarcinoma, the mixed step, and a germ cell
    tumour whose type is not named, with and without immunostains. Site wording comes from
    SITES."""
    st = SITES[site]
    yolk = rec("9071") + (" " + st["yolk_sac_reason"] if st.get("yolk_sac_reason") else "")
    return [
        aid(named("Embryonal carcinoma", "9070", upgrade=IHC_CONFIRMS), AID_EMBRYONAL),
        aid(named("Polyembryoma", "9072", note="D7."), AID_POLYEMBRYOMA),
        aid(named(st["yolk_sac"], "9071", yolk, upgrade=IHC_CONFIRMS), AID_YOLK_SAC),
        aid(named(st["choriocarcinoma"], "9100", note="D8."), AID_CHORIOCARCINOMA),
        aid(go("Mixed germ cell tumour — more than one germ cell component",
               nid(site, "mixed")), AID_MIXED),
        named("Non-seminomatous or non-germinomatous germ cell tumour, type not named", "9065",
              "%s The report places the tumour outside the germinoma family without naming "
              "its type; a non-germinomatous germ cell tumour of the brain is the same "
              "assertion." % rec("9065"),
              note="D2: 9065/3 asserts a non-seminomatous tumour, so it is coded only where "
                   "the report says so."),
        go("Germ cell tumour, type not named, with immunostains listed", nid(site, "ihc")),
        code("Germ cell tumour, type not named, and no immunostains listed", "9064", "3", 7,
             "%s ICD-O-3.2 files Germ cell tumor, NOS under this number, so the record does "
             "not assert that a germinoma was diagnosed." % rec("9064"), note="D2."),
    ]


def histology_node(site, before, after, note):
    """The site's histology node: its own germinoma-family and teratoma options, the shared
    germ cell core, then the site's other tumour lines."""
    return node(
        nid(site, "histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        "Use the report's own term for the tumour.",
        before + germ_cell_core(site) + after, [], note)


CNS_IN_GROUP_X = "In the central nervous system ICCC-3 Group X registers behaviours 0, 1 and 3."


def n_histology_cns():
    s = "cns"
    return histology_node(s, [
        aid(named("Germinoma", "9064", upgrade=IHC_CONFIRMS), AID_GERMINOMA),
        aid(code("Mature teratoma", "9080", "0", 7, "%s %s" % (rec("9080", "0"),
                                                               CNS_IN_GROUP_X),
                 note="D5. ICCC-2017 range 95 (Xa2) declares 0-1,3."), AID_MATURE_TERATOMA),
        aid(named("Immature teratoma", "9080",
                  "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
                  note="D5. The pathway's 9083 for immature teratoma is wrong; 9083/3 is "
                       "Malignant teratoma, intermediate."), AID_IMMATURE_TERATOMA),
        code("Teratoma, with maturity not stated", "9080", "1", 7,
             "%s %s" % (rec("9080", "1"), CNS_IN_GROUP_X), note="D5."),
        aid(code("Dermoid cyst", "9084", "0", 7, "%s %s" % (rec("9084", "0"), CNS_IN_GROUP_X),
                 note="D5."), AID_DERMOID),
        aid(named("Teratoma with a somatic-type malignancy", "9084",
                  "%s ICD-O-3.2 gives it the synonym Teratoma with somatic type malignancies."
                  % rec("9084"), note="D5. Louis 2021 Table 1, p. 1235."), AID_SOMATIC),
    ], [
        refer("Not a germ cell tumour", 3,
              "A tumour of the brain or spinal cord that is not a germ cell tumour belongs to "
              "ICCC-3 Group III. Code the case from the Group III (central nervous system "
              "tumours) tree."),
    ], "Contract §4.3. Louis 2021 Table 1, p. 1235 for the central nervous system germ cell "
       "entities. Behaviours 0 and 1 are Group X codes here (ICCC-2017 ranges 94-99).")


def n_histology_ovary():
    s = "ovary"
    return histology_node(s, [
        aid(named("Dysgerminoma", "9060", upgrade=IHC_CONFIRMS, note="D1, D3."), AID_GERMINOMA),
        aid(named("Germinoma", "9064",
                  "%s A report that uses the term germinoma is coded as written; dysgerminoma "
                  "is 9060/3." % rec("9064"), upgrade=IHC_CONFIRMS, note="D1."), AID_GERMINOMA),
        aid(go("A teratoma, struma ovarii or strumal carcinoid", nid(s, "teratoma")),
            AID_TERATOMA),
    ], [
        aid(go("Gonadoblastoma, alone or with another tumour", nid(s, "gonadoblastoma")),
            AID_GONADOBLASTOMA),
        go("A sex cord–stromal tumour — granulosa cell, Sertoli-Leydig cell, Sertoli cell, "
           "Leydig cell, steroid cell, thecoma or another", nid(s, "sex_cord")),
        go("An epithelial tumour — carcinoma, borderline tumour or cystadenoma",
           nid(s, "epithelial")),
        aid(named("Small cell carcinoma, hypercalcaemic type", "8044",
                  "%s ICD-O-3.2 gives Small cell carcinoma, hypercalcemic type as a related "
                  "term of this code." % rec("8044"), note="D14."), AID_SCCOHT),
        go("Malignant tumour, type not determined", nid(s, "unspecified")),
        go("Another tumour type — neuroendocrine tumour, lymphoma, leukaemia, sarcoma, a "
           "metastatic deposit or another named tumour", nid(s, "other")),
    ], "Contract §4.3. ICD-O-3.2 for every ovarian code; Pfister 2022 Table 3, p. 342, for "
       "paediatric entity currency (D22: no ovary baseline paper on disk).")


def n_histology_testis():
    s = "testis"
    return histology_node(s, [
        aid(named("Seminoma", "9061", upgrade=IHC_CONFIRMS, note="D3."), AID_GERMINOMA),
        aid(named("Seminoma, anaplastic or with a high mitotic index", "9062",
                  "%s ICD-O-3.2 gives it the synonym Seminoma with high mitotic index."
                  % rec("9062"), note="D3."), AID_SEMINOMA_MITOTIC),
        aid(named("Spermatocytic tumour", "9063",
                  "%s ICD-O-3.2 gives it the synonym Spermatocytic tumor." % rec("9063"),
                  note="D3. Moch 2022 Table 3, p. 464."), AID_SPERMATOCYTIC),
        aid(go("A teratoma, dermoid cyst or epidermoid cyst", nid(s, "teratoma")),
            AID_TERATOMA),
    ], [
        named("Epithelioid trophoblastic tumour", "9105", note="D8. Moch 2022 Table 3, p. 464."),
        excl("Placental site trophoblastic tumour", "9104", "1", PSTT_REASON, decision=True,
             note="D8, provisional: the Group 8 9222 pattern."),
        aid(excl_outside("Germ cell neoplasia in situ, or an intratubular seminoma, embryonal "
                     "carcinoma, yolk sac tumour or teratoma, with no invasive tumour",
                     "germ cell neoplasia in situ", "9064", "2",
                     extra="WHO 2022 lists it among the non-invasive germ cell lesions (Moch "
                           "2022, Table 3, p. 464). WHO 2022's intratubular seminoma, embryonal "
                           "carcinoma, yolk sac tumour and teratoma have no ICD-O-3.2 code of "
                           "their own and take this one.",
                     note="D9, settled. Moch's intratubular 9061/2, 9070/2, 9071/2 and 9080/2 "
                          "are not ICD-O-3.2 codes; a report of any of them is this exclusion."),
            AID_GCNIS),
        aid(excl_outside("Regressed (burnt-out) germ cell tumour", "a regressed germ cell tumour",
                     "9080", "1",
                     extra="ICD-O-3.2 lists Germ cell tumor, regressed under this code, and "
                           "WHO 2022 codes regressed germ cell tumours 9080/1 (Moch 2022, "
                           "Table 3, p. 464).",
                     note="Settled by ICD-O-3.2 and Moch 2022 together; the same pattern as "
                          "Group V's 9514/1 spontaneously regressed retinoblastoma."),
            AID_REGRESSED),
        aid(go("Gonadoblastoma, alone or with another tumour", nid(s, "gonadoblastoma")),
            AID_GONADOBLASTOMA),
        go("A sex cord–stromal tumour — Leydig cell, Sertoli cell, granulosa cell or another",
           nid(s, "sex_cord")),
        named("Carcinoma", "8010", upgrade=TYPE_NOT_STATED,
              note="D14: the testis tree offers 8010/3 only."),
        go("Malignant tumour, type not determined", nid(s, "unspecified")),
        go("Another tumour type — neuroendocrine tumour, lymphoma, leukaemia, sarcoma, a "
           "metastatic deposit or another named tumour", nid(s, "other")),
    ], "Contract §4.3. Moch H, et al. European Urology 2022;82(5):458-468, Table 3, "
       "pp. 464-465, is the testis baseline.")


def n_histology_extragonadal():
    s = "extragonadal"
    return histology_node(s, [
        aid(named("Germinoma", "9064", upgrade=IHC_CONFIRMS, note="D1."), AID_GERMINOMA),
        aid(named("Seminoma", "9061", upgrade=IHC_CONFIRMS, note="D3: coded as written."),
            AID_GERMINOMA),
        aid(go("A teratoma or dermoid cyst", nid(s, "teratoma")), AID_TERATOMA),
    ], [
        aid(named("Epithelioid trophoblastic tumour", "9105", note="D8."), AID_ETT),
        aid(excl("Placental site trophoblastic tumour", "9104", "1", PSTT_REASON, decision=True,
                 note="D8, provisional."), AID_PSTT),
        aid(excl_outside("Complete hydatidiform mole", "complete hydatidiform mole", "9100",
                         "0", note="D8, settled."), AID_COMPLETE_MOLE),
        aid(excl_outside("Partial hydatidiform mole", "partial hydatidiform mole", "9103", "0",
                         note="D8, settled."), AID_PARTIAL_MOLE),
        excl_outside("Invasive mole", "invasive mole", "9100", "1", note="D8, settled."),
        go("Not a germ cell or trophoblastic tumour — including a sex cord–stromal tumour or "
           "a carcinoma", nid(s, "other")),
    ], "Contract §4.3. ICCC-2017 ranges 100-105 (Xb), behaviour 3 only. The p57 and "
       "genotyping algorithm for moles is not built: every outcome is an exclusion (D8).")


HISTOLOGY_BUILDERS = {"cns": n_histology_cns, "ovary": n_histology_ovary,
                      "testis": n_histology_testis, "extragonadal": n_histology_extragonadal}


# ------------------------------------------------------------------------------------------
# Site-specific nodes (§4.4)
# ------------------------------------------------------------------------------------------
def n_teratoma_ovary():
    s = "ovary"
    return node(
        nid(s, "teratoma"), "histology_subclassification", 4, "Teratoma",
        "Which teratoma or related tumour does the report diagnose?",
        "Use the report's own term. An immature teratoma of any grade is malignant.",
        [
            aid(excl_outside("Mature cystic teratoma (mature teratoma)",
                             "mature cystic teratoma", "9080", "0", note="D5, settled."),
                AID_MATURE_TERATOMA),
            aid(excl_outside("Dermoid cyst", "dermoid cyst", "9084", "0", note="D5, settled."),
                AID_DERMOID),
            aid(named("Immature teratoma, any grade", "9080",
                      "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
                      note="D5."), AID_IMMATURE_TERATOMA_OVARY),
            excl_outside("Teratoma, with maturity not stated", "a teratoma whose maturity is "
                         "not stated", "9080", "1", note="D5, settled."),
            aid(named("Teratoma or dermoid cyst with a somatic-type malignancy (a carcinoma or "
                      "sarcoma arising in it)", "9084",
                      "%s ICD-O-3.2 gives it the synonym Dermoid cyst with malignant "
                      "transformation." % rec("9084"), note="D5."), AID_SOMATIC),
            aid(excl_outside("Struma ovarii", "struma ovarii", "9090", "0", note="D5, settled."),
                AID_STRUMA),
            named("Malignant struma ovarii", "9090",
                  note="D5. ICCC-2017 range 107 (Xc2)."),
            aid(excl_outside("Strumal carcinoid", "strumal carcinoid", "9091", "1",
                             extra="ICD-O-3.2 has no malignant code for it.",
                             note="D5, settled: ICD-O-3.2 has no 9091/3."),
                AID_STRUMAL_CARCINOID),
            go("A teratoma with a yolk sac tumour or another malignant germ cell component",
               nid(s, "mixed")),
        ],
        [], "Contract §4.4, D5.")


def n_teratoma_testis():
    s = "testis"
    return node(
        nid(s, "teratoma"), "histology_subclassification", 4, "Teratoma",
        "Which teratoma does the report diagnose?",
        "Use the report's own term. WHO 2022 separates prepubertal-type teratoma, which is "
        "benign, from postpubertal-type teratoma, which is malignant (Moch 2022, Table 3, "
        "p. 464).",
        [
            excl_outside("Teratoma, prepubertal type", "teratoma, prepubertal type", "9084",
                         "0", extra="WHO 2022 does the same (Moch 2022, Table 3, p. 464).",
                         note="D5, settled. ICD-O-3.2 related term of 9084/0."),
            aid(excl_outside("Dermoid cyst or epidermoid cyst", "a dermoid cyst", "9084", "0",
                             extra="WHO 2022 codes dermoid and epidermoid cysts of the testis "
                                   "9084/0 (Moch 2022, Table 3, p. 464).",
                             note="D5, settled."), AID_DERMOID_EPIDERMOID),
            named("Teratoma, postpubertal type", "9080",
                  "%s WHO 2022 codes postpubertal-type teratoma 9080/3 (Moch 2022, Table 3, "
                  "p. 464)." % rec("9080"), note="D5."),
            aid(named("Immature teratoma", "9080",
                      "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
                      note="D5."), AID_IMMATURE_TERATOMA),
            excl_outside("Mature teratoma, with prepubertal or postpubertal type not stated",
                         "mature teratoma", "9080", "0", decision=True,
                         note="D5; registrar review A5 open: code as written, or 9080/3 "
                              "after puberty."),
            excl_outside("Teratoma, with maturity and type not stated",
                         "a teratoma whose type is not stated", "9080", "1", decision=True,
                         note="D5; registrar review A5 open: code as written, or 9080/3 "
                              "after puberty."),
            aid(named("Teratoma with a somatic-type malignancy", "9084",
                      "%s ICD-O-3.2 gives it the synonym Teratoma with somatic type "
                      "malignancies." % rec("9084"), note="D5. Moch 2022 Table 3, p. 464."),
                AID_SOMATIC),
            go("Teratoma with another malignant germ cell component", nid(s, "mixed")),
        ],
        [], "Contract §4.4, D5. The prepubertal and postpubertal types enter only here, where "
            "they change the code (D15).")


def n_teratoma_extragonadal():
    s = "extragonadal"
    return node(
        nid(s, "teratoma"), "histology_subclassification", 4, "Teratoma",
        "Which teratoma does the report diagnose?",
        "Use the report's own term and site. ICD-O-3.2 codes immature teratoma of the lung, "
        "thymus or thyroid differently from immature teratoma elsewhere.",
        [
            aid(excl_outside("Mature teratoma", "mature teratoma", "9080", "0",
                             note="D5, settled."), AID_MATURE_TERATOMA),
            aid(excl_outside("Immature teratoma of the lung, thymus or thyroid",
                         "immature teratoma of the lung, thymus or thyroid", "9080", "1",
                         decision=True,
                         extra="ICD-O-3.2 lists the change in 'Terms that are changing "
                               "behaviour', p. 6.",
                         note="D5: the thymus part is provisional. A mediastinal immature "
                              "teratoma recorded at C38.1 is 9080/3 by the same rule."),
                AID_IMMATURE_TERATOMA),
            aid(named("Immature teratoma at any other site — sacrococcygeal region, mediastinum "
                      "outside the thymus, retroperitoneum or elsewhere", "9080",
                      "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
                      note="D5."), AID_IMMATURE_TERATOMA),
            excl_outside("Teratoma, with maturity not stated",
                         "a teratoma whose maturity is not stated", "9080", "1",
                         note="D5, settled."),
            aid(excl_outside("Dermoid cyst", "dermoid cyst", "9084", "0", note="D5, settled."),
                AID_DERMOID),
            aid(named("Teratoma with a somatic-type malignancy", "9084",
                      "%s ICD-O-3.2 gives it the synonym Teratoma with somatic type "
                      "malignancies." % rec("9084"), note="D5."), AID_SOMATIC),
            go("Teratoma with a yolk sac tumour or another malignant germ cell component",
               nid(s, "mixed")),
        ],
        [], "Contract §4.4, D5.")


def n_gonadoblastoma(site):
    assert site in GONADS, site

    def invasive(term_, morph):
        """D3: the invasive germinoma-family tumour is coded as the report writes it. ICCC-2017
        range 106 (Xc1) holds 9060-9065 at both C56.9 and C62."""
        own = term_ == SITES[site]["family_term"]
        return named("Gonadoblastoma with an invasive %s" % term_, morph,
                     None if own else "%s A report that uses the term %s is coded as written."
                     % (rec(morph), term_),
                     upgrade=IHC_CONFIRMS, note="D10, D3%s." % ("" if own else ", D1"
                                                                if morph == "9064" else ""))
    return node(
        nid(site, "gonadoblastoma"), "histology_subclassification", 4, "Gonadoblastoma",
        "What does the report find with the gonadoblastoma?",
        "Gonadoblastoma alone is not malignant. Code an invasive germ cell tumour arising in it "
        "by the report's own term.",
        [
            excl_outside("Gonadoblastoma alone, with no invasive tumour", "gonadoblastoma",
                         "9073", "1", decision=True,
                         extra="ICD-O-3.2 has no malignant code for it, and WHO 2022 lists it "
                               "among the non-invasive lesions (Moch 2022, Table 3, p. 464).",
                         note="D10, provisional. ICCC-2017 range 112 (Xc7) holds no usable "
                              "code."),
            excl_outside("Mixed germ cell–sex cord-stromal tumour, with no invasive tumour",
                         "mixed germ cell-sex cord-stromal tumour", "8594", "1", decision=True,
                         note="D10, provisional. New in ICD-O-3.2."),
            invasive("dysgerminoma", "9060"),
            invasive("seminoma", "9061"),
            invasive("germinoma", "9064"),
            named("Gonadoblastoma with an invasive yolk sac tumour", "9071",
                  upgrade=IHC_CONFIRMS, note="D10."),
            named("Gonadoblastoma with an invasive embryonal carcinoma", "9070",
                  upgrade=IHC_CONFIRMS, note="D10."),
            go("Gonadoblastoma with an invasive mixed germ cell tumour", nid(site, "mixed")),
        ],
        [], "D10. The disorder-of-sex-development entry and karyotype variables are not built "
            "(D10, D15): the tool codes the tumour present in the file.")


def n_sex_cord_ovary():
    s = "ovary"
    return node(
        nid(s, "sex_cord"), "histology_subclassification", 4, "Sex cord–stromal tumour",
        "Which sex cord–stromal tumour does the report diagnose?",
        "Use the report's own term, including the Sertoli-Leydig cell tumour's "
        "differentiation.",
        [
            aid(named("Adult granulosa cell tumour", "8620",
                      "%s ICD-O-3.2 changed the behaviour of the adult granulosa cell tumour of "
                      "the ovary from 1 to 3." % rec("8620"),
                      note="D11. 'Terms that are changing behaviour', p. 4."),
                AID_ADULT_GRANULOSA),
            aid(sex_cord_excl("Juvenile granulosa cell tumour", "juvenile granulosa cell tumour",
                              "8622", "1", decision=True), AID_JUVENILE_GRANULOSA),
            excl("Granulosa cell tumour, adult or juvenile type not stated", "8622", "1",
                 "ICD-O-3.2 prints no term for a granulosa cell tumour of the ovary whose type "
                 "is not stated: the adult type is 8620/3, a Group X cancer, and the juvenile "
                 "type 8622/1, behaviour 1, outside Group X. The juvenile type is the "
                 "granulosa cell tumour of childhood (Pfister 2022, p. 343), so the case is "
                 "shown under 8622/1 and is not recorded as a Group X cancer. A report that "
                 "states the type is coded by that type." + PENDING,
                 decision=True,
                 note="D11; registrar review A1. Code review, 6 October 2026: no option fitted "
                      "a report that leaves the type unstated."),
            aid(named("Sertoli-Leydig cell tumour, poorly differentiated", "8631", note="D11."),
                AID_SLCT_POOR),
            aid(named("Sertoli-Leydig cell tumour, poorly differentiated, with heterologous "
                      "elements", "8634", note="D11."), AID_SLCT_POOR_HETEROLOGOUS),
            aid(sex_cord_excl("Sertoli-Leydig cell tumour, intermediate differentiation",
                              "Sertoli-Leydig cell tumour of intermediate differentiation",
                              "8631", "1"), AID_SLCT_INTERMEDIATE),
            aid(sex_cord_excl("Sertoli-Leydig cell tumour, intermediate differentiation, with "
                              "heterologous elements", "Sertoli-Leydig cell tumour of "
                              "intermediate differentiation with heterologous elements", "8634",
                              "1"), AID_SLCT_INTERMEDIATE_HETEROLOGOUS),
            aid(sex_cord_excl("Sertoli-Leydig cell tumour, well differentiated",
                              "well-differentiated Sertoli-Leydig cell tumour", "8631", "0"),
                AID_SLCT_WELL),
            aid(sex_cord_excl("Sertoli-Leydig cell tumour, retiform",
                              "retiform Sertoli-Leydig cell tumour", "8633", "1"),
                AID_SLCT_RETIFORM),
            sex_cord_excl("Sertoli-Leydig cell tumour, differentiation not stated",
                          "Sertoli-Leydig cell tumour, NOS", "8631", "1"),
            sex_cord_excl("Sertoli cell tumour", "Sertoli cell tumour", "8640", "1"),
            named("Malignant Sertoli cell tumour, or Sertoli cell carcinoma", "8640",
                  note="D11."),
            sex_cord_excl("Leydig cell tumour", "Leydig cell tumour of the ovary", "8650", "0"),
            named("Malignant Leydig cell tumour", "8650", note="D11."),
            sex_cord_excl("Steroid cell tumour", "steroid cell tumour", "8670", "0"),
            named("Malignant steroid cell tumour", "8670", note="D11."),
            sex_cord_excl("Thecoma", "thecoma", "8600", "0"),
            named("Malignant thecoma", "8600", note="D11."),
            aid(sex_cord_excl("Gynandroblastoma", "gynandroblastoma", "8632", "1"),
                AID_GYNANDROBLASTOMA),
            sex_cord_excl("Sex cord tumour with annular tubules",
                          "sex cord tumour with annular tubules", "8623", "1"),
            sex_cord_excl("Microcystic stromal tumour or signet-ring stromal tumour",
                          "microcystic and signet-ring stromal tumours", "8590", "0"),
            sex_cord_excl("Sex cord–stromal tumour, type not stated",
                          "a sex cord-stromal tumour of unstated type", "8590", "1",
                          decision=True),
        ],
        [], "D11 by ICD-O-3.2. Juvenile granulosa cell tumour, the commonest sex cord-stromal "
            "tumour of childhood, is not registrable under ICCC-2017 (D11's registrar "
            "question). D12: no /3 that ICD-O-3.2 does not print. FOXL2 and DICER1 change no "
            "code and are not asked (D11).")


def n_sex_cord_testis():
    s = "testis"
    return node(
        nid(s, "sex_cord"), "histology_subclassification", 4, "Sex cord–stromal tumour",
        "Which sex cord–stromal tumour does the report diagnose?",
        "Use the report's own term. Choose a malignant option only where the report calls "
        "the tumour malignant.",
        [
            sex_cord_excl("Leydig cell tumour", "Leydig cell tumour of the testis", "8650",
                          "1"),
            named("Malignant Leydig cell tumour", "8650", note="D11. Moch 2022 Table 3, "
                                                               "p. 464."),
            sex_cord_excl("Sertoli cell tumour", "Sertoli cell tumour", "8640", "1"),
            named("Malignant Sertoli cell tumour", "8640", note="D11. Moch 2022 Table 3, "
                                                                "p. 465."),
            sex_cord_excl("Large cell calcifying Sertoli cell tumour",
                          "large cell calcifying Sertoli cell tumour", "8642", "1"),
            sex_cord_excl("Adult granulosa cell tumour",
                          "adult granulosa cell tumour of the testis", "8620", "1"),
            sex_cord_excl("Juvenile granulosa cell tumour",
                          "juvenile granulosa cell tumour of the testis", "8622", "0",
                          decision=True),
            named("Sertoli-Leydig cell tumour, poorly differentiated", "8631", note="D11."),
            sex_cord_excl("Mixed or unclassified sex cord–stromal tumour",
                          "a mixed sex cord-stromal tumour", "8592", "1"),
            sex_cord_excl("Sex cord–stromal tumour, type not stated",
                          "a sex cord-stromal tumour of unstated type", "8590", "1",
                          decision=True),
        ],
        [], "D11. Moch 2022 Table 3, pp. 464-465: Leydig 8650/1, malignant 8650/3; Sertoli "
            "8640/1, malignant 8640/3; large cell calcifying 8642/1; adult granulosa 8620/1; "
            "juvenile granulosa 8622/0; mixed 8592/1; NOS 8590/1.")


def n_epithelial_ovary():
    s = "ovary"
    return node(
        nid(s, "epithelial"), "histology_subclassification", 4, "Epithelial tumour",
        "Which epithelial tumour does the report diagnose?",
        "Use the report's own term. Borderline tumours and cystadenomas are not malignant.",
        [
            aid(named("Small cell carcinoma, hypercalcaemic type", "8044",
                      "%s ICD-O-3.2 gives Small cell carcinoma, hypercalcemic type as a related "
                      "term of this code." % rec("8044"), note="D14."), AID_SCCOHT),
            aid(named("Low-grade serous carcinoma", "8460", note="D14."), AID_LOW_GRADE_SEROUS),
            named("High-grade serous carcinoma", "8461", note="D14."),
            named("Serous carcinoma, grade not stated", "8441", note="D14.",
                  upgrade="A report that states the grade gives low-grade serous carcinoma "
                          "(8460/3) or high-grade serous carcinoma (8461/3)."),
            named("Mucinous carcinoma", "8480",
                  "%s ICD-O-3.2 gives it the synonym Mucinous carcinoma." % rec("8480"),
                  note="D14."),
            aid(named("Mucinous cystadenocarcinoma", "8470", note="D14."),
                AID_MUCINOUS_CYSTADENOCARCINOMA),
            named("Endometrioid carcinoma", "8380", note="D14."),
            named("Clear cell carcinoma", "8310", note="D14."),
            named("Seromucinous carcinoma", "8474", note="D14."),
            named("Undifferentiated carcinoma", "8020", note="D14."),
            named("Adenocarcinoma, type not stated", "8140", note="D14.",
                  upgrade=TYPE_NOT_STATED),
            named("Carcinoma, type not stated", "8010", note="D14.", upgrade=TYPE_NOT_STATED),
        ] + [excl_d(label, label.lower(), icdo, beh, "D14", decision=True)
             for label, icdo, beh in (
                 ("Serous borderline tumour", "8442", "1"),
                 ("Mucinous borderline tumour", "8472", "1"),
                 ("Seromucinous borderline tumour", "8474", "1"),
                 ("Endometrioid borderline tumour", "8380", "1"),
                 ("Serous cystadenoma", "8441", "0"),
                 ("Mucinous cystadenoma", "8470", "0"))],
        [], "D14: the paediatric subset of Xd on the tree; every other Xd code is in the "
            "inventory and reachable by search.")


def n_unspecified(site):
    return node(
        nid(site, "unspecified"), "histology_subclassification", 4, "Malignant tumour, type "
        "not determined",
        "How does the report describe the malignant tumour?",
        "The report establishes a malignant tumour without determining its type. Choose the "
        "cell type the report describes, if it describes one.",
        [
            named("Malignant neoplasm, type not determined, cell type not described", "8000",
                  upgrade=TYPE_NOT_STATED),
            named("Malignant tumour, small cell type", "8002", upgrade=TYPE_NOT_STATED),
            named("Malignant tumour, giant cell type", "8003", upgrade=TYPE_NOT_STATED),
            named("Malignant tumour, spindle cell type", "8004", upgrade=TYPE_NOT_STATED),
            named("Malignant tumour, clear cell type", "8005", upgrade=TYPE_NOT_STATED),
        ],
        [], "D13: ICCC-2017 range 117 places 8000-8005 at C56.9 and C62 in Xe.")


# The referrals the gonadal and extragonadal "another tumour type" nodes share. `where`, when
# given, names the gonad in the clerk's sentence.
SARCOMA_REASON = ("A soft tissue sarcoma belongs to ICCC-3 Group IX. Code the case from the "
                  "Group IX (soft tissue sarcomas) tree.")


def refer_lymphoma(where=None):
    return refer("Lymphoma", 2,
                 "A lymphoma%s belongs to ICCC-3 Group II. Code the case from the Group II "
                 "(lymphomas) tree." % (" involving %s" % where if where else ""))


def go_deposit(site):
    return go("A deposit of a tumour that began elsewhere", nid(site, "deposit"))


# A deposit is coded as its primary, from the primary's group, and a deposit with no primary
# found is ICCC-3 Group XII: the pattern of Group III pf_secondary_deposit, Group VII
# hp_secondary_deposit and Group VIII bn_metastasis. A germ cell primary at another site is
# Group X itself, which a referral cannot name, so the hint sends it back to the site step.
DEPOSIT_PRIMARIES = (
    ("Neuroblastoma", 4, "Neuroblastoma is ICCC-3 Group IV."),
    ("Nephroblastoma (Wilms tumour), or another kidney tumour", 6,
     "Renal tumours are ICCC-3 Group VI."),
    ("Hepatoblastoma, or another liver tumour", 7, "Hepatic tumours are ICCC-3 Group VII."),
    ("A bone sarcoma", 8, "Malignant bone tumours are ICCC-3 Group VIII."),
    ("A soft tissue sarcoma, including rhabdomyosarcoma", 9,
     "Soft tissue sarcomas are ICCC-3 Group IX."),
    ("A tumour of the brain or spinal cord", 3,
     "Central nervous system tumours are ICCC-3 Group III."),
    ("Retinoblastoma", 5, "Retinoblastoma is ICCC-3 Group V."),
    ("A carcinoma or melanoma of another organ", 11,
     "Carcinomas of other organs and melanomas are ICCC-3 Group XI."),
)


def n_deposit(site):
    where = SITES[site].get("where")
    return node(
        nid(site, "deposit"), "morphology_only", 5, "Metastatic deposit",
        "Where does the report say the primary tumour is?",
        "The tumour%s is a deposit, not a separate registration: the case is coded at its "
        "primary site. A deposit of a germ cell tumour that began at another site is coded "
        "there: go back to the site step and record the primary's topography. A lymphoma or "
        "leukaemia is answered at the step before." % (" in %s" % where if where else ""),
        [refer(label, group, "%s Code the case at its primary." % why)
         for label, group, why in DEPOSIT_PRIMARIES] + [
            refer("The primary is not known and has not been found", 12,
                  "A deposit with no identified primary belongs in ICCC-3 Group XII, other "
                  "and unspecified malignant neoplasms. Code the case from the Group XII "
                  "tree."),
        ],
        [], "Code review, 6 October 2026: the deposit was non_reportable, so a malignancy "
            "left the registry and an unknown primary had no route.")


def refer_other_named():
    return refer("Another malignant tumour type the report names", 12,
                 "ICCC-3 Group XII holds the specified malignant tumours no other group codes. "
                 "Code the case from the Group XII (other and unspecified malignant neoplasms) "
                 "tree.")


def refer_carcinoma(label, what):
    return refer(label, 11,
                 "%s belongs to ICCC-3 Group XI (other malignant epithelial neoplasms and "
                 "malignant melanomas). Code the case from the Group XI tree." % what)


# ICCC-2017 places these in Group X at every site (000-809), so the extragonadal tree codes them
# rather than referring them: the malignant sex cord-stromal tumours (range 116, Xe,
# 8590-8671) and the ovarian-type carcinomas of range 114 (Xd). ICD-O-3.2 prints no /3 for
# 8443, 8444 or 8451, the rest of range 114.
EXTRAGONADAL_GROUP_X = (
    ("Adult granulosa cell tumour", "8620", 116),
    ("Sertoli-Leydig cell tumour, poorly differentiated", "8631", 116),
    ("Sertoli-Leydig cell tumour, poorly differentiated, with heterologous elements", "8634",
     116),
    ("Malignant Sertoli cell tumour, or Sertoli cell carcinoma", "8640", 116),
    ("Malignant Leydig cell tumour", "8650", 116),
    ("Malignant steroid cell tumour", "8670", 116),
    ("Malignant thecoma", "8600", 116),
    ("Seromucinous carcinoma", "8474", 114),
    ("Clear cell adenocarcinofibroma", "8313", 114),
    ("Mucinous adenocarcinofibroma", "9015", 114),
)


def n_group_x_everywhere():
    return [named(label, morph,
                  "%s ICCC-3 places this tumour type in Group X at every site (ICCC-2017 range "
                  "%d, %s)." % (rec(morph), rng, "Xe" if rng == 116 else "Xd"),
                  note="ICCC-2017 range %d covers sites 000-809." % rng)
            for label, morph, rng in EXTRAGONADAL_GROUP_X]


# ICCC-2017 range 63 (Ewing sarcoma), 59 (osteosarcoma) and 60 (chondrosarcoma) place these
# types at sites 760-768 in Group VIII; at the other extragonadal sites they are Group IX.
BONE_TYPE_AT_PELVIS = refer(
    "Ewing sarcoma, osteosarcoma or chondrosarcoma, with the site recorded as Pelvis, NOS "
    "(C76.3)", 8,
    "At Pelvis, NOS (C76.3) ICCC-3 places Ewing sarcoma, osteosarcoma and chondrosarcoma in "
    "Group VIII (malignant bone tumours). Code the case from the Group VIII tree.")


def n_other_gonad(site):
    assert site in GONADS, site
    where = SITES[site]["where"]
    return node(
        nid(site, "other"), "morphology_only", 4, "Another tumour type",
        "Which tumour does the report diagnose?",
        "A neuroendocrine tumour of %s is coded here. Any other tumour that is not a germ "
        "cell, sex cord–stromal or epithelial tumour is coded from another group, or at its "
        "primary site." % where,
        [
            named("Neuroendocrine tumour or carcinoid tumour", "8240",
                  "%s ICCC-3 places it in Group X at %s (ICCC-2017 range 113, Xd)."
                  % (rec("8240"), where), note="ICCC-2017 range 113: 8221-8241, 8244-8246."),
            named("Neuroendocrine carcinoma", "8246",
                  "%s ICCC-3 places it in Group X at %s (ICCC-2017 range 113, Xd)."
                  % (rec("8246"), where), note="ICCC-2017 range 113: 8221-8241, 8244-8246."),
            refer_lymphoma(where),
            refer("Leukaemic infiltration", 1,
                  "Leukaemic infiltration of %s is coded as the leukaemia, in ICCC-3 Group I. "
                  "Code the case from the Group I (leukaemias) tree." % where),
            refer("Rhabdomyosarcoma or another sarcoma", 9, SARCOMA_REASON),
            go_deposit(site),
            refer_carcinoma("A melanoma", "A melanoma of %s" % where),
            refer_other_named(),
        ],
        [], "Contract §4.4. The neuroendocrine tumours are Xd at the gonads (ICCC-2017 range "
            "113), so they are coded here, not referred.")


def n_other_extragonadal():
    s = "extragonadal"
    return node(
        nid(s, "other"), "morphology_only", 4, "Another tumour type",
        "Which tumour does the report diagnose?",
        "The malignant sex cord–stromal tumours and three ovarian-type carcinomas listed first "
        "are Group X at every site and are coded here. Any other tumour that is not a germ "
        "cell or trophoblastic tumour is coded from another group, or at its primary site.",
        n_group_x_everywhere() + [
            refer_lymphoma(),
            refer("Neuroblastoma", 4,
                  "Neuroblastoma belongs to ICCC-3 Group IV. Code the case from the Group IV "
                  "tree."),
            BONE_TYPE_AT_PELVIS,
            refer("A sarcoma", 9, SARCOMA_REASON),
            go_deposit(s),
            refer_carcinoma("Another carcinoma, or a melanoma", "A carcinoma or melanoma "
                            "outside the gonads"),
            refer_other_named(),
        ],
        [], "Contract §4.4. ICCC-2017 ranges 114 and 116 cover sites 000-809, so their tumour "
            "types are coded here rather than referred.")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def common(site):
    """The sixteen nodes every site tree carries, in tree order: the contract's eight, the four
    laboratory screens behind the evidence checklist (registrar, 6 October 2026), the
    clinical-note and imaging nodes for the cytology and marker evidence contexts, and the
    component checklist after the mixed tumour's named-term question."""
    targets = {"referral": clinical_node(site), "markers": nid(site, "markers"),
               "imaging": imaging_node(site), "cytology": nid(site, "cytology"),
               "histology": nid(site, "histology")}
    lab_targets = {t: lab_node_id(site, t) for t in LAB_TIERS}
    if site == "cns":
        # Registrar, 6 October 2026: the brain marker tier meets the age gate first, and the
        # laboratory screen only under 24 months or with no age (brain_marker_nodes()).
        lab_targets["markers"] = "cn_marker_age"
    return [
        n_document_inventory(nid(site, "document_inventory"), targets, lab_targets,
                             "Contract §4.2: five evidence tiers. Every Group X tree carries "
                             "the same tiers; the router's site capture chose this tree. A "
                             "tier a Lab Report can join routes through a laboratory screen "
                             "when Lab Report is ticked (registrar, 6 October 2026)."),
        *[n_labs(site, t, targets[t]) for t in LAB_TIERS],
        n_clinical_alias(site), n_clinical_alias(site, "cytology"), n_markers(site),
        n_imaging(site), n_imaging(site, "markers"), n_imaging(site, "cytology"),
        n_cytology(site), HISTOLOGY_BUILDERS[site](), n_mixed(site),
        n_mixed_components(site), n_ihc(site),
    ]


TREE_LABELS = {
    "cns": "Germ cell tumours of the brain and spinal cord (C70.0-C72.9, C75.1-C75.3; ICCC-3 Xa "
           "admits behaviours 0, 1 and 3) - an evidence gate, a marker route, and a histology "
           "node with mixed and stain panel steps",
    "ovary": "Germ cell, sex cord-stromal and epithelial tumours of the ovary (C56.9; ICCC-3 "
             "Xc, Xd and Xe, behaviour 3 only) - the common evidence and germ cell nodes, with "
             "behaviour exclusions for benign and borderline tumours",
    "testis": "Germ cell and sex cord-stromal tumours of the testis (C62.0-C62.9; ICCC-3 Xc, Xd "
              "and Xe, behaviour 3 only) - the common evidence and germ cell nodes, with "
              "behaviour exclusions for benign, borderline and in situ lesions",
    "extragonadal": "Germ cell and trophoblastic tumours outside the gonads and the central "
                    "nervous system (ICCC-3 Xb, behaviour 3 only) - the common evidence and germ "
                    "cell nodes, with moles and benign teratomas as behaviour exclusions",
}
SITE_NODES = {
    "cns": brain_marker_nodes,
    "ovary": lambda: [n_teratoma_ovary(), n_gonadoblastoma("ovary"), n_sex_cord_ovary(),
                      n_epithelial_ovary(), n_unspecified("ovary"), n_other_gonad("ovary"),
                      n_deposit("ovary")],
    "testis": lambda: [n_teratoma_testis(), n_gonadoblastoma("testis"), n_sex_cord_testis(),
                       n_unspecified("testis"), n_other_gonad("testis"), n_deposit("testis")],
    "extragonadal": lambda: [n_teratoma_extragonadal(), n_other_extragonadal(),
                             n_deposit("extragonadal")],
}


def _tree(tree_id, label, entry, topography, nodes):
    return {"tree_id": tree_id, "tree_label": label, "entry_node": entry,
            "topography": topography, "basis_of_diagnosis_defaults": dict(BASIS_DEFAULTS),
            "nodes": nodes}


def trees() -> list:
    """Return the four trees as a fresh structure that shares no object with any other call or
    with itself (a JSON round trip), so callers may mutate it freely."""
    out = [_tree(st["tree"], TREE_LABELS[site], nid(site, "document_inventory"),
                 _topo(TOPOGRAPHY_RAW[site]), common(site) + SITE_NODES[site]())
           for site, st in SITES.items()]
    return json.loads(json.dumps(out))
