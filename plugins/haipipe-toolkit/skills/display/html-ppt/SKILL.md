---
name: html-ppt
description: HTML PPT Studio — author standalone static HTML decks with templates, themes, and keyboard navigation. Use when the user explicitly wants an HTML deck, a standalone slide deck, or an HTML deliverable such as an 小红书 carousel. Do not use for a Board Page talk or Page Delivery Slides lane; those are owned by haipipe-plugin-delivery.
---

# html-ppt — HTML PPT Studio

Author professional HTML presentations as static files. One theme file = one
look. One layout file = one page type. One animation class = one entry effect.
All pages share a token-based design system in `assets/base.css`.

## Install

```bash
npx skills add https://github.com/lewislulu/html-ppt-skill
```

One command, no build. Pure static HTML/CSS/JS with only CDN webfonts.

## What the skill gives you

- **37 theme styles** — 36 gallery themes plus the separate `academic-report` house preset, which also uses `assets/academic-report-extras.css`. See [references/themes.md](references/themes.md) for the catalog.
- **15 full-deck templates** (`templates/full-decks/<name>/`) — complete multi-slide decks with scoped `.tpl-<name>` CSS. 8 extracted from real-world decks (xhs-white-editorial, graphify-dark-graph, knowledge-arch-blueprint, hermes-cyber-terminal, obsidian-claude-gradient, testing-safety-alert, xhs-pastel-card, dir-key-nav-minimal), 7 scenario scaffolds (pitch-deck, product-launch, tech-sharing, weekly-report, xhs-post 3:4, course-module, **presenter-mode-reveal** — 演讲者模式专用)
- **31 layouts** (`templates/single-page/*.html`) with realistic demo data
- **27 CSS animations** (`assets/animations/animations.css`) via `data-anim`
- **20 canvas FX animations** (`assets/animations/fx/*.js`) via `data-fx` — particle-burst, confetti-cannon, firework, starfield, matrix-rain, knowledge-graph (force-directed), neural-net (pulses), constellation, orbit-ring, galaxy-swirl, word-cascade, letter-explode, chain-react, magnetic-field, data-stream, gradient-blob, sparkle-trail, shockwave, typewriter-multi, counter-explosion
- **Keyboard runtime** (`assets/runtime.js`) — arrows, T (theme), A (anim), F/O, **S (presenter mode: magnetic-card popup with CURRENT / NEXT / SCRIPT / TIMER cards)**, N (notes drawer), R (reset timer in presenter)
- **FX runtime** (`assets/animations/fx-runtime.js`) — auto-inits `[data-fx]` on slide enter, cleans up on leave
- **Showcase decks** for themes / layouts / animations / full-decks gallery
- **Headless Chrome render script** for PNG export

## When to use

Use when the user wants a standalone HTML presentation or carousel built from
an outline, content brief, or supplied notes. For a Board Page talk, use the
Page's `haipipe-plugin-delivery` Slides lane, which reads the Page and writes
its derived deck under `delivery/slide/`. Do not create a second deck from a
Page request through this standalone skill.

### 🎤 Presenter Mode (演讲者模式 + 逐字稿)

If the user mentions any of: **演讲 / 分享 / 讲稿 / 逐字稿 / speaker notes / presenter view / 演讲者视图 / 提词器**, or says things like "我要去给团队讲 xxx", "要做一场技术分享", "怕讲不流畅", "想要一份带逐字稿的 PPT" — consider the `presenter-mode-reveal` template and write notes sized to the requested talk. As a cue-card starting point, use 150–300 English words or 150–300 Chinese characters per slide; this range does not guarantee a fixed speaking duration.

See [references/presenter-mode.md](references/presenter-mode.md) for the full authoring guide including the 3 rules of speaker script writing:
1. **不是讲稿，是提示信号** — 加粗核心词 + 过渡句独立成段
2. **按语言控制提示卡长度。** 中文每页可从 150–300 个汉字开始，英文可从 150–300 个单词开始；实际长度按演讲时长调整。
3. **用口语，不用书面语** — "因此"→"所以"，"该方案"→"这个方案"

All full-deck templates support the S key presenter mode (it's built into `runtime.js`). **S opens a new popup window with 4 magnetic cards**:
- 🔵 **CURRENT** — live iframe preview of the current slide
- 🟣 **NEXT** — live iframe preview of the next slide
- 🟠 **SPEAKER SCRIPT** — large-font 逐字稿 (scrollable)
- 🟢 **TIMER** — elapsed time + slide counter + prev/next/reset buttons

Each card is **draggable by its header** and **resizable by the bottom-right corner handle**. Card positions/sizes persist to `localStorage` per deck. A "Reset layout" button restores the default arrangement.

Each preview is an `<iframe>` that loads the actual deck HTML with a `?preview=N` query param; `runtime.js` detects this and renders only slide N with no chrome. It uses the same CSS, theme, fonts, and target slide viewport as the audience view, so it should closely match the audience canvas. Browser and font rendering can still differ slightly across machines.

**Smooth navigation**: on slide change, the presenter window sends `postMessage({type:'preview-goto', idx:N})` to each iframe. The iframe just toggles `.is-active` between slides — **no reload, no flicker**. The two windows also stay in sync via `BroadcastChannel`.

Only `presenter-mode-reveal` is designed from the ground up around the feature with proper example 逐字稿 on every slide.

Keyboard in presenter window: `← →` navigate (syncs audience) · `R` reset timer · `Esc` close popup.
Keyboard in audience window: `S` open presenter · `T` cycle theme · `← →` navigate (syncs presenter) · `F` fullscreen · `O` overview.

## House default style: `academic-report` (settled 2026-07-21)

Unless the user asks for something else, **start every new deck from this
style**. It was refined during reviews of a historical REACH-ADHD NIH briefing;
that separate project is not included or required. The preset and rules below are
self-contained in this skill.

| Rule | Value |
|---|---|
| Background | pure white `#ffffff` — page AND cards |
| Font | Times New Roman on every element (code spans too) |
| Type scale | normal-PPT sizes: titles ~33pt, body ~15-18pt; **trim content rather than shrink type** |
| Chrome | NO kicker above titles · NO rule under titles · NO page index |
| Body text | bullets, ONE SENTENCE PER LINE (`.blt` list) |
| Layout | slides fill the page (flex column, space-between) |
| Palette | ink/grays + navy accent `#1f5aa8` + amber warn `#b45309` only |
| Placeholders | dashed amber `.todo` pill — unfilled content is visible, never presentable by accident |
| Corners | square-ish (2px radius), no shadows |

Wire-up in a scaffolded deck's `<head>`. Replace `ASSET_PREFIX` with the
relative prefix already written into `index.html` by `new-deck.sh`:

```html
<link rel="stylesheet" href="ASSET_PREFIX/base.css">
<link rel="stylesheet" id="theme-link" href="ASSET_PREFIX/themes/academic-report.css">
<link rel="stylesheet" href="ASSET_PREFIX/academic-report-extras.css">
```

`themes/academic-report.css` = tokens; `academic-report-extras.css` = the
component conventions (.blt bullets, .todo pill, kicker-off, page-fill,
table styles). For per-slide SVG / PPTX / PDF export of such a deck, use the
sibling **html-to-svg** skill — same contract, plus native-shapes pptx.

## Before you author anything

Reuse details the user already supplied. Ask only for a missing choice that
would materially change the deck; otherwise state a sensible default and
continue.

1. **Content & audience.** Use the supplied outline, slide count, and audience.
   If one is missing and cannot be inferred, ask for that detail.
2. **Style / theme.** Default to `academic-report` unless the user signals
   another tone. When useful, recommend candidates based on the brief:
   - Business / investor pitch → `pitch-deck-vc`, `corporate-clean`, `swiss-grid`
   - Tech sharing / engineering → `tokyo-night`, `dracula`, `catppuccin-mocha`,
     `terminal-green`, `blueprint`
   - 小红书图文 → `xiaohongshu-white`, `soft-pastel`, `rainbow-gradient`,
     `magazine-bold`
   - Academic / report → `academic-paper`, `editorial-serif`, `minimal-white`
   - Edgy / cyber / launch → `cyberpunk-neon`, `vaporwave`, `y2k-chrome`,
     `neo-brutalism`
3. **Starting point.** Choose among the 15 full-deck templates when one fits;
   otherwise use the starter and compose from existing layouts. Ask only when
   two materially different approaches remain plausible.

## Quick start

1. **Scaffold a new deck.** From the user's project directory, call the skill
   script by its installed path. It creates the output under the caller's
   current directory by default:
   ```bash
   HTML_PPT=/path/to/html-ppt
   "$HTML_PPT/scripts/new-deck.sh" my-talk
   open my-talk/index.html
   ```
   Choose a full-deck template with the optional third argument:
   `"$HTML_PPT/scripts/new-deck.sh" my-talk . presenter-mode-reveal`.
   The scaffold rewrites shared-asset links for the caller's project path.
2. **Pick a theme.** Open the deck and press `T` to cycle. Or hard-code it,
   keeping the relative asset prefix already written into `index.html` by the scaffold:
   ```html
   <link rel="stylesheet" id="theme-link" href="ASSET_PREFIX/themes/aurora.css">
   ```
   Keep the asset prefix created by the scaffold and change only the theme filename.
   Catalog in [references/themes.md](references/themes.md).
3. **Pick layouts.** Copy `<section class="slide">...</section>` blocks out of
   files in `templates/single-page/` into your deck. Replace the demo data.
   Catalog in [references/layouts.md](references/layouts.md).
4. **Add animations.** Put `data-anim="fade-up"` (or `class="anim-fade-up"`) on
   any element. On `<ul>`/grids, use `anim-stagger-list` for sequenced reveals.
   For canvas FX, use `<div data-fx="knowledge-graph">...</div>` and include
   `fx-runtime.js` using the scaffold-generated asset prefix.
   Catalog in [references/animations.md](references/animations.md).
5. **Use a full-deck template.** Recreate the deck with
   `"$HTML_PPT/scripts/new-deck.sh" my-talk . <template-name>` so the script
   copies its files and rewrites shared-asset links. Catalog in
   [references/full-decks.md](references/full-decks.md)
   and gallery at `templates/full-decks-index.html`.
6. **Render to PNG.**
   ```bash
   HTML_PPT=/path/to/html-ppt
   "$HTML_PPT/scripts/render.sh" "$HTML_PPT/templates/theme-showcase.html"  # one shot
   "$HTML_PPT/scripts/render.sh" my-talk/index.html 12                        # 12 slides
   ```

## Authoring rules (important)

- **Always start from a template.** Don't author slides from scratch — copy the
  closest layout from `templates/single-page/` first, then replace content.
- **Use tokens, not literal colors.** Every color, radius, shadow should come
  from CSS variables defined in `assets/base.css` and overridden by a theme.
  Good: `color: var(--text-1)`. Bad: `color: #111`.
- **Don't invent new layout files.** Prefer composing existing ones. Only add
   a new `templates/single-page/*.html` if none of the 31 fit.
- **Respect chrome slots.** `.deck-header`, `.deck-footer`, `.slide-number`
  and the progress bar are provided by `assets/base.css` + `runtime.js`.
- **Keyboard-first.** Include `<script src="ASSET_PREFIX/runtime.js"></script>`
  using the asset prefix created by `new-deck.sh`; this supports ← → / T / A / F / S / O / hash deep-links.
- **One `.slide` per logical page.** `runtime.js` makes `.slide.is-active`
  visible; all others are hidden.
- **Supply notes.** Wrap speaker notes in `<div class="notes">…</div>` inside
  each slide. Press S to open presenter mode.
- **NEVER put presenter-only text on the slide itself.** Descriptive text like
  "这一页展示了……" or "Speaker: 这里可以补充……" or small explanatory captions
  aimed at the presenter MUST go inside `<div class="notes">`, NOT as visible
  `<p>` / `<span>` elements on the slide. The `.notes` class is hidden in the
  audience view and shown in presenter mode. Notes remain readable in the
  shared HTML source; never put confidential material there. Slides should
  contain audience-facing content (titles, bullet points, data, charts, images).

## Writing guide

See [references/authoring-guide.md](references/authoring-guide.md) for a
step-by-step walkthrough: file structure, naming, how to transform an outline
into a deck, how to choose layouts and themes per audience, how to do a
Chinese + English deck, and how to export.

## Catalogs (load when needed)

- [references/themes.md](references/themes.md) — all 37 theme styles and when-to-use.
- [references/layouts.md](references/layouts.md) — all 31 layout types.
- [references/animations.md](references/animations.md) — 27 CSS + 20 canvas FX animations.
- [references/full-decks.md](references/full-decks.md) — all 15 full-deck templates.
- [references/presenter-mode.md](references/presenter-mode.md) — **演讲者模式 + 逐字稿编写指南（技术分享/演讲必看）**.
- [references/authoring-guide.md](references/authoring-guide.md) — full workflow.

## File structure

```
html-ppt/
├── SKILL.md                 (this file)
├── references/              (detailed catalogs, load as needed)
├── assets/
│   ├── base.css             (tokens + primitives — do not edit per deck)
│   ├── fonts.css            (webfont imports)
│   ├── runtime.js           (keyboard + presenter + overview + theme cycle)
│   ├── themes/*.css         (37 theme style files, including the house preset)
│   └── animations/
│       ├── animations.css   (27 named CSS entry animations)
│       ├── fx-runtime.js    (auto-init [data-fx] on slide enter)
│       └── fx/*.js          (20 canvas FX modules: particles/graph/fireworks…)
├── templates/
│   ├── deck.html                  (minimal 6-slide starter)
│   ├── theme-showcase.html        (36 gallery themes, iframe-isolated)
│   ├── layout-showcase.html       (iframe tour of all 31 layouts)
│   ├── animation-showcase.html    (20 FX + 27 CSS animation slides)
│   ├── full-decks-index.html      (gallery of all 15 full-deck templates)
│   ├── full-decks/<name>/         (15 scoped multi-slide deck templates)
│   └── single-page/*.html         (31 layout files with demo data)
├── scripts/
│   ├── new-deck.sh                (scaffold a deck from deck.html)
│   └── render.sh                  (headless Chrome → PNG)
└── examples/demo-deck/            (complete working deck)
```

## Rendering to PNG

`scripts/render.sh` wraps headless Chrome at
`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. For multi-slide
capture, runtime.js exposes `#/N` deep-links, and render.sh iterates 1..N.

```bash
HTML_PPT=/path/to/html-ppt
"$HTML_PPT/scripts/render.sh" "$HTML_PPT/templates/single-page/kpi-grid.html"  # single page
"$HTML_PPT/scripts/render.sh" examples/demo-deck/index.html 8 out-dir              # 8 slides
```

## Keyboard cheat sheet

```
←  →  Space  PgUp  PgDn  Home  End    navigate
F                                       fullscreen
S                                       open presenter window (magnetic cards: current/next/script/timer)
N                                       quick notes drawer (bottom overlay)
R                                       reset timer (in presenter window)
?preview=N                              URL param — force preview-only mode (single slide, no chrome)
O                                       slide overview grid
T                                       cycle themes (reads data-themes attr)
A                                       cycle demo animation on current slide
#/N in URL                              deep-link to slide N
Esc                                     close all overlays
```

## License & author

MIT. Copyright (c) 2026 lewis &lt;sudolewis@gmail.com&gt;.
