---
name: haipipe-plugin-display
description: >-
  The display/ plugin of a Board page: the page treated as a small paper, shipping figure and table UNITS at <page>/display/<stem>-DisplayN-<slug>/ under the display family's unit contract adopted verbatim. Owns the page-side delta only: the unit address and naming, routing a claim to the right renderer skill by kind, the five-step walk whose accepted: tick is human-only, and the citation move: a unit's id named in the content sentence chips as an evidence card in place, with the > Display: lane as the machine's filing surface. Loads haipipe-plugin for the four-facet contract and never restates it; cites the display family's unit contract and never forks it. Trigger: display plugin, page display, display unit, make a figure for this page, tikz unit, display tab, evidence card, > Display lane, cite a display, accepted tick, /haipipe-plugin-display.
metadata:
  version: "0.1.2"
  last_updated: "2026-08-16"
  summary: "The projections inherit the citation (JL 260816): latex and word both embed a cited unit after its citing paragraph."
---
# /haipipe-plugin-display · the page as a small paper, its figures as accepted units

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only display's delta: where a unit lives on a PAGE, which renderer makes it, and how a sentence cites it.
The unit's internal shape is NOT defined here: `skills/display/ref/display-unit-output-contract.md` is adopted verbatim (QPf5, ruled JL 260815), and this skill cites it the way `haipipe-plugin-latex` cites `md2tex.py` — a caller, never a fork.

## 🗂 Storage · one unit per folder, the paper contract at a page address

```text
<page>/display/
└── <stem>-Display<N>-<slug>/     the unit, named by the page's stem
    ├── README.md                 claim · kind · accepted: — the human gate lives here
    ├── intake/                   🧑 manifest.yaml + small approved extracts
    ├── recipe/                   🎨 renderer-owned script, spec, receipts
    ├── float.tex                 the unit test: the float a citing page would \input
    ├── preview.tex ▶ preview.pdf ⚙️ the standalone look the tab frames
    ├── assets/                   ⚙️ the WINNING render
    └── candidates/ · versions/   ⚙️ the also-rans and the history
```

The kind is MIXED, and the split runs through the unit: `intake/`, `recipe/`, `float.tex`, `README.md` are PRIMARY originals; `preview.pdf`, `assets/`, `candidates/`, `versions/` are regenerable from them.
What of the derived half is committed is QPf5's open Decision Now row (default ⭐B: sources + `assets/` + `float.tex` in, previews and candidates ignored) — read the row there, this file does not rule it.
The address delta a fresh agent must know: the renderer skills speak PAPER addresses (`displays/displayNN-slug/`, a paper root, the lifecycle gallery); on a page the unit lives at `<page>/display/`, `preview.tex` compiles standalone from the unit folder, and no paper root exists or is walked for.

## ✍️ Writer · a family routed by kind, and a gate no machine may tick

Display is the first plugin whose writer is not one endpoint but a ROUTING DECISION: the claim's kind picks the renderer skill, and the renderer owns `recipe/` end to end.

```text
driven by   kind             renderer                          recipe holds
──────────────────────────────────────────────────────────────────────────────
data        📊 table         haipipe-display-table             the build script
data        📈 figure        haipipe-display-figure            the python + receipts
concept     📐 diagram       haipipe-display-diagram           the FigureSpec JSON → SVG
concept     ✒️ tikz          TeX-native, authored directly     the .tikz.tex source
concept     🎨 illustration  haipipe-display-illustration      the prompt + review log
```

Data-driven kinds take their numbers ONLY through `intake/` citing the task bank by id — ask once, cite twice (QPf5 §4); a render never invents a value.
Every unit walks the same five steps, and the hands alternate:

```text
① INTAKE 🧑 → ② RENDER ⚙️ → ③ PICK 🧑 → ④ BUILD ⚙️ → ⑤ ACCEPT 🧑
```

Only a person ticks `accepted:` in the unit's README, and a changed `intake/` drops the tick back to ⬜ — acceptance binds the render to the inputs it was accepted with.

## 🖼 Surface · the strip that shows everything and writes nothing

The right-pane 🖼 tab is `POST /_board/display` (`live/plugview.py`) writing the derived `<stem>-view.html`.
Units lay as a horizontal strip, one filling the pane, snap-shifted right to the next; a chip row names every unit and clicking a chip shifts the strip to it.
Each card shows the README rows, the framed `preview.pdf` (or a 🕳 no-render-yet notice naming which step is missing), and the unit's folder tree with the ⚙️ derived halves marked.
An empty `display/` renders the contract's ghost scaffold, so an empty tab teaches the unit shape instead of showing a blank.
The surface is read-only by contract: renderers write `recipe/` and `assets/`, a person rules `intake/` and the tick, the pane writes nothing.

## 📎 Citation · a unit is evidence, and the citation lives in the sentence

What no other plugin has: a display unit is an EVIDENCE CARD the page's own prose cites.
The citation's home is the SENTENCE (JL 260816): name the unit's short id in the prose where the claim lives, and it chips as the evidence card in place:

```text
Steps ① ③ ⑤ are a person's and steps ② ④ are machinery
— the split of hands QPf5-Display1 draws.
                     └────🖼 chip────┘
```

The `> Display:` lane under a sentence is the FILING surface, kept for two cases: a machine appending evidence writes a lane and never edits prose, and a binding no sentence carries naturally lands there rather than clotting the line.
`dialect: paper` (`src/dialect_paper.py`) indexes every `<page>/display/*/float.tex` under the board and renders either surface as a chip card — owed, STALE, candidate, or ok — linking to the unit; a chip landing as `#<unit-id>` shifts the 🖼 strip to that card.
Write the bare short id: a backticked id is a code span, and a code span QUOTES instead of chipping.
Naming a ⬜ unit is legal and useful — it binds a pending render, and the chip says what is owed.
THE PROJECTIONS INHERIT THE CITATION (JL 260816): the latex export embeds a cited unit as a real float after the citing paragraph (the winning asset, the unit's own caption and label), and the word export embeds the rasterized figure with the inline `(Figure n)` and a 🖼 Display comment on the sentence — the per-projection mechanics are `haipipe-plugin-latex`'s and `haipipe-plugin-word`'s rows, not this file's.

## 📂 Files

- `../../../display/ref/display-unit-output-contract.md`
  The unit's internal shape; adopted verbatim, never forked.
- `../../haipipe-board/live/plugview.py`
  The 🖼 surface: strip, chips, trees, ghost scaffold; read-only.
- `../../haipipe-board/src/dialect_paper.py`
  The citation index: `<page>/display/*/float.tex` → evidence chips.
- `../../haipipe-board/assets/js/10-drawer/84-plugin-evidence.js`
  The drawer registration: the Plugin ▾ rows for 🖼 Display and 🚪 Probe.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.
