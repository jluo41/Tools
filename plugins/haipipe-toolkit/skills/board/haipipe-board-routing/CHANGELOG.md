haipipe-board-routing · Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.1.0 - 2026-07-31

- First cut, created on JL's order, from QC6 §8's settled shape: routing is the unit
  VERB (one input, find its owning page, write it back) and digest, when it arrives,
  is this verb fanned out over a session transcript, calling routing per input.
- The five-step route reads board.md's `## Pages` as the ONLY registry, because an
  id does not reliably predict a folder (QC6 §9: pages move and letters are
  history), and it ends in exactly three states: LANDED, PROPOSED (never a silent
  page creation), or REPORTED (another family's board gets a report, not an edit).
- Both write laws are inherited, not invented: the tick law (QC6 §10, propose a
  tick, never tick or flip `state:`) and the cross-board law (QB1 §4, mechanical
  writes always, editorial writes never on someone else's board).
- Owns no scripts: the verb is the loaded contract plus the page and sentence
  specs. The named next step is sharing serve.py's anchored-append write path with
  the clicked-comment flow, so a routed write cannot invent its own byte-offset
  splice (the QB4d casualty of 260730).
