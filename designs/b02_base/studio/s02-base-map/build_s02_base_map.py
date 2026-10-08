"""b02 s02 · Base map: s02-base-map.excalidraw, who calls each base family. Feeds reports/q01_base_map.

Read from disk every build, through callmap.py (an index of which files name which skills):

    family x caller      one row per base family, one column per caller (each theme, each other
                         base family, 0_utils, servers, other plugins): how many files name any
                         skill of that family
    theme x theme        the same count between themes: the layer rule says it should be empty
    single caller        base skills named by exactly one theme outside their family (candidates
                         to move into that theme) and base skills nobody outside names

Draws with b04's helpers through b03's canvas.write, so a person's marks survive a rebuild.

    python build_s02_base_map.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(next(p for p in BLOCK.parent.glob("*/studio/_build/sketch.py")).parent))
import callmap as C  # noqa: E402
from sketch import GRAY, concern, families, legend, mono, questions_frame, save, sticky, text  # noqa: E402

BASE = [f.name for f in families("1_base")]
THEMES = [f.name for f in families("2_theme")]
ABBR = {"cowork": "cow", "design": "des", "discovery": "dis", "insight": "ins", "labeling": "lab", "paper": "pap",
        "work": "wrk", "project": "prj", "task": "tsk", "page": "pag", "question": "que", "writing": "wri",
        "display": "dsp", "ideation": "ide", "search": "sea"}


def family_pattern(folder: Path):
    names = [s.name for s in C.skills_of(folder)]
    return names, re.compile("|".join(C.pattern(n).pattern for n in names)) if names else None


def family_callers(layer: str, fam: str) -> dict:
    home = f"{layer}/{fam}"
    names, pat = family_pattern(C.SKILLS / layer / fam)
    out = {}
    if pat is None:
        return out
    for f, area, txt in C.corpus():
        if area != home and pat.search(txt):
            out[area] = out.get(area, 0) + 1
    return out


def cell(n):
    return f"{n:>4}" if n else "   ."


def base_table():
    cols = [f"2_theme/{t}" for t in THEMES] + [f"1_base/{b}" for b in BASE] + ["0_utils", "servers"]
    others = sorted({p.name for p in C.PLUGINS.iterdir() if p.is_dir() and p.name != "haipipe-toolkit"
                     and not p.name.startswith((".", "_"))})
    head = f"{'':<10}" + "".join(f"{ABBR[c.split('/')[1]]:>4}" for c in cols[:len(THEMES)]) + " |" \
        + "".join(f"{ABBR[c.split('/')[1]]:>4}" for c in cols[len(THEMES):len(THEMES) + len(BASE)]) + " |" \
        + f"{'0u':>4}{'srv':>4}" + "".join(f"{o[:6]:>8}" for o in others)
    lines = [head, ""]
    rows = {}
    for b in BASE:
        cc = family_callers("1_base", b)
        rows[b] = cc
        themes = "".join(cell(cc.get(c, 0)) for c in cols[:len(THEMES)])
        bases = "".join(("   -" if c == f"1_base/{b}" else cell(cc.get(c, 0))) for c in cols[len(THEMES):len(THEMES) + len(BASE)])
        tail = cell(cc.get("0_utils", 0)) + cell(cc.get("servers", 0)) + "".join(f"{cc.get(o, 0) or '.':>8}" for o in others)
        n_themes = sum(1 for c in cols[:len(THEMES)] if cc.get(c))
        lines.append(f"{b:<10}{themes} |{bases} |{tail}   {n_themes}/{len(THEMES)} themes")
    return lines, rows


def theme_table():
    head = f"{'':<10}" + "".join(f"{ABBR[t]:>5}" for t in THEMES)
    lines, bad = [head, ""], []
    for t in THEMES:
        cc = family_callers("2_theme", t)
        cells = []
        for u in THEMES:
            n = cc.get(f"2_theme/{u}", 0) if u != t else None
            cells.append("    -" if n is None else (f"{n:>5}" if n else "    ."))
            if n:
                bad.append((u, t, n))
        lines.append(f"{t:<10}" + "".join(cells))
    lines.append("")
    lines.append("row = the theme whose skills are named; column = the theme naming them")
    return lines, bad


def single_callers():
    single, none = [], []
    for b in BASE:
        for s in C.skills_of(C.SKILLS / "1_base" / b):
            cc = {a: n for a, n in C.callers(s.name, f"1_base/{b}").items() if a not in ("toolkit", "agents")}
            if not cc:
                none.append(f"{b}/{s.name}")
            elif len(cc) == 1 and next(iter(cc)).startswith("2_theme/"):
                single.append(f"{b + '/' + s.name:<48} only {next(iter(cc)).split('/')[1]}")
    return single, none


def draw():
    text(0, -170, "b02 s02 · who calls each base family", 44)
    legend(1300, -170)
    text(0, -105, "Read from disk: files that name a skill (`name`, /name, \"name\", skill: name). History left out. "
                  "Numbers = files.", 20, GRAY)
    lines, rows = base_table()
    r1, b1 = mono(0, 0, lines, "base family x caller (themes | other base families | 0_utils, servers, plugins)", size=14)

    tlines, bad = theme_table()
    named = {t for _, t, _ in bad}                      # rows whose skills another theme names
    tlines = [("!" + l) if any(l.startswith(f"{t:<10}") for t in named) else l for l in tlines]
    r2, b2 = mono(0, b1 + 80, tlines, "theme x theme: should be empty (a theme never calls another theme)", size=14)

    single, none = single_callers()
    r3, b3 = mono(r2 + 80, b1 + 80, single or ["(none)"], "base skills named by only one theme", size=14)
    r4, b4 = mono(r2 + 80, b3 + 60, [", ".join(none[i:i + 3]) for i in range(0, len(none), 3)] or ["(none)"],
                  f"base skills nobody outside their family names ({len(none)})", size=14)

    y = max(b2, b4) + 80
    core = [b for b, cc in rows.items() if sum(1 for t in THEMES if cc.get(f"2_theme/{t}")) >= len(THEMES) - 2]
    sticky(0, y, 600, "Called by (almost) every theme:\n" + ", ".join(core), "done")
    sticky(640, y, 600, "A single-caller base skill is a candidate to\nmove into its one theme (Q03 decides).", "idea")
    sticky(1280, y, 600, "A theme naming another theme's skills breaks\nthe layer rule (red rows in theme x theme).", "idea")

    cy = y + 200
    notes = ["? Counts are files that NAME a skill: a mention in a doc counts like a call in code. Good for a map,",
             "  not proof of a dependency; s03 can split code calls from doc mentions."]
    if bad:
        worst = sorted(bad, key=lambda b: -b[2])[:4]
        notes.append("? Themes naming other themes' skills: " + "; ".join(f"{u} names {t} ({n})" for u, t, n in worst) +
                     ". Real dependencies, or just cross-links in docs?")
    few = sorted((sum(1 for t in THEMES if cc.get(f"2_theme/{t}")), b) for b, cc in rows.items())
    few = [(n, b) for n, b in few if n <= 2]
    notes.append("? Base families called by at most 2 themes: " + ", ".join(
        f"{b} ({n}: " + ", ".join(t for t in THEMES if rows[b].get(f"2_theme/{t}")) + ")" for n, b in few) + ".")
    notes.append("  A family only one theme calls (search: discovery) may belong in that theme. (Q03)")
    for c in notes:
        cy = concern(0, cy, c) + 6

    qs = dict(re.findall(r"- id: (Q\d+)\n\s+title: (.+)", (BLOCK / "board.md").read_text(encoding="utf-8")))
    questions_frame(0, cy + 120, [
        (f"Q01 · {qs.get('Q01', '')}",
         [("answer drafted in reports/q01_base_map", "idea"),
          ("your call: is a doc cross-link between\nthemes allowed, or only base calls?", "open")]),
        (f"Q03 · {qs.get('Q03', '')}", [("single-caller skills above feed\ns04-not-base", "idea")]),
    ])
    return rows, bad, single, none


if __name__ == "__main__":
    draw()
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s02-base-map.excalidraw", "build_s02_base_map.py")
