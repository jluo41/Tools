fn-task: Map Points → Tasks
============================

After all reviews are annotated (Phase A) and the master mapping exists
in A-review-content/README.md, map each rebuttal point to concrete tasks.

B-rebuttal-task/ is a MAPPING LAYER only. It does not contain task
implementations. Actual task code, scripts, and results live in the
project's tasks/ directory (e.g., `examples/{project}/tasks/`).

⛔ AND THIS SESSION DOES NOT WRITE THEM (LAW 1). The rebuttal session is a CONSUMER: it
CAUSES bank work and never AUTHORS it. Every task is DISPATCHED to
Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent) with
ONE question in general language, and the EXECUTOR scaffolds, names, runs and reports the
leaf. Nothing under `tasks/` or `discoveries/` is written from here — no README, no script,
no note, no QA file. A rebuttal id (C10, B7) inside a bank file IS the contamination.

---

Input
======

  Prerequisites:
    - A-review-content/README.md has master mapping (Point ↔ concerns)
    - A-review-content/review-{id}.md has annotated reviews with action tags
  User provides: path to review directory

---

Output
=======

  B-rebuttal-task/
  +-- README.md             <- Point → Task mapping table + status
  +-- probe-plan.md    <- Detailed plan: execution order, deps, feasibility

  Task implementations go in the project's tasks/ directory:
  tasks/
  +-- {group}/
      +-- {task_id}/        <- Code, scripts, results for one task

---

Steps
======

Step 1: Load the master mapping from Phase A
-----------------------------------------------

  Read A-review-content/README.md. It contains:
    - Reviewer scores
    - Master mapping table (Point ↔ reviewer concerns)

  Phase B does NOT re-derive the mapping — it takes the points
  and maps each one to concrete executable tasks.

Step 2: Identify tasks for each point
----------------------------------------

  For each point, determine what work is needed based on the
  action tags in the annotated reviews:

    [experiment]  → needs new model training or API calls → task in tasks/
    [analysis]    → needs computation on existing data    → task in tasks/
    [text-change] → just rewriting LaTeX source           → no task needed
    [concede]     → just honest acknowledgment            → no task needed

  Only [experiment] and [analysis] produce tasks.

Step 3: Create B-rebuttal-task/README.md
-------------------------------------------

  The README is one core table — Point → Task mapping:

    | Point | Task                               | Type       | Status |
    |-------|------------------------------------|------------|--------|
    | P1    | {task_id_1}                        | analysis   | todo   |
    | P1    | {task_id_2}                        | analysis   | todo   |
    | P1    | {task_id_3}                        | experiment | todo   |
    | P2    | {task_id_4}                        | experiment | todo   |
    | P2    | {task_id_5}                        | experiment | todo   |
    | ...   | ...                                | ...        | ...    |

  Include a note pointing to the project tasks/ directory:
    "Task implementations are in `{project}/tasks/`."

Step 4: Create probe-plan.md
------------------------------------

  The detailed plan for executing the tasks:

  **Prioritize by effort and impact:**

    Immediate (analysis, hours):
      {analysis tasks — can run on existing data/predictions}

    GPU-required (days):
      {training tasks — need GPU allocation}

    API-required (hours):
      {API tasks — e.g., LLM evaluation}

  **Execution order:**
    - Start GPU/API tasks first (longest lead time)
    - Run analysis tasks in parallel
    - Note dependencies (e.g., C11 depends on B7)

  **Feasibility assessment per task:**
    - GO: can start immediately
    - BLOCKED: depends on another task
    - NOT NOW: too much effort for rebuttal timeline

Step 5: DISPATCH each task to the executor — never author it here
----------------------------------------------------------------

  ⛔ LAW 1 — A CONSUMER SESSION NEVER WRITES A BANK FILE.

  A rebuttal session is a CONSUMER (it is the paper, mid-argument). It may CAUSE a task;
  it may never AUTHOR one. Writing `tasks/C10_eval_cohort_stratification/README.md` from
  here plants the consumer's own ids and framing (C10 / B7 are CLAIM and REBUTTAL ids) into
  the reusable bank — that is verbatim the A03 C6/C7 contamination the ONE-WRITER rule
  exists to prevent, and it makes the evidence single-use.

  So: HAND EACH TASK OVER. One call per task; batch the independent ones.

    Agent(haipipe-task-orchestrator-agent, run_in_background=true, prompt="
      action: qa
      project: <project_root>
      question: |
        <ONE question, in GENERAL language. No reviewer id. No point id. No claim id.
         No 'the reviewer asks'. No hoped-for answer. Just the question, as anyone
         in the world might ask it.>
      leaf: <an existing task-folder path, `NEW <path>`, or omit if unknown>
    ")

  …or Agent(haipipe-discovery-orchestrator-agent, ...) for literature-shaped points
  (prior art, "you missed reference X", landscape).

  THE EXECUTOR scaffolds the task-folder, names it, runs Plan → Build → Execute → Report, and
  returns a PATH to `tasks|discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md` — the answer. Record THAT
  PATH in B-rebuttal-task/README.md's Task column. The bank never learns a rebuttal exists.

  ⚠️ READ THE RETURNED QA FILE'S `- state:` LINE before quoting it (R19/R20):
    state: answered   → quote it.
    state: working    → IN PROGRESS since <started>. Do NOT re-dispatch, do NOT quote an
                        empty Answer. Mark the row `wip` and re-check.
    superseded-by: X  → follow the chain; quote X, never the stale file.

  Never edit a QA file from this session — not the body, not the state line, not once.

Step 6: Update status as tasks complete
------------------------------------------

  As tasks finish, update the Status column in B-rebuttal-task/README.md:

    todo → wip → done

  This is the single source of truth for rebuttal task progress.
