#!/usr/bin/env bash
# html-ppt :: render.sh — headless Chrome screenshot(s)
#
# Usage:
#   render.sh <html-file>                     # one PNG, slide 1
#   render.sh <html-file> <N>                 # N PNGs, slides 1..N, via #/k
#   render.sh <html-file> all                 # autodetect .slide count
#   render.sh <html-file> <N> <out-dir>       # custom output dir
#   render.sh <html-file> <N> <out-dir> <width> <height>
#                                                custom capture dimensions
#
# Requires: Google Chrome at /Applications/Google Chrome.app (macOS).

set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [[ ! -x "$CHROME" ]]; then
  echo "error: Chrome not found at $CHROME" >&2
  exit 1
fi

FILE="${1:-}"
if [[ -z "$FILE" ]]; then
  echo "usage: render.sh <html> [N|all] [out-dir] [width] [height]" >&2
  exit 1
fi
if [[ ! -f "$FILE" ]]; then
  echo "error: $FILE not found" >&2
  exit 1
fi

COUNT="${2:-1}"
OUT="${3:-}"
WIDTH="${4:-1920}"
HEIGHT="${5:-1080}"

if [[ ! "$WIDTH" =~ ^[1-9][0-9]*$ || ! "$HEIGHT" =~ ^[1-9][0-9]*$ ]]; then
  echo "error: width and height must be positive integers" >&2
  exit 1
fi

ABS="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
STEM="$(basename "${FILE%.*}")"

if [[ "$COUNT" == "all" ]]; then
  COUNT="$(grep -c 'class="slide"' "$FILE" || true)"
  [[ -z "$COUNT" || "$COUNT" -lt 1 ]] && COUNT=1
fi

if [[ "$COUNT" != "1" ]]; then
  if [[ -z "$OUT" ]]; then
    OUT="$(dirname "$FILE")/${STEM}-png"
  fi
  mkdir -p "$OUT"
fi

render_one() {
  local url="$1" target="$2"
  "$CHROME" \
    --headless=new \
    --disable-gpu \
    --hide-scrollbars \
    --no-sandbox \
    --virtual-time-budget=4000 \
    --window-size="$WIDTH,$HEIGHT" \
    --screenshot="$target" \
    "$url" >/dev/null 2>&1
  echo "  ✔ $target"
}

if [[ "$COUNT" == "1" ]]; then
  OUT_FILE="${OUT:-$(dirname "$FILE")/${STEM}.png}"
  render_one "file://$ABS" "$OUT_FILE"
else
  for i in $(seq 1 "$COUNT"); do
    render_one "file://$ABS#/$i" "$OUT/${STEM}_$(printf '%02d' "$i").png"
  done
fi

echo "done: rendered $COUNT slide(s) from $FILE"
