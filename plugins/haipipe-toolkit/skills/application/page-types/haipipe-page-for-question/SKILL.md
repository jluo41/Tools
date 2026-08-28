---
name: haipipe-page-for-question
description: >-
  The Page Type contract for one QUESTION page on an InsightBoard: the register of what is asked of one ladder rung, never what is concluded from it. Four exist per board, one facing each of D, I, K and W, each holding that rung's queue, one division per question, with the target, the raiser, what would answer it, and the current state. Use when a Brief raises a need, when someone reading the data becomes curious and the question has nowhere to go, when checking what is runnable today, or when a question is re-targeted to a different rung. Trigger: question page, question register, raise a question, what should we ask, insight queue, board backlog, re-target a question, page-type question, /haipipe-page-for-question.
metadata:
  version: "0.4.2"
  last_updated: "2026-08-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "MT"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "division 1 is Queue, always first; every later division's first word is a question id Q[DIKW]<n>, in id order"
---

# /haipipe-page-for-question · hold what is asked of one rung, and how far it has got

Load `haipipe-page` first, and `haipipe-plugin-pagex` when borrowing the inventory or a lower rung's register.

Declare `page-type: question` and `question-rung: data | information | knowledge | wisdom`.

Four pages exist per InsightBoard, in the `0-MT-meta/` group beside the Meta page:

```text
MT01-question-data/           question-rung: data           faces the D rung
MT02-question-information/    question-rung: information    faces the I rung
MT03-question-knowledge/      question-rung: knowledge      faces the K rung
MT04-question-wisdom/         question-rung: wisdom         faces the W rung

rung-major: the rung is one group (1-D-data/ .. 4-W-wisdom/)
partition-major: the rung spans every partition group (ref/partition.md)
```

## Why this Page exists

Until 260821 a question could only be a table row: `N<n>` in the Brief's Insight Needs, mirrored into `MT00-meta`'s Insight Roster. Two defects followed. A question raised on the InsightBoard itself, by someone reading the data rather than by a Brief, had no home at all, and `haipipe-page-for-meta` forbids one, because Meta raises no question of its own. And a row cannot carry why the question is asked now, what would answer it, or what it is blocked on.

JL ruled the split by rung on 260821, over a single flat register. A question is not asked of the board in general; it is asked of one rung, and the answer lands in that rung's group. Pairing the register with the rung it faces is what makes the queue readable: `MT01`'s queue and the D pages that answer it are the two halves of one sentence.

## Boundary

```text
MT00-meta          what data EXISTS                    describes, never asks
MT0N-question-*    what is ASKED of one rung           asks, never concludes
D/I/K/W page       the ANSWER                          concludes, cites its parent
Brief              which needs BLOCK a design          raises, never answers
```

**Nothing in the MT group concludes.** A question page may say the segment size is unknown. It may not say the segment is small. The moment a division states a value, a comparison or a preference, it belongs on a D, I, K or W page and fails here.

A question may be raised from either side. The Brief raises one when design is blocked; the board raises one when someone reading `MT00-meta` becomes curious. Both land here identically, and division 2 onward records which.

## Question ids

The rung letter is in the id, so a question names its own home.

```text
QD<n>   registered on MT01     answered on the D rung, in the owning group(s)
QI<n>   registered on MT02     answered on the I rung, in the owning group(s)
QK<n>   registered on MT03     answered on the K rung, in the owning group(s)
QW<n>   registered on MT04     answered on the W rung, in the owning group(s)
```

Numbering runs per page, so `QD1` and `QI1` coexist. The id is permanent: a question that is re-targeted moves page and takes a NEW id, and its old division stays behind as a one-line tombstone naming the successor. Nothing that was ever raised silently disappears.

## Partition-major boards: the Queue gains columns (0.2.0)

On a partition-major InsightBoard (`haipipe-application` `ref/partition.md`) a question is written ONCE and asked per partition. The id stays partition-free, `QK1` and never `QK1-B`. The Queue carries one column per partition registered on `MT00`, plus an X column whenever the register holds an X-routed question; X is the cross GROUP, not a partition, so a register with no cross question carries no X column:

```text
id   question                              F·full      B·youngmale   X·cross
──────────────────────────────────────────────────────────────────────────────
QK1  which arm separates, rivals out?      ✅ FK01     🔨 EVIDENCE   ·
QK2  do the arm effects genuinely differ?  ·           ·             ⬜ ready
```

Three cell rules, all closing checks on this layout:

- **A blank cell is illegal.** Every cell is a state, a `🚫` refusal with a reason, or a dot.
- **A dot cell is an explicit routing, restated in the question's division.** A cross-partition question cannot be answered by a per-partition page, so its per-partition cells are `·` and its X cell is live; the reverse holds for per-partition questions with no cross half.
- **A refused cell is the register's half of the mirror rule.** When a partition group is missing a page its template has, the refusal lives HERE, `🚫` plus the reason, so the gap is a recorded decision rather than a silence.

The question's division stays ONE division; it records per-partition standing inside "where it stands" rather than splitting per partition. On a rung-major board this section does not apply and the Queue keeps its single-column shape.

## Fixed Content outline

```text
### 1 · Queue               this rung's questions, target, raiser, state, blocker
#### 2 · Q<R>1 · <slug>     one division per question, in id order
#### 3 · Q<R>2 · <slug>
```

**Queue** is the whole page in one screen. One row per question:

```text
id   question, one line              raised by   answering page   state
─────────────────────────────────────────────────────────────────────────────
QD1  what do the 13 arms say?        BR00 · N4   —                ⬜ ready
QD2  which rows carry an opt-out?    MT00 read   D02-optout       🔨 EVIDENCE
```

`state` is one of `⬜ ready` when nothing blocks it, `⬜ blocked on <id>` when something does, `🔨 <phase>` once the answering page exists, `🟡 partial` when part of the ask has closed and more is owed, `✅ answered` once the answering page closes, and `🚫 <reason>` when the cell closes WITHOUT an answer — refusal reasons (thin, F-only, defer, no-measure) and the tombstone (`🚫 retired`) share ONE grammar: 🚫 always means closed-without-answer, and the reason follows. Only `✅` and `🚫` settle. A `🟡` is never folded into an answered count and keeps its row lap-eligible UNTIL its page states why the remainder cannot close: the cell then reads `🟡 <page> final`, is settled-partial, leaves the lap, and still never joins an answered count. A cell or row may name the planned answering page beside `⬜` (`⬜ FD01`), which reads: the page is allocated and still planned; a `⬜` may also carry a short reason annotation (`⬜ calc` — computed, not yet authored), and an annotated `⬜` is still OPEN, never a refusal. A rollup may abbreviate a token only as `<mark>(<letter>)` with a legend line mapping it to the full token — where the grammar is silent, legends invent, which is how `⬜OPEN` and `🟡f` were coined. When a header count and the Queue rows disagree, the Queue rows are the record and the header is stale — and "header" means EVERY on-register restatement of the Queue: the state line, the Diagram, the Opening. Status WORDS derive by fixed mapping (any lap-eligible cell → 🟡 PARTIAL; all cells terminal → ✅ SETTLED), so reconciling them is the same register-pen act as reconciling a count. A mark's spelling includes its spacing (`🚫 F-only`, never `🚫Fonly`); canonical forward, and a live board is re-spelled only in an authorized sweep that re-pads its tables in the same pass. The `⬜` annotations are the register pen's, like every cell mark: a note about work is state.

**Each question division** owes a reader four things and nothing else:

- **The ask**, in one line, in the words the data uses.
- **Why now**, which is what is blocked or what prompted it. A Brief-raised question names the Brief's Aim; a board-raised question names what was being read.
- **What would answer it**, which is the shape of an acceptable answer, not a guess at its value. "A count of distinct message bodies per arm" is legitimate; "roughly thirteen distinct bodies" has already answered.
- **Where it stands**, naming the answering page once one exists.

A division that argues for an expected answer has decided, and fails the closing checks.

## Aims and States carry the status

One Aim per question, so the engine's own machinery is the status board. The `## States` section is what a reader checks and what `git diff` shows moving.

```text
## Aims                              ## States
### A1 · Queue                       ### A1 · Queue
- A1.1 every raised question         - ✅ A1.1 · four rows, all honest
  is visible, answered or not
#### A2 · QD1                        #### A2 · QD1
- A2.1 the corpus is described       - ⬜ A2.1 · no answering page yet
  Done when: QD1 reaches a D page
```

An Aim's **Done when** names the rung, and only this page's rung. `MT01`'s Aims close at a D page; a D page that turns out to license a recommendation has produced a W claim, and that is a new `QW<n>` on `MT04`, not a broader Done-when here.

## Plugins

```text
outline/    ✅   the plan, like any page
pagex/      ✅   borrow MT00's inventory and the rung below's register
probe/      ❌   FORBIDDEN
display/    ❌   FORBIDDEN
```

**A question page owns no `probe/`.** A probe card reaches Task or Discovery and brings an answer back; if a question page could raise one, the question and its answer would share a folder and the MT group would stop being question-only. The card belongs to the page that answers, at `<D|I|K|W page>/probe/PP<NN>-<slug>/`, and that page names the question id it serves.

`display/` is forbidden for the same reason: a figure is an answer.

## Staleness

A question does not go stale; its answer does. When a source re-runs and reopens a D page, the question whose row names that page moves back from `✅ answered` to `🔨`. The Queue row is the visible consequence, and it is updated by whoever reopens the answering page.

## Closing checks

- Every question in the Queue has a division, and every division has a Queue row.
- No division states a value, a comparison, a rank or a preference.
- No question carries a hoped-for answer, in either its ask or its what-would-answer-it.
- Every question names its raiser: a Brief need id, or what was being read.
- Every `⬜ blocked on <id>` names a real id on this board.
- Every question's target rung is this page's rung. A question facing another rung has been mis-filed and moves.
- The page owns no `probe/` and no `display/`.
- A re-targeted question left a tombstone naming its successor.
- Partition-major only: no cell is blank; every dot cell's routing is restated in its question's division; every 🚫 cell carries a reason.

This variant owns no scripts.
