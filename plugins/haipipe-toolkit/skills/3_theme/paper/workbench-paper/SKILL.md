---
name: workbench-paper
description: "Read the Paper theme inside its owning Block: Report content, Writing and evidence Jobs, draft Tasks, Studio definitions and their source skills. Trigger: paper workbench, paper tab, version tab, Section tab, /workbench-paper."
metadata:
  version: "0.66.0"
  last_updated: "2026-11-27"
---

# Paper workbench

Read [CONSTITUTION.md](CONSTITUTION.md), then load the shared
[workbench skill](../../../1_base/workbench/hai-workbench/SKILL.md). It owns navigation,
page layout, file previews and the rules for opening work. This skill owns Paper
content bindings and routes each edit to its scientific or material owner.

## Open the owning Block

Resolve the SPACE root and its existing host. Open the Block's focus page, then
select the requested Job, Task or Studio topic inside it. Keep the Block title
and route. Use the configured reachable origin for a remote reader and verify
the actual page before returning its link. Repository links are origin-relative.

```text
/_board/workbench?path=〈Block〉&layout=focus&section=report
/_board/workbench?path=〈Block〉&layout=focus&section=jobs
/_board/workbench?path=〈Block〉&layout=focus&section=studio#〈topic〉
```

A file's presence does not establish a passed check, human approval or submission.
Read the source record and its material owner before describing the result.

## Paper definition in Studio

The owning Blueprint is `examples/Project-Ladder/blueprint/b16_theme_paper`.
Its Bands come from Work's shared `studio_types` and b17's type topics; do not
copy the classification or add a Paper Job group as a new Band. Empty Bands are
omitted. Each Studio fold opens independently.

| Studio | Content |
| --- | --- |
| [s01 Idea](../../../../../../examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/s01-idea-block-structure.md) | Candidate Jobs, assessment Tasks and their owning skills |
| [s02 Grant](../../../../../../examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/s02-grant-block-structure.md) | Funding-application structure and its contract boundaries |
| [s03 Paper](../../../../../../examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.md) | Paper folder, Job-Task and Studio organization |
| s11 Idea preview | Authored preview proposal; the live Idea-Example is available through s01 Examples |
| s13 Paper preview | Live Paper-Example Job views and authored proposals |
| s53 Paper Skills | Paper skill design material; the selected skill file defines its current contract |
| s81 Paper Theme Guide | Paper guide design material |

Idea, Grant and Paper are three instances of the shared **Block Structure** Studio
Type. Read b17 `s71-studio-type-block-structure/elements.md` and its views manifest.
Each instance supplies Structure (Folder / Job-Task / Studio), Job types, Task
types, Draw, its verified Examples and Skills. Do not replace that contract with
a theme-specific list of buttons. Omit Examples when no real Block is bound.

The four lists in each topic's `types.md` are the source for type pages, built by
`hai-studio/gallery/block-structure/scripts/block_types_pages.py`. Each type defines its purpose and
required content. Distinguish a semantic role, an observed reader field and a
registered executor; names in 〈 〉 remain proposals. The catalog registers no
execution type and grants no migration or submission authority.

Structure's Studio item describes the actual Idea, Grant or Paper Block: each
Band's name and number range, the Studio types it contains, and what one topic
addresses. Its source is `structure/studio.md`. Those research Bands are distinct
from the Blueprint's shared Studio Bands. Candidate-specific discussion belongs
inside its Idea Job; portfolio discussion belongs at Block level.

Idea-Example, Grant-Example and Paper-Example supply live Folder, Jobs and Studio views through the existing
Block routes. A generated inventory is a reference snapshot, not a live source.
Idea and Grant examples contain illustrative hypotheses and application material; they do not claim scientific results or human selection. Grant Draft examples keep their sentences in `draft/<task>-draft-v1.0.md`; the existing Draft Lab reads them. Their presence does not certify the Story/Presentation Main adapters (see `ref/topics.md`, T13). Skills opens actual owning
SKILL.md files. Draw opens one canvas, built with shared Studio helpers, retaining
every source node and parent. Structure uses S71's folder-style trees.
Type-member links select their Job and Task inside the owning Block.

Use the shared top views, left items and right content. One item is full width.
Structure's Folder, Job-Task and Studio use the shared folder-tree renderer, with
expandable rows and purpose on hover. Open Folder to the Job. Job-Task has at
most four levels: Job group → Job name → Task group → Task name; omit unused
levels. Use S71's common level colours, including its dark-mode palette. Mind-map
cards do not satisfy this view. A changing instance name is written as `〈manuscript name〉`; agreed group
names such as Story and Writing have no brackets. Keep real example names exact.

Paper and Grant structure design uses Story, Evidence, Display, Writing and
Presentation. Story and Evidence are shared Jobs in that design. Main, Appendix
and Explore name Display roles; Review and Submission are groups inside a Writing
Job. A version or a writing step does not create an execution type. Read real
faces and the owning skill before interpreting Job Type, Job Name, Task Type and
Task Name. A content heading such as research question is not by itself a Task.

The structure proposal does not register new types or move research records.
Known contract and preview gaps are recorded in [topics](ref/topics.md).

## Content owners

| Content | Owner |
| --- | --- |
| Block, Job, Task and Run records | Shared `hai-block`, `hai-job`, `hai-task`, `hai-run` |
| Idea candidate and assessment | `hai-ideation` |
| Paper organization and source routing | [hai-paper](../hai-paper/SKILL.md) |
| Story and Section Narrative | [hai-paper-story](../hai-paper-story/SKILL.md) |
| Paper values, citations and display evidence | [hai-paper-evidence](../hai-paper-evidence/SKILL.md) |
| Section prose and its reader contract | [hai-paper-draft](../hai-paper-draft/SKILL.md) and the shared draft skills |
| Comments and response routing | [hai-paper-comments](../hai-paper-comments/SKILL.md) |
| Assembled manuscript and submission artifacts | [hai-paper-assemble](../hai-paper-assemble/SKILL.md) |
| Workflow gates and Run cards | [hai-paper-workflow](../hai-paper-workflow/SKILL.md) |

Related in Idea and Story reads the same Board records. Story by Section in
Story and Displays reads the same selected Story topic. Per-version section
layout and compile order belong to the Writing Job's `## Narrative` and assembly.
Never copy an authority record merely to display it twice.

A Paper developed from an Idea Job retains its source and reviewed selection
links. Follow [the source adapter](../hai-paper-ideation/ref/idea-job-source.md).
The source Job owns scientific evaluation; the Paper topic projects its selected
revision and paper-specific framing. `ideation-origin.yaml` records pointers and
does not by itself implement a new control.

Paper and Grant use the shared Paper content adapters. Funding-call sections,
team/budget adapters and the target Job organization need their own verified
contracts and examples. A working manuscript page does not certify a Grant UI.

## Writing and draft material

A Writing Job's Structure view reads the selected Story and its own `## Narrative`.
It shows the Story arc and claims, then closed Section rows in compile order.
Each Section exposes its reader question, entry, moves, claims, displays, exit
and paragraph plan. Its linked venue examples come from the Task's `examples:`
source and `reads/` records; the same sources appear in the draft Task.

The narrative sign is read from the Writing Job's sign record and checked against
the source Story text. Paragraph constraints and exceptions belong to
`hai-paper-draft`; the shared draft map places findings at the affected
paragraph. The shared UI constitution governs marks and omits check tallies.

Run addresses use `live.address_links`; resolve them in their owning Project,
keep unresolved addresses as text and select child work within its Block. Do not
copy address resolution or invent a second page shell in the Paper adapter.

## Board Report

<!-- render b16.j01.t01-s32 board-report-views: generated from Tools examples/Project-Ladder/blueprint/b16_theme_paper/j01_paper_workbench_pages/t01_board_page/s32-board-ui-report/delivery/skill/board-report-views.md; edit it there, then render_delivery.py -->
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
<!-- /render b16.j01.t01-s32 board-report-views -->

## Runs, delivery and gates

The theme reads source Markdown, authored configuration and receipts. It stores
no per-paper projection cache. Changes to work records go through their owning
skills. Run cards in `hai-paper-workflow/ref/run-cards.md` name the skill and
prompt for the selected work; copying a prompt is not execution or approval.
Draft Tasks use their material workflow's controls and Run records.

Run types, agents and gates are indexed in [the workbench table](ref/workbench-table.md).
Use `table-workbench --check --cards` to compare the table with the owned Run cards.
A soft Run has its ticket, passes and results under its owning Task; use
`hai-run` for allocation and execution rules.

Delivery items name their artifacts: Paper-Latex, Paper-Latex-Diff, Paper-Word,
Supplement-Latex, Supplement-Word, Cover-Letter and the other actual outputs.
Read build manifests and source timestamps to determine which sections the build
contains. The scientific/material owner closes each gate; the UI never infers a
human sign from a file, a percentage or a generated PDF.

| Scope | Gates |
| --- | --- |
| Board | G0 admitted idea; G1 release of Task work; G2 claim and answer |
| Writing Job | G3 release of a Section; G4 submission readiness; G5 responses answered |

## Guide and verification

The Paper Guide reads `servers/workbench-paper/guide/guide.yaml`, its method
material, the workbench table and `servers/workbench-paper/related/papers.md`.
Read those sources before describing a guide entry as implemented.

For Studio bindings, run b16 `delivery/page-spec/check_block_structures.py --bindings-only`.
The full command also checks organization drawings; report its unresolved
findings separately. Open the running Block and test its map, example and skill
entry. For reader changes run the relevant Paper/shared reader tests. Skill
changes require the README fresh-context invocation check.

[Topics](ref/topics.md) records current questions, exact reports and remaining
work. Mark a topic fixed only after its case passes and a guard keeps it passing.
