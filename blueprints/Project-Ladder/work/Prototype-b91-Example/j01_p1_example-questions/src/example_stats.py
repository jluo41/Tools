"""Small statistics two or more of the example's scripts share: a rate with its Wilson interval, a gap between two
rates with its Wald interval, and a z test of two gaps. Standard library and pandas only."""
import math
from statistics import NormalDist

Z = 1.959964


def rate_row(level, n: int, k: int, wilson) -> dict:
    lo, hi = wilson(k, n) if n else (float("nan"), float("nan"))
    return {"level": level, "n": int(n), "k": int(k), "rate_pct": 100 * k / n if n else float("nan"),
            "ci_lo_pct": 100 * lo, "ci_hi_pct": 100 * hi}


def gap(df, outcome: str = "outcome", arm: str = "arm") -> tuple:
    """(gap in points, its standard error in points): arm B minus arm A."""
    a, b = df[df[arm] == "A"][outcome], df[df[arm] == "B"][outcome]
    if len(a) == 0 or len(b) == 0:
        return float("nan"), float("nan")
    pa, pb = a.mean(), b.mean()
    se = math.sqrt(pa * (1 - pa) / len(a) + pb * (1 - pb) / len(b))
    return 100 * (pb - pa), 100 * se


def gap_row(part, g: float, se: float, key: str = "part") -> dict:
    return {key: part, "gap_pp": g, "gap_lo_pp": g - Z * se, "gap_hi_pp": g + Z * se}


def z_test(g1: float, se1: float, g2: float, se2: float) -> tuple:
    """(difference g2 - g1, its standard error, two-sided p)."""
    d, se = g2 - g1, math.sqrt(se1 ** 2 + se2 ** 2)
    p = 2 * (1 - NormalDist().cdf(abs(d) / se)) if se else float("nan")
    return d, se, p
