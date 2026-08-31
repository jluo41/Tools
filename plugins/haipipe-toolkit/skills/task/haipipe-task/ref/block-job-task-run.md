task: Block / Job / Task / Run — the settled naming
=====================================================

Settled with JL on 2026-08-29, and ABSORBED the same day (v0.8.0) into
ref/hierarchy.md, ref/task-structure.md, SKILL.md and ref/run-sh-template.sh —
those are now the authority; this file remains as the settlement record.

Still carrying the old names (next sweep): fn/*.md and the type specialists in
this family, plus the other skill families (~84 non-diagram prose mentions per the 260829 boundary review; diagrams/ snapshots hold ~1300 more). The PowerShell
store-resolution gap (§ Code that must change) is still open.

---

The four words
==============

Named against Databricks, because these repos deploy there and a word that
means two things in one workspace is a defect.

  BLOCK   one large topic                    tasks/b02_llm_recommendation_runs/
          no Databricks equivalent. Airflow has no word, dbt says "project",
          Databricks Asset Bundles says "bundle". The name is therefore FREE.

  JOB     self-contained, submittable        j01_A1_search_physicians/
          = Databricks Job. THE unit of self-containment. Only a Job can be
          scheduled. A job never reaches into a sibling job.

  TASK    one script pipeline = one PAGE     t01_claude_agent_sdk/
          = Databricks Task. task_key is unique WITHIN the job, not globally.
          SELF-CONTAINED (260830): its code, config/, runs/ and its page
          t01_….md sit together. It resolves the job's shared code at ../src/.

  RUN     one submission of one task         config/r03_fold00_opus.yaml
          = Databricks Run. An EXECUTION, not a variant and not a directory
          of its own. What distinguishes two runs is which config the ticket
          named, plus when it was sent.

  ONE GRAMMAR at every level (JL 260829): <level letter><NN>_<noun>_<qualifier>
  — b · j · t · r, two digits, then words that pass the stranger test. No
  letter schemes, no bare letters, no exceptions; a family of parallel blocks
  shows the family in its NAME (b05_reg_trait_opioid · b06_reg_trait_cabg).

---

The shape
=========

  tasks/
  └── b07_reg_trait_cabg/                     BLOCK   (was R03_Reg_TraitCABG)
      └── j02_reg_visitami_leftdigit/         JOB     (was D01-reg_visitami_leftdigit)
          ├── sbatch/run_job_dag.ps1                submit the whole DAG (spans tasks)
          ├── src/                                  shared inside this job
          │   ├── config-defaults.do                job-wide defaults + `store:`
          │   └── lib-*.do
          └── t01_reg_..._lifedigits/         TASK  open THIS to debug
          │       ├── config/                       ALWAYS a folder
          │       │   ├── r01_base.do               rNN = the run's identity, stem = its description
          │       │   └── r02_wide.do
          │       ├── run-pipeline.do
          │       └── step-01..step-10.do
          ├── runs/                                 TICKETS, carry NO params
          │   └── t01_reg_..._lifedigits/           folder name IDENTICAL to scripts/
          │       ├── r01_base.ps1
          │       └── r02_wide.ps1
          ├── results/                              JOB level, two levels deep
          │   └── 01_reg_..._lifedigits/
          │       ├── base/
          │       └── wide/
          └── workflow/

One shape, `<task>/<run>`, repeated in three folders: scripts/ (as config/),
runs/, results/. A run is therefore a PATH, never an invented joined string
like `run_diabetes-dpp4`. The `-` vs `__` separator question does not arise.


---

Addressing (p:bjtr)
===================

One execution has one address, READ OFF THE PATH, never counted from `ls`
(a counted position rots on insertion; a written NN never does):

```
  llmrec:b02j01t01r03
    p      project slug — only across projects; inside a repo, drop it
    b02    the block folder's prefix      tasks/b02_llm_recommendation_runs/
    j01    the job folder's prefix        j01_A1_search_physicians/
    t01    the task folder's prefix       t01_claude_agent_sdk/
    r03    the config file's prefix       config/r03_fold00_opus.yaml
```

The address IS the path: four prefixes, joined. Nothing is computed, mapped
or ranked (JL 260829 rejected b1-as-rank, bA, and bare letters in turn); `ls`
shows the address, and renaming a stem (`fold00_opus` → clearer words) never
breaks a citation, because the number is the identity. Two spellings:
COMPACT `b02j01t01r03` for chat, commits, board citations and grep
(uniquely an address, never a word); READABLE `b02.j01.t01.r03` for file
headers and runtime.yaml. Partial addresses are legal because every segment
is tagged (`j01t01`, `t01r03`); bare numbers (`2.1.1.3`) are not. The ticket stamps both forms into runtime.yaml
(run-sh-template.sh § address).

---

Rules
=====

R1  ⚠️ HIGHEST PRIORITY (JL 260829) — A NAME PASSES THE STRANGER TEST: <noun>_<qualifier>, where the noun is the
    concrete thing (physicians, rankings) and the qualifier says which one
    (from_search_engines, by_region_specialty). Shape words (pool, rank,
    baseline, data, analysis) never stand alone. Full rule: hierarchy.md
    "Naming: the stranger test". Scaffolds refuse names that fail it.

R2  CONFIG LIVES IN THE TASK, ALWAYS AS A FOLDER. PROMPTS ARE CONFIG: a prompt
    file sits in config/prompts/ beside the config that names it, and code
    resolves it relative to that config file (JL 260830). CODE SEVERAL JOBS
    IMPORT IS A LIBRARY in code/haiutils/ (the SPACE package), never in a
    project, block or sibling job.
    A config.do is EXECUTED by Stata, not passed in as a payload, so it is
    debugged in the same interactive session as the steps beside it. Always a
    folder even when it holds one file, so no reader ever has to stat the path
    to learn the rule.

R3  A TICKET CARRIES NO PARAMETERS.
    <task>/runs/<run>.ps1 names a config and submits. It must not define a
    parameter of its own, and it must not repeat its own name: derive the task
    from $PSScriptRoot. Today runs/run_reg_visitami_any_15_24_lifedigits.ps1
    writes that name THREE times (filename, arg 1, arg 2); renaming the task
    breaks two of them silently.

R4  A VARIANT IS A CONFIG, NOT A NEW TICKET SCHEME.
    Two runs of one task differ only by config stem. Two DIFFERENT pipelines
    are two task folders.

R5  UNDER A JOB, `tNN_*` IS EXACTLY ONE TASK AND EVERYTHING ELSE IS NOT.
    Shared material lives in `src/`, one name for every engine (`0-libs/` is read
    but never written — hierarchy.md "The 0-libs exemption"); the reserved
    siblings are `sbatch/ results/ notebooks/ QA/ workflow/ diagram/`. Loose
    files currently use a competing `_` prefix (_lib-describe.do,
    _load-raw-standard.do, _resolve-raw-dir.do) — unify those into `src/`.

R6  ZERO-PAD THE INDEX TO TWO DIGITS.
    Single digits sort wrong: 10_data_VisitOsteo currently sorts BEFORE
    1_data_VisitAMI and before 2_data_VisitLBP.

R7  `store:` IS A JOB PROPERTY, DECLARED ONCE IN src/.
    Never per-run. The moment two runs of one job land in two places,
    `ls results/*/*/` stops being the job's output inventory, which is the
    whole reason results sits at job level. Mirrors the Databricks rule: a Job
    has ONE git source and ONE set of job_clusters; tasks reference, never
    redefine.

R8  OUTPUT IS RESOLVED, NEVER HARDCODED. Precedence, unchanged from
    run-sh-template.sh:59 —
        RESULT_STORE env var   one caller overriding one run     WINS
        config `store:` key    a standing declaration
        neither                task-local                        default
    Mode (2) mirrors the tasks/ path under the store, so store and repo map
    1:1 both ways and <task>/<run> survives the move untouched.

---

Drift checks
============

Every link in this shape is a folder name, so every link is checkable:

  # every task has tickets, every ticket has a task
  comm -3 <(ls runs/) <(ls scripts/ | grep -v '^0-')

  # every config has a ticket, every ticket has a config
  comm -3 <(find scripts -path "*/config/*" -type f \
              | sed "s|^scripts/||; s|/config/|/|; s|\.[^./]*$||" | sort) \
          <(find runs -type f | sed "s|^runs/||; s|\.[^./]*$||" | sort)

  left column  = a config with no ticket        01_reg_lifedigits/wide
  right column = a ticket with no config    <tab>02_reg_falsification/rogue

Both must print nothing. (Verified 2026-08-29 on a mock job: silent when
paired, and each direction reported when broken. Do NOT use `ls scripts/*/config/`
here — with more than one match ls emits `dir:` headers and blank lines that
pollute the comparison.) Under the old flat naming neither check was
possible, which is why 42 folders in examples/ silently drifted configs/
against runs/ — e.g. A00_External_Data/B01_explore_ndc has 17 configs and 18
tickets, and nobody noticed that run_hypertension-umbrella.sh and
run_show_final_ndc.sh have no config at all.

---

Code that must change
=====================

DONE 260829 (v0.8.0): ref/run-sh-template.sh resolves both shapes — nested
CONFIG <task>/config/<run>.yaml and two-level
RESULTS_DIR=$OUTPUT_ROOT/results/<task>/<run>, verified on a mock repo.

STILL OPEN:

  0-libs/run-regression-pipeline.ps1:11   $RESULTS = Join-Path $TASK_DIR "results\$RunName"
  0-libs/run-data-pipeline.ps1:22         same
                              -> resolve a store first, then two levels.

GAP, and it is the side holding PHI: the PowerShell runners have NO store
resolution, NO split-bank guard, and no equivalent of the bash suite's
test_run_template_resolves_rather_than_hardcodes — they do exactly what that
test forbids. R01/R02/R03 are CMS regression jobs whose results legally must
not sit in a git-tracked folder, and mode (2) is currently unavailable to them.

### R9. A job audits itself; order between jobs is a receipt (JL 260830)

No orchestration-only job. The LLMRec block had `j05_audit_ladder`, a job
whose only work was to run j01 → j02 → j03 for one model and stamp one
campaign receipt; JL: "I don't understand this job name" → "why not split
them into each job, so the job folder will be self-contained" → "no more
j05". Ruling: every run ticket ends with `audit_<stage>_outputs.py
--config <its own yaml> --write-receipt`; the receipt MIRRORS the run dir
(`audits/<scale>/<stage folder>/<model folder>/<run name>/audit_receipt.json`),
so two campaigns of one model never share one; a downstream config's
`required_audits` names the exact upstream RUN (path + stage + scale +
provider + model), and `validate_required_audits` refuses to start without
it. Cross-job batch loops live in each job's own `sbatch/run_all_arms.sh`,
which submits only that job's tickets. Shared audit checks are a library:
`code/haiutils/agent_sdk/audit.py`.
