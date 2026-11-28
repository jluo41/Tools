s14 · Labeling at Scale
=======================
view: ui-job

**Tags:** `Block types`
**Stage:** shaping
**For:** the Labeling at Scale Block's Jobs, Tasks and cross-Block handoff.
**Delivery type:** ui
**UI preview:** Job · labeling-scale
**Covers:** Work folders, Job unit, Task groups, Main, selected Task, Studio decisions and versioned delivery.
**Excluded:** production migration and new executor workers; the existing legacy example stays as a comparison.
**Topic:** Execute a frozen guideline on a fixed item snapshot, then audit and publish traceable labels.
**Feeds:** [Three-Block proposal](../delivery/page-spec/block-types-proposal.md)

Contract
--------

- Block: Labeling at Scale.
- Job: One Items snapshot × one signed Guideline release × one executor configuration. Batches and retries are Runs.
- Job topics: Guideline release; recorded on the Block, never inferred from a changing count.
- Task topics: Qualification · Execution · Quality; typed roles, not independent phases promoted to Block types.
- Input: Released Items, signed Guideline and executor configuration.
- Output: Audited labels with coverage, exclusions and per-item provenance.
- Main: input binding, Task folds with their recorded results and Runs; Findings only for a real issue; Delivery only for a released package.
- Selected Task: its evidence and Runs, then the narrow action it owns. The Task row hides on Main.
- Studio: human choices; Jobs read those decisions and close on machine-checkable evidence.

What is live
------------

Page embeds [task-release-current](/_board/workbench?path=examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t04_example_expression&layout=focus&section=report&group=release&mark=ls-view), the existing mixed-Job walkthrough. It is a baseline, not a live implementation of this new Block type.
Effect hosts the proposed Labeling at Scale page. Its examples are synthetic and actions are memory-only.
The scale comparison is the existing expression release page; no separate production Scanning page is claimed.

Decided
-------

- s14-D01 · Three Block types, one separate Studio design each (user, 2026-11-26).
- s14-D02 · Reuse Job topic → Job → Main / Task topic → Task, horizontal rows, Task row hidden on Main.
- s14-D03 · Freeze explicit input versions; link upstream packages rather than copying mutable work folders.
- s14-D04 · Plans and actual changes live in the [design Trace](../trace/261126/1722_labeling_three_blocks.md).

Open
----

- Review the proposed Job/Task grouping and human decisions in Effect.
- Implement this Block subtype, its folder writer, server reader and migration checks together after the design is accepted.
- Add the new type's real example Block and replace the legacy baseline; keep the unresolved boundary visible in this record.

Files
-----

- [s14-scale-job-preview.html](s14-scale-job-preview.html): live baseline and Effect entries.
- [job-preview.html](delivery/ui/job-preview.html): clickable proposal.
- [s14-scale-job-preview.excalidraw](s14-scale-job-preview.excalidraw): workflow and handoff drawing.
- [s14-scale-job-preview.png](s14-scale-job-preview.png): drawing preview.
- [s14-scale-job-preview.mindmap.md](s14-scale-job-preview.mindmap.md): structured contract.

Execution gate
--------------

Run all is enabled only for signed immutable inputs and the exact qualified executor. It schedules only missing batches of this Job. Retries preserve completed results; a new Items, Guideline or executor binding is a new Job. Uncertain items retain an unresolved disposition, not an invented negative label. Final delivery waits for coverage and audit checks.
