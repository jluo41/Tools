#!/usr/bin/env bash
# check_comment_only.sh — gate a 4-edit pass: prove it did NOT change the prose.
#
# Usage:
#   check_comment_only.sh [--mode comment|words] <orig.tex> <new.tex>
#
#   --mode comment  (default)  Annotate / Round-1 gate.
#                              Active prose lines must be BYTE-IDENTICAL, and
#                              every line added vs <orig> must be a LaTeX comment.
#                              Use after Stage 2 (annotate) and any comment-only pass.
#
#   --mode words               Format-check gate (Stage 1).
#                              Same WORDS, re-wrap allowed. Compares prose with
#                              whitespace collapsed, so splitting a paragraph into
#                              one-sentence-per-line passes, but any reworded
#                              token fails.
#
# Exit: 0 = pass, 1 = invariant violated, 2 = usage/IO error.
#
# "Active prose" = every line that is NOT a whole-line LaTeX comment (^ optional
# space then %) and not blank. Escaped %% inside prose (e.g. 95\%) is fine because
# only LINE-LEADING % marks a comment line.

set -u

mode=comment
if [[ "${1:-}" == "--mode" ]]; then mode="${2:-}"; shift 2; fi

orig="${1:-}"; new="${2:-}"
if [[ -z "$orig" || -z "$new" ]]; then
  echo "usage: $0 [--mode comment|words] <orig.tex> <new.tex>" >&2
  exit 2
fi
for f in "$orig" "$new"; do
  [[ -f "$f" ]] || { echo "error: no such file: $f" >&2; exit 2; }
done
case "$mode" in comment|words) ;; *) echo "error: bad --mode '$mode'" >&2; exit 2;; esac

strip() { grep -v '^[[:space:]]*%' "$1" | grep -v '^[[:space:]]*$'; }

fail=0

if [[ "$mode" == "words" ]]; then
  a=$(strip "$orig" | tr -s '[:space:]' ' ')
  b=$(strip "$new"  | tr -s '[:space:]' ' ')
  if [[ "$a" == "$b" ]]; then
    echo "PASS [words]: prose words identical (re-wrap allowed)"
  else
    echo "FAIL [words]: prose WORDS changed (not just layout) —"
    diff <(strip "$orig") <(strip "$new") | sed 's/^/  /'
    fail=1
  fi
else
  # The gate: strip whole-line comments + blanks from both, then diff. If the
  # remaining prose is identical, NO prose was added, deleted, reworded, or
  # reordered. This single check is complete; a raw line-diff is NOT used because
  # inserting comment/banner blocks makes it resync poorly and falsely report
  # prose as "added".
  if diff -q <(strip "$orig") <(strip "$new") >/dev/null; then
    n=$(strip "$orig" | grep -c '')
    co=$(grep -c '^[[:space:]]*%' "$orig" || true)
    cn=$(grep -c '^[[:space:]]*%' "$new"  || true)
    echo "PASS [comment]: active prose byte-identical (${n} prose lines); comment lines ${co} -> ${cn} (+$((cn - co)))"
  else
    echo "FAIL [comment]: prose changed (added / deleted / reworded a non-comment line) —"
    diff <(strip "$orig") <(strip "$new") | sed 's/^/  /'
    fail=1
  fi
fi

exit $fail
