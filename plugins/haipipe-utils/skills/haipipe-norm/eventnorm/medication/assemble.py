"""
One medication event, raw to output (b51 s13): the preprocess step makes the input, describe-medication describes each
item (the drug's words and its NDC when the catalog gives one; never the dose: a catalog name's strength is not what
the person took, j03 t03 adapter_medication_named.py), and the event is set out by local hour: a dose is a moment, so
its start's hour holds it all, share 1; a temporary basal with an end is shared by its minutes.

    event(raw={"type": "app_id", "rows": [{...one MedAdministration row...}]})
    event(input={"start": "2024-08-29 10:01 -04:00", "items": [{"drug": "metformin", "dose": 500, "unit": "mg"}]})
    event(raw=..., input={...})                                 both: a field given in input wins

An item with insulin: true leaves here named; its action over the hours is s14's (describe-insulin).
"""
from functools import lru_cache

from ..hours import by_hour
from ..schema import RAW_DROP
from .preprocess import preprocess, total_of
from .schema import INPUT_KEYS, ITEM_KEYS


def plain(v):
    if hasattr(v, "item"):
        v = v.item()
    return None if isinstance(v, float) and v != v else v


@lru_cache(maxsize=20000)
def describe(drug: str, ndc: str = None) -> dict:
    """describe-medication, asked the drug's words (and its NDC when known): its whole answer, once per request."""
    from mednorm import normalize
    a = normalize([drug], ndcs=[ndc] if ndc else None)[0]
    return {k: plain(v) for k, v in a.items()}


def item_of(it: dict) -> dict:
    """An input item described: the FDA product's ingredient, brand, class, form, route and NDC, whether it is an
    insulin, how sure; the dose, unit and delivery as the input states them."""
    if not it.get("drug"):
        a = {}
    else:
        a = describe(str(it["drug"]), it.get("ndc") or None)
    return {"id": it["id"], "ingredient": a.get("Ingredient"), "brand": a.get("BrandName"),
            "class": a.get("PharmClass"), "form": a.get("DosageForm"), "route": a.get("Route"),
            "ndc": a.get("NDC"), "dose": it.get("dose"), "unit": it.get("unit"), "delivery": it.get("delivery"),
            "insulin": a.get("IsInsulin"), "conf": a.get("MedConf") or "MISS"}


def items_of(items):
    """Items made elsewhere, checked: a list of {"drug", "ndc"?, "dose"?, "unit"?, "delivery"?}."""
    if items is None:
        return None
    if not isinstance(items, list) or not all(isinstance(i, dict) and str(i.get("drug") or "").strip() for i in items):
        raise ValueError('input.items must be a list of {"drug": "...", "dose"?: number, "unit"?: "mg"}')
    return [{**{k: None for k in ITEM_KEYS}, **{k: v for k, v in i.items() if k in ITEM_KEYS or k == "class_word"},
             "id": i.get("id") or f"i{k + 1}"} for k, i in enumerate(items)]


def event(raw: dict = None, input: dict = None) -> dict:
    """{"raw", "input", "output", "step"}: raw as it came (whose-row columns dropped), the input, the output by local
    hour, and what the preprocess step did. A ValueError names what is wrong with what was sent."""
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"start", "items", ...}}, or both')
    pre = preprocess(raw) if raw else {"input": {}, "kind": None, "step": "no raw: the input as sent"}
    shown = {**{k: v for k, v in raw.items() if k != "rows"},
             "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]} if raw else None
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    inp = {k: (pre["input"] or {}).get(k) for k in INPUT_KEYS}
    if "items" in given:
        given["items"] = items_of(given["items"])
        given.setdefault("total", total_of(given["items"]))
    inp.update(given)
    if inp.get("source") is None:
        inp["source"] = {"kind": "logged"}
    if inp.get("logged_at") is None and not raw:
        inp["logged_at"] = inp.get("start")
    step = pre["step"] + ("; given in input: " + ", ".join(given) if given and raw else "")
    items = [item_of(i) for i in inp["items"]] if inp.get("items") else None
    total = None if inp.get("total") is None else {**inp["total"], **(
        {"unit": items[0]["unit"]} if items and len(items) == 1 and "unit" not in inp["total"]
        and "doses" in inp["total"] else {})}
    out = by_hour({"start": inp.get("start"), "end": inp.get("end"), "logged_at": inp.get("logged_at"),
                   "total": total, "items": items, "timeline": None, "source": inp["source"]})
    return {"raw": shown, "input": inp, "output": out, "step": step}
