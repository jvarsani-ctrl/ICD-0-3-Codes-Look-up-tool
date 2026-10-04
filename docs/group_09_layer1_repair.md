# Group 9 — Layer 1 Repair Package (REDCap `ix_morph`)

**2 October 2026** · a **REDCap-project** document. The lookup tool does not depend on any of it:
`group_09_dt.json` is generated from `icdo32.sqlite` and `ICCC-2017.sqlite`. **Nothing here has been
applied to the live form**, and per the vault's routing rules the REDCap side of every item below
belongs to the REDCap Registry repository (`Cancer Registry/REDCap Registry/`), not to this one.

**Method:** the Group 6 package's. Each of the 136 options in
`ICD coding/RedCap Options/Group 9- Soft Tissue And Other Extraosseous Sarcomas.md` was compared on
2 October 2026 with the ICD-O-3.2 terms for its code in `icdo32.sqlite` and with the four IARC
3.1→3.2 change documents. `REDCap Registry/docs/data-dictionary/Diagnosis.md` records the live
`ix_morph` dropdown as identical to that file, pick for pick (13 August 2026).

**Scale:** 72 of 136 options are not the ICD-O-3.2 preferred term at behaviour 3; four ICD-O-3.2
codes have no option. Most of the 72 are benign or intermediate lesions, which are a scope question
(§5), not a defect in the option.

---

## 0. How `ix_morph` stores a code, and why relabelling is safe

`ix_morph` stores the real ICD-O-3 code as the option value; there is no `_code` companion.
`ix_extended` and `ix_subgroup` are `if()` chains keyed on the literal value
(`Diagnosis.md`, § `ix_extended`, § `ix_subgroup`). **Changing an option's label changes nothing a
calculation reads.** Retiring an option does: the value disappears from the dropdown, and records
already holding it keep it.

---

## 1. Two retired numbers — the dangerous class

| Option | REDCap label | ICD-O-3.2 | What a clerk records today |
|---|---|---|---|
| `9260` | Ewing sarcoma | **`9260/3` deleted, "Moved to 9364/3"**; `9260` survives only as `9260/0` *Aneurysmal bone cyst* (IARC *Deleted codes*, p. 6; *New codes*, p. 4; *Summary of main changes*, p. 2) | a code ICD-O-3.2 now assigns to a benign bone cyst, for the commonest paediatric round cell sarcoma |
| `9150` | Hemangiopericytoma, malignant | **deleted**; /0, /1 and /3 moved to `8815`/0, /1, /3 (IARC *Deleted codes*, p. 1) | a number that resolves to nothing in ICD-O-3.2 |

**Repair:** retire both with the `[RETIRED]` treatment the Group V package defines for `9514`.
Relabel `9364` from *Peripheral neuroectodermal tumor* to **Ewing sarcoma**, its ICD-O-3.2
preferred term, so the clerk finds Ewing sarcoma under its current number. Group VIII's option list
carries the same `9260` defect; that is the Group 8 build's to record.

## 2. Labels naming the wrong behaviour on the right number

| Option | REDCap label | ICD-O-3.2 at that number | Consequence |
|---|---|---|---|
| `8825` | Myofibroblastoma | `/0` *Myofibroblastoma*; `/1` *Myofibroblastic tumor, NOS*; **`/3` Myofibroblastic sarcoma** | a clerk coding low-grade myofibroblastic sarcoma picks a label naming a benign tumour |
| `9220` | Chondroma, NOS | `/0` *Chondroma, NOS*; **`/3` Chondrosarcoma, NOS** | same, for an extraskeletal chondrosarcoma |
| `8832` | Dermatofibrosarcoma, NOS | `/1` *Dermatofibrosarcoma, NOS*; **`/3` Dermatofibrosarcoma protuberans, fibrosarcomatous** (IARC *Summary*, p. 2) | an ordinary DFSP, behaviour 1 since ICD-O-3.2, is recorded as a Group IX sarcoma |
| `8833` | Pigmented dermatofibrosarcoma protuberans | `/1` only since ICD-O-3.2 | a behaviour-1 tumour recorded as a sarcoma |

**Repair:** relabel `8825` to *Myofibroblastic sarcoma*, `9220` to *Chondrosarcoma, NOS*, `8832` to
*Dermatofibrosarcoma protuberans, fibrosarcomatous*; retire `8833`.

## 3. Labels that are a synonym, not the preferred term

Cosmetic, but they are the strings a clerk matches against the tool's output.

| Option | REDCap label | ICD-O-3.2 preferred term |
|---|---|---|
| `8811` | Fibromyxosarcoma | Myxofibrosarcoma |
| `9364` | Peripheral neuroectodermal tumor | **Ewing sarcoma** (§1) |
| `8963` | Malignant rhabdoid tumor | Rhabdoid tumor, NOS |
| `9133` | Epithelioid hemangioendothelioma, malignant | Epithelioid hemangioendothelioma, NOS |
| `9187` | Intraosseous well differentiated osteosarcoma | Low grade central osteosarcoma |
| `8921` | Rhabdomyosarcoma with ganglionic differentiation | Ectomesenchymoma |

## 4. Labels missing a qualifier

| Option | REDCap label | ICD-O-3.2 preferred term |
|---|---|---|
| `9540` | Malignant peripheral nerve sheath tumor | …, NOS |
| `8851` | Liposarcoma, well differentiated | …, NOS |
| `9186` | Central osteosarcoma | …, NOS |
| `8804` | Epithelioid sarcoma | …, NOS |
| `8842` | Ossifying fibromyxoid tumor | …, **malignant** — the NOS form is `8842/0` |

`8842` is the one that matters: without "malignant" the label names the behaviour-0 tumour.

## 5. Fifty-seven options below behaviour 3

ICCC-3 Group IX declares behaviour 3 for every range (`docs/group_09_build_contract.md` §0.2). These
options exist in ICD-O-3.2 only at behaviour 0 or 1:

> `8587` `8712` `8713` `8820` `8821` `8822` `8823` `8824` `8826` `8827` `8831` `8833` `8834`
> `8835` `8836` `8841` `8856` `8860` `8861` `8862` `8870` `8880` `8881` `8892` `8893` `8897`
> `8898` `8903` `8904` `8905` `9121` `9122` `9123` `9125` `9131` `9132` `9135` `9136` `9141`
> `9142` `9160` `9161` `9171` `9172` `9173` `9174` `9175` `9191` `9200` `9210` `9260` `9373`
> `9491` `9541` `9550` `9562` `9570`

(`9260` is listed because only `9260/0` exists; §1 covers it.) The lookup tool emits none of them;
each reaches a behaviour-exclusion or not-reportable terminal. Whether the registry wants any of
these lesions recorded is registrar question G1. If it does, they need a home outside Group IX.

## 6. Four ICD-O-3.2 codes with no option

`8714`, `9045`, `9137`, `9542`. Already drafted for `ix_morph`, `ix_extended` and `ix_subgroup` in
`REDCap Registry/docs/data-dictionary/Diagnosis.md` (13 August 2026, not yet applied). Listed in
`docs/codes-awaiting-redcap.md` under *Group 9 — open*.

## 7. Topography: no `C44.4`

`Topography Redcap.md` offers 440–443 and 445–449. `C44.4`, skin of scalp and neck, is missing, so a
scalp or neck skin lesion — a cutaneous Kaposi sarcoma, say — cannot be recorded at its own site.

## 8. Pre-flight, before changing anything

Read-only counts against the live project, run by whoever applies this in the REDCap Registry repo:

1. records with `ix_morph` = `9260`, `9150`, `8832`, `8833` — each is a record whose meaning changes
   with this repair;
2. records with any §5 code — each is a benign or intermediate lesion held in the malignant registry.

The lookup tool's tests never call the live API, and this package does not either.
