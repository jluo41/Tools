fn/report-stata — Stata-specific execution report
===================================================

Mirrors `fn/plan-stata.md` structure, filled with what actually happened. Reads Stata logs, summary.txt, and config_snapshot.do — NOT runtime.yaml or notebooks (those are Python/papermill concepts).


When to call
------------

After execution, when `/haipipe-task report` targets a Stata task folder.
Also callable standalone: `/haipipe-task-for-stata report <task-folder-path>`


Procedure
---------

### Step 0 — Read the plans

Read `workflow/plan.yaml` and all `workflow/plan-script-*.yaml`. These are the contracts to report against. If plans don't exist, run `fn/plan-stata.md` first.

### Step 1 — Scan execution evidence

For each RUNNAME in the plan, check:

1. **Results dir exists:** `results/<RUNNAME>/`
2. **Logs present:** `results/<RUNNAME>/log/*.txt` (one per step per year)
3. **Logs clean:** grep each log for `r(\d+)` — any match is a Stata error
4. **Summary exists:** `results/<RUNNAME>/summary.txt`
5. **Config snapshot exists:** `results/<RUNNAME>/config_snapshot.do`
6. **Manifest exists:** `results/<RUNNAME>/manifest.json` (optional)

Also scan _WorkSpace output:
7. **Heavy assets created:** check `_WorkSpace/{N}-*Store/<asset>/year-<year>/` has `.dta` files
8. **No .dta in results/:** confirm results/ is light-only

### Step 2 — Generate per-script reports

Mirror each `plan-script-*.yaml`, filling status per step:

```yaml
name: <same as plan>
plan: workflow/plan-script-<name>.yaml
reported_at: "<timestamp>"

phases:
  - title: "<Phase from plan>"
    steps:
      - label: "<phase>:<step>"
        status: done | skipped | failed
        files_in: [actual files read]
        files_out: [actual files created]
        output:
          log_clean: true | false
          rows: <from summary.txt if available>
          error: "<r(NNN) message if failed>"
        note: "<observation>"

summary:
  status: ok | incomplete | failed
  phases_completed: "N/N"
  steps_done: X
  steps_skipped: Y
  steps_failed: Z
  verdict: pass | warn | fail
```

**How to determine step status:**
- `done`: output .dta exists + log has no `r(...)` errors
- `skipped`: topic flag = 0 (read from config) or output pre-existed (skip log)
- `failed`: log contains `r(...)` error OR output .dta missing when expected

### Step 3 — Generate task-level report.yaml

Roll up script reports. Use the same IPO preview tree as plan.yaml but annotated
with completion status:

```yaml
# --- Preview -----------------------------------------------------------
# <task_name> — execution report
#
# I: <inputs> ✅|❌
#
# +-- emoji P1: <phase>   ✅ done N/N steps
# +-- emoji P2: QC        ✅ done
#
# O: status=ok  phases=N/N  steps=X done, Y skipped
#    _WorkSpace used: ...
#    _WorkSpace generated: ...
# -------------------------------------------------------------------

name: <task_name>
plan: workflow/plan.yaml
reported_at: "<timestamp>"

execution:
  mode: manual | auto
  agents_used: []
  skills_used: [haipipe-task-for-stata]

phases:
  - title: "<Phase>"
    steps:
      - label: "<phase>:<step>"
        status: done | skipped | failed
        files_out: [...]
        note: "..."

summary:
  status: ok | incomplete | failed
  phases_completed: "N/N"
  steps_done: X
  steps_skipped: Y
  steps_failed: Z
  verdict: pass | warn | fail
  issues: []
```

### Step 4 — Synth vs full traceability

If config_snapshot.do exists, extract and report:
- `case_asset_name` / `case_asset_version` → confirms synth or full build
- `cms_source` → synth or full
- Compare snapshot globals against live config — flag any drift

### Step 5 — Report

```
📋 Report: <task_name>
   phases: N/N complete
   steps: X done, Y skipped, Z failed
   verdict: <pass|warn|fail>
   _WorkSpace:
     input:  1-CMS-Store/... ✅
     output: 2-Case-Store/... ✅ (N years, M panels/yr)
```


Return contract
---------------

```yaml
status: ok | incomplete | failed
report_path: workflow/report.yaml
script_reports: [workflow/report-script-*.yaml]
phases_completed: "N/N"
steps_done: X
steps_total: Y
verdict: pass | warn | fail
```
