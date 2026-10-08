"""The slide draft's kit (excalidraw-slide, 261007): its colours, and a check of `slides.py`.

A slide draft (a studio topic s61-s69) proposes a deck before it is built: one `slides.py` is the ONE
source that its drawing and its deck both read. This kit holds what every slide draft shares:

    ACCENT · ACCENT_FILL · MUTED   the one colour exception, inside a slide only
    off_palette(els)               what a slide draft drew outside black · red · green and the accent
    load(path) · check(path)       read a slides.py; list what breaks its field contract

    python slide_kit.py check <studio/s6N-<deck>/slides.py>

The field contract is ref/slide-draft.md § slides.py. The check is mechanical (the fields are there and
agree); whether the argument holds is the person's read of the drawing.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

# the studio look around the slides (haipipe-studio): black, red = an open question, green = a change
INK, RED, GREEN = "#1e1e1e", "#e03131", "#2f9e44"
# inside a slide only: one accent marks the slide's key thing, a muted gray its caption (JL 261007: "make
# the slide to be a bit colorful by highlight the important things")
ACCENT, ACCENT_FILL, MUTED = "#1971c2", "#d0ebff", "#868e96"

SLIDE_KEYS = ("n", "slug", "group", "title", "headline", "visual", "caption", "source", "next", "notes")
MODULE_KEYS = ("SLIDES", "GROUPS", "OPEN")
MODULE_FACE = ("AUDIENCE", "LENGTH", "SHOWN")       # who it is for, how long, when it is shown
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def off_palette(els):
    """The elements a slide draft drew outside black · red · green and, inside a slide, the accent, its
    light fill and the muted caption gray. Images keep their own picture."""
    strokes = (INK, RED, GREEN, ACCENT, MUTED, "transparent", "")
    fills = ("transparent", "#ffffff", "", ACCENT_FILL)
    return [e for e in els if e.get("type") != "image"
            and (str(e.get("strokeColor", INK)).lower() not in strokes
                 or str(e.get("backgroundColor", "transparent")).lower() not in fills)]


def load(path: Path):
    """The slides.py module, imported from its file."""
    spec = importlib.util.spec_from_file_location("slides", Path(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(path: Path) -> list[tuple[str, str]]:
    """[(level, finding)]: what in a slides.py breaks the field contract; [] when it holds."""
    try:
        mod = load(path)
    except Exception as err:                          # a slides.py that does not import
        return [("error", f"{Path(path).name} does not import: {type(err).__name__}: {err}")]
    out = [("error", f"no {k}") for k in MODULE_KEYS if not hasattr(mod, k)]
    out += [("warn", f"no {k} (the face says who, how long, when)") for k in MODULE_FACE if not hasattr(mod, k)]
    if any(l == "error" for l, _ in out):
        return out
    groups = [g[0] if isinstance(g, (tuple, list)) else g for g in mod.GROUPS]
    slugs = []
    for i, s in enumerate(mod.SLIDES, 1):
        where = f"slide {i}"
        if not isinstance(s, dict):
            out.append(("error", f"{where}: not a dict"))
            continue
        out += [("error", f"{where}: no {k}") for k in SLIDE_KEYS if k not in s]
        if s.get("n") != f"{i:02d}":
            out.append(("error", f"{where}: n is {s.get('n')!r}, expected '{i:02d}' (slides in order)"))
        slug = str(s.get("slug", ""))
        if not SLUG.match(slug):
            out.append(("error", f"{where}: slug {slug!r}: lower-case kebab"))
        slugs.append(slug)
        if s.get("group") not in groups:
            out.append(("error", f"{where}: group {s.get('group')!r} is not in GROUPS"))
        visual = s.get("visual")
        if not isinstance(visual, dict) or not visual.get("kind"):
            out.append(("error", f"{where}: visual needs a kind (ONE visual per slide)"))
        ask = s.get("ask", [])
        if not isinstance(ask, (list, tuple)) or not all(isinstance(q, str) and q.strip() for q in ask):
            out.append(("error", f"{where}: ask is a list of questions (strings), drawn in red under the slide"))
        if i < len(mod.SLIDES) and not str(s.get("next") or "").strip():
            out.append(("warn", f"{where}: next is empty (why the next slide follows)"))
    out += [("error", f"slug {s!r} is used twice") for s in sorted({s for s in slugs if slugs.count(s) > 1})]
    out += [("warn", f"group {g!r} has no slide") for g in groups if g not in {s.get('group') for s in mod.SLIDES
                                                                              if isinstance(s, dict)}]
    return out


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "check":
        print(__doc__.split("\n\n")[-2].strip())
        return 2
    found = check(Path(sys.argv[2]))
    for level, text in found:
        print(f"{level:<6} {text}")
    if not found:
        print(f"{sys.argv[2]}: the field contract holds")
    return 1 if any(l == "error" for l, _ in found) else 0


if __name__ == "__main__":
    sys.exit(main())
