s03 · Delivery: its workbench and its skill
===========================================

New on 261010 (JL: "have a s03 delivery-workbench-skill"); s03 was the Guide's old number, free since it
became s31 (261007). The Studio's twin is s02-studio-workbench-skill.

**Tags:** `Structure` · `UI`

**Stage:** shaping

**Topic:** the Delivery seen from both sides: its workbench (the Delivery view at the right end of the
top row, Studio | Block · Job · Task | Delivery, opened from every level) and its skill
(`/haipipe-delivery`). Jobs and Tasks make outputs; only the Block keeps them, in its one `delivery/`;
each subfolder leads back to the Job or Task folder that made it. A Report stays with each level
(s09-D02); what is handed over lives once, at the Block (s09-D05). On screen (JL 261012: "add the UI for
the expected UI and card UI for showing the results of the delivery, what are the current results"): today's
five Delivery screens, the one screen we expect, and one card per result.

**Feeds:** `reports/` q07_workbench_mapping · q08_workbench_base


Files
-----

```text
s03-delivery-workbench-skill/
├── s03-delivery-workbench-skill.md            this face
├── s03-delivery-workbench-skill.excalidraw    three frames: Background tree, boxes with arrows, the screen
├── s03-delivery-workbench-skill.png           its preview
├── .s03-delivery-workbench-skill.seed.json    generated snapshot for preserving marks
├── build_s03_delivery_workbench_skill.py      the builder; reads frame.py, every delivery/ and this face on each build
└── history/                                   the 261011, 261012 and 261012b builders, faces and previews
```
skill: Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-delivery/
```


Frames
------

The drawing's ① and ② are drawn from this block by `topic_map.draw_topic`'s drawing code (haipipe-studio 0.13.0);
the builder fills the live trees (today's screens, every `delivery/`, the skill's folder) by box id. Frame ③
is drawn by the builder.

```yaml
frames:
- title: "🧭 Background: Delivery, for a newcomer"
  intro: What a Block hands over, the words this topic uses, and where it sits. Frame ② explains each part; frame ③ is the screen.
  cols: 2
  tree:
  - "📤 What Delivery is":
    - "📦 what a Block hands over: a paper PDF, a Word file, a deck, an email draft"
    - "👀 seen from both sides: its workbench (the Delivery view) and its skill (/haipipe-delivery)"
    - '💬 JL 261012: "add the UI for the expected UI and card UI for showing the results of the delivery"'
  - "⚡ In one minute":
    - "🧱 Jobs and Tasks make outputs; only the Block keeps them, in its one delivery/"
    - "🔗 each subfolder leads back to the Job or Task folder that made it: the path is the link"
    - "📝 a Report stays with each level (s09-D02); what is handed over lives once, at the Block (s09-D05)"
    - "🗂️ a send (something that went out) is one row of delivery/delivery.md"
  - "📖 Words it uses":
    - "🧊 Block: one question or one paper; Job: one slot of work in it; Task: one step of a Job"
    - "📦 delivery/: the Block's one folder of built files, under their source address"
    - "📄 result: a file a reader opens (PDF, Word, deck, web page, sheet, image); twins are one result"
    - "🃏 card: one result on screen, with the result itself inside"
    - "🗂️ send: one row of delivery.md (date, for, from, status); only a person writes sent"
    - "🧭 source row: Block, then each Job and Task part, on the Delivery screen"
    - "🎨 theme: the kind of Block (work, cowork, paper, insight, design, discovery, labeling)"
  - "📍 Where it sits":
    - "🔝 the top row of the workbench: Studio | Block · Job · Task | Delivery (s03-D04)"
    - "👯 twin of s02-studio-workbench-skill; neighbours s04 Related, s05 Report, s06 Run"
    - "🖥️ code: servers/workbench/frame.py, one look for every theme"
    - "🔗 feeds the reports q07_workbench_mapping and q08_workbench_base"
  - "🗺️ How to read this drawing":
    - "① this frame, the words"
    - "② boxes: why each part exists, joined by arrows; a red dashed arrow is not built yet"
    - "③ the screen: the expected Delivery (s03-D07) and one result card (s03-D08)"
    - "❓ a red leaf is an open point; ✅ done, 🔶 partly, ⬜ open"
- title: "🚚 Delivery: what makes it, what keeps it, what shows it"
  intro: Each box says why the part exists and holds its own tree; the arrows say how one leads to the next.
  boxes:
  - id: jobs
    at: [0, 0]
    title: "🧱 Jobs and Tasks"
    why: They do the work, so they make the outputs.
    most: 1
    tree:
    - "✅ keep no delivery/ of their own (s03-D01)"
    - "✅ a Task folder is tNN_<task>/, a Job jNN_<job>/"
  - id: delivery
    at: [1, 0]
    title: "📦 The Block's delivery/"
    why: One owner, so a reader finds every output in one place.
    most: 2
    tree:
    - "✅ delivery/jNN_<job>/tNN_<task>/<lane>/"
    - "✅ the path is the link to its source (s03-D02)"
  - id: sends
    at: [2, 0]
    title: "🗂️ delivery.md"
    why: Says what went out, to whom, so a resend is a row, not a copy.
    most: 1
    tree:
    - "✅ one row per send: date, for, from, status (s03-D05)"
    - "✅ status turns sent only by a person"
    - "❓ a Report's own build: a row here too?"
  - id: screens
    at: [3, 0]
    title: "🖥️ Today's five screens"
    why: One screen per theme, read live, so we see what each shows.
    most: 1
    tree:
    - "❓ cowork lists build.py as a sent message: fix it, or use delivery.md?"
  - id: skill
    at: [0, 1]
    title: "🧰 Skill and frame.py"
    why: One skill owns the rule; frame.py draws it for every theme.
    most: 1
    tree: []
  - id: rules
    at: [1, 1]
    title: "📏 The rules"
    why: Fixed choices, so no part keeps its own copy.
    most: 2
    tree:
    - "✅ D01 one owner, the Block"
    - "✅ D02 the path is the link"
    - "✅ D03 one skill owns the rule"
    - "✅ D04 Delivery at the right end of the top row"
    - "✅ D05 named by source; a send is a row of delivery.md"
    - "✅ D06 from a Job or Task, Delivery opens the Block's"
  - id: card
    at: [2, 1]
    title: "🃏 One card per result"
    why: A reader opens a file, so each result shows itself, with its state.
    most: 1
    tree:
    - "🔶 a card holds kind, state, size and source, sends, the result, its files"
    - "🔶 preview by kind: PDF the page, Word its PDF twin, sheet its rows"
    - "🔶 state in four words: current, stale, not built, old local"
    - "❓ stale needs what a result read: a list per part, from its build?"
  - id: expected
    at: [3, 1]
    title: "🎯 Expected Delivery"
    why: Today's five shapes become one screen for every Block.
    most: 1
    tree:
    - "🔶 top row, source row, Sends, Results as cards, checks below"
    - "🔶 small parts one row each until one is picked"
    - "❓ do rows take the Studio's groups, the same code?"
    - "❓ a deliverable from several Blocks: its own Block?"
    - "❓ build D07 and D08 in frame.py once JL agrees"
  arrows:
  - {from: jobs, to: delivery, label: produces}
  - {from: delivery, to: sends, label: records}
  - {from: sends, to: screens, label: shows}
  - {from: skill, to: rules, label: owns}
  - {from: rules, to: delivery, label: keeps one owner}
  - {from: screens, to: expected, label: "? not built yet", dashed: true}
  - {from: expected, to: card, label: made of}
```


In Tools
--------

Where its skill and code sit, under `Tools/plugins/haipipe-toolkit/`. The skill box in the drawing
reads the same off the disk on every build: the skill's folder as it is, its version, and each
function looked up in its file (JL 261011: "show what are the skills related folders in the Tools").

```text
skills/1_base/project/
├── haipipe-studio/     s02 Studio
├── haipipe-delivery/   s03 Delivery   ◀ this topic
├── haipipe-related/    s04 Related
├── haipipe-report/     s05 Report
└── haipipe-run/        s06 Run
servers/workbench/frame.py                        delivery_parts · _delivery_row · delivery_by_source
                                                  · _delivery_cards (a Page Task's card per lane)
skills/1_base/page/haipipe-draft/src/common.py    delivery_owner · delivery_dir · delivery_source
```


What the drawing holds
----------------------

Three frames (JL 261012; haipipe-studio 0.13.0), drawn from the `frames:` yaml above and the builder:

```text
① Background    a newcomer's folder tree, an emoji on every node: what Delivery is, the words, where it sits
② the boxes     eight boxes, each with an emoji title, a why line and its own tree: Jobs and Tasks, the
                Block's delivery/, delivery.md, today's five screens, the skill and frame.py, the rules,
                one card per result, the expected Delivery; arrows: produces, records, shows, owns, keeps
                one owner, made of, and a red dashed "? not built yet"; ❓ leaves are the open points
③ the screen    the expected Delivery (s03-D07) drawn with Paper-ScalingGlucose's own files, and one result
                card close up (s03-D08), in the workbench's colours
```

Read from disk on every build (filled into the boxes by id): each screen through `servers/workbench/frame.py` (`frame.render`, the Runs
panel left out), every Block's `delivery/` in `Tools/blueprints/` and in the SPACE beside Tools whose `Tools/`
link leads here (its `examples-*/`), the decisions and open items of this face, and the skill's folder.


Finding (read 261012)
---------------------

1. 13 Blocks keep a `delivery/`: 2 in Tools, 5 cowork, 5 paper, 1 design. Each theme draws it its own
   way: a table of files (vanilla, SHIFT), a table of sends (Samsung), a PDF preview then tables (paper
   Boards), and, for a paper Section, a card per lane with its state and the result inside.
2. 9 of 13 show no result inside the page, only names and counts; the 4 paper Boards with a built PDF
   show one. Only the Page Task's cards (`_delivery_cards`) show every result, embedded, with its state.
3. 3 of 13 keep `delivery.md` (SHIFT b02, b03, b04: 4 rows, all draft, none sent); none of their
   screens shows those rows. The other 10 have no record of what went out.
4. Samsung b11 and b12: cowork's send table reads each file of a send folder as a message, so
   `build.py` is listed with state `sent`; only a person may write sent (s03-D05).
5. 37 old `delivery/` folders still sit below a Block, against s03-D01: 13 in Paper-TimeEventDM, 11 in
   Paper-AnchorPK, 9 in Paper-CGMtoHbA1c, 4 in Design-PreVisitChecklist.


Decided
-------

s03-D01 · Delivery has one physical owner, the Block: Jobs and Tasks keep no `delivery/` of their own;
    their outputs sit under their source address, `delivery/jNN_<job>/tNN_<task>/<lane>/` (carries
    s02-D14 and s09-D05 on; JL 261010).
s03-D02 · The path is the link: each subfolder leads back to its source, `delivery/jNN_<job>/` to the
    Job folder and `delivery/jNN_<job>/tNN_<task>/` to the Task folder; `delivery_source()` and
    `delivery_dir()` in haipipe-draft/src/common.py map one to the other (JL 261010: "track the
    subfolder to link to the job folder and job/task folder").
s03-D03 · One skill owns the rule: `/haipipe-delivery`, beside haipipe-studio and haipipe-report;
    haipipe-block, haipipe-report, haipipe-cowork and haipipe-draft-delivery point to it instead of
    each keeping a copy. How a file is built stays with its lane owner (JL 261010: "should we have a
    skill named /haipipe-delivery? ... just as we have the /haipipe-studio").
s03-D04 · Delivery sits at the right end of the top row and opens like Studio: only it selected, the
    work row hidden, the level buttons keep the way back (s02-D18; JL 261010).
s03-D05 · A delivery folder keeps its source's name, `delivery/jNN_<job>/` (and `tNN_<task>/` under
    it); no `dNN-<send>/` card and no `dNN_jNN_<job>/` prefix (JL 261011: "could this be still the
    today's version or to make it like dNN_j01_vXXXX?"). A send is one row of one table,
    `delivery/delivery.md` (date · for · from · status), so a resend or a second reader is a row, not
    a copy, and Status turns `sent` only by a person. Why: the path stays the link (s03-D02) with
    nothing to strip; a paper's version Job already names the send (`j01_v1009_nmi`); and `dNN` is
    already a design in the design theme (b12, `run-generate-d<NN>`). Like `related/related.md` for
    what came in (b10 s01-D34), `delivery/delivery.md` lists what went out. Swept 261011: the s01
    screens and the s11 · s12 · s13 mock screens show parts by source, and `run-delivery-<dNN>`
    is `run-delivery-<lane>`, as haipipe-run already names it.
s03-D06 · From a Job or Task, the top row's Delivery opens the Block's Delivery, as Studio opens the
    Block's Studio: a Job or Task has no Studio, Related or Delivery of its own (JL 261011, "apply it
    to all the workbench"). A source row, Block · jNN · tNN, comes first with the open Job or Task
    picked, and each source's part shows inside it. This refines s09-D05's "the Job and Task views
    show their own part": the part is now a pick inside the Block's Delivery, not a separate page.
    Built by the b16 session in servers/workbench/frame.py (render's Delivery mode).


Proposed
--------

s03-D07 · Proposed (JL 261012): one Delivery screen for every Block, in every theme, top to bottom: the
    top row with Delivery at its right end (s03-D04); the source row, Block · each Job and Task part
    (s03-D06); Sends, the rows of `delivery/delivery.md`, what went out, to whom, draft or sent
    (s03-D05); then Results of the part picked, one card each (s03-D08); many small parts (a paper's
    Sections) one row each until one is picked; a theme's own checks (a paper's G4) folded below the
    results, never in place of them. It replaces today's five shapes (① of the drawing).
s03-D08 · Proposed (JL 261012): a result is a file a reader opens: a PDF, a Word file, a deck, a web
    page, a sheet, an image; an email is its send folder's draft page. Its twins (a .docx and the .pdf
    beside it) are one card; build files, logs and pieces (LaTeX's `master.pdf`, a `-view` page,
    `draft-sections/`) are not results. A card holds: kind and name; state (current · stale · not
    built · old local); size, when it was built and the part it came from ↗; its sends, the
    delivery.md rows that name it; the result itself, embedded; its files, Rebuild (copies a prompt,
    starts nothing) and the way back to its source. The Page Task's cards (`_delivery_cards`) do most
    of this already, per lane; the proposal widens them to every part of every Block.

s03-D09 · Decided (JL 261012, through the b10 watcher: "go ahead and do all"): the drawing is three frames,
    each a folder tree: ① Background, ② the Tree, ③ the screen, the expected Delivery with one result
    card close up; the old frames are folded in; the old builder, face and preview are in history/.
s03-D10 · Decided (JL 261012, through the b10 watcher): the drawing is boxes with trees joined by named arrows,
    an emoji on every node (haipipe-studio 0.13.0); the old builder, face and preview are in history/
    (-261012b).

Open
----

1. Settled 261011 by s03-D05 (named by source, one row per send). Was: each delivery is one dNN card named by the send,
   `delivery/dNN-<send>/`, with a face `dNN-<send>.md` (For · From · Status · Files); the parts keep
   their source folder inside it; Status turns `sent` only by a person, never by a build. Today the
   folders are named by source (`delivery/j01_v1009_nmi/`): rename now, or at the next send?
2. A Report's own build (`delivery/reports/qNN_<topic>/`): a row in `delivery.md` too?
3. Settled 261012 by b10 s32-D18 (JL: "for the delivery, we should also have the group tags as well, and have
   the delivery card, similar to the studio"): yes, the same group bar; one card per result; built in the base.
4. Built 261011 (b16 session): the Block's own Delivery ends with "By source" (part · from · files),
   one row per Job and Task part, each linking back to its folder (s03-D02).
5. A deliverable that pulls from several Blocks (a meeting deck): its own Block, as a paper Board is?
6. Stale needs to know what a result read: a Page knows (its check); a cowork `build.py` lists its
   inputs only in words. One small list per part, written by its build?
7. The 37 old `delivery/` folders below a Block (Finding 5): move them into the Block's `delivery/`
   with haipipe-delivery's move, paper by paper?
8. Cowork's send table lists `build.py` as a sent message (Finding 4): fix the cowork theme's reader,
   or replace that table with Sends from `delivery.md` (s03-D07)?
9. Build s03-D07 and s03-D08 in frame.py's Delivery mode once JL agrees: one card renderer for every
   part, from `_delivery_cards`.

(write here, or mark the drawing in red)
