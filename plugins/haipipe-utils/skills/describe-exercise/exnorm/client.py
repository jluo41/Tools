"""
The door. A caller knows this signature and nothing else about this package.

    from exnorm import normalize
    out = normalize(["Walking", "src20:20903"], minutes=[30, 11], weight_kg=82)

Deliberately the shape of a third-party API call, exactly as describe-food's
door is: the Stage-1 SourceFn that consumes it must not know the dialect layer,
the compendium, or which repository either ships from, so all of those can move
or become a remote service without a pipeline file changing.

WHY THIS DOOR TAKES MORE THAN A LIST OF STRINGS
================================================================================
haipipe-norm's contract is `normalize(items: list[str])`. Food obeys it exactly
because a meal string is self-contained. An exercise row is not:

    minutes    MET is a RATE. Without minutes there is no dose to report, and
               inventing one is rule 4's exact prohibition.
    weight_kg  kcal scales with body mass. Same.
    source_ids the EntrySourceID that issued a numeric code. Without it, '20903'
               cannot be placed in a vendor namespace and cannot be typed.
    person_ids WHOSE bout this is. The Compendium publishes one MET per activity
               for a population; passing an identity lets that number be
               adjusted toward the person or the wearable that measured them.
               Absent, the population number is returned, which is what this
               door did before the argument existed.

Each is OPTIONAL and each is a SCALE or a KEY, never an identity of the ITEM --
the item string still names the thing. Omit them all and the door behaves
exactly like food's: strings in, records out, on the per_minute basis with a
basis column saying so. That is the contract honoured, not bent: the extra
arguments cannot change WHICH activity is resolved, only what scale it can be
reported on and whose scale that is.

    minutes  weight  ->  what comes back           ExerciseBasis
    -------  ------      ---------------           -------------
    no       no          MET only                  per_minute
    yes      no          MET + ActiveMinutes       per_minute
    no       yes         MET only                  per_minute
    yes      yes         MET + minutes + kcal      per_session

BATCH IS THE UNIT, not the row. 136,555 exercise rows carry 135 distinct types,
a thousand-fold ratio, so resolution is done once per DISTINCT (type, source)
and only the scaling runs per row. person_ids does NOT enter that cache key and
must not: which activity a string names has nothing to do with who did it, and
folding a person into the key would multiply the cache by the cohort size to
buy nothing.

TRANSPORT is the one thing that varies, chosen by EXNORM_TRANSPORT:
    local   the default. In process, no service, no network. A cook must not
            fail because a daemon was down, so this is what ships.
    http    POST EXNORM_URL/normalize/batch. Same contract over the wire.
"""
import json
import os
from typing import Dict, List, Optional, Sequence, Union

from . import scale as _scale
from .aggregate import build
from .constants import FIELDS
from .dialect import parse
from .retrieve import resolve

DEFAULT_TRANSPORT = os.environ.get("EXNORM_TRANSPORT", "local")
DEFAULT_URL = os.environ.get("EXNORM_URL", "http://127.0.0.1:8078")

Scalarish = Union[None, float, int, str, Sequence]


def _spread(v: Scalarish, n: int, name: str) -> List:
    """None -> [None]*n, a scalar -> the same value n times, a sequence -> itself.
    A length mismatch is an error and not a silent zip truncation, which would
    quietly re-pair every row after the first missing one."""
    if v is None:
        return [None] * n
    if isinstance(v, (int, float, str)):
        return [v] * n
    v = list(v)
    if len(v) != n:
        raise ValueError(f"{name} has {len(v)} values for {n} activities")
    return v


def _num(v, name: str = "value") -> Optional[float]:
    """None / NaN / '' -> not stated. Anything else non-numeric -> the caller's
    error, raised.

    These two used to share a return. They are different failures: a NaN in a
    DataFrame column means the log stated no duration, while the string 'abc'
    means whoever built the request has a bug. Swallowing the second as the
    first turns a caller mistake into a silent MISS, which is the exact shape of
    the defect this package's rule 5 exists to prevent."""
    if v is None:
        return None
    if isinstance(v, str) and not v.strip():
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"{name}={v!r} is not a number")
    return None if f != f else f          # NaN is not a quantity


def _normalize_local(activities: Sequence[str], minutes=None, weight_kg=None,
                     source_ids=None, person_ids=None, path=None,
                     scale_path=None, **kw) -> List[Dict]:
    n = len(activities)
    mins = _spread(minutes, n, "minutes")
    kgs = _spread(weight_kg, n, "weight_kg")
    srcs = _spread(source_ids, n, "source_ids")
    pids = _spread(person_ids, n, "person_ids")

    resolved = {}                          # (raw, source) -> (Activity, row, conf, source_str)
    scales = {}                            # (person, source, code) -> factor triple
    out = []
    for i, raw in enumerate(activities):
        key = (str(raw), str(srcs[i]))
        if key not in resolved:
            act = parse(raw, srcs[i])
            row, conf, src = resolve(act, path)
            resolved[key] = (act, row, conf, src)
        act, row, conf, src = resolved[key]

        code = row["activity_code"] if row is not None else None
        skey = (str(pids[i]), str(srcs[i]), str(code))
        if skey not in scales:
            scales[skey] = _scale.factor_for(pids[i], srcs[i], code, scale_path)

        out.append(build(act, row, conf, src,
                         _num(mins[i], "minutes"), _num(kgs[i], "weight_kg"),
                         scale=scales[skey]))
    return out


def _normalize_http(activities: Sequence[str], minutes=None, weight_kg=None,
                    source_ids=None, person_ids=None, url=None, timeout=None,
                    **kw) -> List[Dict]:
    import requests
    base = (url or DEFAULT_URL).rstrip("/")
    payload = {"activities": list(activities)}
    for k, v in (("minutes", minutes), ("weight_kg", weight_kg),
                 ("source_ids", source_ids), ("person_ids", person_ids)):
        if v is not None:
            payload[k] = v if isinstance(v, (int, float, str)) else list(v)
    r = requests.post(f"{base}/normalize/batch", json=payload,
                      timeout=int(timeout or os.environ.get("EXNORM_TIMEOUT", "600")))
    r.raise_for_status()
    return r.json()["results"]


TRANSPORTS = {"local": _normalize_local, "http": _normalize_http}


def normalize(activities: Sequence[str], minutes: Scalarish = None,
              weight_kg: Scalarish = None, source_ids: Scalarish = None,
              person_ids: Scalarish = None,
              transport: Optional[str] = None, **kw) -> List[Dict]:
    """Batch, order-preserving, one result per input, duplicates resolved once.

    Every result carries the same 14 keys (constants.FIELDS) whether it hit or
    missed, so a caller never branches on shape -- only on ExerciseConf.
    """
    t = transport or DEFAULT_TRANSPORT
    if t not in TRANSPORTS:
        raise ValueError(f"unknown transport {t!r}; have {sorted(TRANSPORTS)}")
    return TRANSPORTS[t](list(activities), minutes=minutes, weight_kg=weight_kg,
                         source_ids=source_ids, person_ids=person_ids, **kw)
