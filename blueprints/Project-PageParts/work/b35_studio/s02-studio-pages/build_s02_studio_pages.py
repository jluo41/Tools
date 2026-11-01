"""b35-s02:studio @ studio_pages, its drawing: the five parts (haipipe-studio scripts/five_parts.py) with s02's own facts
and its Design: the Studio inside a page, where a link to an sNN lands (s02-D05, JL 261031: "we will remove the single
page for the studio"), the pop-out, and the code's structure."""
import re
import sys
from pathlib import Path

STUDIO_SKILL = Path("/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio")
sys.path.insert(0, str(STUDIO_SKILL / "scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402  (underscore names skip the star import)
import five_parts  # noqa: E402

HERE = Path(__file__).resolve().parent
WB = Path("/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/servers/workbench")
_fp = (WB / "focus_page.py").read_text(encoding="utf-8")
_fr = (WB / "frame.py").read_text(encoding="utf-8")
_css = (WB / "focus-assets/focus.css").read_text(encoding="utf-8")
SPEC = {
    "title": "The Studio's UI: inside every page, an sNN's link lands on its card",
    "why": {"question": "why do we need s02?",
            "notes": ["the Studio hid in\na studio/ folder", "no page showed sNN\nwith their Jobs", "a link to an sNN\nhad nowhere to land"],
            "quote": "JL 261030: “what I want to achieve is how to get the UI for the studio page”"},
    # each part names its file and functions (JL 261030: "for this one, you should specify the path"), under
    # plugins/haipipe-toolkit/servers/workbench/; the second line says what it is and why
    "what": {"head": "\u2461 what s02 hands over: the Studio's UI", "icon": "code", "name": "servers/workbench/", "type": "code",
             "deck_why": "stays in s02's delivery/deck/, so anyone gets it in a minute",
             "parts": [  # (icon, file: functions, what it is: why, built now)
                 ("code", "focus_page.py: studio_html, status_now_html", "the Studio inside a page: design beside the work",
                  "def status_now_html" in _fp and "def studio_html" in _fp and "STUDIO_ITEM" in _fr),
                 ("code", "focus_page.py: topic_home, rail_url", "an sNN's link: its card in its level's Studio (s02-D05)",
                  "def topic_home" in _fp and "def topic_page" not in _fp),
                 ("code", "focus_page.py: studio_html's picture", "the Studio card: its drawing, made by five_parts.py",
                  (HERE.parent / "s01-studio-skill/s01-studio-skill.png").is_file()),
                 ("code", "focus-assets/focus.css, focus.js", "the pop-out: a drawing opens big, page stays", "width:96vw" in _css)]},
    "job": HERE.parent / "j02_studio_pages",
    "target": "the workbench: focus_page.py, focus.css",
    "missing": [("ui/studio-in-a-page", "the agreed screen draft, not drawn yet")],
}


def frame_box(eid, x, y, w, h, title):
    """A browser window, drawn plainly: a frame and its address bar."""
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, title, 12, BODY)


def card(eid, x, y, w, name, stage, words, buttons):
    """An sNN's card: its name, stage and line, its buttons, its picture on the right."""
    els = [_el("rectangle", eid, x, y, w, 92, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_n", x + 12, y + 10, name, 14, TITLE)
    els += [_el("rectangle", eid + "_st", x + 12 + len(name) * 14 * 0.62 + 8, y + 9, len(stage) * 12 * 0.62 + 14, 20, ROOM, "#f1f3f5", roundness={"type": 3})]
    els += text(eid + "_st_t", x + 19 + len(name) * 14 * 0.62 + 8, y + 12, stage, 12, BODY) + text(eid + "_w", x + 12, y + 36, words, 12, INK)
    bx = x + 12
    for k, b in enumerate(buttons):
        bw = len(b) * 12 * 0.62 + 20
        els += [_el("rectangle", f"{eid}_b{k}", bx, y + 60, bw, 22, ROOM, "#ffffff", roundness={"type": 3})] + text(f"{eid}_b{k}_t", bx + 10, y + 64, b, 12, INK)
        bx += bw + 8
    return els + [_el("rectangle", eid + "_pic", x + w - 130, y + 10, 118, 72, ROOM, "#fff4e6")] + text(eid + "_pic_t", x + w - 120, y + 38, "its drawing", 11, OR)


def design():
    els = []
    #   A: the Studio inside a page, a Block's (also a Job's or a Task's): its sNN as cards, beside its Jobs
    els += text("skA", 690, 280, "A · the Studio inside a page", 18, TITLE)
    els += shapes("skA_s", 690, 306, "delivery/ui/studio-in-a-page")
    els += frame_box("wA", 690, 340, 640, 470, "…/_board/workbench?path=b35_studio&section=studio")
    els += text("wA_crumb", 740, 380, "Tools-SPACE / blueprints / Project-PageParts / work / b35_studio", 11, BODY)
    els += text("wA_t", 740, 400, "b35_studio", 22, INK) + text("wA_sec", 890, 406, "Studio", 18, ROOM)
    for k in range(6):                                   # the section rail: Report, Work, Studio (here), Delivery, ...
        els += line(f"wA_rail{k}", [(704, 446 + 22 * k), (722, 446 + 22 * k)], OR if k == 2 else ROOM, 3 if k == 2 else 1)
    for k, (nm, st, wd) in enumerate((("b35-s01:studio @ studio_skill", "shaping", "one sNN, one idea, one delivery."),
                                      ("b35-s02:studio @ studio_pages", "explore", "the Studio's UI: inside every page"),
                                      ("b35-s03:studio @ mindmap_leaf_drawing", "explore", "one leaf, one drawing"))):
        els += card(f"wA_c{k}", 740, 446 + 110 * k, 570, nm, st, wd, ["Draw", "Mind map", "Ideas"])
    els += text("wA_n", 690, 822, "Report › Status lists the same sNN first, then the Jobs and Tasks", 13, BODY)
    els += sticky("ask_jobpage", 1180, 880, 300, 64, "? a Job page shows its\nTasks' sNN too", 15, -0.03, RED, RE)

    #   B: a link to an sNN lands on its card (s02-D05): the left rail's sNN opens its level's Studio, the card outlined
    XB = 1440
    els += text("skB", XB, 280, "B · a link to an sNN lands on its card", 18, TITLE)
    els += shapes("skB_s", XB, 306, "s02-D05: no page of its own (JL 261031)")
    els += [_el("rectangle", "wB_rail", XB, 340, 170, 300, ROOM, "#ffffff", roundness={"type": 3})]
    els += text("wB_rail_t", XB + 12, 350, "left rail", 12, BODY)
    for k, nm in enumerate(("b35_studio", "s01-studio-skill", "s02-studio-pages", "s05-studio-gallery", "j01_…", "j02_…")):
        els += text(f"wB_r{k}", XB + (12 if k == 0 else 26), 378 + 34 * k, nm, 13, OR if k == 2 else INK)
    els += arrow("wB_go", [(XB + 176, 454), (XB + 250, 454)], OR)
    els += frame_box("wB", XB + 260, 340, 380, 330, "…?path=b35_studio&section=studio#s02-studio-pages")
    for k, nm in enumerate(("b35-s01 @ studio_skill", "b35-s02 @ studio_pages", "b35-s05 @ studio_gallery")):
        hot = k == 1
        els += [_el("rectangle", f"wB_c{k}", XB + 280, 390 + 90 * k, 340, 76, OR if hot else ROOM, "#e7f5ff" if hot else "#ffffff",
                    roundness={"type": 3}, strokeWidth=3 if hot else 1)]
        els += text(f"wB_c{k}_t", XB + 294, 402 + 90 * k, nm, 13, TITLE if hot else INK)
        els += text(f"wB_c{k}_b", XB + 294, 430 + 90 * k, "Slide · Draw · Mind map · Work", 11, BODY)
    els += text("wB_n", XB, 700, "an old ?path=…/sNN link is sent on (302) to the same card;\nthe card's name and line open the face, its picture the slide", 13, BODY)

    #   C: the pop-out: Draw, Mind map and Ideas open over the page, nearly the whole window
    YC = 980
    els += text("skC", 690, YC, "C · the pop-out", 18, TITLE)
    els += shapes("skC_s", 690, YC + 26, "focus.css: the dialog, 96% x 94% of the window")
    els += [_el("rectangle", "pC_page", 690, YC + 70, 420, 250, ROOM, "#f1f3f5")]
    els += [_el("rectangle", "pC_dlg", 700, YC + 78, 400, 234, INK, "#ffffff", roundness={"type": 3})]
    els += text("pC_t", 714, YC + 86, "s01-studio-skill", 12, INK) + text("pC_x", 1060, YC + 86, "Close", 12, BODY)
    els += text("pC_in", 760, YC + 180, "the drawing, to pan, zoom and draw", 13, BODY)
    els += text("pC_n", 1130, YC + 120, "a row's Draw, Mind map\nor Ideas opens here;\nthe page stays behind it", 13, INK)

    #   D: the code's structure: the workbench files the Studio's UI lives in, s02's parts in green
    XD = 1440
    els += text("skD", XD, YC, "D · the code's structure: servers/workbench", 18, TITLE)
    els += shapes("skD_s", XD, YC + 26, "green = s02's parts, read from the code")
    mine = {"studio_html", "status_now_html", "picture_of", "is_topic", "topic_home", "rail_url", "static_page",
            "delivery_document", "parts_mindmap"}
    fns = [f for f in re.findall(r"(?m)^def (\w+)\(", _fp) if f in mine]
    els += listing("cD_fp", XD, YC + 66, f"focus_page.py · {len(re.findall(r'(?m)^def ', _fp))} functions, s02's:", fns, lambda r: True)
    frs = [f for f in ("_studio_topics", "topic_owner", "group_file", "topic_label", "topic_address") if f"def {f}(" in _fr]
    els += listing("cD_fr", XD + 330, YC + 66, "frame.py, s02's:", frs, lambda r: True)
    els += listing("cD_as", XD + 330, YC + 66 + 28 + 22 * len(frs) + 20, "focus-assets/", ["focus.css: the pop-out's size", "focus.js: opens the pop-out"],
                   lambda r: True)
    return els


if __name__ == "__main__":
    def with_kept():
        els = design()
        return els + kept_first(HERE, max(e["y"] + e["height"] for e in els) + 120)
    five_parts.build(HERE, SPEC, with_kept)
