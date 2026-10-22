# runs/rNN_<run>/rNN_<run>.ps1 -- self-orchestrating data-stage ticket (no year axis; the runner IS the orchestrator).
# Current practice is the two-line caller into the Job's shared runner, whose body this file stands in for:
#   & "$PSScriptRoot\..\..\..\src\0-libs\run-data-pipeline.ps1" "$PSScriptRoot\config.do"
# EDIT: $COHORT, $DESIGN, conditional input paths. A flat runs\<run>.ps1 (a Block not yet moved) reads scripts\config\<run>.do, writes results\<run>\.
$ErrorActionPreference = "Stop"

# ---- 1. Identity ----
$COHORT  = "<Cohort>"
$DESIGN  = "<Design>"
$CFG     = [IO.Path]::GetFileNameWithoutExtension($PSCommandPath)
$RUNNAME = $CFG

# ---- 2. Paths ----
$FLAT     = (Split-Path -Leaf $PSScriptRoot) -eq "runs"
$TASK_DIR = if ($FLAT) { Split-Path -Parent $PSScriptRoot } else { Split-Path -Parent (Split-Path -Parent $PSScriptRoot) }
$TASK     = Split-Path -Leaf $TASK_DIR
$CFG_REL  = if ($FLAT) { "scripts/config/$CFG.do" } else { "runs/$RUNNAME/config.do" }
$OUTPUT_ROOT = if ($env:OUTPUT_ROOT) { $env:OUTPUT_ROOT } else { Split-Path -Parent $TASK_DIR }
$RESULTS  = if ($FLAT) { Join-Path $OUTPUT_ROOT "$TASK\results\$RUNNAME" } else { Join-Path $OUTPUT_ROOT "$TASK\runs\$RUNNAME\result" }
Write-Host "[$RUNNAME] task $TASK_DIR -> $RESULTS"

# ---- 3. Preconditions ----
$CFG_FILE = Join-Path $TASK_DIR $CFG_REL
if (-not (Test-Path $CFG_FILE)) { Write-Error "[$RUNNAME] Missing config: $CFG_FILE"; exit 1 }
$cfgText   = Get-Content $CFG_FILE -Raw
$caseName  = if ($cfgText -match 'global\s+case_asset_name\s+"([^"]+)"')    { $Matches[1] } else { $null }
$caseVer   = if ($cfgText -match 'global\s+case_asset_version\s+"([^"]+)"') { $Matches[1] } else { $null }
$caseSrc   = if ($cfgText -match 'global\s+case_source\s+"([^"]+)"')        { $Matches[1] } else { $COHORT }
$yearStart = if ($cfgText -match 'global\s+data_year_start\s+(\d+)')        { [int]$Matches[1] } else { 2015 }
$yearEnd   = if ($cfgText -match 'global\s+data_year_end\s+(\d+)')          { [int]$Matches[1] } else { 2020 }
if (-not $caseName -or -not $caseVer) {
    Write-Error "[$RUNNAME] Could not parse case_asset_name/version from config"
    exit 1
}
$WS_ROOT = $TASK_DIR
while ($WS_ROOT -and -not (Test-Path (Join-Path $WS_ROOT "pyproject.toml"))) { $WS_ROOT = Split-Path -Parent $WS_ROOT }
if (-not $WS_ROOT) { Write-Error "[$RUNNAME] repo root not found"; exit 1 }
$WS_ROOT = Join-Path $WS_ROOT "_WorkSpace"
$CASE_PATH = "$WS_ROOT\2-Case-Store\$caseName\$caseVer"
$required = @($CFG_FILE)
for ($y = $yearStart; $y -le $yearEnd; $y++) {
    $required += "$CASE_PATH\year-$y\CASES-BeneNpiObsdt-$caseSrc-$y.dta"
}
$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing) {
    Write-Error ("[$RUNNAME] Missing inputs:`n  - " + ($missing -join "`n  - "))
    exit 1
}

# ---- 4. Results + snapshot ----
New-Item -ItemType Directory -Force -Path "$RESULTS\log" | Out-Null
Copy-Item $CFG_FILE "$RESULTS\config_snapshot.do" -Force

# ---- 5. Run pipeline ----
& powershell -File "$TASK_DIR\scripts\run_data_steps.ps1" -cfg $CFG_REL -resultsDir $RESULTS -wsRoot $WS_ROOT
if ($LASTEXITCODE -ne 0) { throw "Data pipeline failed: $LASTEXITCODE" }

# ---- 6. Manifest ----
@{ runname=$RUNNAME; cohort=$COHORT; design=$DESIGN; config=$CFG_REL; finished=(Get-Date -Format o) } |
    ConvertTo-Json | Set-Content "$RESULTS\manifest.json"
Write-Host "[$RUNNAME] done. results: $RESULTS"
