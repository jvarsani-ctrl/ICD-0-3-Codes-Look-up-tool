# Group IX — build report, 2026-10-03

Soft tissue and other extraosseous sarcomas. Branch `claude/group-9-tumor-pathway-911c69`, a
worktree cut from `main` at `cff8149`, built overnight 2–3 October 2026 alongside the Group 7 and
Group 8 sessions. Nothing is merged and nothing is pushed.

**Read first:** `docs/group_09_registrar_questions.md`. Every decision the sources do not settle is
there, with what the build does meanwhile. The five marked ★ change what a clerk records today.

---

## 1. What this group is, and the fact that reshaped it

ICCC-3 Group IX is behaviour 3 only, across all 22 code ranges. The generated inventory is 82 codes
(`build/generate_group09_entries.py`). The REDCap option file offers 136.

### ★ Ewing sarcoma is `9364/3`, not `9260/3`

The diagnostic pathway document builds its round cell branch on `9260 Ewing sarcoma`. ICD-O-3.2
deleted it: IARC's *Summary of main changes* (p. 2) and *Deleted codes and their terms* (p. 6)
record `9260/3` "Moved to 9364/3", and `9260` now carries only `9260/0` *Aneurysmal bone cyst*.
ICCC-2017, which predates ICD-O-3.2, still files Ewing sarcoma under `9260` and files `9364` at IXd2.
The REDCap dropdown still offers `9260 - Ewing sarcoma`. A clerk picking it today records, for the
commonest paediatric round cell sarcoma, a number ICD-O-3.2 assigns to a benign bone cyst.

The tree emits `9364/3` for every Ewing sarcoma. The Group 8 session found the same fact
independently and makes the same choice for bone.

## 2. The baseline, and what it did and did not settle

**Sbaraglia M, Bellan E, Dei Tos AP.** *Pathologica* 2021;113(2):70–84, read in full from Europe
PMC. Twelve tables of WHO 2020 soft tissue entities, **no ICD-O codes printed**. It settled which
entities exist; ICD-O-3.2 settled the codes.

**Pfister SM, et al.** *Cancer Discovery* 2022;12(2):331–355 — unlike Groups V and VI, it has a soft
tissue section and a Table 2 of paediatric entities (read from the table image). It is the evidence
for paediatric occurrence (ruling 1). Recorded in `docs/group_baseline_documents.md`.

**No registry-implications paper exists** for this group (the MeSH sweep in `Group 9 Papers/`).

Four WHO 2020 entities have no ICD-O-3.2 code: CIC-rearranged sarcoma, sarcoma with BCOR genetic
alterations, round cell sarcoma with EWSR1–non-ETS fusions (WHO gives `9367`, `9368`, `9366`), and
myxoid pleomorphic liposarcoma. The tool codes them `8803/3` and `8850/3`. Registrar questions B1, B2.

## 3. Where the sources disagree with the pathway, and what won

The pathway document (v1, 2 July 2026) predates the registrar's rulings of 4 September and the
Group 3 method. Its structural diagnosis — a lineage router, IHC surrogates, the Kaposi misrouting
trap — is right and is built. Twelve of its statements are corrected; the table is contract §5.
The four that change codes:

| The pathway says | What the sources say |
|---|---|
| Ewing sarcoma `9260` | `9364/3` (§1) |
| No soft tissue sarcoma is imaging-codable; imaging is "never an entity code" | Visser 2023 Table 3, p. 04, read off the PDF page: sarcoma NOS `8800/3`, liposarcoma `8850/3`, leiomyosarcoma `8890/3`, angiosarcoma `9120/3` at basis 2 — and **Kaposi sarcoma of the skin `9140/3` at basis 1** |
| `9140` must not resolve without LANA positive | Contradicts the basis-1 row; not built as a gate (registrar questions E1, E2) |
| DFSP `8832`/`8833` are Group IX codes | Both moved to behaviour 1; only fibrosarcomatous DFSP is `8832/3` |

The basis-1 Kaposi sarcoma row is the most consequential single fact for this registry. In a
KSHV-endemic paediatric population it will be the commonest Group IX registration made without
pathology, and the pathway does not mention it.

## 4. The tree

`g9_soft_tissue`, 26 nodes, 182 options, 20 checklist rules. **Named diagnosis first, markers
second:** a pathology report states a diagnosis and the registry codes it, so the lineage nodes are
picklists of named entities, and the three checklists (`st_round_cell_ihc`, `st_spindle_ihc`,
`st_epithelioid_ihc`) handle the descriptive report. One node after "histology present" captures what
the report holds and asserts basis 7 or 8 once, so a defining fusion raises the basis without every
named option carrying it.

Three rules were changed after checking the pathway's sources against the PDFs held in
`Group 9 Papers/`:

- **H3K27me3 loss codes MPNST only with nerve sheath features.** Martinez & Fritchie 2018 give loss
  in 34–73% of MPNST and in some synovial sarcomas, fibrosarcomatous DFSP and melanomas.
- **Myogenin is asked before pan-TRK.** Hung 2018: pan-TRK is "highly sensitive but not entirely
  specific", and spindle cell rhabdomyosarcoma is among its positive mimics.
- **SMARCB1 loss never sets a code without morphology.** Agaimy 2014 Table 1: loss in 50% of
  epithelioid MPNST, 10–40% of myoepithelial carcinoma, 16% of extraskeletal myxoid
  chondrosarcoma. Rhabdoid tumour needs the loss **and** rhabdoid morphology; brain, kidney and liver
  sites refer to Groups III, VI and VII first.

## 5. Shared-layer changes — coordinated with Groups 7 and 8

Agreed by message with both sessions on 2 October 2026, and recorded in their reports too:

| Group 9 changed | Left to its owner |
|---|---|
| `groups["9"]` built | `dual_group_rules["9260"]` re-key to `9364`/`9365` — **Group 8** |
| lymphadenopathy archetype and `C77.9` list Group 9 (nodal Kaposi sarcoma) | any `9180`/`9220`/`9231`/`9240` rule, the `tumour_origin` discriminator — **Group 8** |
| `dual_group_rules["9473"]` removed; its exemption deleted from the CNS check | `dual_group_rules["8963"]` liver branch, a new `8991` rule, the C22 branch of `8000-8005` — **Group 7** |
| 39 topography codes in six new rows (skin, bladder, prostate, vulva/vagina/cervix, paratesticular, extrahepatic bile duct); Group 9 added to orbit, nasopharynx, lymph node | |

**Expected merge conflicts, all mechanical:** `build_database.py` (the `GROUP8`/`GROUP9` lines in the
behaviour table and the two guards; the group check blocks inserted after Group 6's), the end of
`docs/clinical-warnings.md`, the Group sections of `docs/codes-awaiting-redcap.md`, and
`alias_index.json`, which is generated — rebuild it after merging. Keep both sides of each. The
README's status sentence ("Groups 1 to 6 are built") was left alone on purpose; set it once, after
all three branches merge.

## 6. Layer 1

`docs/group_09_layer1_repair.md`. 72 of 136 options are not the ICD-O-3.2 preferred term at
behaviour 3. The dangerous ones: two retired numbers (`9260`, `9150`) and three labels naming a
benign or behaviour-1 lesion on a malignant code (`8825` *Myofibroblastoma*, `9220` *Chondroma*,
`8832` *Dermatofibrosarcoma, NOS*). Four ICD-O-3.2 codes (`8714`, `9045`, `9137`, `9542`) have no
option; the REDCap Registry docs already drafted them on 13 August 2026. Nothing was applied to the
live form, and no live API call was made.

## 7. What the browser found that the build did not

Five scenarios driven at `http://localhost:8819`:

| Scenario | Result |
|---|---|
| Lymphadenopathy → lymph node → biopsy with LANA-positive Kaposi sarcoma | `9140/3`, IXc, C77.9, basis 7 — Group IX offered beside lymphoma |
| Cutaneous lesion → skin C44.7 → clinical note, Kaposi sarcoma of the skin | `9140/3` at **basis 1**, histology and IHC outstanding |
| Thigh mass → descriptive round cell report → stains one at a time | `9364/3`, IXd2, after eight stains; the REDCap out-of-date-label banner fires on `9364`'s *Peripheral neuroectodermal tumor* label |
| Thigh mass → named rhabdoid tumour → SMARCB1 loss | `8963/3`, IXd3; the brain, kidney and liver referrals correctly dead at C49.2 |
| Incidental imaging → retroperitoneum → "sarcoma likely" | `8800/3` at basis 2, histology outstanding |

**One defect, fixed.** The cutaneous Kaposi sarcoma output read "Histology, IHC would yield a more
specific code." `9140` is already the specific code; a biopsy confirms it. That is the overstating
class the project tests first. The two Kaposi sarcoma branches where the confirming test is known to
be missing now carry an authored upgrade line saying the test would confirm and would not change the
code.

**Three engine findings, not fixed here — `app.js` is shared and none is group-specific:**

1. **The automatic upgrade sentence overstates confirmatory tests everywhere.** "X would yield a more
   specific code" is printed for any outstanding test, including immunohistochemistry on a named
   entity coded from H&E alone, where the test would confirm, not refine. A wording change in
   `finish()` would fix every group.
2. **The express lane silently enters the lowest-numbered group** for a term several groups share
   (`hit.groups[0]`). Ten Group 9 strings are shared: the rhabdoid and INI1 terms with Group 6, the
   peripheral PNET wordings with Group 4. Typing *Rhabdoid tumor, NOS* for a soft tissue case enters
   the kidney tree. This predates Group 9 — those strings already mapped to Groups 6 and 4 alone —
   but the express lane should ask which group when a term maps to more than one.
3. **The family question says "Which does the pathology report support?"** even on the clinical-note
   route, where there is no pathology report.

## 8. The alias layer

`data/aliases/aliases_group_09.json`, 237 records, built by one subagent against contract §6 and
validated twelve ways. 40 records map to no code (benign, intermediate, or another group). NCIt IDs
only from the alias instructions' confirmed list; five of those rows pair the right entity with a
retired code, and the record says so. Two decisions are the registrar's (questions C2).
`alias_index.json` is now 36.6 KB against the ~30 KB guidance: a WARN, and Groups 7 and 8 will add
to it.

## 9. What needs you

`docs/group_09_registrar_questions.md`, sections A–J. The five starred: Ewing at `9364` and the REDCap
`9260` option (A1); the DFSP labels (A2); the Ewing-like sarcomas at `8803` (B1); fusion-negative
alveolar rhabdomyosarcoma (D1); the basis-1 cutaneous Kaposi sarcoma route (E1).

## 10. Proof

1. `python3 build/build_database.py` → **0 FAIL**, 76 WARN. Group 9's own WARNs: two `[obs]`-only
   entries (`9560`, `8853`), four codes awaiting REDCap, the alias index size.
2. `python3 build/induce_flow.py` → every rule in every checklist has a witness.
3. `node build/check_engine_flow.mjs` → Group 9's three checklists swept exhaustively, OK.
4. **44 negative controls and correct-data probes on the ten Group 9 rules, all as expected**, plus
   controls on the round trip and on the removed `9473` exemption: `docs/group_09_negative_controls.md`,
   pinned to `a46d52c`.
5. Five browser scenarios (§7).
6. Groups 1–6, their alias files, `app.js`, `index.html`, `uccf-tool.css`, `induce_flow.py` and
   `check_engine_flow.mjs` are byte-identical to `main`.

## 11. Not done

- **The Diagnostic Pathway document itself was not edited.** It lives in the vault, outside this
  repository; contract §5 lists its errors for whoever revises it.
- **Twenty-two inventory codes have no tree leaf** by design (contract §1): `[obs]`-only codes, bone
  osteosarcoma subtypes at soft tissue sites, and codes with no WHO 2020 soft tissue entity.
- **The Visser imaging subtype rows (`8850`, `8890`, `9120`) are built** pending registrar
  question F.
