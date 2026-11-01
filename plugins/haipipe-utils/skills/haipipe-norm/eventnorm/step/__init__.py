"""
eventnorm.step: one step event, raw to output (b51 s05, s15; JL 261027: "你继续去弄啊", s15-D03 drawn on s12's
second version).

    raw (a logged StepEntry row, a wearable's steps) ─▶ preprocess ─▶ input JSON ─▶ output by local hour
        a logged row: each hour its share to the second, the row's total, and its own minutes and steps (in_hour);
        a whole day keeps its day. a stream: each hour its own samples, and its walks for POST /exercise/event

    from eventnorm.step import event
    ev = event(raw={"type": "log", "rows": [{...one StepEntry row...}]})
    ev = event(input={"start": "2022-06-29 16:56 -05:00", "end": "2022-06-29 17:24 -05:00", "total": {"steps": 128}})

    schema.py      the raw types, the input's keys, the kinds by length
    preprocess.py  raw to input: a WellDoc row's times and device, a stream's samples and walks (exercise's runs_of)
    hours.py       by local hour: shares to the second, in_hour; a stream's hours from its samples
    assemble.py    event(), events()

Lifted from b51 s05's drawing builder (studio/_build/topic_frames.py: span_times, span_kind, device_name, span_hours,
span_event_dict), where it ran first; s05 ② and ③'s rows are its test (eventnorm/tests/test_step_event.py). Served as
POST /step/event (servers/api-step/server.py).
"""
from .assemble import event, events            # noqa: E402
from .hours import kind, log_hours, span_hours, stream_hours  # noqa: E402
from .preprocess import device_name, preprocess  # noqa: E402
