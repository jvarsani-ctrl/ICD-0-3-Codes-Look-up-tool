# Group 3 build contract — CNS and Miscellaneous Intracranial and Intraspinal Neoplasms

**2026-09-14.** The single spec every Group 3 build task works from. It exists because six
trees, an engine change, a validator change and an alias file are being authored in parallel
and they must agree on the schema before any of them is written.

**Authority, in order:**

1. `ICD Look Up tool/Group 3 — CNS and Miscellaneous Intracranial and Intraspinal Neoplasms — Diagnostic Pathway (Revision 2).md` — the clinical and structural source of truth. Part 6 is the implementation spec.
2. `ICD Look Up tool/Decision tree JSON Build — Master Instruction File.md` — the base schema.
3. `ICD Look Up tool/memory/*.md` — locked decisions. `registrar-rulings.md` binds.
4. This file — where 1–3 need reconciling for Group 3, the reconciliation is written here.

**Superseded, do not use:** `Group 3 — CNS And Miscellaneous Intracranial And Intraspinal
Neoplasms Diagnostic Pathway.md` (the 2026-05-05 revision). Revision 2 §0.2 lists 28 substantive
corrections to it, nine of them BLOCKING code-identity errors. Reading it will produce wrong codes.

---

## 0. The rule that governs the whole build

**Group III is not Group I or Group II with different codes. Do not copy their tree shapes.**

Groups 1 and 2 key their trees to histological families. Revision 2 §6.3 rules that wrong for
this group and says why: CNS5 defines ependymoma *by anatomical compartment*, ICCC-3 splits
`9380` and gates `8158`/`8290`/`9501`–`9504`/`8000`–`8005` by topography, and the paediatric
posterior fossa differential is a compartment differential before it is a histological one.
Compartment is also known at Stage 1, before any histology — so the router can hand off without
asking the clerk an extra question.

Group III also carries three things no other group has, and each changes the shape of a node:

- **A two-track output.** For much of this group there is no code to emit for the diagnosis the
  pathologist actually reached. The code and the rendered diagnosis are separate outputs (§2).
- **A resource-level gate.** Whether a branch is askable at all depends on the laboratory's
  capability *for that tumour family*, not on the site as a whole.
- **Grade as its own decision.** A molecular finding can set a grade with no histological change,
  and grade is not derivable from the code.

Anything that looks like a Group 1 or Group 2 idiom should be checked against Revision 2 before
it is written. Where they conflict, Revision 2 governs for this group.

---

## 1. The inventory is generated, never transcribed

`build/generate_group03_inventory.py` joins `ICCC-2017.sqlite` to `icdo32.sqlite` and emits every
`(code, behaviour)` Group III can carry. Run it; build `morphology_entries[]` from its output.

```
python3 build/generate_group03_inventory.py --out <scratch>/g3_inventory.json
```

Verified output, which reproduces Revision 2 §1.1 exactly:

| | |
|---|---|
| ICCC-3 code-range entries | 104 |
| Distinct codes | 103 |
| Absent from ICD-O-3.2 | **16** — `8274`–`8279`, `9402`–`9409`, `9422`, `9536` |
| Usable codes | **87** |
| `(code, behaviour)` records | 109, of which `9380/3` appears twice (two subgroups, one pair) |
| **`morphology_entries[]` target** | **108** |
| Behaviour declaration | `0-1,3` — exactly one across every Group III range |

### 1.1 Layer 1 for this group is ICD-O-3.2, not the REDCap option file

Revision 2 §1.1b, and it is a scope *reduction*. The REDCap registry and this tool are separate
projects. `icdo32.sqlite` is authoritative for code identity, term strings and behaviour;
`ICCC-2017.sqlite` for subgroup, topography constraint and behaviour range.

Consequences, all verified against the two databases on 2026-09-14:

- **`9476` is the only Group III code absent from the REDCap option list.** It is built anyway
  (ruling 3), declares `awaiting_layer1`, and gets an entry in `docs/codes-awaiting-redcap.md`.
- **Seven codes the option list offers are not usable Group III codes** — `8274`–`8279`, `9536`.
  They do not exist in ICD-O-3.2. They must appear nowhere in the JSON, in any alias *target*,
  or in any example (§6.6 rule 7). They are alias *inputs* only.
- **15 preferred terms the tool emits are not in circulation** among abstractors. The tool emits
  them regardless; they are listed in Revision 2 §1.1b so the alias file does not assume an
  abstractor has seen them.

### 1.2 Behaviour-overloaded codes — 18 of them

`9390`, `9391`, `9442`, `9501`, `9502`, `9505`, `9530`, `9538`, `9539`, `8000`, `8001`, `8005`,
`8270`, `8272`, `8280`, `8281`, `8290`, `8300`. One `morphology_entries[]` object per behaviour,
each with its own explicit `behavior_code` and its own ICD-O-3.2 preferred term. Most carry a
benign term at `/0`–`/1` against a carcinoma at `/3`; a table printing only the lowest behaviour
reads "adenoma" where the data says "carcinoma".

**`8000` is authored at `/0`, `/1` and `/3` only.** `/6` and `/9` exist in ICD-O-3.2 but fall
outside the group's `0-1,3` declaration, so a case carrying them leaves Group III silently.
Metastatic disease is handled at Stage 1 — code the primary, not the biopsy site.

### 1.3 `9380` — the one intra-group topography split, and the field it needs

ICCC-3 puts `9380/3` in **IIIb at C72.3** and **IIId2 at C70.0–C72.2, C72.4–C72.9, C75.1, C75.3**.
That is one `(code, behaviour)` pair with two subgroups, and the schema allows only one entry per
pair — `check_duplicate_code_behavior_pairs` FAILs on two, and `renderOutput()` reads
`iccc3_subgroup_id` straight off the entry.

**Resolution — one new group-agnostic field, `iccc3_subgroup_by_topography[]`:**

```json
"iccc3_subgroup_id": "IIId2",
"iccc3_subgroup_name": "Mixed and unspecified gliomas",
"iccc3_subgroup_by_topography": [
  { "topography_in": ["C72.3"],
    "iccc3_subgroup_id": "IIIb",
    "iccc3_subgroup_name": "Astrocytomas" }
],
"topography_dependent": true,
"topography_routing_note": "ICCC-3 routes 9380 to IIIb at C72.3 (optic nerve) and to IIId2 at every other CNS site. The entry's own subgroup is the default (IIId2, the larger destination); the rule above overrides it when the captured topography is C72.3."
```

Ordered rules, first match wins, the entry's own `iccc3_subgroup_id` as the default — the same
shape `dual_group_rules` already uses in the router, applied intra-group. The engine resolves it
against captured topography at output time.

> ⚠️ **FOR THE REGISTRAR.** This field is not in Revision 2. It is forced by the schema: §1.1
> lists `9380` under two subgroups and §6.6 rule 6 forbids duplicate pairs. The alternative —
> pinning `9380` to IIId2 and accepting that an optic nerve glioma reports the wrong subgroup —
> is silently wrong for exactly the cases IIIb exists to catch. Flagged, built, reversible.

---

## 2. The six new fields (Revision 2 §6.2)

**No new node type.** The closed vocabulary of DT master §3A is unchanged. All six are *fields*,
exactly as Group 1's six and Group 2's five were. The engine supports them; only
`group_03_dt.json` uses them; no other group is obliged to adopt them.

### (1) `diagnosis_rendering` — the two-track output

On a code-emitting branch or a terminal.

```json
"diagnosis_rendering": {
  "track": "adaptr_descriptive",
  "who_diagnosis": null,
  "descriptive_diagnosis": "ST ependymoma, NOS",
  "suffix": "nos",
  "grade_system": "roman",
  "grade": "III",
  "comment": "Morphology and basic IHC are consistent with a supratentorial ependymoma. ZFTA and YAP1 fusion status could not be determined."
}
```

- `track` — `who_cns5` | `adaptr_descriptive`. Required.
- `who_cns5` requires `who_diagnosis` non-null, `grade_system: "arabic"`, `descriptive_diagnosis: null`, `comment: null`.
- `adaptr_descriptive` requires `descriptive_diagnosis` non-null, `grade_system: "roman"`, `who_diagnosis: null`, `comment` non-null.
- `suffix` — `nos` | `nec` | `none`. **`nec` only on a branch that also asserts an adequate
  result was obtained.** A registry that cannot do the test can never legitimately emit NEC.
- `grade` — a string, or `null`. Never `"NA"`, never `""`.
- Arabic set includes **1** (CNS5 Table 3 grades MVNT, PLNTY, meningioma and diffuse astrocytoma
  MYB/MYBL1-altered at 1). Roman set is **II, III, IV** only.
- Orthogonal to `nos_fallback`: that names the **code** to fall back to, this names **what the
  report says**. A branch may carry both.

### (2) `resource_level_gate` — availability as reachability

```json
"resource_level_gate": {
  "family": "ependymal",
  "required_rl": "IV",
  "tier": "highly_recommended",
  "referral_tier": "highly_recommended",
  "unreachable_destination": { "morphology_code": "9391", "behavior_code": "3" }
}
```

- `family` is **required** — RL is computed per tumour family, never per site. A laboratory with
  GFAP, synaptophysin and INI1 is RL III for AT/RT and RL II for ependymoma. Family vocabulary:
  `ependymal`, `embryonal`, `diffuse_glial`, `glioneuronal`, `meningothelial`, `sellar`,
  `pineal`, `choroid_plexus`, `pituitary`, `unspecified`.
- `required_rl` — `I` | `II` | `III` | `IV` | `V`.
- `tier` / `referral_tier` — `can_be_considered` | `highly_recommended` | `obligatory`.
  **`obligatory` must never be authored on an ependymal-family node** — Satgunaseelan uses only
  the first two tiers and a three-value enum mis-renders every ependymal node.
- **Unavailability follows from a declared site profile, never from the required level.**
  *(Corrected 14 September 2026 — the rule here previously said the opposite.)* A site declared
  resource level V MEETS a requirement of resource level V; reaching the last rung is not sitting
  above it. So `required_rl: "V"` is not evidence that any laboratory cannot run the test, and
  with no site profile the honest output is **not established**, not *unavailable*. The old rule
  forced all 14 resource level V branches in Group 3 down their `unreachable_destination`, which
  discarded the WHO CNS5 diagnosis the clerk had just evidenced and printed "the test is
  unavailable" over it. It also built the tool around one kind of laboratory, which this tool is
  not: a site at the top of the scale is as ordinary a case as one at the bottom. The flag that
  policed it, `upgrade_line_says_unavailable`, is now **banned** and the build FAILs on it.
- `unreachable_destination` is still required on every gate. It is what a site whose **declared**
  level is below the requirement resolves to.
- Where the family has no ADAPTR paper (meningioma, germ cell, pineal, choroid plexus,
  craniopharyngioma, pituitary, glioneuronal, and the paediatric-type diffuse gliomas), add
  `"rl_assignment": "by_analogy"`. Do not present it as sourced.

### (3) `entity_annotation` — the WHO CNS5 entity, recorded without a code

```json
"entity_annotation": {
  "who_cns5_entity": "Posterior fossa ependymoma, group PFA",
  "code_status": "shares_code",
  "shared_with": ["Posterior fossa ependymoma, group PFB", "..."],
  "evidence": "H3 K27me3 loss (>80% of cells negative)",
  "provisional": false
}
```

- `code_status` — `shares_code` | `no_code` | `own_code` (`own_code` replaced `awaiting_layer1` on 4 October 2026: the tool does not verify REDCap, standing rule 16).
- `no_code` covers the CNS5 entities with no ICD-O-3.2 code at all: PLNTY, MVNT, DLGNT, DGONC,
  CNS neuroblastoma FOXR2-activated, CNS tumour with BCOR ITD, HGAP, infant-type hemispheric
  glioma, diffuse hemispheric glioma H3 G34-mutant, diffuse astrocytoma MYB/MYBL1-altered,
  diffuse low-grade glioma MAPK pathway-altered, diffuse paediatric-type HGG H3-/IDH-wildtype,
  myxoid glioneuronal tumour, desmoplastic myxoid tumour of the pineal region SMARCB1-mutant,
  pineal anlage tumour, and the three cIMPACT-NOW update 11 NEC labels.
- `who_cns5_entity` must match **CNS5 Table 1's** spelling. CNS5 is internally inconsistent
  (Table 2 punctuates the paediatric-type HGG name differently; Table 7 prints `FET-CREB fusion
  positive` against the prose's `fusion-positive`). Table 1 wins.
- **The string `(provisional type)` is an extraction artefact of the source's italics. It must
  never appear inside an entity name.** Use `"provisional": true` instead.

### (4) `grade_resolution` — grade as its own decision

Modelled on Group 2's `behaviour_resolution`, resolving a grade instead.

```json
"grade_resolution": {
  "criterion": "CDKN2A/B homozygous deletion in an IDH-mutant astrocytoma",
  "variable": "cdkn2a_status",
  "detection_method_required": ["Cytogenetics/FISH", "Molecular/PCR"],
  "values": {
    "homozygous_deletion":  { "grade": "4", "grade_system": "arabic" },
    "hemizygous_or_absent": { "grade": null, "reason": "Hemizygous deletion is explicitly excluded by cIMPACT-NOW update 12." }
  },
  "unresolved": { "grade": null, "defer_to": "histological_grade" }
}
```

- **`unresolved` must never invent a grade.** Where grade cannot be established it is omitted —
  which is exactly what update 8 requires for untested brain-invasive meningioma.
- **The numeral system follows the track, never the evidence type.** A grade reached on histology
  alone is Arabic whenever the diagnosis is a WHO CNS5 diagnosis. CNS5 grades meningioma and
  subependymoma histologically and both are Track A. Getting this backwards fails validation
  rule 1 on the two commonest histology-only branches in the group.

### (5) `basis_of_diagnosis` — computed, ENCR

Derived from the evidence gate as the **highest** of codes 1–8; `0` and `9` override.
**Codes 3 and 6 do not exist.** Valid set: `{0,1,2,4,5,7,8,9}`.

| Code | Means |
|---|---|
| 0 | Death certificate only |
| 1 | Clinical — physical examination only |
| 2 | Clinical investigation — imaging, endoscopy, exploratory surgery, autopsy, **without tissue** |
| 4 | Specific tumour markers |
| 5 | Cytology — including flow cytometry and liquid biopsy, **not** 8 |
| 7 | Histology |
| 8 | Cytogenetic/molecular, **specific to that cancer** |
| 9 | Unknown |

Two gaps ENCR leaves, declared rather than inferred: `"ihc_counts_as": 7`,
`"methylation_counts_as": 8`.

**No Group III terminal may emit basis code 1** — every CNS row in ENCR Table 3 is basis 2.

Keep it separate from `confidence`. ENCR says a registry may *register* on imaging; it does not
say the tool may assign that code with high confidence.

### (6) `diversion_criteria[]` — on `imaging_pathway`

Features that force the tissue branch even when the imaging constellation is met. Modelled on
the existing `biochemical_questions[]` pattern.

```json
"diversion_criteria": [
  { "feature": "Age under 3 years", "reason": "Favours an infant-type or embryonal tumour." },
  { "feature": "Symptom duration of 6 months or more", "reason": "Atypical for DIPG; consider angiocentric glioma or a MYB/MYBL1-altered tumour." }
],
"endpoint_verification": "not_verified",
"no_tissue": true
```

Any diversion feature ticked routes to the tissue branch, whatever the constellation says.

### (7) Amendment to `numeric_gate.bands[]` — `unit` is now required

This group states mitotic thresholds in five incompatible units: `≥4 mitoses in 10 HPF of
0.16 mm²`, `≥2.5 mitoses/mm²`, `≥2 mitoses/10 HPF (0.23 mm²)`, `≥3 mitoses/2.4 mm²`,
`<1 mitosis/20 HPF`. An HPF is not a fixed area. **A band list without a denominator is a build
error.**

`unit` ∈ `per_mm2` | `per_10_hpf` | `per_hpf` | `percent`. Where the source states an HPF area,
carry `hpf_area_mm2`. The existing domain-sweep rule then runs **per unit**.

---

## 3. Tree architecture — six trees, keyed by compartment

`metadata.decision_trees` lists all six. Each begins at its own `document_inventory`.
Node IDs are tree-prefixed and globally unique across the file.

| `tree_id` | Node prefix | Topography it owns | Dominant differential |
|---|---|---|---|
| `g3_posterior_fossa` | `pf_` | C71.6, C71.7 | Medulloblastoma · PF ependymoma · pilocytic astrocytoma · AT/RT · diffuse midline glioma |
| `g3_supratentorial` | `st_` | C71.0–C71.5, C71.8 | Paediatric-type diffuse gliomas · glioneuronal · ST ependymoma · choroid plexus · CNS embryonal |
| `g3_midline` | `md_` | C72.2, C72.3, C72.4, C72.5, C75.1, C75.2, C75.3 | Craniopharyngioma · pituitary · pineal · germ cell exclusion · optic pathway glioma · cranial nerve lesions |
| `g3_spinal` | `sp_` | C72.0, C72.1 | Myxopapillary and MYCN-amplified ependymoma · spinal pilocytic astrocytoma vs DLGNT |
| `g3_meninges` | `mn_` | C70.0, C70.1, C70.9 | Meningioma · solitary fibrous tumour · melanocytic |
| `g3_unspecified` | `un_` | C71.9, C72.8, C72.9, C80.9 | IIIf, with the five-point flag |

**The map must be total and disjoint, and that is a validation rule.** Sweep every topography
code the group can carry — C70.0–C70.9, C71.0–C71.9, C72.0–C72.9, C75.1–C75.3, C80.9 — and
assert each resolves to exactly one tree. Revision 2 records that the first draft of this table
assigned C72.9 to two trees and left C72.2, C72.4 and C72.5 unrouted; both faults are invisible
until a case hits them, and a duplicate silently picks whichever row the engine reads first.

`g3_unspecified` is reachable from **every** tree as the terminal for an inadequate specimen or
an unestablished site. The router picks the tree from the topography already captured at
Stage 1 — **no extra question is asked of the clerk.**

---

## 4. Process steps this group adds

Revision 2 Part 3. The Design Specification's Stage 0 → 5 model holds; these are additions.

**Specimen adequacy** (§3.3) — a second question on `document_inventory`, expressed with the
existing `test_result_states` construct, whose closed set already contains `adequate` and
`inadequate`. The rule that construct already carries applies: **no branch may treat
`not_assessable` identically to `negative`.** A failed stain is not a negative stain and a
crush-artefact biopsy is not a negative biopsy. An inadequate specimen resolves to the group NOS
code with a `provisional_pending` naming re-biopsy, and to **basis 2, not 7** — the tissue did
not yield a diagnosis.

**Intraoperative diagnosis** (§3.4) — frozen section and squash cytology are RL I and are often
the only neuropathology available within the surgical episode. Two rules: an intraoperative
diagnosis is **never the coded diagnosis**, it routes to the definitive-histology node; and where
no definitive histology ever follows, it stands as **cytology, basis 5**, code capped at NOS,
confidence low. It must not be silently promoted to basis 7.

**The AFP / β-hCG rule** (§3.2) — one-directional. **Elevated → refer to Group X and stop.
Normal → proceed to tissue, with germ cell tumour still live in the differential.** A normal
result excludes nothing. β-hCG is higher in CSF (≥8.2 IU/L, sensitivity 47%); αFP is higher in
serum (≥25 ng/mL). Never apply one compartment's cut-off to the other. Capture the number, not
a yes/no — one control craniopharyngioma reached CSF β-hCG of 8 against a cut-off of 8.2.

> **Cut-offs changed, registrar's ruling of 6 October 2026.** The `md_gct_*` gates now read the
> SIOP cut-offs, the same in serum and cerebrospinal fluid: alpha-fetoprotein above 25 ng/mL and
> β-hCG above 50 IU/L, "above" being strict (SIOP CNS GCT 96, Calaminus 2017, Methods; SIOP CNS
> GCT II, Calaminus 2026, Table 2). They replace the Hu 2016 values above (serum αFP ≥ 25, CSF αFP
> ≥ 3.8 ng/mL; serum β-hCG ≥ 2.5, CSF β-hCG ≥ 8.2 IU/L), which separate any intracranial germ cell
> tumour from a non-germ-cell lesion rather than germinoma from a non-germinomatous tumour. The rule
> stays one-directional and the routing is unchanged. Evidence and the trace of a β-hCG of 20 IU/L:
> `docs/group_10_registrar_review.md` E6. Check: `check_brain_marker_cutoffs`; controls:
> `build/negative_controls_group03.py`.

**The two imaging-only endpoints** (§3.5) — keep both, gate both, and **do not give them the
same confidence.**

- **NF1 optic pathway glioma** — 100% first-round consensus. Gated four ways: NF1 established by
  the Legius 2021 criteria; imaging typical; confidence below histologically-confirmed; an
  NF1-screening flag so these cases can be analysed separately. Emits `9421/1` at C72.3.
- **DIPG** — κ = 0.297 interobserver agreement and an explicit statement that it does not meet
  the standard-of-care threshold. A **flagged, lower-confidence, non-verified terminal, never the
  default.** Emits `9440/3`, basis 2, confidence low, `no_tissue: true`, with the six diversion
  criteria of §6.2(6).

---

## 5. Reconciliations — where the base rules and Revision 2 need a ruling

### 5.1 Clinical alerts stay out of the JSON

Revision 2 §6.4 tabulates 18 Group III alerts. **Registrar ruling 9 (4 Sep 2026) stands:** this
is a coding tool, not a clinical one. `check_no_clinical_alerts` FAILs the build if any
`clinical_alert` carries text.

So: `clinical_alert` is `null` everywhere in `group_03_dt.json`, and all 18 strings go into
`docs/clinical-warnings.md` under a Group III heading, in the same format the 302 existing
strings use — each with the exact place it came from, so it can be put back when the tool takes
on a clinical role. Nothing is lost.

Where an alert carries information the clerk **must act on to code correctly**, that information
belongs in `question`, `hint`, or the branch's own `label` or `reason` — never in `coding_note`,
which is author-facing and is not displayed.

### 5.2 The exact-string check is keyed to ICD-O-3.2 for this group

`check_redcap_exact_names` currently requires `morphology_name` to be character-identical to the
REDCap option string. Revision 2 §6.6 rule 13 supersedes that for Group 3 with a **stronger**
check: every `(morphology_code, morphology_name, behavior_code)` triple the engine can emit must
exist verbatim in `icdo32.sqlite`.

It is stronger because it catches the 28 invalid `(code, term)` pairs currently in circulation
rather than inheriting them. Option-list strings belong in the **alias** file, checked the other
way: every alias must resolve to a valid triple, and **no alias may be emitted**.

Groups 1 and 2 keep their current behaviour exactly — this must not regress them.

### 5.3 `9475`'s spelling exemption — raised, then retired

**Superseded 14 September 2026. There are now no name exemptions in Group 3.**

The 2019 draft workbook `ICD-O-3.2_MFin_17042019_web.xls` printed `Medullobloastoma,
WNT-activated, NOS`. Revision 2 §8.2 decision 3 handled it by displaying the corrected spelling,
keeping the exact source string in `source_term`, and running the round-trip check against
`source_term` — an exemption that named its anchor so it would collapse the moment the anchor
drifted.

IARC's **final** ICD-O-3.2 workbook, `ICD-O-3.2_final_update09102020.xls` (9 October 2020),
spells it correctly. Rebuilding Layer 1 against that file collapsed the exemption exactly as
designed: the build FAILed with *"THE EXEMPTION HAS COLLAPSED — its anchor is that ICD-O-3.2
carries 'Medullobloastoma, WNT-activated, NOS' for 9475/3, and it does not"* rather than passing
quietly. The exemption and the `source_term` anchor were then removed, and
`ICDO32_SOURCE_TERM_EXEMPTIONS` in `build/build_database.py` is now empty.

Every Group 3 `morphology_name` round-trips against `icdo32.sqlite` unaided.

**Layer 1 is the final workbook**, not the draft. Eleven of the 87 Group 3 codes differed between
the two — all of them spelling normalisations and `, NOS` suffixes, no code, behaviour or `[obs]`
change: `9350`, `9380`, `9395`, `9396`, `9400`, `9401`, `9411`, `9424`, `9471`, `9475`, `9582`.

### 5.4 Two strings whose exact spelling is load-bearing

- **`Medulloblastoma, SHH activated, NOS`** (`9471/3`, Related) — **no hyphen in "SHH activated"**,
  where the sibling term `Medulloblastoma, SHH-activated and TP53-wildtype` on the same code has
  one. Reproduce exactly.
- ICD-O-3.2 uses **`tumor`**, never `tumour`, in every term string. The prose of Revision 2 uses
  British spelling; the code strings do not.

### 5.5 `9476` is built ahead of REDCap

Ruling 3. It declares `awaiting_layer1` and gets an entry in `docs/codes-awaiting-redcap.md`
following the format the three Group 2 entries use. It is the only such code in this group.

---

## 6. Validation rules (Revision 2 §6.6) — all fourteen

Added to `build/build_database.py` alongside the existing checks. Every one gets a **negative
control**: break the data deliberately, confirm the check FAILs, restore, confirm it passes.
Record the controls in `docs/validator_negative_controls.md` in the format already used there.

1. **Numeral invariant.** `track == "who_cns5"` ⟺ `grade_system == "arabic"`.
2. **NEC gate.** No branch emits `suffix: "nec"` unless the same branch asserts an adequate result.
3. **Tier enum by family.** No ependymal-family node carries `tier: "obligatory"`.
4. **Unit on every numeric gate.** Domain sweep runs per unit.
5. **Entity strings** match the transcribed CNS5 Table 1 reference list, not recall.
6. **Behaviour split.** The 18 codes of §1.2 each appear as separate entries with explicit `behavior_code`.
7. **Non-existent codes.** `9402`–`9409`, `9422`, `8274`–`8279`, `9536` appear nowhere — not in
   the JSON, not as an alias target, not in an example.
8. **Anchor every name check to `icdo32.sqlite`, never to a flag in the file being checked.**
   No flag exempts a name. The one exemption (§5.3) names its `source_term` anchor.
9. **Grade resolution.** `unresolved` never carries a non-null `grade`. Every `values` entry names
   either a grade with its `grade_system`, or `null` with a `reason`. `"NA"` and `""` are errors.
10. **Basis of diagnosis** ∈ `{0,1,2,4,5,7,8,9}`; 3 and 6 rejected; 0 and 9 override; no Group III
    terminal emits 1.
11. **Imaging terminals.** Every terminal reached through an `imaging_pathway` without histology
    carries `no_tissue: true`, `endpoint_verification: "not_verified"`, `basis_of_diagnosis: 2`,
    and a **non-empty** `diversion_criteria[]`. An empty diversion list is a build error.
12. **Topography map is total and disjoint** (§3).
13. **ICD-O-3.2 round-trip** (§5.2).
14. **Negative controls** for all of the above.

### Checks already in the pipeline that Group 3 must satisfy

The build auto-discovers `data/database/group_*_dt.json`, so **every existing check runs against
Group 3 the moment the file lands.** The ones that will bite:

- `check_no_clinical_alerts` — see §5.1.
- `check_flow_charts` — every `ihc_checklist` carries a `branch_sequence` induced by
  `build/induce_flow.py`, and **every rule needs a witness**: an answer vector under which it,
  and no earlier rule, matches. Rerun `induce_flow.py` after editing any `resolution_logic`.
- `check_nos_fallback_by_node_type` — non-null for `ihc_checklist`, `cytogenetics_dropdown`,
  `molecular_freetext`, `numeric_gate`; **null** for `document_inventory`, `clinical_alias`,
  `morphology_only`, `imaging_pathway`, `histology_subclassification`, `site_resolution`.
- `check_satisfies_tests` — values come from the closed vocabulary and must appear in the terminal
  code's own `diagnostic_tests_required`. It suppresses an outstanding-workup row, so it is the
  one field that can make a case look better evidenced than it is.
- `check_refer_terminals` — clerk-facing text in `reason`, never `coding_note`.
- `check_metadata_counts`, `check_orphan_nodes`, `check_node_ids_unique_and_prefixed`.

---

## 7. Build order

Parts are built **in full** before anything is validated. Validating between trees on Group 1
produced 132, then 88, then 4 failures that were all "a later tree does not exist yet" and
cleared on their own.

1. `build/generate_group03_inventory.py` — done.
2. This contract — done.
3. `morphology_entries[]` — all 108, one pass.
4. Engine + validator support for the seven fields.
5. The six trees.
6. Router registration.
7. `aliases_group_03.json`.
8. Docs — clinical warnings, codes awaiting REDCap, negative controls.
9. **Then verify once:** `induce_flow.py` → `build_database.py` → negative controls → drive the
   tool in a browser.

**A green build is not a working tool.** Group 2 passed 74 checks, 10 of 10 data-level traversals
and 102 engine assertions while 15 of its 61 nodes did not render at all. Every automated layer
tested the data or the renderer in isolation; the fault was in the seam between them. Step 9's
browser pass is not optional.
