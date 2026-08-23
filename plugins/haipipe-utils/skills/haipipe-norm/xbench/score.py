"""
Metric primitives. Everything here is noun-agnostic on purpose: the moment a
function needs to know what the number MEANS, it belongs in the noun's metric.
"""
import numpy as np
import pandas as pd

MISS = "MISS"
MIN_TO_CORRELATE = 10   # below this a Pearson r is noise wearing a decimal point


def basics(df: pd.DataFrame, spec) -> dict:
    """The Q1 half: how much came back, and how confident. No gold involved."""
    conf = df[spec.conf_col]
    out = {
        "n": int(len(df)),
        "n_unique_input": int(df[spec.text_col].nunique()),
        "coverage": round(float((conf != MISS).mean()), 4) if len(df) else None,
        "conf": {str(k): int(v) for k, v in conf.value_counts().items()},
    }
    if spec.basis_col and spec.basis_col in df.columns:
        out["basis"] = {str(k): int(v)
                        for k, v in df[spec.basis_col].dropna().value_counts().items()}
    return out


def mae_r(true, pred):
    """Two aligned series -> (MAE, Pearson r, n). (None, None, n) if too few.

    Returns n even when it will not quote a correlation, because "we scored 3
    rows" and "we scored 3,000" are different claims and a bare null hides it.
    """
    t = pd.to_numeric(pd.Series(true), errors="coerce")
    p = pd.to_numeric(pd.Series(pred), errors="coerce")
    ok = t.notna() & p.notna()
    t, p = t[ok], p[ok]
    if len(t) < MIN_TO_CORRELATE:
        return None, None, int(len(t))
    if t.std() == 0 or p.std() == 0:
        # A constant column makes r undefined, not zero. Saying 0.0 here would
        # read as "no relationship measured" when nothing was measurable.
        return round(float((t - p).abs().mean()), 2), None, int(len(t))
    return (round(float((t - p).abs().mean()), 2),
            round(float(np.corrcoef(t, p)[0, 1]), 3),
            int(len(t)))
