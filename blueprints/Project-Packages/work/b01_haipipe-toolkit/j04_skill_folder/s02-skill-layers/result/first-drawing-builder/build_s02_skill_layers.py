"""b04 s02 · Skill layers: s02-skill-layers.excalidraw, what each layer holds and how servers pair
with the workbench skills. Feeds reports/q01_skill_layers.

Read from disk every build: each layer's families and their skills, every workbench-* skill and
the server folder of the same name, folder names that occur twice. The open choices are pink
notes; concerns are red text.

    python build_s02_skill_layers.py [out.excalidraw]
"""
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "_build"))
from sketch import (GRAY, SKILLS, TK, concern, families, legend, mono, questions_frame, save,  # noqa: E402
                    skill_dirs, sticky, text)


def layer_lines(layer):
    if layer == "0_utils":
        return [d.name for d in families(layer)]
    out = []
    for f in families(layer):
        names = [s.name for s in skill_dirs(f)]
        out.append(f"{f.name + '/':<12}{len(names):>3}  " + ", ".join(names[:3]) + (", ..." if len(names) > 3 else ""))
    return out


def pairing_lines():
    servers = TK / "servers"
    out = []
    for sk in sorted(p for p in SKILLS.rglob("workbench*") if p.is_dir() and (p / "SKILL.md").exists()
                     and not any(x.startswith("_") for x in p.relative_to(SKILLS).parts)):
        rel = sk.relative_to(SKILLS).as_posix()
        name = sk.name
        if (servers / name).is_dir():
            srv = f"servers/{name}"
        elif name in ("workbench", "workbench-studio"):
            srv = "servers/workbench (the base)"
        elif name == "workbench-page":
            sub = [d.name for d in (servers / "workbench").iterdir() if d.is_dir() and not d.name.startswith("_")
                   and d.name != "assets"]
            srv = "servers/workbench/" + (sub[0] if sub else "?") + " (the base's Task level)"
        else:
            srv = "! no server of this name"
        depth = len(sk.relative_to(SKILLS).parts)
        out.append(("!" if depth > 3 or srv.startswith("!") else "") + f"{rel:<55} <-> {srv.lstrip('! ')}")
    return out


def duplicate_names():
    names = Counter(p.name for p in SKILLS.rglob("*") if p.is_dir()
                    and not any(x.startswith(("_", ".")) for x in p.relative_to(SKILLS).parts)
                    and len(p.relative_to(SKILLS).parts) <= 4)
    generic = {"ref", "agents", "scripts", "tests", "feedback", "fn", "references", "cli", "lesson", "assets",
               "src", "checks", "templates", "examples", "docs", "studio", "profiles", "methods", "data"}
    return sorted(n for n, c in names.items() if c > 1 and n not in generic)


def draw():
    text(0, -170, "b04 s02 · the three skill layers", 44)
    legend(900, -170)
    text(0, -105, "Read from disk: each layer's families, the workbench skills and their servers. "
                  "Red = open concern; green ✎ = a change.", 20, GRAY)
    x = 0
    bottoms = []
    for layer in ("0_utils", "1_base", "2_theme"):
        r, b = mono(x, 0, layer_lines(layer), f"skills/{layer}/")
        bottoms.append(b)
        x = r + 60
    y = max(bottoms) + 100
    r, b = mono(0, y, pairing_lines(), "workbench skill  <->  server folder")

    sy = 0
    for body, kind in [("1 workbench-page: keep in 1_base\n(its server is the base's Task level)", "idea"),
                       ("2 frame contract: a new 1_base/workbench/\n(workbench, -studio, -page)?", "open"),
                       ("3 servers/: stay flat; the name\nsays the layer", "idea")]:
        sy = sticky(x + 40, sy, 480, body, kind) + 24

    cy = b + 80
    dups = duplicate_names()
    for c in ["? 1_base/task holds 50 skills, among them the HAI-Pipe stage pipelines (data, nn, end,",
              "  individual): is that base, or a domain? (b17 q04 decides the work theme)",
              "? 0_utils also holds personal tools (meal-cam-logger, whoop-connect): a 0_utils, or a",
              "  separate plugin?",
              f"? folder names that occur twice: {', '.join(dups) or 'none'}: skill_dir() returns the",
              "  first one it finds, so a lookup by such a name is ambiguous",
              "? the page family holds three workbench skills (workbench, -studio, -page) for one",
              "  server, while each theme has one"]:
        cy = concern(0, cy, c) + 6

    qs = dict((q, t) for q, t in __import__("sketch").board_questions(BLOCK))
    questions_frame(0, cy + 120, [
        (f"Q01 · {qs.get('q01_skill_layers', 'skill layers')}",
         [("choices 1-3 above; recommended:\n1 keep, 2 new family, 3 flat", "idea"),
          ("your call on 2 (moving workbench,\n-studio, -page out of page/)", "open")]),
        ("(proposed) Is every theme folder the same shape?\na haipipe-<theme> door, workbench-<theme> at the\n"
         "family top, its agents in one place (see s04)",
         [("s04 reads each theme's shape", "idea")]),
    ])


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s02-skill-layers.excalidraw", "build_s02_skill_layers.py")
