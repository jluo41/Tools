---
name: workbench-paper
description: >-
  The paper theme of the shared workbench frame: a paper Board, each version and
  each Section open on the frame's top row Guide · Studio | Paper Board ·
  Version ▾ · Section ▾ | Delivery, each level with its work row (Description ·
  Report · Work · Runs) and a Runs panel whose buttons are the paper's run cards by
  level and Space; Studio (with Related folded under its topics) and Delivery are the Board's. Read-only: it shows the paper's Markdown and copies prompts.
  Trigger: Paper Workbench, paper workbench, paper theme, paper tab, version tab,
  Section tab, paper spaces, /workbench-paper.
metadata:
  version: "0.52.0"
  last_updated: "2026-11-01"
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

## 🪜 Levels and Spaces

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
| Block › Report · Work (focus page) | Idea · Story · Data + Paper Plan · Support blocks · Evidence · Displays · Writing | `layout=focus&section=report\|work&group=<key>\|work-<key>`; the views are below (🖥 The focus page) |
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
### The paper Board's Report and Work: seven views, A to G

A paper Board's Report and Work show the paper's four layers as views, one button each, in this order, with the same
letters on both (b16 s32-D12, s33-D02): the plan (A to C), what supports it (D), the evidence (E, F), the writing (G).
Idea (the many directions) and Story (the one chosen) are two views (s32-D44); Data flow and Paper flow are one,
Data + Paper Plan (s32-D28, D29); Venue is inside Story (s32-D12); Displays stands after Evidence and before Writing
(s32-D26). A view shows only when the Board has its part: no ideation topic, no Idea view; no Story topic, no Story
view; no evidence Job, no Evidence view; no display Job or display plan, no Displays view.

```text
idea      A Idea               the many directions: 🎨 Studio, then 🔀 Directions and 🎓 Theory as left tabs (no Story yet: 🧭 Direction first, 📚 Related after Theory)
story     B Story              the one chosen: 🎨 Studio, Direction, Pitch, Theory, Research Questions, Stakes and evidence, Related (related/related.md), Venues (venues/<venue>/call.md), Story by Section
plan      C Data + Paper Plan  🗄️ Data flow and 📝 Paper flow, each its topic's mind map worked on in place, then 🗺️ Roadmaps; each topic's drawing after the dashed rule
explore   D Support blocks     🧪 Work and 🔎 Discovery: the Blocks its pages name, one folder tree per Project, folding down to each Task's Runs
evidence  E Evidence           🔢 Values and 📚 Citations: a left tab per Task, the thing itself on the right
displays  F Displays           Plan (the display plan's drawing), 🖼️ Displays by Main, Supplement and Others (each its preview.pdf), 🔍 Examples
draft     G Writing            a ✍️ section per version, its Sections as left tabs to read; 📄 The assembled paper; 📮 Ready for the portal
```

**Every view ends in 🙋 Interaction, and every bar starts closed** (s32-D38, D41, D42). The last numbered section of
each Report and Work view is 🙋 Interaction: the collection Runs about this view, a left tab per question and its form
on the right, Back and Next, Copy feedback on a set's last question; with none it says so. Every section bar starts
closed (▸); what you open stays open in this browser.

**The Report is the view's own sections, 1, 2, 3; Work adds two bands, each numbered from 1** (s32-D27, from
s32-D22 and s33-D03; JL 261101: "for the Results and Process, they will just be in the Work"). ⚙️ PROCESS is how the
layer is being made, step by step (s33-D06): 📌 Open points, only when a part's face marks lines waiting for you; then
the view's own steps (Idea and Story 🚧 Open; Data + Paper Plan 🧭 Plan, ⚙️ Runs to do when the Story has a Task
Roadmap, 🗓️ Next steps to the send; Evidence 📋 Where each stands; Displays 🖼️ Where each display stands; Writing 🪜
Sections to finish); then 🧰 Skills that do it. PROCESS has no 🙋 step: the open forms show once, in 🙋 Interaction
(JL 261105: "keep only the bottom"). 📊 RESULTS is the Report's sections, drawn with the same code, so the two never
disagree. A PROCESS title names the step, never a count (s33-D08).

**The Data + Paper Plan view's PROCESS is the plan center** (s33-D07): 🗂️ Design the dataset, 📈 Design the
regressions, ⚙️ Make them run, 🖼️ Plan the displays, 🔎 Plan the reading, each one row with the skill to use, Open (the
mind map, the main analysis Job, the Story's roadmaps, the display plan) and Copy prompt; the prompt has the session
screenshot the mind map and show its plan before any change.

A state is always a coloured word: orange waits on you, blue running, green done, grey not started or open.

```text
servers/workbench/ui_parts.py            the shared pieces and their stylesheet (phone rules last)
servers/workbench/interaction_section.py 🙋 Interaction, the last section of every Report and Work view
servers/workbench-paper/board_views.py   board_report_views, board_work_views: the two bands
                        board_results.py the seven views' RESULTS
                        board_process.py PROCESS: the rows, the plan center
                        board_read.py    BOARD_VIEWS; reading the Board's topics, faces, tables and folders
                        board_evidence.py, board_interactions.py, paper_version.py
```
<!-- /render b16.j01.t01-s32 board-report-views -->

**Skills band.** The PROCESS band's last section, 🧰 Skills that do it, shows in every Work view (`board_process.py`
`VIEW_SKILLS`); Data + Paper Plan's also lists the skills its plan rows name.

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
