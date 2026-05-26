---
name: section-results
description: "Playbook for the Results section. Lists arcs (figure-driven / claim-driven / comparison-driven / surprise-first), how to map claims to subsections, common ordering. Use when writing or revising 0-sections/02*.tex (Results). Trigger: results, results section, figure mapping, claim mapping, /section-results."
allowed-tools: Read, Grep, Glob
---

section-results — Playbook (STUB)
==================================

Reference for writing/revising the **Results** section.

Story arcs
----------

```
figure-driven      each subsection = one main figure
claim-driven       each subsection = one claim, figures support it
comparison-driven  ours vs baselines across multiple settings
surprise-first     lead with the unexpected finding, build up to it
```

Subsection pattern (matches 02-XX_*.tex)
-----------------------------------------

```
02-00_overview.tex                 "We organize results around N claims"
02-01_<characterization>.tex       what the data / setting looks like
02-02_<headline>.tex               THE main result (figure 1 anchor)
02-03_<validation>.tex             how we know it's real (sensitivity, CI)
02-04_<distribution>.tex           population view, subgroup breakdowns
02-05_<correlation>.tex            mechanism / explanatory variables
02-06_<subgroup>.tex               where does it work / fail
02-07_<cluster-or-extra>.tex       deeper cut, optional
```

Claim ↔ figure ↔ subsection
----------------------------

Each subsection should answer one question. Map:
- claim → 1 sentence in 02-XX
- figure → at most 1 main figure per subsection (others go to appendix)
- supporting tables → cited inline

Common failure modes
---------------------

- Figure dump — figures without claims attached
- Buried headline — main result on page 6
- Comparison fog — too many baselines without selection criteria
- Repeating Methods — describing how, not what was found

TODO
----

- Link to `components/figure/` for figure ↔ claim alignment audit
- Link to `5-review/paper-claim-audit/` — every claim cross-checked
