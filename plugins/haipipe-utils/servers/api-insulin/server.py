"""
describe-insulin over HTTP.

    Tools/plugins/haipipe-utils/servers/_host/run.sh
    curl -s localhost:8070/insulin/normalize -H 'content-type: application/json' \
         -d '{"item":"Insulin lispro-aabc"}'
    curl -s localhost:8070/insulin/normalize -H 'content-type: application/json' \
         -d '{"item":"basal insulin","dia_hours":7.0}'
         -d '{"item":"Novolin R","delivery":"iv"}'

Its input is describe-medication's `DrugKey`. See insnorm/__init__.py for why
the two are a chain and not siblings.
"""
import os
import sys as _sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from insnorm import FIELDS, __version__, normalize
from insnorm.pk_table import ALIASES, COMBINATIONS, PK

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):      # eventnorm, beside describe-insulin
    if (_base.parents[2] / "skills" / "haipipe-norm" / "eventnorm").is_dir():
        _sys.path.insert(0, str(_base.parents[2] / "skills" / "haipipe-norm"))
        break
from eventnorm import insulin as insulin_events  # noqa: E402

MAX_BATCH = int(os.environ.get("INSNORM_MAX_BATCH", "50000"))
app = FastAPI(title="describe-insulin", version=__version__)
Scalarish = Union[None, float, int, str, List]


class One(BaseModel):
    item: str
    dia_hours: Optional[float] = None
    # The route the LOG stated. Optional, and the HTTP door must accept it or
    # the two transports answer differently for the same row -- which is the
    # one thing a transport switch may never do.
    delivery: Optional[str] = None
    # The log's own string beside the seam. Used only where it resolves to a
    # strictly more specific key -- a premix ratio or a concentration the
    # upstream bank stripped.
    raw: Optional[str] = None


class Batch(BaseModel):
    items: List[str]
    dia_hours: Scalarish = None
    delivery: Scalarish = None
    raw: Scalarish = None


@app.get("/healthz")
def healthz():
    return {"ok": True, "version": __version__,
            "products": len(PK), "aliases": len(ALIASES),
            "combinations": len(COMBINATIONS), "fields": list(FIELDS)}


@app.post("/normalize")
def normalize_one(req: One):
    return normalize([req.item], dia_hours=req.dia_hours,
                     delivery=req.delivery, raw=req.raw, transport="local")[0]


@app.post("/normalize/batch")
def normalize_batch(req: Batch):
    if len(req.items) > MAX_BATCH:
        raise HTTPException(413, f"{len(req.items)} items exceeds "
                                 f"INSNORM_MAX_BATCH={MAX_BATCH}")
    try:
        rows = normalize(req.items, dia_hours=req.dia_hours,
                         delivery=req.delivery, raw=req.raw, transport="local")
    except ValueError as e:
        raise HTTPException(422, str(e))
    return {"count": len(rows), "results": rows}


class EventIn(BaseModel):
    raw: Optional[Dict[str, Any]] = Field(default=None, description='What arrives, as it arrives: {"type": '
                                          '"app_id" | "text" | "pump" | "class_word", "rows": [{...one row...}]}')
    input: Optional[Dict[str, Any]] = Field(default=None, description='An input JSON, or the fields of it to set: '
                                            '{"start", "end", "logged_at", "items": [{"drug", "ndc"?, "dose"?, '
                                            '"unit"?, "delivery"?}]}')
    dia_hours: Optional[float] = Field(default=None, description="the person's duration of insulin action, hours: "
                                       "it ends a curve")


@app.post("/event")
def insulin_event(body: EventIn):
    """ONE insulin event (b51 s14; JL 261027, as POST /medication/event): the raw, the input JSON medication's
    preprocess step makes of it, and the output by local hour: each drug asked of the insulin chain (describe-medication,
    then describe-insulin), a dose spread by its curve, a pump rate by its minutes, as j04 t03 froze ext_insulin_event."""
    try:
        ev = insulin_events.event(raw=body.raw, input=body.input, dia_hours=body.dia_hours)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"event failed: {type(e).__name__}: {e}")
    return {**ev, "version": __version__}
