"""
describe-exercise over HTTP. The same contract as `from exnorm import normalize`,
reachable from anywhere, by anything that can POST JSON.

    Tools/plugins/haipipe-utils/skills/describe-exercise/run_server.sh
    curl -s localhost:8078/normalize -d '{"activity":"Walking","minutes":30,"weight_kg":82}' \
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
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from exnorm import FIELDS, __version__, normalize
from exnorm.constants import DEFAULT_BANK
from exnorm.met_db import load

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
    return {"ok": True, "version": __version__, "bank": str(DEFAULT_BANK),
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
