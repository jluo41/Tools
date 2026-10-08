# q02_questions · draft v0.1
draft-version: v0.1
supersedes: none
date: 261003
approved: ⬜
status: working · written from the 2026-10-03 skill changes in run-section
arc: A question is a topic one skill owns, each chat section names one, and a missing one is proposed with its folder.

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Answer
- C1.P1 · A question is a topic with one owner
- C2 · Evidence
- C2.P2 · The skills and their history
- C3 · Limits
- C3.P3 · What the rules cannot do yet
- C4 · Next
- C4.P4 · What to watch and add

### C1.P1 · A question is a topic with one owner
- B1 · [Answer] A board question is a topic, not a decision.
  Note: Kept as reports/qNN_<topic>/ beside studio/.
  Evidence: none · reads the files linked under Evidence
- B2 · [Reason] Each chat section names one question in its last line.
  Note: The Related question line; no Session form.
  Evidence: none · reads the files linked under Evidence
- B3 · [Detail] A missing question is proposed, with its folder.
  Note: Created only on agreement.
  Evidence: none · reads the files linked under Evidence
- B4 · [Owner] One skill owns the question; the others point to it.
  Note: skills/question/ since 2026-10-03.
  Evidence: none · reads the files linked under Evidence

### C2.P2 · The skills and their history
- B1 · [Evidence] haipipe-question holds the size tests and create steps.
  Note: SKILL.md.
  Evidence: none · reads the files linked under Evidence
- B2 · [Evidence] The reply format reached this shape in seven steps.
  Note: CHANGELOG 0.11.0 to 0.17.0.
  Evidence: none · reads the files linked under Evidence
- B3 · [Evidence] This question was created by the moved helper.
  Note: Tests the create path.
  Evidence: none · reads the files linked under Evidence

### C3.P3 · What the rules cannot do yet
- B1 · [Limit] The size tests are judgment, not a check.
  Note: No checker.
  Evidence: none · reads the files linked under Evidence
- B2 · [Limit] Paper boards have no register block.
  Note: Helper is task-block only.
  Evidence: none · reads the files linked under Evidence

### C4.P4 · What to watch and add
- B1 · [Next] Watch replies for proposals that should reuse.
  Note: Feeds this report.
  Evidence: none · reads the files linked under Evidence
- B2 · [Next] Give Paper boards a register.
  Note: So the helper works there.
  Evidence: none · reads the files linked under Evidence

## 2 · Scratch · What to write here

### C1.P1 · A question is a topic with one owner

### C2.P2 · The skills and their history

### C3.P3 · What the rules cannot do yet

### C4.P4 · What to watch and add

## 3 · Draft · Reading and Revise

### C1.P1 · A question is a topic with one owner
- B1 · A board question is a topic that many sections, sessions and Runs feed, kept as `reports/qNN_<topic>/` beside `studio/`, and it grows into its report over time; a narrow decision is one of the things that report records, not a question of its own.
- B2 · Every ordinary chat section ends with one Related question line that names the board, the question's QNN and the short topic question, then says why the section serves it; a question that exists only in the session no longer has a form of its own.
- B3 · When no recorded question fits, the section writes `(proposed) <Board> "<short question>"` without an id, and the closing Summary and Next offers to create its folder with the board's next free number; nothing is created until the person agrees.
- B4 · One skill owns these rules, `haipipe-question` in the new `skills/question/` skillset beside `ask-questions`, and `response-format`, `haipipe-task` and `haipipe-paper` point to it instead of restating them.

### C2.P2 · The skills and their history
- B1 · The question contract, its five size tests and its create steps are in [haipipe-question SKILL.md](../../../../../plugins/haipipe-toolkit/skills/question/haipipe-question/SKILL.md), with the register and report fields in [block-questions.md](../../../../../plugins/haipipe-toolkit/skills/question/haipipe-question/ref/block-questions.md).
- B2 · The reply format reached this shape in seven versions dated 2026-10-03, 0.11.0 to 0.17.0, recorded in [response-format CHANGELOG.md](../../../../../plugins/haipipe-toolkit/skills/0_utils/response-format/CHANGELOG.md).
- B3 · This question was itself created by `block_questions.py add-question` from its new place under `haipipe-question`, which shows the create path works after the move.

### C3.P3 · What the rules cannot do yet
- B1 · Whether a question is a topic or a decision is still a judgment against the five tests; no checker flags a question that is too narrow.
- B2 · A Paper board has no question register yet: its questions are the Story's research questions, its folders are made by hand, and the helper only accepts a Task Block.

### C4.P4 · What to watch and add
- B1 · Watch the next replies: when sections keep proposing new questions where a recorded one would serve, the size rule is too loose, and the finding belongs in this report.
- B2 · Give Paper boards a question register, so `haipipe-question`'s helper can create their questions as it does on a Task Block.
