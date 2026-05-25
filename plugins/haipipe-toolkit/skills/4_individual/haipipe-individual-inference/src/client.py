"""Thin HTTP client for a deployed CGM Endpoint_Set.

Backend-agnostic: same call works against the local FastAPI server
(today), a Databricks Model Serving endpoint, or a SageMaker invoke
endpoint — they all consume the same dataframe_records payload.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

DEFAULT_URL = os.environ.get("CGM_ENDPOINT_URL", "http://127.0.0.1:8765/invocations")
DEFAULT_TIMEOUT = int(os.environ.get("CGM_ENDPOINT_TIMEOUT", "60"))


def call_predict(
    payload: Dict[str, Any],
    *,
    endpoint_url: Optional[str] = None,
    bearer_token: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """POST dataframe_records payload → forecast dict.

    Args:
        payload: Endpoint_Set dataframe_records payload (see build_payload).
        endpoint_url: override URL (default: $CGM_ENDPOINT_URL).
        bearer_token: optional auth header (Databricks/SageMaker tokens).
    """
    url = endpoint_url or DEFAULT_URL
    headers = {"Content-Type": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    r = requests.post(url, json=payload, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.json()


def slice_last_window(forecast_resp: Dict[str, Any]) -> Dict[str, Any]:
    """Return a response with only the most recent forecast window kept.

    The endpoint's TrigFn (CGM5MinLTS) emits one forecast per valid 288-step
    contiguous segment in the input — for backtesting use cases this is up
    to 45 windows. For live "next 2 hours" inference we only care about the
    last one (anchored at the most recent CGM observation).

    Slicing client-side rather than constraining the endpoint avoids the
    Record-stage timestamp normalization that drops fragile single-window
    payloads on real-world (jittery) CGM data.
    """
    out = dict(forecast_resp)
    models = out.get("models") or []
    sliced = []
    for m in models:
        m2 = dict(m)
        fc = m2.get("forecast") or []
        if fc:
            last = fc[-1]
            m2["forecast"] = [last]
            # Endpoint's PostFn mislabels window-count as horizonSteps.
            # Replace with actual per-window horizon length.
            md = dict(m2.get("metadata") or {})
            y = last.get("y_pred_h24") or []
            md["horizonSteps"] = len(y)
            m2["metadata"] = md
        sliced.append(m2)
    out["models"] = sliced
    return out
