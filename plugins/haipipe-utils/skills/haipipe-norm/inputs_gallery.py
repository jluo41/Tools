"""
`0-inputs/` — one specimen of every SHAPE that can arrive at a describe-* door.

    from inputs_gallery import Shape, build
    build(noun="exercise", info=INFO, shapes=[...], call=..., keep=[...])

WHAT THIS IS, AND WHAT `5-api-examples` IS
================================================================================
    0-inputs         what can COME IN       one specimen per input shape
    5-api-examples   what the door ANSWERS  one case per behaviour

Two different questions. A folder that tries to be both drifts, so each specimen
carries a `SEE.md` pointing at its behaviour case and the pointer runs one way.

WHY THE ENGINE IS SHARED AND THE SHAPES ARE NOT
================================================================================
Every noun answers the same four questions about an input -- what shape is it,
how much of the board is it, what does the door say, where is the behaviour
documented -- and every noun has a different list of shapes. Food can arrive as
a photograph and exercise cannot; exercise arrives as a vendor code 22% of the
time and food never does. So the four questions live here and the list lives
with the noun, exactly as `xbench` holds the grading and `spec.py` holds the
NounSpec.

NOTHING A GALLERY PRINTS IS HAND-TYPED. Counts are computed from the noun's own
frozen corpus; every `door.json` is the real answer captured at build time.
Build twice and the bytes are identical, so a diff means the resolver moved.
"""
import json
import pathlib
import shutil
from dataclasses import dataclass
from typing import Callable, Optional, Sequence

__all__ = ["Shape", "build", "CONTRACT", "DEPLOYMENT", "ABSENT", "CALL"]

# A shape with no counter is one of two different things, and the page says which.
ABSENT = "absent"   # the API promises it; this board has never written one
CALL = "call"       # a CALL shape (a batch), which has no row count at all


CONTRACT = "contract"      # the API's own input. This is what a paper reports.
DEPLOYMENT = "deployment"  # one site's plumbing, which UNWRAPS to a contract
                           # shape before the door sees it. An internal id is
                           # not a different kind of input, it is a wrapper.


@dataclass
class Shape:
    slug: str                       # 01-plain-text
    title: str                      # what a reader calls it
    why: str                        # why it is its own shape, not a variant
    request: dict                   # the specimen, as it arrives
    count: object                   # callable(corpus) -> int, or ABSENT / CALL
    see: Optional[str] = None       # relative path into 5-api-examples
    sample: Optional[Callable] = None  # callable(corpus) -> (request, provenance)
                                       # Pulls a REAL row off the board. When a
                                       # shape has rows, use this: a gallery whose
                                       # specimens were typed by hand shows what
                                       # someone imagined arriving, not what does.
    layer: str = CONTRACT           # CONTRACT or DEPLOYMENT
    unwraps_to: Optional[str] = None   # DEPLOYMENT only: the contract shape it
                                       # becomes, and what it costs to get there


def _share(shape, n, total):
    if n is not None:
        return f"{n:,} rows ({n / total:.1%})" if total else f"{n:,} rows"
    return {ABSENT: "**no row on this board yet**",
            CALL: "a call shape, not a row shape"}.get(shape.count, "-")


def build(noun: str, info: pathlib.Path, shapes: Sequence[Shape],
          call: Callable[[dict], list], keep: Sequence[str],
          corpus=None, total: int = 0, verdict: Callable = None,
          sources: Callable = None) -> pathlib.Path:
    """Write `<info>/0-inputs/`. Returns the folder."""
    out = pathlib.Path(info) / "0-inputs"
    out.mkdir(parents=True, exist_ok=True)

    # Remove shapes that are no longer declared. Without this the folder only
    # ever grows: describe-insulin's list went from 6 shapes to 8 and left 5
    # orphans behind, one of them still carrying a claim that had been
    # corrected. A gallery that only adds cannot be a drift detector, because
    # a rebuild would no longer reproduce the folder.
    declared = {sh.slug for sh in shapes}     # NOT `keep`: that is the caller's
                                              # field list, and shadowing it made
                                              # every door.json come back keyed by
                                              # slug instead of by column.
    dropped = []
    for d in sorted(out.iterdir()):
        if d.is_dir() and d.name not in declared:
            shutil.rmtree(d)
            dropped.append(d.name)
    if dropped:
        print(f"  dropped {len(dropped)} shape(s) no longer declared: "
              + ", ".join(dropped))
    verdict = verdict or (lambda a: f"`{a.get('conf')}`")
    table = []

    for sh in shapes:
        n = sh.count(corpus) if callable(sh.count) else None
        d = out / sh.slug
        d.mkdir(exist_ok=True)
        if sh.sample is not None:
            request, provenance = sh.sample(corpus)
        else:
            request, provenance = sh.request, (
                "CONSTRUCTED. No row on this board has this shape, so the "
                "specimen is written rather than sampled.")
        answers = call(request)

        (d / "input.json").write_text(json.dumps(request, indent=1, default=str) + "\n")
        (d / "door.json").write_text(json.dumps(
            [{k: a.get(k) for k in keep} for a in answers],
            indent=1, default=str) + "\n")

        verdicts = " · ".join(verdict(a) for a in answers)
        share = _share(sh, n, total)
        (d / "NOTE.md").write_text(
            f"# {sh.title}\n\n"
            f"shape   `{sh.slug}`\n"
            f"layer   {sh.layer}"
            + ("   (the API's own input; a paper reports this)\n"
               if sh.layer == CONTRACT else
               "   (one site's plumbing; it unwraps before the door)\n")
            + f"board   {share}\n"
            f"door    {verdicts}\n"
            + (f"unwraps {sh.unwraps_to}\n" if sh.unwraps_to else "")
            + f"\nSPECIMEN. {provenance}\n"
            + f"\n{sh.why}\n\n"
            f"`input.json` is the shape as it arrives. `door.json` is what "
            f"describe-{noun} answered when this folder was last built; it is "
            f"captured, never transcribed.\n")
        if sh.see:
            (d / "SEE.md").write_text(
                "The behaviour this shape produces is documented at\n\n"
                f"    ../{sh.see}\n")
        table.append((sh.slug, sh.title, share, verdicts, sh.layer, sh.unwraps_to))

    lines = [
        f"# Every shape that can arrive at describe-{noun}",
        "",
        "One specimen per input shape. `0-` because it is where a reader starts:",
        "before the per-cohort tables, before the corpus, before the contract.",
        "",
        "This folder answers WHAT CAN COME IN. `5-api-examples` answers WHAT THE",
        "DOOR ANSWERS. Each specimen's `SEE.md` points at the matching behaviour",
        "case; the pointer runs one way only, so the two cannot drift into each",
        "other.",
        "",
        (f"Row counts are computed from this noun's frozen corpus ({total:,} rows)."
         if total else "This noun's corpus counts distinct strings, not rows."),
        "Every `door.json` is the real answer captured at build time; build twice",
        "and the bytes are identical, so a diff means the resolver moved.",
        "",
        "## The contract — what the API takes, and what a paper reports",
        "",
        "| shape | what it is | share of the board | door today |",
        "|---|---|---|---|",
    ]
    for slug, title, share, verdicts, layer, _ in table:
        if layer == CONTRACT:
            lines.append(f"| `{slug}` | {title} | {share} | {verdicts} |")

    dep = [t for t in table if t[4] == DEPLOYMENT]
    if dep:
        lines += [
            "",
            "## Deployment — one site's plumbing, not a second kind of input",
            "",
            "These are not different inputs. They are the same inputs WRAPPED: an",
            "internal id, a JSON record, a vendor code. Each unwraps to a contract",
            "shape above before the door sees it, so a paper reports the contract",
            "row and an engineer needs the row below it.",
            "",
            "| shape | what it is | share of the board | unwraps to | door today |",
            "|---|---|---|---|---|",
        ]
        for slug, title, share, verdicts, _, unwraps in dep:
            lines.append(f"| `{slug}` | {title} | {share} | {unwraps or '-'} | {verdicts} |")

    # ---- the second table: where the inputs come from ----------------------
    if sources is not None:
        srows, note = sources(corpus)
        lines += [
            "",
            "## Where the inputs come from",
            "",
            "The table above says WHAT can arrive. This one says WHO WROTE IT.",
            "",
            "A *row* is one real logged event. A *writing* is what is left after",
            "identical text is merged, so it is what the resolver has to recognise.",
            "Repeat is rows divided by writings: a source with one writing and",
            "thousands of rows typed the same word every single time, and a source",
            "whose repeat is near 1 wrote something new almost every time.",
            "",
            "| source | rows | writings | repeat | what it writes |",
            "|---|---|---|---|---|",
        ]
        for r in srows:
            lines.append("| `{}` | {} | {} | {} | {} |".format(*r))
        if note:
            lines += ["", note]

    lines += ["", f"GENERATED by `describe-{noun}/build_inputs_gallery.py`. "
                  f"Do not hand-edit: rerun it, and a shape whose answer moved "
                  f"will say so.", ""]
    (out / "README.md").write_text("\n".join(lines))
    return out
