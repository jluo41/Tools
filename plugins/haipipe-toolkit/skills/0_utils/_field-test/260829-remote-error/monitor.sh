#!/usr/bin/env bash
# MONITOR, read-only. Finds the field desk by its custom title and reports drift.
# Never writes to the field desk. Reports to the human only. (field-test law 8)
set -u
NAME="${1:-C-VisitLBP-FieldTest}"
ROOT="/Users/jluo41/Desktop/Physician-SPACE"
REG="$ROOT/_WorkSpace/0-CMS-Store/Issue-From-CMS-Server"
P="$HOME/.claude/projects/-Users-jluo41-Desktop-Physician-SPACE"

echo "== $(date '+%H:%M:%S')  field desk '$NAME' =="
HIT=$(grep -l "\"customTitle\":\"$NAME\"" "$P"/*.jsonl 2>/dev/null | head -1)
if [ -z "$HIT" ]; then echo "   session: NOT STARTED YET"; else
  echo "   session: $(basename "$HIT" .jsonl)"
  echo "   turns  : $(grep -c '"type":"assistant"' "$HIT")   last: $(date -r "$HIT" '+%H:%M:%S')"
fi
echo "== target drift =="
echo "   260829/ : $(ls "$REG/260829/" 2>/dev/null | tr '\n' ' ')"
echo "   git     : $(git -C "$ROOT" status --short | wc -l | tr -d ' ') dirty paths"
echo "   FROZEN? : $(git -C "$ROOT/Tools" status --short plugins/haipipe-toolkit/skills/0_utils/remote-error | wc -l | tr -d ' ') edits to the skill under test  (must stay 0)"
echo "   friction: $([ -f "$(dirname "$0")/friction-log.md" ] && echo present || echo absent)"
