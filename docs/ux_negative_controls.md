# Negative controls for the tick-list, Home, filter, result-block and referral-hop checks

**6 October 2026.** Standing rule 10: break the data or the code on purpose, watch the check fail for
the right reason, restore, watch it pass. `build/negative_controls_ux.py` does it for every check added
with the interface changes of that day (spec `docs/superpowers/specs/2026-10-06-ux-overall-fixes-design.md`).

```bash
python3 build/negative_controls_ux.py     # exit 0 when every control behaves
```

It runs in about a minute. The engine controls run the new section of the engine gate alone
(`ONLY=ux node build/check_engine_flow.mjs`); the unbroken engine runs the whole gate once first.

## Engine controls

Each copies `app.js` to a scratch file, applies one edit that undoes a feature, and runs the engine gate
against that copy with `APP=<copy>`. The gate must exit non-zero **and** the named check must be among the
lines it prints as FAIL. An edit that matches nothing, or matches twice, is refused, so a control cannot pass
by changing nothing.

| Broken on purpose | The check that must name it |
|---|---|
| fit ignores `excludes` | imaging alone takes the imaging tier |
| fit ignores `any_of` | imaging alone takes the imaging tier |
| first_match takes the last fit, not the first | first_match: the first fitting option is the destination |
| a chosen special situation is ignored | a special situation routes at once |
| stepping back loses the ticks | stepping back to the tier taken automatically |
| the hop keeps the stains read under the old tree | the topography and the documents ticked carry over |
| the hop forgets where the evidence began | the trail shows the hop |
| the hop button is never offered | a referral to a built group offers Continue |
| an aid shows on every option, not only the selected one | a list with recognition aids shows none until an option is selected |
| Home never asks first | Home on a case with answers asks first |
| the organ-system filter ignores region names | typing a region name that is not in the system |
| no list has a filter box | the context list carries its own filter box |
| the benign terminal says no code is emitted again | a benign tumour reports Name, Morphology code |
| topography prints the C-code | topography is the code without its letter and point |
| the interface says Behaviour again | the interface says Behavior, never Behaviour |
| the behavior meaning is dropped | behavior codes read /N (meaning) |
| a laboratory value is also stored as a case variable a rule could read | the values stay out of the case variables |
| text that is not a number is accepted as a result | text that is not a number is refused |
| the panel's values are written into Suggested based on | the panel is one trail entry that summarises it |
| the laboratory screen offers the diagnostic escapes | the laboratory screen has a row per test |
| a result in the panel no longer ticks Lab Report | a result in the panel ticks Lab Report |
| an empty row is no longer taken as not in the file | an empty panel continues |
| the boxes start ticked again | an EMPTY Not in the file box |
| the hop drops the laboratory panel | the laboratory panel is a fact of the case |
| stepping back loses what was typed on the laboratory screen | stepping back reopens the panel as it was typed |
| the result no longer lists the panel | the result lists each test with its value and unit |
| the exit bar scrolls the page around the frame again | the tool opens no dialog, window or storage |
| a confirm dialog replaces the exit bar | the tool opens no dialog, window or storage |
| the unit sentence says "entering the count" under every unit again | the unit sentence no longer says |
| the second question lists every tier, not the ones that fit | two tiers fit histology with stains |
| a refused number ticks the blank rows' boxes | after a refused number the boxes the clerk did not tick are still empty |
| stepping back to the laboratory screen ticks the blank rows' boxes | stepping back shows no box ticked that the clerk did not tick |
| hex, exponent and thousands marks are accepted as results | a result is digits with at most one decimal mark |
| the number box has no length limit | the number box is length-limited |
| the laboratory entry is not marked as typed text | the entry is marked as typed text |
| a second laboratory panel replaces the first | a second panel replaces the tests it lists and keeps the rest |
| a unit another panel held is shown though this test does not list it | a unit held from another panel that this test does not list |
| stepping back across a hop leaves the receiving group's file loaded | stepping back across the hop brings the first group's file back |
| the app bar names whichever group file is in memory | the app bar names that group, not the one left |
| a step back forgets where the evidence began | stepping back to the tree question keeps where the evidence began |
| a tap while a group file loads is acted on | a second tap while the group is loading does nothing |
| a hop is offered into a site-routed group with no site | a referral into a group that routes its trees by site offers no hop |
| the hop keeps the old tree's grade and entity | the hop clears the old tree's reading |
| the hop forgets the organ system and the discriminator answers | the hop keeps the case |
| a range of sites with an instruction is mangled into a code | a topography written as a range with an instruction prints as written |
| Home is offered on a start-up failure | Home is not offered on a start-up failure |
| the Leave this case bar comes before the screen | the Leave this case bar comes after the screen |
| Home does not hand the focus to Keep Working | Home hands the keyboard focus to Keep Working |
| Keep Working does not hand the focus back to Home | Keep Working hands the focus back to Home |
| a redraw drops the keyboard focus | a box ticked from the keyboard keeps the focus through the redraw |
| a new screen takes the old control's focus | a new screen restores no focus |
| a refused number leaves the focus where it was | a refused number moves the focus to its box |
| the error is not tied to its box | a refused number moves the focus to its box, which names the error |
| the filter hides the selected row of a select-then-confirm list | a select-then-confirm list keeps the selected row on screen |
| the filter hides the chosen radio row | a radio list keeps the row the clerk has chosen on screen |
| typing hides the selected row on screen | typing in a filter box hides the rows that do not match and keeps the selected one |
| the filter count is not announced | typing in a filter box hides the rows that do not match |
| Enter in an empty filter box answers with the first option | Enter in an empty filter box answers nothing |
| Enter takes the selected row instead of the first match | Enter takes the first row that matches what was typed |
| Escape does not answer the leave bar | Escape answers the Leave this case bar with Keep Working |
| typing a number leaves Not in the file ticked | typing a number in a laboratory row clears |
| a box cannot be unticked | tick lists in the data |
| the ticks are kept in the order they were ticked, not the order drawn | tick lists in the data |
| a referral loses its Suggested based on row | a referral prints its rows |
| a non-reportable exclusion loses its topography row | a non-reportable exclusion prints its rows |
| the standard terminal loses its Suggested based on row | a code from the standard terminal at behavior |
| a tier taken by the engine is listed in Suggested based on again | a tier the engine takes by itself stays out of |
| a cytogenetics dropdown is no longer a filtered radio list | a cytogenetics dropdown is a filtered radio list |

## Data controls

Each hands `check_tick_lists()` a small node broken one way and expects a FAIL that names it. A sound
evidence gate and a sound `first_match` list are the positive controls.

| Broken on purpose | FAIL it must name |
|---|---|
| `{ihc}` alone fits no tier | N of 128 ticked sets fit no option |
| an id in both `requires` and `excludes` | the id and the two fields |
| an id not in the list | the id |
| an unknown vocabulary | the vocabulary |
| an evidence gate with no `tick_list` | evidence gate with no `tick_list` |
| `ticks` on options of a node with no `tick_list` | declares no `tick_list` |
| an unknown `resolve` mode | the mode |
| an unknown `ticks` field | unknown ticks field |
| no tier at all | needs at least one option with `ticks` |
| `first_match` with no fallback | a set fits no option |
| a shadowed `first_match` option | never the first fit |
| a `first_match` option with no `ticks` | every option carries `ticks` |
| more than 12 items | the enumeration budget |
| the tree's own first gate renamed, with no tick list | evidence gate with no `tick_list` |
| the gate behind a laboratory screen at the tree's entry, with no tick list | evidence gate with no `tick_list` |
| an `ask_siblings` tier with `ticks: {}` | fits every ticked set |
| a node renames the vocabulary's variable | overrides the vocabulary's variable |
| a vocabulary sentence names a schema field | internal identifier |
| a recognition aid on a node type, or a tick-list node, that does not draw it | never be shown |
| an empty recognition aid | non-empty string |
| a prompt, a `context_prompt`, a `none_label`, a `sibling_prompt` or a unit names a schema field | the field name |
| two tiers' rules swapped against the registrar-reviewed mapping | the node, "differs" |
| a router entry that is a laboratory screen not leading to a gate | not a document_inventory |

A sound input is the positive control for each: a gate that matches its mapping, a laboratory entry that leads to its
gate, an aid on a morphology list, a prompt with no field name.

## What the controls found in the checks themselves

The first run of the engine controls failed seven times, and each failure was a weakness in the new gate,
not in the engine:

- **One throw ended the whole section.** Five controls made the engine throw, the first throw aborted the
  scenarios, and the gate then failed with "the scenarios ran to the end" instead of naming the check that
  should have caught the fault. Fixed: a throw is now held and attached to the next check, which fails on its
  own assertion.
- **A test passed for the wrong reason.** "Typing `ovary` finds Ovary and testis" passed with the region
  names removed from the search, because the system's own label already contains the word. The test now types
  `lower limb`, which is in no system's label.
- **A test never reached the code it guarded.** The Behavior-spelling test called `currentLabel()` with a result
  on screen, which returns "Output" before the line that was changed. The test now clears the result first.
- **An assertion threw on the fault it was written to catch.** After the ticks were lost the test read
  `undefined.join()`. It now reads `(ticks || []).join()`.

The review of the same day (spec section 12) added these, and the controls above for them:

- **The gate never drew a screen.** `render()` and the listeners never ran, so Home, the leave bar, the filter, Enter and
  Escape were unguarded. The gate now draws into a stand-in page, and boots the real engine against the data on disk to
  fire the delegated listeners with synthetic events.
- **The sweep set the ticks directly.** It now ticks every box through the `tick` handler, in reverse order, then unticks
  those outside the set, so both branches of the handler and the drawn order are exercised; a special situation keeps the
  ticks on the case.
- **The result block was asserted on one terminal.** It is now checked on the standard terminal at /0, /1 and /3, the
  behavior exclusion, a referral and a non-reportable exclusion, each with the laboratory panel.
- **The lab boxes came back ticked** after a refused entry or a step back, and no check saw it. Three checks now count the
  ticked boxes, and two controls put the derived flag back.
- **A control broke the syntax** (a stale replacement left unbalanced parentheses) and the gate "failed" without naming a
  check. The runner already requires the named check among the FAIL lines, so the control was reported, not passed.
