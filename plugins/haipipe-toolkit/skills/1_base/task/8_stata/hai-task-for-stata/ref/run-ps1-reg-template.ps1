# runs/rNN_<run>/rNN_<run>.ps1 -- self-contained reg ticket: <estimator> family, <window> window. EDIT: $workers.
# Current practice is the two-line caller into the Job's shared runner, whose body this file stands in for:
#   & "$PSScriptRoot\..\..\..\src\0-libs\run-regression-pipeline.ps1" "$PSScriptRoot\config.do"
# result\ = what a reader reviews (RUN-REPORT.md, tables\, describe\); passes\pNN-<MMDD>\ = this execution's logs, .done, runtime.yaml. Flat runs\<run>.ps1: results\<run>\.
$ErrorActionPreference = "Stop"
$RUN  = [IO.Path]::GetFileNameWithoutExtension($PSCommandPath)
$FLAT = (Split-Path -Leaf $PSScriptRoot) -eq "runs"
$TASK_DIR = if ($FLAT) { Split-Path -Parent $PSScriptRoot } else { Split-Path -Parent (Split-Path -Parent $PSScriptRoot) }
$TASK     = Split-Path -Leaf $TASK_DIR
$CFG_REL  = if ($FLAT) { "scripts/config/$RUN.do" } else { "runs/$RUN/config.do" }
if (-not (Test-Path (Join-Path $TASK_DIR $CFG_REL))) { Write-Error "config not found: $TASK_DIR\$CFG_REL"; exit 1 }
$OUTPUT_ROOT = if ($env:OUTPUT_ROOT) { $env:OUTPUT_ROOT } else { Split-Path -Parent $TASK_DIR }
if ($FLAT) {
    $RESULT = Join-Path $OUTPUT_ROOT "$TASK\results\$RUN"; $PASS = $RESULT
} else {
    $RUN_OUT = Join-Path $OUTPUT_ROOT "$TASK\runs\$RUN"
    $RESULT  = Join-Path $RUN_OUT "result"
    $n = @(Get-ChildItem (Join-Path $RUN_OUT "passes") -Directory -Filter "p*" -ErrorAction SilentlyContinue).Count + 1
    $PASS = Join-Path $RUN_OUT ("passes\p{0:D2}-{1}" -f $n, (Get-Date -Format "MMdd"))
}
$WS_ROOT  = $TASK_DIR
while ($WS_ROOT -and -not (Test-Path (Join-Path $WS_ROOT "pyproject.toml"))) {
    $WS_ROOT = Split-Path -Parent $WS_ROOT
}
if (-not $WS_ROOT) { Write-Error "repo root (pyproject.toml) not found above $TASK_DIR"; exit 1 }
function Resolve-StataExe {
    if ($env:HAIPIPE_STATA -and (Test-Path $env:HAIPIPE_STATA)) { return $env:HAIPIPE_STATA }
    foreach ($edition in @("StataMP-64.exe","StataSE-64.exe","StataBE-64.exe","Stata-64.exe")) {
        $hit = Get-ChildItem "C:\Program Files\Stata*\$edition" -ErrorAction SilentlyContinue |
               Sort-Object { [int]($_.Directory.Name -replace '\D','') } -Descending |
               Select-Object -First 1 -ExpandProperty FullName
        if ($hit) { return $hit }
    }
    return $null
}
$stata = Resolve-StataExe
if (-not $stata) { Write-Error "No Stata found under 'C:\Program Files\Stata*\' (or set `$env:HAIPIPE_STATA)."; exit 1 }
$env:HAIPIPE_WS_ROOT    = Join-Path $WS_ROOT "_WorkSpace"
$env:HAIPIPE_RUN_CONFIG = $CFG_REL
$env:HAIPIPE_RUN_RESULT = $RESULT
$env:HAIPIPE_PASS_DIR   = $PASS
New-Item -ItemType Directory -Force -Path $RESULT, (Join-Path $PASS "log") | Out-Null
Write-Host "[$RUN] task $TASK_DIR -> $RESULT (pass $PASS)"
$workers = @(
    "<worker-1>.do",
    "<worker-2>.do"
)
Push-Location $TASK_DIR
try {
    foreach ($w in $workers) {
        Write-Host "  -> $w"
        & $stata /e do "scripts/$w"
        if ($LASTEXITCODE -ne 0) { throw "Stata worker failed: $w ($LASTEXITCODE)" }
    }
} finally { Pop-Location }
Write-Host "done: $RUN"
