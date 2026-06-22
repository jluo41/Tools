fn/audit-stata — Stata-aware pre-flight audit
===============================================

Extends the generic four-sister audit (`../../haipipe-task/fn/workflow-audit.md`) with Stata-engine-specific checks. Runs as an overlay — the generic audit runs first, then this adds Stata items.


When to call
------------

Automatically as part of the `/haipipe-task` lifecycle on any existing Stata task folder. Also callable standalone:
`/haipipe-task-for-stata audit <task-folder-path>`


Procedure
---------

### Step 0 — Run generic audit first

Execute `../../haipipe-task/fn/workflow-audit.md` Steps 1-6 to get the baseline four-sister report (run_names, sisters, issues, type detection).

### Step 1 — Detect stage

Same cascade as `fn/plan-stata.md` Step 1. Must know stage before checking stage-specific patterns.

### Step 2 — Three-layer config check (case stage)

If stage=case, verify the three-layer config pattern:

1. **Source selectors exist:** `configs/_source_synth.do` and `configs/_source_full.do`
2. **Shared cohort config exists:** `configs/<Cohort>.do` (the one WITHOUT source/year suffix)
3. **Per-run configs exist:** `configs/<Cohort>_{synth|full}_{year}.do` for each runner
4. **Loading order:** Each per-run config loads source selector THEN shared config
   (grep for `do configs/_source_` appearing BEFORE `do configs/<Cohort>.do`)
5. **Source tag in output:** `case_asset_name` does NOT contain `${cms_source}`
   (source goes in VERSION not NAME per current convention)

Issue types:
- `missing_source_selector` — FIXABLE (generate from template)
- `missing_shared_config` — FAIL (cannot generate; needs authoring)
- `missing_per_run_config` — FIXABLE (generate thin wrapper from `ref/config-seed-run.do`)
- `wrong_loading_order` — WARN (source selector must load before cohort config)
- `source_in_asset_name` — WARN (convention: source goes in version, not name)

### Step 3 — STATATMP check

Grep all `.ps1` files (orchestrator + runners) for `STATATMP`:

1. **Orchestrator sets STATATMP:** grep `run_case_year.ps1` (or equivalent) for
   `$env:STATATMP` BEFORE any `Start-Process $stata`
2. **Describe runner sets STATATMP:** grep `run_describe_*.ps1` for `$env:STATATMP`

Cross-reference with `preserve`/`tempfile`/`tempvar` usage in `.do` files:
- grep all `scripts/**/*.do` for `\bpreserve\b|\btempfile\b|\btempvar\b`
- If any .do uses these AND orchestrator doesn't set STATATMP → CRITICAL

Issue types:
- `statatmp_missing` — CRITICAL if preserve/tempfile used; INFO otherwise
- `preserve_usage` — INFO (list files and lines)

### Step 4 — SSC dependency scan

Grep all `.do` files for known SSC commands:

```
rangejoin  distinct  ftools  gtools  fmerge  fcollapse
estout  outreg2  coefplot  reghdfe  binscatter  ssc
```

Each hit is a potential FAIL on the CMS server (clean Stata, no SSC, no internet).

Issue types:
- `ssc_dependency` — FAIL per command found (file, line, command)
- `ssc_install` — FAIL (any `ssc install` line is dead on server)

### Step 5 — Topic flag consistency (case stage)

If stage=case, verify topic flags:

1. Read `configs/<Cohort>.do` for `global run_topic_*` definitions
2. Read `case_pipeline.do` for dispatcher branches that check those flags
3. Read `run_case_year.ps1` for `Get-TopicFlag` calls
4. Verify: every topic flag defined in config has a matching dispatcher branch
   AND a matching orchestrator block

Issue: `topic_flag_mismatch` — WARN (flag defined but no dispatcher branch, or vice versa)

### Step 6 — CMS server readiness (Gate 2 pre-flight)

Quick scan for the most common CMS server failure modes:

| Check | How | Severity |
|-------|-----|----------|
| PS7 syntax | grep .ps1 for `&&` `\|\|` `?:` `??` | FAIL |
| pwsh calls | grep .ps1 for `\bpwsh\b` | FAIL |
| Non-ASCII in .ps1 | byte-scan for >127 | WARN |
| Start-Job usage | grep .ps1 for `Start-Job` | WARN (constrained lang mode) |
| Exit code checking | grep orchestrator for `ExitCode` | WARN if absent |
| Stata exe resolution | grep orchestrator for Resolve-StataExe or `$stata` | INFO |

These overlap with `/cms-server-checklist` Gate 2 items B1-C6. This audit is a quick scan; the full checklist is the definitive check.

### Step 7 — Orphan / stale results

Extend generic audit's stale_result classification:
- Results folders matching old naming conventions (pre-source-dimension: `run_case_<Cohort>_<year>/` without source tag) → `stale_naming`
- Results folders with `_v2603` or other version suffixes → `stale_versioned`
- Results under `_old/` → `archived` (INFO, no action)

### Step 8 — Report

Extend the generic audit report with Stata-specific sections:

```
📋 Audit: <task_folder>
   stage: <detected>
   
   Four-sister check: (from generic audit)
     ...
   
   Stata checks:
     Three-layer config: ok | N issues
     STATATMP: set | MISSING (preserve used in N files)
     SSC deps: none | N commands (rangejoin in 12 files)
     Topic flags: consistent | N mismatches
     CMS readiness: N issues (quick scan)
   
   Issues (N fixable, M warn, K fail):
     ...
```


Return contract
---------------

```yaml
status: ok | issues_found
stage: <cms|case|data|reg>
generic_audit: { ... }     # from parent audit
stata_checks:
  config_layers: ok | N issues
  statatmp: set | missing
  ssc_deps: [{ command, file, line }]
  topic_flags: consistent | N mismatches
  cms_readiness: N issues
issues: [{ id, type, severity, file, line, detail }]
```
