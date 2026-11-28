s11 · Itemization
=================
view: ui-job

**Tags:** `Block types`
**Stage:** shaping
**For:** the Itemization Block's Jobs, Tasks and cross-Block handoff.
**Delivery type:** ui
**UI preview:** Job · labeling-items
**Covers:** Work folders, Job unit, Task groups, Main, selected Task, Studio decisions and versioned delivery.
**Excluded:** production migration and new executor workers; the existing legacy example stays as a comparison.
**Topic:** Turn a source snapshot into reusable items without choosing a downstream label.
**Feeds:** [Three-Block proposal](../delivery/page-spec/block-types-proposal.md)

Contract
--------

- Block: Itemization.
- Job: One source snapshot × one accepted item recipe; recipe trials are Runs of the same Job.
- Job topics: Source collection; recorded on the Block, never inferred from a changing count.
- Task topics: Source · Build · Check; typed roles, not independent phases promoted to Block types.
- Input: Source snapshot and an accepted item recipe.
- Output: Items package with stable IDs, context and source references.
- Main: input binding, Task folds with their recorded results and Runs; Findings only for a real issue; Delivery only for a released package.
- Selected Task: its evidence and Runs, then the narrow action it owns. The Task row hides on Main.
- Studio: human choices; Jobs read those decisions and close on machine-checkable evidence.

What is live
------------

Page embeds [task-items-current](/_board/workbench?path=examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t01_example_items&layout=focus&section=report&group=items&mark=work-section-group), the existing mixed-Job walkthrough. It is a baseline, not a live implementation of this new Block type.
Effect hosts the proposed Itemization page. Its examples are synthetic and actions are memory-only.

Decided
-------

- s11-D01 · Three Block types, one separate Studio design each (user, 2026-11-26).
- s11-D02 · Reuse Job topic → Job → Main / Task topic → Task, horizontal rows, Task row hidden on Main.
- s11-D03 · Freeze explicit input versions; link upstream packages rather than copying mutable work folders.
- s11-D04 · Plans and actual changes live in the [design Trace](../trace/261126/1722_labeling_three_blocks.md).

Open
----

- Review the proposed Job/Task grouping and human decisions in Effect.
- Implement this Block subtype, its folder writer, server reader and migration checks together after the design is accepted.
- Add the new type's real example Block and replace the legacy baseline; keep the unresolved boundary visible in this record.

Files
-----

- [s11-itemization-job-preview.html](s11-itemization-job-preview.html): live baseline and Effect entries.
- [job-preview.html](delivery/ui/job-preview.html): clickable proposal.
- [s11-itemization-job-preview.excalidraw](s11-itemization-job-preview.excalidraw): workflow and handoff drawing.
- [s11-itemization-job-preview.png](s11-itemization-job-preview.png): drawing preview.
- [s11-itemization-job-preview.mindmap.md](s11-itemization-job-preview.mindmap.md): structured contract.
