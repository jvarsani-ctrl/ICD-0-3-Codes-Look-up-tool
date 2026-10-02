# ICCC-3 / ICD-O-3 Lookup Tool

Workstream E of the UCI / UCCF Paediatric Cancer Registry. This file holds the
standing rules for this repository, and following them needs nothing outside it.

## Where the inputs live

This repository is one part of a larger registry vault. Two inputs live beside
it in that vault and are deliberately not versioned here, because the sync layer
that carries the vault corrupts git internals.

| Input | Path | In a standalone clone |
|---|---|---|
| Memory router and its concern files | `../CLAUDE.md`, `../memory/*.md` | absent |
| Layer 1, the code source of truth | `../../ICD coding/` | absent |

**When this checkout sits in the registry vault**, those documents are
authoritative for design, engine, data, nodes and REDCap output. Read the router
before changing any of them.

**In a standalone clone they are absent, and that is expected — it blocks
nothing in this file.** `README.md` and `docs/` carry the same decisions: the
three rules and the registrar's thirteen rulings in `README.md`; the per-group
build contracts, build reports, baseline documents and negative controls in
`docs/`. The tool itself runs with no build step and no vault — see "Run it".

`build/build_database.py` is the one thing that does need Layer 1. Without it the
preflight stops and says so. That is the gate working, not a fault to route
around: no morphology code can be verified when the source of truth is absent.

## Standing rules

These apply to every session and every subagent working in this repository.

1. **Never fabricate a morphology code.** Verify against Layer 1 — the ICCC-3
   tables, `icdo32.sqlite`, `ICCC-2017.sqlite` and the REDCap option strings,
   at `../../ICD coding/` when the vault is present. A code that cannot be
   verified stops the work and goes to the registrar. The build fails on an unverifiable code by
   design — do not route around it.
2. **The tool codes to ICD-O-3.2.** ICD-O-4 is out of scope: no five-digit
   codes in the data, no migration TODOs, corroboration at most.
3. **ICCC-2017 is the grouping convention only.** It predates ICD-O-3.2, so a
   valid code outside every range still belongs to its major group. Only a code
   ICCC places in a different group is a conflict.
4. **Jay is the registrar.** Their ruling settles any coding conflict. The
   thirteen rulings of 4 September 2026 are in `README.md`, which is in this
   repository, and in full in `../memory/registrar-rulings.md` when the vault is
   present: ICCC ranges govern, the latest document wins, and the tool shows no
   warnings.
5. **Never put clinical logic in `app.js`.** No codes, no marker names, no
   `if (group === X)`. Anything that varies by group lives in the JSON. A new
   kind of question is one new `node_type`, not a group-specific branch.
6. **`node_type` is a closed vocabulary.** A group may use any subset. None may
   invent a type: validation rejects unknown types and the engine throws.
7. **Author-facing text stays out of the UI.** `coding_note` and
   `topography_routing_note` are for whoever builds the JSON. Clerk-facing text
   belongs in `reason`, `hint` or `clinical_alert`.
8. **The tool is advisory and must never overstate its evidence.** Every defect
   that reached the browser made a case look better evidenced than it was. Test
   that class of fault first. The abstractor confirms every code.
9. **The tool is global, not LMIC-specific.** UCI is one site among many. A
   site profile is a template anyone fills in, never UCI's inventory.
10. **Prove every check with a negative control.** Break the data or the code on
    purpose, watch the check fail for the right reason, restore, watch it pass.
    Key a check off the source of truth, never off a flag in the thing being
    checked. A check that tests a destination rather than a condition passes
    while the engine never reads the branch at all.
11. **A green data build is not a working tool.** `build_database.py` validates
    the data; `check_engine_flow.mjs` drives the engine. The defects that forced
    the engine gate into existence sat in the seam between them. Drive the UI
    before believing a pass.
12. **Build every part before verifying.** Finish the whole piece, then verify
    once. Per-part checks spend time on failures a later part removes.
13. **Several sessions share this working tree.** Run `git status` before
    editing, and pin negative controls to a pre-fix commit, never `HEAD`. A
    parallel agent gets its own git worktree and branch under `.claude/worktrees/`.
14. **Write plain declarative prose** in docs, comments and commit messages: no
    hedges, no intensifiers, no throat-clearing. Cite the paper and the page
    ("cIMPACT-NOW update 8, p. 1142") and use full forms, never bare acronyms.
15. **Commit the generated alias index.** `data/aliases/alias_index.json` is
    produced by the build but is tracked on purpose: deployment is GitHub Pages
    serving this repo with no build step, and `app.js` falls back to `{}` on a
    missing index — so an untracked index makes express-lane search return
    nothing for every term, silently.

## Before you push

```bash
python3 build/build_database.py
```

One command: preflight, then the data gate, then the engine gate. Preflight
reports every missing requirement at once. Node.js is required and the engine
gate is never skipped when it is absent — registrar's decision, 23 September
2026. A gate that skips an absent tool returns a green build that checked
nothing.

While iterating on `app.js`, run the engine gate alone:

```bash
node build/check_engine_flow.mjs
```

Negative controls for it are in `docs/engine_flow_negative_controls.md`.

## Run it

```bash
python3 -m http.server 8811
```

No build step and nothing to install: `index.html`, `app.js`, one stylesheet.
That dependency-free property belongs to the tool and is load-bearing. The
gates above run outside the browser and do not touch it.

## Branches

One branch per ICCC group — `group-03-cns`, `group-04-neuroblastoma`,
`group-05-retinoblastoma`, `group-06-renal` — merged to `main` when the group's
build report and code verification are done. Released states are kept as
`archive/vN.N-YYYY-MM`.
