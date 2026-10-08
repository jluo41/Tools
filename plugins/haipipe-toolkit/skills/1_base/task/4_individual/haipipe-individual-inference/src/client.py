"""Thin HTTP client for a deployed CGM Endpoint_Set.

The caller supplies the payload shape declared by its deployed Src2Input /
Input2Src pair. Local wrappers use that same selected contract. This HTTP
client supports ordinary JSON endpoints; direct SageMaker Runtime invocation
requires its AWS SDK/SigV4 transport, not a bearer token.
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
    """POST platform-specific JSON payload → forecast dict.

    Args:
        payload: Endpoint_Set dataframe_records payload (see build_payload).
        endpoint_url: override URL (default: $CGM_ENDPOINT_URL).
        bearer_token: optional bearer auth for a compatible HTTP service.
    """
    url = endpoint_url or DEFAULT_URL
    headers = {"Content-Type": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    r = requests.post(url, json=payload, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.json()


def slice_last_window(forecast_resp: Dict[str, Any]) -> Dict[str, Any]:
    """Keep the last returned window according to the Endpoint ordering contract.

    This does not independently establish that its anchor is the latest CGM
    observation. Consumers must preserve that uncertainty unless the response
    provides verifiable window timestamps.
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
