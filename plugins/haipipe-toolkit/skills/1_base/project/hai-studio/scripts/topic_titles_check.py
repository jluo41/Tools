"""Every Studio topic of a blueprint Block (its bands named by the shared studio-bands.json) or of a Block whose face names its Studio bands (`bands: s0N 🧱 Block Structure · ...`) sits in a
named band, and its title starts with that band's name: `s02 · Block Structure: Blueprint` (hai-studio A05).

    python topic_titles_check.py [examples/<Project>/...]

One line per problem with ❗, a count, exit 1 on any. A Block that names no Studio band is not checked.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from new_topic import band_name  # noqa: E402

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())


def problems(block: Path) -> list[str]:
    out = []
    for topic in sorted(block.glob("s[0-9][0-9]-*/")):
        face = topic / f"{topic.name}.md"
        if not face.is_file():
            continue
        nn = int(topic.name[1:3])
        name = band_name(block, 70 if "-studio-type-" in topic.name else nn)   # type topics run on past s79
        rel = topic.relative_to(SPACE)
        if not name:
            out.append(f"❗ {rel}: s{nn // 10}N has no configured band name")
            continue
        first = face.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
        if not re.match(rf"s{nn:02d} · {re.escape(name)}: \S", first):
            out.append(f"❗ {rel}: title {first!r} does not start with {name!r}")
    return out


def main(argv: list[str]) -> int:
    base = (SPACE / (argv[0] if argv else "examples")).resolve()
    blocks = [b for b in sorted([base, *base.glob("**/b[0-9][0-9]_*/")]) if b.name[:1] == "b" if (b / "board.md").is_file()
              and (b.parent.name == "blueprint"     # a blueprint Block: the shared registry names its bands
                   or re.search(r"(?mi)^bands:.*\bs\dN\b", (b / "board.md").read_text(encoding="utf-8", errors="ignore")))]
    found = [p for b in blocks for p in problems(b)]
    print("\n".join(found)) if found else None
    print(f"{'❗' if found else '✅'} topic titles: {len(blocks)} Blocks with Studio bands, {len(found)} problems")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
