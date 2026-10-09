"""Who names which skill: an index over the toolkit's skills and servers and the other plugins.

A file "calls" a skill when it names it the way skills are named: `name`, /name, "name",
'name', skill: name, skill("name" ..., or as a whole hyphenated word (haipipe-task-for-fit).
History is left out (CHANGELOG.md, _legacy/, dated feedback records, chat transcripts, drawings).
"""
import re
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if p.name == "blueprints").parent
PLUGINS = TOOLS / "plugins"
TK = PLUGINS / "haipipe-toolkit"
SKILLS = TK / "skills"
EXT = {".md", ".py", ".js", ".mjs", ".yaml", ".yml", ".json", ".toml", ".sh"}


def area_of(f: Path) -> str:
    """The caller a file belongs to: '2_theme/<theme>', '1_base/<family>', '0_utils', 'servers', or a plugin."""
    try:
        r = f.relative_to(TK).parts
    except ValueError:
        return f.relative_to(PLUGINS).parts[0]
    if r[0] == "skills" and len(r) > 2:
        return r[1] if r[1] == "0_utils" else f"{r[1]}/{r[2]}"
    return r[0] if r[0] in ("servers", "agents") else "toolkit"


def skip(f: Path) -> bool:
    parts = set(f.parts)
    return (f.suffix not in EXT or f.name == "CHANGELOG.md" or re.match(r"\d{4}-\d{2}-\d{2}_", f.name)
            or bool(parts & {"_legacy", "_old", "node_modules", "__pycache__", "venue", "chat", ".git"})
            or f.is_symlink())


@lru_cache(maxsize=1)
def corpus():
    out = []
    for f in PLUGINS.rglob("*"):
        if f.is_file() and not skip(f):
            try:
                out.append((f, area_of(f), f.read_text(encoding="utf-8", errors="ignore")))
            except OSError:
                pass
    return out


def skills_of(folder: Path) -> list[Path]:
    return sorted(p.parent for p in folder.rglob("SKILL.md")
                  if not any(x.startswith(("_", ".")) or x == "venue" for x in p.relative_to(folder).parts))


def pattern(name: str):
    hy = re.escape(name)
    forms = [rf"`{hy}`", rf"(?<![\w/-])/{hy}(?![\w-])", rf"[\"']{hy}[\"']", rf"skill:\s*{hy}\b", rf"skill_dir\([\"']{hy}"]
    if "-" in name:
        forms.append(rf"(?<![\w/-]){hy}(?![\w-])")
    return re.compile("|".join(forms))


@lru_cache(maxsize=None)
def callers(name: str, home: str) -> dict:
    """{area: files} for files outside the skill's own area `home` that name it."""
    pat, out = pattern(name), {}
    for f, area, text in corpus():
        if area != home and pat.search(text):
            out[area] = out.get(area, 0) + 1
    return out
