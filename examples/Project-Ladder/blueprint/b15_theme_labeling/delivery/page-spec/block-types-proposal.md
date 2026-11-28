# Three Labeling Block types

Design proposal, corrected 2026-11-27. The three-type split is the user's decision; the detailed folder names, Job units and UI below are proposed. Three independent synthetic example Blocks now own their entry pages. Existing production contracts have not been migrated.

The Block is the only independently addressable UI level. Job and Task are embedded records and controls, never independent page links or titles. Studio topics do not stand in for these Blocks. This follows `PRINCIPLE.md` and UI constitution A10.

| Block type | Owns | One Job | Main output |
| --- | --- | --- | --- |
| Itemization | Source-to-item conversion | Source snapshot × accepted item recipe | Immutable Items package |
| Guideline Generation | Human meaning and its executable expression | One candidate expression method under a fixed construct and human authority | Signed Guideline package |
| Labeling at Scale | Execution and audit under a frozen guideline | Items snapshot × Guideline release × executor configuration | Audited label release |

These are three types, not three permanent instances. One Items package may feed several Guideline Blocks. A Guideline release may be used by several Scale Blocks. The same type can be instantiated for another corpus, construct or application scope.

## Work Folder first

All three keep the common Block → Job → Task → Run → Result ladder. Each Block has its own `board.md`, `jNN_` Jobs, `sNN-` human Studio topics, `trace/` and `delivery/`. References connect Blocks; a downstream owner does not copy upstream mutable working directories.

```text
<Project>/labeling/
├── bNN_itemization/
│   ├── board.md
│   ├── sNN-item-boundaries/       human choice of unit and context
│   ├── jNN_<source>_<recipe>/
│   │   ├── tNN_describe/
│   │   ├── tNN_build/
│   │   └── tNN_check/
│   ├── delivery/jNN_<job>/items-vNN/
│   └── trace/
├── bNN_guideline_generation/
│   ├── board.md
│   ├── sNN-label-meaning/         scope, judgments, acceptance and signature
│   ├── jNN_<expression_method>/
│   │   ├── tNN_prepare_cases/
│   │   ├── tNN_draft_rules/
│   │   └── tNN_evaluate/
│   ├── delivery/jNN_<job>/guideline-vNN/
│   └── trace/
└── bNN_labeling_at_scale/
    ├── board.md
    ├── sNN-audit-review/          acceptance and semantic escalation
    ├── jNN_<items>_<release>_<executor>/
    │   ├── tNN_qualify/
    │   ├── tNN_batches/
    │   ├── tNN_audit/
    │   └── tNN_package/
    ├── delivery/jNN_<job>/labels-vNN/
    └── trace/
```

A Task's operations live in `runs/rNN_<operation>/` with their `result/`. Rounds and batch retries are Runs within the same scoped Job. Job closure is a check of output completeness and validity. Human acceptance belongs to Studio; a candidate being generated successfully does not imply it was accepted or released.

The first implementation must decide and register explicit Block-kind values before any new Work Blocks are written. The names above are a proposal, not newly recognized `board-kind` values. Legacy combined Jobs remain readable until an explicit migration maps each artifact to its new owner.

## Handoffs

| Package | Required identity and content | Downstream rule |
| --- | --- | --- |
| Items | Source snapshot, recipe version, stable item IDs, text/context, source references, exclusions and coverage | Guideline and Scale name the exact package. Context never exposes protected reference labels. |
| Guideline | Construct and scope, human authority, meaning and expression versions, calibration examples, validation evidence and signature | Scale reads the exact signed release. A new draft never changes an existing binding. |
| Labels | Items, Guideline and executor versions, batch identities, per-item labels, uncertainty, exclusions, coverage and audit evidence | A partial execution is inspectable as a Run result but cannot claim final delivery. |

Itemization may calculate reusable features such as embeddings, but this is optional and does not decide a target label. Partition membership and protected-gold custody remain an explicit governed manifest; shared Items do not grant access to sealed-test labels. External ground truth is optional reference material available only to an authorized scoring Task. No public-gold majority becomes human semantic authority.

Guideline Generation alternates human decisions with automatic candidate preparation and checks. Human preferences are collected in Studio; Jobs consume their recorded versions. Expression problems can trigger a new Run under the same meaning. Semantic problems require a new human-confirmed meaning version. Held-out test labels are never input to rewriting; a diagnostic that causes redesign requires fresh evaluation under the existing custody rules.

Scale's **Run all** binds Items + signed Guideline + qualified executor. It schedules only missing batches, preserves completed matching work and exposes failures for targeted retry. Any change to those three identity fields creates a new Job. Issues about meaning are sent back to Guideline Generation; Scale cannot silently edit the guideline. Auditing preserves uncertainty and unresolved cases instead of inventing a negative label.

## Work UI

Every type uses the Work sequence: Job topic → Job → Main / Task topic → Task. Each row is horizontal and scrollable. Main hides the Task row. The selected Task is remembered within its topic. Labels name things; counts are only findings or the waiting-items tray.

| Type | Job topics | Task topics | Main | Selected Task |
| --- | --- | --- | --- | --- |
| Itemization | Source collection | Source · Build · Check | Source/recipe binding, item-producing Tasks, boundary decisions, released package | Source rows, item/context preview, provenance checks and Runs |
| Guideline Generation | Target construct | Cases · Rules · Validation | Candidate methods, versioned evidence, decisions waiting in Studio, signed release | Case selection, rule differences, predictions, errors, evidence and Runs |
| Labeling at Scale | Guideline release | Qualification · Execution · Quality | Immutable input binding, Run all gate, batches, audit, final release | Qualification evidence, batch results/retries, audit cases, coverage and package records |

Main has Plan + Results; Findings appears only for a meaningful issue; Delivery appears when a release exists. Folds start closed. A Task's results and its Runs stay together. Human decisions are opened at the relevant item and also reachable from the title's waiting tray. A preview opens from its top-right dot. All three use the same palette, typography, folds and horizontal navigation as Work.

## Three independent example Blocks

| Block | Owner | Embedded content |
| --- | --- | --- |
| Itemization | `examples/Project-Ladder/labeling/b03_itemization` | Source/recipe Jobs, source/build/check Tasks, recipe review, Items delivery |
| Guideline Generation | `examples/Project-Ladder/labeling/b04_guideline_generation` | Expression-method Jobs, cases/rules/validation Tasks, human review, Guideline release |
| Labeling at Scale | `examples/Project-Ladder/labeling/b05_labeling_at_scale` | Version-bound Jobs, qualification/batch/audit Tasks, review, label delivery |

Each owner has its own `board.md`, `delivery/ui/model.json` and `delivery/ui/block.html`. The Workbench reads the explicit `preview-only: true` declaration and renders this Block's page at its Block route. These are synthetic design examples; no production worker or signature is implied. Jobs, Tasks and review selections are local controls. They do not create links, change browser history, or replace the Block title.

The same fragment is used for the Block route and the inline conversation preview. `build_blocks.py` regenerates both from the Block-owned model and shared template, styles and behavior. `check_blocks.py` rejects standalone child links and stale copies. The old s11/s12/s14 prototypes and their builders are archived under `history/261127-studio-prototypes/`; their old Task URLs are historical, not current navigation.

Guideline confirmation follows human judgments, generation and candidate-bound validation. Changing a judgment invalidates the draft evidence. Recipe acceptance enables building without falsely completing it. Scale retains its exact Items, Guideline and executor binding, including after another Block confirms a new Guideline.

## Acceptance and next implementation

This correction closes when the three independent Block routes render, Job/Task selections remain inside their Block, human and execution gates work, the three interaction surfaces render inline, and the Trace records the files and checks.

The overall topic remains open until the user accepts the details and implementation ships together: production folder writers and contracts, non-preview workflow readers, shared-frame adapters, release readers, guarded actions, migration and regression tests. No example or signature is fabricated to call that future work complete.
