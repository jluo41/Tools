### The focused Paper Board: seven content Views

The current focused Board uses Report → Review Content → Around the Work.
Review Content combines each View's content and its existing preparation actions.
Jobs and Tasks are selected inside their owning Block; their content and workflow controls follow their own source contracts.

| Key | View | Content sources and Sections |
|---|---|---|
| idea | Idea | Ideation topic: Directions and Theory; Related from the Board reference records, even when a Story exists. Direction appears here only before a Story exists. |
| story | Story | Current Story topic and chosen direction: Direction (its question large, `**Label**:` paragraphs as label rows), Pitch (the one-sentence identity large, then the pitch a sentence a line; the stage only on the bar; `⟦pending …⟧` a muted chip), Theory, Research Questions (the paper's question large, then ONE table, a row per question, every field side by side: RQ | Question | Why we ask | Asked before | New here | Expected (the report link at its end; no State column), the three middle columns from §3's table when it has them; full card width, the paper's question on its left edge; stacked per row on a phone), Related, Venues (each card's first row its editor's test, from §9's `editor's test` column, with an "Open the editor's test" pop-out when the Board has `reports/q*_editor_test_<venue slug without hyphens>*/`; under it "To pass the desk", a numbered list of the first sentence of each item in that report's `**To raise the odds**` list, hidden with no report) and Story by Section (reads § 8 as the shared narrative; left tabs, right content: first the whole paper's Story arc from § 8, then a tab per Section from the newest version's `## Narrative` row, its small line what the reader leaves with; its panel Reader asks, Comes in with, Moves as a numbered list 1, 2, 3, Leaves with, Hands on, Must not say, Displays, then its claims); no Open points section. Prose shares one 92-character measure centred in the card, text left-aligned; a compared table (the Research Questions) takes the card's width. |
| plan | Data + Paper Plan | Two sections, the skill's Plan : 1 · 🗄️ Data flow, the s03 topic's Excalidraw drawing (how the data become each answer), and 2 · 📝 Paper flow, the s04 topic's drawing (how each answer becomes the page), as Displays shows s06. Each bar carries a small Prompts button with that flow's plan prompts (Data flow: design the dataset, design the regressions, make them run; Paper flow: plan the displays). Every fact once: no summary on top, no Runs to do (§ 7 shows in the Data flow drawing), no separate Plan prompts; the § 6 reading is the Story view's 📚 Reading. A line that is only a template slot (`<...>`) is not shown. |
| explore | Support blocks | Internal Work and external Discovery Blocks named by the paper, linked back to their source work. |
| evidence | Evidence | Returned values and citations from evidence Jobs, with their source marks. |
| displays | Displays | The display plan, display previews (each display's state in its tab), examples, then last Story by Section from the same Story topic, the same section the Story view shows. A tab names its display by the face's `name:`, else the s06 plan's `name`, using the display's source name; a Task whose face says `number: not printed` is left out (`board_displays.retired`). |
| draft | Writing | Version sections, assembled documents, portal preparation and sections still to finish. |

**One source, several entry points.** Related in Idea and Story is the same
`related/` material. Closest-work positioning is owned by hai-paper-related;
record storage by hai-related. Story by Section in Story and Displays is the
same current Story topic's `Section Narrative` (§ 8: title, story, claims; no
Section rows), owned by hai-paper-story. Its Section rows and per-version
compile order remain with the writing Job's `## Narrative` and assembly. Neither
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
servers/workbench/page/job_task_views/work_frame.py          shared sections and view ownership
servers/workbench/side_pane/rail_sections/skills_section.py      skill catalog and links
servers/workbench-paper/paper_focus.py   Paper content adapter and scoped sources
                        board_views.py  View registration and content composition
                        board_results.py content renderers shared across Views
                        board_process.py preparation actions and semantic skills
                        board_read.py   source topics, faces, tables and folders
```
