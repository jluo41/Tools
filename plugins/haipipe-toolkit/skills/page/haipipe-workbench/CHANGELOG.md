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
  (JL: one skill per workbench, keep haipipe-board small) — the same third leg
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
  haipipe-board 0.128.0), registered with the `tab: {url, write}` spec.
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
