# Slide · every page may have a deck, and the deck is authored
state: ✅ SETTLED · the surface is live end to end and all four aims closed 260815; the slide's only home is the plugin, everywhere
owner: JL
page-type: design
method: describe the plugin as it runs today; history lives in Log and `_archive/`
session: 65d477e7-b493-49d7-b508-2b0f7ea0772c

## Opening
Where does a page's talk live, and how does it stay fresh?

Every page MAY have one deck at `slide/<page>-deck.html`, optional the way a scene in `draw/` or a kept session in `chat/` is.
The deck is the AI deck, JL's ruling: Claude reads the page's markdown, makes editorial choices, and writes the file on the html-ppt shell.
A ✨ Regenerate button on both doors re-authors it in one click, so a deck is never more than one gesture behind its page.
The design succeeds when a reader opens the Slides tab, watches a real talk about the page, and can refresh it without leaving the browser.

**Covered elsewhere**: `QPf1` rules that every subfolder of a page is a plugin; `QPf2` and `QPf4` are the sibling plugins this one is shaped like; the html-ppt skill (`display/html-ppt`) owns everything a deck looks like.

## Diagram
**One file, two doors, one button**: where the deck lives and how it opens and refreshes.
```text
  📋 the PAGE                        🎞 the DECK, beside it (OPTIONAL)
  ┌─────────────────────────┐       ┌──────────────────────────────┐
  │ ## Content …            │  tab  │ <page>/slide/                │
  │ the source Claude       │ ─────▶│   <page>-deck.html           │
  │ distills into a talk    │  🎞    │ html-ppt shell · themes ·    │
  └───────────┬─────────────┘       │ runtime · speaker notes      │
              │                     └──────────▲───────────────────┘
              │   ✨ Regenerate                │ writes
              └──▶ POST /_board/autodeck ── claude -p ──┘
```

## Content
### 1 · The home: derived, never registered
**One path per page**: existence of the file is the whole state.
```text
  📄 <page>/slide/<page>-deck.html
  🔑 derived from the page's own path, the way Draw derives its owner
  🕳 no manifest row, no registry: HEAD the path and you know
```
A folded page (`<name>/<name>.md`) owns the `slide/` folder, and the deck's filename is the page stem plus `-deck.html`.
Both doors below derive this path from the page they are on, so nothing keeps a list that could drift.
When the file is absent the surfaces say so and offer the button, and nothing generates a deck behind your back.

### 2 · The two doors
**Where a deck opens**: the shell tab and the page panel, one loader behind both.
```text
  🚪 the shell's 🎞 Slides tab      beside Chat and Draw, with the
                                    ✨ bar riding above the frame
  🚪 the page's 🎞 panel            a resizable right split, with
                                    ✨ regenerate in its header
  🔑 ?plain                         or the deck comes back wearing
                                    the operating shell
```
Both doors HEAD the derived path and show the saved deck, or a pointer to the ✨ button when none exists.
Every load is cache-busted, so a freshly written deck appears on the next click and a stale iframe can never survive its file.

### 3 · ✨ Regenerate: one click, one authored deck
**The loop**: what the button does and what it overwrites.
```text
  ✨ click ──▶ POST /_board/autodeck {file, prompt?}
           ──▶ live/autodeck.py runs `claude -p` on the page's .md
           ──▶ 💾 slide/<page>-deck.html replaced ──▶ frame reloads
  ⏱ a few minutes · the status word says so while it thinks
```
The ask box is optional: empty means present the page's argument, and a typed ask steers the talk's emphasis.
The `<head>` with its asset hops is computed server-side from real paths, so the model's freedom starts at `<body>` and a generated deck can never 404 its own stylesheets.
The server validates before writing: a complete document, at least three slides, the asset links present, or the deck is refused and the old file stands.
Regeneration always overwrites, so a lasting correction belongs on the PAGE, which is what every regeneration reads.

### 4 · What a deck is
**The form**: html-ppt's shell, this board's voice.
```text
  🎨 academic-report theme · T cycles the short gallery
  ⌨️ ← → move · F fullscreen · O overview · S presenter mode
  🗣 every slide carries speaker notes, surfaced by S
  🛡 scripts blocked? a data-js stamp is absent and CSS flattens
     the deck to one fragment-picked slide, so it still reads
```
A deck is six to nine slides: a cover, a closer, and distilled middles built from the page's own emoji, numbers, and quoted rulings.
The deck links at the html-ppt skill's assets by relative path, so a theme improvement reaches every deck with no rebuild.
Nothing from the skill is copied into the board, and the board contributes no CSS of its own.

## Aims
- [x] ✂️ `live/deck.py` retires
      Deleted 260815 with its `/_board/deck` route and the DeckMixin; the ✨ path is the only writer.
- [x] 🗑 `haipipe-page-for-slide` leaves `page-types/`
      Removed 260815; `haipipe-page` 0.26.0 drops the `page-type: slide` key, `plug` refreshed `Design-3`'s title, and `install.sh --global` is owed a re-run.
- [x] 🧾 `QPs2`'s roster drops for-slide
      The hub was swept to the two-kind world the same day; its pre-sweep record is archived whole.
- [x] 👀 A deck needs no acceptance gate (CC ruled under JL's delegation, "check it yourself")
      The presenter is responsible for having read what they present, and regeneration is one click, so a gate would add friction with no consumer; reversible the day a deck misleads someone.

## States
All four aims closed on 260815: three by subtraction (the endpoint, the shipped unit, the hub's roster) and one by ruling.
The surface is proven, not described: `/_board/autodeck` authored a real deck for `QF2-newcomer` on its first live run, and JL's own ✨ click regenerated this page's deck the same evening.

## Files
- `../../board/haipipe-board/live/autodeck.py`
  The ✨ button's server half: prompt, validation, and the computed `<head>`.
- `../../board/haipipe-board/assets/js/10-drawer/70-plugin-slides.js`
  The page panel: derives the deck path, shows it or the pointer, carries ✨ regenerate.
- `../../board/haipipe-board/live/shell.py`
  The Slides tab and its ✨ bar; one loader, cache-busted.
- `../../display/html-ppt/assets/academic-report-extras.css`
  The house style, including the monospace carve-out that keeps ascii figures aligned inside a Times deck.
- `../../../display/html-ppt/`
  The skill that owns what a deck looks like; every deck links at its assets.

## Log
- 260815 1900 · [JL via CC] `haipipe-plugin-slide` drafted under `page-plugins/`, round 2 of the thin-door migration: delta-only over `haipipe-plugin`.
- 260815 2100 · [CHECK-CC, JL delegated] all four aims closed ("you should check it yourself, we will just keep the things with slides like the plugin"): `live/deck.py` + its route deleted; `haipipe-page-for-slide` removed and `haipipe-page` bumped to 0.26.0 (Design-3 re-plugged, title refreshed); `QPs2` swept to the two-kind hub; the acceptance question ruled no-gate by CC under delegation. Same pass: ascii figures inside decks render aligned again, a monospace carve-out in `academic-report-extras.css` where strict Times had crushed them, plus figure-alignment rules in autodeck's prompt.
- 260815 2010 · [REVISE-CC, JL asked] rewritten to the working contract only ("focus on how current slide plugin work"); the dead type's story, the tier history, and the selection record left this page for `_archive/QBt9-for-slide.md` and this Log, where the board keeps history.
- 260815 1930 · [REVISE-CC, JL asked] the ✨ Regenerate button shipped on both doors: `POST /_board/autodeck` runs `claude -p` server-side and writes the deck; deck loads became cache-busted; the display plugin's move (`display/skills/html-ppt` to `display/html-ppt`) was repaired across all decks; the runtime-vs-fallback freeze (only slide 1 visible) was fixed with the `data-js` stamp.
- 260815 1730 · [REVISE-CC, JL ruled] the slide page-type retired ("the slide will just be the plugin version"): every page may have one optional deck in `slide/`; the QBt9 specimen archived whole; the third kind reduced to material after for-skill and for-meeting.
- 260815 1700 · [REVISE-CC, JL ruled] the deck tier collapsed to the AI deck ("We will just have the AI deck"); the browser reflow retired from client and shell; six decks authored the same hour.
