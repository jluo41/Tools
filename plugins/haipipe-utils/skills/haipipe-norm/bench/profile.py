"""What a member declares so the shared benchmark can grade it.

A profile is a RESTATEMENT of the contract in machine-readable form. Every
field here already exists in the member's own `constants.py` as prose or as a
tuple; the profile is where those become checkable.

The point of the two field tuples is that they are DIFFERENT tuples, and a
generic checker that lumped them would be wrong in a way that matters:

    governed   what goes NULL when confidence is not trusted (rule 3).
               Not every value is governed. exercise's ActiveMinutes is the
               LOG's own number and survives a bank miss; medication's DrugKey
               is the SEAM to describe-insulin and rule 9 exists because it
               must survive one too. Nulling those on a miss would be a bug,
               not compliance.

    scaled     what is meaningless without a basis (rule 4). A dose without
               its scale is not a number, so `scaled` non-null implies basis
               non-null. A member with nothing on a scale -- insulin's onset
               and duration are properties of the DRUG, not of an event --
               declares an empty tuple and the check records itself n/a rather
               than silently passing.
"""
import importlib
import pathlib
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

# The members, in chain order: a consumer comes after what it consumes.
MEMBERS = ["food", "exercise", "medication", "insulin"]


@dataclass
class Profile:
    noun: str
    emoji: str
    skill: str                      # the folder under skills/
    door: Callable                  # normalize(items) -> list[dict]

    required: Tuple[str, ...]       # keys present on EVERY result, hit or miss
    governed: Tuple[str, ...]       # rule 3: null whenever conf is untrusted
    scaled: Tuple[str, ...]         # rule 4: non-null implies basis non-null

    conf_field: str
    source_field: str
    basis_field: Optional[str]      # None when the noun has no scale
    conf_order: List[str]           # most-trusted first
    trusted: List[str]              # must be a contiguous PREFIX of conf_order

    port: int                       # which 5-api-examples fixtures are mine
    url_env: str
    dest: pathlib.Path              # the _XInfo folder this member reports into
    examples: pathlib.Path          # where its fixtures live

    probe: Sequence[str]            # plain single-string inputs, for invariants
    adapt: Optional[Callable] = None  # request.json dict -> list[dict]
    optional: Tuple[str, ...] = ()    # documented extra keys, not a violation

    # A fixture this benchmark will not replay, and WHY. It returns a
    # sentence, never a bare True: a skipped case is reported in the run
    # file with its reason, because a benchmark that silently drops the
    # hard cases reads as coverage it does not have.
    skip: Optional[Callable] = None

    # What the CALLER supplied that must come back unchanged, as
    # {door kwarg: (response field, a probe value)}.
    #
    # This is the half of the contract that resolution cannot touch. A log
    # said 30 minutes; whether the bank recognised the activity is a fact
    # about the bank, and it is not a licence to forget the 30. Rule 9 says
    # the seam field must survive a bank miss; so must every echo.
    echo: Dict[str, tuple] = field(default_factory=dict)

    def call(self, request: Dict) -> List[Dict]:
        """Replay one fixture request through the door."""
        if self.adapt is None:
            raise NotImplementedError(f"{self.noun}: no adapt()")
        return self.adapt(request)

    def dict(self) -> Dict:
        return {
            "noun": self.noun, "emoji": self.emoji, "skill": self.skill,
            "required": list(self.required), "governed": list(self.governed),
            "scaled": list(self.scaled), "conf_field": self.conf_field,
            "source_field": self.source_field, "basis_field": self.basis_field,
            "conf_order": list(self.conf_order), "trusted": list(self.trusted),
            "port": self.port, "dest": str(self.dest),
        }


def load_profiles(only: Optional[Sequence[str]] = None) -> List[Profile]:
    """Import each member's declared profile.

    A member is discovered by IMPORT, not by a registry in this file: adding
    describe-<noun> to env.sh's PYTHONPATH and shipping bench_profile.py is the
    whole of registering it, so this file never has to be edited again.
    """
    out = []
    for noun in (only or MEMBERS):
        pkg = {"food": "foodnorm", "exercise": "exnorm",
               "medication": "mednorm", "insulin": "insnorm"}.get(noun, noun)
        mod = importlib.import_module(f"{pkg}.bench_profile")
        out.append(mod.PROFILE)
    return out
