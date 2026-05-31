# =============================================================================
# Template for runs/<RUN>.ps1   —  STATA DIALECT
# =============================================================================
# Stata analog of run-sh-template.sh. A thin wrapper that:
#   1. Resolves identity (RUNNAME) from this script's own path.
#   2. Precondition-checks required inputs (fail early if missing).
#   3. Pre-flight code-review gate (CODE_REVIEW.md), portable skip flags.
#   4. Snapshots config (.do + .yaml) into results/<RUN>/.
#   5. Writes runtime.yaml (status: running), atomically.
#   6. Runs the Stata steps via the task's run_<stage>_year.ps1 orchestrator.
#   7. Finalizes runtime.yaml (status: ok|failed, duration, exit_code, headline).
#   8. Regenerates task-log.md via haipipe-task-logging/ref/regen_task_log.py.
#
# Variables you MUST set (section 1). Everything else derives from $PSScriptRoot.
# See ../../haipipe-task/ref/stata-dialect.md for the full contract.
# =============================================================================

$ErrorActionPreference = "Stop"

# ─── 1. What this run is (EDIT THESE) ────────────────────────────────────────
$RUNNAME   = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Path)  # = run_cms_2015
$CFG       = "cms_production"          # configs/<CFG>.do  (Stata globals, source of truth)
$STATA     = "C:\Program Files\Stata18\StataMP-64.exe"
# Precondition inputs (absolute or repo-relative). Empty list = no check.
$REQUIRED  = @(
    # "_WorkSpace\1-CMS-Store\cms_full\v0001_0130\year-2015\PDE-Neat-2015.dta"
)

# ─── 2. Resolve identity from this script's path ─────────────────────────────
$TASK_DIR   = Split-Path -Parent $PSScriptRoot      # ...\{NN}_{stage}_pipeline
$REPO_ROOT  = (& git -C $TASK_DIR rev-parse --show-toplevel).Trim()
$RESULTS    = Join-Path $TASK_DIR "results\$RUNNAME"
$LOG_DIR    = Join-Path $RESULTS "log"
$RUNTIME    = Join-Path $RESULTS "runtime.yaml"
$CFG_DO     = Join-Path $TASK_DIR "configs\$CFG.do"
$CFG_YAML   = Join-Path $TASK_DIR "configs\$RUNNAME.yaml"     # _meta block (this dialect)
$STARTED    = (Get-Date).ToString("o")
$GIT_SHA    = (& git -C $TASK_DIR rev-parse --short HEAD 2>$null); if (-not $GIT_SHA) { $GIT_SHA = "unknown" }
$HOSTID     = "$(hostname)/$env:USERNAME"
$CMD        = "pwsh $($MyInvocation.MyCommand.Path)"

# ─── 3. Precondition check ───────────────────────────────────────────────────
$missing = @()
foreach ($f in $REQUIRED) { if (-not (Test-Path $f)) { $missing += $f } }
if (-not (Test-Path $CFG_DO)) { $missing += $CFG_DO }
if ($missing) {
    Write-Error ("[$RUNNAME] Missing required inputs:`n  - " + ($missing -join "`n  - "))
    exit 1
}

# ─── 3a. Pre-flight code-review gate ─────────────────────────────────────────
# Skip via _meta.skip_review: true in <run>.yaml, or $env:HAIPIPE_SKIP_REVIEW=1.
$CODE_REVIEW = Join-Path $TASK_DIR "CODE_REVIEW.md"
$skipCfg = (Test-Path $CFG_YAML) -and (Select-String -Path $CFG_YAML -Pattern '^\s*skip_review:\s*true\b' -Quiet)
if ($skipCfg -or $env:HAIPIPE_SKIP_REVIEW -eq "1") {
    Write-Host "==> [pre-flight] code review SKIPPED (explicit skip flag)"
} elseif (-not (Test-Path $CODE_REVIEW)) {
    Write-Error ("[$RUNNAME] BLOCKED: no CODE_REVIEW.md in $TASK_DIR`n" +
                 "    Run the Run Script Reviewer agent, or set `$env:HAIPIPE_SKIP_REVIEW=1.")
    exit 2
} else {
    $verdict = (Select-String -Path $CODE_REVIEW -Pattern '^- overall_verdict:\s*(\S+)' |
                ForEach-Object { $_.Matches[0].Groups[1].Value } | Select-Object -First 1)
    switch ($verdict) {
        { $_ -in 'pass','skipped','warn' } { Write-Host "==> [pre-flight] code review verdict=$verdict (proceeding)" }
        default { Write-Error "[$RUNNAME] BLOCKED: code review verdict='$verdict' (expected pass|warn|skipped)"; exit 2 }
    }
}

# ─── 4. Prepare results dir + snapshot config ────────────────────────────────
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null
Copy-Item $CFG_DO (Join-Path $RESULTS "config_snapshot.do") -Force
if (Test-Path $CFG_YAML) { Copy-Item $CFG_YAML (Join-Path $RESULTS "config_snapshot.yaml") -Force }

# ─── 5. runtime.yaml (status: running, atomic) ───────────────────────────────
function Write-Runtime([hashtable]$kv) {
    $lines = $kv.GetEnumerator() | ForEach-Object { "{0,-11} {1}" -f ($_.Key + ":"), $_.Value }
    Set-Content -Path "$RUNTIME.tmp" -Value $lines -Encoding utf8
    Move-Item "$RUNTIME.tmp" $RUNTIME -Force
}
Write-Runtime ([ordered]@{
    status = "running"; started = $STARTED; git_sha = $GIT_SHA; host = $HOSTID
    cmd = $CMD; config = "configs/$RUNNAME.yaml"; notebook = "results/$RUNNAME/log/"
})

# ─── 6. Execute the Stata steps via the per-stage orchestrator ───────────────
$EXIT = 0
try {
    & pwsh -File (Join-Path $TASK_DIR "run_<stage>_year.ps1") -cfg $CFG -resultsDir $RESULTS
    $EXIT = $LASTEXITCODE
} catch {
    $EXIT = 1
    Write-Warning $_.Exception.Message
}

# ─── 7. Finalize runtime.yaml ────────────────────────────────────────────────
$ENDED = (Get-Date).ToString("o")
$dur   = [datetime]$ENDED - [datetime]$STARTED
$DURATION = if ($dur.Hours) { "{0}h{1:00}m" -f $dur.Hours, $dur.Minutes } else { "{0}m{1:00}s" -f $dur.Minutes, $dur.Seconds }
$STATUS = if ($EXIT -eq 0) { "ok" } else { "failed" }
# Headline: prefer first non-empty line of summary.txt; else "-".
$summaryFile = Join-Path $RESULTS "summary.txt"
$HEADLINE = "-"
if (Test-Path $summaryFile) {
    $h = Get-Content $summaryFile | Where-Object { $_.Trim() } | Select-Object -First 1
    if ($h) { $HEADLINE = $h.Trim() }
}
Write-Runtime ([ordered]@{
    status = $STATUS; started = $STARTED; ended = $ENDED; duration = $DURATION
    git_sha = $GIT_SHA; host = $HOSTID; exit_code = $EXIT; cmd = $CMD
    config = "configs/$RUNNAME.yaml"; notebook = "results/$RUNNAME/log/"; headline = $HEADLINE
})

# ─── 8. Regenerate task-log.md ───────────────────────────────────────────────
$regen = Join-Path $REPO_ROOT "Tools\plugins\haipipe-toolkit\skills\C_task\haipipe-task-logging\ref\regen_task_log.py"
if (Test-Path $regen) {
    try { & python $regen $TASK_DIR } catch { Write-Warning "task-log regen failed (non-fatal)" }
}

Write-Host "[$RUNNAME] done (status=$STATUS, $DURATION). results: $RESULTS"
exit $EXIT
