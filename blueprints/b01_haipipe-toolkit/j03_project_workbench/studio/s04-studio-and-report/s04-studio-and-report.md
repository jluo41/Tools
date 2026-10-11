s04 · Studio and Report
=======================

**Tags:** `Structure` · `Workflow`

**Topic:** how a Block's Studio items (`studio/sNN-<topic>/`) and its report Questions
(`reports/qNN_<topic>/`) relate. Both draw. The studio is the source; a report's drawing is
generated from named studio frames, never drawn by hand (JL 261007: "use the draw from the sNN to
format its own draw").

**Feeds:** `reports/q03_block_questions/` (how Questions live in a Block), `q07_workbench_mapping/`
(Idea Studio and Audience Report on screen), `q09_studio_report_on_screen/`
(frame-to-Question links, panel behavior and safe drawing saves). The earlier note on this topic (261006) is now draft
v0.1 of Q03: `../../reports/q03_block_questions/draft/q03_block_questions-draft-v0.1.md`.


Files
-----

```text
s04-studio-and-report/
├── s04-studio-and-report.md            this face: what is decided, what is open
├── build_s04_studio_and_report.py      the builder; marks are kept on rebuild
├── studio_report_ui.py                 the workbench screens, drawn large; s11 draws them too
├── s04-studio-and-report.excalidraw    the drawing: nine frames, relationship and screen prototypes
├── s04-studio-and-report.png           the full preview
└── s04-relationship.png                a readable preview of the relationship frame
haipipe-report scripts/build_report_drawing.py   builds a report's drawing from its figure list (✎ 261007 moved from excalidraw-report, s21)
```

Rebuild: `python build_s04_studio_and_report.py` (or `../_build/make.sh`).
A report: `python Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-report/scripts/build_report_drawing.py <reports/qNN_<topic>/>`.


What the drawing holds
----------------------

The first row holds the current relationship and interaction proposal. The existing screen
prototypes stay as reference; the proposed linked panel has not been implemented in the server.

```text
6 · Studio item, frames and Questions   one sNN item has N frames; n primary frames each anchor qNN
7 · Linked Studio and Report panels    one workspace, two linked panels; on-disk sources (UI proposal)
8 · From exploration to an answer      promote a question, develop a partial answer, review source changes
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


Decided
-------

s04-D07 · A row/folder `sNN-<topic>/` is called a **Studio item**. Idea Studio is the view;
    a Studio item is a broad topic containing drawings, each with named frames (JL 261009-261010).
s04-D08 · One Studio item may have N frames, and only n of N need Question links. The default
    is one primary frame per Question; exploratory/background frames can stay without a
    Question and may be cited as supporting frames. A frame is the visual source, not the
    Question object itself (JL 261009-261010).
s04-D09 · Keep `qNN` for the Question and its answering Report, which share one identity.
    Keep `rNN` for computational Runs. A Report can hold an open or partial current answer;
    its figure is generated from selected Studio frames (JL 261010, accepted naming proposal).

The shared relationship is owned here: `b03_project_workbench/studio/s04-studio-and-report/`,
at Block level. CoWork and other themes use the same contract. No new Job is needed to draw
and discuss it; an implementation Job can be scoped later against Q09 if needed.

Interaction proposal (261010)
----------------------------

Two linked panels on the same work page: Studio canvas at left, collapsible Question/Report
at right. Selecting a frame opens its qNN; selecting qNN locates its primary source frame.
Keep the viewport and selection when switching. New frames can remain exploratory. Keep
one session as a pass of `run-draw-sNN`; the panel does not create a second session log.
The Report panel presents Answer, Evidence, Limits and Next, plus a source link. Its figure
comes from the source canvas, with no independently edited second copy. Source changes
should flag a Report for review before changing an accepted answer. These are UI proposals,
not server behavior delivered by this drawing update.


Earlier proposals
-----------------

s04-D01 · Proposed (261007): the studio makes, the report shows. A studio topic holds many rough
    drawings that a person edits freely; a report holds one drawing, generated.
    Refined by D07-D09: Studio item contains frames; a Report may still have a partial answer.
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
7. Q09: store a durable frame ID alongside its readable name, or cite by name only? How do
   renamed, split or merged frames preserve the primary Question link?
8. Q09: how should selection, viewport and open text edits survive panel switching, and what
   exact source changes should mark a Report as needing review?
