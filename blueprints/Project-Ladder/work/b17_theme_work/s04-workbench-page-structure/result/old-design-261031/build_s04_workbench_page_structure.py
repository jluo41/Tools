"""b17-s04:theme_work @ workbench_page_structure, its drawing: the five parts (haipipe-studio scripts/five_parts.py) with
s04's own facts and its Design: one sketch per piece of its delivery, each made by a Task of j03 (JL 261031: "How do you
update the design part based on the new skills we have"). A: the work Block page (t01); B: the same rows at a Job and a
Task (t02); C: one look per element, from the old s32 (t03). The page's names, sections, Jobs and Tasks are read from
disk on every build; the first drawing stays whole below the Design, its screenshot kept."""
import json
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402  (underscore names skip the star import)
import five_parts  # noqa: E402

BLOCK = HERE.parent
WB = TOOLS / "plugins/haipipe-toolkit/servers/workbench"
_fp = (WB / "focus_page.py").read_text(encoding="utf-8")
RAIL = re.findall(r'rail\.append\(\("\w+", "([^"]+)", ""\)\)', _fp)          # the right rail, in its order
JOBS = sorted(BLOCK.glob("j[0-9]*_*"))
J03 = BLOCK / "j03_work_workbench_pages"


def field(face: Path, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.+)$", face.read_text(encoding="utf-8")) if face.is_file() else None
    return m.group(1).strip() if m else ""


def tasks_of(job: Path) -> list:
    """(name, goal, open) for each Task of a Job, from its face."""
    out = []
    for t in sorted(job.glob("t[0-9]*_*")):
        face = t / f"{t.name}.md"
        out.append((t.name, field(face, "goal"), "OPEN" in field(face, "state")))
    return out


SPEC = {
    "title": "Workbench page structure: the work Block, Job and Task pages",
    "why": {"question": "why do we need s04?",
            "notes": ["a page scatters\nwhere, why and result", "Report, Work and Studio\nrepeated in two places",
                      "a Job's goal sits apart\nfrom its status and output"],
            "quote": "JL 261028: path first, one row per item, important content visible"},
    "what": {"head": "② what s04 hands over: the work pages", "icon": "page", "name": "delivery/ui/", "type": "ui",
             "deck_why": "stays in s04's delivery/deck/, so anyone gets it in a minute",
             "parts": [  # (icon, piece: what it is, why, done: its screen draft is in delivery/ui/)
                 ("page", "ui/block-page", "the work Block page: Report, Work, Studio (s51 · s52 · s53)",
                  (HERE / "delivery/ui/block-page").exists()),
                 ("page", "ui/job-page", "the work Job page: Report, Work, Studio (s54 · s55 · s56)",
                  (HERE / "delivery/ui/job-page").exists()),
                 ("page", "ui/task-page", "the work Task page: Report, Work, Studio (s57 · s58 · s59)",
                  (HERE / "delivery/ui/task-page").exists())]},
    "job": J03,
    "target": "servers/workbench/focus_page.py (design_b02_workbench)",
    "missing": [(f"ui/{n}", "the agreed screen draft, not drawn yet") for n in ("block-page", "job-page", "task-page")
                if not (HERE / "delivery/ui" / n).exists()],
}


def window(eid, x, y, w, h, url):
    """A browser window, drawn plainly: a frame and its address bar."""
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def rails(eid, x, y, right, here_right, left, here_left, rx):
    """The two quiet rails: short bars, the page here in orange; their names show on hover (s04 agreed)."""
    els = []
    for k, name in enumerate(left):
        on = name == here_left
        els += line(f"{eid}_l{k}", [(x + 8, y + 22 * k), (x + 24, y + 22 * k)], OR if on else ROOM, 3 if on else 1)
    for k, name in enumerate(right):
        on = name == here_right
        els += line(f"{eid}_r{k}", [(rx, y + 22 * k), (rx + 16, y + 22 * k)], OR if on else ROOM, 3 if on else 1)
    return els


def row(eid, x, y, w, name, goal, status, output, warn=False):
    """One item, one full-width row: its name and goal, then status, then output, read left to right."""
    els = [_el("rectangle", eid, x, y, w, 58, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_n", x + 12, y + 8, name, 14, TITLE)
    els += text(eid + "_g", x + 12, y + 32, textwrap.shorten(goal, int((w - 260) / 7), placeholder="…"), 11, BODY)
    sx = x + w - 230
    els += [_el("rectangle", eid + "_s", sx, y + 16, 92, 24, RE if warn else ROOM, "#fff5f5" if warn else "#f1f3f5",
                roundness={"type": 3})] + text(eid + "_s_t", sx + 8, y + 20, status, 12, RE if warn else INK)
    els += text(eid + "_o", sx + 104, y + 20, output, 12, GR)
    return els


def design():
    els = []
    #   A: the work Block page (j03 t01): path, name and section, the section's views, purpose, one row per Job
    els += text("skA", 690, 280, "A · the work Block page", 18, TITLE)
    els += shapes("skA_s", 690, 306, "delivery/ui/block-page  (j03 t01)")
    els += window("wA", 690, 340, 660, 520, "…/_board/workbench?path=…/b17_theme_work&layout=focus&section=work")
    els += text("wA_crumb", 740, 382, "Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work", 11, BODY)
    els += text("wA_t", 740, 402, BLOCK.name, 22, INK) + text("wA_sec", 930, 408, "Work", 18, ROOM)
    for k, v in enumerate(("Progress", "Results")):
        els += [_el("rectangle", f"wA_v{k}", 740 + 92 * k, 442, 84, 24, OR if k == 0 else ROOM,
                    "#fff4e6" if k == 0 else "#ffffff", roundness={"type": 3})] + text(f"wA_v{k}_t", 752 + 92 * k, 446, v, 12, INK)
    els += text("wA_p_h", 740, 482, "PURPOSE", 10, ROOM)
    els += text("wA_p", 740, 498, textwrap.shorten(field(BLOCK / "board.md", "spine"), 84, placeholder="…"), 11, INK)
    for k, j in enumerate(JOBS):
        ts = tasks_of(j)
        n_open = sum(1 for _, _, o in ts if o)
        els += row(f"wA_j{k}", 740, 536 + 70 * k, 570, j.name, field(j / f"{j.name}.md", "goal"),
                   f"{n_open} of {len(ts)} open", "▸ " + {"j01": "s01 skill", "j02": "s02 skill", "j03": "s04 ui"}.get(j.name[:3], ""))
    blocks = sorted(p.name for p in BLOCK.parent.iterdir() if p.is_dir() and re.match(r"b\d+_", p.name))
    els += rails("wA_rail", 690, 560, RAIL, "Work", blocks, BLOCK.name, 1330)
    els += text("wA_n", 690, 872, f"left: {len(blocks)} sibling Blocks · right: {' · '.join(RAIL)}  (names on hover)", 13, BODY)
    els += sticky("ask_below", 1210, 960, 300, 64, "? what sits right under\nthe purpose: views or rows", 15, -0.03, RED, RE)

    #   B: the same rows one level down (j03 t02): a Job's Tasks, and a Task's Runs
    XB = 1460
    els += text("skB", XB, 280, "B · the same rows at a Job and a Task", 18, TITLE)
    els += shapes("skB_s", XB, 306, "delivery/ui/job-task-pages  (j03 t02, Phase A)")
    els += window("wB", XB, 340, 640, 300, f"…&path=…/{J03.name}")
    els += text("wB_t", XB + 30, 384, J03.name, 18, INK) + text("wB_sec", XB + 290, 388, "Work", 15, ROOM)
    for k, (tn, goal, o) in enumerate(tasks_of(J03)):
        els += row(f"wB_t{k}", XB + 30, 420 + 68 * k, 580, tn, goal, "open" if o else "closed", "▸ delivery/ui/")
    t01 = J03 / "t01_block_page"
    els += window("wC", XB, 670, 640, 190, f"…&path=…/{J03.name}/{t01.name}")
    els += text("wC_t", XB + 30, 714, t01.name, 18, INK) + text("wC_sec", XB + 200, 718, "Work", 15, ROOM)
    for k, card in enumerate(sorted(t01.glob("runs/*/run.yaml"))):
        st = re.search(r"(?m)^status:\s*(\w+)", card.read_text()).group(1)
        els += row(f"wC_r{k}", XB + 30, 750 + 68 * k, 580, card.parent.name, "the screen draft of the Block page",
                   st, "▸ result/", warn=False)
    els += text("wB_n", XB, 872, "each row: goal ▸ status ▸ output, the same at every level", 13, BODY)
    els += sticky("ask_accept", XB + 380, 960, 300, 64, "? run finished is not goal\naccepted: who marks it", 15, 0.03, RED, RE)

    #   C: one look per element (j03 t03), from the old s32 gallery: an item is one row of four parts
    YC = 1100
    els += text("skC", 690, YC, "C · one look per element: an item is one row", 18, TITLE)
    els += shapes("skC_s", 690, YC + 26, "delivery/ui/element-picks  (j03 t03, from the old s32)")
    els += row("pC", 690, YC + 80, 660, "j01_work_ladder_contract", field(JOBS[0] / f"{JOBS[0].name}.md", "goal"),
               "3 of 3 open", "▸ s01 skill")
    for k, (x, words) in enumerate(((700, "1 its name\nwith its address"), (900, "2 one line:\nwhat it is for"),
                                    (1100, "3 where it stands,\nin words"), (1262, "4 its output\nor picture"))):
        els += arrow(f"pC_a{k}", [(x + 40, YC + 200), (x + 40, YC + 145)], OR, width=2)
        els += text(f"pC_w{k}", x, YC + 208, words, 13, INK)
    els += text("pC_note", 690, YC + 270, "lists, tables and cards all become this row (s32 leaning: never a grid)", 13, BODY)
    els += sticky("ask_run", 1210, YC + 320, 300, 64, "? a Run: the same row,\nor only a pop-out", 15, -0.02, RED, RE)

    #   D: where the old s03 and s32 went, so the merge reads on the drawing
    XD = 1460
    els += text("skD", XD, YC, "D · merged into s04 on 261031", 18, TITLE)
    els += shapes("skD_s", XD, YC + 26, "kept whole in result/merged-*/")
    for k, (nm, what) in enumerate((("s03-work-workbench", "today's workbench: the before picture"),
                                    ("s32-work-element-ui", "every element as drawn today, 96 versions"))):
        y = YC + 80 + 74 * k
        els += i_page(f"mD{k}", XD, y) + text(f"mD{k}_n", XD + 50, y - 2, f"result/merged-{nm}/", 15, TITLE)
        els += text(f"mD{k}_w", XD + 50, y + 22, what, 13, BODY)
    return els


def keep_files(out: Path, *sources: Path) -> None:
    """five_parts writes no images; carry the kept drawing's embedded pictures over, so its screenshot still shows."""
    d = json.loads(out.read_text(encoding="utf-8"))
    for src in sources:
        if src.is_file():
            d["files"].update(json.loads(src.read_text(encoding="utf-8")).get("files", {}))
    out.write_text(json.dumps(d, ensure_ascii=False) + "\n", encoding="utf-8")


def smaller(els, x0, y0, s=0.4):
    """The kept first drawing at 40% size: the viewer fits the whole canvas but never below 10% zoom, so a full-size
    old drawing (about 8,000 px tall) opened on its own frames and hid the five parts above it (261031)."""
    for e in els:
        if not e["id"].startswith("kept_") or e["id"] in ("kept_h", "kept_rule"):
            continue
        e["x"], e["y"] = x0 + (e["x"] - x0) * s, y0 + (e["y"] - y0) * s
        e["width"], e["height"] = e["width"] * s, e["height"] * s
        if "fontSize" in e:
            e["fontSize"] = max(1, round(e["fontSize"] * s))
        if "points" in e:
            e["points"] = [[px * s, py * s] for px, py in e["points"]]
    return els


if __name__ == "__main__":
    def with_kept():
        els = design()
        top = max(e["y"] + e["height"] for e in els) + 120
        return els + smaller(kept_first(HERE, top), 690, top + 70)
    out = five_parts.build(HERE, SPEC, with_kept)
    keep_files(out, HERE / "result" / "first-drawing.excalidraw")
