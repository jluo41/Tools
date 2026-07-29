---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 8
kind: defect
context: authoring
lands_in: "check-probe-cards.sh + haipipe-probe SKILL.md"
session: "the 2026-07-27 MISQ session, §4/§5 + PROBE tail (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
Not a JL quote. Found by running `check-probe-cards.sh` for the first time this session.

Eight entries FAILed. Six were `answered-not-read`, and in every one of the six the harvest had
ALREADY HAPPENED: the `### a-executor` carried 7 to 13 lines of transcribed, sourced answer. What was
missing was one word, `state: answered` never advanced to `state: read`.

So the failure was not an un-harvested answer. It was a state field nobody advances, on entries that
look complete to a reader. The checker's own comment concedes the circularity: "`answered-not-read`
fires only AFTER someone advanced the state -- which IS the harvest step."

Two more were worse and are the class the checker calls out as a hard fail:
`commissioned-target-answered`, where the target QA had gone `answered` while the entry's a-executor
was still empty. Real evidence sat on disk unread for days.

The fix is not more checking, it is closing the gap between doing the harvest and recording it. Either
the harvest step writes both at once, or the checker distinguishes "a-executor empty" from
"a-executor populated but state stale" so the second reports as a one-word fix rather than as the
same red as the first.
