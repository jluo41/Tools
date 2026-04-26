#!/usr/bin/env bash
# install-cron.sh — install a 22:00-daily trigger for chronicle-daily rollup.
#
# Usage:
#   install-cron.sh              # install
#   install-cron.sh --dry-run    # print plist, don't write
#   install-cron.sh --uninstall  # remove
#
# On macOS: writes ~/Library/LaunchAgents/dev.jluo41.chronicle-daily.plist
# On Linux: appends a line to crontab (idempotent).

set -euo pipefail

LABEL="dev.${USER}.chronicle-daily"
ROLLUP="$(cd "$(dirname "$0")" && pwd)/rollup.sh"
LOG_DIR="$HOME/Daily/.logs"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"

mode="${1:-install}"

case "$mode" in
    --uninstall|uninstall)
        if [ "$(uname)" = "Darwin" ] && [ -f "$PLIST" ]; then
            launchctl unload "$PLIST" 2>/dev/null || true
            rm -f "$PLIST"
            echo "✓ removed $PLIST"
        else
            crontab -l 2>/dev/null | grep -v "$ROLLUP" | crontab - || true
            echo "✓ removed cron entry"
        fi
        exit 0
        ;;
    --dry-run|dry-run)
        DRY=1
        ;;
    install|"")
        DRY=0
        ;;
    *)
        echo "Usage: $0 [install|--dry-run|--uninstall]" >&2
        exit 2
        ;;
esac

mkdir -p "$LOG_DIR"

if [ "$(uname)" = "Darwin" ]; then
    PLIST_BODY=$(cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>           <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>${ROLLUP}</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>   <integer>22</integer>
    <key>Minute</key> <integer>0</integer>
  </dict>
  <key>StandardOutPath</key> <string>${LOG_DIR}/chronicle-daily.out.log</string>
  <key>StandardErrorPath</key><string>${LOG_DIR}/chronicle-daily.err.log</string>
  <key>RunAtLoad</key>       <false/>
</dict>
</plist>
EOF
)
    if [ "${DRY:-0}" -eq 1 ]; then
        echo "$PLIST_BODY"
        exit 0
    fi
    mkdir -p "$(dirname "$PLIST")"
    printf '%s\n' "$PLIST_BODY" > "$PLIST"
    launchctl unload "$PLIST" 2>/dev/null || true
    launchctl load "$PLIST"
    echo "✓ installed launchd job: $LABEL"
    echo "  → fires daily at 22:00, logs in $LOG_DIR/"
else
    LINE="0 22 * * * /bin/bash -lc '${ROLLUP}' >>${LOG_DIR}/chronicle-daily.out.log 2>>${LOG_DIR}/chronicle-daily.err.log"
    if [ "${DRY:-0}" -eq 1 ]; then
        echo "$LINE"
        exit 0
    fi
    (crontab -l 2>/dev/null | grep -v "$ROLLUP"; echo "$LINE") | crontab -
    echo "✓ installed crontab entry"
fi
