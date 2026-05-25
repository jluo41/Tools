#!/usr/bin/env bash
# Upload a .excalidraw file as a public GitHub gist and print a one-click
# excalidraw.com URL that loads it.
#
# Usage:  share-canvas.sh path/to/canvas.excalidraw [-d "description"]
#
# Output:
#   <gist URL>           — the gist page (raw JSON view)
#   <raw URL>            — direct raw .excalidraw, CORS-open
#   <excalidraw URL>     — https://excalidraw.com/#url=<raw URL>  ← click this
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 path/to/canvas.excalidraw [-d description]" >&2
  exit 1
fi

file="$1"; shift || true
desc="ASCII diagrams canvas (diagram-ascii-canvas)"
if [[ "${1:-}" == "-d" ]]; then
  desc="$2"
  shift 2
fi

if [[ ! -f "$file" ]]; then
  echo "file not found: $file" >&2
  exit 1
fi

bytes=$(wc -c < "$file" | tr -d ' ')
if (( bytes > 9 * 1024 * 1024 )); then
  echo "warn: file is ${bytes} bytes — gist hard limit is 10MB per file" >&2
fi

# Create the gist; gh prints the gist URL on stdout.
gist_url=$(gh gist create --public --desc "$desc" "$file")
gist_id="${gist_url##*/}"

# gh api to discover owner login + the canonical raw_url for this file.
read -r owner raw_url < <(
  gh api "gists/$gist_id" --jq \
    '[.owner.login, (.files | to_entries[0].value.raw_url)] | @tsv'
)

excali_url="https://excalidraw.com/#url=${raw_url}"

echo "gist:       $gist_url"
echo "raw:        $raw_url"
echo "excalidraw: $excali_url"
