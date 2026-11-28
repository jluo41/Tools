# A01 · A sentence's marks agree with its record

> "why this is not fully alligned." (JL 261118, Draft Lab, ScalingGlucose t00_abstract s6)

## 1. Need
At the end of the Section workflow, each sentence row in Draft Lab should show marks that agree with the record: a current score as ★N, an applied edit as 📝, and only the person's own pending step as ✓?.

## 2. Now
The s6 row read ★– 📊1 📝1 💬1 ✓?. Pass 7 (`## Pass 7 · 2026-11-18 · on draft v1.9`) rated s6's v1.9 words, the same words s6 has now. The page still marked the score stale: rendered `data-stale=1` on the s6 review card.

## 3. Gap
`draft_step_revise.py` (about line 130) set the review's date with `_when(head)`, the first date in the report body. The body's `Standard: … (261115)` line gave 2026-11-15. The s6 card, `State: written · 2026-11-18`, was "later" than that, so s6 went into `since` and its ★ showed –. The Pass title's own date was never read.

## 4. Methods
Read the Pass title's date first and fall back to the body only when the title has none: `seen = {"": _when(title) or _when(head)}`. A sentence whose words did change after the review is still caught by the separate words test (`scored_words` on the Pass's `on draft vN`).

## 5. Update
- `servers/workbench/workbench-task-draft/revise_steps/draft_step_revise.py`: review date from the Pass title
- `servers/workbench/workbench-task-draft/revise_steps/tests/test_draft_lab_mustcheck.py`: `ReviewDateFromPassTitleTest`, fails without the fix and passes with it
- host 5602 restarted; t00_abstract s6 now renders ★8 (`data-scores="logic 8 · read 8 · human 8"`, no `data-stale`)

## 6. Never again
The test pins the case: a rule date in the body plus a card written on the Pass's day. All 47 draft tests pass. The ✓? marks on s5, s6 and s7 stay, because they are the person's step: their check was on words that later changed, and W5 asks for a new ✓.
