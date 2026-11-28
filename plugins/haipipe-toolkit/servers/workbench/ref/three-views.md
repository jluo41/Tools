# Three views: Folder, Element, Session

Every theme describes its work three ways, and the three point at each other (JL 261117):

- **Folder**: how the work is stored on disk (Block, Job, Task, Run, and the files in them).
- **Element**: how a workbench page shows those folders (view, section, row, card, tab).
- **Session**: the important history of the chat sessions that changed them, cut into episodes, each episode
  naming the folders and elements it touched.

From any one of them a reader reaches the other two: from a folder, the page parts that draw it; from a page part,
the episodes that changed it; from an episode, the folders it wrote and where they show.

This contract was merged from the six theme sessions' maps (Insight, Labeling, Design, Work, Paper, Project). The
shared part is built once in `servers/workbench/page`; each theme only fills a hook (§ 6).

## 1. Keys

Two keys join the views. Never invent a third.

| Key | Names | Example |
| --- | --- | --- |
| path | a folder or file, relative to the SPACE root | `paper/Paper-X/j02_writing_v1115_jama/t02_methods/draft/` |
| card address | an item inside a page, as `ref/cards.md` § 3 defines it | `j02.t01.r05`, `C3.P5.s14`, `ex-26`, `r1.2`, `K01.age65` |

- The path is SPACE-relative, not Block-relative: one episode often writes two Blocks (an Insight Question Book and
  its Board, a Design Method Book and its Board), the Project level sits above any Block, and Board sessions also
  edit `Tools/` (skills, servers). A Block-relative path falls out of the SPACE-relative one.
- Items that live inside a file (a sentence, a labeled item, a rule, a design) are named by card address, never by a
  made-up path.

## 2. Folder view

Studio > Folder (`side_pane/files_tree/frame_folders.py`) already draws it. Two additions:

- A folder outside the Block that the Block names (an Insight extract, a corpus path) is shown as one pointer row,
  never walked.
- Each row an episode touched, and each folder above it, carries 🧵 (`side_pane/files_tree/frame_folders.py`); a click opens
  Sessions showing only the episodes that touched it.

## 3. Element view

The Element view says, for each folder kind, which page parts draw it. Two relations:

| Relation | Means | Example |
| --- | --- | --- |
| shows | the part draws this folder or file | `runs/rNN_<segment>/` shows on Task > Answer > By segment, Job > Progress, Board > Findings |
| derived from | the part is computed from several folders | Insight Job > Changes is derived from two Jobs |

- The map is many to many: one folder may show in several parts on several levels.
- It is generated from the code that builds the page, never written by hand, so it cannot drift. Each theme's hook
  returns it from its real view tables (§ 6), not from `Theme.spaces` alone: Insight's and Design's ladder pages
  are built by their focus views, and `Theme.spaces` only builds the older tabbed layout.
- Each theme keeps a test that every folder kind in its skill's tree has at least one part that shows it.

## 4. Session view

### 4.1 What an episode is

An episode is one goal worked in one sitting, recorded as one **pass**: `passes/pNN-<MMDD>/pass.md` inside the soft
Run that served the goal (`runs/run-<verb>-<target>/`, hai-run). It may span several Runs and several folders
(a Labeling meaning loop is four Runs; a Design sitting walks generate, verify and revise across Tasks). Runs it
starts, such as 181 Insight segment Runs, are folders it touched, never episodes of their own.

Work done on the Block as a whole, not as one Run's round, is kept as a trace in its `trace/` (hai-trace); the
Files pane draws it. When no soft Run fits the goal and the work is not kept as a trace, it opens a soft Run at the level it acts on, as
hai-run already allows. So every episode is a pass, and a pass is found the same way at
every level.

### 4.2 The record

```text
runs/run-<verb>-<target>/passes/pNN-<MMDD>/
  pass.md          the episode: front matter + ## Ask, ## Summary, ## Changed
  transcript.md    optional; the raw chat, shown only where the theme allows (§ 5)
```

```yaml
---
session: <the session's saved name>       # who did it; kept in the record, never a page label
provider: claude | codex
date: 2026-11-17
goal: revise Methods to v0.4               # one line, the episode's title on the page
paths:                                     # SPACE-relative, every file or folder it wrote
  - paper/Paper-X/j02_writing_v1115_jama/t02_methods/draft/t02_methods-draft-v0.4.md
cards:                                     # card addresses it changed, when below a folder
  - t02.C3.P5.s14
---
```

`## Ask` is what was asked, `## Summary` what happened, `## Changed` the changes in words. The soft Run's
`run.yaml` keeps `passes:` and its `writes:` list, as Insight and Work already do.

`paths:` is written when the episode happens, by the one writer every session uses,
`hai-run/scripts/soft_run.py pass <run> --title … --changed <files> --session <name> [--cards …]`, from the
files the session itself wrote (its Edit and Write calls; `git diff` shows other sessions' work too).
A file a shell command wrote is not seen in the session's Edit and Write calls and is named with `--changed`. Several sessions edit the same folders at once, so one folder will have many overlapping
episodes; that is expected.

### 4.3 Records that already count

These are read as episodes where they are, never copied into a second record:

| Theme | Existing record | Read as |
| --- | --- | --- |
| every theme | Studio topic `sNN-<topic>/passes/pNN-<MMDD>/` (digest.md, transcript.md) | one episode per pass |
| Insight, Work, Design | soft Run `runs/run-*/passes/pNN-<MMDD>/pass.md` | one episode per pass |
| Labeling, Work | collect Run `runs/rNN_collect_*/passes/pNN-<MMDD>/pass.md` (a person's form round) | one episode per pass |
| Paper | `draft/records/<stem>-revise.md`, each `## Pass N … on draft vX` | one episode per Pass |
| Project | git commits on Block paths (`home/project_branches.py`) | stations on the Timeline, beside the passes |

An older record without `paths:` is joined to the folder that holds it, and its `## Changed` is shown as written.

### 4.4 Where it shows

- **Session view**: the episodes of the page's folder and everything below it, newest first, grouped by folder (by
  the loop's `mNN` or `eNN` in Labeling, by draft version in Paper). Each row: date, goal, and the folders and cards
  it touched as links.
- **Beside the element**: 🧵 after each content item an episode touched (a sentence, a design, a rule, a cell:
  the items `ref/cards.md` § 2 calls content), passed as a derived mark (`item_marks.DERIVED`), so it opens in
  the same card slot. Never 💬, which means open comments. Structure rows (Job, Task and Run rows, folds, tabs,
  section bars) carry no 🧵; there the Folder and Sessions parts show it.
- **Project level**: nothing new to draw. The Timeline (`home/project_branches.py`, through
  `focus_studio.timeline_events`) already draws every Run pass as a □ station; one station per pass, one 🙋 tip
  per Block, no count on its bar, commits and passes on one day stay separate stations.

## 5. Rules

0. **Speed.** The reader never walks a folder recursively: it globs fixed depths (`frame_sessions.PASS_DIRS`,
   `CHAT_DIRS`, `REVISE_FILES`), never enters results/, data/ or node_modules/, and parses each record once per version of it
   (path, mtime, size). At SPACE and Project level it runs on every Home load.

1. **Page words** (AGENTS.md): no count labels ("12 episodes"), no state words, no hashes, no "JL 2611xx" tags. The
   episode's own date and goal are content and stay; `session:` stays in the record.
2. **Signed files are never written** by an episode recorder: `design-goal.md` signs, `meaning/mNN.approved.yaml`,
   release signs, `draft/records/<stem>-sign.md`, `records/narrative-sign.md`.
3. **Frozen folders take no new file** (`inputs/inputs-vN/`, `observed/eNN_<exp>/`, a Book's `mK.md`, a released
   Job). The pass lives in the soft Run that acted and lists the frozen folder in `paths:`.
4. **Fences hold.** A design Job's `inputs/` is closed; a pass never sits inside it, and maker and reviewer Runs
   never read another Run's passes. Verify and rank still run in a context that generated nothing in the Job.
5. **No transcript on a page.** The Session view links `pass.md` or `digest.md`, never `transcript.md`: a
   transcript may hold printed rows, which Insight's pages must never show. A theme that wants transcripts shown
   opts in with `show_transcript`; none does yet.

## 6. Theme hooks

| Theme | Hook returns | Built from |
| --- | --- | --- |
| Insight | element map; extract pointer | `insight_focus_*_views`; board.md extract path |
| Labeling | element map; episode grouping by `mNN` / `eNN` | `labeling_focus_frame.task_frame`, `labeling_meaning_view`, `labeling_expression_view` |
| Design | element map (folder kind → view, section) | `BLOCK_VIEWS`, `BOARD_LAYOUT`, `JOB_VIEWS`, `TASK_STEPS`, `BOOK_VIEWS` |
| Work | element map | `work_sections`, `focus_plan_results`, `focus_tree`, `tab_cards` |
| Paper | element map; Pass reader for `-revise.md`; grouping by draft version | `paper_focus`, `paper_theme_*`, `workbench-task-draft` steps |
| Project | Timeline stations | `project_branches.py` |

## 7. Built

- `side_pane/rail_sections/frame_sessions.py`: the reader (`episodes`, `touched`, `touched_set`) and Studio › Sessions
  (`sessions_part`, the seventh folding part, under Folder; not shown when empty).
- Focus pages (`layout=focus`, the Files section): `side_pane/files_tree/work_files.py` puts 🧵 on touched folders and files of
  the tree (lazy expands too) and Sessions under it, filtered to the page's folder (`sessions_part(..., under=)`).
  `focus_studio.files_html` does the same for the plain folder list.
- Older tabbed Studio: `side_pane/files_tree/frame_folders.py` 🧵 on touched rows; Sessions after Folder (`page/block_index_page/frame.py`).
- `page/element_marks/item_marks.py`: 🧵 in `DERIVED`.
- SPACE root: the nearest folder with `env.sh` or `.server_config` (`frame_sessions.SPACE_MARKS`).
- Cache: one entry per record file, replaced when its (mtime, size) changes; the touched set per Block is kept
  until any record's signature changes.
- `hai-run/scripts/soft_run.py pass`: `--session`, `--provider`, `--cards`; SPACE-relative `--changed`.
- Tests: `servers/workbench/side_pane/rail_sections/tests/test_frame_sessions.py`, `hai-run/tests/test_soft_run.py`.
- Still to do: each theme's element map and its 🧵 on content items (§ 6); episode grouping by `mNN`/`eNN` and by
  draft version (today grouped by the folder holding the record).

## 8. Owners

- Shared code in `servers/workbench/page/` belongs to WorkBench-Project-UI; it agrees before the shared part is
  built. Its uncommitted change to `frame_runs.py` is kept.
- Each theme's hook and its folder-kind test belong to its `Workbench-<Theme>-UI` session.
- Still owed by Insight: a check that every soft Run's `writes:` names real paths, since the join rests on it.
