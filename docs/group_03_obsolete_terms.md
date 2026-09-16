# Group 3 — the `[obs]` marker, and the eleven terms that left the decision tree

**Registrar's rulings, 14 September 2026.** Terms IARC marks obsolete come out of the decision
tree. Two codes were removed under that ruling and then **restored**, because the ruling is about
*terms* and those two removals had treated it as being about *codes*. This file records what
`[obs]` actually marks, which codes left, and which came back.

---

## 1. What `[obs]` marks: the term, not the number

The column is IARC's own, carried straight through from the source workbook:

| | |
|---|---|
| Source file | `ICD-O-3.2_final_update09102020.xls` — IARC's **final** ICD-O-3.2, 9 October 2020 |
| SHA-256 | `7ca51dcb66107d6462b43212b26aa65d52f6b0e306c6295e8c751416b3278a21` |
| Sheet | `ICD-O-3.2 Morphology`, 2,955 data rows |
| Header, verbatim | `ICDO3.2 \| Level \| Term \| Code reference \| obs \| See also \| See note \| Includes \| Excludes \| Other text` |
| Converted by | `ICD coding/ICD-O-3.2/convert_icdo32.py` |
| Retrieved from | <http://www.iacr.com.fr/images/Newsflash/ICD-O-3.2_final_update09102020.xls> |

**285 of the 2,955 rows carry `[obs]`, and it is the column's only value.** Three independent
checks establish that it marks a *term string* and never retires a code:

**a. Inside the file.** 40 (code, behaviour) pairs carry `[obs]` and non-`[obs]` terms at the same
time. `9400/3` Astrocytoma, NOS has seven live terms and two marked `[obs]`. A marker that killed
the number could not do that.

**b. IARC's word for a dead number is "deleted", and it keeps a separate list.**
[*Deleted codes and their terms*](http://www.iacr.com.fr/images/Newsflash/3.1%20to%203.2%20-%20Deleted%20codes%20and%20their%20terms-09102020.pdf)
(IACR Working Group on ICD-O Updates, prepared by Mark Short, Australian Institute of Health and
Welfare, 9 October 2020) names eight deleted four-digit 9xxx codes — 9150, 9670, 9728, 9729, 9826,
9836, 9991, 9992. Inside that same document `[obs]` appears on individual synonyms sitting *under
live codes*: "Hemangiopericytic meningioma (C70._) **[obs]**" beneath 9150/1, "FAB L3 **[obs]**"
beneath 9826/3.

**c. A registry coding table keyed to ICD-O-3.2 says it in one line.** The Belgian Cancer
Registry's *WHO classification of tumours of the central nervous system*, built on **CNS5 2021
and ICD-O-3.2**, assigns:

```
Astroblastoma, MN1-altered                   *9430/3  (C71._)
Primary intracranial sarcoma, DICER1-mutant  *9480/3  (C70._; C71._; C72._)
```

and footnotes the asterisk: **"These entities have undergone a change in terminology of a
previous code."** The terminology changed; the number did not. That is the whole finding, stated
by a national registry within ICD-O-3.2 itself.

**d. ICD-O-3.2 never touched astroblastoma.** The
[full 3.1 → 3.2 change listing](http://www.iacr.com.fr/images/Newsflash/ICD-O-3.2Changes_update09102020.xls)
carries 1,094 change rows and no row for 9430 or 9480, and no status in it means "made obsolete" —
the statuses are new terms, moves between preferred/synonym/related, behaviour changes and code
changes. The marker is inherited from ICD-O-3.1 or earlier.

> **Scope.** Everything above is ICD-O-3.2. This tool codes to ICD-O-3.2 and to nothing else;
> later editions are neither evidence nor a plan here.

Reproduce the obsolete set:

```sql
SELECT code4, behaviour, level, term
FROM   icd_o_3_2_morphology
WHERE  trim(coalesce(obs,'')) = '[obs]'
ORDER BY code4, behaviour;
```

---

## 2. The test a code has to fail before it leaves the tree

Every Group III entry was checked. **13 of the 108** have no non-obsolete term at their behaviour
in ICD-O-3.2 — for all thirteen, *every* row on that code at that behaviour is marked, preferred
terms and synonyms alike.

That finding is correct, but it is not sufficient on its own. The question a decision tree has to
answer is not "does ICD-O-3.2 still print a usable string" but:

> **Does a current WHO classification entity live on this stem?**

Two of the thirteen answer yes, and they are back in the tree. Eleven answer no — no WHO CNS5
entity is carried on any of their stems — and they stay out.

---

## 3. The two that came back

| Code | ICD-O-3.2 term | WHO CNS5 entity carried on that code | ICCC-3 |
|---|---|---|---|
| `9430/3` | Astroblastoma `[obs]` | Astroblastoma, MN1-altered | IIId3 |
| `9480/3` | Cerebellar sarcoma, NOS `[obs]` | Primary intracranial sarcoma, DICER1-mutant | IIIc1 |

Both are WHO CNS5 Table 1 types — Louis DN, et al. *The 2021 WHO Classification of Tumors of the
Central Nervous System: a summary.* Neuro-Oncology 2021;23(8):1231–1251, Table 1, pp. 1233–1235;
astroblastoma under Circumscribed astrocytic gliomas, the DICER1-mutant sarcoma under Mesenchymal,
non-meningothelial tumours.

**Eight branches and one node fallback were restored** (seven in `st_astroblastoma_gate`, one in
`pf_family_triage`). The obsolete wording stays off the clerk's diagnosis line: the ICD-O-3.2 term
is shown as the code's label, and `diagnosis_rendering.who_diagnosis` carries the CNS5 name.

**9480 carries a caveat.** ICCC-3 files 9480 in **IIIc1 Medulloblastomas**, so a DICER1-mutant
primary intracranial sarcoma coded 9480/3 counts in the medulloblastoma subgroup. That is ICCC-3's
own mapping, not a coding error. The tool has no dedicated DICER1-mutant route yet — see
`docs/TODO.md`.

---

## 4. The eleven that stay out

| Code | Obsolete ICD-O-3.2 term | ICCC-3 | Now emits | Why that target |
|---|---|---|---|---|
| `8280/0` | Acidophil adenoma | IIIe1 | `8272/0` Pituitary adenoma, NOS | the subgroup's own non-obsolete NOS; somatotroph/lactotroph lineage survives in the entity annotation |
| `8280/3` | Acidophil carcinoma | IIIe1 | `8272/3` Pituitary carcinoma, NOS | non-obsolete equivalent |
| `8281/0` | Mixed acidophil-basophil adenoma | IIIe1 | `8272/0` Pituitary adenoma, NOS | non-obsolete NOS |
| `8281/3` | Mixed acidophil-basophil carcinoma | IIIe1 | `8272/3` Pituitary carcinoma, NOS | non-obsolete equivalent |
| `8300/0` | Basophil adenoma | IIIe1 | `8272/0` Pituitary adenoma, NOS | corticotroph lineage survives in the entity annotation |
| `8300/3` | Basophil carcinoma | IIIe1 | `8272/3` Pituitary carcinoma, NOS | non-obsolete equivalent |
| `9360/1` | Pinealoma | IIIe3 | `8000/1` Neoplasm, uncertain whether benign or malignant | no non-obsolete pineal NOS exists. `9361/1` and `9362/3` each assert a type the file did not state |
| `9410/3` | Protoplasmic astrocytoma | IIIb | `9400/3` Astrocytoma, NOS | CNS5 subsumes protoplasmic astrocytoma into diffuse astrocytoma |
| `9460/3` | Oligodendroblastoma | IIId1 | `9450/3` Oligodendroglioma, NOS | Pathway Revision 2 §4.8 already directs these to `9450` |
| `9472/3` | Medullomyoblastoma | IIIc1 | `9470/3` Medulloblastoma, NOS | medulloblastoma is established; the rhabdomyoblastic differentiation survives in the coding note |
| `9535/0` | Hemangioblastic meningioma | IIIe5 | **no code — refers to Group IX** | not a meningioma at all; see §4.1 |

### 4.1 `9535/0` refers out of Group III — corrected 15 September 2026

The first correction sent this to `9530/0` Meningioma, NOS. That was wrong, and it was wrong in
the direction that matters: it asserted *meningioma* for a tumour the classification says is not
one.

IARC marks both ICD-O-3.2 terms on the code `[obs]` — `Hemangioblastic meningioma` and its
synonym `Angioblastic meningioma`. The entity they named is meningeal haemangiopericytoma, and
WHO CNS5 retires that term outright:

> "The term *hemangiopericytoma* has been retired, with the tumor now termed only Solitary
> fibrous tumor (rather than the hybrid term *Solitary fibrous tumor/hemangiopericytoma* used in
> the 2016 CNS classification)."
>
> — Louis DN, et al. *The 2021 WHO Classification of Tumors of the Central Nervous System: a
> summary.* Neuro-Oncology 2021;23(8):1231–1251, **p. 1248**

On that same page the paper makes meningioma **a single type with fifteen morphological
subtypes**, and neither *haemangioblastic* nor *angioblastic* is among them — neither word occurs
anywhere in the paper.

| If the tumour is | ICD-O-3.2 | ICCC-3 |
|---|---|---|
| meningeal haemangiopericytoma → solitary fibrous tumour | `8815` | IXb1 — **Group IX** |
| a true haemangioblastoma | `9161` | IXd8 — **Group IX** |

Either reading leaves Group III. The `mn_he_subtype` option that captures those words now carries
`refer_group: 9` and emits no code; the two `mn_grade_assembly` rules that graded it as a
meningioma were deleted, and `build/induce_flow.py` was re-run so the flow chart's witness count
matches. `9535/0` is retained in `morphology_entries[]`, flagged, unreachable.

---

**16 branches across four trees remain re-pointed**, plus one entry-level fallback: `9361/1`
Pineocytoma fell back to `9360`, which would have routed a case into an obsolete term by the back
door. It now falls back to `8000/1`.

---

## 5. What was deliberately *not* done

**The `morphology_entries[]` objects are retained**, each flagged `obsolete_term: true` with
`obsolete_source` naming the evidence above. Only the *decision tree* stopped reaching them.

1. A historical record already coded `9472` still resolves. Deleting the entry would break it.
2. The alias file routes the words. A clerk who types "medullomyoblastoma" gets an answer — the
   code the tree now emits — rather than silence.
3. It is reversible per code, as the two restorations show.

Each re-pointed branch records `superseded_obsolete_code` and a coding note giving the original
code, the reason and this source, so the next author does not "correct" it back.

The two restored entries carry `obsolete_term_string: true` instead — the term is obsolete, the
code is current, and the distinction is now in the data rather than only in this file.

---

*Generated 2026-09-14. The obsolete set is re-derived from `icdo32.sqlite` on every run of the
merge script, which aborts if the hard-coded list and the database disagree — so this file cannot
drift from the database without the build saying so.*
