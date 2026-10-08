---
name: haipipe-paper-comments
description: >-
  The paper's comments PageType: take in what people say about a paper (a review report, an editor's letter,
  a coauthor pass, a meeting, an advisor's notes), split each batch into points with ids by source, group
  them into named Review Items, route each item to its owner, record the reply and its state, and propose
  the Board questions worth answering before anyone asks again. A review batch closes with an approved
  response. Use when taking in comments, triaging them, answering a review, or turning recurring comments
  into questions. Replaces haipipe-paper-round (renamed 2026-10-07).
metadata:
  version: "1.2.0"
  last_updated: "2026-10-07"
  group-token: "CM"
  legacy-group-token: "RD"
  outline:
    mode: fixed
    source: "this SKILL.md"
    surface: "Opening → Outline → Content → Aims"
    shape: "Batch Identity and Intake → Feedback Concern Table → Review Items → Decisions and Response Strategy → Change Routing → Applied and Checked Changes → Response Package → Proposed Questions → Close Receipt and Handoff"
---

# /haipipe-paper-comments · take in what people say, answer every point once

Load `haipipe-page`, `haipipe-page-workflow`, the current Run Workflow/Spec owner, `haipipe-paper-workflow`,
then this PageType and its references. Use the shared Page contract for Page work and `response.<batch>` for a
commissioned response package; triage alone does not allocate a Run. Declare `page-type: comments`. A Page
that still declares `page-type: round` (written before 1.0.0) is a review batch of this PageType, read as is.

This skill replaces `haipipe-paper-round` (JL 261007: "we do not need to keep the round anymore … change it to
the comments"). Everything the Round did carries over: one batch, one concern table, every point exactly once,
routing to the owner, human authority, CHECK before close. What is new: any source, point ids by source,
Review Items, proposed questions, and a batch placed where its subject lives: a batch is a **report of type
comments** in that level's `reports/` (1.1.0; JL 261007: "comments … are a special type of report … it should be
in the reports/ but you can say its type is the Comments").

## 🗂️ Batch kinds and where each lives

One **batch** is one bounded set of comments taken in together. Its kind names its source:

```text
kind      source                         lives in (the ladder)                       shows in
review    reviewers' reports             <answering version>/reports/qNN_<kind>-<MMDD>/   version › Audience Report › Comments
editor    the editor's letter            with its reviews, one batch                 (same)
coauthor  a coauthor's pass on a draft   <the version drafted>/reports/qNN_…/        version › Comments
meeting   what a meeting said            Paper-<Slug>/reports/qNN_…/ (the Board)     Block › Related Questions (proposed)
advisor   an advisor's notes             Paper-<Slug>/reports/qNN_…/ (the Board)     Comments, then proposed questions
internal  a pre-submission audit         <the version>/reports/qNN_…/                version › Comments
(today's desk shelves: B<x>-<desk>-Round/CM<NN>-…/, and Paper-<Slug>/comments/ for a Board batch, still read)
```

A batch about a send (a review, an editor's letter, a coauthor pass on that draft) belongs to that version; a
batch about the Story (a meeting, an advisor) belongs to the Board. Either way it is a report: one folder in that
level's `reports/`, numbered with the other reports (`qNN_<kind>-<MMDD>/`), its face declaring
`page-type: comments`, registered in the face's `## Questions` with group `comments`. A review batch sits in the
version that answers it (the next send, whose face says `responds-to: reports/qNN_<kind>-<MMDD>/…`; the report's own
`answers:` names its Question id, haipipe-report); its Review Items'
work and the response letter (`t32_response`, a letter Task) are in that version too. A batch is never a Task.

## Paper ownership and entry

This skill owns the comments batch Page and its `page-type: comments` contract. A review batch opens on a
feedback batch any time after a build exists, and closes through gate G5: every concern in the table belongs to
one Review Item and is routed exactly once (the Story's §5 support and §6/§7 needs for new evidence, a Story §8
Section Narrative row for retelling, a Section for rework), and a person approves the response receipt. A
meeting, advisor or internal batch closes when every point has a terminal state and its proposed questions are
decided. `haipipe-paper-workflow` holds the full gate assertions; this block only binds the Page owner. The page
itself always runs through `/haipipe-page` and `haipipe-page-workflow` (OUTLINE → … → CHECK), never a private
lifecycle. A batch is a Page-level control surface, not a Run, an Evidence/Execution owner, or a second Story.

## 🔄 Grain and boundary

Create one batch Page for one bounded set of comments against one named subject: a paper build for a review,
coauthor or internal batch; the Story for a meeting or advisor batch.

```text
a subject (a build, or the Story) + received comments
                  ↓
        one batch Page: its concern table and Review Items
                  ↓ routes work to
      Story §5–§8 content · Sections · their evidence/workbenches · proposed Board questions
                  ↓ returns checked versions to
       replies (+ for a review: response package, revised build, close receipt)
```

Do not create one batch per reviewer, comment, or changed Section. Keep every atomic concern addressable inside
the same concern table. Open a new batch when a new decision or set of comments arrives after closure.

A **comments batch** is the persistent cycle defined here. A **Page controller round** is the numeric reopening
counter in a controller receipt. A writing **Version** is an append-only episode inside one fixed-goal Page
writing Run. Never use one term or counter as the other. A Run can support work requested by a batch, but a
batch id never supplies a Run number.

## 🪪 Required identity block

Record the batch identity before triage:

```text
batch-id          stable id, unique across this paper (`CM<NN>`; a legacy batch keeps `RD<NN>`)
page-id           full Page stem (`CM<NN>-<desk|story>-<kind>-<YYYYMMDD>`)
kind              review · editor · coauthor · meeting · advisor · internal ·
                  foreign-desk (a review of this work's telling at a desk with no §8 rows on this board)
about             the base build (exact manuscript/PDF/version) for a send, or the Story and its version
venue-page        selected Venue Page and version, or explicit none
story             governing Story page, its §8 target, and version
received-from     editor, reviewer labels, coauthor, meeting attendees, advisor, or internal authority
received-at       date and source location
answered-by       the version that answers it (a review), or explicit none
response-due      date, explicit none, or unknown
```

A review batch BEGINS with a delivery and ENDS with one: the version you sent that drew the comments, and the
version you released with every concern answered. Both are frozen inside the batch folder, beside what came back:

```text
Paper-<Slug>/
└── j0N_v<MMDD>_<desk>/reports/                the answering version's reports (today: B<x>-<desk>-Round/)
    └── qNN_<kind>-<MMDD>/                     (today: CM<NN>-<desk>-<kind>-<YYYYMMDD>/)
        ├── qNN_<kind>-<MMDD>.md               the batch Page: page-type: comments
        ├── sent/             (review) immutable copy of every declared submission output,
        │                     plus build-manifest.json and display-register.md
        ├── feedback/         immutable received letters, memos, notes and marked-up files
        ├── released/         (review) immutable answering build with the same manifest set
        ├── response/         (external review) approved response letter/table and its manifest
        └── draft/            Page Context/Outline/Evidence/Log projections

Paper-<Slug>/reports/qNN_<meeting|advisor>-<MMDD>/   a Board-level batch: feedback/ + draft/
                                                       (today: Paper-<Slug>/comments/CM<NN>-story-…/)
```

`sent/` and `released/` contain the exact output set declared by the paper-root `delivery/paper-build.toml`. If
a paper declares an online supplement, its PDF and DOCX belong in both snapshots; do not freeze only the main
manuscript. The batch Page records each snapshot's relative path, its `build-manifest.json` `built` time, and
creation event (no content hash). A missing declared output is a failed freeze, not a silently partial batch.

`response/` is not another manuscript source or evidence lane. It is the immutable upload-facing response
package, cut only after the response content has human approval; its manifest records the response paragraphs
and the Review Items they answer. A batch with no external reader records `no external response required`.

The next review batch normally starts by copying this batch's `released/` into its `sent/`. If an intervening
rebuild changes the manuscript, that new build is the next batch's base and its different `built` time is
recorded explicitly; never silently reuse an older snapshot. Root `delivery/` stays the factory; `sent/` and
`released/` are copies cut from it, never edited. Store supplied letters, memos and meeting notes in `feedback/`
and preserve their wording; never rewrite received material into a cleaner second source.

### 🪪 Naming law

```text
j02_v<MMDD>_<desk>/reports/q01_review-1020/      a review batch, in the version that answers it
reports/q07_meeting-1022/                         a meeting about the telling, at the Board
Bc-<desk>-Round/CM03-<desk>-review-<YYYYMMDD>/   older shelves (legacy, read as is), RD<NN>-… too
```

- On the ladder a batch is a report, `reports/qNN_<kind>-<MMDD>/`, numbered after the level's other reports
  and typed by its face (`page-type: comments`); never a Task, so never `t3N_` (that band is letters: t31 cover
  letter, t32 response). Its `batch-id` stays `CM<NN>` (a legacy batch keeps `RD<NN>`) inside the Page. On older desk shelves it
  keeps `CM<NN>-…`. `haipipe-paper/scripts/carry_over/rename_tasks.py` moves an old `RD<NN>-…` batch into `reports/`.
- `CM<NN>` is unique across the paper. Existing `RD<NN>-…` Pages keep their names: Runs, receipts and Story
  rows cite them. Do not shorten `CM` to `C` (a claim id) or reuse `RD` for a new batch.
- The Page stem is `CM<NN>-<desk|story>-<kind>-<YYYYMMDD>`, with ASCII lowercase letters, digits and single
  hyphens in `<kind>`; keep it stable after intake.
- A Run may record a relation to a batch as `round: <batch-id>` (the key keeps its name); the relation does not
  move evidence into the Paper Board or mint a new Run.

At intake of a review, record the frozen base build (snapshot path and manifest `built` time); mark the
answering build `pending` until it exists. Both exact builds are required for closure. The root `delivery/`
remains the mutable factory, while all snapshots are immutable.

## 🧭 Page surface and control loop

Batch content follows the shared Page surface exactly; the Outline is a generated Page projection:

```text
## Opening   identity, subject, intake, and boundary
generated Outline   plan table: item · route · owner · state · checked version
## Content   the roles below, in order
## Aims      human decisions, open actions, and the close test
```

The generated Outline is a projection of the current plan, not a second concern table. Do not author
`## Outline`, `## States`, `## Files`, `## Discussion`, or `## Log` on the Page; those records belong under
`draft/` and are linked from the Page. The shared Page controller Steps give the batch this route; they do not
create a private lifecycle or extra Runs:

```text
CONTEXT  freeze identity + inventory sent/feedback
OUTLINE  atomize concerns + group them into Review Items + propose routes (no silent disposition)
EVIDENCE record only the bounded support needed to answer or verify an item
CONTENT  record human decisions, owning-page returns, replies and proposed questions
CHECK    verify coverage, snapshot builds, reply trace, deferred handoffs, approval
```

## ✉️ A submission batch carries the cover letter

A batch that begins with a submission (`CM<NN>-<desk>-submission-<YYYYMMDD>`, kind `editor`) holds the cover
letter's words in a `### Cover letter` division of its Content, drafted in `draft/` and adopted after the
person's approval like any page. `run-delivery-coverletter` (haipipe-paper-assemble) fills the facts, renders
PDF and DOCX into `delivery/cover-letter/`, and `build.py send <batch-id>` freezes the letter with the manuscript
into `sent/`. The letter never repeats a number the manuscript does not print, and never states a fact the venue
page or paper-build.toml does not hold.

## 📐 Required Content roles

Keep all roles inspectable. Combine divisions only when their addresses remain unambiguous. A meeting, advisor or
internal batch records `none` in the roles that need a build or an external reader.

```text
1  Batch Identity and Intake
   identity block · what was sent (`sent/`) · what came back (`feedback/`) · scope · due date
2  Feedback Concern Table
   one row per atomic point; every received point appears exactly once
3  Review Items
   one row per item: the points it cites, where it lands, the work, the reply, the state
4  Decisions and Response Strategy
   accept · narrow · answer · decline · defer, with human authority and reason
5  Change Routing
   affected claim · Story §8 row · Section · evidence/workbench need · owner
6  Applied and Checked Changes
   what changed · owning Page · before/after version · CHECK result
7  Response Package
   point-by-point reply, editor note, tracked-change/diff pointers, commitments
8  Proposed Questions
   the points any reader would raise again, proposed as Board questions, and each one's decision
9  Close Receipt and Handoff
   totals · the released build (review) · response artifact or explicit no-response record ·
   deferred items · next batch · approved-by · approved-at · approval record
```

## 📋 Concern table contract

Atomize bundled comments before routing them. Give every point one stable id by its source, and these fields:

```text
R<n>.<k> reviewer n, point k   E<n>.<k> editor   A<n>.<k> coauthor   M<n>.<k> meeting   V<n>.<k> advisor
```

The local severity is judged against the paper's claims, evidence, reader interpretation, and delivery.
Preserve a reviewer's original severity label verbatim when supplied; record the local mapping separately.

| Local severity | Anchor | Required response route |
|---|---|---|
| `blocking` | Could make a claim, result, citation, ethics disclosure, or released artifact incorrect or materially misleading; closure cannot proceed on the current package. | Route to the evidence/artifact owner or human disposition; close only after checked repair, justified answer, or explicit deferral that keeps the blocker open. |
| `material` | Could change how a reader interprets a claim or its support, but does not by itself establish that the released package is false. | Require a point-specific answer and checked change or reasoned disposition before the batch is answered. |
| `editorial` | Local wording, formatting, or presentation issue with no effect on claim meaning, evidence, or reproducibility. | May be batched; record the response or explicit human deferral. |

When evidence does not support a stable mapping, use `unresolved` as a triage state, preserve the wording and
evidence, and name the human resolver. Do not force a severity merely to complete the table.

```text
item-id           the point id by source (R1.3 · E1.2 · A1.1 · M2.3 · V1.1)
source actor and source anchor
verbatim quote or faithful pointer
issue kind · severity as supplied · local severity or unresolved
exact concern
affected claim ids
affected Story Section Narrative row and version
affected Section or appendix Page
required evidence/citation/value/display work
human disposition and rationale
owning Page and owner
response strategy and response paragraph id
support/result relation (`round: <batch-id>` plus the full owner-native id)
state
before version and checked after version
open blocker or explicit deferred handoff
review item       the Review-<slug> that answers it (below)
```

Use `open`, `routed`, `applied`, `answered`, `declined`, or `deferred` as states. `open` and `routed` are
non-terminal. `applied` means a changed owning Page has passed CHECK and is waiting for the response trace; it is
not terminal for an external review. `answered` is the terminal state for a checked change or for a justified
answer requiring no manuscript change. `declined` requires a human rationale, and `deferred` requires a named
owner, reason, and next-batch handoff. Never use a blank state and never drop a concern because it causes no
manuscript change.

## 🧾 Review Items

Points are what people said; a **Review Item** is what gets answered. One item is one concern, named and
numbered, and it may gather the same point from several people (JL 261007). Keep them in a `## Review Items`
table in the batch Page, beside the concern table:

```text
## Review Items
| item                | cites              | lands on                        | work                    | reply | state    |
|---------------------|--------------------|---------------------------------|-------------------------|-------|----------|
| Review-causal-claim | R1.1 · R1.3 · E1.2 | t04_results ¶2 · C2             | run-revise-causal-claim | P3    | answered |
```

- **item**: `Review-<slug>`, unique in the batch; the row order is its number on screen.
- **cites**: the point ids it answers, joined by " · ". Each point belongs to exactly one item, and its concern
  row names it in `review item`.
- **lands on**: the owning Page stem (+ ¶N), then any claim ids. A Section's tab lists the items whose
  `lands on` starts with its stem.
- **work**: the owner-native Run that answers it (`run-revise-<slug>` on a Section, `<task> › rNN` for a new
  analysis), or `declined`.
- **reply**: the paragraph id in the Response Package (role 7).
- **state**: the states above; an item is `answered` only when every point it cites is.

The workbench reads this table as written: a version's Audience Report › Comments shows one row per item
(Review Item │ Work │ Report), and each Section's Comments view shows the items that land on it.

## 🔀 Route work; do not absorb it

Keep authority with the artifact being changed:

| Item is about | Owning destination |
|---|---|
| evidence the paper does not yet hold (new analysis class, ablation, downstream outcome) | the Story's §5 evidence proposition plus the corresponding §6 Discovery or §7 Task need |
| contribution, claim role, or paper order | the Story's §8 Section Narrative row (and its compile-order block) |
| section argument, wording, placement, or limitation | owning Section Page |
| missing analysis or factual support | consuming Page's typed Evidence Item; a new study need also changes Story §7 |
| citation request | consuming Page's CITE Evidence Item and verified source set |
| number correction | consuming Page's VALUE Evidence Item and accepted local Result |
| table or figure change | consuming Page's DISPLAY Evidence Item and accepted `results/<re-run>/payload/<unit>/` |
| a question every reader would ask | a proposed Board question (below) |
| response wording and coverage | this batch Page |

For a `foreign-desk` batch, the received desk is named in the identity and the route still lands first on the
governing Story. A request about the telling becomes a human-approved §8 candidate row; it does not create a
foreign Section or let the batch write a second manuscript.

**Where a routed item LANDS on its owner**: the owning page's `draft/records/<stem>-feedback.md` (a section per
batch), a register the page projects from this table during its own OUTLINE pass (`haipipe-page-structure` ⓪
COLLECT). This page never writes into another page's folder, and it never dispatches an agent at its targets:
it DECLARES reopenings. `cli/feedback.py collect --all <board>` lands every register in one process with no
agent at all, and `cli/feedback.py reopen <board>` lists which pages hold an open row, in the order this table's
own gates impose (a Section whose concern also routes to the Story waits on the Story). Dispatch each affected
Page through the shared Page authority test. Wording feedback on a matching open Page writing Run resumes its
next Writing Step; it does not rerun OUTLINE. A changed plan uses OUTLINE/SHAPE and its required human decision.
`applied` here needs that register's `landed:` version first, and G5 runs `feedback-coverage` board-wide before
a review batch may close.

**Routed exactly once** means one concern row and one route decision, not that a concern can name only one
affected artifact. A single route may name a primary owning Page plus a required Story §5/§6/§7 or §8 update;
those linked destinations remain one coordinated route under the same item. Do not clone a concern into a second
row or create duplicate work items. The batch records routes and checked returns; it never becomes a second home
for revised section prose, research values, citations, or paper displays. A concern may say `applied` only after
the owning Page names a checked version; "edited" or "agent finished" is not proof.

## ❓ Proposed questions

A point any reader would raise again is worth answering once for everyone. After routing, propose it as a Board
question in Block › Audience Report › Related Questions, in its group (reviewer · coauthor · editor · reader),
citing the points it came from:

```text
RV1  Is the effect causal, or selection?   ← cites R1.1 · M2.3   → reports/qNN_<topic>/
```

The batch proposes; a person adopts, declines or defers each one, and an adopted question is added through
`haipipe-question` (Ask a Question). A meeting or advisor batch often ends here: its points become questions
rather than Section changes.

## 🃏 Evidence and delivery boundary

The batch does not own an Evidence/Execution lane. Its Context and concern table may point to an accepted Result,
a source path, or a checked Page version, but it does not create new evidence/execution Runs or typed evidence
items during triage. A separately commissioned response session follows `response.<batch>`; ordinary Page
writing keeps its native Page Run contract. If an item needs substantive new evidence, route it to the Story's §5
support and §6/§7 need, then let the external Discovery/Task/Run owner return the result. If a Section needs a
local CITE/VALUE/DISPLAY item, the consuming Section owns that item and its Page workflow. Comments are stored in
`feedback/`, not converted into a new evidence authority.

The assembler owns complete-manuscript artifacts; the Page Delivery workbench owns individual Page exports. The
assembler's `send` action freezes the identified base build into `sent/` under the existing human authorization.
For closure, first check the concern table, Review Items, response and candidate answering build; this
preliminary review does not close the batch. After the person approves that response/build and authorizes
closure, freeze it into `released/`, record its snapshot path and manifest `built` time, then perform the final
CHECK/G5 closure against both frozen snapshots. Reuse the recorded approval if those exact artifacts are
unchanged; a changed response/build needs a new matching decision. The batch records paths and build times and
never edits generated manuscript prose.

## ✍️ Response contract

For an external review, make every response item traceable:

```text
point id → Review Item → disposition → checked change/evidence → response paragraph
```

Distinguish completed changes from commitments. Do not claim a revision is complete until its owning Page has
passed CHECK and the revised build contains that version. A batch with no external reader records
`no external response required` in role 7 and the close receipt; the item-by-item decision record still remains.

## ✋ Human authority

Reserve these acts for a person:

- approve consequential accept, narrow, decline, or defer decisions;
- adopt, decline or defer each proposed question;
- approve the final response package;
- approve the batch's closure.

A machine may propose points, Review Items, dispositions, routes and questions, route accepted work, and close an
already answered Decision Now row with the human's words. It may not manufacture a decision or mark the batch
closed from counts alone. Gate G5 leaves its receipt row under `draft/` and a linked summary in role 9, stating
the gate, assertion results, snapshot paths, and who approved the response receipt.

## ✅ Closing checks

Close only through CHECK when:

- the identity names one batch and one subject (one base build for a review);
- every received point appears exactly once in the concern table, and belongs to one Review Item;
- every Review Item has a terminal state with inspectable support;
- every applied change names the owning Page and its checked after-version;
- for a review: `sent/` and `released/` each contain the complete declared delivery output set, both snapshot
  paths and `built` times are recorded, and every external response paragraph maps back to Review Items;
- the revised paper build and external response artifact, when required, are regenerated and recorded; a batch
  with no external reader records the explicit no-response decision;
- every proposed question is adopted, declined or deferred by a person;
- every deferred item names a reason, owner, and next-batch handoff;
- a person approves the response and close receipt, with identity, timestamp, and approval record recorded.

After closure, treat the batch as a historical record. Later comments open a new batch Page; they do not rewrite
the closed one.

It owns one script, `scripts/review_items.py` (b16 Q05), the runner of its three run cards (`Job › Audience
Report`, view comments): `add` files a batch as a comments report in the version that answers it (Add comments),
`route` sets one Review Item's `lands on`, `work` and state (Route an item), and `reply` sets its `reply` and state
(Reply to an item). Each keeps the old text with a record (`.paper-version-N.yaml`) so `rollback` restores it, and
none writes into another Page's folder: a route prints the `feedback.py collect` and `page.py open-run` commands
that land it.
