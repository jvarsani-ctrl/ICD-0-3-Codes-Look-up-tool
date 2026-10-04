# Group I — morphology names moved to ICD-O-3.2

Closes the Group I half of `docs/TODO.md` §27, except for four codes that need a registrar
ruling (§4 below). Opened and done 4 October 2026.

## 1. Why

Standing rule 16 removed `check_redcap_exact_names`, which was the only check on Group I's
`morphology_name` strings. Every other group's names go through `check_icdo32_round_trip()`,
which asks a stronger question: *is this a real ICD-O-3.2 term for this code at this
behaviour*, rather than *does it match a REDCap option string that may itself be stale*.

With `GROUP1` added to `ROUND_TRIP_GROUPS` the round trip failed **33** times. It now fails
**4**, and those four are the ruling in §4.

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
| 9975/3 | …unclassifiable**.** | …unclassifiable | **Related** — see §3.1 |
| 9980/3 | Refractory anemia | Myelodysplastic syndrome with single lineage dysplasia | Preferred |
| 9983/3 | Refractory anemia with excess blasts | Myelodysplastic syndrome with excess blasts | Preferred |

**9869 was a correctness defect, not a wording one.** `t(13.3)(q21;q26.2)` is not valid
cytogenetic notation; ICD-O-3.2 has `t(3;3)(q21;q26.2)`. It had been on screen since the
Group 1 build and no check could see it, because the REDCap option carries the same error.

### 3.1 The one deliberate deviation: 9975

ICD-O-3.2's **Preferred** term for 9975/3 is `Myeloproliferative neoplasm, unclassifiable`.
`Myelodysplastic/myeloproliferative neoplasm, unclassifiable` is a **Related** term on the
same code — a real, non-obsolete ICD-O-3.2 term, which is what the round trip tests
(`if name in terms`; level is not consulted, only `[obs]` is, and it warns).

Every route into this terminal is an MDS/MPN **overlap**: the four MDS-tree nodes
(`mds_jmml_genetics`, `mds_jmml_like_genotype`, `mds_jmml_unconfirmed`,
`mds_monocytosis_gate`) and the NOS fallback for CMML (9945) and JMML (9946). The preferred
term names a different entity — a pure MPN, with no dysplastic component. Driven in the
browser, the output block for this terminal shows the name beside an UPGRADE row reading
*"MDS/MPN overlap picture recorded but the CMML, aCML and JMML criteria were not met"*; the
preferred term would contradict that line on the same screen.

So only the stray full stop was removed. Control D below proves the preferred term would
also pass, so this is a choice and not a workaround — one string to reverse if the registrar
wants strict preferred-term consistency across groups.

## 4. The four that need a ruling — and why it is not a naming question

`9826/3`, `9836/3`, `9991/3`, `9992/3`. ICD-O-3.2 carries no term for these at **any**
behaviour; they are absent from the database entirely.

They are already **closed terminals**: each entry's note says RETIRED and *"must never be
selected as a live code"*, each is retained only so aliases and pre-2021 archival records
resolve, and **none is reachable from any tree** (0 mentions across all four trees). Their
current names are the correct historical ICD-O-3.1 terms, which is what a retained retired
code should display. Renaming them to their replacements' terms would be worse — 9836 would
read `B lymphoblastic leukemia/lymphoma, NOS` while carrying 9836.

The precedent in Groups 3–9 does not cover this. Their `*_ABSENT_CODES` **ban** a code from
appearing at all; Group I **retains** these four on purpose.

| Code | Current name | Replaced by | Where the entity went in ICD-O-3.2 |
|---|---|---|---|
| 9826/3 | Burkitt cell leukemia | 9687/3, Group II | Leukaemic Burkitt codes 9687 from 1 Jan 2021 |
| 9836/3 | Precursor B-cell lymphoblastic leukemia | 9811/3 | Merged into 9811 |
| 9991/3 | Refractory neutropenia | 9980/3 | Now an `[obs]` synonym under 9980/3 |
| 9992/3 | Refractory thrombocytopenia | 9980/3 | Now an `[obs]` synonym under 9980/3 |

Options, for the registrar:

1. **Exempt deliberately-retired closed terminals from the round trip**, under a narrow
   declared rule that collapses: the entry must be flagged retired, the pair must genuinely
   be absent from `icdo32.sqlite`, and the code must be unreachable from every tree. It then
   FAILs the day ICD-O-3.2 starts carrying the pair, or the day a tree makes it reachable.
2. **Drop the four entries** and let their aliases route to 9811, 9687, 9980 and 9980. Loses
   the ability to resolve a pre-2021 archival record to the number actually filed at the time.
3. Rename them to the replacement's term. Not recommended — the name would then disagree
   with the code on the same row.

`GROUP1` is **not** in `ROUND_TRIP_GROUPS` yet, because option 1 is the only one that makes
the build pass and it is not mine to choose. That is a one-line change once ruled.

## 5. Aliases

Five of the superseded REDCap wordings were already aliases (`Hairy cell leukemia`,
`Acute myelomonocytic leukemia`, `Juvenile myelomonocytic leukemia`, `Refractory anemia`,
`Refractory anemia with excess blasts`). Eight were added, following the Groups VII and IX
convention — `origin_system: "REDCap option label"`, `full_form` as
`"<REDCap wording> -> <ICD-O-3.2 term> (<code>)"`. All eight resolve in the generated
`alias_index.json`, and `Therapy related myeloid neoplasm` was driven through the real
express lane to confirm it still lands on the code.

This is what keeps the rename safe for the clerk: the string they can see in REDCap is still
what they can type into the tool.

## 6. Proof

Four negative controls, each pinned to an explicit string rather than to `HEAD`:

| Control | FAILs | Expected |
|---|---|---|
| Baseline, corrected data | 4 | the §4 four |
| A. 9869 `t(13.3)` typo restored | 5 | fires |
| B. one `nos_fallback_name` left stale on 9964 | 5 | fires |
| C. 9980 near-miss — `single-lineage` hyphenated | **7** | fires |
| D. 9975 set to the ICD-O-3.2 **preferred** term | 4 | **quiet** |

C landing on 7 rather than 5 is the cascade proving itself in the other direction: renaming
the 9980 entry also breaks the two `nos_fallback_name` references in 9991 and 9992. D staying
at baseline is what makes §3.1 a choice rather than a workaround.

Driven in the browser at the renamed terminals, not only in the validator. One incidental
fix surfaced there: the stray full stop on 9975 had been rendering the escape-hatch sub-line
as *"…unclassifiable., flagged as discordant."*

## 7. Owed elsewhere

15 REDCap `i_morph` relabels, listed in `docs/TODO.md` §7. Nothing here touches REDCap —
standing rule 16.

`9984/3` still raises a WARN: `Refractory anemia with excess blasts in transformation` is
ICD-O-3.2's **Preferred** term for that code but is marked `[obs]`, and the code's only
non-obsolete term is the abbreviation `RAEB-T`. RAEB-T was abolished in 2001. Left as it is
— the WARN is accurate — but the entry is a candidate for the same retired-terminal
treatment as the §4 four.
