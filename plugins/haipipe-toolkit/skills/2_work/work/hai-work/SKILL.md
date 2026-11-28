---
name: hai-work
description: "Propose or update Work Blocks: propose reads material and plans sections and Jobs; update aligns named Blocks with their current record and page contracts; update --check inspects without edits or service changes. Trigger: update work block, work theme, /hai-work."
metadata:
  version: "0.4.0"
  last_updated: "2026-11-27"
---

# Work

Coordinate bounded execution work: code, data, models and calculations. This skill
proposes and aligns Work records; the Block, Job, Task and Run owners define their
formats and execution gates. [Workbench](../../../1_base/workbench/hai-workbench/SKILL.md)
opens and explains their pages.

```text
work/bNN_〈block〉/
├── board.md
├── sNN-〈topic〉/
├── trace/
└── jNN_〈job〉/
    └── tNN_〈task〉/
        └── runs/rNN_〈run〉/
            └── result/
```

This pattern shows containment. Use the owning writer's actual naming and record
contract. A Work Block executes work; a Work Block (Blueprint) develops and checks tools,
pages and skills. A Blueprint lives in the Project's `blueprint/` folder and keeps
the same Block-owned navigation. Use its purpose and authored bindings to decide
which views apply; being an example does not make a Block a Blueprint.

## Update named Blocks

```text
/hai-work update 〈Block path〉
/hai-work update 〈Block path〉 --check
/hai-work update 〈Block A〉 〈Block B〉
```

These are instructions to the skill-running agent, not flags for `wb.py`.
Read [the update procedure](ref/update.md) and
[the shared page rules](../../../1_base/workbench/hai-workbench/ref/work-pages.md).
Inspect the named Blocks, list supported changes and follow repository approval
rules, then apply and verify only those changes. `--check` performs no edits,
installation, execution, service start or restart.

With no path, use an unambiguous Block from the conversation; otherwise resolve
the intended target before writing. Multiple inputs bound the batch to those
Blocks. An update does not authorize a SPACE-wide sweep, folder moves, Run pruning,
execution or release.

## Propose sections and Jobs

```text
/hai-work propose 〈Block path〉
```

Read the Block's material and propose sections that express its actual work.
[The proposal procedure](ref/propose.md) covers authored Overview and Findings
sections, Jobs and their source bindings. The person confirms the proposal before
it is applied. Preserve source material, identifiers and human decisions.

## Plan execution

Write an agreed plan as the records the page reads before executing it. Use real
Job and Task names, goals, close conditions and declared types. Groups follow
explicit `bands:` and type contracts; a use case describes an application and does
not create a new Job type.

Create planned Runs through their owning generator or writer. Verify their
appearance inside the Block, including dependency and execution requirements,
before dispatch. Read receipts and the owning acceptance rules before changing
work state. Returned files alone do not establish a completed or accepted Task.

## Owners

| Work | Owner |
|---|---|
| Propose sections and Jobs from material | [ref/propose.md](ref/propose.md) |
| Align named Blocks or inspect them with `--check` | [ref/update.md](ref/update.md) |
| Open or inspect the Block and its embedded selections | `workbench` |
| Create or edit the Block face | `hai-block` |
| Create or edit Job faces and grouping | `hai-job` |
| Plan, build, execute, review or close Tasks | `hai-task`, then its applicable type skill |
| Run graph, tickets, dependencies and receipts | `hai-run` |
| Studio topics and bindings | `hai-studio` |
| Questions and reports | `hai-report`; `hai-draft` for report writing |
| Interactions and decisions requiring the person | `hai-interaction` |
| Data, model, endpoint or individual pipelines | The relevant task-type and stage skills |

Read each owner before changing its records. Keep one writer for each record and
reuse its scaffold or generator when applicable. Use the current theme contract
for CoWork, Discovery, Paper, Design, Insight and Labeling content rather than
reclassifying those records as Work.
