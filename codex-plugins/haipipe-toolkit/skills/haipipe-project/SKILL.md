---
name: haipipe-project
description: "Run any project-level work in the haipipe workspace. Parses intent (build vs read vs modify) and dispatches to the right specialist (/haipipe-task for scaffolding tasks under examples/, /haipipe-project-inspect for review/summary/inventory/overview, /haipipe-project-organize for reorganizing files). Use for creating new projects/task-groups/task-folders (data / algo / training / eval / display / individual / agent) under examples/, auditing structure, generating docs, reorganizing. Trigger: project scaffold, new task, new figure task, new evaluation task, project review, project summary, organize project, reorganize files, /haipipe-project."
argument-hint: "[function] [project_id] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Run any project-level work in the haipipe workspace."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-project (orchestrator)
======================================

User-facing entry for project-level work. Routes by **risk profile** (build / read / modify) — the three specialists differ in `allowed-tools` and blast radius.

```
/haipipe-project                                          overview of all projects under examples/
/haipipe-project task                                     scaffold (asks: project / task-group / task-folder)
/haipipe-project task project <project_id>                scaffold a new project
/haipipe-project task task-group                          scaffold a new task-group
/haipipe-project task task-folder                         scaffold a new task-folder (asks task-type, dispatches)
/haipipe-project task task-folder <type> [args...]        scaffold task-folder of given task-type directly:
                                                            type ∈ {data, algo, training, eval,
                                                                    display, individual, agent}
/haipipe-project task run [task-path] [name]              scaffold a new run (asks _meta)
/haipipe-project review <project_id>                      structural audit
/haipipe-project summarize <project_id>                   generate summary doc
/haipipe-project inventory [project_id]                   file inventory
/haipipe-project overview [project_id]                    overview of one or all projects
/haipipe-project organize <project_id>                    reorganize files (modifies!)
/haipipe-project scan-status <task_dir> [key] [out_txt]   scan B01 eval, update status.json + txt
/haipipe-project "<natural language>"                     infer function, dispatch
```

---

Specialists
-----------

```
Lives in project/  (project-scope work):

  haipipe-project-inspect    READ:   review, summarize, inventory, overview (no writes)
  haipipe-project-organize   MODIFY: reorganize files (mv/rename, dry-run supported)

Lives in task/  (task-scope work — sibling section):

  haipipe-task               BUILD orchestrator: task-folder lifecycle + run scaffold +
                                     task-folder dispatch to the 7 type specialists below.
  haipipe-task-for-data          data-pipeline (Stage 1-4)           D-series  → /haipipe-data
  haipipe-task-for-algo          algo-dev smoke-test                 X_algo    → /haipipe-nn-algo
  haipipe-task-for-training      model training (Stage 5)            A-series  → /haipipe-nn-tuner+instance
  haipipe-task-for-eval          evaluation                          B-series  → (project-local; future)
  haipipe-task-for-display       paper figures / tables              C-series  → (independent)
  haipipe-task-for-individual    individual-centric query               E-series  → /haipipe-individual
  haipipe-task-for-agent         LLM agent call                      F-series  → (none yet)

(Per-run logging is automatic via runs/<NAME>.sh → results/<NAME>/runtime.yaml.
 For probe-level claims + aggregation, see probe/* skills.)
```

Conceptual layering — a `project` is the umbrella, containing five parallel worlds. Each world has its own specialist family:

```
📦 project (umbrella)            /haipipe-project              ← this skill
   │
   ├── 💼 tasks/                  /haipipe-task-*               (task/)
   │       "did THIS run work?"   — code + runs + per-run metrics
   │
   ├── 📊 probes/            /haipipe-probe           (probe/)
   │       "does the HYPOTHESIS   — steering state; NO code, only
   │        hold?"                  arms[] pointers into tasks/
   │
   ├── 💡 insights/               /haipipe-insight              (insight/)
   │       "what does the         — cross-probe synthesis
   │        PROJECT know?"          D/I/K/W markdown layers
   │
   ├── 📰 paper/                   /paper-*                     (separate section)
   │       "what claims ship      — consumes K/W from insights/
   │        to academia?"
   │
   └── 📬 applications/           /haipipe-application-*         (application/)
           "what do we deliver    — patient/clinician messages,
            to non-academic         UI sketches, stakeholder reports;
            audiences?"            reads insights/K + W (NEVER writes back);
                                   can TRIGGER /haipipe-insight ask to
                                   close knowledge gaps mid-draft
```

**For the boundary between task and probe** (the most-confused pair, since both touch results/), see `probe/MENTAL_MODEL.md` — onboarding doc with FAQ + "rules of thumb" + walkthrough of one probe's full lifecycle.

---

Two Structural Rules (cross-cutting; ref'd by all specialists)
---------------------------------------------------------------

Rule 1 — Three-level hierarchy (project → task-group → task-folder):
  `examples/{PROJECT_ID}/tasks/` contains task-groups: `{G}{NN}_{group_name}/`
    (e.g., `A01_pretraining_clm/`, `B01_evaluation_clm/`, `C01_paper_figures/`).
  Each task-group contains task-folders: `{NN}_{task_name}/`
    (e.g., `01_train_clm_num_modelsize/` inside `A01_pretraining_clm/`).
  Each task-folder is self-contained: `*.py`, `configs/`, `runs/`, `results/`,
    `notebooks/` (NO README.md — doc surface is `diagram/`).
  No flat task folders directly in `tasks/` — they must be inside a task-group.
  Group letter convention: A=training (model-run), B=evaluation, C=display,
                           D=data-pipeline, E=individual, F=agent, X=algo-dev (X_algo).

Rule 2 — Code always has a paired example:
  Every new pipeline Fn stub or ML model stub in Track A auto-generates
  a paired example task in `tasks/`.

These rules live in `ref/project-structure.md` and `ref/code-structure.md`,
which all three specialists read.

---

Function Verb Map
------------------

```
project, new project, scaffold project        -> this skill, fn/project.md (project-scope)
task-group, new group, scaffold group         -> this skill, fn/task-group.md (project-scope)
task, task-folder, new task, scaffold task     -> haipipe-task (task/) — task-folder + below only
  (for scope=task-folder, -task dispatches to one of:
     haipipe-task-{data,algo,training,eval,display,individual,agent})
run, new run                                  -> haipipe-task (task/) — run scaffold
review, audit, check, validate, lint          -> haipipe-project-inspect (review)
summarize, summary, docs                      -> haipipe-project-inspect (summarize)
inventory, list files, files                  -> haipipe-project-inspect (inventory)
overview, show, status                        -> haipipe-project-inspect (overview)
organize, reorganize, fix structure, move     -> haipipe-project-organize
scan-status, scan eval, eval status           -> haipipe-project-inspect (scan-status)

(claims / probes / comparison: → /haipipe-probe under probe/)
```

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve function via verb map.
  - If verb is unambiguous -> done.
  - If first positional looks like a project_id (matches an existing
    examples/{X}/) and no verb -> default to overview for that project.
  - If no args at all -> overview across ALL projects (umbrella inline).

Step 3: Decide specialist:
  - project / task-group scaffold        -> this skill (fn/project.md, fn/task-group.md)
  - task-folder / run scaffold           -> haipipe-task (in task/)
  - review/summarize/inventory/overview  -> haipipe-project-inspect
  - organize                             -> haipipe-project-organize

Step 4: Dispatch:
    Skill("haipipe-project-<specialist>", args="<verb> <remaining_args>")

Step 5: Capture the structured tail and present.
```

---

Cross-Project Overview (no-arg case)
-------------------------------------

When invoked with no arguments, list all projects under `examples/` with
a one-line status per project (task count, last-modified, violations
flagged). Inline (no specialist dispatch needed for this lightweight view).

---

Disambiguation Rules
---------------------

  - Verb missing, project_id present -> default to `overview` for that id.
  - Verb missing, no args            -> cross-project overview (inline).
  - `organize` without project_id    -> ASK which project. Don't guess.
  - Multi-project ops (e.g. "review all") -> dispatch sequentially per project.

---

Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths created / read / moved]
next:      suggested next command
```

---

Files Owned by This Umbrella
-----------------------------

```
ref/project-structure.md   Track B layout (tasks/, configs/, runs/, results/, paper)
ref/code-structure.md      Track A layout (code-dev/, hainn/, haifn/) + paired-example rule
```

These ref files are SHARED across specialists. Each specialist reads them when its function depends on the rules. The inventory helper scripts (`ref/inventory/*.py`) live with `haipipe-project-inspect` since only that specialist uses them.

---

## Feedback

`/haipipe-project feedback "<text>"` captures a complaint / confusion / wish about THIS
skill into `feedback/` (one dated file per item, `status: open`) to fix in a
later revision pass. `/haipipe-project feedback list` shows the open items. This is
feedback about the tool, not the work it produces. Route a `feedback` first-token
here before other parsing. Full convention: `feedback/README.md`.
