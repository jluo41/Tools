---
name: diagram-ascii-canvas
description: Bundle a folder of ASCII `.txt` diagrams (output of diagram-ascii) into one Excalidraw canvas — screenshots each .txt as a PNG and embeds all of them into a single .excalidraw file laid out in a grid. Use when the user has multiple ASCII diagrams and wants to view them together, rearrange them, or draw connections between them. No re-drawing — just screenshot + embed.
---

# /diagram-ascii-canvas — Bundle ASCII diagrams into one Excalidraw file

**Purpose**: take a directory (or list) of `.txt` ASCII diagrams produced by `diagram-ascii` and assemble them into a single `.excalidraw` file. Each `.txt` is rendered to a PNG via headless Chromium (so emoji are colored correctly) and embedded as an image element in the canvas. A title text element is placed above each image so you can see at a glance which file is which.

The resulting `.excalidraw` opens in Excalidraw / VS Code's Excalidraw extension, where you can drag images around, draw arrows between them, and add notes — without re-drawing anything.

## When to Use

- User has 3+ `.txt` diagrams and asks "put them together", "see how they relate", "make one big canvas"
- After `diagram-ascii` produces multiple files in a folder
- Before a design review where someone wants to gesture across diagrams

## When to Defer

- User wants editable text inside Excalidraw — this skill embeds PNGs, not live text. Editing means changing the `.txt` and re-running.
- Only one diagram — just open the `.txt`, no canvas needed.

## Inputs

| Input | Form |
|---|---|
| A directory of `.txt` files | `path/to/diagrams/` — script picks up `*.txt` |
| Explicit list of files | space-separated `.txt` paths |
| Output path (optional) | defaults to `<input-dir>/canvas.excalidraw` |

## Output

- `canvas.excalidraw` — single file with all diagrams embedded
- `_pngs/` (sibling dir) — intermediate PNGs, kept for re-use / debugging

## How to Run

The skill ships two scripts. Step 1 is always required; step 2 is for sharing.

### 1. Build the canvas

`bin/txt-to-canvas.py` uses `uv` to pull `playwright` on demand; the chromium browser must already be cached (`~/Library/Caches/ms-playwright/chromium-*`).

```bash
# whole directory (auto-splits each .txt at runs of 2+ blank lines)
bin/txt-to-canvas.py path/to/diagrams/

# explicit files + custom output
bin/txt-to-canvas.py a.txt b.txt c.txt --out path/to/big.excalidraw

# tweak gutters (px) — defaults: col 300, row 50
bin/txt-to-canvas.py path/to/diagrams/ --col-gutter 500 --row-gutter 60

# disable section splitting (one PNG per file)
bin/txt-to-canvas.py path/to/diagrams/ --blank-lines 0

# split more aggressively (any 1+ blank line is a section break)
bin/txt-to-canvas.py path/to/diagrams/ --blank-lines 1
```

### Layout: one column per file, sections stacked top→bottom

Reading order on the canvas matches reading order in your folder:

```
┌─ 📄 00-index.txt ─┐  ┌─ 📄 01-repo-layout.txt ─┐  ┌─ 📄 02-… ─┐
│ §1/N · <title>    │  │ §1/N · <title>          │  │ …         │
│ [image]           │  │ [image]                 │  │           │
│                   │  │                         │  │           │
│ §2/N · <title>    │  │ §2/N · <title>          │  │           │
│ [image]           │  │ [image]                 │  │           │
│ …                 │  │ …                       │  │           │
└───────────────────┘  └─────────────────────────┘  └───────────┘
   column = 1 file        column = 1 file              …
```

- **Each column** is one source `.txt` file, with a bold filename header.
- **Each row inside a column** is one section, stacked top→bottom in source order.
- **Each section** has a `§N/TOTAL · <section title>` label above its image. The section title is the first non-blank line of that section.
- Columns aren't height-aligned — files with more sections just go further down. That's intentional and easier to scan than forcing a strict grid.

### Section splitting — explicit `─§` markers only

A file is split into sections **only** at lines that match this marker:

```
─§ Section Title ────────────────────────────────
--§ Section Title ----------------------------------    # ASCII fallback
```

The `§` symbol is the unambiguous trigger. The marker line itself is consumed (not rendered) — only its title is shown above the section's image. Files without any `─§` markers render as **one PNG per file**; the tool does not guess section boundaries from blank lines, box borders, or rule lines, because those over-fire on diagram content.

If you have a marker-less file you don't want to retrofit, opt into a blank-line fallback with `--blank-lines 2` (splits at runs of 2+ blank lines, but only when no markers are present).

See `diagram-ascii` SKILL → "Section dividers" for the canonical convention.

### 2. Share as a clickable URL (optional)

`bin/share-canvas.sh` uploads the `.excalidraw` to a **public GitHub gist** and prints a `https://excalidraw.com/#url=...` link that opens the canvas directly in the browser. Requires `gh` CLI logged in with the `gist` scope.

```bash
bin/share-canvas.sh path/to/canvas.excalidraw [-d "description"]
# prints:
#   gist:       https://gist.github.com/USER/HASH
#   raw:        https://gist.githubusercontent.com/USER/HASH/raw/.../canvas.excalidraw
#   excalidraw: https://excalidraw.com/#url=<raw>     ← click this
```

How it works: Excalidraw's web app accepts a `#url=<remote .excalidraw>` hash param and fetches the scene from that URL. `raw.githubusercontent.com` serves with CORS open, so the gist's raw URL works without any other infra.

**Privacy note**: this creates a **public** gist. Don't share canvases that include sensitive paths, secrets, or internal architecture you wouldn't put in an open-source repo. The PNGs are baked into the JSON as base64 — they're public the moment the gist is created.

## How It Works

1. **Render each `.txt` → PNG** via headless Chromium screenshot of an HTML `<pre>` block (system monospace + emoji fonts).
2. **Measure each PNG** to get its native width/height.
3. **Assemble Excalidraw JSON**:
   - Each PNG → one `image` element + a `text` element above it as a title.
   - Layout is **one column per source `.txt` file** (sections stacked top→bottom inside each column). Columns are spaced by `--col-gutter` (default 300px); sections inside a column by `--row-gutter` (default 50px). Columns are not height-aligned — easier to scan than a strict grid.
   - PNG bytes → base64 → `files` dict keyed by SHA-1.
4. **Write `canvas.excalidraw`** — opens directly in Excalidraw.

## Calling From `diagram-ascii`

`diagram-ascii` should suggest this skill **whenever it has just produced 3+ `.txt` files in the same folder**. Example handoff line:

> 我把这 5 个 diagram 写到了 `examples/foo/`。要把它们拼成一张 Excalidraw 大图吗？(运行 `diagram-ascii-canvas`)

Don't auto-run — confirm first, since the canvas is a downstream artifact the user may not always want.

## Anti-patterns

- Running on a directory with non-diagram `.txt` files — script renders everything matching `*.txt`. Filter the input directory first.
- Editing the embedded PNGs in Excalidraw — they're images; edit the source `.txt` and re-run.
- Re-running without deleting old `_pngs/` — script overwrites by filename, but stale PNGs from removed `.txt` files will linger. Clean `_pngs/` if the input set shrinks.
