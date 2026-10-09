# Base skills built: every frame button names its owner

## Ask

Build the base skills s21 proposes (haipipe-report, haipipe-board, haipipe-job, haipipe-studio; extend haipipe-run) so every Run button of the frame has an owning skill; then phase 5 and the open calls.

## Summary

Four skills built (report 0.1.1, board 2.0.0, job 0.1.0, studio 0.4.1), haipipe-run 0.32 extended (run-types-by-space, soft_run.py), haipipe-question 0.6.0 asks only. Every frame button names its skill. Phase 5: canvas.py, render_png.py and build_report_drawing.py live only in the skills; all builders import from there. Decided: delivery stays in each level skill (s21-D03); checked is not a fourth state (s21-D04); folder moves handed to b04. Studio look: black, red = open, green = change, enforced by canvas.write (slide drafts exempt). Slide drafts moved to the new excalidraw-slide. Paper Boards read by the ladder audit.

## Changed

- `Tools/designs/b03_project_workbench/studio/s21_project-run-skill/s21_project-run-skill.md`
- `Tools/designs/b03_project_workbench/studio/s21_project-run-skill/build_s21_project_run_skill.py`
- `Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-report`
- `Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-board`
- `Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-job`
- `Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio`
- `Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-slide`
- `Tools/plugins/haipipe-toolkit/servers/workbench/frame.py`
