# s52 Board UI: Work · the cell as a whole · stage 1 · r01

```text
letter      mean   result    lowest rubric
A Answers   7.1    not yet   Salience 4
B Tracks    7.6    not yet   One job 6, Salience 6
C Jobs      7.9    not yet   Lean 7, One job 7, Same look 7, Salience 7
D Data      8.0    not yet   Salience 6
E Handoff   7.7    not yet   Salience 6
```

## Does each letter belong

1. A as drawn does not earn its place: one agent Run and "Waits on you: nothing".
2. B is named Tracks but holds proposals; its content and its name disagree.
3. C belongs, but lacks the Jobs themselves; a Block's Work lists its Jobs (haipipe-ui, The page at each level).
4. D and E belong; both are action buttons with no picture of what they act on.
5. Nothing is redundant, but the four 🙋 signs are spread over B, C and E, so no single place answers "what waits on me".

## Pairing with Report (s51)

Shared letters work for C, D and E. A and B do not pair: Report A shows answers, Work A shows an empty inbox; Report B shows tracks, Work B shows a triage count. The agreed design intent (s52-D01: "Work opens on what waits on the person") is not met by the drawing: Work opens on A, whose first and largest line is "nothing".

## Further improvements (beyond the rubric fixes)

1. Make Work A's section 1 the Board's whole 🙋 inbox (Sign AP2, Close j03, Triage proposals, Sign the handoff), each with ready or not ready and one verb; agent work goes below, smaller. Why: it meets s52-D01 without undoing the shared letters.
2. Answer Open question 1 ("Sign AP2 here, or only in the Prototype"): only in the Prototype; the Board shows the 🙋 row with "Open in Prototype". Same for Triage. Why: signing a release and triage are the Prototype's Runs (run-sign-release-pN, run-triage-proposals-pN), and AGENTS.md says one owner per page.
3. Show each Job as a row in C with its pipeline as a short chain (Runs ✅ · pages ⏳ 12 · checks ⬜ 3 · close 🙋). Why: the person needs to see why Close j03 is not ready yet, and Report C's grid holds no progress.
4. Replace every generic "Run" with the action's verb (Write, Propose, Draft) and remove the Run ids (run-propose-j03, run-draft-handoff) and rule sentences. Why: three of five views lose Lean and Words for the same reason.
5. Order rows by when they can be done: a 🙋 row that cannot be done yet says "not ready" and sits under the step it waits on. Why: E shows Sign above Draft, the reverse of the real order.

(reviewer: a fresh general-purpose agent, 261101)
