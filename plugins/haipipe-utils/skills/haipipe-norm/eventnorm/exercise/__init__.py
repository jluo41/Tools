"""
eventnorm.exercise: one exercise event, raw to output (b51 s02, s12; JL 261022: "就是你要 follow 他，然后做一下跟他一样
的事情", following food's eventnorm).

    raw (a logged row, words, a wearable's samples) ─▶ preprocess ─▶ input JSON ─▶ describe-exercise, the item
        ─▶ output by local hour, each hour its own part (no share: an exercise event can be cut by the clock)

    from eventnorm.exercise import event
    ev = event(raw={"type": "device_code", "rows": [{...one ELogExerciseEntry row...}]})
    ev = event(raw={"type": "text", "rows": [{"text": "brisk walking 30 min", "time": "2026-10-22 08:05 -04:00"}]})
    ev = event(input={"start": "...", "end": "...", "items": [{"activity": "Walking"}]})

    schema.py      the raw types and the input's keys
    preprocess.py  raw to input: a logged row named through the code book, words, a stream and its rule
    hours.py       each hour its own part: a logged event by its minutes, a stream by its own samples
    assemble.py    event(): the input, describe-exercise for the item, the output by local hour

Lifted from b51 s02's drawing builder (studio/_build/topic_frames.py: exercise_event_dict, exercise_stated_total,
stream_table, stream_runs, longest_bout, exercise_stream_event, exercise_hours), where it ran first; s02 ③ and ④'s
examples are its test (eventnorm/tests/test_exercise_event.py). Served as POST /exercise/event
(servers/api-exercise/server.py); shown on /try/exercise.
"""
import sys
from pathlib import Path

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):
    _ex = _base.parents[3] / "describe-exercise"
    if (_ex / "exnorm").is_dir():
        if str(_ex) not in sys.path:
            sys.path.insert(0, str(_ex))
        break

from .assemble import event                     # noqa: E402
from .hours import exercise_hours, stream_hours  # noqa: E402
from .preprocess import preprocess               # noqa: E402
