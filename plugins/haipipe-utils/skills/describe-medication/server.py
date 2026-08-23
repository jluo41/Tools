"""
describe-medication over HTTP. Same contract as `from mednorm import normalize`,
reachable from anywhere by anything that can POST JSON.

    Tools/plugins/haipipe-utils/skills/describe-medication/run_server.sh
    curl -s localhost:8079/normalize -H 'content-type: application/json' \
         -d '{"item":"612997","dose":39}'

A consumer needs NO Python environment: a SourceFn, a notebook, a Databricks
job or a colleague's laptop calls a URL and nothing on their side imports this
package, pins its dependencies, or knows where the FDA file lives.

NOT AUTHENTICATED, bound to 127.0.0.1. Medication logs are PHI.
"""
import os
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mednorm import FIELDS, __version__, normalize
from mednorm.bank import stats
from mednorm.constants import BANK, LEXICON

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
    return {"ok": True, "version": __version__, "bank": str(BANK),
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
