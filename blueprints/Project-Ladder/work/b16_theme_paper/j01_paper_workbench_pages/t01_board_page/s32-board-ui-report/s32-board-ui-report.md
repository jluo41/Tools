s32 · Board UI: Report
======================

**Tags:** `Block UI`

**Stage:** agreed

**For:** a deck, and the paper Board's Report screen on the focus page (`delivery/ui/board-report`), for the people who build the workbench

**Delivery type:** ui

**Covers:** the Board's Report: seven views, A Idea · B Story (Venue inside it) · C Data flow · D Paper flow · E Support blocks · F Evidence · G Writing, each in two bands, RESULTS first (the view's own sections), then PROCESS (Interactions, then its to-dos); the drawing and the mind map at the bottom.

**Excluded:** the other eight cells of the 3 × 3 (j01's other sNN); the draft Task page itself (b32-s42:draft @ draft_task_focus_page).

**Topic:** The Board's Report: the paper's four layers as views, Idea to Writing; one cell of the paper's 3 × 3, the paper Board × Report (check) (JL 261031: "we have the board, then job of the
paper version, and task of the section draft, I think it should be 3 x 3"). Its drawing is haipipe-studio's five parts,
drawn by `build_s32_board_ui_report.py` through j01's `paper_ui_cells.py`; its Design is the screen as proposed
(A) and what it leans on (B). Names are placeholders: the papers are unpublished, and Tools is public.

**Feeds:** `reports/` q01_paper_ladder


Files
-----

```text
s32-board-ui-report/
├── s32-board-ui-report.md            this face
├── build_s32_board_ui_report.py      the builder (../../paper_ui_cells.py draws it)
├── s32-board-ui-report.excalidraw    the five parts: Idea · Now · Design · Process · Delivery
├── s32-board-ui-report.png           its card
└── delivery/ui/                     the agreed screens, A to G
```


Decided
-------

s32-D01 · The Board's Report opens on the MindMap, not Findings (JL 261031, r01_collect_board_ui_report Q1: B, changed from my pick A).

s32-D02 · The Board's Report has two views, MindMap and Versions; Findings, Status and Questions are dropped (JL 261031, r04_collect_board_report_views Q1: A). Versions says where each send stands (venue, send, round); Work › Job-Versions says what waits (Q2: A). (superseded by s32-D12)

s32-D03 · Each Versions row carries PDF and Word buttons that open that version's latest build in the pop-out, so a version's delivery is checked in one click (JL 261031, r04 Q2 note: "How to make the version of the j01_xx, or j02 etc, to check their dleivery very quickly").


s32-D04 · The Board's Report shows the paper's own parts first, one view each: Idea, Story, Venue, Data flow, Paper flow, Related work (JL 261031: "for the report, I think we should have the things like the idea, the story, the venue, and the data flow, and the paper flow, etc."). Each view is that topic's line, its drawing and its face's parts; Venue is venues/<venue>/call.md and the Story's venue comparison. MindMap, Status, Findings and Questions follow for now (this replaces s32-D02's two views); Versions stay in Work › Job-Versions. Live: focus_draft.board_report_views. (superseded by s32-D12)

s32-D05 · Venue and Related work are one view, and Status, Findings and Questions go: the Report is Idea · Story · Venue · Data flow · Paper flow · MindMap (JL 261031: "I think venue and related work should be together, right? and we don't need to have the status, findings or questions, no need to use them anymore"). Venue holds the desk rules, the ladder of journals, then the venue's related work (the s10 topic); a Board with no venues/ says no desk record exists yet. (superseded by s32-D12)

s32-D06 · The mind map and Interactions are sections inside each part's view, not views of their own: Report and Work list Idea · Story · Venue · Data flow · Paper flow · Draft (JL 261031: "I think the interaction and MindMap should be something like the sections under the view"). Recorded: runs/r05_collect_board_ui_report_decisions. (superseded by s32-D22)

s32-D07 · The Board's views follow the paper's four layers: Idea, Story, Venue, Data flow, Paper flow (plan), Explore (the work Blocks, internal, and the discovery Blocks, external, that this paper draws on, read from the paths its pages name), Evidence, Writing (JL 261031: "one paper's studio should be \"explore blocks\" this will be one of the view as well, which indicate what are the work blocks and what are the citation blocks will be used to support this work"). Live: focus_draft.explore_html. Recorded: t01 runs/r05_collect_board_ui_report_decisions.

s32-D08 · The Explore view is named Support blocks: the work Blocks (internal exploration, the analysis) and discovery Blocks that support this paper (JL 261031, b16 runs/r02_collect_paper_jobs Q1: "This should be in the support-blocks in the View.")

s32-D09 · The eight views are lettered A to H (A Idea, B Story, C Venue, D Data flow, E Paper flow, F Support blocks, G Evidence, H Writing) and settled one round each; the same letter names the small screen in the drawing, its decision here and its file in delivery/ui/board-report/ (JL 261031: "we might want to update them one by one, right? ... I think you should have the A, B, C, D"). (superseded by s32-D12)

s32-D10 · A · Idea opens answer first: 1 · Direction, then 🙋 Interactions only when one waits, then the drawing and the mind map, then 2 · Directions considered and 3 · Hand-off, the answered forms last (JL 261031: "do you think we should put the Direction to the top?"; "yes, please update them accordingly"). Live: focus_draft.ANSWER_FIRST. (superseded by s32-D14)

s32-D11 · The delivery is one ui delivery with two targets: delivery/ui/board-report/ (A to H, built into servers/workbench-paper/) and delivery/skill/board-report-views.md (the views' manual, rendered into workbench-paper/SKILL.md); render.yaml lists both (JL 261031: "this should be reconsidered as well, like we should have the skill folder and workbench folder as well").

s32-D12 · Venue is merged into Story, so the views are seven, A to G (A Idea, B Story, C Data flow, D Paper flow, E Support blocks, F Evidence, G Writing); each journal is a tab in Story's 4 · Venues, its related papers inside it (JL 261031: "I want to merge the venue to the story"; "the journal can serve the same ... merge the 4 and 5 together").

s32-D13 · Every view's shape: numbered heading bars with one emoji each, in reading order; the main point large under section 1, no coloured edge; content shown as tiles, tabs or a chain; the helpers (🙋 Interactions, 🖼️ The drawing, 🧠 The mind map) at the bottom after a dashed line (JL 261031: "I still want each section to be the [heading bar] ... seems to be ordered"; "at the bottom, we should check the Interaction, Draw"; "I don't want to have this" of the edge).

s32-D14 · A · Idea passed the design loop: drawing review/A-s1-r02.md (8.7), live page review/A-s2-r04.md (8.5); live in focus_draft.idea_view. It replaces s32-D10's order.

s32-D15 · Cards that hold more than their line are card tabs, the open card's detail in a panel below; joined by arrows, a card-tab chain (JL 261031: "what is the name for this structure?"; "we will use the cards-tab"). A's directions considered became card tabs (JL 261031: "could you make it the same to [the Questions]").

s32-D16 · C to G take the same shape (JL 261031: "Please go ahead to update other views as well"): C · Data flow (1 Flow with its drawing, 2 Questions to Runs, 3 Waits on (moved to PROCESS by s32-D22)), D · Paper flow (1 Send, 2 Sections, 3 Displays, 4 Timeline), E · Support blocks (1 Work Blocks, 2 Discovery Blocks), F · Evidence (1 Displays, 2 Values, 3 Citations), G · Writing (one section per version, its Sections as card tabs, then the assembled paper). Live in focus_draft.dataflow_view to writing_view; their review rounds are in review/.

s32-D17 · C · Data flow leads with the map of how the data come together: the data, the linking, the tables, the questions, joined by lines, read from the data-flow topic's own `<topic>-drawing.yaml`; its drawing moves to the helpers (JL 261101: "for the data flow, we should focus on the mindmap, show the mind map of how these data are collected together"). F · Evidence reads Values, Citations, then Displays, with all displays as one PDF (JL 261101).

s32-D18 · C · Data flow has no mind-map helper: its Flow map is the mind map (JL 261101: "I think the mind map here is the Flow, right?"). E · Support blocks is two sections, 1 · Work and 2 · Discovery, each a folder tree of only what this paper uses, one tree per Project (the paper's own and any other it names, as Project-Example-B bNN_<block>): work/ or discovery/, then each Block, Job and Task its pages name by path or by address (bNN.jNN.tNN), one line each, each a link (JL 261101: "more like the folder tree, only show the related folder tree"; "we will have both the work and discovery, as two sections"; "we can have the works from multiple projects").

s32-D19 · Report is for reading, so F · Evidence and G · Writing use side tabs: the items as a list on the left (each Section, value set, citation set, display), the open one's content on the right to read; G's panel is the Section's text itself, not its step words (JL 261101: "we just report the report"; "in the left there is a panel, and we can read the content quickly").

s32-D20 · G's assembled paper is side tabs too: each output on the left (the paper as LaTeX builds it, as Word prints it, the Word supplement, then each earlier round), the open one shown on the right as its PDF, page by page, with Open the PDF and Open the Word file (JL 261101: "should we show it as well? like different versions of the output with the left panel?"). The PDF is a large view, so a "⤢ Pop out" button above it opens it over the page at full size and closes back to the same place (JL 261101: "we want to make the things to be pop out as well").

s32-D21 · All seven views pass the live design loop (stage 2): A Idea A-s2-r05 (9.5), B Story B-s2-r06 (8.1), C Data flow C-s2-r03 (8.6), D Paper flow D-s2-r03 (8.5), E Support blocks E-s2-r04 (8.5), F Evidence F-s2-r03 (8.3), G Writing G-s2-r03 (8.75). Round 2 failed C to G on Phone alone: the phone rules sat before the base rules they change, so the base rules won; they now come last in focus_draft.PB_CSS. E marks the Job the paper's pages name most as its "main analysis" and shows only the words that set sibling Tasks apart.

s32-D22 · Every view is two bands, RESULTS and PROCESS, each numbered from 1: RESULTS is the view's own sections (as s32-D21 passed them), PROCESS is how the layer is being made: 1 · 🙋 Interactions (what was decided, each answered form), 2 · 🚧 Open (Evidence: 📋 Where each stands; Writing: 🪜 Steps); Report reads RESULTS first. Data flow's Waits on moves into PROCESS as Open. The drawing and the mind map stay at the bottom after the dashed rule (JL 261101: "the index for each section should be 1, 2, ... 1, 2, 3"; "the results should be consistent to the report"). Live: focus_draft.banded, process_html.

s32-D23 · Report's PROCESS uses the same rows as Work's (s33-D06), read side: 1 · 🙋 N decisions made, one row per answered question with its pick and a green Answered pill; 2 the same to-dos with their pills (JL 261101).

s32-D24 · The Report is agreed, all seven views A to G, and handed over: the agreed screens in delivery/ui/board-report/ (written by paper_ui_cells.py from AGREED), the views' manual in delivery/skill/board-report-views.md, rendered into workbench-paper/SKILL.md; the code lives in workbench-paper's board_views.py, board_results.py, board_process.py, board_read.py and the shared servers/workbench/ui_parts.py, split out of focus_draft.py (JL 261101: "s32 is very good now"; "for the blocks I think they are good to go"; "try to split them").

s32-D25 · Report's Data flow PROCESS shows the same plan rows as Work's (s33-D07), read side: each step with Open, the skill to use and Copy prompt. A PROCESS title names the step and carries no count (JL's rule "labels carry no counts", decided 261101): the code no longer shows "7 decisions" or "5 of 9 open".

Open
----

(none)

(write here, or mark the drawing in red)
