#!/usr/bin/env bash
# Start the describe-medication service.
#
#   Tools/plugins/haipipe-utils/skills/describe-medication/run_server.sh
#   MEDNORM_PORT=9000 .../run_server.sh
#
# PYTHONPATH is set to THIS directory so the package imports as a top-level name
# whether or not the caller sourced the workspace env.sh -- a service must start
# from a bare shell.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${MEDNORM_HOST:-127.0.0.1}"
PORT="${MEDNORM_PORT:-8079}"

PY=python3
for cand in "${HERE}/../../../../../.venv/bin/python" "${VIRTUAL_ENV:-}/bin/python"; do
  [ -x "$cand" ] && PY="$cand" && break
done

echo "describe-medication -> http://${HOST}:${PORT}  (python: ${PY})"
PYTHONPATH="${HERE}:${PYTHONPATH:-}" exec "$PY" -m uvicorn server:app \
  --app-dir "${HERE}" --host "${HOST}" --port "${PORT}"
