# Acute tree: ask the morphology first, fall back to it when no marker defines a lineage

Registrar's direction, 14 October 2026. Approved by the registrar on 14 October 2026 ("Go ahead and build"), with the Burkitt addition in section 4.5. Built the same day; results in section 11.

## 1. Purpose

The acute tree's last lineage screen, `ac_alal_resolve` ("Panel adequacy"), asks the clerk what the flow panel covered, after the clerk has already entered the markers. When one marker was entered, its first two answers (a comprehensive panel with at most one marker per lineage, or two or more markers of one lineage) cannot be true, and the engine cannot check them: a marker never added reads as negative or not done (ruling 11). All three panel answers end at the same code, 9801; only the annotation differs.

The registrar's replacement: ask what the blood film, marrow aspirate or trephine report describes, before the lineage markers. If the markers define a lineage, they set the diagnosis. If they do not, or none was entered, the case reverts to what the morphology report says and takes the closest diagnosis.

## 2. Decisions already made

| Decision | Source |
|---|---|
| Markers that define a lineage override the morphology, even when they disagree | registrar, 14 Oct 2026 (by the stated rule; confirm in review) |
| Closest diagnosis per morphology answer is the one `ac_morphology_only` already gives | same |
| Scope is the acute tree; other trees keep their own NOS fallbacks | recommended design, approved 14 Oct 2026 |
| Of the panel screen's four non-panel exits: "mixed phenotype with no detail" and "no leukaemic population" become morphology answers; the genetic or clinical category exit relies on the genetics and prior-therapy screens asked earlier; the divergent-clone exit is dropped | registrar, 14 Oct 2026 |
| The tool stops asserting a positive AUL or ALAL-NOS diagnosis | follows from removing the panel question |

## 3. The flow

Before, for a file with a marrow, film or trephine report and flow cytometry or IHC:

`evidence screen` → prior therapy → defining genetics → blast gate → lineage markers → (no rule fits) → **panel adequacy** → 9801, 9805 or the AML genetics list.

After:

`evidence screen` → **morphology** → prior therapy → defining genetics → blast gate → lineage markers → (no rule fits) → the code the morphology answer names.

Files with a marrow report and no flow or IHC are unchanged: they already meet `ac_morphology_only`, which ends in a code.

## 4. Data changes (`data/database/group_01_dt.json`, tree `tree_acute_leukemia`)

### 4.1 New node `ac_morphology_first`

`node_type: morphology_only`, `step_label: "Blood film / marrow morphology"`, `nos_fallback: null`. Question: "What does the blood film, marrow aspirate or trephine report describe?" Hint, as on `ac_morphology_only`: "Cytochemistry (MPO, Sudan black, PAS, non-specific esterase) counts as morphology, not as flow cytometry." `captured_variables`: `morphology_finding`, `apl_phenotype`. No option writes `evidence_tests`, so the tick-derived evidence is kept.

| # | Option | Captures | Destination |
|---|---|---|---|
| 0 | Lymphoid blasts, MPO / Sudan black negative on cytochemistry | `morphology_finding: lymphoid_blasts` | `ac_prior_therapy_gate` |
| 1 | Myeloid blasts, Auer rods and/or MPO / Sudan black positive cytochemistry | `morphology_finding: myeloid_blasts` | `ac_prior_therapy_gate` |
| 2 | Hypergranular promyelocytes / faggot cells with coagulopathy (DIC) | `morphology_finding: hypergranular_promyelocytes`, `apl_phenotype: suspected` | `ac_prior_therapy_gate` |
| 3 | Two distinct blast populations, or the report states "mixed phenotype" / "biphenotypic acute leukaemia" | `morphology_finding: mixed_phenotype_stated` | `ac_prior_therapy_gate` |
| 4 | Blasts present, lineage not stated in the report | `morphology_finding: lineage_not_stated` | `ac_prior_therapy_gate` |
| 5 | Marrow reviewed: no leukaemic population; reactive or non-neoplastic | none | non-reportable terminal, reason as on `ac_morphology_only` option 4 |

### 4.2 `ac_document_inventory`

Options 4 (morphology and flow cytometry) and 5 (morphology and IHC, no flow) change `next_node` from `ac_prior_therapy_gate` to `ac_morphology_first`. Their tick conditions and captures are untouched.

### 4.3 `ac_lineage_assignment`

Add `morphology_finding` to `captured_variables`. Insert five rules after the last marker rule (rule 39) and before the existing "nothing entered" rule (rule 40). Each has a `when` and no marker tokens, so any marker combination that defines a lineage fires first.

| New rule, `when` | Destination | Annotation |
|---|---|---|
| `morphology_finding: hypergranular_promyelocytes` | `next_node: ac_apl_status_lineage` | the lineage-route PML::RARA question, whose "not tested" answer goes on to the AML genetics list |
| `morphology_finding: myeloid_blasts` | 9861 | `workup_status: incomplete`, low confidence |
| `morphology_finding: lymphoid_blasts` | 9835 | `workup_status: incomplete`, low confidence |
| `morphology_finding: mixed_phenotype_stated` | 9805 | low confidence; upgrade: the marker-level flow report would give 9806, 9807, 9808 or 9809 |
| `morphology_finding: lineage_not_stated` | 9801 | `workup_status: incomplete`, `alal_subtype: null`, low confidence; upgrade: a comprehensive flow panel covering the five rare lineages would establish a definite lineage |

Each upgrade line says no lineage-defining marker was entered and the code follows the morphology report. The missing comprehensive immunophenotype is named in the upgrade line, not as an outstanding test: `outstanding_tests[]` accepts only the closed list of test names the build checks (`check_outstanding_tests`). Rule 40 (nothing entered, no morphology fact) stays and records 9801. Rule 41, the catch-all that went to `ac_alal_resolve`, becomes `morphology_code: 9801`, low confidence, `workup_status: incomplete`. It is reached by cases handed in from other trees that carry no acute morphology answer. The five rules and rule 41 get witnesses from `build/induce_flow.py`, which is rerun to regenerate `branch_sequence`.

### 4.4 Remove `ac_alal_resolve`

Its only inbound route was rule 41. `metadata.total_decision_nodes` stays 98 (one removed, one added). `docs/clinical-warnings.md` keeps an entry for the removed node only as archive text; it is marked removed.

### 4.5 Burkitt-pattern morphology (added at approval)

ICD-O-3.2 codes Burkitt lymphoma to 9687/3 (Group II) and lists "Burkitt cell leukemia" and "Acute leukemia, Burkitt type" as its synonyms; 9826 no longer exists (`icdo32.sqlite`, and `docs/group_01_icdo32_names.md` §4). So a Burkitt-pattern film that no marker overrides refers to Group II. Both mature-lymphoid options that lead to the Burkitt discriminator panel (`ml_morphology_only` option 5, `ml_morphology_pattern` option 5) now also record `morphology_finding: burkitt_pattern`. One more rule on `ac_lineage_assignment`, among the morphology rules, sends that finding to `ml_burkitt_refer`, where the clerk confirms the referral or goes back to the discriminator panel. The screenshot route (MYC FISH and TdT, then TdT alone on the acute markers) therefore ends at the Group II referral. The new rules are six, not five.

## 5. What each old answer became

| Old panel answer | Now |
|---|---|
| 0 Comprehensive panel, at most one marker per lineage (AUL) | gone; morphology answer 4, or the fall-through rules 40 and 41, records 9801 with the missing comprehensive immunophenotype named in the upgrade line |
| 1 Comprehensive panel, two or more markers of one lineage (ALAL-NOS) | gone, same |
| 2 Genetic or clinical category | gone; the defining-genetics and prior-therapy screens already route these cases |
| 3 Divergent clone under 5% | dropped |
| 4 "Mixed phenotype" with no detail (9805) | morphology answer 3 |
| 5 Panel incomplete, not performed (9801) | morphology answer 4 or rule 40/41 |
| 6 No leukaemic population | morphology answer 5 |

## 6. What this gives up

- **AUL and ALAL-NOS** are no longer asserted. Both are immunophenotypic diagnoses, and the engine cannot verify the panel; the case is recorded as 9801, the code both share. Group 1 Diagnostic Pathway §4.1's four-row 9801 table diverges from the tool from this date (ruling 2, the latest document wins).
- **The divergent-clone exit** is gone, so a case with a minor second clone is coded by its markers and morphology without the under-5% prompt.
- **CML blast crisis, therapy-related AML, AML-MR clinical history and eosinophilia with a kinase fusion** lose the screen that named them. They keep whatever the earlier screens already route.

## 7. Behaviour to expect

- A TdT-only entry after lymphoid-blast morphology returns 9835, not a panel question.
- Cases handed in from the mature-lymphoid, MDS and Down syndrome routes have no acute morphology answer and end at 9801 where the panel screen used to be. The leukaemic Burkitt route in the screenshot is of this kind. Whether Burkitt-suspected morphology should instead map to a Group II referral is a separate decision, not part of this change.
- Reachability: 9805 and 9801 stay reachable. No other code's route passes through the removed node.

## 8. Tests and controls

1. `python3 build/build_database.py` with the three Layer 1 paths exported: preflight, data gate (next-node resolution, declared variables, rule-subsumption lint, node count, witnesses) and engine gate.
2. One existing engine-gate assertion is edited because the behaviour it records changes on purpose: `check_engine_flow.mjs` line 2215 expects marrow aspirate with PCR and flow to reach `ac_prior_therapy_gate`; it now expects `ac_morphology_first`. No other assertion names the changed routes. The nothing-entered test at line 1133 must still pass untouched.
3. Replays through the real engine (scratch simulator, UI-fidelity guard on), each read for code, outstanding tests and trail:
   - lymphoid blasts, TdT only: 9835, no panel screen
   - lymphoid blasts, CD19 strong and CD10: the B-ALL genetics screen (markers override)
   - myeloid blasts, nothing entered: 9861
   - myeloid blasts, cMPO strong: the AML genetics list
   - mixed phenotype stated, TdT only: 9805
   - hypergranular promyelocytes, CD45 negative only: `ac_apl_status_lineage`
   - lineage not stated, nothing entered: 9801
   - no leukaemic population: non-reportable, no code
   - the screenshot route (Burkitt screen, MYC FISH and TdT): 9801 directly
   - the Group 1 exploration rerun: the 75 reachable codes unchanged
4. Control (rule 10, hard ones only): in a scratch copy of the data, restore rule 41's old `next_node: ac_alal_resolve` target and remove the five morphology rules; the lymphoid-blast TdT-only replay must then fail by reaching the old panel question. Then restore and watch it pass. The real data and tests are never edited to run it.
5. Drive the real page (`python3 -m http.server 8811`) through the screenshot route and three awkward cases, and read the output block (rule 11).

## 9. Out of scope

`app.js` (no clinical logic there). The mature-lymphoid, MDS and chronic myeloid trees. The other open findings from the reachability review. Rare-lineage morphology routes (megakaryoblastic, erythroid, basophilic, plasmacytoid dendritic cell-like, NK), which need sourced descriptors and a ruling on 9840. REDCap is not touched; the work stays uncommitted for review.

## 10. Open points for the registrar

1. Hypergranular promyelocytes route to the lineage-route PML::RARA question (`ac_apl_status_lineage`), not the morphology-route twin (`ac_apl_status`) that closes at 9861 when PML::RARA is not tested. The 13 October engine-gate comment records that closing as intended for the morphology-only route; this design only uses the lineage twin.
2. Confidence is low on every morphology fall-back rule, because flow was done and defined nothing. `ac_morphology_only` records the same codes with no confidence override.

## 11. Result of the build (14 October 2026)

- `python3 build/build_database.py`: BUILD PASSED, 0 FAIL, no warning names a changed node. `induce_flow.py`: every rule has a witness.
- Engine gate: the assertion at line 2215 now expects the morphology question for flow and IHC tick sets; ten new scenarios were added (section 8, plus the Burkitt route). All pass.
- Control (scratch copy only): with the old panel question and catch-all restored and the six morphology rules removed, five of the new assertions fail by landing on the old question or on 9801; the three that must still hold (markers override, cMPO strong, lineage not stated with nothing entered) pass.
- Real page, driven in the browser: the screenshot route ends at the Group II Burkitt referral; lymphoid blasts with TdT alone give 9835; lymphoid blasts with CD19 strong and CD10 reach the B-ALL genetics; myeloid blasts with no marker give 9861.
- Group 1 exploration rerun: 75 reachable codes before and after, no throws. 9805 is no longer reachable from the mature-lymphoid, chronic myeloid and MDS hand-overs (they carry no acute morphology answer and end at 9801); it stays reachable on the acute tree.
- Not changed: `app.js`. Nothing committed.
- Known and left alone: the output block prints "Workup: Complete — no outstanding tests" beside the new upgrade line, as it does for every code whose required tests are credited.

## 12. Later the same day: the prior-therapy screen is removed (registrar, 14 October 2026)

The `ac_prior_therapy_gate` named in sections 4 to 6 no longer exists. Jay removed the prior-therapy question from all four Group 1 trees as unnecessary: every answer led to the same next screen, no rule read the answer, and its only effect was a `therapy_related` chip on the output. Each option that led to a gate now leads to the screen that followed it (`ac_defining_genetics_context`, `ml_morphology_pattern`, `mpn_bcr_abl1_gate`, `mds_germline_ibmfs_gate`). Fifteen links were repointed and the node count is 94. The tables above keep the gate name as the record of what was built first.

## 13. Later the same day: pathway-recheck fixes in the other trees (registrar, 14 October 2026)

Twelve fixes followed the pathway recheck, in the acute Down syndrome gate and in the chronic myeloid, mature-lymphoid and MDS trees. `ac_ds_gate` sends an untested GATA1s result to `ac_lineage_assignment`, so the Down syndrome gate no longer emits 9898 on age alone. Seven nodes were added: `mpn_eos_clonal_fish_prompt`, `mpn_eos_clonal_unresolved`, `mds_monocytic_entity_fork_unassessed`, `mds_cmml_unassessed`, `mds_monocytic_entity_fork_lt10`, `mds_blast_nd_fork` and `mds_del5q_blast_gate`. The full list, with pathway sections, is in `memory/registrar-rulings.md` under the same date.

