#!/usr/bin/env bash
# write-session.sh — atomically log a session .txt to ~/Daily/ and sync to remote.
#
# Usage:
#   write-session.sh <slug>            < session-content.txt
#   write-session.sh <slug> <txt-path>
#
# Behavior:
#   1. cd ~/Daily
#   2. git pull --rebase --autostash   (no-op if no remote configured)
#   3. pick target date: today, OR tomorrow if today/.closed exists
#   4. write content to ~/Daily/<target_date>/<YYMMDD>-session-<slug>.txt
#   5. git add + commit + push (retry once on rejection)
#
# Exits non-zero on validation failure or git hard error.
# Skips push silently if no `origin` remote is set.

set -euo pipefail

DAILY_ROOT="${DAILY_ROOT:-$HOME/Daily}"

usage() {
    echo "Usage: $0 <slug> [content-file]    (or pipe content via stdin)" >&2
    exit 2
}

[ $# -ge 1 ] || usage
SLUG="$1"
CONTENT_SRC="${2:-/dev/stdin}"

# Validate slug: lowercase letters, digits, hyphens, 2-4 words.
if ! [[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+){1,5}$ ]]; then
    echo "✗ slug must be 2-6 hyphenated lowercase tokens, got: $SLUG" >&2
    exit 2
fi

if [ ! -d "$DAILY_ROOT/.git" ]; then
    cat >&2 <<EOF
✗ $DAILY_ROOT is not a git repo.

This workspace hasn't been bootstrapped for chronicle yet. Run:

    Tools/plugins/chronicle/bin/setup.sh git@github.com:<you>/Daily.git
        (existing private repo)
or:
    Tools/plugins/chronicle/bin/setup.sh init
        (local-only, no remote — push will be skipped)

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

# 2. Determine target date.
TODAY=$(date +%Y-%m-%d)
if [ -f "$DAILY_ROOT/$TODAY/.closed" ]; then
    TARGET_DATE=$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d "+1 day" +%Y-%m-%d)
    echo "ℹ today ($TODAY) is closed; writing to $TARGET_DATE instead"
else
    TARGET_DATE="$TODAY"
fi

YYMMDD=$(date -j -f %Y-%m-%d "$TARGET_DATE" +%y%m%d 2>/dev/null \
         || date -d "$TARGET_DATE" +%y%m%d)
HHMM=$(date +%H%M)   # write-time of THIS invocation; gives chronological lexical sort

mkdir -p "$DAILY_ROOT/$TARGET_DATE"
OUT="$DAILY_ROOT/$TARGET_DATE/${YYMMDD}-${HHMM}-${SLUG}.txt"

if [ -e "$OUT" ]; then
    echo "✗ $OUT already exists. Pick a different slug or rename." >&2
    exit 1
fi

# 3. Write content (atomic via temp + mv).
TMP="$OUT.tmp.$$"
cat "$CONTENT_SRC" > "$TMP"
mv "$TMP" "$OUT"
echo "→ wrote $OUT ($(wc -l <"$OUT" | tr -d ' ') lines)"

# 4. Commit.
git add -- "$OUT"
git commit -m "session($TARGET_DATE): $SLUG" >/dev/null
echo "→ committed: session($TARGET_DATE): $SLUG"

# 5. Push (retry once on rejection).
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

echo "✓ done: $OUT"
