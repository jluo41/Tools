s32 · Design element UI
=======================

**Topic:** every kind of element the design theme draws, in one gallery, so the UI can be unified (JL
261007, b03 s32: "collect all types of the UI of different types of the element ... so we can unify
them"). Each element is shown three ways: as the design theme draws it today on the frame
(`/_board/workbench` at its Block, Job and Task levels, every Space and view), as its old board and item
pages draw it (flagged OLD), and as s11 · s12 · s13 plan it. Beside each element, a "· proposed" frame:
one look, b03's picks kept, with why, a green line for what changed and a red line for what is open. It
is b03's `s32-element-ui` cut to one theme, and it adds the elements that only design has.

**Feeds:** `../../reports/` q02_design_workbench · and b03's s32 (its Theme elements list).


Files
-----

```text
s32-design-element-ui/
├── s32-design-element-ui.md              this face
├── build_s32_design_element_ui.py        the builder: --shoot screenshots each element live, then draws
├── shots/                                one picture per card (<element>__NN.png, proposed__<element>.png)
│                                         and facts.json (each one's page, selector and computed style)
├── s32-design-element-ui.excalidraw      the gallery: title · Theme elements · Pick, then one frame per
│                                         element and its "· proposed" frame
├── .s32-design-element-ui.seed.json      the last build, so a rebuild keeps marks
└── s32-design-element-ui.png             its preview
```

Shoot (headless Chrome; a live host serves this SPACE):
`uv run --no-project --with playwright --with pillow python build_s32_design_element_ui.py --shoot [--base http://127.0.0.1:5851]`.
`--no-project` is needed inside the SPACE, or uv tries to build the SPACE's own environment.
Draw only: `python build_s32_design_element_ui.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s32-design-element-ui.excalidraw s32-design-element-ui.png 0.2`.

No Project holds a design Block on the ladder yet. So `--shoot` writes the design tests' sample Project
(`servers/workbench-design/tests/design_fixture.py`, placeholders only) to a temp folder, starts a
second host on it (the same `serve.py`, a free port), shoots the ladder pages live from it, then stops
it. The old pages come from the SPACE's host. b12 has no build script of its own: b03's
`studio/_build/make.sh` builds b12's s01, s11 – s13 and, since 261008, this topic (draw only).


What the gallery holds
----------------------

```text
element                                      cards   OLD   planned screen
1 · Top tabs                                   5      2    s13 · d04 Description › Design
2 · View row                                   6      2    s12 · Runs › Setup
3 · Audience Report rows                       4      0    s11 · Audience Report › Questions
4 · The Space body                             8      2    s12 · Audience Report › Reason ideas
5 · Tables                                     9      3    s13 · t99 Audience Report › Ranking
6 · Rows and cards                             7      2    s11 · Description › Goals
7 · Disk · Runs panel                          6      2    s12 · Work Details › Conduct & Review (s12's name)
8 · Tags and pills                             3      0    (none: no tags)
9 · Page header                                5      2    (none: the planned screens draw no header)
10 · One design's display                      5      2    s13 · d04 Description › Design
11 · Design display                            6      2    s12 · Audience Report › Design display
--- the design theme's own elements ---
12 · A design as it reads (the phone)          5      1    s13 · d04 Audience Report › Drafts
13 · Goal × method Map                         4      2    s11 · Description › Map
14 · Inputs fence                              3      1    s12 · Description › Inputs
15 · Reasoning chains                          3      0    s13 · t00 Audience Report › Topics
16 · Predicted vs observed, cost               5      0    s11 · Audience Report › Predicted vs observed
17 · Review: tests and ranking                 5      1    s13 · d04 Tests · t99 Coverage
                                              89     24    16 planned screens · 17 proposed frames
```

The OLD pages are the design board page (`/_board/design-board`, the B01 and B00 boards) and the design
item page (`/_board/design`, one design task; one AuthenUI login card). Both boards moved into
`designs/_old/` on 261008. The frame on an older board (B01 at Block level, and one Design Folder that
embeds its old item page) is the current frame, so it is not flagged.


Theme elements
--------------

element · level · Space › view · from the base, or the theme's own and why · drawn today (GAP = open)

- top tabs · every level · the level row and the six Spaces · the base; the Task select by step through
  the theme's `option()` hook ("Task · d04 · ask-only", grouped ② · ③ · ⑤) · yes
- view row · every level · every Space's views · the base · yes (one casing: Reason ideas · Conduct &
  review · Review whole)
- Question rows · Block · Audience Report › Questions · the base (Insight's row) · yes
- Question-style row · Block, Job, Task · Predicted vs observed; Description › Design · the base row,
  with the columns Design │ Predicted │ Observed · yes
- Space body and Disk · Runs · every level · every Space · the base · yes
- table · every level · Map, Inputs, Cost, Ranking, Ideas, Elements, Tests, Runs, the Block's Job
  preview, Delivery, Drafts · the base (wf-table; no tile grid) · yes
- folding row (the "card" of s11 · s12) · Block, Job, Task · Goals, Methods, Inputs, Runs, Method,
  Kept · Dropped, Conduct & review (a row per design Task) · the base row · yes (dropped: plain, folded)
- Runs panel · every level · every Space · the base (4 rows per type, then +N more) · yes
- tags · none (b03 s32-D09) · an id is mono text, its words after it · yes (chips removed)
- header · every level · the top line · the base · yes
- design card (Design │ Process │ Review) · Job, Task · Audience Report › Design display; Task
  Description › Design · its own: a design is read three ways side by side · yes
- Design display · Job · Audience Report › Design display · its own: the N designs in order, the
  dropped folded · yes
- design as it reads · Block, Job, Task · Design display, Drafts, Predicted vs observed, Delivery, the
  Block's Job preview · its own (b03 261008): an SMS on a phone, a UI design as its screens/ PNG · yes ·
  GAP: no UI design on the ladder yet to show the screen with
- goal × method Map · Block · Description › Map, and its compare pop-out · its own: Jobs placed by
  goal and method, a column per registered method · yes
- inputs fence · Block, Job · Description › Inputs · its own: what the design work may see · yes
- Reason ideas (chains) · Job, t00 · Audience Report › Reason ideas; t00 › Topics, Chains · its own:
  step ②'s topics and chains · yes
- Review whole (ranking) · Job, t99 · Audience Report › Review whole; t99 › Ranking, Coverage,
  Kept · Dropped · the base table and its kept line · yes
- Tests (④) · Task · Audience Report › Tests; Description › Evaluation · the base table · yes
- predicted vs observed, scorecard, cost · Block, Job, Task · Audience Report views; Performance · the
  base table and the phone · yes · GAP: tokens are empty until the Run receipt has `usage:`
- Idea Studio · every level · Idea Studio · the base (b03 s32-D06) · yes
- one design's own page · old · `/_board/design` · retires: a design is a Task · old page


Decided
-------

s32-D01 · Done (261008): b03's picks hold for the design theme too: top tabs in the D · E look, the
    view row in the E look, the Question cell as the Insight row, Disk inside the Runs panel, no tags
    (b03 s32-D01, D02, D05, D08, D09). The design theme gives the words, and the layout of its own
    elements only.
s32-D02 · Done (261008): the ladder levels are shot live from the design tests' sample Project, served
    by its own host for the shoot, until a Project holds a design Block on the ladder. The old pages
    are shot from the SPACE's host and flagged OLD (`old_reason`, read off the code).
s32-D03 · Done (261008, asked by b03 for JL): each element also shows its planned screen, drawn by
    s11 · s12 · s13's own builder functions (`../_build/design_ui.py`), so the gallery follows the
    level designs on every rebuild.
s32-D04 · Proposed (261008): six elements are the design theme's own (12 – 17). Each is proposed as
    the frame draws it today, built on the base's table, row and box. Only the phone's look is new,
    and it should move into the base's styles (Open 3).
s32-D05 · Proposed (261008): one design opens as its own Task (s13), and the design item page
    retires. An older Design Folder keeps its old item view inside the frame until it moves onto the
    ladder (b03 s32-D11).

s32-D06 · Done (261008, b03's rulings on the nine gaps): the Task select is grouped by step through the
    theme's `option()` hook (`design_theme.option`); the Runs panel pages at 4 per type (base). In the
    design theme (`design_views.py`): no chips, an id in mono with its words; the tile grid replaced by
    the base table; the dropped designs plain and folded; a Map column per registered method; Job ›
    Runs › Conduct & review one row per design Task; one casing for the Job's views; a UI design shows
    its `screens/` PNG where an SMS shows the phone. Tested in `test_design_ladder.py`
    (`test_the_b12_s32_rulings`).


Open
----

1. Pick one look per element: the Pick frame lists each one, with b03's picks in green and the
   proposal in red.
2. No UI design sits on the ladder yet, so its rendered screen is tested but not shot.
3. Tokens stay empty until a Run's receipt carries `usage:` (another owner, s11).
4. When `designs/Design-SMSR2-Stage25-CarryOver-261008/` (new 261008, still empty when this was shot)
   holds the ladder, shoot its live pages instead of the sample Project's.

(write here, or mark the drawing in red)
