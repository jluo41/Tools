# run_<stage>_year.ps1 - ORCHESTRATOR: one run (one year), steps in dependency phases
# Contract: do <NN>_<stage>_pipeline.do <cfg> <step> <year> <results_dir> <ws_root>
# EDIT the <placeholders>: dispatcher name, stage name, step names, phase grouping.
# Phase rule: independent steps -> one parallel block; dependent steps -> -Wait, in order.
param([string]$cfg = "<cfg>", [string]$year = "2015")

$stata = "C:\Program Files\Stata18\StataMP-64.exe"   # server exe; edit this ONE line per machine
$dir   = $PSScriptRoot                               # task folder = Stata working dir (configs/, scripts/ resolve relative)
$ws    = $dir; while ($ws -and -not (Test-Path "$ws\pyproject.toml")) { $ws = Split-Path $ws }
$base  = "do <NN>_<stage>_pipeline.do $cfg"
$tail  = "`"$dir\results\run_<stage>_$year`" `"$ws\_WorkSpace`""   # results_dir + ws_root, both absolute

# phase 1: independent steps, parallel (~32GB RAM per Stata job; keep <= 4)
$jobs = "<step_a>","<step_b>","<step_c>" |
        ForEach-Object { Start-Process $stata "/e $base $_ $year $tail" -WorkingDirectory $dir -PassThru }
$jobs | Wait-Process

# phase 2: dependent steps, sequential
Start-Process $stata "/e $base <dependent_step> $year $tail" -WorkingDirectory $dir -PassThru -Wait
Start-Process $stata "/e $base summary $year $tail" -WorkingDirectory $dir -PassThru -Wait
Write-Host "Year $year done."
