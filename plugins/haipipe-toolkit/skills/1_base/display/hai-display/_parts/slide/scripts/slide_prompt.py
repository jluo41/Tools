"""The full image prompt for one slide picture: the shared shell, one named style, the slide's own content.

    python slide_prompt.py --styles                         every style, with its one-line look
    python slide_prompt.py <style> <content.txt | ->        one prompt, from a content block
    python slide_prompt.py --deck <folder> [--slide NN]     a deck's slides, from <folder>/<name>.slides.json

A deck names its look once, `"style": "<name>"` at the top of its `.slides.json`, and each slide carries its
`content` block (headline, groups of text with what is drawn, layout, focal point; ../content-rules.md). The style is
a file in ../styles/; adding a look is adding a file. The prompt goes to the codex-image2 bridge as it is.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PART = Path(__file__).resolve().parent.parent
STYLES = PART / "styles"
SOURCE = re.compile(r"^<!--.*?-->\s*", re.S)               # a style file's first line names where it came from


def styles() -> dict[str, str]:
    """Every style by name, with its one-line look (the line under its heading)."""
    out = {}
    for f in sorted(STYLES.glob("*.md")):
        lines = [l for l in SOURCE.sub("", f.read_text(encoding="utf-8")).splitlines() if l.strip()]
        out[f.stem] = lines[1] if len(lines) > 1 else ""
    return out


def style_text(name: str) -> str:
    f = STYLES / f"{name}.md"
    if not f.is_file():
        raise SystemExit(f"no style {name!r}; pick one of: {', '.join(styles())}")
    return SOURCE.sub("", f.read_text(encoding="utf-8")).strip()


def base() -> str:
    text = (PART / "base-prompt.md").read_text(encoding="utf-8")
    return text.split("<!-- BASE -->")[1].strip()


def build(style: str, content: str) -> str:
    """The prompt for one slide: the shell, then the style, then what this slide says."""
    if not content.strip():
        raise SystemExit("the slide has no content: write its headline, text groups, layout and focal point")
    return f"{base()}\n\nSTYLE: {style}\n\n{style_text(style)}\n\nSLIDE CONTENT\n\n{content.strip()}\n"


def deck(folder: Path) -> tuple[str, list[dict]]:
    """A deck's style and slides, from <folder>/<folder name>.slides.json."""
    spec = folder / f"{folder.name}.slides.json"
    if not spec.is_file():
        raise SystemExit(f"{folder.name} has no {spec.name}")
    data = json.loads(spec.read_text(encoding="utf-8"))
    style = data.get("style", "")
    style_text(style)                                     # refuses an unknown name, listing the known ones
    return style, data["slides"]


def deck_prompts(folder: Path, slide: str | None = None) -> dict[str, str]:
    """Each slide's id and full prompt; one slide when `slide` is given."""
    style, slides = deck(folder)
    chosen = [s for s in slides if slide in (None, s["id"])]
    if not chosen:
        raise SystemExit(f"no slide {slide!r} in {folder.name}")
    return {s["id"]: build(style, s.get("content", "")) for s in chosen}


def main(argv: list[str]) -> None:
    if argv[:1] == ["--styles"]:
        width = max(map(len, styles()))
        for name, look in styles().items():
            print(f"{name:<{width}}  {look}")
    elif argv[:1] == ["--deck"] and len(argv) in (2, 4):
        slide = argv[3] if len(argv) == 4 and argv[2] == "--slide" else None
        for sid, text in deck_prompts(Path(argv[1]).absolute(), slide).items():
            print(f"===== slide {sid}\n{text}")
    elif len(argv) == 2 and not argv[0].startswith("-"):
        content = sys.stdin.read() if argv[1] == "-" else Path(argv[1]).read_text(encoding="utf-8")
        print(build(argv[0], content))
    else:
        sys.exit(__doc__.split("\n\n")[1])


if __name__ == "__main__":
    main(sys.argv[1:])
