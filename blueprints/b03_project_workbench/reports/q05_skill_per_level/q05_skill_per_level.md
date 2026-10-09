# Which skill owns each level?
state: 🟡 DRAFT · v0.2 adopted; CHECK pending (v0.1's CHECK returned CONTENT)
content: draft v0.2 · approved and adopted 261008 0913 (JL: "approve v0.2")
answers: Q05
answer-status: partial
results-read: 2026-10-08T08:44:01-04:00

## Opening

Separate level skills, not one door with sub-skills: haipipe-board owns the Block, haipipe-job the Job and haipipe-task the Task; the Spaces every level shares have their own owners (haipipe-studio; haipipe-question and haipipe-report; haipipe-run), and the levels around them keep theirs. haipipe-folder's place is still to be written.

**Where this Page sits:** [Q05 · How should the skills line up with the ladder: one haipipe-project door with a sub-skill per level (theme, block, job, task, run), separate level skills, or one skill with sub-commands; and where do haipipe-board, haipipe-folder, haipipe-task and haipipe-run go?](../../board.md).

**Why it matters:** Every button of the workbench frame needs one skill that answers it; without an owner per level and per Space, a button copies a prompt that no skill answers.

## Content

### 1 · Answer

The skills line up with the ladder as separate level skills, not as one haipipe-project door with a sub-skill per level: haipipe-board owns the Block, haipipe-job the Job, and haipipe-task the Task, each with its face, its scaffold and its level's own buttons. <!-- realizes: C1.P1.B1 -->
The Spaces every level shares have their owners at every level: haipipe-studio the Idea Studio, haipipe-question (the asking) and haipipe-report (the rest) the Audience Report, and haipipe-run the Runs. <!-- realizes: C1.P1.B2 -->
Each theme keeps its own skills over these, the way its theme file sits over the base frame, so the theme owners stay apart from the level owners. <!-- realizes: C1.P1.B3 -->
The levels around them keep their owners: haipipe-project the Project root, haipipe-run each Run, and each theme's own skills its Theme, Guide included; a Page Task's own buttons belong to the haipipe-page skills. <!-- realizes: C1.P1.B4 -->
Of the four skills the question names, haipipe-board returns as the Block skill (the static board site it once built stays retired), haipipe-task keeps its role (only its paths were fixed on 261007), haipipe-run is extended with the Run types by Space and a soft-Run writer, and haipipe-folder's place is not yet written. <!-- realizes: C1.P1.B5 -->
Every Run button of the frame now names the skill that owns it, through a `skills:` field on its run type. <!-- realizes: C1.P1.B6 -->

### 2 · Evidence

The level and Space skills are [haipipe-board](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-board/SKILL.md), [haipipe-job](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-job/SKILL.md), [haipipe-studio](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/SKILL.md), [haipipe-question](../../../../plugins/haipipe-toolkit/skills/1_base/question/haipipe-question/SKILL.md) and [haipipe-report](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-report/SKILL.md); [haipipe-task](../../../../plugins/haipipe-toolkit/skills/1_base/task/haipipe-task/SKILL.md), [haipipe-run](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-run/SKILL.md) and [haipipe-project](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/SKILL.md) hold the levels around them. <!-- realizes: C2.P2.B1 -->
The button table is haipipe-run's [run-types-by-space](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-run/ref/run-types-by-space.md) reference, and the frame sets each button's skill in [frame.py](../../../../plugins/haipipe-toolkit/servers/workbench/frame.py). <!-- realizes: C2.P2.B2 -->
The [s21 topic](../../studio/s21_project-run-skill/s21_project-run-skill.md) reads the frame back at build time and finds every button naming its owner; two of its frames are this report's figures. <!-- realizes: C2.P2.B3 -->

### 3 · Limits

haipipe-folder is not placed: the register asks where it goes, and s21 did not decide it. <!-- realizes: C3.P3.B1 -->
Where these skills finally sit, and any renames, were handed to the skill-folder design Block. <!-- realizes: C3.P3.B2 -->
Page Tasks still write their Runs in the older layout, which the [ladder audit](../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-project/ref/ladder.md) reports as debt; that is the Page engine's change, not the level skills'. <!-- realizes: C3.P3.B3 -->
haipipe-task still says Board rendering belongs to haipipe-page and routes a Block report through haipipe-question; it was left untouched on purpose, so its routing trails the new owners. <!-- realizes: C3.P3.B4 -->

### 4 · Next

Decide whether haipipe-folder's Page Face and Task Face contract folds into the level skills or stays its own. <!-- realizes: C4.P4.B1 -->
Update haipipe-task's routing to name haipipe-board and haipipe-report once it may be touched. <!-- realizes: C4.P4.B2 -->
Check this report again in a fresh context before it is called answered. <!-- realizes: C4.P4.B3 -->

## Figures

```yaml
figures:
- from: ../../studio/s21_project-run-skill/s21_project-run-skill.excalidraw
  frame: "2 · The skills"
  caption: the skills, one per level and one per shared Space, and what each owns
- from: ../../studio/s21_project-run-skill/s21_project-run-skill.excalidraw
  frame: "3 · skill × Space"
  caption: who owns each Space at each level
```
