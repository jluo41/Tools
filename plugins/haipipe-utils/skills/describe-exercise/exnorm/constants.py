"""
The fixed vocabulary of this normalizer: what a row can BE, how sure we are,
and on what scale a number is reported.

Nothing here is measured or tuned. Anything that varies by dataset lives in
alias_dict.py; anything that varies by deployment lives in an env var.
"""
import os
from pathlib import Path

# ---------------------------------------------------------------- the bank ---
# The PA Compendium 2024, next to usda_fdc in ExternalStore. Resolution order:
#   1. EXNORM_DB              an explicit path. how a service on another host,
#                             or an A/B against a newer compendium, is done.
#   2. $LOCAL_EXTERNAL_STORE  set by the workspace env.sh. A SPACE declares where
#                             its stores are; this package does not guess.
#   3. walk up from this file to the repo root.
#                             the fallback for someone who imported the package
#                             without sourcing anything, e.g. a bare pytest run.
def _find_bank() -> Path:
    explicit = os.environ.get("EXNORM_DB")
    if explicit:
        return Path(explicit)
    rel = Path("pa_compendium") / "compendium_2024.csv"
    store = os.environ.get("LOCAL_EXTERNAL_STORE")
    roots = []
    if store:
        roots.append(Path(store))
        # LOCAL_EXTERNAL_STORE is relative to the repo root, not to cwd.
        roots += [anc / store for anc in Path(__file__).resolve().parents]
    roots += [anc / "_WorkSpace" / "ExternalStore"
              for anc in Path(__file__).resolve().parents]
    for r in roots:
        if (r / rel).exists():
            # ALWAYS absolute. A relative hit here resolves only while the
            # process happens to sit in the repo root, and a service that must
            # be startable from anywhere cannot depend on its own cwd.
            return (r / rel).resolve()
    return (Path("_WorkSpace/ExternalStore") / rel).resolve()  # a readable error later, not a crash here


DEFAULT_BANK = _find_bank()

# ------------------------------------------------------------- what a row IS --
# Rule 2 of haipipe-norm: TYPE, DO NOT DELETE. Every input leaves the dialect
# layer wearing exactly one of these. Only `session` may reach the bank.
SESSION = "session"            # a bounded bout of activity. resolvable.
DAILY_ROLLUP = "daily_rollup"  # a device's once-a-day summary posted at midnight.
                               #   NOT an exercise event. 88,394 of 136,555
                               #   WellDoc rows. Reaching the bank with one of
                               #   these prices a whole day as a single workout.
PLACEHOLDER = "placeholder"    # 'Unknown', 'Other'. Logged, never named.
OPAQUE_CODE = "opaque_code"    # a vendor enum with no codebook on this machine.
                               #   Parked, pending the WellDoc codebook. It is
                               #   a KNOWN unknown and must not read as a miss
                               #   of the bank's, which is a different failure.
TYPES = (SESSION, DAILY_ROLLUP, PLACEHOLDER, OPAQUE_CODE)

# ------------------------------------------------------------- how sure we are --
# Rule 3: only GOOD / OK / ALIAS may be written into value columns.
# GOOD is currently UNREACHABLE and that is deliberate -- see retrieve.CONF_CAP.
GOOD, OK, ALIAS, WEAK, MISS = "GOOD", "OK", "ALIAS", "WEAK", "MISS"
TRUSTED = (GOOD, OK, ALIAS)

# ------------------------------------------------------------------ the scale --
# Rule 4: BASIS IS A COLUMN. MET is a RATE; kcal is a DOSE. Turning one into the
# other needs BOTH minutes and body mass, and a log that states neither gets the
# rate and a basis saying so -- never a dose with an invented denominator.
PER_SESSION = "per_session"    # kcal for this bout. minutes AND weight known.
PER_MINUTE = "per_minute"      # MET only. the bout's length or the body is not known.
BASES = (PER_SESSION, PER_MINUTE, None)

# ------------------------------------------------------------- whose MET is it --
# A SECOND axis, and not the same one as BASIS. Basis says rate-or-dose; this
# says WHOSE rate. The Compendium publishes one MET per activity for a
# population, and reading that as this person's number is the largest remaining
# error in this normalizer: within one activity the device-measured spread is
# 1.69 MET, between activities it is 1.70. Naming the activity buys half.
#
# POPULATION is the floor and is what a caller who passes no identity gets, so
# adding this axis changed no existing behaviour. See scale.py for the ladder
# and for the fence each tier has to clear.
POPULATION = "population"            # the Compendium's own number. factor 1.0.
DEVICE = "device"                    # this EntrySourceID's median bias.
PERSON = "person"                    # this patient, across activities.
PERSON_ACTIVITY = "person_activity"  # this patient doing this activity.
SCALES = (POPULATION, DEVICE, PERSON, PERSON_ACTIVITY)

# A factor outside this band is a builder bug wearing a plausible value. Clipped
# where the bank is built and refused again where it is read.
SCALE_MIN, SCALE_MAX = 0.4, 2.5

# kcal/min = MET * 3.5 mL O2/kg/min * kg / 200        (1 L O2 ~ 5 kcal)
VO2_REST_ML_KG_MIN = 3.5
KCAL_PER_L_O2 = 5.0

# The longest bout we will multiply through. A POLICY, stated here rather than
# buried, and overridable with EXNORM_MAX_BOUT_MINUTES.
#
# Found by running all 136,555 real rows, which is the only way it could have
# been found: a log claiming a 4,680-minute walk produced 18,829 kcal, and the
# absurd number was OURS -- MET x mass x THEIR duration. The MET is still right
# (walking is walking however long you claim to have done it) and the duration
# is still reported; only the DOSE is withheld, and the basis drops to
# per_minute to say so. Rule 3: a confidently wrong value is worse than a
# missing one, and rule 4: never produce a dose you cannot stand behind.
#
# 240 is chosen on physiology, not on chasing a percentile. It caps the largest
# estimate at 3,726 kcal, inside an adult's whole-day total energy expenditure,
# and costs 180 of 31,724 dosed rows. Measured alternatives, if a consumer wants
# a different trade:
#
#     limit   rows losing kcal   share    largest surviving estimate
#       120                829   2.61%                   1,786 kcal
#       240                180   0.57%                   3,726 kcal   <- default
#       480                 88   0.28%                   4,984 kcal
#      1440                  2   0.01%                  18,882 kcal
#
# These are user data-entry errors, not a hidden class: the durations decay
# smoothly with no spike at a day boundary and appear in every cohort and every
# EntrySourceID. So they are NOT typed as something new; only the dose is refused.
MAX_BOUT_MINUTES = float(os.environ.get("EXNORM_MAX_BOUT_MINUTES", "240"))

# The 14 fields every result carries, in order. A caller reads this, not a
# hand-written list somewhere else.
#
# METValue is ALWAYS THE BEST ESTIMATE AVAILABLE, so a consumer never writes a
# branch to find the good number -- that was the whole reason not to bolt the
# scaled MET on as a second optional column. METReference always carries the
# Compendium's published value for ActivityCode, so the adjustment is auditable
# and reversible, and METScale names which rung produced it.
VALUES = ("METValue", "ActiveMinutes", "CaloriesBurnedEst")
IDENTITY = ("ActivityResolved", "ActivityCode", "MajorHeading")
SCALE = ("METReference", "METScale", "METScaleFactor")
PROVENANCE = ("ExerciseSource", "ExerciseConf", "ExerciseBasis",
              "TypeSource", "TypeConf")
FIELDS = VALUES + IDENTITY + SCALE + PROVENANCE
