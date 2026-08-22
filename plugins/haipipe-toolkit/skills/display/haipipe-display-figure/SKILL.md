---
name: haipipe-display-figure
description: "Generate publication-quality data plots from experiment results (line/bar/scatter/heatmap/box). Use when user says \"画图\", \"作图\", \"generate figures\", \"paper plots\", or needs data-driven plots for a paper. The plot renderer of the display family; tables are rendered by haipipe-display-table."
argument-hint: "[figure-plan-or-data-path]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "0.2.1"
  last_updated: "2026-07-27"
  summary: "Generate publication-quality data plots from a provenance-bound Display Intake."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Display Figure: Publication-Quality Plots from Experiment Data

Generate the data plots for a paper based on: **$ARGUMENTS**

> **Boundary:** this skill renders **plots only**. For any other display kind
> (tables, diagrams, AI concept art), see the sibling-routing table in
> `../ref/display-unit-output-contract.md`.

## Output: write into a display unit

The plot goes into a `displays/displayNN-<slug>/` unit per the shared contract:
`../ref/display-unit-output-contract.md`.
THIS renderer's row: asset -> `assets/figure.pdf`; rebuild spec -> `recipe/gen_*.py`
(+ `recipe/paper_plot_style.py`).

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
| **Architecture/pipeline diagrams** | ❌ No — manual | Model architecture, data flow diagrams, system overviews. At best can generate a rough TikZ skeleton, but **expect to draw these yourself** using tools like draw.io, Figma, or TikZ |
| **Generated image grids** | ❌ No — manual | Grids of generated samples (e.g., GAN/diffusion outputs). These come from running your model, not from this skill |
| **Photographs / screenshots** | ❌ No — manual | Real-world images, UI screenshots, qualitative examples |

**In practice:** For a typical ML paper, this skill handles the data plots (a large share of the figure set).
Tables go to `haipipe-display-table`; the hero figure / architecture diagram / qualitative results are created via the diagram/illustration skills or manually and placed in `figures/` before running `/haipipe-paper section-edit`.
The skill will detect manually-made figures as "existing figures" and preserve them.

## Constants

- **STYLE = `publication`** — Visual style preset.
  Options: `publication` (default, clean for print), `poster` (larger fonts), `slide` (bold colors)
- **DPI = 300** — Output resolution
- **FORMAT = `pdf`** — Output format.
  Options: `pdf` (vector, best for LaTeX), `png` (raster fallback)
- **COLOR_PALETTE = `tab10`** — Default matplotlib color cycle.
  Options: `tab10`, `Set2`, `colorblind` (deuteranopia-safe)
- **FONT_SIZE = 10** — Base font size (matches typical conference body text)
- **FIG_DIR** — for a paper, the display unit `displays/displayNN-slug/` (plot -> `assets/figure.pdf`, scripts -> `recipe/`).
  Flat `figures/` only with no paper.
- **REVIEWER_MODEL = `gpt-5.5`** — Model used via Codex MCP for figure quality review.

## Inputs

1. **Display contract** — the unit's `README.md` and the paper-stage brief.
2. **Display Intake** — `intake/manifest.yaml` and its approved CSV/JSON snapshot.
3. **Existing candidate** — only when the caller asked to refine that named candidate.

If no display unit or verified Intake exists, stop and ask the caller to create one.

## Workflow

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
import matplotlib.pyplot as plt
import matplotlib
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
    """Save figure to FIG_DIR with consistent naming."""
    fig.savefig(f'{FIG_DIR}/{name}.{fmt}')
    print(f'Saved: {FIG_DIR}/{name}.{fmt}')
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

### Step 4: Generate Each Figure

For the current display unit, create a standalone Python script in `recipe/`:

**Line plots** (training curves, scaling):
```python
# gen_fig2_training_curves.py
from paper_plot_style import *
import json

with open('intake/inputs/exp_results.json') as f:
    data = json.load(f)

fig, ax = plt.subplots(1, 1, figsize=(5, 3.5))
ax.plot(data['steps'], data['fac_loss'], label='Factorized', color=COLORS[0])
ax.plot(data['steps'], data['crf_loss'], label='CRF-LR', color=COLORS[1])
ax.set_xlabel('Training Steps')
ax.set_ylabel('Cross-Entropy Loss')
ax.legend(frameon=False)
save_fig(fig, 'fig2_training_curves')
```

**Bar charts** (comparison, ablation):
```python
from paper_plot_style import *
import pandas as pd

data = pd.read_csv('intake/inputs/comparison.csv')
fig, ax = plt.subplots(1, 1, figsize=(5, 3))
bars = ax.bar(data['method'], data['value'], color=[COLORS[i] for i in range(len(data))])
ax.set_ylabel('Accuracy (%)')
# Add value labels on bars
for bar, val in zip(bars, data['value']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.1f}', ha='center', va='bottom', fontsize=FONT_SIZE-1)
save_fig(fig, 'fig3_comparison')
```

**Comparison / coefficient tables** (LaTeX): out of scope — use `haipipe-display-table`, which owns booktabs rules, significance stars, SE rows, panels, and table notes.
Do not emit `.tex` tables from this skill.

**Architecture/pipeline diagrams** are outside this skill's scope.
Route them to `haipipe-display-diagram` or `haipipe-display-illustration` through the Display stage.

### Step 5: Run All Scripts

```bash
# Run all figure generation scripts
for script in gen_fig*.py; do
    python "$script"
done
```

Verify all output files exist and are non-empty.

### Step 6: Hand Back to the Unit Wrapper

The renderer writes the asset and recipe only. `float.tex` is caller-owned: after the Paper
adapter supplies an approved caption, label, and placement, a renderer may refresh just its asset
reference under the shared contract. It never invents or changes those semantic fields.
Do not create a parallel `latex_includes.tex` file or write an ad hoc figure block in a section.

The Paper adapter places the accepted unit through its existing `float.tex`.

### Step 7: Figure Quality Review with REVIEWER_MODEL

Send figure descriptions and captions to GPT-5.5 for review:

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Review these figure/table plans for a [VENUE] submission.

    For each figure:
    1. Is the caption informative and self-contained?
    2. Does the figure type match the data being shown?
    3. Is the comparison fair and clear?
    4. Any missing baselines or ablations?
    5. Would a different visualization be more effective?

    [list all figures with captions and descriptions]
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

## Output

The display unit layout (approved values -> `intake/inputs/`, asset -> `assets/figure.pdf`,
rebuild recipe -> `recipe/gen_figNN_*.py` + `recipe/paper_plot_style.py`) and the no-paper flat
fallback are the shared contract:
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
| Architecture | System overview | 0.95\textwidth |
| Multi-panel | Combined results (subfigures) | 0.95\textwidth |
