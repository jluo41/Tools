---
title: Paper Studio alignment
date: 2026-11-27 15:48
topic: s03-paper-block-structure
aim: Use shared Studio Bands, embed the real example in Structure, retain the folded Paper map and current owning-skill instructions.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1548_studio_alignment.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/studio-views.json
  what: Remove the duplicate Examples top view; retain its authored structure and owning skills.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/studio-views.json
  what: Remove the empty Examples top view; retain its actual structure and owning skills.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/studio-views.json
  what: Put the real Paper-Example Block inside Structure; retain the simple folded map and Skills.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py
  what: Guard Structure / Draw / Skills and the real Block binding, preserving the mind-map checks.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/SKILL.md
  what: Document the current Paper Studio entry and scope using current rules only.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/CONSTITUTION.md
  what: Align the Studio rule with shared Bands, folded mind maps, bracketed variable names and embedded examples.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md
  what: Record this topic and the exact remaining source/preview gaps, without claiming unsupported types are implemented.
- do: edit
  path: examples/Project-Ladder/blueprint/b16_theme_paper/j01_paper_workbench_pages/t01_board_page/s32-board-ui-report/delivery/skill/board-report-views.md
  what: Synchronize the generated Board content rules with their owning source; preserve current details.
changed:
- examples/Project-Ladder/blueprint/b16_theme_paper/trace/261127/1548_studio_alignment.md
- examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/studio-views.json
- examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py
- plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/SKILL.md
- plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/CONSTITUTION.md
- plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md
- examples/Project-Ladder/blueprint/b16_theme_paper/j01_paper_workbench_pages/t01_board_page/s32-board-ui-report/delivery/skill/board-report-views.md
approval: User explicitly confirmed the listed plan; the linked generation source is the necessary dependency identified before editing.
---

# Paper Studio alignment

## Prompts

- **15:48** 你确定你整好了吗？你也就是按照这个方案去更新了吗？你有什么计划？如果你有计划的话，你就按照计划去执行吧。然后你要把这个链接给我一下，我打开看一看，好吧。

## Check

- PASS: check_block_structures.py --bindings-only validates all three Structure / Draw / Skills declarations and existing source paths.
- PASS: negative binding cases reject a missing Paper example, a Job used as a Block, an extra Examples view and a non-SKILL.md Skills target.
- PASS: 12 shared test_structure_views.py tests.
- PASS: fresh-context workbench-paper invocation; all 17 links resolve; generated Board guidance equals its source; source Idea ownership and proposed versus live behavior remain explicit.
- PASS: live Tailscale Block acceptance — shared Bands, folded Paper map, Paper-Example inside Structure, actual owning skill files and updated workbench-paper guidance.
- OPEN, pre-existing: full organization guard reports stale Idea and Grant generated maps. These source/drawing changes are outside this binding update and remain T08.
- Scope: no shared server edits, service restart, directory renumbering or new Studio types. Shared S75/S77/S79 definition removal belongs to Work and is not claimed here.

## Summary

Aligned the three Block Structure entries to Structure / Draw / Skills, embedded the real Paper-Example in Paper Structure, and retained the existing simple folded map. Updated current workbench-paper rules and their generation source, preserving prior wording below. T09 is fixed for this binding and skill case; T07 execution-contract gaps and T08 Idea/Grant map synchronization remain open.

Verified entry: [Paper Studio](http://100.121.165.84:5623/_board/workbench?path=examples%2FProject-Ladder%2Fblueprint%2Fb16_theme_paper&layout=focus&section=studio#s03-paper-block-structure).

## Preserved source wording

### plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/SKILL.md

> ---
> name: workbench-paper
> description: "Reads the Paper theme workbench: a Board's focus Report, its shared supporting sections, and the version, evidence, submission and draft pages. Use to find which source record and skill owner a view maps to. Trigger: paper workbench, paper tab, version tab, Section tab, /workbench-paper."
> metadata:
>   version: "0.64.0"
>   last_updated: "2026-11-21"
> ---
> 
> # /workbench-paper · the paper theme on the shared frame
> 
> Read CONSTITUTION.md first; it wins over this file.
> 
> **LOAD `/wb` (the workbench skill) FIRST.** It defines the common Workbench law: STORAGE, SURFACE, WRITER and BOUNDARY, and
> the frame every theme shares (`servers/workbench/`, `servers/workbench/README.md`). This skill is the paper's
> delta: which views each level's Spaces show, where they read, and which run cards their Runs panels list.
> 
> The current Block organization is drawn in `examples/Project-Ladder/blueprint/b16_theme_paper/`:
> [s01 Idea](../../../../../../examples/Project-Ladder/blueprint/b16_theme_paper/s01-idea-block-structure/s01-idea-block-structure.md),
> [s02 Grant](../../../../../../examples/Project-Ladder/blueprint/b16_theme_paper/s02-grant-block-structure/s02-grant-block-structure.md), and
> [s03 Paper](../../../../../../examples/Project-Ladder/blueprint/b16_theme_paper/s03-paper-block-structure/s03-paper-block-structure.md).
> Their shared Structure / Draw / Examples / Skills views are installed; an unbound Examples view is omitted.
> Each distinguishes Job Type, Job Name, Task Type and Task Name from grouping. A03 governs the target organization;
> unresolved runtime contracts and record migration remain explicit in the structures and `ref/topics.md` T07.
> 
> The earlier implementation and level designs remain in s11 (the Board), s12 (a version), s13 (a Section),
> s21 (the skills and Runs), s31 (the Guide by level). These preserve current/legacy behavior and do not override
> the named target organization. The page
> designs are b16 j01's topics, under `j01_paper_workbench_pages/`: in `t01_board_page/`, s32 (the Board's Report,
> agreed), s33 (the Board's Work) and s34 (its Studio); in `t02_version_page/`, s35 to s37 (a version's Report, Work,
> Studio); in `t03_section_page/`, s38 to s40 (a Section's Report, Work, Studio). The paper's folders are
> `hai-paper/ref/paper-ladder.md`. The four-Space page that came before (`/_board/paper-board`) is retired;
> what it showed is kept in [`ref/old-page.md`](ref/old-page.md), since several views below still draw with its
> renderers.
> 
> ## 🔗 The link
> 
> ```text
> <DOMAIN>/_board/workbench?path=<Paper-…>                      the Board (Block tab)
> <DOMAIN>/_board/workbench?path=<Paper-…>/<jNN_writing_v<MMDD>_<desk>>  a version (Job tab)
> <DOMAIN>/_board/workbench?path=<…>/<jNN_…>/<tNN_<title>>       a Section, the Abstract or a letter (Task tab)
>    &space=<Space>&sub=<view>                                   open one Space and view
> 
> <DOMAIN>/_board/workbench?path=<Board>&layout=focus&section=report&group=<key>        the focus page, Report
> <DOMAIN>/_board/workbench?path=<Board>&layout=focus&section=work&group=work-<key>     an old Work link: Report
>    <key>: story · plan · explore · evidence · displays · draft   (views A to F)
> ```
> 
> The first block is the frame layout. **Report is the focus page** (`layout=focus`,
> `servers/workbench/focus_page.page_url`; `group` picks the view). **Work is retired** at Block, Job and Task (JL
> 261111: "the Work is no longer used"): it is off the right rail, and an old `section=work` or `work-<key>` link opens
> the same Report view. What Work's ⚙️ Process held (a version's 🪜 Sections step words, an evidence Job's or Task's
> to-do rows and how it is made) is the first numbered sections of that Report view, with no Process or Results
> heading and no grey caption under the view buttons; each view's asks stay in its last 🙋 Interaction. An older
> `jNN_v<MMDD>_<desk>` version folder still opens.
> 
> **A version's Structure view comes first** (JL 261111: "it should be a view for the job workbench UI"; redone after
> "it is so ugly, could you try it again"): `group=structure` on a version's Report, before Draft-Main. Read-only,
> nothing copied (`servers/workbench-paper/paper_structure.py`). The whole-paper structure is this view, never a Task.
> Two numbered sections, no wide table, no sideways scroll at 390 px:
> 
> 1. **🧭 The story**: the Board Story's Section Narrative (shared by every version) by its parts, never its prose: from its ```text
>    block the TITLE large, the STORY in one line, the other keys (explanation, boundaries) small; the § 8 claims table
>    as small cards, each claim with its numbers; on the right the version's sign (`narrative-approved:`, written from
>    the person's words by hai-draft `page.py sign-narrative`): signed, not signed, or stale when the Story's Section Narrative
>    changed since (compared as text with `<version>/records/narrative-sign.md`). Links open the Story's Section Narrative and the
>    face's `## Narrative` as written.
> 2. **🗺️ The Sections**: one closed row per Section in compile order (the face's compile-order block), from the face's
>    per-Section table (`section | reader question | entry | ordered moves | must refuse | displays | exit`): the name
>    and the reader question, the moves as one step line, chips for the claims it carries (named in the row, or through
>    the face's "Claims to displays:" line by its figures) and its figures, a bar for its paragraph count (the current
>    Draft's `### C<n>.P<m> · <name>` headings) and its plan sign (`approved:`). Opened: comes in, must refuse, leaves
>    with, displays; its paragraphs grouped by C<n>; the venue's papers for that Section, one thin bar each (the first
>    `section.key` line of `reads/pNN-<author><year>/reading.yaml`, linked to `shots/section.jpg`), ours first (JL
>    261111: "the examples to be shared across the job level and each draft task"). One source, two levels: the row
>    reads the examples topic its Task face names in `examples:`, joined by `<author><year>`, so no file moves; each
>    draft Task's 📚 Examples card keeps showing its own Section. s04's Sections table (hai-paper-plan) is the
>    plan; this view is what the Drafts hold now.
> 
> **A paragraph out of range is marked** (JL 261112, hai-paper-draft § Paragraphs of 4 to 7 sentences): on the
> Plan mind map, both in Structure and in the draft Task's Plan view (one renderer, `draft_steps._plan_map`), an off
> paragraph's box shows "❗ <n> sentences (4 to 7)" in red, and one with a `reason:` line shows "<n> sentences · reason
> given" muted; a Section's tab in Structure carries no tally.
> 
> **Every Run address is a link** (JL 261103: "b52.j01.t01.r01 <--- how could you make this to be clickable"). A
> `bNN.jNN[.tNN[.rNN]]`, or `bNN jNN tNN` with spaces, in a paper Board's views, a version's Report views and a draft
> Section's step pages opens that folder's focus page (`?path=<folder>&layout=focus`, `target=_top`), found in the
> address's own Project, `work/` first, then `discovery/`; a Run number that is shared or missing opens its Task (then
> Job, Block). A Section name `tNN_<name>` of a writing Job opens that Section's Write step. An address that
> finds no folder stays plain text, and a page never links to itself. One helper does it,
> `servers/workbench/page/element_marks/address_links.py` (`live.address_links`: `resolve`, `href`, `linkify`, `page_linker`,
> `linked_views`; standard library only), applied where the views are built (`board_views`, `paper_version`,
> `focus_draft.parts`, `draft_steps.step_view`); never copy it into a page's own code.
> 
> `path` is the folder, relative to the SPACE root; `/w/<paper-board-folder>` lands on the Block tab. `<DOMAIN>`
> is the origin the reader uses (the host's `--public-url`); find the listening port before quoting a link, and
> never hand a remote reader `127.0.0.1`. Follow the link and read one real value off the page before returning it.
> 
> ## Paper types and semantic owners
> 
> Paper Board and Grant Board belong to the same Paper theme. Grant shares the
> Paper content and lifecycle contracts; its extra Sections adapt the funding
> call, aims, approach, team, budget and application package. Its design uses Idea,
> Story and Data + Paper Plan too. Venues means the funding program/call and Paper
> flow means the application narrative in that context.
> 
> The [Paper router](../hai-paper/SKILL.md#paper-types-and-shared-content)
> links each content owner. This skill owns which source the UI reads and where
> it appears, not the source’s meaning or approval. Related reads the same Board
> records in Idea and Story. Story by Section reads the same Story topic in Story
> and Displays. Never copy records to make another View.
> 
> The generic Grant scaffold is implemented by `hai-paper/scripts/paper_ladder.py` and uses the shared Paper
> renderer. Grant-specific section templates, call adapters and the new Job/Task organization remain proposals;
> no canonical live Grant example is bound to s02. Keep these boundaries explicit and do not link a Grant example
> to a manuscript page as though it were a working grant. Every Paper Board, Job
> and Task page shows its type and use case under its title (the shared
> `focus_page.page_identity_html`). The use case is the face's `use-case:` line,
> else the single use its type has in the b16 matrices; a type with several and
> none written shows none, never a guess. The face writes it: `hai-paper`
> scaffolds stamp every new Board, Job and Task face, and `paper_ladder.py update`
> (layout line L6) stamps an older Board's.
> 
> ## Source Idea Job
> 
> For a Paper developed from an Idea Job, read
> [the source adapter](../hai-paper-ideation/ref/idea-job-source.md).
> The source Job owns scientific evaluation and decisions; `s01-ideation/`
> projects the relevant revision and paper-specific framing. Keep the source
> Job/selection links on the topic face so existing readers can follow them.
> `ideation-origin.yaml` records those pointers but does not by itself add a
> renderer or a UI control. A dedicated Idea Board UI remains separate work.
> Legacy Paper-local portfolios keep their current views. Related remains in
> Idea and Story; Story by Section remains in Story and Displays.
> 
> ## 🪜 Classic frame and specialized level contracts
> 
> `servers/workbench-paper/paper_theme.py` exports `THEME`: `spaces(level, folder, root, sub)` returns each Space
> of a level; anything it leaves out is the frame's vanilla Space. `level_patterns` reads both layouts: a
> `jNN_` folder (or an older `Ba-`/`Bb-`/`Bc-` group) is a Job, a `tNN_` folder (or an older `S-…`, `RD<NN>`) a Task.
> 
> | Level › Space | Its third-row views | Reads |
> |---|---|---|
> | Block › Studio › Related (folds under the topics) | one part, folded until a Related link opens it | the frame's own view (`hai-related`): one row per `related/related.md` row, grouped by its subfolder first and then its `group` cell, each opening on its file (a Word file read in place, an email with its headers); files with no row yet, dashed. By question: Report › Related Papers, which leaves out meetings, files and emails and lists a paper under each question in its `group` cell |
> | Block › Description | Scope · Venue · Resources | `board.md`; `venues/*/call.md`; `## Related resources` |
> | Block › Idea Studio | one row per topic | `sNN-<topic>/` (the frame's studio rows) |
> | Block › Audience Report | Ideation · Narrative · High-level logic + Low-level work · Related Questions · Related Papers | `board.md ## Questions` by `group:`, their `reports/qNN_`; the current telling's studio topic; the related papers under the question each bears on (`related/related.md`, else the telling's related-papers table) |
> | Block › Work Details | Idea · Story · DataFlow · PaperFlow · Jobs | the paper's steps before its versions, each Operation (Input, Prompt) over Result (its Studio topic's drawing, then Open and Decided): Idea the Ideation topic (s01), each idea a card; Story the Story topic (s02), as sections with a card per research question; DataFlow and PaperFlow the Plan topics (s03, s04); then the versions |
> | Block › Report (focus page; legacy Work links redirect) | Idea · Story · Data + Paper Plan · Support blocks · Evidence · Displays · Writing | `layout=focus&section=report\|work&group=<key>\|work-<key>`; the views are below (🖥 The focus page) |
> | Block › Runs · Delivery | (Delivery) LaTeX · Word · Cover letter · Rounds | the Board's `runs/`; the newest version's `delivery/jNN_<version>/`; then Sections in the build, every version's Sections from its `build-manifest.json`: ready at the build, in the build or changed after it, a link to each Section's part and its folder |
> | Job › Report (focus page; Work retired, its links redirect) | Structure (first) · Draft-Main · … | Structure: 🧭 The story (§ 8 title, story, claim cards, the version's sign) · 🗺️ The Sections (a closed row per Section: question, moves, claims, figures, paragraph bar, plan sign; opened: its paragraphs and the venue's papers) |
> | Job › Description | Version · Venue rules | the version face; its venue's `call.md` |
> | Job › Audience Report | Questions · Draft-Main · Draft-Appendix · Comments · Cover letter | the face's `## Questions` and the standing J1–J5; each Section as Question │ Work │ Report with its rendered draft beside its drawing; the comments reports' `## Review Items`; the letter by paragraph |
> | Job › Work Details | All · Main · Appendix · Letters | its `t0N_` · `t2N_` · `t3N_` Tasks; the comments reports the letters answer |
> | Job › Runs · Delivery | (Delivery) one card per kind: manuscript · letters · Sections · checks · sent | the version's `runs/`; its part of the Board's delivery, `delivery/jNN_<version>/` |
> | Task › every Space | the Page Task's own views (`servers/workbench/workbench-task-draft`) | the Section folder; the paper adds the reader contract (Scope), its `SUB-*` rows (Requirement), Comments, and "ready for the build" apart from "done" (Delivery) |
> 
> **Markdown is the only truth source (JL 260918).** Every view is drawn from the paper's `.md` files (and
> authored config, `paper-build.toml`; and receipts, `build-manifest.json`, `runtime.yaml`) on each open; a
> Markdown edit is live on reload. The theme stores nothing: no `console/`, no `data.js`.
> 
> **Base styles only (JL 261007).** A view uses the classes the frame gives every theme (`servers/workbench/README.md`):
> the folding `.topic` row, `.q-row`, `wf-table`, `.st-ok` · `.st-warn`, `.topic.missing`. A view still drawn by the
> old page's renderer is wrapped in `pv()`, which scopes that page's stylesheet to it. The reading rules stay: base
> type 16px, never under 12px, every table with cell edges, a closed card shows its whole headline.
> 
> ## 🖥 The focus page: a paper Board's views (`layout=focus`)
> 
> <!-- render b16.j01.t01-s32 board-report-views: generated from Tools examples/Project-Ladder/blueprint/b16_theme_paper/j01_paper_workbench_pages/t01_board_page/s32-board-ui-report/delivery/skill/board-report-views.md; edit it there, then render_delivery.py -->
> ### The focused Paper Board: seven content Views
> 
> The current focused Board uses Report → Review Content → Around the Work.
> Review Content combines each View's content and its existing preparation actions.
> Legacy `section=work&group=work-<key>` Board links open the corresponding Report
> View. The classic frame and specialized Job/Task Report/Work workflows remain
> supported separately; Board behavior does not imply their migration.
> 
> | Key | View | Content sources and Sections |
> |---|---|---|
> | idea | Idea | Ideation topic: Directions and Theory; Related from the Board reference records, even when a Story exists. Direction appears here only before a Story exists. |
> | story | Story | Current Story topic and chosen direction: Direction (its question large, `**Label**:` paragraphs as label rows), Pitch (the one-sentence identity large, then the pitch a sentence a line; the stage only on the bar; `⟦pending …⟧` a muted chip), Theory, Research Questions (the paper's question large, then ONE table, a row per question, every field side by side: RQ | Question | Why we ask | Asked before | New here | Expected (the report link at its end; no State column), the three middle columns from §3's table when it has them; full card width, the paper's question on its left edge; stacked per row on a phone), Related, Venues (each card's first row its editor's test, from §9's `editor's test` column, with an "Open the editor's test" pop-out when the Board has `reports/q*_editor_test_<venue slug without hyphens>*/`; under it "To pass the desk", a numbered list of the first sentence of each item in that report's `**To raise the odds**` list, hidden with no report) and Story by Section (reads § 8 as the shared narrative; left tabs, right content: first the whole paper's Story arc from § 8, then a tab per Section from the newest version's `## Narrative` row, its small line what the reader leaves with; its panel Reader asks, Comes in with, Moves as a numbered list 1, 2, 3, Leaves with, Hands on, Must not say, Displays, then its claims); no Open points section. Prose shares one 92-character measure centred in the card, text left-aligned; a compared table (the Research Questions) takes the card's width. |
> | plan | Data + Paper Plan | Two sections, the skill's Plan (JL 261111, after re-reading hai-paper-plan; Paper-CMS-AI-Usage r03_collect_plan_view_decisions): 1 · 🗄️ Data flow, the s03 topic's Excalidraw drawing (how the data become each answer), and 2 · 📝 Paper flow, the s04 topic's drawing (how each answer becomes the page), as Displays shows s06. Each bar carries a small Prompts button with that flow's plan prompts (Data flow: design the dataset, design the regressions, make them run; Paper flow: plan the displays). Every fact once: no summary on top, no Runs to do (§ 7 shows in the Data flow drawing), no separate Plan prompts; the § 6 reading is the Story view's 📚 Reading. A line that is only a template slot (`<...>`) is not shown. |
> | explore | Support blocks | Internal Work and external Discovery Blocks named by the paper, linked back to their source work. |
> | evidence | Evidence | Returned values and citations from evidence Jobs, with their current state. |
> | displays | Displays | The display plan, display previews (each display's state in its tab), examples, then last Story by Section from the same Story topic, the same section the Story view shows. A tab names its display by the face's `name:`, else the s06 plan's `name`, never the folder's old number; a Task whose face says `number: not printed` is left out (`board_displays.retired`). |
> | draft | Writing | Version sections, assembled documents, portal preparation and sections still to finish. |
> 
> **One source, several entry points.** Related in Idea and Story is the same
> `related/` material. Closest-work positioning is owned by hai-paper-related;
> record storage by hai-related. Story by Section in Story and Displays is the
> same current Story topic's `Section Narrative` (§ 8: title, story, claims; no
> Section rows), owned by hai-paper-story. Its Section rows and per-version
> compile order remain with the writing Job's `## Narrative` and assembly. Neither
> extra UI entry creates another authoring location.
> 
> Views and Sections depend on source content. No ideation topic means no Idea
> View; no Story topic means no Story View. Evidence is registered when a
> non-version Job exists (including submission); its Sections render only the
> sources present. Displays is registered when a display Job or display-plan
> topic exists.
> Related is omitted when no reference items exist. Story by Section is omitted
> when the selected Story has no Section Narrative. Do not invent source content
> to fill a matrix cell.
> 
> Around the Work uses the shared unnumbered order: Studio, Interactions,
> Decisions, Things to Know, Checklist, Timeline, Skills and Files. Supporting
> records belong to a View through explicit `view:` metadata first, then their
> linked Topic. Unassigned records stay available in the aggregate right rail.
> The same selection drives view-scoped Skills and Files. Studio is shown in this
> shared group, not repeated above Idea and Story. Delivery remains a rail entry.
> 
> Section bars start closed. The view buttons stay above the goal. Content and
> supporting sections use the shared components and style rules; no Paper-specific
> copy of the common frame is introduced.
> 
> **Grant is a Paper type.** Its design shares Idea, Story, Data + Paper Plan,
> Related and Story by Section with Paper Board. Funding-call requirements, aims,
> approach, team, budget and submission preparation specialize the content.
> Grant-specific rendering, examples and scaffolding are not implemented merely
> because they appear in the matrix. See the Paper router's ownership table.
> 
> ```text
> servers/workbench/page/job_task_views/work_frame.py          shared sections and view ownership
> servers/workbench/side_pane/rail_sections/skills_section.py      skill catalog and links
> servers/workbench-paper/paper_focus.py   Paper content adapter and scoped sources
>                         board_views.py  View registration and classic wrappers
>                         board_results.py content renderers shared across Views
>                         board_process.py preparation actions and semantic skills
>                         board_read.py   source topics, faces, tables and folders
> ```
> <!-- /render b16.j01.t01-s32 board-report-views -->
> 
> **Skills.** Current focused Boards show Skills once in Around the Work and in the aggregate rail. `board_process.py` `VIEW_SKILLS` supplies the semantic owners; it is not an extra PROCESS step.
> 
> ## ✍️ Writer: the Runs panel
> 
> The theme is a read-only projection. **Its only engagement is the Runs panel** of each Space: the buttons are the
> run cards of `hai-paper-workflow/ref/run-cards.md` whose Space field is that `<Level> › <Space>`, kept for the
> open view (`paper_theme._run_cards(level, space, view)`); a Section's buttons are the Page workflow's cards. As
> every button of the frame, it is named by the Run it makes (the card's `🏷 RUN` line, `run-<type>-<target>`), its
> label in small under it (hai-run `ref/run-types-by-space.md`). A button shows its skill and copies its prompt, `{folder}` filled with the open folder; the person runs it in a
> Claude or Codex session. Clicking never sends, starts, allocates or writes.
> 
> Every Run is `run-<type>-<target>` (no date): a Board's or a version's is a folder in its `runs/` (`run.yaml`, ticket,
> `passes/`, the shared Run contract); a Section's is its Page engine ticket. The run types,
> with each one's agent, skill and sign, are `ref/workbench-table.md`; `table-workbench --check --cards` keeps the
> table and the cards equal.
> 
> ## 🧭 The Guide
> 
> The Guide tab reads `servers/workbench-paper/guide/guide.yaml` (family `paper`): its description, the Workbench
> Table (`ref/workbench-table.md`, this skill's), Method (`guide/method.md`, split by level, its cards in
> `guide/methods/`, its canvas `guide/methods.excalidraw`, the canvas being the source), RoadMap Draw, and Related
> Paper (`servers/workbench-paper/related/papers.md`, `table-papers`).
> 
> ## 🚦 Gates
> 
> The theme shows each gate where it is signed; the named owner closes it, never the screen:
> 
> ```text
> Board    G0 the admitted idea · G1 release of Task work · G2 the claim state and the answer
> version  G3 release of one Section (Draft-Main) · G4 submission readiness (Delivery › checks) ·
>          G5 every response answered (Comments, the t32_response letter)
> ```
> 
> The theme never infers a human approval from a percentage, a folder's existence, a generated PDF or a
> `recorded` row. Gates: `hai-paper-workflow`.
> 
> ## 🚧 Boundary
> 
> The theme coordinates the paper; it never becomes the owner of Page prose, Evidence Results, Discovery records,
> Task configurations or delivery wording, and no view copies an authority record to make a table easier to draw.
> The frame (`servers/workbench/`, `servers/_host/`) belongs to its owner; ask before changing it.
> 
> ## ✅ Completion checks
> 
> - `servers/workbench-paper/tests` and `servers/_host/tests` pass; every paper Board renders at every level.
> - Every button of every level's Space is a run card; `render_workbench_table.py ref/workbench-table.md --check
>   --cards ../hai-paper-workflow/ref/run-cards.md` says PASS.
> - No view writes, and none reads a `console/`, `data.js` or other per-paper projection.
> 
> ## 🗂 Topics
> 
> This theme's topics (a problem, a missing step or a rule that was unclear, each with its state and the guard that
> keeps it fixed) are kept in [`ref/topics.md`](ref/topics.md); a new one is added there before it is worked (the
> repository's AGENTS.md § Report). The paper's writing lab (`hai-paper/scripts/open_writing_lab.py`,
> `ref/writing-lab.md`) reports here too.

### plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/CONSTITUTION.md

> # workbench-paper · Constitution
> 
> JL's feedback on the paper workbench, kept verbatim. It wins over SKILL.md; where they disagree, follow this file. The shared `hai-ui/CONSTITUTION.md` applies to every Paper view.
> 
> 
> ## A01 · Every Delivery item names its artifact
> 
> > "could you udpaet the name? … call it Paper-Latex, and Paper-Latex-Diff, you need to udpate it to the skills, using /haistack for it." (JL 261121, chat, with screenshots of the Paper Board's Delivery › LaTeX list showing "The paper" and "Changes since the last round")
> 
> **Rule:** Every item in the paper panel's Delivery lists is named by its artifact, as a hyphenated Kind-Lane[-Variant] name (Paper-Latex, Paper-Latex-Diff, Paper-Word), and the name shown in the list is the item's full name.
> **Why:** The list showed "The paper" under both LaTeX and Word and "Changes since the last round" for the diff, so a reader could not tell the LaTeX PDF from the Word file, nor name the diff to a co-author.
> **Class:** a delivered artifact shown under a generic description instead of its own name.
> **Cases:** ✅ Paper-Latex · ✅ Paper-Latex-Diff · ✅ Paper-Word · ✅ Paper-Word-Tracked · ✅ Supplement-Latex · ✅ Supplement-Word · ✅ Combined-Latex · ✅ Cover-Letter · ✅ Portal · ✅ hai-paper-assemble `ref/latex-diff.md` (names the diff item)
> **Check:** `TAB_GROUPS` in `servers/workbench-paper/board_writing.py` holds only artifact names whose shown name equals the full name, includes Paper-Latex and Paper-Latex-Diff, and no old generic name is written.
> **Run:** `python3 -m pytest -q plugins/haipipe-toolkit/servers/workbench-paper/tests/test_delivery_item_names.py`
> **Status:** solved 261121
> **Solved by:** `servers/workbench-paper/board_writing.py`: TAB_GROUPS and item names renamed
> **Report:** constitution/A01-delivery-item-names.md
> 
> 
> ## A02 · Keep the source Idea Job when it becomes a Paper
> 
> > “I’m thinking about to make the idea to be one specific block them self. And one idea will be a job and then in the task, they are a series of skills to evaluate it and check it. Do you get what I mean? I hope each idea will be developed to one paper later. What is your thoughts”
> 
> Recorded 2026-11-24.
> 
> **Rule:** A Paper developed from an Idea Job links to that source and the
> reviewed human decision. The Idea view projects the source; it does not
> create a second scientific Card or move the Job into Paper. Existing Paper Jobs retain their stored version/evidence/submission identities until a scoped migration; the named target design in A03 governs new structure proposals. Existing Paper-local portfolios
> remain readable until a scoped migration is requested.
> 
> **Contract:** [Idea Job source adapter](../hai-paper-ideation/ref/idea-job-source.md).
> **Guard:** Ideation `tests/test_idea_job_selection.py` checks selected Paper
> destinations and exact semantic revisions. Normal Markdown source links on
> the topic face are the existing reader route.
> **Still owed:** a dedicated Idea Board renderer and live-page verification of
> any future origin-file controls. The plugin-content update does not implement
> those controls or claim this UI case fixed.
> 
> 
> ## A03 · Block structure names its work and distinguishes types from names
> 
> > “第一个 drop group 是 story 啊，第二个是那个 evidence 啊，这个应该写这个呀。”
> 
> Recorded 2026-11-27. The complete correction and the relayed execution authorization are in `ref/topics.md` T07.
> 
> **Rule:** A type-specific structure Studio names that Block’s actual groups and meaningful work. For Paper and Grant the Job groups are Story, Evidence, Display, Writing and Presentation. Show Job Type, Job Name, Task Type and Task Name separately, and show how they relate. Grouping is not a type; a version, role or use case does not create a new type by itself. The shared framework supplies the hierarchy, not numbered placeholder content.
> 
> Idea has candidate Jobs and registered `ideation` assessment Tasks. Paper/Grant default to shared Story and Evidence; Main/Appendix/Explore are Display roles; Review and Submission stay within Writing. Missing or conflicting contracts must be identified from owners and files, never silently registered by a drawing. Structure and Draw agree. Skills is a view of the same Studio, and example labels use their real source names.
> 
> **Guard:** `examples/Project-Ladder/blueprint/b16_theme_paper/delivery/page-spec/check_block_structures.py` checks the named organization, distinct fields, drawing labels, local source bindings and four-view declaration.
> **Scope:** Structure design and its displayed sources. Type registration, research-record migration, and missing live Idea/Grant examples remain separate work.
> 
> 
> ## A04 · Organization is a connected mind map
> 
> > “不是，我意思是做一个mind map一样的炊，你懂吗。”
> 
> Recorded 2026-11-27; verified human message in the Work session, relayed to the theme owners.
> 
> **Rule:** The primary organization in Structure and Draw is one left-to-right branching map: Job Type → Job Name → Task Type → Task Name. Each parent appears once within its branch and connects to its children. A Job without mapped Tasks ends at Job Name. Group labels remain metadata; neither a four-column table nor four cascading selectors replaces the map. Keep the named content and explicit contract gaps required by A03. The same map content appears in both views.
> 
> **Implementation:** b16 `delivery/page-spec/build_organization_maps.py` passes each Studio's `structure/organization.json` to Work's shared `organization_document` renderer. Existing Excalidraw group overviews and human marks remain intact; the authored Studio manifest selects the connected map first.
> **Guard:** b16 `delivery/page-spec/check_block_structures.py` checks four-level parentage, unique siblings, actual node/edge counts, sources, generated content and identical Structure/Draw bindings.
> **Scope:** Presentation of the named design; it does not register execution types or migrate research folders.

### plugins/haipipe-toolkit/skills/3_theme/paper/workbench-paper/ref/topics.md

> # Paper topics
> 
> The Paper theme's topics, one section each (the repository's AGENTS.md § Report). A topic is the one thing
> behind a message or a Report, not the case it showed up in. `fixed` means the case that raised it passes and
> something keeps it passing (the guard); `open` names the work still owed.
> 
> ```text
> T01  an older writing Job hides board.md's session prefix      open
> T02  the lab opens windows with no terminals                    open
> T03  the lab opens no pages when settings.env names no origin   open
> T04  a resumed Section session never gets its first turn        open
> T05  Idea Jobs retain their identity through Paper handoff       open
> T06  Paper and Idea Jobs share Work's navigation and Main        open
> T07  Block structures name their groups, types and work          open
> T08  Organization uses a connected four-level mind map          fixed
> ```
> 
> P below is `skills/3_theme/paper/hai-paper`.
> 
> ## T06 · Paper and Idea Jobs share Work's navigation and Main · open
> 
> The six-type proposal below is historical. T07 records the later named group/type separation and Review/Submission placement; its structure design takes precedence.
> 
> - **From:** user, 2026-11-26: “那你知道你该去怎么去设计吗？然后你能不能比如说做一个 plan，然后设计一下这些东西呢？然后跟其他的保持一致，尤其是跟这个 work block 里面内容，就是说保持一致吧。你明白我意思吗？”
> - **Approval:** “OK，好，那你执行吧。然后执行完了给我讲。” The preceding reply listed nine design/preview files; production reader changes were a later phase.
> - **Questions:** Which navigation and Main parts must remain shared? Which
>   content varies across the six Paper Job types? How does Grant specialize
>   writing without another Job hierarchy? How does Idea keep its own assessments?
>   How are Task workflow controls preserved when embedded?
> - **Observed cause:** `servers/workbench/page/job_task_views/focus_jobs.py:126`
>   `job_pane` takes `ctx.body` without its view bar. Paper evidence/submission
>   default to MindMap. `servers/workbench-paper/paper_jobs.py:43` registers five
>   labels but no Review Job; `board_read.is_version` correctly excludes review.
>   The current matrix therefore omits a type the comments contract already owns.
> - **Design:** Work's Job topic → Job → Main / Task topic → Task; Main uses
>   Overview, Tasks and populated Findings. Manuscript/Grant share six types;
>   Idea adds its candidate Job type. The Overview merge follows b17's eventual
>   shared decision. Skills remain methods inside assessment Tasks.
> - **Delivered:** b16 `s13-paper-job-preview/` has live Paper views plus the Paper/Grant
>   proposal. `s11-idea-job-preview/` has the Idea proposal. The proposed content
>   map and implementation/acceptance plan are in `delivery/page-spec/job-ui-design.md`.
> - **Guard:** `hai-ui/scripts/ui_preview_check.py` checks the Paper entry's
>   live links and quick-view path. Preview interactions are reviewed in the
>   browser. These checks guard the design entry, not the unimplemented Main.
> - **Still owed:** actual Main/Task composition, Review dispatch, canonical
>   Grant/Idea examples, updated current matrix and renderer regression cases.
>   Idea's missing live view is an expected open A08 finding. With quick views
>   alone, the current Studio reader wraps its entry under Page; the entry names
>   Effect explicitly. Do not manufacture a live Idea address or claim this fixed.
> - **Rerun:** reload b16 Studio → Levels to review the files. No reader code is
>   changed and no host restart is required for this design-file delivery.
> 
> ## T05 · Idea Jobs retain their identity through Paper handoff · open
> 
> - **From:** user, 2026-11-24: “I’m thinking about to make the idea to be one specific block them self. And one idea will be a job and then in the task, they are a series of skills to evaluate it and check it. Do you get what I mean? I hope each idea will be developed to one paper later. What is your thoughts”
> - **Implementation request:** “After make the plan and then do the implementation to update the content in the plugin”
> - **Questions:** Who owns a candidate before Paper exists? What does a Task
>   evaluate? How does selection link the Idea Job to Paper without losing its
>   history? Which parts already have a workbench reader?
> - **Content change:** Ideation owns a direction Block, one Idea Job per Card,
>   evaluation Tasks and shared soft assessment Runs. Paper owns the linked
>   manuscript and a projection of the selected source. The source adapter is
>   `hai-paper-ideation/ref/idea-job-source.md`; the owning rule is A01 in
>   this skill's Constitution. Legacy Task portfolios remain readable.
> - **Guard:** Ideation's Block checker and new ownership/selection regression
>   cases cover one-Card Jobs, destination joins, exact revisions and selection
>   without a pre-existing Paper. They do not certify a new UI.
> - **Fresh-context findings addressed:** registered an authored Ideation Task
>   type, allowed an honestly empty opportunity map with explicit gaps, and
>   taught the shared structure audits the Ideation family's folders. The
>   independent fixture retains two ideas and one soft assessment commission;
>   no scientific evidence or human selection was invented.
> - **Still owed:** dedicated Idea Board rendering and a real-page check of any
>   origin-file controls. Existing faces can carry ordinary source links. Keep
>   the UI topic open until implemented and verified.
> 
> ## T01 · An older writing Job hides board.md's session prefix · open
> 
> - **From**: Report, drfirst-space-2f, 261116, on `/hai-lab examples-4-learning/Project-ExpLearn-SMSDesign/paper/
>   Paper-TestToLearn-MS2026`: "`/hai-lab <paper>` stopped with 'pass --prefix <Short>: …'. board.md already has
>   `session-prefix: TestToLearn`, and no other paper uses it."
> - **What happened**: `P/scripts/create_section_sessions.py` `board_prefix()` (line 77) takes the newest writing
>   Job face's `session-prefix:`; with none there and more than one writing Job it returns "" and ignores board.md.
>   The paper has j11 (v0429) and j12 (v1007), two versions of one manuscript, neither face naming a prefix. The same
>   refusal text is in `open_writing_lab.py:271` and `create_section_sessions.py:481`.
> - **Why the rule is there**: JL 261114, two writing Jobs in flight at once (a letter and a full proposal) must not
>   share sessions. An older version of the same manuscript is not in flight, so the rule over-fires here.
> - **Questions**: does board.md's prefix count when no other writing Job face already claims it (which keeps the
>   261114 case safe)? Should the refusal name board.md's prefix as the value to pass?
> - **Still owed**: the rule change in `board_prefix()`, `ref/writing-lab.md` § the session prefix, a test with two
>   writing Jobs (one older, no face prefix) and one with two Jobs where the other face already holds board.md's.
> 
> ## T02 · The lab opens windows with no terminals · open
> 
> - **From**: the same Report: "the lab opened both windows with no terminals and mentioned the missing extension
>   only in the last lines of its output. Once `code --install-extension` ran, the windows that were already open
>   loaded the extension … and started all 8 sessions right away, without being reopened."
> - **What happened**: `P/scripts/open_writing_lab.py` `main()` checks `extension_installed()` (line 205) only after
>   the workspaces and prompts are written, prints a notice and opens the windows anyway (line 333).
>   `P/ref/writing-lab.md:85` says a newly installed version runs only in a window opened after the install, which
>   holds for an upgrade but not a first install (`activationEvents: onStartupFinished`).
> - **Questions**: should the plan (no `--apply`) name the missing extension? Should `--apply` stop before opening
>   windows without it (the install is the person's step, never an agent's, `ref/writing-lab.md` § The extension)?
> - **Passed on**: the Block lab prints the same late notice (`skills/1_base/workbench/hai-lab/cli/lab.py:262`); that is
>   the shared workbench's, not this theme's.
> - **Still owed**: the check moved into the plan, the stop on `--apply`, the doc line split into first install and
>   upgrade, a test that `--apply` opens nothing without the extension.
> 
> ## T03 · The lab opens no pages when settings.env names no origin · open
> 
> - **From**: the same Report: "every unit's `url` in haipipeLab.terminals was None, so no page opened above any
>   terminal, and the lab printed nothing about it. The SPACE's server was running at 127.0.0.1:5603."
> - **What happened**: `P/scripts/open_writing_lab.py` `board_origin()` and `page_url()` (lines 138 to 159) read only
>   `PUBLIC_URL` or `DOMAIN` from `.server_config/settings.env` and return None silently. `wb.py` writes only `PORT`
>   there on first start and builds its own links from `http://127.0.0.1:<port>`
>   (`skills/1_base/workbench/hai-workbench/cli/wb.py:256`). The sender fixed their machine with `DOMAIN=127.0.0.1`.
> - **Also found**: `board_origin()` strips a `JJLUO_` key prefix and its docstring names it, against the
>   repository's AGENTS.md § Keep it general.
> - **Questions**: may the lab fall back to the loopback origin, since the lab runs on the same machine as its
>   reader (`skills/1_base/draft/hai-draft/fn/serve-host.md:133` allows a loopback DOMAIN for the person at this
>   machine), or must it warn and stop? Should `wb.py` write `DOMAIN` beside `PORT`?
> - **Passed on**: `wb.py` writing `DOMAIN` is the shared workbench's.
> - **Still owed**: the decision above; the plan line naming a missing origin; the deployment prefix dropped; a test.
> 
> ## T04 · A resumed Section session never gets its first turn · open
> 
> - **From**: the same Report: "all 7 Section sessions resumed and then sat idle. The first turn in their
>   prompts/<unit>.txt (a read-only look, then the review round) was never sent."
> - **What happened**: `P/scripts/lab_launch.py:45` runs `claude --resume <sid>` without the prompt, while
>   `P/ref/writing-lab.md:54` says every unit's first turn includes the default review round, skipped only when the
>   newest Draft was already reviewed at its version.
> - **Questions**: should a resume send the prompt when the Section's newest Draft has not been reviewed at its
>   version, or should the doc say a resumed session gets no turn? Can a resumed turn re-run a review a person
>   already answered?
> - **Still owed**: the decision, the change in `lab_launch.py` (or the doc), a test.
> 
> 
> ## T07 · Block structures name their groups, types and work · open
> 
> - **From:** user, 2026-11-27: “你这里面不能用index了，哎呀我操，这个就是你是具体的paper，你的paper你的block，你还有一二三四吗？你应该就是有具体的名字了呀。 就是你不要再用那个 drop 1、drop 2、drop 3 了，你应该是找 Q的 example。你比如说我刚才讨论的那什么，第一个 drop group 是 story 啊，第二个是那个 evidence 啊，这个应该写这个呀。”
> - **Verified follow-up:** the user in Work thread `01a21d6c-cdee-7580-aeda-b1852ffb4a14` required Job Type / Job Name / Task Type / Task Name, then said “给每一个session都去发个message，让他们就是重新再去更新一下他们的plan，然后去执行。”
> - **Questions:** Which named groups belong to Idea, Grant and Paper? Which names denote types versus work instances? Which type definitions actually exist? Do Structure and Draw show the same relations through the shared renderer?
> - **Cause:** the previous staged Paper builder displayed generic numbered Job/Task branches, while its five named groups appeared only in secondary prose. The same generalization obscured Idea and Grant. The corrected builders and structure/jobs.md now name the work directly.
> - **Design:** Idea → candidate Jobs → ideation assessment Tasks. Paper/Grant → Story, Evidence, Display, Writing, Presentation; Review/Submission stay inside Writing. Display roles and versions do not become arbitrary new types. The current reader’s inferred Job kinds and exact Task fields are documented separately from proposed contracts.
> - **Contract findings:** `servers/workbench-paper/paper_jobs.py:27` infers legacy Job kinds; value faces use an unregistered `value` Task key; citation faces use `evidence` but the base owner describes numeric extraction. The final Paper asset is not the upstream `display` input Task. Story, consolidated Evidence and media contracts require definition before migration.
> - **Delivered:** s01 Idea, s02 Grant and s03 Paper structure packages, authored shared-view manifests and named organization sources. Old s01–s03 are preserved in `_archive/20261127/` with historical references retained.
> - **Verified:** the running b16 page opens all three named Structure sources and editable Draw canvases. Paper Skills loads its owning skill; Paper Examples embeds the actual Paper-Example. Idea and Grant omit the unbound Examples view. Fresh-context review also corrected the skill entry, installed-view wording, and the distinction between the existing generic Grant scaffold and proposed Grant adapters.
> - **Guard:** `delivery/page-spec/check_block_structures.py` in b16; A03 in this skill. Browser acceptance and results are recorded in `trace/261127/1049_named_block_structures.md`.
> - **Still owed:** resolved runtime type contracts, a scoped migration of Paper-Example and real Idea/Grant example bindings. Empty Examples entries are omitted by the shared reader; no fabricated live routes are supplied. The broader topic stays open until those contracts and examples are implemented and checked.
> - **Rerun:** reload b16 → Studio → Structure. Shared server code is unchanged; no restart is required for these authored files.
> 
> ## T08 · Organization uses a connected four-level mind map · fixed
> 
> - **From:** user, 2026-11-27, verified in Work thread `01a21d6c-cdee-7580-aeda-b1852ffb4a14`: “不是，我意思是做一个mind map一样的炊，你懂吗。” Work relayed the clarification under the earlier instruction to notify the theme sessions, revise plans and execute.
> - **Questions:** Does the map show Job Type → Job Name → Task Type → Task Name as connected parent/child branches? Is each parent drawn once? Are concrete names, missing contracts and Job-only branches retained? Do Structure and Draw use the same source?
> - **Cause:** the previous `structure/jobs.md` sources led with reference tables; the Excalidraw overviews combined several Job names in one text node and emphasized groups. Naming the fields did not yet draw individual type/name branches.
> - **Change:** three `structure/organization.json` trees feed `delivery/page-spec/build_organization_maps.py`, which imports Work's `organization_document` with the complete tree and source paths. Structure and Draw both select the same generated `jobs.html`; the existing canvases remain as Overview. Contract evidence stays in reference documents linked from nodes. The four levels are semantic organization, not storage directories.
> - **Guard:** A04 and `check_block_structures.py`: four levels, unique siblings, parent-child edges, shared renderer output, source existence, real names and common Structure/Draw binding. The existing runtime type gaps remain T07.
> - **Verification:** all three Structure and Draw views loaded the same connected maps through the running Workbench. Paper's Fit to width and Actual size controls worked; direct map and final shared-layout reload were inspected. Fresh-context skill validation passed semantic ownership, source bindings and Job-only branches. The generated outputs were rebuilt after the shared renderer's final update; the guard passed with no problems. Evidence is recorded in `trace/261127/1111_branching_block_maps.md`. T07 remains open for runtime contracts and record migration.

