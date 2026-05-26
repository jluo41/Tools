---
name: section-intro
description: "Playbook for the Introduction section. Lists possible hooks (motivation / problem-statement / gap / story / surprising-result), how to lead with one-message pitch, common failure modes (over-claim, no clear contribution, lit-review-creep). Use when writing or revising 0-sections/01_introduction.tex or when picking an angle for a new paper's intro. Trigger: intro, introduction, hook, motivation, contribution claim, /section-intro."
allowed-tools: Read, Grep, Glob
---

section-intro — Playbook (STUB)
================================

Reference for writing/revising the **Introduction** of a paper.

Hook types
----------

```
motivation-hook    "X is critical because Y is rising."
problem-hook       "Existing methods fail when Z."
gap-hook           "No prior work addresses ABC."
story-hook         "Imagine a clinician facing patient P..."
surprising-result  "We find that A actually causes B (not assumed)."
```

Required elements (in this order, ~5 paragraphs total)
-------------------------------------------------------

1. Hook + why-it-matters (2-3 sentences)
2. State of the art + the specific gap
3. Our approach in one sentence (the pitch)
4. Headline contribution claims (bulleted or in-paragraph)
5. Paper roadmap (one sentence per section)

Common failure modes
---------------------

- Over-claim — promising results the paper doesn't deliver
- Lit-review-creep — too much background, no claim
- No pitch — reader can't say "this paper is about X" after intro
- Vague contribution — "we propose a novel method" tells nothing

TODO
----

- Add 2-3 worked examples (good intros from accepted papers in this group)
- Link to `1-narrative/narrative-report/` — the pitch in intro must
  match the narrative report's take-away message
- Add "swap-test": replace your hook with a competitor's — still defensible?
