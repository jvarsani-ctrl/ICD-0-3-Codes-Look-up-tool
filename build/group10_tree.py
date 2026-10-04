"""The ICCC-3 Group X decision trees, as data.

Authored here rather than by hand in group_10_dt.json so the trees and the entries regenerate
together from one command (build/generate_group10_entries.py). Edit the trees HERE; the JSON is
the product. Architecture: docs/group_10_build_contract.md §4. Code decisions D1-D22:
docs/superpowers/specs/2026-10-04-group-10-germ-cell-code-decisions-design.md.

Five trees. Four site trees share one set of node builders, parameterised by SITES, so the
histotype logic is written once: g10_cns (cn_), g10_ovary (ov_), g10_testis (ts_),
g10_extragonadal (eg_). The fifth, g10_site_unstated (su_), is the router's default: it asks the
evidence, then the site, and hands on by cross-tree next_node into the matching site tree. It
emits nothing itself.

Clerk-facing text lives in `question`, `hint`, `label`, `reason` and `upgrade_path`.
`coding_note` is author-facing and never rendered. No clerk-facing string names a node id or a
schema field (check_no_internal_identifier_leaks). `clinical_alert` is null everywhere
(ruling 9). Every name a reason gives a code is the ICD-O-3.2 Preferred term, read from
icdo32.sqlite when the trees are built (term()), never typed.

Tree `topography` values are author-facing documentation. The validator reads them only for
Groups 3 and 4, so this file writes the Group 8 range format, converted from the ICCC-2017
range strings in TOPOGRAPHY_RAW. g10_site_unstated owns no topography: it is the router's
default and the search box's entry, so its list is empty.
"""
from __future__ import annotations

import copy
import os
import sqlite3
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_DEFAULT_ICDO = REPO.parents[1] / "ICD coding" / "ICD-O-3.2" / "icdo32.sqlite"
_PREFERRED: dict | None = None


class TreeError(Exception):
    """A tree names a (code, behaviour) ICD-O-3.2 does not carry, or Layer 1 is absent."""


def _icdo_path() -> Path:
    return Path(os.environ.get("ICDO_DB", str(_DEFAULT_ICDO)))


def term(code: str, beh: str) -> str:
    """The ICD-O-3.2 Preferred term at (code, behaviour), from icdo32.sqlite."""
    global _PREFERRED
    if _PREFERRED is None:
        path = _icdo_path()
        if not path.exists():
            raise TreeError("icdo32.sqlite not found at %s — set ICDO_DB" % path)
        con = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
        try:
            index: dict = {}
            for c, b, t in con.execute(
                    "SELECT code4, behaviour, term FROM icd_o_3_2_morphology "
                    "WHERE level = 'Preferred' AND code4 IS NOT NULL AND behaviour IS NOT NULL"):
                key = (str(c), str(b))
                if key in index and index[key] != t:
                    raise TreeError("icdo32.sqlite carries two Preferred terms at %s/%s" % key)
                index[key] = str(t)
        finally:
            con.close()
        _PREFERRED = index
    try:
        return _PREFERRED[(code, beh)]
    except KeyError:
        raise TreeError("ICD-O-3.2 has no Preferred term at %s/%s" % (code, beh)) from None


# ------------------------------------------------------------------------------------------
# Shared wording
# ------------------------------------------------------------------------------------------
VISSER = "Visser 2023, European Network of Cancer Registries"
SIEGMUND = "Siegmund 2022"
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

BEH_TEXT = {"0": "behaviour 0, benign", "1": "behaviour 1, uncertain or borderline",
            "2": "behaviour 2, in situ"}
OUTSIDE_CNS = ("Outside the central nervous system ICCC-3 Group X registers behaviour 3 "
               "(malignant) only, so no Group X code is recorded.")
SETTLED = " Whether the registry records it elsewhere is the registrar's decision."
PENDING = " This exclusion awaits the registrar's decision."

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
         "clinical_alert": None, "coding_note": note, "captured_variables": captured}
    if options is not None:
        n["options"] = options
    n.update(extra)
    n.setdefault("nos_fallback", None)
    return n


# ------------------------------------------------------------------------------------------
# Sites
# ------------------------------------------------------------------------------------------
GONADS = ("ovary", "testis")
SITES = {
    "cns": {"prefix": "cn_", "tree": "g10_cns", "family": "9064",
            "where": "the brain or spinal cord", "fluid": "cerebrospinal fluid"},
    "ovary": {"prefix": "ov_", "tree": "g10_ovary", "family": "9060",
              "where": "the ovary", "fluid": "ascitic fluid or a fine-needle aspirate"},
    "testis": {"prefix": "ts_", "tree": "g10_testis", "family": "9061",
               "where": "the testis", "fluid": "a fine-needle aspirate"},
    "extragonadal": {"prefix": "eg_", "tree": "g10_extragonadal", "family": "9064",
                     "where": "this site", "fluid": "an effusion or a fine-needle aspirate"},
}
# The name a site's germinoma-family report uses for the family code (D3).
FAMILY_TERM = {"cns": "germinoma", "ovary": "dysgerminoma", "testis": "seminoma",
               "extragonadal": "germinoma"}


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
TIER_NODE = {"referral": "clinical_alias", "markers": "markers", "imaging": "imaging",
             "cytology": "cytology", "histology": "histology"}


def n_document_inventory(node_id, targets, note):
    return node(
        node_id, "document_inventory", 1, "Evidence in file",
        "What is in the file for this tumour?",
        "Pick the highest tier of evidence in the file. A radiology report counts as imaging. "
        "A pathology report on a biopsy or resection counts as histology.",
        [go(TIER_LABELS[t], targets[t], copy.deepcopy(TIER_CAPTURES[t])) for t in TIERS],
        EVIDENCE_TIER, note)


def n_clinical_alias(site):
    return node(
        nid(site, "clinical_alias"), "clinical_alias", 2, "Referral wording",
        "What does the referral letter or clinical note say?",
        "No imaging report, marker result or tissue report is in the file. A note alone never "
        "establishes a germ cell tumour's type.",
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
            go("An imaging report is in the file after all", nid(site, "imaging"),
               copy.deepcopy(TIER_CAPTURES["imaging"])),
        ],
        EVIDENCE_TIER,
        "Contract §4.2. Visser O, et al. Frontiers in Oncology 2023;13:1250549, rules 4 and 5, "
        "p. 03: 8000/3 at basis 1 when cancer is at least probable. 8000/3 is Group X only at "
        "the gonads (ICCC-2017 range 117); elsewhere the branch refers (D4).")


def n_markers(site):
    opts = [
        code("Imaging shows a tumour and the report calls alpha-fetoprotein raised, with or "
             "without human chorionic gonadotropin", "9065", "3", 4,
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
            "Imaging shows a tumour of the uterus or placenta after a pregnancy, and the "
            "report calls human chorionic gonadotropin raised", "9100", "3", 4,
            "%s Choriocarcinoma of the placenta with a raised human chorionic gonadotropin is "
            "registered to this code without tissue (%s, Table 4)." % (rec("9100", "3", 4),
                                                                       VISSER),
            {"workup_status": "incomplete", "basis_evidence_tier": "markers_hcg_gestational"},
            note="D4, extragonadal tree only. Visser Table 4, p. 06."))
    opts += [
        code("Imaging shows a tumour and the report calls human chorionic gonadotropin raised; "
             "alpha-fetoprotein is normal or not measured", "9064", "3", 4,
             "%s ICD-O-3.2 files Germ cell tumor, NOS under this number, and a germ cell "
             "tumour with a raised human chorionic gonadotropin is registered to it without "
             "tissue (%s, Table 4). The record does not assert that a germinoma was diagnosed; "
             "a histology report gives the type." % (rec("9064", "3", 4), VISSER),
             {"workup_status": "incomplete", "basis_evidence_tier": "markers_hcg"},
             note="D2, D4. Visser Table 4, p. 06."),
        go("Neither marker is raised", nid(site, "imaging"),
           {"basis_evidence_tier": "markers_not_raised"}),
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
        "These codes apply to a tumour the file calls a germ cell tumour (%s, Table 4)."
        % VISSER,
        opts, EVIDENCE_TIER,
        "D4. The report's own statement against the age-specific range is read; nothing is "
        "re-gated numerically (Group III's md_gct_* gates stay in Group III).")


def n_imaging(site):
    return node(
        nid(site, "imaging"), "morphology_only", 2, "Imaging conclusion",
        "No tissue is in the file. What does the imaging report conclude?",
        "Answer from the radiologist's own conclusion. Imaging alone never establishes a germ "
        "cell tumour's type.",
        [
            unspecified(site, "Imaging shows a malignant tumour, at least probable", 2, "8000",
                        "Imaging alone does not establish a germ cell tumour (%s, rule 5)."
                        % VISSER,
                        {"evidence_tests": ["Imaging"], "workup_status": "incomplete",
                         "basis_evidence_tier": "imaging_malignant"},
                        after="A histology report gives the specific code."),
            nonrep("Imaging calls it possible only, or describes a benign lesion",
                   NOT_REGISTRABLE_POSSIBLE,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "imaging_nondiagnostic"}),
            go("A histology report is in the file", nid(site, "histology"),
               {"evidence_tests": ["Imaging", "Histology"], "workup_status": "incomplete",
                "basis_evidence_tier": "histology"}),
            go("No imaging report in the file either — only a referral letter or clinical note",
               nid(site, "clinical_alias"), copy.deepcopy(TIER_CAPTURES["referral"]),
               note="Reached from non-diagnostic cytology with no imaging report. Without this "
                    "option the only code here claims imaging as evidence (Group 8 "
                    "bn_imaging_line precedent)."),
        ],
        EVIDENCE_TIER,
        "D4. Visser 2023 has no germ cell row in Table 3, so imaging alone is 8000/3 at basis 2 "
        "(rule 5, p. 03); in the central nervous system and at extragonadal sites that code is "
        "not Group X and the branch refers.")


def n_cytology(site):
    fam = SITES[site]["family"]
    opts = [code("Cytology names %s" % FAMILY_TERM[site], fam, "3", 5,
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
        go("No malignant cells, scant material, or a non-diagnostic report",
           nid(site, "imaging"),
           {"workup_status": "incomplete", "basis_evidence_tier": "cytology_nondiagnostic"},
           note="Non-diagnostic cytology leaves imaging as the best evidence."),
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
    opts = [
        code("Choriocarcinoma is one of the components", "9101", "3", 7, rec("9101")),
        code("Embryonal carcinoma and teratoma, and nothing else", "9081", "3", 7,
             "%s ICD-O-3.2 gives it the synonym Mixed embryonal carcinoma and teratoma."
             % rec("9081")),
        code("The report uses the term teratocarcinoma", "9081", "3", 7, rec("9081")),
        code("The report uses the term malignant teratoma, undifferentiated (or anaplastic)",
             "9082", "3", 7, rec("9082")),
        code("The report uses the term malignant teratoma, intermediate", "9083", "3", 7,
             rec("9083")),
    ]
    if site in GONADS:
        opts.append(code("The report uses the term malignant teratoma, trophoblastic", "9102",
                         "3", 7, rec("9102"),
                         note="D6. ICCC-2017 range 110 (Xc5) only: ovary and testis."))
    if site == "extragonadal":
        opts.append(code("A germ cell tumour with an associated haematological malignancy",
                         "9086", "3", 7,
                         "%s The haematological malignancy is coded separately, from its own "
                         "group." % rec("9086"),
                         note="D17. New in ICD-O-3.2; ICCC-2017 range 105 (Xb6) only."))
    opts += [
        code("Teratoma and seminoma, germinoma or dysgerminoma", "9085", "3", 7,
             "%s ICD-O-3.2 gives it the related term Mixed teratoma and seminoma."
             % rec("9085")),
        code("Any other combination, or the components are not listed", "9085", "3", 7,
             rec("9085")),
    ]
    return node(
        nid(site, "mixed"), "histology_subclassification", 3, "Mixed germ cell tumour",
        "Which components does the report list?",
        "Where the report uses one of the named terms below, choose it. Otherwise choose by "
        "the components the report lists.",
        opts, [],
        "D6. WHO 2022 (Moch 2022, Table 3, p. 464) codes every mixture 9085/3; ICD-O-3.2 keeps "
        "the specific terms, coded as written (Group 8 D8 precedent). 9102/3 is ovary and "
        "testis only (range 110); 9086/3 extragonadal only (range 105).")


IHC_MARKER_GROUPS = [
    {"group_label": "Germ cell lineage", "markers": ["SALL4", "OCT3/4"]},
    {"group_label": "Seminoma, dysgerminoma and germinoma",
     "markers": ["CD117", "SOX17", "D2-40"]},
    {"group_label": "Embryonal carcinoma", "markers": ["CD30", "SOX2"]},
    {"group_label": "Yolk sac tumour",
     "markers": ["Glypican-3", "Alpha-fetoprotein (tissue stain)", "HNF1-beta"]},
]


def n_ihc(site):
    fam = SITES[site]["family"]
    fam_reason = ("Dysgerminoma, seminoma and germinoma are one tumour under three names (Moch "
                  "2022, p. 464), and the name this site uses is recorded. %s" % rec(fam))
    rules = [
        code(["OCT3/4", "CD30"], "9070", "3", 7,
             "OCT3/4 and CD30 are positive, and the seminoma markers CD117 and SOX17 are not: "
             "the embryonal carcinoma pattern (%s, p. 37). %s" % (SIEGMUND, rec("9070")),
             satisfies=["IHC"], key="positive", negative=["CD117", "SOX17"],
             note="Rule 1. Siegmund 2022 p. 37: CD30 stains embryonal carcinoma (83-100%) and "
                  "focally stains 0-50% of seminomas; CD30+/KIT- is 100% specific for "
                  "embryonal carcinoma (Leroy). OCT3/4 marks seminoma and embryonal carcinoma "
                  "(100% each, p. 37). negative CD117 and SOX17: added to the contract's rule, "
                  "so a seminoma with focal CD30 is not coded embryonal carcinoma. SOX17 is "
                  "negative in 100% of embryonal carcinomas (Nonaka, p. 37)."),
        code(["OCT3/4", "SOX2"], "9070", "3", 7,
             "OCT3/4 and SOX2 are positive and SOX17 is not: the embryonal carcinoma pattern "
             "(%s, p. 37). %s" % (SIEGMUND, rec("9070")),
             satisfies=["IHC"], key="positive", negative=["SOX17"],
             note="Rule 2. Siegmund 2022 p. 37 (Nonaka): diffuse SOX2 with negative SOX17 in "
                  "100% of embryonal carcinomas; diffuse SOX17 with negative SOX2 in 100% of "
                  "seminomas. SOX2 in teratoma epithelium (up to 81%) is excluded by OCT3/4, "
                  "which teratoma lacks (Table 1, p. 34)."),
        code(["OCT3/4", "CD117"], fam, "3", 7,
             "OCT3/4 and CD117 are positive and CD30 is not: the seminoma pattern (%s, pp. "
             "36-37). %s" % (SIEGMUND, fam_reason),
             satisfies=["IHC"], key="positive", negative=["CD30"],
             note="Rule 3. Siegmund 2022 p. 36: KIT stains 88-100% of seminomas; focal "
                  "cytoplasmic KIT occurs in 32-44% of non-seminomatous tumours. p. 37: "
                  "CD30-/KIT+ is 100% specific for seminoma (Leroy). negative CD30: added to "
                  "the contract's rule for the same reason as rule 1. Family code by site, D3."),
        code(["OCT3/4", "SOX17"], fam, "3", 7,
             "OCT3/4 and SOX17 are positive: the seminoma pattern. Embryonal carcinoma does "
             "not express SOX17 (%s, p. 37). %s" % (SIEGMUND, fam_reason),
             satisfies=["IHC"], key="positive",
             note="Rule 4. Siegmund 2022 p. 37 (Nonaka): SOX17 diffuse in 100% of seminomas, "
                  "negative in 100% of embryonal carcinomas and in choriocarcinoma; variable "
                  "in yolk sac tumour and teratoma, both OCT3/4 negative (Table 1, p. 34)."),
        code(["OCT3/4", "D2-40"], fam, "3", 7,
             "OCT3/4 and D2-40 are positive and CD30 is not: the seminoma pattern (%s, pp. "
             "36-37). %s" % (SIEGMUND, fam_reason),
             satisfies=["IHC"], key="positive", negative=["CD30"],
             note="Rule 5. Siegmund 2022 p. 36: D2-40 strongly stains up to 100% of seminomas; "
                  "embryonal carcinoma stains in 0-69%, focally. negative CD30: added to the "
                  "contract's rule, so focal D2-40 in an embryonal carcinoma does not read as "
                  "seminoma. p. 37: KIT/D2-40/SOX17 mark seminoma, CD30/SOX2 embryonal "
                  "carcinoma."),
        code(["Glypican-3"], "9071", "3", 7,
             "Glypican-3 is positive and OCT3/4 is not: the yolk sac tumour pattern (%s, p. 38; "
             "Wu 2020, Table 2). %s" % (SIEGMUND, rec("9071")),
             satisfies=["IHC"], key="positive", negative=["OCT3/4"],
             note="Rule 6. Siegmund 2022 p. 38: glypican-3 in 100% of yolk sac tumours, not "
                  "detected in seminoma; choriocarcinoma 33-100%, teratoma 20-38%, embryonal "
                  "carcinoma 0-8%. Wu P, et al. Pediatr Surg Int 2020 "
                  "(doi:10.1007/s00383-020-04652-w; the PDF prints no page numbers), Table 2: "
                  "22/22 paediatric yolk sac tumours, 1/10 mature teratomas (weak, 3% of "
                  "cells). OCT3/4 negative in yolk sac tumour, Table 1, p. 34."),
        code(["Alpha-fetoprotein (tissue stain)"], "9071", "3", 7,
             "Alpha-fetoprotein stains the tumour and OCT3/4 is not positive: the yolk sac "
             "tumour pattern (%s, p. 38; Wu 2020, Table 1). %s" % (SIEGMUND, rec("9071")),
             satisfies=["IHC"], key="positive", negative=["OCT3/4"],
             note="Rule 7. Siegmund 2022 p. 38: tissue alpha-fetoprotein in 55-100% of yolk "
                  "sac tumours, patchy; embryonal carcinoma 21% (OCT3/4 positive, excluded); "
                  "teratoma 0-27%. Wu 2020 Table 1: 21/22 paediatric yolk sac tumours, 2/10 "
                  "mature teratomas weakly (2% of cells)."),
        code(["HNF1-beta"], "9071", "3", 7,
             "HNF1-beta is positive and OCT3/4 is not: the yolk sac tumour pattern (Rougemont "
             "2018, p. 26; %s, p. 38). %s" % (SIEGMUND, rec("9071")),
             satisfies=["IHC"], key="positive", negative=["OCT3/4"],
             note="Rule 8. Rougemont AL, Tille JC. Human Pathology 2018;81:26-36, p. 26: "
                  "nuclear HNF1-beta in the yolk sac component of 49/49 tumours; embryonal "
                  "carcinoma 0/32 and seminoma 0/6 negative; choriocarcinoma cytoplasmic only; "
                  "enteric-type teratoma glands 11/16 (specificity 80%). p. 31: every yolk sac "
                  "tumour SALL4 positive and OCT4 negative. Table 5, p. 33."),
    ]
    return node(
        nid(site, "ihc"), "ihc_checklist", 4, "Germ cell stain panel",
        "Answer each stain as the report states it.",
        "The report calls the tumour a germ cell tumour without naming its type. Answer 'Not "
        "done or not readable' for a stain the report does not mention. A tumour with more than "
        "one germ cell component is coded at the mixed germ cell tumour step instead. Human "
        "chorionic gonadotropin staining does not establish choriocarcinoma: it also stains the "
        "syncytiotrophoblastic cells found in seminoma (%s, p. 38)." % SIEGMUND,
        None, [],
        "Contract §4.2, each rule verified against the printed page. Siegmund SE, Mehra R, "
        "Acosta AM. Human Pathology 2023;133:32-55 (online 2022): Table 1, p. 34; KIT and "
        "D2-40, p. 36; CD30, OCT3/4, SOX2 and SOX17, p. 37; glypican-3, alpha-fetoprotein, "
        "human chorionic gonadotropin and HNF1-beta, p. 38. Wu 2020, Tables 1-3. Rougemont "
        "2018, pp. 26, 31, 33. All eight contract rules are kept; rules 1, 3 and 5 carry "
        "negatives the contract's table did not, so a panel with markers of both seminoma and "
        "embryonal carcinoma falls to the fallback instead of a definite type. SALL4 is "
        "declared and asked by no rule: it marks germ cell lineage, not type (Siegmund p. 36). "
        "Choriocarcinoma is not coded from immunohistochemistry (contract §4.2). Fallback "
        "9064/3 per D2.",
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
# Histology (§4.3)
# ------------------------------------------------------------------------------------------
def named(label, morph, reason=None, upgrade=None, note=None):
    """A histology report naming the type, basis 7."""
    return code(label, morph, "3", 7, reason or rec(morph), upgrade=upgrade, note=note)


def untyped_gct(site):
    return [
        go("Germ cell tumour, type not named, with immunostains listed", nid(site, "ihc")),
        code("Germ cell tumour, type not named, and no immunostains listed", "9064", "3", 7,
             "%s ICD-O-3.2 files Germ cell tumor, NOS under this number, so the record does "
             "not assert that a germinoma was diagnosed." % rec("9064"), note="D2."),
    ]


def histology_node(site, options, note):
    return node(
        nid(site, "histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        "Use the report's own term for the tumour.",
        options, [], note)


def n_histology_cns():
    s = "cns"
    return histology_node(s, [
        named("Germinoma", "9064", upgrade=IHC_CONFIRMS),
        code("Mature teratoma", "9080", "0", 7,
             "%s In the central nervous system ICCC-3 Group X registers behaviours 0, 1 and 3."
             % rec("9080", "0"), note="D5. ICCC-2017 range 95 (Xa2) declares 0-1,3."),
        named("Immature teratoma", "9080",
              "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
              note="D5. The pathway's 9083 for immature teratoma is wrong; 9083/3 is "
                   "Malignant teratoma, intermediate."),
        code("Teratoma, with maturity not stated", "9080", "1", 7,
             "%s In the central nervous system ICCC-3 Group X registers behaviours 0, 1 and 3."
             % rec("9080", "1"), note="D5."),
        code("Dermoid cyst", "9084", "0", 7,
             "%s In the central nervous system ICCC-3 Group X registers behaviours 0, 1 and 3."
             % rec("9084", "0"), note="D5."),
        named("Teratoma with a somatic-type malignancy", "9084",
              "%s ICD-O-3.2 gives it the synonym Teratoma with somatic type malignancies."
              % rec("9084"), note="D5. Louis 2021 Table 1, p. 1235."),
        named("Embryonal carcinoma", "9070", upgrade=IHC_CONFIRMS),
        named("Polyembryoma", "9072", note="D7."),
        named("Yolk sac tumour (endodermal sinus tumour)", "9071", upgrade=IHC_CONFIRMS),
        named("Choriocarcinoma", "9100", note="D8."),
        go("Mixed germ cell tumour — more than one germ cell component", nid(s, "mixed")),
    ] + untyped_gct(s) + [
        refer("Not a germ cell tumour", 3,
              "A tumour of the brain or spinal cord that is not a germ cell tumour belongs to "
              "ICCC-3 Group III. Code the case from the Group III (central nervous system "
              "tumours) tree."),
    ], "Contract §4.3. Louis 2021 Table 1, p. 1235 for the central nervous system germ cell "
       "entities. Behaviours 0 and 1 are Group X codes here (ICCC-2017 ranges 94-99).")


def n_histology_ovary():
    s = "ovary"
    return histology_node(s, [
        named("Dysgerminoma", "9060", upgrade=IHC_CONFIRMS, note="D1, D3."),
        named("Germinoma", "9064",
              "%s A report that uses the term germinoma is coded as written; dysgerminoma is "
              "9060/3." % rec("9064"), upgrade=IHC_CONFIRMS, note="D1."),
        named("Yolk sac tumour (endodermal sinus tumour)", "9071", upgrade=IHC_CONFIRMS),
        named("Embryonal carcinoma", "9070", upgrade=IHC_CONFIRMS),
        named("Polyembryoma", "9072", note="D7."),
        named("Non-gestational choriocarcinoma", "9100", note="D8."),
        go("A teratoma, struma ovarii or strumal carcinoid", nid(s, "teratoma")),
        go("Mixed germ cell tumour — more than one germ cell component", nid(s, "mixed")),
        go("Gonadoblastoma, alone or with another tumour", nid(s, "gonadoblastoma")),
    ] + untyped_gct(s) + [
        go("A sex cord–stromal tumour — granulosa cell, Sertoli-Leydig cell, Sertoli cell, "
           "Leydig cell, steroid cell, thecoma or another", nid(s, "sex_cord")),
        go("An epithelial tumour — carcinoma, borderline tumour or cystadenoma",
           nid(s, "epithelial")),
        named("Small cell carcinoma, hypercalcaemic type", "8044",
              "%s ICD-O-3.2 gives Small cell carcinoma, hypercalcemic type as a related term of "
              "this code." % rec("8044"), note="D14."),
        go("Malignant tumour, type not determined", nid(s, "unspecified")),
        go("Another tumour type — lymphoma, leukaemia, sarcoma, a metastatic deposit or "
           "another named tumour", nid(s, "other")),
    ], "Contract §4.3. ICD-O-3.2 for every ovarian code; Pfister 2022 Table 3, p. 342, for "
       "paediatric entity currency (D22: no ovary baseline paper on disk).")


def n_histology_testis():
    s = "testis"
    return histology_node(s, [
        named("Seminoma", "9061", upgrade=IHC_CONFIRMS, note="D3."),
        named("Seminoma, anaplastic or with a high mitotic index", "9062",
              "%s ICD-O-3.2 gives it the synonym Seminoma with high mitotic index."
              % rec("9062"), note="D3."),
        named("Spermatocytic tumour", "9063",
              "%s ICD-O-3.2 gives it the synonym Spermatocytic tumor." % rec("9063"),
              note="D3. Moch 2022 Table 3, p. 464."),
        named("Embryonal carcinoma", "9070", upgrade=IHC_CONFIRMS),
        named("Polyembryoma", "9072", note="D7."),
        named("Yolk sac tumour, prepubertal or postpubertal type", "9071",
              "%s WHO 2022 codes both types 9071/3 (Moch 2022, Table 3, p. 464)."
              % rec("9071"), upgrade=IHC_CONFIRMS),
        named("Choriocarcinoma", "9100", note="D8."),
        named("Epithelioid trophoblastic tumour", "9105", note="D8. Moch 2022 Table 3, p. 464."),
        excl("Placental site trophoblastic tumour", "9104", "1", PSTT_REASON, decision=True,
             note="D8, provisional: the Group 8 9222 pattern."),
        go("A teratoma, dermoid cyst or epidermoid cyst", nid(s, "teratoma")),
        go("Mixed germ cell tumour — more than one germ cell component", nid(s, "mixed")),
        excl_outside("Germ cell neoplasia in situ only, with no invasive tumour",
                     "germ cell neoplasia in situ", "9064", "2",
                     extra="WHO 2022 lists it among the non-invasive germ cell lesions (Moch "
                           "2022, Table 3, p. 464).",
                     note="D9, settled. Moch's intratubular 9061/2, 9070/2, 9071/2 and 9080/2 "
                          "are not ICD-O-3.2 codes; a report of any of them is this exclusion."),
        go("Gonadoblastoma, alone or with another tumour", nid(s, "gonadoblastoma")),
    ] + untyped_gct(s) + [
        go("A sex cord–stromal tumour — Leydig cell, Sertoli cell, granulosa cell or another",
           nid(s, "sex_cord")),
        named("Carcinoma", "8010",
              "%s Where the report names the carcinoma's type, search for that type's own "
              "code." % rec("8010"), note="D14: the testis tree offers 8010/3 only."),
        go("Malignant tumour, type not determined", nid(s, "unspecified")),
        go("Another tumour type — lymphoma, leukaemia, sarcoma, a metastatic deposit or "
           "another named tumour", nid(s, "other")),
    ], "Contract §4.3. Moch H, et al. European Urology 2022;82(5):458-468, Table 3, "
       "pp. 464-465, is the testis baseline.")


PSTT_REASON = (
    "ICD-O-3.2 codes placental site trophoblastic tumour 9104/1, behaviour 1, uncertain or "
    "borderline. WHO 2022 prints 9104/3, a code approved after ICD-O-3.2 (Moch 2022, Table 3, "
    "pp. 464-465). The case is not recorded as a Group X cancer until the registrar rules.")


def n_histology_extragonadal():
    s = "extragonadal"
    return histology_node(s, [
        named("Germinoma", "9064", upgrade=IHC_CONFIRMS, note="D1."),
        named("Seminoma", "9061", upgrade=IHC_CONFIRMS, note="D3: coded as written."),
        go("A teratoma or dermoid cyst", nid(s, "teratoma")),
        named("Yolk sac tumour (endodermal sinus tumour)", "9071", upgrade=IHC_CONFIRMS),
        named("Embryonal carcinoma", "9070", upgrade=IHC_CONFIRMS),
        named("Polyembryoma", "9072", note="D7."),
        named("Choriocarcinoma, gestational or non-gestational", "9100", note="D8."),
        named("Epithelioid trophoblastic tumour", "9105", note="D8."),
        excl("Placental site trophoblastic tumour", "9104", "1", PSTT_REASON, decision=True,
             note="D8, provisional."),
        excl_outside("Complete hydatidiform mole", "complete hydatidiform mole", "9100", "0",
                     note="D8, settled."),
        excl_outside("Partial hydatidiform mole", "partial hydatidiform mole", "9103", "0",
                     note="D8, settled."),
        excl_outside("Invasive mole", "invasive mole", "9100", "1", note="D8, settled."),
        go("Mixed germ cell tumour — more than one germ cell component", nid(s, "mixed")),
    ] + untyped_gct(s) + [
        go("Not a germ cell or trophoblastic tumour", nid(s, "other")),
    ], "Contract §4.3. ICCC-2017 ranges 100-105 (Xb), behaviour 3 only. The p57 and "
       "genotyping algorithm for moles is not built: every outcome is an exclusion (D8).")


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
            excl_outside("Mature cystic teratoma (mature teratoma)",
                         "mature cystic teratoma", "9080", "0", note="D5, settled."),
            excl_outside("Dermoid cyst", "dermoid cyst", "9084", "0", note="D5, settled."),
            named("Immature teratoma, any grade", "9080",
                  "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
                  note="D5."),
            excl_outside("Teratoma, with maturity not stated", "a teratoma whose maturity is "
                         "not stated", "9080", "1", note="D5, settled."),
            named("Teratoma or dermoid cyst with a somatic-type malignancy (a carcinoma or "
                  "sarcoma arising in it)", "9084",
                  "%s ICD-O-3.2 gives it the synonym Dermoid cyst with malignant "
                  "transformation." % rec("9084"), note="D5."),
            excl_outside("Struma ovarii", "struma ovarii", "9090", "0", note="D5, settled."),
            named("Malignant struma ovarii", "9090",
                  note="D5. ICCC-2017 range 107 (Xc2)."),
            excl_outside("Strumal carcinoid", "strumal carcinoid", "9091", "1",
                         extra="ICD-O-3.2 has no malignant code for it.",
                         note="D5, settled: ICD-O-3.2 has no 9091/3."),
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
            excl_outside("Dermoid cyst or epidermoid cyst", "a dermoid cyst", "9084", "0",
                         extra="WHO 2022 codes dermoid and epidermoid cysts of the testis "
                               "9084/0 (Moch 2022, Table 3, p. 464).",
                         note="D5, settled."),
            named("Teratoma, postpubertal type", "9080",
                  "%s WHO 2022 codes postpubertal-type teratoma 9080/3 (Moch 2022, Table 3, "
                  "p. 464)." % rec("9080"), note="D5."),
            named("Immature teratoma", "9080",
                  "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
                  note="D5."),
            excl_outside("Mature teratoma, with prepubertal or postpubertal type not stated",
                         "mature teratoma", "9080", "0", note="D5, settled."),
            excl_outside("Teratoma, with maturity and type not stated",
                         "a teratoma whose type is not stated", "9080", "1",
                         note="D5, settled."),
            named("Teratoma with a somatic-type malignancy", "9084",
                  "%s ICD-O-3.2 gives it the synonym Teratoma with somatic type malignancies."
                  % rec("9084"), note="D5. Moch 2022 Table 3, p. 464."),
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
            excl_outside("Mature teratoma", "mature teratoma", "9080", "0",
                         note="D5, settled."),
            excl_outside("Immature teratoma of the lung, thymus or thyroid",
                         "immature teratoma of the lung, thymus or thyroid", "9080", "1",
                         decision=True,
                         extra="ICD-O-3.2 lists the change in 'Terms that are changing "
                               "behaviour', p. 6.",
                         note="D5: the thymus part is provisional. A mediastinal immature "
                              "teratoma recorded at C38.1 is 9080/3 by the same rule."),
            named("Immature teratoma at any other site — sacrococcygeal region, mediastinum "
                  "outside the thymus, retroperitoneum or elsewhere", "9080",
                  "%s ICD-O-3.2 gives it the synonym Immature teratoma, NOS." % rec("9080"),
                  note="D5."),
            excl_outside("Teratoma, with maturity not stated",
                         "a teratoma whose maturity is not stated", "9080", "1",
                         note="D5, settled."),
            excl_outside("Dermoid cyst", "dermoid cyst", "9084", "0", note="D5, settled."),
            named("Teratoma with a somatic-type malignancy", "9084",
                  "%s ICD-O-3.2 gives it the synonym Teratoma with somatic type malignancies."
                  % rec("9084"), note="D5."),
            go("Teratoma with a yolk sac tumour or another malignant germ cell component",
               nid(s, "mixed")),
        ],
        [], "Contract §4.4, D5.")


def n_gonadoblastoma(site):
    family_label = {"ovary": "dysgerminoma", "testis": "seminoma"}[site]
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
            named("Gonadoblastoma with an invasive %s" % family_label, SITES[site]["family"],
                  upgrade=IHC_CONFIRMS, note="D10, D3."),
            named("Gonadoblastoma with an invasive germinoma", "9064",
                  "%s A report that uses the term germinoma is coded as written." % rec("9064"),
                  upgrade=IHC_CONFIRMS,
                  note="D1, D10. The contract's single 'dysgerminoma, seminoma or germinoma' "
                       "option is split so a report that says germinoma gets 9064/3 (D1)."),
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

    def x(label, what, icdo, beh, decision=False, extra=""):
        return excl_outside(label, what, icdo, beh, decision=decision, extra=extra,
                            note="D11%s." % (", D12: provisional" if decision else ", settled"))
    return node(
        nid(s, "sex_cord"), "histology_subclassification", 4, "Sex cord–stromal tumour",
        "Which sex cord–stromal tumour does the report diagnose?",
        "Use the report's own term, including the Sertoli-Leydig cell tumour's "
        "differentiation.",
        [
            named("Adult granulosa cell tumour", "8620",
                  "%s ICD-O-3.2 changed the behaviour of the adult granulosa cell tumour of the "
                  "ovary from 1 to 3." % rec("8620"),
                  note="D11. 'Terms that are changing behaviour', p. 4."),
            x("Juvenile granulosa cell tumour", "juvenile granulosa cell tumour", "8622", "1",
              decision=True),
            named("Sertoli-Leydig cell tumour, poorly differentiated", "8631", note="D11."),
            named("Sertoli-Leydig cell tumour, poorly differentiated, with heterologous "
                  "elements", "8634", note="D11."),
            x("Sertoli-Leydig cell tumour, intermediate differentiation",
              "Sertoli-Leydig cell tumour of intermediate differentiation", "8631", "1"),
            x("Sertoli-Leydig cell tumour, intermediate differentiation, with heterologous "
              "elements", "Sertoli-Leydig cell tumour of intermediate differentiation with "
              "heterologous elements", "8634", "1"),
            x("Sertoli-Leydig cell tumour, well differentiated",
              "well-differentiated Sertoli-Leydig cell tumour", "8631", "0"),
            x("Sertoli-Leydig cell tumour, retiform", "retiform Sertoli-Leydig cell tumour",
              "8633", "1"),
            x("Sertoli-Leydig cell tumour, differentiation not stated",
              "Sertoli-Leydig cell tumour, NOS", "8631", "1"),
            x("Sertoli cell tumour", "Sertoli cell tumour", "8640", "1"),
            named("Malignant Sertoli cell tumour, or Sertoli cell carcinoma", "8640",
                  note="D11."),
            x("Leydig cell tumour", "Leydig cell tumour of the ovary", "8650", "0"),
            named("Malignant Leydig cell tumour", "8650", note="D11."),
            x("Steroid cell tumour", "steroid cell tumour", "8670", "0"),
            named("Malignant steroid cell tumour", "8670", note="D11."),
            x("Thecoma", "thecoma", "8600", "0"),
            named("Malignant thecoma", "8600", note="D11."),
            x("Gynandroblastoma", "gynandroblastoma", "8632", "1"),
            x("Sex cord tumour with annular tubules", "sex cord tumour with annular tubules",
              "8623", "1"),
            x("Microcystic stromal tumour or signet-ring stromal tumour",
              "microcystic and signet-ring stromal tumours", "8590", "0"),
            x("Sex cord–stromal tumour, type not stated", "a sex cord-stromal tumour of "
              "unstated type", "8590", "1", decision=True),
        ],
        [], "D11 by ICD-O-3.2. Juvenile granulosa cell tumour, the commonest sex cord-stromal "
            "tumour of childhood, is not registrable under ICCC-2017 (D11's registrar "
            "question). D12: no /3 that ICD-O-3.2 does not print. FOXL2 and DICER1 change no "
            "code and are not asked (D11).")


def n_sex_cord_testis():
    s = "testis"

    def x(label, what, icdo, beh, decision=False):
        return excl_outside(label, what, icdo, beh, decision=decision,
                            note="D11%s." % (", D12: provisional" if decision else ", settled"))
    return node(
        nid(s, "sex_cord"), "histology_subclassification", 4, "Sex cord–stromal tumour",
        "Which sex cord–stromal tumour does the report diagnose?",
        "Use the report's own term. Choose a malignant option only where the report calls "
        "the tumour malignant.",
        [
            x("Leydig cell tumour", "Leydig cell tumour of the testis", "8650", "1"),
            named("Malignant Leydig cell tumour", "8650", note="D11. Moch 2022 Table 3, "
                                                               "p. 464."),
            x("Sertoli cell tumour", "Sertoli cell tumour", "8640", "1"),
            named("Malignant Sertoli cell tumour", "8640", note="D11. Moch 2022 Table 3, "
                                                                "p. 465."),
            x("Large cell calcifying Sertoli cell tumour",
              "large cell calcifying Sertoli cell tumour", "8642", "1"),
            x("Adult granulosa cell tumour", "adult granulosa cell tumour of the testis",
              "8620", "1"),
            x("Juvenile granulosa cell tumour", "juvenile granulosa cell tumour of the testis",
              "8622", "0", decision=True),
            named("Sertoli-Leydig cell tumour, poorly differentiated", "8631", note="D11."),
            x("Mixed or unclassified sex cord–stromal tumour",
              "a mixed sex cord-stromal tumour", "8592", "1"),
            x("Sex cord–stromal tumour, type not stated", "a sex cord-stromal tumour of "
              "unstated type", "8590", "1", decision=True),
        ],
        [], "D11. Moch 2022 Table 3, pp. 464-465: Leydig 8650/1, malignant 8650/3; Sertoli "
            "8640/1, malignant 8640/3; large cell calcifying 8642/1; adult granulosa 8620/1; "
            "juvenile granulosa 8622/0; mixed 8592/1; NOS 8590/1.")


def n_epithelial_ovary():
    s = "ovary"

    def x(label, what, icdo, beh):
        return excl_outside(label, what, icdo, beh, decision=True,
                            note="D14, provisional.")
    return node(
        nid(s, "epithelial"), "histology_subclassification", 4, "Epithelial tumour",
        "Which epithelial tumour does the report diagnose?",
        "Use the report's own term. Borderline tumours and cystadenomas are not malignant.",
        [
            named("Small cell carcinoma, hypercalcaemic type", "8044",
                  "%s ICD-O-3.2 gives Small cell carcinoma, hypercalcemic type as a related "
                  "term of this code." % rec("8044"), note="D14."),
            named("Low-grade serous carcinoma", "8460", note="D14."),
            named("High-grade serous carcinoma", "8461", note="D14."),
            named("Serous carcinoma, grade not stated", "8441", note="D14."),
            named("Mucinous carcinoma", "8480",
                  "%s ICD-O-3.2 gives it the synonym Mucinous carcinoma." % rec("8480"),
                  note="D14."),
            named("Mucinous cystadenocarcinoma", "8470", note="D14."),
            named("Endometrioid carcinoma", "8380", note="D14."),
            named("Clear cell carcinoma", "8310", note="D14."),
            named("Seromucinous carcinoma", "8474", note="D14."),
            named("Undifferentiated carcinoma", "8020", note="D14."),
            named("Adenocarcinoma, type not stated", "8140", note="D14."),
            named("Carcinoma, type not stated", "8010", note="D14."),
            x("Serous borderline tumour", "serous borderline tumour", "8442", "1"),
            x("Mucinous borderline tumour", "mucinous borderline tumour", "8472", "1"),
            x("Seromucinous borderline tumour", "seromucinous borderline tumour", "8474", "1"),
            x("Endometrioid borderline tumour", "endometrioid borderline tumour", "8380", "1"),
            x("Serous cystadenoma", "serous cystadenoma", "8441", "0"),
            x("Mucinous cystadenoma", "mucinous cystadenoma", "8470", "0"),
        ],
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
            named("Malignant neoplasm, type not determined, cell type not described", "8000"),
            named("Malignant tumour, small cell type", "8002"),
            named("Malignant tumour, giant cell type", "8003"),
            named("Malignant tumour, spindle cell type", "8004"),
            named("Malignant tumour, clear cell type", "8005"),
        ],
        [], "D13: ICCC-2017 range 117 places 8000-8005 at C56.9 and C62 in Xe.")


def n_other_gonad(site):
    where = SITES[site]["where"]
    return node(
        nid(site, "other"), "morphology_only", 4, "Another tumour type",
        "Which tumour does the report diagnose?",
        "A tumour of %s that is not a germ cell, sex cord–stromal or epithelial tumour is "
        "coded from another group, or at its primary site." % where,
        [
            refer("Lymphoma", 2,
                  "A lymphoma involving %s belongs to ICCC-3 Group II. Code the case from the "
                  "Group II (lymphomas) tree." % where),
            refer("Leukaemic infiltration", 1,
                  "Leukaemic infiltration of %s is coded as the leukaemia, in ICCC-3 Group I. "
                  "Code the case from the Group I (leukaemias) tree." % where),
            refer("Rhabdomyosarcoma or another sarcoma", 9,
                  "A soft tissue sarcoma belongs to ICCC-3 Group IX. Code the case from the "
                  "Group IX (soft tissue sarcomas) tree."),
            nonrep("A deposit of a tumour that began elsewhere",
                   "The tumour in %s is a deposit of a tumour that began elsewhere. Code that "
                   "tumour at its primary site, from its own group's tree." % where,
                   heading="Metastatic deposit: code the primary tumour"),
            refer("Another malignant tumour type the report names", 12,
                  "ICCC-3 Group XII holds the specified malignant tumours no other group codes. "
                  "Code the case from the Group XII (other and unspecified malignant neoplasms) "
                  "tree; a melanoma is coded from the Group XI tree instead."),
        ],
        [], "Contract §4.4.")


def n_other_extragonadal():
    s = "extragonadal"
    return node(
        nid(s, "other"), "morphology_only", 4, "Another tumour type",
        "Which tumour does the report diagnose?",
        "A tumour that is not a germ cell or trophoblastic tumour is coded from another group, "
        "or at its primary site.",
        [
            refer("A sarcoma", 9,
                  "A soft tissue sarcoma belongs to ICCC-3 Group IX. Code the case from the "
                  "Group IX (soft tissue sarcomas) tree."),
            refer("Neuroblastoma", 4,
                  "Neuroblastoma belongs to ICCC-3 Group IV. Code the case from the Group IV "
                  "tree."),
            refer("Lymphoma", 2,
                  "A lymphoma belongs to ICCC-3 Group II. Code the case from the Group II "
                  "(lymphomas) tree."),
            nonrep("A deposit of a tumour that began elsewhere",
                   "The tumour is a deposit of a tumour that began elsewhere. Code that tumour "
                   "at its primary site, from its own group's tree.",
                   heading="Metastatic deposit: code the primary tumour"),
            refer("Another malignant tumour type the report names", 12,
                  "ICCC-3 Group XII holds the specified malignant tumours no other group codes. "
                  "Code the case from the Group XII (other and unspecified malignant neoplasms) "
                  "tree; a carcinoma or melanoma is coded from the Group XI tree instead."),
        ],
        [], "Contract §4.4.")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def common(site):
    """The eight nodes every site tree carries, in tree order."""
    p = SITES[site]["prefix"]
    targets = {t: p + TIER_NODE[t] for t in TIERS}
    histology = {"cns": n_histology_cns, "ovary": n_histology_ovary,
                 "testis": n_histology_testis,
                 "extragonadal": n_histology_extragonadal}[site]
    return [
        n_document_inventory(p + "document_inventory", targets,
                             "Contract §4.2: five evidence tiers. Every Group X tree carries "
                             "the same tiers; the router's site capture chose this tree."),
        n_clinical_alias(site), n_markers(site), n_imaging(site), n_cytology(site),
        histology(), n_mixed(site), n_ihc(site),
    ]


def site_unstated_nodes():
    targets = {t: "su_site_" + t for t in TIERS}
    nodes = [n_document_inventory(
        "su_document_inventory", targets,
        "Contract §4.5. The router's default: no topography captured, or one no rule names. "
        "The search box enters here. Same five tiers and captures as the site trees.")]
    for t in TIERS:
        tier_node = TIER_NODE[t]
        nodes.append(node(
            "su_site_" + t, "site_resolution", 2, "Tumour site",
            "Where is the tumour?",
            "The topography was not recorded at Stage 1. Record it on the case as well.",
            [
                go("Brain or spinal cord, including the pineal and suprasellar regions",
                   "cn_" + tier_node, {"gct_site": "cns"}),
                go("Ovary", "ov_" + tier_node, {"gct_site": "ovary"}),
                go("Testis", "ts_" + tier_node, {"gct_site": "testis"}),
                go("Any other site — sacrococcygeal region, mediastinum, retroperitoneum or "
                   "elsewhere", "eg_" + tier_node, {"gct_site": "other"}),
            ],
            ["gct_site"],
            "Contract §4.5. Cross-tree next_node into the site tree's %s node, which "
            "check_orphan_nodes and app.js findNode both allow. No terminal here." % tier_node))
    return nodes


def _tree(tree_id, label, entry, topography, nodes):
    return {"tree_id": tree_id, "tree_label": label, "entry_node": entry,
            "topography": topography, "basis_of_diagnosis_defaults": dict(BASIS_DEFAULTS),
            "nodes": nodes}


def trees() -> list:
    """Return a fresh list each call, so callers may mutate it."""
    return [
        _tree("g10_cns",
              "Germ cell tumours of the brain and spinal cord (C70.0-C72.9, C75.1-C75.3; "
              "ICCC-3 Xa admits behaviours 0, 1 and 3) - an evidence gate, a marker route, and "
              "a histology node with mixed and stain panel steps",
              "cn_document_inventory", _topo(TOPOGRAPHY_RAW["cns"]), common("cns")),
        _tree("g10_ovary",
              "Germ cell, sex cord-stromal and epithelial tumours of the ovary (C56.9; ICCC-3 "
              "Xc, Xd and Xe, behaviour 3 only) - the common evidence and germ cell nodes, "
              "with behaviour exclusions for benign and borderline tumours",
              "ov_document_inventory", _topo(TOPOGRAPHY_RAW["ovary"]),
              common("ovary") + [n_teratoma_ovary(), n_gonadoblastoma("ovary"),
                                 n_sex_cord_ovary(), n_epithelial_ovary(),
                                 n_unspecified("ovary"), n_other_gonad("ovary")]),
        _tree("g10_testis",
              "Germ cell and sex cord-stromal tumours of the testis (C62.0-C62.9; ICCC-3 Xc, "
              "Xd and Xe, behaviour 3 only) - the common evidence and germ cell nodes, with "
              "behaviour exclusions for benign, borderline and in situ lesions",
              "ts_document_inventory", _topo(TOPOGRAPHY_RAW["testis"]),
              common("testis") + [n_teratoma_testis(), n_gonadoblastoma("testis"),
                                  n_sex_cord_testis(), n_unspecified("testis"),
                                  n_other_gonad("testis")]),
        _tree("g10_extragonadal",
              "Germ cell and trophoblastic tumours outside the gonads and the central nervous "
              "system (ICCC-3 Xb, behaviour 3 only) - the common evidence and germ cell nodes, "
              "with moles and benign teratomas as behaviour exclusions",
              "eg_document_inventory", _topo(TOPOGRAPHY_RAW["extragonadal"]),
              common("extragonadal") + [n_teratoma_extragonadal(), n_other_extragonadal()]),
        _tree("g10_site_unstated",
              "Site not recorded - asks the evidence, then the site, and continues in the "
              "matching site tree; emits no code itself",
              "su_document_inventory", [], site_unstated_nodes()),
    ]
