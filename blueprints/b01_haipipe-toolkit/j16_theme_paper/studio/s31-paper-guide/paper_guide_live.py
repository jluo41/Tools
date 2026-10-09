"""What the live paper Guide says at one level, as s31 card items, for guide_block · guide_job · guide_task.

Read at build time from the paper workbench's own files, so the drawing shows what the Guide renders:
servers/workbench-paper/guide/guide.yaml (levels:, roadmap:), guide/method.md (its **Block · …** · **Job · …** ·
**Task · …** step tables and its method-card tables), related/papers.md (its level column); and the
six Spaces' third rows and run types from the live frame (servers/workbench/frame.py with the paper theme),
over a placeholder paper Board in a temp folder, never a real paper.
"""
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[4]
SERVER = TOOLS / "plugins" / "haipipe-toolkit" / "servers" / "workbench-paper"
sys.path.insert(0, str(SERVER.parent / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
import yaml  # noqa: E402
from live import frame  # noqa: E402

GUIDE = yaml.safe_load((SERVER / "guide" / "guide.yaml").read_text(encoding="utf-8"))
BASE = yaml.safe_load((SERVER.parent / "workbench" / "guide" / "levels.yaml").read_text(encoding="utf-8"))
METHOD = (SERVER / "guide" / "method.md").read_text(encoding="utf-8")
PAPERS = (SERVER / "related" / "papers.md").read_text(encoding="utf-8")


def _table(lines):
    """The rows of a Markdown table as dicts by its head; the separator row skipped."""
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if l.startswith("|")]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
    return [dict(zip(rows[0], r)) for r in rows[1:]] if rows else []


def role(level):
    return ((GUIDE.get("levels") or {}).get(level) or {}).get("role") or BASE[level]["role"]


def steps(level):
    """Step cards: the rows of method.md's table under **<level> · …**."""
    m = re.search(rf"(?ms)^\*\*{level}\b[^\n]*\*\*\n+(\|.*?)(?:\n\n|\Z)", METHOD)
    rows = _table(m.group(1).splitlines()) if m else []
    return [(r["step"], r["what happens"], f'where: {r["where in the workbench"]}   methods: {r["methods"]}   '
                                           f'signs: {r["who signs"]}') for r in rows]


def papers(level):
    """Paper cards: the papers.md rows whose level names this level."""
    out = []
    for r in _table(PAPERS.splitlines()):
        if level not in [x.strip() for x in (r.get("level") or "").split(";")]:
            continue
        who, _, title = r["paper"].partition(" · ")
        out.append((title or who, f'{who} · {r["venue"]}', f'role: {r["role"]}   group: {r["group"]}   ↗ doi'))
    return out


def method_cards(level):
    """Method cards: a card serves the level its papers are filed under (papers.md level · group)."""
    by_group = {}
    for r in _table(PAPERS.splitlines()):
        by_group.setdefault(r["group"], set()).update(x.strip() for x in (r.get("level") or "").split(";"))
    out = []
    for block in METHOD.split("| family |")[1:]:
        for r in _table(("| family |" + block).splitlines()[:40]):
            if not r.get("card", "").endswith(".md"):
                continue
            if level in by_group.get(r["method"].lower(), set()):
                out.append((r["method"] + " ↗", r["family"].split(":")[0] + " methods · a method card",
                            "guide/" + r["card"]))
    return list(dict.fromkeys(out))


def drawings(level):
    """Drawing cards from guide.yaml roadmap:, the first open."""
    out = []
    for k, d in enumerate((GUIDE.get("roadmap") or {}).get(level) or []):
        board = TOOLS.parent / d["board"]
        here = board.parent
        builder = next(iter(sorted(here.glob("build_*.py")) + sorted(here.glob(board.stem + ".py"))), None)
        line = (f'source: {d["board"].replace("Tools/blueprints/", "")}   built by: '
                f'{builder.name if builder else "by hand"}   ↗ full size'
                + ("" if board.is_file() else "   ? not on disk"))
        out.append((d["title"], d["shows"], line, k == 0))
    return out


def _board(tmp):
    """A placeholder paper Board in a temp folder, so the frame reads the paper theme's Spaces."""
    b = Path(tmp) / "examples-demo" / "Project-Demo" / "papers" / "Paper-Demo"
    (b / "A1-Story").mkdir(parents=True)
    (b / "board.md").write_text("# Paper-Demo\n\n## Pages\n\n### A1 · A1-Story\n", encoding="utf-8")
    (b.parents[1] / "project.yaml").write_text("name: Demo\n", encoding="utf-8")
    return b


def space_cards(level):
    """The six Space cards: the paper's words (guide.yaml levels:, else the base's), and each Space's third
    row and run types as the live frame gives them for the paper theme at this level."""
    theme = frame.themes()["paper"]
    words = {**BASE[level]["spaces"], **(((GUIDE.get("levels") or {}).get(level) or {}).get("spaces") or {})}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        at = _board(tmp) if level == "Block" else None
        live = frame.space_cards(theme, level, at, root)
    out = []
    for space, subs, runs in live:
        w = words.get(space) or {}
        out.append((space, w.get("is", ""), f'sub: {" · ".join(subs) or "—"}   reads: {w.get("reads", "—")}   '
                                            f'runs: {" · ".join(runs) or "—"}'))
    return out
