#!/usr/bin/env bash
# Start the haipipe-utils API host from a bare shell.
#
#   Tools/plugins/haipipe-utils/servers/_host/run.sh                       # 127.0.0.1:8070, every lane
#   Tools/plugins/haipipe-utils/servers/_host/run.sh --only insulin        # one lane
#   Tools/plugins/haipipe-utils/servers/_host/run.sh --store /path/to/_WorkSpace/ExternalStore
#   HAIPIPE_UTILS_PORT=9000 .../run.sh
#
# The only job here is choosing an interpreter that has fastapi: $HAIPIPE_UTILS_PYTHON,
# then the SPACE venv (Tools sits at <SPACE>/Tools), then uv with the deps pinned
# inline, then whatever python3 is active. Everything else is serve.py's.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS=(fastapi 'uvicorn[standard]' pandas pyarrow requests python-multipart)

if [[ -n "${HAIPIPE_UTILS_PYTHON:-}" ]]; then
  exec "${HAIPIPE_UTILS_PYTHON}" "${HERE}/serve.py" "$@"
fi
for cand in "${HERE}/../../../../../.venv/bin/python" "${VIRTUAL_ENV:-/nonexistent}/bin/python"; do
  if [[ -x "$cand" ]] && "$cand" -c 'import fastapi, uvicorn' 2>/dev/null; then
    exec "$cand" "${HERE}/serve.py" "$@"
  fi
done
if command -v uv >/dev/null 2>&1; then
  WITH=(); for d in "${DEPS[@]}"; do WITH+=(--with "$d"); done
  exec uv run --quiet --python 3.13 "${WITH[@]}" python "${HERE}/serve.py" "$@"
fi
exec python3 "${HERE}/serve.py" "$@"
