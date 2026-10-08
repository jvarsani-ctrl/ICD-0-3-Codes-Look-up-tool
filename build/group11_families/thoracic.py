"""g11_thoracic (prefix tx_): carcinomas of the heart, pleura and other thoracic and respiratory
sites at C38.0, C38.4, C38.8 and C39.x, ICCC-3 subgroup XIf10 (range 134).

Built from docs/group_11_evidence/XIf4_lung_pleura.json, the pleura nodes (pl_site, pl_evidence,
pl_cytology, pl_histology, pl_ihc), with the builders in build/group11_common.py, in the shape of
build/group11_organs/thyroid.py. The evidence's pl_ node ids become tx_, the tree's prefix (contract
§4.1). Every option's label, code, behaviour, basis, reason and recognition aid comes from that file
unless a departure below says otherwise; the cite (file, page, quotation) is the comment above the
option. File names in the comments are the evidence's own:
    Sauter     XIf10-pleura__Sauter-2022.txt (Sauter JL, et al. The 2021 WHO Classification of
               Tumors of the Pleura. J Thorac Oncol 2022;17:608-622)
    ICCR-Meso  XIf10-pleura__ICCR-Mesothelioma-3rd.txt (ICCR Mesothelioma in the Pleura,
               Pericardium and Peritoneum Histopathology Reporting Guide, 3rd edition, version 3.1,
               September 2022)
    Nicholson  XIf4-lung__Nicholson-2022.txt (J Thorac Oncol 2022;17:362-387)
    Pfister    ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules      RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)

Nodes, in tree order:
    tx_document_inventory  document_inventory  evidence gate (evidence pl_evidence)
    tx_clinical, tx_clinical_cytology  clinical_alias
    tx_imaging, tx_imaging_cytology  morphology_only
    tx_cytology            morphology_only     (evidence pl_cytology)
    tx_histology           histology_subclassification  (evidence pl_histology)
    tx_stains              histology_subclassification  (evidence pl_ihc and ihc_rules 1-2)
    tx_not_malignant       histology_subclassification  (the exclusions of evidence pl_histology)
    tx_deposit             morphology_only      (D10)
    tx_picker              histology_subclassification  (D2; evidence pl_histology's "another
                                               carcinoma", which named the general picker)

Departures from the evidence nodes, and why
-------------------------------------------
1. pl_site is not built. The router's site capture records C38.0, C38.4, C38.8, C39.0, C39.8 and
   C39.9 and chose this tree (D14). Its options that leave these sites (the lung or a bronchus, to
   g11_lung; the mediastinum or thymus, to g11_thymus; the chest or chest wall with no organ named,
   Rule A, to the site the tumour type implies) are router answers.
2. pl_evidence: the referral and imaging-only tiers recorded 8000/3 at basis 1 and 2 on the gate,
   and "possible, probable or suspected" was one not-registrable tier. D7: each tier routes to its
   own screen, which refers 8000/3 to Group XII (ICCC-2017 range 143: XIIb at every routed site;
   evidence conflicts, Group 12, registrar question 6). Visser rule 4 makes "possible" not
   registrable and "probable" registrable, so the hint drops "probable"; "Choose the strongest
   report" is dropped, because the document checklist replaces it. The evidence gives no laboratory
   test and no Visser Table 4 row concerns these sites, so the gate has no marker tier.
3. pl_cytology: "Carcinoma, and the file names the organ where the tumour began" went to a site
   capture with recapture_site. A referral to Group XI itself is not built (SELF_REFERRAL is False,
   D10), and the deposit question cannot be reached from cytology, because its "carcinoma whose
   primary has not been found" option continues in the unspecified tree's histology screen, where
   every code is basis 7. The instruction moves to the cytology screen's hint instead: the deposit
   is coded at the organ the file names, from the site step. "Malignant cells, with no tumour type
   named" (8000/3 basis 5) is the common referral to Group XII with 8001 (D8). The evidence's
   suspicious line becomes the common one, with "reactive or atypical mesothelial cells" as its own
   not-registrable line, from the evidence's hint.
4. pl_histology: the five non-malignant lines (two well-differentiated papillary mesothelial
   tumours, adenomatoid tumour, mesothelioma in situ, cardiac rhabdomyoma) move to tx_not_malignant,
   reached by the standard option, whose label names them (thyroid departure 5).
5. pl_histology, deposits. The evidence's deposit option (site capture with recapture) is the
   common deposit question (D10); its "A carcinoma that has spread here, and the organ where it
   began is not known" (8010/3, topography_override C80.9) is that question's "A carcinoma whose
   primary has not been found", which continues at C80.9 in the unspecified tree's histology screen.
6. pl_histology, "A malignant tumour, with no type named" (8000/3 basis 7) is the common referral to
   Group XII with 8000 (D7). The trailing options are the common ones (tail_options), with the
   leukaemia, germ cell and other-named referrals the evidence lacks.
7. pl_ihc is built as a choice, tx_stains, not as an ihc_checklist. Its first rule refers to Group
   XII and its second goes on to a question (where the carcinoma began), and an ihc_checklist rule
   can do neither: a rule emits a code. Its fallback, 8000/3, is a Group XII code, and an
   ihc_checklist's fallback must be a Group XI entry. So the panel is three answers: the mesothelioma
   pattern refers to Group XII; the carcinoma pattern goes to the deposit question (the evidence's
   outcome; data gap 5: no primary carcinoma of the pleura, pericardium or heart is reported); and
   neither pattern refers to Group XII with 8000. The nut_nodes() precedent in group11_common
   builds NUT_carcinoma.json's nut_ihc the same way. The "two or more of" conditions are written
   in the labels, so the clerk reads them off the report. Its third rule, thoracic
   SMARCA4-deficient undifferentiated tumour on 8044/3, is not built (D4; registrar question 3), and
   no screen names the entity.
8. Melanoma (D13): the pleura and heart are none of skin, eye or central nervous system, so the hop
   enters me_mucosa, as the thyroid's and the lung's do (evidence conflicts: T2c to confirm the
   melanoma tree takes a melanoma of an internal organ).
9. tx_picker: D2 replaces the general picker the evidence named (gc_picker). ICCC-2017 range 134
   places the whole shared carcinoma list in XIf10 at every routed site, so the picker offers the
   lung-specific codes too (8250/3 Lepidic adenocarcinoma, 8253/3, 8254/3, 8256/3, 8257/3), which
   the evidence's Rule H row says are offered only at the lung. D2 and validator rule 4 decide; the
   build report lists them for the registrar. 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous is
   held off this picker as off the lung's (registrar question 4; lung module departure 15).
10. Not built from the evidence: the thoracic SMARCA4-deficient undifferentiated tumour (D4), a code
   for mesothelioma in situ (9050/2 is not in ICD-O-3.2; registrar question 5).

Registrar questions 3, 5 and 6 of the evidence stay open; the defaults above apply until they are
answered (docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, code, deposit_node, evidence_gate, excl, go,
                            make_tree, named, node, nonrep, not_malignant_node, rec, refer,
                            refer_germ_cell, refer_leukaemia, refer_other_named,
                            refer_sarcoma, refer_unspecified, tail_options, term)
from group11_organs.lung import PICKER_HOLDS, hold_from_picker, referral_reason

TREE_ID = "g11_thoracic"
P = "tx_"
WHERE = "the pleura, the heart or another thoracic or respiratory site"
EVIDENCE = "XIf4_lung_pleura"


def n(name: str) -> str:
    return P + name


# Sauter p. 2 "Diffuse mesothelioma, NOS 9050/3b", "Sarcomatoid mesothelioma 9051/3",
# "Epithelioid mesothelioma 9052/3", "Mesothelioma, biphasic 9053/3". ICCC-2017: 9050-9053 at
# every routed site -> XIIa5.
MESO_REASON = (
    "ICD-O-3.2 codes mesothelioma from %s (9050/3) to %s (9053/3), and ICCC-3 places those codes "
    "in Group XII (other and unspecified malignant neoplasms), not Group XI. Code the case from "
    "the Group XII tree." % (term("9050", "3"), term("9053", "3")))
MESO_NOTE = ("Evidence conflicts, Group 12: mesothelioma is ICCC-2017 XIIa5 at every site. "
             "Sauter 2022, p. 2.")

# Evidence pl_cytology option 0 (departure 3). ICCR-Meso p. 6 "to definitively rule out metastasis
# from a known tumour"; Sauter p. 2 'titled "Metastasis to the pleura" was added to the 2021
# classification'.
CYTOLOGY_DEPOSIT = (" A carcinoma in pleural or pericardial fluid that the file says began in "
                    "another organ is a deposit: it is coded at that organ. Go back to the site "
                    "step and record the organ the file names.")


def lymphoma():
    """The common lymphoma referral (refer_lymphoma) names the site twice; with this tree's
    six-site phrase that sentence does not read, so the same content is written once here."""
    # Rules p. 2 (printed p. 15) "Code extranodal lymphomas to the site of origin".
    return refer("Lymphoma", 2,
                 "A lymphoma belongs to ICCC-3 Group II. A lymphoma that arises in %s keeps that "
                 "site (WHO Rule D: an extranodal lymphoma is coded to its site of origin). Code "
                 "the case from the Group II (lymphomas) tree." % WHERE,
                 note="ICD-O-3.1 Rule D, p. 15. The hop carries the case's site. Evidence "
                      "pl_cytology option 4 and pl_histology option 11.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence pl_evidence, pl_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour of the pleura, heart or another thoracic "
                 "site?",
        # Evidence pl_evidence hint, less "Choose the strongest report" and "probable"
        # (departure 2).
        hint=("A radiology report counts as imaging. Cytology of pleural or pericardial fluid, or "
              "of a needle aspirate, counts as cytology. A pathology report on a biopsy or "
              "resection counts as histology. A biopsy or cytology report that calls the "
              "specimen inadequate or non-diagnostic counts as no tissue. A report that calls the "
              "tumour possible or suspected cancer does not register it."),
        tier_labels={
            "cytology": "A cytology report (pleural or pericardial fluid, or a needle aspirate) - "
                        "no histology report",
            "histology": "A histology report on a biopsy or resection, with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=[
            # Evidence pl_cytology option 2. Sauter p. 2 "Diffuse mesothelioma, NOS 9050/3b".
            refer("Mesothelioma", 12, MESO_REASON, note="Evidence pl_cytology option 2. " +
                                                       MESO_NOTE),
            # Evidence pl_cytology option 1. Rules p. 6 (printed p. 19) "the appropriate code is
            # C80.9 (unknown primary site) 8010/3".
            code("Carcinoma, and the file does not name the organ where it began", "8010", "3", 5,
                 "%s A carcinoma whose site of origin is not known is recorded at C80.9, unknown "
                 "primary site (WHO coding guidelines, ICD-O-3.1, printed p. 19). Cytology does "
                 "not give the full histological type; a histology report confirms it."
                 % rec("8010", "3", 5),
                 captures={"topography": "C80.9", "workup_status": "incomplete",
                           "basis_evidence_tier": "cytology_named"},
                 note="D8, D10. Evidence pl_cytology option 1 (topography_override C80.9, carried "
                      "as a topography capture; app.js applies captures before finish()). "
                      "ICCC-2017 range 136 places 8010/3 at C80.9 in XIf11."),
            # Evidence pl_cytology hint "Reactive or atypical mesothelial cells are not a
            # diagnosis of cancer."
            nonrep("Reactive or atypical mesothelial cells",
                   "Reactive or atypical mesothelial cells are not a diagnosis of cancer, so "
                   "nothing is registered.",
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "cytology_reactive_mesothelial"},
                   note="Evidence pl_cytology hint and option 5 (departure 3)."),
            # Evidence pl_cytology option 4.
            lymphoma(),
        ],
        note="Evidence pl_evidence and pl_cytology (departures 2 and 3 in the module docstring).")
    for nd in nodes:
        if nd["node_id"] == n("cytology"):
            nd["hint"] += CYTOLOGY_DEPOSIT
            nd["coding_note"] += (" The hint's last sentences carry evidence pl_cytology option 0 "
                                  "(thoracic module departure 3).")
    return nodes


# ------------------------------------------------------------------------------------------
# Histology (evidence pl_histology)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # Sauter p. 2 "Localized mesothelioma 9050/3b", "Sarcomatoid mesothelioma 9051/3",
        # "Epithelioid mesothelioma 9052/3", "Mesothelioma, biphasic 9053/3".
        refer("Mesothelioma of any type: diffuse or localized, epithelioid, sarcomatoid, "
              "desmoplastic or biphasic", 12, MESO_REASON,
              note="Evidence pl_histology option 0. " + MESO_NOTE),
        # Evidence pl_histology option 8 and pl_ihc (departure 7).
        go("A malignant tumour the report does not type, with immunohistochemistry that compares "
           "mesothelioma and carcinoma", n("stains"), note="Evidence pl_histology option 8."),
        # Nicholson p. 3 "Pleuropulmonary blastoma 8973/3". ICCC-2017: 8973 -> XIIa3.
        refer("Pleuropulmonary blastoma", 12,
              referral_reason("8973", "Group XII (other and unspecified malignant neoplasms)",
                              "Group XII tree"),
              note="Evidence pl_histology option 9; ICCC-2017 XIIa3 at every site."),
        # Evidence pl_histology option 13 ("Carcinoma, with no type named", 8010/3). Data gap 5:
        # no primary carcinoma of these sites is reported.
        named("Carcinoma, with no type named", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence pl_histology option 13; the generic option of the screen."),
    ] + tail_options(
        P, "mucosa", where=WHERE,
        not_malignant_label="A benign tumour or one of uncertain behaviour, such as a "
                            "well-differentiated papillary mesothelial tumour, an adenomatoid "
                            "tumour, mesothelioma in situ or a cardiac rhabdomyoma",
        referrals=[
            # Evidence pl_histology option 11.
            lymphoma(),
            refer_leukaemia(WHERE),
            # Evidence pl_histology option 10. Sauter p. 2 "Mesenchymal tumors of the pleura have
            # been moved to a new chapter".
            refer_sarcoma(WHERE),
            refer_germ_cell(WHERE),
            refer_other_named(),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence pl_histology hint.
        "Mesothelioma is coded in Group XII. A carcinoma in the pleura, pericardium or heart that "
        "began in another organ is a deposit: choose a deposit of a tumour that began elsewhere, "
        "and the case is coded at that organ.",
        opts, [],
        "Evidence pl_histology (departures 4 to 8). Data gap 5: Sauter 2022 and the ICCR "
        "mesothelioma dataset name no primary carcinoma of the pleura, pericardium or heart, so "
        "the screen offers carcinoma with no type named, the picker and the deposit question.")


def stains():
    marks = ("calretinin, WT1, cytokeratin 5/6 and D2-40", "claudin 4, MOC31, BG8 and BerEP4")
    return node(
        n("stains"), "histology_subclassification", 4, "Stain panel",
        "Which pattern does the immunohistochemistry report give?",
        # Evidence pl_ihc hint; ICCR-Meso p. 12 "at least two mesothelial and two carcinoma
        # markers with greater than 80%".
        "Mesothelial markers are %s (podoplanin). Carcinoma markers are %s. Answer from the stains "
        "the report calls positive or negative." % marks,
        [
            # Evidence ihc_rules 1. ICCR-Meso p. 12 "The most useful mesothelial markers are
            # calretinin, WT-1, cytokeratin 5/6"; "at least two mesothelial and two carcinoma
            # markers with greater than 80%".
            refer("Two or more mesothelial markers (calretinin, WT1, cytokeratin 5/6, D2-40) are "
                  "positive, and the carcinoma markers (claudin 4, MOC31, BG8, BerEP4) are "
                  "negative", 12,
                  "This is the mesothelioma pattern (ICCR mesothelioma dataset, 3rd edition, "
                  "p. 12). " + MESO_REASON,
                  note="Evidence ihc_rules 1 (pl_ihc), built as a choice (departure 7)."),
            # Evidence ihc_rules 2. Sauter p. 7 "Claudin 4 with membranous and cytoplasmic
            # staining has emerged as a reliable carcinoma marker"; ICCR-Meso p. 12 "carcinoma
            # markers are claudin 4,31 MOC31, BG829,32 and BerEp4".
            go("Claudin 4 is positive, or two or more of MOC31, BG8 and BerEP4 are positive, and "
               "the mesothelial markers are negative", n("deposit"),
               note="Evidence ihc_rules 2: 'carcinoma: the next question asks whether the report "
                    "names the organ where it began' (departure 7; D10)."),
            # Evidence pl_ihc fallback: 8000/3 'the markers do not settle the tumour type'. D7.
            refer_unspecified("Neither pattern, or the report gives too few stains to decide",
                              "8000", 7, "The stains do not settle the tumour type.",
                              where=WHERE,
                              note="Evidence pl_ihc fallback (8000/3), a Group XII code at these "
                                   "sites: refer_code 8000 (D7; departure 7)."),
        ], [],
        "Evidence pl_ihc and ihc_rules 1-2, built as a choice (departure 7). The 8044/3 rule "
        "(thoracic SMARCA4-deficient undifferentiated tumour, Sauter 2022, p. 10) is not built: "
        "D4, registrar question 3.")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # Sauter p. 2 "Well-differentiated papillary mesothelial tumor 9052/1b".
            excl("Well-differentiated papillary mesothelial tumour (well-differentiated papillary "
                 "mesothelioma) of the pleura", "9052", "1",
                 what="a well-differentiated papillary mesothelial tumour of the pleura",
                 note="Evidence pl_histology option 1. Rule H: ICD-O-3.2 prints the /1 term for "
                      "the pleura only."),
            # Evidence pl_histology option 2; icdo32.sqlite 9052/0 Related Well differentiated
            # papillary mesothelioma.
            excl("Well-differentiated papillary mesothelial tumour of the pericardium", "9052",
                 "0",
                 what="a well-differentiated papillary mesothelial tumour away from the pleura",
                 extra="ICD-O-3.2 gives Well differentiated papillary mesothelioma as a related "
                       "term of this code, and codes the tumour of the pleura 9052/1.",
                 note="Evidence pl_histology option 2; Rule H."),
            # Sauter p. 2 "Adenomatoid tumor 9054/0".
            excl("Adenomatoid tumour", "9054", "0", what="an adenomatoid tumour",
                 note="Evidence pl_histology option 3."),
            # Sauter p. 2 "Mesothelioma in situ 9050/2c". Registrar question 5.
            nonrep("Mesothelioma in situ",
                   "Mesothelioma in situ is not a malignant tumour and ICD-O-3.2 gives it no code, "
                   "so it is not registered.",
                   note="Evidence pl_histology option 4; code_currency 9050/2 (WHO prints it, "
                        "ICD-O-3.2 lacks it); registrar question 5."),
            # Pfister p. 14 "Heart Cardiac rhabdomyoma".
            excl("Cardiac rhabdomyoma", "8900", "0", what="a cardiac rhabdomyoma",
                 note="Evidence pl_histology option 5."),
        ],
        where=WHERE,
        note="The five non-malignant lines of evidence pl_histology (departure 4).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), stains(), not_malignant(), deposit_node(P, where=WHERE)]
    return hold_from_picker(make_tree(TREE_ID, nodes), P, PICKER_HOLDS)


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8010/3": ("D8, D10", EVIDENCE,
               "Carcinoma of the pleura, heart or another thoracic or respiratory site whose type "
               "the report does not name, at basis 7 on the histology screen, and at basis 5 at "
               "C80.9 when pleural or pericardial fluid cytology shows a carcinoma and the file "
               "does not name the organ where it began. No primary carcinoma of these sites is "
               "reported (evidence data gap 5)."),
}
