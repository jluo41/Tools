# Profile: cms-stata

The CMS secure server. Stata batch mode plus Windows PowerShell 5.1, driving CMS
Medicare claims that never leave that machine.

Load this profile only when the user or verified project configuration names
the CMS secure-server environment. Stata `r(nnn)`, `.do`, `.ps1`, or log-path
shapes alone do not establish CMS. Home repo: `Physician-SPACE`, project
`examples-2-cms/Project-Personality-OpioidRx`; unrelated projects use their own
profile or the generic method.

Two skills own the other half of this environment and should be read alongside:
`haipipe-task-for-stata` (scaffold a task folder, run the pre-flight gate, write
`SERVER_CHECK.md`), and its `ref/cms-server-checklist.md` (the three-gate model
and the full register naming rules).

---

## Defaults

```
register default   _WorkSpace/0-CMS-Store/Issue-From-CMS-Server/
register index     SERVER-READY-CHECK.md
issue file         ${REGISTER}/<YYMMDD>/issue-00N-<slug>.md
daily findings     ${REGISTER}/<YYMMDD>/FINDINGS.md
issue template     issue-file-template.md
status file        <task-folder>/ISSUES.md
static gate        python work/_tools/check_server_ready.py <UNIT>     19 rules
shared copies      python work/_tools/check_preupload.py <work dir>    M10: every SHARED COPY byte-identical
tree check         python work/_tools/check_task_tree.py <Block dir>
dry run            python work/_tools/dryrun/dryrun.py                every ticket, stand-in Stata, server layout
upload package     python work/_tools/pack_upload.py <tag> --per-block  one short-named zip per Block, <tag>-PerBlock/,
                   for every server Block of both Projects (it ignores --project); the default for an upload
                   (or --project CmsPipeline|OpioidRx, then --check: 0 differences from the repo)
results back       work/_tools/collect_results.ps1 (server), file_server_return.py (laptop)
server home        F:\Physician-SPACE\work\<Block>\...                never the repo's own depth
```

`<UNIT>` is any part of a Job's folder name, not a path: `j21_C1D_reg_VisitLBP` picks one Job (plain `j21` matches
every visit Block's j21; the old units `R01`, `C01`, `A11` name the pre-261019 folders). No unit checks every Job.
Every `work/_tools/` path is inside `examples-2-cms/Project-Personality-OpioidRx/`; `python` here is always the
SPACE's `.venv/bin/python` (the Mac's system `python3` is 3.9).
Since 261019 a file shared by many Jobs carries a `SHARED COPY` banner instead of `GENERATED FILE`: there is
no generator to rerun, so edit every copy the same way and `check_preupload.py` must report 0 (M10).

---

## Step 1: where the error actually is

Three artifacts, and most people open only the first:

```
results/<run>/log/data-pipeline.txt   the run log
results/<run>/log/batch-<step>.txt    Stata's OWN /e log. The ONLY place an
                                      error raised BEFORE `log using` opens
                                      appears. Added 260829.
results/<run>/data-state.tsv          row + column delta per step, one screen.
                                      A step whose row delta goes to zero is a
                                      [LIES], not a [CRASH].
```

Success is the `.done-*` marker file, never the exit code.

A regression Run in a Run folder (since 261020) splits these: `runs\<run>\result\` keeps only what a reader
reviews (`RUN-REPORT.md`, `tables\`, `describe\`), and each execution's `log\`, `steps\`, `.done`,
`runtime.yaml` and `config_snapshot.do` go to `runs\<run>\passes\pNN-<MMDD>\`, which stays on the server.
A Run that failed prints `STOPPED: <entry> ended with r(<rc>)` in that pass's log (`stata-guard.do`).

---

## Step 2: the code table

```
r(198)  invalid syntax     often a PARSER rule, not a bad value.
                           `forvalues yr = ${a}/${b} {` closes the loop on the
                           macro's own brace. Use `$a/$b` inside a forvalues
                           RANGE; `${name}` is right everywhere else.
                           Story: 260828/issue-001-forvalues-brace-r198.md
r(111)  variable not found a merge or egen naming a column the build never wrote
r(601)  file not found     a path built from a global that nothing set yet
r(459)  guard exit         this repo's chronic-condition guard uses it on purpose
r(603)  cannot open        %TEMP% is unwritable on this server. $env:STATATMP
                           must be redirected before Stata launches.
r(681)  preserve failed    same cause as r(603)
zip     "The Compressed (zipped) Folder ... is invalid" in Explorer, while unzip -t on the laptop is clean:
invalid one entry name inside passes 260 characters (v1022 to v1023b held one of 264). First compare the
        server file's size with the build: a copy from an earlier build is the cheaper cause. Rebuild with
        pack_upload.py --per-block (entries start at work\, none past 240) and extract with Expand-Archive
        into F:\u. 7-Zip opens such a zip (it has no 260 limit), which confirms the cause. Register
        261023/issue-002.
exit 0  after an error     Stata does this. ENV-02. The marker is the only gate.
modal   any error at all   /e mode pops a dialog and the run waits all night for
dialog                     a click. ENV-01. `set batch` does not exist here.
"has    a Break, not an    "<entry> has been interrupted. Would you like the batch job to continue?" in the
been    error              middle of a long step. A Break (the Break key, a click on a busy Stata window) passes
inter-                     `capture`, so stata-guard.do cannot catch it. Yes resumes the step and it finishes;
rupted"                    No ends Stata, and the step is rebuilt next time. Fix since 261025: stata-guard.do runs
                           `nobreak cap noi do`. Register 261024/issue-004.
FAIL:   enabled feature    check-07 of a C table: one year lacks a file its newer steps make (BFAF-NpiObsdt-PDE-
missing a year built       OpioidRx-2019 when 2020 was built later). Rerun that year's Task (B extends in place;
        before the step    built steps skip), then the C table. Ask for the year folder's listing, not the log.
not     an uploaded .ps1   "<ticket>.ps1 cannot be loaded. The file ... is not digitally signed", at run_long.ps1's
digit-  with the internet  `& ".\$x"`: the policy (RemoteSigned) refuses a script unpacked from a downloaded zip
ally    mark               (Mark of the Web); run_long.ps1, typed on the server, runs. Fix, from F:\Physician-SPACE,
signed                     after every upload: `gci examples-2-cms -r | unblock-file`, then `gci w -r | unblock-file`
                           (the first gives FileNotFound on OpioidRx paths past 260; w reaches them). A Group Policy
                           pins RemoteSigned: `set-executionpolicy bypass -scope process` and -ExecutionPolicy
                           Bypass are both overridden ("ExecutionPolicyOverride"). Check one file: `gi <file>
                           -stream *` lists Zone.Identifier while it is marked. 261025 r27 (b21 j31): only :$DATA,
                           no mark, still refused; its real path is 284 characters (via w 238), and every ticket
                           that ran is 256 or less, so a real path past 259 likely reads as not local (inferred;
                           286 of 738 OpioidRx tickets pass 259). Fix in run_long.ps1: on PSSecurityException it
                           runs the ticket's lines as a script block (the policy checks files, not commands),
                           $PSScriptRoot replaced by the ticket's w folder; the launcher, a short-path file, runs.
                           Such a Run's runtime.yaml names run_long.ps1 as its ticket.
not     a ticket path      `.\x.ps1 : The term ... is not recognized`: a list with a path cut short (no .ps1 file
recog-  that is a folder   name). Before 261024 run_long.ps1 had no `$ErrorActionPreference = 'Stop'`, so the
nized                      list went on and a C table ran on half-built inputs; it stops now.
```

Normal on this server, never a fault:

```
"(Not Responding)"   a Stata window busy in a long step; it has no time to redraw. Leave it, never X it;
                     choose Wait if Windows asks.
[wave5] SKIPPED      run_topic_pde is 0 in the pain cohorts (no C or D step reads all-fill features); waves
                     9-10 have no pain Task (run_topic_lines 0). The waves: b02 studio s01-case-pipeline-waves.
a quiet C window     the C launcher printed nothing for hours before 261025; it now prints each step from
                     log\by-step\ as it starts (run_fix_data_table.ps1 patches the server copy).
Killing Stata (PID)  Ctrl+C in that window: its launcher stopped its own Stata. Closing a window with X skips
                     this and leaves Stata running alone; match a dialog's run name to a live window first.
```

Two silent-wrong-number patterns this environment has produced twice:

```
a merge where BOTH sides carry the same column name: Stata keeps master's copy
with no warning, and the join is silently on the wrong thing.       [C01-02]
a merge on keys stored at different string widths: str16 against str10 gives
0 matches out of 2.7M, no error, no warning, an empty result.       [C01-03]
```

---

## Step 3: the hard limits

```
ASCII only, no CRLF          Windows PowerShell 5.1 is the shell
no `pwsh`                    PowerShell 7 is not installed
no `ssc install`             no network at runtime; built-ins only
                             (egen tag for distinct counts, never `distinct`)
one comment line = one       gate rule R14. A wrapped sentence FAILS the gate.
  sentence, never wrapped    A long line is fine.
no version string in a .ps1  gate rule R05. Versions live in one config.
the .done marker is the      never `$proc.ExitCode -ne 0`. Start-Process
  only success gate          -PassThru can return $null, and $null -ne 0 is TRUE
                             in PowerShell, so a GOOD run reports as failed.
cite as [ID] in the code     `// [C01-02] ...` at the causing line
no paste, no file upload     every character is typed by hand (since 261025: the
  (261025)                   CRD on-screen keyboard, /remote-keyboard-typist), so
                             server commands stay short: a Run by its address,
                             never its 200-character path
gci <wild*>\x -r finds      Windows PowerShell 5.1 reads a wildcard path with -r as a
  nothing (5.1)              NAME filter: `gci w\b21*\j31*\src -r` lists nothing and
                             `... | unblock-file` silently does nothing. Resolve first:
                             `gci (rvpa w\b21*\j31*\src) -r` (PowerShell 7 differs)
a running .do is read by     Stata reads a do-file as it runs: a server patch to a
  position                   file a live Stata is still in keeps its byte length
                             (`capture noisily do` -> `nobreak cap noi do`)
```

A file whose head reads `GENERATED FILE` is written by a script: change the script and rerun it (the Task
pages and the `sbatch\by_*` wrappers are written by `work/_tools/write_pages.py`). A `SHARED COPY` is edited in
every copy alike (Defaults above).

---

## Step 4: the gate, and what it cannot see

```bash
.venv/bin/python work/_tools/check_server_ready.py <UNIT>
```

19 rules, each one an entry in `_old/task.old/LESSON.MD`, each entry a failure that has
already cost a real run. Exit 0 means every rule passed.

Register entry **ALL-09** is why green is not proof: a synthetic unit built to
carry eleven real, observed-failure-class violations passed 17 of the 19 rules.
Thirteen rules can pass on a genuine violation. Say "Gate 1 green, <n>/19" and
never "this will run".

---

## Before an upload: the pre-flight (261022)

A failure on this server costs a day, so an upload is checked against every lesson first, not only the gate.
Run all of it; each step catches what the others cannot.

```
1 gates      check_server_ready.py (R14 alone is not runtime) · check_preupload.py 0 · check_task_tree.py 0
             (check_preupload.py M12: every server path under 260, folder 248, zip entry 240; run it on every
             Project's work/ that travels, siblings included)
2 register   read SERVER-READY-CHECK.md AND every <YYMMDD>/FINDINGS.md; its status column can be stale,
             so check each CRASH and SERVER entry in today's code, not in the table
3 patterns   no `set batch`, no `ssc install`, no `forvalues x = ${a}/${b}`, `estat firststage, all` only
             under capture, no PowerShell 7 syntax (`??`, `&&`, `ForEach-Object -Parallel`), no `pwsh`,
             no Python or `.sh` in a server ticket (ENV-08); check_preupload.py M11 finds the forvalues one,
             M13 a function in `file write` without its own parentheses (`(c(current_date))`), ASCII and no CR in every .do and .ps1,
             every launcher on stata-guard.do and setting STATATMP, only installed community commands
4 dry run    dryrun.py: every ticket through its real launcher; seed an asset only the server holds
             (case_osteo v0001) and rerun that part with --reuse/--refresh --only
5 inputs     what each stage reads must already be on F: (the dry run lists it); name what is missing
6 package    pack_upload.py <tag> --per-block (b02B.zip, b11CD.zip, ...); no result\, results\, passes\;
             every zip entry at most 240 characters (the packer refuses more), entries start at work\
7 unzip      test every zip: unzip -t, every file equal to the repo, and pwsh Expand-Archive into a short
             folder; the longest path at F:\u and at F:\Physician-SPACE must stay under 260
```

What the dry run proves: paths, launchers, `.done` markers, hand-offs between stages, path length. What it
cannot prove: any number, a missing column, or a guard that depends on data (the stand-in Stata marks such
conditions "unknown"). Read those guards in the code, and say which ones were read, not run.

When a whole stage fails the dry run at its input check, suspect the stand-in before the code: read the ticket's
rows in the sandbox's `ledger.jsonl` for `unknown` (a value it could not compute). On 261023 every full-year table
failed because `fakestata.py` had no `numlist ..., sort`, so the detected years were unknown and every year loop
was skipped; with that command added, all seven tables passed. Fix the stand-in, never the server code, for this.

## Running on the server

Since 261023 the server keeps the repo's own layout (`F:\Physician-SPACE\examples-2-cms\<Project>\work\`), and
every Run starts from `F:\Physician-SPACE` through a short root script, each named for the kind of Run it starts
(JL 261025). They live in the SPACE root of the repo and are typed onto the server by hand:

```
run_long.ps1 <path>, <path> [-Parallel]   the engine: runs tickets in order, stops at the first failure; an
                                          OpioidRx path goes through F:\Physician-SPACE\w, a junction to its
                                          work\ (same folder, longest path 253, the C/D 23-character check met)
run_case_year.ps1 -v <visit> -y <years>   stage B: every case Task of a visit, per year, in tNN order; any CMS
                                          Project (LBP ... T2D, AMI, AiProc); -Parallel: a window per visit-year
run_bjtr.ps1 b11.j21.t01.r04, ...         any one Run by its address; refuses an address with 0 or 2 tickets
run_tables.ps1 / run_tables_pooled.ps1    stage C: the cohort tables, then b19's pooled table (it reads LBP,
                                          Osteo, Headache, Cancer)
run_paper_jama.ps1 / run_paper_misq.ps1   stage D: the Runs each paper's results Block (b51, b52) reads
run_fix.ps1, run_fix_data_table.ps1       one-off server patches (the guard's nobreak; the C launcher's steps)
```

- A Run is never started by its own long path on the server: with no paste, the address is the whole command.
- Wait for every window of one stage (`Finished!`, or `complete`) before the next stage; each reads the last.
- Never press Ctrl+C in a running window to copy: it stops that run. Select text first, or right-click.
- Unpack an upload with PowerShell, not by double-clicking: all zips into one short folder, then copy its `work\`
  over `F:\Physician-SPACE\work` (add and replace, never delete):
  `Get-ChildItem F:\<tag>-PerBlock\*.zip | ForEach-Object { Expand-Archive $_.FullName -DestinationPath F:\u -Force }`
- After a new upload, run two short tickets first (the package's `README-UPLOAD.md` names them): one that reads
  headers only (`b01_A_cms_description\j01_A0_cms_description\sbatch\run_slice.ps1`), and one that MUST fail in
  seconds (`b14_CD_visit_pain_musc\j21_D_reg_VisitMusc_1stPair_yr16_19_bigfive_ols\t01_C1_D_reg_VisitMusc_agre\runs\
  r01_D_reg_VisitMusc_1stPair_agre_af7d_ols\r01_D_reg_VisitMusc_1stPair_agre_af7d_ols.ps1`: until the full-year table
  is built it stops with `MISSING FILE` and r(601)). It proves an error ends Stata instead of opening the /e dialog
  (ENV-01/ENV-11); if the dialog opens instead, close it and stop.

## Bringing results back

`collect_results.ps1 [-Block b11] [-WhatIf]` (`-Block` is a name prefix; there is no Task filter) packs only aggregate output (`RUN-REPORT.md`, `tables\`, `describe\`,
`summary.txt`, receipts; b01's step logs) into `F:\ret\work-<yyMMdd>.zip`, by Run path, and judges every file
for the colleague who reviews it before it leaves:

```
STOP   an identifier column (bene_id, npi_id, clm_id, pde_id) or a count 1-10: held back, never zipped
LOOK   a log, a picture, or text that may print a small count or a 10-digit number: a person reads it
OK     an aggregate table or receipt with no count under 11 and no identifier
```

The reviewer reads `EXPORT-REVIEW.md` first (STOP and LOOK only, grouped by reason); each Run's `REVIEW.md`
explains every file in one line. On the laptop, `file_server_return.py <zip> --apply` files each part into its
own Run and refuses a count 1-10 again. A file the script cannot read (a CSV with two columns of one name) is
LOOK, never a crash of the whole pack.

## CMS status and local verification

A local fix is `🟠 FIXED`; it becomes `✅ CLOSED` only after a clean remote run.
The remaining states are `🔴 OPEN`, `🟡 PARTIAL`, and `⚪ KNOWN`. Use this
vocabulary only for this profile. Report the actual static gate verdict as
`<UNIT> n/<total>`; if the checker is unavailable, say so and leave that
verification pending. Never substitute a successful local edit for a gate.

## Step 5: the ID prefixes

Ruled by JL 260822, replacing a flat `S01..S37` counter that told a reader
nothing about where to look. Six characters, always.

```
ENV-nn   the SERVER itself: Stata, PowerShell, the filesystem.
         No task folder can fix an ENV issue.
ALL-nn   the .ps1 runner or config SHAPE. The same shape sits in EVERY task
         folder, so an ALL fix is a sweep, not one edit.

A11-nn   work/A11_CMS-pipeline
C01-nn   work/B01_CaseData_TraitOpioid   (case stage)
R01-nn   work/R01_Reg_TraitOpioid
R02-nn   work/R02_Reg_TraitDiabetesNDC
R03-nn   work/R03_Reg_TraitCABG
```

The prefix is the folder's own index, verbatim, never an abbreviation invented
for the register. A folder with no issues yet has no prefix yet.

The register's four files:

```
${REGISTER}/SERVER-READY-CHECK.md   the register: one line per issue, ID, status
${REGISTER}/ISSUE.md                the same issues drawn, one diagram each
${REGISTER}/AUDIT.md                the other axis: task folder vs its issues
${REGISTER}/<YYMMDD>/FINDINGS.md    the day it was seen, plus raw screenshots
```

---

## PHI, which overrides everything above

CMS data is protected health information. `_WorkSpace/1-CMS-Store`,
`2-Data-Store` and any `cms_full` stay on the secure server; only aggregated
output is movable. Never paste a data row, a `bene_id`, or an `npi_id` into an
issue file, a log excerpt, or a chat reply. A column NAME is fine; a column
VALUE is not.

`cms_synth` is laptop-safe and is never used for substantive results.
