---
name: workbench-design
description: >-
  The design theme of the shared workbench frame: a design Block, each Job and
  each Task open on the frame's tabs Guide · Block · Job ▾ · Task ▾, each with the
  six Spaces (Description · Idea Studio · Audience Report | Work Details | Runs ·
  Delivery) as b12's s11 · s12 · s13 draw them, and a Runs panel whose buttons are
  the design run cards by level and Space. Read-only display: it shows the
  ladder's files and copies prompts; it never sets up a Block, launches a Job or
  writes anything (that is haipipe-design and the owning design skills). The
  shared Guide explains the family (Guide › Method: the design methods; Guide ›
  Related Paper). An older Design Folder board keeps its own page. Use to see or
  explain what a design screen shows and which file each view reads. Trigger:
  design workbench, design tab, design Block tab, design Job tab, design Task tab,
  design spaces on screen, theory of design, /workbench-design.
metadata:
  version: "0.15.0"
  last_updated: "2026-10-07"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /workbench-design · the design ladder on the shared frame

**LOAD `workbench` FIRST.** It owns the shared frame (tabs, the six Spaces, the Runs panel, the Guide). This skill
owns only the design theme's delta: what each Space shows at each level of the design ladder
(`haipipe-design/ref/design-ladder.md`), which file it reads, and which run cards its Runs panel shows.

## Where it runs

```text
servers/workbench-design/design_theme.py    the theme on the base frame (servers/workbench/frame.py): THEME "design"
servers/workbench-design/design_reader.py   reads a ladder Block from disk (read-only): board · job · design · runs
servers/workbench-design/design_views.py    draws each level's six Spaces from what the reader returns
servers/workbench-design/guide/             the Guide: guide.yaml, method.md and the method cards, related/
```

A Block is on the ladder when one of its Jobs pins a registered method on its face (`method: M04 m2`); the theme then
draws every level from the folders. Any other design Block reads as vanilla, and an older board keeps its own page
(below). The tabs are the frame's: Guide · Block · Job ▾ (every Job of the Block) · Task ▾ (the Job's Tasks, grouped
by step: t00, the designs in order with the dropped folded at the end, t99).

## The six Spaces, level by level

Each view reads the files named beside it; nothing is stored twice and nothing is computed that a Run did not write.

**Block** (b12 s11): one application, one channel.

| Space | Views | Reads |
|---|---|---|
| Description | Map · Goals · Methods · Inputs | `board.md ## Goals`; the Jobs' pins (the Map: goals down × methods across, each cell its chain of Jobs); the method registry (read only); `inputs/iN/manifest.yaml` |
| Idea Studio | the Block's topics | `studio/sNN-<topic>/` |
| Audience Report | Questions · Cost · Predicted vs observed · Method scorecard | `board.md ## Questions` and `reports/`; each Job's Run cards (`usage:`, times, rounds); `observed/eNN_<exp>/arms.csv` and `run-score-eNN` `scores.csv`; the scores summed per method version |
| Work Details | All · one per goal | one card per Job: goal · method version · inputs · state; open, a preview of its Tasks |
| Runs | All · Set up · Launch a Job · Report | the Block's `runs/run-<type>-<target>/run.yaml` |
| Delivery | — | `delivery/designs.json` · `designs.md`: every Job's release |

**Job** (b12 s12): one goal × one method version × one inputs version → N designs.

| Space | Views | Reads |
|---|---|---|
| Description | Goal · Method · Inputs | the face's pins; `inputs/goal.md`; `inputs/method.md` (the pinned version, its five steps); `inputs/` and `manifest.yaml` (the fence) |
| Idea Studio | the Job's topics | `studio/` |
| Audience Report | Reason ideas · Design display · Review whole · Predicted vs observed · Performance | t00's `chains.yaml`; each design as the reader sees it (an SMS as a phone bubble, a UI as its screen) with its process and review; t99's `ranking.csv`; each design's `prediction.yaml` beside its Exp arm; each Run's cost |
| Work Details | Reason ideas · Conduct & review · Review whole | t00, the design Tasks (each row opens its Task tab), t99 |
| Runs | Setup · Reason ideas · Conduct & review · Review whole | the Job's and its Tasks' Run cards |
| Delivery | designs.md · designs.json | `delivery/` |

**Task** (b12 s13): one tab for every Task; its run types decide what each Space shows.

| Space | t00 · reason ideas ② | a design ③ ④ | t99 · review whole ⑤ |
|---|---|---|---|
| Description | Task | Design · Evaluation | Task |
| Audience Report | Topics · Ideas | Tests · Drafts · Performance | Ranking · Coverage |
| Work Details | Chains | Elements (`elements.yaml`; the Rationale folded in) | Kept · Dropped |
| Runs | All · hard · soft | All · hard · soft | All · hard · soft |
| Idea Studio | its topics | its topics | its topics |
| Delivery | `ideas.yaml` to the design Tasks | released with the Job | the kept, to the Job |

## The Runs panel

Each Space shows the run cards of its level and Space from
`haipipe-design-workflow/references/run-cards.md` (`label · <Level> › <Space> · ^run-<type>- · views …`): the
button, the skill, the agent, what a person signs, and the prompt it copies, then the Runs already made of that type
with their status. Every Run is `run-<type>-<target>/`; hard or soft is read from its `run.yaml` `kind:`. Older names
(`rNN_<type>_<target>/`) still read.

The cards are the authority. Until `design_views.py` reads them (as the paper theme does,
`_run_cards(level, space, view)`), it types each Space's buttons in code, and those typed buttons may still differ
from the cards in their Run names, owners and prompts; where they differ, follow the card.

## Read-only

The theme writes nothing. A button copies a prompt; the Run it starts is written by the skill its card names
(`haipipe-design`, `-goal`, `-method`, `-unit`, `-workflow`, `-delivery`). A view that finds no file says which Run
writes it ("No ranking yet: t99's run-rank-t99").

## The Guide

The shared Guide's design family is `servers/workbench-design/guide/guide.yaml`: Guide › Method (`guide/method.md`
and its method cards, the 13 kinds of design method), Guide › Related Paper (`related/papers.md`), and the family's
skills. The drawings stay in the design Block `Tools/designs/b12_theme_design/studio/` (s02 the workbench, s03 the
methods and the design unit, s11 · s12 · s13 the levels, s21 Runs and skills).

## Older board page

An older board (`B00_DesignBoard-<name>/` with `0-BR-brief/` and `2-Design[-M<NN>]/Design-NN-<slug>/`) keeps its
own workbench until it is carried over: the page (`servers/workbench-design/design.py`, `/_board/design`) and the
board (`designboard.py`, `/_board/design-board`). Its contract is [ref/legacy/older-page.md](ref/legacy/older-page.md)
(this skill's text before 261007), the board grain [ref/design-board.md](ref/design-board.md), and the Space ↔ file
maps [ref/space-mapping.md](ref/space-mapping.md) (page) and
[ref/legacy/design-board-space-mapping.md](ref/legacy/design-board-space-mapping.md) (board). Its run cards are the
last section of `run-cards.md`; its Workbench Table is [ref/legacy/workbench-table-older.md](ref/legacy/workbench-table-older.md).
The ladder's Workbench Table, [ref/workbench-table.md](ref/workbench-table.md), is generated from the ladder cards by
`scripts/cards_table.py` (never edited by hand) and is the one `guide.yaml` names.

## Files

```text
workbench-design/
├── SKILL.md                               the ladder on the shared frame
├── ref/workbench-table.md                 the Workbench Table, generated from the ladder cards (guide.yaml names it)
├── scripts/cards_table.py                 writes it from run-cards.md
├── ref/design-board.md                    the older board (other skills link it here)
├── ref/space-mapping.md                   the older page's Space ↔ file map
└── ref/legacy/                            older-page.md · design-board-space-mapping.md
```
