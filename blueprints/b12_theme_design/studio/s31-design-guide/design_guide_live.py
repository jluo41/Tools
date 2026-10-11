"""What the live design Guide says at one level, as s31 card items, for guide_block · guide_job · guide_task.

Read at build time from the design workbench's own files, so the drawing shows what the Guide renders today:
servers/workbench-design/guide/guide.yaml (description, skills), guide/method.md (the six steps, the
thirteen method cards, the five tests), related/papers.md (its group column: a method, `all methods` or
`tests`); and the six Spaces' third rows and run types from the live frame (servers/workbench/frame.py with
the design theme), over a placeholder design ladder made by the design scaffold in a temp folder.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = Path(__file__).resolve().parents[4]
SERVER = TOOLS / "plugins" / "haipipe-toolkit" / "servers" / "workbench-design"
SCAFFOLD = TOOLS / "plugins" / "haipipe-toolkit" / "skills" / "2_theme" / "design" / "haipipe-design" / "scripts" / "design_ladder.py"
STUDIO = HERE.parent
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'plugins/haipipe-toolkit/servers' / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
import yaml  # noqa: E402
from live import frame  # noqa: E402

GUIDE = yaml.safe_load((SERVER / "guide" / "guide.yaml").read_text(encoding="utf-8"))
BASE = yaml.safe_load((Path(__file__).resolve().parents[4] / 'plugins/haipipe-toolkit/servers' / "workbench" / "guide" / "levels.yaml").read_text(encoding="utf-8"))
METHOD = (SERVER / "guide" / "method.md").read_text(encoding="utf-8")
PAPERS = (SERVER / "related" / "papers.md").read_text(encoding="utf-8")


def _table(lines):
    """The rows of a Markdown table as dicts by its head; the separator row skipped."""
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if l.startswith("|")]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
    return [dict(zip(rows[0], r)) for r in rows[1:]] if rows else []


def _after(head):
    """The first Markdown table whose head row starts with `head`."""
    i = METHOD.index(head)
    return _table(METHOD[i:].split("\n\n")[0].splitlines())


def role(level):
    """The level's role: the base's words (the design Guide has no levels: yet)."""
    return BASE[level]["role"]


def steps(numbers):
    """Step cards: the six-step rows of method.md § 1 whose step number is in `numbers`."""
    out = []
    for r in _after("| step | what happens |"):
        n = int(r["step"].split("·")[0])
        if n in numbers:
            out.append((r["step"], r["what happens"].split(":")[0], f'where today: {r["where in the workbench"]}   '
                                                                  f'who: {r["who"]}'))
    return out


def method_cards():
    """The thirteen method cards (method.md § 2.3), one per row: the method, its family, its file."""
    return [(r["method"] + " ↗", r["family"] + " · a method card", "guide/" + r["card"])
            for r in _after("| family | method | card |")]


def family_cards():
    """The three families, each with its methods."""
    fam = {}
    for r in _after("| family | method | card |"):
        fam.setdefault(r["family"], []).append(r["method"].replace("By ", "by "))
    return [(f, f"{len(m)} methods", " · ".join(m)) for f, m in fam.items()]


def tests():
    """The five tests T0 to T4 (method.md § 4.1)."""
    return [(r["test"], r["asks"], f'where: {r["where"]}   source: {r["source"]}') for r in _after("| test | asks |")]


def papers(groups):
    """Paper cards: the papers.md rows whose group names one of `groups` (or a method in it)."""
    out = []
    for r in _table(PAPERS.splitlines()):
        have = {g.strip() for g in (r.get("group") or "").split(";")}
        if not have & set(groups):
            continue
        who, _, title = r["paper"].partition(" · ")
        out.append((("★ " if r.get("key") else "") + _short(title or who, 60), f'{who} · {r["venue"]}',
                    f'group: {r["group"]}   role: {r["role"]}   ↗ doi'))
    return out


def method_groups():
    """Every papers.md group that is a method (not `all methods`, not `tests`)."""
    return sorted({g.strip() for r in _table(PAPERS.splitlines()) for g in (r.get("group") or "").split(";")}
                  - {"all methods", "tests", ""})


def _short(s, n):
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def drawings(topics):
    """Drawing cards for b12 studio topics: (topic folder, title, what it shows); the first open."""
    out = []
    for k, (topic, title, shows) in enumerate(topics):
        folder = STUDIO / topic
        pngless = sorted(folder.glob("*.excalidraw"))
        builder = next(iter(sorted(folder.glob("build_*.py")) + sorted(folder.glob("*_drawing.py"))), None)
        line = (f"source: b12_theme_design/studio/{topic}/   built by: {builder.name if builder else 'by hand'}"
                "   ↗ full size" + ("" if pngless else "   ? not on disk"))
        out.append((title, shows, line, k == 0))
    return out


def _ladder(tmp):
    """A placeholder design ladder under a placeholder Project, as the scaffold makes it (✎ 261007: the ladder of
    s11 – s13, was a `_by-<method>` Job): a Block with a signed goal G01 and signed shared rules, inputs i1, a Job
    j01_g01_m04 pinning M04 m2, and one design Task."""
    block = Path(tmp) / "examples-demo" / "Project-Demo" / "designs" / "b01_demo_app"
    job = block / "j01_g01_m04"

    def scaffold(*args):
        subprocess.run([sys.executable, str(SCAFFOLD), *map(str, args)], check=True, capture_output=True)
    scaffold("block", block, "--channel", "<channel>")
    board = block / "board.md"
    board.write_text(board.read_text(encoding="utf-8").replace(
        "goals: []", "goals:\n- id: G01\n  aim: <aim>\n  who: <who>\n  venue: <channel>\n  n: 10\n  rules: []\n"
                     "  leave-out: <what>\n  signed: ✅ 261007"), encoding="utf-8")
    rules = block / "design-goal.md"
    rules.write_text(rules.read_text(encoding="utf-8").replace("signed: ''", "signed: ✅ 261007"), encoding="utf-8")
    (block / "inputs" / "i1").mkdir(parents=True, exist_ok=True)
    scaffold("job", job, "--goal", "G01", "--method", "M04 m2", "--inputs", "i1")
    scaffold("task", job, "d01", "draft")
    (block.parents[1] / "project.yaml").write_text("name: Demo\n", encoding="utf-8")
    return {"Block": block, "Job": job, "Task": job / "t01_d01_draft"}


def space_cards(level):
    """The six Space cards: the base's words, and each Space's third row and run types as the live frame
    gives them for the design theme at this level, over the placeholder ladder."""
    theme = frame.themes()["design"]
    words = BASE[level]["spaces"]
    with tempfile.TemporaryDirectory() as tmp:
        at = _ladder(tmp)[level]
        live = frame.space_cards(theme, level, at, Path(tmp))
    out = []
    for space, subs, runs in live:
        w = words.get(space) or {}
        out.append((space, w.get("is", ""), f'sub: {" · ".join(subs) or "—"}   reads: {w.get("reads", "—")}   '
                                            f'runs: {" · ".join(runs) or "—"}'))
    return out
