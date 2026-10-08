"""g11_lung (prefix lu_): carcinomas of the lung and bronchus at C34.0-C34.9, ICCC-3 subgroup XIf4.

Built from docs/group_11_evidence/XIf4_lung_pleura.json, the lung nodes (lu_site, lu_evidence,
lu_lab, lu_cytology, lu_histology, lu_picker, lu_carcinoid, lu_not_malignant), with the builders
in build/group11_common.py, in the shape of build/group11_organs/thyroid.py. Every option's
label, code, behaviour, basis, reason and recognition aid comes from that file unless a departure
below says otherwise; the cite (file, page, quotation) is the comment above the option or aid.
File names in the comments are the evidence's own:
    Nicholson  XIf4-lung__Nicholson-2022.txt (Nicholson AG, et al. The 2021 WHO Classification
               of Lung Tumors. J Thorac Oncol 2022;17:362-387). "image" marks a quotation read
               from the page image.
    ICCR-Lung  XIf4-lung__ICCR-Lung-4th.txt (ICCR Lung Cancer Histopathology Reporting Guide,
               4th edition, version 4.0, April 2023)
    Pfister    ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules      RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Ozkan      XIf4-lung-paediatric__Ozkan-2024.txt (Turk Gogus Kalp Damar Cerrahisi Derg 2024;
               PMC10995685). A PubMed Central text has sections, not pages: "s. 2" is section 2.
    Chen       XIf4-lung-paediatric__Chen-2026.txt (Biomed Rep 2026; PMC13320230), sections as
               for Ozkan.
    Visser     Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's
               file set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    lu_document_inventory  document_inventory  evidence gate (evidence lu_evidence)
    lu_labs_referral, lu_labs_markers, lu_labs_cytology, lu_labs_histology  lab_results
                                               (evidence lu_lab)
    lu_clinical, lu_clinical_cytology  clinical_alias
    lu_imaging, lu_imaging_markers, lu_imaging_cytology  morphology_only
    lu_cytology            morphology_only     (evidence lu_cytology)
    lu_histology           histology_subclassification  (evidence lu_histology)
    lu_nscc_confirm, lu_nscc_favour  histology_subclassification  (registrar, 8 October 2026,
                                               review A2, E6: SEER lung rule H3)
    lu_nscc_ihc            ihc_checklist       (evidence lu_nscc_favour; Nicholson 2022, PDF pp. 5-6)
    lu_nscc_confirm_cyto, lu_nscc_favour_cyto  the same at basis 5 (cytology); the stain
                                               patterns are options, not a panel
    lu_carcinoid           histology_subclassification  (evidence lu_carcinoid)
    lu_nut_result, lu_nut_basis, lu_nut_tests  histology_subclassification  (D12)
    lu_not_malignant       histology_subclassification  (evidence lu_not_malignant and the
                                               exclusions of lu_histology)
    lu_deposit             morphology_only      (D10)
    lu_picker              histology_subclassification  (D2; evidence lu_picker's long tail)

Departures from the evidence nodes, and why
-------------------------------------------
1. lu_site is not built. The router's site capture already records C34.0 to C34.9 and chose this
   tree (D14: an organ question the router answers). Its three options that leave the lung (the
   lung with the pleura or chest wall, C39.8; the pleura only; beside the lung or a bronchus, Rule
   B) are router answers: C39.8 and the pleura route to g11_thoracic, and a paratracheal or
   peribronchial site to the ill-defined sites.
2. lu_evidence: the referral and imaging-only tiers recorded 8000/3 at basis 1 and 2 on the gate
   itself, and "possible, probable or suspected" was one not-registrable tier. D7: each tier
   routes to its own screen, which refers 8000/3 to Group XII (ICCC-2017 range 143 places it in
   XIIb at C34; evidence conflicts, Group 12, and registrar question 6). Visser rule 4 makes
   "possible" not registrable and "probable" registrable, so the hint drops "probable" and the
   clinical and imaging screens carry the not-registrable line. "Choose the strongest report" is
   dropped: the document checklist replaces it (thyroid departure 1).
3. lu_lab: a lab_results screen cannot choose a code (registrar, 6 October 2026). Its options
   move to lu_imaging_markers: 8240/3, 8241/3 and 8158/3 at basis 4 when imaging shows the tumour,
   the report calls the marker raised and the file names the tumour the marker registers (Visser
   Table 4; thyroid departure 2). "None of these is raised" (8000/3 basis 2) is the common
   "Imaging shows a malignant tumour ... no marker result above registers it" referral to Group
   XII. The chromogranin A label adds "without naming a hormone it produces" so that a file naming
   a serotonin- or adrenocorticotropic hormone-producing tumour takes that option, not both. The
   evidence gives no unit for any of the three tests; the lab rows carry the units laboratories
   print, for the registrar to confirm. The screen rests on the Visser Table 4 ruling alone: the
   lung papers name no serum test (evidence data gap 3, registrar question 7).
4. lu_cytology: the evidence's first option ("A named carcinoma or neuroendocrine tumour type")
   continued to lu_histology at basis 5, which would put basis 7 codes on a cytology path. D8:
   each named type is a basis 5 option instead: the three the option names (carcinoid tumour,
   small cell carcinoma, non-small cell carcinoma) and the histology screen's paediatric types a
   cytology report can name (adenocarcinoma, squamous cell carcinoma, mucoepidermoid carcinoma).
   A type the list does not hold records 8010/3 at basis 5, the less specific code (standing rule
   8: understate, never overstate). "Malignant cells, with no tumour type named" (8000/3, basis 5)
   is the common referral to Group XII with 8001 (D8). The lymphoma referral is kept.
5. lu_histology, order and content. The seven paediatric entities lead, as the evidence orders
   them, then pleuropulmonary blastoma, pulmonary blastoma and paraganglioma (referrals the
   evidence places next), then the generic options, then the common trailing options
   (tail_options). The carcinoid option's search_terms are not carried: a histology screen does not
   filter by search; the alias layer (T5) holds those terms.
6. lu_histology, NUT carcinoma (D12). The evidence's direct 8023/3 option is replaced by the
   common NUT screens (nut_nodes: lu_nut_result, lu_nut_basis, lu_nut_tests), which record 8023/3
   at basis 8 with a NUTM1 result and at basis 7 otherwise, and route a NUTM1-rearranged sarcoma
   or leukaemia out. The option carries the common NUT recognition aid (NUT_carcinoma.json), not
   this evidence's.
7. lu_histology, non-small cell carcinoma. The evidence's choice is 8046/3 for a report of
   non-small cell carcinoma with no type named, including one that says it favours a type, as a
   picker entry with that label (registrar question 2). The D2 picker shows the ICD-O-3.2
   Preferred term and cannot carry the "favours a type" instruction, so the option moves to the
   histology screen with the evidence's label and reason, and the picker leaves 8046 out.
   Superseded 8 October 2026 (registrar, review A2, E6): the option, and its cytology twin, lead
   to lu_nscc_confirm, lu_nscc_favour and the lu_nscc_ihc stain panel (nscc_nodes), which code the
   favoured type when the file confirms it (SEER lung rule H3) and 8046/3 otherwise.
8. lu_histology, acinar adenocarcinoma. The evidence's picker offered "Acinar adenocarcinoma" on
   8551/3, whose Preferred term ICD-O-3.2 marks [obs]. D3 holds 8551 off every screen until the
   registrar rules, so the screen offers acinar adenocarcinoma on the nearest generic code,
   Adenocarcinoma, NOS (8140/3), the decision pending. Without the option the picker's search for
   "acinar adenocarcinoma" finds 8480/3 Mucinous adenocarcinoma (its synonym "Acinar
   adenocarcinoma, mucinous variant") and 8550/3 Acinar cell carcinoma, both wrong for the lung.
9. lu_histology, deposits. The evidence's deposit option (next site_capture with recapture) is the
   common deposit question (D10). Its option "A carcinoma that the report says has spread to the
   lung, and the organ where it began is not known" (8010/3 with topography_override C80.9) is the
   deposit question's "A carcinoma whose primary has not been found", which continues in the
   unspecified tree's histology screen at C80.9 (D10, ICCC-2017 range 136).
10. lu_histology, "A malignant tumour, with no type named" (8000/3 basis 7) is the common referral
   to Group XII with 8000 (D7).
11. lu_histology, referrals. Lymphoma keeps the evidence's label naming Langerhans cell
   histiocytosis and Erdheim-Chester disease and adds Hodgkin lymphoma, and the sarcoma label adds
   the sarcomas Chen 2026 reports in children (evidence data gap 10). Inflammatory myofibroblastic
   tumour, an exclusion (8825/1) in the evidence, is referred to Group IX with the sarcomas
   (controller's instruction): the Group IX tree holds both Myofibroblastic tumor, NOS (8825/1) as
   an exclusion and Myofibroblastic sarcoma (8825/3), so it records whichever the report names.
   The common leukaemia, germ cell and other-named referrals are added; the germ cell referral
   carries the mature teratoma Chen 2026 reports (evidence data gap 8: Group X records its
   behaviour). Carcinosarcoma and myoepithelial carcinoma (Group XII) follow the common
   referrals.
12. lu_histology, the exclusions (congenital peribronchial myofibroblastic tumour 8827/1) and the
   not-registrable fetal lung interstitial tumour move to lu_not_malignant, reached by the
   standard option, whose label names them (thyroid departure 5).
13. Melanoma (D13): the lung is none of skin, eye or central nervous system, so the hop enters
   me_mucosa, as the thyroid's does (evidence conflicts: the melanoma tree needs a route for a
   melanoma of an internal organ; T2c to confirm).
14. lu_picker: D2 replaces the evidence's curated picker (thyroid departure 12). The labels are
   the ICD-O-3.2 Preferred terms, so seven WHO 2021 names on the evidence's picker are not shown,
   and the picker's search does not find four of them: Hyalinizing clear cell carcinoma (8310/3),
   Invasive mucinous adenocarcinoma (8253/3; the search "mucinous adenocarcinoma" finds 8480/3
   instead), Mixed invasive mucinous and non-mucinous adenocarcinoma (8254/3) and Non-keratinizing
   squamous cell carcinoma (8072/3; ICD-O-3.2 writes "nonkeratinizing"). The build report lists
   them for the alias layer and the registrar. The evidence's picker aids (minimally invasive
   adenocarcinoma, fetal adenocarcinoma, enteric-type adenocarcinoma) are not shown either.
15. (Superseded 8 October 2026: the registrar agreed 8252/3, review E3; the hold below is released.)
   lu_picker: 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous was held off the picker (the
   evidence's action: not on any screen until registrar question 4 is ruled; controller's
   instruction). ICCC-2017 places it in XIf4 at C34, so D2 would offer it: hold_from_picker()
   removes it after make_tree() and records the hold in the picker's coding_note and
   PICKER_REPORT. Validator rule 4 (every live code has a route) will report it until the
   registrar rules or the rule admits a registrar hold.
16. lu_not_malignant: the common screen's hint replaces the evidence's; the evidence's Rule F
   sentence ("If the pathologist states that one of these tumours is malignant, the stated
   behaviour is recorded") is not shown, because D6 does not build Rule F stated behaviour.
17. Not built from the evidence: thoracic SMARCA4-deficient undifferentiated tumour on 8044
   (D4; no screen names the entity), 8251/3 and 8042/3 (D3), 8551/3 (D3), and Rule K on the
   histology screen's hint (evidence data gap 9: the screen shows no codes to compare). The
   lu_nscc_favour stain rules, held here until 8 October 2026, are built as lu_nscc_ihc (item 7).

Registrar questions the evidence raised (XIf4_lung_pleura.json §10, questions 2 to 7) stay open;
the defaults above apply until they are answered (docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

import group11_common as common
from group11_common import (TYPE_NOT_STATED, aid, code, cyto, deposit_node, evidence_gate, excl,
                            go, ihc_node, lab, make_tree, marker, named, node, nonrep,
                            not_malignant_node, nut_nodes, rec, refer, refer_germ_cell,
                            refer_leukaemia, refer_lymphoma, refer_other_named, rule,
                            tail_options, term)

TREE_ID = "g11_lung"
P = "lu_"
WHERE = "the lung"
EVIDENCE = "XIf4_lung_pleura"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Ozkan s. 2 "a combination of mucus-secreting, squamous, and intermediate cell types".
AID_MEC = "Reports describe a mix of mucus-secreting, squamous and intermediate cells."
# Nicholson p. 13 "greater than the upper threshold of mitotic counts for atypical carcinoid";
# "The current recommendation is to label such tumors as LCNEC".
AID_LCNEC = ("A tumour that looks like a carcinoid but has a mitotic count above the atypical "
             "carcinoid range is called large cell neuroendocrine carcinoma.")
# Nicholson p. 3 "Pulmonary blastoma 8972/3" and "Pleuropulmonary blastoma 8973/3".
AID_BLASTOMA = ("Pulmonary blastoma and pleuropulmonary blastoma are different tumours; choose "
                "the one the report names.")
# Ozkan s. 2 "They can mimic carcinoid tumors or primary lung cancer".
AID_PARAGANGLIOMA = ("Paraganglioma and carcinoid tumour can look alike; choose the one the "
                     "report names.")
# Nicholson p. 12 "with mitoses and presence of necrosis representing the mainstay for
# classification".
AID_ATYPICAL = ("Reports separate atypical from typical carcinoid by a higher mitotic count or by "
                "necrosis.")

SUBTYPE_UPGRADE = ("The report does not name a subtype. A report that names one (for example "
                   "lepidic, papillary, micropapillary, solid or invasive mucinous adenocarcinoma) "
                   "gives that subtype's own code: go back and take another carcinoma the report "
                   "names.")
SQUAMOUS_UPGRADE = ("The report does not name a subtype. A report that names one (keratinizing, "
                    "non-keratinizing or basaloid squamous cell carcinoma) gives that subtype's "
                    "own code: go back and take another carcinoma the report names.")
PENDING_DECISION = "This awaits the registrar's decision."


def referral_reason(morph: str, group_text: str, tree_text: str, extra: str = "") -> str:
    """'ICD-O-3.2 codes it as <Preferred term> (<code>/3). ICCC-3 places that code in <group>,
    not Group XI. Code the case from the <tree>.' The Preferred term is read from icdo32.sqlite."""
    return ("ICD-O-3.2 codes it as %s (%s/3). ICCC-3 places that code in %s, not Group XI.%s "
            "Code the case from the %s." % (term(morph, "3"), morph, group_text,
                                            (" " + extra) if extra else "", tree_text))


def hold_from_picker(tree: dict, prefix: str, holds: dict) -> dict:
    """Remove the codes in `holds` ({code: why}) from the tree's picker after make_tree(), and
    record the hold in the picker's coding_note and in PICKER_REPORT. A code the evidence keeps
    off every screen until the registrar rules is held this way (group11_common offers no hold
    parameter; the module returns the request)."""
    if not holds:
        return tree
    picker = next(nd for nd in tree["nodes"] if nd["node_id"] == prefix + "picker")
    present = [o["morphology_code"] for o in picker["options"] if o.get("morphology_code") in holds]
    if sorted(present) != sorted(holds):
        raise common.TreeError("%s: the picker does not offer %s, so it cannot be held"
                               % (tree["tree_id"], ", ".join(sorted(set(holds) - set(present)))))
    picker["options"] = [o for o in picker["options"] if o.get("morphology_code") not in holds]
    picker["coding_note"] += (" Held off the picker until the registrar rules: %s."
                              % "; ".join("%s (%s)" % (c, holds[c]) for c in sorted(holds)))
    rep = common.PICKER_REPORT.get(tree["tree_id"])
    if rep is not None:
        rep["offered"] = [c for c in rep["offered"] if c not in holds]
        rep["held_registrar"] = sorted(holds)
    return tree


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence lu_evidence, lu_lab, lu_cytology)
# ------------------------------------------------------------------------------------------
MARKER_TESTS = "chromogranin A, serotonin or adrenocorticotropic hormone"
VISSER_T4 = ("Visser O, et al. Front Oncol 2023;13:1250549, Table 4, p. 06 (%s), rule 6, p. 05. "
             "Evidence XIf4_lung_pleura.json tissue_free row %d and lu_lab option %d; the lung "
             "papers name no serum test (data gap 3, registrar question 7).")


def gate():
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this lung tumour?",
        # Evidence lu_evidence hint, less "Choose the strongest report" and "probable"
        # (departure 2).
        hint=("A radiology report counts as imaging. Cytology of sputum, a bronchial washing or "
              "brushing, or a needle aspirate counts as cytology. A pathology report on a biopsy "
              "or resection counts as histology. A biopsy or cytology report that calls the "
              "specimen inadequate or non-diagnostic counts as no tissue. A report that calls "
              "the tumour possible or suspected cancer does not register it."),
        # Evidence lu_lab (departure 3): the three tests Visser Table 4 names for functioning and
        # non-functioning neuroendocrine tumours. The evidence prints no unit.
        labs=[lab("chromogranin_a", "Serum chromogranin A", ("ng/mL", "µg/L")),
              lab("serotonin", "Serum serotonin", ("ng/mL", "nmol/L")),
              lab("acth", "Plasma adrenocorticotropic hormone (ACTH)",
                  ("pg/mL", "ng/L", "pmol/L"))],
        marker_tests=MARKER_TESTS,
        markers=[
            # Evidence tissue_free row 3, lu_lab option 1. Visser Table 4, p. 06: neuroendocrine
            # tumour, chromogranin A, 8240/3 (contract §0.5: the row names no site).
            marker("8240", test="chromogranin A",
                   diagnosis="carcinoid tumour or neuroendocrine tumour", where="in the lung",
                   label="Imaging shows a tumour in the lung, the report calls chromogranin A "
                         "raised, and the file calls it a carcinoid tumour or neuroendocrine "
                         "tumour without naming a hormone it produces",
                   note=VISSER_T4 % ("neuroendocrine tumour, chromogranin A", 3, 1)),
            # Evidence tissue_free row 4, lu_lab option 2. Visser Table 4, p. 06: functioning
            # neuroendocrine tumours, serotonin, 8241/3. icdo32.sqlite 8241/3 Synonym Serotonin
            # producing carcinoid.
            marker("8241", test="serotonin",
                   diagnosis="serotonin-producing carcinoid or neuroendocrine tumour",
                   where="in the lung",
                   label="Imaging shows a tumour in the lung, the report calls serotonin raised, "
                         "and the file calls it a serotonin-producing (functioning) carcinoid or "
                         "neuroendocrine tumour",
                   extra="ICD-O-3.2 gives Serotonin producing carcinoid as a synonym of this "
                         "code.",
                   note=VISSER_T4 % ("functioning neuroendocrine tumours, serotonin", 4, 2)),
            # Evidence tissue_free row 5, lu_lab option 3. Visser Table 4, p. 06: functioning
            # neuroendocrine tumours, adrenocorticotropic hormone, 8158/3.
            marker("8158", test="adrenocorticotropic hormone",
                   diagnosis="adrenocorticotropic hormone-producing neuroendocrine tumour",
                   where="in the lung",
                   label="Imaging shows a tumour in the lung, the report calls adrenocorticotropic "
                         "hormone (ACTH) raised, and the file calls it an adrenocorticotropic "
                         "hormone-producing (functioning) carcinoid or neuroendocrine tumour",
                   note=VISSER_T4 % ("functioning neuroendocrine tumours, adrenocorticotropic "
                                     "hormone", 5, 3)),
        ],
        tier_labels={
            "imaging": "An imaging report only (chest X-ray, computed tomography or magnetic "
                       "resonance imaging) - no chromogranin A, serotonin or adrenocorticotropic "
                       "hormone result, no tissue",
            "cytology": "A cytology report (sputum, bronchial washing or brushing, or a needle "
                        "aspirate) - no histology report",
            "histology": "A histology report on a biopsy or resection, with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=[
            # Evidence lu_cytology option 1 ("such as carcinoid tumour"). Nicholson p. 3
            # "Carcinoid tumor, NOS/neuroendocrine tumor, NOS 8240/3"; Nicholson p. 5 "terms AIS
            # and minimally invasive ADC should not be used for diagnosis of small biopsies".
            cyto("Carcinoid tumour or neuroendocrine tumour", "8240",
                 "ICD-O-3.2 gives Carcinoid tumor, NOS as a synonym of this code.",
                 note="Evidence lu_cytology option 1 (departure 4)."),
            # Evidence lu_cytology option 1 ("small cell carcinoma"). Nicholson p. 3 "Small cell
            # carcinoma 8041/3".
            cyto("Small cell carcinoma", "8041",
                 note="Evidence lu_cytology option 1 (departure 4)."),
            # Evidence lu_cytology option 1 ("non-small cell carcinoma") and lu_picker option 25.
            # Nicholson p. 6 image "Nonsmall cell carcinoma NOS"; p. 5 "NSCC-NOS may need a
            # cytokeratin to confirm carcinoma". Registrar question 2.
            go("Non-small cell carcinoma, with no type named, including one the report says "
               "favours a type", n("nscc_confirm_cyto"),
               captures={"workup_status": "incomplete", "basis_evidence_tier": "cytology_named"},
               note="Evidence lu_cytology option 1 and lu_picker option 25 (departures 4, 7). "
                    "Registrar, 8 October 2026 (review A2, E6): the favoured type is coded when "
                    "the file confirms it (SEER lung rule H3), and the stains decide the favoured "
                    "type (Nicholson 2022, PDF pp. 5-6)."),
            # Nicholson p. 2 "Adenocarcinoma, NOS 8140/3"; Ozkan s. 2 "epithelial origin in
            # pediatric patients are carcinoid tumors, mucoepidermoid carcinoma, adenocarcinoma,
            # squamous cell carcinoma".
            cyto("Adenocarcinoma", "8140",
                 note="Departure 4: a paediatric type of the histology screen a cytology report "
                      "can name."),
            # Nicholson p. 2 "Squamous cell carcinoma, NOS 8070/3"; Ozkan s. 2 (as above).
            cyto("Squamous cell carcinoma", "8070",
                 note="Departure 4: a paediatric type of the histology screen a cytology report "
                      "can name."),
            # Nicholson p. 3 "Mucoepidermoid carcinoma 8430/3"; Ozkan s. 2 "It was reported as
            # the second most common primary malignant pulmonary tumor in children".
            cyto("Mucoepidermoid carcinoma", "8430",
                 note="Departure 4: a paediatric type of the histology screen a cytology report "
                      "can name."),
            # Evidence lu_cytology option 2 ("Carcinoma, with no type named", 8010/3 basis 5).
            cyto("A carcinoma whose type the cytology report does not name, or names a type not "
                 "listed above", "8010",
                 "A type this list does not hold is recorded with the generic carcinoma code; a "
                 "histology report gives the type's own code.",
                 note="Evidence lu_cytology option 2, widened to the named types the list does "
                      "not hold (departure 4; standing rule 8)."),
            # Evidence lu_cytology option 4. Rules p. 2 (printed p. 15) "Code extranodal
            # lymphomas to the site of origin".
            refer_lymphoma(WHERE),
        ],
        note="Evidence lu_evidence, lu_lab and lu_cytology (departures 2 to 4 in the module "
             "docstring).")


# ------------------------------------------------------------------------------------------
# Histology (evidence lu_histology)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # Nicholson p. 3 "Carcinoid tumor, NOS/neuroendocrine tumor, NOS 8240/3"; Ozkan s. 2
        # "Bronchial carcinoids account for 42-63% of all primary lung malignancies in the
        # pediatric population"; Chen s. 10 "the most prevalent primary malignant pulmonary tumors
        # in children are carcinoid tumors and PPB". D1.
        go("Carcinoid tumour, typical or atypical carcinoid, or neuroendocrine tumour",
           n("carcinoid"), note="D1: Ozkan 2024, Chen 2026 (evidence §11)."),
        # Nicholson p. 3 "Mucoepidermoid carcinoma 8430/3"; Ozkan s. 2 "It was reported as the
        # second most common primary malignant pulmonary tumor in children"; Chen s. 10
        # "followed by mucoepidermoid carcinoma, which constitutes 11.11%". D1.
        aid(named("Mucoepidermoid carcinoma", "8430", note="D1: Ozkan 2024, Chen 2026."),
            AID_MEC),
        # Nicholson p. 2 "Adenocarcinoma, NOS 8140/3"; Ozkan s. 2 "Adenocarcinoma was more common
        # than squamous cell carcinoma." D1.
        named("Adenocarcinoma, with no subtype named", "8140", upgrade=SUBTYPE_UPGRADE,
              note="D1: Ozkan 2024."),
        # Nicholson p. 2 "Acinar adenocarcinoma 8551/3". D3 holds 8551 (departure 8).
        named("Acinar adenocarcinoma", "8140",
              "ICD-O-3.2 places acinar adenocarcinoma of the lung on a code whose Preferred term "
              "it marks obsolete, and no screen offers that code until the registrar rules, so "
              "the generic adenocarcinoma code is recorded. " + PENDING_DECISION,
              note="D3: 8551/3 Preferred term [obs], Related term Acinar adenocarcinoma of lung "
                   "live (currency check §4); departure 8."),
        # Nicholson p. 2 "Squamous cell carcinoma, NOS 8070/3"; Ozkan s. 2 "epithelial origin in
        # pediatric patients are carcinoid tumors, mucoepidermoid carcinoma, adenocarcinoma,
        # squamous cell carcinoma". D1.
        named("Squamous cell carcinoma, with no subtype named", "8070", upgrade=SQUAMOUS_UPGRADE,
              note="D1: Ozkan 2024."),
        # Nicholson p. 3 "Small cell carcinoma 8041/3"; Ozkan s. 2 "Small cell lung carcinoma is
        # exceedingly rare in pediatric patients."; Chen s. 2 "neuroendocrine tumors (small cell
        # carcinoma and large cell neuroendocrine carcinoma)". D1.
        named("Small cell carcinoma", "8041",
              "ICD-O-3.2 gives Small cell neuroendocrine carcinoma as a related term of this "
              "code.", note="D1: Ozkan 2024, Chen 2026."),
        # Nicholson p. 2 "Large cell carcinoma 8012/3"; Ozkan s. 2 "adenocarcinoma, squamous cell
        # carcinoma, small cell carcinoma, and large cell carcinoma". D1.
        named("Large cell carcinoma", "8012", note="D1: Ozkan 2024."),
        # Nicholson p. 3 "Large cell neuroendocrine carcinoma 8013/3"; Nicholson p. 13; Chen
        # s. 2. D1. Rules p. 11 (printed p. 24): the combined tumour has its own code (Rule K
        # not needed).
        aid(named("Large cell neuroendocrine carcinoma, including combined large cell "
                  "neuroendocrine carcinoma", "8013",
                  "ICD-O-3.2 gives Combined large cell neuroendocrine carcinoma as a related term "
                  "of this code.", note="D1: Chen 2026."), AID_LCNEC),
        # Evidence lu_picker option 25 (departure 7). Nicholson p. 6 image "Nonsmall cell
        # carcinoma NOS"; Nicholson p. 5 "NSCC-NOS may need a cytokeratin to confirm carcinoma".
        go("Non-small cell carcinoma, with no type named, including one the report says "
           "favours a type", n("nscc_confirm"),
           note="Moved from the evidence's picker (departure 7). Registrar, 8 October 2026 "
                "(review A2, E6): the favoured type is coded when the file confirms it (SEER "
                "lung rule H3), and the stains decide the favoured type (Nicholson 2022, PDF "
                "pp. 5-6)."),
        # Pfister p. 14 "Congenital peribronchial myofibroblastic tumor Pleuropulmonary
        # blastoma"; Nicholson p. 3 "Pleuropulmonary blastoma 8973/3"; Chen s. 9 "Pleuropulmonary
        # blastoma (PPB) was the most prevalent tumor type, comprising 44.44%". ICCC-2017: 8973
        # at C34 -> XIIa3.
        refer("Pleuropulmonary blastoma", 12,
              referral_reason("8973", "Group XII (other and unspecified malignant neoplasms)",
                              "Group XII tree"),
              note="Evidence lu_histology option 8; ICCC-2017 XIIa3 at every site (evidence "
                   "conflicts, Group 12)."),
        # Nicholson p. 3 "Pulmonary blastoma 8972/3"; Chen s. 9 "The third patient was diagnosed
        # with pulmonary blastoma". ICCC-2017: 8972 at C34 -> XIIa3.
        aid(refer("Pulmonary blastoma", 12,
                  referral_reason("8972", "Group XII (other and unspecified malignant neoplasms)",
                                  "Group XII tree"),
                  note="Evidence lu_histology option 9; ICCC-2017 XIIa3."), AID_BLASTOMA),
        # Ozkan s. 2 "the second pediatric functioning PPP in the literature"; Ozkan s. 2 "They
        # can mimic carcinoid tumors or primary lung cancer". ICCC-2017: 8680 and 8693 at C34 ->
        # IVb.
        aid(refer("Paraganglioma", 4,
                  "ICD-O-3.2 codes it as %s (8680/3), or %s (8693/3) when the report says it "
                  "arises outside the adrenal gland. ICCC-3 places both codes in Group IV "
                  "(neuroblastoma and other peripheral nervous cell tumours), not Group XI. Code "
                  "the case from the Group IV tree." % (term("8680", "3"), term("8693", "3")),
                  note="Evidence lu_histology option 10; ICCC-2017 IVb at every site."),
            AID_PARAGANGLIOMA),
        # Evidence lu_histology option 21 ("Carcinoma, with no type named", 8010/3).
        named("Carcinoma, with no type named", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence lu_histology option 21; the generic option of the screen (D4's "
                   "nearest generic code). A non-small cell carcinoma takes the option above, "
                   "whose stain panel is lu_nscc_ihc."),
    ] + tail_options(
        P, "mucosa", where=WHERE, nut=True,
        not_malignant_label="A benign tumour, a precursor lesion or an in situ carcinoma, such as "
                            "adenocarcinoma in situ, a papilloma, a hamartoma, sclerosing "
                            "pneumocytoma, a congenital peribronchial myofibroblastic tumour or a "
                            "fetal lung interstitial tumour",
        referrals=[
            # Nicholson p. 3 "MALT lymphoma 9699/3", "Langerhans cell histiocytosis 9751/1";
            # Chen s. 9 "A patient with Hodgkin's lymphoma was confirmed by ultrasound-guided
            # biopsy". Rules p. 2 (printed p. 15) Rule D. ICCC-2017: 9650 at C34 -> IIa; 9699 ->
            # IIb2.
            refer("Lymphoma, including Hodgkin lymphoma, or Langerhans cell histiocytosis or "
                  "Erdheim-Chester disease", 2,
                  "Lymphomas and histiocytic tumours belong to ICCC-3 Group II. A lymphoma that "
                  "arises in the lung keeps the lung as its site (WHO Rule D: an extranodal "
                  "lymphoma is coded to its site of origin). Code the case from the Group II "
                  "(lymphomas and reticuloendothelial neoplasms) tree.",
                  note="Evidence lu_histology option 14 (departure 11). ICD-O-3.1 Rule D, p. 15. "
                       "ICCC-2017 holds no range for 9749 Erdheim-Chester disease; the Group II "
                       "tree carries it (evidence conflicts, Group 2)."),
            refer_leukaemia(WHERE),
            # Nicholson p. 3 "Intimal sarcoma 9137/3", "PEComa, malignant 8714/3"; ICCR-Lung
            # p. 6 "Data from non-epithelial tumours should be collected using other ICCR
            # datasets"; Chen s. 2 "Mesenchymal tumors (rhabdomyosarcoma and inflammatory
            # myofibroblastic tumor)"; Chen s. 9 "The second pediatric patient with Ewing sarcoma
            # with EWSR1-FLI1 gene fusion", "pulmonary alveolar soft tissue sarcoma". ICCC-2017 at
            # C34: 8900 IXa, 9364 IXd2, 9581 IXd10, 9137 IXd8, 8714 and 8842 IXd11.
            refer("A sarcoma, such as rhabdomyosarcoma, Ewing sarcoma, alveolar soft part "
                  "sarcoma, intimal sarcoma, pulmonary myxoid sarcoma or malignant perivascular "
                  "epithelioid tumour (PEComa)", 9,
                  "A soft tissue sarcoma of the lung belongs to ICCC-3 Group IX. Code the case "
                  "from the Group IX (soft tissue and other extraosseous sarcomas) tree.",
                  note="Evidence lu_histology option 15 with the paediatric sarcomas of Chen 2026 "
                       "(departure 11, evidence data gap 10)."),
            # Pfister p. 6 "infantile fibrosarcoma or inflammatory myofibroblastic tumor"; Ozkan
            # s. 2 "Inflammatory myofibroblastic tumors account for more than 50% of benign
            # pulmonary tumors in childhood". icdo32.sqlite 8825/1 Synonym Inflammatory
            # myofibroblastic tumor; ICCC-2017: 8825 at C34 -> IXb1.
            refer("Inflammatory myofibroblastic tumour", 9,
                  "ICD-O-3.2 codes an inflammatory myofibroblastic tumour as %s (8825/1), "
                  "behaviour 1, uncertain, and a myofibroblastic sarcoma as %s (8825/3), which "
                  "ICCC-3 places in Group IX. Code the case from the Group IX (soft tissue and "
                  "other extraosseous sarcomas) tree, which records whether the report's tumour "
                  "is registered." % (term("8825", "1"), term("8825", "3")),
                  note="Evidence lu_histology option 17 was an exclusion (8825/1); referred to "
                       "Group IX on the controller's instruction (departure 11). The Group IX "
                       "screen g9_soft_tissue st_fibroblastic holds the exclusion and 8825/3."),
            # Chen s. 11 "Pulmonary sclerosing pneumocytoma 4 Hamartoma 3 Langerhans cell
            # histiocytosis 2 Mature teratoma 1". ICCC-2017: 9080 at C34 -> Xb2.
            refer_germ_cell(WHERE),
            refer_other_named(),
        ],
        extra_referrals=[
            # Nicholson p. 3 "Carcinosarcoma 8980/3". ICCC-2017: 8980 at C34 -> XIIa4.
            refer("Carcinosarcoma", 12,
                  referral_reason("8980", "Group XII (other and unspecified malignant neoplasms)",
                                  "Group XII tree"),
                  note="Evidence lu_histology option 11; ICCC-2017 XIIa4 (evidence conflicts, "
                       "Group 12)."),
            # Nicholson p. 3 "Myoepithelial carcinoma 8982/3". ICCC-2017: 8982 at C34 -> XIIa4.
            refer("Myoepithelial carcinoma", 12,
                  referral_reason("8982", "Group XII (other and unspecified malignant neoplasms)",
                                  "Group XII tree"),
                  note="Evidence lu_histology option 12; ICCC-2017 XIIa4."),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence lu_histology hint; Rules p. 11 (printed p. 24) for the combined types.
        "Choose the name in the report's diagnosis line. A tumour that the report says has "
        "spread to the lung from another organ is a deposit: it is coded at the organ where it "
        "began. Adenosquamous carcinoma and combined small cell carcinoma each have their own "
        "code: find them under another carcinoma the report names.",
        opts, [],
        "Evidence lu_histology (departures 5 to 13). D1: the paediatric entities are carcinoid "
        "tumour, mucoepidermoid carcinoma, adenocarcinoma, squamous cell carcinoma, small cell "
        "carcinoma, large cell carcinoma and large cell neuroendocrine carcinoma (Ozkan 2024, Chen "
        "2026; evidence §11). D12: NUT carcinoma (Nicholson 2022, p. 3; Pfister 2022, p. 14).")


# ------------------------------------------------------------------------------------------
# Non-small cell carcinoma with no definite type (registrar, 8 October 2026, review A2, E6)
# ------------------------------------------------------------------------------------------
# Jay: "Does a doctor elsewhere in the file state the type, or is the patient treated for it? A
# yes records 8140/3 Adenocarcinoma, NOS or 8070/3 Squamous cell carcinoma, NOS; a no records
# 8046/3. Add this. This is actually standard." SEER Solid Tumor Rules, lung, rule H3 (added
# 12 October 2018; SEER inquiries 20180110 and 20180113): a non-small cell carcinoma "favor" or
# "consistent with" a type is coded to that type when a physician confirms it or the patient is
# treated for it. Jay: the TTF-1 and p40 rules, "Add it". Nicholson 2022, PDF p. 5: "where TTF-1
# and/or mucin stains are positive but p40 is negative, the diagnosis is 'NSCC, favor
# adenocarcinoma'"; "In cases with both negative TTF-1 and p40, the diagnosis of adenocarcinoma
# can be supported if mucin stains are positive". PDF p. 6, Table 3: "supported by stains (i.e.,
# p40+)" -> "Nonsmall cell carcinoma, favor squamous cell carcinoma"; no staining pattern ->
# "Nonsmall cell carcinoma NOS". The confirmation is asked first, because an ihc_checklist rule
# is a terminal and cannot pass on to a question.
H3_SOURCE = ("Registrar, 8 October 2026 (review A2, E6). SEER Solid Tumor Rules, lung, rule H3 "
             "(added 12 October 2018). ")
STAIN_SOURCE = "Nicholson 2022, PDF p. 5 (TTF-1, mucin, p40) and PDF p. 6, Table 3. "
CONFIRMED = ("The pathology report favours this type, and the file confirms it: a doctor states "
             "it, or the patient is treated for it.")
NOT_CONFIRMED = ("A report that says the carcinoma favours a type, or gives stains that point to "
                 "one, has not stated the type, and nothing else in the file confirms it.")
NSCC_UPGRADE = ("The file does not confirm a type. A later pathology report or a doctor's note "
                "that states adenocarcinoma or squamous cell carcinoma, or treatment for one, "
                "gives that type's code: go back and answer yes.")
CYTO_TAIL = " Cytology does not give the full histological type; a histology report confirms it."


def nscc_nodes(basis: int) -> list:
    """<p>nscc_confirm, <p>nscc_favour and <p>nscc_ihc at basis 7. The cytology route (suffix
    _cyto, basis 5) has no stain panel: the engine records a stain panel's fallback at the tree's
    ihc_counts_as basis, 7, so the two stain patterns are options of <p>nscc_favour_cyto, as
    g11_thoracic builds tx_stains."""
    sfx = "" if basis == 7 else "_cyto"
    tail = "" if basis == 7 else CYTO_TAIL
    report = "histology" if basis == 7 else "cytology"

    def coded(label, morph, sentence, *, note, upgrade=None):
        return code(label, morph, "3", basis, rec(morph, "3", basis) + " " + sentence + tail,
                    note=H3_SOURCE + note, upgrade=upgrade)

    confirm = node(
        n("nscc_confirm" + sfx), "histology_subclassification", 4, "Type confirmed",
        "The %s report calls the tumour a non-small cell carcinoma and states no definite type. "
        "Does a doctor elsewhere in the file state the type, or is the patient treated for one "
        "type?" % report,
        "A report that says the carcinoma \"favours\" adenocarcinoma or squamous cell carcinoma, "
        "or gives stains that point to one, has not stated the type. The type is recorded only "
        "when the file confirms it: a doctor (an oncologist, a chest physician, a surgeon or a "
        "later pathology report) states it, or the patient is treated for it. This is the "
        "lung rule for uncertain terms of the Surveillance, Epidemiology, and End Results (SEER) "
        "Program's Solid Tumor Rules.",
        [
            go("Yes: a doctor states adenocarcinoma or squamous cell carcinoma, or the patient is "
               "treated for one of them", n("nscc_favour" + sfx),
               note=H3_SOURCE + "Condition 1 (physician confirmation) or 2 (treatment)."),
            coded("No, or the file says nothing more about the type", "8046", NOT_CONFIRMED,
                  note="Neither condition holds: non-small cell carcinoma, NOS (Nicholson 2022, "
                       "PDF p. 6, Table 3).", upgrade=NSCC_UPGRADE),
        ], [],
        H3_SOURCE + "Asked before the favoured type because an ihc_checklist rule is a terminal.")

    favour = node(
        n("nscc_favour" + sfx), "histology_subclassification", 5, "Favoured type",
        "Which type does the %s report favour?" % report,
        "Use the report's diagnosis line or comment. When the report favours no type in words "
        "but gives TTF-1, p40 or a mucin stain, choose the option for the stains. When the type a "
        "doctor states or treats differs from the type the report favours, choose the last "
        "option.",
        [
            coded("The report favours adenocarcinoma", "8140", CONFIRMED,
                  note="WHO small-biopsy term 'non-small cell carcinoma, favor adenocarcinoma' "
                       "(Nicholson 2022, PDF p. 6, Table 3)."),
            coded("The report favours squamous cell carcinoma", "8070", CONFIRMED,
                  note="WHO small-biopsy term 'non-small cell carcinoma, favor squamous cell "
                       "carcinoma' (Nicholson 2022, PDF p. 6, Table 3)."),
        ] + ([
            go("The report favours no type in words, and gives TTF-1, p40 or a mucin stain",
               n("nscc_ihc"), note=STAIN_SOURCE + "The stains decide the favoured type."),
        ] if basis == 7 else [
            coded("The report favours no type in words; TTF-1 or a mucin stain is positive and "
                  "p40 is negative", "8140",
                  "The WHO calls this non-small cell carcinoma, favour adenocarcinoma. " + CONFIRMED,
                  note=STAIN_SOURCE + "Built as a choice on the cytology route (nscc_nodes)."),
            coded("The report favours no type in words; p40 is positive, and TTF-1 and the mucin "
                  "stain are negative", "8070",
                  "The WHO calls this non-small cell carcinoma, favour squamous cell carcinoma. "
                  + CONFIRMED,
                  note=STAIN_SOURCE + "Built as a choice on the cytology route (nscc_nodes)."),
        ]) + [
            coded("The report favours no type, and the stains are absent or point both ways, or "
                  "the type stated elsewhere differs from the type the report favours", "8046",
                  "The pathology report favours no type, or not the type the file states "
                  "elsewhere, so no type is confirmed.",
                  note="H3 codes the favoured type only; with no favoured type, or a different "
                       "one, the code stays non-small cell carcinoma, NOS.",
                  upgrade=TYPE_NOT_STATED),
        ], [],
        H3_SOURCE + STAIN_SOURCE)

    if basis != 7:
        return [confirm, favour]
    stains = ihc_node(
        P,
        [
            {"group_label": "Adenocarcinoma markers", "markers": ["TTF-1", "Mucin stain"]},
            {"group_label": "Squamous cell carcinoma marker", "markers": ["p40"]},
        ],
        [
            rule(["TTF-1"], "8140",
                 "TTF-1 is positive and p40 is not: the WHO calls this non-small cell carcinoma, "
                 "favour adenocarcinoma. %s %s%s" % (CONFIRMED, rec("8140", "3", basis), tail),
                 negative=["p40"], basis=basis,
                 note=H3_SOURCE + "Nicholson 2022, PDF p. 5: 'TTF-1 and/or mucin stains are "
                      "positive but p40 is negative'."),
            rule(["Mucin stain"], "8140",
                 "A mucin stain is positive and p40 is not: the WHO calls this non-small cell "
                 "carcinoma, favour adenocarcinoma. %s %s%s"
                 % (CONFIRMED, rec("8140", "3", basis), tail),
                 negative=["p40"], basis=basis,
                 note=H3_SOURCE + "Nicholson 2022, PDF p. 5: 'the diagnosis of adenocarcinoma "
                      "can be supported if mucin stains are positive'."),
            rule(["p40"], "8070",
                 "p40 is positive, and TTF-1 and the mucin stain are not: the WHO calls this "
                 "non-small cell carcinoma, favour squamous cell carcinoma. %s %s%s"
                 % (CONFIRMED, rec("8070", "3", basis), tail),
                 negative=["TTF-1", "Mucin stain"], basis=basis,
                 note=H3_SOURCE + "Nicholson 2022, PDF p. 6, Table 3: 'supported by stains (i.e., "
                      "p40+)'."),
        ],
        fallback="8046",
        fallback_reason=("The stains favour no type, or point both ways. %s%s"
                         % (rec("8046", "3", basis), tail)),
        question="Answer each stain as the %s report states it." % report,
        hint="Answer positive or negative, and 'Not done or not readable' for a stain the report "
             "does not mention. TTF-1 or a mucin stain points to adenocarcinoma; p40 points to "
             "squamous cell carcinoma.",
        note=H3_SOURCE + STAIN_SOURCE + "Both TTF-1 and p40 positive, or neither stain and no "
             "mucin, fall to non-small cell carcinoma, NOS (Table 3).",
        name="nscc_ihc", step=6)
    return [confirm, favour] + ([stains] if basis == 7 else [])


def carcinoid():
    return node(
        n("carcinoid"), "histology_subclassification", 4, "Neuroendocrine tumour type",
        "Which neuroendocrine tumour does the report name?",
        # Evidence lu_carcinoid hint. Rules p. 9 (printed p. 22): Rule G, the higher grade.
        "When the report gives both typical and atypical carcinoid features, choose atypical "
        "carcinoid: the higher grade is recorded (WHO coding Rule G). A small biopsy or cytology "
        "report may call the tumour carcinoid tumour, not otherwise specified.",
        [
            # Nicholson p. 3 "Typical carcinoid/neuroendocrine tumor, grade 1 8240/3"; ICCR-Lung
            # p. 11 "Typical carcinoid/neuroendocrine tumour, grade 1 8240/3"; Ozkan s. 2.
            named("Typical carcinoid, or neuroendocrine tumour grade 1", "8240",
                  "ICD-O-3.2 gives Typical carcinoid as a synonym of this code."),
            # Nicholson p. 3 "Atypical carcinoid/neuroendocrine tumor, grade 2 8249/3"; Nicholson
            # p. 12; Ozkan s. 2 "Atypical bronchial carcinoids occur more frequently in children."
            aid(named("Atypical carcinoid, or neuroendocrine tumour grade 2", "8249",
                      "ICD-O-3.2 gives Atypical carcinoid tumor as a synonym of this code."),
                AID_ATYPICAL),
            # Nicholson p. 3 "Carcinoid tumor, NOS/neuroendocrine tumor, NOS 8240/3"; Nicholson
            # p. 12 "for small samples from primary or metastatic NETs and to record the mitotic
            # count"; icdo32.sqlite 8240/3 Related Bronchial adenoma, carcinoid. Rules p. 7
            # (printed p. 20): bronchial adenoma of carcinoid type is 8240/3.
            named("Carcinoid tumour or neuroendocrine tumour, with no type or grade stated, or "
                  "bronchial adenoma of carcinoid type", "8240",
                  "ICD-O-3.2 gives Carcinoid tumor, NOS as a synonym and Bronchial adenoma, "
                  "carcinoid as a related term of this code.",
                  upgrade="The report does not state typical or atypical carcinoid. A report "
                          "that calls the tumour atypical carcinoid gives Neuroendocrine tumor, "
                          "grade 2 (8249/3)."),
            # Nicholson p. 13 "The current recommendation is to label such tumors as LCNEC".
            named("A tumour with carcinoid appearance that the report calls large cell "
                  "neuroendocrine carcinoma", "8013"),
        ], [],
        "Evidence lu_carcinoid. D1: typical and atypical carcinoid are paediatric (Ozkan 2024, "
        "Chen 2026). Rule G: the sixth-digit grade is not built (registrar, 7 October 2026).")


def not_malignant():
    def x(label, icdo, beh, what, extra="", note=None):
        return excl(label, icdo, beh, what=what, extra=extra, note=note)
    return not_malignant_node(
        P,
        [
            # Nicholson p. 2 "Adenocarcinoma in situ, nonmucinous 8250/2".
            x("Adenocarcinoma in situ, non-mucinous", "8250", "2",
              "a non-mucinous adenocarcinoma in situ of the lung"),
            # Nicholson p. 2 "Adenocarcinoma in situ, mucinous 8253/2".
            x("Adenocarcinoma in situ, mucinous", "8253", "2",
              "a mucinous adenocarcinoma in situ of the lung"),
            # Nicholson p. 2 "Atypical adenomatous hyperplasia 8250/0".
            x("Atypical adenomatous hyperplasia", "8250", "0", "atypical adenomatous hyperplasia"),
            # Nicholson p. 2 "Squamous cell carcinoma in situ 8070/2".
            x("Squamous cell carcinoma in situ", "8070", "2", "a squamous cell carcinoma in situ"),
            # Nicholson p. 2 "Mild squamous dysplasia 8077/0".
            x("Mild squamous dysplasia", "8077", "0", "mild squamous dysplasia"),
            # Nicholson p. 2 "Moderate squamous dysplasia 8077/2", "Severe squamous dysplasia
            # 8077/2".
            x("Moderate or severe squamous dysplasia", "8077", "2",
              "moderate or severe squamous dysplasia",
              extra="ICD-O-3.2 gives Squamous dysplasia, high grade as a synonym of this code."),
            # Nicholson p. 2 "Squamous cell papilloma, NOS 8052/0".
            x("Squamous cell papilloma", "8052", "0", "a squamous cell papilloma"),
            # Nicholson p. 2 "Squamous cell papilloma, inverted 8053/0".
            x("Inverted squamous cell papilloma", "8053", "0", "an inverted squamous cell papilloma"),
            # Nicholson p. 2 "Glandular papilloma 8260/0", "Papillary adenoma 8260/0".
            x("Glandular papilloma or papillary adenoma", "8260", "0",
              "a glandular papilloma or papillary adenoma",
              extra="ICD-O-3.2 gives Glandular papilloma as a related term of this code."),
            # Nicholson p. 2 "Mixed squamous cell and glandular papilloma 8560/0".
            x("Mixed squamous cell and glandular papilloma", "8560", "0",
              "a mixed squamous cell and glandular papilloma"),
            # Nicholson p. 2 "Sclerosing pneumocytoma 8832/0"; Chen s. 9 "Pulmonary mucoepidermoid
            # carcinoma and pulmonary sclerosing pneumocytoma each accounted for 11.11%".
            x("Sclerosing pneumocytoma", "8832", "0", "a sclerosing pneumocytoma",
              extra="ICD-O-3.2 lists Sclerosing pneumocytoma as a related term of this code."),
            # Nicholson p. 2 "Alveolar adenoma 8251/0".
            x("Alveolar adenoma", "8251", "0", "an alveolar adenoma"),
            # Nicholson p. 2 image "Bronchiolar adenoma/ciliated muconodular papillary tumor
            # 8140/0".
            x("Bronchiolar adenoma or ciliated muconodular papillary tumour", "8140", "0",
              "a bronchiolar adenoma or ciliated muconodular papillary tumour"),
            # Nicholson p. 2 "Mucinous cystadenoma 8470/0".
            x("Mucinous cystadenoma", "8470", "0", "a mucinous cystadenoma"),
            # Nicholson p. 2 "Mucous gland adenoma 8480/0".
            x("Mucous gland adenoma", "8480", "0", "a mucous gland adenoma",
              extra="ICD-O-3.2 gives Mucous gland adenoma as a related term of this code."),
            # Nicholson p. 3 "Pleomorphic adenoma 8940/0".
            x("Pleomorphic adenoma", "8940", "0", "a pleomorphic adenoma"),
            # Nicholson p. 3 "Myoepithelioma 8982/0".
            x("Myoepithelioma", "8982", "0", "a myoepithelioma"),
            # Nicholson p. 3 "Diffuse idiopathic neuroendocrine cell hyperplasia 8040/0".
            x("Diffuse idiopathic neuroendocrine cell hyperplasia, or a tumourlet", "8040", "0",
              "diffuse idiopathic neuroendocrine cell hyperplasia or a tumourlet",
              extra="ICD-O-3.2 gives Diffuse idiopathic neuroendocrine cell hyperplasia as a "
                    "related term of this code."),
            # Nicholson p. 3 "Pulmonary hamartoma 8992/0"; Ozkan s. 2 "Benign pulmonary tumors in
            # childhood include inflammatory myofibroblastic tumors, hamartoma".
            x("Pulmonary hamartoma", "8992", "0", "a pulmonary hamartoma"),
            # Nicholson p. 3 "Chondroma 9220/0".
            x("Chondroma", "9220", "0", "a chondroma"),
            # Nicholson p. 3 "PEComa, benign 8714/0".
            x("Benign perivascular epithelioid tumour (PEComa)", "8714", "0",
              "a benign perivascular epithelioid tumour"),
            # Nicholson p. 3 "Meningioma 9530/0".
            x("Meningioma", "9530", "0", "a meningioma"),
            # Rules p. 7 (printed p. 20) "has therefore been assigned the behavior code /1 to
            # indicate that it is uncertain"; icdo32.sqlite 8140/1 Synonym Bronchial adenoma, NOS.
            x("Bronchial adenoma, with no type named", "8140", "1",
              "a bronchial adenoma with no type named",
              extra="ICD-O-3.2 gives Bronchial adenoma, NOS as a synonym of this code. A "
                    "bronchial adenoma of carcinoid type is a carcinoid tumour: go back and "
                    "choose carcinoid tumour."),
            # Pfister p. 14 "Congenital peribronchial myofibroblastic tumor Pleuropulmonary
            # blastoma"; Nicholson p. 3 "Congenital peribronchial myofibroblastic tumor 8827/1".
            x("Congenital peribronchial myofibroblastic tumour", "8827", "1",
              "a congenital peribronchial myofibroblastic tumour",
              extra="ICD-O-3.2 gives Congenital peribronchial myofibroblastic tumor as a synonym "
                    "of this code.",
              note="Evidence lu_histology option 16 (departure 12)."),
            # Pfister p. 14 "Thoracic tumors Lung Fetal lung interstitial tumor". Registrar
            # question 5; evidence data gap 4.
            nonrep("Fetal lung interstitial tumour",
                   "Fetal lung interstitial tumour has no malignant code in ICD-O-3.2, so it is not "
                   "registered.",
                   note="Evidence lu_histology option 18 (departure 12); registrar question 5."),
        ],
        where=WHERE,
        note="The 23 exclusions of evidence lu_not_malignant, the exclusion and the "
             "not-registrable line of lu_histology (departures 12 and 16).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
# Evidence code_currency 8252: held until the registrar ruled. Registrar, 8 October 2026 (review A1 (c),
# E3): "Bronchioloalveolar carcinoma, non-mucinous" finds the current Preferred term 8252/3 -- agreed.
# The hold is released, so D2 offers 8252/3 in the lung and chest pickers with its live ICD-O-3.2 terms.
PICKER_HOLDS = {}


def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology()] + nscc_nodes(7) + nscc_nodes(5) + [carcinoid()] + \
        nut_nodes(P) + [
        not_malignant(), deposit_node(P, where=WHERE)]
    tree = make_tree(TREE_ID, nodes, subtype_screens=(n("carcinoid"), n("nscc_confirm")))
    return hold_from_picker(tree, P, PICKER_HOLDS)


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]). The lu_nscc_ihc rules emit 8140/3 and
# 8070/3, so those entries require histology and immunohistochemistry and name the rules' markers
# (the generator's check_ihc_overrides; decisions() unites the lists with other trees').
# ------------------------------------------------------------------------------------------
_IHC = ["Histology", "IHC"]

DECISIONS = {
    "8240/3": ("D1, D7, D8", EVIDENCE,
               "Carcinoid tumour of the lung: typical carcinoid and carcinoid with no type or "
               "grade stated (Ozkan 2024, Chen 2026) on the neuroendocrine tumour screen, at basis "
               "5 when cytology names it, and at basis 4 with imaging and a raised chromogranin A "
               "(Visser 2023 Table 4; registrar question 7)."),
    "8249/3": ("D1", EVIDENCE,
               "Atypical carcinoid of the lung, reported in children (Ozkan 2024), on the "
               "neuroendocrine tumour screen."),
    "8241/3": ("D7", EVIDENCE,
               "Serotonin-producing carcinoid or neuroendocrine tumour of the lung at basis 4 with "
               "imaging and a raised serotonin (Visser 2023 Table 4; registrar question 7)."),
    "8158/3": ("D7", EVIDENCE,
               "Adrenocorticotropic hormone-producing neuroendocrine tumour of the lung at basis 4 "
               "with imaging and a raised adrenocorticotropic hormone (Visser 2023 Table 4; "
               "registrar question 7)."),
    "8430/3": ("D1, D8", EVIDENCE,
               "Mucoepidermoid carcinoma of the lung, the second commonest primary lung "
               "malignancy of children (Ozkan 2024, Chen 2026), on the histology screen and at "
               "basis 5 from cytology."),
    "8140/3": ("D1, D3, D8", EVIDENCE,
               "Adenocarcinoma of the lung with no subtype named (Ozkan 2024) on the histology "
               "screen and at basis 5 from cytology; a non-small cell carcinoma favouring "
               "adenocarcinoma, in words or by TTF-1 or a mucin stain, that the file confirms "
               "(SEER lung rule H3; Nicholson 2022, PDF p. 5); and acinar adenocarcinoma, whose "
               "code 8551/3 "
               "carries an obsolete Preferred term and is held off every screen until the "
               "registrar rules (D3).",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["TTF-1", "Mucin stain"]}),
    "8070/3": ("D1, D8", EVIDENCE,
               "Squamous cell carcinoma of the lung with no subtype named (Ozkan 2024) on the "
               "histology screen and at basis 5 from cytology, and a non-small cell carcinoma "
               "favouring squamous cell carcinoma, in words or by p40, that the file confirms "
               "(SEER lung rule H3; Nicholson 2022, PDF p. 6, Table 3).",
               {"diagnostic_tests_required": _IHC, "ihc_markers_required": ["p40"]}),
    "8041/3": ("D1, D8", EVIDENCE,
               "Small cell carcinoma of the lung (Ozkan 2024, Chen 2026) on the histology screen "
               "and at basis 5 from cytology."),
    "8012/3": ("D1", EVIDENCE, "Large cell carcinoma of the lung (Ozkan 2024) on the histology "
                               "screen."),
    "8013/3": ("D1", EVIDENCE,
               "Large cell neuroendocrine carcinoma of the lung, combined or not (Chen 2026), on "
               "the histology screen and for a tumour of carcinoid appearance the report calls "
               "large cell neuroendocrine carcinoma (Nicholson 2022, p. 13)."),
    "8046/3": ("D8", EVIDENCE,
               "Non-small cell carcinoma of the lung with no type named, or with a favoured type "
               "the file does not confirm, at basis 7 and at basis 5 from cytology (Nicholson "
               "2022, PDF pp. 5-6). Registrar, 8 October 2026 (review A2, E6): the favoured type "
               "is coded only when a doctor confirms it or the patient is treated for it (SEER "
               "Solid Tumor Rules, lung, rule H3)."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma of the lung whose type the report does not name, at basis 7 on the "
               "histology screen and at basis 5 when cytology names a carcinoma without its type "
               "or a type the cytology list does not hold."),
    "8023/3": ("D12, D15", EVIDENCE + ", NUT_carcinoma",
               "NUT carcinoma of the lung (Nicholson 2022, p. 3, p. 15) from the NUT carcinoma "
               "screens: basis 8 with a NUTM1 rearrangement or fusion, basis 7 otherwise."),
}
