#!/usr/bin/env bash
# r01_copy_estimates: ticket of the Values tabs example; hand-kept beside scripts/tables.yaml. Placeholders only.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_NAME="$(basename "$0" .sh)"
TASK_DIR="$(cd "$RUN_DIR/../.." && pwd)"
RESULT_DIR="$RUN_DIR/result"
export RESULT_DIR
TK=""; PY="${HAIPIPE_PYTHON:-}"; D="$RUN_DIR"; SPACE=""
while [ "$D" != "/" ]; do
  for c in "$D/Tools/plugins/haipipe-toolkit" "$D/plugins/haipipe-toolkit"; do
    [ -z "$TK" ] && [ -d "$c" ] && { TK="$c"; SPACE="$D"; }
  done
  [ -z "$PY" ] && [ -x "$D/.venv/bin/python" ] && PY="$D/.venv/bin/python"
  D="$(dirname "$D")"
done
[ -n "$TK" ] || { echo "haipipe-toolkit not found above $RUN_DIR" >&2; exit 2; }
PY="${PY:-$(command -v python3)}"
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
started_by: 'JL 261104: the Values tabs as the paper Board standard'
ticket: runs/$RUN_NAME/$RUN_NAME.sh
worker: this ticket
RECEIPT
  exit "$rc"
}
trap finish EXIT
SRC="blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t01_example_main/runs/r01_example_main/result"
mkdir -p "$RESULT_DIR/estimates"
cp "$SPACE/$SRC/values.csv" "$RESULT_DIR/estimates/values.csv"
echo "copied from $SRC" > "$RESULT_DIR/estimates/SOURCE.txt"
cat > "$RESULT_DIR/values.json" <<'JSON'
{"V_main_b": {"value": 2.3461, "text": "2.35", "says": "points, the main association", "source": "b90 j02 t01 r01 · values.csv · main.b"}}
JSON
echo "1 file copied, 1 printed value" > "$RESULT_DIR/headline.txt"
