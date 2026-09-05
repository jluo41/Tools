# Slide lane · the page's deck authored from the page's own words

This is an internal lane contract of `haipipe-plugin-delivery`. The category
skill owns the public surface; this reference owns deck authoring, storage,
validation, and regeneration promises.

> 📤 Since 260831 evening the 🎞 segment inside the 📤 Delivery tab (`haipipe-plugin-delivery`) is this lane's ONE surface, and it carries the ✨ authoring bar (one explicit press → /_board/autodeck); the shell's native 🎞 row folded with the studio fold.

## 🗂 Storage · one deck per page, derived

```text
<page>/delivery/slide/
└── <stem>-deck.html     the deck, one self-navigating file
```

DERIVED and regenerable: the next ✨ Regenerate overwrites it whole, so a hand edit to the deck is a note to yourself that the machine will eat.
A flat page has no deck: autodeck writes only for a folded page, so folding the page comes first.
The 📂 Folder tab flags this lane STALE when the deck predates the page's `.md`.

## ⚙️ Writer · authored, validated, overwritten whole

The one door is `POST /_board/autodeck` (`live/autodeck.py`), and it AUTHORS rather than projects: `claude -p` reads the page's `.md` and writes the talk, so a Content division arrives as slides a presenter can speak, not as pasted prose.
Validation runs before the write, and a deck that fails it never lands; overwrite is always whole-file, never a merge.
Authoring is the only path: the reflow projection (`live/deck.py`) was retired the same evening (JL 260815), and a page with no deck yet shows a pointer that invites ✨ instead of a mechanical copy.

## 📡 Surface · the runtime is html-ppt's, never copied

Delivery's 🎞 segment frames the deck `?plain`; ✨ Regenerate sits in that segment.
The deck links straight at `display/html-ppt`'s own assets by relative path: 36 themes, T to cycle them, F fullscreen, O overview, S presenter mode.
Nothing is vendored, so the deck improves when that skill improves; reimplementing any of it in the board would be the second worst thing here, and copying it the worst.


The writer always lands new decks in `delivery/slide/`. A pre-migration flat
`slide/` may be read during a sweep, but it is not a current destination and
must not be shown as the canonical Folder row.

## 📂 Files

- `../../../haipipe-board/live/autodeck.py`
  The authoring door: claude -p, validation, whole-file overwrite.
- `../../../../display/html-ppt/`
  The runtime and 36 themes every deck links at, never copies.
- `../../../haipipe-plugin/ref/roster.md`
  The `delivery/slide/` lane row this category owns.
