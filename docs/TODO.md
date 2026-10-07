# Lookup tool — open items

Things found while building that are real and are not fixed. Each says what closing it takes.
Nothing here blocks the current build.

**Citation convention.** A claim names the paper and the page, not the series. Abbreviations
that have a full form are written out.

**Closed items are deleted, not archived here.** An item that has been settled or fixed leaves
this file; its record lives in the commit that closed it, in the group's build report, and for
the Group 3 obsolete terms in `docs/group_03_obsolete_terms.md`.

---

## 1. Layer 1 — REDCap side

### 1.1 `C71.0` Cerebrum is missing from the topography dropdown

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

### 1.2 `9476/3` has no REDCap option

The only Group III code with no `iii_morph` entry. Built under registrar ruling 3 of 4 September
2026. Detail, including the `iii_extended` / `iii_subgroup` formula change: `docs/codes-awaiting-redcap.md`.

### 1.3 Ligature damage in `Topography Redcap.md`

The sweep of 14 September 2026 concluded Group 3 was the only affected **morphology** option
file. `Topography Redcap.md` is a thirteenth file and was not swept: `so!` for *soft* (lines 30,
56, 278), `Le!` for *Left* (line 97), `"roat` for *Throat* (line 65). **None is in the CNS
block.** Documentation defect.

A fourth instance of the same `so!` corruption surfaced during the Group 5 build: line 696,
`So!` for *Soft* (`"So! tissue of orbit"` for *Soft tissue of orbit*, inside the C69.6 Orbit,
NOS parenthetical). Written correctly in `topography_codes.json`; the source file itself was
not touched — Group 5 build contract §7.1.

---

## 2. Schema gaps — three trees hit each of these independently

### 2.1 No marker answer means *loss* as distinct from *not done*

`markerOff()` returns true for an absent marker, an explicit `neg` and `nd` alike. A rule
written `negative: ["SMARCB1 (INI1)"] → 9508` fires for a laboratory that **never ran the
stain**.

Both embryonal trees found it independently and worked around it the same way: SMARCB1 (INI1),
BRG1/SMARCA4 and H3 K27me3 were moved off the marker grid into option-based capture nodes, each
offering an explicit *performed but uninterpretable* state. It works, but the three most
important stains in this group are now asked as evidence questions rather than as markers.

**To close:** a marker answer meaning *loss* (or *retained*), distinct from *not done*.

### 2.2 `refer_group` cannot say "code the primary at Stage 1"

One integer 1–12, and a metastasis's destination depends on a primary the tree has not captured.
Three trees hit this; all used `refer_group: 12` with the real instruction in `reason`.

**To close:** a fifth branch destination — `refer_stage: 1`, or a `recapture_site` terminal.

### 2.3 `provisional_pending` holds only one `resolving_test`

Group 3 Diagnostic Pathway Revision 2 §4.8 requires naming **both** isocitrate dehydrogenase
(IDH) mutation and 1p/19q co-deletion for an untested oligodendroglioma. The supratentorial tree
names one in the schema field and the second in a non-schema `additional_resolving_tests[]`.

### 2.4 "Methylation" is not in the closed diagnostic-test vocabulary

Resource level V is reached by DNA methylation profiling throughout this group, but the closed
set is `Referral only · Histology · Imaging · IHC · ISH · Flow cytometry · Cytogenetics/FISH ·
Molecular/PCR`. Trees use `Molecular/PCR`; the engine's `methylation_counts_as: 8` basis default
matches on the evidence-gate token instead.

### 2.5 `check_fallback_chains` keys the fallback graph by code alone

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

### 2.6 The resource-level gate's `family` vocabulary has no mesenchymal value

The gate's `family` vocabulary has ten values and **none is mesenchymal**, so the node declares
`unspecified`. The clerk-facing line therefore reads *"Resource level IV is required for the
**unspecified** family"* — honest, but clumsy. Adding `mesenchymal` would read better but changes a
closed list that Groups 1 and 2 also validate against. Left pending a ruling.

---

## 3. Behaviour

### 3.1 Six fallbacks raise behaviour

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

### 3.2 `9391/1` Sellar ependymoma is unreachable

107 of 108 entries are reachable. A sellar ependymoma arises at C75.1, which routes to
`g3_midline`, and that tree has no ependymal branch. Rare, but `terminal_reachable` exists to
catch exactly this.

---

## 4. Pre-existing, outside Group 3

### 4.1 All four Group 2 `prior_probability` blocks never render

`markerFlow()` asks one marker at a time and never renders marker groups, so it never renders
their priors. `nodeControl()` routes to `markerFlow` whenever a `branch_sequence` exists, which
`induce_flow.py` puts on every `ihc_checklist`. Only `markerGrid()` renders them, and it is now
unreachable in Groups 1 and 2.

Affected: `g2_hodgkin`, `g2_matureB`, `g2_nkt`, `g2cut_ebv_cutaneous` — every marker-group prior
Group 2 has. `check_prior_probability` passes them because it validates shape, not reachability.

---

## 5. Configuration — the site profile

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

## 6. Clinical rulings still owed

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

---

## 7. REDCap changes owed — every group, one place

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
| **III** | `topo_code` | — | — | `710, Cerebrum` | Open — §1.1 above | same |
| **IV** | `iv_morph` | **3** — picks 10, 12, 20 | **8** — picks 1, 4, 6, 9, 14, 16, 17, 19 | **0** | Ready to review, not applied | `ICD Look Up tool/Group 4 — Layer 1 Repair Package (REDCap iv_morph).md` |
| **IV** | `topo_code` | — | — | **0** | ✅ Nothing owed — every Group IV site is already in the dropdown | same, §7 |
| **VII** | `vii_morph` | **10** — picks 1, 2, 3, 39, 46, 47, 60, 83, 102, 103 (pick 2, `8975`, kept by ruling of 3 October 2026) | **27** | **8** — `8171`–`8175`, `8023`, `8054`, `8504/3` as picks 113–120 | Ready to review, not applied | `docs/group_07_layer1_repair.md` |
| **I, II** | — | — | — | `9715`, `9749`, `9819` | Open | `docs/codes-awaiting-redcap.md` |
| **I** | `i_morph` | **15** — picks on lines 28, 54, 55, 62, 68, 72, 88, 94, 95, 96, 98, 120–123 of the Group 1 option file, now that Group I's names are ICD-O-3.2 terms (§27). `9869` is a correctness fix, not a wording one: the option reads `t(13.3)(q21;q26.2)`, which is not valid cytogenetic notation; ICD-O-3.2 has `t(3;3)(q21;q26.2)`. `9980` and `9983` move off the FAB-era *Refractory anemia* wording to the WHO names. | **4** — lines 17, 25, 104, 105 (`9836`, `9826`, `9991`, `9992`). The tool no longer carries these; they were removed from Group I by registrar ruling of 6 October 2026, and ICD-O-3.2 carries no term for any of them. Retire in place, never delete — `i_morph` stores a pick number. | — | Open — not applied | §27 below, and `docs/group_01_icdo32_names.md` |
| **VI** | `vi_morph` | **8** label drifts (contract §2C) | — | **3** — `8023/3`, `8054/3`, `8482/3` | Ready to review, not applied | `docs/group_06_layer1_repair.md`; `docs/codes-awaiting-redcap.md` |
| **VIII** | `viii_morph` | **8** — picks 7, 8, 24, 35, 39, 66, 75, 98 | **3** — picks 18, 19 (wrong number `9211`) and **33** (`9260` Ewing sarcoma, a retired number now meaning aneurysmal bone cyst) | **2** — `9220/3` Chondrosarcoma, NOS; `9302/3` Ghost cell odontogenic carcinoma | Ready to review, not applied. 49 more picks sit below behaviour 3 and await the registrar | `docs/group_08_layer1_repair.md` |
| **IX** | `ix_morph` | **14** — `8825`, `9220`, `8832` (labels naming a benign or behaviour-1 lesion on a malignant code); `9364` to *Ewing sarcoma*; `8811`, `8963`, `9133`, `9187`, `8921` (synonym, not the preferred term); `9540`, `8851`, `9186`, `8804`, `8842` (missing qualifier) | **3** — `9260` (Ewing sarcoma, a retired number now meaning aneurysmal bone cyst), `9150` (deleted, moved to `8815`), `8833` (behaviour 1 only) | **4** — `8714/3`, `9045/3`, `9137/3`, `9542/3` | Ready to review, not applied. 57 more options sit below behaviour 3 and await the registrar (Group 9 registrar questions G1). `ix_morph` stores the code itself, not a pick number, so relabelling changes nothing a calculation reads | `docs/group_09_layer1_repair.md` |
| **IX** | `topo_code` | — | — | `444, Skin of scalp and neck` | Open — Group 9 registrar questions H2 | same, §7 |

### 7.1 Group IV — `iv_morph`, 11 of 26 options are invalid

**11 of the 26 `iv_morph` options carry a term the code does not have in ICD-O-3.2, or a
behaviour ICCC-3 Group IV does not admit.** `ICCC-3 declares behaviour `3`, and only `3`, for
every Group IV range` — that one fact drives six of the eleven.

This does **not** contradict `REDCap Registry/docs/data-dictionary/Group IV Verification.md`, which
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

### 7.2 Pre-flight before any of it is applied

Export `record_id`, `iv_morph`, `iv_code` and count records on picks **1, 4, 6, 9, 14, 16, 17,
19**. Picks 4, 6, 14 and 16 move to the NOS pick on the same code (5, 5, 13, 15) with no recode.
Picks 1, 17 and 19 are **benign tumours outside ICCC-3 Group IV** — out of scope, not miscoded,
and the registrar decides whether the record stays in the registry. Pick 9 is re-coded from the
report. If all eight return zero records the repair is label-and-formula only, which is likely:
the registry began operating in 2025 and Group IV is small.

---

## 9. CoGNET has no ICD-O code in any source

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

## 10. ⚠️ Group 3 defect — three `imaging_pathway` nodes throw at runtime

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

## 11. ⚠️ Group 3 defect — two `ihc_checklist` nodes render no way to answer them

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
node exists to ask about — the same "green build, broken seam" failure mode as §10 above, on a
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

## 12. ✅ CLOSED — router dual-group rules and the stale CNS topography scope

> **Closed 22 September 2026 on the Group VI branch (`group-06-renal`) for `8963` and
> `8000-8005`, the two rules Group VI owns, and for `9380` and `8158,8290`, which turned out to
> have a second and worse defect described below. `9473` remains open and is now the only open
> part of this item — it is exempt by name in `check_router_cns_topography_completeness()`, and
> that exemption FAILS the build if the rule is ever repaired without deleting the name.**
>
> **A fourth rule was in the list and a worse defect was underneath all of it.** Four branches —
> `9380` at `C72.3`, `8158,8290` at `C75.1`, `8963` at `C64.9` and the `8000-8005` branch added
> in the same commit — wrote `topography_equals`, a key `app.js`'s `branchMatches()` has never
> read. All four were **dead**: the branch never matched and every case fell to the rule's
> default. Two crossed an ICCC-3 group boundary — a pituitary tumour sited at the pituitary gland
> routed to **Group XI**, and a rhabdoid tumour of the kidney could never reach **Group VI**, the
> group that owns the code. So the stale CNS scope note was hiding a second, larger fault on the
> same objects.
>
> **Two checks were written, and the one this section proposed is the second of them.**
> `check_router_branch_when_vocabulary()` closes the branch `when` vocabulary against
> `branchMatches()` itself — it catches a branch that can never match.
> `check_router_cns_topography_completeness()` is the check proposed in "To close" below — it
> catches a branch that matches at the NOS level and misses every specific subsite, which is the
> worse of the two to find because it works in testing. Its trigger is the **NOS-level** codes and
> not any CNS code: a branch saying "the CNS" must name all of it, while `9380`'s single `C72.3`
> is saying something narrower and is left alone. Four negative controls on the first check and
> two on the second, all confirmed firing and restored.

> **`9473` closed 2 October 2026 on the Group 9 branch.** Group IX's half of the "Group III/IX
> decision" this item left open: ICCC-2017 range 29 is the only range carrying `9473`, at sites
> `000-809`, resolving to IIIc2, and ICD-O-3.2 codes the peripheral PNET wordings at `9364/3`. Group
> IX has no claim on `9473` at any site. The rule was removed, so `9473` is a single-group Group III
> code, and its name was deleted from `check_router_cns_topography_completeness()` in the same
> change; a stale-name clause cannot fire once the rule it names is gone (Group 9 build contract
> §3.12; `docs/group_09_negative_controls.md`).

**Found 18 September 2026 during the Group 4 build, extending the `9501-9504` rule. Fixed 22
September 2026 on the Group VI branch, except for `9473`.**

The `9501-9504` rule carried a note reading *"Extend both files together when Group III is
authored"* and was extended during the Group 4 build. **Three other
rules in `data/shared/presentation_router.json` carry the identical note, verbatim, and were
not extended.** `9260` was a separate defect (the former §8.1), closed on the Group VIII
branch on 2 October 2026 by re-keying the rule to `9364` and `9365`.

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

## 13. `C32.x`, `C77.0` and `C10.x` are missing from `topography_codes.json`

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

## 14. ❓ FOR THE REGISTRAR — ruling D6's CD99 gate was applied wider than D6 names

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

## 15. ❓ FOR THE REGISTRAR — the head and neck and sinonasal panels have no NEGATIVE button

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

`check_ihc_checklist_renders_a_control`, added in this build (§11 above), asks whether a node
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

## 16. ❓ FOR THE REGISTRAR — a CNS neuroblastoma cannot reach Group IVa, and ICCC-3 puts it there

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

## 17. ⚠️ Every field on an alias entry except `alias` and `also_known_as` is dead

**Found 22 September 2026 during the Group 5 build, reading `app.js` to settle whether an alias
entry's clerk-facing text renders. It does not. Nothing on any alias entry does.**

> ### ⚠️ RE-RATED 23 September 2026 — "mostly nothing today" is no longer true
>
> The assessment below was written when every alias mapped to a code, so a dead `notes` field cost
> only some helpful prose. **Group VI's alias file has sixteen entries that deliberately map to no
> code at all**, and their whole purpose is to say something to the clerk. All sixteen are silent.
>
> Confirmed in the browser, 23 September 2026: typing *hypernephroid* finds the alias and drops the
> clerk into `rn_document_inventory`, whose first question is about evidence tiers. The tree does
> not know a trap word was typed, and **none of the entry's `notes` reaches the screen** — including
> the sentence that exists precisely to stop the case going wrong: *"Do not select REDCap option
> 8311 for a case described only this way."*
>
> Two that matter most:
>
> | Typed | What the clerk is told | What they should be told |
> |---|---|---|
> | *hypernephroid* | nothing | the REDCap label for `8311` is an obsolete term for a different, borderline lesion; `8311/3` now carries seven molecularly defined carcinomas; if none is named, this is outside the group |
> | *oncocytoma* | nothing | renal oncocytoma is `8290/0`, benign; `8290/3` Oxyphilic adenocarcinoma is on the same stem and **is** in the Group VI dropdown, so picking `8290` registers a benign tumour as a carcinoma |
>
> A clerk who types *oncocytoma* now enters the Group VI tree and can walk it to a carcinoma
> terminal. The alias file knows better and cannot say so.
>
> This is no longer a tidiness item. Rendering an alias entry's `notes` — one line at the top of the
> node the alias routes into — would close it, and the data is already authored and validated.

### What happens

The search path is three steps and reads two values.

1. `searchAlias(q)` (app.js:380) matches the query against **`alias_index.json` only** — a generated
   map of `alias string -> [group numbers]`, built by `build_database.py` from each entry's `alias`
   field and nothing else.
2. `handleOption`'s `case 'alias'` (app.js:1990) does `state.group = hit.groups[0]` and calls
   `afterGroup()`. The tree is then picked from `presentation_router.json`.
3. `aliasesFor(code)` (app.js:1894) later renders the *"Also called"* line from `alias` and
   `also_known_as`.

So of the seventeen keys an alias entry carries, **`alias` and `also_known_as` are read and the
other fifteen are not**: `maps_to_morphology_codes`, `maps_to_iccc3_subgroup_id`, `full_form`,
`alias_type`, `origin_system`, `nci_concept_id`, `who_version_current`, `needs_ihc_tree`,
`ihc_tree_id`, `tree_entry_node`, `clinical_alert`, `notes`, `coding_note`, `refer_group`,
`refer_code`.

### What it costs

Mostly nothing today, and one thing that will bite.

- `ihc_tree_id` and `tree_entry_node` are validated by `check_alias_cross_references` and are
  **correct data that the engine ignores** — routing comes from the router's handoff instead. Two
  sources of truth for the same fact, one of them unread. The day they disagree, nothing notices.
- **`refer_group` on an alias does not refer.** `aliases_group_04.json`'s *Peripheral
  neuroectodermal tumor* entry carries `refer_group: [8, 9]` and `refer_code: "9364"`; Group 5's
  *Trilateral retinoblastoma* entry carries `refer_group: 3`. A clerk who reaches either by search
  is put into the entry's own group and sees no referral at all. The referral survives only because
  both trees also carry it as a branch destination, where it *is* rendered. Nobody should rely on
  that holding for the next group.
- **★ `state.group = hit.groups[0]` picks the lowest-numbered group with no disambiguation, and
  there are already 24 collisions — every one of them on a dual-group term.** Swept across all five
  alias files on 22 September 2026:

  | Groups | Colliding alias strings |
  |---|---|
  | **1 / 2** (21) | `adult t-cell leukemia/lymphoma` · `atl` · `atll` · `b lymphoblastic leukemia/lymphoma` · `b-cell chronic lymphocytic leukemia/small lymphocytic lymphoma` · `bcr-abl1-like b-all` · `burkitt cell leukemia` · `burkitt leukaemia` · `cll` · `fab l3` · `l3 all` · `leukaemic burkitt lymphoma` · `lgl leukaemia` · `mature b-cell all` · `non-hodgkin lymphoma` · `ph-like all` · `sll` · `small lymphocytic lymphoma` |
  | **3 / 4** (6) | `medulloepithelioma` · `medulloepithelioma, nos` · `teratoid medulloepithelioma` · `teratoid medulloepithelioma, nos` · `neuroepithelioma` · `spongioneuroblastoma` |

  **These are not incidental collisions. They are the dual-group families** — the B-lymphoblastic
  family, chronic lymphocytic leukaemia / small lymphocytic lymphoma, adult T-cell
  leukaemia/lymphoma and Burkitt, whose group turns on `primary_compartment`; and `9501`–`9504`,
  whose group turns on topography. They are precisely the terms for which the group is *undecided
  until a question is asked*, and the express lane answers it by taking the lower number.

  A clerk who types `CLL` is put in Group 1 without being asked whether the disease is marrow- or
  node-centred. A clerk who types `medulloepithelioma` is put in Group 3 — yet an intraocular
  medulloepithelioma of the ciliary body (C69.4) is an ICCC-3 **Group IV** tumour, which is why
  `topography_codes.json` now gives C69.4 candidate groups `[5, 4]` (Group 5 build contract §5.3,
  §7.1).

  Recovery is not guaranteed and is not designed. `group_01_dt.json` and `group_02_dt.json` do
  carry `primary_compartment` (32 and 23 occurrences), so a case that entered the wrong one of that
  pair may still be referred out by the tree it landed in. Nothing verifies that for the 3/4 pair,
  and nothing verifies it for any pair added by Groups 6–12. **The express lane's own comment says
  it "bypasses the clinical scaffold" — the scaffold is where the discriminator is asked.**

### To close

Three options, in increasing order of work, and this is a design decision rather than a bug fix:

1. **Document the fields as author-facing** and stop writing clerk-facing text into them. Cheapest,
   and honest. `notes` and `coding_note` are already author-facing by convention; the others would
   join them.
2. **Render what is already authored** — a referral entry that shows its `refer_group` and `reason`
   before entering a tree, and the `full_form` on the search result row.
3. **★ Ask when an alias is ambiguous**, instead of taking `groups[0]`. This is the one that is
   already costing something, on 24 terms. The router already owns the machinery: `discriminators`
   in `presentation_router.json` defines `primary_compartment` and `tumour_origin` with their
   questions, options and `narrows` maps, and `dual_group_rules` names which codes need which. An
   ambiguous alias hit should route into that same question rather than round down.

Two validator rules are worth having whichever option is taken:

- An alias string indexed to more than one group **is reported**, with the groups named. Today the
  count is 24 and nobody knew.
- An alias entry carrying `refer_group` while the corresponding group's tree carries no matching
  referral branch is a referral that exists only on paper.

### How it was found

The Group 5 alias author added a `reason` key to its trilateral-retinoblastoma entry — a key the
Group 4 schema does not have — and flagged it as a deliberate schema deviation rather than adding
it silently. Checking whether the deviation mattered meant tracing the field to the renderer, which
showed that neither `reason` nor the fourteen other fields reach one. Sweeping the five alias files
for collisions, to confirm the Group 5 author's "no collisions" claim (true for its own file), then
turned up the 24.

---

## 18. ⚠️ FOR THE REGISTRAR — 375 authored alias terms cannot be searched

**Found 22 September 2026, driving Group V in a browser. Measured across all five alias files.**

### What happens

`build_database.py` builds `alias_index.json` from each entry's **`alias`** field and nothing
else — one line, `index.setdefault(alias.strip(), set()).add(group)`. `app.js`'s `searchAlias()`
matches the query against that index alone. **`also_known_as` is never indexed.** It is read only
by `aliasesFor(code)`, which renders the *"Also called"* chips on a finished case — that is, it is
shown to a clerk only **after** they have already reached the code it would have helped them find.

Driven in the browser against the live tool:

| Typed | Result | Why |
|---|---|---|
| `leukocoria` | ✅ Group 5 | it is an `alias` |
| `buphthalmos` | ✅ Group 5 | it is an `alias` |
| `eye cancer` | ✅ Group 5 | it is an `alias` |
| `white pupil` | ❌ *"No match. Use guided entry."* | it was an `also_known_as` |
| `cat` (for cat's-eye reflex) | ❌ no match | `also_known_as` |
| `squint` | ❌ no match | `also_known_as` |
| `protruding` (protruding eye) | ❌ no match | `also_known_as` |

**All four now return Group 5** — see *What was fixed for Group 5* below. The table records the
state that was found.

### The scale

| Group | `alias` entries | `also_known_as` strings |
|---|---|---|
| 01 | 283 | 448 |
| 02 | 368 | 484 |
| 03 | 223 | 445 |
| 04 | 69 | 115 |
| 05 | 19 | 25 |

793 distinct `also_known_as` strings exist. **375 of them are not reachable by search at all** —
the rest coincide with some entry's primary `alias`. Roughly a third of every search term the alias
builds authored is inert.

| Group | still unsearchable |
|---|---|
| 01 | 69 |
| 02 | 121 |
| 03 | 168 |
| 04 | 21 |
| **05** | **0 — fixed, see below** |

### What it costs

The `also_known_as` field exists to hold *what a clerk might actually type*. That is the whole of
its job, and it does not do it. The cost is worst exactly where the registry needs it most: this is
a Ugandan paediatric registry where late presentation is normal and referrals arrive in lay
language. Group V's alias build was asked specifically to cover referral-letter vernacular, and it
did — `white pupil`, `white eye`, `cat's-eye reflex`, `squint`, `crossed eye`, `protruding eye`,
`bulging eye`. **Every one of those is unsearchable.** A clerk holding a letter that says
"white eye" is told there is no match and sent to guided entry.

### To close — and the reason this is the registrar's call and not a quiet fix

Indexing `also_known_as` is a small change to one loop in `build_database.py`. Measured before
proposing it: it would add **12 new cross-group collisions** to the 24 that already exist (§17).

```
b-cell lymphoblastic leukemia/lymphoma   [01, 02]   nhl                              [01, 02]
htlv-1 associated adult t-cell l/l       [01, 02]   pgl                              [02, 04]
iamp21                                   [01, 02]   precursor b lymphoblastic l/l    [01, 02]
lgll                                     [01, 02]   precursor t-cell lymphoblastic   [01, 02]
neuroepithelioma, nos                    [03, 04]   t-all                            [01, 02]
t-cell all                               [01, 02]   t-lgl leukemia                   [01, 02]
```

Every one lands in a family §17 already names, and §17's defect is that
`state.group = hit.groups[0]` resolves an ambiguous hit by **taking the lower group number without
asking the discriminator**. So indexing `also_known_as` on its own would make search much better
and make an existing silent-misroute defect fire more often — a net that nobody should decide
on a build branch.

**Recommended order:** fix §17 option 3 first (ask when an alias is ambiguous, reusing the
router's existing `discriminators` block), then index `also_known_as`. Doing both makes 395 terms
findable with no new silent misroute. Doing the second alone does not.

### What was fixed for Group 5, and why that route does not scale to the rest

**The registrar asked the obvious question — why not just put them in `alias`?** For Group 5 that
was exactly right, and it was done: **20 strings promoted to primary alias entries**, taking the
file from 19 entries to 39. `white pupil`, `white eye`, `cat's-eye reflex`, `squint`, `crossed
eye`, `protruding eye`, `bulging eye`, `eye tumor`, `intraocular mass` and eleven clinical variants
are now searchable, all verified in the browser. Group 5's unsearchable count is **0**.

Three things made it safe and correct **here**:

1. **The master instruction file already says so.** Sec. 2 defines `alias` as *"the primary search
   term… Separate entries for abbreviation vs full name vs eponym vs **local term**"*, and
   `alias_type: local` as *"registry-, setting- or region-specific terminology not in international
   databases"*. Referral-letter vernacular is a local term by that definition, so it belonged in
   `alias` from the start. This was an authoring miss, not a schema limitation.
2. **Zero new collisions.** Swept before promoting: not one of the 20 collides with any string in
   Groups I–IV.
3. **The display is unchanged.** `aliasesFor()` dedupes the *"Also called"* list
   case-insensitively, so the strings stay in `also_known_as` for provenance and nothing renders
   twice — verified: 28 chips, 0 duplicates.

**Why the remaining 375 are not the same job.** Group 5's were curated by hand: 11 of the 20 are
lay vernacular with `nci_concept_id: null`, authored for this registry's referral letters. The
other groups' `also_known_as` arrays are **machine-harvested from the NCI Thesaurus and EBI OLS
`synonyms` arrays** (master file Sec. 4E). Promoting 375 harvested synonyms into full entries would
duplicate `maps_to_morphology_codes`, `notes`, `coding_note` and `nci_concept_id` 375 times, with
nothing keeping the copies in step — and it would still add the 12 collisions, because those come
from the strings entering the index, not from the mechanism that puts them there.

So: **promote a curated local term; index a harvested synonym.** The one-loop index fix is still
the right answer for the other four groups, and it still wants §17 fixed first.

Not done on this branch for Groups I–IV: it changes search behaviour for four built groups, and
the Group 5 work neither needs it nor is the right place to prove it.

---

## 19. ✅ CLOSED — the engine gate runs inside the Python gate

> **Registrar's decision, 23 September 2026: add Node.js.** *"if certain dependencies are lacking,
> user must be warned, when the tool launches. I think there must be a verification layer, that
> checks for all necessary requirements for the tool to run before it loads."*
>
> Implemented as a **preflight** section that reports every missing requirement at once and stops
> before anything else runs, plus the engine gate as section E of the same command. Node.js is
> required and the gate is never skipped when it is absent. Four negative controls run and
> confirmed: Node.js off PATH, four requirements missing together, the engine script deleted, and a
> broken engine swapped in — that last one now fails `build_database.py` itself.
>
> **Carry this into the merge.** Against `main`'s `app.js` the gate finds 458 stranded flows in
> Group 2, 11 in Group 3 and 16 in Group 4, with matching screen-versus-record failures. The gate
> and the `app.js` fix must merge together; wiring in the gate alone turns `main` red for three
> groups on the first run.

**Raised 22 September 2026 with `build/check_engine_flow.mjs`. Closed 23 September 2026. The
reasoning is kept below because the trade it records is the reason the preflight is shaped the way
it is.**

There are now two gates and they test different layers:

```bash
python3 build/build_database.py      # the DATA
node build/check_engine_flow.mjs     # the ENGINE
```

`check_engine_flow.mjs` is JavaScript because `app.js` is: testing the engine means loading and
running it, and only a JavaScript runtime can. That means it needs **Node.js installed**, and
`build_database.py` needs nothing but Python and SQLite.

**The trade, stated plainly.** Wiring the engine gate into `build_database.py` gives one command
that cannot be forgotten, and costs the Python gate its dependency-free property — a machine
without Node.js could no longer run the build at all. Leaving them separate keeps that property and
costs the guarantee: someone runs the Python gate, reads `BUILD PASSED`, and pushes. **That is
exactly how both engine defects survived**, with every data check green while the tool told a clerk
one code and recorded another.

**The trap, whichever way it goes.** If it is wired in it must **FAIL** when Node.js is absent,
never skip. A gate that silently skips a missing tool returns a green build that checked nothing,
which is worse than either option above. The check already behaves correctly on its own: it exits
1 when its target file is missing rather than passing.

**A recommendation, not a decision.** Wire it in with a hard failure. The dependency-free property
that is genuinely load-bearing belongs to the *tool* — `index.html`, `app.js`, one stylesheet, no
build step, which is what the README's boast is actually about — and that is untouched either way.
The gate already requires Python and SQLite. The failure mode being prevented has now bitten twice.

~~Recorded meanwhile in `README.md`'s "Before you push" block, beside the command it does not
replace.~~ Superseded: `README.md` now documents the single command, its preflight table and the
engine gate.

---

## 20. 20 `ihc_checklist` nodes are swept to a path budget, not exhaustively

*Count raised from 19 to 20 on 2 October 2026: Group VIII's `bn_round_cell_ihc` (14 markers) joins them.*

**Raised 22 September 2026 with `build/check_engine_flow.mjs`.**

The engine gate walks one witness per rule plus a budgeted exhaustive walk per node — 68 nodes, 743
walks, about 58,000 stops, under a minute. Nodes with many markers (up to 40) exceed
`STOP_BUDGET`, currently 3000, and are sampled instead.

**They are reported as partial and never as OK**, which is the right behaviour — a sampled node is
not a proved node, and the check says so rather than implying coverage it does not have. The 19 are
named in its output; the largest are `g2_plasmablastic`, `g2_lineage`, `g2_matureB`,
`ac_lineage_assignment` and `st_glioneuronal_family`.

Raising the budget is a one-line change and costs only wall-clock. Left where the whole sweep
finishes in under a minute, because a gate nobody waits for is a gate nobody runs. Worth revisiting
if a defect is ever found in one of the 19.

---

## 21. Nothing tests `app.js` except the engine gate, and nothing tests the engine gate

**Raised 22 September 2026, from the same two defects.**

`build/check_engine_flow.mjs` is the only thing in the repository that exercises `app.js` at all.
Its own correctness rests on its negative controls: nine fixtures that must fail against a pre-fix
`app.js`, run via `APP=<path>`, three of which exist only to fail a fix bought too cheaply. That is
a real proof and it is documented in `docs/engine_flow_negative_controls.md`.

But it is a proof someone has to *re-run*. The controls are not part of either gate — running them
means checking out an old `app.js` and pointing the checker at it by hand. So the check that guards
the engine is itself guarded only by a procedure in a document.

No action proposed. Recorded because the shape is familiar: both defects it now catches survived
precisely because the thing that would have caught them was not part of anything automatic.


---

## 22. ❓ FOR THE REGISTRAR — Group VII items still open

**Raised 4 October 2026, after Group VII merged (pull request #2).** The full reasoning for each is in
`docs/group_07_open_questions.md` under the number given; the build contract section is named there.
Items 2–7 were ruled on 3 October 2026 and are built.

**Coding rulings owed**

| Open question | Today | Decide |
|---|---|---|
| **1** Baseline document | Built on the International Pediatric Liver Tumors Consensus Classification — López-Terrada 2014 (*Modern Pathology*) and 2025 (*Virchows Archiv*, Table 1, p. 24) — because Nagtegaal 2019 does not cover hepatoblastoma | Confirm López-Terrada 2025 as the Group VII baseline in `docs/group_baseline_documents.md` |
| **8** `8148/2` high-grade biliary intraepithelial neoplasia | Behaviour exclusion headed "In situ"; REDCap has a pick for it | Register it on that pick, or treat it as not cancer and retire the pick with the other in situ picks. Kept open 3 October 2026 |
| **18** A report that *diagnoses* malignant rhabdoid tumour | `8963/3` on the diagnosis alone, IHC outstanding when not recorded | Confirm, or route it through INI1 and SMARCA4 like the rest |
| **19** Fibrolamellar carcinoma's basis of diagnosis | `DNAJB1::PRKACA` fusion basis 8; PRKAR1A loss basis 7 | Keep 8 for the fusion or drop it to 7 (it also occurs in oncocytic pancreatic and biliary neoplasms, López-Terrada 2025, p. 29); confirm 7 for PRKAR1A |
| **20** Consensus table versus text on small cell undifferentiated hepatoblastoma | The tool follows the text (p. 25): INI1-lost tumours are malignant rhabdoid tumours | Confirm |
| **22** Behaviour of `8975` is not recorded | The tool gives `8975/1` or `8975/3`, but the headline shows `8975` and REDCap has no behaviour field, so one pick serves both | Whether REDCap records behaviour (a field, or two picks — a REDCap Registry change), and whether the headline shows the digit when a code carries two behaviours (an engine change for every group) |

**REDCap.** Open questions 9 and 21 are the Group VII repair package, indexed in §7 above. Nothing
applied. Pick 113, fibrolamellar carcinoma `8171/3`, matters most.

**Shared layers and engine**

| Open question | Item |
|---|---|
| **10** | Router rule `8158,8290` sends both codes to Group XI everywhere except C75.1; ICCC-2017 puts `8158` in VIIb at the liver and `8290` in VIb at the kidney. Splitting it is a Group III-owned rule |
| **11** | A search alias that exists in two groups enters the first (`hit.groups[0]`); and the REDCap-framed output's "REDCap value" row shows the ICD-O code, not the pick number, for the pick-number groups (III, IV, VII, VIII) |
| **12** | `alias_index.json` is over its ~30 KB guideline (Architecture §4C), and Groups VIII and IX will add more |
| **13** | Confirm the engine changes made on this branch for every group: the behaviour-exclusion heading names the behaviour digit (behaviour 0 reads "Benign neoplasm (benign tumour)", which changes Groups IV–VI); `outstanding_tests[]`; `non_reportable_heading`. The Decision Tree master file §3F, in the vault, needs a line for the two fields |

**Documents and scope**

| Open question | Item |
|---|---|
| **14** | The Group 7 Diagnostic Pathway and Alias Build Instructions predate the 4 September rulings; revise to v2, or leave the build contract as the record |
| **15** | Hepatoblastoma subtype, PRETEXT stage and specimen timing are not captured — whether the registry wants any of them recorded |
| **16** | Hepatocellular carcinoma subtypes without their own ICD-O-3.2 code are coded `8170/3`; the WHO digestive volume would confirm (`docs/sources-requested.md` item 12) |
| **17** | C23.9 and C24.x have no row in `topography_codes.json`, so a gallbladder or extrahepatic bile duct primary cannot reach Group VII — whether to add them |

---

---

## 23. ❓ FOR THE REGISTRAR — Group IV refers CD99-positive cases to Group VIII expecting Ewing sarcoma; Group VIII asks for more

**Found 2 October 2026 building Group VIII.** `group_04_dt.json` `op_ewing_site`, option "Bone",
tells the clerk: *"CD99 positive, PHOX2B and synaptophysin negative … an Ewing-family tumour,
ICD-O-3.2 9364/3 Ewing sarcoma. Code this case from the ICCC-3 Group VIII tree."* The Group VIII
round cell panel records `9364/3` only on CD99 **with** NKX2-2, on a FET::ETS fusion, or on the
report's own diagnosis of Ewing sarcoma. CD99 alone falls to `8002/3` Malignant tumor, small
cell type, because *"CD99 is not specific for sarcomas such as Ewing sarcoma; it is also
expressed in many acute leukemias"* (Kallen ME, Hornick JL. Semin Diagn Pathol
2022;39(1):29–37, p. 30).

**What it costs.** A clerk sent from Group IV with a CD99-only panel arrives expecting `9364`
and gets `8002`. Both screens say what they are doing, so nothing is silent, but the two groups
state different thresholds. It extends §14, which is the same gate seen from the Group IV side.

**To close.** Either Group IV's referral text drops "9364/3 Ewing sarcoma" and says only "code
from the Group VIII tree", or the registrar rules that CD99 with PHOX2B and synaptophysin
negative is enough for `9364/3`, and Group VIII's rule 11 and `check_group8_ewing_requires_partner`
change with it.

## 24. `alias_index.json` is over the Architecture §4C size guideline

**Found 2 October 2026.** With Group VIII's 127 aliases the index is 33,383 bytes against
Architecture §4C's "keep it under ~30 KB". The build WARNs. Groups VII and IX are being built in
parallel and will add more. It is a budget for the whole tool, not a defect in one group's file:
either the guideline is raised, or the index is split per group and loaded with the group,
which `app.js`'s lazy loading (data.md §7) already does for the decision trees.

## 25. `ICCC-2017.sqlite` range 60 ends in a trailing comma

**Found 2 October 2026.** Range 60 (VIIIb) reads `9210,9220,9240,`. The build reports an
unreadable range token for Group VIII (WARN). The three codes still classify through the other
VIIIb ranges and the generator, so nothing is mis-coded today. A Layer 1 repair, the same class
as the broken Group I row in `docs/codes-awaiting-redcap.md`.

---

## 26. ❓ FOR THE REGISTRAR — Group VIII codes the REDCap dropdown does not offer correctly

**Found 2 October 2026; recorded here 4 October 2026 by the registrar's direction.** The tool
is a data-entry aid. It does not connect to REDCap and does not verify what REDCap holds, so
these are listed here for the REDCap side to fix, not handled in the tool. Pick numbers are
from `viii_morph`; the full table is `docs/group_08_layer1_repair.md`.

| Code the tool emits | What `viii_morph` offers | Risk at data entry |
|---|---|---|
| `9220/3` Chondrosarcoma, NOS | No `/3` option. Picks 20 and 21 are `9220 - Chondroma, NOS` (`/0`) and `9220 - Chondromatosis, NOS` (`/1`) | A chondrosarcoma entered under a benign label |
| `9302/3` Ghost cell odontogenic carcinoma | Pick 64 `9302 - Odontogenic ghost cell tumor`, the `/0` synonym | A carcinoma entered under a benign label |
| `9310/3` Ameloblastoma, metastasizing | Two rows on 9310: `Ameloblastoma, NOS` (`/0`) and `Ameloblastoma, malignant` (pick 66) | The clerk must pick the second; the four-digit code alone does not decide |
| `9364/3` Ewing sarcoma | Pick 33 `9260 - Ewing sarcoma` (9260 is now Aneurysmal bone cyst, `/0`); pick 35 `9364 - Peripheral neuroectodermal tumor` | Picking by name records the retired, benign number |

For `9220` and `9302` the tool's output currently shows the "label is out of date — match on the
four-digit code" banner, which points the clerk at the benign row. `docs/group_08_registrar_review.md` §C,
items 1–3, carries the proposed REDCap repair.

---

*Last updated 4 October 2026, merging the Group VIII branch (`claude/group-8-tumor-pathway-64edbc`): its §22–§25 are renumbered §23–§26 after the Group VII §22 — §23 the Group IV CD99 referral, §24 the alias index size, §25 ICCC-2017 range 60, §26 the Group VIII codes the REDCap dropdown does not offer correctly; §8 closed and deleted (the `9260` router rule is re-keyed to `9364` and `9365`); §7 gains the Group VIII row; §20 recounted. Previously 4 October 2026, with §22 — the Group VII items still open after the Group VII merge — and the
Group VII row of §7. Previously 23 September 2026, on the Group VI branch (`group-06-renal`), with §19–§21 from the
engine gate and §19 closed by the registrar the same day. Previously 22 September 2026 on the same branch, closing §12 for all
but `9473`. Previously 22 September 2026 on the Group 5 branch (`group-05-retinoblastoma`), with
§17 and the second ligature instance in §1.3; and 18 September 2026 on the Group 4 branch
(`group-04-neuroblastoma`), with the Group 4 build documentation (§14–§18).*

## 27. Groups I and II: morphology names are validated against nothing

**Opened 4 October 2026.** The registrar removed `check_redcap_exact_names` (standing rule 16), the
only check that compared Groups I and II's `morphology_name` strings with anything; it compared them
with the REDCap option file. Every other group's names go through `check_icdo32_round_trip()`.
Groups I and II's are REDCap wordings and fail it (33 in Group I, 31 in Group II). Each build prints
a NOTE for both groups until this closes.

The work: move each name to its ICD-O-3.2 preferred term, keep the REDCap wording as an alias, and
add GROUP1 and GROUP2 to `ROUND_TRIP_GROUPS`. The pairs ICD-O-3.2 does not carry at all need the
registrar first. These are Group I's 9826/3, 9836/3, 9991/3 and 9992/3, and Group II's 9670/3,
9673/3, 9725/3, 9765/3, 9767/3, 9768/3, 9769/3, 9823/3, 9970/3 and 9971/3. To reproduce the full list,
add the group to `ROUND_TRIP_GROUPS` temporarily and run the build. Handed to the Group 1 and Group 2
sessions on 4 October 2026.

**Group I: CLOSED, 6 October 2026.** `GROUP1` is in `ROUND_TRIP_GROUPS` and the build reports
`186/186 (code, name, behaviour) triple(s) exist verbatim in icdo32.sqlite; 0 declared name
exemption(s)`. Group I no longer prints the "not validated against any source" NOTE. Detail in
`docs/group_01_icdo32_names.md`.

The 33 failures were 15 wrong names plus 18 echoes of three of them in `nos_fallback_name` and
node-level `nos_fallback`; 9945 needed no rename. One was a correctness defect rather than a
wording one: 9869 read `t(13.3)(q21;q26.2)`, which is not valid cytogenetic notation.

Two registrar rulings closed it. **9975** moves to the ICD-O-3.2 preferred term
(`Myeloproliferative neoplasm, unclassifiable`); the MDS/MPN overlap wording stays as an alias
and on the output block's ALSO CALLED row. **9826, 9836, 9991 and 9992 are removed from the
group** rather than exempted — ICD-O-3.2 carries no term for them, they were already closed
terminals, and every term that used to reach them still resolves (Burkitt to Group II's mirror,
the other three to aliases Group I already carried). No exemption mechanism was added.

REDCap now owes 15 relabels **and 4 retires**, logged in §7 above.

**Group II is still open** and is the Group 2 session's work.

## 28. Interface changes of 6 October 2026: what they leave owed

Spec `docs/superpowers/specs/2026-10-06-ux-overall-fixes-design.md`. Handover to the Group 10 session:
`docs/handover_group_10_ux_changes.md`. Proof of every new check: `docs/ux_negative_controls.md`.

**Owed to the data**

- **Sweep "behaviour" to "behavior" in clerk-facing sentences.** The interface says "Behavior" since 6 October;
  these keys in `data/database/group_01` to `group_09_dt.json` still carry the British spelling in prose a clerk
  reads: `reason` (about 180), `upgrade_path` (37), `comment` (28), `hint` (8), `label` (4), `descriptive_diagnosis`
  (3), `descriptor` (2), `question` (1). Do not touch `coding_note`, `notes`, `authoring_note`, schema keys such as
  `behaviour_resolution` and `behaviour_documented`, or node ids. Run it once the group branches that hold those
  files open have merged. Group 10's own text is written to the new spelling by its session.
- **Group 10: apply the evidence mapping and write the new fields.** Steps in the handover document.
  Until the mapping is applied the data gate fails four nodes with "evidence gate ... no `tick_list`".
- **Mixed-tumour components as tick-boxes** (the four `*_mixed` nodes of Group 10) and **recognition aids** for its
  long histology lists are the Group 10 session's to author; the engine and the data gate are ready.

**Owed to the registrar**

- Confirm the document meanings, above all the three haematology readings (flow cytometry is Lab Report; blood
  film and marrow aspirate smear are Cytology; trephine biopsy is Histology Report). Table and per-gate
  questions: `docs/evidence_document_mapping.md`.
- Decide each "DATA GAP" in that document: a gate has no option that truthfully describes a file the checklist
  can now express (for example a cytology-only file in a gate with no cytology option).
- Rule on two readings the review of 6 October made visible. A Lab Report tick reaches the tier whose old option
  said flow cytometry, and that option's captures credit flow cytometry (and IHC, where the label says "and/or"), so a
  blood count alone lifts the tier and shortens the workup list. And a file no option describes takes the nearest lower
  tier, whose sentence can deny a document that is ticked (the tool now keeps that sentence out of "Suggested based on").
  Fixing either needs new options or a document item for flow cytometry, both clerk-facing wording.
- Decide whether the seven documents need a one-line definition on screen. The registrar's wording is the bare
  label, so none was added.

**Not changed, on purpose**

- The test-result state chips, the marker grid and flow, and the workup status dropdown carry no filter box:
  they are not lists of one answer to pick. `FILTER_MIN_OPTIONS` in `app.js` turns the filter off for short lists.
- `outActions()` and the override handler are untouched; `feature/report-an-error` (parked) rewrites them. Both
  branches change `renderOutput()`, so the second to merge resolves a few lines by hand.

---

## 29. ❓ FOR THE REGISTRAR — should the tool carry the ICD-O sixth digit (grade, differentiation, phenotype)?

Registrar, 7 October 2026: wants the digit added, and wants its impact on reporting in a hospital-based
registry researched first. Nothing is built.

### What the tool does today

It emits a four-digit morphology code and a behavior digit. No group prints or records a sixth digit.
Group III prints a CNS WHO grade in a Grade row, which is a different scale from the sixth digit (WHO
ICD-O-3 first revision, section 4.6, p. 27). Rule G cannot be applied as written because there is
nowhere to put the digit. The audit of 7 October 2026 found this for Groups I to IX (rule G report)
and for Group 10 (findings F-G-04 and F-G-07).

### What the WHO manual says

Rule G (section 4.1, p. 15; section 4.3.4 with Tables 21 and 22, pp. 21-22): assign the highest grade or
differentiation described in the diagnostic statement, as the sixth digit; only malignant tumours are
graded; 9 means not stated. For lymphomas and leukaemias the sixth digit may carry the phenotype
instead (T-cell 5, B-cell 6, null cell 7, NK cell 8), which takes priority over grades 1 to 4 and which
section 3.13.3 (p. 14) calls optional. The manual's own example is "malignant teratoma, anaplastic",
coded 9082/34.

### What to research

1. Which registry standards ask a hospital-based registry for grade or differentiation, whether they
   hold it as the sixth digit of the morphology code or as a separate item, and what they use it for.
2. How complete the item is in practice, and whether registries that collect it say it changed an
   analysis or a treatment audit.
3. Which paediatric tumours carry a grade that a clerk can read from the report, and which carry none.
4. How the digit relates to the entities whose grade is already in the four-digit name (follicular
   lymphoma grade 1 to 3, Hodgkin lymphoma nodular sclerosis grade 1 and 2, solitary fibrous tumour
   grade 1 to 3). Coding the digit as well would record the grade twice.

### Decisions the research feeds

- Whether the digit is collected, and for which entities.
- Where it appears in the output block. The registrar's output-block ruling of 6 October 2026 fixed the
  rows, so a new row reopens it.
- How the clerk gives it: a question per entity, or the report's own wording captured.
- How it is labelled against the Group III CNS WHO grade, so the two scales are not read as one.
- The lymphoma and leukaemia phenotype digit stays out unless the registrar says otherwise, because the
  manual makes it optional.

The dictionary side belongs to `REDCap Registry/`, never to this repository. The tool's design does not
wait on it (registrar, 6 October 2026).

---

## 30. ❓ FOR THE REGISTRAR — "take the higher" (WHO Rules G and K): what is built, and what waits

Registrar, 7 October 2026: where a report states two grades, or two descriptive modifiers of one tumour that
no single code covers, the clerk records the higher. It applies to grade-named ICD-O-3.2 entities and to
descriptive modifiers, as a hint on the screen that offers both (WHO ICD-O-3 first revision, Rule G, p. 15;
Rule K, p. 16; section 4.3.4, pp. 21-22).

### Built

- **Hints:** Hodgkin lymphoma nodular sclerosis (`g2_chl_subtype`); spinal ependymoma grade, diffuse glioma
  grade, oligodendroglioma, meningioma architecture, central nervous system descriptors 8002 to 8005, and the
  ependymoma 9392 and 9393 pair (`sp_ependymal_grade`, `st_diffuse_glioma_grade`, `st_oligo_molecular`,
  `mn_he_subtype`, `un_report_descriptor`, `pf_ependymal_exclusions`, `st_legacy_documented`); hepatocellular
  carcinoma 8172 to 8175 (`hp_hcc_subtype`); osteosarcoma, chondrosarcoma and chordoma (`bn_osteosarcoma`,
  `bn_cartilage`, `bn_chordoma`); solitary fibrous tumour, liposarcoma, leiomyosarcoma (`st_sft_behaviour`,
  `st_adipocytic`, `st_smooth_muscle`).
- **Follicular lymphoma:** two new grade markers ("Grade 3 or grade 2-3 stated", "Grade 2 stated") and their
  rules; the highest grade ticked wins.
- **Meningioma:** BAP1 loss is recorded and changes neither the code nor the grade. The four rules that let it
  pre-empt the subtype are gone, so a rhabdoid or papillary meningioma records 9538/3.
- **Retinoblastoma:** the higher grade governs, severe anaplasia outranks G1 and G2, and a diffuse infiltrating
  growth pattern outranks a grade (contract §2.4).

### Waiting on the registrar

- **Neuroendocrine tumour, grade 2 (`8249`, atypical carcinoid).** No group offers it. ICCC-2017 places 8249 in
  Group XI by site (XIf1 to XIf11), and none of those ranges covers the kidney or the liver. Offering it in Groups
  VI and VII needs an entry, aliases and a line on the REDCap-side list.
- **Moderate anaplasia with a stated differentiation grade** changes no code in retinoblastoma. The sentence rests
  on the 7 October decision alone; the Mendoza scale places moderate between the two ends and has no bridge.
- **A typed term filed under several groups** still stops when the picked site names neither group (4 October
  ruling). The record-only site step covers single-group terms only, so a lymphoma term filed under Groups I and II
  and typed at a kidney stops for the registrar.
- **Group 10**, merged after this tree was cut: `9082` and `9083` are reachable only through the mixed-tumour
  screen; a named mixed term ends the case, so teratocarcinoma with a choriocarcinoma component records `9081`
  where `9101` fits; Sertoli-Leydig intermediate differentiation ends in a behavior-1 exclusion with no hint to
  take the poorer grade; a stain panel with embryonal and yolk sac markers records `9070`.

### Known and not changed

- `build/drive_first_tap.mjs` stops at its fourth control, which looks for a `select` that is now a filtered
  radio list. It predates this change.
- `presentation_router.json`: `asked_by` on `primary_compartment` lists `unsure`, which does not set
  `dual_group_discriminator`. The build now notes it.
- `fl_grade` ("not graded" in three paediatric rules), `bap1_status` and `meningioma_risk_tier` are recorded and
  read by nothing.
