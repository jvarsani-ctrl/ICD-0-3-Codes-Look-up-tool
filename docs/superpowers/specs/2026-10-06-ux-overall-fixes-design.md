# UX fixes: result block, Home, search boxes, tick lists, referral hop

**Status:** approved by the registrar on 6 October 2026. Written from the "ICD Overall fixes" session on branch
`claude/overall-fixes-ux`, worktree `.claude/worktrees/overall-fixes-ux`.

**Source:** the registrar's hand review of Group 10 (evidence question, benign result, organ-system list, no
way out of a case) and three engine features handed over by the Group 10 session the same day (recognition
aids, tick-boxes for mixed tumours, a referral that continues into the receiving group).

## 1. Result block

Every terminal that finds a code prints one block, in this order:

| Row | Content |
|---|---|
| Name | the entry's `morphology_name` |
| Morphology code | four digits, no behaviour |
| Behavior code | `/N (meaning)`: `/0 (Benign neoplasm)`, `/1 (Uncertain whether benign or malignant)`, `/2 (In situ)`, `/3 (Malignant)`, `/6 (Metastatic)`, `/9 (Malignant, uncertain whether primary or metastatic)` |
| Topography code | the ICD-O code without its letter and point, then the ICD-O name: `569 (Ovary)` for C56.9, derived from the C-code. A group may record a range with an instruction ("C70.0-C72.9 - record the exact code documented"); that is text, and prints as written |
| Suggested based on | the trail since the case entered its group (was "Based on") |

- The behaviour-exclusion terminal (Group 4 ruling D1) prints the same block. Its "Morphology: No code emitted
  here" row is removed. The registrar's ruling of 6 Oct 2026: a morphology code is always reported, benign or not.
- The group's own admitted behaviour becomes a plain row: "Group admits: Behavior code /3 (Malignant) only".
  The "Registrar decision required" banner stays.
- The other terminals keep their shape. A referral and a non-reportable exclusion carry no morphology code of
  their own. Their Topography row uses the same `569 (Ovary)` format.
- "Behaviour" becomes "Behavior" in every interface label in `app.js`. The ~260 clerk-facing sentences in the
  group JSON files are a later scripted sweep, because the Group 10 session has those files open.

## 2. Home

A Home button sits in the top bar on every stage except the landing screen and a failed start. With nothing answered it
resets at once. With answers it shows a quiet bar below the screen, "Leave this case? The answers given so far will be
discarded.", with Discard and Keep Working (the first version was a yellow banner above the screen; the registrar
found it too eye-catching). Home hands the keyboard focus to Keep Working; Escape answers Keep Working and the focus
returns to Home.

## 3. Search boxes

Every single-choice list gets a filter box above the options (registrar's choice: every question, including
yes/no). The options stay visible, so one tap still works. Typing hides non-matching options; Enter picks the
first match, and does nothing when the box is empty. The row the clerk has selected stays on screen whatever is typed.
The filter text is kept in `state.draft` so a re-render does not lose it. One constant, `FILTER_MIN_OPTIONS`,
restores "long lists only". The count of rows showing is read out through a status line.

The organ-system list also matches the region names inside each system, so "ovary" finds "Ovary and testis".

Not filtered: test-result state chips, the marker grid and the workup status dropdown. They are not questions
with one answer to pick.

## 4. Tick lists (one schema extension, ratified 6 Oct 2026)

A node may declare `tick_list`. No new `node_type`. It replaces the node's single-choice screen with a
checklist, then resolves a destination from the ticked set.

```json
"tick_list": {
  "vocabulary": "evidence_documents",     // a list in presentation_router.json ...
  "items": [ { "id": "…", "label": "…" } ], // ... or items authored on the node
  "variable": "documents_in_file",         // captured as an array of ids
  "label": "Documents in file",            // trail label
  "prompt": "Tick every report that is in the file.",
  "resolve": "ask_siblings"                // or "first_match"
}
```

Each option may carry `ticks`:

```json
"ticks": { "requires": ["histology"], "any_of": ["ihc", "genetics"], "excludes": ["cytology"] }
```

An option **fits** a ticked set when every `requires` item is ticked, at least one `any_of` item is ticked (when
`any_of` is given), and no `excludes` item is ticked. `ticks: {}` fits every set.

- `ask_siblings` (the evidence gate): options with `ticks` are tiers; options without it are special
  situations, listed under the checklist with a default "None of these". A chosen special situation routes at
  once. Otherwise one fitting tier is taken automatically (an automatic trail entry); two or more are asked on a
  second screen.
- `first_match` (mixed-tumour components): the first fitting option in file order is the destination. An
  unconditioned last option is the fallback.

Rules that stay mechanical in the data gate, each with a negative control:

1. every id in `requires`, `any_of` and `excludes` is in the vocabulary, and none of the three overlap;
2. every ticked set (2^n) fits at least one tier, so no set dead-ends;
3. every tier fits at least one set. For `first_match` every option must be the first fit for some set
   (a witness), or the build fails.

The seven evidence documents, worded as the registrar wrote them: Referral Letter/Clinical Note, Imaging
Report, Lab Report, Cytology, Histology Report, IHC Report, Gene reports for cancer.

The ticked ids are captured and reused: a second gate in the same case (a lymphoma gate that hands to the
leukaemia gate) opens with the same boxes ticked.

Existing options keep their labels, captures and routes. Only `ticks` is added, so no clinical branch moves.

One exception, and it adds no branch. A tier whose label offers two alternatives ("flow cytometry and/or IHC") needs
morphology AND (Lab Report OR IHC Report), which one `any_of` cannot say. The mapping then lists `extra_options`: a
copy of that option with the other rule and with the tests it may not credit removed (an IHC report alone is not
flow cytometry). Group I's acute and mature-lymphoid gates have three and two.

A tier the engine takes by itself is kept out of "Suggested based on", which lists the documents ticked: the tier's
sentence can say more or less than was ticked (an imaging report beside "no imaging report"). A tier the clerk picks on
the second screen is their answer and stays.

## 5. Recognition aids

An option may carry `recognition_aid`, clerk-facing text in report vocabulary ("sheets of small round blue
cells", "starry sky"). A list in which any option carries one becomes select-then-confirm: a tap selects (bold,
aid shown beneath), Confirm advances. Lists with no aids stay one-tap.

This is a deliberate exception to standing rule 7. The 4 October ruling removed the always-visible grey
sub-line. The registrar confirmed on 6 October that text shown only after selection, from its own field, is
wanted. `coding_note` is never reused. Rule 7 and the memory note get a sentence recording the exception.

## 6. Referral hop

A `refer_group` terminal to a built group offers "Continue in Group N". It:

- keeps the case facts: topography, organ system, tissue origin, discriminator answers and the ticked
  documents; and the asserted basis of diagnosis;
- clears what the old tree read: stain results, workup, grade, entity, parked branches, alerts;
- records the hop as a trail entry that rewinds to the referral screen;
- routes through the receiving group's own `tree_routing` or tree selection, and does not apply the
  `candidate_groups` site check, because the referral establishes the group;
- keeps the original group-entry point, so "Suggested based on" still shows the evidence that led to the hop.

A referral to a group that is not built keeps today's terminal.

## 7. Evidence-gate conversion

All 28 evidence gates (Groups 1 to 10) gain a `tick_list` and per-option `ticks`. Agents proposed the mapping
and a second set re-derived it without seeing the first; disagreements are in
`docs/evidence_document_mapping.md` for the registrar. Group 10's file belongs to another session. Its mapping
is delivered as `docs/evidence_documents/group_10.json` and applied by `build/apply_evidence_documents.py`. The data
gate applies each mapping to a copy of its group file and fails where a mapped gate differs, so a tier's rule is
changed in the mapping, where the registrar can see it. Every tree-entry gate (seen through a laboratory screen)
must carry a tick list, whatever its label.

Haematology wording the registrar must confirm: blood film and marrow aspirate smear count as Cytology,
trephine biopsy as Histology Report, flow cytometry as Lab Report.

## 8. Verification

Data gate: the rules in section 4, run on every group, each proved with a broken input.
Engine gate: drives every evidence gate through Screen A and Screen B for all 128 tick sets; the Home button,
the filter, the recognition-aid confirm and the referral hop get fixtures. A browser walk covers Jay's
scenarios 4, 8 and 11. The merge with `feature/report-an-error` (parked) will conflict in `renderOutput` and
`outActions`; the handover names it.

## 9. Laboratory results (added the same day, from the Group 10 session)

A new `node_type`, `lab_results` (standing rule 6 permits one, with the validator, the engine gate and a negative
control). Decision Tree master §3I holds the schema. One screen, a row per test: a number as the report gives it, a
unit from the test's own closed list, and "Not in the file". The box starts empty; a row left without a number is
recorded as not in the file whether or not it is ticked, and ticking it also clears a number. The registrar chose the
closed list over a free-text unit: the group adds the typical units a report may use.

- The numbers are recorded and shown, and nothing reads them. They live in `state.labs`, never in
  `state.captured`, so no rule can use one. The node carries no key a code is chosen by; the data gate fails one that
  does.
- The result shows each test with its value and unit or "not in the file", on every terminal. The panel is one
  quiet trail entry and stays out of "Suggested based on". It survives a referral hop.
- A result in the panel ticks Lab Report on the evidence checklist that follows (`implies_ticks`).
- The screen offers no diagnostic escapes. A value that is not a number is refused on the row: digits with at most one
  decimal mark, so `0x1A`, `1e3`, signs and thousands marks fail. The error names the row, takes the focus and is tied to
  its box. The boxes are the clerk's own: a refused entry and a step back show them as they were left, and a blank row
  is recorded as not in the file without a box being ticked for it.
- A second panel replaces the tests it lists and keeps the rest. A unit held from another panel that this test does not
  list shows, and records, the test's own first unit. The trail entry is marked `typed`.
- The screen may be a tree's entry node, ahead of the evidence gate (the router accepts a `lab_results` entry whose
  `next_node` is a `document_inventory`). The express lane enters at the gate and skips it.

## 10. The unit sentence on a numeric gate

`numeric_gate` said "Check the report states the same denominator before entering the count" under every
reading, including a serum concentration. It now says "Check that the report gives the value in the same unit, and a
count over the same denominator, before entering it." A unit already carries its denominator ("per mm²" is not "per
10 HPF"), so one sentence serves counts, percentages and concentrations.

## 11. Embedding

The tool is embedded in a frame inside another page, and that is the only relationship it has with it. So nothing
this work adds opens a browser dialog (the "Leave this case?" question is a bar, not `confirm()`), opens a window,
uses browser storage, or scrolls any page but its own (no `scrollIntoView()`). The engine gate fails if one of those
appears in `app.js`. The `window.prompt` calls of the older override handler are the only dialog left; the parked
"Report an error" branch removes them.


## 12. Review of the same day

Seven independent reviews of the built work found these, all fixed and each with a check that fails when the fix is
removed (`docs/ux_negative_controls.md`):

- Stepping back across a referral hop left the receiving group's file loaded, so the first group's screen did not draw;
  `hopFrom` was not in the snapshot, so a step back to the tree question dropped the evidence from "Suggested based on";
  the app bar named the group left. A second tap on "Continue in Group N" while the file loaded sent the case to an
  error screen. A hop into a group that routes its trees by site, with no site on the case, entered its default tree in
  silence; no hop is offered there.
- Home on a failed start reset to a page with nothing to draw.
- The lab "Not in the file" boxes came back ticked after a refused entry or a step back.
- The filter could hide the selected row, and Confirm still recorded it.
- A checkbox, radio or select change dropped the keyboard focus; the leave bar could not be reached or dismissed by
  keyboard; a lab error showed no focus and no link to its box; groups had no names; Enter in an empty filter box
  answered the question; the touch targets were small.
- The engine gate never ran `render()` or the listeners. It now draws screens into a stand-in page and boots the real
  engine against the data on disk to fire the listeners.

What the review found and this work leaves to the registrar (`docs/TODO.md` §28): the evidence checklist inherits each
option's captures, so a Lab Report tick is read as flow cytometry and a tier that says "and/or IHC" credits both; a file
with no option that describes it (imaging only, flow report only, cytology without tissue, an aspirate and trephine
without IHC) takes the nearest lower tier, whose sentence can deny a ticked document. The mapping lists each as a data
gap.
