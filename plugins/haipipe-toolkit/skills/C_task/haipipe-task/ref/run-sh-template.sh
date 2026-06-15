#!/bin/bash
# =============================================================================
# Template for runs/<NAME>.sh
# =============================================================================
# Each run.sh is a thin wrapper that:
#   1. Snapshots launch state -> results/<NAME>/runtime.yaml (status: running)
#   2. Convert .py -> template .ipynb
#   3. papermill execute -> notebooks/<NAME>.ipynb
#   4. Finalize runtime.yaml (status: ok | failed)
#
# Notebook policy (configs/<RUN>.yaml -> _meta.notebook: full | thin | off):
#   full (default) keep the executed notebook with all outputs
#   thin           execute, then clear cell outputs (small record; keeps code+params,
#                  drops bulky stream/image output) — good for heavy compute (training/data)
#   off            execute via papermill (so config injection + the .py run identically),
#                  but DON'T keep the .ipynb artifact at all
# All three execute the .py the same way; they differ only in what notebook is retained.
#
# Variables you MUST set:
#   TASK_NAME — the .py basename (without .py) at task root
#
# Everything else is derived from $0 (the script path).
# =============================================================================

set -uo pipefail

# ─── Manual config: edit for the task ──────────────────────────────────────
TASK_NAME="01_pretrain_baseline"          # the <task>.py at task root

# ─── 1. Resolve identity from $0 ───────────────────────────────────────────
RUN_NAME="$(basename "$0" .sh)"                            # e.g. run_seed42_baseline
TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"                # absolute task-folder path
REPO_ROOT="$(git -C "$TASK_DIR" rev-parse --show-toplevel)"
STARTED="$(date -Iseconds)"                                # 2026-05-24T14:30:01-04:00

CONFIG="configs/${RUN_NAME}.yaml"
RESULTS_DIR="$TASK_DIR/results/${RUN_NAME}"
RUNTIME_YAML="$RESULTS_DIR/runtime.yaml"
NOTEBOOK_TEMPLATE="$TASK_DIR/${TASK_NAME}.ipynb"
NOTEBOOK_OUT="notebooks/${RUN_NAME}.ipynb"

# Notebook policy: full (keep) | thin (keep, outputs cleared) | off (execute, don't keep).
NOTEBOOK_MODE="$(grep -E '^\s*notebook:\s*(full|thin|off)\b' "$TASK_DIR/$CONFIG" 2>/dev/null | awk '{print $2}' | head -1)"
NOTEBOOK_MODE="${NOTEBOOK_MODE:-full}"
NOTEBOOK_RECORD=$([ "$NOTEBOOK_MODE" = "off" ] && echo "(off)" || echo "$NOTEBOOK_OUT")

mkdir -p "$RESULTS_DIR" "$TASK_DIR/notebooks"

# ─── 2. Capture launch state ───────────────────────────────────────────────
GIT_SHA="$(git -C "$TASK_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
HOST="$(hostname)/$(whoami)"
CMD="bash $(realpath "$0")"

# ─── 2a. Pre-flight code review gate ───────────────────────────────────────
# Block launch unless a fresh CODE_REVIEW.md (produced by the Run Script Reviewer
# agent) exists for this task-folder and matches the current git_sha.
# Skip mechanisms (any one):
#   • _meta.skip_review: true   in configs/<RUN_NAME>.yaml
#   • HAIPIPE_SKIP_REVIEW=1     env var at launch
# Verdict semantics:
#   pass | skipped → proceed
#   warn           → proceed with stderr warning
#   fail | <none>  → exit 2; user must run the agent or fix code
CODE_REVIEW="$TASK_DIR/CODE_REVIEW.md"
SKIP_REVIEW_CONFIG="$(grep -E '^\s*skip_review:\s*true\b' "$TASK_DIR/$CONFIG" 2>/dev/null || true)"
if [ -n "$SKIP_REVIEW_CONFIG" ] || [ "${HAIPIPE_SKIP_REVIEW:-0}" = "1" ]; then
  echo "==> [pre-flight] code review SKIPPED (explicit skip flag)" >&2
else
  if [ ! -f "$CODE_REVIEW" ]; then
    echo "==> [pre-flight] BLOCKED: no CODE_REVIEW.md in $TASK_DIR" >&2
    echo "    Run the Task Reviewer agent (GATE 1) on this task-folder first," >&2
    echo "    or set HAIPIPE_SKIP_REVIEW=1 to bypass." >&2
    echo "    Agent: Tools/plugins/haipipe-toolkit/skills/C_task/agents/haipipe-task-reviewer-agent.md" >&2
    exit 2
  fi
  REVIEW_SHA="$(grep -E '^- git_sha:' "$CODE_REVIEW" 2>/dev/null | awk '{print $3}')"
  REVIEW_VERDICT="$(grep -E '^- overall_verdict:' "$CODE_REVIEW" 2>/dev/null | awk '{print $3}')"
  if [ "$REVIEW_SHA" != "$GIT_SHA" ] && [ "$GIT_SHA" != "unknown" ]; then
    echo "==> [pre-flight] BLOCKED: CODE_REVIEW.md is stale" >&2
    echo "    review git_sha = ${REVIEW_SHA:-<none>}, current git_sha = $GIT_SHA" >&2
    echo "    Re-run the Task Reviewer agent (GATE 1), or set HAIPIPE_SKIP_REVIEW=1." >&2
    exit 2
  fi
  case "$REVIEW_VERDICT" in
    pass|skipped)
      echo "==> [pre-flight] code review verdict=$REVIEW_VERDICT (proceeding)" >&2
      ;;
    warn)
      echo "==> [pre-flight] code review verdict=WARN (proceeding — see $CODE_REVIEW)" >&2
      ;;
    fail)
      echo "==> [pre-flight] BLOCKED: code review verdict=FAIL" >&2
      echo "    See $CODE_REVIEW for action items." >&2
      echo "    Fix and re-run the agent, or set HAIPIPE_SKIP_REVIEW=1 to override." >&2
      exit 2
      ;;
    *)
      echo "==> [pre-flight] BLOCKED: CODE_REVIEW.md has unrecognized verdict='$REVIEW_VERDICT'" >&2
      echo "    Expected one of: pass | warn | fail | skipped" >&2
      exit 2
      ;;
  esac
fi

# ─── 3. Write runtime.yaml (status: running, atomic) ───────────────────────
cat > "$RUNTIME_YAML.tmp" <<EOF
status:     running
started:    $STARTED
git_sha:    $GIT_SHA
host:       $HOST
cmd:        $CMD
config:     $CONFIG
notebook:   $NOTEBOOK_RECORD
EOF
mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"

# ─── 4. Execute (convert + papermill, per notebook policy) ─────────────────
# off → execute to a temp notebook we delete after; full/thin → keep the real one.
if [ "$NOTEBOOK_MODE" = "off" ]; then
  NB_TARGET="$TASK_DIR/notebooks/.${RUN_NAME}.tmp.ipynb"
else
  NB_TARGET="$TASK_DIR/$NOTEBOOK_OUT"
fi

EXIT_CODE=0
{
  python "$REPO_ROOT/code/scripts/convert_to_notebooks.py" \
         "$TASK_DIR/${TASK_NAME}.py" \
         -o "$NOTEBOOK_TEMPLATE"

  papermill "$NOTEBOOK_TEMPLATE" "$NB_TARGET" \
            -p config "$TASK_DIR/$CONFIG"
} || EXIT_CODE=$?

# Apply notebook policy (does not affect EXIT_CODE — the run already happened).
case "$NOTEBOOK_MODE" in
  thin) jupyter nbconvert --clear-output --inplace "$NB_TARGET" 2>/dev/null \
          || echo "==> [warn] notebook=thin: clear-output failed; keeping full notebook" >&2 ;;
  off)  rm -f "$NB_TARGET" ;;
esac

# ─── 5. Finalize runtime.yaml ──────────────────────────────────────────────
ENDED="$(date -Iseconds)"
DURATION="$(python3 -c "
from datetime import datetime
s = datetime.fromisoformat('$STARTED'); e = datetime.fromisoformat('$ENDED')
d = e - s; m, s = divmod(int(d.total_seconds()), 60); h, m = divmod(m, 60)
print(f'{h}h{m:02d}m' if h else f'{m}m{s:02d}s')
")"
STATUS=$([ $EXIT_CODE -eq 0 ] && echo ok || echo failed)
HEADLINE="$(python3 -c "
import json
try:
    d = json.load(open('$RESULTS_DIR/metrics.json'))
    print(d.get('summary', {}).get('headline') or '-')
except Exception:
    print('-')
")"

cat > "$RUNTIME_YAML.tmp" <<EOF
status:     $STATUS
started:    $STARTED
ended:      $ENDED
duration:   $DURATION
git_sha:    $GIT_SHA
host:       $HOST
exit_code:  $EXIT_CODE
cmd:        $CMD
config:     $CONFIG
notebook:   $NOTEBOOK_RECORD
headline:   $HEADLINE
EOF
mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"

# ─── 6. Regenerate task-log.md (delegate to haipipe-task-logging) ─────────
REGEN="$REPO_ROOT/Tools/plugins/haipipe-toolkit/skills/C_task/haipipe-task-logging/ref/regen_task_log.py"
if [ -f "$REGEN" ]; then
  python3 "$REGEN" "$TASK_DIR" 2>/dev/null \
    || echo "==> [warn] task-log regen failed (non-fatal, see $REGEN)" >&2
fi

exit $EXIT_CODE
