---
name: section-abstract
description: "Playbook for the Abstract. Condensation strategies (which 3 sentences to keep), venue-specific length limits, structured-vs-prose abstract formats. Use when writing or revising 0-sections/00_abstract.tex. Trigger: abstract, /section-abstract."
allowed-tools: Read, Grep, Glob
---

section-abstract — Playbook (STUB)
===================================

Reference for writing/revising the **Abstract**.

Templates
---------

```
4-sentence (ML conference)
  S1: problem / motivation
  S2: what we do (the pitch)
  S3: how we evaluate / setting
  S4: headline number + what it implies

5-sentence (clinical / biomedical)
  S1: background
  S2: methods
  S3: results (specific number)
  S4: limitations / scope
  S5: implication

Structured (Nature Methods / clinical journals)
  Background: ...
  Methods: ...
  Results: ...
  Conclusions: ...
```

Length limits (rough)
----------------------

- ICML / NeurIPS / ICLR: ~250 words, single paragraph
- Nature Methods: 250 words, single paragraph
- Nature Biotech: 150 words for "editorial summary" + 250 abstract
- PNAS: 250 words + "significance statement" (~120 words)
- MISQ: 250 words
- npj journals: 150-200 words

Rule: every claim in abstract must appear (with same magnitude) in
results.

Common failure modes
---------------------

- Two pitches — abstract carries two ideas. Pick one (one paper, one message).
- Numbers without anchor (e.g. "improved by 5%") — say baseline
- Buried headline — main number is in S5 instead of S2/S3
- Jargon in S1 — should be venue-readable, not subfield-readable

TODO
----

- Cross-check with `1-narrative/narrative-report` — abstract pitch
  must equal narrative pitch
- Per-venue word counts auto-checked
