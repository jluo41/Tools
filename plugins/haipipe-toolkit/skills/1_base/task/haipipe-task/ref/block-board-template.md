# <Block title>

board-kind: task-block
workbench-layout: workflow
spine: <one sentence naming the Block's topic and boundary>
close: <what must be true for this Block Board to close>

<!-- For question-driven Blocks, add the optional Questions and Related
resources registers from haipipe-report's ref/block-questions.md. Reports live in
reports/qNN_<topic>/qNN_<topic>.md, a report's own drawings in reports/qNN_<topic>/studio/; drawings
the whole Block shares live in studio/. -->

## Topic

<Why these Jobs belong to one Block and what this Block excludes.>

## Pipeline

```text
Block Board -> Job Group -> Task Page -> Run execution record
```

<Describe the dependency story between Jobs. A dependency is a Result binding,
not a scheduler relationship between Jobs.>

## Deliverables

<!-- What no single Job owns: a drawing or comparison across Jobs ("Across all Jobs" on the Goal
tree). Each Job's own items live in its face's ## Deliverables (haipipe-job ref/job-contract.md);
a table a Run makes belongs to that Run's Job, since a hard Run lives in a Task. -->

```yaml
deliverables:
- what: One drawing per Job
  kind: figure
  means:
  - The Studio topics, one drawing per Job.
  - Each shows what the Job ran, what it found, and what is still open.
  files: studio/s2[1-9]-*/s2*.png
```

## Pages

<!--
The Task tree supplies membership and default order automatically.

Use Job headings and introductions when they improve the reading path:

### j01 · <Job title>

<What this Job contributes.>

Only list Tasks here when an explicit presentation order is needed. Use the
full relative path, never a bare Task filename:

- j01_job_name/t01_task_name/t01_task_name.md
-->
