"""
describe-exercise over HTTP. The same contract as `from exnorm import normalize`,
reachable from anywhere, by anything that can POST JSON.

    Tools/plugins/haipipe-utils/servers/_host/run.sh
    curl -s localhost:8070/exercise/normalize -d '{"activity":"Walking","minutes":30,"weight_kg":82}' \
         -H 'content-type: application/json'

WHY A SERVICE AT ALL, when `local` is the default transport: so a consumer needs
NO Python environment. A SourceFn, a notebook, a Databricks job, or a colleague's
laptop calls a URL; nothing on their side imports this package, pins its
dependencies, or knows where the compendium lives. That is the whole point --
the resolver can move to another host and only EXNORM_URL changes.

NOT AUTHENTICATED, and bound to 127.0.0.1 by default. Exercise logs are PHI.
Before this listens on anything routable it needs auth in front of it.
"""
import os
import sys as _sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from exnorm import FIELDS, __version__, normalize
from exnorm.constants import DEFAULT_BANK
from exnorm.met_db import load

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):      # eventnorm, beside describe-exercise
    if (_base.parents[2] / "skills" / "haipipe-norm" / "eventnorm").is_dir():
        _sys.path.insert(0, str(_base.parents[2] / "skills" / "haipipe-norm"))
        break
from eventnorm import exercise as exercise_events  # noqa: E402

MAX_BATCH = int(os.environ.get("EXNORM_MAX_BATCH", "50000"))

app = FastAPI(title="describe-exercise", version=__version__)

Scalarish = Union[None, float, int, str, List]


class One(BaseModel):
    activity: str
    minutes: Optional[float] = None
    weight_kg: Optional[float] = None
    source_id: Optional[Union[int, str]] = None
    person_id: Optional[Union[int, str]] = None


class Batch(BaseModel):
    activities: List[str]
    minutes: Scalarish = None
    weight_kg: Scalarish = None
    source_ids: Scalarish = None
    person_ids: Scalarish = None


@app.get("/healthz")
def healthz():
    """Cheap enough to poll, real enough to mean something: it touches the bank,
    so a service whose compendium went missing reports unhealthy instead of
    failing on the first request."""
    try:
        n = len(load())
    except Exception as e:
        raise HTTPException(503, f"bank unavailable: {e}")
    return {"ok": True, "status": "ok", "version": __version__, "bank": str(DEFAULT_BANK),
            "activities": n, "fields": list(FIELDS)}


@app.post("/normalize")
def normalize_one(req: One):
    return normalize([req.activity], minutes=req.minutes,
                     weight_kg=req.weight_kg, source_ids=req.source_id,
                     person_ids=req.person_id, transport="local")[0]


@app.post("/normalize/batch")
def normalize_batch(req: Batch):
    if len(req.activities) > MAX_BATCH:
        raise HTTPException(413, f"{len(req.activities)} activities exceeds "
                                 f"EXNORM_MAX_BATCH={MAX_BATCH}")
    try:
        rows = normalize(req.activities, minutes=req.minutes,
                         weight_kg=req.weight_kg, source_ids=req.source_ids,
                         person_ids=req.person_ids, transport="local")
    except ValueError as e:
        # A length mismatch is the caller's error, not a 500.
        raise HTTPException(422, str(e))
    return {"count": len(rows), "results": rows}


class EventIn(BaseModel):
    raw: Optional[Dict[str, Any]] = Field(default=None, description='What arrives, as it arrives: {"type": '
                                          '"device_code" | "app_list" | "other" | "log" | "text" | "met_stream" | '
                                          '"steps_stream" | "named_stream" | ..., "rows": [{...}, ...]}')
    input: Optional[Dict[str, Any]] = Field(default=None, description='An input JSON, or the fields of it to set: '
                                            '{"start", "end", "total", "items": [{"activity", "met"?}], "timeline"}')


@app.post("/event")
def exercise_event(body: EventIn):
    """ONE exercise event (b51 s12; JL 261022: "就是你要 follow 他，然后做一下跟他一样的事情", as POST /food/event): the
    raw, the input JSON the preprocess step makes of it, and the output by local hour, each hour its own part (s02-D23),
    its one item described by describe-exercise (words and minutes only) or by the MET its device gives."""
    try:
        ev = exercise_events.event(raw=body.raw, input=body.input)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"event failed: {type(e).__name__}: {e}")
    return {**ev, "version": __version__}
