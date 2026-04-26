#!/usr/bin/env bash
# rollup.sh — end-of-day rollup: build canvas + mark day closed + sync.
#
# Usage:
#   rollup.sh                  # today
#   rollup.sh 2026-04-25       # specific date (YYYY-MM-DD)
#
# Idempotent: if <date>/.closed already exists, exits 0 silently.

set -euo pipefail

DAILY_ROOT="${DAILY_ROOT:-$HOME/Daily}"
CANVAS_TOOL="${CANVAS_TOOL:-$(dirname "$0")/../../../../diagram-skill/skills/diagram-ascii-canvas/bin/txt-to-canvas.py}"

TARGET_DATE="${1:-$(date +%Y-%m-%d)}"

if ! [[ "$TARGET_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "✗ bad date: $TARGET_DATE (expect YYYY-MM-DD)" >&2
    exit 2
fi

if [ ! -d "$DAILY_ROOT/.git" ]; then
    echo "✗ $DAILY_ROOT is not a git repo" >&2
    exit 1
fi

DAY_DIR="$DAILY_ROOT/$TARGET_DATE"
if [ ! -d "$DAY_DIR" ]; then
    echo "ℹ no folder for $TARGET_DATE — nothing to rollup"
    exit 0
fi

if [ -f "$DAY_DIR/.closed" ]; then
    echo "ℹ $TARGET_DATE already closed; skipping"
    exit 0
fi

cd "$DAILY_ROOT"

# Pull latest before rebuilding, in case another device pushed sessions.
if git remote get-url origin >/dev/null 2>&1; then
    echo "→ pulling from origin..."
    git pull --rebase --autostash 2>&1 | sed 's/^/   /'
fi

# Re-check after pull (a sibling device may have already closed the day).
if [ -f "$DAY_DIR/.closed" ]; then
    echo "ℹ $TARGET_DATE was closed by another device while pulling; skipping"
    exit 0
fi

# Need at least one session.
# Match the YYMMDD-HHMM-*.txt naming pattern (chronicle-session output).
N_SESSIONS=$(find "$DAY_DIR" -maxdepth 1 -type f -name '[0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-*.txt' | wc -l | tr -d ' ')
if [ "$N_SESSIONS" -eq 0 ]; then
    echo "⚠ no *-session-*.txt files in $DAY_DIR; nothing to rollup"
    exit 0
fi

echo "→ rolling up $TARGET_DATE ($N_SESSIONS sessions)"

# Resolve canvas tool path (allow override via env).
if [ ! -x "$CANVAS_TOOL" ]; then
    # Try a couple of sensible fallbacks.
    for cand in \
        "$HOME/.claude/skills/diagram-ascii-canvas/bin/txt-to-canvas.py" \
        "$(cd "$(dirname "$0")"/../.. && pwd)/diagram-skill/skills/diagram-ascii-canvas/bin/txt-to-canvas.py" \
        ; do
        if [ -x "$cand" ]; then CANVAS_TOOL="$cand"; break; fi
    done
fi
if [ ! -x "$CANVAS_TOOL" ]; then
    echo "✗ can't find txt-to-canvas.py (set CANVAS_TOOL env var)" >&2
    exit 1
fi

"$CANVAS_TOOL" "$DAY_DIR" 2>&1 | sed 's/^/   /'

# Mark day closed.
touch "$DAY_DIR/.closed"
echo "→ marked .closed"

# Commit + push the rolled-up artifacts.
git add -- "$DAY_DIR"
git commit -m "rollup($TARGET_DATE): $N_SESSIONS sessions" >/dev/null
echo "→ committed: rollup($TARGET_DATE): $N_SESSIONS sessions"

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

echo "✓ done: $TARGET_DATE rolled up and closed"
