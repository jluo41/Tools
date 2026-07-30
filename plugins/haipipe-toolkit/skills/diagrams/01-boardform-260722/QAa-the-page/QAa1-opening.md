# Page Opening: the head and the door
state: 🟡 PARTIAL · rules settled on QAa0, carved 260729; face awaits JL
owner: CC
method: the lead is the door; everything behind it is one flat drawer

## Question
What belongs in a page's head and Opening, what stays on stage, and what one click on the lead reveals?
The head is three lines (`state:` · `owner:` · `method:`) plus the title; Opening is the question lead, always on stage, with Boundary and the S-only orientation folded behind it.
The rules were settled on the former QA4 and moved here verbatim, so this face owns them going forward: any new decision about the head, the lead, the drawer, or Boundary lands here, not on `QAa0`.

## Boundary
- ✅ Covered here
  The three head fields, the title, the question lead as the door, the flat drawer behind it (Boundary · Why this matters · Stage Record · Stage Contract), and their typography.
- ↪ Covered elsewhere
  The fixed on-stage order the Opening sits first in: `QAa0`.
  The source side is §5 and §6 below.
  The managed Stage Contract mechanics (`stage.py`, requires/style-from): `QAa0`'s Law and `ref/board-form.md`.

## Diagram

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAa1

## Content
### 1 · What Opening must do
Opening answers "What am I looking at, and why should I care?" before asking the reader to absorb detail.
The 🧭 Opening heading never folds and the question lead never folds: both are always on stage, and the lead is the door (JL 260725).
Clicking the lead opens everything that explains it, in a fixed order: Boundary first, Why this matters directly below it (Q and S alike, JL 260729), and on an S page an optional Stage Record and the Stage Contract after them.
The fold belongs on the sentence rather than on the section name, because a collapsed row reading only "🧭 Opening" announces nothing: a reader cannot tell that the decision's scope is inside it, which is the fold-works-and-is-invisible failure the 260724 item Law already forbids.
A long question sentence with a caret beside it does announce itself, and it is the thing a reader wants explained, so the sentence is the honest handle.
Behind that one click everything is flat (JL 260725: "I don't want to have >"): Boundary always rendered as a plain heading plus its rows, and Why this matters, Stage Record, and the Stage Contract's Required Inputs, Writing Style, and venue section now render the same way instead of each sitting behind its own ▸.
The version that kept them as nested disclosures read as though the material were missing, because opening the lead revealed a list of shut doors rather than the orientation itself; one door is a disclosure, two doors in a row is a search.
Those seven headings also carry no icons (JL 260725): two of them had one and five did not, and a list where some entries are decorated reads as though the decorated ones were a different kind of thing.
Plain words are the consistent choice here because the drawer is one flat list of orientation, not a set of sections a reader navigates between.
The drawer is typeset as Content, not as chrome (JL 260725): its headings take Content's subsection size and weight with a rule between blocks, and its prose takes Content's size, colour, and leading.
It had been set in small accent-blue capitals over 12.5px muted grey, which is the page's metadata voice, and that voice was telling the reader this material was incidental when the venue contract and the required inputs are among the most consequential things on an S page.
The lead question is bold, which is what separates it from that prose: it is the one sentence always on stage and the handle for the drawer, so it should not read as the first line of what it opens.
Opening prose carries no attribution parentheticals (JL 260729, in chat): a "(JL 260729)" belongs in the Log, and the orientation sentences stay clean.
A reader should be able to state the page's purpose and scope after reading Opening alone.
Under the base/variant model on `QAa0`, Opening is frame: a page kind may contribute rows INTO the drawer, which is what Stage Record and Stage Contract are, and no kind may change the door, the flat drawer, or its typography.

### 2 · Boundary
Boundary says both what this page decides and where adjacent concerns belong.
Its `↪ Covered elsewhere` half must name the owning Q or S, because an exclusion without a destination leaves the reader stranded.

### 3 · Stage Contract (S only)
Stage Contract is part of Opening: one collapsed disclosure after Why this matters and Stage Record, never its own page section (JL 260725).
It tells the reader which upstream outputs this stage requires and which writing contract governs it before showing the stage's own substance.
The managed block is generated from explicit `requires` and `style-from` metadata; it links and summarizes acceptance conditions without copying upstream Content.

### 4 · Why this matters sits in the drawer, below Boundary
The rationale paragraph explains the lead, so it belongs behind the lead: clicking the question opens Boundary and Why this matters together, on Q exactly as on S (JL 260729).
The drawer's order is fixed, and JL confirmed the position in chat the same day, "just below the Boundary": Boundary first, Why this matters directly below it, then the S-only Stage Record and Stage Contract, which is the sequence the renderer assembles.
Until 260729 a Q page's rationale rendered as Content's first subsection instead; Content now holds only what the author explicitly wrote, which is `QAa3`'s flexibility decision seen from this side.
Implemented in `src/page_question.py` the same day; `check.py`'s template coverage asserts the drawer row, and `ref/board-form.md`, `ref/q-template.md`, and `SKILL.md` say the new placement.

### 5 · The source: Question plus optional Boundary
Write `## Question` as one actual question lead followed by one rationale paragraph.
The lead renders in Opening.
The rationale becomes the Why this matters row inside Opening's drawer, directly below Boundary, on Q and S alike (JL 260729).
An optional `## Boundary` joins the same Opening and redirects excluded concerns to their owning Q or S.

### 6 · The source: Stage Contract
S pages use `stage.py new` or `stage.py sync` to generate the managed part of `## Stage Contract` from explicit `requires` and `style-from` metadata.
The managed markers protect authored Content; an author-owned `### Provides` after the markers states the compact output inherited downstream.
Anything else hand-written also belongs after the markers, which is where a manuscript page's venue contract lives: `replace_managed` rewrites only the marked span, so an authored subsection survives every sync (verified across the MISQ pages on 260725).
The whole section renders as one collapsed row inside Opening, so it is a source section without being a page section.
Q pages delete this section and the S-only metadata.

### 7 · A page map in the drawer
JL asked on 260729 for Opening to also show an ascii diagram of THIS page's structure.
The design that fits the frame: one more drawer row, `Page map`, GENERATED at build time from the already-parsed page, never authored.
The renderer holds every section and every Content division at render time, so the map is a projection exactly like the ▧/✏️ split: the source gains nothing, and a computed map cannot go stale, where an authored one would rot on every edit.
It belongs to Opening rather than to Diagram because `## Diagram` owes the SUBJECT's figure and this map is about the PAGE, which is Opening's orientation job.
One sketch of the row's figure:

```
🧭 Opening        the lead, and this drawer
🖼 Diagram        1 figure · 1 canvas
📚 Content        4 divisions: §1 the base and its variants · §2 the template · …
🎯 Items          3 open / 17 done
📍 Where we are   4 dated entries
📎 Files          12 rows
```

The row sits last in the drawer, after the kind's own rows, so the reader meets the question's orientation before the page's anatomy.

## Items to Finish
- [x] 🧭 Why this matters renders in Opening for Q and S alike
      JL 260729, implemented and verified the same round: the renderer branch is gone, the checker asserts the drawer row, and the three spec files say the new placement.
- [ ] 🗺 The generated Page map row ships
      JL asked 260729; the design is §7: a drawer row rendered by `page_question.py` from the parsed page, sections plus Content divisions plus counts.
      Ships on this board first, and the shape is JL's to confirm before it graduates to the spec.
- [ ] 🧠 JL confirms this face owns Opening
      Carved 260729 from QA4 §1 with the text verbatim; the history and its ticked items stay on `QAa0`.

## Where we are
The rules are settled and shipped (see `QAa0`'s history); this face was carved 260729 and owns any future Opening decision.

## Files
- `src/page_question.py`
  Renders the head, the lead-as-door summary, and the flat drawer.
- `ref/board-form.md`
  §8 carries the graduated on-stage spec this face's rules live in.
- `ref/q-template.md`
  The guide text a new page copies for its head and `## Question`.

## Log
260729 · Opening writing rule added on JL's ask: no attribution parentheticals in Opening sentences, dates live in the Log; the QAa faces' Question and Boundary prose swept clean the same round
260729 · §7 added (JL in chat: Opening should also show an ascii of this page's structure): designed as a generated Page map drawer row, a projection of the parsed page, never authored; build is an open item
260729 · Drawer order pinned (JL: Why this matters "just below the Boundary"): Boundary -> Why this matters -> Stage Record -> Stage Contract, which is the order the renderer already assembles; the two sentences here still describing the pre-260729 placement (§1, §5) repaired the same round
260729 · Marked frame under the base/variant model on QAa0: a kind contributes drawer rows, never mechanics
260729 · Why this matters moved into Opening's drawer for Q pages too (JL: "move it to QAa1"); renderer, checker and specs updated the same round
260729 · Opened by carving QA4 §1 (Opening) out to its own face, text verbatim; QA4 renamed QAa0 the same round
