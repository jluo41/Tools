"""Render and check a Workbench Table (skills/0_utils/table-workbench/SKILL.md).

    python render_workbench_table.py <workbench-table.md> [--format md|blocks] [--check [--cards <run-cards.md>]]

The table is the one Markdown table in the file whose header is exactly
Level | Space | View | Run type | Agent | Skill | Person signs.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

COLUMNS = ["Level", "Space", "View", "Run type", "Agent", "Skill", "Person signs"]
JUDGE = re.compile(r"\b(verify|review|check|judge)\b", re.I)
NEW = re.compile(r"\s*\(new\)\s*$")


def plugins_root(start: Path) -> Path:
    """The Tools/plugins folder above this script."""
    for parent in start.resolve().parents:
        if parent.name == "plugins":
            return parent
    raise SystemExit("cannot find Tools/plugins above " + str(start))


def read_table(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells == COLUMNS:
            rows = []
            for row in lines[i + 2:]:
                if not row.strip().startswith("|"):
                    break
                values = [c.strip() for c in row.strip().strip("|").split("|")]
                rows.append(dict(zip(COLUMNS, values + [""] * (len(COLUMNS) - len(values)))))
            return rows
    raise SystemExit(f"{path}: no table with the header {' | '.join(COLUMNS)}")


def known_names(plugins: Path) -> tuple[set[str], set[str]]:
    skills, agents = set(), set()
    for skill in plugins.glob("**/SKILL.md"):
        match = re.search(r"(?m)^name:\s*(\S+)", skill.read_text(encoding="utf-8", errors="replace")[:600])
        skills.add(match.group(1) if match else skill.parent.name)
        skills.add(skill.parent.name)
    for agent in plugins.glob("**/agents/*.md"):
        agents.add(agent.stem)
    return skills, agents


def check(rows: list[dict], plugins: Path) -> tuple[list[str], list[str]]:
    skills, agents = known_names(plugins)
    problems, planned = [], []
    makers = {(r["Level"], NEW.sub("", r["Agent"])) for r in rows
              if r["Agent"] != "none" and not JUDGE.search(r["Run type"])}
    for n, r in enumerate(rows, 1):
        where = f'row {n} ({r["Level"]} · {r["Space"]} · {r["View"]} · {r["Run type"]})'
        for col in COLUMNS:
            if not r[col]:
                problems.append(f"{where}: empty {col}")
        agent, skill = NEW.sub("", r["Agent"]), NEW.sub("", r["Skill"])
        if r["Run type"] != "none" and agent == "none":
            problems.append(f"{where}: a run with no agent")
        if agent != "none" and not agent.endswith("-agent"):
            problems.append(f"{where}: Agent {agent!r} is not an agent; a person signs, never runs")
        if skill.endswith("-workflow"):
            problems.append(f"{where}: {skill} routes and gates; name the small skill that does the work")
        if JUDGE.search(r["Run type"]) and (r["Level"], agent) in makers:
            problems.append(f"{where}: {agent} also makes on this level; a judging run needs another agent")
        for name, kind, pool, raw in ((agent, "agent", agents, r["Agent"]), (skill, "skill", skills, r["Skill"])):
            if name == "none":
                continue
            if NEW.search(raw):
                planned.append(f"{kind} {name}")
            elif name not in pool:
                problems.append(f"{where}: {kind} {name} not found under Tools/plugins and not marked (new)")
    return problems, sorted(set(planned))


def read_cards(path: Path) -> list[dict]:
    """A run-cards file -> [{Run type, Agent, Skill, Person signs}], one per 🔘 BUTTON."""
    cards, card = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^🔘 BUTTON\s+(.+?)\s+·", line)
        if m:
            card = {"Run type": m.group(1), "Agent": "", "Skill": "", "Person signs": ""}
            cards.append(card)
            continue
        for mark, col in (("🤖 AGENT", "Agent"), ("🧩 SKILL", "Skill"), ("✍️ SIGNS", "Person signs")):
            if card is not None and line.startswith(mark):
                card[col] = line[len(mark):].strip()
    return cards


def check_cards(rows: list[dict], cards: list[dict]) -> list[str]:
    """Each run type of the table is one card with the same agent, skill and signs, and back."""
    cols = ("Agent", "Skill", "Person signs")
    want = {r["Run type"]: r for r in rows if r["Run type"] != "none"}
    have = {c["Run type"]: c for c in cards}
    out = [f"run type {k!r} is in the table but has no card" for k in want if k not in have]
    out += [f"card {k!r} is not in the table" for k in have if k not in want]
    for k in want.keys() & have.keys():
        out += [f"run type {k!r}: {c} is {want[k][c]!r} in the table, {have[k][c]!r} on the card"
                for c in cols if want[k][c] != have[k][c]]
    return out


def render_md(rows: list[dict]) -> str:
    out = ["| " + " | ".join(COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
    out += ["| " + " | ".join(r[c] for c in COLUMNS) + " |" for r in rows]
    return "\n".join(out)


def render_blocks(rows: list[dict]) -> str:
    out, last = [], None
    for r in rows:
        head = f'{r["Level"]} · {r["Space"]}'
        if head != last:
            out += ["", head, "-" * len(head)]
            last = head
        sign = "" if r["Person signs"] == "none" else f'   signs: {r["Person signs"]}'
        out.append(f'  {r["View"]} › {r["Run type"]}{sign}')
        out.append(f'      agent {r["Agent"]}   skill {r["Skill"]}')
    return "\n".join(out).lstrip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("table", type=Path)
    ap.add_argument("--format", choices=("md", "blocks"), default="md")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--cards", type=Path, help="a run-cards file that must agree with the table")
    args = ap.parse_args(argv)
    rows = read_table(args.table)
    print(render_md(rows) if args.format == "md" else render_blocks(rows))
    if not args.check:
        return 0
    problems, planned = check(rows, plugins_root(Path(__file__)))
    if args.cards:
        problems += check_cards(rows, read_cards(args.cards))
    print()
    print("check: PASS" if not problems else f"check: {len(problems)} finding(s)")
    for p in problems:
        print("  " + p)
    if planned:
        print("planned (new): " + ", ".join(planned))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
