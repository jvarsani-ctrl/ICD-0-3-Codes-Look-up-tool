"""g11_head_neck (prefix hn_): carcinomas of the lip, oral cavity, oropharynx, hypopharynx and pharynx,
nasal cavity, middle ear and sinuses, larynx and trachea (C00-C06, C09-C10, C12-C14, C30-C33), ICCC-3
subgroup XIf10.

Built from docs/group_11_evidence/XIf10_head_neck.json (the oral, laryngeal and sinonasal nodes) and the
oropharynx nodes of docs/group_11_evidence/XIc_nasopharynx.json (op_carcinoma_other, op_squamous_hpv),
with the builders in build/group11_common.py, in the shape of build/group11_organs/thyroid.py and
nasopharynx.py. Every option's label, code, behaviour, basis, reason and recognition aid comes from those
files unless a departure below says otherwise; the cite (file, PDF page, quotation) is the comment above
the option. File names in the comments are the evidence's own:
    Muller    XIf10-oral-cavity__Muller-2022.txt (Muller S, Tilakaratne WM. Head Neck Pathol
              2022;16:54-62, WHO 5th edition, oral cavity and mobile tongue)
    ICCR-Oral XIf10-oral-cavity__ICCR-Oral-Cavity-2nd.txt (Carcinomas of the Oral Cavity, 2nd edition,
              version 2.1, July 2024)
    Zidar     XIf10-larynx__Zidar-2022.txt (Zidar N, Gale N. Head Neck Pathol 2022;16:31-39, WHO 5th
              edition, hypopharynx, larynx, trachea)
    ICCR-Lx   XIf10-larynx__ICCR-Hypopharynx-Larynx-Trachea-2nd.txt (Carcinomas of the Hypopharynx,
              Larynx and Trachea, 2nd edition, version 2.0, July 2024)
    Thompson  XIf10-nasal-cavity__Thompson-2022.txt (Thompson LDR, Bishop JA. Head Neck Pathol
              2022;16:1-18, WHO 5th edition, nasal cavity, paranasal sinuses and skull base)
    ICCR-Nasal XIf10-nasal-cavity__ICCR-Nasal-Cavity-2nd.txt (Carcinomas of the Nasal Cavity and
              Paranasal Sinuses, 2nd edition)
    Badoual / ICCR-Op   XIc-nasopharynx__Badoual-2022.txt, XIc-nasopharynx__ICCR-Oropharynx-Nasopharynx-2nd.txt
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 section 4, printed pp. 14-28)

Nodes, in tree order:
    hn_document_inventory  document_inventory  evidence gate (evidence hn_oral/lx/sn_document_inventory)
    hn_clinical, hn_clinical_cytology  clinical_alias   (evidence hn_clinical)
    hn_imaging, hn_imaging_cytology    morphology_only  (evidence hn_imaging)
    hn_cytology            morphology_only     (evidence hn_cytology)
    hn_histology           histology_subclassification  (evidence hn_oral/lx/sn_histology, merged)
    hn_oropharynx_hpv      histology_subclassification  (evidence op_squamous_hpv)
    hn_squamous_type       histology_subclassification  (evidence hn_squamous_type and hn_sn_squamous_type)
    hn_salivary            histology_subclassification  (evidence hn_salivary)
    hn_mnti                histology_subclassification  (evidence hn_mnti)
    hn_ihc                 ihc_checklist        (evidence hn_ihc; lip, mouth, pharynx, larynx, trachea)
    hn_sn_ihc              ihc_checklist        (evidence hn_sn_ihc; nose and sinuses)
    hn_nut_result, hn_nut_basis, hn_nut_tests  histology_subclassification (D12, nut_nodes())
    hn_not_malignant       histology_subclassification  (evidence hn_oral/lx/sn_not_malignant, merged)
    hn_deposit             morphology_only      (D10; evidence hn_deposit)
    hn_picker              histology_subclassification  (D2; evidence hn_carcinoma_picker, op_carcinoma_other)

Departures from the evidence nodes, and why
-------------------------------------------
1. Three evidence trees become one (D14). The evidence drew an oral, a laryngeal and a sinonasal
   document_inventory and histology screen; the router gives a tree one entry node and the engine cannot
   filter options by site, so hn_histology merges them and names the organ in the label where a
   screen's options differ by organ (the oropharynx and the nose and sinuses). The three
   document_inventory nodes become the common one, which hands every histology report to hn_histology.
   Evidence data gap 4 (no WHO 5th edition source for the middle ear, C30.1) leaves C30.1 with the
   other sinonasal sites; the squamous screen below serves it.
2. Gate. The referral and imaging tiers recorded 8000/3 at basis 1 and 2. D7: ICCC-2017 range 143
   places 8000/3 in XIIb at every routed site, so each refers to Group XII with refer_code 8000. The
   escapes "An imaging report is in the file after all" (hn_clinical) and the two cytology escapes are
   replaced by the document checklist's own routes (group11_common departures). Cytology: "Cytology
   names a carcinoma with no type" is cyto_carcinoma_nos(); "Malignant cells ... no tumour type named"
   (8001/3, basis 5) refers to Group XII with refer_code 8001 (D8); "Cytology names melanoma" keeps its
   hop into the melanoma tree's cytology screen (me_cytology); the lymphoma line is a referral. No
   laboratory screen and no marker tier: the evidence's lab_tests give no test a diagnostic role at
   these sites, and Visser 2023 Table 4 has no row for them (evidence data gap 7). The hint adds WHO
   coding Rule C (Rules p. 5), which the evidence placed at the router's site capture: a tumour that
   overlaps two subsites with no stated origin takes the .8 subsite. The router is not this module's
   file.
3. hn_histology merges squamous cell carcinoma into two organ-labelled options (D14): the oropharynx,
   which asks the human papillomavirus question first (departure 4), and every other site, which goes
   to one squamous type screen (departure 5). The evidence's poorly-differentiated option splits in two
   for the same reason: the lip, mouth, pharynx, larynx and trachea read hn_ihc, the nose and sinuses
   read hn_sn_ihc, whose rules differ (departure 6). The sinonasal "Adenocarcinoma with no type named,
   or non-intestinal-type adenocarcinoma" option (8140/3) keeps its organ in the label. "Carcinoma,
   with no type named" (8010/3) is one option for all sites.
4. hn_oropharynx_hpv (evidence op_squamous_hpv, status "proposed: built only if the registrar rules
   oropharyngeal squamous cell carcinoma a paediatric option"). Built, as the brief for this tree
   asks, under the D1 exception: the code of an oropharyngeal squamous cell carcinoma depends on a
   further answer (human papillomavirus status), so it is an option, not a picker entry. 8085/3 and
   8086/3 are new in ICD-O-3.2 and absent from REDCap (the REDCap-side list, standing rule 16).
   The evidence's third option, "no human papillomavirus or p16 result in the report", recorded 8070/3
   directly; here it continues to hn_squamous_type, so a verrucous or basaloid oropharyngeal carcinoma
   with no virus result still reaches its subtype code. Its first answer on that screen records 8070/3.
5. hn_squamous_type merges hn_squamous_type and hn_sn_squamous_type: the codes are the same set; the
   sinonasal screen added a DEK::AFF2 carcinoma note to non-keratinising squamous cell carcinoma, a
   recognition aid on keratinising and non-keratinising carcinoma, and the sentence on a carcinoma
   arising in a sinonasal papilloma, which this screen carries. Carcinoma cuniculatum records 8051/3,
   the code the WHO tables give it (ICD-O-3.2 prints Verrucous carcinoma, NOS there; registrar review
   A18, Q110). "Another squamous type the report names" continues to hn_picker.
6. hn_ihc and hn_sn_ihc. D12 replaces the evidence's two NUT rules (NUTM1 rearrangement at basis 8, NUT
   immunostain at basis 7) with the NUT carcinoma option and its screens, as the nasopharynx tree did;
   the hints say a file reporting a NUT immunostain or a NUTM1 test is answered there. The sinonasal
   rule on loss of SMARCB1 or SMARCA4 staining (8044/3, SWI/SNF complex-deficient sinonasal
   carcinoma) is not built: ICD-O-3.2 prints 8044/3 as Small cell carcinoma, intermediate cell, so D4
   builds no code for the entity (registrar review A18, Q106) and no screen names it. The remaining rules
   keep the evidence's order, and the fallback stays 8020/3.
7. hn_salivary is a histology_subclassification, not the evidence's morphology_only (a node with
   coded branches and a hop is one the validator accepts either way). Its last option, "Another salivary
   gland-type carcinoma", went to sg_carcinoma_picker, the salivary tree's picker, whose list is valid at the
   salivary sites, not here; it goes to hn_picker. The evidence's conflicts row 11 records that
   ICCC-2017 places myoepithelial carcinoma (8982/3) and malignant mixed tumour (8940/3) in Group XII
   at every site, so the screen adds the same Group XII referral the nasopharynx tree carries.
8. hn_mnti is the evidence node. Its malignant answer refers to Group XII without a code: the tumour
   called malignant is 9363/3 in ICCC-2017 (XIIa6), and ICD-O-3.2 prints 9363 at behaviour 0 only
   (evidence code_currency; D6), so no reason names a /3 term.
9. hn_not_malignant merges the three evidence exclusion screens. Each exclusion's reason is the
   common wording with the ICD-O-3.2 Preferred term; the evidence's non-reportable lines (hamartomas,
   glomangiopericytoma, benign and reactive oral lesions) are kept. Squamous cell papilloma (8052/0) and
   the two intraepithelial grades appear once, with the sites in the label.
10. Referrals. The evidence's options for a malignant odontogenic tumour or jaw bone tumour (Group
   VIII, oral) and for chordoma or another skull-base or facial-bone tumour (Group VIII, sinonasal)
   are one option with recapture_site. Myeloid sarcoma (Group I, keeps its site) is the common
   leukaemia referral, which records C42.1 (check_leukaemia_referrals_record_marrow admits a
   site-keeping Group I referral on listed nodes only). Teratocarcinosarcoma joins the germ cell
   referral (Group X). Olfactory neuroblastoma and paraganglioma are Group IV referrals;
   chondrosarcoma of the laryngeal or tracheal cartilage is a Group IX referral; craniopharyngioma or
   meningioma is a Group III referral.
11. hn_deposit is the common deposit_node (D10) with the evidence's hint sentence appended.
12. hn_picker (D2) replaces hn_carcinoma_picker and op_carcinoma_other. Labels are the ICD-O-3.2
   Preferred terms; search_terms the live synonyms. The evidence's picker entries that name no code
   (teratocarcinosarcoma, olfactory neuroblastoma, myoepithelial carcinoma) are referrals above. 8044/3
   (SWI/SNF complex-deficient sinonasal carcinoma in the evidence's picker) appears only under its
   ICD-O-3.2 term, if ICCC-2017 places it in Group XI at every routed site, and no label names the WHO
   entity (D4). 8085/3 and 8086/3 are options (departure 4) and so leave the picker. The evidence's
   picker hint sentences (higher code for two types, higher grade for two neuroendocrine grades, a
   mixed neuroendocrine-non-neuroendocrine neoplasm recorded by its neuroendocrine part, an organ-named
   term describes a deposit) are appended after make_tree(). The evidence's Rule H list of codes left out
   of the picker (picker_left_out_rule_h) is not applied: D2 and validator rule 4 decide, as for the
   thoracic tree (thoracic departure 9); the build report lists the organ-specific codes the picker
   holds.
13. Not built from the evidence: 8000/3 and 8001/3 as codes (D7, D8: Group XII referrals), 8044/3 for
   SWI/SNF complex-deficient sinonasal carcinoma, 8483/3 for human papillomavirus-related
   multiphenotypic sinonasal carcinoma (ICD-O-3.2 holds no 8483), a code for sinonasal
   glomangiopericytoma and for congenital granular cell epulis (ICD-O-3.2 holds none), and a
   site_resolution node for Rule A, B or C (no evidence node proposes one).

Registrar questions the evidence raised (XIf10_head_neck.md; docs/group_11_registrar_review.md A18 Q106
and Q110) stay open; the defaults above apply until they are answered.
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, aid, cyto, cyto_carcinoma_nos, deposit_node,
                            evidence_gate, excl, go, ihc_node, make_tree, named, node, nonrep,
                            not_malignant_node, nut_nodes, rec, refer, refer_leukaemia,
                            refer_other_named, refer_sarcoma, rule, tail_options)

TREE_ID = "g11_head_neck"
P = "hn_"
WHERE = "the head and neck"
EVIDENCE = "XIf10_head_neck"
EVIDENCE_OP = "XIc_nasopharynx"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Zidar p. 4 "Verrucous carcinoma is a variant of well-differentiated SCC"; ICCR-Lx p. 12.
AID_VERRUCOUS = ("The report describes a well-differentiated squamous carcinoma without cytologic "
                 "features of malignancy, invading below the adjacent epithelium.")
# Zidar p. 4 "with prominent basaloid morphology and the presence of squamous differentiation".
AID_BASALOID = "The report describes prominent basaloid cells with squamous differentiation."
# Zidar p. 4 "composed of papillae covered by atypical stratified squamous or immature basaloid
# epithelium".
AID_PAPILLARY = "The report describes papillae covered by atypical squamous or basaloid epithelium."
# ICCR-Oral p. 8 "Spindle cell (sarcomatoid) squamous cell carcinoma 8074/3"; Zidar p. 4 "usually
# with a SCC component".
AID_SPINDLE = "The report describes spindle or pleomorphic cells, usually with a squamous carcinoma component."
# Zidar p. 5 "biphasic tumor showing both squamous and glandular differentiation".
AID_ADENOSQUAMOUS = "The report describes separate squamous and glandular components in one tumour."
# Zidar p. 5 "with prominent lymphoplasmacytic infiltration of the stroma".
AID_LYMPHOEPITHELIAL = ("The report describes a poorly differentiated squamous carcinoma with prominent "
                        "lymphoplasmacytic infiltration of the stroma.")
# Muller p. 6 "a rare well-differentiated locally destructive SCC with a unique burrowing invasive".
AID_CUNICULATUM = "The report describes burrowing, keratin-filled crypts of well-differentiated squamous carcinoma."
# Thompson p. 4 "separated into well, moderately and poorly differentiated categories"; "may be
# associated with a precursor SNP".
AID_KERATINISING = ("The report describes keratinising squamous carcinoma graded well, moderately or "
                    "poorly differentiated, sometimes arising in a sinonasal papilloma.")
# Thompson p. 4 "characterized by minimal to no keratinization combined with invasion in the form of
# expansile nests"; ICCR-Nasal p. 11 "Diffuse expression of squamous markers (e.g., p40, CK5/6)".
AID_NONKERATINISING = ("The report describes nests or ribbons with minimal or no keratin and diffuse p40 or "
                       "CK5/6 staining.")
# ICCR-Op p. 10 "p16 positivity is an acceptable surrogate marker"; Badoual p. 4 "threshold at 70% of
# tumor cells staining positive for p16".
AID_HPV = ("Reports count a tumour as HPV-associated when p16 stains at least 70% of tumour cells, "
           "nuclear and cytoplasmic.")
# ICCR-Nasal p. 8 "Non-intestinal-type adenocarcinoma 8140/3"; p. 11 "Often positive for SOX10, S100,
# and DOG1".
AID_SN_ADENO = ("The report describes seromucinous-type glands, often S100, SOX10 and DOG1 positive, "
                "without intestinal differentiation.")
# Thompson p. 14 "uniform cells with a salt-and-pepper nuclear chromatin arranged in sharply
# demarcated lobules".
AID_ONB = ("The report describes lobules of uniform cells with salt-and-pepper chromatin, at or near the "
           "cribriform plate.")
# Thompson p. 7 "A high-grade mixed epithelial, mesenchymal, and primitive neuroectodermal malignancy".
AID_TCS = "The report describes epithelial, mesenchymal and primitive neuroectodermal elements in one tumour."
# ICCR-Lx p. 15 "Special stains for mucin and FISH for MAML2 rearrangement may help to diagnose".
AID_MEC = "The report states mucin staining or a MAML2 rearrangement in support."


# ------------------------------------------------------------------------------------------
# Referrals shared by the screens
# ------------------------------------------------------------------------------------------
def lymphoma(label="Lymphoma, Langerhans cell histiocytosis or another haematolymphoid tumour"):
    # Rules p. 5 "Waldeyer ring, Peyer patches in the small intestine"; Muller p. 7 "plasmablastic
    # lymphoma, Langerhans cell". Rule D: Rules p. 2 (printed p. 15).
    return refer(label, 2,
                 "A lymphoma belongs to ICCC-3 Group II. An extranodal lymphoma is coded to the site "
                 "where it arose (WHO Rule D), except that a lymphoma of the tonsil or Waldeyer ring "
                 "is a nodal lymphoma. Langerhans cell histiocytosis is also coded in Group II. "
                 "Code the case from the Group II (lymphomas) tree.",
                 note="ICD-O-3.1 Rule D, p. 15. Evidence hn_*_histology lymphoma option.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence hn_*_document_inventory, hn_clinical, hn_imaging, hn_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    lymph_cyto = lymphoma("Cytology names a lymphoma")
    melanoma_cyto = go("Cytology names melanoma", "me_cytology",
                       note="Evidence hn_cytology option 5 (mel_cytology): the melanoma tree's "
                            "cytology screen, which records 8720/3 at basis 5 (D8, D13). "
                            "group11_tree.trees() defers this hop while g11_melanoma has no module.")
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour of the lip, mouth, pharynx, larynx, trachea, "
                 "nose or sinuses?",
        # Evidence hn_*_document_inventory hint; Rule C: Rules p. 5 "Use subcategory '.8' when a
        # single tumor overlaps the boundaries of two or more" (evidence rules_a_to_k C; departure 2).
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology. A stain or a gene result counts only as part of a histology "
              "report. A biopsy or cytology report that calls the specimen inadequate or "
              "non-diagnostic counts as no tissue. A tumour that overlaps two subsites with no "
              "stated origin takes the subsite for overlapping lesions (WHO coding Rule C): go back "
              "to the site step."),
        tier_labels={
            "cytology": "A cytology report, such as a fine-needle aspirate or a smear - no histology "
                        "report",
            "histology": "A histology report, with or without stains or gene results",
        },
        cytology=[
            # Evidence hn_cytology option 1.
            cyto("Cytology names squamous cell carcinoma", "8070", note="Evidence hn_cytology option 1."),
            # Evidence hn_cytology option 2; icdo32.sqlite 8020/3 Related "Carcinoma, poorly
            # differentiated, NOS".
            cyto("Cytology names a poorly differentiated or undifferentiated carcinoma", "8020",
                 "ICD-O-3.2 gives Carcinoma, poorly differentiated, NOS as a related term of this "
                 "code.", note="Evidence hn_cytology option 2."),
            cyto_carcinoma_nos(note="Evidence hn_cytology option 3 ('Cytology names a carcinoma "
                                    "with no type')."),
            melanoma_cyto,
            lymph_cyto,
        ],
        note="Evidence hn_*_document_inventory, hn_clinical, hn_imaging and hn_cytology "
             "(departures 1 and 2 in the module docstring).")


# ------------------------------------------------------------------------------------------
# Histology (evidence hn_oral_histology, hn_lx_histology, hn_sn_histology, merged)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # ICCR-Op p. 10 "Squamous cell carcinoma, HPV-associated 8085/3"; "Squamous cell carcinoma,
        # HPV-independent 8086/3". Departure 4; D1 exception (the code needs a further answer).
        go("Squamous cell carcinoma of the oropharynx (tonsil, base of the tongue, soft palate, uvula, "
           "vallecula or the oropharyngeal wall)", n("oropharynx_hpv"),
           note="D14 organ label; evidence op_squamous_hpv (departure 4). D1: the code depends on "
                "the human papillomavirus answer."),
        # Zidar p. 1 "and its variants are by far the most common malignancies at these locations";
        # Muller p. 6 "The listed subtypes of OSCC are unchanged"; ICCR-Oral p. 8 "Subtypes should be
        # assigned for both prognosis and cancer registry."; ICCR-Nasal p. 8 "Keratinising squamous
        # cell carcinoma 8071/3".
        go("Squamous cell carcinoma, of any subtype, of the lip, mouth, tongue, hypopharynx, larynx, "
           "trachea, nose, sinuses or middle ear", n("squamous_type"),
           note="Evidence hn_oral_histology option 1, hn_lx_histology option 1, hn_sn_histology "
                "option 1 (departures 3 and 5). Squamous cell carcinoma is an option on indirect "
                "paediatric evidence (evidence data gap 1)."),
        # Zidar p. 3 "If poorly differentiated, neuroendocrine carcinoma, melanoma and lymphoma must
        # be excluded".
        go("Poorly differentiated or undifferentiated carcinoma of the lip, mouth, pharynx, larynx or "
           "trachea, and the report names no type", n("ihc"),
           note="Evidence hn_oral_histology option 3, hn_lx_histology option 3 (departure 3): the "
                "stain panel, whose fallback records 8020/3 when no stain is reported."),
        # Zidar p. 3 (as above); Thompson p. 7 "SNUC is negative or, at most, focally positive with
        # squamous markers".
        go("Poorly differentiated or undifferentiated carcinoma of the nose, nasal cavity or paranasal "
           "sinuses, and the report names no type", n("sn_ihc"),
           note="Evidence hn_sn_histology option 3 (departure 3)."),
        # ICCR-Oral p. 4 "including mucosal lip and tongue (mucosal carcinomas, minor salivary gland";
        # ICCR-Lx p. 5 "Salivary-type malignancies arising from minor mucoserous glands of the
        # hypopharynx and larynx"; Thompson p. 2 "Salivary gland-type neoplasms may arise"; Pfister
        # p. 14 "Malignant Mucoepidermoid carcinoma Acinic cell carcinoma". D1: paediatric.
        go("A salivary gland-type carcinoma, such as mucoepidermoid carcinoma or acinic cell carcinoma, "
           "or an adenocarcinoma of a minor salivary gland", n("salivary"),
           note="Evidence hn_*_histology salivary option. D1: mucoepidermoid and acinic cell "
                "carcinoma are paediatric (Pfister 2022 Table 3, p. 14)."),
        # ICCR-Nasal p. 8 "Non-intestinal-type adenocarcinoma 8140/3"; Thompson p. 10 "Non-ITAC is
        # dichotomous, subdivided into low-grade and high-grade tumors"; p. 11 "Often positive for
        # SOX10, S100, and DOG1".
        aid(named("Adenocarcinoma of the nose or sinuses with no type named, or non-intestinal-type "
                  "adenocarcinoma, low grade or high grade", "8140",
                  "Low grade and high grade take the same code.",
                  note="Evidence hn_sn_histology option 4 (departure 3). Intestinal-type "
                       "adenocarcinoma is a picker entry."), AID_SN_ADENO),
        # ICCR-Nasal p. 7 "with an explanatory comment may be given if a diagnosis cannot be further
        # refined".
        named("Carcinoma, with no type named", "8010",
              upgrade=TYPE_NOT_STATED,
              note="Evidence hn_oral_histology option 5, hn_lx_histology option 5, hn_sn_histology "
                   "option 6."),
        # Pfister p. 14 "Nasopharyngeal carcinoma NUT carcinoma Melanotic neuroectodermal tumor of
        # infancy"; Muller p. 7 "MNTI is not an exclusive tumor of bone". D1: paediatric.
        go("Melanotic neuroectodermal tumour of infancy", n("mnti"),
           note="Evidence hn_oral_histology option 7. D1: paediatric (Pfister 2022 Table 3, p. 14)."),
    ] + tail_options(
        P, "mucosa", where=WHERE, nut=True,
        not_malignant_label="A benign lesion, papilloma, hamartoma, angiofibroma, dysplasia or carcinoma "
                            "in situ, with no invasive tumour",
        referrals=[
            lymphoma(),
            refer_leukaemia(WHERE),
            # ICCR-Lx p. 6 "Lymphomas and sarcomas are not included"; Thompson p. 4
            # "adamantinoma-like Ewing sarcoma; negative results for NUT, CD99, and NKX2.2".
            refer_sarcoma(WHERE, label="Rhabdomyosarcoma or another soft-tissue sarcoma, including "
                                       "biphenotypic sinonasal sarcoma and Ewing sarcoma of soft tissue"),
            # ICCR-Nasal p. 8 "Teratocarcinosarcoma 9081/3".
            aid(refer("Teratocarcinosarcoma, teratoma or another germ cell tumour", 10,
                      "Germ cell tumours, teratomas and teratocarcinosarcoma belong to ICCC-3 Group X at "
                      "these sites. Code the case from the Group X (germ cell tumours) tree.",
                      note="Evidence hn_sn_histology option 9: ICCC-2017 range 101 (Xb2) places "
                           "9081/3 at the nose and sinuses (conflicts row 3)."), AID_TCS),
            refer_other_named(),
        ],
        extra_referrals=[
            # Thompson p. 14 "olfactory neuroblastoma (ONB) was retained in the sinonasal tract
            # chapter"; ICCC-2017: 9520-9523 -> IVb at every site (conflicts row 1).
            aid(refer("Olfactory neuroblastoma (esthesioneuroblastoma)", 4,
                      "Olfactory neuroblastoma is coded in ICCC-3 Group IV, Neuroblastoma and other "
                      "peripheral nervous cell tumours. Code the case from the Group IV tree.",
                      note="Evidence hn_sn_histology option 8."), AID_ONB),
            # ICCR-Lx p. 5 "Neuroendocrine neoplasms, as newly defined, include paraganglioma";
            # ICCC-2017: 8693 -> IVb at every site (conflicts row 2).
            refer("Paraganglioma", 4,
                  "Paraganglioma is coded in ICCC-3 Group IV, Neuroblastoma and other peripheral "
                  "nervous cell tumours. Code the case from the Group IV tree.",
                  note="Evidence hn_lx_histology option 7."),
            # Zidar p. 5 "Both tumors arise in laryngeal hyaline cartilages"; ICCC-2017 IXd9.
            refer("Chondrosarcoma of the laryngeal or tracheal cartilage", 9,
                  "Chondrosarcoma of the larynx or trachea is coded in ICCC-3 Group IX, Soft-tissue "
                  "and other extraosseous sarcomas. Code the case from the Group IX tree.",
                  note="Evidence hn_lx_histology option 8."),
            # Thompson p. 2 "but are included in the odontogenic and maxillofacial bone"; p. 12 "This
            # malignant bone tumor recapitulating notochordal". ICCC-2017: 9370/3 VIIId2, 9270 VIIId3
            # (conflicts row 5). recapture_site: the bone is not this tree's site.
            refer("A malignant odontogenic tumour such as ameloblastic carcinoma, chordoma of the skull "
                  "base, or another tumour of the jaw or facial bones", 8,
                  "Malignant odontogenic tumours, chordoma and bone tumours are coded in ICCC-3 Group "
                  "VIII, Malignant bone tumours, at the bone. Code the case from the Group VIII tree; "
                  "it asks for the bone site.",
                  recapture=True,
                  note="Evidence hn_oral_histology option 11 and hn_sn_histology option 13 (departure "
                       "10)."),
            # Thompson p. 3 "Adamantinomatous craniopharyngioma Meningioma of sinonasal tract
            # Olfactory neuroblastoma"; ICCC-2017: 9351 IIIe2, 9530 IIIe5 at every site.
            refer("Craniopharyngioma or meningioma", 3,
                  "Craniopharyngioma and meningioma, benign ones included, are coded in ICCC-3 Group "
                  "III (central nervous system and miscellaneous intracranial and intraspinal "
                  "neoplasms). Code the case from the Group III tree.",
                  note="Evidence hn_sn_histology option 14."),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence hn_*_histology hints. Thompson p. 4 "may be associated with a precursor SNP".
        "Use the report's own term. A grade (well, moderately or poorly differentiated) does not change "
        "the code. An adenocarcinoma of the mouth, pharynx or larynx is a minor salivary gland "
        "carcinoma: choose the salivary gland-type answer. A carcinoma that arose in a sinonasal "
        "papilloma is coded as the carcinoma. Neuroendocrine carcinomas, sinonasal undifferentiated "
        "carcinoma, intestinal-type adenocarcinoma and other named carcinomas are under Another "
        "carcinoma the report names.",
        opts, [],
        "Evidence hn_oral_histology, hn_lx_histology and hn_sn_histology, merged (departures 1 and 3). "
        "D1: the paediatric entities are NUT carcinoma, mucoepidermoid carcinoma, acinic cell "
        "carcinoma and melanotic neuroectodermal tumour of infancy (Pfister 2022 Table 3, p. 14); "
        "squamous cell carcinoma and the oropharyngeal human papillomavirus entities are options "
        "because their code depends on a further answer. Every other carcinoma code ICCC-2017 places "
        "in XIf10 at all routed sites is a picker entry (D2).")


def oropharynx_hpv():
    return node(
        n("oropharynx_hpv"), "histology_subclassification", 4, "Oropharyngeal carcinoma",
        "What does the report say about human papillomavirus (HPV) in the squamous cell carcinoma?",
        # Evidence op_squamous_hpv hint. ICCR-Op p. 10 "HPV-associated is the term applied even if
        # only p16 is performed"; Rules p. 3 "use the numerically higher code number if the diagnosis
        # of a single tumor".
        "A p16 result alone counts: p16 positive is HPV-associated, p16 negative is HPV-independent. A "
        "squamous subtype named with an HPV status takes the HPV code, the higher code.",
        [
            # ICCR-Op p. 10 "Squamous cell carcinoma, HPV-associated 8085/3"; "p16 positivity is an
            # acceptable surrogate marker"; Badoual p. 4 "threshold at 70% of tumor cells staining
            # positive for p16".
            aid(named("Squamous cell carcinoma, HPV-associated, or p16 positive", "8085",
                      note="Evidence op_squamous_hpv option 1 (departure 4). New in ICD-O-3.2 and "
                           "absent from REDCap: the REDCap-side list (standing rule 16)."), AID_HPV),
            # ICCR-Op p. 10 "Squamous cell carcinoma, HPV-independent 8086/3"; "p16 negativity is an
            # acceptable surrogate marker"; Badoual p. 5 "distinguished from those described above by
            # the absence of high-risk HPV infection".
            named("Squamous cell carcinoma, HPV-independent, or p16 negative", "8086",
                  note="Evidence op_squamous_hpv option 2 (departure 4). New in ICD-O-3.2 and absent "
                       "from REDCap: the REDCap-side list (standing rule 16)."),
            # ICCR-Op p. 10 "HPV-associated is the term applied even if only p16 is performed".
            go("The report gives no HPV or p16 result", n("squamous_type"),
               note="Evidence op_squamous_hpv option 3 (8070/3 directly); departure 4: the subtype "
                    "screen records 8070/3 for a squamous cell carcinoma with no subtype."),
        ], [],
        "Evidence op_squamous_hpv (XIc_nasopharynx; departure 4). D1 exception: the code depends on the "
        "human papillomavirus answer. D5: a squamous subtype named with an HPV status takes the HPV "
        "code, the higher code (Rules p. 3).")


def squamous_type():
    return node(
        n("squamous_type"), "histology_subclassification", 4, "Squamous cell carcinoma type",
        "Which type of squamous cell carcinoma does the report name?",
        # Evidence hn_squamous_type and hn_sn_squamous_type hints. Rules p. 3 "use the numerically
        # higher code number if the diagnosis of a single tumor"; ICCR-Oral p. 8 "Hybrid lesions such
        # as verrucous carcinoma and SCC exist".
        "Pick the subtype the diagnosis names. A grade does not change the code; when the report gives "
        "two grades, the higher grade is the one recorded in the file. When the report names two types "
        "for one tumour and no answer covers both, pick the one with the higher code: a hybrid of "
        "verrucous carcinoma and conventional squamous cell carcinoma is recorded as squamous cell "
        "carcinoma (8070/3). An HPV, p16 or Epstein-Barr virus result reported as a separate test does "
        "not change the code, except for a carcinoma of the oropharynx (go back and take the "
        "oropharynx option). A carcinoma that arose in a sinonasal papilloma is coded as the carcinoma "
        "named here.",
        [
            # ICCR-Lx p. 12 "Conventional squamous cell carcinoma 8070/3"; ICCR-Nasal p. 10 "can be
            # diagnosed by routine microscopy".
            named("Squamous cell carcinoma with no subtype named, or conventional squamous cell "
                  "carcinoma", "8070",
                  upgrade="The report does not name the subtype. A report that names it gives that "
                          "subtype's own code: go back and take the option that names it.",
                  note="Evidence hn_squamous_type option 1, hn_sn_squamous_type option 3."),
            # ICCR-Lx p. 12 "Verrucous squamous cell carcinoma 8051/3"; Zidar p. 4 "Verrucous
            # carcinoma is a variant of well-differentiated SCC"; Muller p. 6 "adversely affect
            # outcome and should be treated as VC".
            aid(named("Verrucous carcinoma (verrucous squamous cell carcinoma)", "8051",
                      note="Evidence hn_squamous_type option 2."), AID_VERRUCOUS),
            # ICCR-Lx p. 12 "Basaloid squamous cell carcinoma 8083/3".
            aid(named("Basaloid squamous cell carcinoma", "8083", note="Evidence hn_squamous_type "
                                                                       "option 3."), AID_BASALOID),
            # ICCR-Lx p. 12 "Papillary squamous cell carcinoma 8052/3".
            aid(named("Papillary squamous cell carcinoma", "8052", note="Evidence hn_squamous_type "
                                                                        "option 4."), AID_PAPILLARY),
            # ICCR-Oral p. 8 "Spindle cell (sarcomatoid) squamous cell carcinoma 8074/3".
            aid(named("Spindle cell squamous carcinoma (sarcomatoid squamous cell carcinoma)", "8074",
                      note="Evidence hn_squamous_type option 5."), AID_SPINDLE),
            # ICCR-Oral p. 8 "squamous cell carcinoma 8075/3"; icdo32.sqlite 8075/3 Synonym
            # "acantholytic".
            named("Acantholytic squamous cell carcinoma", "8075",
                  note="Evidence hn_squamous_type option 6."),
            # ICCR-Lx p. 12 "Adenosquamous carcinoma 8560/3"; Zidar p. 5.
            aid(named("Adenosquamous carcinoma", "8560", note="Evidence hn_squamous_type option 7."),
                AID_ADENOSQUAMOUS),
            # ICCR-Lx p. 12 "Lymphoepithelial carcinoma 8082/3"; Zidar p. 5.
            aid(named("Lymphoepithelial carcinoma (lymphoepithelial squamous cell carcinoma)", "8082",
                      note="Evidence hn_squamous_type option 8."), AID_LYMPHOEPITHELIAL),
            # ICCR-Oral p. 8 "Carcinoma cuniculatum 8051/3"; Muller p. 6. Departure 5; registrar review
            # A18 Q110.
            aid(named("Carcinoma cuniculatum", "8051",
                      "This is the code the WHO classification gives carcinoma cuniculatum; ICD-O-3.2 "
                      "prints no separate term for it.",
                      note="Evidence hn_squamous_type option 9 (departure 5; registrar question 6, "
                           "review A18 Q110)."), AID_CUNICULATUM),
            # ICCR-Nasal p. 8 "Keratinising squamous cell carcinoma 8071/3".
            aid(named("Keratinising squamous cell carcinoma", "8071",
                      note="Evidence hn_squamous_type option 10, hn_sn_squamous_type option 1."),
                AID_KERATINISING),
            # ICCR-Nasal p. 8 "Non-keratinising squamous cell carcinoma 8072/3"; Thompson p. 5
            # "DEK::AFF2 carcinomas may represent an emerging, distinctive tumor type".
            aid(named("Non-keratinising squamous cell carcinoma, including DEK::AFF2 carcinoma", "8072",
                      note="Evidence hn_squamous_type option 11, hn_sn_squamous_type option 2."),
                AID_NONKERATINISING),
            go("Another squamous type the report names, such as microinvasive, clear cell or "
               "HPV-associated squamous cell carcinoma - type its name to find it", n("picker"),
               note="Evidence hn_squamous_type option 12, hn_sn_squamous_type option 12."),
        ], [],
        "Evidence hn_squamous_type and hn_sn_squamous_type, merged (departure 5). D1: squamous cell "
        "carcinoma is an option on indirect paediatric evidence (evidence data gap 1) and its subtypes "
        "are subdivisions.",
        )


def salivary():
    return node(
        n("salivary"), "histology_subclassification", 4, "Salivary gland-type carcinoma",
        "Which salivary gland-type carcinoma does the report name?",
        # Evidence hn_salivary hint. Rules p. 11 "coders should use the topography code for oral
        # cavity, C06.9"; "should be coded to the topographic site".
        "Minor salivary gland in the diagnosis names where the tumour began, not a separate type. The "
        "tumour is coded at the place where the gland lies, such as the hard palate; when the report "
        "names no place in the mouth, the site is mouth, not otherwise specified (C06.9).",
        [
            # Pfister p. 14 "Malignant Mucoepidermoid carcinoma Acinic cell carcinoma Sialoblastoma
            # Nasopharyngeal carcinoma"; ICCR-Lx p. 15. D1: paediatric.
            aid(named("Mucoepidermoid carcinoma", "8430",
                      note="Evidence hn_salivary option 1. D1: Pfister 2022 Table 3, p. 14."), AID_MEC),
            # Pfister p. 14 (as above); icdo32.sqlite 8550/3 Synonym "Acinic cell adenocarcinoma".
            named("Acinic cell carcinoma", "8550",
                  "ICD-O-3.2 gives Acinic cell adenocarcinoma as a synonym of this code.",
                  note="Evidence hn_salivary option 2. D1: Pfister 2022 Table 3, p. 14."),
            # Rules p. 11 "should be coded to the topographic site".
            named("Adenocarcinoma with no type named, or minor salivary gland adenocarcinoma", "8140",
                  note="Evidence hn_salivary option 3."),
            # Evidence conflicts rows 8 and 11: myoepithelial carcinoma (8982/3) and malignant mixed
            # tumour (8940/3) are XIIa4 at every site (departure 7).
            refer("Myoepithelial carcinoma, or malignant mixed tumour of salivary gland type", 12,
                  "ICCC-3 places Myoepithelial carcinoma (8982/3) and Mixed tumor, malignant, NOS "
                  "(8940/3) in Group XII (other and unspecified malignant neoplasms) at these sites, "
                  "not in Group XI. Code the case from the Group XII tree.",
                  note="Departure 7. ICCC-2017 range XIIa4 holds 8982/3 and 8940/3 at these sites."),
            # ICCR-Oral p. 8 "For guidance on histological typing of minor salivary gland carcinomas".
            go("Another salivary gland-type carcinoma, such as adenoid cystic carcinoma, polymorphous "
               "adenocarcinoma or secretory carcinoma - type its name to find it", n("picker"),
               note="Evidence hn_salivary option 4 (sg_carcinoma_picker, built as hn_picker: "
                    "departure 7)."),
        ], [],
        "Evidence hn_salivary (departure 7). D1: mucoepidermoid and acinic cell carcinoma are "
        "paediatric (Pfister 2022 Table 3, p. 14); the other salivary gland-type carcinomas are picker "
        "entries.")


def mnti():
    return node(
        n("mnti"), "histology_subclassification", 4, "Melanotic neuroectodermal tumour",
        "Does the report call the melanotic neuroectodermal tumour malignant, or report a metastasis?",
        "",
        [
            # Muller p. 7 "about 2% of MNTI behave in a malignant fashion with metastases"; Rules p. 2
            # "code as the pathologist indicates".
            refer("Yes: the report calls it malignant or reports a metastasis", 12,
                  "A melanotic neuroectodermal tumour stated to be malignant is coded in ICCC-3 Group "
                  "XII, Other and unspecified malignant neoplasms. Code the case from the Group XII "
                  "tree.",
                  note="Evidence hn_mnti option 1 (departure 8): ICCC-2017 holds 9363/3 in XIIa6; "
                       "ICD-O-3.2 prints 9363 at behaviour 0 only, so no /3 term is named."),
            # Pfister p. 14 "Melanotic neuroectodermal tumor of infancy".
            excl("No: the report does not call it malignant and reports no metastasis", "9363", "0",
                 what="melanotic neuroectodermal tumour",
                 note="Evidence hn_mnti option 2."),
        ], [],
        "Evidence hn_mnti (departure 8). D1: paediatric (Pfister 2022 Table 3, p. 14). D6: Rule F "
        "stated behaviour is not built where ICD-O-3.2 prints the term only below /3.")


# ------------------------------------------------------------------------------------------
# The stain panels (evidence hn_ihc and hn_sn_ihc; departure 6)
# ------------------------------------------------------------------------------------------
NE = "Synaptophysin, chromogranin or insulinoma-associated protein 1 (INSM1)"
KERATIN = "Keratin (pan-cytokeratin or another keratin)"
SQUAMOUS = "p40, p63 or cytokeratin 5/6 (CK5/6)"
EBER = "Epstein-Barr virus encoded RNA (EBER) in situ hybridisation"
NUT_HINT = (" A file that reports a NUT immunostain or a NUTM1 gene test is answered on the NUT carcinoma "
            "option of the histology screen, not here.")


def ihc():
    return ihc_node(
        P,
        [
            {"group_label": "Epithelial and squamous markers", "markers": [KERATIN, SQUAMOUS]},
            {"group_label": "Neuroendocrine markers", "markers": [NE]},
        ],
        [
            # ICCR-Lx p. 15 "positive reaction for neuroendocrine markers (synaptophysin,
            # chromogranin, INSM1) and for epithelial markers".
            rule([NE, KERATIN], "8246",
                 "A neuroendocrine marker and a keratin are positive: the neuroendocrine carcinoma "
                 "pattern (International Collaboration on Cancer Reporting hypopharynx, larynx and "
                 "trachea dataset, p. 15). %s" % rec("8246"),
                 note="Evidence ihc_rules 2. ICCR-Lx p. 15 'positive reaction for neuroendocrine "
                      "markers (synaptophysin, chromogranin, INSM1) and for epithelial markers'."),
            # ICCR-Lx p. 15 "must be used only in case of poorly differentiated SCC to confirm the
            # diagnosis"; ICCR-Oral p. 14 "markers may be required for poorly differentiated or spindle
            # cell carcinoma including".
            rule([SQUAMOUS], "8070",
                 "A squamous marker is positive: a squamous cell carcinoma whose subtype the stains do "
                 "not name (International Collaboration on Cancer Reporting hypopharynx, larynx and "
                 "trachea dataset, p. 15). %s" % rec("8070"),
                 note="Evidence ihc_rules 3. ICCR-Lx p. 15 'must be used only in case of poorly "
                      "differentiated SCC to confirm the diagnosis'; ICCR-Oral p. 14."),
        ],
        fallback="8020",
        fallback_reason=("The stains do not establish the carcinoma's type. %s ICD-O-3.2 gives "
                         "Carcinoma, poorly differentiated, NOS as a related term of this code."
                         % rec("8020")),
        # Evidence hn_ihc hint; Zidar p. 3 "If poorly differentiated, neuroendocrine carcinoma,
        # melanoma and lymphoma must be excluded".
        hint="Answer from the stains in the histology report, for a poorly differentiated or "
             "undifferentiated carcinoma that names no type. Answer 'Not done or not readable' for a "
             "stain the report does not mention. If the report concludes melanoma or lymphoma, go back "
             "and choose it on the histology screen." + NUT_HINT,
        note="Evidence hn_ihc and ihc_rules 2-4 (departure 6). Fallback 8020/3: evidence ihc_rules 4, "
             "Zidar p. 3 'If poorly differentiated, neuroendocrine carcinoma, melanoma and lymphoma "
             "must be excluded'.")


def sn_ihc():
    return ihc_node(
        P,
        [
            {"group_label": "Epithelial and squamous markers", "markers": [KERATIN, SQUAMOUS]},
            {"group_label": "Neuroendocrine markers", "markers": [NE]},
            {"group_label": "Epstein-Barr virus", "markers": [EBER]},
        ],
        [
            # ICCR-Nasal p. 11 "at least one specific neuroendocrine marker (synaptophysin,
            # chromogranin, INSM1) and an epithelial marker".
            rule([NE, KERATIN], "8246",
                 "A neuroendocrine marker and a keratin are positive: the neuroendocrine carcinoma "
                 "pattern (International Collaboration on Cancer Reporting nasal cavity and paranasal "
                 "sinuses dataset, p. 11). %s" % rec("8246"),
                 note="Evidence hn_sn_ihc rule 4. ICCR-Nasal p. 11 'at least one specific "
                      "neuroendocrine marker (synaptophysin, chromogranin, INSM1) and an epithelial "
                      "marker'."),
            # ICCR-Nasal p. 11 "Usually positive for Epstein-Barr virus (EBV) by in situ
            # hybridization"; Thompson p. 6 "strongly associated with Epstein-Barr virus (EBV)
            # infection".
            rule([EBER], "8082",
                 "Epstein-Barr virus encoded RNA is positive: the lymphoepithelial carcinoma pattern "
                 "(International Collaboration on Cancer Reporting nasal cavity and paranasal sinuses "
                 "dataset, p. 11). %s" % rec("8082"),
                 note="Evidence hn_sn_ihc rule 5. ICCR-Nasal p. 11 'Usually positive for "
                      "Epstein-Barr virus (EBV) by in situ hybridization'; Thompson p. 6."),
            # ICCR-Nasal p. 11 "Diffuse expression of squamous markers (e.g., p40, CK5/6) required
            # (core)"; Thompson p. 4 "NKSCC is diffusely positive for squamous markers such as p40".
            rule([SQUAMOUS], "8072",
                 "Diffuse p40, p63 or cytokeratin 5/6 staining: the non-keratinising squamous cell "
                 "carcinoma pattern (International Collaboration on Cancer Reporting nasal cavity and "
                 "paranasal sinuses dataset, p. 11). %s" % rec("8072"),
                 note="Evidence hn_sn_ihc rule 6. ICCR-Nasal p. 11 'Diffuse expression of squamous "
                      "markers (e.g., p40, CK5/6) required (core)'."),
        ],
        fallback="8020",
        fallback_reason=("The stains do not establish the carcinoma's type. %s ICD-O-3.2 gives "
                         "Carcinoma, poorly differentiated, NOS as a related term of this code."
                         % rec("8020")),
        # Evidence hn_sn_ihc hint. Thompson p. 7 "SNUC is negative or, at most, focally positive with
        # squamous markers".
        hint="Answer from the stains in the histology report, for a poorly differentiated or "
             "undifferentiated carcinoma of the nose or sinuses that names no type. Answer 'Not done or "
             "not readable' for a stain the report does not mention. If the report concludes melanoma "
             "or lymphoma, go back and choose it on the histology screen." + NUT_HINT,
        note="Evidence hn_sn_ihc (departure 6: NUT rules replaced by the D12 screens; the SMARCB1 and "
             "SMARCA4 rule on 8044/3 not built, D4). Fallback 8020/3: Thompson p. 7 'consisting of a "
             "high-grade carcinoma that lacks any significant squamous, glandular, or neuroendocrine'.",
        name="sn_ihc")


# ------------------------------------------------------------------------------------------
# The exclusion screen (evidence hn_oral/lx/sn_not_malignant, merged; departure 9)
# ------------------------------------------------------------------------------------------
def not_malignant():
    return not_malignant_node(
        P,
        [
            # ICCR-Oral p. 13 "Carcinoma in situ is considered synonymous with severe dysplasia";
            # Zidar p. 2 "a two-tiered system with low-grade (LG) dysplasia/SILs and high-grade (HG)
            # dysplasia/SILs".
            excl("Carcinoma in situ, with no invasive carcinoma", "8070", "2",
                 what="squamous carcinoma in situ"),
            # ICCR-Oral p. 3 "High grade dysplasia is synonymous with moderate/severe dysplasia."; p.
            # 13 "subset of oral dysplasia is positive for high risk human papillomavirus".
            excl("Moderate, severe or high-grade dysplasia, or high-grade squamous intraepithelial "
                 "lesion, with no invasive carcinoma", "8077", "2",
                 what="high grade squamous dysplasia"),
            # Muller p. 4 "morphology without cytologic atypia should be considered mild dysplasia".
            excl("Mild or low-grade dysplasia, or low-grade squamous intraepithelial lesion", "8077",
                 "0", what="low grade squamous dysplasia"),
            # Pfister p. 14 "Head and neck tumors Benign Squamous cell papilloma of larynx".
            excl("A single squamous cell papilloma", "8052", "0", what="a squamous cell papilloma"),
            # Zidar p. 6 "decline of juvenile-onset SP incidence in children"; "High-grade dysplasia
            # is typically seen in recurrent SP".
            excl("Papillomatosis (recurrent respiratory papillomatosis), with or without dysplasia",
                 "8060", "0", what="squamous papillomatosis",
                 extra="A carcinoma arising in it is coded as the carcinoma."),
            # Thompson p. 3 "Sinonasal papilloma, inverted type Sinonasal papilloma, oncocytic type".
            excl("Sinonasal papilloma, inverted type or oncocytic type", "8121", "1",
                 what="an inverted sinonasal papilloma",
                 extra="A carcinoma arising in it is coded as the carcinoma."),
            # Thompson p. 3 "Sinonasal papilloma, exophytic type".
            excl("Sinonasal papilloma, exophytic type", "8121", "0",
                 what="an exophytic sinonasal papilloma"),
            # Pfister p. 14 "Nasal chondromesenchymal hamartoma Pleomorphic adenoma".
            excl("Pleomorphic adenoma", "8940", "0", what="a pleomorphic adenoma"),
            # Muller p. 7 "age range (7 to 78 years-of age) but is most common in".
            excl("Ectomesenchymal chondromyxoid tumour", "8982", "0", what="a myoepithelioma"),
            # Muller p. 6 "This section includes congenital granular cell epulis".
            excl("Granular cell tumour", "9580", "0", what="a granular cell tumour"),
            excl("Chondroma", "9220", "0", what="a chondroma"),
            # Pfister p. 8 "Sinonasal angiofibroma"; Thompson p. 10 "designated as sinonasal tract
            # angiofibroma, moved out of the nasopharynx chapter".
            excl("Sinonasal tract angiofibroma (juvenile angiofibroma)", "9160", "0",
                 what="an angiofibroma",
                 extra="ICD-O-3.2 gives Juvenile angiofibroma as a synonym of this code."),
            # Thompson p. 12 "sinonasal tract ameloblastoma must be centered in the sinonasal tract".
            excl("Sinonasal ameloblastoma", "9310", "0", what="an ameloblastoma"),
            # Thompson p. 3 "pediatric patients comprise the majority of affected"; "Respiratory
            # epithelial adenomatoid hamartoma Seromucinous hamartoma".
            nonrep("Nasal chondromesenchymal hamartoma, respiratory epithelial adenomatoid hamartoma "
                   "or seromucinous hamartoma",
                   "A hamartoma is not a neoplasm in the registry's sense. It is not registrable.",
                   note="Evidence hn_sn_not_malignant option 7."),
            # Thompson p. 11 "this soft tissue tumor to remain in the sinonasal tract chapter".
            nonrep("Sinonasal glomangiopericytoma",
                   "Glomangiopericytoma is not malignant, and ICD-O-3.2 holds no code for it. It is "
                   "not registrable in Group XI.",
                   note="Evidence hn_sn_not_malignant option 8; evidence data gap 6."),
            # Pfister p. 14 "Congenital granular cell epulis".
            nonrep("Congenital granular cell epulis, proliferative verrucous leukoplakia, or another "
                   "benign or reactive lesion",
                   "The report describes a benign or reactive lesion. It is not registrable.",
                   note="Evidence hn_oral_not_malignant option 8."),
        ],
        where=WHERE,
        note="The lines of evidence hn_oral_not_malignant, hn_lx_not_malignant and "
             "hn_sn_not_malignant, merged (departure 9).")


def deposit():
    d = deposit_node(P, where=WHERE)
    # Evidence hn_deposit hint. Thompson p. 9 "the distinction from a distant metastasis to the
    # sinonasal tract must be made".
    d["hint"] += (" A nasopharyngeal carcinoma can extend into the nose or the oropharynx. An "
                  "intestinal-type adenocarcinoma of the nose is separated from a bowel deposit by "
                  "the clinical and imaging findings.")
    return d


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
# Evidence hn_carcinoma_picker hint. Rules p. 3 "use the numerically higher code number if the
# diagnosis of a single tumor"; Rules p. 2 (Rules G and H). Departure 12.
PICKER_HINT_EXTRA = (" When the report names two types for one tumour and no answer covers both, pick the "
                     "one with the higher code number. When the report gives two grades of a "
                     "neuroendocrine tumour, pick the higher grade. A mixed neuroendocrine-non-"
                     "neuroendocrine neoplasm is recorded by its neuroendocrine part: small cell or "
                     "large cell. A term that names another organ, such as breast, lung or thyroid, "
                     "describes a deposit: go back and choose the deposit answer.")


def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), oropharynx_hpv(), squamous_type(), salivary(), mnti(), ihc(),
                      sn_ihc()] + nut_nodes(P) + [not_malignant(), deposit()]
    tree = make_tree(
        TREE_ID, nodes,
        subtype_screens=(n("oropharynx_hpv"), n("squamous_type"), n("salivary"), n("mnti")))
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
    "8070/3": ("D1, D8", EVIDENCE,
               "Squamous cell carcinoma of the lip, mouth, pharynx, larynx, trachea, nose or sinuses "
               "with no subtype named (ICCR-Lx p. 12), at basis 5 when cytology names squamous cell "
               "carcinoma, and from the stain panel when a squamous marker is positive (ICCR-Lx p. "
               "15).",
               {"diagnostic_tests_required": _IHC, "ihc_markers_required": [SQUAMOUS]}),
    "8071/3": ("D1", EVIDENCE,
               "Keratinising squamous cell carcinoma on the squamous type screen (ICCR-Nasal p. 8)."),
    "8072/3": ("D1", EVIDENCE,
               "Non-keratinising squamous cell carcinoma on the squamous type screen (ICCR-Nasal p. 8), "
               "and from the sinonasal stain panel when a squamous marker is diffusely positive "
               "(ICCR-Nasal p. 11).",
               {"diagnostic_tests_required": _IHC, "ihc_markers_required": [SQUAMOUS]}),
    "8051/3": ("D1, D4", EVIDENCE,
               "Verrucous carcinoma on the squamous type screen (ICCR-Lx p. 12). Carcinoma cuniculatum "
               "records the same code, the one the WHO tables give it (ICCR-Oral p. 8) where "
               "ICD-O-3.2 prints no separate term; registrar review A18, Q110."),
    "8083/3": ("D1, D5", EVIDENCE,
               "Basaloid squamous cell carcinoma on the squamous type screen (ICCR-Lx p. 12)."),
    "8052/3": ("D1", EVIDENCE,
               "Papillary squamous cell carcinoma on the squamous type screen (ICCR-Lx p. 12)."),
    "8074/3": ("D1", EVIDENCE,
               "Spindle cell squamous carcinoma on the squamous type screen (ICCR-Oral p. 8)."),
    "8075/3": ("D1", EVIDENCE,
               "Acantholytic squamous cell carcinoma on the squamous type screen (ICCR-Oral p. 8); "
               "ICD-O-3.2 gives Squamous cell carcinoma, adenoid as the Preferred term."),
    "8560/3": ("D1", EVIDENCE,
               "Adenosquamous carcinoma on the squamous type screen (ICCR-Lx p. 12)."),
    "8082/3": ("D1", EVIDENCE,
               "Lymphoepithelial carcinoma on the squamous type screen (ICCR-Lx p. 12), and from the "
               "sinonasal stain panel when Epstein-Barr virus encoded RNA is positive (ICCR-Nasal p. "
               "11).",
               {"diagnostic_tests_required": _IHC, "ihc_markers_required": [EBER]}),
    "8085/3": ("D1, D5", EVIDENCE_OP,
               "Squamous cell carcinoma of the oropharynx, human papillomavirus-associated or p16 "
               "positive (ICCR-Op p. 10; Badoual p. 4). New in ICD-O-3.2 and absent from REDCap: the "
               "REDCap-side list (standing rule 16)."),
    "8086/3": ("D1, D5", EVIDENCE_OP,
               "Squamous cell carcinoma of the oropharynx, human papillomavirus-independent or p16 "
               "negative (ICCR-Op p. 10; Badoual p. 5). New in ICD-O-3.2 and absent from REDCap: the "
               "REDCap-side list (standing rule 16)."),
    "8010/3": ("D8", EVIDENCE,
               "Carcinoma of the head and neck whose type the report does not name, at basis 7 on "
               "the histology screen (ICCR-Nasal p. 7), and at basis 5 when cytology names a "
               "carcinoma without its type."),
    "8020/3": ("D8", EVIDENCE,
               "Poorly differentiated or undifferentiated carcinoma whose type the report does not "
               "name: the stain panels' fallback at basis 7, and basis 5 when cytology names such a "
               "carcinoma. ICD-O-3.2 gives Carcinoma, poorly differentiated, NOS as a related term "
               "of 8020/3."),
    "8246/3": ("D2", EVIDENCE,
               "Neuroendocrine carcinoma from the stain panels (a neuroendocrine marker and a keratin "
               "positive; ICCR-Lx p. 15, ICCR-Nasal p. 11) and in the picker.",
               {"diagnostic_tests_required": _IHC, "ihc_markers_required": [NE, KERATIN]}),
    "8140/3": ("D1", EVIDENCE,
               "Adenocarcinoma of the nose or sinuses with no type named, or non-intestinal-type "
               "adenocarcinoma (ICCR-Nasal p. 8), and the minor salivary gland adenocarcinoma with no "
               "type named (Rules p. 11)."),
    "8430/3": ("D1", EVIDENCE,
               "Mucoepidermoid carcinoma of a minor salivary gland on the salivary gland-type screen "
               "(Pfister 2022 Table 3, p. 14)."),
    "8550/3": ("D1", EVIDENCE,
               "Acinic cell carcinoma of a minor salivary gland on the salivary gland-type screen "
               "(Pfister 2022 Table 3, p. 14); ICD-O-3.2 gives Acinic cell adenocarcinoma as a "
               "synonym of 8550/3."),
    "8023/3": ("D12, D15", EVIDENCE,
               "NUT carcinoma at the head and neck sites (Pfister 2022 Table 3, p. 14; ICCR-Nasal p. "
               "8) on the NUT carcinoma screens: basis 8 with a NUTM1 result, basis 7 otherwise. New "
               "in ICD-O-3.2 and absent from REDCap's XIf10 list: the REDCap-side list (standing rule "
               "16)."),
}
