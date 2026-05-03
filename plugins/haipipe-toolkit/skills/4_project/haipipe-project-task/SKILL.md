---
name: haipipe-project-task
description: "Build specialist for haipipe-project. Scaffolds projects, task-groups, and task-folders under examples/ using the project → task-group → task-folder hierarchy with task-type awareness (model-run / evaluation / display / data-pipeline). Replaces the older -new specialist with task-centric vocabulary. Called by /haipipe-project orchestrator. Direct invocation works for scaffold work."
argument-hint: [scope] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-project-task
=============================

Build specialist organized around the **task hierarchy**:

```
project           examples/Proj{...}/
  └── task-group  tasks/{G}{NN}_{name}/
        └── task-folder  {NN}_{name}/{*.py, configs/, runs/, results/, notebooks/}
```

Each task-folder is one of these **task-types**:

```
model-run     trains a model              (Stage 5; A-series groups)
evaluation    scores a trained model      (B-series groups)
display       paper figures / tables      (C-series groups)
data-pipeline runs a Stage 1-4 builder    (typically D_demo or in-project)
other         free-form / utility
```

Called by `/haipipe-project` when the request is to **create** something
in the hierarchy. For audit / read see `-inspect`; for moves see `-organize`.

---

Commands
--------

```
/haipipe-project task                    -> ASK which scope
/haipipe-project task project [id]       -> scaffold a new project
/haipipe-project task task-group         -> scaffold a new task-group
/haipipe-project task task-folder        -> scaffold a new task-folder (asks task-type)
```

Shorthand: `/haipipe-project task` with no scope and no args defaults to
`task-folder` (most common ask).

---

Dispatch Table
--------------

```
Scope            Ref                                       Function file
---------------- ----------------------------------------- ----------------------
project          ref/hierarchy.md                          fn/project.md
                 ../haipipe-project/ref/project-structure.md
                 ../haipipe-project/ref/code-structure.md
task-group       ref/hierarchy.md                          fn/task-group.md
                 ../haipipe-project/ref/project-structure.md
task-folder      ref/hierarchy.md                          fn/task-folder.md
                 ../haipipe-project/ref/project-structure.md
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/hierarchy.md` first. It's the conceptual model.
        Then read `../haipipe-project/ref/project-structure.md`.
        For scope=project, also read `../haipipe-project/ref/code-structure.md`.

Step 1: Parse args. Resolve scope:
          - explicit token (`project` / `task-group` / `task-folder`) → done
          - missing → ASK
          - shorthand: no args at all → default to `task-folder`

Step 2: Read the matching `fn/*.md` for the scaffold procedure.

Step 3: Execute. Follow the function file step-by-step. ASK for any
        metadata not provided.

Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command
```

---

Risk Profile
-------------

CREATES files under `examples/{PROJECT_ID}/`. For scope=project with
new code stubs, also creates files under `code-dev/` and `code/hainn/`.
Refuse to overwrite existing names — abort and recommend `-organize`.
