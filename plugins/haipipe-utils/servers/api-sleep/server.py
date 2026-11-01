"""
The sleep event over HTTP: the same contract as `from eventnorm.sleep import event`, reachable by anything that can
POST JSON (b51 s06, s16; JL 261027: "send the message to other sessions to ask them to build their own page
accordingly").

    Tools/plugins/haipipe-utils/servers/_host/run.sh
    curl -s localhost:8070/sleep/event -H 'content-type: application/json' \\
         -d '{"input": {"start": "2023-01-23 02:00 -05:00", "end": "2023-01-23 06:00 -05:00",
                        "timeline": [{"from": "02:30", "to": "05:30", "state": "asleep"}]}}'

ONE DOOR, NO /normalize. Sleep has nothing to look up (items: null, s06-D05), so this lane has only POST /event, as
step's, and no describe-sleep skill: the host loads it without one. Each local hour keeps its own minutes in bed,
asleep and awake in bed; a night with no pieces keeps them as unknown.

NOT AUTHENTICATED, and bound to 127.0.0.1 by default. Sleep logs are PHI. Before this listens on anything routable it
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
from eventnorm import sleep as sleep_events  # noqa: E402
from eventnorm.sleep.schema import RAW_TYPES  # noqa: E402

__version__ = "0.1.0"

app = FastAPI(title="sleep event", version=__version__)


@app.get("/healthz")
def healthz():
    """Real enough to mean something: JL's night (asleep 02:30 to 05:30) through the whole event."""
    try:
        ev = sleep_events.event(input={"start": "2023-01-23 02:00 -05:00", "end": "2023-01-23 06:00 -05:00",
                                       "timeline": [{"from": "02:30", "to": "05:30", "state": "asleep"}]})
        assert len(ev["output"]) == 4
    except Exception as e:
        raise HTTPException(503, f"sleep event broken: {type(e).__name__}: {e}")
    from eventnorm.step.preprocess import devices
    return {"ok": True, "status": "ok", "version": __version__, "raw_types": sorted(RAW_TYPES),
            "devices": len(devices())}


class EventIn(BaseModel):
    raw: Optional[Dict[str, Any]] = Field(default=None, description='What arrives, as it arrives: {"type": "log", '
                                          '"rows": [{...}, ...], "pieces"?: [{"StartDateTime", "EndDateTime"}, ...]}')
    input: Optional[Dict[str, Any]] = Field(default=None, description='An input JSON, or the fields of it to set: '
                                            '{"start", "end", "device", "timeline": [{"from", "to", "state"}]}')


@app.post("/event")
def sleep_event(body: EventIn):
    """ONE sleep event: the raw, the input JSON the preprocess step makes of it (the night, its stretches asleep), and
    the output by local hour (each hour its own minutes in bed, asleep and awake in bed, or unknown)."""
    try:
        ev = sleep_events.event(raw=body.raw, input=body.input)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"event failed: {type(e).__name__}: {e}")
    return {**ev, "version": __version__}
