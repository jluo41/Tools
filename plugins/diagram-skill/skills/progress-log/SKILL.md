---
name: progress-log
description: Image-heavy Markdown progress reports for recording experiment status and sharing with teammates. Use when the user wants to log a run, record progress, or share a visual update. Output is a .md file with minimal text and embedded PNG/SVG figures, including side-by-side layouts. Renders natively in VS Code preview, GitHub, GitLab — no build step. For pure-ASCII sketches inside the log, invoke the diagram-ascii skill.
---

# /progress-log — Image-Heavy Markdown Progress Reports

**Purpose**: record and share progress on experiments / runs / projects. **Few words, many figures.** Opens in VS Code (Cmd+Shift+V preview) or any Markdown viewer — no tooling, no build step.

## When to Use
- Recording progress on an experiment, run, or project
- Sharing visual status with teammates
- Consolidating figures from multiple runs into one chronological log
- Quick visual update after each major step

## When to Defer
- Need runnable code + outputs → Jupyter (`.ipynb`)
- Need captions, numbering, PDF export → Quarto (`.qmd`)
- Need interactive plots / dashboards → HTML
- Pure ASCII sketch only → `diagram-ascii`

## Output

- **Filename convention**: `progress-YYYY-MM-DD.md` or `progress-<topic>.md`.
- **Rendering**: VS Code Markdown preview (Cmd/Ctrl+Shift+V), GitHub/GitLab web, any `.md` viewer — native, no extensions required.

## Save Location

- **User specifies the path when invoking this skill.** Example: *"log today's run to `examples/hainn-v0319/progress/progress-2026-04-24.md`"*.
- If no path given: default to CWD, confirm with user before writing.
- If only a directory given: use a `progress-YYYY-MM-DD.md` filename with today's date.
- **Figures go in a `figs/` subfolder next to the `.md`** (e.g. `.../progress/figs/loss.png`). Always use relative paths in the markdown (`./figs/loss.png`).

## Core Principle — Few Words, Many Images

Every entry is figure-first. Text only for:
- What the figure shows (1 sentence)
- What it means (1 sentence)
- Next step (1 sentence, optional)

Aim for **<50 words of prose per figure block.**

## Layout Patterns

### Single figure
```markdown
## 2026-04-24 — Loss stabilized

![loss curve](figs/loss.png)

AUC 0.82 at epoch 20. Adding dropout next.
```

### Side-by-side — markdown table trick (preferred)
```markdown
| Loss | ROC |
|---|---|
| ![](figs/loss.png) | ![](figs/roc.png) |
```
Renders two-column in VS Code / GitHub / GitLab with no HTML.

### Three-up grid
```markdown
| Train | Val | Test |
|---|---|---|
| ![](figs/train.png) | ![](figs/val.png) | ![](figs/test.png) |
```

### HTML fallback (when you need explicit sizing / centering)
```markdown
<p align="center">
  <img src="figs/loss.png" width="48%" />
  <img src="figs/roc.png" width="48%" />
</p>
```
Use only if the table trick doesn't give enough control.

## Daily Log Template

```markdown
# 🧪 <experiment-name> — progress log

## 2026-04-24

### ✅ Training stabilized
| Loss | ROC |
|---|---|
| ![](figs/loss.png) | ![](figs/roc.png) |

Plateau at epoch 15, AUC 0.82.

### ⏳ Eval sweep
![sweep](figs/sweep.png)

Running over 5 seeds — 3 done.

---

## 2026-04-23

### ✅ Data load
![dist](figs/data-dist.png)

N=12k patients, 80/10/10 split.
```

## Embedding ASCII Sketches

When a figure is conceptual (architecture, flow) rather than data, skip the PNG — inline an ASCII block:

````markdown
### System flow
```text
+----------+     +----------+     +----------+
| 📥 Load  |---->| 🧠 Train |---->| 📊 Eval  |
+----------+     +----------+     +----------+
```
````

For production ASCII, use the `diagram-ascii` skill to generate the block.

## Naming & Organization

- Figures in `figs/` subfolder next to the `.md` file
- Descriptive filenames: `loss-epoch50.png`, `roc-val.png` — not `fig1.png`
- One `.md` per experiment per day, or per milestone (user's call)
- Prefer PNG / SVG over JPG (sharper for plots / diagrams)
- Use relative paths (`./figs/loss.png`), not absolute

## Light Rules

- Keep prose tight: **1–3 short sentences per figure**
- Date-stamp each entry so the log reads chronologically (newest on top)
- Emoji status markers in headings help scanning: ✅ done · ⏳ running · ❌ failed · 🚩 issue
- Always open VS Code preview (Cmd/Ctrl+Shift+V) after writing — confirm images load and layout renders

## See Also

- `diagram-ascii` — generates ASCII sketches to embed as ```` ```text ```` blocks inside the log
- `diagram-drawio` / `diagram-excalidraw` — author diagrams, export to PNG, then embed via the layout patterns above
