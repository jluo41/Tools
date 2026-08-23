"""
The corpus taxonomy for describe-exercise: two ORTHOGONAL axes over every
Exercise row on the board.

    KIND    a property of the row. What the log is even claiming.
    LABEL   a property of the numbers. What we may grade against.

KIND IS NOT A DETAIL HERE, IT IS THE HEADLINE. 88,467 of 136,555 rows are
daily device roll-ups -- a whole day's movement under one activity name -- and
5,289 more are placeholders. Counting either as a failed match measures the
shape of the log, not the resolver: it is the difference between an 8.6%
headline and a 95% one.

This file classifies from the CODEBOOKS ONLY, never by calling the resolver.
The corpus must be a fact about the data; if it moved when dialect.py moved,
every stored run would silently stop being comparable.
"""
import re

from exnorm import codebooks

# ── KIND ─────────────────────────────────────────────────────────────────────
SESSION      = "session"        # one bout, a named activity
DAILY_ROLLUP = "daily_rollup"   # a device's whole-day total wearing an activity name
PLACEHOLDER  = "placeholder"    # 'Other', 'Unmapped' -- the log named nothing
OPAQUE_CODE  = "opaque_code"    # a vendor code with no codebook on this machine

_PLACEHOLDER_TEXT = {"other", "unknown", "none", "nan", "n/a", "", "unmapped"}
_WS = re.compile(r"\s+")


def _fold(s):
    return _WS.sub(" ", str(s).strip().lower().replace("_", " "))


def classify_kind(row):
    """One Exercise row -> one KIND. Never raises."""
    raw = row.get("ExerciseType")
    src = row.get("EntrySourceID")
    s = "" if raw is None else str(raw).strip()
    if not s or _fold(s) in _PLACEHOLDER_TEXT:
        return PLACEHOLDER

    book = codebooks.SOURCE_TO_BOOK.get(src if src is None else int(src)) \
        if str(src).strip() not in ("", "None", "nan") else None
    if not s.lstrip("-").isdigit():
        # free text. Trust the words.
        return PLACEHOLDER if _fold(s) in _PLACEHOLDER_TEXT else SESSION
    if book is None:
        return OPAQUE_CODE
    if book == "apple":
        if s in codebooks.APPLE_ROLLUP:
            return DAILY_ROLLUP
        if s == codebooks.APPLE_UNMAPPED:
            return PLACEHOLDER
    label = codebooks.decode(s, book)
    if label is None:
        return OPAQUE_CODE
    return PLACEHOLDER if _fold(label) in _PLACEHOLDER_TEXT else SESSION


# ── LABEL ────────────────────────────────────────────────────────────────────
DEVICE_MET   = "device_met"     # kcal + duration + a body mass -> a MET we can grade
DURATION_ONLY = "duration_only" # a bout length, no energy figure
NO_LABEL     = "no_label"

# Only this carries a number independent of the Compendium.
GRADEABLE = {DEVICE_MET: ("MET_device",)}

# WHY THERE IS NO `derived` CLASS HERE, AND WHY THAT IS NOT AN OVERSIGHT
# ============================================================================
# describe-food needed one because the library had been wired into a cohort's
# cook. Nothing writes into Exercise.parquet, so no row's label is our own
# output. The OTHER circularity -- rule 11, a bank harvested from the board --
# also does not apply: the PA Compendium is a published table of indirect-
# calorimetry measurements and has never seen a WellDoc patient.
#
# The question that DID have to be answered is whether the vendors' logged
# kcal is itself a MET-table lookup, which would make the gold the prediction
# wearing a different hat. Measured 260822 on 24,047 rows: within one
# (vendor, activity) pair the implied MET has a coefficient of variation of
# 0.21-0.51, median 0.31-0.37 per vendor. A table lookup would give 0.00.
# Every vendor derives its figure from sensors. The gold is independent.

MIN_MET, MAX_MET = 0.5, 25.0


def classify_label(row, _derived=None):
    """A row's numbers -> one LABEL class."""
    met = row.get("MET_device")
    try:
        met = float(met)
    except (TypeError, ValueError):
        met = None
    if met is not None and met == met and MIN_MET <= met <= MAX_MET:
        return DEVICE_MET
    try:
        dur = float(row.get("ExerciseDuration"))
    except (TypeError, ValueError):
        dur = None
    if dur is not None and dur == dur and dur > 0:
        return DURATION_ONLY
    return NO_LABEL
