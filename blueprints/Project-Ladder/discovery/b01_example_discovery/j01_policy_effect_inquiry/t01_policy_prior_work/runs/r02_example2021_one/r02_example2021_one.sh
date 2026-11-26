#!/usr/bin/env bash
# r02_example2021_one: a Discovery Paper Run of Tools' placeholder discovery example (b01.j01.t01.r02).
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
  --task . --run "$RUN" --address b01.j01.t01.r02 \
  --title '<An outcome> in one setting: a placeholder' \
  --authors 'Ann Example' \
  --year '2021' \
  --venue 'Example Journal' \
  --abstract 'A placeholder abstract for a public example. In one setting, <an outcome> was measured before and after <a policy> began, over two years. It rose in both years after the change, by made-up amounts. Every word and number here is a placeholder, and no real study stands behind it.' \
  --bib-file 'scripts/placeholder.bib' \
  --bib-key 'example2021one' \
  --verification 'checked against its placeholder entry: title, author and year agree' \
  --trigger 'the Paper-Example'\''s introduction cites it' \
  --readout '<An outcome> rose again in a second year of the same setting (a placeholder finding).' \
  --reuse 'The introduction cites it for the effect in one setting.'
sed -i.bak -E "s/^status: .*/status: complete/" "$RUN_DIR/run.yaml" && rm -f "$RUN_DIR/run.yaml.bak"
