s02 · Block Structure: Grant
==========================================
view: overview

**Tags:** `Structure`

**Studio Type:** [Block Structure](../../b17_theme_work/s71-studio-type-block-structure/elements.md).

**For:** the folder, Job/Task types and Studio organization of a Grant Block.

**Delivery type:** skill

**Topic:** Define a Grant Block through the shared Block Structure Studio Type, with real skill sources and explicit execution boundaries.

**Source:** [Shared Block Structure requirements](../../b17_theme_work/s71-studio-type-block-structure/elements.md), [type catalog](types.md), [Studio organization](structure/studio.md).

**Files:** Structure reads the Folder, Job-Task and Studio outlines through the shared folder-tree renderer. Level colours and hover purposes follow S71. Type views read types.md; Draw opens one canvas; Examples opens real Block views.

**Example:** [Grant-Example](../../../paper/Grant-Example/board.md). Examples reads its actual Folder, Jobs and Studio through the shared Block page. Content is illustrative; scientific results, completed assessments and human selection are not asserted.

## Design record

Connected organization map

--------------------------

[Job Type → Job Name → Task Type → Task Name](structure/jobs.html) is the primary organization in both Structure and Draw. Each parent appears once in its branch. Group labels remain metadata, not extra type levels. Jobs without mapped Tasks end at the Job Name. Names describe design examples; † marks a missing contract and ‡ marks a legacy type conflict. The existing Excalidraw canvas remains an Overview of groups and Studio topics.

The user clarified: “不是，我意思是做一个mind map一样的炊，你懂吗。” (2026-11-27, verified in the Work session). This presentation supersedes the earlier table/combined-node overview as the primary organization view.


Grant structure
---------------

Grouping metadata follows **Job group → Job → Task group → Task**; the primary map uses the four type/name levels above. Grant uses meaningful names at each level:

| Job group | Job | Task group → Task examples |
| --- | --- | --- |
| Story | Research case | Aims → Specific aims; Rationale → Significance; Approach → Research plan |
| Evidence | Preliminary evidence | Values → Pilot measurements; Citations → Closest work; Checks → Source provenance |
| Display | Main; Appendix; Explore | Figures → Study design; Tables → Feasibility summary |
| Writing | Letter of intent; Full application; Revision | Application → Research strategy; Attachments → Budget justification; Review → Reviewer response; Submission → Upload package |
| Presentation | Slides; Video; Poster | Content → Research pitch; Production → Deck, video or poster; format-specific review and export |

The Job and Task titles above are **design examples**, not claims that those records already exist. The call determines which application sections and attachments are needed. Each group can hold several records; the normally shared Story and Evidence Jobs have explicit scope rather than a numbered placeholder name.

Studio organization follows **Studio group → Studio topic**. Illustrative discussions are Research design → Aims and rationale, and Communication → Application narrative. These are optional design topics, not a mandatory set to scaffold. A topic is an `sNN` record beside the `jNN` Jobs; a Task is a `tNN` record inside its Job. All group labels are metadata, with no extra folder level.

The same structure Studio declares these top views in its installed manifest. Each uses shared top controls, left entries and right content. A view with one item uses the full width; an unbound Examples view is omitted.

| Top view | Left entries | Right content |
| --- | --- | --- |
| Structure | Jobs & Tasks; Studio | Named Grant Job and Task groups, their records, Studio organization and ownership rules |
| Draw | Jobs & Tasks; Overview | The shared connected organization map and retained group overview |
| Examples | Actual names of bound Grant Blocks | Real example Blocks rendered by the shared page; no invented names or routes |
| Skills | The relevant skills and their functions | Inputs, outputs, workflow and checks for the selected function |

Structure contains both the Job/Task hierarchy and Studio organization as left entries. Examples entries appear only when bound to real example Blocks and their routes have been checked; this draft supplies no fabricated bindings.

Skills stays a top view in **this same Studio**. A skill can have multiple functions within its entry. There is no separate skill Studio for each skill or function. The `hai-block structure` interface will read the theme's structure definition; its generic input and output contract remains shared.

Types, names and groups
-----------------------

A **Job group** organizes Jobs. **Job Type** selects a behavioral contract; **Job Name** identifies an instance. A **Task group** organizes that Job's Tasks. **Task Type** selects the Task's skill and workflow; **Task Name** names its deliverable. Group, type and name are distinct, even when a visible word happens to coincide.

| Job group / Task group | Job Type | Job Name | Task Type | Task Name | Contract evidence and limit |
| --- | --- | --- | --- | --- | --- |
| Story / Aims | Proposed; no Story Job type in the current Paper reader | Research case | `draft` for a prose Page; Grant Story adapter proposed | Specific aims | Reuses the registered prose workflow; a research assessment is not automatically a draft |
| Evidence / Values | Proposed consolidated Evidence Job contract | Preliminary evidence | Unresolved Grant mapping; legacy Paper uses unregistered `value` | Pilot measurements | Proposed consumer of returned Work Results; do not equate the legacy value reader with the numeric executor |
| Evidence / Citations | Same proposed consolidated contract | Preliminary evidence | Unresolved Grant mapping; legacy Paper writes `evidence` with a conflicting meaning | Closest-work citation check | Citation validation differs from the registered numeric executor; ownership and routing need reconciliation |
| Display / Figures | Existing reader kind `display`; shared role-based Job contract proposed | Main, Appendix or Explore | Final-asset type unresolved | Study design figure | Registered `display` owns upstream summary data, not the final Paper/Grant asset |
| Writing / Application | Existing reader label **Writing Version**; explicit field contract proposed | Full application | `draft` | Research strategy | The existing section scaffold writes `task-type: draft`; call-specific structure remains proposed |
| Writing / Attachments | Same Writing Version contract | Full application | `draft` for authored prose only | Budget justification | Uploaded forms or files need their own task contract; the call decides what exists |
| Writing / Review | Same Writing Version contract | Revision | `draft` for the written response | Reviewer response | Intake of feedback and its receipt is separate from response prose; migration remains proposed |
| Writing / Submission | Same Writing Version contract | Full application | Packaging Task type unresolved | Upload package | Submission remains a Task group; no new Submission Job or permission to send |
| Presentation / Content | Presentation Job contract unresolved | Slides, Video or Poster | `draft` for authored script/prose | Research pitch | Production/export contracts remain unresolved; the format name is not itself a registered type |

The [Paper Job reader](../../../../../plugins/haipipe-toolkit/servers/workbench-paper/paper_jobs.py) currently infers `display`, `value`, `citation` and `submission` branches from folder names and separately identifies Writing Version. The [scaffolder](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/scripts/paper_ladder.py) does not emit an explicit `job-type:` field for these Jobs. The new design therefore cannot claim that its five groups are five registered `job-type` values.

These Grant Job and Task names are proposed targets, not current Grant records. The [Task type registry](../../../../../plugins/haipipe-toolkit/skills/1_base/task/hai-task/ref/types.md) registers `draft` and `evidence`, but not `value`. The actual [Paper value face](../../../paper/Paper-Example/j02_evidence_value/t01_values-sample/t01_values-sample.md) declares `task-type: value` and reads returned measurements. The [Paper citation face](../../../paper/Paper-Example/j03_evidence_cite/t01_cite-prior-work/t01_cite-prior-work.md) and [citation scaffold](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper-evidence/scripts/cite_tasks.py) declare `task-type: evidence` for bibliographic and source-card checks. That conflicts with the registered [Evidence executor contract](../../../../../plugins/haipipe-toolkit/skills/1_base/task/10_evidence/hai-task-for-evidence/SKILL.md), whose worker computes or extracts numbers into `values.yaml`. These are observed legacy inconsistencies, not a resolved common Evidence Task type. Grant Values, Citations and Checks need an explicit consumer contract and routing decision before scaffolding. The [display-input contract](../../../../../plugins/haipipe-toolkit/skills/1_base/task/7_display/hai-task-for-display/SKILL.md) explicitly excludes ownership of the final asset. Neither the Main/Appendix/Explore roles nor Slides/Video/Poster formats justify inventing new type values.

Grant type rules
----------------

A Grant is its own Block, `paper/Grant-<slug>/`, beside Idea and Paper. It uses the shared Work framework. An Idea may support a Grant and a Paper through separate links; neither destination consumes or renames the source Idea Job.

| Job group | What one Job represents | Expected multiplicity | Task groups and examples |
| --- | --- | --- | --- |
| Story | The shared research case: aims, rationale and approach | Normally one shared Job | Aims; Rationale; Approach — hypothesis, significance, milestones, risks and alternatives |
| Evidence | The shared evidence register with source bindings | Normally one shared Job | Values; Citations; Checks — preliminary findings, closest work, feasibility and provenance |
| Display | A collection of figures/tables serving a role | Main, Appendix and Explore Jobs as needed | Figures; Tables — a Task owns one figure/table, its source bindings, rendering and verification |
| Writing | One application version for a named call and stage | LOI, full application and later revisions as needed | Application; Attachments; Review; Submission |
| Presentation | One communication output for an audience or occasion | Slides, Video and Poster Jobs as needed | Format-specific content, production, review and export Tasks |

These are five **Job groups**, not a claim that there are five registered runtime Job types. Main, Appendix and Explore are Display Job roles. LOI and full application are Writing contexts. Presentation can have distinct output types. The exact Job Type / Job Name / Task Type / Task Name mapping above separates current contracts from the remaining implementation decisions.

Review and Submission belong to the relevant Writing Job. A review Task keeps the received source and the exact application build it addresses; a response or later version refers to that record. Submission Tasks prepare the cover letter, portal fields and upload package. They do not imply permission to submit.

The call defines the Application and Attachments Task menu. Typical content includes specific aims, research strategy, milestones, team responsibilities, budget justification and required forms. Create only required work. Proposed experiments and anticipated outcomes belong to the approach; they are never recorded as completed evidence.

Sources and dependencies
------------------------

- The funding call and its requirements are owned once in `venues/<call>/`; versions refer to their relevant requirement revision. Material retargeting keeps provenance visible.
- Story owns the shared rationale and research plan. Writing versions record the Story revision they use, then own their application wording and call-specific emphasis.
- Work Tasks own computation and returned measurements. Discovery owns source acquisition and readings. Evidence binds those owner Results and verified citations; it does not copy raw datasets or recompute them.
- Display owns renderable figures/tables and their evidence bindings. Writing and Presentation select those assets and their revisions. A target-specific rendering does not create a second source fact.
- An Idea-to-Grant source link preserves the Idea identity and decision. A complete Grant handoff adapter is still proposed; the current scientific selection contract implements Paper destinations.

Physical folders
----------------

Groups are navigation metadata, not an extra folder level. Allocate unused Job and Task numbers; the numbers do not define the group.

```text
paper/Grant-<slug>/
├── board.md
├── venues/<call>/call.md
├── jNN_<job>/
│   ├── jNN_<job>.md
│   └── tNN_<task>/
│       ├── tNN_<task>.md
│       └── runs/<run>/                 Run and its Result keep their source identity
├── sNN-<topic>/                        discussion and design
├── related/                           received material, kept once
├── trace/                             the work record
└── delivery/jNN_<job>/tNN_<task>/<lane>/
```

The Block owns the only physical `delivery/` root. Assembly outputs may live at `delivery/jNN_<writing>/`; Task lanes keep the deeper Task path. A new version references prior reviews and shared evidence, retaining immutable old sends and receipts.

What the Block page shows
-------------------------

The common navigation remains **Job group → Job → Main / Task group → Task**, inside the Grant Block's title and route. Main hides the Task row. Groups and Jobs restore their own selections.

Main reads **Overview → Tasks → populated Findings**. Overview has one Brief with Goal, Requirements and MindMap; the map separates Topics and Work Structure. A selected Task shows its question or deliverable, inputs, appropriate workflow controls, Runs and outputs. Findings are actual Values, Displays or Reports, never a replacement for feedback. Feedback and decisions stay beside their source items and in the shared tray.

Grant-specific Main content follows ownership: Story shows aims and rationale; Evidence shows linked preliminary findings and limitations; Display shows the chosen role's assets; Writing shows the selected application's sections, requirements and package; Presentation shows its audience, narrative and produced format.

Q01 · Answer
------------

**Answer:** Story, Evidence, Display, Writing and Presentation are Grant's Job groups. Their meaningful Jobs, Task groups and deliverables make the shared hierarchy concrete. Studio groups organize named discussion records beside those Jobs; groups add no folder layer.

**Evidence:** [Structure drawing](s02-grant-block-structure.excalidraw) · [structured map](s02-grant-block-structure.mindmap.md).

**Limits:** The grouping and specialized Main content are the agreed design direction, not implemented runtime claims.

Q02 · Answer
------------

**Answer:** Call requirements, received resources and the Delivery root belong to the Block. Each output retains its Job/Task source address inside that root.

**Evidence:** [Block contract](../../../../../plugins/haipipe-toolkit/skills/1_base/project/hai-block/SKILL.md) · [Paper ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/ref/paper-ladder.md).

**Limits:** A call's actual attachment slots must come from that call, not this generic structure.

Q03 · Answer
------------

**Answer:** Review and Submission are Task groups inside a Writing version. Revisions preserve links to the exact feedback source and prior build.

**Limits:** Existing helpers still create separate Submission and Review Jobs. Moving that content needs a migration design preserving old addresses and receipts.

Live and proposed
-----------------

The [Paper router](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/SKILL.md) and [scaffold](../../../../../plugins/haipipe-toolkit/skills/3_theme/paper/hai-paper/scripts/paper_ladder.py) already support `Grant-<slug>` with `board-kind: grant-board`. The existing [Paper Job reader](../../../../../plugins/haipipe-toolkit/servers/workbench-paper/paper_jobs.py) still has the older separate display/value/citation/submission branches. Grant-specific section templates, the five-group reader, the revised scaffold and Idea-to-Grant handoff remain to implement. This drawing is a design, not a live application example.

The shared [Job navigator](../../../../../plugins/haipipe-toolkit/servers/workbench/page/job_task_views/focus_jobs.py) and [Brief](../../../../../plugins/haipipe-toolkit/servers/workbench/page/job_task_views/job_overview.py) supply the common page components. A theme supplies content to them; it does not build a separate navigation shell.

Files
-----

- [Face](s02-grant-block-structure.md), [mind map](s02-grant-block-structure.mindmap.md) and [open choices](s02-grant-block-structure.ideas.md).
- [Drawing](s02-grant-block-structure.excalidraw), [preview](s02-grant-block-structure.png) and [builder](build_s02_grant_block_structure.py).
- `.s02-grant-block-structure.seed.json` is the shared canvas writer's annotation-preservation record.

Decided
-------

s02-D01 · Grant is a separate Block alongside Idea and Paper; it shares the Work framework (user decision, 2026-11-27).
s02-D02 · Paper and Grant use Story, Evidence, Display, Writing and Presentation Job groups; Review and Submission stay inside Writing (user decisions, recorded 2026-11-27).
s02-D03 · Display may have Main, Appendix and Explore Jobs; Presentation may have Slides, Video and Poster Jobs (user decisions, recorded 2026-11-27).
s02-D04 · This Studio is s02 Grant Block Structure; the earlier s02 Paper Studio is historical (user decision, 2026-11-27). Its decisions are preserved under `_archive/20261127/s02-paper-studio/`; they are not reinterpreted as these decisions.
s02-D05 · “skill might still be into one item in the top view list. No need to have a new studio for it” — Skills remains a top view of this same structure Studio (user correction, 2026-11-27).
s02-D06 · Earlier generic naming direction, superseded by s02-D08: keep the shared hierarchy, but show Grant-specific names in this type-specific Studio (user corrections, 2026-11-27).
s02-D07 · The shared top views are Structure, Draw, Examples and Skills. Structure contains both Job/Task hierarchy and Studio organization; Examples requires real Block bindings and their actual names (user corrections relayed from Design, 2026-11-27).
s02-D08 · “不要再用那个 [Job] 1、[Job] 2、[Job] 3” — a type-specific Block Structure Studio uses the named groups and meaningful Jobs, Task groups and Tasks. Grant leads with Story, Evidence, Display, Writing and Presentation; illustrative instances are design examples, never fake live records (user correction relayed by the Paper owner, 2026-11-27).

s02-D09 · Keep Job Type, Job Name, Task Type and Task Name explicit, with groups recorded separately. Existing owner contracts determine type values; absent Grant contracts stay proposed or unresolved (user correction relayed from the Work owner, 2026-11-27).

Open
----

1. Which explicit Job Type contracts will own Story, consolidated Evidence, final Display assets and Presentation, and which Task types cover packaging and media production? How will Grant Values/Citations/Checks reconcile legacy `value` and citation `evidence` with the numeric-executor contract?
2. Which explicit metadata fields will group Jobs and Tasks without relying on number bands, and how will Studio groups reference their sNN records?
3. How should call-specific requirements generate Application and Attachments Tasks while preserving local edits?
4. Which adapter will bind a reviewed Idea revision to a Grant and keep reciprocal links?
5. How should old Submission/Review Jobs move into Writing without breaking immutable references?

Examples now binds the authored Grant-Example Block. Execution-contract gaps remain separate from this live content example.
