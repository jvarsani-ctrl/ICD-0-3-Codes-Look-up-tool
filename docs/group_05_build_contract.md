# Group 5 build contract — Retinoblastoma

**Branch:** `group-05-retinoblastoma`, cut from `group-04-neuroblastoma` (28 commits ahead of `main`).
**Written:** 22 September 2026, by the build controller, before any tree was authored.
**Governs:** `data/database/group_05_dt.json`, `data/aliases/aliases_group_05.json`, the shared-layer
changes named in §7, and the validator rules in §8.

**Source of the method:** `docs/group_baseline_documents.md` — the registrar's ruling of
16 September 2026 that every group is built the way Group 3 was built.

> **Read this file, not the whole repo.** §0 is the complete pre-context for an implementing agent:
> every fact, code, citation and engine constraint needed to author this group is stated here or
> in the one file §0.9 names. Do not re-read the diagnostic pathway, the master instruction files,
> `app.js` or another group's `dt.json` unless this contract sends you there by name.

---

## 0. Pre-context — everything an implementing agent needs

### 0.1 What this group is

ICCC-3 **Group V — Retinoblastoma**. One subgroup (`V`), one tumour, one site. It is the smallest
group in the classification. ICCC-2017 defines it as morphology **9510–9514 at behaviour `3`,
topography `C00.0–C80.9`** (all sites — the constraint is morphological, not anatomical).

Retinoblastoma is the embryonal tumour of the retina, almost entirely a disease of children under
five. About 30–40% of cases are hereditary (germline *RB1*), and those are bilateral or multifocal.

### 0.2 The four codes this group builds, and the two it cannot

Generated, never transcribed — `python3 build/generate_group_inventory.py --group V` joins
ICCC-2017.sqlite to icdo32.sqlite and returns exactly this:

| ICD-O-3.2 | Preferred term | Built? |
|---|---|---|
| `9510/3` | Retinoblastoma, NOS | ✅ the dominant code |
| `9511/3` | Retinoblastoma, differentiated | ✅ |
| `9512/3` | Retinoblastoma, undifferentiated | ✅ |
| `9513/3` | Retinoblastoma, diffuse | ✅ |
| `9510/0` | **Retinocytoma** | ❌ behaviour outside the declaration |
| `9514/1` | **Retinoblastoma, spontaneously regressed** | ❌ behaviour outside the declaration |

`morphology_entries[]` therefore has **four** objects. The generator's own summary line reads
`codes_absent_from_icdo32: ["9514"]` — not because the number is missing from ICD-O-3.2 but
because ICD-O-3.2 carries no `9514/3`, and Group V admits behaviour 3 only. This is the identical
mechanism that kept `8683` out of Group IV (Group 4 contract §0.2).

**Neither exclusion is a deletion.** Both codes exist and are current in ICD-O-3.2. They are
unreachable *here* because ICCC-3 Group V does not register them. §2.1 and §2.2 say what the tree
must do about each.

### 0.3 ICD-O-3.2 changed nothing on this stem — checked, not assumed

All four IARC 3.1→3.2 change documents were text-extracted and searched on 22 September 2026:

| Document | Hits for `951[0-9]`, `retinoblast`, `retinocyt`, `retinom` |
|---|---|
| *Deleted codes and their terms* (9 Oct 2020) | **none** |
| *New codes and their terms* | **none** |
| *Terms that are changing behaviour* | **none** |
| *A summary of the main changes* | **none** |

So `9510/0`, `9510/3`, `9511/3`, `9512/3`, `9513/3` and `9514/1` all pre-date ICD-O-3.2, were
untouched by it, and carry **no `[obs]` marker** on any term in `icdo32.sqlite`. None has a
`see_also`, a `see_note`, an `includes` or an `excludes`. Six clean rows, no synonyms, no related
terms — which is why the alias layer has to do more work than usual (§6).

The multiple-primaries workbook (`Multiple_primaries_ICD-O-3.2_06102020.xls`, 27 rows) names no
eye or retinoblastoma rule. Bilateral retinoblastoma is governed by the registry's general
multiple-primary rules, not by a morphology-specific one.

### 0.4 ★ The single most load-bearing fact in this build: Visser Table 3

`docs/references/visser-2023-key-points.md` §5, from **Visser O, et al. *2022 revised European
recommendations for the coding of the basis of diagnosis of cancer cases in population-based
cancer registries.* Frontiers in Oncology 2023;13:1250549**, Table 3, pp. 04–05:

> | Entity | Basis | Topography | Morphology |
> |---|---|---|---|
> | **Retinoblastoma** | **1 or 2** | **C69.2** | **`9510/3`** |

Retinoblastoma is one of only **five** entities in the entire ENCR scheme that may be registered at
**basis 1 — clinical examination alone, with no imaging and no tissue.** The other four are
melanoma of the skin, melanoma of the eye, angiosarcoma of the irradiated breast, and Kaposi
sarcoma of the skin. The paper heads retinoblastoma's row group *"Solid childhood cancers
(age <15 years)"*.

Four consequences, and every one of them shapes the tree:

1. **A clinical-only terminal emits a real code here.** In Group IV every referral-tier branch
   refers to Group XII, because Group IV has no Table 3 row. Group V has one. `rb_clinical_alias`
   emits `9510/3` at **basis 1** — the only group built so far that may.
2. **The imaging route emits `9510/3` at basis 2.** This is the modal output of the whole group.
3. **Table 3 licenses `9510/3` and nothing else.** No branch may reach `9511`, `9512` or `9513`
   without a pathology report. Basis 1 and basis 2 terminals emit `9510/3` only.
4. **Visser rule 4, p. 03 — "possible" is not registrable.** Codes 1 and 2 may be used only when
   cancer is *at least likely*. "If clinical investigation makes cancer only *possible*, or if a
   non-malignant disorder could equally explain the findings, the case is not registered at all in
   the absence of pathology." This is the citation behind the leukocoria-mimic branch (§2.3) — and
   it is a `non_reportable` destination, not a `refer_group` one, because Coats disease and
   persistent hyperplastic primary vitreous are not cancers in any group.

**This is what stands in place of a Hoogendijk-equivalent.** No registry-implications paper exists
for the WHO Eye and Orbit volume (a MeSH sweep recorded in
`Group 5 Papers/Group 5 — Registry-Implications MeSH Search Results.md` found none, and §10
re-tested it). The cross-cutting layer carries the whole load, and for this group it carries it
unusually well: Visser names the entity, the topography, the code and the basis explicitly.

### 0.5 The three structural facts that make this group unlike every group built so far

From `Group 5 — Retinoblastoma Diagnostic Pathway.md` §0 (Razek & Elkhamary 2011; Ghose & Kaliki
2022; College of American Pathologists Retinoblastoma Protocol v4.0.0.0 Note A):

1. **Biopsy of an intact globe is contraindicated.** Incisional or needle biopsy risks extraocular
   seeding and can convert a curable intraocular tumour into fatal orbital or metastatic disease.
   There is no histology-first branch for an intact eye. Histology exists *only* after the eye has
   been removed — and enucleation is a **treatment decision**, not a missing investigation.
2. **Diagnosis is clinical plus imaging.** Leukocoria on examination with a calcified intraocular
   mass on B-scan ultrasound is the diagnostic standard. The imaging route is the **primary
   spine**, not an exception.
3. **Molecular findings never change the code.** *RB1* germline status, *MYCN* amplification and
   chromosome 6p gain drive counselling and prognosis. Hereditary and sporadic retinoblastoma both
   code `9510/3`. `code_neutral_molecular` is `true` on every entry in this group.

The practical result: **most cases code `9510/3`.** The subtypes exist for enucleated eyes with a
pathology report that states a grade or a growth pattern.

### 0.6 ⚠️ Engine constraint on `imaging_pathway` — the node type this group is built on

`docs/TODO.md` §10, found 18 September 2026, verified against `app.js` on this branch:

- `app.js` line 1005 `imagingPathway()` renders **only** `imaging_features`,
  `biochemical_questions` and `diversion_criteria`. **`options[]` is never rendered.**
- Line 2263 resolves it: any ticked diversion criterion, or an incomplete constellation, goes to
  `fallbackTarget(n)`; a complete constellation advances to **the node itself**, so the node
  carries the `morphology_code`.
- `fallbackTarget()` tries `insufficient_next_node`, then `nos_fallback`, then **throws**.
  `nos_fallback` is forbidden on `imaging_pathway` by `NOS_FORBIDDEN_TYPES`.

> **Therefore:** every `imaging_pathway` node in `group_05_dt.json` **must** declare
> `insufficient_next_node`, **must not** declare `options[]`, and carries its own
> `morphology_code` + `behavior_code` + `basis_of_diagnosis` for the confirmed-constellation
> outcome. Three Group 3 nodes crash at runtime for want of exactly this. §8 rule 1 makes it a
> build failure.

**And four fields the validator already demands, which the first draft of this contract missed.**
`check_imaging_terminals` in `build/build_database.py` is written as Group 3's rule 11 but carries
**no group guard**, so it runs on every file. An imaging-only terminal must declare all four:

| Field | Required value |
|---|---|
| `no_tissue` | `true`. It is what stops the case being counted as microscopically verified. |
| `endpoint_verification` | the exact string `"not_verified"` |
| `basis_of_diagnosis` | `2` or `4`, as an **integer**. Group V uses `2`; there is no tumour-marker route in this disease. |
| `diversion_criteria` | present and **non-empty**; every element an object with a non-empty `feature` **and** a non-empty `reason` |

`"diversion_criteria": []` is an explicit build error, not "no diversions apply" — in the check's
own words it *"renders exactly like a terminal that was never gated, while reading to the next
author as considered and cleared."*

**Basis 1 is legal here.** The ban on basis 1 is guarded by `ctx.group == GROUP3`, because every
central-nervous-system row in Visser Table 3 is basis 2. Retinoblastoma's row reads *1 or 2*
(§0.4), so `rb_clinical_alias` may and does emit `basis_of_diagnosis: 1`.

### 0.7 Schema, in one place

**`morphology_entries[]`** — every field required, `null` where it does not apply:
`morphology_code`, `morphology_name`, `iccc3_subgroup_id`, `iccc3_subgroup_name`, `who_version`,
`behavior_code`, `diagnostic_tests_required[]`, `ihc_markers_required`, `ihc_markers_exclude`,
`imaging_sufficient`, `imaging_features`, `nos_fallback_code`, `nos_fallback_name`,
`confidence_ceiling`, `clinical_alert`, `coding_note`, `code_neutral_molecular`, `redcap_value`,
`primary_sites[]`, `topography_dependent`, `topography_routing_note`.

`diagnostic_tests_required` is drawn from the closed list
`["Referral only","Histology","Imaging","IHC","ISH","Flow cytometry","Cytogenetics/FISH","Molecular/PCR"]`
and has **no OR semantics** — express substitution on the branch with `satisfies_tests[]`.
`confidence_ceiling` is the confidence achievable **with all required tests present**; the engine
caps at `medium` while any required test is outstanding.

**Node types** — a closed vocabulary; a group uses any subset and may not invent one:
`document_inventory` (entry node of every tree), `clinical_alias`, `morphology_only`,
`imaging_pathway`, `ihc_checklist`, `cytogenetics_dropdown`, `molecular_freetext`,
`histology_subclassification`, `site_resolution`. (`clinical_presentation` and `site_capture` are
router-tier and live in `presentation_router.json`, never in a group file.)

**`nos_fallback` by node type** — non-null for `ihc_checklist`, `cytogenetics_dropdown`,
`molecular_freetext`, `numeric_gate`; **null** for `document_inventory`, `clinical_alias`,
`morphology_only`, `imaging_pathway`, `histology_subclassification`, `site_resolution`. A node-type
rule, not a step-number rule.

**Branch destinations — exactly one per branch**, on every `options[]` entry, every
`resolution_logic[]` rule and every `nos_fallback`:

| Destination | Fields | Means |
|---|---|---|
| Code | `morphology_code` (+ `behavior_code`) | this group owns the case |
| Continue | `next_node` | ask another question |
| Not reportable | `non_reportable: true` + `reason` | not a malignancy; emits no code |
| Refer | `refer_group` (1–12, not 5) + `reason` | a real cancer in a different group |
| Behaviour-excluded | `behaviour_exclusion` {} (§2.1) | the entity exists; its behaviour is outside the group |

**`reason` is clerk-facing and is rendered. `coding_note` and `topography_routing_note` are
author-facing and are displayed nowhere.** Registrar's ruling. Anything a clerk must read at the
point of decision goes in `question`, `hint`, `reason` or the branch's own `label`.

**`basis_of_diagnosis`** — ENCR, valid set `{0,1,2,4,5,7,8,9}`; 3 and 6 do not exist; 0 and 9
override; otherwise the highest of 1–8. Declared per tree as
`"basis_of_diagnosis_defaults": {"ihc_counts_as": 7, "methylation_counts_as": 8}`.

### 0.8 Rules inherited unchanged, which this build does not reopen

- **`clinical_alert` is `null` everywhere.** The tool renders no clinical warnings — registrar's
  ruling of 4 September 2026. Clinically consequential material goes to
  `docs/clinical-warnings.md` instead. Group V has a great deal of it (§9).
- **No `resource_level_gate`, and no site profile.** Unavailability follows from a declared site
  profile, never from the required level. With no profile the honest output is *not established*,
  not *unavailable*. The flag `upgrade_line_says_unavailable` is banned and the build fails on it.
  This bites here: B-scan ultrasound and orbital magnetic resonance imaging are not universally
  available. That is a reason for a node to ask **which imaging was actually done**, never a
  reason to gate. The tool is global; the Uganda Cancer Institute is one site among many.
- **`satisfies_tests[]`** suppresses an outstanding-workup row, so it is the one field that can
  make a case look better evidenced than it is. Values must come from the closed vocabulary and
  must appear in the terminal code's own `diagnostic_tests_required`. Declare it only for the
  modality the branch's own finding text names.
- **Never fabricate a morphology code.** Verify against Layer 1; if it cannot be verified, stop and
  flag it.
- **No clinical logic in `app.js`.** Anything that varies by group belongs in JSON.

### 0.9 The one other file to read

`docs/references/visser-2023-key-points.md` — 6 pages, and §5's Table 3 row is the spine of this
group. Read it once. Everything else you need is in this contract.

---

## 1. The inventory is generated, never transcribed

```bash
python3 build/generate_group_inventory.py --group V --out <scratch>/g5_inventory.json
```

Output, 22 September 2026: `ICCC range entries 5 · distinct codes 5 · absent from ICD-O-3.2 1 ·
usable 4 · (code,behaviour) records 4`.

`morphology_name` is the **ICD-O-3.2 Preferred term**, keyed to `icdo32.sqlite`, not to the REDCap
option file (Group 4 ruling D5). For this group the two agree on all four built codes, which is
worth stating because §1.1 is where they do not.

### 1.1 Layer 1 conflict — REDCap offers a code the tool cannot emit

`ICD coding/RedCap Options/Group 5- Retinoblastoma.md` offers five options:

```
9510, 9510 - Retinoblastoma, NOS
9511, 9511 - Retinoblastoma, differentiated
9512, 9512 - Retinoblastoma, undifferentiated
9513, 9513 - Retinoblastoma, diffuse
9514, 9514 - Retinoblastoma, spontaneously regressed
```

The fifth is not assignable. ICD-O-3.2 carries `9514` only at behaviour `/1`, and ICCC-3 Group V
declares behaviour `3`. A case coded `9514/1` is not a Group V case and is not a malignant
registration at all.

**This is a Layer 1 defect, not a tool defect.** It is recorded in
`docs/group_05_layer1_repair.md` (§7.3) for the registrar, alongside the Group 3 and Group 4
repair packages. The tool does not emit `9514`, does not offer it, and says why when a clerk
arrives with the words (§2.2).

---

## 2. The four code decisions this group forces

### 2.1 `9510/0 Retinocytoma` — out of group, and the tree must say so

Retinocytoma (retinoma) is the benign counterpart of retinoblastoma: a differentiated, non-growing
retinal tumour, often with calcification, sometimes found in the relative of a proband. ICD-O-3.2
codes it **`9510/0`**, sharing its four-digit stem with `9510/3`. **That shared stem is the trap** —
a tree that resolves "retinocytoma" to `9510` without carrying the behaviour emits `9510/3
Retinoblastoma, NOS` for a benign lesion.

**Required:** a branch whose destination carries `behaviour_exclusion`, the field Group 4 added
(Group 4 contract §3) and which Group 5 is the first other group to adopt:

```json
"behaviour_exclusion": {
  "icdo_code": "9510",
  "icdo_behaviour": "0",
  "icdo_term": "Retinocytoma",
  "group_declares": "3",
  "reason": "Retinocytoma (retinoma) is the benign counterpart of retinoblastoma. ICD-O-3.2 codes it 9510/0. ICCC-3 Group V admits behaviour 3 only, so it is not a registrable cancer in this group and no Group V code is emitted for it. Record the finding and refer the case to the registrar.",
  "registrar_decision_required": true
}
```

All six keys required; `icdo_code`, `icdo_behaviour` and `icdo_term` must round-trip against
`icdo32.sqlite` as the **Preferred** term at that `(code, behaviour)` — `Retinocytoma` is the
Preferred term at `9510/0`, confirmed. `icdo_behaviour` must not be in the group's declaration.
A branch carrying `behaviour_exclusion` emits **no** `morphology_code`; carrying both is a build
error. `reason` is clerk-facing and is rendered.

### 2.2 `9514/1 Retinoblastoma, spontaneously regressed` — the same treatment

A spontaneously regressed retinoblastoma — the shrunken, calcified, non-functional globe (phthisis
bulbi) with no viable tumour — is real, occurs in about 2% of cases, and has its own ICD-O-3.2
code at behaviour `/1`. It is outside Group V's declaration for the same reason. Second
`behaviour_exclusion`, with `icdo_code: "9514"`, `icdo_behaviour: "1"`,
`icdo_term: "Retinoblastoma, spontaneously regressed"`.

**The registrar owes a decision here**, and the tool must not pre-empt it: a regressed
retinoblastoma is a *treated or self-treated cancer that existed*. Whether the registry registers
it as an incident case (and if so on what code) is a registration-rules question, not a morphology
question. Recorded in §11 and flagged, not resolved.

### 2.3 ⚠️ Retinocytoma is a genuine homonym — the disambiguation is mandatory

"Retinocytoma" names two different things and the tool must separate them:

1. **A standalone lesion** — pure retinocytoma/retinoma with no viable retinoblastoma. That is
   `9510/0`, §2.1, behaviour-excluded.
2. **The lowest grade on Mendoza's anaplasia scale** (Mendoza PR, et al. *Histopathologic grading
   of anaplasia in retinoblastoma.* American Journal of Ophthalmology 2015;159(4):764–776), which
   runs *retinocytoma / mild / moderate / severe* **inside an active retinoblastoma**. A
   "retinocytomatous area" in an enucleation report is differentiation within a retinoblastoma,
   not a retinocytoma.

Coding the second as `9510/0` would record a benign tumour for a child with a malignant one. The
branch must ask which the report means, in the report's own words, and must not infer.

### 2.4 The subtype codes are read from the report, never derived by the tool

`9511` differentiated, `9512` undifferentiated and `9513` diffuse are live, non-obsolete Preferred
terms in ICD-O-3.2 (§0.3) and all three are REDCap options. They are built.

**But the tool does not grade a retinoblastoma.** Following the Group 4 D3 precedent
(`sn_report_wording`), the subtype is taken from the pathology report's own stated grade or growth
pattern, and the node's hint says so explicitly. The mapping, from the College of American
Pathologists Retinoblastoma Protocol v4.0.0.0 (2017) and the diagnostic pathway §2A:

| What the enucleation report states | Code |
|---|---|
| **Diffuse infiltrating** growth — grows laterally within the retina, no discrete mass | `9513/3` |
| Fleurettes or neuronal differentiation (grade **G1**); many Flexner-Wintersteiner rosettes (grade **G2**, "moderately differentiated") | `9511/3` |
| Occasional rosettes (grade **G3**); no rosettes with anaplasia, poorly differentiated (grade **G4**) | `9512/3` |
| Enucleation performed, grade or subtype not stated (**GX**) | `9510/3` |

Where the report states a Mendoza anaplasia grade *instead of* a differentiation grade, the bridge
is: retinocytoma-grade or mild ≈ the differentiated end; severe ≈ the undifferentiated end. **Where
the report states more than one grade, code the higher.** Severe anaplasia outranks a G1 or G2
differentiation grade, and a G3 or G4 differentiation grade outranks mild anaplasia. Moderate
anaplasia changes no code where a differentiation grade is stated; moderate anaplasia alone stays in
the GX/`9510` option. The registrar confirmed both on 7 October 2026 (TODO §30).

*Decision, 7 October 2026 (registrar).* The first build said "code from the differentiation grade"
and recorded anaplasia as a prognostic finding that changes no code. That coded a G2 report with
severe anaplasia as `9511`, although this contract's own bridge places severe anaplasia at the
undifferentiated end, and the tool has no field in which to record the anaplasia it told the clerk to
set aside. The registrar replaced the rule with the higher-grade rule. Sources: the WHO ICD-O-3 first
revision, section 4.3.4, pp. 21-22 (code the higher of two stated degrees; "anaplastic" is grade IV
beside "undifferentiated"); College of American Pathologists Retinoblastoma Protocol v4.0.0.0, p. 4,
Note K (anaplasia is graded on its highest level in the tumour); Mendoza PR, et al., American Journal
of Ophthalmology 2015;159(4):764-776, p. 765 (a moderately anaplastic tumour with a focal region of
severe anaplasia is graded severe). The same rule governs an area called "retinocytoma" inside an
active tumour (§2.3): it sets `9511` only where the report states no poorer grade and no severe
anaplasia for the rest of the tumour, and `9512` otherwise. A stated diffuse infiltrating growth pattern outranks a grade, because `9513` is the higher code (WHO Rule K: two modifiers with different codes and no combined code).

### 2.5 `9513` cannot use the imaging route, and `9510` must

Diffuse infiltrating retinoblastoma grows as a flat placoid infiltrate **without a discrete
calcified mass**, is rare (1–2%), presents later (around age 6), and mimics uveitis or
endophthalmitis. The Track-1 criteria — calcified mass, child under five — would **falsely
exclude** it.

**Required:** `imaging_sufficient: true` on `9510` **only**; `false` on `9511`, `9512` and `9513`.
And the imaging node's own text must not assert that an older child with an infiltrative
intraocular process does not have retinoblastoma; the diversion criteria send that case to tissue,
which is the correct outcome, not to a "not cancer" terminal.

---

## 3. No new schema fields

Group 1 added six, Group 2 five, Group 3 seven, Group 4 one. **Group 5 adds none.**

`behaviour_exclusion` is adopted from Group 4 unchanged (§2.1). Group 4's contract anticipated
this: *"Groups 5–12 will meet the same problem … and may adopt it then, on their own evidence."*
The evidence is §0.2 — two codes on live stems whose behaviours fall outside the declaration.

The one thing this group genuinely lacks a field for is recorded in §11 as an open item rather than
invented here.

---

## 4. Tree architecture — one tree, two tracks

**One tree: `g5_retinoblastoma`, entry node `rb_document_inventory`.** Group V has one subgroup and
one tumour; a multi-tree architecture would be scaffolding around nothing. Groups 1–4 all have
several trees because they hold several tumour families. This one does not.

The split that matters is inside the tree, and it is a single question: **has the eye been
removed?**

```
rb_document_inventory  (Step 1 — evidence in file)
  ├── referral / clinical note only ............. rb_clinical_alias      → 9510/3 basis 1
  ├── ophthalmic examination and/or imaging ..... rb_imaging_pathway     → 9510/3 basis 2
  │                                                 diverted/incomplete ↘ rb_imaging_insufficient
  ├── cytology or aqueous-humour liquid biopsy .. rb_cytology            → 9510/3 basis 5
  ├── enucleation or exenteration specimen ...... rb_enucleation_report  → 9511/9512/9513/9510 basis 7
  └── inadequate / uninterpretable specimen ..... rb_imaging_pathway or the non-registrable terminal
```

- **`rb_document_inventory`** — `document_inventory`. Its histology option is labelled
  **"Enucleation or exenteration specimen with a pathology report"**, never "histology" or
  "biopsy". An intact-eye biopsy is contraindicated (§0.5) and the tool must not present it as a
  normal route. The node's `hint` says so.
- **`rb_clinical_alias`** — the only clinical-alias node in the tool that emits a specific code.
  Visser Table 3 basis 1 (§0.4). It emits `9510/3`, `confidence` capped low by the engine, and its
  branches distinguish *a note that asserts retinoblastoma or leukocoria with a suspected
  intraocular tumour* (→ code) from *a note that asserts nothing diagnostic* (→ the
  not-registrable terminal, Visser rule 4).
- **`rb_imaging_pathway`** — `imaging_pathway`, per the engine constraint in §0.6:
  `imaging_features[]` carries the constellation, `diversion_criteria[]` carries the mimics and the
  features that demand tissue, `insufficient_next_node` is set, `options[]` is absent,
  `nos_fallback` is null, and the node itself carries `morphology_code: "9510"`,
  `behavior_code: "3"`, `basis_of_diagnosis: 2`.
- **`rb_cytology`** — `morphology_only`. Added 22 September 2026 once the baseline paper was on
  disk (§10.9). Cytology of a retinoblastoma is discouraged but real, and it is **stronger evidence
  than imaging**: Visser 2023 Table 1 puts cytology at **basis 5**, and rule 8, p. 06 puts an
  aqueous-humour or plasma **liquid biopsy at 5 as well**, not 8, when no pathology is available.
  It emits **`9510/3` at basis 5** and never a subtype — a cytology cannot grade differentiation or
  establish a growth pattern. Its `hint` carries Milman 2023 Table 10's own cautions verbatim in
  substance: necrosis, mitoses and nuclear atypia should be present before retinoblastoma is
  diagnosed on a cytology, and sampling of retinal neurons and scant material are the named
  pitfalls. **The branch must not read as a route to pursue.** Biopsy is avoided; this option
  exists because the report may already be in the file.
  It is **not** an `imaging_pathway` node, so the four fields in §0.6 do not apply to it, and
  `no_tissue` must **not** be set on it — a cytology has tissue-derived cells.
- **`rb_enucleation_report`** — `histology_subclassification`. The subtype comes from the report's
  own words (§2.4). Its `GX` option emits `9510/3` at basis 7. Its retinocytoma and
  phthisis-bulbi options carry `behaviour_exclusion` (§2.1, §2.2).
- **Molecular capture is code-neutral and optional.** If a `molecular_freetext` node is authored
  for *RB1*, *MYCN* and chromosome 6p, every destination returns the same code the case already
  had, and its `nos_fallback` (mandatory on that node type) names that code. Do not author
  cytogenetics options that imply a code change; there are none in this disease.

### 4.1 The imaging constellation, and what must divert

`imaging_features[]` — every one must be ticked for the constellation to resolve:

1. an intraocular mass on B-scan ultrasound or on orbital magnetic resonance imaging;
2. **calcification within the mass** — on ultrasound, high-reflectivity foci casting acoustic
   shadows;
3. child under five years.

Feature 2 is the discriminator and is not optional. Leukocoria causes retinoblastoma in only
56–72% of children; the rest is Coats disease (4–16%), persistent hyperplastic primary vitreous
(19–28%), coloboma, sclerosing endophthalmitis, retinal astrocytoma, Norrie disease, retinopathy of
prematurity and medulloepithelioma (Razek & Elkhamary 2011). Coats disease and persistent
hyperplastic primary vitreous characteristically show **no** calcified mass. A node that accepts
"an imaging report exists" over-calls retinoblastoma. **Ultrasound, not magnetic resonance
imaging, is the calcification detector** — magnetic resonance imaging detects calcification
poorly, and computed tomography is avoided in a child who may carry a germline tumour-suppressor
mutation.

`diversion_criteria[]` — any one ticked sends the case to `insufficient_next_node`, whatever the
constellation shows:

- retinal detachment or exudate with **no** calcified mass — the Coats disease / persistent
  hyperplastic primary vitreous pattern;
- a flat, diffusely infiltrating intraocular process without a discrete mass, or a child over
  five — the diffuse-variant pattern (§2.5), which needs tissue, not exclusion;
- pseudohypopyon or an anterior-segment mass suggesting an inflammatory mimic;
- extraocular or orbital extension, which changes the specimen that will arrive.

### 4.2 Trilateral retinoblastoma is a second primary, not a dual-group code

Bilateral retinoblastoma with a midline intracranial primitive neuroectodermal tumour — usually
pineoblastoma, suprasellar in the tetralateral form — occurs in 1.5–5% of cases and is associated
with hereditary disease. The ocular tumour codes `9510/3` in Group V. **The intracranial tumour is
a separate primary in Group III** and needs its own tumour record.

This is **not** a dual-group code: the same code does not route to two groups by site. Group V's
codes never leave Group V — `topography_dependent` is `false` on all four entries, and no
`topography_routing_note` is written. The instruction to open a second record belongs in the
clerk-facing `reason` of a branch or in a `hint`, and in `docs/clinical-warnings.md` (§9).

### 4.3 Bilaterality and multifocality change no code

Hereditary retinoblastoma is bilateral in about 30% of cases and often multifocal within one eye.
Laterality and focality are registry fields. Bilateral disease is still `9510/3`. The tool records
the finding and does not branch on it.

---

## 5. What the diagnostic pathway document gets wrong

`Group 5 — Retinoblastoma Diagnostic Pathway.md` (2 June 2026) is a good document and its §7 named
eleven build conflicts before anyone wrote a line of JSON. Four of its statements are wrong and
must not be carried into the build.

### 5.1 It gives `9514` behaviour `/3`. ICD-O-3.2 gives it `/1`.

Pathway §1's table reads "`9514` | Retinoblastoma, spontaneously regressed | **/3**". It is `/1` in
ICD-O-3.2, which is why the code is not buildable at all (§0.2). The pathway's §4C and §7.10, which
both route to `9514`, are unimplementable as written; §2.1–§2.3 above replace them.

### 5.2 It maps retinocytoma to `9514`. ICD-O-3.2 gives retinocytoma its own code, `9510/0`.

Pathway §4C treats retinocytoma/retinoma and phthisis bulbi as two scenarios converging on one
code. They are two codes: `9510/0` and `9514/1`. Both are behaviour-excluded, for different
reasons, and the branch texts differ.

### 5.3 It says medulloepithelioma routes "Group III/IV/V by site". It never routes to Group V.

Pathway §1 reads: *"Contrast medulloepithelioma 9501–9504, which routes Group III/IV/V by site."*
ICCC-2017, queried directly: `9501`–`9504` belong to **IIIc3** at C70.0–C72.9 and to **IVb** at
every other site, including C69.4 (ciliary body). Intraocular medulloepithelioma — a genuine
leukocoria mimic — is an **ICCC-3 Group IV** tumour. The router's `9501-9504` dual-group rule is
already correct and is not changed. Any branch that names medulloepithelioma refers to **Group 4**.

### 5.4 Its §7.11 proposes extending the closed test vocabulary. Do not.

Pathway §7.11 suggests adding "Ophthalmic examination (EUA)" to `diagnostic_tests_required`. Its
own recommendation — map examination under anaesthesia, ultrasound and magnetic resonance imaging
all onto `"Imaging"` — is right and costs no schema change. Take it. The distinction the pathway
was reaching for is carried by `basis_of_diagnosis` (1 for examination alone, 2 for imaging),
which is a better instrument and already exists.

### 5.5 Seven of its eleven §7 items are correct and are implemented

7.1 (relabel the histology option, branch on intact vs enucleated), 7.2 (no `ihc_checklist`
anywhere, `ihc_markers_required: null` on every entry), 7.3 (molecular is capture-only),
7.4 (imaging-first is the spine, `imaging_sufficient: true` on `9510` only), 7.5 (the "upgrade" to
a subtype is enucleation, a treatment — the text must not read as a data-quality gap a clerk can
close), 7.6 (require the calcified-mass discriminator), 7.7 (`9513` is enucleation-only),
7.8 (trilateral is a second primary), 7.9 (`9510` is both default output and NOS fallback).

---

## 6. The alias layer does more work here than in any other group

`Group 5 — Alias Build Instructions.md` (13 May 2026) specifies 15 entries with NCI Thesaurus
concept identifiers confirmed by direct API lookup on that date. Its schema is the one already in
`data/aliases/aliases_group_04.json`: `alias`, `full_form`, `also_known_as[]`, `alias_type`,
`origin_system`, `nci_concept_id`, `who_version_current`, `maps_to_morphology_codes[]`,
`maps_to_iccc3_subgroup_id`, `needs_ihc_tree`, `ihc_tree_id`, `tree_entry_node`, `clinical_alert`,
`notes`, `coding_note`, and optionally `refer_group` / `refer_code`.

Three reasons the alias file matters more than usual:

1. **ICD-O-3.2 gives these six rows no synonyms and no related terms at all** (§0.3). Every
   findable string a clerk might type has to be authored here; nothing comes free from the
   dictionary.
2. **"Eye cancer" and "white eye" are what referral letters actually say.** Late presentation is
   the norm in the populations this registry serves, and referrals arrive in lay language:
   proptosis described as "protruding eye", leukocoria as "white pupil" or "cat's-eye reflex".
3. **`needs_ihc_tree` is `false` on every entry and `ihc_tree_id` is the tree, not an IHC tree.**
   The field name is historical. Point `ihc_tree_id` at `g5_retinoblastoma` and `tree_entry_node`
   at `rb_document_inventory`.

**Two corrections to the alias instructions, forced by §2:**

- Its entries for retinocytoma and retinoma map to `9514`. They must map to **no Group V code**:
  `maps_to_morphology_codes: []`, and `notes` explaining `9510/0` and the homonym (§2.3). The same
  for "spontaneously regressed retinoblastoma", which is `9514/1`.
- Its note 3 claims "all retinoblastoma codes are malignant (/3)". Two are not.

**Trilateral retinoblastoma** gets an entry that carries `refer_group: 3` with a `reason` naming
the pineal tumour as a separate primary, while still mapping the ocular component to `9510`.

---

## 7. Shared-layer changes this build requires

### 7.1 `data/shared/topography_codes.json` — the eye has one code and needs nine

`coarse_organ_crosswalk` currently holds `{"organ": "eye", "topography_range": "C69", "codes":
["C69.9"], "candidate_groups": [5], "label": "Eye"}`. **`C69.2` (retina), the topography Visser
Table 3 names for retinoblastoma, does not exist in the file.** A retinoblastoma at the retina
cannot reach Group V today. This is the same class of defect as the Group 4 `C48.2` fix — a
tumour that could never reach its own group.

Add all nine codes REDCap carries, with REDCap's own numeric values:

| ICD-O-3.2 | REDCap | Label (REDCap's own wording) |
|---|---|---|
| C69.0 | 690 | Conjunctiva |
| C69.1 | 691 | Cornea, NOS (Limbus of cornea) |
| **C69.2** | **692** | **Retina** |
| C69.3 | 693 | Choroid (Crystalline lens) |
| C69.4 | 694 | Ciliary body (Iris, Sclera, Uveal tract, Intraocular, Eyeball) |
| C69.5 | 695 | Lacrimal gland (Lacrimal duct, NOS, Nasal lacrimal duct, Nasolacrimal duct, Lacrimal sac) |
| C69.6 | 696 | Orbit, NOS (Autonomic nervous system of orbit, Connective tissue of orbit, Extraocular muscle, Peripheral nerves of orbit, Retrobulbar tissue, Soft tissue of orbit) |
| C69.8 | 698 | Overlapping lesion of eye and adnexa |
| C69.9 | 699 | Eye, NOS |

`candidate_groups`: `[5]` for C69.2 and C69.9; **`[5, 4]` for C69.4**, because intraocular
medulloepithelioma of the ciliary body is an ICCC-3 Group IV tumour (§5.3) and is a genuine
leukocoria mimic; `[5]` for the rest, with a note that orbital rhabdomyosarcoma (Group 9) and
ocular melanoma (Group 11) also live at C69 and will be added when those groups are built. Do not
invent candidate groups for tumours no built tree can receive.

⚠️ **`Topography Redcap.md` line 696 reads `So! tissue of orbit`** — ligature damage, the same
class of defect `docs/TODO.md` §1.3 already records elsewhere in that file. Write `Soft tissue of
orbit` in the JSON and add the line to the existing TODO item; do not propagate the corruption.

### 7.2 `data/shared/presentation_router.json`

- `groups["5"]` becomes `{"name": "Retinoblastoma", "built": true, "trees": [{"tree_id":
  "g5_retinoblastoma", "entry_node": "rb_document_inventory"}], "handoff": {"group": 5, "tree_id":
  "g5_retinoblastoma", "entry_node": "rb_document_inventory"}}`.
- No `tree_routing` and no `tree_selection`: one tree, no second question to ask.
- `site_to_group` already reads `"C69": [5]`. Leave it.
- The `organ_functional_sign` archetype already names leukocoria in its label and already lists
  group 5 in `candidate_groups`. Leave it.
- **No new `dual_group_rules` entry.** Group V's codes route nowhere else.

### 7.3 `docs/group_05_layer1_repair.md`

New, following `Group 3 — Layer 1 Repair Package (REDCap iii_morph).md` and the Group 4 equivalent.
One item: `9514` must be withdrawn from the `v_morph` option list, or the registrar must rule that
the registry registers spontaneously regressed retinoblastoma and say on what code. Until then the
option is selectable in REDCap and unreachable in the tool.

---

## 8. Validation rules this group adds

Every rule is proved with a **negative control**: break the data deliberately, confirm the check
FAILs, restore, confirm it passes. Key each check off **Layer 1**, never off a flag in the file
being checked. Record every control in `docs/validator_negative_controls.md` in the existing
format.

1. **`imaging_pathway` shape.** An `imaging_pathway` node must declare `insufficient_next_node` and
   must **not** declare `options[]`. `docs/TODO.md` §10 proposed this rule; three Group 3 nodes
   crash at runtime for want of it. Scope it to all groups — it is an engine fact, not a Group 5
   fact — and expect it to report the three Group 3 nodes. **They are on `main`, outside this
   branch: report them, do not fix them here.** If the rule FAILs on Group 3 and so breaks the
   build for files this branch does not own, emit WARN for groups other than 5 and FAIL for
   group 5, and say so in the check's docstring.
2. **`behaviour_exclusion` round-trip, extended to Group 5.** The Group 4 check exists; confirm it
   is group-agnostic and keys `icdo_code`/`icdo_behaviour`/`icdo_term` off `icdo32.sqlite`'s
   Preferred term. If it is hard-coded to Group 4, generalise it rather than forking it.
3. **No Group V terminal emits a code outside `{9510, 9511, 9512, 9513}`**, and **no terminal at
   basis 1 or basis 2 emits anything but `9510/3`** — Visser Table 3 (§0.4). This is the rule that
   would catch the most consequential possible error in this group: a specific subtype assigned on
   imaging alone.
4. **`9514` and `9510/0` appear nowhere as a `morphology_code`** in `group_05_dt.json` or as a
   `maps_to_morphology_codes` value in `aliases_group_05.json`. They may appear only inside a
   `behaviour_exclusion` block or in author-facing `notes`.
5. **`imaging_sufficient` is `true` on `9510` only** among Group V entries (§2.5).
6. **Every Group V entry has `ihc_markers_required: null`, `ihc_markers_exclude: null`, and the
   tree contains zero `ihc_checklist` nodes.** Pathway §7.2 asked whether the validator tolerates a
   group with no Stage-3 node. It must, and this check proves the group is authored that way on
   purpose rather than by omission.
7. **Every Group V entry has `code_neutral_molecular: true`** (§0.5, fact 3).

---

## 9. Clinical warnings

`clinical_alert` is `null` everywhere (§0.8). Material that is clinically consequential but not
code-changing goes to `docs/clinical-warnings.md`, in that file's existing format. For this group
it is unusually heavy, and three items are the reason the file exists:

1. **Biopsy of an intact globe is contraindicated** and can convert a curable tumour into fatal
   disease. A tool that lists "histology" as a routine option for an intact eye would be inviting
   it.
2. **High-risk histopathological features drive adjuvant chemotherapy and change no code.** Record
   each structure discretely rather than trusting a report's single "high risk: yes/no" label:
   thresholds differ by institution. Massive choroidal invasion is a focus **≥3 mm**; focal is
   **<3 mm** not reaching the sclera. Optic nerve invasion is graded prelaminar / laminar /
   retrolaminar / surgical margin. Of 27 experts across 16 countries surveyed by Kaliki S, et al.
   (*JAMA Ophthalmology* 2022;140(1):30–36), only three features were unanimous: post-laminar optic
   nerve invasion, optic-nerve transection-margin involvement, and extrascleral extension.
3. **Bilateral retinoblastoma with a pineal or suprasellar mass** is trilateral disease and needs a
   second tumour record in Group III (§4.2). A tool that codes the eye and stops loses the second
   primary.

Also recorded: severe anaplasia independently flags metastatic risk even with no standard high-risk
feature present (Mendoza 2015).

> ⚠️ **Two claims in the first draft of this section were wrong, and the papers were re-read to
> settle them (22 September 2026). Do not restore either.**
>
> **Chromosome 6p gain and extraocular spread.** The draft said 6p gain *"correlates with severe
> anaplasia and extraocular spread"*. Only the first half holds. Stålhammar G, et al.
> *Ophthalmology Science* 2022;2(1):100089, **p. 7**: *"The relative risk for extraocular spread in
> tumors with 6p **trended toward significance** at 6.7 (95% confidence interval, 0.9–52.2;
> P = 0.07)"* — and *"Neither severe anaplasia (P = 0.57), gain of 9q (P = 0.48), nor histologic
> high-risk features (P = 0.60) correlated to extraocular spread."* What is significant is shorter
> progression-free survival, P = 0.03. **The paper's own title and conclusion say "correlates
> with … extraocular spread" and its results do not support it.** Cite the result, not the title.
>
> **Aqueous-humour cell-free DNA.** The draft said it is used *"for prognostication, never for
> primary diagnosis"*. The paper does not confine it that way. Ghose N & Kaliki S, *Seminars in
> Ophthalmology* 2022;37(7–8):813–819, **p. 4**: *"it has been established that liquid biopsy from
> AH aids in **diagnosis**, prognostication, and treatment monitoring in RB."* What the same paper
> does say, **pp. 2–3**, is the contraindication this group is built on: *"direct tumor biopsy for
> genetic analysis and prognostication is an **absolute contraindication** at this point of time
> for the fear of extraocular tumor spread."* Aqueous paracentesis is the thing that is safe; the
> restriction is on cutting the tumour, not on what the fluid may be used for. This is why §4
> carries a cytology and liquid-biopsy route at basis 5 (§10.9) rather than treating every
> non-enucleation case as imaging-only.

---

## 10. The baseline document

Verified 22 September 2026 against PubMed, the open WHO Blue Books structure page and the
PubMed Central full text. The registrar's flag of 16 September 2026 — *"Milman 2023 is indexed by
PubMed as an Editorial with no abstract … usable as a pointer; thin as an authority"* — is half
right, and the half that is wrong matters.

### 10.1 Milman 2023 stands, and the reason it was doubted is not a reason

> **Milman T, Grossniklaus HE, Goldman-Levy G, Kivelä TT, Coupland SE, White VA, Mudhar HS,
> Eberhart CG, Verdijk RM, Heegaard S, Gill AJ, Jager MJ, Rodríguez-Reyes AA, Esmaeli B,
> Hodge JC, Cree IA.** *The 5th Edition of the World Health Organization Classification of Tumours
> of the Eye and Orbit.* Ocular Oncology and Pathology 2023;9(3–4):71–95.
> [10.1159/000530730](https://doi.org/10.1159/000530730) · PMID 37900189 · PMC10601864

- The **Editorial** tag is real — PubMed's structured metadata carries it and the Karger journal
  page prints it. It is not a PubMed indexing artefact.
- It is also not a measure of standing. The paper runs **25 pages** (71–95) against Louis 2021's
  21 (1231–1251), is organised by taxonomic chapter with *"ICD-O coding"* and *"ICD-11 coding"*
  subsections throughout, and is written by **the Eye and Orbit volume's own editorial board** —
  Milman, Grossniklaus, Kivelä, Coupland, Mudhar, Eberhart, Verdijk, Heegaard, Gill, Jager,
  Rodríguez-Reyes, Esmaeli and Hodge, with three IARC staff (Goldman-Levy, White, Cree). That is
  the same model as Louis 2021, which is the CNS volume's own editorial board and also includes
  Cree. Same genre of document, different journal tag.

**No better candidate exists.** A search for a further summary of Volume 13 returned nothing.

### 10.2 ⚠️ The real weakness, which nobody had flagged: a three-year beta gap

Milman 2023 states outright that it summarises a classification *"currently available online as a
**beta version ahead of print**"* (April 2023). The bound book — *WHO Classification of Tumours,
5th edition, Volume 13: Eye and Orbit Tumours*, IARC, ISBN 978-92-832-4546-9 — did not reach final
print until **23 January 2026**, thirty-three months later. Louis 2021 had no such gap; the CNS
volume and its summary were contemporaneous.

**No comparison of the 2023 beta against the 2026 final print exists in the open literature.**
Whether the retina chapter changed between them is **not established**, and only IARC or a copy of
the book can settle it. This is recorded as §11 item 7, not glossed.

### 10.2b ★ The paper is now held on disk, and it was read in full

**The registrar supplied it on 22 September 2026**, after §10.1 and §10.2 were written from PubMed
metadata and the open structure page. It is at
`Group 5 Papers/oop-2023-0009-03-4-530730.pdf`, 25 pages, and everything below §10.3 has been
re-derived from the primary text rather than from a summary of it.

**Cite it by table, not by page.** The copy held is the online-first version — received 15 March
2023, accepted 22 March 2023, published online 18 April 2023 — and is paginated **1–25**, not
71–95. Page numbers taken from this PDF will not match the citation. Every reference below names a
table.

**The two structural facts the full text settles:**

1. **The paper states no ICD-O code anywhere.** The string "ICD-O" occurs exactly **once** in
   twenty-five pages, as a subsection heading in Table 1's list of what a book entity section
   contains — never with a number beside it. The book has ICD-O coding blocks; this summary does
   not reproduce them.

   This is the same standing Group 4's baseline had, and the Group 4 contract §10.1 recorded it in
   the same words: the paper *"never states an ICD-O code anywhere… it corroborates that a current
   WHO entity lives on the stem; `icdo32.sqlite` states the number."* **A paper that prints no code
   cannot retire one.**

2. **Confirmed: it summarises a beta.** *"This review outlines the major general and specific
   changes in the WHO Eye5, which is currently available online as a beta version ahead of print"*,
   and its own reference 2 is *"Eye tumours [Internet; beta version ahead of print]… 2023. vol.
   13"* — with the chapter URL left unfilled as `chapters/??`. §10.2 stands unchanged.

### 10.3 What the classification lists under the retina — the finding that shapes §2.4

The open WHO Blue Books structure page and the PubMed Central full text of Milman 2023 were
checked independently and agree. **Table 9, *Tumours of the neurosensory retina*, lists four
entities and only four:**

> Astrocytic tumours · Nodular and massive retinal gliosis · **Retinocytoma** · **Retinoblastoma**

**"Retinoblastoma, differentiated", "retinoblastoma, undifferentiated" and "retinoblastoma,
diffuse" are not named entities in the WHO Eye and Orbit 5th edition.** The words do not appear as
subtype names anywhere in the summary. Current literature treats them as descriptors and not as
diagnoses: Nag A, Khetan V. *Retinoblastoma — a comprehensive review, update and recent advances.*
Indian Journal of Ophthalmology 2024;72(6):778–788, describes differentiation as a spectrum —
well, moderately, poorly differentiated or undifferentiated — and growth pattern separately as one
of four — endophytic, exophytic, mixed, diffuse infiltrating. Both are prognostic features of one
entity.

**★ What this does not settle — and the full text makes the reason precise.** Table 9 lists tumour
**types**. The paper's own **Table 2** defines three different things:

> **Type** (formerly "entity") — *"Separate entity in which multiple parameters … differ from those
> of other types"*
> **Subtype** (formerly "variant") — *"A variant of a tumor type in which one or two parameters …
> make it desirable to recognize it as being distinct from other subtypes but still related to the
> parent type"*
> **Pattern** — *"Morphologic or immunohistochemical pattern in a tumor, without distinct clinical,
> molecular, or prognostic parameters that make it desirable to be recognized as a subtype"*

And **Table 1** shows that *Subtypes* and *"Description of recognized histopathological subtypes"*
are subsections **inside an entity's own section** — not entries in the chapter's type list.

> **A subtype would not appear in Table 9 at all.**

So Table 9's silence proves that differentiated, undifferentiated and diffuse retinoblastoma are
**not separate types**. It says nothing whatever about whether they are **subtypes** carrying their
own ICD-O codes inside the Retinoblastoma entity section — which is the question the governing test
actually asks, and which needs the entity page the paywall still withholds. Growth pattern —
endophytic, exophytic, mixed, diffuse infiltrating — most likely sits at Table 2's third level,
*pattern*, below subtype; that would put `9513` in a different position from `9511` and `9512`, and
it is not established either.

The governing test is *a code leaves the decision tree only when no current WHO entity lives on its
stem.* Nothing read here shows that. A paper that prints no code cannot retire one (§10.2b).

So the three codes are **built, and reachable only from the pathology report's own stated grade or
growth pattern** (§2.4). That is the Group 4 D3 precedent on comparable evidence: ICD-O-3.2 prints
all three as live, non-obsolete Preferred terms (§0.3), all three are REDCap options, and what the
tool declines to do is *derive* them. Removing them on this evidence would repeat the error that
wrongly deleted `9430/3 Astroblastoma` and `9480/3` from Group 3. Registrar item §11 item 5, whose
wording is now narrower than when it was written: the question is **subtype or pattern**, not
*entity or nothing*.

### 10.4 Retinocytoma is premalignant to the World Health Organization and benign to IARC

Milman 2023: *"Retinocytoma is classified as a premalignant tumor, considering the genetic data
that these tumors carry biallelic RB1 mutations and clinical evidence that they can dedifferentiate
into retinoblastoma."*

ICD-O-3.2 codes it **`9510/0`** — behaviour 0, benign. Confirmed independently by Al-Hussaini M,
Al Sharie S, Sultan H, Mohammad M, Yousef YA. *Retinocytoma: understanding pathogenesis, diagnosis,
and treatment approaches.* International Journal of Retina and Vitreous 2025;11:20:
*"According to the International Classification of Diseases for Oncology (ICD-O), retinocytoma is
coded as 9510/0 (Retinocytoma, C69.2)… retinoblastoma that has spontaneously regressed is coded as
9514/1 (Retinoblastoma, spontaneously regressed, C69.2)."*

**The behaviour code is IARC's, not the World Health Organization's**, and the same reasoning the
Group 4 contract recorded at its §10.1b applies: a WHO word for a tumour's biology does not change
the digit ICD-O prints. The tool codes to ICD-O-3.2. Nobody should "fix" `9510/0` to `9510/1`.

But the divergence is real and it sharpens §11 item 3: the registry is being asked whether to hold
a lesion that IARC calls benign and the World Health Organization calls premalignant.

The same paper records a genuine terminological tension the pathway document did not: *"the term
retinoma was first coined by Gallie et al. to replace the older term 'spontaneously regressing
retinoblastoma'"*, with retinocytoma proposed later to parallel pineocytoma and pineoblastoma. So
`9510/0` and `9514/1` are two ICD-O stems for what much of the clinical and genetic literature now
treats as one biological entity. That is §11 item 6.

### 10.5 The paediatric volume is not the spine for this group

`docs/group_baseline_documents.md` §1 left open whether **Pfister SM, et al. Cancer Discovery
2022;12(2):331–355**, summarising the inaugural WHO Paediatric Tumours volume, is the better spine
for paediatric-site groups. **For Group V it is not, and the question can be closed.**

The complete open-access full text was retrieved and searched: the words *eye*, *ocular* and
*retina* do not appear anywhere in it. *Retinoblastoma* appears **exactly once**, inside a list of
cancer predisposition syndromes — *"predisposition to neural tumors, including neuroblastoma,
glioma, medulloblastoma, retinoblastoma, and rhabdoid tumors"*. There is no discussion of its
classification, its entities or its codes. Volume 7 reportedly contains an *Eye tumours* chapter
per bookseller listings — a secondary source — but Pfister's summary does not engage it.

This is worth recording beyond Group V: Pfister 2022 is Group IV's baseline and covers it well.
Its coverage is chapter-by-chapter and uneven, and the volume name matching the group name proved
nothing here. Check the fit before assuming it for Groups VI, VII and X.

### 10.6 No registry-implications paper, and the one that is coming

Confirmed again, by PubMed and by web search: **there is no Hoogendijk-equivalent for the Eye and
Orbit volume.** The earlier MeSH sweep recorded in `Group 5 Papers/Group 5 — Registry-Implications
MeSH Search Results.md` stands.

Two things fill the gap, one now and one later:

- **Now — Visser 2023, Table 3.** §0.4. For this group the cross-cutting layer does the job
  unusually well: it names the entity, the topography `C69.2`, the code `9510/3` and the basis.
  No other group gets that much from it.
- **Later — the International Collaboration on Cancer Reporting's *Ocular retinoblastoma*
  dataset**, in development explicitly *"in synchrony with"* the WHO Eye and Orbit 5th edition and
  chaired by Patricia Chévez-Barrios. Per the Collaboration's live *Upcoming Datasets* page, open
  consultation is expected **late 2026** and publication in the **first half of 2027** — a slip
  from the Q1/Q2 2026 dates its announcement of 30 January 2026 gave. When it publishes it will
  probably be this group's registry-implications document and should settle §10.3 explicitly.
  The already-published **Royal College of Pathologists dataset G055, *Dataset for
  histopathological reporting of ocular retinoblastoma* (2018)**, predates the volume entirely and
  is keyed to the AJCC staging of its own era.

### 10.7 No sixth edition, and one title that reads like one

No 6th-edition Eye and Orbit volume and no revision announcement. One adjacent paper is easy to
misread: **Giesen C, Goldman-Levy G, Cree IA, Cierco Jimenez R, Machado A, Lokuhetty D.** *WHO
Classification of Tumours: moving towards the sixth edition.* Histopathology 2024;86(6):839–844.
The title is forward-looking and the paper concerns the direction of the whole fourteen-volume
series. It is not an announcement of a sixth edition of anything.

### 10.9 Table 10, and why this group needs a cytology route

The baseline paper's **Table 10**, *Diagnostic cytology of tumours of the retina and
neuroepithelium*, is the WHO-level statement of the fact §0.5 rests on, and it is more precise than
the secondary sources the pathway document used. Verbatim, on retinoblastoma:

> *"Generally, biopsy is avoided due to the risk of extraocular recurrence and metastasis.
> Cytological samples often have pitfalls (sampling of retinal neurons, scant material) that may be
> misleading. Diagnostic features of malignancy such as necrosis, mitoses, and nuclear atypia
> should be present when diagnosing retinoblastoma in a cytology. Consultation with an experienced
> ophthalmic cytopathologist is recommended if a biopsy is considered."*

Read it carefully: **avoided, with conditions attached for when it is done** — not "never
happens". A retinoblastoma cytology is a real document that can arrive in a real file, and under
Visser 2023 it is **basis 5**, stronger than the imaging route's basis 2. Rule 8, p. 06 puts an
aqueous-humour or plasma liquid biopsy at **5 as well**, not 8, whenever no pathology is available.

Without a route for it the tool has two dishonest options and no honest one: force the case down
the imaging branch and understate the evidence at basis 2, or force it down the enucleation branch
and claim a specimen that does not exist. Hence `rb_cytology` in §4. It emits `9510/3` and never a
subtype — a cytology cannot grade differentiation or establish a growth pattern.

**Table 10 also gives the discriminator for the one mimic that is another built group's tumour.**
Of medulloepithelioma it says immunohistochemical staining *"expresses LIN28A and PAX8 …, which may
help distinguish these tumors from retinoblastoma"*. Medulloepithelioma of the ciliary body is in
Table 9 as a current entity, and ICCC-3 puts `9501`–`9504` outside the central nervous system in
**Group IV** (§5.3). C69.4 now carries candidate groups `[5, 4]` for exactly this reason (§7.1), and
Group IV's router default already routes it to `g4_other_peripheral`, whose `op_medulloepithelioma`
node is where such a case belongs. Any Group V branch naming medulloepithelioma refers to group 4
and may cite this table for the two markers.

### 10.8 The staging systems, and a citation the pathway document has wrong

The pathway document's §1E table cites *"Murphree (2005) IIRC"* with no page range for the
intraocular groups A–E. **Two different systems are routinely conflated under those letters:**

| System | Author, institution | Citation |
|---|---|---|
| **International Intraocular Retinoblastoma Classification** | A. Linn Murphree, Children's Hospital Los Angeles | Murphree AL. *Intraocular retinoblastoma: the case for a new group classification.* Ophthalmology Clinics of North America 2005;18(1):41–53, viii. [10.1016/j.ohc.2004.11.003](https://doi.org/10.1016/j.ohc.2004.11.003) · PMID 15763190 |
| **International Classification of Retinoblastoma** | Carol Shields and colleagues, Wills Eye Hospital, 2006 | a later modification with **materially different group E criteria** |

They are not interchangeable: a tumour filling more than half the globe with no destructive
features is group E under one and group B to D under the other depending on seeding.

**This costs the build nothing** — neither system changes a morphology code, and the tool records
no intraocular group. It costs the pathway document a correction, and it is §11 item 8.

**AJCC pathologic staging:** the **8th edition** (Mallipatna A, Gallie BL, Chévez-Barrios P, et al.,
*Retinoblastoma* chapter, AJCC Cancer Staging Manual, 8th edition, Springer, 2017) remains in force.
AJCC version 9 has published no retinoblastoma chapter; its rollout so far covers selected head and
neck sites, lung, anal and appendiceal neuroendocrine tumours. The College of American Pathologists
protocol the pathway document rests on is keyed to the 8th edition and is current.

---

## 11. What needs the registrar

Recorded, not resolved. The build proceeds around each of these.

1. **`9514` is a selectable REDCap option the tool cannot emit** (§1.1, §7.3). Withdraw the option,
   or rule that the registry registers spontaneously regressed retinoblastoma and say on what code.
2. **Is a regressed retinoblastoma an incident case?** (§2.2). A registration-rules question, not a
   morphology one.
3. **Is a pure retinocytoma registrable anywhere?** (§2.1). ICCC-3 registers no benign eye tumour;
   `9510/0` has no group. The parallel is Group 4's ganglioneuroma, ruled D1 on 16 September 2026.
4. **The baseline is settled and needs ratifying, not deciding** (§10.1, §10.5). Milman 2023 stands;
   the WHO Paediatric Tumours volume does not cover this group and its summary paper mentions
   retinoblastoma once, in a list. The open structural question in
   `docs/group_baseline_documents.md` §1 can be closed for Group V. Worth ratifying, because the
   same file's provisional flag on this entry should come off.
5. **★ Do `9511/3`, `9512/3` and `9513/3` still carry a World Health Organization entity?** (§10.3).
   The Eye and Orbit 5th edition names one entity, *Retinoblastoma*, not three subtypes. The entity
   page that would say whether its coding block still prints the three numbers is paywalled and was
   not read. **This is the single ruling that most changes what the tree contains.** Built and
   report-wording-only in the meantime, which is the conservative reading of the governing test.
6. **Are `9510/0` retinocytoma and `9514/1` spontaneously regressed retinoblastoma one entity or
   two?** (§10.4). ICD-O-3.2 keeps two stems; much of the clinical and genetic literature treats
   them as historically overlapping names for one lesion.
7. **Did the retina chapter change between the 2023 beta and the January 2026 final print?**
   (§10.2). Thirty-three months apart, no published comparison. Only IARC or the book can say.
8. **Which intraocular classification does the pathway document mean by "Murphree 2005"?**
   (§10.8) — the International Intraocular Retinoblastoma Classification, which is Murphree's own
   paper, or the International Classification of Retinoblastoma, which is Shields 2006 and has
   different group E criteria. A documentation correction; it changes no code.
9. **Revisit when the International Collaboration on Cancer Reporting publishes its *Ocular
   retinoblastoma* dataset** (§10.6), projected first half of 2027. It is being built in synchrony
   with the volume and should answer item 5 explicitly.

---

*Group 5 build contract. Written before the tree, as the Group 3 method requires. Every code in
§0.2 was verified against `icdo32.sqlite` and the four IARC 3.1→3.2 change documents on
22 September 2026; every ICCC-3 assignment against `ICCC-2017.sqlite` the same day.*
