F_paper/components — Cross-cutting Skills
==========================================

Skills here are not tied to a single lifecycle stage. They are
**utilities** invoked by multiple stages (write / revise / review /
respond) and they operate on shared paper-folder assets.

Layout
------

```
components/
├── figure/          Display assets (0-display/Figure, /Table, /AppendixFigure, /AppendixTable)
│   ├── paper-figure/
│   ├── figure-spec/
│   ├── figure-planner/
│   ├── paper-illustration/
│   ├── paper-illustration-image2/
│   └── paper-structure-diagram/
│
├── citation/        Bibliography integrity (0-XXX.bib)
│   ├── citation-audit/
│   ├── citation-verifier/
│   └── reference-audit-guide/
│
├── compile/         Build pipeline (LaTeX → PDF, sync to Overleaf)
│   ├── paper-compile/
│   └── overleaf-sync/
│
└── diff/            Change-set production (vs prior submission / commit / branch)
    ├── paper-diff-pdf/      Two .tex files → colored-diff PDF
    └── paper-diff-folder/   Two paper folders → 1-diff/vs-<ref>/ writeup
```

Why these are components, not stages
-------------------------------------

- **figure**: built during plan/write, audited during review, swapped during revise — not one stage's job.
- **citation**: same — written during write, audited during review, fixed during revise.
- **compile**: every stage may need a PDF to inspect; build is not a stage in itself.
- **diff**: produced after revise, surfaced during respond — cross-stage artifact.

Lifecycle stages (1-narrative … 7-present) call these components as
needed; venue specialists in `0-workflow/` may also call them directly.
