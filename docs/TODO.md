# Lookup tool — open items

Things found while building that are real and are not fixed. Each says what closing it takes.
Nothing here blocks the current build.

**Citation convention.** A claim names the paper and the page, not the series. Abbreviations
that have a full form are written out.

---

## 1. The eleven obsolete terms, with the source of each

Removed from the decision tree on the registrar's ruling of 14 September 2026. The
`morphology_entries[]` objects are retained and flagged `obsolete_term: true` so historical
records and alias input still resolve; only the tree stopped reaching them. Narrative and the
re-pointing table: `docs/group_03_obsolete_terms.md`.

**Thirteen were removed; two came back.** `[obs]` marks a TERM STRING, not a code — see §2 below
for the evidence and for what replaced the test. `9430/3` and `9480/3` are in the tree.

**Where the obsolescence finding comes from.** International Agency for Research on Cancer,
*International Classification of Diseases for Oncology, third edition, second revision*
(ICD-O-3.2), morphology table — IARC's **final** workbook `ICD-O-3.2_final_update09102020.xls`,
9 October 2020, SHA-256
`7ca51dcb66107d6462b43212b26aa65d52f6b0e306c6295e8c751416b3278a21`, sheet *ICD-O-3.2
Morphology*, 2,955 data rows, **column `obs`**. Converted to
`ICD coding/ICD-O-3.2/icdo32.sqlite` by `ICD coding/ICD-O-3.2/convert_icdo32.py`; the row
numbers below are `source_row` in that table, which is the workbook's own row.

285 of the 2,955 rows carry `[obs]` and it is the column's only value. For all eleven below,
**every** row on that code at that behaviour is marked — preferred term and synonyms alike — so
there is no non-obsolete string to fall back on, **and** no current WHO entity lives on the stem.

**Where the subgroup comes from.** International Classification of Childhood Cancer, third
edition, 2017 recode table, converted to `Cancer Registry/ICCC-2017.sqlite`. Every Group III
range is declared `icdo3_behavior = '0-1,3'` with topography `C00.0–C80.9` unless noted.

| ICD-O-3.2 code | Obsolete preferred term | ICD-O-3.2 workbook row | ICCC-3 subgroup | Tree now emits |
|---|---|---|---|---|
| `8280/0` | Acidophil adenoma | 569 | IIIe1 Pituitary adenomas and carcinomas | `8272/0` Pituitary adenoma, NOS |
| `8280/3` | Acidophil carcinoma | 571 | IIIe1 | `8272/3` Pituitary carcinoma, NOS |
| `8281/0` | Mixed acidophil-basophil adenoma | 575 | IIIe1 | `8272/0` Pituitary adenoma, NOS |
| `8281/3` | Mixed acidophil-basophil carcinoma | 576 | IIIe1 | `8272/3` Pituitary carcinoma, NOS |
| `8300/0` | Basophil adenoma | 591 | IIIe1 | `8272/0` Pituitary adenoma, NOS |
| `8300/3` | Basophil carcinoma | 593 | IIIe1 | `8272/3` Pituitary carcinoma, NOS |
| `9360/1` | Pinealoma | 2072 | IIIe3 Pineal parenchymal tumours | `8000/1` Neoplasm, uncertain whether benign or malignant |
| `9410/3` | Protoplasmic astrocytoma | 2138 | IIIb Astrocytomas | `9400/3` Astrocytoma, NOS |
| `9460/3` | Oligodendroblastoma | 2182 | IIId1 Oligodendrogliomas | `9450/3` Oligodendroglioma, NOS |
| `9472/3` | Medullomyoblastoma | 2192 | IIIc1 Medulloblastomas | `9470/3` Medulloblastoma, NOS |
| `9535/0` | Haemangioblastic meningioma | 2278 | IIIe5 Meningiomas | **no code — refers to Group IX** |

Row numbers are the **final** workbook's, which runs two rows longer than the 2019 draft in this
range; the draft's numbers were 568, 570, 574, 575, 590, 592, 2071, 2136, 2180, 2190, 2276.

Reproduce the finding:

```sql
SELECT code4, behaviour, source_row, level, term
FROM   icd_o_3_2_morphology
WHERE  trim(coalesce(obs,'')) = '[obs]'
ORDER BY code4, behaviour;
```

**Supporting classification evidence for two of them**, where a paper rather than the table
explains why the term went:

- `9410/3` **Protoplasmic astrocytoma** — subsumed into diffuse astrocytoma. Louis DN, et al.
  *The 2021 WHO Classification of Tumors of the Central Nervous System: a summary.*
  Neuro-Oncology 2021;23(8):1231–1251, **Table 1, p. 1233** (the circumscribed and adult-type
  diffuse astrocytic lists carry no protoplasmic entry).
- `9460/3` **Oligodendroblastoma** — Group 3 Diagnostic Pathway Revision 2 §4.8 already directed
  these to `9450`.

## 2. ✅ Settled — `9430/3` and `9480/3` are restored

**`[obs]` marks the term, not the number.** Established 14 September 2026 against IARC's own
documents, and the ruling applied: a code leaves the decision tree only when **no current WHO
entity lives on its stem**, not merely when ICD-O-3.2 prints no usable string.

| ICD-O-3.2 code | ICD-O-3.2 term | WHO CNS5 entity on this code | ICCC-3 |
|---|---|---|---|
| `9430/3` | Astroblastoma `[obs]` | **Astroblastoma, MN1-altered** | IIId3 |
| `9480/3` | Cerebellar sarcoma, NOS `[obs]` | **Primary intracranial sarcoma, DICER1-mutant** | IIIc1 |

**`9535/0` was corrected on 15 September 2026** — it now refers to **Group IX** and emits no
code, rather than falling back to `9530/0` Meningioma, NOS. Haemangioblastic/angioblastic
meningioma is the historical name for meningeal haemangiopericytoma, which WHO CNS5 retires in
favour of solitary fibrous tumour (Louis DN, et al. Neuro-Oncology 2021;23(8):1231–1251,
**p. 1248**); that is `8815`, ICCC-3 IXb1. See `docs/group_03_obsolete_terms.md` §4.1.

Both entities are WHO CNS5 Table 1 types — Louis DN, et al. 2021, Neuro-Oncology 23(8),
**Table 1, pp. 1233–1235**. Both are assigned these ICD-O-3.2 codes by the Belgian Cancer
Registry's CNS5 coding table, under its footnote *"These entities have undergone a change in
terminology of a previous code"* — the terminology changed, the number did not. Evidence and
the independent checks: `docs/group_03_obsolete_terms.md` §1.

### 2.1 ✅ Settled — *Primary intracranial sarcoma, DICER1-mutant* is now reachable

Built 15 September 2026. One shared node, **`st_dicer1_sarcoma`**, reached from four compartment trees.

**Why it needed building.** `g3_supratentorial` had no mesenchymal family option at all, so an
intra-axial sarcoma fell to `8000/3` "no family can be assigned". The only route to `9480/3` was the
posterior-fossa branch, behind a descriptor requiring the report to say *cerebellar sarcoma* — and the
entity is **92% supratentorial**, median age **6 years**, 87% paediatric (Tauziède-Espariat A, et al.
*Mesenchymal non-meningothelial tumors of the central nervous system: a literature review and diagnostic
update.* Acta Neuropathologica Communications 2023;11(1):22). The one route we had was in the 8% tail.

**Reached from** `st_lesion_gate` (new option), `pf_family_triage` (re-pointed), `sp_morphology_pattern`
(new option) and `mn_lesion_triage` (new option, leptomeningeal or dural). **`g3_midline` deliberately
does not reach it** — registrar's ruling, no reported sellar or pineal case, and the pineal myogenic
differential is alveolar rhabdomyosarcoma with a *FOXO1* fusion, a different tumour.

**Six outcomes, one code.** Every branch emits `9480/3`; only the diagnosis, basis and confidence move.
*DICER1* sequencing or the methylation class gives Track A *Primary intracranial sarcoma, DICER1-mutant*
at basis 8, high confidence. Supporting immunohistochemistry — H3K27me3 loss, nuclear TLE1 — gives Track
B at medium. No testing gives Track B at low with a provisional-pending naming the resolving test. A
negative *DICER1* result gives Track B suffixed NEC. The legacy *cerebellar sarcoma* wording is preserved
as the sixth outcome.

**No grade on any branch** — WHO CNS5 assigns none to the newly recognised mesenchymal types.

**Germline referral on all six**, carried in `upgrade_path`: about a quarter of reported cases with
constitutional data carry a germline *DICER1* alteration, and none of the patients in the founding
series had a recognised cancer syndrome at diagnosis (Koelsche C, et al. *Primary intracranial spindle
cell sarcoma with rhabdomyosarcoma-like features share a highly distinct methylation profile and DICER1
mutations.* Acta Neuropathologica 2018;136(2):327–337).

`9480`'s `confidence_ceiling` was raised **low → high**. It was set when the code was a legacy string
only, and it was flooring a molecularly confirmed case at low confidence — caught by driving the branch,
not by the build.

Design record: `docs/superpowers/specs/2026-09-15-dicer1-intracranial-sarcoma-design.md`.

#### 2.1a ⬜ Open, cosmetic — the resource-level gate says "the unspecified family"

The gate's `family` vocabulary has ten values and **none is mesenchymal**, so the node declares
`unspecified`. The clerk-facing line therefore reads *"Resource level IV is required for the
**unspecified** family"* — honest, but clumsy. Adding `mesenchymal` would read better but changes a
closed list that Groups 1 and 2 also validate against. Left pending a ruling.

---

### 2.2 — withdrawn, filed in error

This item claimed `8280/0` Acidophil adenoma was routed too coarsely and that a prolactin branch was
needed to reach `8271/0` Lactotroph adenoma. **The tree already does this.** `md_pituitary_ihc` reads
PIT1, TPIT and SF-1 before the hormone stains, emits `8271/0` on PIT1 + prolactin at high confidence on
the WHO track, and emits it on prolactin alone at medium on the descriptive track. Its hint already
states the principle: *"every lineage except lactotroph is an ICD-O-3.2 Related term on 8272/0"*. The
H&E-only route sending "acidophil pattern" to `8272/0` is correct, not coarse — without
immunohistochemistry lactotroph cannot be asserted. The item was written from the obsolete-recode table
without checking the immunohistochemistry node.

---

## 3. Layer 1 — REDCap side

### 3.1 `C71.0` Cerebrum is missing from the topography dropdown

`ICD coding/RedCap Options/Topography Redcap.md` jumps from `709, Meninges, NOS` to `711,
Frontal lobe`. There is no `710`. Verified against the live list, 14 September 2026.

**Why it matters.** Group III is the first group to key its decision trees to anatomical
compartment, and C71.0 is the supratentorial compartment's own code — cerebrum, and with it
**thalamus, basal ganglia and hypothalamus**. A thalamic diffuse midline glioma, H3
K27-altered, lands there. The tool routes C71.0 to `g3_supratentorial`; a clerk with no
dropdown value will pick `C71.9 Brain, NOS`, which is a different compartment and a different
tree.

**To close:** add `710, Cerebrum (Supratentorial NOS, Basal ganglia, Cerebral cortex, Corpus
striatum, Globus pallidus, Hypothalamus, Thalamus)` to `topo_code`. It is an **append**, so no
existing pick renumbers — confirm against the field's current ordering first, since `topo_code`
is positional in the same way `iii_morph` is.

`data/shared/topography_codes.json` already carries C71.0 with `redcap_code: null`.

### 3.2 `9476/3` has no REDCap option

The only Group III code with no `iii_morph` entry. Built under registrar ruling 3 of 4 September
2026. Detail, including the `iii_extended` / `iii_subgroup` formula change: `docs/codes-awaiting-redcap.md`.

### 3.3 Ligature damage in `Topography Redcap.md`

The sweep of 14 September 2026 concluded Group 3 was the only affected **morphology** option
file. `Topography Redcap.md` is a thirteenth file and was not swept: `so!` for *soft* (lines 30,
56, 278), `Le!` for *Left* (line 97), `"roat` for *Throat* (line 65). **None is in the CNS
block.** Documentation defect.

---

## 4. Schema gaps — three trees hit each of these independently

### 4.1 No marker answer means *loss* as distinct from *not done*

`markerOff()` returns true for an absent marker, an explicit `neg` and `nd` alike. A rule
written `negative: ["SMARCB1 (INI1)"] → 9508` fires for a laboratory that **never ran the
stain**.

Both embryonal trees found it independently and worked around it the same way: SMARCB1 (INI1),
BRG1/SMARCA4 and H3 K27me3 were moved off the marker grid into option-based capture nodes, each
offering an explicit *performed but uninterpretable* state. It works, but the three most
important stains in this group are now asked as evidence questions rather than as markers.

**To close:** a marker answer meaning *loss* (or *retained*), distinct from *not done*.

### 4.2 `refer_group` cannot say "code the primary at Stage 1"

One integer 1–12, and a metastasis's destination depends on a primary the tree has not captured.
Three trees hit this; all used `refer_group: 12` with the real instruction in `reason`.

**To close:** a fifth branch destination — `refer_stage: 1`, or a `recapture_site` terminal.

### 4.3 `provisional_pending` holds only one `resolving_test`

Group 3 Diagnostic Pathway Revision 2 §4.8 requires naming **both** isocitrate dehydrogenase
(IDH) mutation and 1p/19q co-deletion for an untested oligodendroglioma. The supratentorial tree
names one in the schema field and the second in a non-schema `additional_resolving_tests[]`.

### 4.4 "Methylation" is not in the closed diagnostic-test vocabulary

Resource level V is reached by DNA methylation profiling throughout this group, but the closed
set is `Referral only · Histology · Imaging · IHC · ISH · Flow cytometry · Cytogenetics/FISH ·
Molecular/PCR`. Trees use `Molecular/PCR`; the engine's `methylation_counts_as: 8` basis default
matches on the evidence-gate token instead.

### 4.5 `check_fallback_chains` keys the fallback graph by code alone

`nxt[code] = fb`, with `fb == code` failed as a self-reference. An entry falling back to a
**different behaviour of the same code** is rejected, and where two behaviours of one code have
different targets only the last written is checked.

**What it costs.** Sahm F, et al. *cIMPACT-NOW update 8: Clarifications on molecular risk
parameters and recommendations for WHO grading of meningiomas.* Neuro-Oncology
2025;27(2):319–330 — the recommendation that a brain-invasive otherwise-benign meningioma
without molecular data be reported as *meningioma, not otherwise specified* with the grade
omitted is at **pp. 324–325**. That is literally `9530/3` → `9530/0`. The validator forbids it,
so the case goes to `8000` instead, which drops "meningioma" from the record. Three more are
compromised the same way: `9390/1` → `8000/1` where `9390/0` was right, `9391/1` → `9380/3`,
`9505/3` → `8000/3`.

**Not urgent:** `app.js` never reads `nos_fallback_code`; the engine uses the node-level
`nos_fallback`, which carries a behaviour. Nothing miscodes today.

**To close:** key by `(code, behaviour)`; add `nos_fallback_behavior_code` to the entry schema.

---

## 5. Behaviour

### 5.1 Six fallbacks raise behaviour

ICD-O-3.2 has no `/0` or `/1` NOS code in these families, so the alternatives are the family's
`/3` NOS or `8000`. Group 3 Diagnostic Pathway Revision 2 §4.7 says keep the family rather than
discard established morphology:

| Entry | Falls back to |
|---|---|
| `9421/1` Pilocytic astrocytoma | `9400/3` Astrocytoma, NOS |
| `9384/1` Subependymal giant cell astrocytoma | `9400/3` Astrocytoma, NOS |
| `9442/1` Gliofibroma | `9400/3` Astrocytoma, NOS |
| `9391/1` Sellar ependymoma | `9380/3` Glioma, malignant |
| `9431/1` Angiocentric glioma | `9380/3` Glioma, malignant |
| `9444/1` Chordoid glioma | `9380/3` Glioma, malignant |

Now that non-malignant CNS tumours are registered, a pilocytic astrocytoma whose subtype cannot
be confirmed falls back to a **malignant** code. Structurally the same as the open Group 2
question on `9740/1` Mastocytoma, NOS against a `/3`-only ICCC range. **Registrar's ruling wanted.**

### 5.2 `9391/1` Sellar ependymoma is unreachable

107 of 108 entries are reachable. A sellar ependymoma arises at C75.1, which routes to
`g3_midline`, and that tree has no ependymal branch. Rare, but `terminal_reachable` exists to
catch exactly this.

---

## 6. Pre-existing, outside Group 3

### 6.1 All four Group 2 `prior_probability` blocks never render

`markerFlow()` asks one marker at a time and never renders marker groups, so it never renders
their priors. `nodeControl()` routes to `markerFlow` whenever a `branch_sequence` exists, which
`induce_flow.py` puts on every `ihc_checklist`. Only `markerGrid()` renders them, and it is now
unreachable in Groups 1 and 2.

Affected: `g2_hodgkin`, `g2_matureB`, `g2_nkt`, `g2cut_ebv_cutaneous` — every marker-group prior
Group 2 has. `check_prior_probability` passes them because it validates shape, not reachability.

---

## 7. Configuration — the site profile

`resource_level_gate` is authored on 97 branches across 41 nodes, validated and rendered, and it
changes no routing, because nothing declares a resource level.

The gate needs a level **per tumour family**, never one number per site: a laboratory with
glial fibrillary acidic protein (GFAP), synaptophysin and SMARCB1 (INI1) is at resource level
III for atypical teratoid/rhabdoid tumour and level II for ependymoma.
`data/shared/site_profile.template.json` says in its own text that `app.js` does not read it
until wired in deliberately, and `site_profile.json` does not exist.

The engine runs three states — blocked, available, **not established** — and with no profile
everything is the third, which deliberately does not divert (diverting on an undeclared profile
would emit a fallback code on no evidence) and does not dangle the test as an upgrade either.

**Corrected 14 September 2026: `required_rl: "V"` is no longer an exception.** It used to be
treated as above any declarable profile, so it always read *unavailable* and always diverted. It
was wrong on both counts. A site declared resource level V MEETS a requirement of resource level
V — reaching the last rung is not sitting above it — so an undeclared profile settles nothing
there either. The effect was not theoretical: all 14 resource level V branches in Group 3
diverted to their `unreachable_destination`, which discards `basis_of_diagnosis` and
`diagnosis_rendering` by design, so a clerk who recorded *"methylation profiling assigns the
MN1-altered astroblastoma class"* was answered with a bare code, no WHO CNS5 diagnosis, no basis
of diagnosis, confidence **low**, and the sentence *"The test is unavailable"* — about a test the
same clerk had just said was performed. It now reads *"not established — confirm it before
recording it as a next step"*, and the branch is taken.

The flag that carried the old rule, `upgrade_line_says_unavailable`, is banned; the build FAILs
on it. Unavailability follows from a **declared** site level below the requirement and from
nothing else.

**To close:** write `data/shared/site_profile.json` and wire the fetch.

> **Build it as a template, not as one registry's inventory.** This tool is for any registry
> anywhere; the Uganda Cancer Institute is one deploying site among many. The file ships with
> every family present and unset, and each site fills in what its own laboratory can do. A site
> at the top of the scale is as normal a case as one at the bottom, and no branch, label or
> default should assume otherwise. The resource-level machinery asks what a laboratory can do;
> it must stay neutral about the answer.

Families in use: `ependymal`, `embryonal`, `diffuse_glial`, `glioneuronal`, `meningothelial`,
`sellar`, `pineal`, `choroid_plexus`, `pituitary`, `unspecified`.

---

## 8. Clinical rulings still owed

1. **`9392/3` and `9393/3`** — WHO CNS5 abolished anaplastic ependymoma and papillary ependymoma
   as types (Louis DN, et al. 2021, Neuro-Oncology 23(8), Table 1 p. 1233, and the ependymal
   discussion at p. 1238). The tree emits them where the report uses the word, while the
   *rendered* diagnosis is the CNS5 type. Code and diagnosis deliberately disagree on those two
   branches; folding both into `9391/3` is the alternative.
2. **`9425/3` pilomyxoid astrocytoma versus `9421/1` pilocytic astrocytoma** — CNS5 folds
   pilomyxoid into pilocytic astrocytoma as a pattern, but the two codes differ in **behaviour**.
   Coded as documented, not migrated.
3. **Multinodular and vacuolating neuronal tumour, diffuse leptomeningeal glioneuronal tumour
   and diffuse glioneuronal tumour with oligodendroglioma-like features and nuclear clusters all
   resolve to `8000/1`.** Revision 2 §4.14 offers `9505/1`, `9509/1` or `8000/1` "by morphology";
   none of the three is ganglioglioma-like or papillary-glioneuronal, so either coded neighbour
   would assert a tumour nobody saw.

### Settled since this file was first written

- **Desmoplastic myxoid tumour of the pineal region, SMARCB1-mutant** — **ICCC-3 Group IX**
  (registrar's ruling, 14 September 2026). Group IX is not yet built, so `md_pineal_ihc` rule 0
  now carries `refer_group: 9` and emits no code here. It was previously `8000/1` with a
  code-neutral entity annotation, taken as the conservative default while Revision 2 §4.13 left
  the destination open.

---

## 9. REDCap changes owed — every group, one place

**Added 16 September 2026 at the registrar's instruction: every change that has to be made in
REDCap is tracked here.** This section is the index; the detail lives in the per-group repair
package named against each row. Nothing below has been applied to the live form.

The three safe operations never change: **relabel in place**, **retire in place** (prefix
`[RETIRED]`, the `_code` formula returns blank), **append at the end**. `_morph` fields store a
pick number, not a diagnosis, so **a pick is never deleted** — deleting one renumbers every pick
after it and silently invalidates stored data with nothing that trips a Data Quality rule.

| Group | Field | Relabel | Retire | Append | Status | Detail |
|---|---|---|---|---|---|---|
| **III** | `iii_morph` | 35 labels disagreeing with ICD-O-3.2 | — | `9476/3` | Ready to apply, not applied | `ICD Look Up tool/Group 3 — Layer 1 Repair Package (REDCap iii_morph).md` |
| **III** | `topo_code` | — | — | `710, Cerebrum` | Open — §3.1 above | same |
| **IV** | `iv_morph` | **3** — picks 10, 12, 20 | **8** — picks 1, 4, 6, 9, 14, 16, 17, 19 | **0** | Ready to review, not applied | `ICD Look Up tool/Group 4 — Layer 1 Repair Package (REDCap iv_morph).md` |
| **IV** | `topo_code` | — | — | **0** | ✅ Nothing owed — every Group IV site is already in the dropdown | same, §7 |
| **I, II** | — | — | — | `9715`, `9749`, `9819` | Open | `docs/codes-awaiting-redcap.md` |

### 9.1 Group IV — `iv_morph`, 11 of 26 options are invalid

**11 of the 26 `iv_morph` options carry a term the code does not have in ICD-O-3.2, or a
behaviour ICCC-3 Group IV does not admit.** `ICCC-3 declares behaviour `3`, and only `3`, for
every Group IV range` — that one fact drives six of the eleven.

This does **not** contradict `Registry Data/data dictionary/Group IV Verification.md`, which
found the field clean. That audit asked *does pick N return the code its label says?* and the
answer is still yes for all 26. This asks *does that code actually carry that term, at a
behaviour the group admits?* A pick-to-code audit cannot see a label defect, because the label
is what it trusts. The same blind spot left 35 of 234 `iii_morph` labels wrong while `iii_code`
was formula-correct.

**Retire — 8 picks:** `9490 Ganglioneuroma` (that string is `9490/0`, benign) · `8680
Paraganglioma, benign` and `8680 Paraganglioma, malignant` (neither string exists; `8680/3`
carries one term, `Paraganglioma, NOS`) · `8683 Gangliocytic paraganglioma` (**not a usable
Group IV code at all** — see below) · `8693 Extra-adrenal paraganglioma, malignant` · `8700
Pheochromocytoma, malignant` · `9501 Medulloepithelioma, benign` · `9502 Teratoid
medulloepithelioma, benign`.

**Relabel — 3 picks, no code changes so `iv_code` is untouched:** `8690 Glomus jugulare tumor,
NOS` → **`Middle ear paraganglioma`** · `8692 Carotid body tumor` → **`Carotid body
paraganglioma`** · `9502 Teratoid medulloepithelioma` → **`Teratoid medulloepithelioma, NOS`**.
In all three the current string is a **Synonym** on the same code and the replacement is the
**Preferred** term. Same entity, current wording.

**`8683` is the one that is not a labelling defect.** ICD-O-3.2 carries it at `/0` only —
`Gangliocytic paraganglioma`, `(C17.0)`, duodenum — and WHO 2022 renamed the entity *composite
gangliocytoma/neuroma and neuroendocrine tumor* (CoGNET), moving it out of the paraganglioma
family rather than changing its behaviour (Mete O, et al. *Overview of the 2022 WHO
Classification of Paragangliomas and Pheochromocytomas*, Endocrine Pathology 2022;33(1):90–114,
abstract). Both legs of the two-source test remove it. A record sitting on pick 9 has **no
automatic destination** and is re-coded from the source pathology report.

**After the repair, `iv_morph` has 18 live options for 18 usable codes** — one each, exactly.

**Open and needing a paywalled full text:** whether WHO 2022 states an ICD-O code for CoGNET.
Only Mete's abstract was retrievable (no PMCID, not open access). Until that is answered a CoGNET
case has no settled code in this registry and is a registrar decision.

### 9.2 Pre-flight before any of it is applied

Export `record_id`, `iv_morph`, `iv_code` and count records on picks **1, 4, 6, 9, 14, 16, 17,
19**. Picks 4, 6, 14 and 16 move to the NOS pick on the same code (5, 5, 13, 15) with no recode.
Picks 1, 17 and 19 are **benign tumours outside ICCC-3 Group IV** — out of scope, not miscoded,
and the registrar decides whether the record stays in the registry. Pick 9 is re-coded from the
report. If all eight return zero records the repair is label-and-formula only, which is likely:
the registry began operating in 2025 and Group IV is small.

---

## 10. Pre-existing defects found during the Group 4 build, outside Group 4

### 10.1 The router's `9260` dual-group rule routes a code ICD-O-3.2 no longer carries

`data/shared/presentation_router.json → dual_group_rules → "9260"` routes Ewing sarcoma to
`VIIIc1` at bone and `IXd1` at soft tissue. **ICD-O-3.2 carries `9260` at `/0` only —
`Aneurysmal bone cyst`.** Ewing sarcoma is `9364/3`, which also carries `Peripheral
neuroectodermal tumor`, `PPNET` and `Peripheral primitive neuroectodermal tumor` as its own
synonyms. Verified 2026-09-16 against both the 2019 draft and the 9 October 2020 final workbook,
so it is neither a conversion artefact nor a draft-stage edit.

A Group VIII/IX defect, not a Group IV one, and deliberately **not** touched by the Group 4
build. Closing it means re-pointing the rule to `9364` and re-checking the `VIIIc1`/`VIIIc2` and
`IXd1`/`IXd2` subgroup labels, which change with the code.

### 10.2 The `9501-9504` dual-group rule is stale and misroutes CNS cases — **fixed in Group 4**

Recorded for the audit trail. The rule matched only `C70.9`, `C71.9` and `C72.9` and carried its
own note: *"Extend both files together when Group III is authored."* Group III was authored on
16 September 2026, so a medulloepithelioma at `C71.6` fell through to Group IV, which is wrong —
ICCC-3 gives `9501`–`9504` to Group III across the whole of `C70.0`–`C72.9`. Extended as part of
this build.

---

## 11. CoGNET has no ICD-O code in any source

**Registrar's instruction, 18 September 2026: leave it here and stop chasing it.**

WHO 2022 renamed *gangliocytic paraganglioma* to **composite gangliocytoma/neuroma and
neuroendocrine tumour (CoGNET)**. The old code `8683` exists in ICD-O-3.2 at `/0` only, ICCC-3
Group IV admits `/3` only, so `8683` drops out of the group and `iv_morph` pick 9 is retired
(`ICD Look Up tool/Group 4 — Layer 1 Repair Package (REDCap iv_morph).md` §4).

**No source gives CoGNET an ICD-O code. Four have now been checked in full:**

| Source | What it says |
|---|---|
| **Mete O, et al.** *Overview of the 2022 WHO Classification of Paragangliomas and Pheochromocytomas.* Endocrine Pathology 2022;33(1):90–114 · [DOI](https://doi.org/10.1007/s12022-022-09704-6) | States the rename at p. 94. **No ICD-O code for any entity in 25 pages.** Never mentions `8683`. |
| **Juhlin CC.** *The road ahead: a brief guide to navigating the 2022 WHO classification of endocrine and neuroendocrine tumours.* Journal of Clinical Pathology 2025;78:1–10 · [DOI](https://doi.org/10.1136/jcp-2023-209060) | Names it at p. 8 — *"composite gangliocytoma/neuroma and neuroendocrine tumour, previously called 'gangliocytic paraganglioma'"* — under the heading *paraganglioma-like neuroendocrine neoplasia*. **No code.** Does not say which volume owns it. |
| **Pfister SM, et al.** Supplementary Table S3, the WHO Paediatric Tumours entity list | Gangliocytic paraganglioma and CoGNET both **absent** — consistent with the entity leaving the paraganglioma family. |
| IARC ICD-O-3.2 *Deleted codes and their terms* · *New codes and their terms* · *Summary of main changes* | `8683` is **not** in the deleted list. The summary says only *"In the 3-digit group 868–870 the only remaining non-malignant term is under 8683/0."* No successor code is named. |

**What this costs.** Exactly one thing: a REDCap record sitting on `iv_morph` pick 9 has no
automatic destination and must be re-coded from the source pathology report. The repair package
says so. Nothing in `group_04_dt.json` depends on it — `8683` is an alias input only, resolving to
a terminal that explains the rename.

**What would close it:** the WHO *Classification of Endocrine and Neuroendocrine Tumours*, 5th
edition (IARC Blue Book volume 10) itself, which is not freely available and which the registrar
has already tried to obtain. Or a future IARC ICD-O revision that assigns the entity a number.
**Do not spend further effort on secondary sources — four have been read and all four are silent.**

---

*Last updated 18 September 2026, on the Group 4 build. Previously 16 September 2026.*
