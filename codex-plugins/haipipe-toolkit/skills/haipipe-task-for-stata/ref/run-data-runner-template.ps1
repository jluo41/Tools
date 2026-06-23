# runs/run_data_<Spec>.ps1 -- self-orchestrating data-stage runner
# Data-stage: no year axis; runner IS the orchestrator. See topology: SELF-ORCHESTRATING.
# EDIT: $COHORT, $DESIGN, conditional input paths.
$ErrorActionPreference = "Stop"

# ---- 1. Identity ----
$COHORT  = "<Cohort>"
$DESIGN  = "<Design>"
$CFG     = "run_data_${COHORT}_${DESIGN}"
$RUNNAME = "run_data_${COHORT}_${DESIGN}"

# ---- 2. Paths ----
$TASK_DIR = Split-Path -Parent $PSScriptRoot
$RESULTS  = "$TASK_DIR\results\$RUNNAME"

# ---- 3. Preconditions ----
$CFG_FILE = "$TASK_DIR\configs\$CFG.do"
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
& powershell -File "$TASK_DIR\run_data_steps.ps1" -cfg $CFG -resultsDir $RESULTS -wsRoot $WS_ROOT

# ---- 6. Manifest ----
@{ runname=$RUNNAME; cohort=$COHORT; design=$DESIGN; config=$CFG; finished=(Get-Date -Format o) } |
    ConvertTo-Json | Set-Content "$RESULTS\manifest.json"
Write-Host "[$RUNNAME] done. results: $RESULTS"
