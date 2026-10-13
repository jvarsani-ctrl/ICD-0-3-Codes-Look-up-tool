# Group I evidence gates: one box per test

**Written 13 October 2026.** Registrar's direction after trying a B-ALL with a negative BCR::ABL1 in
the Group I evidence gate. Related: `docs/evidence_document_mapping.md`, `docs/superpowers/specs/2026-10-06-ux-overall-fixes-design.md` §4 and §7.

## Purpose

The clerk records which tests are in the patient's file, one box per test, and the tool records
exactly those tests as the case's evidence. Options that cluster several tests into one tier ("karyotype
or FISH", "PCR or sequencing", "both") are removed.

## What the registrar said, and what I assumed

**Said:** separate tickboxes for Morphology, Flow cytometry, IHC, Sequencing, PCR and FISH; no clustered
options. Confirmed the nine-box list below ("Yes, exactly this").

**Assumed, to be corrected if wrong:**
- Group I only. The list is haematology tests, and Groups II to XI keep the document boxes. Group XI alone has
  19 gates on them.
- The boxes record that a test was done, not what it showed. Results (BCR::ABL1 negative, ETV6::RUNX1) are
  asked at the later steps, as now.
- The data's evidence list stays as it is for now (below, "Out of scope").

## The boxes

| Box | Credits |
|---|---|
| Referral / clinical note | Referral only |
| Marrow aspirate or blood film | Histology |
| Trephine biopsy | Histology |
| Flow cytometry | Flow cytometry |
| IHC | IHC |
| Karyotype | Cytogenetics/FISH |
| FISH | Cytogenetics/FISH |
| PCR | Molecular/PCR |
| Sequencing | Molecular/PCR |

Karyotype and FISH are separate boxes because they are different tests with different blind spots: only a
karyotype sees hyperdiploidy, hypodiploidy and complex karyotypes, and a normal karyotype must never close
the ETV6::RUNX1 branch. Marrow aspirate and trephine are separate because the MDS gate requires both.

## Design

**A second named tick vocabulary, `haematology_tests`,** in `data/shared/presentation_router.json`. The four
Group I gates (`ac_`, `ml_`, `mpn_`, `mds_document_inventory`) point at it. The engine already resolves a vocabulary
by name, so no other group changes.

**Each box carries `credits`.** When a vocabulary has them, the engine records as the case's evidence exactly
the union of the ticked boxes' credits (`tickCredited()` in `app.js`). An option's own `captures.evidence_tests`
describes a tier, and a tier says more or less than the file holds. It is kept only as the fallback when nothing
ticked credits anything, which is the referral tier on an empty checklist. The engine knows no test by name.

**The tiers become routing rules the clerk never sees.** The vocabulary sets `tiers_exclusive`, so no ticked set
fits two tiers and the sibling question cannot occur. The routes are the ones the gates had:

| Gate | Route | Rule |
|---|---|---|
| all four | referral node | no aspirate and no trephine |
| acute, mature lymphoid | morphology-only node | an aspirate or trephine, no flow, no IHC |
| acute, mature lymphoid | the tree's next node | an aspirate or trephine with flow; or with IHC and no flow |
| MPN | morphology-only node | an aspirate or trephine, none of karyotype, FISH, PCR, sequencing |
| MPN | prior-therapy node | an aspirate or trephine with at least one gene test (four exclusive cases) |
| MDS | morphology-only node | morphology that is not aspirate + trephine + IHC (three exclusive cases) |
| MDS | marrow-pattern node | aspirate, trephine and IHC |

A rule has one "any of" group, so "morphology and (flow or IHC)" and "a gene test" are written as exclusive cases.
The build enumerates every ticked set (512 for nine boxes) and fails if one fits no tier, if a tier can never be
offered, or, because of `tiers_exclusive`, if one fits two.

**Removed from the earlier version of this change:** the legend above the boxes, the three-way gene-test options
and the generated tier copies. The boxes name the tests, so none is needed. The generator keeps one new capability,
a per-node `vocabulary`.

**Kept:** the wording fixes at the genetics steps (a negative BCR::ABL1 has an answer; the B-ALL answers name
ETV6::RUNX1 and say a BCR::ABL1 result alone does not count).

## Behaviour changes, so none is a surprise

1. A file with morphology and a gene test but no flow or IHC still goes to the morphology-only node, as before.
   The gene tests are now credited as evidence on the way, where before the tier assumed them.
2. The special situations (Trisomy 21, extramedullary mass, malignancy excluded) are unchanged, and their own
   assumed evidence is also replaced by the ticks when anything is ticked.
3. `karyotype_result_status` and `workup_status` are no longer set at the gate. Nothing reads either.

## Testing

- Build: the tick-list enumeration, the exclusivity check, a check that every `credits` value is in the closed test
  list, and the generator sync check.
- Engine gate: a fixture where a tier overclaims its evidence, proving the ticks win; order independence; two boxes
  crediting one test once; the empty-checklist fallback.
- Negative controls: a credit typo; two tiers made to overlap; a tier rule edited without the mapping.
- Browser: the registrar's case (marrow aspirate, flow, BCR::ABL1 RT-PCR only) through the acute tree.

## Out of scope, for the registrar to decide

1. **Splitting the evidence list.** Karyotype and FISH credit one test, and PCR and sequencing credit one. They are
   recorded as separate boxes on the case but credit merged tests. Splitting means changing `diagnostic_tests_required`
   on 61 lines in Group I and the upgrade text. It matters clinically: PCR cannot find an ASXL1 mutation and sequencing can.
2. **Skipping questions the ticks already answer.** The genetics step still asks "is there a genetics report"
   after a gene test was ticked, and the later steps ask for FISH or RT-PCR results the clerk has just ticked. Nothing
   reads the ticks after the gate yet.
3. **Groups II to XI.** Each would need its own vocabulary of tests.
