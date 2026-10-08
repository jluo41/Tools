261006 · design session · s02-studio-and-report
===============================================

session: (subagent of a Claude Code session; id not recorded) · agent: cc · date: 2026-10-06
topic: s02-studio-and-report · feeds: Q03, Q07, proposed Q09, Q10
kind: design only; no skill or server was changed; no patient data was read or written


Ask
---

Read JL's four red notes on the ladder drawing (studio drawing = creation, report drawing =
presentation, sessions saved into a topic's `chat/`, every reply section links a studio topic
or a report question) and propose which topics, skills and workbench pieces must change, how
sessions get saved, and a short plan. Write only this topic folder.

Mid-session change from the coordinator: JL created `studio/s01-overall-tree-structure/`
with hyphens, so this topic became `s02-studio-and-report/` and the proposal uses `sNN-<topic>/`.


Read
----

- `Tools/designs/b03_project/board.md` and `reports/` (Q01 to Q08, all open)
- JL's marks on `studio/s01-overall-tree-structure/ladder-v3.excalidraw` (the person's own text elements)
- skills: `0_utils/response-format`, `display/excalidraw-report` (+ `ref/report-drawing.md`),
  `question/haipipe-question`, `task/haipipe-task` (+ `ref/hierarchy.md`, `ref/check_task_tree.py`),
  `project/haipipe-project` (+ `ref/project-structure.md`), `page/haipipe-workbench-studio`
  (+ `ref/chat.md`, `ref/draw.md`), `page/haipipe-page`
- servers: `workbench-shared/xcal.py`, `workbench-shared/assets/xcal-boot.js`,
  `workbench-shared/chat.py` (keep), `workbench-task/task_questions.py`, `workbench-task/task_views.py`
- the merge writer `Tools/designs/b03_project/studio/_build/canvas.py`


Sections
--------

1. Reading of the notes: two drawing modes, same seed-and-edit mechanics, different edit rule. (studio: s02)
2. Topics: main home Q03, plus Q07; proposed Q09 shared drawings, Q10 agent sessions; s03 to s05 suggested. (report: Q03)
3. Skills: response-format Related line takes sNN or qNN; haipipe-question report folder gets draft/ and a same-stem drawing; excalidraw-report gets a tree scratch and a report suggestion loop. (studio: s02)
4. Workbench: plain drawings save with no revision check; RoadMap Draw scans only flat studio/*.excalidraw; generated drawings are view only by script, not by mode. (report: Q07)
5. Sessions: one summary file per session, no raw log, PHI gate, no absolute paths. (studio: s02)


Changed
-------

- `Tools/designs/b03_project/studio/s02-studio-and-report/s02-studio-and-report.md` (new): the proposal
- `Tools/designs/b03_project/studio/s02-studio-and-report/chat/261006-design-session.md` (new): this file


Decided
-------

Nothing is decided; all of it is a proposal for JL. Findings that hold regardless of JL's answers:

1. `xcal.py` saves a plain (non-linked) drawing with no revision check, so a stale tab overwrites a newer build.
2. The Page chat keep writes the absolute jsonl path into `transcript.md` and `digest.md` (AGENTS.md rule 7).
3. Several contracts say drawings are "never edited by hand", which contradicts "keep human's scratch".
4. `haipipe-question` puts a report's drawing in `reports/qNN/studio/`; JL's tree puts it beside the Page.


Open
----

For JL: the ten questions at the end of `s02-studio-and-report.md` (hyphen or underscore, Jobs or
folders, one drawing per topic, flat drawings, folded suggestions, owner of studio topics, raw
transcripts, every section linked, register, new Questions).
