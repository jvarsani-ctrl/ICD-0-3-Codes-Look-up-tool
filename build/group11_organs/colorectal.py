"""g11_colorectal (prefix cr_) and g11_appendix (prefix ap_): carcinomas of the colon, rectum and
anus (C18.0, C18.2-C18.9, C19.9, C20.9, C21.0-C21.8, ICCC-3 subgroup XIf2) and of the appendix
(C18.1, XIf3).

One module builds both trees; build(tree_id) dispatches. Both are built from
docs/group_11_evidence/XIf2_XIf3_digestive.json, which covers every digestive organ: this module
takes the evidence agent's nodes dg_document_inventory, dg_marker, dg_cytology,
dg_colorectal_histology, dg_appendix_histology, dg_net_grade, dg_not_malignant_gut and
dg_carcinoma_picker, and leaves dg_site's other organs and the oesophagus, stomach, small
intestine, biliary and pancreas screens to the digestive family module. Every option's label,
code, behaviour, basis, reason and recognition aid comes from that file; the cite (file, page,
quotation) is the comment above the option or the aid. File names in the comments are the
evidence's own:
    Nagtegaal  XIf2-colorectum-XIf3-appendix-XIf10-digestive__Nagtegaal-2019.txt (Nagtegaal ID,
               et al. The 2019 WHO classification of tumours of the digestive system.
               Histopathology 2020;76:182-188). Cited by PDF page.
    Pfister    ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355).
               Cited by PDF page.
    Polat      XIf2-colorectum-paediatric__Polat-2021.txt (Colorectal Carcinoma in Childhood.
               JPGN Rep 2021;2:e039). A PubMed Central text: "PMC section" is the evidence's
               page field.
    Mahajan    XIf2-colorectum-paediatric__Mahajan-2022.txt (Pediatric Colorectal Carcinoma: A
               Series of Seven Cases. J Indian Assoc Pediatr Surg 2022). PMC section.
    Roganovic  XIf3-appendix-neuroendocrine-paediatric__Roganovic-2026.txt (Appendiceal
               Neuroendocrine Tumors in Children and Adolescents. Acta Med Acad 2026). PMC
               section.
    ICCR-St    XIf10-stomach__ICCR-Stomach-3rd.txt; ICCR-Oe  XIf10-oesophagus__ICCR-Oesophagus-
               3rd.txt. "image" marks a quotation read from the page image of the WHO table.
    Rules      RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser     Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's
               file set, so the evidence carries no page quotation for it)

Nodes of g11_colorectal, in tree order:
    cr_document_inventory  document_inventory  evidence gate (evidence dg_document_inventory)
    cr_labs_referral, cr_labs_markers, cr_labs_cytology, cr_labs_histology  lab_results
    cr_clinical, cr_clinical_cytology  clinical_alias
    cr_imaging, cr_imaging_markers, cr_imaging_cytology  morphology_only  (evidence dg_marker)
    cr_cytology            morphology_only     (evidence dg_cytology)
    cr_histology           histology_subclassification  (evidence dg_colorectal_histology)
    cr_net_grade           histology_subclassification  (evidence dg_net_grade)
    cr_not_malignant       histology_subclassification  (evidence dg_not_malignant_gut)
    cr_deposit             morphology_only      (D10)
    cr_picker              histology_subclassification  (D2; evidence dg_carcinoma_picker)
Nodes of g11_appendix: the same with the prefix ap_, from dg_appendix_histology in place of
dg_colorectal_histology.

Departures from the evidence nodes, and why
-------------------------------------------
1. dg_site is not built. The router's site capture chose the tree (D14), so its organ question,
   its liver referral and the other digestive organs are answered before the tree begins. Its
   Rule B and Rule C advice moves to the gate hint: tissue beside the bowel, such as retrocaecal
   tissue, is C48.0 (Rules PDF p. 4), and one tumour spanning two parts of the colon is C18.8,
   spanning the rectum, anus and anal canal C21.8 (Rules PDF p. 5).
2. dg_document_inventory: the referral and imaging-only tiers recorded 8000/3 at basis 1 and 2
   on the gate itself. D7: each routes to its own screen (cr_clinical, cr_imaging), which refers
   the case to Group XII with refer_code 8000, because ICCC-2017 places 8000/3 in XIIb at every
   routed site (the evidence's own conflicts entry for Group 12 says the same). The evidence's
   "possible, probable or suspected" line is not built as written: Visser rule 4 makes only
   "possible" non-registrable, so a probable tumour reaches the Group XII referral and a
   possible one the common non-registrable line. The gate's options are the contract §4.2 tiers
   with laboratory copies (registrar, 6 October 2026); the hint drops "Choose the strongest
   evidence the file holds", which the document checklist replaces.
3. dg_marker: a lab_results screen cannot choose a code (registrar, 6 October 2026; Group 10
   lesson). Its code options move to <p>imaging_markers, which reads the report's own words, and
   the <p>labs_* screens record the values. Of its eight Visser Table 4 rows only chromogranin A
   (8240/3) and serotonin (8241/3) are built here (controller's instruction for these trees): the
   other six (insulin, glucagon, gastrin, vasoactive intestinal peptide, somatostatin,
   adrenocorticotropic hormone) name functioning tumours of the pancreas and the other digestive
   organs, which the digestive family tree carries. Serotonin is listed first, because a tumour
   with both markers raised takes the higher code (Rule K). The colorectal tree adds Visser
   Table 4's colorectal cancer with carcinoembryonic antigen row (contract §0.5), which records
   8000/3 at basis 4 and therefore refers to Group XII with refer_code 8000. The appendix tree
   does not offer that row: its diagnosis is colorectal cancer, and a malignant tumour on imaging
   reaches the same Group XII referral at basis 2. The evidence's "Another raised result, and
   the imaging report states a malignant tumour" (8000/3, basis 2) is the common Group XII line.
   The laboratory screens record serum chromogranin A and serotonin, and on the colorectal tree
   carcinoembryonic antigen. No source in the part prints a unit; the unit lists follow Group
   10's carcinoembryonic antigen row where one exists and are the registrar's to confirm. Roganovic
   (evidence data gap 5) states that raised chromogranin A or urinary 5-HIAA has not been
   described in children with appendiceal neuroendocrine tumours, and Mahajan that the role of
   carcinoembryonic antigen in children is not established: the marker answers rest on the
   registrar's Visser rule alone (registrar question 7).
4. dg_cytology: "A named tumour type" sent the clerk to the histology screen, whose codes record
   at basis 7. D8: cytology that names an entity records it at basis 5, so the cytology screen
   names the types itself: on the colorectal tree the paediatric types a cytology report can name
   (mucinous adenocarcinoma, signet ring cell carcinoma, adenocarcinoma) and the evidence's
   neuroendocrine tumour; on the appendix tree neuroendocrine tumour and adenocarcinoma.
   Tubular adenocarcinoma (an architectural type) and adenocarcinoma in familial adenomatous
   polyposis (a clinical setting) are not cytology answers. "Malignant, with no tumour type
   named" (8000/3, basis 5) becomes the common referral to Group XII with refer_code 8001 (D8).
   "Carcinoma, with no type named" is cyto_carcinoma_nos(); the lymphoma referral is kept.
5. dg_colorectal_histology: the neuroendocrine tumour moves from the picker to its own option
   and grade screen, cr_net_grade. D1 exception: its code depends on the grade (8240/3 or
   8249/3), which the picker cannot ask. A generic "carcinoma whose type the report does not
   name" option (8010/3) is added (contract §4.2). The exclusions move to cr_not_malignant
   (contract §4.2). The trailing options are tail_options(): melanoma (D13; the bowel is a
   mucosal site, so the hop enters me_mucosa), the picker (relabelled with the evidence's
   examples), the exclusion screen, the deposit question (D10; the evidence's referral with no
   group and recapture_site is that question), "Malignant tumour, type not determined" (Group
   XII, 8000, D7), and the referrals lymphoma (evidence label, Burkitt lymphoma), leukaemia,
   gastrointestinal stromal tumour (Group XII; refer_code 8936, the evidence's code), sarcoma
   (evidence label), germ cell tumour and another named tumour. NUT carcinoma has no option: D12
   does not name the bowel, so 8023/3 is a picker entry.
6. The five paediatric colorectal options rest on carcinomas of the colon, rectosigmoid junction
   and rectum (Polat, Mahajan). The tree also serves the anus (C21.0-C21.8), and the engine cannot
   filter options by site, so they show at the anus too (evidence data gap 7, for the registrar).
   Squamous cell carcinoma of the anal canal stays a picker entry, as the evidence has it: the
   picker lists its ICD-O-3.2 forms (8070/3 and the human papillomavirus-positive and -negative
   codes 8085/3 and 8086/3) by name.
7. dg_appendix_histology: the low-grade appendiceal mucinous neoplasm exclusion moves to
   ap_not_malignant, which the evidence's exclusion screen also held it on (a merged duplicate);
   the exclusion option's label names it. Its reason no longer says "or calls the tumour
   malignant": D6 builds no stated-behaviour code, so only a report that diagnoses an invasive
   mucinous adenocarcinoma leaves the exclusion. Goblet cell adenocarcinoma moves from the picker
   to the histology screen. D3 says the tree offers the current entity's code (8243/3, never
   8245/3), and ICD-O-3.2 holds no term "goblet cell adenocarcinoma" (evidence code currency,
   8243): its Preferred term is the retired name Goblet cell carcinoid, so a clerk who types the
   WHO name in the picker finds nothing. The option names the entity as the report does and
   records 8243/3. Generic adenocarcinoma (8140/3) and carcinoma (8010/3) options are added
   (contract §4.2). The trailing options are tail_options(), as departure 5, without the
   gastrointestinal stromal tumour referral, which the evidence does not give the appendix.
8. dg_net_grade is built once per tree (cr_net_grade, ap_net_grade), because every node id
   carries its tree's prefix. Its hint cites Rule G for two grades and adds the Rule K choice for
   a report that names a grade and the cell type or hormone together (D5): grade 2 and grade 3
   (8249/3) are higher than every cell-type and hormone code; with grade 1 or no grade the clerk
   finds the named type in the picker. The evidence's picker hint gives the same instruction
   (registrar question 8). The last option's label adds a tumour named by its cell type or
   hormone, such as an enterochromaffin cell (serotonin-producing) tumour, 8241/3 in the picker.
9. dg_not_malignant_gut is split by tree. Each tree keeps the lesions whose evidence entity lists
   the tree's sites: the colorectal tree drops 8144/0 (stomach, small intestine), 8052/0 and
   8060/0 (oesophagus) and 8480/1 (appendix); the appendix tree drops those and 8220/0 and
   8077/0, 8077/2 (anus). The hint keeps the evidence's "if the report states invasion, go back";
   "or calls the lesion malignant" is not carried (D6). "Another benign lesion" is the common
   catch-all.
10. dg_carcinoma_picker: D2 replaces the evidence's curated list. Labels are ICD-O-3.2 Preferred
   terms, search_terms the live synonyms and related terms, and the options carry no
   recognition aid, so the evidence's picker aids (mucinous adenocarcinoma, signet ring cell or
   poorly cohesive carcinoma, hepatoid adenocarcinoma, goblet cell adenocarcinoma, adenosquamous
   carcinoma, neuroendocrine carcinoma, mixed neuroendocrine-non-neuroendocrine neoplasm) are
   not shown; the build report lists them.
11. Not built from the evidence: 8245/3 Adenocarcinoid tumor, 8124/3 Cloacogenic carcinoma and
   8512/3 (D3; the registrar ruled on 8 October 2026, review A5, E7, that an adenocarcinoid takes
   Rule K's 8244/3, built on the appendix histology screen),
   high-grade appendiceal mucinous neoplasm and malignant gastrointestinal neuroectodermal tumour
   (no source in the part gives an ICD-O-3.2 code: evidence data gaps 2 and 6; the sarcoma
   referral covers the latter), and a Rule F stated-behaviour code for the low-grade appendiceal
   mucinous neoplasm (D6).

Registrar questions the evidence raised (XIf2_XIf3_digestive.md §10, questions 1, 4, 7 and 8 for
these trees) and data gaps 4, 5, 7 and 8 stay open; the defaults above apply until they are
answered (docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, aid, cyto, cyto_carcinoma_nos, deposit_node,
                            evidence_gate, excl, go, lab, make_tree, marker, named, node,
                            not_malignant_node, refer, refer_germ_cell, refer_leukaemia,
                            refer_lymphoma, refer_other_named, refer_sarcoma, refer_unspecified,
                            tail_options, term)

CR, AP = "g11_colorectal", "g11_appendix"
PREFIX = {CR: "cr_", AP: "ap_"}
WHERE = {CR: "the colon, rectum or anus", AP: "the appendix"}
EVIDENCE = "XIf2_XIf3_digestive"
VISSER_NOTE = ("Visser O, et al. Front Oncol 2023;13:1250549, Table 4, p. 06, read from the page "
               "image (contract §0.5), with rule 6, p. 05 (basis 4 never stands alone).")


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Mahajan PMC section 4 "Tumor cells are seen floating in pools of extracellular mucin".
AID_MUCINOUS = "Reports describe tumour cells floating in pools of extracellular mucin."
# Mahajan PMC section 4 "Tumor cells show intracellular mucin"; PMC section 5 "signet ring cells
# constitute more than 50% of tumor".
AID_SIGNET = ("Reports describe tumour cells holding mucin inside the cell, with signet ring cells "
              "making up more than half of the tumour.")
# Nagtegaal p. 4 "well-differentiated neuroendocrine tumours (NETs) and poorly differentiated
# neuroendocrine carcinomas (NECs)" and "NET, G1 Well differentiated Low <2 <3%"; Roganovic PMC
# section 4 "Pediatric aNETs are typically well-differentiated, low- to intermediate-grade
# tumors".
AID_NET = ("The report calls the tumour well differentiated and may give a grade (grade 1, 2 or "
           "3, written G1, G2 or G3), a Ki-67 index or a mitotic count.")
# Nagtegaal p. 4 "NET, G1 Well differentiated Low <2 <3%"; Roganovic PMC section 4 "Mitosis and
# Ki-67 index are usually low (<3%), consistent with the grade 1".
AID_G1 = "Ki-67 index below 3% and fewer than 2 mitoses per 2 mm2."
# Nagtegaal p. 4 "NET, G2 Intermediate 2-20 3-20%".
AID_G2 = "Ki-67 index from 3% to 20%, or 2 to 20 mitoses per 2 mm2."
# Nagtegaal p. 4 "NET, G3 High >20 >20%"; p. 5 "well-differentiated NETs may be high grade".
AID_G3 = ("Ki-67 index above 20%, or more than 20 mitoses per 2 mm2, in a tumour the report calls "
          "well differentiated.")
# Nagtegaal p. 4 "renamed goblet cell adenocarcinoma (formerly called goblet cell
# carcinoid/carcinoma) of the appendix"; p. 2 "recognised to have a minor neuroendocrine
# component".
AID_GOBLET = "Reports describe a carcinoma of the appendix with a minor neuroendocrine component."


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence dg_document_inventory, dg_marker, dg_cytology)
# ------------------------------------------------------------------------------------------
# Evidence lab_tests rows 1 and 2: chromogranin A and serotonin in serum, with the role the
# registrar's Visser Table 4 rule gives them. No file in the part prints a unit. The
# chromogranin A and carcinoembryonic antigen units follow Group 10's carcinoembryonic antigen
# row (ng/mL equals µg/L); the serotonin units are mass and molar concentration. The registrar
# confirms all three.
LAB_CHROMOGRANIN = lab("chromogranin_a", "Serum chromogranin A", ("ng/mL", "µg/L"))
LAB_SEROTONIN = lab("serotonin", "Serum serotonin", ("ng/mL", "nmol/L"))
# Contract §0.5 (Visser Table 4, colorectal cancer with carcinoembryonic antigen); Mahajan,
# evidence data gap 5 ("the role of carcinoembryonic antigen in paediatric colorectal carcinoma
# is not established").
LAB_CEA = lab("cea", "Serum carcinoembryonic antigen (CEA)", ("ng/mL", "µg/L"))


def _markers(where_of, tree_id):
    """The Visser Table 4 rows for these sites (departure 3). Serotonin first: Rule K."""
    out = [
        # Evidence tissue_free row 9 and dg_marker option 7 ("Serotonin", 8241/3, basis 4).
        marker("8241", test="serum serotonin", diagnosis="serotonin-producing neuroendocrine "
                                                         "tumour", where=where_of,
               label="Imaging shows a tumour %s, the report calls serum serotonin raised (with "
                     "or without a raised chromogranin A), and the file calls it a "
                     "serotonin-producing neuroendocrine tumour or carcinoid" % where_of,
               note=VISSER_NOTE + " Functioning neuroendocrine tumour, serotonin. Evidence "
                                  "XIf2_XIf3_digestive.json tissue_free row 9, dg_marker option "
                                  "7."),
        # Evidence tissue_free row 3 and dg_marker option 1 ("Chromogranin A", 8240/3, basis 4).
        marker("8240", test="serum chromogranin A", diagnosis="neuroendocrine tumour",
               where=where_of,
               label="Imaging shows a tumour %s, the report calls serum chromogranin A raised, "
                     "and the file calls it a neuroendocrine tumour or carcinoid" % where_of,
               note=VISSER_NOTE + " Neuroendocrine tumour, chromogranin A; the row names no "
                                  "site. Evidence tissue_free row 3, dg_marker option 1."),
    ]
    if tree_id == CR:
        # Contract §0.5: Visser Table 4 colorectal cancer with carcinoembryonic antigen gives
        # 8000/3, which ICCC-2017 places in XIIb at these sites.
        out.append(refer_unspecified(
            "Imaging shows a tumour of the colon or rectum, the report calls serum "
            "carcinoembryonic antigen raised, and the file calls it colorectal cancer", "8000", 4,
            "A raised carcinoembryonic antigen with a colorectal cancer shown on imaging "
            "registers the cancer without its type (Visser 2023, European Network of Cancer "
            "Registries, Table 4).",
            where=WHERE[CR],
            captures={"workup_status": "incomplete", "basis_evidence_tier": "markers_cea"},
            note="D7. " + VISSER_NOTE + " Colorectal cancer, carcinoembryonic antigen: 8000/3, "
                 "XIIb at the routed sites, so the referral names refer_code 8000."))
    return out


def _gate(tree_id):
    P, where = PREFIX[tree_id], WHERE[tree_id]
    if tree_id == CR:
        where_of = "of the colon, rectum or anus"
        labs = [LAB_CHROMOGRANIN, LAB_SEROTONIN, LAB_CEA]
        tests = "chromogranin A, serotonin or carcinoembryonic antigen"
        cytology = [
            # Mahajan PMC section 1 "showed mucinous adenocarcinoma in four/seven patients".
            cyto("Mucinous adenocarcinoma, or colloid carcinoma", "8480",
                 note="Evidence dg_cytology option 1 (a named type) with the paediatric type of "
                      "dg_colorectal_histology (departure 4)."),
            # Mahajan PMC section 1 "signet cell variant was seen in 2/7".
            cyto("Signet ring cell carcinoma", "8490",
                 note="Evidence dg_cytology option 1 with dg_colorectal_histology (departure 4)."),
            # Polat PMC section 2 "was compatible with poorly differentiated adenocarcinoma".
            cyto("Adenocarcinoma, with no subtype named", "8140",
                 note="Evidence dg_cytology option 1 ('such as ... adenocarcinoma')."),
            # Evidence dg_cytology option 1 ("such as ... neuroendocrine tumour").
            cyto("Neuroendocrine tumour, or carcinoid", "8240",
                 "Cytology does not give the tumour's grade.",
                 note="Evidence dg_cytology option 1 ('such as ... neuroendocrine tumour')."),
        ]
        hint_site = ("A tumour reported only in the tissue beside the bowel, such as retrocaecal "
                     "tissue, is not a tumour of the bowel: ICD-O-3.1 lists that tissue under "
                     "the retroperitoneum (C48.0), so go back to the site step. One tumour that "
                     "spans two parts of the colon is recorded at C18.8, and one that spans the "
                     "rectum, anus and anal canal at C21.8 (WHO coding Rule C).")
    else:
        where_of = "of the appendix"
        labs = [LAB_CHROMOGRANIN, LAB_SEROTONIN]
        tests = "chromogranin A or serotonin"
        cytology = [
            # Evidence dg_cytology option 1 ("such as ... neuroendocrine tumour"); Roganovic PMC
            # section 1 "represent the most frequent gastrointestinal epithelial tumors in this
            # age group".
            cyto("Neuroendocrine tumour, or carcinoid", "8240",
                 "Cytology does not give the tumour's grade.",
                 note="Evidence dg_cytology option 1 (departure 4)."),
            # Evidence dg_cytology option 1 ("such as ... adenocarcinoma").
            cyto("Adenocarcinoma, with no subtype named", "8140",
                 note="Evidence dg_cytology option 1 (departure 4)."),
        ]
        hint_site = ("A tumour reported only in the tissue beside the appendix and caecum, such "
                     "as retrocaecal tissue, is not a tumour of the appendix: ICD-O-3.1 lists "
                     "that tissue under the retroperitoneum (C48.0), so go back to the site "
                     "step.")
    cytology += [
        cyto_carcinoma_nos(note="Evidence dg_cytology option 2 ('Carcinoma, with no type "
                                "named', 8010/3, basis 5)."),
        # Evidence dg_cytology option 4; Pfister p. 6 "high-grade B-cell lymphomas (particularly
        # Burkitt lymphoma)".
        refer_lymphoma(where),
    ]
    return evidence_gate(
        P, where=where,
        question="What is in the file for this tumour %s?" % where_of,
        # Evidence dg_document_inventory hint, with dg_site's Rule B and Rule C advice
        # (departure 1): Rules PDF p. 4 "are listed and given the code number C48.0"; PDF p. 5
        # "when a single tumor overlaps the boundaries of two or more categories or
        # subcategories" and "C21.8 Overlapping lesion of rectum, anus and anal canal".
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. %s A report that calls the "
              "tumour possible or suspected does not register it." % hint_site),
        labs=labs, marker_tests=tests, markers=_markers(where_of, tree_id),
        tier_labels={
            # Evidence dg_document_inventory options 5 and 6.
            "cytology": "A cytology report (fine-needle aspiration, brushings or fluid) - no "
                        "histology report",
            "histology": "A histology report on a biopsy or resection, with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=cytology,
        note="Evidence dg_document_inventory, dg_marker and dg_cytology (departures 2 to 4 in "
             "the module docstring).")


# ------------------------------------------------------------------------------------------
# The trailing options and the referrals
# ------------------------------------------------------------------------------------------
def _relabel(branch, label):
    branch["label"] = label
    return branch


def _referrals(tree_id):
    where = WHERE[tree_id]
    out = [
        # Pfister p. 6 "high-grade B-cell lymphomas (particularly Burkitt lymphoma)"; ICCC-2017
        # places 9687 in IIc at every digestive site (evidence conflicts, Group 2).
        _relabel(refer_lymphoma(where), "Lymphoma, for example Burkitt lymphoma"),
        refer_leukaemia(where),
    ]
    if tree_id == CR:
        # Pfister p. 9 "Pediatric gastrointestinal stromal tumor (GIST)"; ICCC-2017 places 8936
        # in XIIa1 at every colorectal site (evidence conflicts, Group 12).
        out.append(refer(
            "Gastrointestinal stromal tumour (GIST)", 12,
            "A gastrointestinal stromal tumour is registered as %s (8936/3), which ICCC-3 places "
            "at %s in Group XII (other and unspecified malignant neoplasms), not in Group XI. "
            "Code the case from the Group XII tree." % (term("8936", "3"), where),
            refer_code="8936",
            note="Evidence dg_colorectal_histology option 9 (refer to Group 12, 8936/3). "
                 "ICCC-2017 XIIa1 at C18.0-C21.8; refer_code names the code Group XII "
                 "records."))
    out += [
        # Nagtegaal p. 3 "EWSR1 fusions in gastrointestinal clear cell sarcoma and malignant
        # gastrointestinal neuroectodermal tumour"; ICCC-2017 places 9044 in IXd7 and 8900-8920
        # in IXa (evidence conflicts, Group 9).
        refer_sarcoma(where, label="A sarcoma, for example rhabdomyosarcoma or clear cell "
                                   "sarcoma"),
        refer_germ_cell(where),
        refer_other_named(),
    ]
    return out


def _tail(tree_id, picker_label, not_malignant_label):
    P = PREFIX[tree_id]
    opts = tail_options(P, "mucosa", where=WHERE[tree_id], referrals=_referrals(tree_id),
                        not_malignant_label=not_malignant_label)
    for o in opts:
        if o.get("next_node") == P + "picker":
            _relabel(o, picker_label)
    return opts


# ------------------------------------------------------------------------------------------
# Histology: colon, rectum and anus (evidence dg_colorectal_histology)
# ------------------------------------------------------------------------------------------
RULE_K_HINT = ("Use the report's final diagnosis. When the report gives two tumour types for one "
               "tumour and no answer covers both, choose the answer with the higher code (WHO "
               "coding Rule K).")
UPGRADE_ADENO = ("The report does not name a subtype of adenocarcinoma. A report that names one "
                 "gives that subtype's own code: go back and take the option that names it, or "
                 "find it under another carcinoma the report names.")


def colorectal_histology():
    P = PREFIX[CR]
    opts = [
        # Mahajan PMC section 1 "showed mucinous adenocarcinoma in four/seven patients and signet
        # cell variant was seen in 2/7"; Polat PMC section 2 "Histopathology of the tumors
        # confirmed a mucinous adenocarcinoma in the remaining 4 patients"; Mahajan PMC section 5
        # "more than 50% of pediatric patients are diagnosed with poorer histological subtypes
        # such as mucinous". D1: paediatric, the commonest type.
        aid(named("Mucinous adenocarcinoma, or colloid carcinoma", "8480",
                  "ICD-O-3.2 gives Colloid carcinoma as a synonym of this code.",
                  note="D1: Polat 2021, Mahajan 2022."), AID_MUCINOUS),
        # Mahajan PMC section 1 (as above); PMC section 5 "subtypes such as mucinous and signet
        # ring cell type". D1.
        aid(named("Signet ring cell carcinoma, or signet ring cell variant of adenocarcinoma",
                  "8490", "ICD-O-3.2 gives Signet ring cell adenocarcinoma as a synonym of this "
                          "code.", note="D1: Mahajan 2022."), AID_SIGNET),
        # Polat PMC section 2 "was compatible with poorly differentiated adenocarcinoma"; Mahajan
        # PMC section 4 "swelling (4 month) Right - NOS Guided biopsy". D1.
        named("Adenocarcinoma with no subtype named, including poorly differentiated "
              "adenocarcinoma", "8140", "The grade is not part of the code.",
              upgrade=UPGRADE_ADENO, note="D1: Polat 2021, Mahajan 2022."),
        # Mahajan PMC section 5 "arise in the setting of hereditary cancer syndromes, more
        # commonly FAP and HNPCC"; Polat PMC section 3 "The most common predisposing factors are
        # familial adenomatous polyposis". D1.
        named("Adenocarcinoma arising in familial adenomatous polyposis", "8220",
              note="D1: Mahajan 2022, Polat 2021."),
        # Polat PMC section 2 "Solid mass in descending colon RS, DC None MA + TA" and "MA,
        # mucinous adenocarcinoma; TA, tubular adenocarcinoma". D1; evidence data gap 8: the only
        # paediatric report gives it as a component of a mucinous adenocarcinoma.
        named("Tubular adenocarcinoma", "8211", note="D1: Polat 2021; evidence data gap 8."),
        # Nagtegaal p. 4 "well-differentiated neuroendocrine tumours (NETs) and poorly
        # differentiated neuroendocrine carcinomas (NECs)". D1 exception: the code needs the
        # grade (departure 5).
        aid(go("Neuroendocrine tumour, or carcinoid", P + "net_grade",
               note="D1 exception (grade screen); moved from the evidence's picker."), AID_NET),
        # Contract §4.2: the generic carcinoma option; D4's nearest generic code.
        named("A carcinoma whose type the report does not name", "8010", upgrade=TYPE_NOT_STATED,
              note="Contract §4.2 generic option (departure 5)."),
    ] + _tail(
        CR,
        # Evidence dg_colorectal_histology option 6.
        "Another carcinoma or neuroendocrine tumour the report names, such as serrated "
        "adenocarcinoma, squamous cell carcinoma or neuroendocrine carcinoma - type its name to "
        "find it",
        # Evidence dg_colorectal_histology option 7.
        "An adenoma, a polyp, a serrated lesion, polyposis or dysplasia, or another tumour the "
        "report calls benign, borderline or in situ")
    return node(
        P + "histology", "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence dg_colorectal_histology hint; Rules (Rule K).
        RULE_K_HINT + " A mucinous adenocarcinoma with a tubular component is 8480.",
        opts, [],
        "Evidence dg_colorectal_histology (departures 5 and 6). D1: the paediatric entities are "
        "mucinous adenocarcinoma, signet ring cell carcinoma, adenocarcinoma, adenocarcinoma in "
        "familial adenomatous polyposis and tubular adenocarcinoma (Polat 2021, Mahajan 2022); "
        "the neuroendocrine tumour is an option because its code needs the grade. The Rule K "
        "example is Polat 2021 Table 1 (MA + TA), which the evidence records 8480/3.")


# ------------------------------------------------------------------------------------------
# Histology: appendix (evidence dg_appendix_histology)
# ------------------------------------------------------------------------------------------
def appendix_histology():
    P = PREFIX[AP]
    opts = [
        # Pfister p. 13 "Gastrointestinal tract Epithelial tumors Gastroblastoma Appendiceal
        # NETs"; Nagtegaal p. 4; Roganovic PMC section 1 "represent the most frequent
        # gastrointestinal epithelial tumors in this age group"; PMC section 4 "Pediatric aNETs
        # are typically well-differentiated, low- to intermediate-grade tumors". D1.
        aid(go("Neuroendocrine tumour, or carcinoid", P + "net_grade",
               note="D1: Pfister 2022 Table 3, Roganovic 2026."), AID_NET),
        # Nagtegaal p. 4 "renamed goblet cell adenocarcinoma (formerly called goblet cell
        # carcinoid/carcinoma) of the appendix". D3: the current entity's code, never 8245/3.
        aid(named("Goblet cell adenocarcinoma, also reported as goblet cell carcinoid or goblet "
                  "cell carcinoma", "8243",
                  "The WHO digestive system classification (5th edition) renamed this tumour "
                  "goblet cell adenocarcinoma; ICD-O-3.2 keeps its former name for this code.",
                  note="D3 (departure 7): moved from the evidence's picker because ICD-O-3.2 "
                       "holds no term 'goblet cell adenocarcinoma'. Evidence code currency "
                       "8243. Adenocarcinoid takes the option below (review A5, E7)."),
            AID_GOBLET),
        # Registrar, 8 October 2026 (review A5, E7): "Use rule K". 8245/3 Adenocarcinoid tumor is
        # [obs] (D3). Rule K (ICD-O-3.1 printed p. 24): the term names adenocarcinoma (8140) and
        # carcinoid (8240), and one code includes both, 8244/3, whose ICD-O-3.2 synonyms are
        # "Mixed carcinoid and adenocarcinoma" and "Combined carcinoid and adenocarcinoma".
        named("Adenocarcinoid tumour", "8244",
              "ICD-O-3.2 marks the term Adenocarcinoid tumor obsolete. The term names an "
              "adenocarcinoma and a carcinoid, and this is the one code that includes both: "
              "ICD-O-3.2 gives Mixed carcinoid and adenocarcinoma as a synonym (WHO coding Rule "
              "K). A report that names goblet cell adenocarcinoma or goblet cell carcinoid takes "
              "that option instead.",
              note="Registrar, 8 October 2026 (review A5, E7): Rule K."),
        # Nagtegaal p. 3 "pathogenesis of adenocarcinomas of the intestines (the small and large
        # bowel and the appendix)". Contract §4.2 generic option.
        named("Adenocarcinoma with no subtype named", "8140", upgrade=UPGRADE_ADENO,
              note="Contract §4.2 generic option (departure 7); evidence entity 'Adenocarcinoma "
                   "NOS' (C18.1, picker)."),
        named("A carcinoma whose type the report does not name", "8010", upgrade=TYPE_NOT_STATED,
              note="Contract §4.2 generic option (departure 7)."),
    ] + _tail(
        AP,
        # Evidence dg_appendix_histology option 3.
        "Another carcinoma the report names, such as mucinous adenocarcinoma, signet ring cell "
        "carcinoma or neuroendocrine carcinoma - type its name to find it",
        # Evidence dg_appendix_histology options 2 and 4.
        "A low-grade appendiceal mucinous neoplasm, an adenoma, a serrated lesion or dysplasia, "
        "or another tumour the report calls benign, borderline or in situ")
    return node(
        P + "histology", "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence dg_appendix_histology hint; Rules (Rule K).
        RULE_K_HINT,
        opts, [],
        "Evidence dg_appendix_histology (departure 7). D1: the appendiceal neuroendocrine tumour "
        "is the paediatric entity (Pfister 2022, Roganovic 2026); goblet cell adenocarcinoma is "
        "an option under D3; the generic options follow contract §4.2.")


# ------------------------------------------------------------------------------------------
# Neuroendocrine tumour grade (evidence dg_net_grade)
# ------------------------------------------------------------------------------------------
def net_grade(tree_id):
    P = PREFIX[tree_id]
    return node(
        P + "net_grade", "histology_subclassification", 4, "Neuroendocrine tumour grade",
        "Which grade does the report give the neuroendocrine tumour?",
        # Evidence dg_net_grade hint; rules_a_to_k G (Nagtegaal 2020 Table 2 footnote) and K
        # (the evidence's picker hint, registrar question 8).
        "If the report gives two grades, or the Ki-67 index and the mitotic count point to "
        "different grades, choose the higher grade (WHO coding Rule G). A neuroendocrine "
        "carcinoma (poorly differentiated, small cell or large cell) is the last answer. When "
        "the report names the tumour's cell type or hormone as well as a grade, choose the "
        "answer with the higher code (WHO coding Rule K): grade 2 and grade 3 (8249) are higher "
        "than every cell-type or hormone code; with grade 1 or no grade, take the last answer "
        "and find the named type.",
        [
            # Nagtegaal p. 4 "NET, G1 Well differentiated Low <2 <3%"; Roganovic PMC section 4
            # "Mitosis and Ki-67 index are usually low (<3%), consistent with the grade 1".
            aid(named("Grade 1 (G1)", "8240",
                      "ICD-O-3.2 gives Neuroendocrine tumor, grade 1 as a related term of this "
                      "code."), AID_G1),
            # Nagtegaal p. 4 "NET, G2 Intermediate 2-20 3-20%"; Roganovic PMC section 4 "grade 2
            # tumors are rare in children".
            aid(named("Grade 2 (G2), or atypical carcinoid", "8249",
                      "ICD-O-3.2 gives Atypical carcinoid tumor as a synonym of this code."),
                AID_G2),
            # Nagtegaal p. 4 "NET, G3 High >20 >20%"; p. 5 "well-differentiated NETs may be high
            # grade". Evidence data gap 4: no grade 3 tumour reported in a child.
            aid(named("Grade 3 (G3), and the report still calls the tumour well differentiated",
                      "8249", "ICD-O-3.2 gives Neuroendocrine tumor, grade 3 as a related term "
                              "of this code.",
                      note="Evidence data gap 4 (the option rests on Pfister 2022's listing of "
                           "appendiceal neuroendocrine tumours)."), AID_G3),
            # Nagtegaal p. 4 "well-differentiated neuroendocrine tumours (NETs)"; Roganovic PMC
            # section 1 (as above).
            named("No grade stated, or carcinoid with no grade", "8240",
                  "ICD-O-3.2 gives Carcinoid tumor, NOS as a synonym of this code.",
                  upgrade="The report does not state the grade. A report that gives grade 2 or "
                          "grade 3 records Neuroendocrine tumor, grade 2 (8249/3): go back and "
                          "take the option that names it."),
            # Nagtegaal p. 4 (as above); p. 5 "NECs are no longer graded".
            go("Neuroendocrine carcinoma (poorly differentiated, small cell or large cell), a "
               "mixed tumour with a neuroendocrine component, or a tumour the report names by "
               "its cell type or hormone, such as an enterochromaffin cell (serotonin-producing) "
               "tumour - type its name to find it", P + "picker",
               note="Evidence dg_net_grade option 5 (to dg_carcinoma_picker), with the Rule K "
                    "cell-type case (departure 8)."),
        ], [],
        "Evidence dg_net_grade (departure 8). ICD-O-3.2: 8240/3 Neuroendocrine tumor, NOS holds "
        "grade 1 as a related term; 8249/3 Neuroendocrine tumor, grade 2 holds grade 3 as a "
        "related term. D1 exception: the code depends on the grade.")


# ------------------------------------------------------------------------------------------
# Benign, borderline and in situ (evidence dg_not_malignant_gut)
# ------------------------------------------------------------------------------------------
def _exclusions(tree_id):
    out = []
    if tree_id == AP:
        # Nagtegaal p. 4 "many tumours of the appendix develop via neoplastic precursor lesions";
        # evidence code currency 8480/1. D6 (departure 7).
        out.append(excl(
            "Low-grade appendiceal mucinous neoplasm, with no invasive carcinoma diagnosed",
            "8480", "1", what="a low-grade appendiceal mucinous neoplasm",
            extra="A report that diagnoses an invasive mucinous adenocarcinoma is answered from "
                  "the carcinoma options: go back and find it under another carcinoma the report "
                  "names.",
            note="Evidence dg_appendix_histology option 2 and dg_not_malignant_gut option 13 "
                 "(merged). D6: no stated-behaviour code."))
    out += [
        # ICCR-St p. 14 image "Adenomatous polyp, low-grade dysplasia 8210/0*".
        excl("Adenomatous polyp, or adenoma with low-grade dysplasia", "8210", "0",
             what="an adenomatous polyp"),
        # Nagtegaal p. 3 "conventional adenomas and serrated precursor lesions".
        excl("Tubular adenoma", "8211", "0", what="a tubular adenoma"),
        # Nagtegaal p. 3 "the recently renamed sessile serrated lesion (formerly called sessile
        # serrated polyp/adenoma)"; icdo32.sqlite 8213/0 Related Sessile serrated polyp.
        excl("Sessile serrated lesion, serrated adenoma or serrated polyp", "8213", "0",
             what="a sessile serrated lesion or serrated adenoma",
             extra="ICD-O-3.2 gives Sessile serrated polyp as a related term of this code."),
    ]
    if tree_id == CR:
        # Nagtegaal p. 6 "Lynch syndrome and familial adenomatous polyposis"; Pfister p. 19
        # "APC-associated polyposis syndromes"; Polat PMC section 3. The evidence entity lists
        # no appendix site.
        out.append(excl(
            "Familial adenomatous polyposis, or multiple adenomatous polyps, with no carcinoma",
            "8220", "0", what="familial adenomatous polyposis with no carcinoma",
            extra="ICD-O-3.2 gives Familial polyposis coli as a synonym of this code. A "
                  "carcinoma arising in it is answered from the carcinoma options."))
    out += [
        # Nagtegaal p. 2 "Use of the term 'carcinoma in situ' is not recommended"; Polat PMC
        # section 2 "revealed adenomatous polyps with high-grade dysplasia".
        excl("High-grade dysplasia, or carcinoma in situ, in a polyp", "8210", "2",
             what="high-grade dysplasia or carcinoma in situ in an adenomatous polyp"),
        # ICCR-Oe p. 12 "Oesophageal glandular dysplasia (intraepithelial neoplasia), low grade
        # 8148/0"; Nagtegaal p. 2 "The term 'dysplasia' is preferred for lesions in the tubal
        # gut".
        excl("Glandular dysplasia or intraepithelial neoplasia, low grade", "8148", "0",
             what="low-grade glandular dysplasia"),
        # ICCR-Oe p. 12 "Oesophageal glandular dysplasia (intraepithelial neoplasia), high grade
        # 8148/2".
        excl("Glandular dysplasia or intraepithelial neoplasia, high grade", "8148", "2",
             what="high-grade glandular dysplasia"),
    ]
    if tree_id == CR:
        out += [
            # ICCR-Oe p. 12 "Oesophageal squamous intraepithelial neoplasia (dysplasia), low
            # grade 8077/0"; Nagtegaal p. 2 "Anal squamous dysplasia". The entity's sites are
            # the oesophagus and the anus.
            excl("Squamous dysplasia or squamous intraepithelial neoplasia, low grade (anus)",
                 "8077", "0", what="low-grade squamous dysplasia of the anus",
                 extra="ICD-O-3.2 gives Anal intraepithelial neoplasia, low grade as a related "
                       "term of this code."),
            # Nagtegaal p. 2 "Anal squamous dysplasia"; evidence code currency 8077/2 (ICCR's
            # 'low grade' label on 8077/2 is a printing error).
            excl("Squamous dysplasia or squamous intraepithelial neoplasia, high grade (anus)",
                 "8077", "2", what="high-grade squamous dysplasia of the anus",
                 extra="ICD-O-3.2 gives Anal intraepithelial neoplasia, grade III as a related "
                       "term of this code."),
        ]
    return out


def not_malignant(tree_id):
    n_ = not_malignant_node(PREFIX[tree_id], _exclusions(tree_id), where=WHERE[tree_id],
                            note="Evidence dg_not_malignant_gut, split by tree (departure 9).")
    # Evidence dg_not_malignant_gut hint, less "or calls the lesion malignant" (D6).
    n_["hint"] += (" A report that states invasion, or diagnoses an invasive carcinoma arising in "
                   "the lesion, is answered from the carcinoma options: go back to the step "
                   "before.")
    return n_


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str) -> dict:
    assert tree_id in PREFIX, tree_id
    P = PREFIX[tree_id]
    histology = colorectal_histology() if tree_id == CR else appendix_histology()
    nodes = _gate(tree_id) + [histology, net_grade(tree_id), not_malignant(tree_id),
                              deposit_node(P, where=WHERE[tree_id])]
    return make_tree(tree_id, nodes, subtype_screens=(P + "net_grade",))


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the trees emit outside their
# pickers. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8480/3": ("D1, D8", EVIDENCE,
               "Mucinous adenocarcinoma, the commonest type of colorectal carcinoma in children "
               "(Polat 2021, Mahajan 2022), on the colorectal histology screen, and at basis 5 "
               "when cytology names it."),
    "8490/3": ("D1, D8", EVIDENCE,
               "Signet ring cell carcinoma of the colon or rectum, reported in children (Mahajan "
               "2022), on the colorectal histology screen, and at basis 5 when cytology names "
               "it."),
    "8140/3": ("D1, D8", EVIDENCE,
               "Adenocarcinoma with no subtype named: a paediatric option on the colorectal "
               "histology screen (Polat 2021, Mahajan 2022), the generic adenocarcinoma option of "
               "the appendix screen (contract §4.2), and at basis 5 when cytology names it."),
    "8220/3": ("D1", EVIDENCE,
               "Adenocarcinoma arising in familial adenomatous polyposis on the colorectal "
               "histology screen (Mahajan 2022, Polat 2021)."),
    "8211/3": ("D1", EVIDENCE,
               "Tubular adenocarcinoma on the colorectal histology screen; the one paediatric "
               "report gives it as a component of a mucinous adenocarcinoma (Polat 2021; "
               "evidence data gap 8)."),
    "8240/3": ("D1, D7, D8", EVIDENCE,
               "Neuroendocrine tumour of grade 1 or with no grade stated on the colorectal and "
               "appendiceal grade screens (appendiceal neuroendocrine tumours: Pfister 2022 Table "
               "3, Roganovic 2026; the colorectal option is the D1 exception for a code that "
               "needs the grade), at basis 5 when cytology names a neuroendocrine tumour, and at "
               "basis 4 with imaging and a raised serum chromogranin A (Visser 2023 Table 4)."),
    "8249/3": ("D1", EVIDENCE,
               "Neuroendocrine tumour of grade 2, or of grade 3 that the report calls well "
               "differentiated, on the colorectal and appendiceal grade screens; ICD-O-3.2 holds "
               "grade 3 as a related term at 8249/3."),
    "8241/3": ("D2, D7", EVIDENCE,
               "Enterochromaffin cell carcinoid at basis 4 with imaging of a tumour of the colon, "
               "rectum, anus or appendix and a raised serum serotonin (Visser 2023 Table 4, "
               "functioning neuroendocrine tumours), and in the colorectal and appendix pickers "
               "(registrar question 7)."),
    "8243/3": ("D3", EVIDENCE,
               "Goblet cell adenocarcinoma of the appendix (Nagtegaal 2020, the WHO 5th edition "
               "name) records 8243/3 Goblet cell carcinoid, never the obsolete 8245/3; an option "
               "on the appendix histology screen because ICD-O-3.2 holds no term under the WHO "
               "name, and a picker entry in the colorectal tree."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma whose type the report does not name: the generic option of the "
               "colorectal and appendix histology screens (contract §4.2), and at basis 5 when "
               "cytology names a carcinoma without its type."),
}
