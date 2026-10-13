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


---
---

# Group III checks — negative controls

Evidence that the twelve checks added to `build/build_database.py` for Group III catch what
they claim to, and that they fire on nothing else. Same method as the Group II section
above, per `memory/data.md` §5A: break the data deliberately, confirm the check FAILs,
restore, confirm it passes — and separately confirm it does **not** fire on correct data,
because a false FAIL is the more corrosive failure.

**92 controls. All 92 behaved as designed** — 73 expected to FAIL and did, 19 expected to
PASS and did — and all 92 restored to a clean build.

## The fixture

`scratchpad/fixture/` — a synthetic Group III repo. `data/database/group_03_dt.json` was
**not** on disk when this work was done and still is not: it is being authored in parallel
by other tasks, so there was no real data to validate against and every control here runs
against a fixture instead. That is contract §6 rule 14's requirement anyway.

The fixture is **generated, not transcribed** (`scratchpad/make_fixture.py`). Every code,
every term string and every subgroup in it is pulled from `icdo32.sqlite` and
`ICCC-2017.sqlite` at generation time, so the fixture cannot drift from Layer 1 and a
control that breaks a name is breaking a string the database actually carries. It holds:

- **50 morphology entries** — all eighteen behaviour-overloaded codes of contract §1.2 at
  every behaviour ICD-O-3.2 carries within the group's `0-1,3` declaration, plus `9380`
  (the intra-group topography split), `9475` (the one `source_term` exemption), `9476` (the
  one `awaiting_layer1`), `9471/3` carrying the §5.4 string `Medulloblastoma, SHH activated,
  NOS` verbatim, and the codes the trees emit.
- **Six trees, 14 nodes**, node-prefixed `pf_ st_ md_ sp_ mn_ un_`, with the contract §3
  topography map declared on both `metadata.decision_trees[]` and the tree objects.
- **At least one live instance of every one of the seven §2 fields**: two-track
  `diagnosis_rendering` on four branches, three `resource_level_gate`s (ependymal,
  embryonal, meningothelial-by-analogy), three `entity_annotation`s, one
  `grade_resolution`, `basis_of_diagnosis` on fourteen branches, two `imaging_pathway`
  endpoints with `diversion_criteria[]` (the DIPG six and the NF1 two), and a
  `numeric_gate` whose bands are stated in **two different units**.

Runs are:

```
python3 build/build_database.py --repo <scratchpad>/fixture \
        --layer1 "/Users/jay/Ai Environment/Cancer Registry/ICD coding"
```

## The false-FAIL control (correct data)

On the unmodified fixture the group_03 section reports **0 FAIL**, and each of the twelve
checks reports OK against real content rather than an empty NOTE:

```
OK  4 diagnosis_rendering block(s): every track carries its own numeral system (rule 1) and every "nec" suffix rests on an asserted adequate result (rule 2)
OK  3 resource_level_gate(s): every one names its family, no ependymal node carries tier "obligatory" (rule 3), and every family without an ADAPTR paper declares rl_assignment "by_analogy"
OK  1 numeric_gate node(s): every band names a unit from the closed set, and 2 unit-partition(s) cover their domain with no gap and no overlap (rule 4)
OK  3 entity_annotation(s): no "(provisional type)" artefact, no whitespace drift, no Table 2 spelling, all matched against data/shared/who_cns5_table1.json
OK  all 18 behaviour-overloaded codes of contract §1.2 are authored one entry per behaviour, each with an explicit behavior_code, against the behaviour set ICD-O-3.2 carries (rule 6)
OK  none of the 16 codes that ICCC-3 names but ICD-O-3.2 does not carry (9402-9409, 9422, 8274-8279, 9536) appears as a code, a fallback, an alias target or in clerk-facing text (rule 7)
OK  1 grade_resolution block(s): no `unresolved` invents a grade, and every outcome names a grade with its system or a null with a reason (rule 9)
OK  14 basis_of_diagnosis value(s) in the ENCR set [0, 1, 2, 4, 5, 7, 8, 9]; none is 3, 6 or (in Group III) 1 (rule 10)
OK  2 imaging_pathway node(s): every imaging-only terminal carries no_tissue, endpoint_verification "not_verified", basis 2 and a NON-EMPTY diversion_criteria[] (rule 11)
OK  topography map is total and disjoint: all 25 recordable code(s) in the Group III sweep resolve to exactly one of 6 tree(s) (rule 12)
OK  50/50 (code, name, behaviour) triple(s) exist verbatim in icdo32.sqlite; 1 declared name exemption(s), each still anchored to a string the database actually carries (rules 8 and 13)
OK  1 iccc3_subgroup_by_topography[] rule list(s): every rule names a subgroup ICCC-2017 assigns to that code at that topography, and so does every entry's own default (contract §1.3)
```

## Regression — Groups 1 and 2 are byte-identical

Ran the pre-change `build_database.py` and the post-change one over the real repo (which
holds `group_01_dt.json` and `group_02_dt.json` and no Group 3 file) and diffed the whole
report. **One line differs, and it is the check count:**

```
153c153
<   checks run : 87
---
>   checks run : 111
```

`OK 82 · NOTE 17 · WARN 21 · FAIL 0 · BUILD PASSED` before and after. Not one new finding
on either group. Every Group III check returns **nothing at all** — not an OK, not a NOTE —
on a file that does not use the field it is about, which is what makes that diff possible.

## Four defects the fixture exposed, all in the checks rather than the data

Recorded because §5A's point is that this is where the defects are.

1. **`check_non_reportable_terminals` false-FAILed on every `diversion_criteria[]` entry
   and every `grade_resolution` outcome** — nine FAILs on correct data. Both constructs
   require a clerk-facing `reason` and neither has a destination, and that check reads "a
   `reason` and no destination" as a terminal that forgot to flag itself. This is the third
   time that shape has bitten: `nos_fallback` and `provisional_pending` were the first two.
   Fixed the same way, with `is_diversion_criterion_object()` and
   `is_grade_resolution_leaf()` scoped to the key they hang off **and** their shape —
   controls X.2 and X.3 prove the narrowing did not absorb a real code-less terminal.

2. **My own domain sweep false-FAILed on `"<2.5"`.** A band that reaches below the floor of
   its domain was read as overlapping a region the domain does not contain. Clamped. This
   is the corrosive kind: the only way for an author to clear it would have been to write
   `"0-2.49"` in place of the threshold the source actually states.

3. **Every Group III check discarded its own FAIL when its "seen" counter was zero.** The
   early return was `if not seen: return []`, so a finding produced *before* the counter
   incremented was thrown away — including the two rules that fire precisely when the
   construct is ABSENT (a `9380` with two ICCC-2017 subgroups and no routing rules; an
   `ihc_counts_as` on a file with no `basis_of_diagnosis`). Control §1.3.2 caught it: it
   expected FAIL and got PASS. Now `if not seen and not out`. This is exactly the failure
   §5A names — a check that confirms the error it exists to catch.

4. **Rule 12's sweep, read literally, demanded a tree for nine topography codes that do not
   exist.** C70.2–C70.8, C72.6 and C72.7 are inside the contract's ranges and are in no
   topography list; demanding an assignment for them is a false FAIL whose only fix is to
   invent one. Existence is now read off Layer 1's topography option list, and **every code
   the sweep drops is reported** so the reduction is visible rather than silent.

---

## `check_diagnosis_rendering` — rules 1 and 2 (contract §2(1))

**What it catches.** The numeral invariant in both directions, the per-track field shape
(`who_cns5` fills `who_diagnosis` and nothing else; `adaptr_descriptive` fills
`descriptive_diagnosis` and `comment`), a grade that is a placeholder rather than a grade,
a grade outside its own system's set — and the NEC gate: a `suffix: "nec"` on a branch that
does not assert an adequate result was obtained.

### Control 1.1 — Arabic grade_system on an ADAPTR descriptive track

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node st_ependymoma_gate (resolution_logic[0]): RULE 1 — track 'adaptr_descriptive' requires grade_system 'roman', got 'arabic'. The numeral system follows the TRACK, never the evidence type (contract §2(4)): a grade reached on histology alone is still Arabic when the diagnosis is a WHO CNS5 diagnosis. Printed the other way round, the line claims a diagnosis the registry did not reach
```

### Control 2.1 — the NEC branch re-gated on `specimen_adequacy: "inadequate"`

The branch still says NEC. It is now reached *because the specimen was inadequate*.

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node pf_medulloblastoma_molecular (resolution_logic[1]): RULE 2 — suffix "nec" on a branch reached on 'inadequate'. NEC says the test WAS done and the tumour fitted no WHO type (cIMPACT-NOW update 1). A branch reached because the test did not return cannot say that — it is a NOS, and a registry that cannot do the test can never legitimately emit NEC (contract §2(1), §6 rule 2)
```

### Control 2.4 — the same branch relabelled `suffix: "nos"`, still on a not-done test

Expected **PASS**, got **PASS** — as designed. NOS is exactly what an unresolved test
produces; only NEC is a positive claim about a result.

---

## `check_resource_level_gate` — rule 3 (contract §2(2))

**What it catches.** A missing or invented `family` (RL is per family, never per site), an
`obligatory` tier on an ependymal node, and a family with no ADAPTR paper behind it that
does not declare `rl_assignment: "by_analogy"`.

### Control 3.1 — `tier: "obligatory"` on the ependymal node

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node st_ependymoma_gate (resolution_logic[0]): RULE 3 — tier 'obligatory' on a node in the ependymal family. Satgunaseelan uses only can_be_considered and highly_recommended for this family, so a third value has no source behind it and a three-value enum mis-renders every ependymal node (contract §2(2), §6 rule 3)
```

### Control 3.3 — the same `obligatory` tier on the EMBRYONAL node

Expected **PASS**, got **PASS** — as designed. The restriction is per family; a
three-value enum is legal everywhere Satgunaseelan's ependymoma tables are not the source.

---

## `check_numeric_gate_units` — rule 4 (contract §2(7))

**What it catches.** A band with no `unit`, a unit outside the closed set, a per-HPF band
with no `hpf_area_mm2`, and — the reason the rule exists — a gap or an overlap in the band
domain, swept **per unit** so that a `per_mm2` band is never compared with a `per_10_hpf`
one.

### Control 4.3 — one band re-labelled `per_mm2`, opening a gap in the `per_10_hpf` partition

The node's bands are `0-3`, `4-19`, `>=20` per 10 HPF and `<2.5`, `>=2.5` per mm². Moving
`4-19` into the per-mm² partition leaves 4 to 19 uncovered in the first and overlapping in
the second.

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  numeric_gate mn_mitotic_gate [per_10_hpf]: no band covers 4 to 20 — the next band is bands[2] ('>=20'). DT master §4: bands cover their domain with no gap at the authored precision. An uncovered value falls silently to NOS and reads as a clinical decision rather than a hole in the file
```

### Control 4.7 — the two units left as authored

Expected **PASS**, got **PASS** — as designed. Swept together rather than per unit, these
five bands manufacture both a gap and an overlap that are not there.

---

## `check_entity_annotation` — rule 5 (contract §2(3))

**Its anchor.** `data/shared/who_cns5_table1.json` — Louis 2021 Table 1, 109 type rows
transcribed with a `provisional` flag per row. Rule 5 says the entity strings are checked
against a transcribed list "not against recall", and that file is the list. Where it is
absent the check says so in a WARN and proves only the artefact, whitespace and divergence
rules; it does not imply it checked Table 1.

No spelling rule is imposed on an entity name. Table 1 uses `tumor`, and the check knows
that because the transcription says so, not because anyone remembered it.

### Control 5.1 — `ZFTA fusion positive`, the hyphen written as a space

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node st_ependymoma_gate (resolution_logic[0]): entity_annotation.who_cns5_entity 'Supratentorial ependymoma, ZFTA fusion positive' is a near-miss on the transcribed CNS5 Table 1 string 'Supratentorial ependymoma, ZFTA fusion-positive' — they differ only in case, punctuation or spacing, which is exactly the drift rule 5 exists to catch
```

Controls 5.2 (trailing space), 5.3 (`tumour` for `tumor`), 5.4 (`(provisional type)` inside
the name), 5.5 (the artefact inside `shared_with[]`), 5.6 (CNS5 Table 2's comma-before-and
spelling of the Table 1 entity) and 5.7 (`provisional: false` on an entity Table 1 marks
provisional) all behaved as designed.

---

## `check_group3_behaviour_split` — rule 6 (contract §1.2)

**What it catches.** Any of the eighteen overloaded codes missing, missing a behaviour,
carrying a behaviour ICD-O-3.2 does not have for it, or carrying an entry with no explicit
`behavior_code`. The expected behaviour set is **computed** — ICD-O-3.2's behaviours for
the code intersected with the group's `0-1,3` declaration — so it cannot be got wrong from
memory, and `8000`'s `/6` and `/9` fall outside the group without a special case.

### Control 6.1 — the `8000/0` entry deleted

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  RULE 6 — code 8000 is authored at /1, /3; ICD-O-3.2 carries it at /0, /1, /3 within the group's "0-1,3" declaration.  Missing: /0. (contract §1.2, §6 rule 6)
```

### Control 6.3 — an `8000/6` entry added

Expected **FAIL**, got **FAIL** — as designed. `/6` exists in ICD-O-3.2 and is outside the
group; metastatic disease is handled at Stage 1.

---

## `check_group3_absent_codes` — rule 7 (contract §1.1)

**What it catches.** `9402`–`9409`, `9422`, `8274`–`8279` and `9536` as a code, a fallback
code, an alias target, or in clerk-facing text. `alias` and `also_known_as` are deliberately
not scanned — §1.1 keeps those codes as alias *inputs*, which is what a clerk types.

### Control 7.2 — `9422` printed in a clerk-facing `reason`

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  RULE 7 — group_03_dt.json.decision_trees[4].nodes[1].nos_fallback.reason prints 9422, a code that does not exist in ICD-O-3.2, in text a clerk reads. A code on screen is a code that gets entered (contract §1.1, §6 rule 7)
```

### Control 7.3 — the same `9422` in an author-facing `coding_note`

Expected **PASS** (a WARN, not a FAIL), got **PASS** — as designed. `coding_note` is never
displayed, so no clerk can copy the digits out of it; the WARN still asks for the range to
be named rather than the code.

### Control 7.5 — `9536` left in `also_known_as`

Expected **PASS**, got **PASS** — as designed. That is the one place the code belongs.

---

## `check_grade_resolution` — rule 9 (contract §2(4))

### Control 9.1 — `unresolved` given a grade

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node mn_mitotic_gate (bands[0]): RULE 9 — grade_resolution.unresolved carries grade '1'. `unresolved` must NEVER invent a grade: where the grade cannot be established it is omitted, which is what cIMPACT-NOW update 8 requires for an untested brain-invasive meningioma. A number here is one no test produced (contract §2(4), §6 rule 9)
```

Controls 9.2 (a grade with no `grade_system`), 9.3 (a null grade with no `reason`), 9.4
(`"NA"`), 9.5 (`""`), 9.6 (`unresolved` removed) and 9.7 (a `variable` not declared in
`captured_variables[]`) all behaved as designed.

---

## `check_basis_of_diagnosis` — rule 10 (contract §2(5))

### Control 10.1 — basis code 6

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  node pf_medulloblastoma_molecular (resolution_logic[0]): RULE 10 — basis_of_diagnosis 6 does not exist. The ENCR scale is [0, 1, 2, 4, 5, 7, 8, 9]; 3 and 6 are not values in it, so a receiving registry reads this as something else entirely (contract §2(5), §6 rule 10)
```

Control 10.3 (basis 1 on a Group III terminal — every CNS row in ENCR Table 3 is basis 2),
10.5 (`ihc_counts_as: 8` where §2(5) closes the gap at 7) and 10.7 (a declared basis lower
than the components it says it derived from) behaved as designed. Control 10.6 (basis 5,
cytology) expected PASS and passed.

---

## `check_imaging_terminals` — rule 11 (contract §2(6), §3.5)

### Control 11.1 — `diversion_criteria[]` emptied on the DIPG terminal

The list is the only thing standing between a κ = 0.297 imaging endpoint and a case coded
without tissue. Empty, it renders exactly like a terminal that was never gated.

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  imaging_pathway pf_dipg_imaging ((node level)): RULE 11 — diversion_criteria[] is EMPTY. An empty list is a build error, not "no diversions apply": it renders exactly like a terminal that was never gated, while reading to the next author as considered and cleared. DIPG's imaging-only endpoint has κ = 0.297 agreement and is explicitly below standard of care — the six diversion criteria are what make it safe to offer at all (contract §2(6), §6 rule 11)
```

Controls 11.2 (the list removed), 11.3 (basis 7 on an imaging-only terminal), 11.4
(`no_tissue` dropped), 11.5 (`endpoint_verification: "verified"`) and 11.6 (a criterion
with a feature and no reason) behaved as designed. Control 11.7 — the NF1 terminal's two
criteria against DIPG's six — expected PASS and passed: the rule is non-empty, not a count.

---

## `check_group3_topography_map` — rule 12 (contract §3)

Revision 2 records that the first draft of the §3 table assigned C72.9 to two trees and
left C72.2, C72.4 and C72.5 unrouted. Both controls reproduce those faults exactly.

### Control 12.1 — C72.9 given to `g3_midline` as well as `g3_unspecified`

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  RULE 12 — topography C72.9 resolves to 2 trees (g3_midline, g3_unspecified). The map must be disjoint: a duplicate does not fail, it silently picks whichever row the engine reads first — which is not a decision anybody made (contract §3, §6 rule 12)
```

### Control 12.2 — C72.4 removed from `g3_midline`

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  RULE 12 — 1 topography code(s) in the Group III sweep resolve to NO tree: C72.4. A case at one of these reaches the router, finds no handoff and dead-ends (contract §3, §6 rule 12)
```

### Control 12.5 — C70.2–C70.8, C72.6 and C72.7 owned by nobody

Expected **PASS**, got **PASS** — as designed, and reported as a NOTE naming all nine. They
are inside rule 12's literal ranges, they are in no topography list, and no case can carry
them. See defect 4 above.

### Control 12.4 — every topography declaration removed

Expected **FAIL**, got **FAIL** — as designed. A missing map is not an empty map: the router
picks the Group III tree from topography and nothing else.

---

## `check_icdo32_round_trip` — rules 8 and 13 (contract §5.2, §5.3)

**What it catches.** Any `(morphology_code, morphology_name, behavior_code)` triple the
engine can emit that ICD-O-3.2 does not carry — including a `nos_fallback` naming a string
no entry on that code carries. Where a name fails, the message prints the near-miss, so the
author sees which string they meant.

**This replaces `check_redcap_exact_names` for Group 3 and for Group 3 only** (contract
§5.2). That check now returns a single NOTE for group 3 saying so, and is otherwise
untouched: Groups 1 and 2 keep the Layer 1 keying, the sibling behaviour-overload exemption
and every message they had.

### Control 13.2 — `Medulloblastoma, SHH activated, NOS` hyphenated to `SHH-activated`

The sibling Related term on the same code, `Medulloblastoma, SHH-activated and
TP53-wildtype`, *does* have the hyphen. This is the single most likely name defect in the
group.

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  entry 9471/3: the triple (9471, 'Medulloblastoma, SHH-activated, NOS', 3) does not exist in ICD-O-3.2. RULE 13 — every name the engine can emit must be a real term for that code at that behaviour, checked against the database and not against the REDCap option list, which carries 28 (code, term) pairs ICD-O-3.2 does not (contract §5.2, §6 rule 13).
```

### Control 13.3 — `tumor` spelled `tumour`

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  entry 9473/3: the triple (9473, 'CNS embryonal tumour, NOS', 3) does not exist in ICD-O-3.2. RULE 13 — every name the engine can emit must be a real term for that code at that behaviour, checked against the database and not against the REDCap option list, which carries 28 (code, term) pairs ICD-O-3.2 does not (contract §5.2, §6 rule 13).
```

### Control 13.4 — the same drifted name flagged `redcap_option_verified: true`

Rule 8: no flag exempts a name.

Expected **FAIL**, got **FAIL** — as designed, with the identical message. The flag is not
read.

```
FAIL  entry 9473/3: the triple (9473, 'CNS embryonal tumour, NOS', 3) does not exist in ICD-O-3.2. RULE 13 — every name the engine can emit must be a real term for that code at that behaviour, checked against the database and not against the REDCap option list, which carries 28 (code, term) pairs ICD-O-3.2 does not (contract §5.2, §6 rule 13).
```

### Control 13.1 — a trailing space on a `morphology_name`

Expected **FAIL**, got **FAIL** — as designed.

### The `9475` exemption, and proof that it collapses

`9475/3`'s ICD-O-3.2 preferred term is misspelt `Medullobloastoma`. The entry displays the
corrected spelling and carries the source string in `source_term`; the round-trip runs
against `source_term`. The exemption rests on three conditions, re-checked on every build.

#### Control 13.6 — `source_term` corrupted to the corrected spelling, so the anchor goes

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  entry 9475/3: source_term is 'Medulloblastoma, WNT-activated, NOS'; the exemption is declared against 'Medullobloastoma, WNT-activated, NOS' (contract §5.3). ICD-O-3.2 prints 'Medullobloastoma' (contract §5.3, Revision 2 §8.2 decision 3). The entry displays the corrected spelling.
```

#### Control 13.7 — `source_term` added to an entry that is not the declared exemption

Expected **FAIL**, got **FAIL** — as designed. A `source_term` any entry may add is a
general escape hatch from rule 13.

```
FAIL  entry 9440/3: carries a `source_term`, but 9440/3 is not the one declared name exemption (contract §5.3 exempts only 9475/3). A `source_term` that any entry may add is a general escape hatch from rule 13 — and a flag that exempts a name is exactly what rule 8 forbids
```

#### Control 13.9 — `9475` as authored

Expected **PASS**, got **PASS** — as designed.

The third condition has no control here because it cannot be staged without editing
`icdo32.sqlite`, which is read-only Layer 1: if ICD-O-3.2 ever carries the corrected
spelling for `9475/3`, the check FAILs with "THE EXEMPTION IS NO LONGER NEEDED". It is a
two-line branch in `check_icdo32_round_trip()` and it is the reason the exemption cannot
outlive its cause.

---

## `check_iccc3_subgroup_by_topography` — contract §1.3

**Its anchor.** `ICCC-2017.sqlite`. For every code in the file, at every topography code the
group can carry, the subgroup the ordered rules resolve to must be the subgroup ICCC-2017
assigns — which catches the missing rule as well as the wrong one.

### Control §1.3.2 — the `9380` rule list removed

Expected **FAIL**, got **FAIL** — as designed. *This is the control that caught defect 3:
on its first run it expected FAIL and got PASS.*

```
FAIL  entry 9380/3: ICCC-2017 assigns this code to 2 subgroups by topography (IIIb at C72.3…; IIId2 at C70.0, C70.1, C70.2…) and the entry carries no iccc3_subgroup_by_topography[]. One of them is being reported for every case, and it is wrong for exactly the cases the other subgroup exists to catch (contract §1.3)
```

Controls §1.3.1 (the C72.3 rule re-pointed at IIId2), §1.3.3 (the rule's topography changed
to C72.2, so C72.3 falls through to the IIId2 default), §1.3.4 (`topography_dependent`
flipped to false), §1.3.5 (two rules claiming C72.3, so rule order decides a subgroup) and
§1.3.6 (the rule naming IIIb with a label ICCC-2017 does not use) all behaved as designed.

---

## Contract §5.5 — `check_awaiting_layer1` already covers `9476`

Confirmed rather than written. The existing check requires an entry carrying
`awaiting_layer1` to have a `reason`, to carry `redcap_option_verified: false`, and to be
listed under `## Group 3 — open` in `docs/codes-awaiting-redcap.md`; and it requires a code
listed there as open to still carry the flag. All three directions fire.

### Control §5.5.1 — the `## Group 3 — open` section removed from the doc

Expected **FAIL**, got **FAIL** — as designed.

```
FAIL  entry 9476 carries awaiting_layer1 but is not listed under '## Group 3 — open' in docs/codes-awaiting-redcap.md (ruling 3)
```

Controls §5.5.2 (`awaiting_layer1` removed while the doc still lists 9476) and §5.5.3
(`awaiting_layer1` set with `redcap_option_verified: true`) behaved as designed. **No change
to `check_awaiting_layer1` was needed.** `docs/codes-awaiting-redcap.md` does not yet have a
`## Group 3 — open` section; it needs one before `group_03_dt.json` lands.

---

## When an anchor is missing, the check says so

Every anchored check was run with its anchor removed. None passes silently.

| Anchor removed | Result |
|---|---|
| `icdo32.sqlite` (`ICDO_DB=/nonexistent`) | WARN ×2 — rule 13 "morphology_name is NOT validated for this group … nothing is checking the names at all"; rule 6 falls back to the weaker form and says so |
| `ICCC-2017.sqlite` (`ICCC_DB=/nonexistent`) | WARN — "whether a rule names the subgroup ICCC-2017 actually assigns is UNVERIFIED" |
| `data/shared/who_cns5_table1.json` | WARN naming each unverified entity — "Table 1 conformance is UNVERIFIED, not verified" |
| `RedCap Options/Topography Redcap.md` | WARN — the rule 12 sweep falls back to the contract §3 union and says what that no longer catches |

---

## All 92 controls

| # | Control | Expected | Actual | As designed |
|---|---|---|---|---|
| 1 | 1.1 Arabic grade_system on an ADAPTR descriptive track | FAIL | FAIL | yes |
| 2 | 1.2 Roman grade_system on a who_cns5 track | FAIL | FAIL | yes |
| 3 | 1.3 who_cns5 branch also filling descriptive_diagnosis | FAIL | FAIL | yes |
| 4 | 1.4 adaptr_descriptive branch with comment nulled | FAIL | FAIL | yes |
| 5 | 1.5 grade "NA" on a diagnosis_rendering | FAIL | FAIL | yes |
| 6 | 1.6 grade "" on a diagnosis_rendering | FAIL | FAIL | yes |
| 7 | 1.7 grade "4 " — a trailing space on a valid grade | FAIL | FAIL | yes |
| 8 | 1.8 Roman numeral III on the Arabic (who_cns5) track | FAIL | FAIL | yes |
| 9 | 1.9 grade 1 on a who_cns5 track — CNS5 Table 3 grades MVNT/PLNTY at 1 | PASS | PASS | yes |
| 10 | 2.1 NEC branch reached on specimen_adequacy "inadequate" | FAIL | FAIL | yes |
| 11 | 2.2 NEC branch reached on a test that was not done | FAIL | FAIL | yes |
| 12 | 2.3 NEC branch with no asserted result at all | FAIL | FAIL | yes |
| 13 | 2.4 the same branch relabelled suffix "nos" — NOS needs no adequate result | PASS | PASS | yes |
| 14 | 3.1 tier "obligatory" on the ependymal node | FAIL | FAIL | yes |
| 15 | 3.2 referral_tier "obligatory" on the ependymal node | FAIL | FAIL | yes |
| 16 | 3.3 tier "obligatory" on the EMBRYONAL node — legal, must not fire | PASS | PASS | yes |
| 17 | 3.4 resource_level_gate.family removed | FAIL | FAIL | yes |
| 18 | 3.5 family "ependymoma" — a plausible near-miss on "ependymal" | FAIL | FAIL | yes |
| 19 | 3.6 rl_assignment dropped from the meningothelial gate | FAIL | FAIL | yes |
| 20 | 4.1 `unit` dropped from one band | FAIL | FAIL | yes |
| 21 | 4.2 unit "per_10hpf" — a plausible near-miss on "per_10_hpf" | FAIL | FAIL | yes |
| 22 | 4.3 one band re-labelled per_mm2, opening a gap in the per_10_hpf partition | FAIL | FAIL | yes |
| 23 | 4.4 "4-19" widened to "4-25", overlapping ">=20" | FAIL | FAIL | yes |
| 24 | 4.5 "0-3" narrowed to "1-3", leaving 0 uncovered | FAIL | FAIL | yes |
| 25 | 4.6 ">=20" changed to "20-40", leaving everything above 40 uncovered | FAIL | FAIL | yes |
| 26 | 4.7 the two units swept SEPARATELY — per_mm2 "<2.5"/">=2.5" beside per_10_hpf "0-3"/"4-19"/">=20" | PASS | PASS | yes |
| 27 | 5.1 entity "…ZFTA fusion positive" — hyphen written as a space | FAIL | FAIL | yes |
| 28 | 5.2 entity with a trailing space | FAIL | FAIL | yes |
| 29 | 5.3 entity spelled "tumour" where CNS5 Table 1 prints "tumor" | FAIL | FAIL | yes |
| 30 | 5.4 the "(provisional type)" extraction artefact inside an entity name | FAIL | FAIL | yes |
| 31 | 5.5 the artefact inside a shared_with[] entry | FAIL | FAIL | yes |
| 32 | 5.6 CNS5 Table 2's spelling (comma before "and") of the Table 1 entity | FAIL | FAIL | yes |
| 33 | 5.7 provisional: false on an entity CNS5 Table 1 marks provisional | FAIL | FAIL | yes |
| 34 | 5.8 code_status "shares_code" with an empty shared_with[] | FAIL | FAIL | yes |
| 35 | 5.9 code_status "no_code" left as-is on a real Table 1 no-code entity | PASS | PASS | yes |
| 36 | 6.1 the 8000/0 entry deleted | FAIL | FAIL | yes |
| 37 | 6.2 behavior_code nulled on the 9391/1 entry | FAIL | FAIL | yes |
| 38 | 6.3 an 8000/6 entry added — /6 is outside the group's "0-1,3" declaration | FAIL | FAIL | yes |
| 39 | 7.1 9536 as an alias TARGET in maps_to_morphology_codes | FAIL | FAIL | yes |
| 40 | 7.2 9422 printed in a clerk-facing `reason` | FAIL | FAIL | yes |
| 41 | 7.3 9422 mentioned in an author-facing `coding_note` — WARN, not FAIL | PASS | PASS | yes |
| 42 | 7.4 8274 as a nos_fallback_code | FAIL | FAIL | yes |
| 43 | 7.5 9536 left where it belongs — an alias INPUT in also_known_as | PASS | PASS | yes |
| 44 | 9.1 grade_resolution.unresolved given a grade | FAIL | FAIL | yes |
| 45 | 9.2 a values entry with a grade and no grade_system | FAIL | FAIL | yes |
| 46 | 9.3 a values entry with grade null and no reason | FAIL | FAIL | yes |
| 47 | 9.4 a values entry with grade "NA" | FAIL | FAIL | yes |
| 48 | 9.5 a values entry with grade "" | FAIL | FAIL | yes |
| 49 | 9.6 grade_resolution.unresolved removed entirely | FAIL | FAIL | yes |
| 50 | 9.7 grade_resolution.variable not declared in captured_variables[] | FAIL | FAIL | yes |
| 51 | 9.8 unresolved with grade null and a defer_to — the contract's own shape | PASS | PASS | yes |
| 52 | 10.1 basis_of_diagnosis 6 | FAIL | FAIL | yes |
| 53 | 10.2 basis_of_diagnosis 3 | FAIL | FAIL | yes |
| 54 | 10.3 basis_of_diagnosis 1 on a Group III terminal | FAIL | FAIL | yes |
| 55 | 10.4 basis_of_diagnosis "7" as a string | FAIL | FAIL | yes |
| 56 | 10.5 ihc_counts_as declared as 8 | FAIL | FAIL | yes |
| 57 | 10.6 basis_of_diagnosis 5 (cytology) — a real ENCR value | PASS | PASS | yes |
| 58 | 10.7 basis 5 declared against components [7, 8] | FAIL | FAIL | yes |
| 59 | 11.1 diversion_criteria[] emptied on the DIPG terminal | FAIL | FAIL | yes |
| 60 | 11.2 diversion_criteria removed entirely | FAIL | FAIL | yes |
| 61 | 11.3 basis_of_diagnosis 7 on an imaging-only terminal | FAIL | FAIL | yes |
| 62 | 11.4 no_tissue dropped | FAIL | FAIL | yes |
| 63 | 11.5 endpoint_verification "verified" | FAIL | FAIL | yes |
| 64 | 11.6 a diversion criterion with a feature and no reason | FAIL | FAIL | yes |
| 65 | 11.7 the NF1 terminal's two criteria left intact — fewer than DIPG's six is legal | PASS | PASS | yes |
| 66 | 12.1 C72.9 given to g3_midline as well as g3_unspecified | FAIL | FAIL | yes |
| 67 | 12.2 C72.4 removed from g3_midline, leaving it routed to no tree | FAIL | FAIL | yes |
| 68 | 12.3 g3_supratentorial's range written C71.5-C71.0 (descending) | FAIL | FAIL | yes |
| 69 | 12.4 every tree's topography declaration removed | FAIL | FAIL | yes |
| 70 | 12.5 C70.2-C70.8, C72.6 and C72.7 owned by nobody — codes Layer 1 does not carry | PASS | PASS | yes |
| 71 | 13.1 a trailing space on a morphology_name | FAIL | FAIL | yes |
| 72 | 13.2 "Medulloblastoma, SHH activated, NOS" hyphenated to "SHH-activated" | FAIL | FAIL | yes |
| 73 | 13.3 "tumor" spelled "tumour" in a morphology_name | FAIL | FAIL | yes |
| 74 | 13.4 the same drifted name flagged redcap_option_verified: true | FAIL | FAIL | yes |
| 75 | 13.5 a name that is right for a DIFFERENT behaviour of the same code | FAIL | FAIL | yes |
| 76 | 13.6 9475's source_term corrupted to the corrected spelling — the anchor goes | FAIL | FAIL | yes |
| 77 | 13.7 source_term added to an entry that is not the one declared exemption | FAIL | FAIL | yes |
| 78 | 13.8 a nos_fallback naming a string no entry on that code carries | FAIL | FAIL | yes |
| 79 | 13.9 9475 displaying the corrected spelling behind its source_term — the one legal exemption | PASS | PASS | yes |
| 80 | §1.3.1 the 9380 C72.3 rule re-pointed at IIId2 | FAIL | FAIL | yes |
| 81 | §1.3.2 the 9380 rule list removed — one pair, two ICCC subgroups | FAIL | FAIL | yes |
| 82 | §1.3.3 the rule's topography_in changed from C72.3 to C72.2 | FAIL | FAIL | yes |
| 83 | §1.3.4 topography_dependent flipped to false with the rules left in place | FAIL | FAIL | yes |
| 84 | §1.3.5 a second rule also claiming C72.3 | FAIL | FAIL | yes |
| 85 | §1.3.6 the rule naming IIIb with the wrong ICCC-2017 label | FAIL | FAIL | yes |
| 86 | §5.5.1 the "## Group 3 — open" section removed from docs/codes-awaiting-redcap.md | FAIL | FAIL | yes |
| 87 | §5.5.2 awaiting_layer1 removed from 9476 while the doc still lists it | FAIL | FAIL | yes |
| 88 | §5.5.3 awaiting_layer1 present with redcap_option_verified true | FAIL | FAIL | yes |
| 89 | X.1 diversion_criteria[] and grade_resolution outcomes on correct data — check_non_reportable_terminals must NOT read them as code-less terminals | PASS | PASS | yes |
| 90 | X.2 a genuine code-less terminal with a `reason` added beside them — the narrowing must not have absorbed it | FAIL | FAIL | yes |
| 91 | X.3 a dict carrying `grade` and `reason` under some OTHER key than grade_resolution — the predicate is path-scoped, so this is still a terminal | FAIL | FAIL | yes |
| 92 | X.4 topography declared under the synonym `owns_topography` | PASS | PASS | yes |

---

## Two Layer 1 findings the checks turned up

Not defects in the tool. Reported here because they are owed to Layer 1.

1. **`C71.0` (Cerebrum) is missing from `ICD coding/RedCap Options/Topography Redcap.md`.**
   The list runs `700, 701, 709, 711, 712 …` — there is no `710`. Contract §3 gives C71.0 to
   `g3_supratentorial`, so a supratentorial hemispheric tumour has a tree and no REDCap
   topography option. `check_group3_topography_map` reports it as a WARN on every build.

2. **`8280`, `8281` and `8300` have no non-obsolete term in ICD-O-3.2.** Every row for all
   three, Preferred included, is marked `[obs]` — `Acidophil adenoma`, `Acidophil carcinoma`,
   `Mixed acidophil-basophil adenoma`, `Mixed acidophil-basophil carcinoma`, `Basophil
   adenoma`, `Basophil carcinoma`. They round-trip, so rule 13 passes, but the round-trip
   WARNs: these are six of the group's 108 entries and whatever they display will be an
   obsolete pituitary term. That is a decision for the registrar, not for the validator.

---

## What could not be checked statically

Stated plainly rather than covered by a check that looks like it covers it.

- **Contract §2(2), `required_rl: "V"` must produce an upgrade line that says the test is
  *unavailable*, not one that dangles it as a next step.** That is a rendering rule. The
  validator can see the field; it cannot see the sentence `app.js` builds from it. There is
  a narrow guard (an explicit `upgrade_line_says_unavailable: false` FAILs) but the real
  rule needs the browser pass of contract §7 step 9.

- **Contract §2(2), `rl_assignment: "by_analogy"` on the paediatric-type diffuse gliomas.**
  The contract exempts "the paediatric-type diffuse gliomas" from ADAPTR sourcing, and the
  `family` vocabulary has one value, `diffuse_glial`, covering both those and the adult-type
  gliomas ADAPTR does cover. A blanket rule on `diffuse_glial` would false-FAIL the
  adult-type nodes, so the check enforces the six families the contract names
  unambiguously and leaves `diffuse_glial` alone. Either the vocabulary needs a
  `paediatric_diffuse_glial` member or this stays a reading job.

- **Contract §2(5), "0 and 9 override".** Enforced only where a holder writes down the
  component codes it derived from (`basis_components[]`). Where the basis is a bare number
  the validator has nothing to compare it against — it can prove the value is in the ENCR
  set, is not 3, 6 or 1, and is 2 on an imaging-only terminal, and that is all.

- **Contract §2(3), the `FET-CREB fusion positive` / `fusion-positive` divergence.**
  Revision 2 records what Table 7 and the prose print and does **not** say which Table 1
  uses. `data/shared/who_cns5_table1.json` prints `Intracranial mesenchymal tumor, FET-CREB
  fusion-positive`, and the check enforces that string because the transcription says so —
  but it is worth a second reading against the source, because it is the one divergence
  Revision 2 flagged and did not resolve.

- **Contract §4, the AFP / β-hCG rule, specimen adequacy, and intraoperative diagnosis.**
  These are process steps expressed through existing constructs (`test_result_states`,
  `numeric_gate`, node wiring). No Group III-specific check was written for them; the
  existing `check_test_result_states` rule that `not_assessable` may not share a destination
  with `negative` is what carries the adequacy rule, and it already runs on Group 3.

- **Contract §6 rule 14 itself** is this document.

- **Rule 5 against the full 144 rows.** `who_cns5_table1.json` carries 109 type rows; the
  other 35 printed rows are family headings and are not entity names. The check validates
  against the 109. If a Group III entity annotation ever needs a string that is a heading
  rather than a type, it will FAIL and the transcription is what needs extending.

- **A green build is still not a working tool.** Every check here tests the data. Group 2
  passed 74 checks with 15 of its 61 nodes not rendering at all, because the fault was in
  the seam between the data and the renderer. Contract §7 step 9's browser pass is not
  optional and nothing in this document substitutes for it.

---

# Group IV checks — negative controls

Evidence that the `behaviour_exclusion` field (contract §3) and the eight validation rules
added for it (contract §8) catch what they claim to, and that they fire on nothing else.
Same method as the Group II and Group III sections above: break the data deliberately,
confirm the check FAILs, restore, confirm it passes — and separately confirm it does
**not** fire on correct data or on another group's data, because a false FAIL is the more
corrosive failure.

**`data/database/group_04_dt.json` did not exist when this work was done.** Three other
agents are authoring trees into it in parallel, and this task was explicitly told not to
touch it, not to read it, and not to run `python3 build/build_database.py` — the standing
rule on this project, restated for this build: the trees do not exist yet, a real run would
fail on things later tasks fix, and would tell this task nothing about whether ITS OWN
checks work. So every control here runs the way contract §8's own instructions describe:
**the check functions are imported directly from `build/build_database.py` and called
against a synthetic `DTContext`, the way a unit test would** — never through `run_build()`,
never through `main()`, and never against the real file.

## The fixture

A Python harness (`g4_negative_controls.py`, kept outside the repo in the session
scratchpad — it is a test script, not a build artefact) builds one synthetic, in-memory
`group_04_dt.json`-shaped `dict` and wraps it in `build_database.DTContext` directly:

- **18 `morphology_entries[]`**, one per contract §1's inventory table, every
  `(morphology_code, morphology_name, behavior_code)` triple copied character-for-character
  from a direct query against `icdo32.sqlite` (not from the contract's prose table, and not
  from memory) before being written into the fixture — the same discipline rule 13/8
  itself enforces on real data.
- **Four trees**, one per contract §5's table (`g4_sympathoadrenal`, `g4_head_neck_paraganglia`,
  `g4_sinonasal`, `g4_other_peripheral`), each declaring a topography under
  `metadata.decision_trees[].topography`.
- **One live `behaviour_exclusion`** — the ganglioneuroma case, contract §3's own worked
  example verbatim — on `g4_sympathoadrenal`'s `histology_subclassification` node,
  alongside a sibling option that emits `9500` at basis 7.
- **One live `imaging_pathway`** (`sa_imaging`) with a non-empty `biochemical_questions[]`,
  a basis-4 terminal emitting `9500`, and a basis-1 terminal that emits no code and refers
  to Group 12 — the two legal shapes contract §4.2 describes.
- **9504** is authored in `morphology_entries[]` (entry 14) and referenced by NO node — the
  D2 shape under test.

Because Group IV's own topography scope is close to the whole ICD-O topography space
(contract §5: "C00.0–C80.9 for fourteen of its eighteen codes"), sweeping the REAL Layer 1
topography list for `check_group4_topography_map` would require the fixture's four trees to
between them own several hundred real subcodes, which is unit-testing the wrong thing — it
would prove the fixture was transcribed correctly, not that the check's TOTAL/DISJOINT logic
and its C70–72 cross-check are correct. So for rule 5 only, `build_database._existing_topography`
(the function that reads Layer 1's real topography option list) is monkey-patched for the
duration of the call to return a small, fixed, four- or five-code universe
(`{"C74.9","C75.5","C30.0","C47.0"}`, one per tree, plus `"C70.9"` for the cross-check
control only). This is standard test isolation — stubbing the one external dependency so the
function under test is exercised on a domain small enough to reason about by hand — and it
is declared here rather than left implicit. It does **not** touch the real Layer 1 file, and
it is undone (the real function restored) immediately after each call.

Every other check (behaviour_exclusion's round-trip, rule 7's round-trip) reads the REAL
`icdo32.sqlite` at its real path, read-only — that is the anchor these two rules exist to
key off, and stubbing it would prove nothing.

## The false-FAIL control (correct data)

Every one of the eight rules reports **0 FAIL** against the unmodified fixture, with an OK
line describing real content:

```
OK    1 behaviour_exclusion block(s) well formed: all six keys present, icdo_code/icdo_behaviour/icdo_term
      round-trip to the Preferred ICD-O-3.2 term, the named behaviour is outside the group's own
      declaration, no branch also carries morphology_code, and reason is non-empty (rule 1)
OK    18 Group IV morphology_entries[] object(s) all carry behavior_code 3, the group's own declaration (rule 2)
OK    RULE 3 — 8683 appears nowhere as a morphology_code, a nos_fallback_code or an alias target in
      group_04_dt.json or its alias file (contract §0.2, §8 rule 3)
OK    9504 (Spongioneuroblastoma) is unreachable: no morphology_code emission, node-level nos_fallback or
      entry-level nos_fallback_code anywhere in the file names it (rule 4)
OK    topography map is total and disjoint: all 4 recordable code(s) resolve to exactly one of 4 tree(s),
      and no tree declaring C70.0-C72.9 emits 9501-9504 (rule 5)
OK    3 basis-1/2/4 terminal(s): none emits a Group IV code at basis 1 or 2 (Visser rule 5 — Group IV has
      no Table 3 entries), and every basis-4 emission is 9500 or 8700 with a non-empty
      biochemical_questions[] (rule 6)
OK    RULE 8 — 9364 appears nowhere as a morphology_code in group_04_dt.json (contract §2.4, §8 rule 8)
OK    18/18 (code, name, behaviour) triple(s) exist verbatim in icdo32.sqlite; 0 declared name
      exemption(s), each still anchored to a string the database actually carries (rules 8 and 13)
NOTE  group 4: morphology_name is checked by check_icdo32_round_trip() against icdo32.sqlite instead of
      against the REDCap option file (contract §5.2 for Group 3; §1.1a for Group 4). […] Groups 1 and 2
      are unaffected.
```

**All 62 assertions in the harness behaved as designed** — 21 expected FAIL and did, 41
expected PASS/no-op and did, 0 mismatches.

---

## `check_behaviour_exclusion` (contract §3, §8 rule 1)

**What it catches.** All six keys required and non-null/non-empty; `icdo_code`/
`icdo_behaviour`/`icdo_term` round-trip to the **Preferred** ICD-O-3.2 term at that pair;
`icdo_behaviour` must NOT be a member of the group's own declaration; a branch may not carry
both `behaviour_exclusion` and `morphology_code`; `reason` non-empty.

### Control 1.1 — `reason` deleted

Expected **FAIL**, got **FAIL**:

```
FAIL  node sa_histology_subtype (options[1]) behaviour_exclusion is missing, null or empty for reason —
      all six keys are REQUIRED (contract §3, §8 rule 1)
```

Restored: **0 FAIL.**

### Control 1.2 — THE SUBTLE ONE: `icdo_behaviour` set to `"3"`, a behaviour Group IV admits

Rule 1's own text calls this out as the one to get right: a `behaviour_exclusion` naming an
admitted behaviour would hide a code that should have been emitted. Expected **FAIL**, got
**FAIL** — and a second, independent FAIL alongside it, because `icdo_term` ("Ganglioneuroma")
is real only at `9490/0`, not `9490/3` ("Ganglioneuroblastoma"), so the round-trip rule fires
too. Both are real defects on this mutated fixture; nothing was suppressed:

```
FAIL  node sa_histology_subtype (options[1]) behaviour_exclusion: icdo_term 'Ganglioneuroma' is not a
      term ICD-O-3.2 carries for 9490/3. (contract §3, §8 rule 1)
FAIL  node sa_histology_subtype (options[1]) behaviour_exclusion: icdo_behaviour '3' IS in Group IV's
      own declaration (behaviour 3). A behaviour_exclusion may only name a behaviour the group does NOT
      admit — naming an admitted one would HIDE a code that should have been emitted as a real Group IV
      entry instead of excluded (contract §3, §8 rule 1 — the subtle one)
```

Restored: **0 FAIL.**

### Control 1.3 — the same branch also given `morphology_code: "9490"`

Expected **FAIL**, got **FAIL**:

```
FAIL  node sa_histology_subtype (options[1]) behaviour_exclusion: this branch ALSO carries
      morphology_code '9490'. behaviour_exclusion and morphology_code are mutually exclusive
      destinations — app.js's advance() checks morphology_code first, so this exclusion would never
      fire at runtime (contract §3, §8 rule 1)
```

Restored: **0 FAIL.**

### Control 1.4 — `icdo_term` is a real but non-Preferred term (`9501/0` "Diktyoma, benign" is a Synonym; the Preferred term is "Medulloepithelioma, benign")

Expected **FAIL**, got **FAIL**:

```
FAIL  node sa_histology_subtype (options[1]) behaviour_exclusion: icdo_term 'Diktyoma, benign' is a
      Synonym term for 9501/0, not the PREFERRED one. Contract §3 requires the Preferred term at that
      (code, behaviour) pair
```

Restored: **0 FAIL.**

### Control 1.5 — `icdo_term` case-drifted (`"GANGLIONEUROMA"`)

Expected **FAIL**, got **FAIL**, with the near-miss printed:

```
FAIL  node sa_histology_subtype (options[1]) behaviour_exclusion: icdo_term 'GANGLIONEUROMA' is not a
      term ICD-O-3.2 carries for 9490/0.
               ICD-O-3.2 has  : 'Ganglioneuroma' (contract §3, §8 rule 1)
```

Restored: **0 FAIL.**

---

## `check_group4_behaviour_declaration` (contract §1, §8 rule 2)

**What it catches.** Any `morphology_entries[]` object whose `behavior_code` is not `"3"` —
Group IV's own declaration, read off the named constant `GROUP4_BEHAVIOUR_DECLARED` rather
than compared against a bare literal inline (see "generalised or hardcoded", below).

### Control 2.1 — the `9490` entry moved to `behavior_code: "0"`

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 2 — morphology_entries[8] (code 9490) carries behavior_code '0'; Group IV's own declaration
      is behaviour 3 and nothing else (contract §1, §8 rule 2). Any other value files the entry under a
      behaviour ICCC-3 does not register for this group
```

Restored: **0 FAIL.**

### Control 2.2 — regression: a Group III-shaped entry at `behavior_code: "1"` (legal for Group III) run through this same function

Expected **`[]`** (a true no-op — the function is scoped to Group 4 only), got **`[]`**.

---

## `check_group4_absent_codes` — `8683` (contract §0.2, §8 rule 3)

**What it catches.** `8683` as a `morphology_code`, a `nos_fallback_code`, or an alias
target — never a substring sweep of the file, so the contract §0.2 prose explaining the
exclusion is free to name the digits.

### Control 3.1 — `8683` authored as a `morphology_code`

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 3 — group_04_dt.json.decision_trees[1].nodes[0].options[2].morphology_code carries code
      8683. ICD-O-3.2 carries 8683 only at /0 (Gangliocytic paraganglioma); ICCC-3 Group IV admits
      behaviour 3 only, so there is no Group IV entry for it (contract §0.2, §8 rule 3)
```

Restored: **0 FAIL.**

### Control 3.2 — `8683` named in an author-facing `coding_note`

Expected **WARN, not FAIL** (this is the prose caveat the contract explicitly asks for), got
exactly that:

```
WARN  RULE 3 — […].coding_note mentions 8683 in author-facing text. That is fine and expected — this
      field is never displayed, so no clerk reads it, and the contract's own reasoning for excluding
      the code is written in exactly these terms (contract §0.2, §8 rule 3)
OK    RULE 3 — 8683 appears nowhere as a morphology_code, a nos_fallback_code or an alias target in
      group_04_dt.json or its alias file (contract §0.2, §8 rule 3)
```

Restored: **0 FAIL.**

### Control 3.3 — `8683` named in a clerk-facing `reason`

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 3 — group_04_dt.json.decision_trees[0].nodes[2].options[1].reason prints 8683 in text a
      clerk reads. A code on screen is a code that gets entered (contract §0.2, §8 rule 3)
```

Restored: **0 FAIL.**

---

## `check_group4_9504_unreachable` (contract §2.3, ruling D2, §8 rule 4)

**What it catches.** `9504` reached by any of the three live paths: a direct
`morphology_code` emission, a node-level `nos_fallback`, or an entry-level
`nos_fallback_code` naming it.

### Control 4.1 — a node emits `morphology_code: "9504"` directly

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 4 — node op_entry (options[2]) emits morphology_code 9504. Spongioneuroblastoma is
      authored in morphology_entries[] and reachable from NO tree — no current WHO entity lives on the
      stem (contract §2.3, ruling D2, §8 rule 4)
```

Restored: **0 FAIL.**

### Control 4.2 — a node-level `nos_fallback` names `9504`

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 4 — node op_entry (nos_fallback) nos_fallback names code 9504. Same rule as a direct
      emission: 9504 is reachable from no tree (contract §2.3, ruling D2, §8 rule 4)
```

Restored: **0 FAIL.**

### Control 4.3 — an entry-level `nos_fallback_code` (on the `9503` entry) names `9504`

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 4 — morphology_entries[12] (code 9503) declares nos_fallback_code 9504. An entry-level
      fallback IS a live path to the code, and 9504 must be reachable from no tree at all (contract
      §2.3, ruling D2, §8 rule 4)
```

Restored: **0 FAIL.**

---

## `check_group4_topography_map` (contract §5, §8 rule 5)

**What it catches.** An unrouted topography code, a duplicated one, and — the second
clause — `9501`–`9504` reachable from a tree whose own declared topography sits inside
`C70.0`–`C72.9`, which belongs to Group III.

### Control 5.1 — `g4_other_peripheral`'s declared topography emptied (unrouted)

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 5 — 1 topography code(s) resolve to NO tree: C47.0. A case at one of these reaches the
      router, finds no handoff and dead-ends (contract §5, §8 rule 5)
```

Restored: **0 FAIL.**

### Control 5.2 — `C74.9` also declared by `g4_head_neck_paraganglia` (duplicate)

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 5 — topography C74.9 resolves to 2 trees (g4_head_neck_paraganglia,
      g4_sympathoadrenal). The map must be disjoint: a duplicate does not fail, it silently picks
      whichever row the engine reads first — which is not a decision anybody made (contract §5, §8
      rule 5)
```

Restored: **0 FAIL.**

### Control 5.3 — `g4_other_peripheral` claims `C70.9` and its node still emits `9501`

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 5 — node op_entry (options[0]) in tree 'g4_other_peripheral' emits 9501. This tree
      declares topography inside C70.0-C72.9, which belongs to Group III (contract §0.6, §2.5) —
      9501-9504 must be unreachable from any node there
```

Restored: **0 FAIL.**

---

## `check_visser_table4_gate` (contract §4.2, §8 rule 6) — REVISED mid-build

**The correction.** Specified first as binding on `no_tissue: true`. A finished tree exposed
the blind spot: `8680` emitted off a referral-letter-only finding at `basis_of_diagnosis: 1`,
and `9522` off an inadequate specimen at basis 2 — neither carrying `no_tissue: true`, so the
`no_tissue`-bound check never saw either. Rewritten to bind on `basis_of_diagnosis` itself,
at any node type, per the corrected spec: basis 1/2 emitting a code is always a build error
for Group IV (Visser rule 5, p. 03 — Group IV has no Table 3 exceptions), and basis 4 may
emit only `9500`/`8700` with a non-empty `biochemical_questions[]` (Visser rule 6, p. 05).
The `no_tissue`/`endpoint_verification`/`diversion_criteria[]` requirements stay exactly as
they were, in the pre-existing, group-agnostic `check_imaging_terminals()` (rule 11) — this
rule does not replace or duplicate that one.

### Control 6.1 — the coordinator's own example 1: `8680` emitted at basis 1 (referral-letter-only)

Expected **FAIL**, got **FAIL**:

```
FAIL  node hn_entry (options[0]): RULE 6 — basis_of_diagnosis 1 emits morphology_code 8680. Visser
      rule 5, p. 03: basis 1 or 2 means 8000/3 except for Table 3 entities, and ICCC-3 Group IV has
      NO Table 3 entries — so no Group IV code may be emitted at this basis at all (contract §4.2, §8
      rule 6)
```

Restored: **0 FAIL.**

### Control 6.2 — the coordinator's own example 2: `9522` emitted at basis 2 (inadequate specimen)

Expected **FAIL**, got **FAIL**:

```
FAIL  node sn_entry (options[0]): RULE 6 — basis_of_diagnosis 2 emits morphology_code 9522. Visser
      rule 5, p. 03: basis 1 or 2 means 8000/3 except for Table 3 entities, and ICCC-3 Group IV has NO
      Table 3 entries — so no Group IV code may be emitted at this basis at all (contract §4.2, §8
      rule 6)
```

Restored: **0 FAIL.**

### Control 6.3 — a basis-1, no-code terminal referring to the wrong group (8, not 12)

Expected **FAIL**, got **FAIL**:

```
FAIL  node sa_imaging (options[1]): RULE 6 — basis_of_diagnosis 1 emits no morphology_code and must
      instead carry refer_group: 12 (the 8000-8005 dual-group rule to Group XII), got 8. Visser rule
      5, p. 03: with no Table 3 entry to except it, everything at this basis is 8000/3, which is not a
      Group IV code (contract §4.2, §8 rule 6)
```

Restored: **0 FAIL.**

### Control 6.4 — the coordinator's requested basis-4 control: `9501` emitted at basis 4

Expected **FAIL**, got **FAIL**:

```
FAIL  node sa_imaging (options[0]): RULE 6 — basis_of_diagnosis 4 emits 9501, which is neither 9500
      nor 8700. Visser Table 4 (p. 06) names exactly these two entities a marker constellation alone
      may establish (contract §4.2, §8 rule 6)
```

Restored: **0 FAIL.**

### Control 6.5 — basis 4, correct code (`9500`), `biochemical_questions[]` emptied

Expected **FAIL**, got **FAIL**:

```
FAIL  node sa_imaging (options[0]): RULE 6 — biochemical_questions[] is missing or empty on the
      reaching imaging_pathway for a basis-4 9500 terminal. Visser rule 6, p. 05: basis 4 never stands
      alone — the marker must accompany a clinical diagnosis or investigation, and this is the field
      that records it (contract §4.2, §8 rule 6)
```

Restored: **0 FAIL.**

### Control 6.6 — THE REGRESSION THE COORDINATOR ASKED FOR: a Group III fixture emitting its own group NOS code (`9473`) at basis 2

Group III legitimately does this — Visser Table 3 carries forty-three CNS rows, so an
inadequate CNS specimen defaulting to the group NOS code at basis 2 is an entity Table 3
explicitly covers. Expected **`[]`** (still passes — the check is scoped to Group 4 only),
got **`[]`**.

---

## `check_group4_not_a_group_code` — `9364` (contract §2.4, §8 rule 8, ruling D4)

**What it catches.** `9364` as a `morphology_code` in `group_04_dt.json` — narrower than
rule 3: `9364` is a real code that a `refer_code` hint or D4's own `coding_note` reasoning
may legitimately carry, so only the emitting field is bound.

### Control 8.1 — `9364` authored as a `morphology_code`

Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 8 — group_04_dt.json.decision_trees[3].nodes[0].options[2].morphology_code carries code
      9364. ICD-O-3.2 moved Ewing sarcoma to 9364/3 and made it the peripheral neuroectodermal tumour
      / pPNET code too (ruling D4); Group IV's pPNET aliases refer OUT to Group VIII/IX rather than
      emitting it here (contract §2.4, §8 rule 8)
```

Restored: **0 FAIL.**

### Control 8.2 — `9364` named in an author-facing `coding_note`

Expected **WARN, not FAIL**, got exactly that (same prose caveat as rule 3):

```
WARN  RULE 8 — […].coding_note mentions 9364 in author-facing text. That is fine and expected — […]
      (contract §2.4, §8 rule 8)
```

Restored: **0 FAIL.**

### Control 8.3 — the false-FAIL guard: `9364` as a legitimate `refer_code` hint on a referral branch

D4's own design has `9364` appear exactly this way. Expected **PASS (no FAIL, not even a
WARN)**, got **PASS** — `refer_code` is outside this rule's scope by design.

Restored (no change needed): **0 FAIL.**

---

## `check_icdo32_round_trip` extended to Group 4, and `check_redcap_exact_names` stepping aside (contract §1.1a, §8 rule 7)

**What it catches.** Every `(morphology_code, morphology_name, behavior_code)` triple in
`group_04_dt.json` must exist verbatim, as the **Preferred** term or otherwise, in
`icdo32.sqlite` — the same rule Group 3 already runs under, now also scoped to Group 4.
`check_redcap_exact_names` steps aside for Group 4 exactly as it already does for Group 3,
so the two REDCap/ICD-O-3.2 divergences contract §0.3 documents (`8690`/"Glomus jugulare
tumor, NOS", `9522`/"Esthesioneuroblastoma", …) are never matched against the wrong Layer 1.

### Control 7.1 — `9522`'s `morphology_name` case-drifted to `"Olfactory Neuroblastoma"`

Expected **FAIL**, got **FAIL**, with the near-miss printed:

```
FAIL  entry 9522/3: the triple (9522, 'Olfactory Neuroblastoma', 3) does not exist in ICD-O-3.2.
      RULE 13 — every name the engine can emit must be a real term for that code at that behaviour,
      checked against the database and not against the REDCap option list […] (contract §5.2, §6 rule
      13).
               ICD-O-3.2 has  : 'Olfactory neuroblastoma'
```

Restored: **0 FAIL.**

### Control 7.2 — the same Group 4 file run through `check_redcap_exact_names` with a synthetic REDCap option (`9522` → `"Esthesioneuroblastoma"`, the real REDCap synonym) that would fail an exact-string match

Expected: steps aside with a single **NOTE**, no comparison attempted. Got exactly that:

```
NOTE  group 4: morphology_name is checked by check_icdo32_round_trip() against icdo32.sqlite instead
      of against the REDCap option file (contract §5.2 for Group 3; §1.1a for Group 4). […]
```

### Control 7.3 — REGRESSION: Group 1 is untouched by either change

`check_icdo32_round_trip` on a synthetic Group 1 fixture still returns `[]` (still steps
aside — unchanged). `check_redcap_exact_names` on the same fixture, given a REDCap option
that does NOT match the authored name, still does its **real** comparison and FAILs exactly
as before:

```
FAIL  entry 9861: a REDCap option EXISTS for this code and morphology_name is not character-identical
      to it (redcap_option_verified: True — the flag does not exempt it).
               dt.json : 'Right name'
               REDCap  : 'Wrong name entirely'
```

---

## Regression — all seven new Group-4-scoped checks are a true no-op on Groups 1–3

Every one of `check_behaviour_exclusion`, `check_group4_behaviour_declaration`,
`check_group4_absent_codes`, `check_group4_9504_unreachable`, `check_group4_topography_map`,
`check_visser_table4_gate` and `check_group4_not_a_group_code` was run against a minimal
synthetic fixture with `metadata.group_id` set to 1, 2 and 3 in turn. **Every call returned
exactly `[]`** — not an OK, not a NOTE, not a WARN — confirming the `if ctx.group != GROUP4:
return []` guard at the top of each (contract §8's own scoping requirement, and this task's
"do not regress Groups 1–3").

## How rule 2 reads the group's declaration

Contract §8 asked, for rule 2: "Make this general — read the group's declaration rather than
hardcoding `"3"` for group 4 if you can do so cleanly; say which you did." Done narrowly, not
generally: the expected set is `GROUP4_BEHAVIOUR_DECLARED = {"3"}`, a named constant declared
once and cited to contract §1, and `check_group4_behaviour_declaration()` compares against
that constant rather than a bare `"3"` written inline in the loop — so the function itself
never contains the literal string being checked for. It is **not** generalised into a
cross-group lookup table keyed by `ctx.group` (which would also run the same flat membership
test over Group III's ~90 non-overloaded entries): Group III's own declaration is already
validated, more strongly, by `check_group3_behaviour_split()`'s per-code computation against
ICD-O-3.2, and extending a second, weaker test onto live Group III data has not been verified
against the real `group_03_dt.json` — this task must not run the real build — so it was left
scoped to Group 4 only, matching every other group-specific check already in this file.

## What this could not check

- **The real Layer 1 topography sweep for rule 5.** `_existing_topography()` was stubbed to
  a five-code universe for the reason given above (the fixture). The check's TOTAL/DISJOINT
  and C70–72 cross-check LOGIC is proven; that it correctly enumerates the real, full
  C00.0–C80.9 sweep against the real `RedCap Options/Topography Redcap.md` is not proven
  until a real `group_04_dt.json` exists and the standing build (contract §9 step 9) runs
  against it.
- **`check_visser_table4_gate`'s interaction with real trees' node wiring** — the fixture's
  `sa_imaging` node is deliberately small (one basis-4 branch, one basis-1 branch). The four
  real trees will have considerably more branches per node; the per-holder, per-branch loop
  was written to be shape-agnostic (it walks every branch container generically), but that is
  a code-reading claim until the real trees exist.
- **A green build is still not a working tool.** Everything above tests the data and the
  validator. Contract §9 step 9's browser pass — driving the real tool once all four trees
  exist — is not optional and nothing here substitutes for it.

---

# Group IV validator false-FAILs — three fixes (2026-09-18)

The real `group_04_dt.json` now exists (four trees, 34 nodes, all committed) — the gap the
previous section's "What this could not check" named first. A full `python3
build/build_database.py` run against it surfaced three checks FAILing on data that was
correct: `check_non_reportable_terminals` misreading a `nos_fallback` object and a
`behaviour_exclusion` object as code-less terminals (7 FAIL), `check_group4_topography_map`
sweeping the whole registry's topography space instead of Group IV's own (1 FAIL, 292 codes
named), and `check_group4_absent_codes`/`check_group4_not_a_group_code` (RULE 3/8) failing on
`8683`/`9364` appearing in clerk-facing PROSE rather than as an emitted code (3 FAIL). This
section is evidence that the fix in each case made the check MORE correct — tightened where
it was too loose (RULE 5 now reads Group IV's real candidate universe instead of assuming
one), loosened only where the old shape test demanded something the schema never required
(`nos_fallback.name`) or the contract never banned (a code named in a `reason`) — and that
none of the three now fires on nothing, or on the wrong thing.

## Method

`data/database/group_04_dt.json` is fully built and committed on this branch, so — unlike
the Group IV section above, written before it existed — every control here runs the check
functions **directly against the REAL file**, imported as a module the way a unit test
would (`build_database` loaded via `importlib`, never through `run_build()`/`main()`).
Every mutation is made on an in-memory `copy.deepcopy()` of the loaded dict fed to a fresh
`DTContext`; the real file is never written. `git status` after every run in this section
showed `build/build_database.py` as the only modified file. The one control that needs a
mutated `presentation_router.json` (2c, below) builds a throwaway temp directory holding an
unmodified **copy** of the real `data/shared/topography_codes.json` and a mutated copy of
`presentation_router.json`, and points the check's `repo` argument at that temp directory —
the real repo tree is untouched. The harness is `g4_validator_bugfix_controls.py`, kept in
the session scratchpad, not the repo.

## The false-FAIL control (correct data, unmodified)

Baseline run of all five touched checks against the real, unmodified file: **0 FAIL** on
every one.

```
OK    1 non-reportable terminal(s) emit no morphology code; no unflagged code-less terminals
OK    3 behaviour_exclusion block(s) well formed: all six keys present, icdo_code/icdo_behaviour/icdo_term
      round-trip to the Preferred ICD-O-3.2 term, the named behaviour is outside the group's own
      declaration, no branch also carries morphology_code, and reason is non-empty (rule 1)
WARN  1 topography code(s) are owned by a tree but are outside the sweep: C80.9
OK    topography map is total and disjoint: all 34 Group IV candidate topography code(s) resolve to
      exactly one of 4 tree(s), the router's default catch-all resolves to a tree this file declares,
      and no tree declaring C70.0-C72.9 emits 9501-9504 (rule 5)
OK    RULE 3 — 8683 appears nowhere as a morphology_code, a nos_fallback_code or an alias target in
      group_04_dt.json or its alias file (contract §0.2, §8 rule 3)
OK    RULE 8 — 9364 appears nowhere as a morphology_code in group_04_dt.json (contract §2.4, §8 rule 8)
```

(The `C80.9` WARN is expected and correct, not a residual defect: `C80.9`/Unknown Primary
Site is `"route_by_morphology"` in `topography_codes.json`, not a member of Group IV's
candidate-group-4 list, so it sits outside the 34-code positive sweep even though
`g4_other_peripheral` legitimately declares it as the router's own catch-all target. See
`_group4_candidate_topography()`'s docstring.)

A full `python3 build/build_database.py` run before and after the fix, diffed line for
line: **Groups 1, 2 and 3's sections are byte-identical** (see "Regression" below) and the
summary moved from `FAIL: 11` / `BUILD FAILED` to `FAIL: 0` / `BUILD PASSED`, with every one
of the 11 cleared FAILs matching one of the three bugs below and no new FAIL or WARN
appearing anywhere else.

---

## `check_non_reportable_terminals` / `is_nos_fallback_object()` — the `nos_fallback.name` false-FAIL

**What changed.** `is_nos_fallback_object()` required BOTH `code` and `name` on the object
hanging off a `nos_fallback` key before treating it as the DT-master `nos_fallback`
construct and exempting it from the code-less-terminal sweep. Nothing in the schema
requires `name`: `app.js`'s `fallbackTarget()` reads only `.code`/`.behavior_code`/`.reason`
off it, and `check_terminal_codes_exist()` only ever demanded `.code`. Groups 1–3 happened
to always author a `name` alongside it; Group 4's own fallbacks correctly do not
(`{"code": "9500", "behavior_code": "3", "reason": "…"}` on `sa_ihc_checklist` and three
siblings). Requiring `name` made the predicate miss exactly these four, so each fell through
to the near-miss net and was reported as an unflagged code-less terminal. **Fixed by
dropping the `name` requirement — `code` alone is now the shape test**, alongside the
existing path test (`where` ends in `"nos_fallback"`). This is strictly a loosening of an
over-strict shape test to match the actual, load-bearing schema; the path test still means
the predicate can only ever match an object that IS hung off a `nos_fallback` key, and
`check_terminal_codes_exist()` still independently demands and validates `.code`, so a
`nos_fallback` block with no `code` at all is still caught (control 1b, below) — the
loosening cannot mask a genuinely broken fallback.

### Control 1a — a real code-less terminal (reason, no destination) still FAILs

`op_medulloepithelioma` `options[0]` (`morphology_code: "9501"`, a `reason`, no `next_node`)
had its `morphology_code` deleted in memory. Expected **FAIL**, got **FAIL**:

```
FAIL  op_medulloepithelioma (options[0]) carries a 'reason' but no destination and no recognised
      non-reportable flag — if this is the clean 'not a reportable malignancy' terminal it must say
      so with "non_reportable": true; if it belongs to another ICCC-3 group it must say so with
      "refer_group"; otherwise its emit-no-code rule is never checked
```

Restored (pristine data): **0 FAIL** — `OK 1 non-reportable terminal(s) emit no morphology
code; no unflagged code-less terminals`.

### Control 1b — a `nos_fallback` with no `code` at all still FAILs (the loosened predicate stays narrow)

`sa_ihc_checklist.nos_fallback` (`{"code", "behavior_code", "reason"}`) had `.code` deleted
in memory, leaving exactly the broken shape the dropped `name` requirement must NOT start
waving through. Expected **FAIL**, got **FAIL**:

```
FAIL  sa_ihc_checklist (nos_fallback) carries a 'reason' but no destination and no recognised
      non-reportable flag — if this is the clean 'not a reportable malignancy' terminal it must say
      so with "non_reportable": true; if it belongs to another ICCC-3 group it must say so with
      "refer_group"; otherwise its emit-no-code rule is never checked
```

Restored: **0 FAIL.**

---

## `check_non_reportable_terminals` / new `is_behaviour_exclusion_object()` — the `behaviour_exclusion` false-FAIL

**What changed.** A `behaviour_exclusion` block (contract §3, ruling D1) is, by design, a
terminal that carries a clerk-facing `reason` and emits no code — the same documented shape
as `non_reportable: true` and `refer_group`, for the case where a real WHO entity's ICD-O-3.2
behaviour sits outside what the group admits. `check_non_reportable_terminals` had no
predicate recognising it, so its own `reason` (nested one level down, inside the
`behaviour_exclusion` object itself) read as a terminal that forgot to declare its
destination. **Fixed by adding `is_behaviour_exclusion_object()`**, identified the same
deliberately narrow way as the file's other shape predicates (`is_nos_fallback_object()`,
`is_provisional_pending_object()`, `is_diversion_criterion_object()`,
`is_grade_resolution_leaf()`): the key it hangs off (`where` ends in `"behaviour_exclusion"`)
AND its shape (`icdo_code` present) — and wiring the new predicate into the near-miss loop
alongside the others. This cannot mask a real code-less terminal: a branch carrying BOTH
`behaviour_exclusion` and `morphology_code` is already its own FAIL under
`check_behaviour_exclusion()`'s pre-existing rule 4 (control 1c proves that rule is still
live).

### Control 1c — a `behaviour_exclusion` branch that ALSO carries `morphology_code` still FAILs

`op_medulloepithelioma options[2]` (a real `behaviour_exclusion`, the benign
"Medulloepithelioma, benign" 9501/0 case) was given `morphology_code: "9501"` alongside it
in memory. Expected **FAIL** (from `check_behaviour_exclusion`, the check that owns this
rule), got **FAIL**; `check_non_reportable_terminals` correctly stays silent on the same
mutation, because the field it inspects for a destination lives on the OUTER option and
was never in its scope:

```
FAIL  node op_medulloepithelioma (options[2]) behaviour_exclusion: this branch ALSO carries
      morphology_code '9501'. behaviour_exclusion and morphology_code are mutually exclusive
      destinations — app.js's advance() checks morphology_code first, so this exclusion would never
      fire at runtime (contract §3, §8 rule 1)
```

Restored: **0 FAIL** on both checks.

---

## `check_group4_topography_map` (RULE 5) — the whole-registry sweep

**What changed.** RULE 5 generated every `C00.0`–`C80.9` slot and swept it against Layer 1's
REDCap topography option list — the whole REGISTRY's topography universe (every code any
group can carry), not Group IV's. `C50.x` breast, `C34.x` lung, `C61.9` prostate and 289
others came back "resolve to NO tree" — real, existing codes that no Group IV tree was ever
supposed to claim. **Fixed in two parts**, both read mechanically from
`data/shared/topography_codes.json` rather than hand-transcribed, for the same reason
`GROUP3_TREE_TOPOGRAPHY` has no Group IV analogue:

1. The **positive** sweep universe is now the 34 codes whose `topography_lookup` entry
   names group 4 in `candidate_groups` (`_group4_candidate_topography()`), checked TOTAL
   and DISJOINT exactly as before — just over the right 34, not the wrong ~330.
2. A **new assertion**: `presentation_router.json`'s `groups["4"].tree_routing.default`
   must exist and must name a `tree_id` this file actually declares — the mechanism
   `app.js`'s own `routedTree()` requires at runtime for "everything else Group IV can
   carry" (contract §5), now checked at build time instead of discovered by a clerk.
3. A **new validity assertion**, incidental to fixing the universe but implied by "every
   code claimed by a tree exists in `topography_codes.json`": a tree declaring a code
   absent from the full `topography_lookup` (a typo, not merely outside Group IV's 34)
   still FAILs.

### Control 2a — a topography claimed by two Group IV trees still FAILs (disjoint)

`C74.0` (already `g4_sympathoadrenal`'s) added in memory to `g4_head_neck_paraganglia`'s
declared topography. Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 5 — topography C74.0 resolves to 2 trees (g4_head_neck_paraganglia, g4_sympathoadrenal).
      The map must be disjoint: a duplicate does not fail, it silently picks whichever row the
      engine reads first — which is not a decision anybody made (contract §5, §8 rule 5)
```

Restored: **0 FAIL.**

### Control 2b — a tree claiming a code absent from `topography_codes.json` still FAILs

`C99.9` (not a real ICD-O-3 topography code at all) added in memory to
`g4_other_peripheral`'s declared topography. Expected **FAIL**, got **FAIL**:

```
FAIL  RULE 5 — tree(s) g4_other_peripheral declare topography C99.9, which is not in
      data/shared/topography_codes.json at all — a case can never actually carry it, so the code
      that would route it there is untested and probably wrong (contract §5, §8 rule 5)
```

Restored: **0 FAIL.**

### Control 2c — a group with neither full coverage nor a declared default still FAILs

Both mutated at once, in memory / in the throwaway repo copy described under Method:
`g4_head_neck_paraganglia`'s declared topography reduced from `["C75.4", "C75.5", "C30.1"]`
to `["C30.1"]` (a coverage gap), AND `presentation_router.json`'s
`groups["4"].tree_routing.default` deleted. Expected **two independent FAILs**, got both:

```
FAIL  RULE 5 — 2 topography code(s) resolve to NO tree: C75.4, C75.5. A case at one of these reaches
      the router, finds no handoff and dead-ends (contract §5, §8 rule 5)
FAIL  RULE 5 — presentation_router.json groups["4"].tree_routing declares no usable 'default'. Group
      IV's trees claim only 34 of the topography codes it can carry (contract §5: "C00.0-C80.9 for
      fourteen of its eighteen codes") — without a declared catch-all, a case whose topography is not
      one of those 34 reaches the router, finds no handoff and dead-ends, exactly as app.js's own
      routedTree() refuses to run without one (contract §5, §8 rule 5)
```

Restored (pristine data, real repo): **0 FAIL** — the same OK line quoted in the false-FAIL
control above.

---

## `check_group4_absent_codes` (RULE 3, `8683`) and `check_group4_not_a_group_code` (RULE 8, `9364`) — the clerk-facing-prose false-FAIL

**What changed.** Both rules' shared scanner, `_scan_group4_banned_code()`, treated a banned
code appearing in ANY clerk-facing text field (`reason`, `hint`, `label`, …) as a FAIL, on
the reasoning that a code the clerk can read is a code that gets entered. But neither
contract §0.2 (`8683`) nor §2.4/ruling D4 (`9364`) bans the code from PROSE — each rule's own
text says the code must not appear as a `morphology_code` (RULE 3 also: `nos_fallback_code`
or an alias target), and both codes are real, valid ICD-O-3.2 codes this group legitimately
talks ABOUT: `9364` is exactly what a `refer_group` branch's `reason` should name, because
Group IV's own pPNET aliases refer OUT to Group VIII/IX and the clerk needs to be told what
they will find there. Group 3 already sets this precedent, naming its own referral targets'
codes in `refer_group` `reason` text. **Fixed by making a clerk-facing-text hit a WARN
instead of a FAIL** — recorded, reviewable, never blocking the build — while a hit in an
actual EMITTING field (`morphology_code`, and for RULE 3 also `nos_fallback_code`/alias
target) is still an unconditional FAIL. This is deliberately narrower than
`check_group3_absent_codes()` (RULE 7), which still FAILs clerk-facing text and is
UNCHANGED: RULE 7's codes do not exist in ICD-O-3.2 at all, so naming one in prose can only
be a mistake, where `8683`/`9364` are real codes with a real, correct reason to be named.

### Control 3a — `9364` as a `morphology_code` still FAILs (RULE 8)

`op_medulloepithelioma options[0].morphology_code` set to `"9364"` in memory. Expected
**FAIL**, got **FAIL** (alongside the pre-existing, unaffected author-facing-text WARNs):

```
FAIL  RULE 8 — group_04_dt.json.decision_trees[3].nodes[3].options[0].morphology_code carries code
      9364. ICD-O-3.2 moved Ewing sarcoma to 9364/3 and made it the peripheral neuroectodermal
      tumour / pPNET code too (ruling D4); Group IV's pPNET aliases refer OUT to Group VIII/IX rather
      than emitting it here (contract §2.4, §8 rule 8)
```

Restored: **0 FAIL** — `OK RULE 8 — 9364 appears nowhere as a morphology_code in
group_04_dt.json (contract §2.4, §8 rule 8)`.

### Control 3b — `8683` as a `morphology_code` still FAILs (RULE 3)

`op_medulloepithelioma options[1].morphology_code` set to `"8683"` in memory. Expected
**FAIL**, got **FAIL**:

```
FAIL  RULE 3 — group_04_dt.json.decision_trees[3].nodes[3].options[1].morphology_code carries code
      8683. ICD-O-3.2 carries 8683 only at /0 (Gangliocytic paraganglioma); ICCC-3 Group IV admits
      behaviour 3 only, so there is no Group IV entry for it (contract §0.2, §8 rule 3)
```

Restored: **0 FAIL** — `OK RULE 3 — 8683 appears nowhere as a morphology_code, a
nos_fallback_code or an alias target in group_04_dt.json or its alias file (contract §0.2,
§8 rule 3)`.

### Control 3c (bonus) — `8683` named in a clerk-facing `reason` is now WARN, not FAIL

The real file only ever exercised this WARN path for RULE 8/`9364` (three occurrences, all
in `nodes[6]`'s `hint`/`reason`, all now WARN — see the false-FAIL control above). To prove
the identical treatment applied to RULE 3/`8683` actually fires, `"(see also 8683, which
this group does not code)"` was appended in memory to `op_medulloepithelioma
options[0].reason`. Expected **0 FAIL, 1 new WARN**, got exactly that:

```
WARN  RULE 3 — group_04_dt.json.decision_trees[3].nodes[3].options[0].reason prints 8683 in text a
      clerk reads. That is fine and expected — RULE 3 bans 8683 only as a morphology_code, a
      nos_fallback_code or an alias target, never in prose, and naming the destination code in a
      `reason`/`hint` is how a referral or an exclusion tells the clerk what to expect (contract
      §0.2, §8 rule 3)
OK    RULE 3 — 8683 appears nowhere as a morphology_code, a nos_fallback_code or an alias target in
      group_04_dt.json or its alias file (contract §0.2, §8 rule 3)
```

Restored: **0 FAIL**, and this WARN is gone.

---

## Regression — Groups 1, 2 and 3 do not regress

Two of the three fixes touch shared, all-group code paths
(`is_nos_fallback_object()`/`is_behaviour_exclusion_object()` inside
`check_non_reportable_terminals()`, which runs for every group's file). Verified by running
the full `python3 build/build_database.py` against the real repo **before** the fix
(`git stash` on `build/build_database.py` alone, leaving every data file untouched) and
**after**, and diffing the two complete outputs line for line: **the `-- B.
data/database/group_01_dt.json` through `group_03_dt.json` sections are byte-identical**,
every difference is confined to `group_04_dt.json`'s own section (the 11 FAILs this task
was scoped to clear) and the run summary. `is_behaviour_exclusion_object()` and the RULE
5/8/3 changes are additionally scoped (`if ctx.group != GROUP4: return []`, or bound to
fields `_scan_group4_banned_code()` already only ever ran for Group 4), so they are a
structural no-op on Groups 1–3 regardless — the byte-identical diff confirms it rather than
assuming it.

## FAIL count

Before this task's three fixes (data agent's four defects already committed; only this
task's three bugs remaining): **11 FAIL** — 7 from Bug 1 (`nos_fallback`/
`behaviour_exclusion`), 1 from Bug 2 (RULE 5, naming 292 topography codes), 3 from Bug 3
(RULE 8). After: **0 FAIL**, `BUILD PASSED`, 243 checks run. Every FAIL this task was told
NOT to touch (the four "NOT YOURS" data defects — `adaptr_descriptive`/`roman` (11),
bare-string `nos_fallback` (2), `test_result_states` closed vocabulary (2),
`provisional_pending` on a codeless branch (3)) was already cleared by the data agent's own
commit (`798a3ec Fix four Group IV data defects in group_04_dt.json`) before this task's
fixes were even written, and is confirmed absent from the final 0-FAIL, 243-check run.

---

# `check_ihc_checklist_renders_a_control` — a new, cross-group check (2026-09-18)

**What it catches.** `hn_ihc_checklist` and `sn_ihc_checklist` (Group 4) were driven in a
browser and rendered a question, a hint and a Continue button — and nothing to answer.
`branch_sequence.order` was empty (their `resolution_logic[]` keys off captured state
variables, not marker tokens, so `induce_flow.py` induces nothing to ask) and neither node
carried a `test_result_states` block. `app.js`'s `nodeControl()` (~line 615) routes every
`ihc_checklist` carrying a `branch_sequence` to `markerFlow()`, which asks one marker at a
time strictly from `branch_sequence.order` (`nextMarker()`, ~line 846) and never reads
`marker_groups[]`. `dispatchNode()` (~line 613) separately prepends `stateSelectors()`,
which renders one set of buttons per `test_result_states` block (`stateBlocks()`, ~line
643) — the only other control an `ihc_checklist` can show. Empty `order` and no
`test_result_states` together mean neither renderer produces a single input.

Neither `build/build_database.py` nor `build/induce_flow.py` caught it before this check:
`induce_flow.py` only proves every rule in `resolution_logic[]` has a *witness* — an answer
vector that fires it — and a `when`-keyed rule keying off a captured variable has a witness
regardless of whether anything in the UI can ever set that variable. `check_flow_charts()`
(this file, above `check_ihc_checklist_renders_a_control`) already tolerates an empty
`branch_sequence.order` as "legitimate" whenever the node's rules read no marker tokens, on
the theory that `test_result_states` selectors are the flow chart in that case — but it
never actually checks that a `test_result_states` block exists. Both defects passed every
existing check clean; the new check is the first one that looks at the RENDERED CONTROL
rather than at the rule logic behind it.

**The rule.** A non-empty `branch_sequence.order`, OR a non-empty `test_result_states` —
one or the other, not both required. `marker_groups[]` alone can never satisfy it:
`markerFlow()` is the renderer an `ihc_checklist` with a `branch_sequence` is routed to, and
it does not read `marker_groups[]` at all (confirmed by reading `app.js` directly, not
inferred from the schema) — `marker_groups[]` only feeds `check_marker_tokens_declared`,
`check_marker_names_verbatim`, and `induce_flow.py`'s own marker universe.

This check is registered unconditionally (`report.run(check_ihc_checklist_renders_a_control,
ctx)`, immediately after `check_flow_charts`) and runs on every group's file, not just
Group 4.

**The Group 3 exemption.** Group 3 — already merged to `main`, out of scope for this
branch's data to touch — has the identical defect on two of its own nodes:
`pf_mb_molecular_gate` and `mn_grade_assembly`. A blanket `if ctx.group == GROUP4` guard
would have hidden that Group 3 needs its own fix; instead `GROUP3_UNANSWERABLE_IHC_EXEMPTION`
names the two node IDs explicitly, dated, and downgrades ONLY them to WARN when
`ctx.group == GROUP3`. Every other unanswerable `ihc_checklist`, in any group, including
any OTHER Group 3 node, still FAILs. The exemption carries its own collapse assertion: on
every Group 3 run it re-checks each named node, and FAILs (loudly, on its own, independent
of the main sweep) if a named node no longer has the defect — so a fix landing in Group 3
cannot leave a stale, silently-passing exemption behind. `docs/TODO.md` §7 records the
Group 3 defect and what closing it takes.

## Method

Like the "Group IV validator false-FAILs" section immediately above, `check_
ihc_checklist_renders_a_control` is exercised directly against a hand-built `DTContext`
(`build_database.DTContext`, imported the way a unit test would), never through
`run_build()`/`main()`. Controls 1, 2, 3 and 3b use small synthetic node dicts — this check
needs nothing from Layer 1, `redcap_options`, or any other file, so a synthetic node is a
cleaner, more exact control than a fixture repo would be. Controls 4 and 5 use synthetic
copies of the two real Group 3 node IDs (never the real file — `data/database/
group_03_dt.json` is not opened for writing anywhere in this harness). The two "restore"
runs at the end load the REAL `group_04_dt.json` and `group_03_dt.json` read-only and
confirm the check's verdict on unmodified data. The harness is `nc_harness.py`, kept in the
session scratchpad, not the repo. `git status` after every run in this section shows only
`build/build_database.py` and `data/database/group_04_dt.json` as modified — both
deliverables of this task, neither a control artefact.

### Control 1 — non-empty `branch_sequence.order`, no `test_result_states` — PASSES

A synthetic node (`order: ["CD99"]`, a `positive`-keyed rule, no `test_result_states`).
Expected **pass**, got:

```
OK    1 ihc_checklist node(s) all render at least one input control — a non-empty branch_sequence.order or test_result_states (contract §3.4)
```

### Control 2 — empty `order`, `test_result_states` present — PASSES

A synthetic node (`order: []`, a `when`-keyed rule, one `test_result_states` block).
Expected **pass**, got:

```
OK    1 ihc_checklist node(s) all render at least one input control — a non-empty branch_sequence.order or test_result_states (contract §3.4)
```

### Control 3 — neither — FAILS, exact message

A synthetic node (`order: []`, a `when`-keyed rule, no `test_result_states`) — the exact
shape `hn_ihc_checklist`/`sn_ihc_checklist` shipped with. Expected **FAIL**, got:

```
FAIL  node ctrl_c is an ihc_checklist with an empty branch_sequence.order and no test_result_states — app.js's markerFlow() asks only from branch_sequence.order and never reads marker_groups[], so this node renders a question, a hint and a Continue button with nothing to answer (contract §3.4; app.js nodeControl()/markerFlow())
```

### Control 3b — no `branch_sequence` key at all — FAILS the same way (defensive-null variant)

A synthetic node with no `branch_sequence` key whatsoever (pre-`induce_flow.py` state, or a
hand-authored node nobody has run the inducer over yet). Expected **FAIL**, got:

```
FAIL  node ctrl_c2 is an ihc_checklist with an empty branch_sequence.order and no test_result_states — app.js's markerFlow() asks only from branch_sequence.order and never reads marker_groups[], so this node renders a question, a hint and a Continue button with nothing to answer (contract §3.4; app.js nodeControl()/markerFlow())
```

Confirms `bs.get("order") if isinstance(bs, dict) else None` degrades safely instead of
raising `AttributeError` on `None.get(...)`.

### Control 4 — the Group 3 exemption produces WARN, not FAIL

Synthetic copies of both named nodes, `ctx.group = 3`, both still carrying the defect
(empty `order`, no `test_result_states`, exactly as the real file has them). Expected **WARN
on both, FAIL on neither**, got:

```
WARN  node mn_grade_assembly is an ihc_checklist with an empty branch_sequence.order and no test_result_states — app.js's markerFlow() asks only from branch_sequence.order and never reads marker_groups[], so this node renders a question, a hint and a Continue button with nothing to answer (contract §3.4; app.js nodeControl()/markerFlow()) — known Group 3 defect (pf_mb_molecular_gate, mn_grade_assembly), tracked in docs/TODO.md, out of scope for this branch
WARN  node pf_mb_molecular_gate is an ihc_checklist with an empty branch_sequence.order and no test_result_states — app.js's markerFlow() asks only from branch_sequence.order and never reads marker_groups[], so this node renders a question, a hint and a Continue button with nothing to answer (contract §3.4; app.js nodeControl()/markerFlow()) — known Group 3 defect (pf_mb_molecular_gate, mn_grade_assembly), tracked in docs/TODO.md, out of scope for this branch
```

Confirmed against the REAL, unmodified `group_03_dt.json` too (loaded read-only): identical
two WARNs, plus `OK 29 of 31 ihc_checklist node(s) render at least one input control … 2
exempted (see WARN above)` for the other 29 Group 3 checklist nodes that do not have the
defect.

**Correction, 18 September 2026 (review of commit 65444ab).** The OK line originally read
`OK 31 ihc_checklist node(s) all render at least one input control` — FALSE: it counted every
`ihc_checklist` node in the file (`checked`), not the ones that actually render a control
(`rendered`), so on a file with any WARN it claimed more nodes were answerable than the WARN
lines immediately above it said were. A summary that contradicts the findings above it is the
exact failure mode this check exists to prevent. Fixed by tracking `rendered` separately from
`checked` and, whenever `checked != rendered` (i.e. the check raised at least one WARN and no
FAIL), printing `"%d of %d … %d exempted (see WARN above)"` instead of the unconditional
`"all render"` line. Control, before/after, on the real unmodified `group_03_dt.json`:

```
BEFORE (defect): OK    31 ihc_checklist node(s) all render at least one input control — a non-empty branch_sequence.order or test_result_states (contract §3.4)
AFTER  (fixed):  OK    29 of 31 ihc_checklist node(s) render at least one input control — a non-empty branch_sequence.order or test_result_states (contract §3.4); 2 exempted (see WARN above)
```

A second, synthetic control proves the branch generalises past the specific 29/31 numbers:
three `ihc_checklist` nodes (two healthy, one named `pf_mb_molecular_gate` and left broken,
`ctx.group = 3` so it is exempted rather than failed) produce:

```
WARN  node pf_mb_molecular_gate is an ihc_checklist with an empty branch_sequence.order and no test_result_states — app.js's markerFlow() asks only from branch_sequence.order and never reads marker_groups[], so this node renders a question, a hint and a Continue button with nothing to answer (contract §3.4; app.js nodeControl()/markerFlow()) — known Group 3 defect (pf_mb_molecular_gate, mn_grade_assembly), tracked in docs/TODO.md, out of scope for this branch
OK    2 of 3 ihc_checklist node(s) render at least one input control — a non-empty branch_sequence.order or test_result_states (contract §3.4); 1 exempted (see WARN above)
```

The all-OK case (no WARN, no FAIL) is unchanged — Groups 1, 2 and 4 above still print the
original `"%d ihc_checklist node(s) all render…"` sentence, because there `checked == rendered`
and the unqualified claim is true.

### Control 5 — the exemption's own collapse test: one named node repaired

Same fixture as Control 4, except `pf_mb_molecular_gate` is given a `test_result_states`
block in memory (`mn_grade_assembly` left broken). Expected **FAIL, naming
`pf_mb_molecular_gate`, saying to delete it from the exemption** (and `mn_grade_assembly`
still WARN, since it is still genuinely broken), got:

```
WARN  node mn_grade_assembly is an ihc_checklist with an empty branch_sequence.order and no test_result_states — app.js's markerFlow() asks only from branch_sequence.order and never reads marker_groups[], so this node renders a question, a hint and a Continue button with nothing to answer (contract §3.4; app.js nodeControl()/markerFlow()) — known Group 3 defect (pf_mb_molecular_gate, mn_grade_assembly), tracked in docs/TODO.md, out of scope for this branch
FAIL  GROUP3_UNANSWERABLE_IHC_EXEMPTION names pf_mb_molecular_gate, which now renders a control (branch_sequence.order or test_result_states is no longer empty) — the Group 3 defect this exemption covers for pf_mb_molecular_gate is fixed. DELETE pf_mb_molecular_gate from GROUP3_UNANSWERABLE_IHC_EXEMPTION in build/build_database.py
```

### Control 5b — both named nodes repaired: the exemption is fully stale

Same fixture, both `pf_mb_molecular_gate` and `mn_grade_assembly` given a fix (a
`test_result_states` block on the first, a non-empty `order` on the second). Expected **two
independent FAILs, one per node, no WARN**, got:

```
FAIL  GROUP3_UNANSWERABLE_IHC_EXEMPTION names mn_grade_assembly, which now renders a control (branch_sequence.order or test_result_states is no longer empty) — the Group 3 defect this exemption covers for mn_grade_assembly is fixed. DELETE mn_grade_assembly from GROUP3_UNANSWERABLE_IHC_EXEMPTION in build/build_database.py
FAIL  GROUP3_UNANSWERABLE_IHC_EXEMPTION names pf_mb_molecular_gate, which now renders a control (branch_sequence.order or test_result_states is no longer empty) — the Group 3 defect this exemption covers for pf_mb_molecular_gate is fixed. DELETE pf_mb_molecular_gate from GROUP3_UNANSWERABLE_IHC_EXEMPTION in build/build_database.py
```

Restored (real files, unmodified, both controls above re-run against them): the real
`group_03_dt.json` never trips this collapse assertion — both named nodes still have the
defect on disk — and the real `group_04_dt.json` shows `OK 4 ihc_checklist node(s) all
render at least one input control` with no FAIL and no WARN.

## Full-build confirmation (real repo, not the harness)

Before Deliverable 1's fix, `hn_ihc_checklist` and `sn_ihc_checklist` had no
`test_result_states` at all; before Deliverable 2 the new check did not exist, so nothing
in `python3 build/build_database.py`'s output ever named the defect. After both:

* `python3 build/induce_flow.py` — `group_04_dt.json 4 checklist nodes OK`, all four
  (`op_ihc_cd99`, `sa_ihc_checklist`, `hn_ihc_checklist`, `sn_ihc_checklist`) proven to have
  a witness for every rule; overall `Every rule in every checklist has a witness. Flow
  charts written.`
* `python3 build/build_database.py`, before registering the new check (Deliverable 1
  already applied): **243 checks run, OK 173, WARN 49, FAIL 0, BUILD PASSED.**
* Same command, after registering `check_ihc_checklist_renders_a_control`: **247 checks
  run, OK 177, WARN 51, FAIL 0, BUILD PASSED** — 4 more checks run (one per group's file),
  2 more WARN (`pf_mb_molecular_gate`, `mn_grade_assembly`, Group 3 only), 4 more OK lines
  (one per group, each reporting every `ihc_checklist` node in that file renders a
  control), 0 new FAIL.
* `git diff --quiet main -- data/database/group_01_dt.json` — exit 0, identical.
* `git diff --quiet main -- data/database/group_02_dt.json` — exit 0, identical.
* `git diff --quiet main -- data/database/group_03_dt.json` — exit 0, identical.

---

# `check_no_internal_identifier_leaks` — review of commit 65444ab (2026-09-18)

An independent review of `65444ab` (browser-drive plus an independent negative-control
reproduction) found two defects in that commit's own work, on top of the OK-line defect
already corrected above:

1. **A JSON field name printed in text a clerk reads.** Twelve strings this commit added to
   `hn_ihc_checklist`/`sn_ihc_checklist` (`reason` and `provisional_pending.reason`, both
   rendered — `orow('Provisional', …)`, app.js ~1836) contained the literal substring
   `refer_group 11`, e.g. "...route the case to the neuroendocrine/carcinoma pathway
   (refer_group 11) instead of leaving it here." A clerk has no way to know what
   `refer_group` is; it names nothing they can see anywhere in the interface.
2. **A bare node id printed in text a clerk reads.** Nine occurrences, across seven strings,
   of a real `node_id` this file declares — e.g. "...move the case on to grading and staging
   at `sn_grading_staging`." Two were this commit's own (`hn_ihc_checklist`/
   `sn_ihc_checklist` `resolution_logic` `reason` text); the other five were pre-existing,
   written by the tree-authoring agents, and equally invisible to a clerk (a node id is not
   displayed anywhere in the rendered UI).

Both are the SAME underlying defect — an internal identifier crossing into clerk-facing
prose — so one check, `check_no_internal_identifier_leaks`, covers both: a fixed list of
eleven schema-field-name tokens (`INTERNAL_IDENTIFIER_TOKENS`), and a per-file, dynamically
built set of every declared `node_id`/`tree_id`, both scanned as whole words against every
key in `CLERK_FACING_PROSE_KEYS` — a list built by reading `app.js` directly (every call site
cited in the constant's own comment), not guessed from the schema.

## Data fix

All twelve `refer_group 11` occurrences rewritten to name the destination in words, matching
the house style already committed in `group_02_dt.json` and `group_03_dt.json` (Roman
numeral plus the group's own name in parentheses — see `check_no_internal_identifier_leaks`'s
sibling checks for precedent): `"...into ICCC-3 Group XI (other malignant epithelial
neoplasms and malignant melanomas)..."`. All nine node-id occurrences rewritten to name the
step in words (its own `step_label`/`question`) or drop the pointer where the sentence works
without it — for example "...a completed panel would allow a site-specific code to be
assigned once the site is documented" (`hn_site_resolution`'s own step is literally "Site
sets the code"), and "...move the case on to grading and staging" with the bare
`at sn_grading_staging` dropped, since the preceding words already say what that step is.

## Method

Same as the "Group IV validator false-FAILs" and `check_ihc_checklist_renders_a_control`
sections above: `build_database` imported directly, `DTContext` built from an in-memory
`copy.deepcopy()` of the loaded real file, never through `run_build()`. A companion
standalone scan script (not the check itself — a second, independent implementation of the
same idea) was run first against all four groups' real, unmodified files, to find every real
hit before any fix and to confirm Groups 1-3 are clean, exactly as the reviewer's own
independent scan reported. The harness is `nc_harness2.py`, kept in the session scratchpad.

## The false-FAIL control (real files, unmodified, before any fix in this section)

Independent scan, all four groups, `CLERK_FACING_PROSE_KEYS` × (`INTERNAL_IDENTIFIER_TOKENS`
∪ every declared `node_id`/`tree_id`):

```
group_01_dt.json -> internal-identifier-token hits: 0   node/tree id leak hits: 0
group_02_dt.json -> internal-identifier-token hits: 0   node/tree id leak hits: 0
group_03_dt.json -> internal-identifier-token hits: 0   node/tree id leak hits: 0
group_04_dt.json -> internal-identifier-token hits: 0   node/tree id leak hits: 9
```

Groups 1-3 at zero, confirmed independently rather than trusted from the reviewer's report.
The nine Group 4 hits are exactly the nine cited above; fixed as described under "Data fix".
After the fix, the same scan and the real check both report zero across all four groups
(see "Full-build confirmation" below).

**Boundary control — `coding_note` is correctly NOT scanned.** `group_04_dt.json` carries 14
occurrences of an internal-identifier token or a declared node id inside `coding_note`
(author-facing per memory `uccf-lookup-tool-clerk-facing-text` — never rendered, e.g.
`decision_trees[1].nodes[1].options[1].coding_note`: "Do not code 8692/8690/8691/8693/8682/
8680 from a referral, however specific its wording. hn_site_resolution..."). None of the 14
is reported by `check_no_internal_identifier_leaks`, because `coding_note`/
`topography_routing_note` are excluded from `CLERK_FACING_PROSE_KEYS` by construction. A
check that scanned every string field regardless of key would false-FAIL on all 14 of these
legitimate author notes; confirming they do NOT fire is as important as confirming the real
leaks DO.

### Control A — a JSON field name planted back into a `reason` — FAILS, exact message

`(refer_group 11)` appended in memory to `hn_ihc_checklist`'s `keratin_status: not_done`
branch `reason` (the exact defect this section fixes, reintroduced to prove the check would
have caught it). Expected **FAIL**, got:

```
FAIL  node hn_ihc_checklist (resolution_logic[3]).reason contains the internal identifier 'refer_group' — a clerk cannot see JSON field names anywhere in the interface, so this leaks the engine's own vocabulary instead of a clinical fact: 'Keratin has not been performed, so a well-differentiated neuroendocrine tumour cannot yet be excluded. An unread keratin is not a negative one: keratin-negative is what confirms paraganglioma, so this case cannot be treated as though it had cleared that test. 8680/3 Paraganglioma, NOS is recorded at the family level (basis 7) while the stain is outstanding; a keratin-positive result would move this case out of Group IV entirely and into ICCC-3 Group XI (other malignant epithelial neoplasms and malignant melanomas), not to a more specific code here. (refer_group 11)'
```

Restored (real, unmodified `group_04_dt.json`): **0 FAIL** on this check.

### Control B — a bare node id planted into a `reason` — FAILS, exact message

`" See sn_grading_staging for details."` appended in memory to `sn_ihc_checklist`'s
`pankeratin_status: not_done` branch `reason`. Expected **FAIL**, got:

```
FAIL  node sn_ihc_checklist (resolution_logic[3]).reason contains 'sn_grading_staging', a node_id/tree_id this file declares — a clerk cannot see node or tree ids anywhere in the interface. Name the step in words (its own step_label/question), or drop the pointer where the sentence works without it: 'Pankeratin has not been performed, so the carcinoma differential (olfactory carcinoma, IDH2-mutant sinonasal carcinoma) cannot yet be excluded. An unread pankeratin is not a negative one: pankeratin-negative is what confirms olfactory neuroblastoma over the carcinoma differential, so this case cannot be treated as though it had cleared that test. 9522/3 Olfactory neuroblastoma is recorded at the family level (basis 7) while the stain is outstanding; a pankeratin-positive result would move this case out of Group IV entirely and into ICCC-3 Group XI (other malignant epithelial neoplasms and malignant melanomas), not to a more specific code here. See sn_grading_staging for details.'
```

Restored: **0 FAIL** on this check.

## Full-build confirmation (real repo)

* `python3 build/induce_flow.py` — unchanged, clean, all four Group 4 checklist nodes OK.
* `python3 build/build_database.py`, before this section's two fixes (Deliverable 1/2 of the
  original task already applied): **247 checks run, OK 177, WARN 51, FAIL 0, BUILD PASSED**,
  but the OK line at Group 3 read the false `"31 ... all render"` sentence and Group 4 still
  carried the twelve `refer_group 11` / nine node-id leaks (not yet checked for, so not yet
  counted as FAIL).
* After both fixes and registering `check_no_internal_identifier_leaks`: **251 checks run, OK
  181, WARN 51, FAIL 0, BUILD PASSED** — 4 more checks run (one per group), each reporting
  `OK no clerk-facing string names an internal schema field (11 checked) or a declared
  node_id/tree_id (N checked)`, 0 new FAIL, 0 new WARN, the Group 3 OK line now reads
  `29 of 31 … 2 exempted (see WARN above)`.
* `git diff --quiet main -- data/database/group_01_dt.json` — exit 0, identical.
* `git diff --quiet main -- data/database/group_02_dt.json` — exit 0, identical.
* `git diff --quiet main -- data/database/group_03_dt.json` — exit 0, identical.

---

# `check_override_affordance` — "Override this code" on terminals that emit no code (2026-09-18)

## The defect

`outActions()` (app.js) rendered the terminal action bar unconditionally, on every
terminal:

```js
function outActions() {
  return '<div class="out__actions"><button class="btn" data-act="restart">Start new case</button>' +
    '<button class="btn btn--ghost" data-act="override">Override this code</button></div>';
}
```

Three of the tool's four terminal kinds emit no morphology code at all — a cross-group
referral (`refer()`: "CODE HERE — None. Emitting a code from this group would put the case
in the wrong ICCC-3 group"), a Group 4 behaviour exclusion (`excludeBehaviour()`:
"MORPHOLOGY — No code emitted here") and a non-reportable exclusion (`exclude()`). On all
three the button offered to override a code that does not exist, and the handler
(`case 'override':`) validates the typed code with `entryFor(code)`, which resolves only
against THIS group's `morphology_entries`. So the single thing the button could do on a
screen that had just said the case belongs elsewhere was force it into this group.

Driven in a real browser before any fix — Group XI referral terminal out of
`hn_ihc_checklist` (guided entry → Mass / swelling → Soft tissue → Carotid body and other
paraganglia → Carotid body → Tissue with a definitive pathology report → `keratin status:
positive` → Continue), with `window.prompt` stubbed to answer `9490` because the harness
does not support it:

```
before: {referral: true, group: 11, note: "Paragangliomas are consistently keratin-negative. …"}
after : {code: "9490", name: "Ganglioneuroblastoma", upgrade: "Abstractor override: testing the defect"}
```

A cross-group referral to ICCC-3 Group XI became a Group IV code, on one click of an
affordance the terminal should never have offered. That is the exact error the terminal
exists to prevent.

## The fix, and what it keys off

`state.result.code` — the RESOLVED OUTCOME, not a flag on the branch and not the rendered
text. `finish()` is the only function in app.js that sets it, from the branch's own
`morphology_code`, and only after `entryFor()` has proved the code is real. The other
three terminal builders never set it: `refer()` builds `{referral, group, codeHint}`,
`exclude()` builds `{excluded, reason}`, `excludeBehaviour()` builds `{behaviourExcluded,
icdoCode}` — and `icdoCode` is deliberately a DIFFERENT key, because the code a benign
tumour sits at is not a code this group emitted. So `code` is the one value that separates
the terminals that emitted a code from the terminals that emitted none; it is the same
value the headline renders and the same value an override would replace; and a fifth
terminal kind added in a later group is covered without touching anything, because
anything that does not run through `finish()` carries no code.

`resultCarriesCode(r) { return !!(r && r.code); }` gates both `outActions()` (the button)
and `handleOption()`'s `case 'override'` (the action, refused BEFORE `window.prompt`, so
the clerk is never asked for a code that would be discarded). The handler guard is not
redundant with the renderer: a delegated listener acts on whatever markup carries
`data-act`, so a renderer regression or a hand-dispatched action must not be able to turn a
referral into a code from this group.

## Method

Same as the sections above: `build_database` imported directly, `DTContext` built from a
`copy.deepcopy()` of each loaded real file, never through `run_build()`. The engine half is
exercised by seeding `_APP_JS_CACHE` with a mutated copy of the real `app.js` under a
fixture key — the real `app.js` on disk is never modified by the harness. Harnesses are
`nc_override.py` / `nc_override2.py`, kept in the session scratchpad. All controls are run
against the real, unmodified `group_04_dt.json` (the only file carrying all three code-less
terminal kinds), and the two-sided controls also against `group_01_dt.json`.

## The false-FAIL control (real `app.js`, all four real files)

The check must not fire on the fixed engine, and its OK line must report real content —
both tallies — rather than asserting the rule in the abstract:

```
OK    "Override this code" is offered on exactly the terminals that emitted one: 241 coded terminal(s) keep it, 64 code-less terminal(s) suppress it (15 cross-group referral, 49 non-reportable, 0 behaviour-exclusion). app.js gates both outActions() and handleOption('override') on resultCarriesCode(state.result), and state.result.code is set only by finish()
OK    "Override this code" is offered on exactly the terminals that emitted one: 306 coded terminal(s) keep it, 77 code-less terminal(s) suppress it (14 cross-group referral, 63 non-reportable, 0 behaviour-exclusion). app.js gates both outActions() and handleOption('override') on resultCarriesCode(state.result), and state.result.code is set only by finish()
OK    "Override this code" is offered on exactly the terminals that emitted one: 629 coded terminal(s) keep it, 85 code-less terminal(s) suppress it (55 cross-group referral, 30 non-reportable, 0 behaviour-exclusion). app.js gates both outActions() and handleOption('override') on resultCarriesCode(state.result), and state.result.code is set only by finish()
OK    "Override this code" is offered on exactly the terminals that emitted one: 50 coded terminal(s) keep it, 31 code-less terminal(s) suppress it (27 cross-group referral, 1 non-reportable, 3 behaviour-exclusion). app.js gates both outActions() and handleOption('override') on resultCarriesCode(state.result), and state.result.code is set only by finish()
```

(group_01, group_02, group_03, group_04 in that order. Groups 1-3 carry referral and
non-reportable terminals but no behaviour exclusions — that field is new in Group 4 — so
they get the same fix for the same reason, which is intended.)

### Control A — `outActions()` reverted to the pre-fix unconditional version — FAILS, exact message

The defect itself, reintroduced verbatim. Expected **FAIL**, got:

```
FAIL  outActions() renders "Override this code" without `if (resultCarriesCode(state.result))` around it, so it is offered on terminals that emitted no code. In group_04_dt.json that is 31 terminal(s) — 27 cross-group referral, 1 non-reportable, 3 behaviour-exclusion — where the handler can only emit a code from THIS group: hn_clinical_alias (options[0]); hn_clinical_alias (options[1]); hn_clinical_alias (options[2]); hn_document_inventory (options[1]); and 27 more
```

Restored (real, unmodified `app.js`): **0 FAIL** on this check.

### Control B — the handler guard deleted, button gate left in place — FAILS, exact message

Proves the two halves are checked independently: a correct renderer does not excuse an
unguarded handler, because the handler is what actually emits the code.

```
FAIL  handleOption()'s `case 'override'` does not refuse on a code-less outcome — it must return early on `if (!resultCarriesCode(state.result))`, so a renderer regression or a hand-dispatched action cannot turn one of group_04_dt.json's 31 code-less terminal(s) into a code from this group: hn_clinical_alias (options[0]); hn_clinical_alias (options[1]); hn_clinical_alias (options[2]); hn_document_inventory (options[1]); and 27 more
```

Restored: **0 FAIL** on this check.

### Control C — the override button removed outright — FAILS, exact message

**This is the control proving a CODED terminal still keeps the button.** Suppressing the
affordance everywhere would silence Controls A, B and G while destroying a feature the
registrar uses on every coded case, so the check has to be two-sided: it fails on a coded
terminal that LOSES the button exactly as loudly as on a code-less one that gains it.

```
FAIL  app.js renders data-act="override" in 0 place(s); it must be rendered in exactly one, inside outActions(), so there is a single gate to hold. 50 coded terminal(s) in group_04_dt.json depend on that button and 31 code-less terminal(s) depend on its absence
FAIL  outActions() renders no override button at all, so the 50 coded terminal(s) in group_04_dt.json LOSE "Override this code" — the affordance is removed from terminals that did emit a code, not just from the ones that did not: hn_genetics (nos_fallback); hn_ihc_checklist (nos_fallback); hn_ihc_checklist (resolution_logic[2]); hn_ihc_checklist (resolution_logic[3]); and 46 more
```

Restored: **0 FAIL** on this check.

### Control G — the gate inverted, `if (!resultCarriesCode(state.result))` — FAILS, exact message

The same two-sidedness on a subtler regression: the button is still rendered exactly once,
still inside `outActions()`, still under a `resultCarriesCode` gate — only the polarity is
wrong. A check that merely looked for "a conditional" would pass this. Run against
`group_04_dt.json` and `group_01_dt.json`:

```
FAIL  outActions() guards "Override this code" on `if (!resultCarriesCode(state.result))` — the gate is INVERTED. In group_04_dt.json that offers it on all 31 code-less terminal(s), where the handler can only emit a code from THIS group, and removes it from all 50 coded terminal(s), which are the only ones that have a code to override
FAIL  outActions() guards "Override this code" on `if (!resultCarriesCode(state.result))` — the gate is INVERTED. In group_01_dt.json that offers it on all 64 code-less terminal(s), where the handler can only emit a code from THIS group, and removes it from all 241 coded terminal(s), which are the only ones that have a code to override
```

Restored: **0 FAIL** on this check.

### Control D — the gate keyed off the terminal-kind flags instead of the outcome — FAILS, exact message

`resultCarriesCode` rewritten to `return !!(r && !r.referral && !r.excluded &&
!r.behaviourExcluded);`. This is **behaviourally correct today** — it suppresses the button
on exactly the same three terminals — and the check still FAILs it, on purpose. It is a
list someone has to remember to extend, and the first terminal kind left off it gets the
affordance back silently. Keying off a flag is the defect one release later.

```
FAIL  resultCarriesCode() is keyed off the terminal-kind flag(s) referral, excluded, behaviourExcluded instead of the resolved outcome's own code — that is a list someone must remember to extend, and the first terminal kind left off it gets "Override this code" back. Test r.code, which only finish() ever sets
FAIL  resultCarriesCode() does not read the resolved outcome's code — its body must be `return !!(r && r.code);`, the value finish() sets and refer()/exclude()/excludeBehaviour() never do. Body is: return !!(r && !r.referral && !r.excluded && !r.behaviourExcluded);
```

Restored: **0 FAIL** on this check.

### Control F — the handler guard present but placed after the prompt — FAILS, exact message

The refusal has to land before the clerk is asked for a code that will be thrown away.

```
FAIL  handleOption()'s `case 'override'` tests resultCarriesCode() only AFTER window.prompt() — the clerk is asked for a code on a terminal that emits none before the refusal. Move the guard above the prompt
```

Restored: **0 FAIL** on this check.

## Browser confirmation (real DOM, real handlers, `http://localhost:8811`)

The browser pane cannot be displayed in this environment, so every step was driven through
the real DOM with `.click()` on real elements and read back from `state` and
`document.body.innerText`. `window.prompt()` is unsupported there and was stubbed for the
override probes only.

**(a) Cross-group referral — Group XI, out of `hn_ihc_checklist`.** Guided entry → Mass /
swelling → Soft tissue → Carotid body and other paraganglia → Carotid body → Tissue with a
definitive pathology report → `keratin status: positive` → Continue.

```
BELONGS TO ANOTHER GROUP
This case is a malignancy, but not one this group codes. Record it under group 11 — Other Malignant Epithelial Neoplasms and Malignant Melanomas.
CODE HERE   None. Emitting a code from this group would put the case in the wrong ICCC-3 group.
…
Start new case
```

`.out__actions` holds one button, `restart`. `document.querySelector('[data-act="override"]')`
is `null`. Before the fix this same screen ended `Start new case  Override this code`.

The hardened handler, on that same terminal, with the button injected by hand to dispatch
the action anyway:

```
promptsShown : 0
state.result : {referral: true, group: 11, …}   (unchanged — no code emitted)
state.error  : "This terminal emits no morphology code, so there is no code to override. Overriding here would emit a code from this group — which is the one thing this terminal exists to prevent."
```

**(b) Behaviour exclusion — 9490/0 ganglioneuroma, `sa_histology_subclassification` in the
`g4_sympathoadrenal` tree.** Guided entry → Mass / swelling → Soft tissue → Adrenal gland
and paraspinal sympathetic chain → Medulla of adrenal gland → Definitive histology report →
fully mature / maturing ganglioneuroma.

```
BENIGN — OUTSIDE THIS GROUP’S DECLARED BEHAVIOUR
MORPHOLOGY        No code emitted here.
ICD-O-3.2         9490/0 — Ganglioneuroma
GROUP DECLARES    Behaviour 3 only
REGISTRAR DECISION REQUIRED …
…
Start new case
```

`.out__actions` holds one button, `restart`; no `[data-act="override"]` in the DOM.

**(c) A terminal that DOES emit a code — 8680/3.** Same head-and-neck route with
`keratin status: not done`.

```
8680  Paraganglioma, NOS
Other peripheral nervous cell tumors — ICCC-3 IVb
…
Start new case      Override this code
```

`.out__actions` holds `restart` **and** `override`, unchanged from before the fix. Taking
the override on it still works end to end: two prompts shown, `state.result.code` moves to
the entered code with `upgrade: "Abstractor override: …"` and `state.error` null.

**(d) A Group 1 coded terminal, to confirm a merged group is untouched.** Guided entry →
Blood / marrow signs → Blood and bone marrow → Blood, bone marrow and haematopoietic system
→ Bone marrow → Chronic myeloid proliferation → Morphology + cytogenetics / FISH → no prior
cytotoxic therapy → Philadelphia chromosome positive → blasts under 10%:

```
9875  Chronic myelogenous leukemia, BCR/ABL positive
Chronic myeloproliferative diseases — ICCC-3 Ic
…
Start new case      Override this code
```

Both buttons present.

## Full-build confirmation (real repo)

* `python3 build/induce_flow.py` — unchanged, clean: `group_01 7 / group_02 25 /
  group_03 31 / group_04 4 checklist nodes OK`, `Every rule in every checklist has a
  witness. Flow charts written.`
* Baseline, measured by running **HEAD's** `build_database.py` against the current working
  tree (the doc's earlier 251 / OK 181 / WARN 51 had already drifted to WARN 53 through
  another agent's concurrent work before this branch touched anything): **251 checks run,
  OK 183, NOTE 36, WARN 53, FAIL 0, BUILD PASSED.**
* After the app.js fix and registering `check_override_affordance`: **255 checks run, OK
  187, NOTE 36, WARN 53, FAIL 0, BUILD PASSED** — 4 more checks run (one per group's
  file), 4 more OK lines, 0 new WARN, 0 new FAIL.
* `git diff --quiet main -- data/database/group_01_dt.json` — exit 0, identical.
* `git diff --quiet main -- data/database/group_02_dt.json` — exit 0, identical.
* `git diff --quiet main -- data/database/group_03_dt.json` — exit 0, identical.
* No `group_0*_dt.json` was edited by this branch; the fix is entirely in `app.js` and the
  check entirely in `build/build_database.py`.

---

# Group V checks — negative controls

**22 September 2026, on the `group-05-retinoblastoma` branch.** Evidence that the six checks
added for Group 5, plus the generalisation of `check_behaviour_exclusion()`, catch what they
claim to. Method unchanged: break the data deliberately, confirm the check FAILs, restore,
confirm it passes — and separately confirm none fires on correct data, because a false FAIL is
the more corrosive failure.

## The fixture

A schema-complete Group V file built **in memory** by
`scratchpad/nc5.py`, not written to `data/database/`: four morphology entries
(`9510`, `9511`, `9512`, `9513` — the generated inventory), one tree `g5_retinoblastoma`, three
nodes covering the three shapes the rules are about — a `document_inventory`, an
`imaging_pathway` carrying all seven of its required fields, and a
`histology_subclassification` whose third option is a well-formed `behaviour_exclusion` for
`9510/0 Retinocytoma`.

It is deliberately **not** `data/database/group_05_dt.json`. That file was being authored by
another agent while these controls ran, and a control that mutates the real file cannot prove
anything about a file someone else is writing.

The checks are exercised by importing `build/build_database.py` as a module and calling each
function against a `DTContext` built from the fixture, so a control exercises the check and
nothing else — no build ordering, no other group's data, no filesystem state.

## The false-FAIL control (correct data)

On the unmodified fixture, **0 FAIL**, and every one of the seven checks reports OK against
real content rather than an empty NOTE:

```
OK  1 imaging_pathway node(s): each declares insufficient_next_node and none declares options[] (rule 1)
OK  RULE 3 — every emitted code is in {9510, 9511, 9512, 9513}; 1 terminal(s) at basis 1 or 2 emit 9510 and nothing else (Visser Table 3)
OK  GROUP 5 RULE 4 — 9514 appears nowhere as a morphology_code, a nos_fallback_code or an alias target
OK  RULE 5 — imaging_sufficient is true on 9510 only
OK  RULE 6 — no ihc_checklist node; ihc_markers_required and ihc_markers_exclude null on all 4 entries
OK  RULE 7 — code_neutral_molecular true on all 4 entries
OK  1 behaviour_exclusion block(s) well formed: all six keys present, icdo_code/icdo_behaviour/icdo_term round-trip to the Preferred term
```

## The thirteen controls

All thirteen caught, none missed.

| | Control | Mutation | Caught by |
|---|---|---|---|
| **A** | `imaging_pathway` loses `insufficient_next_node` | delete the key | rule 1 |
| **B** | `imaging_pathway` gains `options[]` | add one option | rule 1 |
| **C** | **a subtype emitted at basis 2** | `rb_imaging_pathway` emits `9513` instead of `9510` | rule 3b |
| **D** | a code outside the group | an option emits `9501` | rule 3a |
| **E** | `9514` emitted as a `morphology_code` | an option emits `9514` | rule 4 |
| **F** | `imaging_sufficient` true on `9513` | flip the entry's flag | rule 5 |
| **G** | `imaging_sufficient` false on `9510` | flip the entry's flag | rule 5 |
| **H** | an `ihc_checklist` node appears | append one | rule 6 |
| **I** | `ihc_markers_required` non-null | set `["CRX"]` | rule 6 |
| **J** | `code_neutral_molecular` false | flip one entry | rule 7 |
| **K** | **`behaviour_exclusion` names an ADMITTED behaviour** | `icdo_behaviour` `"0"` → `"3"` | rule 2 |
| **L** | `behaviour_exclusion` `icdo_term` does not round-trip | `"Retinocytoma"` → `"Retinoblastoma, NOS"` | rule 2 |
| **M** | `behaviour_exclusion` also carries a `morphology_code` | add `9510` to the same branch | rule 2 |

### The three that matter most

**C — a subtype emitted at basis 2.** This is the error the whole group is most exposed to and
the one a reader would least likely notice. `9513` at basis 2 is a syntactically perfect
record that says a diffuse infiltrating retinoblastoma was established by imaging, when
diffuse retinoblastoma is the one variant with **no** calcified mass and the constellation
could not have confirmed it. Downstream it reads as a graded, enucleation-confirmed tumour for
a child whose eye was never removed. Visser 2023 Table 3 licenses `9510/3` and nothing else
without pathology, and rule 3b is that sentence made executable.

**K — the subtle clause, and the proof the generalisation landed.** A `behaviour_exclusion`
naming a behaviour the group *does* admit would **hide a code that should have been emitted**.
Before 22 September 2026 `check_behaviour_exclusion()` was hard-guarded
`if ctx.group != GROUP4: return []`, so a Group 5 block would have been authored and never
validated at all. Control K's FAIL message reads *"IS in Group **V**'s own declaration"* — the
group label and the `BEHAVIOUR_DECLARED_BY_GROUP` lookup are both resolving for group 5, which
is what proves the check now reaches the group rather than silently returning an empty list.

**A and B — the rule that found a defect it was never shown.** Run against the real repository,
rule 1 reported the three Group 3 nodes `pf_imaging_no_tissue`, `st_imaging_pathway` and
`sp_imaging_no_tissue` with 6, 4 and 4 dead options each and no `insufficient_next_node` —
matching `docs/TODO.md` §10's independently-recorded table exactly. That is a real-world
positive control nobody had to construct: the check found a known runtime crash from first
principles. It is WARN rather than FAIL outside group 5 because those three files are on
`main` and outside this branch.

## Regression evidence for Groups 1–4

The pre-change validator (`git show HEAD:build/build_database.py`) and the new one were run
over identical data from the repository root. **255 checks / 0 FAIL** against
**279 checks / 0 FAIL**. Diffing the two reports line by line, **no finding changed for any
group** — every difference is one of the new checks. Groups 1, 2 and 3's `dt.json` and alias
files, and `app.js`, are byte-identical to HEAD.

The one FAIL raised during this work was real and was fixed: adding the nine `C69` codes to
`topography_codes.json` made `C69.4` a Group 4 candidate site, and
`check_group4_topography_map` (rule 5) correctly reported it resolving to no Group 4 tree.
`C69.4` is now declared on `g4_other_peripheral`, whose `op_medulloepithelioma` node was
already the right destination — a fix to a pre-existing gap, since before this change `C69`
held `C69.9` alone and no ciliary body case could reach any group at all.

---

# Group VII checks — negative controls

**2–3 October 2026, on `claude/group-7-tumor-pathway-a88513`.** Evidence that the nine Group 7
checks, and Group 7's entry into `check_icdo32_round_trip()` and `check_behaviour_exclusion()`,
catch what they claim to. Method unchanged: break the data, confirm the check FAILs for the stated
reason, and confirm no check fires on the correct data.

## The harness

`build/negative_controls_group07.py`, committed so the controls rerun from a clean checkout:

```
ICD_LAYER1="<vault>/ICD coding" python3 build/negative_controls_group07.py
```

It loads the real `group_07_dt.json`, `aliases_group_07.json` and `presentation_router.json` into
memory, applies one mutation, writes the three into a scratch directory for the checks that read
files, runs the one check that should catch it, and requires a FAIL whose message contains the
expected text. Nothing under `data/` is written.

## The false-FAIL control (correct data)

All eleven checks report OK on the unmodified files, against real content: 92 entries and 36
emissions in the inventory; no §2A code emitted, used as a fallback or targeted by an alias; four
behaviour exclusions on Group VII stems; two `8963` terminals, each on an INI1 or SMARCA4 loss
marker; sixteen C22-only emissions, all on routes that establish the liver; three no-pathology
emissions; one imaging node with the alpha-fetoprotein question and both age diversions; four `8171`
terminals; the router agreeing with ICCC-2017; 99 of 99 name triples real in `icdo32.sqlite`; four
behaviour exclusions naming the preferred term.

## The thirty-seven controls

All caught. 4G–4I were added after the independent review of 3 October 2026.

| | Rule | Mutation |
|---|---|---|
| 1A | 1 | an entry's code fabricated, `8970` → `8971` |
| 1B | 1 | a node emits a fabricated `8176` |
| 1C | 1 | the INI1 fallback names `8999` |
| 2A | 2 | high-grade biliary intraepithelial neoplasia emitted as `8148/3` |
| 2B | 2 | the calcifying nested stromal-epithelial tumour abbreviation maps to `9013` |
| 2C | 2 | an entry's `nos_fallback_code` is `9013` |
| 3A | 3 | `group_declares` copied from Group III, `"0-1,3"` |
| 3B | 3 | a behaviour exclusion on `9131/0`, no Group VII stem |
| 3C | 3 | the bile duct adenoma exclusion names `8160/9`, not a real pair |
| 10A | 10 | `8975/3` on the option with no malignancy stated |
| 10B | 10 | `8975/1` on the malignant-or-metastatic option |
| 10C | 10 | the `8975/3` entry dropped |
| RT2 | round trip | the `8975/3` matrix entry renamed to REDCap's word order |
| 4A | 4 | the `8963` rule keyed on INI1 RETAINED |
| 4B | 4 | the small cell undifferentiated histology option codes `8970` directly |
| 4C | 4 | the `8970` rule keyed on INI1 loss |
| 4D | 4 | INI1 not done falls back to `8970` |
| 4E | 4 | every `8970` rule deleted from the INI1 step |
| 4F | 4 | the small cell undifferentiated alias maps to `8970` again |
| 4G | 4 | the `8970` rule loses its small-cell condition, so rhabdoid cells with INI1 retained reach it |
| 4H | 4 | the small cell undifferentiated option codes `8963` directly, on morphology alone |
| 4I | 4 | the diagnosed-rhabdoid-tumour option also names a small cell pattern |
| 4J | 4 | small cell undifferentiated with INI1 retained and SMARCA4 not recorded stops owing IHC |
| 4K | 4 | hepatoblastoma with rhabdoid cells, SMARCA4 not recorded, claims IHC done instead |
| 4L | 4 | the hepatoblastoma-with-rhabdoid-cells option stops saying the report diagnoses hepatoblastoma |
| 5A | 5 | the histology route stops capturing C22 |
| 5B | 5 | an `8963` rule loses its `primary_site` `when` |
| 6A | 6 | the no-tissue cholangiocarcinoma option codes `8172` |
| 6D | 6 | hepatocellular carcinoma at basis 4 with alpha-fetoprotein not raised |
| 6B | 6 | the referral note's basis-9 option coded at basis 1 |
| 6C | 6 | no tissue, `8000` at basis 4 |
| 7A | 7 | the alpha-fetoprotein question removed |
| 7B | 7 | the alpha-fetoprotein question requires "no" |
| 7C | 7 | the under-6-months diversion removed |
| 7D | 7 | `8170` marked `imaging_sufficient` |
| 7E | 7 | the hepatoblastoma imaging node codes `8170` |
| 8A | 8 | a `DNAJB1::PRKACA` finding codes `8170` |
| 8B | 8 | the fibrolamellar histology option codes `8170` |
| 8C | 8 | "not tested" fibrolamellar codes `8170` |
| 8D | 8 | every fibrolamellar branch codes `8170` |
| 9A | 9 | the router's `8963` C22 branch removed |
| 9B | 9 | the `8991` C22 branch names VIIa1 |
| 9C | 9 | the `8170` default reverted to group 11 |
| 9D | 9 | the `8000-8005` C22 branch removed |
| RT | round trip | `8970` named by REDCap's string "Hepatoblastoma" |
| BE | exclusion | the `8170/0` exclusion names its synonym, not the preferred term |
| OT1 | `check_outstanding_tests` | a value outside the diagnostic-test vocabulary |
| NH1 | `check_non_reportable_heading` | a benign heading on a branch that codes `8991` |
| NH2 | `check_non_reportable_heading` | an empty heading |
| OT2 | `check_outstanding_tests` | a rule lists IHC in both `satisfies_tests` and `outstanding_tests` |

## What the first pass found in the checks themselves

**A false FAIL on correct data, rule 8.** Clause (d) marked every node reached from an option whose
label asserts fibrolamellar carcinoma. The option "Hepatocellular carcinoma, including fibrolamellar
carcinoma" routes to the subtype node, so scirrhous `8172` failed. Clause (d) now reads only the
molecular step a fibrolamellar option routes into. Without the correct-data run this would have
reached the build as a FAIL on good data — the kind that teaches the next author to bend the data.

**A control missed, rule 9.** 9B (wrong subgroup on the `8991` branch) raised no FAIL. The ICCC
lookup returned the main group as the integer 7 and the filter compared it with the string `"VII"`,
so the expected subgroup was always empty and the subgroup comparison never ran. 9A's message showed
it too ("ICCC-2017 says group 7 ?"). Fixed; 9B is caught.

**A gap only the browser showed, rule 4.** An alias on `8970` and `8963` put "SCUD hepatoblastoma"
under "Also called" on every `8970` output, including a hepatoblastoma coded on imaging alone. No
check read the alias layer for this. Clause (e) and control 4F were added.

**A gap the first control list missed, rule 8.** "Not tested" fibrolamellar carcinoma re-pointed at
`8170` names no fibrolamellar or molecular finding in its own label, so the first two clauses could
not see it. Clause (d) and control 8C were added before the first run.

## Regression

Groups 1–6 data and alias files are byte-identical to `main`. The full build reports 0 FAIL, the
engine gate included.

## What the independent review found in the checks (3 October 2026)

**Rule 4 permitted the defect it exists to stop.** Clause (c) exempted any `8970` branch carrying the
INI1-RETAINED marker, and one histology option carried both a small cell undifferentiated pattern and a
rhabdoid diagnosis into the INI1 step, so an INI1-retained malignant rhabdoid tumour (Vokuhl 2016,
p. 927) was coded `8970`. Every control passed, because none built that case. Clause (f) now asks the
condition directly: can an `8970` rule fire for a route that does not describe a small cell
undifferentiated pattern? Control 4G breaks it.

**The fix then exposed a matcher defect.** The shared `_marker_asserted()` reads 90 characters after a
term as well as before it, so the new label "A small cell undifferentiated (blastemal) pattern
predominates, with no rhabdoid cells described" read as not asserting the small cell pattern. The
correct-data run reported a false FAIL, and controls 4B and 4D went missing because no option was
counted as routing to the step. Rule 4 now uses `_g7_asserted()`, which reads only before the term;
Group 6's checks keep the shared matcher.

---

# Group 8 — Malignant Bone Tumours (2 October 2026)

Three rules, build contract §8. Runner: `build/negative_controls_group08.py`. It mutates an
in-memory copy of the data, runs one rule, and expects FAIL. It first runs each rule on the
unmutated data and expects it to pass, because a check is proved with correct data as well as
broken data. Nothing on disk changes. Exit status 0 on 2 October 2026: **12 of 12 caught, 3 of 3
probes pass.** R1-E and R1-F were added on 4 October 2026 with the code-review fix to rule 1; the
merge with `main` the same day ran **14 of 14 caught, 3 of 3 probes pass.**

| | Control | Mutation | Caught by |
|---|---|---|---|
| R1-A | a round cell option emits 9260 | `bn_round_cell` option 1 `9364` → `9260` | rule 1 |
| R1-B | an alias maps to 9260 | alias "Ewing sarcoma" → `["9260"]` | rule 1 (reads the alias file) |
| R1-C | **the aneurysmal bone cyst exclusion claims /3** | `icdo_behaviour` `"0"` → `"3"` | rule 1, keyed off the behaviours `icdo32.sqlite` carries for 9260 |
| R1-D | a fallback names 9260 | `bn_round_cell_ihc` `nos_fallback.code` → `9260` | rule 1 |
| R1-E | an alias maps to 9260 in the other file shape | the alias file wrapped as `{"aliases": [...]}`, "Ewing sarcoma" → `["9260"]` | rule 1 (reads both shapes) |
| R1-F | the router regains a 9260 rule | `dual_group_rules["9260"]` copied from `9364` with `codes` `["9260"]` | rule 1 (sweeps the router's dual-group codes) |
| R2-A | a specific code with no tissue | `bn_imaging_os` emits `9364` | rule 2 |
| R2-B | a no-tissue terminal claims basis 7 | `bn_imaging_line` 8000 option, basis 2 → 7 | rule 2 |
| R2-C | a specific code at basis 1 | `bn_clinical_alias` emits `9180` at basis 1 | rule 2 |
| R2-D | **the path, not the flag** | the evidence gate's histology option captures `["Imaging"]` instead of `["Histology"]` | rule 2 — every histology terminal is now reached with no tissue in the file, and the first reported is "Sarcoma, type not stated" at basis 7 |
| R2-E | chondrosarcoma on imaging (design D10) | `bn_imaging_line` 8000 option → `9220` | rule 2 |
| R3-A | Ewing sarcoma on CD99 alone | the CD99 + NKX2-2 rule loses NKX2-2 | rule 3 |
| R3-B | the fusion rule weakened | the FET::ETS rule's `positive` → CD99 alone | rule 3 |
| R3-C | the Ewing rules disappear | every `9364` rule re-pointed to `8803` | rule 3 ("found no marker rule emitting 9364") |

**R2-D is the one that matters.** Rule 2 could have read each terminal's own
`basis_of_diagnosis` and checked that no basis-1 or basis-2 terminal emits a specific code. That
version passes a branch that misstates its own basis, which is the defect it exists to catch.
The rule walks the tree from the entry and carries `evidence_tests` the way `app.js`'s
`capture()` does, so a terminal's evidence comes from the path that reaches it. R2-D changes one
capture at the gate and leaves every terminal untouched, and the rule fails on terminals it
never had reason to look at before.

**The engine fix found while driving the tree has no build check.** The behaviour-exclusion
banner read "Benign" for every behaviour; `9250/1` Giant cell tumour of bone rendered as benign.
Observed in the browser on commit `1cb7a27` and corrected in `2580cdb`. After the fix the same
path rendered "Borderline or uncertain behaviour — outside this group's declared behaviour".
At the merge with `main` (4 October 2026) the Group VII fix replaced it; the path now renders
"Uncertain whether benign or malignant — outside this group's declared behaviour".

---

# Group 10 — Germ Cell, Trophoblastic and Gonadal Tumours (4 October 2026)

Four rules, build contract §5. Runner: `build/negative_controls_group10.py`. It mutates an
in-memory copy of the tree file, the router or the alias list, writes the router, the topography
lookup and the alias list to a temporary directory, runs one rule, and expects FAIL. A control
counts as caught only when a FAIL message carries the fragments the runner names for it; a FAIL
for another reason prints WRONG REASON. Before the controls, each rule runs on the unmutated data
and must pass, and rule 3 must return a NOTE when the alias file is absent. Nothing on disk
changes. The runner checks rule 3 against `data/aliases/aliases_group_10.json` (123 aliases since
five generic terms were left out on 6 October 2026; 128 under the union filter earlier that day, 46 under the intersection filter, 112 before it; Task T5); when the file is absent it uses seven correct aliases it holds itself. Exit status 0 on
4 October 2026, and on 6 October 2026 after Group 10 was listed at the 24 central nervous system
sites (registrar review B1): **24 of 24 caught for the expected reason, 5 of 5 probes pass.**
R3-E, R3-F and R3-G were added the same day with the spec-review fixes to rule 3; run against
rule 3 as committed in `4a1c0eb`, before those fixes, all three are MISSED. R1-F, R2-E and R4-D
were added at code review, so that the nos_fallback clause of rule 1, the placental scoping of
rule 2 and the default-tree clause of rule 4 each have a control.

**Revised the same day, after the merge of `main`.** The express lane now asks the site before
it enters a group whose data reads the site (registrar, 4 October 2026), so every entry into
Group X carries a topography and `g10_site_unstated` was removed. R1-E, which tested that the site
resolver emitted nothing, went with it. Rule 4 now requires the default to be `g10_extragonadal`
(R4-D, mutated to `g10_cns`) and requires every lookup topography from which `app.js` can enter
Group X, a code whose `candidate_groups` lists 10 or is not a list, to be named by a rule. With
the default on the extragonadal tree, dropping an Xb code from the rules no longer changes its
tree, so R4-C is now caught by that clause, and R4-E removes a second such code, `C38.1`, from
every rule.

**Rule 4 then checked destinations only, and code review found the gap.** A code the rules drop
reaches the default, which is the extragonadal tree, so an Xb rule stripped of every code that
cannot enter Group X passed, and so did an Xb rule naming `C77.9`. Rule 4 now requires each site
tree's rules to name exactly the lookup codes ICCC-2017 places in its family (Xa for `g10_cns`,
569 for `g10_ovary`, 620–629 for `g10_testis`, Xb for `g10_extragonadal`) and names every missing
and every extra code. R4-F and R4-G test the two directions; run against rule 4 as committed in
`aa0dbb1`, before the fix, both are MISSED. R4-F drops `C11.0`, whose candidate groups are 4, 9
and 11: the lookup holds no `C00.0`, the first code of the Xb range.

Each rule reads its source on every build. Rules 1 and 4 read ICCC-2017.sqlite ranges 94–117.
Rule 1 takes a tree's site from the router: the topography codes `groups["10"].tree_routing`
sends to that tree, resolved first-match as `app.js` `routedTree()` resolves them, not the tree's
own `topography` field. Rule 4 holds the router to ICCC-2017, so the extragonadal tree's site is
the Xb ranges and the one lookup code outside every Group X site range, `C77.9`, which reaches it
as the default. Rule 2 walks each tree from its entry and carries `evidence_tests` as `app.js`
`capture()` does (`_group8_terminals_by_evidence`, unchanged). Rule 3 reads every term in
`icdo32.sqlite`, `[obs]` terms included: an alias equal to an obsolete term still names that
term's code (R3-F). It compares an alias with a term after folding case, reading "tumour" as
"tumor" and dropping a trailing ", NOS". Without the last step R3-B matches nothing: ICD-O-3.2
carries "Mature teratoma, NOS", not "Mature teratoma". The same step reads "Teratoma" as
"Teratoma, NOS" (9080/1), so design D21's behaviour-neutral alias "Teratoma" → 9080, 9084 is
exempt by name (`GROUP10_D21_NEUTRAL_ALIASES`). The exemption matches the alias text with case
and whitespace folded, before the ", NOS" step, mapped to exactly those two codes: R3-D changes
the codes and R3-E the text, and both are checked in full. With the alias file present, rule 3
fails when no alias outside the exemption equals an ICD-O-3.2 term, because a rule that checked
nothing must not pass (R3-G).

| | Control | Mutation | Caught by |
|---|---|---|---|
| R1-A | a central nervous system teratoma hidden | `cn_histology` "Mature teratoma" loses its code and carries `excl 9080/0` | rule 1: "excludes 9080/0, but ICCC-2017 range 95 (Xa2) admits it at this tree's site, so the exclusion hides a Group X code" |
| R1-B | a benign ovarian teratoma registered | `ov_teratoma` "Mature cystic teratoma" emits `9080/0` instead of excluding it | rule 1: "emits 9080/0, which no ICCC-2017 Group X range admits at the 1 topography code(s) the router sends to this tree. Ranges holding 9080: 95 (Xa2, behaviour 0,1,3), 101 (Xb2, behaviour 3), 107 (Xc2, behaviour 3)" |
| R1-C | an extragonadal-only code in the testis | `ts_mixed` gains a `9086/3` branch | rule 1: "emits 9086/3 … Ranges holding 9086: 105 (Xb6, behaviour 3)" |
| R1-D | a gonadal-only code outside the gonads | `eg_mixed` gains a `9102/3` branch | rule 1: "emits 9102/3 … at the 115 topography code(s) the router sends to this tree. Ranges holding 9102: 110 (Xc5, behaviour 3)" |
| R1-F | a fallback off its site | `ov_ihc` `nos_fallback.code` `9064` → `9086` | rule 1: "g10_ovary ov_ihc: nos_fallback emits 9086/3, which no ICCC-2017 Group X range admits at the 1 topography code(s) the router sends to this tree (C56.9). Ranges holding 9086: 105 (Xb6, behaviour 3)" |
| R2-A | a histology from a marker | `cn_markers` alpha-fetoprotein option emits `9071/3` at basis 4 | rule 2: "emits 9071/3 at basis 4. Basis 4 registers 9064/3 or 9065/3, and 9100/3 for choriocarcinoma of the placenta in g10_extragonadal only (Visser 2023 Table 4, p. 06)" |
| R2-B | **the path, not the flag** | `ov_document_inventory`'s histology option captures `["Imaging"]` instead of `["Histology"]` | rule 2: "g10_ovary ov_histology: 'Dysgerminoma', reached with evidence ['Imaging'], emits 9060/3 at basis 7 with no histology or cytology in the file" |
| R2-C | basis 4 without imaging | `eg_document_inventory`'s markers option captures `["Tumour markers"]` only | rule 2: "eg_markers … reached with evidence ['Tumour markers'], emits 9065/3 at basis 4 without both Imaging and Tumour markers on the path (… rule 6, p. 05)" |
| R2-D | a histology from imaging | `ts_imaging` emits `9061/3` at basis 2 | rule 2: "emits 9061/3 at basis 2. Without pathology Group X registers 8000/3 at basis 1 or 2 (Visser 2023 rule 5, p. 03)" |
| R2-E | the placental code outside the extragonadal tree | `ov_markers` gains a `9100/3` branch at basis 4 | rule 2: "g10_ovary ov_markers … emits 9100/3 at basis 4. Basis 4 registers 9064/3 or 9065/3, and 9100/3 for choriocarcinoma of the placenta in g10_extragonadal only". Rule 1 passes it: 9100/3 is Xc5 at C56.9 |
| R3-A | germinoma filed as dysgerminoma | alias "Germinoma" → `["9060"]` | rule 3: "alias 'Germinoma' maps to 9060 Dysgerminoma. ICD-O-3.2 files Germinoma under 9064" |
| R3-B | **D21's own example** | alias "Mature teratoma" → `["9080"]` | rule 3: "D21 — alias 'Mature teratoma' is the ICD-O-3.2 term 'Mature teratoma, NOS' at 9080/0, and Group X emits 9080 at behaviour(s) 0, 1, 3" |
| R3-C | an in situ term on an invasive code | alias "Germ cell neoplasia in situ" → `["9064"]` | rule 3: "D21 — … 'Germ cell neoplasia in situ' at 9064/2, and Group X emits 9064 at behaviour(s) 3" |
| R3-D | the D21 exemption stretched by code | alias "Teratoma" → `["9080"]` alone | rule 3: "D21 — alias 'Teratoma' is the ICD-O-3.2 term 'Teratoma, NOS' at 9080/1, and Group X emits 9080 at behaviour(s) 0, 1, 3" |
| R3-E | the D21 exemption stretched by text | alias "Teratoma, NOS" → `["9080", "9084"]` | rule 3: "alias 'Teratoma, NOS' is the ICD-O-3.2 term 'Teratoma, NOS' at 9080/1, and maps to 9084, a code ICD-O-3.2 does not file it under" |
| R3-F | an obsolete term on the wrong code | alias "Granulosa cell carcinoma" → `["9064"]` | rule 3: "alias 'Granulosa cell carcinoma' is the ICD-O-3.2 term 'Granulosa cell carcinoma [obs]' at 8620/3, and maps to 9064, a code ICD-O-3.2 does not file it under" |
| R3-G | an alias file that checks nothing | every alias's text moved from the `alias` key to `term` | rule 3: "none of the 123 alias(es) in aliases_group_10.json outside the D21 exemption equals an ICD-O-3.2 term, so the rule checked nothing" |
| R4-A | a central nervous system subgroup lost | entry `9071/3` loses its `Xa4` rule | rule 4: "9071/3 shows subgroup 'Xc4' at C70.0, where ICCC-2017 places it in Xa4; 24 lookup topography code(s) disagree in all" |
| R4-B | a testis routed to the ovary | `C62.0` moves from the testis routing rule to the ovary rule | rule 4: "the router sends C62.0 to 'g10_ovary'; ICCC-2017 makes it an Xc topography, which goes to 'g10_testis'" |
| R4-C | the sacrococcygeal site unrouted | `C76.3` dropped from the extragonadal routing rule | rule 4: "C76.3 can enter Group X (its candidate_groups is [9, 10]) but no groups["10"].tree_routing rule names it, so it reaches the default instead of the tree ICCC-2017's site ranges give it" |
| R4-D | the default moved off the extragonadal tree | `tree_routing.default` → `g10_cns` | rule 4: "groups["10"].tree_routing.default is 'g10_cns'; a topography outside the Group X germ cell site ranges goes to g10_extragonadal" |
| R4-E | a mediastinal site unrouted | `C38.1` removed from every routing rule | rule 4: "C38.1 can enter Group X (its candidate_groups is [2, 4, 10]) but no groups["10"].tree_routing rule names it, so it reaches the default" |
| R4-F | an Xb site that cannot enter Group X unrouted | `C11.0` dropped from the extragonadal routing rule | rule 4: "the g10_extragonadal rule omits 1 lookup code(s) ICCC-2017 places in Xb: C11.0" |
| R4-G | a site outside every germ cell range routed | `C77.9` added to the extragonadal routing rule | rule 4: "the g10_extragonadal rule names 1 code(s) ICCC-2017 does not place in Xb: C77.9" |

**R2-B is the one that matters.** The mutation leaves the option's `basis_evidence_tier`
reading "histology" and every terminal under `ov_histology` reading basis 7; only the captured
`evidence_tests` changes. A rule that read the flag, or each terminal's own basis, passes this
file. Rule 2 walks from the entry and carries the evidence the way `app.js` does, so every ovarian
histology terminal is now reached with an imaging report as the only evidence on file, and the
first reported is "Dysgerminoma", 9060/3 at basis 7. The walk keeps one state per (node,
evidence) pair, so a terminal reached by a correct path as well is reported only for the faulty
one.

---

## REDCap flags removed from every group, 4 October 2026

Standing rule 16: the tool does not verify REDCap. `redcap_option_verified` and `awaiting_layer1`
were removed from Groups 1–8 (Group 9 already wrote neither) and from the Group 6, 7 and 8
generators. Group 3's one `code_status: "awaiting_layer1"` annotation became `own_code`, which
renders "Has its own ICD-O-3.2 code". Each generator was rerun to a scratch file: its output equals
the committed data minus the two keys, byte for byte for Groups 7, 8 and 9. For Group 6 the
original generator's output minus the two keys equals the edited generator's. Group 6's data also
carries hand corrections from 22 September 2026 that its generator never reproduced, before and
after this change.

Removed from `build/build_database.py`: `check_redcap_banner_signal` and `check_awaiting_layer1`,
whose only job was to keep the flags consistent with the REDCap option files.

Changed: `check_codes_against_source_of_truth` no longer consults the REDCap list. A code passes when
the ICCC classification for its group carries it (the markdown table, or `ICCC-2017.sqlite`, which
the table lacks for Group VII), or when ICD-O-3.2 carries its (code, behaviour) pair. Anything else
FAILs. `check_redcap_exact_names` reads no flag and no longer warns that REDCap lacks a code. It still
compares Groups 1 and 2's names with the option strings, pending the registrar. Group 5 moved to
`check_icdo32_round_trip()`, which it passes.

Controls, run against the working tree of `claude/remove-redcap-flags`:

| Control | Expected | Result |
|---|---|---|
| baseline: Groups 1–9 through the code guard | no FAIL | ok |
| A fabricated `9999/3` in Group 7 | FAIL | ok: "morphology_code 9999/3 is in neither the ICCC classification table for group 7 nor icdo32.sqlite" |
| B `8140/9`, a behaviour ICD-O-3.2 lacks, outside every Group IX range | FAIL | ok |
| C probe: `8140/3`, valid ICD-O-3.2 outside every Group IX range | NOTE, no FAIL | ok |
| D `ICCC-2017.sqlite` withheld | Group 7's ruled `8975/3` FAILs, so the database is what verifies it | ok |
| E Group 2 `9597` renamed | the exact-name check FAILs | ok |
| F probe: Group 1 baseline | the `9898` sibling exemption holds without any flag | ok |

**Later the same day, the registrar's ruling: `check_redcap_exact_names` is removed.** Groups 1 and 2,
the only groups it still compared, now have no name check. `check_icdo32_round_trip()` reports that
in a NOTE for each group outside `ROUND_TRIP_GROUPS`, so the gap shows in every build. Moving their
names to ICD-O-3.2 terms, which today fails the round trip 64 times (33 in Group 1, 31 in Group 2),
was handed to the Group 1 and Group 2 sessions. Control E above no longer applies; control F's
exemption went with the check.

# Brain marker cut-offs — Groups III and X (6 October 2026)

`check_brain_marker_cutoffs`, the registrar's ruling of 6 October 2026: the brain reads the SIOP
cut-offs, alpha-fetoprotein above 25 ng/mL and β-hCG above 50 IU/L, in serum and in cerebrospinal
fluid (Calaminus 2017, Methods; Calaminus 2026, Table 2). The check puts every reading through a
Python copy of `app.js` `inBand()`. In Group X it walks 324 cases (age not entered, 23, 24 and
120 months; each marker not entered, at its cut-off, and 0.01 above it) from the brain tree's
marker tier and compares the basis-4 codes still reachable where the numbers stop with the ruling's.
In Group III each `md_gct_*` gate must refer to Group X just above its cut-off and well above it,
and continue at the cut-off, at zero and with no value. Evidence: `docs/group_10_registrar_review.md`
E6.

Runners: `build/negative_controls_group10.py` (R5-A to R5-J) and `build/negative_controls_group03.py`
(G3-A to G3-G). Each control mutates an in-memory copy and expects a FAIL carrying named fragments.
The probe on the unmutated data passes first, which is the restore. Controls R5-J and G3-G load the
data as it stood at commit `689d610`, before the ruling, by `git show`, never from HEAD.

| Control | Breaks | First FAIL |
|---|---|---|
| R5-A | `cn_marker_age` boundary 24 → 12 months | age 23, cerebrospinal fluid alpha-fetoprotein 25.01 reaches `cn_afp_raised`; the ruling gives the report question |
| R5-B | `cn_afp_serum` 25 → 250 | serum 25.01 reaches `cn_markers`; the ruling gives alpha-fetoprotein raised |
| R5-C | `cn_afp_csf` 25 → 250 | serum 25, cerebrospinal fluid 25.01 reaches `cn_markers` |
| R5-D | `cn_afp_csf_no_serum` 25 → 250 | serum not entered, cerebrospinal fluid 25.01 reaches `cn_markers` |
| R5-E | `cn_hcg_serum` 50 → 250 | β-hCG serum 50.01 reaches `cn_markers`; the ruling gives β-hCG raised |
| R5-F | `cn_hcg_csf` 50 → 250 | β-hCG cerebrospinal fluid 50.01 reaches the imaging question |
| R5-G | `cn_hcg_csf_no_serum` 50 → 250 | β-hCG serum not entered, cerebrospinal fluid 50.01 reaches `cn_markers` |
| R5-H | `cn_afp_serum` reads "at or above" 25 | serum 25 reaches `cn_afp_raised`; the ruling gives the report question |
| R5-I | `cn_hcg_csf` sends a missing value to the imaging question | cerebrospinal fluid β-hCG not entered reaches the imaging question |
| R5-J | the brain tree at `689d610` | age 24, cerebrospinal fluid alpha-fetoprotein 25.01 reaches `cn_markers` |
| G3-A–D | each `md_gct_*` cut-off → 250 | 25.01 ng/mL (or 50.01 IU/L) does not refer to Group X |
| G3-E | `md_gct_afp_serum` reads "at or above" 25 | 25 ng/mL refers to Group X (band `>=25`) |
| G3-F | `md_gct_hcg_csf` bands read in ng/mL | bands[0] is read in `ng_per_ml`; the cut-off is 50 IU/L |
| G3-G | Group III at `689d610`, Hu 2016's cut-offs | 50 IU/L refers to Group X (band `>=2.5`) |

Result, 6 October 2026: **R5-A to R5-J all caught (34 of 34 in the Group X runner, 6 of 6 probes
pass); G3-A to G3-G all caught (7 of 7, 1 of 1 probe passes).**

End to end through the generator: `BRAIN_AFP_CUTOFF` set to 250 in `build/group10_tree.py` and
the data regenerated gives 13 FAIL lines, the first "afp_csf_ng_ml 25.01 … reaches cn_markers …
the ruling gives alpha-fetoprotein raised"; restored to 25 and regenerated, the check passes.


---

# Group 11 — Other malignant epithelial neoplasms and malignant melanomas (8 October 2026)

Four rules of build contract §5 (rules 1, 2, 3 and 5), plus the registration changes Group 11
needed in `build/build_database.py`. Rules 4, 6, 7 and 8 of the contract are on `docs/TODO.md`:
the registrar trimmed this task on 8 October 2026 to save usage. Runner:
`build/negative_controls_group11.py`. It mutates an in-memory copy of the tree file or the router,
writes the router and the topography lookup to a temporary directory, runs one rule, and expects
FAIL. A control counts as caught only when a FAIL message carries every fragment the runner names
for it; a FAIL for another reason prints WRONG REASON. Before the controls, each rule and each
registration check runs on the unmutated data and must pass. Nothing on disk changes and nothing
is pinned to a commit. Exit status 0: **20 of 20 caught for the expected reason, 10 of 10 probes
pass.**

Registration. `GROUP11 = 11`; `BEHAVIOUR_DECLARED_BY_GROUP[GROUP11] = {"3"}` (ICCC-2017 ranges
118–136 declare behaviour 3 on every row); `GROUP11` joins `ROUND_TRIP_GROUPS`, so the generic
"names are REDCap wordings" NOTE is no longer printed for the group, and the 13 entries whose
ICD-O-3.2 Preferred term is `[obs]` (the eleven all-`[obs]` pairs, 8551 and 8780) are WARN, never
FAIL. `check_refer_terminals` admits `refer_group` equal to the file's own group only on a branch
with `recapture_site: true` (contract D10), and `SELF_REFERRAL` is True in
`build/group11_common.py`: all 18 deposit nodes that have a deposit question carry "A carcinoma or
melanoma of another organ" → Group 11 with `recapture_site` (the melanoma tree's `me_deposit` has
its own shape). `parse_classification_subgroups` reads two-digit subgroup ids (`XIf10`, `XIf11`)
and a Group XII heading that has no colon; before, both rows of subgroups were filed under `XIf9`
and every Group XII row under group 11.

Each rule reads its source on every build. Rules 1, 3 and 5 read ICCC-2017.sqlite (rules 1 and 5
main group XI, ranges 118–136; rule 1 also every other range) and `icdo32.sqlite`. The routed
sites of every tree come from `group11_common.trees_table()`, the table the router and the trees
are built from; the helpers Group 10 wrote for the same purpose were parameterised by group
(`_iccc_ranges`, `_group10_tree_routing(repo, group)`), not copied. Rule 1 tests each emission at
every routed site of its tree. It passes at a site when a Group XI range holds the pair there, or
when no range of any group does (standing rule 3, design D11), and fails when another group holds
it: 8170/3 in the lung is Group VII range 57. The melanoma tree routes no site, so its emissions
must lie in an XId range. Rule 2 walks each tree from its entry and carries `evidence_tests` as
`app.js` `capture()` does (`_group8_terminals_by_evidence`, unchanged): basis 1 may emit only
8720/3 and only in `g11_skin` (Visser 2023 Table 3), basis 4 only a Table 4 pair with Imaging and
Tumour markers on the path, and nothing else is reachable without histology or cytology, basis 2
included. Rule 3 reads every emission against the eleven typed numbers and against every Preferred
term `icdo32.sqlite` marks `[obs]`. Rule 5 holds the subgroup `app.js` shows to ICCC-2017 at every
lookup topography and each routing rule to the sites `TREES` gives its tree. A lookup code that
lists Group 11 and no rule names reaches the default, and is a NOTE: C75.1 is the one today.

| | Control | Mutation | Caught by |
|---|---|---|---|
| R1-A | **a hepatic code in the lung** | `lu_picker` gains an `8170/3` branch | rule 1: "g11_lung lu_picker … emits 8170/3, which no ICCC-2017 Group XI range admits at 6 of this tree's 6 routed site(s) (C34.0 … C34.9), where another range holds it. Ranges holding 8170: 57 (VIIb, behaviour 3)" |
| R1-B | a carcinoma code in the melanoma tree | `me_picker` gains an `8070/3` branch | rule 1: "g11_melanoma me_picker … emits 8070/3, which is no ICCC-2017 XId (malignant melanoma) code; this tree routes no site, so every emission must lie in an XId range" |
| R1-C | a Group XI code hidden by an exclusion | the NIFTP exclusion in `th_not_malignant` names `8260/3` | rule 1: "excludes 8260/3, but ICCC-2017 range 120 (XIb) admits it at this tree's site, so the exclusion hides a Group XI code" |
| R1-D | a fallback off its site | `th_ihc` `nos_fallback.code` → `8170` | rule 1: "g11_thyroid th_ihc: nos_fallback emits 8170/3 … at 1 of this tree's 1 routed site(s) (C73.9) … 57 (VIIb, behaviour 3)" |
| R2-A | a specific code from a marker | the medullary option of `th_imaging_markers` emits `8260/3` at basis 4 | rule 2: "emits 8260/3 at basis 4. Basis 4 registers only the Visser 2023 Table 4 marker codes (8151, 8152, 8153, 8155, 8156, 8158, 8240, 8241, 8345)" |
| R2-B | **the path, not the flag** | the histology tier of `th_document_inventory` captures `["Imaging"]` | rule 2: "g11_thyroid th_histology: 'Poorly differentiated thyroid carcinoma, or insular carcinoma', reached with evidence ['Imaging'], emits 8337/3 at basis 7 with no histology or cytology in the file" |
| R2-C | the skin melanoma code outside the skin | the `8720/3` basis-1 branch of `sk_clinical` is copied into `lu_clinical` | rule 2: "g11_lung lu_clinical … emits 8720/3 at basis 1 in g11_lung. Only g11_skin registers a melanoma on clinical evidence" |
| R2-D | basis 4 without the marker | the markers tier of `th_document_inventory` captures `["Imaging"]` only | rule 2: "th_imaging_markers … reached with evidence ['Imaging'], emits 8345/3 at basis 4 without both Imaging and Tumour markers on the path" |
| R3-A | one of the eleven all-`[obs]` numbers | `th_picker` gains an `8130/3` branch | rule 3: "emits 8130/3, whose ICD-O-3.2 Preferred term is [obs] (design D3: such a pair stays off every screen)" |
| R3-B | an `[obs]` Preferred term not in the typed list | `me_picker` gains an `8780/3` branch | rule 3: "emits 8780/3, whose ICD-O-3.2 Preferred term is [obs]". 8780 is read from `icdo32.sqlite`, not from the eleven |
| R5-A | a subgroup rule lost | entry `8070/3` loses its `XIf4` rule | rule 5: "8070/3 shows subgroup 'XIf10' at C34.0, where ICCC-2017 places it in XIf4; 6 lookup topography code(s) disagree in all" |
| R5-B | a lung site unrouted | `C34.0` dropped from the lung routing rule | rule 5: "the g11_lung rule omits 1 routed site(s) TREES gives it: C34.0" |
| R5-C | a lung site routed to the thyroid | `C34.0` moves from the lung rule to the thyroid rule | rule 5: "the g11_thyroid rule names 1 code(s) TREES does not route to it: C34.0" |
| R5-D | the default moved | `tree_routing.default` → `g11_lung` | rule 5: "groups["11"].tree_routing.default is 'g11_lung'; a topography no tree routes goes to g11_unspecified" |
| R5-E | a rule routes to the melanoma tree | a rule sends `C77.9` to `g11_melanoma` | rule 5: "tree_routing.rules[18] routes to 'g11_melanoma', which is the melanoma tree, entered by a hop and named by no rule" |
| R5-F | **a shadowed rule** | `C34.0` also named by the first (adrenal) rule | rule 5: "the router sends C34.0 to 'g11_adrenal'; TREES routes it to g11_lung (a rule listed earlier names it too)" |
| REG-A | a self-referral with no `recapture_site` | the "another organ" option of `th_deposit` loses `recapture_site` | `check_refer_terminals`: "refer_group 11 is this group … The one exception is a recapture_site referral, which re-enters this group at the primary's site" |
| REG-B | the round trip runs for Group 11 | the `8010/3` entry carries the name "Control name" | `check_icdo32_round_trip`: "the triple (8010, 'Control name', 3) does not exist in ICD-O-3.2" |
| REG-C | the behaviour declaration is registered | the NIFTP exclusion names `8260/3`, behaviour 3 | `check_behaviour_exclusion`: "icdo_behaviour '3' IS in Group XI's own declaration (behaviour 3)". Without `BEHAVIOUR_DECLARED_BY_GROUP[GROUP11]` the check returns nothing |
| REG-D | the two parser patterns | the old and the new pattern, applied to "XIf10 Carcinomas of other specified sites" and "## XII Other And Unspecified Malignant Neoplasms" | the old subgroup pattern does not match the first and the old heading pattern does not match the second; the new patterns match both |

Probes (each passes on the committed data): rules 1, 2, 3 and 5; `check_refer_terminals`, which
now sees 18 recapture self-referrals and rejects none; `check_icdo32_round_trip` (13 `[obs]`
WARNs, no FAIL, no "REDCap wordings" NOTE); `check_behaviour_exclusion` (204 blocks); rule 5's
NOTE for C75.1; and `parse_classification_subgroups` (XIf9, XIf10 and XIf11 apart, XIIa1 under
group 12).

**R1-A and R2-B are the two the contract names.** R1-A needs the all-groups range read: 8170 at
the lung is in no Group XI range and in a Group VII range at every site, so "no range of any group
holds it there" (the D11 allowance) does not apply. A rule that tested only Group XI ranges would
either pass 8170 (no XI range, so "no XI range holds it") or fail every D11 code. R2-B changes
only the captured `evidence_tests`: every terminal under `th_histology` still reads basis 7 and
the option's `basis_evidence_tier` still reads "histology".

**What the controls do not reach.** Rule 1's D11 allowance passes any code that no ICCC-2017 range
holds at a site, so a code the registrar has not approved for that tree (a site-specific entity
offered at an organ that does not hold it) passes as long as no range places it elsewhere. Rule 5
does not test the lookup's `candidate_groups` against ICCC. The Layer 1 markdown for Group XI
(`ICCC 2017 Cancer Classification.md`) still disagrees with `ICCC-2017.sqlite`: the seven skin
codes 8090 to 8095 and 8097 read as outside every range, and the tokens `C80.90-C80.98` and
`C80.98` do not parse. `check_iccc_subgroup_ranges` reports 12 WARNs for it (4 unreadable tokens,
8 codes, the eighth being `8339`, which is outside every range by standing rule 3). The repair is
a Layer 1 job and is not yet in `docs/group_11_layer1_repair.md`.

## Compartment discriminator, 13 October 2026

Registrar's ruling: only the hard controls. `check_compartment_discriminator` is quiet on the real data and
fires when a group file captures a value the marrow question no longer offers: `group_01_dt.json` edited in a
scratch copy to capture `primary_compartment = nodal` (the retired value Group 2 still captured six times before
this change) gives `group_01_dt.json captures primary_compartment = ['nodal'], which the question does not
offer (marrow, not_marrow, not_known); a rule reading it never matches`. The fault sits between two layers: the
router's rules and the trees' captures each look correct alone.
