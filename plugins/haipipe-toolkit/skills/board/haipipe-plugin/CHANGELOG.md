haipipe-plugin — Changelog
===============================

Skill-scoped changelog (never loaded at invocation). Versions match SKILL.md frontmatter `version:`. Newest first.

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
