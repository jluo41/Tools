"""
The door. A caller knows this signature and nothing else about this package.

    from mednorm import normalize
    normalize(["612997"], doses=[39])
    normalize(["Insulin dose - s.c."], doses=[5],
              payloads=['{"MedicationName": "insulin degludec, 12 IU"}'])

Deliberately the shape of a third-party API call, exactly as describe-food's and
describe-exercise's doors are.

WHY THE DOOR TAKES MORE THAN A LIST OF STRINGS
================================================================================
haipipe-norm's contract is `normalize(items: list[str])`. Food obeys it exactly
because a meal string is self-contained. A medication row is not:

    doses      the Dose column. A quantity, never an identity.
    payloads   the `medication` JSON column. OhioT1DM's drug CLASS and
               Shanghai's drug STRING exist ONLY in there -- for those two
               cohorts the MedicationID column holds no drug at all.

Both are optional and neither can change WHICH drug is resolved for a WellDoc
row. Omit them and the door behaves like food's: strings in, records out, with
no dose and a null basis saying so.

BATCH IS THE UNIT. 397,133 medication rows carry 1,373 distinct MedicationIDs,
so resolution runs once per distinct (id, payload) and only the dose scaling
runs per row.

TRANSPORT, chosen by MEDNORM_TRANSPORT: `local` in process (the default, so a
cook never fails because a daemon was down) or `http` against MEDNORM_URL.
"""
import os
from typing import Dict, List, Optional, Sequence, Union

from .aggregate import build
from .constants import FIELDS
from .dialect import parse
from .retrieve import resolve

DEFAULT_TRANSPORT = os.environ.get("MEDNORM_TRANSPORT", "local")
DEFAULT_URL = os.environ.get("MEDNORM_URL", "http://127.0.0.1:8079")

Scalarish = Union[None, float, int, str, Sequence]


def _spread(v, n, name):
    """None -> [None]*n; a scalar -> n copies; a sequence -> itself.
    A length mismatch raises: a silent zip truncation would re-pair every row
    after the missing one onto the wrong drug."""
    if v is None:
        return [None] * n
    if isinstance(v, (int, float, str)):
        return [v] * n
    v = list(v)
    if len(v) != n:
        raise ValueError(f"{name} has {len(v)} values for {n} items")
    return v


def _normalize_local(items, doses=None, payloads=None, **kw) -> List[Dict]:
    n = len(items)
    ds = _spread(doses, n, "doses")
    ps = _spread(payloads, n, "payloads")
    cache, out = {}, []
    for i, raw in enumerate(items):
        # The dose is part of the key only because a sentinel dose changes the
        # TYPE of the row, not merely its value.
        key = (str(raw), str(ps[i]), str(ds[i]) if ds[i] in (-1, 255, 999) else "")
        if key not in cache:
            item = parse(raw, ds[i], ps[i])
            cache[key] = (item,) + resolve(item)
        item, hit, conf, src, ndc = cache[key]
        # Re-parse only when this row's own dose differs from the cached one.
        if item.dose != _f(ds[i]) and item.kind not in ("sentinel",):
            item = parse(raw, ds[i], ps[i])
        out.append(build(item, hit, conf, src, ndc))
    return out


def _f(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if v != v else v


def _normalize_http(items, doses=None, payloads=None, url=None, timeout=None, **kw):
    import requests
    base = (url or DEFAULT_URL).rstrip("/")
    payload = {"items": list(items)}
    if doses is not None:
        payload["doses"] = doses if isinstance(doses, (int, float, str)) else list(doses)
    if payloads is not None:
        payload["payloads"] = payloads if isinstance(payloads, str) else list(payloads)
    r = requests.post(f"{base}/normalize/batch", json=payload,
                      timeout=int(timeout or os.environ.get("MEDNORM_TIMEOUT", "600")))
    r.raise_for_status()
    return r.json()["results"]


TRANSPORTS = {"local": _normalize_local, "http": _normalize_http}


def normalize(items: Sequence[str], doses: Scalarish = None,
              payloads: Scalarish = None, transport: Optional[str] = None,
              **kw) -> List[Dict]:
    """Batch, order-preserving, one result per input, duplicates resolved once.

    Every result carries the same 12 keys (constants.FIELDS) whether it hit or
    missed, so a caller never branches on shape -- only on MedConf.
    """
    t = transport or DEFAULT_TRANSPORT
    if t not in TRANSPORTS:
        raise ValueError(f"unknown transport {t!r}; have {sorted(TRANSPORTS)}")
    return TRANSPORTS[t](list(items), doses=doses, payloads=payloads, **kw)
