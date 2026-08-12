# Display Intake Contract

Owner: the `display/` family.

The **intake** is the provenance-bound input package for one display unit.
It answers a different question from the render recipe and the final asset.

```text
task / case / narrative material
        │  canonical source of truth
        ▼
unit/intake/                 what this display was allowed to read
        │
        ├── unit/recipe/     how the renderer transforms those inputs
        └── unit/assets/     the promoted visual the paper actually shows
```

A first-class View may be the caller and place this unit at
`views/<ViewPageStem>/output/<PageID>-Display<n>-<slug>/`. That folder is the
renderer unit itself, not an adapter copy. The View owns `output.md`, the
reader job, evidence/Card bindings, and acceptance; the renderer still owns
the recipe and promoted asset.

`intake/` is not a second data store.
For a data display it holds a small, approved summary extract plus a manifest
that points back to the exact task holder and run that produced it.
The task output remains canonical.

## Unit layout for new units

```text
<unit-dir>/
├── README.md
├── intake/
│   ├── manifest.yaml        provenance, snapshots, and permitted use
│   ├── inputs/              small display-safe extracts only
│   │   └── source_data.csv
│   └── narrative-context.md optional claim, reader, or table-description context
├── recipe/                  script, FigureSpec, prompt, and renderer receipts
├── candidates/
├── assets/
├── versions/
├── float.tex
├── preview.tex
└── preview.pdf
```

`source/` is the **legacy** layout name.
Existing units may retain it unchanged.
New work uses `intake/` for values and `recipe/` for code or prompts.
Do not bulk-migrate a working paper merely to rename folders.

## The manifest

Every new unit begins with `intake/manifest.yaml`, seeded from
`intake-manifest.template.yaml` in this directory.

The path fields are project-root-relative unless `location: secure-server` says
otherwise.
The important boundary is explicit:

```text
origin.holder       the task, case, discovery, or paper holder that owns the source
origin.run           the precise run within that holder, when applicable
origin.artifact      the canonical input file that was read
origin.provenance    the producing task's evidence and selection record, when applicable
snapshot.path        the frozen small extract inside this display unit
recipe/              never a source of truth for values
```

For a numeric display, every `role: values` source MUST contain all of
`origin.holder`, `origin.artifact`, `origin.provenance`, `origin.sha256`, `snapshot.path`, and
`snapshot.sha256`.
The snapshot must be an aggregate that is safe to keep in the paper folder.

For a concept display, omit `role: values` entirely.
Record the paper-context input instead, for example the narrative beat, claim,
or human-approved table description.
A concept figure may not invent numeric facts.
If it shows real counts, percentages, or estimates, add a separate
`role: values` source for those facts.

## Materializing a task result

The normal data route is deliberately small:

```text
tasks/<holder>/results/<run>/source_data.csv
        │
        ├── task keeps the canonical aggregate and provenance.json
        ▼
displays/displayNN-<slug>/intake/
        ├── manifest.yaml records holder, run, artifact, hashes, and purpose
        └── inputs/source_data.csv is the frozen render input
```

The display stage or its adapter materializes the snapshot.
It must copy only the display-ready summary CSV, never raw data or a broad
intermediate file.
The renderer reads `intake/inputs/`; it does not search task folders, inspect
raw data, or choose a subset by itself.

If a task only has a large or ambiguous result file, the right action is a new
task deliverable: a named, display-ready aggregate.
It is not acceptable for a renderer to silently select rows from an arbitrary
upstream CSV.

The task's `provenance.json` must identify the producing holder and run, the aggregate's SHA-256,
the upstream artifacts, selection logic, and an explicit display-safety assertion.
The Intake manifest repeats the holder, run, canonical artifact, and snapshot hash rather than
assuming that a renderer will discover them from task files.

## Updating an intake

Snapshots are immutable evidence inputs.
When the producing task is rerun or the selected rows change:

1. materialize a new snapshot;
2. update `origin.run`, hashes, and the purpose in `manifest.yaml`;
3. retain the prior snapshot or record its successor in `versions/`;
4. rerun the recipe and promote a candidate through the normal review path.

Never hand-edit a snapshot to "fix" a value.
The correction belongs in the producing task or in a newly named summary
deliverable.

## Ownership and refusal rules

```text
Task / Case       produces the canonical aggregate and its run provenance.
View or consumer  decides why the reader needs the display and owns placement.
Display Intake    binds approved inputs to one unit and records their origins.
Renderer           reads the intake, writes recipe/candidate/asset files, and refuses to guess.
```

A renderer MUST refuse a numeric render when the values input lacks a task
holder, canonical artifact, or matching snapshot hash.
It MUST also refuse a snapshot containing raw or disallowed sensitive data.
Candidate rendering must not mutate `intake/`.

## Minimum verification

- `manifest.yaml` parses and names the unit's display id.
- Every snapshot path exists and its hash matches the manifest.
- Every numeric visual element traces to a `role: values` source.
- Every values source points to a task holder, run when applicable, and canonical artifact.
- `recipe/` reads only declared intake inputs for values.
- The owning View Display row or legacy Paper `S-Display-N` page points to the manifest as its provenance binding.
