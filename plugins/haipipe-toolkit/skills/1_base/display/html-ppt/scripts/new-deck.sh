#!/usr/bin/env bash
# html-ppt :: new-deck.sh — scaffold a deck from a base or full-deck template
#
# Usage:
#   new-deck.sh <name> [output-parent-dir] [full-deck-template]
#
# Creates <parent>/<name>/index.html under the caller's current directory
# (unless parent is absolute), with paths rewritten to the skill's shared
# assets. Defaults to templates/deck.html and the current directory.

set -euo pipefail

NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  echo "usage: new-deck.sh <name> [parent-dir] [full-deck-template]" >&2
  exit 1
fi
if [[ "$NAME" == "." || "$NAME" == ".." || "$NAME" == */* ]]; then
  echo "error: name must be one directory name, without slashes" >&2
  exit 1
fi

PARENT="${2:-.}"
FULL_DECK="${3:-}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "$FULL_DECK" ]]; then
  TEMPLATE="$HERE/templates/deck.html"
  if [[ ! -f "$TEMPLATE" ]]; then
    echo "error: template not found at $TEMPLATE" >&2
    exit 1
  fi
else
  if [[ ! "$FULL_DECK" =~ ^[a-z0-9-]+$ ]]; then
    echo "error: full-deck template must be a simple template name" >&2
    exit 1
  fi
  TEMPLATE_DIR="$HERE/templates/full-decks/$FULL_DECK"
  if [[ ! -f "$TEMPLATE_DIR/index.html" ]]; then
    echo "error: full-deck template not found at $TEMPLATE_DIR" >&2
    exit 1
  fi
fi

if [[ "$PARENT" == /* ]]; then
  OUT_PARENT="$PARENT"
else
  OUT_PARENT="$(pwd -P)/$PARENT"
fi
OUT_DIR="$OUT_PARENT/$NAME"
if [[ -e "$OUT_DIR" ]]; then
  echo "error: $OUT_DIR already exists" >&2
  exit 1
fi
mkdir -p "$OUT_DIR"

if [[ -n "$FULL_DECK" ]]; then
  cp -R "$TEMPLATE_DIR/." "$OUT_DIR/"
else
  cp "$TEMPLATE" "$OUT_DIR/index.html"
fi

# Compute links from the new deck to this skill's shared assets, independent
# of whether the output parent is shallow, nested, absolute, or spaceful.
ASSET_REL="$(python3 - "$HERE/assets" "$OUT_DIR" <<'PY'
import os, sys
print(os.path.relpath(sys.argv[1], sys.argv[2]).replace(os.sep, "/") + "/")
PY
)"
python3 - "$OUT_DIR" "$ASSET_REL" <<'PY'
from pathlib import Path
import re
import sys

output_dir = Path(sys.argv[1])
asset_rel = sys.argv[2]
for output in output_dir.rglob("*"):
    if not output.is_file() or output.suffix.lower() not in {".html", ".css", ".js"}:
        continue
    text = output.read_text(encoding="utf-8")
    text = re.sub(r"(?:\.\./)+assets/", asset_rel, text)
    output.write_text(text, encoding="utf-8")
PY

printf '✔ created %s\n\n' "$(printf '%q' "$OUT_DIR/index.html")"
printf 'next steps:\n'
printf '  open %s\n' "$(printf '%q' "$OUT_DIR/index.html")"
printf '  # press T to cycle themes, ← → to navigate, O for overview\n\n'
printf '  # render to PNG:\n'
printf '  %s %s all\n' \
  "$(printf '%q' "$HERE/scripts/render.sh")" \
  "$(printf '%q' "$OUT_DIR/index.html")"
