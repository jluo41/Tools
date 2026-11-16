# The frame: shared Guide and Studio, the work Spaces and themes

Part of the [Workbench base README](../README.md).

The frame: shared Guide and Studio (with Related), the work Spaces (frame.py)
-----------------------------------------------------------------------------

`GET /_board/workbench?path=<folder>[&space=<Space>][&sub=<subspace>][&studio=1][&theme=<name>][&format=json]`
draws any Block, Job or Task folder in one frame (`frame.py`, route `frame_view.py`):

```text
Guide · Studio | Block · Job ▾ · Task ▾ | Delivery             top navigation
Description | Report | Work | Runs                             work mode only
<subspaces>                                                             the third row
content                                                    │ Runs panel (runs_panel.py)
```

Studio and Delivery are the Block's two shared views (b10 s02-D18, s09-D05): thinking comes in
through the Studio, outputs leave through the Delivery. Selecting either selects only it and hides
the work Spaces row. A Job or Task has no Related, Studio or Delivery of its own (b10 s03-D06; JL
261011: "for the section, we will do not have the related studio and delivery"; "also for the
Jobs"): from any level, Delivery is the Block's, titled with the Block. Its source row (Block · jNN ·
jNN › tNN) picks one part, the open Job or Task picked when opened from there; a part shows what is
under its own path, `delivery/jNN_<job>/tNN_<task>/`, and links back down to its folder. The Block's
own Delivery ends with "By source", one row per part with its files (`frame.delivery_parts`,
`delivery_by_source`, `_delivery_row`). A lanes row follows only when a part has more than one lane.
`space=Delivery` links keep working.

Related, the Block's `related/` (what came in: meetings, papers, files we were sent), folds inside
the Studio as its second part, under the topic cards (b10 s04-related-workbench-skill; JL 261011:
"put the related as the second collapse part in the box of the studio items", "I might just want to
keep Guide, Studio | Block, Job, Task | Delivery"). One folding row per `related/related.md` row,
under the Studio's own group bar (JL 261011: "🎯Current 0 / Untagged 4 / + Group — for the studio"):
Current stays in the browser, a group is a name in the row's `group` cell (comma-separated, like a
topic's **Tags:** line), `related/_groups.txt` keeps the button order. Drag a row by ⋮⋮ onto a group,
× on its chip takes it out, × on a group clears it from every row. One bar, one script and one
`POST /_board/studio-group` (`kind: related`) serve both (`frame.group_list`, `studio_group_op`).
The subfolders (`materials/`, `meetings/`, `papers/` …) only keep the files; a file no row names yet
shows dashed under Untagged ("no row yet"), and a drag gives it a row. An opened
row is the file itself, read in place: a Word file through its package (`view=docx`,
`frame.docx_preview`, the Word renderer's projection: text, tables, images, comments in the margin;
JL 261011: "could we preview the word here?"), a PDF, a page or a picture (`frame.related_view`,
wrapped by `frame.studio_related`). Every theme shows this one view; paper's cards by question stay in
Report › Related Papers. Folded by default; a
`space=Related` link, or an older `space=Description&sub=Related` one, opens the Studio with it unfolded.

Delivery is the Studio's third folding part, under Related (JL 261014: "a new item after the Related to
name it as the delivery ... show all the delivery and preview them here"; b10 s03-D09): what came in, then
what went out. Every result of the Block's `delivery/`, from every Job and Task, as Delivery's own cards
(`frame.delivery_view`, wrapped by `frame.studio_delivery`), each opened on its preview, under the same
group bar; its line counts the results by kind. The top row's Delivery stays the full view.
A deliverable is one item, its lanes and versions folded in (`frame.delivery_items`, `frame.version_roots`, the
version rule Related shares; b10 s03-D10): a row of versions, newest picked, over that version's preview. A deck
with no render is drawn slide by slide from its package (`frame.pptx_preview`, `?view=pptx&path=<.pptx>`, its
pictures from `&media=`).

Runs is the Studio's fourth folding part, under Delivery (JL 261019: "list another one to show the Hard Run, for
each task, and just show their status"; b10 s06-D07): every hard Run (`runs/rNN_*`) of every Task under the Block,
grouped Job → Task, one line each: its mark, its status and the day it finished (`frame.hard_runs`,
`frame.studio_runs`). A Job and a Task each carry a tally (✅ complete · ❌ failed · 🟧 blocked · 🏃 running · ⏳ queued
· ⬜ planned or not run). It reads each Run's `result/runtime.yaml`, else its `run.yaml`; soft Runs (`run-*`) and
`history/` copies are left out, and nothing is written. SPACE Home uses the same reader (`frame.runs_tally`,
`frame.run_cells`): a Project's line and each Block row count their Runs, and an opened Block row shows each
Job with its Runs: its tally on the Job row, each Task's Runs under it when opened (b10 s06-D08, s06-D10).

Timeline is the Studio's fifth folding part, under Runs (JL 261011: "add another section of the
Timeline"; b10 s08-studio-timeline): what moved when, on one axis down the page, the oldest day at the
top and the newest at the bottom, a dot per day (JL 261011: "a real timelne ... with a axis down", "up to
down"). Three levels of detail (JL: "different level of details"): Days, the default, a chart, a row per
day, a column per topic group (by group, the default; JL: "the columns can also be the topic groups") or per
topic (by topic), a bubble sized by how much moved that day and the day's total as a bar; a group's column
picks that group in the bar above and shows its topics; clicking topics picks them and their items show under
the chart, on the same axis (JL: "select the topics we are interest in we show there content");
Topics, a line per topic with a stacked bar of its kinds (decided, session, note); Everything, each
decision, session and note. The browser keeps the level picked. The chart is plain HTML and CSS in the
page, no chart library (JL 261011: "it is not that beautiful ... like using the versualiaation tools?"). Nothing new is written for it; it reads what the topics already keep: each decision
`sNN-DNN · … (JL 261011)` by the first date in it, each session `runs/run-draw-<sNN>/passes/pNN-<MMDD>/`,
and the green change notes `✎ <YYMMDD> …` in the topic's drawings (`frame.timeline_events`,
`frame.studio_timeline`). It follows the group bar above, and has its own row of the same groups (All ·
Current · each group) so a group is picked without scrolling up: a picked group shows only its topics, as
columns and lines; by group shows every group again. A topic's name, column or bubble opens its row.
Decisions with no date are left off (b10 s08-D10). By topic, each column, 60 px wide, carries the topic's
full name: the sNN straight and bold, the rest slanted above it (s08-D12, s08-D14). Every day from the first to the last stays on the axis: a day with nothing shown gets a
short row and a hollow dot, more than 3 in a row are one row, "N quiet days" (s08-D13).

Folder is the Studio's sixth folding part, under Timeline (JL 261012: "在 related 和 timeline 下面再搞一个 folder，
这样我就可以看到这些 folder 里面（也就是这个 block 的 folder）都长什么内容"; b10 s09-block-folder): the Block's own
folder as one tree, folders first, then files, by name. A folder folds and says how many things it holds and what it is
for (`frame.folder_word`: the names every Block shares by a fixed line, a Run by its card, else its face's title); a
file opens in the pop-out (a .md in the reader, a drawing as the drawing, else itself) and says its size and its day.
Only the first level comes with the page; a folder's rows load when it opens, from `?view=dir&path=<folder>`
(`frame.folder_rows`, `frame_view.py`), 300 at a time with a button for the rest, so a Block of thousands of files
stays light (b00_rawdata: 5,317). Dotfiles and caches are left out. `path=` is the key the share doors check.

Every theme opens in this one frame (JL 261011). The themes' older Block pages,
`/_board/cowork-board`, `/_board/work-board` and `/_board/discovery-board`, send a Block to
the frame (`frame_redirect`, their old view mapped to its Space), as `/_board/insight-board`
already did; their pop-outs, report pages and `format=json` stay. An `--only` host serves no
frame and keeps its theme's own page.

Studio has one entry immediately after Guide and before the Block / Job / Task controls
(261010, b03 s02-D07–D09). Like Guide, it opens a shared view: only Studio is highlighted,
and the work Space and subspace rows are absent. Inside Guide, SPACE and Project are the first
buttons, before Description, Method, RoadMap Draw and Related Paper (s02-D12, renamed from Index
by s02-D31). Both leave the whole workbench, including from the embedded Guide. SPACE opens the
SPACE Home: it defaults to /?view=radial&measure=studios and may be set with the host's
--index-url or INDEX_URL setting. Project opens this host's Home showing only the folder's
Project, /?project=<Project folder>, or its SPACE bucket (shared:space) outside a Project. Studio's title is `<Theme> · Studio · <Block tag> · <Block name>`.
The topics, Disk, topic sessions and new-topic prompts all use the owning Block, including
when opened from a Job or Task. A theme's Studio content is taken from its Block adapter.

`studio=1` preserves `path`, `space` and `sub` as the work context. Clicking a level returns
to that work view; an open Job or Task has a clickable level button and a sibling picker in
Studio. The older `space=Idea Studio` links open this same shared view, returning to Description
when no work Space was supplied. The plain Block button keeps its tag in the page title.
The Report button is shortened from Audience Report (s02-D10); existing `space=Audience Report`
links and theme adapters keep their names.
Studio topics may record **Tags:** (or one **Type:**) in their notes, separated by commas,
middle dots or vertical bars. One topic may have several tags. The shared list shows each
tag on its row. Current comes first and the tag groups follow; there is no All button: with
no group picked every topic shows (the default), and picking the open group again unpicks it
(s02-D16). An sNN is one topic; a group is a set of topic references. A group other than
Current is a tag: `+ Group` names a new one, dragging a card by its handle onto a group writes
that tag into the topic's **Tags:** line, × on a card's chip takes it out, and × beside a group
deletes the tag from every topic (the topics stay). The writes go through POST
`/_board/studio-group` (`studio_group_op`), so groups live on disk and every person and agent
sees the same ones. `studio/_groups.txt` keeps the groups in button order, empty ones
included; dragging a group button sideways rewrites it (s02-D17). Each group shows an emoji
picked from its name by `group_emoji` (a word table, else a fixed palette pick); the × controls
show only under the mouse.
Current is personal: drop a card on it, or use Add to Current / Remove from Current (a Delivery
card has no such button, only the drop; JL 261014). It is
saved in localStorage under the Block's relative path and shared across that Block's
Block, Job and Task views. It does not sync to another browser or machine. A failed save
keeps the old selection and reports the failure. The URL stores studio_tag, or
studio_group=current; studio_group=all still opens the unpicked view.
Existing Job and Task topics remain in the shared list until their files are moved;
a Source picker can narrow the list. Cards show the topic name, tags and controls;
source badges, decision/open/session counts and feeds chips are omitted. Repeated sNN names use their source-qualified path
for membership and anchors, so two old topics cannot overwrite each other. The SPACE index counts this same list. No source files are moved or
renumbered by grouping. New topics still go into the owning Block's studio/.
A direct topic anchor reveals its row even when a saved filter would hide it.
Topic-to-Job construction, linked-topic filters and migration of existing local Studios remain
separate work in s02's Open list; this update does not move their files.

Two words keep apart: the **level** Task (a `tNN_<task>/` folder, a Task / Page in every theme)
and a **theme** (work, discovery, paper, insight, design, cowork, labeling; the old "task" theme is
work). The base owns the levels, shared Guide and Studio, the five work Spaces and their order, the third row, the
Runs panel and the look; `workbench-task-draft/` holds the Page Task's own views (outline, evidence, value,
delivery, exports).

**A Task type** (b32 s41-D15, JL 261016) is one folder, `workbench-task-<type>/`, holding everything a Task of that
type shows: its layout `task_<type>.py` (`TASK_TYPE`, `spaces(folder, root, sub)`), its views, their
`assets/`, its tests. A Task's face picks it with `task-type: <type>`; `frame.task_layouts()` finds every
such folder through `host_registry.task_folders()`, and the theme's own Spaces go on top. Its manual is the
skill `workbench-task-<type>`. A type every theme can use sits here, a theme's own type in its theme:

```text
servers/workbench/workbench-task-draft/                  task_draft.py   ⟷ workbench-task-draft     (today)
servers/workbench-<theme>/workbench-task-<type>/         task_<type>.py  ⟷ workbench-task-<type>    (a theme's own)
```

**A theme** is `servers/workbench-<theme>/<theme>_theme.py` exporting `THEME = Theme(...)`:
`name`, `label`, `icon`, `guide` (its Guide family), `levels`, `level_names`, and
`spaces(level, folder, root, sub) -> {Space name: Space(html, subspaces, open, run_types)}`.
Each run type is `{"label", "prompt", "skills"}`: every button names the skill that owns it
(b03 s21, 261007; the vanilla buttons' owners are listed in haipipe-run's
`ref/run-types-by-space.md`), and a theme's own buttons name theirs the same way.
A level with no folders shows a greyed tab, so every page keeps one tab row; a theme may set
`hide_empty_levels=True` to leave it out instead.
Anything it leaves out is the **vanilla** default, read from the standard folders: the face
`.md`, `studio/`, `reports/qNN_*/` (Question │ Work │ Report), the child `jNN_` / `tNN_`
folders, `runs/` (grouped by run type from `run.yaml`) and `delivery/`. With no theme the folder
opens as the vanilla workbench. `/w/<block>`, `/b/<block>` and every SPACE Home card open
here (261007). The page has no band line (JL 261007): the level tabs say where you are, and the
folder's path is the title's tooltip. The theme is the folder's Theme folder (`tasks/` or `work/` →
work, …) unless `theme=` names one. Example: `workbench-work/work_theme.py`. Helpers a theme may import
from `live.frame`: `Space`, `Theme`, `face`, `chain`, `children`, `runs_of`, `esc`, `link`, `reader`, `rel`,
`table`, `title`, `fields`, `studio_cards`, `pop`. Tests:

`_host/tests/test_frame.py` and its parts `test_frame_page_task.py`, `test_frame_delivery.py`,
`test_frame_studio.py`, `test_frame_groups.py`, `test_frame_routes.py` (fixtures: `frame_fixtures.py`).

Studio and Report follow b03's `s02-studio-workbench-skill` (s02-D04, D06):

- **Studio** (`studio_cards`): one closed row per topic with its name, tags,
  Current control and drawing links. A click opens its live drawing in place, loaded
  only when opened. A hand-drawn topic has Edit to switch its canvas to the editor;
  a builder's drawing stays view only. ↗ pops the topic out full size;
  `#topic-<name>` in the address opens that row. A topic's sessions are the passes of
  `runs/run-draw-<sNN>/passes/pNN-<MMDD>/` (and its older `chat/*.md` until they move), listed
  under "Save this session" in the Runs panel (`studio_sessions`).
- **Report** (`question_rows`, stored Space key `Audience Report`): one row per Question of the level's register (the
  face's `## Questions` yaml), plus any `reports/qNN_*/` not yet registered; the third row is
  All · its groups. Logic: id, title, answer-status, and "from the Studio": the topics whose
  **Feeds:** name it, each popping out its drawing. Work: the Jobs and Tasks whose face says
  `answers: <id>`, then the register's `work`. Report: the title (the Page in the pop-out), the
  Opening's first paragraph, `qNN_<topic>.png` as a thumbnail (its generated drawing, view only,
  in the pop-out) and a tag. A Task with no reports shows its own face as the report.

The frame's page carries the base's shared styles and no theme's own (JL 261007, "base styles only"):
a theme's Space html uses only base classes: the frame's `.topic` folds (`.topic.missing`: a dashed
card awaiting a Run), `.wf-table`, `.q-row`, `.chip`, `.mut`, the status marks `.st-ok` and
`.st-warn`; `SPACE_VIEW_CSS` (`workbench-task-draft/space_views.py`: Space tabs and views, evidence tables, the
Supporting Runs tree) and `WORK_ITEM_CSS` (`work_items.py`: the `bj-` and `lw-` work rows). A
component a theme lacks goes into the base for every theme. `_host/tests/test_frame_routes.py` StyleTest
keeps these styles off the frame's own parts.

A run type may carry `rows` (Runs panel cards). `pop(href, label)` opens any link in the frame's
pop-out (an in-page window with "Open in its own tab").

A theme may name its levels, pick which levels it has, name the subspaces of each Space, fill a
Space and list its run types. It may not change the levels, the six Spaces or their order, draw
its own tab rows, or carry its own look; ask the base's owner (design Block b03) for a frame change.
