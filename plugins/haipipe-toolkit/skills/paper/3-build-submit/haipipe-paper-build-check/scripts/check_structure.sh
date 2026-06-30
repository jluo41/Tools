#!/bin/bash
# check_structure.sh : conformance audit against the gold-standard paper folder
# layout (4-build-submit/_shared/paper-folder-anatomy.md, grounded in
# Paper-MapPhyTrait-npjDM2025).
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

echo "== paper-structure-check: $(pwd)"

# ---------- A. master documents ----------
MASTERS=$(ls 0-*.tex 2>/dev/null | grep -v -- '-DIFF')
if [ -z "$MASTERS" ]; then
  bad "no 0-*.tex master document found (is this a paper folder?)"
  echo "== verdict: ✗ not a conforming paper folder"
  exit 2
fi
for m in $MASTERS; do
  if grep -q '^[^%]*\\documentclass' "$m"; then
    ok "master: $m"
  else
    bad "master $m has no \\documentclass"
  fi
done

# ---------- B. compile script ----------
if [ -x 1-compile.sh ]; then ok "1-compile.sh present + executable"
elif [ -f 1-compile.sh ]; then warn "1-compile.sh present but not executable (chmod +x 1-compile.sh)"
else bad "1-compile.sh missing (paper-scaffold templates/compile.sh.tpl provides it)"
fi

# ---------- C. 0-sections naming grammar + numbering ----------
SECTION_FILES=""
if [ ! -d 0-sections ]; then
  bad "0-sections/ missing"
else
  SECTION_FILES=$(ls 0-sections/*.tex 2>/dev/null)
  [ -z "$SECTION_FILES" ] && warn "0-sections/ has no .tex files"

  NAME_RE='^([0-9]{2}(-[0-9]{2})?|[A-Z])_[A-Za-z0-9._-]+\.tex$'
  for f in $SECTION_FILES; do
    b=$(basename "$f")
    echo "$b" | grep -qE "$NAME_RE" || bad "naming: $b does not match NN[-MM]_<slug>.tex / X_<slug>.tex"
  done

  # top-level NN contiguity
  TGAPS=$(ls 0-sections 2>/dev/null | grep -E '^[0-9]{2}_' | sed -E 's/^([0-9]{2})_.*/\1/' | sort -u | awk '
    NR > 1 && $1 + 0 != prev + 1 { printf "section numbering gap: %02d then %02d\n", prev, $1 + 0 }
    { prev = $1 + 0 }')
  if [ -n "$TGAPS" ]; then echo "$TGAPS" | while read -r line; do printf '  ✗ %s\n' "$line"; done; FAIL=1; fi

  # NN-MM contiguity within each section group
  GAPS=$(ls 0-sections 2>/dev/null | grep -E '^[0-9]{2}-[0-9]{2}_' | sed -E 's/^([0-9]{2})-([0-9]{2})_.*/\1 \2/' | sort | awk '
    function flush(  i) { for (i = 1; i < n; i++) if (mm[i] != mm[i-1] + 1) printf "subsection numbering gap in %s: %02d then %02d (close the gap, rewire \\input)\n", g, mm[i-1], mm[i] }
    $1 != g { if (g != "") flush(); g = $1; n = 0 }
    { mm[n++] = $2 + 0 }
    END { if (g != "") flush() }')
  if [ -n "$GAPS" ]; then echo "$GAPS" | while read -r line; do printf '  ✗ %s\n' "$line"; done; FAIL=1; fi

  # NN-MM leaves without an NN_ wrapper file
  for g in $(ls 0-sections 2>/dev/null | grep -E '^[0-9]{2}-' | cut -c1-2 | sort -u); do
    ls 0-sections/${g}_*.tex >/dev/null 2>&1 || warn "section $g has NN-MM leaves but no ${g}_<slug>.tex wrapper"
  done
fi

ALL_TEX="$MASTERS $SECTION_FILES"

# ---------- D. \input wiring: orphans / double-inputs ----------
N_WRAP=0; N_LEAF=0
for f in $SECTION_FILES; do
  b=$(basename "$f" .tex)
  N=$(cat $ALL_TEX 2>/dev/null | grep -v '^[[:space:]]*%' | grep -F -e "\\input{0-sections/$b}" -e "\\input{0-sections/$b.tex}" | wc -l | tr -d ' ')
  if [ "$N" -eq 0 ]; then bad "orphan: 0-sections/$b.tex is never \\input by any master or wrapper"
  elif [ "$N" -gt 1 ]; then warn "0-sections/$b.tex is \\input $N times"
  fi
done

# ---------- E. file roles ----------
for f in $SECTION_FILES; do
  grep -q '\\documentclass' "$f" && bad "$f contains \\documentclass (only 0-*.tex masters may)"
  if grep -v '^[[:space:]]*%' "$f" | grep -q '\\input{0-sections/'; then
    N_WRAP=$((N_WRAP+1))
    IMPURE=$(grep -v '^[[:space:]]*%' "$f" | grep -v '^[[:space:]]*$' | grep -cv '\\input{0-sections/' | tr -d ' ')
    [ "$IMPURE" -gt 0 ] && bad "wrapper $f contains $IMPURE non-\\input line(s); prose belongs in a leaf"
  else
    N_LEAF=$((N_LEAF+1))
    grep -v '^[[:space:]]*%' "$f" | grep -qE '\\section\{' && warn "leaf $f has an unstarred \\section{} (the driver owns \\section headings; \\section*{} is fine)"
  fi
done
[ -n "$SECTION_FILES" ] && ok "file roles: $N_WRAP wrapper(s), $N_LEAF leaf/leaves scanned"

# ---------- F. \input targets exist ----------
MISS_IN=0
while read -r tgt; do
  [ -z "$tgt" ] && continue
  if [ ! -f "$tgt" ] && [ ! -f "$tgt.tex" ]; then bad "broken \\input target: $tgt"; MISS_IN=1; fi
done < <(cat $ALL_TEX 2>/dev/null | grep -v '^[[:space:]]*%' | grep -oE '\\input\{[^}]*\}' | sed -E 's/\\input\{([^}]*)\}/\1/' | sort -u)
[ "$MISS_IN" -eq 0 ] && ok "all \\input targets resolve"

# ---------- G. \includegraphics targets exist ----------
MISS_IMG=0
while read -r img; do
  [ -z "$img" ] && continue
  if [ ! -f "$img" ] && [ ! -f "$img.pdf" ] && [ ! -f "$img.png" ] && [ ! -f "$img.jpg" ] && [ ! -f "$img.jpeg" ] && [ ! -f "$img.eps" ]; then
    bad "missing graphic: $img"
    MISS_IMG=1
  fi
done < <(cat $ALL_TEX 2>/dev/null | grep -v '^[[:space:]]*%' | grep -oE '\\includegraphics(\[[^][]*\])?\{[^}]*\}' | sed -E 's/.*\{([^}]*)\}$/\1/' | sort -u)
[ "$MISS_IMG" -eq 0 ] && ok "all \\includegraphics targets resolve"

# ---------- H. bibliography resolves ----------
for m in $MASTERS; do
  for bb in $(grep -v '^[[:space:]]*%' "$m" | grep -oE '\\bibliography\{[^}]*\}' | sed -E 's/\\bibliography\{([^}]*)\}/\1/' | tr ',' ' '); do
    if [ -f "$bb.bib" ]; then ok "$m → $bb.bib"; else bad "$m: \\bibliography{$bb} but $bb.bib not found"; fi
  done
done

# ---------- I. aux hygiene ----------
AUX=$(ls *.aux *.log *.bbl *.blg *.out 2>/dev/null | wc -l | tr -d ' ')
[ "$AUX" -gt 0 ] && warn "$AUX aux file(s) lingering at top level (run ./1-compile.sh --clean-only)"

# ---------- verdict ----------
echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "== verdict: ✓ conforms ($WARN warning(s))"
  exit 0
else
  echo "== verdict: ✗ non-conforming ($WARN warning(s)); see haipipe-paper-build-check/SKILL.md for fix routing"
  exit 1
fi
