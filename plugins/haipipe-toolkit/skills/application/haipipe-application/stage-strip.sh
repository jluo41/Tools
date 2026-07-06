#!/bin/sh
# stage-strip.sh <intervention-dir> — render the haipipe-application lifecycle
# stage strip from an intervention's STATUS.md. Deterministic: same STATUS.md
# always yields the same strip, so it can never be mis-ordered or mis-marked.
#
# Output (one line):
#   seed ✅  claims 🔥🚀  venue ⬜  pitch ⬜  narrative --  display --  section-edit --  →  draft ⬜  →  review ⬜  →  deploy ⬜
# Markers per haipipe-application/SKILL.md Closing Block (single source of truth):
#   🔥 = active now (the stage worked THIS session, optional 2nd arg)
#   🚀 = frontier (current_layer, the farthest stage the intervention has reached)
#   🔥🚀 = collapsed when the session works AT the frontier
#   ✅ = user-confirmed in the Gate Ledger (preferred) or stage sits BEFORE
#        current_layer (fallback when no ledger exists); venue slot = pinned
#   ⬜ = not started / not confirmed
#   -- = skipped by the pinned venue (STATUS.md `| stages_skipped |`, written at
#        venue pin time); a skipped stage can never carry 🔥 or 🚀.
#   Gate rules: wiki/08-stage-gate.md.
#
# Usage: sh stage-strip.sh [intervention-dir] [session-stage]   (dir defaults to
# cwd; looks upward for STATUS.md so it works from inside the intervention.
# session-stage is an optional spine key, e.g. "claims", marked 🔥; when it
# equals current_layer the two markers collapse to 🔥🚀.)

app="${1:-.}"
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

status=$(find_status "$app") || { echo "stage-strip: no STATUS.md at or above $app" >&2; exit 1; }

current=$(grep -m1 '^| current_layer |' "$status" | sed 's/^|[^|]*|[[:space:]]*//' | sed 's/[[:space:]]*|.*//' | tr -d '[:space:]')
# fallback to old format
[ -z "$current" ] && current=$(grep -m1 '^current_layer:' "$status" | sed 's/^current_layer:[[:space:]]*//' | tr -d '[:space:]')
# normalize numbered stage-folder names (1-claims -> claims); spine keys are bare
current=$(printf '%s' "$current" | sed 's/^[0-9]-//')

# canonical spine order: venue coupling gradient FREE→FREE→(pin)→ALIGNED, then delivery tail
# seed(FREE) claims(FREE) venue(chooser) pitch narrative display section-edit(ALIGNED, venue-gated) draft review deploy
keys="seed claims venue pitch narrative display section-edit draft review deploy"

# venue is confirmed by a pinned `| venue |` field in STATUS.md, not a ledger row
venue_pinned=false
v=$(grep -m1 '^| venue |' "$status" | sed 's/^|[^|]*|[[:space:]]*//' | sed 's/[[:space:]]*|.*//')
[ -n "$v" ] && venue_pinned=true

# venue-skipped stages: `| stages_skipped | narrative display section-edit |` row, written at pin time
skipped=$(grep -m1 '^| stages_skipped |' "$status" | sed 's/^|[^|]*|[[:space:]]*//' | sed 's/[[:space:]]*|.*$//')
is_skipped() {
  case " $skipped " in *" $1 "*) return 0 ;; esac; return 1
}

# read Gate Ledger: extract confirmed stages into a space-separated string
# (flag-based scan: the ledger table may sit after a blank line; end only at the next ## heading)
confirmed=""
if grep -q '## Gate Ledger' "$status"; then
  confirmed=$(awk '/^## Gate Ledger/{f=1;next} f&&/^## /{f=0} f' "$status" \
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

out=""; i=0
for k in $keys; do
  if is_skipped "$k"; then
    # skipped stages can never carry 🔥/🚀/✅ — venue declared them out
    m="--"
  elif [ "$i" -eq "$cur_idx" ]; then
    # frontier; collapse to 🔥🚀 when this session works AT the frontier
    if [ -n "$session" ] && [ "$k" = "$session" ]; then m="🔥🚀"; else m="🚀"; fi
  elif [ -n "$session" ] && [ "$k" = "$session" ]; then
    m="🔥"
  elif [ "$k" = "venue" ]; then
    if [ "$venue_pinned" = true ]; then m="✅"; else m="⬜"; fi
  elif [ "$has_ledger" = true ]; then
    if is_confirmed "$k"; then m="✅"; else m="⬜"; fi
  elif [ "$i" -lt "$cur_idx" ]; then
    m="✅"
  else
    m="⬜"
  fi
  seg="$k $m"
  if [ -z "$out" ]; then
    out="$seg"
  else
    case "$k" in
      draft|review|deploy) out="$out  →  $seg" ;;
      *)                   out="$out  $seg" ;;
    esac
  fi
  i=$((i+1))
done

printf '%s\n' "$out"
