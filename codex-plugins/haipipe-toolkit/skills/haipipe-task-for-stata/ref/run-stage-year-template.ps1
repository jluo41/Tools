# run_<stage>_year.ps1 -- per-year orchestrator (<=30 lines)
# EDIT: param defaults, $stata path, dispatcher name, step names, phase grouping.
param([string]$cfg = "<cfg>", [string]$year = "2015")
$ErrorActionPreference = "Stop"
$stata = "C:\Program Files\Stata18\StataMP-64.exe"
$dir = $PSScriptRoot
$ws = $dir
while ($ws -and -not (Test-Path "$ws\pyproject.toml")) { $ws = Split-Path $ws }
if (-not $ws) { Write-Error "pyproject.toml not found above $dir"; exit 1 }
if (-not (Test-Path "$dir\configs\$cfg.do")) { Write-Error "config not found: configs\$cfg.do"; exit 1 }
$wsRoot = "$ws\_WorkSpace"
$resultsDir = "$dir\results\run_<stage>_$year"
New-Item -ItemType Directory -Force -Path "$resultsDir\log" | Out-Null
if (-not $env:STATATMP) { $env:STATATMP = "$resultsDir\tmp" }
New-Item -ItemType Directory -Force -Path $env:STATATMP | Out-Null
$base = "do <NN>_<stage>_pipeline.do $cfg"
$tail = "`"$resultsDir`" `"$wsRoot`""

# Phase 1: independent steps in parallel
$p1 = @(
    Start-Process $stata -ArgumentList "/e $base <step_a> $year $tail" -WorkingDirectory $dir -PassThru
    Start-Process $stata -ArgumentList "/e $base <step_b> $year $tail" -WorkingDirectory $dir -PassThru
)
$p1 | Wait-Process
# Phase 2: dependent step (sequential)
Start-Process $stata -ArgumentList "/e $base <dependent_step> $year $tail" -WorkingDirectory $dir -PassThru -Wait
# Phase 3: summary
Start-Process $stata -ArgumentList "/e $base summary $year $tail" -WorkingDirectory $dir -PassThru -Wait
Write-Host "[run_<stage>_$year] done."
