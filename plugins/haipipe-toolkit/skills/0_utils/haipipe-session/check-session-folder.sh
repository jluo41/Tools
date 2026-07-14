#!/bin/sh
# check-session-folder.sh -- deterministic verifier for a SESSION TOPIC FOLDER.
#
# THE UNIT RULE (LAW 1). ONE FOLDER PER TOPIC, NOT PER SESSION.
#   A folder is diagram/<YYMMDD>-<topic>/ -- dated at BIRTH, never re-dated. A later
#   session APPENDS to it (a new ruling in the ledger, a `>> CC{MMDD}:` reply, a status
#   flip); it opens a NEW folder only for a NEW TOPIC. The rulings ledger is APPEND-ONLY,
#   and one-folder-per-session would split it across dates -- killing the one property the
#   whole design exists for: ONE grep finds every ruling this topic ever made.
#   The session is the INPUT; the topic folder is the OUTPUT.
#
# Usage: sh check-session-folder.sh <diagram/YYMMDD-topic-folder>
# Exit 0 = clean (WARNs allowed). Exit 1 = any FAIL. RUN this, never eyeball it.
#
# POSIX sh (dash), on purpose. The first cut of this file was bash + a python3 heredoc: it
# died on `set -o pipefail` under `sh` -- exit 2 on BOTH live folders, i.e. under its own
# documented invocation it never checked anything at all. Structure follows the house
# checker, check-probe-cards.sh: arg parse, problem accumulation, `FAIL <name> --<problems>`.
#
# THE SPEC OF RECORD IS THE TWO LIVE FOLDERS, NOT THIS FILE'S OPINION:
#   Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/         (5 files)
#   Tools/plugins/haipipe-toolkit/diagram/260714-resource-stage/   (6 files)
# Every threshold below was MEASURED against those files before it was written. A gate that
# FAILs correct work gets MUTED, and it takes its real detections down with it -- so where
# the folders and a tidy rule disagree, the checker follows the DISK, and says so at the rule.
#
# WHAT IT CHECKS -- three passes.
#
# PASS 0: THE FOLDER
#   1. MAX 6 .txt files      FAIL. The cap IS the point: a 7th file means a THEME needs
#                            merging, not a new page.
#   2. NO INDEX FILE         FAIL. 00-index.txt / index / README are FORBIDDEN. An index is
#                            a second place to keep the truth, and it rots first.
#   3. .md in the folder     WARN (markdown breaks monospace alignment; the house form is .txt).
#   4. NN-<slug>.txt naming  WARN, plus a WARN on a gap in the 01..NN run.
#   5. <YYMMDD>-<topic>      WARN (LAW 1: dated at BIRTH).
#
# PASS 1: EACH FILE
#   6. LENGTH -- TWO TIERS, AND THE TWO TIERS ARE NOT SLOP.
#      The house rule is "max ~250 lines" -- JL wrote the `~`, and it is load-bearing:
#      260714-probe-qa/05-status-and-open-items.txt is 252 lines ON DISK, in a folder that
#      is BY DEFINITION correct (it is half the spec). A hard FAIL at 251 would red a
#      CORRECT folder on its very first run, and a gate that cries wolf on day one is muted
#      by day two -- taking the dangling-ref detections, the ones that actually bite, down
#      with it. So: >SOFT = WARN (the theme is getting heavy; watch it). >HARD = FAIL (the
#      file is carrying TWO themes, which is the defect the cap exists to catch -- and a
#      two-theme file does not land at 252, it lands at 350).
#   7. NO MARKDOWN TABLE     FAIL (JL house rule): sections + bullets + ASCII boxes only.
#                            A table is caught by its SEPARATOR ROW (`|---|---|`) anywhere,
#                            and by any `| ... |` line in PROSE. Inside a fence a pipe is
#                            ASCII box art -- a blessed style -- and is left alone.
#   8. TITLE UNDERLINE       FAIL. Line 2 is `=` repeated to the width of line 1 --
#                            MEASURED IN CODEPOINTS, WITH A ONE-COLUMN TOLERANCE, AND THAT
#                            TOLERANCE IS ALSO ON DISK. The two live folders disagree about
#                            the em-dash: resource-stage counts it as 1 column (6/6 files:
#                            diff = 0), probe-qa counts it as 2 (5/5 files: diff = +1). Both
#                            LOOK aligned in a terminal. Demanding exact equality would FAIL
#                            5 of the 11 files that ARE the spec. `0 <= u - t <= 1` holds on
#                            all 11 with zero exceptions, and still catches the real bug --
#                            a heading retitled without retyping its underline -- instantly.
#   9. HOUSE FORM            WARN: section-underline drift (outside fences), a tab, trailing
#                            whitespace, a fence opener that is not ```text, a markdown ATX
#                            heading. All measured clean on the 11 live files. WARN and not
#                            FAIL deliberately: emoji and circled numerals make display width
#                            genuinely ambiguous (the live 05 carries -1 and +2 diffs on emoji
#                            headings), and no gate should go red over one codepoint.
#
# PASS 2: THE REFERENCES -- the killer bug, and the reason this file exists.
#  10. LOCAL REF        `06-shipped-owed.txt` cited in prose must EXIST in this folder. A
#                       file merged away (08-open-questions.txt) leaves live citations
#                       behind it and NOTHING on disk complains. FAIL dangling-local-ref.
#  11. CROSS-FOLDER REF TWO DESIGN FOLDERS CITE EACH OTHER AND ARE EDITED IN PARALLEL
#                       SESSIONS. One restructures; the other's citations rot in silence.
#                       Both live citation forms resolve here:
#                           `probe-qa 02-the-files.txt`      (date-STRIPPED slug + file)
#                           `diagram/260714-probe-qa/...`    (full dated path)
#                       against the REAL sibling folder on disk. FAIL dangling-cross-ref.
#                       RESOLVED BY SLUG, NOT BY LITERAL NAME: probe-qa's own 05 cites
#                       `diagram/probe-qa/` (undated -- it is proposing that very rename).
#                       A literal-path checker calls that dangling and FAILs a CORRECT
#                       folder. The date is stripped from every sibling before matching, so
#                       the dated and the undated citation both resolve.
#
# A REF INSIDE A FENCED BLOCK IS STILL A REF. The diagrams cite files constantly
# (`|-- see 05-rulings.txt (C9)`), and a rotted citation inside a diagram misleads exactly
# as hard as one in prose. Scanning fences is deliberate, and it costs nothing on the 11
# live files: every ref in them resolves.
#
# SCAFFOLD MODE, AND THE VACUOUS GREEN IT NEARLY SHIPPED. A folder fresh from ref/skeleton/
# is not a topic note yet: its citations cannot resolve, and reporting them as rot would
# drown the author. So PASS 2 is skipped for a skeleton -- but the DETECTOR MUST BE LITERAL.
# The first cut detected a scaffold by ANY angle-bracket token (`<[A-Za-z]...>`), and the
# real notes are FULL of them (`QA/<n>-<slug>.md`, `<YYMMDD>-<topic>`: 12 x `<n>` alone).
# Result: BOTH LIVE FOLDERS were classified as unfilled skeletons, PASS 2 never ran, and the
# checker exited 0 having verified NOTHING -- a green light with the lamp unplugged, which is
# strictly worse than a red one. The marker is now the literal authoring text the skeleton
# carries and a real note never does: RENAME THIS FILE / SKELETON. / PLACEHOLDER (verified:
# 0 hits across the 11 live files, 3 hits across the 6 skeleton files).

set -u

folder=""
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) echo "usage: check-session-folder.sh <diagram/YYMMDD-topic-folder>"; exit 0 ;;
    *) if [ -z "$folder" ]; then folder=$1
       else echo "FAIL  unexpected arg: $1"; exit 1; fi ;;
  esac
  shift
done
[ -n "$folder" ] || { echo "usage: check-session-folder.sh <diagram/YYMMDD-topic-folder>"; exit 1; }

# GUARD THE cd (same reason as check-probe-cards.sh): an unchecked cd into a missing dir
# leaves the path EMPTY, and every check below then passes vacuously over nothing.
root=$(cd "$folder" 2>/dev/null && pwd) || root=""
[ -n "$root" ] || { echo "FAIL  no such folder: $folder"; exit 1; }
parent=$(dirname "$root")
self=$(basename "$root")

US=$(printf '\037')
MAX_FILES=6
SOFT_LINES=250      # the house "~250": over this is a WARN -- the theme is getting heavy.
HARD_LINES=300      # over this the file is carrying TWO themes. That is the defect. FAIL.

fail=0
tmp="/tmp/.session_refs.$$"
trap 'rm -f "$tmp"' EXIT HUP INT TERM

# ---------------------------------------------------------------------------
# cplen -- length in CODEPOINTS, locale-independent.
#
# `awk length()` is BYTES here (mawk), so a 41-char em-dash title measures 43 and EVERY
# heading in both live folders reports a mismatch -- the check would be muted within a day.
# Counting the bytes that are NOT UTF-8 continuation bytes (0x80-0xBF) is the exact
# codepoint count for valid UTF-8, and needs no locale to be set.
# ---------------------------------------------------------------------------
cplen() {
  printf '%s' "$1" | LC_ALL=C tr -d '\200-\277' | LC_ALL=C wc -c | tr -d ' '
}

# The em-dash tolerance, in ONE place. Both live dialects pass; a real mismatch does not.
underline_ok() {  # $1 = title text, $2 = underline text
  _ut=$(cplen "$1"); _uu=$(cplen "$2")
  [ "$_uu" -ge "$_ut" ] && [ "$_uu" -le $((_ut + 1)) ]
}

# ---------------------------------------------------------------------------
# resolve_folder -- a sibling citation key -> a real folder on disk, or nothing.
# Accepts the literal dated name (`260714-probe-qa`) AND the date-stripped slug
# (`probe-qa`), because BOTH forms are live in the two folders that are the spec.
# ---------------------------------------------------------------------------
resolve_folder() {
  _k=$1
  [ -n "$_k" ] || return 1
  if [ -d "$parent/$_k" ]; then printf '%s' "$parent/$_k"; return 0; fi
  for _d in "$parent"/*/; do
    [ -d "$_d" ] || continue
    _n=$(basename "$_d")
    _s=$(printf '%s' "$_n" | sed 's/^[0-9][0-9][0-9][0-9][0-9][0-9]-//')
    if [ "$_s" = "$_k" ]; then printf '%s' "$parent/$_n"; return 0; fi
  done
  return 1
}

# ===========================================================================
# PASS 0 -- THE FOLDER
# ===========================================================================
fprob=""

case "$self" in
  [0-9][0-9][0-9][0-9][0-9][0-9]-*) : ;;
  *) echo "WARN  $self/  -- folder name is not <YYMMDD>-<topic> (LAW 1: dated at BIRTH, never re-dated)" ;;
esac

ntxt=0
for f in "$root"/*.txt; do
  [ -e "$f" ] || continue
  ntxt=$((ntxt + 1))
done
[ "$ntxt" -gt "$MAX_FILES" ] && \
  fprob="$fprob too-many-files($ntxt > MAX $MAX_FILES: a 7th file means a THEME needs merging, not a new page);"

for f in "$root"/*; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  # The index is FORBIDDEN: a second place to keep the truth, and it rots first.
  case "$b" in
    00-*|index.txt|index.md|INDEX*|README*|readme*)
      fprob="$fprob index-file($b: FORBIDDEN -- no index, no 00-, no README: the themed files ARE the index);" ;;
  esac
  case "$b" in
    *.md) echo "WARN  $self/$b  -- .md in a .txt folder (markdown breaks monospace alignment)" ;;
  esac
  case "$b" in
    *.txt)
      case "$b" in
        [0-9][0-9]-[a-z0-9]*.txt) : ;;
        *) echo "WARN  $self/$b  -- name is not NN-<slug>.txt" ;;
      esac ;;
  esac
done

# The 01..NN run must be contiguous. A gap means a file was deleted -- and its citations are
# now dangling somewhere, which PASS 2 is about to prove.
i=1
while [ "$i" -le "$ntxt" ]; do
  nn=$(printf '%02d' "$i")
  hit=0
  for f in "$root"/"$nn"-*.txt; do
    [ -e "$f" ] && hit=1
  done
  [ "$hit" -eq 0 ] && echo "WARN  $self/  -- no ${nn}-*.txt (the 01..NN run has a gap)"
  i=$((i + 1))
done

if [ -n "$fprob" ]; then
  echo "FAIL  $self/  --$fprob"
  fail=1
fi

# SCAFFOLD MODE -- an unfilled skeleton is not rot. Detect it once, before PASS 2.
scaffold=0
if [ "$ntxt" -gt 0 ]; then
  if grep -lE 'RENAME THIS FILE|SKELETON\.|PLACEHOLDER' "$root"/*.txt >/dev/null 2>&1; then
    scaffold=1
  fi
fi

# ===========================================================================
# PASS 1 + PASS 2 -- each file
# ===========================================================================
for f in "$root"/*.txt; do
  [ -e "$f" ] || continue
  name=$(basename "$f")
  prob=""

  # -- 6. LENGTH (two tiers; see the header) -------------------------------
  lines=$(wc -l < "$f" | tr -d ' ')
  if [ "$lines" -gt "$HARD_LINES" ]; then
    prob="$prob too-long(${lines} lines > HARD ${HARD_LINES}: this file carries TWO themes -- split the THEME, do not shrink the prose);"
  elif [ "$lines" -gt "$SOFT_LINES" ]; then
    echo "WARN  $name  -- ${lines} lines, over the ~${SOFT_LINES} house cap (the theme is getting heavy)"
  fi

  # -- 7. MARKDOWN TABLE ---------------------------------------------------
  # A TABLE IS ITS SEPARATOR ROW -- AND ASCII BOXES ARE BLESSED, SO THE NAIVE RULE IS WRONG.
  # `^\s*\|.*\|` alone ALSO matches ASCII box art with vertical walls (`| a diagram |`),
  # which is the house's OWN blessed style ("sections + bullets + ASCII boxes"). Failing a
  # correct diagram is how this gate gets muted. So:
  #   outside a fence -> any `| ... |` line is a table (prose has no business drawing boxes);
  #   inside a fence  -> only a genuine markdown SEPARATOR ROW (`|---|---|`: pipes, dashes
  #                      and colons, nothing else) counts. ASCII art never contains one.
  tab=$(awk '
    function is_sep(s) {
      gsub(/[[:space:]]/, "", s)
      if (s !~ /^\|/)      return 0
      if (s !~ /---/)      return 0
      if (s ~ /[^|:-]/)    return 0
      return 1
    }
    /^```/ { fence = !fence; next }
    is_sep($0)                              { n++; next }
    !fence && /^[[:space:]]*\|.*\|/         { n++ }
    END { print n + 0 }
  ' "$f")
  [ "$tab" -gt 0 ] && \
    prob="$prob markdown-table(${tab}-lines: JL house rule -- sections + bullets + ASCII boxes, never a table);"

  # -- 8. TITLE UNDERLINE (line 1 / line 2) --------------------------------
  t1=$(sed -n '1p' "$f")
  t2=$(sed -n '2p' "$f")
  case "$t2" in
    ===*)
      underline_ok "$t1" "$t2" || \
        prob="$prob underline-mismatch(line 2 has $(cplen "$t2") '=' for a $(cplen "$t1")-char title -- retype the underline to the title's width);" ;;
    *)
      prob="$prob no-title-underline(line 2 must be '=' repeated to the width of line 1);" ;;
  esac

  # -- 9. HOUSE FORM (WARN only) -------------------------------------------
  # Array-based so the ATX rule can LOOK AHEAD one line -- see the whitelist below.
  awk -v N="$name" '
    { L[NR] = $0 }
    /^```/ {
      fence = !fence; INF[NR] = 1
      if (fence && $0 != "```text") printf "WARN  %s:%d  -- fence opener \"%s\" (every fenced block is ```text)\n", N, NR, $0
      next
    }
    fence     { INF[NR] = 1 }
    /\t/      { printf "WARN  %s:%d  -- tab character (spaces only)\n", N, NR }
    /[ \t]$/  { printf "WARN  %s:%d  -- trailing whitespace\n", N, NR }
    END {
      if (fence) printf "WARN  %s  -- unbalanced fences\n", N
      for (i = 1; i <= NR; i++) {
        if (INF[i] || L[i] !~ /^#/) continue
        # THE QUOTED-ARTIFACT WHITELIST. `## Demand` / `## Questions` in
        # 260714-resource-stage/02-worked-example.txt are NOT markdown headings: they are the
        # literal SECTION NAMES OF THE ARTIFACT BEING QUOTED (1-resource.md), and each is
        # itself `=`-underlined. Flagging them would fire on a file that IS the spec -- the
        # first step toward a muted gate. An ATX line immediately followed by an `=` underline
        # is a quotation; anything else is a real markdown heading, and gets the WARN.
        nxt = (i < NR) ? L[i+1] : ""
        if (L[i] ~ /^## / && nxt ~ /^===*[[:space:]]*$/) continue
        printf "WARN  %s:%d  -- markdown ATX heading (house form is === / --- underlines)\n", N, i
      }
    }
  ' "$f"

  # Section-underline drift, outside fences. WARN: see the header note on emoji width.
  awk -v SEP="$US" '
    /^```/ { fence = !fence; prev = ""; next }
    fence  { prev = $0; next }
    /^===*[[:space:]]*$/ || /^---*[[:space:]]*$/ {
      if (NR > 2 && prev != "") { u = $0; sub(/[[:space:]]+$/, "", u); print NR SEP prev SEP u }
    }
    { prev = $0 }
  ' "$f" | while IFS="$US" read -r ln title uline; do
    underline_ok "$title" "$uline" || \
      echo "WARN  $name:$ln  -- underline is $(cplen "$uline") for a $(cplen "$title")-char heading"
  done

  # -- 10 + 11. REFERENCES -------------------------------------------------
  # awk finds the two citation shapes; the shell resolves them on disk (awk cannot).
  #   PATH  diagram/<key>/[file]           -- the full-path form (dated name or slug)
  #   FILE  [<word>] NN-<slug>.txt         -- bare (local), or <sibling-slug>-prefixed
  if [ "$scaffold" -eq 0 ]; then
    seen=""
    awk -v SEP="$US" '
      {
        line = $0

        # PATH form: captures the folder key and an OPTIONAL trailing filename.
        t = line
        while (match(t, /diagram\/[0-9A-Za-z][0-9A-Za-z._-]*\/[0-9A-Za-z._-]*/)) {
          tok = substr(t, RSTART, RLENGTH); t = substr(t, RSTART + RLENGTH)
          print "PATH" SEP NR SEP tok SEP ""
        }

        # FILE form: NN-<slug>.txt. A token preceded by "/" already belongs to a PATH ref
        # above; a token glued to a word character is part of a larger identifier.
        r = line
        while (match(r, /[0-9][0-9]-[a-z0-9][a-z0-9-]*\.txt/)) {
          pre = substr(r, 1, RSTART - 1)
          fn  = substr(r, RSTART, RLENGTH)
          r   = substr(r, RSTART + RLENGTH)
          if (pre ~ /[\/A-Za-z0-9._-]$/) continue
          w = pre
          sub(/[ \t]+$/, "", w)
          if (match(w, /[A-Za-z0-9._-]+$/)) w = substr(w, RSTART, RLENGTH); else w = ""
          print "FILE" SEP NR SEP fn SEP w
        }
      }
    ' "$f" > "$tmp"

    while IFS="$US" read -r kind ln ref word; do
      [ -n "${kind:-}" ] || continue
      # One report per distinct citation, however many times the file repeats it.
      case "$seen" in *"${US}${kind}:${ref}:${word}${US}"*) continue ;; esac
      seen="$seen${US}${kind}:${ref}:${word}${US}"

      case "$kind" in
        PATH)
          rest=${ref#diagram/}
          key=${rest%%/*}
          tail=${rest#*/}
          [ "$tail" = "$rest" ] && tail=""
          if tgt=$(resolve_folder "$key"); then
            [ -n "$tail" ] && [ ! -e "$tgt/$tail" ] && \
              prob="$prob dangling-cross-ref(:$ln $ref -- $(basename "$tgt")/ exists, that FILE does not: the sibling was restructured);"
          else
            prob="$prob dangling-cross-ref(:$ln $ref -- no sibling folder resolves '$key' (tried the dated name and the date-stripped slug));"
          fi
          ;;
        FILE)
          tgt=""
          [ -n "$word" ] && { tgt=$(resolve_folder "$word") || tgt=""; }
          if [ -n "$tgt" ]; then
            # A `<sibling-slug> NN-<file>.txt` citation. THE KILLER BUG lives here.
            if [ ! -e "$tgt/$ref" ]; then
              if [ "$(basename "$tgt")" = "$self" ]; then
                prob="$prob dangling-local-ref(:$ln '$word $ref' -- no such file in this folder);"
              else
                prob="$prob dangling-cross-ref(:$ln '$word $ref' -- $(basename "$tgt")/ has no $ref: the sibling was restructured in a parallel session);"
              fi
            fi
          elif [ -e "$root/$ref" ]; then
            :  # a plain local citation, and it resolves.
          else
            case "$word" in
              *-*) prob="$prob dangling-cross-ref(:$ln '$word $ref' -- no sibling folder '$word', and no $ref here);" ;;
              *)   prob="$prob dangling-local-ref(:$ln $ref -- cited, but not in this folder: merged away?);" ;;
            esac
          fi
          ;;
      esac
    done < "$tmp"
    rm -f "$tmp"
  fi

  if [ -n "$prob" ]; then
    echo "FAIL  $name  --$prob"
    fail=1
  else
    echo "PASS  $name  (${lines} lines)"
  fi
done

[ "$scaffold" -eq 1 ] && \
  echo "SCAFFOLD  <PLACEHOLDER> tokens present -- citation checks (PASS 2) SKIPPED. Fill the note in, then re-run."

echo "folder: $root  ($ntxt files · MAX $MAX_FILES · one THEME per file · no index)"
exit $fail
