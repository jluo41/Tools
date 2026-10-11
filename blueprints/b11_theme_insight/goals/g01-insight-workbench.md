Goal · the Insight workbench on the shared frame
================================================

(261007, JL: "give me the goal prompt that you can update the workbench-insight in the server and make
it run, and align with our current design". The /goal line points here; this file is the full spec.)

**Goal:** make the Insight workbench run on the shared frame (`/_board/workbench`) at all three
levels, Board · Job · Task, matching b11's current design, and keep today's insight data working.
Done = the host serves every Space at every level as the design draws it, the tests pass, and
screenshots match.


Read first (the design is the source of truth; never edit these drawings)
--------------------------------------------------------------------------

- `Tools/blueprints/b11_theme_insight/studio/`: s00-insight-structure (the Project, the two Blocks, two
  clocks, run types by level), s11-block-level, s12-job-level, s13-task-level (one screen per Space,
  "on disk" under each), s31-insight-guide (the Guide by level). Read each `.md`, then its
  `build_*.py` (the SCREENS lists give each Space's views, button rows and run types).
- `Tools/plugins/haipipe-toolkit/servers/workbench/README.md`: the theme contract
  (`<theme>_theme.py` exporting `THEME = Theme(...)`; `spaces(level, folder, root, sub)` →
  `{Space: Space(html, subspaces, open, run_types)}`); examples `workbench-work/work_theme.py`,
  `workbench-design/design_theme.py`.
- `servers/workbench-insight/insight_theme.py` (interim: today's content at the Block level only;
  build on it, do not replace it), `insightboard.py`, `instance_reader.py`.
- `skills/2_theme/insight/haipipe-insight/ref/block-contract.md`; haipipe-run (hard and soft Runs).


The design (settled: implement)
-------------------------------

1. Plan C. The Prototype (questions + scripts) is its own work Block; its Jobs are versions `j0N_pN/`,
   each with `release.yaml`, `partitions.md`, `thresholds.yaml` (cuts, power floors, compare rule). The
   insight Board holds one dataset with dated versions; its Jobs are `j0N_pN_<d>vM/` (one Prototype
   version × one data version, pinned by path + hash, frozen once closed); a Job's Tasks are its
   questions; their hard Runs are `runs/rNN_<partition>/` (+ `rNN_cross`).
2. Board (s11): Description = Map · Prototype · Dataset · Partitions; Work Details = the Jobs, the
   open one expanded to its Tasks' quick results; Audience Report = Partition × Reading (Coverage ·
   Tracks · Consistency · Findings), D · I · K · W as sections, every view Question │ Work │ Report;
   Runs = the Board's soft runs (add a data version, add a Job, propose a cut, run-coverage,
   run-track-<q>, run-consistency-<jA>-<jB>, run-report-<qNN>, check the Board, handoff), then hard
   from below; Delivery = the signed Wisdom counsel naming its Job.
3. Job (s12): no band; the line "pN × <d>vM · closed, frozen · moved from <prev>: the code | the data"
   opens Description › Prototype. Description = Prototype · Dataset; Audience Report = Question │ Work │ Report by D · I · K · W,
   filtered by Partition × Period (Current · vs previous); vs previous reads only
   `reports/vs-<prev>.md` (written by the Job's run-compare-<prev>), statuses new question · new
   finding · held · changed · dropped · not comparable; Work Details = the Job → Task → Run tree;
   Runs = run-launch · run-power · run-compare-<prev> · run-propose-<job> · run-close, then the Tasks';
   run-propose-<job> (button "Propose questions", on vs previous and in Runs) files new or changed
   questions to the Prototype's proposals/; a Task proposes nothing.
4. Task (s13): one Task type, an insight question on its Job's pair. No band; the line
   "K01 · in <job> · release pN · <d>vM · ✅ checked" opens Description › Question.
   Description = Question · Plan · Data, read only from the release (the ask, DIKW level, why now,
   signed; the needs with work spec, pass rule, Ask covered; each partition's n, base rate, power);
   no propose button (a change is proposed from the Job, run-propose-<job>). Audience Report =
   Question │ Work │ Report over the question's needs (need → the Run that answers it → the page's
   sentence), filtered by Partition × Period; Cross shows the difference test and POOL or SPLIT;
   vs previous reads this question's rows of the Job's `reports/vs-<prev>.md`. Work Details = the
   Task → Run tree; Runs = by type, in order rNN_<partition> → rNN_cross → run-write → run-check
   (→ run-sign, W only); Delivery only for a W Task.
5. Pop-outs: every ↗ opens one: the question (`question.md`, read only), a Run (run.yaml, pins, n and
   power, passes, result preview, report.md), the Cross Run, the page, a method card.
6. Guide (s31): implement only what s31 draws without "?"; leave every red "?" item undone.


Still open (do NOT decide; render nothing for them; list them in the report)
-----------------------------------------------------------------------------

What "held" means; backfill Jobs; whether a handoff goes stale; Findings per partition; whether
Readings re-run automatically; a Board Run's own pop-out; the Prototype's steps in the Guide.


Data on disk today (carry over what exists)
-------------------------------------------

- No plan-C Board exists yet: build a placeholder plan-C Board + Prototype Block as a test fixture in
  a temp folder (no real names, no data values) and render plan C from it.
- `examples-5-design/Project-Application-SMSDesign/tasks/b52_sms_question_dikw` (board.md
  `workbench: insight`; one Job per DIKW level, today's layout): DONE by the base owner (261007,
  design-b03-project-workbench-UI): the base's `Theme.claims` lets insight claim it, so it opens in the
  insight theme with today's Block content (`insight_theme.py`, 5 tests). Keep that working; never
  migrate or rewrite its files. What is still missing there: b11's Map, the Reading row, the Job and
  Task levels, and Check's gates as chips.
- Keep the old route `/_board/insight-board` working until JL retires it.


Rules
-----

- Edit only `servers/workbench-insight/**` (theme, readers, its tests, `guide/` where settled). Ask
  design-b03-project before any change in `servers/workbench/**` or `servers/_host/**`.
- Read-only workbench: nothing writes; a run type only copies its prompt.
- Base look only: the frame's classes, no theme stylesheet.
- Say "DIKW level", never the old word. Paths relative to the SPACE root in anything written.
- No PHI: counts, rates and cut names only; never a row-level value or an identifier.
- Never hand-edit generated files (`results/`, `reports/<run>/`, `delivery/`, `notebooks/`).
- Do not commit or push.


Verify (report each)
--------------------

1. Tests before and after, no new failures: `servers/_host/tests`, `servers/workbench-insight/tests`
   (add: the theme pick for b52, each level's Spaces and subviews on the fixture, every ↗ target),
   `skills/2_theme/insight/haipipe-insight-check/tests`, `skills/1_base/page/haipipe-page/tests`
   (baseline 909 pass / 11 known failures).
2. Restart the host on 5796 (same command); GET `/_board/workbench?path=<…>&format=json` for the
   fixture Board, one fixture Job, one fixture Task, b52 and the register board; list each Space's
   subviews and run types.
3. Headless Chrome screenshots of every Space at each level on the fixture, each beside the matching
   s11/s12/s13 frame, with the differences listed.
4. A table, Space × level: as designed │ as served │ match?


Report
------

Files changed; the table; the screenshots' paths; what is still open (the list above); anything in the
design that could not be built without a base change, and the message sent to b03.
