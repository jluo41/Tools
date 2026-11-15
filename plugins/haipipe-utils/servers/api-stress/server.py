"""
The stress event over HTTP: the same contract as `from eventnorm.stress import event`, reachable by anything that can
POST JSON (b51 j08, s18; built as step's, sleep's and still's lanes).

    Tools/plugins/haipipe-utils/servers/_host/run.sh
    curl -s localhost:8070/stress/event -H 'content-type: application/json' \\
         -d '{"raw": {"type": "readings", "rows": [{"time": "2026-11-09 10:00", "value": 74}]}}'

ONE DOOR, NO /normalize. A score has no words to look up, so this lane has only POST /event, as step's and still's,
and no describe-stress skill: the host loads it without one. Each hour's minutes come back six ways (rest, low,
medium, high, active, unknown) by Garmin's own bands, with the mean of its scored minutes; a Fitbit day score stays
its day, and its direction is the other way (higher is calmer).

NOT AUTHENTICATED, and bound to 127.0.0.1 by default. Stress readings are PHI. Before this listens on anything
routable it needs auth in front of it.
"""
import sys as _sys
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):      # eventnorm, in skills/haipipe-norm
    if (_base.parents[2] / "skills" / "haipipe-norm" / "eventnorm").is_dir():
        _sys.path.insert(0, str(_base.parents[2] / "skills" / "haipipe-norm"))
        break
from eventnorm import stress as stress_events  # noqa: E402
from eventnorm.stress.schema import BANDS, DIRECTION, RAW_TYPES  # noqa: E402

__version__ = "0.1.0"

app = FastAPI(title="stress event", version=__version__)

HEALTH_RAW = {"type": "readings", "end": "2026-11-09 10:10",
              "rows": [{"time": f"2026-11-09 10:{m:02d}", "value": v}
                       for m, v in ((0, 20), (1, 22), (2, 60), (3, -2), (4, -1), (6, 80))]}


@app.get("/healthz")
def healthz():
    """Real enough to mean something: ten typed minutes through the whole event, its six adding to 10."""
    try:
        h = stress_events.event(raw=HEALTH_RAW)["output"]["2026-11-09 10:00"]
        assert [h[f"{k}_min"] for k in ("rest", "low", "medium", "high", "active", "unknown")] == [2, 0, 1, 1, 1, 5]
    except Exception as e:
        raise HTTPException(503, f"stress event broken: {type(e).__name__}: {e}")
    return {"ok": True, "status": "ok", "version": __version__, "raw_types": sorted(RAW_TYPES),
            "bands": {name: [lo, hi] for name, lo, hi in BANDS}, "direction": DIRECTION}


class EventIn(BaseModel):
    raw: Optional[Dict[str, Any]] = Field(default=None, description='What arrives, as it arrives: {"type": "readings" | '
                                          '"day_score", "rows": [{...}, ...], "offset"?, "start"?, "end"?}')
    input: Optional[Dict[str, Any]] = Field(default=None, description='An input JSON: {"timeline": [{"from", "to", '
                                            '"level", "mean"}, ...]}, its minutes as stretches at one level')


@app.post("/event")
def stress_event(body: EventIn):
    """ONE stress event: the raw, the input JSON (its minutes as stretches at one level) the preprocess step makes of
    it, and the output by local hour: each hour's minutes rest, low, medium, high, active and unknown, with why
    unknown and the mean of its scored minutes. A day score stays its day."""
    try:
        ev = stress_events.event(raw=body.raw, input=body.input)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"event failed: {type(e).__name__}: {e}")
    return {**ev, "version": __version__}
