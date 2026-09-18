# Group IV — build report, 2026-09-18

**What was built:** `group_04_dt.json` (18 morphology entries · 4 trees · 34 nodes) and
`aliases_group_04.json` (69 aliases), plus one new schema field, eight new validation rules,
two new cross-group validation rules, and the shared-layer changes the group could not route
without. Built on the Group 4 build contract of 16 September 2026 and the registrar's six
rulings D1–D6 of the same date.

**Final build, run 18 September 2026:** `python3 build/build_database.py` — **255 checks run ·
187 OK · 36 NOTE · 53 WARN · 0 FAIL · BUILD PASSED.** The baseline at the start of the
documentation task was 251 checks; the four added since are the concurrent validator agent's.

**Read this first if you read nothing else:** §7 is what needs you — five open items, three of
them registrar decisions, one of which moves cases between two published ICCC-3 incidence
groups. §6 is what a green build still missed. §1 is the shape of the group and why it is
unlike the three before it.

---

## 1. What this group is, and why it did not behave like Groups 1–3

Group IV is three biologically unrelated tumour families sharing one ICCC-3 group: the
neuroblastic spectrum (`9490`, `9500`), the paraganglioma and pheochromocytoma family
(`8680`–`8700`), and the olfactory and peripheral neuroepithelial codes (`9501`–`9504`,
`9520`–`9523`). It is also the first group whose topography is **every site**: fourteen of its
eighteen codes are admitted at `C00.0`–`C80.9`.

Two consequences shaped the build.

**Site is the tree key**, as compartment was in Group 3. The router captures topography at
Stage 1, so the tree is chosen without asking the clerk anything extra. Four trees, one per
site family, with a catch-all:

| `tree_id` | Prefix | Nodes | Topography declared | Dominant differential |
|---|---|---|---|---|
| `g4_sympathoadrenal` | `sa_` | **15** | `C74.0/1/9` · `C47.0`–`C47.9` · `C48.0/2/8` · `C38.1`–`C38.3` | Neuroblastoma · ganglioneuroblastoma · ganglioneuroma · pheochromocytoma · sympathetic paraganglioma |
| `g4_head_neck_paraganglia` | `hn_` | **5** | `C75.4` · `C75.5` · `C30.1` | Carotid body · jugulotympanic · vagal paraganglioma |
| `g4_sinonasal` | `sn_` | **5** | `C30.0` · `C31.0`–`C31.9` · `C11.0`–`C11.9` | Olfactory neuroblastoma · sinonasal small round cell differential |
| `g4_other_peripheral` | `op_` | **9** | `C80.9`, plus the router's default catch-all | Medulloepithelioma · neuroepithelioma at peripheral sites; the unestablished-site terminus |

**Seventeen of the eighteen codes are reachable by walking a tree.** The eighteenth is `9504/3
Spongioneuroblastoma`, unreachable by ruling D2 (§2).

**The group's behaviour declaration is `3`, and nothing else**, across every ICCC-3 Group IV
range. That single fact generated the group's one new schema field (§3) and its most
consequential ruling.

**Evidence, stated plainly.** The assigned baseline — Pfister SM, et al., *A Summary of the
Inaugural WHO Classification of Pediatric Tumors*, Cancer Discovery 2022;12(2):331–355 — gives
peripheral neuroblastic tumours one paragraph and defers to a Supplementary Table S3 that was
not held when the contract was written. **The registrar supplied Supplementary Table S3 on 18
September 2026**, and it is the WHO paediatric entity list for both halves of the group. The
paraganglionic family rests on Mete O, et al., *Overview of the 2022 WHO Classification of
Paragangliomas and Pheochromocytomas*, Endocrine Pathology 2022;33(1):90–114, read in full; the
olfactory family on Rooper LM, *Navigating New Developments in High Grade Sinonasal
Neuroendocrine and Neuroectodermal Neoplasms*, Head and Neck Pathology 2023;17(2):299–312, and
Agarwal A, et al., *Update from the 5th Edition of the WHO Classification of Nasal, Paranasal,
and Skull Base Tumors*, AJNR 2023;44(10):1116–1125, both read in full. **`9501`–`9504` at
peripheral sites rest on one 1986 case report**, and no pathway is built for them.

**No paper in this group states an ICD-O code.** Not Mete 2022, not Rooper 2023, not Agarwal
2023, not Juhlin 2025, not Pfister 2022. For every code in the group the two-source test
resolves as **ICD-O-3.2 decides, the WHO paper corroborates** — the WHO leg confirms that a
current entity lives on the stem and never confirms the number.

---

## 2. The six rulings, and the node that realises each

| Ruling | What it says | Where it lives in the data |
|---|---|---|
| **D1** | A ganglioneuroma gets no Group IV code. `behaviour_exclusion` is ratified. | `sa_histology_subclassification` **option 3** carries a `behaviour_exclusion` naming `9490/0 Ganglioneuroma` against the group's `3` declaration, and emits no `morphology_code`. Its label requires the report to exclude **both** a neuroblastic component **and** a paraganglioma/pheochromocytoma component, so a composite case is routed to option 4 and `sa_composite_component` instead, and can never reach the exclusion. |
| **D2** | `9504 Spongioneuroblastoma` is built, flagged, and reachable from no tree. | `morphology_entries[]` carries it with `obsolete_term: true` and an `obsolete_source` that states in terms that this is **not** an IARC `[obs]` marking but the build's own finding on the Group 3 test. `check_group4_9504_unreachable` (rule 4) proves no emission, no node-level `nos_fallback` and no entry-level `nos_fallback_code` names it. |
| **D3** | All four olfactory codes built; only `9522` resolvable. | `sn_report_wording`, a `clinical_alias` node. Option 0 (`Olfactory neuroblastoma` / `Esthesioneuroblastoma`) advances to `sn_ihc_checklist`; options 1–3 resolve `9520/3`, `9521/3` and `9523/3` **only on the report's exact wording**, each with a clerk-facing `reason` flagging registrar review before the code is finalised in REDCap. `sn_ihc_checklist` and every histological route can reach `9522/3` only. |
| **D4** | "pPNET" and its synonyms alias to `9364`, with a cross-group referral. | `op_clinical_alias` option 0 routes *Peripheral primitive neuroectodermal tumor* / *Peripheral neuroectodermal tumor* / *PPNET* to `op_ewing_site`, which refers to Group VIII at a bony primary and Group IX at soft tissue. **`9364` is never written to a `morphology_code`** — `check_group4_not_a_group_code` (rule 8) proves it. |
| **D5** | `morphology_name` is keyed to ICD-O-3.2, not to the REDCap option file. | `check_icdo32_round_trip` extended to Group 4: **34 of 34 (code, name, behaviour) triples exist verbatim in `icdo32.sqlite`, with 0 declared name exemptions.** `check_redcap_exact_names` is suppressed for Group 4 with a NOTE explaining why, exactly as for Group 3. Groups 1 and 2 keep their existing behaviour. |
| **D6** | "Peripheral neuroepithelioma" goes to `9503`, and the branch asks what the IHC shows. | `op_ihc_cd99`, an `ihc_checklist` keyed on `cd99_ewing_panel_result` across the full five-state closed vocabulary. CD99 positive with PHOX2B and synaptophysin negative advances to the Ewing referral; a genuine negative resolves `9503/3` with the workup complete; `not_done` / `not_available` / `not_assessable` each resolve `9503/3` with a `provisional_pending` naming the outstanding panel. **A tested-negative panel and an untested one do not share a destination.** |

**One part of D3 has been superseded and the data reflects the later ruling, not the earlier
one.** D3 specifies `confidence_ceiling: "low"` on the three alias-only olfactory branches. The
registrar removed confidence from the engine entirely on 16 September 2026 — *"the variable:
confidence itself must be removed from code"* — and `confidence` now appears **zero times** in
`group_04_dt.json`. Under latest-document-wins the removal governs. D3's intent is carried by
the clerk-facing `reason` on each branch instead, which says the term is not confirmed against
a current WHO classification and is flagged for registrar review. Recorded here so nobody
reconciles the two documents by re-adding the field.

---

## 3. The one new field, and the two extra uses the trees found for it

**`behaviour_exclusion`.** Group 1 added six fields, Group 2 five, Group 3 seven. Group 4 adds
**one**, forced by D1: the schema had no way to say *this histological entity exists, has an
ICD-O code, and that code's behaviour falls outside the group's declaration, so no Group IV
code may be emitted.* Without it the only options were to emit `9490/3 Ganglioneuroblastoma`
for a benign tumour, or to refer to a group that does not exist — ICCC-3 registers benign
neurogenic tumours nowhere.

Six required keys; `icdo_code`, `icdo_behaviour` and `icdo_term` must round-trip to the
**Preferred** term at that `(code, behaviour)` in `icdo32.sqlite`; `icdo_behaviour` must **not**
be in the group's own declaration; a branch carrying it may not also carry a `morphology_code`;
`reason` is clerk-facing and is rendered. `app.js` dispatches such a branch to a new
`excludeBehaviour()` terminal.

**The contract predicted one instance. The build has three**, and the two extra ones were found
by the tree author rather than by the contract:

| Where | Excluded code | ICD-O-3.2 Preferred term at that behaviour |
|---|---|---|
| `sa_histology_subclassification` option 3 | `9490/0` | Ganglioneuroma |
| `op_medulloepithelioma` option 2 | `9501/0` | Medulloepithelioma, benign |
| `op_medulloepithelioma` option 3 | `9502/0` | Teratoid medulloepithelioma, benign |

The contract's §1.2 had already listed `9501/0` and `9502/0` among the four `/0` terms Group IV
does not admit, and said none was authored. What it did not draw is the consequence: a report
reading *benign medulloepithelioma* is a real diagnosis that the tree must be able to accept and
explain, not a case that falls through. All three round-trip against `icdo32.sqlite` and all
three pass `check_behaviour_exclusion`.

---

## 4. Shared-layer changes

### 4.1 `topography_codes.json` — 68 codes to 87

The contract's §7.1 listed seven blocks Group IV needed and none of which existed. Nineteen
codes were added — `C30.0`, `C30.1`, `C31.0`–`C31.9`, `C75.4`, `C75.5`, `C38.1`–`C38.3`,
`C11.0`–`C11.9` — each with `code`, `label`, `coarse_organ`, `candidate_groups`, and a
`redcap_code` **read from `ICD coding/RedCap Options/Topography Redcap.md`, never invented**.
Five new `coarse_organ_crosswalk` rows went with them: *Nasopharynx*, *Nasal cavity and middle
ear*, *Accessory sinuses*, *Mediastinum*, *Carotid body and other paraganglia*.

**Three sites the contract names are still absent, and the build said so rather than inventing
them** — `C10.x` oropharynx, `C32.x` larynx, `C77.0` lymph nodes of head, face and neck.
`presentation_router.json`'s `tree_routing._comment` records the omission in the file itself.
`docs/TODO.md` §15 records what closing it takes; the REDCap codes all exist and none needs
inventing.

### 4.2 The `C48.2` fix — a neuroblastoma that could never reach the group

`C48.0 Retroperitoneum` and `C48.8 Overlapping lesion of retroperitoneum and peritoneum` both
carried `candidate_groups: [2, 4, 9]`. **`C48.2 Peritoneum, NOS` alone carried `[2, 9]`**,
inside the same crosswalk row — an oversight, not a decision.

It matters because of how `narrowBySite()` works: it intersects the site's candidate list with
the archetype's, and falls back to the site's own list **only when the intersection is empty**.
`[2, 9]` against `solid_mass`'s `[2, 4, 6, 7, 8, 9, 10]` is non-empty, so the fallback never
fires and Group 4 was dropped before its tree could be chosen. `g4_sympathoadrenal` declared a
topography the router would never route to it, and a retroperitoneal neuroblastoma extending
into the peritoneum would have left the group silently.

Found by sweeping all 34 topography codes the four trees claim against the three archetypes
that can reach the group. `C48.2` was the only failure.

### 4.3 `presentation_router.json`

- **Group 4 registered** — `built: true`, four trees with their entry nodes, a `handoff`, and a
  `tree_routing` block of four `topography_in` rules plus a default resolving to
  `g4_other_peripheral`. The map is total and disjoint over all 34 codes
  `topography_codes.json` associates with Group 4, and `check_group4_topography_map` (rule 5)
  proves it on every build.
- **The `9501-9504` dual-group rule extended from 3 codes to all 21.** It matched only `C70.9`,
  `C71.9` and `C72.9` and carried its own note — *"Extend both files together when Group III is
  authored."* Group III was authored 16 September 2026, so a medulloepithelioma at `C71.6` fell
  through to Group 4, which is wrong: ICCC-3 gives `9501`–`9504` to Group III (`IIIc3`) across
  the whole of `C70.0`–`C72.9`. Extended, and the obsolete scope note deleted. No ruling was
  needed — this is the fix the note itself asked for.
- **`op_document_inventory` does not rely on that rule.** Its first option gates on a
  `C70.0`–`C72.9` topography and refers to Group III before any code is emitted, and its
  `coding_note` says the router's own rule *"must not be relied on as the only safeguard."*

**Three sibling rules carrying the identical stale note were not touched** — `9473`, `8963` and
`8000-8005`, all out of scope for this branch. `docs/TODO.md` §14 records them, with the
ICCC-2017 ranges that decide each. Checking those ranges turned up a wider defect on `9473`:
range 29 is the only range in `ICCC-2017.sqlite` carrying `9473`, it takes sites `000-809`, and
it resolves to `IIIc2`, so the rule's *"Peripheral / soft tissue PNET"* default to Group IX has
no basis at **any** topography.

---

## 5. The new validation rules, and what each would have caught

Eight Group IV rules, plus two cross-group rules the build's own defects forced. Every one has
negative controls in `docs/validator_negative_controls.md`.

| Check | Rule | What it would have caught |
|---|---|---|
| `check_behaviour_exclusion` | 1 | A `behaviour_exclusion` naming an **admitted** behaviour — which would hide a code that should have been emitted. Also a block carrying both an exclusion and a `morphology_code`, and a term that does not round-trip to the Preferred ICD-O-3.2 string. |
| `check_group4_behaviour_declaration` | 2 | Any Group IV entry not carrying `behavior_code: "3"`, read off a named constant rather than a bare literal. |
| `check_group4_absent_codes` | 3 | `8683` emitted as a `morphology_code`, a `nos_fallback_code` or an alias target. Prose mentions are WARN, not FAIL — the contract's own reasoning names the digits. |
| `check_group4_9504_unreachable` | 4 | A branch, a node-level `nos_fallback` or an entry-level `nos_fallback_code` reaching `9504`, breaking D2. |
| `check_group4_topography_map` | 5 | A topography routing to two trees or to none; a catch-all that is a dead end; and `9501`–`9504` emittable from a tree declaring a `C70.0`–`C72.9` topography. |
| `check_visser_table4_gate` | 6 | **Revised mid-build on a real defect a finished tree exposed** — `8680` and `9522` were being emitted at basis 1/2 with no `no_tissue` flag, so a check bound to `no_tissue` missed them. Now bound to `basis_of_diagnosis` directly, at any node type. Basis 1 or 2 emitting **any** Group IV code is a build error (ENCR rule 5 — Group IV has no Table 3 entries); basis 4 may emit only `9500` or `8700`, and only with a non-empty `biochemical_questions[]` (ENCR rule 6, basis 4 never stands alone). |
| `check_icdo32_round_trip` · `check_redcap_exact_names` | 7 | Extended to Group 4 the way they already covered Group 3. A `(code, name, behaviour)` triple the REDCap option list carries that ICD-O-3.2 does not. |
| `check_group4_not_a_group_code` | 8 | `9364` written to a `morphology_code` anywhere in the file — the failure D4 exists to prevent. |
| `check_ihc_checklist_renders_a_control` | cross-group | An `ihc_checklist` with neither a non-empty `branch_sequence.order` nor a non-empty `test_result_states` — a node that renders **no way to answer it**. `marker_groups[]` cannot satisfy it, because `markerFlow()` does not read it. Registered for every group. |
| `check_no_internal_identifier_leaks` | cross-group | A schema field name or a declared `node_id`/`tree_id` appearing in clerk-facing prose. `coding_note` and `topography_routing_note` stay exempt, and are confirmed not to false-FAIL despite carrying 14 such mentions legitimately. |

Three checks were found FAILing on **correct** data and were fixed rather than the data:
`check_non_reportable_terminals` misread a `nos_fallback` object and a `behaviour_exclusion`
block as code-less terminals (7 FAIL); `check_group4_topography_map` swept the whole registry's
topography space instead of Group IV's own (1 FAIL, naming 292 codes); rules 3 and 8 failed on
`8683`/`9364` in clerk-facing prose (3 FAIL). Eleven FAILs to zero, with Groups 1–3 confirmed
byte-identical before and after.

---

## 6. What a green build missed — the browser pass

**A green build is not a working tool.** Contract §9 step 9 required driving the real tool in a
browser once all four trees existed. It was done, and it found two defects, both of them
invisible to every automated layer.

### 6.1 Two `ihc_checklist` nodes rendered no way to answer them

`hn_ihc_checklist` and `sn_ihc_checklist` rendered a question, a hint and a bare **Continue**
button — and nothing to tap. Both keyed `resolution_logic[]` off captured state variables
rather than marker tokens, so `induce_flow.py` induced an empty `branch_sequence.order`, and
neither node carried a `test_result_states` block. `app.js`'s `nodeControl()` routes every
`ihc_checklist` carrying a `branch_sequence` to `markerFlow()`, which asks strictly from
`branch_sequence.order` and never reads `marker_groups[]`; `dispatchNode()` separately prepends
`stateSelectors()`, which renders only where `test_result_states` exists. Both absent, no
input.

**Why the build missed it.** `induce_flow.py` proves every rule in `resolution_logic[]` has a
*witness* — an answer vector that fires it, checked in the abstract against the rule logic. A
`when`-keyed rule keying off a captured variable has a witness whether or not anything in the
interface can ever set that variable. `check_flow_charts` already tolerated an empty
`branch_sequence.order` whenever a node's rules read no marker tokens, on the theory that
`test_result_states` selectors are the flow chart in that case — but it never checked that a
`test_result_states` block existed. Both checks validate the rule logic; neither looked at
whether the renderer that logic depends on has anything to show.

Fixed by giving each node a `test_result_states` array, and `keratin_status` /
`pankeratin_status` the full five-state closed vocabulary with a branch per state — so an
unread stain carries a `provisional_pending` instead of resolving as though it had come back
negative. **Negative is what confirms paraganglioma and olfactory neuroblastoma**, so treating
*not done* the same way would have let an excludable case through.

The same shape was then searched for across every group's `ihc_checklist` nodes. It turned up
**exactly two more, both in Group 3** — `pf_mb_molecular_gate` and `mn_grade_assembly` — already
merged to `main` and out of scope here. They are named in a dated exemption that downgrades
them to WARN and FAILs on its own if either stops having the defect. `docs/TODO.md` §13.

**Two variables on those two nodes are still wrong, and it is recorded rather than fixed.**
`general_ne_markers_status` and `architecture_status` declare only `positive`, so a clerk whose
neuroendocrine panel came back **negative** has no button for it, and leaving the line blank
emits `8680/3` or `9522/3` with a reason saying the panel *"was either not completed or
equivocal."* A tested-and-negative panel is neither. `docs/TODO.md` §17 — it is a registrar
question, and a five-state vocabulary cannot simply be copied on, because
`check_declared_states_consumed` (ruling 11) FAILs any declared state no `when` clause consumes.

### 6.2 Internal identifiers printed in text a clerk reads

An independent review of the fix above — browser drive plus an independent negative-control
reproduction — found the fix itself had introduced a second defect. Twelve `reason` and
`provisional_pending.reason` strings contained the literal `refer_group 11`, a JSON field name
naming nothing a clerk can see. A further scan found nine occurrences, across seven strings, of
a bare `node_id` — **five of them pre-existing, written by the tree-authoring agents.**

Both are the same underlying defect, so one check covers both. All twelve field-name mentions
now name the destination in words — *"ICCC-3 Group XI (other malignant epithelial neoplasms and
malignant melanomas)"* — matching the house style already in `group_02_dt.json` and
`group_03_dt.json`. All nine node-id mentions name the step in words or drop the pointer.
Groups 1–3 independently confirmed at zero, before and after.

The same review also found `check_ihc_checklist_renders_a_control`'s own OK line claiming *"31
ihc_checklist node(s) all render at least one input control"* on Group 3 **immediately below a
WARN saying two of those 31 do not** — a summary contradicting the findings above it, which is
the exact failure mode the check exists to prevent. It now reports "29 of 31 … 2 exempted"
whenever a WARN was raised.

### 6.3 Four data defects found by the validator once it ran against real trees

Recorded for completeness: a Group 3 two-track output construct (`diagnosis_rendering`) carried
on 11 Group IV branches where it does not apply; two bare-string `nos_fallback` values; invented
`test_result_states` on `op_ihc_cd99` (`yes` / `no_or_not_done`) rewritten to the closed
vocabulary; and `provisional_pending` on three branches that emit no code. All four fixed
before the final run.

---

## 7. What needs you

### ★ 1. A CNS neuroblastoma cannot reach Group IVa, and ICCC-3 puts it there

**This is the item worth your time.** Three parts, in three files, one of them in Group 3 which
is already merged. Full detail and the Layer 1 queries are in `docs/TODO.md` §18.

ICD-O-3.2 carries `CNS neuroblastoma` and `Central neuroblastoma` (the latter with an explicit
`(C71._)` site reference) as synonyms on **`9500/3`**. ICCC-2017 range 43 gives `9490,9500` to
**IVa at sites `000-809`** — every site, the central nervous system included — and it is the
only range in the table carrying either code. The site split applies to `9501`–`9504` only.

But all 21 CNS topography codes in `topography_codes.json` declare `candidate_groups: [3]`, so
the case cannot reach Group IV by site routing at all; `op_document_inventory` option 0's label
refers every CNS topography out unconditionally, although its own `reason` correctly scopes the
rule to `9501`–`9504`; and `group_03_dt.json` codes `CNS neuroblastoma, FOXR2-activated` to
`9473/3` and emits `9500` nowhere.

**The cost is concrete: a paediatric CNS neuroblastoma is recorded in ICCC-3 Group III when
ICCC-3 puts it in Group IVa.** That moves the case between two published incidence groups.

Part 3 may well be deliberate and this report does not assert it is wrong — ICD-O-3.2 was
finalised 9 October 2020, WHO CNS5 followed in 2021, ICD-O-3.2 carries no FOXR2 entity
anywhere, and Group 3 records the entity as `code_status: "no_code"` against `9473/3` with its
reasoning written down. **The reconciliation is yours, and all three parts need ruling
together**, because changing part 1 alone changes routing for a merged group.

Build contract §0.6 identified the substance of this on 16 September 2026 and asked for a
routing note. One was written, and it is right — but it is in `9500`'s `coding_note`, which is
author-facing and never displayed. `9500`'s `topography_routing_note` is `null`.

Already paid: the alias agent declined to author the `CNS neuroblastoma` and `Central
neuroblastoma` aliases, correctly, because they would resolve into a tree that immediately
refers the case out.

### 2. Ruling D6's CD99 gate was applied wider than D6 names

D6 names one phrase — *peripheral neuroepithelioma*. As built, `op_clinical_alias` routes bare
`Neuroepithelioma, NOS` — the exact ICD-O-3.2 Preferred term on `9503/3`, and the subject of
alias-instruction entry 29, which D4 leaves standing — through the same Ewing-family gate. The
build wrote its reasoning into the node's `coding_note` and it is defensible, but it is not what
D6 says, and the gate can only move a case **out** of Group IV, never in. One question, one
option split if the answer is "the peripheral phrase only". `docs/TODO.md` §16.

### 3. The head and neck and sinonasal panels have no NEGATIVE button

§6.1 above. `docs/TODO.md` §17.

### 4. Three sites the contract names are still unroutable

`C10.x`, `C32.x` and `C77.0`. Laryngeal paraganglioma in particular is named in build contract
§5 as one of the head and neck tree's dominant differentials, and ICD-O-3.2 carries *Laryngeal
paraganglioma* as a Related term on `8693/3`. The cost is a less specific code — `8680/3
Paraganglioma, NOS` from the catch-all instead of `8693/3` with a site-resolution step. Adding
`C77.0` needs a decision first: a paraganglioma recorded at a lymph node is more often a
metastasis than a primary. `docs/TODO.md` §15.

### 5. A mis-citation in `hn_genetics`, in scope for this branch and not mine to fix

`hn_genetics`'s clerk-facing `hint` reads: *"Parasympathetic head and neck paraganglioma is
predominantly SDHD (46.5%), then SDHB (30.2%), then SDHC (16.3%) (Mete 2022, Supplementary Table
S3)."* **The figures are right; the attribution is wrong.** They are from **Pfister 2022
Supplementary Table S3**, rows 115–121. Mete 2022 has exactly one table — Table 1, p. 108, the
INPC classification — and no supplementary table at all. The three other *Supplementary Table
S3* mentions in the file attribute correctly to Pfister. One string, one edit, and it is in a
field a clerk reads.

---

## 8. Divergences recorded, not acted on

- **Visser's Table 4 puts phaeochromocytoma in ICCC-3 Group XI.** ICCC-2017 puts `8700` in
  **IVb**. ICCC-2017 is Layer 1 and governs. Recorded in `sa_imaging_pheo`'s `coding_note`; the
  routing is unchanged.
- **CoGNET still has no ICD-O code in any source.** Four have now been read in full and all
  four are silent. The registrar's instruction of 18 September 2026 is to stop chasing it.
  `docs/TODO.md` §11.
- **The `/3`-only rule rests on IARC, never on a WHO paper.** Juhlin CC, *The road ahead*,
  Journal of Clinical Pathology 2025;78:1–10, p. 8, says pheochromocytoma and paraganglioma
  *"display some malignant potential, the overall risk of distant metastasis is low"*. Read
  carelessly that looks like an argument against `/3`. It is not: WHO abolished the benign and
  malignant **adjectives** in its 4th edition (Mete 2022, p. 100), IARC implemented that as a
  behaviour code, and ICD-O behaviour is not a prognosis. Build contract §10.1b exists to stop
  anyone "fixing" this.
- **The Hyams grading criteria have no citable primary source.** The scheme is a 1988 Armed
  Forces Institute of Pathology fascicle with no PMID and no DOI. The table is held only through
  Gargano SM, et al., Head and Neck Pathology 2025;19(1):92, Table 1, whose own multivariable
  analysis found original Hyams grade **not** significantly associated with survival. The
  sinonasal tree records the grade the report states, as a string, and asserts nothing about
  what it means.
- **Kadish defined three stages, A to C.** Stage D is Morita's. The four-stage system is
  Kadish-Morita. The pathway document prints a four-row table under Kadish's name alone.

---

## 9. Clinical warnings

`clinical_alert` is `null` on all 34 nodes and all 18 morphology entries, and
`check_no_clinical_alerts` confirms it on every build (registrar ruling 9, 4 September 2026).
So unlike Groups I and II there were no strings to lift.

**Sixteen warnings were derived** from the trees' own `hint` and `reason` text, the build
contract and the papers, and recorded in `docs/clinical-warnings.md` under a Group IV heading,
each naming its source. The four that matter most:

- **Head and neck paragangliomas are often biochemically silent** — *"biochemical evidence may
  be absent, and patients could lack any symptoms"* (Di Stasio 2022, p. 930). A normal or
  untested catecholamine result excludes nothing, and the tool never requires it.
- **PHOX2B was positive in only 1 of 6 olfactory neuroblastomas** (Manethova 2023), and is
  absent from Rooper 2023's panel. A negative PHOX2B must not be used to rule it out.
- **A keratin-positive tumour in the paraganglioma differential is a well-differentiated
  neuroendocrine tumour** — *"Virtually all PPGLs lack expression of keratins"* (Mete 2022,
  p. 96). This is why an **unread** keratin is answered with a provisional and never with the
  negative branch.
- **SDHx germline testing changes surveillance for the patient and the family, and changes no
  code.** SDHB loss is a surrogate marker and a screening trigger, not a genetic diagnosis
  (Mete 2022, p. 103; Maignan 2017). Nobody downstream of the tool is told a family may need
  screening.

Two things the section records that the Group IV pathway document does not carry at all:
**calretinin**, offered by Rooper 2023 as the discriminator separating olfactory neuroblastoma
from the other sinonasal small round blue cell tumours; and the finding that a negative
vanillylmandelic acid / homovanillic acid pair excludes nothing — the full eight-metabolite
panel detected elevation in 93% of patients negative on those two (Verly 2017, as the pathway
document transcribes it; the primary was not re-read for this build).

One entry is recorded as **not source-verified**: the perioperative risk in an untreated
pheochromocytoma. No paper held in `Group 4 Papers/` states it. It is in the section because
build contract §4.1 named it as one of the pressures this group puts on ruling 9, and the gap
should be visible rather than silently absent.

---

*Sources: `ICD-Lookup/docs/group_04_build_contract.md` (2026-09-16, with §10.1b, §10.2b and
§10.2c added 18 September) · `Group 4 — Neuroblastoma Diagnostic Pathway.md` (2026-06-02, with
the corrections of contract §0 applied) · `Group 4 — Alias Build Instructions.md`, with
entries 30, 31 and 33 overridden by D4 · `ICD coding/ICD-O-3.2/icdo32.sqlite` (IARC FINAL,
9 October 2020) · `ICCC-2017.sqlite` · the seventeen key-point extractions in `Group 4 Papers/`.
Open items: `ICD-Lookup/docs/TODO.md` §§10–18. Negative-control evidence:
`ICD-Lookup/docs/validator_negative_controls.md`. Clinical warnings:
`ICD-Lookup/docs/clinical-warnings.md`, Group IV. A copy of this report is at
`ICD-Lookup/docs/group_04_build_report.md` so repo cross-references resolve.*
