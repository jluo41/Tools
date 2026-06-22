#!/bin/sh
# stage-strip.sh <paper-dir> — render the haipipe-paper lifecycle stage strip
# from a paper's STATUS.md `current_layer`. Deterministic: same current_layer
# always yields the same strip, so the strip can never be mis-ordered or mis-marked.
#
# Output (one line):
#   seed ✅  pitch ✅  ...  →  write/edit ▶️  →  review ⬜
# Markers: ✅ done   ▶️ current   ⬜ not started.
#
# Marker semantics (CURRENT, pre-gate-ledger): ✅ = stage sits BEFORE current_layer
# in the spine order. Once the Stage Gate confirmation ledger exists, switch ✅ to
# mean "user-confirmed in the ledger" (read the ledger instead of position). See
# feedback/2026-06-22_stage-advance-needs-user-confirm.md.
#
# Usage: sh stage-strip.sh [paper-dir]   (paper-dir defaults to cwd; looks upward
# for STATUS.md so it also works from inside the paper folder).

paper="${1:-.}"

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

current=$(grep -m1 '^current_layer:' "$status" | sed 's/^current_layer:[[:space:]]*//' | tr -d '[:space:]')

# canonical spine order
keys="seed pitch claims narrative display minimap write-edit review"

# locate current_layer index
cur_idx=-1; i=0
for k in $keys; do
  [ "$k" = "$current" ] && cur_idx=$i
  i=$((i+1))
done

label() { case "$1" in write-edit) printf 'write/edit' ;; *) printf '%s' "$1" ;; esac; }

out=""; i=0
for k in $keys; do
  if   [ "$i" -lt "$cur_idx" ]; then m="✅"
  elif [ "$i" -eq "$cur_idx" ]; then m="▶️"
  else                               m="⬜"
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
