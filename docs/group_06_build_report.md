# Group VI — build report, 2026-09-23

**Branch:** `group-06-renal`, cut from `group-05-retinoblastoma`, itself unmerged. `main` untouched.
**Contract:** `docs/group_06_build_contract.md`.

Read §1 and §8 if you read nothing else. §1 is what this group turned out to be; §8 is what needs
you.

---

## 1. What this group is, and the one fact that reshaped it

Ninety codes, of which **five carry the paediatric disease**: `8960/3` nephroblastoma, `8959/3`
malignant cystic nephroma, `8963/3` rhabdoid tumour of the kidney, `8964/3` clear cell sarcoma of
the kidney, and `8510/3` renal medullary carcinoma. The other eighty-five are the ICCC-3 carcinoma
block transplanted onto the kidney, most of which a paediatric registry will never meet.

You said this group has low research output because the system is small. That is right, and it
shows: Wilms tumour is roughly 90% of paediatric renal cancer and clear cell sarcoma of the kidney
about 5%. What it does not predict is where the difficulty actually sat, which was not in the
literature at all but in the **code set**.

### ★ `8311/3` is not "Hypernephroid tumor", and that changes about half the carcinomas

The diagnostic pathway document's §4F and §7.6 instruct the build to route every molecularly defined
renal carcinoma — TFE3-rearranged, TFEB-altered, ELOC-mutated, fumarate hydratase-deficient,
succinate dehydrogenase-deficient, ALK-rearranged — to `8312/3` renal cell carcinoma NOS, "because
the registry code set has no distinct codes" for them, capturing the subtype as annotation only.

The code set does have one. **ICD-O-3.2 created `8311/3` for exactly these tumours**, and WHO 2022
Table 1 assigns seven entities to it. Three independent confirmations:

| Source | What it says |
|---|---|
| `icdo32.sqlite` | `8311/3` Preferred: *Hereditary leiomyomatosis and renal cell carcinoma (HLRCC) syndrome-associated renal cell carcinoma*; Related: *MiT family translocation carcinoma*, *Succinate dehydrogenase deficient renal cell carcinoma* |
| IARC *3.1 to 3.2 — New codes and their terms*, p. 5 | `8311/3` listed among the new codes, with both terms new in 3.2 |
| Moch 2022, Table 1 | seven WHO 2022 entities on `8311/3` |

**How much this decides.** Cajaiba MM, et al. *Cancer* 2018;124(16):3381–3389 classified 212 renal
cell carcinomas in children and young adults on Children's Oncology Group protocol AREN03B2. Mapped
onto ICD-O-3.2: MiT-family translocation carcinoma **41.5%**, ALK-rearranged 3.8%, fumarate
hydratase-deficient 1.4%, succinate dehydrogenase-deficient 0.5% — **47.2% of paediatric renal cell
carcinoma sits on `8311/3`**, and MiT-family translocation carcinoma alone is the commonest subtype
in this age group. Following the pathway document would have recorded nearly half of this group's
carcinomas as unclassified when the file names the entity.

That is the mirror of the failure this project usually guards against. Overstating evidence makes a
case look better worked up than it is; this would have made it look *worse*, and the registry then
cannot count what it actually holds. Both directions are now banned and checked.

**The REDCap dropdown still says the old thing.** Its `8311` option reads *"Hypernephroid tumor
[obs]"* — the obsolete `8311/1` term, for a different lesion. §8 item 3.

---

## 2. The baseline, and the thing it turned out to be

**Moch H, Amin MB, Berney DM, et al.** *The 2022 World Health Organization Classification of Tumours
of the Urinary System and Male Genital Organs — Part A: Renal, Penile, and Testicular Tumours.*
European Urology 2022;82(5):458–468. PMID 35853783.

It was not on disk. It is CC BY 4.0 open access, but the Zurich and Bern repository copies sit
behind bot checks I would not bypass; the Francis Crick Institute's figshare deposit serves the
publisher PDF directly, and with your permission it was downloaded, extracted and read in full. It
now lives at `Group 6 Papers/Moch-2022-WHO-urinary-male-genital-PartA.pdf`.

**Its Table 1 is this group's Hoogendijk.** *"ICD-O coding of tumours of the kidney"* prints the
ICD-O-3.2 code against every WHO 2022 renal entity — precisely what Hoogendijk 2022's Table 1 does
for the central nervous system, and what `docs/group_baseline_documents.md` §1b says usually does
not exist. **For Group VI the classification summary and the registry-implications document are the
same paper.** The PubMed MeSH sweep for a Hoogendijk equivalent returned nine records and no
candidate, and that is the correct result rather than a gap.

What Table 1 settled, none of which was derivable from the pathway document:

| Finding | Consequence |
|---|---|
| `8311/3` carries **seven** entities | §1 above |
| `8510/3` carries **four** — medullary carcinoma NOS plus three SMARCB1-deficient forms | the fork at §4 |
| `8316/3` carries **two** — tubulocystic and acquired cystic disease-associated | code-sharing, recorded |
| `8959` appears only at `/0` and `/1` | **no WHO 2022 entity lives at `8959/3`** — §8 item 1 |
| mesoblastic nephroma is `8960/**1**` | the proposed recode is refused — §8 item 2 |
| nephrogenic rests and nephroblastomatosis carry **no ICD-O code at all** | the imaging route's diversion criteria |

**Pfister 2022 is not the spine for this group, and this was checked rather than assumed.** The full
text was retrieved from PubMed Central (PMC9401511) and searched: **"kidney" appears zero times.**
"Renal" appears 16 times and opens no renal section; "Wilms" appears 6 times, all in passing — as
the worked example of a blastoma, in the anaplasia criterion, and among the cancer-predisposition
syndromes. This is the second paediatric-site group checked this way and the second to come back
negative, which is now recorded in `docs/group_baseline_documents.md`.

---

## 3. Where the sources disagree, and how that was handled

**Haemoglobinopathy and renal medullary carcinoma.** The pathway document says a haemoglobinopathy
is an "essential diagnostic criterion" for `8510/3`. It was not making that up — Trpkov 2021, p.
1407, says exactly that, and the Genitourinary Pathology Society split the SMARCB1-lost tumour
*without* one off as "unclassified renal cell carcinoma with medullary phenotype". Moch 2022 §2.4
reverses it a year later: *"sickle cell is not a prerequisite for this genetic lesion"*, and WHO 2022
Table 1 puts both on `8510/3`.

Latest document wins, and it is also the baseline, so the tool follows Moch. Both quotes are in the
contract and in `docs/clinical-warnings.md` — the older source is recorded as superseded, not as
wrong, because it was current when the pathway document was written.

**Nuclear unrest.** The usual shorthand is that it "behaves like favourable histology". Hill 2003 is
more careful: recurrence at five years was 22.2% against favourable histology's 12.2%, overall
survival *"nearly identical"*, and the conclusion is that nuclear unrest *"represents an intermediary
in the continuum"*. Grouping it with favourable histology is a treatment-stratification decision, not
a claim the two are the same thing. The warning says so.

**"SIOP protocol, so no biopsy" is not what SIOP says.** Spreafico 2021 gives SIOP's own biopsy
indications — age seven or older, or psoas infiltration, numerous calcifications, vessel encasement,
massive lymphadenopathy. Those four atypical features became the tree's diversion criteria,
replacing a list I had assembled myself. What differs between the Children's Oncology Group and SIOP
is *staging*, not whether tissue is ever taken. And a needle biopsy does not settle the question a
clerk is coding: it *"cannot reliably distinguish WT from nephrogenic rests, and often misses
anaplasia"*.

---

## 4. The tree

One tree, `g6_renal`, 12 nodes, entry `rn_document_inventory`. Its signature branch is the
**SMARCB1/INI1 fork**: one immunohistochemical result is the defining finding for both `8963/3`
rhabdoid tumour of the kidney and `8510/3` renal medullary carcinoma, and loss alone must never
choose between them. Three rules, conditioned first, gated on age band and sickle-cell status —
where `unknown` is never read as `negative`, and in this registry `unknown` will be the common
answer.

The imaging route emits `8960/3` at **basis 2 and never basis 1**. Visser 2023 Table 3 gives
nephroblastoma basis 2, C64, `8960/3` — the only Group VI row in the table. Retinoblastoma's "1 or
2" is why Group V's alias node can emit a code on a referral letter's wording; Group VI's cannot, and
that difference is deliberate.

Four deviations from the contract's diagram are recorded in the file with their reasons, the
substantive one being that `rn_sickle_status` is a node of its own because `test_result_states` is a
closed vocabulary of test outcomes with no room for "trait" or "disease".

---

## 5. Shared-layer changes, and four dead router branches

Declaring Group VI built required touching `presentation_router.json`, and doing so found that
**four dual-group branches had never worked**.

`app.js`'s `branchMatches()` reads two shapes: `topography_in`, a list, and `captured_variable` with
a comparator. Four branches wrote `topography_equals`, which it has never read. Each returned false
always, so every case fell to the rule's default:

| Rule | Intended | Actually went to |
|---|---|---|
| `9380` at C72.3 | Group III `IIIb` | Group III `IIId2` |
| `8158,8290` at C75.1 | Group III `IIIe1` | **Group XI** |
| `8963` at C64.9 | **Group VI `VIa2`** | **Group IX `IXd3`** |
| `8000-8005` at C64.9 | Group VI `VIc` | (branch added in the same commit) |

Two crossed an ICCC-3 group boundary. A pituitary tumour sited at the pituitary gland routed out of
Group III. **A rhabdoid tumour of the kidney could never reach Group VI — the group that owns the
code.**

Nothing caught it because nothing asked the right question. The existing checks prove every
*destination* is real; neither asks whether a *condition* can ever be true, and a branch with an
unreadable condition has a perfectly valid destination it never reaches. `check_router_branch_when_vocabulary()`
now closes the `when` vocabulary against `branchMatches()` itself.

The same edit closed `docs/TODO.md` §12 for the two rules Group VI owns, extending them from the
three NOS-level central nervous system codes to all 21 in C70.0–C72.9, and added the completeness
check §12 itself proposed. `9473` stays open and is exempt **by name**, with an exemption that fails
the build if the rule is ever repaired without deleting the name.

---

## 6. Layer 1 — nineteen findings, the largest repair package yet

`docs/group_06_layer1_repair.md`. Nineteen findings against 98 `vi_morph` options, where Group V had
one against five. The reason is structural: VIb is the whole ICCC-3 carcinoma range transplanted onto
the kidney, so it inherits every drift that range carries — including codes that were never kidney
entities. `8561 Adenolymphoma`, a benign salivary-gland Warthin tumour, is offered as a renal choice.

- **One retired number**, `8965/0 Nephrogenic adenofibroma`, deleted by IARC and moved to `9013/0` —
  the first retired number this project has met in a live option list, and unlike a behaviour
  exclusion it can never be re-scoped by a registry decision.
- **Ten behaviour exclusions**, Group V's `9514` pattern, of which `8040` is a double defect: out of
  behaviour *and* mislabelled, so the form offers one disease under two option values reading
  identical text, and the one a clerk might pick first is the code for a benign lung lesion.
- **Eight string drifts**, of which `8311` and `8504` name a *different lesion* from the one the code
  now carries.
- **One code with no current term at all**: every ICD-O-3.2 term at `8130/3` carries `[obs]`, because
  invasive papillary urothelial carcinoma now codes `8120/3`. Not a relabel — the registrar decides
  whether to retire the option.

`vi_morph` stores the real ICD-O code as the option value, so every repair is a label edit and no
stored value moves.

---

## 7. What a green build missed — twice

**This is the section to read alongside §5.** A green `build_database.py` proved nothing about either
defect below. Both were found by driving the tool in a browser, and both were in the engine.

**7.1 The tool told the clerk one code and recorded another.** On the fork at §4, with SMARCB1, WT1
and BCOR all negative in a 14-year-old with sickle-cell trait, the node stopped asking. The screen
read *"One outcome remains. Continue to record it."* above `8311`. Continue emitted `8000`. ALK was
never asked. `nextMarker()` treated "one rule left" as "decided", but a rule stays live while a
marker it needs is merely unanswered.

**7.2 The wording promised what the button would not deliver.** The same mistake in `markerFlow()`
survived the first fix: the sentence came from the count of live rules, so a fully negative panel
read *"0 outcomes still in play"* with *"One outcome remains. Continue to record it."* directly
beneath. I had checked the code that came out and the marker sequence and called that path honest.
Its routing was; its screen was not.

**Neither was Group VI's.** A parallel session swept all 68 checklist nodes: the first defect is
reachable in **565 states across 14 nodes in four groups** — at `g2_hodgkin`, four negatives recorded
`9650/3` while a rule needing EBER, LMP1 and EBNA2 was never asked — and the second in **1546 states
across 15 nodes**.

`build/check_engine_flow.mjs` is the check that closes this, and it is the only thing in the
repository that tests `app.js` at all. Its open items are `docs/TODO.md` §19–§21.

**7.3 The tool told clerks eleven selectable codes could not be selected.** Found on the `8311`
output. The banner read *"This code has no option in the registry dropdown, so it cannot be selected
yet"* — off a flag that only means the option string was not *verified*. Eleven codes across Groups
I, II and VI have an option a clerk can select today and were being told they could not. Sending
someone away from a row that is there is the same class of defect as sending them to one that is
not. Reasoning in `docs/codes-awaiting-redcap.md`.

---

## 8. What needs you

1. **★ `8959/3` carries no WHO 2022 entity.** ICD-O-3.2 has the code and ICCC-3 admits it at
   behaviour 3; WHO 2022 Table 1 lists `8959` only at `/0` (mixed epithelial and stromal tumour,
   adult and paediatric cystic nephroma) and `/1` (cystic partially differentiated nephroblastoma).
   Does the tool keep emitting it, or does malignant cystic nephroma become a registrar referral?
2. **★ The congenital mesoblastic nephroma recode.** The pathway document asserts a registry
   convention mapping it to `8960`, citing nothing. Both ICD-O-3.2 and WHO 2022 put it at
   `8960/**1**`. Coding it `8960/3` would register a borderline tumour of infancy as a malignant
   Wilms tumour, so this build refuses it and emits a behaviour exclusion. If the convention is real
   it needs a ruling on the record.
3. **`8311` is mislabelled in REDCap** as `[obs]` "Hypernephroid tumor" — a different lesion. Given
   §1, this is the most consequential single option-file defect the project has found.
4. **`8965` is a retired number still in the dropdown** — the first of its kind met here.
5. **Benign renal entities.** Ten REDCap options are behaviour 0 or 1. Group VI declares behaviour 3
   and cannot hold them. If the registry wants them they need a home outside Group VI, not a
   behaviour override inside it.
6. **Both Chung RadioGraphics papers are still missing**, so `8960/3`'s imaging features rest on
   Spreafico 2021 and the papers index rather than a dedicated imaging source. On
   `docs/sources-requested.md`.
7. **Should the engine gate run inside the Python gate?** `docs/TODO.md` §19, with a recommendation
   and the reason it is yours rather than mine.

---

## 9. Proof

| Gate | Result |
|---|---|
| `python3 build/build_database.py` | 0 FAIL |
| `python3 build/induce_flow.py` | every rule in every checklist has a witness |
| `node build/check_engine_flow.mjs` | 68 nodes, 743 walks, ~58,000 stops, OK |
| negative control, engine gate vs pre-fix `app.js` | 1245 failures, as it must |
| Groups 1–5 vs `group-05-retinoblastoma` | byte-identical |

Every new check was proved by breaking the data and watching it fail, then restoring. One was also
proved the other way: `check_group6_molecular_rcc_code` passed its negative control first try and
then **failed on correct data** — a carcinoma still unclassified after a complete workup in which
every molecularly defined entity was tested and negative, which is exactly the case `8312/3` exists
for. A false FAIL is the more corrosive kind, because it teaches the next author to restructure
correct data to appease the validator. Contract §8.1 now requires both controls for any check that
reads free text.
