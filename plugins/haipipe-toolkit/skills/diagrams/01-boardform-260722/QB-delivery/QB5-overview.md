# The sentence: one source line, and everything that attaches to it
state: 🟡 PARTIAL · the unit is settled; the family map is new (260729)
owner: JL
method: one sentence per source line; everything that attaches to a sentence gets its own face

## Opening
What is the smallest unit a board can address, and what attaches to it?
A board writes one sentence per source line, so that line is the anchor a reader clicks.
What attaches is a `>` line written straight under it: a citation, a remark, a record of an edit.
Nothing is stored to link them, so a record belongs to the sentence above it and to nothing else.
This page settles the sentence as that unit and hands each attachment to its own page.

**Where this page sits**: `QB4` takes the whole page and the order its sections keep, and it stops there.
This page is the next rung down the same ladder: Board, Group, Page, Section, Sentence.
The sentence is where a reader's finger actually lands, so it is the last rung and nothing sits below it.

**What "attaches" means here**: a record written on its own line, starting with `>`, directly beneath a sentence.
`> Citation: Smith 2019` is one, and `> Comment JL this number moved · 260802 0110` is another.
The sentence keeps its own words on stage; its records sit under it and stay shut until someone clicks.

**Why it matters**: a claim and its evidence are read together or they are not read at all.
Push the evidence to the bottom of the page and the reader has to work out which sentence it came from.
Give the sentence an id and keep the link somewhere else, and the link rots the first time the prose is rewritten.
Adjacency costs nothing to write and nothing to maintain, which is why the whole family rests on it.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Demonstrate before explaining**: `### 1` is written in the grammar it documents, so a reader meets the sentence by using one.
A rule added to this page has to survive being shown on a live row there, not only described in prose.

**Use the current page ids**: the five faces are `QB5a` through `QB5e`.
The older `QAb0` to `QAb4` and `QA6` still resolve through `board.md`'s alias map, so old lines keep working, but nothing new is written with them.

**Name lanes and badges the way `src/body.py` renders them**: a typed lane is `> Citation:`, a person's remark is `> Comment WHO …`, an edit is `> ✎ …`.
The badge is `💬`, `✎`, or `⚑`, and a wrong glyph here teaches a reader to expect the wrong thing on every other page.

## Diagram

**The sentence and its five faces**: one source line, and the page that rules each thing hanging off it.

```
📄 ONE SOURCE LINE = 🎯 ONE ANCHOR · everything else hangs off it

   ✏️ "The coefficient is 0.42 in the pooled model."      💬 3
        │
        ├── 💬 a person's remark    > Comment JL …         QB5b
        ├── ⚑ a typed lane         > Citation: …          QB5a
        ├── ✎ a change record      > ✎ ~old~ *new*        QB5c
        ├── 🤖 what an agent is told the focus packet       QB5d
        └── 🧹 clean up             filter · archive        QB5e

   🏷 binding   adjacency alone · no id · no sidecar file
   🔒 default   SHUT · one click opens
   🎖 badge     💬 person waiting ▸ ✎ change ▸ ⚑ lane
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAb0

## Content
### 1 · Try it on this row
**The three badges**: one live sentence per badge kind, so the rule can be clicked instead of read.

```
🧪 THREE ROWS · one per badge kind · all shut until clicked

   💬 a person is waiting     > Comment WHO …
   ✎ a change was recorded   > ✎ ~old~ *new* · WHO · time
   ⚑ typed lanes are filed   > Citation: · > Value: · > Display:

🖱 hover      the address · ＋ Comment · 💬 Chat
🖱 dblclick   edit this sentence
📱 touch      ⋯ opens the same three
```
📌 Establishes what a sentence does before the page explains it: click a real row and the family answers.

#### 1.1 · A sentence with typed lanes
(three typed lanes are filed under this sentence, so its badge reads ⚑ 3)
This sentence carries three typed lanes, and none of them is stored anywhere but on the lines below it.
> Citation: `QB5a` rules what may attach to a sentence and how the drawer renders it.
> Value: 3 lanes are attached here, which is the number the badge counts.
> Display: the figure in `## Diagram` draws the same five branches.

#### 1.2 · A sentence a person is waiting on
(one remark is written under this sentence, so its badge reads 💬 1 and outranks any record)
A person's remark is written `> Comment WHO …`, and the badge turns 💬 because someone is owed an answer.
> Comment CC this row exists so the 💬 badge has something real to count · 260802 1400

#### 1.3 · A sentence that was changed
(one change record is written under this sentence, so its badge reads ✎ 1)
An edit replaces the source line and leaves one record of what moved, which is why the old wording is never stored a second time.
> ✎ An edit replaces the source line and leaves one record of ~the change~ *what moved*, which is why the old wording is never stored a second time. · CC · 260802 1400

#### 1.4 · What each gesture does
(one gesture per thing a reader may want, and one page rules each of them)
Click a sentence to open its records: they start shut, and the badge says which kind is under it.
Hover it, or reach it by keyboard, to see its generated address, its `＋` Comment action, and its `💬` Chat action.
Double-click it to edit the source sentence, which is what wrote the `✎` record above.
On touch there is no hover, so `⋯` opens the same Comment, Chat, and Edit actions.
Filtering, resolving, archiving, and restoring these records is designed on `QB5e` and is not built yet.

### 2 · Why adjacency, and not new syntax
**Three ways to link a record to a sentence**: what each costs, and what breaks it.

```
🔗 HOW A RECORD FINDS ITS SENTENCE

  ✅ adjacency          the > line directly under the sentence
     cost              nothing · a line an author could have typed
     breaks when       the line moves without its records

  ❌ an id in the prose  a marker the reader has to look past
     cost              a second thing to keep in step
     breaks when       the prose is rewritten

  ❌ a sidecar file      one more file per page
     cost              two files to edit instead of one
     breaks when       anyone touches the .md by hand

⚖️ the whole family rests on the first row
```
📌 Establishes why nothing new was invented: the files already carried `>` runs under the sentences they discussed.

#### 2.1 · The convention was already there
(the paper unit docs wrote review threads under a sentence long before a board rendered them)
The paper unit docs already write review threads and `> Check:` blocks under the sentence they discuss.
Those files gained the behavior with zero edits the first time their board rebuilt.
That is the test this page keeps: every attached record is one line an author could have typed by hand.

#### 2.2 · Adjacency is a real binding, not a habit
(a lane placed after a paragraph attaches to the last sentence of it, which is not the one it is about)
A `>` line attaches to the sentence above it and to nothing else: no marker, no id, no sidecar file.
The MISQ rollout found the failure this creates.
A lane sat after a paragraph while its own prose said "the sentence above", so it had silently attached to the wrong sentence and had to be moved.
A concern that belongs to the whole page has no sentence to attach to, and it belongs in `## Aims`, or in that Aim's `Plan` when the move is temporary.

#### 2.3 · One lane is one source line
(a wrapped lane becomes its own row on the page and captures every lane below it)
A lane is one source line, however long it runs.
Wrap it and the second half becomes its own sentence row, takes its own badge, and captures every lane written beneath it.
The markdown looks fine and only the rendered page shows the broken row, which is the same one-sentence-per-line rule the prose already obeys.

### 3 · The family, one page each
**Who rules what**: the five faces, and the one thing each of them owns.

```
🗺 FIVE FACES · one question each · QB5 is the front door

  QB5a  evidence card       typed lanes · ⚑ badge · the drawer
  QB5b  comments            > Comment WHO · the write-back
  QB5c  editing             one line replaced · one ✎ record
  QB5d  chat                the address · what an agent is handed
  QB5e  details lifecycle   filter · resolve · archive · restore

🚪 this page   the unit itself, and which face owns which question
```
📌 Establishes the map: every question about a sentence has exactly one owning face, and this page is not it.

#### 3.1 · The card, and what may attach
(QB5a rules the typed lanes and the drawer they open in)
`QB5a` renders the sentence clean and shows its records on click.
It owns the typed lanes: Citation, Value, Display, Check, Q-consumer, Link, Source, and Note.
It also owns the ⚑ badge, the click-to-add form, and the inline-marker chips that a paper board resolves at build time.

#### 3.2 · The remark, and the edit
(QB5b writes what a person says; QB5c replaces the sentence and records the change)
`QB5b` writes one remark directly under the sentence a reader selected, and the form to write is `> Comment WHO …`.
The older `> JL:` form still renders, so nothing already written breaks, and `check.py` warns on it inside Content.
`## Discussion` is a different thing and is untouched: it keeps `> JL:` with `>> CC0726:` replies, because that is a thread with nested answers rather than a note on one sentence.
`QB5c` replaces one plain source line and writes one `> ✎` record beside it, so the old wording is never stored a second time.

#### 3.3 · The address, and the lifecycle
(QB5d hands one location to an agent; QB5e keeps the records from piling up forever)
`QB5d` gives every heading and every Content sentence a generated address, and rules what an agent acting on that location is handed.
`QB5e` rules what happens as records pile up: typed views, record states, previewed cleanup, archive, restore, and purge.
`QB5d`'s addresses are made at render time and stored nowhere, and whether `QB5e` needs a durable key of its own is the one identity question still open.

## Aims
### A1 · 🧪 Try it on this row
- A1.1 · A reader meets the sentence by using one, before the page explains it.
  **Done when:** `### 1` carries one live row per badge kind, and each row's records, address, and chat action can be reached on the rendered page.

### A2 · 🔗 Why adjacency, and not new syntax
- A2.1 · Adjacency stays the only binding between a sentence and its records.
  **Done when:** Every attached record on this board is one line an author could have typed, with no id in the prose and no second file.

### A3 · 🗺 The family, one page each
- A3.1 · Every question about a sentence has exactly one owning face.
  **Done when:** JL confirms the map, and `QB5a` through `QB5e` each name the one attachment they rule.

## States
### Decision Now
- [ ] 🗣 Is the sentence family carved into the right five faces?
      📍 `Part` `### 3 · The family, one page each`
      🔔 `Why now` The faces were carved on 260729 and renamed `QB5a` to `QB5e` on 260731; nobody has confirmed the split since.
      ⭐ `A ·` accept the five as drawn, which fixes where every future sentence rule gets written.
      `B ·` name a face that is missing, or two that should merge, which reopens the ids and every line pointing at them.
      🛑 `Blocks` nothing; all five pages render and are being worked.
      🤖 `If nobody answers` A takes effect, and the map stands as `### 3` states it.

### A1 · 🧪 Try it on this row
- ✅ A1.1 · `### 1` carries three live rows, one per badge kind. All three are shut on the rendered page and each badge names its own kind.

### A2 · 🔗 Why adjacency, and not new syntax
- ✅ A2.1 · Settled and live on every board. `src/body.py` binds a `>` run to the plain sentence above it and reads nothing else.

### A3 · 🗺 The family, one page each
- 🧠 A3.1 · The five faces exist and each names the attachment it rules. The map itself waits on the Decision Now row above.

## Files
### ⚙️ Engines · what RUNS this subject
- `src/body.py`
  RENDER. One sentence per source line, the adjacency walk that folds a `>` run under the sentence above it, and the badge that names which kind is underneath.
- `cli/serve.py`
  WRITE. The routes that add a remark, add a typed lane, or replace one sentence, each anchored on an exact source line.
- `assets/js/40-sentence/00-apparatus.js`
  The controls a reader touches: the generated address, the `＋` Comment row, the `💬` Chat action, and the `⋯` menu on touch.

### 🤝 Hands off · what RULES one question about a sentence
- `QB-delivery/QB5a-evidence-card.md`
  What may attach, the ⚑ badge, and the drawer it opens in.
- `QB-delivery/QB5b-comments.md` · `QB-delivery/QB5c-editing.md`
  Writing a person's remark under a sentence; replacing the sentence and recording the change.
- `QB-delivery/QB5d-agent-visibility.md` · `QB-delivery/QB5e-sentence-details-lifecycle.md`
  The generated address and what an agent is handed; what happens once the records pile up.

### 🧪 Checks · what CATCHES a page breaking a rule
- `cli/check.py`
  Owns `old-comment-form`, which warns when a sentence comment inside Content still uses the bare `> JL:` shape.

## Lesson
- 260801 JL · 🧪 The family's operations now have a run of their own
  JL: "I feel the sentences part is almost crash", after three separate sentence defects reached him in a week.
  `QF5` owns the answer: sixteen shapes a sentence can take, crossed with the six operations that read one, and five assertions per cell.
  Its first tier is written and was red on its first run, which is the only evidence a test is worth keeping.

## Glossary
- ✏️ **sentence**: one source line of prose, and the smallest thing on a board a person can point at, comment on, or edit.
- 📎 **attached record**: a line starting with `>` written directly under a sentence, which belongs to that sentence and to no other.
- ⚑ **typed lane**: an attached record whose first word names its kind, such as `> Citation:` or `> Value:`.
- 🗂 **apparatus**: the technical name for all the records attached beneath one sentence; the panel a reader opens is called Sentence details.
- 🔗 **adjacency**: the rule that position alone binds a record to its sentence, with no id in the prose and no second file.
- 🪞 **face**: a page carrying one part of a subject, whose id is its parent's id plus a letter, as `QB5a` is a face of `QB5`.

## Log
260802 · Rebuilt to the page contract: `Boundary` deleted with its pointers moved into the Opening's More details, `Items to Finish` and `Where we are` became `Aims` and `States` with three groups mirroring Content, Content renumbered `### 1` to `### 3` with a captioned face figure each, `Files` regrouped and its five dead face paths repaired, and a Writing Style plus a Glossary added. The 260801 JL record moved verbatim from the old `Where we are` into `## Lesson`
260802 · Comment and badge wording brought to the 260802 rulings: a person's remark is written `> Comment WHO …` (the bare `> JL:` still renders, and `check.py` warns on it inside Content), attached records start SHUT, and the badge names which kind is under the sentence, `💬` a person waiting over `✎` a change over `⚑` a typed lane. The demonstration was split into one live row per badge kind so all three can be clicked
260802 · Legacy ids `QAb0`-`QAb4` and `QA6` replaced by `QB5` and `QB5a`-`QB5e` throughout the prose and Files; the alias map in `board.md` still resolves the old ones, so nothing already written breaks
260801 · `QF5` opened as the sentence family's test face: the shape matrix, the operation matrix, and the four tiers, with tier 1 running today
260731 1905 · Sentence-tail ⚑N badge no longer strands on its own line: renderer now glues it to the last word inside the `<p>` (`.snw` nowrap wrapper in body.py + board.css), so it sits at the sentence end and wraps together with the last word when space is tight
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Added §1 Demonstration so one sentence exposes Evidence, Comment, Chat, Edit, address, and the QAb4 lifecycle boundary before the reader enters the detailed family map
260729 · Added QAb4 as the independent Sentence details lifecycle face for filters, statuses, cleanup, archive, restore, and purge
260729 · Opened as the sentence family's front door when QAb was carved (JL: QAb0 overview, QAb1 evidence card, QAb2 editing)
