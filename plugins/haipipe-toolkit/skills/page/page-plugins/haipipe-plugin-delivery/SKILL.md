---
name: haipipe-plugin-delivery
description: >-
  The ONE presentation plugin for what leaves a page: a single 📤 Delivery tab
  showing the latex, word, slide and render lanes as segments. It owns those
  four internal lane contracts without exposing duplicate plugin skills;
  slides are never auto-built. Trigger: delivery plugin, delivery tab,
  exports tab, LaTeX, compile PDF, Word, docx, slide deck, render preview,
  show the pdf docx deck together,
  /haipipe-plugin-delivery.
metadata:
  version: "0.5.0"
  last_updated: "2026-09-13"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-delivery · one tab owns what four lanes ship

**LOAD `haipipe-plugin` FIRST.** This CATEGORY plugin owns the SURFACE over
`delivery/` and the four internal lane contracts beneath it (latex · word ·
slide · render). Each lane keeps its own storage, writer, and gate in `ref/`;
none is a second callable Plugin skill.

Load `../../haipipe-page/ref/page-run-families.md` for the Page Run identity
contract. Each concrete delivery target/version is commissioned as an `RD`
Page Delivery Run (`rdNN_web`, `rdNN_latex`, `rdNN_word`, `rdNN_slide`, or
`rdNN_render`). This plugin remains one visible tab and four lane contracts;
the RD identity is the execution lineage behind a lane, not a second tab.

```text
this file     the 📤 Delivery tab: a 🏠 stat of what is built, one segment per lane
the lanes     delivery/latex/ · delivery/word/ · delivery/slide/ ·
              delivery/render/; contracts in ref/{latex,word,slide,render}.md
              — one canonical physical home per lane
the category  <page>/delivery/ (flat names are compatibility reads only)
```

## 📡 Surface · one tab, five segments

```text
📤 Delivery
├── 🏠 What's built   default: one row per lane — ✅ built · mtime, or ⬜ with
│                     the way to build it; render/ shows its file count
├── 📜 LaTeX          the saved <stem>-view.html; BUILT ON CLICK via
│                     /_board/latex when missing (deterministic, safe)
├── 📝 Word           same, via /_board/word
├── 🎞 Slides         the saved <stem>-deck.html + the ✨ AUTHORING bar (one
│                     explicit press → /_board/autodeck, claude -p); a missing
│                     deck is a ghost until a person presses — never a view
└── 📱 Render         saved recipient previews; build through the live
                      Folder-native `haipipe-application/fn/render.md` writer;
                      `POST /_board/render` is only an optional served adapter
```

- **The shell's native 🎞 row folded 260831 evening** (with the studio fold);
  its ✨ bar moved into the Slides segment here, still one explicit press.
- **The separate 📜 and 📝 strip rows are folded** (82-plugin-delivery.js,
  replacing 82-plugin-exports.js), the way Citations folded into Outline's
  Evidence Workspace.
- **The tab auto-calls no model.** LaTeX/Word build on click through their
  own deterministic pens; the deck authors only on the ✨ press; Render shows
  the live lane and may invoke only its explicit Folder-native writer/adapter.

## 🧾 RD ownership and receipt

An RD binds one source Page version to one target lane and records the artifact,
build diagnostics, and `delivery/<lane>/build-manifest.json`. Rebuilding the
same target may be another attempt in that RD lineage; a different target or
materially different source version gets a different RD. The build receipt is
machine-readable delivery evidence, not a whole-Page acceptance decision.
Evidence truth remains in the RE Result, Page prose remains in the Page
source, and `haipipe-page-check` remains the only human whole-Page close gate.

## 🗺 Status · 🟢 built 260831

`live/delivery.py` serves GET `/_board/delivery` (the segmented surface) and
its POST twin; `82-plugin-delivery.js` registers the ONE row.

## 🚫 No standalone delivery check lane

Delivery has no separate quality lane or sibling report. Its machine receipt
is the single `build-manifest.json`, whose `status`, `readiness`,
`checks`, and `render` fields describe what was built and which blockers remain.
The Page workflow's `haipipe-page-check` owns the human whole-Page close gate;
Delivery only projects the declared outputs and their build diagnostics.

## 📂 Files

- `ref/latex.md` · `ref/word.md` · `ref/slide.md` · `ref/render.md` · the
  four internal lane contracts; load only the one needed for the requested
  projection
- `../../haipipe-page/ref/page-run-families.md` · RP/RE/RD identity and
  Result/Card/Label binding contract
- `../../../board/haipipe-board/live/delivery.py` · the segmented surface and its twin
- `../../../board/haipipe-board/assets/js/10-drawer/82-plugin-delivery.js` · the one registry row
- `../_shared-export/` · the builders the lanes' routes call (md2tex, md2docx)
