#!/usr/bin/env python3
"""
Upload a .excalidraw file to the self-hosted server and register it as a named board.

Usage:
    python3 upload.py <file-path> <board-name>

The server handles AES-256-GCM encryption internally, so no local crypto
dependencies are required. Only Python stdlib is used.
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path


SERVER = "http://localhost:3003"


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: upload.py <file-path> <board-name>", file=sys.stderr)
        sys.exit(1)

    file_path  = Path(sys.argv[1]).expanduser().resolve()
    board_name = sys.argv[2]

    if not file_path.exists():
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    raw = file_path.read_bytes()

    # Basic sanity check
    try:
        scene = json.loads(raw)
        assert scene.get("type") == "excalidraw"
    except Exception:
        print(f"Error: not a valid .excalidraw file: {file_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Uploading {file_path.name}  →  board '{board_name}' …")

    req = urllib.request.Request(
        f"{SERVER}/upload/{board_name}",
        data=raw,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
    except urllib.error.URLError as exc:
        print(f"Error: could not reach server at {SERVER}: {exc}", file=sys.stderr)
        print("Is the Excalidraw stack running?  cd apps/excalidraw && docker compose up -d", file=sys.stderr)
        sys.exit(1)

    print(f"✓  https://draw.jjluo.com/d/{result['board']}")


if __name__ == "__main__":
    main()
