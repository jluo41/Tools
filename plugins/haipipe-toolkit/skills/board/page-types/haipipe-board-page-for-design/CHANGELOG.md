haipipe-board-page-for-design · Changelog
=============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.1.1 - 2026-08-05

Review fixes:

- The opener names this type's own risk, choosing among candidates, instead of
  sharing a byte-identical first line with `-for-display`.
- The REQUIRED `page-type: design` frontmatter key is stated: no filename shape
  marks a brief (base type resolution ③).
- The design-to-display handoff is named: the SELECTION record's new
  `downstream` line points, by path, at the display unit page the winning
  candidate becomes or updates.

## 0.1.0 - 2026-08-05

**Created on JL's ruling** (QB6 Decision Now, option A; his definition, 260805:
"we want to design some messages, say message A, B, C for one group of people;
the Content divisions ARE the different messages").

The page is the brief (audience, goal, constraints in the Opening); one Content
division per candidate, each carrying the artifact itself, its rationale, and
its fit to the brief's criteria; Aims are the criteria. The page closes on a
SELECTION record naming the winner, why, and each loser's disposition (dropped ·
kept for A/B test · merged). Sits upstream of for-display: design selects the
candidate, display accepts its render. A losing division is never silently
deleted, because the rationale for NOT choosing is part of the design record.
