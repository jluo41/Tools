# j03 · Project structure and its workbench

job-of: b01_haipipe-toolkit (the Block `b03_project_workbench` until 261009; its questions, studio and runs moved with it)
spine: Design questions about how a Project is built from its root down to one Run: the Themes (tasks, discoveries, cowork, papers, insights, designs), the Block → Job → Task → Run levels inside them, the Questions at Block level, how content crosses Themes, the checker that tests it all, and the workbench that shows it: the base frame (Block · Job · Task × six Spaces), each theme on it, and its Guide.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, checker or workbench change that settled it.

## Topic

A Project (`examples*/<Project>/`) holds Themes; a Theme holds Blocks (`bNN_<topic>/`
with `board.md`); a Block holds Jobs (`jNN_<job>/`); a Job holds Tasks (`tNN_<task>/`,
a Task Folder is a Page Folder); a Task holds Runs (`runs/<run>.*` with the same-stem
`results/<run>/`). Today the levels are written in pieces: `haipipe-project` owns the root
and the Themes, each domain skill owns its own inside, and `haipipe-run` owns Run identity
without knowing the tree. This Block asks how they fit into one contract, how each Theme
climbs it, and how one checker can test it.

Most answers here are a change to `haipipe-project` (its `ref/` and
`scripts/audit_projects.py`), `haipipe-run`, or a Theme owner's skill, not a Task Run. A
Question may therefore have no work entries; its report links the changed files and the
drawings in `studio/`.

Excluded: the internals of each Theme (owned by `haipipe-task`, `haipipe-discovery`,
`haipipe-paper`, `haipipe-insight`, `haipipe-design`, `haipipe-cowork`); this Block asks
only about the levels they share and what crosses between them.

The workbench is the same design seen on screen (merged from b02_workbench, 261007: "the project
folder and workbench UI are the same things"): the base `servers/workbench/` draws any Block, Job
or Task folder in one frame, each theme (`servers/workbench-<theme>/`) fills it, and each theme's
Guide lives in its `guide/` and `related/`. Q07 and Q10-Q09 are these questions; their answers are
changes to the servers or a workbench skill.

## Pipeline

```text
chat section -> Related question -> haipipe-question -> skill or checker change -> report Page
                                                     -> studio/ scratch drawings (shared by the questions)
```

## Pages

No Jobs yet. The working drawing is `studio/project-scratch.excalidraw`, rebuilt by
`studio/_build/make.sh` from what is on disk.
The workbench drawings are `studio/s02-workbench-shared/` (the base frame and each theme on it) and
`studio/s31-guide/` (the Guide tab), both rebuilt by the same `make.sh`; `studio/s32-element-ui/` is the
gallery of every element's looks today, to pick one each.

## Questions

```yaml
questions:
- id: Q01
  title: What are the boundaries of B, J, T and R?
  question: What does each of Block, Job, Task and Run own, where does one end and
    the next begin, and what files must each hold?
  hypothesis: Block = one topic with board.md and its Questions; Job = one line of
    work; Task = one folder that is also a Page; Run = one commissioned ticket with
    its same-stem Result and receipt.
  acceptance: Answered when each level has one definition, its required files and
    its owner skill, written in one hierarchy reference that the checker reads.
  work: []
  report: reports/q01_bjtr_boundary/q01_bjtr_boundary.md
- id: Q02
  title: How does B-J-T-R run through each Theme?
  question: How do tasks, discoveries, cowork, papers, insights and designs each fill
    the Block, Job, Task and Run levels, and where does a Theme bend or skip a level?
  hypothesis: tasks and discoveries use all four; insights, designs and papers fill
    the levels under their own names; cowork stops at Job. One table per Theme can
    declare this instead of forcing renames.
  acceptance: Answered when every Theme has a row saying which folder fills each level
    or that it skips it, and the scan on disk agrees with the table.
  work: []
  report: reports/q02_bjtr_across_themes/q02_bjtr_across_themes.md
- id: Q03
  title: How do Questions live at the Block level?
  question: How does every Theme keep its Questions at Block level (the board.md register,
    reports/qNN_<topic>/, studio/), and how do its Jobs, Tasks and Runs feed those
    reports?
  hypothesis: 'Every Block in every Theme keeps one shape: board.md register, reports/qNN_<topic>/
    beside studio/; the Runs below are the evidence a report cites.'
  acceptance: Answered when each Theme's Block has the same register and reports/
    shape, or a stated reason why not, and the checker can see it.
  work: []
  report: reports/q03_block_questions/q03_block_questions.md
- id: Q04
  title: How is content shared across Themes?
  question: 'What crosses between Themes and how is it bound: a paper taking from
    tasks and discoveries, a design from insights, and does insights read from tasks
    or hold its own Runs?'
  hypothesis: 'A consumer binds a producer''s Result by exact identity and never copies
    it: papers bind Task and Discovery Results, designs read a signed Insight handoff.
    Whether Insight calls Task Runs or runs its own is open: the older register board
    runs from tasks/, the Prototype/Instance pair runs its own.'
  acceptance: Answered when each consumer and producer pair names what crosses (a
    Result, a handoff, a Page) and how it is bound, and the insights choice is made.
  work: []
  report: reports/q04_cross_theme_content/q04_cross_theme_content.md
- id: Q05
  title: Which skill owns each level?
  question: 'How should the skills line up with the ladder: one haipipe-project door
    with a sub-skill per level (theme, block, job, task, run), separate level skills,
    or one skill with sub-commands; and where do haipipe-board, haipipe-folder, haipipe-task
    and haipipe-run go?'
  hypothesis: One haipipe-project door plus haipipe-project-theme, -block, -job, -task,
    -run; each Theme keeps its own owner; haipipe-task keeps only the tasks Theme;
    haipipe-board retires into -block in steps, not one delete.
  acceptance: Answered when every level names exactly one owner skill, the Theme owners
    are separated from the level owners, and the migration of haipipe-board, haipipe-folder
    and haipipe-run is written.
  work: []
  report: reports/q05_skill_per_level/q05_skill_per_level.md
- id: Q06
  title: What should the project checker test?
  question: How deep should haipipe-project's checker go below the Project root, and
    what should it test at each level?
  hypothesis: 'Walk every Theme down to Run: the names at each level, board.md, Ticket
    and Result pairs, and the receipt run: equal to its stem; what a receipt means
    stays with each owner.'
  acceptance: Answered when audit_projects.py walks all six levels, the report lists
    what it finds on disk, and the skill documents the checks.
  work: []
  report: reports/q06_project_checker/q06_project_checker.md
- id: Q07
  title: How does the workbench map onto the ladder?
  question: How do the workbench parts (Space, View, Run type, Run, skills and agents)
    line up with Theme, Block, Job, Task and Run, so each level has one place to look
    and one place to act?
  hypothesis: 'A workbench shows one level: a Board workbench a Block, the Page workbench
    a Task. Spaces are the stages of that level (Guide, setup, work, Delivery), Views
    the tabs inside a Space, a Run type is a kind of Run Spec, a Run is the ladder
    Run, and each Workbench Table row binds Space, View, Run type, Agent, Skill and
    who signs.'
  acceptance: Answered when a table maps each level to its workbench, Spaces and Run
    types, and each Run type names its skill, agent and signer.
  work: []
  report: reports/q07_workbench_mapping/q07_workbench_mapping.md
- id: Q08
  title: 'How is a workbench managed: one shared base, a theme each?'
  question: What does workbench own for every level (Block, Job, Task), what does
    each workbench-<theme> give it, and where does a theme keep its Guide?
  hypothesis: 'workbench is the base: the level tabs, the six Spaces and their
    order, the third row, Idea Studio, the Runs panel, Question │ Work │ Report, the BJTR
    tree and one look; each theme gives a theme.py (level names, levels, subspaces, fields,
    run types), its own guide/ (Description, Method, RoadMap, Related Paper) and optional
    views/ where one Space needs its own body.'
  acceptance: Answered when the frame contract is written (a workbench skill),
    the Runs panel lives in workbench, one theme (task) runs on the base, and each
    theme's Guide is read from its own guide/.
  work: []
  report: reports/q08_workbench_base/q08_workbench_base.md
- id: Q09
  title: How do Studio drawings and Reports show and save in a workbench?
  question: How does a workbench list a Block's studio/sNN-<topic>/ drawings and its
    reports/qNN_<topic>/ Pages, who may edit each drawing, and how does it keep a person's
    canvas edits safe from a newer build?
  hypothesis: 'Studio is for creation and Report for presentation: Idea Studio lists one
    row per studio topic; a generated drawing stays view only, a scratch gets the pen, a
    report drawing opens view first with Suggest; a plain drawing save checks its base
    revision and is refused when stale; + Add topic makes studio/sNN-<topic>/; a session is
    kept as one summary in the topic''s chat/.'
  acceptance: Answered when the six workbench changes in the Q03 draft (Workbench to
    change) are made or turned down with a reason, and a stale editor tab can no longer
    save over a newer build.
  work: []
  report: reports/q09_studio_report_on_screen/q09_studio_report_on_screen.md
- id: Q10
  title: How should a workbench's Guide explain its method?
  question: What should Guide › Method hold for a family, how is it drawn, and how
    do its methods connect to their papers?
  hypothesis: 'One page per family: the steps, a method file with one card per method,
    an editable methods canvas, and the tests; shared rendering so every family''s
    page looks alike.'
  acceptance: Answered when the families' Method pages follow one shape, served by
    one renderer, and the shape is written in servers/README.md.
  work: []
  report: reports/q10_guide_method/q10_guide_method.md
- id: Q11
  title: How should a Page's logic and structure be drawn?
  question: How should a Section's argument and its place in the paper be drawn, so
    a person can read, write beside and check each point and its evidence?
  hypothesis: 'Two drawings read left to right: the logic tree is the person''s and
    editable; the Section map is generated and view only; both put each Bullet on
    its own row with its evidence cards beside it.'
  acceptance: Answered when both drawings exist on a real Section, pass their checks,
    and show in the workbench without one canvas saving into another.
  work: []
  report: reports/q11_logic_drawing/q11_logic_drawing.md
- id: Q12
  title: How do we host the SPACE so others can open it?
  question: 'How should the SPACE-level website (SPACE Home, the Block workbenches,
    the studio drawings) be hosted so colleagues can open it from their own machines:
    where it runs, how they sign in, what they may see and do, and how it stays in
    sync with the repository?'
  hypothesis: Run the live server on an always-on internal host behind company sign-in,
    in a viewer mode with no terminal, chat or writes, pulling the SPACE from git;
    sharing a laptop over Tailscale is the stopgap. A static export stays retired.
  acceptance: Answered when a colleague opens SPACE Home and a Block workbench from
    their own machine, sees only what a viewer may see, and the host, sign-in, viewer
    mode and sync are written in servers/README.md.
  work: []
  report: reports/q12_space_hosting/q12_space_hosting.md
```

## Renumbered (261007)

b02 (workbench) merged into this Block, which became `b03_project_workbench`; the studio topics
and Questions were then put in order: the folders, then the screens, then each Space, then the
variants by level. A decision id moved with its topic (`s02-D05` is now `s04-D05`). Run names
inside a report keep the numbers they were made with.

```text
studio topic                     was        Question                      was
s01-overall-tree-structure       s01        q01_bjtr_boundary             q01
s02-workbench-shared             s07        q02_bjtr_across_themes        q02
s03-guide                        s08        q03_block_questions           q03
s04-studio-and-report            s02        q04_cross_theme_content       q04
s05-runs                         s06        q05_skill_per_level           q06
s06-block-variants               s03        q06_project_checker           q05
s07-job-variants                 s04        q07_workbench_mapping         q07
s08-task-variants                s05        q08_workbench_base            q11 (b02 q03)
                                            q09_studio_report_on_screen   q12 (b02 q04)
                                            q10_guide_method              q09 (b02 q01)
                                            q11_logic_drawing             q10 (b02 q02)
                                            q12_space_hosting             q08
```

Then (261007, later) the level topics and the Guide moved to their own ranges: the Block, Job and
Task variants are s11 · s12 · s13 (as in the theme Blocks), the Guide is s31 (as each theme's s31-<theme>-guide).
Their decision ids moved too (`s03-D07` is now `s31-D07`).

```text
studio topic                     was
s11-block-variants               s06
s12-job-variants                 s07
s13-task-variants                s08
s31-guide                        s03
s32-element-ui                   s03 (261008: the element gallery beside the Guide, s3x)
```

## Related resources

```yaml
resources:
- title: haipipe-project skill (root contract, Themes, audit_projects.py)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/1_base/project/haipipe-project
  questions:
  - Q01
  - Q02
  - Q06
  contribution: Owns the Project root and the Themes; its audit checks the root only.
  notes: ''
- title: haipipe-run skill (Run identity, dialects, receipts)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/1_base/project/haipipe-run
  questions:
  - Q01
  - Q06
  contribution: Owns what a Run is, its Ticket/Result pairing and the six storage dialects.
  notes: ''
- title: Shared Guide method page (workbench_guide.method_page_html)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/servers/workbench
  questions:
  - Q10
  contribution: Serves a family's method file, cards and methods canvas in Guide ›
    Method.
  notes: ''
- title: draw-logic-tree and excalidraw-section skills
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree
  questions:
  - Q11
  contribution: The logic tree (the person's drawing) and the Section map (generated),
    with their checks.
  notes: ''
