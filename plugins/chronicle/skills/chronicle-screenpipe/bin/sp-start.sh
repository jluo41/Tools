#!/usr/bin/env bash
# sp-start.sh — start a scoped screenpipe recording for ONE meeting.
#
# Usage:
#   sp-start.sh <slug> [--with-vision]
#
# Default is AUDIO-ONLY (screenpipe --disable-vision): mic + system audio,
# no screen capture, no OCR frames. Pass --with-vision to also record the
# screen (slides/shared docs become selectable "iframes" at extract time).
#
# Behavior:
#   1. refuse if a meeting is already active (marker file exists)
#   2. read MAX(id) of audio_transcriptions / frames  -> watermarks
#      (this is how `end` knows what is "new" — timezone-free)
#   3. launch screenpipe detached (nohup), write PID + watermarks to marker
#
# Marker file: $SP_DIR/.active-meeting  (JSON-ish, sourced by sp-end.sh)

set -euo pipefail

SP_DIR="${SCREENPIPE_DIR:-$HOME/.screenpipe}"
SP_BIN="${SCREENPIPE_BIN:-$HOME/.local/bin/screenpipe}"
DB="$SP_DIR/db.sqlite"
MARKER="$SP_DIR/.active-meeting"
LOG="$SP_DIR/.active-meeting.log"

usage() { echo "Usage: $0 <slug> [--with-vision]" >&2; exit 2; }

[ $# -ge 1 ] || usage
SLUG="$1"; shift || true
VISION_FLAG="--disable-vision"
MODE="audio-only"
for arg in "$@"; do
  case "$arg" in
    --with-vision) VISION_FLAG=""; MODE="audio+vision" ;;
    *) echo "✗ unknown arg: $arg" >&2; usage ;;
  esac
done

if ! [[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+){0,5}$ ]]; then
  echo "✗ slug must be lowercase hyphenated tokens, got: $SLUG" >&2; exit 2
fi
[ -x "$SP_BIN" ] || { echo "✗ screenpipe not found at $SP_BIN" >&2; exit 1; }
[ -f "$DB" ]     || { echo "✗ db not found at $DB" >&2; exit 1; }

if [ -f "$MARKER" ]; then
  echo "✗ a meeting is already active. Run sp-end.sh first:" >&2
  cat "$MARKER" >&2
  exit 1
fi

# Timezone-free watermarks: everything created after these ids belongs to this meeting.
AUDIO_WM=$(sqlite3 "$DB" "SELECT COALESCE(MAX(id),0) FROM audio_transcriptions;")
FRAME_WM=$(sqlite3 "$DB" "SELECT COALESCE(MAX(id),0) FROM frames;")
START_TS=$(date +%Y-%m-%dT%H:%M:%S)

# Launch detached. screenpipe records until killed.
nohup "$SP_BIN" $VISION_FLAG >"$LOG" 2>&1 &
PID=$!
sleep 2
if ! kill -0 "$PID" 2>/dev/null; then
  echo "✗ screenpipe failed to start — see $LOG" >&2
  tail -5 "$LOG" >&2 || true
  exit 1
fi

cat > "$MARKER" <<EOF
SP_SLUG=$SLUG
SP_MODE=$MODE
SP_PID=$PID
SP_START_TS=$START_TS
SP_AUDIO_WM=$AUDIO_WM
SP_FRAME_WM=$FRAME_WM
EOF

echo "🎙️  recording started — slug=$SLUG mode=$MODE pid=$PID"
echo "    audio watermark=$AUDIO_WM  frame watermark=$FRAME_WM"
echo "    stop with: sp-end.sh   (logs: $LOG)"
