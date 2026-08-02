"""QD2 R1 · the turn ring, tested where a browser cannot see it.

The bug these exist for was not visible in any assertion about output: the
first `drain()` treated a notify that did not satisfy its condition as a reason
to leave the wait, so it wrote a keepalive per iteration and spun. The server
answered correctly right up until it stopped answering at all, with 13,149
threads and 292% CPU. So the tests that matter here are about the SHAPE of the
loop, not only about what it delivers.
"""

import threading
import time

import pytest

from live import turnring


def _drain(turn, cursor=0):
    """Drain into a list on its own thread; returns (thread, sink, stop)."""
    sink = []

    def write(obj):
        sink.append(obj)
        return True

    t = threading.Thread(target=turn.drain, args=(cursor, write), daemon=True)
    t.start()
    return t, sink


def test_a_reader_gets_everything_from_its_cursor():
    turn = turnring.Turn("k")
    for i in range(5):
        turn.push({"t": "delta", "text": str(i)})
    t, sink = _drain(turn, cursor=2)
    turn.push({"t": "done"})
    turn.finish()
    t.join(timeout=5)
    assert not t.is_alive(), "drain did not return when the turn finished"
    assert [e["n"] for e in sink] == [2, 3, 4, 5]


def test_a_late_reader_still_ends_at_done():
    turn = turnring.Turn("k")
    turn.push({"t": "delta", "text": "a"})
    turn.finish()
    t, sink = _drain(turn, cursor=0)
    t.join(timeout=5)
    assert not t.is_alive()
    assert [e["n"] for e in sink] == [0]


def test_a_busy_producer_does_not_make_drain_spin():
    """The regression itself: every push notifies, and a notify must not by
    itself produce a write. 200 events must yield 200 writes, never 200 plus a
    keepalive per wakeup."""
    turn = turnring.Turn("k")
    t, sink = _drain(turn, cursor=0)
    for i in range(200):
        turn.push({"t": "delta", "text": "x"})
        time.sleep(0.001)
    turn.finish()
    t.join(timeout=5)
    assert not t.is_alive()
    assert len(sink) == 200, f"expected exactly 200 writes, got {len(sink)}"
    assert not [e for e in sink if e.get("t") == "ping"], "spun: keepalives during a busy turn"


def test_a_departed_reader_ends_only_itself():
    turn = turnring.Turn("k")
    gone = []

    def write(obj):
        gone.append(obj)
        return False                      # the socket is closed

    t = threading.Thread(target=turn.drain, args=(0, write), daemon=True)
    turn.push({"t": "delta", "text": "a"})
    t.start()
    t.join(timeout=5)
    assert not t.is_alive(), "drain did not give up on a dead socket"
    assert not turn.done, "one reader leaving must not end the turn"
    turn.push({"t": "delta", "text": "b"})
    assert turn.seq == 2, "the turn kept recording after its reader left"


def test_trimming_tells_the_reader_it_missed_something():
    turn = turnring.Turn("k")
    turn.push({"t": "delta", "text": "a"})
    turn.base, turn.seq = 5, 6            # pretend the front was trimmed away
    turn.events[0]["n"] = 5
    turn.finish()
    t, sink = _drain(turn, cursor=0)
    t.join(timeout=5)
    assert not t.is_alive()
    assert sink and sink[0]["t"] == "gap" and sink[0]["missed"] == 5


def test_the_cap_trims_from_the_front():
    turn = turnring.Turn("k")
    big = "x" * 40_000
    for _ in range(40):                   # 1.6MB against a 1MB cap
        turn.push({"t": "delta", "text": big})
    assert turn.bytes <= turnring.MAX_BYTES
    assert turn.base > 0, "nothing was trimmed"
    assert turn.events[0]["n"] == turn.base, "base and the first event disagree"


def test_a_finished_ring_is_swept_after_its_grace():
    turnring.TURNS.clear()
    turn = turnring.start("scope")
    turn.finish()
    assert turnring.get("scope") is turn
    turn.ended_at = time.time() - turnring.GRACE_S - 1
    assert turnring.get("scope") is None, "a stale ring was never swept"


def test_live_is_true_only_while_a_turn_runs():
    turnring.TURNS.clear()
    assert turnring.live("s") is False
    t = turnring.start("s")
    assert turnring.live("s") is True
    t.finish()
    assert turnring.live("s") is False


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
