---
name: haipipe-board-page-for-slide
description: >-
  The VARIANT contract for a SLIDE Page: one page per deck, one Content division per talk BEAT, one embed and one accept row PER SLIDE inside the beat. Each division carries the beat's SOURCE half (outline and talk notes, usually extracted from section pages) and its RENDER half: each slide LIVE as `![slide N](deck.html?preview=N#sN)`, an iframe of the one deck file in single-slide mode, so one slide can be accepted while its neighbor is redone. The same file opened bare is the full keyboard presentation, so review surface and presentation surface can never drift; `?preview=A-B` remains a legal compact strip for a settled beat. It loads haipipe-board-page for the base frame and shares for-display's acceptance model: a person accepts a specific render. Use when writing or fixing a slide page, when a talk needs a review surface colleagues can read beside the live slides, when a slide shows a number nothing traces, or when the embed shows the wrong slide or none. Trigger: slide page, deck page, talk page, slides, beat, presentation page, slide binding, preview mode, range strip, embed html, presenter deck, html-ppt, /haipipe-board-page-for-slide.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-05"
  summary: "Re-ruled A on QA4 (JL 260805, after seeing B rendered): per-slide embeds and per-slide acceptance inside beat divisions, so slides iterate one by one; the ?preview=A-B strip stays a compact form for a settled beat."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-slide · one deck file, and every division shows its slide live

**LOAD `haipipe-board-page` FIRST.** It owns the base frame. This file adds only what a deck needs, and its acceptance model is `for-display`'s: a person accepts a RENDER, never a name.

**The kind this variant covers**: one page per DECK, one Content division per talk BEAT, one embed per SLIDE inside it (JL re-ruled A on QA4, 260805, after B's beat-grain tick blocked slide-by-slide iteration).

```
kind    subject                              closes when
──────────────────────────────────────────────────────────────────────
Slide   one deck · beat order IS             a person accepts every
page    deck order · each slide in a         slide, or cuts it from
        beat embeds on its own               the talk
```

**The type key.** A slide page declares `page-type: slide` in its frontmatter, and the line is REQUIRED: a deck can sit on any filename, and the proving page `QA4` wears a Q filename, so only the key says the divisions are slides and the page closes slide by slide. The `page-type:` key beats the filename (base, type resolution step ③).

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

**The embed carries BOTH selectors: `?preview=N#sN`.** The query drives the runtime; the fragment drives a scripts-off fallback. The DEFAULT is one embed per slide, because acceptance iterates per slide. `?preview=A-B` is the COMPACT form for a beat that is already settled: the runtime renders slides A..B as a vertical strip (each at 16:9 of the frame width, a hairline between them) and the board sizes the frame to `aspect-ratio:16/(9×count)`; its cost is that the scripts-off fallback shows only the range's first slide, and a tick would cover the set. The deck gives each `<section class="slide">` an `id="sN"` and carries one small style block, SCOPED so it never fights the runtime (unscoped, it hid every non-target slide of a strip):

```css
html:not([data-preview]) .deck .slide:target{opacity:1;transform:none;pointer-events:auto}
html:not([data-preview]) .deck:has(.slide:target) .slide:not(:target){display:none}
```

So on a surface that blocks scripts (a VS Code webview, a locked-down frame), the fragment still shows the slide; with scripts on, the runtime stamps `data-preview` and takes over. Verified both ways in a real Chrome on QA4, including with script execution disabled, over the tailnet address a reader actually uses.

🚫 **Never paste slide markup into the page, and never write the embed bare.** Raw html in a division is escaped to visible text by the renderer; an embed without `?preview=N#sN` shows the whole deck cover in every division, or a blank frame where scripts are off. The embed is always the one deck file plus the slide's own preview number and fragment.

**What the earlier version of this contract got wrong, recorded so the mistake stays on the page**: 0.1.0 ruled "never embed the live deck, embed the PNG export, because `build.py` strips JS". The first real page (`QA4` on the boardform board, 260805) disproved both halves: the build never strips scripts from anything it ships, it only ASSERTS the page stays readable with scripts off (the open link under each frame is that no-JS path), and an iframe's file is never rewritten by the build at all. JL's ruling was "embed the html in the content division", and that is the rule. The PNG export remains available for surfaces that cannot iframe (a paper figure, an offline export); it is not the board's path.

## 🧬 The division: source half, render half, and the slide binding

```markdown
### 3 · How it works · slides 5-6
**What this beat must land**: Type × Phase, then the bounded loop.
<the outline · the talk notes, in speaking order>
![slide 5 · type × phase](…deck.html?preview=5#s5)
- accepted: ⬜ · slide 5 · source: `QB5` `QB6` · rendered: 260805
![slide 6 · the loop](…deck.html?preview=6#s6)
- accepted: ⬜ · slide 6 · source: `QB5` §6 §9 · rendered: 260805
```

The typed record is the SLIDE BINDING, one per SLIDE: the slide ↔ its source (which section pages or outline lines feed it) ↔ the deck file and preview number ↔ its own acceptance row. Per-slide rows are the point of ruling A: one slide is accepted while its neighbor is redone, which is the iteration a review loop needs. Deck order is beat order down the page, embed order inside a beat; the base's numbering rules do the bookkeeping. The embed IS the division's figure: the checker accepts a media embed where it would demand a fenced diagram, and the caption rule (`**Name**: …` as the first line) still applies.

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

A rebuilt or reworded slide returns ITS acceptance row to ⬜ (a compact-strip beat resets as a set, which is the compact form's stated cost); the deck file is live, so an edit shows everywhere the moment it lands, and the row is what says a human has not re-seen it. The deck-level gate closes only when every slide's row is accepted or the slide is explicitly cut from the talk.

## 📂 Files

```
haipipe-board-page-for-slide/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-board-page`; the acceptance model is `haipipe-board-page-for-display`'s; the number rule is `haipipe-board-page-for-value`'s; the builder is `display/skills/html-ppt` (36 themes, 31 layouts, `?preview=N` single-slide mode, PNG export for non-iframe surfaces); the paper family's outline extractor is `display/skills/paper-slides`; the proving page is the boardform board's `QA-design/QA4-board-skillset.md`.
