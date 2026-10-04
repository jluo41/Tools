# b02 · Workbenches

board-kind: task-block
spine: Design questions about the served workbenches in `plugins/haipipe-toolkit/servers/workbench-*`: the shared shell and Guide, and how each family's workbench explains and shows its work.
close: Each recorded question has a report Page with an answer status, and every answered question names the server or skill change that settled it.

## Topic

Every family has a workbench (Page, Paper, Task, Insight, Design, Labeling) on one shared
shell from `workbench-shared`: a band, a Space row with Guide first, one box per Space, and a
Runs panel beside it. Guide has four Views (Description, Method, RoadMap Draw, Related Paper)
filled from `guide_families.py`. Its questions are about the workbenches themselves: what a
Guide View should hold, how a family's method is explained and drawn, and how the Spaces
show a family's work.

Most answers here are a change to a workbench's server code, its skill's `ref/` files or the
shared rules in `servers/README.md`, not a Task Run. A Question may therefore have no work
entries; its report links the changed files.

Excluded: the small cross-cutting skills (`0_utils`, Block b01) and the question skills
(`skills/question/`).

## Pipeline

```text
chat section -> Related question -> haipipe-question -> workbench change -> report Page
```

## Pages

No Jobs yet: the first questions are answered by workbench changes.

## Questions

```yaml
questions:
- id: Q01
  title: How should a workbench's Guide explain its method?
  question: What should Guide › Method hold for a family, how is it drawn, and how
    do its methods connect to their papers?
  hypothesis: 'One page per family: the steps, a method file with one card per method,
    an editable methods canvas, and the tests; shared rendering so every family''s
    page looks alike.'
  acceptance: Answered when the families' Method pages follow one shape, served by
    one renderer, and the shape is written in servers/README.md.
  work: []
  report: reports/q01_guide_method/q01_guide_method.md
- id: Q02
  title: How should a Page's logic and structure be drawn?
  question: How should a Section's argument and its place in the paper be drawn, so
    a person can read, write beside and check each point and its evidence?
  hypothesis: 'Two drawings read left to right: the logic tree is the person''s and
    editable; the Section map is generated and view only; both put each Bullet on
    its own row with its evidence cards beside it.'
  acceptance: Answered when both drawings exist on a real Section, pass their checks,
    and show in the workbench without one canvas saving into another.
  work: []
  report: reports/q02_logic_drawing/q02_logic_drawing.md
```

## Related resources

```yaml
resources:
- title: Shared Guide method page (workbench_guide.method_page_html)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/servers/workbench-shared
  questions:
  - Q01
  contribution: Serves a family's method file, cards and methods canvas in Guide ›
    Method.
  notes: ''
- title: draw-logic-tree and excalidraw-section skills
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree
  questions:
  - Q02
  contribution: The logic tree (the person's drawing) and the Section map (generated),
    with their checks.
  notes: ''
```
