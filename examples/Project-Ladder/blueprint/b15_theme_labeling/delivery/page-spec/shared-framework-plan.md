# Labeling: one framework, three Blocks

Proposed implementation plan, 2026-11-27. The three Block owners already exist, but their custom preview shell is not compliant with PRINCIPLE. This plan replaces that shell through shared code; it does not claim the migration has shipped.

## Product structure

Each independent Block uses the shared Report, Studio and Jobs sections. A section is a view of its Block, never another Block or an independently linked Job/Task page.

| Block | Report: read the work | Studio: resolve choices | Jobs: perform the work |
| --- | --- | --- | --- |
| Itemization | Items, source/context provenance, exclusions and checks | Item unit, boundaries and context recipe | Describe source → build items → check → release |
| Guideline Generation | Current rules, evidence, unresolved disagreements and accepted Guideline | Label meaning, human judgments, rule changes and acceptance | Prepare cases → draft rules → evaluate → package |
| Labeling at Scale | Coverage, labels, uncertainty, audit findings and release | Audit decisions and issues to return to Guideline Generation | Qualify executor → Run all / retry → audit → package |

Studio records human decisions once. A related Job or Task exposes that same decision at the point where it is needed; it does not maintain a second answer or signature. Studio's Page view contains the live example; Effect holds only a pending proposal.

The handoff is Corpus → Items package → Guideline package → Labels package. Each downstream Job binds explicit immutable versions. Generating a candidate does not approve it. Scale never changes the Guideline; a meaning issue returns to Guideline Generation.

## Job units and embedded navigation

| Block | One Job | Job topic | Task topics |
| --- | --- | --- | --- |
| Itemization | Source snapshot × item recipe | Source collection | Source · Build · Check |
| Guideline Generation | Candidate expression method within one construct and human authority | Construct | Cases · Rules · Validation |
| Labeling at Scale | Items snapshot × signed Guideline × executor configuration | Guideline release | Qualification · Execution · Quality |

Use the shared horizontal sequence Job topic → Job → Main / Task topic → Task. Main shows input bindings, Tasks and their results, decisions that block work, and the released output when it exists. A selected Task shows its input, operation, results, Runs and relevant human action. Main hides the Task row. All selections retain the owning Block title and path.

## Implementation order

1. **Connect Itemization end to end.** Remove the custom page bypass for its example. Use the same shared shell, section selection, Jobs rows and Studio renderer as Work Theme. Add only Labeling content adapters. Verify this working example before spreading the integration.
2. **Connect the other two Blocks through that adapter contract.** Supply their Report contents, Job/Task bodies and human interactions. Preserve candidate-bound validation and version-bound Scale execution. Do not introduce another navigation implementation.
3. **Make the data and actions durable.** Materialize canonical example Job/Task/Run records through the owning writers. Bind real operations to the existing guarded engine routes. Preserve actual results and human decisions on disk; prototype clicks are not execution or approval receipts. Before migrating existing work, enumerate its old owners and destinations and retain readable history.
4. **Publish the same rendered examples in Workbench and chat.** Build inline HTML from the shared renderer and its assets. Preserve the same layout and navigation; embed actions only when supported, and clearly identify synthetic demonstrations. Remove the old custom shell after the shared examples pass.

The first acceptance milestone is all three examples on the real shared framework with working embedded navigation. Production execution is a further milestone requiring persisted actions, receipts and handoff checks; neither milestone substitutes for the other.

## Code and record boundaries

The following are implementation work packages, not a blanket approval to edit every file. Each execution Trace must enumerate exact files, including writer-generated records, before that pass begins.

| Owner | Intended change |
| --- | --- |
| `servers/workbench-labeling/labeling_focus.py` | Delegate Block requests to the shared page pipeline; preserve section selection. |
| `servers/workbench-labeling/labeling_block_preview.py` | Remove the standalone document shell and provide explicit example content through the shared path. |
| New `servers/workbench-labeling/labeling_context.py` | Supply Labeling Report content and shared-section associations. |
| New `servers/workbench-labeling/labeling_jobs.py` | Supply Job grouping, Main and Task content; own no navigation markup or switching code. |
| `servers/workbench/page/block_index_page/focus_render.py` | Register the content adapter within the shared pipeline. |
| `servers/workbench/page/job_task_views/focus_jobs.py` | Reuse the existing adapter seam for Labeling and remove independently addressed Task openings. Keep Work and Design on the same implementation. |
| `b15_theme_labeling/delivery/ui/labeling-blocks/build_blocks.py` | Export inline examples from the shared renderer. |
| `b15_theme_labeling/delivery/ui/labeling-blocks/block-template.html`, `block-preview.css`, `block-preview.js` | Retire the independent header, section menu and Job/Task switching; retain only necessary domain interactions through the shared content layer. |
| `b15_theme_labeling/delivery/ui/labeling-blocks/check_blocks.py` | Check shared-renderer use, Block identity and absence of child-page destinations; do not merely ban all links. |
| `servers/workbench-labeling/tests/test_block_preview.py` and adapter tests | Exercise rendering through the real shared pipeline, plus invalid bindings and human gates. |
| Shared `tests/test_focus_jobs.py` | Guard Work and Design navigation while adding Labeling; Main hides Tasks and links retain Block ownership. |
| `Project-Ladder/labeling/b03_itemization`, `b04_guideline_generation`, `b05_labeling_at_scale` | Keep three Block owners. Enumerate canonical fixture records and regenerated previews in the execution Trace before writing them. |
| Labeling skills, their owning constitution, `ref/topics.md` and `b15_theme_labeling/delivery/page-spec/` | Align contracts, decisions and live examples with the implemented behavior. Keep detailed rules here, not in PRINCIPLE. |

Shared server files are already being changed in this workspace. Recheck their diffs and current interface before each pass, and preserve other work. If a pass needs a different file or interface, revise that Trace's file list before editing.

## Acceptance

- The real Work example and all three Labeling Blocks use the same shell, section controls and Jobs components. A call-path check establishes reuse; visual similarity alone does not.
- Report, Studio and Jobs each work on all three Block routes. Job/Task selections do not create standalone pages or replace the Block title. Main hides the Task row.
- Itemization preserves item IDs, source references and context. Guideline changes invalidate obsolete validation; release requires the relevant human acceptance. Run all rejects unqualified or unaccepted bindings and schedules only missing matching work.
- Refresh preserves committed records and decisions. Synthetic example state is identified and never counted as a production receipt.
- Inspect the real pages in the browser and the inline exports at desktop and narrow widths. Run focused shared-navigation and Labeling regression checks.
- Every pass records prompts, exact planned files, actual changes and verification in `b15_theme_labeling/trace/`. A topic closes only when the original case passes and a check or written rule guards it.
