# q01_skill_layers

answer-status: open

Answer
======

The skills now sit in three layers. Counts are SKILL.md files, taken on 2026-10-07 after q02 and
q03. The servers do not mirror the layers as folders. They mirror them by name: the base is
`servers/workbench` (with its Task level at `servers/workbench/task`), and each theme is a
`servers/workbench-<theme>`. Three choices are still open (see Open choices); the
recommendations below are proposals for JL to settle.

Drawing: [s02 skill layers](../../studio/s02-skill-layers/s02-skill-layers.excalidraw), read from disk; open points in red.


What each layer holds
=====================

```text
skills/
├── 0_utils/   10   one folder per skill, not tied to the Block -> Job -> Task ladder
│                   response-format · diagram-ascii · draw-logic-tree · table-workbench ·
│                   table-papers · notebook-cell-python · remote-error · call-peer ·
│                   meal-cam-logger · whoop-connect
├── 1_base/   109   what every theme is built on
│   ├── project   2   haipipe-project (the Project and its worlds) · haipipe-run (the Run contract)
│   ├── task     50   haipipe-task, workbench-task, the task-for-* variants, and the data ·
│   │                 nn · end · individual pipeline skills
│   ├── page     15   haipipe-page, haipipe-folder, haipipe-sentence, haipipe-page-workflow and
│   │                 its Run skills, workbench (the contract), workbench-page, workbench-studio
│   ├── question  4   haipipe-question, -asking, -review, ask-questions
│   ├── writing   4   haipipe-writing, humanizer, academic-humanizer, writing-dna-skill
│   ├── display  12   haipipe-display and its renderers, html-ppt, excalidraw-*, *-to-svg
│   ├── ideation 13   haipipe-ideation and its generate · test · select skills
│   └── search    9   haipipe-search, arxiv, openalex, semantic-scholar, ...
└── 2_theme/   57   one folder per theme: its haipipe-<theme> skills and its workbench-<theme>
    ├── cowork    2   haipipe-cowork · workbench-cowork
    ├── design    6   haipipe-design (+ brief, goal, unit, workflow) · workbench-design
    ├── discovery 8   haipipe-discovery (+ inquiry, review, synthesize), 3 reading skills · workbench-discovery
    ├── insight  13   haipipe-insight and its folder-kinds · workbench-insight
    ├── labeling 19   haipipe-labeling (the door) and its -workflow, -building, -scanning (+ their
    │                 workflows), workbench-labeling, the 12 view skills in 1_data/ 2_labeling/
    │                 3_quality/ 4_delivery/, engine/  (renamed and grouped 261007, see q04)
    ├── paper     9   haipipe-paper (+ story, section, round, assemble, ...) · workbench-paper
    └── work      2   haipipe-work (the door, new 261007) · workbench-work (moved from 1_base/task)
```


How the servers pair with them
==============================

| Layer | Skill (contract) | Server (served face) |
|---|---|---|
| 1_base | `page/workbench` (Storage · Surface · Writer · Boundary) and `page/workbench-studio` | `servers/workbench` (Studio, Guide, the base) |
| 1_base | `page/workbench-page` (the Page Task's Spaces) | `servers/workbench/task` (the base's Task level, once workbench-page) |
| 2_theme | `<theme>/workbench-<theme>` for cowork · design · discovery · insight · labeling · paper · work | `servers/workbench-<theme>` |
| outside | none | `servers/_host` (transport), `space-home`, `haipipe-page` (standalone Page server) |

`0_utils` has no server.

Code finds a skill by its folder name (`host_paths.skill_dir`), and the host finds the
workbenches by the `workbench` and `workbench-*` names (`host_registry.workbench_folders`). So
a layer move does not touch the servers, and a server move does not touch the skills.


Open choices
============

1. Where workbench-page sits.
   It is the Page Task's workbench, so it could move to `2_theme/page` while the Page core
   (haipipe-page, the workflow, its Runs) stays in `1_base/page`. JL settled the server side on
   2026-10-07: workbench-page's server became the base workbench's Task level,
   `servers/workbench/task`. Recommendation: keep the skill in `1_base`, so skill and server
   stay in the same layer. A `2_theme/page` would then hold nothing.

2. A workbench skill for the frame contract, in 1_base.
   b03's design (`designs/b03_project_workbench/studio/s02-workbench-shared/`; b03's s08, then b02's s01, back in
   b03 when b02 merged into it on 2026-10-07) proposes that the base workbench own the Block · Job · Task frame, and that
   each theme give only its `theme.py` and views. Its contract already exists in parts:
   `1_base/page/workbench` (the four-part contract) and `1_base/page/workbench-studio` (Studio).
   Recommendation: give them their own base family, `1_base/workbench/`, holding `workbench`
   (the frame contract), `workbench-studio`, and `workbench-page` as the Task level. This pairs
   one to one with `servers/workbench/` and `servers/workbench/task/`, and leaves `1_base/page`
   to the Page core.

3. Whether servers/ mirrors the layers.
   Option (a): keep it flat, with the name carrying the layer (`workbench` is the base,
   `workbench-<theme>` a theme). Option (b): `servers/1_base/`, `servers/2_theme/`.
   Recommendation: (a). The names already say the layer, the host discovers workbenches by name,
   and (b) would repeat q02's path fix for no gain. A theme's server still sits next to the
   theme's skills by name: `skills/2_theme/<theme>/workbench-<theme>` ↔ `servers/workbench-<theme>`.


Things the inventory shows
==========================

- Task is in 1_base, but its Block workbench is shaped like a theme. JL settled this on
  2026-10-07: the theme is now `work`, and its server is `servers/workbench-work` (URL still
  `/_board/task-board`, `--only task` still accepted). The skill `1_base/task/workbench-task` has
  not followed yet; see the work-theme question.
- Done 261007: `workbench-labeling` moved to the family top and the labeling door is
  `haipipe-labeling`; work has `haipipe-work` and `workbench-work` in `2_theme/work/`. Every theme
  now has a `haipipe-<theme>` door and a top-level workbench skill (drawn in s04); only insight's
  agents still break the common shape.
- `1_base/task` (50 skills) also holds the HAI-Pipe ML pipeline (data · nn · end · individual).
  Those are work-Task variants, but they could form their own theme if the base should stay
  generic.
- `0_utils` also holds personal tools (meal-cam-logger, whoop-connect), not just toolkit helpers.


Next
====

- JL: settle choices 1–3.
- If choice 2 is taken: move `workbench`, `workbench-studio` (and `workbench-page`) into
  `1_base/workbench/`, then rerun the q02 checks (link checker, FAMILIES check, the suites).
