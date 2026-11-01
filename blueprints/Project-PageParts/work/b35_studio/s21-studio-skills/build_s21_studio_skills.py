"""b35-s21:studio @ studio_skills, its drawing: haipipe-studio's five parts, its Design the map of b35's skills (JL 261031:
"could you have one group to list all the skills? the skills covered by this b35_studio"). The face's `Skills` list says
which skills and which sNN feed each; each skill's version, its purpose and its scripts are read from its own SKILL.md
and scripts/ on every build, never typed here.

    .venv/bin/python build_s21_studio_skills.py
"""
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
SKILLS = TOOLS / "plugins/haipipe-toolkit/skills"
sys.path.insert(0, str(SKILLS / "1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
import five_parts  # noqa: E402


def skill_facts(name: str) -> dict:
    """A skill's version, its first sentence and its scripts, from disk."""
    home = next(SKILLS.glob(f"*/*/{name}"))
    text = (home / "SKILL.md").read_text(encoding="utf-8")
    version = (re.search(r'version:\s*"([^"]+)"', text) or [None, "?"])[1]
    desc = re.search(r"(?ms)^description:\s*(.+?)\n[a-z_-]+:", text)
    first = re.split(r"(?<=[.:])\s", " ".join((desc.group(1) if desc else "").split()), maxsplit=1)[0].rstrip(".:")
    scripts = sorted(p.name for p in (home / "scripts").glob("*.py")) if (home / "scripts").is_dir() else []
    return {"home": home.relative_to(SKILLS).as_posix(), "version": version, "first": first, "scripts": scripts}


def build(topic: Path = HERE) -> Path:
    face = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    m = re.search(r"(?ms)^Skills\n-+\n(.*?)\n\n\n", face)
    rows = [re.match(r"\d+\.\s+(\S+) · fed by ([^·]+) · (.+)$", ln).groups()
            for ln in m.group(1).splitlines() if re.match(r"\d+\.", ln)]
    asks = re.findall(r"(?m)^\d+\.\s+(.+\?)$", face.split("\nOpen\n", 1)[-1])
    spec = {"title": "The skills b35 covers",
            "why": {"question": "where is each Studio rule written?",
                    "notes": ["one list of b35's skills", "and the sNN that change each"],
                    "quote": "JL 261031: \"one group to list all the skills\""},
            "what": {"head": "② what s21 hands over: the skill map", "icon": "page", "name": "delivery/skill/",
                     "type": "skill", "deck_why": "stays in s21's delivery/deck/, so anyone gets it in a minute",
                     "parts": [("page", "skill/map", "each skill, its version, its scripts, its sNN", False)]},
            "job": None, "target": "the four skills' SKILL.md", "missing": []}

    def design():
        els = text("mapT", 690, 280, "A · the skills, read from disk on every build", 18, TITLE)
        y = 330
        for i, (name, fed, owns) in enumerate(rows):
            f = skill_facts(name)
            els += text(f"sk{i}", 690, y, f"{name}  {f['version']}", 22, NAVY)
            els += text(f"sk{i}h", 1080, y + 4, f"{f['home']}/", 14, BODY)
            els += text(f"sk{i}o", 690, y + 34, "\n".join(textwrap.wrap(owns, 80)), 16, INK)
            els += text(f"sk{i}f", 690, y + 60, f"fed by {fed.strip()}", 16, OR)
            words = "scripts: " + (", ".join(f["scripts"]) if f["scripts"] else "none (its rules are its SKILL.md)")
            wrapped = "\n".join(textwrap.wrap(words, 90))
            els += text(f"sk{i}s", 690, y + 86, wrapped, 14, BODY)
            y += 130 + 18 * wrapped.count("\n")
        if asks:
            els += sticky("askD", 1000, y + 60, 420, 90, "\n".join(textwrap.wrap(asks[0], 46)), 15, -0.02, RED, RE)
        return els

    return five_parts.build(topic, spec, design)


if __name__ == "__main__":
    build()
