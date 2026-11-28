---
name: hai-ladder
description: "Choose where work belongs across Project, Block, Job, Task, Run and Studio, and route it to its work-kind and record-owning skills. Use when deciding whether to reuse, split or connect work at different levels."
---

# Ladder

Read [CONSTITUTION.md](CONSTITUTION.md). Decide the scope and owner of work before
creating records. Read the target Project and the relevant existing Blocks first.

## Two independent choices

Containment answers where a record belongs. Work kind answers which method and
acceptance rules apply. Theme folders group Blocks; they do not add an execution
step. A request to organize work does not require creating every level.

```text
Project
└── 〈theme〉/
    └── bNN_〈block〉/
        ├── sNN-〈topic〉/
        └── jNN_〈job〉/
            └── tNN_〈task〉/
                └── runs/rNN_〈run〉/
```

This is a containment example. Use the selected owners' actual names, allowed
types and writers. Studio topics can also serve a Job or Task under the Studio
contract; they are not another step between Task and Run. A Block owns the workbench
page; its Job, Task and Run selections remain inside it.

## Choose the smallest coherent scope

| Need | Owner to read |
|---|---|
| A durable boundary across related work | [hai-project](../hai-project/SKILL.md) |
| A bounded topic or goal with its own work and handoff | [hai-block](../hai-block/SKILL.md) plus its work-kind skill |
| A distinct line of work within that goal | [hai-job](../hai-job/SKILL.md) |
| An independently executable unit with inputs and a close check | [hai-task](../../task/hai-task/SKILL.md), then its allowed type skill |
| A concrete execution, its identity and receipt | [hai-run](../hai-run/SKILL.md) |
| A question, explanation or design being developed | [hai-studio](../hai-studio/SKILL.md) |

Reuse an existing record when its goal and ownership fit. Split when the pieces
have independently meaningful goals, inputs or handoffs; more files or a longer
discussion alone do not establish a new Job or Block. A repeat execution usually
belongs under its existing Task, subject to the Run owner's reuse rules.

Resolve the work kind by intended output, not by the wording of a folder name:

| Intended output | Work-kind entry |
|---|---|
| Code, data, models or calculations | [hai-work](../../../2_work/work/hai-work/SKILL.md) |
| Tool, skill or workbench definitions and their verified implementation | [hai-blueprint](../../../2_work/blueprint/hai-blueprint/SKILL.md) |
| External sources and durable evidence synthesis | [hai-discovery](../../../2_work/discovery/hai-discovery/SKILL.md) |
| Coordination, requests and replies | [hai-cowork](../../../2_work/cowork/hai-cowork/SKILL.md) |
| Learning a concept, explaining it and optional practice | [hai-knowledge](../../../2_work/knowledge/hai-knowledge/SKILL.md) |

For other kinds, read their existing theme entry. For example, dataset findings
belong to Insight and a manuscript to Paper. This table does not reclassify them.
Compose a kind's method with the shared level contract; create a specialized skill
only when a distinct method needs one, not for every kind-by-level combination.

## Connect without duplicating authority

Name the consumer's source record or accepted output and link to it. Discovery
can supply evidence to Knowledge, and Knowledge can refer to Work practice, without
copying either producer's records or starting another execution. Apply the producer's
version and handoff rules where they exist.

Keep containment separate from process order. Dependencies, branches, human gates
and resumption of Run execution belong to [hai-run's Workflow contract](../hai-run/ref/workflow.md).
Do not turn Project → Block → Job → Task → Run into a mandatory lifecycle.

Concept-only learning may need Studio topics and no execution records. Follow
CoWork's own contract for a coordination Job rather than inventing Task/Run folders.
If an example and an owner disagree, identify the specific conflict; do not silently
invent a new schema. If “Scene” means something beyond a Theme grouping, resolve
that meaning before creating a new containment level.

## Hand off the decision

Return the proposed existing or new owner path, why that scope fits, the work-kind
entry and record writer to use, and any real unresolved type or ownership question.
Read the chosen owners before implementation and follow the repository's file-plan
approval rules. This skill does not itself authorize migration, execution or sending.

Project root creation and shape audits remain with hai-project, including its
[ladder table](../hai-project/ref/ladder.md) and scripts. File formats, numbering,
execution gates and acceptance stay with the respective record owners.
