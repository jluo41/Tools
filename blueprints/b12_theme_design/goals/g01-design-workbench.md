Goal · the Design workbench on the shared frame
===============================================

(261007, JL: "give me a prompt for the set up goals so that the goal will update the workbench-design to
be aligned with the things we designed here", following `../../b11_theme_insight/goals/g01-insight-workbench.md`
and `servers/workbench-insight/`. The /goal line points here; this file is the full spec.)

**Goal:** make the Design workbench run on the shared frame (`/_board/workbench`) at all three levels,
Block · Job · Task, as b12 draws them in s11 · s12 · s13, and keep today's design Boards working.
Done = the host serves every Space at every level as the design draws it, the tests pass, and the
screenshots match.


Read first (the design is the source of truth; never edit these drawings)
--------------------------------------------------------------------------

- `Tools/blueprints/b12_theme_design/studio/`: s11-design-block, s12-design-job, s13-design-task (one
  screen per view, "on disk" and "skills" under each, green ✎ = decided, red ? = open), s03-design-methods
  (the design unit's five steps and the registered methods M01 – M05), s31-design-guide (the Guide by
  level). Read each `.md`, then its `build_*.py`: the SCREENS lists give each Space's views, its third
  row, its Runs-panel run types and its on-disk tree; DISK and SKILLS give the folders and the skills;
  QUESTIONS give what is decided (✎) and what is open (?). s00 still draws a methods Block: JL removed
  it (261007); ignore that part.
- `servers/workbench/README.md`: the theme contract (`<theme>_theme.py` exporting `THEME = Theme(...)`;
  `spaces(level, folder, root, sub)` → `{Space: Space(html, subspaces, open, run_types)}`).
- The pattern to follow: `servers/workbench-insight/`: `insight_plan_c.py` (reads the new layout from
  the folders, read only), `insight_views.py` (draws each level's Spaces in the base's look),
  `insight_theme.py` (`PC.is_plan_c(block)` picks the new views, else today's), `tests/plan_c_fixture.py`
  (a placeholder Board built in a temp folder).
- Today's design server: `servers/workbench-design/design_theme.py` (the ladder as of 261007 morning:
  `jNN_<goal>_by-<method>`, family from the slug), `designboard.py` (the old Board route and Guide ›
  Method), `design.py` (the old Page workbench), `tests/test_design_theme.py`.
- `skills/2_theme/design/haipipe-design/` (`scripts/design_ladder.py`, the scaffold; `ref/`),
  `haipipe-design-unit`, `haipipe-design-workflow/references/run-cards.md`, `venue/venue-sms`;
  haipipe-run (hard and soft Runs).


The design (settled: implement)
-------------------------------

1. The ladder on disk (s11 · s12 · s13 DISK):

   ```text
   bNN_<app>/                              Block: one application, one channel
   ├── board.md                            ## Goals: one card per goal (aim · who · venue · N · rules · leave out · signed)
   ├── inputs/iN/ + manifest.yaml          inputs versions: rules · theory · handoff links, each file's sha256
   ├── observed/eNN_<exp>/                 what an Exp returned: arms.csv (arm · jNN · dNN · n · totals) · source.md · manifest.yaml
   ├── runs/run-<type>-<target>/           the Block's Runs, every one soft
   ├── reports/qNN_<topic>/                the Block's questions' reports
   ├── delivery/                           designs.json · designs.md · screens/: every released design, every Job
   └── jNN_<goal>_<design-method>/         Job: one goal × one registered method version × one inputs version
       ├── jNN_….md                        its pins: goal G01 · method M04 m2 (sha) · inputs i2 · state
       ├── inputs/ + manifest.yaml         the fence: goal.md · method.md -> … · rules.md -> … · handoff · venue
       ├── runs/                           soft only: run-setup-goal|method|inputs-jNN · run-open-designs-jNN ·
       │                                   run-freeze-predictions-jNN · run-release-jNN
       ├── t00_reason-ideas/               ② runs/r01_reason_15/result/: chains.yaml · ideas.yaml · topics.md
       ├── tNN_d<NN>_<slug>/               ③ ④ one design: elements.yaml · prediction.yaml ·
       │                                   runs/r01_generate_dNN · r02_verify_dNN · run-revise-dNN · r03_verify_dNN
       ├── t99_review-whole/               ⑤ runs/r01_rank_15/result/ranking.csv (kept N of N + 5)
       └── delivery/                       designs.json · designs.md · screens/
   ```

   A Job is recognised by its face's pins (`goal:` · `method:` · `inputs:`), not by a `_by-` slug.
   Its goal comes from `goal:`, its method id and version from `method:`, and its method's type (one
   of the 13 cards) from the registered method: M01 By goal · M02 By precedent · M03 By insight ·
   M04 By insight · M05 By insight (s03, decided 261007). The registry folder does not exist yet: read
   the type from this table, never create the registry.
2. Block (s11): Description = Map (goals down × registered methods across, each cell its chain of
   Jobs; two Jobs picked in a cell pop out what moved and what it changed) · Goals · Methods (one card
   per registered method used: type, versions, its Jobs) · Inputs (one card per version, its parts
   labelled by step ①'s parts). Audience Report = Questions · Cost (a card per Job: tokens, time,
   rounds, first try, per passed) · Predicted vs observed (each tested design as it reads, its frozen
   prediction beside its arm in observed/, scored by run-score-eNN's scores.csv) · Method scorecard (a
   card per method version, summed from scores.csv). Work Details = one card per Job (All · per goal);
   open, a preview of its Tasks: t00 · each design as a small phone with its state · t99 · released.
   Runs = all soft, grouped Set up (run-add-goal-<goal> · run-setup-rules · run-add-inputs-<iN>) ·
   Launch a Job (run-add-job-<jNN>) · Report (run-add-observed-<eNN> · run-score-<eNN> ·
   run-propose-questions · run-report-<qNN>), plus run-propose-<method> · run-draw-<sNN>. Delivery =
   every released design as it reads (an SMS as a phone bubble, a UI as its screen), in order, naming
   its Job.
3. Job (s12): Description = Goal (pinned, signed once at the Block) · Method (M04's choices at the
   five steps) · Inputs (the fence, each input labelled by its step-① part, manifest). Audience Report =
   Reason ideas (②, the chains) · Design display (③ ④, one card per design, the design as it reads │
   its process │ its review) · Review whole (⑤, the ranking) · Predicted vs observed (its own rows,
   read from the Block's observed/ and scores.csv) · Performance. Work Details = Reason Ideas ·
   Conduct & Review · Review Whole, every Task a card. Runs = Setup · Reason Ideas · Conduct & Review ·
   Review Whole (hard or soft a column). Delivery = designs.md · designs.json.
4. Task (s13): one tab, the same six Spaces for every Task; its run types decide what each shows.
   Three kinds: t00 (② Topics · Ideas · Chains), a design (③ ④ Description › Design · Evaluation;
   Audience Report › Tests · Drafts · Performance; Work Details › Elements), t99 (⑤ Ranking ·
   Coverage · Kept · Dropped). Idea Studio at every Task.
5. Runs panel: every entry a folding card named run-<type>-<target> (soft) or rNN_<type>_<target>
   (hard, as its folder); each run type lists the skills s11 · s12 · s13 SKILLS name for that screen; a
   run type only copies its prompt.
6. Pop-outs: every ↗ opens one: a method card (the Guide's card), a Job, two Jobs in a Map cell, a
   design Task, a Run (run.yaml, its result), an insight row a design cites.
7. Guide: s31-design-guide, only what it draws without "?"; Guide › Method keeps serving
   `studio/s03-design-methods/parts/`.


Still open (do NOT decide; render nothing or "—"; list them in the report)
--------------------------------------------------------------------------

Re-read every red "?" in s11 · s12 · s13 QUESTIONS when you start; green ✎ notes are settled. At
261007 the red ones need another owner: `usage:` (tokens) in Run receipts (show tokens as "—"); the
method registry `haipipe-design-unit/methods/`; the Block's Run cards in `run-cards.md` (the theme holds
the prompts until then); a design delivery skill (`haipipe-design-delivery`, proposed, to own
designs.json's schema); a reviewer agent for ④ ⑤; and the Exp's owner naming jNN · dNN on each arm.
Everything else in s11 · s12 · s13 is decided (green), including s12's inputs/ fence rules (relative
symlinks + sha256; a changed target blocks Generate; data outside the SPACE named by its variable).


Data on disk today (carry over what exists)
-------------------------------------------

- No Board on the new ladder exists yet. Build a placeholder Board as a test fixture in a temp folder
  (`tests/design_fixture.py`, like insight's `plan_c_fixture.py`): one Block, two goals, inputs i1 · i2,
  Jobs on two registered methods, t00 · ten design Tasks (five dropped) · t99, one observed Exp with
  scores. Placeholders only (`<opening>`, `<goal>`, PATIENT_001-style ids if any): no DrFirst content,
  no data values.
- `examples-5-design/Project-Application-SMSDesign/designs/B00_DesignBoard-R2Messages-260821` and
  `B01_DesignBoard-Stage25-CarryOver-261005` are the older layout (0-BR-brief/ · 2-Design/ …): they keep
  reading as today (vanilla on the frame; `/_board/design-board` and the Page workbench in
  `design.py`). Never migrate or rewrite their files.
- `design_theme.py`'s `_by-<method>` reading changes in one go here (method from the face's `method:`,
  goal from `goal:`, family from the method's type), with its tests; the scaffold
  `haipipe-design/scripts/design_ladder.py` may be updated to make the new ladder, so the fixture and
  the scaffold agree.


Rules
-----

- Edit only `servers/workbench-design/**` (theme, readers, views, its tests, `guide/` where settled)
  and the scaffold above. Ask design-b03-project before any change in `servers/workbench/**` or
  `servers/_host/**`.
- Read-only workbench: nothing writes; a run type only copies its prompt.
- Base look only: the frame's classes (.topic folds, .wf-table, .chip, .st-ok / .st-warn, the tab
  rows); no theme stylesheet. A design shown "as it reads" may use the old Page's phone markup.
- Paths relative to the SPACE root in anything written. No PHI: per-arm totals only, never a row.
- Never hand-edit generated files (`results/`, `reports/<run>/`, `delivery/`, `notebooks/`).
- Do not commit or push.


Verify (report each)
--------------------

1. Tests before and after, no new failures: `servers/_host/tests`, `servers/workbench-design/tests`
   (add: the theme pick for a new-ladder Block and for B00 · B01; each level's Spaces and views on the
   fixture; every ↗ target; the Job reader without `_by-`), `skills/1_base/page/haipipe-page/tests`
   (baseline 909 pass / 11 known failures).
2. Restart the host on 5796 (the same command it runs with now); GET
   `/_board/workbench?path=<…>&format=json` for the fixture Block, one Job, t00, one design Task, t99,
   and B01; list each Space's views and run types.
3. Headless Chrome screenshots of every Space at each level on the fixture, each beside the matching
   s11 · s12 · s13 screen, with the differences listed.
4. A table, Space × level: as designed │ as served │ match?


Report
------

Files changed; the table; the screenshots' paths; what is still open (the list above); anything in the
design that could not be built without a base change, and the message sent to b03.
