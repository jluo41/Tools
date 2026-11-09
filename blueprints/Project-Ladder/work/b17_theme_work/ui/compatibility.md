# Work UI compatibility review

Reviewed against current and previous Work renderers, native page faces across local SPACEs, and theme-owned adapters. This is a structural audit, not a claim that every deployed page or workflow has passed UI acceptance.

## Classification

| Dimension | Meaning | Evidence |
| --- | --- | --- |
| Page level | Block, Job, Task, Run | `haipipe-project`; `haipipe-job/ref/job-contract.md` |
| UI contract | The renderer and record schema that determine views and sections | `work_theme.spaces`; `focus_page.page_module`; `frame._task_modules` |
| Execution kind | A declared `task-type` or `discovery-type` and its execution/skill contract | `haipipe-task/ref/types.md`; Task face |
| Use case | The purpose of a particular piece of work | Job title, goal and Tasks; not a UI dispatcher |

Data processing, model experiments, statistical analysis, software development, comparisons, report production and theme development are not seven distinct Work Job UI types. The common Job scaffold has no Job-type field, and the Work renderer uses the common Job page. These purposes may be retained as examples.

## Existing UI contracts

| Contract | Existing behavior | Fit / boundary |
| --- | --- | --- |
| Work Job | Tasks, their Runs and result headlines; conditional Values and Maps | One Job matrix row. Same contract across different work purposes. |
| CoWork Job | Recorded move, waiting state, messages, meetings and checklist steps; Tasks when present | Real adapter. People is a reference Job variant, without a next-move workflow. |
| Discovery Job | Groups inquiry Tasks and adds Papers, Evidence Bib and Synthesis | One inquiry Job renderer; research subjects are not distinct Job UI types. |
| Work Task | Common result/Run page; task-type can select supporting skills | Execution kinds are not automatically different page layouts. |
| Draft Task | Dedicated Plan, Write, Evidence, Display, Revise and Runs workflow; separate reading views | Must not be presented as a verified generic four-view Task. |
| Prototype | Release Jobs, question sets, proposals and pinned/frozen releases | Insight-owned adapter, explicitly excluded from the new common Work frame. |
| Paper, Insight, Design, Labeling | Theme-owned views, metadata, checks and approval gates | Own matrices must use actual dispatch and contracts, not arbitrary names. |
| Workflow layout | Goal, Plan, Execution, Results; file-backed Deliverables and execution state | Exists alongside focus pages. No completed parity audit or migration is claimed. |
| Legacy work locations | Both tasks/ and work/ trees; some undeclared or historical type aliases | Preserve routes and actual metadata. Do not infer missing types from titles. |
| External results | Receipts and light evidence beside Runs; large outputs referenced in _WorkSpace | Files/Delivery must follow declared references without importing unrelated paths. |
| Component repositories | Code/services without native BJTR faces | Not already supported as a native Work hierarchy; an adapter would be new work. |

## Corrections in this review

- Replaced the fabricated Work Job purpose rows with the common Job contract and actual CoWork/Discovery adapters.
- Registered one public Job example for each displayed variant. Kept existing example folders intact.
- Restored Tasks in the generic Job Status cell and renamed Topics to the implemented View BJTR.
- Documented conditional content and mutually exclusive CoWork states in clickable explanations.
- Marked the old Task matrix as an unverified draft. Its current rows still mix execution kinds and use cases; its cells are not a verified inventory of each Task renderer.

## Open checks

- [ ] Rebuild Task UI rows from actual renderer dispatch; expose execution kinds separately without losing their contracts.
- [ ] Check every Block UI row against its adapter, including Prototype and workflow-layout boundaries.
- [ ] Compare focus views with Goal/Plan/Execution/Results: planning, execution controls, receipt provenance, Deliverables and closure checks.
- [ ] Check external _WorkSpace references in Files and Delivery against real declared sources.
- [ ] Review undeclared/legacy Task metadata without inventing new types or rewriting source records.
- [ ] Reconcile CoWork's existing Status Timeline / Steps with the shared supporting sections without dropping content.
- [ ] Verify phone layout and all relevant UI interactions before calling compatibility complete.

The proposed Checklist evidence/reviewer state machine is not implemented. These open checks are ordinary source-backed review notes, not a new runtime API.

## Code sources

- `plugins/haipipe-toolkit/skills/1_base/project/haipipe-job/ref/job-contract.md`
- `plugins/haipipe-toolkit/skills/1_base/project/haipipe-job/scripts/new_job.py`: `new_job`
- `plugins/haipipe-toolkit/servers/workbench-work/work_theme.py`: `spaces`
- `plugins/haipipe-toolkit/servers/workbench-work/work_progress.py`: workflow layout
- `plugins/haipipe-toolkit/servers/workbench/focus_page.py`: `page_module`, `job_findings`, `status_now_html`, `render`
- `plugins/haipipe-toolkit/servers/workbench/frame.py`: `task_type`, `_task_modules`
- `plugins/haipipe-toolkit/servers/workbench-cowork/cowork_focus.py`: `job_status`, `parts`
- `plugins/haipipe-toolkit/servers/workbench-discovery/discovery_focus.py`: `parts`, `status`
- `plugins/haipipe-toolkit/servers/workbench-insight/insight_prototype.py`: release adapter

## Verification of this correction

- Seven targeted matrix/example regression tests passed.
- Four registered Job examples rendered Overview, Status, Findings and Delivery: sixteen views checked.
- Live browser check confirmed the reduced matrix, Job explanation dialog, its source example URL, and the People reference example in the left-tab/right-content preview.
- Independent factual review found missing conditional CoWork Values, Maps and Meeting headlines; these were added.
- Independent screenshot review did not grant visual acceptance: the rightmost column is clipped until horizontally scrolled, some icons/labels wrap poorly, and mutually exclusive collaboration states are too easy to read as simultaneous sections. Phone layout was not verified in this correction.

Classification is corrected. Full layout and cross-SPACE workflow acceptance remain open.

## Use Cases column

The Job matrix now separates Job Type from Use Cases before the View columns. Examples such as data preparation and model training describe uses of the common Job layout; they do not create new UI types. The renderer treats Use Cases as metadata, even if an example has the same name as a Section, and keeps subsequent View routes intact.

The table uses natural column widths and horizontal scrolling to avoid splitting labels and emoji. Seven matrix regression tests passed after this change; live inspection confirmed column order and the Overview Goal dialog route. Mobile acceptance remains open.
