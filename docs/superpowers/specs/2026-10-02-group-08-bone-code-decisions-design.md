# Group VIII — code decisions and tree shape (design)

**Written 2 October 2026, before any Group VIII JSON was authored.** Brainstorming output for
the Group VIII build on branch `claude/group-8-tumor-pathway-64edbc`. The registrar was not
available during the session. Each decision below carries the options, the one this build
takes, and why. Decisions marked **PROVISIONAL** are built as written and are listed for the
registrar in `docs/group_08_registrar_review.md`. The build contract is
`docs/group_08_build_contract.md`.

## Sources this rests on

| Role | Source |
|---|---|
| Code currency | `ICD coding/ICD-O-3.2/icdo32.sqlite` (IARC final, 9 October 2020) and the four IARC 3.1→3.2 change documents |
| Grouping | `ICCC-2017.sqlite`, `code_ranges` for `main_group = 'VIII'` (ranges 59–71) |
| WHO 2020 bone entities with ICD-O codes | WHO Classification of Tumours Editorial Board, *Soft Tissue and Bone Tumours*, 5th ed., 2020, Table 1, reproduced with WHO/IARC permission in the International Collaboration on Cancer Reporting dataset *Primary tumour in bone — resection*, note "Histological tumour type", pp. 1–2 (iccr-cancer.org/datasets/docs/iccr-boner-histott) |
| WHO 2020 bone narrative | Anderson WJ, Doyle LA. *Updates from the 2020 World Health Organization Classification of Soft Tissue and Bone Tumours.* Histopathology 2021;78(5):644–657 |
| WHO 2022 odontogenic entities | Soluk-Tekkesin M, Wright JM. *The World Health Organization Classification of Odontogenic Lesions: A Summary of the Changes of the 2022 (5th) Edition.* Turk Patoloji Derg 2022;38(2):168–184, Table 1 |
| Registration without pathology | Visser O, et al. Front Oncol 2023;13:1250549, rules 4–5 (p. 03), Table 3 (pp. 04–05) |

## D1 — Ewing sarcoma is `9364/3`. Settled, not provisional.

ICD-O-3.2 deleted `9260/3`. IARC *Deleted codes and their terms* (9 October 2020), p. 6:
"9260/3 Ewing sarcoma, Ewing tumor — Moved to 9364/3". *Summary of main changes*: 9260 survives
only because `9260/0` Aneurysmal bone cyst was introduced. Ruling 5 settles retired codes by
ICD-O-3.2. WHO 2020 Table 1 agrees: Ewing sarcoma `9364/3`.

**Consequence the registrar needs to see.** ICCC-2017 files `9364` at bone in **VIIIc2**
"Peripheral neuroectodermal tumor (pPNET) of bone" (range 65), and `9260` in VIIIc1 (range 63).
Coded to ICD-O-3.2, every Ewing sarcoma of bone lands in VIIIc2. VIIIc1 then holds only
`9365/3` Askin tumour. The tool emits what the table says. Whether the registry reports VIIIc1
and VIIIc2 combined is a reporting decision.

## D2 — "Askin tumour" in the report → `9365/3`, as written.

WHO 2020 has no Askin entity; it is chest-wall Ewing sarcoma. ICD-O-3.2 still carries
`9365/3 Askin tumor` as a preferred term. **Taken:** code the stated term (ICD-O practice) →
`9365/3`, VIIIc1. A chest-wall Ewing sarcoma reported as Ewing sarcoma is `9364/3`.
**PROVISIONAL.** Agreed with the Group IX session for soft tissue (IXd1).

## D3 — Chondrosarcoma grade 1 (axial skeleton). PROVISIONAL.

| Source | Says |
|---|---|
| WHO 2020 Table 1 | Atypical cartilaginous tumour `9222/1` (appendicular); **Chondrosarcoma, grade 1 `9222/3`**, marked "approved by the IARC/WHO Committee for ICD-O at its meeting in January 2020" |
| ICD-O-3.2 final, and IARC *New codes and their terms* p. 2 | `9222/1` carries both *Atypical cartilaginous tumor* and *Chondrosarcoma, grade 1 (C40._, C41._)*. **No `9222/3`.** |
| ICCC-2017 range 61 | admits `9222` at behaviour 3 |
| Anderson & Doyle 2021, p. 652 | ACT restricted to the appendicular skeleton; "chondrosarcoma, grade 1" for axial tumours |

Options:
- **A — ICD-O-3.2 literally.** Grade 1 at any site → behaviour exclusion `9222/1`, registrar
  decision required. Faithful to Layer 1. Drops a tumour WHO calls malignant out of the
  malignant registry.
- **B — `9220/3` Chondrosarcoma, NOS.** Keeps it malignant and registered. Contradicts
  ICD-O-3.2's explicit placement of the grade 1 term under `9222/1`.
- **C — emit `9222/3`.** Not in `icdo32.sqlite`; the build's round-trip check fails it by
  design (standing rule 1). Not available without a registrar ruling and a Layer 1 change.

**Taken: A**, with the branch worded so the clerk sees the conflict and the registrar flag.
Paediatric exposure is small: conventional chondrosarcoma is an adult tumour (Diagnostic
Pathway §3, VIIIb). The branch is one option and switches to B or C by editing one block.

## D4 — Atypical cartilaginous tumour → behaviour exclusion `9222/1`. Settled.

WHO 2020 and ICD-O-3.2 agree. Group VIII declares behaviour 3 only.

## D5 — Undifferentiated pleomorphic sarcoma of bone → `8830/3`. PROVISIONAL.

WHO 2020 Table 1 prints *Pleomorphic sarcoma, undifferentiated* `8802/3`. ICD-O-3.2 prints
*Undifferentiated high grade pleomorphic sarcoma of bone (C40._, C41._)* as a synonym on
`8830/3`. ICCC-2017 admits `8830` at bone (VIIId1, range 66) and has **no** bone range for
`8802` (VIIIe range 71 lists 8800, 8801, 8803–8805; IXe range 93 excludes 400–419). **Taken:**
`8830/3`. The tool codes to ICD-O-3.2, and ICD-O-3.2 has the bone-specific term. The Group IX
session codes soft-tissue UPS `8802/3`; the two do not conflict.

## D6 — CIC-rearranged, BCOR-altered and EWSR1–non-ETS round cell sarcomas → `8803/3`. PROVISIONAL.

WHO 2020 Table 1: `9366/3*`, `9367/3*`, `9368/3*`, all asterisked. None is in
`icdo32.sqlite` or any ICCC-2017 range. Coding them to Ewing sarcoma would contradict WHO 2020,
which classifies them separately from Ewing sarcoma (Anderson & Doyle 2021, p. 650). **Taken:**
`8803/3` Small cell sarcoma, via its ICD-O-3.2 synonym *Round cell sarcoma, NOS*, VIIIe at
bone. The Diagnostic Pathway's `9260`/`8002` suggestion is superseded: `9260/3` no longer
exists, and `8803` names the sarcoma line where `8002` does not. Agreed with the Group IX
session (IXe at soft tissue).

## D7 — Poorly differentiated chordoma → `9370/3`. Settled.

WHO 2020 Table 1 prints `9370/3` for poorly differentiated chordoma. The Diagnostic Pathway
(§1, §4E, §8 item 6) says it has no code. The pathway is wrong on this point. Anderson &
Doyle 2021, pp. 653–654: occurs in children at the skull base and upper cervical spine;
brachyury and keratins positive; SMARCB1 (INI1) lost.

## D8 — Subtype terms ICD-O-3.2 still codes separately. PROVISIONAL.

WHO 2020 Table 1 lists telangiectatic and small cell osteosarcoma under *Osteosarcoma
`9180/3`*, and chondroid chordoma under *Conventional chordoma `9370/3`*. Anderson & Doyle 2021,
p. 653: small cell and telangiectatic osteosarcoma "are now described as variants of
osteosarcoma rather than as separate entities". ICD-O-3.2 still carries `9181`, `9182`,
`9183`, `9185` and `9371` as live preferred terms. **Taken:** code the term as written.
A report naming the subtype gets the specific ICD-O-3.2 code, the term-as-written convention
the registry already uses. The specific codes are live in ICD-O-3.2 and in ICCC-2017 VIIIa/VIIId2.

## D9 — "Conventional osteosarcoma" → `9180/3`. PROVISIONAL.

WHO 2020 Table 1 puts conventional osteosarcoma at `9180/3`. ICD-O-3.2 carries
*Conventional central osteosarcoma* as a synonym on `9186/3`. **Taken:** the WHO term
"conventional osteosarcoma" → `9180/3`. A report that says "central", "conventional central"
or "medullary" osteosarcoma reaches `9186/3` by alias, as written.

## D10 — No imaging-only chondrosarcoma route. PROVISIONAL.

Visser Table 3 allows `9220/3` at C40/C41 on clinical investigation (basis 2). Sharif B, et
al. Eur J Radiol 2021;137:109579, PDF p. 4: in 17 paediatric central chondrosarcomas, MRI and
surgical grade disagreed in 47%. Paediatric enchondromas are commonly expansile, and "some of
the MRI features used to differentiate high-grade CS from ACT in adults cannot be applied to
children". **Taken:** the only imaging-sufficient code is `9180/3`. An imaging-only cartilage
lesion is `8000/3` at basis 2 when the report calls malignancy likely. Under Visser rule 4 it
is not registered when a benign cartilage tumour is in the differential.

## D11 — Intermediate tumours are behaviour exclusions. PROVISIONAL.

Giant cell tumour of bone `9250/1`, atypical cartilaginous tumour `9222/1`, aggressive
osteoblastoma `9200/1`, chondroblastoma `9230/1`, desmoplastic fibroma `8823/1`,
osteochondromatosis `9210/1`, chondromatosis `9220/1`. Group VIII declares behaviour 3 only, so
none can be emitted. Each terminal names its ICD-O-3.2 code and preferred term and sets
`registrar_decision_required`, following the Group IV `behaviour_exclusion` precedent. Whether
the registry records intermediate bone tumours outside ICCC-3 is the registrar's decision.

## D12 — Osteofibrous dysplasia-like adamantinoma → not reportable. PROVISIONAL.

Anderson & Doyle 2021, p. 654: the osteofibrous dysplasia-like variant "has now been classified
as an intermediate-category (locally aggressive) neoplasm". ICD-O-3.2 has only `9261/3`.
WHO 2020 Table 1's intermediate rows do not list the variant. **Taken:** `non_reportable`,
with the reason stating it is intermediate and the code question is open. Classic and
dedifferentiated adamantinoma → `9261/3`.

## D13 — Odontogenic malignancies. PROVISIONAL where marked.

Soluk-Tekkesin & Wright 2022, Table 1, malignant odontogenic tumours, mapped to ICD-O-3.2 by
term:

| WHO 2022 entity | ICD-O-3.2 | How the term matches |
|---|---|---|
| Ameloblastic carcinoma | `9270/3` | synonym |
| Primary intraosseous carcinoma, NOS | `9270/3` | synonym |
| Sclerosing odontogenic carcinoma | `9270/3` | **no term**; nearest is the synonym *Odontogenic carcinoma*. PROVISIONAL |
| Clear cell odontogenic carcinoma | `9341/3` | preferred (behaviour moved from /1 in ICD-O-3.2) |
| Ghost cell odontogenic carcinoma | `9302/3` | preferred (new in ICD-O-3.2) |
| Odontogenic carcinosarcoma | `9342/3` | preferred |
| Odontogenic sarcomas: ameloblastic fibrosarcoma | `9330/3` | preferred |
| Odontogenic sarcomas: ameloblastic fibrodentinosarcoma, fibro-odontosarcoma | `9290/3` | synonyms |

WHO 2022 places **metastasizing ameloblastoma** among the benign epithelial odontogenic
tumours. ICD-O-3.2 codes it `9310/3` *Ameloblastoma, metastasizing*. **Taken:** `9310/3`,
because the case has metastasised and ICD-O-3.2 gives behaviour 3. PROVISIONAL. The same paper
gives median ages of 49 and 53 for the two commonest carcinomas, so these are adult tumours.
They get one node, not a reasoning tree.

## D14 — ICD-O-3.2 codes with no WHO 2020 bone entity stay in the inventory, off the tree.

`9230/3` Chondroblastoma, malignant; `9195/3` Intracortical osteosarcoma; `9231/3` Myxoid
chondrosarcoma (WHO's entity is extraskeletal); `8811/3` Myxofibrosarcoma; `8812/3`
Periosteal fibrosarcoma; `8804/3` Epithelioid sarcoma. All are live ICD-O-3.2 terms inside
ICCC-2017 VIII ranges, so the generator keeps them and the alias layer reaches them on the
report's own wording. None has a WHO 2020 bone-chapter entity, so the tree builds no branch
to them. This applies the Group 3 test as written: a code leaves the **tree**, not the
**inventory**.

## D15 — Pre-analytic decalcification is a hint, not a variable. Deviation from the pathway.

The Diagnostic Pathway §4A and §7.3 propose a `decalcification_status` variable wired into the
FOS, brachyury and H3.3 G34W rules. Rulings 11 and 12 already make an unreadable stain drop to
the nearest code, and every marker offers `nd` (not done or not readable). **Taken:** no new
variable. Each affected marker's hint tells the clerk to answer `nd` when the report calls the
stain non-contributory after decalcification. The tree never reads FOS or H3.3 G34W as a
code-setting rule, so the variable would have nothing to gate.

## Tree shape

One tree, `g8_bone`, prefix `bn_`, entered from the router's existing `tumour_origin = bone`
and C40–C41 site path. No tree routing: every Group VIII tumour sits at C40–C41, so site
cannot pick a tree (Diagnostic Pathway §0 point 1).

```
bn_document_inventory
 ├─ referral only ──────────► bn_clinical_alias ── 8000/3 basis 1 · not registrable · → imaging
 ├─ imaging, no tissue ─────► bn_imaging_line ─┬─► bn_imaging_os (imaging_pathway) ── 9180/3 basis 2
 │                                             ├─ 8000/3 basis 2 (malignant, not osteosarcoma)
 │                                             └─ not registrable (benign in differential)
 ├─ cytology only ──────────► bn_cytology ── 8001/3 basis 5 · → imaging
 └─ histology ──────────────► bn_histology_line  (the matrix router)
        ├─ bone-forming ──────► bn_osteosarcoma      9180–9194 · behaviour exclusions
        ├─ cartilage ─────────► bn_cartilage ─► bn_cartilage_benign
        ├─ small round cell ──► bn_round_cell ─► bn_round_cell_ihc (ihc_checklist, fallback 8002/3)
        ├─ notochordal ───────► bn_chordoma           9370 · 9371 · 9372 · 9370/0 exclusion
        ├─ giant cell-rich ───► bn_giant_cell         9250/3 · 9250/1 · 9230/1 · 9260/0 · 8003/3
        ├─ spindle/pleomorphic► bn_spindle            8830/3 · 8810/3 · 8801/3 · 8805/3 · 8004/3 · refer IX
        ├─ fibro-osseous tibia► bn_adamantinoma       9261/3 · not reportable
        ├─ odontogenic ───────► bn_odontogenic        9270 · 9290 · 9302 · 9310 · 9330 · 9341 · 9342
        ├─ vascular / smooth muscle sarcoma ─ refer Group IX
        ├─ lymphoma, plasmacytoma, Langerhans cell histiocytosis ─ refer Group II
        ├─ metastasis ────────► bn_metastasis         refer IV / IX / XII
        ├─ sarcoma NOS ─ 8800/3 · malignant NOS ─ 8000/3
        └─ no tumour (infection, fracture, reactive) ─ not reportable
```

## What was weighed and not taken

- **Four sub-trees dispatched by matrix** (Diagnostic Pathway §7.2). One tree with a router
  node does the same job and reuses the Group VI shape the engine already drives. Four trees
  would need `tree_selection`, which only Group 4 exercises.
- **A FOS checklist to separate osteoblastoma from osteosarcoma** (Diagnostic Pathway §2E,
  §7.7). FOS is "supportive, not definitive" (Lam 2020), so it can never set a code. A report
  that leaves the question open is not registrable under Visser rule 4 until the final report
  arrives.
- **An imaging route for chondrosarcoma** (D10).
