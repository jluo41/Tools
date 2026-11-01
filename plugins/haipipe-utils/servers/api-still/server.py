"""
The still event over HTTP: the same contract as `from eventnorm.still import event`, reachable by anything that can
POST JSON (b51 s17; JL 261027: every event type its own tab of the try page, as food's).

    Tools/plugins/haipipe-utils/servers/_host/run.sh
    curl -s localhost:8070/still/event -H 'content-type: application/json' \\
         -d '{"raw": {"type": "minutes", "day": "2026-10-27", "rows": [{"from": "10:00", "to": "10:40", "bpm": 72}]}}'

ONE DOOR, NO /normalize. A minute has no words to look up, so this lane has only POST /event, as step's, and no
describe-still skill: the host loads it without one. Each hour's minutes come back four ways (asleep, moving, still,
unknown); how few steps make a worn, awake minute still is not decided yet (s17 Open 1), so the rule is 0 steps until
j07's rule Task, and a request may send its own as still_max_steps.

NOT AUTHENTICATED, and bound to 127.0.0.1 by default. Heart rate, steps and sleep are PHI. Before this listens on
anything routable it needs auth in front of it.
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
from eventnorm import still as still_events  # noqa: E402
from eventnorm.still.schema import RAW_TYPES, STILL_MAX_STEPS  # noqa: E402

__version__ = "0.1.0"

app = FastAPI(title="still event", version=__version__)

HEALTH_RAW = {"type": "minutes", "day": "2026-10-27",
              "rows": [{"from": "10:00", "to": "10:40", "bpm": 72, "steps": 0},
                       {"from": "10:40", "to": "10:50", "bpm": 95, "steps": 80}, {"from": "10:50", "to": "11:00"}]}


@app.get("/healthz")
def healthz():
    """Real enough to mean something: one typed hour through the whole event, its four adding to 60."""
    try:
        h = still_events.event(raw=HEALTH_RAW)["output"]["2026-10-27 10:00"]
        assert (h["still_min"], h["moving_min"], h["unknown_min"]) == (40, 10, 10)
    except Exception as e:
        raise HTTPException(503, f"still event broken: {type(e).__name__}: {e}")
    return {"ok": True, "status": "ok", "version": __version__, "raw_types": sorted(RAW_TYPES),
            "still_max_steps": STILL_MAX_STEPS}


class EventIn(BaseModel):
    raw: Optional[Dict[str, Any]] = Field(default=None, description='What arrives, as it arrives: {"type": "minutes" | '
                                          '"mcphases", "rows": [{...}, ...], "day"?, "start"?, "end"?}')
    input: Optional[Dict[str, Any]] = Field(default=None, description='An input JSON: {"timeline": [{"from", "to", '
                                            '"steps", "worn", "level"}, ...]}, its minutes as stretches')
    still_max_steps: Optional[int] = Field(default=None, ge=0, description="the most steps a still minute may hold; "
                                           f"{STILL_MAX_STEPS} until j07's rule Task")


@app.post("/event")
def still_event(body: EventIn):
    """ONE still event: the raw, the input JSON (its minutes) the preprocess step makes of it, and the output by local
    hour: each hour's minutes asleep, moving, still and unknown, with why unknown."""
    try:
        ev = still_events.event(raw=body.raw, input=body.input, still_max_steps=body.still_max_steps)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"event failed: {type(e).__name__}: {e}")
    return {**ev, "version": __version__}
