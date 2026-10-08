# run_<stage>_year.ps1 -- per-year orchestrator (short controller with required checks)
# EDIT: param defaults, $stata path, dispatcher name, step names, step grouping.
param([string]$cfg = "rNN_<run>", [string]$year = "", [string]$resultsDir)
$ErrorActionPreference = "Stop"
$stata = if ($env:HAIPIPE_STATA) { $env:HAIPIPE_STATA } else { "C:\Program Files\Stata18\StataMP-64.exe" }
$dir = Split-Path -Parent $PSScriptRoot
$ws = $dir
while ($ws -and -not (Test-Path "$ws\pyproject.toml")) { $ws = Split-Path $ws }
if (-not $ws) { Write-Error "pyproject.toml not found above $dir"; exit 1 }
if (-not (Test-Path "$dir\scripts\config\$cfg.do")) { Write-Error "config not found: scripts\config\$cfg.do"; exit 1 }
$cfgText = Get-Content "$dir\scripts\config\$cfg.do" -Raw
if ($cfgText -notmatch '(?m)^\s*global\s+data_year\s+"?(\d{4})"?\s*$') { throw "Per-run config must pin data_year" }
$configYear = $Matches[1]
if ($year -and $year -ne $configYear) { throw "Ticket year differs from config data_year" }
$year = $configYear
$wsRoot = "$ws\_WorkSpace"
if (-not $resultsDir) { throw "Pass the resolved OUTPUT_ROOT/<task>/results/<run> path" }
New-Item -ItemType Directory -Force -Path "$resultsDir\log" | Out-Null
if (-not $env:STATATMP) { $env:STATATMP = "$resultsDir\tmp" }
New-Item -ItemType Directory -Force -Path $env:STATATMP | Out-Null
$base = "do scripts/<stage>_pipeline.do $cfg"
$tail = "`"$resultsDir`" `"$wsRoot`""

# Step group 1: independent steps in parallel
$p1 = @(
    Start-Process $stata -ArgumentList "/e $base <step_a> $year $tail" -WorkingDirectory $dir -PassThru
    Start-Process $stata -ArgumentList "/e $base <step_b> $year $tail" -WorkingDirectory $dir -PassThru
)
$p1 | Wait-Process
foreach ($child in $p1) { $child.Refresh(); if ($child.ExitCode -ne 0) { throw "Extraction worker failed: $($child.ExitCode)" } }
# Step group 2: dependent step (sequential)
$child = Start-Process $stata -ArgumentList "/e $base <dependent_step> $year $tail" -WorkingDirectory $dir -PassThru -Wait
if ($child.ExitCode -ne 0) { throw "Stata worker failed: $($child.ExitCode)" }
# Step group 3: summary
$child = Start-Process $stata -ArgumentList "/e $base summary $year $tail" -WorkingDirectory $dir -PassThru -Wait
if ($child.ExitCode -ne 0) { throw "Stata worker failed: $($child.ExitCode)" }
Write-Host "[run_<stage>_$year] done."
