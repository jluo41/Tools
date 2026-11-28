# Propose a Block's structure from its material

`/hai-work propose 〈Block〉` reads the Block's material and proposes its own
sections and Jobs. Confirm the proposal with the person before creating records.
Use the standard sections when they express the material well; otherwise use the
supported authored-section format.

## Read

Read the Block face and its source material, Studio topics, linked inputs and
outputs. Identify the material's real groups, questions, dates and relationships.
Prefer an existing meaningful group over one invented for visual symmetry. Keep
source identity and the evidence behind each proposed section.

## Propose

Prepare a reviewable proposal containing:

| Part | Purpose | Source |
|---|---|---|
| Overview sections | What the reader needs to understand the work | Its goal, scope, context and requirements |
| Findings sections | The work's answers and outputs | Recorded evidence and meaningful source groups |
| Jobs and Tasks | Work needed to produce or check those answers | Concrete goals and the owning type contracts |

Keep observed work separate from planned work. Cite existing Run cards and receipts
for completed execution. Do not manufacture completed Runs from an artifact or a
memory of work. A repeatable build is executed only when authorized and through
its actual writer, with a real receipt.

Use the existing interaction mechanism governed by `hai-interaction` to present
choices and record the person's decision. Its schema determines the record; do
not invent a second approval format. List each concrete file change and follow
repository approval rules before applying the accepted proposal.

## Build the accepted structure

1. Author source-backed Markdown sections. When material is generated, maintain a
   builder that reproduces it from the declared sources; preserve manually written
   material and stable comment IDs. Each section file has a meaningful `#` title.
2. Bind sections from the Block face: `## Review Content` supplies Overview,
   `## Plan + Results` adds content after Jobs, and `## Findings` supplies findings.
   Each `### 〈title〉` is one section. `embed: 〈path〉` includes supported Markdown
   or SVG content; `each: 〈glob〉` creates one section per matching Markdown file,
   using its title. Resolve paths relative to the owning records as the reader does.
3. Keep authored content inside the Block's shared sections. The section embed
   reader accepts Markdown and SVG; an HTML design proposal belongs in its Studio
   binding, not in an unsupported section embed.
4. Use the Block, Job, Task and Run owners to create accepted work records. Declare
   real goals, close conditions and types. Use explicit grouping fields and keep
   use cases distinct from types. Do not create empty Task or Run records merely
   to populate a view.
5. Preserve source links and required human decisions. Keep plans and execution
   evidence in their owning records, and record this work in the Block's Trace.

The section reader is
`plugins/haipipe-toolkit/servers/workbench/page/job_task_views/work_sections.py`.
It also supports folded list details and time-labelled lists. Prefer the simplest
supported structure that represents the material; do not create a separate renderer
for one Block.

## Check

Resolve the Block before opening it with `workbench`. Verify all applicable views,
each accepted section and its source links. Empty content, broken embeds, console
errors or duplicate records are failures to fix, not evidence to mark complete.

Follow `hai-ui`'s readability checks using a fresh reader for generated
sections. Save the actual evaluation under the owning Block and address the
reported issues. Inspect Job and Task selections against their real records;
verify completion only where the execution and acceptance evidence support it.

Rebuild generated sections once and inspect again. Their content, source links,
comment IDs and manually authored material must survive. Report what was created,
what was verified and what remains undecided or untested.
