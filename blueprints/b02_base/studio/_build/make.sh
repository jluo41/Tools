#!/bin/bash
# Rebuild every b02 studio drawing and its .png preview; a rebuild keeps a person's marks.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
STUDIO="$(cd "$HERE/.." && pwd)"
PY="${PYTHON:-python3}"
RENDER="$STUDIO/../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py"   # haipipe-studio (b03 s21, 261007)
for d in "$STUDIO"/s[0-9][0-9]-*/; do
  t="$(basename "$d")"
  [ -f "$d/build_${t//-/_}.py" ] || continue
  "$PY" "$d/build_${t//-/_}.py"
  "$PY" "$RENDER" "$d/$t.excalidraw" "$d/$t.png"
done
