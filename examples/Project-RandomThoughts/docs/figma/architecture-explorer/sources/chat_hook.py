"""Claude Code Stop hook: when an answer ends, refresh the chat this session is kept as (hai-chat).

Reads the hook's JSON on stdin ({session_id, transcript_path, ...}). A session never saved with
`new_chat.py new --from` is not in the registry, and the hook exits at once without importing anything heavy.
It never blocks the session: every error is written to stderr and the exit code is 0.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> int:
    try:
        event = json.load(sys.stdin)
        reg = Path(os.environ.get("HAIPIPE_CHAT_REGISTRY") or Path.home() / ".claude" / "hai-chat" / "kept.json")
        folder = json.loads(reg.read_text()).get(event.get("session_id", "")) if reg.is_file() else None
        source = event.get("transcript_path") or ""
        if not folder or not Path(folder).is_dir() or not Path(source).is_file():
            return 0
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import new_chat
        new_chat.main(["refresh", folder, "--from", source, "--quiet"])
    except Exception as err:                    # a hook must never stop the session
        print(f"hai-chat hook: {err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
