fn-task: Map Points → Tasks
============================

After all reviews are annotated (Phase A) and the master mapping exists
in A-review-content/README.md, map each rebuttal point to concrete tasks.

B-rebuttal-task/ is a MAPPING LAYER only. It does not contain task
implementations. Actual task code, scripts, and results live in the
project's tasks/ directory (e.g., `examples/{project}/tasks/`).

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
  +-- experiment-plan.md    <- Detailed plan: execution order, deps, feasibility

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

Step 4: Create experiment-plan.md
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

Step 5: Create task folders in the project's tasks/ directory
----------------------------------------------------------------

  For each new task, create a folder in the project's tasks/ directory.
  Follow the project's task naming convention (e.g., A2_data_event_alignment,
  B7_train_fairness_aware, C10_eval_cohort_stratification).

  Each task folder should contain:
    - README.md: what this task does, inputs, outputs
    - Scripts/notebooks to run the task
    - Results (or symlinks to results)

  Use the /haipipe-project skill if available for task folder structure.

Step 6: Update status as tasks complete
------------------------------------------

  As tasks finish, update the Status column in B-rebuttal-task/README.md:

    todo → wip → done

  This is the single source of truth for rebuttal task progress.
