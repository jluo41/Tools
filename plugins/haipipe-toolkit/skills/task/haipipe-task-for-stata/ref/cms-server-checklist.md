# CMS Secure Server -- Full Checklist

> One-stop reference for migrating Stata pipeline code to the CMS secure server. Organized as **three gates** -- each catches different failure modes.
> Source: `task/haipipe-task-for-stata/ref/stata-dialect.md` + field incidents.

---

## Three-Gate Model

```
  Gate 1: LOCAL SYNTH RUN         Gate 2: SERVER PRE-FLIGHT        Gate 3: FIRST REAL-DATA RUN
  (does the logic work?)          (will it parse on the server?)   (does real data behave?)
  ────────────────────            ─────────────────────────        ────────────────────────────
  Run on laptop, synth config     Machine checks before shipping   First run on CMS server

  Catches:                        Catches:                         Catches:
  - dispatcher wiring bugs        - encoding traps (em-dash)       - filter no-ops (synth=0)
  - wrong file paths              - PS7 syntax (&&, ??, pwsh)      - IV constant-zero crash
  - missing scripts/configs       - SSC dependency (distinct)      - sample size surprises
  - heavy/light mis-routing       - dead %TEMP% (preserve)         - merge mismatches on real IDs
  - config plumbing               - path portability (ws_root)     - PHI-specific edge cases
```

All three gates run **in order**. Gate 1 on the laptop with synth. Gate 2 on the laptop before shipping. Gate 3 on the server after the first real run.

---

# Gate 1: Local Synth Run

**Purpose:** validate pipeline LOGIC end-to-end before touching the server. Synth data is small and laptop-safe -- errors are cheap to catch here.

## 1.1 How to run

Each pipeline stage has a synth-compatible config. Run the same runner, different config:

```
  STAGE          COMMAND (from task folder)                          SYNTH CONFIG
  ─────          ───────────────────────                             ────────────
  A  cms         powershell run_cms_year.ps1 -cfg cms_synth -year 2015       cms_synth.do
  B  case        powershell run_case_year.ps1 -source synth -year 2015       _source_synth.do
  C  data        powershell run_data.ps1 -cfg <Cohort>_1stPair_synth         <Cohort>_1stPair_synth.do
  D  reg         powershell run_reg.ps1 -cfg <Cohort>_1stPair_synth          <Cohort>_1stPair_synth.do
```

The synth config sets `cms_source "synth"`, `cms_asset_name "cms_synth"`, `file_physician "PhyReview2021Synth"`. Same runner code, different globals.

## 1.2 Post-run checks

| ID | Check | Where to look | Pass |
|----|-------|---------------|------|
| L1 | Pipeline ran to completion | Console / Stata exit code | No `r(...)` errors; all phases finished |
| L2 | Heavy assets created | `_WorkSpace/{1-CMS,2-Case,...}-Store/` | Expected `.dta` files exist, non-zero size |
| L3 | Light outputs created | `results/<run>/` | `log/`, `summary.txt`, config snapshot present |
| L4 | No heavy in results/ | `results/<run>/` | Zero `.dta` files under `results/` |
| L5 | No light in _WorkSpace/ | `_WorkSpace/...-Store/` | No `.tex`/`.csv` tables leaked into store dirs |
| L6 | Logs clean | `results/<run>/log/*.txt` | No `r(...)` error codes; no "variable not found" |
| L7 | Describe/QC sane | `results/<run>/log/describe_*.txt` | Row counts > 0; key variables present; no all-missing |
| L8 | Config snapshot matches | `results/<run>/config_snapshot.do` | Globals match what you intended (source, paths, version) |
| L9 | Dispatcher routes correct | Stata log for each step | Each step logged; no "step not recognized" |
| L10 | Output paths land in _WorkSpace | Check actual file locations | All `.dta` under `_WorkSpace/`, not under task folder |

### Quick post-run verify (PowerShell, from task folder)

```powershell
# Check heavy assets exist
Get-ChildItem "$ws\_WorkSpace\1-CMS-Store\cms_synth" -Recurse -Include *.dta |
    Select-Object FullName, @{N='MB';E={[math]::Round($_.Length/1MB,1)}}

# Check no .dta leaked into results/
Get-ChildItem "results" -Recurse -Include *.dta

# Scan logs for Stata errors
Select-String -Path "results\*\log\*.txt" -Pattern 'r\(\d+\)' -Recurse
```

## 1.3 Known synth limitations (what Gate 1 CANNOT catch)

```
  LIMITATION             WHY                                    GATE 3 CATCHES IT
  ────────────           ───                                    ─────────────────
  Filter no-ops          Synth cancer coded 0/1 not ICD ==3     G3.1: drops > 0
                         Synth MDDO/review filters drop 0       G3.1
                         Synth physician merge: matched = all   G3.4: unmatched > 0
  Tiny sample            Synth n ~ 151, few opioid events       G3.2: n >> 151
  IV infeasible          0 high-MME -> constant DV -> r(459)    G3.3: DV has variance
  Merge mismatches       Synth IDs always match                 G3.4: real unmatched
  Coefficient signs      Too few obs for meaningful estimates    G3.8: direction check
```

These ONLY surface at Gate 3. Gate 1 passing does NOT mean the pipeline is correct -- it means the plumbing works.

---

# Gate 2: Server Pre-flight

**Purpose:** verify that code will PARSE and RUN on the locked-down CMS server environment. All checks run locally before shipping.

## 2.0 Server Environment (what you are dealing with)

```
  OS             Windows Server (same PS edition as Win 11)
  Shell          Windows PowerShell 5.1 ONLY -- pwsh absent, installs blocked
  Stata          Clean install + rangejoin (manually installed); no other SSC add-ons
  Network        NONE -- no internet, no winget, no pip, no ssc install
  Temp           %TEMP% is DEAD (unwritable across drives)
  PHI            cms_full + G:\CMS\DATA live here, never leave
  Access         Isolated -- no shared drive/sync with laptop; hand-copy only
  Python         Available but $env:PYTHONUTF8 not set by default
```

## 2.1 Encoding & Shell (will .ps1 parse on PS 5.1?)

| ID | Check | Symptom if violated | Fix |
|----|-------|---------------------|-----|
| B1 | No PS7-only syntax: `&&` `\|\|` ternary `?:` null-coalescing `??` | `ParserError`, `Unexpected token` | Rewrite: `A; if ($?) { B }` for `&&`; `if/else` for ternary |
| B2 | No `pwsh` calls anywhere | `CommandNotFoundException` | Use `& powershell -File <path>` or `& $script` (same session) |
| B3 | `.ps1`/`.do` files are ASCII-only | Em-dash `--` (0xE2 0x80 0x94) mis-decodes on 5.1 as smart-quote; truncates string -> `Unexpected token` | Keep ASCII. If non-ASCII unavoidable, save **UTF-8 WITH BOM** |
| B4 | `$env:PYTHONUTF8="1"` set before Python steps | Python `read_text()`/`print()` crash on UTF-8 files (Windows cp1252 default) | Set in orchestrator `.ps1` before `Start-Process python` |
| B5 | No `winget`, `pip install`, `npm`, etc. | Command not found / network timeout | Pre-install nothing; all deps must be already on the server |

### Machine check (run locally before shipping)

```powershell
# Scan for non-ASCII bytes in .ps1/.do files
Get-ChildItem -Recurse -Include *.ps1,*.do | ForEach-Object {
    $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
    $bad = $bytes | Where-Object { $_ -gt 127 }
    if ($bad) { Write-Host "NON-ASCII: $($_.FullName) ($($bad.Count) bytes)" }
}

# Grep for PS7-only syntax + pwsh
Select-String -Path *.ps1 -Pattern '\?\?|\?\.|&&|\|\||pwsh' -Recurse

# PS 5.1 parse check (catches syntax errors without running)
Get-ChildItem -Recurse -Include *.ps1 | ForEach-Object {
    $tokens = $null; $errors = $null
    [System.Management.Automation.PSParser]::Tokenize(
        (Get-Content $_.FullName -Raw), [ref]$errors) | Out-Null
    if ($errors) { Write-Host "PARSE FAIL: $($_.FullName)"; $errors }
}
```

## 2.2 Stata Runtime (will .do run on clean Stata?)

| ID | Check | Symptom if violated | Fix |
|----|-------|---------------------|-----|
| C1 | No SSC commands EXCEPT `rangejoin` (installed on server). Block: `distinct`, `ftools`, `gtools`, etc. | `command ... is unrecognized r(199)` | Use built-ins: `egen tag()` + `count` for distinct; `summarize`/`tabulate` for stats. `rangejoin` is the one allowed SSC package. |
| C2 | No `ssc install` anywhere | Network timeout then `r(631)` or `r(199)` | Remove the line; use only built-in Stata commands |
| C3 | Never launch `.do` via editor "Do" button | Stages to `%TEMP%\pNNNN.do` -> fails `command E is unrecognized r(199)` | Launch ONLY via `.ps1`: `Start-Process $stata "/e do <dispatcher>.do ..."` |
| C4 | Avoid `preserve`/`restore` (writes to %TEMP%) | File-write error or silent corruption | Set `$env:STATATMP` to writable in-repo dir in orchestrator, OR rewrite without preserve |
| C5 | Avoid `tempfile` (also writes to %TEMP%) | Same as C4 | Stage intermediates with explicit `save "${temp_dir}/..."` + `use` |
| C6 | `capture`-guard optional variables | `variable ... not found r(111)` when a condition/feature var is absent | Wrap in `capture confirm variable <var>` or `capture noisily` |

### Machine check

```powershell
# Grep .do files for SSC commands
Select-String -Path *.do -Pattern '\bdistinct\b|\bssc\b|\bftools\b|\bgtools\b' -Recurse

# Find preserve/tempfile usage (needs STATATMP redirect)
Select-String -Path *.do -Pattern '\bpreserve\b|\btempfile\b' -Recurse
```

### STATATMP redirect pattern

```powershell
# In orchestrator .ps1, BEFORE launching Stata:
$env:STATATMP = "$dir\results\run_cms_$year\_tmp"
New-Item -ItemType Directory -Force -Path $env:STATATMP | Out-Null
```

Stata resolves temp: `STATATMP` -> `TMP` -> `TMPDIR` -> `TEMP`. Setting `STATATMP` overrides the dead `%TEMP%` for `preserve`/`tempfile`/`postfile`.

## 2.3 Path Portability (will it find its files on any machine?)

Three rules -- a task must run identically on laptop and server, launched from anywhere, regardless of the folder's own name.

| ID | Check | Symptom if violated | Fix |
|----|-------|---------------------|-----|
| D1 | `$stata` = ONE editable line at top of orchestrator | Stata not found on different machine | `$stata = "C:\Program Files\Stata18\StataMP-64.exe"` at line ~5; one machine edits one line |
| D2 | Run from `$PSScriptRoot`; `configs/` + `scripts/` relative | File not found when launched from different CWD | Orchestrator: `$dir = $PSScriptRoot`; Stata working dir = `$dir`; all code paths relative to `$dir` |
| D3 | Output paths from ABSOLUTE `_WorkSpace` via `pyproject.toml` walk-up | Heavy assets land in wrong place (classic: 50+ GB under task folder) | Walk up: `$ws = $dir; while ($ws -and -not (Test-Path "$ws\pyproject.toml")) { $ws = Split-Path $ws }`; pass `"$ws\_WorkSpace"` as arg |
| D4 | Never write relative `"_WorkSpace"` in config | Outputs land wherever CWD is (not the repo) | Config: `global out_root "${ws_root}/1-CMS-Store/..."` (ws_root from dispatcher arg) |
| D5 | No hardcoded folder name -- task folder renameable with `mv` | Script breaks if folder renamed | Use `$PSScriptRoot` not literal path segments; dispatcher `do "scripts/..."` not `do "A01_cms_pipeline/scripts/..."` |
| D6 | Fixed external inputs (e.g. `G:\CMS\DATA`) stay absolute in config | Works on server, fails on laptop (expected -- synth has different path) | Keep in config `.do` as `global cms_data_root "G:\CMS\DATA"`; laptop config uses synth path |

### Good pattern (from A01_cms_pipeline)

```powershell
# run_cms_year.ps1 -- top of file
param([string]$cfg = "cms_production", [string]$year = "2015")

$stata = "C:\Program Files\Stata18\StataMP-64.exe"       # D1: one line
$dir   = $PSScriptRoot                                     # D2: task root
$ws    = $dir                                              # D3: walk-up
while ($ws -and -not (Test-Path "$ws\pyproject.toml")) { $ws = Split-Path $ws }
$base  = "do 01_cms_pipeline.do $cfg"
$tail  = "`"$dir\results\run_cms_$year`" `"$ws\_WorkSpace`""

Start-Process $stata "/e $base pde $year $tail" -WorkingDirectory $dir -PassThru
```

## 2.4 PHI & Data Safety (what goes where?)

| ID | Check | Symptom if violated | Fix |
|----|-------|---------------------|-----|
| E1 | HEAVY `.dta` assets -> `_WorkSpace/{1-CMS,2-Case,...}-Store/` | PHI leaks into repo; bloats git | Never place `.dta` under `results/` or in-repo paths |
| E2 | LIGHT outputs (logs, `.tex`, `.csv` tables, `summary.txt`) -> `results/<run>/` | Results not tracked in git | Reg tables and logs go to `results/`; only data assets go to `_WorkSpace/` |
| E3 | synth vs full tagging -- outputs never collide | Synth results overwrite real or vice versa | Tag by `${cms_source}`: `case_lbp_synth` vs `case_lbp_full`; separate configs per source |
| E4 | Only CODE ships to server (`.do`, `.ps1`, `.yaml`, `.md`) | PHI leaves server; data leaves laptop | Use `ship-to-cms-server.ps1`: excludes `.dta`, `.csv`, `.log`, `results/`, `_WorkSpace/` |
| E5 | Verify which build produced current data | Reg runs on synth n=151, crashes IV `r(459)` | Check `config_snapshot.do` -> `case_asset_name` = `case_lbp` (real) vs `case_lbp_synth` |

## 2.5 Code Style (will the reviewer pass it?)

| ID | Check | Rule | Detail |
|----|-------|------|--------|
| F1 | Header | 1-2 comment lines: what + args/usage | No banners, no `===`/`---` walls, no ASCII-art, no box-drawing chars |
| F2 | Size | orchestrator `.ps1` <= ~30 lines; `runs/` entry as small as possible (ideal: 2-3 lines -- comment + call orchestrator); `sbatch/` batcher <= ~10 lines | worker `.do` = one focused step. `runs/` entries should be thin dispatch-only: set the year, call the orchestrator. All logic (path resolution, dir creation, validation) lives in the orchestrator. |
| F3 | No ceremony | No `runtime.yaml`/`manifest.json`/config snapshots in runners | Stata logs + `summary.txt` are the record |
| F4 | Dispatcher braces | Multi-line braces only | `else if "step" == "x" {` then body indented, then `}` on own line. No one-liners |
| F5 | No patch markers | No `// CHANGE (n)` in committed code | Give patch instructions in chat, not as in-file markers |
| F6 | Orchestrator reads as | Variable block, then action lines | No interleaved logic/declarations |

---

# Gate 3: First Real-Data Run

**Purpose:** validate that the pipeline behaves correctly with real CMS PHI data. These items CANNOT be validated on synth -- they only surface on the server.
Check after the first successful run with `cms_production` / `cms_full` config.

## 3.1 Post-run checks

| ID | Check | Where to look | Pass |
|----|-------|---------------|------|
| R1 | Filters actually drop rows | `log/filter_case.txt`, `filter_external.txt` | Cancer exclusion, MDDO, review-range all drop > 0 |
| R2 | Sample size reasonable | `log/describe_*.txt` or reg output | n >> 151; expect thousands per cohort-year |
| R3 | IV has variation in DV | Reg output / log | No `r(459)` "variable is constant"; DV has non-zero variance |
| R4 | Physician merge has matches | `log/filter_external.txt` | "Not matched" < total; matched > 0; match rate plausible |
| R5 | Outcome variables non-zero | Describe output | Opioid/MME DVs have non-zero obs in both 0 and 1 groups |
| R6 | Config snapshot says "full" | `config_snapshot.do` | `case_asset_name` = `case_lbp` (not `_synth`); `file_physician` = `PhyReview2021` (not `Synth`) |
| R7 | Year-specific counts plausible | Cross-year comparison | No year with 0 obs; no wild n jumps between adjacent years |
| R8 | Coefficient signs correct | Reg `.tex` tables | Key regressors non-zero; direction matches theory |
| R9 | All estimators ran | Check OLS + IV + DID output | Each estimator folder has output; IV didn't crash on a constant |
| R10 | All cohorts ran | Check across cohort folders | Each cohort has results; no cohort silently skipped |

## 3.2 Diagnostic commands (run in Stata on the server)

```stata
// Quick sanity on the analysis file
use "${ws_root}/3-Data-Store/<Cohort>_1stPair/v001_base/ANALYSIS-CMS-Filter.dta", clear
describe, short
summarize is_opioid_rx is_high_mme_daily, detail
tab is_opioid_rx, missing

// Check filter log tells
// In results/<run>/log/filter_case.txt, look for:
//   "Exclude cancer (dropped N)"    -- N > 0 on real data
//   "is_mddo==1 (dropped N)"        -- N > 0 on real data
//   "Reviews 5-100 (dropped N)"     -- N > 0 on real data
//
// In results/<run>/log/filter_external.txt:
//   "Not matched N"                 -- N > 0 but < total
```

## 3.3 synth vs full diagnostic tells

How to confirm a build used real data (not synth):

```
  CHECK 1: config_snapshot.do
           case_asset_name = "case_lbp"        (real)  vs "case_lbp_synth"
           file_physician  = "PhyReview2021"    (real)  vs "PhyReview2021Synth"

  CHECK 2: filter logs
           SYNTH tells:  "Exclude cancer (dropped 0)"
                         "Not matched 0"
                         "is_mddo==1 (dropped 0)"
                         "Reviews 5-100 (dropped 0)"
           REAL data:    all these should drop rows > 0

  CHECK 3: sample size
           Synth:  n ~ 151, few opioid events, 0 high-MME
           Real:   n in thousands per cohort-year
```

---

# Migration Workflow

The full three-gate flow:

```
  LAPTOP (Claude + user)                        CMS SERVER (user only)
  ========================                      =======================

  1. Edit code locally
         |
  2. Gate 1: run with synth config     <-----  same runner, synth config
     Check: L1-L10 (logic, paths,              no server needed
     wiring, heavy/light split)
         |
  3. Gate 2: server pre-flight         <-----  machine checks only
     Check: B1-B5, C1-C6, D1-D6,              no server needed
     E1-E5, F1-F6
         |
  4. Package: ship-to-cms-server.ps1
     (code only, no data)
         |
  5. --------[ hand-copy zip ]--------------->  6. Unzip into tasks/
                                                7. Edit $stata path (D1)
                                                8. Run: powershell run_*.ps1
                                                      -cfg cms_production
                                                9. Gate 3: check R1-R10
                                                   (filters, n, IV, signs)
         |                                             |
  11. Fix code <---[ paste errors/output ]---- 10. Paste back to Claude
         |
  (repeat from step 1)
```

### Key workflow rules

- **Claude never runs the real pipeline** -- only edits + parse-checks locally
- **User's server output = sole ground truth** -- never claim "it works"
- **End every reply with change-list** -- exact files + line edits to hand-port
  (section heading: `## Change on the CMS server`)
- **Watch scope** -- a fix usually hits ALL estimator folders (OLS/IV/DID) x ALL cohorts

### Ship script

```powershell
# From repo root:
powershell -File examples\ProjB-PhyTrait-OpioidRx\ship-to-cms-server.ps1

# Ships: *.do *.ps1 *.sh *.yaml *.yml *.md *.txt *.py *.bib *.tex
# Drops: results/ tmp/ logs/ .git/ __pycache__/ *.dta *.csv *.log
# Output: ProjB-cms-server-code-YYYYMMDD.zip
```

---

# Quick Reference Card

```
  GATE 1 -- LOCAL SYNTH RUN (does the logic work?)
  ─────────────────────────
  Run with synth config on laptop.
  Check: pipeline completes [L1], heavy in _WorkSpace [L2 L4],
         light in results/ [L3 L5], logs clean [L6], describe sane [L7].

  GATE 2 -- SERVER PRE-FLIGHT (will it parse on the server?)
  ────────────────────────────
  ENCODING    ASCII-only .ps1/.do (or UTF-8+BOM)         [B3]
  SHELL       powershell not pwsh; no && || ?: ??         [B1 B2]
  STATA       no SSC except rangejoin (installed); no ssc install [C1 C2]
  LAUNCH      .ps1 only, never editor Do button           [C3]
  TEMP        set $env:STATATMP if preserve/tempfile used [C4 C5]
  PATHS       $stata line + $PSScriptRoot + ws_root       [D1 D2 D3]
  WORKSPACE   heavy .dta -> _WorkSpace/; light -> results/[E1 E2]
  PHI         synth/full tagged; code-only ships          [E3 E4]
  STYLE       1-2 line header; orch<=30; runs/ as small as possible [F1 F2]
  PYTHONUTF8  $env:PYTHONUTF8="1" before Python steps    [B4]

  GATE 3 -- FIRST REAL-DATA RUN (does real data behave?)
  ──────────────────────────────
  Run with cms_production on server.
  Check: filters drop > 0 [R1], n >> 151 [R2], IV runs [R3],
         merge matches [R4], config says "full" [R6],
         all estimators x cohorts ran [R9 R10].
```
