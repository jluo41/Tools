#!/usr/bin/env python3
"""lab_launch.py <session-id> <name> <first-prompt-file> · one terminal of the paper writing lab.

open_writing_lab.py puts this in each workspace task. It resumes the Section session when its transcript
exists, else starts a new session with that id, that name and the unit's read-only first turn. A session
already open in another terminal is not opened twice.
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def open_elsewhere(sid):
    try:
        out = subprocess.run([CLAUDE, "agents", "--json"], capture_output=True, text=True, timeout=30).stdout
        return any(x.get("sessionId") == sid and x.get("kind") == "interactive" for x in json.loads(out or "[]"))
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


CLAUDE = os.environ.get("CLAUDE_BIN") or "claude"
KEEP = {"CLAUDE_CONFIG_DIR"}


def own_session_env():
    """A lab opened from inside a Claude session inherits that session's markers (CLAUDE_CODE_CHILD_SESSION,
    CLAUDE_CODE_SESSION_ID, CLAUDECODE, ...). Claude then treats the Section session as a child and saves no
    transcript ("Transcript saving is off"). Drop them so each Section session is its own top-level session."""
    for k in list(os.environ):
        if (k.startswith("CLAUDE") and k not in KEEP) or k == "CLAUDECODE":
            del os.environ[k]


def main():
    sid, name, prompt_file = sys.argv[1:4]
    home = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    exists = any((home / "projects").glob(f"*/{sid}.jsonl"))
    if exists and open_elsewhere(sid):
        print(f"{name} is already open in another terminal; it is not opened twice.")
        return
    own_session_env()
    if exists:
        os.execvp(CLAUDE, [CLAUDE, "--resume", sid])
    prompt = Path(prompt_file).read_text(encoding="utf-8")
    os.execvp(CLAUDE, [CLAUDE, "--session-id", sid, "-n", name, prompt])


if __name__ == "__main__":
    main()
