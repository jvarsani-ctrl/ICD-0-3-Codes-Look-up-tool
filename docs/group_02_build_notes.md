# Group II open items — append only, registrar reads this in the morning

- **`behaviour_resolution.values` key spelling — contract vs. Pathway disagree, contract
  wins as documented.** Diagnostic Pathway §7.3 item 1 proposes `values: { "/1": …, "/3": … }`
  (behaviour keyed by the ICD-O behaviour string with the slash). `G2_BUILD_CONTRACT.md` §3.1
  specifies `values` as an object with exactly the keys `"1"` and `"3"` (no slash, bare
  behaviour-code string) and its worked JSON uses that form. The master instruction file
  (`Decision tree JSON Build — Master Instruction File.md` §3G, added 2026-09-04) documents
  the contract's `"1"`/`"3"` form, per this build's stated order of authority (contract over
  Pathway on anything the contract covers). Flagging because whoever writes
  `group_02_dt.json`'s actual `behaviour_resolution` blocks and whoever writes the validator
  for them must agree on one spelling — if the validator is built against the Pathway's
  `"/1"`/`"/3"` keys instead, every `behaviour_resolution` object authored against §3G's
  documented form will fail silently or loudly depending on how the check is written. Not a
  clinical question — a spelling reconciliation between two internal documents. — added by
  the master-file-documentation agent, 2026-09-04, while writing §3G.

---

## From the engine agent (`app.js`), 2026-09-04 — after implementing contract §3

- **The engine is agnostic to the `"1"`/`"3"` vs `"/1"`/`"/3"` key spelling flagged above.**
  `behaviour_resolution.values` is walked with `Object.keys()` and the key is never
  interpreted; the behaviour that reaches `finish()` comes from each leaf's own
  `behavior_code`, and the only key the engine reads by name is `unresolved`. So the
  reconciliation is a validator-and-authoring question only — nothing in the runtime has
  to change whichever spelling wins. Both orders render deterministically.

- **Two stylesheet variants requested (`design.md` owner).** The output block now emits
  `.orow--provisional` and `.orow--followup` alongside the plain `.orow`. Both degrade to
  an ordinary row today, which is *correct but quiet*: the follow-up row is the one that
  re-opens a deferred case months later, and `.orow--upgrade` already exists precisely
  because a row nobody notices stops being a checklist. Asking, not assuming — the engine
  agent does not own `uccf-tool.css`.

- **`entity_boundary` pre-empts the node's own branch selection.** A `numeric_gate` that
  carries one should declare **no `bands[]`** — they would be dead. Suggest a validator lint
  (`entity_boundary` + non-empty `bands` = WARN). It also only fires on node types that
  render a **Continue** button (`ihc_checklist`, `cytogenetics_dropdown`,
  `molecular_freetext`, `numeric_gate`, `imaging_pathway`) — never on a plain option-list
  node, and never on a node that also declares `test_result_states`.

- **Decision needing a ruling: what an undecidable boundary should do.** Contract §3.5 does
  not say. Implemented as: if the reading is absent *and* `also_outside_when` does not force
  the outside, the case goes to the node's `nos_fallback` at low confidence — it must not be
  read as "inside", which would hand back the narrow entity's code on no evidence. If the
  registrar wants a *named* destination for that case (the way `behaviour_resolution` requires
  a named `unresolved`), that is a schema addition — say so and it is a two-line change.

- **`deferrable: true` surfaces `follow_up_review` on the output block regardless of which
  leaf the clerk took**, not only on `unresolved`. Rationale: "deferrable" means the answer
  can still change after today, so suppressing the row on a confidently-answered case would
  understate. Confirm this is what was meant.

- **`unresolved` captures `null` into the criterion variable** (the fact was not established),
  not a sentinel string. If a later node needs to branch on "the behaviour was never
  established", it currently cannot — a `"unresolved"` sentinel would be the change. Nobody
  has asked for it yet.

- **`test_result_states` routes through the node's `resolution_logic[]`, not `options[]`.**
  Author one flat rule per state, `"when": { "<variable>": "<state>" }` — including one for
  `not_assessable` that does not reach a code the `negative` branch's evidence would have
  excluded. If no rule matches, the node's `nos_fallback` takes it at low confidence.

- **A branch-level `clinical_alert` is still not rendered anywhere.** Contract §7 says an
  alert may sit "on the node/branch where the decision is taken"; today only a **node**-level
  `clinical_alert` and a `morphology_entries[]` one reach the screen — an alert written on an
  `options[]` entry or a `resolution_logic[]` rule is silently invisible. Group 1 has several.
  This predates Group II and was left alone deliberately (out of scope, and changing it moves
  Group 1's rendered output). It needs a ruling: render branch alerts, or forbid authoring
  them there.

- **A branch may not carry both `behaviour_resolution` and `morphology_code`.** The engine
  asks the criterion and the code is ignored. Suggest a validator FAIL on the combination.

- **`ANSWER_LABELS` covers `y`/`n`/`yes`/`no`/`unknown`.** A leaf whose `when` uses any other
  token renders that token raw as its button label, so such a leaf must carry its own
  `label`. Any of the three leaves may override with `label` in all cases.

## g2_mastcell (9740 / 9741 / 9742) — opened 2026-09-04

- **No "mast cell neoplasm, NOS" code exists in the Layer 1 option list.** `9740 Mastocytoma, NOS`
  is used as the family-level fallback on all five refining nodes and on every "cannot be
  established" terminal. It is the least-overstating of the three available codes (9741 would
  assert systemic disease; 9742 would assert leukaemia) and it is the ICD-O mast-cell-tumour
  rubric — but it reads "mastocytoma" on a marrow case. **Registrar to confirm** 9740 is the
  intended carrier, or name another. Pathway §7.4 gives no NOS-fallback row for `g2_mastcell`.
- **Mast cell sarcoma is coded 9741 per Pathway §5.2, but ICD-O-3.2 codes it 9740/3.** Contract
  §2.1 permits behaviour splits only for 9718/9725/9751, so the /3 half was not built and §5.2
  was followed. The terminal carries a `provisional_pending` naming the entity. **Registrar to
  decide** whether mast cell sarcoma should instead get a 9740 `/3` behaviour-split object,
  which would put a localised destructive tumour in a code that does not say "indolent".
- **§5.1 defines two overlapping variables for the same fact**: `classification_used`
  (WHO-HAEM5 / ICC / harmonized — "FL grade, NLPHL grade, mastocytosis") and `criteria_set_used`
  (WHO / ICC / harmonized — "mastocytosis SM diagnosis"). This tree branches on
  `criteria_set_used` only, per the build brief. **Collapse them or document the difference**
  before the two mastocytosis rows drift apart.
- **`criteria_set_used` needed a fourth value, `"not stated"`.** Real reports frequently omit the
  framework. It is handled with the harmonized arithmetic but kept distinct on the record, so it
  is never silently rewritten as "harmonized". **Ratify the added value.**
- **`kit_d816v` has two conflicting vocabularies.** §5.1 says `pos / neg / not done`; contract
  §3.4's `test_result_states` closed set is `positive / negative / not_assessable / not_done /
  failed`. The tree uses the §3.4 spellings, because `not_assessable` and `failed` have no §5.1
  equivalent and the whole point of the node is that a Sanger "negative" is not a negative.
  **Registrar to align §5.1.**
- **Variables coined because §5.1 lacks them** (all mastocytosis-specific):
  `mast_cell_pct_smear`, `mast_cell_smear_band`, `tryptase_band`, `tryptase_minor_criterion_met`,
  `associated_myeloid_neoplasm`, `tpsab1_extra_copies`, `sm_major_criterion`,
  `sm_minor_criteria_count`, `sm_variant`, `mast_cell_ihc_panel`, `uncoded_entity_freetext`.
  `associated_myeloid_neoplasm` is deliberately **not** `prior_haematopoietic_malignancy`: the
  tryptase caveat turns on a *concurrent myeloid* neoplasm, not a prior one. Both are captured.
- **Serum tryptase when the AHN status is unknown.** The tryptase minor criterion is voided
  outright only when an associated myeloid neoplasm is documented (`override_when`). When AHN
  status is "not documented" the gate still runs, and the criterion's own checkbox text requires
  the clerk to confirm the absence of a myeloid neoplasm before ticking it. **Decide** whether
  "unknown" should void the criterion too — voiding is safer, but it removes the only minor
  criterion a Tier 0 site can reach.
- **Does SM-AHN generate a second registration?** The AHN component (MDS, MPN, CMML, AML) is a
  Group I neoplasm. Pathway §5.2 keeps the case at 9741 + free text and contract §4.1 does not
  list SM-AHN among the `refer_group: 1` targets, so **no referral branch was built**. If the
  registry wants the AHN counted, that is a second primary and needs a rule.
- **No `prior_probability` block was authored anywhere in this tree.** The construct needs a
  sourced `expected_positive_pct`, and no retained source gives a paediatric base rate for any
  mastocytosis test. Inventing one would be worse than omitting it. The LOW-confidence base-rate
  note lives in `coding_note` on `g2mast_sm_variant` and `g2mast_unresolved` instead.
- **No `behavior_code` is emitted on any branch**, matching `group_01_dt.json`. If the
  `morphology_entries[]` author gives 9740/9741/9742 anything other than a single object each,
  the terminals here will need behaviour codes added.

## g2_cutaneous (`g2_tree_cutaneous.json`) — 2026-09-04

- **Three coined `captured_variables`.** Pathway §5.1 has no name for these; all three carry a
  `when` condition, so they must be added to §5.1 or renamed to existing spellings before the
  merged file is validated. (a) `cutaneous_clinical_pattern` — the cutaneous presentation
  archetype (`patch_plaque_mf` / `erythroderma` / `papulonecrotic_self_healing` /
  `solitary_tumour` / `hv_photodistributed` / `mosquito_bite_hypersensitivity` /
  `panniculitic_nodules` / `ulcerating_plaques` / `solitary_plaque_facial` / `acral_nodule` /
  `generalised` / `not_determined`). It is what carries the two anti-miscoding rules of §3.7
  ("should be diagnosed as MF or LyP, irrespective of phenotype"), which cannot be encoded
  without it. (b) `gd_population_neoplastic` (`y` / `n` / `not_determined`) — §3.7 requires that
  the γδ cells be shown to be the *neoplastic* ones before 9726, and no §5.1 variable says that.
  (c) `proliferation_band_cutaneous` (`low` / `intermediate` / `high` / `not_documented`) — §5.1
  gives `proliferation_pct_cutaneous` as numeric, and `when` clauses cannot express `>20`.
- **`alk_ihc` value spelling.** Pathway §5.1 gives `pos / neg / not done`; build contract §1
  writes `alk_ihc: "negative"`. This tree uses the §5.1 spellings throughout. **Someone must fix
  one of the two documents** or the main tree and this tree will capture different strings for
  the same fact.
- **`resolving_test` for EBER ISH.** The closed diagnostic-test vocabulary (DT master §2) has no
  in-situ-hybridisation member. This tree maps EBER ISH to `"IHC"` (it is a tissue-section stain
  run in the same laboratory). Registrar to confirm, or add an `ISH` member — it affects every
  EBV-gated `provisional_pending` in Group II, not only this tree.
- **Severe mosquito-bite allergy has no ICD-O code.** Pathway §3.7 places it with hydroa
  vacciniforme-like LPD in one section (*cutaneous chronic active EBV disease*) with one shared
  progression risk, but §5.2 does not list a fallback for it. This tree routes it through the
  **9725 behaviour_resolution** — least-wrong and reversible, because the `/1` half is out of
  Group II anyway and the `/3` half catches a progressor. **Registrar decision required:** accept
  9725, or add a fallback row to §5.2.
- **EBER gates 9708 and 9726 in this tree.** Willemze's table lists EBV as negative for both, and
  §3.7 warns that an NK-phenotype HV-LPD mimics 9708 in a child, so `eber_status` of `not_done`
  or `not_assessable` stops at 9702 + `provisional_pending` rather than reaching 9708 or 9726.
  **This makes both codes unreachable at a site with no EBER ISH.** It is consistent with
  §7.7 rule 1, but the main tree (which also owns 9708) must gate it the same way or the two
  trees will disagree about the same case.
- **`satisfies_tests` is used nowhere in this tree, deliberately.** The codes' own
  `diagnostic_tests_required` lists are being written by another agent, and a value that does not
  match is an inert no-op that still reads as a live claim (DT master §3F). The entries author
  should decide whether any cutaneous branch genuinely discharges a listed modality and add it
  then. Omission understates the workup; it cannot overstate it.
- **`entity_boundary` evaluation order is unspecified.** Contract §3.5 puts the block on the node,
  but does not say whether the engine applies it before or after `resolution_logic` and
  `nos_fallback`. This tree is authored so that either order is safe (the exclusion rules route
  non-entity cases away first, and both the fallback and the outside branch land on 9702/3, so a
  case can never reach 9709 by default). **The engine owner should still state the order.**
- **9708 is emitted from `g2cut_panniculitic_phenotype`, not from the main tree.** See the build
  report; if the main tree also emits 9708 the two must not disagree on the βF1/CD56 rule.

## morphology_entries[] (the 92) — opened 2026-09-04 by the morphology-layer agent

- **`topography_dependent` is set on TWELVE codes, not the eleven contract §2.4 enumerates.**
  §2.4 names 9811–9818, 9823, 9827, 9837 (eleven). **9591 was added as a twelfth**, because
  it genuinely is dual-group and the contract is silent on its flag rather than negative
  about it: `presentation_router.json → dual_group_rules['9591']` routes C42.0/1/3/4 to
  Group I Ia4 and everything else to Group II IIb4; `group_01_dt.json`'s own 9591 entry
  already declares `topography_dependent: true`; and DT master §6 requires the flag on
  **every** `morphology_entries[]` object for a code that maps to different ICCC-3 groups by
  topography. Leaving it false would also make `check_dual_group_referrals` FAIL on any tree
  branch that ever refers a marrow-presenting NHL-NOS to Group I with `refer_code: "9591"`.
  **If the controller's merge check asserts the contract's eleven exactly, flip one boolean
  and delete one note — nothing else depends on it.** (The build brief relayed to this agent
  said "nine codes"; §2.4's own list is eleven. Worth reconciling the brief.)

- **Five codes are carried at `/3` although ICD-O prints them at `/1`.** 9765 MGUS, 9769
  immunoglobulin deposition disease, 9970 lymphoproliferative disorder NOS, 9971 PTLD NOS,
  and 9740 mastocytoma NOS (ICD-O reserves 9740/3 for mast cell sarcoma). Pathway §5.4 lists
  9971 among the /3→/1 changes; contract §1 applies behaviour changes **only** to 9718, 9725
  and 9751, and Pathway §4.1 states that every ICCC-2017 Group II range requires behaviour 3,
  so a `/1` here would remove the case from the group the reference file assigns it to.
  `behavior_code: "3"` is therefore the least-wrong reversible choice and each entry's
  `coding_note` says so. **Registrar decision:** either ratify /3 for these five, or extend
  the applied behaviour-change list — the second option needs a matching `behaviour_resolution`
  or an out-of-group exit for each, which is a bigger change than it looks.

- **9751 and 9754 present the clerk with two REDCap options carrying nearly identical text.**
  Layer 1 gives 9751 "Langerhans cell histiocytosis, NOS" and 9754 "Langerhans cell
  histiocytosis, NOS (replaces former 9751/1 through 9754/3 codes)". Pathway §6 reads them as
  "9751 (+ extent → 9754)", so this build treats 9754 as the documented-multisystem slot and
  9751/3 as LCH with extent unknown. **The tool is advisory and the clerk matches the whole
  option string by eye — two options whose first four words are identical is a real
  mis-selection risk that only the registrar can fix, at the REDCap end.** Neither name was
  edited here.

- **Three option lines are merged in the Layer 1 source markdown.** `Group 2- Lymphomas And
  Reticuloendothelial Neoplasms.md` line 30 carries 9814 and 9815 on one physical line,
  line 51 carries 9690 and 9691, and lines 57–58 split 9732/9733 mid-record. This no longer
  blocks the build — `build_database.py`'s `OPTION_HEAD_RE` was extended during this session
  and now splits merged headers correctly (verified: 91 options parsed, 89/89 names
  character-identical). **Left as a source-hygiene item, not a blocker**; a newline in three
  places would remove the dependency on that regex.

- **EBER ISH is counted under `"IHC"` in `diagnostic_tests_required`, not `"Molecular/PCR"`.**
  It is an in-situ stain read on a tissue section and §2.6 places it in the Tier 2 antibody
  adds, so a site with the Tier 2 panel satisfies the requirement naturally. The hard gate is
  carried explicitly by "EBER ISH" appearing in `ihc_markers_required` on 9719, 9724, 9725 and
  9766 (and in `ihc_markers_exclude` on 9659, 9708, 9726, where a positive EBER argues against
  the code). **HTLV-1 serology goes the other way — it is under `"Molecular/PCR"` on 9827,
  matching the convention `group_01_dt.json` already uses for the same code.** A tree branch
  that captures an HTLV-1 result must therefore declare `satisfies_tests: ["Molecular/PCR"]`,
  and a branch that captures EBER must declare `satisfies_tests: ["IHC"]`. **Tree agents: this
  is the pairing your `satisfies_tests[]` must match, or a fully worked-up case will report a
  phantom outstanding test.**

- **9687 does NOT list `"Cytogenetics/FISH"`.** Pathway §3.3 gives four validated FISH-free
  routes to Burkitt, so requiring FISH would report an outstanding test on every correctly
  worked-up case. **What FISH's absence costs is carried on the branch instead: §4.2 makes
  `provisional_pending` MANDATORY on every 9687 terminal reached without a FISH result.** The
  flow-signature and ctDNA routes must declare `satisfies_tests: ["IHC"]` — the entry names
  IHC, not Flow cytometry, deliberately.

- **`who_version` is `"WHO-HAEM5"` on 91 of 92 entries; 9680 alone is `"ICC-2022"`.** §5.3's
  arbitration table recommends "Follow ICC" on exactly one axis that changes a code boundary —
  a TdT-positive high-grade or diffuse large B-cell lymphoma stays **mature** with TdT noted
  and must not be reclassified as lymphoblastic. That governs 9680's upper boundary (and
  blocks 9727/9811 for those cases, noted in both). The other §5.3 rows either recommend
  capturing both systems (FL grading, Burkitt subtyping), recommend the **harmonized** 2024
  criteria rather than either classification (mastocytosis), or are registry decisions
  (9758/9759 stay in IId; 9659 stays in IIa). **Confirm this is the intended reading of "except
  where §5.3 says the registry follows ICC".**

- **9750 is repurposed as the MHN-NOS carrier.** §5.2 marks this P0 and offers two options —
  repurpose 9750 with a coding note, or leave the cases uncoded. This build took the first,
  because Goyal 2026 records that only 52% of cases referred as "malignant histiocytosis" are
  confirmed on expert review, and leaving MHN-NOS uncoded loses about half of that stream.
  **9750 is also the code that carries Erdheim-Chester tonight** (9749 not built, contract §1),
  with a visible `provisional_pending` naming ECD — so 9750 now carries two distinct meanings
  and both are documented in its `coding_note`. **Registrar to ratify, and to decide whether
  ECD should instead sit at 9750 permanently or wait for 9749.**

- **The three contract §1 redirects are recorded in the carrying code's `coding_note`, as
  asked:** ALK-negative ALCL → **9714** (Layer 1's "T cell and Null cell type" is the pre-split
  ICD-O-3.1 term spanning both; capture `alk_ihc: "negative"`); Erdheim-Chester → **9750**;
  Ph-like B-ALL → **9811**. Each note names the missing code, why it is missing, and what has
  to happen for it to be added.

- **17 codes are `terminal_reachable: false`**, all of them archaic ICD-O terms or adult-only
  entities that Pathway §3, §4, §5.2, §6 and §7.4 never name as an endpoint: 9597, 9661, 9662,
  9671, 9675, 9684, 9689, 9712, 9733, 9760, 9761, 9762, 9764, 9765, 9767, 9768, 9769. They are
  carried because Layer 1 carries them and the clerk may meet the wording on a historical file;
  the alias file is where those terms are retargeted. **If a tree agent wires a branch to any of
  these, flip the flag** — the field is a claim about this build, not about the code.

- **Chain roots (`nos_fallback_code: null`) are 9590, 9740, 9750, 9751 (both halves), 9758 and
  9759.** 9590 is the group root. The five IId roots are deliberate: Goyal 2026 excludes LCH
  (9751/9754) from the malignant histiocytic neoplasm category and excludes 9758/9759 by name
  as stroma-derived, so falling back from any of them to 9750 would upgrade a lesion without
  malignant cytology into the malignant bucket. There is no family-level NOS code for either
  family. **If the registry wants a single histiocytic root, that is a new code request, not a
  rewiring.**

- **`clinical_alert` is populated on 23 entries and left null everywhere §5.5 does not name the
  code** — including 9708 and 9726, where §3.7 calls HLH "a prognostic and clinical-alert flag
  on both". That text sits in `coding_note` instead, so the alert set stays exactly §5.5's.
  **If the registrar wants §3.7's HLH warning rendered, say so and it moves in one edit** —
  or the tree carries it at the node, which contract §7 also permits.
- **`g2mast_sarcoma_gate` is typed `ihc_checklist`, not `cytogenetics_dropdown`, although it reads
  a molecular result.** Forced by the engine agent's note above: `test_result_states` routes
  through `resolution_logic[]`, not `options[]`, and `resolution_logic` is documented on
  `ihc_checklist`. `cytogenetics_dropdown` (the natural type for a KIT result, and the type
  `group_01_dt.json` uses for CSF3R) takes `options[]` and would have left the declared states
  unrouted. **If `cytogenetics_dropdown` gains a `resolution_logic[]` path, retype this node.**
- **Branch-level `clinical_alert` was removed from this tree entirely** after the engine agent's
  note that it renders nowhere. Every warning now sits at node level, where it is rendered; the
  SM-AHN and ICC-provisional sentences that had been on branches were folded into their nodes'
  alert text rather than dropped. If branch alerts become rendered, four nodes here could carry
  a more targeted alert per branch. — g2_mastcell agent
- **Interaction between the morphology-layer agent's `behavior_code: "3"` default and this tree's
  use of 9740 as the family-level fallback.** That agent notes ICD-O reserves **9740/3 for mast
  cell sarcoma**, and is emitting a single 9740 entry with `behavior_code: "3"`. This tree emits
  9740 seventeen times as the *mastocytoma / mast-cell-family* label (skin mastocytoma, and every
  "cannot be established from this file" terminal), where the intended ICD-O behaviour is **/1**.
  So a 9740 terminal here will carry a behaviour that reads "sarcoma". Two ways out, both for the
  registrar: give 9740 a `/1` behaviour-split sibling (which would also give mast cell sarcoma a
  proper home and retire the 9741-plus-free-text fallback), or accept /3 on all of them and
  record the distinction in free text only. **This is the one item in this tree that could make a
  benign solitary skin mastocytoma register as a sarcoma.** — g2_mastcell agent

---

## Controller rulings, 2026-09-04 (these are decided, not open — recorded here so the trail is in one place)

- **`behaviour_resolution.values` keys are `"1"` / `"3"`, no slash.** Contract §3.1 wins over Pathway §7.3 item 1. The engine never interprets the key; the validator and the authored JSON both use the bare form. Reconciled.
- **Captured-variable VALUES follow Pathway §5.1 verbatim** — `alk_ihc` is `pos` / `neg` / `not done`, not `positive` / `negative`. Contract §1's worked example used the long form and was wrong. The controller normalises every tree fragment at merge; the pathway's vocabulary is the one that survives, because it is the document a future author reads.
- **`ISH` is added to the closed diagnostic-test vocabulary.** EBER in-situ hybridisation is not IHC: Pathway §4.3 makes EBER ISH on tissue the only entity-defining EBV test, LMP1 IHC explicitly cannot substitute (absent in latency I and 0, forbidden in plasmablastic lymphoma), and serology cannot upgrade any code. Reporting "IHC outstanding" to a site that has a full antibody panel but no ISH probe would name the wrong missing test. Additive to the shared vocabulary; no existing group is affected.
- **An undecidable entity boundary resolves to the node's `nos_fallback` at low confidence, never to "inside".** 9709 is a `/1` code outside Group II; defaulting to it would delete a case from the registry. Both the engine and the cutaneous tree reached this independently.
- **`deferrable: true` surfaces the follow-up row on every leaf, not only `unresolved`.** A case coded `/3` today on a criterion that can change in six months still needs the review.
- **Branch-level `clinical_alert` will be rendered.** It is the clerk-facing field (DT master §3E); 52 alerts in Group 1 — including three copies of "APL — haematological emergency" and the TAM "never code 9898" warning — have been invisible since the tool shipped. Group 1's output changing is the point.

## For the registrar — consequences worth knowing before the counts are used

- **EBER ISH gates 9708 and 9726.** A site without an EBER probe cannot reach either; those cases stop at 9702 with a named provisional. Deliberate — §3.7 warns that NK-phenotype hydroa-vacciniforme LPD mimics 9708 in a child, so without EBER the mimic cannot be excluded — but it means the 9708/9726 split (5-year disease-specific survival 87% against 11%) is unavailable below Tier 2, and those cases will accumulate at 9702. Same shape as the LCH `extent_unknown` bias: the direction must be published with the counts.

## ★ REGISTRAR ITEM 1 — 9740 behaviour. The one thing in this build that can record a cancer that does not exist.

Layer 1's option is `9740 - Mastocytoma, NOS`. Under ICD-O-3, **9740/1 is cutaneous mastocytoma
and 9740/3 is mast cell sarcoma** — one code, two very different diseases. But every
ICCC-2017 Group II range requires `behaviour = 3`, so a /1 assignment drops the case out of
Group II altogether, and the mast cell tree needs 9740 seventeen times as its family-level
"cannot be established" carrier.

As built tonight, 9740 is a single `/3` entry. **The consequence is that a solitary benign
skin mastocytoma registers with a sarcoma behaviour.** Nothing else in this build can do
that, and it is exactly the error the non-reportable terminal exists to prevent.

It was left as built rather than fixed, because fixing it means answering a question only the
registrar can answer: **does UCI register cutaneous mastocytoma at all?** The three options:

1. **Do not register it** — route the solitary-mastocytoma and skin-limited branches to the
   non-reportable terminal, as "mastocytosis in the skin without a marrow" already is. Most
   defensible clinically; contradicts Pathway §6, which assigns the code.
2. **Behaviour-split 9740** into `/1` (mastocytoma) and `/3` (the in-group carrier), the way
   9718, 9725 and 9751 are split. Mechanically clean — both halves carry the Layer 1 name so
   the exact-string check passes without needing the sibling exemption — but it puts every
   /1 case outside Group II, which is a systematic under-count of the subgroup.
3. **Leave it** and accept that IId mastocytoma counts carry a behaviour that overstates them.

Mitigation shipped tonight: 9740 carries a `clinical_alert` stating the conflict, so the
abstractor sees it at the point of coding rather than discovering it in the counts. Whichever
option is chosen, it is one boolean and a handful of branch edits.

Related, and also the registrar's: **Pathway §5.2 routes mast cell sarcoma to 9741** (*Indolent
systemic mastocytosis*) *"+ free text"* — plainly the wrong entity, chosen because §5.2 assumes
9740/3 is unavailable. If 9740 is behaviour-split under option 2, mast cell sarcoma should move
to 9740/3 and §5.2 should be corrected. The tool follows the pathway tonight.

---

## Histiocytic and dendritic tree (`g2_histiocytic`, `g2hist_*`) — registrar items

*Appended by the histiocytic subagent. Tree file: `scratchpad/g2_tree_histiocytic.json`, 15 nodes.*

### Registrar decisions

- [ ] **Add 9749 (Erdheim-Chester disease) to Layer 1** (contract §1, Pathway §5.4, §7.5).
  Tonight every confirmed ECD terminal emits **9750** carrying a `provisional_pending` that names
  Erdheim-Chester disease and says 9749 is pending — five branches on `g2hist_ecd`. The case stays
  in the registry, visibly provisional, and **the switch is one line per branch** when the code
  lands. 9749 must be added to **both** `code_ranges` and `morphology_codes` in `ICCC-2017.sqlite`
  (§9.1 item 12) or `iccc_code` will not populate.

- [ ] **Which REDCap row is house style for Langerhans cell histiocytosis — 9751 or 9754?**
  Layer 1 carries **both**: 9751 *"Langerhans cell histiocytosis, NOS"* and 9754 *"Langerhans cell
  histiocytosis, NOS (replaces former 9751/1 through 9754/3 codes)"*. The contract mandates the
  behaviour split on **9751** (§2.3), so 9751 is the default route. **9754 is used in exactly two
  places** and both are reversible in one line: (a) as the `nos_fallback` on `g2hist_lch_confirm`,
  chosen because 9754 has a single behaviour and can be named without an extent, whereas a bare
  "9751" fallback would be ambiguous between its `/1` and `/3` entries; (b) as the terminal for a
  report using a legacy collapsed eponym (Letterer-Siwe, Hand-Schüller-Christian, eosinophilic
  granuloma of bone, Hashimoto-Pritzker) with no current extent statement. If the registrar rules
  that 9754 is never to be used, both routes retarget to 9751/3.

- [ ] **Ratify or override `lch_extent_unknown_policy`** (§9.2, §9.3 — already outstanding; restated
  because this tree implements it). Default `retain_in_group_ii` + `extent_unknown`. Every
  `unresolved` leaf of the 9751 `behaviour_resolution` emits **9751/3**, records which imaging was
  actually done (`imaging_extent_modality`), and states in clerk-facing text that a skeletal survey
  plus abdominal ultrasound plus chest X-ray **under-calls multisystem disease** — a systematic
  ascertainment bias that must be published with the counts. Five imaging modalities each carry
  their own `unresolved.reason`. **Whichever way this is ratified, the direction must go out with
  the incidence figures.**

- [ ] **The high-grade indeterminate dendritic cell tumour currently exits as non-reportable, and
  that loses an incident cancer.** Pathway §5.2 gives it *"none — never 9751 and never 9756"*, and
  the tree follows that. But **Goyal 2026 places it INSIDE the MHN scope** (its table lists
  "high-grade indeterminate dendritic cell tumour (no code)" among the four MHN entities), and
  §9.1 item 5 makes **9750 the MHN-NOS carrier**. Those two rulings point opposite ways for a
  tumour that is overtly malignant. Options: (a) keep the non-reportable exit with the entity name
  recorded (built tonight); (b) route it to **9750** with `mhn_designation` = "MHN — indeterminate
  dendritic cell tumour, high-grade", consistent with §9.1 item 5. Affects one branch on
  `g2hist_mhn_algorithm` and one option on `g2hist_uncoded_exit`.

- [ ] **`refer_group: 11` is used twice** (`g2hist_minimum_panel`, `g2hist_mhn_algorithm`) for a
  melanocytic-marker-positive lesion. Contract §4.1 says Group II's only sanctioned `refer_group`
  target is **1**, "unless the pathway names one" — Pathway §3.8 names melanoma as the mandatory
  exclusion for 9757, which has no defining marker of its own, and melanoma is ICCC-3 **Group XI**.
  Marking such a case non-reportable would delete a real cancer. **Confirm 11 is acceptable**, or
  say what a melanoma-positive lesion should do instead.

- [ ] **`provisional_pending.resolving_test` has no value meaning "code pending".** The closed
  diagnostic-test vocabulary is Histology / IHC / Flow cytometry / Cytogenetics/FISH / Molecular/PCR
  / Referral only. The five ECD terminals record **`Molecular/PCR`** (a sequencing-grade BRAF V600E
  assay is the outstanding *laboratory* investigation) and put the truth — that the real resolving
  step is the registrar adding 9749 — in the clerk-facing `reason`. If a `Registry action` value is
  added to the vocabulary, those five branches should move to it.

### Variables coined by this tree (Pathway §5.1 has no row for them)

Declared per contract §5's instruction to say so. `cd1a` (positive/negative/not_assessable/not_done)
· `overt_malignant_cytology` (present/absent/uncertain) · `mhn_minimum_panel_status`
(complete/incomplete/not done) · `melanocytic_markers` · `clusterin` · `fdc_marker_count` ·
`fdc_subtype` (free text — 9758 covers both FDC sarcoma and EBV-positive inflammatory FDC sarcoma)
· `braf_v600e` · `braf_assay` (the pathway requires the assay be recorded but names no variable) ·
`ecd_radiology` · `imaging_extent_modality` (§5.1's `pet_ct_available` is y/n and **cannot
distinguish vertex-to-toes from the explicitly inadequate skull-to-mid-thigh scan**, which is the
whole point of §4.1) · `extent_unknown` · `diabetes_insipidus` · `uncoded_entity_name` ·
`myeloid_sarcoma_excluded` · `clonal_relatedness_tested` (§5.1 has `secondary_mhn_status` but its
value set has no way to say "clonal relatedness was never tested" — recording "MHN-AHN" there would
claim a test that was not run).

**Value-spelling divergence to ratify:** §5.1 spells the marker variables `pos / neg / not done`;
contract §3.4's closed `test_result_states` vocabulary is `positive / negative / not_assessable /
not_done`. Where both apply the contract wins (§0), so this tree uses the **underscore vocabulary
throughout** for `cd163`, `cd1a`, `cd207_langerin` and `alk_ihc`. `s100` additionally uses `patchy`,
which is in §5.1 but not in the closed vocabulary — `s100` is therefore deliberately **not**
declared in any `test_result_states` block.

### Notes for the merge

- One **cross-tree `next_node`**: `g2hist_document_inventory` → **`g2_lineage`** (main tree), for a
  case that turns out to be a lymphoma. The id comes from contract §4.2's NOS-fallback table. If the
  main-tree author names that node differently, this is the one reference to update.
- **`satisfies_tests` is used nowhere in this tree**, deliberately: the terminal codes'
  `diagnostic_tests_required` lists are authored elsewhere, and contract §3F requires any value to
  appear in the terminal's own list. An unverifiable `satisfies_tests` suppresses a real workup gap.

### Closed by the coordinator's ruling, 2026-09-04 (same agent, later the same session)

- **RESOLVED — branch-level `clinical_alert` is now rendered.** Ruling: `clinical_alert` is the
  clerk-facing warning field (DT master §3E), the counterpart of the author-facing
  `coding_note`; an alert on the branch carrying the risky choice is the field working as
  designed. Implemented: on an `options[]` entry (and a behaviour leaf) it renders **with the
  option, before it is taken**; on a dropdown option it renders the moment that option is
  selected, still before Continue; on a rule/band/override/fallback/leaf that **terminates**
  it reaches the output block in the entry-alert treatment; on one that **routes onward** it
  is carried exactly one hop and banners on the screen the clerk acts on next. Shown once
  where the branch and the entry (or the next node) carry the same string. Group 1's rendered
  output changed in 167 of 1057 swept scenarios, additively only.
- **RESOLVED — `.orow--provisional` and `.orow--followup` added to `uccf-tool.css`**, plus
  `.opt__alert` for the compact option warning. All three use `var(--…)` tokens only; both new
  output rows are marigold cautions (coral stays reserved for `clinical_alert`) and are
  separated from each other by border treatment — solid 2px vs dashed 3px — as well as by
  their own uppercase row labels, so no state rests on colour alone.
- **RATIFIED, recorded in code comments so they are not "improved" away**: an undecidable
  `entity_boundary` goes to the node's `nos_fallback` at low confidence and is never read as
  either side; `deferrable` surfaces the follow-up row on every leaf, not only `unresolved`.

---

## `aliases_group_02.json` — open items (alias-layer author, 2026-09-04)

File: `scratchpad/aliases_group_02.json` — 367 entries, 89 of 89 buildable Layer 1 codes covered.
Builder: `scratchpad/work/build_g2_aliases.py`. Validator: `scratchpad/work/verify_g2_aliases.py`
(27 checks, all passing). Negative controls: `scratchpad/work/negative_controls.py` (28 deliberate
defects, all caught).

### Decisions taken that a person should confirm

- **`needs_ihc_tree` is `true` on every entry, and `ihc_tree_id` is therefore non-null on every
  entry.** This departs from `aliases_group_01.json`, where 221 of 283 entries are `false` with a
  null `ihc_tree_id` but a populated `tree_entry_node`. Two reasons: (a) the build contract requires
  every `ihc_tree_id` / `tree_entry_node` to be one of the four legal pairs, and a null tree id is
  not one of them; (b) it is clinically true for Group II in a way it is not for Group I — all four
  Group II entry nodes are `document_inventory` nodes, and Pathway §2.3 means no Group II alias can
  emit a code without the not-lymphoma gate first (FNAC calling "NHL" has PPV 71.4%; a child with a
  peripheral node is ~14× more likely to have mycobacterial disease than cancer). The cost is that
  the field no longer discriminates *within* Group II — `confidence` now carries that signal alone.
  **If the engine renders "requires decision tree" per alias, confirm this reads correctly to a
  clerk.** Reversible: one dict in the builder.
- **Entries that reach a non-reportable or uncoded terminal carry `maps_to_iccc3_subgroup_id: null`**
  (31 entries). The Master schema types that field as a string. Null is the honest value — there is
  no code, so there is no subgroup — but if the validator requires a string, the field needs an
  agreed sentinel rather than a subgroup being invented.
- **`nci_concept_id` is null on 74 entries** — local terms, molecular notation, uncoded WHO entities,
  9662 (no NCIt concept), 9727 (the recorded lookup returned Hepatosplenic T-Cell Lymphoma, a label
  mismatch) and terms the Group II lookup session did not record. No ID was invented; every non-null
  value is traceable to §1 of `Group 2 — Alias Build Instructions.md`.

### Blockers that need the registrar

- **9750 / MHN-NOS (Pathway §5.2, §9.3) is still undecided and now has three aliases pointing at it.**
  `Malignant histiocytosis`, `Malignant histiocytic neoplasm` and `MHN-NOS` all route to 9750, and
  so does `Erdheim-Chester disease` (because 9749 is not built). Only ~52% of cases referred as
  "malignant histiocytosis" are confirmed on expert review. Either 9750 is formally repurposed as
  the MHN-NOS carrier with a coding note, or these aliases are pointing a clerk at a code whose name
  does not mean what the report says.
- **9715 / 9749 / 9819** — the three ICD-O-3.2 additions. Aliases retarget to 9714 / 9750 / 9811 and
  every affected `notes` string opens with `REGISTRAR ACTION PENDING`, so they are greppable. When
  Layer 1 gains the codes, `grep "REGISTRAR ACTION PENDING" aliases_group_02.json` finds all seven
  entries.
- **9728 / 9729 retirement.** `Precursor B-cell lymphoblastic lymphoma` → 9811 and
  `Precursor T-cell lymphoblastic lymphoma` → 9837, with the reason in `notes`. Greppable on
  `RETIRED`. Query `i_morph` for existing records before the REDCap change lands.
- **Indolent T-cell lymphoma of the GI tract** — Pathway §5.2 says it "needs a code decision".
  Aliased to 9702 plus site, which is the pathway's own stated fallback, but it is a placeholder.

### Cross-file consequences

- **`aliases_group_01.json` now has a stale note.** Six of its entries (`Burkitt cell leukemia`,
  `Burkitt leukaemia`, `FAB L3`, `L3 ALL`, `Leukaemic Burkitt lymphoma`, `Mature B-cell ALL`) say
  *"The same alias string must be carried in aliases_group_02.json … THAT MIRROR DOES NOT YET EXIST
  and is a flagged gap."* **The mirror now exists** — all six are present here against 9687. Those
  six Group 1 `notes` strings should have that sentence updated when someone next touches Group 1.
- **Cross-group abbreviation collisions the `alias_index.json` build will have to arbitrate.**
  This file claims: `MCL` → 9673 mantle cell (mast cell leukaemia must be typed in full); `MF` →
  9700 (Group I uses it for myelofibrosis); `MM` → 9732 (melanoma); `SS` → 9701 (synovial sarcoma,
  Group IX); `PCL` is *not* aliased here to avoid a third collision; `HD`, `ATL`, `PBL`, `MCHL` are
  aliased with an explicit caution in `notes` and `confidence` lowered. **Whoever builds
  `alias_index.json` needs a documented policy for one string resolving in two groups** — the notes
  warn the clerk, but the index has to decide what the search returns.

### Terms deliberately left out

- **Hypersensitivity reaction to mosquito bites** — Willemze places it beside HV-like LPD under
  cutaneous chronic active EBV disease, but neither the pathway's §4.5 non-reportable inventory nor
  its §5.2 uncoded-entity table names it, so there is no sourced destination. Add it if the
  registrar wants an NK-lineage counterpart to the 9725 entry.
- **Primary cutaneous CD8+ aggressive epidermotropic cytotoxic T-cell lymphoma** — a real WHO entity
  with no ICD-O-3 code and no fallback stated in §5.2. Aliasing it would have meant choosing a code
  the sources do not choose. (`Primary cutaneous acral CD8+ T-cell lymphoma`, which §5.2 *does*
  place at 9702, is included.)
- **Bare `CLL`** is included but at `confidence: low` — written alone it usually means the Group I
  leukaemic presentation. It is here only so a nodal presentation reported as CLL still resolves.

## g2_lymphoid_main (main lymphoid spine) — 20 nodes

**Deviations from the pathway's own sketch**

- **§7.2 pencils `g2_notlymphoma_gate` as an `ihc_checklist`; built as a `document_inventory`.** It is a gate,
  not a refining node, and per §3D an `ihc_checklist` must carry a non-null `nos_fallback` — falling back to
  "lymphoma NOS" when the TB workup is inconclusive is exactly the over-call this gate exists to prevent.
  As a `document_inventory` its fallback is null and the inconclusive paths route to repeat-or-escalate.
  **Decision needed:** ratify, or add a node type that gates without an NOS floor.
- **§4.2 gives `g2_fish` the NOS fallback "the code that entered the node"; JSON cannot express that.**
  Set to 9680 with a reason that names the rule, and every entering morphology is written into the option
  `finding` text so the correct code is emitted on a match rather than through the fallback. **Decision needed:**
  either accept 9680 as the static floor, or the engine gains a `nos_fallback: "carry_forward"` sentinel.
- **§4.2 gives `g2_all_fish` the NOS fallback "9811 / 9837"; one node can carry one code.** Set to 9811, and
  T-lineage cases are terminated at 9837 inside `g2_precursor` and on their own option in `g2_all_fish`, so no
  T-lineage case can fall through to the 9811 floor. Verified by the reachability check.
- **One extra node beyond the binding inventory: `g2_specimen_escalation`.** §2.4 requires *inadequate* to route
  to repeat-or-escalate and never to 9590, which needs a destination to exist. It is also the landing point for a
  trace-positive Ultra, an Ultra-negative granulomatous node, and a paediatric FNAB called "neoplastic".

**Choices the pathway left open**

- **`test_result_states` for `fish_status`.** §5.1 gives the values `done / failed / not available / not indicated`,
  but contract §3.4's closed state vocabulary has no `done`. Declared as
  `positive / negative / not_assessable / failed / not_available / not_done`, and `done` is expressed as
  positive-or-negative. **Registrar to reconcile §5.1 with the closed vocabulary.**
- **`provisional_pending.resolving_test` must come from the closed diagnostic-test vocabulary**
  (`Cytogenetics/FISH`, `Flow cytometry`, `Histology`, `IHC`, `Molecular/PCR`, `Referral only`). That vocabulary
  has **no entry for in-situ hybridisation**, so an EBER-resolving provisional cannot name its own test. All eight
  provisionals in this tree resolve on `Cytogenetics/FISH` and the EBER-outstanding cases are carried on
  `upgrade_path` instead. **Decision needed: add `ISH` to the test vocabulary**, or EBER can never be shown as an
  outstanding workup row anywhere in Group II.
- **`satisfies_tests` policy, stated so the next author can hold the line.** Declared *only* on branches whose own
  `finding` text plus `detection_method` name a karyotype/FISH/RT-PCR result — 18 branches, all in `g2_fish` and
  `g2_all_fish`. Deliberately **not** declared on IHC-derived terminals: the morphology entries are being written
  by another agent, and a `satisfies_tests` value the code does not require is an inert no-op that reads to the
  next author as a live claim. `g2_molecular` originally claimed `Molecular/PCR`; removed, because 9819 is
  precisely the molecular result still outstanding there.
- **`not_assessable` vs `negative` (§3.4).** Enforced as the contract's operative test rather than as
  "different destination tuple": a `not_assessable` branch must exist wherever a `negative` branch does, must never
  take a `negative` branch's non-reportable or refer exit, must never emit a code only a `positive` branch
  establishes, and must never be textually identical to the negative branch. Under a strict
  "must differ in destination" reading, three branches would fail — all three emit 9702 alongside a negative
  branch, which is correct medicine (EBER is not entity-defining for Burkitt, and 9702 is the ceiling for an
  ungated NK/T case). **Registrar/engine owner to confirm which reading the validator will implement.**
- **9709 is never emitted by this tree**, so `9709/3` cannot be produced here by construction.
- **Codes in the Group II list this tree cannot reach, and why.** `9661` Hodgkin granuloma and `9662` Hodgkin
  sarcoma are archaic synonyms of mixed cellularity and lymphocyte depletion — alias-file business, not tree
  business. `9675` (Working Formulation "mixed small and large cell, diffuse") likewise. `9762` heavy chain
  disease, `9765` MGUS, `9769` immunoglobulin deposition disease and `9970` lymphoproliferative disorder NOS have
  no defensible paediatric route and are deliberately left unreachable rather than given a speculative branch —
  **confirm this is what the registrar wants before `terminal_reachable` is set on those entries.** The remaining
  unreached codes belong to the cutaneous, histiocytic and mast-cell trees.
- **MPO threshold is not hard-coded** at either MPAL exit (`g2_lineage`, `g2_precursor`). The branch keys on
  `lineage_count`, and the `reason` instructs the clerk to record `mpo_pct` and `mpo_method`.
- **No new captured variables were coined.** Clinical and site facts that §5.1 has no variable for — anterior
  mediastinal mass, localised head-and-neck presentation, splenic/intestinal primary, body-cavity effusion,
  lung involvement — are carried as tick items in a "Clinical and site context" marker group rather than as
  invented variables. If the engine would rather have them as variables, they are the ones to add.

### Engine/validator contradiction, live as of 2026-09-04 — needs the validator agent

- **`markerOk()` now accepts a marker name containing colons; `build_database.py` still
  rejects one.** The engine reads only a *trailing* `:strong`/`:weak` as an intensity suffix,
  so `NPM1::ALK t(2;5) by FISH or RT-PCR` resolves to the marker actually declared on the
  node. The validator still reports these as `positive[] token … — the only allowed suffixes
  are ':strong' and ':weak'` and FAILs the build on three Group II tokens (`g2_precursor`
  rule 4, `g2cut_cd30_lpd` rule 1, `g2hist_ecd` rule 1). The coordinator's ruling was that
  the validator should **accept** the token and separately require every token's marker name
  to be declared in that node's `marker_groups` — under the new parse all three are declared,
  so that second check passes. Engine side is done and proven; the validator half has not
  landed. `build/build_database.py` is not mine to edit.
- Worth knowing for whoever picks that up: `g2hist_ecd` rule 1 was **not merely dead** under
  the old parser — the case fell through to rule 6 and took a different destination
  (9750 vs a continuing node). Two dead rules, one silent mis-route.

## Controller findings from driving the real tool, 2026-09-04 (all fixed, recorded so the lesson survives)

- **`test_result_states` replaced the node's own control instead of adding to it**, on 15 of
  Group II's 61 nodes — the entry gate, both FISH dropdowns, and ten `ihc_checklist` nodes
  including `g2_matureB` with its 37 marker rules. The build passed, 74 checks, 0 FAIL; the
  data-level traversal passed 10 of 10; the engine's own 102-assertion fixture passed. **Only
  opening the tool in a browser found it**, because every automated layer tested the data or
  the renderer in isolation and the fault was in the seam between them. If one habit survives
  this build, it is that a green build is not a working tool.
- **`markerOk()` split marker names on the first colon**, so `NPM1::ALK t(2;5) by FISH or
  RT-PCR` looked up a marker called `NPM1`. Two rules were dead and one **silently mis-routed**
  — `g2hist_ecd` fell through to a later rule with a different destination. `::` is the standard
  fusion separator and is used throughout this project, so the engine now strips only a trailing
  `:strong` / `:weak`.
- **Two marginal-zone rules were dead behind a broader earlier rule**, so splenic marginal zone
  lymphoma (9689) and the MNDA/IRTA1 route to 9699 could never be reached. Found by replacing
  the rule-order lint's positional heuristic with a subsumption test.
- **`g2_tfh` carried a `positive[]` token that was never declared in its `marker_groups`**, so
  the "only 1 TFH marker" rule was dead and a single-marker case fell to the node's fallback —
  which is 9705 carrying the reason *"Two or more TFH markers are expressed"*. A claim the case
  did not support, on the highest-volume correction in IIb3.
- **`terminal_reachable` had drifted from the data on 12 entries.** Now derived from the trees
  rather than authored — the same failure mode as Group 1's `redcap_option_verified`.
- **13 inert `satisfies_tests` declarations removed** (3 on branches that emit no code, where
  `finish()` never applies them; 10 naming a test the terminal code does not require).

### Two engine decisions from the browser pass, 2026-09-04 — both deviate from a literal reading of the brief

- **`test_result_states` AUGMENTS the node's control; it does not replace it.** Contract §3.4
  says "render those states as the node's answer options", which I implemented literally, and
  it emptied 15 of 61 Group II nodes of their own control — the group's entry node lost its
  10-option specimen ladder, two dropdowns lost 13 findings each, and ten `ihc_checklist`
  nodes lost their marker grids so no `positive[]` rule could match. Ruled and fixed: the
  selector renders **above** the native control (an option list advances on tap, so the state
  has to be settable before that tap), choosing a state captures and re-renders **without
  advancing**, and the node still resolves through its own options or rules. §3.4's wording
  should be amended to say "augments" before another group adopts the construct.
- **A `provisional_pending`'s `resolving_test` is now listed as an outstanding workup item.**
  The brief said a provisional "must not silently lower the confidence value". Implemented
  literally, the Jaw-Burkitt case rendered **CONFIDENCE HIGH** and "Workup: complete — no
  outstanding tests" directly above a Provisional row reading "MYC status unknown; HG/LBCL-11q
  and HGBL-DH not excluded. Resolved by: Cytogenetics/FISH." 9687 requires only Histology and
  IHC, so nothing was missing by the entry's own list. That is the panel positively asserting
  completeness while naming an unresolved test — the exact overstatement class this tool
  exists to avoid. The named provisional row is untouched and is still not a confidence proxy;
  the test simply joins the workup list under its own name with its own status dropdown, and
  confidence falls to `medium` through the pre-existing outstanding-test rule. Nothing is
  silent. **Flagging it because it is a deviation from an explicit instruction** — overrule me
  if the registrar prefers HIGH there, but I do not think they will.
