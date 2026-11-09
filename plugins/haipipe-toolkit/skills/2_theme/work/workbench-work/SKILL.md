---
name: workbench-work
description: "Open and interpret current work focus pages at Block, Job and Task level: Overview, Status, Findings, Delivery and view-scoped Around the Work. Distinguish Work Block and Blueprint Block with configured UI views. Read-only; /haipipe-work update aligns existing records. Classic layouts remain supported. Trigger: work workbench, work Block view, /workbench-work."
metadata:
  version: "0.10.0"
  last_updated: "2026-11-09"
---

# Work Block Workbench (the work theme, once task)

## Current focus pages

By default, open a work Block, Job or Task on the focus page (`servers/workbench/focus_page.py`,
`work_frame.py`), its views Overview · Status · Findings · Delivery. These hold, each one
b17 `s04-workbench-page-structure` Decided:

| Rule | What the page does | Decided |
|---|---|---|
| Two groups | **📋 Review Content**: the view's own numbered sections. **Around the Work**: Studio, Interactions, Decisions, Things to Know, Checklist, Timeline, Skills, Files, unnumbered, the same under every view | s04-D12 |
| Interactions, Decisions | Separate sections with topics on the left and their questions or decisions on the right. Inside a view, show its linked records; on the rail, roll up the page and its descendants across views | s04-D13; current shared scope |
| Decisions readable | One row per `sNN-DNN`: number, first clause, a tag only from its own words (Replaced, Waiting, Proposed); full text on open; nothing called confirmed from a quote | s04-D14 |
| View's own records | Every shared section uses the same explicit view/topic association. Matching Studio tags provide a fallback when no explicit view is set; this applies to all views | s04-D15; current shared scope |
| Checklist icon | 📝 (☑️ draws as a grey box) | s04-D16 |
| Skills | Each skill read in place: its SKILL.md, and a button per file in its folder, SKILL.md first | s04-D17 |
| Status | Jobs and Tasks first, the 261105 look: a band per jNN, each Job its emoji, jNN, name and how far (`partly · 7 Tasks · 14%`), opening to Tasks and Runs; Topics only when they group differently | s04-D18 |
| Job names | A Job's name is its folder's words; its emoji is its face's `emoji:` line (`haipipe-job`) | s04-D19 |

One thing shows once, in one look, under one name: a topic has the same name in Studio and
Decisions, and Jobs are never listed twice.

## Work Block and Blueprint Block

Both belong to Work; neither changes the B–J–T–R ladder or introduces a new
`board-kind`. **Work Block** executes work and returns results. **Blueprint Block**
develops a theme's UI and skills. A folder inside `blueprints/` can still be a
normal Work example: the purpose and authored configuration decide.

Both have Overview · Status · Findings · Delivery. Only a Blueprint with the
corresponding `ui-block:`, `ui-job:`, `ui-task:`, `ui-run:` examples adds Block UI · Job UI ·
Task UI · Run UI. The ordinary Work example is `b90_example_paper_results`; the Blueprint
example is `b17_theme_work`, both under `blueprints/Project-Ladder/work/` in Tools.
The type/view matrices and `view-guide.json` in b17's `ui/` are the current comparison.

Each main view has numbered **📋 Review Content**, then the same eight unnumbered
**🧭 Around the Work** sections: Studio, Interactions, Decisions, Things to Know,
Checklist, Timeline, Skills, Files. The right rail uses those same names and
aggregates the current page and its descendants across views. Report combines
results and work actions; there is no separate Work rail entry in this focus UI.

Status uses topics on the left and related B–J–T–R on the right, alongside actual
Jobs/Tasks/Run states. It does not replace those records with a generic Next Steps
list. The other views read their own source records and retain theme-specific parts.

Checklist reads authored checks in scoped faces/topics and, for UI views, recorded
walkthrough presence. A skill-based acceptance checklist must be authored and
verified; it is not automatically generated or certified by the renderer.
See [the update procedure](../haipipe-work/ref/update.md) for source fields, view
associations, evidence, and the difference between format alignment and completion.

## Open or update

Use `/wb <Block | Job | Task>` for the current focus page on its existing SPACE
host, with `layout=focus&section=report` and the appropriate `group`. Use the host's
configured origin; preserve its authentication and binding settings.

This skill reads and verifies; it does not edit records. To align an existing
Block and its child pages, use `/haipipe-work update <Block>`; add `--check` for
inspection only. That is an agent procedure, not a `wb.py` subcommand. Do not
apply the legacy `/wb update` migration merely to adopt the current focus format.

## Classic workbench (compatibility only)

The remaining sections describe classic routes and their stored contracts. They
are not the target format for `/haipipe-work update`. Do not remove their metadata
or move their files merely to open the current focus page.

One `work/bNN_*/board.md` declaring `board-kind: task-block` opens one
Workbench, drawn in the Insight Workbench's style (`servers/workbench-insight/`):
the title alone in the header, the Block band, the Spaces Guide · Scope · Task ·
Check · Delivery, every View opened by a heading and one lead line, and each
Space's content in one box beside its Runs panel. Guide explains the family;
its four Views (Description, Method, RoadMap Draw, Related Paper) come from
`servers/workbench-work/guide/guide.yaml` (family `task`). Method is the shared method
page: `guide/methods.excalidraw` first, then `guide/method.md` as fold
cards with its Run and Report method cards (`guide/methods/`); Related Paper is
`related/papers.md`, all in `servers/workbench-work/`; RoadMap Draw opens the generated
`Tools/blueprints/Project-Ladder/work/b17_theme_work/s04-workbench-page-structure/result/merged-s03-work-workbench/task-workbench-design.excalidraw`.

### Classic workflow layout


A Block whose `board.md` says `workbench-layout: workflow` (LLMRec b01 and b02, 261021) opens on
**Goal · Plan · Execution · Results**: Goal is one folded to-do tree, Goal → Job → Task → item, built
from each Job face's `## Deliverables` (haipipe-job `ref/job-contract.md`) and ticked from disk;
Execution groups each Task's Runs by their card's `role:`. The server is
`servers/workbench-work/work_progress.py`; its README says what each view reads.

For an explicitly requested structural migration to this classic workflow, `/wb update`
has its own dry run, apply and proposal rules. It can move files and add Run metadata.
It is not required to render the current focus page, and is not `/haipipe-work update`.

### Classic routes

Use the existing shared host at the selected SPACE, Project, tasks or Block
root. Derive the board path relative to the root:

```text
/_board/work-board?path=<block>/board.md&view=task
/w/<block-folder>
```

The short route uses the Block's basename. When names collide between
Projects, use the canonical full root-relative `path=`. A Block served as root
uses `path=board.md`. The bare endpoint opens the only Block or lists Blocks.
All URLs are origin-relative; use the running host's configured origin.
Do not start another host when the needed one is already running.

The host is `<plugin>/servers/_host/serve.py`; the presenter is
`<plugin>/servers/workbench-work/`. The full host supplies embedded Excalidraw
and its native save API. `--only task,page` supplies Questions, reports and
execution drill-downs but disables drawing routes. The shared Guide remains
available. Preserve the existing host's authentication settings.

## Spaces and Views

| Space › View | Contents | Source |
|---|---|---|
| Scope › Block | The spine, close condition, Jobs and board.md, as label and value rows | `board.md` |
| Scope › Questions | The Question register: id, group, topic, question, linked Tasks | `board.md` Questions |
| Scope › Resources | Workspace data: each `_WorkSpace` folder a Job declares (`raw_store` + `cohort`, or a `_WorkSpace/` path, in `src/config-defaults.yaml`) and the Block's ProjectResult folder, its files by kind (data named and sized only; documents, figures, drawings and scripts pop out); then the Related resources and the add form | Job defaults; `board.md` Related resources |
| Scope › RoadMap Draw | The question map first (generated, view only), then freeform drawings, then the studio topics (the Block's, then each Job's under its name) with their sessions and previews, each a folding row | Block `studio/*.excalidraw`, `sNN-<topic>/`, `jNN_*/sNN-<topic>/`, `runs/run-draw-<sNN>/passes/` |
| Task › each group | One table per register `group:` (one, Questions, when there is none): a row per Question, **Logic │ Task Work │ Report** | `board.md` Questions; native Tasks; report Pages |
| Check › Runs | Every Run and its receipt status | Native Ticket/Result reader |
| Check › Tasks | Each Task Folder's run counts and audit findings | Native Task reader |
| Check › Reports | Each report's answer status, evidence warnings and next action | Same snapshot; no second progress file |
| Delivery › Reports | Each report whose `answer-status` is `answered`: its Opening and Answer word for word, its evidence and drawings | report Pages |

Each Space has the shared Runs panel on the right (`servers/workbench/runs_panel.py`),
folded at first as Insight's: its run types are this skill's `ref/workbench-table.md` rows
for that Space, each with its agent, skill and a prompt to copy; Task's "Run a Task" lists
every native Run with its status. Clicking a Question row (outside its links) selects it:
the Task panel narrows to that Question's Runs and names it in each prompt. The panel
starts nothing. Earlier `view=` keys still open: `task` is the first group, `studio` is
Scope › RoadMap Draw, `related-paper` is Scope › Resources, `progress` is Check › Reports.

A row follows Insight's partition table. Logic shows "Question N", the title, the
question and its aim (when the register gives one), with "What we expect" (hypothesis) and "What would answer it" (acceptance) under
a folded **More**. Task Work is one light tree, Block → Job → Task → Run, each level written
once, a Task folding its Runs and its Task Page, each opening in the shared pop-out with an
own-tab link; the fold's line counts Tasks and Runs, never their status. Report shows the
report's title (the pop-out to the Page reader), the first paragraph of its Opening, any
one drawing: the first `.excalidraw` it links under Evidence (shown as its `.png` preview when
one sits beside it, as CoWork's, and opened read-only in the Excalidraw viewer; drawn by the
`excalidraw-report` skill, pictures inside it); a second drawing or a linked picture is a
finding in Check (JL 261005: "for each question we should just have one excalidraw"), and a tag
"report qNN". A named id (`Q-food-1`) shows as itself, and a Question with no `title`
shows its question once. No status, path, Limits or Next appear in the table; Check keeps them.

Work order follows `board.md`. Optional `work[].stage` is kept for other readers; the
table does not show it, and `role` is the Task line's hover text, falling back to the
Task's Opening. Do not infer types or progress from names. One Task may support several
Questions; Tasks under no Question close the last group's table under **Not under a
Question**. Questions can be answered by reasoning or existing evidence without BJTR work.
`page.toml` explicitly registers each report. `answer-status` is the declared Question
answer; `state:` remains the Page's own state. A changed linked evidence file is flagged
for rereading without silently changing either field. This display is not a Page CHECK,
evidence certification, adoption or release.

For creating a Question, writing a Report or adding a resource, read
`../../../1_base/project/haipipe-report/ref/block-questions.md` (the register, its optional
`group:`, report folders). A Question is shaped by `haipipe-report` and judged by
`haipipe-report`; Page owns the Report writing flow. Keep report Page Folders out
of native Task iteration and BJTR counters. The resource form adds only its register
entry; it does not download a paper or execute a Discovery workflow.

## RoadMap Draw

The question map is retired (JL 261031, b35 r02 Q2: "Just delete them"): the Report's
MindMap draws each Question with its answer, and `question_map.py` writes nothing now.
The rows are freeform: ideation, possible workflows, paths or other useful sketches, with no
required type or metadata. **Add drawing** opens a new native Block scene. Expanding a row
loads its viewer; **Edit drawing** takes the native editor's pen. The existing Excalidraw
lock permits one editing surface at a time. Full-screen opens the same file and obeys that
lock. No drawings or reports are created just by opening the Workbench page.

## Continue with a session

A session edits the Question register, Reports and native work through their
owning skills; a browser reload rereads them. Question/drawing folds persist in this
browser session. The page keeps Insight's shell (title, band, Space row with Guide first,
one box per Space with the Runs panel on the right), its colors, tab sizes and class
names; it adds no search or refresh controls of its own.

Keep execution, Question answers and Page acceptance distinct:

- Native Run status comes from the shared Ticket/Result reader, including
  redirected Job stores. A running receipt is not a heartbeat.
- Build counts describe existing files, not a passed review. Only allocated,
  non-superseded Task Tickets enter Task completion counts; Page Runs and
  orphan Results remain visible without inflating those counts.
- Signed readings and declared execution reports never imply Folder closure.
  Closure still belongs to `haipipe-task` and its current Page gates.

Server integration and source formats are documented in
`<plugin>/servers/workbench-work/README.md`.
