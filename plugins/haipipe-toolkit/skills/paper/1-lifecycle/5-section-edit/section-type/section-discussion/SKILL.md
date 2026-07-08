---
name: section-discussion
description: "Playbook for the Discussion section. Lists framings (limitation-first / implication-first / future-first / counter-claim), the 'don't overclaim' rule, how to acknowledge limits without weakening contribution. Use when writing or revising 0-sections/03*.tex (Discussion). Trigger: discussion, limitations, implications, future work, /section-discussion."
allowed-tools: Read, Grep, Glob
---

section-discussion — Playbook (STUB)
=====================================

Reference for writing/revising the **Discussion** section.

Framings (pick one as lead)
----------------------------

```
limitation-first  open with constraints, then show what's defensible
implication-first lead with what this changes downstream
future-first      this is a step in a larger program — here's the next step
counter-claim     acknowledge a strong reading against your result, refute
```

Subsection pattern (matches 03-XX_*.tex)
-----------------------------------------

```
03-00_overview.tex             summary of headline + scope
03-01_limitations.tex          honest constraints (this is where reviewers look)
03-02_ethics-implications.tex  bias / fairness / deployment risk (most venues require)
03-03_future-work.tex          (optional) what's the next claim
```

Required elements
------------------

1. Restate the headline claim ONCE — short, no fanfare
2. Position it: what changes because of this result
3. Limitations — be specific, not generic
4. (For biomedical / ML-applied) Ethics / implications
5. Future work — only if it sets up a clear next paper

Common failure modes
---------------------

- Restating Results
- Vague limitations ("more data needed") — useless, reviewers see through this
- Overclaim — "our method solves X" when it solves a restricted form of X
- Generic ethics ("models can be biased") — must be specific to YOUR result

TODO
----

- Add per-venue ethics requirements (Nature, ICML/NeurIPS, MISQ)
- Add "limitations cheatsheet" — sampling bias / scope / generalizability / temporal
