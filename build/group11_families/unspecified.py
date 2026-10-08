"""g11_unspecified (prefix un_): carcinomas at the peritoneum and retroperitoneum (C48.x), the
brain, spinal cord and meninges (C70 to C72), the ill-defined sites (C76.x) and an unknown
primary site (C80.9), ICCC-3 subgroup XIf10 (range 134) and XIf11 (range 136). It is also the
router default, so a case can arrive at a site no Group XI range covers (bone, soft tissue, lymph
node, marrow), for example from Group IX st_not_sarcoma keeping the soft tissue site.

Built from docs/group_11_evidence/XIf10_parathyroid_other_unspecified.json, the unknown-primary,
central nervous system and peritoneum nodes (cu_evidence, cu_clinical, cu_imaging, cu_lab,
cu_cytology, cu_primary, cu_region, cu_histology, cn_evidence, cn_clinical, cn_imaging,
cn_histology, pe_evidence, pe_clinical, pe_imaging, pe_histology, ou_cytology, ou_picker), with
the builders in build/group11_common.py, in the shape of build/group11_organs/thyroid.py. The
evidence's cu_, cn_, pe_ and ou_ node ids become un_, the tree's prefix (contract §4.1). Every
option's label, code, behaviour, basis, reason and recognition aid comes from that file unless a
departure below says otherwise; the cite (file, page, quotation) is the comment above the option.
File names in the comments are the evidence's own:
    Hernandez-Prera  XIf11-unknown-primary-head-neck__Hernandez-Prera-2022.txt (Head Neck Pathol
                     2022;16:110-122)
    Rules            RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser           Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's
                     file set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    un_document_inventory  document_inventory  evidence gate (evidence cu_, cn_, pe_evidence)
    un_labs_referral, un_labs_markers, un_labs_cytology, un_labs_histology  lab_results
    un_clinical, un_clinical_cytology  clinical_alias
    un_imaging, un_imaging_markers, un_imaging_cytology  morphology_only
    un_cytology            morphology_only     (evidence cu_cytology and ou_cytology)
    un_primary             histology_subclassification  (evidence cu_primary and cu_region)
    un_histology           histology_subclassification  (evidence cu_, pe_ and cn_histology)
    un_not_malignant       histology_subclassification  (the exclusions of evidence pe_histology)
    un_deposit             morphology_only      (D10)
    un_picker              histology_subclassification  (D2; evidence ou_picker)

un_histology is the node the other trees' deposit questions hop to for "a carcinoma whose primary
has not been found" (group11_common.UNSPECIFIED_HISTOLOGY): the hop captures C80.9, and ICCC-2017
range 136 places the shared carcinoma list at C80.9 in XIf11.

Departures from the evidence nodes, and why
-------------------------------------------
1. Three site families in one tree. The evidence has cu_ nodes for C76.x and C80.9, cn_ nodes for
   C70 to C72 and pe_ nodes for C48.x. The engine cannot filter options by site inside one tree
   (D14), so the three histology screens are one screen, un_histology, and the clinical, imaging
   and cytology screens are written once. The evidence's three cytology screens (cu_cytology,
   ou_cytology) are one: un_cytology.
2. The deposit question comes first (the brief for this tree). The gate's histology tier goes to
   un_primary, not to un_histology: the evidence's cu_primary asks whether the report names the
   organ where the carcinoma began. un_primary is that question, and sends a deposit to un_deposit
   (D10) and a primary tumour at the site to un_histology. The evidence's cu_region (Rules A to C)
   is not a screen: the router's site step records the region and the tissue (D14), and the
   histology hint carries its three rules (the skin of a region, a lymph node of a region, a site
   written with peri-, para- or area of). The two skin lines of cu_region, which re-site the case
   to C44.x with recapture_site, cannot be built as options: a referral to Group XI itself is not
   built (SELF_REFERRAL is False, D10); the hint sends the clerk back to the site step.
3. The evidence's deposit options on the clinical, imaging and cytology screens (a referral to
   Group XI with recapture_site) are not built, for the reason in departure 2 and because the
   deposit question cannot be reached from a tissue-free or cytology path (its "carcinoma whose
   primary has not been found" option continues in un_histology, where every code is basis 7). The
   instruction moves to the gate's hint and to the cytology screen's hint.
4. Tissue-free routes (D7). The evidence's clinical and imaging screens refer a primary tumour of
   the brain, spinal cord or meninges to Group III with refer_code 8000. The build's walk (rule C)
   admits only a Group XII referral with 8000 or 8001 on a path with no tissue, so that option is
   not built on the tissue-free screens. un_histology refers it (with tissue: choroid plexus
   carcinoma, craniopharyngioma, a pituitary or pineal tumour or any primary tumour of the brain,
   spinal cord or meninges), and each tissue-free route to Group XII carries a guard in its label,
   "not a tumour of the brain, spinal cord or meninges", because ICCC-2017 places 8000/3 and
   8001/3 at C70 to C72 in Group III (IIIf), not Group XII. The unspecified route's check that
   ICCC-2017 places 8000 and 8001 in Group XII at every routed site is bypassed by passing
   refer_unspecified explicitly. Request 1 in the module's return asks the walk to admit a
   Group III referral at a site ICCC-2017 places there.
5. cu_cytology option 2 ("A named carcinoma type, ... and no primary site was found") went to the
   picker at basis 5. The picker's options are basis 7, so the screen offers the four types the
   evidence names (Hernandez-Prera p. 8, "squamous cell, undifferentiated, and neuroendocrine
   morphology", and the label's adenocarcinoma) as cytology options at basis 5, each capturing C80.9
   (D8): squamous cell carcinoma, NOS (8070/3), adenocarcinoma, NOS (8140/3), undifferentiated
   carcinoma, NOS (8020/3) and neuroendocrine carcinoma, NOS (8246/3). ou_cytology's "A carcinoma
   the report says began at this site" is the carcinoma, NOS option with no site capture. The
   mesothelioma cytology line (ou_cytology option 2) refers to Group XII.
6. cu_lab is the marker tier (D7): imaging that shows tumour deposits with a raised chromogranin A
   (8240/3) or serotonin (8241/3) and a stated neuroendocrine tumour, at basis 4, captures C80.9.
   Its "another marker, or the clinician names no tumour type" line is the common imaging-only
   fallback of _imaging_markers. Visser Table 4 names no site for either row; the evidence gives
   them at C80.9 only, so the marker label says the primary site was not found.
7. cu_histology. The organ-named lines the evidence refers to Group XI with recapture_site (papillary
   thyroid carcinoma, nasopharyngeal carcinoma, parathyroid carcinoma) are cross-tree hops that
   capture the organ's site (Rule H; Rules p. 10, printed p. 23, "Use the topography code
   provided when a topographic site is not stated in the diagnosis"): th_histology with C73.9,
   np_histology with C11.9 and en_histology with C75.0. Hepatocellular carcinoma refers to Group
   VII as the evidence has it.
8. pe_histology. Peritoneal inclusion cyst (9055/0) and the well-differentiated papillary
   mesothelial tumour of the peritoneum (9052/0) move to un_not_malignant, reached by the standard
   option, whose label names them. "Pseudomyxoma peritonei, or carcinoma spread over the
   peritoneum from an organ" is the common deposit question (D10), whose last option records the
   unknown primary at C80.9. Seromucinous carcinoma (8474/3) refers to Group X, desmoplastic small
   round cell tumour to Group IX, mesothelioma to Group XII, as the evidence has them.
9. Melanoma (D13): the screen offers the general hop, me_mucosa, and one for the brain, spinal
   cord or meninges, me_cns, as the evidence's cu_histology "Melanoma" line has no site kind.
10. un_picker: D2. ICCC-2017 places the shared carcinoma list in Group XI at C48.x, C70 to C72,
    C76.x and C80.9 (XIf10 and XIf11), so the picker offers every code valid at all of the tree's
    routed sites.

Registrar question 4 of the evidence (an EBER-positive or p16-positive neck node with no primary
named) and question 6 (carcinoma of unknown primary in children) stay open; the defaults above
apply until they are answered (docs/group_11_registrar_review.md, task T6).
"""
from __future__ import annotations

from group11_common import (aid, code, cyto, cyto_carcinoma_nos, deposit_node, evidence_gate,
                            go, lab, make_tree, marker, melanoma_option, named, node,
                            not_malignant_node, refer, refer_germ_cell, refer_leukaemia,
                            refer_other_named, refer_sarcoma, refer_unspecified, excl,
                            tail_options, term)

TREE_ID = "g11_unspecified"
P = "un_"
WHERE = "the peritoneum, retroperitoneum, an ill-defined site or an unknown primary site"
EVIDENCE = "XIf10_parathyroid_other_unspecified"
GUARD = " (not a tumour of the brain, spinal cord or meninges, which Group III codes)"
NO_PRIMARY = "no primary site was found"


def n(name: str) -> str:
    return P + name


# Hernandez-Prera p. 6 and Rules p. 6 (printed p. 19) "the site of origin is unknown, the
# appropriate code is C80.9 (unknown primary site) 8010/3".
C80_9 = {"topography": "C80.9"}

# Evidence ou_cytology option 2; pe_histology option 0. Group XII holds mesothelioma at every
# site (ICCC-2017 XIIa5).
MESO_REASON = (
    "ICD-O-3.2 codes mesothelioma from %s (9050/3) to %s (9053/3), and ICCC-3 places those codes "
    "in Group XII (other and unspecified malignant neoplasms), not Group XI. Code the case from "
    "the Group XII tree." % (term("9050", "3"), term("9053", "3")))


def lymphoma():
    """The common lymphoma referral (refer_lymphoma) names the site twice; with this tree's
    phrase that sentence does not read, so the same content is written once here."""
    return refer("Lymphoma", 2,
                 "A lymphoma belongs to ICCC-3 Group II. A lymphoma that arises outside a lymph "
                 "node is coded to the site where it arose (WHO Rule D: an extranodal lymphoma "
                 "is coded to its site of origin). Code the case from the Group II (lymphomas) "
                 "tree.",
                 note="ICD-O-3.1 Rule D, p. 15. The hop carries the case's site.")


def at_c80_9(branch):
    """Record the case at Primary site not found (C80.9): the reason says so and the option
    captures it."""
    branch["captures"] = dict(branch.get("captures") or {}, **C80_9)
    branch["reason"] += " It is recorded at Primary site not found (C80.9)."
    return branch


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence cu_, cn_, pe_evidence; cu_lab; cu_cytology and ou_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour at the peritoneum or retroperitoneum, an "
                 "ill-defined site, the brain or spinal cord, or with no primary site found?",
        # Evidence cu_evidence, cn_evidence and pe_evidence hints; cu_primary hint; Rules p. 7
        # (printed p. 20) "indicating that the associated topography code is not the site of
        # origin"; Rules p. 1 (printed p. 14) "If the diagnosis does not specify the tissue of
        # origin" and p. 4 "be coded to C44.6 (skin of arm) rather than C76.4". The evidence's
        # deposit options become this hint (departure 3).
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. An immunohistochemistry or "
              "gene report on its own does not stand in for a histology report. A deposit of a "
              "cancer that began in another organ is coded at that organ: go back to the site "
              "step and record the organ the file names. A squamous cell or basal cell carcinoma "
              "of a region, such as the arm, the chin or the forehead, is skin: go back to the "
              "site step and record the skin of that region. A primary tumour of the brain, "
              "spinal cord or meninges that is not a carcinoma is coded in Group III: go back "
              "and search its name. A report that calls the tumour possible or suspected does "
              "not register it."),
        labs=[
            # Evidence lab_tests rows 4 and 5 (cu_lab): chromogranin A and serotonin. The
            # evidence prints no unit (departure 6).
            lab("chromogranin_a", "Plasma or serum chromogranin A", ("ng/mL", "µg/L", "nmol/L")),
            lab("serotonin", "Serotonin", ("ng/mL", "µg/L", "nmol/L")),
        ],
        marker_tests="chromogranin A or serotonin",
        markers=_markers(),
        unspecified=refer_unspecified,
        tier_labels={
            "imaging": "An imaging report only - no chromogranin A or serotonin result, no "
                       "tissue",
            "cytology": "Cytology only - a fine-needle aspirate, a smear or a fluid sample "
                        "(cerebrospinal fluid, ascitic fluid); no histology report",
            "histology": "A histology report: biopsy or resection of a lymph node, a deposit or "
                         "a mass, with or without immunohistochemistry or gene reports",
        },
        cytology=_cytology(),
        note="Evidence cu_evidence, cn_evidence, pe_evidence, cu_lab and cu_cytology "
             "(departures 1 to 6 in the module docstring).")
    entry = n("histology")
    for nd in nodes:
        # Departure 2: the histology tier asks the deposit question first.
        if nd.get("next_node") == entry:
            nd["next_node"] = n("primary")
        for o in nd.get("options") or []:
            if o.get("next_node") == entry:
                o["next_node"] = n("primary")
            # Departure 4: ICCC-2017 places 8000/3 and 8001/3 at C70 to C72 in Group III, so
            # every route to Group XII says so.
            if o.get("refer_group") == 12 and o.get("refer_code") in ("8000", "8001"):
                o["label"] += GUARD
                o["coding_note"] += (" The label's guard: ICCC-2017 places this code at C70 to "
                                     "C72 in Group III, and the walk admits no Group III route "
                                     "without tissue (departure 4).")
        if nd["node_id"] == n("cytology"):
            nd["hint"] += (" Cytology of a carcinoma that the file says began in another organ "
                           "is a deposit: it is coded at that organ. Go back to the site step "
                           "and record the organ the file names.")
            nd["coding_note"] += (" The hint's last sentences carry the evidence's deposit "
                                  "option (unspecified module departure 3).")
    return nodes


def _markers():
    note = ("Visser O, et al. Front Oncol 2023;13:1250549, Table 4, p. 06, and rule 6, p. 05. "
            "Evidence cu_lab options 0 and 1 (departure 6); the evidence gives both at C80.9 "
            "only, so the case is re-sited there.")
    out = []
    for morph, test, diagnosis, label in (
            ("8240", "chromogranin A", "neuroendocrine tumour",
             "Imaging shows tumour deposits, the report calls chromogranin A raised, the "
             "clinician states a neuroendocrine tumour, and %s" % NO_PRIMARY),
            ("8241", "serotonin", "neuroendocrine tumour",
             "Imaging shows tumour deposits, the report calls serotonin raised, the clinician "
             "states a neuroendocrine tumour, and %s" % NO_PRIMARY)):
        out.append(at_c80_9(marker(
            morph, test=test, diagnosis=diagnosis, where="with no primary site found",
            label=label, note=note)))
    return out


def _cytology():
    out = [
        # Evidence ou_cytology option 2. Hernandez-Prera / ICCR-Meso: peritoneal fluid.
        refer("Mesothelioma cells in peritoneal fluid", 12, MESO_REASON,
              note="Evidence ou_cytology option 2 (departure 5); ICCC-2017 XIIa5 at every site."),
        # Evidence ou_cytology option 3 (departure 5): the report says the carcinoma began at
        # this site, so the site stays.
        cyto("Carcinoma cells, type not named, and the report says the carcinoma began at this "
             "site (the peritoneum, retroperitoneum, an ill-defined site or the brain or spinal "
             "cord)", "8010",
             note="Evidence ou_cytology option 3, carried as 8010/3 at basis 5: the picker's "
                  "options are basis 7 (departure 5)."),
        # Evidence cu_cytology option 1. Rules p. 6 (printed p. 19) "the site of origin is
        # unknown, the appropriate code is C80.9 (unknown primary site) 8010/3".
        at_c80_9(cyto("Carcinoma or malignant epithelial cells, type not named, and %s"
                      % NO_PRIMARY, "8010",
                      note="Evidence cu_cytology option 1; ICCC-2017 range 136 places 8010/3 at "
                           "C80.9 in XIf11.")),
    ]
    # Evidence cu_cytology option 2 (departure 5); Hernandez-Prera p. 8 "CUP that exhibits
    # squamous cell, undifferentiated, and neuroendocrine morphology".
    for morph, name in (("8070", "Squamous cell carcinoma"), ("8140", "Adenocarcinoma"),
                        ("8020", "Undifferentiated carcinoma"),
                        ("8246", "Neuroendocrine carcinoma")):
        out.append(at_c80_9(cyto("%s, and %s" % (name, NO_PRIMARY), morph,
                                 note="Evidence cu_cytology option 2, built as a named cytology "
                                      "option (departure 5).")))
    return out


# ------------------------------------------------------------------------------------------
# The deposit question first (evidence cu_primary; departure 2)
# ------------------------------------------------------------------------------------------
def primary():
    return node(
        n("primary"), "histology_subclassification", 2, "Deposit or primary tumour",
        "Does the report call the tumour a deposit?",
        # Evidence cu_primary hint; Hernandez-Prera p. 8 (EBER, p16). Rules p. 7 (printed p. 20)
        # "indicating that the associated topography code is not the site of origin"; Rules p. 1
        # and p. 4 (Rules A and B).
        "A carcinoma in a lymph node or another organ is recorded at the organ where it began. "
        "Some tests point to an organ: Epstein-Barr virus encoded RNA (EBER) to the nasopharynx, "
        "p16 or high-risk human papillomavirus to the oropharynx, ultraviolet-signature "
        "mutations to the skin. Record that organ only when the report or the treating "
        "clinician names it as the primary site. A site written with a prefix such as peri- or "
        "para-, or as the area or region of a site, stays at the ill-defined site unless the "
        "tumour type shows its tissue.",
        [
            # Evidence cu_primary option 0 and option 2; cu_region option 1; pe_histology option
            # 4; cn_histology options 0 and 1.
            aid(go("A deposit (metastasis) or a carcinoma in a lymph node: the report names the "
                   "organ where it began, or the primary has not been found", n("deposit"),
                   note="Evidence cu_primary options 0 and 2, cu_region option 1, cn_histology "
                        "options 0 and 1 (departure 2). D10: un_deposit asks where the primary "
                        "is."),
                "The report or the clinical note names the primary site, often after a test such "
                "as Epstein-Barr virus encoded RNA (EBER) or p16; or the report may say carcinoma "
                "of unknown primary, or metastatic carcinoma with the primary not identified "
                "after work-up."),
            # Evidence cu_primary option 1; cu_region options 2 and 3; cn_histology option 4;
            # pe_histology option 6.
            go("A primary tumour: the report says it began at this site, or at an ill-defined "
               "site or a region of the body, and names no organ", n("histology"),
               note="Evidence cu_primary option 1, cu_region options 2 and 3, cn_histology "
                    "option 4, pe_histology option 6."),
        ], [],
        "Evidence cu_primary and cu_region (departure 2). The router's site step records the "
        "region (D14), so cu_region is not a screen; its three rules are in this hint and the "
        "gate's.")


# ------------------------------------------------------------------------------------------
# Histology (evidence cu_histology, pe_histology, cn_histology)
# ------------------------------------------------------------------------------------------
def histology():
    opts = [
        # Evidence cu_histology option 0. Rules p. 6 (printed p. 19) "the site of origin is
        # unknown, the appropriate code is C80.9 (unknown primary site) 8010/3".
        named("Carcinoma with no type named: carcinoma, metastatic carcinoma, or malignant "
              "epithelial tumour", "8010",
              note="Evidence cu_histology option 0; the generic option of the screen. Registrar "
                   "question 6: squamous cell, undifferentiated, neuroendocrine and adenocarcinoma "
                   "stay in the picker."),
        # Evidence cu_histology option 1. Rules p. 10 (printed p. 23) "Use the topography code
        # provided when a topographic site is not stated in the diagnosis"; Hernandez-Prera p. 6
        # "follicular cells are not present in the lateral neck". Departure 7.
        aid(go("Papillary thyroid carcinoma", "th_histology", {"topography": "C73.9"},
               note="Evidence cu_histology option 1, as a cross-tree hop that captures the "
                    "thyroid (departure 7). th_histology is the thyroid tree's histology "
                    "screen."),
            "A papillary thyroid carcinoma in a lymph node at the side of the neck is a deposit "
            "from the thyroid."),
        # Evidence cu_histology option 2. Hernandez-Prera p. 8 "strongly correlates with a
        # nasopharynx origin"; ICD-O-3.2 ties Schmincke tumor to C11.
        go("Nasopharyngeal carcinoma, or Schmincke tumour", "np_histology",
           {"topography": "C11.9"},
           note="Evidence cu_histology option 2, as a cross-tree hop that captures the "
                "nasopharynx (departure 7). np_histology is the nasopharynx tree's histology "
                "screen."),
        # Evidence cu_histology option 3. ICCR p. 9 image "Parathyroid carcinoma 8140/3".
        go("Parathyroid carcinoma", "en_histology", {"topography": "C75.0"},
           note="Evidence cu_histology option 3, as a hop into this part's endocrine tree that "
                "captures the parathyroid gland (departure 7)."),
        # Evidence cu_histology option 4. Pfister p. 13 "Pediatric hepatocellular carcinoma".
        refer("Hepatocellular carcinoma", 7,
              "ICD-O-3.2 ties %s to the liver (C22.0). ICCC-3 places hepatocellular carcinoma "
              "in Group VII, hepatic tumours, at every site. Code the case from the Group VII "
              "tree." % term("8170", "3"),
              note="Evidence cu_histology option 4; ICCC-2017 places 8170/3 in Group VII."),
        # Evidence pe_histology option 0; ICCR-Meso / Sauter p. 13 "Mesothelial tumors".
        refer("Mesothelioma (malignant mesothelioma; epithelioid, biphasic or sarcomatoid "
              "mesothelioma)", 12, MESO_REASON,
              note="Evidence pe_histology option 0; ICCC-2017 XIIa5 at every site."),
        # Evidence pe_histology option 3. Pfister p. 9 "Desmoplastic small round cell tumor".
        refer("Desmoplastic small round cell tumour", 9,
              "Desmoplastic small round cell tumour is coded in ICCC-3 Group IX (soft-tissue and "
              "other extraosseous sarcomas) at every site. Code the case from the Group IX "
              "tree.",
              note="Evidence pe_histology option 3."),
        # Evidence pe_histology option 5. ICCC-2017: 8474/3 is Group X at every site.
        refer("Seromucinous carcinoma", 10,
              "ICCC-3 places %s (8474/3) in Group X, germ cell, trophoblastic and gonadal "
              "neoplasms, at every site. Code the case from the Group X tree."
              % term("8474", "3"),
              note="Evidence pe_histology option 5."),
        # Evidence cn_histology options 2 and 3. Pfister p. 17 "Choroid plexus carcinoma",
        # p. 18 "Adamantinomatous craniopharyngioma", "Pituitary blastoma". Departure 4.
        refer("Choroid plexus carcinoma, craniopharyngioma, a pituitary or pineal tumour, or any "
              "other primary tumour of the brain, spinal cord or meninges", 3,
              "These tumours are coded in ICCC-3 Group III (central nervous system and "
              "miscellaneous intracranial and intraspinal neoplasms). Code the case from the "
              "Group III tree.",
              note="Evidence cn_histology options 2 and 3, widened to every primary tumour of "
                   "the central nervous system so that a brain tumour that is not a carcinoma "
                   "does not reach the Group XII options (departure 4)."),
    ] + tail_options(
        P, "mucosa", where=WHERE,
        not_malignant_label="A peritoneal inclusion cyst, a well-differentiated papillary "
                            "mesothelial tumour of the peritoneum, or another tumour the report "
                            "calls benign, borderline or in situ",
        referrals=[
            lymphoma(),
            refer_leukaemia(WHERE),
            refer_sarcoma(WHERE),
            refer_germ_cell(WHERE),
            refer_other_named(),
        ])
    # Departure 9: the melanoma hop for the brain, spinal cord or meninges.
    for i, o in enumerate(opts):
        if o.get("next_node") == "me_mucosa":
            o["label"] = "Melanoma, away from the brain, spinal cord and meninges"
            cns = melanoma_option("cns")
            cns["label"] = "Melanoma of the brain, spinal cord or meninges"
            opts.insert(i + 1, cns)
            break
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the report call the tumour?",
        # Evidence cu_histology hint; pe_histology hint; cn_histology hint. Rules p. 10
        # (printed p. 23); ICD-O-3.1 §4.3.8.
        "When no primary site is found, a tumour name that ICD-O ties to one organ is recorded "
        "at that organ: papillary thyroid carcinoma at the thyroid, parathyroid carcinoma at the "
        "parathyroid gland, hepatocellular carcinoma at the liver, infiltrating duct carcinoma "
        "at the breast. First check that the report does not place the primary somewhere else. "
        "Tissue around the pancreas, the adrenal gland or the caecum is retroperitoneum "
        "(C48.0). A neuroblastoma, paraganglioma, sarcoma, germ cell tumour or lymphoma of the "
        "retroperitoneum is coded in its own group: go back and search its name. ICD-O ties "
        "high-grade and low-grade serous carcinoma to the ovary: record the peritoneum only "
        "when the report says the tumour began in the peritoneum. A carcinoma found in the "
        "brain, spinal cord or meninges is almost always a deposit: it is coded at the organ "
        "where it began, unless the report states that it began here.",
        opts, [],
        "Evidence cu_histology, pe_histology and cn_histology merged (departure 1).")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # Evidence pe_histology option 1. Sauter p. 13 "Peritoneal inclusion cysts".
            excl("Peritoneal inclusion cyst (also called multicystic or cystic mesothelioma)",
                 "9055", "0", what="a peritoneal inclusion cyst",
                 note="Evidence pe_histology option 1."),
            # Evidence pe_histology option 2. Sauter p. 13 "Mesothelial tumors".
            excl("Well-differentiated papillary mesothelioma (well-differentiated papillary "
                 "mesothelial tumour) of the peritoneum", "9052", "0",
                 what="a well-differentiated papillary mesothelial tumour of the peritoneum",
                 note="Evidence pe_histology option 2."),
        ],
        where=WHERE,
        note="The two non-malignant lines of evidence pe_histology (departure 8).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [primary(), histology(), not_malignant(), deposit_node(P, where=WHERE)]
    return make_tree(TREE_ID, nodes)


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8010/3": ("D8, D10", EVIDENCE,
               "Carcinoma whose type the report does not name: basis 7 on the histology screen "
               "(at C80.9 when the deposit question sends a carcinoma with no primary found "
               "here), and basis 5 on the cytology screen. ICCC-2017 range 136 places 8010/3 at "
               "C80.9 in XIf11."),
    "8070/3": ("D8", EVIDENCE,
               "Squamous cell carcinoma with no primary site found, named by cytology, at basis "
               "5 and C80.9 (Hernandez-Prera p. 8)."),
    "8140/3": ("D8", EVIDENCE,
               "Adenocarcinoma with no primary site found, named by cytology, at basis 5 and "
               "C80.9."),
    "8020/3": ("D8", EVIDENCE,
               "Undifferentiated carcinoma with no primary site found, named by cytology, at "
               "basis 5 and C80.9 (Hernandez-Prera p. 8)."),
    "8246/3": ("D8", EVIDENCE,
               "Neuroendocrine carcinoma with no primary site found, named by cytology, at "
               "basis 5 and C80.9 (Hernandez-Prera p. 8)."),
    "8240/3": ("D7", EVIDENCE,
               "Neuroendocrine tumour with no primary site found: imaging that shows tumour "
               "deposits with a raised chromogranin A and a stated neuroendocrine tumour, at "
               "basis 4 and C80.9 (Visser 2023 Table 4)."),
    "8241/3": ("D7", EVIDENCE,
               "Enterochromaffin cell carcinoid with no primary site found: imaging that shows "
               "tumour deposits with a raised serotonin and a stated neuroendocrine tumour, at "
               "basis 4 and C80.9 (Visser 2023 Table 4)."),
}
