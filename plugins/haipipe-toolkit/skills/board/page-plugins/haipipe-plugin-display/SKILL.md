---
name: haipipe-plugin-display
description: >-
  The display/ plugin of a Board page: the page treated as a small paper, shipping figure and table UNITS at <page>/display/<stem>-DisplayN-<slug>/ under the display family's unit contract adopted verbatim. Owns the page-side delta only: the unit address and naming, routing a claim to the right renderer skill by kind, the five-step walk whose accepted: tick is human-only, and the citation move: a unit's id named in the content sentence chips as an evidence card in place, with the > Display: lane as the machine's filing surface. Loads haipipe-plugin for the four-facet contract and never restates it; cites the display family's unit contract and never forks it. Trigger: display plugin, page display, display unit, make a figure for this page, tikz unit, algorithm block, equation float, display tab, evidence card, > Display lane, cite a display, accepted tick, /haipipe-plugin-display.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-17"
  summary: "0.3.0 writes down where a data unit's numbers come from: intake freezes FROM a probe card's proof/ with the card's own sha256, never from the workspace a second time, so staleness is computable and a unit cannot exist before a card has answered."
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
concept     ✒️ tex           haipipe-display-tex               the .tex source
concept     🎨 illustration  haipipe-display-illustration      the prompt + review log
```

The ✒️ row is named after the MECHANISM, not after one package (JL 260816): tikz, an
`algorithm2e` block, and a display equation are one kind, because they share the writer (a
person), the recipe (a hand-authored `.tex` that `float.tex` inputs), and now one skill.
Three names for one mechanism would be the drift.
`haipipe-display-tex` holds that kind's craft, including the rule that such a unit still owes
`assets/figure.pdf`, since a consumer's master rarely carries the author's preamble.

`haipipe-display` is the DOOR over that table (JL 260816): say what you want shown and it picks the renderer, or name the renderer directly when the kind is already clear.
The family retired its poster and slides renderers the same day; a page's talk is the slide plugin's deck, never a display unit.

Data-driven kinds take their numbers ONLY through `intake/` citing the task bank by id — ask once, cite twice (QPf5 §4); a render never invents a value.
Every unit walks the same five steps, and the hands alternate:

```text
① INTAKE 🧑 → ② RENDER ⚙️ → ③ PICK 🧑 → ④ BUILD ⚙️ → ⑤ ACCEPT 🧑
```

Only a person ticks `accepted:` in the unit's README, and a changed `intake/` drops the tick back to ⬜ — acceptance binds the render to the inputs it was accepted with.

## ❄️ Intake · a unit freezes FROM a probe card, never from the workspace

The commonest question about a data-driven unit is where its numbers come from (JL 260817: "是不是 display 可以去 get 这个 probe 里面的东西，然后把 probe 里面的东西复制到 display 那个 folder 去，然后它再去做图?"). Yes, and the path is fixed:

```text
  task folder / shipped run
        │  PROBE pulls, with source · run · sha256 · aggregate: true
        ▼
  probe/PP<NN>-<slug>/proof/<file>          ← the card's own evidence
        │  ① INTAKE copies it, verbatim, and records the SAME sha256
        ▼
  display/<stem>-Display<N>-<slug>/intake/inputs/<file>
        │  ② RENDER reads the frozen copy at run time
        ▼
  assets/table-body.tex · float.tex · preview.pdf
```

**The unit never reaches into the workspace a second time.** The card already crossed the wall and recorded the provenance; a unit that re-pulls the same file is a second, unwitnessed pull that can silently disagree with the card. `intake/manifest.yaml` names the card, the card's state, and the card's own `sha256`, which is what makes staleness COMPUTABLE: if the card re-pulls and the hash moves, the intake is stale and `accepted:` drops back to ⬜.

**A unit may only be created once a card serving it has ANSWERED.** An `intake/` freezes from a `proof/` that does not exist until an answer does, which is why the display unit is created at EVIDENCE and not at OUTLINE or PROBE (`haipipe-page-workflow` §🃏). Until then the plan carries a bare `🖼 owed` mark and no folder: on `QC1-visitlbp` that is 1 of 4 proposed units buildable, because the other three wait on two `planned` cards.

**The recipe TYPES no cell.** `recipe/` reads the frozen intake at run time, so re-running it against the same intake yields the same bytes and a reader can check any printed number against the card's `proof/`. It also fails loudly on a ragged read: `QC1-visitlbp-Display1-control-ladder` caught Stata writing `="771,449"`, where the `=` outside the quote makes a CSV parser split inside the number and deliver 11 cells where 5 were expected.

**A unit names the bullet it serves**, the same backlink a probe card carries (`haipipe-plugin-probe` §↩), in a `serves:` row of its README: the plan was frozen before the unit existed, so the unit points at the plan and never the reverse.

## 🖼 Surface · the strip that shows everything and writes nothing

The right-pane 🖼 tab is `POST /_board/display` (`live/plugview.py`) writing the derived `<stem>-view.html`.
Units lay as a horizontal strip, one filling the pane, snap-shifted right to the next; a chip row names every unit and clicking a chip shifts the strip to it.
Each card shows the README rows, the framed `preview.pdf` (or a 🕳 no-render-yet notice naming which step is missing), and the unit's folder tree with the ⚙️ derived halves marked.
The strip header reports three independently computed counts: **declared** means a unit folder exists, **rendered** means a winning asset and `preview.pdf` both exist, and **accepted** means the README carries a human `accepted: ✅ ...` decision. Folder count is never presented as completed work.
The no-render notice is evidence-driven: it identifies the first missing step among frozen `intake/inputs`, renderer-owned `recipe/`, a winning `assets/` file, `preview.pdf`, and human acceptance. It must not claim that intake or recipe exists merely because the unit folder exists.
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
Inside its own Page, write the bare Page-local id (`Display1`, `Display2`, …); cross-page prose may use the fully qualified `<stem>-DisplayN` id. Both aliases resolve to the same unit and both exporters place that unit once. A backticked id is a code span, and a code span QUOTES instead of chipping.
Naming a ⬜ unit is legal and useful — it binds a pending render, and the chip says what is owed.
Candidate rendering does not wait for release approval: PHI-safe aggregate intake may be rendered for review while a method or provenance Probe remains open. Release and interpretation still require the Probe gates and the separate human `accepted:` decision.
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
