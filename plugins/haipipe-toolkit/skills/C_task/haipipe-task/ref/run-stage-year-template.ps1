# =============================================================================
# Template for run_<stage>_year.ps1   —  STATA DIALECT  (intra-run ORCHESTRATOR)
# =============================================================================
# Lives at the TASK-FOLDER ROOT (next to the dispatcher <NN>_<stage>_pipeline.do).
# Internal helper: called by runs/<RUN>.ps1; NOT invoked directly by a human.
#
# Responsibilities:
#   1. Resolve the Stata exe WITHOUT hardcoding a version (local 17 vs server 18).
#   2. Run Stata from the task folder ($PSScriptRoot) so the dispatcher's
#      task-folder-relative paths (configs/, scripts/) resolve.
#   3. Sequence the dispatcher's steps in dependency-correct PHASES, with
#      within-phase parallelism via Start-Process ... -PassThru | Wait-Process.
#   4. Pass the ABSOLUTE data root (<ws_root>) straight through to the dispatcher
#      so NOTHING counts "../.." or assumes tree depth or the folder's own name.
#
# Contract with the dispatcher (see ref/dispatcher-do-template.do):
#   do <NN>_<stage>_pipeline.do <cfg> <step> <year> <results_dir> <ws_root>
#
# See ref/stata-dialect.md for the full engine contract.
# =============================================================================

param(
    [Parameter(Mandatory=$true)][string]$cfg,
    [Parameter(Mandatory=$true)][string]$year,
    [Parameter(Mandatory=$true)][string]$resultsDir,
    [Parameter(Mandatory=$true)][string]$wsRoot       # absolute path to _WorkSpace (resolved by the runner)
)

# ─── Resolve the Stata executable without hardcoding a version ───────────────
# Order: explicit override ($env:HAIPIPE_STATA) -> newest StataMP (pipelines
# assume MP) -> newest of any edition (SE/BE/base) -> $null. Handles local-dev
# vs server version differences (e.g. Stata17 local, Stata18 server) with no
# per-machine edits.
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
if (-not $stata) {
    Write-Error "No Stata found. Install StataMP/SE/BE under 'C:\Program Files\Stata*\' or set `$env:HAIPIPE_STATA to the .exe."
    exit 1
}

# ─── Run from the task-folder root; paths inside the dispatcher are relative ──
$cmsRoot = $PSScriptRoot   # this file lives at the task-folder root; run Stata from here
$base    = "do <NN>_<stage>_pipeline.do $cfg"   # EDIT: the dispatcher filename (name is free)
$tail    = "`"$resultsDir`" `"$wsRoot`""         # results_dir + ws_root, both absolute, both quoted

Write-Host "=== <stage> year $year starting (Stata: $stata) ==="
Write-Host "    results : $resultsDir"
Write-Host "    ws_root : $wsRoot"

# ─── Phases (EDIT for your stage's dependency graph) ─────────────────────────
# Example below is the CMS extract shape: 4 independent extracts in parallel,
# then bene_year (needs PDE output), then summary. Replace step names / phase
# structure to match your stage.
#
# Phase 1: independent steps in parallel
$p1 = @(
    Start-Process $stata -ArgumentList "/e $base pde           $year $tail" -WorkingDirectory $cmsRoot -PassThru
    Start-Process $stata -ArgumentList "/e $base carrier_claim $year $tail" -WorkingDirectory $cmsRoot -PassThru
    Start-Process $stata -ArgumentList "/e $base carrier_line  $year $tail" -WorkingDirectory $cmsRoot -PassThru
    Start-Process $stata -ArgumentList "/e $base outpatient    $year $tail" -WorkingDirectory $cmsRoot -PassThru
)
$p1 | Wait-Process
Write-Host "<stage> year $year Phase 1 done."

# Phase 2: dependent step(s), sequential
Start-Process $stata -ArgumentList "/e $base bene_year $year $tail" -WorkingDirectory $cmsRoot -PassThru -Wait
Write-Host "<stage> year $year Phase 2 done."

# Phase 3: summary (light artifact: writes summary.txt into $resultsDir)
Start-Process $stata -ArgumentList "/e $base summary $year $tail" -WorkingDirectory $cmsRoot -PassThru -Wait
Write-Host "<stage> year $year Phase 3 done."
