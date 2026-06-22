paper/sections — Per-Section Playbooks (Dimension B)
=======================================================

Each playbook here is **reference material for a specific section**:
which angles exist, common framings, what to avoid, what a strong
version looks like. Read by lifecycle skills (3-write / 4-revise /
5-review) when they target a particular .tex file under `0-sections/`.

Each playbook is a thin SKILL.md with slug `section-<name>` — invocable
directly for guidance, or pulled in by a stage skill as context.

Layout
------

```
sections/
├── section-intro/           hooks, motivation framings, contribution claim
├── section-methods/         formal vs operational angles, reproducibility
├── section-results/         story arc, claim mapping, figure choice
├── section-discussion/      limitation framing, implication framing, future-work
├── section-abstract/        condensation strategies (which 3 sentences to keep)
├── section-related-work/    positioning angles
└── section-appendix/        which extras live in appendix vs main paper
```

These map to file groups under `0-sections/` in a real paper folder:

```
0-sections/00_abstract.tex          ← section-abstract
0-sections/01_introduction.tex      ← section-intro
0-sections/02*.tex (Results)        ← section-results
0-sections/03*.tex (Discussion)     ← section-discussion
0-sections/04*.tex (Methods)        ← section-methods
0-sections/05_back-matter.tex       ← (covered by section-discussion / -appendix)
0-sections/A_*.tex .. E_*.tex       ← section-appendix
```

What playbooks are NOT
-----------------------

- NOT a writing skill — they don't produce prose. They provide guidance
  consumed by writing/revising skills.
- NOT venue-specific — venue conventions live in `_venue/` specialists.
- NOT tied to a stage — the same intro playbook informs both writing
  (3-write) and revising (4-revise).

Open questions (not yet decided)
---------------------------------

- Should there also be `section-title/` and `section-cover-letter/`?
  Cover letter is in `0-extra/`, not `0-sections/`, so it may belong
  elsewhere.
- Are 7 sections enough? Real papers may have `limitations/`,
  `ethics/`, `reproducibility/` as standalone sub-sections.
