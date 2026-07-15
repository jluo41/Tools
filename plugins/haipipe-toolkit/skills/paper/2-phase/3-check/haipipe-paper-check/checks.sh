#!/usr/bin/env bash
# checks.sh — deterministic MECHANICAL sub-checks for haipipe-paper-check.
# ============================================================================
# Runs ONLY the checks that are pure text-matching (no judgment): em-dash,
# AI-voice tells, TODO markers, bibtex-in-markdown, broken \cite (key not in
# any .bib), and unresolved \ref (no matching \label). Judgment checks
# (citation support, value provenance, display correctness, prose quality)
# are NOT here — those are the human's / reviewer's job during CHECK.
#
# Emits one ✅ / ⚠️ / ❌ line per check so the agent can paste results straight
# into the CHECK REPORT and seed > CHECK: comments at the reported line numbers.
#
# Usage:
#   checks.sh <tex-file-or-paper-dir> [--md <file> ...] [--log <file>] [--depth N] [--compile]
#
#   <tex-file-or-paper-dir>  a single .tex, OR a paper dir (all *.tex scanned)
#   --md <file>              a markdown working doc (_CITATION_/_VALUES_/outline)
#                            to scan for bibtex leakage; repeatable
#   --log <file>             a _LOG_*.md changelog: verify the newest [REVISE]
#                            entry carries its `workers:` proof line, and warn
#                            if REVISE ran with no [GATE] draft-review on record
#   --depth N                find maxdepth for *.tex / *.bib when target is a dir
#                            (default 2; raise for deeper layouts / split bibs)
#   --compile                run ./1-compile.sh in the paper dir and grep its log
#                            for LaTeX errors (opt-in; slow; needs a TeX toolchain)
#
# Exit code: 0 if no ❌ (FAIL) items, 1 if any ❌. ⚠️ never fails the run.
# ❌ tier: em-dash, TODO/FIXME, bibtex-in-md, broken \cite, broken \ref, compile,
#          [REVISE] entry without workers: line.
# ⚠️ tier: AI-voice, orphan \label, Pn.Sn sequence, cite-with-no-bib-found,
#          REVISE-without-[GATE]-draft-review.
# Caveat: .bib discovery is bounded by --depth; a split .bib deeper than DEPTH
# makes its keys report as broken \cite — raise --depth rather than trusting a red.
# ============================================================================
set -uo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "usage: checks.sh <tex-file-or-paper-dir> [--md <file> ...] [--depth N] [--compile]" >&2
  exit 2
fi
shift || true

MD_FILES=()
LOG_FILES=()
DEPTH=2
COMPILE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --md) shift; if [[ -z "${1:-}" || "${1:-}" == --* ]]; then echo "--md needs a file argument" >&2; exit 2; fi; MD_FILES+=("$1") ;;
    --log) shift; if [[ -z "${1:-}" || "${1:-}" == --* ]]; then echo "--log needs a file argument" >&2; exit 2; fi; LOG_FILES+=("$1") ;;
    --depth) shift; DEPTH="${1:-2}"
             if ! [[ "$DEPTH" =~ ^[0-9]+$ ]]; then echo "--depth needs a numeric argument, got: $DEPTH" >&2; exit 2; fi ;;
    --compile) COMPILE=1 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift || true
done

# Resolve tex files and paper dir.
if [[ -f "$TARGET" ]]; then
  TEX_FILES=("$TARGET")
  PAPER_DIR="$(dirname "$TARGET")"
elif [[ -d "$TARGET" ]]; then
  PAPER_DIR="$TARGET"
  TEX_FILES=()
  while IFS= read -r _f; do [[ -n "$_f" ]] && TEX_FILES+=("$_f"); done < <(find "$TARGET" -maxdepth "$DEPTH" -name '*.tex' -not -path '*/_archive/*' -not -path '*/_external/*' | sort)
else
  echo "not a file or dir: $TARGET" >&2
  exit 2
fi

FAIL=0
strip_comments() { sed -E 's/(^|[^\\])%.*$/\1/' "$@"; }

echo "# checks.sh — MECHANICAL sub-checks"
echo "# target: $TARGET   tex files: ${#TEX_FILES[@]}   md files: ${#MD_FILES[@]}"
echo "─────────────────────────────────────────────"

# ── REVISE: em-dashes (comments stripped so %% ---- Pn.Sn ---- markers don't hit)
#    ❌ FAIL, not ⚠️: the house rule is absolute (prose-quality.md), same tier as
#    TODO markers (JL 2026-07-07: "统一提议" on making the exit code match the rule).
emdash=$(for f in "${TEX_FILES[@]}"; do
  awk -v F="$f" '{ l=$0; sub(/(^|[^\\])%.*$/,"",l); if (l ~ /---/ || l ~ /—/) printf "%s:%d:%s\n", F, NR, $0 }' "$f" 2>/dev/null
done)
if [[ -z "$emdash" ]]; then
  echo "✅ no em-dashes"
else
  echo "❌ em-dashes found (recast as commas/colons/parens):"; echo "$emdash" | sed 's/^/    /'; FAIL=1
fi

# ── REVISE: AI-voice tells (high-signal only; noisy connectives like
#    Furthermore/Moreover/Additionally are intentionally EXCLUDED — they're
#    legitimate in academic prose and drowned the real tells on live papers)
AI_TELLS='delve|tapestry|realm|seamless|showcase|intricate|nuanced|utilize|underscore|leverage'
# comments stripped (same as em-dash): a "delve" inside a % comment is noise, not prose
# portable (mawk-safe): lowercase + explicit non-letter boundaries, no gawk \< \> / IGNORECASE
aivoice=$(for f in "${TEX_FILES[@]}"; do
  awk -v F="$f" -v P="$AI_TELLS" '{ l=$0; sub(/(^|[^\\])%.*$/,"",l); if (tolower(l) ~ ("(^|[^a-z])(" P ")([^a-z]|$)")) printf "%s:%d:%s\n", F, NR, $0 }' "$f" 2>/dev/null
done)
if [[ -z "$aivoice" ]]; then
  echo "✅ no AI-voice tells"
else
  echo "⚠️ AI-voice tells (confirm each — some may be legitimate):"; echo "$aivoice" | sed 's/^/    /'
fi

# ── META: TODO markers ───────────────────────────────────────────────────────
#    Comments deliberately NOT stripped: legacy % TODO[values] / % TODO[cite] flags are
#    planted in comments by DRAFT and MUST block the gate until PROBE fills them.
#    XXX deliberately EXCLUDED: it collides with double-blind anonymization
#    placeholders (\author{XXX}, "XXX University") that are legitimate at submission.
todos=$(for f in "${TEX_FILES[@]}"; do grep -nHE '\b(TODO|FIXME)\b' "$f" 2>/dev/null; done)
if [[ -z "$todos" ]]; then
  echo "✅ no TODO/FIXME markers"
else
  echo "❌ TODO markers remain:"; echo "$todos" | sed 's/^/    /'; FAIL=1
fi

# ── PROBE/citation: no bibtex in markdown working docs ───────────────────────
if [[ ${#MD_FILES[@]} -gt 0 ]]; then
  # any entry type: @word{key, — anchored to the entry-plus-brace-plus-key-comma
  # shape so venue names with bare @ (e.g. "KHD@IJCAI workshop") don't false-hit
  bibleak=$(for f in "${MD_FILES[@]}"; do [[ -f "$f" ]] && grep -nHE '^\s*@[A-Za-z]+\{[^,}]+,' "$f" 2>/dev/null; done)
  if [[ -z "$bibleak" ]]; then
    echo "✅ no bibtex in markdown (bibtex lives ONLY in .bib)"
  else
    echo "❌ bibtex leaked into markdown (move to .bib):"; echo "$bibleak" | sed 's/^/    /'; FAIL=1
  fi
fi

# ── META/PROBE: broken \cite (key not in any .bib) ───────────────────────────
BIB_FILES=()
while IFS= read -r _f; do [[ -n "$_f" ]] && BIB_FILES+=("$_f"); done < <(find "$PAPER_DIR" -maxdepth "$DEPTH" -name '*.bib' -not -path '*/_archive/*' -not -path '*/_external/*' 2>/dev/null | sort)
has_cites=$(for f in "${TEX_FILES[@]}"; do strip_comments "$f"; done | grep -cE '\\cite' || true)
if [[ ${#BIB_FILES[@]} -eq 0 ]]; then
  if [[ "$has_cites" -gt 0 ]]; then
    # NOT a silent skip: \cite with no discoverable .bib is a real gap
    echo "⚠️ \\cite present but NO .bib found under $PAPER_DIR (depth $DEPTH) — missing bib, or raise --depth"
  else
    echo "-- \\cite check skipped (no .bib and no \\cite in target)"
  fi
else
  bibkeys=$(grep -hoE '@[A-Za-z]+\{[^,]+' "${BIB_FILES[@]}" 2>/dev/null | sed -E 's/@[A-Za-z]+\{//; s/[[:space:]]//g' | sort -u)
  citekeys=$(for f in "${TEX_FILES[@]}"; do strip_comments "$f"; done \
    | grep -oE '\\(cite|citep|citet|citealp|citealt|citeauthor|citeyear|citeyearpar)\*?(\[[^]]*\])?(\[[^]]*\])?\{[^}]+\}' \
    | grep -oE '\{[^}]+\}$' | tr -d '{}' | tr ',' '\n' | sed 's/[[:space:]]//g' | grep -v '^$' | sort -u)
  broken=""
  while IFS= read -r k; do
    [[ -z "$k" ]] && continue
    grep -qxF "$k" <<<"$bibkeys" || broken+="$k"$'\n'
  done <<<"$citekeys"
  broken=$(echo "$broken" | grep -v '^$' || true)
  if [[ -z "$broken" ]]; then
    echo "✅ all \\cite keys resolve in .bib ($(grep -c . <<<"$citekeys") cited, ${#BIB_FILES[@]} .bib)"
  else
    echo "❌ broken \\cite keys (not in any .bib):"; echo "$broken" | sed 's/^/    /'; FAIL=1
  fi
fi

# ── META: broken \ref (no matching \label) ───────────────────────────────────
labels=$(for f in "${TEX_FILES[@]}"; do strip_comments "$f"; done \
  | grep -oE '\\label\{[^}]+\}' | sed -E 's/\\label\{//; s/\}//' | sort -u)
refs=$(for f in "${TEX_FILES[@]}"; do strip_comments "$f"; done \
  | grep -oE '\\(ref|autoref|cref|Cref|eqref|nameref)\*?\{[^}]+\}' \
  | grep -oE '\{[^}]+\}$' | tr -d '{}' | sort -u)
if [[ -z "$refs" ]]; then
  echo "-- \\ref check skipped (no \\ref in target)"
else
  brokenref=""
  while IFS= read -r r; do
    [[ -z "$r" ]] && continue
    grep -qxF "$r" <<<"$labels" || brokenref+="$r"$'\n'
  done <<<"$refs"
  brokenref=$(echo "$brokenref" | grep -v '^$' || true)
  if [[ -z "$brokenref" ]]; then
    echo "✅ all \\ref resolve to a \\label"
  else
    echo "❌ broken \\ref (no matching \\label):"; echo "$brokenref" | sed 's/^/    /'; FAIL=1
  fi
fi

# ── META: orphan \label (defined but never \ref-ed — informational) ──────────
if [[ -n "$labels" ]]; then
  orphan=""
  while IFS= read -r lab; do
    [[ -z "$lab" ]] && continue
    grep -qxF "$lab" <<<"$refs" || orphan+="$lab"$'\n'
  done <<<"$labels"
  orphan=$(echo "$orphan" | grep -v '^$' || true)
  if [[ -z "$orphan" ]]; then
    echo "✅ no orphan \\label (all are \\ref-ed)"
  else
    echo "⚠️ orphan \\label (defined, never \\ref-ed — remove or wire up):"; echo "$orphan" | sed 's/^/    /'
  fi
fi

# ── REVISE: Pn.Sn markers present & sequential (per-file) ────────────────────
for f in "${TEX_FILES[@]}"; do
  markers=$(grep -oE '%% ---- P[0-9]+\.S[0-9]+ ----' "$f" 2>/dev/null | grep -oE 'P[0-9]+\.S[0-9]+')
  [[ -z "$markers" ]] && continue
  n=$(echo "$markers" | grep -c .)
  # per paragraph Pk, sentence numbers must run 1,2,3… with no gap/dupe
  bad=$(echo "$markers" | awk -F'[PS.]' '
    { p=$2+0; s=$4+0;
      if (p!=curp) { curp=p; expect=1 }
      if (s!=expect) { out=out sprintf("P%d.S%d(want S%d) ", p, s, expect) }
      expect=s+1 }
    END { if (out) print out }')
  if [[ -z "$bad" ]]; then
    echo "✅ $(basename "$f"): $n Pn.Sn markers, sequential"
  else
    echo "⚠️ $(basename "$f"): Pn.Sn out of sequence: $bad"
  fi
done

# ── REVISE: proof-carrying dispatch (--log) ──────────────────────────────────
#    Newest-first _LOG: the FIRST `## … [REVISE]` heading is the latest run.
#    Its block (up to the next `## ` heading) must carry a `workers:` line —
#    proof the 2-revise workers were dispatched, not hand-edited inline.
for lf in ${LOG_FILES[@]+"${LOG_FILES[@]}"}; do
  if [[ ! -f "$lf" ]]; then
    echo "⚠️ --log file not found: $lf"; continue
  fi
  revise_block=$(awk '/^## .*\[REVISE\]/{grab=1; next} grab && /^## /{exit} grab{print}' "$lf")
  if ! grep -q '\[REVISE\]' "$lf"; then
    echo "-- REVISE proof skipped ($(basename "$lf"): no [REVISE] entry yet)"
  elif echo "$revise_block" | grep -q 'workers:'; then
    echo "✅ $(basename "$lf"): newest [REVISE] carries its workers: line"
  else
    echo "❌ $(basename "$lf"): newest [REVISE] entry has NO workers: line (revise workers not dispatched?)"; FAIL=1
  fi
  if grep -q '\[REVISE\]' "$lf" && ! grep -q '\[GATE\] draft-review' "$lf"; then
    echo "⚠️ $(basename "$lf"): [REVISE] present but no [GATE] draft-review on record (draft gate skipped?)"
  fi
done

# ── META: compile clean (opt-in; --compile) ──────────────────────────────────
if [[ $COMPILE -eq 1 ]]; then
  if [[ -f "$PAPER_DIR/1-compile.sh" ]]; then
    clog=$(cd "$PAPER_DIR" && bash 1-compile.sh 2>&1)
    cerr=$(echo "$clog" | grep -iE '^!|LaTeX Error|Undefined control sequence|Emergency stop' | head -20)
    if [[ -z "$cerr" ]]; then
      echo "✅ compiles clean (1-compile.sh)"
    else
      echo "❌ compile errors:"; echo "$cerr" | sed 's/^/    /'; FAIL=1
    fi
  else
    echo "⚠️ --compile requested but no 1-compile.sh in $PAPER_DIR"
  fi
else
  echo "-- compile check skipped (pass --compile to run ./1-compile.sh)"
fi

echo "─────────────────────────────────────────────"
if [[ $FAIL -eq 0 ]]; then
  echo "MECHANICAL: no ❌ FAIL items (⚠️ warnings may remain — confirm in-file)"
else
  echo "MECHANICAL: ❌ FAIL items present — see above"
fi
exit $FAIL
