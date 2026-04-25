---
name: haipipe-project-new
description: "Build specialist for haipipe-project. Scaffolds a new project under examples/ with the two-track structure (Track A code stubs in code-dev/hainn/haifn; Track B examples/{PROJECT_ID}/ with tasks/{group}/{task}/, configs, runs, results, paper). Called by /haipipe-project orchestrator. Direct invocation works for project scaffold work."
argument-hint: [project_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-project-new
===========================

Build specialist. Scaffolds a brand-new project across both tracks:

```
Track B  ->  examples/{PROJECT_ID}/  (tasks, configs, runs, results, paper)
Track A  ->  code-dev/ + code/hainn/ + code/haifn/  (Fn builders, ML model stubs)
```

Called by the `/haipipe-project` orchestrator when the request is to
**create** a new project. For audit / read / reorganize, see the
`-inspect` and `-organize` siblings.

  Function axis:  new (only — this skill is purpose-built)

---

Commands
--------

```
/haipipe-project-new                            -> ASK for project_id
/haipipe-project-new <project_id>               -> scaffold the project
/haipipe-project-new <project_id> --task A_data -> scaffold + add a starter task group
```

---

Dispatch Table
--------------

```
Invocation                Ref file(s)                          Function file
------------------------- ------------------------------------ ----------------
new (with project_id)     ../haipipe-project/ref/project-      fn/new.md
                          structure.md +
                          ../haipipe-project/ref/code-
                          structure.md
```

---

Step-by-Step Protocol
----------------------

Step 0: Read both umbrella ref files first:
          - `../haipipe-project/ref/project-structure.md`  (Track B layout)
          - `../haipipe-project/ref/code-structure.md`     (Track A layout)
        Mandatory.

Step 1: Parse args. Must have `<project_id>` (e.g. `cgm-forecast-v1`).
        If missing -> ASK for it.

Step 2: Read `fn/new.md` for the scaffold procedure.

Step 3: Verify two-level task hierarchy rule (umbrella ref):
          - Tasks live inside group folders: `{G}_{group_name}/`.
          - Each group contains `{G}{N}_{task_name}/` task folders.
          - No flat tasks directly in `tasks/`.

Step 4: Verify code-paired-example rule (umbrella ref):
          Every Track A code stub must auto-generate a paired example
          task in Track B `tasks/`.

Step 5: Execute the scaffold per `fn/new.md`. Touches both tracks.

Step 6: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded (paths created)
artifacts: [project_root, list of created files/dirs]
next:      suggested next command (often /haipipe-project-inspect review)
```

---

Risk Profile
-------------

This skill **creates** files in two locations:
  - `examples/{PROJECT_ID}/`
  - `code-dev/`, `code/hainn/`, `code/haifn/` stubs

Allowed-tools includes Write/Edit; blast radius is bounded to NEW directories.
Refuse to overwrite existing project IDs — abort and recommend
`/haipipe-project-organize` instead.
