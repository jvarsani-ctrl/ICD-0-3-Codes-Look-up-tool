# Group 5 — Layer 1 Repair Package (REDCap `v_morph`)

**2026-09-22** · a **REDCap-project** document. The ICD-O lookup tool is a separate project and
**does not depend on any of this** — it generates its inventory from `icdo32.sqlite` and
`ICCC-2017.sqlite` directly. Nothing here gates `group_05_dt.json`.
**Status:** ready to review. **Nothing has been applied to the live form.**
**Method:** identical to `Group 3 — Layer 1 Repair Package (REDCap iii_morph).md` and the Group 4
package.
**Scale:** one finding, on one option. This is the smallest repair package of the three.

---

## 0. Why this is the easiest block in the form

`v_morph` is the simplest of the twelve morphology fields, and the repair inherits that simplicity.

- It stores the **real ICD-O-3 code as the option value** — `9510`, `9511`, `9512`, `9513`,
  `9514` — not a pick number.
- It has **no `v_code`, no `v_extended`, no `v_subgroup` companion field.** The field label says so
  outright: *"Note: This classification does not have subgroups."* That is correct — ICCC-3 Group V
  has no second or third tier.
- Its branching logic is `diag_main = '5'` and `dx_cancer = '1'`.

So the renumbering hazard that shapes the Group 4 package — insert or delete a pick and every
later pick silently changes meaning — **does not exist here.** There is no position-to-code
formula to keep in step, because the position *is* the code. Retiring an option is a label change
and nothing else.

---

## 1. The finding

**Option `9514` — "9514 - Retinoblastoma, spontaneously regressed" — is not an assignable Group V
code, and never has been.**

Verified 22 September 2026 against IARC's final ICD-O-3.2 workbook
`ICD-O-3.2_final_update09102020.xls` (9 October 2020), via `ICD coding/ICD-O-3.2/icdo32.sqlite`,
and against the ICCC-3 2017 recode table via `ICCC-2017.sqlite`:

| Source | What it says |
|---|---|
| `icdo32.sqlite` | `9514` exists at **one** behaviour: `9514/1`, Preferred term *Retinoblastoma, spontaneously regressed*. There is no `9514/3` and no `9514/0`. |
| `ICCC-2017.sqlite` | Group V is declared as morphology `9510–9514` at behaviour **`3`**, topography `C00.0–C80.9`. Behaviour `3` and only `3`. |
| IARC 3.1→3.2 change documents | All four — *Deleted codes*, *New codes*, *Terms changing behaviour*, *Summary of main changes* — mention no code in the range `9510`–`9514` anywhere. The behaviour is not a 3.2 change; it is what the code has always carried. |

A case selected as `9514` therefore records a morphology at behaviour `/1` in a field whose whole
range is declared malignant. It is not a Group V registration, and under the ICCC-3 recode it is
not a malignant registration at all.

This is the same class of finding as Group 4's `8683` Gangliocytic paraganglioma, which exists in
ICD-O-3.2 only at `/0` and was likewise withdrawn rather than recoded.

**The lookup tool already behaves correctly.** `build/generate_group_inventory.py --group V`
returns four usable codes, not five, and `group_05_dt.json` emits `9514` from no branch. A clerk
who arrives with the words *spontaneously regressed retinoblastoma* reaches a terminal that says
why no Group V code is assigned and sends the case to the registrar. The discrepancy is on the
REDCap side alone.

---

## 2. Pre-flight — run before changing anything

Export `record_id`, `diag_main` and `v_morph`, and count records on option `9514`.

| Check | Option | If any records are found |
|---|---|---|
| **Behaviour outside the group's declaration** | `9514` | The lesion is a spontaneously regressed retinoblastoma — a phthisical, calcified, non-functional globe with no viable tumour. Review each against the source clinical or pathology record. There is **no automatic destination**: whether the case is an incident registration at all is §4, and it is the registrar's decision, not a recode. |

The registry began operating in 2025 and spontaneous regression occurs in roughly 2% of
retinoblastoma, so **a count of zero is the likely result**, in which case the whole repair is a
label change with no data migration.

---

## 3. The repair

One operation. **Retire in place.**

| Option value | Current label | Proposed label |
|---|---|---|
| `9514` | `9514 - Retinoblastoma, spontaneously regressed` | `[RETIRED] 9514 - Retinoblastoma, spontaneously regressed` |

- **Never delete the option.** Deleting it would make any stored `9514` unreadable. If it must
  eventually disappear, that is a separate migration with its own data move, done once.
- **No formula changes.** There is no `v_code`, `v_extended` or `v_subgroup` to update.
- **No renumbering.** The remaining four options keep their values, which are their codes.
- **No appends.** All four usable Group V codes already have a correct option, so nothing goes on
  `docs/codes-awaiting-redcap.md` for this group.

The other four options need no change at all. Each label's term is character-identical to the
ICD-O-3.2 Preferred term at that code and behaviour:

| Option | REDCap label | ICD-O-3.2 Preferred term at `/3` | Match |
|---|---|---|---|
| `9510` | `9510 - Retinoblastoma, NOS` | Retinoblastoma, NOS | ✅ |
| `9511` | `9511 - Retinoblastoma, differentiated` | Retinoblastoma, differentiated | ✅ |
| `9512` | `9512 - Retinoblastoma, undifferentiated` | Retinoblastoma, undifferentiated | ✅ |
| `9513` | `9513 - Retinoblastoma, diffuse` | Retinoblastoma, diffuse | ✅ |

Four for four. This is the only morphology field in the form where the Layer 1 audit found no
label drift.

---

## 4. ⚠️ The decision this package cannot make

**Retiring the option removes a wrong code. It does not answer whether the case is registrable.**

A spontaneously regressed retinoblastoma is a cancer that existed and then involuted. Whether the
registry counts it as an incident case — and if so on what code — is a registration-rules
question, not a morphology question, and it belongs to the registrar.

The same question arises for **retinocytoma (retinoma)**, the benign counterpart, which ICD-O-3.2
codes `9510/0`. It shares its four-digit stem with `9510/3 Retinoblastoma, NOS`, which is the trap:
a system that stores `9510` without the behaviour records a malignant retinoblastoma for a benign
lesion. `v_morph` stores four digits and no behaviour, so **there is no way to select a
retinocytoma in this form that would not read as a retinoblastoma.** The tool refuses to emit it
for exactly that reason.

Three options, none of them the tool's to choose:

1. **Out of scope.** ICCC-3 registers no benign eye tumour. Both lesions fall outside the registry
   and are not entered. The parallel is Group 4's ganglioneuroma, ruled D1 on 16 September 2026.
2. **Registered outside the ICCC-3 morphology fields**, in whatever the registry uses for
   non-malignant lesions of interest — which would need a field that does not exist today.
3. **Registered in Group V on a code the registrar names**, which would require a behaviour to be
   storable alongside the four digits.

Until that ruling, both lesions reach a terminal in the tool that states the finding, states why no
Group V code is assigned, and refers the case to the registrar. Nothing is silently dropped and
nothing is silently coded.

---

*Every finding verified 22 September 2026 against `ICD coding/ICD-O-3.2/icdo32.sqlite` (IARC final
workbook, 9 October 2020), `ICCC-2017.sqlite`, the four IARC 3.1→3.2 change documents, and
`EAFYA IMPORT/redcap_field_choices.json` for the live `v_morph` option list. See
`docs/group_05_build_contract.md` §1.1, §2.1, §2.2 and §7.3.*
