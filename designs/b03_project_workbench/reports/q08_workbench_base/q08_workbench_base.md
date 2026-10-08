# How is a workbench managed: one shared base, a theme each?

answers: Q08
answer-status: open

The drawing is `../../studio/s02-workbench-shared/s02-workbench-shared.excalidraw`: today who owns
which part (read off the code), the servers/ tree today and proposed, the Spaces each workbench
draws, the frame, the base and three themes, and the steps.

Done so far (261007)
--------------------

- `servers/workbench-shared` → `servers/workbench`: the base; with no theme, the vanilla workbench.
- `workbench-page` → `servers/workbench/task-page`: the Page Task's own views (the level is Task;
  a Task is a Page in every theme).
- `workbench-task` → `servers/workbench-work` and the skill `workbench-work`: the old "task" theme
  is the work theme.
- `runs_panel.py` moved into the base; the Guide's design is `studio/s31-guide/` (its 261002 drawings in `history/`).
- The frame: `servers/workbench/frame.py` + `frame_view.py`, route `/_board/workbench`; the work
  theme is its first user (`workbench-work/work_theme.py`); contract in `servers/workbench/README.md`;
  tests `servers/_host/tests/test_frame.py` (5). Theme sessions b11–b17 build on it.

Left: each theme's `<theme>_theme.py`; each theme's own `guide/`; the old per-theme pages move
onto the frame and retire; Job and Task levels of the vanilla content filled from s12 and s13.
