# Group I — morphology names moved to ICD-O-3.2

**Closes the Group I half of `docs/TODO.md` §27.** Opened 4 October 2026; the two registrar
rulings that finished it were given on 6 October 2026. `GROUP1` is in `ROUND_TRIP_GROUPS`
and the build reports `186/186 (code, name, behaviour) triple(s) exist verbatim in
icdo32.sqlite; 0 declared name exemption(s)`.

## 1. Why

Standing rule 16 removed `check_redcap_exact_names`, which was the only check on Group I's
`morphology_name` strings. Every other group's names go through `check_icdo32_round_trip()`,
which asks a stronger question: *is this a real ICD-O-3.2 term for this code at this
behaviour*, rather than *does it match a REDCap option string that may itself be stale*.

With `GROUP1` added to `ROUND_TRIP_GROUPS` the round trip failed **33** times. It now passes.

## 2. What the 33 actually were

They are not 33 wrong names. They are 15 wrong names, and 18 echoes of three of them:

| | count |
|---|---|
| `morphology_entries[].morphology_name` that is not an ICD-O-3.2 term | 15 |
| `nos_fallback_name` inside another entry repeating one of those names | 8 |
| node-level `nos_fallback` doing the same | 6 |
| pairs ICD-O-3.2 carries no term for at all | 4 |

Fourteen of the eighteen echoes are of just three strings — 9975, 9964 and 9980 — so
correcting those three entries cleared them. **9945 needed no rename**: `Chronic
myelomonocytic leukemia, NOS` is already a valid term, and it appeared in the failure list
only because its `nos_fallback_name` carried 9975's bad string.

## 3. The 15 renames

Source is `ICD coding/ICD-O-3.2/icdo32.sqlite`. Level is the level the new string sits at.

| Code | Was | Now | Level |
|---|---|---|---|
| 9867/3 | Acute myelomonocytic leukemia | Acute myelomonocytic leukemia, NOS | Preferred |
| 9869/3 | …or t(13.3)(q21;q26.2); RPN1-EVI1 | …or **t(3;3)**(q21;q26.2); RPN1-EVI1 | Preferred |
| 9878/3 | …biallelic mutation**s** of CEBPA | …biallelic mutation of CEBPA | Preferred |
| 9898/3 | …Down **S**yndrome | …Down syndrome | Preferred |
| 9920/3 | Therapy related myeloid neoplasm | Therapy-related myeloid neoplasm | Preferred |
| 9940/3 | Hairy cell leukemia | Hairy cell leukemia, NOS | Preferred |
| 9946/3 | Juvenile myelomonocytic leukemia | Juvenile myelomonocytic leukemia, NOS | Preferred |
| 9964/3 | Chronic eosinophilic leukemia, NOS | Chronic eosinophilic leukemia | Preferred |
| 9965/3 | Myeloid **and** lymphoid neoplasm**s** with PDGFRA rearrangement | Myeloid **or** lymphoid neoplasm with PDGFRA rearrangement | Preferred |
| 9966/3 | Myeloid neoplasm**s** with PDGFRB rearrangement | Myeloid neoplasm with PDGFRB rearrangement | Preferred |
| 9967/3 | Myeloid **and** lymphoid neoplasm**s** with FGFR1 abnormalities | Myeloid **or** lymphoid neoplasm with FGFR1 abnormalities | Preferred |
| 9968/3 | Myeloid**/**lymphoid neoplasm with PCM1-JAK2 | Myeloid **or** lymphoid neoplasm with PCM1-JAK2 | Preferred |
| 9975/3 | Myelodysplastic/myeloproliferative neoplasm, unclassifiable**.** | Myeloproliferative neoplasm, unclassifiable | Preferred — see §3.1 |
| 9980/3 | Refractory anemia | Myelodysplastic syndrome with single lineage dysplasia | Preferred |
| 9983/3 | Refractory anemia with excess blasts | Myelodysplastic syndrome with excess blasts | Preferred |

**9869 was a correctness defect, not a wording one.** `t(13.3)(q21;q26.2)` is not valid
cytogenetic notation; ICD-O-3.2 has `t(3;3)(q21;q26.2)`. It had been on screen since the
Group 1 build and no check could see it, because the REDCap option carries the same error.

### 3.1 9975 — the preferred term, by ruling

ICD-O-3.2's **Preferred** term for 9975/3 is `Myeloproliferative neoplasm, unclassifiable`.
`Myelodysplastic/myeloproliferative neoplasm, unclassifiable` is a **Related** term on the
same code, and the round trip accepts either — it tests `name in terms` and consults level
only to warn on `[obs]`.

This build first kept the Related (overlap) wording, on the grounds that every route into
the terminal is an MDS/MPN overlap — the four MDS-tree nodes, and the NOS fallback for CMML
(9945) and JMML (9946) — so the preferred term names a different entity from the case in
hand. **The registrar overruled that on 6 October 2026: use the preferred term.** Done, and
the superseded wording is preserved in two places that both render:

* the Group I alias on 9975 keeps it searchable in the express lane, and
* it appears on the output block's **ALSO CALLED** row, next to `MDS/MPN-U` and
  `MDS/MPN overlap`.

Driven in the browser, the terminal now reads `9975 Myeloproliferative neoplasm,
unclassifiable`, with the overlap wording immediately below it on ALSO CALLED and the
UPGRADE row still reading *"MDS/MPN overlap picture recorded but the CMML, aCML and JMML
criteria were not met"*. Headline and UPGRADE line therefore sit in mild tension on the same
screen; the ALSO CALLED row is what resolves it for the clerk. Noting it because it is the
visible cost of choosing consistency across groups over per-terminal wording, and it is one
string to reverse.

## 4. The four absent pairs — removed, by ruling

`9826/3`, `9836/3`, `9991/3`, `9992/3`. ICD-O-3.2 carries no term for these at **any**
behaviour. All four were already closed terminals: marked RETIRED, *"must never be selected
as a live code"*, kept only so aliases and pre-2021 archival records resolve, and no branch
in any tree targeted them.

Three options were put to the registrar — exempt them from the round trip, drop them, or
rename them to their replacements' terms. **Ruling of 6 October 2026: remove the codes.** So
no exemption mechanism was added, which is the better outcome: an exemption is a hole that
has to be maintained, and there is now nothing to maintain.

| Removed | Was | Replaced by | Old term now finds |
|---|---|---|---|
| 9826/3 | Burkitt cell leukemia | 9687/3, **Group II** | Group II, via that group's own alias mirror |
| 9836/3 | Precursor B-cell lymphoblastic leukemia | 9811/3 | 9811, via an alias Group I already carried |
| 9991/3 | Refractory neutropenia | 9980/3 | 9980, via an alias Group I already carried |
| 9992/3 | Refractory thrombocytopenia | 9980/3 | 9980, via an alias Group I already carried |

**Nothing became unfindable.** Checked before removing, not assumed. All six Group I Burkitt
aliases (`Burkitt cell leukemia`, `Burkitt leukaemia`, `FAB L3`, `L3 ALL`, `Leukaemic Burkitt
lymphoma`, `Mature B-cell ALL`, with their `also_known_as`) are mirrored in
`aliases_group_02.json` against 9687, so they were deleted from Group I rather than left
dangling. Driven in the browser, `Burkitt leukaemia` now returns **one** result, Group 2 —
where before it offered both Group 1 and Group 2 and the clerk had to know which was current.
The other three terms already had Group I aliases pointing at the replacement code, so they
now land on a live code instead of a read-only one.

**What was given up**, and the registrar accepted it: the tool can no longer resolve a
pre-2021 archival record to the number actually filed at the time. A 2019 record coded 9826
will now be looked up and answered 9687.

Two clerk-visible strings referred to these codes and were corrected rather than left:
`ml_*` node 22's fallback reason (`9826 is retired and is never emitted` → `no longer carried
in Group I at all`) and node 25's first option, which also carried a **stale warning** —
*"the same alias strings must exist in aliases_group_02.json … that mirror is a flagged
gap"*. The mirror was built on 4 September 2026 and is complete; the sentence now says so.

## 5. Aliases

Five superseded REDCap wordings were already aliases (`Hairy cell leukemia`, `Acute
myelomonocytic leukemia`, `Juvenile myelomonocytic leukemia`, `Refractory anemia`,
`Refractory anemia with excess blasts`). **Nine** were added or retuned, following the Groups
VII and IX convention — `origin_system: "REDCap option label"`, `full_form` as
`"<REDCap wording> -> <ICD-O-3.2 term> (<code>)"`:

* eight for the renamed codes (9878, 9898, 9920, 9964, 9965, 9966, 9967, 9968);
* one for **9869**, which is the only alias in Group I that deliberately records an *error*.
  The REDCap option label reads `t(13.3)(q21;q26.2)`. A clerk who copies that string out of
  REDCap would otherwise find nothing, because the tool now shows the correct notation;
* the pre-existing 9975 alias was retuned for the new display term and given
  `MDS/MPN-U` / `MDS/MPN overlap` in `also_known_as`, which is what puts them on the
  ALSO CALLED row.

Six Group I Burkitt aliases were **deleted** with the 9826 entry (§4).

All of them resolve in the generated `alias_index.json`. `Therapy related myeloid neoplasm`,
`MDS/MPN overlap` and `Burkitt leukaemia` were each driven through the real express lane.
This is what keeps the renames safe for the clerk: the string they can see in REDCap is
still what they can type into the tool.

## 6. Proof

Six negative controls, each pinned to an explicit string rather than to `HEAD`.

Before the rulings, with `GROUP1` enabled and the four absent pairs still present
(baseline 4 FAILs):

| Control | FAILs | Expected |
|---|---|---|
| A. 9869 `t(13.3)` typo restored | 5 | fires |
| B. one `nos_fallback_name` left stale on 9964 | 5 | fires |
| C. 9980 near-miss — `single-lineage` hyphenated | **7** | fires |
| D. 9975 set to the ICD-O-3.2 preferred term | 4 | quiet |

After the rulings (baseline 0 FAILs):

| Control | FAILs | Expected |
|---|---|---|
| E. re-add 9991, as a full clone of a valid entry | ≥1, including `entry 9991/3: ICD-O-3.2 carries no term at all` | fires |
| F. 9975 back to the Related term | 0 | quiet |

C landing on 7 rather than 5 is the cascade proving itself in the other direction: renaming
the 9980 entry also breaks the two `nos_fallback_name` references in 9991 and 9992. D and F
staying quiet are what make §3.1 a registrar's choice rather than something the validator
forced either way.

E was run twice. The first attempt added 9991 as a minimal stub and produced 10 FAILs, most
of them missing-field errors from the stub itself — a control that fires for the wrong
reason proves nothing, so it was re-run with a full clone of a valid entry to isolate the
round-trip failure.

Driven in the browser at the renamed terminals, not only in the validator. Two things
surfaced there and nowhere else: the stray full stop on 9975 had been rendering the
escape-hatch sub-line as *"…unclassifiable., flagged as discordant."*, and `Burkitt leukaemia`
had been returning two results where only the Group II one is current.

## 7. Owed elsewhere

15 REDCap `i_morph` relabels **and 4 retires** (`9836`, `9826`, `9991`, `9992` — the codes
removed in §4), listed in `docs/TODO.md` §7. Retire in place, never delete: `i_morph` stores
a pick number, so deleting one renumbers every pick after it. Nothing here touches REDCap —
standing rule 16.

`9984/3` still raises a WARN: `Refractory anemia with excess blasts in transformation` is
ICD-O-3.2's **Preferred** term for that code but is marked `[obs]`, and the code's only
non-obsolete term is the abbreviation `RAEB-T`. RAEB-T was abolished in 2001. Left as it is
— the WARN is accurate — but the entry is a candidate for the same retired-terminal
treatment as the §4 four.
