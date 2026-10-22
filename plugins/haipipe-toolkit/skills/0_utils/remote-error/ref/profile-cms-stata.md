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
upload package     python work/_tools/pack_upload.py <tag> [--check]
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
exit 0  after an error     Stata does this. ENV-02. The marker is the only gate.
modal   any error at all   /e mode pops a dialog and the run waits all night for
dialog                     a click. ENV-01. `set batch` does not exist here.
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
2 register   read SERVER-READY-CHECK.md AND every <YYMMDD>/FINDINGS.md; its status column can be stale,
             so check each CRASH and SERVER entry in today's code, not in the table
3 patterns   no `set batch`, no `ssc install`, no `forvalues x = ${a}/${b}`, `estat firststage, all` only
             under capture, no PowerShell 7 syntax (`??`, `&&`, `ForEach-Object -Parallel`), no `pwsh`,
             no Python or `.sh` in a server ticket (ENV-08), ASCII and no CR in every .do and .ps1,
             every launcher on stata-guard.do and setting STATATMP, only installed community commands
4 dry run    dryrun.py: every ticket through its real launcher; seed an asset only the server holds
             (case_osteo v0001) and rerun that part with --reuse/--refresh --only
5 inputs     what each stage reads must already be on F: (the dry run lists it); name what is missing
6 package    pack_upload.py <tag>, then --check: 0 differences from the repo; no result\, results\, passes\
```

What the dry run proves: paths, launchers, `.done` markers, hand-offs between stages, path length. What it
cannot prove: any number, a missing column, or a guard that depends on data (the stand-in Stata marks such
conditions "unknown"). Read those guards in the code, and say which ones were read, not run.

## Running on the server

Every Task runs one way, from the SPACE folder, by its `by_task` wrapper. The laptop path minus
`examples-2-cms/Project-Personality-OpioidRx/` is the server path:

```powershell
cd F:\Physician-SPACE
.\work\b11_CD_visit_pain_lbp\j21_C1D_reg_VisitLBP_1stPair_yr15_20_bigfive_ols\sbatch\by_task\t04_C1_D_reg_VisitLBP_extr.ps1 -WhatIf
.\work\b11_CD_visit_pain_lbp\j21_C1D_reg_VisitLBP_1stPair_yr15_20_bigfive_ols\sbatch\by_task\t04_C1_D_reg_VisitLBP_extr.ps1 -ContinueOnError
```

- `-WhatIf` prints the Runs and starts none; `-Sequential` runs one at a time; filters compose (`-Window af14d`).
- The wrapper finds its Job from its own place (`$PSScriptRoot`), so the folder you start in does not matter;
  `\` and `/` both work. `.\sbatch\run_slice.ps1` from a Job folder runs the whole Job.
- Every Task has a wrapper, a Job of one Task too: `write_pages.py` writes them (it always writes `by_task`).
- Never copy `work\` to the repo's depth (`F:\Physician-SPACE\examples-2-cms\...`): the deepest files pass
  259 characters there, and the C and D launchers refuse a home folder longer than 23 characters.
- After a new upload, run two short tickets first (the package's `README-UPLOAD.md` names them): one that reads
  headers only (`b01_A_cms_pipeline\j01_A0_cms_description\sbatch\run_slice.ps1`), and one that MUST fail in
  seconds (`b14_CD_visit_pain_musc\j02_C2_data_VisitMusc_1stPair_yr15_24\t01_C2_data_build_VisitMusc\runs\r02_*.ps1`,
  Musc has no 2021-2024 case years). It proves an error ends Stata instead of opening the /e dialog (ENV-01/ENV-11);
  if the dialog opens instead, close it and stop.

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
