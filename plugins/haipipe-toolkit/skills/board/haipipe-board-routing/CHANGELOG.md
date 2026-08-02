haipipe-board-routing · Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.9.0 - 2026-08-02

- **`haipipe-board-index` is merged into this skill and retired** (JL 260802: "maybe
  merge, I will do B"). This verb now owns BOTH altitudes: `board.md`'s structure and
  a page's sections. The family goes from one door, one altitude, two specs and one
  verb to one door, two specs, one verb.
- What the audit found, and why the merge and not a rename. Three of the index's five
  verbs were other people's work written a second time: `propose` and `materialize`
  are `haipipe-board`'s `open` action, `regroup` wrapped `haipipe-board/cli/regroup.py`,
  and `check` was a subset of `haipipe-board/cli/check.py`. Only `src/lanes.py` was
  code the family held nowhere else, and it moved here with the merge.
- **The gap this closes, which is the actual reason to do it.** A finding about a
  whole GROUP had no target and stayed in chat, because this verb resolved pages only
  while the block such a finding belongs in was owned by the other unit. The new
  landing rule: a group-altitude input lands in the group's intro prose in `board.md`
  `## Pages`, written at the section boundary, with `lanes.py` refreshing the block
  underneath. Decomposing a group finding onto its member pages was the alternative
  and is refused, because the pieces individually say less than the whole did.
- **The two altitudes keep separate approval rules, and the merge must not blur them.**
  A page-altitude write lands on its own, because it records something that already
  happened. A board-altitude write asks a person first, because it decides what pages
  will exist and the group letters it chooses are cited by every future page.
- `haipipe-board`'s `open` action keeps its own description of propose and materialize
  on purpose: a person opening their first board should not have to load a second
  skill. The duplication is now declared in both files rather than undiscovered, and
  the two must be corrected together.
- Inherited from `haipipe-board-index`, unchanged in substance: `lanes.py` round-trips
  (roster generated from `## Pages`, every typed cell kept, a new page arrives with `?`,
  a retired page's row dropped); kept cells are collected GLOBALLY by page id, so a
  page that changes group carries its cells with it, proven when 31 of 42 pages moved
  in the `01-boardform-260722` restructure; the board canvas shows how GROUPS connect
  and is never a second copy of the page roster; a group anchors at `#group-<token>`
  and is not a page.

## 0.8.0 - 2026-08-02

- Carries QA3's five-condition gate that runs BEFORE the reply, with `cli/gate.py`
  as its one command. ③ compares warnings PER PAGE so a concurrent session cannot
  fail your round; ① and ④ are reported as not tested rather than assumed. A round
  that changed prose also owes a cold read; a mechanics-only round does not.

## 0.7.0 - 2026-08-02

- A machine now CLOSES a `### Decision Now` row once the person has answered it,
  recording which option, who ruled, when, and the words they used (JL 260802:
  "I think you should close it automatically, please go ahead and do it").
  It still may not close a row nobody answered, and may not flip a page-level
  human gate; a machine's own recommendation is never an answer. Before this a
  row answered in chat and acted on within the hour still rendered as pending,
  so the page reported work as waiting that had already shipped.

## 0.6.1 - 2026-08-02

- Repointed the two inherited write laws and the claim-automation citation after `QC1b`'s
  260802 Content rebuild: `QC6 §9` is now `QC1b §4` and `QC6 §10` is now `QC1b §5`.

## 0.6.0 - 2026-08-02

- The reply LISTS its Decision Now rows in brief instead of naming a count
  (JL 260802: "I think you can also briefly list the 5 decisions here as well").
  One line per row, the ask plus the recommended option; the full row, with its
  `Part`, `Why now`, options, `Blocks` and default, still lives only on the page.
  This amends the count-only rule of 260731, which was too thin to act on: a
  number says something waits, not whether it is worth opening the page now.
- Note for the reader: `0.5.0` is in `SKILL.md` frontmatter with no entry below.
  It was not written by this change and its content is unknown here.

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
