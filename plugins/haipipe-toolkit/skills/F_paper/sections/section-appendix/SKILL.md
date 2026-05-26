---
name: section-appendix
description: "Playbook for Appendix / Supplementary Information. Decides what lives in appendix vs main paper (page-limit overflow / proofs / extra ablations / prompts / negative results), how to letter and reference. Use when writing or revising 0-sections/A_*.tex … E_*.tex. Trigger: appendix, supplementary, SI, /section-appendix."
allowed-tools: Read, Grep, Glob
---

section-appendix — Playbook (STUB)
===================================

Reference for writing/revising the **Appendix** / **Supplementary Information**.

What belongs here
------------------

```
proofs                  formal derivations too long for main text
extra ablations         beyond the main "ours vs baseline" sweep
prompts / configs       LLM prompts, hyperparameter sweeps verbatim
extended dataset stats  per-group, per-version, per-split breakdowns
case studies            illustrative examples, qualitative analysis
negative results        what didn't work and why (only if instructive)
implementation details  code snippets, library versions, environment
```

What does NOT belong (move to main paper)
------------------------------------------

- Anything cited from Methods that the reader needs to understand the headline
- Validation that establishes the result is real (sensitivity, robustness)
- Comparison to a baseline you claim to beat

Naming convention (this group)
-------------------------------

Lettered prefix, sibling to numbered main-paper sections inside `0-sections/`:

```
A_<topic>.tex    Appendix A
B_<topic>.tex    Appendix B
C_<topic>.tex    Appendix C
...
E_supplementary-revision.tex   (added during revision rounds)
```

In master `.tex`, included with `\section*{SI-N: <Title>}` + `\input{0-sections/A_...}`.

Common failure modes
---------------------

- Appendix-as-graveyard — dumping cuts without curation
- Missing reference — main text says "see SI" without pinning which appendix
- Inconsistent depth — A is 1 page, B is 12 pages, no rationale
- Re-deriving — repeating proofs already in main text

TODO
----

- Per-venue: which journals allow unlimited SI vs strict page limits
- Cross-link to `components/figure/`: appendix figures go in
  `0-display/AppendixFigure/`, not `0-display/Figure/`
