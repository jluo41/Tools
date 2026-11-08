#!/usr/bin/env bash
# r03_example2022_two: a Discovery Paper Run of Tools' placeholder discovery example (b01.j01.t01.r03).
# A made-up paper: paper_result_build.py --placeholder writes its Result (receipt, Card, facts, source access and one
# Bib entry copied from scripts/placeholder.bib) from the metadata below, with no network call. Rerun to rebuild.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN="$(basename "$0" .sh)"
TASK_DIR="$(cd "$RUN_DIR/../.." && pwd)"
TK=""; PY="${HAIPIPE_PYTHON:-}"; D="$RUN_DIR"
while [ "$D" != "/" ]; do
  for c in "$D/Tools/plugins/haipipe-toolkit" "$D/plugins/haipipe-toolkit"; do
    [ -z "$TK" ] && [ -d "$c" ] && TK="$c"
  done
  [ -z "$PY" ] && [ -x "$D/.venv/bin/python" ] && PY="$D/.venv/bin/python"
  D="$(dirname "$D")"
done
[ -n "$TK" ] || { echo "haipipe-toolkit not found above $RUN_DIR" >&2; exit 2; }
PY="${PY:-$(command -v python3)}"
export PYTHONDONTWRITEBYTECODE=1
cd "$TASK_DIR"
"$PY" "$TK/skills/2_theme/discovery/haipipe-discovery/scripts/paper_result_build.py" --placeholder \
  --task . --run "$RUN" --address b01.j01.t01.r03 \
  --title '<An outcome> in a second setting: a placeholder' \
  --authors 'Ben Sample; Ann Example' \
  --year '2022' \
  --venue 'Example Review' \
  --bib-file 'scripts/placeholder.bib' \
  --bib-key 'example2022two' \
  --verification 'NEEDS a person: its venue and year are not checked against a source' \
  --trigger 'the Paper-Example'\''s introduction cites it' \
  --readout 'Read from its placeholder metadata only: it names a second setting, and its finding is not read yet.' \
  --reuse 'The introduction cites it beside r02; its citation waits for a check.'
sed -i.bak -E "s/^status: .*/status: complete/" "$RUN_DIR/run.yaml" && rm -f "$RUN_DIR/run.yaml.bak"
