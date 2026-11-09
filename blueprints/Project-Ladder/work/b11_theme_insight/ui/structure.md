Current implementation inventory and design proposals. The matrices describe current Insight Views; the shared frame and new Task design below are separate targets. Existing Insight pages remain unchanged.

## Original design

The Insight theme was designed at three page levels, each with Report, Work and Studio. The table below follows the later focus-page designs, not the earlier six-Space sketches.

| Level | Owns | Report | Work | Studio design |
| --- | --- | --- | --- | --- |
| Block · Insight Board | One dataset across analysis plans and data freezes | Answers · Questions · Jobs · Data · Handoff · MindMap | The same views, with proposals, new Jobs and freezes, report writing and handoff preparation | Map · Why it moved · Story for Design |
| Job · Analysis | One analysis plan × one data freeze | Overall · Grid · vs previous · MindMap | Write the overall report; launch, write and check questions; compare, propose and close | Why it moved · Story for Design |
| Task · Question | One question within one Job | Answer · By cut · Across Jobs · Plan · MindMap | Plan → agree → Runs → page → check → alignment; one next action | This Task |

Report presents results; Work adds actions before the same results. The Job's comparison appears only when there is a previous Job. Studio entries describe the original drawings; they are not a claim that every drawn feature is implemented.

The earlier Board drawing put the analysis plan × data freeze matrix first in Answers. The current renderer puts that matrix in Jobs only. Answers starts with the newest Job that contains Executive questions, then its Overall Report and question coverage; this selection can differ from the newest Job. Its Questions canvas places Executive questions above Data, Information, Knowledge and Wisdom, with citation links. Keep this drawing/implementation difference visible rather than describing either as both.

Earlier sketches used Description, Idea Studio, Audience Report, Work Details, Runs and Delivery at every level. An older storage layout used a Job per Data, Information, Knowledge or Wisdom level. The current analysis-plan × data-freeze ladder replaced that Job meaning; evidence levels now classify questions within an analysis.

## Recorded decisions

These choices are recorded in the November 2 and November 6 answer collections, later than several Studio faces' open questions.

| Decision | Carry into the proposal |
| --- | --- |
| Newest Job, marked as a preview | Keep this selection and its preview state; do not silently switch to the newest closed Job |
| Executive answers in side tabs | One answer and its figure at a time on Board and Job |
| Question relationships on a canvas | Executive above Data → Information → Knowledge → Wisdom; citation links and foldable level groups |
| Compact Job progress | Questions in words, marks grouped by evidence level, with an understandable legend |
| Data-freeze cards | Key aggregate numbers first; files one click away |
| Wisdom drafts before signature | Show draft counsel in Delivery before the handoff is signed |
| Comparison only after the first Job | No empty vs previous view |
| Job MindMap groups Tasks by evidence level | Keep source Tasks and Runs reachable through page navigation; current map leaves are text only |
| Keep the Task MindMap | Keep its question and evidence structure within proposed Overview |
| Show the answer's first figure | Further figures remain reachable beside the answer |
| Studio at every level | Each page's topics and Add a topic remain reachable even when no topics exist |

Three proposed changes need to remain visible: merging Report with Work; moving the matrix from the current Jobs View into Status; and making MindMap a section of Overview rather than a separate View. None is recorded here as accepted for Insight. The earlier Answers-first matrix decision and the current Jobs-only implementation are distinct evidence, not an inferred approval of either new proposal.

## Current View sections

The Block, Job and Task matrices list their specialized Report sections. Each section opens a requirement, layout, source, applicable skill and a correctly routed live example. Conditional sections are described as conditional. Prototype examples remain linked context, not additional Insight page types.

| Level | Report View | Work adds before the same results | Source |
| --- | --- | --- | --- |
| Block | Answers | The Overall Report writing action | insight_focus.py: _bw_answers / _answers |
| Block | Questions | Next analysis plan, proposal triage, new questions | _bw_questions / _questions_view; Prototype proposals and releases |
| Block | Jobs | Each Job's steps; add a Job | _bw_jobs / _jobs_view; Board Jobs and their receipts |
| Block | Data | Add a freeze; propose a cut | _bw_data / _data_view; Board versions and release partitions |
| Block | Handoff | Counsel, draft and human sign | _bw_handoff / _handoff_view; Wisdom pages and delivery |
| Job | Overall | Plan signature, Overall Report writing and gated close; what close freezes | _overall_proc / _overall_res |
| Job | Grid | Launch, write and check each cell | _grid_proc / _grid_res |
| Job | vs previous | Compare, then propose | _vs_proc / _vs_res; hidden for the first Job |
| Task | Answer | Plan → agree → run/gather → page → check → alignment | _tw_answer / _t_answer |
| Task | By cut | Run each cut or gather cited answers; propose a new cut only for compute Tasks | _tw_cuts / _t_cuts |
| Task | Across Jobs | Track this question across Jobs | _tw_across / _t_across |
| Task | Plan | Plan the evidence; another agent agrees | _tw_plan / _t_plan |

Report links use section=report and the actual group (answers, overall, answer, etc.). Work uses section=work and work-prefixed groups (work-answers, work-overall, work-answer, etc.). MindMap remains its own View. Studio and supporting rails belong to the page shell; the eight-section shared frame is not yet integrated into this renderer.

## Proposed alignment

Keep Block → Job → Task → Run. Merge Report and Work into Report, with four Views and the same supporting sections as Work.

| View | Block · Insight Board | Job · Analysis | Task · Question |
| --- | --- | --- | --- |
| Overview | Goal and requirements; question relationships; dataset and freezes; linked analysis plans | Goal; pinned plan and freeze; questions, cuts and evidence requirements | Question; evidence plan; assumptions and permitted claims; MindMap and dependencies |
| Status | Topic → related BJTR; plan × freeze matrix; dependencies and pending decisions | Question × cut progress; launch, write, check, compare and close gates | Runs by cut or evidence need; writing, check and alignment state |
| Findings | Overall understanding; answers across Jobs; changes, limits and unresolved questions | Overall Report; question answers; comparison with the previous Job | Answer and figures; uncertainty; evidence by cut or cited question; Across Jobs |
| Delivery | Reports; draft and signed Design handoffs; version and scope | This analysis's report and artifacts; close record | Answer page and supporting artifacts; review record |

Each View uses **Review Content**, then **Around the Work**. Actions stay beside the relevant content. Status is where execution and dependencies are inspected; Findings is where the meaning and strength of the evidence are read.

These are proposed destinations for existing content, not implemented replacement screens. A completed analysis may have an inconclusive answer. A checked answer does not imply a signed handoff.

## What moves

### Block

| Existing content | Proposed destination | Preserve |
| --- | --- | --- |
| Answers | Findings | Overall Report and answers across Jobs; preserve preview and make the selected source Job explicit |
| Questions | Overview | Question canvas, DIKW relationships and linked Prototype |
| Jobs | Status | Analysis plan × data freeze matrix and what changed |
| Data | Overview | Frozen versions and planned cuts; aggregate data only |
| Handoff | Delivery | Draft, signature, evidence boundary and stale status |
| MindMap | Overview | Topic and evidence relationships |

### Job

| Existing content | Proposed destination | Preserve |
| --- | --- | --- |
| Overall | Findings | Overall Report; move the plan/freeze facts to Overview |
| Grid | Status | Question × cut marks and next actions; detailed answers open in Findings |
| vs previous | Findings | Comparison, uncertainty and proposals; hide when no previous Job exists |
| MindMap | Overview | Questions and what they must establish |
| Close | Delivery | Human sign and frozen scope; dependencies visible in Status |

### Task

| Existing content | Proposed destination | Preserve |
| --- | --- | --- |
| Answer | Findings | Answer, confidence, figures and cited evidence |
| By cut | Status and Findings | Status shows execution; Findings shows each cut's evidence, without repeating the full result |
| Across Jobs | Findings | The same question's history and changes |
| Plan | Overview | Evidence needs, agreement and permitted claims |
| Work chain | Status | Plan, review, execution, writing, check and alignment records |
| MindMap | Overview | Keep the Task's question and evidence relationships, as explicitly decided |

## Shared sections

Studio · Interactions · Decisions · Things to Know · Checklist · Timeline · Skills · Files.

Confirmed common target, not yet implemented for Insight: use Review Content → Around the Work, with the same names, order, components and scope as Work. This does not require adopting Work's four business Views. View sections contain explicitly linked View or Topic records. The right rail contains records from the current page and its descendants. Unassigned records remain in the rail. Parent context is a link, not a copied inbox or Studio list.

Topic lists use left tabs and right content. Files uses folder types, expandable trees and file pop-outs. Related Skills and Files follow the same selection as the View. Routine helper text is omitted.

The original Job and Task Studio drawings included parent topics. Under the proposed shared scope, those become explicit parent links rather than automatically included records.

## New Task design

The user's November 8 discussion adds three ongoing Board activities: enrich the dataset; continually propose or improve DIKW questions; and find literature or theory. Analysis and synthesis complete the feedback loop. These activities are not yet new Task types or Jobs in the ladder contract.

The [Task design proposal](task-design.md) separates the enduring activity from a bounded Task, specifies inputs, outputs and completion evidence, and compares placement options. DIKW classifies what an answer can claim; activity classifies what work is being done. Neither axis replaces the other.

## Use Cases

The current matrices have eight clickable Use Cases: dataset investigation; applying an analysis plan; comparing analyses; auditing extract quality; measuring outcomes; assessing differences across cuts; developing counsel; and summarizing findings. These describe applications of existing page contracts, not new types. The Task matrix labels DIKW/X as Task Role.

Each dialog groups source-backed pages by SPACE, distinguishes Project from Blueprint example, links the actual Block/Job/Task hierarchy, and exposes Tasks and Path as expandable details. Public examples are relative paths in view-guide.json. Cross-SPACE project mappings live only in the ignored .server_config/workbench-examples.json; their links use each source SPACE's configured DOMAIN. No cross-root file serving is added.

The selected source records include previews, a comparison in which both plan and data changed, draft counsel and a refused answer. Their labels preserve these distinctions. Existing project links do not establish deployment of the proposed shared Insight frame. Prototype development remains linked context, rather than being folded into the Analysis Job type or misclassified as a dataset-answer Task.

Source and served-template checks passed. Some external services failed HTTP verification; their private labels identify the observed availability issue. Browser interaction and phone checks remain pending. See [acceptance](acceptance.md).

## Implementation boundary

| State | Content | Evidence or next check |
| --- | --- | --- |
| Implemented | Specialized Report/Work views and example ladders | insight_focus.py; live examples in the matrices |
| Implemented in blueprint | Current section inventories, clickable specifications and explicit View routes | block-views.md, job-views.md, task-views.md, view-guide.json |
| Common target; Insight integration pending | Review Content → Around the Work; eight scoped sections | Shared work_frame.py exists; Insight still renders Process/Results and its existing shell |
| Discussion | Four business Views; new activity-based Task types and their owning Jobs | Proposed alignment; task-design.md |
| Discussion | Work's proposed four-state acceptance checklist | No new state schema is assumed here |

[Acceptance checks](acceptance.md) distinguish source/render checks from live visual and interaction checks. A specification or rendered HTML is not a passed live UI review.

## Boundaries

- This Block, **Theme: insight**, designs the theme. An **Insight Board** is the dataset-facing product it designs.
- The linked **Prototype** owns reusable questions, scripts and signed analysis-plan releases. It is shown as a separate example; it does not become a dataset Board or an analysis Job.
- Data, Information, Knowledge, Wisdom and Executive questions share a Task frame but show different evidence. Current D/I/K compute roles show cut Runs; citation-only W/X examples show their cited answers. Broader evidence-mode specialization remains a proposal. No artificial compute grid is added to a synthesis Task.
- Delivery references existing files under the Block's delivery tree. Job and Task views select their own outputs without creating local delivery folders.
- Preserve review, refusal, signatures and stale-handoff rules. UI alignment grants no new authority to sign or run work.
- Existing records and old links must remain usable. No historical drawing or decision is overwritten by this proposal.

## Sources

- [Original page-level design](../j01_insight_workbench_pages/j01_insight_workbench_pages.md)
- [Board Report](../j01_insight_workbench_pages/t01_board_page/s51-block-ui-report/s51-block-ui-report.md) · [Board Work](../j01_insight_workbench_pages/t01_board_page/s52-block-ui-work/s52-block-ui-work.md) · [Board Studio](../j01_insight_workbench_pages/t01_board_page/s53-block-ui-studio/s53-block-ui-studio.md)
- [Job Report](../j01_insight_workbench_pages/t02_job_page/s54-job-ui-report/s54-job-ui-report.md) · [Job Work](../j01_insight_workbench_pages/t02_job_page/s55-job-ui-work/s55-job-ui-work.md) · [Job Studio](../j01_insight_workbench_pages/t02_job_page/s56-job-ui-studio/s56-job-ui-studio.md)
- [Task Report](../j01_insight_workbench_pages/t03_task_page/s57-task-ui-report/s57-task-ui-report.md) · [Task Work](../j01_insight_workbench_pages/t03_task_page/s58-task-ui-work/s58-task-ui-work.md) · [Task Studio](../j01_insight_workbench_pages/t03_task_page/s59-task-ui-studio/s59-task-ui-studio.md)
- [Board decisions](../j01_insight_workbench_pages/t01_board_page/runs/r01_collect_board_report_decisions/result/answer_collection.md) · [Board refinements](../j01_insight_workbench_pages/t01_board_page/runs/r02_collect_board_report_next/result/answer_collection.md) · [Studio decisions](../j01_insight_workbench_pages/t01_board_page/runs/r03_collect_studio_every_level/result/answer_collection.md)
- [Job refinements](../j01_insight_workbench_pages/t02_job_page/runs/r01_collect_job_report_next/result/answer_collection.md) · [Task refinements](../j01_insight_workbench_pages/t03_task_page/runs/r01_collect_task_report_next/result/answer_collection.md)
- [Current Insight renderer](../../../../../plugins/haipipe-toolkit/servers/workbench-insight/insight_focus.py)
- [Work shared frame](../../../../../plugins/haipipe-toolkit/servers/workbench/README.md)
