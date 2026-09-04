# Changelog · haipipe-plugin-delivery

## 0.3.1 — 2026-09-03
- Clarify that Delivery presents the roster's `delivery/` category row while
  owning no lane writer or second folder.

## 0.3.0 — 2026-09-03
- Make `delivery/latex/`, `delivery/word/`, `delivery/slide/`, and
  `delivery/render/` the physical writer destinations and saved-view URLs.
- Keep old flat lanes readable only for migration; never present or write them
  as the current structure.

## 0.2.1 — 2026-08-31
- Point all segments at canonical `delivery/<lane>/` addresses and present
  Render as a live Folder-native writer with an optional served adapter, not a
  ghost route.

## 0.2.0 — 2026-08-31
- The Slides segment gained the ✨ authoring bar (explicit press →
  /_board/autodeck) as the shell's native 🎞 row folded with the studio
  fold; the tab is now the delivery category's one surface entire.

## 0.1.0 — 2026-08-31
- Born as the 📤 presenter over the delivery/ category (JL 260831, the 🧾
  Evidence fold's twin): live/delivery.py + one registry row replacing the
  separate 📜 LaTeX and 📝 Word rows (82-plugin-exports.js → 82-plugin-delivery.js);
  slides read-only (authoring stays on the native 🎞 tab), render ghost until
  its route ships.
