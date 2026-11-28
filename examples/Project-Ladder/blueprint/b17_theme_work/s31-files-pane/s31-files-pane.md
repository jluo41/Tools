s31 · UI Plugin: Files
======================
view: overview
emoji: 🗂️

**Tags:** `All pages`

**Stage:** shaping

**For:** the right-hand Files pane every work page shares (Block, Job, Task), as screen previews in `delivery/ui/`, for JL to decide and for the workbench code (`servers/workbench/side_pane/files_tree/trace_view.py`, `work_files.py`, `file_info.py`)

**Delivery type:** ui

**Covers:** the one Files tree and its parts by role (Block, Maintain: kind, Read-From, Touch); the marks a trace puts on its files; the effects; the right-click card; the Timeline of traces

**Excluded:** the page frame and the sections menu (s04-discovery-structure); what a trace file holds (hai-ui A07); the Job and Studio split (hai-block A06)

**Why:** when work is going on, can a reader see on the file tree which files it plans to change, is changing, and has changed?

**Topic:** a trace (`trace/<YYMMDD>/<HHMM>_<slug>.md`) is one piece of work with its plan written first. JL wants that plan and its progress visible where the files are, not in a separate view, so a change can be checked before it is confirmed. The code is built under `../j03_work_workbench_pages/t04_shared_parts/`, one trace per change, each naming this topic (`topic: s31-files-pane`).

**Feeds:** none


Files
-----

```text
s31-files-pane/
├── s31-files-pane.md              this face
├── s31-files-pane.mindmap.md      its mind map
├── s31-files-pane.excalidraw      quick drawing
└── delivery/ui/
    ├── files-trace-view.html      the first trace tree preview
    └── files-trace-effects.html   marks, effects, extends-into line, right-click card
```


Decided
-------

- s31-D01 · One tree; the traces mark their files on it, no Files/Timeline switch (JL 261125: "I just want one UI of this, and everytime, I work on a trace, the related files will be flagged")
- s31-D02 · Marks: ◌ planned, ◐ editing, ●✓ closed but not committed, ◆ changed but not in the plan, • committed (JL 261125: "so we can have the files to be flag like before, during, and after")
- s31-D03 · A file still to create is a `+` row in grey italic, slowly fading; no striped box (JL 261125: "I wnat to change this effect")
- s31-D04 · A file being changed has a light sweeping across it; no orange bar on the left (JL 261125: "and remove" the bar)
- s31-D05 · UI and Skills sit under an "extends into" line: what the Block reaches out to (JL 261125: "what I mean is more like the extension")
- s31-D06 · What a file or folder is shows on a right-click card (Open, Copy path), never on hover and never as grey text on its row (JL 261125: "you right click it, show the informaiton, and I don't want to hover")
- s31-D07 · Many traces live on a Timeline (a row per file, a column per trace, a click opens the trace), behind a button (JL 261125: "the x row is the timeline, the each rwo is the file, and the dots will be the trace")
- s31-D08 · Icons come from `file_icons.py`, in previews too; `.py` is Python's own mark (JL 261125: "I think the python icon is not this icon, right")
- s31-D09 · The things to change show in the Files tree before JL confirms them (JL 261125: "I hope next time, the things to change will be shown in" the tree)
- s31-D10 · An open trace opens the tree down to every file it plans, without a click (JL 261125: "if they are about to be changed by this plan, could you explan and show them?")
- s31-D11 · A planned file outside Block, UI and Skills shows under Also touched, by its full path (same request)
- s31-D12 · One Trace button replaces the chips and the Timeline window: it lights up one trace's files, opens the tree down to them and dims the rest, never hiding a row (JL 261125: "can have a trace mode to replace [the ⊞], and click it, and we can show which files will be infleunces by the current trace"; "why I find many details are gone")
- s31-D13 · A trace is picked by a click (a trace file, or a time or station on the metro), no dropdown; its aim stays beside Trace; a small one-line-one-station icon shows or hides the metro (JL 261125: "we can just clikc and select, we can drop [the dropdown] and keep [the aim]"; "we might also have an icon to hide or show the metro map"; "maybe a btter icon? this is too complicated")
- s31-D14 · The real Files pane carries the metro map beside the tree, as the Metro map preview; Trace is the highlighter icon, the metro's show or hide is the branching line (JL 261125: "I want this [C Highlighter] and this [D Branching line]"; "where is the metro map?")
- s31-D15 · Picking a trace opens its card under the top row (title and time, the whole aim, prompts with "more", Check, Summary, Open); it folds to one line and stays at the top (JL 261125: "I cannot see the content of the trace, when I select one")
- s31-D16 · Folder scope: what the page owns decides which parts show, where a file lives decides where it sits. Block, Support, Code (the page's own servers and page spec), Skills (the page's own skills); a traced file inside them sits there, every other traced file (another server, another skill, AGENTS.md) is Also touched (JL 261125: "how do we handle the folder scope, right? this is also an important topic"; JL 261126: "these two will also be the also touched, can you remove them out?")
- s31-D17 · Every Block's Files pane has the trace bar; a trace kept in another Block that planned or changed this Block's files joins its metro and marks only this Block's files; with no trace at all the bar stays, greyed (JL 261126: "for this, why I cannot see [the trace bar]")

- s31-D18 · A part is named by its role, never by a number that runs down the page: Block (where the work is, no number), Maintain N (a folder the Block changes and keeps: Code, Skills, OneDrive), ReadFrom N (a folder it only reads: a Block it waits for, an example Block), Touch N (a folder a trace touched outside them). A role is one part with its name once; inside it one folder is one row, numbered within the role (so "Maintain 2" is row 2 under Maintain), and a path line opens each run of rows that share a parent folder (JL 261127: "this looks too sparse"); the "extends into" line (s31-D05) and Also touched (s31-D11) are these roles now (JL 261127: "they should not be order with 2, 3, 4"; "Maintain 1, Maint 2 ... Readfrom 1, ReadFrom 2 ... Touch 1, Touch 2")
- s31-D19 · Withdrawn: a Maintain row shows its folder only. The Job and Studio codes at the end of a row (`j12 s31`, `+N`) and the code that computed them are gone (JL 261127: "I want to drop them")
- s31-D20 · The role is written Read-From: what the Block does not change (sources, supporting Blocks, data). Read-From and Maintain each show one path line, the folder all their rows share, and a row that sits deeper is named by its path below it (`cowork/b01_example_cowork`, `skills/0_utils/hai-trace`); this replaces the path line per parent folder of s31-D18 (JL 261127: "why not Read-From?"; "READ-FROM is more like somethings we will not change, like the sources, supporting blocks, and the things like data"; "I think we will main taim as well")
- s31-D21 · Read-From also lists the Block's data: each store of its board.md `## Data` list whose `where:` is a folder of the SPACE (`_WorkSpace/2-RecStore/cohort_a`). The face gets no new line: the Data list already says where the data is; a catalog or a share has no folder and shows only in Findings (JL 261127: "READ-FROM is more like somethings we will not change, like the sources, supporting blocks, and the things like data")
- s31-D22 · What the Block maintains is one part per kind, each numbering its own rows: Maintain: ServerUI (server code and page spec), Maintain: Skills, Maintain: Block-Example (the example Blocks of `examples:`, which leave Read-From), Maintain: Blueprint Blocks (for a blueprint Block, the other Blocks of its `blueprint/` folder that its traces planned or changed, one row per Block, their files marked in place instead of listed under Touch) and Maintain: OneDrive. Read-From keeps the Blocks it waits for and the data (JL 261127: "this is also the main, right? I will call it Maintain: Block-Exmaple"; "split them into two: and call it Maintain: ServerUI and Maintain: Skills"; "we can have Maintain: Blueprint Blocks")
- s31-D23 · Touch shows each touched file inside its real folders, opened down to it, under the numbered path line; a run of folders that each hold one folder is one row (`draft/hai-draft`), and a file still to create keeps one row by its path (JL 261127: "why for this, we do no organize them with the folders as well?")

Open
----

1. (answered by s31-D12: no Timeline window; the metro map in the tree is plan 1543, on hold)
2. A file two open traces both plan: one mark (the stronger), or both?
