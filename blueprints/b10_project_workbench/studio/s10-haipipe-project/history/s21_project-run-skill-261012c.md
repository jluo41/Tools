s21 · Project Run and skill
===========================

**Stage:** shaping

**Tags:** `Run and Skill`

**Topic:** every Run button of the base frame, by level and Space, the skill that should own it, and the
plan to update the base skills so every button has one (JL 261007: "what skill we should have for the studio
and for the report … I think we should have the haipipe-block, and haipipe-job, and also haipipe-studio and
haipipe-report, and haipipe-run … we need to update the skills a lot"). The base's counterpart of b16's
`s21-paper-run-skill`, in its style: lines-only tables, ink and gray, red for what is open, green ✎ for what
changed.

**Feeds:** `reports/` q05_skill_per_level · q08_workbench_base.

**Source:** read from disk on every build:

- the base frame's Run buttons per level and Space (`servers/workbench/frame.py`: `vanilla()` through
  `spaces_for`, and the Page Task's `page_task_spaces`), and whether each names a skill
- each skill's folder in `Tools/`, found by name: its `SKILL.md` version and what it holds (ref ·
  scripts · tests), every skill in `skills/1_base/project/`, and the themes in `skills/2_theme/` and
  `servers/workbench-<theme>/`
- every file of `haipipe-report/`, the example's skill, opened

Typed, since they are the proposal: each button's owning skill and Run name, the skills table's "owns" and
"takes from", the skill × Space grid, the folders after, the plan, and JL's four calls.


Files
-----

```text
s21_project-run-skill/
├── s21_project-run-skill.md            this face
├── build_s21_project_run_skill.py      the builder; fills the `@` lines of the frames yaml from disk; marks are kept
├── s21_project-run-skill.excalidraw    the drawing: a tree frame and two box frames joined by arrows
├── s21_project-run-skill.png           its preview
└── history/                            the 261007, 261012 and 261012b (three folder trees) builders, previews and faces
```

Rebuild: `python build_s21_project_run_skill.py` (or `../_build/make.sh`).


What the drawing holds
----------------------

Three frames (haipipe-studio 0.13.0, JL 261012: trees inside boxes, joined by named arrows, an emoji on every node):

```text
① Background  ──▶  ② 🗺️ the Map                          ③ 📦 Reference
   a tree: words,     boxes per level (🧱 🧩 📄 📝) ─runs─▶     boxes per Tools/ folder, joined
   where it sits      boxes per skill group; red dashed          by names · opens · sits over
                      "? named by no button" (haipipe-delivery)
```

1. **① Background**: a tree: what the topic is about, the screen in one minute, the words, where it sits.
2. **② the Map**: a box per level (Block, Job, Task, Page Task), a tree of its buttons, each with its skill,
   read from `frame.py`; boxes for the skills (of one level, of a shared Space, of a Page, haipipe-delivery);
   "runs" arrows; a red dashed arrow for the skill no button names (Open 1).
3. **③ Reference**: `Each skill is one folder in Tools/`, read from disk: servers, the themes, the base skills
   (version, what each holds), the others, and `haipipe-report/` opened file by file.


The frames (structure here; a tree line starting `@` is filled from disk on every build):

```yaml
frames:
- title: 🧭 Background, which skill each button runs
  intro: The words this topic uses, and where it sits. The map is the next frame.
  cols: 2
  tree:
  - 🎯 What this topic is about:
    - ✅ Every Run button on the base workbench screen names one skill; this topic lists them all
    - ✅ {total} buttons in frame.py across four levels (Block, Job, Task, Page Task); {named} name a skill
    - ✅ JL 261007, "what skill we should have for the studio and for the report ... we need to update the skills a lot"
    - 🔗 b16 s21-paper-run-skill is the paper's counterpart of this topic
  - 🖥️ The screen in one minute:
    - 🧱 a level is the folder you stand in (Block, Job or Task; a Page Task is a Task that writes one Page)
    - 🗂️ a Space is a tab of that level (Description, Studio, Report, Work, Runs, Delivery)
    - ▶️ a Space holds Run buttons; pressing one opens a Run, a folder in runs/
    - 🧰 the Run is made by the skill the button names
  - 📖 Words it uses:
    - 🧰 skill = a folder in Tools/ whose SKILL.md says what it owns; Claude reads it first
    - ▶️ Run = one folder in runs/; a soft Run writes a report, a hard Run writes evidence
    - 🔁 pass = a new round on the same Run target, passes/pNN-MMDD/
    - 🎨 theme = the kind of Block (work, cowork, paper ...); it keeps its own skills over the base
  - 📍 Where it sits:
    - 💻 servers/workbench/frame.py gives each button its skills field (s21-D02)
    - 📐 the whole Run contract is s06-run-workbench-skill
    - 📊 feeds the Questions q05_skill_per_level and q08_workbench_base
  - 🧭 How to read the next two frames:
    - 🗺️ ② the Map, a box per level with its buttons, a box per skill group, arrows named "runs"
    - ❓ a red dashed arrow is a link not recorded yet
    - 📦 ③ each skill as one folder in Tools/, read from disk
- title: 🗺️ Every button runs one skill
  intro: A level's buttons (left and right) run the skills in the middle. Read from frame.py; a red dashed arrow is a skill no button names.
  boxes:
  - id: block
    at: [0, 0]
    title: 🧱 Block
    why: "{nblock} buttons; holds Jobs, Questions, Studio"
    tree: ["@level:Block"]
    most: 1
  - id: job
    at: [0, 1]
    title: 🧩 Job
    why: "{njob} buttons; holds Tasks in order"
    tree: ["@level:Job"]
    most: 1
  - id: task
    at: [2, 0]
    title: 📄 Task
    why: "{ntask} buttons; one piece of work"
    tree: ["@level:Task"]
    most: 1
  - id: page
    at: [2, 1]
    title: 📝 Page Task
    why: "{npage} buttons; writes one Page"
    tree: ["@level:Page Task"]
    most: 1
  - id: own
    at: [1, 0]
    title: 🧱 Skills of one level
    why: One per level, plus asking; each owns a face
    tree: ["@skills:haipipe-block,haipipe-job,haipipe-task,haipipe-question"]
    most: 1
  - id: shared
    at: [1, 1]
    title: 🗂️ Skills of a shared Space
    why: Same skill at every level, so they behave alike
    tree: ["@skills:haipipe-studio,haipipe-report,haipipe-run"]
    most: 1
  - id: draft
    at: [3, 1]
    title: 📝 Skills of a Page
    why: Only a Page Task presses these
    tree: ["@skillsb:haipipe-draft-scratch,haipipe-draft-structure,haipipe-draft-evidence,haipipe-draft-writing,haipipe-draft-revise,haipipe-draft-delivery,haipipe-draft-check,haipipe-display"]
    most: 1
  - id: delivery
    at: [3, 0]
    title: 📤 haipipe-delivery
    why: For Block/delivery/ (s02-D14); no button names it
    tree: ["@skills:haipipe-delivery"]
    most: 1
  arrows:
  - {from: block, to: own, label: runs}
  - {from: job, to: shared, label: runs}
  - {from: task, to: own, label: runs}
  - {from: page, to: draft, label: runs}
  - {from: task, to: delivery, label: "? named by no button", dashed: true}
- title: 📦 Each skill is one folder in Tools/
  intro: The button names the skill; the skill is a folder. Its SKILL.md says what it owns, its scripts do the work. Read from disk.
  boxes:
  - id: servers
    at: [0, 1]
    title: 🖥️ servers/
    why: The screen's code; it is where each button gets its skill name
    tree: ["@tools:servers"]
    most: 1
  - id: themes
    at: [0, 0]
    title: 🎨 skills/2_theme/
    why: A theme keeps its own skills over the base
    tree: ["@tools:themes"]
    most: 1
  - id: base
    at: [1, 0]
    title: 🧰 skills/1_base/project/ (haipipe-<name>)
    why: The base, one skill per level and per shared Space; each is linked from ~/.claude/skills/ on every machine
    tree: ["@tools:base"]
    most: 2
  - id: others
    at: [1, 1]
    title: 📦 skills/1_base/ the others
    why: The rest of the skills the buttons name
    tree: ["@tools:others"]
    most: 2
  - id: report
    at: [2, 0]
    title: 📝 haipipe-report/ opened
    why: The example's skill, file by file
    tree: ["@tools:report"]
    most: 1
  arrows:
  - {from: servers, to: base, label: names}
  - {from: servers, to: others, label: names}
  - {from: themes, to: base, label: sits over}
  - {from: base, to: report, label: opens}
```


Finding (read 261010, the folders 261011)
-----------------------------------------

42 of 42 buttons name their skill: Block 9 · Job 9 · Task 9 · Page Task 15 (on 261007: 12 of 49), 21
rows once a button is counted once across levels. Every level has a Description button and a Studio
button; the Studio one opens the Block's shared Studio. Work Details is called Work on screen. (An earlier
read showed no Description button: the probe folders had no face; fixed 261010.)

In `Tools/` (261011): the buttons name 15 skills. Five of them are among the seven in
`plugins/haipipe-toolkit/skills/1_base/project/`; `haipipe-question` and `haipipe-task` sit in `1_base/question/`
and `1_base/task/`; the Page Task's seven draft skills in `1_base/page/workflow-runs/`, and `haipipe-display`
in `1_base/display/`. Each reaches Claude
through a link, `~/.claude/skills/<name>`. `haipipe-delivery` (0.2.2) is there but no button names it, and
it holds only its `SKILL.md`: the Block's and Job's Delivery buttons name `haipipe-block` and `haipipe-job`
(Open 1).


Proposed (261007)
-----------------

s21-D01 · Proposed (JL 261007): the base skills are one per level and one per shared Space; each theme keeps
    its own skills over them, as its `<theme>_theme.py` does over the frame.

```text
              Description    Studio          Report            Work            Runs          Delivery
Block    ─▶   haipipe-block  haipipe-studio  haipipe-report    haipipe-block   haipipe-run   haipipe-block ?
Job      ─▶   haipipe-job    haipipe-studio  haipipe-report    haipipe-job     haipipe-run   haipipe-job ?
Task     ─▶   haipipe-task   haipipe-studio  haipipe-report*   haipipe-task    haipipe-run   haipipe-draft-delivery
Guide    ─▶   workbench-<theme>
```

    - haipipe-block (new; the deleted one's name): the Block's face and question register, its Spaces, a
      new-Block scaffold, how a theme claims a Block (`Theme.claims`).
    - haipipe-job (new): the Job's face, its Tasks in order, a new-Job scaffold, a theme's own Job names.
    - haipipe-task: not touched (JL 261007: "you should not touch the haipipe-task"); the Task level's
      buttons name it as they are. `skills/1_base/task/` keeps every folder: the task kinds (1_data …
      10_page), agents, page-types, haipipe-task, haipipe-workflow, haipipe-page-task.
    - haipipe-studio (new): `studio/sNN-<topic>/` at any level, its face and builders that keep marks, the
      numbering (s0x concepts · s1x levels · s2x runs and skills · s3x Guide · s5x server), sessions as passes
      of `run-draw-<sNN>`; takes the scratch mode of excalidraw-report and `canvas.py` · `render_png.py`.
    - haipipe-report (new; JL 261007: "to define the question - work - report workflow in the Audience
      report"): the Question │ Work │ Report row at any level, what each cell reads, how work links to a
      question (`answers:` on a Job or Task face, a need id like `QK10.E1`), the walk open → partial →
      answered (→ checked, proposed), the report Page (Opening · Answer · Evidence · Limits · Next), its
      `## Figures` and drawing; a comments batch is a report kind (b16). haipipe-question keeps the asking.
    - haipipe-run (extended): names without `<MMDD>`, `run.yaml` as the Runs Space reads it, a Run type table
      per Space that names each button's skill.

s21-D02 · Proposed: every frame button names its skill (a `skills:` field on its run type), as the Page's run
    cards already do; `Update the description` → the level's skill, `Add a topic` → haipipe-studio,
    `Write the report` → haipipe-report, `Run` → haipipe-run.

s21-D03 · Decided (261007): Block and Job delivery stay in their level skills (haipipe-block,
    haipipe-job), following the theme's delivery rule; a Page Task's is haipipe-draft-delivery's. No
    haipipe-delivery until a theme's Block delivery needs more than the level skill holds. Reason: no
    Block or Job delivers anything yet, so a separate skill would have nothing to build.

s21-D04 · Decided (261007): "checked" is not a fourth answer state. The walk stays open → partial →
    answered; the report Page's own CHECK verdict (run-check-<qNN>) is shown beside answered.
    Reason: the walk says where the answer stands, a check judges one version of the Page; one fact
    lives in one place.


s21-D05 · Decided (JL 261010): s21 is drawn as one story, four frames joined by arrows, each with its
    sentence; the reference table sits below the story, off its path. The 261007 tables (the skill folders
    before and after, the update plan) were finished work and stay in history/.
s21-D06 · Decided (JL 261011: "we also need to show what is the skill folder looks like ... in the Tools/
    what are the folders related to this"): a frame under ② shows each skill as its folder in `Tools/`,
    read from disk on every build, with the example's skill (`haipipe-report/`) opened file by file; an
    arrow from ② says "each skill is one folder in Tools/".
s21-D07 · Decided (JL 261012: "yes, rename haipipe-board to haipipe-block"): the Block's skill is named
    after its level, haipipe-block beside haipipe-job and haipipe-task (2.1.0). `aliases: [haipipe-board]`
    keeps the old name working; haipipe-board-reviewer-agent is now haipipe-block-reviewer-agent. The face
    file stays `board.md` for now: renaming it touches every Block and every reader, a separate step.

s21-D08 · Decided (JL 261012, through the b10 watcher: "go ahead and do all"): the drawing is three frames,
    each a folder tree: ① Background, ② the Tree, ③ the reference, each skill as one folder in Tools/; the old
    frames are folded in; the old builder, face and preview are in history/.

s21-D09 · Decided (JL 261012, through the b10 watcher): the drawing is boxes with trees joined by named arrows, an emoji on every node (haipipe-studio 0.13.0); the old builder, face and preview are in history/ (-261012b).


Built (261007)
--------------

✎ 261007 the five skills exist and every frame button names one (phases 1-4); phase 5 moved `canvas.py`,
`render_png.py` and `build_report_drawing.py` into the skills; folder moves went to b04. The full record,
with each phase, is `history/s21_project-run-skill-261007.md`.


Open
----

1. s21-D03 kept delivery in the level skills because no Block or Job delivered yet. Now every output is
   stored in Block/delivery/ (s02-D14) and Delivery has its own skill, haipipe-delivery: re-decide D03.
2. What must each level's report answer? The Studio sets it, each level reports (meeting 261010).
3. A Job holds soft Runs only: where does a batch launch, run-launch-<group>, go? (s06 open 2)

(write here, or mark the drawing in red)
