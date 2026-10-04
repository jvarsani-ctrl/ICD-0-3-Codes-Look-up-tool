"""The ICCC-3 Group VIII decision tree, `g8_bone`, as data.

Authored here rather than by hand in group_08_dt.json so the tree and the entries regenerate
together from one command (build/generate_group08_entries.py). Edit the tree HERE; the JSON
is the product. Architecture: docs/group_08_build_contract.md §4. Code decisions D1-D15:
docs/superpowers/specs/2026-10-02-group-08-bone-code-decisions-design.md.

Clerk-facing text lives in `question`, `hint`, `label`, `finding`, `reason` and the imaging
lists. `coding_note` is author-facing and never rendered (registrar ruling, Aug 2026). No
clerk-facing string names a node id or a schema field (check_no_internal_identifier_leaks).
`clinical_alert` is null everywhere (ruling 9).
"""
from __future__ import annotations

TREE_ID = "g8_bone"
ENTRY = "bn_document_inventory"

# Short citations for clerk-facing `reason` text. Full forms are in the build contract §10.
VISSER = "Visser 2023, European Network of Cancer Registries"
NOT_REGISTRABLE_POSSIBLE = (
    "Cancer is only possible on this evidence. Under the European registry rules a case "
    "that is only possibly cancer is not registered without pathology (%s, rule 4)." % VISSER)
EVIDENCE_TIER = ["evidence_tests", "workup_status", "basis_evidence_tier"]
# The conventional high-grade osteosarcoma radiograph, Menendez 2022, p. 99. The one copy:
# the imaging node shows it and entry 9180 records it (generate_group08_entries.py).
OSTEOSARCOMA_IMAGING_FEATURES = [
    "A lesion inside the bone at the metaphysis of a long bone, with poorly defined "
    "margins or permeative destruction",
    "Cloud-like sclerotic (osteoid) matrix mineralisation",
    "An aggressive periosteal reaction: sunburst spicules or a Codman triangle",
]


def _tail(b, captures=None, note=None, negative=None):
    """Append the optional keys every branch helper shares, in one fixed order."""
    if note:
        b["coding_note"] = note
    if captures:
        b["captures"] = captures
    if negative:
        b["negative"] = negative
    return b


def code(label, morph, basis, reason, captures=None, satisfies=None, note=None, key="label",
         negative=None):
    b = {key: label, "morphology_code": morph, "behavior_code": "3",
         "basis_of_diagnosis": basis, "reason": reason}
    if satisfies:
        b["satisfies_tests"] = satisfies
    return _tail(b, captures, note, negative)


def go(label, node, captures=None, note=None):
    return _tail({"label": label, "next_node": node}, captures, note)


def excl(label, icdo, beh, term, reason, captures=None, note=None):
    return _tail({"label": label,
                  "behaviour_exclusion": {"icdo_code": icdo, "icdo_behaviour": beh,
                                          "icdo_term": term, "group_declares": "3",
                                          "reason": reason,
                                          "registrar_decision_required": True}},
                 captures, note)


def nonrep(label, reason, captures=None, note=None):
    return _tail({"label": label, "non_reportable": True, "reason": reason}, captures, note)


def refer(label, group, reason, captures=None, note=None, key="label"):
    return _tail({key: label, "refer_group": group, "reason": reason}, captures, note)


def node(node_id, node_type, step, step_label, question, hint, options, captured, note,
         **extra):
    n = {"node_id": node_id, "node_type": node_type, "step_number": step,
         "step_label": step_label, "question": question, "hint": hint,
         "clinical_alert": None, "coding_note": note, "captured_variables": captured}
    if options is not None:
        n["options"] = options
    n.update(extra)
    n.setdefault("nos_fallback", None)
    return n


def benign_reason(name, icdo, beh, kind="a benign"):
    return ("%s is %s tumour, ICD-O-3.2 %s/%s. ICCC-3 Group VIII registers malignant "
            "(behaviour 3) tumours only, so no Group VIII code is recorded. Whether the "
            "registry records it elsewhere is the registrar's decision."
            % (name, kind, icdo, beh))


def intermediate_reason(name, icdo, beh):
    return benign_reason(name, icdo, beh, kind="a locally aggressive (intermediate)")


# ------------------------------------------------------------------------------------------
NODES = [
    node(
        "bn_document_inventory", "document_inventory", 1, "Evidence in file",
        "A suspected malignant bone tumour. What is actually in this patient's file?",
        "Pick the highest tier of evidence genuinely in the file. A radiology report counts "
        "as imaging. A pathology report on a biopsy, curettage or resection counts as "
        "histology.",
        [
            go("Referral letter or clinical note only — no imaging report, no cytology, no "
               "histology report in the file", "bn_clinical_alias",
               {"evidence_tests": ["Referral only"], "workup_status": "not done",
                "basis_evidence_tier": "referral"}),
            go("X-ray, CT or MRI report — no tissue (cytology or histology) in the file",
               "bn_imaging_line",
               {"evidence_tests": ["Imaging"], "workup_status": "incomplete",
                "basis_evidence_tier": "imaging"}),
            go("Histology report from a biopsy, curettage or resection", "bn_histology_line",
               {"evidence_tests": ["Histology"], "workup_status": "incomplete",
                "basis_evidence_tier": "histology"}),
            go("Fine-needle aspiration or other cytology report only — no histology report",
               "bn_cytology",
               {"evidence_tests": ["Cytology"], "workup_status": "incomplete",
                "basis_evidence_tier": "cytology"}),
            go("A specimen was taken but the report calls it inadequate, non-diagnostic or "
               "uninterpretable", "bn_imaging_line",
               {"evidence_tests": [], "workup_status": "incomplete",
                "basis_evidence_tier": "inadequate_specimen"},
               note="An inadequate specimen leaves the imaging as the best evidence; the "
                    "imaging line offers a route back to histology when tissue arrives."),
            refer("The tumour arises in soft tissue, not bone — the mass is outside the bone "
                  "and the cortex is intact", 9,
                  "A sarcoma arising in soft tissue belongs to ICCC-3 Group IX, even where the "
                  "same tumour in bone is Group VIII (Ewing sarcoma, fibrosarcoma, "
                  "chondrosarcoma, osteosarcoma). Code the case from the Group IX (soft tissue "
                  "sarcomas) tree.", {"tumour_origin": "soft_tissue"},
                  note="Origin gate. The express lane enters at this node without asking the "
                       "router's tumour_origin discriminator, and ICCC-2017 files many Group VIII "
                       "codes in Group IX off bone (dual_group_rules 9364 and 9365)."),
        ],
        EVIDENCE_TIER,
        "Build contract §4. Five routes, the Group 6 rn_document_inventory idiom. Every "
        "Group VIII tumour sits at C40-C41, so the router's site capture already holds the "
        "topography and this node does not ask it again.",
    ),
    node(
        "bn_clinical_alias", "clinical_alias", 2, "Referral wording",
        "What does the referral letter or clinical note say?",
        "No imaging or pathology report is in the file. On a note alone the tool can record "
        "only an unspecified malignant neoplasm, never a specific bone tumour.",
        [
            code("The note states a malignant bone tumour as the diagnosis (for example "
                 "osteosarcoma, Ewing sarcoma or bone cancer)", "8000", 1,
                 "Recorded as Neoplasm, malignant (8000/3) at basis of diagnosis 1. A "
                 "diagnosis resting on clinical information alone is registered with the "
                 "unspecified code; osteosarcoma needs at least an imaging report (%s, rule 5 "
                 "and Table 3). Obtain the imaging or pathology report and code again."
                 % VISSER,
                 {"workup_status": "incomplete", "basis_evidence_tier": "referral_malignant"},
                 note="Visser rule 5 permits 8000/3 at basis 1 when cancer is at least "
                      "likely. Registrar review B4: Group VI emits nothing at basis 1."),
            go("The file also holds an X-ray, CT or MRI report", "bn_imaging_line",
               {"evidence_tests": ["Referral only", "Imaging"], "workup_status": "incomplete",
                "basis_evidence_tier": "imaging"}),
            nonrep("The note describes pain, a swelling or a limp with no stated diagnosis, or "
                   "names a non-malignant cause in the differential (infection, injury, a "
                   "benign lesion)", NOT_REGISTRABLE_POSSIBLE,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "referral_nondiagnostic"}),
        ],
        EVIDENCE_TIER,
        "Visser O, et al. Frontiers in Oncology 2023;13:1250549, rules 4 and 5, p. 03.",
    ),
    node(
        "bn_imaging_line", "morphology_only", 2, "Imaging conclusion",
        "No tissue diagnosis is in the file. What does the imaging report conclude?",
        "Answer from the radiologist's own conclusion. Only osteosarcoma can be coded as a "
        "specific tumour on imaging alone.",
        [
            go("An aggressive bone-forming tumour — the report favours osteosarcoma",
               "bn_imaging_os", {"basis_evidence_tier": "imaging_osteosarcoma"}),
            code("An aggressive malignant bone tumour of another or unstated type — for "
                 "example a permeative lesion favouring Ewing sarcoma, or a malignant-looking "
                 "cartilage tumour", "8000", 2,
                 "Recorded as Neoplasm, malignant (8000/3) at basis of diagnosis 2. Ewing "
                 "sarcoma is not among the diagnoses the European rules allow without "
                 "pathology, and imaging does not grade cartilage tumours reliably in "
                 "children (%s, rule 5 and Table 3; Sharif 2021). A biopsy report gives the "
                 "specific code." % VISSER,
                 {"evidence_tests": ["Imaging"], "workup_status": "incomplete",
                  "basis_evidence_tier": "imaging_malignant_unspecified"},
                 note="Design D10. Sharif B, et al. Eur J Radiol 2021;137:109579, p. 4, citing "
                      "Ardakani et al., Skeletal Radiol 2020: 47% MRI-surgery grade mismatch "
                      "in 17 paediatric central chondrosarcomas."),
            nonrep("A benign-looking lesion, or a report whose differential includes a benign "
                   "tumour, infection or injury", NOT_REGISTRABLE_POSSIBLE,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "imaging_nondiagnostic"}),
            go("Tissue has since been obtained — a histology report is now in the file",
               "bn_histology_line",
               {"evidence_tests": ["Imaging", "Histology"], "workup_status": "incomplete",
                "basis_evidence_tier": "histology"}),
            go("Tissue has since been obtained — a cytology report only", "bn_cytology",
               {"evidence_tests": ["Imaging", "Cytology"], "workup_status": "incomplete",
                "basis_evidence_tier": "cytology"}),
            go("No imaging report in the file either — only a referral letter or clinical note",
               "bn_clinical_alias",
               {"evidence_tests": ["Referral only"], "workup_status": "incomplete",
                "basis_evidence_tier": "referral"},
               note="Reached from an inadequate specimen or non-diagnostic cytology with no "
                    "imaging report. Without this the only code here claimed Imaging as "
                    "evidence; the referral node gives 8000/3 at basis 1 (Visser rule 5)."),
        ],
        EVIDENCE_TIER,
        "Visser Table 3 allows 9180/3 and 9220/3 at C40/C41 on clinical investigation; this "
        "build uses 9180/3 only (design D10). Everything else without pathology is 8000/3 "
        "under rule 5.",
    ),
    node(
        "bn_imaging_os", "imaging_pathway", 3, "Imaging — osteosarcoma",
        "No tissue exists. Tick every feature the X-ray, CT or MRI report actually states, "
        "then answer the checklist below.",
        "All three features must be stated in the report for osteosarcoma to be coded on "
        "imaging. Do not infer one feature from another.",
        None, EVIDENCE_TIER,
        "imaging_sufficient is true on 9180/3 only. The three features are the conventional "
        "high-grade osteosarcoma radiograph description of Menendez N, et al. Semin "
        "Ultrasound CT MRI 2022;43(1):97-114, p. 99. Basis 2 per Visser 2023 Table 3. "
        "Histology stays outstanding on purpose: biopsy gives the subtype and is standard "
        "before treatment.",
        imaging_features=OSTEOSARCOMA_IMAGING_FEATURES,
        diversion_criteria=[
            {"feature": "The matrix shows cartilage-type 'rings and arcs' calcification",
             "reason": "Rings-and-arcs calcification is the cartilage-matrix pattern. "
                       "Chondroblastic osteosarcoma and chondrosarcoma both show it, and "
                       "imaging cannot separate them (Menendez 2022, p. 99). Tissue is "
                       "required."},
            {"feature": "The tumour sits on the surface of the bone rather than inside it",
             "reason": "Surface osteosarcomas (parosteal, periosteal, high-grade surface) "
                       "carry separate codes that histology decides (Menendez 2022, p. 108)."},
            {"feature": "Fluid-fluid levels with little or no mineralised matrix",
             "reason": "This is the telangiectatic osteosarcoma pattern, which can be "
                       "mistaken for an aneurysmal bone cyst, a benign lesion (Menendez "
                       "2022, pp. 109–110). Tissue is required."},
        ],
        no_tissue=True,
        endpoint_verification="not_verified",
        morphology_code="9180",
        behavior_code="3",
        basis_of_diagnosis=2,
        insufficient_next_node="bn_imaging_insufficient",
        upgrade_path="A biopsy would confirm osteosarcoma and give its subtype.",
        captures={"evidence_tests": ["Imaging"], "workup_status": "incomplete",
                  "basis_evidence_tier": "imaging"},
    ),
    node(
        "bn_imaging_insufficient", "morphology_only", 4, "Imaging did not confirm",
        "The imaging features did not confirm osteosarcoma. What does the report support?",
        "A diversion means only that tissue is needed; it does not say what the tumour is.",
        [
            code("The radiologist still calls the lesion a malignant bone tumour", "8000", 2,
                 "Recorded as Neoplasm, malignant (8000/3) at basis of diagnosis 2. The "
                 "imaging does not support a specific code; a biopsy report gives it.",
                 {"evidence_tests": ["Imaging"], "workup_status": "incomplete",
                  "basis_evidence_tier": "imaging_insufficient"}),
            nonrep("A benign lesion, infection or injury remains in the differential",
                   NOT_REGISTRABLE_POSSIBLE,
                   {"workup_status": "not registrable",
                    "basis_evidence_tier": "imaging_nondiagnostic"}),
            go("Tissue has since been obtained — a histology report is now in the file",
               "bn_histology_line",
               {"evidence_tests": ["Imaging", "Histology"], "workup_status": "incomplete",
                "basis_evidence_tier": "histology"}),
            go("Tissue has since been obtained — a cytology report only", "bn_cytology",
               {"evidence_tests": ["Imaging", "Cytology"], "workup_status": "incomplete",
                "basis_evidence_tier": "cytology"}),
        ],
        EVIDENCE_TIER,
        "Reached only from the osteosarcoma imaging node's insufficient_next_node, the Group "
        "6 rn_imaging_insufficient idiom.",
    ),
    node(
        "bn_cytology", "morphology_only", 2, "Cytology",
        "What does the fine-needle aspiration or other cytology report show?",
        "Cytology cannot establish a bone tumour's matrix or subtype. A specific code needs a "
        "histology report.",
        [
            code("Malignant cells are present (a malignant tumour, sarcoma or small round "
                 "cell tumour), with no tissue diagnosis", "8001", 5,
                 "Recorded as Tumor cells, malignant (8001/3) at basis of diagnosis 5, "
                 "cytology. A histology report gives the specific code.",
                 {"workup_status": "incomplete", "basis_evidence_tier": "cytology_malignant"}),
            go("No malignant cells, scant material, or a non-diagnostic report",
               "bn_imaging_line",
               {"workup_status": "incomplete", "basis_evidence_tier": "cytology_nondiagnostic"},
               note="Non-diagnostic cytology leaves imaging as the best evidence."),
            go("A histology report is now also in the file", "bn_histology_line",
               {"evidence_tests": ["Cytology", "Histology"], "workup_status": "incomplete",
                "basis_evidence_tier": "histology"}),
        ],
        EVIDENCE_TIER,
        "Basis 5 for cytology: Visser 2023 Table 1, p. 03. 8001/3 is the ICD-O-3.2 'Tumor "
        "cells, malignant' term, VIIIe at C40-C41.",
    ),
    node(
        "bn_histology_line", "histology_subclassification", 3, "Tumour line",
        "What kind of tumour does the histology report describe?",
        "Choose the line the report's diagnosis belongs to. If the report names the tumour, "
        "choose that tumour's line.",
        [
            go("Bone-forming — osteosarcoma, or a tumour making osteoid or bone "
               "(osteoblastoma, osteoid osteoma)", "bn_osteosarcoma",
               {"tissue_line": "bone_forming"}),
            go("Cartilage-forming — chondrosarcoma, atypical cartilaginous tumour, "
               "enchondroma, osteochondroma, chondroblastoma", "bn_cartilage",
               {"tissue_line": "cartilage"}),
            go("Small round cell tumour — Ewing sarcoma, a round cell sarcoma, or a small "
               "round blue cell tumour still being classified", "bn_round_cell",
               {"tissue_line": "small_round_cell"}),
            go("Notochordal — chordoma", "bn_chordoma", {"tissue_line": "notochordal"}),
            go("Giant cell-rich — giant cell tumour of bone, or another lesion full of "
               "osteoclast-like giant cells", "bn_giant_cell", {"tissue_line": "giant_cell"}),
            go("Spindle cell or pleomorphic sarcoma without bone or cartilage matrix",
               "bn_spindle", {"tissue_line": "spindle_pleomorphic"}),
            go("Epithelial islands in fibro-osseous tissue, in the tibia or fibula — "
               "adamantinoma or osteofibrous dysplasia", "bn_adamantinoma",
               {"tissue_line": "fibro_osseous"}),
            go("Odontogenic tumour of the jaw", "bn_odontogenic",
               {"tissue_line": "odontogenic"}),
            refer("Vascular sarcoma of bone (angiosarcoma, epithelioid haemangioendothelioma) "
                  "or leiomyosarcoma of bone", 9,
                  "ICCC-3 files vascular sarcomas and leiomyosarcomas in Group IX at every "
                  "site, bone included. Code the case from the Group IX (soft tissue "
                  "sarcomas) tree.", {"tissue_line": "vascular_or_smooth_muscle"},
                  note="ICCC-2017.sqlite ranges 86 (IXd6, 8890-8898, 000-809) and 88 (IXd8, "
                       "9120-9175, 000-809). WHO 2020 Table 1 lists epithelioid "
                       "haemangioendothelioma 9133/3, angiosarcoma 9120/3 and leiomyosarcoma "
                       "8890/3 in the bone chapter."),
            refer("Lymphoma or plasmacytoma in bone", 2,
                  "Haematolymphoid tumours of bone belong to ICCC-3 Group II at every site. "
                  "Code the case from the Group II (lymphomas) tree.",
                  {"tissue_line": "haematolymphoid"},
                  note="WHO 2020 Table 1 'Haematopoietic neoplasms of bone'; ICCC-2017 ranges "
                       "12-23 are site-independent for these codes."),
            refer("Langerhans cell histiocytosis in bone (eosinophilic granuloma)", 2,
                  "Langerhans cell histiocytosis is coded in ICCC-3 Group II, not here. It is not "
                  "always malignant: ICD-O-3.2 codes a single bone lesion (monostotic) 9751/1 "
                  "and disseminated disease 9751/3. Code the case from the Group II tree, which "
                  "decides the behaviour.",
                  {"tissue_line": "langerhans_cell_histiocytosis"},
                  note="icdo32.sqlite: 9751/1 'Langerhans cell histiocytosis, NOS' with Related "
                       "terms monostotic and polystotic; 9751/3 'disseminated'. group_02_dt.json "
                       "carries both. The engine's refer() banner still says 'This case is a "
                       "malignancy'; this reason corrects it beneath. Changing the banner is an "
                       "engine-wide decision."),
            go("A metastatic deposit from a primary tumour elsewhere", "bn_metastasis",
               {"tissue_line": "metastasis"}),
            code("Sarcoma, type not stated", "8800", 7,
                 "The report calls the tumour a sarcoma without naming its type. Recorded as "
                 "Sarcoma, NOS (8800/3).", {"tissue_line": "sarcoma_nos"}),
            code("Malignant tumour, type not stated", "8000", 7,
                 "The report establishes a malignant tumour without naming its type. "
                 "Recorded as Neoplasm, malignant (8000/3).", {"tissue_line": "malignant_nos"}),
            nonrep("No tumour — infection, fracture callus, or reactive or other "
                   "non-neoplastic change",
                   "The histology shows no tumour. Not a reportable malignancy.",
                   {"tissue_line": "no_tumour", "workup_status": "not registrable"}),
        ],
        ["tissue_line"],
        "The matrix router (Diagnostic Pathway §2A), read from histology. The imaging-read "
        "half of the pathway's router is the separate imaging line, so this node never "
        "accepts an imaging answer (design, 'What was weighed').",
    ),
    node(
        "bn_osteosarcoma", "histology_subclassification", 4, "Bone-forming tumour",
        "Which bone-forming tumour does the report diagnose?",
        "Use the report's own term. A conventional osteosarcoma is coded as Osteosarcoma, NOS "
        "unless the report names the chondroblastic or fibroblastic subtype.",
        [
            code("Osteosarcoma, conventional osteosarcoma, osteoblastic osteosarcoma, or "
                 "high-grade osteosarcoma with no subtype named", "9180", 7,
                 "Recorded as Osteosarcoma, NOS (9180/3), WHO 2020's code for conventional "
                 "osteosarcoma."),
            code("Central or medullary osteosarcoma (the report uses this term)", "9186", 7,
                 "Recorded as Central osteosarcoma, NOS (9186/3), the report's own term.",
                 note="Design D9: 'conventional' goes to 9180/3; 'central', 'conventional "
                      "central' or 'medullary' is coded as written."),
            code("Chondroblastic osteosarcoma", "9181", 7,
                 "Recorded as Chondroblastic osteosarcoma (9181/3), the report's own term."),
            code("Fibroblastic osteosarcoma", "9182", 7,
                 "Recorded as Fibroblastic osteosarcoma (9182/3), the report's own term."),
            code("Telangiectatic osteosarcoma", "9183", 7,
                 "Recorded as Telangiectatic osteosarcoma (9183/3), the report's own term."),
            code("Small cell osteosarcoma", "9185", 7,
                 "Recorded as Small cell osteosarcoma (9185/3), the report's own term."),
            code("Low-grade central osteosarcoma (intraosseous well-differentiated "
                 "osteosarcoma)", "9187", 7,
                 "Recorded as Low grade central osteosarcoma (9187/3)."),
            code("Parosteal osteosarcoma", "9192", 7,
                 "Recorded as Parosteal osteosarcoma (9192/3)."),
            code("Periosteal osteosarcoma", "9193", 7,
                 "Recorded as Periosteal osteosarcoma (9193/3)."),
            code("High-grade surface osteosarcoma", "9194", 7,
                 "Recorded as High grade surface osteosarcoma (9194/3)."),
            code("Secondary osteosarcoma, or osteosarcoma in Paget disease of bone", "9184", 7,
                 "Recorded as Osteosarcoma in Paget disease of bone (9184/3), the ICD-O-3.2 "
                 "code whose synonym is Secondary osteosarcoma."),
            excl("Osteoblastoma", "9200", "0", "Osteoblastoma, NOS",
                 benign_reason("Osteoblastoma", "9200", "0")),
            excl("Aggressive osteoblastoma", "9200", "1", "Aggressive osteoblastoma",
                 intermediate_reason("Aggressive osteoblastoma", "9200", "1")),
            excl("Osteoid osteoma", "9191", "0", "Osteoid osteoma, NOS",
                 benign_reason("Osteoid osteoma", "9191", "0")),
            nonrep("The report does not reach a final diagnosis between a benign bone-forming "
                   "tumour and osteosarcoma",
                   "Malignancy is not established. A case that is only possibly cancer is not "
                   "registered (%s, rule 4). Code again when the final or expert report is "
                   "issued." % VISSER,
                   {"workup_status": "not registrable"},
                   note="Design, 'What was weighed': FOS is supportive, not definitive (Lam "
                        "2020), so the tool does not try to settle this from a marker."),
        ],
        [],
        "Design D8 and D9. WHO 2020 Table 1 lists conventional, telangiectatic and small cell "
        "osteosarcoma under 9180/3; ICD-O-3.2 keeps 9181, 9182, 9183 and 9185 live, and a "
        "report naming the subtype gets the specific code.",
    ),
    node(
        "bn_cartilage", "histology_subclassification", 4, "Cartilage tumour",
        "Which cartilage tumour does the report diagnose?",
        "Chondrosarcoma grade 1 and atypical cartilaginous tumour share one ICD-O-3.2 code of "
        "borderline behaviour. Chondrosarcoma grade 2 and grade 3 are malignant.",
        [
            code("Chondrosarcoma grade 2 or grade 3 (central or secondary peripheral), or "
                 "chondrosarcoma with no grade stated", "9220", 7,
                 "Recorded as Chondrosarcoma, NOS (9220/3), WHO 2020's code for "
                 "chondrosarcoma grade 2 and grade 3."),
            excl("Chondrosarcoma grade 1 (usually in the pelvis, scapula or skull base)",
                 "9222", "1", "Atypical cartilaginous tumor",
                 "ICD-O-3.2 codes chondrosarcoma grade 1 to 9222/1, together with atypical "
                 "cartilaginous tumour, and has no malignant code for it. WHO 2020 codes "
                 "axial chondrosarcoma grade 1 as 9222/3, a number ICD-O-3.2 does not carry. "
                 "The case is not recorded as a Group VIII cancer until the registrar rules.",
                 note="Design D3, registrar review A1. Switching to option B (9220/3) or C "
                      "(9222/3 after a Layer 1 change) is this one block."),
            excl("Atypical cartilaginous tumour (usually in a long bone of a limb)", "9222",
                 "1", "Atypical cartilaginous tumor",
                 intermediate_reason("Atypical cartilaginous tumour", "9222", "1")),
            code("Periosteal (juxtacortical) chondrosarcoma", "9221", 7,
                 "Recorded as Periosteal chondrosarcoma (9221/3)."),
            code("Mesenchymal chondrosarcoma", "9240", 7,
                 "Recorded as Mesenchymal chondrosarcoma (9240/3)."),
            code("Clear cell chondrosarcoma", "9242", 7,
                 "Recorded as Clear cell chondrosarcoma (9242/3)."),
            code("Dedifferentiated chondrosarcoma", "9243", 7,
                 "Recorded as Dedifferentiated chondrosarcoma (9243/3)."),
            go("A benign or borderline cartilage tumour — enchondroma, chondroma, "
               "osteochondroma, chondroblastoma, chondromyxoid fibroma", "bn_cartilage_benign"),
            nonrep("The report does not decide between a benign cartilage tumour and "
                   "chondrosarcoma",
                   "Malignancy is not established. A case that is only possibly cancer is not "
                   "registered (%s, rule 4). Code again when the final report is issued."
                   % VISSER, {"workup_status": "not registrable"}),
        ],
        [],
        "WHO 2020 Table 1 chondrogenic tumours: atypical cartilaginous tumour 9222/1, "
        "chondrosarcoma grade 1 9222/3*, "
        "grade 2 and 3 9220/3, periosteal 9221/3, clear cell 9242/3, mesenchymal 9240/3, "
        "dedifferentiated 9243/3. Anderson & Doyle 2021, p. 652: atypical cartilaginous "
        "tumour for the appendicular "
        "skeleton, chondrosarcoma grade 1 for axial tumours.",
    ),
    node(
        "bn_cartilage_benign", "morphology_only", 5, "Benign cartilage tumour",
        "Which benign or borderline cartilage tumour does the report diagnose?",
        "None of these is a Group VIII cancer. The answer records the ICD-O-3.2 code the "
        "tumour sits at.",
        [
            excl("Enchondroma or chondroma", "9220", "0", "Chondroma, NOS",
                 benign_reason("Chondroma", "9220", "0")),
            excl("Chondromatosis (multiple chondromas)", "9220", "1", "Chondromatosis, NOS",
                 benign_reason("Chondromatosis", "9220", "1", kind="a borderline")),
            excl("Periosteal (juxtacortical) chondroma", "9221", "0", "Periosteal chondroma",
                 benign_reason("Periosteal chondroma", "9221", "0")),
            excl("Osteochondroma (cartilaginous exostosis)", "9210", "0", "Osteochondroma",
                 benign_reason("Osteochondroma", "9210", "0")),
            excl("Osteochondromatosis (multiple osteochondromas)", "9210", "1",
                 "Osteochondromatosis, NOS",
                 benign_reason("Osteochondromatosis", "9210", "1", kind="a borderline")),
            excl("Chondroblastoma", "9230", "1", "Chondroblastoma, NOS",
                 benign_reason("Chondroblastoma", "9230", "1", kind="a borderline"),
                 note="ICD-O-3.2 moved chondroblastoma from /0 to /1 (IARC 'Terms that are "
                      "changing behaviour'); Anderson & Doyle 2021, p. 652 records WHO 2020 "
                      "calling it benign."),
            excl("Chondromyxoid fibroma", "9241", "0", "Chondromyxoid fibroma",
                 benign_reason("Chondromyxoid fibroma", "9241", "0")),
        ],
        [],
        "Behaviour exclusions only (Group IV precedent). Design D11.",
    ),
    node(
        "bn_round_cell", "morphology_only", 4, "Small round cell tumour",
        "What final diagnosis does the report give for the small round cell tumour?",
        "If the report gives only a description and a panel of stains or molecular tests, "
        "choose the last option and enter the panel.",
        [
            code("Ewing sarcoma (or Ewing tumour, or peripheral neuroectodermal tumour), with "
                 "an EWSR1 or FUS fusion to an ETS gene demonstrated", "9364", 8,
                 "Recorded as Ewing sarcoma (9364/3) at basis of diagnosis 8: a FET::ETS "
                 "fusion is specific to Ewing sarcoma.", satisfies=["IHC"],
                 note="Basis 8 per Visser 2023 rule 10. satisfies IHC: a demonstrated "
                      "FET::ETS fusion is stronger evidence than the immunohistochemistry it "
                      "replaces."),
            code("Ewing sarcoma diagnosed on morphology and immunohistochemistry, with no "
                 "molecular result reported", "9364", 7,
                 "Recorded as Ewing sarcoma (9364/3). Ewing sarcoma has been coded 9364 "
                 "since ICD-O-3.2; the old code 9260 now means aneurysmal bone cyst.",
                 satisfies=["IHC"]),
            code("Ewing sarcoma named as the diagnosis, with no supporting test described",
                 "9364", 7,
                 "Recorded as Ewing sarcoma (9364/3) on the report's diagnosis. No "
                 "immunohistochemistry is described, so it shows as outstanding."),
            code("Askin tumour (the report uses this term)", "9365", 7,
                 "Recorded as Askin tumor (9365/3), the report's own term. A chest-wall "
                 "tumour reported as Ewing sarcoma is coded Ewing sarcoma instead.",
                 note="Design D2. No satisfies_tests: the option asserts a term, not a "
                      "stain, so IHC stays outstanding as on the 'Ewing sarcoma named' option."),
            code("CIC-rearranged sarcoma, sarcoma with a BCOR genetic alteration, or round "
                 "cell sarcoma with an EWSR1–non-ETS fusion", "8803", 7,
                 "Recorded as Small cell sarcoma (8803/3), whose ICD-O-3.2 synonym is Round "
                 "cell sarcoma, NOS. These sarcomas are classified separately from Ewing "
                 "sarcoma and ICD-O-3.2 has no code of their own.",
                 note="Design D6, registrar review A2. Basis 7 rather than 8: the report may "
                      "rest on a surrogate stain (ETV4, BCOR) rather than the "
                      "rearrangement itself."),
            code("Small cell osteosarcoma (the round cells make osteoid)", "9185", 7,
                 "Recorded as Small cell osteosarcoma (9185/3). Osteoid production separates "
                 "it from Ewing sarcoma."),
            code("Mesenchymal chondrosarcoma (round cells with islands of cartilage)", "9240", 7,
                 "Recorded as Mesenchymal chondrosarcoma (9240/3)."),
            refer("Lymphoma, including lymphoblastic lymphoma", 2,
                  "Lymphoma in bone belongs to ICCC-3 Group II. Code the case from the Group "
                  "II (lymphomas) tree."),
            refer("Rhabdomyosarcoma", 9,
                  "Rhabdomyosarcoma belongs to ICCC-3 Group IX at every site. Code the case "
                  "from the Group IX (soft tissue sarcomas) tree."),
            refer("Neuroblastoma", 4,
                  "Neuroblastoma in bone is metastatic, and neuroblastoma belongs to ICCC-3 "
                  "Group IV. Code the primary tumour from the Group IV tree."),
            code("Round cell sarcoma or undifferentiated round cell sarcoma, not further "
                 "classified", "8803", 7,
                 "Recorded as Small cell sarcoma (8803/3), whose ICD-O-3.2 synonym is Round "
                 "cell sarcoma, NOS."),
            go("Only a description (small round blue cell tumour) and a panel of stains or "
               "molecular tests", "bn_round_cell_ihc"),
        ],
        [],
        "Kallen ME, Hornick JL. Semin Diagn Pathol 2022;39(1):29-37: CD99 is not specific "
        "(p. 30); lymphoblastic lymphoma (TdT), neuroblastoma (PHOX2B) and rhabdomyosarcoma "
        "(desmin, myogenin, MyoD1) are the exclusions (p. 30); Table 1, p. 31. This node "
        "receives the Group IV op_ewing_site and Group III st_lesion_gate referrals.",
    ),
    node(
        "bn_round_cell_ihc", "ihc_checklist", 5, "Round cell panel",
        "Answer each stain or test as the report states it.",
        "Answer 'not done' for anything the report does not mention, and for a stain the "
        "report calls non-contributory (for example after decalcification). CD99 alone does "
        "not establish Ewing sarcoma.",
        None, [],
        "Rule order, build contract §4: haematolymphoid, neuroblastic and myogenic lines "
        "first; then the fusions; then the surrogate stains; then CD99 with NKX2-2. Kallen ME, "
        "Hornick JL. Semin Diagn Pathol 2022;39(1):29-37, Table 1 (p. 31) and Table 2 (p. 32). "
        "Fallback 8002/3 claims neither a sarcoma nor Ewing sarcoma.",
        marker_groups=[
            {"group_label": "Other lines — lymphoma, neuroblastoma, rhabdomyosarcoma, "
                            "synovial sarcoma",
             "markers": ["TdT", "CD45", "PHOX2B", "Myogenin", "MyoD1", "SS18::SSX"]},
            {"group_label": "Fusions (FISH, RT-PCR or sequencing)",
             "markers": ["FET::ETS fusion (EWSR1::FLI1, EWSR1::ERG or another)",
                         "EWSR1 or FUS fusion with a non-ETS partner (NFATC2, PATZ1)",
                         "CIC rearrangement",
                         "BCOR::CCNB3 fusion or BCOR internal tandem duplication"]},
            {"group_label": "Round cell sarcoma stains",
             "markers": ["ETV4", "BCOR", "CD99 (strong, diffuse, membranous)", "NKX2-2"]},
        ],
        resolution_logic=[
            refer(["TdT"], 2, "TdT is the marker of lymphoblastic lymphoma, a Group II "
                  "tumour that also expresses CD99. Code the case from the Group II tree.",
                  key="positive"),
            refer(["CD45"], 2, "CD45 marks a lymphoid neoplasm. Code the case from the Group "
                  "II (lymphomas) tree.", key="positive"),
            refer(["PHOX2B"], 4, "PHOX2B marks neuroblastoma, a Group IV tumour. Code the "
                  "primary from the Group IV tree.", key="positive"),
            refer(["Myogenin"], 9, "Myogenin marks rhabdomyosarcoma, a Group IX tumour. Code "
                  "the case from the Group IX tree.", key="positive"),
            refer(["MyoD1"], 9, "MyoD1 marks rhabdomyosarcoma, a Group IX tumour. Code the "
                  "case from the Group IX tree.", key="positive"),
            refer(["SS18::SSX"], 9, "SS18::SSX defines synovial sarcoma, a Group IX tumour. "
                  "Code the case from the Group IX tree.", key="positive"),
            code(["FET::ETS fusion (EWSR1::FLI1, EWSR1::ERG or another)"], "9364", 8,
                 "A FET::ETS fusion is specific to Ewing sarcoma. Recorded as Ewing sarcoma "
                 "(9364/3) at basis of diagnosis 8.", satisfies=["IHC"], key="positive"),
            code(["EWSR1 or FUS fusion with a non-ETS partner (NFATC2, PATZ1)"], "8803", 8,
                 "An EWSR1 or FUS fusion with a non-ETS partner defines a round cell sarcoma "
                 "classified separately from Ewing sarcoma. Recorded as Small cell sarcoma "
                 "(8803/3) at basis of diagnosis 8; ICD-O-3.2 has no code of its own.",
                 key="positive"),
            code(["CIC rearrangement"], "8803", 8,
                 "A CIC rearrangement defines CIC-rearranged sarcoma. Recorded as Small cell "
                 "sarcoma (8803/3) at basis of diagnosis 8; ICD-O-3.2 has no code of its own.",
                 key="positive"),
            code(["BCOR::CCNB3 fusion or BCOR internal tandem duplication"], "8803", 8,
                 "A BCOR fusion or internal tandem duplication defines sarcoma with BCOR "
                 "genetic alteration. Recorded as Small cell sarcoma (8803/3) at basis of "
                 "diagnosis 8; ICD-O-3.2 has no code of its own.", key="positive"),
            code(["ETV4"], "8803", 7,
                 "ETV4 is highly specific for CIC-rearranged sarcoma. Recorded as Small cell "
                 "sarcoma (8803/3); ICD-O-3.2 has no code of its own.", key="positive",
                 note="Kallen & Hornick 2022, p. 34, figure caption. negative NKX2-2: "
                      "CIC-rearranged sarcoma is NKX2-2 negative (p. 33), so a panel positive "
                      "for both is discordant and falls to 8002.",
                 negative=["NKX2-2"]),
            code(["BCOR"], "8803", 7,
                 "Diffuse nuclear BCOR marks sarcoma with BCOR genetic alteration. Recorded as "
                 "Small cell sarcoma (8803/3); ICD-O-3.2 has no code of its own.",
                 key="positive",
                 note="Kallen & Hornick 2022, p. 33: highly sensitive, moderately specific; "
                      "poorly differentiated synovial sarcoma also expresses BCOR, which the "
                      "SS18::SSX rule above catches first when tested. negative NKX2-2: "
                      "Ewing sarcoma is BCOR negative (Table 2, p. 31), so a panel positive "
                      "for both is discordant and falls to 8002.",
                 negative=["NKX2-2"]),
            code(["CD99 (strong, diffuse, membranous)", "NKX2-2"], "9364", 7,
                 "Strong diffuse membranous CD99 with nuclear NKX2-2 is the Ewing sarcoma "
                 "immunophenotype. Recorded as Ewing sarcoma (9364/3).", satisfies=["IHC"],
                 key="positive",
                 note="Kallen & Hornick 2022, p. 31. Placed after every fusion rule: CD99 "
                      "and NKX2-2 are not exclusive to Ewing sarcoma, and a demonstrated "
                      "non-ETS fusion overrides them (contract §4). negative ETV4 and BCOR: "
                      "Ewing sarcoma is negative for both (Table 2, p. 31), so a discordant "
                      "panel falls to 8002.",
                 negative=["ETV4", "BCOR"]),
        ],
        nos_fallback={
            "code": "8002", "behavior_code": "3", "name": "Malignant tumor, small cell type",
            "reason": "The panel does not establish the tumour's line. Recorded as Malignant "
                      "tumor, small cell type (8002/3), which claims neither a sarcoma nor "
                      "Ewing sarcoma. CD99 alone is not enough: it is also expressed in acute "
                      "leukaemias and other round cell tumours.",
        },
    ),
    node(
        "bn_chordoma", "histology_subclassification", 4, "Notochordal tumour",
        "Which notochordal tumour does the report diagnose?",
        "Nuclear brachyury staining defines chordoma.",
        [
            code("Chordoma, or conventional chordoma", "9370", 7,
                 "Recorded as Chordoma, NOS (9370/3)."),
            code("Poorly differentiated chordoma (brachyury positive, SMARCB1/INI1 lost)",
                 "9370", 7,
                 "Recorded as Chordoma, NOS (9370/3). WHO 2020 codes poorly differentiated "
                 "chordoma 9370/3; it has no separate code.",
                 note="Design D7. Receives Group III pf_ini1_loss_adjudication's brachyury "
                      "referral."),
            code("Chondroid chordoma", "9371", 7,
                 "Recorded as Chondroid chordoma (9371/3), the report's own term."),
            code("Dedifferentiated chordoma", "9372", 7,
                 "Recorded as Dedifferentiated chordoma (9372/3)."),
            excl("Benign notochordal cell tumour", "9370", "0", "Benign notochordal cell tumor",
                 benign_reason("Benign notochordal cell tumour", "9370", "0")),
        ],
        [],
        "WHO 2020 Table 1 notochordal tumours: conventional chordoma 9370/3 (chondroid "
        "chordoma beneath it), poorly differentiated chordoma 9370/3, dedifferentiated "
        "chordoma 9372/3. ICD-O-3.2 keeps 9371/3 live (design D8).",
    ),
    node(
        "bn_giant_cell", "histology_subclassification", 4, "Giant cell-rich lesion",
        "Which giant cell-rich lesion does the report diagnose?",
        "H3.3 G34W staining supports giant cell tumour of bone but does not decide whether it "
        "is malignant. Use the report's diagnosis.",
        [
            code("Malignant giant cell tumour of bone (the report calls it malignant)", "9250",
                 7, "Recorded as Giant cell tumor of bone, malignant (9250/3)."),
            excl("Giant cell tumour of bone", "9250", "1", "Giant cell tumor of bone, NOS",
                 intermediate_reason("Giant cell tumour of bone", "9250", "1")),
            excl("Chondroblastoma", "9230", "1", "Chondroblastoma, NOS",
                 benign_reason("Chondroblastoma", "9230", "1", kind="a borderline")),
            excl("Aneurysmal bone cyst", "9260", "0", "Aneurysmal bone cyst",
                 benign_reason("Aneurysmal bone cyst", "9260", "0"),
                 note="The one place this file names 9260: ICD-O-3.2's 9260 is now this "
                      "benign lesion (check_group8_no_retired_ewing_code)."),
            nonrep("Non-ossifying fibroma, brown tumour, giant cell reparative granuloma or "
                   "another reactive giant cell lesion",
                   "A benign or reactive giant cell lesion. Not a reportable malignancy."),
            code("A malignant giant cell-rich tumour whose type the report does not establish",
                 "8003", 7, "Recorded as Malignant tumor, giant cell type (8003/3)."),
        ],
        [],
        "WHO 2020 Table 1 osteoclastic giant cell-rich tumours: giant cell tumour of bone "
        "9250/1, giant cell tumour of bone, malignant 9250/3. Anderson & Doyle 2021, p. 653: G34W positivity is not synonymous with "
        "benignity.",
    ),
    node(
        "bn_spindle", "histology_subclassification", 4, "Spindle or pleomorphic tumour",
        "Which spindle cell or pleomorphic tumour does the report diagnose?",
        "Use the report's own term.",
        [
            code("Undifferentiated pleomorphic sarcoma of bone, or malignant fibrous "
                 "histiocytoma", "8830", 7,
                 "Recorded as Malignant fibrous histiocytoma (8830/3), the ICD-O-3.2 code that "
                 "carries the term Undifferentiated high grade pleomorphic sarcoma of bone.",
                 note="Design D5, registrar review A3."),
            code("Fibrosarcoma of bone", "8810", 7, "Recorded as Fibrosarcoma, NOS (8810/3)."),
            code("Spindle cell sarcoma, not further classified", "8801", 7,
                 "Recorded as Spindle cell sarcoma (8801/3)."),
            code("Undifferentiated sarcoma, not further classified", "8805", 7,
                 "Recorded as Undifferentiated sarcoma (8805/3)."),
            refer("Leiomyosarcoma or a vascular sarcoma (angiosarcoma, epithelioid "
                  "haemangioendothelioma) of bone", 9,
                  "ICCC-3 files leiomyosarcomas and vascular sarcomas in Group IX at every "
                  "site, bone included. Code the case from the Group IX tree."),
            excl("Desmoplastic fibroma", "8823", "1", "Desmoplastic fibroma",
                 intermediate_reason("Desmoplastic fibroma", "8823", "1")),
            excl("Fibrous dysplasia", "8818", "0", "Fibrous dysplasia",
                 benign_reason("Fibrous dysplasia", "8818", "0")),
            code("A malignant spindle cell tumour the report does not call a sarcoma", "8004",
                 7, "Recorded as Malignant tumor, spindle cell type (8004/3)."),
        ],
        [],
        "WHO 2020 Table 1: fibrosarcoma NOS 8810/3; pleomorphic sarcoma, undifferentiated "
        "8802/3, coded 8830/3 here (design D5).",
    ),
    node(
        "bn_adamantinoma", "histology_subclassification", 4, "Adamantinoma",
        "Which fibro-osseous tumour does the report diagnose?",
        "Use the report's own term.",
        [
            code("Adamantinoma (classic)", "9261", 7,
                 "Recorded as Adamantinoma of long bones (9261/3)."),
            code("Dedifferentiated adamantinoma", "9261", 7,
                 "Recorded as Adamantinoma of long bones (9261/3); WHO 2020 gives "
                 "dedifferentiated adamantinoma no separate code."),
            nonrep("Osteofibrous dysplasia-like adamantinoma",
                   "WHO 2020 classifies osteofibrous dysplasia-like adamantinoma as "
                   "locally aggressive (intermediate), not malignant, and ICD-O-3.2 has no "
                   "code for it below behaviour 3. Not recorded as a Group VIII cancer; the "
                   "registrar decides how it is recorded.",
                   note="Design D12, registrar review B2. Anderson & Doyle 2021, p. 654."),
            nonrep("Osteofibrous dysplasia",
                   "Osteofibrous dysplasia is a benign fibro-osseous lesion. Not a reportable "
                   "malignancy."),
        ],
        [],
        "WHO 2020 Table 1: adamantinoma of long bones 9261/3, dedifferentiated adamantinoma "
        "beneath it. Anderson & Doyle 2021, p. 654.",
    ),
    node(
        "bn_odontogenic", "histology_subclassification", 4, "Odontogenic tumour",
        "Which odontogenic tumour does the report diagnose?",
        "Use the report's own term.",
        [
            code("Ameloblastic carcinoma", "9270", 7,
                 "Recorded as Odontogenic tumor, malignant (9270/3), whose ICD-O-3.2 synonyms "
                 "include Ameloblastic carcinoma."),
            code("Primary intraosseous carcinoma", "9270", 7,
                 "Recorded as Odontogenic tumor, malignant (9270/3), whose ICD-O-3.2 synonyms "
                 "include Primary intraosseous carcinoma."),
            code("Sclerosing odontogenic carcinoma", "9270", 7,
                 "Recorded as Odontogenic tumor, malignant (9270/3). ICD-O-3.2 has no term "
                 "for sclerosing odontogenic carcinoma; its synonym Odontogenic carcinoma is "
                 "the nearest.", note="Design D13, registrar review A7."),
            code("Clear cell odontogenic carcinoma", "9341", 7,
                 "Recorded as Clear cell odontogenic carcinoma (9341/3)."),
            code("Ghost cell odontogenic carcinoma", "9302", 7,
                 "Recorded as Ghost cell odontogenic carcinoma (9302/3)."),
            code("Odontogenic carcinosarcoma", "9342", 7,
                 "Recorded as Odontogenic carcinosarcoma (9342/3)."),
            code("Ameloblastic fibrosarcoma", "9330", 7,
                 "Recorded as Ameloblastic fibrosarcoma (9330/3)."),
            code("Ameloblastic fibrodentinosarcoma or ameloblastic fibro-odontosarcoma",
                 "9290", 7,
                 "Recorded as Ameloblastic odontosarcoma (9290/3), whose ICD-O-3.2 synonyms "
                 "are these two terms."),
            code("Metastasizing ameloblastoma", "9310", 7,
                 "Recorded as Ameloblastoma, metastasizing (9310/3).",
                 note="Design D13, registrar review A6: WHO 2022 places it among the benign "
                      "tumours; ICD-O-3.2 codes it /3."),
            code("Malignant odontogenic tumour, type not stated", "9270", 7,
                 "Recorded as Odontogenic tumor, malignant (9270/3)."),
            excl("Ameloblastoma", "9310", "0", "Ameloblastoma, NOS",
                 benign_reason("Ameloblastoma", "9310", "0")),
            nonrep("Another benign odontogenic tumour, or an odontogenic cyst",
                   "A benign odontogenic tumour or cyst. Not a Group VIII cancer."),
        ],
        [],
        "Soluk-Tekkesin M, Wright JM. Turk Patoloji Derg 2022;38(2):168-184, Table 1, "
        "malignant odontogenic tumours, mapped to ICD-O-3.2 by term (design D13).",
    ),
    node(
        "bn_metastasis", "morphology_only", 4, "Metastatic deposit",
        "Which primary tumour has spread to the bone?",
        "A metastasis in bone is coded from its primary tumour's group.",
        [
            refer("Neuroblastoma", 4, "Code the primary neuroblastoma from the Group IV tree."),
            refer("Rhabdomyosarcoma", 9, "Code the primary rhabdomyosarcoma from the Group IX "
                  "tree."),
            refer("Renal tumour (Wilms tumour, clear cell sarcoma of the kidney)", 6,
                  "Code the primary renal tumour from the Group VI tree."),
            refer("Retinoblastoma", 5, "Code the primary retinoblastoma from the Group V tree."),
            refer("Liver tumour (hepatoblastoma, hepatocellular carcinoma)", 7,
                  "Code the primary liver tumour from the Group VII tree."),
            refer("Germ cell tumour", 10, "Code the primary germ cell tumour from the Group X "
                  "tree."),
            refer("Carcinoma or melanoma (for example nasopharyngeal carcinoma)", 11,
                  "Code the primary carcinoma or melanoma from the Group XI tree."),
            go("A bone sarcoma that has spread from another bone (osteosarcoma, Ewing sarcoma, "
               "chondrosarcoma)", "bn_histology_line",
               note="A bone sarcoma metastatic to bone is still Group VIII; code it by its "
                    "line from the primary's histology."),
            refer("Primary not found, and the tumour type is not stated", 12,
                  "A metastasis whose primary is not found and whose type is not stated is "
                  "an unspecified malignancy of unknown primary site, which belongs to "
                  "ICCC-3 Group XII."),
        ],
        [],
        "Receives Group III's pf_secondary_deposit and un_metastatic_deposit 'bone' "
        "referrals only when the bone lesion is itself a deposit. ICCC-2017 range 143 "
        "(XIIb) admits 8000-8005 at 809.",
    ),
]


def trees() -> list:
    """Return a fresh copy each call, so callers may mutate it."""
    import copy
    return [{
        "tree_id": TREE_ID,
        "tree_label": ("Malignant bone tumours (C40.0-C41.9; ICCC-3 Group VIII declares "
                       "behaviour 3 only) - an evidence gate, an imaging route that can code "
                       "osteosarcoma alone, and a histology matrix router feeding eleven "
                       "tumour lines, with benign and intermediate tumours recorded as "
                       "behaviour exclusions"),
        "entry_node": ENTRY,
        "topography": ["C40.0-C41.9"],
        "basis_of_diagnosis_defaults": {"ihc_counts_as": 7, "methylation_counts_as": 8},
        "nodes": copy.deepcopy(NODES),
    }]
