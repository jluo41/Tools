"""
NounSpec -- everything xbench needs to know about one noun, and nothing more.

The seam is deliberately narrow. xbench never names a macro, a MET, or an
insulin class; a noun never writes a split rule, a cell loop, or a JSON layout.
If a field here starts describing HOW to grade rather than WHAT the columns
are, it belongs in the noun's own metric callable instead.
"""
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Tuple


@dataclass(frozen=True)
class NounSpec:
    # ── identity ────────────────────────────────────────────────────────────
    noun: str                      # "food" | "exercise" | "medication" | "insulin"
    frame: str                     # typed frame stem: 1-SourceStore/*/@*/<frame>.parquet

    # ── columns of the SOURCE frame ─────────────────────────────────────────
    text_col: str                  # the string being resolved; also the dedup key
    id_cols: Tuple[str, ...]       # carried through so a row can be found again
    label_cols: Tuple[str, ...]    # the self-gold columns, renamed true_<col>
    extra_cols: Tuple[str, ...] = ()   # anything classify_shape needs (ImagePath…)

    # ── columns the NORMALIZER returns ──────────────────────────────────────
    conf_col: str = ""             # e.g. NutritionConf. Coverage = != "MISS"
    basis_col: str = ""            # e.g. NutritionBasis. May be "" if the noun has none
    derived_col: Optional[str] = None
    # ^ the column whose mere presence proves the normalizer wrote this row.
    #   Non-null => the row is circular and can never be graded on VALUE.

    # ── the taxonomy ────────────────────────────────────────────────────────
    classify_shape: Callable = None      # (row: dict) -> shape str
    classify_label: Callable = None      # (row: dict, derived_value) -> label str
    gradeable: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    derived_label: str = "derived"

    circular_conf: Tuple[str, ...] = ()
    # ^ CONFIDENCE VALUES THAT MEAN "THE BANK HANDED BACK THE LABEL".
    #   The derived_col rule catches circularity in the FRAME: the normalizer
    #   wrote this row, so never grade it. This catches circularity in the
    #   BANK: the row is honest, but the reference contains the very number we
    #   are about to score against, so the score is memorisation.
    #
    #   Found 260822, the first hour xbench existed. describe-food had gained a
    #   T0 tier that looks a meal up in a bank harvested from the board's own
    #   logged rows; 20.8% of test-split food names the train split never saw
    #   were in it. Graded naively the resolver read r 0.988 on a cell whose
    #   frozen baseline was r 0.821.
    #
    #   These rows are NOT dropped -- rule 2 -- they are scored separately and
    #   the headline is the non-circular half.

    # ── the work ────────────────────────────────────────────────────────────
    augment: Callable = None
    # ^ (df, cohort) -> df, called on each cohort's frame BEFORE classification.
    #   For a noun whose label is not a column of its own frame. describe-
    #   exercise's gold is a MET back-solved from logged kcal, duration and a
    #   body mass that lives in Weight.parquet; without this hook the label
    #   would have to be precomputed by hand and the corpus would stop being
    #   reproducible from the store alone.
    normalize: Callable = None     # (DataFrame) -> same rows + conf/basis/value cols
    metric: Callable = None        # (enriched: DataFrame, label: str) -> dict
    # ^ metric receives truth as true_<label_col> and prediction under the
    #   normalizer's own names. It returns whatever the noun considers a score;
    #   xbench stores it verbatim and never interprets it.

    def check(self):
        """Fail loudly at import, not three minutes into a run."""
        if self.derived_label in self.gradeable:
            raise ValueError(
                f"{self.noun}: {self.derived_label!r} is in gradeable. Those rows "
                f"were written BY the normalizer; grading them is circular. This "
                f"is xbench's one non-negotiable rule.")
        for fn in ("classify_shape", "classify_label", "normalize", "metric"):
            if getattr(self, fn) is None:
                raise ValueError(f"{self.noun}: NounSpec.{fn} is required")
        if not self.gradeable:
            raise ValueError(f"{self.noun}: nothing is gradeable; a benchmark of "
                             f"coverage alone must still declare its cells")
        return self
