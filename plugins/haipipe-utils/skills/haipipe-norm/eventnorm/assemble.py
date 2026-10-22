"""
One event, raw to output (s01 ⑦ ④): the preprocess step makes the input from the raw, the noun enriches the items,
and the event is set out by local hour. Lifted from b51 s01's drawing builder (studio/_build/topic_frames.py
food_event_dict), where it ran first; s01 ③'s eight meals are its test (tests/test_eventnorm.py).

    event(raw={"type": "app_log", "rows": [...]})                  the preprocess step makes the input
    event(input={"start": ..., "items": [{"food": "Banana"}]})    an input made elsewhere
    event(raw=..., input={"items": [...]})                         both: a field given in input wins (a photo row
                                                                   and the photo API's names)

The food API reads only the items (s01-D12): the time, the meal type and the meal's own total pass by it into the
output. The output's total is the tables' when there are items, else the input's own, and says which ("source").
"""
from .hours import by_hour
from .preprocess import preprocess
from .schema import INPUT_KEYS, RAW_DROP

GRAMS = __import__("re").compile(r"^[0-9]*\.?[0-9]+ (g|ml)$")


def ask_of(item: dict) -> str:
    """How an item made elsewhere is asked: its food, and its amount when that is grams or ml (as Shanghai's lines
    are asked); a serving word adds nothing the observed table can read."""
    a = str(item.get("amount") or "").strip()
    return f"{item['food']} {a}" if GRAMS.match(a) else str(item["food"])


def items_of(items) -> list:
    """Items made elsewhere, checked: a list of {"food", "amount"?, "food_zh"?}; each gets an id when it has none."""
    if items is None:
        return None
    if not isinstance(items, list) or not all(isinstance(it, dict) and str(it.get("food") or "").strip()
                                              for it in items):
        raise ValueError('input.items must be a list of {"food": "...", "amount"?: "...", "food_zh"?: "..."}')
    return [{"id": it.get("id") or f"i{k + 1}", **{f: it[f] for f in it if f != "id"}} for k, it in enumerate(items)]


def assemble(inp: dict, asks=None, meal=None, weight=None) -> dict:
    """The input -> the output by local hour: the items enriched (match, serving, 14 nutrients, GI and GL), the total
    from the tables when there are items, else the input's own; an event with no start is one entry, "no time"."""
    from foodnorm.items import enrich_items
    items, total = enrich_items(inp["items"], asks, meal) if inp.get("items") else (None, None)
    total = {**total, "source": "tables"} if total else {**inp["total"], "source": "input"} if inp.get("total") else None
    ev = {k: inp.get(k) for k in INPUT_KEYS if k not in ("total", "items", "timeline")}
    ev.update(total=total, items=items, timeline=inp.get("timeline"))
    line = inp.get("timeline") or []
    weight = weight or ("carbs" if line and all(pt.get("carbs") not in (None, "") for pt in line) else None)
    return by_hour(ev, weight) or {"no time": {"share": 1.0, **ev}}


def event(raw: dict = None, input: dict = None) -> dict:
    """{"raw", "input", "output", "step"}: raw as it came (whose-row columns dropped), the input, the output by local
    hour, and what the preprocess step did. A ValueError names what is wrong with what was sent."""
    if not raw and not input:
        raise ValueError('send {"raw": {"type", "rows"}} or {"input": {"items", ...}}, or both')
    pre = preprocess(raw) if raw else {"input": {}, "asks": None, "meal": None, "step": "no raw: the input as sent"}
    inp = {k: pre["input"].get(k) for k in INPUT_KEYS}
    given = {k: v for k, v in (input or {}).items() if k in INPUT_KEYS}
    asks, meal = pre["asks"], pre["meal"]
    if "items" in given:                                         # items made elsewhere: asked as they are
        given["items"] = items_of(given["items"])
        asks = [ask_of(it) for it in given["items"] or []]
        meal = "; ".join(asks)
    inp.update(given)
    out = {"raw": {**{k: v for k, v in raw.items() if k != "rows"},
                   "rows": [{k: v for k, v in r.items() if k not in RAW_DROP} for r in raw["rows"]]} if raw else None,
           "input": inp, "output": assemble(inp, asks, meal), "step": pre["step"]}
    if given and raw:
        out["step"] += "; given in input: " + ", ".join(given)
    return out
