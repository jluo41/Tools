---
name: hai-job
description: "Owns a Job's face, ordered Task records and scaffold. Use to create a Job, add a Task or check a Job face. Trigger: job, new job, add a task, job face, jNN, /hai-job."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.2"
  last_updated: "2026-11-27"
---

# A Job's records

A Job is one bounded unit of work inside a Block. Its owning Block type determines what a Job represents and whether it contains Tasks. This skill owns the Job face and its Task register. Task execution belongs to `hai-task`; the Block type's contract decides applicable levels.

The Block owns the workbench page. Selecting a Job or Task keeps the Block's route and title. Page layout and interaction rules belong to the shared workbench contract; this skill defines the records those controls read.

Read [ref/job-contract.md](ref/job-contract.md) before creating a Job or adding a Task.
For an Ideation Block, also read [the Idea Job contract](../../ideation/hai-ideation/references/idea-block.md):
a Job preserves one candidate idea through its evaluations and linked Paper handoff; Tasks name bounded
research questions or outputs, and skills are methods.

## Folder and face

```text
bNN_〈block〉/
└── jNN_〈job〉/
    ├── jNN_〈job〉.md
    ├── tNN_〈task〉/       when the Job contains Tasks
    ├── sNN-〈topic〉/      when a Studio topic serves this Job
    ├── runs/               Job-owned Runs under hai-run
    └── src/ · sbatch/      when Tasks share code or supervision
```

The face identifies the Job's title, `goal:`, `close:`, optional `answers:`, and its authored content. `emoji:` is the Job's display mark. Its title follows the real folder's words. Fill required fields before treating the scaffold as usable work.

A Job's `job-type:` states its type. The applicable Block type contract defines the allowed types. A group names a collection of Jobs; the Block's `bands:` associates a numbered range with that group. A type is not inferred from a group's spelling or from a use-case label. `code`, `doc` and `check` are example type values, not a universal list.

Where a Job contains Tasks, `## Tasks` lists their real folder names in reading/dependency order. Assigned record numbers stay stable; do not renumber to sort the page. Optional sections and deliverable records follow `ref/job-contract.md` and the owning Block type.

## Create and check

```bash
S=plugins/haipipe-toolkit/skills/1_base/project/hai-job/scripts
python "$S/new_job.py" job  <block> --slug <job> --title '<title>' --goal '<goal>' --close '<close>'
python "$S/new_job.py" task <job> --slug <task> --title '<title>' --kind <task-type>
python "$S/new_job.py" check <job>
```

- The scaffold chooses the next free number; `--nn` chooses an explicit free number and `--name` uses a theme-owned folder name. Existing folders are refused.
- `--answers` records the Question addressed by the Job or Task.
- A Task scaffold creates its face and adds it to `## Tasks`. `hai-task` supplies its execution contract.
- `check` compares the Task register with real folders and validates authored deliverable records. A check result is evidence only for the rules it checks.

## Delivery

A Block owns the physical `delivery/` folder. A Job's published material lives beneath `delivery/jNN_〈job〉/`; Task material beneath `delivery/jNN_〈job〉/tNN_〈task〉/〈lane〉/`, relative to that Block. Resolve these paths through the delivery owner; do not create a Job-local delivery root. Runs and Results remain at their producing records. A successful build does not grant acceptance or release.

## Owners

| Owner | Responsibility |
|---|---|
| `hai-project` | Folder hierarchy and structural audit |
| `hai-block` | The owning Block |
| `hai-job` | Job face, Task register, scaffold and record checks |
| `hai-task` | Task identity, execution type, lifecycle and Runs |
| `hai-report` | Question links carried by `answers:` |
| `hai-delivery` | Delivery ownership and release |

Theme-specific folder patterns belong to their theme contract. Do not manufacture a Job or Task level where that contract has none.
