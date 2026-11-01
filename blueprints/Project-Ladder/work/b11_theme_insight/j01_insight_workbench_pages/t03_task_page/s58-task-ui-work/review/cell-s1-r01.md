# s58 · Task UI: Work · cell review · stage 1 · r01

Scores: A Answer 8.0 pass (borderline: Lean 7, Words 7, Salience 7) · B By cut 8.4 not yet (Salience 6) · C Across Jobs 8.3 not yet (Salience 4) · D Plan 8.4 not yet (Salience 6).

## Does each letter belong

- A is the chain the design intent asks for (plan, agree, cuts, page, check), but its button says "Answer" and no box carries a state, so "its next step" is never shown.
- B By cut belongs, but shows one Run and drops the not-asked cuts; the Task's grid is missing in Work as well.
- C Across Jobs does not belong at Task level: run-track-<q> is a Board Run in insight-ladder.md's Runs table (rule 12). Recommend removing it, or keeping only "Propose from a change".
- D Plan is doubtful on a Board Task: run-plan-evidence-<l><nn> and run-review-plan-<l><nn> are release (question) Runs, and a signed release is frozen (rule 2). On a Board Task it should read "agreed ✅ in p2" with a Propose a fix verb. Ask JL; the design intent names plan and agree in the chain, so keep them as chain states either way.
- Missing: two Task Runs from the ladder appear nowhere: run-pool-t<NN> (pool or split on Cross) and run-check-alignment-t<NN>.

## Pairing with Report (s57)

Letters and names match. Content does not pair: Work A is not about the answer, Work C is a Board action, Work D repeats work Report D says is done. If C goes, Report keeps four views and Work three; haipipe-ui allows each section its own letters when the lists differ, so dropping the shared lettering is acceptable.

## Further improvements (beyond the rubric fixes)

1. Merge A and B into one cut × step grid, each cell a state word, the next cell outlined with its one verb (Run, Retry, Pool). Why: s58-D01's grid, the chain and the per-cut rows are the same object drawn three ways.
2. Remove "No sign here" and let the absence of 🙋 rows say it. Why: rule 4, no instruction rows; the cell line above the screens already states it.
3. Show only one Run button at a time, on the next step. Why: Open question 1 ("the whole chain, or only the next step") is best answered as the whole chain visible, one verb live.
4. Replace "Rerun" with "Retry" on open Runs only. Why: a closed hard Run's result/ never changes (ladder, Runs section); the button invites breaking that.
5. Add run-check-alignment-t10 as the last chain box after check, and run-pool-t10 on the Cross row. Why: they are Task Runs in the ladder and have no home in the drawing.
