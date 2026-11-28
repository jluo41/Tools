# Paper and Idea Job UI · proposed

This specification records the reviewed design. It does not replace the current
`job-views.md` inventory or claim the new server composition is implemented.
Studio entrypoints: [Paper / Grant](../../s13-paper-job-preview/s13-paper-job-preview.md) and
[Idea](../../s11-idea-job-preview/s11-idea-job-preview.md).

## Shared structure

```text
Job topic                 Evidence   Writing   Submission   Review
Job                       j11 …      j12 …
Main or Task topic        Main       Main text   Appendix   Letters
Task                      t00 …      t01 …                 (hidden on Main)

Main                      selected Task
  Overview                  Overview
  Tasks                     Plan + Results
  Findings, when populated    workflow controls, output, Runs
                            Findings, when populated
```

Use b17's shared navigation and page parts. Job/Task selection remains in place;
each Task topic remembers its last selected Task. The shell owns selection and
scrolling; a theme supplies semantic groups and content. Names come from the
real faces and source records. Do not infer that a lower decade is obsolete.

One Overview fold replaces the separate Goal / Requirements / map folds in this
proposal. Inside it, use top-view-left-tab-right-content: Page, Draw and Delivery
when present, with one source per item. The final merged form follows b17's
Overview decision; its pending alternatives are not a settled shared contract.

Main hides the Task row. Reserve `Main` for the Job overview; Task topics use
distinct names such as `Main displays`. Empty bands are absent. Folds start closed. Marks and
inline cards carry waits, with the same asks collected in the title tray. Open
dots open their source; hide dots collapse the item list. Mobile navigation rows
scroll horizontally without making the page overflow.

## Types and content

Six Paper Job types are shared by manuscript and Grant. Idea contributes one
separate Job type inside its own Paper-family Block. Initial and revised sends,
individual reviewers and different assessment skills do not add Job types.

| Canonical type | One Job | Job topic | Task topics | Main content | Selected Task |
|---|---|---|---|---|---|
| Writing Version | One send to one target | Writing | Main text / Appendix / Letters; Grant: Application / Attachments / Letters | Question, target requirements, narrative, evidence/display links, built outputs | Its plan, prose, evidence, display, revision controls and Runs |
| Display Evidence | The paper's figure/table collection | Evidence | Main displays / Appendix, from actual placement | Display plan, previews, relevant examples | Display, source tables, method, caption and bindings |
| Value Evidence | The printed-value evidence | Evidence | Value groups / Whole-paper check | Printed items and returned-source bindings | Value group, raw table, Result pointer and check |
| Citation Evidence | The claim/citation evidence | Evidence | Claim groups / Whole-paper check | Claim-to-source coverage | Claim, source passages, citation records and check |
| Submission | One writing version's submission package | Submission | Submission; subdivide only for actual work | Upload set, linked letter and portal fields | Writing-letter reference, portal walk or fill output |
| Review Job | One bounded comments batch against a build | Review | Review Items / Response checks, from actual work | Concerns, routing, replies, sent/released artifacts | Concern IDs, owned changes/evidence, checked reply and Runs |
| Idea Job | One candidate within a direction | Ideas; explicit subtopics when needed | Framing / Assessment / Decision, only as needed | Question, claim, closest work, gaps, assessments, human decision, Paper link | Bounded question, input revision, authored receipts, evidence links and soft Runs |

These Task topics are a menu, not mandatory empty folders or a renumbering rule.
Group existing tasks from their declared semantics. A review's response letter
stays in the answering writing version; submission references that version's
letter. The Idea Job remains the source after Paper handoff.

Grant specializes funding-call requirements, aims, approach, team, budget and
attachments within the shared structure. Keep preliminary findings distinguishable
from proposed outcomes. A grant scaffold does not imply a grant-specific section
template or submission adapter already exists.

## Current reader boundary

- The shared Job rows are implemented in `focus_jobs.py`.
- Writing currently exposes Structure / Evidence / Display.
- Evidence and Submission have specialized views but default to MindMap.
- Review is excluded from writing-version detection but lacks its own Job label
  and content dispatch, so it falls back to generic Job views.
- Embedded views take `ctx.body` and omit `ctx.bar`; simply adding the old bar
  would preserve links that navigate away. Task controls need scoped in-place
  view composition, using the shared pane components.
- Idea already has a basic Block list, Job face and novelty-receipt reader.
  The fuller Main described here is proposed.
- Paper has a real canonical example. Grant and Idea example obligations remain.

## Reader and source ownership

| Responsibility | Existing owner |
|---|---|
| Common selection rows and embedded composition | `servers/workbench/page/job_task_views/focus_jobs.py` |
| Job/Task view maps | `servers/workbench/page/block_index_page/focus_render.py` |
| Writing structure and evidence/display sources | `servers/workbench-paper/paper_version.py`, `paper_structure.py` |
| Evidence and submission content | `servers/workbench-paper/paper_jobs.py`, `paper_tasks.py` |
| Idea content | `servers/workbench-paper/idea_block.py`; scientific contract in `hai-ideation` |
| Reviews | `hai-paper-comments`; UI type dispatch still owed |
| Studio live/proposal distinction | `servers/workbench/studio/tabs/studio_tabs.py`; hai-ui A08 |

Paths in this table are relative to `plugins/haipipe-toolkit/`. No new persistent
UI store or second scientific source is introduced.

## Implementation order

1. Keep the shared navigation controller. Add a small theme adapter for semantic
   groups and Main content; avoid a separate Paper copy of the controller.
2. Compose the six Paper Main types from their existing readers, including Review.
3. Preserve Task workflows using scoped, shared view/pane components. Namespace
   selectors by Job and Task so prebuilt panels cannot switch one another.
4. Create Grant and Idea canonical examples through the existing scaffold writers.
   Inventory the exact output files before writing; do not migrate research data.
5. Update the current page-spec matrix, example inventory, owning skills and
   constitution articles together with code and renderer regression coverage.
6. Verify the real example pages, then mark the corresponding Effect old. Remove
   an old preview only when it is no longer needed for comparison.

This implementation is outside the approved design-file change. Its exact code,
test and fixture file list must be reviewed before that work begins.

## Acceptance

- All seven Job types use the shared rows; manuscript and Grant each traverse
  Writing → Task → workflow controls without a full Block reload.
- Main hides the Task row; topic switches restore the selected Task.
- Evidence is not faded merely because its Job number is below Review's.
- Review concerns retain their routing, and Idea retains source identity,
  revision, human decision and reciprocal Paper link.
- Controls read their original sources; no guessed current artifacts, progress
  tallies, empty bands or duplicate authoring locations appear.
- Existing Paper/Idea tests and affected shared-navigation tests pass; real
  renderer cases guard type dispatch and every required content entry.
- Check desktop and 390px layouts, keyboard navigation, inline asks and dots.
- Paper's A08 preview check passes. Idea's missing live view remains explicitly
  open until its own example is established; do not substitute another theme's
  live page just to make the checker pass.

## Preview integration

The two Effect HTML files are self-contained review snapshots, with local-only
sample interactions. Studio owns the surrounding Page/Effect UI; Paper's quick
view selects Paper or Grant, and its Job rows reach the six types. Idea's quick
view contains its own candidates and assessments.

For a quick-only topic, the current Studio reader still wraps the entry under
Page. The Idea entry explicitly offers Effect inside that wrapper. Native
Page/Effect separation is pending its genuine live example or a separately
reviewed shared-reader change. No production renderer is changed by this design.
