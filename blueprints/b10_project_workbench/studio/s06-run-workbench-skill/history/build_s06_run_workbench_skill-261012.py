"""s06 · Run: its workbench and its skill: s06-run-workbench-skill.excalidraw, one story read left to right
(JL 261011: "call it run-workbench-skill ... make the run to be a good definition and explanation, about
what they are doing"); s06 since JL set the order by the screen: s02 Studio, s03 Delivery, s04 Related, s05 Report.

    ① what a Run is  -->  ② what it leaves: hard or soft  -->  ③ every round is a pass  -->  ④ the workbench
                                                                                           shows it, /haipipe-run
                                                                                           keeps it
    still open (red)            hard and soft row by row, and the folders (reference)

Read from disk on every build: this Block's own Runs (runs/*/run.yaml and each ticket's close: line), the
Runs Space as servers/workbench/frame.py draws it for this Block, and haipipe-run's version. Typed, since they
are the design or sit in another repository: the hard example (Proj11-CGM-Corpus r01_rate_tir_hypo), the
rules of ② and ③, the open points. The 261010 builder (five frames, then s05-runs) is in history/.

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

TODAY = "261011"
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


# ── ① what a Run is ──────────────────────────────────────────────────────────────────────────────
def frame_what(runs):
    fr = L.open_frame("What a Run is")
    y = heading("①", "What a Run is",
                "One piece of work, asked for once: a target, an ask, a rule that says done, an output that lasts.") + 40
    card, close = runs[EXAMPLE]
    writes = card.get("writes") or []
    parts = [("target", "what it works on", f"target: {card.get('target')}"),
             ("ticket", "the ask, written down:\nwho does what", f"{card.get('ticket')}"),
             ("close rule", "how we know it is done,\nor honestly not done", wrap(close, 30).split("\n")[0] + " …"),
             ("output", "what stays after it:\nits result/, or what it changed",
              (writes[0].rsplit("/", 1)[0] + "/") if writes else "")]
    bw, gap = 380, 26
    width = 4 * bw + 3 * gap
    cx = width // 2
    rect(cx - 300, y, 600, 118, bold=True)
    say(cx - 270, y + 16, "a Run", HEAD)
    say(cx - 270, y + 60, "one folder: runs/<run>/", CODE, font=L.MONO)
    top = y + 118 + 70
    for i, (title, what, example) in enumerate(parts):
        x = i * (bw + gap)
        line([(cx, y + 118), (x + bw // 2, top)], arrow=False)
        rect(x, top, bw, 210)
        say(x + 22, top + 16, title, HEAD)
        say(x + 22, top + 58, what, BODY)
        say(x + 22, top + 150, example, CODE, font=L.MONO)
    y = top + 240
    y = say(0, y, f"The example is {EXAMPLE}, a Run of this Block, read from its ticket and run.yaml: "
                  f"{len(card.get('passes') or [])} passes, status {card.get('status')}.", BODY) + 6
    missing = [r for r, (_c, cl) in runs.items() if not named_close(cl)]
    if missing:
        y = say(0, y, wrap(f"? {len(missing)} of {len(runs)} Runs here have no close rule: {', '.join(missing)} "
                           f"still say <what settles it>.", 120), BODY, L.RED) + 6
    else:
        y = say(0, y, f"All {len(runs)} Runs here name their close rule.", BODY) + 6
        note(0, y, "close rules filled; new_topic.py now writes one (s06-D06)")
        y += 26
    y += 34
    say(0, y, "Where it sits", HEAD)
    x = 260
    for k, lv in enumerate(("Block", "Job", "Task", "Run", "pass")):
        w = 120 if lv != "Run" else 110
        rect(x, y - 8, w, 46, bold=lv == "Run")
        say(x + 20, y + 2, lv, BODY)
        if k < 4:
            line([(x + w + 6, y + 15), (x + w + 44, y + 15)])
        x += w + 50
    y = say(0, y + 60, "A Run sits in its level's runs/. A Task holds hard and soft Runs; a Block and a Job, soft only.",
            BODY) + 34
    say(0, y, "Is a Run", HEAD)
    say(820, y, "Is not a new Run", HEAD)
    y += 44
    yes = ["a model fit, with its own result/", "redrawing one studio topic: run-draw-s21",
           "writing one report: run-report-q05", "checking one report in a fresh context: run-check-q05"]
    no = ["one click, one tool call, one script line  → a step in a Run",
          "a retry with the same ticket and inputs  → a new pass",
          "a later session on the same target  → a new pass",
          "a comment or a signature  → a step, unless asked for on its own"]
    for k, (a, b) in enumerate(zip(yes, no)):
        say(0, y + k * 34, a, BODY)
        say(820, y + k * 34, b, BODY)
    y += 4 * 34 + 34
    say(0, y, "It earns a Run when all six hold", HEAD)
    y += 44
    six = ["1  a named target", "2  a type, so its owner can name it", "3  a ticket that asks",
           "4  a close rule", "5  an output that lasts", "6  it closes without the screen open"]
    for k, s in enumerate(six):
        say((k // 3) * 820, y + (k % 3) * 34, s, BODY)
    note(0, y + 3 * 34 + 16, "the Run defined first, in plain words (JL)")
    L.close_frame(fr, pad=60)
    return fr


# ── ② what it leaves: hard or soft ───────────────────────────────────────────────────────────────
HARD_RULES = ["makes new evidence: a number, a table, a figure", "keeps it in its own result/, generated",
              "lives only in a work Task", "a Page reads it and never recomputes it"]
SOFT_RULES = ["changes something its level keeps", "writes into draft/ · studio/ · reports/ · delivery/",
              "lives at a Block, a Job or a Task", "work, not evidence: its passes say what changed"]
HARD_TREE = [("runs/r01_rate_tir_hypo/", ""), ("├── run.yaml", "the card"),
             ("├── r01_rate_tir_hypo.sh", "the ticket, runnable"), ("├── config.yaml", "its frozen inputs"),
             ("├── result/", "metrics.json · reward_spec.yaml"), ("└── passes/p01-<MMDD>/", "log · runtime.yaml")]


def frame_kinds(runs):
    fr = L.open_frame("Hard or soft")
    y = heading("②", "What it leaves: hard or soft",
                "A hard Run makes new evidence in its own result/; a soft Run changes something its level keeps.") + 40
    card, _close = runs[PASSES]
    soft_tree = [(f"runs/{PASSES}/", ""),
                 ("├── run.yaml", f"kind: {card.get('kind')} · type: {card.get('type')} · status: {card.get('status')}"),
                 (f"├── {card.get('ticket')}", "the ticket: target · ask · close"), ("└── passes/", "")]
    soft_tree += [(("    └── " if k == len(card.get("passes") or []) - 1 else "    ├── ") + f"{p}/pass.md",
                   "the ask · summary · changed" if k == 0 else "")
                  for k, p in enumerate(card.get("passes") or [])]
    cols = [(0, "HARD", "rNN_<slug>", HARD_RULES,
             ["e.g. r01_rate_tir_hypo", "Proj11-CGM-Corpus › b04_grpo_corpus › j02_reward_functions",
              "› t01_reward_definition; target: rate of change, time in", "range, hypoglycemia ahead"], HARD_TREE),
            (900, "SOFT", "run-<type>-<target>", SOFT_RULES,
             [f"e.g. {PASSES}, in this Block (b10)", f"target: topic {card.get('target')}; read from its run.yaml"],
             soft_tree)]
    bottom = y
    for x, kind, name, rules, example, rows in cols:
        rect(x, y, 820, 70, bold=True)
        say(x + 24, y + 18, kind, HEAD)
        say(x + 140, y + 21, name, CODE, font=L.MONO)
        yy = y + 100
        for r in rules:
            yy = say(x, yy, r, BODY) + 4
        yy += 26
        for ex in example:
            yy = say(x, yy, ex, BODY)
        bottom = max(bottom, tree(x, yy + 20, rows, gap=340))
    y = say(0, bottom + 30, wrap("? r01_rate_tir_hypo is still in the older layout: runs/r01_rate_tir_hypo.sh "
                                 "beside results/r01_rate_tir_hypo/ (open 6).", 80), BODY, L.RED) + 40
    rect(0, y, 1720, 110)
    say(24, y + 18, "The rule: a new number needs a hard Run in a work Task. A Run that only changes a draft, a drawing,",
        BODY)
    say(24, y + 58, "a report or a delivery is soft; so is a person's decision (signing a goal, a release).", BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── ③ every round is a pass ──────────────────────────────────────────────────────────────────────
def frame_passes(runs):
    fr = L.open_frame("Every round is a pass")
    y = heading("③", "Every round is a pass",
                "The same target again is a new pass; new inputs or a new target make a new Run.") + 50
    card, _close = runs[PASSES]
    passes = card.get("passes") or []
    steps = [("run type", "a button names it:\nrun-draw-<sNN>"), ("ticket + card", "run.yaml written,\nstatus: planned")]
    steps += [(f"pass {p}", "round 1: ask ·\nsummary · changed" if k == 0 else f"round {k + 1},\nthe same target")
              for k, p in enumerate(passes)]
    steps += [("closed", "the passes stay\nas they were")]
    bw, gap = 290, 54
    for k, (title, what) in enumerate(steps):
        x = k * (bw + gap)
        rect(x, y, bw, 150, bold=title.startswith("pass"))
        say(x + 20, y + 16, title, HEAD)
        say(x + 20, y + 60, what, BODY)
        if k < len(steps) - 1:
            line([(x + bw + 6, y + 75), (x + bw + gap - 6, y + 75)])
    y += 180
    y = say(0, y, f"{PASSES} in this Block: {len(passes)} sessions on topic {card.get('target')}, so one Run with "
                  f"{len(passes)} passes (read from its run.yaml).", BODY) + 40
    say(0, y, "The same Run, a new pass", HEAD)
    say(860, y, "A new Run", HEAD)
    y += 46
    same = ["a later session on the same target", "a retry: the same ticket and inputs",
            "feedback inside the same goal: a step in the open pass"]
    new = ["new inputs, data, goal or close rule", "a new target: another sNN, another qNN",
           "a wet Run repeated: a replication (proposed, s06-D02)"]
    for k, (a, b) in enumerate(zip(same, new)):
        say(0, y + k * 36, a, BODY)
        say(860, y + k * 36, b, BODY, L.RED if "proposed" in b else L.INK)
    y += 3 * 36 + 40
    say(0, y, "What a pass holds", HEAD)
    y += 46
    y = say(0, y, "hard: its log and runtime.yaml, the receipt the ticket writes", BODY)
    y = say(0, y, "soft: pass.md, the ask, the summary and what changed, written by soft_run.py pass", BODY) + 30
    y = say(0, y, wrap("A pass grows while it is open and never changes once closed; the Run's history is its "
                       "passes/. An agent session on a studio topic is a pass of run-draw-<sNN> (s06-D03).", 110),
            BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── ④ the workbench shows it, the skill keeps it ─────────────────────────────────────────────────
def frame_screen(space, version):
    heads, rows, subs, buttons = space
    fr = L.open_frame("Workbench and skill")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    y = heading("④", "The workbench shows it; /haipipe-run keeps it",
                "Buttons start Runs; the Runs Space lists them from run.yaml; the skill writes each card and pass.") + 40
    say(0, y, f"On screen: Block {BLOCK.name.split('_')[0]} › Runs  (read from frame.py)", HEAD)
    y += 50
    x = 0
    for k, s in enumerate(subs):                                  # the third row
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
    y = say(0, y, wrap(f"Runs panel, beside every Space: its buttons copy a prompt and start nothing. "
                       f"Here: {label}, \"{doing}\".", 66), BODY) + 20
    if len(heads) < 7:
        y = say(0, y, wrap(f"? {len(heads)} columns today; s06-D01 proposed seven: run · kind · type · target · "
                           "status · passes · last.", 66), BODY, L.RED) + 6
    y = say(0, y, wrap("? a row opens nothing yet: the Run pop-out (its card and passes) is proposed in s06-D01.", 66),
            BODY, L.RED)
    xr, yr = 960, 140
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
    rect(xr, yr + 480, 780, 180)
    say(xr + 24, yr + 498, "What a Run makes belongs to its button's skill", HEAD)
    by = yr + 544
    for s in ["haipipe-studio draws · haipipe-report writes", "haipipe-task runs a hard Run",
              "haipipe-run keeps only the card and the passes"]:
        by = say(xr + 24, by, s, BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── still open, and the reference ───────────────────────────────────────────────────────────────
def frame_open(runs, space):
    fr = L.open_frame("Still open")
    y = say(0, 0, "Still open", T) + 20
    missing = [r for r, (_c, cl) in runs.items() if not named_close(cl)]
    items = [
        "Wet Runs: a hard Run a person carries out; add a protocol ticket and a signed receipt to haipipe-run? (s06-D02)",
        "A Job holds soft Runs only: where does a batch launch, run-launch-<group>, go?",
        "A hard Run's heavy output: show it on screen, or only its heavy.yaml pointer?",
        "The Runs Space: this level's Runs only, or rolled up from the levels below?",
        "A soft pass: when does it close, and who writes its touched.yaml?",
        "The older layout (runs/<run>.sh beside results/<run>/): when does haipipe-project update move it?",
    ]
    if missing:
        items.append(f"Close rules: {len(missing)} of {len(runs)} Runs in b10 have none. Should soft_run.py new "
                     "refuse a ticket without one?")
    items.append(f"The Runs Space shows {len(space[0])} columns and no pop-out: build s06-D01?")
    for k, item in enumerate(items, 1):
        y = say(0, y, wrap(f"{k}. {item}", 74), BODY, L.RED) + 16
    L.close_frame(fr, pad=60)
    return fr


KINDS = [  # what · hard · soft
    ("name", "rNN_<slug>", "run-<type>-<target>, no date"),
    ("ticket", "rNN_<slug>.sh, or a runner's .yaml", "run-<type>-<target>.md"),
    ("output", "its own result/, generated", "its level's draft/ studio/ reports/ delivery/"),
    ("counts as", "evidence", "work, not evidence"),
    ("where", "a work Task only", "a Block, a Job or a Task"),
    ("receipt", "runtime.yaml, written by the ticket", "pass.md per pass, by soft_run.py"),
    ("new pass", "a retry, the same ticket and inputs", "one more round on the same target"),
    ("new Run", "new inputs, data, goal or close rule", "a new target"),
]
TREES = [
    ("a work Task's runs/", [
        ("tNN_<task>/runs/", ""), ("├── rNN_<slug>/", "hard"), ("│   ├── run.yaml", "the card"),
        ("│   ├── rNN_<slug>.sh", "the ticket"), ("│   ├── config.yaml", "frozen inputs"),
        ("│   ├── result/", "metrics · tables · figures · heavy.yaml"),
        ("│   └── passes/p01-<MMDD>/", "log · runtime.yaml"), ("└── run-<type>-<target>/", "soft"),
        ("    ├── run.yaml", ""), ("    ├── run-<type>-<target>.md", "target · ask · close"),
        ("    └── passes/p01-<MMDD>/", "pass.md")]),
    ("a Block's or a Job's runs/: soft only", [
        ("bNN_<topic>/runs/", ""), ("├── run-draw-<sNN>/", "→ studio/sNN-<topic>/"),
        ("├── run-report-<qNN>/", "→ reports/qNN_<topic>/"), ("└── run-delivery-<target>/", "→ delivery/")]),
    ("the older layout, until haipipe-project update", [
        ("tNN_<task>/", ""), ("├── runs/rNN_<slug>.sh", "the ticket, beside ..."),
        ("└── results/rNN_<slug>/", "... its Result, in another folder")]),
]


def frame_reference():
    fr = L.open_frame("For reference")
    y = say(0, 0, "For reference: hard and soft row by row, and the folders", T) + 6
    y = say(0, y, "from haipipe-run's contract; every row is drawn in ① to ③ above", SUB) + 30
    cx = (0, 200, 680)
    for c, h in zip(cx, ("", "hard", "soft")):
        say(c, y, h, HEAD)
    y += 42
    line([(0, y), (1220, y)], arrow=False)
    y += 12
    for what, hard, soft in KINDS:
        say(cx[0], y, what, BODY)
        say(cx[1], y, hard, BODY)
        say(cx[2], y, soft, BODY)
        y += 40
    line([(0, y), (1220, y)], arrow=False)
    xt, yt = 1340, 120
    for k, (title, rows) in enumerate(TREES):
        x, ty = (xt, yt) if k == 0 else (0 if k == 1 else 700, y + 50)
        say(x, ty, title, HEAD)
        tree(x, ty + 44, rows, gap=420 if k == 0 else 360)
    L.close_frame(fr, pad=60)
    return fr


# ── the story ────────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s06-run-workbench-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    runs, space = block_runs(), runs_space()
    story = [frame_what(runs), frame_kinds(runs), frame_passes(runs), frame_screen(space, skill_version())]
    tall = max(f["height"] for f in story)
    for f in story:                                   # one strip: every chapter the same height
        f["height"] = tall
    below = [frame_open(runs, space), frame_reference(),
             L.tools_frame("In Tools: haipipe-run", ["1_base/project/haipipe-run"],   # its skill and code (JL 261011)
                           [("servers/workbench/frame.py", ["runs_of"]),
                            ("servers/workbench/runs_panel.py", ["run_types", "panel_html", "panel_markup"])],
                           around=["haipipe-task runs a hard Run", "haipipe-studio's run-draw-<sNN> (s02)",
                                   "haipipe-report's run-report-<qNN> (s05)", "each workbench's run table names its types"],
                           note="its skill's folder and code, read from disk (JL)")]
    canvas.grid(L.els, [[f["id"] for f in story], [f["id"] for f in below]], gap=260)

    top = story[0]["y"]
    L.text(0, top - 250, "s06 in one sentence: a Run is one piece of work with a target and an end ①, what it leaves "
                         "makes it hard or soft ②, each round on it is a pass ③, and the workbench lists it while "
                         "/haipipe-run keeps its card ④.", 40)
    L.text(0, top - 180, "Read left to right along the arrows. Below the strip: what is still open, and the full "
                         "hard and soft table with the folders.", BODY)
    for k, what in enumerate(("redrawn as one story that defines the Run first (JL); the 261010 frames are in history/",
                              "renamed s06-run-workbench-skill, was s05-runs; ids s05-D01..D05 now s06-D01..D05 (JL)",
                              "every Run here names its close rule; new_topic.py writes one (s06-D06)")):
        L.els.append(canvas.change_note(0, top - 130 + k * 26, what, TODAY, None, size=18))
    for a, b, word in zip(story, story[1:], ("leaves", "repeats", "shows")):
        ay = a["y"] + 180
        x0, x1 = a["x"] + a["width"] + 20, b["x"] - 20
        line([(x0, ay), (x1, ay)])
        L.els[-1]["strokeWidth"] = 3
        L.text(x0 + 30, ay - 44, word, HEAD)
    kinds, ref = story[1], below[1]
    ax = max(kinds["x"] + 200, ref["x"] + 200)
    line([(ax, kinds["y"] + kinds["height"] + 20), (ax, ref["y"] - 20)], dashed=True)
    L.text(ax + 20, kinds["y"] + kinds["height"] + 90, "row by row", HEAD)
    for e in canvas.off_palette(L.els):
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s06_run_workbench_skill.py")


if __name__ == "__main__":
    main()
