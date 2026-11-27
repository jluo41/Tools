s11 · Work Job UI preview: a Job worked on inside its Block
===========================================================
view: overview

**Tags:** `All pages`

**Stage:** shaping

**For:** the Block's 💼 Jobs section, where a Job is worked on without leaving the Block page, as a screen preview in `delivery/ui/`, for JL to agree and for the workbench code (`servers/workbench/page/job_task_views/focus_jobs.py`)

**Delivery type:** ui

**UI preview:** Job · work

**Covers:** the Job buttons (one line each, the newest decade first, a line between decades, an earlier or closed Job faded); a Job's own view buttons, Main and then one per Task; a Task's view, its page with its bands and folds (its Runs among them); what a Task's mark says

**Excluded:** the stand-alone Job page and its Report, Work and Studio (`j03_work_workbench_pages/t02_job_page/` s54, s55, s56); what belongs in a Job and what in Studio (haipipe-block A06); the layout's parts and dots (`servers/workbench/ref/top-view-left-tab-right-content.md`)

**Why:** the Block is the one index page; can a person open a Job, pick one of its Tasks and work on it there, the way the Report and Studio already read?

**Topic:** a Job is the code-heavy place (A06): it runs by itself and asks a person for a little design. Inside the Block's 💼 Jobs, view buttons pick the Job (j01, j02, j03). The picked Job has its own view buttons: Main (its Report bands, as the Block's Main) and then one per Task, t01, t02, t03. A Task's view is its page, its bands and folds, its Runs among them; its folds look like a Studio topic's. Its goal is the hover of its button; no MindMap, no empty Findings, a Task's state a mark after its name (⏳ ✅ 🙋 N; an open Task shows none), never 🔴.

**Feeds:** `servers/workbench/page/job_task_views/focus_jobs.py`


Decision
--------

JL 261125 16:45: "we select Job in the view bottom and that job can have its own sub view buttom list, and then each
task view buttom can have a list of task folder, and we may have task 1, 2, 3, and then we have the things like task
page ... task then can have the fold."

JL 261125 17:05: "should we call it the main? ... how about we get the tasks to be the view as well".

JL 261125 17:45, of the Job buttons wrapping onto three lines: "How could we make this to be better?"; then "could you
put the design of the UI of the Job to the draw first?". The drawing shows it: j11 j12 j13, a line, then j01 j02 j03
faded; one line each.

JL 261125 17:47: "I am thinking what if we have more and more jobs or tasks? Do you think it will be okay to have the job
topics view buttom and task topic view buttom?" Proposed, drawn as MANY under FEW: a decade becomes a topic button
(board.md's `bands:` names it, Workbench · j1N), one row per level, shown only when a row would pass about 7 buttons.

JL 261125 18:00, of MANY's four rows: "we might need to think about what is the best UI design for it, not to be too
crowded"; 17:59 "could you update the design first?". Proposed: one line, a path of dot-words, `• j03 · Work workbench
pages › • t02 · Job page`, each opening a menu of its siblings, the decades as headings and an earlier decade faded,
Main the first item of the Task menu; no topic row and no switch. Preview `delivery/ui/job-view-path.html` (removed 261126), beside
today's rows (`job-view.html`, removed 261126).

JL 261125 18:02, of the path: "I don't like this"; of MANY's rows: "still want things here, to see, to get". Now: every
Job and Task a visible button in two rows at most; a decade's topic is a small grey word inside its row (`j1N
Workbench · j11 j12 … │ j0N earlier · j01 …`), not a row of its own; with more than 7 Tasks a Task shows its number,
its name on hover and when picked. No menus, no switch. Preview `delivery/ui/job-view-rows.html` (removed 261126) (FEW and MANY).

```text
[j11 · Workbench page] [j12] [j13] │ j01 j02 j03 (faded)         Job buttons (hover: its goal)
  [Main] t01 · Block page 🙋3  t02 · Job page 🙋3  t03 …  t04 …   the Job's own views
  t02's page                                         •  open dot
  🧭 Overview ──────
   ▸ 1 · 🎯 Goal
  📊 Plan + Results ─
   ▾ 1 · ⚙️ Runs   r01 collect job report views · r02 … · run-design-job-page
   ▸ 2 · 🙋 Interactions 🙋3
```


JL 261125 20:34, of j11's Main, every Task row a red dot: "why the status is this? ... design the structure of the s11
for how should the job's main should looks like." The dot is the face's `state: 🔴 OPEN`, copied by
`ui_parts.state_mark`. Proposed, Main of a Job: one 📊 Plan + Results band, 1 · 🧱 Tasks (each row its name in words,
its newest round's title, its mark: a STANDING Task's from its check Run's newest pass, any other Task's from its face,
an open Task with no Run none) and 2 · 🧾 Traces (every trace whose `work:` names the Job or one of its Tasks, newest
first); then 🔎 Findings with only what is still open, under its Task, not drawn when empty. No Overview Goal (the Job
button's hover), no empty Requirements, no MindMap. Preview `delivery/ui/job-main.html` (removed 261126) (proposed beside today).

```text
[Main] t01 · Block index page  t02 …  t04 · Shared parts 🙋1  t05 …
📊 Plan + Results
 ▾ 1 · 🧱 Tasks ▰▰▰▰▱
    Block index page            live restarts   ✅
    Shared parts and file map   live restarts   ⬜
 ▸ 2 · 🧾 Traces   task health runs · page subfolders · workbench jobs
🔎 Findings
 ▾ 1 · Shared parts and file map 🙋1   page words
```


JL 261125 20:50, of the Topic rows preview: "what I want is this version"; 20:57 "this is not updated yet". Taken and
live on the Block's 💼 Jobs: four fixed rows, each one line that scrolls sideways under a faded edge (a mouse can drag
it); row 1 the Job topics and row 3 (Main, then the Task topics) always shown; row 4, that topic's Tasks, only once a
Task topic is picked, and the Task last picked there comes back; a topic reads its name, then its code small and grey
(`Workbench · j1N`), from a `bands:` line.

JL 261125 21:05, of Main's Tasks (one half fold, the rest flat rows) beside a Studio topic's fold: "why the fold is
not like this". Now each Task is a boxed numbered fold, as a Studio topic is (`band_sec`): `t01 · Block index page`, its
newest round's title as its word and its mark on the right, closed; opened, its folder and its rounds, newest first.

```text
▾ 1 · 🧱 Tasks ▰▰▰▰▱
  ▾ t01 · Block index page            live restarts ✅
      servers/workbench/page/block_index_page/
      ✅ p02 live restarts · ✅ p01 first check round
  ▸ t04 · Shared parts and file map 🙋 1   live restarts ⬜
```

JL 261125 21:20, of the real 💼 Jobs beside the Topic rows preview: "You need to tell the differneces". The four rows
match; the content does not: the preview holds the picked view in one box with its open dot on the top-right corner,
the real Main has no box and no dot (a Task view a dot and no box), and the real Main still shows Goal, Requirements,
MindMap and "No findings here.". The Topic rows preview now holds the whole structure: the box and its dot for every
view; Main is Job Main (📊 Plan + Results, 1 · 🧱 Tasks with a boxed fold per Task; 🔎 Findings only
when something waits); a Task is its page (1 · ⚙️ Runs, its rounds newest first; its Findings when it waits).

JL 261125 21:31, of a box inside a box inside a box (the view's box, 1 · 🧱 Tasks, each Task): "you have so many boxes
here", beside the real page's bands; 21:32 "please update the design without my approval". One level of boxes,
as the real page and Studio: a band holds folds, a fold holds lines. No box around the view (its open dot at the first
band line's right end); under 📊 Plan + Results each Task is a fold (a Task view: each round); 🔎 Findings only when something waits.

```text
📊 Plan + Results ──────────────────────────────── •
▾ t01 · Block index page          live restarts ✅
    ✅ p02 live restarts · ✅ p01 first check round
▸ t04 · Shared parts and file map 🙋1  live restarts ⬜
```

JL 261125 21:40, of the 🧾 Traces band copied in from the Job Main preview: "I did not ask for
the Traces band". Removed; a Job's Main is 📊 Plan + Results (its Tasks) and 🔎 Findings when something waits, nothing more.

JL 261126 12:30, of 🧭 Overview's three folds (Goal, Requirements, MindMap): "merge the three fold into one fold",
top-view-left-tab-right-content. A Job with nothing found draws no 🔎 Findings band (no "No findings here.").

JL 261127 00:08, of the four Overview quick views: "I prefer to have this one", overview-top-views. A Job's 🧭 Overview
is one fold, 1 · 📋 Brief (JL 261127 00:30; first the Job's name, which repeated its Job button), top views Goal · Requirements · MindMap, MindMap's left tabs Topics and Work
Structure (`work_frame.overview`, `top_views`). Live under Page › job-overview; the quick view fades (old); the other
three (left tabs, Brief and MindMap, Goal on top) removed 261127.

JL 261127 00:40-00:45, of 🔎 Findings: "they are more like the values, the tables, the figures, the report". Findings
is what a Job's Runs made, by type: a Run names its files in run.yaml `finds:` (value, display, report), and Findings
draws 🔢 Values, 🖼️ Displays, 📄 Reports, a left tab per file of each Task's newest Run, its open dot opening the file
where the Run wrote it; no findings/ folder (`run_finds.py`). The round folds per Task group are gone; rounds stay in
📊 Tasks. Overview is the Job's aim and scope, Tasks its progress, Findings its outputs.

JL 261127 12:08, of a Value's raw file: a finding names where it came from, `from:` (the raw files) and `how:` (its
steps) in its `finds:` entry. Under the finding each raw file shows with its open dot and ✅ or ❗ (the raw file changed
after the finding, or is gone), and the steps in a "How this table is made" fold, as the paper theme's Values link to
their source Runs. A fold with one finding shows it full width (trace 261127/1215).

JL 261127, after trying the inline Overview proposal: "我觉得这个做得挺好的。你能不能嵌到，比如说，呃我们那个内部呢？我看看什么样子。"
The new Effect › Overview · interactive keeps the preview in this topic: Goal / Requirements / MindMap,
Topics / Work Structure, Task inspection, and dots to expand Overview or hide its navigation. It is a separate
proposal for comparison, not a replacement for Page › job-overview. The user approved the four-file integration
plan with "Okay, go ahead." The related conversation and checks are in `../trace/261127/0850_overview_effect.md`.

JL 261127, after reviewing the interactive Effect: "要不然现在你就直接 implement 一下吧，把它给弄到这个 page 里面去，我看看什么效果。"
The user confirmed the eight-file implementation plan with "确认，按这份清单实现". Now live in Page › job-overview:
one Brief fold, Goal / Requirements / MindMap, actual Task groups in Topics, recorded Task goals in Work Structure,
local Task detail dialogs, and the expand/restore dot. Controls are scoped to each Job; inspecting a Task keeps
the owning Block's title and route. Authored Review Content remains authoritative. The matching interactive
Effect is faded and retained for comparison. Implementation: `job_task_views/job_overview.py`; checks and the
request are recorded in `../trace/261127/0912_overview_live.md`.

Files
-----

- Page: job-rows, job-overview, job-tasks, job-findings, one live page (b01_example_work's Jobs, j11 picked) with four marks: the rows, 🧭 Overview, 📊 Tasks, 🔎 Findings
- `delivery/ui/task-states.html` (Effect › Task states): the Topic rows page (`?demo=effects`), one Task per state with its effect, a legend beside it
- `delivery/ui/overview-interactive.html` (Effect › Overview · interactive, faded): the accepted comparison; implemented in Page › job-overview by `job_overview.py`
- `delivery/ui/overview-top-views.html` (Effect, faded): the Overview layout picked 261127, live in `work_frame.py`
- `delivery/ui/job-view-topics.html`: the design, taken (20:50), live in `focus_jobs.py`; its four rows outlined red
- `s11-work-job-preview.html`: the topic's Page; Studio lists its previews as left tabs
