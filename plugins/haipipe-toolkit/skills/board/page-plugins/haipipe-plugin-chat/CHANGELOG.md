## 0.4.2 — 2026-08-31
- Composer grew ⌨ TUI (presses the header's .term — one switch, QD1; the
  ← returns) and the ⚙ menu an Aa text-size select (--chatfs, stored).

## 0.4.1 — 2026-08-31
- 🖌 grew its menu: ✨ Draw it (composer text = the ask, toast progress) ·
  Hide/Show the drawing; outside the shell both say where the drawing lives.

## 0.4.0 — 2026-08-31
- The composer took the Claude Code shape (JL): rounded card, control row
  inside (＋ 🗂 ✨ ⚙ 🖌 ➤); the toggles open POPUPS above the composer;
  sessions no longer auto-open at boot (reverses 260815 "list first");
  ＋ = new session direct; 🖌 = the studio draw fold; bubbles 12.5px.

## 0.3.3 — 2026-08-31
- Surface rehomed: the pane is the lower half of the one 🎨 Studio tab
  (haipipe-plugin-studio); GUI/TUI segment, keep step, walls unchanged.

## 0.3.2 · 2026-08-31

§🗺 row: the chat edits the page's excalidraw scene mid-discussion on the
person's ask (haipipe-plugin-draw 0.2.2 holds the pen law).

# haipipe-plugin-chat · Changelog

## 0.3.1 · 2026-08-31

The boot's task-list pointer follows the task→pagex merge under evidence/
(category folders, haipipe-page 0.47.0).


## 0.3.0 · 2026-08-31

§🗺 gains the collection-job row: "collect this page's values" lands in the
page's own collection job (task-type `page`, `haipipe-task-for-page`), beside
the generic task-work row.


## 0.2.0 · 2026-08-31
- Rewritten from 49 to 140 lines with the three things a page chat needs: **§🔒 access** (read everything in the SPACE, write anywhere; the walls are the rules, the checker teeth and one log record per write; generated files by their generator only; `_runs/`, `runs/` and a `state: working` QA file never; the four ticks a person's), **§🗺 the table** (what a message is → the file it lands in → the grammar → the authority → the ONE skill loaded for it), **§🧠 the boot** (`prime_context` injects page type, phase, the outline inventory, the page's `skill/` and `task/` lists). A kept session lands one log record listing the files it changed, which is its receipt. **§🔁 The chat runs the page workflow** (JL 260831: "make the chat implement the whole workflow of haipipe-page"): the seven phases with their verbs, the skill each loads, its exit and its trace; the strip from `src/page_phase.py` at boot; a pass in the chat is a pass; CHECK stays a fresh agent. `live/chat.py`'s four rule strings became one page ruleset and one board ruleset that carry the compact table and point here; `scoped` keeps the Skill tool.

## 0.1.0 · 2026-08-15
- Initial draft, round 2 of the thin-door migration (JL 260815): every live QPf plugin gains its skill; delta-only over haipipe-plugin.
