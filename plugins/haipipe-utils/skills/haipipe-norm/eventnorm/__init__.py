"""
eventnorm: the event layer every normalizer shares (s01 ⑦ ①; JL 261021: "make the page on event to work").

    raw (many kinds) ─▶ preprocess ─▶ input JSON ─▶ the noun's enrich(items) ─▶ output JSON by local hour

    from eventnorm import event
    ev = event(raw={"type": "app_log", "rows": [...]})      # {"raw", "input", "output", "step"}

    schema.py      the event JSON: raw, input, output
    preprocess/    raw to input, a file a raw type: app_log, text, photo, numbers_only
    hours.py       hour_shares, by_hour: any event by local hour (food and exercise both call it)
    assemble.py    event(), assemble(): input + enrich(items) to the output

Food only for now: enrich(items) is describe-food's foodnorm/items.py, put on sys.path here when the caller has not
(the API host already has). Served as POST /food/event (servers/api-food/server.py); shown on /try/food.
"""
import sys
from pathlib import Path

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):
    _food = _base.parents[2] / "describe-food"
    if (_food / "foodnorm").is_dir():
        if str(_food) not in sys.path:
            sys.path.insert(0, str(_food))
        break

from .assemble import assemble, event          # noqa: E402
from .hours import by_hour, hour_shares        # noqa: E402
from .preprocess import preprocess             # noqa: E402

__all__ = ["event", "assemble", "preprocess", "by_hour", "hour_shares"]
