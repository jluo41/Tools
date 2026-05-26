#!/bin/bash
# make-diff.sh — build a tracked-changes PDF against a baseline commit.
#
# Class-aware: auto-detects \documentclass and picks appropriate latexdiff
# flags (informs / acmart / IEEEtran / llncs / NeurIPS / ICML / generic).
#
# Walks UP from the current directory to find the paper root (the directory
# that contains the master .tex file and 1-diff/). Working tree is NEVER
# modified.
#
# Usage (from anywhere inside the paper repo):
#   make-diff.sh <baseline-commit-or-tag> [<tag-name>] [<main-tex>]
#
# Examples:
#   make-diff.sh a362838 v0503
#   make-diff.sh c982fb4 v0429
#   make-diff.sh b5491ac paper-revise 0-MainPaper.tex
#
# Output:  <paper-root>/1-diff/vs-<tag>-<sha>/
#   ├── <main>-DIFF.pdf                    tracked-changes PDF (commit this)
#   ├── <main>-DIFF.tex                    latexdiff source (commit this)
#   ├── silenced-changes.txt               (optional) noise filter rules
#   ├── config.sh                          (optional) per-diff overrides
#   ├── old/                               baseline snapshot (gitignored)
#   ├── new/                               current snapshot (gitignored)
#   └── 0-display → new/0-display          symlink so figures resolve

set -e

# ─── Locate the script and paper root ─────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

find_paper_root() {
    # Walk up from $PWD looking for a directory that has BOTH:
    #   - at least one 0-*.tex master file at its root, AND
    #   - a 1-diff/ directory (or, if missing, somewhere we can create one)
    # Falls back to nearest ancestor with a 0-*.tex master.
    local dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        if compgen -G "$dir/0-*.tex" > /dev/null 2>&1; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

PAPER_DIR="$(find_paper_root)" || {
    echo "Error: cannot find a paper root (no 0-*.tex master found in any ancestor of $(pwd))" >&2
    exit 1
}

# ─── Parse arguments ──────────────────────────────────────────────────────
if [ $# -lt 1 ]; then
    cat >&2 <<EOF
Usage: $0 <baseline-commit-or-tag> [<tag-name>] [<main-tex>]
Examples:
  $0 a362838 v0503                                  # auto-detect master tex
  $0 c982fb4 v0429
  $0 b5491ac paper-revise 0-MainPaper.tex           # explicit master
EOF
    exit 1
fi

BASELINE="$1"
TAG="${2:-}"
MAIN_TEX_OVERRIDE="${3:-}"

# Resolve to short SHA (works for tags, branch names, and commit hashes)
SHA=$(cd "$PAPER_DIR" && git rev-parse --short "$BASELINE" 2>/dev/null) || {
    echo "Error: cannot resolve '$BASELINE' to a git commit (not in repo? bad ref?)" >&2
    exit 1
}

# Build subdir name
if [ -n "$TAG" ]; then
    SUBDIR="vs-${TAG}-${SHA}"
else
    SUBDIR="vs-${SHA}"
fi

DIFF_DIR="$PAPER_DIR/1-diff"
WORK_DIR="$DIFF_DIR/$SUBDIR"

# ─── Pick master tex ──────────────────────────────────────────────────────
if [ -n "$MAIN_TEX_OVERRIDE" ]; then
    MAIN_TEX="$MAIN_TEX_OVERRIDE"
else
    # Heuristic preference: submission-named master > generic 0-*.tex
    MAIN_TEX=$(cd "$PAPER_DIR" && ls 0-*Submission*.tex 2>/dev/null | head -1)
    if [ -z "$MAIN_TEX" ]; then
        MAIN_TEX=$(cd "$PAPER_DIR" && ls 0-*.tex 2>/dev/null | grep -v -- '-DIFF' | head -1)
    fi
fi

if [ -z "$MAIN_TEX" ] || [ ! -f "$PAPER_DIR/$MAIN_TEX" ]; then
    echo "Error: cannot find master .tex file in $PAPER_DIR (tried: $MAIN_TEX)" >&2
    exit 1
fi

# Verify master exists at baseline; fall back to any 0-*.tex that does
if ! (cd "$PAPER_DIR" && git cat-file -e "$SHA:$MAIN_TEX" 2>/dev/null); then
    FALLBACK=$(cd "$PAPER_DIR" && git ls-tree --name-only "$SHA" 2>/dev/null \
        | grep -E '^0-.*\.tex$' \
        | grep -v -- '-DIFF' \
        | grep -v -- '-Submission-' \
        | head -1)
    if [ -n "$FALLBACK" ]; then
        echo "  note: $MAIN_TEX did not exist at $SHA; falling back to $FALLBACK" >&2
        MAIN_TEX="$FALLBACK"
    else
        echo "Error: $MAIN_TEX did not exist at $SHA, and no 0-*.tex master found in baseline tree" >&2
        exit 1
    fi
fi

DIFF_NAME="${MAIN_TEX%.tex}-DIFF"

# ─── Header banner ────────────────────────────────────────────────────────
cat <<EOF
─── make-diff: $SUBDIR ─────────────────────────────
  baseline:    $BASELINE → $SHA
  paper dir:   $PAPER_DIR
  output dir:  $WORK_DIR
  main tex:    $MAIN_TEX
EOF

mkdir -p "$WORK_DIR/old" "$WORK_DIR/new"

# ─── 1. Extract baseline tree (tolerate missing files) ────────────────────
echo "[1/6] Extracting baseline $SHA into old/ ..."
BASELINE_PATHS=()
for p in 0-sections 0-display "$MAIN_TEX"; do
    if (cd "$PAPER_DIR" && git cat-file -e "$SHA:$p" 2>/dev/null); then
        BASELINE_PATHS+=("$p")
    else
        echo "  note: '$p' not in $SHA — skipping" >&2
    fi
done
for ext in bib cls bst sty; do
    while IFS= read -r f; do
        BASELINE_PATHS+=("$f")
    done < <(cd "$PAPER_DIR" && git ls-tree --name-only "$SHA" 2>/dev/null | grep -E "\.${ext}\$" || true)
done

if [ ${#BASELINE_PATHS[@]} -eq 0 ]; then
    echo "Error: no files to extract from baseline $SHA" >&2
    exit 1
fi

(cd "$PAPER_DIR" && git archive "$SHA" -- "${BASELINE_PATHS[@]}" | tar -x -C "$WORK_DIR/old/")

# Borrow current versions of class/style/logo files missing at baseline
for ext_pattern in '*.cls' '*.bst' '*.sty'; do
    for f in "$PAPER_DIR"/$ext_pattern; do
        [ -f "$f" ] || continue
        bn=$(basename "$f")
        [ -f "$WORK_DIR/old/$bn" ] || cp "$f" "$WORK_DIR/old/$bn"
    done
done

# ─── 2. Copy current working tree ─────────────────────────────────────────
echo "[2/6] Copying current working tree into new/ ..."
(cd "$PAPER_DIR" && cp -r 0-sections 0-display "$MAIN_TEX" *.bib *.cls *.bst *.sty "$WORK_DIR/new/" 2>/dev/null || true)

# ─── 3. Detect class & load config (with optional override) ───────────────
echo "[3/6] Detecting paper class & loading config ..."
eval "$(bash "$SCRIPT_DIR/detect-paper-class.sh" "$WORK_DIR/new/$MAIN_TEX")"

# Allow per-diff override file
if [ -f "$WORK_DIR/config.sh" ]; then
    echo "  loading user override: $WORK_DIR/config.sh" >&2
    # shellcheck disable=SC1090
    source "$WORK_DIR/config.sh"
fi

# Default markup style
LATEXDIFF_TYPE="${LATEXDIFF_TYPE:-UNDERLINE}"

# ─── 4. Run latexdiff ─────────────────────────────────────────────────────
echo "[4/6] Running latexdiff --flatten (--type=$LATEXDIFF_TYPE) ..."
(cd "$WORK_DIR" && latexdiff --flatten --type="$LATEXDIFF_TYPE" \
    --exclude-textcmd="$LATEXDIFF_EXCLUDE_TEXTCMD" \
    --append-textcmd="$LATEXDIFF_APPEND_TEXTCMD" \
    --append-context2cmd="$LATEXDIFF_APPEND_CONTEXT2CMD" \
    "old/$MAIN_TEX" "new/$MAIN_TEX" \
    > "$DIFF_NAME.tex" 2>/dev/null)

# Bootstrap silenced-changes.txt with class-detected protect-block: lines
if [ ! -f "$WORK_DIR/silenced-changes.txt" ]; then
    {
        echo "# Silenced numerical changes for this diff"
        echo "# Format: OLD<TAB>NEW   (tab-separated; lines starting with # are ignored)"
        echo "#"
        echo "# protect-block: <COMMAND>  — never silence inside \\<COMMAND>{...}"
        for blk in $(echo "$PROTECTED_BLOCKS" | tr ',' ' '); do
            echo "protect-block: $blk"
        done
        echo ""
        echo "# Add (old, new) pairs below, one per line, tab-separated."
        echo "# Example:"
        echo "#  6.7${TAB:-	}6.5"
    } > "$WORK_DIR/silenced-changes.txt"
fi

# Apply silencer
echo "[4b] Applying silenced-changes.txt ..."
cp "$WORK_DIR/$DIFF_NAME.tex" "$WORK_DIR/$DIFF_NAME.tex.bak"
perl "$SCRIPT_DIR/silence-minor-changes.pl" \
    "$WORK_DIR/silenced-changes.txt" \
    "$WORK_DIR/$DIFF_NAME.tex.bak" \
    > "$WORK_DIR/$DIFF_NAME.tex" \
    2> >(sed 's/^/    /' >&2)
rm -f "$WORK_DIR/$DIFF_NAME.tex.bak"

# Run post-flatten hook (defined optionally in config.sh)
if declare -F POST_FLATTEN_HOOK >/dev/null; then
    echo "[4c] Running POST_FLATTEN_HOOK from config.sh ..."
    POST_FLATTEN_HOOK "$WORK_DIR/$DIFF_NAME.tex"
fi

# ─── 5. Stage support files + figure symlink ──────────────────────────────
echo "[5/6] Staging support files + figure symlink ..."
(cd "$WORK_DIR" && cp new/*.bib new/*.cls new/*.bst new/*.sty . 2>/dev/null || true)
# Replace any existing 0-display symlink/dir
(cd "$WORK_DIR" && rm -rf 0-display 2>/dev/null; ln -sfn new/0-display 0-display)

# ─── 6. Compile ───────────────────────────────────────────────────────────
echo "[6/6] Compiling diff PDF (4-pass with bibtex) ..."
COMPILER="${COMPILER_HINT:-pdflatex}"
(cd "$WORK_DIR" && \
    "$COMPILER" -interaction=nonstopmode "$DIFF_NAME.tex" > .p1.log 2>&1 || true; \
    bibtex "$DIFF_NAME" > .b.log 2>&1 || true; \
    "$COMPILER" -interaction=nonstopmode "$DIFF_NAME.tex" > .p2.log 2>&1 || true; \
    "$COMPILER" -interaction=nonstopmode "$DIFF_NAME.tex" > .p3.log 2>&1 || true)

# Cleanup intermediates and staged support files
(cd "$WORK_DIR" && rm -f .p*.log .b.log *.aux *.bbl *.blg *.log *.ent *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz)
(cd "$WORK_DIR" && rm -f *.bib *.cls *.bst *.sty)

# ─── Report ───────────────────────────────────────────────────────────────
if [ -f "$WORK_DIR/$DIFF_NAME.pdf" ]; then
    PDF_SIZE=$(ls -lh "$WORK_DIR/$DIFF_NAME.pdf" | awk '{print $5}')
    PDF_PAGES=$(pdfinfo "$WORK_DIR/$DIFF_NAME.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}')
    echo
    echo "✓ Done: $WORK_DIR/$DIFF_NAME.pdf ($PDF_SIZE, $PDF_PAGES pages)"
else
    echo "✗ PDF not generated — inspect $WORK_DIR/.p3.log (run with --keep to retain)"
    exit 1
fi
