haipipe-page-for-dash-section · Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.1.0 - 2026-08-09

First cut of the SECTION dash, on JL's 260809 ruling that each multi-unit paper family gets
a dash and every dash reads the venue structure.

- Ranks every section unit against the venue blueprint's allocation, so a person can choose what to work on next.
- Records that **Section includes Appendix** (JL 260809): one stage row, one Page Type, one dash. Two dash pages would measure one family twice.
- Declares `requires: S-Open-Venue`. This OVERTURNS the line in
  `haipipe-page-for-stage` that a dash never takes `requires:`. That line
  conflated two things: a dash still takes no human GATE and is still never
  counted as settled, but it cannot measure a family without the blueprint.
  One of four real dashes already declared it; the other three declared nothing.
- Ships under `paper/page-types/` because the paper family owns it (JL 260809,
  page-types are the page versions of a skill set).
- Loads `haipipe-page` for the base frame and `haipipe-page-for-stage` for the
  family grammar; restates neither.
