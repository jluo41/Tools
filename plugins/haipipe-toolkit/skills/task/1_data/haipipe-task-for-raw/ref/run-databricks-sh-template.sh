#!/bin/bash
# =============================================================================
# Template for runs/<NAME>.sh — raw extraction task (CONVERT-ONLY)
# =============================================================================
# Unlike the standard run-sh-template.sh, this template does NOT execute
# the notebook via papermill. Raw extraction notebooks run on Databricks,
# not locally. This script:
#   1. Captures launch state -> results/<NAME>/runtime.yaml
#   2. Converts .py -> .ipynb (for Databricks upload)
#   3. Copies .ipynb to notebooks/<NAME>.ipynb
#   4. Finalizes runtime.yaml (status: converted)
#
# Variables you MUST set:
#   TASK_NAME — the .py basename (without .py) at task root
#
# Everything else is derived from $0 (the script path).
# =============================================================================

set -uo pipefail

# ─── Manual config: edit for the task ──────────────────────────────────────
TASK_NAME="01_stage1_extract_tables"     # the <task>.py at task root

# ─── 1. Resolve identity from $0 ───────────────────────────────────────────
RUN_NAME="$(basename "$0" .sh)"                            # e.g. extract_all
TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"                # absolute task-folder path
REPO_ROOT="$(git -C "$TASK_DIR" rev-parse --show-toplevel)"
STARTED="$(date -Iseconds)"

CONFIG="configs/${RUN_NAME}.yaml"
RESULTS_DIR="$TASK_DIR/results/${RUN_NAME}"
RUNTIME_YAML="$RESULTS_DIR/runtime.yaml"
NOTEBOOK_TEMPLATE="$TASK_DIR/${TASK_NAME}.ipynb"
NOTEBOOK_OUT="notebooks/${RUN_NAME}.ipynb"

mkdir -p "$RESULTS_DIR" "$TASK_DIR/notebooks"

# ─── 2. Capture launch state ───────────────────────────────────────────────
GIT_SHA="$(git -C "$TASK_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
HOST="$(hostname)/$(whoami)"
CMD="bash $(realpath "$0")"

# ─── 3. Write runtime.yaml (status: converting) ───────────────────────────
cat > "$RUNTIME_YAML.tmp" <<EOF
status:     converting
started:    $STARTED
git_sha:    $GIT_SHA
host:       $HOST
cmd:        $CMD
config:     $CONFIG
notebook:   $NOTEBOOK_OUT
execution:  databricks
note:       "Convert-only — upload notebook to Databricks to execute"
EOF
mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"

# ─── 4. Convert .py -> .ipynb (NO execution) ──────────────────────────────
EXIT_CODE=0
{
  python "$REPO_ROOT/code/scripts/convert_to_notebooks.py" \
         "$TASK_DIR/${TASK_NAME}.py" \
         -o "$NOTEBOOK_TEMPLATE"

  cp "$NOTEBOOK_TEMPLATE" "$TASK_DIR/$NOTEBOOK_OUT"
} || EXIT_CODE=$?

# ─── 5. Finalize runtime.yaml ─────────────────────────────────────────────
ENDED="$(date -Iseconds)"
STATUS=$([ $EXIT_CODE -eq 0 ] && echo converted || echo failed)

cat > "$RUNTIME_YAML.tmp" <<EOF
status:     $STATUS
started:    $STARTED
ended:      $ENDED
git_sha:    $GIT_SHA
host:       $HOST
exit_code:  $EXIT_CODE
cmd:        $CMD
config:     $CONFIG
notebook:   $NOTEBOOK_OUT
execution:  databricks
note:       "Convert-only — upload notebook to Databricks to execute"
EOF
mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"

# ─── 6. Print next steps ──────────────────────────────────────────────────
if [ $EXIT_CODE -eq 0 ]; then
  echo ""
  echo "==> Notebook converted: $TASK_DIR/$NOTEBOOK_OUT"
  echo ""
  echo "    Next steps:"
  echo "    1. Upload notebook to Databricks workspace"
  echo "    2. Attach to a cluster and run"
  echo "    3. Sync extracted parquet files to local _WorkSpace/0-RawStore/"
  echo ""
fi

exit $EXIT_CODE
