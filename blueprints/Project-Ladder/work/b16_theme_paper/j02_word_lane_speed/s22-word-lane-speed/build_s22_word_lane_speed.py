"""b16.j02-s22:theme_paper.word_lane_speed @ word_lane_speed, its drawing: haipipe-studio's five parts. Its Design:
A, where the 28 minutes goes, drawn from the measured calls; B, what the fallback does to a page; C, the five ways to go
faster, the open question in red. Numbers are the ones the face records (261104).

    python build_s22_word_lane_speed.py      writes the .excalidraw and its card, the .png
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

SPEC = {
    "title": "Word lane speed: is Word slow, or stuck?",
    "why": {"question": "why do we need s22?",
            "notes": ["one sentence:\nhalf an hour\nto see Word", "LaTeX: 30 s\nWord stage:\n28 minutes", "asked three\ntimes how long\nit would take"],
            "quote": 'JL 261104: "I think the speed here is a issue,\nplease document it well"'},
    "what": {"head": "② what s22 hands over: faster Word code", "icon": "code", "name": "the Word lane", "type": "code",
             "deck_why": "stays in s22's delivery/deck/, so anyone gets it in a minute",
             "parts": [("code", "latex_room_to_docx.py", "measure, queue, draft mode", False),
                       ("code", "build_delivery.py", "the flags, the report", False)]},
    "job": HERE.parent,
    "target": "haipipe-paper-assemble scripts/",
    "missing": [],
}


def bar(eid, x, y, w, h, stroke, fill, words, size=15):
    return [_el("rectangle", eid, x, y, w, h, stroke, fill)] + text(eid + "_t", x + w / 2, y + h / 2 - size * 0.62, words, size, INK, "center")


def page(eid, x, y, label, top, color):
    els = [_el("rectangle", eid, x, y, 150, 190, INK, "#ffffff")]
    yy = y + 14
    if top:
        els += bar(eid + "_d", x + 12, yy, 126, 62, color, "#ebfbee" if top == "ok" else "#fff5f5", "Table 1", 15)
        yy += 74
    for k in range(5 if top else 3):
        els += line(f"{eid}_l{k}", [(x + 14, yy + k * 16), (x + 136, yy + k * 16)], ROOM, 1)
    if not top:
        yy += 56
        els += bar(eid + "_d", x + 12, yy, 126, 62, color, "#fff5f5", "Table 1", 15)
    return els + text(eid + "_c", x + 75, y + 200, label, 15, color, "center")


def design():
    x0, y = 690, 280
    els = text("a_h", x0, y, "A · where the 28 minutes goes", 26, TITLE)
    els += bar("a_latex", x0, y + 50, 40, 44, GR, "#ebfbee", "", 13) + text("a_latex_lbl", x0, y + 102, "LaTeX\n30 s", 15, GR)
    for k in range(14):
        els += bar(f"a_{k}", x0 + 60 + k * 66, y + 50, 62, 44, RE, "#fff5f5", "2 min", 14)
    els += text("a_each", x0 + 60, y + 102, "14 displays, each waits out AppleScript's 120-second timeout, then falls back", 18, RE)
    els += text("a_lock", x0 + 60, y + 134, "Word's main thread: on a lock, 0% CPU, 2561 of 2561 samples", 18, INK)
    els += bar("a_ok", x0 + 60, y + 170, 62, 44, GR, "#ebfbee", "40-80 s", 14)
    els += text("a_q", x0 + 136, y + 180, "the whole build on a working Word: 14 displays, at page tops", 20, GR)
    y2 = y + 270
    els += text("b_h", x0, y2, "B · what the 28 minutes bought", 26, TITLE)
    els += page("b_want", x0, y2 + 50, "wanted: top of the page", "ok", GR) + page("b_got", x0 + 220, y2 + 50, "got: after its paragraph", "", RE)
    els += text("b_n", x0 + 440, y2 + 80, "Word tab said \"as Word prints it\"", 19, INK)
    els += text("b_n2", x0 + 440, y2 + 112, "pdfinfo: LibreOffice", 19, RE)
    els += text("b_n3", x0 + 440, y2 + 160, "✎ 261104 now found in 30 s and said", 17, GR)
    y3 = y2 + 300
    els += text("c_h", x0, y3, "C · five ways to go faster", 26, TITLE)
    rows = [("a Word queue", "builds take turns; may prevent the hang", "✎ built, 261104"),
            ("a draft that skips measuring", "fast; displays after their paragraph", "saves seconds now"),
            ("one Word session", "repaginate once, keep it open", "saves seconds now"),
            ("reuse the last placement", "when no text before it changed", "saves seconds now"),
            ("ask Word for the next page", "one call, not about 17", "saves about 3 s a display")]
    for k, (name, why, when) in enumerate(rows):
        yy = y3 + 50 + k * 58
        els += bar(f"c_{k}", x0 + k * 34, yy, 300, 44, TITLE, "#fff3bf" if k == 0 else "#ffffff", name, 17)
        els += text(f"c_{k}_w", x0 + k * 34 + 316, yy + 4, why, 16, INK) + text(f"c_{k}_n", x0 + k * 34 + 316, yy + 24, when, 14, BODY)
    return els


if __name__ == "__main__":
    wide = max(e["x"] + e["width"] for e in design())
    shift = max(1050, int((wide - 690) * five_parts.GROW + 690 + five_parts.MOVE - 2020 + 120))
    five_parts.build(HERE, SPEC, design, shift)
