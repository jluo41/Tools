"""Render an sNN's delivery out to where it is used (JL 261030: "studio/sNN/delivery, this is the delivery, and then we
do the render, to render the delivery out, to that area, like the haipipe-studio").

An sNN's `delivery/` holds the agreed version: `deck/` (its slides, which stay there) and the thing it hands over.
`delivery/render.yaml` lists where each piece goes:

    pieces:
      - from: skill/first-principle.md                  # a text piece: written between two markers in its target
        to: plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/SKILL.md
        block: first-principle
      - code: "new_topic.py writes the For: line"        # a code piece: built by a Task, never copied
        by: j01_studio_delivery_type/t02_new_topic_for_line
      - from: paper/s03-results.md                      # a Theme piece: the Theme's skill renders it
        rendered_by: haipipe-paper-assemble

A text piece lands between `<!-- render <address> <block> ... -->` and `<!-- /render <address> <block> -->` in its
target; the region is generated, edited only in the sNN's delivery/. `to:` is relative to the SPACE root (the first
folder above the sNN that holds it).

    python render_delivery.py <sNN folder>            check: each piece same, differs, or not placed
    python render_delivery.py <sNN folder> --apply    write the pieces that differ
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


def address(topic: Path) -> str:
    """b35-s01 (the Block's number, then the sNN's), from where the sNN sits."""
    owner = topic.parent.parent if topic.parent.name == "studio" else topic.parent
    rungs = []
    while re.match(r"^[bjt]\d+_", owner.name):
        rungs.insert(0, owner.name.split("_")[0])
        if rungs[0].startswith("b"):
            break
        owner = owner.parent
    return ".".join(rungs) + "-" + topic.name.split("-")[0]


def markers(addr: str, block: str) -> tuple[str, str]:
    return f"<!-- render {addr} {block}", f"<!-- /render {addr} {block} -->"


def pieces(topic: Path) -> list[dict]:
    card = topic / "delivery" / "render.yaml"
    return (yaml.safe_load(card.read_text(encoding="utf-8")) or {}).get("pieces", []) if card.is_file() else []


def root_for(topic: Path, rel: str) -> Path | None:
    return next((p for p in topic.parents if (p / rel).exists()), None)


def state(topic: Path, piece: dict) -> tuple[str, str]:
    """('same' | 'differs' | 'not placed' | 'no source' | 'code', a few words)."""
    if "code" in piece:
        return "code", f"built by {piece.get('by', 'a Task')}"
    if "rendered_by" in piece:                       # a Theme piece: the Theme's own skill builds it
        return "theme", f"rendered by {piece['rendered_by']}"
    src = topic / "delivery" / piece["from"]
    if not src.is_file():
        return "no source", f"delivery/{piece['from']} is missing"
    root = root_for(topic, piece["to"])
    if root is None:
        return "not placed", f"{piece['to']} not found"
    text = (root / piece["to"]).read_text(encoding="utf-8")
    start, end = markers(address(topic), piece["block"])
    m = re.search(re.escape(start) + r"[^\n]*-->\n(.*?)\n" + re.escape(end), text, re.S)
    if not m:
        return "not placed", f"no {start} ... marker in {piece['to']}"
    return ("same" if m.group(1) == src.read_text(encoding="utf-8").rstrip("\n") else "differs"), piece["to"]


def render(topic: Path, apply: bool = False) -> list[tuple[dict, str, str]]:
    out = []
    for piece in pieces(topic):
        st, words = state(topic, piece)
        if st == "differs" and apply:
            root = root_for(topic, piece["to"])
            target = root / piece["to"]
            text = target.read_text(encoding="utf-8")
            start, end = markers(address(topic), piece["block"])
            body = (topic / "delivery" / piece["from"]).read_text(encoding="utf-8").rstrip("\n")
            text = re.sub(re.escape(start) + r"([^\n]*-->)\n.*?\n" + re.escape(end),
                          lambda m: start + m.group(1) + "\n" + body + "\n" + end, text, count=1, flags=re.S)
            target.write_text(text, encoding="utf-8")
            st = "rendered"
        out.append((piece, st, words))
    return out


def main(argv: list[str]) -> int:
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    topic = Path(argv[0]).resolve()
    rows = render(topic, "--apply" in argv)
    if not rows:
        print(f"{topic.name}: no delivery/render.yaml")
        return 1
    for piece, st, words in rows:
        print(f"{st:10} {piece.get('block') or piece.get('code') or piece.get('from')}  ({words})")
    return 0 if all(st in ("same", "rendered", "code", "theme") for _, st, _ in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
