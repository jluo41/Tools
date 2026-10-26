---
name: haipipe-job
description: "Owns the Job level: its face jNN_<job>.md (goal, close, answers:, its Tasks in order, ## Deliverables ticked from disk), its Spaces and buttons, a new-Job scaffold with Task slots, a check of Tasks against folders, and a theme's own Job and Task names. Trigger: job, new job, add a task, job face, jNN, tasks in order, level_patterns, /haipipe-job."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /haipipe-job · one Job, its face and its Tasks in order

Delivery belongs to the Block (JL 261010). Only the Block has a physical
`delivery/` folder. A Job writes `delivery/jNN_<job>/`, a Task writes
`delivery/jNN_<job>/tNN_<task>/<lane>/`, and a Report writes
`delivery/reports/qNN_<report>/<lane>/`, all relative to its Block. Child
Delivery views select their own source subtree. Runs and Results remain at
their source; a build grants no acceptance or release. Use
`haipipe-draft/src/common.py` for the path, never create Job/Task-local delivery.
Standalone Pages without a Block retain their own output root.


A Job is a group of Tasks in a Block that share inputs, code or one question: `jNN_<job>/`
with its face `jNN_<job>.md`. This skill owns the Job level of the frame and the order of
its Tasks; building each Task is `haipipe-task`'s, the folder's shape `haipipe-project`'s.

```text
bNN_<block>/jNN_<job>/
├── jNN_<job>.md      the face: # jNN · <title> · goal · close · emoji · answers: · Topic · ## Tasks · ## Deliverables
├── runs/ studio/     soft Runs (haipipe-run) · its own topics (haipipe-studio)
├── src/ sbatch/      code its Tasks share
└── tNN_<task>/       its Tasks, in the order ## Tasks lists them
```

Read `ref/job-contract.md` before creating a Job or adding a Task: the face, the Spaces, the
buttons, a theme's own names.


Create a Job, add its Tasks
---------------------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-job/scripts
python $S/new_job.py job  <block> --slug <job>  --title '<title>' [--answers Q01]
python $S/new_job.py task <job>   --slug <task> --title '<title>' [--kind page] [--answers Q01.E1]
python $S/new_job.py check <job>
```

1. **Number**: the next free `jNN` / `tNN`, or `--nn`; a taken one is refused.
2. **Task slot**: a bare face and a line in `## Tasks`; then build it with `haipipe-task`.
3. **Order**: `## Tasks` is the order; a number never moves once given.
4. **Link**: `--answers` writes the face's `answers:` (`haipipe-report`'s link rule).
5. **Check**: the list against the folders; exit 1 when they disagree.


The buttons it owns
-------------------

| Space | Button | Run | does |
|---|---|---|---|
| Description | Update the description | `run-face-<jNN>` | edit the face's fields, Topic, Tasks list |
| Work Details | Add a Task | `run-add-<tNN>` | `new_job.py task <job>` |
| Delivery | Build the delivery | `run-delivery-<target>` | the theme's delivery rule (decided 261007: stays here) |

At Block level, Add a Job is `haipipe-block`'s button and calls `new_job.py job`.


A theme's own names
-------------------

A theme that names its Jobs and Tasks its own way declares a regex per level on its Theme,
`level_patterns={"Job": r"^<…>", "Task": r"^<…>"}`; the frame then reads those folders as
Jobs and Tasks (a Job pattern directly under its Block, a Task pattern directly under a Job).
Scaffold them with `--name <folder>`.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-project` | the ladder's shape and its audit |
| `haipipe-block` | the Block above, and its Add a Job button |
| `haipipe-job` | the Job face, its Tasks in order, its Job-level buttons, a theme's Job names |
| `haipipe-task` | each Task: its Page, its kind, its Runs (not changed by this skill) |
| `haipipe-report` | how a Job's `answers:` links it to a Question |


Files
-----

```text
haipipe-job/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/job-contract.md     the face, the Spaces, the buttons, a theme's own names
├── scripts/new_job.py      job · task · check
└── tests/test_new_job.py
```
