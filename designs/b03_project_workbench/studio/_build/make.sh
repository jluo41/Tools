#!/bin/bash
# Rebuild every b03 studio drawing and its .png preview. Run from anywhere: make.sh
# A rebuild keeps whatever a person drew on the canvas (see the builder's docstring).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
STUDIO="$(cd "$HERE/.." && pwd)"
TOOLS="$(cd "$STUDIO/../../.." && pwd)"           # the Tools checkout: the skills live here
PY="${PYTHON:-python3}"
SKILLS="$TOOLS/plugins/haipipe-toolkit/skills/1_base/project"   # haipipe-report and haipipe-studio (b03 s21, 261007)
RENDER="$SKILLS/haipipe-studio/scripts/render_png.py"         # the previewer (moved from _build/, 261007)
# the first scratches (project-scratch, ladder-grid, ladder-trees) were removed from studio/ on 261007;
# their builders stay in _build/ but are not run, so a rebuild does not bring the drawings back
# "$PY" "$HERE/build_project_scratch.py" "$STUDIO/project-scratch.excalidraw"
# "$PY" "$HERE/build_ladder_grid.py" "$STUDIO/ladder-grid.excalidraw"
# "$PY" "$HERE/build_ladder_trees.py" "$STUDIO/ladder-trees.excalidraw"
# studio topics: each sNN-<topic>/ holds its own builder
S01="$STUDIO/s01-overall-tree-structure"
"$PY" "$S01/build_ladder_v4.py"              # frame 1 -> s01-overall-tree-structure.excalidraw
"$PY" "$STUDIO/s04-studio-and-report/build_s04_studio_and_report.py"
"$PY" "$STUDIO/s05-runs/build_s05_runs.py"
# frames 2-4 as their own topics, each its own drawing
"$PY" "$STUDIO/s11-block-variants/build_s11_block_variants.py"
"$PY" "$STUDIO/s12-job-variants/build_s12_job_variants.py"
"$PY" "$STUDIO/s13-task-variants/build_s13_task_variants.py"
# drawn from these definitions in another Block: b11's insight ladder (moved from s06, 261007)
B11="$(cd "$STUDIO/../../b11_theme_insight/studio" && pwd)"
"$PY" "$B11/s01-insight-ladder/build_s01_insight_ladder.py"
# and b12's design ladder (moved from s07, 261007)
B12="$(cd "$STUDIO/../../b12_theme_design/studio" && pwd)"
"$PY" "$B12/s01-design/build_s01_design.py"
for b in "$B12"/s1[123]-design-*/build_s1*_design_*.py; do "$PY" "$b"; done   # b12: one level per drawing (261007)
# and b13-b17's theme ladders (261007), one per theme, all drawn by theme_ladder.py
THEMES=()
for b in cowork discovery labeling paper work; do
  d="$(cd "$STUDIO/../.." && pwd)/$(cd "$STUDIO/../.." && ls -d b1[3-7]_theme_$b)/studio/s01-$b-ladder"
  "$PY" "$d/build_s01_${b}_ladder.py"
  THEMES+=("$d/s01-$b-ladder.excalidraw")
done
# the workbench topics (b02 merged into b03, 261007): the base frame and the Guide
"$PY" "$STUDIO/s02-workbench-shared/build_s02_workbench_shared.py"
"$PY" "$STUDIO/s32-element-ui/build_s32_element_ui.py"     # the element gallery, from its shots/ (--shoot to retake)
# each theme's own element gallery, built on b03's (261008): b12 design, b16 paper; a theme without one is skipped
THEME_S32=()
for b in "$(cd "$STUDIO/../.." && pwd)"/b1[1-7]_theme_*/studio/s32-*-element-ui/build_s32_*_element_ui.py; do
  [ -f "$b" ] || continue
  "$PY" "$b" || { echo "skipped $b: it failed (its session may be retaking shots)" >&2; continue; }
  THEME_S32+=("$(dirname "$b")/$(basename "$(dirname "$b")").excalidraw")
done
"$PY" "$STUDIO/s31-guide/build_s31_guide.py"
# the server topics (s51 on): how the server runs, read off its code
"$PY" "$STUDIO/s51-server-runtime/build_s51_server_runtime.py"
# s21: the base Runs and skills, read off the frame and the skills
"$PY" "$STUDIO/s21_project-run-skill/build_s21_project_run_skill.py"
# the report drawings: every reports/qNN_<topic>/ whose .md lists its ## Figures, built from studio frames
REPORTS=()
for md in "$STUDIO"/../reports/q*/q*.md; do
  [ -f "$md" ] && grep -q "^## Figures" "$md" || continue
  "$PY" "$SKILLS/haipipe-report/scripts/build_report_drawing.py" "$(dirname "$md")" >/dev/null
  REPORTS+=("${md%.md}.excalidraw")
done
for f in "${REPORTS[@]}" "${THEMES[@]}" ${THEME_S32[@]+"${THEME_S32[@]}"} "$B11"/s01-insight-ladder/s01-insight-ladder.excalidraw "$B12"/s01-design/s01-design.excalidraw "$B12"/s1[123]-design-*/s1*-design-*.excalidraw "$S01"/s01-overall-tree-structure.excalidraw "$STUDIO"/s0[2-5]-*/s0*.excalidraw "$STUDIO"/s1[1-3]-*/s1*.excalidraw "$STUDIO"/s3[0-9]-*/s3*.excalidraw "$STUDIO"/s5[0-9]-*/s5*.excalidraw "$STUDIO"/s21_project-run-skill/s21_project-run-skill.excalidraw; do
  "$PY" "$RENDER" "$f" "${f%.excalidraw}.png"
done
