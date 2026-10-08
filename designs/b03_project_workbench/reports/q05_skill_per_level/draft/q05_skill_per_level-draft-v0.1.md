# q05_skill_per_level · draft v0.1
draft-version: v0.1
supersedes: none
date: 261008
approved: ⬜
status: working · written from b03 s21's built result in run-report-q05
arc: One skill per level, one per shared Space; themes keep their own over them.

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Answer
- C1.P1 · Separate level skills, one per shared Space
- C2 · Evidence
- C2.P2 · The skills, the frame and s21
- C3 · Limits
- C3.P3 · What is not settled
- C4 · Next
- C4.P4 · What to do next

### C1.P1 · Separate level skills, one per shared Space
- B1 · [Answer] Separate level skills, not one door with sub-skills.
  Note: Block board, Job job, Task task.
  Evidence: none · reads the files linked under Evidence
- B2 · [Detail] One skill per shared Space at every level.
  Note: studio, question and report, run.
  Evidence: none · reads the files linked under Evidence
- B3 · [Detail] Themes keep their own skills over these.
  Note: as a theme file does over the frame.
  Evidence: none · reads the files linked under Evidence
- B4 · [Owner] Where the four named skills went.
  Note: board reused, task untouched, run extended, folder open.
  Evidence: none · reads the files linked under Evidence
- B5 · [Detail] Every frame button names its skill.
  Note: a skills field on each run type.
  Evidence: none · reads the files linked under Evidence

### C2.P2 · The skills, the frame and s21
- B1 · [Evidence] The new skills and their contracts.
  Note: board, job, studio, report.
  Evidence: none · reads the files linked under Evidence
- B2 · [Evidence] The button table and the frame.
  Note: run-types-by-space, frame.py.
  Evidence: none · reads the files linked under Evidence
- B3 · [Evidence] s21 reads it back from disk.
  Note: every button names its owner.
  Evidence: none · reads the files linked under Evidence

### C3.P3 · What is not settled
- B1 · [Limit] haipipe-folder's place is not written.
  Note: the register asks for it.
  Evidence: none
- B2 · [Limit] Where the skills finally sit is b04's.
  Note: folder moves handed over.
  Evidence: none
- B3 · [Limit] Page Tasks still write Runs the old way.
  Note: haipipe-page, not the level skills.
  Evidence: none

### C4.P4 · What to do next
- B1 · [Next] Decide haipipe-folder against the level skills.
  Evidence: none
- B2 · [Next] Check this report in a fresh context.
  Evidence: none

## 2 · Draft

### C1.P1
The skills line up with the ladder as separate level skills, not as one haipipe-project door with a sub-skill per level: haipipe-board owns the Block, haipipe-job the Job, and haipipe-task the Task, each with its face, its scaffold and its level's own buttons.
The Spaces every level shares have one skill each at every level: haipipe-studio the Idea Studio, haipipe-question the asking and haipipe-report the rest of the Audience Report, and haipipe-run the Runs.
Each theme keeps its own skills over these, the way its theme file sits over the base frame, so the theme owners stay apart from the level owners.
Of the four skills the question names, haipipe-board returns as the Block skill (the static board site it once built stays retired), haipipe-task is left as it is, haipipe-run is extended with the Run types by Space and a soft-Run writer, and haipipe-folder's place is not yet written.
Every Run button of the frame now names the skill that owns it, through a `skills:` field on its run type.

### C2.P2
The level and Space skills are haipipe-board, haipipe-job, haipipe-studio and haipipe-report, each with its contract, scripts and tests.
The button table is haipipe-run's run-types-by-space reference, and the frame sets each button's skill in frame.py.
The s21 topic reads the frame back at build time and finds every button naming its owner; its face records the decisions on delivery and on the answer states.

### C3.P3
haipipe-folder is not placed: the register asks where it goes, and s21 did not decide it.
Where these skills finally sit, and any renames, were handed to the skill-folder design Block.
Page Tasks still write their Runs in the older layout, which the level skills cannot fix; that is the Page engine's change.

### C4.P4
Decide whether haipipe-folder's Page Face and Task Face contract folds into the level skills or stays its own.
Check this report in a fresh context before it is called answered.
