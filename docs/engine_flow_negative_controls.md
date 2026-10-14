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

## 7 October 2026: the Group X audit

Each control below was run on a scratch copy of the tree (the repository was not touched), the check was watched
failing for the reason shown, and the clean tree passes. The gate computes every expected outcome from the router and
the data, never from a flag the engine sets.

### The typed lane enters a group at every site its own routing names

The router marks Group X `occurs_at_routed_sites`. A typed Group X term used to stop at 102 of the 167 selectable sites (65 entered)
because the site's `candidate_groups` omitted 10, with a screen that said the group does not code the term there. Now a
term filed under Group X alone enters at a site a `tree_routing` rule names when its own entries list the site in
`primary_sites`: a germ cell term at 167 of the 175 selectable sites (the 8 lymph node sites stay outside: no Group X
germ cell range covers them). A term ICCC-2017 places only at the gonads is stopped where the site's own list omits
Group 10, because the first version of this change entered such terms at the liver (found by the independent review);
where the site's list names Group 10 or names no group it enters the site's tree, which refers a carcinoma on
(third review, finding 3: this paragraph said "at every other site" before). A term filed under several groups, and a term
whose group file is not loaded, stay strict. A site that names a group of the term still decides, and the group does not tie
with it. The gate reads the expected outcome from the alias files and the entries by a second parser. On the real tree:
8246 (term, site) pairs routed through a group that occurs at any site or at its routed sites, 6674 of them at routed
sites. A synthetic fixture in the `ux` section pins the cases real data cannot tell apart.

| Control | Scratch tree | Result |
|---|---|---|
| the defect | `app.js` before the change | FAIL: `a site that a routing rule names, and the site's own list omits, takes the group that occurs at its routed sites` |
| the flag ignores the rule list | `occursAtRoutedSite` returns true on the flag alone | FAIL: `a site no routing rule names still stops, although the group routes a default tree` |
| the default tree counts as a named site | `\|\| tr.default` added | FAIL: `"Adenocarcinoma, NOS" [10] at C77.0 [2,9]: expected a stop (no group), got stage node, group 10` |
| the fallback added to the survivors, not only when there are none | `afterSearchSite` | FAIL: `"Carcinoid tumor, NOS" [6,10] at C64.9 [6]: expected Group 6, got stage search_unresolved, group null` |
| the term's own entries not read (the flag and the rules alone) | `occursAtRoutedSite` | FAIL: `"Adenocarcinoma, NOS" [10] at C42.0 [1,2]: expected a stop (no group), got stage node, group 10`; and `a routed site the term's own entries do not list stops` |
| a term filed under several groups taken by the fallback | the one-group test removed | FAIL: `a term filed under several groups is not taken by the routed-site fallback` |
| the router's flag deleted | router edited | FAIL: `no term was routed by occurs_at_routed_sites` |
| the flag a string, on an unbuilt group, or on a group with no routing rules | router edited | build FAIL: `occurs_at_routed_sites` must be true or absent; not on a group that is not built; not on a group with no `tree_routing` rules |
| fix | none | OK |

### A referral asks for the primary's site

A referral can say `recapture_site`. The referral screen then does not print the deposit's site as the case's, and
"Continue in Group N" drops the site, asks for the primary's, and enters the receiving group with it. A group that reads
no site records the answer only and offers "The file does not state the site"; one that routes its trees from the site
is given one. The gate drives every such branch in the data (60 to built groups, of 71 in all, in Groups III, VII, VIII, IX and X) through
the referral, the hop, the site, the group's first screen, a step back to the organ system with a second site, and a step
back to the referral.

| Control | Scratch tree | Result |
|---|---|---|
| the defect | `app.js` before the change | FAIL: `23 problem(s): ... no recapture referral, stage output` (and the leukaemia and routed-site checks) |
| the hop keeps the site | `delete state.captured.topography` removed | FAIL: `after the hop stage site, group 4, record group 4, topography C56.9` |
| the referral screen prints the site | the row restored | FAIL: `the referral screen prints the deposit's site as the case's` |
| no hop for a case with no site | `canHop` without the exemption | FAIL: `a referral that asks for the primary's site offers the hop into a group that routes by site although the case has no site` |
| "not stated" offered to a group that reads the site | `siteRecordOnly = true` always | FAIL: `the "not stated" answer is offered to a group that reads the site` |
| the flag left out of the snapshot | `snapshot()` | FAIL: `stepping back to the organ system gave stage site, record group null` |
| the flag not cleared once the group is fixed | `enterRecordedGroup()` | FAIL: `after recording C42.0 stage handoff, group 2, topography C42.0, record group 2` |
| the opening presentation's site list kept after the hop | `state.archetype` not cleared | FAIL: `after a recapture hop the primary's site is asked from every organ system, not only those the opening presentation fixed` (`system rows 1 then 1 of 28`) |
| `recapture_site` false, or with a captured topography | data edited | build FAIL: `recapture_site must be true or absent`; `sets a topography and also asks for the primary's site` |
| a deposit referral without it, or a leukaemia that does not set C42.1 | Groups III, VII, VIII and X edited | build FAIL: `a deposit is coded at its primary, but this referral does not ask for the primary's site`; `a leukaemia is recorded at the bone marrow, C42.1` |
| the extragonadal bone sarcoma without it, a leukaemic infiltration that keeps the gonad, a myeloid sarcoma that sets a site | Group X edited | build FAIL: `GROUP 10 RULE 5` in each case |
| a deposit node renamed so its id says neither word, with its flags removed (the review's own test) | Group VII edited | build FAIL: `hp_secondary_site (options[0]) ... a deposit is coded at its primary, but this referral does not ask for the primary's site`, found by the referral's own text |
| a neuroblastoma-in-bone referral, or a spinal-canal neuroblastic referral, without the flag | Group VIII, Group III edited | build FAIL: `bn_round_cell (options[9]) ... does not ask for the primary's site`; `sp_extrinsic_gate (options[2]) ...` |
| the leukaemic infiltration relabelled and its C42.1 removed | Group X edited | build FAIL: `GROUP 10 RULE 5: ov_other ... must record the bone marrow, C42.1` (before the review this passed, counting the branch but asserting nothing) |
| "the primary is not known" without C80.9 | Group X edited | build FAIL: `ts_deposit (options[8]) ... a deposit whose primary is not known is recorded at C80.9` |
| fix | none | OK |

### The subgroup line at a site no Group X range covers

C77.x is reached only by a referral hop, and the router sends it to the extragonadal tree. A pair with an Xb and an Xc
subgroup shows Xb there, not the gonadal default. The build derives the expected line from ICCC-2017: 144 (entry,
topography) pairs. Control: the C77 codes removed from one entry's Xb rule, so it falls back to Xc1: build FAIL
`shows subgroup 'Xc1' at C77.0, a site outside every Group X germ cell range that only a referral hop reaches`.

### The laboratory panel takes a limit

`>1210` and `<0.5` are recorded as typed and printed with the number and unit; `>`, `<`, `>>5`, `>-5`, `5>`, `<1e3`,
`=5` and `≥5` are still refused. Controls: the old pattern fails `>1210 refused` and the print check; a pattern that
accepts `=` or repeated signs fails `>>5 accepted, ><5 accepted, =5 accepted`.

### Added on the same day, under the registrar's delegation

Each run on a scratch copy and watched failing for the reason shown.

| Control | Scratch tree | Result |
|---|---|---|
| a Group II leukaemia referral without the bone marrow | Group II edited | build FAIL: `g2_compartment_gate (options[3]) '' -> Group 1: a leukaemia is recorded at the bone marrow, C42.1 (WHO Rule E)` |
| Group VII's liver leukaemia referral without it | Group VII edited | build FAIL: `hp_histology (options[15]) ... -> Group 1: ... this referral sets None` |
| a histology screen that lacks dysgerminoma, or a teratoma screen that lacks `9083/3` | Group X edited | build FAIL: `GROUP 10 RULE 6: ts_histology offers no option that records 9060/3 (Dysgerminoma)`; `eg_teratoma offers no option that records 9083/3` |
| the marker gates' fallback hint back to the laboratory's range, or a hint that says the cut-offs are not applied, or a `<=` band pointed back at cn_markers | Group X edited | build FAIL: `BRAIN MARKERS — cn_markers_cutoff is where a walk from 24 months stops when a value was not entered, but its hint does not apply the SIOP cut-offs` (the review found the first version of this check missed the last two) |
| a Group II referral that drops C42.1 and adds "This is not a myeloid sarcoma." | Group II edited | build FAIL: `g2_precursor (resolution_logic[0]) '' -> Group 1: a leukaemia is recorded at the bone marrow, C42.1` (the first version let any mention of the words through) |
| fix | none | OK, 1142 checks |

### The marker gates' second answer, the three sites and the gonadal carcinoma picker (registrar's approval, 7 October 2026)

Each run on a scratch copy and watched failing for the reason shown.

| Control | Scratch tree | Result |
|---|---|---|
| a gate that offers "another unit" with no band to send it to, or two answers that do not exclude each other | `app.js`, fixture | engine gate FAIL on the matching fixture check |
| `cn_hcg_csf` sends "not documented" to the report question (the rule before the approval) | Group X edited | `negative_controls_group10.py` R5-I: `BRAIN MARKERS — ... hcg_csf_iu_l not entered ... reaches cn_markers_cutoff ... the ruling gives neither raised` |
| `cn_hcg_csf` reads "in another unit or only described" as not raised | Group X edited | R5-K: `hcg_csf_iu_l in another unit or only described ... reaches cn_imaging_markers` |
| `cn_afp_csf` sends "not documented" to the report question | Group X edited | R5-L |
| a gate without an `other_unit` band (the walk cannot see it: the gate's fallback edge reaches the same question) | Group X edited | R5-M: `BRAIN MARKERS — cn_afp_serum has no other_unit band` |
| the thymus dropped from the extragonadal routing rule | router edited | build FAIL: `GROUP 10 RULE 4: C37.9 can enter Group X ... but no tree_routing rule names it` |
| an Xd code removed from the picker | Group X edited | build FAIL: `GROUP 10 RULE 7: g10_ovary offers no option that records 1 gonadal carcinoma code(s) ... 8560`; the engine gate fails its picker checks |
| a search term that is not an ICD-O-3.2 synonym | Group X edited | build FAIL: `GROUP 10 RULE 7: ts_carcinoma_other 'Epithelioma, malignant': search term 'Not an ICD-O name' is not a live ICD-O-3.2 Synonym or Related term of 8011/3` |
| synonyms not matched by the filter | `app.js` | gate FAIL: `an ICD-O-3.2 synonym finds the option although no label shows it` |
| the typed term not carried into the filter, or refilled after the clerk clears it | `app.js` | gate FAIL: `a case from the search box starts with the typed term in the filter`; `clearing the box shows the whole list and does not refill it` |
| fix | none | OK, 1152 checks; `negative_controls_group10.py` 36 of 36 caught, 6 of 6 probes pass (before the third review, below) |

### The third independent review of the Group X batch (7 October 2026)

An independent reader drove the real `app.js` against `main` and the branch and found five defects and one minor
one. Each fix below was run on a scratch copy (`app.js`, Group X data) or in `negative_controls_group10.py` and
watched failing for the reason shown.

| Finding | Fix | Control | Result |
|---|---|---|---|
| 1. Nine aliases the picker added were strings another group already files (six Group VI, three Group III), so six Group VI terms that entered Group VI at every site on `main` stopped at 174 sites, and three Group III terms tied at the pituitary and the brain. A sweep of all 297,325 (term, site) cells against `main` now changes only `search_unresolved` to a Group X tree, in 6,674 cells. | `generate_group10_aliases.py` leaves a picker-only code's alias with the group that holds it; Group 10 rule 8 forbids sharing. | `negative_controls_group10.py` R8-A (a Group VI string on 8510), R8-B (a Group III string on 8158) | CAUGHT: `GROUP 10 RULE 8: ... 'Medullary carcinoma, NOS' is also held by Group 6` |
| 2. Thirty-seven typed names (ICD-O-3.2 Related terms) opened the picker with the name in the box and no option visible. | `search_terms` are the live Synonym and Related terms; rule 7 accepts both and rejects an obsolete term. The engine gate checks every ICD-O-3.2 name the alias layer indexes for a picker code against the filter's own matcher. | the Related terms stripped from a scratch copy of the data | engine gate FAIL: `every ICD-O-3.2 name the search box indexes ... is found by that picker's filter box`; 398 pairs, `Keratoacanthoma` among those not found |
| 2, residue. A curated name or the REDCap wording that the list cannot find (`Gastrinoma, NOS`) left the box hiding every row. | `optionList` starts no filter when no option matches the typed name. | the fallback removed from a scratch `app.js` | engine gate FAIL: `a typed name that matches no option starts no filter, so the whole list shows` |
| 4. Six codes whose ICD-O-3.2 Preferred term is `[obs]` were on screen (five in the picker, `8630/3` on the sex cord screens), against the build's own warning and design D11. | Taken off; Group 10 rule 7 exempts them from "every Xd code has an option" and fails any option that records an obsolete pair. | an option for `8130/3` added to the picker | CAUGHT: R7-B `GROUP 10 RULE 7: an option records 1 pair(s) whose ICD-O-3.2 Preferred term is marked [obs] ... 8130/3` |
| 2 and 4, rule 7's other two faces. | | an Xd code removed from the picker; a search term that is no ICD-O-3.2 term | CAUGHT: R7-A, R7-C |
| 3, 5, 6. Documents. The claim that a gonad-only term stops at every other site was false where the site's list names Group 10; figures were stale (159 of 167 sites, 57 of 159, 82 and 86 options, "every one of the 136 entries"); the lymph node sentence ignored ranges 114 and 116. | `docs/TODO.md` §34, `docs/group_10_registrar_review.md`, this file, and the 8010/3 line in `generate_group10_entries.py`, corrected from computed counts. | none (text) | |
| Found while rerunning the suites. Two controls in `negative_controls_ux.py` edited the old text of `canHop` in `app.js`, which the recapture hop had changed, so they reported "occurs 0 times" and checked nothing. | Both repointed at the current line; a third control added for the recapture exception (`r.recaptureSite === true ||`). | the exception removed from a scratch `app.js` | gate FAIL: `a referral that asks for the primary's site offers the hop into`; `negative_controls_ux.py`: every control behaves |
| fix | | none | OK, 1162 checks; `negative_controls_group10.py` 41 of 41 caught, 8 of 8 probes pass; `negative_controls_ux.py` every control behaves; Groups III, VII, VIII and IX control suites pass |

### Guided entry: body system, organ and the marrow question (13 October 2026)

Registrar's ruling the same day: write only the hard controls (`CLAUDE.md`, rule 10). Each row restores a
plausible pre-fix behaviour in a scratch copy of `app.js` (`APP=<copy> node build/check_engine_flow.mjs`) and
must fail for the reason shown. The unbroken engine passes all 196 checks.

| Breakage | Where | Result |
|---|---|---|
| The site narrows the candidates before the marrow question is settled (the order the engine had before this change). The design exists to prevent it: a leukaemia that presents in a lymph node loses Group I. | `app.js`, `afterSite()` | gate FAIL, 5 checks: `more than 25% blasts keeps Group I for a node that is the site` (candidates `[9]`), `no marrow aspirate yet drops nothing` (`[2,9]`), `a thyroid under "not sure" is asked`, the region check, the trail check |
| A step back forgets the body system, so the case keeps the system it had chosen and lists only that system's organs. | `app.js`, `snapshot()` | gate FAIL, exactly one check: `stepping back to the site of origin shows the system screen with the earlier answers gone` |

### Group 5: the registrar's rulings of 14 October 2026

Hard controls only (`CLAUDE.md`, rule 10). Each was planted in a scratch copy of the tree and run with `ONLY=g05 node build/check_engine_flow.mjs`. The unbroken tree passes every Group 5 check.

| Breakage | Where | Result |
|---|---|---|
| The conflict notice ignores which boxes conflict and shows for any ticked box beside the row. | `app.js`, `tickConflictNotice()` | gate FAIL: `the inadequate-specimen row beside a ticked histology report shows a notice, and the notice does not show for a cytology report ...` |
| The conflicting tick is kept when the row wins. Found on the real page: the result read "Suggested based on Histology report" for a report the clerk had marked inadequate. | `app.js`, `tickContinue()` | gate FAIL: `... does not list the report as the evidence it rests on (RP6)` |
| The enucleation screen reads a differentiated finding before a poorly differentiated one. The data gate's first-match rules still pass, because each option stays the first fit for some set. | `group_05_dt.json`, `rb_enucleation_report` options | gate FAIL, 2 checks: the golden routes and `every one of the 64 ticked sets ends where the order says` |
| The referral wording reads a named retinoblastoma before a named non-malignant cause. | `group_05_dt.json`, `rb_clinical_alias` options | gate FAIL, 2 checks: the golden routes and `of the 16 ticked sets only a named retinoblastoma ... records 9510/3` |
| The fourth screen reads a mimic box before a needs-tissue box, so both ticked ends the case as not reportable. The data gate's first-match rules still pass, because each option stays the first fit for some set. | `group_05_dt.json`, `rb_imaging_insufficient` options | gate FAIL, 3 checks: the golden routes, the RP2 box check, and `of the 8 ticked sets, any needs-tissue box refers Group XII even beside a mimic box` |
| The imaging tier forgets to exclude a liquid biopsy, so two tiers fit and the clerk is asked to choose. | `group_05_dt.json`, `rb_document_inventory` option 1 | gate FAIL: `each of the 16 ticked sets goes straight to ... and the clerk is never asked to choose between tiers` (the data gate's mapping check fails too) |

