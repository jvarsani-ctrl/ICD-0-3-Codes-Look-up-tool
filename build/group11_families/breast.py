"""g11_breast (prefix br_): carcinomas of the breast at C50.0-C50.9, ICCC-3 subgroup XIf6.

A family tree (contract §4.1) with one organ. It is built from
docs/group_11_evidence/XIf6_breast.json (the evidence agent's nodes br_document_inventory,
br_clinical, br_imaging, br_cytology, br_site, br_histology, br_fibroepithelial, br_not_malignant
and br_carcinoma_picker; the part has no ihc_rules and no lab_tests) with the builders in
build/group11_common.py, in the shape of build/group11_organs/thyroid.py. Every option's label,
code, behaviour, basis, reason and recognition aid comes from that file; the cite (file, PDF page,
quotation) is the comment above the option or the aid. File names in the comments are the
evidence's own:
    Tan       XIf6-breast__Tan-2020.txt (Tan PH, et al. The 2019 World Health Organization
              classification of tumours of the breast. Histopathology 2020;77:181-185)
    ICCR      XIf6-breast__ICCR-Invasive-Breast-2nd.txt (ICCR Invasive Carcinoma of the Breast,
              2nd edition, version 2.1, June 2022). "image" marks a quotation read from the page
              image of the WHO table (PDF pp. 13-14).
    Sosnowska XIf6-breast-paediatric__Sosnowska-Sienkiewicz-2024.txt (Front Pediatr
              2024;12:1417050); PubMed Central section numbers stand for pages
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser    Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
              set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    br_document_inventory  document_inventory  evidence gate (evidence br_document_inventory)
    br_clinical, br_clinical_cytology  clinical_alias  (evidence br_clinical)
    br_imaging, br_imaging_cytology    morphology_only (evidence br_imaging)
    br_cytology            morphology_only     (evidence br_cytology)
    br_histology           histology_subclassification  (evidence br_histology)
    br_fibroepithelial     histology_subclassification  (evidence br_fibroepithelial)
    br_papillary           histology_subclassification  (built from evidence br_carcinoma_picker
                                                         and br_not_malignant: departure 7)
    br_not_malignant       histology_subclassification  (evidence br_not_malignant)
    br_deposit             morphology_only      (D10)
    br_picker              histology_subclassification  (D2; evidence br_carcinoma_picker)

Departures from the evidence nodes, and why
-------------------------------------------
1. br_document_inventory: the gate's options are the contract §4.2 tiers (D7); the histology tier
   goes to br_histology, not br_site (departure 3). The gate has no laboratory copy and no marker
   tier: the evidence gives no laboratory test, and its tissue_free row 5 declines the Visser
   Table 4 chromogranin A route at the breast (Tan p. 3 "it is prudent to exclude metastasis from
   another site"). The gate becomes a document checklist through
   docs/evidence_documents/group_11.json. The hint carries the evidence's histology sentences and
   the site rules of the dropped br_site (departure 3).
2. br_clinical: "The note names melanoma of the skin of the breast" hopped to the melanoma tree. A
   melanoma of the skin of the breast is at C44.5, a site the skin tree routes, and validator
   rule 2 lets basis 1 record 8720/3 on a skin tree only. The option is not built; br_clinical's
   hint (and the gate's) sends the clerk to the site step for C44.5. "An imaging report is in the
   file after all" (br_clinical) and "A histology report is in the file after all" (br_imaging)
   are not built: the document checklist decides the tier (group11_common, departures from
   Group 10). The 8000/3 lines are the common screens' Group XII referrals (D7).
3. br_site is not built. The router's site step chooses this tree from C50.0-C50.9 and records the
   part of the breast, so the question is one the router already answers (D14). Its Rule A, B and
   C content (clock-face position C50.9; one tumour over two or more parts C50.8; periareolar
   carcinoma is a breast tumour) and its "Skin of the breast" line (C44.5, the skin tree) move to
   the hints of br_document_inventory and br_histology.
4. br_cytology: "Cytology names a carcinoma, with or without a type" (8010/3, basis 5) is kept
   (ICCR p. 12 "cannot be determined with certainty on a limited core biopsy sample"), with an
   upgrade line. "Cytology names melanoma" hopped to the melanoma tree, whose screens are
   histology screens (basis 7); D8 records Malignant melanoma, NOS (8720/3) at basis 5 instead,
   with a reason that sends a melanoma that began elsewhere to its primary site. The lymphoma,
   sarcoma and fibroepithelial lines are kept. "Malignant cells, no type" (Group XII, 8001) and the
   non-diagnostic routes are the common ones; the common suspicious line is added.
5. br_histology: the six carcinomas the 8 October ruling put on the screen keep the evidence's
   order (Sosnowska section 72). D2 holds their codes off the picker (data gap 6), so the evidence's
   gateway "An invasive carcinoma of a named type" is the common picker option, and the
   microinvasion answer on br_not_malignant returns to br_histology instead of the picker.
6. br_histology: the trailing options are the common ones (tail_options): melanoma (D13, me_mucosa,
   as the thyroid's: the breast is none of skin, eye or central nervous system; T2c to confirm the
   screen takes a melanoma of an internal organ), the picker, the exclusion screen, the deposit
   question (D10; the evidence's deposit referral with recapture), "Malignant tumour, type not
   determined" (Group XII, 8000, D7), and the referrals lymphoma (II, keeps the breast, Rule D),
   leukaemia (I, C42.1), sarcoma (IX), teratoma or another germ cell tumour (X; ICCC-2017 places
   9080 and 9100 at C50 in Group X, evidence conflicts row 6) and another named tumour (XII). The
   evidence's myoepithelial carcinoma or malignant mixed tumour referral (XII) follows them. The
   evidence's "or myeloid sarcoma" is not on the leukaemia line: refer_leukaemia records C42.1,
   and check_leukaemia_referrals_record_marrow admits a site-keeping Group I referral only on the
   nodes it lists (group11_common refer_leukaemia). NUT carcinoma has no option: D12 does not name
   the breast, so 8023/3 is a picker entry.
7. br_papillary is new. The evidence put Encapsulated papillary carcinoma with invasion (8504/3),
   Solid papillary carcinoma with invasion (8509/3), tall cell carcinoma with reversed polarity
   (8509/3) and Intraductal papillary adenocarcinoma with invasion (8503/3) in the picker, and the
   in situ forms 8504/2 and 8509/2 on br_not_malignant. D1's exception applies: each code depends
   on whether the report describes invasion, which the picker cannot ask. The screen pairs each
   invasive code with its in situ exclusion; 8503/2 is the papillary pattern of ductal carcinoma
   in situ the evidence names (entity 8500/2). The picker also cannot find tall cell carcinoma
   with reversed polarity by name, because ICD-O-3.2 prints no term for it (registrar question 3).
   8504/2 and 8509/2 stay on br_not_malignant as well.
8. br_not_malignant: the common exclusion screen. "Paget disease of the nipple, which the report
   calls in situ" and "Juvenile papillomatosis" are non-reportable lines, not exclusions: ICD-O-3.2
   prints no term at 8540/2, and none for juvenile papillomatosis. Tubular adenoma (8211/0) is
   added from the evidence's exclusion entity (data gap 8), so a report of it does not reach
   Tubular adenocarcinoma (8211/3) in the picker. The evidence's catch-all is the common one.
9. br_carcinoma_picker: D2 replaces the evidence's curated picker. Labels are ICD-O-3.2 Preferred
   terms and search_terms the live synonyms and related terms, so the evidence's own labels
   ("Tall cell carcinoma with reversed polarity") and search terms not printed by ICD-O-3.2
   ("Invasive papillary carcinoma") are not carried; the first is on br_papillary. The evidence
   picker's hint sentences on Rules J and K and on organ-named carcinomas are appended to the
   common hint (PICKER_HINT_EXTRA).
10. Not built from the evidence: 8508/3 and 8512/3 (D3; data gap 3, registrar question 2), the
   chromogranin A marker route (departure 1), and a Rule K code for the WHO special patterns of
   no special type (registrar question 2; D5).

Registrar questions the evidence raised (XIf6_breast.json registrar_questions 2 to 5) stay open;
questions 1 and 6 were answered by the 8 October 2026 ruling and the paediatric source. The
defaults above apply until the others are answered (docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

from group11_common import (OUTSIDE_XI, TYPE_NOT_STATED, aid, cyto, deposit_node,
                            evidence_gate, excl, go, make_tree, named, node, nonrep,
                            not_malignant_node, refer, refer_germ_cell, refer_leukaemia,
                            refer_lymphoma, refer_other_named, refer_sarcoma, tail_options)

TREE_ID = "g11_breast"
P = "br_"
WHERE = "the breast"
EVIDENCE = "XIf6_breast"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Shared clerk-facing sentences (the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Evidence br_site option 10 and rules_a_to_k A: "A tumour of the skin of the breast is coded
# from the skin tree, at skin of trunk (C44.5); the breast (C50) does not include its skin."
# Rules p. 1 "If the diagnosis does not specify the tissue of origin".
SKIN_OF_BREAST = ("A tumour of the skin of the breast is a skin tumour, recorded at the skin of "
                  "the trunk (C44.5): go back to the site step and record C44.5.")
# Evidence br_site hint; Rules p. 5 "when a single tumor overlaps the boundaries of two or more";
# ICCR p. 8 "Clock face delineation of location is a more"; rules_a_to_k B (periareolar).
SITE_RULES = ("The site step records the part of the breast the report names. A report that "
              "gives only a clock-face position is recorded at breast, part not stated (C50.9). "
              "One tumour that crosses two or more parts, with no stated origin, is recorded at "
              "overlapping lesion of breast (C50.8). A periareolar or retroareolar carcinoma is a "
              "breast tumour.")
# Evidence br_not_malignant hint; ICCR p. 7 "microinvasive carcinoma (≤1 millimetres (mm))".
MICROINVASION = ("An in situ carcinoma with microinvasion (invasion of 1 mm or less) is an "
                 "invasive carcinoma: choose the invasive type the report names.")

# Evidence br_carcinoma_picker hint. Rules p. 3 "Change the order of word roots in a compound
# term" (Rule J) and "use the numerically higher code number" (Rule K); ICCR p. 12 "mixed IBC-NST
# and invasive lobular carcinoma"; Rules p. 10 "may be used when the topographic site is not
# given in the diagnosis" (Rule H). Registrar question 5 (metaplastic subtypes).
PICKER_HINT_EXTRA = (
    " If a compound name is not found, search for its parts in the other order (WHO coding Rule "
    "J). A carcinoma of no special type mixed with lobular carcinoma is Infiltrating duct and "
    "lobular carcinoma (8522/3); mixed with another special type it is Infiltrating duct mixed "
    "with other types of carcinoma (8523/3). When one tumour carries two type names and no "
    "single option names both, choose the higher code number (WHO coding Rule K): a metaplastic "
    "squamous cell carcinoma is recorded as Metaplastic carcinoma, NOS (8575/3). A name that "
    "places the tumour in another organ, such as the lung, pancreas, thymus or ovary, means a "
    "deposit unless the report says the tumour began in the breast: go back and choose the "
    "deposit answer.")


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Sosnowska section 72 "The most common subtype of invasive breast cancer in children is invasive
# secretory carcinoma (ISC)".
AID_SECRETORY = "The report may call it invasive secretory carcinoma (ISC)."
# Tan p. 4 "its presence alone should not warrant a malignant grade in phyllodes tumours"; Tan
# p. 4 "Periductal stromal tumour is now considered to be a variant of phyllodes tumour".
AID_MALIGNANT_PHYLLODES = ("The report itself calls the phyllodes tumour malignant; a "
                           "well-differentiated liposarcoma-like component on its own does not "
                           "make it malignant.")
# Tan p. 2 "Breast tumour resembling the tall cell variant of papillary thyroid carcinoma; solid
# papillary carcinoma with reverse polarity" and "Now grouped as tall cell carcinoma with reversed
# polarity" (the evidence's search_terms for this entity).
AID_TCCRP = ("Older reports call it a breast tumour resembling the tall cell variant of papillary "
             "thyroid carcinoma, or solid papillary carcinoma with reverse polarity.")
# Evidence br_histology sarcoma option; ICCR p. 14 image "Metaplastic carcinoma with mesenchymal
# differentiation (chondroid, osseous, other types of mesenchymal differentiation)".
AID_SARCOMA = ("A report that calls the tumour metaplastic carcinoma, even with chondroid or "
               "osseous differentiation, names a carcinoma, and a phyllodes tumour is answered "
               "under fibroadenoma or phyllodes tumour.")
# Evidence br_histology myoepithelial option; ICCR p. 13 image "Spindle cell carcinoma/myoepithelial
# carcinoma".
AID_MYOEPITHELIAL = ("A report that names metaplastic carcinoma with a spindle cell or "
                     "myoepithelial pattern names a carcinoma: choose another carcinoma the "
                     "report names.")
# Evidence br_histology deposit option; Tan p. 3 "it is prudent to exclude metastasis from another
# site"; Sosnowska section 67 (metastatic disease in the breast is commoner than a primary breast
# neoplasm in children; data gap 9).
AID_DEPOSIT = ("The report calls the tumour metastatic, or names a tumour of another organ, such "
               "as a neuroendocrine tumour shown to come from elsewhere.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence br_document_inventory, br_clinical, br_imaging, br_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    # Evidence br_cytology options 3 and 4. Rules p. 2 "extranodal lymphomas to the site of
    # origin" (Rule D).
    lymphoma_cyto = refer_lymphoma(WHERE)
    lymphoma_cyto["label"] = "Cytology names a lymphoma"
    sarcoma_cyto = refer_sarcoma(WHERE, label="Cytology names a sarcoma")
    # Evidence br_cytology option 1; ICCR p. 12 "cannot be determined with certainty on a limited
    # core biopsy sample" (tissue_free row 4: family-level code only).
    carcinoma_cyto = cyto("Cytology names a carcinoma, with or without naming its type", "8010",
                          "The type of a breast carcinoma is not settled on a limited sample, so "
                          "a type the cytology report names does not change the code.",
                          note="Evidence br_cytology option 1 and tissue_free row 4.")
    carcinoma_cyto["upgrade_path"] = ("A histology report gives the carcinoma's type and that "
                                      "type's own code.")
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this breast tumour?",
        # Evidence br_document_inventory hint, with the br_site content (departure 3).
        hint=("A radiology report counts as imaging. A core needle biopsy, excision or "
              "mastectomy report counts as histology; an immunohistochemistry or gene report on "
              "its own does not stand in for one. A biopsy or cytology report that calls the "
              "specimen inadequate or non-diagnostic counts as no tissue. %s %s A report that "
              "calls the tumour possible or suspected does not register it."
              % (SITE_RULES, SKIN_OF_BREAST)),
        tier_labels={
            # Evidence br_document_inventory option 2; ICCR p. 9 "magnetic resonance imaging
            # (MRI), ultrasound, mammographic".
            "imaging": "An imaging report only (mammogram, ultrasound or magnetic resonance "
                       "imaging) - no tissue",
            # Evidence option 3; Tan p. 1 "needle aspiration considerations".
            "cytology": "A cytology report (a fine-needle aspirate or a smear) - no histology "
                        "report",
            # Evidence option 4; Tan p. 1 "Core biopsy diagnosis, an important preoperative
            # tool"; ICCR p. 8 "Partial mastectomy, lumpectomy and quadrantectomy/segmental
            # excision".
            "histology": "A histology report (core needle biopsy, excision or mastectomy), with "
                         "or without immunohistochemistry or gene reports",
        },
        cytology=[
            carcinoma_cyto,
            # Evidence br_cytology option 2 (departure 4). D8: cytology naming an entity records
            # it at basis 5. ICCC-2017 range 123 places 8720/3 in XId at every site.
            cyto("Cytology names a melanoma", "8720",
                 "A melanoma that began elsewhere, such as the skin, is coded at that primary "
                 "site: go back to the site step and record it.",
                 note="Evidence br_cytology option 2 (departure 4): D8 in place of the hop to the "
                      "melanoma tree, whose screens record basis 7."),
            lymphoma_cyto,
            sarcoma_cyto,
            # Evidence br_cytology option 5; Tan p. 3 "as a histological criterion of
            # malignancy".
            nonrep("Cytology names a fibroadenoma, a phyllodes tumour or another fibroepithelial "
                   "lesion",
                   "Not registrable. Whether a phyllodes tumour is malignant is decided on "
                   "histology, so the case is not registered from this report.",
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "cytology_fibroepithelial"},
                   note="Evidence br_cytology option 5."),
        ],
        note="Evidence br_document_inventory, br_clinical, br_imaging and br_cytology "
             "(departures 1 to 4 in the module docstring).")
    # Departure 2: a clinical note naming a melanoma of the skin of the breast belongs to the skin
    # tree at C44.5, which registers it on clinical information (Visser Table 3).
    for nd in nodes:
        if nd["node_id"] in (n("clinical"), n("clinical_cytology")):
            nd["hint"] += (" A melanoma of the skin of the breast is a skin tumour: go back to the "
                           "site step and record the skin of the trunk (C44.5).")
    return nodes


# ------------------------------------------------------------------------------------------
# Histology (evidence br_histology)
# ------------------------------------------------------------------------------------------
def histology():
    myoepithelial = aid(refer(
        "Myoepithelial carcinoma or malignant mixed tumour, named on its own", 12,
        "ICCC-3 places Myoepithelial carcinoma (8982/3) and Mixed tumor, malignant, NOS (8940/3) "
        "in Group XII at every site, so the case is coded from the Group XII (other and "
        "unspecified malignant neoplasms) tree.",
        note="Evidence br_histology; conflicts row 2; registrar question 5. ICCC-2017 places "
             "8982/3 and 8940/3 in XIIa4 at C50."), AID_MYOEPITHELIAL)
    lymphoma = refer_lymphoma(WHERE)
    # Evidence br_histology lymphoma option; conflicts row 4 (9715/3, Group II).
    lymphoma["label"] = ("Lymphoma, including breast implant-associated anaplastic large cell "
                         "lymphoma")
    tail = tail_options(
        P, "mucosa", where=WHERE,
        # Evidence br_histology; Rules p. 2 "code as the pathologist indicates" (Rule F).
        not_malignant_label="A tumour the report calls benign, in situ or of uncertain malignant "
                            "potential, for example ductal carcinoma in situ",
        referrals=[
            lymphoma,
            # Rules p. 2 "Code all leukemias except myeloid sarcoma" (departure 6).
            refer_leukaemia(WHERE),
            # Evidence br_histology sarcoma option; conflicts row 3 (8800, 9120 in Group IX).
            aid(refer_sarcoma(WHERE, label="A sarcoma or another malignant soft tissue tumour"),
                AID_SARCOMA),
            # ICCC-2017: 9080 and 9100 at C50 in Group X (evidence conflicts row 6).
            refer_germ_cell(WHERE),
            refer_other_named(),
        ],
        extra_referrals=[myoepithelial])
    for o in tail:
        if o.get("next_node") == n("deposit"):
            aid(o, AID_DEPOSIT)
    opts = [
        # Sosnowska section 72 "The most common subtype of invasive breast cancer in children is
        # invasive secretory carcinoma"; ICCR p. 14 image "Secretory carcinoma 8502/3". D1.
        aid(named("Secretory carcinoma (also called juvenile carcinoma)", "8502",
                  "ICD-O-3.2 gives Juvenile carcinoma of breast as a related term of this code.",
                  note="D1: Sosnowska-Sienkiewicz 2024, section 72 (common in children)."),
            AID_SECRETORY),
        # Sosnowska section 72 "subtypes of breast cancer in children (invasive ductal, invasive
        # lobular, medullary, inflammatory, and anaplastic carcinomas)"; Sosnowska section 76
        # "Invasive ductal carcinoma Lump, typically small circumscribed painless palpable masses";
        # ICCR p. 13 image "Invasive breast carcinoma of no special type (see 'a' below) 8500/3".
        named("Invasive ductal carcinoma, or invasive carcinoma of no special type", "8500",
              "ICD-O-3.2 gives Invasive breast carcinoma of no special type as a synonym of this "
              "code.",
              note="D1: Sosnowska-Sienkiewicz 2024, sections 72 and 76. Registrar question 2 "
                   "(special patterns of no special type)."),
        # Sosnowska section 72 (as above); ICCR p. 13 image "Invasive lobular carcinoma (see 'b'
        # below) 8520/3".
        named("Invasive lobular carcinoma", "8520",
              "ICD-O-3.2 gives Infiltrating lobular carcinoma, NOS as a synonym of this code.",
              note="D1: Sosnowska-Sienkiewicz 2024, section 72."),
        # Sosnowska section 72 (as above); Tan p. 2 "with a medullary pattern as representing one
        # end of the spectrum".
        named("Medullary carcinoma", "8510",
              note="D1: Sosnowska-Sienkiewicz 2024, section 72. Registrar question 2: a report "
                   "of no special type with a medullary pattern is not this option until the "
                   "registrar rules."),
        # Sosnowska section 72 (as above); Tan p. 2 "distinct clinical presentations rather than
        # special subtypes".
        named("Inflammatory carcinoma", "8530",
              note="D1: Sosnowska-Sienkiewicz 2024, section 72. Registrar question 2."),
        # Sosnowska section 72 (as above).
        named("Anaplastic carcinoma", "8021",
              note="D1: Sosnowska-Sienkiewicz 2024, section 72."),
        # Pfister p. 13 "Breast tumors", "Fibroepithelial tumors"; Sosnowska section 2 (malignant
        # phyllodes tumour among the malignant breast lesions of children and adolescents).
        go("Fibroadenoma or phyllodes tumour", n("fibroepithelial"),
           note="D1: malignant phyllodes tumour, Sosnowska-Sienkiewicz 2024, sections 2 and 76; "
                "juvenile fibroadenoma, Pfister 2022 Table 3, p. 13."),
        # Departure 7. D1 exception: the code depends on invasion.
        go("Papillary carcinoma: encapsulated (intracystic), solid or intraductal papillary "
           "carcinoma, invasive papillary carcinoma, or tall cell carcinoma with reversed "
           "polarity", n("papillary"),
           note="D1 exception (invasion screen); moved from the evidence's picker "
                "(departure 7)."),
        # Evidence br_histology "Carcinoma, with no type named".
        named("Carcinoma, with no type named", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence br_histology; the generic option of the screen (data gap 7)."),
    ] + tail
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence br_histology hint; Rules p. 2 "code as the pathologist indicates" (Rule F).
        "Use the report's own term. When a core needle biopsy and a later excision both name a "
        "type, use the excision report. If the report states that the tumour is benign, in situ "
        "or of uncertain malignant potential, choose that answer, even for a tumour type that is "
        "usually malignant. %s %s" % (MICROINVASION, SKIN_OF_BREAST),
        opts, [],
        "Evidence br_histology (departures 5 to 7). D1: the paediatric entities are secretory "
        "carcinoma (common) and invasive ductal, invasive lobular, medullary, inflammatory and "
        "anaplastic carcinoma (Sosnowska-Sienkiewicz 2024, section 72; registrar, 8 October "
        "2026), and malignant phyllodes tumour (sections 2 and 76) on the fibroepithelial "
        "screen; the papillary carcinomas are options because their codes need the invasion "
        "answer.")


def fibroepithelial():
    return node(
        n("fibroepithelial"), "histology_subclassification", 4, "Fibroadenoma or phyllodes tumour",
        "Which fibroadenoma or phyllodes tumour does the report name?",
        # Evidence br_fibroepithelial hint; icdo32.sqlite 9020/1 Synonym Phyllodes tumor, NOS.
        "Choose the grade the report states: benign, borderline or malignant. A phyllodes tumour "
        "reported with no grade is answered as borderline.",
        [
            # Pfister p. 13 "Juvenile fibroadenoma".
            excl("Juvenile fibroadenoma", "9030", "0", what="a juvenile fibroadenoma"),
            excl("Giant fibroadenoma", "9016", "0", what="a giant fibroadenoma"),
            # Sosnowska section 12 "Fibroadenomas are the most common (95% of all breast lesions)
            # benign breast tumors in adolescents".
            excl("Fibroadenoma of any other kind", "9010", "0", what="a fibroadenoma"),
            # Sosnowska section 77 "The most common histopathologic diagnoses are fibroadenoma and
            # benign phyllodes tumor".
            excl("Phyllodes tumour, benign", "9020", "0", what="a benign phyllodes tumour"),
            # Tan p. 3 "as a histological criterion of malignancy".
            excl("Phyllodes tumour, borderline - or with no grade stated", "9020", "1",
                 what="a borderline phyllodes tumour",
                 extra="ICD-O-3.2 gives Phyllodes tumor, NOS as a synonym of this code, so a "
                       "phyllodes tumour reported with no grade is not malignant."),
            # Tan p. 4 "Periductal stromal tumour is now considered to be a variant of phyllodes
            # tumour"; Sosnowska section 76 "Malignant lesions Phyllodes tumor (malignant)".
            aid(named("Phyllodes tumour, malignant - or periductal stromal tumour", "9020",
                      "ICD-O-3.2 gives Periductal stromal tumor, low grade as a related term of "
                      "this code.",
                      note="D1: Sosnowska-Sienkiewicz 2024, sections 2 and 76. ICCC-2017 places "
                           "9020/3 at C50 in XIf6 (registrar question 6, answered 8 October "
                           "2026)."),
                AID_MALIGNANT_PHYLLODES),
        ], [],
        "Evidence br_fibroepithelial, in the evidence's order (data gap 10: the residual "
        "fibroadenoma answer follows the named variants). Only the malignant grade is a Group XI "
        "code.")


def papillary():
    return node(
        n("papillary"), "histology_subclassification", 4, "Papillary carcinoma",
        "Which papillary carcinoma does the report name, and does it describe invasion?",
        "Choose the type the report names and whether the report describes invasion. "
        "Microinvasion (invasion of 1 mm or less) counts as invasion. A report that names "
        "papillary carcinoma with no further type is found under another carcinoma the report "
        "names; an intraductal papilloma is answered under a tumour the report calls benign.",
        [
            # icdo32.sqlite 8504/3 Preferred Encapsulated papillary carcinoma with invasion;
            # currency check §3 (8504 /3 to /2). Evidence picker option and code_currency 8504.
            named("Encapsulated (intracystic) papillary carcinoma, with invasion", "8504",
                  "ICD-O-3.2 gives Intracystic papillary carcinoma with invasion as a synonym of "
                  "this code.",
                  note="D1 exception. Currency check §3: 8504/3 is Encapsulated papillary "
                       "carcinoma with invasion."),
            # Evidence br_not_malignant option 5; code_currency 8504.
            excl("Encapsulated (intracystic) papillary carcinoma, with no invasion", "8504", "2",
                 what="an encapsulated papillary carcinoma with no invasion",
                 extra="ICD-O-3.2 moved Intracystic carcinoma, NOS from behaviour 3 to behaviour "
                       "2; only the tumour with invasion, Encapsulated papillary carcinoma with "
                       "invasion (8504/3), is malignant.",
                 note="Currency check §3."),
            # ICCR p. 14 image "Solid papillary carcinoma - invasive 8509/3".
            named("Solid papillary carcinoma, with invasion", "8509",
                  note="D1 exception. Currency check §6: 8509 is new in ICD-O-3.2 and absent "
                       "from REDCap (the REDCap-side list, standing rule 16)."),
            # Tan p. 3 "solid papillary carcinoma of both in-situ and invasive types".
            excl("Solid papillary carcinoma in situ, with no invasion", "8509", "2",
                 what="a solid papillary carcinoma in situ"),
            # ICCR p. 14 image "Tall cell carcinoma with reversed polarity 8509/3"; Tan p. 2 "Now
            # grouped as tall cell carcinoma with reversed polarity"; Tan p. 4 "is introduced in
            # the section about rare and salivary gland-type tumours". Registrar question 3.
            aid(named("Tall cell carcinoma with reversed polarity", "8509",
                      "The WHO classification of breast tumours codes tall cell carcinoma with "
                      "reversed polarity 8509/3, and ICD-O-3.2 prints no term for it. This awaits "
                      "the registrar's decision.",
                      note="Registrar question 3 (evidence code_currency 8509)."),
                AID_TCCRP),
            # ICCR p. 14 image "Invasive papillary carcinoma 8503/3".
            named("Invasive papillary carcinoma, or intraductal papillary carcinoma with "
                  "invasion", "8503",
                  "ICD-O-3.2 gives Papillary carcinoma of breast as a related term of this code.",
                  note="D1 exception."),
            # Evidence entity 8500/2: "Its patterns carry their own /2 codes (cribriform 8201/2,
            # papillary 8503/2, micropapillary 8507/2)"; ICCR p. 7 "with or without ductal
            # carcinoma in situ (DCIS)".
            excl("Intraductal papillary carcinoma, or papillary ductal carcinoma in situ, with no "
                 "invasion", "8503", "2",
                 what="an intraductal papillary carcinoma with no invasion",
                 extra="ICD-O-3.2 gives Ductal carcinoma in situ, papillary as a synonym of this "
                       "code."),
        ], [],
        "Departure 7: built from the evidence's picker options 8504/3, 8509/3 (two) and 8503/3 "
        "and its br_not_malignant exclusions 8504/2 and 8509/2, with 8503/2 from entity 8500/2. "
        "D1 exception: each code depends on the invasion answer.")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # Evidence br_not_malignant option 1; ICCR p. 7 "microinvasive carcinoma (≤1
            # millimetres (mm))". Departure 5: returns to br_histology.
            go("In situ carcinoma with microinvasion - invasion of 1 mm or less", n("histology"),
               note="Evidence br_not_malignant option 1 routed to the picker; D2 holds the six "
                    "histology-screen carcinomas off the picker, so the option returns to "
                    "br_histology (departure 5; data gap 6)."),
            # ICCR p. 7 "DCIS without invasive carcinoma and microinvasive carcinoma".
            excl("Ductal carcinoma in situ, of any pattern or grade", "8500", "2",
                 what="ductal carcinoma in situ",
                 extra="Its patterns carry their own behaviour 2 codes."),
            # Tan p. 2 "As well as classic lobular carcinoma in situ (LCIS)".
            excl("Lobular carcinoma in situ, classic or florid", "8520", "2",
                 what="lobular carcinoma in situ"),
            # Tan p. 2 "Pleomorphic LCIS shows marked nuclear".
            excl("Lobular carcinoma in situ, pleomorphic", "8519", "2",
                 what="pleomorphic lobular carcinoma in situ"),
            # Code currency 8504; currency check §3.
            excl("Encapsulated papillary carcinoma or intracystic papillary carcinoma, with no "
                 "invasion", "8504", "2",
                 what="an encapsulated papillary carcinoma with no invasion"),
            # Tan p. 3 "solid papillary carcinoma of both in-situ and invasive types".
            excl("Solid papillary carcinoma in situ", "8509", "2",
                 what="a solid papillary carcinoma in situ"),
            # Rules p. 8 "in the absence of a demonstrable tumor, it should be considered"; Rules
            # p. 2 "code as the pathologist indicates" (Rule F). Departure 8: no 8540/2 term.
            nonrep("Paget disease of the nipple, which the report calls in situ",
                   "Not registrable. A behaviour the pathologist states is recorded as stated "
                   "(WHO coding Rule F), and in situ is behaviour 2. ICD-O-3.2 codes Paget "
                   "disease, mammary as 8540/3 and prints no in situ term on that number. %s"
                   % OUTSIDE_XI,
                   note="Evidence br_not_malignant option 7 (exclusion 8540/2), built as a "
                        "non-reportable line because ICD-O-3.2 prints no term at 8540/2 "
                        "(departure 8)."),
            # Pfister p. 13 "Juvenile papillomatosis"; Sosnowska section 33 "Juvenile
            # papillomatosis is a benign condition but is associated with carcinoma".
            nonrep("Juvenile papillomatosis",
                   "Not registrable. Juvenile papillomatosis is a benign breast lesion, and "
                   "ICD-O-3.2 prints no term for it. %s" % OUTSIDE_XI,
                   note="Evidence br_not_malignant option 8: a code-less exclusion. Intraductal "
                        "papillomatosis, NOS (8505/0) is a different entity and is not used for "
                        "it (evidence entity; data gap 4)."),
            # Sosnowska section 25 "they can also occur in children, although very rarely".
            excl("Intraductal papilloma", "8503", "0", what="an intraductal papilloma"),
            excl("Intraductal papillomatosis", "8505", "0", what="intraductal papillomatosis"),
            excl("Adenoma of the nipple", "8506", "0", what="an adenoma of the nipple"),
            excl("Lactating adenoma", "8204", "0", what="a lactating adenoma"),
            # Sosnowska section 2 "juvenile papillomatosis, fibrous nodules, tubular adenoma,
            # hamartoma, cysts, fibrocystic lesions or". Departure 8; data gap 8.
            excl("Tubular adenoma", "8211", "0", what="a tubular adenoma",
                 extra="Tubular adenocarcinoma, the malignant code on the same number, is a "
                       "different tumour.",
                 note="Evidence exclusion entity 8211/0 (data gap 8)."),
            excl("Adenomyoepithelioma, not called malignant", "8983", "0",
                 what="an adenomyoepithelioma"),
        ],
        where=WHERE,
        note="Evidence br_not_malignant (departures 5 and 8). The fibroadenoma and phyllodes "
             "exclusions are on br_fibroepithelial.")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), fibroepithelial(), papillary(), not_malignant(),
                      deposit_node(P, where=WHERE)]
    tree = make_tree(TREE_ID, nodes, subtype_screens=(n("fibroepithelial"), n("papillary")))
    for nd in tree["nodes"]:
        if nd["node_id"] == n("picker"):
            nd["hint"] += PICKER_HINT_EXTRA
    return tree


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8502/3": ("D1", EVIDENCE,
               "Secretory carcinoma, the commonest invasive breast cancer in children "
               "(Sosnowska-Sienkiewicz 2024, section 72), first on the breast histology screen; "
               "ICD-O-3.2 gives Juvenile carcinoma of breast as a related term."),
    "8500/3": ("D1", EVIDENCE,
               "Invasive ductal carcinoma or invasive breast carcinoma of no special type on the "
               "breast histology screen (Sosnowska-Sienkiewicz 2024, sections 72 and 76; "
               "registrar question 2 on the special patterns)."),
    "8520/3": ("D1", EVIDENCE,
               "Invasive lobular carcinoma on the breast histology screen (Sosnowska-Sienkiewicz "
               "2024, section 72)."),
    "8510/3": ("D1", EVIDENCE,
               "Medullary carcinoma on the breast histology screen (Sosnowska-Sienkiewicz 2024, "
               "section 72); the WHO 2019 medullary pattern of no special type waits on "
               "registrar question 2."),
    "8530/3": ("D1", EVIDENCE,
               "Inflammatory carcinoma on the breast histology screen (Sosnowska-Sienkiewicz "
               "2024, section 72; registrar question 2)."),
    "8021/3": ("D1", EVIDENCE,
               "Anaplastic carcinoma on the breast histology screen (Sosnowska-Sienkiewicz 2024, "
               "section 72)."),
    "9020/3": ("D1", EVIDENCE,
               "Malignant phyllodes tumour, including periductal stromal tumour, on the breast "
               "fibroepithelial screen; ICCC-2017 places 9020/3 at C50 in XIf6 "
               "(Sosnowska-Sienkiewicz 2024, sections 2 and 76; registrar question 6, answered "
               "8 October 2026)."),
    "8504/3": ("D1", EVIDENCE,
               "Encapsulated papillary carcinoma with invasion on the breast papillary screen; "
               "ICD-O-3.2 moved Intracystic carcinoma, NOS to 8504/2 (currency check §3)."),
    "8509/3": ("D1", EVIDENCE,
               "Solid papillary carcinoma with invasion, and tall cell carcinoma with reversed "
               "polarity, which the WHO breast classification codes 8509/3 (ICCR Invasive Breast "
               "2022, p. 14; registrar question 3), on the breast papillary screen. New in "
               "ICD-O-3.2 and absent from REDCap: the REDCap-side list (standing rule 16)."),
    "8503/3": ("D1", EVIDENCE,
               "Invasive papillary carcinoma, or intraductal papillary carcinoma with invasion, on "
               "the breast papillary screen (ICCR Invasive Breast 2022, p. 14)."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Breast carcinoma whose type the report does not name, at basis 7 on the "
               "histology screen, and any carcinoma cytology names at the breast, at basis 5: "
               "the type is not settled on a limited sample (ICCR Invasive Breast 2022, p. 12)."),
    "8720/3": ("D8, D13", EVIDENCE,
               "Melanoma named on breast cytology, at basis 5; a histology report reaches the "
               "melanoma tree instead."),
}
