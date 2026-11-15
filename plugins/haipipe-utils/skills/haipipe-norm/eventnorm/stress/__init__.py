"""
eventnorm.stress: one stress event, raw to output (b51 j08, s10, s18; JL 261109: "set this as a goal and then go
ahead to make it").

    raw (a Garmin's stress reading every minute; a Fitbit's one score a day) ─▶ preprocess ─▶ input JSON, its minutes
        as stretches at one level ─▶ output by local hour: rest + low + medium + high + active + unknown = its minutes

    from eventnorm.stress import event
    ev = event(raw={"type": "readings", "rows": [{"time": "2023-11-27 20:28", "value": 74}, ...]})
    ev = event(raw={"type": "day_score", "rows": [{...one mcPhases stress_score.csv row...}]})

    schema.py      the raw types, the levels and their bands, the two scores' directions
    preprocess.py  raw to the minute timeline (readings), or to the day (day_score)
    hours.py       each minute one level; each hour added up, with its mean score
    assemble.py    event()

Built as step's, sleep's and still's (eventnorm/still is its nearest: an hour's minutes split, adding to its minutes).
Its test is eventnorm/tests/test_stress_event.py, on AI-READI's Garmin files and mcPhases' stress_score.csv. Served as
POST /stress/event (servers/api-stress/server.py).
"""
from .assemble import event                    # noqa: E402
from .hours import by_hour, level_of           # noqa: E402
from .preprocess import preprocess             # noqa: E402
