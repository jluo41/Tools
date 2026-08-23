"""The _XInfo folder writer. See __init__.py for why it is shared."""
import json
import os
import pathlib
import shutil
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

SCHEMA = pathlib.Path(__file__).resolve().parent / "schema.json"

# The five layers every _XInfo folder has, in this order, with the same meaning
# for every noun. A member that has nothing for a layer leaves it absent rather
# than inventing a different name for it.
LAYERS = {
    "1-per-cohort": "one page per cohort: what goes in, and what comes out",
    "2-corpus":     "the gradeable subset, its gold, and the current baseline",
    "3-reference":  "symlinks to the banks in ExternalStore. never copies",
    "4-contract":   "the record's JSON Schema and worked specimens, all real rows",
    "5-api-examples": "real request/response pairs against the running service",
}

# There is no ONE confidence vocabulary, and trying to impose one was wrong.
# describe-food ranks MEASURED / ESTIMATED / MISS -- did the value come from a
# measurement or from a model. describe-medication ranks GOOD / OK / ALIAS /
# WEAK / MISS -- how likely the match is to be right. Different questions.
# A calibration benchmark does not need the same words; it needs a DECLARED
# ORDER, so each member ships its own and the shared code reads it.
DEFAULT_CONF_ORDER = ["GOOD", "OK", "ALIAS", "WEAK", "MISS"]


@dataclass
class CohortStats:
    """One cohort's entry. Field order matches schema.json."""
    noun: str
    cohort: str
    rows: int
    patients: Optional[int] = None
    kinds: Dict[str, int] = field(default_factory=dict)
    denominator: Dict = field(default_factory=dict)
    coverage: Dict[str, int] = field(default_factory=dict)
    confidence: Dict[str, int] = field(default_factory=dict)
    basis: Dict[str, int] = field(default_factory=dict)
    gradeable: Dict[str, int] = field(default_factory=dict)
    confidence_order: List[str] = field(default_factory=list)
    trusted: List[str] = field(default_factory=list)
    origin: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def dict(self) -> Dict:
        d = asdict(self)
        return {k: v for k, v in d.items() if v not in (None, {}, [])}

    # -- convenience readers, so every renderer computes these the same way --
    @property
    def resolvable(self) -> int:
        return self.denominator.get("resolvable", self.rows)

    @property
    def written(self) -> int:
        return self.coverage.get("value_written", 0)

    @property
    def rate(self) -> Optional[float]:
        """Coverage over the HONEST denominator, never over rows."""
        d = self.resolvable
        return (self.written / d) if d else None


def validate(stats: List[CohortStats]) -> List[str]:
    """Return a list of problems. Empty means conforming.

    Arithmetic, not taste: the two sums that must hold are the ones a reader
    will silently assume and that nothing else checks.
    """
    problems = []
    for s in stats:
        p = f"{s.noun}/{s.cohort}"
        if s.kinds and sum(s.kinds.values()) != s.rows:
            problems.append(f"{p}: kinds sum to {sum(s.kinds.values())}, rows is {s.rows}")
        if s.denominator:
            if "resolvable" not in s.denominator:
                problems.append(f"{p}: denominator has no 'resolvable'")
            else:
                tot = s.denominator["resolvable"] + sum(
                    s.denominator.get("excluded", {}).values())
                if tot != s.rows:
                    problems.append(
                        f"{p}: resolvable + excluded = {tot}, rows is {s.rows}")
        if s.confidence:
            order = s.confidence_order or DEFAULT_CONF_ORDER
            if not s.confidence_order:
                problems.append(
                    f"{p}: confidence present with no confidence_order. A "
                    f"confidence column nobody can rank is decoration.")
            bad = set(s.confidence) - set(order)
            if bad:
                problems.append(f"{p}: confidence keys {sorted(bad)} are not in "
                                f"confidence_order {order}")
            if s.trusted and not all(t in order for t in s.trusted):
                problems.append(f"{p}: trusted {s.trusted} not a subset of order")
            if s.trusted and list(s.trusted) != order[:len(s.trusted)]:
                problems.append(
                    f"{p}: trusted {s.trusted} is not a PREFIX of "
                    f"confidence_order {order}; rule 3 requires the trusted "
                    f"levels be the most-trusted ones, contiguously")
            if sum(s.confidence.values()) != s.rows:
                problems.append(
                    f"{p}: confidence sums to {sum(s.confidence.values())}, rows is {s.rows}")
        if s.written > s.resolvable:
            problems.append(
                f"{p}: value_written {s.written} exceeds resolvable {s.resolvable}")
    return problems


def pct(n, d) -> str:
    return f"{n / d:6.1%}" if d else "     -"


def block(lines) -> str:
    return "```text\n" + "\n".join(lines) + "\n```"


def link_reference(dest: pathlib.Path, name: str, target: pathlib.Path):
    """3-reference is symlinks, never copies. usda_fdc alone is 128 MB and
    _WorkSpace is not a git tree, so a copy is dead weight nobody can diff."""
    d = dest / "3-reference"
    d.mkdir(parents=True, exist_ok=True)
    link = d / name
    if link.is_symlink() or link.exists():
        link.unlink()
    os.symlink(os.path.relpath(target, d), link)


def copy_api_examples(dest: pathlib.Path, src: pathlib.Path) -> int:
    """Copy a skill's generated request/response pairs into 5-api-examples.

    The GENERATOR stays in the skill, under git. Only its output lands here,
    which is the same rule 3-reference follows and the same one _FoodInfo's
    README states: `_WorkSpace` is not a git tree, so nothing whose history
    matters may live in it -- only regenerable artifacts."""
    if not src.exists():
        return 0
    out = dest / "5-api-examples"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)
    return sum(1 for _ in out.rglob("response.json"))


def render_index(noun: str, emoji: str, tagline: str, producer: str,
                 rerun: str, stats: List[CohortStats],
                 sections: Optional[List[str]] = None) -> str:
    """The shared README. Every noun's folder opens with the SAME table, so a
    reader who has read one can read all four."""
    live = [s for s in stats if s.rows]
    empty = [s for s in stats if not s.rows]
    kind_keys, conf_keys = [], []
    for s in live:
        for k in s.kinds:
            if k not in kind_keys:
                kind_keys.append(k)
        for k in (s.confidence_order or DEFAULT_CONF_ORDER):
            if k in s.confidence and k not in conf_keys:
                conf_keys.append(k)

    head = (f"{'cohort':<20}{'rows':>9}{'pts':>6} │ "
            + "".join(f"{k[:9]:>10}" for k in kind_keys)
            + " │ " + f"{'solvable':>9}{'written':>9}{'of solv':>9}")
    lines = [head, "─" * len(head)]
    for s in sorted(live, key=lambda x: -x.rows):
        lines.append(
            f"{s.cohort:<20}{s.rows:>9,}{(s.patients or 0):>6} │ "
            + "".join(f"{s.kinds.get(k, 0):>10,}" for k in kind_keys)
            + " │ " + f"{s.resolvable:>9,}{s.written:>9,}"
            + f"{pct(s.written, s.resolvable):>9}")
    tr, tw, ts = (sum(s.rows for s in live), sum(s.written for s in live),
                  sum(s.resolvable for s in live))
    lines += ["─" * len(head),
              f"{'TOTAL':<20}{tr:>9,}{'':>6} │ "
              + "".join(f"{sum(s.kinds.get(k, 0) for s in live):>10,}" for k in kind_keys)
              + " │ " + f"{ts:>9,}{tw:>9,}{pct(tw, ts):>9}"]

    conf = []
    if conf_keys:
        h2 = f"{'cohort':<20}" + "".join(f"{k:>10}" for k in conf_keys)
        trusted = next((s.trusted for s in live if s.trusted), [])
        conf = ["", "", "## Confidence, per cohort", "",
                "Ordered most-trusted first. Rule 3 says only "
                + (" / ".join(trusted) if trusted else "the trusted levels")
                + " may be written into a value",
                "column. That rule is unfalsifiable until this table exists.",
                "", block([h2, "─" * len(h2)] + [
                    f"{s.cohort:<20}" + "".join(f"{s.confidence.get(k, 0):>10,}" for k in conf_keys)
                    for s in sorted(live, key=lambda x: -x.rows)])]

    basis = []
    if any(s.basis for s in live):
        bk = []
        for s in live:
            for k in s.basis:
                if k not in bk:
                    bk.append(k)
        h3 = f"{'cohort':<20}" + "".join(f"{str(k)[:9]:>10}" for k in bk)
        basis = ["", "", "## Scale, per cohort", "",
                 "Rule 4: a quantity without the scale it is on is not interpretable.",
                 "This is how often we actually have one.",
                 "", block([h3, "─" * len(h3)] + [
                     f"{s.cohort:<20}" + "".join(f"{s.basis.get(k, 0):>10,}" for k in bk)
                     for s in sorted(live, key=lambda x: -x.rows)])]

    grade = []
    if any(s.gradeable for s in live):
        rows = []
        for s in sorted(live, key=lambda x: -x.rows):
            for g, n in sorted(s.gradeable.items()):
                rows.append(f"{s.cohort:<20}{g:<28}{n:>9,}")
        grade = ["", "", "## What can be graded, and against what", "",
                 "Gradability is a property of the TARGET columns, never of the input",
                 "string. A cohort whose values ARE this library's own output cannot",
                 "grade it, however well-formed its rows look.",
                 "", block([f"{'cohort':<20}{'gold':<28}{'rows':>9}",
                            "─" * 57] + rows)]

    body = [
        f"# {emoji} _{noun.capitalize()}Info", "",
        tagline, "",
        "GENERATED. Do not hand-edit. The producer is under git at",
        f"`{producer}`.", "", "```bash", rerun, "```", "",
        "Shape is fixed by `haipipe-norm/xinfo/schema.json` and is IDENTICAL for",
        "every describe-* normalizer, so a benchmark that reads coverage,",
        "confidence or basis is written once and runs against all of them.", "",
        "", "## Read this table first", "",
        "`solvable` is the HONEST DENOMINATOR: rows that could have been resolved",
        "at all. Counting a row the log never named as a miss measures the shape",
        "of the log, not the quality of the resolver.", "",
        block(lines),
    ]
    if empty:
        body += ["", f"empty frames (table exists, zero rows): "
                     + " · ".join(s.cohort for s in sorted(empty, key=lambda x: x.cohort))]
    body += conf + basis + grade
    if sections:
        body += ["", ""] + sections
    body += ["", "", "## Layers", "", block(
        [f"  {k:<16} {v}" for k, v in LAYERS.items()])]
    return "\n".join(body) + "\n"


def write(noun: str, emoji: str, tagline: str, producer: str, rerun: str,
          dest, stats: List[CohortStats],
          pages: Optional[Dict[str, str]] = None,
          sections: Optional[List[str]] = None,
          strict: bool = True) -> Dict:
    """Write a whole _XInfo folder. Returns a small report."""
    dest = pathlib.Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    problems = validate(stats)
    if problems:
        msg = "\n".join("  ! " + p for p in problems)
        if strict:
            raise ValueError(f"_stats.json does not conform to xinfo-v1:\n{msg}")
        print(f"  ⚠️ non-conforming, written anyway:\n{msg}")

    (dest / "_stats.json").write_text(
        json.dumps([s.dict() for s in stats], indent=1) + "\n")

    if pages:
        d = dest / "1-per-cohort"
        d.mkdir(exist_ok=True)
        for cohort, text in pages.items():
            (d / f"{cohort}.md").write_text(text)

    (dest / "README.md").write_text(
        render_index(noun, emoji, tagline, producer, rerun, stats, sections))
    return {"cohorts": len(stats), "problems": problems, "dest": str(dest)}
