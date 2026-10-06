# ICCC-3 Lookup Tool

An **advisory** decision tool for the UCI / UCCF paediatric cancer registry. It helps a data
abstractor turn the clinical language in a patient file into a standardised ICD-O-3
morphology code, mapped to an ICCC-3 subgroup, ready for manual entry into REDCap.

**The tool does not write to REDCap.** It displays the answer; the clerk selects the matching
option by hand. Every screen carries the line *"Advisory only — the abstractor confirms every
code."*

This repository is the implementation. The specifications and the code source of truth live
in the registry vault one directory up. See "Working outside the registry vault" for what
this repository does without them.

---

## Run it

No build step, no dependencies, no `npm`. It is static files.

```bash
python3 -m http.server 8811
```

Then open <http://localhost:8811>. Deployment is GitHub Pages on push to `main`.

### URL flags

Two flags, deliberately **orthogonal** — do not merge them.

| Flag | Decides | Driven by |
|---|---|---|
| `?mode=rail\|transcript` | Shell layout — overrides the 880px breakpoint | available width |
| `?host=redcap` | Output-block framing | who is reading |

`?mode=` is load-bearing, not a testing convenience: on a 1440px screen the REDCap form region
is ~1000–1050px, over the breakpoint, so width alone would wrongly give REDCap the rail. The
iframe src carries `?host=redcap&mode=transcript`.

---

## Working outside the registry vault

This repository is one part of a larger registry vault. Two inputs live beside it there
rather than in git, because the sync layer that carries the vault corrupts git internals.

| Input | Path in the vault | In a standalone clone |
|---|---|---|
| Layer 1 — ICCC-3 tables, `icdo32.sqlite`, the REDCap option strings, and `ICCC-2017.sqlite` beside it | `../../ICD coding/` | absent |
| Project map and the ratified decisions | `../CLAUDE.md`, `../memory/*.md` | absent |

A standalone clone can:

- **Run the tool.** Nothing to install, no build step, no vault — see "Run it".
- **Run the engine gate.** `node build/check_engine_flow.mjs` reads only `app.js` and
  `data/`, and sweeps every built group.
- **Read the decisions.** `CLAUDE.md` holds the standing rules, this file holds the three
  rules and the registrar's rulings, and `docs/` holds the per-group build contracts, build
  reports, baseline documents and negative controls.

It cannot run `build/build_database.py`, which verifies every morphology code against Layer 1.
No code can be verified when the source of truth is absent, so preflight stops and lists every
missing requirement at once. That is the gate working, not a fault to route around. Point it
at Layer 1 wherever it sits:

```bash
python3 build/build_database.py --layer1 "/path/to/ICD coding"
```

```bash
export ICD_LAYER1="/path/to/ICD coding"
```

With neither given the default is `<repo>/../../ICD coding`, which is correct when the
checkout sits in the vault.

## Layout

```
index.html          single entry point
app.js              the engine — ONE file, identical logic for all 12 groups
uccf-tool.css       one flattened stylesheet: tokens + corrections + primitives
assets/             UCCF mark and wide lockup
data/
  database/         group_NN_dt.json — morphology_entries[] + decision_trees[]
  aliases/          aliases_group_NN.json + the generated alias_index.json
  shared/           presentation_router.json, topography_codes.json
build/
  build_database.py regenerates alias_index.json and validates everything
```

## The four layers — never inverted

```
LAYER 1  ../../ICD coding/  ICCC-3 tables + the REDCap option strings   read-only truth
         vault-side; override with --layer1 or $ICD_LAYER1
LAYER 2  data/database/group_NN_dt.json     morphology entries + trees
LAYER 3  data/shared/ + data/aliases/       routing and alias JSON
LAYER 4  app.js                             one group-agnostic engine
```

## The three rules

1. **Never fabricate a morphology code.** Verify against Layer 1; if it cannot be verified,
   stop and flag it. The build fails on an unverifiable code — by design.
2. **Never put clinical logic in `app.js`.** No codes, no marker names, no `if (group === X)`.
   Anything that varies by group lives in the JSON. A new *kind* of question is one new
   `node_type` in the engine, not a group-specific branch.
3. **`node_type` is a closed vocabulary.** A group may use any subset; none may invent a type.
   Validation rejects unknown types and the engine throws on one.

## Before you push

```bash
python3 build/build_database.py
```

One command. It now runs **two** gates and a preflight, in that order.

**Preflight.** Every external requirement is checked before anything else, and **all of
them are reported at once** — a gate that dies on the first missing thing sends you away
to install it, come back, and be sent away again. Nothing else runs until they are
satisfied, because a partial run reports green sections that were never exercised.

| Requirement | Why |
|---|---|
| Python 3.9+, `sqlite3` | the gate itself |
| Layer 1: `RedCap Options`, `icdo32.sqlite`, `ICCC-2017.sqlite` | the source of truth every code is verified against |
| **Node.js** | the engine gate below |

**The engine gate.** `build/check_engine_flow.mjs` loads the shipped `app.js` and drives
it. It is JavaScript because `app.js` is — testing the engine means running it — and it is
**the only thing in this repository that tests `app.js` at all**. `build_database.py`
validates the DATA; this drives the ENGINE; the defects that forced it into existence sat
in the seam between them, where the data was correct, every data check passed, and the tool
still told a clerk one code and recorded another. A green data build is not a working tool.

**Node.js is required, and the gate is never skipped when it is missing.** Registrar's
decision, 23 September 2026. A gate that silently skips an absent tool returns a green
build that checked nothing, which is how these defects shipped in the first place. The
dependency-free property that is actually load-bearing belongs to the **tool** —
`index.html`, `app.js`, one stylesheet, no build step, nothing to install to run it — and
that is untouched. Nothing here runs in the browser.

Run the engine gate alone while iterating on `app.js`:

```bash
node build/check_engine_flow.mjs
```

See `docs/engine_flow_negative_controls.md`.

All data checks must pass. `--strict` also promotes warnings to failures. The gate covers
decision-tree integrity, the NOS-fallback rule *by node type*, the closed node vocabulary,
cross-layer references, and the checks that exist because their absence would be invisible:

- **exact-string match** of every `morphology_name` to the REDCap option string — the clerk
  matches on the whole string, so drift between the tool and the options file breaks the
  advisory model itself;
- **raw-hex ban** — no colour outside the `:root` token block in `index.html`, `app.js` or
  `uccf-tool.css`;
- **cryptic-genetics lint** — a cryptic terminal must never be reachable only through a
  normal-karyotype branch. Valid JSON, clinically wrong;
- **rule-ordering lint** — inside every `resolution_logic[]`, rules carrying a `when` must
  precede unconditioned ones, because first match wins.
- **`satisfies_tests` guard** — that field suppresses an outstanding-workup row, so it is the
  one field that can make a case look better worked up than it is. A typo never matches (the
  suppression quietly does nothing); a value the code does not require is an inert no-op that
  still reads as a live claim.
- **`outstanding_tests` guard** — the reverse field: a branch names tests its finding leaves owed,
  which `app.js` adds to the outstanding-workup rows. Same closed vocabulary; it must sit on a
  code-emitting branch and never repeat a value from `satisfies_tests`.
- **`non_reportable_heading` guard** — a non-reportable terminal may name what the lesion is
  ("Benign neoplasm (benign tumour)") in place of the generic banner; the field must sit on a
  `non_reportable` branch and be a non-empty string, or `app.js` silently ignores it.
- **`refer_group` shape** — a referral must name a different ICCC-3 group, carry no
  morphology code, and put its clerk-facing text in `reason` (`coding_note` is not rendered).

The engine gate adds two invariants of its own, swept across every `ihc_checklist` node in
every group: a stopped flow may not leave a marker unasked that could still satisfy a live
rule, and what the screen says at that stop must equal what Continue records.

Every check is proved with a **negative control** — break the data, watch it fail, restore.
For the engine gate the same method runs against a copy of a pre-fix `app.js` via
`APP=<path>`, because a check only ever proved against code that passes has not been
proved at all.
No REDCap flag is kept in the data (standing rule 16, 4 October 2026). Before that, a flag
authored to mean "not yet checked" was once read as "exempt", and six drifted names passed a
green build; checks key off Layer 1, never off a flag in the file being checked.

## Status

**Groups 1 to 10 are built and passing.** `data/database/` carries `group_01_dt.json` through
`group_10_dt.json` with an alias file for each. The router declares Groups 11 and 12
`built: false` and the tool says "not yet available" rather than throwing. Each group from 7 on
has its build report in `docs/`: `group_07_build_report.md` (hepatic tumours, open questions in
`group_07_open_questions.md`), `group_08_build_report.md` (malignant bone tumours) and
`group_09_build_report.md` (soft tissue sarcomas, registrar questions in
`group_09_registrar_questions.md`) and `group_10_build_report.md` (germ cell, trophoblastic and
gonadal tumours, registrar review in `group_10_registrar_review.md`).
`python3 build/build_database.py` reports `BUILD PASSED`.

Group 1's 15 `refer_group` branches resolve — building Group II cleared that debt.

When this checkout sits in the registry vault, `../CLAUDE.md` holds the project map and
`../memory/` the ratified decisions behind every choice here. In a standalone clone both are
absent, and `CLAUDE.md` and `docs/` carry the same decisions.

## The 4 September 2026 registrar rulings

Jay ruled on the twenty problems in the Group II review. The binding text is in
`../memory/registrar-rulings.md` when the vault is present; what follows is what changed in
this repository, and stands on its own without it.

**The checklist is a flow chart (ruling 13).** A node of type `ihc_checklist` used to show
every marker it knew about and evaluate an ordered rule list against whatever was ticked.
Two consequences followed from that shape and neither was visible on screen: a rule whose
conditions are a subset of an earlier rule's could never fire, and the clerk saw every code
the node could reach with nothing saying which were still in play.

`build/induce_flow.py` now induces, per node, the order its markers should be asked in, and
writes it into the node as `branch_sequence`. The engine asks one marker at a time in that
order, skips any question that can no longer change the answer, and stops as soon as the
first still-live rule is satisfied outright. The order is clinical content and lives in the
JSON; the narrowing is arithmetic on rules the engine already evaluates.

The same script proves every rule is reachable by constructing a witness — an answer vector
under which that rule, and no earlier one, matches. A rule with no witness is a build
failure. Three real dead rules turned up on the first run and are fixed:

- `g2hist_lch_confirm`: the "langerin not done" provisional sat *below* the rule that reads an
  absent langerin as a negative, so a case where the stain was never done was being called an
  indeterminate dendritic cell tumour — a definite diagnosis from a missing test.
- `mds_rcc_aplastic_ihc` and `g2hist_lch_confirm`: a bare catch-all below a rule that already
  covered every remaining case. Merged.

**A marker can now be answered "not done or not readable"** (ruling 11). It matches exactly as
an absent marker does, so no rule changes meaning; the difference is that the clerk said so,
and the answer block names it.

**Warnings left the tool** (ruling 9). `app.js` no longer renders `clinical_alert` and neither
group file carries the text. All 302 strings are in `docs/clinical-warnings.md` with the exact
place each came from.

**The answer always names the code's aliases** (ruling 6), on every path.

**Codes are built ahead of REDCap** (rulings 1-3), for example Group II's `9715` ALCL ALK
negative, `9749` Erdheim-Chester disease and `9819` B lymphoblastic leukemia/lymphoma
BCR-ABL1-like. The tool does not verify REDCap (standing rule 16): the data carries no REDCap
flag, the output shows no REDCap banner, and what REDCap owes is listed in `docs/TODO.md` §7.
Every code is verified against the ICCC-2017 classification or the IARC ICD-O-3.2 table,
converted to `icdo32.sqlite` inside Layer 1 (`../../ICD coding/ICD-O-3.2/` when the vault is
present).

**9754 is retired** (ruling 8). ICD-O-3.2 does not list it; the REDCap row for it carries
9751's name and 9751's change note. LCH resolves to 9751 with the behaviour split.

## Routing: the tool narrows to a family, it does not ask for one

Until 4 September 2026 the presentation stage ended with **"Which family does this case belong
to?"** — the question the tool exists to answer, put to a clerk who cannot answer it. It fired
for six of the seven presentations, because nothing narrowed the candidates: `afterDiscriminator`
read the archetype's advisory list and rendered it.

Three facts were already in the data and none was consulted. `site_to_group` appeared in
`app.js` only inside a comment. `dual_group_rules` ran once, at a terminal, though the router's
own note says it belongs at "Moment 1, before any tree loads". And `candidate_groups` on two
archetypes was the string `"all"`, which `arr()` reads as an empty list — so *Incidental imaging
finding* and *Not sure / mixed presentation* failed outright with "No candidate group for this
presentation."

The stage is now **origin → organ system → region → family**, and the family is derived:

- The presentation gives an advisory candidate list.
- The tissue-origin question is asked **first**, and each answer declares what it rules out
  (`discriminators[…].narrows`) — bone origin drops Group IX, soft tissue drops Group VIII.
- The organ system is asked next, with the systems matching that origin listed first and the
  rest still available: an abdominal mass is soft tissue and may still be renal or hepatic.
- The region is a second tap, and it records the actual topography code. It used to record
  `codes[0]` for the whole row — so "bone" always recorded `C40.9`, and "soft tissue" always
  recorded `C47.9`, the autonomic nervous system, for a rhabdomyosarcoma of the thigh.
- The topography's own `candidate_groups` intersects what is left. One survivor and the tool
  enters that group without asking.

Seven of eight test paths now derive a single group. The one that does not is a paravertebral
abdominal mass at `C47.4`, which is genuinely Group IV or Group IX — presentation and site
cannot separate neuroblastoma from a nerve sheath sarcoma, and the tool says so instead of
guessing.

**Layer 1 has twenty-one soft-tissue topography codes; the crosswalk carried two.** All of
C47, C48 and C49 are now in `topography_codes.json`, grouped into three systems — peripheral
nerves and autonomic nervous system, connective and subcutaneous soft tissues, retroperitoneum
and peritoneum — each with its nine or three regions. `C48` was absent entirely, so a
retroperitoneal mass had nowhere to go.

`check_routing_narrows` in the validator holds this together: no `candidate_groups` may be
anything but a non-empty list of real groups, every crosswalk code must resolve in the lookup,
every organ system needs a clerk-facing label, and every discriminator needs a clerk-facing
question, hint and option labels. The discriminator screen used to print `settles` — "Group
VIII vs Group IX split for 9260 (Ewing sarcoma family). See dual_group_rules." — at the
abstractor.
