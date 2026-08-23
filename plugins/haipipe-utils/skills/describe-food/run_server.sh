#!/usr/bin/env bash
# Start describe-food as a service.
#
#     ./run_server.sh                  # 127.0.0.1:8077, this box only
#     HOST=0.0.0.0 PORT=9000 ./run_server.sh
#
# THIS is the only process that needs the resolver on its PYTHONPATH. A consumer
# needs an address. That is the whole point of serving it: the service can move
# to another host, a container or a managed endpoint, and every consumer keeps
# working because all it ever knew was FOODNORM_URL.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8077}"

# The resolver package sits beside this script.
export PYTHONPATH="${HERE}:${PYTHONPATH:-}"

# Find an interpreter that has fastapi. A workspace venv is the normal case;
# fall back to whatever python is active.
if [[ -n "${FOODNORM_PYTHON:-}" ]]; then
  PY="${FOODNORM_PYTHON}"
elif [[ -x "${HERE}/../../../../../.venv/bin/python" ]]; then
  PY="$(cd "${HERE}/../../../../.." && pwd)/.venv/bin/python"
else
  PY="$(command -v python3)"
fi

echo "describe-food · ${PY}"
echo "  bank      ${FOODNORM_DB:-<library default>}"
echo "  listening http://${HOST}:${PORT}   (health: /healthz)"
exec "${PY}" -m uvicorn server:app --app-dir "${HERE}" --host "${HOST}" --port "${PORT}"
