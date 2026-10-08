"""What the insight Guide says at one level, as s31 card items, for guide_block · guide_job · guide_task.

Read at build time, so the drawing never drifts from its sources:
- the insight Guide's own files: servers/workbench-insight/guide/guide.yaml, guide/method.md (its six-step
  table and its method-card tables) and related/papers.md (its group column);
- the base's words per level: servers/workbench/guide/levels.yaml;
- each level's six Spaces, their third rows and run buttons, from the level drawings that design them
  (b11 studio s11 Block · s12 Job · s13 Task, their SCREENS lists), until insight_theme.py exists;
- the drawings: b11's studio topics and their notes' **Topic:** lines.
Placeholders only; nothing here reads a Project.
"""
import importlib
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent
TOOLS = HERE.parents[3]
SERVER = TOOLS / "plugins" / "haipipe-toolkit" / "servers" / "workbench-insight"
GUIDE = yaml.safe_load((SERVER / "guide" / "guide.yaml").read_text(encoding="utf-8")) or {}
BASE = yaml.safe_load((SERVER.parent / "workbench" / "guide" / "levels.yaml").read_text(encoding="utf-8"))
METHOD = (SERVER / "guide" / "method.md").read_text(encoding="utf-8")
PAPERS = (SERVER / "related" / "papers.md").read_text(encoding="utf-8")
LEVEL_DRAWING = {"Block": ("s11-block-level", "build_s11_block_level"), "Job": ("s12-job-level", "build_s12_job_level"),
                 "Task": ("s13-task-level", "build_s13_task_level")}


def _table(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if l.strip().startswith("|")]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
    return [dict(zip(rows[0], r)) for r in rows[1:]] if rows else []


def role(level, words):
    """The insight level's role: guide.yaml levels:, else this theme's words, else the base's."""
    return ((GUIDE.get("levels") or {}).get(level) or {}).get("role") or words or BASE[level]["role"]


def steps_today():
    """method.md's six steps today: {N: (step, board, what happens, where, who decides)}."""
    m = re.search(r"(?ms)^\| step \| board \|.*?(?:\n\n|\Z)", METHOD)
    out = {}
    for r in _table(m.group(0).splitlines()) if m else []:
        n = re.match(r"\**(\d+)", r["step"])
        if n:
            out[int(n.group(1))] = (r["step"].strip("*"), r["board"], r["what happens"],
                                    r["where in the workbench"], r["who decides"])
    return out


def step_card(n, level_word):
    """A step card from today's table, its 'where' still in today's Space words (gray in the Guide)."""
    s = steps_today().get(n)
    if not s:
        return (f"? step {n}", "not in method.md", "")
    return (s[0], s[2][:96], f"today on the {s[1]} board · where: {s[3][:60]}   decides: {s[4]}")


def method_cards(names):
    """Method cards by name, from method.md's card tables (family · method · card)."""
    out = []
    for block in METHOD.split("| family |")[1:]:
        for r in _table(("| family |" + block).splitlines()[:40]):
            if r.get("method") in names and r.get("card", "").endswith(".md"):
                where = "Question-asking skill" if "question-asking" in r["card"] else "guide/" + r["card"]
                out.append((r["method"] + " ↗", r["family"] + " · a method card", where))
    return list(dict.fromkeys(out))


def papers(groups, limit=4):
    """Paper cards: papers.md rows whose group names one of these methods (lower case)."""
    out = []
    for r in _table(PAPERS.splitlines()):
        mine = [g.strip() for g in (r.get("group") or "").split(";")]
        if not any(g in groups for g in mine):
            continue
        who, _, title = r.get("paper", "").partition(" · ")
        out.append((title or who, f'{who} · {r.get("venue", "")}', f'role: {r.get("role", "")}   group: {r.get("group", "")}   ↗ doi'))
    return out[:limit], len(out)


def drawings(topics):
    """Drawing cards: b11 studio topics, the first open."""
    out = []
    for k, t in enumerate(topics):
        d = STUDIO / t
        md = next(iter(sorted(d.glob("*.md"))), None)
        m = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", md.read_text(encoding="utf-8"), re.S) if md else None
        shows = re.sub(r"\s+", " ", m.group(1))[:90] if m else ""
        builder = next(iter(sorted(d.glob("build_*.py"))), None)
        line = f"source: b11_theme_insight/studio/{t}/   built by: {builder.name if builder else 'by hand'}   ↗ full size"
        out.append((t, shows, line, k == 0))
    return out


def space_cards(level, words):
    """The six Space cards: this theme's words, then each Space's third row and run buttons as the level
    drawing (s11 · s12 · s13) designs them."""
    folder, name = LEVEL_DRAWING[level]
    sys.path.insert(0, str(STUDIO / folder))
    mod = importlib.import_module(name)
    seen = {}
    for sc in mod.SCREENS:
        space, third, runs = sc[0], sc[1], sc[2]
        subs = []
        if third:
            for row in (third if isinstance(third[0], list) else [third]):
                subs += [lab for lab, _ in row if not lab.endswith(":") and lab.strip() != "|"]   # skip group labels, dividers
        c = seen.setdefault(space, [[], []])
        c[0] += [s for s in subs if s not in c[0]]
        c[1] += [r for r in runs if r not in c[1]]
    out = []
    for space in ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery"):
        subs, runs = seen.get(space, [[], []])
        is_, reads = words.get(space, ("", ""))
        out.append((space, is_, f'sub: {" · ".join(subs) or "—"}   reads: {reads}   runs: {" · ".join(runs) or "—"}'))
    return out
