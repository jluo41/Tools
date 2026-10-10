#!/usr/bin/env bash
# SYNTHETIC fixtures: run the In-Lab Console on generated data only (no real person, record or study).
#
#   bash fixtures/run_fixture.sh [--record] [--build] [console_port] [stub_port]   defaults 8191 8192, loopback
#
#   --record   serve SynthCGM_v0 from the synthetic record store, read in place (j02 Q02), not the json copy
#   --build    rebuild the front end even when web/dist exists
#
# Builds the fixtures and (if missing) the front end, starts the stub endpoint and the console, and prints both
# PIDs. Stop them with `kill <pid> <pid>`; never stop a process by a name pattern (pkill -f, killall).
set -euo pipefail
RECORD=0
BUILD=0
while [ "${1:-}" = "--record" ] || [ "${1:-}" = "--build" ]; do
  [ "$1" = "--record" ] && RECORD=1
  [ "$1" = "--build" ] && BUILD=1
  shift
done
HERE="$(cd "$(dirname "$0")" && pwd)"
APP="$(dirname "$HERE")"
CPORT="${1:-8191}"
SPORT="${2:-8192}"
PY="${PYTHON:-python3}"
LOG="${INLAB_FIXTURE_LOG:-$HERE/.logs}"
mkdir -p "$LOG"

"$PY" "$HERE/build_fixtures.py" --port "$SPORT"
if [ "$BUILD" = 1 ] || [ ! -f "$APP/web/dist/index.html" ]; then
  (cd "$APP/web" && { [ -d node_modules ] || npm install --no-audit --no-fund; } && npm run build) > "$LOG/build.log" 2>&1
fi

"$PY" "$HERE/stub_endpoint.py" --port "$SPORT" > "$LOG/stub.log" 2>&1 &
STUB=$!

export INLAB_DATASET_STORE="$HERE/store"
export INLAB_CASE_STORE="$HERE/casestore"
export INLAB_PROJECTS_ROOT="$HERE/projects"
if [ "$RECORD" = 1 ]; then
  export INLAB_RECORD_STORE="$HERE/recstore"
fi
export INLAB_ENDPOINT_STORE="$HERE/endpoints"
export INLAB_REGISTRY="$HERE/registry.json"
export INLAB_RUN_STORE="$HERE/.runs"
# the console's own dependencies (pyproject.toml): uvicorn[standard] carries the websockets library /ws/haichat
# needs; through uv when it is installed, else whatever $PY already has
if command -v uv > /dev/null; then
  RUN=(uv run --quiet --no-project --with fastapi --with "uvicorn[standard]" --with claude-agent-sdk --with pyarrow python)
else
  RUN=("$PY")
fi
(cd "$APP" && exec "${RUN[@]}" -m uvicorn main:app --host 127.0.0.1 --port "$CPORT") > "$LOG/console.log" 2>&1 &
CONSOLE=$!

for _ in $(seq 1 40); do
  curl -s -o /dev/null "http://127.0.0.1:$CPORT/api/health" && break
  sleep 0.5
done
echo "stub     pid $STUB     http://127.0.0.1:$SPORT"
echo "console  pid $CONSOLE  http://127.0.0.1:$CPORT"
echo "stop:    kill $STUB $CONSOLE"
