---
name: section-related-work
description: "Playbook for the Related Work section. Positioning angles (axis-of-comparison / chronological / closest-prior), how to avoid lit-review-creep, when to use a comparison table. Use when writing or revising 0-sections/02_related_work.tex (or equivalent). Trigger: related work, lit review, positioning, /section-related-work."
allowed-tools: Read, Grep, Glob
---

section-related-work — Playbook (STUB)
=======================================

Reference for writing/revising **Related Work** / **Background**.

Positioning angles
-------------------

```
axis-of-comparison  organize by 2-3 dimensions, place self on each axis
chronological       trace the field's development, your work is the next step
closest-prior       focus on the 3-5 papers most similar, sharp deltas
problem-shape       group by problem-framing similarity, not method
```

Where it goes
--------------

```
Conference papers     short, often merged into intro (no separate section)
Journal papers        full section, may be 1-2 pages
Survey / benchmark    multi-page, with taxonomy table
```

Required behavior
------------------

1. Identify 3-5 anchor papers — the ones reviewer #2 will expect
2. State sharp deltas to each — what does YOUR paper do that they don't
3. Avoid listing without comparing ("Smith et al. did X. Jones did Y.")
4. If using a comparison table: each row = a paper, columns = features.
   Self goes in last row, must have a column where it's the only ✓.

Common failure modes
---------------------

- Citation dump — list of papers without claims
- Missing anchor — reviewer's favorite paper isn't cited
- Self over-positioning — claim novelty on a dimension nobody cares about
- Wrong section — half of this section belongs in Introduction

TODO
----

- Auto-suggest anchor papers from `components/citation/citation-audit`
- Add per-venue expectation: how long, separate section or merged
