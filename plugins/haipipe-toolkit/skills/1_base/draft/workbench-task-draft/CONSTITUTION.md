# workbench-task-draft · constitution

JL's feedback on the Draft Lab page, as articles. It wins over SKILL.md; where they disagree, follow this, then bring
SKILL.md in line.

## A01 · A sentence's marks agree with its record

> "why this is not fully alligned." (JL 261118, Draft Lab, ScalingGlucose t00_abstract s6, a row reading ★– 📊1 📝1 💬1 ✓?)

**Rule:** A sentence's ★ shows its newest score whenever that score rated the words the sentence has now; ★– only when the words changed after the review.
**Why:** The W4 loop wrote the s6 rewrite into v1.9 and Pass 7 rated v1.9, yet the page drew ★–. The page took the review's date from the first date in the report body, a rule date `Standard: … (261115)`, so the card written 2026-11-18 looked later than the review.
**Class:** the review's date read from the wrong place, so a current score is drawn as an old one at the end of a workflow.
**Cases:** ✅ the review date (draft_step_revise.py, `seen`, now the Pass title first) · ✅ the score-against-words test (scored_words on the Pass's `on draft vN`, unchanged, already right) · ✅ ✓? on s5, s6, s7 is the person's own step (their check is on words that changed; the workflow's W5 asks for it), not a misalignment
**Check:** a Pass whose body carries an older rule date and a card written on the Pass's day keeps that sentence's ★ current.
**Run:** `cd plugins/haipipe-toolkit/servers/workbench && PYTHONPATH=../_host python -m pytest -q workbench-task-draft/revise_steps/tests/test_draft_lab_mustcheck.py -k ReviewDateFromPassTitle`
**Status:** solved 261118
**Solved by:** `servers/workbench/workbench-task-draft/revise_steps/draft_step_revise.py`: review date from the Pass title
**Report:** constitution/A01-marks-agree-with-record.md

## A02 · The manual says what the page shows

**Rule:** SKILL.md describes only the page the code draws now: its views, the side pane, Delivery and what each click writes. A layout the page no longer has goes to `ref/classic/` or the CHANGELOG, never above the current contract.
**Why:** 261127: SKILL.md led with a contract of nine views and an Around the Work band, then 540 lines of older layouts, while the page drew four views and the band was gone (hai-block A01); an agent reading it from the top would rebuild what was removed.
**Class:** a manual that grows by stacking each new layout over the last, so the first thing read is stale.
**Cases:** ✅ the focus page (1 · Draft, 2 · Plan, 3 · Evidence, 4 · Display) · ✅ the old layouts moved to `ref/classic/`, the cards to `ref/draft-lab.md`, Runs to `ref/runs.md`
**Check:** every view `focus_draft_words.WORK` builds is named in SKILL.md § The page, and no view or band the page lost is.
**Run:** `cd plugins/haipipe-toolkit/servers/workbench && PYTHONPATH=../_host python -m pytest -q workbench-task-draft/page_shell/tests/test_manual_matches_page.py`
**Status:** solved 261127
**Solved by:** SKILL.md rewritten to the current page; `page_shell/tests/test_manual_matches_page.py`
