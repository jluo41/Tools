# run_<stage>_year.ps1 -- per-year runner for ORCHESTRATED stages (cms/case), in the Job's src/ (or a Task's scripts/ when one Task uses it).
# Arg: the config that IS the Run: runs/<run>/config.do (a Run folder) or scripts/config/<run>.do (a flat Block not yet moved).
# The Task is found from that config, never from this file's own folder. Result: <OUTPUT_ROOT>/<task>/runs/<run>/result (flat: results/<run>).
# EDIT: $stata path, dispatcher name, step names, step grouping.
param([Parameter(Mandatory)][string]$ConfigPath, [string]$year = "")
$ErrorActionPreference = "Stop"
$stata = if ($env:HAIPIPE_STATA) { $env:HAIPIPE_STATA } else { "C:\Program Files\Stata18\StataMP-64.exe" }
$cfgFile = (Resolve-Path $ConfigPath).Path
$cfgDir = Split-Path -Parent $cfgFile
$flat = (Split-Path -Leaf $cfgFile) -ne "config.do"
$run = if ($flat) { [IO.Path]::GetFileNameWithoutExtension($cfgFile) } else { Split-Path -Leaf $cfgDir }
$dir = Split-Path -Parent (Split-Path -Parent $cfgDir)
if ((Split-Path -Leaf $dir) -notmatch '^t\d\d_') { throw "config is not inside a tNN_ Task folder: $cfgFile" }
$cfgRel = $cfgFile.Substring($dir.Length + 1) -replace '\\', '/'
$outputRoot = if ($env:OUTPUT_ROOT) { $env:OUTPUT_ROOT } else { Split-Path -Parent $dir }
$task = Split-Path -Leaf $dir
$resultsDir = if ($flat) { Join-Path $outputRoot "$task\results\$run" } else { Join-Path $outputRoot "$task\runs\$run\result" }
$ws = $dir
while ($ws -and -not (Test-Path (Join-Path $ws "pyproject.toml"))) { $ws = Split-Path $ws }
if (-not $ws) { Write-Error "pyproject.toml not found above $dir"; exit 1 }
$cfgText = Get-Content $cfgFile -Raw
if ($cfgText -notmatch '(?m)^\s*global\s+data_year\s+"?(\d{4})"?\s*$') { throw "Per-run config must pin data_year" }
$configYear = $Matches[1]
if ($year -and $year -ne $configYear) { throw "Ticket year differs from config data_year" }
$year = $configYear
$wsRoot = Join-Path $ws "_WorkSpace"
Write-Host "[$run] task $dir -> $resultsDir"
New-Item -ItemType Directory -Force -Path (Join-Path $resultsDir "log") | Out-Null
# Stata temp files hold CMS rows: they go to _WorkSpace, never into result/, which travels back.
if (-not $env:STATATMP) { $env:STATATMP = Join-Path $wsRoot "_stata-tmp\$run" }
New-Item -ItemType Directory -Force -Path $env:STATATMP | Out-Null
$base = "do scripts/<stage>_pipeline.do $cfgRel"
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
Write-Host "[$run] done."
