s11 · Block Job UI Preview: Idea
================================

**Tags:** `Levels`

**For:** one candidate Idea Job developed and assessed inside its direction Block

**Delivery type:** ui

**UI preview:** Job · idea

**Covers:** the Ideas topic, candidate Jobs, Main, assessment-question Task groups, Task workflow controls, soft Runs and human decisions

**Topic:** How does a candidate become a defensible paper idea while its history stays intact? Use Work's Job navigation and Main bands; show the candidate's question, claim, evidence gaps, assessments and decision in their own places. A skill is a method within a Task.

**Source:** [Work Job preview](../../b17_theme_work/s11-work-job-preview/s11-work-job-preview.md), [Paper Job design](../s13-paper-job-preview/s13-paper-job-preview.md), [proposed specification](../delivery/page-spec/job-ui-design.md).

**Feeds:** `servers/workbench-paper/idea_block.py` and shared Job/Task view composition; the scientific owner remains `hai-ideation`.

## Effect

`delivery/ui/idea-job-main.html` contains the interactive proposal with fictional candidates. Main uses Overview, Tasks and populated Findings. Framing, Assessment and Decision organize the bounded questions; choosing a Task opens its authored assessment, sources, decision controls and Runs.

The preview's choices are local demonstrations. They never create an immutable selection receipt, scientific evidence, a real Run or a Paper destination.

## Decided

- An Idea Block lives in `paper/Idea-<Slug>/`; one candidate is one Job.
- Each assessment Task owns a question or deliverable. Different skills or reviewers do not create different Job types.
- Work owns new computation; Discovery owns source acquisition. Idea assessments link their evidence.
- A reviewed selection links to a Paper while keeping the source Idea Job and revision history.
- The navigation and page parts follow Work; content varies by the folder's contract.

## Open

- Create a canonical Idea example through the existing scaffold writers and attach its genuine live Page view.
- Render the candidate Card, broader assessment receipts, decision and reciprocal Paper links in the shared Main; today's reader shows the face and novelty receipts only.
- Verify selection marks, exact source revisions, empty-state omission and Task controls on the real example.
- The current Studio reader splits Page and Effect only when both live and quick sources exist. Until the live example exists, Studio wraps this entry under Page; the entry itself explicitly offers Effect. This limitation remains open, rather than substituting an unrelated live Block.

## Files

- `s11-idea-job-preview.html`: the Effect-only preview entry.
- `delivery/ui/idea-job-main.html`: candidate and assessment interaction proposal.
- `../delivery/page-spec/job-ui-design.md`: shared design and remaining implementation.

## Check

The A08 preview check is expected to report exactly one missing live view for this topic. Its quick-view path must resolve. Clear that finding only after the real Idea example and reader are verified; a proposed destination is not a live page.
