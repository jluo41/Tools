# QY4 · Source/fixture functional regression

date: 260810
context: isolated QY4 filesystem scope; executed in the implementation thread after the external fresh-agent runner was rejected by repository privacy policy

## Task

Create one complete `QY4-for-view` with two answered QA Probes, one canonical BibTeX source, one rendered table Display, one real local consumer, waiting human gates, a default fixture build, and an explicit `--target` fixture build.

## Commands and results

```text
view.py check QY4-for-view.md
  valid · 2 QA probes · 1 display · 1 consumer · acceptance waiting

view.py status QY4-for-view.md
  QY4-Display1 rendered/waiting · C1 planned · View waiting

view.py build QY4-for-view.md
  built _fixture · review + 1 paper-ready Display + references

view.py build QY4-for-view.md --check
  current · review + Displays + references

view.py build QY4-for-view.md --target override-fixture
  built override-fixture · review + 1 paper-ready Display + references

view.py build QY4-for-view.md --target override-fixture --check
  current · review + Displays + references
```

Every command exited 0.

## Authored tree

```text
QY4-for-view.md
consumers/S-Results.md
views/QY4-for-view/
├── manifest.json
├── input/
│   ├── QA-probes/{Q1-observable-signal.md,Q2-measurement-boundary.md}
│   └── sources/references.bib
└── output/QY4-Display1-measurement-boundary-table/
    ├── output.md
    ├── float.tex
    ├── assets/table.tex
    ├── preview.png
    └── preview.pdf
```

There is no authored `build/`, `view.md`, or root Display adapter Markdown Page.

## Generated tree

```text
_fixture/
├── .haipipe-view-build.json
├── references.bib
├── views/QY4-for-view/
│   ├── QY4-for-view.tex
│   ├── QY4-for-view.pdf
│   ├── QY4-for-view.docx
│   ├── assets/display-1.png
│   └── build-manifest.json
└── displays/QY4-Display1-measurement-boundary-table/
    ├── float.tex
    ├── assets/table.tex
    ├── preview.png
    └── preview.pdf
```

`override-fixture/` has the same shape. Neither generated Display contains `output.md`.

## Boundary assertions

- The distributed float uses `displays/QY4-Display1-measurement-boundary-table/assets/table.tex`; the source float retains `output/...`.
- Canonical and generated `references.bib` are byte-identical in this one-View fixture.
- Both fixture roots contain ownership/freshness registries.
- Default and overridden builds leave the canonical Page and resource folder unchanged.
- View acceptance is `waiting`; Display acceptance is `waiting`; Consumer status is `planned`.

## Divergence

No functional divergence was found in create/check/status/build/build-check or `--target` behavior. A separate fresh-agent interpretation run remains unavailable in this environment: the external Claude runner was rejected for private-repository transmission risk, and the internal thread backend returned no registered handler. This report therefore validates mechanics in an isolated fixture, not fresh-context skill discovery.
