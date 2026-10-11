s02 · Workbench shared
======================

Was b03's s08, then b02's s01, then b03's s07; s02 since the renumbering (261007), as the workbench topic of this Block.

**Tags:** `Structure` · `UI`

**Topic:** what `Tools/plugins/haipipe-toolkit/servers/workbench` holds today, how every
other workbench leans on it, and how it owns the Block / Job / Task frame. The current model keeps sNN topics only
at Block level, constructs Jobs from those topics, and separates Studio from Audience
Report (261010). Earlier framing (JL 261007:
"should it propose the structure of board, job, and tasks? ... what are their relationship to the
workbench shared?").

**Feeds:** `q07_workbench_mapping` · `q08_workbench_base` · `q09_studio_report_on_screen`

**Source:** the reference grid is read off each workbench's own Python every build (an
import or link of a shared part; its own stylesheet), so it shows what the code does now. The Space
rows come from `../s01-overall-tree-structure/level_views.py` (`SERVER`, read from the server code).


Files
-----

```text
s02-workbench-shared/
├── s02-workbench-shared.md            this notes file
├── build_s02_workbench_shared.py      the builder; marks are kept on rebuild
├── s02-workbench-shared.excalidraw    the drawing
├── s02-workbench-shared.png           its rebuilt preview
└── .s02-workbench-shared.seed.json     generated snapshot for preserving marks
```


What the drawing says
---------------------

Three discussion frames lead in one row (261010), sized to read as whole frames:

1. **Shared workbench across levels** (Q08): Guide · Studio | Block · Job · Task at the
   top. Studio opens a shared view like Guide: only Studio is selected, and the work Space
   and subspace rows are absent. Block, Job and Task open the same Block-owned topics,
   Disk and topic sessions. The title says Workbench · Studio · bNN · Block name; the work
   level stays in the controls. Inside Guide, Index comes before Description and returns
   to the SPACE's studio index. Below the Studio title,
   Current, topic tags and All focus the list; drag a card into Current or use its button.
   Each row shows its tags and source. Clicking that level returns to its selected work Space and view
   (implemented 261010).
2. **Block topics construct Jobs** (Q07): an sNN topic holds ideas, choices and the agreed
   plan. Construct a Job from that plan, keeping its jNN identity and a link back to the
   Block topic. A topic may lead to zero, one or several Jobs. Jobs hold their goal, close
   and Tasks; actual Runs execute the work and produce evidence.
3. **Studio and Report** (Q09): a shared Studio view and a separate work Space. Studio holds
   working drawings, alternatives, decisions and topic sessions; Report shows
   Question / supporting work / Report. Open a Report in its Space, or open a source topic
   back in Studio. One topic may feed several Reports, and a Report may use several topics.

These ownership and view rules are approved for the blueprint (261010). Shared Studio,
its single selected top entry, hidden work rows, Block-owned topics, Disk, session history
and new-topic prompts are implemented in the live shared frame (261010). The same shared
view opens from Block, Job and Task. `studio=1` keeps the work path, Space and subspace for
return; older `space=Idea Studio` links also open shared Studio.
Each sNN source is `bNN_<block>/studio/sNN-<topic>/`. A Job's own plan, Tasks and execution
history remain in its Job folder. Topic-to-Job construction, linked-topic filtering and
migration of existing local Studios remain proposed; existing local files have not moved.
The shared list now includes those local topics by reference, with their source shown (D13).
Report ownership is a separate rule; the blueprint makes sNN topics Block-only.
The topic-to-Job link's stored field, migration of existing local Studios and topic / canvas return behavior
remain open below. `s04-studio-and-report` is earlier background and needs the same rule
when its own blueprint is revised.

The eight reference frames keep their names and positions below the discussion row.
Their shared-base table shows Job / Task links to Block topics and separate Studio / Report
columns. The screen references now show five lower buttons in work mode and no work rows in Studio;
dated green notes mark the changes. Code-backed references show current server code.
The following notes record the earlier discussion. New material uses black lines,
red open questions and green change notes.

1. Today every workbench draws its own page (header, band, Space row, stylesheet) and borrows a few
   parts: Guide (all eight), Studio (all but labeling), the Runs panel (all eight, but it lives in
   workbench-page), the BJTR tree (paper only), Related Papers (insight, design).
1b. The servers/ tree (JL 261007: "the tree-structure, like draw"): today's tree read off the disk,
   beside the proposed one: `workbench/frame/` (levels, spaces, qwr, one css) new,
   `runs_panel.py` moved in from workbench-page, one `spaces()` adapter per family (task first),
   workbench-page at Task level only, and a `workbench` skill to pair with the server (?).
2. Each workbench names its own Spaces, at one level: a Block (task, discovery, cowork, paper,
   insight, design board, labeling board) or one Page (page, design page, labeling page). No
   workbench has a Job level.
3. Proposed: workbench owns the frame (level tabs, the six Spaces and their dividers, the
   third row, Studio, the Runs panel, Report's Question │ Work │ Report, the BJTR tree,
   Guide, one look); a family hands it, per level, its Spaces' subspaces, content and run types.
3b. The base and a theme (JL 261007: "in the shared, the structure of the board-level, job-level
   and task-level; the workbench-xxx just gives the themes"): workbench holds Block · Job ·
   Task × the six Spaces, each cell what it reads by default from the standard folders, so a theme
   with nothing special works as is. A theme, one per Theme of the Project, is `theme.py`
   (declared: level names, which levels, subspaces, extra fields, run types, Guide) plus optional
   `views/` (code, where one Space needs its own body). Filled in: task (config only), paper
   (config + a Story view ?), page (Task only; config + its outline, evidence and export code).
   A theme may not change the levels, the six Spaces or their order, draw tab rows or carry CSS.
4. Steps: move `runs_panel.py` to shared; build the frame and move one family (task, Block level);
   the rest follow as s11 · s12 · s13 settle; old routes stay meanwhile.

5. On screen (JL 261007: "I want the real ui, just like the s04"), two frames on the right, drawn
   the s04 way: "the base, at Block, Job and Task", one full screen per level opening the Space
   that holds its children or its Runs (Block › Work Details: its Jobs; Job › Work Details: its
   Tasks; Task › Runs: its Runs), an "on disk" tree under each naming the folders it reads and the
   base files that draw it (frame.py, frame_view.py, runs_panel.py, work_items.py ?), and a Run
   pop-out; then "a theme on the base", the same Block screen under the work theme and the paper
   theme: the same frame, its own level names, third row and rows, and the theme file behind it.

6. Done (261007, JL: "add the disks as well, to show what files are associated with the content in
   the screen ... so we have both disks and runs"): the right column holds a Disk box above the
   Runs panel. It lists what the open Space reads, under the open folder, each path with what it
   feeds on screen; a glob says how many it finds, what is not there yet is greyed, a .md links
   to the reader. The base fills it per Space (`frame.vanilla_disk`); an open Page view brings its
   own (`PAGE_VIEW_DISK`); a theme sets `Space(disk=...)` per subspace, so the box always names
   what that view really reads. The live twin of the "on disk" trees under each screen here.

Decided
-------

s02-D01 · Three large discussion frames lead the shared workbench drawing; their Questions
    are Q08, Q07 and Q09 (drawing plan approved 261010; current model revised 261010).
s02-D02 · The eight existing reference frames keep their names and positions. The builder
    writes through the Studio writer so existing marks survive a rebuild (261010).
s02-D03 · sNN identifies a topic only at the Block level. The Block owns ideation, topic
    notes, drawings and topic sessions; Jobs and Tasks do not create a local sNN namespace
    (261010, requested by the user).
s02-D04 · Jobs are constructed from an agreed topic plan and linked back to that Block
    topic. sNN and jNN remain separate names. A topic can stay exploratory or lead to more
    than one Job (261010).
s02-D05 · Idea Studio and Audience Report are separate Spaces with separate purposes:
    working ideas and plans versus Questions, supporting work and audience-facing answers.
    Source and Report links connect them; a Report panel is not embedded in the Studio
    proposal (261010).
s02-D06 · A Job's or Task's Idea Studio view opens related Block topics by reference.
    The source and topic history remain at the Block. Report ownership is decided separately
    from the Block-only sNN rule (261010).
s02-D07 · Idea Studio has one main entry immediately after Guide and before Block in the
    shared live header, with a divider before the work levels. Its second-row button is removed.
    The Block control shows its bNN tag, including at Job / Task level and while Guide is open.
    Existing Space routes and contents are kept; topic linking and migration remain separate
    work (261010, requested and implemented).

s02-D08 · The visible Idea Studio label is shortened to Studio; the top Block button says
    Block without its bNN tag. The page title keeps the Block context at every level and
    while Guide is open. This updates D07's button labels; existing `space=Idea Studio`
    links and contents remain supported (261010, requested and implemented).

s02-D09 · Studio is a shared view like Guide, accessible from Block, Job and Task. Only
    Studio is selected; the work Space and subspace rows are absent. Topics, Disk, topic
    sessions and new-topic prompts all use the owning Block. The work path, Space and
    subspace stay available for return through the level controls. Existing Studio URLs
    remain supported. This completes D06's shared source behavior; topic-to-Job construction,
    linked-topic filtering and migration of existing local Studios remain separate work
    (261010, requested and implemented).

s02-D10 · The visible Audience Report button is shortened to Report. Existing
    `space=Audience Report` links, theme adapters and report contents keep working
    (261010, requested and implemented).

s02-D11 · Studio's title shows the owning Block's tag and full name at Block, Job and Task
    level. Index sits before Guide and returns to the studio index; its destination is a
    host setting, defaulting to this SPACE. Each topic records one or more explicit Tags
    in its notes. The shared list shows tag badges and All / tag buttons with topic counts.
    Filtering changes the view, keeps the sNN identity and Block ownership, and stores
    the selected tag in the URL. Topics without tags remain visible in All and Untagged;
    a direct topic link can reveal its row across a filter. For b03 the first tags are
    Structure, Workflow, UI, Guide and Server (261010, requested and implemented).

s02-D12 · Index moves from the top navigation into Guide's own button row, before
    Description, Method, RoadMap Draw and Related Paper. The top row is Guide · Studio |
    Block · Job · Task. Index remains a link to the configured SPACE studio overview and
    leaves the whole workbench rather than opening inside Guide's iframe. This updates
    D11's placement; the Studio title, tags and Block ownership stay the same
    (261010, requested and implemented).

s02-D13 · An sNN stays one topic; a group holds references to topics. Current is the
    first group, type/tag groups follow, and All is last. Drag a card by its handle into
    Current, or use Add to Current / Remove from Current. This first version saves the
    Current selection in this browser per Block, shared across Block / Job / Task views;
    it does not sync between people, browsers or machines. Existing Job / Task topics are
    included with their source labels and a Source picker while file migration remains
    open. Repeated sNN names keep separate source-qualified references and anchors.
    New topics still belong to the Block; grouping changes membership only. The SPACE
    index counts the same shared list (261010, requested and implemented).

Open
----

1. How do existing Job and Task Studios move into the Block without losing names, marks,
   session history or incoming links?
2. Where is the durable source-topic link stored on a Job face, and how does the topic list
   discover its linked Jobs?
3. When constructing a Job, how are goal, close and Task slots taken from the agreed plan?
4. How do topic and frame links survive a topic or frame being renamed, split or merged?
5. How does moving between the separate Spaces restore the topic, Job filter and canvas position?
6. When a cited frame changes, how should its Report request review before the accepted answer changes?

7. A `workbench` skill to match the server (the frame contract), as workbench-page and
   workbench-paper have theirs?
8. Insight fits the frame (its session's answer, 261007): partitions are Audience Report's third row,
   the DIKW levels are Jobs, its Insight table is Question / Work / Report, and its question map is a
   generated, view-only Idea Studio row. Still open: its Check (a question's gates) has no Space;
   proposed as chips on each question row.
9. Labeling (own host, own write door): a family's own body inside a Space?
10. The paper's Job tab: workbench-paper as the version Job (s12).
11. The shared README's Space order gives way to the six Spaces.
12. Write the contract now; code it once s12 and s13 settle.

(write here, or mark the drawing in red)
