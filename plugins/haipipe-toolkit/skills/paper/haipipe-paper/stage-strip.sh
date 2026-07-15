#!/bin/sh
# stage-strip.sh <paper-dir> — render the haipipe-paper lifecycle stage strip
# from a paper's STATUS.md `current_layer`. Deterministic: same current_layer
# always yields the same strip, so the strip can never be mis-ordered or mis-marked.
#
# Output (one line):
#   seed 🔥  claims ✅  pitch ✅  ...  →  section-edit 🚀  →  review ⬜
# Markers per haipipe-paper/SKILL.md Closing Block (single source of truth):
#   🔥 = active now (the stage worked THIS session, optional 2nd arg)
#   🚀 = frontier (current_layer, the farthest stage the paper has reached)
#   🔥🚀 = collapsed when the session works AT the frontier
#   ✅ = user-confirmed in the Gate Ledger (preferred) or stage sits BEFORE
#        current_layer (fallback when no ledger exists)
#   ⬜ = not started / not confirmed. Gate rules: wiki/08-stage-gate.md.
#
# Usage: sh stage-strip.sh [paper-dir] [session-stage]   (paper-dir defaults to
# cwd; looks upward for STATUS.md so it works from inside the paper folder.
# session-stage is an optional spine key, e.g. "seed", marked 🔥; when it equals
# current_layer the two markers collapse to 🔥🚀.)

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

current=$(grep -m1 '^| current_layer |' "$status" | sed 's/^|[^|]*|[[:space:]]*//' | sed 's/[[:space:]]*|.*//' | tr -d '[:space:]')
# fallback to old format
[ -z "$current" ] && current=$(grep -m1 '^current_layer:' "$status" | sed 's/^current_layer:[[:space:]]*//' | tr -d '[:space:]')
# normalize numbered stage-folder names (1-claims -> claims); spine keys are bare
current=$(printf '%s' "$current" | sed -E 's/^[0-9]+[a-z]?-//')

# canonical spine order: venue coupling gradient FREE→ALIGNED→HEAVY→SPECIFIC
# seed(FREE) resource(FREE) claims(FREE) venue(chooser) pitch(ALIGNED=cover letter) narrative(ALIGNED) display(HEAVY) section-edit(SPECIFIC) review
# resource added 2026-07-14 (JL): what must EXIST for the paper to be testable.
# The NUMBER is decoration -- this list is the only machine-readable ordering in
# the toolkit, and line ~40 strips the numeric+letter prefix before matching.
# The SKILL folders are 1a-resource/ and 1b-claims/; the paper's 0-lifecycle/ folders stay 1-resource/1-claims/.
keys="seed resource claims venue pitch narrative display section-edit review"

# Does this stage have an artifact folder on disk? (0-lifecycle/<N>-<key>/ or
# 0-lifecycle/<key>/ -- the number varies across papers, so match on the KEY.)
paper_dir=$(dirname "$status")
stage_has_artifact() {
  for d in "$paper_dir"/0-lifecycle/*-"$1" "$paper_dir"/0-lifecycle/"$1"; do
    [ -d "$d" ] && return 0
  done
  return 1
}

# venue is confirmed by a pinned `| venue |` field in STATUS.md, not a ledger row
venue_pinned=false
v=$(grep -m1 '^| venue |' "$status" | sed 's/^|[^|]*|[[:space:]]*//' | sed 's/[[:space:]]*|.*//')
[ -n "$v" ] && venue_pinned=true

# read Gate Ledger: extract confirmed stages into a space-separated string
# (flag-based scan: the ledger table may sit after a blank line; end only at the next ## heading)
confirmed=""
if grep -q '## Gate Ledger' "$status"; then
  confirmed=$(awk '/^## Gate Ledger/{f=1;next} f&&/^## /{f=0} f' "$status" \
    | grep '| yes |' \
    | sed 's/|[[:space:]]*//' | sed 's/[[:space:]]*|.*//' | tr -d ' \t' \
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

# An unknown current_layer used to fail SILENTLY: cur_idx stayed -1, no branch
# caught it, and the strip rendered EVERY stage ⬜ and exited 0 -- so a paper at
# its frontier reported as untouched. (Live today: Paper-CGMtoHbA1c's
# `write/edit` is not a spine key.) Never fail silently about a paper's position.
if [ "$cur_idx" -eq -1 ]; then
  echo "stage-strip: WARNING -- current_layer '${current:-<empty>}' is not a spine key." >&2
  echo "stage-strip:            spine: $keys" >&2
  echo "stage-strip:            the strip below has NO frontier marker and is not trustworthy." >&2
fi

label() { case "$1" in write-edit) printf 'write/edit' ;; *) printf '%s' "$1" ;; esac; }

out=""; i=0
for k in $keys; do
  if [ "$i" -eq "$cur_idx" ]; then
    # frontier; collapse to 🔥🚀 when this session works AT the frontier
    if [ -n "$session" ] && [ "$k" = "$session" ]; then m="🔥🚀"; else m="🚀"; fi
  elif [ -n "$session" ] && [ "$k" = "$session" ]; then
    m="🔥"
  elif [ "$k" = "venue" ]; then
    if [ "$venue_pinned" = true ]; then m="✅"; else m="⬜"; fi
  elif [ "$has_ledger" = true ]; then
    if is_confirmed "$k"; then m="✅"; else m="⬜"; fi
  elif [ "$i" -lt "$cur_idx" ]; then
    # INDEX FALLBACK (fires on every live paper -- zero of them have a machine-
    # readable Gate Ledger, so `has_ledger` is always false). "Before the frontier"
    # is only EVIDENCE of doneness, not proof: inserting a new stage into `keys`
    # would otherwise green-light it instantly on every paper that never ran it.
    # (Adding `resource` before `claims` would have rendered `resource ✅` on 4
    # live papers on commit day, for a stage that has never executed.)
    # So demand an artifact on disk. `review` is post-submission and owns no folder.
    if [ "$k" = "review" ] || stage_has_artifact "$k"; then m="✅"; else m="⬜"; fi
  else
    m="⬜"
  fi
  seg="$(label "$k") $m"
  if [ -z "$out" ]; then
    out="$seg"
  else
    case "$k" in
      section-edit|review) out="$out  →  $seg" ;;
      *)                 out="$out  $seg" ;;
    esac
  fi
  i=$((i+1))
done

printf '%s\n' "$out"
