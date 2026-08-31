---
name: haipipe-plugin-delivery
description: >-
  The ONE presentation plugin for what leaves a page: a single 📤 Delivery tab
  showing the latex, word, slide and render lanes as segments. Presentation
  only — the four storage folders, their builders and routes stay with their
  own contracts; slides are never auto-built here. Trigger: delivery plugin,
  delivery tab, exports tab, show the pdf docx deck together,
  /haipipe-plugin-delivery.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-delivery · one tab presents what four lanes ship

**LOAD `haipipe-plugin` FIRST.** The 🧾 Evidence fold's twin, one category
over: this plugin owns no storage and no writer, it is the SURFACE over the
`delivery/` category (roster: latex · word · slide · render — what leaves the
page). It is a PRESENTER plugin (haipipe-plugin §🔌): no roster row, no
folder of its own.

```text
this file     the 📤 Delivery tab: a 🏠 stat of what is built, one segment per lane
the lanes     latex/ (haipipe-plugin-latex) · word/ (haipipe-plugin-word) ·
              slide/ (haipipe-plugin-slide) · render/ (haipipe-plugin-render)
              — storage, builders, routes UNCHANGED
the category  <page>/delivery/ (flat names are migration stubs, QPf1)
```

## 📡 Surface · one tab, five segments

```text
📤 Delivery
├── 🏠 What's built   default: one row per lane — ✅ built · mtime, or ⬜ with
│                     the way to build it; render/ shows its file count
├── 📜 LaTeX          the saved <stem>-view.html; BUILT ON CLICK via
│                     /_board/latex when missing (deterministic, safe)
├── 📝 Word           same, via /_board/word
├── 🎞 Slides         the saved <stem>-deck.html, READ-ONLY: a missing deck is
│                     a ghost pointing at the native 🎞 tab's ✨ bar, because
│                     that pen is claude -p authoring, never pressed by a view
└── 📱 Render         ghost until the lane's route ships (roster 🟡)
```

- **The native 🎞 Slides tab STAYS on the strip** (like 💬 and 🖌): a tool
  with an authoring pen keeps its surface; this tab only shows the projection.
- **The separate 📜 and 📝 strip rows are folded** (82-plugin-delivery.js,
  replacing 82-plugin-exports.js), the way 📚 bibex folded into 🧾 Evidence.
- **The tab writes nothing and calls no model.** LaTeX/Word builds it presses
  are the lanes' own deterministic pens; everything else it only frames.

## 🗺 Status · 🟢 built 260831

`live/delivery.py` serves GET `/_board/delivery` (the segmented surface) and
its POST twin; `82-plugin-delivery.js` registers the ONE row.

## 📂 Files

- `../haipipe-plugin-latex/SKILL.md` · `../haipipe-plugin-word/SKILL.md` ·
  `../haipipe-plugin-slide/SKILL.md` · `../haipipe-plugin-render/SKILL.md` ·
  the four lane contracts this surface presents
- `../../haipipe-board/live/delivery.py` · the segmented surface and its twin
- `../../haipipe-board/assets/js/10-drawer/82-plugin-delivery.js` · the one registry row
- `../_shared-export/` · the builders the lanes' routes call (md2tex, md2docx)
