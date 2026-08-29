# ICCC-3 Lookup Tool

An **advisory** decision tool for the UCI / UCCF paediatric cancer registry. It helps a data
abstractor turn the clinical language in a patient file into a standardised ICD-O-3
morphology code, mapped to an ICCC-3 subgroup, ready for manual entry into REDCap.

**The tool does not write to REDCap.** It displays the answer; the clerk selects the matching
option by hand. Every screen carries the line *"Advisory only — the abstractor confirms every
code."*

Specifications live one directory up, in `../`. This repository is the implementation.

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

All checks must pass. `--strict` also promotes warnings to failures. The gate covers
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
- **`refer_group` shape** — a referral must name a different ICCC-3 group, carry no
  morphology code, and put its clerk-facing text in `reason` (`coding_note` is not rendered).

Every check is proved with a **negative control** — break the data, watch it fail, restore.
The exact-string check is keyed off Layer 1, never off `redcap_option_verified`: a flag
authored to mean "not yet checked" was once read as "exempt", and six drifted names passed a
green build.

## Status

Group 1 (Leukaemias) is built and passing: 84 morphology entries, 4 trees, 97 nodes, 283
aliases, 32 checks green. Groups 2–12 are declared in the router as `built: false`; the tool
says "not yet available" rather than throwing.

Group 1's 15 `refer_group` branches point at a Group II that does not exist, so leukaemic
Burkitt currently lands nowhere — building Group II clears that debt.

See `../CLAUDE.md` for the project map and `../memory/` for the ratified decisions behind
every choice in this repository.
