s12 · Job level
===============

**Tags:** `Levels`

**Stage:** explore

**For:** a deck, and one insight Job's tab, its Spaces as full screens with what is on disk, for the people who build the workbench

**Delivery type:** ui

**Topic:** one Job's tab, drawn for j03_p2_<d>v2: one Prototype version × one data version (s00), its six Spaces as full screens on the shared frame (Guide · Block · Job · Task),
each with "on disk" under it (JL 261007: "s11, s12, s13 ... for the Block level, Job level and task
level, to make each of them, instead of nesting all the things together"). It follows s00: a Job
pins one Prototype version and one data version; a DIKW level groups the questions inside a Job. The
method cards come from s03.

**Source:** the screens are drawn by `../_build/insight_ui.py`, shared by s11 · s12 · s13 and s03;
the cards (names, skills, the DIKW levels they fit) are read from their files at build time.


Files
-----

```text
s12-job-level/
├── s12-job-level.md               this notes file
├── build_s12_job_level.py     the builder; marks are kept on rebuild
├── s12-job-level.excalidraw       the drawing: today → proposed, a frame per Space with its views, pop-outs, open notes
└── s12-job-level.png              its preview
```

Rebuild: `python build_s12_job_level.py`, then
`python ../../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s12-job-level.excalidraw s12-job-level.png 0.4`.


Proposed (261007)
-----------------

1. Description: Prototype · Dataset (JL 261007: "It will be of no map, just the prototype and Dataset").
   Prototype: release p2, its questions by DIKW level (new · changed · retired), its cuts as defined in
   the release, its shared code, all read only. Dataset: <d>v2, its extract, frozen date, rows, what is
   new, then each cut's n, power and refused cells. No band beside the tabs (JL 261007: remove it on every
   frame page): the pair's line "p2 × <d>v2 · closed, frozen · moved from j02: the code (p1 → p2)" opens
   Description › Prototype.
2. Audience Report is the Question │ Work │ Report table (JL 261007: "I actually want to put the Question Work
   Report to the Audience Report"), under D · I · K · W with the method chips, filtered by Partition (Full · A ·
   B · Cross) × Period (Current · vs previous). Every cell opens a pop-out: the question (question.md from the
   release), the Run, the page, a chip's card. Under vs previous the Report cell carries the status (new · held ·
   changed · dropped) and the summary line; on Cross it carries POOL or SPLIT.
3. Work Details is the Job › Task › Run tree (JL 261007: "maybe show the J-T-R structure?"): a Task row under
   its DIKW level, opening to its Runs (hard, one per partition, and rNN_cross; then soft write and check), each
   with kind · status · passes · last; third row All · hard · soft. A Task's ↗ opens its tab (s13), a Run's ↗
   the Run pop-out (run.yaml, pins, n and power, passes, a preview of result/, report.md, Rerun · Check).
3c. vs previous is produced by the Job's soft Run run-compare-<prev> (here run-compare-j02), which reads both
   Jobs' results and pages and writes reports/vs-j02.md; the view reads only that file. Its held rule is plan,
   fixed in the release's thresholds.yaml (compare: same direction and intervals overlap; D counts within a
   tolerance). Statuses: new question · new finding · held · changed · dropped · not comparable (JL 261007,
   via the s00/s01 session: "we might want to propose more run-types").
3d. Runs: by type (hard · soft · launch · power · compare · close), then the Job's run order: Add a Job
   (Board) → run-launch → run-power → per Task rNN_<partition> → rNN_cross → run-write → run-check →
   run-compare → run-close (frozen). Beside it, the run types of every level (proposed).
3e. (261007) The Job proposes: run-propose-j03, a soft Run after run-compare-j02 and before run-close-j03,
   reads vs-j02.md's statuses and the gaps ("we cannot answer <what>") and files each new or changed
   question to the Prototype's `proposals/<slug>.md` (kind · DIKW level · from j03 · why). Button "Propose
   questions" on Audience Report › vs previous and in Runs. A Task no longer proposes (s13; JL 261007: "the
   question propose is conducted in the job level?"). Adding questions makes no new kind of Job: the
   proposal opens the Prototype's next version Job (j0N_p3), then the Board adds an ordinary pair Job
   (p3 × <d>v2, the code moved). Open: a new question answered on data already seen is exploratory until the
   next data version confirms it; the next Job reruns unchanged questions or links their Runs by hash.
3f. (261007) The Board's soft Runs in the Runs aside now use s11's words.
4. Idea Studio's typical topics, to the right of its frame: s01-<what moved>, s02-<a surprise>.
5. Delivery (?): only the latest Job's Wisdom counsel goes to the Board's handoff.

Decided
-------

s12-D01 · The Job's Work is its steps, 1 · Launch · 2 · Run · 3 · Write · 4 · Check · 5 · Compare · 6 · Close, a
tab each, in the order a Job runs. A tab is Operation over Result, as the draft and labeling Tasks' steps are: its
work panel (Input, Running now, the step's run-card prompt with your notes and the Job's session line, the close's
sign) folds until you open it, its Result by DIKW level under it. Chips are read from the files; a bare link opens
the step that comes next; the Job → Task → Run tree is 2 · Run's last card. Built: workbench-insight 1.2.0, and the
Job › Work Details run cards by step, haipipe-insight-workflow 3.1.0 (JL 261022: "how to make it that when the
user want, they can open this work panel and work on it").

s12-D02 · A person works the Job on the screen too, beside the agent's prompt (JL 261023: "design the work in a way that
we human can operate this system as well", then "go ahead and do it"): in 4 · Check, a page's row folds a CHECK (tick
"I read the page and its Runs' results", then ✅ Pass, or ↩ Return with the reason; a returned page goes back to
3 · Write), and 6 · Close has 🙋 Sign the close once every step before it is done. One route, `POST
/_board/insight-act`, re-checks each gate and writes what the agent's Run would, `by: a person`, no name. Built:
workbench-insight 1.3.0; browser check `servers/_host/checks/person_actions_browser.mjs`.


Open
----

1. The Task's Work as steps too (s13): Plan · Run cuts · Pool · Write · Check.
2. Work in place: a chat docked under the open step, or copy to a session only (today: copy).
3. Agree its **For:** line and **Delivery type:** (ui), proposed by the agent 261030?

Changes are marked on the drawing in green (✎ <yymmdd>), and listed on its title frame.

See the drawing's Questions frame (red).

(write here, or mark the drawing in red)
