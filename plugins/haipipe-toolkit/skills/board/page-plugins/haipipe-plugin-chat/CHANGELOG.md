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
