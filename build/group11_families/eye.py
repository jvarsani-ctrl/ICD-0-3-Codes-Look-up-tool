"""g11_eye (prefix ey_): carcinomas of the eye, lacrimal gland and orbit at C69.0-C69.9, ICCC-3
subgroup XIf9.

A family tree (contract §4.1) over one organ system with four parts: the surface of the eye
(conjunctiva and cornea), the lacrimal gland and its drainage passages, the inside of the eye
(retina, choroid, ciliary body) and the orbit. It is built from docs/group_11_evidence/XIf9_eye.json
(the evidence agent's nodes ey_evidence, ey_cytology, ey_site, ey_surface_histology,
ey_lacrimal_histology, ey_intraocular_histology, ey_orbit_histology, ey_carcinoma_other and
ey_deposit; the part has no ihc_rules and no lab_tests) with the builders in
build/group11_common.py, in the shape of build/group11_organs/thyroid.py. Every option's label,
code, behaviour, basis, reason and recognition aid comes from that file unless a departure below
says otherwise; the cite (file, PDF page, quotation) is the comment above the option. File names in
the comments are the evidence's own:
    Milman    XIf9-eye-XId-ocular-melanoma__Milman-2023.txt (Milman T, et al. The 5th Edition of the
              World Health Organization Classification of Tumours of the Eye and Orbit. Ocul Oncol
              Pathol 2023;9:71-95)
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser    Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
              set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    ey_document_inventory  document_inventory  evidence gate (evidence ey_evidence)
    ey_clinical, ey_clinical_cytology  clinical_alias
    ey_imaging, ey_imaging_cytology    morphology_only
    ey_cytology            morphology_only     (evidence ey_cytology)
    ey_histology           histology_subclassification  (D14: the four histology screens of the
                                               evidence, in one, with the exclusions grouped by
                                               part of the eye)
    ey_site                site_resolution     (D9; the part of the eye, for a site recorded C69.8
                                               or C69.9)
    ey_not_malignant       histology_subclassification  (the exclusions of the four screens)
    ey_deposit             morphology_only      (D10)
    ey_picker              histology_subclassification  (D2; evidence ey_carcinoma_other)

Departures from the evidence nodes, and why
-------------------------------------------
1. ey_evidence: the gate's options are the contract §4.2 tiers (D7). Its first option, "the file
   names retinoblastoma or retinocytoma", is not an option of the common gate, whose tiers the
   document checklist chooses from the reports ticked. A referral to Group V on a clinical-note
   or imaging screen is a tissue-free path that refers to a group other than XII, which the
   walk rejects (tissue-free paths emit only Group XII referrals, not-registrable lines, or a
   Visser Table 4 code), so the referral is on ey_cytology and ey_histology only. The gate's hint
   tells the clerk that retinoblastoma is recorded in Group V on an eye examination or imaging,
   and is not coded from this tree (Milman p. 11 "Generally, biopsy is avoided due to the risk of
   extraocular recurrence and metastasis"). Without that, an imaging-only retinoblastoma records
   8000/3 (XIIb); the request is in the return. The evidence's 8000/3 lines at basis 1 and 2 are
   the common Group XII referrals (D7: ICCC-2017 range 143 places 8000/3 at C69 in XIIb). The
   gate has no laboratory screen and no marker tier: the evidence gives no laboratory test and
   Visser Table 4 names no eye entity.
2. ey_site is kept only where the router's site capture leaves the part of the eye open (D14, D9).
   The router records C69.0 to C69.9 and chooses this tree, so the evidence's site question is
   one the router answers. ey_site is reached from ey_histology by one option, for a site
   recorded as overlapping lesion of eye and adnexa (C69.8) or eye, part not stated (C69.9)
   when the report names the part where the tumour began (Rule H). Its options capture the part
   (C69.0 to C69.6) and return to ey_histology. The evidence's other site options leave to other
   trees or other screens and are not repeated: the eyelid (C44.1; departure 5), the optic nerve
   (C72.3; departure 4), the periorbital region (C76.0, Rule B: a router answer) and the deposit
   (ey_histology's deposit option). The evidence's C69.8 and C69.9 options are the router's.
3. ey_surface_histology, ey_lacrimal_histology, ey_intraocular_histology and ey_orbit_histology
   are one screen, ey_histology (D14: the engine cannot filter options by site inside one tree).
   Every option of those screens that is not a part-specific exclusion is common to the four, so
   the merge drops nothing: retinoblastoma, medulloepithelioma, melanoma, lymphoma, rhabdomyosarcoma
   and other soft tissue sarcoma, myeloid sarcoma (departure 6), Langerhans cell histiocytosis,
   germ cell tumours, bone tumour of the orbit, carcinoma of unstated type, the carcinoma picker,
   the exclusions and the deposit. The exclusions keep their part of the eye in the label and
   the reason (ey_not_malignant).
4. Optic nerve, medulloepithelioma. The optic nerve is C72.3, a central nervous system site.
   "An optic nerve tumour (glioma or medulloepithelioma)" refers to Group III and captures C72.3
   (evidence ey_site option 11; ICCC-2017 places 9501 at C70-C72 in IIIc3 and 9421 in IIIb).
   Medulloepithelioma of the eye (ciliary body, 9501/3) refers to Group IV (ICCC-2017 range IVb
   outside the central nervous system), as the brief and the evidence's conflicts row 2 give.
5. Eyelid and sebaceous carcinoma. The eyelid is skin (C44.1) and belongs to the skin tree, which
   routes C44.x. A referral to Group XI itself is built only with SELF_REFERRAL (D10), which is
   False, and a hop to sk_histology without the topography capture would emit skin codes at C69
   sites. ey_histology therefore carries one non-reportable line, "A tumour of the eyelid,
   including sebaceous carcinoma", whose reason says the eyelid is a skin site, to be recorded at
   C44.1 from the site step. Evidence ey_surface_histology option 2 (hop to sk_histology) and
   ey_site option 10 become that line. With SELF_REFERRAL enabled, the line becomes a Group XI
   referral with recapture_site.
6. Myeloid sarcoma of the orbit (evidence ey_orbit_histology option 3, Group I keeping the orbit)
   is not built as its own option: check_leukaemia_referrals_record_marrow admits a site-keeping
   Group I referral only on the nodes it lists, and refer_leukaemia records C42.1, which would
   misplace an orbital myeloid sarcoma (Rule E). The standard leukaemia line is kept; the request
   is in the return.
7. Carcinomas. Ruling 1 makes an entity an option only when a source reports it in children; no
   source reports an eye carcinoma in a child (evidence data gap 1; Pfister Table 3 lists none).
   So the evidence's ey_carcinoma_other is the common picker (D2), and the screen offers
   carcinoma of unstated type (8010/3) only. D2 puts every XIf9 code valid at all routed sites
   in the picker; the evidence's Milman-first ordering and its recognition aids (squamous cell
   carcinoma, adenosquamous, mucoepidermoid and the lacrimal types) are not carried, because the
   picker's options are the Preferred-term options of picker_node(). The picker's hint names the
   part of the eye and Rule H: the salivary-gland site printed beside 8941/3, the breast site
   beside 8500/3 and the skin site beside 8410/3 do not apply at the eye.
8. Malignant mixed tumour of the lacrimal gland (evidence ey_lacrimal_histology option 2, 8940/3,
   Group XII: ICCC-2017 XIIa4 at every site) is a Group XII referral on ey_histology.
9. ey_cytology: "Another carcinoma the report names" (go ey_carcinoma_other) is not built. The
   picker holds every carcinoma at basis 7, and the engine takes the basis from the gate answer,
   so a cytology route into it would record basis 7 on a case with no histology. Squamous cell
   carcinoma and adenocarcinoma are the two named entities (D8), and a carcinoma of any other
   type is "carcinoma, type not stated" (8010/3 at basis 5). "Melanoma" is D8's 8720/3 at basis 5,
   not the hop, because the melanoma tree's screens record basis 7 (breast departure 4).
   Retinoblastoma, medulloepithelioma and lymphoma are the evidence's referrals.
10. Not built from the evidence: squamous cell carcinoma with mucinous differentiation
   (registrar question; its code 8070/3 is the squamous cell carcinoma option, with Rule K giving
   8480/3 if the registrar rules so), and oncocytic carcinoma of the lacrimal gland (8290/3), which
   WHO Eye5 removed as obsolete and ICD-O-3.2 keeps current. The picker offers 8290/3 because the
   XIf9 inventory holds it; the registrar decides (evidence code_currency). Codes the WHO prints
   that ICD-O-3.2 lacks are not built (D4).

Registrar questions of the evidence stay open; the defaults above apply until they are answered
(docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, cyto, cyto_carcinoma_nos, deposit_node,
                            evidence_gate, excl, go, make_tree, named, node, nonrep,
                            not_malignant_node, refer, refer_germ_cell, refer_leukaemia,
                            refer_other_named, refer_sarcoma, tail_options, term)

TREE_ID = "g11_eye"
P = "ey_"
WHERE = "the eye, the lacrimal gland or the orbit"
EVIDENCE = "XIf9_eye"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Shared referrals
# ------------------------------------------------------------------------------------------
def retinoblastoma(label="Retinoblastoma, or retinocytoma (retinoma)", note=None):
    # Pfister p. 12 "Retinocytoma Retinoblastoma Medulloepithelioma"; Milman p. 11 "Generally,
    # biopsy is avoided due to the risk of extraocular recurrence and metastasis"; Milman p. 8
    # "Retinocytoma is classified as a premalignant tumor"; ICCC-2017 places 9510-9514 in Group V
    # at every site.
    return refer(label, 5,
                 "%s is recorded in ICCC-3 Group V, which registers it on an eye examination or "
                 "imaging, because a biopsy of the eye is usually avoided. Code the case from the "
                 "Group V (retinoblastoma) tree." % term("9510", "3"),
                 note=note or "Evidence ey_evidence option 0, ey_intraocular_histology option 0 "
                              "and ey_orbit_histology option 8; ICCC-2017 places 9510-9514 in "
                              "Group V at every site.")


def medulloepithelioma():
    # Pfister p. 12 "Retinocytoma Retinoblastoma Medulloepithelioma"; Milman p. 10
    # "Medulloepithelioma of the ciliary body"; ICCC-2017 places 9501-9504 at C00-C69 in IVb.
    return refer("Medulloepithelioma (diktyoma) of the eye, including teratoid "
                 "medulloepithelioma", 4,
                 "%s (9501/3) of the eye, such as the ciliary body, is recorded in ICCC-3 Group "
                 "IV (neuroblastoma and other peripheral nervous cell tumours), outside the "
                 "central nervous system. Code the case from the Group IV tree."
                 % term("9501", "3"),
                 note="Evidence ey_intraocular_histology option 1 and ey_cytology option 6. "
                      "ICCC-2017 places 9501-9504 at C00-C69 in IVb. Departure 4.")


def optic_nerve():
    # Milman p. 12 "Gliomas of the optic nerve"; Pfister p. 12 "Pilocytic astrocytoma and other
    # gliomas of the optic nerve"; ICCC-2017 places 9421 in IIIb and 9501 at C70-C72 in IIIc3.
    return refer("A tumour of the optic nerve, such as a glioma or a medulloepithelioma", 3,
                 "A tumour of the optic nerve is recorded at the optic nerve (C72.3), a central "
                 "nervous system site, in ICCC-3 Group III. Code the case from the Group III "
                 "(central nervous system tumours) tree.",
                 captures={"topography": "C72.3"},
                 note="Evidence ey_site option 11. Departure 4. ICCC-2017: 9421 IIIb, 9501 at "
                      "C70-C72 IIIc3.")


def lymphoma(label="Lymphoma, including a lymphoma inside the eye"):
    # Milman p. 16 "Ocular adnexal lymphomas", "Primary vitreoretinal large cell B-cell lymphoma";
    # Rules p. 2 (printed p. 15) "Code extranodal lymphomas to the site of origin".
    return refer(label, 2,
                 "A lymphoma belongs to ICCC-3 Group II. A lymphoma that arises in the eye, the "
                 "lacrimal gland or the orbit keeps the part of the eye where it arose (WHO Rule "
                 "D: an extranodal lymphoma is coded to its site of origin). Code the case from "
                 "the Group II (lymphomas) tree.",
                 note="ICD-O-3.1 Rule D, p. 15. The hop carries the case's site. Evidence "
                      "ey_cytology option 7 and the lymphoma options of the four histology "
                      "screens.")


def histiocytosis():
    # Milman p. 16 "Langerhans cell tumors"; ICCC-2017 places 9751 in IId.
    return refer("Langerhans cell histiocytosis of the orbit", 2,
                 "%s (9751/1) is recorded in ICCC-3 Group II, which decides its behaviour and "
                 "whether it registers. Code the case from the Group II tree." % term("9751", "1"),
                 note="Evidence ey_orbit_histology option 5. ICCC-2017 places 9751 in IId.")


def malignant_mixed():
    # Rules p. 2 "code as the pathologist indicates"; ICCC-2017 places 8940 in XIIa4 at every
    # site; evidence conflicts row 5.
    return refer("Malignant mixed tumour, or malignant pleomorphic adenoma, of the lacrimal "
                 "gland, with no carcinoma named", 12,
                 "%s (8940/3) is recorded with the other specified malignant tumours, ICCC-3 "
                 "Group XII, not in Group XI. A carcinoma ex pleomorphic adenoma is a carcinoma: "
                 "choose it from the list of other carcinomas instead. Code the case from the "
                 "Group XII tree." % term("8940", "3"),
                 note="Evidence ey_lacrimal_histology option 2. Departure 8; ICCC-2017 places "
                      "8940 in XIIa4 at every site.")


def bone_of_orbit():
    # Milman p. 21 "Other tumors of orbital bone Ewing sarcoma".
    return refer("A tumour of the bone of the orbital wall, such as Ewing sarcoma", 8,
                 "A bone tumour is recorded at the bone where it arose, in ICCC-3 Group VIII. "
                 "Code the case from the Group VIII (malignant bone tumours) tree.",
                 recapture=True,
                 note="Evidence ey_orbit_histology option 9. ICCC-2017 places 9364 at C40-C41 in "
                      "VIIIc2.")


def eyelid():
    # Milman p. 7 "Sebaceous carcinoma, covered in Tumors of the Eyelid chapter, has been
    # removed"; p. 9 "Malignant adnexal tumors of the eyelid Sebaceous carcinoma".
    return nonrep("A tumour of the eyelid, including sebaceous carcinoma of the eyelid, the "
                  "conjunctiva or the caruncle",
                  "A tumour of the eyelid is a skin tumour, recorded at the skin of the eyelid "
                  "(C44.1), and WHO groups sebaceous carcinoma of the conjunctiva and caruncle "
                  "with the eyelid tumours. It is not coded from the eye tree. Go back to the "
                  "site step, record the eyelid (C44.1) and code the case from the skin "
                  "carcinoma tree.",
                  heading="Skin of the eyelid",
                  note="Evidence ey_surface_histology option 2 and ey_site option 10, which hop "
                       "to sk_histology. Departure 5: SELF_REFERRAL is False, so the line is "
                       "non-reportable; ICD-O-3.2 prints the skin site (C44._) beside 8410/3.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence ey_evidence, ey_cytology)
# ------------------------------------------------------------------------------------------
GATE_HINT = (
    "A radiology or ultrasound report counts as imaging. A cytology report on a fine-needle "
    "aspirate or fluid counts as cytology. A pathology report on a biopsy or excision counts as "
    "histology. A biopsy or cytology report that calls the specimen inadequate or non-diagnostic "
    "counts as no tissue. A file that names retinoblastoma or retinocytoma is recorded in Group "
    "V, which registers it on an eye examination or imaging, because a biopsy of the eye is "
    "usually avoided: do not code it from this tree, and code it from the Group V tree. Choose the "
    "tier that matches the reports for any other tumour. A tumour of the eyelid is a skin tumour (C44.1): go back to the site step. A "
    "report that calls the tumour possible or suspected does not register it.")


def gate():
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour of the eye, the lacrimal gland or the "
                 "orbit?",
        hint=GATE_HINT,
        tier_labels={
            "cytology": "A cytology report (a fine-needle aspirate or fluid) - no histology "
                        "report",
            "histology": "A histology report (biopsy or excision), with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=[
            # Evidence ey_cytology option 0. Rules p. 6 (printed p. 19) "the appropriate code is
            # C80.9 (unknown primary site) 8010/3 (carcinoma)". D8.
            cyto_carcinoma_nos(note="Evidence ey_cytology option 0. D8; departure 9."),
            # Evidence ey_cytology option 1. Milman p. 3 "Conjunctival squamous cell carcinoma".
            cyto("Cytology names a squamous cell carcinoma", "8070",
                 note="Evidence ey_cytology option 1. D8."),
            # Evidence ey_cytology option 2. Milman p. 12 "Malignant epithelial tumors of the
            # lacrimal drainage system"; p. 10 "Adenoma and adenocarcinoma of the ciliary body".
            cyto("Cytology names an adenocarcinoma", "8140",
                 note="Evidence ey_cytology option 2. D8."),
            # Evidence ey_cytology option 4. Milman p. 3 "Conjunctival melanocytic intraepithelial
            # lesions Conjunctival melanoma". D8 in place of the hop (departure 9).
            cyto("Cytology names a melanoma", "8720",
                 "A melanoma that began elsewhere, such as the skin, is coded at that primary "
                 "site: go back to the site step and record it.",
                 note="Evidence ey_cytology option 4 (departure 9): D8 in place of the hop to "
                      "the melanoma tree, whose screens record basis 7."),
            # Evidence ey_cytology option 5. Pfister p. 12 and Milman p. 11.
            retinoblastoma("Cytology names retinoblastoma",
                           note="Evidence ey_cytology option 5."),
            # Evidence ey_cytology option 6.
            medulloepithelioma(),
            # Evidence ey_cytology option 7.
            lymphoma("Cytology names a lymphoma"),
        ],
        note="Evidence ey_evidence and ey_cytology (departures 1 and 9 in the module "
             "docstring).")
    return nodes


# ------------------------------------------------------------------------------------------
# Histology (the four histology screens of the evidence, in one: departure 3, D14)
# ------------------------------------------------------------------------------------------
HISTOLOGY_HINT = (
    "Use the report's own term. A carcinoma of the eye is recorded at the part of the eye the "
    "report names. If the site step recorded the eye with no part named (C69.9) or with more than "
    "one part (C69.8), and the report names the part where the tumour began (the conjunctiva, "
    "cornea, retina, choroid, ciliary body, lacrimal gland or orbit), choose the answer that "
    "records the part. Squamous intraepithelial neoplasia, dysplasia and carcinoma in situ of the "
    "conjunctiva or cornea, and the benign tumours of the lacrimal gland, have not invaded and "
    "are found under the answer for a benign, borderline or in situ tumour. A tumour the report "
    "places at the limbus, where the cornea meets the conjunctiva, is recorded at the cornea "
    "(C69.1). Squamous cell carcinoma and adenocarcinoma of the conjunctiva, the lacrimal "
    "gland, the ciliary body or the retinal pigment epithelium are found under another carcinoma "
    "the report names. A tumour of the eyelid is a skin tumour.")


def histology():
    opts = [
        # Evidence ey_intraocular_histology option 0; ey_orbit_histology option 8.
        retinoblastoma(),
        # Evidence ey_intraocular_histology option 1.
        medulloepithelioma(),
        # Evidence ey_site option 11.
        optic_nerve(),
        # Evidence ey_site options 0 to 9 (departure 2). Rules p. 5 "its point of origin cannot be
        # determined"; Milman p. 3, p. 10, p. 12.
        go("The site step recorded the eye with the part not stated, or with more than one part, "
           "and the report names the part where the tumour began", n("site"),
           note="D9, departure 2: the part of the eye, for a site recorded C69.8 or C69.9."),
        # Evidence ey_surface_histology option 1, ey_lacrimal_histology option 1,
        # ey_intraocular_histology option 5, ey_orbit_histology option 1. Rules p. 6 (printed p.
        # 19) "the appropriate code is C80.9 (unknown primary site) 8010/3 (carcinoma)".
        named("Carcinoma of any part of the eye, the lacrimal gland or the orbit, with no type "
              "named", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence ey_surface_histology option 1 and the matching options of the "
                   "other three screens; the generic option of the screen."),
        eyelid(),
    ] + tail_options(
        P, "eye", where=WHERE,
        not_malignant_label="A tumour the report calls benign, borderline or in situ: squamous "
                            "intraepithelial neoplasia, squamous papilloma or oncocytoma of the "
                            "conjunctiva or cornea, a benign tumour or intraductal carcinoma of "
                            "the lacrimal gland, or an adenoma of the ciliary body or retina",
        referrals=[
            lymphoma(),
            histiocytosis(),
            malignant_mixed(),
            refer_leukaemia(WHERE),
            refer_sarcoma(WHERE, "A soft tissue sarcoma, such as rhabdomyosarcoma of the orbit"),
            bone_of_orbit(),
            refer_germ_cell(WHERE),
            refer_other_named(),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        HISTOLOGY_HINT,
        opts, ["topography"],
        "Evidence ey_surface_histology, ey_lacrimal_histology, ey_intraocular_histology and "
        "ey_orbit_histology, as one screen (departure 3, D14). Carcinomas of every type are "
        "picker entries (departure 7); Milman 2023 and Pfister 2022 Table 3 report no eye "
        "carcinoma in children. The unstated-type option is the generic option. Melanoma hops to "
        "me_eye (D13); T2c to confirm the screen takes a melanoma of the conjunctiva, the "
        "intraocular structures, the lacrimal drainage system and the orbit.")


SITE_HINT = (
    "Use this question only when the site step recorded the eye with the part not stated (C69.9) "
    "or with more than one part (C69.8), and the histology report or the operation note names "
    "the part where the tumour began (WHO coding Rule H). A tumour the report places at the "
    "limbus, where the cornea meets the conjunctiva, is recorded at the cornea (C69.1). A tumour "
    "of the eyelid is a skin tumour: go back to the site step. A site named only by a prefix such "
    "as peri- is not an ICD-O site: go back to the site step. The next screen asks the tumour "
    "type again.")


def site():
    caps = (lambda topo: {"topography": topo})
    back = n("histology")
    return node(
        n("site"), "site_resolution", 4, "Part of the eye",
        "Which part of the eye does the report name as the place where the tumour began?",
        SITE_HINT,
        [
            # Milman p. 3 "Conjunctival squamous cell carcinoma".
            go("Conjunctiva", back, captures=caps("C69.0"), note="Evidence ey_site option 0."),
            # Evidence ey_site option 1; evidence hint (limbus).
            go("Cornea, or the limbus", back, captures=caps("C69.1"),
               note="Evidence ey_site option 1."),
            # Milman p. 10 "Adenoma and adenocarcinoma of the RPE".
            go("Retina, including the retinal pigment epithelium", back, captures=caps("C69.2"),
               note="Evidence ey_site option 4."),
            # Evidence ey_site option 5.
            go("Choroid", back, captures=caps("C69.3"), note="Evidence ey_site option 5."),
            # Milman p. 10 "Adenoma and adenocarcinoma of the ciliary body".
            go("Ciliary body or iris", back, captures=caps("C69.4"),
               note="Evidence ey_site option 6."),
            # Milman p. 12 "Benign and premalignant epithelial tumors of the lacrimal gland";
            # "Malignant epithelial tumors of the lacrimal drainage system".
            go("Lacrimal gland, lacrimal sac or nasolacrimal duct (the tear drainage passages)",
               back, captures=caps("C69.5"),
               note="Evidence ey_site options 2 and 3: Lacrimal gland and duct (C69.5)."),
            # Evidence ey_site option 7.
            go("Orbit (the tissue around the eyeball, including the muscles that move the eye)",
               back, captures=caps("C69.6"), note="Evidence ey_site option 7."),
        ], ["topography"],
        "Departure 2: the part-of-eye options of evidence ey_site (D9; Rule H). Each captures the "
        "topography and returns to ey_histology, the salivary tree's sg_site pattern. The "
        "evidence's C69.8 and C69.9 options, the eyelid, the optic nerve, the periorbital "
        "region and the deposit are the router's, other screens' or other trees'. Every code "
        "ey_histology emits is a Group XI code at C69.0 to C69.6 (this tree's routed sites).")


# ------------------------------------------------------------------------------------------
# The exclusion screen (the exclusions of the four evidence screens, grouped by part of the eye)
# ------------------------------------------------------------------------------------------
def not_malignant():
    return not_malignant_node(
        P,
        [
            # Milman p. 3 "Conjunctival squamous intraepithelial neoplasia".
            excl("Conjunctiva or cornea: squamous intraepithelial neoplasia, high grade, or "
                 "moderate or severe dysplasia", "8077", "2",
                 what="a high-grade squamous intraepithelial neoplasia",
                 note="Evidence ey_surface_histology option 5."),
            excl("Conjunctiva or cornea: squamous intraepithelial neoplasia, low grade, or mild "
                 "dysplasia", "8077", "0", what="a low-grade squamous intraepithelial neoplasia",
                 note="Evidence ey_surface_histology option 6."),
            # Rules p. 6 "Carcinoma in situ and CIN III".
            excl("Conjunctiva or cornea: squamous cell carcinoma in situ, with no invasion",
                 "8070", "2", what="a squamous cell carcinoma in situ",
                 note="Evidence ey_surface_histology option 7."),
            # Milman p. 3 "Conjunctival squamous papilloma"; p. 12 "Papillomas (squamous and
            # inverted)".
            excl("Conjunctiva or tear drainage passages: squamous papilloma", "8052", "0",
                 what="a squamous papilloma",
                 note="Evidence ey_surface_histology option 8 and ey_lacrimal_histology option "
                      "9."),
            # Milman p. 3 "Conjunctival oncocytoma"; p. 12 "Lacrimal gland oncocytoma".
            excl("Conjunctiva or lacrimal gland: oncocytoma", "8290", "0", what="an oncocytoma",
                 extra="ICD-O-3.2 gives Oncocytoma as a synonym of this code.",
                 note="Evidence ey_surface_histology option 9 and ey_lacrimal_histology option "
                      "6."),
            # Milman p. 12 "Pleomorphic adenoma (PA) of the lacrimal gland".
            excl("Lacrimal gland: pleomorphic adenoma", "8940", "0",
                 what="a pleomorphic adenoma", note="Evidence ey_lacrimal_histology option 5."),
            # Milman p. 12 "Lacrimal gland oncocytoma Myoepithelioma Intraductal carcinoma".
            excl("Lacrimal gland: myoepithelioma", "8982", "0", what="a myoepithelioma",
                 note="Evidence ey_lacrimal_histology option 7."),
            excl("Lacrimal gland: intraductal carcinoma, with no invasion", "8500", "2",
                 what="an intraductal carcinoma",
                 note="Evidence ey_lacrimal_histology option 8."),
            # Milman p. 12 "Papillomas (squamous and inverted)".
            excl("Tear drainage passages: inverted papilloma", "8121", "1",
                 what="an inverted papilloma", note="Evidence ey_lacrimal_histology option 10."),
            # Milman p. 10 "Adenoma and adenocarcinoma of the ciliary body", "Adenoma and
            # adenocarcinoma of the RPE".
            excl("Inside the eye: adenoma of the ciliary body epithelium or of the retinal "
                 "pigment epithelium", "8140", "0", what="an adenoma",
                 note="Evidence ey_intraocular_histology option 6."),
        ],
        where=WHERE,
        note="The exclusions of the four evidence screens, one line per tumour, with the part of "
             "the eye in the label (departure 3).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), site(), not_malignant(), deposit_node(P, where=WHERE)]
    return make_tree(TREE_ID, nodes)


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma of the eye, lacrimal gland or orbit whose type the report does not "
               "name, at basis 7 on the histology screen, and at basis 5 when cytology names a "
               "carcinoma only. No source reports an eye carcinoma in children (Pfister 2022 "
               "Table 3; Milman 2023), so every named carcinoma type is a picker entry."),
    "8070/3": ("D8", EVIDENCE,
               "Squamous cell carcinoma named on eye cytology, at basis 5 (Milman 2023, PDF p. "
               "3); a histology report reaches it from the picker."),
    "8140/3": ("D8", EVIDENCE,
               "Adenocarcinoma named on eye cytology, at basis 5 (Milman 2023, PDF pp. 10 and "
               "12); a histology report reaches it from the picker."),
    "8720/3": ("D8, D13", EVIDENCE,
               "Melanoma named on eye cytology, at basis 5; a histology report reaches the "
               "melanoma tree instead."),
}
