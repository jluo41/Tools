"""Lazy access to the WellDoc MedicationID lexicon.

The insulin door normally consumes ``DrugKey`` (a name), but WellDoc's raw
shape hands the chain an integer ``MedicationID``.  The medication resolver
already owns this lookup; this small, optional reader lets the second half
honour the same E2_LEXICON seam when it is called directly with that id.

The parquet file is loaded only when a numeric id is requested.  Name-only
uses therefore keep describe-insulin's lightweight, standalone behaviour, and
an absent/unreadable external store is an honest lexicon miss rather than a
service import failure.
"""
import os
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional


def _candidate_paths():
    """Yield the configured or workspace-local lexicon locations."""
    explicit = os.environ.get("INSNORM_LEXICON")
    if explicit:
        p = Path(explicit).expanduser()
        yield p / "med_lexicon.parquet" if p.is_dir() else p

    # Honour the medication skill's existing external-store setting too.  It
    # is the same MedicationID namespace and avoids a second configuration for
    # callers that run both halves of the chain.
    store = os.environ.get("LOCAL_EXTERNAL_STORE")
    if store:
        yield Path(store) / "medbank" / "med_lexicon.parquet"

    med_db = os.environ.get("MEDNORM_DB")
    if med_db:
        p = Path(med_db).expanduser()
        yield p / "medbank" / "med_lexicon.parquet" if p.is_dir() else p

    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        yield parent / "_WorkSpace" / "ExternalStore" / "medbank" / "med_lexicon.parquet"


def _path() -> Optional[Path]:
    seen = set()
    for candidate in _candidate_paths():
        candidate = candidate.resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_file():
            return candidate
    return None


def _id(value) -> Optional[str]:
    """Canonicalize the integer-shaped ids used by WellDoc."""
    text = str(value or "").strip()
    if text.isdigit():
        return str(int(text))
    if text.endswith(".0") and text[:-2].isdigit():
        return str(int(text[:-2]))
    return None


@lru_cache(maxsize=1)
def _entries() -> Dict[str, str]:
    path = _path()
    if path is None:
        return {}
    try:
        import pandas as pd

        frame = pd.read_parquet(path)
    except Exception:
        return {}

    id_col = next((c for c in ("MedicationID", "unit") if c in frame), None)
    name_col = next((c for c in ("MedicationName", "unit_text") if c in frame), None)
    if id_col is None or name_col is None:
        return {}

    out = {}
    for raw_id, name in zip(frame[id_col], frame[name_col]):
        key = _id(raw_id)
        text = str(name or "").strip()
        if key and text and text.lower() not in ("nan", "none"):
            out.setdefault(key, text)
    return out


def lookup(value) -> Optional[str]:
    """Return the MedicationName/unit_text for one MedicationID."""
    key = _id(value)
    return _entries().get(key) if key else None


def known(value) -> bool:
    """Whether the configured lexicon contains the id (useful in diagnostics)."""
    key = _id(value)
    return bool(key and key in _entries())
