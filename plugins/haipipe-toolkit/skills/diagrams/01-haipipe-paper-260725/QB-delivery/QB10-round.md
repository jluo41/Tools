# Delivery Round: one batch of feedback, kept together from review to resubmission

state: 🟡 PARTIAL
owner: JL
method: keep each batch of review, rebuttal, revision, and resubmission as one dated round record

## Opening

How does a paper record what happened after it was submitted?

A round is one externally triggered batch: reviews arrive, decisions are taken, edits are applied, a response is written, the paper is rebuilt and resubmitted. It repeats until the paper is accepted or retired. The danger is splitting one batch across pages, so nobody can say which change answered which reviewer.

**Where this page sits**: QB9 Build owns the diff, the compile, and the shipment of whatever a round produces.
This concern owns the record: what was asked, what was decided, what changed, and what went back.

**Why a batch is the unit and not a reviewer**: a single edit often answers two reviewers, and a single reviewer often raises points answered in three places.
Keeping the batch whole is what lets a later reader follow one round end to end instead of reconstructing it.

**Why the same four pages repeat rather than multiply**: round two runs the same reconcile, compile, review, and submit chain as round one.
Duplicating a page set per round would give the paper four new pages every cycle and no better record.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../BoardSkillBoard-260722/QPs-page-structure/QPs1-overall/QPs1-overall.md` and are not restated here.

**This page DESIGNS; the paper board SHOWS**: `### 2` states what a paper must carry for this concern, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

**Say Round, never Response**: JL renamed it on 260729 and the old word describes only one quarter of what a round holds.
A sentence that calls the batch a response has dropped the revision and the resubmission from it.

## Diagram

**One round, four moves**: what comes in, what goes back, and what repeats.

```text
   📮 submission
        │
        ▼
   ┏━━━━ ROUND n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ 📥 review      what the editor and reviewers ┃
   ┃                 asked                        ┃
   ┃ ✍️ rebuttal     what we answer, point by     ┃
   ┃                 point                        ┃
   ┃ 🔧 revision     what actually changed, and   ┃
   ┃                 on which page                ┃
   ┃ 📤 resubmission the package that went back   ┃
   ┗━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┛
                        ▼
              ROUND n+1  …  ✅ accepted / 🗑 retired

  🔁 the SAME four submission pages are reused every round
  🚫 no new page set per round ── the record is dated, not duplicated
  🚪 the gate: every response is applied or explicitly DECLINED, and
     the resubmission matches the round record
```

## Content

### 1 · The delivery contract

**What Round owes**: a batch a later reader can follow end to end.

```text
  📥 CONSUMES                📤 PROJECTS TO           🚪 GATE
  reviewer and editor   ━━▶  rebuttal           ━━▶  every response is
  input                      response letter          applied or
  the accepted prior         revised manuscript       explicitly declined,
  submission                 diff · package           and the resubmission
                                                      matches the record
```

📜 Establishes the batch as the unit, and what has to be true before it goes back.

| Field | Contract |
|---|---|
| Lifecycle | Submission and every later batch of external feedback and revision. |
| Authority | One `S-Round-*` page per batch, with dated decisions and applied changes. |
| Projects to | Rebuttal, response letter, revised manuscript, diff, and resubmission package. |
| Skills | `haipipe-paper-round`, rebuttal, diff, compile, and ship leaves. |
| Consumes | Reviewer/editor input plus the accepted prior submission. |
| Gate | A human verifies every response is applied or explicitly declined and the resubmission matches the round record. |
| Open gaps | Board filename resolution still needs `Round` added as a first-class family. |

#### 1.1 · Declining a reviewer counts as answering them
(the gate says applied OR explicitly declined, and the second half is the one that gets skipped)
A response that quietly ignores a point looks identical, in the record, to one nobody read.
Writing down that a change was declined, and why, is what lets the next round argue from a position rather than rediscover the objection.

### 2 · What we want on the paper board

**The group we are designing**: one Q page for the rule, and dated round pages as they happen.

```text
  🎯 WHAT WE WANT a paper to carry for this concern
  ### Delivery · Round
        📄 QR0-round-delivery.md   a Q page: how THIS paper runs a round
        📄 S-Round-1-<slug>.md     one page per BATCH, added when it happens
        📄 S-Round-2-<slug>.md     …

  ⚡ this concern owns NO STAGE ── `../../paper/haipipe-paper-stage/stages/index.yml` has no `round` key
  ⚠️ `Round` is not yet a first-class Board family, so a filename does
     not resolve today
  🔁 the four Build submission pages are REUSED every round, and live
     under Delivery · Build, not here
```

🎯 Establishes what a paper board must show for this concern, and the one thing that stops it working today.

#### 2.1 · The group starts as one Q page and grows only when a round happens
(a paper before submission has a rule and no rounds, and that is the correct empty state)
`QR0-round-delivery.md` states how this paper will run a round, and it exists from the start.
An `S-Round-n` page appears the day reviews arrive and never before, so an empty group here means the paper has not been reviewed rather than that something is missing.

#### 2.2 · Round is not a Board family yet, and that is the blocker
(the naming is ruled and the tooling has not caught up)
An S filename resolves from `board_family`, `board_unit`, and `board_slug`, and the recognized families do not include Round.
So `S-Round-1-<slug>.md` is what the design wants and not something `stage.py resolve` can produce, which is why the paper's `7-round/` folder is empty.

#### 2.3 · Where the MISQ paper stands against this
(the rule page exists and no round has happened)
`Delivery · Round` holds `QR0-round-delivery.md`, and `0-lifecycle/7-round/` is empty.
That is the correct state for a paper that has not been submitted, so nothing here is behind except the family resolution in `2.2`.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · The batch is the unit, and it is called Round.
  **Done when:** no page on this board or a paper board calls the batch a Response, and one round's review, decision, change, and shipped artifact sit together.
- A1.2 · A declined response is recorded as explicitly declined.
  **Done when:** a round record shows, for every reviewer point, either the change that answered it or the reason it was declined.

### A2 · 🎯 What we want on the paper board
- A2.1 · `Round` resolves as a first-class Board family.
  **Done when:** `stage.py resolve` composes `S-Round-<unit>-<slug>.md`, and a paper can open a round page without a workaround.
- A2.2 · A paper board shows one Q page from the start and gains a round page per batch.
  **Done when:** `Delivery · Round` holds a round-delivery Q page before submission, and one `S-Round-n` page appears per batch afterwards.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · JL renamed Response to Round on 260729 and defined it as batch ownership; the Law carries it.
- 🔨 A1.2 · Written into `§1.1` and the Gate row. No round has run, so nothing has tested whether a declined point is actually recorded.

### A2 · 🎯 What we want on the paper board
- ⬜ A2.1 · Not started, and it is this concern's blocker. Round is not among the Board families, so `S-Round-*` cannot be resolved and `7-round/` stays empty.
- ✅ A2.2 · Built as designed on the MISQ paper: `Delivery · Round` holds `QR0-round-delivery.md`, and the absence of round pages is correct for an unsubmitted paper.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `board.md` · the `## Pages` order and the Board Map row for this concern
- `QB9-build.md` · owns the four submission pages a round reuses, plus the diff and the compile

📥 **Input files** · what the work reads

- `../../board/haipipe-board/cli/stage.py` · resolves an S filename from family, unit, and slug, and does not yet know Round

## Law

- Use Round, not Response. One batch is one round, and every round keeps its review, decision, applied change, and shipped artifact together.
  The four Build submission pages are reused every round; a round never duplicates a page set.
  A response is answered when it is applied or when it is explicitly declined with a reason.

## Glossary

- **Round**: one externally triggered batch of review, rebuttal, revision, and resubmission.

## Log

260802 · Migrated to the QB4 page contract and given `### 2 · What we want on the paper board`. The blocker is now stated where a reader meets it: `Round` is not a Board family, so `stage.py resolve` cannot compose an `S-Round-*` filename and `7-round/` stays empty. An empty group here is the correct state for an unsubmitted paper, which the page now says rather than leaving it to look like a gap.
260729 · JL renamed Response to Round and defined it as batch/iteration ownership.
