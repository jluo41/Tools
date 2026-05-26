---
name: figure-planner
description: Orchestrate manuscript display design end-to-end inside a paper's `0-display/` folder. One `.txt` per figure carries both the spec metadata header (label, location, source, status, claim, caption, what-it-shows, notes) AND the emoji-rich ASCII sketch body. Bundles them into one Excalidraw canvas via /diagram-ascii-canvas, and embeds existing result PNGs from `0-display/Figure/` (and `0-display/AppendixFigure/`) so spec + sketch + real image sit side-by-side. Use when designing, restructuring, or auditing a paper's displays.
---

# /figure-planner — Orchestrator for `0-display/_design/`

**Anchor**: this skill always operates inside a paper's `0-display/` folder. Per-figure `.txt` files, the index, and the final Excalidraw canvas all live in `0-display/_design/`. Existing result PNGs in sibling `0-display/Figure/` and `0-display/AppendixFigure/` are referenced by the `.txt` files and embedded into the canvas.

```
<paper>/
├── 0-display/
│   ├── Figure/                  ← existing main-paper PNGs (results)
│   ├── AppendixFigure/          ← existing appendix PNGs
│   ├── Table/                   ← existing .tex tables (no _design entries)
│   ├── AppendixTable/
│   └── _design/                 ← THIS SKILL OPERATES HERE
│       ├── 00-index.txt         ← claims-to-displays matrix + ordering
│       ├── fig-<label>.txt      ← spec header + ASCII sketch per figure
│       ├── canvas.excalidraw    ← bundled gallery (the deliverable)
│       └── _pngs/               ← intermediate PNG renders (gitignored)
```

**File convention** — *one `.txt` per display, no `.md` cards*. Each per-figure `.txt` is the single source of truth: spec metadata as a header block, ASCII sketch as the body, real-result PNG reference as a trailer marker. Plain text keeps monospace alignment for the sketch and lets `/diagram-ascii-canvas` render it as a PNG inside the gallery.

Tables get no `_design` entries — their spec already lives in the LaTeX caption + the section `.tex`. The canvas gallery is figures-only.

## When to Use

- Designing a paper's display set from scratch
- Auditing or restructuring an existing display set
- Reviewing displays before submission (claim coverage, orphan check)
- Producing a single navigable Excalidraw gallery of all displays for review

Do not use for:
- Final visual styling of individual PNGs (use the underlying plotting code)
- Manuscript-wide claim restructuring beyond the displays (use `/manuscript-optimizer`)

## Core Rule

Each main figure should earn its place by carrying ONE dominant claim. If a figure cannot be summarized by one clean sentence, either split it, demote part of it to the supplement, or rewrite the figure around a clearer claim.

## Pipeline (3 steps)

```
1. WRITE             2. BUNDLE              3. EMBED
─────────            ──────────             ──────────
fig-<label>.txt   →  canvas.excalidraw   →  real PNGs patched
(spec header +       (one column per         into the canvas
 ASCII sketch +      .txt) via /diagram-     via inject-
 REAL PNG marker)    ascii-canvas (REBUILD)  existing-pngs.py
in _design/                                  (Step 3a)
```

### Step 1 — WRITE the per-figure `.txt`

For every figure in the paper (main + appendix), write one `.txt` file inside `0-display/_design/`. Naming:

- `fig-<label-suffix>.txt` for `\label{fig:<label-suffix>}`

Each `.txt` has two zones — a metadata header followed by the ASCII sketch body. Plain text keeps the sketch monospaced; the header is parsed by the inject helper to find the real PNG.

Template:

```
============================================================
 <Display ID>  —  <short title>                  [STATUS · CLAIM]
============================================================

 📂 Label:     <latex label>
 📍 Location:  §X.Y   (0-sections/<filename>.tex)
 📊 File:      0-display/Figure/<filename>.png    ← if Wired
 📦 Source:    <analysis pipeline path>
 ✅ Status:    Wired | Orphan | Planned
 🏷  Supports:  <claim tag(s)>

────────────────────────────────────────────────────────────
 CAPTION
────────────────────────────────────────────────────────────

  "<caption verbatim from .tex>"

────────────────────────────────────────────────────────────
 SKETCH
────────────────────────────────────────────────────────────

  <emoji-rich ASCII rendering of the panels, axes, annotations>

────────────────────────────────────────────────────────────
 WHAT IT SHOWS
────────────────────────────────────────────────────────────

  <one-paragraph narrative of the visual argument>

────────────────────────────────────────────────────────────
 NOTES / TODOS
────────────────────────────────────────────────────────────

  <open items, framing TODOs, companion displays>

📌 REAL PNG: ../Figure/<filename>.png   ← inject-existing-pngs target
```

The trailing `📌 REAL PNG: <relpath>` line (relative to the `.txt` file) is the anchor the inject helper uses. Multi-panel composites can list multiple `📌 REAL PNG:` markers; each becomes one image element under the column.

Plus the maintained `00-index.txt` file at the folder root, listing all displays in reading order with claim tags. The order in `00-index.txt` IS the canvas column order.

Use `/diagram-ascii` conventions for the SKETCH body:
- emoji-rich (load-bearing — do not strip)
- emoji as the primary visual scaffolding
- prefer alignment over decoration

### Step 2 — BUNDLE (canvas via /diagram-ascii-canvas)

Use REBUILD mode:

```bash
$DIAGRAM_CANVAS/bin/txt-to-canvas.py 0-display/_design/ \
    --out 0-display/_design/canvas.excalidraw
```

Where `$DIAGRAM_CANVAS` resolves to the `diagram-ascii-canvas` skill directory (look it up at runtime via the skill registry; do not hardcode).

REBUILD is correct for stable display sets — the canvas is regenerated from `.txt` sources each run. Manual annotations DO NOT survive a rebuild; if reviewers add sticky notes/arrows, save them to a sibling `canvas-annotated.excalidraw` and only rebuild the spec canvas. APPEND mode is wrong here — display sets are stable, not accreting.

The script reads `.txt` files in folder order. `00-index.txt`'s display ordering should match the `.txt` file naming so columns appear in claim-logical order in the canvas.

### Step 3 — EMBED (existing PNGs into the canvas)

After the canvas builds, the Excalidraw file contains one image element per `.txt` (rendered from the ASCII). To get the **actual result PNGs from `0-display/Figure/`** into the same canvas underneath their spec column, do ONE of:

**(3a) Recommended — patch via helper.** Run the bundled helper:

```bash
$FIGURE_PLANNER/bin/inject-existing-pngs.py 0-display/_design/canvas.excalidraw
```

It scans `_design/fig-*.txt` for `📌 REAL PNG: <relpath>` markers (and falls back to the `📊 File:` header), finds the matching column (anchor = column whose top text contains the `.txt` filename), and appends each real PNG as an `image` element under that column with a `📷 RESULT · <filename>` text label. Multi-panel figures with several `📌 REAL PNG:` markers inject each panel sequentially.

**(3b) Manual fallback — drag-drop.** Open `canvas.excalidraw` in Excalidraw or the VS Code extension, then drag-drop each real PNG from `0-display/Figure/` next to its spec column. This is one-time setup; subsequent rebuilds wipe it (use 3a if you rebuild often).

Result: each canvas column shows `[card title] / [ASCII sketch PNG] / [📷 real result PNG]` stacked top-to-bottom.

## Panel Roles

Assign each panel one primary role before writing the legend or Results paragraph:

- claim-supporting evidence
- methodological bridge or definition
- validation under a new regime
- ranking or benchmark comparison
- translational or practical consequence
- case illustration
- failure mode or limitation

Do not let one panel pretend to do three jobs at once.

## Main Figure vs. Supplement

Keep in main figures:
- panels required to establish the core claim
- the key comparison readers must see immediately
- panels defining a new metric or decomposition when that definition is part of the argument

Move to the supplement (`AppendixFigure/`):
- robustness variants
- denser method-by-method comparisons
- extended cases
- secondary ablations

## Legend Rules

Each legend should:
- define the role of each panel
- preserve the key quantitative anchors omitted from compressed main text
- stay consistent with panel letters, metrics, datasets, baselines
- avoid interpretation stronger than the plotted evidence

## Visual Hygiene Pass

After the figure logic is stable:
- consistent figure-internal fonts close to manuscript reading scale
- prefer vector graphics for plots/diagrams/schematics
- restrained palette; same category in same color family
- trim dead margins
- keep arrow direction and symbol conventions consistent

## Orphan Reconciliation

Any PNG in `0-display/Figure/` or `0-display/AppendixFigure/` that has no `\includegraphics` reference in `0-sections/*.tex` is an **orphan**. The figure `.txt` MUST set `✅ Status: Orphan` in the header and the NOTES section MUST resolve it before submission to one of:

- **WIRE**: add `\includegraphics{...}` + `\label{...}` + `\caption{...}` in the right section file
- **DELETE**: remove the PNG and the figure `.txt` (or keep `.txt` with `Status: Deleted` for audit trail)
- **DEFER**: park as supplement-only or companion-note material

## Common Failure Modes

- one figure trying to carry multiple unrelated claims
- panel order following plotting chronology instead of argument logic
- methodological bridge panels described as generic motivation
- Results text claiming something the legend or panel does not support
- supplementary figures cited too vaguely when one panel is doing the real work
- PNGs in `0-display/Figure/` with no matching `fig-*.txt` in `_design/` (drift)
- `fig-*.txt` with `Status: Wired` but no actual `\includegraphics` in the .tex (false-wired)

## Output Standard

When using this skill, produce:
- one `fig-<label>.txt` per figure in `0-display/_design/` (spec header + ASCII sketch + REAL PNG marker)
- `00-index.txt` listing all figures in reading order with claim tags
- `canvas.excalidraw` bundled gallery
- real PNGs injected via `inject-existing-pngs.py` (Step 3a)
- orphan list resolved (each PNG wired, deleted, or deferred)

## Companion Skills

- `/diagram-ascii` — conventions for the emoji-rich ASCII sketch body inside each `fig-*.txt`
- `/diagram-ascii-canvas` — bundles `.txt` into Excalidraw (Step 2); REBUILD mode for stable display sets
- `/manuscript-optimizer` — when display restructuring exceeds the figures themselves
- `/paper-claim-audit` — verify the numbers in each card match raw result files

## Anti-Patterns

- Editing `code/haifn/` figure-generation code from this skill — that's the analysis layer, not the display-design layer
- Adding new figures here without a matching `\includegraphics` plan — orphans accumulate
- Hand-writing `canvas.excalidraw` JSON — always rebuild from `.txt` files via Step 2
- Running this skill outside a `0-display/_design/` folder — the orchestration is anchored to that path
