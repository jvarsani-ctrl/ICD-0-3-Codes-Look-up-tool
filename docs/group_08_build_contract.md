# Group 8 build contract — Malignant Bone Tumours

**Branch:** `claude/group-8-tumor-pathway-64edbc`, a worktree cut from `main` at `cff8149`.
`main` stays untouched until the registrar merges.

**Written 2 October 2026, before any JSON was authored.** Everything in §0 was verified on that
date against `icdo32.sqlite`, `ICCC-2017.sqlite`, the four IARC 3.1→3.2 change documents, the
REDCap dictionary snapshot of 1 October 2026 and the sources named in §10. The code decisions
are argued in `docs/superpowers/specs/2026-10-02-group-08-bone-code-decisions-design.md` (D1–D15)
and are not repeated here. Everything that needs the registrar is in
`docs/group_08_registrar_review.md`.

> **Standing rule, inherited.** Advisory tools must never overstate evidence. This group has a
> sharp instance of it in Layer 1: REDCap's `viii_morph` pick 33 reads "9260 - Ewing sarcoma",
> and ICD-O-3.2's `9260` is *Aneurysmal bone cyst*, a benign lesion (§2).

---

## 0. Pre-context

### 0.1 What this group is

ICCC-3 Group VIII, **Malignant bone tumours**. Osteosarcoma and Ewing sarcoma account for most
paediatric cases. Everything else is rare in children: conventional chondrosarcoma, chordoma
(except the poorly differentiated subtype), adamantinoma, malignant giant cell tumour and the
odontogenic carcinomas.

### 0.2 ★ The ICCC-3 definition, read off `ICCC-2017.sqlite`

`code_ranges` for `main_group = 'VIII'`, verbatim (ranges 59–71):

| Range | Subgroup | Morphology | Topography | Behaviour |
|---|---|---|---|---|
| 59 | VIIIa Osteosarcomas | `9180-9187,9191-9195,9200` | `400-419,760-768,809` | 3 |
| 60 | VIIIb Chondrosarcomas | `9210,9220,9240` | `400-419,760-768,809` | 3 |
| 61 | VIIIb | `9211-9213,9221,9222,9230,9241-9243` | `000-809` | 3 |
| 62 | VIIIb | `9231` | `400-419` | 3 |
| 63 | VIIIc1 Ewing tumor and Askin tumor of bone | `9260` | `400-419,760-768,809` | 3 |
| 64 | VIIIc1 | `9365` | `400-419` | 3 |
| 65 | VIIIc2 pPNET of bone | `9364` | `400-419` | 3 |
| 66 | VIIId1 Malignant fibrous neoplasms of bone | `8810,8811,8818,8823,8830` | `400-419` | 3 |
| 67 | VIIId1 | `8812,9262` | `000-809` | 3 |
| 68 | VIIId2 Malignant chordomas | `9370-9372` | `000-809` | 3 |
| 69 | VIIId3 Odontogenic malignant tumors | `9270-9275,9280-9282,9290,9300-9302,9310-9312,9320-9322,9330,9340-9342` | `000-809` | 3 |
| 70 | VIIId4 Miscellaneous malignant bone tumors | `9250,9261` | `000-809` | 3 |
| 71 | VIIIe Unspecified malignant bone tumors | `8000-8005,8800,8801,8803-8805` | `400-419` | 3 |

What follows from it:

1. **Group VIII declares behaviour 3 and nothing else.** Every benign and intermediate bone
   tumour is outside the group by the recode's own definition. Twenty-eight of the 76 range
   codes exist in ICD-O-3.2 only below behaviour 3.
2. **`9260` no longer reaches the group.** ICD-O-3.2 deleted `9260/3` (§0.4). Ewing sarcoma is
   `9364/3`, range 65, subgroup **VIIIc2**.
3. **`8802` has no bone range.** VIIIe skips it and IXe (range 93) excludes `400-419`. The
   ICD-O-3.2 bone term for undifferentiated pleomorphic sarcoma sits on `8830/3` (D5).
4. **VIIIe is C40–C41 only.** `8000/3` at a bone site is VIIIe. The router's `8000-8005` rule
   defaults to Group XII, and ICCC-2017's XIIb (range 143) excludes `400-419`, so the rule gets
   a bone branch (§7). The branch is a record, not a fix: app.js reads resolveGroup() only for
   its `note`, and the group on screen comes from the tree and the entry.

### 0.3 ★ The inventory — 48 usable codes, generated

`build/generate_group_inventory.py --group VIII`, 2 October 2026:

```
ICCC range entries 76 · distinct codes 76 · absent from ICD-O-3.2 28 · usable 48 · (code,behaviour) records 48
```

"Absent" means **absent at behaviour 3**, the same wording trap Groups IV, V and VI record. The
28: `8818 8823 9191 9200 9210 9211 9212 9213 9222 9241 9260 9262 9271 9272 9273 9274 9275 9280
9281 9282 9300 9301 9311 9312 9320 9321 9322 9340`. Every one exists in ICD-O-3.2 at /0 or /1
except `9260`, which exists only at /0 as *Aneurysmal bone cyst*.

The 48 usable records by subgroup, counted from the generator's output: VIIIa 12 · VIIIb 7 ·
VIIIc1 1 (`9365`) · VIIIc2 1 (`9364`) · VIIId1 4 · VIIId2 3 · VIIId3 7 · VIIId4 2 · VIIIe 11.

### 0.4 ICD-O-3.2 changed this group, checked against the IARC documents

| Change | Source |
|---|---|
| `9260/3` Ewing sarcoma, Ewing tumor **deleted**, "Moved to 9364/3" | *Deleted codes and their terms*, 9 Oct 2020, p. 6 |
| `9260` kept only for new `9260/0` Aneurysmal bone cyst | *Summary of main changes*; *New codes and their terms*, p. 3 |
| `9222/1` new: *Atypical cartilaginous tumor*, *Chondrosarcoma, grade 1 (C40._, C41._)* | *New codes and their terms*, p. 2 |
| `9230/0` Chondroblastoma moved to `/1` | *Terms that are changing behaviour* |
| `9341/1` Clear cell odontogenic tumor moved to `/3` | *Terms that are changing behaviour*, p. 4 |
| `9302/3` Ghost cell odontogenic carcinoma, `9341/3` Clear cell odontogenic carcinoma new | *New codes and their terms* |
| `9370/0` Benign notochordal cell tumour new | *New codes and their terms* |
| `9211/0` Osteochondromyxoma, `9212/0`, `9213/0` new; `8818/0` Fibrous dysplasia new | *New codes and their terms*, p. 2 |

### 0.5 The engine facts that shape every node

Unchanged from Group 6 build contract §0.8–§0.9, and not re-derived here: `when` is string
equality; `resolution_logic[]` is flat and first-match-wins; `imaging_features` on a node is a
checklist where **every** box must be ticked; `diversion_criteria` fire on **any** one;
`clinical_alert` is `null` everywhere (ruling 9); NOS fallback is required on `ihc_checklist`
and forbidden on `document_inventory`, `clinical_alias`, `morphology_only`, `imaging_pathway`
and `histology_subclassification`; `refer_group` carries no code and puts its text in `reason`;
`behaviour_exclusion` names the ICD-O-3.2 **preferred** term at its (code, behaviour) pair.

### 0.6 ★ Visser Table 3 — what may be registered without tissue

Visser O, et al. Front Oncol 2023;13:1250549, Table 3, pp. 04–05: *Osteosarcoma ·
chondrosarcoma, basis 2, C40, C41, `9180/3` · `9220/3`, Group VIII.* Rule 5 (p. 03): anything
else without pathology is `8000/3`. Rule 4 (p. 03): "possible" is not registrable.

This build uses **`9180/3` only** as an imaging-sufficient code (D10). Ewing sarcoma is not in
Table 3, so a permeative lesion on imaging alone is `8000/3` at basis 2. No Group VIII terminal
emits basis 1 except `8000/3` from the referral node, which rule 5 permits.

---

## 1. The inventory is generated, never transcribed

`morphology_entries[]` comes from `build/generate_group08_entries.py`, which calls
`build_inventory()` with `group="VIII"` and adds the annotation layer keyed by code. It reads
`ICCC_DB` and `ICDO_DB` from the environment when set, because this worktree sits two levels
below the repository's usual vault position. The tree is authored in the same script's
`TREE` structure and written beside the entries. After any change, run
`python3 build/induce_flow.py`.

`morphology_name` is the ICD-O-3.2 preferred term (Group 6 convention). REDCap strings that
differ go to the alias file and to `docs/group_08_layer1_repair.md`.

---

## 2. ★ Layer 1 conflict — `viii_morph` against ICD-O-3.2

99 options, 72 distinct codes. Generated 2 October 2026 from the option file and confirmed
character-identical to `REDCap Registry/snapshots/2026-10-01/data_dictionary.csv`.

| Class | Count | What |
|---|---|---|
| Exact ICD-O-3.2 preferred term at /3 | 39 | correct as they stand |
| Valid /3 term, not the preferred one | 6 | `9187` "Intraosseous well differentiated osteosarcoma", `9221` "Juxtacortical chondrosarcoma", `9364` "Peripheral neuroectodermal tumor", `8811` "Fibromyxosarcoma", `9310` "Ameloblastoma, malignant", `9341` "Clear cell odontogenic tumor" |
| /3 string drift, no exact match | 2 | `9186` "Central osteosarcoma" (ICD-O-3.2: *Central osteosarcoma, NOS*); `8804` "Epithelioid sarcoma" (*Epithelioid sarcoma, NOS*) |
| Behaviour exclusion — the term exists below /3 | 49 | 47 exact, plus `8811` "Fibromyxoma" and `8830` "Benign fibrous histiocytoma", which match /0 terms bar the ", NOS" suffix |
| ★ Retired number | 1 | pick 33 **`9260` "Ewing sarcoma"** — `9260` is now *Aneurysmal bone cyst*, /0 |
| ★ Wrong number | 2 | picks 18–19 **`9211`** "Juxtacortical chondroma" / "Juxtacortical chondrosarcoma" — `9211` is *Osteochondromyxoma* /0; both terms belong to `9221`, already offered at picks 22 and 24 |
| ★ /3 codes the tool emits with no option naming them | 3 | **`9220/3` Chondrosarcoma, NOS** (the only `9220` options are /0 and /1 terms); **`9302/3` Ghost cell odontogenic carcinoma** (the only `9302` option is the /0 synonym); **`9364/3` "Ewing sarcoma"** (pick 35 carries the right number under a synonym, and pick 33 offers the term on the wrong number) |

All 48 inventory codes are present in `viii_morph` **by number**, so nothing needs an
`awaiting_layer1` declaration: `check_codes_against_source_of_truth()` is a code-level test.
The name-level gaps are the repair package's business.

---

## 3. The code decisions this group forces

D1–D15 in the design document. In one line each:

| | Decision | Status |
|---|---|---|
| D1 | Ewing sarcoma `9364/3`, VIIIc2 | settled (ICD-O-3.2) |
| D2 | "Askin tumour" as written `9365/3`, VIIIc1 | provisional |
| D3 | Chondrosarcoma grade 1 → behaviour exclusion `9222/1` | provisional |
| D4 | Atypical cartilaginous tumour → behaviour exclusion `9222/1` | settled |
| D5 | Undifferentiated pleomorphic sarcoma of bone `8830/3` | provisional |
| D6 | CIC / BCOR / EWSR1–non-ETS round cell sarcomas `8803/3` | provisional |
| D7 | Poorly differentiated chordoma `9370/3` | settled (WHO 2020 Table 1) |
| D8 | Subtype terms coded as written to ICD-O-3.2's specific code | provisional |
| D9 | "Conventional osteosarcoma" `9180/3` | provisional |
| D10 | No imaging-only chondrosarcoma; imaging-sufficient is `9180/3` only | provisional |
| D11 | Intermediate tumours → behaviour exclusions | provisional |
| D12 | Osteofibrous dysplasia-like adamantinoma → not reportable | provisional |
| D13 | Odontogenic carcinomas mapped by term; metastasizing ameloblastoma `9310/3` | provisional |
| D14 | Codes with no WHO 2020 bone entity stay in the inventory, off the tree | settled (Group 3 test) |
| D15 | Decalcification is a hint, not a variable | deviation from pathway |

---

## 4. Tree architecture

One tree, `g8_bone`, entry `bn_document_inventory`, topography `C40.0–C41.9`. Diagram in the
design document.

| Node | Type | Reached from | Emits / routes |
|---|---|---|---|
| `bn_document_inventory` | `document_inventory` | router handoff | → clinical alias · imaging line · cytology · histology line |
| `bn_clinical_alias` | `clinical_alias` | referral only | `8000/3` basis 1 · not registrable · → imaging line |
| `bn_imaging_line` | `morphology_only` | imaging, inadequate specimen | → imaging osteosarcoma · `8000/3` basis 2 · not registrable · → histology · → cytology |
| `bn_imaging_os` | `imaging_pathway` | imaging line | `9180/3` basis 2; insufficient → `bn_imaging_insufficient` |
| `bn_imaging_insufficient` | `morphology_only` | imaging osteosarcoma | `8000/3` basis 2 · not registrable · → histology · → cytology |
| `bn_cytology` | `morphology_only` | cytology only | `8001/3` basis 5 · → imaging line |
| `bn_histology_line` | `histology_subclassification` | histology | the matrix router — eleven lines, three referrals, two NOS codes, one non-reportable |
| `bn_osteosarcoma` | `histology_subclassification` | bone-forming | `9180 9181 9182 9183 9184 9185 9187 9192 9193 9194` · exclusions `9191/0`, `9200/0`, `9200/1` · not registrable (unresolved) |
| `bn_cartilage` | `histology_subclassification` | cartilage | `9220 9221 9240 9242 9243` · exclusion `9222/1` ×2 · → benign cartilage · not registrable (unresolved) |
| `bn_cartilage_benign` | `morphology_only` | cartilage | exclusions `9220/0 9220/1 9221/0 9210/0 9210/1 9241/0 9230/1` |
| `bn_round_cell` | `morphology_only` | small round cell | `9364` (basis 7 or 8) · `9365` · `8803` · `9185` · `9240` · refer II / IV / IX · → IHC |
| `bn_round_cell_ihc` | `ihc_checklist` | round cell, descriptive report | `9364` · `8803` · refer II / IV / IX · fallback `8002/3` |
| `bn_chordoma` | `histology_subclassification` | notochordal | `9370` ×2 · `9371` · `9372` · exclusion `9370/0` |
| `bn_giant_cell` | `histology_subclassification` | giant cell-rich | `9250/3` · exclusions `9250/1`, `9230/1`, `9260/0` · not reportable · `8003/3` |
| `bn_spindle` | `histology_subclassification` | spindle or pleomorphic | `8830/3` · `8810/3` · `8801/3` · `8805/3` · `8004/3` · refer IX · exclusions `8823/1`, `8818/0` |
| `bn_adamantinoma` | `histology_subclassification` | fibro-osseous, tibia or fibula | `9261/3` ×2 · not reportable ×2 |
| `bn_odontogenic` | `histology_subclassification` | odontogenic | `9270` ×4 · `9290` · `9302` · `9310` · `9330` · `9341` · `9342` · exclusion `9310/0` · not reportable |
| `bn_metastasis` | `morphology_only` | metastatic deposit in bone | refer IV · refer IX · refer XII |

`bn_round_cell_ihc` is the only `ihc_checklist`. Its rules, first match wins:

| # | Positive | Result | Source |
|---|---|---|---|
| 1 | TdT | refer Group II (lymphoblastic lymphoma) | Kallen & Hornick 2022, p. 30 |
| 2 | PHOX2B | refer Group IV (neuroblastoma) | p. 30; Table 1 |
| 3 | Myogenin or MyoD1 | refer Group IX (rhabdomyosarcoma) | p. 30; Table 1 |
| 4 | SS18::SSX | refer Group IX (synovial sarcoma) | Table 1 |
| 5 | FET::ETS fusion (EWSR1::FLI1, EWSR1::ERG, FUS::ERG and others) | `9364/3` basis 8 | Table 2; WHO 2020 |
| 6 | EWSR1 or FUS fused to a non-ETS partner (NFATC2, PATZ1) | `8803/3` basis 8 | Table 2; D6 |
| 7 | CIC rearrangement | `8803/3` basis 8 | Table 2; D6 |
| 8 | BCOR::CCNB3 fusion or BCOR internal tandem duplication | `8803/3` basis 8 | Table 2; D6 |
| 9 | ETV4 | `8803/3` (CIC-rearranged sarcoma) | Table 1, p. 34 caption |
| 10 | BCOR (diffuse nuclear) | `8803/3` (BCOR-altered sarcoma) | Table 1; p. 33 |
| 11 | CD99 (strong, diffuse, membranous) **and** NKX2-2 | `9364/3` basis 7 | p. 31 |
| — | fallback | `8002/3` Malignant tumor, small cell type | D6; Diagnostic Pathway §1 VIIIe |

Rule 11 sits after the molecular rules. EWSR1 break-apart FISH alone does not name the partner,
and EWSR1–non-ETS sarcomas and CIC-rearranged sarcomas express CD99 too (Kallen & Hornick
2022, pp. 33–34). A CD99-positive tumour with NKX2-2 negative or not done falls to `8002/3`:
"If this pattern is lacking, the diagnosis of Ewing sarcoma is highly unlikely" (p. 31) states
the converse, not the sufficiency.

---

## 5. What the Diagnostic Pathway gets wrong

The pathway (13 June 2026) predates the ICD-O-3.2 conversion. Ruling 7 says the latest
document wins, and ruling 5 settles retired codes by ICD-O-3.2.

1. **Ewing sarcoma is `9260` throughout.** It is `9364/3` (§0.4). The pathway's "9364/9365
   legacy aliases of 9260" (§4F, §7.4) inverts the current coding.
2. **"Poorly differentiated chordoma has no code"** (§1, §4E, §8.6). WHO 2020 Table 1 prints
   `9370/3`.
3. **"Ewing-like sarcomas collapse to 9260 / 8002"** (§4D). WHO 2020 assigns `9366`–`9368`,
   which ICD-O-3.2 lacks; the tool codes `8803/3` (D6).
4. **Chondroblastoma is `/0`** (§1). ICD-O-3.2 moved it to `/1`.
5. **Giant cell tumour of bone is listed in VIIId4 as if reportable.** Only `9250/3` is; the
   conventional tumour is `9250/1`, outside the group.
6. **Five malignant odontogenic codes.** ICD-O-3.2 carries seven at /3, adding `9302/3` and
   `9341/3`.
7. **`9221` is offered as `/0 ; /3` and `9211` is not questioned.** `9211` is now
   *Osteochondromyxoma*.
8. **`clinical_alert` strings** on 9180, 9250, 9370, 9200 and 9260 (§4A–§4H). Ruling 9 moved all
   warnings out of the tool; they go to `docs/clinical-warnings.md`, Group VIII section.
9. **A `decalcification_status` variable** (§4A, §7.3). Not built (D15).
10. **Imaging-sufficient chondrosarcoma.** Not built (D10).

---

## 6. The alias layer

`data/aliases/aliases_group_08.json`, same schema as Group 6. Coverage:

- every ICD-O-3.2 preferred term, synonym and related term on the 48 usable records;
- every `viii_morph` string that differs from the preferred term (§2), resolving to the code
  ICD-O-3.2 gives it, with the drift stated in `notes`;
- the WHO 2020 and WHO 2022 names the tree uses (conventional osteosarcoma, secondary
  osteosarcoma, poorly differentiated chordoma, CIC-rearranged sarcoma, BCOR sarcoma,
  sclerosing odontogenic carcinoma, undifferentiated pleomorphic sarcoma of bone);
- **`Ewing sarcoma` → `9364`**, never `9260`.

Benign and intermediate terms are not aliased to a code. The express lane is for codes this
group emits; benign entities are reached through the tree's behaviour exclusions.

---

## 7. Shared-layer changes

Agreed with the Group VII and Group IX sessions on 2 October 2026. Group VIII owns
`dual_group_rules["9260"]`, any `9180/9220/9231/9240` rule and the `tumour_origin`
discriminator. Group IX stays off them.

| File | Change |
|---|---|
| `data/shared/presentation_router.json` | `groups["8"]` → `built: true`, tree `g8_bone`, handoff |
| | `dual_group_rules["9260"]` re-keyed to `9364,9365` with the VIIIc2/VIIIc1 and IXd2/IXd1 subgroups ICCC-2017 gives each |
| | `dual_group_rules["8000-8005"]` gains one branch: C40.0–C41.9 → group 8, VIIIe. Group VII appends a disjoint C22 branch |
| | `discriminators.tumour_origin.authoring_note` names `9364`, not `9260` |
| `data/shared/topography_codes.json` | add `C40.0`, `C40.1`, `C40.2`, `C40.3`, `C40.8`, `C41.8` with REDCap codes `400 401 402 403 408 418` read from `Topography Redcap.md`, and add them to the `bone` crosswalk row. Today the file lacks C40.2, the commonest osteosarcoma and Ewing sarcoma site. |
| `build/build_database.py` | `GROUP8 = 8`; `BEHAVIOUR_DECLARED_BY_GROUP[GROUP8] = {"3"}`; `GROUP8` joins the `check_icdo32_round_trip()` and `check_redcap_exact_names()` guards; the Group VIII rules in §8 |
| `docs/clinical-warnings.md` | Group VIII section |
| `data/aliases/alias_index.json` | regenerated by the build and committed (standing rule 15) |

The Group IX session expects text conflicts on the `build_database.py` guard lines. Keep both.

---

## 8. Validation rules this group adds

Scoped to Group 8, a no-op on every other group's file, each proved with a negative control
recorded in `docs/validator_negative_controls.md`.

1. **`check_group8_no_retired_ewing_code`** — no branch, fallback, alias target or
   `behaviour_exclusion` other than the `9260/0` aneurysmal bone cyst exclusion names `9260`.
   Keyed off ICD-O-3.2: the check reads which behaviours `9260` has in `icdo32.sqlite`.
2. **`check_group8_no_pathology_codes`** — every terminal reached with no tissue
   (`basis_of_diagnosis` 1 or 2) emits `9180/3` or `8000/3`, and basis 1 is `8000/3` only
   (Visser rules 4–5, Table 3; D10).
3. **`check_group8_ewing_requires_partner`** — no `ihc_checklist` rule emitting `9364` may fire
   on CD99 alone: it must also require NKX2-2 or a FET::ETS fusion. Keyed off the rule's own
   `positive[]`, against the condition, never the destination.

---

## 9. Proof before this group is called done

1. `python3 build/build_database.py` → 0 FAIL.
2. `python3 build/induce_flow.py` → every rule has a witness.
3. A negative control on each §8 rule.
4. Drive the tree in the browser: osteosarcoma on imaging, Ewing sarcoma on a descriptive
   report with markers, chondrosarcoma grade 1, a referral out to Group II.
5. Groups 1–7 and 9–12 byte-identical to `main` except the shared files in §7.

---

## 10. The baseline document

`docs/group_baseline_documents.md` assigns Group VIII the Sbaraglia 2020 soft-tissue paper and
flags that it does not cover bone. This build resolves the gap without a new purchase:

| Need | Source used | Held |
|---|---|---|
| WHO 2020 bone entities with ICD-O codes | WHO 2020 Table 1, reproduced with WHO/IARC permission in the ICCR *Primary tumour in bone — resection* dataset, histological tumour type note, pp. 1–2 | downloaded 2 Oct 2026; not committed (WHO copyright) |
| WHO 2020 bone narrative | Anderson & Doyle, Histopathology 2021;78(5):644–657 | `Group 8 Papers/` |
| WHO 2022 odontogenic entities | Soluk-Tekkesin & Wright, Turk Patoloji Derg 2022;38(2):168–184, Table 1 | read via Europe PMC, PMC9999699 |
| Registry-implications paper | none exists (`Group 8 Papers/Group 8 — Registry-Implications MeSH Search Results.md`, 32 records, no candidate) | — |

Choi JH, Ro JY. *The 2020 WHO Classification of Tumors of Bone: An Updated Review.* Adv Anat
Pathol 2021;28(3):119–138 (PMID 33480599) remains the natural summary paper and is paywalled.
Vered M, Wright JM. Head Neck Pathol 2022;16(1):63–75 (PMC9019005) could not be read: the
publisher withholds the XML and the PMC page served a CAPTCHA. Both are on the registrar's list.

---

## 11. Tasks

- [x] T1 `build/generate_group08_entries.py` → `group_08_dt.json` entries and metadata
- [x] T2 the tree, in the same script, then `induce_flow.py`
- [x] T3 `aliases_group_08.json`
- [x] T4 router and topography changes (§7)
- [x] T5 `build_database.py` registration and the three §8 rules
- [x] T6 `docs/clinical-warnings.md` Group VIII section; `docs/group_08_layer1_repair.md`
- [x] T7 build, negative controls, browser drive
- [x] T8 `docs/group_08_build_report.md`; registrar review file complete
