"""g11_salivary (prefix sg_): carcinomas of the major salivary glands at C07.9 and C08.0-C08.9,
ICCC-3 subgroup XIf1.

Built from docs/group_11_evidence/XIf1_salivary.json (the evidence agent's nodes sg_site,
sg_document_inventory, sg_cytology, sg_histology, sg_carcinoma_picker, sg_sialoblastoma,
sg_not_malignant) with the builders in build/group11_common.py, in the shape of the thyroid
exemplar. Every option's label, code, behaviour, basis, reason and recognition aid comes from that
file; the cite (file, PDF page, quotation) is the comment above the option or the aid. File names
in the comments are the evidence's own:
    ICCR      XIf1-salivary-gland__ICCR-Major-Salivary-Glands-2nd.txt (ICCR Carcinomas of the
              Major Salivary Glands, 2nd edition, version 2.0, July 2024). "image" marks a
              quotation read from the page image (Table 1, PDF p. 8).
    Skalova   XIf1-salivary-gland__Skalova-2022.txt (Skalova, Hyrcza, Leivo. Head Neck Pathol
              2022;16:40-53)
    Perez     XIf1-salivary-gland-paediatric__Perez-de-Oliveira-2025.txt (Med Oral Patol Oral Cir
              Bucal 2025; PMC12019652). Its pages are PMC sections, written "§5".
    Pfister   ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules     RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser    Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's file
              set, so the evidence carries no page quotation for it: evidence data gap 6)

Nodes, in tree order:
    sg_document_inventory  document_inventory  evidence gate (evidence sg_document_inventory)
    sg_clinical, sg_clinical_cytology  clinical_alias
    sg_imaging, sg_imaging_cytology    morphology_only
    sg_cytology            morphology_only     (evidence sg_cytology)
    sg_histology           histology_subclassification  (evidence sg_histology)
    sg_duct                histology_subclassification  (salivary duct and intraductal carcinoma)
    sg_site                site_resolution     (the Rule B option of evidence sg_site)
    sg_nut_result, sg_nut_basis, sg_nut_tests  histology_subclassification  (D12)
    sg_not_malignant       histology_subclassification  (evidence sg_not_malignant)
    sg_deposit             morphology_only     (D10)
    sg_picker              histology_subclassification  (D2; evidence sg_carcinoma_picker)

Departures from the evidence nodes, and why
-------------------------------------------
1. sg_site: the five gland options (parotid C07.9, submandibular C08.0, sublingual C08.1,
   overlapping lesion C08.8, major salivary gland NOS C08.9) are dropped. The router's site step
   answers them (D14), and the evidence gate is the tree's entry node.
2. sg_site, Rule B: kept, because the evidence argues it (rules_a_to_k B; Rules p. 1, printed
   p. 14) and the router cannot answer it: whether a tumour the report places beside a gland or
   in its region keeps the gland depends on the tumour's type. It is a site_resolution node
   reached from one histology option. A salivary gland carcinoma type returns to the histology
   screen with the site unchanged; any other type, or none, captures head, face or neck NOS
   (C76.0) and continues in the unspecified tree's histology screen (un_histology), the deposit
   node's pattern for C80.9 (D10). The evidence referred the case to Group XI with
   recapture_site; SELF_REFERRAL is False, so the capture replaces the self-referral. Registrar
   question 9 stays open.
3. sg_site, minor salivary gland: not built as an option. The evidence referred it to Group XI
   with recapture_site; the site it needs (the hard palate C05.0, or mouth NOS C06.9 when the
   report names no place; Rules p. 11, printed p. 24) is asked at the site step, which only a
   self-referral could reopen. The gate hint sends the clerk back to the site step, the
   deposit_node wording while SELF_REFERRAL is False.
4. sg_document_inventory: the referral and imaging tiers recorded 8000/3 at basis 1 and 2 on the
   gate itself. D7: each routes to its own screen (sg_clinical, sg_imaging), which refers the
   case to Group XII with refer_code 8000, because ICCC-2017 places 8000/3 at C07-C08 in XIIb
   (range 143; evidence conflicts, registrar question 8). The gate's options are the contract
   §4.2 tiers; the document checklist replaces the evidence's tier labels.
5. sg_document_inventory, "possible, probable or suspected cancer only": "probable" is
   registrable under Visser rule 4, which the common clinical and imaging screens apply (8000/3,
   referred to Group XII); "possible" and "suspected" are not registrable there. The evidence's
   option put "probable" with the non-registrable cases.
6. sg_cytology: the evidence's "A named carcinoma type -> sg_histology (basis 5)" cannot carry
   basis 5 onto the histology screen's basis-7 options. The cytology screen offers the named
   types itself at basis 5 (cyto(), D8): the five paediatric types and salivary gland
   carcinoma or adenocarcinoma NOS. A type the screen does not list records Carcinoma, NOS
   (8010/3) at basis 5, which understates the report, because group11_common has no cytology
   picker (request 1). "Malignant, with no tumour type named" (8000/3 at basis 5) becomes the
   common line, which refers to Group XII with 8001 (D8). The lymphoma referral is kept, and a
   Group XII referral is added for myoepithelial carcinoma, carcinosarcoma and malignant mixed
   tumour, so a cytology report naming one records no Group XI code. "Suspicious for
   malignancy, atypical, benign, or non-diagnostic" becomes the common suspicious line and the
   common non-diagnostic routes.
7. sg_histology: NUT carcinoma moves from the picker to the histology screen through the common
   NUT screens (D12, the controller's instruction for this tree). The evidence's entity row puts
   it in the picker because no salivary source names it; Pfister p. 14 lists it among the
   malignant head and neck tumours of children.
8. sg_histology: microsecretory adenocarcinoma (evidence picker option, 8502/3) merges into the
   secretory carcinoma option, which records the same code. ICD-O-3.2 prints no term for it, and
   the D2 picker's filter matches ICD-O-3.2 terms only, so the picker could not find it by name.
9. sg_histology: salivary duct carcinoma (evidence picker option, 8500/3) joins intraductal
   carcinoma on sg_duct. Intraductal carcinoma's code depends on invasion (8500/2 or 8500/3), so
   it is a histology option (D1 exception); salivary duct carcinoma shares the code and has no
   ICD-O-3.2 term the picker could find. The two intraductal options of evidence
   sg_not_malignant move to sg_duct; the in situ exclusion also stays on sg_not_malignant, where a
   report that calls the tumour in situ leads. picker_keep keeps 8500/3 in the picker as
   Infiltrating duct carcinoma, NOS.
10. sg_sialoblastoma: D6. The option "Yes, the report calls it malignant" (Group XII, 8974/3, a
   pair ICD-O-3.2 does not print) is not built. With one option left the screen collapses into
   a sialoblastoma exclusion (8974/1) on the histology screen, where the evidence placed the
   entity, and on sg_not_malignant. Registrar question 1. Superseded 8 October 2026 (review A11,
   E10): the registrar went with the papers, which call sialoblastoma malignant, so both screens
   refer every sialoblastoma to Group XII with refer_code 8974 (ICCC-2017 XIIa4).
11. sg_carcinoma_picker: D2 replaces the curated picker. Labels are ICD-O-3.2 Preferred terms,
   search_terms the live synonyms and related terms, and the options carry no recognition aid
   (Group 10's picker shape). Not shown from the evidence: the WHO labels and aids of
   hyalinizing clear cell carcinoma (EWSR1::ATF1), mucinous adenocarcinoma, sclerosing
   microcystic adenocarcinoma, carcinoma ex pleomorphic adenoma, squamous cell carcinoma "which
   the report states began in the salivary gland", oncocytic, poorly differentiated, small cell
   and large cell neuroendocrine carcinoma; the build report lists them. A recognition aid on
   the histology screen's picker option names the ICD-O-3.2 term under which the picker lists
   hyalinizing clear cell carcinoma (8310/3) and sclerosing microcystic adenocarcinoma (8407/3).
   The deposit option's aid carries the evidence's squamous cell carcinoma caution. 8407/3 is a
   D11 picker entry: no ICCC-2017 range holds it at C07-C08 (the evidence's code_currency row).
12. sg_carcinoma_picker, the three Group XII referrals (myoepithelial carcinoma 8982/3,
   carcinosarcoma 8980/3, malignant mixed tumour 8940/3; ICCC-2017 XIIa4 at every site): the
   picker holds codes only, so they move to the histology screen's referrals, each with its
   refer_code. The histology hint says where they are.
13. sg_histology, trailing options: the common ones (tail_options). Melanoma enters me_mucosa
   (D13): a salivary gland is none of skin, eye or central nervous system. The evidence's deposit
   option (refer_group null, recapture) is the deposit question (D10). The lymphoma referral
   splits in two under Rule D (Rules p. 2, printed p. 15): a lymphoma of the gland keeps the
   site; a lymphoma of an intraparotid or periparotid lymph node refers with recapture_site,
   because it takes a lymph node site (the evidence's reason). The sarcoma label is the
   evidence's. The common leukaemia (Group I, C42.1), germ cell (Group X) and other named tumour
   (Group XII) referrals are added; the evidence has no leukaemia option (rules_a_to_k E).
14. sg_not_malignant: the evidence's last line (another benign tumour, such as sclerosing
   polycystic adenoma) replaces the common catch-all, with the common reason, so the screen has
   one catch-all. The exclusion reasons are excl()'s standard wording with the evidence's
   synonyms as the extra sentence.
15. sg_histology hint: keeps the evidence's grade sentence and adds Rule K (the evidence's picker
   hint, since the D2 picker's hint is common), the carcinoma ex pleomorphic adenoma default
   (registrar questions 4 and 5) and where the Group XII referrals are.
16. Not built from the evidence: 8440/3 and 8450/3 (D3, every term [obs]); the /1
   forms of 8430 and 8550 (every term [obs]).

Registrar questions the evidence raised (XIf1_salivary.md, Registrar questions 1-9) stay open;
the defaults above apply until they are answered (docs/group_11_registrar_review.md).
"""
from __future__ import annotations

from group11_common import (TYPE_NOT_STATED, UNSPECIFIED_HISTOLOGY, aid, cyto, deposit_node,
                            evidence_gate, excl, go, make_tree, named, node, nonrep,
                            not_malignant_node, nut_nodes, refer, refer_germ_cell,
                            refer_leukaemia, refer_lymphoma, refer_other_named, refer_sarcoma,
                            tail_options, term, OUTSIDE_XI, live_search_terms)

TREE_ID = "g11_salivary"
P = "sg_"
WHERE = "the salivary glands"
EVIDENCE = "XIf1_salivary"


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Skalova p. 2 "Carcinoma types for which validated grading systems exist include adenoid
# cystic carcinoma, mucoepidermoid"; Skalova p. 3 "CRTC1-MAML2".
AID_MEC = ("The report may give a low, intermediate or high grade, or name a CRTC1::MAML2 or "
           "CRTC3::MAML2 fusion.")
# Skalova p. 3 "NR4A3 fusion/activation"; ICCR p. 9 "Tumours for which this phenomenon is well
# characterised include acinic cell".
AID_ACINIC = "The report may name an NR4A3 rearrangement, or high grade transformation."
# Perez §5 "Secretory carcinoma was first described in 2010, mimicking AciCC." and "presence of
# ETV6 translocation and if positive, reclassified as secretory carcinoma"; Skalova p. 3
# "ETV6-NTRK3 fusion"; Skalova p. 5 "myxoid stroma and shows strong mammaglobin positivity";
# the evidence's microsecretory picker option: Skalova p. 3 "MEF2C-SS18 fusion".
AID_SECRETORY = ("Secretory carcinoma resembles acinic cell carcinoma. The report may name an "
                 "ETV6 translocation, an ETV6::NTRK3 fusion or strong mammaglobin staining. "
                 "Microsecretory adenocarcinoma carries an MEF2C::SS18 fusion.")
# ICCR p. 2 "Tubular/cribriform pattern predominant"; Skalova p. 3 "MYB fusion/activation/
# amplification"; Perez §5 "CRTC1-MAML2 and MYB-NFIB fusion genes found in MEC and ACC,
# respectively".
AID_ADCC = ("The report may describe a tubular, cribriform or solid pattern, or name a MYB::NFIB "
            "fusion or another MYB or MYBL1 rearrangement.")
# Skalova p. 1 "Cribriform adenocarcinoma of salivary gland origin (CASG) now represents a
# distinctive subtype of polymorphous"; Skalova p. 7 "(previously known as polymorphous
# low-grade adenocarcinoma)".
AID_PAC = ("Cribriform adenocarcinoma of salivary gland origin is the cribriform subtype of "
           "polymorphous adenocarcinoma. Older reports call it polymorphous low-grade "
           "adenocarcinoma.")
# ICCR p. 8 image "Hyalinising clear cell carcinoma 8310/3" and "Sclerosing microcystic
# adenocarcinoma 8407/3"; icdo32.sqlite 8310/3 Preferred Clear cell adenocarcinoma, NOS, 8407/3
# Preferred Microcystic adnexal carcinoma (departure 11).
AID_PICKER = ("ICD-O-3.2 lists hyalinizing clear cell carcinoma as Clear cell adenocarcinoma, "
              "NOS, and sclerosing microcystic adenocarcinoma as Microcystic adnexal carcinoma: "
              "type those names.")
# ICCR p. 7 "typically a metastasis from another site" (squamous cell carcinoma in a salivary
# gland); ICCR p. 9 "intra- and peri-parotid or submandibular gland lymph nodes are commonly
# present"; the evidence's squamous cell carcinoma picker aid ("state that a skin or mucosal
# primary has been excluded").
AID_DEPOSIT = ("A squamous cell carcinoma in a salivary gland is typically a deposit from a "
               "primary in the skin or mucosa, often in a lymph node within or beside the "
               "gland.")
# Skalova p. 7 "Its in situ intraductal nature is demonstrated by an intact surrounding
# myoepithelial cell"; Skalova p. 2 "frank invasive growth with loss of myoepithelial cells can
# be seen".
AID_DUCT = ("An intraductal carcinoma keeps an intact layer of myoepithelial cells around its "
            "ducts; a report of invasive growth describes loss of that layer.")


# ------------------------------------------------------------------------------------------
# Group XII referrals for the salivary carcinomas ICCC-2017 places in XIIa4 (departure 12)
# ------------------------------------------------------------------------------------------
def refer_xii(label, morph, extra, *, note):
    """A WHO salivary tumour that ICCC-2017 places in XIIa4 at every site: refer to Group XII
    and name its code (refer_code)."""
    return refer(label, 12,
                 "ICCC-3 codes %s (%s/3) in Group XII (other and unspecified malignant "
                 "neoplasms, subgroup XIIa4), not in Group XI.%s Code the case from the Group XII "
                 "tree." % (term(morph, "3"), morph, (" " + extra) if extra else ""),
                 refer_code=morph, note=note)


def xii_referrals():
    return [
        # ICCR p. 8 image "Myoepithelial carcinoma 8982/3". Evidence code_currency 8982:
        # ICCC-2017 XIIa4; registrar question 2.
        refer_xii("Myoepithelial carcinoma", "8982", "",
                  note="Evidence sg_carcinoma_picker option 17; registrar question 2. ICCC-2017 "
                       "code_lookup 8982 XII XIIa4 000-809."),
        # ICCR p. 8 image "Carcinosarcoma of the salivary glands 8980/3".
        refer_xii("Carcinosarcoma", "8980", "",
                  note="Evidence sg_carcinoma_picker option 18; registrar question 2. ICCC-2017 "
                       "code_lookup 8980 XII XIIa4 000-809."),
        # Rules p. 11 (printed p. 24) "'malignant mixed tumor', and 'adenocarcinoma, NOS'".
        refer_xii("Malignant mixed tumour", "8940",
                  "ICD-O-3.2 gives Mixed tumor, salivary gland type, malignant as a synonym of "
                  "this code.",
                  note="Evidence sg_carcinoma_picker option 19. ICCC-2017 code_lookup 8940 XII "
                       "XIIa4 000-809. Not a WHO 5th-edition entity; ICD-O-3.2 keeps it current."),
    ]


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence sg_document_inventory, sg_cytology)
# ------------------------------------------------------------------------------------------
def gate():
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this salivary gland tumour?",
        # Evidence sg_document_inventory hint; Skalova p. 2 "(FNA) as an initial diagnostic
        # approach, and the Milan". The minor salivary gland sentence is evidence sg_site option
        # 7 (departure 3): Rules p. 11 (printed p. 24) "Neoplasms of the minor salivary glands
        # can be found anywhere in the oral cavity" and "coders should use the topography code
        # for oral cavity, C06.9, which includes".
        hint=("A radiology report counts as imaging. A fine-needle aspiration report counts as "
              "cytology. A pathology report on a biopsy or resection counts as histology. A "
              "cytology or biopsy report that calls the specimen inadequate or non-diagnostic "
              "counts as no tissue. A tumour of a minor salivary gland, in the palate, lip, "
              "cheek, tongue or another part of the mouth or a neighbouring organ, is not coded "
              "to these glands: go back to the site step and record the place where the gland "
              "lies, or mouth, not otherwise specified (C06.9), when the report names none. A "
              "report that calls the tumour possible or suspected does not register it."),
        tier_labels={
            # Evidence sg_document_inventory options 4 and 5. ICCR p. 5 "This dataset is based
            # on histology, but if cytology is the only material available".
            "cytology": "A cytology report (fine-needle aspiration) - no histology report",
            "histology": "A histology report on a biopsy or resection, with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=[
            # Skalova p. 2 "(FNA) as an initial diagnostic approach, and the Milan" (evidence
            # sg_cytology option 1, a named carcinoma type); ICCR p. 8 image "Mucoepidermoid
            # carcinoma 8430/3".
            cyto("Mucoepidermoid carcinoma", "8430",
                 note="Evidence sg_cytology option 1, built per named type (departure 6)."),
            # ICCR p. 8 image "Acinic cell carcinoma 8550/3".
            cyto("Acinic cell carcinoma", "8550",
                 "ICD-O-3.2 gives Acinic cell adenocarcinoma as a synonym of this code.",
                 note="Evidence sg_cytology option 1 (departure 6)."),
            # ICCR p. 8 image "Secretory carcinoma 8502/3" and "Microsecretory carcinoma 8502/3".
            cyto("Secretory carcinoma, or microsecretory adenocarcinoma", "8502",
                 note="Evidence sg_cytology option 1 (departures 6 and 8)."),
            # ICCR p. 8 image "Adenoid cystic carcinoma 8200/3".
            cyto("Adenoid cystic carcinoma", "8200",
                 note="Evidence sg_cytology option 1 (departure 6)."),
            # ICCR p. 8 image "Polymorphous carcinoma 8525/3".
            cyto("Polymorphous adenocarcinoma", "8525",
                 "ICD-O-3.2 gives Polymorphous carcinoma as a synonym of this code.",
                 note="Evidence sg_cytology option 1 (departure 6)."),
            # ICCR p. 8 image "Salivary gland carcinoma NOS and emerging entities 8140/3".
            cyto("Salivary gland carcinoma, not otherwise specified, or adenocarcinoma, not "
                 "otherwise specified", "8140",
                 note="Evidence sg_cytology option 1 (departure 6)."),
            # Evidence sg_cytology option 2 ("Carcinoma, with no type named", 8010/3 basis 5).
            cyto("Cytology names a carcinoma of a type not listed above, or a carcinoma without "
                 "naming its type", "8010",
                 "A type this screen does not list is recorded as the carcinoma code; the "
                 "histology report gives the type its own code.",
                 note="Evidence sg_cytology option 2, widened to the types the screen does not "
                      "list (departure 6; request 1: a cytology picker)."),
            # ICCR p. 8 image "Myoepithelial carcinoma 8982/3", "Carcinosarcoma of the salivary
            # glands 8980/3"; ICCC-2017 XIIa4 at every site.
            refer("Myoepithelial carcinoma, carcinosarcoma or malignant mixed tumour", 12,
                  "ICCC-3 codes Myoepithelial carcinoma (8982/3), Carcinosarcoma, NOS (8980/3) "
                  "and Mixed tumor, malignant, NOS (8940/3) in Group XII (other and unspecified "
                  "malignant neoplasms, subgroup XIIa4), not in Group XI. Code the case from the "
                  "Group XII tree.",
                  note="Departure 6: not in the evidence's cytology screen; added so a cytology "
                       "report naming one of these records no Group XI code."),
            # ICCR p. 4 "Melanomas, lymphomas, and sarcomas are dealt with in separate".
            refer_lymphoma(WHERE),
        ],
        note="Evidence sg_document_inventory and sg_cytology (departures 3 to 6). No laboratory "
             "screen and no marker tier: Visser 2023 Table 4 names no salivary marker "
             "(evidence §§5-6).")


# ------------------------------------------------------------------------------------------
# Histology (evidence sg_histology)
# ------------------------------------------------------------------------------------------
def tail():
    lymphoma_gland = refer_lymphoma(WHERE)
    lymphoma_gland["label"] = "Lymphoma of the salivary gland itself"
    referrals = [
        # Rules p. 2 (printed p. 15) "Code extranodal lymphomas to the site of origin"; ICCR p. 4
        # "Melanomas, lymphomas, and sarcomas are dealt with in separate".
        lymphoma_gland,
        # ICCR p. 9 "intra- and peri-parotid or submandibular gland lymph nodes are commonly
        # present"; the evidence's lymphoma reason ("A lymphoma in a lymph node within or beside
        # the parotid takes a lymph node site").
        refer("Lymphoma in a lymph node within or beside a salivary gland (an intraparotid, "
              "periparotid or submandibular lymph node)", 2,
              "A lymphoma belongs to ICCC-3 Group II. A lymphoma in a lymph node within or "
              "beside a salivary gland is a lymph node lymphoma, coded to the lymph node and not "
              "to the gland (WHO Rule D). Code the case from the Group II (lymphomas) tree at "
              "the lymph node's site.",
              recapture=True,
              note="Departure 13. ICD-O-3.1 Rule D, p. 15. recapture_site: the gland is not the "
                   "lymphoma's site."),
        refer_leukaemia(WHERE),
        # ICCR p. 4 "Melanomas, lymphomas, and sarcomas are dealt with in separate". Evidence
        # conflicts: rhabdomyosarcoma at C07-C08 is IXa; extraosseous Ewing sarcoma 9364 IXd2.
        refer_sarcoma(WHERE, label="Rhabdomyosarcoma or another sarcoma"),
        refer_germ_cell(WHERE),
        refer_other_named(),
    ]
    opts = tail_options(
        P, "mucosa", where=WHERE, nut=True,
        # Evidence sg_histology option 10; Pfister p. 14 "Head and neck tumors Benign Squamous
        # cell papilloma of larynx".
        not_malignant_label="A tumour the report calls benign, borderline or in situ, such as "
                            "pleomorphic adenoma, Warthin tumour, another adenoma, "
                            "myoepithelioma or oncocytoma",
        referrals=referrals, extra_referrals=xii_referrals())
    for o in opts:
        if o.get("next_node") == n("picker"):
            aid(o, AID_PICKER)
        elif o.get("next_node") == n("deposit"):
            # ICCR p. 7 "typically a metastasis from another site"; ICCR p. 9 (see AID_DEPOSIT).
            aid(o, AID_DEPOSIT)
    return opts


def histology():
    opts = [
        # Perez §5 "Regarding histological subtypes, MEC is the most common malignant SGT.";
        # Perez §1 "Pleomorphic adenoma and mucoepidermoid carcinoma are the most frequently
        # observed entities."; Pfister p. 14 "Pleomorphic adenoma Malignant Mucoepidermoid
        # carcinoma Acinic cell carcinoma Sialoblastoma"; ICCR p. 8 image "Mucoepidermoid
        # carcinoma 8430/3". D1: paediatric, common.
        aid(named("Mucoepidermoid carcinoma", "8430", note="D1: Perez-de-Oliveira 2025 §5."),
            AID_MEC),
        # Perez §5 "Notably, AciCC and secretory carcinoma is the second and third most frequent
        # malignant SGT"; Pfister p. 14; ICCR p. 8 image "Acinic cell carcinoma 8550/3".
        aid(named("Acinic cell carcinoma", "8550",
                  "ICD-O-3.2 gives Acinic cell adenocarcinoma as a synonym of this code.",
                  note="D1: Perez-de-Oliveira 2025 §5; Pfister 2022, p. 14. Evidence "
                       "code_currency 8550: the WHO name is not an ICD-O-3.2 term."), AID_ACINIC),
        # Perez §5 (ranking above); ICCR p. 8 image "Secretory carcinoma 8502/3" and
        # "Microsecretory carcinoma 8502/3".
        aid(named("Secretory carcinoma, or microsecretory adenocarcinoma", "8502",
                  "The World Health Organization classification codes microsecretory "
                  "adenocarcinoma 8502/3 (International Collaboration on Cancer Reporting, "
                  "salivary gland dataset, Table 1).",
                  note="D1: Perez-de-Oliveira 2025 §5. Departure 8: the evidence's "
                       "microsecretory picker option merges here."), AID_SECRETORY),
        # Perez §5 "polymorphous adenocarcinoma and ACC are less frequently observed in
        # pediatric patients"; ICCR p. 8 image "Adenoid cystic carcinoma 8200/3".
        aid(named("Adenoid cystic carcinoma", "8200",
                  note="D1: Perez-de-Oliveira 2025 §5 (evidence data gap 2: no paediatric "
                       "count)."), AID_ADCC),
        # Perez §5 (as above); ICCR p. 8 image "Polymorphous carcinoma 8525/3"; Skalova p. 1,
        # p. 7.
        aid(named("Polymorphous adenocarcinoma, classic or cribriform subtype", "8525",
                  "ICD-O-3.2 gives Polymorphous carcinoma as a synonym of this code.",
                  note="D1: Perez-de-Oliveira 2025 §5 (evidence data gap 2)."), AID_PAC),
        # ICCR p. 8 image "Salivary duct carcinoma 8500/3" and "Intraductal carcinoma 8500/2".
        # D1 exception: intraductal carcinoma's code depends on invasion (departure 9).
        aid(go("Salivary duct carcinoma, or intraductal carcinoma", n("duct"),
               note="D1 exception (invasion screen); departure 9."), AID_DUCT),
        # ICCR p. 8 image "Salivary gland carcinoma NOS and emerging entities 8140/3".
        named("Salivary gland carcinoma, not otherwise specified, or adenocarcinoma, not "
              "otherwise specified", "8140", upgrade=TYPE_NOT_STATED,
              note="Evidence sg_histology option 7; the generic option of the screen (evidence "
                   "data gap 7)."),
        named("Carcinoma, with no type named", "8010", upgrade=TYPE_NOT_STATED,
              note="Evidence sg_histology option 8; the generic option of the screen (evidence "
                   "data gap 7)."),
        # Rules p. 1 (printed p. 14) "unless the type of tumor indicates origin from a particular
        # tissue" and "general rule also applies to imprecise phrases such as". Departure 2.
        go("The report places the tumour beside a salivary gland or in its region (for example "
           "periparotid), not in the gland", n("site"),
           note="Departure 2: the Rule B option of evidence sg_site; registrar question 9."),
        # Perez §5 "rare malignant neoplasm primarily diagnosed in the neonatal period or early
        # childhood"; Pfister p. 14; ICCR p. 8 image "Sialoblastoma 8974/1". D6 (departure 10).
        sialoblastoma(),
    ] + tail()
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence sg_histology hint; the Rule K sentence is the evidence's sg_carcinoma_picker
        # hint (Rules p. 3, printed p. 16); registrar questions 4 and 5 (carcinoma ex
        # pleomorphic adenoma).
        "Use the report's final diagnosis. The grade the report gives, and high grade "
        "transformation, do not change the code: choose the carcinoma type the report names. A "
        "carcinoma ex pleomorphic adenoma is recorded as such whatever carcinoma the report "
        "names inside it. When the report names two carcinoma types in one tumour and no option "
        "names both, choose the one with the higher ICD-O code (WHO coding Rule K). Myoepithelial "
        "carcinoma, carcinosarcoma and malignant mixed tumour are coded in Group XII: their "
        "options are at the end of the list.",
        opts, [],
        "Evidence sg_histology (departures 2 and 7 to 15). D1: the paediatric entities are "
        "mucoepidermoid, acinic cell and secretory carcinoma (Perez-de-Oliveira 2025 §5; "
        "Pfister 2022, p. 14), and adenoid cystic carcinoma and polymorphous adenocarcinoma "
        "(Perez-de-Oliveira 2025 §5, observed less often in children). Intraductal carcinoma is "
        "an option because its code needs the invasion answer.")


def sialoblastoma():
    # Registrar, 8 October 2026 (review A11, E10): "I would go with what papers tell here."
    # Pfister 2022 (the WHO classification of paediatric tumours), PDF p. 13, Table 3, lists
    # sialoblastoma under "Malignant" head and neck tumours; Perez-de-Oliveira 2025, PMC section 5,
    # "a rare malignant neoplasm primarily diagnosed in the neonatal period or early childhood".
    # ICCC-2017 holds 8974 only at /3, in XIIa4. ICD-O-3.2 prints 8974/1 only (ICCR p. 8 too).
    return refer("Sialoblastoma", 12,
                 "Sialoblastoma is a malignant tumour of the salivary glands in infants and young "
                 "children (the WHO classification of paediatric tumours). ICCC-3 places "
                 "sialoblastoma (8974) at behaviour 3 in Group XII (other and unspecified malignant "
                 "neoplasms), not Group XI. Code the case from the Group XII tree, as malignant.",
                 refer_code="8974",
                 note="Registrar, 8 October 2026 (review A11, E10). ICD-O-3.2 prints 8974 at /1 "
                      "only; 8974/3 is Group XII's to record (TODO §35.12).")


def duct():
    return node(
        n("duct"), "histology_subclassification", 4, "Duct carcinoma",
        "Which duct carcinoma does the report name?",
        # Skalova p. 7 "Its in situ intraductal nature is demonstrated by an intact surrounding
        # myoepithelial cell"; Rules p. 2 (printed p. 15) "code as the pathologist indicates".
        "An intraductal carcinoma is in situ while its layer of myoepithelial cells is intact. It "
        "is coded as invasive only when the report states invasion or invasive growth (WHO "
        "coding Rule F).",
        [
            # ICCR p. 8 image "Salivary duct carcinoma 8500/3"; Rules p. 10 (printed p. 23)
            # "C07.9 Parotid gland C08._ Salivary gland" (Rule H, Table 23).
            named("Salivary duct carcinoma", "8500",
                  "The World Health Organization classification codes salivary duct carcinoma "
                  "8500/3 (International Collaboration on Cancer Reporting, salivary gland "
                  "dataset, Table 1). ICD-O links this code to the breast, but the salivary "
                  "gland stays the site (WHO coding Rule H).",
                  note="Departure 9: the evidence's picker option."),
            # Skalova p. 2 "frank invasive growth with loss of myoepithelial cells can be seen";
            # Rules p. 2 (printed p. 15) "code as the pathologist indicates".
            named("Intraductal carcinoma, and the report states invasion or invasive growth",
                  "8500",
                  "The report states invasion, so the invasive code is recorded (WHO coding Rule "
                  "F). This awaits the registrar's decision.",
                  note="Evidence sg_not_malignant option 9; registrar question 3."),
            # ICCR p. 8 image "Intraductal carcinoma 8500/2"; Skalova p. 7.
            intraductal_in_situ(),
        ], [],
        "Departure 9. D1 exception: intraductal carcinoma's code depends on invasion. ICD-O-3.2 "
        "prints no salivary duct carcinoma term; the WHO code is 8500/3 (evidence code_currency "
        "8500).")


def intraductal_in_situ():
    return excl("Intraductal carcinoma, with no invasion stated", "8500", "2",
                what="an intraductal carcinoma with no invasion stated",
                extra="ICD-O-3.2 gives Intraductal carcinoma, NOS as a synonym of this code.",
                note="Evidence sg_not_malignant option 8. ICCR p. 8 image 'Intraductal "
                     "carcinoma 8500/2'.")


def site():
    return node(
        n("site"), "site_resolution", 4, "Site of the tumour",
        "Does the tumour's type show that it arose in the salivary gland?",
        # Evidence sg_site option 6 reason; Rules p. 1 (printed p. 14) "unless the type of tumor
        # indicates origin from a particular tissue".
        "The report places the tumour beside the gland or in its region (for example "
        "periparotid, or in the region of the parotid), not in it. Such a tumour is coded to the "
        "gland only when its type shows that it arose there; otherwise it is coded to head, face "
        "or neck, not otherwise specified (C76.0) (WHO coding Rule B).",
        [
            go("Yes: the report names a salivary gland carcinoma type, for example "
               "mucoepidermoid, acinic cell, secretory, adenoid cystic or polymorphous carcinoma, "
               "or calls it a salivary gland carcinoma", n("histology"),
               note="Rule B exception: the type indicates origin in the gland, so the routed site "
                    "stands. Returns to the histology screen, as nut_tests returns."),
            go("No: a carcinoma of another type, such as squamous cell carcinoma, or a carcinoma "
               "whose type the report does not name", UNSPECIFIED_HISTOLOGY,
               captures={"topography": "C76.0"},
               note="Rule B: C76.0, then the unspecified tree's histology screen (cross-tree "
                    "next_node), the deposit node's pattern for C80.9. ICCC-2017 range 136 "
                    "places the shared list at C76.0 in XIf11. group11_tree.trees() defers this "
                    "hop while g11_unspecified has no module."),
        ], ["topography"],
        "Departure 2: the Rule B option of evidence sg_site (registrar question 9). The router "
        "answers the gland itself (D14).")


def not_malignant():
    return not_malignant_node(
        P,
        [
            # Registrar, 8 October 2026 (review A6, E7): Rule F (ICD-O-3.1 printed p. 15). ICCR
            # Major Salivary Glands, PDF pp. 7-8, calls the intracapsular tumour in situ.
            # ICD-O-3.2 prints 8941 at /3 only; the name does not change with the behaviour
            # (build_database.ICDO32_MATRIX_RULE). A report that does not state it in situ keeps
            # 8941/3 from the picker, as the WHO table codes every extent.
            excl("Carcinoma ex pleomorphic adenoma that the report calls in situ, intracapsular "
                 "and non-invasive, or intraductal", "8941", "2",
                 what="a carcinoma ex pleomorphic adenoma the report calls in situ",
                 extra="The pathologist's stated behaviour is recorded (WHO coding Rule F).",
                 note="Registrar, 8 October 2026 (review A6, E7): Rule F; matrix-rule pair."),
            # Perez §5 "Regarding histopathological diagnoses, PA is the most prevalent
            # neoplasm."; ICCR p. 7 "technically considered benign under the recent WHO
            # classification of tumours".
            excl("Pleomorphic adenoma, including metastasizing pleomorphic adenoma", "8940", "0",
                 what="a pleomorphic adenoma",
                 extra="ICD-O-3.2 gives Mixed tumor, salivary gland type, NOS as a synonym of "
                       "this code. A metastasizing pleomorphic adenoma is benign in the WHO "
                       "classification.",
                 note="Evidence sg_not_malignant option 1."),
            # Perez §5 "PA and MEC are the most prevalent. Benign: PA and myoepithelioma.";
            # Skalova p. 2 "myoepithelioma vs myoepithelial carcinoma".
            excl("Myoepithelioma", "8982", "0", what="a myoepithelioma",
                 extra="A myoepithelial carcinoma is coded in Group XII: take its option on the "
                       "histology screen.",
                 note="Evidence sg_not_malignant option 2."),
            # Skalova p. 4 "Warthin tumor, and necrotizing sialometaplasia".
            excl("Warthin tumour", "8561", "0", what="a Warthin tumour",
                 extra="ICD-O-3.2 gives Warthin tumor as a synonym of this code.",
                 note="Evidence sg_not_malignant option 3."),
            # Skalova p. 3 "Basal cell adenoma".
            excl("Basal cell adenoma", "8147", "0", what="a basal cell adenoma",
                 note="Evidence sg_not_malignant option 4."),
            # Skalova p. 4 "duct adenoma, basal cell adenoma, and canalicular adenoma".
            excl("Canalicular adenoma", "8149", "0", what="a canalicular adenoma",
                 note="Evidence sg_not_malignant option 5."),
            # ICCR p. 10 "oncocytic metaplasia, hyperplasia and oncocytoma may be challenging".
            excl("Oncocytoma", "8290", "0", what="an oncocytoma",
                 extra="ICD-O-3.2 gives Oncocytoma as a synonym of this code.",
                 note="Evidence sg_not_malignant option 6."),
            # Skalova p. 3 "Sialadenoma papilliferum".
            excl("Sialadenoma papilliferum", "8406", "0", what="a sialadenoma papilliferum",
                 extra="ICD-O-3.2 gives Sialadenoma papilliferum as a related term of this code.",
                 note="Evidence sg_not_malignant option 7."),
            # ICCR p. 8 image "Intraductal carcinoma 8500/2" (departure 9: also on sg_duct).
            intraductal_in_situ(),
            # Perez §5; Pfister p. 14; ICCR p. 8 image "Sialoblastoma 8974/1" (departure 10).
            sialoblastoma(),
            # Skalova p. 1 "including sclerosing polycystic adenoma, keratocystoma" and "and
            # striated duct adenoma among the benign neoplasms".
            nonrep("Another tumour the report calls benign, borderline or in situ, such as "
                   "sclerosing polycystic adenoma, keratocystoma, intercalated duct adenoma or "
                   "striated duct adenoma",
                   "A tumour the report calls benign, borderline or in situ is not a malignant "
                   "tumour. %s" % OUTSIDE_XI,
                   note="Evidence sg_not_malignant option 10, replacing the common catch-all "
                        "(departure 14)."),
        ],
        where=WHERE, catch_all=False,
        note="The exclusions of evidence sg_not_malignant (departures 9, 10 and 14).")


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), duct(), site()] + nut_nodes(P) + [
        not_malignant(), deposit_node(P, where=WHERE)]
    tree = make_tree(
        TREE_ID, nodes,
        subtype_screens=(n("duct"),),
        # Standing rule 3 (D11): no ICCC-2017 range holds 8407 at C07-C08, and the evidence names
        # it (sclerosing microcystic adenocarcinoma, ICCR p. 8 image; code_currency 8407).
        d11=("8407",),
        # sg_duct offers 8500/3 only as salivary duct and invasive intraductal carcinoma; the
        # picker keeps Infiltrating duct carcinoma, NOS (departure 9).
        picker_keep=("8500",))
    # Registrar ruling of 8 October 2026 on review A1 (a)(b), docs/group_11_evidence/
    # registrar_A1ab_rules.md C6 (a3): a mucinous adenocarcinoma with a signet ring subtype is
    # recorded as 8490/3. ICD-O-3.2 prints Mucinous carcinoma, signet ring cell type as a Synonym
    # of 8490/3 (ICD-O-3.1 section 4.3.3, p. 21); if a coder declines that match, Rule K (p. 24)
    # takes the higher of 8480 and 8490, which is 8490: both routes agree.
    synonym = "Mucinous carcinoma, signet ring cell type"
    assert synonym in live_search_terms("8490", "3"), "ICD-O-3.2 no longer lists %s" % synonym
    for nd in tree["nodes"]:
        if nd["node_id"] == n("picker"):
            nd["hint"] += (" A %s with a signet ring subtype is recorded as %s (8490/3): ICD-O-3.2 "
                           "lists it as %s, and 8490 is the higher code."
                           % (term("8480", "3").lower(), term("8490", "3"), synonym))
    return tree


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
DECISIONS = {
    "8430/3": ("D1, D8", EVIDENCE,
               "Mucoepidermoid carcinoma, the commonest malignant salivary gland tumour of "
               "children and adolescents (Perez-de-Oliveira 2025), on the salivary histology "
               "screen and at basis 5 when cytology names it."),
    "8550/3": ("D1, D8", EVIDENCE,
               "Acinic cell carcinoma (Perez-de-Oliveira 2025; Pfister 2022), recorded as Acinar "
               "cell carcinoma, on the salivary histology screen and at basis 5 when cytology "
               "names it."),
    "8502/3": ("D1, D8", EVIDENCE,
               "Secretory carcinoma (Perez-de-Oliveira 2025) and microsecretory adenocarcinoma, "
               "which the International Collaboration on Cancer Reporting salivary gland "
               "dataset (Table 1) codes 8502/3, on the salivary histology screen, and at basis 5 "
               "when cytology names either."),
    "8200/3": ("D1, D8", EVIDENCE,
               "Adenoid cystic carcinoma, observed less often in children than in adults "
               "(Perez-de-Oliveira 2025), on the salivary histology screen and at basis 5 when "
               "cytology names it."),
    "8525/3": ("D1, D8", EVIDENCE,
               "Polymorphous adenocarcinoma, classic or cribriform subtype (Perez-de-Oliveira "
               "2025; Skalova 2022), on the salivary histology screen and at basis 5 when "
               "cytology names it."),
    "8140/3": ("D8", EVIDENCE,
               "Salivary gland carcinoma, not otherwise specified, or adenocarcinoma, not "
               "otherwise specified (the International Collaboration on Cancer Reporting "
               "salivary gland dataset, Table 1, codes the category 8140/3), on the salivary "
               "histology screen and at basis 5 from cytology."),
    "8010/3": ("D8", EVIDENCE,
               "Salivary gland carcinoma whose type the report does not name: basis 7 on the "
               "histology screen, basis 5 when cytology names a carcinoma without its type or a "
               "type the cytology screen does not list."),
    "8500/3": ("D1", EVIDENCE,
               "Salivary duct carcinoma (the International Collaboration on Cancer Reporting "
               "salivary gland dataset, Table 1, codes it 8500/3; the salivary site stands under "
               "Rule H) and intraductal carcinoma whose report states invasion (Rule F; "
               "registrar question 3), on the salivary duct carcinoma screen."),
    "8023/3": ("D12", "%s, NUT_carcinoma" % EVIDENCE,
               "NUT carcinoma on the salivary tree's NUT screens (D12): basis 8 with a NUTM1 "
               "result, basis 7 on histology with or without a NUT immunostain."),
}
