g03 · Finish the paper workbench, then migrate one paper Board
=============================================================

One goal prompt for one session (written 261007 by the Block session, design_b16_theme_paper-block). Every
decision is made below; run it without asking unless a Stop rule fires. Run it as:

```text
Run Tools/designs/b16_theme_paper/goals/g03-paper-workbench-and-migration.md with TARGET=<SPACE-relative path of one Paper-<Name>/ Board>
```


Read first
----------

- Designs: `Tools/designs/b16_theme_paper/studio/` s11-paper-block (Board), s12-paper-job (a version), s13-paper-task
  (a Section), s31-paper-guide (the Guide by level), s03-paper-migration (the move, by level; its earlier detailed
  version is `history/build_s03_paper_migration-261007-v2.py`).
- Code: `Tools/plugins/haipipe-toolkit/servers/workbench-paper/paper_theme.py` and `paper.py`;
  `servers/workbench/frame.py` (`level_patterns`, `question_rows`, `page_task_spaces`) and `servers/workbench/README.md`
  (the base classes a Space may use).


Decisions (made; follow them)
-----------------------------

D1. `A1-Story/` → `j00_story/`, a reference Job. Story Pages keep their stems (`Story00-…`, `Story<L>-…`).
D2. One send = one version Job: `Ba-<desk>-Main/`, `Bb-<desk>-Appendix/`, `Bc-<desk>-Round/` merge into
    `j01_v1_<desk>/` (desk lowercased, from the `Ba-` name). Sections and Rounds keep their stems; Main and
    Appendix are read from the stem.
D3. A review round stays inside its send as a Task (`RD<NN>-…`); a resubmission to another venue is a new version
    Job, `j02_v2_<desk>/`.
D4. `delivery/` moves into `j01_v1_<desk>/delivery/`. Generated files there are rebuilt only by their generator
    (haipipe-paper-assemble); frozen `sent/` and `released/` builds move as records, unchanged.
D5. `studio/`, `reports/` and any `related/`, `venues/` stay at the Board. The migration creates no venue or
    related file; the workbench keeps reading the Story's venue line and related-papers table until they are added.
D6. The version gets a face, `j01_v1_<desk>/j01_v1_<desk>.md`: send, desk, venue, state, which Story it tells
    (read from `board.md`'s `story-current:`), and an empty `## Questions` register.
D7. Uncommitted work in TARGET does not block the move. Snapshot `git -C TARGET status --porcelain` into the moves
    map first; `git mv` tracked paths (their edits travel with them), plain `mv` untracked ones; never commit.
D8. Guide: a Block step 0, "Set up the paper" (scope, venues, related work; signed by naming the target venue),
    goes into `guide/method.md`'s **Block** table. Skills stay one list (no skills by level). The venue lives in
    both places: the Board's `venues/` for every venue, the version's face for its one.
D9. In Related, the group of datasets and repos is named "Datasets and repos", so "Resources" means only
    Description › Resources.


Part A · the workbench (servers/workbench-paper/ only)
-------------------------------------------------------

The version tab is drafted in `paper_theme.py` (`version_spaces`) and renders on every paper Board; the Board's
Work Details lists its Jobs; Rounds open as Tasks. Finish:

1. Check `version_spaces` against s12, view by view, and fix what differs:
   - Description: Version · Venue rules.
   - Audience Report: Questions (J1–J5, Q│W│R) · Draft-Main · Draft-Appendix · Comments. Comments is the
     Rounds' `## Review Items`, falling back to the Feedback Concern Table.
   - Work Details: All · Main · Appendix · Letters.
   - Delivery: LaTeX · Word · Cover letter · Checks.

   The version reads its face (D6) when present. Then send the live third rows to design_b16_theme_paper-job.
2. `paper.paper_desk()` also reads the desk from `jNN_v<N>_<desk>/`.
3. `guide/guide.yaml` `folders:` gains `j00_story/…` and `jNN_*/` patterns beside today's; `guide/method.md` gains
   step 0 (D8); the Related group rename (D9) in `paper_theme.py`.
4. `skills/2_theme/paper/haipipe-paper/ref/paper-structure.md` shows both layouts, the ladder first; the other
   paper docs that teach the old layout get one line pointing there.
5. Tests in `servers/workbench-paper/tests/`:
   - a placeholder fixture Board in each layout (temp folder);
   - every level and third-row choice renders;
   - a Round's Description has no reader contract (the Task session's ask).
   - Run `_host/tests` and `workbench-paper/tests`; report counts.

Never touch `section_spaces` or the helpers it calls (the Task session's), `servers/workbench/` or `servers/_host/`
(ask design-b03-project-workbench-UI).


Part B · migrate TARGET
-----------------------

1. Preflight. Stop rules, the only ones:
   - Part A's tests fail;
   - a live session is editing TARGET right now: check ListAgents, message any whose work names TARGET, and wait
     for its answer.
2. Write `skills/2_theme/paper/haipipe-paper/scripts/migrate_paper.py`, generic, one Board per run:
   - `--dry-run` prints every move (D1-D4), the `board.md ## Pages` heading rewrite, the
     `delivery/paper-build.toml [pages]` path edits, each `../` link edit (file:line) in non-generated `.md`, the
     version face it will write (D6), and the Run receipts it leaves as history;
   - `--apply` does all of that and writes `<board>/.paper-moves.yaml`: old → new, the date, the pre-move
     `git status` snapshot (D7);
   - `--rollback` reverses every move from the moves map.
3. Rehearse on a copy of TARGET in the session's scratch folder: `--dry-run`, then `--apply`, then the checks of
   step 5. Fix the script until they pass.
4. Apply to TARGET. No commit.
5. Verify, reporting each count:
   - every Page opens at its level on the frame (Board · j00_story · j01_v1_<desk> · each Section · each Round);
   - the old page (`/_board/paper-board`) opens;
   - `haipipe-paper-assemble --dry-run` finds every Section fragment through the new `[pages]` paths;
   - no broken relative link in a non-generated `.md`.

   If any check fails on TARGET, run `--rollback` and report.
6. Do not rebuild `delivery/` (it needs a full LaTeX run); say it is the next step and how to run it.


Never
-----

- Hand-edit a generated file (`delivery/**` outputs, `results/**`, receipts, `notebooks/**`; AGENTS.md rule 0).
- Rename a Page stem; commit, push, reset, clean or stash; touch a Board other than TARGET.
- Write an absolute `/Users/…` path into a tracked file; put a project, Board or person's name in Tools files.


Done when
---------

- Part A: 0 test failures; every paper Board renders at every level.
- Part B: TARGET is on the ladder (D1-D6), opens at every level, its build finds every Section, the moves map is
  written, and `git -C TARGET status` shows the moves for JL.
- A short report: files changed (one line each), check counts, what is left (rebuild delivery/, Q02/Q03 notes).
