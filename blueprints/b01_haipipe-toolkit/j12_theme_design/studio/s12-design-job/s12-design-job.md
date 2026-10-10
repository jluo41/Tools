s12 · Design Job
================

**Topic:** One design Job's tab, drawn for j03_<goal>_<design-method> (G01 × design method M04, version m2 × inputs i2, N = 10) (JL 261007: "s11, s12, s13 … for the Block level, Job level and task level … instead of
nesting all the things together"), drawn the way b11 draws its levels (JL 261007: "check s11 s12 and s13
[of b11] … borrow their ideas"). It follows `../s00-design-structure/`: a Job pins one goal, one method
version and one inputs version, and returns N designs, each a Task.

The drawing, top to bottom:

- **Job level · today → proposed**: where each part of today's design workbench moves.
- **one frame per Space** (Description · Idea Studio · Audience Report · Work Details · Runs · Delivery),
  each holding all its views, each view a full screen on the shared frame (Guide · Block · Job · Task)
  with "on disk" under it: the folders and files that screen reads. Red dashed = proposed.
- **pop-outs**: what a ↗ opens (a method card, read from its file; one design).
- **open ?**: the level's open questions, as loose red notes.

Proposed (261007)
-----------------

1. Description: only what the Job pins: Goal (the aim, N, the rules it keeps), Method (the registered method M04, version m2, read only: its choices at each of the design unit's five steps, See input · Reason ideas · Conduct process · Review item · Review whole, read from `../s03-design-methods/design_unit_drawing.py`), Inputs (the Job's own `inputs/`, the only folder the design work sees: `goal.md`, relative symlinks to the Block's inputs and the insight handoff, and a frozen `manifest.yaml`; step ① decides what goes in). No Map: the Map of goals × methods is the Block's (s11).
2. Audience Report follows the design unit: Reason ideas (②, t00's reasoning chains, one card per topic, from `chains.yaml`) · Design display (③ ④, one card per design, in order: the design as the reader sees it, an SMS as a phone bubble, a UI as its rendered screen │ its process │ its review and expected outcome; dropped designs folded at the end) · Review whole (⑤, t99 ranks the 15 and keeps 10) · Predicted vs observed (each released design's frozen prediction beside the Exp, read from the Block's observed/eNN/arms.csv and run-score-eNN scores.csv rows for this Job) · Performance (each design: tokens, time, rounds, length, its prediction frozen at release). No vs last Job: Jobs are compared on the Block (s11's Method scorecard, or two Jobs in a Map cell).
3. Work Details: t00 reason ideas · t01 – t15 one design each (a row opens its Task tab, s13) · t99 review whole; a looping method adds rounds (red).
4. Runs: the three setup Runs · run-open-designs-j03 · each Task's hard Runs (t00 run-reason-t00 · tNN run-generate-dNN, run-verify-dNN-v1 · t99 run-rank-t99) and revise.
5. Delivery: the passed designs, word for word; a person releases.

**Source:** the screens are drawn by `../_build/design_ui.py`, shared by s11 · s12 · s13 and borrowed from
`../../../b11_theme_insight/studio/_build/insight_ui.py`; the method cards are read from
`servers/workbench-design/guide/methods/` at build time. The rows of b03 (proposed above today's served
screens) stay in `../../../b03_project_workbench/studio/` s11-block-variants, s12-job-variants and s13-task-variants.

**Feeds:** `../../reports/` q01_design_ladder · q02_design_workbench.


Files
-----

```text
s12-design-job/
├── s12-design-job.md            this notes file
├── build_s12_design_job.py      the builder (screens from ../_build/design_ui.py)
├── s12-design-job.excalidraw    the drawing; marks are kept on rebuild
└── s12-design-job.png           its preview
```

Rebuild: `python build_s12_design_job.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s12-design-job.excalidraw s12-design-job.png 0.4`.


Decided (261007, JL)
--------------------

✎ 261007: every Run is named `run-<type>-<target>`, hard ones too (JL: "unify the name to be run-xxx-xxx"):
`run-reason-t00` · `run-generate-d<NN>` · `run-verify-d<NN>-v<k>` (v<k> = the draft it checks) · `run-rank-t99`;
a looping method's second round is `run-reason-t00-r2` · `run-rank-t99-r2` (new inputs, so a new Run). Was
`rNN_<type>_<target>`.

1. Every step of the method is a Task: `t00_reason-ideas/` (② Reason ideas), `t01_d01_<slug>/` …
   `t15_d15_<slug>/` (③ ④, one design each), `t99_review-whole/` (⑤ Review whole: rank the 15, keep 10).
2. A design and its review are one Task with two Runs: `run-generate-d<NN>/` (③) and `run-verify-d<NN>-v1/` (④,
   another agent), then `run-revise-d<NN>` and a further verify. A new object is a new Task; another step on
   the same object is another Run.
3. A Job is set up by three soft Runs in its `runs/`: `run-setup-goal-j03`, `run-setup-method-j03`,
   `run-setup-inputs-j03`; set up = all three closed. No methods Block: a method is a registered card in the
   design skill, linked into `inputs/method.md`.

4. Settled with the Task session (s13, on JL's "use your own judgement"): `run-open-designs-jNN` (the Job's)
   opens the design Tasks, and t00 only writes `ideas.yaml`; T2 critique runs per design inside ④, and T3 pretest
   once per Job on the kept designs; t99's rank Run writes each prediction as a draft, frozen when a person
   releases; dropped designs keep their Tasks, marked dropped and folded; each reasoning step's `from` is a
   file in the manifest or "own knowledge", checked by the reviewer before the design Tasks open.
5. The goal is signed once, in the Block's goal list; `run-setup-goal-jNN` only pins it (with s11).
6. The Exp's data and its scoring are the Block's, once per Exp (`observed/eNN/`, `run-score-eNN`); the Job's
   Predicted vs observed view reads its own rows (with s11).


Code change, waiting on decision ⑤ (registered methods)
--------------------------------------------------------

The Job folder is now `jNN_<goal>_<design-method>/` (JL 261007) in every b12 drawing; the code still reads
`jNN_<goal>_by-<method>/`. Once ⑤ is settled, this session (the Job level) changes it in one pass, and the
Block session reviews the Block side and rebuilds s11:

1. `servers/workbench-design/design_theme.py`: `method_of` reads the Job face's `method:` field, not the folder
   name; `is_design_job` follows. `_block` takes each Job's goal from the face's `goal:` field (today it splits the
   folder name on `_by-`, in the goals set and in the Goal list table).
2. `FAMILY`: the family comes from the registered method's type (its card), not from the slug.
3. `skills/2_theme/design/haipipe-design/scripts/design_ladder.py` and `ref/design-ladder.md`: the scaffold and
   the contract name the new folder, write `goal:` and `method:` on the face, and make the Job's `inputs/` with
   its `manifest.yaml`.
4. `servers/workbench-design/tests/test_design_theme.py`: scaffold new-style Jobs; keep one test that an old
   `_by-` folder still reads.


Open
----

See the drawing's open notes (red).

(write here, or mark the drawing in red)
