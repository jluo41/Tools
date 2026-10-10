# j02 · The console

job-of: b03_inlab-human (261009)
spine: CONSOLE mode: `/inlab-human-console` (0.1.0) and `servers/haichat-inlab` (FastAPI routers and a React SPA, built by HAIChat-SPACE as a per-thread iframe).
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

Patient first: pick a patient, read the chart as of the index date, pick a model, run it; the score comes from
the endpoint verbatim. Its routers: console_api (patients, models, predict), message_api (compose a patient
message, judge it, record the human's verdict), labeling_api (read a subjective-label project's artifacts),
tasks_api (a project's task folders), haichat_api (the agent drawer, j04).

Since g02 (261009) it reads a record set in place (`record_store.py`, beside the engine's json reader; the json copy
is the fallback) and a dataset's cooked case set (`case_store.py`), names no table or column of any dataset, reads
Tasks off the Block · Job · Task ladder, and hides a view at the scope where it is only a placeholder. Q02, Q03 and
Q05 are answered; s33 marks what each fix changed.

## Questions

```yaml
questions:
- id: Q01
  title: What does the console own, and what is the toolkit's?
  question: message_api composes and judges with the toolkit's individual-inference report and judge personas, but
    the clinician-brief persona lives only in the console and patient-friendly only in the toolkit; labeling_api
    reads the toolkit's labeling artifacts. Where should each piece live?
  hypothesis: Personas live with their skill in the toolkit and the console reads them; the console keeps only routing
    and display.
  acceptance: Answered when every persona has one home and the console reads it, never copies it.
  work: []
  report: reports/q01_console_vs_toolkit/q01_console_vs_toolkit.md
- id: Q02
  title: Copy each human to json, or read the record store in place?
  question: The engine reads one json per human, so a build step copies each RecSet into InLabStore/<dataset>/patients/
    (a second copy that can go stale, and one more copy of patient data to secure); an adapter would read 2-RecStore
    per request instead (one source of truth, a parquet filter per request). Which way? (JL's question in diagram/09-workspace-wiring.txt;
    drawn in studio s02.)
  hypothesis: 'The adapter: one source of truth and no extra copy of patient data outweigh a cached parquet filter
    per request.'
  acceptance: Answered when one way is chosen with its reason, and the other is removed from the docs.
  work:
  - goals/g02-console-fixes-and-decisions.md
  - ../../../plugins/inlab-human/mcp-servers/endpoint-predict/record_store.py
  - ../../../plugins/inlab-human/mcp-servers/endpoint-predict/server.py
  - ../../../plugins/inlab-human/servers/haichat-inlab/console_api.py
  - ../../../plugins/inlab-human/servers/haichat-inlab/case_store.py
  - ../../../plugins/inlab-human/servers/haichat-inlab/labeling_api.py
  - ../../../plugins/inlab-human/servers/haichat-inlab/fixtures/build_fixtures.py
  - ../../../plugins/inlab-human/servers/haichat-inlab/diagram/09-workspace-wiring.txt
  report: reports/q02_copy_or_read/q02_copy_or_read.md
- id: Q03
  title: How does the tasks feed read the project ladder?
  question: tasks_api.py reads examples/Project-*/tasks/<A01_*> (a letter series) and classifies each task as individual
    or group; today's projects are examples-N-*/Project-*/tasks/bNN_*/jNN_*/tNN_*. How should the feed find and
    scope tasks on the ladder? (s33 issue 5.)
  hypothesis: Read Blocks, Jobs and Tasks the way the project skill defines them, from every examples-* world, with
    the scope read from each Task's face.
  acceptance: Answered when the feed lists a real project's Tasks under their Blocks and Jobs, at the right scope,
    on a fixture tree.
  work:
  - goals/g02-console-fixes-and-decisions.md
  - ../../../plugins/inlab-human/servers/haichat-inlab/tasks_api.py
  - ../../../plugins/inlab-human/servers/haichat-inlab/web/src/components/TasksView.tsx
  - ../../../plugins/inlab-human/servers/haichat-inlab/fixtures/build_fixtures.py
  report: reports/q03_tasks_on_the_ladder/q03_tasks_on_the_ladder.md
- id: Q04
  title: One look for the console and the workbench?
  question: 'The console draws in a Databricks/Mattermost grammar (rail, tab strip, dock); the toolkit''s workbench
    frame has its own (level row, Spaces row, view row, light tables, a Runs panel). Should they share one look,
    or keep two? (Evidence: studio s32''s side by side; s01''s ladder against the toolkit''s.)'
  hypothesis: Share the parts both have (tables, the Runs panel's row, buttons and their states); keep the console's
    rail and dock, which the frame has no counterpart for.
  acceptance: Answered when each element of s32 is marked share or keep, with a reason.
  work: []
  report: reports/q04_one_look/q04_one_look.md
- id: Q05
  title: Build or drop the placeholder views?
  question: 'Seven views are a placeholder at Group scope (Raw, Source, Record, Internal, External, Model, Checklist),
    and Internal and External at Individual too. Which are built next, and which leave the rail at that scope? (Evidence:
    studio s11, s12.)'
  hypothesis: Drop what has no Group meaning yet from the Group rail; build Internal first (the DIKW cards it promises).
  acceptance: Answered when every placeholder has a build-or-drop decision and the rail shows only built views.
  work:
  - goals/g02-console-fixes-and-decisions.md
  - ../../../plugins/inlab-human/servers/haichat-inlab/web/src/views.ts
  - ../../../plugins/inlab-human/servers/haichat-inlab/web/src/components/NavRail.tsx
  - ../../../plugins/inlab-human/servers/haichat-inlab/web/src/Console.tsx
  report: reports/q05_placeholder_views/q05_placeholder_views.md
```
