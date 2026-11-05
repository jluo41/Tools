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
