# b02 · Base skills

board-kind: task-block
spine: Design questions about the base layer, `plugins/haipipe-toolkit/skills/1_base/`: what each base family (project, task, page, question, writing, display, ideation, search) gives the themes, whether every base family has one common shape, and which skills sit in base but belong elsewhere.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill change that settled it (or the move b04 made for it).

## Topic

The toolkit's skills sit in three layers: `0_utils` (generic helpers, Block b01), `1_base` (what
every theme is built on, this Block) and `2_theme` (one folder per theme, Blocks b11 to b17).
The base layer holds eight families, each with a `haipipe-<family>` door:

```text
skills/1_base/
├── project/    haipipe-project (the Project and its worlds) · haipipe-run (the Run contract)
├── task/       haipipe-task (the Task folder: Plan, Build, Execute, Report), the
│               haipipe-task-for-<kind> skills, the HAI-Pipe stage pipelines (data, nn, end,
│               individual), haipipe-workflow, haipipe-page-task, the task agents
├── page/       haipipe-page (the Page engine), haipipe-page-workflow and its Run skills,
│               haipipe-folder, haipipe-sentence, workbench, workbench-studio, workbench-page
├── question/   haipipe-question (a Block's Questions and report folders), -asking, -review
├── writing/    haipipe-writing, humanizer, academic-humanizer, writing-dna-skill
├── display/    haipipe-display and its renderers, html-ppt, excalidraw-*, *-to-svg
├── ideation/   haipipe-ideation and its generate · test · select skills
└── search/     haipipe-search, arxiv, openalex, semantic-scholar, ...
```

A theme may call any base family, but never another theme: what several themes call belongs in
base. This Block asks, family by family, what the base gives, whether its shape is the same
everywhere, and what is in base by accident.

Most answers here are a decision recorded in a report Page and a drawing; a decision that moves
or renames a skill is carried out by b04_skill_folder (it owns skill moves and path fixes).

Excluded: the Block → Job → Task → Run ladder and the base workbench's frame (b03_project_workbench);
each theme's internals (its b1x Block); the `0_utils` helpers (b01_utils); moving files (b04_skill_folder).

## Pipeline

```text
read the base on disk -> studio/ drawing -> report Page -> decision (JL) -> b04 moves or renames
```

## Pages

No Jobs yet. The working drawings are `studio/sNN-<topic>/`, each built from disk by a script beside
it (with b04's `studio/_build/sketch.py`); `studio/_build/make.sh` rebuilds them all:

```text
studio/
├── s01-base-overview/       the base layer at a glance: every family, its door, skills, agents, tests
├── s02-base-map/            Q01: each base family x who calls it            (drawn)
├── s03-base-shape/          Q02: one row per family, where it differs          (planned)
├── s04-not-base/            Q03: each candidate and its proposed home          (planned)
└── s05-workbench-skills/    Q04: page's three workbench skills, servers/workbench (planned)
```

## Questions

```yaml
questions:
- id: Q01
  title: What does each base family give the themes?
  question: For each base family, what does it provide (contract, engine, CLI, agents),
    and which themes and other base families call it?
  hypothesis: Every theme calls haipipe-task, haipipe-run, haipipe-page and haipipe-question;
    no theme calls another theme; a few base skills are called by one theme only,
    which makes them candidates to move into that theme.
  acceptance: Answered when a map of base family x caller (theme or base family) is
    drawn from disk, and every theme-to-theme call and every single-caller base skill
    is listed.
  work: []
  report: reports/q01_base_map/q01_base_map.md
- id: Q02
  title: Does a base family have one common shape?
  question: What should every base family have (door skill, ref/, cli/ or scripts/,
    agents, tests, CHANGELOG), and which families differ from that shape today?
  hypothesis: The shape matches a theme's (a haipipe-<family> door at the family top,
    its agents in one place); the families differ mainly in where agents live and
    in nested sub-families (task's 1_data ... 10_page, ideation's 1_generate ... 3_select).
  acceptance: Answered when the common shape is written down and one row per family
    shows where it differs, drawn in studio/.
  work: []
  report: reports/q02_base_shape/q02_base_shape.md
- id: Q03
  title: What sits in base but is not base?
  question: Which skills in 1_base are specific to one domain or one theme (the HAI-Pipe
    stage pipelines in task/, paper-only skills in ideation/ and search/), and where
    should each go?
  hypothesis: The stage pipelines are a domain, not base; haipipe-workflow belongs
    beside haipipe-run in project/; paper-only skills (journal fit, Nature-paper review)
    belong to the paper theme; agree the task/ split with b17 (its Q04 asks what the
    work theme takes).
  acceptance: Answered when every candidate has a proposed home JL agrees, and b04
    has moved the ones that move.
  work: []
  report: reports/q03_not_base/q03_not_base.md
- id: Q04
  title: Where does the page family's workbench part belong?
  question: The page family holds three workbench skills (workbench, workbench-studio,
    workbench-page) for one server, servers/workbench (with its Task level). Should
    they stay in page/, or form their own base family beside the base workbench's
    frame?
  hypothesis: A 1_base/workbench/ family (the frame contract, Studio, the Page Task
    level) pairs one to one with servers/workbench/ and leaves page/ to the Page engine;
    settle with b03, which designs the frame.
  acceptance: Answered when JL and b03 agree where the three skills sit, and b04 has
    moved them.
  work: []
  report: reports/q04_workbench_skills/q04_workbench_skills.md
```
