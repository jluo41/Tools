# Page Files: Engines, Input files, Output files
state: 🟡 PARTIAL · the taxonomy is ruled; the placement rule and the row grammar are open
owner: JL
method: one shared trio, and a placement test that answers which group a file goes in
session: 797ebed2-5d87-4fa3-aac2-44f35ad9e8f2

## Question
How does a Page's `## Files` actually organize the files that Page needs, and which group does a given file go in?

JL ruled on 260731 that one shared taxonomy is fine: `Engines`, `Input files`, `Output files` is the standard shape rather than an example set each Page has to justify.
That turns the open question around, because it was written as "how do we avoid forcing every Page into one taxonomy" and the taxonomy turns out to be the answer, not the risk.
What is left is the part that was never written: how a Page decides which of the three a file belongs to, and what to do with the files that look like two of them at once.
The trio is the same Input, Process, Output shape the toolkit's own basic unit uses, so a reader who has read one board's Files section can read every other one without learning a second vocabulary.


## Boundary
- ✅ Covered here
  The purpose of Files, when subsections are useful, contextual subsection names, generated-file warnings, and heading-level Copy and Chat paths.
- ↪ Covered elsewhere
  The fixed Page order is `QB4`; the general subsection renderer and paragraph grammar are `QB4c`; generated heading paths and Chat focus are `QB5d`.

## Diagram

```
 ## Files  ·  HOW A PAGE ORGANIZES THE FILES IT NEEDS
 ═══════════════════════════════════════════════════════════════════

 THE STANDARD TRIO · one shared taxonomy, ruled OK by JL 260731
 ───────────────────────────────────────────────────────────────────
   Engines        what RUNS this page's subject
                  you open one to CHANGE behaviour
   Input files    what the work READS
                  specs, templates, source pages, evidence
   Output files   what the work WRITES
                  generated; you open one to CHECK, never to edit

 THE PLACEMENT TEST · ask what YOU do to the file, not what it is
 ───────────────────────────────────────────────────────────────────
   I edit it to change behaviour   ──▶   Engines
   I read it, or an engine does    ──▶   Input files
   a build wrote it                ──▶   Output files

   it fits two?  the ACTION wins over the dataflow, because Files is
   ordered by what you open FIRST rather than by how the data moves

 WHAT STAYS FREE · rename a group when the trio genuinely misfits
 ───────────────────────────────────────────────────────────────────
   QB2:   Board source   ──▶   Index renderer   ──▶   Generated view
   that is the exception now, not the rule; an empty group is omitted
```

```
example for QB2, the Board-Webpage design page

📎 Files
├── Board source
│   └── board.md                  the accepted Index structure
├── Index renderer
│   ├── src/page_board.py         builds the top view
│   └── assets/board.css          shared visual language
└── Generated view
    └── board.html                generated · never hand-edit

QB2 / Files / Index renderer                 [⧉ Copy] [🤖 Chat]
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAa7

## Content
### 1 · What Files conveys
```
📎 Files · answers: which few files do I open to continue this work?
──────────────────────────────────────────────────────────────
conveys   the action map: entry points, never an exhaustive change list
holds     the standard trio: Engines, what runs the subject · Input files,
          what the work reads · Output files, what a build writes
source    one backticked path + its role in one sentence, per row ·
          a generated file says so in its row: never hand-edit
rules     place a file by what YOU do to it, not by what it is · rename a
          group only when the trio truly misfits · omit an empty group ·
          three rows or fewer stay flat
omit      allowed but strongly advised against: a page with no Files
          leaves the next person searching
```
Files answers one question: which files does the next person open to continue THIS page?
It is an action map, so a short list of real entry points beats an exhaustive record of everything the work touched.
Every row names one path in backticks and explains its role in one sentence, because a bare path says where to click and never why.
Mark generated artifacts in the row itself, such as `generated · never hand-edit`, so nobody edits the layer the next build overwrites.
Paths declared in `board.md`'s `## Links` render clickable, which is what makes the map usable rather than merely correct.

### 2 · The three groups, and what each one holds
```
🗂 the standard trio · one shared taxonomy (JL 260731: "that should be ok")
──────────────────────────────────────────────────────────────
  Engines        what RUNS this page's subject
                 open one to CHANGE behaviour
  Input files    what the work READS
                 specs, templates, source pages, evidence
  Output files   what the work WRITES
                 generated; open one to CHECK, never to edit

  the same Input · Process · Output shape the toolkit's units use,
  ordered by what you open FIRST rather than by how the data flows
```
#### One shared trio, and why sharing it is the point
(the 260731 ruling, which reversed this page's opening premise)
`Engines`, `Input files`, and `Output files` is the standard shape for a Page's Files section, and a Page reusing it verbatim needs no justification.
This page opened on the opposite assumption, that a shared taxonomy would flatten every Page into one mould, and the assumption was wrong in the direction that matters: a reader meets Files on fifty pages, and a vocabulary they already know costs them nothing to read.
The trio is not an arbitrary three either, because it is Input, Process, Output, which is the shape every haipipe unit already runs on, so Files is that shape applied to one Page's file map.
It also matches the Board Map's own lanes, engine on the left and folder on the right, so the two views of a Page speak one language.

#### What each group actually holds
(so a row lands in the right group without a second reading)
`Engines` are the files that RUN this Page's subject: the renderer, the checker, the script, the stylesheet, whatever you edit when the behaviour must change.
`Input files` are what the work READS: the spec that governs it, the template an author copies, the source Page, the sibling Page kept as a worked example, the evidence.
`Output files` are what the work WRITES: generated artifacts you open to check the result and never to edit, which is why each one carries its own do-not-hand-edit warning.
Order is Engines first because Files is ordered by what a reader opens first, not by how data flows through the build; the dataflow order would put Input first and answer a question nobody asked at this point on the Page.

#### Renaming a group is the exception, not the rule
(the freedom that survives the ruling, narrowed to where it earns its keep)
A Page whose work genuinely has different coherent parts still names its own, such as `Board source`, `Index renderer`, and `Generated view` on `QB2`.
The bar is now higher than it was: reach for a rename when the trio would misdescribe the work, not merely when a truer-sounding word exists.
Omit an empty group rather than leaving a heading with nothing under it, and never invent a row to fill one.
Stay flat with no headings at all when the list is short and coherent, because three or fewer rows about one subject read better as a plain list.

### 3 · Which group does this file go in
```
🧭 the placement test · ask what YOU do to it, not what it IS
──────────────────────────────────────────────────────────────
  I edit it to change behaviour     ──▶  Engines
  I read it, or an engine reads it  ──▶  Input files
  a build wrote it                  ──▶  Output files

  it fits two? the ACTION wins:
    this page's own .md   a build reads it, but you EDIT it  ─ Input
    ref/q-template.md     governs, and does not run          ─ Input
    check.py              runs, and its rules are code       ─ Engines
    board.html            rewritten on every save            ─ Output
```
The hard part of Files was never the group names, it was that many files honestly fit two groups, and a rule that says "put it where it belongs" decides nothing.
The test is what YOU do to the file when you continue this Page, because Files is an action map and the reader arrives holding an intention rather than a taxonomy.
A spec such as `ref/q-template.md` is read by the work and by every author, and it does not execute, so it is an Input even though changing it changes what gets produced.
`check.py` reads pages and could be argued the same way, and it is an Engine, because the thing you change in it is code and the thing it produces is a verdict.
A generated file is the one unambiguous case, so when a row is generated the group is already decided and the row still says so in its own words.
When two groups remain genuinely equal after the test, put the row where the reader who is about to act would look for it, and say the other role in the role sentence rather than duplicating the row.

### 4 · The source form
```
✏️ what a heading inside ## Files becomes    (source ──▶ page)
──────────────────────────────────────────────────────────────
  a group heading    a subsection holding every row below it
  the next heading   closes the previous group, opens the next
  every heading      a rail outline row, plus Copy and Chat
  ## Files itself    unchanged in the fixed frame, however grouped
  ⚠ rows written under ANOTHER section's heading belong to THAT
     section, which is how QE4's Files section rendered empty
```
Each optional `###` heading groups the file rows that follow it until the next `###`.
It renders as a `.sh` subsection heading inside 📎 Files and appears in the rail's outline, so a reader can jump straight to one group.
The heading receives a generated breadcrumb with Copy and Chat actions, whose path grammar is `QB5d`'s and is the open half of this Page.
The Page-level `## Files` heading stays in the fixed frame whatever its internal organization is, so grouping is a Page's own call and never a change to the Page order (`QB4`).
One trap is real and has already cost a page: rows written under another section's subsection belong to that subsection, which is how `QE4`'s Files section rendered empty.

## Items to Finish
### The taxonomy and the placement rule
- [ ] 🗂 The trio is the standard shape, and it renders as real subsections
      PROPOSED: ruled by JL 260731 ("It is ok to have the same taxonomy, like the Engine, Input, Output, that should be ok") and shipped the same day: `###` inside Files renders as a `.sh` heading, the sidebar outline lists the groups under 📎 Files, and this page's own Files carries the trio as the worked example.
- [ ] 🧭 Settle the placement test for a file that fits two groups
      §3 proposes it: ask what the reader DOES to the file, so a governing spec is an Input and a script whose rules are code is an Engine.
      This closes when the rule is written into `ref/q-template.md`'s Files guide and a sweep finds no row that the rule sends to a different group than the one it sits in.
- [ ] 📐 Settle the row grammar
      Keep paths, roles, and generated-file warnings readable without forcing a table onto small Pages.

### Access and ownership
- [ ] 🧭 Give each subsection a copyable Chat path
      Reuse `QB5d` so the focus packet includes Page, Files, contextual subsection, source path, and visible rows.
- [ ] 🧠 JL confirms Files has its own QAa face

## Where we are
JL ruled the taxonomy on 260731 and it reversed this page's premise: the trio is the standard shape rather than an example set, and a Page reusing it verbatim owes no justification.
The rendering shipped the same day, so `###` groups inside Files render as subsection headings and the rail's 📎 Files row unfolds them.
What is open moved with the ruling: the placement test in §3 is proposed and not yet written into the template, and the row grammar and Chat focus are unchanged.

- 260731 CC · 🖼 The figures were rebuilt, and the renderer was the real defect
  JL, of this page's head figure: "it is very hard to read. Why?"
  The cause was not the drawing: an emoji is not monospace, so a figure whose columns are straight in the `.md` arrives bent on the page, differently per emoji, because `pre` asks for `ui-monospace` and every emoji falls back to the colour-emoji font at its own width.
  `body.pad_emoji` now wraps each emoji at build and `pre .eu` pins it to `2ch`, which is the width the author drew against in a terminal; the markdown is untouched, so the figure still survives being copied out, which is `QB4b` §0's rule.
  The figures on this page were redrawn on top of that: no literal markdown tokens inside the drawing, one hierarchy per figure, and no emoji standing in a column that has to align.
- 260731 CC · 🧹 The trio was swept across the whole board
  The same sweep grouped Files on 23 of 51 pages, most of them under the trio, the rest under truer contextual names where the trio did not fit.
  Pages with three or fewer rows stayed flat, per §2.
  One real defect surfaced on the way: `QE4`'s Files rows had been nested INSIDE its Decision Now subsection, so the section rendered empty; the sweep separated them.

### Decision Now
- [ ] 🧭 Confirm the placement test in §3
      What is true today: the trio is ruled, and nothing says which group a file that fits two belongs to, so the sweep placed 23 pages' rows by judgement.
      A · the ACTION test: what do you DO to this file, so a governing spec is an Input and a script whose rules are code is an Engine.
      B · the DATAFLOW test: what does the build do with it, so anything the build reads is an Input and anything that executes is an Engine.
      → CC recommends A, because Files is an action map and the reader arrives holding an intention; B is also cheaper to check mechanically, which is the one argument for it.
- [ ] 🧠 Confirm Files owns its own face
      Opened 260730; a tick here also closes the same row in Items to Finish.

### Decisions taken
- 260731 JL · 🗂 One shared taxonomy is fine, and the trio is it
  JL: "I think the question here is how to really organize the files related to this Q. It is ok to have the same taxonomy, like the Engine, Input, Output, that should be ok."
  This page had been written the other way round, treating a shared taxonomy as the thing to avoid and contextual naming as the rule, so its own §2 spent its length arguing that the trio was only an example.
  The ruling makes `Engines`, `Input files`, `Output files` the standard shape, moves renaming to the exception, and re-points the open question at the part that was never answered: which group a given file goes in.
  §2 and §3 were rewritten to that shape, and the 🏷 contextual-naming item was replaced by the 🧭 placement-test item, because the question it asked is no longer the live one.

## Files
### Engines
- `../../board/haipipe-board/src/page_question.py`
  `structure_rows()` and the `.sh` rendering path, the renderer half of Files subsections.
- `../../board/haipipe-board/src/body.py`
  `pad_emoji()` and `EMOJI`, which pin a figure's emoji to two cells so its columns land where they were drawn.
- `../../board/haipipe-board/src/page_board.py`
  `board_status()`, whose 📚 cell counts divisions against face diagrams and is how this page's own retrofit was checked.
- `../../board/haipipe-board/assets/css/`
  `.sh`, `pre .eu`, and the rail's outline styles, the visual half.

### Input files
- `../../board/haipipe-board/ref/q-template.md`
  The shared Page source template whose guide text teaches the trio; where the placement test must land.
- `../../board/haipipe-board/ref/board-form.md`
  The Page grammar where the settled Files form belongs.

### Output files
- `board.html`
  The rendered board; this page's Files section is the worked example inside it.

## Discussion
> JL: Files section should also have the subsection as well, like the Engines (what are the related skill content), and the Input Files (what are the input files), and Output Files ( what this board finally rendered)
> CC: Shipped 260731: your trio is the default example set in §2 and the template guide, `###` groups render inside Files, the rail lists them, and this page's own Files demonstrates all three.
> JL: please update this page to follow the requirement. Like the diagram, and the content, there is no diagram in content sections, and also I feel the whole content in this page is hard to read.
> CC: Fixed 260731: every division opens with a face diagram (QB4c's rule, matrix 📚 `4÷·4🖼`), and the head figure was redrawn.
> JL: for this one, it is very hard to read. Why? Could you make it to be like more modern? here which Q we should work and which skill part we should update.
> CC: The cause was the renderer, not the drawing: emoji are not monospace, so the columns bent on the page while being straight in the source. `body.pad_emoji` + `pre .eu` now pin every figure emoji to 2ch, board-wide. The remaining half is taste, and it belongs to `QB2`, which owns the board's visual system and its audit-first protocol.
> JL: I think the question here is how to really organize the files related to this Q. It is ok to have the same taxonomy, like the Engine, Input, Output, that should be ok.
> CC: Recorded as the 260731 ruling: the trio is the standard shape, renaming is the exception, and the live question became which group a file goes in. §2 and §3 carry it, and the placement test is on Decision Now.

## Log
260801 · §1 renamed "What Files conveys" and its face diagram reshaped to the five-row protocol (conveys · holds · source · rules · omit) on JL's ask; master view on QB4 §0
260731 · JL ruled one shared taxonomy: the trio is the STANDARD shape, renaming is the exception, and the live question became placement. Question, §2, §3 rewritten; the 🏷 contextual-naming item replaced by the 🧭 placement test; state 🔴 -> 🟡
260731 · Figures rebuilt after JL called the head figure unreadable: root cause was the renderer (emoji are not monospace), fixed board-wide by body.pad_emoji + pre .eu; this page's figures redrawn with no markdown tokens and no emoji inside an aligning column
260731 · Retrofitted to QB4c's face-diagram rule: every Content division opens with a face diagram (matrix 📚 3÷·0🖼 -> 4÷·4🖼)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · JL's trio recorded as the default example set and the rendering shipped: ### groups inside Files render as .sh subsections, the rail unfolds them, and this page's Files regrouped as the worked example (0.70.0)
260730 · Opened from JL's decision that Files may have optional subsections whose names come from each Page's context
