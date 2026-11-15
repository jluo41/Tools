Current implementation inventory and design proposals. The matrices describe current Insight Views; the shared frame and new Task design below are separate targets. Existing Insight pages remain unchanged.

## Original design

The Insight theme was designed at three page levels, each with Report, Work and Studio. The table below follows the later focus-page designs, not the earlier six-Space sketches.

| Level | Owns | Report | Work | Studio design |
| --- | --- | --- | --- | --- |
| Block · Insight Board | One dataset across question versions and data versions | Findings · Questions · Data · Advice · Jobs · MindMap | The same views, with ideas, new Jobs and data versions, report writing and advice preparation | Map · Why it moved · Story for Design |
| Block · Question Book | The questions and their code, one signed question version at a time (`InsightQuestionBook-<Topic>/`) | Questions · Ideas · Versions · MindMap | Sort ideas into the next question version; review the questions; sign it | Its questions, version by version |
| Job · Analysis | One question version × one data version | Findings · Changes (from the second Job) · Progress · MindMap | Write the overall report; compare and propose; launch, write and check questions; close | Why it moved · Story for Design |
| Task · Question | One question within one Job | Answer · Changes · Method · MindMap | Plan → agree → Runs → page → check → alignment; one next action | This Task |

Report presents results; Work adds actions before the same results. The Job's comparison appears only when there is a previous Job. Studio entries describe the original drawings; they are not a claim that every drawn feature is implemented.

The earlier Board drawing put the question version × data version matrix first in Findings. The current renderer puts that matrix in Jobs only. Findings starts with the newest Job that contains Executive questions, then its Overall Report and question coverage; this selection can differ from the newest Job. The Question map places Executive questions above Data, Information, Knowledge and Wisdom, with citation links. Keep this drawing/implementation difference visible rather than describing either as both.

Earlier sketches used Description, Idea Studio, Audience Report, Work Details, Runs and Delivery at every level. An older storage layout used a Job per Data, Information, Knowledge or Wisdom level. The current question version × data version ladder replaced that Job meaning; evidence levels now classify questions within an analysis.

## Recorded decisions

These choices are recorded in the November 2 and November 6 answer collections, later than several Studio faces' open questions.

| Decision | Carry into the proposal |
| --- | --- |
| Newest Job, marked as open | Keep this selection and its open state; do not silently switch to the newest closed Job |
| Executive answers in side tabs | One answer and its figure at a time on Board and Job |
| Question relationships on a canvas | Executive above Data → Information → Knowledge → Wisdom; citation links and foldable level groups |
| Compact Job progress | Questions in words, marks grouped by evidence level, with an understandable legend |
| Data-version cards | Key aggregate numbers first; files one click away |
| Wisdom drafts before signature | Show draft advice in Delivery before the advice is signed |
| Comparison only after the first Job | No empty Changes view |
| Job MindMap groups Tasks by evidence level | Keep source Tasks and Runs reachable through page navigation; current map leaves are text only |
| Keep the Task MindMap | Keep its question and evidence structure within proposed Overview |
| Show the answer's first figure | Further figures remain reachable beside the answer |
| Studio at every level | Each page's topics and Add a topic remain reachable even when no topics exist |

Three proposed changes need to remain visible: merging Report with Work; moving the matrix from the current Jobs View into Status; and making MindMap a section of Overview rather than a separate View. None is recorded here as accepted for Insight. The earlier Findings-first matrix decision and the current Jobs-only implementation are distinct evidence, not an inferred approval of either new proposal.

## Current View sections

The Block, Job and Task matrices list their specialized Report sections. Each section opens a requirement, layout, source, applicable skill and a correctly routed live example. Conditional sections are described as conditional. Question Book examples remain linked context, not additional Insight page types.

| Level | Report View (link key) | Work adds before the same results | Source |
| --- | --- | --- | --- |
| Block | Findings (answers) | The Overall Report writing action | insight_focus.py: _bw_answers / _answers |
| Block | Questions (questions) | Next question version, sorting ideas, new questions | _bw_questions / _questions_view; Question Book ideas and question versions |
| Block | Data (data) | Add a data version; propose a segment | _bw_data / _data_view; Board versions and the segments of the question version the newest Job runs |
| Block | Advice (handoff) | Advice, draft and human sign | _bw_handoff / _handoff_view; Wisdom pages and delivery |
| Block | Jobs (jobs) | Each Job's steps; add a Job | _bw_jobs / _jobs_view; Board Jobs and their receipts |
| Block · Question Book | Questions (questions) · Ideas (ideas) · Versions (versions) | Sort ideas; review and sign the next question version | prototype_views; insight_prototype.py: _questions_newest / map_top / _proposals_part / _version_part |
| Job | Findings (overall) | The question version's sign, Overall Report writing and gated close; what the close locks | _overall_proc / _overall_res |
| Job | Changes (vs-previous) | Compare, then propose | _vs_proc / _vs_res; hidden for the first Job |
| Job | Progress (grid) | Launch, write and check each cell | _grid_proc / _grid_res |
| Task | Answer (answer) | Plan → agree → run/gather → page → check → alignment; run each segment or gather cited answers; propose a new segment only for compute Tasks | _tw_answer / _t_answer; its By segment section (What it cites for a question with no Run): _tw_cuts / _t_cuts |
| Task | Changes (across-jobs) | Track this question across Jobs | _tw_across / _t_across |
| Task | Method (plan) | Plan the evidence; another agent agrees | _tw_plan / _t_plan |

Report links use section=report and the link key as the group (answers, overall, answer, etc.). Every Report view ends with 🙋 Interaction and prints no caption line. Work uses section=work and work-prefixed groups (work-answers, work-overall, work-answer, etc.). MindMap remains its own View. Studio and supporting rails belong to the page shell; the eight-section shared frame is not yet integrated into this renderer.

## Proposed alignment

Keep Block → Job → Task → Run. Merge Report and Work into Report, with four Views and the same supporting sections as Work.

| View | Block · Insight Board | Job · Analysis | Task · Question |
| --- | --- | --- | --- |
| Overview | Goal and requirements; question relationships; dataset and data versions; linked question versions | Goal; pinned question version and data version; questions, segments and evidence requirements | Question; evidence plan; assumptions and permitted claims; MindMap and dependencies |
| Status | Topic → related BJTR; question version × data version matrix; dependencies and pending decisions | Question × segment progress; launch, write, check, compare and close gates | Runs by segment or evidence need; writing, check and alignment state |
| Findings | Overall understanding; answers across Jobs; changes, limits and unresolved questions | Overall Report; question answers; comparison with the previous Job | Answer and figures; uncertainty; evidence by segment or cited question; the question across Jobs |
| Delivery | Reports; draft and signed advice for Design; version and scope | This analysis's report and artifacts; close record | Answer page and supporting artifacts; review record |

Each View uses **Review Content**, then **Around the Work**. Actions stay beside the relevant content. Status is where execution and dependencies are inspected; Findings is where the meaning and strength of the evidence are read.

These are proposed destinations for existing content, not implemented replacement screens. A completed analysis may have an inconclusive answer. A checked answer does not imply signed advice.

## What moves

### Block

| Existing content | Proposed destination | Preserve |
| --- | --- | --- |
| Findings | Findings | Overall Report and answers across Jobs; keep the open state and make the selected source Job explicit |
| Questions | Overview | Question map, DIKW relationships and linked Question Book |
| Jobs | Status | Question version × data version matrix and what changed |
| Data | Overview | Locked data versions and planned segments; aggregate data only |
| Advice | Delivery | Draft, signature, evidence boundary and stale status |
| MindMap | Overview | Topic and evidence relationships |

### Job

| Existing content | Proposed destination | Preserve |
| --- | --- | --- |
| Findings | Findings | Overall Report; move the question version and data version facts to Overview |
| Progress | Status | Question × segment marks and next actions; detailed answers open in Findings |
| Changes | Findings | Comparison, uncertainty and ideas; hide when no previous Job exists |
| MindMap | Overview | Questions and what they must establish |
| Close | Delivery | Human sign and locked scope; dependencies visible in Status |

### Task

| Existing content | Proposed destination | Preserve |
| --- | --- | --- |
| Answer | Findings | Answer, confidence, figures and cited evidence |
| By segment (a section of Answer) | Status and Findings | Status shows execution; Findings shows each segment's evidence, without repeating the full result |
| Changes | Findings | The same question's history and changes |
| Method | Overview | Evidence needs, agreement and permitted claims |
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

The current matrices have eight clickable Use Cases: dataset investigation; applying a question version; comparing analyses; auditing extract quality; measuring outcomes; assessing differences across segments; developing counsel; and summarizing findings. These describe applications of existing page contracts, not new types. The Task matrix labels DIKW/X as Task Role.

Each dialog groups source-backed pages by SPACE, distinguishes Project from Blueprint example, links the actual Block/Job/Task hierarchy, and exposes Tasks and Path as expandable details. Public examples are relative paths in view-guide.json. Cross-SPACE project mappings live only in the ignored .server_config/workbench-examples.json; their links use each source SPACE's configured DOMAIN. No cross-root file serving is added.

The selected source records include open Jobs, a comparison in which both the question version and the data changed, draft advice and a refused answer. Their labels preserve these distinctions. Existing project links do not establish deployment of the proposed shared Insight frame. Question Book development remains linked context, rather than being folded into the Analysis Job type or misclassified as a dataset-answer Task.

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
- The linked **Question Book** owns reusable questions, scripts and signed question versions. It is shown as a separate example; it does not become a dataset Board or an analysis Job.
- Data, Information, Knowledge, Wisdom and Executive questions share a Task frame but show different evidence. Current D/I/K compute roles show segment Runs; citation-only W/X examples show their cited answers. Broader evidence-mode specialization remains a proposal. No artificial compute grid is added to a synthesis Task.
- Delivery references existing files under the Block's delivery tree. Job and Task views select their own outputs without creating local delivery folders.
- Preserve review, refusal, signatures and stale-advice rules. UI alignment grants no new authority to sign or run work.
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
