haipipe-page-for-dash-value · Changelog
=======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.2.0 - 2026-08-10

The Value Dash now inventories the candidate Value Display card paired with every probe, as well
as the usual binding and staleness state. A card may be `candidate`, `parked`, or
`not-displayable`; Narrative selection and the formal Paper Display unit remain separate steps.

## 0.1.0 - 2026-08-09

First cut of the VALUE dash, on JL's 260809 ruling that each multi-unit paper family gets
a dash and every dash reads the venue structure.

- Holds the binding rule, the staleness rule, and the topic inventory, checked against the sections the desk requires.
- Records that **Value absorbs resource** (JL 260809): a resource question is an inward question answered by the task bank, which is the Value route's definition. `S-Work-R1-cms` already pointed at `tasks/A11_CMS-pipeline/` with no `route:` line, so it was an inward evidence page missing its contract.
- Declares `requires: S-Open-Venue`. This OVERTURNS the line in
  `haipipe-page-for-stage` that a dash never takes `requires:`. That line
  conflated two things: a dash still takes no human GATE and is still never
  counted as settled, but it cannot measure a family without the blueprint.
  One of four real dashes already declared it; the other three declared nothing.
- Ships under `paper/page-types/` because the paper family owns it (JL 260809,
  page-types are the page versions of a skill set).
- Loads `haipipe-page` for the base frame and `haipipe-page-for-stage` for the
  family grammar; restates neither.
