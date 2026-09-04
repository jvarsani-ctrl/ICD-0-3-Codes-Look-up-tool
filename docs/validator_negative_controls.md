# Group II checks — negative controls

Evidence that the six checks added to `build/build_database.py` for Group II actually
catch what they claim to. Method per `memory/data.md` §5A and Decision Tree master §4:
break the data deliberately, confirm the check FAILs, restore, confirm it passes — and
separately confirm it does **not** fire on correct data, because a false FAIL is the more
corrosive failure.

## The fixture

`scratchpad/fixture/data/database/group_02_dt.json` — a small but schema-complete Group II
file: 9 morphology entries (names taken character-for-character from Layer 1, including the
9718 `/1` behaviour-split half that rides the sibling exemption), 8 nodes across two trees
(`g2_lymphoid_main` / `g2_cutaneous`), and at least one live instance of every one of the
five contract §3 constructs plus a viral-gated 9719 terminal behind a real EBER gate.
It is not `data/database/group_02_dt.json` and was never written there — that file is owned
by other agents and did not exist during this work.

Runs are:

```
python3 build/build_database.py --repo <scratchpad>/fixture \
        --layer1 "/Users/jay/Ai Environment/Cancer Registry/ICD coding"
```

## The false-FAIL control (correct data)

On the unmodified fixture the group_02 section reports **0 FAIL**, and each of the six
checks reports OK against real content rather than an empty NOTE:

```
OK  1 behaviour_resolution block(s) well formed; every 'unresolved' names the /3 half
OK  2 provisional_pending block(s) well formed; none names a test it also discharges via satisfies_tests
OK  1 prior_probability block(s) well formed, display-only, none on a code-emitting branch
OK  3 test_result_states block(s) well formed; 2 node/variable pair(s) route not_assessable away from negative
OK  1 entity_boundary block(s) well formed; no 9709/3 anywhere in the file
OK  viral-gated terminal(s) 9719 reachable only where the gating test is established positive
```

`check_viral_gates` additionally has a **real-world** positive control: it runs unchanged over
`data/database/group_01_dt.json`, which emits 9827 at `ml_atll_subtype` behind an HTLV-1 gate,
and passes. Group 1 spells that variable `htlv1_status` where the Group II vocabulary says
`htlv1_serology`; the check accepts both, because the clinical fact and not the spelling is
what it is about. Had it not, a correct file would have been failed over a synonym.

Two defects the fixture exposed in checks *other* than the six — both fixed in
`build_database.py`, both false FAILs on correct Group II data:

1. `check_non_reportable_terminals` read every `provisional_pending` block as an unflagged
   code-less terminal, because §3.2 requires a clerk-facing `reason` on it and that check
   treats "a `reason` and no destination" as a terminal that forgot to declare itself. Fixed
   with `is_provisional_pending_object()`, scoped exactly like the existing
   `is_nos_fallback_object()` — the key it hangs off **and** its shape, so it can never
   absorb a real code-less terminal.
2. My own first draft of `check_test_result_states` treated a single option that merely
   *records* `fish_status` as the node *branching on* it, and demanded a state declaration
   for a test the node does not actually offer choices about. Tightened: a `when` naming the
   variable is a branch; a `captures` is only a branch when two or more branches record
   different states of it.

---

## `check_behaviour_resolution` (contract §3.1)

**What it catches.** Catches a `behaviour_resolution` block whose `unresolved` half is missing or points at `/1` — the case where an unstated clinical history silently deletes a reportable cancer from the registry — plus the shape rules: required keys, the variable declared where the engine can read it, exactly the `"1"`/`"3"` keys, one destination per leaf, real (code, behaviour) pairs, and a `follow_up_review` behind every `deferrable: true`.

### Control 1 — `unresolved` deleted from the block (the author read the `/1` and `/3` values as exhaustive)

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2cut_large_cell_fraction (options[1]): behaviour_resolution.unresolved is REQUIRED (contract §3.1). Without it the engine has no answer for a file that never states the behaviour, and the case leaves the node with no code at all — a reportable childhood cancer dropped from the registry rather than coded
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 2 — `unresolved` left in place but pointed at the `/1` half — the silent-deletion defect

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2cut_large_cell_fraction (options[1]): behaviour_resolution.unresolved emits behavior_code '1' where '3' is required — under values[] the key IS the behaviour, so a mismatch files the case under a behaviour nobody chose (contract §3.1)
FAIL  node g2cut_large_cell_fraction (options[1]): behaviour_resolution.unresolved names 9718/1. It must name the /3 half. Defaulting an unresolved behaviour to /1 does not mis-code the case — it silently deletes a reportable cancer from the registry, because /1 is outside ICCC-3 Group II entirely. Code the reportable half and let the clinical history downgrade it later (contract §3.1)
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 3 — `variable` abbreviated to `self_healing_hx`, a near-miss on the declared `self_healing_history`

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2cut_large_cell_fraction (options[1]): behaviour_resolution.variable 'self_healing_hx' is not declared in this node's captured_variables[] (contract §5) — the engine has nowhere to read the answer from, so the criterion is asked and then discarded
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 4 — `deferrable` flipped to true with no `follow_up_review` written

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2cut_large_cell_fraction (options[1]): behaviour_resolution.deferrable is true, so a non-empty 'follow_up_review' saying what re-opens the case is required — a deferral with no stated trigger is an abandonment (contract §3.1)
```

Restored: **BUILD PASSED**, 0 FAIL.

---

## `check_provisional_pending` (contract §3.2)

**What it catches.** Catches a provisional whose `resolving_test` is outside the closed diagnostic-test vocabulary (so it can never be matched and resolves to nothing), one attached to a branch that emits no code, an `alternative_codes[]` entry this file cannot actually code — and, the reason it exists, a branch that names the same test as both `resolving_test` and `satisfies_tests`, claiming it outstanding and discharged at once.

### Control 1 — `resolving_test` written as `"FISH"` where `"Cytogenetics/FISH"` was meant

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_burkitt_fish (resolution_logic[3]): provisional_pending.resolving_test 'FISH' is not in the closed diagnostic-test vocabulary (Cytogenetics/FISH, Flow cytometry, Histology, IHC, IHC or flow cytometry, Imaging, Molecular/PCR, Referral only). A value nothing can match names no real outstanding test, so the provisional reads as specific and resolves to nothing
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 2 — the same branch declares `Cytogenetics/FISH` as both `resolving_test` and `satisfies_tests`

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_burkitt_fish (resolution_logic[3]): this branch names 'Cytogenetics/FISH' as provisional_pending.resolving_test AND lists it in satisfies_tests. That claims one test simultaneously outstanding and discharged — the provisional says the code may be overturned by it, satisfies_tests strikes it off the outstanding-workup list so nobody is asked for it. The case then reads better evidenced than the file itself says it is. Drop one; they cannot both be true (contract §3.2, §6)
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 3 — a provisional attached to a continuing branch that emits no code

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_burkitt_fish (resolution_logic[2]): provisional_pending on a branch that emits no morphology_code. A provisional QUALIFIES a code; with no code there is nothing to overturn and nothing is rendered (contract §3.2)
```

Restored: **BUILD PASSED**, 0 FAIL.

---

## `check_prior_probability` (contract §3.3)

**What it catches.** Catches a display-only prior that has been given decision-making weight: one carrying a destination of its own, or one sitting on a code-emitting branch where it reads as the evidence for that code — the exact inversion of its purpose. Also catches `expected_positive_pct` written as a number, which asserts a precision the sources do not publish.

### Control 1 — `prior_probability` moved from the node onto the code-emitting branch it appears to justify

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_burkitt_fish (resolution_logic[0]): prior_probability sits on a branch that emits 9687. Rendered beside a code it reads as the evidence for that code, when its entire purpose is the opposite — to say that this result was expected and is weakly informative. Move it to the node's question, its marker/test group, or a continuing branch (contract §3.3, §6)
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 2 — `expected_positive_pct` written as the number 30 rather than the string "30"

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_burkitt_fish ((node level)): prior_probability.expected_positive_pct must be a non-empty STRING (30) — the sources give ranges and bounds ("70-80", "<4"), and a number here quietly asserts a precision nobody published (contract §3.3)
```

Restored: **BUILD PASSED**, 0 FAIL.

---

## `check_test_result_states` (contract §3.4)

**What it catches.** Catches a node that branches on `eber_status`, `fish_status` or `fna_adequacy` without declaring its states or without offering `not_assessable`, a state outside the closed vocabulary (a trailing space is enough), an undeclared variable — and, the load-bearing rule, a `not_assessable` branch routed to the same destination as `negative`, which turns a result nobody could read into evidence of absence.

### Control 1 — the `not_assessable` branch given the same destination as `negative` (9702/3)

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_eber: the not_assessable branch for 'eber_status' (resolution_logic[2]) lands on code 9702/3 — exactly where the negative branch (resolution_logic[1]) lands. A result that could not be read is not a negative result: negative means the finding is absent and the differential narrows, not_assessable means nobody knows and the block has to be recut or the patient re-biopsied. Routing them together turns a missing result into evidence of absence, on a screen that looks complete. Give not_assessable its own branch, and do not let it emit a code the negative branch's evidence would have excluded (contract §3.4, §6; Pathway §2.4, §4.3, §7.3 item 4)
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 2 — a trailing space on `"not_assessable "` in the states list

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_eber: test_result_states state 'not_assessable ' is not in the closed vocabulary (adequate · failed · inadequate · negative · not_assessable · not_available · not_done · not_indicated · positive) (contract §3.4)
FAIL  node g2_eber: test_result_states for 'eber_status' omits 'not_assessable'. This test fails in a way that is neither positive nor negative, and with no state for it the clerk has to file an unreadable result as one of the two real answers (contract §3.4)
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 3 — `not_assessable` dropped from the states list for `eber_status`

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_eber: test_result_states for 'eber_status' omits 'not_assessable'. This test fails in a way that is neither positive nor negative, and with no state for it the clerk has to file an unreadable result as one of the two real answers (contract §3.4)
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 4 — `variable` set to `ebv_status`, which the node does not declare

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2_eber: test_result_states.variable 'ebv_status' is not declared in this node's captured_variables[] (contract §5) — the states are offered and the answer has nowhere to go
FAIL  node g2_eber branches on 'eber_status' but declares no test_result_states for it. Every branch on this test has to offer 'not_assessable', and the node has to say so where the engine can see it (contract §3.4)
```

Restored: **BUILD PASSED**, 0 FAIL.

---

## `check_entity_boundary` (contract §3.5)

**What it catches.** Catches a malformed 9709/9702 boundary — missing keys, an undeclared variable, a non-numeric threshold, an operator outside the closed set, a (code, behaviour) pair with no entry, or an `outside_code` equal to `inside_code`, which makes the question unanswerable in principle. Plus the standalone whole-file assertion that 9709 never carries `behavior_code: "3"` anywhere.

### Control 1 — `outside_code` set to 9709 — the same code as `inside_code`

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2cut_large_cell_fraction (options[0]): entity_boundary.outside_code equals inside_code (9709). Crossing this boundary changes the ENTITY, not the behaviour — if both sides carry the same code the node asks a question whose answer cannot matter, and the out-of-entity case is coded as the entity it is not (contract §3.5)
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 2 — `inside_behavior_code` changed to "3" ("it is a lymphoproliferative disorder, so /3")

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2cut_large_cell_fraction (options[0]): entity_boundary inside side emits 9709/3, which has no morphology_entries[] object in this file (contract §3.5)
FAIL  9709 appears with behavior_code "3" at 2 site(s): decision_trees[1].nodes[0].options[0] (morphology_code), decision_trees[1].nodes[0].options[0].entity_boundary (inside_code). There is no 9709/3 — Pathway §7.5 says in terms that 9709 must NOT get a /3 entry, and contract §3.5 makes it the single most likely invalid code this group can produce. An out-of-entity case is 9702/3 via entity_boundary, which is a DIFFERENT code, not a re-behavioured 9709
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 3 — the 9709 morphology_entries object given `behavior_code: "3"`

Build result: **BUILD FAILED (as designed)**

```
FAIL  node g2cut_large_cell_fraction (options[0]): entity_boundary inside side emits 9709/1, which has no morphology_entries[] object in this file (contract §3.5)
FAIL  9709 appears with behavior_code "3" at 1 site(s): morphology_entries[4] (morphology_code). There is no 9709/3 — Pathway §7.5 says in terms that 9709 must NOT get a /3 entry, and contract §3.5 makes it the single most likely invalid code this group can produce. An out-of-entity case is 9702/3 via entity_boundary, which is a DIFFERENT code, not a re-behavioured 9709
```

Restored: **BUILD PASSED**, 0 FAIL.

---

## `check_viral_gates` (contract §6, Pathway §5.5)

**What it catches.** Catches a definitionally viral code (9678, 9738 / 9827 / 9719, 9724, 9725 / 9737) reachable along any route on which its virus result was never established positive — a path property, not a schema property, so it is a reachability walk rather than a shape check.

### Control 1 — a 9719 terminal added on the exhausted-material route, where EBER never returned

Build result: **BUILD FAILED (as designed)**

```
FAIL  viral-gated terminal 9719 is emitted at g2_eber_repeat (options[1]) on a route where EBER ISH was never established positive. 9719 is DEFINITIONALLY viral — the virus is part of the entity, not an association found beside it — so a case coded here without the result reads as a confirmed diagnosis that nothing in the file supports (contract §6; Pathway §5.5). Capture EBER ISH positive on every route that reaches it (a node or branch `captures`, a `when`, or a `positive[]` marker), or send the untested case to the NOS fallback instead.
```

Restored: **BUILD PASSED**, 0 FAIL.

### Control 2 — the 9719 rule re-conditioned on `eber_status: "not_done"` — the variable is still captured, just not positive

Build result: **BUILD FAILED (as designed)**

```
FAIL  viral-gated terminal 9719 is emitted at g2_eber (resolution_logic[0]) on a route where EBER ISH was never established positive. 9719 is DEFINITIONALLY viral — the virus is part of the entity, not an association found beside it — so a case coded here without the result reads as a confirmed diagnosis that nothing in the file supports (contract §6; Pathway §5.5). Capture EBER ISH positive on every route that reaches it (a node or branch `captures`, a `when`, or a `positive[]` marker), or send the untested case to the NOS fallback instead.
```

Restored: **BUILD PASSED**, 0 FAIL.

---

## `parse_redcap_options` (work item 1) — the Layer 1 parser

Not a check, but the thing every name check stands on, so it gets the same treatment.

**What changed.** Each fenced block in a `RedCap Options/Group N- ….md` file is now parsed as
one text rather than line by line. Three Group 2 options had run together onto one physical
line or been split across two, and a line-oriented parser cannot read either shape.

**Totals, all twelve groups, before and after.** Only group 2 moves; the multi-name behaviour
(a code listed under several subgroups, `names[]` / `options[]`) is untouched.

| Group | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| before | 83 | **88** | 92 | 19 | 5 | 98 | 91 | 71 | 136 | 158 | 282 | 30 |
| after | 83 | **91** | 92 | 19 | 5 | 98 | 91 | 71 | 136 | 158 | 282 | 30 |
| multi-name codes (unchanged) | 0 | 0 | 45 | 6 | 0 | 0 | 18 | 19 | 0 | 0 | 2 | 1 |

Group 2's 91 names match `scratchpad/g2_layer1_names.json` **key by key**, exactly. Nothing
else in any group changed — verified by diffing old against new parser output per code, both
the `names[]` and the `options[]` list.

**The two limits that keep other groups byte-identical**, each of which was found by diffing
rather than reasoned about in advance:

* A name is truncated at the first newline; only the *header* may straddle a line break. The
  Group 3 file carries a bold-wrapped duplicate, `**9381, 9381 - Gliomatosis cerebri, NOS**`,
  which is deliberately not an option header — without the truncation the option above it
  (9380 "Diffuse astrocytoma, low grade") would have swallowed the whole bold line.
* Only ASCII horizontal whitespace is collapsed. Seven Group 7 names contain a non-breaking
  space (`Endocrine tumor, functioning, NOS\xa0(Note: …)`). That character is part of the
  string the clerk sees in REDCap, so normalising it away would manufacture exactly the drift
  the exact-string rule exists to detect.

**Negative control — did the fix restore *enforcement*, or only raise a count?**

Both parsers were run against the same fixture entries and handed to the unmodified
`check_redcap_exact_names`.

A. The three codes the old parser lost entirely (authored the realistic way, with
`redcap_option_verified: false`, because an author who cannot find the option string writes
that):

| code | name correct | name drifted (trailing space) |
|---|---|---|
| 9815 | old WARN / new WARN (stale flag) | old **WARN** / new **FAIL** |
| 9691 | old WARN / new WARN (stale flag) | old **WARN** / new **FAIL** |
| 9733 | old WARN / new WARN (stale flag) | old **WARN** / new **FAIL** |

Before the fix a drifted name on any of those three passed a green build as a warning. Now it
is a FAIL, which is the whole point of the layer.

B. The three codes whose names the old parser corrupted, authored correctly — the
`morphology_name` copied character-for-character from Layer 1:

| code | old parser | new parser |
|---|---|---|
| 9814 | **FAIL** | OK |
| 9690 | **FAIL** | OK |
| 9732 | **FAIL** | OK |

This is the more dangerous half. The old parser failed the *correct* name, because the option
it had parsed was the run-together string with the next option glued onto it. The only way to
make that build pass was to copy the corrupted string into `morphology_name` — putting into
the tool a name that does not exist anywhere in REDCap and that the clerk could never match.
A false FAIL does not merely annoy; here it would have actively produced the defect.

---

## Coordinator follow-ups (second pass)

Three items raised after the first pass: a seventh check, one tightening to the viral-gate
synonym set, and a boundary case to confirm.

### `check_burkitt_provisional` (Pathway §4.2; contract §3.2, §6) — new

**What it catches.** 9687 reachable by any route on which no FISH or molecular result was
established, unless the emitting branch carries a `provisional_pending`. Without the test,
high-grade/large B-cell lymphoma with 11q aberration and B-ALL with MYC rearrangement — both
phenotypically indistinguishable from Burkitt — are absorbed into 9687 silently. Where
Burkitt is the commonest childhood cancer this is the highest-*volume* version of the
evidence-overstatement defect in the group. Generalised over `UNDERDETERMINED_CODES`, so the
same policy covers 9680/LBCL-IRF4 on a context-gated arm.

Evidence is read from the route, not just the branch: a `captures`/`when` on a FISH variable
whose value actually came back, a `satisfies_tests` naming `Cytogenetics/FISH` or
`Molecular/PCR`, an evidence-tier capture listing one of those, or a FISH-bearing
`detection_method`. MYC IHC is deliberately not evidence (Pathway §4.2/§5.1 keep an explicit
30-50% indeterminate band because the stain does not settle what the FISH settles).

#### Control 1 — the `provisional_pending` stripped from the FISH-not-done 9687 terminal

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  under-determined terminal 9687 (Burkitt lymphoma) is emitted at g2_burkitt_fish (resolution_logic[3]) on a route where no FISH or molecular result was established, and the branch carries no provisional_pending. Without the test, 9687 absorbs high-grade/large B-cell lymphoma with 11q aberration, and B-ALL with MYC rearrangement — both phenotypically indistinguishable from Burkitt, and the case is recorded as a settled diagnosis with nothing on screen saying what was never excluded — the highest-volume version of that defect in this group (Pathway §4.2; contract §3.2, §6). Either establish the result on the route, or add a provisional_pending whose reason is 'MYC status unknown; HG/LBCL-11q and HGBL-DH not excluded' and whose resolving_test is 'Cytogenetics/FISH'.
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — the same branch with its provisional stripped, but a `fish_panel_performed` capture added upstream on the route

Expected **PASS**, got **PASS** — as designed.

No FAIL — the route establishes the result, so the named provisional is not
required. This is the both-ways half the coordinator asked for: the check has to stay
silent when the evidence is actually there, or authors learn to add a provisional
everywhere to keep the build green, which is how a real flag becomes noise.

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 3 — the provisional replaced by a MYC IHC result (`myc_ihc_pct: "95"`) — a stain, not a FISH

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  under-determined terminal 9687 (Burkitt lymphoma) is emitted at g2_burkitt_fish (resolution_logic[3]) on a route where no FISH or molecular result was established, and the branch carries no provisional_pending. Without the test, 9687 absorbs high-grade/large B-cell lymphoma with 11q aberration, and B-ALL with MYC rearrangement — both phenotypically indistinguishable from Burkitt, and the case is recorded as a settled diagnosis with nothing on screen saying what was never excluded — the highest-volume version of that defect in this group (Pathway §4.2; contract §3.2, §6). Either establish the result on the route, or add a provisional_pending whose reason is 'MYC status unknown; HG/LBCL-11q and HGBL-DH not excluded' and whose resolving_test is 'Cytogenetics/FISH'.
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 4 — the provisional stripped and `fish_status` set to `"failed"` — attempted, but nothing came back

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  under-determined terminal 9687 (Burkitt lymphoma) is emitted at g2_burkitt_fish (resolution_logic[3]) on a route where no FISH or molecular result was established, and the branch carries no provisional_pending. Without the test, 9687 absorbs high-grade/large B-cell lymphoma with 11q aberration, and B-ALL with MYC rearrangement — both phenotypically indistinguishable from Burkitt, and the case is recorded as a settled diagnosis with nothing on screen saying what was never excluded — the highest-volume version of that defect in this group (Pathway §4.2; contract §3.2, §6). Either establish the result on the route, or add a provisional_pending whose reason is 'MYC status unknown; HG/LBCL-11q and HGBL-DH not excluded' and whose resolving_test is 'Cytogenetics/FISH'.
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 5 — the FISH node's `nos_fallback` set to 9687 with a bland reason (contract §4.2: "the code that entered the node")

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_burkitt_fish: the nos_fallback emits 9687 (Burkitt lymphoma) on a route where no FISH or molecular result was established, and its 'reason' does not name what is unresolved. 9687 absorbs high-grade/large B-cell lymphoma with 11q aberration, and B-ALL with MYC rearrangement — both phenotypically indistinguishable from Burkitt when the test never returns, and Pathway §4.2 requires an explicit named flag rather than silent absorption. A nos_fallback has no provisional_pending slot, so its rendered 'reason' must carry the flag — say 'MYC status unknown; HG/LBCL-11q and HGBL-DH not excluded'.
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 6 — the same 9687 nos_fallback with the Pathway §4.2 flag written into its `reason`

Expected **PASS**, got **PASS** — as designed.

No FAIL — the route establishes the result, so the named provisional is not
required. This is the both-ways half the coordinator asked for: the check has to stay
silent when the evidence is actually there, or authors learn to add a provisional
everywhere to keep the build green, which is how a real flag becomes noise.

Restored: **BUILD PASSED**, 0 FAIL.

Two design decisions inside this check, both visible rather than silent:

* **The 9680 arm is context-gated** on localised paediatric head-and-neck disease, because
  Pathway §4.2 asks for the flag there and not on every 9680 — and 9680 is also the mature-B
  NOS fallback (contract §4.2), where an unconditional rule would fire on every unresolved
  large-cell case. Pathway §5.1 defines **no** head-and-neck site variable, so the arm is
  armed against anticipated names; when it finds no such context in a file it emits a NOTE
  saying it tested nothing, rather than passing quietly. A rule that can never fire is a hole.
* **A `nos_fallback` has no `provisional_pending` slot** in its `{code, name, reason}` shape,
  but contract §4.2 lets the FISH node fall back to "the code that entered the node" — which
  is exactly a FISH-less 9687. There the named flag has to live in the rendered `reason`, so
  the reason must at least name what is unresolved. Controls 5 and 6 above are that pair.
* A FISH-evidence value in neither the resolved nor the unresolved vocabulary is **accepted**
  (failing closed would fail correct files over an unfamiliar but honest label) and reported
  as a NOTE naming the value, so a typo that discharges the requirement is visible.
  `fish_panel_performed` is exempt from that NOTE — Pathway §5.1 gives it panel names, not
  result states, so any value but `none` is a panel that was run.

---

### `check_viral_gates` — `ebv_status` dropped from the `eber_status` synonym set

Every other synonym names the **test**; `ebv_status` names the **virus**, and it is what an
author reaches for when recording a serology result. Pathway §4.3 is explicit that serology
cannot upgrade any code: VCA IgG+/IgM−/EBNA-1 IgG+ is the near-universal state in a
high-EBV-burden population and supports nothing, EBNA-1 IgG is unreliable in HIV-positive
patients, and viral load has no agreed threshold, unit or specimen. EBER ISH on tissue is the
only entity-defining EBV test. `eber`, `eber_ish`, `eber_status` and `ebv_eber_status` all
name that test and remain accepted.

#### Control — the EBER gate re-keyed to `ebv_status` — the variable an author reaches for when recording serology

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  viral-gated terminal 9719 is emitted at g2_eber (resolution_logic[0]) on a route where EBER ISH was never established positive. 9719 is DEFINITIONALLY viral — the virus is part of the entity, not an association found beside it — so a case coded here without the result reads as a confirmed diagnosis that nothing in the file supports (contract §6; Pathway §5.5). Capture EBER ISH positive on every route that reaches it (a node or branch `captures`, a `when`, or a `positive[]` marker), or send the untested case to the NOS fallback instead.
```

Restored: **BUILD PASSED**, 0 FAIL. Before the tightening this same file passed.

---

### `check_test_result_states` — the boundary case the tightening could have hidden

The first pass narrowed "branches on" to *a `when` naming the variable, or two or more
branches recording distinct states of it*. The case that had to keep firing: a node offering
`positive` / `negative` / `not_done` for `eber_status` and simply omitting `not_assessable`.
Three of twenty-one cases in the Kenyan NLPHL series were uninterpretable on a failed RNA
control, so this is not a hypothetical omission. Both shapes were tested with the branching
done through `captures` rather than `when` — the shape the tightening actually touched.

#### Control 1 — positive / negative / not_done recorded via `captures` (not `when`), `not_assessable` omitted from the declared states

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_eber: test_result_states for 'eber_status' omits 'not_assessable'. This test fails in a way that is neither positive nor negative, and with no state for it the clerk has to file an unreadable result as one of the two real answers (contract §3.4)
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — the same three states via `captures` with no `test_result_states` block at all

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_eber branches on 'eber_status' but declares no test_result_states for it. Every branch on this test has to offer 'not_assessable', and the node has to say so where the engine can see it (contract §3.4)
```

Restored: **BUILD PASSED**, 0 FAIL.

Three distinct states recorded is two or more, so `branches_on()` is true either way: the
declared-but-incomplete shape is caught by the `not_assessable`-required rule, and the
no-block-at-all shape by the missing-declaration rule. The tightening did not hide it, and no
loosening was needed.

---
### `check_burkitt_provisional` — the context-gated 9680 arm, proved separately

The 9680 arm is the generalisation, and an arm that is never exercised is exactly the hole
`data.md` §5A describes — so it was tested in all three of its states rather than left to the
first Group II file to discover.

#### Control 1 — 9680 emitted with no FISH and no provisional, on a route with NO head-and-neck context — the context-gated arm must not apply

Expected **PASS**, got **PASS** — as designed.

```
NOTE  the 9680 arm is context-gated on localised paediatric head-and-neck disease and no route in this file establishes that context, so it tested nothing. Pathway §5.1 defines no head-and-neck site variable; if the tree records one under a name outside anatomic_region, disease_region, head_and_neck_site, primary_compartment, primary_site_region, site_region, add it to HEAD_AND_NECK_CONTEXT_VARIABLES or this rule stays inert.
```

The arm reported that it tested nothing rather than passing quietly — the point of
gating it at all. A silent inert rule and a satisfied rule look identical in a green
build, and that is how a check stops being a check.

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — the same 9680 terminal on a route that establishes `primary_site_region: head_and_neck`

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  under-determined terminal 9680 (Diffuse large B-cell lymphoma, NOS) is emitted at g2_lineage (options[2]) on a route where no FISH or molecular result was established, and the branch carries no provisional_pending. Without the test, 9680 absorbs large B-cell lymphoma with IRF4 rearrangement, a curable paediatric head-and-neck disease that is over-treated when it is absorbed here, and the case is recorded as a settled diagnosis with nothing on screen saying what was never excluded — the highest-volume version of that defect in this group (Pathway §4.2; contract §3.2, §6). Either establish the result on the route, or add a provisional_pending whose reason is 'possible LBCL-IRF4' and whose resolving_test is 'Cytogenetics/FISH'.
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 3 — the same in-context 9680 terminal carrying the named provisional

Expected **PASS**, got **PASS** — as designed.

No FAIL — the named provisional discharges the requirement, exactly as on the 9687 arm.

Restored: **BUILD PASSED**, 0 FAIL.

---
## Third pass — against the merged Group II file

Group II's four trees merged and the build reported **60 FAIL**. Most were checks being
wrong, not data. These controls run against **copies of the real `group_01_dt.json` and
`group_02_dt.json`** (`scratchpad/fixture2/`) rather than the synthetic fixture, because the
defects at issue only appear at real scale — a dozen rules per node with disjoint marker
sets is what broke the old ordering heuristic, and a two-rule fixture could never have shown
it.

| Check | Before | After | Why |
|---|---|---|---|
| `check_mpal_rule_ordering` | 48 FAIL | 0 | positional heuristic replaced by subsumption |
| `check_marker_intensity_tokens` | 3 FAIL | 0 | stopped splitting fusion names on every colon |
| `check_test_result_states` | 5 FAIL | 0 | same destination allowed when distinguishable |
| `check_prior_probability` | 1 FAIL | 0 | narrowed to "decides the code BY that test" |
| `check_satisfies_tests` | 3 FAIL | 0 | real data defects, fixed by the tree authors |

### 1. `check_mpal_rule_ordering` — positional heuristic replaced by subsumption

**What it now catches.** Rule R is dead when an earlier rule E asks for strictly less:
`E.positive ⊆ R.positive` **and** `E.negative ⊆ R.negative` **and** `E.when ⊆ R.when`. Every
case matching R has then already matched E, and first-match-wins stops there.

The old version compared only "has a `when`" against "has none", positionally. That is this
rule's special case — on Group 1 the rules it governed shared one marker set, so E.when = {}
⊆ R.when and the marker sets were equal. On Group II, where nodes carry a dozen rules
distinguished only by their panels, it produced **48 FAILs on perfectly reachable rules**.

#### Control 1 — Group 1's unconditioned 9808/9809 block moved ahead of the `when`-gated 9806/9807 rules — the exact case the check was originally written for

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node ac_lineage_assignment: resolution_logic[7] can never fire — rule [3] above it asks for strictly less (positive ['cCD3', 'cMPO:strong'], negative -, when - vs this rule's positive ['cCD3', 'cMPO:strong'], negative -, when ['kmt2a_status']), so every case that matches [7] has already matched [3] and first-match-wins stops there (Pathway §7.5)
FAIL  node ac_lineage_assignment: resolution_logic[8] can never fire — rule [4] above it asks for strictly less (positive ['cMPO:strong', 'sCD3'], negative -, when - vs this rule's positive ['cMPO:strong', 'sCD3'], negative -, when ['kmt2a_status']), so every case that matches [8] has already matched [4] and first-match-wins stops there (Pathway §7.5)
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — Group II: a broad `Marginal-zone or monocytoid pattern` rule inserted above the splenic 9689 rule

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_matureB: resolution_logic[20] can never fire — rule [19] above it asks for strictly less (positive ['Marginal-zone or monocytoid pattern'], negative -, when - vs this rule's positive ['Marginal-zone or monocytoid pattern', 'Splenic primary'], negative -, when -), so every case that matches [20] has already matched [19] and first-match-wins stops there (Pathway §7.5)
FAIL  node g2_matureB: resolution_logic[21] can never fire — rule [19] above it asks for strictly less (positive ['Marginal-zone or monocytoid pattern'], negative -, when - vs this rule's positive ['MNDA or IRTA1 positive', 'Marginal-zone or monocytoid pattern'], negative -, when -), so every case that matches [21] has already matched [19] and first-match-wins stops there (Pathway §7.5)
FAIL  node g2_matureB: resolution_logic[22] can never fire — rule [19] above it asks for strictly less (positive ['Marginal-zone or monocytoid pattern'], negative -, when - vs this rule's positive ['Marginal-zone or monocytoid pattern'], negative -, when -), so every case that matches [22] has already matched [19] and first-match-wins stops there (Pathway §7.5)
```

Restored: **BUILD PASSED**, 0 FAIL.

Control 1 is the one that mattered: **the case the check was originally written for**. The
genetics-first ordering puts 9806/9807 ahead of the ungenotyped 9808/9809 on the identical
marker set; reversed, the genotyped codes can never fire, and the subsumption test names
exactly those rules. A replacement that could not catch its predecessor's case would not be
a replacement.

The false-FAIL control is the unmodified build: **0 dead rules across 143 Group 1 rules and
349 Group II rules**, where the old check reported 48.

Deliberate limit, stated in the docstring: tokens compare as written, so `CD19` and
`CD19:strong` are different requirements. That is the safe direction — an intensity-qualified
token is genuinely narrower than the bare marker, so treating them as equal would report
reachable rules as dead.

---

### 2. `check_marker_intensity_tokens` relaxed, `check_marker_tokens_declared` added

A token is a marker NAME unless it ends in exactly `:strong` or `:weak`. Splitting on the
first colon read `NPM1::ALK t(2;5) by FISH or RT-PCR` as marker `NPM1` with intensity
`:ALK…` — a permanent tax on correct authoring, since `::` is the fusion separator this
project uses throughout.

Relaxing alone would leave a hole: `CD30:stong` becomes a marker *name*, matches nothing, and
the rule silently never fires. So every token, after a valid suffix is stripped, must name a
marker the node itself declares in `marker_groups[].markers`. Verified before writing it:
**0 of 278 Group 1 tokens undeclared, and exactly one in Group II** — `g2_tfh`'s "Only 1 TFH
marker positive", the rule that stops a single TFH marker being read as the ≥2 that re-routes
a case out of 9702 into 9705.

#### Control 1 — `Only 1 TFH marker positive` put back into a g2_tfh `positive[]` with no such marker declared

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_tfh (resolution_logic[7]): positive[] token 'Only 1 TFH marker positive' names 'Only 1 TFH marker positive', which this node does not declare in marker_groups[].markers. app.js matches tokens against what the clerk ticked, so a marker the node never offers can never match — the rule is dead, and nothing on screen or in the build says so. Either declare the marker or fix the token.
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — a `:stong` typo on a real marker token — the shape the relaxed suffix rule would otherwise read as a marker name

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2cut_cd30_lpd (resolution_logic[1]): positive[] token 'NPM1::ALK t(2;5) by FISH or RT-PCR:stong' names 'NPM1::ALK t(2;5) by FISH or RT-PCR:stong', which this node does not declare in marker_groups[].markers. app.js matches tokens against what the clerk ticked, so a marker the node never offers can never match — the rule is dead, and nothing on screen or in the build says so. Either declare the marker or fix the token.
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 3 — `marker_groups[]` removed from a node that carries marker tokens

Expected **WARN**, got **WARN** — as designed.

```
WARN  node g2cut_cd30_lpd carries 1 marker token(s) but declares no marker_groups[].markers — there is nothing to check them against, so a typo in any of them is a rule that silently never fires
```

Restored: **BUILD PASSED**, 0 FAIL.

Control 2 is the pair that justifies the whole trade: the fusion name now passes the
intensity check, and the `:stong` typo — which the relaxed rule can no longer see — is caught
loudly by the declared-marker check instead. A node with tokens and no `marker_groups[]` is a
WARN, not a FAIL: every token there is unverifiable, which is the same hole, but neither
built file contains one and `--strict` promotes it.

---

### 3. `check_test_result_states` — distinguishable, not merely different

The `not_assessable` branch must differ from the `negative` branch **either in destination,
or by carrying a `provisional_pending` the negative branch does not**.

Demanding a different destination was too narrow. 9719 requires EBER *positivity*, so neither
a negative nor an uninterpretable result unlocks it and both correctly land on 9702; forcing
them apart would be false precision. What may not happen is that they read the same, because
a clean negative means the workup is done and a failed control means a repeat is owed.

Two refinements the real data forced:

* **Compared by content, not presence.** `g2_matureB` carries a provisional on *both* halves —
  MYC on each, plus "EBER control failed, so EBV status is unestablished" on the
  `not_assessable` half. That is exactly the distinction being asked for, and a presence test
  would have failed the best authoring in the file.
* **Deduplicated.** A rule recording the same variable in both a `when` and a `captures` was
  being paired against itself and reported twice — 4 messages for 2 findings at `g2_nkt`.

#### Control 1 — the `provisional_pending` stripped from g2_nkt's not_assessable branch, leaving it identical to the negative branch

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_nkt: the not_assessable branch for 'eber_status' (resolution_logic[7]) is indistinguishable from the negative branch (resolution_logic[6]) — both land on code 9702/None, and the not_assessable branch carries no provisional_pending that says anything the negative branch does not. The same destination can be right (a code that needs POSITIVITY is unlocked by neither answer), but the two must not read the same: a clean negative means the workup is done, a failed control means a repeat on a fresh section is owed. Reported identically, the failed control is recorded as though the test had returned — the case looks better evidenced than it is. Either send not_assessable somewhere else, or give it a provisional_pending naming the repeat (contract §3.4, §6; Pathway §2.4, §4.3, §7.3 item 4)
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — the negative branch given a provisional_pending IDENTICAL to the not_assessable branch's

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_nkt: the not_assessable branch for 'eber_status' (resolution_logic[7]) is indistinguishable from the negative branch (resolution_logic[6]) — both land on code 9702/None, and the not_assessable branch carries no provisional_pending that says anything the negative branch does not. The same destination can be right (a code that needs POSITIVITY is unlocked by neither answer), but the two must not read the same: a clean negative means the workup is done, a failed control means a repeat on a fresh section is owed. Reported identically, the failed control is recorded as though the test had returned — the case looks better evidenced than it is. Either send not_assessable somewhere else, or give it a provisional_pending naming the repeat (contract §3.4, §6; Pathway §2.4, §4.3, §7.3 item 4)
```

Restored: **BUILD PASSED**, 0 FAIL.

---

### 4. `ISH` added to `DIAGNOSTIC_TESTS`

EBER in-situ hybridisation is not IHC. Pathway §4.3 makes EBER ISH on tissue the only
entity-defining EBV test, says LMP1 IHC cannot substitute (LMP1 is absent in latency I and 0),
and rules that serology cannot upgrade any code. Without its own member an EBER-resolving
`provisional_pending` could not name its own test, and EBER could never appear as an
outstanding-workup row anywhere in Group II. **DT master §2 is where this list is documented;
that file is owned elsewhere and was not edited.**

#### Control 1 — an EBER provisional naming its test as `In-situ hybridisation` rather than the vocabulary member `ISH`

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_nkt (resolution_logic[7]): provisional_pending.resolving_test 'In-situ hybridisation' is not in the closed diagnostic-test vocabulary (Cytogenetics/FISH, Flow cytometry, Histology, IHC, IHC or flow cytometry, ISH, Imaging, Molecular/PCR, Referral only). A value nothing can match names no real outstanding test, so the provisional reads as specific and resolves to nothing
```

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — the same provisional naming `ISH`, the member added tonight

Expected **PASS**, got **PASS** — as designed.

No FAIL — the vocabulary is still closed, and `ISH` is now a member of it.

Restored: **BUILD PASSED**, 0 FAIL.

---

### 5. `check_prior_probability` narrowed — a false FAIL of my own

Not on the coordinator's list; found while reading the last remaining FAIL, and fixed because
leaving a known false FAIL in place is the thing §5A warns about.

The rule was "a prior may not sit on any code-emitting branch". **Contract §3.3's own
canonical example violates it**: mixed-cellularity classic Hodgkin lymphoma, EBER expected in
70-80%. `g2_chl_subtype` options[4] emits 9652 on *architecture* and carries the EBER prior to
say that the expected positive result must not be allowed to refine the subtype — the best
anti-overstatement authoring in the file, and my check failed it.

It now fires only when the branch both emits a code **and decides that code on the prior's own
test**, read off the branch's own `when` / `captures` / `positive[]` / `negative[]`.

#### Control 1 — the EBER prior placed on the branch that emits 9652 on ARCHITECTURE — contract §3.3's own canonical placement

Expected **PASS**, got **PASS** — as designed.

No FAIL — the code is reached by architecture, not by EBER, so the prior justifies
nothing. This is the shape the old rule wrongly failed.

Restored: **BUILD PASSED**, 0 FAIL.

#### Control 2 — the same placement plus `when: {eber_status: positive}` — the code is now decided BY the test the prior is about

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node g2_chl_subtype (options[4]): prior_probability about 'EBER ISH' sits on a branch that emits 9652 AND decides that code on 'EBER ISH' itself. Rendered beside a code the branch reached BY that test, the prior reads as the evidence for the code — when its entire purpose is the opposite: to say the result was expected and is weakly informative. A prior belongs where the test is being interpreted, not where its expected answer picks the code (contract §3.3, §6)
```

Restored: **BUILD PASSED**, 0 FAIL.

**The cost of that false FAIL is already visible in the data.** All five Group II priors now
sit on `marker_groups` or at node level; the one that was on the code-emitting option was
moved because my check told the author to move it. It can go back — that placement is legal
again, and it is where the clerk actually needs to read it. This is exactly the dynamic §5A
describes: a false FAIL does not merely annoy, it teaches a fix that was never needed.

---
## Summary

| Check | Controls | All behaved as designed | Clean pass restored | Fires on correct data |
|---|---|---|---|---|
| `check_behaviour_resolution` | 4 | yes | yes | no |
| `check_provisional_pending` | 5 | yes | yes | no |
| `check_prior_probability` | 4 | yes | yes | no |
| `check_test_result_states` | 8 | yes | yes | no |
| `check_entity_boundary` | 3 | yes | yes | no |
| `check_viral_gates` | 3 | yes | yes | no |
| `check_burkitt_provisional` | 9 | yes | yes | no |
| `check_mpal_rule_ordering` | 2 | yes | yes | no |
| `check_marker_tokens_declared` | 3 | yes | yes | no |

41 controls in total — 18 in the first pass, 12 in the second, 11 in the third. All 41 behaved as
designed (33 expected to FAIL and did, 8 expected to PASS and did), all 41 restored to a clean
build, and no check fires on correct data. The parser fix is proved separately above.

The third pass is the one worth remembering: **five of the six defects it found were in the checks,
not the data**, and four of those were false FAILs — 48, 3, 5 and 1 of them. A check that has only
ever seen a two-rule fixture is not known to work on a thirty-seven-rule node. Every check here is
now exercised against the real merged files as well as against the synthetic fixture.

Every check is keyed off Layer 1, off the pathway, or off the file's own structure. None reads a
flag in the file being checked — no `redcap_option_verified`, no `terminal_reachable`, no
`verified: true`. The one data-driven exemption anywhere near this work is the pre-existing
behaviour-split exemption in `check_redcap_exact_names`, anchored to a sibling entry that must
itself match Layer 1 exactly, so it collapses the moment the anchor drifts.
