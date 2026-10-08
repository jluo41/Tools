Run skill draft · haipipe-run and haipipe-project
================================================

**Status:** applied 261006 (JL: "go and update") as haipipe-run 0.31.0 and haipipe-project 0.11.0.
The open points at the end were taken at the lean written beside each.
**From:** the Run decisions in `s01-overall-tree-structure.md` (Block → Job → Task → Run → pass).
**Feeds:** `reports/q01_bjtr_boundary/` (what a Run is), `q06_project_checker/` (what the checker
tests), `q05_skill_per_level/` (who owns what).


Part A · haipipe-run
====================

A1 · The new core (replaces "Run identity = Ticket identity = Result identity")
----------------------------------------------------------------------------

```text
Run type  →  (Run Spec)  →  Run  →  pass
              planned        one folder: runs/<run>/      one execution or one round
```

A Run is one folder in its scope's `runs/`. It is **hard** or **soft**, decided by where its
output lands:

```text
             hard                                soft
name         rNN_<slug>                          run-<type>-<target>       (no date)
ticket       rNN_<slug>.sh (or a runner .yaml)   run-<type>-<target>.md
output       only its own result/ (generated)    its scope's items: draft/ studio/ reports/ delivery/
counts as    evidence                            work, not evidence
where        a work Task only                    Block, Job or Task (a Page Task: soft only)
a new pass   a retry or rerun, same inputs       one more round on the same target
a new Run    new inputs, data, goal, or close    a new target
```

A2 · The folder
---------------

```text
runs/
├── r03_fit_baseline/                 hard
│   ├── run.yaml                      the card (written by tools only)
│   ├── r03_fit_baseline.sh           the ticket
│   ├── config.yaml                   its frozen inputs
│   ├── result/                       generated: receipt, metrics, small tables, figures, heavy.yaml
│   └── passes/
│       ├── p01-1006/                 log · runtime.yaml
│       └── p02-1007/                 a rerun
└── run-section-c2/                   soft
    ├── run.yaml
    ├── run-section-c2.md             the ticket: target, ask, close rule
    └── passes/
        └── p01-1006/                 ask · before/ · after/ of the target · ledger · touched.yaml
```

Heavy output is unchanged: `_WorkSpace/ProjectResult/<Project>/<block>/<job>/<task>/<run>/`,
pointed to by `result/heavy.yaml`.

A3 · run.yaml, the one card
---------------------------

The same fields for both kinds. Tools write it (the scaffolder, the ticket, the soft-Run
writer); nobody edits it by hand. It is the lookup card: a reader never has to open a ticket
or a receipt to list, count or show Runs.

```yaml
run: r03_fit_baseline
kind: hard                     # hard | soft
type: [fit, evaluate]          # one or more Run types; one close rule settles them all
scope: <block>/<job>/<task>    # the folder that holds this runs/
target: model-a / data-v1 / config-v1
ticket: r03_fit_baseline.sh
skill: haipipe-nn
agent: haipipe-task-creator-agent
signs: [agreed, checked]       # which signs it needs (from the workbench table)
status: done                   # planned | running | waiting | done | failed | held | superseded
passes: [p01-1006, p02-1007]
writes: [result/]              # soft: the items it touched, e.g. [draft/sections/c2.md]
feeds: [reports/q02_<topic>]   # who reads its output
```

Type tags: a hard Run may carry several (`[fit, evaluate]`) while one close rule settles it.
If two tags would need two different close rules, they are two Runs.

A4 · Every current dialect, mapped
----------------------------------

Today's catalogue has fourteen naming dialects. Under the two kinds:

```text
today                                   kind   new name
rNN_<noun>_<qualifier>        Task      hard   rNN_<slug>                    (unchanged)
rNN_<author><year>_<subject>  Discovery hard   rNN_<author><year>_<subject>  (unchanged)
run-structure-<MMDD>-<slug>   Page RP   soft   run-structure-<target>
run-scratch-/section-/paragraph-/revise-  soft   run-<kind>-<target>
rNN_page-writing_cNN-pNN      Page      soft   run-paragraph-cNN-pNN
rNN_page-run-analysis         Page      soft   run-analysis-<target>
re-<kind>-NN_<slug>           Page RE   soft   run-value- · run-display- · run-cite-<target>
rNN_page-display_…            display   soft   run-display-<fig>
rdNN_<target>, run-delivery-<lane>      soft   run-delivery-<lane>
<instance>#riNN_<slug>@vNNN   Insight   hard   <dataset>_<partition>  (vNNN → passes) ?
rdNN_commission_<slug>        Design    soft   run-commission-<target>
rdNN_generate_ · rdNN_verify_ Design    hard   rNN_generate_<slug> · rNN_verify_<slug>
ridea- rclaim- rtask- rnarra- Paper     soft   run-idea- · run-claim- · run-task- · run-narrative-<target>
rNN_compile-<slug>            Paper     soft   run-delivery-latex
rresponse-NN_<batch>          Paper     soft   run-response-<batch>
rlNN_<operation>_<target>     Labeling  hard   rNN_<operation>_<target> ?
```

A5 · What changes in the skill text
-----------------------------------

1. `SKILL.md` opening: the identity line becomes the folder line in A1; add the hard/soft
   table; "attempts" and "Versions" become passes.
2. "Choose the next action": the row "an independent later Section session allocates the next
   `run-section-<MMDD>-<slug>`" becomes "the same Section = the same Run, a new pass".
3. "Result, evidence, and closure": evidence = hard Results only; a Page reads them and
   computes no new facts; Page evidence Runs are soft.
4. `ref/identity-and-history.md`: the dialect table (six storage shapes) becomes one shape,
   `runs/<run>/`; the old shapes stay readable until the move (Part B) has run.
5. `ref/receipts-and-inventory.md`: inventory reads `run.yaml`; `runtime.yaml` stays the
   receipt of one pass (`passes/pNN-<MMDD>/runtime.yaml`); a hard `result/` keeps its receipt.
6. `ref/run-catalog.md`: the table in A4 replaces the naming column.

Then, in this order, the owners follow: `haipipe-task` (the Task folder, `runs/<run>/`, the
ticket template writing `result/` and `passes/`), `haipipe-page` (Page Runs soft;
`displays/<fig>/recipe/ · assets/`), and each family's run naming (paper, design, insight,
labeling).


Part B · haipipe-project audit and update, at every level
=========================================================

B1 · Today
----------

`/haipipe-project audit` checks only a Project's root (README, project.yaml, allowed worlds)
and CoWork Blocks. It stops there on purpose: "route any deeper request to the child-world
owner". `update` adds a missing manifest or README and records the rest as migration debt.

B2 · Proposed
-------------

Point it at any folder; it finds the level from the name and checks that level and everything
below it against the ladder.

```text
/haipipe-project audit  <path> [--only] [--format markdown]
/haipipe-project update <path> [--apply]          dry run unless --apply

<path> = a Project · a Block bNN_<topic>/ · a Job jNN_<job>/ · a Task tNN_<task>/ · a Run runs/<run>/
--only = this level alone, not its children
```

The level comes from the name: `bNN_` Block, `jNN_` Job, `tNN_` Task, a folder inside `runs/`
a Run. One table, `ref/ladder.md`, lists each level's face, its allowed specials and its
children; the script reads it, and the s01 drawing can be built from the same table.

```text
level    face               may hold                                       children
Block    bNN_<topic>.md     studio/ reports/ delivery/ resources           jNN_<job>/
Job      jNN_<job>.md       studio/ reports/ delivery/ src/ sbatch/ runs/  tNN_<task>/
Task     tNN_<task>.md      studio/ reports/ delivery/ scripts/ displays/  runs/<run>/
Run      run.yaml           ticket · config.yaml · result/ · passes/       pNN-<MMDD>/
```

A family adds its variant's extras in its own skill (labeling `labeling/`, insight `meta/`,
paper Sections); the checker reads them through the Block's `workbench:` field. So
haipipe-project checks the **shape** at every level, and each domain skill still owns the
**content** (a Page's sections, a ticket's body).

B3 · What audit reports
-----------------------

```text
b03_project_workbench/                  debt   face is board.md (→ bNN_<topic>.md)
└── j02_fit/                  ok
    └── t01_baseline/         debt   2 Runs in the old layout (runs/*.sh + results/)
        └── runs/r03_fit/     failed hard Run with no result/ but status: done
```

Per level: the face name, unknown folders, a child with the wrong prefix, hard Runs outside a
work Task, a hard Run in a Page Task, a soft Run name with a date, a Run with no `run.yaml`,
`run.yaml` disagreeing with the ticket or the receipt, a hard Run writing outside `result/`,
an absolute path (AGENTS.md rule 7), a heavy file inside `result/` (rule 10).

B4 · What update may fix
------------------------

Safe, at any level, after a dry run that prints every move:

1. Write a missing or stale `run.yaml` from the ticket and the receipt (update is one of the
   tools allowed to write it).
2. The one-time move: `runs/<run>.sh` + `results/<run>/` → `runs/<run>/` with the ticket,
   `result/` and a first pass. Whole folders move unchanged; nothing inside a Result is edited.
3. A soft Run's dated name → `run-<type>-<target>`, its date moved into `passes/p01-<MMDD>/`.
4. A Block face `board.md` → `bNN_<topic>.md` (once JL settles that question).

Never: edit a file inside `result/`, move a submodule, or move anything under `_legacy/` or
`_old/`. Scale today: about 740 `runs/` folders and 2,800 tickets across `examples-1` to `-6`,
so the move goes one Block at a time, each checked by a rerun of audit.


Open points, and what was taken
-------------------------------

1. Insight: its Runs `<dataset>_<partition>` with `vNNN` as passes, or rNN names?
   Taken: `<dataset>_<partition>`, vNNN as passes, marked proposed until insight settles.
2. Labeling: `rlNN_` becomes `rNN_`, or keeps its prefix? Taken: keeps `rlNN_` (its owner).
3. A Job's own `runs/`: soft only. Do `src/` + `sbatch/` jobs launched from a Job count as
   Runs of the Job, or of the Task they serve? Taken: the Task they serve.
4. A moved Result's receipt still names its old path. Taken: keep it as history; `run.yaml`
   records `moved_from:` (rule 0: never edit it).
5. A Task whose Results live in an outside store. Taken: the store mirrors
   `<store>/<task>/runs/<run>/result/` and `run.yaml` names it.
