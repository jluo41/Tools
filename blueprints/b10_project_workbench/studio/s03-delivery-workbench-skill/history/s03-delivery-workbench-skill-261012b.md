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
├── s03-delivery-workbench-skill.excalidraw    three frames: Background, the Tree, the screen
├── s03-delivery-workbench-skill.png           its preview
├── .s03-delivery-workbench-skill.seed.json    generated snapshot for preserving marks
├── build_s03_delivery_workbench_skill.py      the builder; reads frame.py, every delivery/ and this face on each build
└── history/                                   the 261011 and the 261012 story builders, faces and previews
```
skill: Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-delivery/
```


In Tools
--------

Where its skill and code sit, under `Tools/plugins/haipipe-toolkit/`. The drawing's "In Tools" frame
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

Three frames (JL 261012), two of them a folder tree:

```text
① Background    a newcomer's tree: what Delivery is, the words it uses, where it sits, how to read the drawing
② the Tree      the topic as one folder tree, red ? leaves for what is open: today's five screens (read
                through frame.render, each with its checks), every delivery/ on disk, the rules s03-D01 to
                D06, the proposals s03-D07 and D08 (card parts, preview by kind, state in four words),
                the open items, In Tools (the skill's folder, version and functions)
③ the screen    the expected Delivery (s03-D07) drawn with Paper-ScalingGlucose's own files, and one result
                card close up (s03-D08), in the workbench's colours
```

Read from disk on every build: each screen through `servers/workbench/frame.py` (`frame.render`, the Runs
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

Open
----

1. Settled 261011 by s03-D05 (named by source, one row per send). Was: each delivery is one dNN card named by the send,
   `delivery/dNN-<send>/`, with a face `dNN-<send>.md` (For · From · Status · Files); the parts keep
   their source folder inside it; Status turns `sent` only by a person, never by a build. Today the
   folders are named by source (`delivery/j01_v1009_nmi/`): rename now, or at the next send?
2. A Report's own build (`delivery/reports/qNN_<topic>/`): a row in `delivery.md` too?
3. Do Delivery rows take the Studio's groups (Current and tags), the same code?
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
