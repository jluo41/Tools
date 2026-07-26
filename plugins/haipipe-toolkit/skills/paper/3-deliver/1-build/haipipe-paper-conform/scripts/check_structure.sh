#!/bin/bash
# check_structure.sh : conformance audit against the paper-folder layout ruled on
# 2026-07-26 (design board QA6, "the paper folder: what exists on disk").
#
# THE CONTRACT, in one line:
#   the NUMBER is the delete test. `rm -rf 0-* 1-* 2-*` must leave a paper that
#   still compiles and still submits.
#
#   0-lifecycle/  the board, and nothing but the board
#   1-probes/     the near side of the wall
#   2-src/        how the deliverable is BUILT, not what it is
#   everything unnumbered  IS the deliverable
#
# Usage: check_structure.sh [paper-dir]     (default: .)
# Exit:  0 = conforms   1 = findings   2 = not a paper folder / usage error
#
# Report-only: never modifies anything. macOS bash 3.2 compatible.

DIR="${1:-.}"
cd "$DIR" 2>/dev/null || { echo "✗ not a directory: $DIR"; exit 2; }

FAIL=0
WARN=0
ok()   { printf '  ✓ %s\n' "$*"; }
bad()  { printf '  ✗ %s\n' "$*"; FAIL=1; }
warn() { printf '  ⚠ %s\n' "$*"; WARN=$((WARN+1)); }
hdr()  { printf '\n-- %s\n' "$*"; }

echo "== paper-structure-check: $(pwd)"

FAMILIES="Seed Work Venue Display Main Appendix Submission Round"

# ---------- A. is this a paper folder at all ----------
hdr "A. paper folder"
if [ ! -d 0-lifecycle ]; then
  bad "0-lifecycle/ missing (every paper is Board-first; this is not a paper folder)"
  echo ""
  echo "== verdict: ✗ not a conforming paper folder"
  exit 2
fi
ok "0-lifecycle/ present"

# ---------- B. three numbered folders, and only three ----------
hdr "B. numbered entries (three folders, and only three)"
STRAY=0
for e in [0-9]-*; do
  [ -e "$e" ] || continue
  case "$e" in
    0-lifecycle|1-probes|2-src) ;;
    *)
      STRAY=1
      if [ -d "$e" ]; then
        bad "$e/ carries a number but is not one of the three (0-lifecycle 1-probes 2-src)"
      else
        bad "$e is a numbered FILE; the prefix is reserved for the three working folders"
      fi
      ;;
  esac
done
[ -d 1-probes ] || warn "1-probes/ missing (created on first probe; absent is legal on a young paper)"
[ -d 2-src ]    || warn "2-src/ missing (arrives with the manuscript upgrade; absent is legal before Display)"
[ "$STRAY" -eq 0 ] && ok "no stray numbered entries"

# ---------- C. no second home for an asset ----------
hdr "C. displays/ is the only home of an asset"
[ -d figures ]    && bad "figures/ exists; a display is a UNIT and its render lives in displays/<unit>/assets/"
[ -d Figures ]    && bad "Figures/ exists; same rule as figures/"
[ -d 0-displays ] && bad "0-displays/ is the OLD name and the old prefix; the deliverable's displays are displays/"
if [ -d displays ]; then
  for b in displays/Figure displays/Table displays/AppendixFigure displays/AppendixTable; do
    [ -d "$b" ] && bad "$b/ is a legacy flat bucket; unitize it into displays/displayNN-<slug>/"
  done
fi
ok "asset-home check complete"

# ---------- D. 0-lifecycle purity + one family, one folder ----------
hdr "D. 0-lifecycle/ purity and family mapping"
for e in 0-lifecycle/*; do
  [ -e "$e" ] || continue
  b=$(basename "$e")
  if [ -d "$e" ]; then
    case "$b" in
      0-seed|1-work|2-venue|3-display|4-main|5-appendix|6-submission|7-round|_archive) ;;
      *) bad "0-lifecycle/$b/ is not one of the eight family folders (0-seed 1-work 2-venue 3-display 4-main 5-appendix 6-submission 7-round) or _archive" ;;
    esac
  else
    case "$b" in
      board.md|board.html|README.md) ;;
      *) bad "0-lifecycle/$b is not the board's own index; the board holds S pages and nothing else" ;;
    esac
  fi
done

for f in 0-lifecycle/*/*; do
  [ -e "$f" ] || continue
  d=$(basename "$(dirname "$f")")
  b=$(basename "$f")
  [ "$d" = "_archive" ] && continue
  [ "$b" = "_archive" ] && continue      # every family may keep its own _archive/
  case "$b" in
    S-*.md) ;;
    *)
      if [ -d "$f" ]; then
        bad "0-lifecycle/$d/$b/ is a folder inside a family folder; a family holds S pages and _archive/, nothing else"
      else
        bad "0-lifecycle/$d/$b is not an S page; the board is pure (move build products and sidecars out)"
      fi
      continue ;;
  esac
  fam=$(echo "$b" | sed -E 's/^S-([A-Za-z]+)-.*/\1/')
  case "$fam" in
    Seed)       want=0-seed ;;
    Work)       want=1-work ;;
    Venue)      want=2-venue ;;
    Display)    want=3-display ;;
    Main)       want=4-main ;;
    Appendix)   want=5-appendix ;;
    Submission) want=6-submission ;;
    Round)      want=7-round ;;
    *) bad "0-lifecycle/$d/$b names family '$fam', which is not one of: $FAMILIES"; continue ;;
  esac
  [ "$d" = "$want" ] || bad "0-lifecycle/$d/$b belongs in $want/ (one family, one folder)"
done
[ -f 0-lifecycle/board.md ] || bad "0-lifecycle/board.md missing (the board's spine)"

# ---------- E. masters ----------
hdr "E. master documents"
MASTERS=$(ls *.tex 2>/dev/null | grep -v -- '-DIFF' | while read -r m; do
  grep -q '^[^%]*\\documentclass' "$m" && echo "$m"
done)
if [ -z "$MASTERS" ]; then
  warn "no unnumbered master .tex with \\documentclass (legal before the manuscript upgrade)"
else
  for m in $MASTERS; do ok "master: $m"; done
fi

# ---------- F. build script ----------
hdr "F. build"
[ -f 1-compile.sh ] && bad "1-compile.sh is the OLD path; the build script lives in 2-src/"
if [ -n "$MASTERS" ]; then
  if [ -x 2-src/compile.sh ];   then ok "2-src/compile.sh present + executable"
  elif [ -f 2-src/compile.sh ]; then warn "2-src/compile.sh present but not executable (chmod +x 2-src/compile.sh)"
  else bad "2-src/compile.sh missing; a paper with a master owes a build script"
  fi
else
  ok "no master yet, so no build script is owed"
fi

# ---------- G. sections/ naming grammar + numbering ----------
hdr "G. sections/ naming"
[ -d 0-sections ] && bad "0-sections/ is the OLD name and the old prefix; generated prose is unnumbered, in sections/"
SECTION_FILES=""
for d in sections appendices; do
  [ -d "$d" ] || continue
  SECTION_FILES="$SECTION_FILES $(ls $d/*.tex 2>/dev/null)"
done

if [ -n "$(echo $SECTION_FILES | tr -d ' ')" ]; then
  NAME_RE='^([0-9]{2}(-[0-9]{2})?|[A-Z])_[A-Za-z0-9._-]+\.tex$'
  for f in $SECTION_FILES; do
    b=$(basename "$f")
    echo "$b" | grep -qE "$NAME_RE" || bad "naming: $b does not match NN[-MM]_<slug>.tex / X_<slug>.tex"
  done

  TGAPS=$(ls sections 2>/dev/null | grep -E '^[0-9]{2}_' | sed -E 's/^([0-9]{2})_.*/\1/' | sort -u | awk '
    NR > 1 && $1 + 0 != prev + 1 { printf "section numbering gap: %02d then %02d\n", prev, $1 + 0 }
    { prev = $1 + 0 }')
  if [ -n "$TGAPS" ]; then echo "$TGAPS" | while read -r line; do printf '  ✗ %s\n' "$line"; done; FAIL=1; fi

  GAPS=$(ls sections 2>/dev/null | grep -E '^[0-9]{2}-[0-9]{2}_' | sed -E 's/^([0-9]{2})-([0-9]{2})_.*/\1 \2/' | sort | awk '
    function flush(  i) { for (i = 1; i < n; i++) if (mm[i] != mm[i-1] + 1) printf "subsection numbering gap in %s: %02d then %02d (close the gap, rewire \\input)\n", g, mm[i-1], mm[i] }
    $1 != g { if (g != "") flush(); g = $1; n = 0 }
    { mm[n++] = $2 + 0 }
    END { if (g != "") flush() }')
  if [ -n "$GAPS" ]; then echo "$GAPS" | while read -r line; do printf '  ✗ %s\n' "$line"; done; FAIL=1; fi

  for g in $(ls sections 2>/dev/null | grep -E '^[0-9]{2}-' | cut -c1-2 | sort -u); do
    ls sections/${g}_*.tex >/dev/null 2>&1 || warn "section $g has NN-MM leaves but no ${g}_<slug>.tex wrapper"
  done
else
  ok "no generated prose yet (sections/ is written at the section frontier)"
fi

ALL_TEX="$MASTERS $SECTION_FILES"
[ -d displays ] && ALL_TEX="$ALL_TEX $(ls displays/*/float.tex 2>/dev/null)"

# ---------- H. \input wiring: orphans / double-inputs ----------
hdr "H. \\input wiring"
N_WRAP=0; N_LEAF=0
for f in $SECTION_FILES; do
  b="${f%.tex}"
  N=$(cat $ALL_TEX 2>/dev/null | grep -v '^[[:space:]]*%' | grep -F -e "\\input{$b}" -e "\\input{$b.tex}" | wc -l | tr -d ' ')
  if [ "$N" -eq 0 ];   then bad "orphan: $f is never \\input by any master or wrapper"
  elif [ "$N" -gt 1 ]; then warn "$f is \\input $N times"
  fi
done

for f in $SECTION_FILES; do
  grep -q '\\documentclass' "$f" && bad "$f contains \\documentclass (only an unnumbered master may)"
  if grep -v '^[[:space:]]*%' "$f" | grep -qE '\\input\{(sections|appendices)/'; then
    N_WRAP=$((N_WRAP+1))
    IMPURE=$(grep -v '^[[:space:]]*%' "$f" | grep -v '^[[:space:]]*$' | grep -cvE '\\input\{(sections|appendices)/' | tr -d ' ')
    [ "$IMPURE" -gt 0 ] && bad "wrapper $f contains $IMPURE non-\\input line(s); prose belongs in a leaf"
  else
    N_LEAF=$((N_LEAF+1))
    grep -v '^[[:space:]]*%' "$f" | grep -qE '\\section\{' && warn "leaf $f has an unstarred \\section{} (the driver owns \\section headings; \\section*{} is fine)"
  fi
done
[ -n "$(echo $SECTION_FILES | tr -d ' ')" ] && ok "file roles: $N_WRAP wrapper(s), $N_LEAF leaf/leaves scanned"

# ---------- I. targets resolve ----------
hdr "I. \\input / \\includegraphics / \\bibliography targets"
TARGETS=$(cat $ALL_TEX 2>/dev/null | grep -v '^[[:space:]]*%' \
  | grep -oE '\\(input|includegraphics(\[[^][]*\])?|bibliography)\{[^}]*\}' \
  | sed -E 's/.*\{([^}]*)\}$/\1/' | tr ',' '\n' | sort -u)

MISS=0
for tgt in $TARGETS; do
  [ -z "$tgt" ] && continue
  FOUND=0
  for ext in "" .tex .pdf .png .jpg .jpeg .eps .bib; do
    [ -f "$tgt$ext" ] && FOUND=1 && break
  done
  [ "$FOUND" -eq 0 ] && { bad "broken target: $tgt"; MISS=1; }
done
[ "$MISS" -eq 0 ] && ok "all \\input / \\includegraphics / \\bibliography targets resolve"

# ---------- J. THE DELETE TEST ----------
hdr "J. the delete test: rm -rf 0-* 1-* 2-*"
DT=0
for tgt in $TARGETS; do
  case "$tgt" in
    0-*|1-*|2-*) bad "DELETE TEST: a master reaches $tgt, which rm -rf 0-* 1-* 2-* would remove"; DT=1 ;;
  esac
done
for m in $MASTERS; do
  case "$m" in 0-*|1-*|2-*) bad "DELETE TEST: the master $m is itself numbered"; DT=1 ;; esac
done
for e in *.bib *.cls *.bst; do
  [ -e "$e" ] || continue
  case "$e" in 0-*|1-*|2-*) bad "DELETE TEST: $e is deliverable but numbered"; DT=1 ;; esac
done
[ "$DT" -eq 0 ] && ok "nothing the deliverable needs sits behind a number"

# ---------- K. hygiene ----------
hdr "K. hygiene"
AUX=$(ls *.aux *.log *.bbl *.blg *.out 2>/dev/null | wc -l | tr -d ' ')
if [ "$AUX" -gt 0 ]; then warn "$AUX aux file(s) lingering at top level (2-src/compile.sh --clean-only)"
else ok "no lingering aux files"; fi
[ -f STATUS.md ] && warn "STATUS.md present; its frontier is derived from disk, and a stored frontier can only go stale (design board QA6)"

# ---------- verdict ----------
echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "== verdict: ✓ conforms ($WARN warning(s))"
  exit 0
else
  echo "== verdict: ✗ non-conforming ($WARN warning(s)); see haipipe-paper-conform/SKILL.md for fix routing"
  exit 1
fi
