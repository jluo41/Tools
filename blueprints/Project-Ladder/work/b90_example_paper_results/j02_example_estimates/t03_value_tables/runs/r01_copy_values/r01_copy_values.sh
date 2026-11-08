#!/usr/bin/env bash
# r01_copy_values: ticket of the example Block of the work theme (b90), scaffolded 261105. Placeholders only: copy the returned values unchanged.
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
started_by: '261105: the example Block of the work theme, placeholders only'
ticket: runs/$RUN_NAME/$RUN_NAME.sh
worker: this ticket
RECEIPT
  sed -i.bak -E "s/^status: .*/status: $([ "$rc" = 0 ] && echo done || echo failed)/" "$RUN_DIR/run.yaml" && rm -f "$RUN_DIR/run.yaml.bak"
  exit "$rc"
}
trap finish EXIT
mkdir -p "$RESULT_DIR/main" "$RESULT_DIR/subgroup"
J="$TASK_DIR/.."
cp "$J/t01_example_main/runs/r01_example_main/result/values.csv" "$RESULT_DIR/main/values.csv"
cp "$J/t02_example_subgroup/runs/r01_example_subgroup/result/values.csv" "$RESULT_DIR/subgroup/values.csv"
echo "copied from blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t01_example_main/runs/r01_example_main/result" > "$RESULT_DIR/main/SOURCE.txt"
echo "copied from blueprints/Project-Ladder/work/b90_example_paper_results/j02_example_estimates/t02_example_subgroup/runs/r01_example_subgroup/result" > "$RESULT_DIR/subgroup/SOURCE.txt"
echo "2 files copied unchanged" > "$RESULT_DIR/headline.txt"
