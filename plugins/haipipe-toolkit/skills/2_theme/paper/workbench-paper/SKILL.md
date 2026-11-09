---
name: workbench-paper
description: >-
  Read the Paper theme workbench: a Board's current focus Report, its shared
  supporting sections, and specialized version, evidence, submission and draft
  pages. Maps views to their source records and semantic skill owners; distinguishes
  the proposed Grant type from implemented Paper behavior. Also documents the
  classic frame. Trigger: Paper Workbench, paper workbench, paper theme, paper tab,
  version tab, Section tab, paper spaces, Grant Board design, /workbench-paper.
metadata:
  version: "0.57.0"
  last_updated: "2026-11-09"
---

# /workbench-paper · the paper theme on the shared frame

**LOAD `/wb` (the workbench skill) FIRST.** It defines the common Workbench law: STORAGE, SURFACE, WRITER and BOUNDARY, and
the frame every theme shares (`servers/workbench/`, `servers/workbench/README.md`). This skill is the paper's
delta: which views each level's Spaces show, where they read, and which run cards their Runs panels list.

The design is drawn in `Tools/blueprints/Project-Ladder/work/b16_theme_paper/`, its topics in the Block folder itself:
s11 (the Board), s12 (a version), s13 (a Section), s21 (the skills and Runs), s31 (the Guide by level). The page
designs are b16 j01's topics, under `j01_paper_workbench_pages/`: in `t01_board_page/`, s32 (the Board's Report,
agreed), s33 (the Board's Work) and s34 (its Studio); in `t02_version_page/`, s35 to s37 (a version's Report, Work,
Studio); in `t03_section_page/`, s38 to s40 (a Section's Report, Work, Studio). The paper's folders are
`haipipe-paper/ref/paper-ladder.md`. The four-Space page that came before (`/_board/paper-board`) is retired;
what it showed is kept in [`ref/old-page.md`](ref/old-page.md), since several views below still draw with its
renderers.

## 🔗 The link

```text
<DOMAIN>/_board/workbench?path=<Paper-…>                      the Board (Block tab)
<DOMAIN>/_board/workbench?path=<Paper-…>/<jNN_writing_v<MMDD>_<desk>>  a version (Job tab)
<DOMAIN>/_board/workbench?path=<…>/<jNN_…>/<tNN_<title>>       a Section, the Abstract or a letter (Task tab)
   &space=<Space>&sub=<view>                                   open one Space and view

<DOMAIN>/_board/workbench?path=<Board>&layout=focus&section=report&group=<key>        the focus page, Report
<DOMAIN>/_board/workbench?path=<Board>&layout=focus&section=work&group=work-<key>     the focus page, Work
   <key>: story · plan · explore · evidence · displays · draft   (views A to F)
```

The first block is the frame layout. **Report and Work use the focus page** (`layout=focus`,
`servers/workbench/focus_page.page_url`): `section` picks Report or Work, `group` the view, `work-` before the key on
Work. An older `jNN_v<MMDD>_<desk>` version folder still opens.

**Every Run address is a link** (JL 261103: "b52.j01.t01.r01 <--- how could you make this to be clickable"). A
`bNN.jNN[.tNN[.rNN]]`, or `bNN jNN tNN` with spaces, in a paper Board's views, a version's Work views and a draft
Section's step pages opens that folder's focus page (`?path=<folder>&layout=focus`, `target=_top`), found in the
address's own Project, `work/` first, then `discovery/`; a Run number that is shared or missing opens its Task (then
Job, Block). A Section name `tNN_<name>` of a writing Job opens that Section's Work › Write view. An address that
finds no folder stays plain text, and a page never links to itself. One helper does it,
`servers/workbench/address_links.py` (`live.address_links`: `resolve`, `href`, `linkify`, `page_linker`,
`linked_views`; standard library only), applied where the views are built (`board_views`, `paper_version`,
`focus_draft.parts`, `draft_steps.step_view`); never copy it into a page's own code.

`path` is the folder, relative to the SPACE root; `/w/<paper-board-folder>` lands on the Block tab. `<DOMAIN>`
is the origin the reader uses (the host's `--public-url`); find the listening port before quoting a link, and
never hand a remote reader `127.0.0.1`. Follow the link and read one real value off the page before returning it.

## Paper types and semantic owners

Paper Board and Grant Board belong to the same Paper theme. Grant shares the
Paper content and lifecycle contracts; its extra Sections adapt the funding
call, aims, approach, team, budget and application package. Its design uses Idea,
Story and Data + Paper Plan too. Venues means the funding program/call and Paper
flow means the application narrative in that context.

The [Paper router](../haipipe-paper/SKILL.md#paper-types-and-shared-content)
links each content owner. This skill owns which source the UI reads and where
it appears, not the source’s meaning or approval. Related reads the same Board
records in Idea and Story. Story by Section reads the same Story topic in Story
and Displays. Never copy records to make another View.

The Grant matrix is a proposed adaptation, not an implemented Grant renderer,
scaffold or example. Keep that status explicit and do not link its examples to
a manuscript page as though it were a working grant. Every Paper Board, Job
and Task page shows its type and use case under its title (the shared
`focus_page.page_identity_html`). The use case is the face's `use-case:` line,
else the single use its type has in the b16 matrices; a type with several and
none written shows none, never a guess. The face writes it: `haipipe-paper`
scaffolds stamp every new Board, Job and Task face, and `paper_ladder.py update`
(layout line L6) stamps an older Board's.

## 🪜 Classic frame and specialized level contracts

`servers/workbench-paper/paper_theme.py` exports `THEME`: `spaces(level, folder, root, sub)` returns each Space
of a level; anything it leaves out is the frame's vanilla Space. `level_patterns` reads both layouts: a
`jNN_` folder (or an older `Ba-`/`Bb-`/`Bc-` group) is a Job, a `tNN_` folder (or an older `S-…`, `RD<NN>`) a Task.

| Level › Space | Its third-row views | Reads |
|---|---|---|
| Block › Studio › Related (folds under the topics) | one part, folded until a Related link opens it | the frame's own view (`haipipe-related`): one row per `related/related.md` row, grouped by its subfolder first and then its `group` cell, each opening on its file (a Word file read in place, an email with its headers); files with no row yet, dashed. By question: Report › Related Papers, which leaves out meetings, files and emails and lists a paper under each question in its `group` cell |
| Block › Description | Scope · Venue · Resources | `board.md`; `venues/*/call.md`; `## Related resources` |
| Block › Idea Studio | one row per topic | `sNN-<topic>/` (the frame's studio rows) |
| Block › Audience Report | Ideation · Narrative · High-level logic + Low-level work · Related Questions · Related Papers | `board.md ## Questions` by `group:`, their `reports/qNN_`; the current telling's studio topic; the related papers under the question each bears on (`related/related.md`, else the telling's related-papers table) |
| Block › Work Details | Idea · Story · DataFlow · PaperFlow · Jobs | the paper's steps before its versions, each Operation (Input, Prompt) over Result (its Studio topic's drawing, then Open and Decided): Idea the Ideation topic (s01), each idea a card; Story the Story topic (s02), as sections with a card per research question; DataFlow and PaperFlow the Plan topics (s03, s04); then the versions |
| Block › Report (focus page; legacy Work links redirect) | Idea · Story · Data + Paper Plan · Support blocks · Evidence · Displays · Writing | `layout=focus&section=report\|work&group=<key>\|work-<key>`; the views are below (🖥 The focus page) |
| Block › Runs · Delivery | (Delivery) LaTeX · Word · Cover letter · Rounds | the Board's `runs/`; the newest version's `delivery/jNN_<version>/`; then Sections in the build, every version's Sections from its `build-manifest.json`: ready at the build, in the build or changed after it, a link to each Section's part and its folder |
| Job › Description | Version · Venue rules | the version face; its venue's `call.md` |
| Job › Audience Report | Questions · Draft-Main · Draft-Appendix · Comments · Cover letter | the face's `## Questions` and the standing J1–J5; each Section as Question │ Work │ Report with its rendered draft beside its drawing; the comments reports' `## Review Items`; the letter by paragraph |
| Job › Work Details | All · Main · Appendix · Letters | its `t0N_` · `t2N_` · `t3N_` Tasks; the comments reports the letters answer |
| Job › Runs · Delivery | (Delivery) one card per kind: manuscript · letters · Sections · checks · sent | the version's `runs/`; its part of the Board's delivery, `delivery/jNN_<version>/` |
| Task › every Space | the Page Task's own views (`servers/workbench/workbench-task-draft`) | the Section folder; the paper adds the reader contract (Scope), its `SUB-*` rows (Requirement), Comments, and "ready for the build" apart from "done" (Delivery) |

**Markdown is the only truth source (JL 260918).** Every view is drawn from the paper's `.md` files (and
authored config, `paper-build.toml`; and receipts, `build-manifest.json`, `runtime.yaml`) on each open; a
Markdown edit is live on reload. The theme stores nothing: no `console/`, no `data.js`.

**Base styles only (JL 261007).** A view uses the classes the frame gives every theme (`servers/workbench/README.md`):
the folding `.topic` row, `.q-row`, `wf-table`, `.st-ok` · `.st-warn`, `.topic.missing`. A view still drawn by the
old page's renderer is wrapped in `pv()`, which scopes that page's stylesheet to it. The reading rules stay: base
type 16px, never under 12px, every table with cell edges, a closed card shows its whole headline.

## 🖥 The focus page: a paper Board's views (`layout=focus`)

<!-- render b16.j01.t01-s32 board-report-views: generated from Tools blueprints/Project-Ladder/work/b16_theme_paper/j01_paper_workbench_pages/t01_board_page/s32-board-ui-report/delivery/skill/board-report-views.md; edit it there, then render_delivery.py -->
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
<!-- /render b16.j01.t01-s32 board-report-views -->

**Skills.** Current focused Boards show Skills once in Around the Work and in the aggregate rail. `board_process.py` `VIEW_SKILLS` supplies the semantic owners; it is not an extra PROCESS step.

## ✍️ Writer: the Runs panel

The theme is a read-only projection. **Its only engagement is the Runs panel** of each Space: the buttons are the
run cards of `haipipe-paper-workflow/ref/run-cards.md` whose Space field is that `<Level> › <Space>`, kept for the
open view (`paper_theme._run_cards(level, space, view)`); a Section's buttons are the Page workflow's cards. As
every button of the frame, it is named by the Run it makes (the card's `🏷 RUN` line, `run-<type>-<target>`), its
label in small under it (haipipe-run `ref/run-types-by-space.md`). A button shows its skill and copies its prompt, `{folder}` filled with the open folder; the person runs it in a
Claude or Codex session. Clicking never sends, starts, allocates or writes.

Every Run is `run-<type>-<target>` (no date): a Board's or a version's is a folder in its `runs/` (`run.yaml`, ticket,
`passes/`, the shared Run contract); a Section's is its Page engine ticket. The run types,
with each one's agent, skill and sign, are `ref/workbench-table.md`; `table-workbench --check --cards` keeps the
table and the cards equal.

## 🧭 The Guide

The Guide tab reads `servers/workbench-paper/guide/guide.yaml` (family `paper`): its description, the Workbench
Table (`ref/workbench-table.md`, this skill's), Method (`guide/method.md`, split by level, its cards in
`guide/methods/`, its canvas `guide/methods.excalidraw`, the canvas being the source), RoadMap Draw, and Related
Paper (`servers/workbench-paper/related/papers.md`, `table-papers`).

## 🚦 Gates

The theme shows each gate where it is signed; the named owner closes it, never the screen:

```text
Board    G0 the admitted idea · G1 release of Task work · G2 the claim state and the answer
version  G3 release of one Section (Draft-Main) · G4 submission readiness (Delivery › checks) ·
         G5 every response answered (Comments, the t32_response letter)
```

The theme never infers a human approval from a percentage, a folder's existence, a generated PDF or a
`recorded` row. Gates: `haipipe-paper-workflow`.

## 🚧 Boundary

The theme coordinates the paper; it never becomes the owner of Page prose, Evidence Results, Discovery records,
Task configurations or delivery wording, and no view copies an authority record to make a table easier to draw.
The frame (`servers/workbench/`, `servers/_host/`) belongs to its owner; ask before changing it.

## ✅ Completion checks

- `servers/workbench-paper/tests` and `servers/_host/tests` pass; every paper Board renders at every level.
- Every button of every level's Space is a run card; `render_workbench_table.py ref/workbench-table.md --check
  --cards ../haipipe-paper-workflow/ref/run-cards.md` says PASS.
- No view writes, and none reads a `console/`, `data.js` or other per-paper projection.
