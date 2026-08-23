"""
The dialect layer: one logged activity, in whatever dialect its cohort wrote it,
becomes a TYPED activity.

TYPING IS THE WHOLE JOB HERE, and it is a bigger job than in describe-food.
A meal string is at least always a meal. An exercise row, measured 260821 over
all 136,555 rows in 1-SourceStore, is one of FOUR different things, and three of
them must never reach a MET table:

    136,555 rows
      88,394  64.7%  a device's DAILY ROLL-UP, posted at midnight        <- not a bout
      13,406   9.8%  a free-text activity name                           <- resolvable
      34,315  25.1%  a vendor's numeric code, no codebook on this box    <- parked
         440   0.3%  'Unknown' / 'Other'                                 <- named nothing

HOW THE ROLL-UPS WERE IDENTIFIED, since 'it looked like one' is not a reason:
codes 20901 / 20903 / 20905 carry 88,394 rows and show, across five cohorts and
four years,

    1.04 rows per patient per DAY          a session count does not do this
    10 distinct times-of-day in 88,394 rows, all 03:59 or 04:59
                                           local midnight, offset by timezone
    CaloriesBurned == 0 in 100.0% of them  a tracker that measured a workout
                                           would have reported its energy

Pricing one of those as a bout says a patient did a single 11-minute workout
every day for four years, and never burned a calorie doing it. Rule 2 of
haipipe-norm applies: TYPE it, do not drop it. A caller that wants daily active
minutes should read ExerciseDuration itself; this normalizer will not launder a
daily total into a session.

THE CODE SPACES ARE NOT ONE CODE SPACE
================================================================================
A cohort's ExerciseType is only meaningful together with the EntrySourceID that
issued it. Measured over 220,528 raw WellDoc rows, EntrySourceID partitions the
129 distinct codes into four vendor namespaces that are disjoint but for a single
code, `25`, and that one collides 5,848 rows against 1:

    EntrySourceID 20              58 codes   20001..20905     172,407 rows
    EntrySourceID 23/24/25/34/36  35 codes   1..25, 1001..     35,041 rows
    EntrySourceID 1/2             13 codes   100..111          10,092 rows
    EntrySourceID 37/40           24 codes   30001..30122       2,988 rows

None of the four codebooks is on this machine, so every numeric code is typed
OPAQUE_CODE and parked. That is a KNOWN unknown, and it is deliberately NOT the
same value as a bank miss: 'nobody here has the vendor's dictionary' and 'the
compendium does not list this activity' are different failures with different
fixes, and rule 5 says they may not share a column.

AND THE COMPENDIUM'S CODES ARE A FIFTH CODE SPACE
================================================================================
The PA Compendium also uses 5-digit codes, and three of them collide with
EntrySourceID-20 codes by pure coincidence:

    WellDoc 20050   median 42 min, 242 kcal   |  Compendium 20050  'Eating at church', MET 1.5
    WellDoc 20037   median 32 min, 204 kcal   |  Compendium 20037  'Walking, 2.8-3.4 mph'
    WellDoc 20020   median 30 min, 142 kcal   |  Compendium 20020  'Standing, singing in church'

Joining on the bare integer would price 1,218 real workouts as eating at church.
`reject_code_join` exists to make that join impossible rather than discouraged,
and test_exnorm covers all three.
"""
import re
from collections import namedtuple
from typing import Optional

from . import codebooks
from .constants import SESSION, DAILY_ROLLUP, PLACEHOLDER, OPAQUE_CODE

# What the dialect layer hands to retrieval.
#   kind      one of constants.TYPES
#   name      the canonical lowercase activity name, or None when there is none
#   raw       exactly what came in, never modified. a caller must always be able
#             to get back to the log's own words.
#   namespace the vendor enum this row's code belongs to, or None for free text
#   via       HOW the name was obtained: 'text' when the log wrote words, or
#             'codebook:<book>' when a vendor code was translated. Rule 5: a
#             name read off a code and a name a patient typed are not the same
#             evidence, and a reader must be able to tell them apart.
Activity = namedtuple("Activity", "kind name raw namespace via")

# EntrySourceID -> vendor namespace. Grouped by the measurement above, not by
# guessing which vendor is which: the grouping is what the data supports, the
# vendor names are what it does not.
SOURCE_NAMESPACE = dict(codebooks.SOURCE_TO_BOOK)

# The three EntrySourceID-20 codes proven to be daily roll-ups.
# Keyed by (namespace, code) and not by code alone, because a bare '20903' from
# some other vendor is a different thing and must not inherit this verdict.
ROLLUP_CODES = {("apple", c) for c in codebooks.APPLE_ROLLUP}

# Free text that names no activity. Typed, never sent to a bank -- there is
# nothing there to match, so any match would be wrong.
PLACEHOLDER_TEXT = {"unknown", "other", "", "none", "n/a", "na", "null", "nan",
                    # a code book's own word for 'nothing named'. Validic 25 is
                    # 'Other' and carries 3,308 rows; sending it to a bank can
                    # only produce a wrong match.
                    "generic", "sedentary"}

_CODE_RE = re.compile(r"^\d+$")
# 'src20:20903' -- how a caller passes a namespace through the string door.
_NS_RE = re.compile(r"^(?:src)?(\d+)\s*:\s*(.+)$", re.I)

# Free text as five cohorts spell it, folded to the compendium's own words.
# 32 distinct values measured over 13,406 rows; the map is written out in full
# rather than derived, because 'Dancing__Aerobics' is not a rule, it is a fact
# about one exporter.
TEXT_CANON = {
    "walk": "walking", "walking": "walking", "treadmill": "walking, treadmill",
    "hike": "hiking", "hiking": "hiking",
    "run": "running", "running": "running",
    "bike": "bicycling", "bicycling": "bicycling", "outdoor bike": "bicycling",
    "swim": "swimming", "swimming": "swimming",
    "yoga": "yoga", "yoga_pilates": "yoga",
    "strength_training": "resistance training", "strengthtraining": "resistance training",
    "weights": "resistance training",
    "aerobic workout": "aerobics", "cardiovascular": "aerobics",
    "dancing__aerobics": "dancing", "dancing": "dancing",
    "elliptical": "elliptical trainer",
    "bootcamp": "circuit training",
    "home_activities": "home activities", "gardening__lawn": "gardening",
    "skiing__skating": "skiing", "tennis": "tennis", "golf": "golf",
    "sports": "sports", "sport": "sports", "workout": "conditioning exercise",
}


def reject_code_join(code: str) -> None:
    """Raise rather than let a cohort's ExerciseType be looked up as a PA
    Compendium activity_code. They are unrelated code spaces that overlap.

    This is a function and not a comment because the collision is silent: the
    join succeeds, returns a plausible row, and prices a workout as church.
    """
    raise ValueError(
        f"{code!r} is a COHORT code, not a PA Compendium activity_code. "
        "The two code spaces overlap by coincidence (WellDoc 20050 is a 42-min "
        "workout; Compendium 20050 is 'Eating at church'). Resolve the cohort "
        "codebook first; see describe-exercise/SKILL.md, PARKED."
    )


def _fold(s: str) -> str:
    """lowercase, underscores to spaces, whitespace collapsed. Nothing else."""
    return " ".join(str(s).strip().lower().replace("_", " ").split())


# The lookup is keyed on FOLDED keys, built once at import. The alternative --
# folding the query and then trying the raw key, then an un-folded variant of it
# -- silently lost 264 rows: 'Dancing__Aerobics' folds to 'dancing aerobics' and
# no amount of putting the underscores back reproduces the double underscore in
# the literal key. Fold both sides with the same function, once.
_FOLDED_CANON = {_fold(k): v for k, v in TEXT_CANON.items()}


def canonical(label: str) -> str:
    """Fold one activity label -- a patient's words or a code book's -- to the
    single canonical name that alias_dict.py is keyed on.

    ONE fold for both, deliberately. Apple calls it 'walking', Validic calls it
    'Walking', a WellDoc user typed 'Walk', and mcphases exported
    'Yoga_Pilates'. Four dialects, one activity, and therefore one curated
    Compendium pick to maintain instead of four."""
    f = _fold(label)
    return _FOLDED_CANON.get(f, f)


def _lookup(code: str, book: str):
    """A vendor code -> its own book's label, or None. Never another book's.

    The prefix arithmetic lives in codebooks.decode, because the benchmark's
    taxonomy needs the same answer and must not reimplement it."""
    return codebooks.decode(code, book)


def parse(raw, source_id=None) -> Activity:
    """Type one logged activity. Never raises, never drops, never guesses.

    raw        the ExerciseType as logged: 'Walking', '20903', or 'src20:20903'
    source_id  the row's EntrySourceID, when the caller still has it. Without it
               a numeric code cannot be placed in a namespace, and this function
               says so instead of picking one.
    """
    original = raw
    text = "" if raw is None else str(raw).strip()

    namespace = SOURCE_NAMESPACE.get(int(source_id)) if source_id is not None \
        and str(source_id).strip() not in ("", "nan", "None") else None

    m = _NS_RE.match(text)
    if m and _CODE_RE.match(m.group(2).strip()):
        namespace = SOURCE_NAMESPACE.get(int(m.group(1)), f"src{m.group(1)}")
        text = m.group(2).strip()

    low = _fold(text)
    if low in PLACEHOLDER_TEXT:
        return Activity(PLACEHOLDER, None, original, namespace, "text")

    if _CODE_RE.match(text):
        if (namespace, text) in ROLLUP_CODES:
            return Activity(DAILY_ROLLUP, None, original, namespace, None)
        if namespace == "apple" and text == codebooks.APPLE_UNMAPPED:
            # 20999, 1,074 rows. Its shape is a real bout -- 695 distinct times
            # of day, median 33 minutes, kcal present in 95.9% -- but Apple's
            # enum has no case for it, so it is WellDoc's bucket for a workout
            # whose type did not map. Nothing was named. That is a placeholder,
            # NOT a missing code book: no dictionary will ever decode it.
            return Activity(PLACEHOLDER, None, original, namespace, "codebook:apple")

        label = _lookup(text, namespace) if namespace else None
        if label is None:
            return Activity(OPAQUE_CODE, None, original, namespace, None)
        via = f"codebook:{namespace}"
        if canonical(label) in PLACEHOLDER_TEXT:
            # The book's own word for 'nothing named' -- Validic 25 is 'Other',
            # 3,308 rows. Decoded successfully, and still names no activity.
            return Activity(PLACEHOLDER, None, original, namespace, via)
        return Activity(SESSION, canonical(label), original, namespace, via)

    return Activity(SESSION, canonical(text), original, namespace, "text")
