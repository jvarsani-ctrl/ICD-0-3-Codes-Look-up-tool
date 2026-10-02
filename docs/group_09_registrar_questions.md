# Group 9 — questions for the registrar

Soft tissue and other extraosseous sarcomas. Branch `claude/group-9-tumor-pathway-911c69`.
Written during the build, 2–3 October 2026.

Every item below is something the sources do not settle. Each one states **what the build does
meanwhile**, so the tool runs while you decide, and each choice can be reversed by editing one
branch. Sections refer to `docs/group_09_build_contract.md`.

Items marked ★ change what code a clerk records today.

---

## A. Codes that changed under ICD-O-3.2

### A1. ★ Ewing sarcoma is `9364/3`, and REDCap still offers the retired `9260` (contract §0.5)

IARC's *Summary of main changes* (p. 2) and *Deleted codes and their terms* (p. 6): `9260/3` Ewing
sarcoma moved to `9364/3`, which is now the preferred term for *Ewing sarcoma*. `9260` survives only
as `9260/0` *Aneurysmal bone cyst*. ICCC-2017 still files Ewing sarcoma under `9260` (IXd1), and files
`9364` at IXd2 *Peripheral neuroectodermal tumour of soft tissue*.

**The build:** every soft tissue Ewing sarcoma codes `9364/3`, which lands in IXd2. IXd1 holds only
Askin tumour. The Group 8 session codes bone Ewing sarcoma `9364/3` too.

**For you:** (a) confirm `9364/3`; (b) the REDCap option `9260 - Ewing sarcoma` should be retired in
both the Group 8 and Group 9 lists, and `9364` relabelled *Ewing sarcoma*; (c) ICCC-2017's subgroup
labels for IXd1/IXd2 now read oddly — whether to report a recode-table note upstream.

### A2. ★ Three DFSP-family labels in REDCap name the wrong behaviour (contract §0.6, §2)

`8832/3` and `8833/3` moved to behaviour 1 in ICD-O-3.2. `8832/3` now carries only
*Dermatofibrosarcoma protuberans, fibrosarcomatous*. The REDCap option `8832 - Dermatofibrosarcoma,
NOS` is today a behaviour-1 term on a number REDCap records as a Group IX sarcoma.

**The build:** fibrosarcomatous DFSP → `8832/3`. Ordinary DFSP, Bednar tumour and giant cell
fibroblastoma → behaviour exclusion, not registered in Group IX.

**For you:** relabel `8832` in REDCap to the fibrosarcomatous term, and retire `8833`.

### A3. `9150` haemangiopericytoma is a deleted number still offered in REDCap

**The build:** malignant haemangiopericytoma → `8815/3` *Solitary fibrous tumor, malignant*.
**For you:** retire `9150` from the dropdown.

### A4. Two more REDCap labels name a benign lesion on a malignant code

`8825 - Myofibroblastoma` (a /0 term) on the code whose /3 is *Myofibroblastic sarcoma*;
`9220 - Chondroma, NOS` (a /0 term) on the code whose /3 is *Chondrosarcoma, NOS*. A clerk recording a
sarcoma picks a label naming a benign tumour. Full list in `docs/group_09_layer1_repair.md`.

---

## B. WHO 2020 entities with no ICD-O-3.2 code

### B1. ★ The Ewing-like round cell sarcomas → `8803/3` (contract §3.2)

CIC-rearranged sarcoma, sarcoma with BCOR genetic alterations, round cell sarcoma with EWSR1–non-ETS
fusions. WHO 2020 gives `9367/3`, `9368/3`, `9366/3`; none is in `icdo32.sqlite` or any ICCC range.

**The build:** `8803/3` (ICD-O-3.2 synonym *Round cell sarcoma, undifferentiated*), IXe. Same as Group 8.
**For you:** confirm, or name another code.

### B2. Myxoid pleomorphic liposarcoma → `8850/3` (contract §3.3)

Characteristic of children and adolescents (Pfister 2022; Sbaraglia 2021), no ICD-O-3.2 code.
**The build:** `8850/3 Liposarcoma, NOS`. **For you:** confirm.

### B3. NTRK-rearranged spindle cell neoplasm (emerging entity)

No ICD-O-3.2 code and no settled behaviour (Sbaraglia, section *Tumours of uncertain differentiation*).
**The build:** reported as a sarcoma or high grade → `8801/3` *Spindle cell sarcoma*; reported as
lipofibromatosis-like neural tumour or low grade → not registered. A pan-TRK-positive spindle cell
tumour at age 2 or over on the IHC route also falls to `8801/3`.
**For you:** is `8801/3` acceptable, and should the low-grade form be registered at all?

### B4. Malignant melanotic nerve sheath tumour → `9540/3` (contract §3.9)

WHO 2020 calls it malignant; ICD-O-3.2 holds *Melanotic MPNST* under `9540/3` and *Melanotic
schwannoma* at `9560/1`. The WHO volume's own code is not printed in the baseline paper.
**The build:** `9540/3`. Adult entity, rare in children. **For you:** confirm.

---

## C. Legacy terms coded as written (contract §3.11)

WHO 2020 retired these names; ICD-O-3.2 still carries them without `[obs]`.

| Report says | The build codes | WHO 2020 name |
|---|---|---|
| Askin tumour | `9365/3` | Ewing sarcoma (`9364/3`) |
| Malignant fibrous histiocytoma (soft tissue) | `8830/3` | Undifferentiated pleomorphic sarcoma (`8802/3`), or myxofibrosarcoma, or a giant cell tumour |
| Mixed type rhabdomyosarcoma | `8902/3` | not in WHO 2020 Table VII |
| Lymphangiosarcoma | `9170/3` | angiosarcoma (`9120/3`) |
| Malignant haemangioendothelioma | `9130/3` | none |

**For you:** keep "code as written", or recode each to the WHO 2020 entity. Askin and Ewing are shared
with Group 8, which made the same choice.

Two codes carry only `[obs]` terms at behaviour 3 — `9560/3` *Neurilemoma, malignant* and `8853/3`
*Round cell liposarcoma*. Neither has a tree leaf. A report saying *round cell liposarcoma* is coded
`8852/3` myxoid liposarcoma, because WHO 2020 lists no round cell liposarcoma and treats it as
high-grade myxoid liposarcoma. **For you:** confirm.

---

## D. Rhabdomyosarcoma

### D1. ★ FOXO1-negative "alveolar" rhabdomyosarcoma (pathway §4D, contract §3.8)

Dehner CA, et al. (*Human Pathology* 2023) report that 10–20% of alveolar rhabdomyosarcoma show no
FOXO1 fusion and behave like embryonal rhabdomyosarcoma. Pfister 2022 defines the alveolar type as
"alveolar with FOXO1 fusions".
**The build:** codes the subtype the report states (`8920/3`) and records the negative fusion.
**For you:** keep `8920/3`, or recode to `8910/3` embryonal.

### D2. Rhabdomyosarcoma, subtype not stated, FOXO1 fusion positive → `8920/3`

**The build:** `8920/3`, on Pfister's definition. Without the fusion it stays `8900/3`. **For you:** confirm.

---

## E. Kaposi sarcoma

### E1. ★ Cutaneous Kaposi sarcoma on examination alone, basis 1 (contract §0.7, §3.5)

Visser 2023 Table 3, p. 04: *Kaposi sarcoma of the skin*, basis 1, C44, `9140/3`. This is the ENCR
rule; the pathway does not mention it.
**The build:** a clinical note describing Kaposi sarcoma of the skin registers `9140/3` at basis 1.
Nodal, mucosal or visceral Kaposi sarcoma without pathology goes to Group XII as `8000/3` (Visser
rule 5).
**For you:** confirm that the registry adopts the basis-1 route. It will be the commonest Group IX
registration in a KSHV-endemic setting.

### E2. The HHV-8 gate is not mandatory (contract §3.5; pathway §7.4)

**The build:** a histology report naming Kaposi sarcoma codes `9140/3` whether or not HHV-8 LANA-1 is
reported; an untested case shows IHC as outstanding. `9140/3` is never emitted where HHV-8 is
reported **negative**; that case goes to a node asking the final diagnosis, and if the report still
says Kaposi sarcoma it is coded as stated and listed here.
**For you:** should HHV-8 LANA-1 be required before `9140/3` when the case has histology?

### E3. Lymphadenopathy now offers Group IX

The lymphadenopathy presentation and the `C77.9` lymph node site now list Group IX, so nodal Kaposi
sarcoma reaches this group by the presentation path (pathway §4A). The clinical warning the pathway
proposes is in `docs/clinical-warnings.md`, not the tool (ruling 9).

---

## F. Basis-2 imaging codes

Visser Table 3 allows `8850/3` liposarcoma, `8890/3` leiomyosarcoma and `9120/3` angiosarcoma at basis
2 when imaging names the type. All three are rare in children; WHO 2020 says true myxoid liposarcoma
"almost never occurs in children" and that reported cases are mostly lipoblastoma.
**The build:** offers all three, each requiring the imaging report to name the type as the likely
diagnosis. **For you:** keep them, or restrict the imaging route to `8800/3` for this population.

---

## G. Scope

### G1. Benign and intermediate soft tissue tumours are not registrable in Group IX

ICCC-3 Group IX declares behaviour 3 only. Desmoid fibromatosis, inflammatory myofibroblastic
tumour, ordinary DFSP, giant cell fibroblastoma, plexiform fibrohistiocytic tumour, angiomatoid
fibrous histiocytoma, kaposiform and other intermediate haemangioendotheliomas, lipoblastoma,
plexiform neurofibroma, EBV-associated smooth muscle tumour and STUMP all reach a behaviour-exclusion
terminal. **57 REDCap options** sit below behaviour 3.
**For you:** if the registry wants any of these recorded, they need a home outside Group IX. The
EBV-associated smooth muscle tumour is the one most likely to matter in an HIV-affected cohort.

### G2. The registry's upper age bound (Programme Plan blocker 2)

Adult-type sarcomas (myxofibrosarcoma, well-differentiated and dedifferentiated liposarcoma, intimal
sarcoma, biphenotypic sinonasal sarcoma) have tree leaves because adolescents and young adults get
them. Whether they belong depends on the age bound, which is still unwritten.

### G3. Myoepithelial carcinoma and GIST of soft tissue go to Group XII

ICCC-2017 places `8982/3` at XIIa4 and `8936/3` at XIIa1. Pfister 2022 lists both in children.
**The build:** refers both to Group XII. **For you:** confirm.

---

## H. Router

### H1. The `9473` rule is removed (contract §3.12)

ICCC-2017 places `9473` in Group III at every site; ICD-O-3.2 codes peripheral PNET as `9364/3`.
The rule's Group IX default had no basis. docs/TODO.md §12 left this as a Group III/IX decision.
**For you:** confirm.

### H2. REDCap's topography list has no `C44.4` (skin of scalp and neck)

`Topography Redcap.md` offers 440–443 and 445–449. A scalp or neck skin lesion cannot be recorded at
its own site.

---

## I. Rhabdoid tumour

### I1. Rhabdoid tumour named, SMARCB1 (INI1) not tested

**The build:** `8963/3` as the report states, IHC outstanding. **For you:** require INI1 loss?

### I2. Rhabdoid morphology, SMARCB1 (INI1) retained

**The build:** `8800/3` *Sarcoma, NOS*, not `8963`. **For you:** confirm.
