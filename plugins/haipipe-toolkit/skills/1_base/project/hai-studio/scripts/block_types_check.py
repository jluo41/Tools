"""Every Job and Task of a Block type's example Block names a type its Block Structure topic lists.

A Block Structure topic (s0N of a blueprint Block) pins its Block type's four lists in `types.md`: `## Job group type`,
`## Job type`, `## Task group type`, `## Task type`, each `### <type>` with `for:`, `holds:` and `agreed:` (no until JL
agrees the type for every Block of the kind; it then shows as 〈type〉), and an `example:` line
naming the Block they are checked against (hai-studio A06; b17 s71 Structure › Job-Task).

    python3 block_types_check.py [examples/Project-Ladder/blueprint/b17_theme_work]

One ❗ line per Job or Task whose `job-type:` / `task-type:` is missing from the list, or type with no `for:` or
`holds:`; exit 1 on any.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
LEVELS = ("Job group type", "Job type", "Task group type", "Task type")


def read_types(path: Path) -> tuple[str, dict]:
    """(example Block, {level: {type: {for, holds}}}) from one types.md."""
    example, out, level, cur = "", {}, None, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("example:"):
            example = line.split(":", 1)[1].strip()
        elif line.startswith("## "):
            level, cur = line[3:].strip(), None
            out[level] = {}
        elif line.startswith("### ") and level:
            cur = out[level].setdefault(line[4:].strip(), {})
        elif cur is not None and re.match(r"^(for|holds|agreed):\s*\S", line):
            key, value = line.split(":", 1)
            cur[key] = value.strip()
    return example, out


def field(face: Path, name: str) -> str:
    m = re.search(rf"(?m)^{name}:\s*(\S+)", face.read_text(encoding="utf-8", errors="ignore")) if face.is_file() else None
    return m.group(1) if m else ""


def problems(types_md: Path) -> list[str]:
    example, types = read_types(types_md)
    rel, out = types_md.relative_to(SPACE), []
    out += [f"❗ {rel}: no `## {lv}` list" for lv in LEVELS if not types.get(lv)]
    out += [f"❗ {rel}: {lv} · {t} lacks {k}:" for lv, ts in types.items() for t, d in ts.items()
            for k in ("for", "holds") if not d.get(k)]
    block = SPACE / example
    if not example or not block.is_dir():
        return out + [f"❗ {rel}: example: names no Block"]
    for job in sorted(block.glob("j[0-9]*_*/")):
        kind = field(job / f"{job.name}.md", "job-type")
        if kind and kind not in types.get("Job type", {}):
            out.append(f"❗ {job.relative_to(SPACE)}: job-type {kind!r} is not a Job type of {rel.parent.name}")
        for task in sorted(job.glob("t[0-9]*_*/")):
            kind = field(task / f"{task.name}.md", "task-type")
            if kind and kind not in types.get("Task type", {}):
                out.append(f"❗ {task.relative_to(SPACE)}: task-type {kind!r} is not a Task type of {rel.parent.name}")
    return out


def main(argv: list[str]) -> int:
    base = (SPACE / (argv[0] if argv else "examples")).resolve()
    files = sorted(base.glob("**/s0[0-9]-*/types.md"))
    found = [p for f in files for p in problems(f)]
    print("\n".join(found)) if found else None
    print(f"{'❗' if found else '✅'} block types: {len(files)} Block types pinned, {len(found)} problems")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
