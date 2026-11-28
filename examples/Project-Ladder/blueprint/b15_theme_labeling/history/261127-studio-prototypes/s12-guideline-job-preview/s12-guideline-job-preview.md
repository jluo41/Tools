s12 · Guideline Generation
==========================
view: ui-job

**Tags:** `Block types`
**Stage:** shaping
**For:** the Guideline Generation Block's Jobs, Tasks and cross-Block handoff.
**Delivery type:** ui
**UI preview:** Job · labeling-guideline
**Covers:** Work folders, Job unit, Task groups, Main, selected Task, Studio decisions and versioned delivery.
**Excluded:** production migration and new executor workers; the existing legacy example stays as a comparison.
**Topic:** Turn human judgments into an explicit guideline with a reviewed scope and a measured executable expression.
**Feeds:** [Three-Block proposal](../delivery/page-spec/block-types-proposal.md)

Contract
--------

- Block: Guideline Generation.
- Job: One candidate rule-expression method under a fixed label scope and human authority; revisions and evaluation rounds are Runs.
- Job topics: Target construct; recorded on the Block, never inferred from a changing count.
- Task topics: Cases · Rules · Validation; typed roles, not independent phases promoted to Block types.
- Input: Versioned Items, the label scope and recorded human decisions.
- Output: A signed, immutable guideline package with examples and validation evidence.
- Main: input binding, Task folds with their recorded results and Runs; Findings only for a real issue; Delivery only for a released package.
- Selected Task: its evidence and Runs, then the narrow action it owns. The Task row hides on Main.
- Studio: human choices; Jobs read those decisions and close on machine-checkable evidence.

What is live
------------

Page embeds [task-meaning-current](/_board/workbench?path=examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t03_example_meaning&layout=focus&section=report&group=preferences&mark=ls-view), the existing mixed-Job walkthrough. It is a baseline, not a live implementation of this new Block type.
Effect hosts the proposed Guideline Generation page. Its examples are synthetic and actions are memory-only.

Decided
-------

- s12-D01 · Three Block types, one separate Studio design each (user, 2026-11-26).
- s12-D02 · Reuse Job topic → Job → Main / Task topic → Task, horizontal rows, Task row hidden on Main.
- s12-D03 · Freeze explicit input versions; link upstream packages rather than copying mutable work folders.
- s12-D04 · Plans and actual changes live in the [design Trace](../trace/261126/1722_labeling_three_blocks.md).

Open
----

- Review the proposed Job/Task grouping and human decisions in Effect.
- Implement this Block subtype, its folder writer, server reader and migration checks together after the design is accepted.
- Add the new type's real example Block and replace the legacy baseline; keep the unresolved boundary visible in this record.

Files
-----

- [s12-guideline-job-preview.html](s12-guideline-job-preview.html): live baseline and Effect entries.
- [job-preview.html](delivery/ui/job-preview.html): clickable proposal.
- [s12-guideline-job-preview.excalidraw](s12-guideline-job-preview.excalidraw): workflow and handoff drawing.
- [s12-guideline-job-preview.png](s12-guideline-job-preview.png): drawing preview.
- [s12-guideline-job-preview.mindmap.md](s12-guideline-job-preview.mindmap.md): structured contract.

Human authority
---------------

The Studio owns scope, case judgments, acceptance and the release signature. A Job produces a candidate and its validation packet; its close is a check of artifacts and evidence, not a human signature. Expression errors can trigger another execution Run; semantic changes return to the human review and create a new meaning version. A release is immutable, so an already-bound scale Job never silently starts using a newer guideline.
