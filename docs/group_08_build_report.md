# Group VIII — build report, 2026-10-02

Branch `claude/group-8-tumor-pathway-64edbc`, a worktree cut from `main` at `cff8149`. Built
overnight while the registrar was away. Every decision that needed the registrar was taken on a
stated default, and each one is listed in `docs/group_08_registrar_review.md`.

| Document | What it holds |
|---|---|
| `docs/group_08_build_contract.md` | the plan: pre-context, code inventory, tree architecture, shared-layer changes, rules |
| `docs/superpowers/specs/2026-10-02-group-08-bone-code-decisions-design.md` | decisions D1–D15, each with its options and sources |
| `docs/group_08_registrar_review.md` | **start here** — what needs you, ordered by cost |
| `docs/group_08_layer1_repair.md` | `viii_morph`, pick by pick |
| `docs/clinical-warnings.md`, Group VIII | the warnings the tool does not show |

---

## 1. What this group is, and the fact that reshaped it

ICCC-3 Group VIII, malignant bone tumours: 48 usable ICD-O-3.2 records across nine subgroups,
all behaviour 3. In children it is mostly osteosarcoma and Ewing sarcoma.

### ★ Ewing sarcoma is `9364/3`, and REDCap offers it on `9260`

ICD-O-3.2 deleted `9260/3` Ewing sarcoma and moved it to `9364/3` (IARC *Deleted codes and their
terms*, 9 October 2020, p. 6). `9260` now means *Aneurysmal bone cyst*, a benign lesion. The
Diagnostic Pathway (13 June 2026), the alias build instructions (14 May 2026), the router's
dual-group rule and `viii_morph` pick 33 all still put Ewing sarcoma on `9260`. A clerk coding
the second commonest malignant bone tumour of childhood today records a benign code.

The tool emits `9364/3` everywhere. A build rule fails any reference to `9260` at a behaviour
ICD-O-3.2 does not carry (§6). The REDCap repair is in the package.

A consequence for reporting: the ICCC-2017 table files `9364` at bone in **VIIIc2** ("pPNET of
bone"). Ewing sarcoma coded to ICD-O-3.2 leaves VIIIc1, which keeps only Askin tumour.

## 2. The baseline

The baseline table gave Group VIII a soft-tissue paper and flagged that it does not cover
bone. The build did not wait for a purchase. Codes come from WHO 2020's own bone Table 1,
reproduced with permission in the International Collaboration on Cancer Reporting bone dataset.
The narrative comes from Anderson & Doyle 2021, held in `Group 8 Papers/`. Odontogenic tumours
come from Soluk-Tekkesin & Wright 2022 through Europe PMC. No registry-implications paper
exists for bone (32-record MeSH sweep, no candidate). Choi & Ro 2021, the natural summary
paper, is paywalled and on the registrar's list.

Four papers in `Group 8 Papers/` were opened (Anderson, Menendez, Sharif, Kallen), each for a
claim the tree rests on. They were first read through macOS PDFKit, which reports PDF page
indices. On 3 October 2026 PyMuPDF was installed, and every page citation was rechecked against
the printed page numbers (§9).

## 3. Where the sources disagree

| | WHO 2020 | ICD-O-3.2 (9 Oct 2020) | Built |
|---|---|---|---|
| Chondrosarcoma grade 1 | `9222/3`* | `9222/1`, with atypical cartilaginous tumour | behaviour exclusion `9222/1`, registrar flag |
| Round cell sarcomas (CIC, BCOR, EWSR1–non-ETS) | `9367/3`*, `9368/3`*, `9366/3`* | absent | `8803/3` *Round cell sarcoma, NOS* |
| Undifferentiated pleomorphic sarcoma of bone | `8802/3` | term on `8830/3` | `8830/3` |
| Telangiectatic, small cell osteosarcoma; chondroid chordoma | under the parent code | `9183`, `9185`, `9371` live | coded as written |
| Metastasizing ameloblastoma | benign category (WHO 2022) | `9310/3` | `9310/3` |

\* WHO's asterisk: "approved by the IARC/WHO Committee for ICD-O at its meeting in January
2020". None of the asterisked numbers reached the final ICD-O-3.2 file, and the tool codes to
ICD-O-3.2.

The Diagnostic Pathway is wrong in ten places (contract §5), most importantly the `9260`
coding and its statement that poorly differentiated chordoma has no code (WHO 2020: `9370/3`).

## 4. The tree

`g8_bone`, 18 nodes, one `ihc_checklist`. An evidence gate leads to four routes:

- **referral:** `8000/3` at basis 1, the only basis-1 code;
- **imaging:** only osteosarcoma is coded on imaging alone (Visser 2023 Table 3), on a
  three-feature constellation from Menendez 2022 p. 99 with three diversion criteria;
  everything else malignant is `8000/3` at basis 2;
- **cytology:** `8001/3` at basis 5;
- **histology:** a matrix router over eleven tumour lines, three cross-group referrals (II,
  IX, and metastases to IV, VI, IX or XII), and the NOS codes.

Imaging-only chondrosarcoma was deliberately not built. Sharif 2021 (p. 4), citing Ardakani et al.
2020, reports a 47% MRI-to-surgery grade mismatch in paediatric central chondrosarcoma. Visser Table 3 would have
allowed it; the registrar has the question.

The Diagnostic Pathway's `decalcification_status` variable was not built (D15). Rulings 11 and
12 already route an unreadable stain to the nearest code, and the tree never sets a code on
FOS or H3.3 G34W. Decalcification is a hint on the round cell panel.

## 5. Shared-layer changes

Agreed with the Group VII and Group IX sessions before any edit:

- **Router:** `groups["8"]` built; `dual_group_rules["9260"]` was dead and is now
  `"9364"` and `"9365"`, closing TODO §8.1; `"8000-8005"` gains a C40–C41 → VIIIe branch,
  recording that 8000-8005 at a bone site is VIIIe; the `tumour_origin` note re-pointed to
  `9364`. None of these rules changes what the tool shows: app.js reads resolveGroup() only
  for its `note`, which these rules do not carry, and nothing reads the routed group. The
  output's group and subgroup come from the tree and the entry.
- **Topography:** six bone codes added: C40.0, C40.1, **C40.2**, C40.3, C40.8, C41.8.
  Before this, the long bones of the lower limb, where most paediatric osteosarcoma and Ewing
  sarcoma arise, could not be selected at all.
- **`build_database.py`:** `GROUP8` registered in the behaviour, round-trip and exact-name
  guards; three Group 8 rules.
- **`app.js`:** no change after the merge with `main`. This branch's behaviour-exclusion title fix
  (§7) was superseded: the Group VII build fixed the same defect on `main` with the registrar's wording (`BEHAVIOUR_LABELS`), and the merge of 4 October 2026 took `main`'s version.

## 6. Rules this group adds

| Rule | Keyed off | Controls |
|---|---|---|
| 1 — no `9260` at a behaviour ICD-O-3.2 lacks | `icdo32.sqlite`, tree, entries, alias file | 4 caught |
| 2 — with no tissue, only `9180/3` or `8000/3`, at basis 1 or 2 | the evidence path, walked from the entry | 5 caught, including R2-D (path, not flag) |
| 3 — no Ewing sarcoma on CD99 alone | the rule's own `positive[]` | 3 caught |

`build/negative_controls_group08.py` reruns all twelve plus three correct-data probes.

## 7. What the browser found that the build did not

Nine paths driven at `localhost:8818`:

| Case | Result |
|---|---|
| Femur, imaging only, three features ticked | `9180` VIIIa, basis 2, histology pending, biopsy upgrade line |
| Femur, descriptive histology, CD99 and NKX2-2 positive, the rest negative or not done | `9364` VIIIc2, basis 7, REDCap label-drift banner pointing at the four-digit code |
| Ewing sarcoma named, fusion shown | `9364`, basis 8 |
| Referral note naming a bone cancer | `8000` VIIIe, basis 1, histology pending |
| Pelvis, chondrosarcoma grade 1 | behaviour exclusion `9222/1`, registrar flag |
| Giant cell tumour of bone | behaviour exclusion `9250/1` |
| Lymphoma in bone | referral to Group II, no code |
| CD99 positive, NKX2-2 not done | screen: "match no rule … records 8002"; output `8002` VIIIe |
| Express lane, "Ewing sarcoma" | one result, Group 8, entering at the evidence gate |

Two defects, both of the kind the project tests for first, because each made a case look other
than it was:

1. **Every behaviour exclusion was titled "Benign".** Giant cell tumour of bone, atypical
   cartilaginous tumour and chondrosarcoma grade 1 are behaviour 1. Fixed in `app.js` from the
   behaviour digit; at the merge, the Group VII build fixed the same defect on `main` with the registrar's wording (`BEHAVIOUR_LABELS`), and the merge of 4 October 2026 took `main`'s version. The banner now reads "Uncertain whether
   benign or malignant — outside this group's declared behaviour".
2. **`8002/3` said "workup complete"** on a panel that stopped before NKX2-2. It now requires
   IHC, so the missing stain shows as pending.

A third came from the build, not the browser. The Layer 1 option file had `9364`'s line
outside a code fence, so the parser could not see an option that REDCap has. Fenced; recorded
for the registrar.

## 8. What needs you

`docs/group_08_registrar_review.md`, in order: chondrosarcoma grade 1 (A1), the round cell
sarcomas (A2), undifferentiated pleomorphic sarcoma (A3), whether intermediate tumours are
registered anywhere (B1), imaging-only chondrosarcoma (B3), REDCap pick 33 (C1), and the CD99
threshold between Groups IV and VIII (D1).

## 9. Proof

- `python3 build/build_database.py`: **578 checks, 0 FAIL**, BUILD PASSED; engine gate
  "Every stopped flow delivers what the screen promised."
- `python3 build/induce_flow.py`: every rule in every checklist has a witness;
  `bn_round_cell_ihc` is swept to budget, reported as partial (TODO §20).
- Negative controls: 12 of 12 caught, 3 of 3 probes pass.
- `group_01`–`group_06` data and alias files, `index.html` and `uccf-tool.css`
  byte-identical to `main`.
- Page citations: 35 cited claims located on their printed pages with PyMuPDF. Two corrected:
  the telangiectatic diversion is Menendez pp. 109–110, not p. 109, and the 47% chondrosarcoma
  grade mismatch is Ardakani et al. 2020 as cited by Sharif 2021, p. 4.
- New WARNs, both recorded: the alias index size (TODO §24) and ICCC-2017 range 60 (TODO §25).
