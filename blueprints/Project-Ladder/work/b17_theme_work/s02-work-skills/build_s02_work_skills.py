"""b17-s02:theme_work @ work_skills, its drawing: haipipe-studio's five parts (scripts/five_parts.py, five_parts.build),
as j03's work_ui_cells.py and b16-s01 draw theirs. s02 hands over workbench-work, rewritten for the focus page's three
work pages (JL 261031, pointing at skills/2_theme/work: "you should update this, right?").

Its Design draws the idea itself: A, the skill's new SKILL.md as proposed, its sections in order, the three page
sections as a 3 x 3 of the cells they come from, each cell's form state read from its run.yaml; then its
ref/workbench-table.md in table-workbench's eight columns. B, what A leans on: today's SKILL.md, its headings read from
disk, each with where it goes; the skills and topics the text follows; and the one red open question. The words are the
face's Design block (`outline:`); "what s02 hands over" is delivery/render.yaml, so it names the skill files
(s02-D05). Rebuild: python build_s02_work_skills.py
"""
import re
import sys
import textwrap
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

BLOCK = HERE.parent                                   # b17_theme_work
JOB = BLOCK / "j02_workbench_work_skill"              # the Job that makes s02's delivery
J03 = BLOCK / "j03_work_workbench_pages"              # the nine cells and their forms
FACE = HERE / f"{HERE.name}.md"
SECTIONS = ("Report", "Work", "Studio")
VERB = {"Report": "check", "Work": "do", "Studio": "think"}
WAITING = "#fff4e6"


def outline() -> dict:
    """The face's Design block: the skill's new outline, the words the drawing lays out."""
    m = re.search(r"(?ms)^Design\n-+\n.*?```yaml\n(.*?)^```", FACE.read_text(encoding="utf-8"))
    return yaml.safe_load(m.group(1))["outline"]


def card_of(path: Path) -> dict:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.is_file() else {}


def parts() -> list:
    """What s02 hands over, from delivery/render.yaml: each piece's file and what it is, done once its Run is done."""
    pieces = card_of(HERE / "delivery" / "render.yaml").get("pieces") or []
    out = []
    for pc in pieces:
        _, _, rest = pc["code"].partition(": ")
        file, _, what = rest.partition(", ")
        out.append(("code", file, what, card_of(BLOCK / pc["by"] / "run.yaml").get("status") == "done"))
    return out


def form_state(rel: str) -> tuple:
    """A cell's form, read from disk: answered, waiting for you, or not sent yet."""
    run = J03 / rel
    tag = run.name.split("_")[0]
    if (run / "result" / "answer_collection.md").is_file():
        return f"✅ {tag} answered", GR, False
    if card_of(run / "run.yaml").get("status") == "waiting":
        return f"\U0001f64b {tag} waits for you", OR, True
    return f"⬜ {tag} not sent yet", ROOM, False


def skill_now(skill: Path) -> tuple:
    """Today's SKILL.md: its version and its section titles, read from disk on every build."""
    text_ = skill.read_text(encoding="utf-8")
    v = re.search(r'(?m)^\s*version:\s*"?([\d.]+)', text_)
    return (v.group(1) if v else "?"), headings(skill)


def badge(eid, x, y, n):
    return [_el("rectangle", eid, x, y, 26, 24, NAVY, "#ffffff", roundness={"type": 3})] + \
        text(eid + "_n", x + 13, y + 3, str(n), 14, NAVY, "center")


def pill(eid, x, y, words, color=PU, fill="#f3f0ff"):
    w = len(words) * 12 * 0.62 + 18
    return [_el("rectangle", eid, x - w, y, w, 22, color, fill, roundness={"type": 3})] + \
        text(eid + "_t", x - w + 9, y + 3, words, 12, color)


def section_row(eid, x, y, w, n, sec):
    """A section of the SKILL.md that is not a page: its number, its name, where it comes from, what it says."""
    els = badge(eid + "_b", x, y + 2, n) + text(eid + "_n", x + 38, y + 2, sec["name"], 16, NAVY)
    els += pill(eid + "_f", x + w, y + 2, "← " + sec["from"])
    return els + text(eid + "_s", x + 38, y + 26, textwrap.shorten(sec["says"], 104, placeholder="…"), 12, BODY)


def page_row(eid, x, y, w, n, sec, cells):
    """A page's section: its name and Task on the left, then its Report, Work and Studio, a cell each."""
    els = badge(eid + "_b", x, y + 4, n) + text(eid + "_n", x + 34, y + 2, sec["name"], 15, NAVY)
    els += text(eid + "_t", x + 34, y + 24, "j03 · " + sec["task"], 11, BODY)
    cx, cw, h = x + 168, (w - 168 - 20) / 3, 94
    for k, cid in enumerate(sec["cells"]):
        cell = cells[cid]
        words, color, waits = form_state(cell["form"])
        bx = cx + k * (cw + 10)
        els += [_el("rectangle", f"{eid}_c{k}", bx, y, cw, h, OR if waits else ROOM, WAITING if waits else "#ffffff",
                    roundness={"type": 3})]
        els += text(f"{eid}_c{k}_h", bx + 10, y + 8, f"{cid} · {cell['section']}", 14, TITLE)
        said = "\n".join(textwrap.wrap(cell["says"], 27)[:2])
        els += text(f"{eid}_c{k}_s", bx + 10, y + 30, said, 12, INK)
        els += text(f"{eid}_c{k}_f", bx + 10, y + 70, words, 12, color)
    return els, y + h


def notes(eid, x, y, items):
    """Small labelled lines: (title, words), a page icon each."""
    els = []
    for k, (t, w) in enumerate(items):
        yy = y + 64 * k
        els += i_page(f"{eid}{k}", x, yy) + text(f"{eid}{k}_n", x + 58, yy - 2, t, 15, TITLE)
        els += text(f"{eid}{k}_w", x + 58, yy + 22, w, 13, BODY)
    return els


def sketch_a(o, x, y, w=860):
    """A · the SKILL.md as proposed, then its ref."""
    els, n = [], 0
    els += text("A_t", x, y, "A · workbench-work's SKILL.md, as proposed", 18, TITLE)
    els += shapes("A_s", x, y + 26, "SKILL.md · ref/workbench-table.md, one section per page")
    top, row = y + 60, y + 60 + 58
    body = []
    body += text("A_doc_t", x + 18, top + 12, "/".join(Path(o["skill"]).parts[-2:]), 16, NAVY)
    body += text("A_doc_v", x + w - 250, top + 14, "proposed · one section per page", 13, BODY)
    body += line("A_doc_rule", [(x, top + 44), (x + w, top + 44)], ROOM, 1)
    pages = [s for s in o["sections"] if "cells" in s]
    first_page = o["sections"].index(pages[0])
    for k, sec in enumerate(o["sections"]):
        n += 1
        if "cells" in sec:
            if k == first_page:                                   # the three columns, named once above the pages
                for j, s in enumerate(SECTIONS):
                    cw = (w - 36 - 168 - 20) / 3
                    body += text(f"A_col{j}", x + 18 + 168 + j * (cw + 10) + 10, row, f"{s} · {VERB[s]}", 13, ROOM)
                row += 26
            els_, bottom = page_row(f"A_p{k}", x + 18, row, w - 36, n, sec, o["cells"])
            body += els_
            row = bottom + 14
        else:
            body += section_row(f"A_r{k}", x + 18, row, w - 36, n, sec)
            row += 54
    doc_h = row - top + 8
    els += [_el("rectangle", "A_doc", x, top, w, doc_h, INK, "#ffffff", roundness={"type": 3})] + body
    # its ref, in table-workbench's eight columns, a few rows as proposed
    ref, ry = o["ref"], top + doc_h + 34
    widths = (46, 56, 66, 106, 200, 106, 84, 156)
    tab, bottom = data_table("A_ref", x + 18, ry + 14, "/".join(Path(ref["file"]).parts[-3:]), ref["columns"], widths,
                             ref["rows"], PU, "#f3f0ff", note="one row per page · section · view · Run type")
    tab += text("A_ref_more", x + 18, bottom + 10, "+ a row for every view the SKILL.md names (Run type none when it "
                "starts nothing), checked by --check", 12, BODY)
    els += [_el("rectangle", "A_refdoc", x, ry, w, bottom - ry + 44, INK, "#ffffff", roundness={"type": 3})] + tab
    return els, bottom + 44


def sketch_b(o, x, y, skill, w=560):
    """B · what A leans on: today's SKILL.md and where each of its sections goes; the sources; the open question."""
    version, heads = skill_now(skill)
    els = text("B_t", x, y, "B · what A leans on", 18, TITLE)
    els += shapes("B_s", x, y + 26, "the outline's order, each section's source")
    top = y + 60
    rows = text("B_now_t", x + 16, top + 12, f"today's SKILL.md · v{version}, read from disk", 15, NAVY)
    yy = top + 46
    for k, h in enumerate(heads):
        goes = o["today"].get(h)
        gone = bool(goes) and goes.startswith("gone")
        rows += text(f"B_h{k}", x + 16, yy, textwrap.shorten(h, 52, placeholder="…"), 13, INK)
        rows += text(f"B_h{k}_to", x + 30, yy + 20, ("✕ " if gone else "→ ") + (goes or "? not placed yet"), 12,
                     ROOM if gone else GR if goes else RE)
        yy += 46
    els += [_el("rectangle", "B_now", x, top, w, yy - top + 4, ROOM, "#ffffff", roundness={"type": 3})] + rows
    ny = yy + 50
    els += notes("B_n", x + 6, ny, (
        ("j03's nine cells", "each page's three forms, then the cells' views-proposal.md"),
        ("b17-s04", "what every work page shares: path, rails, the pop-out"),
        ("haipipe-ui", "the page rules: five seconds, one verb per section"),
        ("table-workbench", "the ref's eight columns, and its --check"),
        ("haipipe-interaction · haipipe-run", "the Interaction button; hard and soft Runs, roles")))
    end = ny + 64 * 5
    return els, end


def design():
    o = outline()
    skill = TOOLS / "plugins/haipipe-toolkit" / o["skill"]
    a, a_end = sketch_a(o, 690, 280)
    b, b_end = sketch_b(o, 690 + 860 + 90, 280, skill)
    bx = 690 + 860 + 90
    els = a + b
    grid = 280 + 60 + 58 + 54 * next(i for i, s in enumerate(o["sections"]) if "cells" in s) + 26 + 47   # Block page row
    els += arrow("AB_cells", [(bx - 6, b_end - 64 * 5 + 10), (690 + 860 + 8, grid)], PU, width=2)
    return els + sticky("askD", bx + 280, b_end + 70, 470, 84,
                        "? one section per page (Block · Job · Task),\nor one per section (Report · Work · Studio)",
                        16, -0.03, RED, RE)


SPEC = {
    "title": "Work skills: workbench-work, rewritten for the work pages",
    "why": {"question": "why do we need s02?",
            "notes": ["the skill still teaches\nScope · Task · Check\n· Delivery",
                      "its Questions and the\nquestion map are gone", "nine cells now design\nthe Block, Job and\nTask pages"],
            "quote": 'JL 261031, at skills/2_theme/work: "you should update this, right?"'},
    "what": {"head": "② what s02 hands over: one skill, rewritten", "icon": "book", "name": "workbench-work",
             "type": "skill", "deck_why": "stays in s02's delivery/deck/, so anyone gets it in a minute", "parts": parts()},
    "job": JOB,
    "target": "skills/2_theme/work/workbench-work (SKILL.md, ref/workbench-table.md)",
    "missing": [],
}


if __name__ == "__main__":
    probe = design()                                       # Process and Delivery move right, past the wide Design
    wide = max(e["x"] + e["width"] for e in probe)
    five_parts.build(HERE, SPEC, design, shift=max(1050, int((wide - 690) * GROW + 690 + MOVE - 2210 + 330)))
