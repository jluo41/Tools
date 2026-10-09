s21 · Project Run and skill
===========================

**Topic:** every Run button of the base frame, by level and Space, the skill that should own it, and the
plan to update the base skills so every button has one (JL 261007: "what skill we should have for the studio
and for the report … I think we should have the haipipe-board, and haipipe-job, and also haipipe-studio and
haipipe-report, and haipipe-run … we need to update the skills a lot"). The base's counterpart of b16's
`s21-paper-run-skill`, in its style: lines-only tables, ink and gray, red for what is open, green ✎ for what
changed.

**Feeds:** `reports/` q05_skill_per_level · q08_workbench_base.

**Source:** read from disk on every build:

- the base frame's Run buttons per level and Space (`servers/workbench/frame.py`: `vanilla()` through
  `spaces_for`, and the Page Task's `page_task_spaces`), and whether each names a skill
- each skill's version and size from its `SKILL.md`, found by name
- the skill folders of `1_base/project` · `task` · `question` · `page/workbench-studio` ·
  `display/excalidraw-report`, and the studio scripts in this Block's `_build/`

Typed, since they are the proposal: each button's owning skill and Run name, the skills table's "owns" and
"takes from", the skill × Space grid, the folders after, the plan, and JL's four calls.


Files
-----

```text
s21_project-run-skill/
├── s21_project-run-skill.md            this face
├── build_s21_project_run_skill.py      the builder; reads the frame and the skills; marks are kept on rebuild
├── s21_project-run-skill.excalidraw    the drawing: five frames
└── s21_project-run-skill.png           its preview
```

Rebuild: `python build_s21_project_run_skill.py` (or `../_build/make.sh`).


What the drawing holds
----------------------

```text
1 · Runs by level and Space   every Run button the frame draws, Block · Job · Task · Page Task: Space · button ·
                              names a skill today · proposed skill · its Run's name
2 · The skills                one per level, one per shared Space: today's version (read) · owns · takes from
3 · skill × Space             who owns each Space at each level; Guide is each theme's
3b · Question │ Work │ Report  the row each Audience Report draws (what each cell reads, its owner), and
                              the walk open → partial → answered → checked, counted from disk
4 · skill folders             today (read from disk) → proposed
5 · skill update plan         six phases, and JL's four calls
```


Finding (261007)
----------------

12 of 49 Run buttons name a skill today: only the Page Task's Work Details and Delivery buttons, which come
from the Page's run-cards.md. Every button the frame draws itself (Description, Idea Studio, Audience Report,
Work Details, Runs and Delivery, at Block, Job and Task) copies a plain prompt that no skill answers. The
studio and report tools are split: `canvas.py` and `render_png.py` live in this Block's `_build/`, which every
theme's design Block imports; `build_report_drawing.py` now sits in `excalidraw-report/ref/`. No skill owns
the Block level since `haipipe-board` was deleted (261005).


Proposed (261007)
-----------------

s21-D01 · Proposed (JL 261007): the base skills are one per level and one per shared Space; each theme keeps
    its own skills over them, as its `<theme>_theme.py` does over the frame.

```text
              Description    Idea Studio     Audience Report   Work Details    Runs          Delivery
Block    ─▶   haipipe-board  haipipe-studio  haipipe-report    haipipe-board   haipipe-run   haipipe-board ?
Job      ─▶   haipipe-job    haipipe-studio  haipipe-report    haipipe-job     haipipe-run   haipipe-job ?
Task     ─▶   haipipe-task   haipipe-studio  haipipe-report*   haipipe-task    haipipe-run   haipipe-page-delivery
Guide    ─▶   workbench-<theme>
```

    - haipipe-board (new; the deleted one's name): the Block's face and question register, its Spaces, a
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

s21-D03 · Decided (261007): Block and Job delivery stay in their level skills (haipipe-board,
    haipipe-job), following the theme's delivery rule; a Page Task's is haipipe-page-delivery's. No
    haipipe-delivery until a theme's Block delivery needs more than the level skill holds. Reason: no
    Block or Job delivers anything yet, so a separate skill would have nothing to build.

s21-D04 · Decided (261007): "checked" is not a fourth answer state. The walk stays open → partial →
    answered; the report Page's own CHECK verdict (run-check-<qNN>) is shown beside answered.
    Reason: the walk says where the answer stands, a check judges one version of the Page; one fact
    lives in one place.


Built (261007)
--------------

✎ 261007 the plan's phases 1-4 are built; frame 5 reads each phase's state from disk.

```text
skills/1_base/project/
├── haipipe-board/    2.0.0  ref/board-contract.md · scripts/new_board.py · tests (7)
├── haipipe-job/      0.1.0  ref/job-contract.md · scripts/new_job.py (job · task · check) · tests (7)
├── haipipe-studio/   0.1.0  ref/topic-contract.md · scripts/canvas.py · render_png.py · new_topic.py · tests (7)
├── haipipe-report/   0.1.0  ref/report-contract.md · scripts/build_report_drawing.py · check_report.py · tests (15)
└── haipipe-run/      0.32.0 + ref/run-types-by-space.md · scripts/soft_run.py · tests (6)
skills/1_base/question/haipipe-question/   0.6.0, asking only; its report part points to haipipe-report
```

1. Every frame button names its skill (s21-D02): `frame.py`'s run types carry `skills:`; frame 1
   reads them back, and `_host/tests/test_frame.py` checks each named skill exists.
2. ✎ 261007 phase 5: `canvas.py` and `render_png.py` left this Block's `_build/`, and
   `build_report_drawing.py` left `excalidraw-report/ref/`. All 36 builders that import canvas
   (b03, b04, b11-b17) load it from haipipe-studio; every `make.sh` and studio note names the skills'
   scripts; the two older snapshots kept in `_build/` moved beside their drawings.
3. The frame's Work column reads a need, `answers: <id>.E<n>`, as its Question (haipipe-report's
   link rule).
4. ✎ 261007 the two open calls are decided (s21-D03, s21-D04); folder moves are handed to b04.
5. ✎ 261008 slide drafts moved out of haipipe-studio into a new `excalidraw-slide` (beside
   excalidraw-report); haipipe-studio enforces its look (black, red = open, green = change) in
   `canvas.write`, slide drafts exempt. Sessions of this topic are passes of `runs/run-draw-s21/`.


Plan (proposed 261007)
----------------------

1. haipipe-board · haipipe-job: faces, registers, scaffolds.
2. haipipe-studio: the topic contract; `canvas.py` and `render_png.py` move into it; every design Block's
   builders import them from the skill.
3. haipipe-report: the report Page and its figures; `build_report_drawing.py` moves in from
   `excalidraw-report/ref/`.
4. haipipe-run: names, the card, the Run type table per Space; the frame's buttons carry their skill.
5. All, with design_b04_skill_folder: old words out, folder moves and renames. The proposal only adds
   skills; nothing in `skills/1_base/task/` is moved or deleted.


Settled (261007)
----------------

- Decided (JL 261007): haipipe-task is not touched.
- Decided (261007, s21-D03): Delivery stays in each level skill; the Page Task's in haipipe-page-delivery.
- Decided (JL 261007): haipipe-report defines the Question │ Work │ Report workflow; haipipe-question
   keeps the asking. Decided (261007, s21-D04): "checked" is not a fourth state.
- Handed to design_b04_skill_folder (261007): where the new skills finally sit, and any renames.


Open
----

None in s21: the folder moves are b04's call (handed over 261007).

(write here, or mark the drawing in red)
