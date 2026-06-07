fn-scaffold: Scaffold a reg-pipeline task-folder (Stata dialect)
================================================================

Runs the estimation grid (OLS / IV / LPM / logit / two-part) on the
data-stage analysis table, writing LIGHT coefficient tables into
`results/<run>/`. Output:
`tasks/{G}{NN}_<group>/D{NN}_reg_pipeline_<study>/`  (task-folder letter D = reg stage).
Read `../haipipe-task-for-stata/ref/stata-dialect.md` for the engine contract.

KEY DIFFERENCE from cms/case/data: the primary output is LIGHT (coef
tables in-repo under `results/`), not a heavy `.dta` in `_WorkSpace/`.
The grid fans wide — organize `runs/` and `scripts/` in per-spec subfolders.

**Default vs topic-split.** By default ONE study folder holds the whole grid
(condition × pairing × trait × estimator) in per-spec subfolders. ACCEPTED
project-local override: if two conditions are genuinely *different topics*, split
into one folder PER topic — `D{NN}_reg_pipeline_<condition>_<pairing>` — making
the condition the folder boundary. Then the folder name already names the spec,
so FLATTEN the redundant inner subfolder (`runs/` + `scripts/` directly). Each
topic still keeps trait × estimator as its inner grid.


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
D{NN}_reg_pipeline_<study>/          # task-folder letter D = reg stage ({LNN})
├── scripts/
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


Step 5 — Run-script (reg runtime contract)
------------------------------------------

Reg is **dispatcher-less** — each `runs/.../<run>.ps1` calls its estimation
`scripts/...do` DIRECTLY (no `run_<stage>_year.ps1`, no year axis). Each `.ps1`:

- sets `$stata` to the server exe (ONE editable line at the top — no resolver functions);
- resolves the absolute `_WorkSpace` (walk up to `pyproject.toml`) and exports it
  as `$env:HAIPIPE_WS_ROOT` — the `.do` reads it AFTER `clear all` via
  `global ws_root : environment HAIPIPE_WS_ROOT` (a `do`-arg/global would not
  survive `clear all`; see ref/stata-dialect.md "reg-stage exception");
- runs Stata from the task folder: `Push-Location $TASK_DIR; try { & $stata /e do
  "scripts/<run>.do" } finally { Pop-Location }`;
- input ← `${ws_root}/3-Data-Store/<spec>/…ANALYSIS-*.dta`; output →
  task-relative `results/<run>.log` + coef tables (LIGHT, in-repo).

A `.ps1` may run ONE cell or loop a worker family (e.g. `-ols.ps1` → run-1..5,
`-iv.ps1` → run-6..8). NO path hardcodes the folder name → renamable by `mv`.

Because output is LIGHT, the `summary.txt` headline should surface the
key coefficient (β · SE · N; first-stage F for IV).


Step 5b — Describe / QC run
---------------------------

Reg's "describe" is a **coefficient-sanity** report (see "Describe / QC run" in
`../haipipe-task-for-stata/ref/stata-dialect.md`). Since reg is dispatcher-less and output
is LIGHT, this is a `runs/run_describe_<Trait>.ps1` that runs a
`scripts/d-Reg-Describe.do` (read-only) which parses the per-spec estimation
logs / saved estimates and `file write`s `reg-describe.txt`: per cell the trait
β · SE · N (first-stage F for IV), and FLAGS any cell that failed to estimate
(no-obs, dropped/collinear). Built-ins only; `capture`-guarded. (The per-run
`summary.txt` headline already surfaces the key β · SE · N; this aggregates the
whole grid into one glance.)


Step 6 — Report
----------------

```
status:    ok
summary:   Scaffolded reg-pipeline task <NN>_reg_pipeline_<study> under {G}{NN}_<group>; grid <conds × pairings × traits × estimators>.
artifacts: [paths created]
next:      author per-spec estimation .do files (+ d-Reg-Describe.do); CODE_REVIEW.md (IV validity / spec / clustering); then runs/.../<run>.ps1 (+ run_describe_<Trait>.ps1)
```


MUST NOT
---------

- Send coefficient tables to `_WorkSpace/` — reg output is LIGHT, in-repo
  under `results/<run>/`.
- Skip the `_meta:` block. Create `README.md`. Use papermill / `.ipynb`.
- Collapse the WHOLE grid (all conditions/traits/estimators) into one run.
  Keep runs at the trait × estimator-family grain so results stay legible.
  (Grouping a worker *family* — e.g. one `-ols.ps1` looping run-1..5 — is fine;
  collapsing distinct traits/conditions into a single run is not.)
