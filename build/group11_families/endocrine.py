"""g11_endocrine (prefix en_): carcinomas of the parathyroid gland and other endocrine glands at
C75.0, C75.2, C75.4, C75.5, C75.8 and C75.9, ICCC-3 subgroup XIf10 (range 134).

Built from docs/group_11_evidence/XIf10_parathyroid_other_unspecified.json, the parathyroid and
endocrine nodes (pt_evidence, pt_clinical, pt_imaging, pt_cytology, pt_histology, en_evidence,
en_clinical, en_imaging, en_histology), with the builders in build/group11_common.py, in the shape
of build/group11_organs/thyroid.py. The evidence's pt_ and en_ node ids become en_, the tree's
prefix (contract §4.1). Every option's label, code, behaviour, basis, reason and recognition aid
comes from that file unless a departure below says otherwise; the cite (file, page, quotation) is
the comment above the option. File names in the comments are the evidence's own:
    ICCR      XIf10-parathyroid__ICCR-Parathyroid-2nd.txt (ICCR Parathyroid Carcinoma and Atypical
              Parathyroid Neoplasm Histopathology Reporting Guide, 2nd edition, version 2.0,
              November 2025). "image" marks a quotation read from the page image (Table 1, PDF
              p. 9).
    Erickson  XIf10-parathyroid__Erickson-2022.txt (Erickson LA, et al. Overview of the 2022 WHO
              Classification of Parathyroid Tumors. Endocr Pathol 2022;33:64-89)
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser    Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
              set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    en_document_inventory  document_inventory  evidence gate (evidence pt_evidence, en_evidence)
    en_clinical, en_clinical_cytology  clinical_alias
    en_imaging, en_imaging_cytology  morphology_only
    en_cytology            morphology_only     (evidence pt_cytology)
    en_histology           histology_subclassification  (evidence pt_histology, en_histology)
    en_not_malignant       histology_subclassification  (the exclusions of evidence pt_histology)
    en_deposit             morphology_only      (D10)
    en_picker              histology_subclassification  (D2; evidence ou_picker)

Departures from the evidence nodes, and why
-------------------------------------------
1. One tree for the parathyroid and the other endocrine sites. The evidence has pt_ nodes for C75.0
   and en_ nodes for C75.2, C75.4, C75.5, C75.8 and C75.9. The engine cannot filter options by site
   inside one tree (D14), so the pt_ and en_ histology screens are one screen, en_histology, and
   the three clinical screens, the two imaging screens and the cytology screen are written once.
2. Tissue-free routes (D7). The evidence's clinical and imaging screens refer a craniopharyngioma
   or another tumour at the craniopharyngeal duct to Group III with refer_code 8000, and a
   paraganglioma to Group IV, without tissue. The build's walk (rule C) admits only a Group XII
   referral with 8000 or 8001 on a path with no tissue, so those options are not built on the
   tissue-free screens. The histology screen and the cytology screen refer them (Group III and
   Group IV, with tissue). Each tissue-free route to Group XII carries a guard in its label, "not
   a craniopharyngioma or a paraganglioma", because ICCC-2017 places 8000/3 and 8001/3 at the
   craniopharyngeal duct (C75.2) in Group III (IIIf), not Group XII. Request 1 (below the
   docstring's departures, in the module's return) asks the walk to admit a Group III or Group IV
   referral at a site ICCC-2017 places there.
3. The evidence's deposit options on the clinical, imaging and cytology screens (a referral to
   Group XI with recapture_site) are not built: a referral to Group XI itself is not built
   (SELF_REFERRAL is False, D10), and the deposit question cannot be reached from a tissue-free
   or cytology path, because its "carcinoma whose primary has not been found" option continues
   in the unspecified tree's histology screen, where every code is basis 7. The instruction moves
   to the gate's hint: a deposit is coded at the organ where it began, from the site step.
4. pt_evidence and en_evidence: "possible or suspected" and the adenoma, hyperplasia and
   hyperparathyroidism lines are the common not-registrable screens, and the document checklist
   decides the tier (contract §9 item 5), so the escape "A pathology report is in the file after
   all" is not built. The evidence's calcium and parathyroid hormone results register no code, so
   the gate has no laboratory screen and no marker tier: the hint says so (Visser Table 4 has no
   parathyroid row; evidence lab_tests rows 1 and 2).
5. pt_cytology. Cytology of a deposit away from the gland that the report calls metastatic
   parathyroid carcinoma records 8140/3 at basis 5 (D8) and re-sites the case to C75.0; cytology
   of the gland itself is not registrable. Added from the common cytology options: a carcinoma
   whose type the report does not name (8010/3, basis 5), a paraganglioma (Group IV) and a
   craniopharyngioma (Group III).
6. pt_histology. "Parathyroid carcinoma" records 8140/3 and captures C75.0 (Rule H: ICD-O-3.2 prints
   C75.0 beside the related term). The five non-malignant lines (atypical parathyroid tumour,
   adenoma, lipoadenoma, hyperplasia) move to en_not_malignant, reached by the standard option,
   whose label names them. The evidence's "A deposit (metastasis) of a tumour that began
   elsewhere, or a tumour of the thyroid" is the common deposit question (D10); its lymphoma and
   sarcoma lines are the common referrals.
7. Water-clear cell and oncocytic parathyroid carcinoma (8322/3, 8290/3) are not options: the WHO
   table prints only 8140/3 (ICCR p. 9), and registrar question 2 stays open. The hint states the
   Rule K choice and 8322/3 and 8290/3 are picker entries (D5). Because the screen offers 8140/3
   only under the narrower label "Parathyroid carcinoma", the picker keeps Adenocarcinoma, NOS
   (picker_keep).
8. The evidence's parafibromin-deficient neoplasm with no stated diagnosis (registrar question 3)
   reaches the common not-registrable line of the exclusion screen, and the histology hint says a
   report that adds "parafibromin-deficient" still names carcinoma, atypical tumour or adenoma.
9. en_histology: "A pituitary tumour or a pineal tumour" (Group III) is built as the evidence has
   it, from en_histology option 2; the evidence's own conflicts note places the pituitary (C75.1)
   and pineal (C75.3), which this tree does not route, in Group III.
10. Melanoma (D13): the endocrine glands are none of skin, eye or central nervous system, so the
   hop enters me_mucosa, as the thyroid's does.

Registrar questions 1 to 3 of the evidence stay open; the defaults above apply until they are
answered (docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

from group11_common import (code, cyto, cyto_carcinoma_nos, deposit_node, evidence_gate, excl, go,
                            make_tree, named, node, nonrep, not_malignant_node, rec, refer,
                            refer_germ_cell, refer_leukaemia, refer_other_named, refer_sarcoma,
                            refer_unspecified, tail_options, term, aid)

TREE_ID = "g11_endocrine"
P = "en_"
WHERE = "the parathyroid gland or another endocrine gland"
EVIDENCE = "XIf10_parathyroid_other_unspecified"
GUARD = " (not a craniopharyngioma or a paraganglioma, which Group III and Group IV code)"


def n(name: str) -> str:
    return P + name


def lymphoma():
    """The common lymphoma referral (refer_lymphoma) names the site twice; with this tree's
    phrase that sentence does not read, so the same content is written once here."""
    # Evidence pt_histology option 5. Rules p. 2 (printed p. 15) "Code extranodal lymphomas to
    # the site of origin".
    return refer("Lymphoma", 2,
                 "A lymphoma belongs to ICCC-3 Group II. A lymphoma that arises in an endocrine "
                 "gland keeps that gland as its site (WHO Rule D: an extranodal lymphoma is coded "
                 "to its site of origin). Code the case from the Group II (lymphomas) tree.",
                 note="ICD-O-3.1 Rule D, p. 15. The hop carries the case's site. Evidence "
                      "pt_histology option 5.")


PARAGANGLIOMA_REASON = ("Paragangliomas are coded in ICCC-3 Group IV (neuroblastoma and other "
                        "peripheral nervous cell tumours) at every site. Code the case from the "
                        "Group IV tree.")
CRANIOPHARYNGIOMA_REASON = ("Craniopharyngioma is coded in ICCC-3 Group III (central nervous "
                            "system and miscellaneous intracranial and intraspinal neoplasms). "
                            "Code the case from the Group III tree.")
DEPOSIT_HINT = (" Cytology of a carcinoma that the file says began in another organ is a deposit: "
                "it is coded at that organ. Go back to the site step and record the organ the "
                "file names.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence pt_evidence, en_evidence, pt_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour of the parathyroid or another endocrine "
                 "gland?",
        # Evidence pt_evidence hint; pt_clinical hint ("High serum calcium and parathyroid
        # hormone raise the question of carcinoma. They do not establish it"); ICCR p. 6 "the
        # diagnosis is not made until surgical inspection and/or histologic review"; Rules p. 7
        # (printed p. 20) "indicating that the associated topography code is not the site of
        # origin". The evidence's deposit options become this hint (departure 3).
        hint=("A radiology report counts as imaging. A parathyroidectomy or another resection "
              "report counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. An immunohistochemistry or "
              "gene report on its own does not stand in for a histology report. Serum calcium "
              "and parathyroid hormone results raise the question of parathyroid carcinoma and "
              "do not register it. A deposit of a cancer that began in another organ is coded "
              "at that organ: go back to the site step and record the organ the file names. A "
              "paraganglioma, a craniopharyngioma, a pituitary tumour or a pineal tumour is "
              "coded in its own group: go back and search its name. A report that calls the "
              "tumour possible or suspected does not register it."),
        unspecified=refer_unspecified,
        tier_labels={
            "imaging": "An imaging report (ultrasound, CT, MRI or a nuclear medicine scan) - no "
                       "tissue",
            "cytology": "Cytology only - a fine-needle aspirate, a smear or a fluid sample; no "
                        "histology report",
            "histology": "A histology report: parathyroidectomy, biopsy or other resection, with "
                         "or without immunohistochemistry or gene reports",
        },
        cytology=[
            # Evidence pt_cytology option 0. ICCR p. 1 "histologically/cytologically documented
            # metastatic disease"; p. 9 image "Parathyroid carcinoma 8140/3".
            cyto("Cytology of a deposit away from the parathyroid gland, which the report calls "
                 "metastatic parathyroid carcinoma", "8140",
                 "ICD-O-3.2 lists Parathyroid carcinoma under this code. A metastasis documented "
                 "on cytology is one of the criteria for parathyroid carcinoma. The case is "
                 "recorded at the parathyroid gland (C75.0).",
                 note="Evidence pt_cytology option 0 (departure 5). Rule H: topography C75.0."),
            # Evidence pt_cytology option 1. ICCR p. 6 "For clinically suspected parathyroid
            # carcinoma, a preoperative biopsy is not recommended."; p. 8 "The diagnosis of
            # parathyroid carcinoma is restricted to a parathyroid neoplasm that shows one of the
            # followings".
            nonrep("Cytology of the parathyroid gland itself, naming a parathyroid lesion, a "
                   "parathyroid neoplasm or atypical cells",
                   "Cytology of the gland cannot show the invasion that defines parathyroid "
                   "carcinoma, so carcinoma is not established. Register the case when the "
                   "resection report names carcinoma.",
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "cytology_parathyroid_gland"},
                   note="Evidence pt_cytology option 1."),
            # Evidence en_histology option 0; Pfister p. 14 "Parasympathetic paraganglioma (H&N
            # paraganglioma)", "Sympathetic paraganglioma".
            refer("A paraganglioma, including a carotid body or aortic body tumour", 4,
                  PARAGANGLIOMA_REASON,
                  note="Evidence en_histology option 0, offered on the cytology screen (departure "
                       "5)."),
            # Evidence en_histology option 1; Pfister p. 18 "Adamantinomatous craniopharyngioma".
            refer("A craniopharyngioma, or a pituitary or pineal tumour", 3,
                  CRANIOPHARYNGIOMA_REASON,
                  note="Evidence en_histology options 1 and 2, offered on the cytology screen "
                       "(departure 5)."),
            cyto_carcinoma_nos(note="Added from the common cytology options (departure 5): a "
                                    "carcinoma is an entity, 8010/3 at basis 5. Malignant cells "
                                    "with no tumour type refer to Group XII with 8001 instead."),
        ],
        note="Evidence pt_evidence, en_evidence and pt_cytology (departures 1 to 5 in the module "
             "docstring).")
    for nd in nodes:
        if nd["node_id"] == n("cytology"):
            nd["hint"] += DEPOSIT_HINT
            nd["coding_note"] += (" The hint's last sentences carry the evidence's deposit "
                                  "option (endocrine module departure 3).")
            for o in nd["options"]:
                if o.get("morphology_code") == "8140":
                    o["captures"]["topography"] = "C75.0"
        # Departure 2: ICCC-2017 places 8000/3 and 8001/3 at the craniopharyngeal duct in
        # Group III, so every route to Group XII says so.
        for o in nd.get("options") or []:
            if o.get("refer_group") == 12 and o.get("refer_code") in ("8000", "8001"):
                o["label"] += GUARD
                o["coding_note"] += (" The label's guard: ICCC-2017 places this code at the "
                                     "craniopharyngeal duct (C75.2) in Group III, and the walk "
                                     "admits no Group III route without tissue (departure 2).")
    return nodes


# ------------------------------------------------------------------------------------------
# Histology (evidence pt_histology, en_histology)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # ICCR p. 9 image "Parathyroid carcinoma 8140/3"; p. 8 "The diagnosis of parathyroid
        # carcinoma is restricted to a parathyroid neoplasm that shows one of the followings";
        # Pfister p. 14 "Parathyroid endocrine tumors", p. 19 "Hyperparathyroidism jaw tumor
        # syndrome". D1: registrar question 1.
        aid(named("Parathyroid carcinoma", "8140",
                  "ICD-O-3.2 lists Parathyroid carcinoma as a related term of this code, at the "
                  "parathyroid gland (C75.0).",
                  captures={"topography": "C75.0"},
                  note="Evidence pt_histology option 0; D1 (registrar question 1). Rule H: "
                       "topography C75.0, which ICD-O-3.2 prints beside the related term."),
            "The report describes invasion of a blood vessel, a lymphatic, a nerve or a "
            "neighbouring structure, or a metastasis."),
        # Evidence en_histology option 0. Pfister p. 14 "Parasympathetic paraganglioma (H&N
        # paraganglioma)", "Sympathetic paraganglioma".
        refer("Paraganglioma, including carotid body paraganglioma (carotid body tumour) and "
              "aortic body paraganglioma", 4, PARAGANGLIOMA_REASON,
              note="Evidence en_histology option 0."),
        # Evidence en_histology option 1. Pfister p. 18 "Adamantinomatous craniopharyngioma".
        refer("Craniopharyngioma", 3, CRANIOPHARYNGIOMA_REASON,
              note="Evidence en_histology option 1."),
        # Evidence en_histology option 2. Pfister p. 18 "Pituitary blastoma".
        refer("A pituitary tumour (pituitary neuroendocrine tumour, pituitary blastoma, pituitary "
              "carcinoma) or a pineal tumour", 3,
              "Pituitary and pineal tumours are coded in ICCC-3 Group III (central nervous "
              "system and miscellaneous intracranial and intraspinal neoplasms). Code the case "
              "from the Group III tree.",
              note="Evidence en_histology option 2."),
    ] + tail_options(
        P, "mucosa", where=WHERE,
        not_malignant_label="An atypical parathyroid tumour, a parathyroid adenoma or "
                            "lipoadenoma, parathyroid hyperplasia, or another tumour the report "
                            "calls benign, borderline or in situ",
        referrals=[
            lymphoma(),
            refer_leukaemia(WHERE),
            # Evidence pt_histology option 6.
            refer_sarcoma(WHERE),
            refer_germ_cell(WHERE),
            refer_other_named(),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence pt_histology hint and en_histology hint. ICD-O-3.1 §4.3.8 (Rule K).
        "Use the diagnosis line of the report. Parathyroid carcinoma requires invasion or a "
        "metastasis. A tumour with worrying features and no invasion is an atypical parathyroid "
        "tumour. A report that adds the words parafibromin-deficient still names one of these "
        "diagnoses: choose that diagnosis. The carotid body and the aortic body are paraganglia. "
        "A pituitary or pineal tumour belongs to the central nervous system group. When one "
        "tumour carries two type names and no single answer names both, choose the higher code "
        "number: a water-clear cell or oncocytic parathyroid carcinoma is found under another "
        "carcinoma the report names.",
        opts, [],
        "Evidence pt_histology and en_histology merged (departure 1). Water-clear cell and "
        "oncocytic parathyroid carcinoma are picker entries (departure 7).")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # Evidence pt_histology option 1. ICCR p. 9 image "Atypical parathyroid tumour
            # 8140/1"; p. 8 "atypical parathyroid neoplasm; parathyroid tumour of low or
            # uncertain malignant potential"; Erickson p. 1 "This entity is now being replaced
            # with the term of".
            aid(excl("Atypical parathyroid tumour (also written atypical parathyroid neoplasm, "
                     "or parathyroid tumour of low or uncertain malignant potential; formerly "
                     "atypical parathyroid adenoma)", "8140", "1",
                     what="an atypical parathyroid tumour",
                     note="Evidence pt_histology option 1."),
                "The report lists worrying features, such as fibrous bands, mitoses or necrosis, "
                "and finds no invasion."),
            # Evidence pt_histology option 2. ICCR p. 9 image "Parathyroid adenoma 8140/0".
            excl("Parathyroid adenoma, in one gland or in several glands (multiglandular "
                 "parathyroid disease); chief cell, oncocytic or water-clear cell adenoma",
                 "8140", "0", what="a parathyroid adenoma",
                 note="Evidence pt_histology option 2."),
            # Evidence pt_histology option 3. ICCR p. 9 image "Parathyroid lipoadenoma 8324/0".
            excl("Parathyroid lipoadenoma", "8324", "0", what="a parathyroid lipoadenoma",
                 note="Evidence pt_histology option 3."),
            # Evidence pt_histology option 4. Erickson p. 1 "is now used primarily in the
            # setting of secondary hyperplasia".
            nonrep("Parathyroid hyperplasia, including hyperplasia with kidney failure",
                   "Parathyroid hyperplasia is not a tumour. It is not registered.",
                   note="Evidence pt_histology option 4."),
        ],
        where=WHERE,
        note="The non-malignant lines of evidence pt_histology (departure 6). A report that "
             "names only a parafibromin-deficient neoplasm and states no diagnosis reaches the "
             "catch-all line (departure 8; registrar question 3).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), not_malignant(), deposit_node(P, where=WHERE)]
    return make_tree(TREE_ID, nodes, picker_keep=("8140",))


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8140/3": ("D1, D8", EVIDENCE,
               "Parathyroid carcinoma on the histology screen at basis 7, and at basis 5 when "
               "cytology of a deposit away from the gland calls it metastatic parathyroid "
               "carcinoma; the case is recorded at C75.0. ICD-O-3.2 lists Parathyroid carcinoma "
               "as a related term of Adenocarcinoma, NOS (ICCR Table 1 prints 8140/3). Rare in "
               "children: Pfister 2022 Table 3 lists parathyroid endocrine tumours without "
               "naming carcinoma (registrar question 1)."),
    "8010/3": ("D8", EVIDENCE,
               "Carcinoma whose type the cytology report does not name, at basis 5 on the "
               "cytology screen."),
}
