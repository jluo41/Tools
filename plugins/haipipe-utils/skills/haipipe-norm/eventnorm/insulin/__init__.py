"""
eventnorm.insulin: one insulin event, raw to output (b51 s04, s14; JL 261027: "send the message to other sessions to ask
them to build their own page accordingly", after j04 t03 froze ext_insulin_event).

    raw (a WellDoc id, a Shanghai cell, a pump cell, an OhioT1DM pump event) ─▶ medication's preprocess ─▶ input JSON
        ─▶ the insulin chain, each drug (describe-medication, then describe-insulin) ─▶ output by local hour:
           a dose spread by its curve, a rate by its minutes

    from eventnorm.insulin import event
    ev = event(raw={"type": "app_id", "rows": [{...one MedAdministration row...}]})
    ev = event(input={"start": "2024-05-09 06:28 -04:00", "items": [{"drug": "Lyumjev", "dose": 2, "unit": "iu",
                                                                     "delivery": "mdi"}]})

    assemble.py    event(): medication's preprocess makes the input; each drug is asked of the insulin chain as j04 t02
                   asks it; a dose is spread over the hours it acts, a rate over the minutes it runs

The raw types and the input are medication's (eventnorm/medication: one preprocess step for both, s14 ① engine 1). The
spread is j04 t03's (t03_insulin_event/scripts/build_insulin_event.py), so a dose sent here answers as
ext_insulin_event froze it (eventnorm/tests/test_insulin_event.py). Served as POST /insulin/event
(servers/api-insulin/server.py).
"""
import sys
from pathlib import Path

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):
    _med = _base.parents[3] / "describe-medication"
    _ins = _base.parents[3] / "describe-insulin"
    if (_med / "mednorm").is_dir():
        for _p in (_med, _ins):
            if str(_p) not in sys.path:
                sys.path.insert(0, str(_p))
        break

from .assemble import event                     # noqa: E402

__all__ = ["event"]
