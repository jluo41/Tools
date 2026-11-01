# s51 Board UI: Report · the cell as a whole · stage 1 · r01

```text
letter      mean   result    lowest rubric
A Answers   8.1    pass      Same look 7, Salience 7
B Tracks    8.3    pass      Words 7, One job 7
C Jobs      8.6    pass      Salience 7
D Data      8.1    not yet   Salience 6
E Handoff   7.9    not yet   Salience 5
```

## Does each letter belong

1. A, B and C belong; they are the three things a reader checks on a dataset: what it says, whether that holds across Jobs, and which Jobs exist.
2. D belongs, but as drawn it lists two dates; it should show what each freeze holds.
3. E belongs, but as drawn it is an empty state plus a rule; it should show the counsel draft and its chain to Design.
4. Missing: the Board's own Questions (board.md `## Questions`, `reports/qNN_<topic>/`, answered across Jobs). The face says this cell feeds `reports/` q01, yet no letter shows a Board question. The section table also lists Questions for a Block's Report.
5. Missing: Coverage (question × cut × Job) is squeezed into B as a "Readings" box with "Open"; it is a grid of its own.

## Pairing with Work (s52)

The letters are shared, as decided. A, C, D, E pair: Report shows the state, Work acts on it. B does not pair: Report B is the question × Job grid, while Work B is a proposal inbox with no track in it. Work B should list the changed tracks from Report B, each with "Propose".

## Further improvements (beyond the rubric fixes)

1. Merge "answer first" and "the grid" into A: rows are the questions (X first, then D, I, K, W), columns are the Jobs, each cell the short answer plus held or changed; the newest column bold. Why: this settles Open question 1 ("Answers first, or Tracks first") by making them one view, and puts the agreed Board grid on the opening screen.
2. Fix the sample state: draw j02 (AP1 × F2, moved: data) so j03 moves only code. Why: the contract (insight-ladder.md, The rules 1) refuses a Job that moves both clocks, and the drawing now teaches the forbidden case as normal.
3. Open on the newest closed Job by default, and show a preview Job's answers under a "preview" state word. Why: A now headlines answers from AP2, a plan nobody has signed, as if they were the Board's.
4. Add the Board's Questions view (or make it B, with Tracks inside it). Why: a Board answers its own questions across Jobs; today none appears anywhere on the page.
5. Give every view the same shape the sibling themes use: numbered bars with one emoji each, and the bottom helpers (🙋 Interactions, 🖼️ The drawing, 🧠 The mind map). Why: only section 1 is a numbered bar today, and no view has the helpers, so the insight Board will read differently from the paper and labeling Boards.

(reviewer: a fresh general-purpose agent, 261101)
