task — Authoring Conventions (shared knowledge pack)
======================================================

The SINGLE home for "how task code is written" in task. Both consume it,
neither duplicates it:

- the **type skills** (`haipipe-task-for-<type>`) read it when a human
  authors interactively;
- the **creator agents** (`code-creator-for-<type>-agent`) read it when
  authoring headless in a fan-out.

If a convention changes, change it HERE — every skill and every creator
picks it up. Type-specific knowledge lives in each `haipipe-task-for-<type>`
skill's own `ref/`; this file is only the cross-type rules.


1. The four sister files (one NAME token)
-----------------------------------------

```
configs/<NAME>.yaml       📥 frozen input (_meta + params)
runs/<NAME>.sh            ▶️  entry (wraps papermill + auto-logs)
results/<NAME>/           📊 light artifacts + runtime.yaml + metrics.json
notebooks/<NAME>.ipynb    📓 papermill executed-notebook record
```

`<NAME>` is `run_`-prefixed, snake_case, `[a-z0-9_]+`, encodes the variant
(seed / arch / data slice), unique within the task-folder.


2. The `_meta` contract (REQUIRED before any run)
-------------------------------------------------

```
purpose   one sentence: why this run exists        (REQUIRED — halt if absent)
note      free-form rationale / discussion notes   (recommended)
input     semantic description of data + ckpt       (recommended)
output    expected artifacts + headline guess       (recommended)
```

`purpose` non-empty is a hard gate. The other three are warn-if-missing.


3. Heavy-artifact placement (hard rule)
---------------------------------------

```
✅ _WorkSpace/5-ModelInstanceStore/<name>/@v<NNNN>/   ← .pt .ckpt .safetensors .bin
❌ results/                                            ← light only: runtime.yaml,
                                                         metrics.json, small figures
```

Never write checkpoints into `results/`. `results/<NAME>/` holds the
per-run record, not weights.


4. Reproducibility (what makes a run trustworthy)
-------------------------------------------------

```
□ config seed     explicit value, not a framework default
□ git_sha         recorded by run.sh; must refer to a real commit
□ runtime.yaml    written by run.sh at launch (status/exit_code/git_sha)
□ metrics.json    parseable, keys match what the claim will reference
```

These are exactly what `haipipe-task-reviewer-agent` (GATE 2) checks. Author
the code so it passes that audit by construction.


5. The first-run gate
---------------------

`runs/<RUN>.sh` refuses to launch if `CODE_REVIEW.md` is missing or stale.
That sidecar is produced by `haipipe-task-reviewer-agent` (GATE 1). The
author NEVER writes its own CODE_REVIEW.md and NEVER self-reviews —
builder ≠ judge. The orchestrator/bridge runs GATE 1 after authoring.


6. Author scope (builder ≠ judge ≠ scaffolder)
----------------------------------------------

```
scaffold the 4 sister files / _meta / hierarchy   → the type SKILL (haipipe-task-for-<type>)
write the <TASK>.py algorithm body + config params → haipipe-task-builder-agent
review code vs intent (GATE 1)                      → haipipe-task-reviewer-agent
audit the finished run (GATE 2)                     → haipipe-task-reviewer-agent
```

A creator authors and stops. It does not scaffold (the skill does), does
not review itself, does not launch.


7. Notebooks & papermill (avoid the bloat trap)
-----------------------------------------------

`<TASK>.py` IS the papermill SOURCE. At run.sh time it is converted to a
template `.ipynb` and executed by papermill into `notebooks/<RUN>.ipynb`,
with `config` injected as a parameter. So:

```
✅ author <TASK>.py as a papermill-style script (a `config` parameter is injected)
❌ do NOT call papermill / nbconvert yourself inside <TASK>.py — run.sh owns that
```

Every run produces a notebook by default — it is the per-run executed record.
The cost to manage is NOT time (the wrapper is seconds) but **notebook bloat**:
a training loop that prints every step / uses tqdm bloats the `.ipynb` to
megabytes of progress bars.

```
□ HEAVY runs (training / data): keep stdout SPARSE — log milestones, not
  per-step. And set `_meta.notebook: thin` in the config (run.sh clears
  outputs → small record that still keeps code + injected params).
□ READ-OUTPUT runs (display / eval / individual / algo / agent): leave
  `_meta.notebook: full` (default) — the inline figures/metrics ARE the value.
□ rare pure-artifact runs: `_meta.notebook: off` (execute, keep no notebook).
```

The knob is `configs/<RUN>.yaml` → `_meta.notebook: full | thin | off`
(default `full`; see `invocation-modes.md`). All three execute the `.py`
identically — they differ only in what notebook is retained.

`notebooks/` holds run ARTIFACTS, not source — the project `.gitignore`
should list `notebooks/` (and `_WorkSpace/`) so N×seeds×arms notebooks never
bloat the repo.
