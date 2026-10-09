#!/usr/bin/env bash
# SYNTHETIC fixtures: run the In-Lab Console on generated data only (no real person, record or study).
#
#   bash fixtures/run_fixture.sh [console_port] [stub_port]     defaults 8191 and 8192, loopback only
#
# Builds the fixtures and (if missing) the front end, starts the stub endpoint and the console, and prints both
# PIDs. Stop them with `kill <pid> <pid>`; never stop a process by a name pattern (pkill -f, killall).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
APP="$(dirname "$HERE")"
CPORT="${1:-8191}"
SPORT="${2:-8192}"
PY="${PYTHON:-python3}"
LOG="${INLAB_FIXTURE_LOG:-$HERE/.logs}"
mkdir -p "$LOG"

"$PY" "$HERE/build_fixtures.py" --port "$SPORT"
if [ ! -f "$APP/web/dist/index.html" ]; then
  (cd "$APP/web" && { [ -d node_modules ] || npm install --no-audit --no-fund; } && npm run build) > "$LOG/build.log" 2>&1
fi

"$PY" "$HERE/stub_endpoint.py" --port "$SPORT" > "$LOG/stub.log" 2>&1 &
STUB=$!

export INLAB_DATASET_STORE="$HERE/store"
export INLAB_PATIENT_STORE="$HERE/store/SynthCGM_v0/patients"
export INLAB_ENDPOINT_STORE="$HERE/endpoints"
export INLAB_REGISTRY="$HERE/registry.json"
export INLAB_RUN_STORE="$HERE/.runs"
# the console's own dependencies (pyproject.toml): uvicorn[standard] carries the websockets library /ws/haichat
# needs; through uv when it is installed, else whatever $PY already has
if command -v uv > /dev/null; then
  RUN=(uv run --quiet --no-project --with fastapi --with "uvicorn[standard]" --with claude-agent-sdk python)
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
