fn-scaffold: Scaffold a reg-pipeline task-folder (Stata dialect)
================================================================

Runs the estimation grid (OLS / IV / LPM / logit / two-part) on the
data-stage analysis table, writing LIGHT coefficient tables into
`results/<run>/`. Output:
`tasks/{G}{NN}_<group>/{NN}_reg_pipeline_<study>/`.
Read `../haipipe-task/ref/stata-dialect.md` for the engine contract.

KEY DIFFERENCE from cms/case/data: the primary output is LIGHT (coef
tables in-repo under `results/`), not a heavy `.dta` in `_WorkSpace/`.
The grid fans wide — organize `runs/` and `stata/` in per-spec subfolders.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (`examples/Proj*/`).
- ASK task-group. Reg work lives in the study group
  (e.g. `R1_Regression_TraitOpioid`) next to its case + data siblings.
- Confirm the upstream data-pipeline task exists (reg consumes its
  `ANALYSIS-*.dta`). If not, suggest `/haipipe-task-for-stata-data` first.


Step 2 — Collect metadata (the grid)
-------------------------------------

- 2-digit NN: next free in this group.
- task_name: `reg_pipeline_<study>` (e.g. `reg_pipeline_opioid`).
- **The estimation grid** — the cartesian product that defines RUNNAMEs:
  - Conditions  (e.g. VisitLBP, VisitWithOpioid)
  - Pairings    (e.g. 1stPair)
  - Traits      (Big Five: Agreeableness, Conscientiousness, ...)
  - Estimators  (ols: progressive/lpm-logit/twopart/windows/traitform;
                 iv: main/grid/overid)
- IV definitions (instrument naming / leave-one-out construction).
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
{NN}_reg_pipeline_<study>/
├── stata/
│   └── <Condition>_<Pairing>/        # per-spec worker .do (run-1..8); authored later
├── configs/
│   └── run_reg_<Condition>_<Pairing>_<Trait>.yaml
├── runs/
│   └── <Condition>_<Pairing>/
│       ├── run-<Condition>_<Pairing>_<Trait>-ols.ps1
│       └── run-<Condition>_<Pairing>_<Trait>-iv.ps1
├── sbatch/
│   ├── run-<Trait>-all.ps1
│   ├── run-<Condition>_<Pairing>-all.ps1
│   └── run-all.ps1
├── results/
└── diagram/
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to
`configs/run_reg_<Condition>_<Pairing>_<Trait>.yaml`. Fill `_meta`, set
`condition:`, `pairing:`, `trait:`, `estimators:`. Shared estimation
settings (controls, cluster level, FE) may live in a `configs/*.do`.


Step 5 — Run-script
-------------------

Copy `../haipipe-task/ref/run-ps1-template.ps1` to each
`runs/<Condition>_<Pairing>/run-<Condition>_<Pairing>_<Trait>-<est>.ps1`.
Set `$RUNNAME = "run_reg_<Condition>_<Pairing>_<Trait>-<est>"`, the
`$REQUIRED` analysis-table precondition, and call the per-spec estimation
`.do` (this stage often calls Stata directly rather than via a
`run_<stage>_year.ps1` orchestrator — there is no year axis).

Because output is LIGHT, the `summary.txt` headline should surface the
key coefficient (β · SE · N; first-stage F for IV).


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded reg-pipeline task <NN>_reg_pipeline_<study> under {G}{NN}_<group>; grid <conds × pairings × traits × estimators>.
artifacts: [paths created]
next:      author per-spec estimation .do files; CODE_REVIEW.md (IV validity / spec / clustering); then runs/.../<run>.ps1
```


MUST NOT
---------

- Send coefficient tables to `_WorkSpace/` — reg output is LIGHT, in-repo
  under `results/<run>/`.
- Skip the `_meta:` block. Create `README.md`. Use papermill / `.ipynb`.
- Collapse the grid into one run — each spec cell is its own RUNNAME so
  results pair 1:1 and task-log.md stays legible.
