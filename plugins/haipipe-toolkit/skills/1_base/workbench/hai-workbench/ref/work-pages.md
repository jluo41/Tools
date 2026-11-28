# Work and Blueprint pages

A Work Block carries execution records. A Work Block (Blueprint) defines and verifies a
tool, its pages and its skills. Both use the shared Block framework. Determine the
role from the Block's purpose and authored configuration; an example directory
alone does not decide its type.

## Page and selection

The Block is the page owner. Jobs, Tasks, Runs and Studio topics remain inside it.
Resolve the Block before invoking the workbench opener, then select the requested
record through its controls. Preserve its title and route while switching items.

Job group, Job type, Task group and Task type are different concepts. Use explicit
faces, `bands:` and the Block type's contract. A name substring does not establish
a type. Show only the levels the Block actually uses. A placeholder is written in
`〈 〉`; an agreed real name is not bracketed. Groups are presentation associations,
not permission to add topic folders to the storage tree.

A Job's Main describes that Job. Its Task selection reads that Job's real Tasks,
with Run records below them. Keep selections and content isolated when different
Blocks contain identically named Jobs or Tasks.

## Content and supporting records

Read the actual applicable views and their source records. Work content includes
Overview, Plan + Results, Findings and Delivery; authored sections can specialize
that content. Blueprint UI controls require authored examples and bindings. Do not
add them to an execution Block merely to make its screen resemble a Blueprint.

- Overview reads the selected record's goal, requirements and authored sections.
- Plan + Results reads actual Jobs, Tasks, Runs and dependencies.
- Findings reads recorded outputs and their source bindings.
- Delivery reads artifacts, acceptance and usage records.

The renderer for authored sections is
`servers/workbench/page/job_task_views/work_sections.py` (paths here are relative
to `plugins/haipipe-toolkit/`). `## Review Content`, `## Plan + Results` and
`## Findings` name content; `###` headings divide it. Their `embed:` and `each:`
lines must resolve to supported, existing content. The Work writing procedure is
`skills/2_work/work/hai-work/ref/propose.md`.

Supporting content includes Studio, Interactions, Decisions, Things to Know,
Checklist, Timeline, Skills and Files. Inside a view it follows the supported
view/topic association; the Block-level rail can collect across views. Preserve
explicit associations. Do not attach every record to every view or invent content
to fill an empty section. An empty section is omitted.

## Preview, inspect and comment

Use the shared top-view, left-tab, right-content controls. A single item uses the
available content width. The top-right preview dot opens that content; the
left-list dot controls its list. Reuse shared file previews and the pop-out viewer.

A live preview reads the actual server-rendered example inside its owning Block.
A proposal is separately authored material. Read each Studio's current manifest
and owning type contract; do not report a design as implemented until its real
page has been checked.

Comments use the recorded address and scope of a registered element or marked
content item. Desktop right-click and touch long-press open the element menu on
supported targets; Comment opens its input. This does not provide targeting for
arbitrary DOM or embedded content. Verify the saved address and scope when reading
or adding a comment; do not assume a label-derived address survives a rename.
Use the existing cards and writer described in `servers/workbench/ref/cards.md`.
Saving a comment does not itself start an AI execution. Read its saved thread
before acting; keep mobile gesture and keyboard verification distinct from
simulated browser checks.

## Files and skills

The shared Files pane reads real folders and keeps their nesting and SPACE-relative
paths. Its roles are Block, Maintain, ReadFrom and trace-derived Touch. The role
explains the relationship; a displayed ordinal is a position, not identity.
Links and selection remain bound to the actual path when order changes. Omit empty
roles. Workspace and code references must resolve to actual folders; do not create
placeholders to fill the UI.

Skills inspection opens actual skill files and folders. Read `SKILL.md` first,
then the relevant constitution and references. The displayed skills must own or
support the selected work. Do not replace a real file with a copied summary or
assign every available skill to every Block.

## Acceptance and ownership

A Checklist item names an observable outcome, its owning skill rule and evidence.
Distinguish a missing applicable feature, an inapplicable requirement and an
unresolved contract. A walkthrough or file presence proves only what it checked.
Use the existing scoped Checklist writer and reader; the renderer does not certify
all skill requirements automatically. Keep unresolved checks in the work records.

Shared controls and page wording belong to `hai-ui`; Studio records and bindings
to `hai-studio`; record alignment to `hai-work` with the Block, Job, Task and
Run owners. Follow these owners' checks before recording completion. History and
implementation plans belong in the Block's records and Trace, not in this contract.
