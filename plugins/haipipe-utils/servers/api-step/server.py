"""
The step event over HTTP: the same contract as `from eventnorm.step import event`, reachable by anything that can
POST JSON (b51 s15-D03; JL 261027: "你继续去弄啊").

    Tools/plugins/haipipe-utils/servers/_host/run.sh
    curl -s localhost:8070/step/event -H 'content-type: application/json' \\
         -d '{"input": {"start": "2022-06-29 16:56 -05:00", "end": "2022-06-29 17:24 -05:00", "total": {"steps": 128}}}'

ONE DOOR, NO /normalize. Food, exercise, medication and insulin look words up in a reference bank; a step count has no
words, so this lane has only POST /event (as s12-D08 dropped exercise's /normalize) and no describe-step skill: the
host loads it without one. A stream's brisk runs (100 steps a minute for 10 minutes, exercise's own runs_of) come
back as "walks", each to be sent to POST /exercise/event.

NOT AUTHENTICATED, and bound to 127.0.0.1 by default. Step logs are PHI. Before this listens on anything routable it
needs auth in front of it.
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
from eventnorm import step as step_events  # noqa: E402
from eventnorm.step.schema import RAW_TYPES  # noqa: E402

__version__ = "0.1.0"

app = FastAPI(title="step event", version=__version__)


@app.get("/healthz")
def healthz():
    """Real enough to mean something: one logged row through the whole event, and the device dictionary read."""
    try:
        ev = step_events.event(input={"start": "2022-06-29 16:56 -05:00", "end": "2022-06-29 17:24 -05:00",
                                      "total": {"steps": 128}})
        assert len(ev["output"]) == 2
    except Exception as e:
        raise HTTPException(503, f"step event broken: {type(e).__name__}: {e}")
    from eventnorm.step.preprocess import devices
    return {"ok": True, "status": "ok", "version": __version__, "raw_types": sorted(RAW_TYPES),
            "devices": len(devices())}


class EventIn(BaseModel):
    raw: Optional[Dict[str, Any]] = Field(default=None, description='What arrives, as it arrives: {"type": "log" | '
                                          '"steps_stream", "rows": [{...}, ...], "zone"?, "device"?}')
    input: Optional[Dict[str, Any]] = Field(default=None, description='An input JSON, or the fields of it to set: '
                                            '{"start", "end", "device", "total": {"steps", ...}}')


@app.post("/event")
def step_event(body: EventIn):
    """ONE step event: the raw, the input JSON the preprocess step makes of it, and the output by local hour (a logged
    row: each hour its share to the second and its own minutes and steps; a whole day stays its day; a stream: each
    hour its own samples, and its walks for POST /exercise/event)."""
    try:
        ev = step_events.event(raw=body.raw, input=body.input)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"event failed: {type(e).__name__}: {e}")
    return {**ev, "version": __version__}
