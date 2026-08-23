#!/usr/bin/env bash
# Start the describe-exercise service.
#
#   Tools/plugins/haipipe-utils/skills/describe-exercise/run_server.sh
#   EXNORM_PORT=9000 .../run_server.sh
#
# PYTHONPATH is set to THIS directory so `exnorm` imports as a top-level name
# whether or not the caller sourced the workspace env.sh -- a service must start
# from a bare shell.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${EXNORM_HOST:-127.0.0.1}"
PORT="${EXNORM_PORT:-8078}"

PY=python3
for cand in "${HERE}/../../../../../.venv/bin/python" "${VIRTUAL_ENV:-}/bin/python"; do
  [ -x "$cand" ] && PY="$cand" && break
done

echo "describe-exercise -> http://${HOST}:${PORT}  (python: ${PY})"
PYTHONPATH="${HERE}:${PYTHONPATH:-}" exec "$PY" -m uvicorn server:app \
  --app-dir "${HERE}" --host "${HOST}" --port "${PORT}"
