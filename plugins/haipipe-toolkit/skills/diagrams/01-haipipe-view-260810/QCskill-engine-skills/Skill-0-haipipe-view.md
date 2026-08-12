# haipipe-view · v?
state: 🟡 in flux · deterministic and fresh-agent runs pass; automatic renderer dispatch remains open
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-view` manages one canonical View resource unit and its consumer-safe fixture. Its commands create, validate, build, and report that unit. Use it after `haipipe-page-for-view` has defined what the Page must say. That sibling owns the Page contract; this door owns folders, manifests, Displays, and deterministic commands. Local regressions and a mounted fresh-context run pass; automatic renderer dispatch remains unproven.

**Boundary**: it does not decide View subject matter, write Paper prose, recompute Task answers, or accept a human gate.

**Current evidence**: three script regressions, the complete QBt1 specimen, and a mounted fresh-agent construction all pass. The fresh agent independently produced two QA bindings, exact-span value/evidence/citation Cards, one rendered table Display, one consumer, and current TeX/PDF/DOCX fixture projections while leaving human acceptance waiting.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start 09d971aecb52acfd view/haipipe-view -->

**What `haipipe-view` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-view/
  agents/
    openai.yaml          4 ln
  assets/
    view-template/
      manifest.json     18 ln
  scripts/
    test_view.py       149 ln  Regression tests for View scaffolding and shared fixture ownership.
    view.py           1308 ln  Create, validate, build, and summarize a canonical Haipipe View Page.
  SKILL.md             206 ln  Haipipe View
```

<!-- haipipe:skill:tree:end -->

**How `haipipe-view` is used**: the Page contract supplies meaning, this skill manages authored resources and Displays, and build publishes a narrow fixture for consumers.

```
View Page + answered Probes + sources
        │ create / add-display / check / build
        ▼
views/<stem>/ authored unit
        │
        └──▶ _fixture/{views,displays,references.bib} ──▶ consumers
```

## Content
<!-- haipipe:skill:body:start 09d971aecb52acfd view/haipipe-view -->

**haipipe-view** · `?` · last shipped ?

- folder   `view/haipipe-view/`
- tools    not declared

### SKILL.md




Load `haipipe-page-for-view` for the Page contract. Use this skill for the same-named resource folder and deterministic checks/builds.


- 1 · Model
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

- 2 · Commands
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

- 3 · Workflow

- 3.1 · 1. Create or inspect the canonical pair
      `create` writes `<ViewPageStem>.md` and `views/<ViewPageStem>/`. It refuses either existing path and creates no fake Display.
      For an existing View, read the Page, manifest, declared inputs, and declared outputs. Treat every `_fixture` file as a generated projection only.

- 3.2 · 2. Bind QA inputs and sources
      Put full answered Probe records in `input/QA-probes/`. Put bibliography and source notes in `input/sources/`. A View may bind several Probes from several QA-banks.
      ```json
      "inputs": {
        "qa_probes": ["input/QA-probes/Q1.md"],
        "sources": ["input/sources/references.bib"]
      }
      ```
      `references.bib` is human-owned. Open it whenever needed and paste or revise valid BibTeX, including Google Scholar exports. The build reads it and regenerates the shared `_fixture/references.bib`; it must never rewrite the canonical file.

- 3.3 · 3. Write the Page body and Cards
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

- 3.4 · 4. Build renderer-complete Displays
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

- 3.5 · 5. Declare consumers
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

- 3.6 · 6. Validate and build the fixture distribution
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

- 3.7 · 7. Stop at the human gate
      Report independently:
      ```text
      input/evidence freshness
      Display artifact + acceptance
      consumer placement + handoff
      fixture review/distribution freshness
      ```
      A current review build is not human acceptance. Never write `accepted` on a person's behalf.

- 4 · Resources
      - `scripts/view.py`: canonical create/check/build/status implementation.
      - `assets/view-template/manifest.json`: resource manifest template.
      - `../../display/ref/display-intake-contract.md`: caller-owned provenance and snapshot rules.
      - `../../display/ref/display-unit-output-contract.md`: native View Display unit layout.
      - `../page-types/haipipe-page-for-view/SKILL.md`: canonical Board Page contract.
### The other files

4 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
agents/openai.yaml                   4 ln
assets/view-template/manifest.json    18 ln
scripts/test_view.py               149 ln  Regression tests for View scaffolding and shared fixture ownership.
scripts/view.py                   1308 ln  Create, validate, build, and summarize a canonical Haipipe View Page.
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🔧 Keep one canonical Page/resource identity and a source-free generated fixture.
  Local unit tests and isolated create/check/build runs cover the current deterministic core.
- [ ] 🔧 Dispatch a View Display to one real table, figure, diagram, or illustration renderer without an adapter copy.
  The contract names this handoff, but `view.py` does not yet perform it.
- [x] 🔎 Complete one fresh-context run in an environment that mounts the relocated View skill.
  A new agent used only the two View skills and a bounded teaching input to create, render, validate, build, and freshness-check QF1 without changing the repository.

## States
The unit ships, its deterministic core works, and the fresh-context discovery/execution gate passes. Automatic renderer dispatch remains open.
- 260811 CC · ✅ Relocation and core regressions
  The top-level `skills/view/` paths, quick validation, unit tests, and isolated fixture build all pass.
- 260811 CC · ✅ Fresh-context execution
  A clean agent discovered both View skills, recovered from a validator-caught consumer-path mistake, rendered one table, and passed check/build/freshness checks with human gates still waiting.
- 260811 CC · 🟡 Renderer dispatch
  Renderer selection remains an agent workflow described by contract; `view.py` does not yet invoke the renderer automatically.

## Log
260811 1935 · recorded the successful mounted fresh-agent construction and narrowed the remaining gap to automatic renderer dispatch
260811 1230 · authored the mirror health judgment and corrected relocated Display-contract links
260811 1200 · page generated from `view/haipipe-view/` by `skillpage.py new`
