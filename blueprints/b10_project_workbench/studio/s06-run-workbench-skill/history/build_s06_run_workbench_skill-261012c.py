"""s06 · Run: its workbench and its skill: s06-run-workbench-skill.excalidraw (haipipe-studio 0.13.0).

Three frames: ① Background, a folder tree; ② the Run, boxes with their own trees joined by named arrows (a button
starts a Run, a Run keeps passes and a result, the screen lists them, the skill owns the card); ③ the screen, this
Block's Runs Space as servers/workbench/frame.py draws it, beside the skill (a ui_frame, drawn here).
Frames ① and ② are the face's `frames:` yaml, drawn by topic_map.draw_topic; the words in ‹ › are filled from the
disk on every build: this Block's Runs (runs/*/run.yaml and each ticket's close: line), the Runs Space as
frame.py draws it, haipipe-run's version. The 261010 and 261012 builders are in history/.

    python build_s06_run_workbench_skill.py
"""
import html
import re
import sys
import textwrap
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent                                      # b10's studio/
BLOCK = STUDIO.parent                                     # b10_project_workbench/
TOOLS = HERE.parents[3]                                   # s05 -> studio -> b10 -> blueprints -> Tools
ROOT = TOOLS
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
RUN_SKILL = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-run"
sys.path.insert(0, str(STUDIO / "s01-overall-tree-structure"))
sys.path.insert(0, str(SERVERS / "_host"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers: base, text, path, frames)
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
import canvas  # noqa: E402

TODAY = "261012"
EXAMPLE = "run-report-q05"                                 # ①'s Run: a soft Run of this Block with all four parts
PASSES = "run-draw-s21"                                    # ③'s Run: one target, two sessions
T, SUB, BODY, HEAD, CODE = 34, 22, 22, 24, 20              # frame title · line under it · words · box titles · paths


# ── facts, read from disk ───────────────────────────────────────────────────────────────────────
def block_runs():
    """{run: (card, close)} for every Run folder in this Block's runs/: its run.yaml and its ticket's close: line."""
    out = {}
    for d in sorted((BLOCK / "runs").iterdir()):
        if not (d / "run.yaml").is_file():
            continue
        card = yaml.safe_load((d / "run.yaml").read_text(encoding="utf-8")) or {}
        ticket = d / (card.get("ticket") or d.name + ".md")
        m = re.search(r"(?m)^close:\s*(.*)$", ticket.read_text(encoding="utf-8")) if ticket.is_file() else None
        out[d.name] = (card, m.group(1).strip() if m else "")
    return out


def named_close(close):
    return bool(close) and not close.startswith("<")


def runs_space():
    """This Block's Runs Space as frame.py draws it: (column heads, rows, third-row buttons, Runs-panel buttons)."""
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    sp = frame.spaces_for(frame.VANILLA, "Block", BLOCK, ROOT)["Runs"]
    cells = lambda s: [html.unescape(re.sub(r"<[^>]*>", "", c)) for c in re.findall(r"<td>(.*?)</td>", s)]
    heads = [html.unescape(h) for h in re.findall(r"<th>(.*?)</th>", sp.html)]
    rows = [cells(r) for r in re.findall(r"<tr>(.*?)</tr>", sp.html) if "<td>" in r]
    return heads, rows, list(sp.subspaces), [(k["label"], k.get("doing", "")) for k in sp.run_types]


def skill_version():
    m = re.search(r'version:\s*"([^"]+)"', (RUN_SKILL / "SKILL.md").read_text(encoding="utf-8"))
    return m.group(1) if m else "?"


# ── drawing helpers for the screen frame ────────────────────────────────────────────────────────
def rect(x, y, w, h, bold=False, dashed=False):
    return L.base("rectangle", x, y, w, h, L.INK, 3 if bold else 1.5, dashed, rough=0)


def say(x, y, s, size=BODY, color=L.INK, font=L.SANS):
    L.text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n))


def line(pts, arrow=True, dashed=False):
    L.path(pts, arrow=arrow, color=L.INK, dashed=dashed)


# ── ③ the screen ────────────────────────────────────────────────────────────────────────────────
def frame_screen(space, version):
    heads, rows, subs, buttons = space
    fr = L.open_frame("The screen: Runs Space and skill")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    L.text(0, 0, "The screen: Block b10 › Runs, and /haipipe-run", T)
    y = say(0, 58, "Read from servers/workbench/frame.py; buttons start Runs, the list reads each run.yaml.", SUB) + 30
    x = 0
    for k, s in enumerate(subs):                              # the third row
        w = int(len(s) * BODY * 0.55) + 40
        rect(x, y, w, 46, bold=k == 0)
        say(x + 20, y + 10, s, BODY)
        x += w + 12
    y += 70
    xs = [0, 320, 440, 560]
    for c, h in zip(xs, heads):
        say(c, y, h, HEAD)
    y += 40
    line([(0, y), (820, y)], arrow=False)
    y += 10
    for r in rows:
        for c, v in zip(xs, r):
            say(c, y, v, CODE, font=L.MONO)
        y += 34
    line([(0, y + 4), (820, y + 4)], arrow=False)
    y += 30
    label, doing = buttons[0] if buttons else ("", "")
    say(0, y, wrap(f"Runs panel, beside every Space: its buttons copy a prompt and start nothing. "
                   f"Here: {label}, \"{doing}\".", 66), BODY)
    xr, yr = 960, 110
    rect(xr, yr, 780, 440, bold=True)
    say(xr + 24, yr + 18, f"SKILL  /haipipe-run  {version}", HEAD)
    say(xr + 24, yr + 56, "skills/1_base/project/haipipe-run", CODE, font=L.MONO)
    yy = yr + 110
    for s in ["owns what a Run is: hard and soft, the folder,", "run.yaml and its passes",
              "names every button's Run and its skill", "(ref/run-types-by-space.md; drawn in s21)"]:
        yy = say(xr + 24, yy, s, BODY)
    yy += 24
    for s in ["soft_run.py new  <scope> --type draw --target s05", "soft_run.py pass <scope>/runs/run-draw-s05"]:
        yy = say(xr + 24, yy, s, CODE, font=L.MONO) + 4
    yy += 20
    for s in ["run.yaml and passes are written by tools,", "never typed by hand"]:
        yy = say(xr + 24, yy, s, BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── words read from the disk, put into the face's yaml ──────────────────────────────────────────
def fills(runs, space, version):
    heads, rows, subs, buttons = space
    card, close = runs[EXAMPLE]
    pcard, _pc = runs[PASSES]
    passes = pcard.get("passes") or []
    missing = [r for r, (_c, cl) in runs.items() if not named_close(cl)]
    return {
        "first_button": buttons[0][0] if buttons else "?",
        "example_line": f"✅ example {EXAMPLE}: target {card.get('target')}, {len(card.get('passes') or [])} passes, status {card.get('status')}",
        "example_ticket": str(card.get("ticket")),
        "example_close": textwrap.shorten(close, 60, placeholder=" ..."),
        "close_line": (f"all {len(runs)} Runs here name their close rule; new_topic.py writes one (s06-D06)" if not missing
                       else f"{len(missing)} of {len(runs)} Runs here have no close rule: {', '.join(missing)}"),
        "passes_line": f"{PASSES}: {len(passes)} sessions on topic {pcard.get('target')} = one Run, {len(passes)} passes",
        "cols_line": f"columns: {' · '.join(heads)} ({len(rows)} rows)",
        "cols_n": str(len(heads)), "subs": " · ".join(subs), "version": version,
        "passes_run": PASSES, "passes_kind": str(pcard.get("kind")), "passes_status": str(pcard.get("status")),
    }


def fill(node, vals):
    if isinstance(node, str):
        for k, v in vals.items():
            node = node.replace("\u2039" + k + "\u203a", v)
        return node
    if isinstance(node, list):
        return [fill(n, vals) for n in node]
    if isinstance(node, dict):
        return {fill(k, vals): fill(v, vals) for k, v in node.items()}
    return node


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────
def main():
    runs, space, version = block_runs(), runs_space(), skill_version()
    vals = fills(runs, space, version)
    import topic_map

    def screen_frame(els):
        L.els.clear()
        L.FRAME[0] = None
        frame_screen(space, version)
        els.extend(L.els)

    topic_map.draw_topic(HERE, extra=screen_frame, source="build_s06_run_workbench_skill.py",
                         fill=lambda frames: fill(frames, vals))      # the ‹ › words, read from disk


if __name__ == "__main__":
    main()
