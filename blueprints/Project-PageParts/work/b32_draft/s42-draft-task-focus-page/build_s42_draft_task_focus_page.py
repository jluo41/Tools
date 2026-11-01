"""b32-s42:draft @ draft_task_focus_page, its drawing: haipipe-studio's five parts (scripts/five_parts.py), as b17-s04.
Its Design is one sketch per piece of what it hands over, the draft Task page on the focus page, live on 5599: A Work,
one step in one shape; B Report's Text, sentences beside their cards; C Report's MindMap, the paper's content; D where
the old page's pieces went. Each sketch carries its open question in red (the same as the collection Run
r01_collect_draft_task_page). The step names are read from draft_steps.STEPS; the code's state from disk."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

DRAFT = TOOLS / "plugins/haipipe-toolkit/servers/workbench/workbench-task-draft"
_ds = (DRAFT / "draft_steps.py").read_text(encoding="utf-8")
STEPS = [s for s in re.search(r"^STEPS = \((.*?)\)$", _ds, re.M).group(1).replace('"', "").split(", ") if s[:1].isdigit()]
CODE = DRAFT / "focus_draft.py"

SPEC = {
    "title": "The draft Task page: a Section, written step by step, on the focus page",
    "why": {"question": "why do we need s42?",
            "notes": ["the old steps showed as\npages in an iframe", "Findings said No\ntakeaways recorded", "Studio and Delivery\nsat as Work buttons"],
            "quote": "JL 261031: we are working on the draft here ourself"},
    "what": {"head": "② what s42 hands over: the draft Task page", "icon": "code", "name": "focus_draft.py", "type": "ui",
             "deck_why": "stays in s42's delivery/deck/, so anyone gets it in a minute",
             "parts": [("code", "workbench-task-draft/focus_draft.py", "Report, Work, Studio, Delivery of a draft Task", CODE.is_file()),
                       ("page", "ui/work-step", "one step, one shape", True),
                       ("page", "ui/report-text", "sentences beside their cards", True)]},
    "job": None,
    "target": "servers/workbench/focus_page.py (one marked HOOK) · workbench-task-draft/focus_draft.py",
    "missing": [],
}


def window(eid, x, y, w, h, url):
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def buttons(eid, x, y, names, words, on=0):
    els, cx = [], x
    for k, n in enumerate(names):
        label = f"{n} {words[k]}" if k < len(words) and words[k] else n
        w = 12 + 7 * len(label)
        els += [_el("rectangle", f"{eid}{k}", cx, y, w, 24, OR if k == on else ROOM, "#fff4e6" if k == on else "#ffffff",
                    roundness={"type": 3})] + text(f"{eid}{k}_t", cx + 6, y + 5, label, 11, INK)
        cx += w + 8
    return els


def bar(eid, x, y, w, words, warn=False):
    return [_el("rectangle", eid, x, y, w, 38, OR if warn else ROOM, "#fff4e6" if warn else "#ffffff",
                roundness={"type": 3})] + text(eid + "_t", x + 14, y + 11, words, 13, INK)


def design():
    els = []
    #   A: Work, one step in one shape
    els += text("skA", 690, 280, "A · Work: one step, one shape", 18, TITLE) + shapes("skA_s", 690, 306, "live on 5599 · focus_draft.step_html")
    els += window("wA", 690, 340, 680, 400, "…&path=…/t00_summary&layout=focus&section=work")
    els += text("wA_t", 730, 382, "t00_summary", 20, INK) + text("wA_s", 880, 386, "Work · do", 15, ROOM)
    els += buttons("bA", 730, 420, [s for s in STEPS] + ["Runs"], ["sign", "done", "next", "none", "next"])
    els += text("wA_aim", 730, 458, "AIM  the Section's reader-question", 12, BODY)
    for k, (w, warn) in enumerate((("Waits for your sign  ·  Open the draft", True), ("▾ Ask the agent  ·  Copy prompt: plan", False),
                                   ("▾ §1 Structure · v0.1", False), ("▾ Scratch · Examples · Contract · Rubric", False),
                                   ("▾ Input · Runs of this step", False))):
        els += bar(f"cA{k}", 730, 486 + 48 * k, 600, w, warn)
    els += sticky("askA", 1080, 790, 300, 70, "? a Sign button, or keep\ntyping ✅ in the draft", 15, -0.03, RED, RE)

    #   B: Report's Text: each sentence beside its cards, read only
    XB = 1480
    els += text("skB", XB, 280, "B · Report › Text: sentence by sentence", 18, TITLE) + shapes("skB_s", XB, 306, "focus_draft.text_html")
    els += window("wB", XB, 340, 640, 400, "…&path=…/t00_summary&layout=focus&section=report")
    els += buttons("bB", XB + 40, 384, ["MindMap", "Text", "Status"], [], on=1)
    for k in range(5):
        y = 440 + 56 * k
        els += text(f"sB{k}", XB + 40, y, f"S{k + 1}", 12, ROOM) + line(f"lB{k}", [(XB + 72, y + 8), (XB + 330, y + 8)], INK, 2) \
            + line(f"mB{k}", [(XB + 72, y + 26), (XB + 280, y + 26)], ROOM, 2)
    for k, (kind, w, c) in enumerate((("Edit · S2", "old → new", OR), ("Evidence · S4", "VALUE 1.1", PU), ("Open · S3", "? to find", RE))):
        y = 470 + 76 * k
        els += [_el("rectangle", f"cB{k}", XB + 370, y, 230, 58, c, "#ffffff", roundness={"type": 3})]
        els += text(f"cB{k}_k", XB + 382, y + 8, kind, 12, c) + text(f"cB{k}_w", XB + 382, y + 30, w, 12, INK)
    els += sticky("askB", XB + 330, 790, 300, 70, "? Ask the agent on top,\nor below the result", 15, 0.03, RED, RE)

    #   C: Report's MindMap: the paper's content
    YC = 920
    els += text("skC", 690, YC, "C · Report › MindMap: the paper's content", 18, TITLE) + shapes("skC_s", 690, YC + 26, "focus_draft.branches")
    els += [_el("rectangle", "mC", 690, YC + 120, 150, 50, INK, "#ffffff", roundness={"type": 3})] + text("mC_t", 704, YC + 136, "t00_summary", 14, INK)
    for k, (p, pts) in enumerate((("C1.P1 Background", ("S1 point ▸ sentence", "S2 point ▸ sentence")),
                                  ("C1.P2 Methods", ("S3 point ▸ sentence",)), ("C1.P3 Findings", ("S7 point ▸ sentence",)))):
        y = YC + 70 + 70 * k
        els += arrow(f"mCa{k}", [(840, YC + 145), (900, y + 18)], ROOM, width=1)
        els += [_el("rectangle", f"mCp{k}", 900, y, 170, 36, INK, "#ffffff", roundness={"type": 3})] + text(f"mCp{k}_t", 910, y + 10, p, 12, INK)
        for j, s in enumerate(pts):
            els += text(f"mCs{k}{j}", 1100, y + 2 + 20 * j, s, 12, BODY)

    #   D: where the old page's pieces went
    els += text("skD", XB, YC, "D · the old page, piece by piece", 18, TITLE) + shapes("skD_s", XB, YC + 26, "Work Details tabs → sections and views")
    for k, (a, b) in enumerate((("Studio · Delivery tabs", "the right-rail"), ("Operation and Result folds", "sections, a heading each"),
                                ("Disk · Runs panel", "Work › Runs, each step's foot"), ("Findings iframe", "Report › Text"))):
        y = YC + 80 + 56 * k
        els += i_page(f"dD{k}", XB, y) + text(f"dD{k}_a", XB + 50, y - 2, a, 15, TITLE) + text(f"dD{k}_b", XB + 50, y + 20, "→ " + b, 13, BODY)
    return els


if __name__ == "__main__":
    five_parts.build(HERE, SPEC, design)
