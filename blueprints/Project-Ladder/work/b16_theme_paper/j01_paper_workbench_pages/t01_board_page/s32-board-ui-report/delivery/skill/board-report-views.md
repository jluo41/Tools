### The focused Paper Board: seven content Views

The current focused Board uses Report → Review Content → Around the Work.
Review Content combines each View's content and its existing preparation actions.
Legacy `section=work&group=work-<key>` Board links open the corresponding Report
View. The classic frame and specialized Job/Task Report/Work workflows remain
supported separately; Board behavior does not imply their migration.

| Key | View | Content sources and Sections |
|---|---|---|
| idea | Idea | Ideation topic: Directions and Theory; Related from the Board reference records, even when a Story exists. Direction appears here only before a Story exists. |
| story | Story | Current Story topic and chosen direction: Direction, Pitch, Theory, Research Questions, Stakes and evidence, Related, Venues and Story by Section (left tabs: first the whole paper's Story arc, then each Section's part of the arc, its claims last). |
| plan | Data + Paper Plan | Data flow and Paper flow from their topics, then Roadmaps and the preparation plan, Runs to do and next steps to the send. |
| explore | Support blocks | Internal Work and external Discovery Blocks named by the paper, linked back to their source work. |
| evidence | Evidence | Returned values and citations from evidence Jobs, with their current state. |
| displays | Displays | The display plan, display previews (each display's state in its tab), examples, then last Story by Section from the same Story topic, the same section the Story view shows. |
| draft | Writing | Version sections, assembled documents, portal preparation and sections still to finish. |

**One source, several entry points.** Related in Idea and Story is the same
`related/` material. Closest-work positioning is owned by haipipe-paper-related;
record storage by haipipe-related. Story by Section in Story and Displays is the
same current Story topic's `Section Narrative`, owned by haipipe-paper-story.
Its per-version compile order remains with the writing Job and assembly. Neither
extra UI entry creates another authoring location.

Views and Sections depend on source content. No ideation topic means no Idea
View; no Story topic means no Story View. Evidence is registered when a
non-version Job exists (including submission); its Sections render only the
sources present. Displays is registered when a display Job or display-plan
topic exists.
Related is omitted when no reference items exist. Story by Section is omitted
when the selected Story has no Section Narrative. Do not invent source content
to fill a matrix cell.

Around the Work uses the shared unnumbered order: Studio, Interactions,
Decisions, Things to Know, Checklist, Timeline, Skills and Files. Supporting
records belong to a View through explicit `view:` metadata first, then their
linked Topic. Unassigned records stay available in the aggregate right rail.
The same selection drives view-scoped Skills and Files. Studio is shown in this
shared group, not repeated above Idea and Story. Delivery remains a rail entry.

Section bars start closed. The view buttons stay above the goal. Content and
supporting sections use the shared components and style rules; no Paper-specific
copy of the common frame is introduced.

**Grant is a Paper type.** Its design shares Idea, Story, Data + Paper Plan,
Related and Story by Section with Paper Board. Funding-call requirements, aims,
approach, team, budget and submission preparation specialize the content.
Grant-specific rendering, examples and scaffolding are not implemented merely
because they appear in the matrix. See the Paper router's ownership table.

```text
servers/workbench/work_frame.py          shared sections and view ownership
servers/workbench/skills_section.py      skill catalog and links
servers/workbench-paper/paper_focus.py   Paper content adapter and scoped sources
                        board_views.py  View registration and classic wrappers
                        board_results.py content renderers shared across Views
                        board_process.py preparation actions and semantic skills
                        board_read.py   source topics, faces, tables and folders
```
