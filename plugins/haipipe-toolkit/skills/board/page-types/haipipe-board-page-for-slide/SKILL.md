---
name: haipipe-board-page-for-slide
description: >-
  The VARIANT contract for a SLIDE Page: one page per deck, one Content division per slide. Each division carries the slide's SOURCE half (outline and talk notes, usually extracted from section pages) and its RENDER half: the LIVE slide, embedded as `![slide N](deck.html?preview=N)`, which the board renders as an iframe of the one deck file in single-slide mode. The same file opened bare is the full keyboard presentation, so review surface and presentation surface can never drift. It loads haipipe-board-page for the base frame and shares for-display's acceptance model: a person accepts a specific render. Use when writing or fixing a slide page, when a talk needs a review surface colleagues can read beside the live slides, when a slide shows a number nothing traces, or when the embed shows the wrong slide or none. Trigger: slide page, deck page, talk page, slides, presentation page, slide binding, preview mode, embed html, presenter deck, html-ppt, /haipipe-board-page-for-slide.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-05"
  summary: "Corrected by its first real page (QA4): the division embeds the LIVE slide via ?preview=N, one deck file for both surfaces; the PNG story and the strips-JS belief are retired."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-slide · one deck file, and every division shows its slide live

**LOAD `haipipe-board-page` FIRST.** It owns the base frame. This file adds only what a deck needs, and its acceptance model is `for-display`'s: a person accepts a RENDER, never a name.

**The kind this variant covers**: one page per DECK, one Content division per SLIDE.

```
kind    subject                              closes when
──────────────────────────────────────────────────────────────────────
Slide   one deck · division order IS         a person accepts every
page    deck order                           slide, or cuts it from
                                             the talk
```

## 🎬 One file, two surfaces

The deck is ONE html-ppt file, and both surfaces read it, so neither can drift:

```
📄 slides/<deck>.html                         ← the ONE file
     │
     ├──▶ 📋 REVIEW surface · the page          division N writes
     │        ![slide N](…deck.html?preview=N)  and the board renders it as a
     │        live iframe: exactly slide N,      no chrome, no keys
     │
     └──▶ 🎥 PRESENTATION surface · a tab       the same file bare, linked
              from ## Files: ← → flip ·          F fullscreen · S notes
```

`?preview=N` is html-ppt's own locked single-slide mode (`assets/runtime.js`): only slide N visible, chrome hidden, keys off. The board engine renders any `![alt](x.html)` as a live iframe with an always-visible open link beneath it (`src/body.py`), and the split-site build reroots the src like any figure path.

🚫 **Never paste slide markup into the page, and never write the embed without `?preview=N`.** Raw html in a division is escaped to visible text by the renderer; an embed without the preview query shows the whole deck cover in every division. The embed is always the one deck file plus the slide's own preview number.

**What the earlier version of this contract got wrong, recorded so it stays wrong**: 0.1.0 ruled "never embed the live deck, embed the PNG export, because `build.py` strips JS". The first real page (`QA4` on the boardform board, 260805) disproved both halves: the build never strips scripts from anything it ships, it only ASSERTS the page stays readable with scripts off (the open link under each frame is that no-JS path), and an iframe's file is never rewritten by the build at all. JL's ruling was "embed the html in the content division", and that is the rule. The PNG export remains available for surfaces that cannot iframe (a paper figure, an offline export); it is not the board's path.

## 🧬 The division: source half, render half, and the slide binding

```markdown
### 3 · The shape: one page, four sections, one place to rule
**What this slide must land**: what a reader sees when they open any page.
<the outline · the talk notes, in speaking order>
![slide 3 · the shape](QA-design/slides/QA4-board-skillset-deck.html?preview=3)
- accepted: ⬜ · source: `QB4` (the page grammar) · rendered: 260805
```

The typed record is the SLIDE BINDING, one per division: the division ↔ its source (which section pages or outline lines feed it) ↔ the deck file and preview number ↔ its acceptance row. Deck order is division order, so reordering the talk is reordering the page, and the base's numbering rules do the bookkeeping. The embed IS the division's figure: the checker accepts a media embed where it would demand a fenced diagram, and the caption rule (`**Name**: …` as the first line) still applies.

Every number a slide shows keeps `for-value`'s rule: a value binding by path, or the producing run named. A slide is a display that talks; it does not get a looser standard because it is temporary.

## 🔗 The chain in, and the build out

```
for-section pages ──▶ the outline            (the paper family's paper-slides
                      one beat per slide      extracts this; other families
      │               + talk notes            write it by hand)
      ▼
this page          ──▶ html-ppt              one deck file: one layout per
                       builds the deck        slide, one theme per deck
      │
      ▼
each division      ──▶ ![…](deck.html?preview=N) · the live embed
```

A rebuilt or reworded slide returns its acceptance row to ⬜, because acceptance was of a specific render; the deck file is live, so an edit shows everywhere the moment it lands, and the row is what says a human has not re-seen it. The deck-level gate closes only when every division's row is accepted or the slide is explicitly cut from the talk.

## 📂 Files

```
haipipe-board-page-for-slide/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-board-page`; the acceptance model is `haipipe-board-page-for-display`'s; the number rule is `haipipe-board-page-for-value`'s; the builder is `display/skills/html-ppt` (36 themes, 31 layouts, `?preview=N` single-slide mode, PNG export for non-iframe surfaces); the paper family's outline extractor is `display/skills/paper-slides`; the proving page is the boardform board's `QA-design/QA4-board-skillset.md`.
