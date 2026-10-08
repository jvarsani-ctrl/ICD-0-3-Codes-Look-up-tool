"""g11_nasopharynx (prefix np_): nasopharyngeal carcinomas at C11.0-C11.9, ICCC-3 subgroup XIc.

Built from docs/group_11_evidence/XIc_nasopharynx.json, the nasopharynx nodes only (np_document_inventory,
np_clinical, np_imaging, np_cytology, np_histology, np_npc_type, np_ihc, np_salivary,
np_not_malignant, np_deposit, np_carcinoma_other). The oropharynx nodes of the same file (op_*) belong
to g11_head_neck. Every option's label, code, behaviour, basis, reason and recognition aid comes from
that file; the cite (file, PDF page, quotation) is the comment above the option or the aid. File names
in the comments are the evidence's own:
    Badoual   XIc-nasopharynx__Badoual-2022.txt (Badoual C. Head Neck Pathol 2022;16:19-30, the WHO
              Classification of Head and Neck Tumours, 5th edition, oropharynx and nasopharynx)
    ICCR      XIc-nasopharynx__ICCR-Oropharynx-Nasopharynx-2nd.txt (International Collaboration on
              Cancer Reporting, Carcinomas of the Oropharynx and Nasopharynx, 2nd edition, version
              2.0, July 2024). Table 2 (the WHO nasopharynx table) is on PDF p. 11.
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 section 4, printed pp. 14-28)

Nodes, in tree order:
    np_document_inventory  document_inventory  evidence gate (evidence np_document_inventory)
    np_clinical, np_clinical_cytology          clinical_alias (evidence np_clinical)
    np_imaging, np_imaging_cytology            morphology_only (evidence np_imaging)
    np_cytology            morphology_only     (evidence np_cytology)
    np_histology           histology_subclassification  (evidence np_histology)
    np_npc_type            histology_subclassification  (evidence np_npc_type)
    np_salivary            histology_subclassification  (evidence np_salivary)
    np_ihc                 ihc_checklist        (evidence np_ihc and ihc_rules 1-4)
    np_nut_result, np_nut_basis, np_nut_tests  histology_subclassification (D12, nut_nodes())
    np_not_malignant       histology_subclassification  (evidence np_not_malignant)
    np_deposit             morphology_only      (D10; evidence np_deposit)
    np_picker              histology_subclassification  (D2; evidence np_carcinoma_other)

Departures from the evidence nodes, and why
-------------------------------------------
1. np_document_inventory: the evidence's four tiers become the contract §4.2 tiers (referral,
   imaging, cytology, histology), whose rules live in docs/evidence_documents/group_11.json. No
   laboratory screen and no marker tier: the evidence's lab_tests give no test a diagnostic role
   (Epstein-Barr virus serology is post-treatment surveillance, ICCR p. 15; plasma Epstein-Barr virus
   DNA is staging, ICCR p. 17), and Visser 2023 Table 4 has no nasopharyngeal row (contract §0.5;
   evidence data gap 7). The imaging tier's label keeps "with or without an Epstein-Barr virus blood
   test" and the hint keeps the evidence's sentence. The hint adds WHO coding Rule C (Rules PDF p. 5),
   which the evidence placed at the router's site capture: a tumour over the nasopharynx and the
   oropharynx with no stated origin is C14.8. The router is not this module's file.
2. np_clinical and np_imaging recorded 8000/3 at basis 1 and 2. D7: ICCC-2017 places 8000/3 at
   C11.0-C11.9 in XIIb (range 143), so each refers to Group XII with refer_code 8000. The escapes
   "An imaging report is in the file after all" and "A histology report is in the file" are dropped:
   the document checklist decides the tier (group11_common, departures from Group 10).
3. np_cytology: "Malignant cells are present, with no tumour type named" (8001/3 at basis 5) refers
   to Group XII with refer_code 8001 (D8; ICCC-2017 range 143). "Cytology names a carcinoma with no
   type" is cyto_carcinoma_nos(). The non-diagnostic routes are the common ones; "Suspicious,
   atypical, indeterminate or benign" is the common non-registrable line, which the evidence lacked.
4. np_histology, NUT carcinoma: the evidence coded 8023/3 at basis 7 directly. D12 replaces it with
   the common NUT option and its screens (np_nut_result, np_nut_basis, np_nut_tests), which record
   8023/3 at basis 7 or, with a NUTM1 result, basis 8 (D15).
5. np_histology, order: the paediatric entities first (D1: nasopharyngeal carcinoma and the
   salivary gland-type carcinomas, Pfister p. 14), then the generic poorly differentiated carcinoma,
   then the common trailing options (tail_options): melanoma (D13, me_mucosa), NUT carcinoma (D12),
   the picker (D2), the exclusion screen (labelled with the evidence's wording), the deposit question
   (D10), "Malignant tumour, type not determined" (Group XII, 8000, D7), and the referrals lymphoma
   (II, keeps C11, Rule D), leukaemia (I, C42.1), rhabdomyosarcoma or another soft tissue sarcoma
   (IX), teratoma or another germ cell tumour (X) and another named tumour (XII). The evidence's
   chordoma (VIII, recapture) and craniopharyngioma or pituitary tumour (III) referrals follow them.
6. np_histology, option 1: the label adds the older names lymphoepithelioma and undifferentiated
   carcinoma of nasopharyngeal type, so a report using them reaches np_npc_type, where each
   records its own code (departure 7).
7. np_npc_type: the evidence's single option for the older names recorded 8072/3, as the evidence's
   registrar question argues from ICCR Table 2 (p. 11) and Badoual p. 8 ("lymphoepithelial
   features" of non-keratinising carcinoma). The registrar ruled on 8 October 2026 that review A1
   (a) and (b) are decided by the WHO ICD-O-3 coding Rules A to K, and docs/group_11_evidence/
   registrar_A1ab_rules.md applies them (C1 to C3). The option splits in two. "Lymphoepithelioma,
   lymphoepithelial carcinoma, lymphoepithelioma-like carcinoma or Schmincke tumour" records 8082/3
   Lymphoepithelial carcinoma, the code ICD-O-3.2 prints for each of those terms (section 4.3.3,
   p. 21; Rule H, p. 23). "Undifferentiated carcinoma of nasopharyngeal type" records 8020/3
   Carcinoma, undifferentiated, NOS: ICD-O-3.2 prints no such term and Rule J word order (p. 24)
   reaches 8020/3; the controller built it without waiting for the report's open point 4. The hint
   adds 8082/3 to the Rule K order. The 8070/3 and 8010/3 options gain upgrade lines; 8010/3 for a
   report that says only "nasopharyngeal carcinoma" awaits the registrar (registrar review A3,
   Q18).
8. np_ihc: the evidence's rule 3 reads "p40" negative while the panel declares "p40 or p63". The
   rule reads the declared marker. Under first-match-wins the result is the same: a positive "p40 or
   p63" with a positive pan-cytokeratin fires rule 1 or rule 2 before rule 3. Marker names are
   capitalised as the screen shows them. The hint adds that a file with a NUT immunostain or a NUTM1
   result is answered on the NUT carcinoma option (evidence data gap 5: the panel cannot exclude NUT
   carcinoma; Luo 2025, p. 7 makes the NUT stain decisive). The fallback stays 8020/3.
9. np_salivary: adds "Myoepithelial carcinoma, or malignant mixed tumour of salivary gland type",
   a referral to Group XII. The evidence's conflicts row 5 records that ICCC-2017 places 8982/3 and
   8940/3 in XIIa4 at every site; iccc_status confirms Group XII at C11.0-C11.9. Without it the
   clerk's next step, the picker, holds neither code.
10. np_not_malignant: the six lines are the evidence's; each exclusion's reason is the common
   wording with the ICD-O-3.2 Preferred term, and the common catch-all line is added.
11. np_deposit: the common deposit_node (D10). The evidence's "carcinoma or melanoma of another
   organ" option (next site_capture, recapture) is the hint's instruction to go back to the site step
   while SELF_REFERRAL is False; its "primary not known" option is the common carcinoma-of-unknown-
   primary hop to un_histology at C80.9. The hint gains the evidence's sentence on an oropharyngeal
   carcinoma that extends into the nasopharynx (ICCR p. 15), appended after deposit_node() returns.
12. np_carcinoma_other becomes np_picker (D2). Labels are ICD-O-3.2 Preferred terms; search_terms
   the live synonyms and related terms. The evidence's label "Low-grade nasopharyngeal papillary
   adenocarcinoma" and its recognition aid (thyroid transcription factor 1 positive, thyroglobulin
   and PAX8 negative; Badoual p. 6) are not shown: the picker lists 8260/3 as Papillary
   adenocarcinoma, NOS. The build report lists the label and aid for the alias layer. 8551/3 (an [obs]
   Preferred term) is not offered (D3). The standing-rule-3 codes are D11 picker entries: 8240/3 and
   8249/3 (the evidence's picker) and 8941/3 and 8147/3 (the evidence's conflicts row 7 names them
   at C11.0-C11.9; np_salivary's "another salivary gland-type carcinoma" reaches the picker). The
   evidence's picker hint sentences (an organ-named term describes a deposit, Rule H; two grades of a
   neuroendocrine tumour take the higher, Rule G) are appended to the common hint after make_tree().
13. Not built from the evidence: 8000/3 and 8001/3 as codes (D7, D8: Group XII referrals), 8085/3
   and 8086/3 (the evidence offers them at the oropharynx only), sialoblastoma (ICD-O-3.2 has no
   /3 term at 8974), and a site_resolution node for Rule C (no evidence node proposes one).

Registrar questions the evidence raised (XIc_nasopharynx.md, "Registrar questions" 2 and 3) stay
open; the defaults above apply until they are answered (docs/group_11_registrar_review.md A1 Q17,
A3 Q18). Questions 1 and 4 concern the oropharynx.
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, aid, cyto, cyto_carcinoma_nos, deposit_node,
                            evidence_gate, excl, go, ihc_node, make_tree, named, node, nonrep,
                            not_malignant_node, nut_nodes, rec, refer, refer_germ_cell,
                            refer_leukaemia, refer_lymphoma, refer_other_named, refer_sarcoma,
                            rule, tail_options, term)

TREE_ID = "g11_nasopharynx"
P = "np_"
WHERE = "the nasopharynx"
EVIDENCE = "XIc_nasopharynx"


def n(name: str) -> str:
    return P + name


# The first type-screen option's code, named by its ICD-O-3.2 Preferred term in the reasons of the
# lymphoepithelial and undifferentiated options (registrar_A1ab_rules.md C1 and C2).
NK_SCC = "%s (8072/3)" % term("8072", "3")


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Badoual p. 6 "NPC is a malignant mucosal epithelial neoplasm usually with evidence of squamous
# differentiation"; Badoual p. 8 "squamous cell differentiation separated by a dense infiltrate of
# lymphocytes and plasma cells"; Pfister p. 14 "Sialoblastoma Nasopharyngeal carcinoma".
AID_NPC = ("Reports describe a carcinoma of the nasopharyngeal lining, usually with squamous "
           "features, often in sheets among many lymphocytes and plasma cells.")
# ICCR p. 11 "appear poorly-differentiated morphologically due to their lymphoepithelial or
# non-keratinising morphology".
AID_POORLY = ("Epstein-Barr virus-positive nasopharyngeal carcinoma often reads as poorly "
              "differentiated because of its non-keratinising, lymphoepithelial look.")
# ICCR p. 11 "appear poorly-differentiated morphologically due to their lymphoepithelial or
# non-keratinising morphology"; Badoual p. 8 "squamous cell differentiation separated by a dense
# infiltrate of lymphocytes and plasma cells"; Badoual p. 8 "positive in most cases of NK-NPC but
# gives variable results in K-NPC".
AID_NONKERATINISING = ("Reports often call it poorly differentiated or undifferentiated and describe "
                       "sheets of tumour cells among many lymphocytes and plasma cells; "
                       "Epstein-Barr virus (EBER) is usually positive.")
# Badoual p. 8 "Keratinizing SCC (K-NPC) does not differ from other keratinizing HNSCC".
AID_KERATINISING = ("Reports describe a keratinising squamous cell carcinoma like those elsewhere "
                    "in the head and neck.")
# Badoual p. 8 "may have some cytologic variations or lymphoepithelial features".
AID_OLDER = ("Older reports use these names for nasopharyngeal carcinoma with many lymphocytes "
             "among the tumour cells.")
# Badoual p. 6 "It is a benign polypoid lesion arising from the lateral wall of the nasopharynx";
# "classify this entity as a hamartomatous (non-neoplastic) process"; "usually occurs in a
# pediatric population".
AID_HAIRY_POLYP = ("A hairy polyp is a benign polyp of the lateral nasopharyngeal wall; a salivary "
                   "gland anlage tumour is a hamartoma of infancy.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence np_document_inventory, np_clinical, np_imaging, np_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    lymphoma_cyto = refer_lymphoma(WHERE)
    lymphoma_cyto["label"] = "Cytology names a lymphoma"
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this nasopharyngeal tumour?",
        # Evidence np_document_inventory hint; ICCR p. 15 "EBV serology may also be a clinically
        # useful post-treatment surveillance option". Rule C: Rules p. 5 "Use subcategory '.8' when
        # a single tumor overlaps the boundaries of two or more" and "C14.8 Overlapping lesion of
        # lip, oral cavity and pharynx" (evidence rules_a_to_k C; departure 1).
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. An Epstein-Barr virus blood test "
              "does not establish the tumour: a file with imaging and an Epstein-Barr virus blood "
              "test belongs with imaging. A tumour that overlaps the nasopharynx and the "
              "oropharynx, with no stated origin, is recorded at C14.8 (WHO coding Rule C): go "
              "back to the site step."),
        tier_labels={
            # ICCR p. 15 "EBV serology may also be a clinically useful post-treatment surveillance
            # option".
            "imaging": "An imaging report, with or without an Epstein-Barr virus blood test - no "
                       "tissue",
            "cytology": "A cytology report, such as a fine-needle aspirate - no histology report",
            # ICCR p. 10 "Epstein-Barr virus (EBV) status (generally by EBER in situ
            # hybridisation) should be assessed".
            "histology": "A histology report, with or without stains or Epstein-Barr virus "
                         "encoded RNA (EBER) in situ hybridisation",
        },
        cytology=[
            # Evidence np_cytology option 1. Badoual p. 6 "usually with evidence of squamous
            # differentiation".
            cyto("Cytology names squamous cell carcinoma", "8070",
                 note="Evidence np_cytology option 1."),
            # Evidence np_cytology option 2; icdo32.sqlite 8020/3 Related "Carcinoma, poorly
            # differentiated, NOS".
            cyto("Cytology names a poorly differentiated or undifferentiated carcinoma", "8020",
                 "ICD-O-3.2 gives Carcinoma, poorly differentiated, NOS as a related term of this "
                 "code.", note="Evidence np_cytology option 2."),
            cyto_carcinoma_nos(note="Evidence np_cytology option 3 ('Cytology names a carcinoma "
                                    "with no type')."),
            # Evidence np_cytology option 5. Badoual p. 5 "nasopharyngeal lymphomas account for
            # 15% of all head and neck lymphomas".
            lymphoma_cyto,
        ],
        note="Evidence np_document_inventory, np_clinical, np_imaging and np_cytology (departures "
             "1 to 3 in the module docstring).")


# ------------------------------------------------------------------------------------------
# Histology (evidence np_histology)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # Badoual p. 6 "NPC is a malignant mucosal epithelial neoplasm usually with evidence of
        # squamous differentiation"; Pfister p. 14 "Sialoblastoma Nasopharyngeal carcinoma". D1:
        # paediatric; the code needs the type answer.
        aid(go("Nasopharyngeal carcinoma, or squamous cell carcinoma of the nasopharynx, including "
               "the older names lymphoepithelioma and undifferentiated carcinoma of "
               "nasopharyngeal type", n("npc_type"),
               note="D1 (Pfister 2022 Table 3, p. 14). Departure 6: the older names lead to the "
                    "type screen."), AID_NPC),
        # Pfister p. 14 "Malignant Mucoepidermoid carcinoma Acinic cell carcinoma Sialoblastoma";
        # ICCR p. 10 "applies only to minor salivary carcinomas arising at these specific sites".
        go("A salivary gland-type carcinoma, such as mucoepidermoid carcinoma or acinic cell "
           "carcinoma", n("salivary"),
           note="D1: mucoepidermoid and acinic cell carcinoma are paediatric (Pfister 2022 Table 3, "
                "p. 14)."),
        # ICCR p. 11 "appear poorly-differentiated morphologically due to their lymphoepithelial or
        # non-keratinising morphology".
        aid(go("Carcinoma, poorly differentiated or undifferentiated, and the report names no type",
               n("ihc"),
               note="Evidence np_histology option 2: the stain panel, whose fallback records "
                    "8020/3 when no stain is reported."), AID_POORLY),
    ] + tail_options(
        P, "mucosa", where=WHERE, nut=True,
        # Badoual p. 6 "They can be either benign or borderline".
        not_malignant_label="A benign lesion, carcinoma in situ or dysplasia, with no invasive "
                            "tumour",
        referrals=[
            # Badoual p. 5 "nasopharyngeal lymphomas account for 15% of all head and neck
            # lymphomas"; "NK/T cell lymphomas are mainly found in the nasopharynx". ICCC-2017:
            # 9680 at C11 -> IIb2.
            refer_lymphoma(WHERE),
            refer_leukaemia(WHERE),
            # ICCR p. 4 "sarcomas, and mucosal melanomas are not included". ICCC-2017: 8900-8920
            # at C11 -> IXa.
            refer_sarcoma(WHERE, label="Rhabdomyosarcoma, or another soft tissue sarcoma"),
            # Evidence conflicts row 6: 9084/3 at C11 -> Xb2.
            refer_germ_cell(WHERE),
            refer_other_named(),
        ],
        extra_referrals=[
            # Badoual p. 5 "Chordoma, which typically occurs in the clivus (base of the skull)".
            # ICCC-2017: 9370/3 -> VIIId2 at every site (evidence conflicts row 3).
            refer("Chordoma", 8,
                  "Chordoma begins in the bone of the skull base, not in the nasopharynx. It is "
                  "coded with the malignant bone tumours (ICCC-3 Group VIII) at its primary bone "
                  "site. Code the case from the Group VIII (bone tumours) tree.",
                  recapture=True,
                  note="Evidence np_histology option 8. recapture_site: the clivus (C41.0) is the "
                       "primary, not C11."),
            # Badoual p. 5 "Craniopharyngioma is described in the chapter on nasal cavity,
            # paranasal sinuses, and skull base"; "ectopic pituitary adenoma is covered in the
            # chapter on neuroendocrine neoplasms". ICCC-2017: 9350-9352 -> IIIe2, 8270-8281 ->
            # IIIe1 at every site, behaviours 0, 1 and 3 (evidence conflicts row 4).
            refer("Craniopharyngioma, or a pituitary neuroendocrine tumour or pituitary adenoma",
                  3,
                  "Craniopharyngioma and pituitary tumours, benign ones included, are coded in "
                  "ICCC-3 Group III (central nervous system and miscellaneous intracranial and "
                  "intraspinal neoplasms). Code the case from the Group III tree.",
                  note="Evidence np_histology option 9."),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence np_histology hint. ICCR p. 10 "still refers to them by histologic type"; ICCR
        # p. 15 "They are EBV (EBER) negative and p16 positive".
        "Use the report's own term. At the nasopharynx the code follows the histologic type: an "
        "Epstein-Barr virus (EBER) or p16 result does not change it.",
        opts, [],
        "Evidence np_histology (departures 4 to 6). D1: the paediatric entities are "
        "nasopharyngeal carcinoma, NUT carcinoma, mucoepidermoid carcinoma and acinic cell "
        "carcinoma (Pfister 2022 Table 3, p. 14). Every other carcinoma code ICCC-2017 places in "
        "XIc at C11 is a picker entry (D2).")


def npc_type():
    return node(
        n("npc_type"), "histology_subclassification", 4, "Nasopharyngeal carcinoma type",
        "Which type of nasopharyngeal carcinoma does the report name?",
        # Evidence np_npc_type hint. Rules p. 3 "use the numerically higher code number if the
        # diagnosis of a single tumor". Registrar ruling of 8 October 2026 on review A1 (a)(b),
        # docs/group_11_evidence/registrar_A1ab_rules.md C3: 8082/3 joins the Rule K order (ICD-O-3.1
        # Rule K, p. 24). The terms are the ICD-O-3.2 Preferred terms, read by term().
        "When the report names two of these types, pick the higher code (WHO coding Rule K): "
        "%s (8083/3), then %s (8082/3), then %s (8072/3), then %s (8071/3). An "
        "Epstein-Barr virus (EBER) result does not change the type."
        % (term("8083", "3"), term("8082", "3"), term("8072", "3"), term("8071", "3")),
        [
            # ICCR p. 11 "Non-keratinising squamous cell carcinoma 8072/3"; Badoual p. 8
            # "Nonkeratinizing SCC (NK-NPC) is the most common histologic subtype".
            aid(named("Non-keratinising squamous cell carcinoma (non-keratinising nasopharyngeal "
                      "carcinoma), differentiated or undifferentiated subtype", "8072",
                      "ICD-O-3.2 gives Squamous cell carcinoma, nonkeratinizing, NOS as a synonym "
                      "of this code, and the WHO classification codes non-keratinising "
                      "nasopharyngeal carcinoma to it.",
                      note="Evidence np_npc_type option 1. D1: nasopharyngeal carcinoma is "
                           "paediatric (Pfister 2022 Table 3, p. 14)."), AID_NONKERATINISING),
            # ICCR p. 11 "Keratinising squamous cell carcinoma 8071/3"; Badoual p. 8.
            aid(named("Keratinising squamous cell carcinoma (keratinising nasopharyngeal "
                      "carcinoma)", "8071", note="Evidence np_npc_type option 2."),
                AID_KERATINISING),
            # ICCR p. 11 "Basaloid squamous cell carcinoma 8083/3"; Badoual p. 8 "Basaloid SCC does
            # not differ in histologic appearance from other locations".
            named("Basaloid squamous cell carcinoma", "8083",
                  note="Evidence np_npc_type option 3."),
            # Registrar ruling of 8 October 2026 on review A1 (a)(b), applied by the WHO ICD-O-3
            # coding Rules A to K (docs/group_11_evidence/registrar_A1ab_rules.md, C1): the code
            # follows the term the report uses (ICD-O-3.1 section 4.3.3, p. 21; Rule H, p. 23 for
            # Schmincke tumor, which ICD-O-3.2 prints with C11._). ICD-O-3.2 prints Lymphoepithelioma,
            # Lymphoepithelioma-like carcinoma and Schmincke tumor under 8082/3 (icdo32.sqlite);
            # this option recorded 8072/3 before the ruling. Badoual p. 8 "may have some cytologic
            # variations or lymphoepithelial features" (the aid).
            aid(named("Lymphoepithelioma, lymphoepithelial carcinoma, lymphoepithelioma-like "
                      "carcinoma or Schmincke tumour", "8082",
                      "ICD-O-3.2 lists Lymphoepithelioma, Lymphoepithelioma-like carcinoma and "
                      "Schmincke tumor as terms of this code, and the code follows the term the "
                      "report uses. A report that says non-keratinising squamous cell carcinoma "
                      "is recorded as %s on the first option." % NK_SCC,
                      note="Registrar ruling 8 October 2026 (review A1 (a), Q17), "
                           "registrar_A1ab_rules.md C1: ICD-O-3.1 section 4.3.3, p. 21 and Rule H, "
                           "p. 23. Departure 7."), AID_OLDER),
            # Registrar ruling of 8 October 2026 on review A1 (a)(b), registrar_A1ab_rules.md C2,
            # built on the controller's decision (open point 4 not held). ICD-O-3.2 prints no term
            # "undifferentiated carcinoma of nasopharyngeal type" (no term of ICD-O-3.2 holds the
            # word nasopharyngeal) and no reordering of its words reaches a printed term (ICD-O-3.1
            # Rule J, p. 24). Rule J word order gives "Carcinoma, undifferentiated", printed as
            # 8020/3 Carcinoma, undifferentiated, NOS; ICCC-2017 places 8020/3 in XIc at C11.0-C11.9.
            # Rule G, p. 22: undifferentiated is a grade word, integral to the printed 8020/3 term.
            # This option recorded 8072/3 before the ruling.
            named("Undifferentiated carcinoma of nasopharyngeal type", "8020",
                  "ICD-O-3.2 prints no term for undifferentiated carcinoma of nasopharyngeal "
                  "type. Reordering its words (WHO coding Rule J) gives Carcinoma, "
                  "undifferentiated, NOS, the term printed at this code. A report that says "
                  "non-keratinising squamous cell carcinoma, undifferentiated subtype, is "
                  "recorded as %s on the first option." % NK_SCC,
                  note="Registrar ruling 8 October 2026 (review A1 (a), Q17), "
                       "registrar_A1ab_rules.md C2: ICD-O-3.1 Rule J, p. 24; Rule G, p. 22."),
            # Badoual p. 6 "NPC is a malignant mucosal epithelial neoplasm usually with evidence of
            # squamous differentiation".
            named("Squamous cell carcinoma, and the report names no type", "8070",
                  upgrade="The report does not name the type of squamous cell carcinoma. A report "
                          "that names it (non-keratinising, keratinising or basaloid) gives that "
                          "type's own code: go back and take the option that names it.",
                  note="Evidence np_npc_type option 4."),
            # Badoual p. 6 "usually with evidence of squamous differentiation". Registrar review
            # A3, Q18: 8010/3 or 8070/3.
            named("Nasopharyngeal carcinoma, and the report names no type and does not call it "
                  "squamous", "8010",
                  "The report does not state the squamous type. Whether a report that says only "
                  "nasopharyngeal carcinoma records this code or Squamous cell carcinoma, NOS "
                  "(8070/3) awaits the registrar's decision.",
                  upgrade=TYPE_NOT_STATED,
                  note="Evidence np_npc_type option 5; evidence registrar question 3 (registrar "
                       "review A3, Q18)."),
        ], [],
        "Evidence np_npc_type (departure 7). ICCR Table 2 (p. 11) lists the WHO nasopharyngeal "
        "carcinomas: non-keratinising 8072/3, keratinising 8071/3, basaloid 8083/3 and low-grade "
        "nasopharyngeal papillary adenocarcinoma 8260/3 (a picker entry). D1: nasopharyngeal "
        "carcinoma is paediatric and its code depends on the type.")


def salivary():
    return node(
        n("salivary"), "histology_subclassification", 4, "Salivary gland-type carcinoma",
        "Which salivary gland-type carcinoma does the report name?",
        # Evidence np_salivary hint. ICCR p. 10 "applies only to minor salivary carcinomas arising
        # at these specific sites"; "Salivary gland carcinomas are classified based on 5th edition
        # WHO Classification".
        "These carcinomas arise in the minor salivary glands of the nasopharynx and carry the same "
        "names as in the major salivary glands.",
        [
            # Pfister p. 14 "Malignant Mucoepidermoid carcinoma Acinic cell carcinoma".
            named("Mucoepidermoid carcinoma", "8430",
                  note="Evidence np_salivary option 1. D1: Pfister 2022 Table 3, p. 14."),
            # Pfister p. 14 "Malignant Mucoepidermoid carcinoma Acinic cell carcinoma";
            # icdo32.sqlite 8550/3 Synonym "Acinic cell adenocarcinoma".
            named("Acinic cell carcinoma", "8550",
                  "ICD-O-3.2 gives Acinic cell adenocarcinoma as a synonym of this code.",
                  note="Evidence np_salivary option 2. D1: Pfister 2022 Table 3, p. 14."),
            # Evidence conflicts row 5: "Myoepithelial carcinoma (8982/3), malignant mixed tumour
            # (8940/3) and sialoblastoma (8974) are XIIa4 at every site". Departure 9.
            refer("Myoepithelial carcinoma, or malignant mixed tumour of salivary gland type", 12,
                  "ICCC-3 places Myoepithelial carcinoma (8982/3) and Mixed tumor, malignant, NOS "
                  "(8940/3) in Group XII (other and unspecified malignant neoplasms) at the "
                  "nasopharynx, not in Group XI. Code the case from the Group XII tree.",
                  note="Departure 9. ICCC-2017 range XIIa4 holds 8982/3 and 8940/3 at "
                       "C11.0-C11.9 (iccc_status other:XII)."),
            go("Another salivary gland-type carcinoma - type its name to find it", n("picker"),
               note="Evidence np_salivary option 3 (to np_carcinoma_other, built as the D2 "
                    "picker)."),
        ], [],
        "Evidence np_salivary (departure 9). D1: mucoepidermoid and acinic cell carcinoma are "
        "paediatric; the other salivary gland-type carcinomas are picker entries, 8941/3 and "
        "8147/3 among them as D11 codes.")


def ihc():
    pan_ck = "Pan-cytokeratin"
    p40 = "p40 or p63"
    eber = "Epstein-Barr virus encoded RNA (EBER) in situ hybridisation"
    neuro = "Chromogranin, synaptophysin or insulinoma-associated protein 1 (INSM1)"
    return ihc_node(
        P,
        [
            {"group_label": "Epithelial and squamous markers", "markers": [pan_ck, p40]},
            {"group_label": "Epstein-Barr virus", "markers": [eber]},
            {"group_label": "Neuroendocrine markers", "markers": [neuro]},
        ],
        [
            rule([pan_ck, p40, eber], "8072",
                 "Pan-cytokeratin, p40 or p63, and Epstein-Barr virus encoded RNA are positive: "
                 "the non-keratinising nasopharyngeal carcinoma pattern (Badoual 2022, p. 8; "
                 "International Collaboration on Cancer Reporting oropharynx and nasopharynx "
                 "dataset, p. 15). %s" % rec("8072"),
                 note="Evidence ihc_rules 1. Badoual p. 8 'These carcinomas show positive staining "
                      "for pan-cytokeratin', 'differentiation of squamous cells can be "
                      "demonstrated by positivity of p40 and p63', 'positive in most cases of "
                      "NK-NPC but gives variable results in K-NPC'; ICCR p. 15 'Epstein-Barr virus "
                      "(EBV) is associated with the non-keratinising types of nasopharyngeal "
                      "carcinomas'; ICCR p. 11."),
            rule([pan_ck, p40], "8070",
                 "Pan-cytokeratin and p40 or p63 are positive, and Epstein-Barr virus encoded RNA "
                 "is not: a squamous cell carcinoma whose type the stains do not name (Badoual "
                 "2022, p. 8). %s" % rec("8070"),
                 negative=[eber],
                 note="Evidence ihc_rules 2. Badoual p. 8 'differentiation of squamous cells can "
                      "be demonstrated by positivity of p40 and p63', 'positive in most cases of "
                      "NK-NPC but gives variable results in K-NPC'; ICCR p. 15 'They are EBV "
                      "(EBER) negative and p16 positive'."),
            rule([neuro, pan_ck], "8246",
                 "A neuroendocrine marker and pan-cytokeratin are positive, and p40 or p63 is not: "
                 "the neuroendocrine carcinoma pattern (Badoual 2022, p. 3). %s" % rec("8246"),
                 negative=[p40],
                 note="Evidence ihc_rules 3 (departure 8: the rule reads the declared marker 'p40 "
                      "or p63'). Badoual p. 3 'expression of neuroendocrine markers (chromogranin, "
                      "synaptophysin or INSM1) is mandatory for the diagnosis', 'P40 expression "
                      "has not been observed in neuroendocrine carcinomas'; ICCR p. 15 'positive "
                      "reaction for neuroendocrine markers (synaptophysin, chromogranin, "
                      "INSM1)'."),
        ],
        fallback="8020",
        fallback_reason=("The stains do not establish the carcinoma's type. %s ICD-O-3.2 gives "
                         "Carcinoma, poorly differentiated, NOS as a related term of this code."
                         % rec("8020")),
        # Evidence np_ihc hint. Badoual p. 8 "EBV in situ hybridization for viral RNA is
        # recommended"; "its presence cannot be demonstrated in half of the NPC biopsies". NUT
        # sentence: departure 8 (Luo 2025, p. 7, in NUT_carcinoma.json).
        hint="The histology report calls the tumour a poorly differentiated or undifferentiated "
             "carcinoma without naming its type. Answer the Epstein-Barr virus question from "
             "Epstein-Barr virus encoded RNA (EBER) in situ hybridisation. A latent membrane "
             "protein 1 (LMP1) stain misses about half of these tumours. Answer 'Not done or not "
             "readable' for a stain the report does not mention. A file that reports a NUT "
             "immunostain or a NUTM1 gene test is answered on the NUT carcinoma option of the "
             "histology screen, not here.",
        note="Evidence np_ihc and ihc_rules 1-4 (departure 8). Fallback 8020/3: evidence "
             "ihc_rules 4, ICCR p. 11 'appear poorly-differentiated morphologically due to their "
             "lymphoepithelial or non-keratinising morphology'.")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # ICCR p. 2 "Only applicable for HPV-independent oropharyngeal and EBV-independent
            # nasopharyngeal tumours"; Rules p. 2 "If the pathologist states that the behavior
            # differs from the usual behavior".
            excl("Carcinoma in situ, with no invasive carcinoma", "8070", "2",
                 what="squamous carcinoma in situ"),
            # ICCR p. 2 "High grade dysplasia is synonymous with moderate/severe dysplasia";
            # Badoual p. 9 "intermediate low- and high-grade dysplastic lesions".
            excl("High grade, moderate or severe dysplasia, with no invasive carcinoma", "8077",
                 "2", what="high grade squamous dysplasia",
                 extra="ICD-O-3.2 gives Squamous dysplasia, high grade as a synonym of this code."),
            # Badoual p. 5 "Nasopharyngeal angiofibroma is covered in the chapter on the nasal
            # cavity".
            excl("Angiofibroma (juvenile or nasopharyngeal angiofibroma)", "9160", "0",
                 what="an angiofibroma",
                 extra="ICD-O-3.2 gives Juvenile angiofibroma as a synonym of this code."),
            # Pfister p. 14 "Nasopharyngeal dermoid".
            excl("Dermoid (nasopharyngeal dermoid)", "9084", "0", what="a dermoid",
                 extra="ICD-O-3.2 gives Dermoid, NOS as a synonym of this code."),
            # Pfister p. 14 "Pleomorphic adenoma Malignant".
            excl("Pleomorphic adenoma", "8940", "0", what="a pleomorphic adenoma"),
            # Badoual p. 6 "It is a benign polypoid lesion arising from the lateral wall of the
            # nasopharynx"; "classify this entity as a hamartomatous (non-neoplastic) process".
            aid(nonrep("Hairy polyp, or salivary gland anlage tumour",
                       "Not registrable. The report describes a benign lesion, which ICD-O-3.2 "
                       "gives no code.",
                       note="Evidence np_not_malignant option 6."), AID_HAIRY_POLYP),
        ],
        where=WHERE,
        note="The six lines of evidence np_not_malignant (departure 10).")


def deposit():
    d = deposit_node(P, where=WHERE)
    # ICCR p. 15 "this may be an oropharyngeal primary tumour that is secondarily involving the
    # nasopharynx" (evidence np_deposit hint; departure 11).
    d["hint"] += (" A carcinoma of the oropharynx can extend into the nasopharynx; it is coded at "
                  "the oropharynx.")
    return d


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
# Evidence np_carcinoma_other hint. Rules p. 2 "ascertain that the neoplasm at the site mentioned is
# not a metastasis" (Rule H) and "code to the higher grade" (Rule G); ICCR p. 11 "NETs are
# separated into grades (1, 2, and 3) based on mitotic rate". Departure 12.
PICKER_HINT_EXTRA = (" A term that names another organ, such as breast, lung or thyroid, describes "
                     "a deposit: go back and take the deposit option. When the report gives two "
                     "grades of a neuroendocrine tumour, pick the higher.")


def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), npc_type(), salivary(), ihc()] + nut_nodes(P) + [
        not_malignant(), deposit()]
    tree = make_tree(
        TREE_ID, nodes,
        subtype_screens=(n("npc_type"), n("salivary")),
        # Standing rule 3 (D11): no ICCC-2017 range holds these at C11.0-C11.9. 8240/3 and 8249/3:
        # the evidence's picker (author_note; ICCR p. 4 and p. 11, neuroendocrine tumours of the
        # nasopharynx). 8941/3 and 8147/3: the evidence's conflicts row 7 names them at C11 as
        # salivary gland-type carcinomas (departure 12).
        d11=("8147", "8240", "8249", "8941"))
    for nd in tree["nodes"]:
        if nd["node_id"] == n("picker"):
            nd["hint"] += PICKER_HINT_EXTRA
    return tree


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
_IHC = ["Histology", "IHC"]
DECISIONS = {
    "8072/3": ("D1, D5", EVIDENCE,
               "Non-keratinising nasopharyngeal carcinoma (ICCR Table 2, p. 11; Pfister 2022 Table "
               "3) on the type screen, and from the stain panel when pan-cytokeratin, p40 or p63 "
               "and Epstein-Barr virus encoded RNA are positive. A report that says "
               "non-keratinising squamous cell carcinoma, undifferentiated subtype, takes it on "
               "the type screen (WHO coding Rule K, ICD-O-3.1 p. 24); the older names "
               "lymphoepithelioma and Schmincke tumour record 8082/3 and undifferentiated "
               "carcinoma of nasopharyngeal type records 8020/3 (registrar ruling of 8 October "
               "2026 on review A1, Q17).",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["Pan-cytokeratin", "p40 or p63",
                                         "Epstein-Barr virus encoded RNA (EBER) in situ "
                                         "hybridisation"]}),
    "8082/3": ("D1", EVIDENCE,
               "Lymphoepithelial carcinoma of the nasopharynx on the type screen, for the terms "
               "lymphoepithelioma, lymphoepithelioma-like carcinoma and Schmincke tumor, which "
               "ICD-O-3.2 prints under this code (registrar ruling of 8 October 2026 on review "
               "A1, Q17: the WHO ICD-O-3 coding Rules A to K; ICD-O-3.1 section 4.3.3, p. 21 and "
               "Rule H, p. 23)."),
    "8071/3": ("D1", EVIDENCE,
               "Keratinising nasopharyngeal carcinoma on the type screen (ICCR Table 2, p. 11)."),
    "8083/3": ("D1, D5", EVIDENCE,
               "Basaloid squamous cell carcinoma of the nasopharynx on the type screen (ICCR Table "
               "2, p. 11); the higher code by Rule K when the report names two types."),
    "8070/3": ("D1, D8", EVIDENCE,
               "Nasopharyngeal carcinoma reported as squamous cell carcinoma with no type, on the "
               "type screen; at basis 5 when cytology names squamous cell carcinoma; and from the "
               "stain panel when pan-cytokeratin and p40 or p63 are positive and Epstein-Barr "
               "virus encoded RNA is not.",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["Pan-cytokeratin", "p40 or p63"]}),
    "8010/3": ("D1, D8", EVIDENCE,
               "Nasopharyngeal carcinoma whose type the report does not state and does not call "
               "squamous, on the type screen (registrar review A3, Q18: 8010/3 or 8070/3); at "
               "basis 5 when cytology names a carcinoma without its type."),
    "8020/3": ("D8", EVIDENCE,
               "Poorly differentiated or undifferentiated carcinoma whose type the report does not "
               "name: the stain panel's fallback at basis 7, and basis 5 when cytology names a "
               "poorly differentiated or undifferentiated carcinoma. ICD-O-3.2 gives Carcinoma, "
               "poorly differentiated, NOS as a related term of 8020/3. Also undifferentiated "
               "carcinoma of nasopharyngeal type on the type screen, which ICD-O-3.2 does not "
               "print: WHO coding Rule J word order reaches this code (registrar ruling of 8 "
               "October 2026 on review A1, Q17)."),
    "8246/3": ("D2", EVIDENCE,
               "Neuroendocrine carcinoma of the nasopharynx from the stain panel (a neuroendocrine "
               "marker and pan-cytokeratin positive, p40 or p63 negative; Badoual 2022, p. 3) and "
               "in the picker.",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["Chromogranin, synaptophysin or insulinoma-associated "
                                         "protein 1 (INSM1)", "Pan-cytokeratin"]}),
    "8430/3": ("D1", EVIDENCE,
               "Mucoepidermoid carcinoma of a nasopharyngeal minor salivary gland, on the salivary "
               "gland-type screen (Pfister 2022 Table 3, p. 14)."),
    "8550/3": ("D1", EVIDENCE,
               "Acinic cell carcinoma of a nasopharyngeal minor salivary gland, on the salivary "
               "gland-type screen (Pfister 2022 Table 3, p. 14); ICD-O-3.2 gives Acinic cell "
               "adenocarcinoma as a synonym of 8550/3."),
    "8023/3": ("D12, D15", EVIDENCE,
               "NUT carcinoma at the nasopharynx (Pfister 2022 Table 3, p. 14) on the NUT "
               "carcinoma screens: basis 8 with a NUTM1 result, basis 7 otherwise. New in "
               "ICD-O-3.2 and absent from REDCap's XIc list: the REDCap-side list (standing rule "
               "16)."),
    "8240/3": ("D2, D11", EVIDENCE,
               "Neuroendocrine tumour of the nasopharynx, a picker entry. No ICCC-2017 range holds "
               "8240 at C11; standing rule 3 keeps it in Group XI. The evidence asks for subgroup "
               "XIc at C11, where D11 gives the entry's default subgroup."),
    "8249/3": ("D2, D11", EVIDENCE,
               "Neuroendocrine tumour, grade 2 or grade 3, of the nasopharynx, a picker entry. No "
               "ICCC-2017 range holds 8249 at C11; standing rule 3 keeps it in Group XI. The "
               "evidence asks for subgroup XIc at C11, where D11 gives the entry's default "
               "subgroup."),
    "8941/3": ("D2, D11", EVIDENCE,
               "Carcinoma ex pleomorphic adenoma of a nasopharyngeal minor salivary gland, a "
               "picker entry. No ICCC-2017 range holds 8941 at C11; standing rule 3 keeps it in "
               "Group XI (evidence conflicts row 7)."),
    "8147/3": ("D2, D11", EVIDENCE,
               "Basal cell adenocarcinoma of a nasopharyngeal minor salivary gland, a picker "
               "entry. No ICCC-2017 range holds 8147 at C11; standing rule 3 keeps it in Group XI "
               "(evidence conflicts row 7)."),
}
