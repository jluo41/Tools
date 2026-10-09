s32 · Paper element UI
======================

**Topic:** every kind of element the paper theme draws today, as it draws it, side by side, so the paper
takes the one look per element that b03 picks for every theme (b03 `s32-element-ui`, JL 261007: "collect all
types of the UI of different types of the element ... so we can unify them"). The versions are shot live from
the frame (`/_board/workbench`) at the paper's Block, Job and Task levels, every Space and every view, and from
its old pages, flagged OLD. Beside each element, its proposed look: b03's picks, a short why, a green line for
what changed and a red line for what is open.

**Feeds:** `reports/` q01_paper_ladder (each level's elements); b03 Q08 (one shared base, a theme each).


Files
-----

```text
s32-paper-element-ui/
├── s32-paper-element-ui.md          this face: Topic · Feeds · Files · Decided · Open, and the Theme elements
├── build_s32_paper_element_ui.py    the builder: --shoot walks the paper pages live, then draws the gallery
├── shots/                           one screenshot per element version, facts.json (place, places seen, style)
├── s32-paper-element-ui.excalidraw  the gallery: one frame per element, its "· proposed" frame beside it, Pick
└── s32-paper-element-ui.png         its preview
```

Shoot (a live host on this SPACE, headless Chrome):
`uv run --no-project --with playwright --with pillow python build_s32_paper_element_ui.py --shoot [--base http://127.0.0.1:5851]`
(`--no-project`: the SPACE's own project does not build under uv). Draw only: `python build_s32_paper_element_ui.py`.
Preview: `python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py
s32-paper-element-ui.excalidraw s32-paper-element-ui.png 0.25`. The Block has no build script of its own;
b03's `studio/_build/make.sh` runs the draw step (s32-D07).

The drawing helpers (picture, style line, the pick script, b03's frame helpers, the haipipe-studio canvas
writer) are imported from b03's `build_s32_element_ui.py`, not copied.


What the gallery holds
----------------------

```text
element                         versions   on old pages   walked from
1 · Top tabs                         5          2          Block · Job · Task; old Board page; Page workbench
2 · View row (third row)            15          5          every Space with views at each level; old pages
3 · Audience Report rows             7          3          every Audience Report view (q-row, lw-row, qc)
4 · The Space body                  22          4          each level × Space, its first view; old Board page
5 · Tables                           2          0          every view (the base's wf-table, the old grid)
6 · Rows and cards                  17          8          every view: topic, sec-row, item-card, rp-card, bj-tr …
7 · Disk · Runs panel                5          2          Block · Job · Task; old Board page; Page workbench
8 · Tags and pills                  15          3          every view: rp-tags, item-status, sec-state, ok/warn …
9 · Page header                      6          3          Block · Job · Task; old pages
10 · One item's display              6          3          a Section in the Task tab; /_board/draft, runs, run-result
11 · The paper's own elements       17          2          one card per paper-only view (Related, Ideation, …)
                                   117         35          + 9 proposed shots
```

Walked: the paper Board on the ladder (TestToLearn: its Block, its versions j01 and j02, and j01's
t01_introduction, which has delivery/, results/ and runs/), and an older Board in the A1-Story layout (its
Block and its Story group). A "distinct" element is one card per look met (its first place, "+N more
places"), told apart by its class and computed style. The old pages: the old paper Board page (rendered by
`paper.render_paper`, since `/_board/paper-board` now forwards to the frame), a Section's Page workbench page
(`/_board/draft`, where a Section row's ↗ goes), its Page Runs page (`/_board/runs`), and one run's results
page (`/_board/run-result`, from a High-level logic row).


Decided
-------

s32-D01 · b03's picks hold for the paper (261008, b03 s32-D01 · D02 · D05 · D08 · D09): top tabs in the D · E
    look and the view row in the E look, both drawn by the base frame, the paper giving its words only (Paper
    Board · Version ▾ · Section ▾); every question view's row is Question │ Work │ Report with the Question
    cell as the Insight row; Disk inside the Runs panel; no tags.

s32-D02 · Today's frame already draws the paper's top tabs, view row, header and Disk · Runs panel in the
    picked looks at every level (frames 1, 2, 7, 9: green "kept"); the Job's Questions view already draws the
    Insight row and is the proposal for every paper question view.

s32-D03 · Old pages are flagged OLD in red, in a red dashed box (b03 s32-D03): the old paper Board page (its
    address forwards to the frame; its look lives on inside the frame through `pv()`), and the item pages a
    paper row opens outside the frame (`/_board/draft`, `/_board/runs`, `/_board/run-result`).

s32-D04 · Done (261008, b03's ruling; JL 261007: reuse the old cards): the paper's views keep the old paper
    page's cards inside the base box through `pv()`: the Sections list (sec-row), the item cards (Draft-Main,
    Draft-Appendix, Comments, Cover letter, Letters) and the paper cards (Related). Only the Delivery grid
    tables take the base `table()`. (Replaces this topic's first proposal to retire `pv()`.)

s32-D05 · Decided (261008, b03's rulings), to build in `paper_theme.py`:
    1. Block › Ideation and Narrative rows take the base `question_cell()` (a "Question N" label with its
       state dot, the slug, one sentence); High-level logic keeps its lw rows.
    2. No tags in the paper's views (`rp-tags` and the other kinds): a state is a word or a dot.
    3. A Section's ↗ and a run row point at the frame (`/_board/workbench?path=…&view=draft`), not at
       `/_board/draft` or `/_board/run-result`.
    4. The views s11 and s12 plan, built in this order: Block Work Details (All · versions · grants · slides),
       the Job's Delivery cards (Manuscript · Letters · Checks · Sent), the Block's Delivery per version, the
       Runs third row.

s32-D06 · Kept as drawn (261008, b03's rulings): Task › Runs embeds the Page Runs page until the base's Page
    views (`?view=runs`) draw lanes; Description › Venue shows one line while no `venues/` is on disk.

s32-D07 · b03's `studio/_build/make.sh` builds this topic (draw only), and b03's s32 reads the Theme elements
    list below (261008).


Theme elements
--------------

The elements the paper theme uses, by level and Space › view, planned in s11 (Block), s12 (Job) and s13
(Task): same as the base, or its own and why; then whether today's frame draws it, a gap marked `? …` (red
on the drawing, frame 11 · proposed).

- Top tabs · all levels · the level row and the six Spaces · base · drawn
- View row · all levels · every Space with views · base · drawn
- Question rows · Block · Audience Report › Ideation (ID…: why this paper) · base question_cell(), the paper's words · ? the older cell: take question_cell()
- Question rows · Block · Audience Report › Narrative (N1–N4: says · drawn · told · attracts) · base question_cell(), the paper's words · ? the older cell: take question_cell()
- Question rows · Block · Audience Report › High-level logic + Low-level work (RQ │ work │ report) · own: the RQ's hypothesis and claim, the work tree under it · kept: its lw rows
- Question rows · Block · Audience Report › Related Questions · base · drawn
- Question rows · Job · Audience Report › Questions (J1–J5) · base · drawn (the Insight row)
- Old item cards · Job · Audience Report › Draft-Main · Draft-Appendix · Comments · Cover letter · own: the old paper cards (pv()) · kept: JL reuses the old cards
- Question rows · Task · Audience Report › Questions · Comments · base · drawn
- Space body · all levels · every Space · base box, the old cards inside (pv()) · drawn
- Tables · Block · Job · Task · Description › Scope · Version · the reader contract · base · drawn
- Tables · Block · Delivery › LaTeX · Word (checks, artifacts) · base table() · ? grid tables: take table()
- Rows · Block · Work Details › Jobs (All · versions · grants · slides, s11) · base · ? build 1: today Jobs · Main · Appendix · Evidence
- Old Section rows · Block · Job · Work Details › Main · Appendix: the Sections · own: the old sec-row (pv()) · kept: JL reuses the old cards
- Old paper cards · Block · Description › Related: paper cards, each opening on its drawing · own: the old rp-card (pv()) · kept; no drawing on a card yet
- Rows · Block · Description › Venue: one row per `venues/<venue>/` · base · kept: no venues/ on disk, one line
- Rows · all levels · Idea Studio: one topic per row · base · drawn
- Disk · Runs panel · Block · Job · every Space · base · drawn
- Disk · Runs panel · Task · Runs Space · base · for now: embeds the Page Runs page (until ?view=runs draws lanes)
- Delivery cards · Job · Delivery (Manuscript · Letters · Checks · Sent, s12) · base cards · ? build 2: today a folding list and a table
- Delivery cards · Block · Delivery (All · j01 · j02: each version's build, s11) · base cards · ? build 3: today LaTeX · Word · Cover letter · Rounds
- Runs third row · Block · Job · Runs (venue · question · draw · version · from below, s11 · s12) · base · ? build 4: no third row yet
- Delivery cards · Task · Delivery (◆ Ready, then Web · LaTeX · Word · Slides · Render, s13) · base cards and the paper's own Ready · drawn
- Table · Reading · Task · Audience Report › Table · Reading · the base's Page Task views · embedded, in the Page's own look
- Draft-… · Evidence-… · Task · Work Details · the base's Page Task views · embedded, in the Page's own look
- Reader contract · Task · Description › Scope (◆) · own lines in a base table · drawn
- SUB-* rows · Task · Description › Requirement (◆) · own lines in a base row · drawn
- Tags · all levels · — · none (b03 s32-D09) · ? 12 kinds drawn today: remove
- Page header · all levels · the title line · base · drawn
- One item's display · Task · a Section opens as the Task tab · base · ? a Section's ↗ and a run row: point at /_board/workbench?…&view=draft

Open
----

1. Build s32-D05 in `servers/workbench-paper/paper_theme.py` (the paper's own code, not the base): the
   question cells, no tags, the Delivery tables, the links into the frame, then the four planned views in
   order. Not done in this topic, whose brief was no server change; waiting for JL's go.
2. Pick the looks b03 leaves open (the Pick frame): one item's display, once the links point at the frame.
3. Related's paper cards have no drawing yet (the discovery read's draw step, s11).

(write here, or mark the drawing in red)
