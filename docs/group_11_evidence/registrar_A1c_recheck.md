# Group 11, registrar review A1 (c): recheck of the three "retired or downgraded" instances

Prepared 8 October 2026 for the registrar. This file establishes facts. It does not decide any coding.

Sources read: Nicholson 2022 (Table 1 read from PDF page 2; text through the snippet tool), ICCR Lung 4th edition
(Table 1 read from PDF pages 10 and 11), Chen 2026 (snippet tool), Goldman-Lévy 2025 (PDF pages 5 and 6 read as
images), Milman 2023 (PDF pages 13 to 15 read as images), the Rules A to K extract (snippet tool; printed page = PDF
page + 13), the ICD-O-3.2 table (`icdo32.sqlite`, 2,955 rows, table `icd_o_3_2_morphology`) and the ICCC-2017
database (`ICCC-2017.sqlite`). Nothing was fetched. Quotations are limited to one short quotation per instance;
all other statements are paraphrase with the page.

---

## c1. Lung: "bronchioloalveolar carcinoma" and "alveolar carcinoma" (Q60, addendum gap 7)

### (1) The claim as the evidence file states it

Registrar review A1 (c): "No entity at 8252; the term was defined as non-invasive. Choices: 8252/3, the current
adenocarcinoma code, or adenocarcinoma in situ (not registered)." Cited to Nicholson 2022, PDF p. 9, and Chen 2026,
PMC section 2.

`XIf4_lung_pleura.json`:
- `entities[38]` (code 8252): "ICD-O-3.2 keeps this preferred term current, but the WHO 2021 lung classification
  prints no entity at 8252. Nicholson 2022 says bronchioloalveolar carcinoma was defined as a noninvasive tumour, so
  an older report using the term may describe an adenocarcinoma in situ (/2)." Cite: Nicholson 2022, PDF p. 9.
- `entities[39]` (code 8251): "Every /3 term at 8251 is [obs] in ICD-O-3.2 ... Chen 2026 names alveolar carcinoma,
  an [obs] ICD-O-3.2 synonym at this code, as an epithelial lung tumour of children." Cites: Nicholson 2022, PDF p. 2;
  Chen 2026, section 2.
- `data_gaps[6]` and `code_currency[4]` restate the same points.

The claim has five parts, checked separately below.

### (2) What the sources say

**Part a. "The WHO 2021 lung classification prints no entity at 8252."** CONFIRMED.
Nicholson 2022 Table 1 (printed p. 363, PDF p. 2, read from the page image) and ICCR Lung 4th edition Table 1 (printed
pages 10 and 11 of 23, read from the page image) print the same adenocarcinoma rows. Neither table has a row coded
8252 or a row named bronchioloalveolar carcinoma. The rows in the adenocarcinoma block are:

| Table row | Code |
|---|---|
| Atypical adenomatous hyperplasia | 8250/0 |
| Adenocarcinoma in situ, non-mucinous (nonmucinous in Nicholson) | 8250/2 |
| Adenocarcinoma in situ, mucinous | 8253/2 |
| Minimally invasive adenocarcinoma, non-mucinous | 8256/3 |
| Minimally invasive adenocarcinoma, mucinous | 8257/3 |
| Lepidic adenocarcinoma | 8250/3 |
| Acinar adenocarcinoma | 8551/3 |
| Papillary adenocarcinoma | 8260/3 |
| Micropapillary adenocarcinoma | 8265/3 |
| Solid adenocarcinoma | 8230/3 |
| Invasive mucinous adenocarcinoma | 8253/3 |
| Mixed invasive mucinous and non-mucinous adenocarcinoma | 8254/3 |
| Colloid adenocarcinoma | 8480/3 |
| Fetal adenocarcinoma | 8333/3 |
| Adenocarcinoma, enteric type | 8144/3 |
| Adenocarcinoma, NOS | 8140/3 |
| Alveolar adenoma (adenoma block) | 8251/0 |

The Nicholson table has no footnote on bronchioloalveolar carcinoma. The ICCR table footnote b says only that the codes
are from ICD-O-3.2, and the dagger footnote marks labels whose terminology changed from a previous code
(bronchiolar adenoma and two other rows; not the adenocarcinomas). The word "bronchioloalveolar" appears once in all
of Nicholson 2022 apart from a reference to bronchoalveolar lavage, and not at all in the ICCR Lung dataset.

**Part b. "The term was redefined as non-invasive (adenocarcinoma in situ, minimally invasive, lepidic, invasive
mucinous)."** NOT CONFIRMED by the files I may read. The one sentence the claim rests on is Nicholson 2022, printed
p. 370 (PDF p. 9). It is about the mucinous tumour only. It explains why the WHO name for the mucinous invasive tumour
was proposed:

> "confusion with mucinous bronchioloalveolar carcinoma, of which the primary definition was a noninvasive tumor"

The sentence closes a statement that the term invasive mucinous adenocarcinoma was first proposed in the
IASLC/ATS/ERS classification of adenocarcinoma (reference 16) to avoid that confusion. It says nothing about non-mucinous bronchioloalveolar
carcinoma, nothing about the term being retired, and does not map the old term to adenocarcinoma in situ, minimally
invasive adenocarcinoma, lepidic adenocarcinoma and invasive mucinous adenocarcinoma. The evidence file's label "term
retired by the WHO" (`entities[38].who_term`) is an inference, not a statement in Nicholson or ICCR. Whether the
2011 IASLC/ATS/ERS paper, or the WHO book itself, states that history is outside my files, so I do not assert it.

**Part c. "Where did the old mucinous bronchioloalveolar carcinoma go?"** Not stated by the WHO or ICCR tables. Two
facts support 8253/3: ICD-O-3.2 files "Bronchiolo-alveolar carcinoma, mucinous" as an [obs] synonym of 8253/3 (see
section 3), and the Nicholson sentence above links the invasive mucinous adenocarcinoma name (8253/3 in Table 1) to the
old mucinous tumour. The sources do not say the old mucinous tumour all became 8253/3: Nicholson says only that its
primary definition was non-invasive, and Table 1 also holds adenocarcinoma in situ, mucinous (8253/2) and minimally
invasive adenocarcinoma, mucinous (8257/3).

**Part d. "Chen 2026 reports an 'alveolar carcinoma' in a child."** NOT CONFIRMED as a case report. The phrase occurs
once, in the Introduction (PMC section 2), in a general sentence on how primary pulmonary tumours of childhood are
categorised: five categories by histological origin, with "alveolar carcinoma" named as the example of epithelial
tumours. The sentence carries no case count and no reference at that point in the text. The 36-child series itself
(PMC section 9) contains 11 histological types: pleuropulmonary blastoma (16), pulmonary mucoepidermoid carcinoma (4),
pulmonary sclerosing pneumocytoma (4), and the remaining 12 children spread over eight other types (hamartoma, Langerhans cell histiocytosis,
pulmonary blastoma, mature teratoma, Hodgkin lymphoma, carcinoid, alveolar soft part sarcoma, Ewing sarcoma). No
alveolar carcinoma and no bronchioloalveolar carcinoma is among them. So Chen 2026 names the term as a category of
childhood lung tumour in its background text and reports no child with it. The evidence file's wording "names alveolar
carcinoma ... as an epithelial lung tumour of children" is accurate; the review table's "a child's report of
'alveolar carcinoma'" overstates it.

**Part f. The Ozkan 2024 series.** `data_gaps[6]` also cites Ozkan 2024 (bronchoalveolar carcinoma, 2% of 211
children). Ozkan 2024 is not among my files, so this cannot be settled here.

### (3) ICD-O-3.2 rows

Query: `select icdo3_2, level, term, code_reference, obs from icd_o_3_2_morphology where icdo3_2 like '825_/%' or
icdo3_2 like '8250/%' ... order by icdo3_2`. The four columns are code, level, term, site reference; [obs] is the
`obs` column.

```
8250/2 Preferred  Adenocarcinoma in situ of lung, non-mucinous        (C34._)
8250/3 Preferred  Lepidic adenocarcinoma                              (C34._)
8250/3 Synonym    Bronchiolo-alveolar adenocarcinoma, NOS             (C34._) [obs]
8250/3 Synonym    Bronchiolo-alveolar carcinoma, NOS                  (C34._) [obs]
8250/3 Synonym    Alveolar cell carcinoma                             (C34._) [obs]
8250/3 Synonym    Bronchiolar adenocarcinoma                          (C34._) [obs]
8250/3 Synonym    Bronchiolar carcinoma                               (C34._) [obs]
8251/0 Preferred  Alveolar adenoma                                    (C34._)
8251/3 Preferred  Alveolar adenocarcinoma                             (C34._) [obs]
8251/3 Synonym    Alveolar carcinoma                                  [obs]
8252/3 Preferred  Bronchiolo-alveolar carcinoma, non-mucinous         (C34._)
8252/3 Synonym    Bronchiolo-alveolar carcinoma, Clara cell           (C34._) [obs]
8252/3 Synonym    Bronchiolo-alveolar carcinoma, type II pneumocyte   (C34._) [obs]
8253/2 Preferred  Adenocarcinoma in situ of lung, mucinous            (C34._)
8253/3 Preferred  Adenocarcinoma of lung, mucinous                    (C34._)
8253/3 Synonym    Bronchiolo-alveolar carcinoma, mucinous             (C34._) [obs]
8253/3 Synonym    Bronchiolo-alveolar carcinoma, goblet cell type     (C34._) [obs]
8254/3 Preferred  Adenocarcinoma of lung, mixed mucinous and non-mucinous (C34._)
8254/3 Synonym    Bronchiolo-alveolar carcinoma, mixed mucinous and non-mucinous (C34._) [obs]
8254/3 Synonym    Bronchiolo-alveolar carcinoma, Clara cell and goblet cell type (C34._) [obs]
8254/3 Synonym    Bronchiolo-alveolar carcinoma, indeterminate type   (C34._) [obs]
8254/3 Synonym    Bronchiolo-alveolar carcinoma, type II pneumocyte and goblet cell type (C34._) [obs]
8256/3 Preferred  Minimally invasive adenocarcinoma, non-mucinous     (C34._)
8257/3 Preferred  Minimally invasive adenocarcinoma, mucinous         (C34._)
```

The claim that "ICD-O-3.2 keeps 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous as a current Preferred
term" is CONFIRMED: the Preferred row has no [obs] flag. "Every 8251/3 term is [obs]" is CONFIRMED: the two rows at
8251/3 (Preferred "Alveolar adenocarcinoma" and Synonym "Alveolar carcinoma") are both flagged. Two facts the evidence
file does not state:
- The plain term "Bronchiolo-alveolar carcinoma, NOS" is an [obs] synonym at 8250/3 Lepidic adenocarcinoma, not at
  8252/3. Within ICD-O-3.2 the qualified term is current at 8252/3 and the unqualified term is obsolete at 8250/3.
- The 8252/3 synonyms (Clara cell, type II pneumocyte) are [obs]; only the Preferred term is current.

### (4) ICCC-2017 placement at the site

8250, 8251, 8252, 8253, 8254, 8256 and 8257 are all held by XIf4 "Carcinomas of lung", range C34.0 to C34.9, behaviour
/3. The XIf4 range lists behaviour /3 only, so the /2 rows (8250/2, 8253/2) are in no ICCC-2017 range.

### (5) Verdict: PARTLY CONFIRMED

Confirmed: the WHO and ICCR tables hold no entity at 8252; ICD-O-3.2 keeps 8252/3 Preferred current; every term at
8251/3 is [obs]; the tables hold the current adenocarcinoma codes in the table above.
Fails: (i) no source I read says the term bronchioloalveolar carcinoma was redefined or retired as a whole; Nicholson
says only that the mucinous tumour was primarily defined as non-invasive; (ii) Chen 2026 reports no child with
alveolar carcinoma, it names the term in background text; (iii) the destination of the old mucinous tumour is not
stated by the WHO or ICCR tables.
Not settled from my files: Ozkan 2024; the WHO book or IASLC/ATS/ERS 2011 on how the old term was retired.

### (6) For information only: what Rules A to K would give

The rules contain no rule on obsolete terms. They give a lookup, not a currency ruling.
- Rule H (printed p. 15, PDF p. 2): the site code is C34._ and the term's printed site (C34._) agrees.
- Rule F (printed p. 15): the fifth digit follows the behaviour the pathologist states, even when the exact term is
  not listed. A report that states the tumour is non-invasive or in situ takes /2; the rule does not say which code.
- Rule J (printed p. 16, PDF p. 3) and Rule K (printed p. 16): the words "bronchioloalveolar carcinoma" with no
  qualifier appear in ICD-O-3.2 only as the [obs] synonym at 8250/3. Rule K does not apply, since the report names
  no second modifying term. A report that says "non-mucinous" finds the Preferred term at 8252/3; a report that says
  "mucinous" finds the [obs] synonym at 8253/3.
- Rule H applied to "alveolar carcinoma": the only listing is the [obs] synonym at 8251/3.

---

## c2. Skin: "cribriform carcinoma" (Q33)

### (1) The claim as the evidence file states it

Registrar review A1 (c): ICD-O-3.2 holds 8201/3 Cribriform carcinoma, NOS (no ICCC-2017 range holds it at skin); the
WHO "downgraded to cutaneous cribriform tumour, which ICD-O-3.2 does not name"; held. Cited to Goldman-Lévy 2025,
PDF p. 5.

`XIe_skin_carcinoma.json`: `entities[71]` (Cutaneous cribriform tumour, behaviour recorded as "0", decision
"exclusion", no code): "The WHO 5th edition downgrades cribriform carcinoma of skin to an indolent cribriform tumour.
ICD-O-3.2 prints no term for the tumour; it is not registered." `entities[72]` (code 8201, decision "registrar"):
"ICD-O-3.2 codes Cribriform carcinoma, NOS 8201/3, and no ICCC-2017 range holds 8201 at skin. The WHO 5th edition says
the skin tumour has no reported recurrence or metastasis and renames it cribriform tumour." Cite on both:
Goldman-Lévy 2025, PDF p. 5.

### (2) What the source says

Goldman-Lévy 2025 (Histopathology 88:555-568; printed p. 559, PDF p. 5, read from the page image), in the section
"Appendageal tumours":

> "is now downgraded to cribriform tumour"

The full sentence says that cribriform carcinoma is now downgraded to cribriform tumour owing to the absence of
reported recurrences and metastases. The next paragraph defines "Cutaneous cribriform tumour" as an indolent adnexal
neoplasm with apocrine differentiation, composed of epithelial cells with eosinophilic cytoplasm forming solid and
cribriform structures and small lumina, with no myoepithelial cell layer.

Points the claim leaves out or the source limits:
- The paper says "indolent". It does not say "benign", and it prints no behaviour code and no ICD-O code for the
  tumour. Table 1 (printed p. 560, PDF p. 6) is a table of molecular alterations; cribriform tumour is not in it.
  The evidence file records the behaviour as "0"; that value is an assumption of the evidence file, not a statement
  in the paper.
- The sentence with "downgraded" says "Cribriform carcinoma" without the word skin; the skin context comes from the
  section heading and from the next paragraph, which says "Cutaneous cribriform tumour".
- The paper is a summary of the changes ("key updates"), not the WHO volume. The WHO volume's own code and behaviour
  for the tumour are not in my files.
- No paediatric skin paper in my files was read for this instance (Huang 2019 and Kaloga 2016 are not on my list).

### (3) ICD-O-3.2 rows

Query: `... where icdo3_2 like '8201/%' or term like '%cribriform%' ...`; and a second query for
`term like '%cribriform tumo%'` (zero rows) and `term like '%cutaneous%' and icdo3_2 like '82%'` (one unrelated row,
8247/3 Primary cutaneous neuroendocrine carcinoma).

```
8201/2 Preferred  Cribriform carcinoma in situ                (C50._)
8201/2 Synonym    Ductal carcinoma in situ, cribriform type   (C50._)
8201/3 Preferred  Cribriform carcinoma, NOS                   (no site reference)
8201/3 Synonym    Ductal carcinoma, cribriform type           (C50._)
8201/3 Related    Cribriform comedo type carcinoma            (C18._, C19.9, C20.9)
8201/3 Synonym    Adenocarcinoma, cribriform comedo type      (C18._, C19.9, C20.9)
8523/3 Related    Infiltrating duct and cribriform carcinoma (C50._)
```

No [obs] flag on any 8201 row. ICD-O-3.2 holds no "cutaneous cribriform tumour" or "cribriform tumour" term at any
code, and no 8201/0 or 8201/1 row. So "a term ICD-O-3.2 does not name" is CONFIRMED. The Preferred term 8201/3
carries no site; the breast and colorectal site references sit on synonyms and related terms.

### (4) ICCC-2017 placement at the site

The skin carcinoma range, XIe range 124, covers C44.0 to C44.9 (plus C51.9, C60.9, C63.2), behaviour /3, histology
8010-8041, 8050-8075, 8078, 8081, 8082, 8090-8098, 8100-8110, 8140, 8143, 8147, 8190, 8200, 8211, 8240, 8246, 8247, 8260,
8263, 8310, 8320, 8323, 8390-8420, 8430, 8480, 8540, 8542, 8560, 8570-8573. It holds 8200 and 8211 but not 8201. The
melanoma range XId (range 123) holds 8720-8780 and 8790 only. A query of every range that holds 8201 against a
topography segment covering C44 (440 to 449) returns zero rows. The ranges that hold 8201 are: VIb (C64.9), VIIb
(C22.0, C22.1), Xd (C56.9, C62), XIb (C73.9), XIc (C11), and XIf1 to XIf11 at their own sites. None covers C44.

### (5) Verdict: CONFIRMED

Confirmed as the evidence file and the review table state it: the WHO downgrade (Goldman-Lévy 2025, printed p. 559),
ICD-O-3.2 8201/3 Preferred as a current term, no ICD-O-3.2 term for the new tumour, and no ICCC-2017 range holding
8201 at skin. Two qualifications for the ruling: the source says "indolent", not "benign", and states no behaviour
code; and the new tumour's own WHO code is not in the source I read, so the behaviour /0 in the evidence file is not
sourced.

### (6) For information only: what Rules A to K would give

- Rule H (printed p. 15): 8201/3 Preferred has no printed site, so the stated site C44._ is used. The rule that the
  term's printed site is used applies only when no site is stated.
- Rule F (printed p. 15): a report that says "cribriform carcinoma" is coded 8201/3 with the stated malignant
  behaviour. A report that calls the tumour a "cribriform tumour" with no behaviour stated has no listed term, and
  the rules do not say which code it takes.
- The rules say nothing about a WHO downgrade. A report using the old term codes 8201/3 under the rules; whether the
  tool records it is the registrar's ruling.

---

## c3. Eye: "oncocytic carcinoma" of the lacrimal gland (Q103)

### (1) The claim as the evidence file states it

Registrar review A1 (c): ICD-O-3.2 8290/3 Oxyphilic adenocarcinoma (current); the WHO "removed as obsolete"; held and
not in the eye picker. Cited to Milman 2023, PDF p. 15.

`XIf9_eye.json`: `entities[25]` (code 8290, behaviour 3, sites C69.5): "WHO Eye5 removed oncocytic carcinoma of the
lacrimal gland as an obsolete entity. ICD-O-3.2 keeps 8290/3 current, and the code is in the XIf9 inventory, so the
picker would offer it. The registrar decides whether the eye picker holds it." `code_currency[5]` repeats this.

### (2) What the source says

Milman 2023 (Ocul Oncol Pathol 9:71-95; printed p. 85, PDF p. 15, read from the page image), in the paragraph headed
"Tumors of the Lacrimal Gland and Lacrimal Drainage System (Table 12)":

> "Obsolete entities, such as oncocytic carcinoma, have been removed."

The next sentence says that tumours rarely encountered in the lacrimal gland or controversial there, such as Warthin
tumour, are also removed. That is all the paper says about oncocytic carcinoma.

What the paper does not say:
- It does not say renamed, reclassified, merged into another entity, or "now called". It names no successor.
- The sentence does not itself say "of the lacrimal gland"; it sits in the lacrimal gland and lacrimal drainage
  chapter paragraph, so the removal applies to that chapter.
- It prints no ICD-O code for any lacrimal entity.

What the paper lists now (Table 12, printed p. 82, PDF p. 12; Table 13, printed pp. 83-85, PDF pp. 13-15, both read
as images and text):
- Benign and premalignant epithelial tumours of the lacrimal gland: pleomorphic adenoma, lacrimal gland oncocytoma,
  myoepithelioma, intraductal carcinoma.
- Malignant epithelial tumours of the lacrimal gland: carcinoma ex pleomorphic adenoma, adenoid cystic carcinoma,
  primary ductal adenocarcinoma of the lacrimal gland, secretory carcinoma, mucoepidermoid carcinoma, epithelial-
  myoepithelial carcinoma, acinic cell carcinoma, adenocarcinoma NOS.
- The benign counterpart, lacrimal gland oncocytoma, stays in the classification. The conjunctiva list (Table 3)
  also holds a benign conjunctival oncocytoma. No malignant oncocytic entity is listed at either site.

The paper does not say where an oncocytic carcinoma of the lacrimal gland should go now; adenocarcinoma NOS is the
nearest listed malignant row, and the paper does not say it takes these tumours.

### (3) ICD-O-3.2 rows

Query: `... where icdo3_2 like '8290/%' or term like '%oncocytic%' or term like '%oxyphil%' order by icdo3_2`.

```
8290/0 Preferred  Oxyphilic adenoma                               (no site reference)
8290/0 Synonym    Oncocytic adenoma
8290/0 Synonym    Oncocytoma
8290/0 Related    Follicular adenoma, oxyphilic cell              (C73.9)
8290/0 Related    Hurthle cell adenoma                            (C73.9)
8290/0 Related    Hurthle cell tumor                              (C73.9)
8290/0 Related    Spindle cell oncocytoma                         (C75.1)
8290/0 Related    Oncocytic papillary cystadenoma
8290/3 Preferred  Oxyphilic adenocarcinoma                        (no site reference)
8290/3 Synonym    Oncocytic adenocarcinoma
8290/3 Synonym    Oncocytic carcinoma
8290/3 Related    Hurthle cell carcinoma                          (C73.9)
8290/3 Related    Hurthle cell adenocarcinoma                     (C73.9)
8290/3 Related    Follicular carcinoma, oxyphilic cell            (C73.9)
```

(Other rows with "oncocytic" in the term: 8121/1 Schneiderian and sinonasal papilloma, oncocytic; 8317/3 Hybrid
oncocytic chromophobe tumor; 8342/3 Papillary carcinoma, oncocytic variant (C73.9).)

No [obs] flag on any 8290/3 row. "Oncocytic carcinoma" is a current Synonym of 8290/3. So "ICD-O-3.2 keeps 8290/3
current" is CONFIRMED.

### (4) ICCC-2017 placement at the site

8290 at C69.5 (lacrimal gland and duct) is held by XIf9 "Carcinomas of eye", C69.0 to C69.9, behaviour /3. (8290 is
also held at VIb, Xd, XIb, XIc, XIf1 to XIf8, XIf10 and XIf11 at their own sites, and in IIIe1 at C75.1; none of
these is the eye.)

### (5) Verdict: CONFIRMED

The WHO Eye and Orbit 5th edition removed oncocytic carcinoma as an obsolete entity, as the evidence file says, and
ICD-O-3.2 keeps 8290/3 current with "Oncocytic carcinoma" as a Synonym. One point for the ruling: Milman states a
removal only. It does not rename or reclassify the entity and names no successor, so the facts do not show what a
report of "oncocytic carcinoma of the lacrimal gland" now is, in WHO terms.

### (6) For information only: what Rules A to K would give

- Rule H (printed p. 15): neither the Preferred term nor the Synonym "Oncocytic carcinoma" carries a printed site, so
  the stated site (lacrimal gland, C69.5) is used.
- Rule F (printed p. 15): behaviour follows the report; a report of "carcinoma" is /3.
- The rules say nothing about a WHO removal. Under the rules a report using the old term codes 8290/3, C69.5.

---

## Closing verdict table

| Instance | Claim part | Verdict |
|---|---|---|
| c1 Lung (Q60, gap 7) | WHO 2021 and ICCR tables print no entity at 8252 | Confirmed (Nicholson 2022 Table 1, PDF p. 2; ICCR Lung Table 1, PDF pp. 10-11, images) |
| c1 | ICD-O-3.2 keeps 8252/3 Bronchiolo-alveolar carcinoma, non-mucinous current | Confirmed; the plain term "Bronchiolo-alveolar carcinoma, NOS" is [obs] at 8250/3 |
| c1 | Every 8251/3 term is [obs] | Confirmed (two rows) |
| c1 | The term was redefined as non-invasive (adenocarcinoma in situ, minimally invasive, lepidic, invasive mucinous) | Not confirmed: Nicholson, printed p. 370, says it of the mucinous tumour only |
| c1 | Old mucinous bronchioloalveolar carcinoma went to 8253/3 | Supported by the ICD-O-3.2 [obs] synonym and the Nicholson sentence; not stated by the WHO or ICCR tables |
| c1 | Chen 2026 reports "alveolar carcinoma" in a child | Not confirmed as a case: background sentence only, absent from the 11 types of the 36-child series |
| **c1 overall** | | **PARTLY CONFIRMED** |
| c2 Skin (Q33) | WHO 5th edition downgraded cribriform carcinoma to cribriform tumour | Confirmed (Goldman-Lévy 2025, printed p. 559, PDF p. 5); source says "indolent", not "benign", and prints no code |
| c2 | ICD-O-3.2 does not name the new tumour; holds 8201/3 Cribriform carcinoma, NOS current | Confirmed |
| c2 | No ICCC-2017 range holds 8201 at skin | Confirmed (XIe range 124 lacks 8201; zero 8201 ranges cover C44) |
| **c2 overall** | | **CONFIRMED** (with the "indolent, no code" qualification) |
| c3 Eye (Q103) | WHO Eye and Orbit 5th edition removed oncocytic carcinoma as obsolete | Confirmed (Milman 2023, printed p. 85, PDF p. 15); removal only, no successor named |
| c3 | ICD-O-3.2 keeps 8290/3 Oxyphilic adenocarcinoma current, "Oncocytic carcinoma" a Synonym | Confirmed |
| **c3 overall** | | **CONFIRMED** |

Open points that my files cannot settle: Ozkan 2024 (the 211-child series that `data_gaps[6]` cites); the WHO book
text or IASLC/ATS/ERS 2011 on how the term bronchioloalveolar carcinoma was retired; the WHO's own code and behaviour
for cutaneous cribriform tumour; any WHO statement of where oncocytic carcinoma of the lacrimal gland now falls.
