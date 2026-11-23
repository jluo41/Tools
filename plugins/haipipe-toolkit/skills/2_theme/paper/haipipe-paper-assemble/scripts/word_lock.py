"""One build at a time in Microsoft Word, for every paper on this machine.

Word's `selection` belongs to its front document, so two builds measuring at once can search each other's file, and one
build's quit can end another's work. A Word stuck on a lock for days (b16.j02-s22, 261104) began when documents from two
papers were open together; whether they caused it is not proven. An OS lock, released when the process ends even on a
crash, on a file in the system temp folder; delivery_lock in build_delivery.py is per paper, this one is per machine.
"""
from contextlib import contextmanager
from pathlib import Path
import sys
import tempfile
import time


@contextmanager
def word_turn(wait: float = 900):
    """Wait for Word's turn; yields False when it does not come in `wait` seconds, and the caller goes without Word."""
    handle = open(Path(tempfile.gettempdir()) / "haipipe-word.lock", "a+", encoding="utf-8")
    try:
        import fcntl
    except ImportError:         # Windows: this lane never drives Word there
        handle.close()
        yield True
        return
    start, told, got = time.monotonic(), False, False
    while True:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            got = True
            break
        except OSError:
            if time.monotonic() - start >= wait:
                print(f"Word's turn did not come in {int(wait)} seconds: another build holds it", file=sys.stderr)
                break
            if not told:
                print("waiting for Word: another build is using it", file=sys.stderr)
                told = True
            time.sleep(2)
    try:
        yield got
    finally:
        if got:
            fcntl.flock(handle, fcntl.LOCK_UN)
        handle.close()


OWN_FOLDERS = ("haipipe-preview", "haipipe-measure")   # the copies a build opens in Word's own container


def word_in_use() -> bool:
    """True when the person has a document open in Word: a build then never opens, prints or closes a file there
    (Pp-AgreeableRx 261122: every build opened and closed windows in a Word open for 36 hours with shared OneDrive
    files, stole focus and left a preview copy open). HAIPIPE_WORD_PREVIEW=word uses Word anyway."""
    import os
    import subprocess
    if os.environ.get("HAIPIPE_WORD_PREVIEW") == "word":
        return False
    if subprocess.run(["pgrep", "-x", "Microsoft Word"], capture_output=True).returncode != 0:
        return False             # not running: a build may start it, use it alone and quit it
    try:                         # asked only while Word runs, so the question never launches it
        r = subprocess.run(["osascript", "-e", 'with timeout of 10 seconds\ntell application "Microsoft Word" to '
                            'get full name of documents\nend timeout'], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return True
    names = [n.strip() for n in r.stdout.split(",") if n.strip()]
    return r.returncode != 0 or any(not any(f in n for f in OWN_FOLDERS) for n in names)
