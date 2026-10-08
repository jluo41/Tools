#!/bin/bash
# Rebuild every b04 studio drawing and its .png preview; a rebuild keeps a person's marks.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
STUDIO="$(cd "$HERE/.." && pwd)"
PY="${PYTHON:-python3}"
# b03's preview renderer, found by its file (the Block folder has been renamed before)
RENDER="$STUDIO/../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py"   # haipipe-studio (b03 s21, 261007)
for t in s01-skill-folder-changes s02-skill-layers s03-path-lookup s04-theme-shape; do
  "$PY" "$STUDIO/$t/build_${t//-/_}.py"
  "$PY" "$RENDER" "$STUDIO/$t/$t.excalidraw" "$STUDIO/$t/$t.png"
done
