---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 1
kind: preference
context: authoring
lands_in: "ref/writing-rules.md + haipipe-paper-probe step 5"
session: "the 2026-07-27 MISQ session, §4/§5 + PROBE tail (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
JL, verbatim: "to fix all the things you can fix, right?"

I had reported the eight harvest debts the checker found and then left them, on the grounds that they
were "§4/§6/§7's, not §5's". That was scope-shedding. They were step 5 of the loop I was already
running, they cost nothing and they dispatched nothing.

The rule: if the work is inside the phase you are running and it costs nothing, do it. Section
ownership is not a reason to leave a failing check.

What it turned out to be once done, and the reason it was worth pushing on: two different problems
wearing one error message. Six entries already had populated `a-executor` blocks and had simply never
had `state:` advanced, so the loop only LOOKED open. Two were the hard-fail class, `commissioned` with
an empty a-executor while the answer had already landed, and those held real unread evidence,
including that §5's stated prior-utilization window does not match the windows actually recorded.

Sub-lesson: my own placeholder guard refused one of the six because the word "placeholders" appeared
in legitimate prose. A guard that trips should be READ, not disabled.
