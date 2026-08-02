"""QD2 §9 R1 · the turn ring — what QD3's terminal has had all along.

A terminal survives a reload because its bytes go to a RING that clients ATTACH
to (`term.py`'s reader thread → `RING_CAP` bytearray → every attached WS client,
replayed in full on reconnect). Chat wrote its bytes straight down the socket of
whoever happened to ask: `emit()` called `self.wfile.write`, so the turn's only
copy of itself WAS one HTTP response, and anything that ended that response ended
the visible turn — navigating away, switching a setting, or a long job timing out
(JL 260801: "为啥我一停，我一 shift 到其他的这个配置，这就停了").

This module is that asymmetry removed. One `Turn` per question key holds the
turn's events with a monotonic cursor; the producer pushes, and any number of
HTTP readers drain from whatever cursor they hold. A reader leaving is no longer
an event the turn can notice, and a reader coming back replays the part it
missed instead of staring at a gap.

Two things are deliberately NOT here. Reaping a held `claude` client stays with
`SessionHost` — this only owns the event record, which is cheap and dies on its
own grace timer. And nothing here decides anything about permissions: the ring
carries the `ask` event like any other, and the gate still lives in `chat.py`.
"""

import threading
import time

# One turn's ring. Chat events are JSON objects rather than terminal bytes, so
# the cap is expressed both ways: a long turn is thousands of `delta` events,
# while one `tool_result` can be large on its own.
MAX_BYTES = 1_048_576
MAX_EVENTS = 20_000
# How long a FINISHED ring stays readable. This is the reader's grace period,
# the same idea as `term.py`'s parking deadline: a browser that comes back
# inside it sees how the turn ended rather than an empty drawer.
GRACE_S = 600
# Silence after which a draining reader is sent a keepalive. Marked `idle` so
# the drawer's watchdog does NOT count it as progress — a hung turn must still
# be able to look hung.
PING_S = 25

TURNS = {}
_LOCK = threading.Lock()


class Turn:
    """The event record of one turn, owned by nobody's socket."""

    __slots__ = ("key", "events", "sizes", "bytes", "base", "seq", "done",
                 "ended_at", "started_at", "cond")

    def __init__(self, key):
        self.key = key
        self.events = []
        self.sizes = []          # parallel to events, so trimming costs nothing
        self.bytes = 0
        self.base = 0            # cursor of events[0]; rises as the ring trims
        self.seq = 0             # cursor the NEXT event will get
        self.done = False
        self.started_at = time.time()
        self.ended_at = None
        self.cond = threading.Condition()

    # ---- producer side -------------------------------------------------
    def push(self, obj):
        """Record one event. Never fails, never blocks on a reader.

        The cursor rides IN the event as `n`, so a returning drawer can say
        exactly where it stopped without having counted anything.
        """
        with self.cond:
            if self.done:
                return
            obj = dict(obj, n=self.seq)
            size = 32 + sum(len(v) for v in obj.values() if isinstance(v, str))
            self.events.append(obj)
            self.sizes.append(size)
            self.bytes += size
            self.seq += 1
            self._trim()
            self.cond.notify_all()

    def finish(self):
        with self.cond:
            self.done = True
            self.ended_at = time.time()
            self.cond.notify_all()

    def _trim(self):
        """Drop from the FRONT, and let `base` remember that we did.

        A reader whose cursor fell behind `base` is told `gap` rather than
        handed a silently incomplete stream: it can then fall back to the
        transcript, which is the honest answer to "you missed some of this".
        """
        while (len(self.events) > MAX_EVENTS or self.bytes > MAX_BYTES) \
                and len(self.events) > 1:
            self.bytes -= self.sizes.pop(0)
            del self.events[0]
            self.base += 1

    # ---- reader side ---------------------------------------------------
    def drain(self, cursor, write):
        """Write every event from `cursor` on, returning when the turn ends.

        `write(obj) -> bool` reports whether the socket is still there. A False
        only ends THIS reader: the turn does not learn about it, which is the
        whole point of the module.
        """
        while True:
            with self.cond:
                # Wait ONLY while there is genuinely nothing for this reader.
                # `Condition.wait` returns False only on timeout, so a notify
                # that does not satisfy the condition sends us back to waiting
                # instead of out of the loop. Getting this wrong spun the CPU
                # and wrote a keepalive per iteration: 13k threads, 292% CPU,
                # and a server that stopped answering (found by driving it).
                idle = False
                while cursor >= self.seq and not self.done:
                    if not self.cond.wait(timeout=PING_S):
                        idle = True               # real silence → keepalive
                        break
                if cursor < self.base:
                    missed = self.base - cursor   # trimmed past this reader
                    cursor, batch = self.base, []
                else:
                    missed = 0
                    batch = self.events[cursor - self.base:]
                done, seq = self.done, self.seq
            if missed:
                if not write({"t": "gap", "missed": missed,
                              "text": "(reconnected mid-turn; %d earlier events "
                                      "are past the buffer)" % missed}):
                    return
                continue
            for e in batch:
                if not write(e):
                    return                        # this reader left; the turn did not
                cursor = e["n"] + 1
            if done and cursor >= seq:
                return
            # A keepalive is owed ONLY after real silence. Sending one merely
            # because we caught up writes a ping after every single event, which
            # is the same spin wearing a different shape: 200 events, 400 writes.
            if idle and not batch and not write({"t": "ping", "idle": True}):
                return


def _sweep():
    now = time.time()
    for key, t in list(TURNS.items()):
        if t.done and t.ended_at and now - t.ended_at > GRACE_S:
            TURNS.pop(key, None)


def start(key):
    """Open a fresh ring for this question, replacing any finished one."""
    with _LOCK:
        _sweep()
        t = Turn(key)
        TURNS[key] = t
        return t


def get(key):
    with _LOCK:
        _sweep()
        return TURNS.get(key)


def live(key):
    t = get(key)
    return t is not None and not t.done
