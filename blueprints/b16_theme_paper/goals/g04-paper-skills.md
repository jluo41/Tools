g04 · Update the paper skills to the ladder
===========================================

One goal prompt for one session (written 261007 by design_b16_theme_paper-s21_skillrun). It runs the skill
update plan of Q05, drawn in `studio/s21-paper-run-skill/`. Every decision is made below; run it without asking
unless a Stop rule fires. Run it as:

```text
Run Tools/blueprints/b16_theme_paper/goals/g04-paper-skills.md with PHASES=1-2
```

**Run 2026-10-07, phases 1-6** (design_b16_theme_paper-s21_skillrun): the outcome and the checks are in
`reports/q05_skills_and_runs/` § 4. Two decisions changed in the run: D9's `template.md` stays (the venue bank links
it) and `ref/call-template.md` is new; Board and version soft Runs are `haipipe-run` folders, not single files.

`PHASES` picks the phases to run (`1-2`, `3`, `4`, `5`, `6`, or `1-6`). Run them in order; a phase starts only
when the one before it passed its checks.


Read first
----------

- The design: `Tools/blueprints/b16_theme_paper/studio/s21-paper-run-skill/` (its notes file, and in the drawing
  the frames "Runs by level", "skill folders: before → after" and "skill update plan"). Its builder holds the
  typed tables this goal follows: `RUN_NAME` (one name per Run), `OWNER` (who owns a Run with no card),
  `FOLDERS` and `NEW_FILES` (each file's before → after, change and why), `PLAN`.
- The levels: `studio/s11-paper-block/` (Board), `s12-paper-job/` (a version), `s13-paper-task/` (a Section).
- The model: the design theme's skill, `skills/2_theme/design/haipipe-design/ref/design-ladder.md` and
  `scripts/design_ladder.py` (one contract, one scaffold for every level).
- The Run contract: `skills/1_base/project/haipipe-run/` (soft Runs `run-<type>-<target>`, hard `rNN_`).
- Reports: `reports/q01_paper_ladder/`, `q04_story_into_topics/`, `q05_skills_and_runs/`.


Decisions (made; follow them)
-----------------------------

D1. One contract: `haipipe-paper/ref/paper-structure.md` → `haipipe-paper/ref/paper-ladder.md` (`git mv`, so its
    history follows). It draws the B J T R tree as design-ladder.md does: the Board face, `studio/` · `reports/`
    · `runs/` (+ `runs/README.md`) · `delivery/` · `venues/` · `related/`; the version `j0N_v<MMDD>_<desk>/`
    with the same Space folders; Tasks `t00_abstract` · `t0N_` Main · `t2N_` Appendix (A = t21) · `t3N_`
    letters; comments as `reports/qNN_<kind>-<MMDD>/` with `page-type: comments`. Every mention of the old file
    name in Tools follows.
D2. One scaffold: `haipipe-paper/scripts/paper_ladder.py` with `board`, `version`, `task`, `run`, each with
    `--dry-run`. `version` takes `version_paper.py`'s `spaces` and `new`; its `comments` moves to
    `haipipe-paper-comments/scripts/review_items.py add`. `paper_ladder.py rollback` still reads the
    `.paper-version-N.yaml` records that `version_paper.py` wrote, so an earlier move can still be undone. Then
    `version_paper.py` is removed. `run` writes `runs/run-<type>-<target>.md` and lists its type in
    `runs/README.md`.
D3. `migrate_paper.py`, `rename_tasks.py`, `topics_paper.py` move into `haipipe-paper/scripts/carry_over/` (`git mv`)
    and keep working, rollback included. They retire once every paper Board has moved (not in this goal).
D4. Run names: every Run is `run-<type>-<target>`, exactly as `RUN_NAME` in the s21 builder says, or the
    card's own pattern where it has one (`run-structure-<slug>`, `run-paper-narrative-<slug>`). Only another
    theme's supporting Run keeps its hard `rNN_` name.
D5. Run cards: `haipipe-paper-workflow/ref/run-cards.md` keeps its line format (`🔘 BUTTON label · Space ·
    pattern · views`, then `🧩 SKILL`, `🤖 AGENT`, `✍️ SIGNS`, `💬 PROMPT`). Its Space field becomes
    `<Level> › <Space>` (`Block › Audience Report`), no " · " inside it, and `views` names the third-row views
    (`narrative`, `draft-main`). One card per Run of s21's frame 1; a Run with two buttons gets one card per
    button with the same pattern. Of the seven cards no screen shows: Idea review and Select idea retire;
    Claim review, Redraw, Evidence runs, Delivery runs and Page check go to the Space s21 names, or retire if
    none fits.
D6. Gates: G0-G2 sign at the Board (the Story's), G3-G5 at the version (release a Section, submission ready,
    every response answered). `run-workflow.md` and the workflow SKILL.md say so.
D7. The workbench reads its run types from the cards by level and Space (`paper.paper_run_types` keyed by the new
    Space field; `paper_theme._kinds(level, space, views)`), never from labels typed in `paper_theme.py`. Labels
    typed there today become cards first, then their typed lists go.
D8. The Story writes `studio/sNN-story-<telling>/` (its face, its drawings) and its research questions as Board
    Questions with `reports/qNN_` (Q04); the Narrative (N1-N4: says · drawn · told · attracts) and the
    audience review are `haipipe-paper-story/ref/narrative.md`. The Ideation writes `studio/s01-ideation/` and
    Questions with `group: ideation`, through `haipipe-ideation-*`. Neither writes a Page any more.
D9. The venue: `haipipe-paper-venue` writes `venues/<venue>/call.md` + `kit/`; `template.md` → `ref/call-template.md`.
    `venue/` (the bank, its own repo) and the assemble skill's `profiles/` stay where they are (JL's call, Q02).
D10. Every skill touched bumps its version (minor) and adds a CHANGELOG entry naming Q05.


The phases
----------

1 · Contract (haipipe-paper)
   1. D1: move and rewrite the contract; fix every mention (`grep -rn paper-structure.md` in Tools).
   2. D2: write `paper_ladder.py`; move `comments` to `review_items.py add`; then remove `version_paper.py`.
   3. D3: move the three carry-over scripts.
   4. `haipipe-paper/SKILL.md`: routes by level (Board · version · Section), names the contract and the scaffold;
      `ref/run-naming.md` (D4), `ref/page-integration.md` (Sections and letters are Page Tasks).
   5. `tests/test_paper_ladder.py`: in a temp folder, `board`, `version`, `task`, `run` make each level, and a
      second `version --from` copies the written files only; `rollback` restores an earlier record exactly.
   Check: the new test; `tests/test_run_naming.py`; `paper_ladder.py board --dry-run` on a temp path.

2 · Cards (haipipe-paper-workflow, workbench-paper)
   1. D5: rewrite `run-cards.md` by level and Space; D6: `run-workflow.md` and the SKILL.md.
   2. `workbench-paper/ref/space-mapping.md` retires (its rows are in the cards); `workbench-table.md` is
      regenerated with `table-workbench` (`0_utils/table-workbench/ref/render_workbench_table.py`), never by hand.
   3. D7 in `servers/workbench-paper/` (`paper.paper_run_types`, `paper_theme._kinds` and its callers only).
   4. `workbench-paper/SKILL.md`: the theme on the shared frame, not the old page's four Spaces.
   5. Rebuild s21 (`python build_s21_paper_run_skill.py`, then render its png): frame 1 must show 0 "screen"
      and 0 "drawn" rows for the Runs whose owner phase is done.
   Check: `table-workbench --check --cards`; `servers/workbench-paper/tests` and `servers/_host/tests` (counts);
   every paper Board renders at every level on the frame, each button with its skill.

3 · Board skills (-story, -ideation, -venue): D8, D9; each SKILL.md's examples use placeholders only.
   Check: on a temp Board made by `paper_ladder.py board`, the Story and Ideation write topics and Questions,
   and the workbench shows them under Audience Report › Narrative and › Ideation.

4 · Version skills (-comments, -assemble, -workflow)
   1. `review_items.py`: `add` (a comments report), `route` (an item to a Section's `run-revise-<item>`),
      `reply` (the answer into the report and the response letter), over the report's `## Review Items` table.
   2. `build_delivery.py`: `send` (freeze the build into `delivery/sent/<MMDD>/`) and `bib` (reference.bib);
      `cover_letter.py` reads the `t31_cover-letter` Task.
   3. The version face's `## Narrative` and standing J1-J5 questions, and Release a Section (G3), in the
      workflow skill.
   Check: `haipipe-paper-assemble/tests/run.sh` (say the two known Word-equation failures if they remain);
   on a temp version, add → route → reply makes one item answered.

5 · Section skill (-section): `t0N_` · `t2N_` · `t3N_`; the reader contract; `ref/requirement.md` (V and W
   rules, the four-axis rubric `1_base/writing/haipipe-writing/ref/evaluation-rubric.md`, the `SUB-*` rows); a Section's own
   `studio/` and `reports/`; `create_section_sessions.py` finds `t0N_` Sections; `ref/section-sessions.md`.
   Check: `paper_ladder.py task` makes a Section the Page workflow opens; `section-stats.py` runs on it.

6 · Old names out (all nine): no Story Page, Ideation Page, `A1-Story`, `B[abc]-`, `RD<NN>`, `S-<desk>`,
   `-<MMDD>-` left in skill docs except CHANGELOGs and the carry-over scripts' own docs (they read the old
   layout on purpose); the family `README.md` lists the skills by level.
   Check: s21's frame "the skills" shows 0 in its "old" column for every skill.

What the level sessions said (261007)
-------------------------------------

- **Board (design_b16_theme_paper-block):** each Space's run types come from `_kinds(group, views)` plus a few
  cards typed in `paper_theme.py`: `READ_A_PAPER`, `ADD_RELATED`, `WILL_IT_ATTRACT`, `ASK`, `RELEASE`,
  `LETTER_RUNS`, and the Delivery "Build · Check" filter. Each becomes a card in phase 2. Keep every button
  label as it is (Ask a Question, Write the report, Review the report, Review for an audience, Release a
  Section): tests and the drawings name them.
- **Version (design_b16_theme_paper-job):** the version tab's buttons sit in `_version_description` (Update the
  version, Check the rules), `_version_report` (`ASK`, `RELEASE`, `LETTER_RUNS`, the delivery kinds for
  Comments), `_version_work` (the sections kinds) and `_delivery_runs` (Build, Check). Their prompts use older
  wording; the cards carry the new prompts.
- **Section (design_b16_theme_paper-task):** `section_spaces` and its helpers never call `_kinds`; a Section's run
  types come from the frame's `PAGE_TASK_RUNS` and the Page's run-cards.md. For phase 5, what is live and
  decided: Sections `t00_abstract` · `t0N_<title>` · `t2N_<title>`; the story-row from the version face's
  `## Narrative`; undated Run names (`page.py run-names` renames dated ones); comments as
  `reports/qNN_<kind>-<MMDD>/` of type comments. s13's Requirement row is the drawing for `ref/requirement.md`.
  The `SUB-*` rows stay in `haipipe-paper/ref/submission-readiness.md`, their one home that
  `paper_theme._sub_rows` reads; `requirement.md` links them and copies none.


After each phase: add a dated line to `reports/q05_skills_and_runs/q05_skills_and_runs.md` § 4, add a green
`✎ <date>` note to s21's CHANGES for what changed, rebuild s21, and report.


Stop rules (the only ones)
--------------------------

- A check fails and two fixes did not clear it: stop and report the failure with its output.
- A live session is editing the same file now: check ListAgents first; before editing `paper.py` or
  `paper_theme.py`, message design_b16_theme_paper-block (Board views) and design_b16_theme_paper-job (version
  views) and wait for their answer. The Section views never call `_kinds` (the task session, 261007), so
  phase 2 needs no answer from design_b16_theme_paper-task.
- A change would move or rename a real Project's folders: none in this goal; stop if one seems needed.


Never
-----

- Hand-edit a generated file (`workbench-table.md` outputs, `delivery/**`, `results/**`, receipts; AGENTS.md rule 0).
- Edit `servers/workbench/` or `servers/_host/` (ask design-b03-project-workbench-UI), the Page skills under
  `1_base/page/` (ask its owner), or `venue/`.
- Commit, push, reset, clean or stash; write an absolute `/Users/…` path; put a project, Board or person's name
  in a skill file (placeholders only).


Done when
---------

- Every Run in s21's frame 1 is a card or the frame's (0 "screen", 0 "drawn" for the phases run).
- The skill folders match s21's "after" tree for the phases run.
- Tests pass with counts reported; each touched skill has its version and CHANGELOG line.
- A short report: files changed (one line each), check counts, what is left (later phases, JL's two calls).
