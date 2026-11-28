# Insight Block structure

The default design entry is the owning Work Block `examples/Project-Ladder/blueprint/b11_theme_insight`. Select its Studio in that Block. The real example's Jobs and Tasks are selections inside its own Block. Internal HTML and mindmap documents are embedded content.

## Shared categories and types

Band is the outer category. Blueprint Band names and order come from `examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json`. Studio Type defines the content an instance must show. Reference the Work definitions; do not copy their registry into a theme renderer. A theme may define a distinct type when its actual responsibility requires one. Omit empty type groups. Ordinary actual Blocks display instances without a required type-definition group.

| Shared Studio Type | Definition in b17 | b11 instances |
|---|---|---|
| Block Structure | s71-studio-type-block-structure | s01 Insight Board, s02 Question Book, s03 DataPrep |
| Block Job UI Preview | s72-studio-type-block-job-ui-preview | s11 Insight Board, s12 Question Book, s13 DataPrep |
| Theme Guide | s78-studio-type-theme-guide | s99 Insight guide |

These instances require no additional local Studio Type. The three Block kinds are not six Studio Types. A type's reference and a folder's number are different facts. Keep s99 and its authored content in place. Task procedures belong to their Task type/skill; guidance belongs to Theme Guide. Use only binding fields supported by the shared reader.

## Type catalogs

Each s01–s03 instance has types.md as its type-list source. Use the four section names below; every type has for, holds, source and owner. An absent section contains an explicit `absent:` reason instead of an invented entry. Owner fields resolve to real SKILL.md files. Responsibilities are semantic contracts: the examples have no universal job-type/task-type field.

| Block | Job group type | Job type | Task group type | Task type |
|---|---|---|---|---|
| Insight Board | Question version | Analysis | Preparation; Question level | Preparation execution; Question answer |
| Question Book | absent: Job is the version | Question-set version | Question level | Question definition |
| DataPrep | absent: Job is the version | Prep-code version | absent: steps ordered directly | Prep step |

The two views Job types and Task types come from shared `hai-studio/scripts/block_types_pages.py`; they are not hand-written button lists. Each generated page describes For/Holds. `structure_contracts.py` validates the catalog and adapts Insight content; shared Studio and mindmap renderers own its presentation.

## Fields, names and owners

| Kind | Real source and naming rule | Owning skill |
|---|---|---|
| Analysis / Question version | board-kind: insight-board; Job release, data and optional prep/prototype pins; jNN_data-vM_prep-vK_question-vN, or the actual two-version form without prep | hai-insight; hai-insight-bind |
| Preparation execution / Preparation | Board t01_prep-vK_〈slug〉 and its Job prep pin; the Task face and Run card | hai-insight; hai-insight-workflow |
| Question answer / Question level | Board tNN_〈L〉NN_〈question〉; Task question id resolves through the pinned release's question.md level | hai-insight; DIKWX level skills; hai-page-insight |
| Question-set version | board-kind: prototype; jNN_question-vN_〈slug〉 face and release.yaml | hai-insight; hai-insight-question |
| Question definition / Question level | release.yaml member paths resolve question.md id, level, ask, needs and agreement; tNN_〈L〉NN_〈question〉 | hai-insight-question; hai-insight-evidence-plan |
| Prep-code version | board-kind: insight-dataprep; jNN_prep-vK_〈slug〉 face | hai-insight |
| Prep step | ordered tNN_〈step〉; step.md goal/interface and scripts | hai-insight; hai-task-for-data under the prep contract |

The catalogs name exact owner paths. DIKWX labels are values of the Question level group. experiment/source/prepare are step names. Version ids and segments do not create types. Grouping adds no folders.

```text
Board   〈question-vN〉 → Job: 〈data-vM〉 × 〈prep-vK〉 → Preparation / DIKWX → Task
Book    Job: 〈question-vN〉 → DIKWX → Task: 〈question〉
Prep    Job: 〈prep-vK〉 → Task: 〈step〉
```

Book membership comes from release.yaml, not the local tNN directory count. Resolve every member relative to its release; retained questions reference their defining Task. Board prep occupies t01, shifting question Task positions; question id and source preserve the association. The Book Task's authority is question.md, not a fictitious tNN face.

DataPrep holds code steps, with step.md and scripts. The consuming Board prep Task executes the whole version in one Run and owns its runtime metrics and ready output. A computed question × segment is a Run below an answer Task. Citation-only questions need no fabricated compute ticket. Proposal triage and review are operations, not new Jobs or question types. Soft work Runs may exist at the version scope; they are not step execution outputs.

## Ordinary Work Studio organization

Structure › Studio describes the actual kind of Work Block. Number ranges come from `hai-studio/scripts/new_topic.py` BANDS; this is separate from the Blueprint's Studio Type registry. These are applicable responsibilities for new topics, not a required set of empty folders.

| Ordinary Work band | Insight Board topic purpose | Question Book topic purpose | DataPrep topic purpose |
|---|---|---|---|
| Concept · s01–s09 | 〈Research frame〉 · Block | 〈Question map〉 · Block | 〈Data conventions and chain〉 · Block |
| Level · s11–s19 | 〈Evidence by level〉 · Task | 〈Question needs and method〉 · Task | 〈Step interfaces〉 · Task |
| Report · s21–s29 | 〈Findings across Jobs〉 · Block/Job | 〈Version changes〉 · Job | 〈Preparation limits〉 · Job |
| Task procedure · s41–s49 | 〈Analysis and review〉 · Task | 〈Question review and release〉 · Job/Task | 〈Step code and review〉 · Task |
| Guide · s81–s89 | 〈Reading this Board〉 · Block | 〈Maintaining the Book〉 · Block | 〈Using this prep version〉 · Block |

Topic purposes and variable names use 〈〉. Each Studio stays with its actual Block, Job or Task. Number allocation is shared across a Block; keep all existing numbers, including a concrete s99 Guide or a report at another number. An actual example reads its existing bands, ordered groups and tags using the shared readers, with Other as fallback. It does not pretend these proposed categories are already configured. DataPrep currently has no actual Studio example. Execution evidence in a Prep report is a reference to Board Runs, never a copy.

## Structure and Draw

s01–s03 use Structure / Job types / Task types / Draw / Skills. Folder, Job-Task and Studio pair naming rules with available actual examples. Fixed names follow contracts; variable slots use 〈placeholders〉. Real examples are folded under the relevant rule; the shared corner dot opens their owning Block. An absent actual Studio is omitted.

Structure uses the existing Folder Tree for all three content items and their inline examples. It is a vertical list with indentation, branch lines and native details/summary; each work level uses its existing colour. Names wrap at normal size. Rule nodes carry purposes and type responsibilities on hover, and actual nodes link their authoritative source. Folder opens down to the Job; semantic groups expand in place.

Structure stays on `folder-rules`, `jobs-rules` and `studio-rules`; it must never select a Draw fragment or render mindmap cards. S71 Draw requires one owned Excalidraw canvas, full width. The three structure Studios currently have no such canvas, and their separate map bindings do not satisfy that requirement; T44 records this gap. Preserve source identities, authored words, notes and descendants through refresh. Skills previews actual owning SKILL.md files.

## Job preview contents

s11–s13 bind Page-Job / Page-Task / Job types / Task types / QuickHtml / Draw with studio-views.json. Page-Job marks navigation, Brief, Tasks and Findings on the existing Block page. Page-Task selects a real Task in that Block. Contract views reference the owner. QuickHtml retains Segment grid, Version changes and Steps and Runs as proposals. Draw preserves the existing mindmap and editable canvas. This Studio type needs no independent Delivery or Instances view; do not apply that rule to other types.

Brief states motivation, evidence, goal and version pins. Plan + Results pairs planned work with its result and obstacles. Findings states what was learned with evidence references. For a Book version, changes include addition, modification, retention and retirement; its Tasks define how questions can be answered. Prep Tasks define step interfaces and reviews, with runtime evidence referenced from Board Runs. A source file or finding is recorded once and referenced across scopes; a new synthesis links its basis.

Record implementation comparisons in the existing Checklist. Structure/proposals do not demonstrate live support for retained Book members, semantic prep grouping or type-to-instance comparisons. Read and drive the actual page before marking a case fixed. Phone layout belongs to the shared renderer; do not shrink text to hide clipping.

## Shared interfaces still to complete

- Shared block_types_check.py requires every section to be nonempty and can pass a tree with no catalogs. The local check requires all three catalogs and validates explicit absence. Do not fabricate types or report zero catalogs as success.
- Shared block_types_pages.py member matching reads only job-type/task-type, not Insight release.yaml, question.md or step.md. Its populated member links use child paths. Complete membership remains in the inline Job-Task example until shared adapters and Block selection routes support it. Do not modify real research records to satisfy that reader.
- Type-page For/Holds generation, structure acceptance and execution-harness acceptance are separate results. T34 tracks the live reader; T36 tracks phone clipping; T41 tracks shared type checking/membership.

## Verify

```text
uv run --python 3.13 --with pyyaml python examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/check_structure.py
uv run --python 3.13 --with pyyaml python examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_job_previews.py --check
uv run --python 3.13 --with pyyaml python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/block_types_pages.py <s01-or-s02-or-s03-folder> --check
```

Use the running workbench's Python environment when available; shared UI imports require Python 3.10 or newer. The local checks cover catalogs, valid absence, owner files, full Book membership, Board pins, prep ownership, Structure Folder Trees, negative rejection of mindmap content/bindings, separate Draw, authored changes, real Studio owners/bands and generated freshness. Then open the three instances within b11, expand Structure trees and actual examples, inspect both type views and source links, and inspect phone layout separately. Verify Draw independently. Fresh-context skill invocation must distinguish all three Block kinds and their signing boundaries. Record results in the active Trace and current topics; a case without a guard remains open.
