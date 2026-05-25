"""Build an Endpoint_Set dataframe_records payload from a individual path.

Conforms to the contract documented in
  endpoint_cgm_patchtst_ohio_v0001/code/haifn/fn_endpoint/fn_input2src/
  CGMDecoder_DBR_Payload2Src_v260101.py (Format 1: dataframe_records).

Output shape:
  {
    "models": ["endpoint_cgm_patchtst_ohio/v0001"],
    "dataframe_records": [{
      "TriggerName_to_CaseTriggerList": {
        "CGM5MinEntry": [{"PatientID": ..., "ObsDT_UTC": ..., "TimezoneOffset": ...}]
      },
      "inference_form": {
        "ElogBGEntry": {"PatientID": [...], "ObservationDateTime": [...], "BGValue": [...]},
        "Patient":     {"PatientID": [...], "Gender": [...], ...},
        "PatientID":   <int_or_str>
      }
    }]
  }
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

from load_patient import load_patient_ctx

DEFAULT_MODEL = "endpoint_cgm_patchtst_ohio/v0001"
# Send the full available history; TrigFn (CGM5MinLTS) will scan it and pick
# the longest contiguous 5-min segment it can find. 288 = minimum for a 24h
# forecast input window; in practice we send much more to give LTS room.
DEFAULT_HISTORY_LEN = None


def _df_to_columnar(df: pd.DataFrame) -> dict:
    """JSON-safe column dict. Coerces NaN/NaT → None and dates → strings."""
    import math

    out: dict = {}
    for col in df.columns:
        v = df[col]
        if v.dtype.kind == "M":
            out[col] = [None if pd.isna(x) else x.strftime("%Y-%m-%d %H:%M:%S") for x in v]
            continue
        vals = v.tolist()
        clean = []
        for x in vals:
            if x is None:
                clean.append(None)
            elif isinstance(x, float) and math.isnan(x):
                clean.append(None)
            elif pd.isna(x):
                clean.append(None)
            else:
                clean.append(x)
        out[col] = clean
    return out


def build_payload(
    individual: str,
    *,
    history_len: int = DEFAULT_HISTORY_LEN,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Individual path/id → Endpoint_Set dataframe_records payload."""
    ctx = load_patient_ctx(individual, cgm_tail=history_len)
    cgm = ctx["tables"].get("CGM")
    if cgm is None or len(cgm) == 0:
        raise ValueError(f"No CGM data for individual {individual!r}")
    ptt = ctx["tables"].get("Ptt", pd.DataFrame())

    last = cgm.iloc[-1]
    trigger = {
        "PatientID": str(last["PatientID"]),
        "ObsDT_UTC": last["ObservationDateTime"].strftime("%m/%d/%Y %I:%M:%S %p"),
        "TimezoneOffset": int(last["TimezoneOffset"]) if "TimezoneOffset" in cgm.columns else 0,
    }

    inference_form = {
        "ElogBGEntry": _df_to_columnar(cgm),
        "PatientID": str(last["PatientID"]),
    }
    if len(ptt):
        inference_form["Patient"] = _df_to_columnar(ptt)

    return {
        "models": [model],
        "dataframe_records": [
            {
                "TriggerName_to_CaseTriggerList": {"CGM5MinEntry": [trigger]},
                "inference_form": inference_form,
            }
        ],
    }


def build_payload_summary(payload: dict) -> dict:
    """Compact view of a payload for logging."""
    rec = payload["dataframe_records"][0]
    trig = rec["TriggerName_to_CaseTriggerList"]["CGM5MinEntry"][0]
    elog = rec["inference_form"]["ElogBGEntry"]
    return {
        "models": payload["models"],
        "trigger": trig,
        "elog_n": len(elog.get("BGValue", [])),
        "has_patient": "Patient" in rec["inference_form"],
    }
