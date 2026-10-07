# The guided flow — negative controls

Evidence that `build/check_engine_flow.mjs` catches what it claims to. Method per
`memory/data.md` §5A and Decision Tree master §4: break the engine deliberately, confirm
the check FAILs, restore, confirm it passes — and separately confirm it does **not** fire
on a correct engine, because a false FAIL is the more corrosive failure.

This check is not a data validator. It drives the shipped `app.js` and it is the only
thing in the repo that tests the ENGINE.

## What went wrong, and why nothing caught it

`induce_flow.py` proves every rule has a witness: an answer vector under which that rule,
and nothing earlier, matches. It proves it against `first_match`, which mirrors
`matchRules()` — the test the Continue button applies. Nothing proved a clerk could ever
ENTER such a vector, because what gets asked is decided by `nextMarker()`, and
`nextMarker()` was in no proof at all.

On 22 September 2026, driving Group VI's renal fork in a browser, the two came apart.
The case: a kidney mass in a child of 14, sickle-cell trait documented, medullary-pattern
histology. Answer SMARCB1 (INI1) loss, WT1 and BCOR all negative and the ALK rule was the
only one left alive — so the flow stopped, with ALK never asked. The screen read "One
outcome remains. Continue to record it." above one candidate, and Continue recorded
8000/3, Neoplasm malignant. The rule had a witness. The flow chart was well formed. The
data was correct. All 477 build checks passed.

That case is the one this file exists to keep coded correctly: ALK-rearranged renal cell
carcinoma is 3.8% of paediatric renal cell carcinoma and shares `8311/3` with six other
entities (Group VI build contract §0.5), and sickle-cell trait is the finding that puts it
on the table alongside renal medullary carcinoma in the first place (Argani 2021). The
engine downgraded it to the generic fallback with nothing on screen to say so.

Two defects, one in each half of that sentence:

1. **`nextMarker()` stopped on liveness.** A rule stays LIVE while a marker it needs is
   merely unanswered — `ruleLive()` skips an undefined marker rather than failing on it,
   which is what lets a partial walk narrow at all. "One rule left" is therefore not
   "decided". Fixed in `nextMarker()`: the node is decided only when what survives is
   also satisfied.
2. **`markerFlow()` chose its wording the same wrong way**, off `outcomeCount(live)`, so
   the screen promised a settled outcome the button would not deliver — including where
   the count line above it read "0 outcomes still in play". Fixed by choosing the wording
   with `matchRules()`, the same call Continue makes, and naming the fallback code the
   clerk is actually about to record.

## The two invariants

Both are read off the engine's own functions, never off a flag the engine sets.

| | |
|---|---|
| **A  Stranding** | When the flow stops with no rule satisfied, no unanswered marker may remain that could still satisfy a live rule — or the clerk was denied the question that would have changed the code. |
| **B  Honest screen** | What the clerk reads when the flow stops must agree with what Continue then records. The screen may promise a settled outcome only when `matchRules()` returns a rule. |

## Coverage

Two sweeps, because neither alone is enough. The **witness** sweep aims one walk at each
rule and so reaches the deep, heavily conditioned rules a branch-first walk never would.
The **exhaustive** sweep takes every branch of every node to a stop budget, which covers
small nodes completely — and the stranding shape lives in small nodes. 19 large nodes are
sampled to the budget and are reported as partial; a partial sweep is never reported OK.

```
node build/check_engine_flow.mjs
```

68 checklist nodes, 743 witness walks, ~58,000 stops, plus 9 fixtures. Under a minute.

## The negative control

`APP=` points the check at another copy of the engine. The pre-fix engine goes in a
scratch file and is swept with the same fixtures, which must then FAIL:

```
git show 0bf4755^:app.js > /tmp/app.prefix.js
APP=/tmp/app.prefix.js node build/check_engine_flow.mjs
```

On the engine as it was before either fix:

```
FAIL  the surviving rule's marker is asked, not stranded      asked ["MARK_A","MARK_B","MARK_C"]
FAIL  positive on that marker resolves to the specific code   got 8000/3 via fallback
FAIL  the screen promises no outcome when none is satisfied   "1 outcome still in play" then
                                                              "One outcome remains. Continue to record it."
                                                              while Continue records 8000/3
FAIL  not done on that marker falls back                      got 8000/3, screen promised an outcome
FAIL  rules sharing one outcome are still asked about         asked [], got 8000/3
```

and across the shipped data, **565 stranded states in 14 nodes over four groups** —
Group VI was not special:

| node | stranded states | | node | stranded states |
|---|---|---|---|---|
| g2_plasmablastic | 324 | | g2cut_acral_cd8 | 4 |
| rn_ihc_checklist | 80 | | md_pineal_ihc | 3 |
| g2_nkt | 73 | | g2_matureB | 3 |
| g2mast_sm_criteria | 40 | | md_pituitary_blastoma | 2 |
| sa_ihc_checklist | 16 | | g2mast_sarcoma_gate | 2 |
| g2_tfh | 8 | | g2_hodgkin | 2 |
| md_cranio_ihc | 6 | | g2_follicular | 2 |

One of those, for the flavour of what was being lost: at `g2_hodgkin` with EBV latency III
recorded, four markers answered negative stopped the flow and recorded 9650/3 while a rule
needing EBER, LMP1 and EBNA2 was still reachable and was never asked.

Invariant B alone, against the engine with the stranding already fixed (`HEAD` at
0d49a81), fires in **1546 states across 15 nodes** — every one of them a screen that named
an outcome the button would not deliver.

## The false-FAIL controls

Three of the nine fixtures exist only to fail a fix that buys invariant A too cheaply.

- **a satisfied first rule stops the flow on one question** — a fix that simply asks every
  marker every time passes A and fails this. The node is genuinely decided after one
  answer and must not walk the rest of the panel; this is the "seventeen questions where
  nine decide it" economy that ruling 13 bought.
- **a rule outside its gate is not asked about** — a rule whose `when` excludes the case
  is dead, and its marker must not be offered.
- **a satisfied rule is not reported as unresolved** — the control against a fix that makes
  every stopped flow read as a fallback.

And two prove the fix does not simply assume the survivor fires: with the stranded marker
answered **negative**, and again **not done or not readable**, the node must still record
its `nos_fallback` — 8000/3 in the fixture — and must not claim otherwise on screen.

## Driven in the browser, not only in the harness

A green harness is not a working tool, so the fix was also driven through the real UI at
`rn_ihc_checklist` — the case above, age band ≥10 with sickle-cell trait — tapping the
rendered buttons rather than calling the engine:

| answers | screen | Continue records |
|---|---|---|
| SMARCB1−, WT1−, BCOR− | asks **ALK** (before the fix: stopped here) | — |
| … ALK positive | "1 outcome still in play" · "One outcome remains. Continue to record it." | 8311 |
| … ALK negative | "0 outcomes still in play" · "These answers match no rule on this node. Continue records 8000 Neoplasm, malignant." | 8000 |
| … ALK not done | same as negative | 8000 |

Note the caching trap: `python3 -m http.server` plus the browser cache serves a stale
`app.js` through a plain reload. `fetch('app.js', {cache:'reload'})` and then reload.

## The express lane — a term filed under several groups is settled by the site

`app.js` entered an express-lane hit with `state.group = hit.groups[0]`. When
`alias_index.json` files a term under more than one group, the clerk went into the
lowest-numbered group's tree without being asked. On `dbe5fd4` the index holds 34 such
terms: "PPNET" (Groups 4 and 8) entered the neuroblastoma tree, "RCC" (Groups 1 and 6;
refractory cytopenia of childhood and renal cell carcinoma) entered the leukaemia trees,
and "Neoplasm, malignant" (Groups 3, 6 and 8) entered the CNS trees. A term shared by
Groups 6 and 9 enters Group 6, whose entry node captures the kidney as the primary site
on every option.

Registrar's ruling, 4 October 2026: the express lane does not ask the clerk for a group.
It asks for the primary site, with the guided route's organ system and region screens,
and intersects the term's groups with the groups the topography carries
(`topography_codes.json`, `candidate_groups`). One survivor is entered, routed rather
than asked, and recorded as a Group entry in the trail. No survivor — the term and the
site point to different groups — stops the case for referral. Several survivors — the
site does not separate them — also stop the case for referral. The guided route's
`narrowBySite` takes the site's list when the intersection is empty; the express lane
does not, because that would enter a group whose tree does not hold the searched term.

Consequence on `dbe5fd4` data: the 18 terms shared by Groups 1 and 2 (for example
"Burkitt leukaemia", "ATLL", "CLL") stop at every blood and bone-marrow code, C42.0 to
C42.4, because the topography carries both groups there. Unknown primary, C80.9, sits in
no organ-system row and cannot be picked on either route.

The engine gate's express-lane section reads `alias_index.json` and
`topography_codes.json`, computes the expected outcome of every (term, topography) pair
from those two files, and taps each pair through `handleOption` — alias, organ system,
region. On `dbe5fd4` data: 34 terms × 100 selectable codes give 841 routed to one group,
2469 stopped with no group and 90 stopped on a tie. The 1139 single-group terms must
still enter their group with no site question.

| engine | result |
|---|---|
| pre-fix, `git show dbe5fd4:app.js` | FAIL: "ATL" [1,2] reached stage handoff, group 1, not the site question |
| the family-question version this replaced | FAIL: "ATL" [1,2] reached stage group, group null, not the site question |
| mismatch falls back to the site's groups, as the guided route does | FAIL: "ATL" [1,2] at C64.9 [6]: expected a stop (no group), got stage node, group 6 |
| a routed group recorded with no trail entry | FAIL: "ATL" [1,2] at C77.9 [2]: entered Group 2 with no trail entry |
| a tie enters the first survivor | FAIL: "ATL" [1,2] at C42.0 [1,2]: expected a stop (tie [1,2]), got stage handoff, group 1 |
| every term asked the site (`> 1` changed to `> 0`) | FAIL: "5q- syndrome" [1] was asked the site — the single-group control |
| fix | OK |

Driven in headless Chrome at 2× by clicking the rendered buttons: "RCC" at the kidney
enters `g6_renal`; at bone marrow, C42.1, it enters Group 1 and asks the marrow pattern;
at C40.2 it stops with "The term and the site point to different groups". "PPNET" at
C40.2 enters `g8_bone`; at C74.0 it enters `g4_sympathoadrenal`. "Burkitt leukaemia" at
C42.1 stops with "The site does not decide the group"; at the lymph nodes it enters
Group 2. "Nephroblastoma" (Group 6 only) enters `g6_renal` with no site question.

Driving it found a second fault. `contextLabel()` named the last group file loaded,
which outlives a step back through the trail and a new case, so the app bar named a
group the case was not in. It now names a group only once `state.group` is set.

### Stepping back

A review of the change and a screenshot of a stepped-back case found three faults that
the walks above could not see, because every walk starts a case clean. All three come
from automatic trail entries. A tree routed from the topography, and a group routed from
the express-lane site, push a trail entry whose snapshot is the state after the answer
that triggered it.

1. **The trail kept the case before the step back.** Stepping back to an automatic Tree
   entry showed the site screen again with the earlier site, group and tree still in the
   trail. "Malignant tumor, giant cell type" routed to Group III at the pituitary, then
   stepped back and re-sited to the blood, stopped under a trail reading "Group: CNS and
   Miscellaneous Intracranial and Intraspinal Neoplasms". The guided route had the same
   fault before this change: stepping back to a routed tree and answering again recorded
   the Topography twice.
2. **The stop screen kept the routed group.** The same rewind restored `state.group`, so
   the app bar named Group III above a screen saying the site belongs to none of the
   term's groups.
3. **A search term leaked into a guided case.** Stepping back to the Tree entry of a
   single-group term that routes its tree returned to the landing screen with the term
   still set. A guided case started there took the express lane's site step.

The fix marks an automatic entry when it is pushed. Stepping back to one goes to the
clerk's answer that produced it. A stop clears `state.group`, and starting the guided
route clears the express lane's term, group and candidates. The engine gate adds three
scenarios that read the router and the two data files, not the engine's flag:

- R1, every multi-group term × every organ system in which it routes to a group that
  routes its tree: route, step back to the Tree entry, answer each site of that screen;
- R2, a single-group term per tree-routing group: step back to the Tree entry, take the
  guided route;
- R3, every presentation × organ system on the guided route: where a tree is routed,
  step back to it and answer again.

1916 stepped-back cases on `dbe5fd4` data.

| engine | result |
|---|---|
| before the review fixes | FAIL: 2570 R1, 2 R2, 51 R3 |
| fixes, without the automatic-entry rewind | FAIL: 1863 R1 ("the trail still carries the case before the step back"), 51 R3 ("the trail holds Topography twice") |
| fixes, without the automatic-entry rewind and without the guided clear | FAIL: 1863 R1, 2 R2, 51 R3 |
| fixes, without clearing `group` on a stop, before the automatic-entry rewind | FAIL: R1 "expected a stop with no group, got … group 3, app bar CNS and Miscellaneous Intracranial and Intraspinal Neoplasms" |
| fix | OK |

The guided clear and the stop's `group` reset are now reached only through an automatic
entry, which the rewind skips. They stay as a second line, and the third and fourth rows
show each one doing its work when the first line is removed.

## One tap must be enough

A click that follows typing was lost. The first tap on an express-lane search result did
nothing and the second worked, and the same held for Continue under a number or a
free-text answer and for "Not documented" under a number. The value typed was kept, so no
answer was misrecorded. The click was simply lost.

The cause was the event wiring at the foot of `app.js`. The search box, the number box
and the free-text box fire `change` when focus leaves them, and focus leaves on the
mousedown of whatever the clerk clicks next. The `change` listener ran the action
through `run()`, which re-renders the screen. The button under the pointer was replaced
before the mouseup, so the browser fired no click. The event trace, from real input:

```
mousedown on alias (pressed button connected: true)
change on query (pressed button connected: true)
mouseup on alias (pressed button connected: false)
```

with no click after it. The keyboard showed the same fault: Tab from the search box
re-rendered the screen and dropped focus to the page, so Enter on the first result did
nothing.

The fix reads a box the clerk types into on every keystroke (`input`), through the same
`handleOption`, and never re-renders for it. Checkboxes and selects keep `change`,
because it fires on their own click and the screen changes with them: "Not documented"
disables the number box, and a dropdown finding enables Continue.

`build/drive_first_tap.mjs` reproduces it. It drives headless Chrome with keystrokes and
mouse presses, because a scripted `element.click()` never moves focus and cannot see the
fault. It is not part of `build_database.py`, since it needs Chrome and a running server.
Each run was made with the engine swapped into the served worktree, then restored and
checked by checksum:

| engine | single taps (search result ×3, Continue after a number, Continue after free text) | "Not documented" after a number | dropdown enables Continue | Tab then Enter |
|---|---|---|---|---|
| before the fix | LOST ×5 | FAIL: the click is lost, the box stays enabled | OK | FAIL: focus goes to the page |
| `change` ignored for every control, an over-broad fix | OK | FAIL: no redraw | FAIL: Continue stays disabled | OK |
| fix | OK | OK | OK | OK |

## A single-group term is asked its site when its group reads the site

Registrar, 4 October 2026: the site must be asked. A term filed under one group entered that
group's tree with no topography, so every rule keyed on the topography failed open. "Rhabdoid
tumour", a Group IX-only spelling, coded a renal rhabdoid tumour as `8963/3` IXd3, because the
Group IX referral to Group VI at C64.9 could never match. The express lane now asks the site of a
single-group term whenever that group's data reads it, meaning the router routes its trees from the
topography or a `when` in its trees names `topography` (`groupReadsSite()` in `app.js`, a test of
the JSON's shape only). `afterSearchSite()` then keeps the group if the site carries it and stops
for the registrar if it does not. On this data that is Groups III, IV and IX.

The gate computes the same set from the router and the group files, never from the engine. Two
controls, each run against the working tree with `app.js` edited and then restored by checksum
(`25760bfcd9b1` before and after):

| Control | Engine edit | Gate result |
|---|---|---|
| the defect | the single-group site branch removed | FAIL: `"ACTH-producing tumor" [3] reached stage node, group 3, not the site question` |
| over-broad fix | `groupReadsSite()` returns true for every group | FAIL: `"5q- syndrome" [1] was asked the site or entered group null` |
| fix | — | OK: 55 multi-group and 483 single-group terms settled by the site; 848 single-group terms of a group that reads no site enter it directly |

`build/drive_first_tap.mjs` still passes every tap with real input.

## 7 October 2026: two site rules changed

Each control was run against the working tree with `APP=` pointed at an edited copy of `app.js`, so the
tree itself was never edited.

### A discriminator answer keeps a group through the site step

`primary_compartment` answers "nodal" and "extranodal" now carry `keep_on_site: [2]`. A lymphoma arises
in organs whose own candidate list does not name Group II; the site used to take the family away at 120
of 157 selectable sites. Driven through `handleOption`, lymphadenopathy then extranodal then every site:
Group II is a candidate at all 157 (62 enter it directly, 95 ask which group applies).

| Control | Result |
|---|---|
| `ONLY=ux` against the `app.js` of 2cb9c61 plus the other fixes, without `keep_on_site` | FAIL: "a group the answer keeps survives the site step when the site does not list it"; FAIL: "the site still narrows every other candidate"; the two controls that expect no change pass |
| `keep_on_site` names a group no asking presentation offers (the "unsure" presentation narrowed first) | build FAIL: "names group(s) [7] that no presentation asking this discriminator offers" |
| the same answer drops and keeps group 2 | build FAIL: "both dropped and kept on site by the same answer" |
| `keep_on_site` is a number, and an empty list | build FAIL: "must be a non-empty list of group numbers 1-12" |
| fix | OK |

### A single-group term of a group that reads no site is asked the site, and only records it

This reverses the control of 4 October 2026 above, which failed any engine that asked every term for its
site. The registrar chose to ask: before, 863 of 1,395 typed terms printed Topography as a dash. The
recorded site never narrows the group and never stops the case, so the gate tries every such term at the
first selectable site, at a site its group's candidate list excludes, at a site it names, and at "The file
does not state the site".

| Control | Engine copy | Gate result |
|---|---|---|
| the defect | `app.js` before the change | FAIL: `"5q- syndrome" [1] reached stage handoff, group 1, not the record-only site question` |
| the recorded site narrows the group | the `siteRecordOnly` branch of `afterSearchSite()` removed | FAIL: `"5q- syndrome" [1] at C64.9 [6]: expected Group 1 entered, got stage search_unresolved, group null` |
| no "not stated" answer | the button condition set to false | FAIL: `"5q- syndrome" [1] site screen offers no "not stated" answer` |
| fix | — | OK |

Driven through the handlers: "Retinoblastoma" at the retina enters Group V and records `C69.2`; "Burkitt
lymphoma" at the kidney enters Group II's tree selection with `C64.9` kept, where the guided route used to
stop; "Retinoblastoma" with "The file does not state the site" enters Group V with no topography.

### Review round, 7 October 2026

Two independent reviewers read the changes above. Their findings changed the engine and the gates:

- **A second tap while a group file was loading** left a multi-group term with the record-only flag, so "The file
  does not state the site" entered the lowest-numbered group. The group-file callback now ignores a case that
  has moved on, and the record-only entry points refuse unless the term is filed under one group. Replayed with the
  reviewer's delayed-fetch script: before, `after "not stated": stage handoff, group 1`; after, the stage stays
  `site` and no group is entered.
- **The `keep_on_site` build check** read `asked_by`, a note that had gone stale (it lists a presentation that never
  asks the question), so every group number passed. It now reads `dual_group_discriminator`, the field the engine
  reads, and requires `ask_before_site`. With the presentation list left alone, a `keep_on_site` naming group 7 now
  fails.
- **New gate checks**, each proved against a scratch tree that must fail:

| Control | Scratch tree | Gate result |
|---|---|---|
| the router's `keep_on_site` deleted | router edited | FAIL R5: found no keep_on_site in the router, so the scenario did not run |
| the engine ignores `keep_on_site`, router intact | `narrowBySite()` without the kept groups | FAIL R5: `lymphadenopathy, answer "nodal", site C64.9: Group 2 was kept by the router but is not a candidate (stage node, group 6, candidates [6])` |
| "not stated" offered on every express-lane site screen | `app.js` button condition widened | FAIL: multi-group term site screen offers "not stated" |
| the record-only flag survives a step back to Search | flag left out of `snapshot()` and of the guided reset | FAIL R4: back to Search, then the guided route, carries the flag |
| BAP1 rules restored | Group III data before the change | FAIL: BAP1 loss changes the code of a meningioma |
| follicular grade markers removed | Group II data before the change | FAIL: highest-grade combinations |
| retinoblastoma retinocytoma options removed | Group V data before the change | FAIL: 9512, 9513 and 9511 routes |

`build/drive_first_tap.mjs` stopped at its fourth control, which looked for a `select` that is now a filtered radio
list; it is fixed below.

## 7 October 2026: Group II occurs at any site, and the first-tap driver

### A group that occurs at any site survives a site that names none of the term's groups

The router marks Group II `occurs_at_any_site`: a lymphoma arises in any organ. A typed term filed under
Groups I and II used to stop at 120 of 157 sites, the sites where neither group is listed. Now the term enters
Group II there with the site recorded. A site that names one of the term's groups still decides, and a site that names
both (the marrow sites C42.0 to C42.4) still stops. The gate computes the expected outcome from the router and the
topography file, never from the engine. On the real tree: 34304 (term, site) pairs routed to one group, 48615 stopped
with no group, 605 stopped on a tie, 1440 pairs routed to a group that occurs at any site.

| Control | Scratch tree | Result |
|---|---|---|
| the defect | `app.js` before the change | FAIL: `"ATL" [1,2] at C64.9 [6]: expected Group 2, got stage search_unresolved, group null` |
| the fallback replaces the term's own survivors | fallback condition widened | FAIL: `"ACTH-producing tumor" [3] at C70.9 [3]: expected Group 3, got stage search_unresolved, group null` |
| the router's flag deleted | router edited | FAIL: no term was routed by `occurs_at_any_site` |
| the fallback added to the survivors, not only when there are none | `app.js`, `ONLY=ux` | FAIL: "a site that names one of the term's groups decides, although another group occurs at any site" |
| the flag a string, false, or on an unbuilt group | router edited | build FAIL: `occurs_at_any_site` must be true or absent; not on a group that is not built |
| fix | none | OK |

No site on the current data names Group I without Group II, so the last "names none" condition cannot be told apart from
an engine that adds the group to the survivors on real data. The synthetic fixture in the `ux` section pins it.

### The first-tap driver

`build/drive_first_tap.mjs` passes all eight checks in headless Chrome (typed first taps, Continue under a typed number
and a free-text answer, "Not documented", a list choice enabling Continue, and the keyboard). Its fourth control now
picks a radio, because the list is no longer a `select`. Control: a scratch copy that never fires the change event fails
that check with `{"before":true,"after":true}`; the other seven pass.
