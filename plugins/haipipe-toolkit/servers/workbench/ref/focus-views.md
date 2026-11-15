# Focus pages: views, Around the Work, Files and UI examples

Part of the [Workbench base README](../README.md).

Project and Theme pages open on **Report** and have no separate Work section.
Their legacy Work/Progress links resolve to Report → Themes; existing authored
Deliverables remain available in Report. A Theme named `work` keeps its name.

At widths of 600px or less, **Pages** opens the left navigation drawer and
**Sections** opens the right navigation drawer. The view buttons remain below the
title; rail links are no longer repeated there. Wider pages retain both rails.
Drawers close with their Close button, Escape, or a click on the backdrop.
Work's Interaction header keeps the waiting badge; question previews appear only
inside the section, not below its closed header.

The shared Studio section uses a Topic list on the left and the selected Topic's
preview on the right. Available Slide, Draw, MindMap, Work and Delivery assets open
inline, with an Open action for the larger view. Preview frames load only when
visible. On narrow screens, a Topic selector replaces the left list.

Work, CoWork, and Discovery now expose **Overview · Status · Findings · Delivery**
on live Block, Job, and Task pages. `work_frame.py` reads their existing records:
Overview contains Goal, Requirements and MindMap; Status uses the same Topic groups
as the map, with a pruned Block–Job–Task–Run tree and Dependencies. Question `work`
links define groups first; existing bands or children provide the fallback. Unlinked
work remains reachable. Findings keeps the theme's results; Delivery owns handoff
files, live services, explicit Acceptance and Usage notes. No acceptance is inferred.
Report and Work are one **Report** entry for these pages. Each view shows Review Content,
including its existing actions when present. Status uses View BJTR: topic tabs on the
left and the linked Block–Job–Task–Run tree on the right, replacing Next steps. The right rail and narrow
screen drawer omit Work; old `section=work` links resolve to the matching Report
view. Job and Task default links retain their Status landing view.

Group headings use an icon, bold title and trailing rule. **Review Content** contains the
view's output and next steps, without a separate Process heading;
**Around the Work** contains eight unnumbered sections, in the same order and
with the same labels/icons as the right rail: Studio, Interactions, Decisions,
Things to Know, Checklist, Timeline, Skills, Files. Both entrances reuse the same
renderers and source records. The rail aggregates the page and its descendants;
view sections use one explicit scope across Studio, Interactions, Decisions,
Things to Know, Checklist, Timeline, Skills and Files. A `view:` field on a page
face or Run takes priority; otherwise a linked Studio Topic must have a matching
view tag (Overview/MindMap, Status, Findings, Delivery, Block UI, Job UI, Task UI).
Unassigned topics and records remain in the right rail, never default to Status
or repeat as common context in every view. The right rail includes only the
current page and its descendants, not ancestor notes.

Decisions, notes and Checklist follow their assigned page or Topic. Timeline
uses that same selection for records and exact Run receipts; page-wide commits
stay in the rail. Delivery records belong to Delivery. No date or approval is
inferred. Skills in a view come from its declared support skills, assigned Tasks,
selected Runs and linked sections; rail Skills include all page support skills
without the former ten-item cap. Pending-question counts use the filtered items.

View Files uses selected Topic/Run directories and assigned page faces, never
falls back to the whole Block or SPACE stores. Its Tools · Skills uses the same
selected skills as Skills; Tools · UI links the source files implementing the
view and its authored view assets. The rail retains the full folder browser.
No records are moved, copied, or relabeled to fill an empty view.

Files uses five folder-type tabs: Workspace, Blocks, Code, Tools · Skills,
and Tools · UI. Only types with existing, accessible directories appear. The right
panel shows expandable folder trees rooted at SPACE-relative paths. Expanding a
folder loads one directory level and keeps its ancestors visible. Selected source
paths share their actual parent branches; intermediate groups include only relevant
paths, while each selected folder can be browsed normally. Clicking a file
opens the shared pop-out viewer; closing it returns to the same tree. Files retain
Open and Download actions. Workspace opens the
served SPACE's `_WorkSpace/` store and is hidden when that directory is absent; Blocks links the containing Block and relevant work pages;
Code opens the served SPACE's existing `code/` directory, never a Block's
src/scripts/config directories; the type is hidden when that store is absent; Tools · Skills resolves
relevant skills through the catalog, and Tools · UI links the current renderer,
theme renderer and authored UI directories. Nothing outside the served root is
exposed. Directory contents load on demand, rather than scanning the workspace.
Static-file policy applies to both listings and previews; text previews are bounded
to 200 KB with a truncation notice. Python previews use token-based syntax highlighting
without executing the source or loading external libraries. Text previews provide a
Line wrap checkbox; switching it off preserves original line widths with horizontal scrolling. No files are copied or moved.

The old `group=mindmap` and `section=delivery` links remain supported. Paper Boards
also use the Report/shared-section frame through `../workbench-paper/paper_focus.py`,
retaining their seven paper views and separate Delivery entry. The adapter supplies
paper Topic ownership and skills to the shared renderers; old Board Work links
open the matching Report view. Paper versions and draft Tasks, Labeling and
specialized Question Book pages keep their existing workflows.

A theme blueprint may keep an authored type/view comparison in `ui/block-views.md`,
`ui/job-views.md`, or `ui/task-views.md`. Its matching UI view reads the Markdown
as a closed **Type × View Button** section.
Blueprints without that file retain their existing sections.
The Project blueprint can declare `ui-project: <Project path>` to add **Project UI**,
with its comparison in `ui/project-views.md`. Any configured UI view may also
provide `ui/<level>-preview.html`: a separate **Proposed UI** section, served only
from inside the current root. This never replaces the current live example.
An optional `ui/structure.md` adds a preceding **Work Structure** section.
Its `##` headings select structure tabs; `###` headings select nested
topic examples. These authored examples are explanatory, not live execution state.
An optional `ui/view-guide.json` supplies section definitions, expected outputs,
layouts, examples by type, and skills by view. Matching section names become
buttons opening a read-only dialog; Close, Escape, or a click outside dismisses it.
Set `proposed: true` in the guide to omit links from these explanations to current
pages that do not yet implement the proposed views. Live examples remain separate.
Live UI examples use the shared left-tab/right-content component even when only
one example is configured. The tabs select actual example pages; their right
panels embed the page and offer an Open action. Optional `ui/example-types.json`
maps each `block`, `job`, or `task` example path to its display type. That type
names the left tab in both the preview and its walkthrough; the actual example
name remains in the preview and Open link. Unmapped examples retain their labels.

Delivery storage (JL 261010)
---------------------------

Only the Block owns a physical `delivery/` directory. Job, Task and Report
outputs retain their source identity under it: `delivery/jNN_<job>/`,
`delivery/jNN_<job>/tNN_<task>/<lane>/`, and
`delivery/reports/qNN_<report>/<lane>/`. The Block's own output uses
`delivery/<lane>/`. Job and Task Delivery views select their source subtree
and link to the whole Block Delivery; they never create local delivery folders.
Runs and Results remain with their source. Every writer and reader uses the
shared `haipipe-draft/src/common.py` Delivery helpers. Standalone Pages without
a Block keep their own output root; an orphan jNN/tNN must acquire a Block.

In this skill, a Page's or Job's `delivery/<lane>/` means its source subtree
inside Block Delivery. Old local lanes are read-only migration inputs. Rebuild
from source before removing generated output; preserve a hand-owned fragment
when the source cannot reproduce it. A storage migration grants no acceptance,
release, send or submission approval.
