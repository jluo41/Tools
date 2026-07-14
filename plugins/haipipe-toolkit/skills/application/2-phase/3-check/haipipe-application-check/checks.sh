#!/usr/bin/env bash
# checks.sh — deterministic MECHANICAL sub-checks for haipipe-application-check.
# ============================================================================
# MARKDOWN-SAFE subset of paper's checks.sh (paper/2-phase/3-check/
# haipipe-paper-check/checks.sh @ 1.7.0). Application artifacts and stage docs
# are markdown, not tex, so ONLY the text-tier checks port:
#   em-dash            ❌  house rule, same tier as TODO (paper 1.7.0 ruling)
#   AI-voice tells     ⚠️  high-signal list, false-positive room stays a warning
#   TODO/FIXME         ❌  planted flags MUST block the gate until resolved
#   bibtex-in-markdown ❌  bibtex lives ONLY in .bib; an application has no .bib
#
# Deliberately NOT ported from paper's checks.sh (tex-only machinery):
#   broken \cite, broken \ref, orphan \label, Pn.Sn sequence, --compile.
#
# Emits one ✅ / ⚠️ / ❌ line per check so the agent can paste results straight
# into the CHECK report and seed > CHECK: comments in STAGE DOCS at the
# reported file:line. 0-artifacts/*.md findings are NEVER seeded in-file (the
# artifact IS the deliverable text) — they go to the Gate Ledger notes column.
#
# Usage:
#   checks.sh <artifact-or-intervention-dir> [--md <file> ...] [--depth N]
#
#   <artifact-or-intervention-dir>  a single .md (artifact or stage doc), OR an
#                                   intervention dir (all *.md under it scanned)
#   --md <file>   an extra markdown working doc to add to the scan set (same
#                 checks); repeatable — use for docs outside the target tree
#   --depth N     find maxdepth for *.md when target is a dir (default 3:
#                 reaches 0-lifecycle/<stage>/0-<stage>.md AND 0-artifacts/*.md
#                 from the intervention root). 1-probes/ probe files (and legacy
#                 _PROBE/ cards) are excluded at any depth — they belong to
#                 check-probe-cards.sh; _LOG* and _archive/ / _external/ trees
#                 are excluded so archived threads quoting old findings don't re-flag.
#
# Exit code: 0 if no ❌ (FAIL) items, 1 if any ❌. ⚠️ never fails the run.
# ❌ tier: em-dash, TODO/FIXME, bibtex-in-md.   ⚠️ tier: AI-voice.
#
# Markdown adaptations vs paper (paper strips % tex comments; md has none):
# - structural dash lines (setext ===/--- underlines, table |---| separator
#   rows, frontmatter fences, horizontal rules) are skipped by the em-dash
#   check — only PROSE lines containing --- or — flag;
# - comment-family lines (> CHECK: / > USER: / > CC: / > REVIEWER:) are
#   skipped by the em-dash and AI-voice checks so a seeded comment quoting a
#   finding doesn't re-flag on the next run; TODO scanning deliberately keeps
#   them (paper precedent: planted TODO flags must block until resolved).
#
# Portability: the awk greps are mawk-safe per paper 1.7.0 — tolower() plus
# explicit non-letter boundary classes, no gawk-only \< \> or IGNORECASE —
# and verified under macOS /usr/bin/awk (BWK awk 20200816). Bash-3.2-safe:
# no mapfile, guarded empty-array expansion.
# ============================================================================
set -uo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "usage: checks.sh <artifact-or-intervention-dir> [--md <file> ...] [--depth N]" >&2
  exit 2
fi
shift || true

MD_FILES=()
DEPTH=3
while [[ $# -gt 0 ]]; do
  case "$1" in
    --md) shift; if [[ -z "${1:-}" || "${1:-}" == --* ]]; then echo "--md needs a file argument" >&2; exit 2; fi; MD_FILES+=("$1") ;;
    --depth) shift; DEPTH="${1:-3}"
             if ! [[ "$DEPTH" =~ ^[0-9]+$ ]]; then echo "--depth needs a numeric argument, got: $DEPTH" >&2; exit 2; fi ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift || true
done

# Resolve the markdown scan set.
SCAN_FILES=()
if [[ -f "$TARGET" ]]; then
  SCAN_FILES=("$TARGET")
elif [[ -d "$TARGET" ]]; then
  while IFS= read -r f; do SCAN_FILES+=("$f"); done < <(find "$TARGET" -maxdepth "$DEPTH" -name '*.md' -not -path '*/_archive/*' -not -path '*/_external/*' -not -path '*/1-probes/*' -not -path '*/1-probe-plans/*' -not -path '*/_PROBE/*' -not -name '_LOG*' | sort)
else
  echo "not a file or dir: $TARGET" >&2
  exit 2
fi
for f in ${MD_FILES[@]+"${MD_FILES[@]}"}; do
  [[ -f "$f" ]] && SCAN_FILES+=("$f") || echo "⚠️ --md file not found (skipped): $f"
done
if [[ ${#SCAN_FILES[@]} -eq 0 ]]; then
  echo "no .md files found under $TARGET (depth $DEPTH) — raise --depth or check the path" >&2
  exit 2
fi

FAIL=0

echo "# checks.sh — MECHANICAL sub-checks (application, markdown-safe subset)"
echo "# target: $TARGET   md files scanned: ${#SCAN_FILES[@]}"
echo "─────────────────────────────────────────────"

# ── REVISE: em-dashes ────────────────────────────────────────────────────────
#    ❌ FAIL, not ⚠️: the house rule is absolute, same tier as TODO markers
#    (paper 1.7.0, JL 2026-07-07: "统一提议"). Structural dash lines (setext
#    underlines, |---| table rows, frontmatter fences) and comment-family
#    lines are skipped — only prose --- / — flags.
emdash=$(for f in "${SCAN_FILES[@]}"; do
  awk -v F="$f" '
    /^[[:space:]]*[-=|+:[:space:]]*$/ { next }
    /^[[:space:]]*>[[:space:]]*(CHECK|USER|CC|REVIEWER):/ { next }
    { if ($0 ~ /---/ || $0 ~ /—/) printf "%s:%d:%s\n", F, NR, $0 }
  ' "$f" 2>/dev/null
done)
if [[ -z "$emdash" ]]; then
  echo "✅ no em-dashes"
else
  echo "❌ em-dashes found (recast as commas/colons/parens):"; echo "$emdash" | sed 's/^/    /'; FAIL=1
fi

# ── REVISE: AI-voice tells (high-signal only; noisy connectives like
#    Furthermore/Moreover/Additionally intentionally EXCLUDED — same list as
#    paper 1.7.0, where they drowned the real tells on live papers)
AI_TELLS='delve|tapestry|realm|seamless|showcase|intricate|nuanced|utilize|underscore|leverage'
# portable (mawk-safe): lowercase + explicit non-letter boundaries, no gawk \< \> / IGNORECASE
aivoice=$(for f in "${SCAN_FILES[@]}"; do
  awk -v F="$f" -v P="$AI_TELLS" '
    /^[[:space:]]*>[[:space:]]*(CHECK|USER|CC|REVIEWER):/ { next }
    { if (tolower($0) ~ ("(^|[^a-z])(" P ")([^a-z]|$)")) printf "%s:%d:%s\n", F, NR, $0 }
  ' "$f" 2>/dev/null
done)
if [[ -z "$aivoice" ]]; then
  echo "✅ no AI-voice tells"
else
  echo "⚠️ AI-voice tells (confirm each — some may be legitimate):"; echo "$aivoice" | sed 's/^/    /'
fi

# ── META: TODO markers ───────────────────────────────────────────────────────
#    Comment-family lines deliberately NOT skipped (paper precedent): planted
#    TODO flags MUST block the gate until resolved, wherever they live.
#    XXX deliberately EXCLUDED (paper 1.7.0: collides with anonymization
#    placeholders; kept out here for one shared tell-list across families).
todos=$(for f in "${SCAN_FILES[@]}"; do grep -nHE '\b(TODO|FIXME)\b' "$f" 2>/dev/null; done)
if [[ -z "$todos" ]]; then
  echo "✅ no TODO/FIXME markers"
else
  echo "❌ TODO markers remain:"; echo "$todos" | sed 's/^/    /'; FAIL=1
fi

# ── PROBE: no bibtex in markdown ─────────────────────────────────────────────
#    Any entry type via the @word{key, shape (paper 1.7.0 D4) so venue names
#    with bare @ (e.g. "KHD@IJCAI workshop") don't false-hit. An application
#    has no .bib at all, so ANY bibtex block in markdown is a leak.
bibleak=$(for f in "${SCAN_FILES[@]}"; do grep -nHE '^[[:space:]]*@[A-Za-z]+\{[^,}]+,' "$f" 2>/dev/null; done)
if [[ -z "$bibleak" ]]; then
  echo "✅ no bibtex in markdown (bibtex lives ONLY in .bib)"
else
  echo "❌ bibtex leaked into markdown (move to the paper family's .bib — applications cite ledger-backed claims, not bibtex):"; echo "$bibleak" | sed 's/^/    /'; FAIL=1
fi

echo "─────────────────────────────────────────────"
if [[ $FAIL -eq 0 ]]; then
  echo "MECHANICAL: no ❌ FAIL items (⚠️ warnings may remain — confirm in-file)"
else
  echo "MECHANICAL: ❌ FAIL items present — see above"
fi
exit $FAIL
