#!/bin/bash
# =============================================================================
# Template for a TICKET: <task>/runs/<run>.sh (nested job) or runs/<run>.sh
# (flat legacy job). Shape is auto-detected from this script's own path.
# =============================================================================
# Each run.sh is a thin wrapper that:
#   1. Snapshots launch state -> results/<NAME>/runtime.yaml (status: running)
#   2. Convert .py -> template .ipynb
#   3. papermill execute -> notebooks/<NAME>.ipynb
#   4. Apply the declared Result gate and finalize runtime.yaml
#      (status: complete | failed)
#
# Notebook policy (resolved Run config -> _meta.notebook: full | thin | off):
#   full (default) keep the executed notebook with all outputs
#   thin           execute, then clear cell outputs (small record; keeps code+params,
#                  drops bulky stream/image output) — good for heavy compute (training/data)
#   off            execute via papermill (so config injection + the .py run identically),
#                  but DON'T keep the .ipynb artifact at all
# All three execute the .py the same way; they differ only in what notebook is retained.
#
# Variables you MUST set:
#   TASK_NAME       — the .py basename (without .py) under scripts/ in a
#                     canonical nested Task, or at Job root in a flat legacy Job
#   RUN_FAMILY      — the haipipe-run family, normally Execution
#   RUN_OPERATION   — the independently closable operation
#   RUN_TARGET      — the bounded target
#   REQUIRED_RESULTS — relative paths under RESULT_DIR that constitute the
#                      worker/dialect's minimum Result gate
#
# Everything else is derived from $0 (the script path).
# =============================================================================

set -uo pipefail

# ─── Manual config: edit for the task ──────────────────────────────────────
TASK_NAME="01_pretrain_baseline"
RUN_FAMILY="Execution"
RUN_OPERATION="task-execution"
RUN_TARGET="01_pretrain_baseline"
REQUIRED_RESULTS=("metrics.json")
# Additional frozen inputs as "path|sha256". Paths may be absolute or
# Job-relative. Use "path|auto" only when this Ticket is allowed to hash the
# resolved file at launch; Page Evidence Item Tickets pin the LAND-frozen hash.
RUN_INPUTS=()

# Extend this function in a specialized Ticket when existence is not the full
# semantic Result gate. It runs only after every REQUIRED_RESULTS path exists.
result_gate() { return 0; }

# ─── 1. Resolve identity from $0 (a ticket never repeats its own name) ─────
# Canonicalize FIRST: a symlinked ticket must resolve shape + job from its
# REAL location, or a nested ticket linked into a flat runs/ silently writes
# into the wrong job's tree.
TICKET="$(realpath "$0" 2>/dev/null || echo "$0")"
RUN_NAME="$(basename "$TICKET" .sh)"                       # e.g. wide, run_1m
_TICKET_PARENT="$(cd "$(dirname "$TICKET")" && pwd)"
_TICKET_GRAND="$(basename "$(dirname "$_TICKET_PARENT")")"
# THREE shapes now live side by side, and two of them put the ticket in a dir
# named `runs`, so the parent's name ALONE no longer decides (JL 260830). The
# grandparent breaks the tie: a task folder is `tNN_*`, a job folder is not.
case "$(basename "$_TICKET_PARENT")" in
  runs)
    case "$_TICKET_GRAND" in
      t[0-9][0-9]_*)
        TASK_SEG="$_TICKET_GRAND"                          # NESTED: <task>/runs/<run>.sh
        TASK_DIR="$(cd "$_TICKET_PARENT/../.." && pwd)" ;;
      *)
        TASK_SEG=""                                        # FLAT legacy: runs/<run>.sh
        TASK_DIR="$(cd "$_TICKET_PARENT/.." && pwd)" ;;
    esac ;;
  *)
    TASK_SEG="$(basename "$_TICKET_PARENT")"               # NESTED pre-260830: <task>/runs/<run>.sh
    TASK_DIR="$(cd "$_TICKET_PARENT/../.." && pwd)" ;;
esac
# TASK_DIR is the JOB folder (name kept: the .py's TASK_DIR contract predates
# the 260829 rename). TASK_SEG is the task segment, empty in flat jobs.
REPO_ROOT="$(git -C "$TASK_DIR" rev-parse --show-toplevel)"
STARTED="$(date -Iseconds)"                                # 2026-05-24T14:30:01-04:00

if [ -n "$TASK_SEG" ] && [ -d "$TASK_DIR/$TASK_SEG/scripts/config" ]; then
  CONFIG="${TASK_SEG}/scripts/config/${RUN_NAME}.yaml"     # canonical nested
elif [ -n "$TASK_SEG" ] && [ -d "$TASK_DIR/$TASK_SEG/config" ]; then
  CONFIG="${TASK_SEG}/config/${RUN_NAME}.yaml"             # pre-260831 nested
elif [ -n "$TASK_SEG" ]; then
  CONFIG="scripts/${TASK_SEG}/config/${RUN_NAME}.yaml"     # older mirrored nested
else
  CONFIG="configs/${RUN_NAME}.yaml"                        # flat legacy
fi
# PY_PREFIX mirrors the CONFIG branch: where the Task's .py lives relative to
# the Job.
if [ -n "$TASK_SEG" ] && [ -d "$TASK_DIR/$TASK_SEG/scripts/config" ]; then
  PY_PREFIX="${TASK_SEG}/scripts/"
elif [ -n "$TASK_SEG" ] && [ -d "$TASK_DIR/$TASK_SEG/config" ]; then
  PY_PREFIX="${TASK_SEG}/"
elif [ -n "$TASK_SEG" ]; then
  PY_PREFIX="scripts/${TASK_SEG}/"
else
  PY_PREFIX=""
fi

# ─── 1a. Resolve the OUTPUT ROOT: am I serving a consumer, or myself? ───────
# A job is SHARED CODE; a run of it is one CALL (JL 260821). When the
# call serves a consumer that owns its own store — an InsightBoard, say — the
# generated bytes belong to that store, mirrored under the task's path, so the
# same code answers the same question on a second cohort without being copied.
# With no store declared, output stays task-local and nothing changes.
#
#   RESULT_STORE env       one caller overriding one run          (wins)
#   config `store:` key    a standing declaration for this call
#   neither                task-local $TASK_DIR                   (the default)
#
# The task layer is told a PATH, never a consumer identity: a dispatching caller
# supplies the store, and the executor still cannot learn whose claim it serves.
# `store:` is a JOB property (JL 260829): declared once in the job's defaults
# (src/config-defaults.yaml nested, configs/_defaults.yaml flat);
# a run config carrying its own is legacy and still honored, run-first.
STORE="${RESULT_STORE:-$(sed -n 's/^store:[[:space:]]*//p' "$TASK_DIR/$CONFIG" \
  "$TASK_DIR/src/config-defaults.yaml" \
  "$TASK_DIR/configs/_defaults.yaml" \
  2>/dev/null | head -1)}"
if [ -n "$STORE" ]; then
  case "$STORE" in /*) : ;; *) STORE="$REPO_ROOT/$STORE" ;; esac   # repo-relative allowed
  case "$TASK_DIR" in
    */tasks/*) TASK_REL="${TASK_DIR#*/tasks/}" ;;   # mirror the task tree in the store
    *) echo "==> BLOCKED: a store is declared but $TASK_DIR is not under a tasks/" >&2
       echo "    directory, so there is no path to mirror. Move the job" >&2
       echo "    under tasks/, or drop the store: key to run self-serving." >&2
       exit 2 ;;
  esac
  OUTPUT_ROOT="$STORE/$TASK_REL"
else
  OUTPUT_ROOT="$TASK_DIR"
  # SPLIT-BANK GUARD (JL 260823). Writing task-local is normal — unless some
  # store already holds answers for THIS job, which means the job is
  # serving a consumer and this run was launched without being told. Two banks
  # for one folder is the failure the store mechanism exists to prevent: the
  # qa gate scans one of them, so the other's answers are invisible and the
  # same work gets commissioned twice.
  if [ -n "${RESULT_STORE_SEARCH_ROOT:-$REPO_ROOT/_WorkSpace}" ] && [ -d "${RESULT_STORE_SEARCH_ROOT:-$REPO_ROOT/_WorkSpace}" ]; then
    _rel="${TASK_DIR#*/tasks/}"
    _hits=$(find "${RESULT_STORE_SEARCH_ROOT:-$REPO_ROOT/_WorkSpace}" -type d -path "*/${_rel}/QA" 2>/dev/null | head -3)
    if [ -n "$_hits" ]; then
      echo "==> [warn] SPLIT BANK: this run writes task-local, but a store already" >&2
      echo "    holds a QA bank for ${_rel}:" >&2
      echo "$_hits" | sed 's/^/      /' >&2
      echo "    Declare store: in src/config-defaults.yaml, or export RESULT_STORE," >&2
      echo "    unless serving no consumer is genuinely what you want here." >&2
    fi
    unset _rel _hits
  fi
fi
export OUTPUT_ROOT

# <task>/<run> is the spine: identical under the job (mode ①) or a store (mode ②).
RUN_REL="${TASK_SEG:+$TASK_SEG/}${RUN_NAME}"               # nested: <task>/<run> · flat: <run>
RESULTS_DIR="$OUTPUT_ROOT/results/${RUN_REL}"
RUNTIME_YAML="$RESULTS_DIR/runtime.yaml"
NOTEBOOK_TEMPLATE="$OUTPUT_ROOT/notebooks/${TASK_SEG:+$TASK_SEG/}_source.ipynb"
NOTEBOOK_OUT="$OUTPUT_ROOT/notebooks/${RUN_REL}.ipynb"

# The .py reads this and must never build an output path of its own.
export RESULT_DIR="$RESULTS_DIR"

# Notebook policy: full (keep) | thin (keep, outputs cleared) | off (execute, don't keep).
NOTEBOOK_MODE="$(grep -E '^\s*notebook:\s*(full|thin|off)\b' "$TASK_DIR/$CONFIG" 2>/dev/null | awk '{print $2}' | head -1)"
NOTEBOOK_MODE="${NOTEBOOK_MODE:-full}"
NOTEBOOK_RECORD=$([ "$NOTEBOOK_MODE" = "off" ] && echo "(off)" || echo "$NOTEBOOK_OUT")

mkdir -p "$RESULTS_DIR" "$OUTPUT_ROOT/notebooks/${TASK_SEG}"

# ─── 1b. Address, read off the path (block-job-task-run.md § Addressing) ───
# the four level prefixes read off the path and joined: b02j01t01r03 (readable
# b02.j01.t01.r03). Nothing computed; a run config without rNN_ falls back to its
# stem (b02j01t01.wide); legacy names without level letters get readable only.
case "$TASK_DIR" in */tasks/*) _JOB_REL="${TASK_DIR#*/tasks/}" ;; *) _JOB_REL="" ;; esac
_BLOCK="${_JOB_REL%%/*}"; _JOB="${_JOB_REL#*/}"
_num() { case "$1" in [0-9]*) printf '%d' "$((10#${1%%[!0-9]*}))" ;; *) printf '' ;; esac; }
_pfx() { case "$1" in [bjtr][0-9][0-9]_*) printf '%s' "${1%%_*}" ;; *) printf '' ;; esac; }   # the level-letter prefix, or empty
_B_PREFIX="$(_pfx "$_BLOCK")"; _JP="$(_pfx "$_JOB")"; _TP="$(_pfx "$TASK_SEG")"; _RP="$(_pfx "$RUN_NAME")"
_J="$(_num "$_JOB")"; _T="$(_num "$TASK_SEG")"; _R="$(_num "$RUN_NAME")"
_PROJECT="$(basename "$(cd "$TASK_DIR" && while [ "$PWD" != / ] && [ ! -d tasks ]; do cd ..; done; pwd)")"
if [ -n "$_B_PREFIX" ] && [ -n "$_JP" ] && { [ -z "$TASK_SEG" ] || [ -n "$_TP" ]; }; then
  ADDRESS="${_B_PREFIX}${_JP}${_TP}"                       # b02j01t01 — read, never computed
  if [ -n "$_RP" ]; then ADDRESS="${ADDRESS}${_RP}"; else ADDRESS="${ADDRESS}.${RUN_NAME}"; fi
  ADDRESS_READABLE="${_B_PREFIX}.${_JP}${_TP:+.$_TP}.${_RP:-$RUN_NAME}"
else
  ADDRESS=""                                               # legacy names without level letters
  ADDRESS_READABLE="${_BLOCK%%_*}.${_JOB%%_*}${TASK_SEG:+.${TASK_SEG%%_*}}.${RUN_NAME}"
fi

# ─── 2. Capture launch state ───────────────────────────────────────────────
GIT_SHA="$(git -C "$TASK_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
GIT_DIRTY=$([ -n "$(git -C "$TASK_DIR" status --porcelain 2>/dev/null)" ] && echo true || echo false)
CONFIG_SHA256="$(shasum -a 256 "$TASK_DIR/$CONFIG" 2>/dev/null | awk '{print $1}')"
CONFIG_SHA256="${CONFIG_SHA256:-unknown}"
HOST="$(hostname)/$(whoami)"
CMD="bash $TICKET"
TICKET_ARGS_JSON="$(python3 -c 'import json, sys; print(json.dumps(sys.argv[1:]))' "$@")"
TICKET_PATH="${TICKET#${TASK_DIR}/}"
RESULT_PATH="${RESULTS_DIR#${OUTPUT_ROOT}/}"
WORKER_PATH="${PY_PREFIX}${TASK_NAME}.py"

_yaml_sq() { printf '%s' "$1" | sed "s/'/''/g"; }
# Resolve every launch-time `|auto` binding exactly once. The running and
# terminal receipts must describe the same frozen input graph even when an
# upstream file changes while the worker is executing.
RESOLVED_RUN_INPUTS=()
for _input_spec in "${RUN_INPUTS[@]}"; do
  _input_path="${_input_spec%%|*}"
  if [ "$_input_path" = "$_input_spec" ]; then
    _input_sha=auto
  else
    _input_sha="${_input_spec#*|}"
  fi
  if [ "$_input_sha" = auto ]; then
    case "$_input_path" in /*) _input_abs="$_input_path" ;; *) _input_abs="$TASK_DIR/$_input_path" ;; esac
    _input_sha="$(shasum -a 256 "$_input_abs" 2>/dev/null | awk '{print $1}')"
    _input_sha="${_input_sha:-unresolved}"
  fi
  RESOLVED_RUN_INPUTS+=("${_input_path}|${_input_sha}")
done

emit_inputs_yaml() {
  printf "  - path: '%s'\n" "$(_yaml_sq "$CONFIG")"
  printf "    sha256: '%s'\n" "$CONFIG_SHA256"
  for _input_spec in "${RESOLVED_RUN_INPUTS[@]}"; do
    _input_path="${_input_spec%%|*}"
    _input_sha="${_input_spec#*|}"
    printf "  - path: '%s'\n" "$(_yaml_sq "$_input_path")"
    printf "    sha256: '%s'\n" "$(_yaml_sq "$_input_sha")"
  done
}

# ─── 2a. Pre-flight code review gate ───────────────────────────────────────
# Block launch unless a fresh CODE_REVIEW.md (produced by the haipipe-task-reviewer-agent (Gate 1)
# agent) exists for this job and matches the current git_sha.
# Skip mechanisms (any one):
#   • _meta.skip_review: true   in the resolved Run config
#   • HAIPIPE_SKIP_REVIEW=1     env var at launch
# Verdict semantics:
#   pass | skipped → proceed
#   warn           → proceed with stderr warning
#   fail | <none>  → exit 2; user must run the agent or fix code
CODE_REVIEW="$TASK_DIR/CODE_REVIEW.md"   # reviews CODE at a git_sha, so it stays with
                                        # the code in BOTH modes. Only RUN_AUDIT.md,
                                        # which audits one run's results, follows output.
SKIP_REVIEW_CONFIG="$(grep -E '^\s*skip_review:\s*true\b' "$TASK_DIR/$CONFIG" 2>/dev/null || true)"
if [ -n "$SKIP_REVIEW_CONFIG" ] || [ "${HAIPIPE_SKIP_REVIEW:-0}" = "1" ]; then
  echo "==> [pre-flight] code review SKIPPED (explicit skip flag)" >&2
else
  if [ ! -f "$CODE_REVIEW" ]; then
    echo "==> [pre-flight] BLOCKED: no CODE_REVIEW.md in $TASK_DIR" >&2
    echo "    Run the Task Reviewer agent (GATE 1) on this job first," >&2
    echo "    or set HAIPIPE_SKIP_REVIEW=1 to bypass." >&2
    echo "    Agent: Tools/plugins/haipipe-toolkit/skills/task/agents/haipipe-task-reviewer-agent.md" >&2
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
run:        $RUN_NAME
family:     $RUN_FAMILY
operation:  $RUN_OPERATION
target:     $RUN_TARGET
status:     running
ticket:     $TICKET_PATH
result:     $RESULT_PATH
inputs:
EOF
emit_inputs_yaml >> "$RUNTIME_YAML.tmp"
cat >> "$RUNTIME_YAML.tmp" <<EOF
worker:
  kind: script
  name: $WORKER_PATH
started_at: $STARTED
finished_at: null
supersedes: null
failure: null
git_sha:    $GIT_SHA
git_dirty:  $GIT_DIRTY
host:       $HOST
cmd:        $CMD
address:    ${ADDRESS:-<none>}
address_readable: $ADDRESS_READABLE
project:    $_PROJECT
config_file: $CONFIG
config_sha256: $CONFIG_SHA256
settings:
  config_file: $CONFIG
  ticket_args: $TICKET_ARGS_JSON
notebook:   $NOTEBOOK_RECORD
EOF
mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"

# ─── 4. Execute (convert + papermill, per notebook policy) ─────────────────
# off → execute to a temp notebook we delete after; full/thin → keep the real one.
if [ "$NOTEBOOK_MODE" = "off" ]; then
  NB_TARGET="$OUTPUT_ROOT/notebooks/${TASK_SEG:+$TASK_SEG/}.${RUN_NAME}.tmp.ipynb"
else
  NB_TARGET="$NOTEBOOK_OUT"
fi

EXIT_CODE=0
{
  python "$REPO_ROOT/code/scripts/convert_to_notebooks.py" \
         "$TASK_DIR/${PY_PREFIX}${TASK_NAME}.py" \
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
STATUS=complete
FAILURE=null
if [ "$EXIT_CODE" -ne 0 ]; then
  STATUS=failed
  FAILURE=process-exit-$EXIT_CODE
else
  for _required in "${REQUIRED_RESULTS[@]}"; do
    if [ ! -e "$RESULTS_DIR/$_required" ]; then
      STATUS=failed
      FAILURE=missing-required-result
      EXIT_CODE=3
      echo "==> [result-gate] missing $RESULTS_DIR/$_required" >&2
      break
    fi
  done
  if [ "$STATUS" = complete ] && ! result_gate; then
    STATUS=failed
    FAILURE=result-gate-failed
    EXIT_CODE=4
    echo "==> [result-gate] worker-specific validation failed" >&2
  fi
fi
HEADLINE="$(python3 -c "
import json
try:
    d = json.load(open('$RESULTS_DIR/metrics.json'))
    print(d.get('summary', {}).get('headline') or '-')
except Exception:
    print('-')
")"

cat > "$RUNTIME_YAML.tmp" <<EOF
run:        $RUN_NAME
family:     $RUN_FAMILY
operation:  $RUN_OPERATION
target:     $RUN_TARGET
status:     $STATUS
ticket:     $TICKET_PATH
result:     $RESULT_PATH
inputs:
EOF
emit_inputs_yaml >> "$RUNTIME_YAML.tmp"
cat >> "$RUNTIME_YAML.tmp" <<EOF
worker:
  kind: script
  name: $WORKER_PATH
started_at: $STARTED
finished_at: $ENDED
supersedes: null
failure: $FAILURE
git_sha:    $GIT_SHA
git_dirty:  $GIT_DIRTY
host:       $HOST
exit_code:  $EXIT_CODE
cmd:        $CMD
address:    ${ADDRESS:-<none>}
address_readable: $ADDRESS_READABLE
project:    $_PROJECT
config_file: $CONFIG
config_sha256: $CONFIG_SHA256
settings:
  config_file: $CONFIG
  ticket_args: $TICKET_ARGS_JSON
notebook:   $NOTEBOOK_RECORD
duration:   $DURATION
headline:   $HEADLINE
EOF
mv "$RUNTIME_YAML.tmp" "$RUNTIME_YAML"

# ─── 6. Hand off observability to Report stage ─────────────────────────────
echo "==> Runtime written to $RUNTIME_YAML"
echo "==> Next: /haipipe-task report $TASK_DIR"

exit $EXIT_CODE
