---
name: workbench-insight
description: 'Open and explain Insight Board, Question Book and DataPrep within the shared Block workbench. Inspect
  current source records, Studio definitions, Job and Task selections, and distinguish live UI from proposals. Trigger:
  insight workbench, Insight UI, Question Book UI, /workbench-insight.'
metadata:
  version: 1.7.1
  last_updated: '2026-11-27'
---

# /workbench-insight

Read [CONSTITUTION.md](CONSTITUTION.md), the shared `workbench` skill and `hai-ui` before changing a page. This skill supplies Insight content; the shared Work renderer owns navigation, layout, Files, Checklist and previews.

## Open the right Block

For theme design, open `examples/Project-Ladder/blueprint/b11_theme_insight` and select its Studio. For actual work, open the requested Block. Resolve its kind from `board.md`, not its directory name. Use `/_board/workbench?path=<Block>&layout=focus`; Job and Task selections stay in that Block through `section=jobs`, `group=jNN` and `task=tNN`. Confirm the title and selection in the real browser. Deliver a verified Tailscale Block URL when the user needs phone access; generated HTML is embedded content.

## Interpret the three kinds

| Block kind | Job | Task | Source |
|---|---|---|---|
| `insight-board` | fixed question release × data version × prep version when used | prep execution or one question's answer | Job pins, question id, Run cards and results |
| `prototype` (Question Book) | one question-set version | question definition, needs, method and review | release.yaml membership and each referenced question.md |
| `insight-dataprep` | one prep-code version | one ordered code step | version face, step.md and scripts |

Question versions group Board Jobs. DIKWX groups question levels; it does not create new folder levels. Book and Prep versions are Jobs themselves. A version id, a segment and a step name are not new types. The current examples have no universal `job-type:` or `task-type:` field.

A Book version may include source Tasks held in other version directories: resolve every `release.yaml` member before counting or describing its questions. A Board question × segment is a Run. DataPrep's whole chain executes in one Board prep Task Run; a code step does not own those execution outputs. A prep Task occupies the first Board position, so match questions by id and source rather than assuming the Book and Board tNN always match.

## Read each scope

- Block: the whole question family, data/prep versions, Jobs, proposals and cumulative Findings.
- Job Main: Brief explains motivation, evidence, goal and version pins; Plan + Results keeps the intended work beside its outcome and obstacles; Findings states what was learned and links its basis.
- Selected Task: the specific question or step, its method and evidence, work/results and review. Book Tasks define questions; Board Tasks answer them; Prep Tasks define code steps.

One file or finding has one authoritative source. Higher scopes reference it. A new synthesis gets its own record and references its supporting results. Do not copy a question, result or finding just to display it twice.

## Studio

Read [ref/block-structure.md](ref/block-structure.md) for the concrete contracts and validation commands.

Band is a shared outer category; Studio Type defines an instance's content and views. Read the shared Band registry in b17 and reference its type definitions. Do not copy that registry or create empty local type groups. Actual Work Blocks show Studio instances without requiring type-definition pages.

- s01–s03: Insight Board, Question Book and DataPrep instances of Block Structure. Structure / Job types / Task types / Draw / Skills. Folder, Job-Task and Studio content each holds its rule and available real example. Read each instance's types.md: Job group, Job, Task group and Task are separate categories, with for/holds/source/owner for every type. Missing layers have explicit absent reasons. Shared block_types_pages.py generates type pages; no new example schema fields are needed.
- s11–s13: the three instances of Block Job UI Preview. Page-Job / Page-Task / Job types / Task types / QuickHtml / Draw. Live selections retain their example Block. The existing Segment grid, Version changes and Steps and Runs live in QuickHtml until their cases are implemented.
- s99: Insight Theme Guide, referencing Work's Theme Guide definition. Keep its directory and authored content.

The Studio rule inside each Block Structure describes the ordinary Work Block: use shared new_topic.py numbering and place each topic at its actual Block/Job/Task owner. Proposed purposes use 〈names〉. Actual examples read configured bands, group order and tags through shared readers. Blueprint categories do not replace that Work organization.

Structure uses the existing vertical Folder Tree for Folder, Job-Task and Studio, including their inline examples. Use native details/summary, branch lines, level colours and source links. Do not bind a mindmap to Structure. Draw is separate: S71 requires one owned Excalidraw canvas. The current s01–s03 Draw binding lacks that canvas; T44 tracks this gap. Do not treat the preserved map presentation as S71 Draw acceptance. Preserve authored words, notes and branches; keep readable names without font scaling.

## Evidence and boundaries

Read the real page and code before asserting a view is implemented. Record UI gaps in [ref/topics.md](ref/topics.md), with the case and a guard. The local structure check requires all three catalogs and accepts only documented absent layers. Shared type checking still requires nonempty layers, and its member reader does not resolve Insight releases; use the complete inline examples and keep those shared interfaces open. Check retained Book membership, prep grouping, phone layout and Checklist integration independently; a successful structure render does not fix the live Job reader. check_structure.py must reject mindmap markup or a Draw fragment bound to Structure.

Run cards are defined by `hai-insight-workflow/ref/run-cards.md`. Their routing classifications do not define the Studio's top buttons. Execution belongs to the skill and agent on the card. A person's CHECK or close action is accepted only through the existing action route and its file-backed gates. Do not infer review or signature from a visible result.

No patient row appears on the workbench. Display aggregates, source references and generated results. Shared component changes and server restarts belong to the shared owner; theme content changes do not authorize a restart.
