s03 · Block Structure: Paper
==========================================
view: overview

**Tags:** `Structure`

**Studio Type:** [Block Structure](../../b17_theme_work/s71-studio-type-block-structure/elements.md).

**For:** the folder, Job/Task types and Studio organization of a Paper Block.

**Delivery type:** skill

**Topic:** Define a Paper Block through the shared Block Structure Studio Type, with real skill sources and explicit execution boundaries.

**Source:** [Shared Block Structure requirements](../../b17_theme_work/s71-studio-type-block-structure/elements.md), [type catalog](types.md), [Studio organization](structure/studio.md).

**Files:** Structure reads the Folder, Job-Task and Studio outlines through the shared folder-tree renderer. Level colours and hover purposes follow S71. Type views read types.md; Draw opens one canvas; Examples opens real Block views.

## Design record

Connected organization map

--------------------------

[Job Type → Job Name → Task Type → Task Name](structure/jobs.html) is the primary organization in both Structure and Draw. Each parent appears once in its branch. Group labels remain metadata, not extra type levels. Jobs without mapped Tasks end at the Job Name. Names describe design examples; † marks a missing contract and ‡ marks a legacy type conflict. The existing Excalidraw canvas remains an Overview of groups and Studio topics.

The user clarified: “不是，我意思是做一个mind map一样的炊，你懂吗。” (2026-11-27, verified in the Work session). This presentation supersedes the earlier table/combined-node overview as the primary organization view.


Views of this structure Studio
------------------------------

Use the shared top-controls / left-entries / right-content arrangement. These are content definitions for the existing renderer, not a second page shell.

| Top view | Left entries | Right content |
| --- | --- | --- |
| Structure | Jobs and Tasks; Studio organization | Paper’s named groups and the Job Type / Job Name / Task Type / Task Name mapping |
| Draw | Jobs & Tasks; Overview | The shared connected organization map and retained group overview |
| Examples | Paper-Example | The existing Paper example, whose legacy organization is documented below |
| Skills | The relevant skills | The picked skill's functions, inputs, outputs, execution flow, checks and design delivery |

**Skills is one top-view item here.** A skill may have many functions in its content. This design creates no separate Studio per skill and no cross-skill Structure/Workflow/Checks Studios. The Skills entries reference the owning contracts rather than copying their full instructions.

Structure contains both the Job/Task hierarchy and Studio organization as left entries. Draw names the Paper groups and work directly. Example entries use the real Block’s name; no numbered display aliases or fabricated routes are introduced. The legacy Paper-Example is not evidence that the proposed five-group mapping is implemented.

Jobs and Tasks: Paper organization
---------------------------------

The five Job groups are **Story / Evidence / Display / Writing / Presentation**. A group organizes selection. A Job Type chooses a contract; a Job Name identifies the particular work. Task Type and Task Name make the same distinction within that Job. None of these semantic groups adds a directory layer.

| Job group | Job Type | Job Name | Task group | Task Type | Task Name |
| --- | --- | --- | --- | --- | --- |
| Story | Story (target; Job contract to define) | Shared story | Questions / Argument / Narrative | Story output (Task contract to define) | Research question / Contribution / Section outline |
| Evidence | Evidence (consolidated target) | Shared evidence | Values | Current face: `value`; absent from shared registry | Reported estimates |
| Evidence | Evidence (consolidated target) | Shared evidence | Citations | Current face: `evidence`; conflicts with base numeric executor contract | Source verification |
| Evidence | Evidence (consolidated target) | Shared evidence | Checks | Current value/citation type reused; no separate check type | Evidence audit |
| Display | Display (`job_kind=display` today) | Main / Appendix / Explore | Figures / Tables | Final Paper asset; no registered `task-type` key | Study workflow / Results table |
| Writing | Writing Version (current reader contract) | Manuscript / Revised manuscript | Main text / Appendix | `draft` | Abstract / Methods / Supplement |
| Writing | Writing Version | Revised manuscript | Review | `draft` for response prose; feedback records retain provenance | Reviewer response |
| Writing | Writing Version | Manuscript / Revised manuscript | Submission | `draft` for letter; portal/packaging type needs definition | Cover letter / Portal fields |
| Presentation | Presentation (target; format contract to define) | Slides / Video / Poster | Content / Delivery (proposed) | Media deliverable type needs definition; authored prose can use `draft` | Slide deck / Script / Poster / Speaker notes / Captions / Export |

These are named design examples, not assertions that new Jobs were created. Main, Appendix and Explore are Display Job roles/names, not three new types. Likewise manuscript versions and presentation formats must not become new types merely because their names differ. Story and Evidence normally have one shared Job; output groups may hold multiple Jobs.

**Type evidence and unresolved conflicts.** The current [Paper Job reader](../../../../../plugins/haipipe-toolkit/servers/workbench-paper/paper_jobs.py) infers display/value/citation/submission branches from names and recognizes Writing Version. It does not register the proposed Story, consolidated Evidence or Presentation Job contracts. Current Jobs generally carry no `job-type:` field. The [shared Task registry](../../../../../plugins/haipipe-toolkit/skills/1_base/task/hai-task/ref/types.md) registers `draft` and `evidence`, but no `value`. Current Paper value faces use `value`; citation faces use `evidence`, whose [base owner](../../../../../plugins/haipipe-toolkit/skills/1_base/task/10_evidence/hai-task-for-evidence/SKILL.md) instead specifies numeric extraction. This is a contract conflict to resolve, not a new field to invent.

The registered [display Task](../../../../../plugins/haipipe-toolkit/skills/1_base/task/7_display/hai-task-for-display/SKILL.md) prepares upstream summary data; it does not produce the final Paper figure/table. A final asset’s `type: figure` or `type: table` is its asset kind, not proof of a registered Task Type. Current portal Tasks say `description`, while the base owner means a stored table’s description; portal execution needs an explicit contract. The design preserves existing files while identifying these gaps.

Studio organization
-------------------

| Studio group | Named Studio topic | What it settles |
| --- | --- | --- |
| Story | Argument design | Which question, contribution and narrative the shared Story should express |
| Display | Figure composition | How evidence becomes the main and appendix figures |
| Writing | Venue fit | How the manuscript responds to the selected venue’s requirements |
| Presentation | Talk narrative | How the paper is told to a particular audience |

These are concrete topic proposals, not mandatory pre-created folders. A topic holds an open design question; a Job Task produces or checks its deliverable. Studio groups are metadata, while each topic has an sNN folder beside the Jobs. This blueprint’s Idea, Grant and Paper structure Studios are not copied into research Paper Blocks.

Folders and ownership
---------------------

This is the physical ladder beneath both navigation views. Space folders appear when their first content exists.

```text
paper/Paper-<slug>/
├── board.md
├── jNN_<job>/
│   ├── jNN_<job>.md
│   └── tNN_<task>/
│       ├── tNN_<task>.md
│       └── runs/<run>/                 the shared Run/Result contract
├── sNN-<studio-topic>/                 beside Jobs, not a Job group
│   ├── sNN-<studio-topic>.md
│   ├── sNN-<studio-topic>.mindmap.md
│   └── sNN-<studio-topic>.excalidraw
├── related/                           incoming material, kept once
├── venues/<target>/                   requirements for a named target
├── trace/                             work history
└── delivery/jNN_<job>/tNN_<task>/<lane>/
```

Only the Block has a physical `delivery/` root. Job-level output uses `delivery/jNN_<job>/<lane>/`; a Studio keeps its design artifacts through the shared Studio contract. Runs and Results remain at their source. Group names add no folder level.

Shared Workbench behavior
-------------------------

The owning Block retains its title and route during Job, Task and Studio selection. In Jobs, the selection sequence is **Job topic → Job → Main or Task topic → Task**. Main hides the Task row; returning to a Task topic restores the last selected Task.

Main uses **Overview → Tasks → Findings**. Overview is one Brief fold with Goal, Requirements and MindMap; MindMap has Topics and Work Structure. Tasks show their actual work and Runs. Findings show produced Values, Displays and Reports. Questions and feedback stay beside their source and in the title tray. No separate page or copied navigation shell is created for these examples.

Paper ownership and grouping rules
----------------------------------

A Paper Block owns one manuscript project. The following five **Job topics/groups** use the shared Work hierarchy with the named organization above. Job types remain separate: Main, Appendix and Explore are roles for Jobs of the Display type. Presentation formats require different workflows; their exact type fields remain to be registered.

| Job topic | One Job represents | Usual multiplicity | Task topics and examples |
| --- | --- | --- | --- |
| Story | The shared research question, contribution and argument | Normally one shared Job | Questions, Argument, Narrative |
| Evidence | The paper's reusable claim-to-evidence record | Normally one shared Job | Values, Citations, Checks |
| Display | A figure/table collection with one role | Main, Appendix and Explore as needed | Figures, Tables; one figure/table per Task |
| Writing | One manuscript version for a target and purpose | As many versions as needed | Main text, Appendix, Review, Submission |
| Presentation | One audience/occasion/format deliverable | Slide decks, videos and posters as needed | Format-specific outline, content, composition, notes/captions and export |

**Review and Submission are Task topics/groups inside the relevant Writing Job.** Review reconciles a feedback batch, revises affected text and produces responses. Submission prepares the cover letter, portal fields and upload package. Feedback remains linked to its exact source and build; an answering version references those records. Preparing the package does not submit it.

Default Story and Evidence Jobs appear when their first work exists. Display, Writing and Presentation Jobs are added for actual roles, versions and audiences. Do not create every example or empty group merely to fill the design.

The source Idea remains a separate Job in its Idea Block, with its Card, assessments, lineage and human selection. Paper stores reciprocal pointers and the selected revision. Work owns computation; Discovery owns source acquisition. Evidence binds claims to returned Results and verified sources. Story owns the scientific argument; Display owns figure/table composition. Writing and Presentation select explicit revisions of that shared material and own their wording/composition.

Related is reachable from Idea and Story, and Story by Section from Story and Displays; each pair reads one source. Grant has its own type mapping in s02.

Q01 · Answer
------------

**Answer:** Job topics group real Jobs; Task topics group real Tasks within each Job. Studio groups organize separate sNN records alongside the Jobs. Paper maps its five Job groups onto this common shape.
**Evidence:** The named type/name mapping and [drawing](s03-paper-block-structure.excalidraw).
**Limits:** The current Paper scaffold still uses earlier evidence/submission/review Job roles.

Q02 · Answer
------------

**Answer:** Incoming records, target requirements and the Delivery root belong to the Block. Job/Task outputs keep their identity in Delivery subtrees; grouping introduces no storage layer.
**Evidence:** The folder shape above and the [delivery contract](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/ref/paper-ladder.md).
**Limits:** This draft moves no source or frozen output.

Q04 · Answer
------------

**Answer:** A candidate remains in its source Idea Job. The proposed Paper Story Job develops the shared argument; Studio topics keep the human design discussions. Skills are read in this structure Studio's Skills top view.
**Evidence:** [Idea source contract](../../../../../plugins/haipipe-toolkit/skills/1_base/ideation/hai-ideation/references/idea-block.md) and the ownership distinctions above.
**Limits:** The current Story-artifact migration still needs implementation; this Studio uses the shared top-view reader.

Current support and design still owed
------------------------------------

Current Paper contracts read Paper/Grant Blocks, writing versions, draft Tasks and Block-owned Delivery. The Idea source contract preserves linked candidate Jobs. Shared Work navigation already embeds Job/Task selections and Brief/Tasks/Findings; shared Studio groups are tags over real sNN folders.

The named drawing is a design, not newly populated research data. Structure / Draw / Examples / Skills uses the shared authored Studio views. It does not implement the missing Paper Job/Task contracts. The Paper scaffold still creates three evidence Jobs and a Submission Job, the comments contract still gives feedback batches Review Jobs, and Story is authored through Studio topics. Those compatibility records differ from the target Paper mapping. Semantic grouping, Story/Evidence regrouping, Display roles, Presentation contracts, migration and rendered examples remain owed.

Sources and history
-------------------

- [Paper router](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/SKILL.md) and [existing ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/ref/paper-ladder.md).
- [Idea source contract](../../../../../plugins/haipipe-toolkit/skills/1_base/ideation/hai-ideation/references/idea-block.md).
- [Story owner](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-story/SKILL.md), [Evidence owner](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/SKILL.md), [comments owner](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-comments/SKILL.md), [assembly owner](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-assemble/SKILL.md).
- [Current Work Job UI decisions](../../b17_theme_work/s11-work-job-preview/s11-work-job-preview.md) and [shared Job navigation](../../../../../plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py).
- Earlier decisions remain in the former [Paper tree concept](../_archive/20261127/s01-paper-tree-concept/s01-paper-tree-concept.md), [Paper Studio](../_archive/20261127/s02-paper-studio/s02-paper-studio.md) and [Paper Delivery](../_archive/20261127/s03-paper-delivery/s03-paper-delivery.md) in the archive. Those topics were preserved under `../_archive/20261127/` when these structures were installed. Their dated decision identities remain historical and are not reassigned to this s03.

Files
-----

```text
s03-paper-block-structure/
├── s03-paper-block-structure.md
├── s03-paper-block-structure.mindmap.md
├── s03-paper-block-structure.ideas.md
├── s03-paper-block-structure.excalidraw
├── s03-paper-block-structure.png
├── .s03-paper-block-structure.seed.json
└── build_s03_paper_block_structure.py
```

The seed belongs to the shared canvas writer and preserves human marks on rebuild. Build with Python 3.12+ and Pillow: `python3 build_s03_paper_block_structure.py --repo-root <Tools-SPACE>` while staged; the installed builder discovers the repository.

Decided
-------

Current user decisions, recorded 2026-11-27; these do not mark the implementation complete.

s03-D01 · s01 designs Idea, s02 Grant and s03 Paper Block structure.
s03-D02 · Superseded: the earlier generic example-name drawing is replaced by named Paper groups and work (s03-D07).
s03-D03 · Studio group → Studio topic shows another grouping over real sNN records beside Jobs.
s03-D04 · Structure, Draw, Examples and Skills are top views of this same structure Studio; no new skill Studio is required.
s03-D05 · Paper maps Story, Evidence, Display, Writing and Presentation onto the common Job-topic shape.
s03-D06 · Review and Submission stay inside Writing; default shared Story/Evidence and multiple output Jobs retain their ownership.
s03-D07 · The primary design names Story, Evidence, Display, Writing and Presentation, and distinguishes Job Type, Job Name, Task Type and Task Name; groups cannot substitute for types. The user’s 2026-11-27 correction supersedes generic numbered labels.
s03-D08 · Missing type registrations and conflicts between current faces and owners remain explicit. Showing a named design is not permission to fabricate a runtime type or migrate research records.

Open
----

1. Which explicit shared fields distinguish topic/group, type, role and instance name while preserving legacy addresses?
2. How should Paper-Example be migrated from separate evidence/submission/review Jobs under a separately scoped implementation?
3. How should the same Studio's Skills view connect each function's inputs, outputs and checks to the agreed type definition?
4. Which existing Story artifacts become references versus Job-owned outputs during Paper migration?
