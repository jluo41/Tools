#!/bin/bash
# run.sh · one hard Run of a plan-C Job: this Task's question on this segment (hai-insight ref/run_job.py).
# The same lines in every ticket; the folder name is the Run (rNN_<segment>).
R="$(cd "$(dirname "$0")" && while [ ! -f env.sh ] && [ "$PWD" != / ]; do cd ..; done; pwd)"
source "$R/env.sh" >/dev/null 2>&1
HERE="$(cd "$(dirname "$0")" && pwd)"
exec "$R/.venv/bin/python" "$R/Tools/plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/ref/run_job.py" \
  "$(cd "$HERE/../.." && pwd)" "$(basename "$HERE")"
