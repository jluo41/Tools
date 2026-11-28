# Elements of a Block Job UI Preview

The parts every topic of this type shows: its views on top, and the left tabs of Page-Job and Page-Task. Read by the shared Studio element reader and the type page generator.
`##` defines a top view; `###` defines its left tab; bullet lines are requirements.
The type shows the requirement; an instance (s11-s14) shows the real thing under the same view and tab.

## Page-Job
from: one `jNN_*` Job of the example Block, live from the server
what: One real Job page, a left tab per part of it.
why: A Job page is judged part by part; each tab outlines one part on the live page.
- The live page, never a copy or a picture.
- Left tabs job-rows, job-overview, job-tasks, job-findings, in that order.

check: Select each left tab. It must show the selected Job inside the owning Block, with the corresponding part outlined.

### job-rows
from: the Block's Jobs section: `job-type:`, `board.md` `bands:`, the `jNN_*` folders
what: The rows that pick a Job: Job type, Job group, Job.
why: A reader has to reach the Job before reading it.
- The Job type row when a Job names a type, then the Job group row, then the Job row.
- The picked Job's own row: Main, then its Task groups.

check: Switch Job type, Job group and Job. Confirm the selected Job and its Main/Task-group row agree and the Block route stays selected.

### job-overview
from: the Job face: goal, close, Requirements, its mind map
what: The Job's brief: what it is for and what it must meet.
why: The goal comes before the work.
- One fold, Brief, with Goal, Requirements and MindMap as its views.

check: Open Brief and select Goal, Requirements and MindMap. Compare their contents with the selected Job face.

### job-tasks
from: the Job's `tNN_*` Tasks and their Runs
what: The Job's Tasks and how far each is.
why: The Tasks are the Job's plan and its progress in one place.
- One fold per Task, its state as a mark, its Runs inside.

check: Compare Task folds with the selected Job folders. Expand a Task and compare its Runs with disk.

### job-findings
from: `finds:` in the newest Run's `run.yaml` of each Task
what: What the Job's Runs made, by kind: Values, Displays, Reports.
why: A reader wants the results without opening each Run.
- A fold per kind that has a file; each file with its open dot.
- Under a file, the raw files it was made from, each marked ✅ or ❗.

check: Compare each nonempty result kind and file with the newest Task Runs; open a file using its dot.

## Page-Task
from: one `tNN_*` Task of that Job, live from the server
what: One real Task page, a left tab per part of it.
why: A Task page is the deepest a reader goes; it is judged part by part too.
- The live page, never a copy or a picture.
- Left tabs task-rows, task-overview, task-runs, task-findings, in that order.
- None for a CoWork preview: a CoWork Job has no Task level.

check: Select each Task tab. Verify its Job and Task remain selected within the owning Block; omit the view if the type has no Tasks.

### task-rows
from: the Job face's `bands:` (t0N, t1N) and the `tNN_*` folders
what: The rows that pick a Task inside its Job: Task group, Task.
why: A Task opens inside its Job, so the reader never loses the Job it serves.
- Main first, then one button per Task group; then the Tasks of the picked group, each with its mark.

check: Switch Task group and Task; compare the selected Task with its parent Job and ensure Main hides the Task row.

### task-overview
from: the Task face: goal, close, Requirements, its mind map
what: The Task's brief.
why: One step still needs its own goal.
- Goal, Requirements and MindMap.

check: Compare Goal, Requirements and MindMap with the selected Task face, not another Task.

### task-runs
from: the Task's `runs/` folders, each Run's `run.yaml` and passes
what: The Task's Runs, newest first, each with its rounds.
why: A Run is where the work happened; its rounds say what was asked and found.
- One row per Run with its name and state mark; its rounds inside.

check: Expand a Run; compare order, names and rounds with this Task runs directory.

### task-findings
from: `finds:` in the Task's newest Run
what: What this Task's Runs made.
why: The result of one step, without the other Tasks around it.
- The same folds as job-findings, for this Task only.

check: Compare result files with this Task newest Run and verify each preview opens.

## Job types
from: `job-type:` on each Job face of the example Block (else `job-kind:`, `kind:`)
what: The types of Job this Block uses, and which Jobs have each.
why: A type says how a Job is worked; the list tells a reader what kinds of work the Block holds.
- Left tabs: one per Job group type, then one per Job type, from the Block type's pinned lists.
- A Job that names no type is listed too, under no type.

check: Compare the group/type tabs with the Block Structure types.md and inspect untyped Jobs separately.

### 〈Job group type〉
from: `## Job group type` in the Block type's `types.md` (its Block Structure topic); a Block names its groups on `board.md` `bands:`
what: One kind of Job group this Block type uses.
why: A group says which stretch of the work a Job belongs to.
- The tab reads the group type's name; one tab per group type the list pins.
- What it is for and what it holds. No Job is listed under it by a guessed name.

check: Compare this type with its for/holds definition in types.md; the page lists no Job.

### 〈Job type〉
from: `## Job type` in the Block type's `types.md`; a Job names its type on its face, `job-type:`
what: One type of Job this Block type uses.
why: A type says how a Job is worked: built, checked or written.
- The tab reads the type's word; one tab per type the list pins.
- What it is for, what it holds, then its Jobs, each with its group.

check: Compare this type with its for/holds definition in types.md and verify every listed member belongs to it.

## Task types
from: `task-type:` on each Task face of the example Block (else `task-kind:`, `type:`)
what: The types of Task this Block uses, and which Tasks have each.
why: A Task's type picks the skill that builds and runs it.
- Left tabs: one per Task group type, then one per Task type, from the Block type's pinned lists.
- None for a CoWork preview.

check: Compare group/type tabs with types.md; omit the view for a type without Tasks.

### 〈Task group type〉
from: `## Task group type` in the Block type's `types.md`; a Job names its Task groups on its face's `bands:`
what: One kind of Task group this Block type uses.
why: A Job with many Tasks reads as a few named steps.
- The tab reads the group type's name; one tab per group type the list pins.
- What it is for and what it holds. No Task is listed under it by a guessed name.

check: Compare this type with its for/holds definition in types.md; the page lists no Task.

### 〈Task type〉
from: `## Task type` in the Block type's `types.md`; a Task names its type on its face, `task-type:`
what: One type of Task this Block type uses.
why: A Task's type picks the skill that builds and runs it.
- The tab reads the type's word; one tab per type the list pins.
- What it is for, what it holds, then its Tasks, each with its Job.

check: Compare this type with its for/holds definition in types.md and verify every listed member belongs to it.

## QuickHtml
from: the quick pages in the topic's `delivery/ui/`
what: Small pages that try a look before the code changes; a replaced one stays, faded.
why: A proposal is cheap to compare and to drop; the code changes only after one is picked.
- One small page per proposal, a left tab each, named for what it tries.
- A replaced proposal stays, faded.

check: Open each existing proposal, compare its title and content, and verify replaced proposals are faded.

## Draw
from: the topic's `.excalidraw` drawing and its `.png`
what: The layout drawn as boxes.
why: The shape of a page is agreed on a drawing before anything is built.
- The layout as boxes, one drawing for the topic.

check: Open the topic drawing and compare its layout with the defined page parts.
