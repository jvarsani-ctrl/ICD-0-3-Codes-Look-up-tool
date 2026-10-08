"""g11_melanoma (prefix me_): malignant melanomas at every site, ICCC-3 subgroup XId.

Built from docs/group_11_evidence/XId_melanoma.json (the evidence agent's nodes mel_evidence,
mel_clinical, mel_cytology, mel_site, mel_skin_histology, mel_conjunctiva, mel_eye, mel_mucosa,
mel_cns, mel_picker) with the builders in build/group11_common.py, in the shape of
build/group11_organs/thyroid.py. Every option's label, code, behaviour, basis, reason and
recognition aid comes from that file; the cite (file, PDF page, quotation) is the comment above
the option or the aid. File names in the comments are the evidence's own:
    ICCR         XId-melanoma__ICCR-Invasive-Melanoma-3rd.txt (ICCR Invasive Melanoma
                 Histopathology Reporting Guide, 3rd edition, version 3.0, January 2026; its
                 Table 1, PDF p. 8, reproduces the WHO Classification of Skin Tumours, 5th edition)
    GoldmanLevy  XId-XIe-skin-melanoma-and-skin-carcinoma__Goldman-Levy-2025.txt (Histopathology
                 2026;88:555-568)
    Sargen       XId-melanoma-paediatric__Sargen-2026.txt (Int J Dermatol 2026;65 Suppl 1:S67-S74)
    Ferrari      XId-melanoma-paediatric__Ferrari-2021.txt (Pediatr Blood Cancer 2021;68 Suppl
                 4:e28992)
    Milman       XIf9-eye-XId-ocular-melanoma__Milman-2023.txt (Ocul Oncol Pathol 2023;9:71-95)
    Pfister      ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules        RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4; PDF page 1 = printed
                 p. 14)
    icdo32       ICD coding/ICD-O-3.2/icdo32.sqlite, read by the builders

ICCC-2017 range 123 places 8720-8780 and 8790 (behaviour 3) in XId at topography 000-809, so
every code this tree records is XId at whatever site the case carries. No routing rule names
this tree (design D13). Every other tree's histology screen hops into one of its screens by a
cross-tree next_node, and the entry node exists because the router lists every tree. The
screens other trees enter are:
    me_skin_histology  melanoma of the skin, the Spitz spectrum among it
    me_eye             conjunctival and intraocular (uveal) melanoma, the orbit, the lacrimal
                       drainage system
    me_mucosa          mucosal melanoma
    me_cns             meningeal and primary central nervous system melanocytic tumours
    me_other           a melanoma found in an internal organ that is none of the above

Nodes, in tree order:
    me_document_inventory  document_inventory   evidence gate (evidence mel_evidence)
    me_clinical, me_clinical_cytology  clinical_alias  (evidence mel_clinical)
    me_imaging, me_imaging_cytology    morphology_only
    me_cytology            morphology_only      (evidence mel_cytology)
    me_histology           site_resolution      (evidence mel_site)
    me_skin_histology      histology_subclassification  (evidence mel_skin_histology)
    me_not_malignant       histology_subclassification  (the skin exclusions of mel_skin_histology)
    me_eye                 histology_subclassification  (evidence mel_conjunctiva and mel_eye)
    me_mucosa              histology_subclassification  (evidence mel_mucosa)
    me_cns                 histology_subclassification  (evidence mel_cns)
    me_other               histology_subclassification  (no evidence node; departure 10)
    me_deposit             morphology_only      (D10; the deposit options of mel_site)
    me_picker              histology_subclassification  (D2; evidence mel_picker)

Departures from the evidence nodes, and why
-------------------------------------------
1. mel_evidence: the imaging tier coded 8000/3 at basis 2 on the gate itself. D7: it routes to
   me_imaging, which refers the case to Group XII with refer_code 8000. The option "An
   immunohistochemistry or gene report only, with no histology report" (not registrable) is not
   built: the document checklist puts IHC or gene reports with no histology report in the
   referral tier (group11_common TIER_RATIONALE), and the gate hint carries the evidence's point
   (Sargen, PDF p. 5). The hint drops "Choose the strongest evidence in the file", which the
   checklist replaces. The tiers are the contract §4.2 tiers; there are no laboratory tests
   (evidence lab_tests is empty) and no marker codes (Visser Table 4 has no melanoma row).
2. mel_clinical: the skin option (8720/3 at basis 1, Visser 2023 Table 3) is not built here, and
   since 8 October 2026 not on the skin tree either: the registrar ruled for the paediatric source
   (review A8, E9; Ferrari 2021, PDF p. 3, excisional biopsy required).
   Every clinical-note route here is the common one: a malignant tumour stated as the diagnosis
   or as probable refers to Group XII with refer_code 8000; possible is not registrable. The tree
   routes no site, so the gate is told the sites where ICCC-2017 places 8000/3 in XIIb (WHERE_NO_TISSUE).
   At C70-C72 ICCC-2017 places 8000/3 in IIIf, and at C22 in VII; no routing rule brings a case to
   this gate, so its Group XII line is never reached at those sites (registrar question 8).
3. mel_cytology: "Melanoma ... in a sample from the primary tumour" and "Melanoma in a deposit, and
   the report states no primary melanoma was found" record 8720/3 at basis 5 (cyto(), D8); the
   second also sets C80.9. "Suspicious for melanoma, or melanoma not excluded" is kept beside the
   common suspicious line. "Melanoma in a lymph node or another deposit, and the primary melanoma
   is known" (refer_group 11 with recapture_site) is built only when group11_common.SELF_REFERRAL
   is True: build_database.check_refer_terminals fails a referral to the file's own group. Until
   then the screen's hint sends the clerk back to the site step, as deposit_node() does.
4. mel_site -> me_histology. Its conjunctiva option and its option for the inside of the eye, the
   orbit and the lacrimal drainage system are one option to me_eye (D14: the router's site step
   already names the part of the eye; mel_conjunctiva and mel_eye are merged, departure 6). Its two
   deposit options (refer_group 11 with recapture_site; 8720/3 at C80.9) become one option to
   me_deposit, which every screen shares (merged duplicates). A new option sends a melanoma of
   another internal organ to me_other (departure 10). The node keeps site_resolution; it captures
   no topography, because each screen records the site the case carries.
5. mel_skin_histology:
   a. "Melanoma arising in a blue naevus" records 8720/3, not 8780/3. D3: ICD-O-3.2 marks the
      Preferred term of 8780/3 [obs] (its synonym Melanoma arising in blue nevus is current), and
      such a code is held off every screen for the registrar. The reason says so, and the registrar
      review carries it.
   b. The hint drops "Record the behaviour the pathologist states" (Rule F). D6: a stated
      behaviour is not built where ICD-O-3.2 prints the term below /3. The hint sends a tumour
      called intermediate, uncertain, in situ or benign to the exclusion screen instead.
   c. The six exclusions (melanoma in situ, Spitz melanocytoma, MELTUMP, pigmented epithelioid
      melanocytoma, proliferative nodule, the naevi) move to me_not_malignant, reached by the
      standard option (contract §4.2), as the thyroid's moved to th_not_malignant.
   d. The naevus line is split. Spitz naevus, Reed naevus and juvenile melanoma are the exclusion
      8770/0: icdo32 gives Juvenile melanoma as a synonym of Epithelioid and spindle cell nevus
      (8770/0), so a report using that name would otherwise read as a melanoma (standing rule 8).
      The other naevi stay a non-reportable line, whose reason names Giant pigmented nevus, NOS
      (8761/1) for the giant congenital naevus.
   e. Spitz melanocytoma (ICCR prints 8770/1, which ICD-O-3.2 lacks: D4) and the CRTC1::TRIM11,
      MED15::ATF1 and dermal clear cell tumours (no code: registrar question 9) are
      non-reportable lines with no ICD-O-3.2 term; the last says the registrar's decision is
      pending.
   f. A deposit option (to me_deposit) is added. The evidence held the deposit on mel_site, which a
      cross-tree hop from the skin tree skips.
6. mel_conjunctiva and mel_eye -> me_eye (D14; the clerk reaches the screen from the eye tree at
   any C69 site). The evidence's picker entries for uveal, orbital and lacrimal melanoma code
   8720/3, the code the screen offers, so they are screen options: the picker's 8720/3 line
   carries the Preferred term, whose search terms hold none of those names. The uveal cell types
   (8770, 8771, 8772, 8773, 8774) stay in the picker. "Uveal naevus, uveal melanocytoma, or
   melanocytoma of the optic disc" (8726/0) is split: 8726/0 is Magnocellular nevus, whose
   synonym is Melanocytoma, eyeball, and no source maps a uveal naevus to it, so the naevus is a
   non-reportable line naming no code. The conjunctival naevus exclusion keeps 8720/0 and its
   reason names Blue nevus, NOS (8780/0) for a blue naevus of the conjunctiva, which the label
   lists. A deposit option (to me_deposit) is added.
7. mel_mucosa: "Mucosal melanoma" moves from the picker to the screen (ICCR, PDF p. 8, codes it
   8720/3), as its own option, so only the "no type stated" option carries an upgrade line. A
   deposit option is added, and the hint asks the clerk to check the report does not call the
   melanoma a deposit (Rule H): the thyroid, adrenal, salivary, nasopharynx, colorectal, lung,
   thymus, thoracic and digestive trees hop here for every non-cutaneous, non-ocular melanoma
   while group11_common.MELANOMA_ENTRY has no "other" kind.
8. mel_cns: "Melanoma that spread to the brain or meninges from a primary elsewhere" (refer_group
   11 with recapture_site) goes to me_deposit. Meningeal melanocytoma (8728/1) and meningeal
   melanocytosis (8728/0) are exclusions with the registrar's decision pending (question 7).
9. me_deposit (D10 for a melanoma; mel_site options 6 and 7): the unknown-primary line records
   8720/3 at basis 7, not 6. D15 lists no basis 6 and code() refuses it; registrar question 5
   asks whether a melanoma known only from a deposit takes basis 6 (histology of a metastasis,
   Rules PDF p. 14, printed p. 27). The primary-known referral is built only when SELF_REFERRAL
   is True (departure 3); until then the hint sends the clerk back to the site step.
10. me_other is not an evidence node. The controller's brief (D13) asks for it: a melanoma found
   in an internal organ that is not skin, eye, mucosa or meninges. It asks whether the report
   calls the melanoma primary in that organ; a primary records 8720/3 or a named type from the
   picker, and anything else goes to me_deposit. No histology screen reaches it until
   MELANOMA_ENTRY names it (request in the build report).
11. mel_picker -> me_picker, computed here rather than by make_tree(). make_tree()'s picker_node()
   takes the codes ICCC-2017 places in Group XI at the tree's routed sites less the XId codes, and
   this tree routes no site, so picker_node() raises. This module builds the same shape (D2):
   every (code, 3) ICCC-2017 places in XId, labelled with its Preferred term, with the live
   synonyms and related terms as search_terms and prefill_filter_from_search, less 8780/3 (D3).
   It keeps the codes the screens offer (make_tree's picker_keep): the picker serves five
   screens, and each screen offers 8720/3, 8770/3, 8743/3, 8761/3 or 8728/3 under a site's own
   label only. The evidence's picker labels and aids are not shown (Group 10's picker shape); its
   hint (Rules H and K, spindle cell melanoma type A and B) is kept.
12. The tree is assembled by _assemble(), which repeats make_tree()'s checks (prefix, unique node
   ids) and output shape, for the reason in departure 11. The tree has no ihc_checklist, so
   make_tree()'s IHC_CONFIRMS step has nothing to do.
13. Not built from the evidence: 8770/1, 8743/2 and 8750/3 (D4: ICCR prints them, ICD-O-3.2 lacks
   them), 8790/3 (ICD-O-3.2 prints 8790/0 only), 8780/3 (D3), an immunohistochemistry checklist
   (the evidence gives no rule), a laboratory screen (none), and Rule F stated-behaviour codes
   (D6). Amelanotic melanoma (8730/3) stays a picker entry as the evidence decided: Ferrari 2021
   (PDF p. 2) reports a clinical colour, not a WHO subtype.

Registrar questions the evidence raised (XId_melanoma.md, questions 1-10) stay open; the
defaults above apply until they are answered (docs/group_11_registrar_review.md).
"""
from __future__ import annotations

import group11_common as common
from group11_common import (OUTSIDE_XI, TYPE_NOT_STATED, TreeError, aid, cyto, evidence_gate,
                            excl, go, named, node, nonrep, not_malignant_node, rec, refer, term)

TREE_ID = "g11_melanoma"
P = "me_"
EVIDENCE = "XId_melanoma"
# Departure 2: the sites where ICCC-2017 places 8000/3 and 8001/3 in XIIb and a melanoma arises.
WHERE_NO_TISSUE = "the skin, the eye, a mucosa or an unknown primary site"
UNKNOWN_PRIMARY = "C80.9"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Sargen p. 3 "defined by the presence of spitzoid morphology plus a Spitz lineage driver event";
# "includes HRAS activating variants or fusion kinases involving"; "ALK, ROS1, NTRK1, NTRK3, MET,
# RET, BRAF, or MAP3K8".
AID_SPITZ = ("The report describes spitzoid cells with an HRAS variant or a kinase fusion such as "
             "ALK, ROS1, NTRK1, NTRK3, MET, RET, BRAF or MAP3K8.")
# Sargen p. 4 "MCMN often develop in the large and giant variants of CMN"; "often develop within
# the first decade of life".
AID_CONGENITAL = ("The report places the melanoma within a large or giant congenital naevus, often "
                  "in a child under ten.")
# Ferrari p. 2 "Among conventional melanoma, the superficial spreading type is the most
# frequently represented".
AID_SUPERFICIAL = ("The report names superficial spreading melanoma, the commonest conventional "
                   "melanoma in adolescents.")
# Sargen p. 4 "with most pediatric cases forming within giant congenital blue".
AID_BLUE = ("The report places the melanoma within a blue naevus, in a child most often a giant "
            "congenital blue naevus.")
# ICCR p. 9 "Melanoma within adnexal epithelium is in situ disease".
AID_IN_SITU = "The report confines the melanoma to the epidermis or the adnexal epithelium."
# Sargen p. 3 "intermediate lesions with a low, but increased risk for"; Ferrari p. 3 "The
# histology report should distinguish melanoma from lesion of uncertain malignancy".
AID_SPITZ_MELANOCYTOMA = "The report calls the Spitz tumour intermediate, or of uncertain malignancy."
# Ferrari p. 2 "number or degree to justify a diagnosis of malignancy"; GoldmanLevy p. 5 "falling
# short of melanoma criteria may be considered to have uncertain malignant potential".
AID_MELTUMP = ("The report lists features suggestive of malignancy but calls them too few to "
               "diagnose melanoma.")
# GoldmanLevy p. 4 "Nodule in congenital nevus (CN) (melanocytoma)"; Sargen p. 4 "difficult to
# distinguish from melanoma based on clinical and histopathologic features".
AID_NODULE = ("The report describes a nodule within a congenital naevus and states it falls short "
              "of melanoma.")
# Milman p. 5 "obvious melanomas without documented evidence of subepithelial invasion".
AID_CONJ_IN_SITU = "The report finds melanoma without subepithelial invasion."
# Sargen p. 4 "leptomeningeal deposits of melanocytes, which can transform into primary central
# nervous system melanoma".
AID_MENINGEAL = "The report may describe the melanoma in a child with a large congenital naevus."

# Departures 3 and 9: the instruction a screen carries while a melanoma deposit with a known
# primary cannot be referred to Group XI itself (group11_common.SELF_REFERRAL).
BACK_TO_SITE = ("When the report names the site where the primary melanoma began, go back to the "
                "site step, record that site, and code the melanoma from that site's screen.")
# Departure 2: the gate's clinical-note screens. Until 8 October 2026 their hint sent a skin
# melanoma on a note to the skin site, where Visser 2023 Table 3 recorded 8720/3 at basis 1. The
# registrar ruled for the paediatric source (review A8, E9; Ferrari 2021, PDF p. 3): a child's
# melanoma needs tissue, so the note screens here are the common ones and the hint is dropped.


def _primary_named(label: str) -> list:
    """D10: a melanoma deposit whose primary the report names re-enters Group XI at the
    primary's site (refer_group 11 with recapture_site). Built only when
    group11_common.SELF_REFERRAL is True; until then the screen's hint says BACK_TO_SITE."""
    if not common.SELF_REFERRAL:
        return []
    return [refer(label, common.GROUP,
                  "A deposit is coded at its primary. Record the site where the primary melanoma "
                  "began; the case returns to Group XI there, and that site's melanoma screen "
                  "gives the code.", recapture=True,
                  note="D10. Rules PDF p. 2 (printed p. 15), Rule H: 'ascertain that the "
                       "neoplasm at the site mentioned is not a metastasis'.")]


def _hint_back_to_site(text: str) -> str:
    return text if common.SELF_REFERRAL else "%s %s" % (text, BACK_TO_SITE)


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence mel_evidence, mel_clinical, mel_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    nodes = evidence_gate(
        P, where=WHERE_NO_TISSUE,
        question="What is in the file about this melanoma?",
        # Evidence mel_evidence hint and option 5. Sargen p. 5 "should not rely solely on a
        # tumor" (a gene profile alone does not diagnose melanoma).
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or excision "
              "counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. An immunohistochemistry or gene "
              "report is read with the histology report it belongs to; on its own it does not "
              "register a melanoma."),
        tier_labels={
            # Evidence mel_evidence option 2.
            "imaging": "An imaging report only (ultrasound, CT or MRI scan) - no tissue",
            # Evidence mel_evidence option 3. Milman p. 8 "for benign and malignant melanocytic
            # tumors of the iris, ciliary body, and choroid"; Ferrari p. 3 "or core biopsy is
            # required if nodal involvement".
            "cytology": "A cytology report (fine-needle aspiration) - no histology report",
            # Evidence mel_evidence option 4. Ferrari p. 3 "When melanoma is suspected, initial
            # excisional biopsy is required."; ICCR p. 16 "Various ancillary studies may be used
            # to assist in establishing a diagnosis of melanoma".
            "histology": "A histology report from a biopsy or excision, with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=[
            # Evidence mel_cytology option 1. Milman p. 10 "spindle-shaped in spindle melanoma
            # cells and ovoid in epithelioid melanoma cells"; Milman p. 8.
            cyto("Melanoma, stated as the diagnosis, in a sample from the primary tumour", "8720",
                 note="Evidence mel_cytology option 1."),
        ] + _primary_named(
            # Evidence mel_cytology option 2. Ferrari p. 3 "or core biopsy is required if nodal
            # involvement"; Rules PDF p. 2 "ascertain that the neoplasm at the site mentioned is
            # not a metastasis".
            "Melanoma in a lymph node or another deposit, and the report names the site where "
            "the primary melanoma began") + [
            # Evidence mel_cytology option 3. GoldmanLevy p. 10 "It comprises metastases to skin
            # and cancer of unknown primary site (CUP)".
            _unknown_primary(cyto(
                "Melanoma in a deposit, and the report states no primary melanoma was found",
                "8720", "The site is recorded as the unknown primary site (C80.9).",
                note="Evidence mel_cytology option 3; D10 (WHO section 4.2.2: an unknown primary "
                     "is C80.9). ICCC-2017 range 123 holds 8720/3 in XId at C80.9.")),
            # Evidence mel_cytology option 4.
            nonrep("Suspicious for melanoma, or melanoma not excluded",
                   "Not registrable. A suspected melanoma is only possible (%s, rule 4). Record "
                   "the case when a report states melanoma." % common.VISSER,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "cytology_suspicious_melanoma"},
                   note="Evidence mel_cytology option 4."),
        ],
        note="Evidence mel_evidence, mel_clinical and mel_cytology (departures 1 to 3 in the "
             "module docstring).")
    for nd in nodes:
        # The common screens say "a carcinoma's type"; this tree's tumour is a melanoma.
        nd["hint"] = nd["hint"].replace("a carcinoma's type", "a melanoma's type")
        if nd["node_id"] == n("cytology"):
            nd["hint"] = _hint_back_to_site("%s A melanoma deposit is coded at its primary."
                                            % nd["hint"])
    return nodes


def _unknown_primary(branch):
    """Set the unknown primary site (C80.9) on a coded branch (D10, WHO section 4.2.2)."""
    branch.setdefault("captures", {})["topography"] = UNKNOWN_PRIMARY
    return branch


# ------------------------------------------------------------------------------------------
# Where the melanoma arose (evidence mel_site)
# ------------------------------------------------------------------------------------------
def histology():
    return node(
        n("histology"), "site_resolution", 3, "Site of the melanoma",
        "Where did the melanoma arise?",
        # Evidence mel_site hint. Rules A, B, C and H (Rules PDF pp. 2-4, printed pp. 15-17):
        # "nevus of the arm are coded to C44.6"; "NOS are not assigned to C76 but to skin (C44)".
        "A melanoma of the arm, leg, trunk, chin or forehead with no tissue named is a melanoma "
        "of the skin of that region. A site named with a prefix such as peri- or para- takes the "
        "tissue the report names. A melanoma that spans two skin regions with no stated point of "
        "origin takes the overlapping-lesion code (.8). ICD-O prints skin (C44) beside many "
        "melanoma names: when the report names another site, record that site once the report "
        "shows the tumour there is not a deposit.",
        [
            # Rules PDF p. 4 "nevus of the arm are coded to C44.6"; Milman p. 9 "Invasive
            # cutaneous melanoma"; GoldmanLevy p. 9 "Acral naevus and melanoma are covered in the
            # dedicated chapter for melanocytic tumours".
            go("Skin, including the eyelid, the skin of the lip, the scalp, the palm, the sole and "
               "the nail unit", n("skin_histology"), note="Evidence mel_site option 1."),
            # Milman p. 3 "Conjunctival melanoma"; p. 10 "Choroidal and ciliary body melanomas";
            # p. 15 "Primary orbital melanoma"; p. 12 "Melanoma involving the lacrimal drainage
            # system".
            go("The eye: the conjunctiva, inside the eye (choroid, ciliary body or iris), the "
               "orbit or the lacrimal drainage system", n("eye"),
               note="Evidence mel_site options 2 and 3, merged (departure 4)."),
            # ICCR p. 8 "Mucosal melanoma 8720/3"; Thompson p. 2 "melanocytic tumors and
            # metastases to head and neck sites are also each included".
            go("A mucosa: mouth, nasal cavity or sinuses, nasopharynx, anal canal or rectum, "
               "vulva, vagina or another mucosa", n("mucosa"), note="Evidence mel_site option 4."),
            # GoldmanLevy p. 5 "Skin5 also includes melanocytic tumours of the central nervous
            # system (CNS)"; Sargen p. 4 "leptomeningeal deposits of melanocytes, which can
            # transform into primary central nervous system melanoma".
            go("The meninges, brain or spinal cord, as the primary site", n("cns"),
               note="Evidence mel_site option 5."),
            go("Another internal organ, such as the lung, the liver or the adrenal gland",
               n("other"), note="Departure 10: the controller's brief (D13)."),
            # GoldmanLevy p. 4 "They should be distinguished from primary clear cell sarcoma".
            _refer_clear_cell_sarcoma(
                "Deep soft tissue, tendon or aponeurosis, and the report calls the tumour clear "
                "cell sarcoma or melanoma of soft parts", "Evidence mel_site option 6."),
            # GoldmanLevy p. 10 "The most frequent primary cancers are breast cancer in women and
            # melanoma in men"; Rules PDF p. 2 "ascertain that the neoplasm at the site mentioned
            # is not a metastasis".
            go("A lymph node or another organ holding a deposit of a melanoma that began "
               "elsewhere", n("deposit"),
               note="Evidence mel_site options 7 and 8, merged in me_deposit (departure 4)."),
        ], [],
        "Evidence mel_site (departure 4). Reached from the gate's histology tier only; the "
        "other trees hop straight to the screens below.")


def _refer_clear_cell_sarcoma(label, note):
    """Clear cell sarcoma (9044/3) is IXd7 at every site (ICCC-2017); ICD-O-3.2 gives Malignant
    melanoma of soft parts as a related term of 9044/3, not of a melanoma code."""
    return refer(label, 9,
                 "%s (9044/3) is a soft tissue sarcoma, ICCC-3 subgroup IXd. ICD-O-3.2 gives "
                 "Malignant melanoma of soft parts as a related term of that code, not of a "
                 "melanoma code. Code the case from the Group IX (soft tissue sarcomas) tree."
                 % term("9044", "3"),
                 note=note + " ICCC-2017: 9044 is IXd7 at 000-809.")


# ------------------------------------------------------------------------------------------
# Wording the registrar's ruling of 8 October 2026 on review A1 (a)(b) adds (docs/
# group_11_evidence/registrar_A1ab_rules.md C9, C10, C11). The terms are read from icdo32.sqlite.
# ------------------------------------------------------------------------------------------
# C10: ICD-O-3.1 Rule H, p. 23. ICD-O-3.2 prints C69._ beside 8773/3 and 8774/3, the usual site; it
# gives way to a site the report states and removes the term from no site. A skin report that says
# only "spindle cell melanoma" is 8772/3 (the picker's own sentence before the ruling).
SPINDLE_AB_SENTENCE = (
    "%s (8773/3) and %s (8774/3) name the eye as the usual site. A skin report that says type A "
    "or type B takes the term; a skin report that says only spindle cell melanoma is %s (8772/3)."
    % (term("8773", "3"), term("8774", "3"), term("8772", "3")))
# C9: ICD-O-3.1 Rule H, pp. 15 and 23. ICD-O-3.2 lists Mixed epithelioid and spindle cell melanoma
# as a Related term of 8770/3, whose Preferred term it prints with C44._; the skin topography does
# not apply to a tumour of the eye. (The rule is applied in the reason below.)
MIXED_EYE = "Mixed epithelioid and spindle cell melanoma"
assert MIXED_EYE in common.live_search_terms("8770", "3"), "ICD-O-3.2 no longer lists " + MIXED_EYE
MIXED_EYE_REASON = (
    "ICD-O-3.2 lists %s under this code. ICD-O-3.2 prints the skin beside this code's Preferred "
    "term; that topography does not apply to a tumour of the eye (WHO coding Rule H)." % MIXED_EYE)
# C11: ICD-O-3.1 section 4.3.3, p. 21: coding is based on what the pathologist states as the
# diagnosis, so a melanoma that is spitzoid only in the description is Malignant melanoma, NOS.
SPITZOID_SENTENCE = (
    "Take the Spitz option when the diagnosis line says spitzoid melanoma, Spitz melanoma or "
    "malignant Spitz tumour. A melanoma described as spitzoid only in the microscopic "
    "description, with a diagnosis of melanoma, is %s (8720/3)." % term("8720", "3"))


# ------------------------------------------------------------------------------------------
# Melanoma of the skin (evidence mel_skin_histology)
# ------------------------------------------------------------------------------------------
def skin_histology():
    return node(
        n("skin_histology"), "histology_subclassification", 4, "Melanoma of the skin",
        "What does the histology report call the tumour?",
        # Evidence mel_skin_histology hint, with Rule F dropped (departure 5b). Rule K: Rules
        # PDF p. 3 (printed p. 16); evidence rules_a_to_k K.
        "If the report names two melanoma types for one tumour, record the type with the higher "
        "code number (WHO coding Rule K): an amelanotic Spitz melanoma is recorded as Malignant "
        "Spitz tumor (8770/3), and an acral nodular melanoma as Acral melanoma (8744/3). A tumour "
        "the report calls intermediate, of uncertain malignant potential, in situ or a naevus is "
        "on the screen for tumours that are not malignant. " + SPITZOID_SENTENCE,
        [
            # ICCR p. 8 "Spitz melanoma 8770/3"; Sargen p. 1 "subtypes of melanoma occur in
            # children: Spitz melanoma,"; Ferrari p. 2 "the most common histotype is spitzoid
            # melanoma". Registrar question 1 (spitzoid melanoma).
            aid(named("Spitz melanoma, malignant Spitz tumour or spitzoid melanoma", "8770",
                      "ICD-O-3.2 gives Spitz melanoma and Spitzoid melanoma as synonyms of this "
                      "code.",
                      note="D1: Sargen 2026, PDF p. 1; registrar question 1."), AID_SPITZ),
            # ICCR p. 8 "Melanoma arising in giant congenital naevus 8761/3"; Ferrari p. 2 "is
            # melanoma arising in association with giant congenital nevi"; Pfister p. 11.
            aid(named("Melanoma arising in a congenital melanocytic naevus, including a large or "
                      "giant congenital naevus", "8761",
                      "ICD-O-3.2 gives Malignant melanoma in congenital melanocytic nevus as a "
                      "synonym of this code, so the size of the naevus does not change it.",
                      note="D1: Sargen 2026, PDF p. 4; Ferrari 2021, PDF p. 2."), AID_CONGENITAL),
            # ICCR p. 8 "Low-cumulative sun damaged melanoma (including superficial spreading";
            # Ferrari p. 2 "the most commonly encountered subtypes are conventional adult
            # melanoma".
            aid(named("Superficial spreading melanoma, or low cumulative sun damage melanoma",
                      "8743",
                      "ICD-O-3.2 gives Superficial spreading melanoma as a related term of this "
                      "code.",
                      note="D1: Sargen 2026, PDF p. 1; Ferrari 2021, PDF p. 2."), AID_SUPERFICIAL),
            # ICCR p. 8 "Melanoma arising in blue naevus 8780/3"; Sargen p. 4 "This melanoma
            # subtype is especially rare in pediatric patients,". D3 (departure 5a).
            aid(named("Melanoma arising in a blue naevus", "8720",
                      "ICD-O-3.2 marks obsolete the Preferred term of 8780/3, the code that holds "
                      "Melanoma arising in blue nevus, and an obsolete term stays off every "
                      "screen, so the general melanoma code is recorded. This awaits the "
                      "registrar's decision.",
                      upgrade="The more specific code, 8780/3, awaits the registrar's decision.",
                      note="D3 (departure 5a); currency check 8780; the registrar review."),
                AID_BLUE),
            # ICCR p. 8 "Melanoma, not otherwise specified (NOS) 8720/3"; ICCR p. 7 "is non-core
            # when it cannot be made with confidence".
            named("Melanoma or malignant melanoma, with no type stated", "8720",
                  "ICD-O-3.2 gives Melanoma, NOS as a synonym of this code.",
                  upgrade=TYPE_NOT_STATED,
                  note="Evidence mel_skin_histology option 5; the screen's generic option."),
            # ICCR p. 8 "Nodular melanoma 8721/3", "Acral melanoma 8744/3", "Desmoplastic
            # melanoma 8745/3", "High-cumulative sun damaged melanoma (lentigo maligna melanoma)
            # 8742/3"; Ferrari p. 2 "Pediatric melanoma might be amelanotic".
            go("Another melanoma type the report names (for example nodular, acral, desmoplastic, "
               "amelanotic, naevoid or lentigo maligna melanoma) - type its name to find it",
               n("picker"), note="D2: the melanoma picker."),
            go("A tumour the report calls intermediate, of uncertain malignant potential, in situ "
               "or benign, including every naevus", n("not_malignant"),
               note="Departure 5c: the exclusion screen (contract §4.2)."),
            go("A deposit (metastasis) of a melanoma that began elsewhere", n("deposit"),
               note="Departure 5f; D10."),
            # GoldmanLevy p. 4 "They should be distinguished from primary clear cell sarcoma".
            _refer_clear_cell_sarcoma("Clear cell sarcoma, or malignant melanoma of soft parts",
                                      "Evidence mel_skin_histology option 13."),
            # GoldmanLevy p. 11 "Dermal spindle and epithelioid cell tumour with partial
            # melanocytic differentiation"; Sargen p. 3 "RNA sequencing is needed to distinguish
            # CTRTs and MARTs"; GoldmanLevy p. 4 "dermal clear cell tumours with melanocytic
            # differentiation". Registrar question 9.
            nonrep("CRTC1::TRIM11 cutaneous tumour, MED15::ATF1-rearranged tumour, or dermal "
                   "clear cell tumour with melanocytic differentiation",
                   "ICD-O-3.2 holds no code for these tumours, and the sources leave open whether "
                   "they are melanomas. No Group XI code is recorded; this awaits the registrar's "
                   "decision.",
                   note="Evidence mel_skin_histology option 14; registrar question 9."),
        ], [],
        "Evidence mel_skin_histology (departure 5). D1: Spitz melanoma, melanoma in a congenital "
        "naevus, low cumulative sun damage melanoma (Sargen 2026, PDF p. 1: the subtypes that "
        "occur in children) and melanoma in a blue naevus (Sargen 2026, PDF p. 4) are options; "
        "every other XId code is in the picker. Cross-tree entry from the skin tree (D13).")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # ICCR p. 9 "Melanoma within adnexal epithelium is in situ disease"; Ferrari p. 2 "are
            # localized (melanoma in situ, stages I and II)".
            aid(excl("Melanoma in situ, with no invasion", "8720", "2", what="a melanoma in situ"),
                AID_IN_SITU),
            # GoldmanLevy p. 4 "Spitz tumours comprise Spitz naevi, Spitz melanocytomas (AST) and
            # Spitz melanomas"; ICCR p. 8 "Spitz melanocytoma (Atypical Spitz tumour) 8770/1"
            # (a code ICD-O-3.2 lacks: D4).
            aid(nonrep("Spitz melanocytoma (atypical Spitz tumour)",
                       "A Spitz melanocytoma is an intermediate tumour between a Spitz naevus and "
                       "a Spitz melanoma, not a malignant one. ICD-O-3.2 holds no term for it. %s"
                       % OUTSIDE_XI,
                       note="Evidence mel_skin_histology option 8; D4 (8770/1); departure 5e."),
                AID_SPITZ_MELANOCYTOMA),
            # Ferrari p. 2 "number or degree to justify a diagnosis of malignancy"; GoldmanLevy
            # p. 5.
            aid(nonrep("Melanocytic tumour of uncertain malignant potential (MELTUMP), a "
                       "melanocytoma, or an atypical cellular blue naevus",
                       "These tumours fall short of melanoma. %s" % OUTSIDE_XI,
                       note="Evidence mel_skin_histology option 9."), AID_MELTUMP),
            # GoldmanLevy p. 4 "PRKAR1A inactivation mutation".
            excl("Pigmented epithelioid melanocytoma", "8780", "1",
                 what="a pigmented epithelioid melanocytoma"),
            # GoldmanLevy p. 4 "Nodule in congenital nevus (CN) (melanocytoma)".
            aid(excl("Proliferative nodule in a congenital naevus", "8762", "1",
                     what="a proliferative nodule in a congenital naevus",
                     extra="ICD-O-3.2 gives Proliferative nodule in congenital melanocytic nevus "
                           "as a synonym of this code."), AID_NODULE),
            # Pfister p. 14 "Pigmented spindle cell nevus (Reed nevus) Melanoma" and "Blue nevus
            # and cellular blue nevus Spitz nevus"; icdo32 8770/0 Synonym Juvenile melanoma
            # (departure 5d).
            excl("Spitz naevus, Reed naevus (pigmented spindle cell naevus), or juvenile melanoma",
                 "8770", "0", what="a Spitz naevus",
                 extra="ICD-O-3.2 gives Spitz nevus, NOS and Juvenile melanoma as synonyms and "
                       "Pigmented spindle cell nevus of Reed as a related term of this code: "
                       "juvenile melanoma is an older name for a Spitz naevus, not a melanoma.",
                 note="Departure 5d: standing rule 8."),
            # Pfister p. 14; ICCR p. 8 "Acral naevus 8744/0".
            nonrep("Another naevus: congenital, blue, cellular blue, dysplastic or acral naevus",
                   "A naevus is not a malignant tumour. ICD-O-3.2 codes these naevi as benign "
                   "(behaviour 0), and a giant congenital naevus as %s (8761/1), behaviour 1, "
                   "uncertain. %s" % (term("8761", "1"), OUTSIDE_XI),
                   note="Evidence mel_skin_histology option 12 (departure 5d)."),
        ],
        where="the skin", catch_all=True,
        note="The exclusions of evidence mel_skin_histology (departure 5c).")


# ------------------------------------------------------------------------------------------
# The eye (evidence mel_conjunctiva and mel_eye)
# ------------------------------------------------------------------------------------------
UVEAL_UPGRADE = ("The report does not state the cell type. A report that names it (epithelioid "
                 "cell, spindle cell, or mixed epithelioid and spindle cell) gives that type's own "
                 "code: go back and choose another melanoma type.")


def eye():
    return node(
        n("eye"), "histology_subclassification", 4, "Melanoma of the eye",
        "What does the report call the tumour of the eye, the orbit or the lacrimal drainage "
        "system?",
        # Evidence mel_picker hint (Rule H, Rules PDF p. 2, printed p. 15).
        SPINDLE_AB_SENTENCE + " A uveal melanoma of mixed epithelioid and spindle cell type is "
        "recorded as Malignant Spitz tumor (8770/3), the code ICD-O-3.2 gives it.",
        [
            # Milman p. 3 "Conjunctival melanoma"; p. 22 "tool for childhood conjunctival
            # melanoma".
            named("Conjunctival melanoma", "8720",
                  note="D1: Milman 2023, PDF p. 22. Evidence mel_conjunctiva option 1."),
            # Milman p. 10 "Choroidal and ciliary body melanomas"; p. 9 "Iris melanoma".
            named("Choroidal, ciliary body or iris melanoma (uveal melanoma), with no cell type "
                  "stated", "8720", upgrade=UVEAL_UPGRADE,
                  note="Evidence mel_eye option 1 and mel_picker option 13 (departure 6)."),
            # Milman p. 15 "Primary orbital melanoma"; p. 12 "Melanoma involving the lacrimal
            # drainage system".
            named("Primary orbital melanoma, or melanoma of the lacrimal drainage system", "8720",
                  note="Evidence mel_picker options 19 and 20 (departure 6)."),
            named("Melanoma of the eye, with no type or part of the eye stated", "8720",
                  upgrade=TYPE_NOT_STATED,
                  note="Evidence mel_conjunctiva option 1 ('or melanoma with no type stated')."),
            # Milman p. 10 "spindle-shaped in spindle melanoma cells and ovoid in epithelioid
            # melanoma cells".
            go("Another melanoma type the report names, including a uveal melanoma's cell type "
               "(epithelioid cell, spindle cell type A or B, or mixed) - type its name to find it",
               n("picker"), note="Evidence mel_conjunctiva option 5; D2."),
            # Milman p. 5 "obvious melanomas without documented evidence of subepithelial
            # invasion".
            aid(excl("Melanoma in situ of the conjunctiva", "8720", "2",
                     what="a conjunctival melanoma in situ"), AID_CONJ_IN_SITU),
            # Milman p. 3 "Conjunctival melanocytic intraepithelial lesions"; p. 5 "The term
            # melanoma in situ may be used for (1) the". Registrar question 10.
            nonrep("Conjunctival melanocytic intraepithelial lesion, low or high grade (primary "
                   "acquired melanosis)",
                   "The lesion is confined to the epithelium; it is not an invasive melanoma. %s"
                   % OUTSIDE_XI,
                   note="Evidence mel_conjunctiva option 3; registrar question 10 (8741/2)."),
            # Pfister p. 12 "Conjunctival junctional, compound, and subepithelial nevi"; Milman
            # p. 3 "Blue nevus of the conjunctiva".
            excl("Conjunctival naevus: junctional, compound, subepithelial, inflamed juvenile, "
                 "blue or deep penetrating naevus", "8720", "0", what="a conjunctival naevus",
                 extra="ICD-O-3.2 gives Conjunctival nevus as a related term of this code, and "
                       "codes a blue naevus as %s (8780/0)." % term("8780", "0")),
            # Milman p. 10 "Uveal melanocytoma"; p. 12 "Melanocytoma of the optic disk and optic
            # nerve".
            excl("Uveal melanocytoma, or melanocytoma of the optic disc", "8726", "0",
                 what="a melanocytoma of the eye",
                 extra="ICD-O-3.2 gives Melanocytoma, eyeball as a synonym of this code.",
                 note="Evidence mel_eye option 2, split (departure 6)."),
            nonrep("Uveal naevus (a naevus of the choroid, ciliary body or iris)",
                   "A uveal naevus is benign. %s" % OUTSIDE_XI,
                   note="Evidence mel_eye option 2, split: no source maps a uveal naevus to an "
                        "ICD-O-3.2 code (departure 6)."),
            go("A deposit (metastasis) of a melanoma that began elsewhere", n("deposit"),
               note="Departure 6; D10."),
        ], [],
        "Evidence mel_conjunctiva and mel_eye, merged (departure 6). D1: conjunctival melanoma "
        "(Milman 2023, PDF p. 22). Cross-tree entry from the eye tree (D13).")


# ------------------------------------------------------------------------------------------
# Mucosa (evidence mel_mucosa)
# ------------------------------------------------------------------------------------------
def mucosa():
    return node(
        n("mucosa"), "histology_subclassification", 4, "Mucosal melanoma",
        "What does the histology report call the melanoma?",
        # Rules PDF p. 2 (printed p. 15), Rule H: "ascertain that the neoplasm at the site
        # mentioned is not a metastasis".
        "Before recording the melanoma at this site, check that the report does not call it a "
        "deposit (metastasis) of a melanoma that began elsewhere: a deposit is coded at its "
        "primary (WHO coding Rule H).",
        [
            # ICCR p. 8 "Mucosal melanoma 8720/3" (departure 7).
            named("Mucosal melanoma", "8720", note="Evidence mel_picker option 5 (departure 7)."),
            named("Melanoma or malignant melanoma, with no type stated", "8720",
                  upgrade=TYPE_NOT_STATED, note="Evidence mel_mucosa option 1."),
            # ICCR p. 8 "Mucosal lentiginous melanoma 8746/3".
            go("Another melanoma type the report names (for example mucosal lentiginous "
               "melanoma) - type its name to find it", n("picker"),
               note="Evidence mel_mucosa option 2; D2."),
            excl("Melanoma in situ of the mucosa", "8720", "2", what="a mucosal melanoma in situ",
                 note="Evidence mel_mucosa option 3."),
            # ICCR p. 8 "Mucosal and genital naevi 8720/0".
            excl("A mucosal or genital naevus", "8720", "0", what="a mucosal or genital naevus",
                 extra="ICD-O-3.2 gives Genital nevus as a related term of this code.",
                 note="Evidence mel_mucosa option 4."),
            go("A deposit (metastasis) of a melanoma that began elsewhere", n("deposit"),
               note="Departure 7; D10."),
        ], [],
        "Evidence mel_mucosa (departure 7). Cross-tree entry (D13) from every tree whose site is "
        "neither skin, eye nor the central nervous system, until MELANOMA_ENTRY names me_other.")


# ------------------------------------------------------------------------------------------
# Central nervous system (evidence mel_cns)
# ------------------------------------------------------------------------------------------
def cns():
    return node(
        n("cns"), "histology_subclassification", 4, "Melanocytic tumour of the meninges",
        "What does the histology report call the melanocytic tumour of the meninges, brain or "
        "spinal cord?",
        "Use the report's final diagnosis. A meningeal melanocytoma or meningeal melanocytosis is "
        "not a malignant tumour.",
        [
            # Pfister p. 18 "Meningeal melanocytosis and melanomatosis"; "This table lists CNS
            # tumor types that mainly occur in children and adolescents".
            named("Meningeal melanomatosis", "8728",
                  note="D1: Pfister 2022, PDF p. 18. Currency check 8728: the REDCap label is the "
                       "/1 term; the REDCap-side list holds the relabel."),
            # Pfister p. 16 "Meningeal melanoma"; Sargen p. 4.
            aid(named("Meningeal melanoma, or primary melanoma of the central nervous system",
                      "8720",
                      "ICD-O-3.2 gives Melanoma, meningeal as a related term of this code.",
                      note="D1: Pfister 2022, PDF p. 16."), AID_MENINGEAL),
            # Pfister p. 16 "Meningeal melanocytoma". Registrar question 7.
            excl("Meningeal melanocytoma", "8728", "1", what="a meningeal melanocytoma",
                 decision=True, note="Evidence mel_cns option 3; registrar question 7."),
            # Pfister p. 18 "Meningeal melanocytosis and melanomatosis". Registrar question 7.
            excl("Meningeal melanocytosis", "8728", "0", what="meningeal melanocytosis",
                 extra="ICD-O-3.2 gives Diffuse melanocytosis as a related term of this code.",
                 decision=True, note="Evidence mel_cns option 4; registrar question 7."),
            # Rules PDF p. 2 "ascertain that the neoplasm at the site mentioned is not a
            # metastasis".
            go("Melanoma that spread to the brain or meninges from a primary elsewhere",
               n("deposit"), note="Evidence mel_cns option 5 (departure 8); D10."),
        ], [],
        "Evidence mel_cns (departure 8). Group III's meningeal lesion triage refers every "
        "melanocytic meningeal tumour to Group XI; this screen receives it (evidence conflicts).")


# ------------------------------------------------------------------------------------------
# Another internal organ (the controller's brief, D13; departure 10)
# ------------------------------------------------------------------------------------------
def other():
    return node(
        n("other"), "histology_subclassification", 4, "Melanoma of an internal organ",
        "Does the report call the melanoma a primary tumour of this organ?",
        # Rules PDF p. 2 (printed p. 15), Rule H.
        "A melanoma is coded at the site where it began. Record it at this organ only when the "
        "report calls it primary here; otherwise it is a deposit, coded at its primary (WHO "
        "coding Rule H).",
        [
            named("The report calls it a primary melanoma of this organ, with no type stated",
                  "8720", upgrade=TYPE_NOT_STATED,
                  note="Departure 10. ICCC-2017 range 123: 8720/3 is XId at every site."),
            go("The report calls it a primary melanoma of this organ and names its type - type "
               "its name to find it", n("picker"), note="Departure 10; D2."),
            go("The report calls it a deposit (metastasis) of a melanoma, or does not call it "
               "primary", n("deposit"), note="Departure 10; D10."),
        ], [],
        "Departure 10: the controller's brief (D13). No evidence node; the evidence's sites "
        "(skin, eye, mucosae, meninges, C80.9) name no internal organ.")


# ------------------------------------------------------------------------------------------
# The deposit question (D10; evidence mel_site options 7 and 8)
# ------------------------------------------------------------------------------------------
def deposit():
    return node(
        n("deposit"), "morphology_only", 5, "Metastatic deposit",
        "Does the report name the site where the primary melanoma began?",
        _hint_back_to_site(
            "The melanoma here is a deposit, not a separate registration: the case is coded at "
            "the site where the primary melanoma began. When no primary has been found, it is "
            "recorded at the unknown primary site (C80.9)."),
        _primary_named("Yes: the report names the site where the primary melanoma began") + [
            # GoldmanLevy p. 10 "It comprises metastases to skin and cancer of unknown primary
            # site (CUP)"; Rules PDF p. 14 "Histology of a metastasis" (basis 6, registrar
            # question 5; departure 9).
            _unknown_primary(named(
                "No: the report states that no primary melanoma was found", "8720",
                "A melanoma known only from a deposit is recorded at the unknown primary site "
                "(C80.9).",
                upgrade="A report that finds the primary melanoma gives the primary's site and "
                        "may name its type.",
                note="Evidence mel_site option 8: basis 6 in the evidence, 7 here (D15; "
                     "registrar question 5). ICCC-2017 range 123 holds 8720/3 in XId at C80.9.")),
        ], ["topography"],
        "D10 for a melanoma (departure 9). SELF_REFERRAL is %s: build_database's "
        "check_refer_terminals fails a referral to Group XI from Group XI's own file."
        % common.SELF_REFERRAL)


# ------------------------------------------------------------------------------------------
# The picker (D2; evidence mel_picker), and the tree
# ------------------------------------------------------------------------------------------
def _option_codes(nodes) -> set:
    return {o["morphology_code"] for nd in nodes for o in nd.get("options") or []
            if isinstance(o, dict) and o.get("morphology_code")}


def picker(offered: set):
    """D2 for the melanoma tree (departure 11): every (code, 3) ICCC-2017 places in XId (range
    123, topography 000-809, so valid at every site), less a Preferred term ICD-O-3.2 marks [obs]
    (D3). The codes the screens offer are kept, because each screen offers them under a site's
    own label only."""
    opts, obsolete = [], []
    for c in sorted(common.melanoma_codes()):
        term(c, "3")
        if common.preferred_is_obsolete(c, "3"):
            obsolete.append(c)
            continue
        if common.iccc_subgroups(c, UNKNOWN_PRIMARY) != ["XId"]:
            raise TreeError("%s/3 is not XId at %s in ICCC-2017" % (c, UNKNOWN_PRIMARY))
        o = named(term(c, "3"), c, MIXED_EYE_REASON if c == "8770" else None,
                  note="D2 picker: ICCC-2017 subgroup XId at every site (range 123, topography "
                       "000-809)." + (" Registrar ruling 8 October 2026 (review A1 (b), Q25), "
                                      "registrar_A1ab_rules.md C9: ICD-O-3.1 Rule H, pp. 15 and "
                                      "23." if c == "8770" else ""))
        found = common.live_search_terms(c, "3")
        if found:
            o["search_terms"] = found
        opts.append(o)
    kept = sorted(offered & {o["morphology_code"] for o in opts})
    common.PICKER_REPORT[TREE_ID] = {"offered": [o["morphology_code"] for o in opts],
                                     "partial": [], "held_as_options": [],
                                     "obsolete": obsolete, "d11": []}
    nd = node(
        n("picker"), "histology_subclassification", 5, "Another melanoma",
        "Which melanoma does the report name?",
        # Evidence mel_picker hint; Rule H (Rules PDF p. 2, printed p. 15) and Rule K (PDF p. 3,
        # printed p. 16).
        "Type part of the name in the box and the matching options appear. The other names "
        "ICD-O-3.2 gives a melanoma find it too. Use the report's own term. If the report names "
        "two melanoma types for one tumour, choose the higher code (WHO coding Rule K). "
        + SPINDLE_AB_SENTENCE,
        opts, [],
        "D2 (registrar, 8 October 2026: 'Picker, as in Group 10'), built in this module "
        "(departure 11): every code ICCC-2017 places in XId (range 123: 8720-8780, 8790 at "
        "topography 000-809), less the [obs] Preferred terms (D3: %s); %d options in code order. "
        "Kept although a screen offers them under a site's own label: %s. 8790/3 is absent: "
        "ICD-O-3.2 prints 8790/0 only."
        % (", ".join(obsolete) or "none", len(opts), ", ".join(kept) or "none"))
    nd["prefill_filter_from_search"] = True
    return nd


def _assemble(nodes: list) -> dict:
    """make_tree()'s checks and output shape without its picker (departures 11 and 12)."""
    row = common.tree_row(TREE_ID)
    ids = [nd["node_id"] for nd in nodes]
    for nid_ in ids:
        if not nid_.startswith(row["prefix"]):
            raise TreeError("%s: node %s does not carry the prefix %s"
                            % (TREE_ID, nid_, row["prefix"]))
    if len(set(ids)) != len(ids):
        raise TreeError("%s: a node id is declared twice" % TREE_ID)
    if any(nd.get("node_type") == "ihc_checklist" for nd in nodes):
        raise TreeError("%s: a stain panel needs make_tree()'s IHC_CONFIRMS step" % TREE_ID)
    return {"tree_id": TREE_ID,
            "tree_label": "%s (every site; ICCC-3 Group XI subgroup XId, behaviour 3 only)"
                          % row["label"],
            "entry_node": n("document_inventory"),
            "topography": [],
            "basis_of_diagnosis_defaults": dict(common.BASIS_DEFAULTS),
            "nodes": nodes}


def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    screens = [skin_histology(), eye(), mucosa(), cns(), other()]
    nodes = gate() + [histology()] + screens[:1] + [not_malignant()] + screens[1:] + [deposit()]
    return _assemble(nodes + [picker(_option_codes(screens))])


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8720/3": ("D1, D3, D8, D10", EVIDENCE,
               "Malignant melanoma, NOS: melanoma with no type stated on the skin, eye, mucosa and "
               "internal-organ screens; conjunctival, uveal, orbital, lacrimal drainage system, "
               "mucosal and meningeal melanoma, which the WHO codes 8720/3; melanoma arising in a "
               "blue naevus, because ICD-O-3.2 marks the Preferred term of 8780/3 obsolete (D3, "
               "registrar); basis 5 when cytology names a melanoma; and a melanoma deposit with no "
               "primary found, recorded at C80.9 at basis 7 or 5 (registrar question 5 asks for "
               "basis 6)."),
    "8770/3": ("D1", EVIDENCE,
               "Spitz melanoma, a melanoma subtype that occurs in children (Sargen 2026, PDF p. 1; "
               "ICCR Invasive Melanoma Table 1), on the skin screen. ICD-O-3.2 gives Spitz "
               "melanoma and Spitzoid melanoma as synonyms at 8770/3 (registrar question 1)."),
    "8761/3": ("D1", EVIDENCE,
               "Melanoma arising in a congenital melanocytic naevus (ICCR Invasive Melanoma Table "
               "1; Sargen 2026, PDF p. 4), on the skin screen."),
    "8743/3": ("D1", EVIDENCE,
               "Superficial spreading melanoma, recorded as Low cumulative sun damage melanoma "
               "(ICCR Invasive Melanoma Table 1; Ferrari 2021, PDF p. 2), on the skin screen."),
    "8728/3": ("D1", EVIDENCE,
               "Meningeal melanomatosis (Pfister 2022, PDF p. 18) on the central nervous system "
               "screen; meningeal melanocytoma (8728/1) and melanocytosis (8728/0) are exclusions "
               "(registrar question 7)."),
}
