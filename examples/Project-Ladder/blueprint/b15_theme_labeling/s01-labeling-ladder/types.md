# Types of Itemization

example: examples/Project-Ladder/labeling/b03_itemization
example-kind: design-preview

This Block contains a UI design, with no Job or Task records. It is not an executed example of these types.
The combined b02 walkthrough supplies Items, Meaning and Expression record evidence only; it is not an
independent Itemization Block. Task names below refer to contract identifiers, not operation names.

## Job group type

absence: No fixed Job group type is registered for this independent Block.
for: Group related Job instances when the Block declares a grouping.
holds: Jobs; a group does not change their types.
field: `bands:` on `board.md` names numbered Job groups.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
source: examples/Project-Ladder/labeling/b03_itemization/board.md
proposal: 〈Source collection〉 is grouping intent, not a registered type or band.

## Job type

absence: The independent Job Type identifier is not registered.
for: One source snapshot and accepted item recipe.
holds: `items` Tasks under that binding.
field: `job-type:` on the Job face; no such independent Job face exists in this preview.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
source: plugins/haipipe-toolkit/skills/3_theme/labeling/hai-labeling/SKILL.md
name: 〈Source and recipe〉; Name the Job for its source collection and item recipe.

## Task group type

absence: No separate Task group is defined; the Job holds its Tasks directly.
for: A declared group would organize Task instances without changing their types.
holds: No additional grouping layer in this Block design.
field: `bands:` on the Job face would name Task groups; none is declared here.
owner: plugins/haipipe-toolkit/skills/1_base/project/hai-job/SKILL.md
source: examples/Project-Ladder/labeling/b03_itemization/board.md

## Task type

field: `task-type:` on each Task face.
source: plugins/haipipe-toolkit/servers/workbench-labeling/labeling_theme.py `TYPES`.

### items
for: Turn a source snapshot into reusable items under an accepted unit recipe.
holds: Source and recipe references; describe, build, revise, check and optional embedding Runs; immutable item versions and check receipts.
field: `task-type: items` on the Task face.
owner: plugins/haipipe-toolkit/skills/3_theme/labeling/1_data/hai-labeling-preparation/SKILL.md
source: plugins/haipipe-toolkit/skills/3_theme/labeling/1_data/hai-labeling-preparation/SKILL.md
name: 〈Construction goal〉; Name the Items Task for the unit it constructs.
evidence: plugins/haipipe-toolkit/skills/3_theme/labeling/1_data/hai-labeling-preparation/SKILL.md — `task-type: items`
evidence: examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t01_example_items/t01_example_items.md — `task-type: items`
