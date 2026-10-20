# Negative controls: the walk-through gate

Run 20 October 2026 against `build/check_demo_walkthroughs.mjs`. Per standing rule 10 and the
13 October 2026 ruling, only the controls that could pass for the wrong reason are written. A
renamed option, a deleted step or a wrong expected code each fail by their own name, and are
not run.

Each control breaks a scratch copy and leaves the real files alone. The engine controls use
`APP=<scratch copy of app.js>`, which `build/demo_driver.mjs` reads.

## C1. A typed number is lost in the engine

**Why it could pass for the wrong reason.** A blast percentage or an age that never reaches the
engine still lets the case reach its code, because the tree has a "not documented" route to the
same outcome. Case 1 reached 9812/3 with no blast percentage recorded, the first time the
driver failed to type it.

**Break.** In the `draft` handler of a scratch `app.js`, skip storing the key `value`.

```
APP=<scratch> node build/check_demo_walkthroughs.mjs
```

**Result.** 8 of 53 checks fail. Case 1 still reaches 9812/3, and the one check that fails is
`the screen reads "82% → >=20"`, which is the check this control exists to prove. Cases 2 and 4
stop on a screen that asks for the age. Restoring the real engine: 59 of 59 pass.

## C2. Choosing a unit clears the typed laboratory value

**Why it could pass for the wrong reason.** The recording types the value, then picks the unit.
An engine that clears the value on a unit change still lets case 5 reach 9065/3 through the
imaging answer, with the laboratory result missing from the case.

**Break.** In the `labunit` branch of a scratch `app.js`, also set `row.value = ''`.

**Result.** 1 of 59 checks fails, and it is `the trail holds "Alpha-fetoprotein (AFP) 1850
ng/mL"`. The code, behaviour and topography checks all pass. This is the only check that sees
the loss.

## C3. The page loses an element the player looks up

**Why it could pass for the wrong reason.** `demo.js` fails silently when its data or its
markup is missing, so that a broken demo never breaks the tool. The cost is that a missing id
hides the whole section with no error anywhere. No replay check sees it, because the replay
does not use the page.

**Break.** In a scratch copy of the repository, rename `id="demos-list"` in `index.html`.

**Result.** 1 of 59 checks fails: `demo.js looks up ids, and index.html has each`, naming
`demos-list`. The real page: 59 of 59 pass.

## Not run

- The browser-only parts (highlight, pacing, the pinned bar, phone width) have no automated
  check. They were driven in a browser instead: all five cases played to their codes, the
  bar closed mid-case and Home pressed afterwards, the tool's own Start new case after a finished
  case, pause and resume, taking over by hand, Watch again, phone width, and the embedded view (`?host=redcap`), which shows nothing and adds no height.
