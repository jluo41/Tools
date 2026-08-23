"""
The DataFrame path, for a SourceFn that has a whole Exercise frame in hand.

It is a thin wrapper over the door and adds exactly one thing: it never mutates
a caller's column. describe-food learned that the hard way -- its stage 0 wrote
resolved names back over FoodName, so the log's own words were gone and no
audit could ever recover what the patient typed.
"""
from typing import Optional

from .client import normalize
from .constants import FIELDS


def enrich_exercise(df, type_col: str = "ExerciseType",
                    minutes_col: Optional[str] = "ExerciseDuration",
                    weight_col: Optional[str] = None,
                    source_col: Optional[str] = "EntrySourceID",
                    person_col: Optional[str] = "PatientID",
                    weight_kg=None, **kw):
    """Return a COPY of df with the 14 exnorm columns appended.

    A column named here but absent from the frame is treated as not stated,
    which is the honest reading -- a frame that lost EntrySourceID in a
    whitelist (see SKILL.md, PARKED) genuinely no longer knows the namespace,
    and must not have one inferred for it.
    """
    out = df.copy()
    col = lambda c: out[c].tolist() if c and c in out.columns else None
    rows = normalize(out[type_col].astype(str).tolist(),
                     minutes=col(minutes_col),
                     weight_kg=col(weight_col) if weight_col else weight_kg,
                     source_ids=col(source_col),
                     person_ids=col(person_col), **kw)
    for f in FIELDS:
        out[f] = [r[f] for r in rows]
    return out
