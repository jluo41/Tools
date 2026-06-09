---
name: haipipe-task-for-stata-cms
description: "Stata-dialect CMS-pipeline task-folder build specialist. Scaffolds {NN}_cms_pipeline/ task-folders that extract + enrich raw CMS claims per year into _WorkSpace/1-CMS-Store (disease-agnostic, run once per year). Called by /haipipe-task orchestrator when task-type=stata-cms. Direct invocation works for scoped scaffolding. Shares the Stata engine in ../haipipe-task-for-stata/ref/stata-dialect.md."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-08"
  summary: "Stata CMS-pipeline task-folder builder."
  changelog:
    - "1.0.0 (2026-05-31): baseline."
    - "1.1.0 (2026-06-08): add metadata; workflow lifecycle compatible."
---

Skill: haipipe-task-for-stata-cms
=================================

Scaffolds a **CMS-pipeline task-folder** (Stata dialect) — extracts and
enriches raw CMS claims into per-year `Neat-*.dta` + `Bene_Info-*.dta`
panels. Disease-agnostic: processes ALL claims with no cohort filter, run
once per year, reused by every downstream study.

Engine: **Stata + PowerShell + logs** (NOT Python/papermill). The full
execution contract is `../haipipe-task-for-stata/ref/stata-dialect.md` — read it
first. This skill only scaffolds the task-folder skeleton under
`examples/`; the worker `.do` logic is authored separately.


Position in the Stata sub-family
--------------------------------

```
/haipipe-task-for-stata-cms     ◀── you are here   (1-CMS-Store, per year)
/haipipe-task-for-stata-case        cohort cases    (2-Case-Store, cohort × year)
/haipipe-task-for-stata-data        analysis table  (*-Data-Store, cross-year)
/haipipe-task-for-stata-reg         estimation      (coef tables → results/, LIGHT)
```


What this scaffolds
-------------------

```
tasks/{G}{NN}_<group>/                          ← group (project-local letter; e.g. D3, A0)
└── A{NN}_cms_pipeline/                          ← task-folder letter A = cms stage ({LNN})
    ├── A{NN}_cms_pipeline.do                    dispatcher: <config> <step> <year> <results_dir> <ws_root>
    ├── scripts/                                 worker .do per step (b-*-All.do, c-Bene-Year.do, d-Year-Summary.do)
    ├── configs/
    │   ├── cms_production.do                    Stata globals (keep-vars, flags; paths from ${ws_root}) — source of truth
    │   └── run_cms_<year>.yaml                  _meta: block + stata_config: pointer
    ├── run_cms_year.ps1                         orchestrator (~15 lines) from ../haipipe-task-for-stata/ref/run-stage-year-template.ps1 ($stata var; 4 extracts ∥ → bene_year → summary)
    ├── runs/
    │   └── run_cms_<year>.ps1                   THIN per-year entry from ../haipipe-task-for-stata/ref/run-ps1-template.ps1
    ├── sbatch/
    │   └── run_cms_<y0>-<y1>.ps1                multi-year batcher: loops the runs/ entries
    ├── results/                                 log/ · summary.txt (heavy .dta → _WorkSpace)
    └── diagram/                                 doc surface (never README.md)
```

- **RUNNAME grammar:** `run_cms_<year>`  (one identity per year, 2015..2020).
- **Steps:** `pde · carrier_claim · carrier_line · outpatient · bene_year · summary`.
- **Heavy outputs:** `_WorkSpace/1-CMS-Store/cms_full/<asset>/year-<year>/`.
- **Headline:** `Bene_Info-<year>` row × col counts.


Commands
--------

```
/haipipe-task-for-stata-cms                          ASK project / group / name
/haipipe-task-for-stata-cms <project> <group> <name>  scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md` for step-by-step. Summary: identify project+group →
collect `_meta` + year axis → create skeleton → seed `configs/<run>.yaml`
from `ref/config-seed.yaml` → copy `runs/<run>.ps1` from the Stata run
template → emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      author the dispatcher .do + scripts/ workers; run stata-script-reviewer-agent before hand-copy to the CMS server
```
