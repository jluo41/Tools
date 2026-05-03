fn-task-folder: Scaffold a New Task-Folder
=============================================

A task-folder is one runnable unit. The scaffold is **task-type aware**:
configs, run-script template, and result location all derive from the
chosen type. See `ref/hierarchy.md` for the type catalog.

Output: `tasks/{G}{NN}_{group}/{NN}_{task_name}/`.


Step 1 — Identify project + task-group
---------------------------------------

Auto-detect from cwd. If group is missing, ASK (or invoke `fn/task-group.md`
first).


Step 2 — Pick the task-type
----------------------------

ASK if not given:

```
(M) model-run      train / sweep a model
(E) evaluation     score a trained model
(F) display        produce paper figures or tables
(D) data-pipeline  run a Stage 1-4 builder
(X) other          free-form / utility
```

The type drives what gets seeded in Step 4. The chosen type should be
consistent with the group letter (A→M, B→E, C→F, D→D); warn if not, but
allow override.


Step 3 — Collect metadata
--------------------------

  2-digit task NN        next free in this group (no gaps)
  snake_case task_name   descriptive (e.g. train_clm_num_modelsize,
                                          eval_clm_forecast,
                                          paper_main_figure)
  Purpose (What)         1 line
  Rationale (Why)        1 line
  Inputs                 1-2 lines (datasets, prior task results, ...)
  Outputs                1-2 lines (checkpoints, metrics, figure files, ...)

  For type=M / E / D: also collect pipeline stages used.


Step 4 — Create skeleton (type-aware)
--------------------------------------

Common to ALL types:

```
{NN}_{task_name}/
├── {NN}_{task_name}.py    ← script, with # %% cells (incl. # %% [parameters])
├── configs/
├── runs/                  ← run_<variant>.sh — one per run
├── results/               ← light artifacts (metrics, figures, logs)
├── notebooks/             ← papermill executed-notebook records (one per run)
└── (no README.md)
```

Stub `.py` (papermill-ready — all task-types use the same shape):
```python
# %% [markdown]
# # {NN}_{task_name}
# TODO: implement

# %% [parameters]
# papermill injects here. Defaults below; override via run_<variant>.sh.
config = "configs/<seed>.yaml"

# %%
import os, sys
from pathlib import Path
try:
    TASK_DIR = Path(__file__).resolve().parent
except NameError:
    try:
        TASK_DIR = Path(__vsc_ipynb_file__).parent.parent
    except NameError:
        TASK_DIR = Path(os.environ.get("TASK_DIR", ""))
        if not TASK_DIR.exists():
            raise RuntimeError("Set TASK_DIR env var before launching.")
REPO_ROOT = TASK_DIR.parents[3]
sys.path.insert(0, str(REPO_ROOT / "code"))
os.environ.setdefault("WORKSPACE_PATH", str(REPO_ROOT / "_WorkSpace"))

# %%
# Main logic
```

### Type-specific seeds (only configs differ; running process is the same)

(M) model-run
  configs/5_model_{name}.yaml
    ModelInstanceClass + modelinstance_name/version + model_tuner_name
    + aidata_name/version + ModelArgs/TrainingArgs/InferenceArgs/EvaluationArgs
  runs/run_{variant}.sh
  results/                empty (checkpoints land in _WorkSpace/5-ModelInstanceStore)
  notebooks/              papermill output dir

(E) evaluation
  configs/eval_{target}.yaml
    modelinstance_name + modelinstance_version + EvaluationArgs
    (which dataset split, which metrics, which horizon, ...)
  runs/run_{target}.sh
  results/<run>/{metrics.json, eval_log.txt}

(F) display
  {NN}_{task_name}.py          reads sibling eval results via REPO_ROOT,
                               aggregates, produces figure/table
  configs/figure_{name}.yaml   list of source runs + plot params
                               (or table_{name}.yaml for a table task)
  runs/run_{name}.sh
  results/<run>/{figure.pdf, figure.png, source_data.csv}
                               or {table.tex, table.csv}

(D) data-pipeline
  configs/{stage}_{dataset}.yaml   {Layer}FnClass + {Layer}Args.dataset_name
                                   (stage in 1..4)
  runs/run_{stage}.sh              invokes builder in code-dev/
  results/                         usually empty (data lands in _WorkSpace/)

(X) other
  No required configs. Free-form .py.


Step 5 — Run-script (papermill — same for every task-type)
-----------------------------------------------------------

Every run.sh follows the same two-step process: convert the task .py to
a template notebook, then papermill it with injected parameters into
notebooks/<variant>.ipynb. The executed notebook IS the run record.

```bash
#!/bin/bash
set -e
TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUN_NAME="$(basename "$0" .sh)"
PROJ="$(cd "$TASK_DIR/../../.." && pwd)"
REPO_ROOT="$(cd "$PROJ/../.." && pwd)"

cd "$REPO_ROOT"
source .venv/bin/activate
source "$PROJ/tasks/{group}/sbatch/env.sh"

# --- parameters (override defaults from the .py [parameters] cell) ---
CONFIG="configs/<seed>.yaml"
# ... task-type-specific params here

# Step 1: convert .py → template .ipynb at task root
TEMPLATE_NB="$TASK_DIR/{NN}_{task_name}.ipynb"
python code/scripts/convert_to_notebooks.py \
    "$TASK_DIR/{NN}_{task_name}.py" -o "$TEMPLATE_NB"

# Step 2: papermill inject + execute → notebooks/<run>.ipynb
export TASK_DIR
mkdir -p "$TASK_DIR/notebooks"
CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}" \
papermill "$TEMPLATE_NB" "$TASK_DIR/notebooks/${RUN_NAME}.ipynb" \
    -p config "$CONFIG" \
    # ... -p <param> <value> per task-type
```

Why one process for everything:
- Every run produces a reviewable notebook (no separate `tee` log discipline).
- Authoring stays in `.py` (diff-friendly); execution leaves an `.ipynb`.
- Params live in `# %% [parameters]` cell — papermill injection is uniform.


Step 6 — Optional task-level diagram/
--------------------------------------

Only if the task **diverges** from the group narrative (most don't —
the group diagram is enough). If needed, author via `/diagram-ascii`:

```
01-overview.txt   What / Why / Inputs / Outputs (1-3 lines each)
02-design.txt     approach detail; for type=M include forward-pass ASCII
                  + architecture-sweep table
03-runs.txt       table | Run | Variant | Result Dir | Status | Notes |
                  (seed empty; status: planned|wip|done|failed|deprecated)
04-progress.txt   dated log, newest on top, seeded with
                  "{YYMMDD} — task scaffolded"
```

Bundle: `/diagram-ascii-canvas {task}/diagram/  →  task.excalidraw`

Otherwise: append a row to the group's `02-tasks.txt` and re-bundle
`group.excalidraw`.


Step 7 — Report
----------------

Print:
  - Task path
  - Type chosen
  - Files created (script, configs, run.sh)
  - Whether task-level diagram was created or group-level updated
  - Suggested next:
      M → fill ModelArgs in config; first run via runs/run_{variant}_nb.sh
      E → fill modelinstance_name in eval config; pair with the source A-task
      F → list which eval runs feed this figure; first build via runs/run_{name}.sh
      D → run the builder; verify via /haipipe-data
      X → fill TODO in {NN}_{task_name}.py


MUST NOT
---------

- Create `README.md`.
- Use any other run-script style — papermill is the one running process.
- Generate real implementation logic in the stub (stubs only).
- Skip configs/ (each task owns its own YAMLs; symlinks forbidden).
- Skip notebooks/ (every run leaves one executed notebook there).
- Place heavy artifacts (.pt / .ckpt / .npy / ...) in results/.
