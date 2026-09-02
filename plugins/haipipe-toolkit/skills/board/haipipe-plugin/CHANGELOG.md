## 0.4.0 · 2026-09-02

- Separate rostered storage lanes from Plugin identity: a category Plugin may
  own several internal lanes without minting one Skill per subfolder.
- Record the unified Evidence ownership of Citation/Bib, Value, Display, and
  PageX; Probe remains the separately governed crossing shown in the same tab.

## 0.3.8 · 2026-09-02
- Treat category Plugins as possible direct owners of an internal lane.
- `haipipe-plugin-evidence` now owns Citations/Bib at `evidence/bibex/`; a
  storage lane no longer implies a duplicate Bibex Plugin Skill.

## 0.3.7 · 2026-09-01
- Make the Runs presenter overview-first: Execution, Discovery, and Page rows
  each join their authored Ticket to the paired Result; Page divides into
  Division Writing and Display.
- Put freestyle Scripts in a separate collapsible region below the overview;
  Results no longer appear as an independent surface.

## 0.3.6 · 2026-09-01
- Rename the presenter from Execution to Runs: Execute remains a workflow
  action, while the plugin presents plural addressable Run attempts.
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
Task/Direction skills from the active plugin list.

## 0.3.2 · 2026-08-31

task/ row ⚰️ RETIRED outright (JL: "we will not have the task/ folder
anymore") — swept pages' folders deleted; pagex/ nested under evidence/
with the mint depth fix noted; studio pair pre-created on swept pages.

## 0.3.1 · 2026-08-31

task/ and meeting/ lose their strip-menu rows (JL: "the task and meeting
should be removed as well") — storage stays on disk, task's read still owed
to a pagex card; roster surface cells updated.

## 0.3.0 · 2026-08-31

§🔌 finalized as JL ruled it ("one plugin for evidence, one for the
delivery, only one for the studio" + outline included): FIVE category
presenters + the 📂 mirror — 🧭 outline (outline/+workflow/, first and
default) · 🧾 evidence · 📤 delivery (🎞 segment carries the ✨ pen) ·
🎨 studio (haipipe-plugin-studio: drawing above, chat below, one page) ·
⚙️ code (pending). No lane sells its own strip row; roster cells for
studio/chat/draw/slide repointed.

## 0.2.0 · 2026-08-31

§🔌 the two plugin kinds: LANE plugins own one rostered folder's law;
PRESENTER plugins own one surface over a category and store nothing (no
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
  (retired at `haipipe-plugin-probe` 0.7.0) and `binding:` (renamed `bank:`), and
  its storage cell named only `card.md` — no `consumer/`, `executor/` or `proof/`,
  which is the entire stake wall. Rewritten from the plugin.
- The ships-under list gained `outline`, and the no-row exemption note now covers
  BOTH surface-only plugins: `haipipe-plugin-folder` (📂, over the list) and
  `haipipe-plugin-value` (🧮, over the `## Values` blocks inside probe cards).

haipipe-plugin — Changelog
===============================

Skill-scoped changelog (never loaded at invocation). Versions match SKILL.md frontmatter `version:`. Newest first.

## 0.1.2 - 2026-08-18

- `task/` joined the roster: the fourth citation twin, a page's ranked list
  of `tasks/` folders it is written about, materialized as symlinks to whole
  DIRECTORIES (never files — the inverse of pagex's own rule, because a task
  folder is never itself a page) and read for live status off `plan.yaml` /
  `report.yaml` / `QA/*.md`, never a hand-typed word. `live/task.py` +
  `assets/js/10-drawer/86-plugin-task.js`; design page QPf13.
- `meeting/` went 🟢 built: `<YYMMDD-HHMM>/digest.md` + `transcript.md`,
  exactly the shape the row already declared. JL ruled it STANDALONE over
  pointing at the separate `Meeting-<n>` page type — a meeting plugin is a
  page's own attachment with nothing to route, where a `Meeting-<n>` page
  owes a decision to some other page. `live/meeting.py` +
  `assets/js/10-drawer/87-plugin-meeting.js`; design page QPf14.

## 0.1.1 - 2026-08-15

- The slide row caught up with the same evening's rulings: writer is
  `/_board/autodeck` (`live/autodeck.py`, `claude -p` AUTHORS the deck from the
  page's .md; ✨ Regenerate on both doors; validation before write, overwrite
  always). The reflow writer it named (`live/deck.py` + `/_board/deck`) was
  deleted that hour and the two SKILL.md sentences shaped on it were reworded.

## 0.2.0 - 2026-08-15

- Per-plugin skills gained a home: `page-plugins/haipipe-plugin-<name>/`
  (JL: one skill per plugin, keep haipipe-board small) — the same third leg
  page-types/ and page-phases/ give the page family. `-word` is the first
  instance: the paragraph rule, the page-bib preference, the twin, the
  flags, and the warts, loadable without the board open.

## 0.1.0 - 2026-08-15

- Born from the QPf board's 260815 ruling (material is a plugin) and
  design.excalidraw's three-way split of the page contract.
- The four-part plugin definition (STORAGE / SURFACE / WRITER / BOUNDARY) and
  the eleven-name roster in `ref/roster.md`.
- First conforming instances: the latex/word/bibex tabs
  (`assets/js/10-drawer/82-plugin-exports.js` + `live/export.py` in
  haipipe-board 0.128.0), registered with the `tab: {url, write}` spec.
