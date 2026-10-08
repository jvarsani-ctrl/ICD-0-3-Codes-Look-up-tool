"""g11_urinary_male_genital (prefix gu_): carcinomas of the bladder (C67, ICCC-3 subgroup XIf8),
the renal pelvis (C65.9), ureter (C66.9), urethra and other urinary organs (C68), prostate (C61.9),
penis (C60.0-C60.8) and the other male genital organs (C63.0, C63.1, C63.7-C63.9), subgroup XIf10.

A family tree (contract §4.1, D14). It is built from
docs/group_11_evidence/XIf8_urinary_male_genital.json (the evidence agent's nodes gu_site,
gu_document_inventory, gu_cytology, gu_urinary_histology, gu_not_malignant_urinary,
gu_urinary_picker, gu_prostate_histology, gu_prostate_picker, gu_not_malignant_prostate,
gu_penis_histology, gu_penis_scc_subtype, gu_penis_hpv, gu_penis_picker, gu_not_malignant_penis,
gu_male_genital_histology) with the builders in build/group11_common.py.
build/group11_organs/thyroid.py is the exemplar whose shape this module copies.

File names in the comments are the evidence's own:
    Netto       XIf8-bladder-XIf10-prostate-urinary-tract__Netto-2022.txt (Netto GJ, et al. The
                2022 WHO Classification of Tumors of the Urinary System and Male Genital Organs,
                Part B. Eur Urol 2022;82:469-482); Tables 1 and 3 read from the page image
    ICCR-Bla    XIf8-bladder__ICCR-Urinary-Bladder-2nd.txt (ICCR Carcinoma of the Bladder, 2nd
                edition, version 2.0, December 2025); "image" marks a table page image
    ICCR-RPU    XIf10-renal-pelvis-ureter__ICCR-Renal-Pelvis-Ureter-2nd.txt (ICCR Carcinoma of
                the Renal Pelvis and Ureter, 2nd edition, version 2.0, December 2025)
    ICCR-Pro    XIf10-prostate__ICCR-Prostate-3rd.txt (ICCR Prostate Cancer, 3rd edition,
                version 3.0, November 2024)
    ICCR-Pen    XIf10-penis__ICCR-Penis-Distal-Urethra-2nd.txt (ICCR Carcinoma of the Penis and
                Distal Urethra, 2nd edition, version 2.0, November 2024)
    Liu         XIf8-bladder-urothelial-paediatric__Liu-2025.txt (Liu P, et al. BMC Urol 2025);
                PubMed Central section numbers stand for pages
    Pfister     ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules       RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser      Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's
                file set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    gu_document_inventory   document_inventory   evidence gate (evidence gu_document_inventory)
    gu_labs_referral, gu_labs_markers, gu_labs_cytology, gu_labs_histology   lab_results
    gu_clinical, gu_clinical_cytology   clinical_alias
    gu_imaging, gu_imaging_markers, gu_imaging_cytology   morphology_only
    gu_cytology             morphology_only      (evidence gu_cytology)
    gu_histology            histology_subclassification  (the four organ screens, merged: D14)
    gu_penis_scc_subtype    histology_subclassification  (evidence gu_penis_scc_subtype)
    gu_penis_hpv            histology_subclassification  (evidence gu_penis_hpv, ihc_rules)
    gu_not_malignant        histology_subclassification  (the three exclusion screens, merged)
    gu_deposit              morphology_only      (D10)
    gu_picker               histology_subclassification  (D2; the three evidence pickers)

Departures from the evidence nodes, and why
-------------------------------------------
1. gu_site is not built. The router's site step chooses this tree and records the site, so the
   organ question is one the router already answers (D14). Its kidney (Group VI), testis
   (Group X), penis, NOS and scrotum (skin tree, XIe) and pelvis or groin (unspecified tree)
   answers belong to the router, which reaches those trees by site. Its WHO Rule B and Rule C
   content and its urachus and renal pelvis notes move to the gate's hint: the urachus is C67.7,
   a renal pelvis tumour that invades the kidney stays C65.9, one tumour across two parts or two
   organs takes the overlapping-lesion code (C67.8, C68.8, C63.8, C60.8), and tissue around an
   organ does not name the organ.
2. gu_document_inventory: the referral and imaging tiers recorded 8000/3 at basis 1 and 2 on the
   gate itself. D7: each routes to its own screen (gu_clinical, gu_imaging), which refers the
   case to Group XII with refer_code 8000, because ICCC-2017 places 8000/3 in XIIb at every
   routed site (evidence conflicts, Group 12). The evidence's "possible, probable or suspected"
   answer is not built: Visser rule 4 registers a tumour stated as probable and leaves only
   "possible" unregistered, which the common clinical and imaging screens apply. The gate's
   options are the contract §4.2 tiers with laboratory copies (registrar, 6 October 2026); the
   hint drops "Choose the strongest evidence the file holds", which the document checklist
   replaces.
3. The marker tier. The evidence's chromogranin A answer (8240/3, basis 4, tissue_free row 3)
   moves to gu_imaging_markers as a marker() option: a lab_results screen cannot choose a code
   (registrar, 6 October 2026), and the option needs imaging that shows the tumour, the raised
   result and the diagnosis Visser Table 4 names. Data gap 6 stands: no file in this part gives
   serum chromogranin A a diagnostic role at these sites; the row rests on Visser Table 4, whose
   chromogranin A row names no site (contract §0.5). The evidence's prostate-specific antigen
   answer ("raised, with no imaging that shows a tumour": not registrable) is the common rule 6
   line. Added, from contract §0.5 (Visser Table 4 read from the page image, 8 October 2026):
   imaging of a prostate tumour with a raised prostate-specific antigen refers to Group XII with
   8000 at basis 4, because Table 4 gives that row 8000/3, not a specific code. The evidence (§5)
   recorded that case at basis 2 and its lab_tests row says Table 4 gives the antigen no basis-4
   code; the contract's reading of the page image governs. The gu_labs_* screens record both
   values. The evidence gives no unit; the unit lists are the units laboratories report
   (registrar to confirm).
4. gu_cytology: "Another named tumour type ... next: gu_histology_by_site" went to the histology
   screens at basis 5, which the engine cannot do: the histology options record basis 7. The
   three types it names (squamous cell carcinoma, adenocarcinoma, small cell carcinoma) are cyto()
   options at basis 5 (D8). "Carcinoma, with no type named" is kept and also takes a carcinoma
   type this list does not show, which records Carcinoma, NOS (8010/3) at basis 5, the nearest
   generic code (D4's rule) and the understating direction. "Malignant, with no tumour type
   named" (8000/3 at basis 5) is the common line that refers to Group XII with 8001 (D8). The
   lymphoma referral is kept. The suspicious, atypical and low-grade urothelial neoplasm answers
   are a not-registrable line of their own in the report's vocabulary; "negative or
   non-diagnostic" is the common not-registrable line and the common non-diagnostic routes. The
   evidence's cytology hint (urine cytology cannot tell invasive carcinoma from carcinoma in
   situ) is in the reason of the high-grade urothelial carcinoma option.
5. The four organ histology screens (gu_urinary_histology, gu_prostate_histology,
   gu_penis_histology, gu_male_genital_histology) and gu_histology_by_site are one screen,
   gu_histology (D14: the engine cannot filter options by site). Options that belong to some
   organs only name them in brackets. The duplicated carcinoma, NOS, lymphoma, sarcoma, germ cell
   tumour, exclusion and deposit answers are one each; the three evidence pickers are the one
   picker option.
6. gu_histology, generic options (contract §4.2: carcinoma, adenocarcinoma and squamous cell
   carcinoma where the site has them). Adenocarcinoma, NOS (8140/3) and squamous cell carcinoma,
   NOS (8070/3), options on the evidence's gu_male_genital_histology and picker rows at the other
   organs, are options at every organ but the penis, whose squamous cell carcinoma goes to the
   subtype screen. The adenocarcinoma label names the four 8140/3 rows of the evidence pickers
   (adenocarcinoma with no type named, mixed adenocarcinoma, carcinoma of the Littre, Skene or
   Cowper glands, acinar adenocarcinoma of the prostate), because D2 drops an offered code from
   the picker. The carcinoma, NOS option names urachal carcinoma with no subtype, the evidence's
   8010/3 picker row, for the same reason; its urachal-site aid is in the gate's hint.
7. gu_histology, the 8120/3 subtypes (data gap 10). Plasmacytoid, lipid-rich, clear cell
   (glycogen-rich) urothelial carcinoma and urothelial carcinoma with squamous, glandular or
   trophoblastic differentiation were gu_urinary_picker rows coding 8120/3. D2 drops 8120 from the
   picker labels and its Preferred term does not name them, so they are one option on the
   histology screen, coding 8120/3, beside the invasive urothelial carcinoma option (D1, Liu
   2025). Registrar question 3 (Rule K's higher code for lipid-rich, glycogen-rich and glandular)
   stays open and the reason says so.
8. gu_penis_hpv was an ihc_checklist whose rules were "p16 positive" (8085/3), "p16 negative"
   (8086/3) and neither (8070/3). app.js meets a `negative` requirement with a marker that is
   off, unrecorded or unreadable (markerOff), so the "p16 negative" rule fires on a report with
   no p16 result and records HPV negative: a code the evidence does not support. The screen is a
   histology_subclassification with the three answers, the shape group11_common.nut_nodes uses
   for the same reason. The tree has no ihc_checklist.
9. gu_penis_scc_subtype: the warty carcinoma label adds warty-basaloid carcinoma, which ICD-O-3.2
   lists as a related term of 8054/3 (D5: the one code that covers both terms). The hint states
   D5: a named subtype's code is recorded whatever HPV status the report gives (registrar
   question 2), and Rule K for two named subtypes no option covers.
10. Inflammatory myofibroblastic tumour: the evidence made it an exclusion (8825/1) on
   gu_urinary_histology. The controller's task instruction refers it to Group IX with
   rhabdomyosarcoma: Pfister 2022 (p. 6) classes it with the soft tissue tumours, and the
   Group IX tree's fibroblastic screen holds the 8825/1 exclusion with the registrar's decision
   required and Myofibroblastic sarcoma (8825/3). The reason states behaviour 1. Registrar
   question 9 stays open.
11. The referrals the evidence gives one code carry it as refer_code: paraganglioma 8693
   (Group IV), stromal sarcoma of the prostate 8935 and mesothelioma of the tunica vaginalis 9050
   (Group XII). Nephroblastoma and renal cell carcinoma refer to Group VI with no code (the
   evidence names 8960, 8311 and 8312). The module checks against ICCC-2017.sqlite that each
   referral's codes sit in the named group at every routed site.
12. The trailing options are the common ones (tail_options): melanoma (D13), the picker, the
   exclusion screen, the deposit question (D10), "Malignant tumour, type not determined" (Group
   XII, 8000, D7), and the referrals: lymphoma (II, keeps the site, Rule D; the reason names the
   organ, not the family), leukaemia (I, C42.1; the evidence has no leukaemia answer), sarcoma
   (IX, with the evidence's rhabdomyosarcoma, rhabdoid tumour and Kaposi sarcoma examples), germ
   cell tumour (X, with the evidence's trophoblastic-differentiation sentence) and another named
   tumour (XII). The deposit option keeps the evidence's "or direct spread" wording and its
   prostate example. The evidence's deposit referral (refer_group null with recapture_site) is
   the deposit question. NUT carcinoma has no option: D12 names no urinary or male genital organ,
   so 8023/3 is a picker entry.
13. Melanoma (D13): no organ of this tree is skin (the penis, NOS and the scrotum go to the skin
   tree), so the hop enters me_mucosa. T2c to confirm the screen takes a melanoma of the urethra,
   bladder or glans penis.
14. The exclusion screens merge into gu_not_malignant, organ named in brackets. Inflammatory
   myofibroblastic tumour leaves it (departure 10). The three Rule F hints are one sentence
   appended to the common hint. "Another benign lesion" is the common catch-all.
15. gu_picker: D2 replaces the three curated pickers. Labels are ICD-O-3.2 Preferred terms with
   live synonyms and related terms as search_terms and no recognition aid (Group 10's picker
   shape), so the evidence's picker labels and aids (the pure squamous cell carcinoma aid, now on
   the squamous cell carcinoma option; the urachal aid, now in the gate hint; the medullary
   carcinoma aid) are not shown; the build report lists them. The picker keeps the codes the
   histology screens offer only under an organ label whose Preferred term names no organ
   (picker_keep): 8120 (urothelial carcinoma arising in the prostate, ICCR-Pro p. 4) and the
   penile squamous cell carcinoma subtypes 8051, 8052, 8054, 8074, 8082, 8083, 8084, 8085, 8086,
   valid at every routed site (verrucous and lymphoepithelioma-like carcinoma are WHO urinary
   entities, ICCR-Bla p. 10-11). The prostate picker's Rule H note (ductal and basal cell
   carcinoma keep the prostate) is in the histology hint.
16. Not built from the evidence: 8130/3 and 8440/3 (D3), 8323/3 for mixed adenocarcinoma (the
   later ICCR prints 8140/3; registrar question 4), 8314/3 and 8315/3 (the WHO prints 8120/3;
   registrar question 3), and 8122/3 for plasmacytoid carcinoma (the ICCR with the July 2024
   corrigenda prints sarcomatoid 8122/3 and no code for plasmacytoid). awaiting_layer1 is not
   carried for 8054, 8085 and 8086: standing rule 16; they go on the REDCap-side list.

Registrar questions the evidence raised (XIf8_urinary_male_genital.json questions 1-9) stay open;
the defaults above apply until they are answered. Data gaps 7 and 8 (no primary paediatric series
of invasive urothelial carcinoma; none at the renal pelvis, ureter or urethra) are the
controller's: the invasive urothelial carcinoma option is offered at every urinary organ, as the
evidence's gu_urinary_histology offered it.
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, VISSER, aid, cyto, deposit_node, evidence_gate,
                            excl, go, iccc_status, lab, make_tree, marker, named, node, nonrep,
                            not_malignant_node, refer, refer_leukaemia, refer_other_named,
                            refer_sarcoma, refer_unspecified, tail_options, term, tree_row,
                            TreeError)

TREE_ID = "g11_urinary_male_genital"
P = "gu_"
WHERE = "the urinary tract or male genital organs"
EVIDENCE = "XIf8_urinary_male_genital"
VISSER_NOTE = ("Visser O, et al. Front Oncol 2023;13:1250549, Table 4, p. 06, read from the page "
               "image (contract §0.5), with rule 6, p. 05.")

URINARY = "(bladder, renal pelvis, ureter or urethra)"
NOT_PENIS = "(bladder, renal pelvis, ureter, urethra, prostate, or a male genital organ other than " \
            "the penis)"


def n(name: str) -> str:
    return P + name


GROUP_NAMES = {
    1: "Group I (leukaemias)", 2: "Group II (lymphomas)",
    4: "Group IV (neuroblastoma and other peripheral nervous cell tumours)",
    6: "Group VI (renal tumours)", 9: "Group IX (soft tissue sarcomas)",
    10: "Group X (germ cell tumours)",
    12: "Group XII (other and unspecified malignant neoplasms)",
}
ROMAN = {1: "I", 2: "II", 4: "IV", 6: "VI", 9: "IX", 10: "X", 12: "XII"}


def _in_group_everywhere(codes, group):
    """The source-of-truth check behind every referral reason that says 'ICCC-3 places that code
    in Group N at these sites': each code (behaviour 3) sits in that group at every routed site
    of the tree, read from ICCC-2017.sqlite."""
    want = "other:%s" % ROMAN[group]
    for c in codes:
        for site in tree_row(TREE_ID)["sites"]:
            got = iccc_status(c, site)
            if got != want:
                raise TreeError("%s: ICCC-2017 places %s/3 at %s in %s, not %s; the referral's "
                                "reason would be false" % (TREE_ID, c, site, got,
                                                           GROUP_NAMES[group]))


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# ICCR-Bla p. 4 "Tumour invades subepithelial connective tissue"; Liu section 8 "often confined
# to the mucosal layer (Ta) with rare infiltration into deeper layers" (evidence
# gu_urinary_histology option 1 aid).
AID_INVASIVE_UC = ("The report states invasion of the lamina propria (subepithelial connective "
                   "tissue) or deeper, pT1 or higher.")
# ICCR-Bla p. 8 "a tumour is classified as a urothelial carcinoma if there is any identifiable
# urothelial component" (evidence gu_urinary_picker, pure squamous cell carcinoma aid).
AID_PURE_SCC = ("At the bladder and urinary tract the tumour is entirely squamous, with no "
                "urothelial component and no urothelial carcinoma in situ; a squamous tumour with "
                "a urothelial component is a urothelial carcinoma.")
# ICCR-Bla p. 12 "which will not invade or metastasise" (evidence gu_not_malignant_urinary,
# PUNLMP aid).
AID_PUNLMP = ("The report places the papillary tumour below low-grade carcinoma; it does not "
              "invade or metastasise.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence gu_document_inventory, gu_cytology; tissue_free; lab_tests)
# ------------------------------------------------------------------------------------------
def _markers():
    """The Visser Table 4 rows that concern these organs (D7): chromogranin A for a
    neuroendocrine tumour (8240/3 at basis 4), and prostate-specific antigen for a prostate
    cancer, which Table 4 gives 8000/3, a Group XII code at these sites."""
    return [
        # Evidence tissue_free row 3 and gu_document_inventory option 3; ICCR-Bla p. 11 "Well
        # differentiated neuroendocrine tumour 8240/3" (the entity at the bladder). Visser Table
        # 4, p. 06: neuroendocrine tumour, chromogranin A (the row names no site). Data gap 6.
        marker("8240", test="serum chromogranin A", diagnosis="neuroendocrine tumour",
               where="of the urinary tract or a male genital organ",
               note=VISSER_NOTE + " Evidence XIf8_urinary_male_genital.json tissue_free row 3; "
                                  "data gap 6 (no file in this part gives serum chromogranin A "
                                  "a diagnostic role at these sites)."),
        # Contract §0.5: Visser Table 4 gives prostate cancer with prostate-specific antigen the
        # code 8000/3 at basis 4, not a specific code; ICCC-2017 range 143 places 8000/3 in XIIb
        # at C61.9. Not in the evidence file (departure 3).
        refer_unspecified(
            "Imaging shows a tumour of the prostate, and the report calls prostate-specific "
            "antigen raised", "8000", 4,
            "A prostate cancer shown on imaging with a raised prostate-specific antigen is "
            "registered without a tumour type (%s, Table 4)." % VISSER,
            where=WHERE,
            captures={"workup_status": "incomplete", "basis_evidence_tier": "markers_psa"},
            note="D7 and contract §0.5: Visser 2023 Table 4, p. 06 (prostate cancer, "
                 "prostate-specific antigen, 8000/3), read from the page image. ICCC-2017 range "
                 "143 holds 8000/3 in XIIb at C61.9. Departure 3."),
    ]


def _refer_lymphoma():
    """WHO Rule D through the common Group II referral, with a reason that names the organ,
    not the tree's family (departure 12)."""
    return refer("Lymphoma", 2,
                 "A lymphoma belongs to ICCC-3 Group II. A lymphoma that arises in the bladder, "
                 "the urinary tract or a male genital organ keeps that organ as its site (WHO "
                 "Rule D: an extranodal lymphoma is coded to its site of origin). Code the case "
                 "from the Group II (lymphomas) tree.",
                 note="ICD-O-3.1 Rule D, p. 15. The hop carries the case's site. Evidence "
                      "gu_cytology option 5 and the lymphoma answer of every histology screen.")


def gate():
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour of the urinary tract or male genital "
                 "organs?",
        # Evidence gu_site hint and options (departure 1). ICCR-Bla p. 9 "diagnosis of urachal
        # carcinoma include location in the bladder dome or anterior wall"; ICCR-RPU p. 11
        # "Invasion of the renal parenchyma is included in the definition of pT3 disease.";
        # Rules PDF p. 5 "tumor overlaps the boundaries of two or more categories or
        # subcategories", "C68.8 Overlapping lesion of urinary organs", "C63.8 Overlapping
        # lesion of male genital organs"; evidence gu_document_inventory hint (prostate-specific
        # antigen).
        hint=("A radiology report counts as imaging. A pathology report on a biopsy, "
              "transurethral resection or resection counts as histology. A biopsy or cytology "
              "report that calls the specimen inadequate or non-diagnostic counts as no tissue. "
              "A urachal carcinoma, at the bladder dome or anterior wall and centred in the "
              "bladder wall, is recorded at the urachus (C67.7). A renal pelvis tumour that "
              "invades the kidney stays at the renal pelvis (C65.9). One tumour across two parts "
              "of the bladder whose origin the report does not give is recorded at overlapping "
              "lesion of bladder (C67.8); across two urinary organs at C68.8; across two male "
              "genital organs at C63.8; across two parts of the penis at C60.8. A report that "
              "names only the tissue around an organ, such as perivesical, periprostatic or "
              "periurethral tissue, does not name that organ. If the site recorded does not "
              "follow these rules, go back to the site step. A raised prostate-specific antigen "
              "alone does not register a tumour, and a report that calls the tumour possible or "
              "suspected does not register it."),
        # Evidence lab_tests (prostate-specific antigen) and tissue_free row 3 (chromogranin
        # A). The evidence prints no unit (departure 3).
        labs=[
            lab("chromogranin_a", "Serum chromogranin A", ("ng/mL", "µg/L", "nmol/L")),
            lab("prostate_specific_antigen", "Serum prostate-specific antigen (PSA)",
                ("ng/mL", "µg/L")),
        ],
        marker_tests="chromogranin A or prostate-specific antigen",
        markers=_markers(),
        tier_labels={
            "imaging": "An imaging report only (ultrasound, CT or MRI) - no chromogranin A or "
                       "prostate-specific antigen result, no tissue",
            # Evidence gu_document_inventory option 6.
            "cytology": "A cytology report (urine, bladder washing, brushing or fine-needle "
                        "aspiration) - no histology report",
            # Evidence gu_document_inventory option 7.
            "histology": "A histology report on a biopsy, transurethral resection or "
                         "resection, with or without immunohistochemistry or gene reports",
        },
        cytology=[
            # Netto PDF p. 9 "Positive for high-grade urothelial Ca (HGUC)" and "staging cannot
            # be achieved on cytology". Evidence gu_cytology option 1; registrar question 7.
            cyto("Positive for high-grade urothelial carcinoma (urine or bladder washing)", "8120",
                 "Urine cytology cannot tell an invasive carcinoma from urothelial carcinoma in "
                 "situ, which Group XI does not register; a histology report decides. This "
                 "awaits the registrar's decision.",
                 note="Evidence gu_cytology option 1; registrar question 7 (8120/3 or 8010/3)."),
            # Evidence gu_cytology option 2 ("such as squamous cell carcinoma, adenocarcinoma or
            # small cell carcinoma"); departure 4.
            cyto("Squamous cell carcinoma", "8070",
                 note="Evidence gu_cytology option 2, the first type it names."),
            cyto("Adenocarcinoma", "8140",
                 note="Evidence gu_cytology option 2, the second type it names."),
            cyto("Small cell carcinoma, or small cell neuroendocrine carcinoma", "8041",
                 "ICD-O-3.2 gives Small cell neuroendocrine carcinoma as a related term of this "
                 "code.", note="Evidence gu_cytology option 2, the third type it names."),
            # Evidence gu_cytology option 3; departure 4.
            cyto("Cytology names a carcinoma without naming its type, or names a carcinoma type "
                 "this list does not show", "8010",
                 "A carcinoma type this list does not show is recorded at this code from "
                 "cytology; the histology report gives that type's own code.",
                 note="Evidence gu_cytology option 3, widened to a named type the list lacks "
                      "(the nearest generic code, as D4 rules for an entity without a code)."),
            # Evidence gu_cytology option 5.
            _refer_lymphoma(),
            # Netto PDF p. 9 "Suspicious for high-grade urothelial Ca (SHGUC)", "Atypical
            # urothelial cells (AUC)", "Low-grade urothelial neoplasm (LGUN)". Evidence
            # gu_cytology option 6.
            nonrep("Suspicious for high-grade urothelial carcinoma, atypical urothelial cells, "
                   "or low-grade urothelial neoplasm",
                   "Not registrable. Cytology that calls the cells suspicious or atypical leaves "
                   "cancer only possible (%s, rule 4). A low-grade urothelial neoplasm on "
                   "cytology names the low-grade papillary lesions, which ICD-O-3.2 codes below "
                   "behaviour 3; a histology report decides." % VISSER,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "cytology_urothelial_atypia"},
                   note="Evidence gu_cytology option 6 (the Paris system categories)."),
        ],
        note="Evidence gu_document_inventory, tissue_free and lab_tests (departures 1 to 3 in "
             "the module docstring).")


# ------------------------------------------------------------------------------------------
# Histology (evidence gu_urinary_histology, gu_prostate_histology, gu_penis_histology,
# gu_male_genital_histology), one screen (D14)
# ------------------------------------------------------------------------------------------
def _refer_coded(label, group, code_, note, *, extra=""):
    """A referral that names the one code the other group records (departure 11)."""
    _in_group_everywhere([code_], group)
    reason = ("ICD-O-3.2 codes it as %s (%s/3). ICCC-3 places that code in %s at every site of "
              "the urinary tract and male genital organs, not in Group XI.%s Code the case from "
              "the %s tree." % (term(code_, "3"), code_, GROUP_NAMES[group],
                                (" " + extra) if extra else "", GROUP_NAMES[group]))
    return refer(label, group, reason, refer_code=code_, note=note)


def _referrals():
    """The not-a-carcinoma referrals of the merged screen (departures 10 to 12)."""
    _in_group_everywhere(["8900", "8910", "8920", "8963", "9140"], 9)
    _in_group_everywhere(["8825"], 9)
    _in_group_everywhere(["9071", "9080", "9100"], 10)
    _in_group_everywhere(["8960", "8311", "8312"], 6)
    return [
        _refer_lymphoma(),
        refer_leukaemia(WHERE),
        # Pfister p. 6 "with rhabdomyosarcomas (RMS) being the most common"; Liu section 8 "other
        # pediatric malignancies, including Wilms tumor and bladder rhabdomyosarcoma". ICCC-2017:
        # 8900-8920 IXa, 8963 IX, 9140 IXc at every routed site.
        refer_sarcoma(WHERE, label="A sarcoma, such as rhabdomyosarcoma (embryonal, botryoid or "
                                   "alveolar), malignant rhabdoid tumour or Kaposi sarcoma"),
        # Pfister p. 6 "Infantile fibrosarcoma and inflammatory myofibroblastic tumor are both
        # tyrosine kinase". Controller's instruction (departure 10); registrar question 9.
        refer("Inflammatory myofibroblastic tumour, or myofibroblastic sarcoma", 9,
              "ICD-O-3.2 codes an inflammatory myofibroblastic tumour as %s (8825/1), behaviour "
              "1, and a myofibroblastic sarcoma as %s (8825/3). Both are soft tissue tumours, "
              "which ICCC-3 places in Group IX, not Group XI. Code the case from the Group IX "
              "(soft tissue sarcomas) tree, which records whether it is registered."
              % (term("8825", "1"), term("8825", "3")),
              note="Departure 10. Evidence gu_urinary_histology option 6 (an exclusion there); "
                   "the Group IX tree's fibroblastic screen holds the 8825/1 exclusion "
                   "(registrar_decision_required) and 8825/3 (IXb1). Registrar question 9."),
        # Pfister p. 12 "Embryonal carcinoma Yolk sac tumor"; Netto p. 7 "8120/3 Urothelial
        # carcinoma with trophoblastic differentiation". ICCC-2017: 9071, 9080, 9100 Group X at
        # every routed site.
        refer("Yolk sac tumour, teratoma, choriocarcinoma or another germ cell tumour", 10,
              "Germ cell tumours belong to ICCC-3 Group X at the urinary tract and male genital "
              "organs. A urothelial carcinoma with trophoblastic differentiation is a carcinoma, "
              "not a choriocarcinoma: take the urothelial carcinoma option instead. Code a germ "
              "cell tumour from the Group X (germ cell tumours) tree.",
              note="Evidence conflicts, Group 10: extragonadal germ cell tumours are Xb at these "
                   "sites; the testis is Group X's own site."),
        # Pfister p. 12 "Nephroblastic and related tumors Pediatric cystic nephroma
        # Nephroblastoma" and "Renal cell carcinoma with MIT translocations". ICCC-2017: 8960
        # VIa1, 8311 and 8312 VIb at every routed site.
        refer("Nephroblastoma (Wilms tumour), or a renal cell carcinoma such as translocation "
              "renal cell carcinoma", 6,
              "Nephroblastoma and renal cell carcinomas are ICCC-3 Group VI (renal tumours) "
              "codes at every site of the urinary tract, not Group XI codes. Code the case from "
              "the Group VI (renal tumours) tree.",
              note="Evidence gu_urinary_histology option 8; conflicts, Group 6 (8960, 8311, "
                   "8312, 8316-8319, 8361 at C65.9 and C66.9)."),
        # ICCR-Bla p. 11 "Paraganglioma is not an epithelial derived tumour." ICCC-2017: 8693
        # IVb at every routed site.
        _refer_coded("Paraganglioma", 4, "8693",
                     "Evidence gu_urinary_histology option 7; conflicts, Group 4.",
                     extra="A paraganglioma is not an epithelial tumour."),
        # ICCR-Pro p. 7 "Stromal sarcoma 8935/3"; Netto p. 2 "8935/3 Stromal sarcoma".
        # ICCC-2017: 8935 XIIa4 at every routed site.
        _refer_coded("Stromal sarcoma (prostate)", 12, "8935",
                     "Evidence gu_prostate_histology option 4; conflicts, Group 12."),
        # Evidence gu_male_genital_histology option 5 (no page quotation). ICCC-2017: 9050 XIIa5
        # at every routed site.
        _refer_coded("Mesothelioma, such as mesothelioma of the tunica vaginalis", 12, "9050",
                     "Evidence gu_male_genital_histology option 5; conflicts, Group 12."),
        refer_other_named(),
    ]


def histology():
    opts = [
        # Netto p. 7 "8120/3 Invasive urothelial carcinoma", "8120/3 Nested urothelial carcinoma";
        # Liu section 8 "often confined to the mucosal layer (Ta) with rare infiltration into
        # deeper layers", "childhood bladder urothelial carcinoma is typically low-grade". D1.
        aid(named("Invasive urothelial (transitional cell) carcinoma, including papillary "
                  "urothelial carcinoma with invasion and the conventional, nested, large nested, "
                  "tubular and microcystic subtypes %s" % URINARY, "8120",
                  "ICD-O-3.2 gives Urothelial carcinoma, NOS as a synonym of this code.",
                  note="D1: Liu 2025 (evidence §11). Evidence gu_urinary_histology option 1. "
                       "8130/3 is all-[obs] (D3): papillary urothelial carcinoma with invasion "
                       "records 8120/3 (evidence code_currency 8130)."),
            AID_INVASIVE_UC),
        # Netto p. 7 "8120/3 Urothelial carcinoma with squamous differentiation", "8120/3
        # Urothelial carcinoma with trophoblastic differentiation", "8120/3 Lipid-rich urothelial
        # carcinoma", "8120/3 Clear cell (glycogen-rich) urothelial carcinoma"; ICCR-Bla p. 10
        # image "Plasmacytoid (no code printed)". Departure 7; registrar question 3.
        named("Plasmacytoid, lipid-rich or clear cell (glycogen-rich) urothelial carcinoma, or "
              "urothelial carcinoma with squamous, glandular or trophoblastic differentiation %s"
              % URINARY, "8120",
              "The WHO classification codes these subtypes with invasive urothelial carcinoma. "
              "This awaits the registrar's decision.",
              note="Departure 7: the evidence's gu_urinary_picker rows 1-3 (8120/3); data gap 10; "
                   "registrar question 3 (Rule K would give 8314, 8315 or 8140)."),
        # D1 exception: the code needs the subtype and the HPV status. ICCR-Pen p. 10 Table 1.
        go("Squamous cell carcinoma, of any subtype or with no subtype named (penis)",
           n("penis_scc_subtype"),
           note="D1 exception (subtype and HPV status screens). Evidence gu_penis_histology "
                "option 1."),
        # Netto p. 7 "8010/3 Urachal carcinoma"; ICCR-Bla p. 9 "If a diagnosis of urachal
        # carcinoma is rendered the subtype must be specified." Evidence gu_urinary_histology
        # option 4, gu_prostate_histology option 3, gu_penis_histology option 3,
        # gu_male_genital_histology option 3; gu_urinary_picker row 16 (departure 6).
        named("A carcinoma whose type the report does not name, or a urachal carcinoma with no "
              "subtype named", "8010",
              "A named urachal carcinoma subtype, such as mucinous adenocarcinoma, gives that "
              "subtype's own code.",
              upgrade=TYPE_NOT_STATED,
              note="The generic option of the screen (D4's nearest generic code); data gap 9 "
                   "(no paediatric source)."),
        # Netto p. 7 "8140/3 Adenocarcinoma, NOS", "8140/3 Carcinoma of Skene glands"; ICCR-Bla p.
        # 11 "Mixed 8140/3"; Netto p. 2 "8140/3 Acinar adenocarcinoma"; ICCR-Pro p. 7 "The vast
        # majority (>95%) of prostate cancers are acinar adenocarcinomas." Departure 6.
        named("Adenocarcinoma with no type named, mixed adenocarcinoma, carcinoma of the Littre, "
              "Skene or Cowper glands, or acinar adenocarcinoma of the prostate (including its "
              "pleomorphic giant cell and prostatic intraepithelial neoplasia-like subtypes)",
              "8140",
              "ICD-O-3.2 gives Acinar adenocarcinoma of prostate and Carcinoma of Skene, Cowper "
              "and Littre glands as related terms of this code. ICD-O-3.2 has no term mixed "
              "adenocarcinoma. A report that says %s (8323/3) or %s (8255/3) is found under "
              "another carcinoma the report names."
              % (term("8323", "3"), term("8255", "3")),
              upgrade="A report that names another adenocarcinoma type, such as mucinous, "
                      "enteric or ductal adenocarcinoma, gives that type's own code: find it "
                      "under another carcinoma the report names.",
              note="Departure 6. Evidence gu_male_genital_histology option 1; gu_urinary_picker "
                   "rows 11, 14, 17; gu_prostate_picker row 1. Mixed adenocarcinoma: registrar "
                   "question 4 (Netto prints 8323/3; the ICCR with the July 2024 corrigenda "
                   "prints 8140/3). Registrar ruling of 8 October 2026 on review A1 (a)(b), "
                   "docs/group_11_evidence/registrar_A1ab_rules.md C8 (a8): ICD-O-3.2 prints no "
                   "term mixed adenocarcinoma and ICD-O-3.1 Rule J (p. 24) reaches no printed "
                   "term, so the code stays 8140/3 and the reason names the two printed terms "
                   "(8323/3 and 8255/3), which the picker holds."),
        # ICCR-Bla p. 11 "Pure squamous cell carcinoma 8070/3"; Netto p. 2 "8070/3 Squamous cell
        # carcinoma". Departure 6.
        aid(named("Squamous cell carcinoma %s" % NOT_PENIS, "8070",
                  note="Departure 6. Evidence gu_male_genital_histology option 2; "
                       "gu_urinary_picker row 9; gu_prostate_picker row 8."),
            AID_PURE_SCC),
    ] + tail_options(
        P, "mucosa", where=WHERE,
        not_malignant_label="A lesion the report calls benign, borderline, non-invasive or in "
                            "situ, such as a papilloma, papillary urothelial neoplasm of low "
                            "malignant potential, non-invasive papillary urothelial carcinoma "
                            "(pTa), carcinoma in situ, prostatic or penile intraepithelial "
                            "neoplasia, or dysplasia",
        referrals=_referrals())
    for o in opts:
        if o.get("next_node") == n("deposit"):
            # ICCR-Bla p. 6 "Most cases of secondary involvement of the urinary bladder represent
            # direct extension" (evidence deposit answers, departure 12).
            o["label"] = ("A deposit (metastasis) or direct spread of a tumour that began "
                          "elsewhere, such as a urothelial carcinoma of the bladder that extends "
                          "into the prostate")
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence gu_urinary_histology hint (ICCR-Bla p. 8; Rule K, Rules PDF p. 11) and
        # gu_prostate_picker hint (Rule H, Rules PDF p. 10 "should be disregarded if the tumor
        # is known to arise at another site").
        "Use the report's final diagnosis. An option that names organs in brackets belongs to "
        "those organs: take it only when the site recorded is one of them. A tumour with any "
        "urothelial component, including urothelial carcinoma in situ, is a urothelial "
        "carcinoma, except a neuroendocrine carcinoma: find that under another carcinoma the "
        "report names. When the report gives two terms for one tumour and no single option "
        "covers both, choose the one with the higher code (WHO coding Rule K). Ductal "
        "adenocarcinoma and basal cell carcinoma of the prostate are found under another "
        "carcinoma the report names and keep the prostate as the site (WHO coding Rule H).",
        opts, [],
        "Evidence gu_urinary_histology, gu_prostate_histology, gu_penis_histology and "
        "gu_male_genital_histology, merged (D14; departures 5 to 13). D1: invasive urothelial "
        "carcinoma is the one carcinoma a paediatric source reports at these organs (Liu 2025, "
        "bladder only; data gaps 7 and 8); penile squamous cell carcinoma is an option because "
        "its code needs the subtype and HPV status. Rule G: no screen offers a grade (evidence "
        "rules_a_to_k G).")


def penis_scc_subtype():
    return node(
        n("penis_scc_subtype"), "histology_subclassification", 4,
        "Squamous cell carcinoma subtype",
        "Which subtype of squamous cell carcinoma of the penis does the report name?",
        # Evidence gu_penis_scc_subtype hint, with D5 (registrar question 2) and Rule K (Rules
        # PDF p. 3, printed p. 16).
        "Choose the subtype the report names. Its code is recorded whatever human papillomavirus "
        "(HPV) status the report gives. A report that names squamous cell carcinoma with no "
        "subtype, or the usual type, takes the last option, which asks the HPV status. When the "
        "report names two subtypes and no single option covers both, choose the one with the "
        "higher code (WHO coding Rule K).",
        [
            # ICCR-Pen p. 10 "Basaloid squamous cell carcinoma 8083/3".
            named("Basaloid squamous cell carcinoma", "8083"),
            # ICCR-Pen p. 10 "Warty carcinoma 8054/3"; icdo32.sqlite 8054/3 Synonym Condylomatous
            # carcinoma, Related Warty-basaloid carcinoma (departure 9).
            named("Warty (condylomatous) carcinoma, or warty-basaloid carcinoma", "8054",
                  "ICD-O-3.2 gives Condylomatous carcinoma as a synonym and Warty-basaloid "
                  "carcinoma as a related term of this code.",
                  note="D5: one code covers both terms of warty-basaloid carcinoma (departure "
                       "9). New in ICD-O-3.2; REDCap lacks it: the REDCap-side list."),
            # ICCR-Pen p. 10 "Clear cell squamous cell carcinoma 8084/3".
            named("Clear cell squamous cell carcinoma", "8084"),
            # ICCR-Pen p. 10 "Lymphoepithelial carcinoma 8082/3".
            named("Lymphoepithelial carcinoma", "8082"),
            # ICCR-Pen p. 10 "Verrucous carcinoma (including carcinoma cuniculatum) 8051/3".
            named("Verrucous carcinoma, including carcinoma cuniculatum", "8051"),
            # ICCR-Pen p. 10 "Papillary squamous cell carcinoma 8052/3".
            named("Papillary squamous cell carcinoma", "8052"),
            # ICCR-Pen p. 10 "Sarcomatoid squamous cell carcinoma 8074/3".
            named("Sarcomatoid squamous cell carcinoma", "8074",
                  "ICD-O-3.2 gives Squamous cell carcinoma, sarcomatoid as a synonym of this "
                  "code."),
            # ICCR-Pen p. 10 "Squamous cell carcinoma, usual type 8086/3"; p. 11 "p16 is not
            # available or is not performed the tumour should be designated as SCC-NOS".
            go("Squamous cell carcinoma with no subtype named, the usual type, or HPV-associated "
               "or HPV-independent squamous cell carcinoma with no subtype named", n("penis_hpv"),
               note="Evidence gu_penis_scc_subtype option 8."),
        ], [],
        "Evidence gu_penis_scc_subtype (departure 9). D1 exception: the code depends on the "
        "subtype. D5: a WHO subtype code that covers the report's terms is recorded; registrar "
        "question 2 (subtype codes lower than 8085).")


def penis_hpv():
    return node(
        n("penis_hpv"), "histology_subclassification", 5, "HPV status",
        "What does the report say about human papillomavirus (HPV) or p16?",
        # Evidence gu_penis_hpv hint; ICCR-Pen p. 16 "the p16 protein is upregulated and can be
        # detected in high risk HPV related malignancies".
        "A p16 immunostain stands for a high-risk human papillomavirus (HPV) test. A p16 result "
        "the report calls equivocal or unreadable counts as no result.",
        [
            # ICCR-Pen p. 10 "Squamous cell carcinoma, HPV-associated 8085/3"; p. 16 (as above).
            named("The report calls the carcinoma HPV-associated, or reports a positive "
                  "high-risk HPV test or a positive p16 immunostain", "8085",
                  "A positive p16 immunostain stands for a positive high-risk HPV test.",
                  note="Evidence ihc_rules 1 (departure 8). New in ICD-O-3.2; REDCap lacks it: "
                       "the REDCap-side list."),
            # ICCR-Pen p. 10 "Squamous cell carcinoma, HPV-independent"; p. 16 "The p16 protein
            # is not only a surrogate for HPV expression".
            named("The report calls the carcinoma HPV-independent, or reports a negative "
                  "high-risk HPV test or a negative p16 immunostain", "8086",
                  "A negative p16 immunostain stands for a negative high-risk HPV test.",
                  note="Evidence ihc_rules 2 (departure 8). New in ICD-O-3.2; REDCap lacks it: "
                       "the REDCap-side list."),
            # ICCR-Pen p. 11 "p16 is not available or is not performed the tumour should be
            # designated as SCC-NOS". Registrar question 6.
            named("The report gives no HPV status, and p16 was not done, not readable or not "
                  "reported", "8070",
                  "Without an HPV status or a p16 result the tumour is squamous cell carcinoma, "
                  "NOS. This awaits the registrar's decision.",
                  upgrade="A report that gives the HPV status or a p16 result gives a more "
                          "specific code: Squamous cell carcinoma, HPV positive (8085/3) or "
                          "Squamous cell carcinoma, HPV negative (8086/3).",
                  note="Evidence ihc_rules 3 (departure 8); registrar question 6 (8070/3 or "
                       "8086/3 for the usual type with no result)."),
        ], [],
        "Evidence gu_penis_hpv and ihc_rules, built as a choice (departure 8: app.js meets a "
        "negative requirement with an unrecorded marker, so an ihc_checklist 'p16 negative' rule "
        "would record 8086/3 for a report with no p16 result).")


def not_malignant():
    nm = not_malignant_node(
        P,
        [
            # Netto p. 7 "8120/0 Urothelial papilloma"; Liu section 8 "the two most common types
            # of bladder neoplasms in children, UP and PUNLMP"; Liu section 7 "comprised 17
            # patients, including 11 children diagnosed with UP".
            excl("Urothelial papilloma (bladder or urinary tract)", "8120", "0",
                 what="a urothelial papilloma"),
            # ICCR-Bla p. 12 "which will not invade or metastasise"; Liu section 8 (as above);
            # Liu section 7 "The study focused on six male children with PUNLMP".
            aid(excl("Papillary urothelial neoplasm of low malignant potential (PUNLMP), "
                     "including the inverted form (bladder or urinary tract)", "8130", "1",
                     what="a papillary urothelial neoplasm of low malignant potential"),
                AID_PUNLMP),
            # Netto p. 7 "8130/2 Noninvasive papillary urothelial carcinoma, low grade"; ICCR-Bla
            # p. 4 "Non-invasive papillary carcinoma"; Liu section 8 "(PUNLMP) and low-grade
            # urothelial carcinomas, often confined to the mucosal layer (Ta)".
            excl("Non-invasive papillary urothelial carcinoma, low grade or high grade (pTa), "
                 "including an inverted growth pattern (bladder or urinary tract)", "8130", "2",
                 what="a non-invasive papillary urothelial carcinoma"),
            # Netto p. 7 "8121/0 Urothelial papilloma, inverted".
            excl("Inverted urothelial papilloma (bladder or urinary tract)", "8121", "0",
                 what="an inverted urothelial papilloma",
                 extra="ICD-O-3.2 lists Urothelial papilloma, inverted as a related term of this "
                       "code."),
            # Netto p. 7 "8120/2 Urothelial carcinoma in situ".
            excl("Urothelial carcinoma in situ, flat (pTis) (bladder or urinary tract)", "8120",
                 "2", what="a urothelial carcinoma in situ"),
            # ICCR-Bla p. 10 image "Dysplasia (no code printed)".
            nonrep("Urothelial dysplasia, with no carcinoma (bladder or urinary tract)",
                   "Not registrable. Urothelial dysplasia with no carcinoma is not a malignant "
                   "tumour, and the WHO classification gives it no code.",
                   note="Evidence gu_not_malignant_urinary option 6."),
            # Netto p. 7 "8052/0 Squamous papilloma".
            excl("Squamous papilloma (bladder or urinary tract)", "8052", "0",
                 what="a squamous papilloma",
                 extra="ICD-O-3.2 gives Squamous papilloma as a synonym of this code."),
            # Netto p. 7 "8261/0 Villous adenoma".
            excl("Villous adenoma (bladder or urinary tract)", "8261", "0",
                 what="a villous adenoma"),
            # Netto p. 7 "8211/0 Tubular adenoma".
            excl("Tubular adenoma (bladder or urinary tract)", "8211", "0",
                 what="a tubular adenoma"),
            # Netto p. 7 "8263/0 Tubulovillous adenoma".
            excl("Tubulovillous adenoma (bladder or urinary tract)", "8263", "0",
                 what="a tubulovillous adenoma"),
            # Netto p. 7 "8140/2 Adenocarcinoma in situ".
            excl("Adenocarcinoma in situ (bladder or urinary tract)", "8140", "2",
                 what="an adenocarcinoma in situ"),
            # ICCR-Bla p. 9 "mucinous cystic tumour of low malignant potential". Evidence
            # code_currency 8472: the WHO code is a data gap (data gap 4).
            excl("Mucinous cystic tumour of low malignant potential (urachus)", "8472", "1",
                 what="a mucinous cystic tumour of low malignant potential",
                 extra="ICD-O-3.2 gives Mucinous tumor, NOS, of low malignant potential as a "
                       "synonym of this code."),
            # Netto p. 2 "8148/2 Prostatic intraepithelial neoplasia, high grade".
            excl("High-grade prostatic intraepithelial neoplasia (prostate)", "8148", "2",
                 what="a high-grade prostatic intraepithelial neoplasia",
                 extra="ICD-O-3.2 gives Prostatic intraepithelial neoplasia, high grade as a "
                       "synonym of this code."),
            # Netto p. 2 "8500/2 Intraductal carcinoma"; Netto p. 3 "is an exceedingly rare
            # finding in biopsies and prostatectomies".
            excl("Intraductal carcinoma of the prostate, with no invasive carcinoma (prostate)",
                 "8500", "2", what="an intraductal carcinoma with no invasive carcinoma",
                 extra="ICD-O-3.2 gives Intraductal carcinoma, NOS as a synonym of this code."),
            # Netto p. 2 "8440/0 Cystadenoma". Evidence code_currency 8440: every /3 term is
            # [obs] (D3).
            excl("Cystadenoma (prostate)", "8440", "0", what="a cystadenoma"),
            # Netto p. 2 "8935/1 Stromal tumor of uncertain malignant potential".
            excl("Stromal tumour of uncertain malignant potential (prostate)", "8935", "1",
                 what="a stromal tumour of uncertain malignant potential",
                 extra="ICD-O-3.2 gives Stromal tumor of uncertain malignant potential as a "
                       "related term of this code."),
            # ICCR-Pen p. 11 "High grade squamous intraepithelial lesion 8077/2".
            excl("High-grade squamous intraepithelial lesion, or HPV-associated penile "
                 "intraepithelial neoplasia (penis)", "8077", "2",
                 what="a high-grade squamous intraepithelial lesion",
                 extra="ICD-O-3.2 gives High grade squamous intraepithelial lesion as a synonym "
                       "of this code."),
            # ICCR-Pen p. 11 "Differentiated penile intraepithelial neoplasia 8071/2".
            excl("Differentiated penile intraepithelial neoplasia (penis)", "8071", "2",
                 what="a differentiated penile intraepithelial neoplasia",
                 extra="ICD-O-3.2 gives Differentiated penile intraepithelial neoplasia (PeIN) "
                       "as a related term of this code."),
            # Evidence gu_not_malignant_penis option 3 (no page quotation).
            excl("Squamous cell carcinoma in situ (penis)", "8070", "2",
                 what="a squamous cell carcinoma in situ"),
        ],
        where=WHERE,
        note="Evidence gu_not_malignant_urinary, gu_not_malignant_prostate and "
             "gu_not_malignant_penis, merged (departure 14); the inflammatory myofibroblastic "
             "tumour line is a Group IX referral (departure 10).")
    # Evidence hints of the three exclusion screens (Rule F, Rules PDF p. 2, printed p. 15).
    nm["hint"] += (" A non-invasive papillary urothelial carcinoma is pTa and urothelial "
                   "carcinoma in situ is pTis. If the report states invasion of the lamina "
                   "propria (subepithelial connective tissue) or deeper (pT1 or higher), or an "
                   "invasive carcinoma beside the lesion, go back and choose the invasive "
                   "carcinoma.")
    return nm


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
# Departure 15: offered only under an organ label, Preferred term names no organ, so the picker
# keeps them for the other organs.
PICKER_KEEP = ("8120", "8051", "8052", "8054", "8074", "8082", "8083", "8084", "8085", "8086")


def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), penis_scc_subtype(), penis_hpv(), not_malignant(),
                      deposit_node(P, where=WHERE)]
    return make_tree(TREE_ID, nodes,
                     subtype_screens=(n("penis_scc_subtype"), n("penis_hpv")),
                     picker_keep=PICKER_KEEP)


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8120/3": ("D1, D2, D8", EVIDENCE,
               "Invasive urothelial carcinoma of the bladder, renal pelvis, ureter or urethra "
               "(Liu 2025 reports infiltration beyond the mucosa in children) on the urinary and "
               "male genital histology screen, with the subtypes the WHO codes with it "
               "(plasmacytoid, lipid-rich, clear cell, divergent differentiation; registrar "
               "question 3); at basis 5 when urine cytology is positive for high-grade "
               "urothelial carcinoma (registrar question 7); in the picker for urothelial "
               "carcinoma arising in the prostate."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma whose type the report does not name, and urachal carcinoma with no "
               "subtype named (Netto 2022 Table 3), on the urinary and male genital histology "
               "screen; at basis 5 when cytology names a carcinoma without its type or a type "
               "the cytology screen does not show."),
    "8140/3": ("D8", EVIDENCE,
               "Adenocarcinoma with no type named, mixed adenocarcinoma (the ICCR prints 8140/3; "
               "registrar question 4), carcinoma of the Littre, Skene or Cowper glands and acinar "
               "adenocarcinoma of the prostate on the urinary and male genital histology screen; "
               "at basis 5 when cytology names an adenocarcinoma."),
    "8070/3": ("D8", EVIDENCE,
               "Squamous cell carcinoma of the urinary tract, prostate and male genital organs "
               "other than the penis on the histology screen; penile squamous cell carcinoma with "
               "no HPV status or p16 result (ICCR penis dataset, p. 11; registrar question 6); "
               "at basis 5 when cytology names a squamous cell carcinoma."),
    "8041/3": ("D2, D8", EVIDENCE,
               "Small cell carcinoma at basis 5 when cytology of the urinary tract or a male "
               "genital organ names it, and in the picker."),
    "8240/3": ("D2, D7", EVIDENCE,
               "Neuroendocrine tumour at basis 4 with imaging and a raised serum chromogranin A "
               "(Visser 2023 Table 4; evidence data gap 6), and in the picker."),
    "8083/3": ("D1, D2, D5", EVIDENCE,
               "Basaloid squamous cell carcinoma on the penile subtype screen (ICCR penis "
               "dataset, Table 1) and in the picker for the other organs."),
    "8054/3": ("D1, D2, D5", EVIDENCE,
               "Warty carcinoma, and warty-basaloid carcinoma (an ICD-O-3.2 related term), on "
               "the penile subtype screen (ICCR penis dataset, Table 1) and in the picker. New in "
               "ICD-O-3.2 and absent from REDCap: the REDCap-side list (standing rule 16)."),
    "8084/3": ("D1, D2, D5", EVIDENCE,
               "Clear cell squamous cell carcinoma on the penile subtype screen (ICCR penis "
               "dataset, Table 1) and in the picker."),
    "8082/3": ("D1, D2, D5", EVIDENCE,
               "Lymphoepithelial carcinoma on the penile subtype screen (ICCR penis dataset, "
               "Table 1) and in the picker, where lymphoepithelioma-like urothelial carcinoma "
               "finds it (ICCR bladder dataset, p. 10; registrar question 2)."),
    "8051/3": ("D1, D2", EVIDENCE,
               "Verrucous carcinoma, including carcinoma cuniculatum, on the penile subtype "
               "screen (ICCR penis dataset, Table 1) and in the picker for verrucous carcinoma of "
               "the urinary tract (ICCR bladder dataset, p. 11)."),
    "8052/3": ("D1, D2", EVIDENCE,
               "Papillary squamous cell carcinoma on the penile subtype screen (ICCR penis "
               "dataset, Table 1) and in the picker."),
    "8074/3": ("D1, D2", EVIDENCE,
               "Sarcomatoid squamous cell carcinoma on the penile subtype screen (ICCR penis "
               "dataset, Table 1) and in the picker; ICD-O-3.2 lists the sarcomatoid term as a "
               "synonym of 8074/3."),
    "8085/3": ("D1, D2", EVIDENCE,
               "Penile squamous cell carcinoma that the report calls HPV-associated or p16 "
               "positive (ICCR penis dataset, pp. 10 and 16), and in the picker. New in "
               "ICD-O-3.2 and absent from REDCap: the REDCap-side list (standing rule 16)."),
    "8086/3": ("D1, D2", EVIDENCE,
               "Penile squamous cell carcinoma that the report calls HPV-independent or p16 "
               "negative (ICCR penis dataset, pp. 10 and 16), and in the picker. New in "
               "ICD-O-3.2 and absent from REDCap: the REDCap-side list (standing rule 16)."),
}
