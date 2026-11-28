s13 · Block Job UI Preview: DataPrep
====================================================
view: ui-job

**Tags:** `Job UI`

**Stage:** shaping

**For:** a DataPrep Job and its Tasks inside their owning Block.

**Delivery type:** ui

**UI preview:** Job · DataPrep

**Why:** What must this kind of Job and its selected Task make understandable?

**Topic:** One prep-code version: an ordered chain of step definitions, reviewed and signed.

**Feeds:** Q01

Main
----

Brief holds the data family, purpose, version and interfaces. Plan + Results pairs each step with its code and review. Findings records preparation limits and reusable knowledge. Execution outcomes link to consuming Board prep Runs.

Selected Task
-------------

A step shows step.md, its goal, inputs, outputs, declared parameters, checks, code and review. Runtime metrics are references to the Board prep Run; no execution Run is invented beneath the code step.

Views
-----

Page-Job embeds the real InsightDataPrep-Example Block with j01 selected: job-rows, job-overview, job-tasks and job-findings. Page-Task selects its actual t01 in the same Block. Job types and Task types read the owning contracts; they do not create schema fields. QuickHtml holds Steps and Runs. Draw preserves the native MindMap and editable Canvas. Outputs stay in their original files and the shared Files pane.

Sources
-------

- [Shared Studio Type: Block Job UI Preview](../../b17_theme_work/s72-studio-type-block-job-ui-preview/s72-studio-type-block-job-ui-preview.md)
- [Actual example](../../../insight/InsightDataPrep-Example/board.md)
- [Binding generator](../delivery/structure/build_job_previews.py)
- [Current bindings](studio-views.json)
- [Steps and Runs proposal](delivery/ui/steps-and-runs.html)

Checklist
---------

- [ ] Open j01 and t01 inside InsightDataPrep-Example; keep the Block title and route.
- [ ] Compare Brief, Plan + Results and Findings with their owning sources.
- [ ] Check Steps and Runs against the implementation; retain the proposal until its case passes.
- [ ] Open source files and Canvas without copying content into this Studio.

Decided
-------

s13-D01 · Page shows the example DataPrep Block's real Jobs view (Topic rows and Job Main, one address, two marks) and a step's page; Effect keeps only Steps and Runs, which the real page cannot draw yet (JL 261126: "please go ahead and do it")

Open
----

- The live Job reader still groups prep versions and steps numerically.
- The example keeps its Block route and title, but the shared header labels it Insight Board; selected t01 shows no step content. The DataPrep identity and step reader need implementation.
- Steps and Runs remains a proposal; real execution stays in the consuming Board.
- Automatic type-to-instance comparison belongs in the shared Checklist interface.
