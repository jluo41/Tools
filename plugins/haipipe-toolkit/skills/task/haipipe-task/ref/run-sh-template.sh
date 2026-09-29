#!/bin/bash
# Canonical Ticket: <job>/tNN_<task>/runs/rNN_<run>.sh

set -uo pipefail

# Fill these for the Task.
TASK_NAME="worker"
RUN_FAMILY="Execution"
RUN_OPERATION="task-execution"
RUN_TARGET="bounded-target"
REQUIRED_RESULTS=("metrics.json")
# Additional declared input files: "path". Relative paths resolve from Job.
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
NOTEBOOK_TEMPLATE="$OUTPUT_ROOT/$TASK_SEG/notebooks/_source.ipynb"
NOTEBOOK_OUT="$OUTPUT_ROOT/$TASK_SEG/notebooks/$RUN_NAME.ipynb"
export RESULT_DIR="$RESULTS_DIR"

NOTEBOOK_MODE="$(grep -E '^\s*notebook:\s*(full|thin|off)\b' "$CONFIG" 2>/dev/null | awk '{print $2}' | head -1)"
NOTEBOOK_MODE="${NOTEBOOK_MODE:-full}"
NOTEBOOK_RECORD=$([ "$NOTEBOOK_MODE" = "off" ] && echo "(off)" || echo "${NOTEBOOK_OUT#"$OUTPUT_ROOT"/}")
mkdir -p "$RESULTS_DIR" "$OUTPUT_ROOT/$TASK_SEG/notebooks"

BP="${BLOCK_SEG%%_*}"
JP="${JOB_SEG%%_*}"
TP="${TASK_SEG%%_*}"
RP="${RUN_NAME%%_*}"
ADDRESS="${BP}${JP}${TP}${RP}"
ADDRESS_READABLE="${BP}.${JP}.${TP}.${RP}"

GIT_SHA="$(git -C "$JOB_FOLDER" rev-parse --short HEAD 2>/dev/null || echo unknown)"
GIT_DIRTY=$([ -n "$(git -C "$JOB_FOLDER" status --porcelain 2>/dev/null)" ] && echo true || echo false)
HOST="$(hostname)/$(whoami)"
# Receipts and notebooks carry SPACE-relative paths: the user name and the
# checkout folder differ per machine, so an absolute path is wrong on the next one.
REPO_ROOT_PHYS="$(cd -P "$REPO_ROOT" && pwd)"
space_rel() {
  local root
  for root in "$REPO_ROOT" "$REPO_ROOT_PHYS"; do
    case "$1" in
      "$root") echo .; return ;;
      "$root"/*) echo "${1#"$root"/}"; return ;;
    esac
  done
  echo "$1"
}
CMD="bash $(space_rel "$TICKET")"
TICKET_ARGS_JSON="$(python3 -c 'import json, sys; print(json.dumps(sys.argv[1:]))' "$@")"
RESULT_PATH="${RESULTS_DIR#"$OUTPUT_ROOT"/}"

_yaml_sq() { printf '%s' "$1" | sed "s/'/''/g"; }

RESOLVED_RUN_INPUTS=()
INPUT_FILES=()
# bash 3.2, which is what macOS ships, treats "${arr[@]}" of an EMPTY array as
# unbound under `set -u` and aborts. The [@]+ form is empty-safe on 3.2 and on 5.
for input_spec in "${RUN_INPUTS[@]+"${RUN_INPUTS[@]}"}"; do
  # An older Ticket may still carry "path|<hash>"; only the path is read.
  input_path="${input_spec%%|*}"
  case "$input_path" in /*) input_abs="$input_path" ;; *) input_abs="$JOB_FOLDER/$input_path" ;; esac
  [ -f "$input_abs" ] && [ -r "$input_abs" ] || fail_shape "declared input is not a readable file: $input_path"
  RESOLVED_RUN_INPUTS+=("$input_path")
  INPUT_FILES+=("$input_abs")
done

emit_inputs_yaml() {
  printf "  - path: '%s'\n" "$(_yaml_sq "$CONFIG_REL")"
  for input_path in "${RESOLVED_RUN_INPUTS[@]+"${RESOLVED_RUN_INPUTS[@]}"}"; do
    printf "  - path: '%s'\n" "$(_yaml_sq "$input_path")"
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
attempt:    $ATTEMPT
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
settings:
  config_file: $CONFIG_REL
  ticket_args: $TICKET_ARGS_JSON
notebook: $NOTEBOOK_RECORD
duration: $duration
headline: $headline
EOF
  mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"
}

# One native writer at a time. An abandoned lock requires owner recovery;
# never remove a lock merely because a second invocation wants to retry.
RUN_LOCK="$RESULTS_DIR/.run-lock"
mkdir "$RUN_LOCK" 2>/dev/null || fail_shape "Run is already active or needs abandoned-lock recovery: $RUN_NAME"
trap 'rmdir "$RUN_LOCK" 2>/dev/null || true' EXIT
# Check the prior receipt and preserve it before launch. A contract file
# (Ticket, config, worker, declared input) newer than that receipt means the
# commission changed after it was written. No hash is computed or compared;
# a leftover hash field in an older receipt is ignored.
# No worker is run and no old receipt is changed when these checks fail.
ATTEMPT="$(python3 - "$RUNTIME_YAML" "$TICKET_ARGS_JSON" "$TICKET" "$CONFIG" "$WORKER" \
  "${INPUT_FILES[@]+"${INPUT_FILES[@]}"}" <<'PY_HISTORY'
from pathlib import Path
import json, re, shutil, sys
runtime, args = Path(sys.argv[1]), json.loads(sys.argv[2])
config = Path(sys.argv[4])
contract_files = [Path(p) for p in sys.argv[3:]]
def scalar(text, key, indent=""):
    match = re.search(r"^" + indent + re.escape(key) + r":[ \t]*(.*)$", text, re.M)
    return match.group(1).strip().strip("\"'") if match else ""
def stop(reason):
    raise SystemExit("Run history: " + reason)
def newer_than_receipt(paths):
    written = runtime.stat().st_mtime
    return [str(p) for p in paths if p.stat().st_mtime > written]
attempt = 1
if runtime.is_file():
    previous = runtime.read_text()
    status = scalar(previous, "status").lower()
    if status in {"complete", "completed", "done", "superseded"}:
        stop("closed Result is immutable; reuse it or commission a new Run")
    started = scalar(previous, "started_at")
    if status == "planned" and started in {"", "null", "~"}:
        if newer_than_receipt([config]):
            stop("planned config changed after planning; resolve the commission before dispatch")
    else:
        if status not in {"failed", "blocked", "running"}:
            stop("unknown prior state; owner recovery is required")
        changed = newer_than_receipt(contract_files)
        if changed:
            stop("contract files changed after the prior attempt (" + ", ".join(changed)
                 + "); preserve history and resolve through the owner")
        old_args = scalar(previous, "ticket_args", indent=r"[ \t]+")
        if old_args and old_args not in {"null", "~"}:
            try:
                same_args = json.loads(old_args) == args
            except ValueError:
                same_args = False
            if not same_args:
                stop("Ticket arguments changed after the prior attempt; resolve through the owner")
        old_attempt = scalar(previous, "attempt")
        if not old_attempt.isdigit() or int(old_attempt) < 1:
            stop("prior attempt number is missing or invalid")
        archive = runtime.parent / "attempts" / f"{int(old_attempt):06d}"
        if archive.exists():
            stop("attempt archive already exists; reconcile interrupted history before retry")
        archive.mkdir(parents=True)
        shutil.copy2(runtime, archive / "runtime.yaml")
        attempt = int(old_attempt) + 1
print(attempt)
PY_HISTORY
)"
HISTORY_EXIT=$?
[ "$HISTORY_EXIT" -eq 0 ] || fail_shape "retry history or changed-contract check failed"
write_receipt running null null null null null

if [ "$NOTEBOOK_MODE" = off ]; then
  NB_TARGET="$OUTPUT_ROOT/$TASK_SEG/notebooks/.$RUN_NAME.tmp.ipynb"
else
  NB_TARGET="$NOTEBOOK_OUT"
fi

EXIT_CODE=0
export HAIPIPE_CONFIG="$CONFIG"
if [ "$NOTEBOOK_MODE" = off ]; then
  # A Task that declared it wants no notebook should not need a notebook stack.
  # Requiring papermill + a working jupyter kernel to produce a file the Ticket
  # then deletes makes every such Task fail on any host without one, for nothing.
  # The worker reads $HAIPIPE_CONFIG, which is the same value papermill injects.
  python "$WORKER" || EXIT_CODE=$?
else
  # A reader-facing worker (`# notebook: hide-code`) hides its input: the converter marks its own
  # cells, and papermill's report mode also hides the parameters cell it injects.
  REPORT_MODE=()
  grep -qE '^#[[:space:]]*notebook:[[:space:]]*hide-code' "$WORKER" && REPORT_MODE=(--report-mode)
  {
    # && not ;: a failed conversion leaves no _source.ipynb, and papermill then
    # reports a missing file instead of the conversion error that actually broke.
    python "$REPO_ROOT/code/scripts/convert_to_notebooks.py" "$WORKER" -o "$NOTEBOOK_TEMPLATE" \
      && papermill "$NOTEBOOK_TEMPLATE" "$NB_TARGET" -p config "$CONFIG" ${REPORT_MODE[@]+"${REPORT_MODE[@]}"}
  } || EXIT_CODE=$?
fi

case "$NOTEBOOK_MODE" in
  thin) jupyter nbconvert --clear-output --inplace "$NB_TARGET" 2>/dev/null || echo "==> [warn] could not thin notebook" >&2 ;;
  off) : ;;   # nothing was written: the off branch above never ran papermill
esac

# The notebook is generated from the worker .py and is never edited here: an
# absolute path it shows (a print, the injected config) is fixed at its source.
if [ "$NOTEBOOK_MODE" != off ] && grep -Iq -e "$REPO_ROOT/" -e "$REPO_ROOT_PHYS/" "$NB_TARGET" 2>/dev/null; then
  echo "==> [warn] the notebook shows an absolute SPACE path; print it SPACE-relative in the worker .py" >&2
fi
if grep -rIlq --exclude='0-*.log' -e "$REPO_ROOT/" -e "$REPO_ROOT_PHYS/" "$RESULTS_DIR" 2>/dev/null; then
  echo "==> [warn] a Result file holds an absolute SPACE path; write it SPACE-relative" >&2
fi
# A Result is light (haipipe-run): flag a file over 10 MB or a link in the Result, and a link in the
# Task folder; heavy output belongs in _WorkSpace, read through its variable, with a pointer in the Result.
HEAVY="$(find "$RESULTS_DIR" \( -type f -size +10M -o -type l \) 2>/dev/null | head -3 | sed "s|$REPO_ROOT/||" | tr '\n' ' ')"
if [ -n "$HEAVY" ]; then
  echo "==> [warn] the Result holds a file over 10 MB or a link; write it to _WorkSpace and keep a pointer: $HEAVY" >&2
fi
LINKS="$(find "$TASK_FOLDER" -type l -not -path '*/results/*' 2>/dev/null | head -3 | sed "s|$REPO_ROOT/||" | tr '\n' ' ')"
if [ -n "$LINKS" ]; then
  echo "==> [warn] the Task folder holds a link; read _WorkSpace through its variable instead: $LINKS" >&2
fi

ENDED="$(date -Iseconds)"
DURATION="$(python3 -c "
from datetime import datetime
s = datetime.fromisoformat('$STARTED'); e = datetime.fromisoformat('$ENDED')
d = e - s; m, sec = divmod(int(d.total_seconds()), 60); h, m = divmod(m, 60)
print(f'{h}h{m:02d}m' if h else f'{m}m{sec:02d}s')
")"
STATUS=complete
FAILURE=null
if [ "$EXIT_CODE" -ne 0 ]; then
  STATUS=failed
  FAILURE=process-exit-$EXIT_CODE
else
  for required in "${REQUIRED_RESULTS[@]+"${REQUIRED_RESULTS[@]}"}"; do
    if [ ! -e "$RESULTS_DIR/$required" ]; then
      STATUS=failed
      FAILURE=missing-required-result
      EXIT_CODE=3
      echo "==> [result-gate] missing $RESULTS_DIR/$required" >&2
      break
    fi
  done
  if [ "$STATUS" = complete ] && ! result_gate; then
    STATUS=failed
    FAILURE=result-gate-failed
    EXIT_CODE=4
  fi
fi

HEADLINE="$(python3 -c "
import json
try:
    print(json.load(open('$RESULTS_DIR/metrics.json')).get('summary', {}).get('headline') or '-')
except Exception:
    print('-')
")"

write_receipt "$STATUS" "$ENDED" "$EXIT_CODE" "$FAILURE" "$DURATION" "$HEADLINE"
echo "==> Runtime written to $RUNTIME_YAML"
echo "==> Next: /haipipe-task report $TASK_FOLDER"
exit "$EXIT_CODE"
