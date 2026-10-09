g02 · Fix the In-Lab Console's bugs, then decide and build three of its Questions
================================================================================

One goal prompt for one session (written 261009 after g01, JL: "give me the prompt for the second goal"). g01
documented the console and its review (`studio/s33-console-ui-issue/`) ranked eleven issues. This goal fixes the
five that need no decision, then decides three Questions and builds what each decision asks. Every decision is made
below; run it without asking unless a Stop rule fires. Run it as:

```text
Run Tools/blueprints/b03_inlab-human/j02_console/goals/g02-console-fixes-and-decisions.md
```


What this is
------------

The console is `Tools/plugins/inlab-human/servers/haichat-inlab/` (React + Vite over five FastAPI routers). Its
synthetic fixtures are `fixtures/` (`run_fixture.sh` starts a stub endpoint and the console on loopback and prints
both PIDs). Its design drawings are `Tools/blueprints/b03_inlab-human/j02_console/studio/`, redrawn by their
builders after `_build/shoot_console.py` re-shoots the fixture console. g01 changed no behaviour; this goal does.


Read first
----------

- `goals/g01-console-design-and-docs.md` (how the fixtures, the shots and the drawings work).
- `studio/s33-console-ui-issue/` (the ranked issues and their evidence) and `studio/s51-console-runtime/`.
- The Job face `j02_console.md` `## Questions`, and the frames `reports/q02_copy_or_read/`,
  `q03_tasks_on_the_ladder/`, `q05_placeholder_views/`.
- The code each step names below; for the store layouts, the haipipe code in `code/haipipe/` (Record and Case
  stages) and the `haipipe-data` skill. Read code and docs only, never a store's data (D1).


Decisions (made; follow them)
-----------------------------

D1. Synthetic data only, as in g01. No real patient, record, case, label or study file is read, rendered or shot.
    Learn every store layout from code and docs. A new fixture (a record store, a case set, a project tree) is
    written by `fixtures/build_fixtures.py`, says "synthetic" in its first line or first key, and is git-ignored
    like the rest of `fixtures/` output.
D2. Fix 1, the image (s33 issue 1). The Dockerfile copies every Python module `main.py` imports, `personas/`, and
    anything those read at run time, with a `.dockerignore` that keeps out `web/node_modules`, `fixtures/` output,
    `__pycache__` and `.runs`. Check: s51's image table has no red row; if Docker is on this machine, `docker build`
    succeeds and the container answers `/api/health` with the fixture stores mounted. If Docker is not available,
    say so in the report; the s51 table is then the check.
D3. Fix 2, Health (issue 3). `console_api.health` counts the store as configured when either `INLAB_DATASET_STORE`
    or `INLAB_PATIENT_STORE` is set, and reports which one it uses. Health shows each setting's NAME and whether
    it resolves (`set · found`, `set · missing`, `unset`), never the path (issue 8, which this fixes too). Check:
    the fixture console started with only the dataset store says ok.
D4. Fix 3, the patient picker (issue 4). `cohortOf` in `web/src/types.ts` returns the store's `summary.cohort`
    and otherwise the dataset's own label; the hard-coded study prefixes go. No study name stays in the plugin's
    code (`grep` for each removed prefix finds nothing in `web/src`). Check: a synthetic glucose patient no longer
    shows MIMIC.
D5. Fix 4, the agent gate (issue 7). `can_use_tool` already denies a tool in neither list; the drawer showed the
    call as if it ran. Make the drawer show a denied call as refused (its chip says refused, with the gate's
    message). Check: on the fixtures, a turn that calls `prepare_payload` shows it refused. If the agent cannot run
    here (no Claude Code login), check with a unit test of the gate and the drawer's handling of a denied result.
D6. Fix 5, small (issue 11). A favicon in `web/public/`, and plotly in its own chunk (`build.rollupOptions.output.
    manualChunks` in `web/vite.config.ts`). Check: no favicon 404 on the walk; `npm run build` warns of no chunk
    over 500 kB, or the remaining one is named in the report.
D6b. Fix 6, any dataset (added 261009 mid-run, JL: "we might have any dataset with any type of table"). The
    Record chart drew one glucose curve with meal, exercise and medication markers, found by table name
    (`/CGM/`, `/Diet/`, `/Exercise/`, `/Med/`) and by fixed column names. It becomes generic: every table with a
    time column (found from the values, not the name) is a lane on one shared time axis; a numeric column is
    a line, any other row a marker whose hover lists the row. No table or column name is written into the
    chart. The Case view's text fallback (D8) and the record-store reader (D7) follow the same rule. What stays
    named is a model's own input contract (the engine's payload dialects, declared by the endpoint's
    manifest), which is about the endpoint, not the data. Check: `grep` finds no table name in
    `RecordChart.tsx`, `record_store.py` or the case code; the record chart draws all three synthetic datasets.
D7. Q02 decided: read the record store in place. One source of truth, and no second copy of patient data to
    secure, outweigh a parquet filter per request (cached per human). Build an adapter beside the engine's json
    reader: when `INLAB_RECORD_STORE` points at a record store (the layout the haipipe Record stage writes), the
    console assembles each human's json per request from it, cached in memory; when only the json stores are set,
    behaviour is unchanged. The fixtures gain a synthetic record store in that layout for the glucose type, and
    `run_fixture.sh` gains a mode that serves from it. Check: every Individual view shows the same patient the same
    way from the record store as from the json copy (compare the API answers, not by eye). Then update
    `diagram/09-workspace-wiring.txt` to say the adapter is the way and the copy is the fallback; update s02 (the
    fork turns black with a green `✎ 261009 decided: read in place` note).
D8. Case view fixed through Q02 (issue 2). When a case set exists for the dataset (the layout the haipipe Case
    stage writes; `INLAB_CASE_STORE`), the Case view lists its cases: one per trigger moment, with its facets.
    Without one, it lists no glucose readings as cases: the banner says "no case set mounted", and text datasets
    (dialogue, review) keep today's one-row-per-text behaviour, named as such in the banner. The fixtures gain a
    synthetic case set for the glucose type (a few meal-triggered cases per human). Check: s13's glucose shot shows
    cases from the case set, not timestamps.
D9. Q03 decided: the tasks feed reads the ladder. `tasks_api.py` finds `examples-*/Project-*/tasks/bNN_*/jNN_*/
    tNN_*` under `INLAB_PROJECTS_ROOT` (the SPACE root, or any folder holding `examples-*`), groups Tasks under their
    Block and Job, and reads each Task's scope from its face (individual or group); the letter series `A01_*` is
    read only as a fallback. The fixtures gain a synthetic project tree (one Block, two Jobs, four Tasks, both
    scopes, every name a placeholder). Check: the Tasks view shows the tree under its Block and Job at the right
    scope.
D10. Q05 decided: hide what is not built. A view that is a placeholder at a scope leaves the rail and the tab strip
    at that scope (one flag per view and scope in `web/src/views.ts`); it comes back when it is built. Nothing new
    is built under Q05 in this goal. Check: the Group rail lists only built views; s11 and s12 are redrawn.
D11. Each decided Question's report gets its Answer, Evidence, Limits and Next written, `answer-status: answered`,
    and the reason above; the register entry's `work:` lists what was changed. Q04 (one look) and j04 Q02 (actions
    as MCP) stay open and untouched.
D12. Drawings: re-shoot with `_build/shoot_console.py`, rebuild every j02 topic, render every preview, read each
    preview yourself. s33 keeps all eleven issues: each fixed one is marked fixed with a green
    `✎ 261009 fixed: <how>` note in its row, and the remaining ones (issue 9, no links out) stay as they were.
    Every drawing that changed gets its green note in place and in its title frame.
D13. Processes and commits as in g01: stop every process this goal starts by its PID only (never `pkill -f` or
    `killall`); `npm install` may run; commit to Tools `main` only the paths this goal touched, named one by one,
    and push; never commit or push DrFirst-SPACE.


Steps
-----

A. Start the fixtures (`run_fixture.sh`, note the PIDs) and confirm g01's API checks still pass.
B. The six fixes (D2–D6b), each with its check. Rebuild the front end after the web changes.
C. Fixtures for the decisions (D1): the synthetic record store, case set and project tree.
D. Q02 and the Case view (D7, D8), with their checks.
E. Q03 (D9) and Q05 (D10), with their checks.
F. Reports and register (D11); regenerate `diagram/10-ui-elements.txt` and `11-routes.txt` with
   `diagram/build_ui_docs.py` if a route or a view changed.
G. Re-shoot and redraw (D12), then walk every view at both scopes on every data type again (as g01 did) and record
   the counts: screens, failed requests, browser errors.
H. Stop the processes by PID, commit and push (D13).


Stop rules (the only ones)
--------------------------

- A real patient, record, case or label file would have to be opened to continue (D1): stop and report what asked
  for it.
- The record store's or the case set's layout cannot be learned from code and docs alone: do steps A, B, E and the
  rest without D7 and D8, mark Q02 `answer-status: partial` with what is missing, and report it.
- A live session is editing `servers/haichat-inlab/` right now: check ListAgents, message any whose work names it,
  and wait for its answer.
- A fix breaks a g01 API check and cannot be repaired in this goal: revert that fix, keep its issue open in s33
  with the reason in red, and continue.


Never
-----

- Hand-edit a generated file (`10-ui-elements.txt`, `11-routes.txt`, drawings, previews, `facts.json`, shots).
- Write an absolute `/Users/…` path, a real person's name, or a project or study name into a Tools file.
- Decide Q04 or j04 Q02, or build a placeholder view.
- Stop a process by a name pattern; commit `node_modules/`, `dist/` or fixture output; commit or push DrFirst-SPACE.


Done when
---------

- The six fixes are in (D2–D6b), each with its check passed (or, for the image, the reason Docker could not run).
- Q02, Q03 and Q05 are answered in their reports with what was built; Q04 and j04 Q02 stay open.
- The console reads a synthetic record store in place, its Case view lists case-set cases (no timestamps as cases),
  its Tasks view shows a ladder tree, and its rails show only built views.
- Every j02 topic is redrawn from new shots, each change with its green note; s33 marks each fixed issue.
- The walk is recorded again (screens, failed requests, browser errors); every process is stopped by PID; Tools
  `main` is pushed.
- A short report: files changed (one line each), each check's result, s33 before and after, and what is left
  (Q04, j04 Q02, issue 9).
