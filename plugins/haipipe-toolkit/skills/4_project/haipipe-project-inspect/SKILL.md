---
name: haipipe-project-inspect
description: "Read-only specialist for haipipe-project. Reviews project structure, summarizes, generates inventory, prints overview. Touches no files. Called by /haipipe-project orchestrator. Direct invocation works for project audit work."
argument-hint: [function] [project_id_or_path] [args...]
allowed-tools: Read, Grep, Glob, Bash
---

Skill: haipipe-project-inspect
===============================

Read-only specialist. Reviews, summarizes, inventories, and overviews
project state without modifying anything. Called by the `/haipipe-project`
orchestrator; can also be invoked directly.

  Function axis:  review | summarize | inventory | overview

---

Commands
--------

```
/haipipe-project-inspect                        -> overview of all examples/
/haipipe-project-inspect overview [project_id]  -> overview of one project (or all)
/haipipe-project-inspect review <project_id>    -> structural audit (group/task rules)
/haipipe-project-inspect summarize <project_id> -> generate summary doc
/haipipe-project-inspect inventory [project_id] -> file inventory (uses ref/inventory/*.py)
```

---

Dispatch Table
--------------

```
Invocation     Ref file(s)                              Function file
-------------- ---------------------------------------- ----------------
overview       ../haipipe-project/ref/project-          fn/overview.md
               structure.md
review         ../haipipe-project/ref/project-          fn/review.md
               structure.md +
               ../haipipe-project/ref/code-structure.md
summarize      ../haipipe-project/ref/project-          fn/summarize.md
               structure.md
inventory      ref/inventory/*.py                       fn/inventory.md
```

---

Step-by-Step Protocol
----------------------

Step 0: Read the relevant umbrella ref(s) per the dispatch table.

Step 1: Parse args.
          function in { overview, review, summarize, inventory, (none) }
          target   = project_id or path; default = scan all of examples/

Step 2: Read this skill's relevant fn doc.

Step 3: For `inventory`, use the helper scripts under `ref/inventory/`:
          - `helpers.py` — building blocks
          - `refresh_all.py` — full repo scan
          - `render.py` — output formatter

Step 4: Execute the function. NO writes. NO mv. NO rm.

Step 5: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on findings (violations? counts? doc generated?)
artifacts: [paths read, output paths if any (e.g. summary.md emitted)]
next:      suggested next command (often /haipipe-project-organize if violations
           found, or /haipipe-project-new for missing project)
```

---

Risk Profile
-------------

**Read-only.** `allowed-tools` deliberately excludes Write/Edit. If a write
is needed (e.g. summarize wants to drop a `summary.md`), the skill calls
`Bash` to redirect output to a file under the project's own folder — but
never modifies code, configs, or other projects' state.

If a violation is found that needs fixing, hand off to
`/haipipe-project-organize`. Don't fix here.
