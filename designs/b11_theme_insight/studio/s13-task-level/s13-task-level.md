s13 · Task level
================

**Topic:** one question's Task tab, drawn for K01 in `j03_p2_<d>v2`, its Spaces as full screens on the shared
frame (Guide · Block · Job · Task), each with "on disk" under it (JL 261007: "s11, s12, s13 ... for the Block
level, Job level and task level, to make each of them"). It follows s00 (a Job pins one Prototype version and
one data version) and s12 one level down (JL 261007: "yes, I think so, that will be better").

**Source:** the screens are drawn by `../_build/insight_ui.py`, shared by s11 · s12 · s13 and s03; the method
cards are read from their files at build time. s31-insight-guide and the goal spec
(`../../goal-insight-workbench.md`) read this builder's SCREENS.


Files
-----

```text
s13-task-level/
├── s13-task-level.md               this notes file
├── build_s13_task_level.py         the builder; marks are kept on rebuild
├── s13-task-level.excalidraw       the drawing: today → proposed, a frame per Space with its views, pop-outs, open notes
└── s13-task-level.png              its preview
```

Rebuild: `python build_s13_task_level.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s13-task-level.excalidraw s13-task-level.png 0.4`.


Proposed (261007)
-----------------

1. One Task type on the Insight Board: an insight question on one Job's pair. Its DIKW level changes what it may
   say and which methods fit; a W Task cites the levels below and is signed (JL 261007: "we just have the insight
   discovery tasks, right?").
2. No band beside the tab (JL 261007: remove it on every frame page). Its line,
   `K01 · in j03_p2_<d>v2 · release p2 · <d>v2 · ✅ checked`, opens Description › Question.
3. Description: Question · Plan · Data. Question and Plan are the release's question.md, read only (the ask,
   DIKW level, why now, signed; the three methods; the needs with work spec, pass rule, Ask covered, agreed).
   Data is this question's n, base rate and power on each partition, before any outcome; a weak cut is refused
   and shown, never run. A new or changed question is proposed from the Job (run-propose), never from a Task
   (JL 261007: "the question propose is conducted in the job level?").
4. Audience Report: Question │ Work │ Report over the question's needs, need → the Run that answers it → the
   page's sentence (or a cited Discovery Result), filtered by Partition × Period. Cross shows the difference
   test and its POOL or SPLIT; vs previous reads this question's rows of the Job's `reports/vs-j02.md`. The page's
   answer heads each view.
5. Work Details: the Task → Run tree, hard (one per partition, then r04_cross) and soft (write, check), each with
   kind · status · passes · last and ↗ to its pop-out.
6. Runs: by type, then the order a Task runs in: rNN_<partition> → rNN_cross → run-write → run-check (→ run-sign,
   W only), inside its Job's run-launch … run-close.
7. Delivery: none, except a W Task, whose signed counsel goes to the Block's handoff.
8. Pop-outs: a need (spec, pass rule, answered by, cited by), the Run, the page, a method card.


Open
----

See the drawing's open notes (red).

(write here, or mark the drawing in red)
