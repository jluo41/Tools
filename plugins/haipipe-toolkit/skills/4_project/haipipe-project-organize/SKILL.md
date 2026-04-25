---
name: haipipe-project-organize
description: "Modify specialist for haipipe-project. Reorganizes files to fix structural violations: flatten flat tasks into groups, rename mis-numbered task folders, align Track A code with Track B examples, fix broken paired-example references. Called by /haipipe-project orchestrator only after /haipipe-project-inspect review identifies issues."
argument-hint: [function] [project_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-project-organize
================================

Modify specialist. Moves and renames files to bring a project into
structural compliance. Called by the `/haipipe-project` orchestrator
typically as a follow-up to `/haipipe-project-inspect review` flagging
violations.

  Function axis:  organize (only — purpose-built)

---

Commands
--------

```
/haipipe-project-organize                              -> ASK what to organize
/haipipe-project-organize <project_id>                 -> propose + apply fixes
/haipipe-project-organize <project_id> --dry-run       -> propose only, no writes
/haipipe-project-organize <project_id> --fix flat-tasks -> targeted fix
/haipipe-project-organize <project_id> --fix renumber  -> renumber {G}{N} tasks
/haipipe-project-organize <project_id> --fix paired    -> fix paired-example refs
```

---

Dispatch Table
--------------

```
Invocation     Ref file(s)                              Function file
-------------- ---------------------------------------- ----------------
organize       ../haipipe-project/ref/project-          fn/organize.md
               structure.md +
               ../haipipe-project/ref/code-structure.md
```

---

Step-by-Step Protocol
----------------------

Step 0: Read both umbrella ref files (project-structure.md + code-structure.md).
        Mandatory — these define the rules being enforced.

Step 1: Parse args. Required: `<project_id>`. Optional flags:
          --dry-run    print plan, do not write
          --fix <X>    targeted fix (`flat-tasks`, `renumber`, `paired`, `all`)

Step 2: Read `fn/organize.md` for the procedure.

Step 3: Verify violations exist:
          - Run a quick scan equivalent to `/haipipe-project-inspect review`.
          - If no violations, exit ok with `summary: nothing to fix`.

Step 4: Build a CHANGE PLAN: list of mv / rename / re-link operations.
        ALWAYS print the plan first. Even without `--dry-run`, the user
        sees the plan before any operation runs.

Step 5: Apply the plan ONLY after the plan has been displayed:
          - Use `git mv` when inside the repo's tracked area.
          - For paired-example reference fixes, edit imports/paths.

Step 6: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was reorganized (counts of moves / renames)
artifacts: [list of moved-from -> moved-to pairs, edited files]
next:      suggested next command (typically /haipipe-project-inspect review
           to confirm violations cleared)
```

---

Risk Profile
-------------

**This skill moves files.** Highest blast radius among the three project
specialists. Discipline:
  - `--dry-run` is supported and recommended for first invocation.
  - Plan is always printed before changes apply.
  - Use `git mv` so changes are tracked and reversible.
  - Refuse to operate if the project has uncommitted changes outside the
    target paths (avoid mixing user's work-in-progress with auto-moves).
  - On any error mid-plan, STOP — don't try to recover by guessing. Report
    what succeeded, what failed, what's left.
