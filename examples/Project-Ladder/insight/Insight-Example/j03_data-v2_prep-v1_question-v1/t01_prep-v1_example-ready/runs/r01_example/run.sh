#!/bin/bash
# run.sh · the prep Run of a Board Job: the whole prep version on the data version's raw export (hai-insight
# ref/run_prep.py). The same lines in every ticket; the folder name is the Run (r01_<dataset>).
R="$(cd "$(dirname "$0")" && while [ ! -f env.sh ] && [ "$PWD" != / ]; do cd ..; done; pwd)"
source "$R/env.sh" >/dev/null 2>&1
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="$R/.venv/bin/python"; [ -x "$PY" ] || PY=python3
exec "$PY" "$R/Tools/plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/ref/run_prep.py" \
  "$(cd "$HERE/../.." && pwd)" "$(basename "$HERE")"
