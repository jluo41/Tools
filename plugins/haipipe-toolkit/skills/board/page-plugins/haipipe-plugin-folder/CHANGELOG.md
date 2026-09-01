# haipipe-plugin-folder · Changelog

## 0.2.1 — 2026-08-31
- The view speaks the two-part grammar: a category chip per lane row, the
  gaps line names outline/workflow + missing categories instead of the old
  flat roster, and flat pre-sweep lanes are called out for the sweep.

## 0.2.0 · 2026-08-16

The unfold shows a folder's structure instead of its path list (JL: "是不是应该加一个 folder structure？… 这个排版不是非常按照我们的思路来排的").

- Files a level owns come first, then one 📁 branch per subfolder carrying its own file count, indented by depth. `display/`, whose units nest three levels, became readable by the same change.
- Rows got legible: 12px monospace to 13px on a 1.6 line, tabular figures so sizes align, more room under each plugin.
- A symlink row wears a bare 🔗 with its target on hover, so a borrowed file never reads as a copy.

## 0.1.5 · 2026-08-16
- display joined the curable set (JL 260816, choosing rebuild over unflagging): its ♻ recompiles each unit's derived preview.tex ▶ pdf, never intake/recipe/accepted; slide is now the only pointer row.

## 0.1.4 · 2026-08-16
- The header 🔄 rebuild stale (n) pill (JL 260816, pointing at the Word view's own button): walks every curable row sequentially, renders only while something mechanical is stale.

## 0.1.3 · 2026-08-16
- ♻ rebuild on MECHANICAL stale rows (JL 260816: "could we update them along the time?"): latex/word/bibex cure in place via their own POST; slide and display rows point instead of firing, because authored and human-gated artifacts are never a button reflex.

## 0.1.2 · 2026-08-16
- Fresh became a two-layer contract (JL 260816: "make sure the folder plugin refreshes every time"): the server's no-store plus the shell's landFrame, which reloads an unchanged src instead of skipping it.

## 0.1.1 · 2026-08-16
- Rows became doors (JL 260816: "how could I click them and view the content?"): a row unfolds its folder's files in place, each a link to the served file in a new tab.

## 0.1.0 · 2026-08-16
- Created the day after the 📂 tab shipped (JL 260816: "where is the plugin for the folder?"): the meta-plugin — no storage, no writer, first in the rail, staleness claimed narrowly over the DERIVED five.
