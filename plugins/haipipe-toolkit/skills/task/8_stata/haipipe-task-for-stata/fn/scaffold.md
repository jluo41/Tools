fn-scaffold: Scaffold a Stata task-folder
==========================================

Unified scaffold for all 4 Stata stages. Read `ref/stata-dialect.md` first for the engine contract.

Output: `tasks/{G}{NN}_<group>/{LNN}_{task_name}/` where {L} = stage letter (A=cms, B=case, C=data, D=reg).


Step 1 -- Identify project + task-group
----------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: ASK task-group.


Step 2 -- Resolve stage
------------------------

- Stage must be known before scaffolding (cms/case/data/reg).
- If not given: AUTO_MODE -> `status: blocked`. Interactive -> ASK which of the four stages.


Step 3 -- Collect metadata
---------------------------

- 2-digit NN: next free in this group.
- snake_case task_name.
- Stage-specific axis:
    cms:  year axis (2015..2020) -> one run per year
    case: cohort list + source list (synth/full) + year axis -> one run per (cohort x source x year)
    data: spec name (cross-year, NO year axis) -> one run per spec
    reg:  window x estimator-family grid -> one run per (window x family)
- `_meta:` block.


Step 4 -- Create skeleton
--------------------------

Stage-specific tree (see SKILL.md for the full tree per stage). Common elements:

    {LNN}_{task_name}/
    |- configs/              Stata .do configs (source of truth) + YAML _meta wrappers
    |- runs/                 THIN .ps1 entries (from ref/run-ps1-template.ps1)
    |- sbatch/               multi-run batchers (optional)
    |- results/              log/ + summary.txt (no ceremony -- no manifest.json)
    +- diagram/              doc surface (never README.md)

Stage differences:
- cms/case/data: have a dispatcher .do (from ref/dispatcher-do-template.do) + orchestrator .ps1 (from ref/run-stage-year-template.ps1) + scripts/ subdirs
- reg: DISPATCHER-LESS -- .ps1 runners call worker .do scripts directly; no orchestrator


Step 5 -- Seed configs
-----------------------

Copy `ref/config-seed-<stage>.do` to `configs/<cfg>.do`. Fill in Stata globals (keep-vars, paths, flags). The `.do` is the source of truth; a companion `.yaml` carries only the `_meta:` discipline block.

Stage-specific seeding:
- cms: one config per year. `stata_config:` points to shared `cms_production.do`.
- case: three layers -- (1) `_source_{synth|full}.do` source selectors, (2) `<Cohort>.do` shared cohort config, (3) thin per-run `<Cohort>_<source>_<year>.do` from `ref/config-seed-run.do`. One YAML + one .do per (cohort x source x year).
- data: paired configs per spec (synth + real variants). No year axis.
    (1) `<Spec>.do` -- synth config (laptop-safe). `data_asset_version "v001_base_synth"`.
    (2) `<Spec>_real.do` -- real config (CMS server). `data_asset_version "v001_base_real"`.
        `case_asset_version` is TODO-tagged until real case-pipeline runs complete.
    Identical except: case_asset_version, data_asset_version, file_physician path.
    Each gets its own runner + results dir. sbatch accepts `-mode synth|real|all`.
- reg: two-layer chain from `ref/config-seed-reg.do` + `ref/config-seed-reg-run.do`:
    (1) `<Cohort>_<Pairing>.do` -- shared: data path + version + res_root.
    (2) `<Cohort>_<Pairing>_synth.do` -- shared synth variant (different data_version).
    (3) `run_reg_<RUNNAME>.do` -- per-run: loads shared + pins outcome_bfaf_window + res_dir.
        DID per-run configs add: `global file_policy "${ws_root}/0-External-Store/Policy/..."`.
    YAML _meta companions are OPTIONAL for reg (simple 5-7 line .do configs are self-describing).
    Controls/outcomes/instruments live in worker .do scripts, NOT in configs.


Step 6 -- Run-scripts
----------------------

**cms/case:** Copy `ref/run-ps1-template.ps1` to `runs/<run>.ps1` for each RUNNAME. Thin entries that delegate to the orchestrator .ps1.

**data:** Copy `ref/run-data-runner-template.ps1` to `runs/<run>.ps1`. Self-orchestrating entries.

**reg:** Copy `ref/run-ps1-reg-template.ps1` to `runs/<run>.ps1`. Self-contained runners with Resolve-StataExe + HAIPIPE_RUN_CONFIG + worker list.

For cms/case: also copy `ref/run-stage-year-template.ps1` as the orchestrator .ps1.
For data/reg: no separate orchestrator -- the runner IS the orchestrator.

Optional: create sbatch/*.ps1 multi-run batchers.


Step 7 -- Report
-----------------

    status:    ok
    summary:   Scaffolded <stage> task <NN>_<name> under {G}{NN}_<group>.
    artifacts: [paths created]
    next:      author dispatcher .do + scripts/ workers (incl. describe step); run haipipe-task-reviewer-agent before hand-copy


MUST NOT
---------

- Write heavy `.dta` files to `results/` -- they go to `_WorkSpace/{1..4}-*Store/` (exception: reg writes LIGHT .tex/.csv only).
- Skip `_meta:` block in any config YAML.
- Create `README.md` -- use `diagram/` for docs.
- Use papermill or `.ipynb` -- this is Stata + PowerShell.
- Use SSC packages in describe scripts (`egen tag` for distinct counts, NOT `distinct` which aborts r(199)).
- For reg: collapse grid runs -- one run per (window x family), collapsing is forbidden.


First-run gate
---------------

Before hand-copy to the CMS server, run `haipipe-task-reviewer-agent` on the task folder. The reviewer enforces the "Script style + server constraints" contract in `ref/stata-dialect.md` (Windows PowerShell 5.1 only, ASCII files, thin headers, no ceremony).
