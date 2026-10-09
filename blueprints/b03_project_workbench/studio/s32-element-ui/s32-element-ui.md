s32 · Element UI
================

**Topic:** every kind of element a workbench draws, as each workbench draws it today, side by side,
so one look per element can be picked and the base draws it for every theme (JL 261007: "collect
all types of the UI of different types of the element ... so we can unify them"; "for each type
of the element, show the different versions, like the gallery, and we will pick and select. Like
for the audience report, we might have different versions as well"). It answers JL's "the current
UI is very bad, not as good as the previous ones": the previous looks are all here to choose from.

**Feeds:** Q08 (one shared base, a theme each).


Files
-----

```text
s32-element-ui/
├── s32-element-ui.md            this face: what is decided, what is open
├── build_s32_element_ui.py      the builder: --shoot screenshots each element live, then draws the gallery
├── shots/                       one screenshot per element and page, and facts.json (each one's computed style)
├── s32-element-ui.excalidraw    the gallery: one frame per element, one card per version, then Pick
└── s32-element-ui.png           its preview
```

Shoot (a live host on this SPACE, headless Chrome):
`uv run --with playwright --with pillow python build_s32_element_ui.py --shoot [--base http://127.0.0.1:5851]`.
Draw only (what `make.sh` runs): `python build_s32_element_ui.py`.


What the gallery holds
----------------------

```text
element                         versions today, from
1 · Top tabs                    8: the frame, paper, work, insight, design, discovery, labeling, Page workbench
2 · View row (third row)        5: paper (frame), work, insight, discovery, Page workbench
3 · Audience Report rows        4: the frame (Question │ Work │ Report), work, insight, discovery (a table)
4 · The Space body              9: every page's open Space, its first screen
5 · Tables                      3: paper (frame), design, discovery
6 · Rows and cards              4: the frame's studio rows, work, insight, labeling
7 · Disk · Runs panel           6: the frame, paper, work, design, discovery, Page workbench (all opened)
8 · Tags and pills              2: discovery, labeling
9 · Page header                 8
(the Disk box was its own element until Disk moved inside the Runs panel, 261007)
```

Under each picture: its first control's computed style (font, corner radius, padding, border,
fill), read live, so two looks that seem alike can be told apart by number.

The pages: the frame (`/_board/workbench`, the new base) and every older page still served beside
it (work-board, insight-board, paper-board, design-board, discovery-board, labeling-board, and one
Page's Draft view). No cowork Block exists on disk, so cowork has no card.


Decided
-------

s32-D01 · Done (261007, JL's marks on frame 1: arrows from D and E to A; "what I mean is the style,
    not the content"): top tabs take the Insight and Design board pages' look, D · E: 16px text,
    6px corners, padding 6px 14px, a grey border (#ced4da), the open one washed blue (#e7f5ff,
    #1864ab). The look only: each workbench keeps its own tabs and words, the frame its level row
    (Guide · Block · Job ▾ · Task ▾) and its six Spaces with their dividers; an optional Space's
    border is solid like the rest (JL 261007: "could you make it the solid line as well?"). The frame took it (`servers/workbench/frame.py`, the `.levels`/`.spaces` rules and the
    `--tab-*` tokens); the third row keeps its own look until picked.

s32-D02 · Done (261007, JL's tick on frame 2, card E; "do not use this one" on the small pills): the
    view row takes the Page workbench's view buttons, E: 16px, 6px corners, padding 5px 12px, a grey
    border, the open one washed blue; the look only. The frame took it (`.subs` rules in frame.py).
s32-D03 · Done (261007, JL: "some of them are old version and we will not use it ... flag them"): a
    card whose page is a theme's old board page (its theme draws on the frame now) or the old Page
    workbench (its views are the frame's Task Spaces) is flagged OLD in red, greyed, in a red dashed
    box; read off the code at build time (`old_reason`). Only the frame is current. A look from an
    old page may still be picked (D · E for the tabs were).

s32-D04 · Proposed (261007, JL: "we want to unify things ... for each frame, add a new frame to the right
    of it and draw the proposed new one and explain why"): beside each element's gallery frame, a
    "· proposed" frame: one look for every theme, drawn by the base, a theme giving the words only.
    Where the frame already draws it in the picked look, its own version is the proposal, shot live
    (tabs, view row, Question rows, Space body, table, rows, Runs panel, Disk, header); tags have no
    frame version yet, so a mock in the frame's colours (one small pill, its colour the state).
    Each says why in two or three lines (`PROPOSALS` in the builder).

s32-D05 · Done (261007, JL on frame 3: "Question label at the top, and then Question slug, and then short
    and concise question explanation ... remove the 'builds on' ... keep 'from the Idea Studio'"): the
    frame's Question cell reads as the Insight row: a label pill (Question 1) with its state dot (grey
    open, yellow partial, green answered), the Question's short name in bold (its register `slug:`,
    `name:` or title), one sentence of what is asked (the register's `question:`, cut at its first
    sentence), › More with the full question, hypothesis and acceptance, then "from the Idea Studio".
    `frame.question_cell`.

s32-D06 · Done (261007, JL on frame 4, card B: "for the idea studio, we will just keep this, move this to
    the right"): Idea Studio keeps the frame's look as it is, one closed row per topic with its facts and
    the Questions it feeds, opened in place; it sits in frame 4's proposed frame as its second picture.

s32-D07 · Done (261007, JL on frame 4, card E: "move this to the right, this is for the Insight board
    only"): the Insight board's body (its partitions as views, its levels folded, a Question │ Work │
    Report row per question) is kept for the insight theme only, the third picture of frame 4's
    proposed frame. And every proposed frame says in short green words what changed there, or that it
    is kept (JL: "my comments with the green short words in where the changes made"; `CHANGED`).

s32-D08 · Done (261007, JL on frame 8: "this one can be removed, as the Disk and Runs are together"):
    no Disk box element; element 7 is the Disk · Runs panel, the Disk list its first part. Tags and the
    header are now 8 and 9.

s32-D09 · Proposed (261008, JL on frame 8: "I will propose we don't use any of them, just remove all"):
    no tags in any theme. A state is a word (open · partial · answered) or the Question's state dot;
    an id is plain text where it stands.

s32-D10 · Proposed (261008, JL: "I didn't see where to have display for the design items"): a new element,
    10 · One item's display: one design, one Insight question page, one Insight run, one labeling job, as
    their item pages draw them today (flagged OLD) and as the frame's design theme draws one design (its
    Task, Work Details). Proposed: an item opens in the frame, as its own level's Spaces or in the pop-out
    from its row; the item pages retire.

s32-D11 · Done (261008, JL: "we will in the Design-Job's Audience Report's Design Display show the Design
    Items ... we will have new frame for it"): a new element, 11 · Design display. On the ladder a design
    Job's items live in its Audience Report › Design display (b12): one row per design, the design as it
    reads │ its process (③) │ its review (④ ⑤), the first open, the dropped folded for the record. No
    Project holds a ladder design Job yet, so its card is drawn from the design tests' sample Block
    (design_fixture.py). An older board (Design-NN folders, also one in designs/_old/ such as AuthenUI)
    shows its old item view in place, its Task › Work Details › Designs (b12); the frame reads a Block
    kept in an archive inside a Theme folder in that theme (frame.theme_folder).

s32-D12 · Done (261008, JL: "for your own s32, you should track these theme based element UI as well"):
    a "Theme elements" frame beside Pick reads every theme Block's own s32 (b11 insight, b12 design and
    b16 paper first, built by their own sessions; b13-b17 as they start) on every build: its folder,
    frames, decisions, open points and the list under its "Theme elements" heading (element · level ·
    Space › view · the base's or its own, and whether the frame draws it). A theme with none reads "not
    started" in red. Each theme drew its list from its own s11 · s12 · s13.


s32-D13 · Done (261008, built in the frame and approved: "it is great", JL on the design Job's top: "How do you think we can replace the 🎨 Design ·
    j04_… and [the level row] … I think we can merge the frame of 1, 2 and 9 together in one frame"; then
    "no, it will still be four lines"): the page header, the top tabs and the view row are drawn as one
    element, "1 · Top of the page" (the others renumbered 2-9; their shots unchanged). The page keeps its
    four lines, in this order (JL's sketch): the level row on top, then the title, then the Spaces row
    and the view row; the title heads what is open below it. JL: "make the first line like the page
    index and the second line to be the title of the webpage", with a larger gap: the level row is the
    navigation, a thin rule under it; the title is larger (26px) with a wide gap above and below. A faint line, as light as the one under the index,
    separates the Spaces row from the view row when there is one ("not that salient"). The title reads the
    theme's icon and name, the level and the folder's own title (its face's heading), the folder name on
    hover; in the level row a Job or Task shows in its dropdown by a short name, its tag and its parts'
    ids (jNN · gNN · mNN) or its tag and first words, the full folder name in the open list; the browser
    tab keeps the full name. The Spaces row and the view row stay as picked.

Open
----

1. Pick one look per element (the Pick frame: write the letter you keep, or draw a new one).
   The first ask (JL 261007, on the tabs): the Insight board's buttons, square corners and a
   washed-blue selected button, the view row inside the content box.
2. Once picked: the base (`servers/workbench/frame.py` CSS, `runs_panel.py`) draws each picked
   look, every theme gets it, and the older pages keep theirs until they retire.

(write here, or mark the drawing in red)
