"""g11_digestive (prefix dg_): carcinomas of the oesophagus, stomach, small intestine, gallbladder
and extrahepatic bile ducts, pancreas and other digestive organs (C15-C17, C23-C26), ICCC-3
subgroup XIf10.

A family tree (contract §4.1, D14). It is built from
docs/group_11_evidence/XIf2_XIf3_digestive.json, from the evidence agent's nodes for these organs
only: dg_document_inventory, dg_marker,
dg_cytology, dg_oesophagus_histology, dg_stomach_histology, dg_small_intestine_histology,
dg_biliary_histology, dg_pancreas_histology, dg_pancreas_ihc, dg_not_malignant_gut,
dg_not_malignant_pancreatobiliary and dg_carcinoma_picker. The appendix and colorectal nodes of
the same file (dg_appendix_histology, dg_net_grade, dg_colorectal_histology) belong to
g11_appendix and g11_colorectal; this module uses only the Ki-67 and mitotic-count aids of
dg_net_grade (departure 9). The builders are build/group11_common.py's; build/group11_organs/
thyroid.py is the exemplar whose shape this module copies.

File names in the comments are the evidence's own:
    Nagtegaal   XIf2-colorectum-XIf3-appendix-XIf10-digestive__Nagtegaal-2019.txt (Nagtegaal ID,
                et al. The 2019 WHO classification of tumours of the digestive system.
                Histopathology 2020;76:182-188)
    ICCR-Oes    XIf10-oesophagus__ICCR-Oesophagus-3rd.txt (ICCR Carcinoma of the Oesophagus,
                3rd edition, version 3.0, December 2025); "image" marks a table page image
    ICCR-Sto    XIf10-stomach__ICCR-Stomach-3rd.txt (ICCR Carcinoma of the Stomach, 3rd edition,
                version 3.0, December 2025)
    Stanley     XIf10-pancreas-solid-pseudopapillary__Stanley-2015.txt (J Diagn Med Sonogr
                2015;31:308-312)
    Ebrahim     XIf10-pancreas-solid-pseudopapillary-paediatric__Ebrahim-2025.txt (Diagn Pathol
                2025); PubMed Central section numbers stand for pages
    Karges      XIf10-pancreas-neuroendocrine-paediatric__Karges-2025.txt (J Neuroendocrinol
                2025); PubMed Central section numbers stand for pages
    Pfister     ALL-paediatric-occurrence__Pfister-2022.txt (Cancer Discov 2022;12:331-355)
    Rules       RULES-A-K__WHO-ICD-O-3-1-manual-extract.txt (ICD-O-3.1 §4, printed pp. 14-28)
    Visser      Visser O, et al. Front Oncol 2023;13:1250549 (contract §0.5; not in the part's
                file set, so the evidence carries no page quotation for it)

Nodes, in tree order:
    dg_document_inventory   document_inventory   evidence gate (evidence dg_document_inventory)
    dg_labs_referral, dg_labs_markers, dg_labs_cytology, dg_labs_histology   lab_results
    dg_clinical, dg_clinical_cytology   clinical_alias
    dg_imaging, dg_imaging_markers, dg_imaging_cytology   morphology_only  (evidence dg_marker)
    dg_cytology             morphology_only      (evidence dg_cytology)
    dg_histology            histology_subclassification  (the five organ screens, merged: D14)
    dg_ihc                  ihc_checklist        (evidence dg_pancreas_ihc and ihc_rules)
    dg_not_malignant        histology_subclassification  (the two exclusion screens, merged)
    dg_deposit              morphology_only      (D10)
    dg_picker               histology_subclassification  (D2; evidence dg_carcinoma_picker)

Departures from the evidence nodes, and why
-------------------------------------------
1. dg_site is not built. The router's site step chooses this tree and records the site, so the
   organ question is one the router already answers (D14). Its appendix, colon, rectum, anus and
   liver answers belong to g11_appendix, g11_colorectal and Group VII, which the router reaches
   by site. Its WHO Rule B and Rule C content moves to the gate's hint: a tumour of the oesophagus
   and stomach is recorded at the cardia (C16.0), a tumour of two digestive organs whose origin
   the report does not give at C26.8, and tissue beside an organ, such as peripancreatic tissue,
   names the retroperitoneum (C48.0), not the organ.
2. dg_document_inventory: the referral and imaging tiers recorded 8000/3 at basis 1 and 2 on the
   gate itself. D7: each routes to its own screen (dg_clinical, dg_imaging), which refers the
   case to Group XII with refer_code 8000, because ICCC-2017 places 8000/3 in XIIb at every routed
   site (evidence conflicts, Group 12). The evidence's "possible, probable or suspected" answer
   is not built: Visser rule 4 registers a tumour stated as probable and leaves only "possible"
   unregistered, which the common clinical and imaging screens apply. The gate's options are the
   contract §4.2 tiers with laboratory copies (registrar, 6 October 2026); the hint drops "Choose
   the strongest evidence the file holds", which the document checklist replaces.
3. dg_marker: a lab_results screen cannot choose a code (registrar, 6 October 2026; Group 10
   lesson). Its eight coded answers move to dg_imaging_markers as marker() options at basis 4,
   each needing imaging that shows the tumour, the raised result and the diagnosis Visser Table 4
   names. "Another raised result, and the imaging report states a malignant tumour" (8000/3 at
   basis 2) is the common "no marker result above registers it" line, which refers to Group XII
   with 8000. "A raised result, and no imaging report shows a tumour" is the common rule 6 line.
   Added, from contract §0.5 (Visser Table 4 read from the page image, 8 October 2026): imaging of
   a tumour of the pancreas, gallbladder or bile ducts with a raised cancer antigen 19-9 refers
   to Group XII with 8000 at basis 4, because Table 4 gives that row 8000/3, not a specific code.
   The dg_labs_* screens record the values. The evidence gives no unit for any test; the unit
   lists are the units laboratories report (registrar to confirm). The evidence calls every
   specimen serum; the adrenocorticotropic hormone row names no specimen, because laboratories
   measure it in plasma. Pancreatic laboratory values have no diagnostic role (Stanley p. 3) and
   have no row.
4. dg_cytology: "A named tumour type" went to the histology screen at basis 5, which the engine
   cannot do: the histology options record basis 7. The three types the evidence names (solid
   pseudopapillary neoplasm, neuroendocrine tumour, adenocarcinoma) are cyto() options at basis 5
   (D8). "Carcinoma, with no type named" is kept and also takes a carcinoma type this list does
   not show, which records Carcinoma, NOS (8010/3) at basis 5, the nearest generic code (D4's
   rule) and the understating direction. "Malignant, with no tumour type named" (8000/3 at
   basis 5) is the common line that refers to Group XII with 8001 (D8). The lymphoma referral
   is kept. "Suspicious for malignancy, atypical, benign or non-diagnostic" is the common
   not-registrable line and the common non-diagnostic routes.
5. The five organ histology screens are one screen, dg_histology (D14: the engine cannot filter
   options by site). Options are grouped by organ and the organ is named in brackets in the
   label: the pancreas first (the paediatric entities, D1), then the gallbladder and bile ducts,
   then the oesophagus, stomach and small intestine. The five "another carcinoma" answers are the
   one picker option, the two "non-invasive lesion" answers the one exclusion option, and the
   duplicated lymphoma, sarcoma, gastrointestinal stromal tumour and deposit answers one each.
   No generic carcinoma option is added: the evidence offers adenocarcinoma, squamous cell
   carcinoma and carcinoma, NOS at these organs only in its picker (no paediatric report, D1), so
   they are D2 picker entries.
6. The trailing options are the common ones (tail_options): melanoma (D13), the picker, the
   exclusion screen, the deposit question (D10), "Malignant tumour, type not determined"
   (Group XII, 8000, D7) and the referrals lymphoma (II, keeps the site, Rule D), leukaemia (I,
   C42.1), sarcoma (IX), teratoma or another germ cell tumour (X) and another named tumour (XII).
   The lymphoma and sarcoma labels keep the evidence's examples. The evidence's deposit referral
   (refer_group null with recapture_site) is the deposit question. NUT carcinoma has no option:
   D12 names no digestive organ, so 8023/3 is a picker entry. Gastroblastoma is not named (D4:
   ICD-O-3.2 holds no 8976; registrar question 2): a report naming it takes "Another malignant
   tumour the report names that is not a carcinoma or melanoma" or "Malignant tumour, type not
   determined", both Group XII.
7. Melanoma (D13): the evidence offered melanoma on the oesophagus, stomach and small intestine
   screens; the one screen hops to me_mucosa at every routed site.
8. The referrals the evidence gives a code carry it as refer_code, which app.js shows as "Code
   there": pancreatoblastoma 8971 (Group XII), gastrointestinal stromal tumour 8936 (Group XII),
   cholangiocarcinoma 8160 and perihilar cholangiocarcinoma 8162 (Group VII). ICCC-2017 places
   each in that group at every routed site; none is a Group XI entry.
9. Recognition aids. The solid pseudopapillary neoplasm aid is the evidence's own. The pancreatic
   neuroendocrine tumour grade options carry dg_net_grade's Ki-67 and mitotic-count aids
   (Nagtegaal p. 4, Table 2, which grades every gastroenteropancreatic neuroendocrine neoplasm),
   and the neuroendocrine carcinoma option carries the aid the evidence's picker gives the same
   entity (Nagtegaal p. 5; ICCR-Sto p. 21).
10. dg_pancreas_ihc: its two fallback answers (8000/3 when the report states a malignant tumour;
   not registrable otherwise) are not buildable on an ihc_checklist, which takes one NOS fallback
   code in this group. The entry option is restricted to "a carcinoma or malignant epithelial
   tumour whose type the report does not name", so the fallback records Carcinoma, NOS (8010/3),
   whose ICD-O-3.2 synonym is Epithelial tumor, malignant. A malignant tumour of undetermined type
   takes the tail's Group XII line, and a tumour the report does not call malignant takes the
   exclusion screen. Marker names are capitalised as the screen shows them ("Beta-catenin
   (nuclear)", the thyroid's spelling).
11. The exclusion screens merge into dg_not_malignant. The two 8148/0 and 8148/2 lines of the gut
   and pancreatobiliary screens are one line each. The low-grade appendiceal mucinous neoplasm
   line (8480/1) is g11_appendix's. "(oesophagus or anus)" becomes "(oesophagus)": the anus is
   g11_colorectal's. The evidence's Rule F hint (go back for an invasive tumour) is appended to
   the common hint. "Another benign lesion" is the common catch-all.
12. dg_carcinoma_picker: D2 replaces the evidence's curated picker. Labels are ICD-O-3.2
   Preferred terms with live synonyms as search_terms and no recognition aid (Group 10's picker
   shape), so the evidence's picker labels and aids (mucinous adenocarcinoma, signet ring cell,
   hepatoid, goblet cell, adenosquamous, mixed neuroendocrine non-neuroendocrine neoplasm, the
   ductal adenocarcinoma "of the pancreas" label) are not shown; the build report lists them.
   The app.js filter matches every typed word anywhere in the label and search terms, so
   "ductal adenocarcinoma" finds Infiltrating duct carcinoma, NOS (8500/3) through its synonyms
   and the evidence's Rule J hint is not needed. The picker keeps every code the histology
   screen offers only under a pancreas label whose ICD-O-3.2 Preferred term does not itself name
   the pancreas (picker_keep): 8151, 8152, 8153, 8155, 8156, 8240, 8246, 8249 and 8550. The hint
   tells the clerk to take a bracketed organ option only at that organ, so the same tumour at
   another organ needs a route; the evidence keeps 8153, 8156, 8240, 8246 and 8249 as picker
   entries at the other organs. 8150 and 8452 stay off the picker: their terms name the pancreas
   (WHO coding Rule H).
13. Not built from the evidence: gastroblastoma 8976 (D4), 8512/3, 8245/3 and 8124/3 (D3), the
   ICCR's 8213/2 and 8144/2 (D4), and a Rule F stated-behaviour code for a solid pseudopapillary
   neoplasm called benign (D6, registrar question 6): the option records ICD-O-3.2's 8452/3 and
   says so.

Registrar questions the evidence raised (XIf2_XIf3_digestive.json, questions 2, 3, 5, 6, 7, 8
and 9 bear on these organs) stay open; the defaults above apply until they are answered.
"""
from __future__ import annotations

from group11_common import (aid, cyto, deposit_node, evidence_gate, excl, go, ihc_node, lab,
                            make_tree, marker, named, node, not_malignant_node, refer,
                            refer_germ_cell, refer_leukaemia, refer_lymphoma, refer_other_named,
                            refer_sarcoma, refer_unspecified, rule, tail_options, term, VISSER)

TREE_ID = "g11_digestive"
P = "dg_"
WHERE = "the digestive organs"
EVIDENCE = "XIf2_XIf3_digestive"
VISSER_NOTE = ("Visser O, et al. Front Oncol 2023;13:1250549, Table 4, p. 06, read from the page "
               "image (contract §0.5), with rule 6, p. 05.")


def n(name: str) -> str:
    return P + name


# ------------------------------------------------------------------------------------------
# Recognition aids (clerk-facing; the source is the comment above each)
# ------------------------------------------------------------------------------------------
# Stanley p. 2 "monomorphic epithelioid cells with round nuclei", "surrounded by a delicate
# fibrovascular network"; Stanley p. 3 "Beta-catenin nuclear immunoreactivity of tumor cells".
AID_SPN = ("Reports describe uniform epithelioid cells around a delicate fibrovascular network, "
           "with nuclear staining for beta-catenin.")
# Nagtegaal p. 4 (Table 2) "NET, G1 Well differentiated Low <2 <3%" (evidence dg_net_grade
# grade 1 aid).
AID_NET_G1 = ("A grade 1 tumour has a Ki-67 index below 3% and fewer than 2 mitoses per 2 mm². "
              "A report that gives no grade also takes this option.")
# Nagtegaal p. 4 (Table 2) "NET, G2 Intermediate 2-20 3-20%" and "NET, G3 High >20 >20%";
# Nagtegaal p. 5 "well-differentiated NETs may be high grade" (evidence dg_net_grade aids).
AID_NET_G2_G3 = ("Grade 2 has a Ki-67 index from 3% to 20%, or 2 to 20 mitoses per 2 mm². Grade 3 "
                 "has a Ki-67 index above 20%, or more than 20 mitoses per 2 mm², in a tumour the "
                 "report still calls well differentiated.")
# Nagtegaal p. 5 "NECs are no longer graded"; ICCR-Sto p. 21 "usually applying synaptophysin and
# chromogranin A as a minimum"; ICCR-Oes p. 19 "applying synaptophysin and chromogranin A as a
# minimum" (evidence dg_carcinoma_picker, neuroendocrine carcinoma aid).
AID_NEC = ("Reports describe a poorly differentiated, high-grade carcinoma that stains for "
           "synaptophysin and chromogranin A; the report gives it no grade.")


# ------------------------------------------------------------------------------------------
# The evidence gate (evidence dg_document_inventory, dg_marker, dg_cytology)
# ------------------------------------------------------------------------------------------
def _markers():
    """The Visser Table 4 rows that concern the digestive organs (D7): chromogranin A and the
    seven functioning neuroendocrine tumour hormones, each at basis 4; and cancer antigen 19-9,
    which Table 4 gives 8000/3, a Group XII code at these sites."""
    # Evidence tissue_free rows 3 to 10 and dg_marker options 1 to 8; Visser Table 4, p. 06.
    rows = [
        ("8240", "serum chromogranin A", "neuroendocrine tumour",
         "a neuroendocrine tumour", "tissue_free row 3, dg_marker option 1 (Neuroendocrine "
         "tumour, chromogranin A)"),
        ("8151", "serum insulin",
         "functioning neuroendocrine tumour that secretes insulin (insulinoma)",
         "an insulinoma", "tissue_free row 4, dg_marker option 2 (functioning neuroendocrine "
         "tumours, insulin)"),
        ("8152", "serum glucagon",
         "functioning neuroendocrine tumour that secretes glucagon (glucagonoma)",
         "a glucagonoma", "tissue_free row 5, dg_marker option 3 (glucagon)"),
        ("8153", "serum gastrin",
         "functioning neuroendocrine tumour that secretes gastrin (gastrinoma)",
         "a gastrinoma", "tissue_free row 6, dg_marker option 4 (gastrin)"),
        ("8155", "serum vasoactive intestinal peptide",
         "functioning neuroendocrine tumour that secretes vasoactive intestinal peptide "
         "(VIPoma)", "a VIPoma, a tumour that secretes vasoactive intestinal peptide",
         "tissue_free row 7, dg_marker option 5 (vasoactive intestinal peptide)"),
        ("8156", "serum somatostatin",
         "functioning neuroendocrine tumour that secretes somatostatin (somatostatinoma)",
         "a somatostatinoma", "tissue_free row 8, dg_marker option 6 (somatostatin)"),
        ("8241", "serum serotonin", "functioning neuroendocrine tumour that secretes serotonin",
         "a serotonin-producing neuroendocrine tumour",
         "tissue_free row 9, dg_marker option 7 (serotonin)"),
        ("8158", "adrenocorticotropic hormone",
         "functioning neuroendocrine tumour that secretes adrenocorticotropic hormone",
         "a neuroendocrine tumour that secretes adrenocorticotropic hormone",
         "tissue_free row 10, dg_marker option 8 (adrenocorticotropic hormone). D16 keeps "
         "8158/3 off the adrenal cortex screens; here it is the functioning neuroendocrine "
         "tumour Visser's row names"),
    ]
    opts = [marker(code_, test=test, diagnosis=diagnosis, where="of the digestive organs",
                   label="Imaging shows the tumour, the report calls %s raised, and the file "
                         "calls it %s" % (test, called),
                   note="%s Evidence %s." % (VISSER_NOTE, cite))
            for code_, test, diagnosis, called, cite in rows]
    # Contract §0.5: Visser Table 4 (page image, 8 October 2026) gives pancreatic and gallbladder
    # or bile duct cancer with cancer antigen 19-9 the code 8000/3 at basis 4, not a specific
    # code; ICCC-2017 range 143 places 8000/3 in XIIb at these sites. Not in the evidence file.
    opts.append(refer_unspecified(
        "Imaging shows a tumour of the pancreas, gallbladder or bile ducts, and the report calls "
        "cancer antigen 19-9 raised", "8000", 4,
        "A pancreatic, gallbladder or bile duct cancer shown on imaging with a raised cancer "
        "antigen 19-9 is registered without a tumour type (%s, Table 4)." % VISSER,
        where=WHERE,
        captures={"workup_status": "incomplete", "basis_evidence_tier": "markers_ca19_9"},
        note="D7 and contract §0.5: Visser 2023 Table 4, p. 06 (pancreatic and gallbladder or "
             "bile duct cancer, cancer antigen 19-9, 8000/3), read from the page image. "
             "ICCC-2017 range 143 holds 8000/3 in XIIb at this tree's sites."))
    return opts


def gate():
    return evidence_gate(
        P, where=WHERE,
        question="What is in the file for this digestive tumour?",
        # Rules PDF p. 5 (printed p. 18) "is specifically indexed to C16.0 (cardia)" and "should
        # be assigned to C26.8, overlapping lesion of digestive system"; Rules PDF p. 4 (printed
        # p. 17) "are listed and given the code number C48.0" (evidence dg_site, departure 1).
        hint=("A radiology report counts as imaging. A pathology report on a biopsy or resection "
              "counts as histology. A biopsy or cytology report that calls the specimen "
              "inadequate or non-diagnostic counts as no tissue. A tumour of the oesophagus and "
              "stomach together is recorded at the cardia (C16.0). A tumour of two digestive "
              "organs whose origin the report does not give, such as the stomach and small "
              "intestine, is recorded at overlapping lesion of the digestive system (C26.8). A "
              "report that names only the tissue beside an organ, such as peripancreatic "
              "tissue, does not name that organ: that tissue is the retroperitoneum (C48.0). If "
              "the site recorded does not follow these rules, go back to the site step. A "
              "report that calls the tumour possible or suspected does not register it."),
        # Evidence lab_tests rows 1 and 2 (the registrar's Visser Table 4 rule) and contract
        # §0.5 (cancer antigen 19-9). The evidence prints no unit (departure 3).
        labs=[
            lab("chromogranin_a", "Serum chromogranin A", ("ng/mL", "µg/L", "nmol/L")),
            lab("insulin", "Serum insulin", ("µIU/mL", "mU/L", "pmol/L")),
            lab("glucagon", "Serum glucagon", ("pg/mL", "ng/L", "pmol/L")),
            lab("gastrin", "Serum gastrin", ("pg/mL", "ng/L", "pmol/L")),
            lab("vasoactive_intestinal_peptide", "Serum vasoactive intestinal peptide",
                ("pg/mL", "ng/L", "pmol/L")),
            lab("somatostatin", "Serum somatostatin", ("pg/mL", "ng/L", "pmol/L")),
            lab("serotonin", "Serum serotonin", ("ng/mL", "µg/L", "nmol/L")),
            lab("adrenocorticotropic_hormone", "Adrenocorticotropic hormone",
                ("pg/mL", "ng/L", "pmol/L")),
            lab("cancer_antigen_19_9", "Cancer antigen 19-9 (CA 19-9)", ("U/mL", "kU/L")),
        ],
        marker_tests="chromogranin A, hormone or cancer antigen 19-9",
        markers=_markers(),
        tier_labels={
            "imaging": "An imaging report only (ultrasound, CT or MRI) - no chromogranin A, "
                       "hormone or cancer antigen 19-9 result, no tissue",
            "cytology": "A cytology report (fine-needle aspiration or brushings) - no histology "
                        "report",
            "histology": "A histology report on a biopsy or resection, with or without "
                         "immunohistochemistry or gene reports",
        },
        cytology=[
            # Evidence dg_cytology option 1 ("such as solid pseudopapillary neoplasm,
            # neuroendocrine tumour or adenocarcinoma"); departure 4.
            cyto("Solid pseudopapillary neoplasm (pancreas)", "8452",
                 note="Evidence dg_cytology option 1, the first type it names."),
            cyto("Neuroendocrine tumour, with grade 1 or no grade stated", "8240",
                 note="Evidence dg_cytology option 1, the second type it names."),
            cyto("Adenocarcinoma", "8140",
                 note="Evidence dg_cytology option 1, the third type it names."),
            # Evidence dg_cytology option 2 ("Carcinoma, with no type named"); departure 4.
            cyto("Cytology names a carcinoma without naming its type, or names a carcinoma type "
                 "this list does not show", "8010",
                 "A carcinoma type this list does not show is recorded at this code from "
                 "cytology; the histology report gives that type's own code.",
                 note="Evidence dg_cytology option 2, widened to a named type the list lacks "
                      "(the nearest generic code, as D4 rules for an entity without a code)."),
            # Evidence dg_cytology option 4.
            refer_lymphoma(WHERE),
        ],
        note="Evidence dg_document_inventory and dg_marker (departures 2 and 3 in the module "
             "docstring).")


# ------------------------------------------------------------------------------------------
# Histology (evidence dg_pancreas_histology, dg_biliary_histology, dg_stomach_histology,
# dg_oesophagus_histology, dg_small_intestine_histology), one screen (D14)
# ------------------------------------------------------------------------------------------
def _refer_coded(label, group, code_, note, *, synonyms="", sites="", extra=""):
    """A referral that names the code the other group records (departure 8). ICCC-2017 holds
    each of these codes at C00.0-C80.9 (000-809) in the one group named."""
    groups = {7: "Group VII (hepatic tumours)",
              12: "Group XII (other and unspecified malignant neoplasms)"}
    trees = {7: "the Group VII (hepatic tumours) tree", 12: "the Group XII tree"}
    reason = ("ICD-O-3.2 codes it as %s (%s/3)%s. ICCC-3 places that code in %s at every site%s, "
              "not in Group XI.%s Code the case from %s."
              % (term(code_, "3"), code_, synonyms, groups[group], sites,
                 (" " + extra) if extra else "", trees[group]))
    return refer(label, group, reason, refer_code=code_, note=note)


def _pancreas():
    return [
        # Karges PMC section 1 "Nonfunctional tumors predominated (75%)."; section 11 "the
        # predominance of nonfunctional panNETs (75%) diverges from the literature". D1.
        named("Non-functioning pancreatic neuroendocrine tumour, or islet cell tumour "
              "(pancreas)", "8150",
              "ICD-O-3.2 gives Pancreatic endocrine tumor, nonfunctioning as a synonym of this "
              "code.",
              note="D1: Karges 2025 (28 patients under 18). Evidence code currency: the label "
                   "names islet cell tumour so an older report finds the current code."),
        # Karges section 2 "Among pediatric panNETs, insulinomas predominate"; section 7
        # "insulinomas constituted the majority with four cases". D1.
        named("Insulinoma (pancreas)", "8151",
              note="D1: Karges 2025. Currency check §3: 8151 moved from /0 to /3."),
        # Pfister p. 13 "Pancreas Epithelial tumors Pancreatoblastoma Pancreatic acinar cell
        # carcinoma Solid pseudopapillary neoplasm"; Stanley p. 2, p. 3; Ebrahim section 13
        # "Among the pediatric cases (n = 4)". D1. D6 and registrar question 6: a report calling
        # it benign keeps ICD-O-3.2's 8452/3.
        aid(named("Solid pseudopapillary neoplasm, or solid pseudopapillary tumour (pancreas)",
                  "8452",
                  "ICD-O-3.2 gives the pancreatic tumour behaviour 3, so a report that calls it "
                  "benign or of low malignant potential does not change the code. This awaits "
                  "the registrar's decision.",
                  note="D1: Pfister 2022, p. 13; Stanley 2015; Ebrahim 2025. D6; registrar "
                       "question 6. Currency check §3: 8452/3 is the pancreas only; the ovary "
                       "is 8452/1, Group X's site."), AID_SPN),
        # Pfister p. 13 (as above). D1.
        named("Acinar cell carcinoma (pancreas)", "8550",
              note="D1: Pfister 2022, p. 13 (evidence 'left as they were': no 8 October paper "
                   "reports it in a child)."),
        # Karges section 8 "one had a grade 1 tumor, and the other had a grade 2"; section 9
        # "well-differentiated, grade 1-3 NETs in 18 of 25 patients". D1.
        aid(named("Neuroendocrine tumour, grade 1, or with no grade stated (pancreas)", "8240",
                  "ICD-O-3.2 lists Neuroendocrine tumor, grade 1 under this code.",
                  note="D1: Karges 2025. Aid from evidence dg_net_grade (departure 9)."),
            AID_NET_G1),
        # Karges section 9 (as above); section 8 "six had grade 2, eight had grade 3 tumors". D1.
        aid(named("Neuroendocrine tumour, grade 2 or grade 3, well differentiated (pancreas)",
                  "8249",
                  "ICD-O-3.2 lists Neuroendocrine tumor, grade 3 under this code.",
                  note="D1: Karges 2025. Aid from evidence dg_net_grade (departure 9)."),
            AID_NET_G2_G3),
        # Karges section 9 "Poorly differentiated neuroendocrine carcinomas were identified in
        # seven patients". D1.
        aid(named("Neuroendocrine carcinoma, poorly differentiated, with no small cell or large "
                  "cell type named (pancreas)", "8246",
                  note="D1: Karges 2025. Aid from evidence dg_carcinoma_picker (departure 9)."),
            AID_NEC),
        # Karges section 7 "while gastrinoma was diagnosed in one"; section 2 "Gastrinomas
        # follow, constituting 20%-30% of functional panNETs". D1.
        named("Gastrinoma (pancreas)", "8153",
              note="D1: Karges 2025. Currency check §3: 8153 moved from /1 to /3."),
        # Karges section 2 "Less common functional variants, including glucagonomas, VIPomas,
        # and somatostatinomas, each contribute less than 10%". D1.
        named("Glucagonoma (pancreas)", "8152", note="D1: Karges 2025."),
        named("VIPoma, a tumour that secretes vasoactive intestinal peptide (pancreas)", "8155",
              note="D1: Karges 2025."),
        named("Somatostatinoma (pancreas)", "8156", note="D1: Karges 2025."),
        # Pfister p. 11 "Pancreatoblastoma, which is extremely rare, occurs predominantly in the
        # first decade of life". ICCC-2017: 8971 XIIa2 at C25.0-C25.9.
        _refer_coded("Pancreatoblastoma (pancreas)", 12, "8971",
                     "Evidence dg_pancreas_histology; conflicts, Group 12. Pfister 2022, p. 11."),
        # Evidence dg_pancreas_histology option 13 -> dg_pancreas_ihc (departure 10).
        go("A carcinoma or malignant epithelial tumour whose type the report does not name, "
           "with immunohistochemistry results (pancreas)", n("ihc"),
           note="Evidence dg_pancreas_histology option 13 (departure 10)."),
    ]


def _biliary():
    return [
        # Rules PDF p. 11 (printed p. 24) "(8160/3) is a specific histologic type" and "therefore
        # should not be automatically coded to C24.0". ICCC-2017: 8160 VIIb at every site.
        # Registrar question 5.
        _refer_coded("Cholangiocarcinoma, bile duct carcinoma or bile duct adenocarcinoma "
                     "(gallbladder or bile ducts)", 7, "8160",
                     "Evidence dg_biliary_histology option 1; conflicts, Group 7; registrar "
                     "question 5. Rules PDF p. 11 (printed p. 24).",
                     synonyms=", and gives bile duct carcinoma and bile duct adenocarcinoma as "
                              "synonyms",
                     sites=", the gallbladder and the extrahepatic bile ducts included",
                     extra="Bile duct carcinoma names a tumour type, not a site: the case keeps "
                           "the site the report states (WHO coding Rule H)."),
        # ICCC-2017: 8162 VIIb at every site. icdo32.sqlite 8162/3 Synonym Klatskin tumor [obs]:
        # the label keeps the report's word (evidence dg_biliary_histology option 2).
        _refer_coded("Perihilar cholangiocarcinoma, or Klatskin tumour (bile ducts)", 7, "8162",
                     "Evidence dg_biliary_histology option 2; conflicts, Group 7."),
    ]


def _gut():
    return [
        # Pfister p. 9 "Pediatric gastrointestinal stromal tumor (GIST)". ICCC-2017: 8936 XIIa1
        # at every routed site.
        _refer_coded("Gastrointestinal stromal tumour (oesophagus, stomach or small intestine)",
                     12, "8936",
                     "Evidence dg_oesophagus_histology, dg_stomach_histology and "
                     "dg_small_intestine_histology option 4; conflicts, Group 12. Pfister 2022, "
                     "p. 9."),
    ]


def histology():
    lymphoma = refer_lymphoma(WHERE)
    # Pfister p. 6 "high-grade B-cell lymphomas (particularly Burkitt lymphoma)".
    lymphoma["label"] = "Lymphoma, such as Burkitt lymphoma"
    opts = _pancreas() + _biliary() + _gut() + tail_options(
        P, "mucosa", where=WHERE,
        referrals=[
            lymphoma,
            refer_leukaemia(WHERE),
            # Nagtegaal p. 3 "EWSR1 fusions in gastrointestinal clear cell sarcoma and malignant
            # gastrointestinal neuroectodermal tumour". ICCC-2017: 8900 IXa, 9044 IXd7.
            refer_sarcoma(WHERE, label="A sarcoma, such as rhabdomyosarcoma or clear cell "
                                       "sarcoma"),
            # ICCC-2017: 9080, 9071 and 9064 Group X at every routed site (evidence conflicts,
            # Group 10: a yolk sac tumour of the stomach is named by the report).
            refer_germ_cell(WHERE),
            refer_other_named(),
        ])
    return node(
        n("histology"), "histology_subclassification", 3, "Tumour type",
        "What does the histology report call the tumour?",
        # Evidence dg_pancreas_histology hint (Rule K), dg_biliary_histology hint (Rule H) and
        # dg_net_grade hint (Rule G); Rules PDF p. 2-3 (printed pp. 15-16).
        "Use the report's final diagnosis. An option that names an organ in brackets belongs to "
        "that organ: take it only when the site recorded is that organ. When the report gives "
        "two terms for one tumour and no single option covers both, choose the one with the "
        "higher code (WHO coding Rule K). A grade given together with a hormone type or with "
        "non-functioning records the grade, whose code is the higher: grade 1 is 8240, grade 2 "
        "or grade 3 is 8249, and the hormone types and non-functioning tumour are 8150 to 8156. "
        "When the report gives two grades, or the Ki-67 index and the mitotic count point to "
        "different grades, choose the higher grade. Bile duct carcinoma names a tumour type, "
        "not a site: keep the site the report states (WHO coding Rule H).",
        opts, [],
        "Evidence dg_pancreas_histology, dg_biliary_histology, dg_stomach_histology, "
        "dg_oesophagus_histology and dg_small_intestine_histology, merged (D14; departures 5 to "
        "8). D1: the paediatric entities are the pancreatic neuroendocrine tumours and "
        "neuroendocrine carcinoma (Karges 2025), solid pseudopapillary neoplasm (Pfister 2022, "
        "p. 13; Stanley 2015; Ebrahim 2025), acinar cell carcinoma (Pfister 2022, p. 13), "
        "pancreatoblastoma (Group XII) and gastrointestinal stromal tumour (Group XII). The "
        "oesophageal, gastric, small-bowel and biliary carcinomas have no paediatric report "
        "(evidence data gap 1) and are picker entries. D5: the Rule K sentence on a grade with a "
        "hormone type is registrar question 8. Rule G: Nagtegaal 2020, Table 2 footnote, p. 4.")


def ihc():
    return ihc_node(
        P,
        [
            {"group_label": "Solid pseudopapillary neoplasm",
             "markers": ["Beta-catenin (nuclear)"]},
            {"group_label": "Neuroendocrine and acinar cell markers",
             "markers": ["Chromogranin", "Trypsin"]},
        ],
        [
            rule(["Beta-catenin (nuclear)"], "8452",
                 "Nuclear beta-catenin is positive, and chromogranin and trypsin are not: the "
                 "solid pseudopapillary neoplasm pattern (Stanley 2015, pp. 2-3). %s"
                 % ("Recorded as %s (8452/3)." % term("8452", "3")),
                 negative=["Chromogranin", "Trypsin"],
                 note="Evidence ihc_rules 1 (dg_pancreas_ihc). Stanley p. 2 'nonreactive toward "
                      "chromogranin and trypsin, thus confirming a solid pseudopapillary "
                      "tumor'; Stanley p. 3 'Beta-catenin nuclear immunoreactivity of tumor "
                      "cells'. Stanley p. 3's 'anti-trypsin' positive stain is a different "
                      "antigen and is not a marker here (evidence §4)."),
        ],
        fallback="8010",
        fallback_reason=("The stains do not establish the tumour's type. Recorded as %s (8010/3), "
                         "the code ICD-O-3.2 gives a malignant epithelial tumour whose type is "
                         "not named." % term("8010", "3")),
        hint="The histology report calls the pancreatic tumour a carcinoma or malignant "
             "epithelial tumour without naming its type. Answer each stain as positive or "
             "negative, and 'Not done or not readable' for a stain the report does not mention. "
             "Immunohistochemistry is read with the histology report; it does not replace it.",
        note="Evidence dg_pancreas_ihc and ihc_rules (departure 10). No file in this part gives "
             "markers that separate acinar cell carcinoma, pancreatoblastoma or a pancreatic "
             "neuroendocrine tumour (evidence data gap 3); a solid pseudopapillary neoplasm "
             "without nuclear beta-catenin (Ebrahim 2025, section 13) has no rule (data gap 9).")


def not_malignant():
    nm = not_malignant_node(
        P,
        [
            # ICCR-Oes p. 12 "Oesophageal squamous intraepithelial neoplasia (dysplasia), low
            # grade 8077/0".
            excl("Squamous dysplasia or squamous intraepithelial neoplasia, low grade "
                 "(oesophagus)", "8077", "0",
                 what="a low-grade squamous dysplasia or squamous intraepithelial neoplasia"),
            # Nagtegaal p. 2 "Anal squamous dysplasia"; evidence code currency: ICCR-Oes Table 1
            # prints 8077/2 against "low grade", a printing error; ICD-O-3.2 8077/2 is high
            # grade.
            excl("Squamous dysplasia or squamous intraepithelial neoplasia, high grade "
                 "(oesophagus)", "8077", "2",
                 what="a high-grade squamous dysplasia or squamous intraepithelial neoplasia"),
            # ICCR-Oes p. 12 "Squamous cell papilloma not otherwise specified (NOS) 8052/0".
            excl("Squamous cell papilloma (oesophagus)", "8052", "0",
                 what="a squamous cell papilloma"),
            # ICCR-Oes p. 12 "Squamous papillomatosis 8060/0".
            excl("Squamous papillomatosis (oesophagus)", "8060", "0",
                 what="squamous papillomatosis"),
            # ICCR-Oes p. 12 "Oesophageal glandular dysplasia (intraepithelial neoplasia), low
            # grade 8148/0"; Nagtegaal p. 2 "'intra-epithelial neoplasia' is preferred for those
            # in the pancreas, gallbladder and biliary tree". Two evidence lines merged.
            excl("Glandular dysplasia or intraepithelial neoplasia, low grade, including "
                 "pancreatic or biliary intraepithelial neoplasia, low grade", "8148", "0",
                 what="a low-grade glandular dysplasia or intraepithelial neoplasia"),
            # ICCR-Oes p. 12 "... high grade 8148/2"; Nagtegaal p. 2 (as above). Registrar
            # question 9: gastric high-grade dysplasia records 8148/2.
            excl("Glandular dysplasia or intraepithelial neoplasia, high grade, including "
                 "pancreatic or biliary intraepithelial neoplasia, high grade", "8148", "2",
                 what="a high-grade glandular dysplasia or intraepithelial neoplasia",
                 note="Registrar question 9 (8213/2 and 8144/2 are not ICD-O-3.2 codes)."),
            # ICCR-Sto p. 14 image "Adenomatous polyp, low-grade dysplasia 8210/0*".
            excl("Adenomatous polyp, or adenoma with low-grade dysplasia", "8210", "0",
                 what="an adenomatous polyp"),
            # Nagtegaal p. 3 "conventional adenomas and serrated precursor lesions".
            excl("Tubular adenoma", "8211", "0", what="a tubular adenoma"),
            # Nagtegaal p. 3 "the recently renamed sessile serrated lesion (formerly called
            # sessile serrated polyp/adenoma)".
            excl("Sessile serrated lesion, serrated adenoma or serrated polyp", "8213", "0",
                 what="a serrated lesion or serrated adenoma"),
            # ICCR-Sto p. 14 image "Intestinal-type adenoma, low grade 8144/0*".
            excl("Intestinal-type adenoma (stomach or small intestine)", "8144", "0",
                 what="an intestinal-type adenoma"),
            # Nagtegaal p. 6 "Lynch syndrome and familial adenomatous polyposis"; Pfister p. 19
            # "APC-associated polyposis syndromes".
            excl("Familial adenomatous polyposis, or multiple adenomatous polyps, with no "
                 "carcinoma", "8220", "0", what="familial adenomatous polyposis",
                 extra="A carcinoma arising in it is found under another carcinoma the report "
                       "names."),
            # Nagtegaal p. 2 "Use of the term 'carcinoma in situ' is not recommended".
            excl("High-grade dysplasia, or carcinoma in situ, in a polyp", "8210", "2",
                 what="high-grade dysplasia or carcinoma in situ in a polyp"),
            # Nagtegaal p. 6 "neoplasms are now classified into two tiers of dysplasia".
            excl("Intraductal papillary mucinous neoplasm with low-grade dysplasia (pancreas)",
                 "8453", "0",
                 what="an intraductal papillary mucinous neoplasm with low-grade dysplasia"),
            excl("Intraductal papillary mucinous neoplasm with high-grade dysplasia (pancreas)",
                 "8453", "2",
                 what="an intraductal papillary mucinous neoplasm with high-grade dysplasia"),
            excl("Mucinous cystic neoplasm with low-grade dysplasia (pancreas)", "8470", "0",
                 what="a mucinous cystic neoplasm with low-grade dysplasia"),
            excl("Mucinous cystic neoplasm with high-grade dysplasia (pancreas)", "8470", "2",
                 what="a mucinous cystic neoplasm with high-grade dysplasia"),
        ],
        where=WHERE,
        note="Evidence dg_not_malignant_gut and dg_not_malignant_pancreatobiliary, merged "
             "(departure 11).")
    # Evidence dg_not_malignant_gut and dg_not_malignant_pancreatobiliary hints (Rule F,
    # Rules PDF p. 2, printed p. 15).
    nm["hint"] += (" If the report states invasion or an associated invasive carcinoma, or calls "
                   "the lesion malignant, go back and choose the invasive tumour.")
    return nm


# ------------------------------------------------------------------------------------------
# Assembly
# ------------------------------------------------------------------------------------------
def build(tree_id: str = TREE_ID) -> dict:
    assert tree_id == TREE_ID, tree_id
    nodes = gate() + [histology(), ihc(), not_malignant(), deposit_node(P, where=WHERE)]
    # D2: the histology screen offers these only under a pancreas label, and their Preferred
    # terms do not name the pancreas, so the picker keeps them for the other organs (departure
    # 12). 8150 and 8452 name the pancreas and stay off the picker.
    return make_tree(TREE_ID, nodes, picker_keep=("8151", "8152", "8153", "8155", "8156", "8240",
                                                  "8246", "8249", "8550"))


# ------------------------------------------------------------------------------------------
# Annotations for the generator (contract §2 item 6): every pair the tree emits outside its
# picker. (D-numbers, evidence file, sentence[, overrides]).
# ------------------------------------------------------------------------------------------
_IHC = ["Histology", "IHC"]
DECISIONS = {
    "8150/3": ("D1", EVIDENCE,
               "Non-functioning pancreatic neuroendocrine tumour on the digestive histology "
               "screen (Karges 2025: 75% of pancreatic neuroendocrine tumours under 18)."),
    "8151/3": ("D1, D2, D7", EVIDENCE,
               "Insulinoma of the pancreas on the digestive histology screen (Karges 2025) and in "
               "the digestive picker for the other organs, and at basis 4 with imaging and a "
               "raised serum insulin (Visser 2023 Table 4)."),
    "8152/3": ("D1, D2, D7", EVIDENCE,
               "Glucagonoma of the pancreas on the digestive histology screen (Karges 2025) and "
               "in the digestive picker for the other organs, and at basis 4 with imaging and a "
               "raised serum glucagon (Visser 2023 Table 4)."),
    "8153/3": ("D1, D2, D7", EVIDENCE,
               "Gastrinoma of the pancreas on the digestive histology screen (Karges 2025) and in "
               "the digestive picker for the other organs, and at basis 4 with imaging and a "
               "raised serum gastrin (Visser 2023 Table 4)."),
    "8155/3": ("D1, D2, D7", EVIDENCE,
               "VIPoma of the pancreas on the digestive histology screen (Karges 2025) and in the "
               "digestive picker for the other organs, and at basis 4 with imaging and a raised "
               "serum vasoactive intestinal peptide (Visser 2023 Table 4)."),
    "8156/3": ("D1, D2, D7", EVIDENCE,
               "Somatostatinoma of the pancreas on the digestive histology screen (Karges 2025) "
               "and in the digestive picker for the other organs, and at basis 4 with imaging "
               "and a raised serum somatostatin (Visser 2023 Table 4)."),
    "8158/3": ("D2, D7, D16", EVIDENCE,
               "ACTH-producing tumor at basis 4 with imaging and a raised adrenocorticotropic "
               "hormone, the functioning neuroendocrine tumour row of Visser 2023 Table 4, and "
               "in the digestive picker."),
    "8241/3": ("D2, D7", EVIDENCE,
               "Enterochromaffin cell carcinoid at basis 4 with imaging and a raised serum "
               "serotonin (Visser 2023 Table 4), and in the digestive picker."),
    "8240/3": ("D1, D2, D7, D8", EVIDENCE,
               "Neuroendocrine tumour, grade 1 or no grade stated, of the pancreas on the "
               "digestive histology screen (Karges 2025) and in the digestive picker for the "
               "other organs; at basis 5 when cytology names it; at basis 4 with imaging and a "
               "raised serum chromogranin A (Visser 2023 Table 4)."),
    "8249/3": ("D1, D2", EVIDENCE,
               "Neuroendocrine tumour, grade 2 or grade 3, of the pancreas on the digestive "
               "histology screen (Karges 2025) and in the digestive picker for the other organs; "
               "ICD-O-3.2 lists Neuroendocrine tumor, grade 3 as a related term."),
    "8246/3": ("D1, D2", EVIDENCE,
               "Neuroendocrine carcinoma of the pancreas on the digestive histology screen "
               "(Karges 2025) and in the digestive picker for the other organs."),
    "8452/3": ("D1, D6, D8", EVIDENCE,
               "Solid pseudopapillary neoplasm of the pancreas on the digestive histology screen "
               "(Pfister 2022, p. 13; Stanley 2015; Ebrahim 2025), at basis 5 when cytology "
               "names it, and from the pancreas stain panel (nuclear beta-catenin positive, "
               "chromogranin and trypsin negative; Stanley 2015, pp. 2-3). A report calling it "
               "benign keeps 8452/3 (registrar question 6).",
               {"diagnostic_tests_required": _IHC,
                "ihc_markers_required": ["Beta-catenin (nuclear)"]}),
    "8550/3": ("D1, D2", EVIDENCE,
               "Acinar cell carcinoma of the pancreas on the digestive histology screen (Pfister "
               "2022, p. 13) and in the digestive picker for the other organs."),
    "8140/3": ("D2, D8", EVIDENCE,
               "Adenocarcinoma at basis 5 when cytology of a digestive organ names it, and in "
               "the digestive picker."),
    "8010/3": ("D2, D4, D8", EVIDENCE,
               "Carcinoma whose type the report does not name: basis 5 when cytology names a "
               "carcinoma without its type or a type the cytology screen does not show, the "
               "pancreas stain panel's fallback, and in the digestive picker."),
}
