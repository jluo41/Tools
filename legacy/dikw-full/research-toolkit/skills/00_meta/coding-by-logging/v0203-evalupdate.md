# Evaluation Scripts Update - v0203

## Summary

Updated evaluation scripts to support the new task context levels: **NewMedium** and **NewDetail**.

## Files Modified

### 1. `evaluation/scripts/shared_config.py`

Added comprehensive task context classification support:

#### New Constants

```python
# Color scheme for task context levels
COLORS_TASK_CONTEXT = {
    'Base': '#7f7f7f',        # Gray
    'NoCtx': '#d62728',       # Red
    'Profile': '#ff7f0e',     # Orange
    'MediumEvent': '#2ca02c', # Green
    'DetailedEvent': '#1f77b4', # Blue
    'NewMedium': '#9467bd',   # Purple (NEW)
    'NewDetail': '#e377c2',   # Pink (NEW)
}

# Task context ordering for sorting
TASK_CONTEXT_ORDER = {
    'Base': 0,
    'NoCtx': 1,
    'Profile': 2,
    'MediumEvent': 3,
    'DetailedEvent': 4,
    'NewMedium': 5,  # NEW
    'NewDetail': 6,  # NEW
}
```

#### New Functions

| Function | Purpose |
|----------|---------|
| `parse_task_context(task_name)` | Extract context level from task name (e.g., `NewMedium`, `DetailedEvent`) |
| `get_task_context_order(task_name)` | Get numeric sorting order for a task's context level |
| `categorize_task(task_name)` | Full task categorization returning `(diabetes, age, event, context, task_name)` |
| `get_task_base_name(task_name)` | Extract base task name without context suffix |

#### Updated Functions

- `get_instance_color(task_name, color_scheme)` - Now accepts `'context'` as a valid `color_scheme` option

### 2. `evaluation/scripts/0-convert-Result-to-model-task-instance-score.py`

Added a **Task Context Level Summary** section that:

1. Parses all tasks to identify their context levels
2. Counts tasks and instances per context level
3. Prints a distribution table
4. Saves `task_context_summary.json` with the breakdown

#### New Output File

`evaluation/results/0-convert-Result-to-model-task-instance-score/task_context_summary.json`:

```json
{
  "context_levels": ["Base", "NoCtx", "Profile", "MediumEvent", "DetailedEvent", "NewMedium", "NewDetail"],
  "tasks_by_context": {"NoCtx": 12, "MediumEvent": 12, "NewMedium": 12, ...},
  "instances_by_context": {"NoCtx": 1200, "MediumEvent": 1200, ...}
}
```

### 3. `evaluation/scripts/1-describe-model-result-data-quality.py`

Updated `categorize_task()` function to include NewMedium and NewDetail:
- NewMedium: context = 5
- NewDetail: context = 6

### 4. `evaluation/scripts/2-generate-Table1-and-Table2.py`

Updated two locations:
- `parse_task_name()` function: Added 'NewMedium' and 'NewDetail' to valid context parts
- `context_levels` list: Extended from 4 to 6 context levels

### 5. `evaluation/scripts/3-R1-llm-vs-baselines-by-context-FigureR1.py`

Updated locations:
- `CONTEXT_LEVELS` default: Extended to include NewMedium and NewDetail
- `task_to_noctx()` function: Added NewDetail and NewMedium to the context suffix list
- **Figure generation**: Changed from hardcoded 1×4 subplot to dynamic 1×N subplot based on `len(CONTEXT_LEVELS)`
- Figure width now scales dynamically: `fig_width = 3.5 * n_contexts`

### 6. `evaluation/scripts/3-R2-llm-with-without-context-FigureR2.py`

Updated multiple locations:
- `context_levels` configuration default (line 97)
- `parse_task_name()` function (line 205)
- Loop for context iteration (line 457)
- Colors array extended to 6 colors (multiple locations)
- Labels array extended to 6 labels (line 668)
- `context_order` list (line 809)
- **Bar chart width**: Changed from hardcoded `width = 0.2` to dynamic `width = 0.8 / n_contexts`
- **Bar offset calculation**: Changed from `(i - 1.5) * width` to `(i - (n_contexts - 1) / 2) * width` for proper centering

### 7. `evaluation/scripts/3-R3-Parameter-Performance-FigureR3.py`

Updated two locations:
- `get_task_attributes_from_json()` function: Added NewMedium and NewDetail to valid context levels
- `ctx_levels_with` set: Added NewMedium and NewDetail for "with context" classification

### 8. `evaluation/scripts/3-R4-instance-group-analysis-FigureR4.py`

Updated multiple locations:
- `parse_task()` function: Added NewMedium and NewDetail to valid context parts
- `valid_contexts` lists (2 locations): Extended to include NewMedium and NewDetail
- `colors` dictionaries (2 locations): Added colors for NewMedium (#9467bd) and NewDetail (#e377c2)
- `plot_order` lists (2 locations): Added NewMedium and NewDetail to plotting order

## Context Level Definitions

| Level | Description | Information Provided |
|-------|-------------|---------------------|
| `Base` | Baseline task | No specific conditions |
| `NoCtx` | No context | Only numerical glucose history |
| `Profile` | Patient profile | Age, diabetes type, basic demographics |
| `MediumEvent` | Basic event info | Event type and timing |
| `DetailedEvent` | Full event details | All event attributes |
| `NewMedium` | **New format** | Timing + key metrics (structured) |
| `NewDetail` | **New format** | Full details with rounded values |

## Usage Examples

### Importing in Other Scripts

```python
from evaluation.scripts.shared_config import (
    COLORS_TASK_CONTEXT,
    TASK_CONTEXT_ORDER,
    parse_task_context,
    categorize_task,
    get_instance_color,
)

# Get context level from task name
ctx = parse_task_context('EventCGMTask_D1_Age18_Diet_Ontime_NewMedium')
# Returns: 'NewMedium'

# Get color for visualization
color = get_instance_color('EventCGMTask_D1_Age18_Diet_Ontime_NewDetail', color_scheme='context')
# Returns: '#e377c2' (pink)

# Sort tasks consistently
tasks_sorted = sorted(task_list, key=categorize_task)
```

### Task Sorting Order

Tasks are sorted by this hierarchy:
1. **Disease type**: D1 < D2
2. **Age group**: Age18 < Age40 < Age65
3. **Event type**: Diet < Exercise
4. **Context level**: NoCtx < Profile < MediumEvent < DetailedEvent < NewMedium < NewDetail

## Things to Be Aware Of

### 1. Task Name Pattern

The new context levels follow the same naming convention:
```
EventCGMTask_{Disease}_{Age}_{Event}_Ontime_{ContextLevel}
```

Examples:
- `EventCGMTask_D1_Age18_Diet_Ontime_NewMedium`
- `EventCGMTask_D2_Age65_Exercise_Ontime_NewDetail`

### 2. Backward Compatibility

- All existing context levels (NoCtx, Profile, MediumEvent, DetailedEvent) continue to work
- Scripts using `shared_config.py` will automatically recognize NewMedium and NewDetail
- The `Base` context level is preserved for tasks without specific context

### 3. Color Scheme Consistency

When creating visualizations, use the shared color schemes:
- NewMedium: Purple (`#9467bd`)
- NewDetail: Pink (`#e377c2`)

### 4. Scripts Updated (Complete List)

All scripts from 0-3 have been updated to support NewMedium and NewDetail:

| Script | Updates Made |
|--------|--------------|
| `0-convert-Result-to-model-task-instance-score.py` | Added context level summary section |
| `1-describe-model-result-data-quality.py` | Updated `categorize_task()` function |
| `2-generate-Table1-and-Table2.py` | Updated `parse_task_name()` and `context_levels` |
| `3-R1-llm-vs-baselines-by-context-FigureR1.py` | Updated `CONTEXT_LEVELS` and `task_to_noctx()` |
| `3-R2-llm-with-without-context-FigureR2.py` | Multiple updates to context lists, colors, labels |
| `3-R3-Parameter-Performance-FigureR3.py` | Updated task attributes and `ctx_levels_with` |
| `3-R4-instance-group-analysis-FigureR4.py` | Updated valid contexts, colors, and plot order |

### 5. Future Scripts

For any new scripts that handle task classification:
- Import from `shared_config.py` when possible
- If defining locally, include all 7 context levels: Base, NoCtx, Profile, MediumEvent, DetailedEvent, NewMedium, NewDetail

### 6. Reference: EventGlucose Project

The `1-describe-model-result-data-quality.py` script in the EventGlucose project already had NewMedium and NewDetail support. The Paper-EventGlucose-KDD2026-2nd project is now synchronized.

## Date

2026-02-03
