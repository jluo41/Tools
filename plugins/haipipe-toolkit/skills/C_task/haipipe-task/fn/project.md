fn-project: Scaffold a New Project
====================================

Output: `examples/{PROJECT_ID}/{tasks/, diagram/, paper/ (optional)}`.
Forbidden at top level: README.md, docs/, cc-archive/, _old/, configs/, results/.

A project is the outer container. It holds task-groups (Level 2), which
hold task-folders (Level 3). See `ref/hierarchy.md`.


Step 1 — Collect metadata (ASK, wait for confirmation)
-------------------------------------------------------

  Identity
    Series letter / Category / Num / CamelCase Name
    → compose PROJECT_ID = `Proj{Series}-{Category}-{Num}-{Name}`

  Scope
    Pipeline stages used (1-6)
    Dataset(s)
    Q7: new pipeline Fn needed?           (yes/no)
    Q8: new ML model needed?              (yes/no)

  Story (for diagram/)
    Research question
    Why it matters
    In-scope (3-5 bullets)
    Out-of-scope (2-3 bullets)
    Initial exploration directions (2-4 bullets)


Step 2 — Create skeleton
-------------------------

```
examples/{PROJECT_ID}/
├── tasks/
├── diagram/
└── paper/Paper-{Name}-{venue}/    (optional)
```


Step 3 — Author project diagram/ via /diagram-ascii
----------------------------------------------------

One call per file. Never write .txt content inline.

```
01-story.txt        Research question / Why it matters / At a glance
02-boundary.txt     In scope / Out of scope / Definitions / Assumptions
03-exploration.txt  Active / Backlog / Tried / Ruled out
                    (seed Active+Backlog from initial directions)
```

Then bundle:
```
/diagram-ascii-canvas {PROJECT}/diagram/  →  project.excalidraw
```


Step 4 — Create first task-group + first task-folder
-----------------------------------------------------

Reuse metadata. Invoke:
  - `fn/task-group.md` (Scope 2)
  - `fn/task-folder.md` (Scope 3)

By default, seed with a task-group matching the dominant task-type
of the project (e.g. model-run → `A01_pretraining_*`).


Step 5 — Track A code stubs (skip if Q7 = Q8 = NO)
---------------------------------------------------

  Q7 YES:
    Create `code-dev/1-PIPELINE/{N}-*-WorkSpace/build_{dataset}_{layer}.py`
    + paired demo task `tasks/D_demo/{NN}_test_{...}/`.
    Check `code/INDEX.md` for existing match before creating.

  Q8 YES:
    Create stubs in `code/hainn/{algo,tuner,instance}/{family}/`
    + paired demo task `tasks/D_demo/{NN}_test_{name}_model/`.
    Add row to `code/INDEX.md`.
    Append a Backlog entry to project's `03-exploration.txt`
    (re-bundle the canvas).


Step 6 — Report
----------------

Print:
  - Track B files created (paths)
  - Diagram files + canvas
  - Track A stubs (if any)
  - Suggested next: `/haipipe-project task task-group` to add another group,
    or `/haipipe-project task task-folder` to add a task within the seed group.
