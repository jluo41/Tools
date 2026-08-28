---
name: haipipe-plugin-slide
description: >-
  The slide/ plugin of a Board page: the page's deck at
  <page>/slide/<stem>-deck.html, derived and regenerable, authored from the
  page's own .md by /_board/autodeck. Trigger: slide plugin, page deck,
  regenerate the deck, slides tab, autodeck, /haipipe-plugin-slide.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-15"
---
# /haipipe-plugin-slide · the page's deck, authored from the page's own words

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only slide's delta: how a deck is authored from a page, and what regeneration promises.

## 🗂 Storage · one deck per page, derived

```text
<page>/slide/
└── <stem>-deck.html     the deck, one self-navigating file
```

DERIVED and regenerable: the next ✨ Regenerate overwrites it whole, so a hand edit to the deck is a note to yourself that the machine will eat.
A flat page has no deck: autodeck writes only for a folded page, so folding the page comes first.
The 📂 Folder tab flags this plugin STALE when the deck predates the page's `.md`.

## ⚙️ Writer · authored, validated, overwritten whole

The one door is `POST /_board/autodeck` (`live/autodeck.py`), and it AUTHORS rather than projects: `claude -p` reads the page's `.md` and writes the talk, so a Content division arrives as slides a presenter can speak, not as pasted prose.
Validation runs before the write, and a deck that fails it never lands; overwrite is always whole-file, never a merge.
Authoring is the only path: the reflow projection (`live/deck.py`) was retired the same evening (JL 260815), and a page with no deck yet shows a pointer that invites ✨ instead of a mechanical copy.

## 📡 Surface · the runtime is html-ppt's, never copied

The 🎞 tab frames the deck `?plain`; ✨ Regenerate sits on both doors, the tab and the menu row.
The deck links straight at `display/html-ppt`'s own assets by relative path: 36 themes, T to cycle them, F fullscreen, O overview, S presenter mode.
Nothing is vendored, so the deck improves when that skill improves; reimplementing any of it in the board would be the second worst thing here, and copying it the worst.

## 📂 Files

- `../../haipipe-board/live/autodeck.py`
  The authoring door: claude -p, validation, whole-file overwrite.
- `../../../display/html-ppt/`
  The runtime and 36 themes every deck links at, never copies.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.
