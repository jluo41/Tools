"""
This run against a frozen baseline. The regression guard.

A benchmark you only ever read forwards tells you where you are; it does not
tell you that you broke something. Every number here is compared cell by cell
and weighting by weighting, and a DROP is reported even when the headline moved
the right way -- describe-food's cleaner food bank improved two cells and
silently stopped resolving a meal that used to resolve.
"""
COVERAGE_DROP = 0.02    # 2 percentage points
R_DROP = 0.02
MAE_RISE = 0.5


def compare(new: dict, baseline: dict, coverage_drop=COVERAGE_DROP,
            r_drop=R_DROP, mae_rise=MAE_RISE) -> list:
    """-> a list of regression dicts, empty when nothing got worse."""
    out = []
    for cell, nb in (new.get("cells") or {}).items():
        ob = (baseline.get("cells") or {}).get(cell)
        if not ob:
            out.append({"cell": cell, "what": "new_cell",
                        "note": "not in the baseline; nothing to compare"})
            continue
        for w in ("row", "dedup"):
            n_, o_ = nb.get(w) or {}, ob.get(w) or {}
            for key, worse, tol in (("coverage", "lower", coverage_drop),
                                    ("r", "lower", r_drop),
                                    ("mae", "higher", mae_rise)):
                a, b = n_.get(key), o_.get(key)
                if a is None or b is None:
                    # A metric that USED to be reportable and now is not is
                    # itself a regression: it means rows stopped scoring.
                    if b is not None and a is None:
                        out.append({"cell": cell, "weighting": w, "what": key,
                                    "from": b, "to": None,
                                    "note": "stopped being measurable"})
                    continue
                bad = (a < b - tol) if worse == "lower" else (a > b + tol)
                if bad:
                    out.append({"cell": cell, "weighting": w, "what": key,
                                "from": b, "to": a, "delta": round(a - b, 4)})
    return out
