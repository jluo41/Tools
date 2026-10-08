#!/usr/bin/env bash
# Run the engine's teeth. Always from THIS directory: the repository's code/ package
# shadows the stdlib `code` module and breaks pytest startup when cwd is the repo root.
cd "$(dirname "$0")" || exit 1
PY="${PYTHON:-$(cd ../../../../../../.. 2>/dev/null && pwd)/.venv/bin/python}"
[ -x "$PY" ] || PY=python3
exec "$PY" -m pytest -q -p no:cacheprovider --rootdir=. "$@" .
