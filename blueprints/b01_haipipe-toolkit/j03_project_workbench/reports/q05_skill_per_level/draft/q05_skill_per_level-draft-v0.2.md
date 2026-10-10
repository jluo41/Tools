# q05_skill_per_level · draft v0.2
draft-version: v0.2
supersedes: v0.1
date: 261008
approved: ✅ 261008 (JL: "approve v0.2")
status: adopted · revises v0.1 after its CHECK (run-check-q05 p01-1008: CONTENT, eight findings)
arc: One skill per level; the shared Spaces have their own; the levels around them keep theirs.

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Answer
- C1.P1 · Separate level skills; the shared Spaces have their own
- C2 · Evidence
- C2.P2 · The skills, the frame and s21
- C3 · Limits
- C3.P3 · What is not settled
- C4 · Next
- C4.P4 · What to do next

### C1.P1 · Separate level skills; the shared Spaces have their own
- B1 · [Answer] Separate level skills, not one door with sub-skills.
  Note: Block board, Job job, Task task.
  Evidence: frame.py LEVEL_SKILL
- B2 · [Detail] The shared Spaces have their owners at every level.
  Note: studio; question and report; run. (check finding 1: Audience Report has two)
  Evidence: run-types-by-space rule 3
- B3 · [Detail] Themes keep their own skills over these.
  Note: as a theme file does over the frame.
  Evidence: run-types-by-space rule 5
- B4 · [Detail] The levels around them keep their owners.
  Note: Project haipipe-project, Run haipipe-run, Theme its own skills, Page Task buttons haipipe-page-*. (finding 3)
  Evidence: haipipe-project SKILL, run-types-by-space
- B5 · [Owner] Where the four named skills went.
  Note: board reused, task's role kept (paths fixed 261007), run extended, folder open. (finding 2)
  Evidence: the four SKILL.md files
- B6 · [Detail] Every frame button names its skill.
  Note: a skills field on each run type.
  Evidence: frame.py run_type

### C2.P2 · The skills, the frame and s21
- B1 · [Evidence] The level and Space skills.
  Note: board, job, studio, question, report, run, task, project. (finding 7)
- B2 · [Evidence] The button table and the frame.
- B3 · [Evidence] s21 reads it back from disk; its two frames are the figures. (finding 8)

### C3.P3 · What is not settled
- B1 · [Limit] haipipe-folder's place is not written.
- B2 · [Limit] Where the skills finally sit is b04's.
- B3 · [Limit] Page Tasks still write Runs the old way; the audit calls it debt. (finding 6: link ladder.md)
- B4 · [Limit] haipipe-task still routes to old owners. (finding 2)
  Note: board rendering to haipipe-page; Block reports through haipipe-question. Not touched (JL 261007).

### C4.P4 · What to do next
- B1 · [Next] Decide haipipe-folder against the level skills.
- B2 · [Next] Update haipipe-task's routing when it may be touched.
- B3 · [Next] Check this report again in a fresh context.

## 2 · Draft

### C1.P1
The skills line up with the ladder as separate level skills, not as one haipipe-project door with a sub-skill per level: haipipe-board owns the Block, haipipe-job the Job, and haipipe-task the Task, each with its face, its scaffold and its level's own buttons.
The Spaces every level shares have their owners at every level: haipipe-studio the Idea Studio, haipipe-question (the asking) and haipipe-report (the rest) the Audience Report, and haipipe-run the Runs.
Each theme keeps its own skills over these, the way its theme file sits over the base frame, so the theme owners stay apart from the level owners.
The levels around them keep their owners: haipipe-project the Project root, haipipe-run each Run, and each theme's own skills its Theme, Guide included; a Page Task's own buttons belong to the haipipe-page skills.
Of the four skills the question names, haipipe-board returns as the Block skill (the static board site it once built stays retired), haipipe-task keeps its role (only its paths were fixed on 261007), haipipe-run is extended with the Run types by Space and a soft-Run writer, and haipipe-folder's place is not yet written.
Every Run button of the frame now names the skill that owns it, through a `skills:` field on its run type.

### C2.P2
The level and Space skills are haipipe-board, haipipe-job, haipipe-studio, haipipe-question and haipipe-report; haipipe-task, haipipe-run and haipipe-project hold the levels around them.
The button table is haipipe-run's run-types-by-space reference, and the frame sets each button's skill in frame.py.
The s21 topic reads the frame back at build time and finds every button naming its owner; two of its frames are this report's figures.

### C3.P3
haipipe-folder is not placed: the register asks where it goes, and s21 did not decide it.
Where these skills finally sit, and any renames, were handed to the skill-folder design Block.
Page Tasks still write their Runs in the older layout, which the ladder audit reports as debt; that is the Page engine's change, not the level skills'.
haipipe-task still says Board rendering belongs to haipipe-page and routes a Block report through haipipe-question; it was left untouched on purpose, so its routing trails the new owners.

### C4.P4
Decide whether haipipe-folder's Page Face and Task Face contract folds into the level skills or stays its own.
Update haipipe-task's routing to name haipipe-board and haipipe-report once it may be touched.
Check this report again in a fresh context before it is called answered.
