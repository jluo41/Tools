---
name: haipipe-view
description: Create, inspect, validate, build, or report a first-class View whose canonical Board Page organizes answered QA Probes into a human-readable body, inline evidence Cards, one or more renderer-complete Display units, downstream consumer bindings, and safe TeX/PDF/Word/manifest fixture projections. Use for View Pages, View resource folders, Citation/Value/Display/Consumer Cards, View-owned Display intake and output folders, or View readiness for Paper and applications.
---

# Haipipe View

Load `haipipe-page-for-view` for the Page contract. Use this skill for the same-named resource folder and deterministic checks/builds.

## Model

One View has one semantic source: its Board Page.

```text
QA inputs → canonical View Page + Cards → <PageID>-Display1..n → consumers
                                      └→ generated `_fixture` distribution
```

Do not create `view.md`, a generated semantic package, root Display adapter Pages, or separate public “for-value / for-literature / for-display” View types. Values, citations, prose evidence, literature syntheses, tables, figures, and illustrations all live in the one View body and its Displays.

```text
QBt1-for-view.md                         canonical semantic source
views/QBt1-for-view/                     same stem; resources only
├── manifest.json
├── input/
│   ├── QA-probes/
│   └── sources/
│       └── references.bib               human-editable canonical BibTeX
├── source/                              optional code
├── output/
│   ├── QBt1-Display1-<slug>/          native generic Display unit
│   └── QBt1-Display2-<slug>/
└── (no generated build here)

_fixture/                                generated distribution, never authored
├── views/QBt1-for-view/
│   ├── QBt1-for-view.{tex,pdf,docx}
│   ├── manifest.json                  safe consumer contract
│   └── build-manifest.json
├── displays/QBt1-Display1-<slug>/
│   └── manifest.json · float.tex · assets/ · preview.{png,pdf}
├── displays/QBt1-Display2-<slug>/
├── references.bib
└── .haipipe-view-build.json             ownership + freshness registry
```

Cards remain annotations immediately under exact words in the canonical Page. They are not separate content files.

## Commands

Resolve the directory containing this SKILL.md as `$HAIPIPE_VIEW_SKILL`.

```bash
python3 "$HAIPIPE_VIEW_SKILL/scripts/view.py" create <page-dir> <ViewPageStem> --title "<title>"
python3 "$HAIPIPE_VIEW_SKILL/scripts/view.py" add-display <ViewPage.md> <kind> <slug> --reader-job "<job>" --body-binding <CardID>
python3 "$HAIPIPE_VIEW_SKILL/scripts/view.py" check <ViewPage.md>
python3 "$HAIPIPE_VIEW_SKILL/scripts/view.py" build <ViewPage.md>
python3 "$HAIPIPE_VIEW_SKILL/scripts/view.py" build <ViewPage.md> --check
python3 "$HAIPIPE_VIEW_SKILL/scripts/view.py" build <ViewPage.md> --target <fixture-root>
python3 "$HAIPIPE_VIEW_SKILL/scripts/view.py" status <ViewPage.md>
```

All non-create verbs take the canonical Page path, not the resource folder.

## Workflow

### 1. Create or inspect the canonical pair

`create` writes `<ViewPageStem>.md` and `views/<ViewPageStem>/`. It refuses either existing path and creates no fake Display.

For an existing View, read the Page, manifest, declared inputs, and declared outputs. Treat every `_fixture` file as a generated projection only.

### 2. Bind QA inputs and sources

Put full answered Probe records in `input/QA-probes/`. Put bibliography and source notes in `input/sources/`. A View may bind several Probes from several QA-banks.

```json
"inputs": {
  "qa_probes": ["input/QA-probes/Q1.md"],
  "sources": ["input/sources/references.bib"]
}
```

`references.bib` is human-owned. Open it whenever needed and paste or revise valid BibTeX, including Google Scholar exports. The build reads it and regenerates the shared `_fixture/references.bib`; it must never rewrite the canonical file.

### 3. Write the Page body and Cards

The Page `## Content` has four direct divisions:

```text
1 · QA inputs
2 · View body
3 · Displays
4 · Consumers
```

Write topic-specific `2.n` subsections that a person can understand before opening Cards. Attach provenance to exact words:

```markdown
The analytic sample contains 3,842 physicians.
> Card 3,842 physicians: V1 · Value · Binding: `views/Q1-for-view/input/QA-probes/Q2.md`. State: current.
```

Reuse `\citep{key}`, checked number/Q-reference syntax, Display markers, and Consumer Cards where the Board has richer resolvers.

### 4. Build renderer-complete Displays

Each real output gets one folder and one acceptance decision:

```text
output/QBt1-Display1-main-result-table/
├── README.md       renderer state and fragility
├── output.md       View-owned reader job, bindings, state, acceptance
├── intake/         caller-owned provenance and approved snapshots/context
├── recipe/         renderer-owned reproducibility material
├── candidates/     alternatives before promotion
├── assets/         winning rendered asset only
├── versions/       superseded artifacts
├── float.tex       caller-owned caption, label, placement, asset reference
├── preview.tex     standalone inspection wrapper
├── preview.png     inline/browser inspection
└── preview.pdf     printable inspection
```

This folder directly conforms to `../../display/ref/display-unit-output-contract.md`; never create a second renderer adapter folder. Keep `output.md` because the View owns semantic judgment, while the generic renderer owns `recipe/` and the promoted asset. Start a unit with `add-display`, bind its approved intake, then dispatch its `kind` to the matching renderer.

Manifest ids are `<PageID>-Display<n>` and folder names are `<DisplayID>-<slug>`. Several panels remain one Display only when they share one reader job and one acceptance decision. One View may own many Displays.

Declare every Display with the complete contract:

```json
{
  "id": "QBt1-Display1",
  "folder": "QBt1-Display1-main-result-table",
  "unit_contract": "display-unit-output-v1",
  "kind": "table",
  "reader_job": "Compare the main estimate with its uncertainty.",
  "body_bindings": ["EC1", "V2"],
  "status": "rendered",
  "acceptance": "waiting",
  "preview_image": "preview.png",
  "preview_pdf": "preview.pdf"
}
```

Dispatch craft by kind to the existing table, figure, diagram, or illustration renderer. Never invent values and never infer human acceptance from successful rendering.

### 5. Declare consumers

Each consumer names a real target, what it uses, placement, and handoff state. `target` is resolved relative to `views/<ViewPageStem>/`; write enough `../` segments to reach the actual file directly. Put the Consumer Card on the exact consumer words in the Page. Consumers may use the whole View or selected Displays.

```json
{
  "id": "C1",
  "target": "../../../QS-consumers/S-Main-4-results.md",
  "uses": ["QBt1-Display1"],
  "placement": "Results / construct interpretation",
  "status": "planned"
}
```

### 6. Validate and build the fixture distribution

Run `check` before `build`. It validates owner-indexed identity, QA/source bindings, citations, Display folders/previews/states, Consumer targets, and exact-span Card paths.

`build` extracts only the canonical Page's `## Content`, embeds current Display previews, resolves local citation labels, and generates two projections:

```text
.tex   editable typesetting projection
.pdf   fixed review surface
.docx  editable Word review with embedded Displays

displays/<DisplayFolder>/
  float.tex + assets/ + preview.png + preview.pdf
```

The manifest field `build.fixture_root` defaults to `../../_fixture` from the resource folder. `--target` may override it for an isolated build or test.

The fixture publishes consumer-safe metadata at `views/<View>/manifest.json` and `displays/<Display>/manifest.json`. It includes identity, kind, reader job, body bindings, artifact paths, acceptance, source digests, and handoff eligibility. It excludes QA Probes, source notes, canonical paths, renderer recipes, candidates, and semantic `output.md`. Consumers must read these generated manifests instead of reaching into authored resources.

The View manifest may list planned or sourced Displays, but only `rendered` or `current` Displays receive `_fixture/displays/` folders. Their human acceptance remains visible and can still block handoff. Removing one View's Display cleans only that View's owned distribution folder.

The review `build-manifest.json` hashes the canonical Page and declared resources. The root `.haipipe-view-build.json` records which exact View and Display directories this builder owns and combines registered BibTeX entries into one deterministic `references.bib`. `build --check` fails on stale review files, transformed floats, Display assets, bibliography, or registry state.

The fixture contains no `view.md`, canonical Page copy, `output.md`, or root Display adapter Page. It is safe for Paper to consume and safe to regenerate. Never hand-edit it.

### 7. Stop at the human gate

Report independently:

```text
input/evidence freshness
Display artifact + acceptance
consumer placement + handoff
fixture review/distribution freshness
```

A current review build is not human acceptance. Never write `accepted` on a person's behalf.

## Resources

- `scripts/view.py`: canonical create/check/build/status implementation.
- `assets/view-template/manifest.json`: resource manifest template.
- `../../display/ref/display-intake-contract.md`: caller-owned provenance and snapshot rules.
- `../../display/ref/display-unit-output-contract.md`: native View Display unit layout.
- `../page-types/haipipe-page-for-view/SKILL.md`: canonical Board Page contract.
