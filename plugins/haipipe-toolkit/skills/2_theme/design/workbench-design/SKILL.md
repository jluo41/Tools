---
name: workbench-design
description: >-
  The design theme of the shared workbench frame: a design Block, each Job and
  each Task open on the frame's tabs Guide · Block · Job ▾ · Task ▾, each with the
  six Spaces (Description · Idea Studio · Audience Report | Work Details | Runs ·
  Delivery) as b12's s11 · s12 · s13 draw them, and a Runs panel whose buttons are
  the design run cards by level and Space. It shows the ladder's files and
  copies prompts; it never sets up a Block or launches a Job (haipipe-design and
  the owning design skills do), and the one thing it writes is a person's own
  Review and approve of a Job's release (POST /_board/design-ladder-act). The
  shared Guide explains the family (Guide › Method: the design methods; Guide ›
  Related Paper). An older Design Folder board keeps its own page. Use to see or
  explain what a design screen shows and which file each view reads. Trigger:
  design workbench, design tab, design Block tab, design Job tab, design Task tab,
  design spaces on screen, theory of design, /workbench-design.
metadata:
  version: "0.18.0"
  last_updated: "2026-11-01"
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

## A Job is named by its folder

Every view that names a Job shows its folder name as it is, `jNN_<goal name>_<method name>`
(`j01_prepare-before-visit_goal-only`), as the Job ▾ menu does: a card title, a link, a list of Jobs, a column head
(JL 261011: "I don't want we just have jNN here, not readable"). Never the bare `jNN`: it says nothing on its own.
The ids (`G01`, `M01 m2`, `i1`) stay on the face as pins and may follow the name as plain detail. An older id-form
folder (`j03_g01-review-new-rx_m04-actionable-insights`) shows the same way, by its folder name.

Two Jobs can share their words: one method's two versions on one goal (`j05_review-new-rx_raw-data-agent` pins M05 m2
and is held, `j06_…` pins M05 m3), or one method on two inputs versions. Both stay, since a changed method or inputs
is a new Job (`haipipe-design/ref/design-ladder.md` rule 1). The Job ▾ menu then adds, after the folder name as it
is, the pins that tell them apart and `held`: `j05_review-new-rx_raw-data-agent · m2 · held`,
`j06_review-new-rx_raw-data-agent · m3` (`design_theme._job_option`; JL 261023: "why we have two here?").

## What a reader with five minutes sees (JL 261012)

From the 10-08 demo to leadership: the Block's Audience Report opens on **Summary**, one page built only from what the
Runs wrote (no new claim), one row per Job and no design cards: a design and its full reason stay on its own page and
in its Job's Review whole; **Rounds** is the Block's memory, one round per inputs version; every predicted number
shows its basis (`against · by · why`: in full on a card, on hover in a table); a held Job says why instead of empty
counts; and freezing and releasing are one button, **Review and approve**, the one place a person reviews.

The Summary leads with the bottom line, the Opening of each Block question partly or fully answered (open ones are
left out); it names methods by name, with ids such as `M04 m3 · inputs i1` only on hover (the demo: "without naming
every part"); each released Job says who approved it and when, from its `run-release-j<NN>` card's `signed:` line, the
full line on hover; its Next line is plain words, never a Run name; and it links the one-page PDF that
haipipe-design-delivery's `summary.py` builds into `delivery/summary.pdf` (JL 261013).

## On the focus page: the j01 letters (b12 j01, 261101)

The focus page (`layout=focus`, what `/wb` opens) draws a design Block, Job and Task in b12 j01's letters, with the
parts every theme's page shares (`servers/workbench/ui_parts.py`): Report is a view's 📊 Results only; Work is ⚙️ Process
(🙋 what waits on you first, then the view's steps, each row ending in a state word, its Run's prompt one Copy away)
over the same Results. `servers/workbench-design/design_focus.py` draws them; `focus_page.py` asks it through one hook,
`design_views`, as it asks the paper and insight themes'.

```text
Block (s51, s52)  Summary · Goals · Jobs · Rounds · Methods
Job   (s54, s55)  Setup · Ideas · Designs · Ranking · Release
Task  (s57, s58)  by type, one view per step:
                  💡 t00 reason ideas   Inputs · Chains · Ideas · Fence check
                  ✏️ one design         Draft · Verify · Revise · State
                  🏆 t99 review whole   Rank · Coverage · Kept
```

🙋 at the Block: an unsigned goal, and each Job whose release is ready ("Review" opens its Release view). At the Job:
Review and approve (the panel on Release, POST /_board/design-ladder-act), then the close. A Task never asks you: its
Process is In → who works → Out, the step's state and its prompt. The Results are the six-Space page's own views
(`design_views`), so the two pages agree. Tests: `tests/test_design_focus.py`.

## The six Spaces, level by level

Each view reads the files named beside it; nothing is stored twice and nothing is computed that a Run did not write.

**Block** (b12 s11): one application, one channel.

| Space | Views | Reads |
|---|---|---|
| Description | Map · Goals · Methods · Inputs | `board.md ## Goals`; the Jobs' pins (the Map: goals down × methods across, each cell its chain of Jobs); the method registry (read only); `inputs/iN/manifest.yaml` |
| Idea Studio | the Block's topics | `sNN-<topic>/` |
| Audience Report | Summary · Rounds · Questions · Predicted vs observed · Method scorecard · Cost | Summary (first, JL 261012): the goal, the answered questions' Openings, one row per Job (method, state and who approved, top design, prediction with its why on hover), the next step, `close:`, the one-page PDF; no design cards; Rounds: one round per `inputs/iN/manifest.yaml`, its Jobs, releases and Exp results; `board.md ## Questions` and `reports/`; `observed/eNN_<exp>/arms.csv` and `run-score-eNN` `scores.csv`; the scores summed per method version; each Job's Run cards (`usage:`, times, rounds) |
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
| Work Details | its steps: 1 · See input · 2 · Reason · 3 · Fence check | 1 · Generate · 2 · Verify · 3 · Revise · 4 · Predict | 1 · Rank · 2 · Keep · 3 · Release (🙋 Review and approve) |
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

## Read-only, but one sign

A button copies a prompt; the Run it starts is written by the skill its card names (`haipipe-design`, `-goal`,
`-method`, `-unit`, `-workflow`, `-delivery`). A view that finds no file says which Run writes it ("No ranking yet:
t99's run-rank-t99").

One thing a person does on the screen itself (JL 261023: "design the work in a way that we human can operate this
system as well"): **🙋 Review and approve**, at the top of a Job's Delivery. It lists each kept design as it reads with
its prediction, as `haipipe-design-delivery`'s own `release.py` would release it today (its dry run); the person
ticks "I read each kept design as it reads, its prediction and why" and approves once. `POST
/_board/design-ladder-act` (`servers/workbench-design/design_ladder_act.py`) then runs `release.py` with today's date
(it checks every design before it writes anything) and adds a pass to `run-freeze-predictions-jNN` and
`run-release-jNN`, each card `by: a person` and `signed: ✅ <YYMMDD> · a person, in the workbench`; the Summary shows
it as "approved ✅ <YYMMDD>", no name. A Job that is not ready says why (a held Job, its hold), and a released one
says who signed and when. The route answers only a page of this host and never a read-only host.

## The Guide

The shared Guide's design family is `servers/workbench-design/guide/guide.yaml`: Guide › Method (`guide/method.md`
and its method cards, the 13 kinds of design method), Guide › Related Paper (`related/papers.md`), and the family's
skills. The drawings stay in the blueprint Block `Tools/blueprints/Project-Ladder/work/b12_theme_design/studio/` (s02 the workbench, s03 the
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
