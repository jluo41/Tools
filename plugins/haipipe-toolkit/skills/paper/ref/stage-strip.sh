#!/bin/sh
# stage-strip.sh <paper-dir> — render the haipipe-paper lifecycle stage strip
# from a paper's STATUS.md `current_layer`. Deterministic: same current_layer
# always yields the same strip, so the strip can never be mis-ordered or mis-marked.
#
# Output (one line):
#   seed ✅  pitch ✅  ...  →  write/edit 🚀  →  review ⬜
# Markers: ✅ done   🚀 current (overall frontier)   🔥 worked-this-session   ⬜ not started.
#
# Marker semantics: ✅ = user-confirmed in the Gate Ledger (preferred) or stage
# sits BEFORE current_layer (fallback when no ledger exists). 🚀 = current_layer,
# the paper's OVERALL lifecycle frontier (the strip is overall progress, so this
# is a calm "you-are-here", not "on fire"). 🔥 = the stage worked THIS session
# (optional 2nd arg); shown only when it DIFFERS from the frontier, so the strip
# reads as overall progress while 🔥 flags where this session actually worked.
# ⬜ = not started / not confirmed. See ref/stage-gate.md.
#
# Usage: sh stage-strip.sh [paper-dir] [session-stage]   (paper-dir defaults to
# cwd; looks upward for STATUS.md so it works from inside the paper folder.
# session-stage is an optional spine key, e.g. "minimap", marked 🔥 when it
# differs from current_layer.)

paper="${1:-.}"
session="${2:-}"

# resolve STATUS.md: given dir, else walk upward from it
find_status() {
  d=$(cd "$1" 2>/dev/null && pwd) || return 1
  while [ -n "$d" ] && [ "$d" != "/" ]; do
    [ -f "$d/STATUS.md" ] && { printf '%s\n' "$d/STATUS.md"; return 0; }
    d=$(dirname "$d")
  done
  return 1
}

status=$(find_status "$paper") || { echo "stage-strip: no STATUS.md at or above $paper" >&2; exit 1; }

current=$(grep -m1 '| current_layer |' "$status" | sed 's/.*|[[:space:]]*//' | sed 's/[[:space:]]*|.*//' | tr -d '[:space:]')
# fallback to old format
[ -z "$current" ] && current=$(grep -m1 '^current_layer:' "$status" | sed 's/^current_layer:[[:space:]]*//' | tr -d '[:space:]')

# canonical spine order
keys="seed pitch claims narrative display minimap write-edit review"

# read Gate Ledger: extract confirmed stages into a space-separated string
confirmed=""
if grep -q '## Gate Ledger' "$status"; then
  confirmed=$(awk '/## Gate Ledger/,/^$|^##/' "$status" \
    | grep '| yes |' \
    | sed 's/|[[:space:]]*//' | sed 's/[[:space:]]*|.*//' | tr -d '[:space:]' \
    | tr '\n' ' ')
fi
has_ledger=false
[ -n "$confirmed" ] && has_ledger=true

is_confirmed() {
  case " $confirmed " in *" $1 "*) return 0 ;; esac; return 1
}

# locate current_layer index
cur_idx=-1; i=0
for k in $keys; do
  [ "$k" = "$current" ] && cur_idx=$i
  i=$((i+1))
done

label() { case "$1" in write-edit) printf 'write/edit' ;; *) printf '%s' "$1" ;; esac; }

out=""; i=0
for k in $keys; do
  if [ "$i" -eq "$cur_idx" ]; then
    m="🚀"
  elif [ -n "$session" ] && [ "$k" = "$session" ]; then
    m="🔥"
  elif [ "$has_ledger" = true ]; then
    if is_confirmed "$k"; then m="✅"; else m="⬜"; fi
  elif [ "$i" -lt "$cur_idx" ]; then
    m="✅"
  else
    m="⬜"
  fi
  seg="$(label "$k") $m"
  if [ -z "$out" ]; then
    out="$seg"
  else
    case "$k" in
      write-edit|review) out="$out  →  $seg" ;;
      *)                 out="$out  $seg" ;;
    esac
  fi
  i=$((i+1))
done

printf '%s\n' "$out"
