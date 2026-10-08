"""g11_female_genital (prefix fg_): carcinomas of the vulva (C51.0-C51.8), vagina (C52.9), cervix
(C53.x, ICCC-3 subgroup XIf7), uterine corpus (C54.x), uterus with no part named (C55.9), other
female genital organs (C57.x) and placenta (C58.9) (subgroup XIf10).

A family tree (contract §4.1, D14). It is built from docs/group_11_evidence/XIf7_female_genital.json
(the evidence agent's nodes fg_site, fg_evidence, fg_cytology, fg_histology, fg_picker, fg_scc,
fg_scc_hpv, fg_not_invasive and fg_deposit, its ihc_rules and its entities) with the builders in
build/group11_common.py, in the shape of build/group11_organs/thyroid.py. Every option's label,
code, behaviour, basis, reason and recognition aid comes from that file unless a departure below
says otherwise; the cite (file, PDF page, quotation) is the comment above the option or the aid.
File names in the comments are the evidence's own:
    Hohn       XIf7-cervix-XIf10-vulva-vagina__Hohn-2021.txt (Hohn AK, et al. 2020 WHO
               Classification of Female Genital Tumors. Geburtshilfe Frauenheilkd
               2021;81:1145-1153); "image" marks a quotation read from a table page image
    ICCR-Cx    XIf7-cervix__ICCR-Cervix-5th.txt (ICCR Carcinoma of the Cervix, 5th edition,
               version 5.0, October 2023)
    ICCR-Vu    XIf10-vulva__ICCR-Vulva-2nd.txt (ICCR Carcinoma of the Vulva, 2nd edition,
               version 2.1, October 2023)
    ICCR-Va    XIf10-vagina__ICCR-Vagina-1st.txt (ICCR Carcinoma of the Vagina, 1st edition,
               version 1.1, August 2021)
    ICCR-En    XIf10-endometrium__ICCR-Endometrial-5th.txt (ICCR Endometrial Cancer, 5th
               edition, version 5.1, August 2024)
    Wohlmuth   XIf7-cervix-XIf10-female-genital-paediatric__Wohlmuth-2021.txt (J Clin Med
               2021;10:722, SEER-18, girls aged 0 to 18); PubMed Central section numbers stand for
               pages
    Pfister    ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules      RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser     Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
               set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    fg_document_inventory  document_inventory  evidence gate (evidence fg_evidence)
    fg_clinical, fg_clinical_cytology  clinical_alias
    fg_imaging, fg_imaging_cytology  morphology_only
    fg_cytology            morphology_only     (evidence fg_cytology)
    fg_histology           histology_subclassification  (evidence fg_histology, with the
                                               referrals of evidence fg_picker)
    fg_scc                 histology_subclassification  (evidence fg_scc)
    fg_scc_hpv             histology_subclassification  (evidence fg_scc_hpv and ihc_rules 1-5)
    fg_not_malignant       histology_subclassification  (evidence fg_not_invasive, with the
                                               benign line of evidence fg_histology)
    fg_deposit             morphology_only      (D10; evidence fg_deposit)
    fg_picker              histology_subclassification  (D2; evidence fg_picker's coded lines)

Departures from the evidence nodes, and why
-------------------------------------------
1. fg_site is not built. The router's site step records the site and chose this tree, so the
   organ question is one the router already answers (D14). Vulva with no part named (C51.9) is a
   skin site in ICCC-2017 (range 124, XIe) and the router sends it to g11_skin (contract §4.1);
   the evidence's registrar question 5 on that routing stays open. The fg_site hint's Rule A and
   Rule C content moves to the gate's hint. Its example of an overlapping lesion ("the cervix and
   the vagina") is not carried: fg_deposit's hint gives the ICCR vagina convention that a vaginal
   carcinoma with a cervical carcinoma is the cervical carcinoma's spread, and the two sentences
   would contradict each other on one screen sequence.
2. fg_evidence: the referral and imaging-only tiers recorded 8000/3 at basis 1 and 2 on the gate
   itself. D7: each routes to its own screen (fg_clinical, fg_imaging), which refers the case to
   Group XII with refer_code 8000, because ICCC-2017 places 8000/3 in XIIb at every routed site
   (range 143). "The file calls the tumour possible or suspected only" is the common
   not-registrable line on those screens (Visser rule 4). "An immunohistochemistry or gene report
   only" is the referral tier of the document checklist, which catches a stain or gene report
   without the report it is read against (TIER_RATIONALE). The evidence names no laboratory test
   and no Visser Table 4 row concerns these sites (evidence lab_tests, tissue_free), so the gate
   has no laboratory screen and no marker tier. The hint drops "Choose the strongest report in
   the file", which the document checklist replaces.
3. fg_cytology: "Malignant cells, with no tumour type named" (8001/3 basis 5) is the common line
   that refers to Group XII with 8001 (D8). "No malignant cells, or an unsatisfactory smear" is
   the common set of non-diagnostic routes. The intraepithelial line keeps its own wording; its
   "suspicious for carcinoma" part is the common suspicious line. The lymphoma referral is kept.
4. fg_histology, D14 and the generic options. The clear cell adenocarcinoma option keeps the
   evidence's organs in brackets, "(cervix or vagina)", and comes first (D1: Wohlmuth 2021,
   paediatric common); the picker keeps 8310 for the corpus and the other organs, where the
   evidence offered it in its picker. Adenocarcinoma with no type named (evidence: cervix and
   uterus on the screen, vulva, vagina and C57 in the picker), squamous cell carcinoma (evidence:
   vulva on the screen, cervix and vagina in the picker) and carcinoma with no type named are the
   contract §4.2 generic options and carry no organ label: each records one code, in Group XI, at
   every routed site. Squamous cell carcinoma opens fg_scc at every site, because its code depends
   on the human papillomavirus status (D1 exception); at the uterus and C57 the evidence recorded
   8070/3 directly, which fg_scc's last line still records.
5. D4 and D5 on the adenocarcinoma option. ICD-O-3.2 holds no 8483 (adenocarcinoma,
   HPV-associated) and no 8484 (adenocarcinoma, HPV-independent, NOS), so neither is built and a
   report naming either reaches the generic adenocarcinoma option (8140/3). Registrar, 9 October
   2026 (review E11): no screen names an entity whose code ICD-O-3.2 lacks, so the option's label no
   longer names the two types. The evidence's HPV-associated line listed the patterns usual type,
   villoglandular, mucinous, intestinal, signet-ring cell and invasive stratified mucin-producing
   carcinoma under 8140/3. Four of those patterns have an ICD-O-3.2 code of their own
   (villoglandular carcinoma, a related term of 8263/3; mucinous adenocarcinoma 8480/3;
   adenocarcinoma, intestinal type 8144/3; signet ring cell carcinoma 8490/3). No single code
   covers "HPV-associated" with the pattern, so WHO coding Rule K records the pattern's higher code
   (D5): those four are picker entries and the screen's hint sends the clerk there. Usual type is
   a synonym of 8140/3 and invasive stratified mucin-producing carcinoma has no ICD-O-3.2 term, so
   both stay on the adenocarcinoma option.
6. D4 on mesonephric-like adenocarcinoma (9113, which ICD-O-3.2 lacks; ICCR-En p. 9). The
   evidence held the case unrecorded (not registrable) until the registrar rules. D4: a report
   naming it reaches the nearest generic option, adenocarcinoma with no type named (8140/3). The
   histology hint names it once, so that the clerk does not take the mesonephric adenocarcinoma
   referral (9110/3, Group XII), which is a different tumour. Registrar question 2 stays open.
7. fg_histology, the trailing options are the common ones (tail_options): melanoma (D13), the
   picker, the exclusion screen, the deposit question (D10), "Malignant tumour, type not
   determined" (Group XII, 8000, D7). The referrals follow, rhabdomyosarcoma first (Wohlmuth
   2021: sarcomas, mostly embryonal rhabdomyosarcoma, are the commonest malignancy at these
   sites), then the evidence picker's referrals (another sarcoma, carcinosarcoma, adenosarcoma,
   endometrial stromal sarcoma, mesonephric adenocarcinoma, myoepithelial carcinoma) and the
   germ cell line, then lymphoma (II), leukaemia (I, C42.1) and another named tumour (XII). A
   referral whose label names one ICD-O-3.2 code carries it as refer_code (adenosarcoma 8933,
   mesonephric adenocarcinoma 9110, myoepithelial carcinoma 8982); ICCC-2017 places each in Group
   XII at every routed site. Endometrial stromal sarcoma carries no organ label: ICCC-2017 places
   8930 and 8931 in Group XII at every routed site, so a label restricted to the uterus would send
   an extrauterine case to the Group IX line.
8. Melanoma (D13): the evidence's line hopped to a skin-or-mucosa question in the melanoma tree
   (mel_site; mel_mucosa for the vagina and cervix). group11_common offers one entry per screen,
   and these organs are mucosal sites, so the hop enters me_mucosa at every routed site. The
   melanoma tree must take a melanoma of the vulva, the hair-bearing skin of the labium majus
   included (Wohlmuth 2021 section 11 reports vulval melanoma at ages 0 to 18; evidence data gap
   9). NUT carcinoma has no option: D12 names no female genital site, so 8023/3 is a picker entry.
9. fg_scc: the growth-pattern lines run from the higher code to the lower (8083, 8076, 8072,
   8071, 8054, 8052, 8051), and the hint says to take the first line that matches. The evidence
   ran them in report order (keratinising first), so a report naming two patterns, such as
   keratinising and microinvasive, took the lower code; WHO coding Rule K records the higher
   (D5). The two human papillomavirus status lines (8085, 8086) and the test-result line stay
   first, as the evidence has them: either status code is higher than every pattern code.
10. fg_scc_hpv is built as a choice (histology_subclassification), not as an ihc_checklist.
   Evidence ihc_rules 3 and 4 record 8086/3 when p16 is not block-type or high-risk human
   papillomavirus is not detected: a rule with only a `negative` requirement. app.js meets a
   `negative` requirement with a marker that is off, never recorded or unreadable (markerOff), so
   on an ihc_checklist those rules fire on a report that gives no p16 or HPV result at all and
   record HPV negative without evidence (standing rule 8). As a choice the five rules are five
   answers in the evidence's order (first match wins), and the evidence's NOS fallback (8070/3)
   is the last answer. The NUT carcinoma screens of group11_common (nut_nodes) and
   g11_thoracic's tx_stains are built the same way. Registrar question 6 (may a test result
   decide the code when the diagnosis line states no status) stays open; the evidence's routing
   is the default.
11. fg_not_invasive becomes fg_not_malignant (the common exclusion screen), reached by the
   standard option, whose label carries the evidence's examples. The benign line of evidence
   fg_histology (Mullerian papilloma, condyloma acuminatum, mesonephric remnants) joins it. The
   evidence's Rule F hint (go back for an invasive carcinoma) is appended to the common hint.
   The mature teratoma line adds that an immature or malignant teratoma is coded in Group X.
12. fg_deposit is the common deposit question (D10). The evidence's "A tumour of the ovary"
   referral (Group X, recapture_site) is added first, because group11_common's DEPOSIT_PRIMARIES
   lacks the ovary (request for group11_common below). "A carcinoma or melanoma of another
   organ" is not built while SELF_REFERRAL is False; the common hint sends the clerk back to the
   site step. The evidence's hint sentence on a vaginal carcinoma beside a cervical carcinoma is
   appended (ICCR-Va p. 5).
13. fg_picker: D2 replaces the evidence's curated picker. Labels are ICD-O-3.2 Preferred terms,
   search_terms the live synonyms and related terms, and the options carry no recognition aid
   (Group 10's picker shape), so the evidence's picker aids are not shown: gastric type (MUC6,
   HIK1083), endometrioid (FIGO grade), intestinal type (CK20, CDX2), adenoid cystic carcinoma
   (Bartholin gland) and Skene gland carcinoma (prostatic markers); the build report lists them.
   The picker keeps 8140/3 as well as offering it on the screen (picker_keep), so that "Carcinoma
   of Skene, Cowper and Littre glands", a related term of 8140/3, is found by typing it. The four
   vulval skin-adnexal codes the evidence names that no ICCC-2017 range holds at C51.0-C51.8
   (8090, 8400, 8409, 8413) are D11 picker entries; D11 gives them XIe, their one ICCC subgroup
   (evidence registrar question 5). The evidence picker's Rule G and Rule H sentences are appended
   to the picker hint; its Rule J sentence is not, because the app.js filter matches every typed
   word in any order. Gastric-type mucinous carcinoma at the corpus (8144/3 or 8482/3, registrar
   question 3) and extramammary Paget disease confined to the epithelium (8542/3, the only code
   ICD-O-3.2 prints; registrar question 7) are picker entries under their ICD-O-3.2 terms.
14. Not built from the evidence: 8483/3, 8484/3, 8483/2, 8484/2 and 9113/3 (D4); the "A carcinoma
   not in this list" hop to a shared list (the D2 picker is that list).

Registrar questions 1 to 8 of the evidence stay open; the defaults above apply until they are
answered (docs/group_11_registrar_review.md, task T6).

Requests for group11_common.py (not patched here)
-------------------------------------------------
* deposit_node(prefix, *, where, extra_primaries=()) to put a site family's own primaries (here
  the ovary, Group X) among the recapture referrals. This module inserts the option into the
  returned node instead.
* picker_node / make_tree(picker_hint_extra="") to append a tree's Rule G and Rule H sentences to
  the picker hint. This module appends to the returned node's hint instead.
"""
from __future__ import annotations

from group11_common import (DEPOSIT_PRIMARIES, TYPE_NOT_STATED, aid, cyto, cyto_carcinoma_nos,
                            deposit_node, evidence_gate, excl, go, make_tree, named, node, nonrep,
                            not_malignant_node, refer, refer_leukaemia, refer_lymphoma,
                            refer_other_named, refer_sarcoma, tail_options, term)

TREE_ID = "g11_female_genital"
P = "fg_"
WHERE = "the female genital organs"
EVIDENCE = "XIf7_female_genital"
HPV = "human papillomavirus (HPV)"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# ICCR-Va p. 12 "clear cell carcinomas are typically positive with napsin A and hepatocyte
# nuclear factor 1-beta"; ICCR-Va p. 5 "primary vaginal adenocarcinomas of clear cell, gastric or
# human papillomavirus (HPV)-associated types arise in adenosis".
AID_CLEAR_CELL = ("Reports may mention vaginal adenosis, or staining for napsin A and hepatocyte "
                  "nuclear factor 1-beta.")
# The report wordings of the evidence's fg_picker options 2 and 4, merged into the adenocarcinoma
# option (departure 5): ICCR-Cx p. 19 image "Adenocarcinoma, HPV-associated 8483/3*"; Hohn p. 6
# image "Usual type"; ICCR-Cx p. 19 image "Adenocarcinoma, HPV-independent, NOS 8484/3*"; the
# fg_picker option 2 label ("invasive stratified mucin-producing carcinoma").
AID_ADENO = ("Reports may write adenocarcinoma, usual type, or invasive stratified "
             "mucin-producing carcinoma.")
# ICCR-Cx p. 29 "Diffuse immunoreactivity (nuclear and cytoplasmic) for p16 is a surrogate marker
# of integrated high risk"; ICCR-Vu p. 16 "the two accepted tools for confirming an
# HPV-association are the direct identification of HPV".
AID_HPV_ASSOCIATED = ("Reports may describe block-type (diffuse and strong) p16 staining, or "
                      "high-risk human papillomavirus detected in the tumour.")
# ICCR-Va p. 12 "mesonephric carcinomas with GATA3, CD10 and TTF1".
AID_MESONEPHRIC = ("Reports may mention staining for GATA3, CD10 or thyroid transcription factor "
                   "1 (TTF-1).")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence fg_evidence, fg_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    nodes = evidence_gate(
        P, where=WHERE,
        question="What is in the file for this tumour of the vulva, vagina, cervix, uterus or "
                 "another female genital organ?",
        # Common hint, with evidence fg_site's Rule C and Rule A content (departure 1): Rules
        # p. 5 "Overlapping lesion of female genital organs"; p. 2 "its point of origin cannot
        # be determined"; p. 1 "If the diagnosis does not specify the tissue of origin".
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology, and a cervical or vaginal smear counts as cytology. A biopsy "
              "or cytology report that calls the specimen inadequate or non-diagnostic counts as "
              "no tissue. The site is the part the report says the tumour began in: a tumour "
              "that involves two parts whose origin the report does not state is an overlapping "
              "lesion of the female genital organs (C57.8). A carcinoma of the skin of the "
              "perineum or groin is a skin tumour, not a vulval one. A report that calls the "
              "tumour possible or suspected does not register it."),
        tier_labels={
            "imaging": "An imaging report only (ultrasound, computed tomography or magnetic "
                       "resonance imaging) - no tissue",
            "cytology": "A cytology report (a cervical or vaginal smear, or a fine-needle "
                        "aspirate) - no histology report",
            "histology": "A histology report, with or without immunohistochemistry or gene "
                         "reports",
        },
        cytology=[
            # Evidence fg_cytology option 0. No cite in the evidence beyond the screen's hint.
            cyto("Squamous cell carcinoma", "8070", note="Evidence fg_cytology option 0."),
            # Evidence fg_cytology option 1.
            cyto("Adenocarcinoma", "8140", note="Evidence fg_cytology option 1."),
            # Evidence fg_cytology option 2.
            cyto_carcinoma_nos(note="Evidence fg_cytology option 2 ('Carcinoma, with no type "
                                    "named')."),
            # ICCR-Cx p. 28 "HSIL which is a true premalignant lesion that can progress to SCC".
            nonrep("A squamous or glandular intraepithelial lesion: low-grade or high-grade "
                   "squamous intraepithelial lesion (LSIL, HSIL), atypical squamous or glandular "
                   "cells, or adenocarcinoma in situ",
                   "An intraepithelial lesion on cytology is not an invasive cancer, and it is "
                   "not registered.",
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "cytology_intraepithelial"},
                   note="Evidence fg_cytology option 4 (departure 3: its 'suspicious for "
                        "carcinoma' part is the common suspicious line)."),
            # Evidence fg_cytology option 6. Rules p. 2 (printed p. 15) Rule D.
            refer_lymphoma(WHERE),
        ],
        note="Evidence fg_evidence and fg_cytology (departures 2 and 3 in the module docstring). "
             "No laboratory screen and no marker tier: the evidence names no laboratory test, and "
             "no Visser Table 4 row concerns these sites.")
    # Evidence fg_cytology hint; ICCR-Cx p. 28 "HSIL which is a true premalignant lesion that can
    # progress to SCC".
    for nd in nodes:
        if nd["node_id"] == n("cytology"):
            nd["hint"] += (" A squamous or glandular intraepithelial lesion on a smear is not an "
                           "invasive cancer.")
    return nodes


# ------------------------------------------------------------------------------------------
# Histology (evidence fg_histology, with the referrals of evidence fg_picker)
# ------------------------------------------------------------------------------------------
def _refer_xii(label, reason_codes, *, refer_code=None, note):
    """A referral to Group XII for a tumour ICCC-2017 places in XIIa at every routed site.
    `reason_codes` is the clerk-facing sentence naming each ICD-O-3.2 term and code."""
    return refer(label, 12,
                 "%s ICCC-3 places %s in Group XII (other and unspecified malignant neoplasms) "
                 "at the female genital organs, not in Group XI. Code the case from the Group XII "
                 "tree." % (reason_codes, "that code" if refer_code else "those codes"),
                 refer_code=refer_code, note=note)


def histology():
    opts = [
        # Wohlmuth p. 10 "The second most common histologic subtype was adenocarcinoma" and "15
        # of 16 cases were cervical clear cell cancers"; ICCR-Va p. 13 "Adenocarcinoma of the
        # vagina in adolescence. A report of 7 cases". D1: paediatric common. D14: the evidence's
        # sites are the cervix and vagina; the picker keeps 8310 for the other organs.
        aid(named("Clear cell adenocarcinoma, or clear cell carcinoma (cervix or vagina)", "8310",
                  "ICD-O-3.2 gives Clear cell carcinoma, NOS as a synonym of this code.",
                  note="D1, D14: Wohlmuth 2021 (cervix), ICCR vagina p. 13 (vagina). Evidence "
                       "fg_histology option 1."), AID_CLEAR_CELL),
        # Wohlmuth p. 10 (as above); Wohlmuth p. 12 "We observed a heterogenous group of
        # sarcomas, adenocarcinomas and choriocarcinomas"; ICCR-Cx p. 19 image "Adenocarcinoma
        # NOS 8140/3"; ICCR-Va p. 8 image "Adenocarcinoma NOS 8140/3". D4: ICCR-Cx p. 19 image
        # "Adenocarcinoma, HPV-associated 8483/3*" and "Adenocarcinoma, HPV-independent, NOS
        # 8484/3*", codes ICD-O-3.2 lacks (registrar question 1). Departure 5.
        # Registrar, 9 October 2026 (review E11): "lets remove such cases where ICD -O- 3.2 does not have the code". The option no longer names the HPV-associated and HPV-independent types.
        aid(named("Adenocarcinoma with no type named", "8140",
                  upgrade="A report that names a type with its own code, such as clear cell, "
                          "gastric type, mucinous, intestinal type, signet ring cell, villoglandular "
                          "or endometrioid, gives that code: go back and take it from another "
                          "carcinoma the report names.",
                  note="D1 (cervix and uterus: Wohlmuth 2021), contract §4.2 generic option, D4 "
                       "(8483, 8484), D5. Evidence fg_histology option 3 and fg_picker options "
                       "2, 4 and 23."), AID_ADENO),
        # Wohlmuth p. 11 "Squamous cell cancer and malignant melanoma of the vulva have a poor
        # prognosis"; ICCR-Cx p. 17 "p16 immunostaining and/or HPV testing are generally required
        # to classify SCC of the cervix". D1 exception: the code depends on the HPV status.
        go("Squamous cell carcinoma, of any type: %s-associated or HPV-independent, "
           "keratinising, non-keratinising, basaloid, warty, verrucous, papillary or "
           "microinvasive" % HPV, n("scc"),
           note="D1 exception (the code depends on the HPV status); evidence fg_histology option "
                "4 and fg_picker options 0 and 1 (departure 4)."),
        # Rules p. 6 "C80.9 (unknown primary site) 8010/3 (carcinoma)". Contract §4.2 generic.
        named("Carcinoma with no type named", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence fg_histology option 7; evidence data gap 7 (no paediatric source)."),
    ] + tail_options(
        P, "mucosa", where=WHERE,
        not_malignant_label="An in situ, precancerous or benign lesion with no invasion, such as "
                            "a squamous or glandular intraepithelial lesion, adenocarcinoma in "
                            "situ, atypical hyperplasia of the endometrium or a papilloma",
        referrals=[
            # Wohlmuth p. 9 "Sarcomas (mainly embryonal rhabdomyosarcomas) represent the most
            # common histologic subtype"; p. 10 "The majority of these were embryonal
            # rhabdomyosarcomas"; Pfister p. 8 "Rhabdomyosarcoma family". ICCC-2017: 8900, 8910
            # at every routed site -> IXa.
            refer("Rhabdomyosarcoma, including embryonal rhabdomyosarcoma, botryoid "
                  "rhabdomyosarcoma or sarcoma botryoides", 9,
                  "Rhabdomyosarcoma belongs to ICCC-3 Group IX (soft tissue and other "
                  "extraosseous sarcomas). ICD-O-3.2 codes embryonal rhabdomyosarcoma, sarcoma "
                  "botryoides among its terms, as %s (8910/3). Code the case from the Group IX "
                  "(soft tissue sarcomas) tree." % term("8910", "3"),
                  note="Evidence fg_histology option 0; entity 8910/3 (paediatric common). "
                       "ICCC-2017: 8900 and 8910 at 510-589 -> IXa."),
            # Evidence fg_picker option 38. ICCC-2017: 8890 at every routed site -> IXd6.
            refer_sarcoma(WHERE, label="Another sarcoma, for example leiomyosarcoma"),
            # Wohlmuth p. 9 "Germ-cell (and specifically yolk sac) tumors represent the second
            # most common vaginal histology"; Wohlmuth p. 12 (as above, choriocarcinomas); ICCR-Cx
            # p. 20 image "Yolk sac tumour NOS 9071/3"; Pfister p. 12 "Yolk sac tumor". ICCC-2017:
            # 9071 Xb4, 9100 Xb5, 9064 Xb1 at every routed site.
            refer("Yolk sac tumour (endodermal sinus tumour), choriocarcinoma, or another germ "
                  "cell tumour", 10,
                  "Germ cell tumours belong to ICCC-3 Group X (germ cell tumours, trophoblastic "
                  "tumours and neoplasms of gonads) at the female genital organs. ICD-O-3.2 codes "
                  "yolk sac tumour, endodermal sinus tumour among its terms, as %s (9071/3) and "
                  "choriocarcinoma as %s (9100/3). Code the case from the Group X tree."
                  % (term("9071", "3"), term("9100", "3")),
                  note="Evidence fg_histology option 2; entities 9071/3 (paediatric common) and "
                       "9100/3 (uterus, paediatric occurs); conflicts, Group 10."),
            # ICCR-Cx p. 18 "Carcinosarcoma is also included in the WHO 2020 Classification in
            # the category of epithelial neoplasms". ICCC-2017: 8980 and 8950 -> XIIa4.
            _refer_xii("Carcinosarcoma, or malignant mixed Müllerian tumour",
                       "ICD-O-3.2 codes carcinosarcoma as %s (8980/3) and malignant mixed "
                       "Müllerian tumour as %s (8950/3)." % (term("8980", "3"),
                                                             term("8950", "3")),
                       note="Evidence fg_picker option 33; conflicts, Group 12; registrar "
                            "question 8."),
            # ICCR-Cx p. 20 image "Adenosarcoma 8933/3". ICCC-2017: 8933 -> XIIa4.
            _refer_xii("Adenosarcoma", "ICD-O-3.2 codes it as %s (8933/3)." % term("8933", "3"),
                       refer_code="8933",
                       note="Evidence fg_picker option 35; conflicts, Group 12."),
            # ICCR-En p. 5 "neoplasms, mesenchymal neoplasms, adenosarcomas, malignant melanomas,
            # other non-epithelial". ICCC-2017: 8930, 8931 -> XIIa4 (departure 7).
            _refer_xii("Endometrial stromal sarcoma, low grade or high grade",
                       "ICD-O-3.2 codes it as %s (8930/3), or as %s (8931/3) when the report "
                       "calls it low grade." % (term("8930", "3"), term("8931", "3")),
                       note="Evidence fg_picker option 37; conflicts, Group 12."),
            # ICCR-Cx p. 19 image "Adenocarcinoma, HPV-independent, mesonephric type 9110/3".
            # ICCC-2017: 9110 -> XIIa6.
            aid(_refer_xii("Mesonephric adenocarcinoma, or Gartner duct carcinoma",
                           "ICD-O-3.2 codes it as %s (9110/3), and gives Mesonephric "
                           "adenocarcinoma as a synonym." % term("9110", "3"),
                           refer_code="9110",
                           note="Evidence fg_picker option 34; conflicts, Group 12; registrar "
                                "question 8."), AID_MESONEPHRIC),
            # ICCR-Vu p. 11 image "Myoepithelial carcinoma 8982/3". ICCC-2017: 8982 -> XIIa4.
            _refer_xii("Myoepithelial carcinoma",
                       "ICD-O-3.2 codes it as %s (8982/3)." % term("8982", "3"),
                       refer_code="8982",
                       note="Evidence fg_picker option 36 (vulva, Bartholin gland); conflicts, "
                            "Group 12."),
            # ICCR-Vu p. 6 "Haematopoietic neoplasms, mesenchymal neoplasms, mixed epithelial and
            # mesenchymal neoplasms,". Rules p. 2 (printed p. 15) Rule D.
            refer_lymphoma(WHERE),
            refer_leukaemia(WHERE),
            refer_other_named(),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence fg_histology hint: Rules p. 2 "ascertain that the neoplasm at the site
        # mentioned is not a metastasis"; ICCR-Va p. 7 "a metastasis from elsewhere should always
        # be excluded". Departures 4 to 6.
        "Use the report's final diagnosis. If the report says the tumour began in another organ, "
        "it is a deposit: choose the deposit line. An option that names an organ in brackets "
        "belongs to that organ: take it only when the site recorded is that organ. Gastric-type, "
        "endometrioid, serous, mucinous, intestinal-type and the other named carcinomas are "
        "under another carcinoma the report names; an adenocarcinoma called HPV-associated or "
        "HPV-independent that also names one of those types takes that type (WHO coding Rule "
        "K). An adenocarcinoma the report calls mesonephric-like is not a mesonephric "
        "adenocarcinoma: ICD-O-3.2 has no code for it, so take adenocarcinoma with no type "
        "named.",
        opts, [],
        "Evidence fg_histology, with fg_picker's referral lines (departures 4 to 8). D1: clear "
        "cell adenocarcinoma at the cervix and vagina, adenocarcinoma at the cervix and uterus and "
        "squamous cell carcinoma at the vulva (Wohlmuth 2021, SEER-18, ages 0 to 18). D4: 8483, "
        "8484 and 9113 are not built; registrar questions 1 and 2. D5: departure 5.")


def scc():
    return node(
        n("scc"), "histology_subclassification", 4, "Squamous cell carcinoma",
        "How does the report describe the squamous cell carcinoma?",
        # Evidence fg_scc hint: Rules p. 3 "When no single code includes all diagnostic terms,
        # use the numerically higher code number"; ICCR-Cx p. 13 "the term superficially
        # invasive squamous cell carcinoma (SISCCA) is used to describe FIGO Stage 1A1".
        # Departure 9: the lines run from the higher code to the lower.
        "Choose the first line that matches the report. The %s status comes first: it carries "
        "a higher code than any growth pattern. When the report names two growth patterns, the "
        "first line that matches has the higher code (WHO coding Rule K). A microinvasive or "
        "superficially invasive carcinoma is invasive and is recorded here." % HPV,
        [
            # ICCR-Cx p. 19 image "Squamous cell carcinoma, HPV-associated 8085/3"; ICCR-Vu p. 16
            # "p16 staining should not be reported simply as positive".
            aid(named("Human papillomavirus (HPV)-associated, or HPV positive", "8085",
                      "ICD-O-3.2 names the HPV-associated squamous cell carcinoma HPV positive.",
                      note="D5; evidence fg_scc option 0. Currency check §6: new in ICD-O-3.2, "
                           "absent from REDCap (the REDCap-side list)."), AID_HPV_ASSOCIATED),
            # ICCR-Cx p. 19 image "Squamous cell carcinoma, HPV-independent 8086/3"; ICCR-Vu p. 10
            # "Verrucous carcinoma falls under the umbrella of HPV-independent SCC".
            (named("HPV-independent, or HPV negative, including a verrucous carcinoma the "
                      "report calls HPV-independent", "8086",
                      "ICD-O-3.2 names the HPV-independent squamous cell carcinoma HPV negative.",
                      note="D5; evidence fg_scc option 1. Currency check §6: new in ICD-O-3.2, "
                           "absent from REDCap.")),
            # ICCR-Vu p. 16 "p16 immunohistochemistry and/or HPV testing is considered a core
            # element in cases of vulval SCC". Registrar question 6.
            go("No HPV status in the diagnosis, and the report gives a p16 or HPV test result",
               n("scc_hpv"), note="Evidence fg_scc option 2; registrar question 6."),
            # ICCR-Cx p. 17 "(e.g., papillary, basaloid, warty, verrucous, etc.) are no longer the
            # basis for subclassification".
            named("Basaloid squamous cell carcinoma, with no HPV status or test result", "8083",
                  note="Evidence fg_scc option 5."),
            # ICCR-Cx p. 13 "Avoid the term 'microinvasive carcinoma'".
            named("Microinvasive or superficially invasive squamous cell carcinoma, with no HPV "
                  "status or test result", "8076", note="Evidence fg_scc option 9."),
            # ICCR-Vu p. 10 "using terms such as keratinising, non-keratinising, basaloid and
            # warty, has been".
            named("Non-keratinising squamous cell carcinoma, with no HPV status or test result",
                  "8072",
                  "ICD-O-3.2 gives Squamous cell carcinoma, nonkeratinizing, NOS as a synonym of "
                  "this code.", note="Evidence fg_scc option 4."),
            # ICCR-Vu p. 10 (as above).
            named("Keratinising squamous cell carcinoma, with no HPV status or test result",
                  "8071", note="Evidence fg_scc option 3."),
            # ICCR-Cx p. 17 (as above).
            named("Warty (condylomatous) carcinoma, with no HPV status or test result", "8054",
                  "ICD-O-3.2 gives Condylomatous carcinoma as a synonym of this code.",
                  note="Evidence fg_scc option 6. Currency check §6: new in ICD-O-3.2, absent "
                       "from REDCap."),
            # ICCR-Cx p. 17 (as above).
            named("Papillary squamous cell carcinoma, with no HPV status or test result", "8052",
                  note="Evidence fg_scc option 8."),
            # Hohn p. 4 "It is unclear why verrucous carcinoma".
            named("Verrucous carcinoma, with no HPV status or test result", "8051",
                  note="Evidence fg_scc option 7."),
            # ICCR-Cx p. 17 "a diagnosis of SCC not otherwise specified (NOS), without
            # differentiating the two categories".
            named("Squamous cell carcinoma, with no HPV status, test result or growth pattern",
                  "8070",
                  upgrade="The report states no HPV status and no growth pattern. A report that "
                          "states either may give a more specific code: go back and take the "
                          "line that names it.",
                  note="Evidence fg_scc option 10."),
        ], [],
        "Evidence fg_scc (departure 9). D1 exception: the code depends on the HPV status, so "
        "squamous cell carcinoma is an option at every routed site. D5: Rule K, Rules p. 3 "
        "(printed p. 16).")


def scc_hpv():
    return node(
        n("scc_hpv"), "histology_subclassification", 5, "p16 and HPV results",
        "Which p16 or %s result does the report give for the squamous cell carcinoma?" % HPV,
        # Evidence fg_scc_hpv hint: ICCR-Cx p. 29 "which is not in keeping with a high risk
        # HPV-associated neoplasm"; ICCR-Vu p. 16 "p16 staining should not be reported simply as
        # positive".
        "Choose the first answer that matches the report. Read each result as the report words "
        "it. Only block-type (diffuse and strong) p16 staining counts as positive; patchy or "
        "mosaic staining counts as negative.",
        [
            # Evidence ihc_rules 1: ICCR-Cx p. 29 "Diffuse immunoreactivity (nuclear and
            # cytoplasmic) for p16 is a surrogate marker of integrated high risk"; Hohn p. 5 image
            # "p16 block staining (Darragh et al. 2013) [12]".
            named("Block-type p16 staining (diffuse and strong)", "8085",
                  "Block-type p16 staining marks the carcinoma as HPV-associated.",
                  note="Evidence ihc_rules 1 (departure 10)."),
            # Evidence ihc_rules 2: ICCR-Vu p. 16 "the two accepted tools for confirming an
            # HPV-association are the direct identification of HPV".
            named("High-risk %s detected by in situ hybridisation or polymerase chain reaction"
                  % HPV, "8085",
                  "A high-risk HPV detected in the tumour marks the carcinoma as HPV-associated.",
                  note="Evidence ihc_rules 2 (departure 10). Basis 7: the evidence gives no "
                       "basis for the panel, and D15's basis 8 is a gene test specific to the "
                       "entity."),
            # Evidence ihc_rules 3: Hohn p. 5 image "p16-negative (non-block staining)"; ICCR-Cx
            # p. 29 "which is not in keeping with a high risk HPV-associated neoplasm".
            named("p16 staining negative, patchy or mosaic (not block-type)", "8086",
                  "p16 staining that is not block-type marks the carcinoma as HPV-independent.",
                  note="Evidence ihc_rules 3 (departure 10)."),
            # Evidence ihc_rules 4: ICCR-Vu p. 16 (as above).
            named("A high-risk HPV test done, and no high-risk HPV detected", "8086",
                  "A high-risk HPV test that detects no high-risk HPV marks the carcinoma as "
                  "HPV-independent.",
                  note="Evidence ihc_rules 4 (departure 10)."),
            # Evidence ihc_rules 5: ICCR-Vu p. 17 "while many, but importantly not all,
            # HPV-independent SCC and precursor lesions exhibit"; ICCR-Va p. 12 "many
            # HPV-independent vaginal SCC contain".
            named("Mutation-type (aberrant) p53 staining, with no p16 result and no HPV test",
                  "8086",
                  "Mutation-type p53 staining marks the carcinoma as HPV-independent when no p16 "
                  "or HPV result is given. This awaits the registrar's decision.",
                  note="Evidence ihc_rules 5 (departure 10): 'Reached only when p16 and HPV were "
                       "not done'. Registrar question 6."),
            # Evidence nos_fallback: ICCR-Cx p. 17 "a diagnosis of SCC not otherwise specified
            # (NOS), without differentiating the two categories".
            named("None of these, for example wild-type p53 staining only, or a result the "
                  "report does not interpret", "8070",
                  "The WHO accepts squamous cell carcinoma, NOS when the p16 or HPV status is not "
                  "known.",
                  upgrade="The report gives no p16 or HPV result that decides the HPV status. A "
                          "report that gives one may give a more specific code.",
                  note="Evidence fg_scc_hpv nos_fallback (departure 10)."),
        ], [],
        "Evidence fg_scc_hpv and ihc_rules 1-5, built as a choice in the evidence's rule order "
        "(departure 10): app.js meets a `negative` requirement with an unrecorded marker, so "
        "rules 3 and 4 would fire on a report with no result. Registrar question 6.")


# ------------------------------------------------------------------------------------------
# Exclusions (evidence fg_not_invasive, and the benign line of fg_histology)
# ------------------------------------------------------------------------------------------
def not_malignant():
    nm = not_malignant_node(
        P,
        [
            # Registrar, 8 October 2026 (review A6, E7): Rule F (ICD-O-3.1 printed p. 15). ICCR
            # Vulva, PDF p. 11. ICD-O-3.2 prints 8542 at /3 only; the name does not change with
            # the behaviour (build_database.ICDO32_MATRIX_RULE). Invasive Paget disease keeps
            # 8542/3 from the picker.
            excl("Extramammary Paget disease that the report calls in situ, intraepithelial or "
                 "confined to the epithelium", "8542", "2",
                 what="an extramammary Paget disease the report calls in situ",
                 extra="The pathologist's stated behaviour is recorded (WHO coding Rule F).",
                 note="Registrar, 8 October 2026 (review A6, E7): Rule F; matrix-rule pair."),
            # ICCR-Cx p. 19 image "High grade squamous intraepithelial lesion 8077/2"; Rules p. 7
            # "could be considered as comparable to carcinoma in situ whether severe dysplasia is
            # mentioned".
            excl("High-grade squamous intraepithelial lesion (HSIL), cervical intraepithelial "
                 "neoplasia (CIN) 2 or 3, vulvar intraepithelial neoplasia (VIN) 2 or 3 of usual "
                 "type, or vaginal intraepithelial neoplasia (VaIN) 2 or 3", "8077", "2",
                 what="a high-grade squamous intraepithelial lesion",
                 extra="ICD-O-3.2 gives High grade squamous intraepithelial lesion as a synonym, "
                       "and cervical, vaginal and vulvar intraepithelial neoplasia grade III as "
                       "related terms, of this code.",
                 note="Evidence fg_not_invasive option 0."),
            # ICCR-Cx p. 19 image "Low grade squamous intraepithelial lesion 8077/0".
            excl("Low-grade squamous intraepithelial lesion (LSIL), cervical intraepithelial "
                 "neoplasia (CIN) 1, or vulvar intraepithelial neoplasia (VIN) 1", "8077", "0",
                 what="a low-grade squamous intraepithelial lesion",
                 extra="ICD-O-3.2 gives Low grade squamous intraepithelial lesion as a synonym of "
                       "this code.",
                 note="Evidence fg_not_invasive option 1."),
            # Hohn p. 2 "The differentiated VIN with its horizontal spread (d-VIN) is a".
            excl("Differentiated vulvar intraepithelial neoplasia (differentiated VIN), or "
                 "HPV-independent vulvar intraepithelial neoplasia", "8071", "2",
                 what="a differentiated vulvar intraepithelial neoplasia",
                 extra="ICD-O-3.2 gives Differentiated vulvar intraepithelial neoplasia (VIN) as "
                       "a related term of this code.",
                 note="Evidence fg_not_invasive option 2."),
            # Hohn p. 2 "the differentiated exophytic VIN lesion (DEVIL) to a less ag"; "vulvar
            # acanthosis with altered differentiation (VAAD) is allo".
            nonrep("Differentiated exophytic vulvar intraepithelial lesion (DEVIL), or vulvar "
                   "acanthosis with altered differentiation (VAAD)",
                   "ICD-O-3.2 gives this HPV-independent precursor lesion no code, and it is not "
                   "registered.", note="Evidence fg_not_invasive option 3."),
            # ICCR-Cx p. 19 image "Adenocarcinoma in situ NOS 8140/2"; ICCR-Cx p. 28 "SMILE is a
            # variant of AIS (and should be coded as such)". D4: 8483/2 and 8484/2 not built.
            excl("Adenocarcinoma in situ (AIS), HPV-associated or HPV-independent (gastric type), "
                 "including stratified mucin-producing intraepithelial lesion (SMILE)",
                 "8140", "2", what="an adenocarcinoma in situ",
                 extra="ICD-O-3.2 has no separate code for the HPV-associated or HPV-independent "
                       "form.",
                 note="Evidence fg_not_invasive option 4; code currency 8483/2 (D4)."),
            # ICCR-Cx p. 28 "High grade cervical glandular intraepithelial neoplasia (HG CGIN) is
            # an alternative terminology".
            excl("High-grade cervical glandular intraepithelial neoplasia (HG CGIN)", "8148", "2",
                 what="a high-grade glandular intraepithelial neoplasia",
                 note="Evidence fg_not_invasive option 5."),
            # ICCR-En p. 9 image "Atypical hyperplasia of the endometrium 8380/2".
            excl("Atypical hyperplasia of the endometrium, or endometrioid intraepithelial "
                 "neoplasia", "8380", "2", what="atypical hyperplasia of the endometrium",
                 extra="ICD-O-3.2 gives Atypical hyperplasia of endometrium as a synonym of this "
                       "code.",
                 note="Evidence fg_not_invasive option 6."),
            # ICCR-En p. 9 image "Endometrial hyperplasia without atypia".
            nonrep("Endometrial hyperplasia without atypia",
                   "ICD-O-3.2 gives endometrial hyperplasia without atypia no code: it is a "
                   "benign change, and it is not registered.",
                   note="Evidence fg_not_invasive option 7."),
            # ICCR-Cx p. 20 image "Adenomyoma 8932/0".
            excl("Adenomyoma", "8932", "0", what="an adenomyoma",
                 note="Evidence fg_not_invasive option 8."),
            # ICCR-Cx p. 20 image "Mature teratoma NOS 9080/0". Departure 11.
            excl("Mature teratoma", "9080", "0", what="a mature teratoma",
                 extra="ICD-O-3.2 gives Mature teratoma, NOS as a synonym of this code. An "
                       "immature or malignant teratoma is a germ cell tumour, coded in ICCC-3 "
                       "Group X.",
                 note="Evidence fg_not_invasive option 9; conflicts, Group 10."),
            # ICCR-Cx p. 20 image "Dermoid cyst NOS 9084/0".
            excl("Dermoid cyst", "9084", "0", what="a dermoid cyst",
                 note="Evidence fg_not_invasive option 10; conflicts, Group 10."),
            # Pfister p. 13 "Mullerian papilloma", "Condyloma acuminatum", "Mesonephric remnants
            # and hyperplasia". Evidence fg_histology option 11 (departure 11).
            nonrep("A benign lesion: Müllerian papilloma, condyloma acuminatum (genital wart), or "
                   "mesonephric remnants or hyperplasia",
                   "The report describes a benign lesion. ICD-O-3.2 gives it no code, and it is "
                   "not registered.",
                   note="Evidence fg_histology option 11; Pfister 2022 Table 3, p. 13."),
        ],
        where=WHERE,
        note="Evidence fg_not_invasive, with fg_histology's benign line (departure 11).")
    # Evidence fg_not_invasive hint (Rule F): Rules p. 6 "By far the largest number of in situ
    # carcinomas are diagnosed in the cervix uteri".
    nm["hint"] += (" If the same report also names an invasive carcinoma, go back and choose the "
                   "carcinoma.")
    return nm


# ------------------------------------------------------------------------------------------
# The deposit question (D10; evidence fg_deposit)
# ------------------------------------------------------------------------------------------
def deposit():
    nd = deposit_node(P, where=WHERE)
    # Evidence fg_deposit option 1, verified by contract §0.1 item 3: carcinomas of the ovary
    # (C56) are Group X. Departure 12: inserted first, ahead of DEPOSIT_PRIMARIES.
    ovary = refer("A tumour of the ovary, an ovarian carcinoma included", 10,
                  "Tumours of the ovary, ovarian carcinomas among them, are coded in ICCC-3 Group "
                  "X (germ cell tumours, trophoblastic tumours and neoplasms of gonads) at the "
                  "ovary (C56.9), not in Group XI. Code the case at its primary.",
                  recapture=True,
                  note="Evidence fg_deposit option 1; D10. ICCC-2017 places carcinomas of C56.9 "
                       "in Group X (contract §0.1 item 3).")
    assert len(nd["options"]) > len(DEPOSIT_PRIMARIES)
    nd["options"].insert(0, ovary)
    # Evidence fg_deposit hint: ICCR-Va p. 5 "is usually taken as evidence for exclusion of a
    # primary vaginal SCC"; Rules p. 2 "ascertain that the neoplasm at the site mentioned is not a
    # metastasis".
    nd["hint"] += (" A carcinoma of the vagina in a patient who has or had a carcinoma of the "
                   "cervix is taken as the cervical carcinoma's spread unless the report states "
                   "otherwise.")
    return nd


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
# Evidence fg_picker hint: Rules p. 2 "Assign the highest grade or differentiation code described
# in the diagnostic statement" (Rule G); Rules p. 10 "topography code should be disregarded if the
# tumor is known to arise at another site" (Rule H). Departure 13.
PICKER_HINT_EXTRA = (" When the report gives a neuroendocrine tumour two grades, choose the higher "
                     "grade (WHO coding Rule G). A carcinoma type that usually begins in another "
                     "organ, such as intestinal-type adenocarcinoma, adenocarcinoma of "
                     "mammary-like glands or Merkel cell carcinoma, is recorded here only when "
                     "the report says it began here (WHO coding Rule H).")
# Registrar ruling of 8 October 2026 on review A1 (a)(b), docs/group_11_evidence/
# registrar_A1ab_rules.md C7 (a9): ICD-O-3.2 prints C53._ beside 8482/3 and the report names the
# uterine corpus, so the cervical topography gives way and the morphology code is kept (ICD-O-3.1
# Rule H, pp. 15 and 23; Rule K, p. 24, gives the same code for the ICCR wording "gastric
# (gastrointestinal)-type", 8482 being higher than 8144). 8144/3 stays the code of a report that
# says intestinal type.
PICKER_HINT_CORPUS = (" %s (8482/3) prints the cervix beside it. When the report places it in the "
                      "uterine corpus, record 8482/3 at the corpus, not %s (8144/3)."
                      % (term("8482", "3"), term("8144", "3")))


def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), scc(), scc_hpv(), not_malignant(), deposit()]
    tree = make_tree(
        TREE_ID, nodes,
        subtype_screens=(n("scc"), n("scc_hpv")),
        # Standing rule 3 (D11): no ICCC-2017 range of any group holds these at C51.0-C51.8 or at
        # any other routed site, and the evidence names them at the vulva: ICCR-Vu p. 11 image
        # "Basal cell carcinoma NOS 8090/3", "Sweat gland adenocarcinoma 8400/3", "Porocarcinoma
        # NOS 8409/3", "Eccrine adenocarcinoma 8413/3". Evidence registrar question 5.
        d11=("8090", "8400", "8409", "8413"),
        # Departures 4 and 13: 8310 for the corpus and other organs (the screen's option names
        # the cervix and vagina); 8140 so that its related term, Carcinoma of Skene, Cowper and
        # Littre glands (ICCR-Va p. 8 image), is found in the picker.
        picker_keep=("8310", "8140"))
    for nd in tree["nodes"]:
        if nd["node_id"] == n("picker"):
            nd["hint"] += PICKER_HINT_EXTRA + PICKER_HINT_CORPUS
    return tree


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8310/3": ("D1, D2, D14", EVIDENCE,
               "Clear cell adenocarcinoma of the cervix or vagina on the female genital histology "
               "screen (Wohlmuth 2021: 15 of 16 cervical adenocarcinomas at ages 0 to 18; ICCR "
               "vagina dataset, p. 13), and in the female genital picker for the corpus and the "
               "other organs."),
    "8140/3": ("D1, D2, D4, D5, D8", EVIDENCE,
               "Adenocarcinoma with no type named on the female genital histology screen "
               "(Wohlmuth 2021: cervix and uterus at ages 0 to 18), including an adenocarcinoma "
               "called HPV-associated or HPV-independent with no other type (8483 and 8484 are "
               "not ICD-O-3.2 codes; registrar question 1) and a mesonephric-like adenocarcinoma "
               "(9113 is not an ICD-O-3.2 code; registrar question 2); at basis 5 when cytology "
               "names an adenocarcinoma; in the picker for Carcinoma of Skene, Cowper and Littre "
               "glands."),
    "8010/3": ("D4, D8", EVIDENCE,
               "Carcinoma whose type the report does not name, at basis 7 on the female genital "
               "histology screen and at basis 5 when cytology names a carcinoma without its "
               "type."),
    "8070/3": ("D1, D5, D8", EVIDENCE,
               "Squamous cell carcinoma with no human papillomavirus status, test result or "
               "growth pattern on the squamous cell carcinoma screen and as the last answer of "
               "the p16 and HPV screen; at basis 5 when cytology names a squamous cell "
               "carcinoma."),
    "8085/3": ("D1, D5", EVIDENCE,
               "Squamous cell carcinoma, HPV positive, for a report that calls it HPV-associated "
               "or HPV positive, or (registrar question 6) gives block-type p16 staining or a "
               "detected high-risk HPV. New in ICD-O-3.2 and absent from REDCap: the REDCap-side "
               "list (standing rule 16)."),
    "8086/3": ("D1, D5", EVIDENCE,
               "Squamous cell carcinoma, HPV negative, for a report that calls it HPV-independent "
               "or HPV negative, or (registrar question 6) gives non-block p16 staining, no "
               "high-risk HPV detected, or mutation-type p53 staining with no p16 or HPV result. "
               "New in ICD-O-3.2 and absent from REDCap: the REDCap-side list."),
    "8083/3": ("D1, D5", EVIDENCE,
               "Basaloid squamous cell carcinoma with no HPV status, on the squamous cell "
               "carcinoma screen."),
    "8076/3": ("D1, D5", EVIDENCE,
               "Microinvasive or superficially invasive squamous cell carcinoma with no HPV "
               "status, on the squamous cell carcinoma screen."),
    "8072/3": ("D1, D5", EVIDENCE,
               "Non-keratinising squamous cell carcinoma with no HPV status, on the squamous cell "
               "carcinoma screen; ICD-O-3.2 holds Squamous cell carcinoma, nonkeratinizing, NOS "
               "as a synonym."),
    "8071/3": ("D1, D5", EVIDENCE,
               "Keratinising squamous cell carcinoma with no HPV status, on the squamous cell "
               "carcinoma screen."),
    "8054/3": ("D1, D5", EVIDENCE,
               "Warty (condylomatous) carcinoma with no HPV status, on the squamous cell carcinoma "
               "screen. New in ICD-O-3.2 and absent from REDCap: the REDCap-side list."),
    "8052/3": ("D1, D5", EVIDENCE,
               "Papillary squamous cell carcinoma with no HPV status, on the squamous cell "
               "carcinoma screen."),
    "8051/3": ("D1, D5", EVIDENCE,
               "Verrucous carcinoma with no HPV status, on the squamous cell carcinoma screen; a "
               "verrucous carcinoma called HPV-independent records 8086/3."),
}
