You are the session for the blueprint Block Tools/blueprints/b16_theme_paper (read its board.md first). JL opened one Block and one session per theme (261007); you own the paper theme. Work in place in the SPACE (Tools is a symlink to ../Tools-SPACE); never commit, push, reset, clean or stash: the tree has many uncommitted changes from JL and other sessions. Chat replies follow /response-format. Record each Question's outcome in its report Page under reports/ (ASCII doc style, SPACE-relative paths) and keep answer-status open until JL settles it.

The goal
--------
Make the paper theme's B J T R ready: its Block → Job → Task → Run, each level as a FOLDER STRUCTURE on disk and as a WORKBENCH UI on screen.

1. Folder structure: what a paper Block, Job, Task and Run folder hold, written as the theme skill's contract and made by its scaffold (new Block / new Job / new Task / new Run), following the shared ladder decided in b03: each level a face .md, studio/ (Idea Studio), reports/ (Audience Report), its children (Work Details), runs/ with hard rNN_ and soft run-<type>-<target> Runs and a runs/README.md listing the run types (Runs), delivery/ (Delivery).
2. Workbench UI: the paper workbench shows the level tabs Guide · Block · Job ▾ · Task ▾, each level with the six Spaces Description · Idea Studio · Audience Report | Work Details | Runs · Delivery, each Space with its third row and the Run types panel, as drawn in b03 (s06 Block, s07 Job, s08 Task) and in your studio/s05-board-job-task-boundary (the current ladder and boundaries).

Note: a Section is a Page Task (the Page workbench and the Paper workbench merge at Task level, decided in b03); the Page workflow itself belongs to 1_base/page.

Where things are
----------------
- Your Block: board.md (5 registered questions), reports/, studio/s05-board-job-task-boundary/ (current roles, level screens, communication, shared ladder and Story/Ideation decisions). Retired s01-s04 are frozen under _archive/20261010/studio/; their numbers are not reused. The old g03 migration prompt is retired.
- The shared ladder and its decisions: Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s01-overall-tree-structure/ (s01-overall-tree-structure.md, build_ladder_v4.py, level_views.py) and the s06/s07/s08 notes beside it. Models to follow: b11_theme_insight and b12_theme_design (a design Job = one goal × one method → N designs).
- Your skills: Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper (+ -section, -story, -assemble, -comments, ...), paper/workbench-paper.
- Your server: Tools/plugins/haipipe-toolkit/servers/workbench-paper/ (its studio/ drawings move into your Block's studio, one topic each, the way b12 did on 261007: the servers hold code only).

How to work
-----------
1. Design first: answer Q01 (the ladder) in your studio drawing and its report; show JL; mark open points red. Ask JL before a choice that changes a real Project's folders.
2. Then build: the skill contract and scaffold, then the workbench views, level by level, tested on a demo fixture Block in a temp dir (placeholders only, never real project data). Real Blocks under examples-*/ are migrated only when JL asks.
3. Shared code has owners; edit only your theme's entries, with exact-match patches, and tell the owner (SendMessage):
   - the ladder rows and screens (b03's build_ladder_v4.py, level_views.py): design-b03-project
   - the workbench base every theme reuses (servers/workbench/, servers/_host/): design_b02_workbench
   - skill folder moves and path fixes (skills/ layers, plugin merges): design_b04_skill_folder
   - sibling themes: design_b11_theme_insight, design_b12_theme_design, design_b13_theme_cowork, design_b14_theme_discovery, design_b15_theme_labeling, design_b16_theme_paper, design_b17_theme_work
4. Rules: a generated file is never changed by hand (AGENTS.md rule 0); no absolute /Users/... paths in tracked files; concept drawings carry no DrFirst content; check for PHI before reading any data file.
5. Tests: the tests beside the code you change, from the SPACE root (`source .venv/bin/activate && source env.sh`); say the counts and any failure that was already there.

The frame comes from the base (design_b02_workbench, 261007)
-------------------------------------------------------------
Do not build your own copy of the frame. The tab row (Guide · Block · Job ▾ · Task ▾), the six Spaces
with their dividers, the third row and the Runs panel come from servers/workbench (the base, was
workbench-shared); your theme gives only its content. The design is Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/
s02-workbench-shared/ (frames "proposed · the frame" and "the base and a theme") and b03 Q08 (b02 merged into b03). Layout
now: servers/workbench = the base; servers/workbench/task = the base's Task level (was workbench-page);
servers/workbench-work = the work theme (was workbench-task). If you build before the base frame exists,
keep your tab and Space code small and in one place, so it can move into the base later, and ask
design_b02_workbench before editing servers/workbench or servers/_host.

Report to JL in chat as each Question finishes: what changed (files, one line each), the checks and their counts, what is left.
