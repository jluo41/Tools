"""Build a Block Structure topic's Structure page from its structure.md, drawn by the same tree as its type's Pattern
(b17 s71), so an instance and the type read alike.

    <host venv python> block_structure_page.py examples/Project-Ladder/blueprint/b17_theme_work/s01-work-structure [--check]

`structure.md` holds `## Folder`, `## Job-Task` and `## Studio`; under each, `> ` lines are the tree (two spaces a
level, `name/` a folder, `  # note` a small word after the name, `  | words` the line's hover; a name not fixed in
〈 〉). Writes `<topic>/delivery/structure.html` (one section per part, shown by its #fragment) and sets the Structure
view of `studio-views.json` to it; the Examples view, which the type does not list, is dropped. `--check` writes
nothing and exits 1 when a file is stale.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))     # hai-studio/scripts: the shared scripts
from type_requirements import CSS, SPACE, tree  # noqa: E402

PARTS = {"Folder": "folder-rules", "Job-Task": "jobs-rules", "Studio": "studio-rules"}
PAGE_CSS = ("main{padding:6px 2px}.part{display:none;overflow-x:auto;padding-bottom:6px}.part:target{display:block}"
            "body:not(:has(:target)) #folder-rules{display:block}")


def read(path: Path) -> dict[str, list[str]]:
    """{part: its tree lines} from one structure.md."""
    out, part = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            part = head.group(1)
            out[part] = []
        elif part and re.match(r"^> ?\s*\S", line):
            out[part].append(line[1:].removeprefix(" ").rstrip())
    return out


def build(topic: Path) -> dict[Path, str]:
    """{file: its text}: the Structure page and the views file."""
    from host_paths import bootstrap
    bootstrap()
    parts = read(topic / "structure.md")
    missing = [p for p in PARTS if not parts.get(p)]
    if missing:
        raise ValueError(f"{topic.name}/structure.md has no tree under: {', '.join(missing)}")
    rel = topic.resolve().relative_to(SPACE).as_posix()
    body = "".join(f'<section class="part" id="{PARTS[p]}">{tree(parts[p])}</section>' for p in PARTS)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{html.escape(topic.name)}</title>'
            f'<style>{CSS}{PAGE_CSS}</style></head><body><main>{body}</main></body></html>\n')
    manifest = topic / "studio-views.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    structure = {"name": "Structure", "items": [{"name": p, "path": f"{rel}/delivery/structure.html", "fragment": PARTS[p]}
                                                for p in PARTS]}
    rest = [v for v in data["views"] if v["name"] not in ("Structure", "Examples")]
    data["views"] = [structure] + rest
    return {topic / "delivery" / "structure.html": page, manifest: json.dumps(data, indent=2, ensure_ascii=False) + "\n"}


def main(argv: list[str]) -> int:
    check = "--check" in argv
    topic = (SPACE / next(a for a in argv if not a.startswith("--"))).resolve()
    files = build(topic)
    stale = [f for f, text in files.items() if not f.is_file() or f.read_text(encoding="utf-8") != text]
    if check:
        for f in stale:
            print(f"❗ {f.relative_to(SPACE)}: stale")
        print(f"{'❗' if stale else '✅'} {topic.name}: Structure page")
        return 1 if stale else 0
    for f, text in files.items():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    print(f"Built the Structure page and its view for {topic.name}.")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(SPACE / "plugins/haipipe-toolkit/servers/_host"))
    sys.exit(main(sys.argv[1:]))
