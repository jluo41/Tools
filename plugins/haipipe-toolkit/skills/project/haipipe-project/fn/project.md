fn-project: Scaffold a New Project (plain directory)
====================================

Output: `examples/{PROJECT_ID}/` container folders (see Step 2 skeleton).
Forbidden at top level: README.md, docs/, cc-archive/, _old/, configs/, results/.

ROUTING: this fn creates a PLAIN DIRECTORY (ProjX-* names). If the name starts with `Project-`, the user wants a REPO-BACKED project (own GitHub repo + submodule) -> use `fn/repo-project.md` instead.

A project is the outer container. It holds task-groups (Level 2), which hold task-folders (Level 3). See `ref/hierarchy.md`.

QUICK BY DEFAULT: setup creates the folders and stops. No metadata questionnaire, no diagram authoring, no seed task-group, no code stubs. Those are on-request extras (see the last section).


Step 1 -- Resolve PROJECT_ID
----------------------------

If the invocation already carries a well-formed name, use it. Otherwise ask ONE question:

  Series letter / Category / Num / CamelCase Name
  → compose PROJECT_ID = `Proj{Series}-{Category}-{Num}-{Name}`

Nothing else is collected at setup.


Step 2 -- Create skeleton
-------------------------

```
examples/{PROJECT_ID}/
├── tasks/             internal structure owned by /haipipe-task
├── discoveries/       internal structure owned by /haipipe-discovery
├── insights/          internal structure owned by /haipipe-insight
├── diagram/           EMPTY at setup; authored later via /diagram-ascii on request
└── papers/            papers land here later (owned by /haipipe-paper-*)
```

Create the top-level folders only. Each world's internal structure is scaffolded later by its owning skill when first used; this fn never restates their rules.


Step 3 -- Report
----------------

Print the folders created + the on-request extras below as suggested next steps. Done.


On request only (NOT part of default setup)
--------------------------------------------

```
project diagram      user asks "author the project diagram" →
                       collect: research question / why it matters / in-out of scope
                       /diagram-ascii → 01-story.txt, 02-boundary.txt (one call per file)
                       /diagram-ascii-canvas {PROJECT}/diagram/ → project.excalidraw

first task-group /   → /haipipe-task (task-group + task-folder scaffolds live there)
task-folder

Track A code stubs   new pipeline Fn or ML model → ref/code-structure.md
                       (paired-example rule: every stub gets a demo task)
```
