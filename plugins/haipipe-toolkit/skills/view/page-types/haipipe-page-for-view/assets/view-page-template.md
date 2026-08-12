# <View title>
state: 🔴 OPEN
owner: <owner>
method: organize answered QA Probes into one readable and validated View
page-type: view
view-unit: views/<ViewPageStem>

## Opening
<Write one topic-specific question paragraph: what this View lets a person understand, why these materials belong together, and who may consume it.>

**View identity**: `<ViewPageStem>.md` is the only semantic source; `views/<ViewPageStem>/` holds authored resources.

**Distribution boundary**: generated review and Paper-ready artifacts live under `_fixture/` and are never edited as source.

**Board bearing**: <name the upstream QA contract and likely downstream consumers>.

## Diagram

**View relation**: how answered QA inputs become readable content, Displays, and consumer bindings.

```text
QA-bank → answered Probes → View body + Cards → <PageID>-Display1..n → consumers
```

**Source and distribution tree**: which files are authored and which files are regenerated.

```text
<ViewPageStem>.md
├── views/<ViewPageStem>/
│   ├── manifest.json
│   ├── input/{QA-probes,sources}/
│   ├── source/
│   └── output/<PageID>-Display1-<slug>/
│       ├── output.md · README.md
│       ├── intake/ · recipe/ · candidates/ · versions/
│       └── assets/ · float.tex · preview.tex · preview.png · preview.pdf
└── _fixture/
    ├── views/<ViewPageStem>/<ViewPageStem>.tex · .pdf · .docx · manifest.json
    ├── displays/<PageID>-Display1-<slug>/manifest.json · float.tex · assets/ · preview.png · preview.pdf
    ├── references.bib
    └── .haipipe-view-build.json
```

## Content

### 1 · QA inputs
**Input bindings**: which answered Probes and QA-banks supply this View.

```text
<Probe path> → <role in this View>
```

<Summarize the input roles and add exact-span QA-input Cards bound to authored Probe files.>

### 2 · View body
**Readable body**: the topic-specific material a person should understand before opening Cards.

```text
<input material> → <organized human-readable content>
```

#### 2.1 · <topic-specific subsection>
<Write readable prose, then attach exact-span Cards to the words they support.>

### 3 · Displays
**Display outputs**: which body material each Display selects and which independent gate it keeps.

```text
<View body/Card ids> → <PageID>-Display1 → <artifact · reader job · acceptance>
```

![](views/<ViewPageStem>/output/<PageID>-Display1-<slug>/preview.png)

<Name the authored preview.png, printable preview.pdf, body bindings, artifact status, and human acceptance.>

### 4 · Consumers
**Consumer bindings**: which downstream Pages or applications use the View or selected Displays.

```text
<View or PageID-DisplayN> → <consumer> → <placement · handoff gate>
```

<Attach a Consumer Card to the exact consumer words and name its real target Page/path.>

## Aims

### A1 · QA inputs
- A1.1 · <durable input-binding target>
  **Done when:** <testable condition>.

### A2 · View body
- A2.1 · <durable body/Card target>
  **Done when:** <testable condition>.

### A3 · Displays
- A3.1 · <durable Display target>
  **Done when:** <testable artifact and acceptance condition>.

### A4 · Consumers
- A4.1 · <durable consumer target>
  **Done when:** <testable placement and handoff condition>.

### P · Source and distribution
- P1 · Keep authored resources separate from generated distribution artifacts.
  **Done when:** `_fixture` is current and no generated build or semantic adapter exists inside `views/<ViewPageStem>/`.

## States

### A1 · QA inputs
- ⬜ A1.1 · <current evidence-freshness fact>.

### A2 · View body
- ⬜ A2.1 · <current Card/body-validity fact>.

### A3 · Displays
- ⬜ A3.1 · <artifact status and separate human-acceptance fact>.

### A4 · Consumers
- ⬜ A4.1 · <placement and handoff fact>.

### P · Source and distribution
- ⬜ P1 · <fixture freshness and boundary fact>.

## Files

### 📥 Input files · what this View READS
- `<ViewPageStem>.md`
  Canonical View Page and only semantic source.
- `views/<ViewPageStem>/input/QA-probes/`
  Full answered Probe records.
- `views/<ViewPageStem>/input/sources/references.bib`
  Human-editable canonical BibTeX.

### ⚙️ Engines · what BUILDS and CHECKS this View
- `views/<ViewPageStem>/manifest.json`
  Identity, input, Display, consumer, acceptance, and fixture-build bindings.
- `views/<ViewPageStem>/source/`
  Optional source code and local checks.

### 📤 Output files · what this View AUTHORS and DISTRIBUTES
- `views/<ViewPageStem>/output/<PageID>-Display1-<slug>/`
  Native renderer unit: semantic brief, intake, recipe, candidates, winning assets, versions, float, and previews.
- `_fixture/views/<ViewPageStem>/`
  Generated TeX/PDF/Word review projection and freshness receipt.
- `_fixture/displays/<PageID>-Display1-<slug>/`
  Generated consumer manifest, Paper-ready float, assets, and previews; no semantic `output.md` or renderer internals.
- `_fixture/references.bib`
  Generated shared bibliography; edit the canonical BibTeX instead.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
<Add only required one-hop upstream or consumer Page relations; delete this group when none apply.>
