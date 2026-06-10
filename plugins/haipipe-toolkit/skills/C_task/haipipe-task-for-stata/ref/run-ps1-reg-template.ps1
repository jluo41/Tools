# runs/run_reg_<RUNNAME>.ps1 -- <estimator> family, <window> window
$ErrorActionPreference = "Stop"
$TASK_DIR = Split-Path -Parent $PSScriptRoot
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
$env:HAIPIPE_WS_ROOT   = Join-Path $WS_ROOT "_WorkSpace"
$env:HAIPIPE_RUN_CONFIG = "<RUNNAME>"
$workers = @(
    "<worker-1>.do",
    "<worker-2>.do"
)
Push-Location $TASK_DIR
try {
    foreach ($w in $workers) { Write-Host "  -> $w"; & $stata /e do "scripts/$w" }
} finally { Pop-Location }
Write-Host "done: <RUNNAME>"
