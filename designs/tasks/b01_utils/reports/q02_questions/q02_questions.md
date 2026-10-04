# How are questions recorded and answered?
state: 🟡 DRAFT · written from the 2026-10-03 skill changes; CHECK pending
content: draft v0.1 · adopted 261003 1925
answers: Q02
answer-status: answered
results-read: 2026-10-03T19:25:45-04:00

## Opening

A board question is a topic, kept as `reports/qNN_<topic>/`, that grows into its report; each chat section names one in its last line, a missing one is proposed with its folder, and one skill, `haipipe-question`, owns these rules.

**Where this Page sits:** [Q02 · What is a board question, how big should it be, where does it live, and how does a chat reply link it?](../../board.md).

**Why it matters:** A question sized as a single decision never grows a report, and rules kept in several skills drift apart.

## Content

### 1 · Answer

A board question is a topic that many sections, sessions and Runs feed, kept as `reports/qNN_<topic>/` beside `studio/`, and it grows into its report over time; a narrow decision is one of the things that report records, not a question of its own. <!-- realizes: C1.P1.B1 -->
Every ordinary chat section ends with one Related question line that names the board, the question's QNN and the short topic question, then says why the section serves it; a question that exists only in the session no longer has a form of its own. <!-- realizes: C1.P1.B2 -->
When no recorded question fits, the section writes `(proposed) <Board> "<short question>"` without an id, and the closing Summary and Next offers to create its folder with the board's next free number; nothing is created until the person agrees. <!-- realizes: C1.P1.B3 -->
One skill owns these rules, `haipipe-question` in the new `skills/question/` skillset beside `ask-questions`, and `response-format`, `haipipe-task` and `haipipe-paper` point to it instead of restating them. <!-- realizes: C1.P1.B4 -->

### 2 · Evidence

The question contract, its five size tests and its create steps are in [haipipe-question SKILL.md](../../../../../plugins/haipipe-toolkit/skills/question/haipipe-question/SKILL.md), with the register and report fields in [block-questions.md](../../../../../plugins/haipipe-toolkit/skills/question/haipipe-question/ref/block-questions.md). <!-- realizes: C2.P2.B1 -->
The reply format reached this shape in seven versions dated 2026-10-03, 0.11.0 to 0.17.0, recorded in [response-format CHANGELOG.md](../../../../../plugins/haipipe-toolkit/skills/0_utils/response-format/CHANGELOG.md). <!-- realizes: C2.P2.B2 -->
This question was itself created by `block_questions.py add-question` from its new place under `haipipe-question`, which shows the create path works after the move. <!-- realizes: C2.P2.B3 -->

### 3 · Limits

Whether a question is a topic or a decision is still a judgment against the five tests; no checker flags a question that is too narrow. <!-- realizes: C3.P3.B1 -->
A Paper board has no question register yet: its questions are the Story's research questions, its folders are made by hand, and the helper only accepts a Task Block. <!-- realizes: C3.P3.B2 -->

### 4 · Next

Watch the next replies: when sections keep proposing new questions where a recorded one would serve, the size rule is too loose, and the finding belongs in this report. <!-- realizes: C4.P4.B1 -->
Give Paper boards a question register, so `haipipe-question`'s helper can create their questions as it does on a Task Block. <!-- realizes: C4.P4.B2 -->
