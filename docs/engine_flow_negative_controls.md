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
