# Primary intracranial sarcoma, DICER1-mutant — design

**Date:** 15 September 2026 · **Status:** built and verified · **Closes:** `docs/TODO.md` §2.1

---

## 1. Problem

WHO CNS5 recognises **Primary intracranial sarcoma, DICER1-mutant**. The tool could not reach it.

The only route to `9480/3` was the posterior-fossa option *"Mesenchymal / sarcomatoid — … reported as a
cerebellar sarcoma"*, which required the report to use the legacy wording. `g3_supratentorial` had **no
mesenchymal family option at all**, so a supratentorial intra-axial sarcoma fell to `8000/3` "no
morphological family can be assigned". `g3_spinal` and `g3_meninges` likewise had none.

That matters because of where the tumour actually is:

| | |
|---|---|
| Supratentorial | **92%** of reported cases |
| Median age | **6 years**; 87% paediatric |
| Infratentorial / spinal | exceptional |

— Tauziède-Espariat A, et al. *Mesenchymal non-meningothelial tumors of the central nervous system: a
literature review and diagnostic update of novelties and emerging entities.* Acta Neuropathologica
Communications 2023;11(1):22. doi 10.1186/s40478-023-01522-z

The single route the tool had was in the 8% tail.

## 2. What the entity is

Discovered by DNA methylation profiling, not morphology. Koelsche and colleagues profiled 22 primary
intracranial sarcomas (18 paediatric) sharing one signature; sequencing found **DICER1 hotspot mutations
in 21/22 (95%)**, *TP53* in 55%, MAPK alterations in 77%. Their own observation is the design constraint:
the tumours *"were initially interpreted to represent various tumor types, but rhabdomyosarcoma was not
among the typical differential diagnoses considered"* — rhabdomyoblasts were found only retrospectively.

— Koelsche C, et al. Acta Neuropathologica 2018;136(2):327–337. doi 10.1007/s00401-018-1871-6

WHO CNS5 essential criteria are two: a primary intracranial sarcoma, and a pathogenic *DICER1* mutation,
germline or somatic. For unresolved lesions the methylation profile is mandatory. **No CNS WHO grade
exists.** Roughly a quarter of cases with constitutional data are germline.

Morphology reachable below molecular testing: spindle, pleomorphic or rhabdoid cells; PAS-positive
cytoplasmic eosinophilic globules; patchy desmin; **GFAP, OLIG2 and cytokeratins negative**. Adjuncts:
H3K27me3 loss and nuclear TLE1 (6/6 in one series — Alexandrescu S, et al. Histopathology
2020;78(2):265–275, doi 10.1111/his.14217).

## 3. Decisions taken

| Decision | Ruling |
|---|---|
| Which compartments | **All that can carry it**, not just the commonest. Topography is recorded per case and is not bound by the ICCC-3 morphology grouping. |
| `g3_midline` | **Excluded.** No reported sellar or pineal case; the pineal myogenic differential is alveolar rhabdomyosarcoma with a *FOXO1* fusion. Deep midline supratentorial structures are `C71.0` and already route to `g3_supratentorial`. |
| Gating | **Family-gated with a molecular upgrade, plus an unconditional germline prompt.** The morphological picture alone emits the code and a descriptive diagnosis; molecular confirmation upgrades the asserted diagnosis without changing the code. |
| ICCC-3 subgroup | Accepted. `9480` maps to **IIIc1 Medulloblastomas at any topography** (`000-809`), unlike `9380` which splits by site. A case coded here counts among the medulloblastomas. |
| Shared vs duplicated node | **One shared node.** Cross-tree `next_node` is already used in this file. Five copies of the same criteria would drift. |

## 4. Implementation

**`st_dicer1_sarcoma`** — `cytogenetics_dropdown`, owned by `g3_supratentorial`, step 4.

Reached from four options, all worded identically:
`st_lesion_gate` (new), `pf_family_triage` (re-pointed from a terminal `9480/3`),
`sp_morphology_pattern` (new), `mn_lesion_triage` (new, adds "leptomeningeal or dural attachment").

> Mesenchymal / sarcomatoid — spindle, pleomorphic or rhabdoid cells with no glial or neuronal
> differentiation; GFAP and OLIG2 negative where stained

Six outcomes. **All emit `9480/3`.**

| Outcome | Track | Diagnosis | Basis | Confidence |
|---|---|---|---|---|
| *DICER1* pathogenic mutation — biallelic, or single with loss of heterozygosity | A | Primary intracranial sarcoma, DICER1-mutant | 8 | high |
| Methylation class assigned | A | Primary intracranial sarcoma, DICER1-mutant | 8 | high |
| *DICER1* sequenced, negative | B | Intracranial sarcoma, **NEC** | 7 | low |
| H3K27me3 loss and/or nuclear TLE1 only | B | Intracranial sarcoma with rhabdomyosarcoma-like features, NOS | 7 | medium |
| No molecular testing | B | Intracranial sarcoma, NOS | 7 | low |
| Report says only *"cerebellar sarcoma"* | B | Cerebellar sarcoma, NOS | 7 | low |

Null grade on every branch. Resource-level gate: sequencing RL IV, methylation RL V, family
`unspecified` with `rl_assignment: by_analogy`. Germline prompt in `upgrade_path` on all six.

**Two supporting changes.** `9480`'s `confidence_ceiling` raised **low → high** — it was set when the
code was a legacy string only and was flooring a molecularly confirmed case at low. Two aliases added:
the WHO CNS5 name and Koelsche's original *"spindle cell sarcoma with rhabdomyosarcoma-like features,
DICER1 mutant"*.

## 5. Verification

`BUILD PASSED` — 163 checks, 0 FAIL. `induce_flow.py` re-run; every rule has a witness.

Three build failures were caught and fixed during the build, each a real rule doing its job: an orphan
node before wiring, a stale `metadata.total_decision_nodes`, and `track: who_cns5` forbidding a
non-null `comment` (contract §2(1) — a branch filling both halves prints two diagnoses for one case).

Driven in the browser, supratentorial `C71.0`:

- *DICER1* mutation → `9480` · **CONFIDENCE HIGH** · Diagnosis *Primary intracranial sarcoma,
  DICER1-mutant (WHO CNS5)* · Basis *8 — Cytogenetic or molecular* · entity annotation rendered
- No testing → `9480` · **CONFIDENCE LOW** · Diagnosis *Intracranial sarcoma (ADAPTR descriptive · NOS)*
  · Basis *7 — Histology* · provisional-pending naming *Molecular/PCR* and the not-excluded entity · no
  WHO entity asserted

Groups 1 and 2 byte-identical to `main`.

## 6. Left open

The gate's `family` vocabulary has no mesenchymal value, so the clerk-facing line reads *"the
unspecified family"*. Recorded as `docs/TODO.md` §2.1a.
