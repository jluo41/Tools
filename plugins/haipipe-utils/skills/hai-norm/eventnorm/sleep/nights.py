"""
Cutting one person's sleep rows into nights (b51 j06; the three rule problems b01 found on WellDoc2025ALS, 261109).

A WellDoc SleepEntry file holds a person's rows from several devices, and a device may write a night as one whole row,
as a whole row with shorter rows inside it, or (Apple) as short rows only. Before a night can be an event its rows
have to be found. For the rows of ONE person and ONE device (EntrySourceID):

    1  a row sent again, the same start and end, is one row: the first is kept, the others named as dropped
    2  the longest row is a night; a shorter row that overlaps it is its piece (asleep). Then the longest row left
       is the next night, and so on. A row is only ever a piece of a night of its own device
    3  a device that writes pieces (Apple, PIECE_SOURCES): rows under 3 hours that are no night's piece and stand
       within JOIN_GAP_MIN minutes of each other are one night with no whole row: its start is the first row's, its
       end the last row's, every row asleep, the gaps awake

Each group says how it was found: "whole_row" (a night and its pieces), "joined" (3), "alone" (one row, no pieces).
"""
from bisect import bisect_right

PIECE_SOURCES = {"20"}                 # AppleHealthKit: the device seen writing stage pieces with no whole row
JOIN_GAP_MIN = 60                      # ALS and CVS: half the gaps between such rows are under 4 minutes, then a
NIGHT_MIN = 180                        #   long tail of next nights; an hour keeps a night's awake gap, not a day's


def cut(spans: list, join: bool = False, gap_min: float = JOIN_GAP_MIN) -> list:
    """`spans`: [(key, start, end)] of one person and one device, times comparable (local or UTC, all the same).
    Returns [{"how", "night": key or None, "pieces": [keys], "rows": [keys, in time order], "dropped": [keys]}] in
    time order."""
    first, dropped = {}, {}
    for key, s, e in sorted(spans, key=lambda x: (x[1], x[2], str(x[0]))):
        if (s, e) in first:
            dropped.setdefault(first[(s, e)][0], []).append(key)      # 1: the same start and end, once
        else:
            first[(s, e)] = (key, s, e)
    rows = sorted(first.values(), key=lambda x: (-(x[2] - x[1]), x[1], str(x[0])))
    starts, nights = [], []                                           # nights never overlap: kept by start
    for key, s, e in rows:
        i = bisect_right(starts, s)
        best, over = None, None
        for j in (i - 1, i):                                          # the night before its start, the one after
            if 0 <= j < len(nights):
                o = min(e, nights[j]["e"]) - max(s, nights[j]["s"])
                if o > o * 0 and (over is None or o > over):          # a positive overlap, whatever the time type
                    best, over = j, o
        if best is None:
            starts.insert(i, s)
            nights.insert(i, {"key": key, "s": s, "e": e, "pieces": []})
        else:
            nights[best]["pieces"].append((key, s, e))                # 2: a piece of the night it overlaps most
    out, chain = [], []

    def close():
        if len(chain) > 1:                                            # 3: no whole row, joined
            out.append({"how": "joined", "night": None, "pieces": [n["key"] for n in chain],
                        "rows": [n["key"] for n in chain], "start": chain[0]["s"], "end": chain[-1]["e"],
                        "dropped": sum((dropped.get(n["key"], []) for n in chain), [])})
        elif chain:
            n = chain[0]
            out.append({"how": "alone", "night": n["key"], "pieces": [], "rows": [n["key"]], "start": n["s"],
                        "end": n["e"], "dropped": dropped.get(n["key"], [])})
        chain.clear()

    for n in nights:
        minutes = (n["e"] - n["s"]).total_seconds() / 60
        bare = not n["pieces"]
        if join and bare and minutes < NIGHT_MIN:
            if chain and (n["s"] - chain[-1]["e"]).total_seconds() / 60 > gap_min:
                close()
            chain.append(n)
            continue
        close()
        if bare:
            chain.append(n)
            close()
        else:
            ps = sorted(n["pieces"], key=lambda x: (x[1], x[2]))
            out.append({"how": "whole_row", "night": n["key"], "pieces": [p[0] for p in ps],
                        "rows": [n["key"]] + [p[0] for p in ps], "start": n["s"], "end": n["e"],
                        "dropped": dropped.get(n["key"], []) + sum((dropped.get(p[0], []) for p in ps), [])})
    close()
    return sorted(out, key=lambda g: (g["start"], str(g["rows"][0])))


def nights(rows: list, id_column: str = "SleepEntryID") -> list:
    """One person's WellDoc rows (any devices) cut into nights: each device apart, so a piece never joins another
    device's night. Returns cut()'s groups with "source" and the rows themselves ("night_row", "piece_rows")."""
    from .preprocess import times
    by = {}
    for r in rows:
        s, e, _zone, _m = times(r)
        by.setdefault(str(r.get("EntrySourceID")), []).append((str(r[id_column]), s, e))
    at = {str(r[id_column]): r for r in rows}
    out = []
    for src, spans in by.items():
        for g in cut(spans, join=src in PIECE_SOURCES):
            out.append({**g, "source": src, "night_row": at.get(g["night"]), "piece_rows": [at[k] for k in g["pieces"]]})
    return sorted(out, key=lambda g: (g["start"], g["source"]))
