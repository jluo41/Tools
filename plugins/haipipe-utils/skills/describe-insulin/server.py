"""
describe-insulin over HTTP.

    Tools/plugins/haipipe-utils/skills/describe-insulin/run_server.sh
    curl -s localhost:8080/normalize -H 'content-type: application/json' \
         -d '{"item":"Insulin lispro-aabc"}'
    curl -s localhost:8080/normalize -H 'content-type: application/json' \
         -d '{"item":"basal insulin","dia_hours":7.0}'
         -d '{"item":"Novolin R","delivery":"iv"}'

Its input is describe-medication's `DrugKey`. See insnorm/__init__.py for why
the two are a chain and not siblings.
"""
import os
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from insnorm import FIELDS, __version__, normalize
from insnorm.pk_table import ALIASES, COMBINATIONS, PK

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
