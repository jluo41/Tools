# The Display Intake
state: ✅ SETTLED
owner: JL
method: bind a small approved display input to its exact upstream holder before any renderer runs

## Question
How does one display unit receive task-produced values without becoming a second data store or losing the task that produced them?

A display needs a small CSV or a table description it can render locally, while the task must remain the canonical owner of the evidence.
The Intake resolves this by freezing only the approved summary input and recording its holder, run, canonical artifact, hashes, and permitted use.

## Boundary
- ✅ Covered here
  The unit-level input package, its traceability fields, and the handoff from a task to a renderer.
- ↪ Covered elsewhere
  `QD5` decides who may commission a render, `QD6` carries the full six-link provenance chain, and `QC3` or `QC4` attaches the completed unit to a sentence.

## Diagram
```text
  TASK HOLDER                         DISPLAY UNIT
  tasks/CNN.../                       displays/displayNN-slug/
  results/<run>/                            │
  source_data.csv ────────────────► intake/manifest.yaml
  provenance.json                   │ holder · run · artifact · hashes
       ▲                             └── inputs/source_data.csv
       │                                      │
  canonical source of truth                 ▼
                                    recipe/gen_<slug>.py
                                             │
                                             ▼
                                    candidates/ → assets/figure.pdf

  VALUES ARE INPUTS.  PYTHON/PROMPTS ARE RECIPES.  ASSETS ARE OUTPUTS.
```

## Content
### The three folders have different jobs
intake/
  Holds the small approved summary CSV or narrative context that this unit may read.
  `manifest.yaml` names the upstream holder, run, canonical artifact, hashes, and use.

recipe/
  Holds Python, a FigureSpec, or a generation prompt that transforms declared intake material into a visual.
  It is never a source of truth for values.

assets/
  Holds the selected visual that `float.tex` references.
  Candidate renders stay outside it until a human-approved promotion.

### The wrapper is not renderer-owned
The Paper-owned `### Wrapper` block on the matching `S-Display-<n>` page records the approved literal caption, stable `\label`, and float placement.
A renderer can serialize those exact fields into an initial `float.tex` or preserve them while refreshing an asset.
It cannot compose or revise them.
Candidate rendering needs no wrapper; finalization does.

### A summary CSV is copied deliberately
A small display-ready `source_data.csv` may be snapshotted into `intake/inputs/`.
The original task output remains canonical.
The manifest makes the copy auditable rather than anonymous.

```yaml
origin:
  holder: tasks/CNN_display/01_summary_export
  run: results/2026-07-27-main
  artifact: tasks/CNN_display/01_summary_export/results/2026-07-27-main/source_data.csv
  provenance: tasks/CNN_display/01_summary_export/results/2026-07-27-main/provenance.json
snapshot:
  path: inputs/source_data.csv
```

If an upstream CSV is too broad, the task must emit a named display-ready aggregate.
The renderer never searches a large file or chooses rows on its own.

If that verified aggregate already exists, start at **Paper Display**, not at the task: accept a DR, allocate the unit, and materialize Intake.
`haipipe-task-for-display` is only the route for a missing or changed aggregate; it does not render the paper-facing visual.

### Numeric and concept units enter differently
A numeric display has a `role: values` source that points to a task holder and an aggregate snapshot.
A concept illustration has narrative context instead and no values source.
If it displays a real N, percentage, or estimate, that fact is a values source too.

### Target layout and legacy migration
```text
displayNN-slug/
├── README.md
├── intake/       verified values snapshot, or concept context
├── recipe/       rebuild code, FigureSpec, prompt, or editable PPTX + export receipt
├── float.tex     caller-owned caption, label, and reference to the promoted asset
├── preview.tex + preview.pdf
├── assets/       the selected manuscript-facing artifact
├── candidates/   unpromoted alternatives
└── versions/     superseded history
```

An old `source/` folder may contain scripts, prompts, and values together, but it does not become the target layout by being renamed.
Migrate only when the values can enter a truthful Intake manifest and the rebuild material can live in Recipe without changing the live asset.
For a concept figure, Intake records narrative context and may have no values CSV.
For a numeric display whose original run is unavailable, retain the legacy folder and record the reason rather than inventing a manifest.

### The task no longer owns the final paper visual
`haipipe-task-for-display` produces `source_data.csv` and `provenance.json`.
It may make diagnostic images, but they are not a canonical paper figure or table.
The Display unit owns candidate selection, recipe, final asset, caption wrapper, and placement.

## Items to Finish
- [x] 📥 Define the Intake, Recipe, and Asset boundary
      `display/ref/display-intake-contract.md` and the manifest template state the new layout.
- [x] 🔗 Require holder-level traceability
      Each numeric source records task holder, run, canonical artifact, snapshot path, and hashes.
- [x] 🧰 Reframe the display task output
      The task produces verified summary data and provenance rather than the paper-facing final asset.
- [x] 🧾 Keep paper wrapper semantics on the Paper side
      `S-Display-<n>` now records the approved caption, label, and placement; a renderer only serializes those fields.
- [x] 🧪 Validate with fresh-context agents
      Two independent agents traced an existing summary CSV through Paper Display → Intake → renderer and refused to read raw task data or invent wrapper semantics.

## Where we are
The design is implemented in the generic Display contract, the Paper Display adapter, the Display stage template, and the display-input task skill.
Existing MISQ units retain their legacy `source/` folders until deliberately migrated.
The existing MISQ display registry and DR vocabulary are likewise not rewritten by this contract; new work uses the Intake gate while an explicit migration handles old units.
The remaining `QB2b` central-Display-page migration is declared separately; meanwhile an explicit `create-page.py display ... --family Display --unit <N>` path creates one independently gated unit.

The MISQ Board now makes this state visible on every allocated Display page: Current Float → live artifact → Display Versions → current folder → display explanation.

## Files
- `display/ref/display-intake-contract.md`
  The generic intake and materialization contract.
- `display/ref/intake-manifest.template.yaml`
  The copyable provenance manifest.
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  The paper-specific task-to-intake bridge.
- `task/7_display/haipipe-task-for-display/SKILL.md`
  The task output contract for a display-ready aggregate.
- `task/7_display/haipipe-task-for-display/ref/provenance-template.json`
  The task-side record of source artifacts, selection logic, output hash, and display safety.

## Log
260727 · Board review order and the legacy-migration rule added: existing folders are shown as they are; no bulk rename, provenance fabrication, or asset promotion accompanies a page-structure change.
260727 · JL approved the small-summary-CSV intake model: the task holder remains canonical and the Display unit stores a traceable snapshot for rendering.
260727 · Wrapper ruling: Paper owns literal caption, label, and placement on `S-Display`; renderers receive those fields but cannot invent or alter them.
260727 · Fresh-context validation passed twice. Existing aggregate → Paper Display → Intake → renderer; task-for-display is only for a missing or changed aggregate.
