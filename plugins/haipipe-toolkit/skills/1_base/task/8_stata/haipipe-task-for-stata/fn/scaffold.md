fn-scaffold: Scaffold a Stata job
==========================================

Unified scaffold for all 4 Stata stages.
Read `ref/stata-dialect.md` first for the engine contract.

Output: `work/bNN_<block>/jNN_<job>/tNN_<task>/`; stage belongs in the suffix.


Step 1 -- Identify project + block
----------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK block.


Step 2 -- Resolve stage
------------------------

- Stage must be known before scaffolding (cms/case/data/reg).
- If not given: AUTO_MODE -> `status: blocked`. Interactive -> ASK which of the four stages.


Step 3 -- Collect metadata
---------------------------

- Allocate unused bNN/jNN/tNN/rNN indices at their own levels; preserve existing identities.
- snake_case task_name.
- Stage-specific axis:
    cms:  year axis (2015..2020) -> one run per year
    case: cohort list + source list (synth/full) + year axis -> one run per (cohort x source x year)
    data: spec name (cross-year, NO year axis) -> one run per spec
    reg:  window x estimator-family grid -> one run per (window x family)
- `_meta:` block.


Step 4 -- Create skeleton
--------------------------

Stage-specific tree (see SKILL.md for the full tree per stage).
Common elements:

    work/bNN_<block>/board.md
    work/bNN_<block>/jNN_<job>/src/                 shared runner .ps1, libraries, defaults
    work/bNN_<block>/jNN_<job>/tNN_<task>/
      tNN_<task>.md + draft/ + workflow/
      scripts/                                    dispatcher, workers (a runner only this Task uses)
      scripts/config/<cfg>.do                     shared globals every Run's config.do loads
      runs/rNN_<run>/rNN_<run>.ps1                the Ticket: two lines into the Job's runner
      runs/rNN_<run>/config.do                    this Run's globals
      runs/rNN_<run>/config.yaml                  optional metadata wrapper (_meta + stata_config)
      runs/rNN_<run>/run.yaml                     its card: run, kind: hard, role, type, status
      sbatch/                                     optional, Task-local only

    Results: $OUTPUT_ROOT/<task>/runs/rNN_<run>/result/ (logs, summary, snapshots, runtime.yaml)
             reg: result/ keeps RUN-REPORT.md, tables/, describe/; passes/pNN-<MMDD>/ keeps logs, .done, runtime.yaml
    Resolve RESULT_STORE, then Job store declaration, then Job root before launch.

Stage differences:
- cms/case: dispatcher .do (from ref/dispatcher-do-template.do) + runner .ps1 in the Job's src/ (from ref/run-stage-year-template.ps1) + scripts/ subdirs
- data: dispatcher .do + scripts/ numbered subdirs, NO orchestrator (self-orchestrating: the Run's ticket IS the orchestrator)
- reg: DISPATCHER-LESS -- .ps1 runners call worker .do scripts directly; no orchestrator


Step 5 -- Seed configs
-----------------------

Copy the shared seed to `scripts/config/<cfg>.do` and create each Run's own wrapper `runs/rNN_<run>/config.do` beside its Ticket.
The wrapper selects shared globals and pins the variant; shared configs never substitute for a Run identity.
Fill in Stata globals (keep-vars, paths, flags).
The `.do` is the source of truth; a companion `.yaml` carries only the `_meta:` discipline block.

Stage-specific seeding:
- cms: one `runs/rNN_<run>/config.do` per year, loading shared `cms_production.do` and pinning `global data_year <year>`. The optional `runs/rNN_<run>/config.yaml` `stata_config:` points to that wrapper.
- case: three layers -- (1) `_source_{synth|full}.do` source selectors, (2) `<Cohort>.do` shared cohort config, (3) the Run's thin `runs/rNN_<run>/config.do` from `ref/config-seed-run.do`. One Run folder (config.do, optional config.yaml) per (cohort x source x year).
- data: paired configs per spec (synth + real variants). No year axis.
    (1) `<Spec>.do` -- synth config (laptop-safe). `data_asset_version "v001_base_synth"`.
    (2) `<Spec>_real.do` -- real config (CMS server). `data_asset_version "v001_base_real"`.
        `case_asset_version` is TODO-tagged until real case-pipeline runs complete.
    Identical except: case_asset_version, data_asset_version, file_physician path.
    Each spec variant is instantiated as its own Run folder `runs/rNN_<run>/` (config.do + Ticket + run.yaml) with its `result/`. sbatch accepts `-mode synth|real|all`.
- reg: two-layer chain from `ref/config-seed-reg.do` + `ref/config-seed-reg-run.do`:
    (1) `<Cohort>_<Pairing>.do` -- shared: data path + version.
    (2) `<Cohort>_<Pairing>_synth.do` -- shared synth variant (different data_version).
    (3) `runs/rNN_<run>/config.do` -- per-run: loads shared + pins outcome_bfaf_window + res_dir (+ pass_dir).
        DID per-run configs add: `global file_policy "${ws_root}/0-External-Store/Policy/..."`.
    YAML _meta companions are OPTIONAL for reg (simple 5-7 line .do configs are self-describing).
    Controls/outcomes/instruments live in worker .do scripts, NOT in configs.


Step 6 -- Run-scripts
----------------------

Every Run is one folder `runs/rNN_<run>/`: its Ticket `rNN_<run>.ps1`, its `config.do` (Step 5) and its card `run.yaml`
(`run`, `kind: hard`, `role:` make, trial for a synth try, or describe; `type`, `scope`, `ticket`, `skill: haipipe-task-for-stata`, `status: planned`).

**cms/case:** Copy `ref/run-ps1-template.ps1` to `runs/rNN_<run>/rNN_<run>.ps1` for each RUNNAME.
Thin entries that hand `config.do` to the Job's runner; in a Run folder this is the two-line caller
`& "$PSScriptRoot\..\..\..\src\run_<stage>_year.ps1" "$PSScriptRoot\config.do"`.

**data:** Copy `ref/run-data-runner-template.ps1` to `runs/rNN_<run>/rNN_<run>.ps1`.
Self-orchestrating entries (or the two-line caller into the Job's `src/0-libs/run-data-pipeline.ps1`).

**reg:** Copy `ref/run-ps1-reg-template.ps1` to `runs/rNN_<run>/rNN_<run>.ps1`.
Self-contained runners with Resolve-StataExe + HAIPIPE_RUN_CONFIG + worker list (or the two-line caller into the Job's `src/0-libs/run-regression-pipeline.ps1`).

For cms/case: also copy `ref/run-stage-year-template.ps1` to the Job's `src/` as `run_<stage>_year.ps1` (a Task's `scripts/` when only that Task uses it).
For data/reg: no separate orchestrator -- the runner IS the orchestrator.

Optional: create sbatch/*.ps1 multi-run batchers.


Step 7 -- Report
-----------------

    status:    ok
    summary:   Scaffolded <stage> task <NN>_<name> under the selected bNN Block / jNN Job.
    artifacts: [paths created]
    next:      author dispatcher .do + scripts/ workers (incl. describe step); run haipipe-task-reviewer-agent before hand-copy


MUST NOT
---------

- Write heavy `.dta` files to a Run's `result/` -- they go to `_WorkSpace/{1..4}-*Store/` (exception: reg writes LIGHT .tex/.csv only).
- Skip `_meta:` block in any config YAML.
- Create `README.md` -- use `diagram/` for docs.
- Use papermill or `.ipynb` -- this is Stata + PowerShell.
- Use SSC packages in describe scripts (`egen tag` for distinct counts, NOT `distinct` which aborts r(199)).
- For reg: collapse grid runs -- one run per (window x family), collapsing is forbidden.


First-run gate
---------------

Before hand-copy to the CMS server, run `haipipe-task-reviewer-agent` on the job folder.
The reviewer enforces the "Script style + server constraints" contract in `ref/stata-dialect.md` (Windows PowerShell 5.1 only, ASCII files, thin headers, no ceremony).
