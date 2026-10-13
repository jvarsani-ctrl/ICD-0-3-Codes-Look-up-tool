# Marker screens as a picker

**Written 13 October 2026.** Registrar's direction after running the Group I acute tree. Related:
`docs/superpowers/specs/2026-10-13-haematology-test-ticks-design.md` (the evidence boxes that precede it).

## Purpose

The clerk records which markers the report lists and what each showed, in one screen, by searching and adding.
A marker the clerk does not add is not done. The clerk is never asked what a panel covered after saying
which markers were in it.

## What the registrar said

- The one-marker-at-a-time screen asks about markers the report never listed. Make it **a search field**: whatever
  the clerk picks is loaded, then ask positive or negative. **Anything not picked is assumed not done.**
- When no marker was entered there is no point in asking what the panel covered.
- Strength: positive or negative for every marker, **plus a strength option only on the markers whose strength
  matters** (answer (a) to my question of 13 October).

## What this reverses

Registrar's ruling 13 (4 September 2026): the logic is a flow chart, and a marker checklist asks one marker at a
time and stops when the answer can no longer change. For the screens that opt in, the engine no longer draws that
sequence. It is not deleted: it is drawn for every other node, in every other group, and the build still requires a
`branch_sequence` and proves a witness for every rule.

## Design

**A node opts in with `marker_entry: "picker"`.** Seven nodes in Group I do: `ac_lineage_assignment`,
`ml_lineage_screen`, `ml_b_entity_panel`, `ml_pll_lineage`, `ml_t_entity_panel`, `ml_burkitt_screen`,
`mds_rcc_aplastic_ihc`. The other 77 marker checklists, in Groups II to XI, are unchanged.

**The screen** (`markerPicker()` in `app.js`): a row per added marker with its results, a filtered list of the
panel's remaining markers to add from, and Continue. Continue waits while an added marker has no result, so
nothing is left half-answered. There is a Remove on each row. The list is the node's `marker_groups`, and the
existing check that every marker a rule reads is on that panel means the picker always offers what a rule needs.

**Results.** Positive and Negative for every marker. Strongly positive and Weakly positive appear on a marker only
where **any rule on the node** reads it that way, taken from the data. The flow screen offered intensity only where
a *live* rule graded it, which is right mid-walk and wrong here. In the acute node that is `cMPO` (strong, read by
13 rules) and `CD19` (strong and weak, read by 9). 21 of its 41 rules read intensity (22 readings in all, one rule reads two), so plain
positive/negative would have changed classifications.

**Not done.** There is no "not done or not readable" answer. A marker never added is not done, and the matcher
already reads a marker never recorded as the same evidence as one that was negative or unreadable (ruling 11), so
nothing a clerk leaves out can be read as a result.

**Nothing entered.** The engine fills `marker_count_variable`, on Continue, with the number of the panel's
markers given a result. `ac_lineage_assignment` names `lineage_markers_entered` and carries a rule, placed before
the unconditional last one, that reads it as zero and records 9801 as *panel incomplete, not performed* (low
confidence, `workup_status: incomplete`, `alal_subtype` null), the outcome of the panel question's own "not performed"
answer, reached directly. With nothing entered, that unconditional rule was the only one that fired, so the new
rule intercepts exactly that case.

## What stays a question

`ac_alal_resolve` (the panel question) still appears when markers *were* entered and no rule settled the case. Its
two panel-coverage answers, AUL and ALAL-NOS, could in principle be derived from the markers, but the Pathway does not
give what that needs:

- AUL is a *positive diagnosis of exclusion*: no lineage-defining marker, **at most one lineage-associated marker per
  lineage**, and five lineages actively excluded (basophilic, erythrocytic, megakaryocytic, plasmacytoid dendritic, NK).
  Counting per lineage needs a table of which marker belongs to which lineage, and the Pathway gives examples, not the table.
- The Pathway's sourced exclusion markers cover **four of the five** lineages; the basophilic marker is unsourced.

The panel question's other answers are clinical judgments no marker can supply: a genetically or clinically
defined category, a divergent clone under 5%, a flow report that says "mixed phenotype" with no detail, and a review
that found no leukaemic population. Deriving AUL and ALAL-NOS needs the registrar to supply the lineage table.

## Testing

- Engine gate: a fixture picker (the screen offers the panel and no "not done"; a marker added gets a row and leaves the
  list; strength only where graded; Continue waits; a strong result takes the strong rule; a marker never added satisfies
  a `negative` requirement; nothing entered counts as zero and takes the `when` rule; a removed marker is as if never added).
- Engine gate: every picker node in the data offers its whole panel, and resolves both with nothing entered and with every
  marker positive. The acute lineage step, with nothing entered, records 9801 without asking.
- Build: `check_marker_entry` (the flag only on a checklist, a picker has markers to offer, the count variable is declared,
  read by a rule, and only on a picker), and `induce_flow.py` proves a witness for the new rule.
- Browser: the registrar's case through the acute lineage step.

## Out of scope, for the registrar to decide

1. **The other 77 marker checklists** (Groups II to XI) keep the one-at-a-time screen.
2. **Deriving AUL and ALAL-NOS** from the markers entered, which needs the marker-to-lineage table and a sourced
   basophilic marker.
3. **Reading the evidence boxes at this step.** A clerk who ticked neither flow cytometry nor IHC at the gate is still
   asked for markers. Nothing reads the ticks after the gate yet.
