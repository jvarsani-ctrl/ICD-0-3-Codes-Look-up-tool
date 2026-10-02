# Group 9 build contract — Soft Tissue and Other Extraosseous Sarcomas

**Branch:** `claude/group-9-tumor-pathway-911c69`, a worktree cut from `main` at `cff8149`.
Groups 7 and 8 are being built at the same time on their own worktrees. `main` is untouched until
the registrar merges.

**Written 2 October 2026, before any JSON was authored.** Everything in §0 was verified on that day
against `ICCC-2017.sqlite`, `icdo32.sqlite`, the four IARC 3.1→3.2 change documents, the REDCap
option file, the baseline paper and the paediatric classification summary. An implementing agent
should author from this file and flag anything in it that turns out to be wrong.

Open decisions for the registrar are collected in `docs/group_09_registrar_questions.md`. The build
proceeds around each one with the choice stated there, and every choice is reversible.

> **Standing rule, inherited.** Advisory tools must never overstate evidence. Every defect that
> reached the browser in Groups 3 to 6 made a case look better evidenced than it was. The mirror
> image is banned too: Group 6 found that routing a named entity to an NOS code understates the
> registry's own code set. Both directions are tested.

---

## 0. Pre-context

### 0.1 What this group is

ICCC-3 Group IX, **soft tissue and other extraosseous sarcomas**. Rhabdomyosarcoma is the most
common paediatric soft tissue sarcoma; the others are grouped by paediatric oncologists as
"sarcomas other than rhabdomyosarcoma" (Pfister SM, et al. *Cancer Discovery* 2022;12(2):331–355,
section *Soft-tissue sarcomas*). Kaposi sarcoma is the highest-volume entity in a KSHV-endemic
paediatric population (Kamiyango W, et al. *Cancer and Metastasis Reviews* 2019, the Group 9
pathway's §4A).

### 0.2 ★ The ICCC-3 definition, read off `ICCC-2017.sqlite`

`code_ranges` for `main_group = 'IX'`, verbatim. **Every range declares behaviour 3 and nothing
else.**

| Subgroup | Morphology | Topography |
|---|---|---|
| IXa | `8900-8905,8910,8912,8920` | `000-809` |
| IXa | `8991` | `000-218,239-809` |
| IXb1 | `8810,8811,8813-8817,8821,8823,8834-8835` | `000-399,440-768,809` |
| IXb1 | `8820,8822,8824-8828,9150,9160` | `000-809` |
| IXb2 | `9540-9571` | `000-809` |
| IXb3 | `9491,9580` | `000-809` |
| IXc | `9140` | `000-809` |
| IXd1 | `9260` | `000-399,440-449,470-759` |
| IXd1 | `9365` | `000-399,470-639,659-768,809` |
| IXd2 | `9364` | `000-399,440-449,470-699,739-768,809` |
| IXd3 | `8963` | `000-218,239-639,659-699,739-768,809` |
| IXd4 | `8850-8858,8860-8862,8870,8880,8881` | `000-809` |
| IXd5 | `8830` | `000-399,440-768,809` |
| IXd5 | `8831-8833,8836,9251,9252` | `000-809` |
| IXd6 | `8890-8898` | `000-809` |
| IXd7 | `9040-9044` | `000-809` |
| IXd8 | `9120-9125,9130-9133,9135-9138,9141,9142,9161,9170-9175` | `000-809` |
| IXd9 | `9180-9187,9191-9195,9200,9210,9220,9240` | `220,300-388,470-509,600-619,649,670-679,696,700-729` |
| IXd9 | `9231` | `000-399,440-768,809` |
| IXd10 | `9581` | `000-809` |
| IXd11 | `8587,8710-8714,8806,8840-8842,8921,8990,8992,9045,9373` | `000-809` |
| IXe | `8800-8805` | `000-399,440-768,809` |

Consequences:

1. **Behaviour 3 only.** Every benign and intermediate soft tissue lesion is outside the group by
   ICCC-3's own definition. The pathway's §4H and §7.6 instruction to author "separate
   `morphology_entries` per behaviour" for the benign catalogue is wrong for the same reason it was
   wrong for Group 6 (Group 6 contract §5): those behaviours are `behaviour_exclusion` blocks on
   branches, never entries.
2. **Ewing sarcoma is filed under `9260`, a number ICD-O-3.2 deleted.** See §0.5.
3. **`8963` is extrarenal and extrahepatic only.** IXd3 excludes `219-238` (liver and biliary is
   VIIa2), `640-658` (kidney is VIa2) and `700-738` (CNS is Group III via `9508`).
4. **IXd9 is site-restricted.** `9180`, `9220` and `9240` belong to Group IX only at the listed
   non-bone sites. At `C40`–`C41`, `C76` and `C80.9` they are Group VIII.
5. **IXe excludes `C40`–`C43`.** `8800`–`8805` at bone are VIIIe.

### 0.3 ★ The code inventory — 82 usable codes, generated, not transcribed

```
ICCC_DB=… ICDO_DB=… python3 build/generate_group_inventory.py --group IX --out <scratch>/g9_inventory.json
```

> ICCC range entries 168 · distinct codes 168 · absent from ICD-O-3.2 at behaviour 3: 86 · usable 82

The worktree sits three directories deeper than the vault layout `generate_group_inventory.py`
assumes, so `ICCC_DB`, `ICDO_DB` and `ICD_LAYER1` must be set. That is a property of worktrees, not a
defect in the script.

The 82 by subgroup: IXa 7 · IXb1 6 · IXb2 5 · IXb3 1 · IXc 1 · IXd1 1 (`9365`) · IXd2 1 (`9364`) ·
IXd3 1 · IXd4 8 · IXd5 4 · IXd6 5 · IXd7 5 · IXd8 6 · IXd9 15 · IXd10 1 · IXd11 9 · IXe 6.

Four ICD-O-3.2 codes are in the inventory and have no REDCap option: `8714/3` perivascular
epithelioid tumour, malignant; `9045/3` biphenotypic sinonasal sarcoma; `9137/3` intimal sarcoma;
`9542/3` malignant peripheral nerve sheath tumour, epithelioid. They are built and declared
`awaiting_layer1` (ruling 3).

### 0.4 ★★ The two baseline documents

**Classification summary.** Sbaraglia M, Bellan E, Dei Tos AP. *The 2020 WHO Classification of Soft
Tissue Tumours: news and perspectives.* Pathologica 2021;113(2):70–84. DOI
[10.32074/1591-951X-213](https://doi.org/10.32074/1591-951X-213) · PMID 33179614 · PMC8167394.
Retrieved in full from Europe PMC on 2 October 2026 and read in full. Its twelve tables list every
WHO 2020 soft tissue entity by category and behaviour class. **They print no ICD-O code**, as the
memory note *WHO chapter tables list types only* predicts, so code currency rests on ICD-O-3.2 and
the paper settles which entities exist.

What it settles for this build:

- Ewing sarcoma sits in a new chapter, *undifferentiated small round cell sarcomas of bone and soft
  tissue*, beside three distinct families: round cell sarcoma with EWSR1–non-ETS fusions,
  CIC-rearranged sarcoma, and sarcoma with BCOR genetic alterations (Table XII, section *Undifferentiated small round cell sarcomas of bone and soft tissues*).
- Haemangiopericytoma is abolished; most are solitary fibrous tumours (section *Pericytic (perivascular) tumours*).
- Kaposi sarcoma is *intermediate (locally aggressive)* and infantile fibrosarcoma *intermediate
  (rarely metastasising)* in WHO's own behaviour classes (Tables IV, II), yet ICD-O-3.2 codes both at
  behaviour 3. **ICD-O behaviour decides ICCC membership, not WHO's behaviour class**, so both stay in
  the group.
- Dermatofibrosarcoma protuberans is intermediate; only the fibrosarcomatous form is malignant
  (Table II). This matches ICD-O-3.2's split of `8832` (§0.6).
- "True myxoid liposarcomas almost never occur in children, those reported case most likely
  representing examples of lipoblastoma" (section *Adipocytic tumours*). Myxoid pleomorphic
  liposarcoma occurs in children and adolescents (same section).
- Malignant fibrous histiocytoma is gone. Undifferentiated pleomorphic sarcoma is the label for its
  storiform-pleomorphic form, myxoid MFH is myxofibrosarcoma, and giant cell MFH splits three ways
  (section *So-called fibrohistiocytic tumour*).
- Melanotic schwannoma is relabelled *malignant melanotic nerve sheath tumour* and is malignant
  (section *Peripheral nerve sheath tumours*, Table X).
- NTRK-rearranged spindle cell neoplasm is an *emerging* entity (Table XI); infantile fibrosarcoma is
  distinct from it (section *Tumours of uncertain differentiation*).
- EBV-associated smooth muscle tumour is intermediate (Table VI).

**Paediatric occurrence.** Pfister SM, et al. *A Summary of the Inaugural WHO Classification of
Pediatric Tumors.* Cancer Discovery 2022;12(2):331–355. DOI
[10.1158/2159-8290.CD-21-1094](https://doi.org/10.1158/2159-8290.CD-21-1094) · PMC9401511.
Retrieved from Europe PMC and searched, as `docs/group_baseline_documents.md` instructs for this
paper. **Unlike Groups V and VI, it does cover this group**: it has a *Soft-Tissue and Bone Tumors*
section and its Table 2 (an image, read slice by slice on 2 October 2026) lists the paediatric soft
tissue entities. It is the evidence for ruling 1's paediatric-occurrence test. What it adds:

- Four rhabdomyosarcoma types: embryonal (including anaplastic), alveolar *with FOXO1 fusions*,
  spindle cell/sclerosing (including infantile VGLL2::NCOA2 and MYOD1-mutant), and pleomorphic,
  "extremely rare in children".
- Synovial sarcoma and malignant peripheral nerve sheath tumour are the non-rhabdomyosarcoma types
  most frequent in children and adolescents.
- Myxoid pleomorphic liposarcoma is characteristic of children, adolescents and young adults.
- BCOR internal tandem duplication marks infantile undifferentiated sarcoma and primitive myxoid
  mesenchymal tumour of infancy; CIC-rearranged and EWSR1–non-ETS sarcomas are adult-age.
- Table 2's paediatric malignant soft tissue list: liposarcoma; infantile fibrosarcoma; paediatric
  NTRK-rearranged spindle cell neoplasm; dermatofibrosarcoma protuberans / giant cell fibroblastoma;
  low-grade fibromyxoid sarcoma / sclerosing epithelioid fibrosarcoma; low-grade myofibroblastic
  sarcoma; Kaposi sarcoma; epithelioid haemangioendothelioma; angiosarcoma; glomus tumour; the
  rhabdomyosarcoma family; ectomesenchymoma; malignant peripheral nerve sheath tumour; clear cell
  sarcoma of soft tissue; alveolar soft part sarcoma; extrarenal rhabdoid tumour; PEComa; synovial
  sarcoma; epithelioid sarcoma; myoepithelial tumours; phosphaturic mesenchymal tumour; desmoplastic
  small round cell tumour; undifferentiated sarcomas; Ewing sarcoma and the three Ewing-like
  families; mesenchymal chondrosarcoma (bone list). It lists **only the EBV-associated smooth muscle
  tumour** under smooth muscle — not leiomyosarcoma.

**No registry-implications paper exists for this group.** The MeSH sweep in
`Group 9 Papers/Group 9 — Registry-Implications MeSH Search Results.md` found no Hoogendijk
equivalent. The cross-cutting layer — the IARC change documents and Visser 2023 — fills the role.

### 0.5 ⚠️ The most load-bearing correction: Ewing sarcoma is `9364/3`, not `9260/3`

The pathway document builds its round-cell branch on `9260 Ewing sarcoma`. **ICD-O-3.2 deleted it.**

```
IARC "Summary of main changes", p. 2:
  "Ewing sarcoma (9260/3) has moved to, and is now the preferred term for, 9364/3 (peripheral
   neuroectodermal tumour). Note, though, that the 4-digit code 9260 has not been deleted
   because a new term has been introduced under 9260/0."
IARC "Deleted codes and their terms", p. 6:  9260/3 Ewing sarcoma, Ewing tumor — Moved to 9364/3
IARC "New codes and their terms", p. 4:      9260/0 Aneurysmal bone cyst

icdo32.sqlite, code4 = 9364
  9364/3  Preferred  Ewing sarcoma
  9364/3  Related    Neuroectodermal tumor, NOS
  9364/3  Related    Peripheral primitive neuroectodermal tumor
  9364/3  Synonym    Ewing tumor
  9364/3  Synonym    Peripheral neuroectodermal tumor
  9364/3  Synonym    PPNET
```

So:

- **Every Ewing sarcoma of soft tissue codes `9364/3`.** ICCC-2017, which predates ICD-O-3.2, files
  `9364` at **IXd2** for soft tissue. IXd1 now holds only `9365` Askin tumour. The main group is
  unchanged; only the subgroup label reads oddly.
- **`9260` emits nothing in this group.** The REDCap option `9260 - Ewing sarcoma` is a retired
  number; a clerk picking it today records a code ICD-O-3.2 now assigns to a benign bone cyst.
- **The pathway's §4G "9364 vs 9473" discrepancy is closed by the same documents.** `9364` is
  peripheral PNET and Ewing sarcoma; `9473` is *CNS embryonal tumor, NOS* (icdo32.sqlite), Group III
  at every site (ICCC-2017 range 29, `000-809`, IIIc2).
- **The router's `9260` rule belongs to Group 8.** Agreed with the Group 8 session on 2 October 2026:
  Group 8 re-keys `dual_group_rules["9260"]` to `9364` and `9365`. Group 9 does not touch it, and its
  tree does not depend on it.

### 0.6 ICD-O-3.2 changed this group materially — checked, not assumed

All four IARC 3.1→3.2 documents were text-extracted on 2 October 2026 and searched for every Group
IX code.

| Change | Source | Consequence |
|---|---|---|
| `9260/3` Ewing sarcoma → `9364/3` | Deleted codes p. 6; Summary p. 2 | §0.5 |
| `9150` haemangiopericytoma deleted; /0, /1, /3 → `8815`/0, /1, /3 | Deleted codes p. 1; Summary p. 2 | REDCap option `9150` is a retired number; malignant haemangiopericytoma codes `8815/3` |
| `8832/3` DFSP NOS and `8833/3` pigmented DFSP (Bednar) → behaviour 1 | Summary p. 2; Behaviour p. 5 | Both out of the group. `8832/3` now carries only *Dermatofibrosarcoma protuberans, fibrosarcomatous* |
| `9133/1` epithelioid haemangioendothelioma → behaviour 3 | Behaviour p. 4; Deleted 5-digit p. 5 | EHE is now in the group |
| `8841/1` angiomyxoma → behaviour 0 | Behaviour p. 2 | out of scope either way |
| `9560/0` melanotic schwannoma → `9560/1` | Behaviour p. 1 | out of the group; WHO 2020 calls it malignant (§3.9) |
| `9540/1` neurofibromatosis deleted | Deleted 5-digit p. 5 | not a neoplasm code |
| `8825/3` myofibroblastic sarcoma, `8842/3` malignant ossifying fibromyxoid tumour | New codes p. 7 | new /3 terms in IXb1 and IXd11 |

**Two codes carry only `[obs]` terms at behaviour 3:** `9560/3` (*Neurilemoma, malignant*,
*Malignant schwannoma, NOS*, *Neurilemosarcoma*) and `8853/3` (*Round cell liposarcoma*). Neither is
in any IARC change document, so the marker is inherited. Both stay in the inventory; neither gets a
tree leaf (Group 3 obsolete-term precedent, `docs/group_03_obsolete_terms.md`).

**Four WHO 2020 entities have no ICD-O-3.2 code.** `icdo32.sqlite` has no rows for `9366`, `9367`,
`9368` or `8859`. WHO 2020 assigns `9366/3` round cell sarcoma with EWSR1–non-ETS fusions, `9367/3`
CIC-rearranged sarcoma, `9368/3` sarcoma with BCOR genetic alterations — reported by the Group 8
session from the ICCR bone dataset's reproduction of WHO Table 1, corroboration only — and
myxoid pleomorphic liposarcoma has no code in ICD-O-3.2 either. The tool codes to ICD-O-3.2 (standing
rule 2), so none of the four numbers is emitted. §3.2 and §3.3 say what is.

### 0.7 ★★ Visser 2023 Table 3 — this group has a no-tissue route after all

The pathway's §0 point 2 and §2B say Group IX has no imaging-sufficient diagnosis and that imaging
without tissue routes to `8800` "never an entity code". **Half right.** Visser O, et al. *Frontiers
in Oncology* 2023;13:1250549, Table 3, p. 04, read off the rendered PDF page on 2 October 2026:

| Cancer type | Basis | Topography | Morphology |
|---|---|---|---|
| Sarcoma, NOS | 2 | any site\* | `8800/3` |
| Liposarcoma | 2 | any site\* | `8850/3` |
| Leiomyosarcoma | 2 | any site\* | `8890/3` |
| Angiosarcoma | 1\*\* or 2 | any site\* | `9120/3` |
| **Kaposi sarcoma of the skin** | **1** | **C44** | **`9140/3`** |

\* "Sarcomas can be localized at any site, but mostly occur in the soft tissues." \*\* Angiosarcoma of
the skin of the breast following radiotherapy — not a paediatric scenario, and not built.

Three things follow:

1. **Imaging naming a sarcoma registers `8800/3` at basis 2**, and imaging naming liposarcoma,
   leiomyosarcoma or angiosarcoma registers that code at basis 2. The pathway is right that no
   *other* entity code is imaging-codable; it is wrong that the imaging route emits only a
   referral-grade code. `8800/3` is a Table 3 code in its own right.
2. **Cutaneous Kaposi sarcoma registers `9140/3` at basis 1 on clinical examination alone.** This is
   the single most consequential fact for a KSHV-endemic registry, and the pathway does not mention
   it. Nodal, mucosal or visceral Kaposi sarcoma has no such row: without pathology it is `8000/3`
   under rule 5, which ICCC-3 files in Group XII.
3. **Rule 4 still holds:** a lesion that a benign process could equally explain is not registered.

`imaging_sufficient` stays `false` on every entry. The basis-2 and basis-1 routes are `clinical_alias`
and `morphology_only` options carrying `basis_of_diagnosis`, not an `imaging_pathway` constellation:
no checklist of imaging features defines a sarcoma, and the Visser rows key off what the clinical
investigation *concludes*.

### 0.8 Engine facts that shape every node

- **`when` is string equality on a captured variable**, a list meaning any-of
  (`app.js` `whenValueOk`). The router's topography is `state.captured.topography`, so an
  `ihc_checklist` rule may gate on site directly with `"when": {"topography": [...]}` once the node
  declares `topography` in `captured_variables`.
- **`resolution_logic[]` is flat and first-match-wins**, conditioned rules before unconditioned.
- **Options cannot be filtered by `when`.** The clerk chooses; only `resolution_logic` rules read
  captured state.
- **Basis of diagnosis is the highest code any branch on the path asserted** (`basisOfDiagnosis()`),
  plus `ihc_counts_as: 7` whenever a marker was read. So a branch early in the histology route can
  assert basis 8 for a defining fusion and every named-diagnosis node below it can stay at 7.
- **Outstanding tests are `diagnostic_tests_required` minus `evidence_tests` minus the branch's
  `satisfies_tests`** (`finish()`). `evidence_tests` is replaced, not appended, by a `captures`.
- **The output block resolves the dual-group rules at output time** (`resolveGroup(code, topography)`).
  A Group 9 terminal emitting `8963` at a CNS site still reports Group III.

### 0.9 Schema, in one place

Unchanged from Group 6 contract §0.9: twenty `morphology_entries[]` fields, never-null
`morphology_code`, `morphology_name`, `behavior_code`; no `confidence_ceiling`; `clinical_alert` null
everywhere (ruling 9, enforced by `check_no_clinical_alerts()`); warnings go to
`docs/clinical-warnings.md`; `coding_note` and `topography_routing_note` are author-facing;
`behaviour_exclusion` shape `{icdo_code, icdo_behaviour, icdo_term, group_declares: "3", reason,
registrar_decision_required}`; `refer_group` carries no `morphology_code` and puts its text in
`reason`. Closed `diagnostic_tests_required` vocabulary; **Flow cytometry is not used in this
group.** Node-id prefix `st_`.

### 0.10 Rules inherited unchanged

Visser basis vocabulary (valid set `{0,1,2,4,5,7,8,9}`), `ihc_counts_as: 7`,
`methylation_counts_as: 8`; rule 4, *possible is not registrable*; ICD-O-3.2, not ICD-O-4; CBTRUS is
not a code-currency source; full forms in clerk-facing text — *desmoplastic small round cell tumour*,
not DSRCT; cite paper and page.

---

## 1. The inventory is generated, never transcribed

`build/generate_group09_entries.py` wraps `generate_group_inventory.build_inventory("IX")`, exactly as
`generate_group06_entries.py` does for Group VI, and adds only the annotation layer. It never
destroys an authored tree: it carries `decision_trees` across on regeneration.

`who_version` is `"WHO 2020"` on every entry (Sbaraglia 2021 is the baseline). Where no WHO 2020 soft
tissue entity lives on the stem, the `coding_note` says so.

**Paediatric core and tree leaves.** A code gets a tree leaf when a current WHO 2020 entity lives on
it, or when the report's own wording is a term ICD-O-3.2 still carries and the coder codes the term
written (§3.11). Codes whose every `/3` term is `[obs]`, and bone-only osteosarcoma subtypes at a
soft tissue site, are reachable by direct code entry only:

| Direct entry only | Why |
|---|---|
| `9560/3`, `8853/3` | every /3 term `[obs]` (§0.6) |
| `9181`–`9187`, `9192`–`9195` | bone osteosarcoma subtypes; WHO 2020 soft tissue lists only *osteosarcoma, extraskeletal* (Table IX) |
| `8813/3` fascial fibrosarcoma, `8855/3` mixed liposarcoma, `8857/3` fibroblastic liposarcoma, `8894/3` angiomyosarcoma, `8895/3` myosarcoma, `8710/3` glomangiosarcoma, `9124/3` Kupffer cell sarcoma, `9251/3` malignant giant cell tumour of soft parts, `8991/3` embryonal sarcoma | no WHO 2020 soft tissue entity on the stem; ICD-O-3.2 still carries the code |

Everything else has a tree leaf.

---

## 2. ★ Layer 1 conflict — REDCap and ICD-O-3.2 disagree in seventy-six places

`RedCap Options/Group 9- Soft Tissue And Other Extraosseous Sarcomas.md` offers **136** options
against the inventory's 82. Compared mechanically on 2 October 2026, 72 options are not the
ICD-O-3.2 preferred term at behaviour 3, and 4 inventory codes have no option:

| Class | Count |
|---|---|
| Label is the ICD-O-3.2 preferred term at /3 | 64 |
| Code exists only below behaviour 3 — out of the group | 57 |
| Label is a /3 synonym or related term, not the preferred term | 6 — `8811`, `9364`, `8963`, `9133`, `9187`, `8921` |
| Label is a term at **another behaviour** on a code whose /3 is a sarcoma | 3 — `8825` *Myofibroblastoma* (/0), `8832` *Dermatofibrosarcoma, NOS* (/1), `9220` *Chondroma, NOS* (/0) |
| Label matches nothing at any level | 5 — `9540`, `8851`, `9186`, `8842`, `8804` (each a missing ", NOS" or ", malignant") |
| Deleted number | 1 — `9150` |
| Retired at /3, moved | 1 — `9260` (counted with the 57 above, since `9260` survives only at /0) |
| ICD-O-3.2 /3 code with no option | 4 — `8714`, `9045`, `9137`, `9542` |

The three behaviour-drift labels are the dangerous ones. A clerk who picks `8825 - Myofibroblastoma`
for a myofibroblastic sarcoma, or `9220 - Chondroma, NOS` for an extraskeletal chondrosarcoma, records
the right number under a label naming a **benign** lesion. A clerk who picks `8832 - Dermatofibrosarcoma,
NOS` for an ordinary DFSP records a behaviour-3 code for a tumour ICD-O-3.2 now codes at behaviour 1.

This does **not** gate the build. It gates the exact-string check, which Group 9 steps aside from in
favour of `check_icdo32_round_trip()`, as Groups 3, 4 and 6 do (§8). The REDCap repair package is
`docs/group_09_layer1_repair.md`. Nothing is applied to the live form.

---

## 3. The code decisions this group forces

Each is recorded with its choice in `docs/group_09_registrar_questions.md`.

### 3.1 Ewing sarcoma → `9364/3`; Askin tumour → `9365/3` as written

§0.5. Agreed with Group 8 so both groups emit the same codes.

### 3.2 The Ewing-like round cell sarcomas → `8803/3`

CIC-rearranged sarcoma, sarcoma with BCOR genetic alterations (including BCOR internal tandem
duplication and primitive myxoid mesenchymal tumour of infancy) and round cell sarcoma with EWSR1–non-ETS
fusions code **`8803/3`**, whose ICD-O-3.2 synonyms include *Round cell sarcoma, undifferentiated*.
Never `9364/3`: WHO 2020 Table XII separates them from Ewing sarcoma. Never `9260`. Same choice as
Group 8.

### 3.3 Myxoid pleomorphic liposarcoma → `8850/3`

No ICD-O-3.2 code exists for it (§0.6). It is a liposarcoma whose subtype the code set cannot carry,
so the honest code is the lineage NOS, `8850/3 Liposarcoma, NOS`. Not `8852` myxoid and not `8854`
pleomorphic: either would assert a subtype the tumour is not.

### 3.4 Malignant fibrous histiocytoma and undifferentiated pleomorphic sarcoma

Soft tissue *undifferentiated pleomorphic sarcoma* codes **`8802/3`** (ICD-O-3.2 synonyms *Pleomorphic
sarcoma*, *Pleomorphic cell sarcoma, undifferentiated*; IXe). A soft tissue report that still says
*malignant fibrous histiocytoma* is coded as written, **`8830/3`** (IXd5), the ICD-O-3.2 preferred
term. Bone is Group 8's (`8830/3`, VIIId1). The two groups do not conflict.

### 3.5 Kaposi sarcoma, the viral gate, and the lymphadenopathy escape

The pathway's §7.4 asks that `9140` "must not resolve without `hhv8_lana_status: positive`". **Not
implemented as written**, for two reasons that are each sufficient:

1. Visser Table 3 registers cutaneous Kaposi sarcoma at basis 1 with no test at all (§0.7). A
   mandatory LANA gate would forbid what the ENCR rules permit.
2. A histology report that names Kaposi sarcoma is coded as Kaposi sarcoma. HHV-8 LANA-1 confirms it
   and is recorded; its absence leaves IHC on the outstanding-workup list, which is the honest signal.

What is implemented instead, and checked (§8): `9140` is **never** emitted on a branch where HHV-8 is
established *negative*; basis 1 is emitted only for `9140` and only on a branch capturing skin
lesions; and a LANA-negative report goes to its own node asking for the final diagnosis.

`9140` is **not** added to `VIRAL_GATED_CODES`, which is global and would apply the Group II rule to
a code whose ENCR row says otherwise.

**The lymphadenopathy escape (pathway §4A) is a routing fact, not a warning.** The `lymphadenopathy`
archetype's `candidate_groups` gains `9`, and `C77.9` gains `9`, so a lymph-node biopsy diagnosed as
Kaposi sarcoma can reach Group IX by the presentation path as well as by the alias lane. The clinical
sentence the pathway proposes ("do not default to a lymphoma code without excluding KS") goes to
`docs/clinical-warnings.md` (ruling 9).

### 3.6 `8963` rhabdoid tumour — extrarenal, extrahepatic, extracranial only

The tree's rhabdoid terminals live behind `st_epithelioid_ihc`, whose SMARCB1 (INI1) loss rules
refer CNS sites to Group III (`9508`), `C64.9` to Group VI and `C22.0`/`C22.1` to Group VII before the
soft tissue rule fires. The named-diagnosis option goes to the same node. The router's `8963` rule is
Group 7's to extend (agreed 2 October 2026).

### 3.7 Extraskeletal osteosarcoma and chondrosarcoma

`9180`, `9220`, `9231`, `9240` are emitted from `st_chondro_osseous`, which says in its question that
the tumour arises outside bone. A tumour arising in bone is referred to Group VIII. Router rules for
these codes are Group 8's (agreed).

### 3.8 Rhabdomyosarcoma subtype and FOXO1

The code follows the subtype the report states (pathway §4D). FOXO1 status is captured and
code-neutral. A rhabdomyosarcoma whose subtype is not stated and which carries a FOXO1 fusion codes
`8920/3`: Pfister 2022 defines the alveolar type as "alveolar with FOXO1 fusions", and Dehner CA, et
al. *Human Pathology* 2023 reports PAX3::FOXO1 and PAX7::FOXO1 in 80–90% of alveolar
rhabdomyosarcoma. An alveolar rhabdomyosarcoma reported FOXO1-negative is still coded `8920/3` as
stated; Dehner 2023 records that these tumours behave like embryonal rhabdomyosarcoma, and whether to
recode them is the registrar's (pathway §4D, §8 item 10).

Mixed-type rhabdomyosarcoma (`8902/3`) has no WHO 2020 entity (Table VII) but ICD-O-3.2 carries the
term; a report using it is coded as written (§3.11).

### 3.9 Malignant melanotic nerve sheath tumour → `9540/3`

WHO 2020 relabels melanotic schwannoma as malignant (Sbaraglia, section *Peripheral nerve sheath
tumours*). ICD-O-3.2 holds *Melanotic
MPNST* as a related term under `9540/3` and *Melanotic schwannoma* at `9560/1`. The tool codes the
WHO 2020 entity to `9540/3`. The WHO 2020 volume's own code for it is not printed in the baseline and
is a registrar question. Adult entity; no paediatric row.

### 3.10 Out-of-group destinations reached from a soft tissue presentation

| Finding | Destination | Source |
|---|---|---|
| Myoepithelial carcinoma of soft tissue, `8982/3` | Group XII (XIIa4) | ICCC-2017; Pfister Table 2 lists myoepithelial tumours in children |
| Gastrointestinal stromal tumour, `8936/3` | Group XII (XIIa1) | ICCC-2017 |
| Lymphoma, lymphoblastic lymphoma, Langerhans cell histiocytosis | Group II | |
| Myeloid sarcoma | Group I | router rule `9930` |
| Neuroblastoma, ganglioneuroblastoma | Group IV | |
| Extrarenal Wilms tumour, `8960` | Group VI | ICCC VIa1 any site |
| Germ cell tumour | Group X | |
| Melanoma, carcinoma | Group XI | |
| Primary bone tumour | Group VIII | |
| Malignant tumour, sarcoma not established, no specific type | Group XII (`8000/3`) | Visser rule 5 |

### 3.11 A term ICD-O-3.2 still carries is coded as written

Where a report uses a legacy term that WHO 2020 has retired but ICD-O-3.2 still carries without
`[obs]` — *Askin tumour* `9365`, *malignant fibrous histiocytoma* `8830`, *mixed type
rhabdomyosarcoma* `8902`, *lymphangiosarcoma* `9170`, *malignant haemangioendothelioma* `9130` — the
tool codes the term written, says so in `reason`, and lists the case as a registrar question. This is
the ICD-O coding convention and it is what Group 8 does for the same terms. The Group 3 test ("a code
leaves the decision tree only when no current WHO entity lives on its stem") is a condition for
*removing* a code, not a requirement to remove every such code.

### 3.12 `9473` is not a Group IX code at any site

`dual_group_rules["9473"]` defaults to Group IX, *"Peripheral / soft tissue PNET."* ICCC-2017 range
29 is the only range carrying `9473`, at sites `000-809`, resolving to IIIc2. ICD-O-3.2 codes the
peripheral PNET wordings at `9364/3`. Docs/TODO.md §12 left the rule open as "a Group III/IX
decision". **This is Group IX's half of it: Group IX has no claim on `9473`.** The rule is removed,
so `9473` is a single-group Group III code; the name-exemption in
`check_router_cns_topography_completeness()` is deleted with it, as that check requires.

---

## 4. Tree architecture

One tree, `g9_soft_tissue`, entry node `st_document_inventory`. Node-id prefix `st_`.

```
st_document_inventory          document_inventory   evidence in the file
  ├── referral / clinical note ........... st_clinical_alias         (Visser basis 1 for cutaneous KS; else XII / not registered)
  ├── imaging only ....................... st_imaging_report         (Visser basis 2: 8800, 8850, 8890, 9120)
  ├── cytology only ...................... st_cytology               (basis 5, lineage NOS only)
  ├── histology .......................... st_report_contents        (evidence_tests + basis 7 or 8)
  └── specimen inadequate ................ st_imaging_report         (ruling 11)

st_report_contents             document_inventory   H&E only · H&E + IHC · + defining fusion (FISH) · + defining fusion (RT-PCR/sequencing)
st_lineage                     histology_subclassification   line of differentiation, or family of the named diagnosis
  ├── skeletal muscle ......... st_rms ── alveolar ─→ st_rms_alveolar_fusion   (cytogenetics_dropdown)
  │                                    └─ not stated ─→ st_rms_unspecified_fusion (cytogenetics_dropdown)
  ├── small round cell ........ st_round_cell ── descriptive ─→ st_round_cell_ihc   (ihc_checklist)
  ├── fibroblastic / fibrohistiocytic ..... st_fibroblastic
  ├── peripheral nerve sheath ............. st_nerve_sheath
  ├── vascular ............................ st_vascular ── KS, HHV-8 negative ─→ st_kaposi_hhv8_negative
  ├── adipocytic .......................... st_adipocytic
  ├── smooth muscle ....................... st_smooth_muscle
  ├── synovial sarcoma .................... st_synovial
  ├── uncertain differentiation ........... st_uncertain ── rhabdoid / epithelioid ─→ st_epithelioid_ihc
  ├── bone or cartilage in soft tissue .... st_chondro_osseous
  ├── undifferentiated / unclassified ..... st_undifferentiated
  ├── spindle cell, no line named ......... st_spindle_age (numeric_gate) → st_spindle_ihc (ihc_checklist)
  ├── epithelioid / rhabdoid, not named ... st_epithelioid_ihc
  ├── not a sarcoma ....................... st_not_sarcoma   (refer_group terminals)
  ├── benign or reactive .................. non_reportable
  └── malignant, type not determined ...... refer XII (8000/3)
```

**Named diagnosis first, markers second.** A histology report normally states a final diagnosis, and
the registry codes that diagnosis. The lineage nodes are picklists of named entities. The three
`ihc_checklist` nodes exist for the descriptive report that gives findings and markers but no named
entity. This is how the pathway's §2C table ("H&E descriptor → lineage NOS, upgrade by IHC
surrogate") and §2D table ("IHC surrogate sets the code") are both honoured: the descriptor routes
the clerk to a lineage, and the surrogate marker sets the entity only where the report itself names
none.

**Basis.** `st_report_contents` asserts 7 or 8; the named-diagnosis branches assert 7; `ihc_counts_as`
asserts 7 when a marker is read. Basis 8 is asserted only on an option whose label requires the
molecular result to identify the fusion **defining the tumour the report names** (Visser rule 10).

### 4.1 The IHC-surrogate rules (pathway §2D), as authored

`st_round_cell_ihc` — rules in order: CD45 → Group II · TdT → Group II (lymphoblastic lymphoma is
CD99-positive) · PHOX2B → Group IV · desmin + myogenin → `st_rms` · desmin + pan-cytokeratin + WT1 →
`8806` · SS18-SSX → `9040` · CD99 + NKX2.2 → `9364` · BCOR → `8803` · fallback `8803`.

`st_spindle_ihc` — HHV-8 LANA-1 → `9140` · myogenin → `8912` (asked before pan-TRK, because Hung
2018 lists spindle cell rhabdomyosarcoma among the pan-TRK-positive mimics) · SS18-SSX → `9041` ·
pan-TRK with age under 2 → `8814` · H3K27me3 loss **with `sarcoma_lineage` nerve sheath** → `9540`
(Martinez & Fritchie 2018: loss in 34–73% of MPNST and in a minority of synovial sarcomas,
fibrosarcomatous DFSP and melanomas, so it does not stand alone) · STAT6 → `st_sft_behaviour` (the
malignant-or-not question is morphological) · MUC4 → `8840` · desmin + h-caldesmon → `8890` ·
fallback `8801`. Pan-TRK at age 2 or over is a NTRK-rearranged spindle cell neoplasm, which has no
ICD-O-3.2 code: fallback `8801`, with the reason saying so (registrar questions B3, J2).

`st_epithelioid_ihc` — CNS site + SMARCB1 loss → Group III (`9508`) · `C64.9` + loss → Group VI ·
`C22.0`/`C22.1` + loss → Group VII · loss with rhabdoid morphology captured → `8963` · TFE3 →
`9581` · fallback `8800`. Epithelioid sarcoma is coded only when the report names it: Agaimy 2014
Table 1 gives SMARCB1 loss in 50% of epithelioid MPNST, 10–40% of myoepithelial carcinoma, 16% of
extraskeletal myxoid chondrosarcoma and 74% (mosaic) of ossifying fibromyxoid tumour, so the stain
with an unspecified morphology sets nothing. Melanocytic markers and cytokeratin were left out of
the node: neither separates clear cell sarcoma from melanoma, or a keratin-positive sarcoma
(epithelioid sarcoma, synovial sarcoma) from carcinoma, without the report's own diagnosis.

Every surrogate whose source calls it imperfect (pan-TRK "not fully specific", Hung 2018; TFE3 IHC
below RT-PCR, Jaber 2015) carries that fact in `clinical-warnings.md`, not in the tree.

---

## 5. What the diagnostic pathway document gets wrong

`../Group 9 — Soft Tissue and Other Extraosseous Sarcomas Diagnostic Pathway.md` (v1, 2 July 2026).
Its §0 diagnosis — lineage router, IHC surrogates, Kaposi misrouting — is sound and is implemented.

| # | The document says | The sources say |
|---|---|---|
| 5.1 | Ewing sarcoma is `9260` throughout (§1, §2D, §4C, §4G, §6) | Deleted in ICD-O-3.2, moved to `9364/3` (§0.5) |
| 5.2 | Ewing-like sarcomas collapse to "9260 or 8803" (§4C) | Never `9260`, never `9364`; `8803/3` (§3.2) |
| 5.3 | No soft tissue sarcoma is imaging-codable; imaging-only is "never an entity code" (§0, §2B) | Visser Table 3: `8800`, `8850`, `8890`, `9120` at basis 2; cutaneous KS `9140` at basis 1 (§0.7) |
| 5.4 | Benign and intermediate members get their own `morphology_entries` (§4H, §7.6) | ICCC-3 Group IX declares behaviour 3 only; they are `behaviour_exclusion` branches (§0.2) |
| 5.5 | DFSP `8832/8833` is a "/3 (low-grade)" Group IX code (§1 IXd5) | Both moved to /1 in ICD-O-3.2; only fibrosarcomatous DFSP is `8832/3` (§0.6) |
| 5.6 | Malignant haemangiopericytoma is `9150` (§1 IXb1) | `9150` deleted; `8815/3` (§0.6) |
| 5.7 | EHE `9133` (§1 IXd8) treated as uncertain | Moved /1 → /3 in ICD-O-3.2; in the group (§0.6) |
| 5.8 | `9364` vs `9473` must be reconciled by the registry (§4G, §8 item 8) | Settled by ICD-O-3.2: `9364` is peripheral PNET; `9473` is CNS embryonal tumour (§3.12) |
| 5.9 | `9140` must not resolve without LANA positive (§7.4) | Contradicts Visser Table 3 basis 1 (§3.5) |
| 5.10 | Plexiform neurofibroma terminal "must carry a caveat" (§4I) | Ruling 9: no warnings in the tool; moved to `clinical-warnings.md` |
| 5.11 | Clinical alerts on `9140`, `8963`, `9260`, `8920`, `9540`, `9550` (§5) | Ruling 9; all null |
| 5.12 | UPS is `8830` (§1 IXd5) | Soft tissue UPS is `8802/3` (§3.4) |

---

## 6. The alias layer

`data/aliases/aliases_group_09.json`, built to `../Alias JSON Build — Master Instruction File.md` and
`../Group 9 — Alias Build Instructions.md`, cross-resolving against `group_09_dt.json`. Vocabulary that
must resolve:

- every ICD-O-3.2 term at /3 on the 82 codes (preferred, related, synonym), the `[obs]` ones flagged;
- the REDCap option strings that drift (§2), so a clerk who knows the dropdown label finds the code;
- **Ewing vocabulary**: *Ewing sarcoma*, *Ewing's sarcoma*, *extraskeletal Ewing sarcoma*, *ES/PNET*,
  *peripheral PNET*, *PPNET* → `9364`; *Askin tumour* → `9365`; *PNET, NOS* and *primitive
  neuroectodermal tumour* without "peripheral" must not resolve to `9364`;
- Ewing-like: *CIC-rearranged sarcoma*, *CIC-DUX4*, *BCOR-rearranged sarcoma*, *BCOR-CCNB3*, *BCOR ITD*,
  *primitive myxoid mesenchymal tumour of infancy*, *NFATC2*, *PATZ1* → `8803`;
- rhabdomyosarcoma: *ERMS*, *botryoid*, *sarcoma botryoides*, *ARMS*, *PAX3::FOXO1*, *PAX7::FOXO1*,
  *fusion-positive RMS*, *spindle cell/sclerosing RMS*, *MYOD1*, *VGLL2*;
- Kaposi: *Kaposi's sarcoma*, *KS*, *HHV-8*, *KSHV*, *lymphadenopathic Kaposi*;
- the INI1 vocabulary: *INI1*, *SMARCB1*, *BAF47*, *SNF5*;
- terms that must resolve to a **non-Group-IX** destination or to an exclusion: *desmoid*, *inflammatory
  myofibroblastic tumour*, *lipoblastoma*, *plexiform neurofibroma*, *DFSP* (NOS), *haemangioma*,
  *kaposiform haemangioendothelioma*, *myxoinflammatory fibroblastic sarcoma*, *GIST*, *myoepithelial
  carcinoma*.

---

## 7. Shared-layer changes this build requires

Coordinated with the Group 7 and Group 8 sessions on 2 October 2026. Group 9 owns only the rows below.

1. `presentation_router.json` `groups["9"]`: `built: true`, tree and handoff.
2. `presentation_router.json` `archetypes[lymphadenopathy].candidate_groups`: add `9` (§3.5).
3. `presentation_router.json` `dual_group_rules["9473"]`: remove (§3.12), and delete the exemption name
   from `check_router_cns_topography_completeness()`.
4. `topography_codes.json`: add `9` to `C69.6` orbit, `C11.x` nasopharynx and `C77.9` lymph node;
   add crosswalk rows and lookup entries for skin `C44` (REDCap offers no `C44.4`), urinary bladder
   `C67`, prostate `C61.9`, vagina `C52.9`, cervix `C53`, vulva `C51`, paratesticular structures
   `C63.0`–`C63.9`, extrahepatic bile duct `C24.0`. Every code checked against `Topography Redcap.md`.
5. `build_database.py`: `GROUP9`, its row in `BEHAVIOUR_DECLARED_BY_GROUP`, its place in the
   round-trip and exact-string guards, and the Group 9 checks (§8). Group 8 makes the same kind of
   edit on the same lines; keep both at merge.
6. `docs/codes-awaiting-redcap.md` — a `## Group 9 — open` section for `8714`, `9045`, `9137`, `9542`.
7. `docs/clinical-warnings.md` — a Group IX section.
8. `docs/group_09_layer1_repair.md` — the REDCap repair package for §2.
9. `docs/group_baseline_documents.md` — record that Pfister 2022 does cover Group IX.

**Not Group 9's:** `dual_group_rules["9260"]`, any `9180`/`9220`/`9231`/`9240` rule, the
`tumour_origin` discriminator (Group 8); `dual_group_rules["8963"]`, `["8991"]`, the C22 branch of
`["8000-8005"]` (Group 7).

---

## 8. Validation rules this group adds

Each gets a negative control that breaks the data and a probe with correct data that must stay
silent (Group 6 contract §8.1).

| # | Check | Catches |
|---|---|---|
| 1 | `check_group9_code_set` | an emitted `(code, behaviour)` not in the generated inventory |
| 2 | `check_group9_absent_codes` | `9260`, `9150`, `9366`, `9367`, `9368`, `8859` emitted anywhere |
| 3 | `check_group9_ewing_code` | any branch whose label or reason names Ewing sarcoma emitting anything but `9364` (or `9365` for Askin), and any Ewing-like family emitting `9364` |
| 4 | `check_group9_basis_rows` | basis 1 on anything but `9140`, or on a `9140` branch that does not capture skin lesions; basis 2 on anything outside Visser Table 3's four codes |
| 5 | `check_group9_kaposi_hhv8` | `9140` emitted on a branch or path where HHV-8 is established negative |
| 6 | `check_group9_8963_site` | the soft tissue `8963` rule not preceded by CNS, kidney and liver referral rules carrying SMARCB1 loss |
| 7 | `check_group9_no_imaging_sufficient` | `imaging_sufficient: true` on any entry |
| 8 | `check_group9_no_flow_cytometry` | Flow cytometry in any `diagnostic_tests_required` |
| 9 | `check_group9_obs_unreachable` | `9560/3` or `8853/3` emitted from a tree |

Plus: `GROUP9` joins `BEHAVIOUR_DECLARED_BY_GROUP` (`{"3"}`) and the round-trip guard; the
exact-string check steps aside for it.

---

## 9. Proof before this group is called done

1. `python3 build/build_database.py` → 0 FAIL.
2. `python3 build/induce_flow.py` → every rule has a witness.
3. Negative controls and correct-data probes on all nine checks, pinned to a commit before the fix.
4. Drive the changed branches in the browser: the Kaposi skin route, the round cell checklist, the
   rhabdoid site referrals, and a lymphadenopathy presentation reaching Group IX.
5. Groups 1–6 byte-identical to `main`.

---

## 10. What needs the registrar

`docs/group_09_registrar_questions.md`.
