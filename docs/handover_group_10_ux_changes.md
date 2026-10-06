# Handover to the Group 10 session: the interface changes of 6 October 2026

**From** the "ICD Overall fixes" session, branch `claude/overall-fixes-ux`. **To** the Group 10 session
(`claude/group-10-tumor-pathway-3a99f7`), and to anyone merging the two.

The registrar approved your engine requests of 6 October 2026 and they are built here, together with the changes
that came out of the registrar's hand review of Group 10. Group 10's data files were not touched. The registrar
asked that nothing be sent to the Group 10 session and will hand this document over.

## What you must do after you merge `main` into your branch

1. **Apply the evidence checklist to your four gates.** The registrar replaced the single-choice "What is in
   the file for this tumour?" with seven document checkboxes. The data gate now fails any node labelled
   "Evidence in file" that has no `tick_list`. For `cn_`, `ov_`, `ts_` and `eg_document_inventory`:

   ```bash
   python3 build/apply_evidence_documents.py data/database/group_10_dt.json docs/evidence_documents/group_10.json
   ```

   The script is idempotent and refuses to touch an option whose label no longer starts as it did on 6 October
   (the mapping was made against `c8e9a0a`), so reorder or reword nothing in those four gates before you run it.
   If it refuses, re-derive that option's rule by hand from `docs/evidence_document_mapping.md`. It also refuses a gate
   whose hint or question was changed since the mapping was made, because applying would overwrite the change.
   Once your group file holds the ticks, the data gate compares each mapped gate with `docs/evidence_documents/group_10.json`
   (`check_evidence_mapping`) and fails where they differ. Until you apply it, that check and the "evidence gate with no
   `tick_list`" check name the four gates. Change a tier's rule in the mapping, then re-run the script.
2. **Re-run your scenarios.** Click paths change in three places:
   - the evidence step is now "tick the boxes, then Continue" (a second question appears only when two or more
     tiers fit);
   - scenarios 4 and 5 (benign teratoma, juvenile granulosa cell tumour) now end on a result block that prints
     `9080`, `/0 (Benign neoplasm)` and `569 (Ovary)` instead of "No code emitted here";
   - scenarios 8 and 11 end on a referral screen with a **Continue in Group N** button, and the hop replaces
     "Start new case -> search".
3. **Set `built: true` for Group 10** in the router when your tree is ready. A referral from another group to
   Group 10 then offers the hop.

## The laboratory screen: the final schema

Jay's decisions of 6 October, built as a new `node_type`, `lab_results` (Decision Tree master §3I). It records
numbers and chooses no code. Place it as the entry node of each of the four trees: the router's `entry_node` names the
`lab_results` node and its `next_node` names the evidence gate that is now the checklist. The data gate accepts that
and only that: a laboratory entry whose `next_node` is not a `document_inventory` fails, and the gate behind the screen
must carry its tick list.

```json
{ "node_id": "ov_labs", "node_type": "lab_results", "step_label": "Laboratory results",
  "question": "Which laboratory results are in the file?",
  "hint": "Enter each number as the report gives it, with its unit. Leave a test the file does not hold empty.",
  "labs": [ { "id": "afp", "label": "Alpha-fetoprotein (AFP)", "units": ["ng/mL", "IU/mL", "kU/L"] }, ... ],
  "implies_ticks": { "vocabulary": "evidence_documents", "ids": ["lab"] },
  "next_node": "ov_document_inventory", "nos_fallback": null }
```

- `labs[].units` is a **closed list the clerk chooses from. There is no free-text unit.** Jay's instruction was to
  add the other typical units as options, so list every unit a report may use for that test, from the sources you
  already cite (van Heerden and Tjalma 2019, Table 4; Rajpert-De Meyts 2015). The build refuses an empty or
  repeated unit list; it cannot check that a unit is right.
- `implies_ticks` ticks Lab Report on the checklist when at least one result is entered.
- The node carries no `options`, `resolution_logic` or terminal keys, and the build fails if it does: a value
  never chooses the code. Lab `id`s must not be captured variables or `when` keys in the file.
- The result screen lists each test with its value and unit, or "not in the file". The panel is not in "Suggested
  based on". The no-tissue routes keep coding on the report's own word "raised".
- The "denominator ... count" sentence on a `numeric_gate` was reworded for every kind of unit ("Check that the
  report gives the value in the same unit, and a count over the same denominator, before entering it."). The new
  screen does not use a `numeric_gate`. Your `UNIT_LABELS` additions (`ng_per_ml`, `iu_per_l`) and the three
  `tokenLabel(UNIT_LABELS, ...)` calls are not in this branch, so they will merge in without overlap.
- The parked "Report an error" feature must leave the values out of an email: they are patient data, and typed
  numbers are the case its free-text rule exists for. The trail entry is marked `typed: true`, which is the flag that
  branch already prints as "[typed text omitted]".
- A result is digits with at most one decimal mark. `units` is scanned for field names like any clerk-facing text.

## What is new for your data

| Feature | Field | Use in Group 10 |
|---|---|---|
| Recognition aid | `recognition_aid` on an option | The explanation in report vocabulary for the histology lists ("sheets of small round blue cells"). Shown only under the selected option; the list becomes select, then Confirm. Clerk-facing prose, never `coding_note`. |
| Tick list, first match | `tick_list` on the node and `ticks` on each option | The four `*_mixed` nodes. Example below. |
| Referral hop | none | A `refer_group` branch to a built group offers the hop with no data change. |

```json
"tick_list": { "resolve": "first_match", "variable": "mixed_components", "label": "Components",
  "prompt": "Tick every component the report lists.",
  "items": [ { "id": "choriocarcinoma", "label": "Choriocarcinoma" }, { "id": "embryonal", "label": "Embryonal carcinoma" },
             { "id": "teratoma", "label": "Teratoma" }, { "id": "seminoma", "label": "Seminoma, germinoma or dysgerminoma" } ] },
"options": [
  { "label": "Choriocarcinoma is among them", "ticks": { "requires": ["choriocarcinoma"] }, "morphology_code": "9101", ... },
  { "label": "Embryonal carcinoma and teratoma only", "ticks": { "requires": ["embryonal", "teratoma"], "excludes": ["choriocarcinoma", "seminoma"] }, ... },
  { "label": "Anything else", "ticks": {}, ... }
]
```

The first option, in file order, whose rule fits the ticked set is the destination. Keep a final option with
`"ticks": {}` as the fallback. The data gate enumerates every ticked set: one that fits no option fails, and so
does an option that is never the first fit for any set (a shadowed rule). Rules and the proof are in
`docs/superpowers/specs/2026-10-06-ux-overall-fixes-design.md` §4 and `docs/ux_negative_controls.md`.

## What changed in the engine, for everyone

- **Result block.** Name, Morphology code, Behavior code (`/N (meaning)`), Topography code (the ICD-O code without
  its letter and point, then the ICD-O name: `569 (Ovary)`), Suggested based on. Benign and behavior-excluded terminals print their code.
- **Home** button on every screen once a case is open; it asks first when there are answers.
- **A filter box** on every single-choice list, and the organ-system list also matches region names.
- **The interface says "Behavior".** About 260 clerk-facing sentences in the group files still say "behaviour";
  they are swept later, not by you now (`docs/TODO.md` §28).

## Merge conflicts to expect

`feature/report-an-error` (parked) rewrites `outActions()` and the override handler; this branch does not touch
either. Both change `renderOutput()`: this one replaces the headline and the Behaviour, Topography and
Based-on rows with `codingBlock()`. Take this branch's rows and keep that branch's buttons.

A trial merge of the two `app.js` files conflicts in five places: the `state` literal, `restore()`, the `advance()` signature
and the `pushTrail` call in it, and `reset()`. Take the union. This branch adds `focusNext` and `hopFrom` to the state
(`hopFrom` is in `snapshot()`), restores the group file in `restore()`, and clears `confirmExit`, `hopFrom`, `labs`
and `focusNext` in `reset()`. Also clear `state.report` in `hopToGroup()`: otherwise the "Error reported" banner and the open
panel of the first group show on the receiving group's result.

## What the review of 6 October found, for the registrar

Seven reviewers read the built work. Everything in the engine and the checks is fixed (spec section 12). These need the
registrar, and the Group 10 gates have the same shape:

- **Lab Report is read as flow cytometry** where the old option says so, and a tier worded "flow cytometry and/or IHC"
  credits both tests, because each option keeps its captures. A Lab Report that is only a blood count lifts the tier.
- **A file no option describes** (imaging only, a flow report only, cytology without tissue, an aspirate and a trephine
  without IHC, a lone marker result) takes the nearest lower tier. Its sentence can deny a document that is ticked. The tool
  now leaves that sentence out of "Suggested based on". The gap is closed only by new options, which are the registrar's to
  word; `docs/evidence_document_mapping.md` lists each as a data gap.
- **IHC beside morphology** now reaches the "flow and/or IHC" tier of Group I's acute and mature-lymphoid gates, through added
  copies of the tier that credit no flow cytometry. The mds gate has no such copy: a trephine with IHC and no aspirate takes the
  aspirate tier.
