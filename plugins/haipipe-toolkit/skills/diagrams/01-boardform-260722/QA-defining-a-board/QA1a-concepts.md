# The words this family uses
state: 🟡 PARTIAL · collected 260729; JL has not read it as a glossary
owner: JL
method: one entry per concept, each the source documents' own word; a coined word is a defect

## Question
What do the family's words mean, one entry each, so no page has to re-explain them?
"Board" names five things, "page" three, "section" two, and until 260729 nothing separated them; this face is the one place the vocabulary is pinned.
Every entry is a word the skill or a face already uses; anything coined here would violate the writing rule it exists to serve.

## Boundary
- ✅ Covered here
  The family vocabulary, one entry per concept, with where each word is defined.
- ↪ Covered elsewhere
  Where things LIVE: `QA1`. This board's own structure: `QA0`. A single page's internal glossary stays that page's `## Glossary`.

## Content
### 1 · The five things "board" names
The FAMILY that ships: `skills/board/` (one skill + one agent).
The SKILL you invoke: `/haipipe-board`.
One topic's FOLDER: `01-boardform-260722/`.
The SOURCE index: `board.md` (spine · close · Topic · Pipeline · Pages · Links).
The GENERATED page: `board.html`, never hand-edited.

### 2 · The page family
page / face: one `Q*.md` or `S*.md`; Q is a decision (closes when its checkboxes close), S is a lifecycle stage (closes at its human gate); one layout serves both.
section: a `##` heading inside a page; the on-stage order is fixed (`QAa0`), and the renderer knows sections only through `ALIAS` (`src/common.py`).
group: a `###` heading in `## Pages`, one folder per group (`QA1`); the id letter records the group a page was OPENED under, not where it is listed today (260729).
state: the first emoji of the `state:` line (🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD); the suffix is human-readable and never a fifth state.

### 3 · The sentence family
sentence: the atomic row, one per source line (`QAb0`).
apparatus / lane: a typed `>` line bound to the sentence above it by adjacency (`QAb1`).
comment: a remark pinned to a selection, living in `## Comments` with a lifecycle (`QA6`).
anchor lost: the pinned quote no longer matches the prose; flagged, never silent.

### 4 · The working vocabulary
decision: what a Q face settles; the word replaced "ruling" on 260729 (JL). A settled decision GRADUATES: its `## Law` is copied into `SKILL.md` (operating rules) or `ref/` (specs), and only then binds.
standing: whether this family may make a given write into a board it renders but does not own; mechanical writes have it, editorial writes do not (`QA1` §4).
spine / close: board.md's one-line purpose and its acceptance condition.
sync / write-back: work done in a round is written back to its owning face the same round; "done" means written back.
managed span: a block between `<!-- haipipe:...start -->` and `end` markers that a script owns (`stage.py`, `skillpage.py`); authors never edit inside.
🧩 Skills: the Where-we-are item listing what a face governs and whether it landed (`QAa5`).

## Items to Finish
- [ ] 🧠 JL reads it once as the glossary and strikes or adds entries
- [ ] 📖 Each entry names its defining face or file, so the glossary never becomes a second source

## Where we are
Collected 260729 from `SKILL.md`, `ref/board-form.md`, and the faces named per entry; nothing here is defined for the first time.

## Files
- `src/common.py`
  `ALIAS`, the machine half of "section".
- `ref/board-form.md`
  The full grammar the words come from.

## Log
260729 · Opened on JL's ask ("what are the concepts we used"), the same round QA1 became the two-folder map
