# Which skills make the work theme?
state: 🔴 OPEN
answers: Q04
answer-status: open

## Opening

A proposal, not yet settled: the work theme takes the skills only work uses, and base keeps what
several themes call. Drawn in [s02 work skills](../../studio/s02-work-skills/s02-work-skills.excalidraw).

**Where this Page sits:** [Q04 · Which of today's 1_base/task skills belong to the work theme (2_theme/work), which stay in base because every theme calls them, and what is the work theme's door?](../../board.md).

**Why it matters:** `skills/2_theme/work/` exists but is empty; every work skill still sits in
`skills/1_base/task/`. The folder move and path fix belong to b04_skill_folder, which moves the
files once this Page records what goes where.

## Content

### Proposal

| Entry in 1_base/task | Proposed home | Why |
|---|---|---|
| `haipipe-task` | stays in `1_base/task` | insight, discovery, paper and page call it (the Task folder and Plan, Build, Execute, Report contract); a theme must not depend on another theme |
| `haipipe-workflow` | `1_base/project/` | a Workflow is a list of Runs; it sits beside `haipipe-run` |
| `workbench-work` | `2_theme/work/workbench-work` | pairs with `servers/workbench-work` |
| `<N>_<kind>/haipipe-task-for-<kind>` | `2_theme/work/<N>_<kind>/` | the kinds of work Task (data, algo, fit, eval, endpoint, display, stata, agent, page, individual) |
| `agents/` (task creator, reviewer, orchestrator) | open | page, insight and paper call them too |
| `haipipe-page-task` | open | the reader page of a work Task; page also calls it |
| stage pipelines (haipipe-data, -nn, -end, -individual) | open | this Block excludes them from the theme; they stay in base or become their own theme |
| `page-types/` | delete | an empty leftover beside `2_theme/insight/haipipe-page-insight` |

### Open points

- Each numbered folder (`1_data`, `2_nn`, `3_end`, `4_individual`) holds a work kind and a
  pipeline; splitting leaves the same number in two places.
- A theme's door is `haipipe-<theme>`. Does work get a thin `haipipe-work`, or is `haipipe-task`
  its door while it stays in base? Renaming `haipipe-task` touches about 830 files in the SPACE.
- `plugins/inlab-human` reads `1_base/task/4_individual` by path; a pipeline move breaks it.

### Evidence

- [s02 work skills](../../studio/s02-work-skills/s02-work-skills.excalidraw): today's
  `1_base/task`, the proposed home of each entry, and who calls each core skill, read from disk.
