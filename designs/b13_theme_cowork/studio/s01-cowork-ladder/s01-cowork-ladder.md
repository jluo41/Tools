s01 · cowork ladder
====================

**Topic:** every cowork row in one drawing, Block down to Run (JL 261007). The overview frame
holds Q01's proposed answer: the ladder, why an email or a meeting is a row and not a Task, each
level's six Spaces, where today's Check Views go, and the open points in red. Below it are the Block
and Job rows. Each row shows its folder, what it holds, its skills and its screens, with the
proposal (teal, solid) above today's workbench (gray, dashed). There is no cowork Task row.

**Source:** the rows are defined once in `../../../b03_project_workbench/studio/s01-overall-tree-structure/`
(`build_ladder_v4.py`, `level_views.py`). This topic's own builder draws them under its overview
frame, as b12's s01-design does. Edit the cowork rows there and this drawing follows on its next build.

**Feeds:** `../../reports/` q01 (the ladder question).


Files
-----

```text
s01-cowork-ladder/
├── s01-cowork-ladder.md            this notes file
├── s01-cowork-ladder.excalidraw    the drawing; marks are kept on rebuild
├── s01-cowork-ladder.png           preview
└── build_s01_cowork_ladder.py
```

Rebuild: `python build_s01_cowork_ladder.py` (or b03's `studio/_build/make.sh`), then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s01-cowork-ladder.excalidraw s01-cowork-ladder.png`.


Decided so far
--------------

(proposed 261007, waiting for JL; Q01)

1. A cowork topic climbs Block → Job → Run. An email, a meeting or a checklist step is a row of its
   Job (Work Details › Timeline · Checklist · Emails · Meetings), not a Task.
2. A Task appears only when a Job writes a document with others over several rounds. It is then a
   Page Task (`tNN_<doc>/`), shown on the shared Task tab.
3. The Job tab gets the Block's six Spaces: Description (the job page; Job · Files) · Idea Studio
   (optional) · Audience Report (optional: the Block's Questions that cite this Job) | Work Details
   | Runs (soft: email · notes · update · check) · Delivery (optional).
4. Cowork has no hard Runs. Work that runs code is a work Task in another Block, cited.


Open
----

- `j00_people/` → `people.md` at the Block? (changes real Blocks: JL)
- A Job's `design/`: drawings → `studio/`, notes → `materials/`? (changes real Jobs: JL)
- Task ▾ greyed unless the open Job has a `tNN_<doc>/`?
- `board.md` → `bNN_<topic>.md`, with every Theme.
- Q02: waiting-on, drafts, stale. Q03: Delivery.

(write here, or mark the drawing in red)
