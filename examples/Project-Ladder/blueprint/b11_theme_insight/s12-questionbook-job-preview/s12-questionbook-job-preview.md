s12 · Block Job UI Preview: Question Book
====================================================
view: ui-job

**Tags:** `Job UI`

**Stage:** shaping

**For:** a Question Book Job and its Tasks inside their owning Block.

**Delivery type:** ui

**UI preview:** Job · Question Book

**Why:** What must this kind of Job and its selected Task make understandable?

**Topic:** One question-set version, containing both its local changes and retained members referenced by release.yaml.

**Feeds:** Q01

Main
----

Brief holds why this version is needed, the evidence and desired improvements. Plan + Results pairs each planned addition, change, retention or retirement with its work and outcome. Findings records what was learned about asking and answering the questions. Review assesses the complete release.

Selected Task
-------------

A question Task shows its neutral ask, motivation, dependencies, evidence needs, method, script, reviews and version source. It defines how to answer; the Board holds answers on actual data.

Views
-----

Page-Job embeds the real InsightQuestionBook-Example Block with j02 selected: job-rows, job-overview, job-tasks and job-findings. Page-Task selects its actual t09 in the same Block. Job types and Task types read the owning contracts; they do not create schema fields. QuickHtml holds Version changes. Draw preserves the native MindMap and editable Canvas. Outputs stay in their original files and the shared Files pane.

Sources
-------

- [Shared Studio Type: Block Job UI Preview](../../b17_theme_work/s72-studio-type-block-job-ui-preview/s72-studio-type-block-job-ui-preview.md)
- [Actual example](../../../insight/InsightQuestionBook-Example/board.md)
- [Binding generator](../delivery/structure/build_job_previews.py)
- [Current bindings](studio-views.json)
- [Version changes proposal](delivery/ui/version-changes.html)

Checklist
---------

- [x] Open j02 and t09 inside InsightQuestionBook-Example; keep the Block title and route.
- [ ] Compare Brief, Plan + Results and Findings with their owning sources.
- [ ] Check Version changes against the implementation; retain the proposal until its case passes.
- [ ] Open source files and Canvas without copying content into this Studio.

Decided
-------

s12-D01 · Page shows the example Book's real Jobs view (Topic rows and Job Main, one address, two marks) and a question's page; Effect keeps only Version changes, which the real page cannot draw yet (JL 261126: "please go ahead and do it")

Open
----

- The live Job reader lists local Task folders and omits retained release members.
- Version grouping and full source-aware membership need the shared reader; Version changes remains a proposal.
- Automatic type-to-instance comparison belongs in the shared Checklist interface.
