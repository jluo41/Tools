# The first unified View specimen: QA inputs, readable body, Displays, and consumers
state: 🟡 PARTIAL · unified structure implemented; human acceptance remains open
owner: JL
method: instantiate and validate one unified View end to end
session: cc37b031-4dff-46bc-860a-1ef28b8c5ac7

## Opening
What should every View Page contain so that many kinds of subject matter can use one stable structure?
A View connects answered QA Probes on the left to downstream consumers on the right through a human-readable body in the middle.
The body holds topic-specific material rather than a fixed claim taxonomy.
This specimen includes definitions, values, citations, interpretation, and limits.
This specimen tests the unified structure itself: QA inputs, View body, Displays, consumers, validation state, and files.

**Application identity**: `QBt1-for-view.md` is the only authored semantic source. The same-named resource folder holds inputs, Displays, and code; generated review and Paper-ready files live under `_fixture/`, with no duplicate `view.md`.
Agreeableness is only the specimen subject; it does not define what every View must contain.

**Where this page sits**: QA1 defines the View boundary, QA2 defines Card storage and binding, and this Page proves both in a complete rendered specimen before the View skill ships.

## Diagram

**The relation model**: multiple QA inputs enter one readable View, which may produce several Displays and serve several consumers.

```text
LEFT · QA INPUTS                    MIDDLE · VIEW                       RIGHT · CONSUMERS

Task / QA-bank ─▶ Probe 1 ─┐        QBt1-for-view.md                   ┌─▶ Paper Section
Task / QA-bank ─▶ Probe 2 ─┼──────▶ ├─ View body                      ├─▶ Appendix
Task / QA-bank ─▶ Probe 3 ─┘        ├─ Citation · Value · other Cards └─▶ Application
                                    ├─ QBt1-Display1 · QBt1-Display2 · ...
                                    └─ validation
```

**Reader-facing orientation aid**: the same relation rendered as a visual explainer. It helps a new reader distinguish the human-readable View from its inputs, inspectable outputs, and independently gated consumers.

![View hub overview](assets/view-hub-overview.png)

**Unified tree**: the Page carries meaning once; its resource folder carries authored inputs and outputs, while `_fixture` carries only regenerated distribution artifacts.

```text
QBt-page-types/
├── QBt1-for-view.md
├── views/QBt1-for-view/                  AUTHORED RESOURCES
│   ├── manifest.json                     Page/resource/build contract
│   ├── input/
│   │   ├── QA-probes/
│   │   │   ├── 1-canonical-definition.md
│   │   │   ├── 2-observable-signal.md
│   │   │   └── 3-measurement-boundary.md
│   │   └── sources/
│   │       ├── references.bib             human-editable source
│   │       └── source-manifest.md
│   ├── source/
│   │   ├── build.py
│   │   └── check_cards.py
│   └── output/
│       ├── QBt1-Display1-trait-description-table/
│       │   ├── output.md · README.md
│       │   ├── intake/{manifest.yaml,inputs/source_data.csv,narrative-context.md}
│       │   ├── recipe/ · candidates/ · versions/
│       │   └── assets/ · float.tex · preview.tex · preview.png · preview.pdf
│       └── QBt1-Display2-trait-illustration/
│           ├── output.md · README.md
│           ├── intake/{manifest.yaml,narrative-context.md}
│           ├── recipe/ · candidates/ · versions/
│           └── assets/ · float.tex · preview.tex · preview.png · preview.pdf
└── _fixture/                              GENERATED DISTRIBUTION
    ├── views/QBt1-for-view/
    │   ├── QBt1-for-view.tex
    │   ├── QBt1-for-view.pdf
    │   ├── QBt1-for-view.docx
    │   ├── assets/
    │   ├── manifest.json                safe consumer contract
    │   └── build-manifest.json
    ├── displays/
    │   ├── QBt1-Display1-trait-description-table/
    │   │   └── manifest.json · float.tex · assets/ · preview.png · preview.pdf
    │   └── QBt1-Display2-trait-illustration/
    │       └── manifest.json · float.tex · assets/ · preview.png · preview.pdf
    ├── references.bib                     generated shared bibliography
    └── .haipipe-view-build.json           ownership + freshness registry

tasks/QV1-agreeableness/QA/
└── 1-bound-source-count.md

QBt-page-types/consumer/
└── S-Main-4-results.md
```

**Generated distribution**: review formats and Paper-ready floats are projections of the canonical View, not another authored package.

```text
QBt1-for-view.md ── build ──▶ _fixture/views/QBt1-for-view/{.tex,.pdf,.docx,manifest.json}
       │
       ├── selects Displays ─▶ _fixture/displays/<DisplayFolder>/
       │                        manifest.json · float.tex · assets/ · preview.{png,pdf}
       │
       └── reads BibTeX ─────▶ _fixture/references.bib
            input/sources/      generated shared citation surface

_runs/browser/QBt1/
├── report.json
├── QBt1-input-card-open.png
├── QBt1-citation-card-open.png
├── QBt1-value-card-open.png
├── QBt1-Display1-card-open.png
├── QBt1-Display2-card-open.png
└── QBt1-consumer-card-open.png
```

## Content

### 1 · QA inputs
**The incoming side**: one View may bind one or several answered Probes, and those Probes may come from one or several Task QA-banks.

```text
QA-bank ─▶ answered Probe ─┐
QA-bank ─▶ answered Probe ─┼─▶ View input collection
QA-bank ─▶ answered Probe ─┘
```

This specimen imports three answered QA Probes: a literature definition, a project-observable signal, and a construct boundary.
> Card three answered QA Probes: QI1 · QA input · Bindings: `QBt-page-types/views/QBt1-for-view/input/QA-probes/1-canonical-definition.md`, `QBt-page-types/views/QBt1-for-view/input/QA-probes/2-observable-signal.md`, `QBt-page-types/views/QBt1-for-view/input/QA-probes/3-measurement-boundary.md`. Status: answered. Role: supply the material organized by this View.

The value Probe resolves the checked count through its task QA-bank answer rather than ending at a copied number.
> Card task QA-bank answer: QI2 · QA bank · Binding: `tasks/QV1-agreeableness/QA/1-bound-source-count.md`. Consumer question: Q-View-1. Status: answered.

The current View binds 3 source Probe records [Q-View-1].
The Probe records remain the full answers; the View body selects and organizes what a person needs to read.

### 2 · View body
**The readable middle**: topic-specific subsections hold the actual substance, while Cards attach provenance and relationships to exact words.

```text
readable sentence + exact-span Card ─▶ inspect evidence without leaving the body
```

#### 2.1 · Trait meaning

Agreeableness is an interpersonal trait expressed through warmth and cooperation.
> Card interpersonal trait: EC1 · Literature · Finding: agreeableness is treated as an interpersonal construct. Bearing: supports. Boundary: trait description only. Binding: `QBt-page-types/views/QBt1-for-view/input/QA-probes/1-canonical-definition.md`. Freshness: current. Used by: QBt1-Display1 QBt1-Display2.
> Card warmth and cooperation: EC2 · Literature · Finding: warmth and cooperation are the facets selected for this specimen. Bearing: supports. Boundary: illustrative, not exhaustive. Binding: `QBt-page-types/views/QBt1-for-view/input/QA-probes/1-canonical-definition.md`. Freshness: current. Used by: QBt1-Display1 QBt1-Display2.

The literature-side construct frame resolves through the real bibliography \citep{john1999bigfive}.

#### 2.2 · Observable project signal

Review text records patient descriptions of patient-facing behavior, so this View treats review-derived scores as patient-perceived signals.
> Card patient-perceived signals: EC3 · Value · Finding: the project observes descriptions and evaluations of behavior. Bearing: qualifies. Boundary: observed signal, not direct latent trait. Binding: `QBt-page-types/views/QBt1-for-view/input/QA-probes/2-observable-signal.md`. Freshness: current. Used by: QBt1-Display1 QBt1-Display2.

#### 2.3 · Measurement boundary

The score is not treated as an error-free measure of latent personality.
> Card not treated as an error-free measure of latent personality: EC4 · Construct · Finding: the current evidence does not justify direct latent-personality measurement. Bearing: bounds this specimen. Boundary: patient-perceived manifestation only. Binding: `QBt-page-types/views/QBt1-for-view/input/QA-probes/3-measurement-boundary.md`. Freshness: current. Used by: QBt1-Display1 QBt1-Display2.

The body is not a hidden evidence ledger.
It is the human-readable synthesis produced from the inputs; Citation, Value, and other Evidence Cards let the reader inspect why each exact phrase is present.

### 3 · Displays
**The visible outputs**: a View produces one or several Displays only when a visual or tabular form helps a reader inspect or reuse part of the body.

QBt1-Display1 is the trait-description table. Its current raster is embedded below; click QBt1-Display1 and the same preview appears first, before its View-body bindings, files, and independent acceptance state.

![](QBt-page-types/views/QBt1-for-view/output/QBt1-Display1-trait-description-table/preview.png)

QBt1-Display2 is the two-panel illustration. Its current raster is embedded below; click QBt1-Display2 and the same preview appears first, before its panel bindings, files, and independent acceptance state.

![](QBt-page-types/views/QBt1-for-view/output/QBt1-Display2-trait-illustration/preview.png)

Each output also carries `preview.pdf` as the printable inspection surface. PNG is shown inline because it renders reliably in the Board browser; PDF remains linked in the Card at full fidelity.

Each authored output folder is also a complete generic renderer unit. `output.md` owns the View-level semantic judgment; `intake/` binds approved evidence or context; `recipe/` records reproducibility; `candidates/`, `assets/`, and `versions/` separate alternatives, the winner, and history. No second Display adapter folder is created.

The two Displays remain separate because a person can inspect and accept them independently.
They remain inside one View because both are outputs selected from the same named View body.
QBt1-Display1 and QBt1-Display2 are the only required outputs in this specimen; prose packs and evidence ledgers are optional outputs, not universal folders.

### 4 · Consumers
**The outgoing side**: consumers may link to the whole View or to selected Displays, and the View exposes that relationship before handoff.

```text
View ─▶ whole-View consumer
  └──▶ QBt1-Display1/2 consumer + placement + gate state
```

The Main Results section plans to consume QBt1-Display1 for its construct-interpretation passage.
> Card Main Results section: C1 · Consumer · Target Page: S-Main-4 · Binding: `QBt-page-types/consumer/S-Main-4-results.md`. Uses: QBt1-Display1. Placement: Results / construct interpretation. Status: planned, blocked on View and Display acceptance.

Other legal consumers include Appendix sections, Narrative pages, reports, and applications.
A consumer may still reach a Probe directly when its own contract allows it; the View route is the normal human-readable handoff, not a ban on every direct link.

## Aims

### A1 · QA inputs
- A1.1 · Bind several answered Probes without copying their full answers into the View.
  **Done when:** The Page names all three Probe files and the rich Q reference reaches the task QA-bank answer.
- A1.2 · Keep one or several QA-bank groups legal under the same input structure.
  **Done when:** The contract uses a plural `input/QA-probes/` collection and no field assumes one bank.

### A2 · View body
- A2.1 · Make the View body substantive rather than a manifest or evidence ledger.
  **Done when:** A reader can understand trait meaning, observable signal, and measurement boundary without opening a Card.
- A2.2 · Make Citation, Value, and other Evidence Cards inspectable on exact words.
  **Done when:** Each marker opens the correct payload and source relationship while prose styling stays intact.

### A3 · Displays
- A3.1 · Produce two independently inspectable Displays from selected View-body content.
  **Done when:** QBt1-Display1 and QBt1-Display2 each show a PNG in the Page, open the same preview first in their rich Display Card, link the printable PDF, and name their View-body bindings.
- A3.2 · Keep the output contract minimal.
  **Done when:** Only QBt1-Display1 and QBt1-Display2 are mandatory in the specimen, while optional output kinds remain absent.

### A4 · Consumers
- A4.1 · Make the downstream use relationship a clickable Consumer Card.
  **Done when:** The exact words “Main Results section” open C1 with a live S-Main-4 Page link, real target file, selected output, placement, and gate state.
- A4.2 · Keep consumer handoff gated independently from evidence validity and Display rendering.
  **Done when:** The review projection can be built and checked while C1 remains blocked on human acceptance.

### P · Unified folder and validation
- P1 · Prove one canonical Page and one resource structure.
  **Done when:** the View check, fixture-build check, Board check, and real-browser Card check all pass without `view.md`, root Display adapter Pages, or generated files inside the authored resource folder.
- P2 · Obtain human acceptance before extracting the shipping skill contract.
  **Done when:** JL accepts the View body, Card model, Display outputs, Consumer relation, and folder boundary.

## States

### Architecture decision
- ✅ JL accepted one canonical View Page plus a same-named authored resource folder and a generated `_fixture` distribution. `view.md` and root Display adapter Pages remain retired; fixture artifacts never become semantic sources.

### A1 · QA inputs
- ✅ A1.1 · The 45 of 45 browser run opens the QA-input Card, checked value, Probe Card, and task QA-bank target.
- ✅ A1.2 · The structure uses plural Probe and source collections without imposing one QA-bank.

### A2 · View body
- ✅ A2.1 · Content 2 presents three readable topic-specific subsections before any Card is opened.
- ✅ A2.2 · The 45 of 45 browser run opens all four exact-span Cards plus the real Citation and Value Cards while preserving prose styling.

### A3 · Displays
- ✅ A3.1 · QBt1-Display1 and QBt1-Display2 share the View Page index, embed both PNGs, and pass preview-first rich-Card acceptance.
- ✅ A3.2 · The former O3 prose-support output was removed; only two actual Displays remain.

### A4 · Consumers
- ✅ A4.1 · C1 points to the QBt consumer fixture, uses QBt1-Display1, and passes live click-through acceptance.
- ✅ A4.2 · S-Main-4 owns the planned landing and remains blocked on View and Display acceptance.

### P · Unified folder and validation
- ✅ P1 · Both authored Displays satisfy the native renderer-unit contract; `_fixture` contains current source-free View/Display manifests, floats, winning assets, previews, and bibliography.
- 🧠 P2 · Human acceptance waits on JL after the rendered specimen is opened.

## Files

### 📥 Input files · what this View READS
- `QBt-page-types/QBt1-for-view.md`
  The only authored semantic source for the View.
- `QBt-page-types/views/QBt1-for-view/input/QA-probes/`
  The three full Probe answers used by the View.
- `QBt-page-types/views/QBt1-for-view/input/sources/`
  The bibliography and source manifest.

### ⚙️ Engines · what BUILDS and CHECKS this View
- `QBt-page-types/views/QBt1-for-view/manifest.json`
  The identity, input, Display, consumer, acceptance, and fixture-build contract.
- `QBt-page-types/views/QBt1-for-view/source/build.py`
  The generator and freshness checker.
- `QBt-page-types/views/QBt1-for-view/source/check_cards.py`
  The real-browser self-reference check.

### 📤 Output files · what this View AUTHORS and DISTRIBUTES
- `QBt-page-types/views/QBt1-for-view/output/QBt1-Display1-trait-description-table/`
  Native table renderer unit with evidence intake, generation recipe, winning asset, float, and inspection previews.
- `QBt-page-types/views/QBt1-for-view/output/QBt1-Display2-trait-illustration/`
  Native illustration renderer unit with concept intake, final brief, review log, winning assets, float, and inspection previews.
- `QBt-page-types/_fixture/views/QBt1-for-view/`
  Generated `.tex`, `.pdf`, `.docx`, safe consumer manifest, embedded review assets, and freshness receipt.
- `QBt-page-types/_fixture/displays/`
  Generated safe Display manifests, Paper-ready floats, assets, and previews; no copied intake, recipe, `output.md`, or semantic adapters.
- `QBt-page-types/_fixture/references.bib`
  Generated shared bibliography; edits belong in the canonical `input/sources/references.bib`.
- `_runs/browser/QBt1/report.json`
  The browser validation record.
- `_runs/fresh-review/S-Main-4-consumer-link.md`
  The fresh-context read-only contract regression for C1-to-S-Main-4.

### 📋 Contracts · what RECEIVES this View
- `QBt-page-types/consumer/S-Main-4-results.md`
  The downstream Consumer Page reached directly from C1.

## Log

- 260810 2036 · [CHECK-CC] Rebuilt the Board after teaching rich Display Cards to prefer View-owned `output.md` over renderer `README.md`; the real-browser suite passes 45/45 with both native previews, EC bindings, files, and independent acceptance gates visible.
- 260810 2034 · [BUILD-CC] Upgraded D1 and D2 into native generic renderer units with intake, recipe, candidates, winning assets, versions, float wrappers, and cropped PNG/PDF inspection surfaces.
- 260810 2034 · [CHECK-CC] Added safe View/Display fixture manifests and multi-View ownership tests; both Skill validators, 3/3 script regressions, specimen check, and fixture freshness check pass while all human gates remain waiting.
- 260810 · [RULING-JL] Moved all generated review and Paper-ready Display projections into `_fixture`; the same-named `views/` unit now contains authored resources only.
- 260810 · [BUILD-CC] Added per-View fixture ownership/freshness registry, deterministic shared BibTeX generation, transformed Paper float paths, and an optional `build --target` override.
- 260810 · [CHECK-CC] The revised Board passes all 45 real-browser Card checks; isolated QY4 default and override fixtures both pass source-free build freshness checks with View/Display human gates waiting.
- 260810 · [CHECK-SONNET] Fresh QY3 regression created one canonical Page, complete Display/Consumer contracts, real review formats, and a Card containing both Binding and Files paths; all checks passed with human gates waiting.
- 260810 · [CHECK-CC] The adapter-free Board passes 8 pages with 0 error, 0 warning, and 0 gap; the Tailscale browser suite passes 45 of 45 Citation, Value, Probe, Display, and Consumer checks.
- 260810 · [BUILD-CC] Generated and validated `QBt1-for-view.tex`, `.pdf`, and `.docx`; both Display images are embedded in PDF and DOCX, while canonical `references.bib` remains untouched.
- 260810 · [RULING-JL] Accepted the single-source architecture: QBt1-for-view.md is canonical; its resource folder owns QA-probes, editable BibTeX, self-contained Displays, and generated TeX/PDF/Word review projections.
- 260810 · [CHECK-SONNET] Fresh QZ1-for-view execution created QZ1-Display1, validated and packaged it without private inputs, and stopped with View and Display acceptance waiting.
- 260810 · [CORRECTION-JL] Replaced the parallel QV1/D1/display01 naming with one owner chain: QBt1-for-view, QBt1-Display1, and QBt1-Display2; moved S-Main-4 into the separate QS consumer group.
- 260810 · [CHECK-CC] The owner-indexed specimen passes 45 of 45 real-browser checks, including both embedded previews, both Display Cards, and C1 navigation to QS/S-Main-4.
- 260810 · [CHECK-SONNET] Fresh read-only regression independently found the live C1 href, opened S-Main-4, and reported no divergence from haipipe-sentence v0.4.1 or haipipe-page-for-view.
- 260810 · [CHECK-CC] The 45 of 45 real-browser run opens C1, finds its live S-Main-4 link, follows it, and verifies the consumer Page's QV1-D1 placement and blocked gate.
- 260810 · [REVISE-CC] Promoted the Main Results consumer from a hidden fixture file to the real S-Main-4 Board Page and added live Page navigation inside C1.
- 260810 · [CHECK-CC] Expanded real-browser acceptance passes 43 of 43, including inline D1/D2 PNG dimensions, preview-first Card ordering, and direct preview.pdf exposure.
- 260810 · [REVISE-CC] Added reproducible PNG/PDF previews for D1 and D2, embedded both rasters in Content 3, and changed rich Display Cards to lead with the inspection artifact instead of burying it below status prose.
- 260810 · [CHECK-CC] Unified specimen passed 40 of 40 real-browser checks across QA input, QA bank, Citation, Value, Probe, four exact-span Evidence Cards, two Displays, and one downstream Consumer Card.
- 260810 · [CHECK-CC] Generated View package is current with view.md plus D1/D2, excludes private inputs, and the Board passes 7 pages · 0 error · 0 warn · 0 gap.
- 260810 · [RULING-JL] Unified every View around QA inputs, a human-readable View body, one or several Displays, downstream consumers, validation state, and files; topic-specific body subsections remain flexible.
- 260810 · [RULING-JL] Cards are source annotations and resolver markers on exact words, not a separate `content/` folder; Consumer is a legal Card kind alongside Probe, Citation, Value, Evidence, and Display.
- 260810 · [REVISE-CC] Renamed the authored unit to `QV1-value-agreeableness-trait-description`, added `view.md` and optional Python `source/`, renamed outputs D1/D2, removed mandatory prose support, and added the Main Results Consumer target.
- 260810 · [RETRACTED-CC] DIKW and one-claim language were examples that CC incorrectly promoted into the universal View contract; neither is part of the unified structure.
