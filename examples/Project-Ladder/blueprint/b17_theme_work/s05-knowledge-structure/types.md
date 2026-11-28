# Knowledge execution types

example: examples/Project-Ladder/knowledge/b18_a2ui_learning

Four lists define the organization; an instance creates only needed members.
A group is a named number range on its owner's bands: line, never a folder.
Each ref: resolves the shared definition at build time. Its for:/holds: lines
below declare that reference; they are not a second copy of the Work contract.
The A2UI mapping is a simulation, not a register of existing Jobs or Tasks.

## Job group type
named: Block board.md bands: associates a concrete group with a jNN range.

### 〈Practice theme〉
for: Group independently deliverable practice Jobs around one application question.
holds: A shared goal, related learning Studios, and needed build, check or documentation Jobs; the group does not execute.
use: A possible A2UI group is 〈Interactive card〉 using j0N. A simple practice can show a Job directly without invented members.

## Job type
field: job-type: on the Job face; shared definitions are owned by Work.

### code
ref: ../s01-work-ladder/types.md | Job type | code
for: Reference the Work code Job type definition.
holds: Follow the referenced Work code content requirements.
use: A proposed Job 〈Build an interactive card〉 connects messages, components, data and actions into a runnable artifact.

### check
ref: ../s01-work-ladder/types.md | Job type | check
for: Reference the Work check Job type definition.
holds: Follow the referenced Work check content requirements.
use: Use a separate 〈Check interaction behavior〉 Job only when validation is an independent delivery; small checks stay with code.

### doc
ref: ../s01-work-ladder/types.md | Job type | doc
for: Reference the Work doc Job type definition.
holds: Follow the referenced Work doc content requirements.
use: Use for independently delivered reusable documentation. A Studio explanation does not automatically become a doc Job; match Task execution contracts first.

## Task group type
named: Job face bands: associates a concrete group with a tNN range.

### Make
ref: ../s01-work-ladder/types.md | Task group type | Make
for: Reference the Work Make Task group type definition.
holds: Follow the referenced Work Make content requirements.
use: A proposed group 〈Interaction implementation〉 uses t0N. Only independent execution units become Tasks.

### Show
ref: ../s01-work-ladder/types.md | Task group type | Show
for: Reference the Work Show Task group type definition.
holds: Follow the referenced Work Show content requirements.
use: Use a group such as 〈Result presentation〉 with t1N only when there is a separate presentation task; it is not a mandatory phase.

## Task type
field: task-type: must additionally resolve through hai-task/ref/types.md before execution.

### code
ref: ../s01-work-ladder/types.md | Task type | code
for: Reference the Work code Task type definition.
holds: Follow the referenced Work code content requirements.
use: A possible Task is 〈Run fixed input messages〉. Work defines the structure, but hai-task/ref/types.md has no code route; resolve its execution owner first.

### display
ref: ../s01-work-ladder/types.md | Task type | display
for: Reference the Work display Task type definition.
holds: Follow the referenced Work display content requirements.
use: Use only for results that meet hai-task-for-display, which expects display-safe aggregate tables; an A2UI live renderer is not that Task type.
