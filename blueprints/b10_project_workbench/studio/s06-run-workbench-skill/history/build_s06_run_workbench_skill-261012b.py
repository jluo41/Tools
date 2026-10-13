"""s06 · Run: its workbench and its skill: s06-run-workbench-skill.excalidraw (haipipe-studio).

Three frames (JL 261012: "每一个 frame 都太像一张 slide ... 我个人更 prefer 那种 tree 结构"): ① Background, the words
a newcomer needs and where a Run sits; ② the Tree, the topic itself as one folder tree (what a Run is, hard and
soft, passes, the workbench and the skill, the folders in Tools, red ? leaves where it is still open); ③ the
screen, this Block's Runs Space as servers/workbench/frame.py draws it, beside the skill (a ui_frame).

Read from disk on every build: this Block's own Runs (runs/*/run.yaml and each ticket's close: line), the Runs
Space as servers/workbench/frame.py draws it for this Block, haipipe-run's version and folder. Typed, since they
are the design or sit in another repository: the hard example (Proj11-CGM-Corpus r01_rate_tir_hypo), the rules of
hard and soft, the open points. The 261010 and 261012 builders (five frames, then four frames and a row below)
are in history/.

    python build_s06_run_workbench_skill.py [out.excalidraw]
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


# ── drawing helpers (black lines, unfilled boxes; red = open, green = changed) ───────────────────
def rect(x, y, w, h, bold=False, dashed=False):
    return L.base("rectangle", x, y, w, h, L.INK, 3 if bold else 1.5, dashed, rough=0)


def say(x, y, s, size=BODY, color=L.INK, font=L.SANS):
    L.text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n))


def line(pts, arrow=True, dashed=False):
    L.path(pts, arrow=arrow, color=L.INK, dashed=dashed)


def note(x, y, what):
    """A green change note where the change is (haipipe-studio: ✎ <date> <what>)."""
    e = canvas.change_note(x, y, what, TODAY, L.FRAME[0], size=18)
    L.els.append(e)
    return e


def heading(n, title, under):
    say(0, 0, f"{n} {title}", T)
    return say(0, 58, under, SUB)


def tree(x, y, rows, gap=500):
    """A folder tree in Cascadia: (path, what it is) per line."""
    for k, (path, what) in enumerate(rows):
        say(x, y + k * 32, path, CODE, font=L.MONO)
        if what:
            say(x + gap, y + k * 32 + 1, what, BODY)
    return y + len(rows) * 32


# ── drawing helpers ─────────────────────────────────────────────────────────────────────────────
def rect(x, y, w, h, bold=False, dashed=False):
    return L.base("rectangle", x, y, w, h, L.INK, 3 if bold else 1.5, dashed, rough=0)


def say(x, y, s, size=BODY, color=L.INK, font=L.SANS):
    L.text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n))


def line(pts, arrow=True, dashed=False):
    L.path(pts, arrow=arrow, color=L.INK, dashed=dashed)


def tree_frame(name, title, lines, nodes, width, cols):
    """One frame: a title, a few lines under it, then the folder tree (canvas.tree)."""
    fr = L.open_frame(name)
    L.text(0, 0, title, T)
    y = 58
    for ln in lines:
        L.text(0, y, ln, SUB)
        y += 32
    els, _ = canvas.tree(0, y + 8, nodes, width, fr["id"], size=20, head=24, cols=cols)
    L.els.extend(els)
    L.close_frame(fr)
    return fr


# ── ① Background ────────────────────────────────────────────────────────────────────────────────
BACKGROUND = [
    {"The words": [
        "Run: one piece of work, asked for once; one folder, runs/<run>/",
        "ticket: the ask, written down (who does what, with which inputs)",
        "close rule: how we know it is done, or honestly not done",
        "pass: one more round on the same target (passes/pNN-<MMDD>/)",
        "hard Run: makes new evidence in its own result/; soft Run: changes what its level keeps",
        "Runs Space: the list of a level's Runs; Runs panel: the buttons beside every Space",
        "skill: /haipipe-run, the owner of the card (run.yaml) and the passes"]},
    {"Where it sits": [
        "Block > Job > Task > Run > pass",
        "a Run lives in the runs/ of its level",
        "a Task holds hard and soft Runs; a Block and a Job, soft only"]},
    {"Why this topic": [
        "JL 261007: how do we manage the runs, soft and hard, in the folder and on screen",
        "feeds q01 (what a Run is, where it may sit) and q07 (the Runs panel, the pop-out)",
        "earlier decisions: s01-D14, s01-D15; the skill change: s01 run-skill-draft.md"]},
]


# ── ② the Tree ──────────────────────────────────────────────────────────────────────────────────
def tree_nodes(runs, space, version):
    heads, rows, subs, buttons = space
    card, close = runs[EXAMPLE]
    writes = card.get("writes") or []
    out_dir = (writes[0].rsplit("/", 1)[0] + "/") if writes else "its result/"
    missing = [r for r, (_c, cl) in runs.items() if not named_close(cl)]
    pcard, _pc = runs[PASSES]
    passes = pcard.get("passes") or []
    label, doing = buttons[0] if buttons else ("", "")

    parts = {f"a Run ({EXAMPLE}, read from its ticket and run.yaml)": [
        f"target: {card.get('target')}",
        f"ticket: {card.get('ticket')}",
        f"close rule: {textwrap.shorten(close, 70, placeholder=' …')}",
        f"output: {out_dir}",
        f"{len(card.get('passes') or [])} passes, status {card.get('status')}"]}
    if missing:
        parts[f"a Run (close rules)"] = [f"? {len(missing)} of {len(runs)} Runs here have no close rule: "
                                         f"{', '.join(missing)}"]
        a_run_close = []
    else:
        a_run_close = [f"✎ 261012 all {len(runs)} Runs here name their close rule; new_topic.py now writes one (s06-D06)"]

    what = {"1  What a Run is": [parts, {"is a Run": [
        "a model fit, with its own result/", "redrawing one studio topic: run-draw-s21",
        "writing one report: run-report-q05", "checking one report in a fresh context: run-check-q05"]},
        {"is a step, or a new pass": [
            "one click, one tool call, one script line: a step",
            "a retry, same ticket and inputs: a new pass",
            "a later session on the same target: a new pass",
            "a comment or a signature: a step, unless asked for on its own"]},
        {"earns a Run when all six hold": [
            "a named target", "a type, so its owner can name it", "a ticket that asks",
            "a close rule", "an output that lasts", "it closes without the screen open"]}] + a_run_close}

    hard = {"2  Hard: rNN_<slug>": [
        "makes new evidence: a number, a table, a figure",
        "keeps it in its own result/, generated; lives only in a work Task",
        "a Page reads it and never recomputes it",
        {"e.g. Proj11-CGM-Corpus r01_rate_tir_hypo": [
            "runs/r01_rate_tir_hypo/", "  run.yaml: the card", "  r01_rate_tir_hypo.sh: the ticket, runnable",
            "  config.yaml: its frozen inputs", "  result/: metrics.json, reward_spec.yaml",
            "  passes/p01-<MMDD>/: log, runtime.yaml",
            "? still in the older layout: runs/r01_rate_tir_hypo.sh beside results/r01_rate_tir_hypo/ (open 6)"]}]}
    soft = {"3  Soft: run-<type>-<target>": [
        "changes something its level keeps: draft/ studio/ reports/ delivery/",
        "lives at a Block, a Job or a Task; work, not evidence",
        "a new number needs a hard Run in a work Task; a person's decision is soft too",
        {f"e.g. {PASSES} (this Block, read from run.yaml)": [
            f"kind {pcard.get('kind')} · type {pcard.get('type')} · status {pcard.get('status')}",
            f"{pcard.get('ticket')}: target · ask · close",
            f"passes/: {', '.join(passes)}"]}]}

    pass_node = {"4  Every round is a pass": [
        f"{PASSES}: {len(passes)} sessions on topic {pcard.get('target')} = one Run, {len(passes)} passes",
        {"same Run, a new pass": ["a later session on the same target", "a retry: same ticket and inputs",
                                  "feedback inside the same goal: a step in the open pass"]},
        {"a new Run": ["new inputs, data, goal or close rule", "a new target: another sNN, another qNN",
                       "? a wet Run repeated: a replication, proposed in s06-D02"]},
        {"what a pass holds": ["hard: its log and runtime.yaml, written by the ticket",
                               "soft: pass.md (ask, summary, changed), written by soft_run.py pass",
                               "a pass grows while open and never changes once closed (s06-D03)"]}]}

    shown = {"5  On screen: the workbench": [
        f"Runs Space of Block {BLOCK.name.split('_')[0]}, read from frame.py: {len(heads)} columns, "
        f"{len(rows)} rows",
        f"columns: {' · '.join(heads)}",
        f"third row: {' · '.join(subs)}",
        f"Runs panel beside every Space: buttons copy a prompt and start nothing (first: {label})",
        f"? {len(heads)} columns today; s06-D01 proposed seven (run · kind · type · target · status · passes · last)",
        "? a row opens nothing yet: the Run pop-out (card and passes) is proposed in s06-D01"]}

    skill = {f"6  The skill and its code (haipipe-run {version})": [
        "owns what a Run is, the folder, run.yaml and its passes",
        "soft_run.py new <scope> --type draw --target s05",
        "soft_run.py pass <scope>/runs/run-draw-s05",
        "run.yaml and passes are written by tools, never typed by hand",
        {"each button's skill makes the output": ["haipipe-studio draws; haipipe-report writes",
                                                   "haipipe-task runs a hard Run",
                                                   "haipipe-run keeps only the card and the passes"]},
        {"in Tools/plugins/haipipe-toolkit": [
            "skills/1_base/project/haipipe-run/", "servers/workbench/frame.py: runs_of",
            "servers/workbench/runs_panel.py: run_types, panel_html, panel_markup"]}]}

    openq = {"7  Still open": [
        "? wet Runs: add the protocol ticket and the person-signed receipt to haipipe-run? (s06-D02)",
        "? a Job holds soft Runs only: where does a batch launch, run-launch-<group>, go?",
        "? a hard Run's heavy output: show it on screen, or only its heavy.yaml pointer?",
        "? the Runs Space: this level's Runs only, or rolled up from the levels below?",
        "? a soft pass: when does it close, and who writes its touched.yaml?",
        "? the older layout: when does haipipe-project update move it?",
        f"? the Runs Space shows {len(heads)} columns and no pop-out: build s06-D01?"]}
    if missing:
        openq["7  Still open"].append(f"? {len(missing)} of {len(runs)} Runs in b10 have no close rule: "
                                      "should soft_run.py new refuse a ticket without one?")
    return [what, hard, soft, pass_node, shown, skill, openq]


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


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s06-run-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    runs, space, version = block_runs(), runs_space(), skill_version()
    ui = frame_screen(space, version)
    bg = tree_frame("Background: what a Run is", "Background: the Run, for a newcomer",
                    ["The words this topic uses, and where a Run sits. The topic itself is the Tree."],
                    BACKGROUND, 1500, 1)
    tree = tree_frame("The Tree: Run, workbench and skill", "The Run: what it is, its workbench, its skill",
                      ["What a Run is, hard and soft, passes, the screen and the skill; red ? leaves are still open."],
                      tree_nodes(runs, space, version), 2600, 3)
    canvas.grid(L.els, [[bg["id"], tree["id"]], [ui["id"]]])
    for e in canvas.off_palette(L.els):
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s06_run_workbench_skill.py")


if __name__ == "__main__":
    main()
