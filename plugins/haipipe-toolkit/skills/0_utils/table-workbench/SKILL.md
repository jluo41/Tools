---
name: table-workbench
description: >-
  Write, check and render a Workbench Table: one row per run type a served
  workbench offers, in seven columns (Level · Space · View · Run type · Agent ·
  Skill · Person signs). It answers, for every Space and view of a workbench,
  which run starts there, which agent does it, which skill tells the agent how,
  and what the person must sign. Use to plan a workbench, to split one large
  skill into one small skill per Space and view, or to audit that every run
  names an agent and a skill that exist. Trigger: workbench table, table
  workbench, space view run type, which agent, which skill, person signs,
  /table-workbench.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.2.1"
  last_updated: "2026-10-01"
  # version history: ./CHANGELOG.md
---

# /table-workbench · Space · View · Run type · Agent · Skill · Person signs

A **Workbench Table** is the contract between a served workbench and the skills
and agents behind it (JL 261001). Each row is one run type a person can start
from one view of one Space:

```text
Level       board or page: which screen of the workbench
Space       a tab of that screen (Design Goal, Design, Delivery, ...)
View        a subspace of the Space: one tab or view inside it
Run type    the button in that Space's Runs panel
Agent       who does the run: an agent, never a person
Skill       how the agent does it: one small skill for that view
Person signs  the decision the person owns on that run, or none
Folder      optional: where the run writes, or none (a verdict only)
```

**Folder** is an optional eighth column. A table has it on every row or on none; when
it is there, `--check` flags an empty cell, `--format blocks` prints a `writes` line, and
the shared Guide's RoadMap Draw shows it beside Agent and Skill.

The skill is the method; the agent is the actor. Every run names both. The
person never does a run; the person signs what is theirs (an aim, a rule, a
release or hold, a test plan), and an agent may prepare each of those.


Rules
-----

1. **One row, one run type.** A view with no run type gets a row with run type
   `none`, agent `none` and skill `none`, so every view is listed.
2. **Every run names an agent.** A run whose agent is `none` is read-only.
3. **One skill per view.** A large owner skill (a `-workflow` skill) routes and
   gates; it is never the Skill of a row. Write the small skill that does the work.
4. **Make and judge apart.** A row that judges another row's output (Verify,
   review, check) names a different agent from the one that made it.
5. **Person signs is a decision.** Write the object signed (`the aim`,
   `release or hold`), or `none`. Never write a person into the Agent column.
6. **Planned rows say so.** A skill or agent that does not exist yet carries
   `(new)` after its name; the checker fails any other name it cannot find.
7. **Order follows the work.** Rows run input → process → output: the Space that
   states the aim first, the Space that makes designs next, delivery last.


Where a table lives
-------------------

Each workbench keeps its own table beside its skill:

```text
skills/<family>/workbench-<name>/ref/workbench-table.md
```

The file is the source. It holds one Markdown table with exactly the seven
columns above, in that order, and may hold notes before and after it. The first
instance is the Design workbench:
`skills/2_theme/design/workbench-design/ref/workbench-table.md`.

When the workbench's Runs panel reads a run-cards file, that file and this table
must agree: each `🔘 BUTTON` is one row's Run type, its `🤖 AGENT`, `🧩 SKILL` and
`✍️ SIGNS` lines are that row's Agent, Skill and Person signs. `--check --cards`
checks both directions. Guide rows have no card: Guide's Runs panel reads them from this table.


Render and check
----------------

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/table-workbench/ref/render_workbench_table.py <table.md>
    --format md        # the Markdown table, as written (default)
    --format blocks    # one block per Space: reads well in a narrow terminal
    --check            # exit 1 on a rule break or a name not found on disk
    --cards <file>     # with --check: the run-cards file must agree with the table
```

`--check` reports, per row: an empty column, a person in the Agent column, a
`-workflow` skill used as a row's Skill, a judging row whose agent also makes,
and every Skill or Agent name that neither exists under `Tools/plugins/` nor
carries `(new)`. It prints the list of planned (`new`) skills and agents last, so
the table doubles as a build list.

Paste a Workbench Table into chat with `--format blocks`: a seven-column box
table wraps into unreadable cells at terminal width.


Boundary
--------

This skill owns the table's shape and its check. It does not create the skills
or agents a table plans, and it does not change a workbench's code; the owning
workbench skill does both, then reruns `--check`.
