---
name: haipipe-workbench-insight
description: >-
  The served face of the Insight family, paired with servers/workbench-insight:
  the 🔎 Insight tab of one InsightBoard page (its register cell, what it
  cites, who cites it, its gates, its log) and the 🔎 Insight Board surface one
  grain up (one selected cell, five Spaces: Scope · Run · Insight · Evidence ·
  Check). Read-only over the board on disk; every write stays with
  haipipe-insight and haipipe-insight-workflow. Trigger: insight tab, insight
  board tab, insight workbench, show the register, which cell answers this
  page, insight gates, /haipipe-workbench-insight.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-workbench-insight · the Insight ladder, seen from one cell

**LOAD `../../page/haipipe-workbench/SKILL.md` FIRST.** It owns what any
workbench is: lane, surface, writer, boundary. This file owns only the Insight
workbench's delta: which pages get the tab, what the two grains show, and the
fact that neither grain writes. The domain itself, DIKW, RI Runs, registers,
handoffs, belongs to `../haipipe-insight/SKILL.md` (the door),
`../haipipe-insight-workflow/SKILL.md` (the Runs) and
`../haipipe-page-insight/SKILL.md` (the Task-side Insight Page Face).

```text
this file      the two 🔎 tabs and their read-only contract
ref/insight-board.md   the Board grain: one cell, five Spaces, seven gates
the server     servers/workbench-insight/insightboard.py · insight_run_specs.py ·
               insight_handoff.py · assets/js/10-drawer/31-workbench-insight.js
the routes     /_board/insight?path=<board>/<page-rel>&file=<page-rel>    page grain
               /_board/insight-board?path=<board>/board.md&file=board.md    board grain
               /w/<board>/<page>/insight  ·  /w/<board>                     short forms
```

## 🧩 The four things

```text
📦 LANE      none of its own. It reads the InsightBoard: board.md, the MT01–MT04
             register pages and their ASCII cell grids, every answering D/I/K/W
             page (header, Opening, rows, citations, ## Log), and the
             runtime.yaml receipts a page names in the store.
🖼 SURFACE   🔎 Insight (page grain) and 🔎 Insight Board (board grain), both
             registered by 31-workbench-insight.js with `applies` = the page is laid
             out the InsightBoard way and sits on the DIKW ladder.
✍️ WRITER    none in the browser. The POST twins of both routes exist only so the
             shell's `tab: {url, write}` contract holds; they return the live URL
             and land no byte. Writers are the Insight owners named above.
🚧 BOUNDARY  it never allocates a Run, promotes a register cell, rewrites a
             finding, grants a handoff, or signs. Board grooming appears here as
             the read-only Check Space and nothing more.
```

## 📡 Page grain · 🔎 Insight

The tab applies to one page whose Face sits at
`<n>-<letter>-<group>/<ID>-<slug>/<ID>-<slug>.md` with a page-type on the
ladder (meta · question · data · information · knowledge · wisdom). It shows
that page as one rung: the register cell it answers (`QW1 × F`: one question
on one partition), what it cites down the chain, who cites it up the chain,
its gates, and its `## Log`. The board level is one link up from every page,
because the board UI had no other way to reach it than a typed URL (JL 260917).

## 📡 Board grain · 🔎 Insight Board

One selected cell, five Spaces, nothing invented; `ref/insight-board.md` has
the Space-by-Space contract. Run Space reads selected Insight work from frozen
Run Spec definitions (`insight_run_specs.py`: support · evidence · structure ·
write · deliver) and never allocates. Check Space reads handoff eligibility
from exact owner receipts (`insight_handoff.py`, `workflow/handoff.yaml`) and
never grants it.

## 🔗 Pairing

`servers/workbench-insight/` is this skill's served face; the two pair by
name, `haipipe-workbench-insight` with `workbench-insight`, like every other
row of the table in `servers/README.md`. `/w/<board>` resolves to
`/_board/insight-board` when `board.md` declares `board-kind: insight-board`
(or the folder is laid out as an InsightBoard); `/w/<board>/<page>/insight`
opens the page grain. `file=` may be omitted on both long routes; the server
derives it from `path=`.

## 📂 Files

- `ref/insight-board.md` · the five Spaces and seven gates of the board grain
- `../haipipe-insight/SKILL.md` · the Insight door and its vocabulary
- `../haipipe-insight-workflow/SKILL.md` · the owner-native Runs this surface projects
- `../haipipe-page-insight/SKILL.md` · the Task-side Insight Page and RI contract
- `../../page/haipipe-workbench/SKILL.md` · lane · surface · writer · boundary
- `../../../servers/workbench-insight/insightboard.py` · both views
- `../../../servers/workbench-insight/insight_run_specs.py` · frozen Run Spec reader
- `../../../servers/workbench-insight/insight_handoff.py` · handoff eligibility reader
- `../../../servers/workbench-insight/assets/js/10-drawer/31-workbench-insight.js` · the two registry rows
