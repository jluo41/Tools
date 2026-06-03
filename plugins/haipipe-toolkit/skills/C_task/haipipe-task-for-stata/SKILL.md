---
name: haipipe-task-for-stata
description: "Stata-engine task-folder build sub-orchestrator — the parent of the four haipipe-task-for-stata-* specialists (cms / case / data / reg). Owns the Stata engine contract, the {LNN} stage-letter alphabet, and stage disambiguation; smartly delegates a Stata build request to the right child. Called by /haipipe-task when engine=Stata; direct invocation works for any Stata-dialect scaffold. Engine = Stata + PowerShell + logs (NOT Python/papermill)."
argument-hint: "[stage] [project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-for-stata  (Stata sub-orchestrator)
====================================================

The **father skill** for Stata task-folder builds. `/haipipe-task` routes any
**engine=Stata** request here; this skill picks the right **stage** specialist
and delegates. The four children differ only in RUNNAME grammar, output store,
and headline — they share ONE execution dialect (`../haipipe-task/ref/stata-dialect.md`).

```
/haipipe-task   (top: ML task-types + engine routing)
└── /haipipe-task-for-stata          ◀── you are here   (Stata engine; stage router)
      ├── /haipipe-task-for-stata-cms     A · 1-CMS-Store   (heavy, per year)
      ├── /haipipe-task-for-stata-case    B · 2-Case-Store  (heavy, cohort × year)
      ├── /haipipe-task-for-stata-data    C · *-Data-Store  (heavy, cross-year)
      └── /haipipe-task-for-stata-reg     D · results/      (LIGHT coef tables)
```


Stage dispatch table
--------------------

```
stage   task-type     Specialist                        {LNN} letter   Output store
─────   ───────────   ────────────────────────────────  ────────────   ────────────────────────
cms     stata-cms     /haipipe-task-for-stata-cms        A              1-CMS-Store   (heavy)
case    stata-case    /haipipe-task-for-stata-case       B              2-Case-Store  (heavy)
data    stata-data    /haipipe-task-for-stata-data       C              *-Data-Store  (heavy)
reg     stata-reg     /haipipe-task-for-stata-reg        D              results/      (LIGHT)
```

The `{LNN}` letter encodes the stage so a task-folder sorts in pipeline order
(`A`cms → `B`case → `C`data → `D`reg). Full definition: the "Task-folder
`{LNN}` stage-letter alphabet" section in `../haipipe-task/ref/stata-dialect.md`.


Stage disambiguation (the "smart delegation")
---------------------------------------------

The bare keyword `stata` (or a `.do` file) signals this skill; the accompanying
**stage word** picks the child:

```
┌────────────┬─────────────────────────────────────────────────────────────────┐
│ stata-cms  │ cms · cms-pipeline · neat · bene_info · extract claims ·         │
│            │ elixhauser · raw cms · per year                                  │
│ stata-case │ case-pipeline · trigger cases · cohort · visit · bfaf ·          │
│            │ opioidrx · case panel · cohort × year                            │
│ stata-data │ data-pipeline · analysis table · filter case · filter external · │
│            │ full variables · ANALYSIS-*.dta · cross-year                     │
│ stata-reg  │ reg · regression · ols · iv · instrument · estimate ·            │
│            │ coef table · two-part · lpm · logit · first-stage                │
└────────────┴─────────────────────────────────────────────────────────────────┘
```

Cascade:
  (1) EXPLICIT — stage given as a positional (`cms`/`case`/`data`/`reg`) → use it.
  (2) KEYWORD-INFERRED — first stage keyword in the args wins.
        AUTO        → accept; log "inferred stata stage '<kw>': <stage>"
        interactive → propose; one-line confirm.
  (3) STILL UNKNOWN — `stata` present but no stage word:
        AUTO        → status: blocked, reason: "stata engine but stage unknown
                      (pass cms/case/data/reg, or a stage keyword)."
        interactive → ASK which of the four stages.


Routing protocol
----------------

Step 0: Read `../haipipe-task/ref/stata-dialect.md` (the engine contract) — the
        three CWD/location-independence rules (Stata auto-detect, run-from-
        `$PSScriptRoot`, `ws_root`-anchored output) and the `{LNN}` alphabet.

Step 1: Detect AUTO_MODE (same triggers as `/haipipe-task`: `--auto`, env, or
        parent passed `--auto`).

Step 2: Resolve stage via the cascade above.

Step 3: Verify ancestors exist (project → group), mirroring `/haipipe-task`
        Step 3b. If a `--project-id` / `--group` is given and missing, scaffold
        via `/haipipe-task` (project / task-group) first; else ASK / block.

Step 4: Delegate —
          Skill("haipipe-task-for-stata-<stage>",
                args="<remaining_args> --project-id <P> --group <G> [--auto]")
        Capture the child's return contract and surface it as our own.


Shared engine assets (all four children inherit these)
------------------------------------------------------

```
../haipipe-task/ref/stata-dialect.md            engine contract + {LNN} alphabet + portability rules
../haipipe-task/ref/run-ps1-template.ps1        per-run ENTRY (resolves ws_root via pyproject; writes runtime.yaml)
../haipipe-task/ref/run-stage-year-template.ps1 intra-run ORCHESTRATOR (Resolve-StataExe; $PSScriptRoot CWD; phases)
../haipipe-task/ref/dispatcher-do-template.do   DISPATCHER (5-arg: <config> <step> <year> <results_dir> <ws_root>)
```

Three portability rules (DO NOT re-derive per task — the templates already bake them):
  1. Resolve Stata, never hardcode a version (`Resolve-StataExe`; honors `$env:HAIPIPE_STATA`).
  2. Run from the task folder (`$PSScriptRoot`); code paths stay relative; folder name is free.
  3. Anchor the DATA root absolute via `ws_root` (config builds paths from `${ws_root}`, never literal `_WorkSpace`).

Every Stata task ALSO ships a read-only **describe / QC run** (`describe` dispatch
step → `scripts/d-<Stage>-Describe.do`, + `runs/run_describe_<...>.ps1`) that
writes a human-readable correctness report to `results/`. Built-ins only — NO SSC
(`egen tag` for distinct counts, never `distinct`). See the "Describe / QC run"
section in `../haipipe-task/ref/stata-dialect.md`; each child scaffolds the
stage-specific version.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences — which stage was chosen + what the child scaffolded
artifacts: [paths created]   (from the child)
next:      author dispatcher .do + scripts/ workers (incl. a `describe` step + run_describe_*.ps1 QC run); CODE_REVIEW.md; then runs/<run>.ps1
```
