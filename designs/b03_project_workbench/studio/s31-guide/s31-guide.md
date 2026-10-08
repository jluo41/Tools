s31 · Guide
===========

**Topic:** the Guide tab of the frame: the family's docs, the same in every Block. Its four Views
(Description · Method · RoadMap Draw · Related Paper), the files each reads in
`servers/workbench-<theme>/`, how those files relate, and each family's status. Drawn in the style
of `../s04-studio-and-report` (moved here from b02's s02 when b02 merged into b03; JL 261007: "for
Guide, we will use this structure"; "just follow the style of s03 (studio and report)": b02's s03 then, s04 now).

**Feeds:** `reports/q08_workbench_base/` (one shared base, a theme each).


Files
-----

```text
s31-guide/
├── s31-guide.md                 this face: what is decided, what is open
├── build_s31_guide.py           the builder (b03's helpers and screen); marks are kept on rebuild
├── s31-guide.excalidraw         the drawing: seven frames, a plain prototype
├── s31-guide.png                its preview
├── method-canvas.py             a tool: a theme's first guide/methods.excalidraw from its method.md
└── history/                     the 261002 Guide design and the first 261007 proposal, each with its builder
```

Rebuild: `python build_s31_guide.py`.


What the drawing holds
----------------------

```text
1 · Guide and the level tabs   side by side: job, what it holds (4 Views × 3 folding sections), its
                               shape (cards), what it reads, its words (base, then theme), what is
                               live, where it is the same, who edits, run types, on screen
2 · From folder to Guide       the base's levels.yaml · guide.yaml · method.md + methods/ · related/ ·
                               the studio drawings -> guide_families.py -> workbench_guide.py -> the
                               Guide tab; <theme>_theme.py -> frame.py spaces_for -> each Space card's
                               sub · runs, live
3 · Guide on screen            the four Views, proposed, each a full screen with the Run types panel
                               (Add a method · Add a paper); every View's body in three folding
                               sections, Block · Job · Task, each a heading over its cards; a fifth
                               screen shows Job and Task folded; under each: "on disk", the files behind
                               it and what on screen each feeds; pop-outs: a method card, the methods
                               canvas, a paper
4 · Guide today                the same four Views as the server renders them now (old Space words)
5 · the logic tree             boxes and lines for what the base holds (guide/levels.yaml, the renderer
                               workbench_guide.py, frame.py) and what a theme's Guide holds (guide/,
                               related/, <theme>_theme.py); labelled arrows: default words, sub · runs
                               live, fills its Spaces, levels: overrides, table and roadmap: name, a step
                               cites its cards, a card cites its papers, pdf column; red: open
6 · status                     what each family's Guide has of the card Guide, read off the code at
                               build time: theme file · levels: · method.md by level · Method 'where'
                               · roadmap: · papers.md level column; red = not yet
```


Proposed
--------

s31-D01 · Proposed (261007): the Guide is the frame's first tab, the family's docs, the same in
    every Block and at every level; its four Views are Description · Method · RoadMap Draw ·
    Related Paper, its Run types Add a method · Add a paper.
s31-D02 · Done (261007): each theme keeps its Guide in `servers/workbench-<theme>/guide/` and
    `related/`; `guide_families.py` loads every `guide/guide.yaml`.
s31-D03 · Proposed (261007): Description shows the six Spaces by level in the theme's words,
    instead of the old board's Spaces.
s31-D04 · Proposed (261007): a Method step's "where in the workbench" names one of the six Spaces.
s31-D05 · Proposed (261007, JL's marks on frame 3: "separate each Guide's subview with three
    sections"): the four View tabs stay; each View's body is a header line, then three sections
    top to bottom, Block · Job · Task. Description: each level's role, its row of the six Spaces,
    its skills and folders. Method: each level's steps table and method cards. RoadMap Draw: each
    level's part of the theme's ladder. Related Paper: the papers behind each level's method (a
    level with none says so). Still one Guide per theme: `guide.yaml`, `method.md`, the ladder and
    `papers.md` each get a Block, a Job and a Task part. Refines s31-D01 and s31-D03.
s31-D06 · Proposed (261007, JL: "more like the section card, from up to down to stack"; "for each
    theme, they have their own definitions, but I want the view of them to be consistent"): inside a
    level's section, its items stack top to bottom as cards, one card shape per View, the same in
    every theme; a theme gives the words, never the shape.

    ```text
    View            card            title line                      second line
    Description     a Space card    <Space>  <what it is here>      sub · reads · runs
    Method          a step card     <N · step>  <what happens>      where · methods · signs
    RoadMap Draw    a drawing card  <drawing>  <what it shows>      the drawing, embedded ↗
    Related Paper   a paper card    <title>  <author year · venue>  role · why here · ↗
    ```

    How they update, so a card never goes stale: the shape lives in the base's one renderer
    (`workbench_guide.py`); a Space card's `sub` and `runs` are read live from the frame
    (`spaces_for`: the base, then the theme's `<theme>_theme.py`); its words come from the base's
    defaults (`servers/workbench/guide/levels.yaml`, proposed), and a theme's `guide.yaml`
    `levels:` overrides only the words that differ. Step cards come from `method.md`'s
    `## Block · ## Job · ## Task` tables; paper cards from `papers.md` with a level column.
s31-D07 · Proposed (261007, JL: "I don't want boxes in box"; "I want they are collapsable in the
    Block, Job and Task level"): a level is a heading, not a box; the cards under it are the only
    boxes (a drawing card's box is the drawing itself). Each level heading folds: ▾ open, ▸ folded
    with one line of what it holds (Description: "6 Spaces · skills · folders"); a click toggles it.
    Proposed: the tab you came from opens its level and the other two start folded. Drawn as the
    fifth screen of frame 3 (Description from the Block tab).
s31-D08 · Proposed (261007, JL: "for the roadmap draw, for each section, could we have cards as
    well, in case there are multiple draw to show"): RoadMap Draw's level sections hold drawing
    cards, one per drawing: ▸ title · what it shows, then its source and builder and ↗ full size;
    a click opens the card and its drawing fills it, view only, as an Idea Studio row does. On disk
    `guide.yaml` gets `roadmap:` with a list of drawings per level.


s31-D09 · Done (261007): the work theme is on the card Guide. The base's words are
    `servers/workbench/guide/levels.yaml`; `workbench_guide.py` draws every View as three folding
    level sections of cards, the earlier body under a closed "All levels"; Space cards read `sub`
    and `runs` from `frame.space_cards`; the frame passes its level, so that section opens. The
    work family's key is `work` (`task` still answers), its `guide.yaml` has `levels:` and
    `roadmap:`, its `method.md` a step table per level, its `papers.md` a `level` column
    (table-papers accepts it as an optional first column). Tests: `_host/tests/test_guide_levels.py`;
    the other families are in the conformance test's GAPS until they move. Frame 6 tracks them.

Open
----

- `levels.yaml`: the base's home for the default card words (Block · Job · Task × the six Spaces)?
- Folds: the tab you came from opens its level and folds the other two; remember a person's folds?
- The page family (`workbench/task-page`): its own Guide, or the Task sections of each theme's Guide?
- A wrong "where": fail the tests, or warn on the page?
- RoadMap Draw per level: which drawings each theme lists first?
- b03's s11 · s12 · s13: draw their screens in this style?
