haipipe-board-page · Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.2.0 - 2026-07-31

- Decision Now: the one RESERVED subsection name inside `## Where we are` (JL, same
  day: "don't make the decision here ... Always go to the corresponding Q's Where we
  are's subsection of Decision Now"). It lists the decisions a machine proposes and
  the human must make, one `- [ ]` row each with the ask, the options, and a
  recommendation; the human answers by ticking; an answered row moves into the
  page's dated record. The 260729 contextual-naming rule stands for every other
  subsection; this is its single exception.
- The tick rule now names the landing spot: a machine PROPOSES a tick as a Decision
  Now row, never in chat alone.
- The board pages `QB4e` (the Where-we-are face) and `QC6` on the design board carry
  the first two live subsections.

## 0.1.0 - 2026-07-31

- First cut, created on JL's order ("make the haipipe-board thinner, and have other
  skills, like haipipe-board-page ... please creating them now") from the roster the
  design board had already settled: QC6 §8's shape is one door, two SPECS, two VERBS,
  and this is the page SPEC the routing and digest verbs LOAD.
- Contract-first: no code moved. It owns what a page IS (the three kinds over one
  base, the seven sections in their fixed order, the write anchors), and it cites
  `haipipe-board/ref/q-template.md` as the authority rather than forking it.
- Carries the two machine-write rules with their provenance: writes land at a
  SECTION BOUNDARY, never a byte offset (QC6 §9, after a concurrent session spliced
  a heading into the middle of another page's Question sentence on 260730), and a
  transcript-reading verb may propose a tick but never tick or flip `state:`
  (QC6 §10, because reporting a claim is not verifying it).
- Names its own next step from QC6 §7: `serve.py`'s `CHAT_RULES` becomes a consumer
  of this contract instead of a hand-rolled copy, which has already rotted once
  (QB5d caught it describing a page shape that no longer existed).
