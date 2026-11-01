"""
eventnorm.medication: one medication event, raw to output (b51 s03, s13; JL 261027: "啊 整去整吧", following food's
eventnorm and exercise's eventnorm.exercise).

    raw (a WellDoc id, a Shanghai cell, a pump cell, an OhioT1DM pump event) ─▶ preprocess ─▶ input JSON
        ─▶ describe-medication, each item ─▶ output by local hour (a dose is a moment: its hour, share 1)

    from eventnorm.medication import event
    ev = event(raw={"type": "app_id", "rows": [{...one MedAdministration row...}]})
    ev = event(raw={"type": "text", "rows": [{"Date": "2021-06-15 08:00:00", "Non-insulin hypoglycemic agents":
                                               "metformin 0.5 g, acarbose 50 mg"}]})
    ev = event(input={"start": "...", "items": [{"drug": "metformin", "dose": 500, "unit": "mg"}]})

    schema.py      the raw types, the input's keys, an item's keys, how a dose went in (delivery)
    preprocess.py  raw to input: a WellDoc id named through WellDoc's catalog, a cell split into its drugs, a pump
                   cell's drug from its header, an OhioT1DM event's class and the patient's product
    assemble.py    event(): the input, describe-medication for each item, the output by local hour (eventnorm/hours.py)

Lifted from b51 s03's drawing builder (studio/_build/topic_frames.py: dose_event_dict), where a dose first became an
event; s03's examples are its test (eventnorm/tests/test_medication_event.py). Served as POST /medication/event
(servers/api-medication/server.py). An item with insulin: true goes on to s14 (describe-insulin) for its curve.
"""
import sys
from pathlib import Path

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):
    _med = _base.parents[3] / "describe-medication"
    if (_med / "mednorm").is_dir():
        if str(_med) not in sys.path:
            sys.path.insert(0, str(_med))
        break

from .assemble import event                     # noqa: E402
from .preprocess import preprocess              # noqa: E402

__all__ = ["event", "preprocess"]
