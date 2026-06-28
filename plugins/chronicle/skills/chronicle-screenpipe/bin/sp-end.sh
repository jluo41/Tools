#!/usr/bin/env bash
# sp-end.sh — stop the active screenpipe meeting and extract a raw transcript.
#
# Usage:
#   sp-end.sh [--keep-running] [--out <path.md>]
#
# Behavior:
#   1. read marker file written by sp-start.sh
#   2. kill the screenpipe PID (unless --keep-running)
#   3. wait for the last audio chunk to flush to the DB
#   4. call sp-extract.py with the recorded watermarks -> raw markdown
#   5. remove the marker file
#
# The raw .md is printed (path on the last line) so the skill can route it
# through /obsidian-note into a meeting note.

set -euo pipefail

SP_DIR="${SCREENPIPE_DIR:-$HOME/.screenpipe}"
MARKER="$SP_DIR/.active-meeting"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW_ROOT="${SCREENPIPE_RAW_ROOT:-$HOME/Documents/Obsidian Vault/_WorkSpace/screenpipe-raw}"

KEEP=0
OUT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --keep-running) KEEP=1 ;;
    --out) OUT="$2"; shift ;;
    *) echo "✗ unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

[ -f "$MARKER" ] || { echo "✗ no active meeting (marker missing)." >&2; exit 1; }
# shellcheck disable=SC1090
source "$MARKER"

if [ "$KEEP" -eq 0 ] && [ -n "${SP_PID:-}" ]; then
  if kill -0 "$SP_PID" 2>/dev/null; then
    kill "$SP_PID" 2>/dev/null || true
    echo "🛑 stopped screenpipe pid=$SP_PID"
    sleep 3   # let the final audio chunk transcribe + flush
  fi
fi

mkdir -p "$RAW_ROOT"
STAMP=$(date +%y%m%d-%H%M)
OUT="${OUT:-$RAW_ROOT/${STAMP}-${SP_SLUG}.md}"

python3 "$HERE/sp-extract.py" \
  --db "$SP_DIR/db.sqlite" \
  --after-audio-id "${SP_AUDIO_WM:-0}" \
  --after-frame-id "${SP_FRAME_WM:-0}" \
  --slug "$SP_SLUG" \
  --mode "${SP_MODE:-audio-only}" \
  --start-ts "${SP_START_TS:-}" \
  --out "$OUT"

rm -f "$MARKER"
echo "✅ meeting ended. raw transcript:"
echo "$OUT"
