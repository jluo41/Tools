#!/bin/bash
# Canonical Ticket: <job>/tNN_<task>/runs/rNN_<run>.sh

set -uo pipefail

# Fill these for the Task.
TASK_NAME="extract_tables"
RUN_FAMILY="Execution"
RUN_OPERATION="raw-extraction"
RUN_TARGET="declared-raw-extraction"
REQUIRED_RESULTS=("manifest.json")
# Additional frozen inputs: "path|sha256". Relative paths resolve from Job.
RUN_INPUTS=()

# Extend when file existence is not the complete acceptance test.
result_gate() { return 0; }

fail_shape() {
  echo "==> BLOCKED: $1" >&2
  exit 2
}

TICKET="$(realpath "$0" 2>/dev/null || echo "$0")"
RUNS_DIR="$(cd "$(dirname "$TICKET")" && pwd)"
[ "$(basename "$RUNS_DIR")" = "runs" ] || fail_shape "Ticket must live in a Task Folder's runs/ lane"

TASK_FOLDER="$(cd "$RUNS_DIR/.." && pwd)"
TASK_SEG="$(basename "$TASK_FOLDER")"
JOB_FOLDER="$(cd "$TASK_FOLDER/.." && pwd)"
JOB_SEG="$(basename "$JOB_FOLDER")"
BLOCK_FOLDER="$(cd "$JOB_FOLDER/.." && pwd)"
BLOCK_SEG="$(basename "$BLOCK_FOLDER")"
TASKS_DIR="$(cd "$BLOCK_FOLDER/.." && pwd)"

case "$TASK_SEG" in t[0-9][0-9]_*) : ;; *) fail_shape "Task Folder must be named tNN_<noun>_<qualifier>" ;; esac
case "$JOB_SEG" in j[0-9][0-9]_*) : ;; *) fail_shape "Job must be named jNN_<noun>_<qualifier>" ;; esac
case "$BLOCK_SEG" in b[0-9][0-9]_*) : ;; *) fail_shape "Block must be named bNN_<noun>_<qualifier>" ;; esac
[ "$(basename "$TASKS_DIR")" = "tasks" ] || fail_shape "Block must be a direct child of tasks/"
[ -f "$TASK_FOLDER/$TASK_SEG.md" ] || fail_shape "Task Folder requires same-stem Page $TASK_SEG.md"

RUN_NAME="$(basename "$TICKET" .sh)"
case "$RUN_NAME" in r[0-9][0-9]_*) : ;; *) fail_shape "Run must be named rNN_<noun>_<qualifier>" ;; esac

CONFIG_REL="$TASK_SEG/scripts/config/$RUN_NAME.yaml"
TICKET_REL="$TASK_SEG/runs/$RUN_NAME.sh"
WORKER_REL="$TASK_SEG/scripts/$TASK_NAME.py"
CONFIG="$JOB_FOLDER/$CONFIG_REL"
WORKER="$JOB_FOLDER/$WORKER_REL"
[ -f "$CONFIG" ] || fail_shape "Run config missing: $CONFIG"
[ -f "$WORKER" ] || fail_shape "Task worker missing: $WORKER"

# The SPACE root, not the innermost git root. A Project may be a git submodule
# (example-1-data/Proj01-CGM-RawData is one), and the converter, the venv and code/
# live in the SPACE ABOVE it, so --show-toplevel points at the wrong tree and the
# notebook conversion fails with a path nobody can read. Walk for the marker.
REPO_ROOT=""
_walk="$JOB_FOLDER"
while [ "$_walk" != "/" ]; do
  if [ -f "$_walk/pyproject.toml" ] && [ -d "$_walk/code" ]; then REPO_ROOT="$_walk"; break; fi
  _walk="$(dirname "$_walk")"
done
[ -n "$REPO_ROOT" ] || REPO_ROOT="$(git -C "$JOB_FOLDER" rev-parse --show-toplevel)"
PROJECT_FOLDER="$(cd "$TASKS_DIR/.." && pwd)"
PROJECT="$(basename "$PROJECT_FOLDER")"
STARTED="$(date -Iseconds)"

# RESULT_STORE from a dispatcher wins. A standing Job store declaration is next.
STORE="${RESULT_STORE:-$(sed -n 's/^store:[[:space:]]*//p' "$JOB_FOLDER/src/config-defaults.yaml" 2>/dev/null | head -1)}"
if [ -n "$STORE" ]; then
  case "$STORE" in /*) : ;; *) STORE="$REPO_ROOT/$STORE" ;; esac
  JOB_REL="${JOB_FOLDER#"$TASKS_DIR"/}"
  [ "$JOB_REL" != "$JOB_FOLDER" ] || fail_shape "Job path cannot be mirrored below tasks/"
  OUTPUT_ROOT="$STORE/$JOB_REL"
else
  OUTPUT_ROOT="$JOB_FOLDER"
fi
export OUTPUT_ROOT

RUN_REL="$TASK_SEG/$RUN_NAME"
RESULTS_DIR="$OUTPUT_ROOT/$TASK_SEG/results/$RUN_NAME"
RUNTIME_YAML="$RESULTS_DIR/runtime.yaml"
NOTEBOOK_TEMPLATE="$OUTPUT_ROOT/$TASK_SEG/notebooks/.$RUN_NAME.source.ipynb"
NOTEBOOK_OUT="$OUTPUT_ROOT/$TASK_SEG/notebooks/$RUN_NAME.ipynb"
export RESULT_DIR="$RESULTS_DIR"

NOTEBOOK_MODE="$(grep -E '^\s*notebook:\s*(full|thin|off)\b' "$CONFIG" 2>/dev/null | awk '{print $2}' | head -1)"
NOTEBOOK_MODE="${NOTEBOOK_MODE:-full}"
NOTEBOOK_RECORD=$([ "$NOTEBOOK_MODE" = "off" ] && echo "(off)" || echo "${NOTEBOOK_OUT#"$OUTPUT_ROOT"/}")
[ ! -e "$RUNTIME_YAML" ] || fail_shape "Run receipt already exists; resume external execution for this identity or allocate a new Run"
mkdir -p "$RESULTS_DIR" "$OUTPUT_ROOT/$TASK_SEG/notebooks"

BP="${BLOCK_SEG%%_*}"
JP="${JOB_SEG%%_*}"
TP="${TASK_SEG%%_*}"
RP="${RUN_NAME%%_*}"
ADDRESS="${BP}${JP}${TP}${RP}"
ADDRESS_READABLE="${BP}.${JP}.${TP}.${RP}"

GIT_SHA="$(git -C "$JOB_FOLDER" rev-parse --short HEAD 2>/dev/null || echo unknown)"
GIT_DIRTY=$([ -n "$(git -C "$JOB_FOLDER" status --porcelain 2>/dev/null)" ] && echo true || echo false)
CONFIG_SHA256="$(shasum -a 256 "$CONFIG" 2>/dev/null | awk '{print $1}')"
CONFIG_SHA256="${CONFIG_SHA256:-unknown}"
HOST="$(hostname)/$(whoami)"
CMD="bash $TICKET"
TICKET_ARGS_JSON="$(python3 -c 'import json, sys; print(json.dumps(sys.argv[1:]))' "$@")"
RESULT_PATH="${RESULTS_DIR#"$OUTPUT_ROOT"/}"

_yaml_sq() { printf '%s' "$1" | sed "s/'/''/g"; }

RESOLVED_RUN_INPUTS=()
# bash 3.2, which is what macOS ships, treats "${arr[@]}" of an EMPTY array as
# unbound under `set -u` and aborts. The [@]+ form is empty-safe on 3.2 and on 5.
for input_spec in "${RUN_INPUTS[@]+"${RUN_INPUTS[@]}"}"; do
  input_path="${input_spec%%|*}"
  if [ "$input_path" = "$input_spec" ]; then input_sha=auto; else input_sha="${input_spec#*|}"; fi
  if [ "$input_sha" = auto ]; then
    case "$input_path" in /*) input_abs="$input_path" ;; *) input_abs="$JOB_FOLDER/$input_path" ;; esac
    input_sha="$(shasum -a 256 "$input_abs" 2>/dev/null | awk '{print $1}')"
    input_sha="${input_sha:-unresolved}"
  fi
  RESOLVED_RUN_INPUTS+=("${input_path}|${input_sha}")
done

emit_inputs_yaml() {
  printf "  - path: '%s'\n" "$(_yaml_sq "$CONFIG_REL")"
  printf "    sha256: '%s'\n" "$CONFIG_SHA256"
  for input_spec in "${RESOLVED_RUN_INPUTS[@]+"${RESOLVED_RUN_INPUTS[@]}"}"; do
    input_path="${input_spec%%|*}"
    input_sha="${input_spec#*|}"
    printf "  - path: '%s'\n" "$(_yaml_sq "$input_path")"
    printf "    sha256: '%s'\n" "$(_yaml_sq "$input_sha")"
  done
}

# Gate 1 belongs to this exact Task Folder.
CODE_REVIEW="$TASK_FOLDER/CODE_REVIEW.md"
SKIP_REVIEW_CONFIG="$(grep -E '^\s*skip_review:\s*true\b' "$CONFIG" 2>/dev/null || true)"
if [ -n "$SKIP_REVIEW_CONFIG" ] || [ "${HAIPIPE_SKIP_REVIEW:-0}" = "1" ]; then
  echo "==> [pre-flight] code review skipped by explicit flag" >&2
else
  [ -f "$CODE_REVIEW" ] || fail_shape "no CODE_REVIEW.md in $TASK_FOLDER"
  REVIEW_SHA="$(grep -E '^- git_sha:' "$CODE_REVIEW" 2>/dev/null | awk '{print $3}')"
  REVIEW_VERDICT="$(grep -E '^- overall_verdict:' "$CODE_REVIEW" 2>/dev/null | awk '{print $3}')"
  if [ "$REVIEW_SHA" != "$GIT_SHA" ] && [ "$GIT_SHA" != unknown ]; then
    fail_shape "CODE_REVIEW.md is stale: review=${REVIEW_SHA:-none}, current=$GIT_SHA"
  fi
  case "$REVIEW_VERDICT" in
    pass|skipped) : ;;
    warn) echo "==> [pre-flight] review verdict=warn; see $CODE_REVIEW" >&2 ;;
    fail) fail_shape "code review verdict=fail" ;;
    *) fail_shape "unrecognized code review verdict: ${REVIEW_VERDICT:-none}" ;;
  esac
fi

write_receipt() {
  receipt_status="$1"
  finished="$2"
  exit_code="$3"
  failure="$4"
  duration="$5"
  headline="$6"
  cat > "$RUNTIME_YAML.tmp" <<EOF
run:        $RUN_NAME
family:     $RUN_FAMILY
operation:  $RUN_OPERATION
target:     $RUN_TARGET
status:     $receipt_status
ticket:     $TICKET_REL
result:     $RESULT_PATH
inputs:
EOF
  emit_inputs_yaml >> "$RUNTIME_YAML.tmp"
  cat >> "$RUNTIME_YAML.tmp" <<EOF
worker:
  kind: script
  name: $WORKER_REL
started_at: $STARTED
finished_at: $finished
supersedes: null
failure: $failure
git_sha: $GIT_SHA
git_dirty: $GIT_DIRTY
host: $HOST
exit_code: $exit_code
cmd: $CMD
address: $ADDRESS
address_readable: $ADDRESS_READABLE
project: $PROJECT
config_file: $CONFIG_REL
config_sha256: $CONFIG_SHA256
settings:
  config_file: $CONFIG_REL
  ticket_args: $TICKET_ARGS_JSON
notebook: $NOTEBOOK_RECORD
duration: $duration
headline: $headline
EOF
  mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"
}

# This Ticket prepares the same extraction Run for external execution.
write_receipt running null null null null preparing-notebook
EXIT_CODE=0
python "$REPO_ROOT/code/scripts/convert_to_notebooks.py" "$WORKER" -o "$NOTEBOOK_TEMPLATE" \
  && cp "$NOTEBOOK_TEMPLATE" "$NOTEBOOK_OUT" || EXIT_CODE=$?
if [ "$EXIT_CODE" -ne 0 ]; then
  write_receipt failed "$(date -Iseconds)" "$EXIT_CODE" conversion-failed null conversion-failed
  exit "$EXIT_CODE"
fi
# Converter success is not extraction success. End time and execution exit remain unknown.
write_receipt blocked null null awaiting-external-execution null notebook-prepared
printf '%s\n' "Notebook prepared: $NOTEBOOK_OUT" \
  "Run $ADDRESS awaits Databricks execution under the same identity." \
  "Follow haipipe-task/ref/databricks-execution.md; bind config hash, cluster run id, logs and output manifest." \
  "Pattern 1: sync only permitted outputs. Pattern 2: raw/row-level data remains on the Volume." \
  "Finalize the execution receipt only after the declared Result gate passes."
exit 0
