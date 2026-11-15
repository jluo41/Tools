"""A watchdog for stuck requests: when any request has run longer than SLOW seconds, every thread's stack is written to
the server's log (stderr, the --daemon log file) once for that request, so a hang names the code that blocks it.
Python cannot stop a stuck thread; this only tells which one it is."""
from __future__ import annotations

import faulthandler
import sys
import threading
import time

SLOW = 30.0                               # seconds before a request counts as stuck
_RUNNING: dict = {}                       # thread id -> [start time, request line, already dumped]
_LOCK = threading.Lock()
_STARTED = False


def _watch() -> None:
    while True:
        time.sleep(5)
        now = time.monotonic()
        with _LOCK:
            stuck = [(tid, r) for tid, r in _RUNNING.items() if not r[2] and now - r[0] > SLOW]
            for _, r in stuck:
                r[2] = True
        for tid, (start, line, _) in stuck:
            print(f"[slow] {now - start:.0f}s on thread {tid}: {line}; all threads:", file=sys.stderr, flush=True)
            faulthandler.dump_traceback(file=sys.stderr, all_threads=True)


def start() -> None:
    global _STARTED
    with _LOCK:
        if _STARTED:
            return
        _STARTED = True
    threading.Thread(target=_watch, name="slow-watch", daemon=True).start()


class SlowWatchMixin:
    """Times each request of the handler it is mixed into; start() runs the watchdog."""

    def handle_one_request(self):
        try:
            return super().handle_one_request()
        finally:
            with _LOCK:
                _RUNNING.pop(threading.get_ident(), None)

    def parse_request(self):
        # the clock starts once a request has arrived: a kept-alive connection waiting for its next one is idle, not stuck
        ok = super().parse_request()
        with _LOCK:
            _RUNNING[threading.get_ident()] = [time.monotonic(), (getattr(self, "requestline", "") or "")[:200], False]
        return ok
