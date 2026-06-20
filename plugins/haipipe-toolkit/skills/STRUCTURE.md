HAI-Pipe Toolkit Skill Structure
================================

Status: draft (2026-06-20)
Scope: top-level mental model for the skill folder.


Core Stack
==========

The core execution model is a stacked sandwich:

```
narrative   story layer        decides what claims the project needs
probe       claim layer        opens a claim contract, then closes it after evidence
discover    outside evidence   sources, notes, prior art, novelty, verdicts
task        inside execution   code, runs, metrics, reports
```

`discover` and `task` are sibling filling under a probe. A probe can dispatch
one discovery, many discoveries, one task, many tasks, or a mix of both. The
probe does not contain the task or discovery; it references their artifacts and
resumes after they are ready.

`narrative` is the outer sandwich. It opens story gaps, starts probes, reads
closed probe verdicts, and decides whether the story is ready to hand off.


Project Folder Contract
=======================

When the stack runs inside a project, the durable project shape should be:

```
examples/<PROJECT>/
|-- _haipipe/
|   |-- project.log.jsonl      single append-only event log
|   |-- project.status.yaml    current project snapshot
|   `-- project.site.md        human dashboard
|-- narratives/
|-- probes/
|-- discoveries/
|-- tasks/
|-- paper/
`-- applications/
```

Local unit folders may have `status.yaml`, `site.md`, contracts, and artifacts.
They should not keep separate event logs. The timeline truth is
`_haipipe/project.log.jsonl`.


Current Folders
===============

Current top-level folders are the working structure:

```
0_*           utilities, connectors, venue playbooks
discover   external evidence capability + durable discovery artifacts
project    project umbrella, inspect, organize, workflow helpers
task       task lifecycle hub and task-type specialists
probe      claim lifecycle hub
insight    deferred export/synthesis layer
paper      paper deliverables
application application/report/message deliverables
narrative  story lifecycle
```

`1_data`, `2_nn`, `3_end`, and `4_individual` stay as top-level task-domain
families. They work with `task`, but they are not being moved under it.

Read them as task-domain families in the current stable folder layout:

```
1_data        data task family
2_nn          model/algorithm task family
3_end         endpoint/deployment task family
4_individual  individual/inference task family
```

Do not plan a prefix migration for these folders. Keep existing skill paths and
references stable.


Skill Identity And Refresh
==========================

Folder names are organization only. A skill is identified by the `name:` field
inside its `SKILL.md` frontmatter.

After a folder rename, an already-running Codex session may still show the old
path in its cached skill list. Start a fresh session or reload the plugin index
to see the new folder paths. Do not rename skill `name:` values just to match
folder names.


Blueprint Docs
==============

`../blueprints/` contains end-to-end blueprints of what a finished or
in-progress run should look like on disk. It is plugin-level documentation,
not a skill family.
