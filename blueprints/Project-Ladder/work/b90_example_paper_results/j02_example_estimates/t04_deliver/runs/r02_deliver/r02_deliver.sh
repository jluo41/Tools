#!/usr/bin/env bash
# r02_deliver: ticket of the example Block of the work theme (b90), made 261106. Placeholders only: a clean copy of the agreed estimates into this Task's address in the Block delivery/ (delivery/j02_example_estimates/t04_deliver/), under -v1; never a sent version written over.
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
started_by: '261106: the example Block of the work theme, placeholders only'
ticket: runs/$RUN_NAME/$RUN_NAME.sh
worker: deliver.py
RECEIPT
  sed -i.bak -E "s/^status: .*/status: $([ "$rc" = 0 ] && echo done || echo failed)/" "$RUN_DIR/run.yaml" && rm -f "$RUN_DIR/run.yaml.bak"
  exit "$rc"
}
trap finish EXIT
export HAIPIPE_TOOLKIT="$TK" PYTHONDONTWRITEBYTECODE=1
"$PY" "$TASK_DIR/scripts/deliver.py"
