#!/usr/bin/env bash
# run-delivery-webpage · build delivery/web/ from this Page. Every rebuild reruns this same Run;
# the files in delivery/web/ are its result and their file time says when it last ran.
# Written by `page.py export`; never edited by hand (AGENTS.md rule 6).
set -euo pipefail
page="$(cd "$(dirname "$0")/../.." && pwd)"
root="$page"
until [ -f "$root/pyproject.toml" ] && [ -d "$root/code" ]; do
  root="$(dirname "$root")"
  [ "$root" = / ] && { echo "run-delivery-webpage: no repository root above $page" >&2; exit 1; }
done
exec "$root/.venv/bin/python" "$root/Tools/plugins/haipipe-toolkit/skills/1_base/draft/haipipe-draft/cli/page.py" \
  export "$page" --lane web
