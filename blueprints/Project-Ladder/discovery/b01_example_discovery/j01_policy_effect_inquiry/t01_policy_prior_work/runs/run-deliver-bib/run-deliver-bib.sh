#!/usr/bin/env bash
# run-deliver-bib: the Delivery Run of Tools' placeholder discovery example (b01.j01.t01). It builds the Task's Evidence
# Bib from its complete Paper Results (paper_runs.py build-bib) and hands a clean copy over to this Task's address in the
# Block's delivery/, with its draft row in delivery/delivery.md (scripts/deliver_bib.py). Rerun to rebuild both.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_NAME="$(basename "$0" .sh)"
TASK_DIR="$(cd "$RUN_DIR/../.." && pwd)"
RESULT_DIR="$RUN_DIR/result"
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
export TASK_DIR RESULT_DIR HAIPIPE_TOOLKIT="$TK" PYTHONDONTWRITEBYTECODE=1
rm -rf "$RESULT_DIR"; mkdir -p "$RESULT_DIR"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
finish() {
  local rc=$?
  local head=""
  [ -f "$RESULT_DIR/headline.txt" ] && head="$(head -n 1 "$RESULT_DIR/headline.txt" | sed 's/"/\\"/g')"
  cat > "$RESULT_DIR/runtime.yaml" <<RECEIPT
run: $RUN_NAME
status: $([ "$rc" = 0 ] && echo complete || echo failed)
headline: "$head"
exit_code: $rc
started_at: '$STARTED_AT'
finished_at: '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
ticket: runs/$RUN_NAME/$RUN_NAME.sh
worker: scripts/deliver_bib.py
placeholder: true
RECEIPT
  sed -i.bak -E "s/^status: .*/status: $([ "$rc" = 0 ] && echo done || echo failed)/" "$RUN_DIR/run.yaml" && rm -f "$RUN_DIR/run.yaml.bak"
  exit "$rc"
}
trap finish EXIT
"$PY" "$TASK_DIR/scripts/deliver_bib.py"
