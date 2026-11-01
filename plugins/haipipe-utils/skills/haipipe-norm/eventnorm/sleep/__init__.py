"""
eventnorm.sleep: one sleep event, raw to output (b51 s06, s16; JL 261027: "send the message to other sessions to ask
them to build their own page accordingly", relayed by EventStore-Food-v2).

    raw (WellDoc SleepEntry rows) ─▶ preprocess ─▶ input JSON ─▶ output by local hour, in minutes
        Apple (EntrySourceID 20) writes a night twice: a whole row, the time in bed, and shorter rows inside it, the
        minutes asleep. The pieces, joined, are the timeline; the gaps are awake in bed. A row with no pieces (FitBit,
        Google, typed) is in bed, asleep not told: unknown. Each local hour keeps its own minutes, never a share.

    from eventnorm.sleep import event
    ev = event(raw={"type": "log", "rows": [{...the whole row...}], "pieces": [{"StartDateTime", "EndDateTime"}, ...]})
    ev = event(input={"start": "2023-01-23 02:00 -05:00", "end": "2023-01-23 06:00 -05:00",
                      "timeline": [{"from": "02:30", "to": "05:30", "state": "asleep"}]})

    schema.py      the raw types, the input's keys, the kinds by length
    preprocess.py  raw to input: the longest row is the night, shorter rows inside it its pieces, clipped and joined
    hours.py       joined, minutes_by_hour: each local hour its minutes in bed, asleep, awake in bed or unknown
    assemble.py    event(), events()

Lifted from b51 s06's drawing builder (studio/_build/topic_frames.py: joined, minutes_by_hour, sleep_night_dict),
where it ran first; s06 ② and ③'s nights are its test (eventnorm/tests/test_sleep_event.py). Served as
POST /sleep/event (servers/api-sleep/server.py).
"""
from .assemble import event, events            # noqa: E402
from .hours import joined, minutes_by_hour, night_hours  # noqa: E402
from .preprocess import preprocess              # noqa: E402
