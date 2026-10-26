# A Block's background index: a connected map of the work

Use this with `haipipe-studio` when a reader asks for the whole picture, where to
start, or an index of every Studio and Job with what remains to finish.

## Start with the Block

Read the Block face, every Studio face, every Job face and checklist, the Jobs'
Tasks, and existing Reports and delivery entries. Include reference and on-hold
Jobs. Account for older Job-local Studios as well as Block-owned topics; retain
their actual paths. A missing face or state is an open point, not a completed item.

Use the shared `scripts/block_index.py <block> --draw` for the canonical
`studio/s00-overview/`. It reads the inventory from disk and draws
the face's `background:` YAML. Keep project-specific older indexes readable;
reuse their background material when updating s00, without silently removing or
renumbering their topics. A cross-Block landing index belongs to the Project and
links to each Block's own index.

## Propose the Studio items still needed

s00 includes a proposed Studio list alongside its existing inventory. Infer each
candidate from real Job goals, checklists, Tasks or unresolved cross-Job work,
following `infer-topics.md`; do not add a generic catalog of subjects.

For each candidate, record a suggested id/name, the question it will settle, the
source Jobs/Tasks, its expected output, a subject group and priority. Mark it
**proposed** or **conditional**, with the condition named. Recommend a small first
batch and show how its outputs lead to existing Reports or Jobs. If no additional
topic is grounded in the work, explain why no addition is proposed.

Propose Jobs the same way, in the face's `job_proposals` yaml: `id`, `slug`,
`title`, `status` (proposed, conditional or created), `topics` (what it rests on)
and `finish` (what closes it). Topics go in `studio_proposals` (`id`, `title`,
`status`, `question`, `jobs`, `output`, `group`, `priority`, `condition`).

Each may carry a `why`: the gap it closes (a Question nobody feeds, a Job with
no close rule, a next step that needs thinking first). Propose only what such a
gap grounds; the builder never invents a proposal.

The shared builder draws the proposals not made yet in their own last frame,
"💡 what we propose next", one row per proposal read left to right like the
index: the gap it closes (its `why`, red), the topic, the Job, what it delivers.
A proposed topic and the first proposed Job resting on it share a row; a Job
left over sits beside the made topic it rests on, drawn in black. Proposed boxes
are red and dashed and show status, question or condition. The index
stays what is on disk and names the proposals in one red line per branch. A
proposal leaves the frame once its folder exists (any `sNN-*` for a topic,
`jNN_<slug>/` for a Job); with none left, the frame is not drawn. A Job number
another folder already holds is flagged in red. The builder's inventory and
counts include actual folders only. Listing candidates creates no topic, changes
no stage and grants no approval to execute their work. Use the numbering bands
and preserve earlier id references when suggesting ids. Update the proposal list
when a topic is actually created, merged or deferred.

## Know what the shared builder covers

To list Tasks under their owning Jobs in the main Index frame, set `tasks: true`
in the face's `index:` YAML. Every Task's id, title and recorded state are read
from its face on each build; they appear as child lines inside the Job's box.
The frame grows down to fit them. The default compact Job view is unchanged.

```yaml
index:
  tasks: true
```

The shared builder supplies a structural inventory, not an interpretation of
what finishes the work. Read checklists and close rules directly when adding
that interpretation; its abbreviated labels do not replace those sources.
Older Job-local Studios may appear only as ids: retain their full paths in the
background or a linked inventory. A shortened status line may also need an open
question taken from the full face.

Use the face's background YAML for a compact connected tree of grounded
relationships and proposed outputs. When those relationships need cross-links
or endpoint arrows the folder-tree builder cannot draw, add a project-local
companion drawing and builder in the same topic, linked from its face. Keep
`s00-overview.excalidraw` as the shared builder's inventory; use a
separate name such as `work-map.excalidraw` for the companion, with `canvas.write`
for human-mark preservation. Do not claim the generated inventory alone answers
where to start or what must be produced.

## Make the relationships visible

The reader should be able to follow this shape:

```text
Block: why this work exists, and what closes it
├── Studio topics → the Questions or Jobs they inform
└── Jobs
    ├── Tasks / checks → current evidence and remaining steps
    └── expected output → Report, delivery, or another named consumer
```

A folder branch means ownership. An arrow means a named relationship such as
"feeds", "produces", or "depends on". Connect the actual endpoints; where two
Jobs use one output, show the shared node or a cross-link. Do not invent a
dependency simply to make the drawing look like a strict tree.

Use a small root and branch junctions with plain text leaves. Put state and the
next action beside the Job they describe, and its intended output on that same
branch. A repeated grid of equal cards obscures the hierarchy; adding decorative
arrows to it does not make it a connected map. Background and the main tree can
share a frame when the background is short. In the index, each topic and Job is
one row: its box, then the arrow to what it leads to, in one column; the frame
grows down instead of packing rows into columns (JL 261012: "each studio should
be a row"). Follow the parent skill's font, palette and frame limits. Actual slide drafts, screen mockups, report plots and
user-requested alternative layouts keep their own contracts.

## Keep current facts separate from the proposed finish

The generated index is the inventory authority; do not hand-copy its state or
counts into another maintained table. The background may explain relationships,
where to start, and expected outputs grounded in Job goals, close rules and
checklists. Identify an inferred output as **proposed**; if its consumer or close
rule is unknown, leave a red question there. A next action is not evidence that
the output exists. Do not change Job state or Topic stage to make the index look
finished.

Show source dates when they matter, especially for an external status that may
have changed. Checklist counts describe recorded steps, not readiness percentages.
For a large Block, summarize Tasks with explicit counts and a link to the full
inventory rather than omitting work or shrinking the drawing's type. Keep every
Studio and Job findable, even when its details are folded.

## Check the map before handing it over

Compare the index's Studio and Job ids against the folders on disk; account for
all of them and check the named outputs against their sources. Resolve local
links. Inspect the drawing in the workbench: follow a branch from the Block to
a Job and its output, check that arrows reach their endpoints without crossing
text, and read it at 50% and 100%. Redraw through `canvas.write` to preserve human
marks. Record the work as the topic's session, with any uncertainty left in place.
