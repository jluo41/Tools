s04 · Studio and Report
=======================

**Topic:** how a Block's studio topics (`studio/sNN-<topic>/`) and its report Questions
(`reports/qNN_<topic>/`) relate. Both draw. The studio is the source; a report's drawing is
generated from named studio frames, never drawn by hand (JL 261007: "use the draw from the sNN to
format its own draw").

**Feeds:** `reports/q03_block_questions/` (how Questions live in a Block), `q07_workbench_mapping/`
(Idea Studio and Audience Report on screen). The earlier note on this topic (261006) is now draft
v0.1 of Q03: `../../reports/q03_block_questions/draft/q03_block_questions-draft-v0.1.md`.


Files
-----

```text
s04-studio-and-report/
├── s04-studio-and-report.md            this face: what is decided, what is open
├── build_s04_studio_and_report.py      the builder; marks are kept on rebuild
├── studio_report_ui.py                 the workbench screens, drawn large; s11 draws them too
├── s04-studio-and-report.excalidraw    the drawing: six frames, a plain prototype
└── s04-studio-and-report.png           its preview
haipipe-report scripts/build_report_drawing.py   builds a report's drawing from its figure list (✎ 261007 moved from excalidraw-report, s21)
```

Rebuild: `python build_s04_studio_and_report.py` (or `../_build/make.sh`).
A report: `python Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-report/scripts/build_report_drawing.py <reports/qNN_<topic>/>`.


What the drawing holds
----------------------

```text
1 · Studio and Report       side by side: job, drawings, who makes and edits them, lifespan, link, screen
2 · From studio to report   studio frames -> the report's figure list -> build_report_drawing.py
                            -> qNN_<topic>.excalidraw (view only) -> the Audience Report row;
                            Suggest goes back to the studio (red: open)
3 · Idea Studio on screen       the workbench screen at the Block, Job and Task tabs: the tabs, the
                                Spaces row, one topic after another (live drawing · status · chat ·
                                feeds), the Runs panel; Work Details noted, empty on a Task
4 · Audience Report on screen   the same three tabs: one row per Question (Question | Work | Report,
                                the generated drawing with Rebuild · Suggest), its Runs panel
                                under every screen: "on disk", the folders and files behind it, each
                                with what on screen it feeds (studio_report_ui.FILES)
5 · the logic tree              boxes and lines for what a Block holds (studio/ -> sNN-<topic>/ ->
                                drawing · face · sessions; reports/ -> qNN_<topic>/ -> Page · drawing);
                                labelled arrows for how they relate: feeds, answered in, cites frames,
                                reads the list, copies, builds, evidence, and Suggest (red, open)
Questions                   what is still open
```


Proposed
--------

s04-D01 · Proposed (261007): the studio makes, the report shows. A studio topic holds many rough
    drawings that a person edits freely; a report holds one drawing, generated.
s04-D02 · Proposed (261007): a report's drawing is built by the excalidraw-report skill's `ref/build_report_drawing.py` from
    the figure list in its own `.md` (a `## Figures` yaml block: `from` a studio drawing, the
    `frame` name, a `caption`). The builder copies each frame with the person's marks except their
    red notes, scales it to one width, straightens lines, and adds a heading frame and a source
    line per figure. It is generated output: change the studio drawing or the list, then rebuild.
s04-D03 · Proposed (261007): a frame's name is the contract between a studio and a report. Rename a
    studio frame and every report citing it fails its build with the frame names it can find.
s04-D04 · Proposed (261007, JL's marks on frames 3 and 4): on screen, Idea Studio lists its topics
    as closed rows showing only the topic's name; a click opens the row in place, with its details
    (decided/open · sessions · feeds) and the live drawing across the row. Audience Report keeps
    today's Report cell (workbench-work `report_html`): the report's title, its answer line, its one drawing as a thumbnail, and a tag;
    the title and the thumbnail each open a pop-out. Rebuild and Suggest live in the Runs panel.
    The Question cell also lists the studio topics that feed it ("from the Idea Studio: s01-<topic> ↗"),
    read from each topic's `feeds:` line; each opens that topic's live drawing in a pop-out.
    Audience Report's third row is buttons, the selected one outlined: the register's Question
    groups (All · <group A> · <group B>), and the table is grouped the same way, a heading per
    group as today's work workbench draws one table per group. On a Page Task the third row is
    the Page's two views, Table · Reading.
    The pop-outs, from any tab: a topic full size; the report as the Page; its drawing full size,
    view only.
s04-D05 · Proposed (261007, JL: "for B, J, T we can have no children (the Work Details), but we can
    have the Idea Studio and Audience Report"): every level tab, Block, Job and Task, has Idea
    Studio and Audience Report. Work Details lists the level's children and may be empty: a Block
    with no Jobs yet, a Job with no Tasks, and always a Task (it has none), where it shows dashed.
    So any level can think in its own `studio/` and answer its own Questions in its own
    `reports/`, and its report drawings are built from its studio frames like the Block's.
    Drawn large in s11's two close-up frames ("Idea Studio · Block, Job, Task" and
    "Audience Report · Block, Job, Task"). Refines s01-D09 and s01-D14.
s04-D06 · Proposed (261007, JL: "I don't want the chat to be here ... is there a better way?"): a
    studio topic has no chat column and no `chat/` folder. A session that works on a topic is a
    pass of the topic's own soft Run, `runs/run-draw-<sNN>/passes/pNN-<MMDD>/`, holding the
    session's ask, its summary and what it changed (s05). The open topic shows its drawing across
    the whole row; its sessions list in the Runs panel beside it, and "Save this session" writes the
    pass. Changes s01-D02 (a topic held `chat/`); the existing `chat/` files move into passes once
    this is agreed.

First run: `reports/q03_block_questions/` cites s01's "1 · The ladder" and s11's "work Block";
its drawing builds (1091 elements) with JL's marks in the work Block frame kept.


Open
----

1. Keep the person's own marks in a figure (today: yes, except red notes)?
2. A frame much wider than the report shrinks to unreadable (s11's work Block, 8461 wide, at 0.34):
   split it into narrower frames, crop to a region, or a wider report?
3. Where the report drawing lives: `qNN_<topic>.excalidraw` beside the Page (s01-D03), or under
   `reports/qNN/studio/` (the excalidraw-report skill's report mode)? The builder follows s01-D03.
4. What Suggest writes: a note on the studio frame, or a comment on the report?
5. When it rebuilds: `make.sh`, a Run button on the Question's row, or on every studio save?
6. `feeds:` in a studio face and `## Figures` in a report: keep both, or derive feeds from the lists?
