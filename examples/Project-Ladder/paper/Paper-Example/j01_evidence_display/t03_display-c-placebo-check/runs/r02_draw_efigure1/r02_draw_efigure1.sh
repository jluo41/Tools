#!/usr/bin/env bash
# r02_draw_efigure1: ticket of Display C (eFigure 1, the placebo check) in Tools' Paper-Example, 261110. Placeholders only.
# Reads the value Run j02_evidence_value/t01_values-sample/runs/r01_read_values (result/values.yaml) by id, never work/; then builds result/preview.pdf.
# A closed Run (result/runtime.yaml says completed) refuses to run again: a change is a new Run.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_NAME="$(basename "$0" .sh)"
TASK_DIR="$(cd "$RUN_DIR/../.." && pwd)"
RESULT_DIR="$RUN_DIR/result"
export RESULT_DIR
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
if [ -f "$RESULT_DIR/runtime.yaml" ] && grep -q '^status: completed' "$RESULT_DIR/runtime.yaml"; then
  echo "$RUN_NAME is closed (result/runtime.yaml says completed): a change is a new Run" >&2
  exit 3
fi
rm -rf "$RESULT_DIR"; mkdir -p "$RESULT_DIR"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
finish() {
  local rc=$?
  cat > "$RESULT_DIR/runtime.yaml" <<RECEIPT
run: $RUN_NAME
status: $([ "$rc" = 0 ] && echo completed || echo failed)
exit_code: $rc
started_at: '$STARTED_AT'
finished_at: '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
started_by: '261110: the evidence chain rules, placeholders only'
ticket: runs/$RUN_NAME/$RUN_NAME.sh
worker: draw_placebo_check.py
reads: j02_evidence_value/t01_values-sample/runs/r01_read_values (result/values.yaml)
RECEIPT
  sed -i.bak -E "s/^status: .*/status: $([ "$rc" = 0 ] && echo done || echo failed)/" "$RUN_DIR/run.yaml" && rm -f "$RUN_DIR/run.yaml.bak"
  exit "$rc"
}
trap finish EXIT
"$PY" "$TASK_DIR/scripts/draw_placebo_check.py"
"$PY" "$TK/skills/1_base/display/hai-display/scripts/build_preview.py" "$RESULT_DIR" --look paper
