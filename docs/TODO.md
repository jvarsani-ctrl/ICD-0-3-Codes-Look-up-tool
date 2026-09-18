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

## 12. ⚠️ Group 3 defect — three `imaging_pathway` nodes throw at runtime

**Found 18 September 2026 during the Group 4 build. Group 3 is merged to `main`. Not fixed here —
it is outside the Group 4 branch — but it is the most serious open item in this file.**

### What happens

`app.js` resolves an `imaging_pathway` node at line 2217. There are exactly three outcomes: a ticked
diversion criterion or an incomplete constellation goes to `fallbackTarget(n)`; a complete
constellation advances to the node itself. **`options[]` is never consulted**, and
`imagingPathway()` at line 1005 renders only `imaging_features`, `biochemical_questions` and
`diversion_criteria` — never an option list.

`fallbackTarget()` tries `insufficient_next_node`, then `nos_fallback`, then **throws
`'Node has no fallback and did not resolve'`**. `nos_fallback` is forbidden on `imaging_pathway`
(`NOS_FORBIDDEN_TYPES`). So a node with neither crashes.

| Node | `options[]` | `insufficient_next_node` | Result |
|---|---|---|---|
| `pf_imaging_no_tissue` | 6 | **null** | **throws** |
| `st_imaging_pathway` | 4 | **null** | **throws** |
| `sp_imaging_no_tissue` | 4 | **null** | **throws** |
| `md_pituitary_prolactin_route` · `md_pituitary_functioning_route` · `md_cranio_imaging` · `md_pineal_imaging_only` · `md_optic_nf1_imaging` · `mn_imaging_pathway` · `un_imaging_only` | 0 | set | work correctly |

**The pattern is exact:** every node that carries options has no `insufficient_next_node`, and every
node that works has `insufficient_next_node` and no options. The author used `options[]` as the
routing mechanism for this node type; the engine does not support it.

### What it costs

1. **A crash on the common path.** Not an edge case — ticking any diversion feature, or leaving the
   constellation incomplete, is the ordinary outcome for most cases reaching these nodes.
2. **14 authored options are dead**, and one of them matters a great deal:
   `pf_imaging_no_tissue`'s first option routes *"A midline mass with an ELEVATED serum AFP or CSF
   β-hCG"* to **`refer_group: 10`**. A secreting germ cell tumour presenting as a midline
   intracranial mass **never leaves Group III.** The Group 3 contract §4 calls the AFP / β-hCG rule
   one-directional and load-bearing — *"Elevated → refer to Group X and stop"* — and it does not run.

### Why the build did not catch it

`check_orphan_nodes` and the rest validate **shape**, not reachability through the renderer. This is
the failure mode the contract §0 already records for Group 2 — 74 checks, 10 of 10 data traversals
and 102 engine assertions passing while 15 of 61 nodes did not render. Every automated layer tested
the data or the renderer in isolation; the fault was in the seam. **A green build is not a working
tool.**

### To close

Give each of the three nodes an `insufficient_next_node`, and re-home the 14 options. The germ-cell
referral needs a real destination — most likely its own node before the imaging gate, since an
elevated marker should divert *before* an imaging constellation is even offered. Then a validator
rule: **an `imaging_pathway` node must declare `insufficient_next_node`, and must not declare
`options[]`.** That rule would have caught all three the day they were written, and it is cheap.

### How it was found

The Group 4 `g4_sympathoadrenal` author was told to read `pf_imaging_no_tissue` for shape, declined
to copy its `options[]` because they could not see the engine reading them, and said so instead of
guessing. Verified from `app.js` afterwards. The Group 4 trees use `insufficient_next_node`
throughout and are not affected.

---

## 13. ⚠️ Group 3 defect — two `ihc_checklist` nodes render no way to answer them

**Found 18 September 2026 fixing the identical defect on `hn_ihc_checklist` and `sn_ihc_checklist`
(Group 4). Group 3 is merged to `main`. Not fixed here — it is outside the Group 4 branch — but
`build/build_database.py` now WARNs about it on every run (`check_ihc_checklist_renders_a_control`,
with a named, dated exemption for exactly these two node IDs) instead of staying silent.**

### What happens

`pf_mb_molecular_gate` and `mn_grade_assembly` are `ihc_checklist` nodes whose `resolution_logic[]`
keys off captured state variables (`when` clauses), not marker tokens. `induce_flow.py` induces
`branch_sequence.order` only from marker names in `positive`/`negative` arrays, so both nodes carry
`{"order": [], "intensity_markers": [], "rule_count": …}` — and neither carries a
`test_result_states` block. `app.js`'s `nodeControl()` routes every `ihc_checklist` with a
`branch_sequence` to `markerFlow()`, which asks one marker at a time strictly from
`branch_sequence.order` and never reads `marker_groups[]`. `dispatchNode()` separately prepends
`stateSelectors()`, which renders a control only where `test_result_states` exists. With both
absent, a clerk reaching either node sees the question, the hint and a bare Continue button, and
nothing to tap to answer it — the exact defect `hn_ihc_checklist`/`sn_ihc_checklist` shipped with on
the Group 4 branch, fixed there by giving each a `test_result_states` array (one block per status
variable its rules key off, matching `op_ihc_cd99`'s own pattern).

| Node | `resolution_logic[].when` variables | `branch_sequence.order` | `test_result_states` | Rendered control |
|---|---|---|---|---|
| `pf_mb_molecular_gate` | (captured molecular/pathway variables) | **empty** (7 rules) | **none** | **nothing** |
| `mn_grade_assembly` | (captured grade-criterion variables) | **empty** (33 rules) | **none** | **nothing** |

### What it costs

A clerk reaching either node cannot answer it and falls through to that node's fallback (or throws,
depending on what `nos_fallback`/`next_node` is declared) without ever recording the finding the
node exists to ask about — the same "green build, broken seam" failure mode as §12 above, on a
different node type.

### Why the build did not catch it

`induce_flow.py` proves every rule in `resolution_logic[]` has a *witness* — an answer vector that
fires it, checked in the abstract against the rule logic. A `when`-keyed rule keying off a captured
variable has a witness whether or not anything in the UI can ever set that variable, so this passed
clean. `check_flow_charts()` in `build/build_database.py` (ruling 13) already special-cases an empty
`branch_sequence.order` as legitimate whenever a node's rules read no marker tokens, on the theory
that `test_result_states` selectors are the flow chart in that case — but until 18 September 2026 it
never actually checked that a `test_result_states` block existed. Both checks validate the RULE
LOGIC; neither looked at whether the renderer that logic depends on has anything to show. Found only
by reading `app.js`'s `nodeControl()`/`markerFlow()` directly while fixing the same defect in Group 4.

### To close

Give `pf_mb_molecular_gate` and `mn_grade_assembly` a `test_result_states` block for each status
variable their `resolution_logic[]` keys off — the same fix applied to `hn_ihc_checklist` and
`sn_ihc_checklist` on the Group 4 branch (see `data/database/group_04_dt.json` for the worked
pattern: one block per variable, closed vocabulary, `not_done`/`not_available`/`not_assessable`
never collapsed onto `negative` where a branch treats a negative result as diagnostic). Both nodes
are `ihc_checklist` with far more rules than Group 4's two (7 and 33 respectively), so read each
node's full `resolution_logic[]` before authoring the states — do not assume the Group 4 shape maps
directly. Once fixed, delete both node IDs from `GROUP3_UNANSWERABLE_IHC_EXEMPTION` in
`build/build_database.py`; the exemption's own collapse assertion FAILs the build and names whichever
one is still listed if this is forgotten.

### How it was found

Found while fixing `hn_ihc_checklist`/`sn_ihc_checklist` on the Group 4 branch: the same
`branch_sequence.order`-empty-and-no-`test_result_states` shape was searched for across every
group's `ihc_checklist` nodes (`data/database/group_0{1,2,3,4}_dt.json`), turning up exactly these
two Group 3 nodes and no others in Groups 1, 2 or 4.

---

## 14. ⚠️ Three router dual-group rules still carry the stale CNS topography scope

**Found 18 September 2026 during the Group 4 build, extending the `9501-9504` rule. Not fixed
here — these are Group III/VIII/IX rules and the Group 4 branch was scoped to its own.**

`docs/TODO.md` §10.2 above records that the `9501-9504` rule carried a note reading *"Extend
both files together when Group III is authored"* and was extended in this build. **Three other
rules in `data/shared/presentation_router.json` carry the identical note, verbatim, and were
not extended.** `9260` is a separate defect and is already recorded at §10.1; it is not
repeated here.

### What happens

Each of the three matches only the NOS-level CNS codes `C70.9`, `C71.9` and `C72.9`, and each
carries the same `cns_topography_scope_note`: *"Uses NOS-level CNS topography codes
(C70.9/C71.9/C72.9) because topography_codes.json does not yet enumerate finer CNS subsites --
that granularity belongs to Group III's own build (not yet started). Extend both files together
when Group III is authored."* **Group III was authored 16 September 2026, and
`topography_codes.json` now enumerates all 21 codes in `C70.0`–`C72.9`.** The premise of the
note is false and the note says so on its face.

| Rule | Codes | CNS branch result | Default when the CNS branch misses | What ICCC-2017 actually says |
|---|---|---|---|---|
| `9473` | `9473` | Group 3, `IIIc2` — *"Intracranial."* | **Group 9**, *"Peripheral / soft tissue PNET."* | range 29 — `9473`, sites **`000-809`**, behaviour `0-1,3` → `IIIc2`. **The only range carrying `9473` at all.** Group III at *every* site |
| `8963` | `8963` | Group 3 — *"Via 9508 (ATRT)."* | **Group 9**, `IXd3` | ranges 48 (`649` → `VIa2`), 54 (`220,221` → `VIIa2`), 82 (`000-218,239-639,659-699,739-768,809` → `IXd3`). **`IXd3`'s site list excludes `700-729` entirely** |
| `8000-8005` | `8000`–`8005` | Group 3, `IIIf` (adds `C75.1`, `C75.2`, `C75.3`) | **Group 12** | range 42 — `8000-8005`, sites **`700-729,751-753`**, behaviour `0-1,3` → `IIIf`. `XIIb` (range 143) excludes both those blocks |

### What it costs

A case at a **specific** CNS subsite falls through the CNS branch to the default, and the
default is a different group.

1. `9473/3 CNS embryonal tumour, NOS` at, say, `C71.6 Cerebellum` routes to **Group IX (soft
   tissue sarcomas)** rather than Group III. `9473` is the CNS primitive neuroectodermal
   tumour stem — build contract §6 ruling D4 records that `Primitive neuroectodermal tumor,
   NOS` and `PNET, NOS` sit on `9473/3` and belong to Group III, while the *peripheral*
   wordings are `9364`. A cerebellar `9473` reaching Group IX is the exact confusion D4 exists
   to prevent, arriving by a different route.

   **And this rule is wrong more broadly than the stale scope note accounts for.** Verified
   against `ICCC-2017.sqlite` `code_ranges` on 18 September 2026: **range 29 is the only range
   in the whole table carrying `9473`**, it takes sites `000-809`, and it resolves to `IIIc2`.
   ICCC-2017 gives `9473` to Group III at **every** site. So the rule's default — *"Peripheral
   / soft tissue PNET"* → Group 9 — has no basis in ICCC-2017 at any topography, not merely at
   unenumerated CNS subsites. Extending `topography_in` would fix the CNS cases and leave a
   genuinely peripheral `9473` still routing to Group IX. The honest fix is probably that
   `9473` is not topography-dependent at all, but that is a Group III/IX decision, not one this
   entry should make.
2. `8963/3 Rhabdoid tumour, NOS` at a specific CNS subsite routes to **Group IX** rather than
   Group III, where it should reach `9508/3 Atypical teratoid/rhabdoid tumour` (range 31,
   `9508`, sites `000-809`, → `IIIc4`). The router's own note, *"Via 9508 (ATRT)"*, states that
   intent correctly. `IXd3`'s ICCC-2017 site list (range 82) **excludes `700-729`**, so the
   default is not merely a less specific answer at a CNS subsite — it names a group ICCC-2017
   does not admit there at all. Group III's clinical warning on atypical teratoid/rhabdoid
   tumour (`docs/clinical-warnings.md`, Group III table) turns on SMARCB1 (INI1) loss and
   rhabdoid tumour predisposition syndrome, none of which the Group IX tree asks about.
3. `8000/3 Neoplasm, malignant, NOS` at a specific CNS subsite routes to **Group XII** rather
   than Group III `IIIf` (unspecified intracranial and intraspinal neoplasms). Same shape as
   the last: `XIIb`'s site list (range 143) excludes `700-729` and `751-753`, so Group XII is
   not an admissible answer there. Note that this rule's CNS branch already reaches beyond
   `C70`–`C72` — it lists `C75.1`, `C75.2` and `C75.3`, exactly matching range 42's
   `700-729,751-753` — so the omission is of subsite granularity, not of the whole idea, and
   those three codes must survive the fix.

Group 4's own exposure is nil: `op_document_inventory`'s first option gates on a
`C70.0`–`C72.9` topography and refers to Group III before any code is emitted, and its
`coding_note` states in terms that *"the router's own dual_group_rule for this must not be
relied on as the only safeguard."* The three rules above have no such second gate.

### Why the build did not catch it

Nothing checks a `dual_group_rule`'s topography list against `topography_codes.json`. The
router check that runs (`check_router_integrity`, `checks routing narrows`) proves every
candidate list is a non-empty list of real groups and every crosswalk code resolves — it never
asks whether a rule's `topography_in` covers the range the rule's own `label` implies. The
`9501-9504` rule was extended in this build only because the Group 4 build contract §2.5 named
it explicitly; the three siblings were never named, so nothing looked at them.

### To close

Extend each rule's `topography_in` to all 21 codes in `C70.0`–`C72.9` that
`topography_codes.json` enumerates — the same edit already applied to `9501-9504` — and delete
the obsolete `cns_topography_scope_note` from each. Then write the check that would have found
all four at once: **a `dual_group_rule` branch whose `topography_in` contains any of `C70.9`,
`C71.9` or `C72.9` must contain all 21**, or declare why not. `8000-8005` additionally keeps
`C75.1`–`C75.3`, which are not part of that range and must not be dropped. The ICCC-2017
ranges are already confirmed in the table above, so no re-derivation is needed — but `9473`
needs the separate decision named under "What it costs" item 1 before its rule is touched,
because extending its topography list alone would leave the larger defect in place.

### How it was found

Extending the `9501-9504` rule for build contract §2.5 meant reading the rule's scope note;
the note's wording was distinctive enough to grep for, and the grep returned four rules
carrying it, not one. Each was then checked against `ICCC-2017.sqlite` directly rather than by
analogy with `9501`–`9504`, which is what turned up the wider `9473` defect.

---

## 15. `C32.x`, `C77.0` and `C10.x` are missing from `topography_codes.json`

**Found 18 September 2026 during the Group 4 build. Not fixed here: the build contract's own
rule is that a topography code is added with a `redcap_code` read from the REDCap file and
never invented, and adding a site the Group 4 trees do not yet claim is a routing change, not
a documentation one.**

### What happens

Build contract §5's tree-architecture table assigns `g4_head_neck_paraganglia` six topography
groups: `C75.4`, `C75.5`, `C30.1`, **`C10.x`, `C32.x` and `C77.0`**. The first three exist in
`data/shared/topography_codes.json`; the last three do not. The file enumerates 87 codes after
this build's 19 additions, and none of them is a larynx, oropharynx or head-and-neck lymph node
code. `C77.9 Lymph node, NOS` is present; `C77.0` is not.

The build reported this rather than inventing it. `presentation_router.json`'s
`groups["4"].tree_routing._comment` says so in the file itself: *"NOT yet routable: the build
contract's own §5 architecture table names C10.x (oropharynx), C32.x (larynx) and C77.0 (lymph
nodes of head/face/neck) as g4_head_neck_paraganglia topography, but none of the three exists
in topography_codes.json yet, so none is included below -- reported, not invented."*

### What it costs

Three presentations cannot be routed to the head and neck paraganglioma tree:

1. **Laryngeal paraganglioma** (`C32.x`). ICD-O-3.2 carries `Laryngeal paraganglioma` as a
   Related term on `8693/3 Extra-adrenal paraganglioma, NOS`, so the code exists and the entity
   is named in Layer 1. Build contract §5 lists laryngeal paraganglioma among the head and neck
   tree's dominant differentials by name.
2. **Vagal paraganglioma presenting in the neck** and any paraganglioma whose recorded
   topography is a head or neck lymph node (`C77.0`).
3. **Oropharyngeal sites** (`C10.x`).

A Group IV case at any of these sites has no `topography_codes.json` row, so `narrowBySite()`
has no candidate list to intersect and the case cannot reach `g4_head_neck_paraganglia` through
the router at all. It is not lost — `g4_other_peripheral` is the declared catch-all and
`op_paraganglioma_uncovered` exists for exactly this, emitting `8680/3 Paraganglioma, NOS` at
the family level. **The cost is a less specific code**: `8693/3 Extra-adrenal paraganglioma,
NOS` rather than `8680/3`, and no site-resolution step.

### Why the build did not catch it

It did catch it — `check_group4_topography_map` (rule 5) proves the map is total and disjoint
over **Group IV's own candidate topography codes**, which is the set `topography_codes.json`
declares. A code absent from that file is absent from the universe the check sweeps, so a
missing site is invisible to a totality check by construction. The check can prove every
declared code routes; it cannot prove every code the group *should* declare is declared. That
gap is what this entry is.

### To close

Add the three blocks to `topography_lookup` with `redcap_code` read from `ICD coding/RedCap
Options/Topography Redcap.md`. **All the values exist there and none needs inventing** —
verified 18 September 2026: `320` Glottis, `321` Supraglottis, `322` Subglottis, `323`
Laryngeal cartilage, `328` Overlapping lesion of larynx, `329` Larynx, NOS; `770` Lymph nodes
of head, face and neck; `100` Vallecula through `109` Oropharynx, NOS. Then add the matching
`coarse_organ_crosswalk` rows — there is no larynx and no oropharynx row today, and the
existing `Lymph nodes` row carries `candidate_groups: [2]` and would need `4` added for
`C77.0`. Then extend `g4_head_neck_paraganglia`'s `topography[]` and the router's
`tree_routing` rule together, and re-run rule 5. Do **not** add `C77.0` to Group 4 without
deciding what it means: a paraganglioma recorded at a lymph node is more often a metastasis
than a primary, and that is a registrar question, not a routing one.

### How it was found

Sweeping all 34 topography codes the four Group 4 trees claim against the three archetypes that
can reach the group — the same sweep that found the `C48.2` defect fixed in commit `10ca4fa` —
and then reading build contract §5's architecture table back against the file.

---

## 16. ❓ FOR THE REGISTRAR — ruling D6's CD99 gate was applied wider than D6 names

**Open question, recorded 18 September 2026. Not resolved by the build, and not to be resolved
by a build task.**

### What happens

Ruling D6 (build contract §6) reads: *"'Peripheral neuroepithelioma' goes to `9503`, and the
branch asks what the IHC shows."* It names **one** phrase — *peripheral neuroepithelioma* — and
rules that because that exact phrase appears nowhere in ICD-O-3.2, the destination is decided by
the CD99 / PHOX2B / synaptophysin panel already on file rather than by the report's wording.

As built, `op_clinical_alias`'s second option is labelled *"Neuroepithelioma, NOS",
"Neuroepithelioma", or "peripheral neuroepithelioma"* and routes **all three** to `op_ihc_cd99`.
So a report whose diagnostic line reads plainly `Neuroepithelioma, NOS` — the exact ICD-O-3.2
Preferred term on `9503/3`, unambiguous in Layer 1, and the subject of alias-instruction entry
29, which D4 explicitly leaves standing — is also sent through the Ewing-family gate, and a
CD99-positive / PHOX2B-negative / synaptophysin-negative panel refers it out of Group IV to
`9364/3 Ewing sarcoma`.

The build knew it was doing this and wrote the reason down in `op_clinical_alias`'s own
`coding_note`: *"entry 29 (Neuroepithelioma alone, to 9503) stands, but every case in this
family is still routed through the CD99/PHOX2B/synaptophysin check (`op_ihc_cd99`) rather than
trusting the word, because that is the evidence-not-wording standard D6 sets and there is no
reason to apply it selectively."* That is a defensible reading. **It is not what D6 says**, and
the difference decides which group a case is counted in.

### What it costs

Nothing today, because no case has been coded. Going forward it is a directional bias of
unknown size: every bare `Neuroepithelioma, NOS` with an Ewing-family immunophenotype leaves
Group IV for Group VIII or IX. If the registrar's intent was that Layer 1's own Preferred term
be honoured when the report uses it, Group IV under-counts and Groups VIII/IX over-count, and
nothing in the record will say why.

Note which way the asymmetry runs. The gate can only move a case **out** of Group IV; it can
never move one in. So a wrong answer here is not neutral.

### Why the build did not settle it

It is not a build question. The evidence is not in dispute — ICD-O-3.2 carries
`9503/3 Neuroepithelioma, NOS` as its only term on the stem, in both the 2019 draft and the
9 October 2020 final, and carries no PNET synonym there; the phrase *peripheral
neuroepithelioma* appears nowhere in the workbook. What is in dispute is how far a ruling
extends beyond the words it uses, and build contract §6 is explicit that **a build task that
finds a ruling inconvenient escalates; it does not reinterpret.** Applying D6 more widely than
its text is a reinterpretation, however reasonable.

### To close

The registrar answers one question: **does the CD99 gate apply to a report that says plainly
`Neuroepithelioma, NOS`, with no "peripheral", or only to the peripheral phrase?**

- **If only the peripheral phrase:** split `op_clinical_alias`'s second option in two. Bare
  `Neuroepithelioma` / `Neuroepithelioma, NOS` resolves directly to `9503/3` at basis 7; only
  *peripheral neuroepithelioma* goes to `op_ihc_cd99`. One option, one destination, no engine
  change.
- **If the gate applies to both:** the data is already correct and D6's text should be amended
  in the contract to say so, so that the next reader is not left reconciling the two.

Either way the answer belongs in `memory/registrar-rulings.md`, because Groups VIII and IX will
meet the other side of it.

### How it was found

Reading `op_clinical_alias`'s option labels against ruling D6's text word for word while
writing this build's documentation.

---

## 17. ❓ FOR THE REGISTRAR — the head and neck and sinonasal panels have no NEGATIVE button

**Open question, recorded 18 September 2026. A real gap in the two trees, and it cannot be
closed by copying the closed vocabulary onto the variables — see "To close".**

### What happens

`hn_ihc_checklist` and `sn_ihc_checklist` each declare three `test_result_states` variables.
Two of the three offer exactly one state:

| Node | Variable | Declared states |
|---|---|---|
| `hn_ihc_checklist` | `keratin_status` | `positive` · `negative` · `not_done` · `not_available` · `not_assessable` |
| `hn_ihc_checklist` | `general_ne_markers_status` | **`positive` only** |
| `hn_ihc_checklist` | `architecture_status` | **`positive` only** |
| `sn_ihc_checklist` | `pankeratin_status` | `positive` · `negative` · `not_done` · `not_available` · `not_assessable` |
| `sn_ihc_checklist` | `general_ne_markers_status` | **`positive` only** |
| `sn_ihc_checklist` | `architecture_status` | **`positive` only** |

`general_ne_markers_status` covers INSM1, synaptophysin and chromogranin; `architecture_status`
covers the zellballen / sustentacular pattern (SOX10, S100) in the head and neck tree and the
S100/SOX10 sustentacular network in the sinonasal tree.

**A clerk whose neuroendocrine panel came back negative has no button for it.** The only
available action is to leave the line blank, which fails the `when` clause that requires
`positive`, drops to the keratin-negative rule, and emits `8680/3 Paraganglioma, NOS` or
`9522/3 Olfactory neuroblastoma` at basis 7 with a `reason` that says the confirmatory panel
*"was either not completed or the result is equivocal."*

**A tested-and-negative panel is neither of those things.**

### What it costs

It conflates *not tested* with *tested and negative* — the exact distinction the keratin line
immediately above it is careful to preserve, at length, in five separate branches, for the
stated reason that *"an unread keratin is not a negative one."* The two variables sit in the
same node, under the same question, and do not make the distinction at all.

And the direction is wrong. A tumour with **negative** general neuroendocrine markers is
evidence **against** paraganglioma and against olfactory neuroblastoma; the case still resolves
to the tree's own family code, with a reason implying the workup is merely incomplete. That is a
case looking better evidenced than it is, on a screen a clerk reads — the class of defect this
project treats as the first thing to test for.

Scale, stated honestly: both codes are the trees' NOS-level family carriers, reached by several
other routes, so this does not silently create a diagnosis out of nothing. It emits a plausible
family code where the honest output is *this does not look like the tree's entity*.

### Why the build did not catch it

`check_ihc_checklist_renders_a_control`, added in this build (§13 above), asks whether a node
renders **any** control. Both nodes now do — the keratin line alone satisfies it. Nothing asks
whether the control offered covers the answers a clerk can actually have. `check_test_result_
states` (ruling 11) asks the opposite question: every **declared** state must be consumed by a
`when` clause. A one-state vocabulary passes both trivially — the single state is rendered, and
it is consumed.

### To close

**Do not simply copy the five-state closed vocabulary onto the two variables.** The
pre-existing `check_declared_states_consumed` (ruling 11) FAILs the build on any declared state
that no `when` clause consumes, so adding `negative`, `not_done`, `not_available` and
`not_assessable` to either variable FAILs immediately unless a branch is written for each, in
both nodes. That is eight new states and, at minimum, a rule per state per node.

The work, once the registrar has ruled on the substance:

1. Decide what a **negative** general neuroendocrine panel means in each tree. In the head and
   neck tree a keratin-negative, neuroendocrine-marker-negative tumour is probably not a
   paraganglioma at all, and the honest destination may be a referral rather than `8680/3`. In
   the sinonasal tree the same logic points away from olfactory neuroblastoma. **Neither is a
   coding-mechanics question, and neither is answered by any paper held in `Group 4 Papers/` —
   Mete 2022 and Rooper 2023 both state the positive panel and are silent on what a fully
   negative one implies.**
2. Then extend both vocabularies and write the branches, keeping `not_done` /
   `not_available` / `not_assessable` distinct from `negative` exactly as the keratin line does.
3. Then re-run `induce_flow.py` and confirm `check_declared_states_consumed` and
   `check_flow_charts` both pass.

A validator rule worth adding at the same time: **a `test_result_states` block declaring a
single state is a build WARN**, naming the node and the variable. One state is a legitimate
shape only when the variable genuinely has one possible answer, which is rare enough to be
worth writing down each time.

### How it was found

Reading `hn_ihc_checklist`'s and `sn_ihc_checklist`'s `test_result_states` blocks against their
own `marker_groups[]` while documenting the fix recorded in §13 — the fix that gave both nodes a
control in the first place established that `keratin_status` needed the full vocabulary and did
not ask the same question of the other two variables.

---

## 18. ❓ FOR THE REGISTRAR — a CNS neuroblastoma cannot reach Group IVa, and ICCC-3 puts it there

**Found 18 September 2026 while checking the alias agent's escalation during the Group 4 build.
Verified against Layer 1 directly, not inferred. Three parts, in three different files, one of
them in Group 3, which is already merged to `main`. Not fixed here. It needs a registrar ruling
on all three parts together — see "To close".**

### What Layer 1 says

**ICD-O-3.2** (`ICD coding/ICD-O-3.2/icdo32.sqlite`, table `icd_o_3_2_morphology`,
`code4 = '9500'`):

```
9500/3  Preferred  Neuroblastoma, NOS
9500/3  Synonym    Central neuroblastoma      (C71._)
9500/3  Synonym    CNS neuroblastoma
9500/3  Synonym    Sympathicoblastoma         [obs]
```

and separately `9490/3  Related  CNS ganglioneuroblastoma`. **ICD-O-3.2 itself puts CNS
neuroblastoma on `9500/3`**, and attaches an explicit `(C71._)` site reference to the *Central
neuroblastoma* synonym — the code is not merely tolerated at a brain site, the workbook names
one.

**ICCC-2017** (`ICCC-2017.sqlite`, table `code_ranges`). Three rows decide this:

| range | histology | sites | behaviour | group |
|---|---|---|---|---|
| 43 | `9490,9500` | **`000-809`** | `3` | 32 = **IVa**, *Neuroblastoma and ganglioneuroblastoma* |
| 45 | `9501-9504` | `000-699,739-768,809` | `3` | 33 = IVb, *Other peripheral nervous cell tumors* |
| 30 | `9501-9504` | `700-729` | `0-1,3` | 21 = IIIc3, *Medulloepithelioma* |

**The site split applies to `9501`–`9504` only.** Range 43 is the only range in the table
carrying `9490` or `9500` at all, it takes sites `000-809`, and it resolves to **IVa**. So
`9490` and `9500` are Group IVa at **every** site, the central nervous system included, and
Group III never claims either. Build contract §0.6 says this in terms: *"There is no conflict
to resolve; there is a routing note to write, because it reads wrong."*

### What happens

Three things, each independently sufficient to stop a CNS neuroblastoma reaching Group IVa.

**1. `data/shared/topography_codes.json` gives all 21 CNS codes `candidate_groups: [3]`.**
`C70.0`, `C70.1`, `C70.9`, `C71.0`–`C71.9`, `C72.0`–`C72.5`, `C72.8`, `C72.9` — every one
offers Group 3 alone. `narrowBySite()` intersects the site's candidate list with the
archetype's, and Group 4 is not in the site's list, so **the case cannot reach Group IV by site
routing at any CNS topography.** This is the same mechanism as the `C48.2` defect fixed in
commit `10ca4fa`, at 21 codes instead of one.

**2. `op_document_inventory` option 0 refers every CNS topography out, unconditionally.** The
option's `reason` is correct and carefully scoped: *"ICCC-3 gives medulloepithelioma, teratoid
medulloepithelioma, neuroepithelioma and spongioneuroblastoma to Group III (IIIc3) across the
whole of C70.0-C72.9, and to Group IV only outside that range."* That is `9501`–`9504`, exactly
right. **The `label` carries no such scope:** *"The topography recorded for this tumour is a
meningeal, brain, spinal cord or other central-nervous-system site coded C70.0 through C72.9"*
→ `refer_group: 3`. The label is what the clerk reads and acts on. A `9500/3` CNS neuroblastoma
that somehow reached this step is referred out of the group ICCC-2017 assigns it to, by a rule
written for four other codes. The node's `hint` repeats the unscoped form: *"If the topography
is … C70.0-C72.9, stop here and use the first option below."*

**3. `group_03_dt.json` codes `CNS neuroblastoma, FOXR2-activated` as `9473/3` and emits `9500`
nowhere** — the string `9500` does not appear in the file. **This part may well be deliberate,
and this entry does not assert that it is wrong.** ICD-O-3.2 was finalised 9 October 2020 and
*WHO Classification of Tumours of the Central Nervous System*, 5th edition followed in 2021, so
ICD-O-3.2 carries no FOXR2 entity anywhere (verified: `term LIKE '%FOXR2%'` returns zero rows),
and Group 3's own data says so — it records the entity with
`"code_status": "no_code"` against `9473/3`, whose ICD-O-3.2 Preferred term is `CNS embryonal
tumor, NOS` and which the Group 3 build designates the live NOS home for the whole new CNS
embryonal family. That is a considered position, written down with its reasoning.

It is also not obviously the same thing as ICD-O-3.2's `9500/3` synonym. *CNS neuroblastoma,
FOXR2-activated* is a molecularly defined 2021 entity; *CNS neuroblastoma* as a `9500/3`
synonym predates it and is defined morphologically. Whether a FOXR2-negative or untested CNS
neuroblastoma is the `9500/3` synonym, or is `9473/3`, is exactly the question nobody has
answered.

### What it costs

**A paediatric CNS neuroblastoma is recorded in ICCC-3 Group III when ICCC-3 puts it in Group
IVa.** That moves the case between two published incidence groups — *III CNS and miscellaneous
intracranial and intraspinal neoplasms* and *IVa Neuroblastoma and ganglioneuroblastoma* —
which are reported separately, compared internationally, and used as denominators. It is not a
less specific code; it is a different count, and both counts are wrong by one in opposite
directions.

The same reasoning applies to `9490/3 Ganglioneuroblastoma` at a CNS site, which ICD-O-3.2
carries as `CNS ganglioneuroblastoma` (a Related term) and range 43 likewise assigns to IVa.

A second, smaller cost, already paid: **the alias agent declined to author the `CNS
neuroblastoma` and `Central neuroblastoma` aliases for Group 4 because of part 2**, on the
ground that the alias would resolve into a tree that immediately refers the case out. That is
the right call — an alias that routes to a referral is worse than no alias, because it looks
like the question was answered. Two ICD-O-3.2 synonyms of a Group IV code are therefore
unsearchable, and will stay unsearchable until this is ruled on.

### Why the build did not catch it

Each check was correct about the thing it was scoped to.

- `check_group4_topography_map` (rule 5) sweeps **Group IV's own candidate topography codes**,
  sourced from `candidate_groups` in `topography_codes.json`. The CNS codes declare `[3]`, so
  they are not in Group IV's universe, so the totality sweep never sees them. The check proves
  every declared code routes to exactly one tree; it cannot prove the declaration is right.
  This is the same blind spot §15 records for `C32.x`/`C77.0`/`C10.x`, at higher stakes.
- The same rule's other half — *"no tree declaring `C70.0`–`C72.9` emits `9501`–`9504`"* — is
  the `9501`–`9504` half of build contract §0.6, and it passes. Nothing asks the converse
  question, whether `9490` and `9500` are **reachable** at a CNS site, because no check is
  framed in terms of reachability by site.
- Nothing compares an option's `label` against its own `reason`. `op_document_inventory`
  option 0 is internally inconsistent — a correctly scoped reason under an unscoped label — and
  no validator reads the two together. `check_no_internal_identifier_leaks` scans clerk-facing
  prose for identifier leaks, not for scope drift against the branch's own justification.
- Group 3's `9500`-absence is invisible from Group 4: no check crosses two group files to ask
  whether a code one group claims is being emitted by another.

Build contract §0.6 identified the substance of this on 16 September 2026 and called for *"a
routing note to write"*. A note was written, and it is exactly right — but it is in **`9500`'s
`coding_note`**, under the heading *CNS NOTE*: *"ICCC-3 places this code in Group IVa at every
site, including the CNS, and Group III does not claim it. This reads wrong to a reviewer who
expects a CNS-sited tumour to route to Group III; it is not an error, it is how ICCC-3 states
the group. Do not 'fix' it by adding a CNS carve-out."* `9500`'s own
`topography_routing_note` field is `null`, and so is `9490`'s.

`coding_note` is author-facing and is never displayed (memory
`uccf-lookup-tool-clerk-facing-text`). **A note in a field nobody reads at runtime does not
change `candidate_groups` and does not make the case routable.** The build wrote down the right
answer, in the one place that could not act on it. That is the gap between what §0.6 asked for
and what the build delivered, and it is worth noting that the note's closing instruction — *do
not add a CNS carve-out* — is correct and points the opposite way from what parts 1 and 2
actually do.

### To close

**This needs a registrar ruling on all three parts together, and no part should be changed
alone.** Part 1 changes routing for Group 3, which is already merged to `main`; changing it
without settling part 3 would make a CNS site offer Group 4 while Group 3's own tree still
codes the entity to `9473/3`, so the same case would resolve differently depending on which
tree the clerk was sent to. Changing part 2 alone would let a case into a tree the router
cannot deliver it to.

The three questions, as they should be put:

1. **Does this registry record a CNS neuroblastoma in ICCC-3 Group IVa, as ICCC-2017 range 43
   states?** If yes, the 21 CNS topography codes need `4` added to `candidate_groups`, and the
   `coarse_organ_crosswalk` row *Brain, meninges and central nervous system* with it. If no,
   the reason belongs in `memory/registrar-rulings.md`, because it overrides Layer 1 and the
   next builder will otherwise reopen it.
2. **Does `op_document_inventory` option 0's label need the `9501`–`9504` scope its own reason
   already carries?** This one is a defect on any answer to question 1 — the label and the
   reason contradict each other, and only the label is displayed. The minimal fix is to name
   the four codes in the label, matching the reason.
3. **Is `9473/3` the right home for `CNS neuroblastoma, FOXR2-activated`, given that ICD-O-3.2
   carries `CNS neuroblastoma` as a `9500/3` synonym?** State what each source says: ICD-O-3.2
   has no FOXR2 entity and puts CNS neuroblastoma on `9500/3`; WHO CNS5 (2021) defines the
   FOXR2 entity and postdates ICD-O-3.2; ICCC-2017 range 43 puts `9500` in IVa at every site
   and range 29 puts `9473` in IIIc2 at every site. **The reconciliation is the registrar's.**
   Whichever way it goes, a FOXR2-negative or untested CNS neuroblastoma needs a destination
   too, and that case is not covered by either file today.

Once ruled, the alias agent's two withheld aliases (`CNS neuroblastoma`, `Central
neuroblastoma`) can be authored against whichever code the ruling names, and a check is worth
adding: **a code ICCC-2017 admits at a topography must be reachable at that topography**,
derived from `code_ranges` rather than from `candidate_groups`, so the declaration is checked
against Layer 1 instead of being trusted as the universe.

### How it was found

The alias agent escalated rather than authoring `CNS neuroblastoma` and `Central neuroblastoma`
into `aliases_group_04.json`, having noticed that `op_document_inventory` would refer the case
straight out of the group. Checking that escalation meant querying `icdo32.sqlite` and
`ICCC-2017.sqlite` for what each actually says about `9500` at a CNS site, which turned up
parts 1 and 3 as well.

---

*Last updated 18 September 2026, on the Group 4 branch (`group-04-neuroblastoma`), with the
Group 4 build documentation (§14–§18). Previously 18 September 2026, on the Group 4 build.*
