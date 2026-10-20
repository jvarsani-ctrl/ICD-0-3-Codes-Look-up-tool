# PedsCode

**Childhood Cancer Coding Guide**

PedsCode is a browser-based tool that helps a cancer registry abstractor find the ICD-O-3.2 morphology code for a childhood tumour. The abstractor answers questions about what the patient's file contains, and the tool ends on a code with its behaviour, topography and International Classification of Childhood Cancer, third edition (ICCC-3) group. The Uganda Child Cancer Foundation built it for the Uganda Cancer Institute paediatric cancer registry, and any registry can use it.

Live version: <https://jvarsani-ctrl.github.io/ICD-0-3-Codes-Look-up-tool/>

## How it works

A case starts in one of two ways.

- **Guided entry** starts from how the child presented. The tool asks for the body system, organ and region of the tumour, then which reports are in the file.
- **Confirm existing diagnosis** starts from a diagnosis already written in the file. The abstractor types the term and picks a match, and the tool asks for the site and the evidence behind it.

The site places the case in one of the twelve ICCC-3 groups. From there the tool follows that group's decision tree one question at a time. Marker panels are asked one marker at a time, and the tool stops asking once no further answer could change the result. If the file lacks a test, the abstractor says so and the tool codes from what is there.

The result shows the name, morphology code, behaviour code, topography code, the evidence the code rests on, the ICCC-3 subgroup, other names for the code, and the tests that would give a more specific code.

PedsCode is advisory. It does not connect to REDCap or any other system, and it does not store or send anything. A case exists only in the page and is cleared when the next one starts. The abstractor enters the code in the registry system and confirms it.

Groups I to XI are built. Group XII, other and unspecified malignant neoplasms, shows as not yet available. Five made-up walk-through cases below the tool on the landing page play a case through step by step.

### Structure

PedsCode is static files with no framework and no build step. `app.js` is a single engine with no clinical content. Every code, question and rule is read from JSON.

| Path | Contents |
|---|---|
| `index.html`, `app.js`, `demo.js`, `uccf-tool.css` | the page, the engine, the walk-through player and the stylesheet |
| `data/database/` | one decision-tree file per group, `group_NN_dt.json` |
| `data/aliases/` | alternative names for each code, and the search index built from them |
| `data/shared/` | the presentation router, the topography lookup and the walk-through cases |
| `assets/` | the two UCCF logos the page shows |

## Requirements

To use PedsCode:

- A current version of Chrome, Edge, Firefox or Safari, with JavaScript on.
- A web server. The page loads its data over HTTP, so it cannot run from a file opened off the disk. Any static server works.

To run it on your own computer, Python 3 provides a server. Any other static server does the same job.

## Installation

### Run it on your computer

```bash
git clone https://github.com/jvarsani-ctrl/ICD-0-3-Codes-Look-up-tool.git
cd ICD-0-3-Codes-Look-up-tool
python3 -m http.server 8811
```

Open <http://localhost:8811>. There is nothing to install and no build step.

### Host it

Copy the files to any static host. On GitHub Pages, open Settings, then Pages, and set the source to the `main` branch and the root folder. The repository already contains the `.nojekyll` file that Pages needs.

### Embed it in REDCap

In a Descriptive Text field, use the field's embed link option and enter:

```
https://jvarsani-ctrl.github.io/ICD-0-3-Codes-Look-up-tool/?host=redcap&mode=transcript
```

`host=redcap` labels the answer as the option to select in REDCap. `mode=transcript` gives a single-column layout that suits a wide form, and `mode=rail` forces the side column instead. The walk-through cases are hidden in the embedded view. PedsCode shows the answer and the abstractor selects the option in REDCap.

## Licence

Apache License 2.0. See [`LICENSE`](LICENSE). [`NOTICE`](NOTICE) lists the material the licence does not cover, including the UCCF name and logo.
