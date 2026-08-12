# Fresh-context forward test · QV7

date: 2026-08-10
agent: Ampere · `019febdf-133d-71a0-a072-1c22061ff857`
context: fresh; no design-conversation history
result: PASS

## Assignment

Create `QV7-value-main-association` from two answered Probe files and one bibliography, write a readable body with Cards, declare one table Display and one Results consumer, validate and package the View, and stop before human acceptance.

## Produced structure

```text
QV7-value-main-association/
├── view.md
├── manifest.json
├── input/
│   ├── probes/{Q1-main-estimate.md,Q2-sample.md}
│   └── sources/references.bib
└── output/D1-main-association-table/output.md

package/QV7-value-main-association/
├── view.md
├── outputs/D1-main-association-table/output.md
└── manifest.json
```

## Parent-side verification

```text
check          valid · 2 probes · 1 display · 1 consumer · acceptance waiting
status         D1 current/waiting · C1 linked · View acceptance waiting
build --check  current · 3 files
input compare  both Probe copies byte-identical to supplied originals
privacy        package contains no input/ or source/
```

## Workflow observations

- The agent treated Cards as bindings in `view.md`, not as evidence files.
- The View body remained readable while stating the interpretation fields missing from the supplied Probes.
- D1 selected bounded facts without inventing exposure, outcome, model, or adjustment details.
- The Consumer binding named placement and remained at handoff waiting.
- The agent stopped before human acceptance, as the skill requires.

## Gate disposition

G2 passes. G3, the first real renderer adapter, remains held pending JL acceptance of the specimen and first skill contract.
