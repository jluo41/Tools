"""Deliver every Studio Type a blueprint Block designs into hai-studio, where a topic in any SPACE finds it by name
(hai-studio A12; ref/studio-type.md).

    python types_deliver.py            write what differs
    python types_deliver.py --check    write nothing; exit 1 when a kept type is not what its blueprint says

A type topic `sNN-studio-type-<name>/` with an `elements.md` is delivered to `../gallery/<name>/elements.md`, the file
copied whole. Its `delivery/render.yaml` says so (a file piece, render_delivery.py); this script writes that card
for a type that has none, then renders every one. Never edit a kept type: change the blueprint topic, then deliver.
Two blueprints may not deliver the same name; a kept type no blueprint delivers is reported.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_delivery  # noqa: E402

HERE = Path(__file__).resolve().parent
SPACE = next(p for p in HERE.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
KEPT = HERE.parent / "gallery"
CARD = "# Where this Studio Type is delivered (hai-studio scripts/types_deliver.py): a topic in any SPACE finds it by name.\npieces:\n  - file: elements.md\n    to: {to}\n"


def designed(space: Path = SPACE) -> dict[str, list[Path]]:
    """{type name: its blueprint type topics}, for every type topic that has an elements.md."""
    out: dict[str, list[Path]] = {}
    for pattern in ("*/blueprint/*/", "*/*/blueprint/*/"):
        for topic in sorted(space.glob(pattern + "s[0-9][0-9]-studio-type-*")):
            if (topic / "elements.md").is_file():
                out.setdefault(re.sub(r"^s\d\d-studio-type-", "", topic.name), []).append(topic)
    return out


def main(argv: list[str], space: Path = SPACE, kept: Path = KEPT) -> int:
    check, bad = "--check" in argv, 0
    found = designed(space)
    for name, topics in found.items():
        if len(topics) > 1:
            print(f"❗ {name}: delivered by " + " and ".join(t.parent.name + "/" + t.name for t in topics))
            bad += 1
            continue
        topic, to = topics[0], (kept / name / "elements.md").resolve().relative_to(space.resolve()).as_posix()
        card = topic / "delivery" / "render.yaml"
        want = CARD.format(to=to)
        if not card.is_file() or to not in card.read_text(encoding="utf-8"):
            if check:
                print(f"❗ {name}: {topic.name} has no delivery/render.yaml that delivers it")
                bad += 1
                continue
            card.parent.mkdir(parents=True, exist_ok=True)
            card.write_text(want if not card.is_file() else card.read_text(encoding="utf-8").rstrip("\n") + "\n"
                            + want.split("pieces:\n", 1)[1], encoding="utf-8")
        if not check:
            kept.mkdir(parents=True, exist_ok=True)             # render_delivery finds the SPACE by the target's first folder
        states = [st for piece, st, _ in render_delivery.render(topic, not check) if piece.get("to") == to]
        ok = states and states[0] in ("same", "rendered")
        print(f"{'✅' if ok else '❗'} {name}: {topic.parent.name}/{topic.name}" + ("" if ok else ": the kept copy differs (run types_deliver.py)"))
        bad += not ok
    for folder in sorted(p for p in kept.glob("*") if (p / "elements.md").is_file() and p.name not in found):
        print(f"❗ {folder.name}: kept in hai-studio/gallery, delivered by no blueprint type topic")
        bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
