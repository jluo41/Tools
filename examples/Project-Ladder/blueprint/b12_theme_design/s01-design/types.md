# Design Board types

example: examples/Project-Ladder/design/Design-Example
block-kind: design-board
owner: [hai-design](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/SKILL.md)

Sources: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [design_jobs.py](../../../../../plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py); [example Block](../../../design/Design-Example/board.md).
A semantic Job contract is not a serialized `job-type:` value. Only declared Task values are listed as such.
Group labels and grouping criteria do not establish a separate group-type enum. No example record is changed
by this inventory. Unknown group types are left undeclared instead of adding a type named None or Unknown.

## Job group type

presence: grouping exists; a distinct group-type list is not defined by the current contract.
field: the Job's `method:` resolves the registry's `family:`; fallback reads the Job's `goal:`.
for: keep executions from the same method family together; use goal grouping when no family is available.
holds: Board execution Jobs, each retaining its own goal, method-version and input-version pins.
named: 〈Method family〉 from the registry; otherwise the goal name, then the fixed fallback Goals.
source: [design_jobs.py](../../../../../plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py) `topic()`; [method registry](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/methods).
owner: [workbench-design](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md) for grouping; [hai-design-method](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md) for family values.

The example's j01 and j02 pin M01; j03 pins M02. Their families come from those registry entries.
No `job-group-type:` is stored. This is not Work's decade-based `bands:` grouping contract.

## Job type

field: no separate `job-type:` value on the current Job faces; the entry below is a semantic contract.

### Design execution
for: develop and compare designs for one signed goal under one pinned method version and one frozen inputs version.
holds: the Job face with goal/method/inputs pins, its frozen input fence, reason and design Tasks, whole-set review, and original Runs; released output belongs to the Block's Delivery.
name: `jNN_〈goal〉_M0x-〈method〉-mK_inputs-vM/`.
source: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [scaffold](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/scripts/design_ladder.py).
owner: [hai-design](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/SKILL.md); [hai-design-goal](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-goal/SKILL.md) owns goals and inputs; [hai-design-method](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md) owns methods.
members: j01 and j02 pin G01 / M01 m2 with inputs-v1 and inputs-v2; j03 pins G01 / M02 m1 / inputs-v2.

The current scaffold still creates a Job-local Delivery directory; T19 records the writer mismatch with the
Block-owned Delivery contract. Neither this inventory nor its checks migrate those outputs.

## Task group type

presence: role grouping exists; a distinct task-group-type list is not defined by the current contract.
field: [design_jobs.py](../../../../../plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py) `task_topic()` derives the group from `R.kind_of(task)`, not a group-type field.
for: distinguish idea reasoning, individual designs and whole-set review inside an execution Job.
holds: Ideas contains t00; Designs contains individual design Tasks; Review contains t99.
named: fixed labels Ideas / Designs / Review. Their selector keys are ideas / designs / review.
owner: [workbench-design](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md).

These three groups are not additional Task types. The relation is Ideas → design-reason → reason ideas;
Designs → design-item → 〈design name〉; Review → design-whole → review whole.

## Task type

field: `task-type:` on each Task face, written by the Design scaffold.

### design-reason
for: derive the candidate ideas from the Job's fixed input fence before design Tasks are opened.
holds: fixed t00_reason-ideas Task and its reason Run; the closed Result contains ideas.yaml, chains.yaml and topics.md.
name: fixed `reason ideas`; folder `t00_reason-ideas/`.
group: Ideas.
source: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [example reason Task](../../../design/Design-Example/j01_confirm-by-reply_M01-goal-only-m2_inputs-v1/t00_reason-ideas/t00_reason-ideas.md).
owner: [hai-design-unit](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-unit/SKILL.md) for reasoning; [hai-design-workflow](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-workflow/SKILL.md) for Run routing; [hai-design](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/SKILL.md) for Task allocation.

### design-item
for: develop, independently verify and revise one design, keeping revisions with the same design.
holds: one design Task, its idea/name, Design and Evaluation, element provenance and prediction, and generate/verify/revise Runs with their own Results or passes.
name: `〈design name〉`; folder `tNN_d〈NN〉_〈design〉/`.
group: Designs.
source: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [example design Task](../../../design/Design-Example/j01_confirm-by-reply_M01-goal-only-m2_inputs-v1/t01_d01_yes-first/t01_d01_yes-first.md).
owner: [hai-design-unit](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-unit/SKILL.md) for generation, verification and revision; [hai-design-workflow](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-workflow/SKILL.md) for projections and Runs.

### design-whole
for: compare the Job's designs, rank them and select the kept set with predicted effects.
holds: fixed t99_review-whole Task and independent review/rank Run; its Result contains ranking.csv, with predictions projected by the workflow owner.
name: fixed `review whole`; folder `t99_review-whole/`.
group: Review.
source: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [example review Task](../../../design/Design-Example/j01_confirm-by-reply_M01-goal-only-m2_inputs-v1/t99_review-whole/t99_review-whole.md).
owner: [hai-design-unit](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-unit/SKILL.md) for independent ranking; [hai-design-workflow](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-workflow/SKILL.md) for projection; [hai-design-delivery](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-delivery/SKILL.md) for human-gated release.

## Studio organization

The actual example has Block topics s01-example-design-flow, s03-q01-example-test and s04-q02-prediction-check;
s02-release-choices belongs to j03. Keep that ownership. The Board face declares no numbered Studio Band scheme.
A Design Board Band/numbering contract is still to be specified; the Blueprint registry is not that contract.
Do not turn these example topic names into universal Studio types or move the Job's topic to the Block.

## Validation boundary

Read the inventory with the shared block_types_check.py parser; require this file and the Book inventory
explicitly before comparing types. Compare every declared Task type against the actual faces. Empty group-type
lists describe a contract gap; the shared check currently rejects them. Do not fill them with invented types.
Job serialization, actual-Block Studio Bands and inventory-generated views remain open under T08/T20.
