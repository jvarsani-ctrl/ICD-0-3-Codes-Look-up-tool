# WHO CNS5 Table 1 — transcription notes

Companion to `data/shared/who_cns5_table1.json`.

Source: Louis DN, et al. The 2021 WHO Classification of Tumors of the Central Nervous
System: a summary. *Neuro-Oncology* 2021;23(8):1231–1251. DOI 10.1093/neuonc/noab106.
Transcribed 2026-09-14 from
`Group 3 Papers/Exported Items/PDF/13300/Louis et al. - 2021 - ... a summary.pdf`.

## 1. Location and extraction method

Table 1 occupies **journal pages 1233–1235 = PDF pages 3–5** (0-based page indices 2–4).
It is titled "2021 WHO Classification of Tumors of the Central Nervous System. Provisional
Entities are in Italics" and continues under "Table 1  Continued" on pages 1234 and 1235.
It ends on page 1235 with the Abbreviations footnote, which is where I stopped.

The PDF is a born-digital Adobe InDesign 15.1 file with a real text layer — no OCR was
needed and no page of the table is an image.

Extraction was done twice, by two independent routes, and the results diffed:

1. **PyMuPDF `get_text("dict")`**, span level. This is the route the JSON was built from,
   because it also carries font name and flags per span, which is what identifies the
   italics (see §4), and the x-coordinate of each line, which is what identifies the
   indentation level (see §3).
2. **pdfplumber `extract_text()`**, as an independent check of the characters themselves.

The two routes produced **identical body text for all 144 rows**. The only difference in
the whole diff was that pdfplumber glued the page number `1234` onto the running head on
page 1234; that line is not part of the table.

Rows were then confirmed a third time by rendering the regions as 6× images and reading
them: the provisional-italic rows, the `Oligodendroglioma` row, the `ALK+/ALK−` row, and
the medulloblastoma block. Nothing needed repair, and nothing is recorded as unresolved
(see §8).

Indentation is carried in the PDF by leading em-spaces (U+2003) plus a real x-offset per
line. I used the x-offset, not the space count, because it is unambiguous: level-0 rows
sit at the page's table origin and each further level is +7.5 pt.

## 2. Row count and reconciliation against 144

**Table 1 prints 144 rows. My count agrees exactly: 144.**

Those 144 rows are not 144 tumour types. They break down as:

| | count |
|---|---|
| Family / subfamily / grouping heading rows | 35 |
| Tumour type rows | **109** |
| **Total printed rows** | **144** |

Per page: page 1233 = 48 rows (7 headings, 41 types); page 1234 = 49 rows (14 headings,
35 types); page 1235 = 47 rows (14 headings, 33 types).

So the prior pass's "144 rows" is the count of **printed lines in the table**, and it
reconciles with no discrepancy. `all_names` and `_source.row_count` are **109**, because
those are the tumour type names — the thing the build check greps. The 35 heading rows are
not dropped: they are preserved as the `family` / `subfamily` / `heading_path` of each
group, so every type can be traced back to its family. Nothing was padded or trimmed.

`_source` also carries `table1_printed_rows: 144` and `heading_rows: 35` so this
reconciliation is checkable from the JSON alone.

## 3. How heading rows were told apart from type rows

Table 1 nests up to four levels deep and gives no other cue, so the rule is purely
structural and taken from the table's own indentation:

> **A row is a heading if the row immediately below it is indented deeper. Otherwise it is
> a leaf, and a leaf is a tumour type.**

This is mechanical, and it reproduces the taxonomy correctly everywhere I checked it
against the body text of the paper. Two consequences are worth stating because they look
surprising in the JSON:

- **`Medulloblastomas, histologically defined` is a type, not a heading.** It sits at the
  same indent as `Medulloblastomas, molecularly defined`, but the molecularly-defined row
  has four rows indented beneath it and the histologically-defined row has none. The paper
  confirms the reading on page 1247: "an inclusive tumor type, Medulloblastoma,
  histologically defined (Table 1)". It therefore appears in the JSON as a one-type group
  under `Embryonal tumors > Medulloblastoma`, listed after the molecularly-defined group,
  matching the printed order.
- **`Meningioma` is the type; `Meningiomas` is the family.** Table 1 prints both, one row
  apart, differing only by the plural.

The JSON schema asked for `family` + `subfamily`. Where Table 1 nests deeper than two
levels, `subfamily` is the intermediate heading path joined with ` > ` (for example
`Soft tissue tumors > Uncertain differentiation`), and an extra `heading_path` array
carries the same path unjoined so nothing is lost. `subfamily` is `null` for families that
list their types directly, such as `Choroid plexus tumors`.

## 4. Provisional entities

The table title says provisional entities are in italics, but gene symbols are italic too,
so "this row contains italics" is the wrong test. I classified by the proportion of
non-space characters set in an oblique face (`UniversLTStd-Obl`), and treated a row as
provisional only when **every** character is oblique. Each of the three was then confirmed
by eye from a 6× render.

**Exactly three types are provisional:**

1. `Diffuse glioneuronal tumor with oligodendroglioma-like features and nuclear clusters`
2. `Cribriform neuroepithelial tumor`
3. `Intracranial mesenchymal tumor, FET-CREB fusion-positive`

Rows that are partly italic are gene italics and are **not** provisional. The two that
most look like false negatives, and are not:

- `CIC-rearranged sarcoma` — only `CIC` (3 of 21 characters) is oblique. It reads as
  italic at a glance purely because the row begins with the gene symbol. Confirmed by
  render: "CIC" italic, "-rearranged sarcoma" roman.
- `Desmoplastic myxoid tumor of the pineal region, SMARCB1-mutant` — only `SMARCB1`
  (7 of 55 characters) is oblique. Confirmed by render.

Note that the provisional row `Intracranial mesenchymal tumor, FET-CREB fusion-positive`
is oblique through 52 of 52 characters, including the gene symbols — CNS5 does **not** use
reverse-italics for genes inside provisional names, so a fully-oblique row is a reliable
signal.

The string `(provisional type)` does not appear in Table 1 at all; it is Table 7 that
appends it (see §5). No `name` in the JSON contains it, or the word "provisional".

## 5. Divergences between Table 1 and the rest of the paper

Table 1 is authoritative for this file. Every divergence below was left standing, not
reconciled.

**5.1 `Oligodendroglioma, IDH-mutant, and 1p/19q-codeleted` — extra comma. This one will
bite the build check.**

Table 1 (p. 1233) prints a comma after `IDH-mutant`. Verified by render, not just by text
extraction. Table 2 (p. 1236) and Table 3 (p. 1238) print the same comma.

The paper's own prose on p. 1244 prints it **without** the comma:
"Astrocytoma, IDH-mutant; Oligodendroglioma, IDH-mutant and 1p/19q-codeleted; and
Glioblastoma, IDH-wildtype."

The uncommaed form is also the one used in the WHO blue book itself, and is the form given
in the worked example in this task's own brief. The commaed Table 1 form is what is in the
JSON. **Anything emitting the uncommaed form will fail an exact-match check against this
list.** Flagging, not fixing — but this is the one to look at first if the build check
starts failing.

**5.2 `Diffuse pediatric-type high-grade glioma, H3-wildtype and IDH-wildtype` — Table 2
adds a comma.**

- Table 1 (p. 1233): `H3-wildtype and IDH-wildtype`
- Table 2 (p. 1236): `H3-wildtype, and IDH-wildtype` (the row wraps mid-name; the comma is
  at the end of the first line)
- Table 7 (p. 1241): agrees with Table 1, no comma
- Prose (p. 1244): agrees with Table 1, no comma

Table 2 is the odd one out. Table 1's form is in the JSON.

**5.3 `Intracranial mesenchymal tumor, FET-CREB fusion-positive` — Table 7 drops the
hyphen.**

- Table 1 (p. 1234): `FET-CREB fusion-positive`
- Table 7 (p. 1241): `Intracranial mesenchymal tumor, FET-CREB fusion positive (provisional type)` — no hyphen in "fusion positive"
- Prose (p. 1241 and p. 1248): hyphenated, agreeing with Table 1

Table 7 is the odd one out. Table 1's hyphenated form is in the JSON. Note also that
Table 7 carries `(provisional type)` as literal printed text where Table 1 carries the
same information as italics; the JSON holds it as `"provisional": true` and keeps the name
clean.

**5.4 `Medulloblastomas, histologically defined` — Table 1 plural, prose singular.**

- Table 1 (p. 1234): `Medulloblastomas, histologically defined` (and, one level up,
  `Medulloblastomas, molecularly defined`)
- Prose (p. 1247): "an inclusive tumor type, Medulloblastoma, histologically defined
  (Table 1)" — singular, while citing Table 1

The plural Table 1 form is in the JSON. The singular is the more natural name for a single
tumour type and is likely the intended one, which makes this worth watching.

**5.5 Table 2 groupings with no Table 1 counterpart.** Not name divergences, but they will
not match this list and should not be expected to:

- Table 2 prints `Medulloblastoma, SHH-activated` as one row covering both TP53 states;
  Table 1 splits it into `...and TP53-wildtype` and `...and TP53-mutant`.
- Table 2 prints `Ganglion cell tumors`, which is not a Table 1 row at all. Table 1 has
  `Ganglioglioma` and `Gangliocytoma` separately.

**5.6 Prose casing.** Page 1241 prints `glioblastoma, IDH-wildtype` lowercase inside a
sentence where Table 1 has `Glioblastoma, IDH-wildtype`. Sentence-level styling, noted for
completeness.

**5.7 Not a divergence.** Page 1250 mentions `diffuse midline glioma, H3 K27M-mutant`.
That is inside the title of reference 9 (cIMPACT-NOW update 2), quoting the superseded
2016 name. Table 1's `H3 K27-altered` is correct and the paper explains the change on
p. 1241.

## 6. Apparent typos transcribed as printed, not fixed

- **`Oligodendroglioma, IDH-mutant, and 1p/19q-codeleted`** — the comma in §5.1. This is
  the only thing inside Table 1 itself that I would call a probable typesetting error.
  Transcribed as printed.
- **`Medulloblastomas, histologically defined` / `Medulloblastomas, molecularly defined`**
  — plural where the paper's prose and the entity's own sense are singular (§5.4).
  Transcribed as printed.
- **`Mesenchymal, non-meningothelial tumors`** — Table 1's family heading. The
  corresponding WHO blue book family is "Mesenchymal, non-meningothelial tumours involving
  the CNS". Table 1's shorter label is what is in the JSON. This is a heading, so it is not
  in `all_names`.

The two typos the prior pass flagged are **both in Table 2, not in Table 1**, and I
confirmed both while cross-checking:

- Table 2 (p. 1236) prints **`PDFGRA`** (P-D-F-G-R-A) against `Myxoid glioneuronal tumor`.
  The Figure 3 caption on p. 1244 spells the same gene correctly as `PDGFRA`.
- Table 2 (p. 1236) prints **`ROS`** against `Infant-type hemispheric glioma`, where the
  prose on p. 1245 has `ALK, ROS1, NTRK1/2/3, or MET`.

Neither reaches this file: Table 1 has no gene-list column. I checked every gene symbol
that does appear in Table 1 — MYB, MYBL1, MN1, ZFTA, YAP1, MYCN, FOXR2, BCOR, SMARCB1,
FET, CREB, CIC, DICER1, TP53, IDH, ALK — and found no misspelling.

## 7. Character-level handling

Names are reproduced character-for-character with one deliberate, mechanical exception,
recorded here in full.

**The exception — U+00A0 NO-BREAK SPACE normalised to U+0020.** One type name is
typeset with no-break spaces around its slash:

- `Desmoplastic infantile ganglioglioma / desmoplastic infantile astrocytoma`

These are InDesign line-breaking controls, not orthography, and leaving them in would
make the row fail a plain-text grep for reasons that have nothing to do with the name.
They are stored as ordinary spaces: `Desmoplastic infantile ganglioglioma / desmoplastic
infantile astrocytoma`. This is the **only** character substitution made anywhere in the
file.

**Preserved as printed:**

- **U+2212 MINUS SIGN** in `Anaplastic large cell lymphoma (ALK+/ALK−)`. The character
  after the second `ALK` is a true minus sign, not a hyphen-minus and not an en dash.
  Confirmed by codepoint inventory and by render. Kept verbatim — a grep using an ASCII
  hyphen will not match this row.
- **All hyphens elsewhere are ASCII U+002D**, including `Erdheim-Chester`,
  `Rosai-Dorfman`, `Lhermitte-Duclos`, `FET-CREB`, `non-WNT/non-SHH`.
- Leading em-spaces (U+2003) and en-spaces (U+2002) are indentation only and are stripped;
  they carry no orthographic content.

The full non-ASCII inventory across the three table pages is exactly four codepoints:
U+00A0, U+2002, U+2003, U+2212. There are no ligature artefacts and no footnote markers
glued to any name.

## 8. Unresolved

**Nothing.** All 144 rows resolved cleanly on the first route, were confirmed identical by
the second route, and the rows most at risk were confirmed a third time by image. No row
is recorded as a guess.

## 9. One caution for whoever wires up the build check

Five rows are single printed rows that name more than one entity. They are transcribed as
printed, as single names, because that is what Table 1 prints — but a pathologist's
diagnosis will name only one of the parts, so exact matching against these will not behave
the way it does for the other 104:

- `Desmoplastic infantile ganglioglioma / desmoplastic infantile astrocytoma`
- `Pituicytoma, granular cell tumor of the sellar region, and spindle cell oncocytoma`
- `Meningeal melanocytosis and meningeal melanomatosis`
- `Meningeal melanocytoma and meningeal melanoma`
- `Hemangiomas and vascular malformations`
- `T-cell and NK/T-cell lymphomas`

Also `Chordoma (including poorly differentiated chordoma)` carries a parenthetical that
names a subtype rather than qualifying the type.

## 10. Verification

Assertions run against the delivered JSON: valid JSON; no duplicates in `all_names`;
`len(all_names)` equals the summed `types` across all families and equals
`_source.row_count`; no `name` contains "provisional"; no `name` has leading or trailing
whitespace or a doubled internal space. The checker was first proved against deliberately
broken copies of the file — see the session report for both outputs.
