"""
What every food preprocess step shares: the rows as a table, a time read as local time with its offset, the meal's
own numbers as the raw states them, a meal type word, and a cell of foods split into items. Lifted from b51 s01's
drawing builder (studio/_build/topic_frames.py meal_time, logged_time, stated_total, meal_type, food_record).
"""
import re

from ..schema import RAW_DROP

FOOD_GROUPS = None                                               # filled from foodnorm.items on first use


def groups():
    global FOOD_GROUPS
    if FOOD_GROUPS is None:
        from foodnorm.items import FOOD_GROUPS as G
        FOOD_GROUPS = G
    return FOOD_GROUPS


def frame(raw: dict):
    """raw["rows"] as a DataFrame of text, whose-row columns dropped; a ValueError when there are none."""
    import pandas as pd
    rows = raw.get("rows")
    if not isinstance(rows, list) or not rows or not all(isinstance(r, dict) for r in rows):
        raise ValueError('raw.rows must be a list of rows, each {"column": "value", ...}')
    df = pd.DataFrame([{k: (None if v is None else str(v)) for k, v in r.items() if k not in RAW_DROP} for r in rows])
    return df


def clock(rows, col: str, offset: str = None, zone: str = "", dayfirst: bool = False, latest: bool = False):
    """A time column as local time with its offset, "2021-04-14 07:17 -04:00": the earliest row (the meal began
    then), or the latest with `latest` (when it was logged: the meal is whole only then). `offset` names a column of
    minutes to add to a UTC time (the app; Diet5Min does the same); `zone` names the zone of a local time; neither
    leaves it bare. None when the column is missing or holds no time."""
    import pandas as pd
    if not col or col not in rows.columns:
        return None
    import warnings
    with warnings.catch_warnings():                              # one meal's rows: no format to infer, none needed
        warnings.simplefilter("ignore", UserWarning)
        when = pd.to_datetime(rows[col], errors="coerce", dayfirst=dayfirst)
    if when.isna().all():
        return None
    i = when.idxmax() if latest else when.idxmin()
    ts = when[i]
    if offset and offset in rows.columns and str(rows.loc[i, offset]).strip() not in ("", "None", "nan"):
        m = int(float(rows.loc[i, offset]))
        ts, zone = ts + pd.Timedelta(minutes=m), f"{'+' if m >= 0 else '-'}{abs(m) // 60:02d}:{abs(m) % 60:02d}"
    return f"{ts:%Y-%m-%d %H:%M} {zone}".strip()


def meal_word(v):
    """breakfast, lunch, dinner or snack as the raw says it (CGMacros' Snack, Snacks and Snack 1 are all snack)."""
    v = re.sub(r"^snacks?\b.*", "snack", str(v or "").strip().lower())
    return v if v and v not in ("nan", "none") else None


def stated_total(rows, name_col: str = None, skipped=()):
    """The input's "total" (s01-D23, D28, D33): the meal's numbers as its raw gives them, in the output's groups.
    Each of FatSecret's 14 the raw has a column for, whatever its case, summed over the meal's rows; an empty cell or
    a negative is the vendor's "not given" and is left out, never written as 0. A carb count (a row the food split
    calls no food, `skipped`) gives its carbs only; it is written on every row of its meal, so carbs that agree on
    every row of a meal holding one are counted once; and a meal with a typed count states only its carbs. None when
    the raw states no number."""
    import pandas as pd
    val = lambda v, u: f"{round(float(v), 2):g} {u}"
    cols = {c.lower(): c for c in rows.columns}
    count = rows[name_col].astype(str).str.strip().isin(list(skipped)) if name_col in rows.columns and skipped \
        else pd.Series(False, index=rows.index)
    out = {}
    for g, fields in groups():
        grp = {}
        for name, col, u in fields:
            if col.lower() not in cols:
                continue
            v = pd.to_numeric(rows[cols[col.lower()]], errors="coerce")
            v = v[(v >= 0) & ((col == "Carbs") | ~count)]
            if v.empty:
                continue
            if count.any() and col != "Carbs":
                continue
            once = col == "Carbs" and skipped and len(v) > 1 and v.nunique() == 1
            grp[name] = val(v.iloc[0] if once else v.sum(), u)
        if grp:
            out[g] = grp
    return out or None


AMOUNT = re.compile(r"([0-9]*\.?[0-9]+)\s*(g|ml)\s*$", re.I)


def lines_to_items(cell: str, zh_cell: str = None):
    """A cell of foods, one a line, an amount in grams or ml at its end (Shanghai's Dietary intake; anything typed
    the same way) -> (items, the line each is asked with, the lines that are no food). The Chinese cell, line for
    line, gives each item its food_zh."""
    from foodnorm.dialect import split_meal
    en = [ln.strip() for ln in str(cell or "").split("\n") if ln.strip()]
    zh = [ln.strip() for ln in str(zh_cell or "").split("\n") if ln.strip()]
    items, asks, skipped = [], [], []
    for k, line in enumerate(en):
        c = split_meal(line)
        if not c or c[0].kind != "food":
            skipped.append(line)
            continue
        m = AMOUNT.search(line)
        it = {"id": f"i{len(items) + 1}", "food": re.sub(r"\s*[0-9]*\.?[0-9]+\s*(g|ml)\s*$", "", line, flags=re.I)}
        if m:
            it["amount"] = f"{float(m.group(1)):g} {m.group(2)}"
        if k < len(zh):
            it["food_zh"] = re.sub(r"[\s\t]*[0-9]*\.?[0-9]+\s*(g|ml|克)?\s*$", "", zh[k])
        items.append(it)
        asks.append(line)
    return items, asks, skipped


def step_text(n_rows: int, items: list, skipped: list, head: str = "") -> str:
    """What the step did, in one line: "5 rows of one meal → 5 items; not a food, so no item: 'Just Carbs'"."""
    s = head or f"{n_rows} row{'s' * (n_rows > 1)}{' of one meal' * (n_rows > 1)} → {len(items)} " \
                f"item{'s' * (len(items) != 1)}"
    return s + ("; not a food, so no item: " + ", ".join(f"'{x}'" for x in skipped) if skipped else "")
