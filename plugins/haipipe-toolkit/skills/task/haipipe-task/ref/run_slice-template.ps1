# === Run any slice of THIS JOB ==============================================
# The job's runs form a grid. This is the ONE place the grid is understood; the
# named entry points beside this file are thin calls into it.
#
#   .\run_slice.ps1                       everything
#   .\run_slice.ps1 -Task t01_...         one task
#   .\run_slice.ps1 -Family 3_did         one code path, every task
#   .\run_slice.ps1 -Year 2015 -WhatIf    list, run nothing
#
# Coordinates come from the ticket NAME, which carries them by construction:
#   rNN_D_reg_<asset>_<trait>_<window>_<family>   trait grid   (pain, diabetes)
#   rNN_D_reg_<asset>_<analysis>                  analysis     (cardiac)
#   rNN_C_data_<asset>_<y0>_<y1>                  window       (C stage)
#   rNN_B_case_<asset>_<year>_<source>            year/source  (B stage)
#
# ONE BY ONE OR ALL AT ONCE is a property of the JOB, not of whoever types the
# command, so it is declared in batch.psd1 beside this file and enforced here.
# Every run of this script prints which one it is doing before it starts.
#   -Sequential      force one at a time
#   -Parallel <N>    force N at a time (never past the job's Ceiling)
# ============================================================================
param(
    [string[]]$Task, [string[]]$Family, [string[]]$Window, [string[]]$Trait,
    [string[]]$Analysis, [string[]]$Year, [string[]]$Source,
    [switch]$Sequential, [int]$Parallel = 0,
    [switch]$ContinueOnError, [switch]$WhatIf
)
$ErrorActionPreference = "Stop"
$JOB_DIR = Split-Path -Parent $PSScriptRoot
$JOB     = Split-Path -Leaf $JOB_DIR
# A run is launched by the SAME PowerShell that is reading this file, found rather
# than spelled. Hard-coding "powershell" makes a 5.1 host launch children that are
# whatever is first on PATH, and makes this file Windows-only for no reason.
$PSEXE = (Get-Process -Id $PID).Path
if (-not $PSEXE) { $PSEXE = "powershell" }

# === 1. What this job declares about running its runs together ==============
$DECL_FILE = Join-Path $PSScriptRoot "batch.psd1"
if (-not (Test-Path $DECL_FILE)) {
    Write-Error "no batch.psd1 beside run_slice.ps1: this job has not said whether its runs may go at the same time. Sequential is not a safe guess, so nothing is run."
    exit 1
}
$decl = Import-PowerShellDataFile $DECL_FILE
foreach ($k in @('Mode','Ceiling','CollisionKey','Why')) {
    if (-not $decl.ContainsKey($k)) { Write-Error "batch.psd1 has no '$k'"; exit 1 }
}
if ($decl.Mode -notin @('sequential','parallel')) { Write-Error "batch.psd1 Mode must be 'sequential' or 'parallel', not '$($decl.Mode)'"; exit 1 }

$ceiling = [int]$decl.Ceiling
if ($decl.Mode -eq 'sequential' -and $ceiling -ne 1) { Write-Error "batch.psd1 says Mode='sequential' but Ceiling=$ceiling"; exit 1 }
$width = if ($Sequential) { 1 } elseif ($Parallel -gt 0) { $Parallel } else { $ceiling }
if ($width -gt $ceiling) {
    Write-Error "-Parallel $width is above this job's Ceiling of $ceiling. Raise Ceiling in batch.psd1, with the reason, or run at $ceiling."
    exit 1
}
$keyProps = @($decl.CollisionKey -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })

# === 2. Every ticket, with its coordinates read off its own name ============
$runs = foreach ($t in Get-ChildItem "$JOB_DIR\t*\runs" -Recurse -Filter *.ps1 | Sort-Object FullName) {
    $p = $t.Directory
    while ($p -and $p.Name -ne "runs") { $p = $p.Parent }
    $o = [pscustomobject]@{ Ticket=$t; Name=$t.BaseName; Task=$p.Parent.Name
                            Trait=$null; Window=$null; Family=$null; Analysis=$null
                            Year=$null; Source=$null }
    if     ($t.BaseName -match '^r\d\d_D_reg_.+?_(?<tr>[a-z]+)_(?<w>af\d+d|allw)_(?<f>.+)$') {
        $o.Trait=$Matches.tr; $o.Window=$Matches.w; $o.Family=$Matches.f }
    elseif ($t.BaseName -match '^r\d\d_C_data_.+?_(?<y0>\d{4})_(?<y1>\d{4})$') {
        $o.Window="$($Matches.y0)_$($Matches.y1)" }
    elseif ($t.BaseName -match '^r\d\d_.*?(?<y>\d{4})_(?<s>full|synth)$') {
        $o.Year=$Matches.y; $o.Source=$Matches.s }
    elseif ($t.BaseName -match '^r\d\d_D_reg_.+?_(?<a>[a-z]+)$') { $o.Analysis=$Matches.a }
    else { Write-Warning "cannot read coordinates from $($t.BaseName); skipped"; continue }
    $o
}
if (-not $runs) { Write-Error "no tickets under $JOB_DIR"; exit 1 }
foreach ($k in $keyProps) {
    if ($k -notin @('Name','Task','Trait','Window','Family','Analysis','Year','Source')) {
        Write-Error "batch.psd1 CollisionKey names '$k', which is not a coordinate of a ticket here"; exit 1
    }
}

function Keep($rows, $filter, $prop) {
    if (-not $filter) { return $rows }
    $known = @($rows.$prop | Where-Object { $_ } | Sort-Object -Unique)
    $bad = $filter | Where-Object { $_ -notin $known }
    if ($bad) { Write-Error "unknown $prop`: $($bad -join ', '). Known: $($known -join ', ')"; exit 1 }
    return $rows | Where-Object { $_.$prop -in $filter }
}
$sel = $runs
foreach ($p in @(@{f=$Task;n='Task'}, @{f=$Family;n='Family'}, @{f=$Window;n='Window'},
                 @{f=$Trait;n='Trait'}, @{f=$Analysis;n='Analysis'},
                 @{f=$Year;n='Year'}, @{f=$Source;n='Source'})) { $sel = Keep $sel $p.f $p.n }
if (-not $sel) { Write-Error "no run matches that combination"; exit 1 }
$sel = @($sel | Sort-Object Task, Name)

# === 3. Waves: what may go at the same time =================================
# Two runs that agree on every CollisionKey field write the same files, so they
# are put in DIFFERENT waves however wide the job runs. This is why -Parallel is
# not just a loop with more workers.
function Get-Key($r) { ($keyProps | ForEach-Object { "$($r.$_)" }) -join '|' }
$waves = @()
$pending = [System.Collections.ArrayList]@($sel)
while ($pending.Count) {
    $wave = @(); $used = @{}
    foreach ($r in @($pending)) {
        if ($wave.Count -ge $width) { break }
        $k = Get-Key $r
        if ($used.ContainsKey($k)) { continue }
        $used[$k] = $true; $wave += $r; $pending.Remove($r) | Out-Null
    }
    $waves += ,$wave
}
$serialized = ($waves | Where-Object { $_.Count -lt $width -and $_ -ne $waves[-1] }).Count

# === 4. Say what is about to happen, before doing any of it =================
Write-Host ("==== {0}: {1} of {2} runs ====" -f $JOB, @($sel).Count, @($runs).Count)
if ($width -le 1) {
    Write-Host "     ONE AT A TIME (sequential), $(@($sel).Count) run(s) end to end"
} else {
    Write-Host ("     {0} AT A TIME (parallel), {1} wave(s)" -f $width, $waves.Count)
    Write-Host ("     never together: two runs equal on {0}" -f ($keyProps -join ' + '))
}
$src = if ($Sequential) { "-Sequential on the command line" }
       elseif ($Parallel -gt 0) { "-Parallel $Parallel on the command line (job ceiling $ceiling)" }
       else { "batch.psd1: Mode=$($decl.Mode), Ceiling=$ceiling" }
Write-Host "     from $src"
Write-Host "     why: $($decl.Why)"

if ($WhatIf) {
    Write-Host ""
    foreach ($i in 0..($waves.Count-1)) {
        $h = if ($width -le 1) { "---- run {0} of {1} ----" -f ($i+1), $waves.Count }
              else { "---- wave {0} of {1} ({2} run(s)) ----" -f ($i+1), $waves.Count, $waves[$i].Count }
        Write-Host $h
        foreach ($r in $waves[$i]) { Write-Host "     would run  $($r.Name)   [$($r.Task)]" }
    }
    Write-Host ""
    Write-Host "==== -WhatIf: nothing was run ===="
    exit 0
}

# === 5. Run them ============================================================
$BATCH = Join-Path $JOB_DIR ("results\_batch\" + (Get-Date -Format "yyyyMMdd-HHmmss"))
if ($width -gt 1) { New-Item -ItemType Directory -Force -Path $BATCH | Out-Null }
$ok=@(); $failed=@(); $t0=Get-Date
foreach ($i in 0..($waves.Count-1)) {
    $wave = $waves[$i]
    Write-Host ""
    if ($width -le 1) { Write-Host ("---- run {0} of {1} ----" -f ($i+1), $waves.Count) }
    else { Write-Host ("---- wave {0} of {1} ({2} run(s)) ----" -f ($i+1), $waves.Count, $wave.Count) }

    if ($width -le 1) {
        # One at a time: the run's own output goes straight to this console, live.
        foreach ($r in $wave) {
            Write-Host "     $($r.Name)"
            & $PSEXE -NoProfile -File $r.Ticket.FullName
            if ($LASTEXITCODE -ne 0) {
                $failed += $r.Name
                if (-not $ContinueOnError) { Write-Error "$($r.Name) failed (exit $LASTEXITCODE). -ContinueOnError runs the rest."; exit 1 }
                Write-Host "       FAILED (exit $LASTEXITCODE)"
            } else { $ok += $r.Name }
        }
        continue
    }

    # Several at a time: interleaved consoles are unreadable, so each run's output
    # goes to its own file and is printed when the wave closes.
    $procs = foreach ($r in $wave) {
        Write-Host "     start  $($r.Name)"
        $log = Join-Path $BATCH "$($r.Name).log"
        $p = Start-Process $PSEXE -ArgumentList "-NoProfile","-File",$r.Ticket.FullName `
                -RedirectStandardOutput $log -RedirectStandardError "$log.err" `
                -NoNewWindow -PassThru
        [pscustomobject]@{ Run=$r; Proc=$p; Log=$log }
    }
    $procs.Proc | Wait-Process
    foreach ($x in $procs) {
        $code = $x.Proc.ExitCode
        if ($code -ne 0) { $failed += $x.Run.Name; Write-Host "     FAILED (exit $code)  $($x.Run.Name)  -> $($x.Log)" }
        else { $ok += $x.Run.Name; Write-Host "     ok            $($x.Run.Name)  -> $($x.Log)" }
    }
    if ($failed -and -not $ContinueOnError) {
        Write-Error "wave $($i+1) had $($failed.Count) failure(s); logs under $BATCH. -ContinueOnError runs the rest."
        exit 1
    }
}
Write-Host ""
Write-Host ("==== {0} done in {1} min · OK {2} · FAILED {3} ====" -f $JOB, [int]((Get-Date)-$t0).TotalMinutes, $ok.Count, $failed.Count)
if ($width -gt 1) { Write-Host "     logs: $BATCH" }
foreach ($x in $failed) { Write-Host "    $x" }
if ($failed) { exit 1 }
exit 0
