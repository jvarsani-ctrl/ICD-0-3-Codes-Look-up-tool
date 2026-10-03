# Group VIII — for the registrar

**Written 2 October 2026, overnight, while the Group VIII build ran without you.** Every item
here was built on a stated default so the work could continue. None is hidden in the JSON:
each default is one branch or one alias, and the file named in each item says where. Argument
for each code decision: `docs/superpowers/specs/2026-10-02-group-08-bone-code-decisions-design.md`.
Layer 1 (REDCap) repairs: `docs/group_08_layer1_repair.md`.

Items are ordered by how much a wrong answer costs the registry.

---

## A. Decisions that change which code a case gets

### A1. Chondrosarcoma grade 1 — `9222/1` or `9222/3`? (D3)

WHO 2020 codes axial *chondrosarcoma, grade 1* as `9222/3`, approved by the IARC/WHO ICD-O
committee in January 2020. ICD-O-3.2 (final, 9 October 2020) lists *Chondrosarcoma, grade 1
(C40._, C41._)* under **`9222/1`**, beside *Atypical cartilaginous tumor*, and carries no
`9222/3`.

**Built:** grade 1 at any site → behaviour exclusion `9222/1`, "registrar decision required".
The case leaves the malignant registry.

**If you rule otherwise:** `9220/3` Chondrosarcoma, NOS keeps it registered, with grade lost.
Emitting `9222/3` needs the number added to Layer 1 first. Either is a one-branch change in
`bn_cartilage`.

### A2. CIC-rearranged sarcoma, sarcoma with BCOR alteration, round cell sarcoma with EWSR1–non-ETS fusion → `8803/3`? (D6)

WHO 2020 gives them `9367/3`, `9368/3` and `9366/3`, all asterisked. ICD-O-3.2 has none of the
three. **Built:** `8803/3` *Small cell sarcoma*, through its ICD-O-3.2 synonym *Round cell
sarcoma, NOS*. The Group IX session does the same for soft tissue. The alternative of coding
them as Ewing sarcoma contradicts WHO 2020, which classifies them separately.

### A3. Undifferentiated pleomorphic sarcoma of bone → `8830/3`? (D5)

WHO 2020 prints `8802/3`. ICD-O-3.2 prints *Undifferentiated high grade pleomorphic sarcoma
of bone (C40._, C41._)* on `8830/3`, and ICCC-2017 has no bone range for `8802`. **Built:**
`8830/3`, VIIId1.

### A4. Subtypes WHO 2020 folds into the parent code (D8, D9)

WHO 2020 Table 1 lists telangiectatic and small cell osteosarcoma under `9180/3`, and chondroid
chordoma under `9370/3`. ICD-O-3.2 still codes them `9183`, `9185` and `9371`, with chondroblastic
and fibroblastic osteosarcoma at `9181` and `9182`. **Built:** the term as written gets
ICD-O-3.2's specific code. "Conventional osteosarcoma" → `9180/3`. "Central" or "medullary"
osteosarcoma, as written, → `9186/3`.

### A5. "Askin tumour" in a report → `9365/3`? (D2)

WHO 2020 has no Askin entity; it is chest-wall Ewing sarcoma. ICD-O-3.2 keeps `9365/3`.
**Built:** coded as written, `9365/3`. Same in Group IX.

### A6. Metastasizing ameloblastoma → `9310/3`? (D13)

WHO 2022 places it among the benign odontogenic tumours. ICD-O-3.2's preferred term for
`9310/3` is *Ameloblastoma, metastasizing*. **Built:** `9310/3`.

### A7. Sclerosing odontogenic carcinoma → `9270/3`? (D13)

ICD-O-3.2 has no term for it. **Built:** `9270/3`, through the synonym *Odontogenic
carcinoma*.

---

## B. Decisions that change whether a case is registered

### B1. Intermediate bone tumours — register them anywhere? (D11)

Giant cell tumour of bone `9250/1` is the commonest of them in adolescents. Also: atypical
cartilaginous tumour `9222/1`, aggressive osteoblastoma `9200/1`, chondroblastoma `9230/1`,
desmoplastic fibroma `8823/1`, osteochondromatosis `9210/1`, chondromatosis `9220/1`.
ICCC-3 Group VIII admits behaviour 3 only. **Built:** each is a behaviour exclusion naming its
code and "registrar decision required". This is the same open question as Group VI item 6:
if the registry wants benign and intermediate tumours, they need a home outside ICCC-3.

### B2. Osteofibrous dysplasia-like adamantinoma (D12)

Anderson & Doyle 2021 (p. 654) says WHO 2020 made it intermediate. ICD-O-3.2 has only `9261/3`.
**Built:** not reportable, with the reason stated. If WHO 2020 prints a `/1` code for it
(the bound volume would say; the ICCR table lists intermediate rows only for cartilage and
giant cell tumours), it becomes a behaviour exclusion instead.

### B3. Chondrosarcoma on imaging alone (D10)

Visser Table 3 allows `9220/3` at C40/C41 on imaging (basis 2). Sharif 2021 (p. 4), citing
Ardakani et al. 2020, reports a 47% grade mismatch between MRI and surgery in paediatric central chondrosarcoma, and
paediatric enchondromas often look aggressive. **Built:** no imaging route for
chondrosarcoma. With malignancy called likely, the case is `8000/3` at basis 2; with a benign
cartilage tumour in the differential, it is not registered (Visser rule 4).

### B4. A referral letter naming a bone cancer, with nothing else in the file

**Built:** `8000/3` at basis 1, which Visser rule 5 permits. No other basis-1 code is
emitted. Group VI chose to emit nothing at basis 1 for renal tumours. If you want the bone
group to match, the option becomes "obtain the imaging report".

---

## C. Layer 1 — REDCap `viii_morph` (full detail in the repair package)

1. **★ Pick 33 "9260 - Ewing sarcoma" is a retired number.** `9260` now means *Aneurysmal bone
   cyst* (/0). Any record on pick 33 stores a benign code for a malignant tumour. Ewing sarcoma
   is `9364`, already offered at pick 35 under the synonym "Peripheral neuroectodermal tumor".
2. **★ No option names `9220/3` Chondrosarcoma, NOS.** Both `9220` options are the benign and
   borderline terms.
3. **No option names `9302/3` Ghost cell odontogenic carcinoma**, new in ICD-O-3.2.
4. **Picks 18–19 carry `9211`**, which is now *Osteochondromyxoma*; their two terms belong to
   `9221` and duplicate picks 22 and 24.
5. **49 options are below behaviour 3** and cannot be Group VIII cancers.
6. **Subgroup labelling.** Under ICD-O-3.2, Ewing sarcoma of bone falls in **VIIIc2**
   ("pPNET of bone"), not VIIIc1. VIIIc1 keeps only Askin tumour. Any report built on the
   ICCC-3 subgroups needs to know.

7. **I edited one Layer 1 file, for formatting only.** In `ICD coding/RedCap Options/Group 8-
   Malignant Bone Tumors.md` the VIIIc2 line (`9364, 9364 - Peripheral neuroectodermal tumor`)
   sat outside a code fence, so the build could not see the option and failed on correct data.
   I added the fence; no text changed, and the file still matches the 1 October dictionary
   snapshot. Revert it if you would rather Layer 1 files change only by your hand.
8. **`ICCC-2017.sqlite` range 60 ends in a trailing comma** (`9210,9220,9240,`). Not fixed
   (TODO §24).

---

## D. Found during the build, and what was done about it

1. **Group IV and Group VIII disagree on CD99.** Group IV refers a CD99-positive,
   PHOX2B-negative, synaptophysin-negative bone tumour here and tells the clerk it is `9364/3`.
   Group VIII codes `9364/3` only with NKX2-2, a fusion, or the report's own diagnosis; CD99
   alone gives `8002/3`. Which threshold do you want? (TODO §22, which extends §14.)
2. **The tool called every excluded tumour benign. Fixed.** The behaviour-exclusion banner
   read "Benign" whatever the behaviour, so giant cell tumour of bone (`9250/1`) and
   chondrosarcoma grade 1 (`9222/1`) were announced as benign. It now follows the ICD-O
   behaviour digit. This also corrects Group V's `9514/1` and Group VI's `8960/1` screens,
   which are on `main`.
3. **The alias index is over its size guideline** (33 KB against ~30 KB), and Groups VII and
   IX will add more (TODO §23).
4. **Coordination with the Group VII and IX sessions.** Agreed on 2 October 2026: Group VIII
   owns the Ewing and extraskeletal-bone router rules; Group IX codes soft-tissue Ewing
   `9364/3`, round cell sarcomas `8803/3` and soft-tissue undifferentiated pleomorphic sarcoma
   `8802/3`. Group VII adds a disjoint C22 branch to the `8000-8005` rule. The three branches
   will text-conflict on `build_database.py`'s group guard lines, on the router file, on
   `docs/clinical-warnings.md` and on `docs/TODO.md` (Group IX closed §12 and removed the `9473`
   router rule; this branch deleted §8 and edited §12's pointer to it). Regenerate
   `alias_index.json` after merging rather than resolving it by hand. Keep every side.

## E. Sources

1. **No baseline WHO summary paper covers the bone chapter.** The build used WHO 2020's own
   Table 1, reproduced in the ICCR bone dataset, plus Anderson & Doyle 2021. The natural paper,
   **Choi JH, Ro JY. Adv Anat Pathol 2021;28(3):119–138** (PMID 33480599), is paywalled. If
   you can obtain it, drop it in `Group 8 Papers/`.
2. **Vered M, Wright JM. Head Neck Pathol 2022;16(1):63–75** (PMC9019005) could not be read.
   The publisher withholds the XML and the PMC page served a CAPTCHA. The build used
   Soluk-Tekkesin & Wright 2022 instead. The PubMed connector, which came online later the same night, also
   returns the abstract only. The abstract adds one fact: WHO 2022 brought rhabdomyosarcoma with
   TFCP2 rearrangement into the malignant jawbone tumours. It is a Group IX tumour, and the
   round cell node already refers rhabdomyosarcoma there.
3. The Diagnostic Pathway (13 June 2026) is wrong in ten places listed in the build contract §5.
   Should it be revised, or is the contract's correction list enough?
