haipipe-board-routing · Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.4.1 - 2026-08-01

- Routes current records into the canonical plural `## States` section while
  retaining singular State as an individual record name.

## 0.4.0 - 2026-08-01

- Routes current facts into `## State` and may update an Aim status only from
  inspected evidence, recording the transition reason in Log.
- Keeps `### Decision Now` checkboxes and page-level human gates human-owned.
- Replaced active `Where we are` instructions with the canonical State name.

## 0.3.0 - 2026-07-31

- The footer ends with a `Next:` line. JL, reading a bare routing footer: "what
  should I do? ... you can add a new line like Next:xxxx suggest what user to
  do next." The reply contract now closes with one concrete, immediately
  doable user action (open this page, tick these rows, hard-refresh and click
  this button); one step, never a list, never CC's own next task. The footer
  tells the human where records landed; the Next line tells them what to do
  about it.

## 0.2.0 - 2026-07-31

- Proposals land in Decision Now: whatever routing wants the human to decide
  (a PROPOSED tick, a drafted page, an open fork) is written as a row under the
  owning page's `## Where we are` `### Decision Now`, never left in chat
  (JL 260731: "don't make the decision here").
- The reply contract: every reply closes with the routing footer, one line per
  write, `page id · ## section`, so the human sees where each record landed
  (JL 260731: "show me which page, which section is updated after each response").
  Decisions are pointed at, never re-listed in chat: page id + row count only.
- Step 1 gains the no-write verdict: a DERIVED view, aggregated from state the
  pages already hold (a status readout, a progress table), deserves no write,
  because a copy of the state mirror drifts. First applied to the QB group
  readout the same day.

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
