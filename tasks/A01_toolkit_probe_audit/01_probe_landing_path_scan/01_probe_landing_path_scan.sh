#!/usr/bin/env bash
# 01_probe_landing_path_scan — grep probe-related toolkit files for the literal
# path token "1-probes/", splitting LIVE instruction/code hits from HISTORY
# (CHANGELOGs, _old/ archives, test fixtures).
set -euo pipefail

TOOLKIT="${1:-/Users/floydluo/Desktop/Tools-SPACE/plugins/haipipe-toolkit}"
OUT="${2:-$(dirname "$0")/results/run_scan}"
mkdir -p "$OUT"

# Inventory: probe-related files = under agents/ or skills/, whose path or
# content concerns probe dispatch.
{
  find "$TOOLKIT/agents" -type f -name "*.md"
  find "$TOOLKIT/skills" -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" \)
} | while read -r f; do
  case "$f" in
    *probe*|*Probe*) echo "$f"; continue ;;
  esac
  grep -qli "probe" "$f" 2>/dev/null && echo "$f" || true
done | sort > "$OUT/file-inventory.txt"

# All hits of the literal token across the inventory.
: > "$OUT/grep-live.txt"
: > "$OUT/grep-history.txt"
while read -r f; do
  hits=$(grep -n "1-probes/" "$f" 2>/dev/null || true)
  [ -z "$hits" ] && continue
  case "$f" in
    */_old/*|*CHANGELOG*|*test/fixture*|*_archive*|*_feedback*)
      dest="$OUT/grep-history.txt" ;;
    *)
      dest="$OUT/grep-live.txt" ;;
  esac
  printf '%s\n' "$hits" | sed "s|^|$f:|" >> "$dest"
done < "$OUT/file-inventory.txt"

echo "inventory: $(wc -l < "$OUT/file-inventory.txt") files"
echo "live hits: $(wc -l < "$OUT/grep-live.txt")"
echo "history hits: $(wc -l < "$OUT/grep-history.txt")"
