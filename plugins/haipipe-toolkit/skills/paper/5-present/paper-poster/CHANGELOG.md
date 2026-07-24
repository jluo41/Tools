paper-poster — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [0.2.0] — 2026-07-24

**Split in two: this skill now owns the selection, not the layout.** It used to do
everything — read the paper, decide the content, *and* typeset it. The typesetting half
moved to `display/skills/haipipe-display-poster`, which renders any source, not just papers.

- What stays here: read `paper/sections/*.tex`, choose what a poster shows of this paper,
  condense it, copy the chosen figures — output `poster-content-plan.md` in the shape of
  `display/ref/content-plan-spec.md`, then dispatch to `haipipe-display-poster`.
- What left: LaTeX generation, compile, visual review, PPTX/SVG export.
- Why: paper is paper, display is display. A poster laid out from a grant application or a
  talk outline should not have to go through a paper skill.
