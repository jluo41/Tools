"""
describe-food as a SERVICE. The consumer holds a URL, not an import.

    uvicorn server:app --host 0.0.0.0 --port 8077
    curl -s localhost:8077/healthz

Why this exists. A pipeline that does `from foodnorm import normalize` needs the
resolver's package on its PYTHONPATH, which means every consumer must share this
repository's Python environment. Behind a URL it needs none of that: the bank,
the dialect layer, the stage sequence and the interpreter live on this side of
the wire, and a consumer needs an HTTP client and an address. The service can
then run anywhere -- this box, another host, a container, a managed endpoint --
and no consumer changes when it moves.

THE CONTRACT IS THE SAME ONE `normalize()` HAS, deliberately: one result per
input, in input order, carrying its own provenance. A caller must be able to
swap transport without re-reading the response shape.

    POST /normalize/batch  {"foods": ["fried rice; egg", ...]}
        -> {"results": [ {...}, ... ], "n": 2, "version": "0.4.0"}
    POST /normalize        {"food": "fried rice; egg"}   -> one object
    GET  /healthz          the bank it is actually serving, so a caller can tell
                           WHICH corpus answered before trusting a number
"""
import base64
import binascii
import math
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from foodnorm import NUTRIENTS, PROVENANCE, enrich_food_to_nutrition, normalize
from foodnorm import observed as _observed
from foodnorm.constants import USDA_DB

VERSION = "0.4.0"
# One batch is one cook's worth of DISTINCT strings. Shanghai's 71k rows carry
# ~3,130 of them, so the cap is a runaway guard and not a working limit.
MAX_BATCH = int(os.environ.get("FOODNORM_MAX_BATCH", "20000"))

# Image limits. A meal is one or two frames (a plate, or the before/after pair),
# so the count cap is small on purpose: a large upload here is a mistake, not a
# meal.
MAX_IMAGES = int(os.environ.get("FOODNORM_MAX_IMAGES", "4"))
MAX_IMAGE_BYTES = int(os.environ.get("FOODNORM_MAX_IMAGE_BYTES", str(16 * 1024 * 1024)))
IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic"}
# An image route with the null engine would always answer MISS, so this route
# defaults to reading the image. Overridable per request.
DEFAULT_IMAGE_ENGINE = os.environ.get("FOODNORM_IMAGE_ENGINE_HTTP", "claude")

app = FastAPI(title="describe-food", version=VERSION,
              description="Free-text food, in any cohort's dialect, to USDA nutrition with provenance.")


class BatchIn(BaseModel):
    foods: List[str] = Field(..., description="Food strings, any dialect. Duplicates are fine.")
    options: Optional[Dict[str, Any]] = Field(default=None,
                                              description="Passed to the resolver, e.g. {'stages': '1-2'}")


class OneIn(BaseModel):
    food: str
    options: Optional[Dict[str, Any]] = None


def _jsonable(rows: List[Dict]) -> List[Dict]:
    """NaN is not JSON. pandas hands back float('nan') where a value is absent,
    and `json.dumps` emits a bare `NaN` token that strict parsers reject -- so a
    MISS would arrive as a parse error rather than as a MISS. Every absent value
    crosses the wire as null."""
    out = []
    for r in rows:
        clean = {}
        for k, v in r.items():
            if isinstance(v, float) and math.isnan(v):
                clean[k] = None
            elif hasattr(v, "item"):          # numpy scalar
                clean[k] = v.item()
            else:
                clean[k] = v
        out.append(clean)
    return out


@app.on_event("startup")
def _warm():
    """Resolve one string at startup so the first real request does not pay for
    opening the bank and building its FTS cursor. A cook's first call should not
    be its slowest."""
    try:
        normalize(["rice"])
        print(f"[describe-food {VERSION}] warm · bank={USDA_DB}")
    except Exception as e:                     # a cold bank is worth saying out loud
        print(f"[describe-food {VERSION}] WARMUP FAILED: {e}")


@app.get("/healthz")
def healthz():
    """What a caller needs to know before trusting a number: which corpus
    answered. Two banks sit on this machine and they disagree on the same cell."""
    ok = USDA_DB.exists()
    info = {"status": "ok" if ok else "degraded", "version": VERSION,
            "bank": str(USDA_DB), "bank_exists": ok, "max_batch": MAX_BATCH}
    # T0 of the bank ladder, reported beside the USDA bank: a deployment that is
    # missing it silently degrades every answer from MEASURED to ESTIMATED, and
    # that has to be visible from OUTSIDE the process.
    info["observed_bank"] = str(_observed.DEFAULT_BANK)
    info["observed_entries"] = _observed.size()
    info["conf_values"] = ["MEASURED", "ESTIMATED", "MISS"]
    if ok:
        try:
            import sqlite3
            with sqlite3.connect(f"file:{USDA_DB}?mode=ro", uri=True) as c:
                info["bank_rows"] = c.execute("SELECT count(*) FROM food").fetchone()[0]
        except Exception as e:
            info["bank_rows"] = f"unreadable: {e}"
    return info


@app.post("/normalize/batch")
def normalize_batch(body: BatchIn):
    if len(body.foods) > MAX_BATCH:
        raise HTTPException(413, f"{len(body.foods)} strings exceeds FOODNORM_MAX_BATCH={MAX_BATCH}")
    try:
        rows = normalize(body.foods, **(body.options or {}))
    except Exception as e:
        # Fail loud. A resolver that returns nothing silently is how a SourceSet
        # once shipped with 100% NULL nutrition and nobody noticed.
        raise HTTPException(500, f"resolver failed: {type(e).__name__}: {e}")
    return {"results": _jsonable(rows), "n": len(rows), "version": VERSION}


@app.post("/normalize")
def normalize_one(body: OneIn):
    rows = normalize([body.food], **(body.options or {}))
    return _jsonable(rows)[0]


# ── the image lane, over the wire ───────────────────────────────────────────
#
# THE CONSTRAINT THAT SHAPES THIS ROUTE: a caller must not need to share a
# filesystem with the service. Stage 0 reads image PATHS -- it hands them to a
# vision model that opens them itself -- so a route taking {"image_path": "/x"}
# would work only while caller and service sit on one machine, and would also
# let a caller point the service at any file it likes. So the BYTES cross the
# wire, the service writes them to its OWN temp directory, and stage 0 reads
# paths that the service alone created and deletes.
#
# ⚠️ These frames are PHI. The route holds them only for the length of one
# request, writes them nowhere else, and logs no filename. Authentication is NOT
# solved here: bind the service to localhost, or put a gate in front of it,
# before this route is reachable from a network.

def _one_meal(paths: List[str], engine: str) -> Dict:
    """Resolve ONE meal's frames. Reuses enrich_food_to_nutrition rather than
    re-deriving the provenance columns, so `NameSource`, `NameConf` and the
    `bank_usda|img:` tag keep exactly one owner."""
    df = pd.DataFrame({"FoodName": ["Unknown"], "ImagePath": [",".join(paths)]})
    out = enrich_food_to_nutrition(df, food_col="FoodName", image_col="ImagePath",
                                   image_engine=engine, image_root=None)
    cols = list(NUTRIENTS) + list(PROVENANCE) + ["NameSource", "NameConf", "FoodNameResolved"]
    return _jsonable(out[[c for c in cols if c in out.columns]].to_dict("records"))[0]


def _stage(tmp: str, name: str, data: bytes, idx: int) -> str:
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, f"image {idx} is {len(data)} bytes, over "
                                 f"FOODNORM_MAX_IMAGE_BYTES={MAX_IMAGE_BYTES}")
    if not data:
        raise HTTPException(422, f"image {idx} is empty")
    suffix = Path(name or "").suffix or ".jpg"
    path = os.path.join(tmp, f"{idx:02d}{suffix}")
    with open(path, "wb") as f:
        f.write(data)
    return path


@app.post("/normalize/image")
async def normalize_image(files: List[UploadFile] = File(...),
                          engine: str = Form(default=None)):
    """ONE meal, as uploaded frames. Two frames are read as the same meal
    photographed before and after eating, which is how CGMacros logs one.

        curl -F files=@before.jpg -F files=@after.jpg \\
             http://127.0.0.1:8077/normalize/image
    """
    if not files:
        raise HTTPException(422, "no files")
    if len(files) > MAX_IMAGES:
        raise HTTPException(413, f"{len(files)} frames exceeds FOODNORM_MAX_IMAGES={MAX_IMAGES}; "
                                 "one meal is one or two frames")
    for i, f in enumerate(files):
        if f.content_type and f.content_type.lower() not in IMAGE_TYPES:
            raise HTTPException(415, f"file {i} is {f.content_type}; want one of {sorted(IMAGE_TYPES)}")

    with tempfile.TemporaryDirectory(prefix="foodnorm-upload-") as tmp:
        paths = [_stage(tmp, f.filename, await f.read(), i) for i, f in enumerate(files)]
        try:
            row = _one_meal(paths, engine or DEFAULT_IMAGE_ENGINE)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(500, f"image resolver failed: {type(e).__name__}: {e}")
    return {"result": row, "n_frames": len(paths),
            "engine": engine or DEFAULT_IMAGE_ENGINE, "version": VERSION}


class ImageBatchIn(BaseModel):
    meals: List[List[str]] = Field(..., description="One entry per meal; each a list of base64 frames.")
    engine: Optional[str] = None


@app.post("/normalize/image/batch")
def normalize_image_batch(body: ImageBatchIn):
    """Many meals in one call, frames base64-encoded. multipart cannot express
    'these two frames are one meal and those three are another', and a cook has
    thousands of meals, so the batch form is JSON."""
    if not body.meals:
        return {"results": [], "n": 0, "version": VERSION}
    if len(body.meals) > MAX_BATCH:
        raise HTTPException(413, f"{len(body.meals)} meals exceeds FOODNORM_MAX_BATCH={MAX_BATCH}")

    engine = body.engine or DEFAULT_IMAGE_ENGINE
    results = []
    with tempfile.TemporaryDirectory(prefix="foodnorm-upload-") as tmp:
        for mi, frames in enumerate(body.meals):
            if not frames or len(frames) > MAX_IMAGES:
                raise HTTPException(413, f"meal {mi} has {len(frames)} frames; "
                                         f"want 1..{MAX_IMAGES}")
            paths = []
            for fi, b64 in enumerate(frames):
                try:
                    data = base64.b64decode(b64, validate=True)
                except (binascii.Error, ValueError) as e:
                    raise HTTPException(422, f"meal {mi} frame {fi} is not valid base64: {e}")
                paths.append(_stage(tmp, f"m{mi}f{fi}.jpg", data, fi))
            try:
                results.append(_one_meal(paths, engine))
            except Exception as e:
                raise HTTPException(500, f"meal {mi}: {type(e).__name__}: {e}")
    return {"results": results, "n": len(results), "engine": engine, "version": VERSION}
