"""
The door. A caller knows this signature and nothing else about this package.

    from foodnorm import normalize
    out = normalize(["fried rice; egg", "Cucumber 100g"])

That is deliberately the shape of a third-party API call. The Stage-1 SourceFn
that consumes it must not know the dialect layer, the bank, the stage sequence,
or which repository any of them ship from -- so that all of those can move,
be rewritten, or become a real remote service without a pipeline file changing.

TRANSPORT is the one thing that varies, chosen by FOODNORM_TRANSPORT:

    local   the default. Resolve in process against the local bank. No service
            to run, no network, ~12 ms for one meal. A cook must not fail
            because a daemon was down, so this is what ships.
    http    POST FOODNORM_URL/normalize/batch. The same contract over the wire,
            for when the resolver runs somewhere else.

BATCH IS THE UNIT, not the row. The caller hands over the DISTINCT strings and
gets one result per input, in order: Shanghai's 71k rows carry ~3,130 distinct
meal strings, and a per-row call would be three orders of magnitude of waste.
"""
import json
import os
from typing import Dict, List, Optional, Sequence

# The five nutrients, and the three provenance columns that must travel with
# them. A number without its basis is not interpretable and must never be
# returned alone.
NUTRIENTS = ("Calories", "Carbs", "Protein", "Fat", "Fiber")
PROVENANCE = ("NutritionSource", "NutritionConf", "NutritionBasis",
              "NutritionCoverage")

DEFAULT_TRANSPORT = os.environ.get("FOODNORM_TRANSPORT", "local")
DEFAULT_URL = os.environ.get("FOODNORM_URL", "http://127.0.0.1:8077")


def _empty(reason: str = "none") -> Dict:
    """A MISS, in the same shape as a hit. The caller never branches on
    whether a result came back; it branches on NutritionConf."""
    d = {k: None for k in NUTRIENTS}
    d["NutritionSource"] = reason
    d["NutritionConf"] = "MISS"
    d["NutritionBasis"] = None
    d["NutritionCoverage"] = None
    return d


def _normalize_local(foods: Sequence[str], **kw) -> List[Dict]:
    import pandas as pd
    from .enrich import enrich_food_to_nutrition

    df = pd.DataFrame({"FoodName": list(foods)})
    out = enrich_food_to_nutrition(df, food_col="FoodName", **kw)
    cols = list(NUTRIENTS) + list(PROVENANCE)
    for extra in ("NameSource", "NameConf", "FoodNameResolved"):
        if extra in out.columns:
            cols.append(extra)
    return out[cols].to_dict("records")


def _normalize_http(foods: Sequence[str], url: str = None, timeout: int = 120, **kw) -> List[Dict]:
    import urllib.request

    url = (url or DEFAULT_URL).rstrip("/") + "/normalize/batch"
    body = json.dumps({"foods": list(foods), "options": kw}).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read())
    results = payload.get("results", [])
    # The wire is not trusted to preserve length; the contract is one result per
    # input, in order, and a short reply is padded with MISSes rather than
    # silently shifting every later row onto the wrong meal.
    if len(results) < len(foods):
        results = results + [_empty("transport_short")] * (len(foods) - len(results))
    return results[:len(foods)]


TRANSPORTS = {"local": _normalize_local, "http": _normalize_http}


def normalize(foods: Sequence[str], transport: str = None, **kw) -> List[Dict]:
    """Resolve free-text food strings to nutrition. One dict per input, in order.

    Args:
        foods: the strings, in any cohort's dialect. Duplicates are fine and are
               resolved once.
        transport: "local" (default) or "http"; else FOODNORM_TRANSPORT.
        **kw: passed through to the resolver (stages, image_col, image_engine…).

    Returns one dict per input carrying Calories/Carbs/Protein/Fat/Fiber plus
    NutritionSource, NutritionConf and NutritionBasis. Read NutritionBasis
    before comparing or pooling any number: per_100g is not a meal.
    """
    foods = ["" if f is None else str(f) for f in foods]
    if not foods:
        return []

    name = transport or DEFAULT_TRANSPORT
    if name not in TRANSPORTS:
        raise ValueError(f"unknown transport {name!r}; have {sorted(TRANSPORTS)}")

    # Resolve each DISTINCT string once and fan the answer back out. The
    # resolver caches components internally, but the transport does not, and
    # over HTTP a duplicate is a byte on the wire and a row in the reply.
    order: List[str] = []
    seen = {}
    for f in foods:
        if f not in seen:
            seen[f] = len(order)
            order.append(f)

    resolved = TRANSPORTS[name](order, **kw)
    if len(resolved) != len(order):
        resolved = (list(resolved) + [_empty("transport_short")] * len(order))[:len(order)]
    return [resolved[seen[f]] for f in foods]
