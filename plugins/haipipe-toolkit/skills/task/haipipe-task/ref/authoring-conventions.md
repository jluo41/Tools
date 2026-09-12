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
launch when that review is absent, failed, or stale unless an explicit skip is
recorded.

After execution, the reviewer verifies Results against the Plan and writes the
Run audit. The same agent role may perform both gates, but it must start from
fresh context and may not have authored the code under review.

## Reproducibility

Every Run records:

```text
seed or deterministic policy
git SHA and dirty state
Ticket path and arguments
config path and SHA-256
all additional input paths and hashes
host, start, finish, exit code
declared Result gate outcome
```

A parsing-only pass is a smoke test. A correctness claim must compare the
Result to an expectation, invariant, or independently computed reference.

## Artifact placement

`<task>/results/<run>/` contains light evidence: runtime and metrics files,
small tables, figures, logs, and pointers. Checkpoints, large arrays, raw
tables, and other heavy data live in `_WorkSpace/`.

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
