#!/usr/bin/env python3
"""
Build `_ExerciseInfo/0-inputs/`: one specimen of every SHAPE that can arrive.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-exercise/build_inputs_gallery.py

The engine is haipipe-norm/inputs_gallery.py, shared by all four nouns. This
file holds only the list of shapes, because the list is the part that differs:
exercise arrives as a vendor code 22% of the time and food never does, and two
thirds of its rows are not events at all.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(a for a in HERE.parents
            if (a / "pyproject.toml").exists() and (a / "code").is_dir())
SKILLS = ROOT / "Tools/plugins/haipipe-utils/skills"
sys.path[:0] = [str(HERE), str(SKILLS / "haipipe-norm")]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo"

import pandas as pd                                       # noqa: E402
import exnorm                                             # noqa: E402
from exnorm.dialect import parse                          # noqa: E402
from inputs_gallery import (Shape, build, ABSENT, CALL,
                            CONTRACT, DEPLOYMENT)     # noqa: E402


def call(req):
    kw = {k: v for k, v in req.items() if k != "activities"}
    return exnorm.normalize(req["activities"], **kw)


def by_kind(kind, numeric=None):
    """A corpus row is this shape when dialect.parse types it so."""
    def count(c):
        return sum(1 for k, n in c["rows"]
                   if k == kind and (numeric is None or n == numeric))
    return count


def sample_kind(kind, numeric=None, n=2):
    """The specimen comes off the board. Take the most common real string of
    this shape, with the EntrySourceID that issued it, and say who wrote it."""
    def take(c):
        g, rows = c["g"], c["rows"]
        mask = [k == kind and (numeric is None or nu == numeric) for k, nu in rows]
        sub = g[mask]
        top = sub.ExerciseType.astype(str).value_counts().head(n)
        picked = list(top.index)
        hit = sub[sub.ExerciseType.astype(str).isin(picked)]
        src = [int(hit[hit.ExerciseType.astype(str) == v].EntrySourceID.mode().iloc[0])
               if hit[hit.ExerciseType.astype(str) == v].EntrySourceID.notna().any() else None
               for v in picked]
        who = hit.cohort.value_counts()
        prov = ("Real rows. "
                + " · ".join(f"{v!r} from EntrySourceID {sc}, {int(top[v]):,} times"
                             for v, sc in zip(picked, src))
                + ". Written by " + ", ".join(f"{k} ({int(x):,})" for k, x in who.items()) + ".")
        req = {"activities": picked, "minutes": 30, "weight_kg": 70}
        # Only send source_ids when the board actually recorded one. Coercing a
        # missing EntrySourceID to 0 would invent a namespace that does not exist.
        if all(x is not None for x in src):
            req["source_ids"] = src
        return req, prov
    return take


def sources(c):
    """Who wrote the rows. Exercise splits on whether a cohort types or picks."""
    import re as _re
    g = c["g"]
    rows = []
    for coh, sub in g.groupby("cohort"):
        w = sub.ExerciseType.dropna().astype(str)
        n, u = len(sub), max(w.nunique(), 1)
        num = w.str.fullmatch(r"\d+").mean()
        rows.append((coh, f"{n:,}", f"{u:,}", f"{n/u:.0f}x",
                     "picks from a menu" if num > 0.5 else "types words"
                     + (f" ({1-num:.0%} words)" if 0 < num <= 0.5 else "")))
    rows.sort(key=lambda r: -int(r[1].replace(",", "")))
    tot = len(g); totu = g.ExerciseType.nunique()
    rows.append(("ALL", f"**{tot:,}**", f"**{totu:,}**", f"**{tot/totu:.0f}x**",
                 "103 of the 135 writings are numbers"))
    note = ("Exercise is the opposite of food. Four WellDoc cohorts pick from a "
            "device or app menu, so a whole cohort is covered by a few dozen codes; "
            "only OhioT1DM and mcphases-v1 contain words a person typed. Ten writings "
            "cover 87.9% of all rows, so a row-weighted score is effectively a test "
            "of ten strings.")
    return rows, note


SHAPES = [
    Shape("01-plain-text", "a name a person typed",
          "The contract's default: strings in, records out. Every other shape "
          "here is a way the world fails to be this one.",
          {"activities": ["Walking"], "minutes": 30, "weight_kg": 70},
          by_kind("session", False),
          see="5-api-examples/1-resolves/walk-30min", sample=sample_kind("session", False)),
    Shape("02-decorated-text", "a name with something else stuck to it",
          "What a real free-text box produces. Not on this board, because "
          "WellDoc uses a picker and nobody here has typed one. It is on the "
          "API's promise anyway, and today the door resolves none of the four. "
          "describe-food handles the same shape, because food splits a string "
          "into components and exercise reads it whole.",
          {"activities": ["Walking, measured by Apple Watch", "walking (apple watch)",
                          "Brisk walking", "went for a walk"],
           "minutes": 30, "weight_kg": 70},
          ABSENT),
    Shape("03-vendor-code", "a number, and a codebook that reads it",
          "A code means nothing without the key saying WHOSE code it is. That "
          "key is EntrySourceID, and it is why the same digits from two vendors "
          "get two verdicts and two device scales.",
          {"activities": ["20052", "1001"], "source_ids": [20, 23],
           "minutes": 30, "weight_kg": 70},
          by_kind("session", True),
          sample=sample_kind("session", True), see="5-api-examples/7-codebooks/four-dialects",
          layer=DEPLOYMENT,
          unwraps_to="`01-plain-text` via the vendor's codebook, and it carries "
                     "the device tier with it: the same walk is MET 3.12 from "
                     "Apple and 5.04 from Validic. Unwrapping to bare text OUTSIDE "
                     "the door throws that away."),
    Shape("04-code-no-codebook", "a number nobody here can read",
          "A vendor enum with no book on this machine. It is parked, not "
          "guessed: the row keeps its value and says why it stopped.",
          {"activities": ["9002"], "source_ids": [24], "minutes": 30, "weight_kg": 70},
          by_kind("opaque_code"),
          sample=sample_kind("opaque_code"), see="5-api-examples/5-misses/opaque-code",
          layer=DEPLOYMENT,
          unwraps_to="nothing: no book on this machine reads it. 106 rows."),
    Shape("05-not-an-event", "a device's midnight total",
          "The largest shape on this board and the one that must never reach a "
          "MET table. A day's steps is not a bout. Filtering these out instead "
          "of typing them would make a cohort that is two thirds roll-up read "
          "as 9%.",
          {"activities": ["20905", "20903"], "source_ids": [20, 20], "minutes": 11},
          by_kind("daily_rollup"),
          sample=sample_kind("daily_rollup"), see="5-api-examples/3-rollups/namespace-matters",
          layer=DEPLOYMENT,
          unwraps_to="nothing, and that is correct. A day's total is not an "
                     "event; in contract form a site would not post it at all. "
                     "It is the reason this noun reports two denominators."),
    Shape("06-named-nothing", "a word that names no activity",
          "'Other' and 'Unknown' are answers a UI gave, not activities. "
          "Returning a MET for them would be inventing one.",
          {"activities": ["Other", "Unknown"], "minutes": 30, "weight_kg": 70},
          by_kind("placeholder"),
          see="5-api-examples/5-misses/named-nothing", sample=sample_kind("placeholder")),
    Shape("07-batch", "several at once, mixed shapes",
          "A call shape rather than a row shape. Order is preserved and each "
          "item keeps its own verdict; one MISS does not spoil its neighbours.",
          {"activities": ["Walking", "20905", "Other", "1001"],
           "source_ids": [1, 20, 1, 23], "minutes": 30, "weight_kg": 70},
          CALL, see="5-api-examples/1-resolves/batch-mixed"),
]

if __name__ == "__main__":
    g = pd.read_parquet(INFO / "2-corpus/gold_index.parquet")
    rows = []
    for t, s in zip(g.ExerciseType.astype(str), g.EntrySourceID):
        sid = None if pd.isna(s) else int(s)
        try:
            kind = parse(t, source_id=sid).kind
        except Exception:
            kind = "error"
        rows.append((kind, bool(re.fullmatch(r"\d+", t))))
    out = build("exercise", INFO, SHAPES, call,
                keep=["ExerciseConf", "METValue", "ActivityCode",
                      "ExerciseSource", "ExerciseBasis", "TypeSource"],
                corpus={"rows": rows, "g": g}, total=len(g), sources=sources,
                verdict=lambda a: f"`{a.get('ExerciseConf')}`"
                + (f" MET {a['METValue']}" if a.get("METValue") else ""))
    print(f"wrote {out}")
