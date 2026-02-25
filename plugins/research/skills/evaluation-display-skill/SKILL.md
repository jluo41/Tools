Skill: evaluation-display-skill
================================

Generate evaluation scripts for creating paper tables and figures from model results.

---

Overview
========

This skill helps create Python scripts in `evaluation/scripts/` that:

1. Read model results from CSV (step 0 output)
2. Perform analysis (breakdowns, comparisons, aggregations)
3. Generate tables (LaTeX) or figures (PDF/PNG)
4. Copy outputs to `0-display/` for paper inclusion

**The Pipeline:**

```
1-config.yaml → scripts/X-script.py → results/0-convert-.../metrics.csv
                                    ↓
                         results/X-script/*.pdf
                                    ↓
                         0-display/Figure/ or Table/
```

**Key Benefits:**
- Consistent structure across all evaluation scripts
- Configuration-driven (models, metrics, filters in YAML)
- Automatic notebook conversion for interactive exploration
- Reusable patterns for common analyses

---

When to Use
===========

- User asks to create a new table or figure for the paper
- User wants to add analysis to `evaluation/scripts/`
- User asks "how do I generate [Table/Figure]X?"
- User needs to analyze model performance breakdowns
- User wants to compare models across dimensions

**Examples:**
- "Create a table comparing LLM vs baseline models"
- "Generate a figure showing performance by age group"
- "I need an appendix table with detailed metrics"
- "Add a new analysis for context ablation study"

---

The 11 Rules
============

1. **Naming Convention**
   - Pattern: `{step}-{output-name}.py`
   - Example: `3-R5-llm-comparison.py`
   - Step 0: Metric computation (reserved)
   - Step 1: Data quality (reserved)
   - Step 2+: Your tables/figures

2. **Configuration**
   - Add section to `1-config.yaml` matching TOPIC_NAME
   - Include: exclude_models, exclude_tasks, custom parameters

3. **Template Structure**
   - Use standard script template with TOPIC_NAME
   - Import from shared_config.py for common functions
   - Include progress logging and error handling

4. **File Paths**
   - Input: `results/0-convert-.../clinical_metrics_detailed.csv`
   - Output: `results/{TOPIC_NAME}/`
   - Display: `0-display/Figure/` or `0-display/Table/`

5. **Multi-Metric Support**
   - Loop through MetricsList from config
   - Generate variant for each metric
   - Create "Main" copy for primary metric

6. **Shared Functions**
   - Import from `shared_config.py`: colors, parsers, filters
   - Use consistent model classification and display names
   - Apply standard exclusion patterns

7. **Common Patterns**
   - Breakdown by dimensions (diabetes, age, event, context)
   - Model grouping (LLM vs baselines)
   - LaTeX table generation
   - Matplotlib figure generation

8. **Script Dependencies**
   - All scripts depend on step 0 (metrics CSV)
   - Scripts can read each other's outputs
   - Use results/{other-script}/ for intermediate data

9. **Display Names**
   - Always use model_display_names from config
   - Clean names for tables/figures (e.g., "GPT-4o" not "gpt-4o-context")

10. **Error Handling**
    - Check if data exists before processing
    - Print progress with section markers
    - Handle missing data gracefully

11. **Notebook Conversion**
    - Scripts auto-convert to .ipynb if enabled
    - Use for interactive exploration
    - Notebooks in `evaluation/notebooks/`

---

Standard Script Template
========================

```python
#!/usr/bin/env python3
"""
Brief description of what this script generates.

Input:  evaluation/results/0-convert-.../clinical_metrics_detailed.csv
Output: evaluation/results/{TOPIC_NAME}/{output-files}
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import yaml
import shutil

# ============================================================================
# TOPIC NAME - Must match config section
# ============================================================================
TOPIC_NAME = '{step}-{name}'

# ============================================================================
# SETUP
# ============================================================================
repo_root = Path.cwd()
config = yaml.safe_load((repo_root / '1-config.yaml').read_text())

results_root = repo_root / config['evaluation_results_folder']
output_dir = results_root / TOPIC_NAME
output_dir.mkdir(parents=True, exist_ok=True)

data_path = results_root / '0-convert-Result-to-model-task-instance-score' / 'clinical_metrics_detailed.csv'

print("=" * 80)
print(f"SCRIPT: {TOPIC_NAME}")
print("=" * 80)

# ============================================================================
# LOAD DATA
# ============================================================================
if not data_path.exists():
    print(f"ERROR: Data not found: {data_path}")
    print("Run step 0 first!")
    sys.exit(1)

df = pd.read_csv(data_path)
print(f"Loaded data: {len(df):,} rows")

# Apply filters from config
script_config = config.get(TOPIC_NAME, {})
exclude_models = script_config.get('exclude_models', [])
if exclude_models:
    df = df[~df['model'].isin(exclude_models)]

# ============================================================================
# ANALYSIS
# ============================================================================
# Your analysis code here

# ============================================================================
# SAVE OUTPUTS
# ============================================================================
def save_figure(fig, name):
    """Save figure as PDF and PNG, copy to display."""
    pdf_path = output_dir / f"{name}.pdf"
    png_path = output_dir / f"{name}.png"

    fig.savefig(pdf_path, bbox_inches='tight', dpi=300)
    fig.savefig(png_path, bbox_inches='tight', dpi=300)
    print(f"✓ Saved: {name}")

    # Copy to display folder
    if 'Appendix' in name:
        dest = repo_root / config['AppendixFigurePath'] / f"{name}.pdf"
    else:
        dest = repo_root / config['FigurePath'] / f"{name}.pdf"

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf_path, dest)
    print(f"  → Display: {dest.relative_to(repo_root)}")

def save_table(content, name):
    """Save LaTeX table, copy to display."""
    tex_path = output_dir / f"{name}.tex"
    tex_path.write_text(content)
    print(f"✓ Saved: {name}.tex")

    # Copy to display folder
    if 'Appendix' in name:
        dest = repo_root / config['AppendixTablePath'] / f"{name}.tex"
    else:
        dest = repo_root / config['TablePath'] / f"{name}.tex"

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tex_path, dest)
    print(f"  → Display: {dest.relative_to(repo_root)}")

# Usage:
# save_figure(fig, "FigureX-name")
# save_table(latex_content, "TableX-name")

print("\n" + "=" * 80)
print("✓ SCRIPT COMPLETE")
print("=" * 80)
```

---

Configuration Format
====================

Add a section to `1-config.yaml`:

```yaml
{step}-{name}:
  # Model exclusions
  exclude_models:
    - random
    - oracle
    - chronos-small

  # Task exclusions
  exclude_tasks:
    - EventCGMTask_Base

  # Seeds (empty = all)
  seeds: []

  # Custom parameters
  figure_size: [10, 8]
  font_sizes:
    title: 14
    axis_label: 12
    tick_label: 10

  # Optional: override notebook conversion
  convert_to_notebook: true

  # Optional: override output directory
  # output_dir: custom/path
```

---

Common Patterns
===============

Pattern A: Breakdown by Dimensions
-----------------------------------

```python
from evaluation.scripts.shared_config import (
    parse_task_context,
    parse_instance_subgroup,
    parse_instance_event
)

# Parse task dimensions
df['diabetes'] = df['task'].apply(
    lambda t: 'D1' if 'D1' in t else ('D2' if 'D2' in t else None)
)
df['age'] = df['task'].apply(
    lambda t: 18 if 'Age18' in t else (
        40 if 'Age40' in t else (
            65 if 'Age65' in t else None
        )
    )
)
df['event'] = df['task'].apply(parse_instance_event)
df['context'] = df['task'].apply(parse_task_context)

# Aggregate by dimensions
overall = df.groupby('model')['crps'].agg(['mean', 'sem'])
by_diabetes = df.groupby(['model', 'diabetes'])['crps'].agg(['mean', 'sem'])
by_age = df.groupby(['model', 'age'])['crps'].agg(['mean', 'sem'])
by_event = df.groupby(['model', 'event'])['crps'].agg(['mean', 'sem'])
```

Pattern B: Model Grouping
--------------------------

```python
from evaluation.scripts.shared_config import (
    get_model_class,
    filter_excluded_models
)

# Classify models
df['model_class'] = df['model'].apply(get_model_class)

# Define groups
llm_models = df[
    df['model_class'].isin(['Direct Prompt LLM', 'Direct Prompt LLM (Small)'])
]['model'].unique()

baseline_models = df[
    df['model_class'].isin(['Statistical', 'TS Foundation'])
]['model'].unique()

# Filter
df_llm = df[df['model'].isin(llm_models)]
df_baseline = df[df['model'].isin(baseline_models)]
```

Pattern C: LaTeX Table Generation
----------------------------------

```python
def format_mean_sem(mean, sem):
    """Format as 'mean ± sem'."""
    if pd.isna(mean) or pd.isna(sem):
        return "N/A"
    return f"{mean:.3f} $\\pm$ {sem:.3f}"

def bold_if_best(value_str, is_best):
    """Bold if best value."""
    if is_best and value_str != "N/A":
        return f"\\textbf{{{value_str}}}"
    return value_str

# Build LaTeX table
latex_lines = [
    r"\begin{table}[t]",
    r"\caption{Your caption here}",
    r"\label{table:your-label}",
    r"\centering",
    r"\begin{tabular}{lcc}",
    r"\toprule",
    r"Model & Overall & D1 \\",
    r"\midrule",
]

# Get display names from config
model_display_names = config.get('model_display_names', {})

for model in sorted_models:
    # Get display name
    base = model.replace('-context', '').replace('-nocontext', '')
    display = model_display_names.get(base, model)

    # Format values
    overall_val = format_mean_sem(
        stats.loc[model, 'mean'],
        stats.loc[model, 'sem']
    )

    # Check if best
    is_best = abs(stats.loc[model, 'mean'] - stats['mean'].min()) < 0.001
    overall_val = bold_if_best(overall_val, is_best)

    latex_lines.append(f"{display} & {overall_val} \\\\")

latex_lines.extend([
    r"\bottomrule",
    r"\end{tabular}",
    r"\end{table}"
])

latex_content = "\n".join(latex_lines)
save_table(latex_content, "TableX-name")
```

Pattern D: Matplotlib Figure
-----------------------------

```python
import seaborn as sns
from evaluation.scripts.shared_config import (
    COLORS_MODEL_CLASS,
    get_model_class,
    get_model_display_name
)

# Setup
sns.set_style("whitegrid")
fig_size = script_config.get('figure_size', [10, 6])
fig, ax = plt.subplots(figsize=fig_size)

# Plot data with consistent colors
for model in models:
    data = df[df['model'] == model]

    # Get color from shared config
    model_class = get_model_class(model)
    color = COLORS_MODEL_CLASS.get(model_class, '#7f7f7f')

    # Get display name
    label = get_model_display_name(model)

    ax.plot(data['x'], data['y'], label=label, color=color, linewidth=2)

# Styling
font_sizes = script_config.get('font_sizes', {})
ax.set_xlabel("X Label", fontsize=font_sizes.get('axis_label', 12))
ax.set_ylabel("Y Label", fontsize=font_sizes.get('axis_label', 12))
ax.set_title("Your Title", fontsize=font_sizes.get('title', 14))
ax.legend(fontsize=font_sizes.get('legend', 10))
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_figure(fig, "FigureX-name")
plt.close(fig)
```

Pattern E: Multi-Metric Loop
-----------------------------

```python
METRICS = config.get('MetricsList', ['crps', 'ct_crps', 'mae', 'rmse'])
MAIN_METRIC = config.get('MainMetrics', 'ct_crps')

# Generate for each metric
for metric in METRICS:
    print(f"\n{'='*80}")
    print(f"GENERATING FOR METRIC: {metric.upper()}")
    print(f"{'='*80}")

    # Your analysis using this metric
    result = analyze(df, metric)

    # Generate output
    save_figure(fig, f"FigureX-{metric}")

# Create Main copy for primary metric
import shutil
main_source = output_dir / f"FigureX-{MAIN_METRIC}.pdf"
main_dest = output_dir / f"FigureX-Main.pdf"
shutil.copy2(main_source, main_dest)
print(f"\n✓ Created Main copy: FigureX-Main.pdf")
```

---

Common Analysis Types
=====================

Main Results Table
------------------

Table showing model performance by demographics.

**Columns:** Overall | D1 | D2 | Age18 | Age40 | Age65 | Diet | Exercise

```python
overall = df.groupby('model')[metric].agg(['mean', 'sem'])
by_diabetes = df.groupby(['model', 'diabetes'])[metric].agg(['mean', 'sem'])
by_age = df.groupby(['model', 'age'])[metric].agg(['mean', 'sem'])
by_event = df.groupby(['model', 'event'])[metric].agg(['mean', 'sem'])
```

Context Ablation Study
----------------------

Compare performance across context levels.

```python
context_levels = ['NoCtx', 'Profile', 'MediumEvent', 'DetailedEvent']

results = []
for ctx_level in context_levels:
    df_ctx = df[df['task'].str.contains(ctx_level)]
    stats = df_ctx.groupby('model')[metric].agg(['mean', 'sem'])
    stats['context'] = ctx_level
    results.append(stats)

all_results = pd.concat(results)
```

Model Comparison Figure
-----------------------

Compare two groups of models (e.g., LLM vs baselines).

```python
# Define groups
llm_models = [m for m in df['model'].unique()
              if 'gpt' in m or 'claude' in m]
baseline_models = ['chronos-large', 'r-arima', 'r-ets']

# Aggregate
llm_stats = df[df['model'].isin(llm_models)].groupby('model')[metric].mean()
baseline_stats = df[df['model'].isin(baseline_models)].groupby('model')[metric].mean()

# Bar chart
x = range(len(llm_models))
width = 0.35
ax.bar(x, llm_stats, width, label='LLM', alpha=0.8)
ax.bar([i+width for i in x], baseline_stats, width, label='Baseline', alpha=0.8)
```

Performance Heatmap
-------------------

Model-task performance matrix.

```python
# Pivot to matrix format
pivot = df.pivot_table(
    values='crps',
    index='model',
    columns='task',
    aggfunc='mean'
)

# Heatmap
import seaborn as sns
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', ax=ax)
ax.set_title("Model Performance Heatmap (lower CRPS is better)")
```

---

shared_config.py Functions
===========================

Import commonly used functions:

```python
from evaluation.scripts.shared_config import (
    # Model classification
    get_model_class,           # → 'Statistical', 'TS Foundation', etc.
    get_quant_vs_llm,          # → 'Quantitative', 'LLM-based', 'Hybrid'
    get_context_status,        # → 'Context', 'No Context', 'N/A'
    get_model_display_name,    # → Clean display name

    # Task parsing
    parse_task_context,        # → 'NoCtx', 'Profile', 'MediumEvent', etc.
    parse_instance_subgroup,   # → 'D1_Age18', 'D2_Age40', etc.
    parse_instance_event,      # → 'Diet', 'Exercise', 'Base'
    categorize_task,           # → Sort key tuple

    # Colors
    COLORS_MODEL_CLASS,        # Dict: category → color
    COLORS_SUBGROUP,           # Dict: subgroup → color
    COLORS_EVENT_TYPE,         # Dict: event → color
    COLORS_TASK_CONTEXT,       # Dict: context → color
    get_model_color,           # Get color for model
    get_instance_color,        # Get color for task

    # Filters
    filter_excluded_models,    # Apply model exclusions
    filter_excluded_tasks,     # Apply task exclusions

    # Constants
    EXCLUDE_MODELS,            # List of excluded models
    MODEL_DISPLAY_NAMES,       # Dict: model → display name
)
```

---

Metrics in CSV
==============

The `clinical_metrics_detailed.csv` contains:

**Columns:**
- `model`: Model name
- `task`: Task name
- `seed`: Random seed
- `crps`: Standard CRPS
- `t_crps`: Temporal-weighted CRPS
- `c_crps`: Clarke-weighted CRPS
- `ct_crps`: Clarke-Temporal CRPS
- `mae`: Mean Absolute Error
- `rmse`: Root Mean Square Error
- `clarke_ab`: % in Clarke zones A+B (clinically acceptable)
- `clarke_cde`: % in Clarke zones C+D+E (problematic)

**Example row:**
```
model,task,seed,crps,t_crps,c_crps,ct_crps,mae,rmse,clarke_ab,clarke_cde
gpt-4o-context,EventCGMTask_D1_Age18_Diet_Ontime_DetailedEvent,1,45.2,48.3,42.1,46.5,12.3,18.7,85.2,14.8
```

---

Notebook Conversion
===================

Scripts automatically convert to Jupyter notebooks if enabled.

Global Setting
--------------

In `1-config.yaml`:

```yaml
auto_convert_to_notebook: true
convert_to_notebooks_script: evaluation/notebooks/convert_to_notebooks.py
```

Per-Script Override
-------------------

```yaml
3-R5-my-figure:
  convert_to_notebook: true   # or false to disable
```

How It Works
------------

After running a script:

```bash
python evaluation/scripts/3-R5-my-figure.py
```

Notebook auto-created at:

```
evaluation/notebooks/3-R5-my-figure.ipynb
```

**Conversion Process:**
- Reads Python script
- Splits into markdown and code cells
- Sections with `# ===` become markdown headers
- Code becomes code cells

Manual Conversion
-----------------

```bash
# Convert single script
python evaluation/notebooks/convert_to_notebooks.py evaluation/scripts/3-R5-my-figure.py

# Convert all scripts
python evaluation/notebooks/convert_to_notebooks.py evaluation/scripts/
```

---

Workflow Instructions
=====================

When user requests a new table or figure:

Step 1: Clarify Requirements
-----------------------------

Ask:
- Output type: Table or Figure? Main or Appendix?
- What comparison: models, tasks, dimensions?
- Which metrics: crps, mae, rmse, etc.?
- Any special breakdowns: by diabetes, age, event, context?

Step 2: Choose Step Number
---------------------------

- Step 0: Reserved (metric computation)
- Step 1: Reserved (data quality)
- Step 2: Main tables (Table1, Table2, ...)
- Step 3: Main figures (FigureR1, FigureR2, ...)
- Step 4: Appendix materials
- Step 5: Demo/examples

Step 3: Create Script
----------------------

1. Create `evaluation/scripts/{step}-{name}.py`
2. Use standard template structure
3. Implement analysis using common patterns
4. Add save_figure() or save_table() calls

Step 4: Add Configuration
--------------------------

Add section to `1-config.yaml`:

```yaml
{step}-{name}:
  exclude_models: [...]
  figure_size: [10, 8]
  # ... other parameters
```

Step 5: Test Script
--------------------

```bash
cd /Users/floydluo/Desktop/EventGlucose/paper/3-Paper-EventGlucose-KDD2026
python evaluation/scripts/{step}-{name}.py
```

Step 6: Verify Outputs
-----------------------

Check:
- `evaluation/results/{step}-{name}/` - intermediate files created
- `0-display/Figure/` or `0-display/Table/` - final outputs copied
- `evaluation/notebooks/{step}-{name}.ipynb` - notebook created (if enabled)

Step 7: Iterate if Needed
--------------------------

User can:
- Modify script for adjustments
- Open notebook for interactive exploration
- Re-run to regenerate outputs

---

Quick Reference
===============

File Paths
----------

```python
repo_root = Path.cwd()
config = yaml.safe_load((repo_root / '1-config.yaml').read_text())

# Standard paths
config_yaml = repo_root / '1-config.yaml'
metrics_csv = results_root / '0-convert-Result-to-model-task-instance-score' / 'clinical_metrics_detailed.csv'

# Output paths
output_dir = results_root / TOPIC_NAME
figure_dir = repo_root / config['FigurePath']
table_dir = repo_root / config['TablePath']
appendix_fig_dir = repo_root / config['AppendixFigurePath']
appendix_table_dir = repo_root / config['AppendixTablePath']
```

Save Functions
--------------

```python
# Save figure (PDF + PNG, copy to display)
save_figure(fig, "FigureX-name")

# Save table (TEX, copy to display)
save_table(latex_content, "TableX-name")
```

Task Dimension Parsing
-----------------------

```python
# Extract diabetes type
diabetes = 'D1' if 'D1' in task else ('D2' if 'D2' in task else None)

# Extract age
age = 18 if 'Age18' in task else (40 if 'Age40' in task else (65 if 'Age65' in task else None))

# Extract event
event = 'Diet' if 'Diet' in task else ('Exercise' if 'Exercise' in task else None)

# Or use shared functions
from evaluation.scripts.shared_config import parse_instance_event, parse_task_context
event = parse_instance_event(task)
context = parse_task_context(task)
```

---

Tips for Effective Use
=======================

1. **Always check data exists** - Handle FileNotFoundError gracefully

2. **Use shared_config.py** - Import colors, parsers, filters for consistency

3. **Print progress** - Use section markers (`="*80`) to show status

4. **Apply filters from config** - exclude_models, exclude_tasks, seeds

5. **Use display names** - Get from config, not raw model names

6. **Follow multi-metric pattern** - Loop through MetricsList, create Main copy

7. **Test locally first** - Run script before committing

8. **Check outputs** - Verify both intermediate (results/) and final (0-display/)

9. **Keep scripts focused** - One table or figure per script

10. **Document in docstring** - Brief description, input/output paths

---

Example: Complete Minimal Script
=================================

```python
#!/usr/bin/env python3
"""
Generate Figure R5: Model performance by event type.

Input:  evaluation/results/0-convert-.../clinical_metrics_detailed.csv
Output: evaluation/results/3-R5-event-comparison/FigureR5-*.pdf
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import yaml
import shutil

# ============================================================================
# SETUP
# ============================================================================
TOPIC_NAME = '3-R5-event-comparison'

repo_root = Path.cwd()
config = yaml.safe_load((repo_root / '1-config.yaml').read_text())

results_root = repo_root / config['evaluation_results_folder']
output_dir = results_root / TOPIC_NAME
output_dir.mkdir(parents=True, exist_ok=True)

data_path = results_root / '0-convert-Result-to-model-task-instance-score' / 'clinical_metrics_detailed.csv'

# ============================================================================
# LOAD DATA
# ============================================================================
df = pd.read_csv(data_path)

# Parse event type
df['event'] = df['task'].apply(
    lambda t: 'Diet' if 'Diet' in t else ('Exercise' if 'Exercise' in t else None)
)
df = df[df['event'].notna()]

# ============================================================================
# ANALYSIS
# ============================================================================
by_event = df.groupby(['model', 'event'])['crps'].mean().reset_index()

# ============================================================================
# GENERATE FIGURE
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

# Bar chart
models = sorted(df['model'].unique())
x = range(len(models))
width = 0.35

diet_vals = [by_event[(by_event['model']==m) & (by_event['event']=='Diet')]['crps'].values[0] for m in models]
exercise_vals = [by_event[(by_event['model']==m) & (by_event['event']=='Exercise')]['crps'].values[0] for m in models]

ax.bar(x, diet_vals, width, label='Diet', alpha=0.8)
ax.bar([i+width for i in x], exercise_vals, width, label='Exercise', alpha=0.8)

ax.set_xlabel("Model")
ax.set_ylabel("CRPS (lower is better)")
ax.set_title("Model Performance by Event Type")
ax.set_xticks([i+width/2 for i in x])
ax.set_xticklabels(models, rotation=45, ha='right')
ax.legend()
plt.tight_layout()

# Save
pdf_path = output_dir / "FigureR5-event-comparison.pdf"
fig.savefig(pdf_path, bbox_inches='tight')
print(f"✓ Saved: {pdf_path}")

# Copy to display
display_path = repo_root / config['FigurePath'] / "FigureR5-event-comparison.pdf"
display_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(pdf_path, display_path)
print(f"✓ Copied to display: {display_path}")
```

**Config (`1-config.yaml`):**

```yaml
3-R5-event-comparison:
  exclude_models:
    - random
    - oracle
  figure_size: [10, 6]
```

**Run:**

```bash
python evaluation/scripts/3-R5-event-comparison.py
```

**Outputs:**
- `evaluation/results/3-R5-event-comparison/FigureR5-event-comparison.pdf`
- `0-display/Figure/FigureR5-event-comparison.pdf`
- `evaluation/notebooks/3-R5-event-comparison.ipynb` (if enabled)

---

End of Skill Definition
