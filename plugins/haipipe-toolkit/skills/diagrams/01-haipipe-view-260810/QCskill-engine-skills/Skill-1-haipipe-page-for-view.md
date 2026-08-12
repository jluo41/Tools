# haipipe-page-for-view · v?
state: 🟡 in flux · complete specimen works; standalone multi-View Board remains unproven
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-page-for-view` defines the readable Page contract for one View. Its four divisions cover QA inputs, a substantive body with Cards, Displays, and consumers while preserving separate gates. Load it instead of `haipipe-page-for-display` when the Page organizes evidence and may own several output expressions. The Display sibling governs one Paper float, not the evidence hub around it. QBt1 and cmsreg QV1 implement the contract; a standalone multi-View application Board remains unaccepted.

**Boundary**: the Page Type defines one View unit, not the Board that manages a collection of Views and not the renderer that produces an asset.

**Current evidence**: the complete specimen, browser Cards, and one embedded task-side View work; QA4 keeps standalone application mode open.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start f96945032ad147a8 view/page-types/haipipe-page-for-view -->

**What `haipipe-page-for-view` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-page-for-view/
  agents/
    openai.yaml               4 ln
  assets/
    view-page-template.md   151 ln  <View title>
  SKILL.md                  241 ln  Haipipe Page for View
```

<!-- haipipe:skill:tree:end -->

**How `haipipe-page-for-view` is used**: the base Page frame is specialized into four View divisions, then `haipipe-view` creates and checks the same-named resource unit.

```
haipipe-page base
      │ page-type: view
      ▼
QA inputs · View body · Displays · Consumers
      │ same Page stem
      ▼
haipipe-view resource/build workflow
```

## Content
<!-- haipipe:skill:body:start f96945032ad147a8 view/page-types/haipipe-page-for-view -->

**haipipe-page-for-view** · `?` · last shipped ?

- folder   `view/page-types/haipipe-page-for-view/`
- tools    not declared

### SKILL.md




Load `haipipe-page` first for the shared Opening, Diagram, Content, Aims, States, Files, and evaluation contract. Load `haipipe-view` when creating the same-named resource folder or running deterministic `check`, `build`, `build --check`, or `status` commands.


- 1 · Type, identity, and scope
      Declare:
      ```text
      page-type: view
      view-unit: views/<ViewPageStem>
      ```
      Use one identity chain:
      ```text
      <ViewPageStem>.md
      └── views/<ViewPageStem>/
          └── <PageID>-Display1..n-<slug>/
      ```
      The Page stem is the View identity. The resource folder must have the same stem. Every Display inherits the Page's short id, such as `QBt1-Display1`. Do not create a parallel `QV1` identity, duplicate `view.md`, or root Display adapter Pages.
      A View is a human-readable hub, not a claim type, data type, DIKW level, or Paper section. Its body may organize a sample description, value, result, literature synthesis, method basis, limitation, construct boundary, or any other matter a person needs to inspect. Do not require exactly one claim, one Probe, or one Display. A draft may have no rendered Display yet; a deliverable View has one or more promised Displays.

- 2 · Source and distribution boundary
      Keep authorship and distribution physically separate:
      ```text
      <ViewPageStem>.md                     CANONICAL SEMANTIC SOURCE

      views/<ViewPageStem>/                 AUTHORED RESOURCES
      ├── manifest.json
      ├── input/
      │   ├── QA-probes/
      │   └── sources/
      │       └── references.bib
      ├── source/                            optional code
      └── output/<PageID>-Display1..n-<slug>/
          ├── output.md · README.md
          ├── intake/ · recipe/ · candidates/ · versions/
          └── assets/ · float.tex · preview.tex · preview.png · preview.pdf

      _fixture/                              GENERATED DISTRIBUTION
      ├── views/<ViewPageStem>/
      │   └── <ViewPageStem>.tex · .pdf · .docx · assets/ · manifest.json · build-manifest.json
      ├── displays/<DisplayFolder>/
      │   └── manifest.json · float.tex · assets/ · preview.png · preview.pdf
      ├── references.bib
      └── .haipipe-view-build.json
      ```
      The View Page is the first consumer of its own evidence. Its Cards and inline previews resolve to authored resources under `views/<ViewPageStem>/`, where a person can inspect and revise them.
      Paper, Appendix, and other applications consume accepted distribution artifacts and their safe `manifest.json` files under `_fixture/`. They do not treat internal `output.md`, QA Probes, source notes, intake snapshots, recipes, candidates, or build code as Paper-ready outputs.
      Never hand-edit `_fixture`. Rebuild it from the canonical Page and authored resources. The fixture must contain no canonical Page copy, `view.md`, semantic `output.md`, QA Probe, source note, or root Display adapter Page.
      Keep `input/sources/references.bib` human-editable. A person may open it and paste or revise BibTeX. The build regenerates `_fixture/references.bib` and must not overwrite the canonical bibliography.

- 3 · Page contract
      Write the shared sections in base Page order.

- 3.1 · Opening
      Ask what this specific View lets a person understand, explain why the selected material belongs together, and name likely consumers. Keep the visible paragraph topic-specific; put identity, Board bearing, and boundary details in labelled `More details` parts after the first blank line.

- 3.2 · Diagram
      Draw two captioned figures.
      First show the relation:
      ```text
      Task / QA-bank → answered Probes → View body + Cards → Displays → consumers
      ```
      Then show the physical boundary:
      ```text
      canonical Page + authored views/ → build → generated _fixture/
      ```
      List the important files and generated artifacts rather than naming only the folders.

- 3.3 · Content
      Use exactly four direct divisions. Put topic-specific subsections only under division 2.
      ```text
      ### 1 · QA inputs
      ### 2 · View body
      ### 3 · Displays
      ### 4 · Consumers
      ```
      **1 · QA inputs**
      Name every answered Probe group and QA-bank relation used by this View. Keep complete answers in `input/QA-probes/`; summarize each answer's role in the Page.
      Attach a QA-input Card to the exact words that name the input collection. A View may bind one or several Probes from one or several QA-banks.
      **2 · View body**
      Write the substantive material a person came to read. Divide it into numbered topic-specific subsections such as sample, variable, result, literature finding, interpretation, method, or limitation.
      Keep prose understandable before any Card opens. Put a Card annotation immediately after the sentence containing its exact anchor words:
      ```markdown
      The analytic sample contains 3,842 physicians.
      > Card 3,842 physicians: V1 · Value · Finding: ... · Binding: `input/QA-probes/Q2.md`. Freshness: current.
      ```
      Cards are annotations in the canonical Page, not files in a `content/` or `cards/` folder. Use Citation, Value, Evidence, Probe, Display, and Consumer resolvers as appropriate. Bind evidence Cards to authored sources, never to generated fixture files.
      **3 · Displays**
      List each `<PageID>-Display<n>` with:
      ```text
      reader job
      View-body/Card bindings
      artifact status
      human acceptance
      preview.png
      preview.pdf
      ```
      Each listed folder must also conform directly to the generic Display-unit contract: caller-owned `intake/`, renderer-owned `recipe/`, candidate and version history, a winning `assets/` artifact, `float.tex`, and standalone previews. The View folder is the renderer unit; do not create an adapter copy elsewhere.
      Embed the current authored `preview.png` directly in the Page and make the rich Display Card open with that same preview before metadata. Link `preview.pdf` as the printable inspection surface.
      Several panels remain one Display only when they share one reader job and one acceptance decision. Otherwise split them. Do not create empty output categories such as a prose pack or evidence ledger unless this View actually produces one.
      Rendering does not imply acceptance. A Display can be `rendered/waiting`, independently of the View and every consumer.
      **4 · Consumers**
      Name each downstream Page or application, what it plans to use, placement, and handoff state. A consumer may bind the whole View or selected Displays.
      When the consumer is a Board Page, put both its Page id and source binding in the Consumer Card. The Page id supplies live navigation; the path supplies provenance. The consumer Page owns prose placement and downstream acceptance.
      A planned consumer does not gain access merely because `_fixture` is current. Handoff requires the relevant View and Display human gates.

- 3.4 · Aims and States
      Mirror Content divisions A1 through A4. Add a Page-level `P` group when the source/distribution boundary or fixture build needs an explicit target.
      Keep these states separate:
      ```text
      input/evidence freshness
      View-body/Card validity
      Display artifact status
      Display human acceptance
      fixture build freshness
      consumer placement and handoff
      View human acceptance
      ```
      Machines may establish freshness, rendering, and routing. They may not infer human acceptance from a passing build, browser check, or current fixture.

- 3.5 · Files
      Expose an action map, not a second narrative:
      ```text
      📥 Input files    canonical Page · QA Probes · source notes · canonical BibTeX
      ⚙️ Engines        manifest · optional source code · haipipe-view builder
      📤 Output files   authored Display contracts · generated fixture artifacts
      🔗 Related Pages  selected consumers or upstream Board context, when needed
      ```
      Name canonical and generated locations separately. Never describe `_fixture` as the location a person edits.

- 4 · Manifest contract
      The resource manifest binds identity, inputs, Displays, consumers, acceptance, and the fixture target. At minimum its build block is:
      ```json
      {
        "build": {
          "fixture_root": "../../_fixture",
          "formats": ["tex", "pdf", "docx"]
        }
      }
      ```
      Every Display row declares `"unit_contract": "display-unit-output-v1"`. The generated fixture manifests expose only safe consumer fields and calculate handoff eligibility without changing human acceptance.
      Keep planned and sourced Displays visible in the generated View manifest, but do not create their `_fixture/displays/` folders. Only rendered or current artifacts are distributable; acceptance independently determines whether a consumer may use them.
      Interpret `fixture_root` relative to `views/<ViewPageStem>/`. Use the `haipipe-view` builder's `--target` option only for an intentional isolated distribution or regression; it must not change canonical resources.

- 5 · Repair rules
      - If generated review files sit under `views/<ViewPageStem>/build/`, rebuild them into `_fixture/views/<ViewPageStem>/` and retire the old generated directory.
      - If `_fixture` contains a canonical Page, `view.md`, `output.md`, QA Probe, or adapter Page, remove that generated semantic copy and rebuild the distribution.
      - If a Card binds `_fixture`, point it to the authored source that supports the sentence.
      - If Paper consumes `views/<View>/output/` directly, route it to the accepted `_fixture/displays/` artifact.
      - If a distributed float still points through `output/<DisplayFolder>/`, rebuild it so its path begins `displays/<DisplayFolder>/`.
      - If only fixture freshness changes, do not alter human acceptance. If an accepted source Display changes, reopen the relevant Display and downstream handoff states.

- 6 · Close and CHECK
      Mechanical completion requires:
      ```text
      canonical Page/resource identity valid
      all declared authored inputs resolve
      Cards bind authored evidence
      all declared Displays are inspectable
      consumers resolve with explicit handoff states
      _fixture review, Displays, bibliography, and ownership receipt are current
      consumer-safe View and Display manifests are current
      no semantic adapters or generated build remain in authored resources
      ```
      Page closure additionally requires a person to accept the current View. Each Display keeps its own acceptance decision. A current fixture and a passing Board do not close either gate.
      Evaluate the four Content divisions, the source/distribution Diagram, Files boundary, fixture freshness, and human gates as separate units under the base Page evaluation contract.

- 7 · Template
      Copy `assets/view-page-template.md`, replace every angle-bracket slot, and delete instructions that do not apply. Do not add or reorder base Page sections.
### The other files

2 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
agents/openai.yaml                 4 ln
assets/view-page-template.md     151 ln  <View title>
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🔧 Keep one flexible Page structure across data, method, result, literature, and limitation subjects.
  QBt1 and cmsreg QV1 use the same four divisions without a claim or topic taxonomy.
- [x] 🔧 Make Display cardinality explicit.
  A draft may have no rendered Display yet; a deliverable View promises one or more independently accepted Displays.
- [ ] 🔎 Prove the Page contract on a standalone application Board with several Views.
  Current application evidence is an embedded QV group inside cmsreg.

## States
The Page Type is implemented and used, but the portfolio-level application mode remains a named gap.
- 260811 CC · ✅ Unit contract
  One Page stem, four Content divisions, authored evidence bindings, multi-Display output, and consumer-safe fixture boundaries are implemented.
- 260811 CC · 🟡 Board-level evidence
  QA4 records embedded mode as proven and standalone multi-View mode as waiting for a specimen.

## Log
260811 1231 · authored the mirror health judgment and clarified draft versus deliverable Display cardinality
260811 1201 · page generated from `view/page-types/haipipe-page-for-view/` by `skillpage.py new`
