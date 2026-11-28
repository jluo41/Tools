s03 · Block Structure: Labeling at Scale
========================================
view: overview

**Tags:** `Block Structure`

**Stage:** explore

**For:** the general work hierarchy and Studio organization of a Labeling at Scale Block.

**Delivery type:** structure

**Topic:** Execute and audit labeling under a frozen, accepted Guideline; do not redefine meaning. Topics group work; they add no folder level. Jobs, Tasks and their Studio content remain inside the owning Block.

Views
-----

- Structure: Folder, Job-Task and Studio as collapsible folder trees; each keeps its verified examples with it.
- Task types: generated from the evidenced type catalog; absent type levels are declared explicitly.
- Draw: separate drawing fragments using the same verified names and relationships.
- Skills: the family door, Task owners and workbench reader, read from their actual files.

Contract boundary
-----------------

The Structure view uses Work’s shared `tree_html` and CSS for every subject and its embedded examples. Draw uses the shared drawing component through its own bindings. Fixed Task types use their contract names; variable or undecided names use 〈 〉. Independent Job types need a contract before they can be registered. Topics group work and never substitute for types. Nodes start folded and open progressively at the shared component's normal text size.

One Job: One Items snapshot, signed Guideline release and executor configuration. Batches, qualification and audit stay within this binding.

- Define the independent Labeling at Scale Job type; b05 currently has a preview model and no Job or Task folders.
- The proposed Scanning name consolidates Qualify executor, Run batches, Audit labels and Package labels. These are operations, not four registered Task Types. The optional eval Task needs separate authorized ground truth.

Files
-----

- `studio-views.json`: the shared reader's view manifest.
- `../delivery/structure/scale.html`: embedded content only; the default entry is this Block’s Studio.
- [Previous face](prior-structure-261127.md): original content, preserved verbatim. Its canvases, annotations, builders, results and deliveries remain at their existing paths.

Decided
-------

s03-D01 · The inputs are a human and a corpus; the intended outputs are an approved structured guideline and accepted labeled data, possibly a small subset of the corpus. (user 261026)

s03-D02 · Each iteration distinguishes updating the meaning of the guideline from improving how the same meaning is expressed. (user 261026)

s03-D03 · Compare multiple executor models without changing their weights; aim to improve the weakest model while preserving strong-model quality and reducing the gap. This is an objective to test. (user 261026)

s03-D04 · The two use cases are entry points into one process: rough idea without a guideline or labels, and existing labeled data with an optional old guideline. (user 261026)

s03-D05 · Make the whole process easier: the human makes high-level judgments affecting many items; the agent organizes evidence, applies decisions and checks consistency. (user 261026)

s03-D06 · Draw the two use cases separately, with a third shared execution flow; no outer frame, freer layout, emoji and independently movable nodes. (user 261026)

s03-D07 · Follow the supplied reference: pale role cards, restrained colored connectors, compact emoji, clean typography and clear local zones. Retain no whole-canvas frame and independently editable nodes. This user preference overrides the default monochrome style. (user 261027)

s03-D08 · Replace the primary summary drawing with one large, detailed architecture-style workflow, following the supplied food-event demo: numbered operations, concrete input/output records, explicit failure routes, shared records and evaluation. The main map supersedes the three-card summaries; earlier drawings remain supplemental. Its large size and pale zones are deliberate user overrides; preserve native editability and no whole-canvas outer frame. All steps remain proposed, not implementation or result claims. (user 261027)

s03-D09 · Both use-case slides use three rows: human-agent-corpus dialogue; two aligned outputs, a structured adaptive guideline and human-approved, guideline-consistent labeled data; then executor testing and large-scale labeling with audit. Existing labeled data is the left-side input in use case 2; the large unlabeled target corpus stays on the right in both. (user 261027)

s03-D10 · The presentation, source content, image generation prompts, artwork and prior versions live in this blueprint topic under `slides/`. The former Physician-SPACE output path is a compatibility symlink. (user 261027)

s03-D11 · The Subjective Labeling deck and its sources now live directly under the Tools blueprint Block at `../slides/`, rather than inside a Studio topic or the study paper folder. Earlier paths remain compatibility links. (user 261027)

s03-D12 · Redraw all five Subjective Labeling slides as version 4 in the shared IRB/team-workspace style: outline icons, muted role colors, spacious text and native editable arrows. Preserve both use cases, their paired accepted outputs and scaling row, and the evaluation plan. Keep earlier illustrated versions. (user 261027)

s03-D13 · The deck is this topic's delivery: version 12 and what it builds from live in `delivery/deck/`; versions 1 to 11 moved to `../_archive/20261031/slides-v1-v11/`. Replaces D10 and D11, which put the deck in `slides/` at the Block. (JL 261031)

Open
----

Review the grouping and Task responsibilities. The example Block still uses the earlier synthetic preview until its shared Block-frame migration is completed; this structure view does not claim that migration or production execution is done.
