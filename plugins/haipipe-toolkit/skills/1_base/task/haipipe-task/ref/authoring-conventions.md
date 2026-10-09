# Task authoring conventions

This is the shared knowledge pack for every Task-type specialist and creator
agent. Engine-specific details remain in the owning specialist.

## One Run, four projections

```text
<task>/scripts/config/<run>.yaml        frozen authored input
<task>/runs/<run>.sh                    authored Ticket
$OUTPUT_ROOT/<task>/results/<run>/      generated Result and receipt
$OUTPUT_ROOT/<task>/notebooks/<run>.ipynb
```

The stem is always `rNN_<noun>_<qualifier>` and matches across all four
projections. Shared Task config omits the `rNN_` prefix.

The notebook is generated: the Ticket converts the `# %%` worker `.py` and
executes it. Never edit a notebook, by hand, by find-and-replace, or by a
script that rewrites it after the run. To change what it shows (code, prose,
an output, a path), change the `.py` and rerun the Ticket (JL 260927). The same
holds for every generated file (a Board's `board/` HTML, `TASK-TABLE.md`,
`code/haifn/`): change its source and rerun its generator. Report such a change
by its source ("changed `visualize_explain.py`, reran its 16 Tickets"), never as
an edit to the output (JL 260929).

Encoded ids (`patient_id_encoded`, `invitation_id_encoded`, other encoded UUIDs)
are meaningless ids, not PHI. A notebook, CSV or Result may show them; they are
never a reason to hold back a commit, change a worker or rerun a Ticket. Before a
push, check file size (a large data extract such as a `.parquet` stays out of
git), secrets, and build leftovers (`.pyc`) instead (JL 260929).

## Worker output

The Ticket exports `RESULT_DIR`. A worker must require it and never construct
an output path from its source location:

```python
import os
from pathlib import Path

if "RESULT_DIR" not in os.environ:
    raise RuntimeError("RESULT_DIR is required; launch through the Task Ticket")
results_dir = Path(os.environ["RESULT_DIR"])
```

Cross-Task inputs resolve from an explicit store-aware base and name an exact
upstream Task/Run Result. Never infer a cohort or silently substitute a local
path.

## Paths

Nothing a Run writes to disk may hold an absolute path. The user name and the
checkout folder change per machine (`/Users/<name>/Desktop/<SPACE>/...`), so an
absolute path breaks on the next machine and shows the user name (JL 260927).

- Write every path relative to the SPACE root, the folder that holds `env.sh`
  (for example `examples-2-lm/Proj10-LLM-Baseline/tasks/...`). This covers
  configs, Tickets, the `config` parameter papermill writes into the notebook,
  anything a worker prints, `runtime.yaml`, `metrics.json`, and reports.
- Preferred: the Ticket injects the config SPACE-relative
  (`-p config "$(space_rel "$CONFIG")"`), and the worker turns it back into a
  real path by walking up from its working folder to `env.sh`:

  ```python
  SPACE = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / "env.sh").exists())
  config = str(SPACE / config)      # SPACE-relative becomes real; an absolute path stays as it is
  ```

- Start the notebook kernel in the Task folder (`papermill --cwd <task>`),
  never in the SPACE root. The root holds `code/__init__.py`, which hides
  Python's standard `code` module; ipykernel then dies with
  `Kernel died before replying to kernel_info`.
- Never edit the notebook to fix a path (JL 260927): it is generated from the
  worker `.py`, so the fix goes in the `.py` (or in how the Ticket injects the
  config), then the Ticket reruns. `ref/run-sh-template.sh` only warns: when
  the executed notebook or a Result file still shows `<SPACE root>/`.

## Required config metadata

```yaml
_meta:
  purpose: "Why this Run exists"
  note: "Design rationale"
  input: "Authoritative inputs"
  output: "Expected artifacts and headline"
  notebook: full
```

`purpose` is required. Notebook policy is `full`, `thin`, or `off`:

- `full`: keep executed outputs; useful for display and evaluation.
- `thin`: clear cell outputs after execution; useful for training and data.
- `off`: execute through papermill but keep no notebook artifact.

## Code form

- The worker source is a `.py` file under `<task>/scripts/`.
- Add an `Intent` section to its module docstring.
- Use `# %%` cell boundaries.
- The first executable cell is `# %% [parameters]` and declares injectable
  parameters with safe defaults.
- Do not invoke papermill or notebook conversion inside the worker; the Ticket
  owns conversion and execution.
- Keep stdout sparse for heavy Runs.
- Validate every configured name before use and list missing names in errors.

## Review gates

The creator writes code and config, then stops. The reviewer owns
`CODE_REVIEW.md` and checks intent against implementation. The Ticket refuses
launch when that review is absent or failed unless an explicit skip is
recorded. A review carries no commit id: a commit never blocks a Ticket; when
the code changes, the reviewer updates the review's notes and verdict
(JL 260929).

After execution, the reviewer verifies Results against the Plan and writes the
Run audit. The same agent role may perform both gates, but it must start from
fresh context and may not have authored the code under review.

## Reproducibility

Every Run records:

```text
seed or deterministic policy
git SHA and dirty state
Ticket path and arguments
config path
all additional input paths
host, start, finish, exit code
declared Result gate outcome
```

A parsing-only pass is a smoke test. A correctness claim must compare the
Result to an expectation, invariant, or independently computed reference.

## Artifact placement

The law is haipipe-run's **A Result is light**; this is how a Task keeps it.

`<task>/results/<run>/` contains light evidence: runtime and metrics files,
small tables, figures, logs, and pointers. Heavy output lives in `_WorkSpace/`:

1. **What is heavy**: a checkpoint or model, an array, a cache, a row-level table
   beyond a small sample, or any file over 10 MB.
2. **Where it goes**: the Run's own folder, which the Ticket exports as
   `HEAVY_DIR`:
   `_WorkSpace/ProjectResult/<Project>/<block>/<job>/<task>/<run>/`. It mirrors
   the Run's address below `work/` (Task names repeat across Jobs, so Block and
   Job are part of it). The worker creates it only when it writes there
   (`os.makedirs(os.environ["HEAVY_DIR"], exist_ok=True)`). `LOCAL_PROJECT_RESULT`
   may move the root; the default is `_WorkSpace/ProjectResult`. A pipeline asset
   (a SourceSet, a RecordSet, an ExternalStore version) goes to its stage store
   (`$LOCAL_SOURCE_STORE`, ...) instead, because other Runs look it up by name.
3. **What the Result keeps**: `heavy.yaml`, which the Ticket writes after the
   worker when `HEAVY_DIR` holds files: the folder's SPACE-relative path, then
   each file's path, bytes and sha256.
4. **Never in the Task folder**: no copy of a heavy file and no symlink to an
   absolute path or into `_WorkSpace/` (`data/`, `src/cache/`, ...). Such a link
   stores an absolute path (AGENTS.md rule 7) and dangles on every other
   machine; read the store through its variable instead. A relative link inside
   the repository (Tickets sharing one `_run.sh`) is fine.
5. **Checked**: the Ticket runner warns when a Result holds a file over 10 MB
   or a link, and when the Task folder links to an absolute path or into
   `_WorkSpace/` (JL 260929).

Generated notebooks and Results follow `$OUTPUT_ROOT`. Authored code, config,
Tickets, Page content, and workflow intent remain in the Task Folder.

## Ownership

```text
scaffold Task + Run spine           Task-type specialist
author worker + Run config          creator agent
review code against intent          reviewer agent, Gate 1
execute one Ticket                  Ticket/runtime
audit Result against Plan           reviewer agent, Gate 2
interpret evidence for readers      Task Page workflow
```
