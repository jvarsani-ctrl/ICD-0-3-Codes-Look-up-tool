# Walk-through examples on the landing page

Written 20 October 2026, at the registrar's request. The landing page shows five buttons
just below the tool. Each plays a made-up case through the real engine, one decision at a
time, with a caption saying what the tool is doing.

## What the page does

- **Where it shows.** Below the tool, on the landing screen only. A case in progress is never
  replaced: the buttons come back when the clerk returns to the landing screen. It does not
  show when the page is embedded (`?host=redcap`), because a clerk filling a form has no use
  for a demo and the frame has no room for one.
- **The player.** Pressing a button opens a bar pinned to the foot of the window with the
  made-up file, a caption, **Next step**, **Play all** (and **Pause**) and **Close**. The tool
  above is driven by clicking its own controls, so what the audience sees is the tool.
- **Taking over.** Close leaves the case where it is, and the clerk continues by hand. If the
  tool no longer matches the recording, the player stops and says so, and offers **Watch
  again**.
- **No clinical content in `app.js`.** The player is `demo.js`, the cases are
  `data/shared/demo_walkthroughs.json`, and `app.js` is untouched. `demo.js` reads the engine's
  `state.stage` and calls its `reset()` and `render()`, and nothing else.

## The five cases

| Case | Group | What it shows |
|---|---|---|
| B-cell acute lymphoblastic leukaemia with BCR::ABL1 | I | Four tests ticked, genetics read, lineage markers typed in, subtype named: 9812/3 |
| Myeloid leukaemia in a child with Down syndrome | I | Trisomy 21 sends the case to its own workup; age in months decides: 9898/3 |
| ALK-positive anaplastic large cell lymphoma | II | Enters from the diagnosis in the file ("Confirm existing diagnosis"); marrow gate; one marker at a time: 9714/3 |
| Rhabdoid tumour of the kidney | VI | Loss of one protein fits two tumours; age and sickle-cell status decide: 8963/3 |
| Mediastinal germ cell tumour with no tissue | X | Typed laboratory values, a code without tissue, the workup status: 9065/3 |

Every case is made up. No patient data is used, and none may be added.

## Recording a case

A case is a made-up file (`file`), a list of **beats**, and what it must reach (`expect`). A
beat is one decision: the clicks that make it (`do`) and a caption (`say`) that describes what
the tool did. The caption is shown after the clicks run.

A step names a control by what is on the screen, never by position:

```json
{"act": "opt", "text": "Lymphoid blasts"}
{"act": "markerset", "attrs": {"m": "CD19", "v": "pos"}}
{"act": "draft", "text": "Marrow blast percentage", "type": "82"}
{"act": "tick", "text": "Flow cytometry"}
{"act": "labunit", "attrs": {"i": "0"}, "value": "ng/mL"}
```

`act` is the control's `data-act`. `text` matches the control's visible text as a substring
(an exact match wins over a longer one) and must name exactly one control. `attrs` match
`data-` attributes exactly, written without the prefix. `type` types into a box and `value`
sets a select. Zero or several matches stop the replay, so a renamed option fails the build
instead of replaying a different answer.

To record a new case, walk it through the real tool first, noting each control, then write the
steps. `expect` names the code and behaviour the engine must reach, text the output screen must
carry, and anything typed or chosen that the code does not depend on (`trail`, `workup`). A
typed figure that never registered leaves the code unchanged, so the code alone proves nothing
about it.

Never write a code into a case from memory. The code comes from the engine, and the build
verifies every code in the data against Layer 1 as it always has.

## The gate

```bash
node build/check_demo_walkthroughs.mjs
```

Run by `python3 build/build_database.py` (section F) and by the GitHub pull-request check. It
replays every case through `app.js` and the data on disk, using the player's own matcher
(`PedsDemo.pick` in `demo.js`), and fails unless each case ends on its output screen with the
promised code, behaviour, topography, typed figures and workup status. It also checks the page:
every element `demo.js` looks up must exist in `index.html`, because a missing id hides the
section without an error. Negative controls: `docs/demo_walkthroughs_negative_controls.md`.

`build/demo_driver.mjs` is the headless driver the gate uses. It fires each step through the
same delegated listeners the page registers.

## Not covered by any gate

The player's pacing, the highlight ring and the layout of the bar are checked by driving the
page in a browser, not by the gate. After changing `demo.js` or the styles, play at least one
case to the end, close one mid-way, and open the page at phone width.
