"""A name that is not fixed is written in 〈 〉 (AGENTS.md "Page words"; hai-studio A07).

Scans every Studio Type topic's elements.md and studio-views.json (examples/**/sNN-studio-type-*/): a tab or view whose
name is a numbered slot ("Job type 1", "Example 2", "quick page 1") must read 〈Job type 1〉.

    python3 placeholder_check.py [examples]

One ❗ line per bare slot name, exit 1 on any.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
SLOT = re.compile(r"^[A-Za-z][A-Za-z /-]* \d+$")        # words, then a bare number: a slot, not a real name


def names(topic: Path) -> list[tuple[Path, str]]:
    out = []
    md = topic / "elements.md"
    if md.is_file():
        out += [(md, m.group(1)) for m in re.finditer(r"(?m)^#{2,3}\s+(.+?)\s*$", md.read_text(encoding="utf-8"))]
    views = topic / "studio-views.json"
    if views.is_file():
        try:
            data = json.loads(views.read_text(encoding="utf-8")).get("views", [])
        except ValueError:
            data = []
        out += [(views, v.get("name", "")) for v in data] + [(views, i.get("name", "")) for v in data for i in v.get("items", [])]
    return out


def main(argv: list[str]) -> int:
    base = (SPACE / (argv[0] if argv else "examples")).resolve()
    topics = sorted(base.glob("**/s[0-9][0-9]-studio-type-*/"))
    found = sorted({f"❗ {f.relative_to(SPACE)}: {name!r} is a slot, write 〈{name}〉"
                    for t in topics for f, name in names(t) if SLOT.match(name)})
    print("\n".join(found)) if found else None
    print(f"{'❗' if found else '✅'} placeholders: {len(topics)} Studio Type topics, {len(found)} bare slot names")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
