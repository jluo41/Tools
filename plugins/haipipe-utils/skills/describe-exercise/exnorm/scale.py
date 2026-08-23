"""
Stage 2b: the Compendium publishes ONE MET per activity. This is where that
number stops pretending everyone is the same person.

WHY A SCALE TIER EXISTS AT ALL
================================================================================
Measured on 26,738 gradeable WellDoc bouts: the spread of device-measured MET
WITHIN one activity is 1.69, and the spread BETWEEN activities is 1.70. Knowing
which activity it is buys about half of what there is to know. The Compendium
is not wrong -- it is a population table being read as if it were a personal
one.

THE LADDER, WIDEST FLOOR LAST
================================================================================
    person_activity  this person, this activity, enough history   (not yet built)
    person           this person, any activity                    (not yet built)
    device           this EntrySourceID                           ✅ shipped
    population       the Compendium's own number, factor 1.0      the floor

The floor is never removed. A caller who passes nothing gets exactly what this
package returned before the tier existed, and `METScale` says `population` so
they can tell.

WHY DEVICE IS A TIER AND NOT A DETAIL
================================================================================
It looked like a person effect and a third of it is not. Grouping each patient's
own factor by the wearable they mostly use:

    20  Apple           259 patients   median 0.717
    23  Validic_FitBit  105 patients   median 1.207
    25  Validic_Garmin   26 patients   median 0.829

37.5% of the variance in what reads as a 'person factor' is WHICH VENDOR
computed the calories. Apple and FitBit disagree by 68% on the same activity.
That part needs no personal history and no cold start, which is why it ships
first.

THE FENCE (haipipe-norm rule 11)
================================================================================
A bank built from the board is a second path to the label. The device factors
are fit on TRAIN patients and scored on patients the fit never saw. When the
person tier arrives its fence must be TIME instead -- a person's factor may only
use bouts strictly earlier than the bout being scored -- because a patient-hash
split leaves a test patient with no training rows at all and makes a personal
factor unmeasurable by construction.

THE BANK IS FROZEN, NEVER COMPUTED HERE
================================================================================
`benchmark/build_scale_bank.py` writes it, stamped with `as_of` and a row count
per key. This module only reads. Computing a factor at call time would make the
same input return different numbers as data arrived, and the contract's
determinism check (C06) exists to catch exactly that.
"""
import functools
import os
from pathlib import Path
from typing import Optional, Tuple

from .constants import (POPULATION, SCALE_MAX, SCALE_MIN, DEVICE, PERSON,
                        PERSON_ACTIVITY)

# What a missing bank, an unknown key, or a caller who passed nothing all get.
# One triple, one meaning: the Compendium's own number, unmodified.
NO_SCALE: Tuple[float, str, Optional[str]] = (1.0, POPULATION, None)


def _find_bank() -> Path:
    """Same three-step resolution as the Compendium's, for the same reason:
    an explicit path, then the SPACE's declared store, then a walk up."""
    explicit = os.environ.get("EXNORM_SCALE_DB")
    if explicit:
        return Path(explicit)
    rel = Path("exnorm_scale") / "scale.parquet"
    store = os.environ.get("LOCAL_EXTERNAL_STORE")
    roots = []
    if store:
        roots.append(Path(store))
        roots += [anc / store for anc in Path(__file__).resolve().parents]
    roots += [anc / "_WorkSpace" / "ExternalStore"
              for anc in Path(__file__).resolve().parents]
    for r in roots:
        if (r / rel).exists():
            return (r / rel).resolve()
    return (Path("_WorkSpace/ExternalStore") / rel).resolve()


DEFAULT_SCALE_BANK = _find_bank()


@functools.lru_cache(maxsize=8)
def load(path=None) -> dict:
    """{(kind, key): (factor, n, as_of)}. An absent bank is NOT an error -- it
    is a deployment that has not built one, and the floor still works."""
    p = Path(path or DEFAULT_SCALE_BANK)
    if not p.exists():
        return {}
    import pandas as pd
    d = pd.read_parquet(p)
    out = {}
    for r in d.itertuples(index=False):
        f = float(r.factor)
        if not (SCALE_MIN <= f <= SCALE_MAX):
            # A factor outside the band is a builder bug, not a fact about a
            # person. Skip it and fall through rather than ship it.
            continue
        out[(str(r.kind), str(r.key))] = (f, int(r.n), str(r.as_of))
    return out


def _key(v) -> Optional[str]:
    """EntrySourceID arrives as 20, 20.0, '20' and numpy scalars depending on
    who read the parquet. One spelling, or the bank never hits."""
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "nan", "None", "NaN", "<NA>"):
        return None
    try:
        f = float(s)
    except ValueError:
        return s
    if f != f:
        return None
    return str(int(f)) if f == int(f) else s


def factor_for(person_id=None, source_id=None, activity_code=None,
               path=None) -> Tuple[float, str, Optional[str]]:
    """(factor, tier, provenance). Falls through, never raises, never invents.

    Ordered widest-evidence-first. The first tier that has a key wins, and the
    last one always matches because it needs nothing."""
    bank = load(path)
    if not bank:
        return NO_SCALE

    pid, sid, code = _key(person_id), _key(source_id), _key(activity_code)

    for kind, key in ((PERSON_ACTIVITY, f"{pid}|{code}" if pid and code else None),
                      (PERSON, pid),
                      (DEVICE, sid)):
        if key is None:
            continue
        hit = bank.get((kind, key))
        if hit:
            f, n, as_of = hit
            return f, kind, f"scale:{kind}:{key}:n{n}:{as_of}"
    return NO_SCALE
