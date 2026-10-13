"""s10 · Update a Block to today's rules: s10-update-block.excalidraw (haipipe-studio).

Two frames. First the screens (JL 261011, on s07, now in s05: "make the UI to be the most salient part"): b00_rawdata's
Studio and Report today, beside the same two after `/wb update`, its proposals dashed until a person ticks
them. Then the seven steps, each beside what it finds on b00 today. Read from disk on every build: the
ladder audit's counts (haipipe-project scripts/ladder.py), b00's studio/, register, reports/, related/,
delivery/, runs/ and board.md's sections. The proposals themselves (s10-D04) are typed: they are what s10
proposes, not what the disk holds. New on 261012 (JL: "I want it work like /wb update-to-date path to the
block").

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s10_update_block.py
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
sys.path.insert(0, str(HERE.parent / "s05-report-workbench-skill"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
import report_groups as RG  # noqa: E402  (s05's Report groups: the SPACE beside Tools, a register, short)
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)
import block_inventory as INV  # noqa: E402  (what a Block's Jobs and Tasks already answer)

INK, RED, MONO = L.INK, L.RED, L.MONO
text, path, base = L.text, L.path, L.base
B00 = "examples-1-data/Proj01-CGM-RawData/work/b00_rawdata"
LADDER = L.TOOLKIT / "skills/1_base/project/haipipe-project/scripts/ladder.py"
# s10-D04, inferred from b00's own Jobs and Tasks (haipipe-studio scripts/block_inventory.py; JL 261012: "I don't
# ask the questions that is meaningless ... closely related to the jobs and tasks"): filled from the reading
TOPICS, QUESTIONS = [], []
STEPS = [("1 shape", "haipipe-project ladder.py", "shape"), ("2 today", "the b10 rules as checks", "today"),
         ("3 plan", "a dry run: moves, made, proposed", "plan"), ("4 apply", "--apply: the moves only", "apply"),
         ("5 topics", "haipipe-studio: infer, then new_topic", "topics"),
         ("6 Questions", "haipipe-report: infer; haipipe-question", "qs"),
         ("7 open", "the workbench; run-update-<bNN>", "open")]



def button(x, y, label, size=20, kind="", h=None):
    """A button sized to its words; kind: on (selected), picked, fixed (a double line), new (dashed), red. Kept here
    from s07's 261011 builder (now s05's history/report_groups-261011.py), whose screens this frame still draws."""
    w, h = len(label) * size * 0.56 + 28, h or size + 20
    color = RED if kind == "red" else INK
    base("rectangle", x, y, w, h, color, 3.5 if kind in ("on", "picked") else 1.5, dashed=kind == "new", rough=0)
    if kind == "fixed":
        base("rectangle", x + 4, y + 4, w - 8, h - 8, INK, 1, rough=0)
    text(x + 14, y + (h - size * 1.25) / 2, label, size, color)
    return x + w


def screen(x, y, w, top, bar, views=(), state="", rows=(), today=False, work=True):
    """One workbench screen with the Report open: its top row, its work row, the rows that stay above (views),
    the group bar drawn largest (bar: lines of (label, kind)), then Question │ Work │ Report rows. Returns where
    each bar line and view row ends."""
    at = {"views": [], "bar": []}
    text(x + 24, y + 18, top, 20)
    bx = x + 24
    for lab in ("Description", "Report", "Work", "Runs") if work else ():    # the Studio hides the work row
        bx = button(bx, y + 56, lab, 20, "on" if lab == "Report" else "") + 12
    yy = y + (118 if work else 60)
    for name, items in views:
        text(x + 24, yy + 8, name, 20)
        bx = x + 24 + len(name) * 11 + 16
        for lab, kind in items:
            bx = button(bx, yy, lab, 20, kind) + 8
        at["views"].append((bx, yy))
        yy += 54
    for line in bar:
        bx = x + 24
        for lab, kind in line:
            bx = button(bx, yy, lab, 20 if today else 23, kind, 42 if today else 50) + 10
            if kind == "fixed":
                at.setdefault("fixed", (bx, yy))
        at["bar"].append((bx, yy))
        yy += 54 if today else 64
    if state:
        text(x + 24, yy + 4, state, 20)
        yy += 44
    for left, work_, right, standing in rows:
        base("rectangle", x + 24, yy, w - 48, 62, INK, 1, rough=0)
        text(x + 40, yy + 18, left, 20)
        text(x + 24 + (w - 48) * 0.50, yy + 18, work_, 20)
        text(x + 24 + (w - 48) * 0.72, yy + 18, right, 20)
        if standing:
            at["standing"] = (x + w - 20, yy + 10)
        yy += 72
    base("rectangle", x, y, w, yy - y + 10, INK, 2, rough=0)
    return at

def note(x, y, what):
    e = canvas.change_note(x, y, what, "261012", L.FRAME[0], 17)
    e["id"] = f"v{len(L.els)}"
    L.els.append(e)


def inferred(b):
    """b00's topics and Questions from its reading: each names the Tasks behind it (s10-D04, D05)."""
    r = INV.read_block(b)
    s = INV.summarize(r)
    k, q = s["kinds"], s["subquestions"]
    ready = q.get("source · Is the dataset ready for Source?", {}).get("gist", {})
    blocked = sorted({w.split("/")[0].split("_")[0] for w in ready.get("blocked", [])})
    lack = q.get("intake · Which tables of the family does it lack?", {}).get("gist", {})
    watch = q.get("profile · What should Source watch out for?", {}).get("gist", {})
    nos = {re.search(r"· (no [a-z ]+):", x).group(1): int(re.search(r": (\d+) Tasks", x).group(1))
           for x in s["stands_out"] if x.startswith("profile Openings")}
    fam = s["splits"].get("raw-family", {})
    TOPICS[:] = [("s01-table-profile", f"{k['profile']['tasks']} profile Tasks", "Profile"),
                 ("s02-raw-families", f"raw-family: {len(fam)} values", "Families"),
                 ("s03-source-handoff", f"{k['source']['tasks']} source Tasks", "Handoff"),
                 ("s04-drop-intake", f"{k['intake']['tasks']} intake Tasks", "Intake")]
    QUESTIONS[:] = [("Q01", f"Why are {', '.join(blocked)} blocked from Source?", f"{len(blocked)} source Tasks", "Handoff"),
                    ("Q02", f"Which tables lack an event time ({nos.get('no event time', 0)}) or a person column "
                            f"({nos.get('no person column', 0)})?", "their profile Tasks", "Profile"),
                    ("Q03", "What must Source handle, family by family?",
                     f"{len(watch.get('some', []))} profile Tasks", "Families"),
                    ("Q04", "Which drops lack tables of their family?", f"{len(lack.get('some', []))} intake Tasks",
                     "Intake")]
    return s


def b00_facts():
    """What b00 holds today, and the ladder audit's counts, read on every build."""
    b = (RG.SPACE / B00) if RG.SPACE else None
    if b is None or not b.is_dir():
        return None
    out = subprocess.run([sys.executable, str(LADDER), "audit", str(b), "--summary"], capture_output=True, text=True)
    counts = {m[0]: (int(m[1]), int(m[2])) for m in re.findall(r"(?m)^(\w+)\s+(\d+)\s+ok\s+(\d+)", out.stdout)}
    face = (b / "board.md").read_text(encoding="utf-8")
    sections = re.findall(r"(?m)^## (.+)$", face)
    jobs = sorted(d for d in b.glob("j[0-9]*_*") if d.is_dir())
    inferred(b)
    return {"name": b.name, "counts": counts, "sections": sections, "studio": sorted(p.name for p in (b / "studio").iterdir()),
            "register": len(RG.register_of(b)), "reports": sum(1 for _ in b.rglob("reports")),
            "shelves": {s: (b / s).is_dir() for s in ("related", "delivery", "runs")}, "jobs": len(jobs),
            "kind": (re.search(r"(?m)^board-kind:\s*(\S+)", face) or [None, "?"])[1]}


def ui_frame(f):
    fr = L.open_frame("b00 before and after /wb update")
    canvas.ui_frame(fr, since="261012")                      # a screen: the workbench's colours (JL 261012)
    text(0, 0, "/wb update <block>: an old Block comes out with its topics and its Questions, in its theme's words", 40)
    text(0, 62, f"{f['name']} ({f['kind']}): its Studio and its Report today, and after the update. Dashed: proposed, "
                "a person ticks to keep (s10-D03).", 22)
    note(0, 104, "new: the screens first (JL)")
    top = "Guide · Studio  |  Block · Job ▾ · Task ▾  |  Delivery"
    stop = "Guide · [Studio]  |  Block · Job ▾ · Task ▾  |  Delivery"       # Studio picked, no work row
    # ── Studio, today and after ──
    text(0, 150, "TODAY  the Studio", 25)
    screen(0, 196, 820, stop, [[("Current 0", ""), ("+ Group", "new")]],
              rows=[(f"studio/{n}", "a data file, not a topic", "", False) for n in f["studio"]], today=True,
              work=False)
    text(0, 410, "no sNN topic: the drops' table sits where topics go", 21, RED)
    path([(840, 330), (920, 330)], color=INK)
    L.els[-1]["strokeWidth"] = 4
    text(940, 150, "AFTER  the Studio: four topics, one per kind of work its Tasks do (step 5)", 25)
    note(1900, 156, "inferred from the Tasks, not a generic list (JL)")
    groups = {}
    for _, _, g in TOPICS:
        groups[g] = groups.get(g, 0) + 1
    screen(940, 196, 1620, stop, [[("Current 0", "")] + [(f"{g} {n}", "new") for g, n in groups.items()]
                                     + [("+ Group", "new")]],
              rows=[(t, src, f"proposed  ☐ keep  [{g}]", False) for t, src, g in TOPICS], work=False)
    # ── Report, today and after ──
    y2 = 760
    text(0, y2, "TODAY  the Report", 25)
    screen(0, y2 + 46, 820, top, [], rows=[("No Questions at this level yet.", "", "", False)], today=True)
    text(0, y2 + 330, f"{f['register']} Questions, {f['reports']} reports/ at any level", 21, RED)
    path([(840, y2 + 180), (920, y2 + 180)], color=INK)
    L.els[-1]["strokeWidth"] = 4
    text(940, y2, "AFTER  the Report: where the Jobs' answers differ (step 6, haipipe-report)", 25)
    note(1900, y2 + 6, "each answered by named Tasks (JL)")
    kinds = {}
    for _, _, _, k in QUESTIONS:
        kinds[k] = kinds.get(k, 0) + 1
    screen(940, y2 + 46, 1620, top, [[("Current 0", "")] + [(f"{k} {n}", "new") for k, n in kinds.items()]
                                        + [("+ Group", "new")]],
              rows=[(f"{q}  {RG.short(t, 64)}", by, f"proposed  [{k}]", False) for q, t, by, k in QUESTIONS])
    L.close_frame(fr)
    return fr


def steps_frame(f):
    fr = L.open_frame("The seven steps, read on b00")
    text(0, 0, "The seven steps of /wb update, each beside what it finds on b00 today", 34)
    text(0, 52, "Each a dry run until --apply; each done by the skill that owns that part (s10-D01).", 21)
    c = f["counts"]
    found = {
        "shape": (", ".join(f"{lv} {n}" for lv, (n, _) in c.items()) + ": all ok" if c and all(n == ok for n, ok in c.values())
                  else "see the audit", False),
        "today": (f"studio/ holds {len(f['studio'])} file, no topic · {f['register']} Questions · {f['reports']} reports/ · "
                  + " · ".join(f"no {s}/" for s, there in f["shelves"].items() if not there), True),
        "plan": (f"move studio/raw-drop-manifest.tsv beside family_catalog.yaml; propose {len(TOPICS)} topics, "
                 f"{len(QUESTIONS)} Block Questions, one per Job", False),
        "apply": ("one move; no word of board.md or a face rewritten", False),
        "topics": ("block_inventory.py: one topic per recurring kind of Task, one per split (infer-topics.md)", False),
        "qs": (f"where the {f['jobs']} Jobs' answers differ; each Job asks its source Task's (infer-reports.md)", False),
        "open": ("the Block's workbench, the pass of run-update-b00 listing what to tick", False)}
    for i, (step, who, key) in enumerate(STEPS):
        y = 130 + i * 74
        base("rectangle", 0, y, 360, 56, INK, 1.5, rough=0)
        text(18, y + 14, step, 23)
        text(390, y + 4, who, 20, INK, MONO)
        what, bad = found[key]
        text(390, y + 32, what, 20, RED if bad else INK)
        if i:
            path([(180, y - 18), (180, y)], color=INK)
    yy = 130 + len(STEPS) * 74 + 20
    text(0, yy, "the work decides steps 5 and 6; the theme only names the groups they fall in (s10-D02)", 21)
    note(900, yy + 6, "revised: the work decides, not the theme (JL)")
    for i, q in enumerate(["? the door: /wb update, with haipipe-project as the engine (Open 1)",
                           "? step 2's checks join ladder.md's rules, or a list beside it (Open 2)",
                           "? a whole Project at once, or one Block first (Open 3)"]):
        text(0, yy + 44 + i * 32, q, 20, RED)
    L.close_frame(fr)
    return fr


def main():
    out = HERE / "s10-update-block.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    f = b00_facts()
    if f is None:
        fr = L.open_frame("b00 before and after /wb update")
        text(0, 0, "? b00_rawdata is not on this computer (the WellDoc SPACE beside Tools)", 25, RED)
        L.close_frame(fr)
        frames = [[fr["id"]]]
    else:
        frames = [[ui_frame(f)["id"]], [steps_frame(f)["id"]]]
    canvas.grid(L.els, frames)
    for e in canvas.off_palette(L.els):
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s10_update_block.py")


if __name__ == "__main__":
    main()
