#!/usr/bin/env bash
# plan.sh — write today's plan .txt, render to .excalidraw, sync to remote.
#
# Usage:
#   plan.sh <one-bet-slug>            < plan-content.txt
#   plan.sh <one-bet-slug> <txt-path>
#   plan.sh --force <one-bet-slug>    < plan-content.txt   (overwrite existing)
#
# Behavior:
#   1. cd ~/Daily
#   2. git pull --rebase --autostash   (no-op if no remote configured)
#   3. write content to ~/Daily/<today>/<YYMMDD>-plan.txt   (refuses if exists, unless --force)
#   4. render to ~/Daily/<today>/<YYMMDD>-plan.excalidraw via txt-to-canvas.py
#   5. git add + commit + push (retry once on rejection)
#
# Skips push silently if no `origin` remote is set.

set -euo pipefail

DAILY_ROOT="${DAILY_ROOT:-$HOME/Daily}"
CANVAS_TOOL="${CANVAS_TOOL:-$(cd "$(dirname "$0")"/../.. && pwd)/../diagram-skill/skills/diagram-ascii-canvas/bin/txt-to-canvas.py}"

usage() {
    echo "Usage: $0 [--force] <one-bet-slug> [content-file]    (or pipe via stdin)" >&2
    exit 2
}

FORCE=0
if [ "${1:-}" = "--force" ]; then
    FORCE=1
    shift
fi

[ $# -ge 1 ] || usage
SLUG="$1"
CONTENT_SRC="${2:-/dev/stdin}"

# Validate slug: lowercase letters, digits, hyphens, 2-6 words.
if ! [[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+){1,5}$ ]]; then
    echo "✗ slug must be 2-6 hyphenated lowercase tokens, got: $SLUG" >&2
    exit 2
fi

if [ ! -d "$DAILY_ROOT/.git" ]; then
    cat >&2 <<EOF
✗ $DAILY_ROOT is not a git repo.

Bootstrap chronicle first:
    Tools/plugins/chronicle/bin/setup.sh git@github.com:<you>/Daily.git
or:
    Tools/plugins/chronicle/bin/setup.sh init      (local-only)
EOF
    exit 1
fi

cd "$DAILY_ROOT"

# 1. Pull first if remote configured.
if git remote get-url origin >/dev/null 2>&1; then
    echo "→ pulling from origin..."
    git pull --rebase --autostash 2>&1 | sed 's/^/   /' || {
        echo "✗ git pull failed; resolve manually then retry" >&2
        exit 1
    }
else
    echo "⚠ no 'origin' remote configured; skipping pull/push (local-only mode)"
fi

# 2. Resolve target date = today (plans are always for today).
TARGET_DATE=$(date +%Y-%m-%d)
YYMMDD=$(date -j -f %Y-%m-%d "$TARGET_DATE" +%y%m%d 2>/dev/null \
         || date -d "$TARGET_DATE" +%y%m%d)

mkdir -p "$DAILY_ROOT/$TARGET_DATE"
TXT_OUT="$DAILY_ROOT/$TARGET_DATE/${YYMMDD}-plan.txt"
EXC_OUT="$DAILY_ROOT/$TARGET_DATE/${YYMMDD}-plan.excalidraw"

if [ -e "$TXT_OUT" ] && [ "$FORCE" -ne 1 ]; then
    cat >&2 <<EOF
✗ Plan already exists: $TXT_OUT

Re-run with --force to overwrite, or delete the file first:
    rm $TXT_OUT $EXC_OUT
EOF
    exit 1
fi

# 3. Write content (atomic via temp + mv).
TMP="$TXT_OUT.tmp.$$"
cat "$CONTENT_SRC" > "$TMP"
mv "$TMP" "$TXT_OUT"
echo "→ wrote $TXT_OUT ($(wc -l <"$TXT_OUT" | tr -d ' ') lines)"

# 4. Render to .excalidraw.
# Resolve canvas tool path (allow override via env).
if [ ! -x "$CANVAS_TOOL" ]; then
    for cand in \
        "$HOME/.claude/skills/diagram-ascii-canvas/bin/txt-to-canvas.py" \
        "$(cd "$(dirname "$0")"/../.. && pwd)/../diagram-skill/skills/diagram-ascii-canvas/bin/txt-to-canvas.py" \
        ; do
        if [ -x "$cand" ]; then CANVAS_TOOL="$cand"; break; fi
    done
fi
if [ ! -x "$CANVAS_TOOL" ]; then
    echo "✗ can't find txt-to-canvas.py (set CANVAS_TOOL env var)" >&2
    exit 1
fi

echo "→ rendering canvas..."
"$CANVAS_TOOL" "$TXT_OUT" --out "$EXC_OUT" 2>&1 | sed 's/^/   /'

# 5. Commit.
git add -- "$TXT_OUT" "$EXC_OUT"
# Also include any auto-rendered _pngs so they don't show as dirty.
if [ -d "$DAILY_ROOT/$TARGET_DATE/_pngs" ]; then
    git add -- "$DAILY_ROOT/$TARGET_DATE/_pngs" 2>/dev/null || true
fi
git commit -m "plan($TARGET_DATE): $SLUG" >/dev/null
echo "→ committed: plan($TARGET_DATE): $SLUG"

# 6. Push (retry once on rejection).
if git remote get-url origin >/dev/null 2>&1; then
    if git push 2>&1 | sed 's/^/   /'; then
        echo "✓ pushed"
    else
        echo "⚠ push rejected; pulling and retrying..."
        git pull --rebase --autostash 2>&1 | sed 's/^/   /'
        git push 2>&1 | sed 's/^/   /'
        echo "✓ pushed (after retry)"
    fi
fi

echo "✓ done: $TXT_OUT + $EXC_OUT"
