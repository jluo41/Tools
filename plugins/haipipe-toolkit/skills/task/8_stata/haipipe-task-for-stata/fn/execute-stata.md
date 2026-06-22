fn/execute-stata — Two-mode Stata execution
=============================================

Stata tasks execute via PowerShell runners (`.ps1`), NOT Python/papermill. Two modes: local (laptop, synth) vs server (CMS, full/real). The server is an isolated machine — Claude never runs the real pipeline.


When to call
------------

As Stage 3 of the `/haipipe-task` lifecycle on a Stata task folder.
Also callable standalone: `/haipipe-task-for-stata execute <task-folder-path>`


Two modes
---------

### Mode A: Local (laptop, synth config)

For synth data runs on the developer's laptop.

```
Step 1 — Pre-flight
  - Run fn/audit-stata.md (if not already done)
  - Check: configs/_source_synth.do exists
  - Check: _WorkSpace/1-CMS-Store/cms_synth/ has year dirs

Step 2 — Execute
  - Run: powershell runs/run_case_<Cohort>_synth_<year>.ps1
  - Or batch: powershell sbatch/run_all_2015-2020_synth.ps1

Step 3 — Post-run
  - Scan logs for r(...) errors
  - Check summary.txt row counts
  - Run fn/report-stata.md to generate report
```

### Mode B: Server (CMS, full config)

For real CMS data runs on the isolated secure server.
Claude edits code locally; the user hand-copies to the server and runs.

```
Step 1 — Pre-flight (local, before shipping)
  - Run fn/audit-stata.md
  - Run /cms-server-checklist (Gate 1 + Gate 2)
  - Fix any FAIL items
  - Generate CODE_REVIEW.md and SERVER_CHECK.md

Step 2 — Package (local)
  - List all files to copy (from SERVER_CHECK.md "Files to copy")
  - Exclude: results/, _WorkSpace/, .dta, .csv, .log, .git/
  - Include: *.do, *.ps1, *.yaml, *.md

Step 3 — Hand-copy (user action)
  - User copies code zip to CMS server
  - User edits $stata path if needed (D1 portability rule)
  - User sets $env:STATATMP if not already in orchestrator

Step 4 — Execute (server, user action)
  - User runs: powershell runs/run_case_<Cohort>_full_<year>.ps1
  - Or batch: powershell sbatch/run_all_2015-2020_real.ps1

Step 5 — Feedback loop (user → Claude)
  - User pastes server output / errors back to Claude
  - Claude diagnoses, fixes code locally
  - Run /cms-server-checklist Gate 3 on server output
  - Repeat from Step 1 until clean

Step 6 — Post-run
  - User copies results/ back (logs + summary only, no .dta)
  - Run fn/report-stata.md locally
```


Key rules
---------

- Claude NEVER runs the real CMS pipeline — only edits + local checks
- User's server output is the SOLE ground truth
- Every reply that changes code MUST end with a change-list:
  exact files + line edits to hand-port to the server
- Watch scope: a fix usually hits ALL estimator folders × ALL cohorts


Execution checklist (quick reference)
--------------------------------------

```
LOCAL SYNTH:
  [ ] audit-stata passed
  [ ] synth configs present (_source_synth.do)
  [ ] CMS synth store exists
  [ ] Run: powershell runs/run_*_synth_*.ps1
  [ ] Logs clean (no r(...) errors)
  [ ] Summary row counts > 0

SERVER FULL:
  [ ] audit-stata passed
  [ ] cms-server-checklist Gate 2 passed
  [ ] CODE_REVIEW.md + SERVER_CHECK.md generated
  [ ] Package code (no data)
  [ ] Hand-copy to server
  [ ] User runs powershell runs/run_*_full_*.ps1
  [ ] User pastes output
  [ ] cms-server-checklist Gate 3 (first real run)
  [ ] report-stata generated
```


Return contract
---------------

```yaml
status: ok | blocked | manual
mode: local | server
executed_runs: [list of RUNNAMEs]
gate1_verdict: pass | warn | fail    # CODE_REVIEW.md
gate2_verdict: pass | warn | fail    # SERVER_CHECK.md (server mode)
gate3_verdict: pass | pending | fail # first real-data run (server mode)
next: "<what to do next>"
```
