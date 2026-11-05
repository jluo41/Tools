"""
describe-medication over HTTP. Same contract as `from mednorm import normalize`,
reachable from anywhere by anything that can POST JSON.

    Tools/plugins/haipipe-utils/servers/_host/run.sh
    curl -s localhost:8070/medication/normalize -H 'content-type: application/json' \
         -d '{"item":"612997","dose":39}'

A consumer needs NO Python environment: a SourceFn, a notebook, a Databricks
job or a colleague's laptop calls a URL and nothing on their side imports this
package, pins its dependencies, or knows where the FDA file lives.

NOT AUTHENTICATED, bound to 127.0.0.1. Medication logs are PHI.
"""
import os
import sys as _sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from mednorm import FIELDS, __version__, normalize
from mednorm.bank import stats
from mednorm.constants import BANK, LEXICON

for _base in (Path(__file__).absolute(), Path(__file__).resolve()):      # eventnorm, beside describe-medication
    if (_base.parents[2] / "skills" / "haipipe-norm" / "eventnorm").is_dir():
        _sys.path.insert(0, str(_base.parents[2] / "skills" / "haipipe-norm"))
        break
from eventnorm import medication as medication_events  # noqa: E402

MAX_BATCH = int(os.environ.get("MEDNORM_MAX_BATCH", "50000"))
app = FastAPI(title="describe-medication", version=__version__)
Scalarish = Union[None, float, int, str, List]


class One(BaseModel):
    item: str
    dose: Optional[float] = None
    payload: Optional[str] = None


class Batch(BaseModel):
    items: List[str]
    doses: Scalarish = None
    payloads: Scalarish = None


@app.get("/healthz")
def healthz():
    """Touches both reference files, so a service whose bank went missing
    reports unhealthy instead of failing on the first request."""
    try:
        s = stats()
    except Exception as e:
        raise HTTPException(503, f"bank unavailable: {e}")
    return {"ok": True, "status": "ok", "version": __version__, "bank": str(BANK),
            "lexicon": str(LEXICON), "counts": s, "fields": list(FIELDS)}


@app.post("/normalize")
def normalize_one(req: One):
    return normalize([req.item], doses=req.dose, payloads=req.payload,
                     transport="local")[0]


@app.post("/normalize/batch")
def normalize_batch(req: Batch):
    if len(req.items) > MAX_BATCH:
        raise HTTPException(413, f"{len(req.items)} items exceeds "
                                 f"MEDNORM_MAX_BATCH={MAX_BATCH}")
    try:
        rows = normalize(req.items, doses=req.doses, payloads=req.payloads,
                         transport="local")
    except ValueError as e:
        raise HTTPException(422, str(e))
    return {"count": len(rows), "results": rows}


class EventIn(BaseModel):
    raw: Optional[Dict[str, Any]] = Field(default=None, description='What arrives, as it arrives: {"type": '
                                          '"app_id" | "text" | "pump" | "class_word", "rows": [{...one row...}]}')
    input: Optional[Dict[str, Any]] = Field(default=None, description='An input JSON, or the fields of it to set: '
                                            '{"start", "end", "logged_at", "items": [{"drug", "ndc"?, "dose"?, '
                                            '"unit"?, "delivery"?}]}')


@app.post("/event")
def medication_event(body: EventIn):
    """ONE medication event (b51 s13; JL 261027: "啊 整去整吧", as POST /meal/event and /exercise/event): the raw, the
    input JSON the preprocess step makes of it (a WellDoc id named through WellDoc's catalog, a cell split into its
    drugs, a pump cell's drug from its header), and the output by local hour, each item described by
    describe-medication; a dose is a moment, so its start's hour holds it all."""
    try:
        ev = medication_events.event(raw=body.raw, input=body.input)
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"event failed: {type(e).__name__}: {e}")
    return {**ev, "version": __version__}
