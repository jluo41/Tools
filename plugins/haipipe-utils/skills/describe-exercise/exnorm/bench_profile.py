"""How describe-exercise declares itself to the shared B1 benchmark.

Nothing here is new information. Every tuple restates something already in
`constants.py`; the profile is where prose becomes checkable.
"""
import pathlib

from bench import Profile

from . import normalize
from .constants import BASES, IDENTITY, PROVENANCE, TRUSTED, VALUES

ROOT = pathlib.Path(__file__).resolve().parents[6]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo"


def _adapt(req):
    """A fixture request is the service's body; the door takes the same
    arguments by another name. `activity` is the single form, `activities`
    the batch -- the API offers both and B1 replays whichever the fixture used.
    """
    acts = req.get("activities", [req["activity"]] if "activity" in req else [])
    return normalize(acts,
                     minutes=req.get("minutes"),
                     weight_kg=req.get("weight_kg"),
                     source_ids=req.get("source_ids", req.get("source_id")))


PROFILE = Profile(
    noun="exercise", emoji="🏃", skill="describe-exercise",
    door=normalize,
    required=VALUES + IDENTITY + PROVENANCE,

    # Rule 3 governs VALUE columns, and IDENTITY is deliberately not one of
    # them here. 'Sports' head-anchors onto 'Sports spectator, very excited' at
    # a perfect score; the skill caps it at WEAK and KEEPS the candidate so a
    # person can curate it -- 5-misses/category-word says so in as many words.
    # A candidate a human is meant to read is not a value a pipeline may write.
    #
    # ActiveMinutes is not governed either, for the opposite reason: it is the
    # log's own duration, not the bank's answer.
    governed=("METValue", "CaloriesBurnedEst"),

    # A MET is a rate and a kcal is a dose; neither is readable without knowing
    # which. This is the whole of rule 4 for this noun.
    scaled=("METValue", "CaloriesBurnedEst"),

    conf_field="ExerciseConf", source_field="ExerciseSource",
    basis_field="ExerciseBasis",
    conf_order=["GOOD", "OK", "ALIAS", "WEAK", "MISS"],
    trusted=list(TRUSTED),

    port=8078, url_env="EXNORM_URL",
    dest=INFO / "6-benchmark", examples=INFO / "5-api-examples",

    # Deliberately mixed: one that resolves cleanly, one multi-word, one the
    # bank does not have, one CATEGORY word (rule 7), one placeholder (rule 2).
    probe=["Walking", "Yoga", "Strength_training", "Sports", "Unknown"],
    adapt=_adapt,

    # The log said 30 minutes. The Compendium has no opinion about that.
    echo={"minutes": ("ActiveMinutes", 30.0)},
)
