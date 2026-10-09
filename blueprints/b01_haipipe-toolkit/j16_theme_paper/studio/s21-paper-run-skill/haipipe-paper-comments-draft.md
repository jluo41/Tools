---
name: haipipe-paper-comments
description: >-
  Propose and organize what people say about a paper: a review report, an editor's letter, a meeting, a
  coauthor pass, an advisor's notes. Splits a batch into points with ids by source (R1.1, E1.2, A1.1, M2.3),
  groups them into named Review Items (Review-<slug>), routes each item to its owner, records the reply and
  its state, and proposes the Board questions worth answering before anyone asks again. A review round is one
  kind of batch: it lives in the version Job that answers it. Use when taking in comments, triaging them,
  answering a review, or turning recurring comments into questions.
metadata:
  version: "0.1.0-draft"
  last_updated: "2026-10-07"
  replaces: haipipe-paper-round (0.9.0); its name stays readable during the rename
  group-token: "CM"
  outline:
    mode: fixed
    source: "this SKILL.md"
    surface: "Opening → Outline → Content → Aims"
    shape: "Batch Identity and Intake → Points → Review Items → Decisions and Routes → Applied and Checked Changes → Replies → Proposed Questions → Close Receipt"
---

# /haipipe-paper-comments · take in what people say, answer every point once

DRAFT (b16, 261007, JL: "change it to the haipipe-paper-comments … just for propose and organize the questions
from all kinds of people, from review report and from the meeting"). Not installed: it lives in the paper
design Block until the rename with haipipe-paper-round is planned (b04 owns skill renames).

Load `haipipe-page`, `haipipe-page-workflow`, `haipipe-paper-workflow`, then this PageType. A batch Page is a
Page like any other (`page-type: comments`); triage alone allocates no Run.

## What changed from haipipe-paper-round

```text
haipipe-paper-round (0.9.0)              haipipe-paper-comments (draft)
one Round = one review cycle             one batch = any source: review · editor · meeting · coauthor · advisor
Bc-<desk>-Round/RD<NN>-…/                the batch sits in the level it is about (below)
concern table, one row per point         points (one row per point, an id by source)
                                         + Review Items: Review-<slug> groups the points it answers
response package in the Round            the reply is the answering Job's Letters › response Page
sent/ + released/ inside the Round       the sends' own delivery/…/sent/ (the reviewed Job, the answering Job)
(none)                                   proposed questions: a point worth answering for every reader
```

Everything else carries over unchanged: atomize before routing, every point appears exactly once, routing
to the owner (the table below), severity mapping, human authority, and CHECK before close.

## 🔄 Batch kinds and where each lives

A batch lives in the level it is about, and shows in that level's Audience Report.

```text
kind      source                      lives in                         shows in
review    reviewers' reports          the version Job that ANSWERS it   Job › Audience Report › Comments
editor    the editor's letter         the same answering Job            (same batch as its reviews)
coauthor  a coauthor's pass on a draft the version Job it read          Job › Audience Report › Comments
meeting   what a meeting said         the Board, or the Job it is about Block › Related Questions (proposed qs)
advisor   an advisor's notes          the Board, or the Job it is about Comments, then proposed questions
```

A review round is therefore the next send, not a Page beside the sends (b16 s12: a Job is one send):

```text
j01_v1_<desk>/   sent <date> → decision: revise           closes; delivery/…/sent/ is the reviewed build
      ↓ reviews arrive
j02_v2_<desk>/   answers: CM01 (the reviews of j01)       the batch lives here
   ├── comments/CM01-<desk>-review-<YYYYMMDD>/            points · Review Items · routes
   ├── S-<desk>-Main-…/                                   carried from j01, revised by the items' Runs
   ├── t9N_response/                                      Letters › response: the reply, item by item
   └── delivery/…/sent/                                   the answering build (was the Round's released/)
```

## 🪪 Batch identity

```text
batch-id       CM<NN>, unique across the paper
page-id        CM<NN>-<desk|story>-<kind>-<YYYYMMDD>
kind           review · editor · coauthor · meeting · advisor
about          the build or Page it comments on (a frozen sent build for a review), or the Story
received-from  reviewer labels · editor · coauthor · meeting attendees · advisor
received-at    date and where the source is kept (feedback/)
answered-by    the Job that answers it (a review), or explicit none
response-due   date, none, or unknown
```

Existing `RD<NN>-…` Round Pages stay readable history and are read as review batches; they are not renamed.

## 🔢 Points: one row per thing a person said

Atomize a batch before routing. Each point keeps an id by its source:

```text
R<n>.<k>   reviewer n, point k          E<n>.<k>   editor n, point k
A<n>.<k>   coauthor n, point k          M<n>.<k>   meeting n, point k
V<n>.<k>   advisor n, point k
```

The point table keeps today's concern fields: id · source and anchor · verbatim quote or faithful pointer ·
issue kind · reviewer severity as supplied · local severity (blocking · material · editorial · unresolved) ·
the exact point · its Review Item. Every received point appears exactly once and belongs to exactly one
Review Item. Preserve received wording in `feedback/`; never rewrite it into a cleaner second source.

## 🧾 Review Items: what gets answered

A Review Item is one concern, named and numbered, that may gather the same point from several people. It is
the unit that is routed, worked, answered and listed on the screen.

```text
## Review Items
| item                | cites              | lands on                          | work                     | reply | state    |
|---------------------|--------------------|-----------------------------------|--------------------------|-------|----------|
| Review-causal-claim | R1.1 · R1.3 · E1.2 | S-<desk>-Main-3-Results ¶2 · C2   | run-revise-causal-claim  | P3    | answered |
```

- **item** `Review-<slug>`, unique in the batch; the row order is its number on screen.
- **cites** the point ids it answers, joined by " · ".
- **lands on** the owning Page stem (+ ¶N), then any claim ids; a Section's tab lists the items that start
  with its stem.
- **work** the owner-native Run that answers it (`run-revise-<slug>` on a Section, `<task> › rNN` for new
  analysis), or `declined`.
- **reply** the paragraph id in the answering Job's response Page.
- **state** open · routed · applied · answered · declined · deferred (the Round's states, unchanged).

## 🔀 Route work; do not absorb it

| Item is about | Owner |
|---|---|
| evidence the paper does not hold | the Story's §5 support and its §6 Discovery or §7 Task need |
| contribution, claim role, or order | the Story's Narrative row (and a version's Draft-Main) |
| a Section's argument, wording, placement or limit | the owning Section Page (a revise Run named for the item) |
| a missing analysis or fact | the consuming Page's typed Evidence Item; a new study also changes Story §7 |
| a citation, a number, a table or figure | the consuming Page's CITE, VALUE or DISPLAY Evidence Item |
| the reply's wording and coverage | the answering Job's response Page |

A routed item lands in its owner's `draft/records/<stem>-feedback.md` register, as Rounds do today; this Page
never writes into another Page's folder. `applied` needs the owner's checked after-version.

## ❓ Proposed questions

A point that any reader would raise again is worth answering once for everyone. After routing, propose it as
a Board question in Block › Audience Report › Related Questions, in its group (reviewer · coauthor · editor ·
reader), citing the points it came from:

```text
RV1  Is the effect causal, or selection?   ← cites R1.1 · M2.3   → reports/qNN_<topic>/
```

The skill proposes; a person adds it through `haipipe-question` (Ask a Question). A meeting or advisor batch
often ends here: its points become questions rather than Section changes.

## ✋ Human authority

A person approves consequential decisions (accept · narrow · decline · defer), the reply, each proposed
question that is adopted, and the batch's close. A machine proposes points, items, routes and questions; it
never manufactures a decision or closes a batch from counts alone.

## ✅ Closing checks

- every received point appears exactly once and belongs to one Review Item;
- every Review Item has a terminal state with inspectable support;
- every applied change names its owning Page and checked after-version;
- for a review: the reviewed build and the answering build are frozen in their Jobs' `delivery/…/sent/`, and
  every reply paragraph maps back to items (G5);
- every deferred item names its owner, reason and next batch;
- every proposed question is adopted, declined or deferred by a person;
- a person approves the close, with identity and time recorded.

After closure the batch is history; later comments open a new batch.

This variant owns no scripts.
