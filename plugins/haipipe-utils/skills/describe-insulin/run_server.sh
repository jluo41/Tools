#!/usr/bin/env bash
# Start the describe-insulin service.
#
#   Tools/plugins/haipipe-utils/skills/describe-insulin/run_server.sh
#   INSNORM_PORT=9000 .../run_server.sh
#
# PYTHONPATH is set to THIS directory so the package imports as a top-level name
# whether or not the caller sourced the workspace env.sh -- a service must start
# from a bare shell.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${INSNORM_HOST:-127.0.0.1}"
PORT="${INSNORM_PORT:-8080}"

PY=python3
for cand in "${HERE}/../../../../../.venv/bin/python" "${VIRTUAL_ENV:-}/bin/python"; do
  [ -x "$cand" ] && PY="$cand" && break
done

echo "describe-insulin -> http://${HOST}:${PORT}  (python: ${PY})"
PYTHONPATH="${HERE}:${PYTHONPATH:-}" exec "$PY" -m uvicorn server:app \
  --app-dir "${HERE}" --host "${HOST}" --port "${PORT}"
