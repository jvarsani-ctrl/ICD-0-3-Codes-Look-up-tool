"""g11_skin (prefix sk_): carcinomas of the skin at C44.0-C44.9 and of the genital skin sites C51.9
(vulva, NOS), C60.9 (penis, NOS) and C63.2 (scrotum), ICCC-3 subgroup XIe.

A family tree (contract §4.1, D14). It is built from docs/group_11_evidence/XIe_skin_carcinoma.json
(the evidence agent's nodes sk_document_inventory, sk_clinical, sk_imaging, sk_cytology, sk_site,
sk_histology, sk_not_malignant, sk_carcinoma_other) with the builders in build/group11_common.py,
in the shape of the thyroid exemplar (build/group11_organs/thyroid.py). Every option's label,
code, behaviour, basis, reason and recognition aid comes from that file; the cite (file, PDF page,
quotation) is the comment above the option or the aid. File names in the comments are the
evidence's own:
    Goldman-Levy  XId-XIe-skin-melanoma-and-skin-carcinoma__Goldman-Levy-2025.txt (Goldman-Levy G,
                  et al. WHO classification of skin tumours: key updates in the fifth edition.
                  Histopathology 2025;88:555-568). "image" marks a quotation read from a table's
                  page image.
    ICCR-Merkel   XIe-skin-carcinoma-Merkel__ICCR-Merkel-Cell-2nd.txt (ICCR Merkel Cell Carcinoma
                  Histopathology Reporting Guide, 2nd edition, version 2.0, January 2026)
    Huang         XIe-skin-carcinoma-paediatric__Huang-2019.txt (J Pediatr 2019;211:152-158;
                  PMC7916541). Its pages are PubMed Central sections, written "§6".
    Kaloga        XIe-skin-carcinoma-paediatric__Kaloga-2016.txt (Case Rep Dermatol 2016;8:311-318;
                  PMC5126593). Its pages are PubMed Central sections, written "§9".
    Pfister       ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules         RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser        Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's
                  file set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    sk_document_inventory  document_inventory  evidence gate (evidence sk_document_inventory)
    sk_clinical, sk_clinical_cytology  clinical_alias  (evidence sk_clinical)
    sk_imaging, sk_imaging_cytology    morphology_only (evidence sk_imaging)
    sk_cytology            morphology_only     (evidence sk_cytology)
    sk_histology           histology_subclassification  (evidence sk_histology)
    sk_site                site_resolution     (the Rule A and Rule H options of evidence sk_site)
    sk_nut_result, sk_nut_basis, sk_nut_tests  histology_subclassification  (D12)
    sk_not_malignant       histology_subclassification  (evidence sk_not_malignant)
    sk_deposit             morphology_only     (D10)
    sk_picker              histology_subclassification  (D2; evidence sk_carcinoma_other)

Departures from the evidence nodes, and why
-------------------------------------------
1. sk_document_inventory: the evidence's four tiers are the contract §4.2 tiers. No laboratory
   screen and no marker tier: the evidence names no laboratory test (lab_tests is empty) and
   Visser 2023 Table 4 names no skin marker. The tier labels for cytology and histology are the
   evidence's. The gate hint keeps the evidence's sentences and adds WHO coding Rules A and C
   (the evidence's sk_site hint), so a case at the cytology tier, which never reaches sk_site,
   still records the region's skin.
2. sk_clinical: the evidence's "The note names melanoma of the skin" went to the melanoma tree.
   Until 8 October 2026, evidence_gate(skin_melanoma=True) recorded Malignant melanoma, NOS
   (8720/3) at basis 1 on the note screens (Visser 2023 Table 3). The registrar ruled for the
   paediatric source (review A8, E9; Ferrari 2021, PDF pp. 2-3): a child's melanoma needs tissue,
   so skin_melanoma is False and a note alone takes the common Group XII referral (8000/3).
   "The note states another malignant skin tumour" is the common Group XII referral (8000).
   "An imaging report is in the file after all" is not built: the document checklist decides the
   tier (group11_common, departures). The same holds for sk_imaging's "A histology report is in
   the file after all".
3. sk_cytology: "Cytology names melanoma" went to the melanoma tree. The melanoma tree's
   histology screen records basis 7, which a cytology path cannot carry (D8, the walk's rule D),
   so the cytology screen records Malignant melanoma, NOS (8720/3) at basis 5 itself, as it
   records the three carcinomas the evidence names. "Malignant cells are present, with no tumour
   type named" and the two non-diagnostic routes are the common lines (D8); the common
   "suspicious" line is added, which the evidence's screen lacked.
4. sk_site: the evidence routed every histology case through a 13-option site screen. The
   router's site step already records the site (D14), so the screen keeps only the options that
   correct it: the four body regions WHO coding Rule A sends to the skin (face, trunk, arm, leg),
   and the three genital skin sites ICD-O-3.1 Table 23 names as other primary sites of basal cell
   carcinoma (Rule H, D9). Layer 1's REDCap topography labels put the skin of the vulva, penis
   and scrotum at C51.9, C60.9 and C63.2 (REDCap codes 519, 609, 632), while its C44.9 label
   (code 449, "Skin, NOS (skin of labia majora, skin of vulva, skin of penis, and skin of
   scrotum)") lists the same skin under skin, site not stated, which invites a clerk to record
   C44.9 at the site step; the genital options correct that. It is reached from one histology
   option and returns to the histology screen with the corrected topography, the salivary tree's
   sg_site pattern. Dropped: skin of lip (C44.0), eyelid (C44.1) and external ear (C44.2), which
   are named sites, not Rule A regions, and which the site step offers; skin of the scalp or neck
   (C44.4), which the topography lookup does not carry (contract §3.1: REDCap's topography list
   lacks it); overlapping lesion of skin (C44.8, Rule C), which the site step offers and the gate
   hint explains; skin, site not stated (C44.9), which the site step offers. The site screen is
   not reached from the cytology tier (departure 1 covers it through the gate hint).
5. sk_histology, order: the paediatric entities first (D1; registrar, 8 October 2026): basal cell
   carcinoma, squamous cell carcinoma (Huang, Kaloga), keratoacanthoma (Huang §6); then the
   generic option (carcinoma, with no type named); then the site correction; then the common
   trailing options (tail_options): melanoma (D13, me_skin_histology), NUT carcinoma (D12), the
   picker (D2), the exclusion screen, the deposit question (D10), "Malignant tumour, type not
   determined" (Group XII, 8000, D7) and the referrals. The evidence placed melanoma third and
   keratoacanthoma fourth; contract §4.2 puts melanoma after the generic options.
6. sk_histology, the picker answer: the evidence's "A named subtype of basal cell or squamous
   cell carcinoma ... or another named carcinoma - Merkel cell, adnexal ..." is the common
   picker option. Its examples move to the screen's hint. Merkel cell carcinoma stays a picker
   entry on the histology path (D1: no held source reports it in a child; the evidence's
   registrar question 2, answered 8 October 2026) and a cytology option (the evidence's).
7. sk_histology, NUT carcinoma (D12, the controller's instruction): the evidence kept 8023/3 in
   its picker because no skin source reports it in a child. The common NUT option and screens
   (nut_nodes(skin=True)) replace it, with the common recognition aid; the evidence's NUT aid
   (Goldman-Levy p. 5, p. 7) is not shown.
8. sk_histology, referrals. Lymphoma or histiocytosis keeps the evidence's label and refers to
   Group II at the skin site (Rule D). Leukaemia is the common Group I referral, which records
   C42.1; the evidence's "or myeloid sarcoma" is dropped from the label, because a myeloid
   sarcoma keeps its own site (Rule E) and build_database's
   check_leukaemia_referrals_record_marrow admits a site-keeping Group I referral only on the
   nodes it lists (request 2). The sarcoma referral keeps the evidence's label (Kaposi sarcoma,
   dermatofibrosarcoma protuberans). "Malignant mixed tumour (malignant chondroid syringoma) or
   myoepithelial carcinoma" splits into two Group XII referrals, each with its refer_code (8940,
   8982), as the salivary tree does: one referral carries one code. The common germ cell
   referral (Group X) and "another malignant tumour the report names" (Group XII) are added;
   ICCC-2017 places 9080-9084 in Group X at every routed skin site. The evidence's deposit
   referral (refer_group null with recapture_site) is the deposit question (D10).
9. sk_histology, keratoacanthoma: ruled 8 October 2026 (review A9, E10). A keratoacanthoma is not
   registered unless the pathologist calls it squamous cell carcinoma, so the option is a
   non-reportable line, the picker withholds the term (group11_common.SEARCH_TERMS_WITHHELD) and
   the alias is code-less. The rest of this item describes the build before the ruling.
   ICD-O-3.2 lists Keratoacanthoma as a related term of 8071/3, so the D2 picker's 8071/3 entry
   carries it as a search term: the evidence asked to hold the term out of the search terms
   until the ruling, and the picker's search terms are the live ICD-O-3.2 terms by D2 (validator
   rule 4). Both routes record the same code. The same holds for Pseudovascular squamous cell
   carcinoma on 8074/3 (evidence registrar question 3).
10. sk_not_malignant: the evidence's 21 coded exclusions are excl() lines with the ICD-O-3.2
   Preferred term at each (code, behaviour) and the evidence's labels. Its four exclusions without
   a code (squamoproliferative tumour of uncertain malignant potential, Merkel cell carcinoma in
   situ, nevus sebaceus, cutaneous cribriform tumour) are nonrep() lines, because excl() needs a
   Preferred term ICD-O-3.2 prints at that (code, behaviour) and there is none. Its catch-all is
   the common one. The screen's option on sk_histology names actinic keratosis and nevus
   sebaceus, which are not tumours a clerk would call benign, borderline or in situ.
11. sk_carcinoma_other: D2 replaces the evidence's curated picker. Labels are ICD-O-3.2
   Preferred terms, search_terms the live synonyms and related terms, and the options carry no
   recognition aid (Group 10's picker shape). Not shown from the evidence: the Merkel cell
   carcinoma aid (combined Merkel cell carcinoma; its Rule K sentence moves to sk_histology's
   hint), the NUT carcinoma aid, and the squamoid eccrine ductal carcinoma label and aid (8560/3
   lists as Adenosquamous carcinoma, with Squamoid eccrine ductal carcinoma among its search
   terms); the evidence's labels for 8490/3 and 8509/3 (the picker shows the Preferred terms
   Signet ring cell carcinoma and Solid papillary carcinoma with invasion, and finds the skin
   terms through search_terms). picker_keep keeps 8090/3, 8070/3 and 8071/3, which the
   histology screen offers only as "no subtype named" or as keratoacanthoma, so their synonyms
   (Rodent ulcer, Pigmented basal cell carcinoma, Epidermoid carcinoma, Squamous cell carcinoma,
   keratinizing) stay searchable (evidence data gap 5). The standing-rule-3 codes the evidence
   names (8490, 8502, 8509) are D11 picker entries. D2 also lists 16 codes the evidence's picker
   left out, because ICCC-2017 places them in Group XI at every site: the thyroid codes
   8330-8332, 8335, 8337, 8340-8347 and 8588 (range 121, XIb) and 8370 (range 119, XIa), and
   8540 (departure 12).
12. Paget disease, mammary (8540/3): the evidence leaves it off the skin screens (Rule H; Rules
   p. 10). ICCC-2017 range 124 places it in XIe at every routed site, so the D2 picker lists it
   (validator rule 4). The histology hint sends Paget disease of the nipple or breast back to the
   site step.
13. Not built from the evidence: Cribriform carcinoma, NOS (8201/3) at the skin (evidence
   registrar question 4; no ICCC-2017 range holds 8201 at the skin and the evidence does not put
   it in its picker), and stated-behaviour codes for the tumours ICD-O-3.2 prints only below /3
   (D6). The immunohistochemistry screen is not built: the evidence gives no rules (evidence §4).

Registrar questions the evidence raised (XIe_skin_carcinoma.md §10, questions 1-9) stay open; the
defaults above apply until they are answered (docs/group_11_registrar_review.md).

Requests outside this module
----------------------------
1. build_database.check_leukaemia_referrals_record_marrow: a site-keeping myeloid sarcoma
   referral on sk_histology (WHO Rule E), as the evidence's leukaemia option asked.
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, aid, cyto, cyto_carcinoma_nos, deposit_node,
                            evidence_gate, excl, go, make_tree, named, node, nonrep,
                            not_malignant_node, nut_nodes, refer, refer_germ_cell,
                            refer_leukaemia, refer_other_named, refer_sarcoma, tail_options, term)

TREE_ID = "g11_skin"
P = "sk_"
WHERE = "the skin"
EVIDENCE = "XIe_skin_carcinoma"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Kaloga §9 (figure legend) "Hyperplasia of the squamous epithelium formed from atypical cells
# with hyperkeratosis" (the evidence's sk_histology option 2 aid).
AID_SCC = ("Reports describe atypical squamous cells with hyperkeratosis, and tumour cells "
           "infiltrating the dermis.")

SUBTYPE_UPGRADE = ("The report does not name a subtype. A report that names one may give a more "
                   "specific code: go back and choose another carcinoma the report names.")


# ------------------------------------------------------------------------------------------
# Group XII referrals for the skin tumours ICCC-2017 places in XIIa4 (departure 8)
# ------------------------------------------------------------------------------------------
def refer_xii(label, morph, extra, *, note):
    """A skin tumour that ICCC-2017 places in XIIa4 at every site: refer to Group XII and name
    its code (refer_code). The salivary tree's helper, with the skin's wording."""
    return refer(label, 12,
                 "ICCC-3 codes %s (%s/3) in Group XII (other and unspecified malignant "
                 "neoplasms, subgroup XIIa4) at every site, not in Group XI.%s Code the case from "
                 "the Group XII tree." % (term(morph, "3"), morph, (" " + extra) if extra else ""),
                 refer_code=morph, note=note)


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence sk_document_inventory, sk_clinical, sk_imaging, sk_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this skin tumour?",
        # Evidence sk_document_inventory hint. ICCR-Merkel p. 1 "Biopsy (e.g., curettage, shave,
        # punch, elliptical)". Rules p. 1 (printed p. 14) "should be coded to C44.6 (skin of arm)
        # rather" and "such as chin and forehead, because these regions"; Rules p. 1-2 (printed
        # pp. 14-15) Rule C "when a single tumor overlaps the boundaries of two or more"
        # (evidence sk_site hint; departure 1).
        hint=("A radiology report counts as imaging. A pathology report on a curettage, shave, "
              "punch or excision biopsy counts as histology. An immunohistochemistry or gene "
              "report on its own does not stand in for a histology report. A biopsy or cytology "
              "report that calls the specimen inadequate or non-diagnostic counts as no tissue. "
              "A carcinoma the report places at a body region with no tissue named, such as the "
              "arm, the leg, the back, the chin or the forehead, is recorded at the skin of that "
              "region (WHO coding Rule A). A tumour across two skin regions whose starting point "
              "the report does not give is recorded at overlapping lesion of skin, C44.8 (WHO "
              "coding Rule C): go back to the site step to change the site. A report that calls "
              "the tumour possible or suspected does not register it."),
        tier_labels={
            # Evidence sk_document_inventory options 3 and 4. ICCR-Merkel p. 4 "For small partial
            # biopsies and cytology specimens, reporting the tumour diagnosis is usually
            # sufficient"; ICCR-Merkel p. 1 "Biopsy (e.g., curettage, shave, punch, elliptical)".
            "cytology": "Cytology only - a scraping or fine-needle aspirate; no histology report",
            "histology": "A histology report - biopsy or excision, with or without "
                         "immunohistochemistry or gene reports",
        },
        # D7 withdrew Visser 2023 Table 3's melanoma row for children. Registrar, 8 October
        # 2026 (review A8, E9): "We go with pediatric source". Ferrari 2021, PDF p. 2 (benign
        # pigmented lesions look like melanoma; the ABCDE rule can mislead) and PDF p. 3 ("When
        # melanoma is suspected, initial excisional biopsy is required"). A note alone refers to
        # Group XII with 8000/3 at basis 1, as at every other site.
        skin_melanoma=False,
        cytology=[
            # Evidence sk_cytology option 1; tissue_free row 5 ("Family-level codes only;
            # cytology gives no subtype").
            cyto("Cytology names squamous cell carcinoma", "8070",
                 note="Evidence sk_cytology option 1."),
            # Rules p. 10 image "8090/3 Basal cell carcinoma C44._ Skin".
            cyto("Cytology names basal cell carcinoma", "8090",
                 note="Evidence sk_cytology option 2."),
            # ICCR-Merkel p. 4 "For small partial biopsies and cytology specimens, reporting the
            # tumour diagnosis is usually sufficient"; ICCR-Merkel p. 7 image "Merkel cell
            # carcinoma 8247/3".
            cyto("Cytology names Merkel cell carcinoma", "8247",
                 note="Evidence sk_cytology option 3; tissue_free row 4."),
            cyto_carcinoma_nos(note="Evidence sk_cytology option 4 ('Cytology names a carcinoma "
                                    "without naming its type', 8010/3 at basis 5)."),
            # Evidence sk_cytology option 5 (departure 3). ICCC-2017 range 123 places 8720/3 in
            # XId at every site.
            cyto("Cytology names melanoma", "8720",
                 "ICD-O-3.2 gives Melanoma, NOS as a synonym of this code.",
                 note="Evidence sk_cytology option 5, which went to the melanoma tree; coded here "
                      "at basis 5 (departure 3)."),
            # Rules p. 2 (printed p. 15) "extranodal lymphomas to the site of origin".
            refer("Cytology names a lymphoma", 2,
                  "A lymphoma belongs to ICCC-3 Group II. A lymphoma that arises in the skin "
                  "keeps the skin as its site (WHO Rule D: an extranodal lymphoma is coded to "
                  "its site of origin). Code the case from the Group II (lymphomas) tree.",
                  note="Evidence sk_cytology option 6. ICD-O-3.1 Rule D, p. 15. The hop carries "
                       "the case's site."),
        ],
        note="Evidence sk_document_inventory, sk_clinical, sk_imaging and sk_cytology "
             "(departures 1 to 3).")


# ------------------------------------------------------------------------------------------
# Histology (evidence sk_histology)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # Huang §6 "Forty cases had at least 1 SCC, 95 patients had at least 1 BCC"; Huang §7
        # "12.2 years (range 0.9–19.8) in patients with BCC"; Huang §12 (Table I) "Age at
        # diagnosis 0–5 y 6 (15) 12 (13)". D1: paediatric, first (registrar, 8 October 2026).
        named("Basal cell carcinoma, with no subtype named", "8090", upgrade=SUBTYPE_UPGRADE,
              note="D1: Huang 2019, PMC sections 6, 7 and 12. Evidence sk_histology option 1. "
                   "Evidence data gap 3: no held source describes basal cell carcinoma in report "
                   "vocabulary, so the option carries no recognition aid."),
        # Kaloga §1 "Histology confirmed squamous cell carcinoma in all 3 cases"; Kaloga §4 "A
        # pathological examination of a fragment of the tumor confirmed squamous cell carcinoma";
        # Huang §7 "14.1 years (range 2.2–19.8) in patients with SCC"; Huang §10 "Of those with
        # invasive SCC (n = 29)". D1: paediatric, second.
        aid(named("Squamous cell carcinoma, with no subtype named - well, moderately or poorly "
                  "differentiated, or no grade stated", "8070",
                  "The stated differentiation does not change the code.",
                  upgrade=SUBTYPE_UPGRADE,
                  note="D1: Kaloga 2016, PMC sections 1 and 4; Huang 2019, PMC sections 7, 10 and "
                       "12. Evidence sk_histology option 2; rules_a_to_k G (no screen offers two "
                       "grades)."),
            AID_SCC),
        # Goldman-Levy p. 3 "While the distinction between KA and SCC remains controversial" and
        # "a separate entity from SCC"; Huang §6 "131 SCC (36 in situ, 87 invasive lesions, and 8
        # keratoacanthomas)"; Huang §4 "the term SCC includes SCC in situ, SCC invasive, and
        # keratoacanthomas". Registrar, 8 October 2026 (review A9, E10): "excluded unless the
        # pathologist calls it malignant. Only if the pathologist calls it squamous cell
        # carcinoma".
        nonrep("Keratoacanthoma, which the report does not call squamous cell carcinoma",
               "A keratoacanthoma is not registered unless the pathologist calls it squamous cell "
               "carcinoma. A report that does takes the squamous cell carcinoma option on this "
               "screen.",
               note="Registrar, 8 October 2026 (review A9, E10). Evidence sk_histology option 4. "
                    "ICD-O-3.2 files Keratoacanthoma as a related term of 8071/3 and prints no "
                    "8071/1; Goldman-Levy 2025, p. 3, treats it as likely a separate entity."),
        # Evidence sk_histology option 6 ("Carcinoma, with no type named").
        named("Carcinoma, with no type named", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence sk_histology option 6; the generic option of the screen (evidence "
                   "data gap 6)."),
        # Rules p. 1 (printed p. 14) "should be coded to C44.6 (skin of arm) rather"; Rules p. 10
        # image "8090/3 Basal cell carcinoma C44._ Skin" and "C63.2 Scrotum". Departure 4.
        go("The report places the tumour at a body region, such as the arm, the leg, the back, "
           "the chin or the forehead, or on the skin of the vulva, penis or scrotum, and the site "
           "recorded is a different one", n("site"),
           note="Departure 4: the Rule A and Rule H options of evidence sk_site (D9)."),
    ] + tail_options(
        P, "skin", where=WHERE, nut=True,
        # Evidence sk_histology option 7 ("Benign, in situ, or of uncertain malignant potential
        # - the report says so"); departure 10.
        not_malignant_label="A tumour the report calls benign, in situ or of uncertain malignant "
                            "potential, or a skin lesion such as actinic keratosis or nevus "
                            "sebaceus",
        referrals=[
            # Goldman-Levy p. 7 "In the 5th Edition, among histiocytic and dendritic"; Rules p. 2
            # (printed p. 15) "extranodal lymphomas to the site of origin". ICCC-2017: 9700 IIb3,
            # 9751 IId at every site.
            refer("Lymphoma or histiocytosis in the skin, for example mycosis fungoides or "
                  "Langerhans cell histiocytosis", 2,
                  "Lymphomas and histiocytoses belong to ICCC-3 Group II. A lymphoma that begins "
                  "in the skin keeps the skin as its site (WHO Rule D: an extranodal lymphoma is "
                  "coded to its site of origin). Code the case from the Group II (lymphomas) "
                  "tree.",
                  note="Evidence sk_histology option 8. ICD-O-3.1 Rule D, p. 15. The hop carries "
                       "the case's site."),
            # Rules p. 2 (printed p. 15) "Code all leukemias except myeloid sarcoma". ICCC-2017:
            # 9930 Ib at every site. Departure 8: the myeloid sarcoma half of the evidence's label
            # is not built.
            refer_leukaemia(WHERE),
            # Goldman-Levy p. 9 "The Skin5 includes four new soft tissue tumour". ICCC-2017: 9140
            # IXc, 8832 IXd5 at every site.
            refer_sarcoma(WHERE, label="Sarcoma or another soft tissue tumour, for example Kaposi "
                                       "sarcoma or dermatofibrosarcoma protuberans"),
            # ICCC-2017: 9080-9084 Xb2 at every routed skin site. Not in the evidence (departure 8).
            refer_germ_cell(WHERE),
            # Goldman-Levy p. 6 image "Cutaneous mixed tumour"; ICCC-2017 code_lookup 8940 XII
            # XIIa4 000-809 (evidence conflicts, Group 12; registrar question 8).
            refer_xii("Malignant chondroid syringoma, or malignant mixed tumour of the skin",
                      "8940",
                      "ICD-O-3.2 gives Malignant chondroid syringoma as a related term of this "
                      "code.",
                      note="Evidence sk_histology option 11, split (departure 8). ICCC-2017 "
                           "code_lookup 8940 XII XIIa4 000-809."),
            # Goldman-Levy p. 6 image "Myoepithelioma"; ICCC-2017 code_lookup 8982 XII XIIa4.
            refer_xii("Myoepithelial carcinoma of the skin", "8982",
                      "ICD-O-3.2 gives Malignant myoepithelioma as a synonym of this code.",
                      note="Evidence sk_histology option 11, split (departure 8). ICCC-2017 "
                           "code_lookup 8982 XII XIIa4 000-809."),
            refer_other_named(),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence sk_histology hint (Rules p. 2, printed p. 15, Rule F "code as the pathologist
        # indicates"); evidence sk_carcinoma_other hint, Rule K (Rules p. 11, printed p. 24 "use
        # the numerically higher code number if the diagnosis of a single tumor"; ICCR-Merkel p. 7
        # "The most frequent combination is that of neuroendocrine and in situ and/or invasive
        # squamous cell"); Rules p. 10 "topography code should be disregarded if the tumor is
        # known to arise at another site" (Paget disease, mammary; departure 12).
        "Use the report's own term. If the report states that the tumour is benign, in situ or "
        "of uncertain malignant potential, choose that answer, even for a tumour type that is "
        "usually malignant. A named subtype of basal cell or squamous cell carcinoma (nodular, "
        "superficial, infiltrating, keratinizing and others), Merkel cell carcinoma, and the "
        "adnexal carcinomas (sweat gland, hair follicle or sebaceous) are found under another "
        "carcinoma the report names. When one tumour shows two types and no single answer names "
        "both, choose the higher code (WHO coding Rule K): a Merkel cell carcinoma combined with "
        "squamous cell carcinoma is recorded as Merkel cell carcinoma (8247/3). Paget disease of "
        "the nipple or breast is coded at the breast: go back to the site step.",
        opts, [],
        "Evidence sk_histology (departures 5 to 9). D1: basal cell carcinoma and squamous cell "
        "carcinoma (Huang 2019; Kaloga 2016) and keratoacanthoma (Huang 2019, registrar question "
        "1) are the paediatric entities; Merkel cell carcinoma and the adnexal carcinomas stay "
        "picker entries (evidence data gap 1). NUT carcinoma is an option (D12).")


def site():
    caps = (lambda topo: {"topography": topo})
    back = n("histology")
    return node(
        n("site"), "site_resolution", 4, "Site of the tumour",
        "Where on the body does the report place the tumour?",
        # Evidence sk_site hint. Rules p. 1 (printed p. 14) Rule A "should be coded to C44.6
        # (skin of arm) rather" and "such as chin and forehead, because these regions"; Rule B
        # "unless the type of tumor indicates origin from a particular tissue"; Rules p. 10
        # (printed p. 23) Table 23 image "8090/3 Basal cell carcinoma C44._ Skin" with "C51._
        # Vulva", "C60._ Penis", "C63.2 Scrotum" as other primary sites; Layer 1 Topography
        # Redcap.md lines "519, Vulva, NOS (... Skin of vulva)", "609, Penis, NOS (Skin of
        # penis)", "632, Scrotum, NOS (Skin of scrotum)".
        "A carcinoma the report places at a body region with no tissue named (the arm, the leg, "
        "the back, the chin, the forehead) is recorded at the skin of that region (WHO coding "
        "Rule A). A site written with peri- or para- is the skin of that region when the tumour "
        "is a skin carcinoma (Rule B). Basal cell carcinoma and the other skin carcinomas of the "
        "vulva, penis or scrotum are recorded at the vulva, the penis or the scrotum, which ICD-O "
        "names as other primary sites of basal cell carcinoma (Rule H). For the eyelid, the "
        "external ear, the skin of the lip, or a named part of the vulva or penis, go back to "
        "the site step. The next screen asks the tumour type again.",
        [
            # Rules p. 1 (printed p. 14) "such as chin and forehead, because these regions"; Rules
            # p. 4 (printed p. 17) "are not assigned to C76 but to skin (C44)".
            go("The face: the chin, forehead, nose, cheek or temple, or the face with no part "
               "named (skin of face, C44.3)", back, captures=caps("C44.3"),
               note="Evidence sk_site option 4. Rule A."),
            # Evidence sk_site option 6; Rule A applied to the trunk's regions.
            go("The trunk: the back, chest, abdomen, buttock or groin, or the skin around the anus "
               "(skin of trunk, C44.5)", back, captures=caps("C44.5"),
               note="Evidence sk_site option 6. Rule A."),
            # Rules p. 1 (printed p. 14) "should be coded to C44.6 (skin of arm) rather"; Rules
            # p. 4 (printed p. 17) "types of carcinomas of the arm, such as squamous".
            go("The arm, hand or shoulder (skin of upper limb and shoulder, C44.6)", back,
               captures=caps("C44.6"), note="Evidence sk_site option 7. Rule A."),
            # Evidence sk_site option 8; Rule A applied to the lower limb.
            go("The leg, foot or hip (skin of lower limb and hip, C44.7)", back,
               captures=caps("C44.7"), note="Evidence sk_site option 8. Rule A."),
            # Rules p. 10 (printed p. 23) Table 23 image "C51._ Vulva"; Layer 1 Topography
            # Redcap.md "519, Vulva, NOS (... Skin of vulva)". The skin tree routes C51.9 only; a
            # named part (C51.0-C51.8) is g11_female_genital's.
            go("The skin of the vulva, part not stated (vulva, C51.9)", back,
               captures=caps("C51.9"), note="Evidence sk_site option 11. Rule H, D9."),
            # Rules p. 10 (printed p. 23) Table 23 image "C60._ Penis"; Layer 1 Topography
            # Redcap.md "609, Penis, NOS (Skin of penis)". C60.0-C60.8 are
            # g11_urinary_male_genital's.
            go("The skin of the penis, part not stated (penis, C60.9)", back,
               captures=caps("C60.9"), note="Evidence sk_site option 12. Rule H, D9."),
            # Rules p. 10 (printed p. 23) Table 23 image "C63.2 Scrotum"; Layer 1 Topography
            # Redcap.md "632, Scrotum, NOS (Skin of scrotum)".
            go("The skin of the scrotum (scrotum, C63.2)", back, captures=caps("C63.2"),
               note="Evidence sk_site option 13. Rule H, D9."),
        ], ["topography"],
        "Departure 4: the options of evidence sk_site that correct the site the router recorded "
        "(D9; Rule A, Rules p. 1 and p. 4; Rule H, Table 23, Rules p. 10). Each captures the "
        "topography and returns to the histology screen, the salivary tree's sg_site pattern. "
        "Every code the histology screen emits is a Group XI code at C44.3, C44.5-C44.7, C51.9, "
        "C60.9 and C63.2 (routed sites of this tree). Not built: C44.0-C44.2, C44.8, C44.9 (the "
        "site step offers them) and C44.4 (absent from the topography lookup, contract §3.1).")


# ------------------------------------------------------------------------------------------
# The exclusion screen (evidence sk_not_malignant; departure 10)
# ------------------------------------------------------------------------------------------
def not_malignant():
    return not_malignant_node(
        P,
        [
            # Goldman-Levy p. 3 "However, reliable distinction of these two entities is not always
            # possible"; Rules p. 2 (printed p. 15) "code as the pathologist indicates".
            # Registrar question 5.
            nonrep("Squamoproliferative tumour of uncertain malignant potential",
                   "The report states an uncertain behaviour (behaviour 1), and ICD-O-3.2 prints "
                   "no term for this tumour. ICCC-3 Group XI registers behaviour 3 (malignant) "
                   "only, so no Group XI code is recorded.",
                   note="Evidence sk_not_malignant option 1; registrar question 5."),
            # ICCR-Merkel p. 10 "MCC in situ (i.e., completely limited to epidermis or adnexal
            # epithelium)"; Rules p. 2 "Use the appropriate 5th digit behavior code even if the
            # exact term is not listed".
            nonrep("Merkel cell carcinoma in situ, limited to the epidermis or the adnexal "
                   "epithelium",
                   "The report calls the Merkel cell carcinoma in situ (behaviour 2), and "
                   "ICD-O-3.2 prints no in situ term for it. ICCC-3 Group XI registers behaviour "
                   "3 (malignant) only, so no Group XI code is recorded.",
                   note="Evidence sk_not_malignant option 2."),
            # Pfister p. 14 image "Pilomatricoma"; Goldman-Levy p. 6 image "Pilomatricoma and
            # pilomatrical carcinoma".
            excl("Pilomatricoma", "8110", "0", what="a pilomatricoma",
                 extra="ICD-O-3.2 gives Pilomatrixoma, NOS and Calcifying epithelioma of Malherbe "
                       "as synonyms of this code.",
                 note="Evidence sk_not_malignant option 3."),
            # Pfister p. 14 image "Angiokeratoma".
            excl("Angiokeratoma", "9141", "0", what="an angiokeratoma",
                 note="Evidence sk_not_malignant option 4."),
            # Huang §8 "including 21 with actinic keratoses".
            excl("Actinic keratosis", "8070", "0", what="an actinic keratosis",
                 note="Evidence sk_not_malignant option 5."),
            # Goldman-Levy p. 6 image "Proliferating trichilemmal tumour". Currency check §3:
            # 8103 /0 to /1.
            excl("Proliferating trichilemmal tumour", "8103", "1",
                 what="a proliferating trichilemmal tumour",
                 extra="ICD-O-3.2 gives Proliferating trichilemmal tumor as a synonym of this "
                       "code.",
                 note="Evidence sk_not_malignant option 6; code_currency 8103."),
            excl("Pilar tumour", "8103", "0", what="a pilar tumour",
                 note="Evidence sk_not_malignant option 7; code_currency 8103."),
            # Goldman-Levy p. 6 image "Trichoblastoma (including trichoepitheloma)".
            excl("Trichoblastoma, including trichoepithelioma", "8100", "0",
                 what="a trichoblastoma or trichoepithelioma",
                 extra="ICD-O-3.2 gives Trichoblastoma as a related term of this code.",
                 note="Evidence sk_not_malignant option 8."),
            # Goldman-Levy p. 6 image "Trichilemmoma".
            excl("Trichilemmoma", "8102", "0", what="a trichilemmoma",
                 note="Evidence sk_not_malignant option 9."),
            # Goldman-Levy p. 6 image "Poroma, porocarcinoma".
            excl("Poroma", "8409", "0", what="a poroma",
                 extra="ICD-O-3.2 gives Eccrine poroma, NOS as a related term of this code.",
                 note="Evidence sk_not_malignant option 10."),
            # Goldman-Levy p. 6 image "Hidradenoma, hidradenocarcinoma".
            excl("Hidradenoma", "8402", "0", what="a hidradenoma",
                 extra="ICD-O-3.2 gives Nodular hidradenoma as a synonym of this code.",
                 note="Evidence sk_not_malignant option 11."),
            # Goldman-Levy p. 6 image "Cylindroma, spiradenoma and malignant tumours".
            excl("Spiradenoma", "8403", "0", what="a spiradenoma",
                 extra="ICD-O-3.2 gives Eccrine spiradenoma as a synonym of this code.",
                 note="Evidence sk_not_malignant option 12."),
            # Goldman-Levy p. 6 image "Cylindroma, spiradenoma and malignant tumours". Evidence
            # code_currency 8200: Cylindroma, NOS is [obs] on 8200/3.
            excl("Cylindroma", "8200", "0", what="a cylindroma of the skin",
                 extra="ICD-O-3.2 gives Cylindroma of skin as a related term of this code.",
                 note="Evidence sk_not_malignant option 13; code_currency 8200."),
            # Goldman-Levy p. 6 image "Sebaceous adenoma and sebaceoma".
            excl("Sebaceous adenoma or sebaceoma", "8410", "0",
                 what="a sebaceous adenoma or sebaceoma",
                 extra="ICD-O-3.2 gives Sebaceous adenoma as a related term of this code.",
                 note="Evidence sk_not_malignant option 14."),
            # Goldman-Levy p. 6 image "Syringocystadenoma papilliferum, tubular".
            excl("Syringocystadenoma papilliferum", "8406", "0",
                 what="a syringocystadenoma papilliferum",
                 note="Evidence sk_not_malignant option 15."),
            # Goldman-Levy p. 6 image "Cutaneous mixed tumour".
            excl("Cutaneous mixed tumour, or chondroid syringoma", "8940", "0",
                 what="a benign cutaneous mixed tumour",
                 extra="ICD-O-3.2 gives Chondroid syringoma, NOS as a related term of this code.",
                 note="Evidence sk_not_malignant option 16."),
            # Goldman-Levy p. 6 image "Myoepithelioma".
            excl("Myoepithelioma", "8982", "0", what="a myoepithelioma",
                 note="Evidence sk_not_malignant option 17."),
            excl("Bowen disease", "8081", "2", what="Bowen disease",
                 extra="ICD-O-3.2 gives Intraepidermal squamous cell carcinoma, Bowen type as a "
                       "synonym of this code.",
                 note="Evidence sk_not_malignant option 18; code_currency 8081."),
            # Huang §6 "131 SCC (36 in situ, 87 invasive lesions, and 8 keratoacanthomas)".
            excl("Squamous cell carcinoma in situ", "8070", "2",
                 what="a squamous cell carcinoma in situ",
                 extra="ICD-O-3.2 gives Intraepidermal carcinoma, NOS as a synonym of this code.",
                 note="Evidence sk_not_malignant option 19."),
            excl("Porocarcinoma in situ", "8409", "2", what="a porocarcinoma in situ",
                 note="Evidence sk_not_malignant option 20."),
            excl("Vulvar intraepithelial neoplasia, high grade (VIN III)", "8077", "2",
                 what="a high-grade vulvar intraepithelial neoplasia",
                 extra="ICD-O-3.2 gives Vulvar intraepithelial neoplasia, grade III as a related "
                       "term of this code.",
                 note="Evidence sk_not_malignant option 21 (C51.9)."),
            excl("Differentiated vulvar or penile intraepithelial neoplasia", "8071", "2",
                 what="a differentiated vulvar or penile intraepithelial neoplasia",
                 note="Evidence sk_not_malignant option 22 (C51.9, C60.9)."),
            excl("Queyrat erythroplasia", "8080", "2", what="Queyrat erythroplasia",
                 note="Evidence sk_not_malignant option 23 (C60.9)."),
            # Pfister p. 14 image "Epidermal nevi (nevus sebaceus)"; Pfister p. 11 "Other
            # pediatric skin tumors include hamartomas, epidermal nevi, and additional"; Huang §12
            # (Table I) "Nevus sebaceus 0 (0) 9 (9) 9 (7)".
            nonrep("Nevus sebaceus (epidermal naevus)",
                   "Not registrable. A nevus sebaceus is an epidermal naevus, not a malignant "
                   "tumour, and ICD-O-3.2 prints no term for it. A carcinoma the report finds "
                   "within a nevus sebaceus is coded as that carcinoma: go back and choose it.",
                   note="Evidence sk_not_malignant option 24."),
            # Goldman-Levy p. 5 "is now downgraded to cribriform tumour", "owing to the absence
            # of reported recurrences and metastases" and "Cutaneous cribriform tumour, an
            # indolent adnexal". Registrar question 4 (an older report of cribriform carcinoma of
            # the skin, 8201/3).
            nonrep("Cutaneous cribriform tumour",
                   "Not registrable. The WHO classification of skin tumours, 5th edition, "
                   "classes cutaneous cribriform tumour as an indolent tumour with no recurrence "
                   "or metastasis reported, and ICD-O-3.2 prints no term for it.",
                   note="Evidence sk_not_malignant option 25; registrar question 4."),
        ],
        where=WHERE,
        note="The exclusions of evidence sk_not_malignant (departure 10). Its option 26 is the "
             "common catch-all.")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), site()] + nut_nodes(P, skin=True) + [
        not_malignant(), deposit_node(P, where=WHERE)]
    return make_tree(
        TREE_ID, nodes,
        # Standing rule 3 (D11): no ICCC-2017 range holds these at the routed skin sites, and the
        # evidence names them as picker entries: Signet ring cell/histiocytoid carcinoma
        # (code_currency 8490), Secretory carcinoma (code_currency 8502), Endocrine
        # mucin-producing sweat gland carcinoma (code_currency 8509).
        d11=("8490", "8502", "8509"),
        # Departure 11 (evidence data gap 5): the screen offers these only as "no subtype named"
        # or as keratoacanthoma; the picker keeps their synonyms searchable.
        picker_keep=("8090", "8070", "8071"))


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8090/3": ("D1, D8", EVIDENCE,
               "Basal cell carcinoma, the first skin option (Huang 2019, PMC sections 6, 7 and "
               "12), at basis 7 on the histology screen and basis 5 when cytology names it; in "
               "the skin picker for its synonyms."),
    "8070/3": ("D1, D8", EVIDENCE,
               "Squamous cell carcinoma of the skin (Kaloga 2016; Huang 2019), at basis 7 on the "
               "histology screen and basis 5 when cytology names it; in the skin picker for its "
               "synonyms."),
    "8071/3": ("D1, D2", EVIDENCE,
               "In the skin picker as Squamous cell carcinoma, keratinizing, NOS. A report of "
               "keratoacanthoma does not record it unless the pathologist calls the lesion "
               "squamous cell carcinoma (registrar, 8 October 2026, review A9, E10; Goldman-Levy "
               "2025, p. 3)."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma whose type the report does not name: basis 7 on the skin histology "
               "screen, basis 5 when cytology names a carcinoma without its type."),
    "8247/3": ("D1, D2, D8", EVIDENCE,
               "Merkel cell carcinoma at basis 5 when skin cytology names it (ICCR Merkel Cell "
               "Carcinoma, 2nd edition, p. 4); a skin picker entry on the histology path, because "
               "no held source reports it in a child (evidence data gap 1)."),
    "8720/3": ("D7, D8, D13", EVIDENCE,
               "Melanoma of the skin at basis 5 when skin cytology names melanoma; a skin histology "
               "report reaches the melanoma tree. A clinical note alone does not record it: the "
               "registrar ruled for the paediatric source (review A8, E9; Ferrari 2021, PDF "
               "p. 3)."),
    "8023/3": ("D12, D15", "%s, NUT_carcinoma" % EVIDENCE,
               "Primary cutaneous NUT carcinoma (Goldman-Levy 2025, p. 5) on the skin tree's NUT "
               "carcinoma screens: basis 8 with a NUTM1 result, basis 7 otherwise. New in "
               "ICD-O-3.2 and absent from REDCap's XIe list: the REDCap-side list (standing rule "
               "16)."),
}
