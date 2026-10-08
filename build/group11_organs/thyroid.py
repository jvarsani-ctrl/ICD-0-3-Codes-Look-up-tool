"""g11_thyroid (prefix th_): thyroid carcinomas at C73.9, ICCC-3 subgroup XIb.

The worked exemplar for every Group XI tree module. It is built from
docs/group_11_evidence/XIb_thyroid.json (the evidence agent's nodes th_evidence, th_lab,
th_cytology, th_histology, th_ptc_subtype, th_ftc_invasion, th_dhgtc, th_ihc, th_picker) with the
builders in build/group11_common.py. Every option's label, code, behaviour, basis, reason and
recognition aid comes from that file; the cite (file, PDF page, quotation) is the comment above
the option or the aid. File names in the comments are the evidence's own:
    ICCR      XIb-thyroid__ICCR-Thyroid-3rd.txt (ICCR Carcinoma of the Thyroid, 3rd edition,
              version 3.1, November 2025). "image" marks a quotation read from the page image
              (Table 1, PDF p. 9).
    Juhlin    XIb-thyroid__Juhlin-2022.txt (Juhlin, Mete, Baloch. Endocr Relat Cancer
              2023;30:e220293)
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser    Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
              set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    th_document_inventory  document_inventory  evidence gate (evidence th_evidence)
    th_labs_referral, th_labs_markers, th_labs_cytology, th_labs_histology  lab_results
    th_clinical, th_clinical_cytology  clinical_alias
    th_imaging, th_imaging_markers, th_imaging_cytology  morphology_only
    th_cytology            morphology_only     (evidence th_cytology)
    th_histology           histology_subclassification  (evidence th_histology)
    th_ptc_subtype         histology_subclassification  (evidence th_ptc_subtype)
    th_ftc_invasion        histology_subclassification  (evidence th_ftc_invasion)
    th_dhgtc               histology_subclassification  (evidence th_dhgtc)
    th_ihc                 ihc_checklist        (evidence th_ihc and ihc_rules)
    th_not_malignant       histology_subclassification  (the exclusions of evidence th_histology)
    th_deposit             morphology_only      (D10)
    th_picker              histology_subclassification  (D2; evidence th_picker's long tail)

Departures from the evidence nodes, and why
-------------------------------------------
1. th_evidence: the referral and imaging-only tiers recorded 8000/3 at basis 1 and 2 on the gate
   itself. D7: each routes to its own screen (th_clinical, th_imaging), which refers the case to
   Group XII with refer_code 8000, because ICCC-2017 places 8000/3 at C73.9 in XIIb (range 143).
   The evidence notes the same (conflicts, Group 12). The gate's options are the contract §4.2
   tiers, with laboratory copies (registrar, 6 October 2026); the gate becomes a document
   checklist through docs/evidence_documents/group_11.json. The hint drops "Choose the strongest
   report in the file", which the checklist replaces.
2. th_lab: a lab_results screen cannot choose a code (registrar, 6 October 2026; Group 10
   lesson). Its two options ("raised" -> 8345/3 basis 4; "within the reference range" -> 8000/3
   basis 2) move to th_imaging_markers, which reads the report's own words: 8345/3 at basis 4 when
   imaging shows the tumour, calcitonin is called raised and the file names medullary thyroid
   carcinoma (Visser Table 4 registers the marker code for the diagnosis it names, as Group 10's
   marker options require); otherwise a malignant tumour on imaging refers to Group XII with
   8000. The th_labs_* screens record the calcitonin value. The evidence gives no unit; pg/mL and
   ng/L, which are equal, are the unit list (registrar to confirm).
3. th_cytology: "Malignant, carcinoma of a type the report does not name" (8010/3, basis 5) is
   kept as "Cytology names a carcinoma without naming its type"; the common screen adds
   "Malignant cells are present, with no tumour type named", which refers to Group XII with 8001
   (D8). "Suspicious for malignancy, indeterminate, or benign" is the common non-registrable line.
   The common non-diagnostic routes are added.
4. th_histology: follicular thyroid carcinoma (to th_ftc_invasion) and high-grade differentiated
   thyroid carcinoma (to th_dhgtc) move from the evidence's picker to the histology screen. D1:
   an entity whose code needs a further answer (invasion; dominant type) is an option wherever it
   occurs, because the picker cannot ask the question.
5. th_histology: the six exclusions and the follicular nodular disease line move to
   th_not_malignant, reached by the standard option (contract §4.2). Its label names goitre so a
   clerk with a nodular disease report finds it.
6. th_histology: the trailing options are the common ones (tail_options): melanoma (D13), the
   picker, the exclusion screen, the deposit question (D10), "Malignant tumour, type not
   determined" (Group XII, 8000, D7), and the referrals lymphoma (II, keeps C73.9, Rule D),
   leukaemia (I, C42.1), sarcoma (IX), teratoma or another germ cell tumour (X) and another named
   tumour (XII). The evidence's lymphoma, sarcoma and teratoma referrals are those lines; its
   deposit referral (refer_group null with recapture) is the deposit question. NUT carcinoma has
   no option: D12 does not name the thyroid, so 8023/3 is a picker entry.
7. Melanoma (D13): the thyroid is none of skin, eye or central nervous system, so the hop enters
   me_mucosa, the melanoma tree's screen for non-cutaneous, non-ocular sites. T2c to confirm the
   screen takes a melanoma of an internal organ.
8. th_ptc_subtype, diffuse sclerosing subtype: the reason no longer prints the obsolete term
   (D3: an [obs] term stays off every screen); it says every term on 8350/3 is obsolete.
9. th_ftc_invasion: awaiting_layer1 on 8339/3 is not carried. Standing rule 16 (4 October 2026):
   the tool never tests what REDCap holds; 8339 goes on the REDCap-side list in docs/TODO.md §7.
10. th_dhgtc, "The report does not name the dominant type": the evidence left the code to the
   registrar. D4: a report naming an entity ICD-O-3.2 gives no code reaches the nearest generic
   option, 8010/3, with the registrar's decision pending.
11. th_ihc: marker names are capitalised as the screen shows them ("Calcitonin", "Beta-catenin
   (nuclear)"); the rules and fallback are the evidence's.
12. th_picker: D2 replaces the evidence's curated picker. Labels are ICD-O-3.2 Preferred terms,
   search_terms the live synonyms and related terms, and the options carry no recognition aid
   (Group 10's picker shape), so the evidence's picker aids (oncocytic, anaplastic,
   cribriform-morular, mucoepidermoid, secretory carcinoma) and labels (squamous cell carcinoma,
   thymoma and thymic carcinoma "within the thyroid") are not shown; the build report lists
   them. D2 also puts back the three codes the evidence held back (8050/3, 8510/3, 8021/3), which
   ICCC-2017 places in XIb at C73.9 (validator rule 4). The standing-rule-3 codes the evidence
   names (8502, 8580-8586) are D11 picker entries; 8580-8586 at C73.9 wait on registrar question 7.
13. Not built from the evidence: the "Differentiated high-grade thyroid carcinoma, dominant type
   not named" and thyroblastoma entities (D4), 8350/3 (D3), and Rule F stated-behaviour codes for
   the /1 tumours (D6, registrar question 9).

Registrar questions the evidence raised (XIb_thyroid.json registrar_questions 1-9) stay open; the
defaults above apply until they are answered (docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, aid, cyto, cyto_carcinoma_nos, deposit_node,
                            evidence_gate, excl, go, ihc_node, lab, make_tree, marker, named,
                            node, nonrep, not_malignant_node, refer_germ_cell, refer_leukaemia,
                            refer_lymphoma, refer_other_named, refer_sarcoma, rule, tail_options)

TREE_ID = "g11_thyroid"
P = "th_"
WHERE = "the thyroid"
EVIDENCE = "XIb_thyroid"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Pfister p. 14 "Papillary thyroid carcinoma"; Juhlin p. 5 "Classic PTC with a papillary growth
# and florid nuclear atypia".
AID_PTC = ("Reports describe papillae or follicles lined by cells with the nuclear features of "
           "papillary carcinoma.")
# ICCR p. 11 "defined by invasiveness in the absence of diagnostic nuclear features of papillary
# thyroid carcinoma" (the evidence's th_picker option).
AID_FTC = ("Reports describe a follicular tumour without papillary carcinoma nuclei that invades "
           "its capsule or vessels.")
# Juhlin p. 5 "is also noted in some PDTC cases in adolescents"; ICCR p. 9 image "Insular
# carcinoma 8337/3"; ICCR p. 12 "display a solid, trabecular, and/or insular growth pattern".
AID_PDTC = ("Reports describe solid, trabecular or insular growth without papillary carcinoma "
            "nuclei, with convoluted nuclei, 3 or more mitoses per 2 mm2, or tumour necrosis.")
# Pfister p. 14 "Medullary thyroid carcinoma"; ICCR p. 9 image "Medullary thyroid carcinoma
# 8345/3"; Juhlin p. 7 "verified by calcitonin immunohistochemistry".
AID_MTC = ("Reports describe a tumour of C cells that stains for calcitonin; the report may grade "
           "it low or high, which does not change the code.")
# Juhlin p. 5 "Classic PTC with a papillary growth and florid nuclear atypia"; ICCR p. 9 image
# "Papillary thyroid carcinoma 8260/3".
AID_CLASSIC = ("Reports describe true papillae lined by cells with the nuclear features of "
               "papillary carcinoma.")
# Juhlin p. 5 "infiltrative follicular variant PTC growing into the surrounding thyroid
# parenchyma"; ICCR p. 9 image "Infiltrative follicular variant of papillary thyroid carcinoma
# 8340/3".
AID_IFV = ("Reports describe follicles with papillary carcinoma nuclei growing into the "
           "surrounding thyroid.")
# Juhlin p. 4 "Encapsulated FVPTCs are RAS-driven lesions with a similar invasive pattern as
# FTCs"; ICCR p. 9 image "Invasive encapsulated papillary thyroid carcinoma 8343/3".
AID_IEFV = ("Reports describe an encapsulated follicular-patterned tumour with papillary carcinoma "
            "nuclei that invades its capsule or vessels.")
# ICCR p. 10 "should be termed Encapsulated non-invasive papillary carcinoma".
AID_ENCAPSULATED = ("An encapsulated tumour without invasion is called encapsulated non-invasive "
                    "papillary carcinoma when it has psammoma bodies, true papillae or BRAF "
                    "p.V600E.")
# Juhlin p. 5 "eosinophilic tumor cells with a height of at least three times the width".
AID_TALL = ("Reports describe pink cells at least three times as tall as they are wide, in a "
            "tram-track pattern.")
# Juhlin p. 5 "columnar cells with pseudostratification arranged in papillary and
# pseudoglandular formations"; ICCR p. 9 image "Columnar cell papillary thyroid carcinoma 8344/3".
AID_COLUMNAR = ("Reports describe columnar cells with stacked (pseudostratified) nuclei in "
                "papillae and gland-like spaces.")
# Juhlin p. 5 "oncocytic cells are defined as oncocytic PTC"; ICCR p. 9 image "Oncocytic papillary
# thyroid carcinoma 8342/3".
AID_ONCOCYTIC_PTC = ("Reports describe papillary carcinoma in which 75% or more of the cells are "
                     "oncocytic.")
# Juhlin p. 5 "dense fibrotic stroma with multiple psammoma bodies and associated chronic
# inflammation"; ICCR p. 2 "Diffuse sclerosing subtype".
AID_DIFFUSE_SCLEROSING = ("Reports describe tumour cells in solid nests, sometimes with squamous "
                          "metaplasia, in dense fibrous tissue with many psammoma bodies and "
                          "chronic inflammation.")
# ICCR p. 10 "papillary microcarcinoma is not a histological subtype".
AID_MICRO = ("The report uses papillary microcarcinoma for a papillary carcinoma 10 mm or "
             "smaller.")
# ICCR p. 11 "grossly apparent extensive invasion of the thyroid and/or extra-thyroid tissue";
# ICCR p. 9 image "Follicular thyroid carcinoma 8330/3".
AID_WIDELY_INVASIVE = ("Reports describe extensive invasion of the thyroid or the tissue around "
                       "it, often with loss of the capsule.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence th_evidence, th_lab, th_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this thyroid tumour?",
        # Evidence th_evidence hint. Rules B and H (Rules PDF p. 1-2, printed pp. 14-15): a
        # thyroid carcinoma in a neck lymph node or the perithyroid tissue is recorded at C73.9,
        # the site ICD-O-3.2 prints beside the thyroid codes.
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. A thyroid carcinoma reported in "
              "a neck lymph node or in the tissue around the thyroid is recorded at the thyroid "
              "(C73.9). A report that calls the tumour possible or suspected does not register "
              "it."),
        # Evidence lab_tests: serum calcitonin, the one test the part gives a diagnostic role
        # (Visser Table 4). No source on disk prints a unit; pg/mL equals ng/L.
        labs=[lab("calcitonin", "Serum calcitonin", ("pg/mL", "ng/L"))],
        marker_tests="serum calcitonin",
        markers=[
            # Evidence tissue_free row 3 and th_lab option 1. Visser 2023 Table 4, p. 06, read
            # from the page image (contract §0.5): medullary thyroid carcinoma with calcitonin.
            marker("8345", test="serum calcitonin", diagnosis="medullary thyroid carcinoma",
                   where="of the thyroid",
                   note="Visser O, et al. Front Oncol 2023;13:1250549, Table 4, p. 06 "
                        "(medullary thyroid carcinoma, calcitonin), rule 6, p. 05. Evidence "
                        "XIb_thyroid.json tissue_free row 3."),
        ],
        tier_labels={
            "imaging": "An imaging report only (ultrasound, CT, MRI or a nuclear medicine scan) "
                       "- no serum calcitonin result, no tissue",
            "cytology": "A cytology report (fine-needle aspiration) - no histology report",
            "histology": "A histology report, with or without immunohistochemistry or gene "
                         "reports",
        },
        cytology=[
            # ICCR p. 9 image "Papillary thyroid carcinoma 8260/3".
            cyto("Papillary thyroid carcinoma", "8260",
                 "ICD-O-3.2 gives Papillary carcinoma of thyroid as a related term of this code.",
                 note="Evidence th_cytology option 1."),
            # ICCR p. 9 image "Medullary thyroid carcinoma 8345/3".
            cyto("Medullary thyroid carcinoma", "8345", note="Evidence th_cytology option 2."),
            cyto_carcinoma_nos(note="Evidence th_cytology option 3 ('Malignant, carcinoma of a "
                                    "type the report does not name')."),
            # ICCR p. 11 "primarily depends on the identification of invasion of the tumour
            # capsule".
            nonrep("Follicular neoplasm, or suspicious for a follicular neoplasm",
                   "Not registrable. Cytology cannot show the capsular or vascular invasion that "
                   "defines follicular carcinoma; register the case when histology reports it.",
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "cytology_follicular_neoplasm"},
                   note="Evidence th_cytology option 4."),
        ],
        note="Evidence th_evidence and th_lab (departures 1 and 2 in the module docstring).")


# ------------------------------------------------------------------------------------------
# Histology (evidence th_histology)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # Pfister p. 14 "Papillary thyroid carcinoma"; Juhlin p. 5. D1: paediatric.
        aid(go("Papillary thyroid carcinoma, any subtype, including papillary microcarcinoma and "
               "the encapsulated follicular variant", n("ptc_subtype"), note="D1."), AID_PTC),
        # ICCR p. 11 "defined by invasiveness in the absence of diagnostic nuclear features of
        # papillary thyroid carcinoma". D1 exception: the code needs the invasion answer.
        aid(go("Follicular thyroid carcinoma", n("ftc_invasion"),
               note="D1 exception (invasion screen); moved from the evidence's picker."),
            AID_FTC),
        # Juhlin p. 5 "differentiated high-grade thyroid carcinoma". D1 exception: the code is
        # the dominant type's.
        go("High-grade differentiated thyroid carcinoma (tumour necrosis or 5 or more mitoses "
           "per 2 mm2, with a papillary, follicular or oncocytic pattern)", n("dhgtc"),
           note="D1 exception (dominant-type screen); moved from the evidence's picker."),
        # Juhlin p. 5 "is also noted in some PDTC cases in adolescents"; ICCR p. 9 image
        # "Insular carcinoma 8337/3"; ICCR p. 12.
        aid(named("Poorly differentiated thyroid carcinoma, or insular carcinoma", "8337",
                  "ICD-O-3.2 gives Insular carcinoma as a synonym of this code.",
                  note="D1: reported in adolescents (Juhlin 2022, p. 5)."), AID_PDTC),
        # Pfister p. 14 "Medullary thyroid carcinoma"; ICCR p. 9 image; Juhlin p. 7.
        aid(named("Medullary thyroid carcinoma, or C-cell carcinoma", "8345",
                  "ICD-O-3.2 gives C cell carcinoma as a synonym of this code.",
                  note="D1: Pfister 2022 Table 3, p. 344."), AID_MTC),
        # Pfister p. 14 "Spindle epithelial tumor with thymus-like elements".
        named("Spindle epithelial tumour with thymus-like elements", "8588",
              "ICD-O-3.2 gives Spindle epithelial tumor with thymus-like differentiation as a "
              "synonym of this code.", note="D1: Pfister 2022 Table 3, p. 344."),
        # Registrar, 8 October 2026 (review A6, E7): Rule F (ICD-O-3.1 printed p. 15). ICD-O-3.2
        # prints 8336 at /1 only; the name does not change with the behaviour, so 8336/3 is
        # recorded (build_database.ICDO32_MATRIX_RULE). ICCC-2017 range 121: XIb.
        named("Hyalinizing trabecular tumour that the report calls malignant", "8336",
              "The pathologist's stated behaviour is recorded (WHO coding Rule F). ICD-O-3.2 "
              "prints this tumour as behaviour 1; the report calls it malignant, so behaviour 3 "
              "is recorded with the same name.",
              note="Registrar, 8 October 2026 (review A6, E7): Rule F; matrix-rule pair."),
        go("A carcinoma whose type the report does not name, with immunohistochemistry results",
           n("ihc")),
        named("A carcinoma whose type the report does not name, with no immunohistochemistry",
              "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence th_histology; the generic option of the screen (D4's nearest "
                   "generic code)."),
    ] + tail_options(
        P, "mucosa", where=WHERE,
        not_malignant_label="A tumour the report calls benign or of uncertain malignant "
                            "potential, or a goitre or adenomatous nodule",
        referrals=[
            # Rules p. 2 (printed p. 15) "Code extranodal lymphomas to the site of origin";
            # ICCC-2017: 9680, 9699 at 739 -> IIb2.
            refer_lymphoma(WHERE),
            refer_leukaemia(WHERE),
            # ICCC-2017: 8800 at 739 -> IXe; 9120 at 739 -> IXd8.
            refer_sarcoma(WHERE, label="A sarcoma, for example angiosarcoma"),
            # ICCC-2017: 9080 at 739 -> Xb2; icdo32.sqlite 9080/1 Immature teratoma of thyroid.
            refer_germ_cell(WHERE),
            refer_other_named(),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence th_histology hint. Rules p. 2 and p. 9 (printed pp. 15, 22): Rule G.
        "Use the report's final diagnosis. When the report names a well-differentiated "
        "carcinoma with a poorly differentiated or anaplastic component, choose the "
        "higher-grade tumour (WHO coding Rule G).",
        opts, [],
        "Evidence th_histology (departures 4 to 7). D1: the paediatric entities are papillary "
        "and medullary thyroid carcinoma and the spindle epithelial tumour with thymus-like "
        "elements (Pfister 2022 Table 3, pp. 343-344) and poorly differentiated thyroid "
        "carcinoma (Juhlin 2022, p. 5); follicular and high-grade differentiated carcinoma are "
        "options because their codes need a further answer.")


def ptc_subtype():
    return node(
        n("ptc_subtype"), "histology_subclassification", 4, "Papillary carcinoma subtype",
        "Which subtype of papillary thyroid carcinoma does the report name?",
        # Evidence th_ptc_subtype hint; Rules p. 3 (printed p. 16) Rule K; p. 11 (printed p. 24)
        # Rule J.
        "A high-grade papillary carcinoma (tumour necrosis, or 5 or more mitoses per 2 mm2) is "
        "coded by its subtype. If the report names more than one subtype, or a subtype with "
        "papillary microcarcinoma, choose the one with the higher code (WHO coding Rule K): tall "
        "cell and columnar cell 8344, encapsulated 8343, oncocytic 8342, papillary "
        "microcarcinoma 8341, infiltrative follicular variant 8340, every other subtype 8260. A "
        "report that says papillary and follicular carcinoma is the infiltrative follicular "
        "variant (8340).",
        [
            # Juhlin p. 5; ICCR p. 9 image "Papillary thyroid carcinoma 8260/3".
            aid(named("Classic (usual or conventional) subtype", "8260",
                      "ICD-O-3.2 gives Papillary carcinoma of thyroid as a related term of this "
                      "code."), AID_CLASSIC),
            # Juhlin p. 5; ICCR p. 9 image "Infiltrative follicular variant of papillary thyroid
            # carcinoma 8340/3".
            aid(named("Infiltrative follicular variant, or follicular variant that is not "
                      "encapsulated", "8340"), AID_IFV),
            # Juhlin p. 4; ICCR p. 9 image "Invasive encapsulated papillary thyroid carcinoma
            # 8343/3".
            aid(named("Encapsulated follicular variant with capsular or vascular invasion "
                      "(invasive encapsulated follicular variant)", "8343"), AID_IEFV),
            # ICCR p. 10 "should be termed Encapsulated non-invasive papillary carcinoma".
            aid(named("Encapsulated subtype, including encapsulated non-invasive papillary "
                      "carcinoma", "8343"), AID_ENCAPSULATED),
            # Juhlin p. 5 "eosinophilic tumor cells with a height of at least three times the
            # width"; icdo32.sqlite 8344/3 Synonym Papillary carcinoma, tall cell.
            aid(named("Tall cell subtype", "8344",
                      "ICD-O-3.2 gives Papillary carcinoma, tall cell as a synonym of this "
                      "code."), AID_TALL),
            # Juhlin p. 5; ICCR p. 9 image "Columnar cell papillary thyroid carcinoma 8344/3".
            aid(named("Columnar cell subtype", "8344"), AID_COLUMNAR),
            # Juhlin p. 5 "oncocytic cells are defined as oncocytic PTC"; ICCR p. 9 image
            # "Oncocytic papillary thyroid carcinoma 8342/3".
            aid(named("Oncocytic subtype", "8342"), AID_ONCOCYTIC_PTC),
            # Juhlin p. 5; ICCR p. 2 "Diffuse sclerosing subtype". D3: every 8350/3 term is
            # [obs]. Registrar, 8 October 2026 (review A5, E7): "Use rule K". The one code naming
            # both terms (8350/3 "Papillary carcinoma, diffuse sclerosing") is obsolete, so Rule K
            # takes the higher of the usable codes: 8260/3.
            aid(named("Diffuse sclerosing subtype", "8260",
                      "ICD-O-3.2 has no current term for the diffuse sclerosing subtype: every "
                      "term on 8350/3 is obsolete.",
                      note="D3; registrar, 8 October 2026 (review A5, E7): Rule K."),
                AID_DIFFUSE_SCLEROSING),
            # ICCR p. 2 "Hobnail subtype", "Warthin-like subtype", "Solid subtype". Registrar
            # question 4 (Rule K would give clear cell 8310/3).
            named("Solid, hobnail, Warthin-like, spindle cell or clear cell subtype, or papillary "
                  "carcinoma with fibromatosis-like stroma", "8260",
                  "ICD-O-3.2 holds no separate term for this subtype.",
                  note="D5; registrar question 4."),
            # ICCR p. 10 "papillary microcarcinoma is not a histological subtype". Registrar
            # question 5.
            aid(named("Papillary microcarcinoma, with no subtype named", "8341",
                      note="Registrar question 5."), AID_MICRO),
            # ICCR p. 9 image "Papillary thyroid carcinoma 8260/3".
            named("No subtype named", "8260",
                  "ICD-O-3.2 gives Papillary carcinoma of thyroid as a related term of this "
                  "code.",
                  upgrade="The report does not name a subtype. A report that names one may give "
                          "a more specific code: go back and take the option that names it."),
        ], [],
        "Evidence th_ptc_subtype (departure 8). D1: papillary thyroid carcinoma is paediatric and "
        "its code depends on the subtype.")


def ftc_invasion():
    return node(
        n("ftc_invasion"), "histology_subclassification", 4, "Follicular carcinoma invasion",
        "What invasion does the report describe for the follicular carcinoma?",
        # Evidence th_ftc_invasion hint; ICCR p. 11 "defined as a tumour composed of 75% of
        # oncocytes".
        "Follicular carcinoma is defined by invasion of the capsule or vessels. A tumour with "
        "75% or more oncocytic cells is an oncocytic carcinoma, coded 8290/3 at every invasion "
        "extent: find it under another carcinoma the report names.",
        [
            # ICCR p. 11 "minimally invasive (CI only), encapsulated angioinvasive (any focus of
            # vascular invasion)".
            named("Minimally invasive: capsular invasion only", "8335",
                  note="Currency check §3: 8335/3 is Follicular carcinoma, minimally invasive."),
            # ICCR p. 2 "FTC, encapsulated angioinvasive".
            named("Encapsulated angioinvasive: invasion of a blood vessel", "8339",
                  note="Currency check §§3, 6: new in ICD-O-3.2, outside every ICCC-2017 range "
                       "(standing rule 3, XIb). REDCap lacks it: the REDCap-side list, not a "
                       "flag (departure 9)."),
            # ICCR p. 11 "grossly apparent extensive invasion of the thyroid and/or
            # extra-thyroid tissue"; ICCR p. 9 image "Follicular thyroid carcinoma 8330/3".
            aid(named("Widely invasive", "8330",
                      "ICD-O-3.2 gives Follicular adenocarcinoma, NOS as a synonym of this "
                      "code."), AID_WIDELY_INVASIVE),
            # ICCR p. 9 image "Follicular thyroid carcinoma 8330/3".
            named("Invasive, extent not described", "8330",
                  upgrade="A report that states the extent of invasion may give a more specific "
                          "code: minimally invasive (8335/3) or encapsulated angioinvasive "
                          "(8339/3)."),
            # ICCR p. 10 "If an encapsulated follicular patterned tumour has questionable
            # capsular/vascular invasion".
            excl("Encapsulated, with questionable invasion (uncertain malignant potential)",
                 "8335", "1",
                 what="an encapsulated follicular tumour with questionable capsular or vascular "
                      "invasion"),
            # ICCR p. 11 "primarily depends on the identification of invasion of the tumour
            # capsule"; icdo32.sqlite 8335/1 Synonym Follicular carcinoma, encapsulated, NOS.
            # Registrar question 2.
            excl("Encapsulated follicular carcinoma, no invasion described", "8335", "1",
                 what="an encapsulated follicular carcinoma with no invasion described",
                 extra="ICD-O-3.2 lists Follicular carcinoma, encapsulated, NOS as a synonym of "
                       "this code; only the minimally invasive tumour stays 8335/3.",
                 decision=True, note="Currency check §3; registrar question 2."),
        ], [],
        "Evidence th_ftc_invasion. Currency check §3: 8335 moved /3 to /1 except the minimally "
        "invasive tumour; 8339/3 is new. D1 exception: the code depends on the invasion.")


def dhgtc():
    return node(
        n("dhgtc"), "histology_subclassification", 4, "High-grade differentiated carcinoma",
        "What is the dominant type of the high-grade differentiated thyroid carcinoma?",
        "The report names a carcinoma with tumour necrosis or 5 or more mitoses per 2 mm2 that "
        "keeps its papillary, follicular or oncocytic pattern. It is coded by that type.",
        [
            # ICCR p. 2 "High grade papillary thyroid carcinoma, specify subtype".
            go("High-grade papillary thyroid carcinoma", n("ptc_subtype")),
            # ICCR p. 2 "High grade follicular thyroid carcinoma, specify".
            go("High-grade follicular thyroid carcinoma", n("ftc_invasion")),
            # ICCR p. 2 "High grade invasive encapsulated follicular variant".
            named("High-grade invasive encapsulated follicular variant of papillary thyroid "
                  "carcinoma", "8343"),
            # ICCR p. 2 "High grade oncocytic carcinoma of the thyroid".
            named("High-grade oncocytic carcinoma of the thyroid", "8290",
                  "ICD-O-3.2 gives Oncocytic carcinoma as a synonym of this code."),
            # ICCR p. 12 "HGDTCs need be subclassified according to their dominant histotype".
            # D4: no ICD-O-3.2 code for the entity without a dominant type; registrar question 6.
            named("The report does not name the dominant type", "8010",
                  "ICD-O-3.2 has no code for a high-grade differentiated thyroid carcinoma whose "
                  "dominant type the report does not name, so the generic carcinoma code is "
                  "recorded. This awaits the registrar's decision.",
                  upgrade=TYPE_NOT_STATED, note="D4 (departure 10); registrar question 6."),
        ], [],
        "Evidence th_dhgtc. D1 exception: the code is the dominant type's. D4: the evidence's "
        "code-less option records the nearest generic code.")


def ihc():
    return ihc_node(
        P,
        [
            {"group_label": "Follicular cell origin", "markers": ["Thyroglobulin", "TTF-1"]},
            {"group_label": "Medullary thyroid carcinoma (C cells)", "markers": ["Calcitonin"]},
            {"group_label": "Cribriform-morular thyroid carcinoma",
             "markers": ["Beta-catenin (nuclear)"]},
            {"group_label": "Secretory carcinoma",
             "markers": ["GATA3", "Mammaglobin", "S100 protein"]},
        ],
        [
            rule(["Calcitonin"], "8345",
                 "Calcitonin is positive and thyroglobulin is not: the medullary thyroid "
                 "carcinoma pattern (Juhlin 2022, p. 7; ICCR thyroid dataset, p. 19). "
                 "Recorded as Medullary thyroid carcinoma (8345/3).",
                 negative=["Thyroglobulin"],
                 note="Evidence ihc_rules 1. ICCR p. 19 'calcitonin, chromogranin, "
                      "synaptophysin, carcinoembryonic antigen (CEA) and thyroglobulin may be "
                      "performed' and 'Thyroglobulin, thyroid transcription factor-1 (TTF-1) and "
                      "PAX8 may indicate'; Juhlin p. 7 'verified by calcitonin "
                      "immunohistochemistry'."),
            rule(["Beta-catenin (nuclear)"], "8201",
                 "Nuclear beta-catenin is positive and thyroglobulin is not: the "
                 "cribriform-morular thyroid carcinoma pattern (Juhlin 2022, p. 7). Recorded as "
                 "Cribriform carcinoma, NOS (8201/3).",
                 negative=["Thyroglobulin"],
                 note="Evidence ihc_rules 2. Juhlin p. 7 'presence of nuclear and cytoplasmic "
                      "beta-catenin expression' and 'these tumors lack expression of "
                      "thyroglobulin'. ICCR Table 1 (p. 9, image) codes the entity 8201/3."),
            rule(["GATA3", "Mammaglobin", "S100 protein"], "8502",
                 "GATA3, mammaglobin and S100 protein are positive, and TTF-1 and thyroglobulin "
                 "are not: the secretory carcinoma pattern (Juhlin 2022, p. 7). Recorded as "
                 "Secretory carcinoma (8502/3).",
                 negative=["TTF-1", "Thyroglobulin"],
                 note="Evidence ihc_rules 3. Juhlin p. 7 'positive for GATA3, mammaglobin, "
                      "GCDFP15 and S100 protein' and 'consistently negative for TTF1 and "
                      "thyroglobulin'. D11: no ICCC-2017 range holds 8502 at C73.9."),
        ],
        fallback="8010",
        fallback_reason=("The stains do not establish the carcinoma's type. Recorded as "
                         "Carcinoma, NOS (8010/3). Thyroglobulin, TTF-1 and PAX8 show that a "
                         "tumour comes from follicular cells; they do not name its type (ICCR "
                         "thyroid dataset, p. 19)."),
        hint="The histology report calls the tumour a carcinoma without naming its type. Answer "
             "'Not done or not readable' for a stain the report does not mention. Thyroglobulin, "
             "TTF-1 and PAX8 show that a tumour comes from follicular cells; they do not name its "
             "type.",
        note="Evidence th_ihc and ihc_rules (departure 11). Fallback 8010/3: ICCR p. 19 "
             "'Thyroglobulin, thyroid transcription factor-1 (TTF-1) and PAX8 may indicate'. "
             "Mucoepidermoid carcinoma has no rule: Juhlin p. 7 gives p63 and CK5 as confirming "
             "stains and no marker that separates it (evidence §4).")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # ICCR p. 10 "As NIFTP is not overtly malignant".
            excl("Non-invasive follicular thyroid neoplasm with papillary-like nuclear features "
                 "(NIFTP)", "8349", "1",
                 what="a non-invasive follicular thyroid neoplasm with papillary-like nuclear "
                      "features"),
            # ICCR p. 11 "labelled as follicular tumour of uncertain malignant potential
            # (FT-UMP)".
            excl("Follicular tumour of uncertain malignant potential", "8335", "1",
                 what="a follicular tumour of uncertain malignant potential"),
            # ICCR p. 11 "well differentiated tumour of uncertain malignant potential (WDT-UMP)".
            excl("Well differentiated tumour of uncertain malignant potential", "8348", "1",
                 what="a well differentiated tumour of uncertain malignant potential"),
            # ICCR p. 9 image "Hyalinizing trabecular tumour 8336/1". Currency check §3: /0 to
            # /1. D6: a report calling it malignant is registrar question 9.
            excl("Hyalinizing trabecular tumour, or hyalinizing trabecular adenoma", "8336", "1",
                 what="a hyalinizing trabecular tumour",
                 extra="ICD-O-3.2 gives Hyalinizing trabecular adenoma as a synonym of this code.",
                 note="Currency check §3. A report that calls it malignant takes the histology "
                      "screen's option (registrar, 8 October 2026, review A6, E7)."),
            # Pfister p. 13 "Follicular adenoma of the thyroid".
            excl("Follicular adenoma, including follicular adenoma with papillary architecture",
                 "8330", "0", what="a follicular adenoma"),
            # Juhlin p. 3 "a diagnosis of oncocytic follicular adenoma requires".
            excl("Oncocytic adenoma, or Hurthle cell adenoma", "8290", "0",
                 what="an oncocytic adenoma",
                 extra="ICD-O-3.2 gives Oncocytic adenoma as a synonym and Hurthle cell adenoma "
                       "as a related term of this code."),
            # Juhlin p. 2 "making it impossible to distinguish between non-neoplastic and benign
            # neoplastic follicular neoplasms".
            nonrep("Thyroid follicular nodular disease, goitre or an adenomatous nodule",
                   "Not registrable. Follicular nodular disease is not a malignant tumour.",
                   note="Evidence th_histology."),
        ],
        where=WHERE,
        note="The six exclusions and the nodular disease line of evidence th_histology "
             "(departure 5).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), ptc_subtype(), ftc_invasion(), dhgtc(), ihc(),
                      not_malignant(), deposit_node(P, where=WHERE)]
    return make_tree(
        TREE_ID, nodes,
        subtype_screens=(n("ptc_subtype"), n("ftc_invasion")),
        # Standing rule 3 (D11): no ICCC-2017 range holds these at C73.9, and the evidence names
        # them: secretory carcinoma (th_picker option, Juhlin p. 7), thymoma and its types and
        # thymic carcinoma within the thyroid (ICCR p. 3; Juhlin p. 7; registrar question 7).
        d11=("8502", "8580", "8581", "8582", "8583", "8584", "8585", "8586"))


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
_IHC = ["Histology", "IHC"]
DECISIONS = {
    "8336/3": ("D6", EVIDENCE,
               "A hyalinizing trabecular tumour the report calls malignant, on the histology "
               "screen: the pathologist's stated behaviour (WHO coding Rule F; registrar, "
               "8 October 2026, review A6, E7). ICD-O-3.2 prints 8336 at /1 only; ICCC-2017 range "
               "121 places 8336/3 at C73.9 in XIb (ICCR Thyroid, PDF p. 9)."),
    "8260/3": ("D1, D3, D8", EVIDENCE,
               "Papillary thyroid carcinoma (Pfister 2022 Table 3) at basis 7 on the subtype "
               "screen for the classic, diffuse sclerosing, solid and other subtypes and when no "
               "subtype is named, and at basis 5 when cytology names it. The diffuse sclerosing "
               "subtype records 8260/3 because every 8350/3 term is obsolete (registrar question "
               "3)."),
    "8340/3": ("D1", EVIDENCE,
               "Infiltrative follicular variant of papillary thyroid carcinoma on the subtype "
               "screen (ICCR Table 1)."),
    "8341/3": ("D1", EVIDENCE,
               "Papillary microcarcinoma with no subtype named, on the subtype screen (registrar "
               "question 5)."),
    "8342/3": ("D1", EVIDENCE, "Oncocytic subtype of papillary thyroid carcinoma (ICCR Table 1)."),
    "8343/3": ("D1", EVIDENCE,
               "Invasive encapsulated follicular variant and encapsulated subtype of papillary "
               "thyroid carcinoma, and their high-grade form (ICCR Table 1, p. 2, p. 10)."),
    "8344/3": ("D1", EVIDENCE,
               "Tall cell and columnar cell subtypes of papillary thyroid carcinoma; ICD-O-3.2 "
               "holds tall cell as a synonym at 8344/3."),
    "8337/3": ("D1", EVIDENCE,
               "Poorly differentiated thyroid carcinoma, reported in adolescents (Juhlin 2022, "
               "p. 5)."),
    "8345/3": ("D1, D7, D8", EVIDENCE,
               "Medullary thyroid carcinoma (Pfister 2022 Table 3) on the histology screen, at "
               "basis 5 from cytology, at basis 4 with imaging and a raised serum calcitonin "
               "(Visser 2023 Table 4), and from the stain panel when calcitonin is positive and "
               "thyroglobulin negative.",
               {"diagnostic_tests_required": _IHC, "ihc_markers_required": ["Calcitonin"]}),
    "8588/3": ("D1", EVIDENCE,
               "Spindle epithelial tumour with thymus-like elements (Pfister 2022 Table 3)."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma whose type the report does not name: basis 7 on the histology screen and "
               "as the stain panel's fallback, basis 5 when cytology names a carcinoma without its "
               "type, and the nearest generic code for a high-grade differentiated thyroid "
               "carcinoma whose dominant type the report does not name (D4, registrar question "
               "6)."),
    "8335/3": ("D1", EVIDENCE,
               "Follicular carcinoma, minimally invasive, on the invasion screen; currency check "
               "§3 keeps only this tumour at 8335/3."),
    "8339/3": ("D1, D11", EVIDENCE,
               "Follicular carcinoma, encapsulated, angioinvasive on the invasion screen. New in "
               "ICD-O-3.2 and absent from REDCap: the REDCap-side list (standing rule 16)."),
    "8330/3": ("D1", EVIDENCE,
               "Follicular carcinoma, widely invasive or with no extent stated, on the invasion "
               "screen."),
    "8290/3": ("D1, D2", EVIDENCE,
               "High-grade oncocytic carcinoma on the dominant-type screen; any oncocytic "
               "carcinoma of the thyroid in the picker (registrar question 8)."),
    "8201/3": ("D2", EVIDENCE,
               "Cribriform-morular thyroid carcinoma (ICCR Table 1 codes it 8201/3) from the stain "
               "panel (nuclear beta-catenin positive, thyroglobulin negative; Juhlin 2022, p. 7) "
               "and in the picker.",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["Beta-catenin (nuclear)"]}),
    "8502/3": ("D2, D11", EVIDENCE,
               "Secretory carcinoma from the stain panel (GATA3, mammaglobin and S100 protein "
               "positive; TTF-1 and thyroglobulin negative; Juhlin 2022, p. 7) and in the picker. "
               "No ICCC-2017 range holds 8502 at C73.9; standing rule 3 keeps it in Group XI.",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["GATA3", "Mammaglobin", "S100 protein"]}),
}
