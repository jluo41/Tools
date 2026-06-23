"""Local FastAPI deployment for any haipipe Endpoint_Set.

Wraps `Endpoint_Set.inference()` behind a SageMaker-style HTTP surface so an
agent / client / smoke test can hit a local endpoint with the same wire
contract Databricks Model Serving and SageMaker would consume.

Backend axis (haipipe-end deploy targets) — same contract everywhere:
    local       → this script (Flask/FastAPI)
    databricks  → haipipe-end-deploy-databricks
    sagemaker   → haipipe-end-deploy-sagemaker
    mlflow      → haipipe-end-deploy-mlflow

Run:
    ENDPOINT_PATH=_WorkSpace/6-EndpointStore/<endpoint_name>  python serve_local.py
    PORT=8765  python serve_local.py
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from haipipe.endpoint_base import Endpoint_Set

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("haipipe-end-deploy-local")

WORKSPACE_ROOT = Path(os.environ.get("WORKSPACE_PATH", "/home/jluo41/WellDoc-SPACE"))
ENDPOINT_PATH = Path(
    os.environ.get(
        "ENDPOINT_PATH",
        WORKSPACE_ROOT / "_WorkSpace/6-EndpointStore/endpoint_cgm_patchtst_ohio_v0001",
    )
)

app = FastAPI(title="haipipe-endpoint-local", version="0.1.0")

_ep: Optional[Endpoint_Set] = None
_endpoint_loaded_ok = False


def _load_endpoint() -> Endpoint_Set:
    global _ep, _endpoint_loaded_ok
    if _ep is None:
        SPACE = os.environ.copy()
        SPACE["WORKSPACE_PATH"] = str(WORKSPACE_ROOT)
        _ep = Endpoint_Set.load_from_disk(path=str(ENDPOINT_PATH), SPACE=SPACE)
        _endpoint_loaded_ok = True
        log.info("Endpoint loaded: %s/%s", _ep.endpoint_name, _ep.endpoint_version)
    return _ep


@app.on_event("startup")
def _startup() -> None:
    try:
        _load_endpoint()
    except Exception as e:
        log.warning("Endpoint load failed at startup: %s", e)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "haipipe-endpoint-local",
        "endpoint_path": str(ENDPOINT_PATH),
        "endpoint_loaded": _endpoint_loaded_ok,
    }


@app.get("/meta")
def meta() -> Dict[str, Any]:
    """SageMaker-convention metadata route."""
    ep = _load_endpoint()
    body = (ep.meta_results or {}).get("metadata_response", {}).get("body", {})
    return body or {
        "endpoint_name": ep.endpoint_name,
        "endpoint_version": ep.endpoint_version,
    }


@app.post("/invocations")
def invocations(payload: Dict[str, Any]) -> JSONResponse:
    """SageMaker-convention inference route. Accepts the Endpoint_Set's
    documented payload shape (typically `dataframe_records`)."""
    ep = _load_endpoint()
    try:
        resp = ep.inference(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"inference failed: {e!r}")

    if isinstance(resp, tuple):
        body = resp[0]
        code = resp[2] if len(resp) >= 3 else 200
    else:
        body, code = resp, 200
    return JSONResponse(content=body, status_code=code)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8765)))
