"""g11_adrenal (prefix ad_): adrenal cortical carcinoma at C74.0, C74.1 and C74.9, ICCC-3 subgroup XIa.

Built from docs/group_11_evidence/XIa_adrenal_cortex.json (the evidence agent's nodes ac_evidence,
ac_clinical, ac_imaging, ac_cytology, ac_imaging_cytology, ac_histology, ac_behaviour,
ac_ihc_carcinoma, ac_ihc_malignant) with the builders in build/group11_common.py, in the shape of
the thyroid exemplar. Every option's label, code, behaviour, basis, reason and recognition aid
comes from that file; the cite (file, PDF page, quotation) is the comment above the option or the
aid. File names in the comments are the evidence's own:
    ICCR      XIa-adrenal-cortex__ICCR-Adrenal-Cortex-2nd.txt (ICCR Carcinoma of the Adrenal
              Cortex Histopathology Reporting Guide, 2nd edition, version 2.0, November 2025).
              "image" marks a quotation read from the page image (Table 1, PDF p. 7).
    Mete      XIa-adrenal-cortex__Mete-2022.txt (Mete O, et al. Overview of the 2022 WHO
              Classification of Adrenal Cortical Tumors. Endocr Pathol 2022;33:155-196)
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser    Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
              set)

Nodes, in tree order:
    ad_document_inventory  document_inventory  evidence gate (evidence ac_evidence)
    ad_clinical, ad_clinical_cytology  clinical_alias  (evidence ac_clinical)
    ad_imaging, ad_imaging_cytology    morphology_only (evidence ac_imaging, ac_imaging_cytology)
    ad_cytology            morphology_only     (evidence ac_cytology)
    ad_site_cytology       site_resolution     (D9; the cytology 8370/3 of evidence ac_cytology)
    ad_histology           histology_subclassification  (evidence ac_histology)
    ad_wieneke, ad_wieneke_score  histology_subclassification  (registrar, 8 October 2026,
                                               review A2, E6: the Wieneke score, Mete 2022 Table 6)
    ad_behaviour           histology_subclassification  (evidence ac_behaviour)
    ad_sf1_carcinoma       histology_subclassification  (evidence ac_ihc_carcinoma)
    ad_sf1_malignant       histology_subclassification  (evidence ac_ihc_malignant)
    ad_site                site_resolution     (D9; every histology 8370/3)
    ad_not_malignant       histology_subclassification  (the exclusions of evidence ac_histology)
    ad_deposit             morphology_only     (D10)
    ad_picker              histology_subclassification  (D2)

Departures from the evidence nodes, and why
-------------------------------------------
1. ac_evidence: the gate's options are the contract §4.2 tiers (D7); the gate becomes a document
   checklist through docs/evidence_documents/group_11.json. The hint drops "Choose the most
   complete report on file", which the checklist replaces, and keeps the hormone sentence. No
   laboratory screen: the evidence gives cortisol, androgens, adrenocorticotropic hormone and the
   aldosterone-to-renin ratio no coding role (lab_tests), and contract §4.2 builds lab screens only
   for tests with a diagnostic role. No marker tier: Visser Table 4 has no adrenal cortical row
   (contract §0.5), and D16 keeps 8158/3 off the adrenal screens.
2. ac_clinical, ac_imaging, ac_imaging_cytology: the common screens (evidence_gate), which refer
   the case to Group XII with refer_code 8000 at basis 1 or 2, as the evidence does (ICCC-2017
   range 143 holds 8000-8005 at C74 in XIIb). The escapes "An imaging report is on file after all"
   and "A histology report is on file" are dropped: the checklist decides the tier from the
   reports ticked (group11_common, departures from Group 10). The evidence's single
   ac_imaging_cytology splits into ad_imaging_cytology and ad_clinical_cytology, one per evidence
   context (contract §4.2).
3. The gate hint and the two imaging screens' hints add a sentence that sends a neuroblastoma or
   phaeochromocytoma diagnosed without tissue to Group IV. The evidence's conflicts (Group 4,
   8000) and data gap 5 ask for an option that refers such a case to Group IV before the 8000
   referral. g4_sympathoadrenal does hold that route (sa_imaging_gate, sa_imaging_neuroblastoma,
   sa_imaging_pheo), but validator rule 2 and the walk admit no tissue-free referral other than
   Group XII with 8000 or 8001, so the route is a hint here, not an option (request in the return).
4. ac_cytology: "Adrenal cortical carcinoma" goes to ad_site_cytology, which records 8370/3 at
   basis 5 and the site C74.0 (D9). "Cytology names a carcinoma without naming its type" (8010/3,
   basis 5) is added (D8: a carcinoma is an entity; the thyroid screen has the same line). "No
   malignant cells, an adrenal cortical neoplasm not called malignant, or not diagnostic" is the
   common pair of non-diagnostic routes, with "an adrenal cortical neoplasm the report does not
   call malignant" written into both labels. Malignant cells with no type name refer to Group XII
   with 8001 (common).
5. ac_histology: node type morphology_only becomes histology_subclassification (contract §4.2).
   Every 8370/3 option and answer goes to ad_site, a site_resolution node that captures C74.0
   (D9): ICD-O-3.2 prints C74.0 beside the 8370 terms (Rule H), so a case entered at C74.9 or
   C74.1 is recorded at C74.0. The evidence put "the same code applies when the report places the
   tumour in the periadrenal or suprarenal region" in the option's reason; ad_site asks it.
6. ac_histology: the exclusions move to ad_not_malignant (contract §4.2), as on the thyroid
   tree. The single adenoma line becomes one exclusion per ICD-O-3.2 code, 8370/0 and 8371/0 to
   8375/0: excl() names the Preferred term at its own (code, behaviour), and a compact cell
   adenoma coded as Adrenal cortical adenoma, NOS (8370/0) would name the wrong code (standing
   rule 8; currency check §5, "exclusions where the clerk meets them").
7. Adrenal cortical neoplasm of uncertain malignant potential: the evidence excluded it as
   8370/1. ICD-O-3.2 prints no 8370/1 (D4), so it is a not-registrable line naming no code, on
   ad_not_malignant and ad_behaviour (D6; registrar review A7, question 2).
8. ac_ihc_carcinoma and ac_ihc_malignant become choice nodes (ad_sf1_carcinoma,
   ad_sf1_malignant), as nut_nodes() builds the NUT panel. An ihc_checklist fallback records a
   code, and ac_ihc_malignant's fallback refers to Group XII with 8000 (D7), which no fallback can
   do; and an ihc_checklist rule is a terminal, so its SF1-positive 8370/3 could not pass through
   ad_site (D9). The rules, the fallbacks and the hint are the evidence's. 8370/3 therefore
   requires no immunohistochemistry: most adrenal cortical carcinomas are named on the histology
   report alone.
9. Trailing options (tail_options): melanoma (D13; the adrenal gland is none of skin, eye or
   central nervous system, so the hop enters me_mucosa), the picker (D2), the exclusion screen,
   the deposit question (D10), and the referrals lymphoma (II), leukaemia (I, C42.1), sarcoma
   (IX), germ cell (X) and another named tumour (XII). The evidence's lymphoma, sarcoma and
   teratoma referrals are those lines, the sarcoma reason keeps the evidence's sentence on
   sarcomatoid adrenal cortical carcinoma, and the leukaemia referral is added (common). The
   deposit option keeps the evidence's label and aid (direct spread from the kidney or liver);
   ad_deposit's kidney and liver primaries are Groups VI and VII with recapture_site. The common
   "Malignant tumour, type not determined by the report" line is removed: the evidence's
   "Malignant tumour or malignant neoplasm of the adrenal gland, type not stated" asks SF1 first
   and refers to Group XII with 8000 when SF1 does not show cortical origin, so two lines would
   offer the same report two outcomes.
10. The adrenal medulla referral (Group IV) sits after the cortical options and before the
   trailing options, in the evidence's order: neuroblastoma is the commonest solid tumour of
   childhood (Pfister p. 10) and the commonest adrenal tumour this screen meets.
11. ad_picker: D2 replaces the evidence's "There is no long-tail picker". It offers the codes
   ICCC-2017 places in Group XI at C74.0, C74.1 and C74.9 alike: the XIb thyroid codes of range
   121, which ICCC-2017 holds at every site. 8158/3 is valid at C74.0 only (range 118) and is not
   offered (D16, picker coding_note); 8370/3 and 8010/3 are held as options.
12. Not built from the evidence: 8158/3 ACTH-producing tumor (D16; registrar question 1),
   8370/1 (D4), 8290/3 Oxyphilic adenocarcinoma and 8033/3 Pseudosarcomatous carcinoma for the
   oncocytic and sarcomatoid types (Rule K takes 8370/3; evidence code currency).

Registrar questions the evidence raised (XIa_adrenal_cortex.md, questions 1-6) stay open; the
defaults above apply until they are answered (docs/group_11_registrar_review.md A2 Q3, A7 Q2,
A20 Q1, B Q4, C1 Q6, C5 Q5).
"""
from __future__ import annotations

from group11_common import (aid, code, cyto_carcinoma_nos, deposit_node, evidence_gate, excl, go,
                            make_tree, named, node, nonrep, not_malignant_node, rec, refer,
                            refer_germ_cell, refer_leukaemia, refer_lymphoma, refer_other_named,
                            refer_unspecified, tail_options)

TREE_ID = "g11_adrenal"
P = "ad_"
WHERE = "the adrenal gland"
EVIDENCE = "XIa_adrenal_cortex"
CORTEX = "C74.0"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Mete p. 21 "Wieneke criteria for pediatric adrenal cortical neoplasms"; Mete p. 21
# "Malignant/poor outcome: score".
AID_ACC = ("A report on a child often gives a Wieneke score out of 9; a score of 4 or more is the "
           "malignant category.")
# Pfister p. 14 "Adrenocortical tumors"; Mete p. 1 "Pediatric adrenal cortical neoplasms are
# assessed using the Wieneke system."
AID_TUMOUR = ("Reports on a child often call benign and malignant tumours alike an adrenocortical "
              "tumour and state the behaviour separately, often as a Wieneke score.")
# Mete p. 21 "Benign behavior: score".
AID_ADENOMA = "A report on a child may give this as a Wieneke score of 2 or less."
# Mete p. 21 "Uncertain malignant potential: score 3".
AID_UMP = "A report on a child may give this as a Wieneke score of 3."
# Mete p. 14 "labelled as an adrenal paraganglioma (pheochromocytoma) based on".
AID_MEDULLA = "Phaeochromocytoma is also reported as pheochromocytoma or adrenal paraganglioma."
# ICCR p. 5 "etc, which may metastasize to the adrenal glands, should be included."; Mete p. 5
# "(e.g., renal cell carcinoma and hepatocellular carcinoma)".
AID_DEPOSIT = ("The report may name the primary tumour, for example a melanoma, a lung carcinoma, "
               "or a kidney tumour.")

# ------------------------------------------------------------------------------------------
# Shared clerk-facing sentences
# ------------------------------------------------------------------------------------------
# icdo32.sqlite 8370/3: Preferred Adrenal cortical carcinoma; Synonyms Adrenal cortical
# adenocarcinoma, Adrenal cortical tumor, malignant.
SYNONYMS = ("ICD-O-3.2 gives Adrenal cortical adenocarcinoma and Adrenal cortical tumor, malignant "
            "as synonyms of this code.")
# Rules p. 2 (printed p. 15), Rule H "in the diagnosis, use the suggested code."; evidence
# rules_a_to_k H: "ICD-O-3.2 prints (C74.0) beside every 8370 term."
SITE_H = ("The site is recorded as the adrenal cortex (C74.0), the site ICD-O-3.2 prints beside "
          "adrenal cortical carcinoma (WHO coding Rule H). A case entered at the adrenal gland, "
          "NOS (C74.9) or the adrenal medulla (C74.1) is recorded at C74.0.")
# Rules p. 1 (printed p. 14), Rule B "unless the type of tumor indicates"; Rules p. 4 "periadrenal
# tissue", "number C48.0 which is"; evidence rules_a_to_k A and B.
SITE_B = ("The site is recorded as the adrenal cortex (C74.0): the tumour type shows the tissue it "
          "arose in, so the tissue around the gland is not recorded as the site (WHO coding Rules "
          "B and H).")
# ICCR p. 4 "tumours of the adrenal medulla (e.g., paraganglioma) are dealt with in a separate
# dataset."; Pfister p. 14 "Tumors of the adrenal medulla and extra-adrenal paraganglia".
MEDULLA_REASON = ("Tumours of the adrenal medulla, phaeochromocytoma, paraganglioma, neuroblastoma "
                  "and ganglioneuroblastoma among them, belong to ICCC-3 Group IV (neuroblastoma "
                  "and other peripheral nervous cell tumours). Code the case from the Group IV "
                  "tree.")
MEDULLA_NOTE = ("Evidence entities 8700, 8680, 9500, 9490 (ICCC-2017 IVa and IVb at every site); "
                "conflicts, Group 4. The case keeps its site; Group IV's tree resolves it.")
# Evidence conflicts (Group 4, 8000) and data gap 5; g4_sympathoadrenal sa_imaging_gate.
GROUP_IV_NO_TISSUE = ("A neuroblastoma or phaeochromocytoma diagnosed from imaging and biochemical "
                      "results is coded from the Group IV tree, which has its own route for it: "
                      "go back and choose Group IV (neuroblastoma and other peripheral nervous "
                      "cell tumours).")
# Evidence tissue_free row 3; lab_tests (no coding role); contract §0.5 (no adrenal cortical row
# in Visser Table 4).
HORMONES = ("Hormone results (cortisol, androgens, aldosterone, adrenocorticotropic hormone) do "
            "not change the code and register no code without tissue.")
# Mete p. 23 "to be the most reliable and specific biomarker of adrenal"; Mete p. 23
# "alpha-inhibin cannot be used in the distinction of an adrenal"; Mete p. 14 "inhibin expression
# are not reliable biomarkers in the distinction of"; ICCR p. 17 "SF-1 when available, or
# alpha-inhibin, Melan-A, calretinin, and synaptophysin when SF-1 is not available".
SF1_HINT = ("SF1 is the marker that shows adrenal cortical origin. "
            "Synaptophysin and alpha-inhibin also stain phaeochromocytoma, and Melan-A and "
            "calretinin are not specific.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence ac_evidence, ac_clinical, ac_imaging, ac_cytology,
# ac_imaging_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this adrenal tumour?",
        # Evidence ac_evidence hint (hormones), departure 1; the Group IV sentence, departure 3.
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. %s %s"
              % (HORMONES, GROUP_IV_NO_TISSUE)),
        # Evidence ac_evidence option 4.
        tier_labels={
            "histology": "A histology report from a biopsy or resection, with or without "
                         "immunohistochemistry",
        },
        cytology=[
            # ICCR p. 7 "8370/3"; data gap 2: the cytology option rests on the cytopathologist's
            # stated diagnosis. D9: the site step records C74.0.
            go("Adrenal cortical carcinoma (adrenocortical carcinoma)", n("site_cytology"),
               note="Evidence ac_cytology option 1; D8, D9."),
            # Pfister p. 14 "Tumors of the adrenal medulla and extra-adrenal paraganglia".
            refer("Neuroblastoma, phaeochromocytoma or another tumour of the adrenal medulla", 4,
                  MEDULLA_REASON, note="Evidence ac_cytology option 2. " + MEDULLA_NOTE),
            cyto_carcinoma_nos(note="D8 (departure 4): a carcinoma is an entity, 8010/3 at basis "
                                    "5; D11 gives it XIf10 at C74 (registrar question 5)."),
        ],
        note="Evidence ac_evidence (departure 1).")
    for nd in nodes:
        if nd["node_id"] in (n("imaging"), n("imaging_cytology")):
            # Departure 3.
            nd["hint"] = "%s %s" % (nd["hint"], GROUP_IV_NO_TISSUE)
        if nd["node_id"] == n("cytology"):
            # Departure 4: evidence ac_cytology option 4, "No malignant cells, an adrenal
            # cortical neoplasm not called malignant, or not diagnostic".
            for o in nd["options"]:
                if o["label"].startswith("No malignant cells, scant material"):
                    o["label"] = o["label"].replace(
                        "No malignant cells, scant material",
                        "No malignant cells, an adrenal cortical neoplasm the report does not "
                        "call malignant, scant material", 1)
    return nodes


# ------------------------------------------------------------------------------------------
# The site step (D9): every 8370/3 is recorded at the adrenal cortex, C74.0
# ------------------------------------------------------------------------------------------
SITE_QUESTION = "Where does the report place the adrenal cortical carcinoma?"
# ICCR p. 8 "whether adjacent structures and organs (e.g., kidney, liver, and pancreas) are
# directly involved"; evidence conflicts, Groups 6 and 7.
SITE_HINT = ("Both answers record the adrenal cortex (C74.0), whichever part of the adrenal gland "
             "the case was entered at: ICD-O-3.2 prints C74.0 beside adrenal cortical carcinoma "
             "(WHO coding Rule H). An adrenal cortical carcinoma that has grown into the kidney, "
             "liver or another organ is still recorded at C74.0.")
SITE_NOTE = ("D9, the Group III pf_subsite pattern: the node captures topography. Evidence "
             "rules_a_to_k A, B and H; registrar review C1 (question 6). Both options record the "
             "same code and site; the labels follow the report's wording, and the reasons give "
             "the rule.")
LABEL_GLAND = "In the adrenal gland, or in its cortex"
LABEL_AROUND = ("Around the adrenal gland: the periadrenal or suprarenal tissue, or the "
                "retroperitoneum beside it")


def site():
    """ad_site: the histology 8370/3, basis 7 (ICCR p. 7 image "Adrenal cortical carcinoma
    8370/3")."""
    return node(
        n("site"), "site_resolution", 5, "Site", SITE_QUESTION, SITE_HINT,
        [
            # Rules p. 2 (printed p. 15), Rule H; ICCR p. 7 "8370/3".
            code(LABEL_GLAND, "8370", "3", 7,
                 "%s %s %s" % (rec("8370"), SYNONYMS, SITE_H),
                 captures={"topography": CORTEX},
                 note="Evidence rules_a_to_k H; ac_histology option 1 reason."),
            # Rules p. 1 (printed p. 14), Rule B "unless the type of tumor indicates"; evidence
            # ac_histology option 1 reason "The same code applies when the report places the
            # tumour in the periadrenal or suprarenal region."
            code(LABEL_AROUND, "8370", "3", 7,
                 "%s %s %s" % (rec("8370"), SYNONYMS, SITE_B),
                 captures={"topography": CORTEX},
                 note="Evidence rules_a_to_k A and B; ac_histology option 1 reason."),
        ],
        ["topography"], SITE_NOTE)


def site_cytology():
    """ad_site_cytology: the cytology 8370/3, basis 5 (evidence ac_cytology option 1)."""
    cyto_reason = ("Cytology does not give the full histological type; a histology report "
                   "confirms it.")
    caps = {"topography": CORTEX, "workup_status": "incomplete",
            "basis_evidence_tier": "cytology_named"}
    return node(
        n("site_cytology"), "site_resolution", 3, "Site", SITE_QUESTION, SITE_HINT,
        [
            code(LABEL_GLAND, "8370", "3", 5,
                 "%s %s %s %s" % (rec("8370", "3", 5), cyto_reason, SYNONYMS, SITE_H),
                 captures=caps,
                 note="D8, D9. Evidence ac_cytology option 1; data gap 2 (no source discusses "
                      "cytology of adrenal cortical tumours)."),
            code(LABEL_AROUND, "8370", "3", 5,
                 "%s %s %s %s" % (rec("8370", "3", 5), cyto_reason, SYNONYMS, SITE_B),
                 captures=caps,
                 note="D8, D9. Evidence ac_cytology option 1; rules_a_to_k A and B."),
        ],
        ["topography", "workup_status", "basis_evidence_tier"], SITE_NOTE)


# ------------------------------------------------------------------------------------------
# Histology (evidence ac_histology)
# ------------------------------------------------------------------------------------------
def histology():
    head = [
        # ICCR p. 7 "8370/3" and image "Adrenal cortical carcinoma 8370/3"; Mete p. 1 "are
        # subtyped based on their morphological features to include conventional, oncocytic,
        # myxoid, and sarcomatoid subtypes."; Pfister p. 14 "Adrenocortical tumors"; Mete p. 20
        # "Pediatric ACCs are uncommon adrenal cortical neoplasms,". D1: paediatric.
        aid(go("Adrenal cortical carcinoma (adrenocortical carcinoma, carcinoma of the adrenal "
               "cortex), of any type: conventional, oncocytic, myxoid or sarcomatoid", n("site"),
               note="D1, D9 (departure 5). Rule J: the word-root orders are one term."),
            AID_ACC),
        # Pfister p. 14 "Adrenocortical tumors"; Mete p. 1 "Pediatric adrenal cortical neoplasms
        # are assessed using the Wieneke system."
        aid(go("Adrenocortical tumour or adrenal cortical neoplasm, without the word carcinoma or "
               "adenoma", n("wieneke"), note="D1 exception: the code depends on the behaviour "
                                               "the report states (Rule F)."),
            AID_TUMOUR),
        # Mete p. 23 "to be the most reliable and specific biomarker of adrenal".
        go("Carcinoma of the adrenal gland; the report does not say it began in the adrenal "
           "cortex", n("sf1_carcinoma"), note="Evidence ac_histology; departure 8."),
        # Mete p. 23 "to be the most reliable and specific biomarker of adrenal". Replaces the
        # common "Malignant tumour, type not determined by the report" (departure 9).
        go("Malignant tumour or malignant neoplasm of the adrenal gland, type not stated",
           n("sf1_malignant"), note="Evidence ac_histology; departures 8 and 9."),
        # Pfister p. 14 "Tumors of the adrenal medulla and extra-adrenal paraganglia", p. 14
        # "Pheochromocytoma"; ICCR p. 4 "Neuroblastoma and ganglioneuroblastomas are not covered
        # in the dataset." Departure 10.
        aid(refer("Phaeochromocytoma, paraganglioma, neuroblastoma, ganglioneuroblastoma, or "
                  "another tumour of the adrenal medulla", 4, MEDULLA_REASON,
                  note="Evidence ac_histology. " + MEDULLA_NOTE),
            AID_MEDULLA),
    ]
    # ICCR p. 4 "Core needle biopsies, benign adrenal cortical lesions and tumours, as well as
    # sarcoma, lymphoma and"; Mete p. 18 "Sarcomatoid ACCs that are unassociated with".
    sarcoma = refer("A sarcoma of the adrenal gland", 9,
                    "A soft tissue sarcoma of the adrenal gland belongs to ICCC-3 Group IX. A "
                    "sarcomatoid adrenal cortical carcinoma is not a sarcoma: it is the first "
                    "option of this screen. Code the case from the Group IX (soft tissue "
                    "sarcomas) tree.",
                    note="Evidence ac_histology; ICCC-2017 places 8800-8805 at C74 in IXe.")
    tail = tail_options(
        P, "mucosa", where=WHERE,
        not_malignant_label="A tumour the report calls benign or of uncertain malignant "
                            "potential (an adrenal cortical adenoma or a myelolipoma, for "
                            "example), or a cyst, hyperplasia or nodular disease",
        referrals=[
            # Rules p. 2 (printed p. 15) "extranodal lymphomas to the site of origin,".
            refer_lymphoma(WHERE),
            refer_leukaemia(WHERE),
            sarcoma,
            # Mete p. 6 "cinoma, mature teratomas, ectopic thyroid nodules, and even";
            # ICCC-2017 places 9080-9084 at C74 (range 739-750) in Xb2.
            refer_germ_cell(WHERE),
            refer_other_named(),
        ])
    kept = []
    for o in tail:
        if o.get("refer_group") == 12 and o.get("refer_code") == "8000":
            continue                                            # departure 9
        if o.get("next_node") == n("deposit"):
            # ICCR p. 5 "etc, which may metastasize to the adrenal glands, should be included.";
            # Mete p. 5 "(e.g., renal cell carcinoma and hepatocellular carcinoma)".
            o["label"] = ("A deposit (metastasis) of a tumour that began elsewhere, or a kidney "
                          "or liver tumour growing into the adrenal gland")
            aid(o, AID_DEPOSIT)
        kept.append(o)
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence ac_histology hint; Rule K row (functioning tumour); Rule G row (grade).
        "Use the report's final diagnosis. The oncocytic, myxoid and sarcomatoid types of adrenal "
        "cortical carcinoma take the same code as the conventional type, and so does a "
        "functioning (hormone-producing) adrenal cortical carcinoma. Low grade or high grade "
        "does not change the code.",
        head + kept, [],
        "Evidence ac_histology (departures 5 to 10). D1: adrenal cortical carcinoma and the "
        "adrenocortical tumour are paediatric (Pfister 2022 Table 3, p. 14; Mete 2022, p. 20). "
        "D16: 8158/3 is offered nowhere; Rule K gives a functioning adrenal cortical carcinoma "
        "8370/3 (Rules p. 11, 'coders should use the numerically higher code').")


# ------------------------------------------------------------------------------------------
# The Wieneke score (registrar, 8 October 2026, review A2, E6)
# ------------------------------------------------------------------------------------------
# Jay: "In the tree, lets ask if Weineke score is mentioned in the file? If it is, then list the
# score." Mete 2022, PDF p. 21, Table 6, "Wieneke criteria for pediatric adrenal cortical
# neoplasms": nine parameters, one point each; "Malignant/poor outcome: score >= 4", "Uncertain
# malignant potential: score 3", "Benign behavior: score <= 2". Mete p. 21: the Weiss criteria
# lead "to over-diagnosis of tumors with benign clinical behavior as ACC in children".
WIENEKE_SOURCE = ("Registrar, 8 October 2026 (review A2, E6). Mete 2022, PDF p. 21, Table 6 "
                  "(Wieneke criteria). ")
# Mete p. 21 "Uncertain malignant potential: score 3"; ICCR p. 2 "This is not considered a
# distinct entity under the WHO Classification."
UMP_REASON = ("ICD-O-3.2 prints no code for an adrenal cortical neoplasm of uncertain malignant "
              "potential, and the WHO classification does not treat it as a distinct entity. It "
              "is not a malignant tumour, so no Group XI code is recorded. This line awaits the "
              "registrar's decision.")


def wieneke():
    return node(
        n("wieneke"), "histology_subclassification", 4, "Wieneke score",
        "The report calls the tumour an adrenocortical tumour or adrenal cortical neoplasm. Does "
        "the file give a Wieneke score?",
        "The Wieneke score is the scoring system for adrenal cortical tumours in children. It "
        "counts nine findings, one point each, and is given out of 9. A Weiss score is a "
        "different system, used for adults: answer No for it. When the report states a "
        "behaviour (benign, malignant or uncertain malignant potential) that differs from its "
        "score, answer No and choose the stated behaviour.",
        [
            go("Yes, the file gives a Wieneke score", n("wieneke_score"), note=WIENEKE_SOURCE),
            go("No", n("behaviour"),
               note="The report's stated behaviour decides (Rule F; evidence ac_behaviour)."),
        ], [],
        WIENEKE_SOURCE + "A stated behaviour that differs from the score is coded as stated "
                         "(WHO coding Rule F).")


def wieneke_score():
    opts = []
    for score in range(10):
        label = "Wieneke score %d out of 9" % score
        if score <= 2:
            opts.append(excl(label, "8370", "0",
                             what="an adrenal cortical tumour with a Wieneke score of 2 or less "
                                  "(benign behaviour)",
                             extra="ICD-O-3.2 gives Adrenal cortical tumor, benign as a synonym "
                                   "of this code.",
                             note=WIENEKE_SOURCE + "'Benign behavior: score <= 2'."))
        elif score == 3:
            opts.append(nonrep(label, UMP_REASON,
                               note=WIENEKE_SOURCE + "'Uncertain malignant potential: score 3'; "
                                    "D4, D6; registrar review A7."))
        else:
            opts.append(go(label, n("site"),
                           note=WIENEKE_SOURCE + "'Malignant/poor outcome: score >= 4'; 8370/3 "
                                "at basis 7 on ad_site."))
    return node(
        n("wieneke_score"), "histology_subclassification", 5, "Wieneke score",
        "What Wieneke score does the file give?",
        "A score of 4 or more is malignant, 3 is of uncertain malignant potential, and 2 or less "
        "is benign.",
        opts, [],
        WIENEKE_SOURCE + "Scores 0 to 2: 8370/0 exclusion. Score 3: not registrable (review A7). "
                         "Scores 4 to 9: 8370/3 at C74.0.")


def behaviour():
    return node(
        n("behaviour"), "histology_subclassification", 5, "Behaviour",
        "The report calls the tumour an adrenocortical tumour or adrenal cortical neoplasm. What "
        "does it say about its behaviour?",
        # Evidence ac_behaviour hint; Mete p. 21 Table 6; ICCR p. 16.
        "Use the diagnosis line, a comment or an addendum. With no behaviour stated, ICD-O-3.2 "
        "codes an adrenal cortical tumour as benign.",
        [
            # Mete p. 21 "Wieneke criteria for pediatric adrenal cortical neoplasms",
            # "Malignant/poor outcome: score", "those described by Wieneke et al. in 2003".
            go("Malignant", n("site"),
               note="Evidence ac_behaviour option 1 (8370/3, basis 7); D9. The Wieneke score is "
                    "asked first, on ad_wieneke (registrar, 8 October 2026, review A2, E6)."),
            # Mete p. 21 "Uncertain malignant potential: score 3"; ICCR p. 2 "This is not
            # considered a distinct entity under the WHO Classification."
            nonrep("Uncertain malignant potential", UMP_REASON,
                   note="D4, D6 (departure 7); registrar review A7, question 2. Evidence "
                        "ac_behaviour option 2 named 8370/1, which ICD-O-3.2 does not print."),
            # Mete p. 21 "Benign behavior: score".
            excl("Benign", "8370", "0",
                 what="a benign adrenal cortical tumour",
                 extra="ICD-O-3.2 gives Adrenal cortical tumor, benign as a synonym of this code.",
                 note="Evidence ac_behaviour option 3."),
            # Rules p. 2 "the appropriate 5th digit behavior code even if"; icdo32.sqlite 8370/0
            # Synonym Adrenal cortical tumor, NOS.
            excl("The report states no behaviour", "8370", "0",
                 what="an adrenal cortical tumour with no behaviour stated",
                 extra="ICD-O-3.2 gives Adrenal cortical tumor, NOS as a synonym of this code.",
                 decision=True,
                 note="Evidence ac_behaviour option 4; registrar question 4 (review B)."),
        ], [],
        "Evidence ac_behaviour, kept (registrar's task: the report's stated category decides, "
        "Rule F). Mete 2022, p. 21, Table 6; ICCR, p. 16.")


def sf1_carcinoma():
    return node(
        n("sf1_carcinoma"), "histology_subclassification", 4, "SF1 immunostain",
        "The histology report calls the tumour a carcinoma of the adrenal gland. What does the "
        "immunohistochemistry report say about SF1 (steroidogenic factor 1)?",
        SF1_HINT,
        [
            # Mete p. 23 "to be the most reliable and specific biomarker of adrenal"; Mete p. 1
            # "the most reliable biomarker in the confirmation of adrenal cortical origin"; Mete
            # p. 14 "(C) and is positive for SF1 (D). These findings confirm the adrenal".
            go("SF1 positive", n("site"),
               note="Evidence ihc_rules, panel ac_ihc_carcinoma, rule 1 (8370/3); D9."),
            # Mete p. 23 "alpha-inhibin cannot be used in the distinction of an adrenal"; Mete
            # p. 14 "inhibin expression are not reliable biomarkers in the distinction of"; ICCR
            # p. 17 "SF-1 when available, or alpha-inhibin, Melan-A, calretinin, and
            # synaptophysin when SF-1 is not available".
            named("SF1 negative, not done, or not reported", "8010",
                  "The reports do not show where the carcinoma began.",
                  upgrade="An SF1 immunostain the report calls positive shows adrenal cortical "
                          "origin and gives Adrenal cortical carcinoma (8370/3).",
                  note="Evidence ihc_rules, panel ac_ihc_carcinoma, fallback. D11: no ICCC-2017 "
                       "range holds 8010 at C74; the entry's default subgroup, XIf10 (registrar "
                       "question 5, review C5)."),
        ], [],
        "Evidence ac_ihc_carcinoma, built as a choice (departure 8).")


def sf1_malignant():
    return node(
        n("sf1_malignant"), "histology_subclassification", 4, "SF1 immunostain",
        "The histology report calls the tumour malignant without naming its type. What does the "
        "immunohistochemistry report say about SF1 (steroidogenic factor 1)?",
        SF1_HINT,
        [
            # Mete p. 23, p. 1, p. 14 (as on ad_sf1_carcinoma).
            go("SF1 positive", n("site"),
               note="Evidence ihc_rules, panel ac_ihc_malignant, rule 1 (8370/3); D9. ICD-O-3.2 "
                    "gives Adrenal cortical tumor, malignant as a synonym of 8370/3."),
            # Mete p. 23 "alpha-inhibin cannot be used in the distinction of an adrenal".
            refer_unspecified("SF1 negative, not done, or not reported", "8000", 7,
                              "The reports establish a malignant tumour of the adrenal gland "
                              "without determining its type or showing where it began.",
                              where=WHERE,
                              note="Evidence ihc_rules, panel ac_ihc_malignant, fallback (8000/3 "
                                   "to Group XII); D7. ICCC-2017 range 143 holds 8000 at C74 in "
                                   "XIIb."),
        ], [],
        "Evidence ac_ihc_malignant, built as a choice (departure 8).")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # Mete p. 21 "Benign behavior: score", "10% associated with benign disease and a
            # labeling index of"; Mete p. 19 "Oncocytic adrenal cortical adenoma: absence of major
            # and minor"; Rules p. 11 "coders should use the numerically higher code".
            aid(excl("Adrenal cortical adenoma with no type named, or an oncocytic adrenal "
                     "cortical adenoma", "8370", "0", what="an adrenal cortical adenoma",
                     extra="An oncocytic adrenal cortical adenoma takes this code, not Oxyphilic "
                           "adenoma (8290/0) (WHO coding Rule K).",
                     note="Evidence entities 8370/0 (adenoma; oncocytic adenoma); departure 6."),
                AID_ADENOMA),
            # Evidence entity 8371/0; currency check §5.
            excl("Adrenal cortical adenoma, compact cell", "8371", "0",
                 what="a compact cell adrenal cortical adenoma",
                 note="Evidence entity 8371/0; departure 6."),
            # Mete p. 15 "of pigmented “black” adrenal cortical adenomas can show".
            excl("Adrenal cortical adenoma, pigmented, or black adenoma", "8372", "0",
                 what="a pigmented adrenal cortical adenoma",
                 extra="ICD-O-3.2 gives Black adenoma and Pigmented adenoma as synonyms of this "
                       "code.",
                 note="Evidence entity 8372/0; departure 6."),
            # Evidence entity 8373/0; currency check §5.
            excl("Adrenal cortical adenoma, clear cell", "8373", "0",
                 what="a clear cell adrenal cortical adenoma",
                 note="Evidence entity 8373/0; departure 6."),
            # Evidence entity 8374/0; currency check §5.
            excl("Adrenal cortical adenoma, glomerulosa cell", "8374", "0",
                 what="a glomerulosa cell adrenal cortical adenoma",
                 note="Evidence entity 8374/0; departure 6."),
            # Evidence entity 8375/0; currency check §5.
            excl("Adrenal cortical adenoma, mixed cell", "8375", "0",
                 what="a mixed cell adrenal cortical adenoma",
                 note="Evidence entity 8375/0; departure 6."),
            # ICCR p. 2 "Adrenal cortical neoplasm of uncertain malignant potential", "This is
            # not considered a distinct entity under the WHO Classification."; ICCR p. 7 "can be
            # diagnosed as adrenal cortical neoplasm of uncertain malignant"; Mete p. 19
            # "Oncocytic adrenal cortical neoplasm of uncertain malignant".
            aid(nonrep("Adrenal cortical neoplasm of uncertain malignant potential, including "
                       "the oncocytic type",
                       "ICD-O-3.2 prints no code for an adrenal cortical neoplasm of uncertain "
                       "malignant potential, and the WHO classification does not treat it as a "
                       "distinct entity. It is not a malignant tumour, so no Group XI code is "
                       "recorded. This line awaits the registrar's decision.",
                       note="D4, D6 (departure 7); registrar review A7, question 2."),
                AID_UMP),
            # Mete p. 2 "In addition to adrenal myelolipoma, the new classification of".
            excl("Myelolipoma", "8870", "0", what="a myelolipoma",
                 note="Evidence entity 8870/0. ICCC-2017 places 8870 in IXd4 at behaviour 3, a "
                      "pair ICD-O-3.2 does not print."),
            # Mete p. 6 "grossly cystic adrenal glands are adrenal cortical neoplasms"; Mete p. 2
            # "Adrenal cysts".
            nonrep("A cyst or pseudocyst, haemorrhage, hyperplasia or nodular disease, with no "
                   "tumour", "Not registrable. The report describes no tumour.",
                   note="Evidence ac_histology."),
        ],
        where=WHERE,
        note="The exclusions and the not-registrable lines of evidence ac_histology "
             "(departures 6 and 7).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [site_cytology(), histology(), wieneke(), wieneke_score(), behaviour(),
                      sf1_carcinoma(),
                      sf1_malignant(), site(), not_malignant(), deposit_node(P, where=WHERE)]
    return make_tree(
        TREE_ID, nodes,
        subtype_screens=(n("site"), n("site_cytology"), n("sf1_carcinoma")),
        # Standing rule 3 (D11): no ICCC-2017 range holds 8010 at C74.0, C74.1 or C74.9, and the
        # evidence names it (code currency 8010; registrar question 5).
        d11=("8010",))


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8370/3": ("D1, D8, D9", EVIDENCE,
               "Adrenal cortical carcinoma of any type, conventional, oncocytic, myxoid or "
               "sarcomatoid (ICCR Table 1; Mete 2022, p. 1; Pfister 2022 Table 3), recorded at "
               "C74.0 by the adrenal tree's site step (Rule H), at basis 7 from the histology "
               "screen, from an adrenocortical tumour the report calls malignant or scores 4 or "
               "more on the Wieneke system (registrar, 8 October 2026, review A2, E6), and from a carcinoma or "
               "malignant tumour of the adrenal gland with SF1 positive; at basis 5 when cytology "
               "names it. Rule K takes 8370/3 over 8290, 8033 and 8158 for the oncocytic, "
               "sarcomatoid and functioning tumours."),
    "8010/3": ("D8, D11", EVIDENCE,
               "Carcinoma of the adrenal gland whose cortical origin the reports do not show "
               "(SF1 negative, not done or not reported), at basis 7, and a carcinoma that "
               "cytology names without its type, at basis 5. No ICCC-2017 range holds 8010 at "
               "C74; standing rule 3 keeps it in Group XI with the default subgroup XIf10 "
               "(registrar question 5)."),
}
