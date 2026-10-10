s12 · Job level
===============

**Topic:** a paper version's tab on the shared frame: one version for one venue, its telling, its Sections
and its build; its Spaces as full screens, "on disk" under each, two pop-outs, then Guide › Method
opened from the Job tab (JL 261007).

**Source:** the screens are drawn by `../_build/paper_ui.py`, shared by s11 · s12 · s13; the Guide's
steps and method cards are read from `servers/workbench-paper/guide/method.md` and its `methods/`
(and the Page Task's `guide.yaml` at Task level) at build time. Placeholders only.

**Feeds:** `../../reports/` q01_paper_ladder (and the open marks of q02, q03).


Files
-----

```text
s12-paper-job/
├── s12-paper-job.md           this notes file
├── build_s12_paper_job.py     the builder; marks are kept on rebuild
├── s12-paper-job.excalidraw   the drawing: today → proposed, one row per Space (screen · on disk · why), Guide › Method, open notes
└── s12-paper-job.png          its preview
```

Rebuild: `python build_s12_paper_job.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s12-paper-job.excalidraw s12-paper-job.png 0.4`.


Decided and drawn (261007, green ✎ in the drawing)
--------------------------------------------------

1. A version is `jNN_v<MMDD>_<desk>/`, dated by its send; its face carries venue · deadline · tells
   (a studio topic, `studio/sNN-story-<telling>/`) · from · answers, its `## Narrative` (the old §8, the
   build's order) and its `## Questions`. It holds `studio/` · `reports/` · `runs/`, its Tasks and `delivery/`.
2. Its Tasks: `t00_abstract` · `t0N_` Main · `t2N_` Appendix (A = t21) · `t3N_` letters (t31 cover
   letter, t32 response).
3. Audience Report: Questions (the register, then the standing J1–J5) · Draft-Main · Draft-Appendix
   (Question │ Work │ Report, the rendered draft beside the Section's drawing) · Comments (Review Items
   citing R1.1 · E1.2) · Cover letter (paragraph │ the question it answers │ its text).
4. Comments are a report of type comments, `reports/qNN_<kind>-<MMDD>/` in the version that answers
   them (haipipe-paper-comments 1.1.0); never a Task.
5. Delivery: item cards (Manuscript · Letters · Checks · Sent), no third row.
6. A revision is a new version, starting as a copy of the last one's authored files.

Live: `servers/workbench-paper/paper_theme.py` (`version_spaces`) draws all of this on TestToLearn's
j01 and j02.


Open
----

See the drawing's red notes (open ?).

(write here, or mark the drawing in red)
