"""
eventnorm.still: one still event, raw to output (b51 s07, s17; JL 261027: every event type its own tab of the try page).

    raw (minute rows; mcPhases' steps, heart rate and sleep) ─▶ preprocess ─▶ input JSON, its minutes as stretches
        ─▶ output by local hour: asleep + moving + still + unknown = its minutes

    from eventnorm.still import event
    ev = event(raw={"type": "minutes", "day": "2026-10-27", "rows": [{"from": "10:00", "to": "10:40", "bpm": 72}]})

    schema.py      the raw types, the levels, the rule (provisional: 0 steps, s17 Open 1)
    preprocess.py  raw to the minute timeline: minute rows, mcPhases' three files
    hours.py       each minute one way; each hour added up
    assemble.py    event()

Lifted from b51 s07's drawing builder (studio/_build/topic_frames.py: mc_day, still_hour_counts), where it ran first;
s07 ② and ④'s numbers are its test (eventnorm/tests/test_still_event.py). Served as POST /still/event
(servers/api-still/server.py).
"""
from .assemble import event                    # noqa: E402
from .hours import by_hour, way                # noqa: E402
from .preprocess import preprocess             # noqa: E402
