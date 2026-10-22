"""
A food's GI and GL from ext_food_gi: one food item at a time, by its name (items.py and the event API call it).

Lifted whole from b51 j01 t21_food_gi's scripts/gi_match.py (2026-10-21, s01 ⑦ "glycemic.py moved from t21"); t21's
own Runs keep reading their copy. `matcher()` at the bottom opens the table. The table is internal (CC BY-NC-ND):
callers get one item's gi and gl, never the table.

GL (glycemic load) = GI x available carbohydrate / 100, and available carbohydrate is carbs minus fibre,
for the amount the item's numbers are for. A matched item gets its GL however small. An item that matches
nothing and has under LOW_CARB g of available carbohydrate gets GL 0 and no GI: a GI test feeds about 50 g
of it, so such foods (cheese, egg, spinach) are never tested, and any GI times so little is near 0.

The name match, English: both names lose what is in brackets, trade marks, numbers and units, and a few
filler words; plurals are made singular. The logged name's last word is its head (muffin, rice, bread). A
Table A1 name puts its food before the first comma ("Yoghurt, strawberry" is a yoghurt), so a candidate
must hold the head there; it costs one for each word the logged name lacks, and two more when the head is
not the last word of that first part ("Blueberry muffin" is a muffin, not blueberries). Of the candidates
holding the most logged words (at least MIN_SCORE of them), those within one of the lowest cost are kept,
when that cost is at most MAX_COST, and the GI is their median: "White Rice" meets many rices (GI 54 to
109), so one GI stands for the kind. A name of meal words only ("dinner") is not a food. Chinese: a name of
the Chinese list, its brackets dropped, that the item's Chinese name equals or holds (the longest).

The first r04 pass (2026-10-21) matched without the first-part rule and put "blueberries" on blueberry
muffins, "strawberries" on strawberry yoghurt and "dinner" on a macaroni dinner; the rule came from it.
"""

import re
import statistics

LOW_CARB = 5.0
MIN_SCORE = 2 / 3
MAX_COST = 3
NOT_FOOD = {'breakfast', 'lunch', 'dinner', 'supper', 'snack', 'meal', 'food', 'unknown', 'just', 'carbs', 'carb'}
STOP = {'a', 'an', 'the', 'and', 'with', 'of', 'in', 'on', 'or', 'for', 'to', 'made', 'from', 'type', 'ns',
        'original', 'classic', 'plain', 'regular', 'style', 'homemade', 'fresh', 'oz', 'cup', 'cups', 'g', 'gram',
        'grams', 'tbsp', 'tsp', 'slice', 'slices', 'piece', 'pieces', 'serving', 'servings', 'ml', 'lb', 'small',
        'medium', 'large', 'brand', 'usa', 'us', 'australia', 'canada', 'uk'}
BRACKETS = re.compile(r'\([^)]*\)|\[[^\]]*\]|（[^）]*）')


def singular(w):
    if len(w) > 4 and w.endswith('ies'):
        return w[:-3] + 'y'
    if len(w) > 4 and w.endswith('oes'):
        return w[:-2]
    if len(w) > 3 and w.endswith('s') and not w.endswith('ss'):
        return w[:-1]
    return w


def words(name):
    """'Original English Muffins' -> ['english', 'muffin']: the content words, in order."""
    s = BRACKETS.sub(' ', str(name).lower())
    s = re.sub(r'[™®©]', ' ', s)
    out = [singular(w) for w in re.findall(r'[a-z]+', s)]
    return [w for w in out if w not in STOP and len(w) > 1]


class Matcher:
    """Built once on the ext_food_gi table (a DataFrame); match() and match_zh() answer one name."""

    def __init__(self, table):
        a1 = table[table['source'] == 'atkinson2008_A1']
        self.rows = [(r.gi_id, r.number, r.food_name, float(r.gi), set(words(r.food_name)),
                      words(BRACKETS.sub(' ', r.food_name).split(',')[0])) for r in a1.itertuples()]
        self.index = {}                                         # a word -> the foods whose first part holds it
        for k, row in enumerate(self.rows):
            for w in set(row[5]):
                self.index.setdefault(w, []).append(k)
        cn = table[table['source'] == 'china_gi_list']
        self.zh = sorted(((BRACKETS.sub('', r.food_name).strip(), r.gi_id, r.food_name, float(r.gi))
                          for r in cn.itertuples()), key=lambda x: -len(x[0]))

    def match(self, name):
        """A name -> {gi, gi_lo, gi_hi, n, gi_id, number, food_name, score}, or None."""
        ws = words(name)
        if not ws or set(ws) <= NOT_FOOD:
            return None
        head, want = ws[-1], set(ws)
        cands = [(len(want & self.rows[k][4]) / len(want),
                  len(self.rows[k][4] - want) + (0 if self.rows[k][5][-1] == head else 2), k)
                 for k in self.index.get(head, [])]
        if not cands:
            return None
        best = max(c[0] for c in cands)
        if best < MIN_SCORE:
            return None
        top = [c for c in cands if c[0] == best]
        lowest = min(c[1] for c in top)
        if lowest > MAX_COST:
            return None
        kept = sorted((c for c in top if c[1] <= lowest + 1), key=lambda c: (c[1], c[2]))
        gis = [self.rows[c[2]][3] for c in kept]
        gi_id, number, food_name = self.rows[kept[0][2]][:3]
        return {'gi': float(statistics.median(gis)), 'gi_lo': min(gis), 'gi_hi': max(gis), 'n': len(kept),
                'gi_id': gi_id, 'number': number, 'food_name': food_name, 'score': round(best, 3)}

    def match_zh(self, name_zh):
        """A Chinese name -> the same fields from the Chinese list, or None."""
        s = BRACKETS.sub('', str(name_zh or '')).strip()
        for key, gi_id, food_name, gi in self.zh:
            if key and (s == key or key in s):
                return {'gi': gi, 'gi_lo': gi, 'gi_hi': gi, 'n': 1, 'gi_id': gi_id, 'number': None,
                        'food_name': food_name, 'score': 1.0 if s == key else round(len(key) / len(s), 3)}
        return None


def glycemic(m, name, carbs, fiber, name_zh=None):
    """One item -> {'gi', 'gl', 'from'}: its GI (matched by name) and its GL for the carbs its numbers hold."""
    if carbs is None or carbs != carbs or carbs < 0:
        return {'gi': None, 'gl': None, 'from': 'no carbs'}
    fib = fiber if fiber is not None and fiber == fiber and fiber >= 0 else 0.0
    avail = max(float(carbs) - float(fib), 0.0)
    if m is None:                                            # added on the lift: no table on this host
        return {'gi': None, 'gl': None, 'from': 'no GI table'}
    hit = (m.match_zh(name_zh) if name_zh else None) or m.match(name)
    if hit is None:
        if avail < LOW_CARB:
            return {'gi': None, 'gl': 0.0, 'from': f'under {LOW_CARB:g} g available carbs'}
        return {'gi': None, 'gl': None, 'from': 'no match'}
    where = f"{hit['gi_id']}, {hit['n']} food{'s' * (hit['n'] > 1)}" if hit['n'] > 1 else hit['gi_id']
    return {'gi': hit['gi'], 'gl': round(hit['gi'] * avail / 100, 1), 'from': where}


GI_TABLE = "ext_food_gi/GI2008CN/df_ext_food_gi.parquet"     # no release pins it yet (s01 Open 5)


def _find_table():
    """FOODNORM_GI_TABLE, else $LOCAL_EXTERNAL_STORE, else a walk up to _WorkSpace/ExternalStore: the order
    observed.py uses, so a service starts from any directory."""
    import os
    from pathlib import Path
    explicit = os.environ.get("FOODNORM_GI_TABLE")
    if explicit:
        return Path(explicit)
    store = os.environ.get("LOCAL_EXTERNAL_STORE")             # env.sh writes it relative to the SPACE root
    roots = [Path(store)] + [anc / store for anc in Path(__file__).absolute().parents] if store else []
    roots += [anc / "_WorkSpace" / "ExternalStore" for anc in Path(__file__).absolute().parents]
    roots += [anc / "_WorkSpace" / "ExternalStore" for anc in Path(__file__).resolve().parents]
    roots += [anc / "_WorkSpace" / "ExternalStore" for anc in [Path.cwd(), *Path.cwd().parents]]   # Tools may be a
    # symlink out of the SPACE (WellDoc-SPACE/Tools -> ../Tools-SPACE): a run from the SPACE finds it this way
    return next((r / GI_TABLE for r in roots if (r / GI_TABLE).exists()), None)


_MATCHER = []


def matcher():
    """The Matcher on the GI table, built once; None when the table is absent (every item then says why)."""
    if not _MATCHER:
        import pandas as pd
        p = _find_table()
        _MATCHER.append(Matcher(pd.read_parquet(p)) if p else None)
    return _MATCHER[0]
