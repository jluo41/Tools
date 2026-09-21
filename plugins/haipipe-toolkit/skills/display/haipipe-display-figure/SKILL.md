---
name: haipipe-display-figure
description: "Generate publication-quality data plots from experiment results (line/bar/scatter/heatmap/box). Use when user says \"画图\", \"作图\", \"generate figures\", \"paper plots\", or needs data-driven plots for a paper. The plot renderer of the display family; tables are rendered by haipipe-display-table."
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "0.2.2"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Display Figure: Publication-Quality Plots from Experiment Data

Generate the data plots for a paper based on: **$ARGUMENTS**

> **Boundary:** this skill renders **plots only**. For any other display kind
> (tables, diagrams, AI concept art), see the sibling-routing table in
> `../ref/display-unit-output-contract.md`.

## Output: write into a display unit

The plot goes directly into the caller-supplied unit directory per the shared
contract: `../ref/display-unit-output-contract.md`. For a Page DISPLAY Result,
the caller supplies `<page>/results/<re-run>/payload/<unit>/`; a View or other
caller supplies its own unit path. This renderer never chooses or creates a
parallel destination.
THIS renderer's row: asset -> `assets/figure.pdf`; rebuild spec -> `recipe/gen_*.py`
(+ `recipe/paper_plot_style.py`).

One invocation that produces one bounded display unit may be one Run in the parent Workflow.
The numbered steps, script calls, compilation, review, and retries are internal Steps; separate
units with independent receipts are separate Runs.

For a new unit, read `intake/manifest.yaml` before doing anything else.
The plot script reads only the manifest's approved `intake/inputs/` snapshot.
It never searches a task folder, re-derives values, or chooses rows from an arbitrary result file.
Legacy `source/` units remain valid only through the compatibility path in the shared contract.

## Scope: What This Skill Can and Cannot Do

| Category | Can auto-generate? | Examples |
|----------|-------------------|----------|
| **Data-driven plots** | ✅ Yes | Line plots (training curves), bar charts (method comparison), scatter plots, heatmaps, box/violin plots |
| **Comparison tables** | ➡️ Use `haipipe-display-table` | LaTeX tables (prior bounds, method features, ablation) now live in the dedicated table renderer |
| **Multi-panel figures** | ✅ Yes | Subfigure grids combining multiple plots (e.g., 3×3 dataset × method) |
| **Architecture/pipeline diagrams** | ➡️ Route to `haipipe-display-diagram` | Model architecture, data flow diagrams, system overviews, and deterministic box-and-arrow schematics |
| **Generated image grids** | ❌ No — manual | Grids of generated samples (e.g., GAN/diffusion outputs). These come from running your model, not from this skill |
| **Photographs / screenshots** | ❌ No — manual | Real-world images, UI screenshots, qualitative examples |

**In practice:** For a typical paper, this skill handles data plots. Tables go to
`haipipe-display-table`; architecture diagrams go to `haipipe-display-diagram`; qualitative concept
art goes to `haipipe-display-illustration`. Each result stays in the caller-supplied display unit.
This renderer never writes to a flat `figures/` directory.

## Constants

- **STYLE = `publication`** — Visual style preset.
  Options: `publication` (default, clean for print), `poster` (larger fonts), `slide` (bold colors)
- **DPI = 300** — Output resolution
- **FORMAT = `pdf`** — Output format.
  Options: `pdf` (vector, best for LaTeX), `png` (raster fallback)
- **COLOR_PALETTE = `tab10`** — Default matplotlib color cycle.
  Options: `tab10`, `Set2`, `colorblind` (deuteranopia-safe)
- **FONT_SIZE = 10** — Base font size (matches typical conference body text)
- **Output directory** — `assets/` for the active render; `candidates/` when `DISPLAY_CANDIDATE=<id>` is set. Generation scripts live in `recipe/`. The default final asset is `figure.pdf`; when `FORMAT = 'png'`, use `figure.png` and update the wrapper reference.
- **REVIEWER_MODEL = `gpt-5.5`** — Model used via Codex MCP for figure quality review.

## Inputs

1. **Display contract** — the unit's `README.md` and caller brief.
2. **Display Intake** — `intake/manifest.yaml` and its approved CSV/JSON snapshot.
3. **Existing candidate** — only when the caller asked to refine that named candidate.

If no display unit or verified Intake exists, stop and ask the caller to create one.

## Procedure

A caller-directed invocation that produces one bounded display unit is one Run in its parent's
Workflow. The numbered steps, generation scripts, candidate iterations, compilation, and review stay
inside that Run.

### Step 1: Read the Unit Brief and Intake

Read the unit `README.md` for the claim, audience, caption intent, and target section.
Then read `intake/manifest.yaml` and verify the declared snapshot hash before plotting.
The Display stage, not this renderer, already decided the figure plan and form.

If the manifest has no `role: values` source, stop and route a concept visual to the diagram or
illustration renderer instead.

### Step 2: Set Up Plotting Environment

Create a shared style configuration script:

```python
# paper_plot_style.py — shared across all figure scripts
from pathlib import Path
import os
import re
import matplotlib.pyplot as plt
import matplotlib
UNIT = Path(__file__).resolve().parents[1]
CANDIDATE_ID = os.environ.get('DISPLAY_CANDIDATE', '').strip()
if CANDIDATE_ID and not re.fullmatch(r'[A-Za-z0-9_-]+', CANDIDATE_ID):
    raise ValueError('DISPLAY_CANDIDATE must contain only letters, digits, _ or -')
FIG_DIR = UNIT / ('candidates' if CANDIDATE_ID else 'assets')
FIG_DIR.mkdir(parents=True, exist_ok=True)
FONT_SIZE = 10
DPI = 300
FORMAT = 'pdf'
matplotlib.rcParams.update({
    'font.size': FONT_SIZE,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
    'axes.labelsize': FONT_SIZE,
    'axes.titlesize': FONT_SIZE + 1,
    'xtick.labelsize': FONT_SIZE - 1,
    'ytick.labelsize': FONT_SIZE - 1,
    'legend.fontsize': FONT_SIZE - 1,
    'figure.dpi': DPI,
    'savefig.dpi': DPI,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'text.usetex': False,  # set True if LaTeX is available
    'mathtext.fontset': 'stix',
})

# Color palette
COLORS = plt.cm.tab10.colors  # or Set2, or colorblind-safe

def save_fig(fig, name, fmt=FORMAT):
    """Write the active asset or a named candidate without replacing the other."""
    stem = f'{CANDIDATE_ID}-{name}' if CANDIDATE_ID else name
    path = FIG_DIR / f'{stem}.{fmt}'
    fig.savefig(path)
    print(f'Saved: {path}')
```

### Step 3: Auto-Select Figure Type

Use this decision tree for data-driven figures (inspired by Imbad0202/academic-research-skills):

| Data Pattern | Recommended Type | Size |
|-------------|-----------------|------|
| X=time/steps, Y=metric | Line plot | 0.48\textwidth |
| Methods × 1 metric | Bar chart | 0.48\textwidth |
| Methods × multiple metrics | Grouped bar / radar | 0.95\textwidth |
| Two continuous variables | Scatter plot | 0.48\textwidth |
| Matrix / grid values | Heatmap | 0.48\textwidth |
| Distribution comparison | Box/violin plot | 0.48\textwidth |
| Multi-dataset results | Multi-panel (subfigure) | 0.95\textwidth |
| Prior work comparison / coefficients | (table) → use `haipipe-display-table` | — |

### Step 4: Generate the Unit's Figure

For each display unit, create one active standalone Python generator in `recipe/`. A multi-panel
figure is assembled by that script into one asset. Separate figures use separate caller-supplied
units; candidate variations go in `candidates/` instead of overwriting the active asset.

**Line plots** (training curves, scaling):
```python
# gen_fig2_training_curves.py
from paper_plot_style import *
import json

with open(UNIT / 'intake/inputs/exp_results.json') as f:
    data = json.load(f)

fig, ax = plt.subplots(1, 1, figsize=(5, 3.5))
ax.plot(data['steps'], data['fac_loss'], label='Factorized', color=COLORS[0])
ax.plot(data['steps'], data['crf_loss'], label='CRF-LR', color=COLORS[1])
ax.set_xlabel('Training Steps')
ax.set_ylabel('Cross-Entropy Loss')
ax.legend(frameon=False)
save_fig(fig, 'figure')  # -> assets/figure.pdf
```

**Bar charts** (comparison, ablation):
```python
from paper_plot_style import *
import pandas as pd

data = pd.read_csv(UNIT / 'intake/inputs/comparison.csv')
fig, ax = plt.subplots(1, 1, figsize=(5, 3))
bars = ax.bar(data['method'], data['value'], color=[COLORS[i] for i in range(len(data))])
ax.set_ylabel('Accuracy (%)')
# Add value labels on bars
for bar, val in zip(bars, data['value']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.1f}', ha='center', va='bottom', fontsize=FONT_SIZE-1)
save_fig(fig, 'figure')  # -> assets/figure.pdf
```

**Comparison / coefficient tables** (LaTeX): out of scope — use `haipipe-display-table`, which owns booktabs rules, significance stars, SE rows, panels, and table notes.
Do not emit `.tex` tables from this skill.

**Architecture/pipeline diagrams** are outside this skill's scope.
Route deterministic diagrams to `haipipe-display-diagram`; route qualitative concept art to
`haipipe-display-illustration`. Both use the same caller-supplied display unit.

### Step 5: Run the Active Recipe or a Named Candidate Recipe

```bash
UNIT_DIR=/path/to/caller-supplied-unit
# Normal render: run the single active generator.
python "$UNIT_DIR/recipe/gen_fig2_training_curves.py"
```

Keep one active generator per unit. For an explicit comparison, copy it to a candidate-suffixed
recipe, edit that copy for the proposed variant, and run only that recipe with a candidate id:

```bash
cp "$UNIT_DIR/recipe/gen_fig2_training_curves.py" "$UNIT_DIR/recipe/gen_fig2_training_curves-A.py"
DISPLAY_CANDIDATE=A python "$UNIT_DIR/recipe/gen_fig2_training_curves-A.py"
```

The style helper writes `candidates/A-figure.pdf` (or `.png` when raster output is selected).
Inspect that candidate file itself; do not use the unit's existing `preview.pdf` for it. After the
caller selects a candidate, promote it to the matching `assets/figure.pdf` or `assets/figure.png`,
update the wrapper reference if needed, and rebuild the canonical unit preview.

Verify all output files exist and are non-empty.

Compile and inspect the unit preview from the caller's asset-reference base:

```bash
WORK_ROOT=/path/to/caller-asset-reference-base
(cd "$WORK_ROOT" && pdflatex -output-directory "$UNIT_DIR" "$UNIT_DIR/preview.tex")
```

Open `preview.pdf` and check clipping, legibility, and the caption/asset pairing.
If compilation fails or the preview has a visible defect, return `HOLD` with the
error or defect and keep the unit unaccepted.

### Step 6: Hand Back to the Unit Wrapper

For one caller-directed render, the renderer writes the selected asset and recipe into the unit but
does not mark it accepted. When the caller requests competing candidates, keep alternatives under
`candidates/` until the caller selects one. `float.tex` is caller-owned: after the caller supplies
an approved caption, label, and placement, a renderer may refresh just its asset reference under
the shared contract. It never invents or changes those semantic fields.
Do not create a parallel `latex_includes.tex` file or write an ad hoc figure block in a section.

The caller or its adapter consumes the selected unit through its existing
`float.tex`. The renderer never records `accepted:`.

### Step 7: Figure Quality Review with REVIEWER_MODEL

Send the compiled preview together with its claim and caption to GPT-5.5 for an
advisory visual and editorial review. In candidate mode, attach the asset or
candidate-named preview for that id, not the unit's existing `preview.pdf`. Review the actual
rendered figure, not a plan alone; the caller remains responsible for semantic
accuracy and acceptance.

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Review this compiled data figure for a [VENUE] submission.

    Check the visible labels, scale, legend, comparison, and fit at paper size.
    Also check whether the claim and caption describe what the rendered data
    actually show. Flag issues; do not treat a score as acceptance.

    [attach the matching active preview or candidate asset/preview and include the approved claim and caption]
```

### Step 8: Quality Checklist

Before finishing, verify each figure (from pedrohcgs/claude-code-my-workflow):

- [ ] Font size readable at printed paper size (not too small)
- [ ] Colors distinguishable in grayscale (print-friendly)
- [ ] **No title inside figures** — titles go only in LaTeX `\caption{}` (from pedrohcgs)
- [ ] Legend does not overlap data
- [ ] Axis labels have units where applicable
- [ ] Axis labels are publication-quality (not variable names like `emp_rate`)
- [ ] Figure width fits single column (0.48\textwidth) or full width (0.95\textwidth)
- [ ] PDF output is vector (not rasterized text)
- [ ] No matplotlib default title (remove `plt.title` for publications)
- [ ] Serif font matches paper body text (Times / Computer Modern)
- [ ] Colorblind-accessible (if using colorblind palette)
- [ ] Compiled `preview.pdf` opened and inspected; any compile or visual failure is a HOLD

## Output

The display unit layout (approved values -> `intake/inputs/`, asset -> `assets/figure.pdf`,
rebuild recipe -> `recipe/gen_figNN_*.py` + `recipe/paper_plot_style.py`) is the shared contract:
`../ref/display-unit-output-contract.md`.

## Figure Type Reference

| Type | When to Use | Typical Size |
|------|------------|--------------|
| Line plot | Training curves, scaling trends | 0.48\textwidth |
| Bar chart | Method comparison, ablation | 0.48\textwidth |
| Grouped bar | Multi-metric comparison | 0.95\textwidth |
| Scatter plot | Correlation analysis | 0.48\textwidth |
| Heatmap | Attention, confusion matrix | 0.48\textwidth |
| Box/violin | Distribution comparison | 0.48\textwidth |
| Architecture | ➡️ Use `haipipe-display-diagram` | — |
| Multi-panel | Combined results (subfigures) | 0.95\textwidth |
