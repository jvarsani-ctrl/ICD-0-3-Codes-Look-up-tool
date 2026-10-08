"""g11_thymus (prefix ty_): carcinomas of the thymus and mediastinum at C37.9, C38.1, C38.2 and
C38.3, ICCC-3 subgroups XIf5 (C37.9) and XIf10 (C38.1 to C38.3).

Built from docs/group_11_evidence/XIf5_thymus_mediastinum.json (the evidence agent's nodes
tm_site, tm_evidence, tm_lab, tm_cytology, tm_histology, tm_nut, tm_picker, tm_adeno_ihc and its
ihc_rules) with the builders in build/group11_common.py, in the shape of the thyroid exemplar.
Every option's label, code, behaviour, basis, reason and recognition aid comes from that file; the
cite (file, PDF page, quotation) is the comment above the option or the aid. File names in the
comments are the evidence's own:
    ICCR      XIf5-thymus__ICCR-Thymic-Epithelial-3rd.txt (ICCR Thymic Epithelial Tumours
              Histopathology Reporting Guide, 3rd edition, version 3.0, May 2022). Table 1 (PDF
              pp. 9-10) was read from the page image; its text layer matched.
    Marx      XIf5-thymus-and-mediastinum__Marx-2022.txt (Marx A, et al. J Thorac Oncol
              2022;17:200-213). Tables 1 to 3 (PDF pp. 4, 9, 11) were read from the page image.
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rossi     XIf5-thymus-paediatric__Rossi-2022.txt (Rossi C, et al. Diagnostics (Basel)
              2022;12:2205, PMC9497562). It has sections, not pages: "PMC section N".
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 section 4, printed pp. 14-28)
    Visser    Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
              set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    ty_document_inventory  document_inventory  evidence gate (evidence tm_evidence)
    ty_labs_referral, ty_labs_markers, ty_labs_cytology, ty_labs_histology  lab_results
                                               (evidence tm_lab, lab_tests)
    ty_clinical, ty_clinical_cytology  clinical_alias
    ty_imaging, ty_imaging_markers, ty_imaging_cytology  morphology_only (evidence tm_lab)
    ty_cytology            morphology_only     (evidence tm_cytology)
    ty_site_cytology       site_resolution     (D9; evidence tm_site, cytology context)
    ty_cytology_thymic     morphology_only     (evidence tm_cytology option 1)
    ty_histology           histology_subclassification  (evidence tm_histology)
    ty_site                site_resolution     (D9; evidence tm_site, histology context)
    ty_thymic              histology_subclassification  (evidence tm_histology options 1-6;
                                               tm_picker options 9 and 16)
    ty_ihc                 ihc_checklist       (evidence tm_adeno_ihc and ihc_rules)
    ty_nut_result, ty_nut_basis, ty_nut_tests  histology_subclassification (D12; evidence tm_nut)
    ty_not_malignant       histology_subclassification  (the exclusions of evidence tm_histology)
    ty_deposit             morphology_only     (D10)
    ty_picker              histology_subclassification  (D2; evidence tm_picker's long tail)

Departures from the evidence nodes, and why
-------------------------------------------
1. tm_site: the evidence opens the tree with a site screen. The router captures the case's site
   and routes C37.9 and C38.1 to C38.3 here, and the entry node is the document checklist
   (contract §0.4), so the site screen is not the entry. Options 3 and 5 ("for any other
   tumour", C38.1 and C38.3) are the site the router already holds and need no node. Option 6
   (C38.8, overlapping lesion) and option 7 (C76.1, beside the thymus) are sites the router
   sends to g11_thoracic and g11_unspecified (D14). Option 8 ("Outside the mediastinum", lung or
   neck) is a referral to Group XI itself with recapture_site, which group11_common does not
   build while SELF_REFERRAL is False; the ty_site and ty_histology hints send the clerk back to
   the site step instead, as the common deposit node does. Options 1, 2 and 4 become ty_site and
   ty_site_cytology (D9), reached only when the report names a thymic tumour type (a thymoma, a
   thymic carcinoma or a thymic carcinoid), which is where the evidence's site rule depends on the
   type. Each option captures topography: C37.9 for the thymus, the anterior mediastinum, the
   mediastinum with no part named or the chest (ICD-O-3.2 prints C37.9 beside 8580 to 8586,
   checked in icdo32.sqlite code_reference on 8 October 2026; WHO coding Rule H), and C38.2 for a
   thymic tumour the report says arose in the posterior mediastinum (Rule H, a known other site).
2. tm_evidence: options 1 and 2 recorded 8000/3 at basis 1 and 2 on the gate itself. D7: each
   tier routes to its own screen (ty_clinical, ty_imaging), which refers the case to Group XII
   with refer_code 8000, because ICCC-2017 places 8000/3 at C37.9 and C38 in XIIb (range 143);
   the evidence notes the same (conflicts, Group 12). Option 4 ("possible, probable or suspected
   cancer only") becomes the common pair: "probable" registers 8000 in Group XII and "possible or
   suspected" is not registrable (Visser rule 4). The gate's options are the contract §4.2 tiers,
   with laboratory copies (registrar, 6 October 2026).
3. tm_lab: a lab_results screen cannot choose a code (registrar, 6 October 2026; Group 10
   lesson). The ty_labs_* screens record chromogranin A, adrenocorticotropic hormone,
   alpha-fetoprotein and beta human chorionic gonadotropin (evidence lab_tests; the units are
   Group 10's for the last two, the lung tree's for the first two; the evidence gives none).
   Options 1 and 2 (8240/3, 8158/3, basis 4) move to ty_imaging_markers as marker() options, each
   requiring the diagnosis Visser Table 4 names, as the thyroid's departure 2 does. Option 3
   (alpha-fetoprotein or human chorionic gonadotropin -> Group X) is a sentence in the gate hint
   and the marker screen hint: validator rule 2 and the walk admit no tissue-free referral other
   than Group XII with 8000 or 8001 (request in the return; the adrenal tree's departure 3 is the
   same). Option 4 is the common pair of non-registrable lines.
4. tm_cytology: option 1 sent a named type to the histology screen at basis 5. Basis 7 options
   need Histology on the path, so the cytology types have their own screens: a thymoma, thymic
   carcinoma or thymic carcinoid goes through ty_site_cytology (D9) to ty_cytology_thymic, which
   records the six thymoma lines, 8586/3 Thymic carcinoma, NOS and 8240/3 Neuroendocrine tumor,
   NOS at basis 5 (D8); NUT carcinoma records 8023/3 at basis 5 on ty_cytology, at the site
   entered (D12). Option 2 (8010/3, basis 5) is widened to a named type the list does not hold,
   as the lung tree does (standing rule 8: the generic code understates, never overstates).
   Option 3 (8000/3, basis 5) becomes the common "Malignant cells are present, with no tumour
   type named", which refers to Group XII with 8001 (D8). Options 4 and 5 (lymphoma, Group II;
   germ cell tumour, Group X) are kept. Option 6 is the common non-registrable line, and the
   common non-diagnostic routes are added.
5. tm_histology: node type morphology_only becomes histology_subclassification (contract §4.2).
   The six thymoma options move one screen down, to ty_thymic, after ty_site (D9), with the
   hint's thymoma-type sentence; the first option of ty_histology leads there. D1 holds: Rossi
   2022 makes the thymoma types paediatric, and they are options. The four exclusions and the
   hyperplasia line move to ty_not_malignant (contract §4.2), reached by the standard option,
   whose label names thymic hyperplasia and a thymic cyst. The hint drops "one it calls malignant
   is recorded as malignant": D6 builds no stated-behaviour code above the behaviour ICD-O-3.2
   prints (micronodular thymoma with lymphoid stroma stays 8580/1). It adds where NUT carcinoma
   is recorded (D12) and the route for a thymic tumour outside the mediastinum (departure 1).
6. tm_histology trailing options: the common ones (tail_options): melanoma (D13; the evidence
   has none; the thymus is neither skin, eye nor central nervous system, so the hop enters
   me_mucosa, as the thyroid and lung trees do), NUT carcinoma (D12, the common screens), the
   picker (D2), the exclusion screen, the deposit question (D10; it replaces option 22, a
   referral with recapture_site and no group), and "Malignant tumour, type not determined"
   (Group XII, 8000, D7). The referrals are the evidence's options 15 to 21: germ cell tumour and
   teratoma with somatic-type malignancy (Group X), lymphoma (Group II, keeping the case's site,
   Rule D), T-lymphoblastic leukaemia (Group I at C42.1, Rule E; the common leukaemia line),
   neuroblastoma, ganglioneuroblastoma or paraganglioma (Group IV), sarcoma (Group IX) and
   carcinosarcoma (Group XII), then the common "another named tumour" (Group XII).
7. tm_nut: the common NUT screens (nut_nodes: ty_nut_result, ty_nut_basis, ty_nut_tests). The
   evidence's options map onto them: a nuclear NUT stain records 8023/3 at basis 7, a NUTM1
   fusion at basis 8, a report naming NUT carcinoma with no stain or gene result at basis 7. Its
   option 4 ("possible or suspected only" -> picker) is the common "Neither" line, which returns
   to the histology screen. NUT carcinoma does not pass through ty_site: D12 records the site the
   report gives, so the case keeps the site entered at the start (registrar review C3, Q66).
8. tm_picker: D2 replaces the evidence's curated picker. Labels are ICD-O-3.2 Preferred terms,
   search_terms the live synonyms and related terms, and the options carry no recognition aid
   (Group 10's picker shape). The evidence's picker labels, reasons and aids are therefore not
   shown (metaplastic thymoma and YAP1::MAML2; micronodular thymic carcinoma and terminal
   deoxynucleotidyl transferase; low-grade papillary adenocarcinoma; enteric adenocarcinoma and
   its markers; mucoepidermoid carcinoma and MAML2; hyalinizing clear cell carcinoma and EWSR1;
   neuroendocrine tumour, grade 3; small cell carcinoma and the 10 percent rule); the build
   report lists them. ICD-O-3.2 holds the WHO names as live terms (8200/3 Thymic carcinoma with
   adenoid cystic carcinoma-like features, 8249/3 Neuroendocrine tumor, grade 3, 8033/3 Sarcomatoid
   carcinoma, 8082/3 Lymphoepithelioma-like carcinoma, 8580/3 Metaplastic thymoma), so the
   picker's filter finds them. 8580/3 and 8586/3 stay in the picker (picker_keep), because
   ty_thymic offers them only under narrower labels and the picker is where "metaplastic thymoma"
   and "thymic carcinoma, NOS" are typed. The picker hint gains the evidence's Rule K and Rule G
   sentences.
9. tm_picker option 16 (hepatoid, rhabdoid or sebaceous carcinoma of the thymus, undifferentiated
   large cell carcinoma with a Castleman disease-like reaction -> 8586/3) moves to ty_thymic, where
   the registrar's ruling of 8 October 2026 on review A1 (a) and (b) splits it by the WHO ICD-O-3
   coding Rules A to K (docs/group_11_evidence/registrar_A1ab_rules.md, C4a to C4d, C5). Four
   options replace it: hepatoid carcinoma or hepatoid adenocarcinoma of the thymus records 8576/3
   Hepatoid adenocarcinoma (the term ICD-O-3.2 prints); sebaceous carcinoma of the thymus records
   8410/3 Sebaceous carcinoma (Rule H: the skin topography ICD-O-3.2 prints beside it gives way to
   the stated thymus); undifferentiated large cell carcinoma, including one with a Castleman
   disease-like reaction, records 8012/3 Large cell carcinoma, NOS (Rule G: undifferentiated is a
   grade); rhabdoid carcinoma of the thymus keeps 8586/3 Thymic carcinoma, NOS, because ICD-O-3.2
   prints no such term and Rule J word order reaches none. The reading the controller fixed:
   Thymic carcinoma, NOS is a not-otherwise-specified term, so a specified type replaces it, and
   Rule K is not used, because a NOS term and a specified type are not two modifiers that no single
   code covers. The picker keeps 8576/3, 8410/3 and 8012/3 so that a clerk who types the term
   still reaches each. This is an option for a non-paediatric entity (D1 departure); the picker
   cannot carry the World Health Organization's mapping.
10. tm_picker option 9 (adenocarcinoma with CK20, CDX2 or MUC2 results and no type named) moves
   to ty_thymic as the hop to ty_ihc: the generated picker holds coded options only.
11. tm_adeno_ihc: the three one-marker rules are the evidence's; its fourth rule (CK20, CDX2 and
   MUC2 negative -> 8140/3) is the NOS fallback, 8140/3, which also takes stains not done. The
   rule emitting 8144/3 makes the generator require Histology and IHC on the 8144/3 entry for
   every tree (DECISIONS override; the thyroid's 8201/3 and 8502/3 set the precedent).
12. Exclusions: "Microscopic thymoma, or a thymoma the report calls benign" (8580/0) carries
   registrar_decision_required (registrar review Q69). Thymolipoma names the liposarcoma
   referral (evidence conflicts, Group 9: 8850/0 against 8850/3).
13. Not built from the evidence: thoracic SMARCA4-deficient undifferentiated tumour (D4; no
   ICD-O-3.2 term; registrar review A18, Q71); a Rule F malignant code for micronodular thymoma
   with lymphoid stroma (D6). Combined thymic carcinoma and thymoma (registrar review Q67): the
   ty_thymic hint states the Rule K default (D5), the higher code.

Registrar questions the evidence raised (XIf5_thymus_mediastinum.md questions 1-8; registrar
review Q64 to Q71) stay open; the defaults above apply until they are answered.
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, aid, cyto, deposit_node, evidence_gate, excl, go,
                            ihc_node, lab, make_tree, marker, named, node, nonrep,
                            not_malignant_node, nut_nodes, refer, refer_leukaemia,
                            refer_lymphoma, refer_other_named, refer_sarcoma, rule,
                            tail_options, term, live_search_terms)

TREE_ID = "g11_thymus"
P = "ty_"
WHERE = "the thymus or mediastinum"
EVIDENCE = "XIf5_thymus_mediastinum"
THYMUS = "C37.9"
POSTERIOR = "C38.2"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# ICCR p. 8 "usually arise as a single nodule or mass in the thymus in the anterior".
AID_THYMIC = ("Reports place these tumours in the thymus or in the anterior (prevascular) "
              "mediastinum. A report may call a thymoma or thymic carcinoma a thymic epithelial "
              "tumour, and a thymic carcinoid a thymic neuroendocrine tumour.")
# ICCR p. 9 "This rule does not apply to AB thymoma which is a distinct entity" (evidence
# tm_histology option 3 aid).
AID_AB = ("The report records type AB as one type at 100 percent, not as a mixture of type A and "
          "type B.")
# Marx p. 3 "interpretation as malignant tumors (except for micronodular thymoma with lymphoid
# stroma)"; Marx p. 7 "immature T cells on IHC is distinctive compared with micronodular thymoma
# with lymphoid stroma" (evidence tm_histology option 10 aid).
AID_MICRONODULAR = ("The report describes epithelial nodules in a lymphoid stroma that holds "
                    "immature T cells positive for terminal deoxynucleotidyl transferase (TdT).")
# Marx p. 3 "Microscopic thymomas are now considered nodular epithelial hyperplasias" (evidence
# tm_histology option 11 aid).
AID_MICROSCOPIC = "The current name for microscopic thymoma is nodular epithelial hyperplasia."

# ------------------------------------------------------------------------------------------
# Shared clerk-facing sentences
# ------------------------------------------------------------------------------------------
# Evidence lab_tests row 3: ICCR p. 15 "Germ cell tumours may be diagnosed by appropriate
# immunohistochemical stains including SALL4, OCT4, CD117, CD30"; Marx p. 10
# "misinterpretation of SALL4- and AFP-expressing NUT carcinomas as genuine GCTs". Departure 3.
GROUP_X_NO_TISSUE = ("A germ cell tumour diagnosed from imaging with a raised alpha-fetoprotein or "
                     "human chorionic gonadotropin is coded from the Group X tree, which has its "
                     "own route for it: go back and choose Group X (germ cell, trophoblastic and "
                     "gonadal tumours).")
# ICCR p. 8 "present in the lung, where they should be dealt with as primary pulmonary
# neoplasms"; ICCR p. 8 "ectopic TETs have been described in the neck, posterior (paravertebral)
# mediastinum" (evidence tm_site option 8). Departure 1.
OUTSIDE = ("A thymic tumour the report places inside the lung, in the neck or in the thyroid is "
           "coded at that site: go back to the site step and record it there.")
MARKER_TESTS = ("chromogranin A, adrenocorticotropic hormone, alpha-fetoprotein or human "
                "chorionic gonadotropin")
VISSER_T4 = ("Visser O, et al. Front Oncol 2023;13:1250549, Table 4, p. 06 (%s), rule 6, p. 05. "
             "Evidence XIf5_thymus_mediastinum.json tissue_free row %d and tm_lab option %d. No "
             "source in the part gives a serum or plasma test a diagnostic role (data gap 3).")


# ------------------------------------------------------------------------------------------
# The thymoma types (evidence tm_histology options 1-6), ordered by Rossi 2022's paediatric
# counts: B1 20, B2 12, AB 6, A 3, B3 3 of 44 typed thymomas (PMC section 4).
# (label, code, extra sentence for the reason, aid, cite)
# ------------------------------------------------------------------------------------------
THYMOMAS = (
    # ICCR p. 9 "Thymoma, type B1 8583/3"; Rossi PMC section 4 "20 (45%) type B1", "Type B1
    # thymoma was the most frequent", "Patients ranged in age from 0.9 to 17 years".
    ("Thymoma, type B1", "8583", None, None),
    # ICCR p. 9 "Thymoma, type B2 8584/3"; Rossi PMC section 4 "12 (27%) type B2".
    ("Thymoma, type B2", "8584", None, None),
    # ICCR p. 9 "Thymoma, type AB 8582/3"; Rossi PMC section 4 "6 (14%) type AB".
    ("Thymoma, type AB", "8582", None, AID_AB),
    # ICCR p. 9 "Thymoma, type A, including atypical variant 8581/3"; Rossi PMC section 4 "3 (7%)
    # were WHO type A thymomas".
    ("Thymoma, type A, including atypical type A thymoma", "8581", None, None),
    # ICCR p. 9 "Thymoma, type B3 8585/3"; Rossi PMC section 4 "and 3 (7%) type B3".
    ("Thymoma, type B3", "8585", None, None),
    # ICCR p. 9 "Thymoma, NOS 8580/3"; Marx p. 3 "sclerosing thymomas are now considered to
    # represent conventional thymomas with regressive changes"; Rossi PMC section 3 "retained the
    # original description of the thymoma type when a WHO histotype was not assigned";
    # icdo32.sqlite 8580/3 Related Sclerosing thymoma.
    ("Thymoma with no type named, or sclerosing thymoma", "8580",
     "ICD-O-3.2 gives Sclerosing thymoma as a related term of this code.", None),
)
THYMOMA_TYPE_NOT_STATED = ("The report does not name the thymoma's type. A report that names type "
                           "A, AB, B1, B2 or B3 gives that type's own code: go back and take the "
                           "option that names it.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence tm_evidence, tm_lab, tm_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour of the thymus or mediastinum?",
        # Evidence tm_evidence hint; departure 3 adds the Group X sentence.
        hint=("A radiology report counts as imaging. A fine-needle aspiration report counts as "
              "cytology. A pathology report on a biopsy or a resection counts as histology. A "
              "report that calls the specimen inadequate or non-diagnostic counts as no tissue. "
              "%s" % GROUP_X_NO_TISSUE),
        # Evidence lab_tests (departure 3). No source in the part prints a unit.
        labs=[lab("chromogranin_a", "Plasma chromogranin A", ("ng/mL", "µg/L")),
              lab("acth", "Plasma adrenocorticotropic hormone (ACTH)",
                  ("pg/mL", "ng/L", "pmol/L")),
              lab("serum_afp", "Serum alpha-fetoprotein (AFP)",
                  ("ng/mL", "µg/L", "IU/mL", "kU/L")),
              lab("serum_bhcg", "Serum beta human chorionic gonadotropin (β-hCG)",
                  ("IU/L", "mIU/mL"))],
        marker_tests=MARKER_TESTS,
        markers=[
            # Evidence tissue_free row 3 and tm_lab option 1. Marx p. 8 "TNETs are classified
            # into typical carcinoids, atypical carcinoids (ACs), large cell neuroendocrine
            # carcinomas". Visser Table 4, p. 06: neuroendocrine tumour, chromogranin A, 8240/3
            # (contract §0.5: the row names no site).
            marker("8240", test="chromogranin A",
                   diagnosis="carcinoid tumour or neuroendocrine tumour",
                   where="in the thymus or mediastinum",
                   label="Imaging shows a tumour in the thymus or mediastinum, the report calls "
                         "chromogranin A raised, and the file calls it a carcinoid tumour or "
                         "neuroendocrine tumour without naming a hormone it produces",
                   note=VISSER_T4 % ("neuroendocrine tumour, chromogranin A", 3, 1)),
            # Evidence tissue_free row 4 and tm_lab option 2 ("Raised adrenocorticotropic hormone
            # (ACTH) with Cushing syndrome"). Visser Table 4, p. 06: functioning neuroendocrine
            # tumours, adrenocorticotropic hormone, 8158/3. D16 concerns the adrenal cortex only.
            # The diagnosis is worded to follow marker()'s "A %s shown on imaging".
            marker("8158", test="adrenocorticotropic hormone",
                   diagnosis="functioning neuroendocrine tumour producing adrenocorticotropic "
                             "hormone",
                   where="in the thymus or mediastinum",
                   label="Imaging shows a tumour in the thymus or mediastinum, the report calls "
                         "adrenocorticotropic hormone (ACTH) raised with Cushing syndrome, and "
                         "the file calls it an adrenocorticotropic hormone-producing "
                         "(functioning) carcinoid or neuroendocrine tumour",
                   note=VISSER_T4 % ("functioning neuroendocrine tumours, adrenocorticotropic "
                                     "hormone", 4, 2)),
        ],
        tier_labels={
            "cytology": "A cytology report (fine-needle aspiration or fluid) - no histology "
                        "report",
            "histology": "A histology report on a biopsy or resection, with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=[
            # Evidence tm_cytology option 1 ("A named tumour type, such as thymoma, thymic
            # carcinoma or NUT carcinoma"); D8, D9 (departures 1 and 4).
            aid(go("Thymoma, thymic carcinoma or thymic carcinoid (thymic neuroendocrine "
                   "tumour)", n("site_cytology"),
                   note="Evidence tm_cytology option 1; D8, D9 (departure 4)."), AID_THYMIC),
            # Evidence tm_cytology option 1; icdo32.sqlite 8023/3 Synonyms NUT carcinoma, NUT
            # midline carcinoma; ICCR p. 15 "A diagnosis of NUT carcinoma needs
            # immunohistochemical and/or molecular genetic confirmation". D12: the site entered.
            cyto("NUT carcinoma (NUT midline carcinoma)", "8023",
                 "ICD-O-3.2 gives NUT carcinoma and NUT midline carcinoma as synonyms of this "
                 "code.",
                 note="Evidence tm_cytology option 1; D8, D12 (departure 4). The case keeps the "
                      "site entered (registrar review C3, Q66)."),
            # Evidence tm_cytology option 2 ("Carcinoma, with no type named", 8010/3 basis 5);
            # Rules p. 8 (printed p. 21) "Coding is based on what the pathologist states".
            cyto("A carcinoma whose type the cytology report does not name, or names a type not "
                 "listed above", "8010",
                 "A type this list does not hold is recorded with the generic carcinoma code; a "
                 "histology report gives the type's own code.",
                 note="Evidence tm_cytology option 2, widened to the named types the list does "
                      "not hold, as the lung tree does (departure 4; standing rule 8)."),
            # Evidence tm_cytology option 4. Rules p. 2 (printed p. 15): Rule D.
            refer_lymphoma(WHERE),
            # Evidence tm_cytology option 5; Marx p. 9 "9061/3 Seminoma"; ICCC-2017 places 9061,
            # 9071, 9085 and 9084 at C37.9 and C38 in Xb (evidence conflicts, Group 10).
            refer("Germ cell tumour", 10,
                  "Germ cell tumours of the mediastinum belong to ICCC-3 Group X (germ cell, "
                  "trophoblastic and gonadal tumours). Code the case from the Group X tree.",
                  note="Evidence tm_cytology option 5."),
        ],
        note="Evidence tm_evidence and tm_lab (departures 2 and 3 in the module docstring).")
    for nd in nodes:
        if nd["node_id"] == n("imaging_markers"):
            # Departure 3: evidence tm_lab option 3, the Group X referral, as a sentence.
            nd["hint"] = "%s %s" % (nd["hint"], GROUP_X_NO_TISSUE)
    return nodes


# ------------------------------------------------------------------------------------------
# The site step (D9): a thymic tumour type reported in the mediastinum is recorded at C37.9
# ------------------------------------------------------------------------------------------
SITE_QUESTION = "Where does the report place the thymic tumour?"
# Evidence tm_site hint. ICCR p. 8 "usually arise as a single nodule or mass in the thymus in the
# anterior"; icdo32.sqlite code_reference "(C37.9)" beside every 8580/3 to 8586/3 term (Rule H,
# Rules p. 10, printed p. 23 "the tumor is known to arise at another site").
SITE_HINT = ("A thymoma, a thymic carcinoma and a thymic carcinoid arise in the thymus, which lies "
             "in the anterior (prevascular) mediastinum, and ICD-O-3.2 prints the thymus (C37.9) "
             "beside the thymoma and thymic carcinoma terms (WHO coding Rule H). The thymus is "
             "recorded whichever part of the mediastinum the case was entered at, unless the "
             "report says the tumour arose in thymic tissue in the posterior mediastinum. A "
             "tumour that has spread to the pleura or pericardium keeps the site where it began. "
             "%s" % OUTSIDE)
SITE_NOTE = ("D9, the Group III pf_subsite pattern: each option captures topography and continues. "
             "Evidence tm_site options 1, 2 and 4 (departure 1); registrar review Q65 (C37.9 "
             "against the stated mediastinal site). icdo32.sqlite code_reference prints (C37.9) "
             "beside 8580/3 to 8586/3, checked 8 October 2026.")
# Evidence tm_site options 1 and 2: ICCR p. 8 "usually arise as a single nodule or mass in the
# thymus in the anterior"; Rules p. 3 (printed p. 16) "If the diagnosis does not specify the tissue
# of origin, code the appropriate tissues"; Rules p. 2 (printed p. 15) "If no site is indicated in
# the diagnosis, use the suggested code".
LABEL_THYMUS = ("In the thymus, the anterior (prevascular) mediastinum, the mediastinum with no "
                "part named, or the chest")
# Evidence tm_site option 4: ICCR p. 8 "ectopic TETs have been described in the neck, posterior
# (paravertebral) mediastinum"; Rules p. 10 (printed p. 23) "the tumor is known to arise at
# another site".
LABEL_POSTERIOR = ("In the posterior (paravertebral) mediastinum: the report says the tumour arose "
                   "in thymic tissue there")


def site_options(next_node):
    return [
        go(LABEL_THYMUS, next_node, captures={"topography": THYMUS},
           note="Evidence tm_site options 1 and 2: Thymus (C37.9). WHO coding Rules A and H."),
        go(LABEL_POSTERIOR, next_node, captures={"topography": POSTERIOR},
           note="Evidence tm_site option 4: Posterior mediastinum (C38.2), the known site (Rule "
                "H)."),
    ]


def site():
    return node(n("site"), "site_resolution", 4, "Site", SITE_QUESTION, SITE_HINT,
                site_options(n("thymic")), ["topography"], SITE_NOTE)


def site_cytology():
    return node(n("site_cytology"), "site_resolution", 3, "Site", SITE_QUESTION, SITE_HINT,
                site_options(n("cytology_thymic")), ["topography"],
                SITE_NOTE + " Cytology context: the options keep evidence_tests (Cytology).")


def cytology_thymic():
    """ty_cytology_thymic: the thymic types a cytology report names, at basis 5 (D8)."""
    opts = []
    for label, code_, extra, aid_text in THYMOMAS:
        o = cyto(label, code_, extra,
                 note="Evidence tm_cytology option 1 with tm_histology's thymoma line (D8).")
        opts.append(aid(o, aid_text) if aid_text else o)
    opts += [
        # Marx p. 4 "8586/3 Thymic carcinoma, NOS"; evidence tm_cytology option 1 ("thymic
        # carcinoma"). A named subtype understates to the entity's generic code (standing rule 8).
        cyto("Thymic carcinoma, with or without a type named", "8586",
             "A type the cytology report names is confirmed by a histology report, which gives "
             "the type's own code.",
             note="Evidence tm_cytology option 1 (departure 4)."),
        # ICCR p. 10 "Typical carcinoid / neuroendocrine tumour, grade 1 8240/3"; icdo32.sqlite
        # 8240/3 Synonym Carcinoid tumor, NOS.
        cyto("Thymic carcinoid or neuroendocrine tumour, of any grade", "8240",
             "ICD-O-3.2 gives Carcinoid tumor, NOS as a synonym of this code. A histology report "
             "gives the grade.",
             note="Evidence tm_cytology option 1 with tm_picker option 17 (departure 4)."),
    ]
    return node(
        n("cytology_thymic"), "morphology_only", 4, "Cytology",
        "Which thymic tumour does the cytology report name?",
        "Use the cytology report's own conclusion. Cytology gives basis of diagnosis 5; a "
        "histology report gives the full type.",
        opts, [],
        "D8, D9. Evidence tm_cytology option 1 (departure 4): the named types of the histology "
        "screen a cytology report can name, at basis 5.")


# ------------------------------------------------------------------------------------------
# Histology (evidence tm_histology)
# ------------------------------------------------------------------------------------------
def histology():
    referrals = [
        # Marx p. 9 "9061/3 Seminoma"; Marx p. 9 "type I GCTs encompass infantile teratomas and yolk
        # sac tumors". ICCC-2017: 9061, 9071, 9085 at C37.9 and C38 in Xb (evidence conflicts).
        refer("A germ cell tumour: seminoma, embryonal carcinoma, yolk sac tumour, "
              "choriocarcinoma, teratoma or a mixed germ cell tumour", 10,
              "Germ cell tumours of the mediastinum belong to ICCC-3 Group X (germ cell, "
              "trophoblastic and gonadal tumours). Code the case from the Group X tree.",
              note="Evidence tm_histology option 15."),
        # Marx p. 9 "9084/3 Teratoma with somatic-type malignancies"; icdo32.sqlite 9084/3
        # Preferred Teratoma with malignant transformation; ICCC-2017 Xb2 at C37.9 and C38.
        refer("A carcinoma or another cancer that arose in a teratoma (teratoma with "
              "somatic-type malignancy)", 10,
              "A teratoma with a somatic-type malignancy is coded as %s (9084/3), which ICCC-3 "
              "places in Group X, not as a carcinoma. Code the case from the Group X tree."
              % term("9084", "3"),
              note="Evidence tm_histology option 16; conflicts, Group 10."),
    ]
    # Pfister p. 4 "Primary mediastinal (thymic) large B-cell lymphoma"; ICCR p. 15 "may raise the
    # suspicion of non-Hodgkin lymphoma, especially T-lymphoblastic leukaemia/lymphoma". Rules
    # p. 2 (printed p. 15): Rule D.
    lymphoma = refer_lymphoma(WHERE)
    lymphoma["label"] = ("Lymphoma, including mediastinal large B-cell lymphoma, Hodgkin lymphoma "
                         "and T-lymphoblastic lymphoma")
    lymphoma["coding_note"] += (" Evidence tm_histology option 17; ICCC-2017 9679/3 IIb2 and "
                                "9837/3 IIb1 at C37.9 and C38.")
    # Rules p. 6 (printed p. 19) "Code all leukemias except myeloid sarcoma (9930/3) to C42.1
    # (bone marrow)".
    leukaemia = refer_leukaemia(WHERE)
    leukaemia["label"] = "T-lymphoblastic leukaemia, or another leukaemia"
    leukaemia["coding_note"] += " Evidence tm_histology option 18."
    # Marx p. 10 "Primary intrathoracic synovial sarcoma is uncommon"; Marx p. 11 "9364/3 Ewing
    # sarcoma".
    sarcoma = refer_sarcoma(WHERE, label="A sarcoma, such as synovial sarcoma, rhabdomyosarcoma, "
                                         "Ewing sarcoma, liposarcoma or malignant peripheral "
                                         "nerve sheath tumour")
    sarcoma["coding_note"] = ("Evidence tm_histology option 20. ICCC-2017 at C37.9 and C38: 9040 "
                              "IXd7, 8900 IXa, 9364 IXd2, 9540 IXb2, 8850/3 IXd4 (evidence "
                              "conflicts, Group 9).")
    referrals += [
        lymphoma, leukaemia,
        # Marx p. 10 "ganglioneuroblastoma, ganglioneuroma) occur in the posterior mediastinum";
        # Marx p. 11 "8693/3 Extra-adrenal paraganglioma". ICCC-2017: 9500, 9490 IVa; 8693 IVb.
        refer("Neuroblastoma, ganglioneuroblastoma or paraganglioma", 4,
              "Neuroblastoma, ganglioneuroblastoma and paraganglioma belong to ICCC-3 Group IV "
              "(neuroblastoma and other peripheral nervous cell tumours). Code the case from the "
              "Group IV tree.",
              note="Evidence tm_histology option 19; conflicts, Group 4. The case keeps its site."),
        sarcoma,
        # ICCR p. 10 "Carcinosarcoma 8980/3". ICCC-2017 places 8980 in XIIa4 at every site.
        refer("Carcinosarcoma", 12,
              "ICD-O-3.2 codes carcinosarcoma as %s (8980/3), which ICCC-3 places in Group XII "
              "(other and unspecified malignant neoplasms). Code the case from the Group XII "
              "tree." % term("8980", "3"),
              note="Evidence tm_histology option 21; conflicts, Group 12."),
        refer_other_named(),
    ]
    opts = [
        # Evidence tm_histology options 1-6 and tm_picker's thymic carcinomas and carcinoids,
        # gathered behind the site step (D9, departures 1 and 5). ICCR p. 8 "usually arise as a
        # single nodule or mass in the thymus in the anterior".
        aid(go("Thymoma, thymic carcinoma or thymic carcinoid (thymic neuroendocrine tumour), of "
               "any type", n("site"), note="D1, D9 (departures 1 and 5)."), AID_THYMIC),
        # Evidence tm_histology option 9. Rules p. 8 (printed p. 21) "Coding is based on what the
        # pathologist states".
        named("A carcinoma whose type the report does not name", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence tm_histology option 9; data gap 6 (no paediatric source; a generic "
                   "option)."),
    ] + tail_options(
        P, "mucosa", where=WHERE, nut=True,
        not_malignant_label="A tumour the report calls benign or of uncertain behaviour, thymic "
                            "hyperplasia, or a thymic cyst",
        referrals=referrals)
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence tm_histology hint (departure 5).
        "Use the report's final diagnosis. A thymoma, a thymic carcinoma or a thymic carcinoid of "
        "any type takes the first option, which asks where the report places it. A tumour the "
        "report calls benign is not recorded. NUT carcinoma is recorded at the site entered at "
        "the start: the thymus (C37.9) only when the report names the thymus. %s" % OUTSIDE,
        opts, [],
        "Evidence tm_histology (departures 5 and 6). D12: NUT carcinoma keeps the case's site "
        "(registrar review C3, Q66).")


# Registrar ruling of 8 October 2026 on review A1 (a)(b), registrar_A1ab_rules.md C5 and C4:
# ICD-O-3.1 section 4.2.2, p. 16 (a site noun and its adjective name the same site) and Rule K,
# p. 24. The controller's reading: Thymic carcinoma, NOS is a not-otherwise-specified term, so a
# specified type replaces it, and Rule K is not used.
NOS_REPLACED = ("%s (8586/3) is a not-otherwise-specified term, so a specified type replaces it."
                % term("8586", "3"))
THYMIC_TYPE_SENTENCE = (
    "A name written thymic carcinoma, hepatoid type is the same tumour as a hepatoid carcinoma of "
    "the thymus: the word thymic names the site. Record the type's code, not %s (8586/3). "
    "%s is a not-otherwise-specified term, so a specified type replaces it; this is not a choice "
    "by the higher code (WHO coding Rule K), because a not-otherwise-specified term and a "
    "specified type are not two modifiers that no single code covers."
    % (term("8586", "3"), term("8586", "3")))


def thymic():
    """ty_thymic: the thymic tumour types, after the site step (D9)."""
    opts = []
    for label, code_, extra, aid_text in THYMOMAS:
        o = named(label, code_, extra,
                  note="D1: Rossi 2022, PMC section 4 (evidence tm_histology).",
                  upgrade=THYMOMA_TYPE_NOT_STATED if code_ == "8580" else None)
        opts.append(aid(o, aid_text) if aid_text else o)
    opts += [
        # Marx p. 4 "hepatoid carcinoma, rhabdoid carcinoma, undifferentiated large cell carcinoma
        # associated with Castleman disease-like reaction" (Table 1 footnote g, under 8586/3). This
        # one option recorded 8586/3 for all four wordings, awaiting the registrar (review A1, Q68).
        # Registrar ruling of 8 October 2026 on review A1 (a)(b): the WHO ICD-O-3 coding Rules A to
        # K decide, and docs/group_11_evidence/registrar_A1ab_rules.md (C4a to C4d) applies them.
        # The reading the controller fixed: Thymic carcinoma, NOS (8586/3) is a not-otherwise-
        # specified term, so a specified type replaces it; Rule K (ICD-O-3.1 p. 24) is not used,
        # because a NOS term and a specified type are not two modifiers that no single code covers.
        # C4a: ICD-O-3.1 section 4.3.3, p. 21 (the term printed) and Rule H, p. 23 (the site is
        # stated); icdo32.sqlite 8576/3 Synonym "Hepatoid carcinoma".
        named("Hepatoid carcinoma or hepatoid adenocarcinoma of the thymus", "8576",
              "ICD-O-3.2 lists Hepatoid carcinoma as a term of this code, and the code follows "
              "the term the report uses. %s" % NOS_REPLACED,
              note="Registrar ruling 8 October 2026 (review A1 (a), Q68), "
                   "registrar_A1ab_rules.md C4a: ICD-O-3.1 section 4.3.3, p. 21; Rule H, p. 23. "
                   "Evidence tm_picker option 16 (departure 9)."),
        # C4b: ICD-O-3.1 Rule H, pp. 15 and 23: ICD-O-3.2 prints C44._ beside 8410/3 and the
        # report places the tumour in the thymus, so the skin topography is disregarded and the
        # morphology code is kept (the manual's infiltrating duct carcinoma of the pancreas).
        named("Sebaceous carcinoma of the thymus", "8410",
              "ICD-O-3.2 prints the skin beside this term; the report places the tumour in the "
              "thymus, so the skin is disregarded (WHO coding Rule H). %s" % NOS_REPLACED,
              note="Registrar ruling 8 October 2026 (review A1 (a), Q68), "
                   "registrar_A1ab_rules.md C4b: ICD-O-3.1 Rule H, pp. 15 and 23."),
        # C4c: ICD-O-3.1 Rule J, p. 24: ICD-O-3.2 prints no term "rhabdoid carcinoma" and
        # reordering its words reaches none; Rule K does not apply (rhabdoid is the only modifier).
        # The code stays 8586/3 (the NOS fallback; 8963/3 Rhabdoid tumor, NOS is a Group IX code at
        # C37.9 and is not used). The picker holds 8014/3 for a report that says large cell
        # carcinoma with rhabdoid phenotype.
        named("Rhabdoid carcinoma of the thymus", "8586",
              "ICD-O-3.2 has no term for rhabdoid carcinoma, and reordering its words reaches no "
              "listed term (WHO coding Rule J), so no specified type replaces the "
              "not-otherwise-specified term. A report that calls the tumour a large cell "
              "carcinoma with a rhabdoid phenotype is found in the picker as %s (8014/3)."
              % term("8014", "3"),
              note="Registrar ruling 8 October 2026 (review A1 (a), Q68), "
                   "registrar_A1ab_rules.md C4c: ICD-O-3.1 Rule J, p. 24. Code unchanged."),
        # C4d: ICD-O-3.1 Rule G, pp. 15 and 22 (Table 21): undifferentiated is a grade word and
        # does not change the type's code (the manual's anaplastic squamous cell carcinoma example
        # is coded 8070/3). The Castleman disease-like reaction has no morphology term.
        named("Undifferentiated large cell carcinoma of the thymus, including one with a "
              "Castleman disease-like reaction", "8012",
              "Undifferentiated is a grade, and a grade does not change the code (WHO coding "
              "Rule G). The Castleman disease-like reaction has no ICD-O-3.2 term. %s"
              % NOS_REPLACED,
              note="Registrar ruling 8 October 2026 (review A1 (a), Q68), "
                   "registrar_A1ab_rules.md C4d: ICD-O-3.1 Rule G, pp. 15 and 22."),
        # Marx p. 7 "expression of one or more enteric markers, CK20, CDX2, or MUC2".
        go("Thymic adenocarcinoma with CK20, CDX2 or MUC2 stain results, and no type named",
           n("ihc"), note="Evidence tm_picker option 9 (departure 10)."),
        go("Another thymic carcinoma, a thymic carcinoid or neuroendocrine tumour, a "
           "neuroendocrine carcinoma, or metaplastic thymoma - type its name to find it",
           n("picker"),
           note="Evidence tm_histology option 8: D2, the Group XI picker (departure 8). D1: no "
                "paediatric source reports thymic carcinoma, the thymic neuroendocrine tumours or "
                "metaplastic thymoma (data gap 1; registrar review Q64)."),
        go("A thymic tumour the report calls benign or of uncertain behaviour, such as "
           "micronodular thymoma with lymphoid stroma or microscopic thymoma", n("not_malignant"),
           note="The exclusion screen (contract §4.2)."),
    ]
    return node(
        n("thymic"), "histology_subclassification", 5, "Thymic tumour type",
        "Which thymic tumour does the histology report name?",
        # Evidence tm_histology hint (the thymoma-type sentence); ICCR p. 9 "This rule does not
        # apply to AB thymoma which is a distinct entity"; Rules p. 11 (printed p. 24) Rule K.
        "Use the report's final diagnosis. When the report lists more than one thymoma type in "
        "one tumour, choose the type with the higher code number (WHO coding Rule K): A 8581, AB "
        "8582, B1 8583, B2 8584, B3 8585. Type AB is a single type. A thymoma combined with a "
        "thymic carcinoma or carcinoid in one tumour is coded the same way: every thymoma code is "
        "higher than every thymic carcinoma and carcinoid code except Thymic carcinoma, NOS "
        "(8586). " + THYMIC_TYPE_SENTENCE,
        opts, [],
        "Evidence tm_histology options 1-6 (departure 5), tm_picker options 9 and 16 (departures "
        "9 and 10). D5: combined thymic carcinoma and thymoma takes the Rule K default, the "
        "higher code, as the registrar ruled for two modifiers no single code covers on 7 "
        "October 2026 (registrar review Q67, open).")


def ihc():
    marker_note = ("Evidence ihc_rules %d. Marx p. 7 'expression of one or more enteric markers, "
                   "CK20, CDX2, or MUC2'; Marx p. 4 'with expression of at least one intestinal "
                   "marker, CK20, CDX2, or MUC2'.")
    reason = ("%s is positive: one intestinal marker makes a thymic adenocarcinoma enteric type "
              "(Marx 2022, p. 4 and p. 7). " + "Recorded as %s (8144/3)." % term("8144", "3"))
    return ihc_node(
        P,
        [{"group_label": "Intestinal (enteric) markers", "markers": ["CK20", "CDX2", "MUC2"]}],
        [
            rule(["CK20"], "8144", reason % "CK20", note=marker_note % 1),
            rule(["CDX2"], "8144", reason % "CDX2", note=marker_note % 2),
            rule(["MUC2"], "8144", reason % "MUC2", note=marker_note % 3),
        ],
        fallback="8140",
        fallback_reason=("No intestinal marker (CK20, CDX2 or MUC2) is reported positive. Recorded "
                         "as %s (8140/3)." % term("8140", "3")),
        # Evidence tm_adeno_ihc hint.
        hint="The histology report calls the tumour an adenocarcinoma of the thymus without "
             "naming its type. Answer CK20, CDX2 and MUC2 as the report states them, and 'Not "
             "done or not readable' for a stain the report does not mention. One positive "
             "intestinal marker records Adenocarcinoma, intestinal type (8144/3); with none "
             "positive, the tumour is recorded as Adenocarcinoma, NOS (8140/3).",
        note="Evidence tm_adeno_ihc and ihc_rules 1-4 (departure 11). Rule 4 (CK20, CDX2 and MUC2 "
             "negative -> 8140/3) is the NOS fallback: Marx p. 7 'expression of one or more "
             "enteric markers, CK20, CDX2, or MUC2'. No other marker panel in the part decides "
             "between codes (evidence §4: ICCR p. 15, Marx pp. 8-9).",
        step=6)


def not_malignant():
    return not_malignant_node(
        P,
        [
            # ICCR p. 9 "Micronodular thymoma with lymphoid stroma 8580/1"; Marx p. 3
            # "interpretation as malignant tumors (except for micronodular thymoma with lymphoid
            # stroma)".
            aid(excl("Micronodular thymoma with lymphoid stroma", "8580", "1",
                     what="a micronodular thymoma with lymphoid stroma",
                     note="Evidence tm_histology option 10. D6: a report calling it malignant is "
                          "not given a stated-behaviour code."),
                AID_MICRONODULAR),
            # Marx p. 3 "Microscopic thymomas are now considered nodular epithelial
            # hyperplasias"; Rules p. 2 (printed p. 15) "the pathologist states that the behavior
            # differs from the usual behavior as given in ICD-O"; icdo32.sqlite 8580/0 Related
            # Thymoma, benign.
            aid(excl("Microscopic thymoma, or a thymoma the report calls benign", "8580", "0",
                     what="a microscopic thymoma, and a thymoma the report calls benign,",
                     extra="ICD-O-3.2 gives Thymoma, benign as a related term of this code, and "
                           "the behaviour the report states is coded (WHO coding Rule F).",
                     decision=True,
                     note="Evidence tm_histology option 11; registrar review Q69 (the World "
                          "Health Organization counts every thymoma but micronodular thymoma "
                          "with lymphoid stroma as malignant, Marx 2022, p. 3)."),
                AID_MICROSCOPIC),
            # ICCR p. 14 "nodular epithelial hyperplasia, previously called"; ICCR p. 14 "Cystic
            # changes can involve both thymic epithelial tumours and adjacent thymus".
            nonrep("Nodular epithelial hyperplasia, thymic hyperplasia or a thymic cyst",
                   "Not registrable. These are not tumours.",
                   note="Evidence tm_histology option 12."),
            # ICCR p. 9 "Lipofibroadenoma 9010/0"; icdo32.sqlite 9010/0 Related Lipofibroadenoma.
            excl("Lipofibroadenoma", "9010", "0", what="lipofibroadenoma",
                 extra="ICD-O-3.2 gives Lipofibroadenoma as a related term of this code.",
                 note="Evidence tm_histology option 13."),
            # Marx p. 11 "8850/0 Thymolipoma"; icdo32.sqlite 8850/0 Related Thymolipoma.
            excl("Thymolipoma", "8850", "0", what="thymolipoma",
                 extra="ICD-O-3.2 gives Thymolipoma as a related term of this code. A liposarcoma "
                       "is a sarcoma: take the sarcoma option at the step before.",
                 note="Evidence tm_histology option 14; conflicts, Group 9 (8850/0 against "
                      "8850/3)."),
        ],
        where=WHERE,
        note="The four exclusions and the hyperplasia line of evidence tm_histology (departures "
             "5 and 12).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
# Evidence tm_picker hint (departure 8). Rules p. 11 (printed p. 24) Rule K; Rules p. 8 (printed
# p. 21) Rule G.
PICKER_HINT = (" When the report names two tumour types in one tumour and no entry covers both, "
               "choose the one with the higher code number (WHO coding Rule K). When the report "
               "gives two grades of carcinoid or neuroendocrine tumour, choose the higher grade "
               "(WHO coding Rule G).")


def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [site_cytology(), cytology_thymic(), histology(), site(), thymic(), ihc()] \
        + nut_nodes(P) + [not_malignant(), deposit_node(P, where=WHERE)]
    tree = make_tree(
        TREE_ID, nodes,
        subtype_screens=(n("thymic"),),
        # Departure 8: ty_thymic offers 8580/3 and 8586/3 under narrower labels; the picker keeps
        # them for metaplastic thymoma and thymic carcinoma, NOS. Departure 9 (registrar ruling of
        # 8 October 2026, registrar_A1ab_rules.md C4): 8576/3, 8410/3 and 8012/3 are now options of
        # ty_thymic under narrower labels too (hepatoid; sebaceous; undifferentiated large cell), and
        # the picker keeps them so that a clerk who types the term reaches each, as before the ruling.
        picker_keep=("8580", "8586", "8576", "8410", "8012"))
    picker = next(nd for nd in tree["nodes"] if nd["node_id"] == n("picker"))
    picker["hint"] += PICKER_HINT
    # Registrar ruling of 8 October 2026 on review A1 (a)(b), registrar_A1ab_rules.md C12
    # (ICD-O-3.1 section 4.3.3, p. 21; Rule G, p. 22): ICD-O-3.2 prints Neuroendocrine tumor,
    # grade 3 as a Related term of 8249/3, whose Preferred term reads grade 2. The code is
    # unchanged; the reason says why a report of grade 3 is recorded here.
    grade3 = "Neuroendocrine tumor, grade 3"
    assert grade3 in live_search_terms("8249", "3"), "ICD-O-3.2 no longer lists %s" % grade3
    for o in picker["options"]:
        if o.get("morphology_code") == "8249":
            o["reason"] += (" ICD-O-3.2 lists %s as a related term of this code, so a report that "
                            "says grade 3 is recorded here." % grade3)
    picker["coding_note"] += (" Hint extended with evidence tm_picker's Rule K and Rule G "
                              "sentences (thymus.py departure 8).")
    return tree


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
_IHC = ["Histology", "IHC"]
DECISIONS = {
    "8583/3": ("D1, D8, D9", EVIDENCE,
               "Thymoma, type B1, the commonest paediatric thymoma (Rossi 2022, PMC section 4), "
               "on the thymic type screen after the site step, and at basis 5 when cytology "
               "names it; recorded at the thymus (C37.9) unless the report places it in the "
               "posterior mediastinum."),
    "8584/3": ("D1, D8, D9", EVIDENCE,
               "Thymoma, type B2 (Rossi 2022, PMC section 4) on the thymic type screen and at "
               "basis 5 from cytology, at the site the site step records."),
    "8582/3": ("D1, D8, D9", EVIDENCE,
               "Thymoma, type AB (Rossi 2022, PMC section 4) on the thymic type screen and at "
               "basis 5 from cytology, at the site the site step records."),
    "8581/3": ("D1, D8, D9", EVIDENCE,
               "Thymoma, type A, including atypical type A thymoma (ICCR Thymic Epithelial, p. 9; "
               "Rossi 2022, PMC section 4), on the thymic type screen and at basis 5 from "
               "cytology."),
    "8585/3": ("D1, D8, D9", EVIDENCE,
               "Thymoma, type B3 (Rossi 2022, PMC section 4) on the thymic type screen and at "
               "basis 5 from cytology."),
    "8580/3": ("D1, D2, D8, D9", EVIDENCE,
               "Thymoma, NOS for a thymoma with no type named or a sclerosing thymoma (Rossi 2022, "
               "PMC section 3) on the thymic type screen and at basis 5 from cytology, and in "
               "the thymus picker, where metaplastic thymoma finds it."),
    "8586/3": ("D2, D8, D9", EVIDENCE,
               "Thymic carcinoma, NOS: in the thymus picker; on the thymic type screen for "
               "rhabdoid carcinoma of the thymus, which ICD-O-3.2 does not print and word order "
               "does not reach another code (WHO coding Rule J; registrar ruling of 8 October "
               "2026 on review A1, Q68); and at basis 5 when cytology names a thymic carcinoma."),
    "8576/3": ("D1, D2, D9", EVIDENCE,
               "Hepatoid adenocarcinoma in the thymus picker and on the thymic type screen, for "
               "hepatoid carcinoma and hepatoid adenocarcinoma of the thymus, which ICD-O-3.2 "
               "prints under this code (registrar ruling of 8 October 2026 on review A1, Q68: ICD-O-3.1 section 4.3.3, "
               "p. 21; the World Health Organization table's 8586/3, Marx 2022, p. 4, footnote g, "
               "is not a rule of the manual)."),
    "8410/3": ("D1, D2, D9", EVIDENCE,
               "Sebaceous carcinoma in the thymus picker and on the thymic type screen, for "
               "sebaceous carcinoma of the thymus: ICD-O-3.2 prints the skin beside the term and "
               "the report states the thymus (WHO coding Rule H, ICD-O-3.1 pp. 15 and 23; registrar ruling of 8 October "
               "2026 on review A1, Q68)."),
    "8012/3": ("D1, D2, D9", EVIDENCE,
               "Large cell carcinoma, NOS in the thymus picker and on the thymic type screen, for "
               "undifferentiated large cell carcinoma of the thymus with or without a Castleman "
               "disease-like reaction: undifferentiated is a grade and does not change the code "
               "(WHO coding Rule G, ICD-O-3.1 pp. 15 and 22; registrar ruling of 8 October 2026 on "
               "review A1, Q68)."),
    "8023/3": ("D8, D12, D15", EVIDENCE + ", NUT_carcinoma",
               "NUT carcinoma of the thymus or mediastinum (Marx 2022, p. 4; ICCR Thymic "
               "Epithelial, p. 15) from the NUT carcinoma screens, basis 8 with a NUTM1 "
               "rearrangement or fusion and basis 7 otherwise, and at basis 5 when cytology names "
               "it; recorded at the site the report gives (registrar review Q66)."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma of the thymus or mediastinum whose type the report does not name, at "
               "basis 7 on the histology screen and at basis 5 when cytology names a carcinoma "
               "without its type or a type the cytology list does not hold."),
    "8240/3": ("D2, D7, D8", EVIDENCE,
               "Neuroendocrine tumor, NOS: thymic carcinoid at basis 5 when cytology names it, at "
               "basis 4 with imaging and a raised chromogranin A (Visser 2023 Table 4; evidence "
               "data gap 3), and in the thymus picker."),
    "8158/3": ("D7", EVIDENCE,
               "Adrenocorticotropic hormone-producing neuroendocrine tumour of the thymus or "
               "mediastinum at basis 4 with imaging, a raised adrenocorticotropic hormone and "
               "Cushing syndrome (Visser 2023 Table 4; evidence data gap 3)."),
    "8144/3": ("D2", EVIDENCE,
               "Thymic adenocarcinoma, enteric type from the stain panel (CK20, CDX2 or MUC2 "
               "positive; Marx 2022, p. 4 and p. 7) and in the thymus picker.",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["CK20", "CDX2", "MUC2"]}),
    "8140/3": ("D2", EVIDENCE,
               "Adenocarcinoma, NOS as the thymus stain panel's fallback when no intestinal marker "
               "is positive (Marx 2022, p. 7), and in the thymus picker."),
}
