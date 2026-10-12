## 1.19.2 · 2026-10-12 · Pick topics in the chart, read them under it; no counts in the header

- JL 261011: "Or we can select the topics we are interest in we show there content". In the Timeline's Days
  chart a click on a topic's column (its sNN) or bubble picks it: picked bubbles turn blue, the rest fade,
  and the picked topics' decisions, sessions and notes show under the chart on the same axis ("Reading … ·
  Clear"). The topic's name in that list opens its row above. Picks live in the page only.
- JL 261011, on the header "129 decided · 15 sessions · 105 drawing notes · since 2026-10-06 · 174 shown in
  Structure": "I don't need this, we can delete this part as well". The summary now says only Timeline;
  its count line and the script that kept it are gone.
- b10 s08-D08 and s08-D09 recorded; the drawing shows both with green notes.

## 1.19.1 · 2026-10-11 · A theme's Report: the owner, and its own cards

- For the paper (b16 s05-D01): `Theme.report_fixed(row, owner)` gets the folder whose register is read, so a
  paper's fixed group can come from its telling's **Feeds:**; a one-argument `report_fixed(row)` still works
  (`_theme_fixed`). The group op uses the same rule, so a drag refuses to take a fixed group out.
- `Theme.report_cards(level, folder, root)` -> [{id, title, groups, status, html}]: a theme's own cards that
  are no register row (a paper's ideas, its standing Questions), drawn first under the same bar, not
  draggable, their groups fixed and counted; an op on one is refused (no register line).
- b10 s07-D09.

## 1.19.0 · 2026-10-11 · The Report's groups are tags, as the Studio's

- JL 261011: "if the report card to show, it will be the same as the sNN, we can create and add the tags";
  "for someother report, the groups are of the special forms, and that ones are fixed, depending on different
  theme". `frame.report_view`: the vanilla Report is one folding card per Question under the Studio's group
  bar (`group_list(kind="reports")`: Current · groups · Untagged · + Group); opened, its Logic │ Work │ Report
  row. The paper Board's four buttons (`AUDIENCE_VIEWS`) are no longer drawn on every theme.
- A Question's groups are its register `group:` line; a drag writes it (`_register_set_groups`, that line
  only); `reports/_groups.txt` keeps the order, then a theme's starting groups, then the Studio's order.
- `Theme.report_fixed(row)` and `Theme.report_groups`: a theme's fixed groups (no ×, `data-studio-fixed`,
  a remove refused) and its starting ones. The chips keep no × on a fixed group after a drag (Related's
  subfolder groups too). A `#question-QNN` link opens its card.
- b10 s07-D01, D02, D09.

## 1.18.1 · 2026-10-11 · The chart's columns can be the topic groups

- JL 261011: "I think here the columns can also be the topic groups". `frame.studio_timeline`: the Days
  chart has a second set of columns, one per topic group in the group bar's order (`studio_group_order`,
  then other tags, Untagged last), switched by "columns: by group · by topic" (by group when any topic has
  a group; the browser keeps the pick, `workbench.timeline.cols.v1`). A group's cell carries its topics'
  counts (`data-tl-parts`), so the page script re-adds it from the topics the group bar still shows; a
  topic in two groups counts in both, the day's bar counts each change once. A group's column or bubble
  picks that group in the bar and switches to its topics. `timeline_events` now gives each event its
  topic's `tags`.
- b10 s08-D07 recorded; its screen frame draws the group columns, with a green note.

## 1.18.0 · 2026-10-11 · The Timeline's Days is a chart

- JL 261011, on the Topics list: "it is not that beautiful, how could we have better version? like using
  the versualiaation tools?". `frame.studio_timeline`: Days is now a chart down the same axis, a row per
  day, a column per topic (its sNN on top), a bubble sized by how much that topic moved that day (area by
  the square root), and the day's total as a bar. Topics is a line per topic, `sNN` and its name, a
  stacked bar of decided · session · note and its count; Everything adds each item with a coloured
  mark, one line each. Plain HTML and CSS in the page, no chart library: it takes the frame's light and
  dark colours, and the group bar hides columns and recounts the bars (`timeline()` in the page script).
- b10 s08-studio-timeline: s08-D05 recorded, its screen frame redrawn as the chart.
- Test updated: `test_studio_timeline_reads_dated_decisions_sessions_and_change_notes`.

## 1.17.0 · 2026-10-11 · The Timeline runs down one axis, at three levels

- JL 261011: "I want it to be a real timelne, and make it very concise ... Like the timeline with a axis
  down", "it should also be up to done [down]", "we can show different level of details", "We should
  create a new sNN for it, and show the UI". `servers/workbench/frame.py` `studio_timeline`: an `<ol
  class=tl-axis>` with a dot per day on one line down the page and an arrowhead at the end, the oldest day
  at the top. Three levels, buttons Days · Topics · Everything (`data-level` on the axis, CSS shows the
  parts): Days, each day's topics as sNN chips and its count; Topics, a line per topic with how many
  decided, sessions and notes; Everything, each item. The page script keeps the level in localStorage
  (`workbench.timeline.level.v1`), recounts each day when the group bar hides topics, and a chip opens
  its topic like a name does.
- Its topic: Tools/blueprints/b10_project_workbench/studio/s08-studio-timeline/ (s08-D01 to D04), whose
  builder draws the UI from `frame.timeline_events`.
- Test: `test_studio_timeline_reads_dated_decisions_sessions_and_change_notes`, updated for the axis.

## 1.16.1 · 2026-10-11 · One host per SPACE

- JL 261011: "when we use the /wb we will just start from the SPACE, and then we pickup the board".
  SKILL.md now says it outright: every /wb link goes through the one host rooted at the SPACE, a
  board is a path inside it, and no host is ever rooted at a Project or board folder. A Tools
  blueprint Block opens on the Tools SPACE host. `cli/wb.py` already worked this way; no code change.

## 1.16.0 · 2026-10-11 · The Studio gets a Timeline

- JL 261011: "for the layout of the studio, I think we can also add another section of the Timeline".
  `servers/workbench/frame.py`: Timeline is the Studio's third folding part, under Related, on every
  Block, Job and Task view and in every theme: one block per day, newest first, one line per topic that
  moved that day. It writes nothing; it reads each topic's decisions by the first date in them (b10 has
  110 dated, 13 undated), its sessions (`runs/run-draw-<sNN>/passes/pNN-<MMDD>/`) and the green `✎` change
  notes in its drawings, read once per file version (`timeline_events`, `studio_timeline`, `_decisions`,
  `_drawing_notes`, `_session_day`).
- It follows the group bar: the page script's `apply()` hides a topic's lines when its row is hidden,
  and the summary says how many show in the picked group; a topic's name opens its row.
- Not lifted from the cowork theme's `timeline_view.py`: that one draws an authored Date | Track |
  Development table of one report, oldest first, as cards; the Studio's reads the topics and needs one
  dense line per topic.
- Test: `test_studio_timeline_reads_dated_decisions_sessions_and_change_notes`.

## 1.15.1 · 2026-10-11 · Related's groups work like the Studio's

- JL 261011, relayed by the b02_aid_ai session: "for the group in the related, I want it to be things like
  this: 🎯Current 0 / Untagged 4 / + Group — for the studio". `servers/workbench/frame.py`: Related (folded
  in the Studio, every Block, every theme) now sits under the Studio's group bar, not one heading per
  `related/` subfolder. A group is a name in the row's `group` cell of `related/related.md`
  (comma-separated; the column is added the first time a row gets a group), `related/_groups.txt` keeps
  the button order, Current stays in the browser. A file no row names yet shows under Untagged ("no row
  yet"); dragging it onto a group adds its row.
- One copy of the code: `group_list()` draws the bar for both (`studio_cards()` calls it), `_group_parts()`
  gives a row its ⋮⋮, Add to Current and chips, and `studio_group_op()` takes `kind: related`
  (`_group_members()`, `related_items()`, `_related_set_groups()`). The page script reads
  `data-group-kind` / `data-group-noun`; Related's link keeps its own `related_tag` / `related_group`.

## 1.15.0 · 2026-10-11 · /wb opens a Block, Job or Task on its Studio

- JL 261011: "make the studio to be opened as the default". `cli/wb.py` `target()` adds `studio=1`
  to a Block, Job or Task link, so the frame opens on the Block's shared Studio topics; the new
  `--no-studio` opens the level view as before. SPACE Home and Project links are unchanged.

## 1.14.1 · 2026-10-09 · Audience Report: the paper Board's four views on every level

- JL 261009: "why the Audience Report, there are not sub buttons, it is not correct", then, over the paper Board's
  Audience Report: "I want you to follow things like this". `servers/workbench/frame.py`: on a level no theme draws
  itself (every Tools blueprint Block b01 … b17), Audience Report's third row is the paper Board's four views,
  always there: Ideation (the studio topics on ideas) · Narrative (the studio topics telling the level's story) ·
  High-level logic + Low-level work (the register's Questions, Logic │ Work │ Report, the open view) · Related
  Questions (the Questions others ask: register group reviewer · coauthor · editor · reader). An empty view says what
  belongs there (b03 s01-D22). Before, the row came only from register groups, and no blueprint Block had one, so
  none showed a third row. `question_rows(…, keep=)` picks a view's rows; with groups, a heading per group (b10 s02-D25).
- `frame.py` `studio_sessions()`: the Idea Studio's Runs panel shows each run-draw Run's own status from its
  run.yaml (it wrote "done" for every one; recorded first in workbench-studio 0.6.1).

## 1.14.0 · 2026-10-09 · /wb opens a workbench (JL 261009)

- `/wb` is this skill's short name (`metadata.aliases: [wb]`; `install.sh` and `install.ps1` link
  every alias as one more name for the same folder). JL 261009: "/wb is the same to the /workbench".
- New first section, Open: no input opens the SPACE Home, a Project path opens that Project
  (`/?project=`, new in `servers/space-home/home.py`), a Block, Job or Task path opens the shared
  frame in its theme, and plain words find the place first. JL 261009: "can we with the natural
  language and to find them as well".
- New `cli/wb.py`: finds this SPACE's running host (starts one when none runs, restarts one that
  drops the request), checks the link before printing it, ranks places by words with the server's
  own lists, and names the theme skill to load next.

## 1.13.1 · 2026-10-07 · How to draw a workbench design

- Surface points to excalidraw-report 0.7.0, "Designing a workbench: screens with what is on
  disk" (JL 261007: "I think the s02 excalidraw is brilliant"): a full screen per level, the
  backing files under each, the pop-outs, starting from today's served workbench.

## 1.13.0 · 2026-10-07 · Renamed from haipipe-workbench (JL 261007)

- The skill is `workbench` (was `haipipe-workbench`), its folder `page/workbench/`, its trigger `/workbench`; every live reference in Tools follows. Older entries below keep the old name.

## 1.12.5 · 2026-10-03 · a new served workbench follows the shared rules

- Points to the checklist in `servers/README.md` § Adding a workbench and to the conformance test `servers/_host/tests/test_workbench_conformance.py` (JL 261003: "make sure other new workbench UI will do the same thing").

## 1.12.4 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.

## 1.12.3 · 2026-09-28

- Docs: the Page workbench is three Spaces (Draft, Evidence, Delivery) with a Runs panel each,
  over `draft/`; Run Space is the All-runs view (`lens=run`). Found stale by a fresh-agent field test.

## 1.12.2 · 2026-09-22

- Docs: `rp-struct-NN` is Structure + Outline Bullets, no Mermaid.

## 1.12.1 · 2026-09-22

- The served Page tab reads 📃 Page, not 🧭 Outline; roster and family table say so.

## 1.12.0 · 2026-09-22

- Renamed with the vocabulary: `plugin` now means only a Claude Code plugin
  (`plugins/haipipe-toolkit`), a **lane** is a folder on disk, a **workbench** is
  a served tab and its contract. This skill was `haipipe-plugin`; it pairs by name with
  `servers/workbench-<x>`.
- It is the base every workbench skill loads. The generic Page workbench skills sit flat
  beside it (`haipipe-workbench-page`, `haipipe-workbench-studio`); `page-plugins/` and
  `board-plugins/` are gone; every other workbench skill lives in its owning family
  (design, insight, paper, labeling).

## 1.11.0 · 2026-09-21

- The generic Page Workbench skills are exactly two, pairing by name with the
  served workbenches: `haipipe-workbench-page` ↔ `servers/workbench-page` and
  `haipipe-workbench-studio` ↔ `servers/workbench-studio`. Runs, Folder, and
  Delivery are lane references inside `haipipe-workbench-page/ref/`; the tab bar
  table, the roster prose, and the pairing rule say so.
- `ref/roster.md`: the document writers are `servers/workbench-page/exporters/`.
- 1.10.2 (same day): workbench/workbench pairing note for the `servers/` move.

## 1.10.1 · 2026-09-20

- Align the shared roster with read-only Draft prompt copying, current Result authority, Run ownership, and Design readiness; mark retired lanes and Adopt records as history.

## 1.10.0 · 2026-09-15

- `ref/roster.md` `results/` row: the Draft Space note composer is named as the
  one browser writer, appending pending-Step `#### Feedback` items to the owning
  RP journal.

## 1.9.0 · 2026-09-14

- Replace compact Page Run examples with typed RP/RE identities and document
  `DISPLAY` labels such as `\\figure{D_xxx}`, `\\table{D_xxx}`, and citations
  as `\\cite{C_xxx}`.

## 1.7.0 · 2026-09-13

- Define Workbench Outline as the single three-workspace surface: Bullet,
  Evidence, and Run.
- Remove top-level Runs presentation while retaining the internal compatibility
  route and external Supporting Run references.

## 1.6.0 · 2026-09-12

- Reserve Page Run `rp00` for Mermaid Structure and start paragraph Page Runs
  at `rp01`.

## 1.5.0 · 2026-09-12

- Define the Page lane with `rpNN` Run-of-Page identities and remove the
  second active interactive-writing namespace.
- Keep Page Run and owner-native Task Run storage visibly separate.

## 1.4.1 · 2026-09-12

- Align the base Workbench contract with the Page-owned Run namespace: begin at
  `pr01_mermaid-structure`, continue with `prNN_pNN[-pNN]`, and retain old
  `rpNN_*` records only as readable migration input.

## 1.2.0 · 2026-09-12

- Make the category-workbench surface contract host-neutral across standalone and
  Board Pages. A host advertises only real capabilities in canonical order;
  unavailable Studio is omitted rather than represented by a dead control.

## 1.1.0 · 2026-09-11

- Protect interactive Writing Results as irreplaceable human-feedback history, not a regenerable cache.

## 0.8.0 · 2026-09-03

- Make Skills an explicit Outline-owned storage lane at `outline/skill/`.
- Reserve sibling `skill/` for read-only migration compatibility and keep the
  sole Skills surface inside Outline → Page Records.

## 0.7.0 · 2026-09-03

- Define Page Records as Files + Log + Skills.
- Keep the ranked Skills store in `skill/` but present it inside Outline,
  removing the duplicate top-level Skill picker row.

## 0.6.0 · 2026-09-03

- Name Outline's two primary surfaces Bullet Workspace and Evidence Workspace;
  group Requirement/Discussion/Feedback as Plan Context and Files/Log as Page
  Records.
- Make nested category addresses the current storage contract: evidence lanes
  live under `outline/evidence/`, and outgoing artifacts under
  `delivery/<lane>/`; flat names are compatibility reads only.

## 0.5.1 · 2026-09-03

- Make the source-backed Board Page picker contract explicit: Runs stays
  visible with a truthful empty state, while Evidence and Probe have no
  top-level tabs.
- Remove the retired `workflow/` category from the unit-folder description.

## 0.4.3 · 2026-09-03

- Make an active Workbench tab's close control a separate 36×36 touch target,
  and isolate its gesture from tab activation.
- Keep closed default tabs closed, skip stale entries when choosing the next
  tab, and align the contract with the intentionally absent pane-level close.
- Replace the retired explicit-`＋` opening rule with the direct first-visit
  category strip and Workbench-picker reopen rule used by the live shell.

## 0.4.0 · 2026-09-02

- Separate rostered storage lanes from Workbench identity: a category Workbench may
  own several internal lanes without minting one Skill per subfolder.
- Record the unified Evidence ownership of Citation/Bib, Value, Display, and
  PageX; Probe remains the separately governed crossing shown in the same tab.

## 0.3.8 · 2026-09-02
- Treat category Workbenches as possible direct owners of an internal lane.
- `haipipe-workbench-evidence` now owns Citations/Bib at `evidence/bibex/`; a
  storage lane no longer implies a duplicate Bibex Workbench Skill.

## 0.3.7 · 2026-09-01
- Make the Runs presenter overview-first: Execution, Discovery, and Page rows
  each join their authored Ticket to the paired Result; Page divides into
  Division Writing and Display.
- Put freestyle Scripts in a separate collapsible region below the overview;
  Results no longer appear as an independent surface.

## 0.3.6 · 2026-09-01
- Rename the presenter from Execution to Runs: Execute remains a workflow
  action, while the workbench presents plural addressable Run attempts.
- Resolve both Folder-local and Job-backed Task Run/Result dialects without
  copying generated Job output into the Task Page.

## 0.3.5 · 2026-09-01
- Rename the optional Code presenter to Execution. `runs/` and `results/`
  define the capability as exact pairs; scripts/config are optional support.
- Preserve phase ownership of lifecycle and closure, so Execution remains a
  presenter rather than a second workflow door.

## 0.3.4 · 2026-09-01
- roster: the item table (SURVEY) is where every evidence mark is surveyed
  first; `evidence/probe/` is the outbound-question lane minted at LAND only;
  `probe/haipipe-probe` retired.

## 0.3.3 · 2026-08-31

The roster now treats `haipipe-application/fn/render.md` as Render's live
Folder-native writer, with `POST /_board/render` optional, and removes retired
Task/Direction skills from the active workbench list.

## 0.3.2 · 2026-08-31

task/ row ⚰️ RETIRED outright (JL: "we will not have the task/ folder
anymore") — swept pages' folders deleted; pagex/ nested under evidence/
with the mint depth fix noted; studio pair pre-created on swept pages.

## 0.3.1 · 2026-08-31

task/ and meeting/ lose their strip-menu rows (JL: "the task and meeting
should be removed as well") — storage stays on disk, task's read still owed
to a pagex card; roster surface cells updated.

## 0.3.0 · 2026-08-31

§🔌 finalized as JL ruled it ("one workbench for evidence, one for the
delivery, only one for the studio" + outline included): FIVE category
presenters + the 📂 mirror — 🧭 outline (outline/+workflow/, first and
default) · 🧾 evidence · 📤 delivery (🎞 segment carries the ✨ pen) ·
🎨 studio (haipipe-workbench-studio: drawing above, chat below, one page) ·
⚙️ code (pending). No lane sells its own strip row; roster cells for
studio/chat/draw/slide repointed.

## 0.2.0 · 2026-08-31

§🔌 the two workbench kinds: LANE workbenches own one rostered folder's law;
PRESENTER workbenches own one surface over a category and store nothing (no
roster row) — folder · value · evidence · delivery · code. The strip law:
one tab per category (🧭 🧾 📤 ⚙️-pending), one tool per hand (💬 🖌 🎞).
Roster surface cells repointed: latex/word → 📤 segments, slide → native
tab + read segment, render → 📤 ghost segment, pagex → 🧾 segment
(standalone row folded), workflow 🪜 → a 🧭 segment when built.

## 0.1.5 · 2026-08-31

Category folders (evidence/, delivery/), the runs/ execution door and the
simple-code law stated at the base; rows in ref/roster.md.


## 2026-08-31 · roster: the task/ row names the collection job

The `task/` row's ranked list now states that the page's collection job
(task-type `page`, `haipipe-task-for-page`) ranks first when one exists; the
lane's storage, surface and writer are unchanged.

## 0.1.3 — 2026-08-21

- **`ref/roster.md` gains the `outline/` row it had been missing since 260817.**
  The file's own opening law is that a subfolder of a page's home folder is board
  material only if its name is in this table; `<page>/outline/` had been real
  storage for four days with no row. Found in the 260821 skills audit.
- **The `probe/` row was three retired words deep**: `state: raised→working→bound`
  (retired at `haipipe-workbench-probe` 0.7.0) and `binding:` (renamed `bank:`), and
  its storage cell named only `card.md` — no `consumer/`, `executor/` or `proof/`,
  which is the entire stake wall. Rewritten from the workbench.
- The ships-under list gained `outline`, and the no-row exemption note now covers
  BOTH surface-only workbenches: `haipipe-workbench-page` (📂, over the list) and
  `haipipe-workbench-value` (🧮, over the `## Values` blocks inside probe cards).

haipipe-workbench — Changelog
===============================

Skill-scoped changelog (never loaded at invocation). Versions match SKILL.md frontmatter `version:`. Newest first.

## 0.1.2 - 2026-08-18

- `task/` joined the roster: the fourth citation twin, a page's ranked list
  of `tasks/` folders it is written about, materialized as symlinks to whole
  DIRECTORIES (never files — the inverse of pagex's own rule, because a task
  folder is never itself a page) and read for live status off `plan.yaml` /
  `report.yaml` / `QA/*.md`, never a hand-typed word. `live/task.py` +
  `assets/js/10-drawer/86-workbench-task.js`; design page QPf13.
- `meeting/` went 🟢 built: `<YYMMDD-HHMM>/digest.md` + `transcript.md`,
  exactly the shape the row already declared. JL ruled it STANDALONE over
  pointing at the separate `Meeting-<n>` page type — a meeting workbench is a
  page's own attachment with nothing to route, where a `Meeting-<n>` page
  owes a decision to some other page. `live/meeting.py` +
  `assets/js/10-drawer/87-workbench-meeting.js`; design page QPf14.

## 0.1.1 - 2026-08-15

- The slide row caught up with the same evening's rulings: writer is
  `/_board/autodeck` (`servers/workbench-studio/autodeck.py`, `claude -p` AUTHORS the deck from the
  page's .md; ✨ Regenerate on both doors; validation before write, overwrite
  always). The reflow writer it named (`live/deck.py` + `/_board/deck`) was
  deleted that hour and the two SKILL.md sentences shaped on it were reworded.

## 0.2.0 - 2026-08-15

- Per-plugin skills gained a home: `page-plugins/haipipe-plugin-<name>/` (folder retired 2026-09-22; the skills now sit flat in their families as `haipipe-workbench-<name>`)
  (JL: one skill per workbench, keep haipipe-block small) — the same third leg
  page-types/ and page-phases/ give the page family. `-word` is the first
  instance: the paragraph rule, the page-bib preference, the twin, the
  flags, and the warts, loadable without the board open.

## 0.1.0 - 2026-08-15

- Born from the QPf board's 260815 ruling (material is a workbench) and
  design.excalidraw's three-way split of the page contract.
- The four-part workbench definition (STORAGE / SURFACE / WRITER / BOUNDARY) and
  the eleven-name roster in `ref/roster.md`.
- First conforming instances: the latex/word/bibex tabs
  (`assets/js/10-drawer/82-workbench-exports.js` + `servers/workbench-page/export.py` in
  haipipe-block 0.128.0), registered with the `tab: {url, write}` spec.
## 0.9.0 · 2026-09-04

- Define the Outline category as three peer workspaces: Context, Bullet, and
  Evidence.
- Fold the former Plan Context and Page Records UI groups into Context
  Workspace without merging their source files.
- Retire PageX from active evidence writes; external evidence now enters
  through Supporting Run Results.
## 1.0.0 · 2026-09-04

- Freeze the generic public Page Workbench set at five: Outline, Studio, Runs,
  Delivery, and Folder.
- Make Chat/Draw, LaTeX/Word/Slide/Render, and the ranked Skill record internal
  references under their owning categories; delete Evidence/Probe redirects.
- Move Design to its Application family and Meeting to project/SPACE
  ownership; the Page meeting writer is retired.
