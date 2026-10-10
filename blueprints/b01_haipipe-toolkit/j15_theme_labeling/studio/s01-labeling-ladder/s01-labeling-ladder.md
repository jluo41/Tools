s01 · labeling ladder
======================

**Topic:** every labeling row in one drawing, Block down to Run (JL 261007): an overview frame with
this Block's open questions, then the Board, Job and Task levels, each row with its folder, what it
holds, its skills, and its screens, the proposal (teal, solid) above today's workbench (gray, dashed).

**Source:** the rows are defined once in `../../../b03_project_workbench/studio/s01-overall-tree-structure/`
(`build_ladder_v4.py`, `level_views.py`) and drawn by `../../../b03_project_workbench/studio/_build/theme_ladder.py`;
edit the rows there and this drawing follows on its next build.

**Feeds:** `../../reports/` q01 (the ladder question).


Files
-----

```text
s01-labeling-ladder/
├── s01-labeling-ladder.md            this notes file
├── s01-labeling-ladder.excalidraw    the drawing; marks are kept on rebuild
├── s01-labeling-ladder.png           preview
└── build_s01_labeling_ladder.py
```

Rebuild: `python build_s01_labeling_ladder.py` (or b03's `studio/_build/make.sh`).

Proposed so far
---------------

1. (261007, for Q01) The engine's one labeling job is a Task, `tNN_<dataset>_labeling/` with
   `labeling/`; today's page-level workbench becomes its Task tab, in the six Spaces. Data and
   Labeling and Quality views go to Work Details (Building: Embedding · Definition · Rounds ·
   Guideline | Scanning: Test · Evaluation · Scan · Audit); Contract to Description; REPORT.md to
   Audience Report; Handoff and Final labels stay in Delivery.
2. (261007, for Q01) The Job is one dataset × one label with four step Tasks, prepare · keys ·
   label · score (t01-t04). Its tab is new: Audience Report = our labels vs the dataset's keys
   (was Quality › External gold), Work Details = the four steps (was Data › Preparation's Task
   list). A scan-only Job reads another Job's handoff.
3. (261007, for Q01) A Run is one operation: `runs/rNN_<operation>_<target>/` (was
   `runs/run-labeling-<op>-<MMDD>-<target>.yaml` + `results/<same>/`); a resumed human session
   is a pass.


Open
----

- The real labeling Blocks (`tasks/`, schema at the Block, Jobs by side) move only when JL says.
- schema.yaml at the Block or the Job (Q03).
- A labeling Run: hard with `result.yaml` pointing into `labeling/`, or soft?
- Building | Scanning as the third row, and the gates (Q02).
- The Theme becomes `labeling/` (s01-D29), so `labeling/` appears twice in a job's path; proposed:
  keep the Task's lane name and tell the two apart by depth. `labeling.py`'s `_labeling_job`
  must read both Theme names (via `themes.py`).

(write here, or mark the drawing in red)
