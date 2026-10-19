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
  `spaces_for`, and the Page Task's `draft_task_spaces`), and whether each names a skill
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
├── build_s21_project_run_skill.py      the builder; reads frame.py's buttons; marks are kept on rebuild
├── s21_project-run-skill.excalidraw    the drawing: one story in four frames, then three below
├── s21_project-run-skill.png           its preview
└── history/                            the 261007 builder, preview and face (six tables in one column)
```

Rebuild: `python build_s21_project_run_skill.py` (or `../_build/make.sh`).


What the drawing holds
----------------------

One sentence, told left to right by four frames joined with arrows (JL 261010: "arrange the display
with a sentence of telling stories by arranging the frames, and use --> to connect the frames"):

```text
① you press a button --names--> ② it names one skill --opens--> ③ the skill opens one Run
   --writes--> ④ the Run writes into one folder, and its Space shows it

   Still open (red)    Each skill is one folder in Tools/ (under ②)    Every button, for reference
```

1. **① Press**: the frame's two button rows as they are today, and the Runs panel of the example,
   Job › Report › "write the report"; the button count, read from `frame.py`.
2. **② Skill**: level × Space → the skill each button names, read from `frame.py`; the example cell boxed.
3. **③ Run**: a soft Run's folder and a hard Run's folder; the whole Run contract is `../s06-run-workbench-skill/`.
4. **④ Folder**: the Block tree, who writes each folder and which Space shows it.
5. **Below**: the open points in red; under ②, each skill as a folder in `Tools/` (where it sits, its
   version, what it holds, the buttons that name it) and `haipipe-report/` opened file by file; and every
   button: one row each, a column per level naming its skill.


Finding (read 261010, the folders 261011)
-----------------------------------------

42 of 42 buttons name their skill: Block 9 · Job 9 · Task 9 · Page Task 15 (on 261007: 12 of 49), 21
rows once a button is counted once across levels. Every level has a Description button and a Studio
button; the Studio one opens the Block's shared Studio. Work Details is called Work on screen. (An earlier
read showed no Description button: the probe folders had no face; fixed 261010.)

In `Tools/` (261011): the buttons name 15 skills. Five of them are among the seven in
`plugins/haipipe-toolkit/skills/1_base/project/`; `haipipe-report` is in `1_base/project/` and `haipipe-task` in `1_base/task/`; the Page Task's seven draft skills in `1_base/draft/workflow-runs/`, and `haipipe-display`
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
      10_evidence), agents, page-types, haipipe-task, haipipe-workflow, haipipe-page-task.
    - haipipe-studio (new): `studio/sNN-<topic>/` at any level, its face and builders that keep marks, the
      numbering (s0x concepts · s1x levels · s2x runs and skills · s3x Guide · s5x server), sessions as passes
      of `run-draw-<sNN>`; takes the scratch mode of excalidraw-report and `canvas.py` · `render_png.py`.
    - haipipe-report (new; JL 261007: "to define the question - work - report workflow in the Audience
      report"): the Question │ Work │ Report row at any level, what each cell reads, how work links to a
      question (`answers:` on a Job or Task face, a need id like `QK10.E1`), the walk open → partial →
      answered (→ checked, proposed), the report Page (Opening · Answer · Evidence · Limits · Next), its
      `## Figures` and drawing; a comments batch is a report kind (b16). haipipe-report keeps the asking.
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
