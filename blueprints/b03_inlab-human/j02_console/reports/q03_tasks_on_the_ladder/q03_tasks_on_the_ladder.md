# How does the tasks feed read the project ladder?
state: 🟡 DRAFT · written by g02 2026-10-09 from the rebuilt feed and its check; CHECK pending
answers: Q03
answer-status: answered
results-read: 2026-10-09T10:35:00-04:00

## Opening

The feed reads the ladder: `examples-*/Project-*/tasks/bNN_<block>/jNN_<job>/tNN_<task>/` under `INLAB_PROJECTS_ROOT`
(the SPACE root), lists each Task under its Block and Job, and reads its scope from the Task's face: a `scope:
individual|group` header line, else a `task-type:` naming individual work, else group. The old flat letter series is
read only for a project with no Blocks.

**Where this Page sits:** [Q03 · tasks_api.py reads examples/Project-*/tasks/<A01_*> (a letter series) and classifies each task as individual or group; today's projects are examples-N-*/Project-*/tasks/bNN_*/jNN_*/tNN_*. How should the feed find and scope tasks on the ladder? (s33 issue 5.)](../../j02_console.md).

**Why it matters:** The Tasks view found nothing on any project laid out the current way.

## Content

### Answer

`tasks_api.py` finds Blocks, Jobs and Tasks by their `bNN_` / `jNN_` / `tNN_` prefixes, takes each title from its
face's first heading (a Block's `board.md`, a Task's `tNN_<task>.md`), its kind from the face's header lines, and its
status from what is on disk (results, a report, a plan). The response is a tree (project → Block → Job → Task) and
names the root folder, never its path. The Tasks view draws that tree, with each Task's task-type and status.

### Evidence

- The drawing: [s11 · the Group scope](../../studio/s11-group-scope/s11-group-scope.excalidraw), its Tasks screen.
- The feed: [tasks_api.py](../../../../../plugins/inlab-human/servers/haichat-inlab/tasks_api.py); the view:
  [TasksView.tsx](../../../../../plugins/inlab-human/servers/haichat-inlab/web/src/components/TasksView.tsx).
- The check, on the synthetic ladder (`fixtures/projects/`: one Block, two Jobs, four Tasks): `?scope=group` lists the
  two cohort Tasks under b01 · j01 (one with results, one scaffolded); `?scope=individual` lists the two Tasks whose
  face says `scope: individual`, under j02.

### Limits

- No Task in the projects today carries a `scope:` line, and no task-type names individual work, so on a real SPACE
  every Task reads as group until faces say otherwise.
- Read-only: a Task cannot be opened or run from the view (s33 issue 9, links).

### Next

Add `scope: individual` to the faces of per-subject Tasks as they are written (the haipipe-task face convention), so
the Individual console lists them.
