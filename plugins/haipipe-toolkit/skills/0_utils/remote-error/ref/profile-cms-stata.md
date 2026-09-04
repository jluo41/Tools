# Profile: cms-stata

The CMS secure server. Stata batch mode plus Windows PowerShell 5.1, driving CMS
Medicare claims that never leave that machine.

Load this profile when the pasted error carries an `r(nnn)` Stata code, a `.do`
or `.ps1` path, or a `results/<run>/log/` path. Home repo: `Physician-SPACE`,
project `examples/Project-Personality-OpioidRx`.

Two skills own the other half of this environment and should be read alongside:
`haipipe-task-for-stata` (scaffold a task folder, run the pre-flight gate, write
`SERVER_CHECK.md`), and its `ref/cms-server-checklist.md` (the three-gate model
and the full register naming rules).

---

## Defaults

```
register default   _WorkSpace/0-CMS-Store/Issue-From-CMS-Server/
register index     SERVER-READY-CHECK.md
status file        <task-folder>/ISSUES.md
static gate        python3 tasks/_tools/check_server_ready.py <UNIT>    19 rules
lessons file       tasks/LESSON.MD
sync command       python3 tasks/_tools/sync_shared.py
drift check        python3 tasks/_tools/sync_shared.py --check
canonical root     tasks/00_cms-stata-template/
```

`<UNIT>` is a prefix, not a path: `R01`, `C01`, `A11`, `R03`.

---

## Phase 1: where the error actually is

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

---

## Phase 2: the code table

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

## Phase 3: the hard limits

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

A file whose head reads `GENERATED FILE` names its canonical under
`tasks/00_cms-stata-template/`. Edit there, then `sync_shared.py`. Gate rule R19
fails until you do.

---

## Phase 4: the gate, and what it cannot see

```bash
python3 tasks/_tools/check_server_ready.py <UNIT>
```

19 rules, each one an entry in `tasks/LESSON.MD`, each entry a failure that has
already cost a real run. Exit 0 means every rule passed.

Register entry **ALL-09** is why green is not proof: a synthetic unit built to
carry eleven real, observed-failure-class violations passed 17 of the 19 rules.
Thirteen rules can pass on a genuine violation. Say "Gate 1 green, <n>/19" and
never "this will run".

---

## Phase 5: the ID prefixes

Ruled by JL 260822, replacing a flat `S01..S37` counter that told a reader
nothing about where to look. Six characters, always.

```
ENV-nn   the SERVER itself: Stata, PowerShell, the filesystem.
         No task folder can fix an ENV issue.
ALL-nn   the .ps1 runner or config SHAPE. The same shape sits in EVERY task
         folder, so an ALL fix is a sweep, not one edit.

A11-nn   tasks/A11_CMS-pipeline
C01-nn   tasks/B01_CaseData_TraitOpioid   (case stage)
R01-nn   tasks/R01_Reg_TraitOpioid
R02-nn   tasks/R02_Reg_TraitDiabetesNDC
R03-nn   tasks/R03_Reg_TraitCABG
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
