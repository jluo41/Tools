# Fresh-context preview-first regression · QV9

date: 2026-08-10
agent: Bernoulli · `019fed3b-21c2-7543-91f0-b8e4d5b0a520`
context: fresh; no design-conversation history and no follow-up rendering hint
result: PASS

## Assignment

Create `QV9-value-main-association` from two answered Probes and one bibliography, write a bounded readable View body, render D1 table and D2 diagram, expose PNG/PDF inspection surfaces, bind one Results consumer, package the View, and stop before human acceptance.

## Produced structure

```text
QV9-value-main-association/
├── view.md
├── manifest.json
├── input/{probes,sources}/
└── output/
    ├── D1-main-association-table/{output.md,artifact.svg,preview.png,preview.pdf}
    └── D2-evidence-boundary-diagram/{output.md,artifact.svg,preview.png,preview.pdf}

package/QV9-value-main-association/
├── view.md
├── outputs/D1-main-association-table/{output.md,artifact.svg,preview.png,preview.pdf}
├── outputs/D2-evidence-boundary-diagram/{output.md,artifact.svg,preview.png,preview.pdf}
└── manifest.json
```

## Parent-side verification

```text
check          valid · 2 probes · 2 displays · 1 consumer · acceptance waiting
status         D1 rendered/waiting · D2 rendered/waiting · C1 linked
build --check  current · 10 files
input compare  both Probe snapshots byte-identical to supplied originals
privacy        package contains no input/ or source/
visual read    D1 table and D2 boundary diagram both render and preserve stated limits
```

## Contract behavior observed

- The agent used the skill's local SVG-to-PNG/PDF fallback without a follow-up hint.
- Both PNG paths and both PDF paths are present in `view.md`; the checker enforces this.
- D1 and D2 report only supplied values and explicitly preserve missing analytic and sampling context.
- C1 uses D1 and remains linked pending acceptance.
- View, D1, and D2 all stop at `acceptance=waiting`.

## Gate disposition

The revised View skill passes the required fresh-context regression. Human acceptance of QBt1 remains the gate before the first real renderer/consumer migration.
