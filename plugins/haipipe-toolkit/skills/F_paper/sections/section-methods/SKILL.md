---
name: section-methods
description: "Playbook for the Methods section. Lists possible framings (formal-math / operational-narrative / ablation-driven / reproducibility-first), what each venue expects, how to balance precision vs accessibility. Use when writing or revising 0-sections/04*.tex (Methods). Trigger: methods, method, formalism, reproducibility, /section-methods."
allowed-tools: Read, Grep, Glob
---

section-methods — Playbook (STUB)
==================================

Reference for writing/revising the **Methods** section.

Framings
--------

```
formal-math            theorems / definitions / proofs (theory papers)
operational-narrative  step-by-step procedure (empirical / clinical)
ablation-driven        method described as deltas from baseline
reproducibility-first  explicit configs, seeds, data versions, code refs
```

Most papers blend: a formal block for the contribution, an operational
block for how it was actually run.

Sub-section pattern (matches 04-XX_*.tex layout)
-------------------------------------------------

```
04-00_overview.tex            one-paragraph map of methods section
04-01_data-collection.tex     data: source, cohort, pre-filtering
04-02_<construct>.tex         the thing being measured / formalized
04-03_<algorithm>.tex         the method (model, training, inference)
04-04_<eval>.tex              how it was evaluated
04-05_<consistency>.tex       human / cross-method consistency checks
04-06_statistical-analysis.tex hypothesis tests, CI, error bars
```

Common failure modes
---------------------

- Hidden assumptions — reader can't tell what's load-bearing
- No reproducibility hooks — no config refs, no seeds, no commit SHAs
- Too much code, not enough why
- Method described in past-tense narrative when it should be a contract

TODO
----

- Cross-link to `code/` and `evaluation/scripts` in actual paper folder
- Add reproducibility checklist (NeurIPS-style)
- Add formalism vs prose tradeoff guidance per venue
