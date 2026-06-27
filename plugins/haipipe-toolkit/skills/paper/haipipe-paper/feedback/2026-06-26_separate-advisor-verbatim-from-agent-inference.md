---
status: open
created: 2026-06-26
updated: 2026-06-26
occurrences: 1
context: MISQ-Introduction session; agent conflated Gao-exemplar inferences with Ritu Agarwal's actual instructions twice
fixed_in: ""
regressed: ""
---
The agent must SEPARATE what the advisor ACTUALLY SAID (verbatim quotes from feedback.md) from what the agent INFERS from exemplar analysis. Conflating the two misleads the user into accepting an inference as an instruction.

This session, the agent:
1. Attributed "3-beat intro" to Ritu — she never said that; it was the agent's reading of the Gao 2015 exemplar. User caught it: "why you think Ritu wants to say there are 3 beats in the introduction."
2. Attributed "no lit in the intro" to Ritu — she never said that either; her comments #4 and #6 are about the LITERATURE REVIEW section, not a ban on citations in the intro. User caught it: "does ritu mentioned no lit in the introduction?"

Both times the agent presented its own design choice as if it were the advisor's instruction. When the user accepted it, they were accepting a misattribution, not a real constraint. The agent only corrected itself after the user independently questioned it.

Rule: when referencing advisor feedback, always distinguish "Ritu said (verbatim): ..." from "I infer from the exemplars: ...". Never present an inference in the same voice as a verbatim instruction. When the two are combined into a recommendation, label which part is which.

This is a cross-cutting discipline (applies at every stage where advisor feedback is referenced), not a defect in one skill.
