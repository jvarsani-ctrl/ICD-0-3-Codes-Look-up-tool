# Group 8 — Layer 1 Repair Package (REDCap `viii_morph`)

**Written 2 October 2026 with the Group 8 build.** Input for the REDCap Registry repository,
which owns every change to the registry's dictionary (routing table in `../../CLAUDE.md`).
Nothing here edits REDCap. Live REDCap is production and is written only on the registrar's
approval of a specific change.

**Source.** `viii_morph` in `REDCap Registry/snapshots/2026-10-01/data_dictionary.csv`, 99
choices, character-identical to `ICD coding/RedCap Options/Group 8- Malignant Bone Tumors.md`.
Every option string was compared with `icdo32.sqlite` by script; the tables below are that
script's output, not a transcription.

| Class | Picks | What |
|---|---|---|
| A | 39 | the ICD-O-3.2 preferred term at behaviour 3 — correct as they stand |
| B | 6 | a real behaviour-3 term, not the preferred one — usable, relabel when convenient |
| C | 2 | behaviour 3, but the string is not an ICD-O-3.2 term — relabel |
| D | 49 | a term that exists only below behaviour 3 — cannot be a Group VIII cancer |
| ★ E | 3 | the **number** is wrong — 9211 twice, 9260 once |
| ★ F | 2 missing | behaviour-3 codes the tool emits that no option names |

---

## 1. ★ Class E — three wrong numbers

| Pick | Option string | ICD-O-3.2 |
|---|---|---|
| 18 | `9211 - Juxtacortical chondroma` | 9211 in ICD-O-3.2: 9211/0 Osteochondromyxoma |
| 19 | `9211 - Juxtacortical chondrosarcoma` | 9211 in ICD-O-3.2: 9211/0 Osteochondromyxoma |
| 33 | `9260 - Ewing sarcoma` | 9260 in ICD-O-3.2: 9260/0 Aneurysmal bone cyst |

**Pick 33 is the most consequential defect in this list.** ICD-O-3.2 deleted `9260/3` Ewing
sarcoma and moved it to `9364/3` (IARC *Deleted codes and their terms*, 9 October 2020, p. 6).
`9260` now carries only `9260/0` *Aneurysmal bone cyst*. A clerk who searches the dropdown
for "Ewing sarcoma" finds pick 33 first and records a benign code for the second commonest
malignant bone tumour of childhood. Ewing sarcoma's correct number is already offered, at pick
35, under the synonym "Peripheral neuroectodermal tumor".

**Picks 18 and 19** carry `9211`, which ICD-O-3.2 gives to *Osteochondromyxoma* (/0, new in
ICD-O-3.2). Their two terms belong to `9221` and are already offered there, at picks 22 and 24.

## 2. ★ Class F — two codes with no option string

| Code | ICD-O-3.2 term | What `viii_morph` offers on the number |
|---|---|---|
| `9220/3` | **Chondrosarcoma, NOS** | picks 20–21: *Chondroma, NOS* (/0), *Chondromatosis, NOS* (/1) |
| `9302/3` | **Ghost cell odontogenic carcinoma** (new in ICD-O-3.2) | pick 64: *Odontogenic ghost cell tumor*, the /0 synonym |

`9220/3` is the code for chondrosarcoma grade 2 and grade 3 (WHO 2020 Table 1). Today a clerk
coding one matches the number against an option that reads "Chondroma, NOS".

## 3. Class B and C — relabel

| Pick | Option string | ICD-O-3.2 |
|---|---|---|
| 8 | `9187 - Intraosseous well differentiated osteosarcoma` | 9187/3 Related term; preferred *Low grade central osteosarcoma* |
| 24 | `9221 - Juxtacortical chondrosarcoma` | 9221/3 Related term; preferred *Periosteal chondrosarcoma* |
| 35 | `9364 - Peripheral neuroectodermal tumor` | 9364/3 Synonym term; preferred *Ewing sarcoma* |
| 39 | `8811 - Fibromyxosarcoma` | 8811/3 Related term; preferred *Myxofibrosarcoma* |
| 66 | `9310 - Ameloblastoma, malignant` | 9310/3 Synonym term; preferred *Ameloblastoma, metastasizing* |
| 75 | `9341 - Clear cell odontogenic tumor` | 9341/3 Synonym term; preferred *Clear cell odontogenic carcinoma* |

| Pick | Option string | ICD-O-3.2 |
|---|---|---|
| 7 | `9186 - Central osteosarcoma` | no exact match; 9186/3 preferred *Central osteosarcoma, NOS* |
| 98 | `8804 - Epithelioid sarcoma` | no exact match; 8804/3 preferred *Epithelioid sarcoma, NOS* |

Pick 35 needs relabelling most: the tool's output names the code *Ewing sarcoma*, and the
dropdown row for that code reads "Peripheral neuroectodermal tumor".

## 4. Class D — 49 options below behaviour 3

| Pick | Option string | ICD-O-3.2 |
|---|---|---|
| 9 | `9191 - Osteoid osteoma, NOS` | 9191/0 Preferred term *Osteoid osteoma, NOS* |
| 14 | `9200 - Osteoblastoma, NOS` | 9200/0 Preferred term *Osteoblastoma, NOS* |
| 15 | `9200 - Aggressive osteoblastoma` | 9200/1 Preferred term *Aggressive osteoblastoma* |
| 16 | `9210 - Osteochondroma` | 9210/0 Preferred term *Osteochondroma* |
| 17 | `9210 - Osteochondromatosis, NOS` | 9210/1 Preferred term *Osteochondromatosis, NOS* |
| 20 | `9220 - Chondroma, NOS` | 9220/0 Preferred term *Chondroma, NOS* |
| 21 | `9220 - Chondromatosis, NOS` | 9220/1 Preferred term *Chondromatosis, NOS* |
| 22 | `9221 - Juxtacortical chondroma` | 9221/0 Related term *Juxtacortical chondroma* |
| 23 | `9221 - Periosteal chondroma` | 9221/0 Preferred term *Periosteal chondroma* |
| 26 | `9230 - Chondroblastoma, NOS` | 9230/1 Preferred term *Chondroblastoma, NOS* |
| 30 | `9241 - Chondromyxoid fibroma` | 9241/0 Preferred term *Chondromyxoid fibroma* |
| 36 | `8810 - Fibroma, NOS` | 8810/0 Preferred term *Fibroma, NOS* |
| 38 | `8811 - Fibromyxoma` | 8811/0 Preferred term *Fibromyxoma, NOS* (option omits ', NOS') |
| 40 | `8812 - Periosteal fibroma` | 8812/0 Preferred term *Periosteal fibroma* |
| 42 | `8823 - Desmoplastic fibroma` | 8823/1 Preferred term *Desmoplastic fibroma* |
| 43 | `8830 - Benign fibrous histiocytoma` | 8830/0 Preferred term *Benign fibrous histiocytoma, NOS* (option omits ', NOS') |
| 45 | `9262 - Ossifying fibroma` | 9262/0 Preferred term *Ossifying fibroma* |
| 49 | `9270 - Odontogenic tumor, benign` | 9270/0 Preferred term *Odontogenic tumor, benign* |
| 50 | `9270 - Odontogenic tumor, NOS` | 9270/1 Preferred term *Odontogenic tumor, NOS* |
| 52 | `9271 - Ameloblastic fibrodentinoma` | 9271/0 Preferred term *Ameloblastic fibrodentinoma* |
| 53 | `9272 - Cementoma, NOS` | 9272/0 Preferred term *Cementoma, NOS* |
| 54 | `9273 - Cementoblastoma, benign` | 9273/0 Preferred term *Cementoblastoma, benign* |
| 55 | `9274 - Cementifying fibroma` | 9274/0 Related term *Cementifying fibroma* |
| 56 | `9275 - Gigantiform cementoma` | 9275/0 Preferred term *Gigantiform cementoma* |
| 57 | `9280 - Odontoma, NOS` | 9280/0 Preferred term *Odontoma, NOS* |
| 58 | `9281 - Compound odontoma` | 9281/0 Preferred term *Compound odontoma* |
| 59 | `9282 - Complex odontoma` | 9282/0 Preferred term *Complex odontoma* |
| 60 | `9290 - Ameloblastic fibro-odontoma` | 9290/0 Preferred term *Ameloblastic fibro-odontoma* |
| 62 | `9300 - Adenomatoid odontogenic tumor` | 9300/0 Preferred term *Adenomatoid odontogenic tumor* |
| 63 | `9301 - Calcifying odontogenic cyst` | 9301/0 Preferred term *Calcifying odontogenic cyst* |
| 64 | `9302 - Odontogenic ghost cell tumor` | 9302/0 Synonym term *Odontogenic ghost cell tumor* |
| 65 | `9310 - Ameloblastoma, NOS` | 9310/0 Preferred term *Ameloblastoma, NOS* |
| 67 | `9311 - Odontoameloblastoma` | 9311/0 Preferred term *Odontoameloblastoma* |
| 68 | `9312 - Squamous odontogenic tumor` | 9312/0 Preferred term *Squamous odontogenic tumor* |
| 69 | `9320 - Odontogenic myxoma` | 9320/0 Preferred term *Odontogenic myxoma* |
| 70 | `9321 - Central odontogenic fibroma` | 9321/0 Synonym term *Central odontogenic fibroma* |
| 71 | `9322 - Peripheral odontogenic fibroma` | 9322/0 Preferred term *Peripheral odontogenic fibroma* |
| 72 | `9330 - Ameloblastic fibroma` | 9330/0 Preferred term *Ameloblastic fibroma* |
| 74 | `9340 - Calcifying epithelial odontogenic tumor` | 9340/0 Preferred term *Calcifying epithelial odontogenic tumor* |
| 77 | `9250 - Giant cell tumor of bone, NOS` | 9250/1 Preferred term *Giant cell tumor of bone, NOS* |
| 80 | `8000 - Neoplasm, benign` | 8000/0 Preferred term *Neoplasm, benign* |
| 81 | `8000 - Neoplasm, uncertain whether benign or malignant` | 8000/1 Preferred term *Neoplasm, uncertain whether benign or malignant* |
| 83 | `8000 - Neoplasm, metastatic` | 8000/6 Preferred term *Neoplasm, metastatic* |
| 84 | `8000 - Neoplasm, malignant, uncertain whether primary or metastatic` | 8000/9 Preferred term *Neoplasm, malignant, uncertain whether primary or metastatic* |
| 85 | `8001 - Tumor cells, benign` | 8001/0 Preferred term *Tumor cells, benign* |
| 86 | `8001 - Tumor cells, uncertain whether benign or malignant` | 8001/1 Preferred term *Tumor cells, uncertain whether benign or malignant* |
| 91 | `8005 - Clear cell tumor, NOS` | 8005/0 Preferred term *Clear cell tumor, NOS* |
| 93 | `8800 - Soft tissue tumor, benign` | 8800/0 Preferred term *Soft tissue tumor, benign* |
| 95 | `8800 - Sarcomatosis, NOS` | 8800/9 Preferred term *Sarcomatosis, NOS* |

ICCC-3 Group VIII declares behaviour 3 only (ICCC-2017 ranges 59–71), so none of these is a
Group VIII cancer. The lookup tool records the commonest of them as behaviour exclusions with a
registrar flag (`docs/group_08_registrar_review.md` B1). Whether the registry keeps them in the
dropdown is the same question Groups IV, V and VI raised.

## 5. Pre-flight — before anything changes

Export `record_id`, `viii_morph`, `viii_code` and `viii_subgroup`, and count records on:

- **pick 33** — every record here is a Ewing sarcoma stored as aneurysmal bone cyst. Move to
  pick 35 (`9364`) after relabelling it, and check `viii_subgroup`: under ICCC-2017 the
  subgroup for `9364` at bone is **VIIIc2**, not VIIIc1;
- **picks 18 and 19** — re-code from the report to `9221` (picks 22 or 24 by behaviour);
- **picks 20 and 21** — any record that is really a chondrosarcoma needs the new `9220/3`
  option;
- **the 49 class D picks** — benign and borderline tumours outside ICCC-3 Group VIII; the
  registrar decides whether those records stay.

The registry began operating in 2025, so these counts are likely small. That is the reason to
make the change now, before positional codes accumulate records.

## 6. The repair, proposed

1. Relabel pick 33 `[RETIRED] 9260 - Ewing sarcoma (now 9364)`, as the Group V package did
   for `9514`; do not delete it until pick 33 holds no records.
2. Relabel pick 35 `9364 - Ewing sarcoma`.
3. Add `9220 - Chondrosarcoma, NOS` and `9302 - Ghost cell odontogenic carcinoma`.
4. Retire picks 18 and 19.
5. Relabel picks 7, 8, 39, 66, 75 and 98 to the ICD-O-3.2 preferred terms in §3.
6. Decide on the 49 class D picks (registrar).

Choice codes are positional (Programme Plan blocker 3). Append new choices; never renumber.

## 7. What the lookup tool already does

- Emits `9364` for Ewing sarcoma everywhere; no branch, fallback or alias names `9260` except
  the aneurysmal bone cyst exclusion (`check_group8_no_retired_ewing_code`).
- Shows "The REDCap label for this code is out of date — match on the four-digit code" on every
  entry in classes B, C and F, so the clerk is sent to pick 35, not pick 33.
- Carries every REDCap string in `aliases_group_08.json`, mapped to the code ICD-O-3.2 gives it.

## 8. Two Layer 1 file defects found in passing

1. **`Group 8- Malignant Bone Tumors.md` left the VIIIc2 line outside a code fence**, so the
   build's option parser could not see `9364` at all. Fenced on 2 October 2026 during this
   build; the file's text is otherwise unchanged and still matches the dictionary snapshot.
2. **`ICCC-2017.sqlite` range 60 reads `9210,9220,9240,` with a trailing comma.** The build
   reports it as an unreadable range token (WARN). Same class as the Group I broken row in
   `docs/codes-awaiting-redcap.md`. A Layer 1 fix, not made here.
