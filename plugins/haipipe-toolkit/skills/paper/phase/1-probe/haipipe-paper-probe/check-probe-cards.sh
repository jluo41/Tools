#!/bin/sh
# Compatibility entrypoint. The contract and implementation live together.
exec python3 "$(dirname "$0")/check_topic_entries.py" "$@"
