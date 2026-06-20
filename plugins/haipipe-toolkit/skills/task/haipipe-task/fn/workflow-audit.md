fn/workflow-audit — four-sister consistency check
===================================================

Called by `/haipipe-task` as the first step on any existing task folder.
Read-only scan that reports what's aligned and what's broken.


When to call
------------

Automatically when `/haipipe-task` targets an existing task folder
(not scaffolding a new one). Also callable standalone:

```
/haipipe-task audit <task-folder-path>
```


Procedure
---------

### Step 1 — Discover run names

Scan directories and collect all unique run names. The exact directories
depend on the task engine:

**Python/papermill tasks:**
```
NAMES_FROM_CONFIGS   = stem of each configs/*.yaml
NAMES_FROM_RUNS      = stem of each runs/*.{sh,ps1} (dedupe .sh/.ps1 pairs)
NAMES_FROM_RESULTS   = name of each results/*/ subfolder
NAMES_FROM_NOTEBOOKS = stem of each notebooks/*.ipynb

ALL_NAMES = union of all four sets
```

**Stata tasks** (configs may be .do or .yaml, no notebooks):
```
NAMES_FROM_CONFIGS   = stem of each configs/*.{yaml,do}
                       EXCLUDE shared configs: _source_*.do, bare <Cohort>.do
                       (these are shared/selectors, not per-run configs)
                       INCLUDE per-run configs: <Cohort>_{synth|full}_<year>.do
NAMES_FROM_RUNS      = stem of each runs/*.ps1 (strip run_ prefix to match config stem)
NAMES_FROM_RESULTS   = name of each results/*/ subfolder
NAMES_FROM_LOGS      = stem of each results/*/log/*.txt (Stata log files)

ALL_NAMES = union of all sets
```

Stata tasks may not have notebooks/ at all -- that's expected, not an issue.

**Stata config matching rule:** for a run named `run_case_VisitLBP_synth_2015`,
the matching config is `configs/VisitLBP_synth_2015.do` (strip the `run_case_`
prefix). Shared configs (`VisitLBP.do`, `_source_synth.do`) are NOT per-run
configs -- they are the base layer that per-run configs load via `do` include.
A run without a matching per-run config is flagged `missing_config: FIXABLE`.
The fix: generate a thin `.do` wrapper that loads the source selector + shared
config + pins the year (see `haipipe-task-for-stata-case/ref/config-seed-run.do`).

### Step 2 — Check four-sister pairing

For each name in ALL_NAMES, check sisters exist. The "four sisters" vary
by engine:

**Python:** configs/<NAME>.yaml + runs/<NAME>.sh + results/<NAME>/ + notebooks/<NAME>.ipynb
**Stata:**  configs/<NAME>.{yaml|do} + runs/<NAME>.ps1 + results/<NAME>/ + (log optional)

```
NAME              configs/  runs/   results/  notebooks/
─────────────────────────────────────────────────────────
run_build_physician  ❌       ✅ .sh+.ps1  ✅       ✅
run_build_xwalk      ❌       ✅ .sh+.ps1  ✅       ✅
run_build_cleanse    ❌       ✅ .sh only  ✅       ✅
run_build_roberta    ❌       ❌           ✅       ❌
```

### Step 3 — Classify issues

| Issue type | Pattern | Severity |
|-----------|---------|----------|
| **missing_config** | runs/ exists but configs/<NAME>.yaml missing | FIXABLE — generate from shared config |
| **missing_run** | configs/ exists but runs/<NAME>.sh missing | FIXABLE — generate from template |
| **missing_notebook** | runs/ + results/ exist but notebooks/ missing | INFO — notebook created at runtime |
| **stale_result** | results/<NAME>/ exists but no runs/ or configs/ | WARN — orphaned, candidate for cleanup |
| **shared_config** | one config serves multiple runs | FIXABLE — split into per-run configs |
| **missing_ps1** | .sh exists but .ps1 missing (or vice versa) | FIXABLE — generate counterpart |

### Step 4 — Detect task type

Use the router's inference cascade:
1. Explicit: caller said type
2. Script-inferred: read `<TASK>.py` and `scripts/*.py` imports/content
   - `from haipipe` / `SourceFn` / `RecordFn` → data
   - `import torch` / `Trainer` / `sweep` → training
   - `eval` / `metrics` / `score` → eval
   - `plt.` / `fig` / `savefig` / `.tex` → display
   - `stata` / `.do` / `preserve` → stata (delegate)
   - `agent` / `claude` / `anthropic` → agent
3. Keyword-inferred: scan args for type keywords

NOTE: do NOT infer type from the group letter (A00_, B01_, etc.).
Group letters are project-specific organizational prefixes.

### Step 5 — Check workflow/ folder

```
workflow/ exists?
  ├── YES → read plan.yaml, check it matches current task state
  │         (new runs added since plan was written? files moved?)
  └── NO  → flag as "plan missing, will generate in workflow-plan step"
```

### Step 6 — Report

Output a structured audit:

```
📋 Audit: A01_build_physician
   type: external (inferred from A00_ group)
   
   Four-sister check:
     run_build_physician:  configs ❌  runs ✅  results ✅  notebooks ✅
     run_build_xwalk:      configs ❌  runs ✅  results ✅  notebooks ✅
     run_build_cleanse:    configs ❌  runs ✅  results ✅  notebooks ✅
     run_build_roberta:    configs ❌  runs ❌  results ✅  notebooks ❌  (stale)
   
   Issues (3 fixable, 1 warn):
     FIXABLE: 3 runs missing per-run configs (shared config: external_physician.yaml)
     WARN:    run_build_roberta has results/ but no runner (stale?)
   
   Workflow: plan.yaml exists ✅ / missing ❌
   
   Next: /haipipe-task fix → /haipipe-task plan
```


Return contract
---------------

```yaml
status: ok | issues_found
type: <detected task type>
run_names: [run_build_physician, run_build_xwalk, run_build_cleanse, run_build_roberta]
sisters:
  run_build_physician: { config: false, run: true, result: true, notebook: true }
  run_build_xwalk:     { config: false, run: true, result: true, notebook: true }
  run_build_cleanse:   { config: false, run: true, result: true, notebook: true }
  run_build_roberta:   { config: false, run: false, result: true, notebook: false }
issues:
  - { name: run_build_physician, type: missing_config, severity: fixable }
  - { name: run_build_roberta, type: stale_result, severity: warn }
shared_configs:
  - { config: external_physician.yaml, serves: [run_build_physician, run_build_xwalk, run_build_cleanse] }
workflow_exists: true | false
```
