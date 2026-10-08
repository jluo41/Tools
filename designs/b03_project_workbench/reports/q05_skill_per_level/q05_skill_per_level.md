# Which skill owns each level?
state: 🟡 DRAFT · written from b03 s21's built result in run-report-q05; CHECK pending
content: draft v0.1 · adopted 261008 0040
answers: Q05
answer-status: partial
results-read: 2026-10-08T00:40:00-04:00

## Opening

Separate level skills, not one door with sub-skills: haipipe-board owns the Block, haipipe-job the Job and haipipe-task the Task, while the Spaces every level shares have one skill each (haipipe-studio, haipipe-question and haipipe-report, haipipe-run); haipipe-folder's place is still to be written.

**Where this Page sits:** [Q05 · How should the skills line up with the ladder: one haipipe-project door with a sub-skill per level (theme, block, job, task, run), separate level skills, or one skill with sub-commands; and where do haipipe-board, haipipe-folder, haipipe-task and haipipe-run go?](../../board.md).

**Why it matters:** Every button of the workbench frame needs one skill that answers it; without an owner per level and per Space, a button copies a prompt that no skill answers.

## Content

### 1 · Answer

The skills line up with the ladder as separate level skills, not as one haipipe-project door with a sub-skill per level: haipipe-board owns the Block, haipipe-job the Job, and haipipe-task the Task, each with its face, its scaffold and its level's own buttons. <!-- realizes: C1.P1.B1 -->
The Spaces every level shares have one skill each at every level: haipipe-studio the Idea Studio, haipipe-question the asking and haipipe-report the rest of the Audience Report, and haipipe-run the Runs. <!-- realizes: C1.P1.B2 -->
Each theme keeps its own skills over these, the way its theme file sits over the base frame, so the theme owners stay apart from the level owners. <!-- realizes: C1.P1.B3 -->
Of the four skills the question names, haipipe-board returns as the Block skill (the static board site it once built stays retired), haipipe-task is left as it is, haipipe-run is extended with the Run types by Space and a soft-Run writer, and haipipe-folder's place is not yet written. <!-- realizes: C1.P1.B4 -->
Every Run button of the frame now names the skill that owns it, through a `skills:` field on its run type. <!-- realizes: C1.P1.B5 -->

### 2 · Evidence

The level and Space skills are [haipipe-board](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-board/SKILL.md), [haipipe-job](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-job/SKILL.md), [haipipe-studio](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/SKILL.md) and [haipipe-report](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-report/SKILL.md), each with its contract, scripts and tests. <!-- realizes: C2.P2.B1 -->
The button table is haipipe-run's [run-types-by-space](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-run/ref/run-types-by-space.md), and the frame sets each button's skill in [frame.py](../../../../plugins/haipipe-toolkit/servers/workbench/frame.py). <!-- realizes: C2.P2.B2 -->
The [s21 topic](../../studio/s21_project-run-skill/s21_project-run-skill.md) reads the frame back at build time and finds every button naming its owner; its face records the decisions on delivery and on the answer states. <!-- realizes: C2.P2.B3 -->

### 3 · Limits

haipipe-folder is not placed: the register asks where it goes, and s21 did not decide it. <!-- realizes: C3.P3.B1 -->
Where these skills finally sit, and any renames, were handed to the skill-folder design Block. <!-- realizes: C3.P3.B2 -->
Page Tasks still write their Runs in the older layout, which the level skills cannot fix; that is the Page engine's change. <!-- realizes: C3.P3.B3 -->

### 4 · Next

Decide whether haipipe-folder's Page Face and Task Face contract folds into the level skills or stays its own. <!-- realizes: C4.P4.B1 -->
Check this report in a fresh context before it is called answered. <!-- realizes: C4.P4.B2 -->
