# j12 · Theme: design

job-of: b01_haipipe-toolkit (the Block `b12_theme_design` until 261009; its questions, studio and runs moved with it)
spine: How the design theme sits on the Block → Job → Task → Run ladder and shows in its workbench: a design Board for one application, a Job for one goal done by one design method returning N designs, a Task for one design, and the Runs that commission, generate, verify and revise them; how an insight Block steers a design through one handoff; and which skill and workbench owns each part.
close: Each recorded question has a report Page with an answer status; the drawings in studio/ match the shared definitions in b03_project_workbench, and every open point is either decided or carried as a question.

## Topic

The design theme makes N designs for one goal by one method, checks them, and releases the ones that
pass; running the experiment is outside it. This Block designs that theme's place on the ladder:

```text
B00_DesignBoard-<app>/            Block: one application, one channel
├── Description                   the goal list (Brief) · theory · shared rules
└── jNN_<goal>_<design-method>/       Job: one goal × one method → N designs
    ├── method.md                 the method card, frozen: ① see ② do ③ check
    ├── runs/                     commission · generate (the N drafts)
    └── tNN_d<NN>_<slug>/         Task: one design: Design · Rationale · Evaluation
        └── runs/                 verify · revise
```

The method (13 methods in 3 families, the six steps) is the theme's own:
`plugins/haipipe-toolkit/servers/workbench-design/guide/method.md`. Today's folder
contract is `haipipe-design/ref/method-folders.md` beside it, where the method alone is the Job.

The trees, skills and screens are defined once with every other theme's, in
`../b03_project_workbench/studio/s01-overall-tree-structure/` (`build_ladder_v4.py`, `level_views.py`); this
Block's drawings gather the design rows from there. Its sibling is `../b11_theme_insight/`, the theme
that steers a design.

Its studio holds the theme's drawings, one topic each, each drawing beside the script that draws it;
the design workbench's Guide opens them here (261007: the servers hold code only):

```text
studio/
├── s00-design-structure/  the thinking: what a design method is, how it evolves (a scratch)
├── s01-design/          the design ladder at a glance
├── s02-workbench-ui/    the workbench's drawing (Guide › RoadMap Draw)
├── s03-design-methods/  the methods drawing and the design unit (Guide › Method)
├── s11-design-block/    the Block level: each Space as full screens, on disk under each
├── s12-design-job/      the Job level: one goal × method version × inputs version → N designs
├── s13-design-task/     the Task level: one design
├── s21-run-skill/       every design Run and the skills behind them
├── s31-design-guide/    the Guide tab cut by level: four Views × Block · Job · Task
├── s32-design-element-ui/  every element the design theme draws, today and as planned, with one proposed look each
└── s61-design-slides/   the high-level deck: its logic flow, then the slides (writes delivery/design-slides/)
```

Excluded: making real designs (that is a design Board's own work, under a Project), and the ladder
shared by every theme (`../b03_project_workbench/`).

## Pipeline

```text
a mark on a drawing -> the shared definitions (b03) -> the drawings rebuilt -> a question's report
```

## Questions

```yaml
questions:
- id: Q01
  title: How does design climb the ladder?
  question: Where does design sit on the ladder, and what do its Block, Job, Task and Runs each hold
    and show on screen?
  hypothesis: The Block is one application and channel (its goal list, theory and shared rules); a
    Job is one goal done by one method, returning N designs, with the Block's six Spaces; a Task is
    one design (Design · Rationale · Evaluation); verify and revise are per-design Runs, Generate
    is the Job's.
  acceptance: Answered when every level names its folder and its six Spaces' content, drawn in studio/s11-design-block, s12-design-job and s13-design-task,
    and method-folders.md agrees or is changed.
  work: []
  report: reports/q01_design_ladder/q01_design_ladder.md
- id: Q02
  title: What does the design workbench show?
  question: What does the design workbench show at each level, Space by Space, and how do today's
    Design Tasks, Design and Delivery views move there?
  hypothesis: Description = the goal and the frozen method card; Audience Report = the element matrix
    across the N designs; Work Details = the designs; Runs = commission · generate · verify · revise;
    Delivery = the released designs, word for word.
  acceptance: Answered when each level's screen is drawn (studio/s02-workbench-ui redrawn on the new
    Job) and the workbench serves it.
  work: []
  report: reports/q02_design_workbench/q02_design_workbench.md
- id: Q03
  title: How does insight steer a design?
  question: How does an insight Block steer a design, and where does that link show on both sides?
  hypothesis: 'Through one crossing: a signed Wisdom answer is handed off, listed in the design Block''s
    Resources, read by the Jobs whose method reads our data (by insight · tailoring · theory and insight);
    each design''s elements name it.'
  acceptance: Answered when the handoff path is written on both sides (b11 Q04 and here) and drawn.
  work: []
  report: reports/q03_insight_steers_design/q03_insight_steers_design.md
```
