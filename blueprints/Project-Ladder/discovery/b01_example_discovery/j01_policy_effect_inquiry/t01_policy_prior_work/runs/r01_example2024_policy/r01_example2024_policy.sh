#!/usr/bin/env bash
# r01_example2024_policy: a Discovery Paper Run of Tools' placeholder discovery example (b01.j01.t01.r01).
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
  --task . --run "$RUN" --address b01.j01.t01.r01 \
  --title '<A policy> and <a service>: a placeholder study' \
  --authors 'Ann Example; Ben Sample' \
  --year '2024' \
  --venue 'Example Journal' \
  --doi '10.0000/example.2024.001' \
  --abstract 'A placeholder abstract for a public example. <A policy> changed how <a group> receives <a service> in one setting. The study compares the year before the change with the year after it and finds that <an outcome> rose by a made-up amount. Every word and number here is a placeholder.' \
  --bib-file 'scripts/placeholder.bib' \
  --bib-key 'example2024policy' \
  --verification 'checked against its placeholder entry: title, authors and year agree' \
  --trigger 'the Paper-Example'\''s introduction cites it' \
  --readout '<The policy> raised <an outcome> in the year after it began, in one setting (a placeholder finding). It compares the year before with the year after.' \
  --reuse 'The introduction'\''s first sentence cites it for what <the policy> changed.'
sed -i.bak -E "s/^status: .*/status: complete/" "$RUN_DIR/run.yaml" && rm -f "$RUN_DIR/run.yaml.bak"
