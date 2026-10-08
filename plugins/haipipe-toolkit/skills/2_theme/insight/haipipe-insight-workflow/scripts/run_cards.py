"""run_cards.py · read and check the insight run cards (ref/run-cards.md; b11 s21 phase 2).

    python run_cards.py --check        every card whole, its skill and agent real, its pattern naming its own Run
    python run_cards.py --list         one line per card: level › space · label · run · skill

`cards()` is the one reader: the workbench, the table writer (workbench-insight/scripts/cards_table.py) and the
check read the cards through it. A card is `🔘 BUTTON label · <Level> › <Space> · ^pattern · views <names>` followed
by its 🧩 SKILL, 🤖 AGENT, ✍️ SIGNS and 💬 PROMPT lines. Exit 1 on any problem.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARDS = HERE.parent / "ref" / "run-cards.md"
SKILLS = HERE.parents[3]                                  # plugins/haipipe-toolkit/skills
AGENTS = SKILLS.parent / "agents"
LEVELS = ("Guide", "Block", "Job", "Task", "Prototype", "Release", "Question")
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
GUIDE = ("Method", "Related Paper")
BUTTON = re.compile(r"^🔘 BUTTON\s+(.+?) · (" + "|".join(LEVELS) + r") › (.+?) · (\^\S+)(?: · views (.+))?$")
MARKS = (("🧩 SKILL", "skill"), ("🤖 AGENT", "agent"), ("✍️ SIGNS", "signs"), ("💬 PROMPT", "prompt"))
LEVEL_SKILLS = ("haipipe-insight-data", "haipipe-insight-information", "haipipe-insight-knowledge")


def cards(path: Path = CARDS) -> list[dict]:
    """[{label, level, space, pattern, views, skill, agent, signs, prompt}], in file order."""
    out, card = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = BUTTON.match(line)
        if m:
            card = {"label": m.group(1), "level": m.group(2), "space": m.group(3), "pattern": m.group(4),
                    "views": (m.group(5) or "").split(), "skill": "", "agent": "", "signs": "", "prompt": ""}
            out.append(card)
        elif line.startswith("🔘 BUTTON") or line.startswith("## "):
            card = None
        elif card is not None:
            for mark, key in MARKS:
                if line.startswith(mark):
                    card[key] = line[len(mark):].strip()
    return out


def run_name(card: dict) -> str:
    """The Run a card's prompt names: `as run-…`, or a hard Run's `rNN_<partition>`."""
    m = re.search(r"\bas (run-[^\s;,.:]+(?:\.[^\s;,:]+)*)", card["prompt"])
    if m:
        return m.group(1).rstrip(".")
    return "rNN_<partition>" if card["pattern"].startswith(r"^r\d") else ""


def card_for(run: str, level: str | None = None) -> dict | None:
    """The card of a Run folder name (or a placeholder name like run-add-j<NN>), its own level's first."""
    sample = re.sub(r"<[^>]+>", "x01", run).replace("<", "").replace(">", "")
    found = [c for c in cards() if re.match(c["pattern"], sample) or re.match(c["pattern"], run)]
    return next((c for c in found if c["level"] == level), found[0] if found else None)


def _agent_exists(name: str) -> bool:
    """An agent is agents/<name>.md in the toolkit, or in a skill family's own agents/ folder."""
    return (AGENTS / f"{name}.md").is_file() or any(SKILLS.rglob(f"agents/{name}.md"))


def _skill_exists(name: str) -> bool:
    return any(p.parent.name == name for p in SKILLS.rglob("SKILL.md"))


def check(path: Path = CARDS) -> list[str]:
    problems, seen = [], set()
    all_cards = cards(path)
    if not all_cards:
        return [f"{path.name}: no cards"]
    for c in all_cards:
        where = f"{c['label']} · {c['level']} › {c['space']}"
        for _, key in MARKS:
            if not c[key]:
                problems.append(f"{where}: no {key}")
        if c["space"] not in (GUIDE if c["level"] == "Guide" else SPACES):
            problems.append(f"{where}: {c['space']!r} is not a Space of the {c['level']}")
        if (c["level"], c["space"], c["label"]) in seen:
            problems.append(f"{where}: two cards for one button")
        seen.add((c["level"], c["space"], c["label"]))
        try:
            pat = re.compile(c["pattern"])
        except re.error as e:
            problems.append(f"{where}: pattern {c['pattern']}: {e}")
            continue
        name = run_name(c)
        sample = name.replace("rNN_", "r01_").replace("j<prev>", "j01").replace("<l><nn>", "d01")
        sample = re.sub(r"<[^>]+>", lambda m: "01" if m.group(0) in ("<N>", "<M>", "<NN>") else "x01", sample)
        if not name:
            problems.append(f"{where}: its prompt names no Run (as run-<type>-<target>)")
        elif not pat.match(sample):
            problems.append(f"{where}: pattern {c['pattern']} does not match its own Run {name}")
        skills = LEVEL_SKILLS if c["skill"] == "haipipe-insight-<its level>" else (c["skill"],)
        for s in skills:
            if not _skill_exists(s):
                problems.append(f"{where}: no skill {s}")
        if not _agent_exists(c["agent"]):
            problems.append(f"{where}: no agent {c['agent']}")
        if "{folder}" not in c["prompt"] and c["level"] not in ("Guide",):
            problems.append(f"{where}: its prompt never names {{folder}}")
    return problems


LADDER_LEVEL = {"prototype": "Prototype", "version": "Release", "question": "Question", "board": "Block", "job": "Job",
                "task": "Task"}


def against_scaffold(path: Path = CARDS) -> list[str]:
    """Every run type the scaffold knows (haipipe-insight/scripts/insight_ladder.py TYPES) has a card at its level
    naming the same skill; the scaffold and the cards never drift apart."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("insight_ladder", SKILLS / "2_theme" / "insight" / "haipipe-insight" /
                                                  "scripts" / "insight_ladder.py")
    il = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(il)
    problems, all_cards = [], cards(path)
    for (lv, rtype), (skill, _agent, _signs, hard) in il.TYPES.items():
        level = LADDER_LEVEL[lv]
        sample = "r01_x" if hard else ("run-" + rtype if (lv, rtype) in il.ALONE else
                                       f"run-{rtype}-{il.DEFAULT_TARGET.get((lv, rtype), 'x01')}")
        targets = ("x01", "j01", "t01", "q01", "d01", "p1", "v1", "coverage")
        names = [sample] + ([] if hard else [f"run-{rtype}-{t}" for t in targets])
        mine = [c for c in all_cards if c["level"] == level and any(re.match(c["pattern"], n) for n in names)]
        if not mine:
            problems.append(f"scaffold run type {rtype} ({level}) has no card")
        elif not any(c["skill"] == skill or ("<its level>" in skill and c["skill"] in LEVEL_SKILLS + (
                "haipipe-insight-wisdom",)) for c in mine):
            problems.append(f"scaffold run type {rtype} ({level}) names {skill}; its card names {mine[0]['skill']}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for c in cards():
            print(f"{c['level']} › {c['space']} · {c['label']} · {run_name(c)} · {c['skill']}")
    if a.check or not a.list:
        problems = check() + against_scaffold()
        for p in problems:
            print("problem:", p)
        print(f"{len(cards())} cards, {len(problems)} problems")
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
