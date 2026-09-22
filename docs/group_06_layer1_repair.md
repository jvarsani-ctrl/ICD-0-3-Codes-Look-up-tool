# Group 6 — Layer 1 Repair Package (REDCap `vi_morph`)

**22 September 2026** · a **REDCap-project** document. The ICD-O lookup tool is a separate project
and **does not depend on any of this** — it generates its inventory from `icdo32.sqlite` and
`ICCC-2017.sqlite` directly. Nothing here gates `group_06_dt.json`.
**Status:** ready to review. **Nothing has been applied to the live form.**
**Method:** identical to the Group 3, 4 and 5 packages, extended because this group produces two
finding types those packages did not: the project's first genuinely **deleted** code sitting in a
live option list, and a code collision where one disease is offered under two option values and
one of them is wrong.
**Scale:** the **largest** repair package of the four written so far — **nineteen findings against
ninety-eight options**. Group 5 had one finding against five options.

---

## 0. Why this is the largest repair package in the project

`vi_morph` stores the real ICD-O-3 code as the option value, the same convention `v_morph` uses —
confirmed against `Registry Data/data dictionary/Diagnosis.md` (§ `vi_morph`, `vi_extended`,
`vi_subgroup`) and `EAFYA IMPORT/redcap_field_choices.json`. There is no `vi_code` companion field,
because Group VI's option list is one term per code, the same pattern as Groups I, II, V, IX, X, XI
and XII. **Unlike `v_morph`, Group VI does carry two auto-calculated companion fields**,
`vi_extended` and `vi_subgroup`, both `if()` chains keyed on the literal `vi_morph` value. Because
they match on the value and not on option position, nothing in this repair disturbs them — see §5.

**An unrelated, already-live defect, found while checking this: `vi_extended`'s VIa3 branch
misspells the field reference as `[vi_morp]` instead of `[vi_morph]`** (Diagnosis.md, verified). A
record with `vi_morph = '8967'` fails that malformed condition and `vi_extended` falls through to
blank instead of `"VIa3: Kidney sarcomas"`. This is a calculated-field formula bug, not an
option-list defect, and it happens to touch the same code, `8967`, that §2 below retires. Fixing
one does not fix the other. It is noted here and again in §6, not repaired by this package.

**Why the count is nineteen and not one.** Group V's five-code range is unique to retinoblastoma;
nothing else in ICCC-3 reuses it, so a Group V finding can only come from a change specific to
those five stems. Group VI's VIb subgroup is different in kind: `ICCC-2017.sqlite` assigns it the
generic **8010–8573 carcinoma block** — the same range structure ICCC-3 attaches to several organ
sites — transplanted onto the kidney at `C64.9`. Every drift ICD-O-3.2 introduced anywhere in that
block — the transitional-cell-carcinoma-to-urothelial-carcinoma renaming, papilloma and
papillomatosis terms that were never malignant, a small-cell-carcinoma stem split across two codes,
a behaviour reassignment on an intracystic-lesion code — lands on Group VI whether or not it has
anything to do with a kidney. Group V never had that exposure because it never shared a range with
anything else. Nineteen findings against ninety-eight options is what a generic, heavily-revised
carcinoma range looks like once it is checked term by term, not evidence that this group's own
content is unusually disordered.

---

## 1. Class 1 — one retired number

**Option `8965` — "8965 - Nephrogenic adenofibroma" — is not an ICD-O-3.2 code. It was deleted and
its content moved to a different stem.**

`3.1 to 3.2 – Deleted codes and their terms` (9 October 2020) records it verbatim:

> `8965 /0 Nephrogenic adenofibroma (C64.9) — Moved to 9013/0`

Zero rows survive at `8965` in `icdo32.sqlite`. The disease did not disappear — its content now
lives at `9013/0 Adenofibroma, NOS` — but the four-digit number `8965` no longer resolves to
anything in ICD-O-3.2.

**This is the first retired number the project has met in a live option list.** Group 5's `9514`
and Group 4's `8683` — both discussed as precedent in the Group 6 build contract §0.6 — are
**behaviour exclusions**: numbers that still exist in ICD-O-3.2, just not at the behaviour ICCC-3
Group VI (or IV, or V) declares. `8965` is not that. IARC withdrew the number itself.

**The distinction is not cosmetic — it sets what the repair can promise.** A behaviour exclusion
may be re-scoped: if the registrar later rules that the registry should hold a home for benign
renal entities, ten of this package's nineteen findings (§2) could be un-retired or moved without
IARC's involvement, because the numbers themselves are still current ICD-O-3.2 codes. `8965` cannot
be re-scoped by any registry decision. Reinstating it would require IARC to reissue the number,
which is not a call this project or the registrar can make. `[RETIRED]` on `8965` is permanent in a
way it is not for the ten findings in §2.

**A connecting detail.** `9013`, the code `8965`'s content moved to, is itself one of the ten
findings in §2 — it is a real, current ICD-O-3.2 code, but at behaviour `/0` only, outside Group
VI's behaviour-3 declaration. So the disease named by the deleted `8965` option already has a
correct home in the option file today, under `9013`, and that option is *also* wrong for Group VI,
for a different reason. Retiring both is required; adding a replacement option for either is not.

---

## 2. Class 2 — ten behaviour exclusions

Each of these ten numbers is a real, current ICD-O-3.2 code. Each exists only at behaviour `0` or
`1`. ICCC-3 Group VI declares behaviour **3** and nothing else (build contract §0.2). None of the
ten can be emitted by the tool, for the identical reason Group 5's `9514` cannot: the code the
option names simply does not exist at the behaviour the group requires.

| Option | REDCap label | ICD-O-3.2 behaviour | What WHO 2022 Table 1 says |
|---|---|---|---|
| `8966` | Renomedullary interstitial cell tumor | `/0` only | `8966/0` |
| `8967` | Ossifying renal tumor | `/0` only | `8967/0`, ossifying renal tumour of infancy |
| `8325` | Metanephric adenoma | `/0` only | `8325/0` |
| `8361` | Juxtaglomerular tumor | `/0` only | `8361/0` |
| `9013` | Adenofibroma, NOS | `/0` only | `9013/0`, metanephric adenofibroma |
| `8053` | Squamous cell papilloma, inverted | `/0` only | no renal-specific entry — a generic epithelial-range term, not a kidney entity |
| `8060` | Squamous papillomatosis | `/0` only | no renal-specific entry |
| `8191` | Embryonal adenoma | `/0` only | no renal-specific entry |
| `8561` | Adenolymphoma | `/0` only | no renal-specific entry — this is the Warthin-tumour stem, a salivary-gland lesion carried along by the shared carcinoma range |
| `8040` | Small cell carcinoma, NOS | `/0` and `/1` (Tumorlet) | see below — this one is not just out of behaviour |

The first five carry a Moch 2022 Table 1 citation because they are genuine kidney entities that
the WHO renal classification names at behaviour 0. The last four have no renal-specific citation
because they are not kidney entities at all — they are generic terms sitting in the same 8010–8573
range that VIb declares site-wide at `C64.9` regardless of whether ICD-O-3.2 has ever attached them
to the kidney. `8561 Adenolymphoma`, the Warthin-tumour code, is the clearest case: it is a benign
salivary-gland tumour that the option file offers as a renal choice only because the range crossed
sites, exactly the mechanism §0 describes.

### `8040` — a double defect, not a simple exclusion

`8040` fails on two counts at once, and needs to be understood as one problem, not layered as two.

**It is out of behaviour.** ICD-O-3.2's `8040` is *Tumorlet*, at `/0` and `/1` — a minute,
incidental proliferative pulmonary lesion, not a malignant kidney tumour and not even a kidney
entity.

**It is also mislabelled.** The REDCap label the option carries, "Small cell carcinoma, NOS", is
not `8040` — it is `8041/3`, and the option file already offers `8041` as a separate choice with
the identical label: `8041, 8041 - Small cell carcinoma, NOS`.

So the form currently offers **one disease under two option values**, both reading "Small cell
carcinoma, NOS", and one of those values — `8040` — is not the code for that disease at all; it is
the code for an unrelated benign lung lesion. A clerk who does not already know to prefer `8041`
has no way to tell the two apart from the dropdown text alone, because the text is identical. The
repair does not need a relabel here, because the correct option already exists under `8041`; it
needs `8040` retired, and nothing added.

---

## 3. Class 3 — eight string drifts

Reproduced from build contract §2C. Each row is a case where the code itself is correctly in
Group VI's scope at behaviour 3, but the label the option carries is not the ICD-O-3.2 preferred
term for that code.

| Code | REDCap option string | ICD-O-3.2 preferred term | Where the REDCap string actually sits |
|---|---|---|---|
| `8963` | Malignant rhabdoid tumor | **Rhabdoid tumor, NOS** | a synonym under `8963/3` |
| `8122` | Transitional cell carcinoma, spindle cell | **Urothelial carcinoma, sarcomatoid** | a synonym under `8122/3` |
| `8130` | Papillary transitional cell carcinoma | **Papillary urothelial carcinoma** | a synonym, and **both carry `[obs]`** |
| `8131` | Transitional cell carcinoma, micropapillary | **Urothelial carcinoma, micropapillary** | a synonym under `8131/3` |
| `8240` | Carcinoid tumor, NOS | **Neuroendocrine tumor, NOS** | a synonym under `8240/3` |
| `8155` | Vipoma, malignant | **Vipoma** | **no match at any level** |
| `8311` | Hypernephroid tumor `[obs]` | **Hereditary leiomyomatosis and renal cell carcinoma (HLRCC) syndrome-associated renal cell carcinoma** | the `[obs]` `8311/1` term — see below |
| `8504` | Intracystic carcinoma, NOS | **Encapsulated papillary carcinoma with invasion** | the `8504/**2**` synonym — a behaviour drift |

Two of these are cosmetic in the sense that the option still points a clerk toward the right
disease under an outdated name — `8963`, `8122`, `8131`, `8240` read as older synonyms of the
correct entity, not a different one. `8155` is the odd one in that group: "Vipoma, malignant" does
not match any term ICD-O-3.2 records against `8155` — not the preferred term, not a synonym, not an
obsolete form. It reads as invented wording rather than a stale one. `8130` is unresolved rather
than cosmetic: build contract §2C records that **both** "Papillary transitional cell carcinoma" (the
REDCap string) and "Papillary urothelial carcinoma" (the term this repair would otherwise propose
as the replacement) carry the `[obs]` marker in `icdo32.sqlite`. That means the string this repair
would want to propose is *also* not the current preferred term, and the contract does not record
what is. This package does not guess. §6 flags it for a direct check before any relabel is finalised.

The other two are not cosmetic, and each gets its own paragraph because a clerk picking the option
today is naming a different disease from the one the code now carries.

### `8311` — the most consequential single option-file defect the project has found

The option reads `8311 - Hypernephroid tumor [obs]`. That is the obsolete `8311/1` term, and
REDCap even carries the `[obs]` tag on it — the list is honest that the wording is dated, but not
honest about what has replaced it.

In ICD-O-3.2, `8311/3` is *Hereditary leiomyomatosis and renal cell carcinoma (HLRCC)
syndrome-associated renal cell carcinoma*. Moch H, et al. *European Urology* 2022;82(5):458–468,
Table 1, assigns **seven** molecularly defined renal carcinomas to this one stem: TFE3-rearranged
renal cell carcinoma, TFEB-altered renal cell carcinoma, ELOC-mutated renal cell carcinoma,
fumarate hydratase–deficient renal cell carcinoma, HLRCC-associated renal cell carcinoma,
succinate dehydrogenase–deficient renal cell carcinoma, and ALK-rearranged renal cell carcinoma.

A clerk selecting `8311` today reads a label for a different lesion entirely and has no way to
know it. The option does not merely understate the evidence behind a diagnosis — it names the
wrong disease outright while pointing at a code that is, in current ICD-O-3.2, both valid and
clinically load-bearing: it is the one stem the WHO 2022 renal classification uses to give the
molecularly defined carcinomas a home, rather than collapsing them into `8312/3` Renal cell
carcinoma, NOS (build contract §0.5). This is the most consequential single option-file defect the
project has found.

### `8504` — a behaviour-2 lesion's name sitting on the group's behaviour-3 slot

The option reads "Intracystic carcinoma, NOS". ICD-O-3.2 carries that exact term, but at
`8504/2`, not `/3`. `8504/3` is *Encapsulated papillary carcinoma with invasion*.
`3.1 to 3.2 – Terms that are changing behaviour` records the move: `8504/3 → /2`.

So the option labels a slot that ICCC-3 Group VI declares at behaviour 3 with the name of a lesion
ICD-O-3.2 now carries at behaviour 2 — in situ, not invasive. A clerk who reads "Intracystic
carcinoma, NOS" and selects it believing they are recording a non-invasive process is, under the
code's current behaviour, recording *Encapsulated papillary carcinoma with invasion* instead — an
invasive diagnosis under a label that describes the opposite.

---

## 4. Pre-flight — run before changing anything

The registry began operating in 2025, and paediatric renal cancer is dominated by Wilms tumour
(`8960/3`), roughly 90% of cases, with clear cell sarcoma of the kidney (`8964/3`) most of the
remainder. Every option in this package names an adult-type carcinoma or a benign/borderline
entity that a paediatric renal series meets rarely if at all. **A count of zero on every affected
option is the likely result — but it has to be run, not assumed.**

| Check | Option(s) | If any records are found |
|---|---|---|
| Retired number | `8965` | The record names a lesion ICD-O-3.2 no longer recognises at this stem. Review the source pathology report. The content now sits at `9013/0`, a behaviour outside the group's declaration — the same class of decision as Group 5's `9514`. There is no automatic destination; the registrar decides per record. |
| Behaviour exclusions | `8966`, `8967`, `8325`, `8361`, `9013`, `8053`, `8060`, `8191`, `8561`, `8040` | Each is a benign or borderline entity recorded under a code Group VI cannot hold. Review each against the source record. No automatic destination — the same registrar-review pattern as Group 5 §2 and the Group 6 build contract §3.2 for `8959/0` and `8959/1`. |
| String drift, cosmetic | `8963`, `8122`, `8131`, `8240` | Nothing to review — the code is correct, only the label text is stale. Relabelling does not touch these records. |
| No current term at behaviour 3 | `8130` | Nothing to review for coding — the code is in scope and the record is readable. But no relabel is possible: every ICD-O-3.2 term at `8130/3` is obsolete (§7.1). Retire or leave as is; the registrar decides. |
| String drift, unverifiable label | `8155` | Nothing to review — the code is correct, the label was simply wrong. |
| String drift, meaning changed | `8311`, `8504` | **Pull the source pathology text for every record on these two values before relabelling anything.** A record on `8311` may have been entered when "hypernephroid tumor" was the working diagnosis, or it may correctly name one of the seven molecularly defined carcinomas the code now carries — the stored value cannot distinguish the two. Same for `8504`: the record may describe a genuinely non-invasive intracystic lesion or an invasive encapsulated papillary carcinoma. The relabel changes what the option *says*; it does not, and cannot, tell you what the clerk *meant* on a record entered before the drift was known. |

Export `record_id`, `diag_main` and `vi_morph`, filtered to `diag_main = '6'`, for the count. For
`8311` and `8504`, pull the linked pathology narrative as well — a count alone does not resolve
those two.

---

## 5. The repair

**`[RETIRED]` label prefixes, never deletions, for Class 1 and Class 2.** Deleting an option makes
any stored value unreadable — the same rule Group 5's package states and this package inherits
without change.

| Option value | Current label | Proposed label | Class |
|---|---|---|---|
| `8965` | `8965 - Nephrogenic adenofibroma` | `[RETIRED] 8965 - Nephrogenic adenofibroma` | 1 — retired number, permanent |
| `8966` | `8966 - Renomedullary interstitial cell tumor` | `[RETIRED] 8966 - Renomedullary interstitial cell tumor` | 2 — behaviour exclusion |
| `8967` | `8967 - Ossifying renal tumor` | `[RETIRED] 8967 - Ossifying renal tumor` | 2 |
| `8325` | `8325 - Metanephric adenoma` | `[RETIRED] 8325 - Metanephric adenoma` | 2 |
| `8361` | `8361 - Juxtaglomerular tumor` | `[RETIRED] 8361 - Juxtaglomerular tumor` | 2 |
| `9013` | `9013 - Adenofibroma, NOS` | `[RETIRED] 9013 - Adenofibroma, NOS` | 2 |
| `8053` | `8053 - Squamous cell papilloma, inverted` | `[RETIRED] 8053 - Squamous cell papilloma, inverted` | 2 |
| `8060` | `8060 - Squamous papillomatosis` | `[RETIRED] 8060 - Squamous papillomatosis` | 2 |
| `8191` | `8191 - Embryonal adenoma` | `[RETIRED] 8191 - Embryonal adenoma` | 2 |
| `8561` | `8561 - Adenolymphoma` | `[RETIRED] 8561 - Adenolymphoma` | 2 |
| `8040` | `8040 - Small cell carcinoma, NOS` | `[RETIRED] 8040 - Small cell carcinoma, NOS` | 2 — double defect; `8041` already carries the correct code and label, so no replacement option is needed |

**For Class 1, `[RETIRED]` is a permanent state** — see §1. **For Class 2, `[RETIRED]` marks the
option out of scope under the current behaviour-3 declaration only.** If the registrar rules that
the registry wants a home for benign or borderline renal entities, these ten numbers are still
live ICD-O-3.2 codes and could be un-retired, or moved to a field the registry creates for that
purpose, without needing anything from IARC.

**Relabel, not retire, for Class 3** — the code stays in scope, only the text is wrong:

| Option value | Current label | Proposed label |
|---|---|---|
| `8963` | `8963 - Malignant rhabdoid tumor` | `8963 - Rhabdoid tumor, NOS` |
| `8122` | `8122 - Transitional cell carcinoma, spindle cell` | `8122 - Urothelial carcinoma, sarcomatoid` |
| `8130` | `8130 - Papillary transitional cell carcinoma` | **no relabel is possible — ICD-O-3.2 has no current term at `8130/3`; see §7.1** |
| `8131` | `8131 - Transitional cell carcinoma, micropapillary` | `8131 - Urothelial carcinoma, micropapillary` |
| `8240` | `8240 - Carcinoid tumor, NOS` | `8240 - Neuroendocrine tumor, NOS` |
| `8155` | `8155 - Vipoma, malignant` | `8155 - Vipoma` |
| `8311` | `8311 - Hypernephroid tumor [obs]` | `8311 - Hereditary leiomyomatosis and renal cell carcinoma (HLRCC) syndrome-associated renal cell carcinoma` |
| `8504` | `8504 - Intracystic carcinoma, NOS` | `8504 - Encapsulated papillary carcinoma with invasion` |

**No renumbering, for either kind of repair.** `vi_morph` stores the code itself as the option
value (§0), so every proposed change here is a label edit, never a value edit. A record already
holding `8311` keeps holding `8311` after the relabel; only the text a clerk sees when the record
is reviewed changes. `vi_extended` and `vi_subgroup` key on the value, not the label, so neither
calculated field is touched by anything in this table — including the `8967` retirement, which
does not interact with the separate `[vi_morp]` typo noted in §0 and §6.

**No appends.** The three codes the tool's inventory carries and REDCap does not offer — `8023/3`,
`8054/3`, `8482/3` — go on `docs/codes-awaiting-redcap.md`, not here (Task B of this build).

---

## 6. What the lookup tool already does correctly

The discrepancy this package documents is entirely on the REDCap side. Four things the tool already
gets right, so the reader knows which side of the nineteen findings the fault sits on:

- **`build/generate_group_inventory.py --group VI` returns 90 usable codes, not 98.** It joins
  `ICCC-2017.sqlite`'s behaviour-3 declaration against `icdo32.sqlite` directly, so all eleven
  Class 1 and Class 2 findings are excluded automatically — none of them exists in ICD-O-3.2 at
  behaviour 3, and the generator never offers a code that fails that join. `8965` returns zero rows
  at any behaviour, so it cannot appear even as an out-of-behaviour entry.
- **`morphology_name` in `group_06_dt.json` is the ICD-O-3.2 preferred term, read from
  `icdo32.sqlite`, never transcribed from the REDCap option file.** The tool already emits
  "Rhabdoid tumor, NOS", not "Malignant rhabdoid tumor"; it already emits the full HLRCC-associated
  renal cell carcinoma preferred term at `8311/3`, not "Hypernephroid tumor". None of the eight
  Class 3 drifts reaches a clerk through the tool. They reach a clerk only if they open the REDCap
  dropdown directly, which is the whole reason this repair package exists.
- **`8311/3` and `8312/3` are already routed correctly.** Build contract §0.5 records that the tool
  does not collapse the seven molecularly defined renal carcinomas onto `8312/3` Renal cell
  carcinoma, NOS — it routes six of them, and ALK-rearranged renal cell carcinoma, to `8311/3`
  specifically. The option-file defect in §3 exists entirely outside the tool.
- **Group VI's names are checked against `icdo32.sqlite`, not against the option file.** Build
  contract §8 moves Group VI onto `check_icdo32_round_trip()` and makes `check_redcap_exact_names()`
  step aside, exactly as Groups 3 and 4 already do. That is the stronger question — *is this a real
  ICD-O-3.2 term for this code at this behaviour?* — and it rejects the `(code, term)` pairs the
  option list carries that the database does not, where the option-file check would inherit them.
  The eight Class 3 strings are not discarded: they move to the alias file, where they are checked
  the other way round, so a clerk who types "hypernephroid tumor" still reaches the right place
  while the tool never *emits* that name. Neither check keys off `redcap_option_verified` — that
  flag was authored to mean "not yet checked", was once read as "exempt", and six drifted names
  passed a green build on the strength of it.

---

## 7. What needs the registrar

Scoped to this REDCap repair package. Build contract §11 carries the broader Group VI registrar
list; these four are specific to `vi_morph`.

1. **`8130` cannot be relabelled, because there is no current term to relabel it to — a third
   class of finding, and the only one of its kind in this package.** Queried directly against
   `icdo32.sqlite` on 22 September 2026: `8130` carries exactly six terms across three behaviours,
   and **both of the two at behaviour 3 carry `[obs]`**:

   | | Term | `obs` |
   |---|---|---|
   | `8130/1` Preferred | Papillary urothelial neoplasm of low malignant potential | — |
   | `8130/1` Synonym | Papillary transitional cell neoplasm of low malignant potential | — |
   | `8130/2` Preferred | Papillary urothelial carcinoma, non-invasive | — |
   | `8130/2` Synonym | Papillary transitional cell carcinoma, non-invasive | — |
   | `8130/3` Preferred | Papillary urothelial carcinoma | **`[obs]`** |
   | `8130/3` Synonym | Papillary transitional cell carcinoma | **`[obs]`** |

   `SELECT count(*) … WHERE code4='8130' AND behaviour='3' AND (obs IS NULL OR obs='')` returns
   **0**. None of the four IARC 3.1→3.2 change documents mentions `8130` anywhere, so the marker is
   inherited from ICD-O-3.1 and is not a 3.2 change. The reason is visible in the table: the
   non-invasive and low-malignant-potential forms kept current terms, and the invasive form did not,
   because an invasive papillary urothelial carcinoma is now coded `8120/3 Transitional cell
   carcinoma, NOS` — the "papillary" qualifier was dropped at behaviour 3.

   So `8130` is neither a deleted number (Class 1) nor out of behaviour (Class 2) nor fixably
   drifted (Class 3): it is a code ICD-O-3.2 still carries at behaviour 3 with **no current term on
   it**. WHO 2022 Table 1 does not list `8130` under the kidney at all. **The registrar's decision
   is whether the option is retired or left as is with its obsolete label**, and it is not a
   relabel either way. The tool is unaffected — `8130` is an adult urothelial code with no Group VI
   decision-tree branch, and its entry records the obsolescence in its `coding_note`.
2. **Whether the ten Class 2 numbers get a home outside Group VI, or stay `[RETIRED]`
   indefinitely.** Same open question as build contract §11.6. This package cannot answer it; it
   only establishes that Group VI, as declared, cannot hold them.
3. **`8965` records, if pre-flight finds any, need individual review**, the same as Group 5's
   `9514` — whether the case is recoded to `9013/0`, held outside Group VI, or resolved some other
   way is a per-record registrar decision, not a batch operation.
4. **The `vi_extended` `[vi_morp]` typo** (§0) is a live, independent defect on the same code this
   package retires. It is outside this package's scope — it is a calculated-field formula, not an
   option-list entry — but it is worth its own correction, and it will not be fixed by anything in
   §5.

---

*Every finding verified 22 September 2026 against `ICD coding/ICD-O-3.2/icdo32.sqlite` (IARC final
workbook, 9 October 2020), `ICCC-2017.sqlite`, the four IARC 3.1→3.2 change documents, Moch H, et
al. *European Urology* 2022;82(5):458–468, and `ICD coding/RedCap Options/Group 6 - Renal
Tumors.md` for the live `vi_morph` option list (98 options, confirmed by direct count). Field
storage confirmed against `Registry Data/data dictionary/Diagnosis.md` and
`EAFYA IMPORT/redcap_field_choices.json`. See `docs/group_06_build_contract.md` §0.2, §0.3, §0.5,
§0.6, §2 and §11.*
