"""b35-s01:studio @ studio_skill, its drawing: the five parts (haipipe-studio scripts/five_parts.py) with s01's own
facts and its Design sketches A to E, each shaping a piece of its delivery (the haipipe-studio skill)."""
import re as _re0
import sys
import textwrap
from pathlib import Path

STUDIO_SKILL = Path("/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio")
sys.path.insert(0, str(STUDIO_SKILL / "scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
import five_parts  # noqa: E402
from five_parts import _el  # noqa: E402  (underscore names skip the star import)

HERE = Path(__file__).resolve().parent
_md = (STUDIO_SKILL / "SKILL.md").read_text(encoding="utf-8")
_nt = (STUDIO_SKILL / "scripts/new_topic.py").read_text(encoding="utf-8")
SPEC = {
    "title": "What a Studio is, and what each sNN delivers",
    "why": {"question": "why do we need s01?",
            "notes": ["sNN grew into\nreports and\nlong chats", "they handed\nnothing over", "nobody could say\nwhat a Studio\nis for"],
            "quote": "JL 261029 (translated): \u201cI don't know what this studio really stands for\u201d"},
    "what": {"head": "\u2461 what s01 hands over: one skill", "icon": "book", "name": "haipipe-studio", "type": "skill",
             "deck_why": "stays in s01's delivery/deck/, so anyone gets it in a minute",
             "parts": [  # (icon, part, why, on disk now)
                 ("doc", "SKILL.md: First principle", "so every sNN pulls people in, never a report", "## First principle" in _md),
                 ("doc", "SKILL.md: one delivery, its type", "so every sNN names the one thing it hands over",
                  "one clean thing of one type" in _md and "`**Delivery type:**`" in _md),
                 ("doc", "SKILL.md: where it sits, how many", "so the design sits beside the work", "There is no `studio/` folder" in _md),
                 ("doc", "SKILL.md: how an sNN lives", "so everyone knows when it is done", bool(_re0.search(r"(?m)^How an sNN lives", _md))),
                 ("doc", "SKILL.md: one Studio, every Theme", "so each Theme plugs in the same way",
                  "<!-- /render b35-s01 themes -->" in _md and "(not rendered yet)" not in _md),
                 ("code", "new_topic.py: For:, Delivery type, limits", "so every new sNN names its delivery first",
                  "**For:**" in _nt and "**Delivery type:**" in _nt and "LIMITS" in _nt)]},
    "started": "started from:\nevery studio/ and\ndelivery/, 8 SPACEs",
    "job": HERE.parent / "j01_studio_delivery_type",
    "target": "haipipe-studio SKILL.md",
    "missing": [("skill/how-it-lives.md", "a SKILL.md section, not written yet")],
}


def design():
    els = []
    # fewer, smaller sketches, one per delivery piece, each saying which piece it shapes (JL 261030: "for these design,
    # how do you think these design is attached to the delivery or not?"; "we have so many things here"); the kinds of
    # Block (old sketch C) shape no piece of s01, so they left; the full Theme table lives in delivery/skill/themes.md
    #   A: the rule, shapes skill/one-delivery.md
    els += text("skA", 690, 280, "A \u00b7 the rule: one sNN, one idea, one delivery", 18, TITLE)
    els += shapes("skA_s", 690, 306, "skill/one-delivery.md")
    els += bulb("rule_bulb", 716, 380, 26) + text("rule_idea", 752, 368, "an idea", 16, INK)
    els += arrow("rule_a", [(850, 380), (900, 380)], OR, dashed=True)
    els += [_el("ellipse", "rule_nn", 902, 354, 52, 52, NAVY, SEM["plain"][0], strokeWidth=2)] + text("rule_nn_t", 928, 371, "sNN", 15, NAVY, "center")
    els += arrow("rule_b", [(956, 380), (1000, 380)], GR) + gift("rule_g", 1006, 360, 66, 50)
    els += text("rule_d", 1086, 368, "deck + one thing,\none type", 16, GR)

    #   B: one Studio, every Theme, shapes skill/themes.md; one line a Theme: who renders its sNN's delivery
    THEME = {"work": ("#1864ab", "render_delivery.py, a Task"), "paper": ("#d9480f", "haipipe-paper-assemble"),
             "display": ("#2b8a3e", "haipipe-display"), "labeling": ("#8a6d00", "haipipe-labeling"),
             "design": ("#c2255c", "haipipe-design-delivery"), "insight": ("#0b7285", "haipipe-insight"),
             "discovery": ("#5f3dc4", "haipipe-discovery"), "cowork": ("#7048e8", "a person, haipipe-cowork")}
    els += text("skB", 690, 480, "B \u00b7 one Studio, every Theme", 18, TITLE)
    els += shapes("skB_s", 690, 506, "skill/themes.md")
    els += text("skB_h", 690, 540, "Theme       its sNN's delivery is rendered by", 13, BODY)
    for k, (name, (ink, owner)) in enumerate(THEME.items()):
        y = 568 + 30 * k
        els += text(f"thB{k}", 690, y, name, 16, ink) + arrow(f"thB{k}_a", [(800, y + 10), (850, y + 10)], ink)
        els += text(f"thB{k}_o", 862, y, owner, 15, INK)
    els += text("skB_n", 690, 568 + 30 * len(THEME) + 8, "each Theme's kinds, by level: in themes.md", 13, ROOM)
    els += sticky("ask_kinds", 1170, 640, 230, 70, "? are these\nthe kinds", 16, -0.05, RED, RE)


    #   D: where an sNN sits and how many, shapes skill/where-it-sits.md and skill/how-many.md
    XD = 1440
    els += text("skD", XD, 280, "C \u00b7 where an sNN sits, how many", 18, TITLE)
    els += shapes("skD_s", XD, 306, "skill/where-it-sits.md, skill/how-many.md")
    els += tree("dA", XD, 350, [
        (0, "b35_studio/", "the Block", TITLE),
        (1, "s01-\u2026/", "the whole Block uses it \u00b7 at most 9", NAVY),
        (2, "delivery/", "deck + the thing, then render", GR),
        (1, "j01_\u2026/", "a Job", TITLE),
        (2, "s08-\u2026/", "one Job uses it \u00b7 at most 5", NAVY),
        (2, "t03_\u2026/", "a Task", TITLE),
        (3, "s09-\u2026/", "one result \u00b7 at most 3", NAVY)])

    #   E: how an sNN lives, shapes skill/how-it-lives.md, not written yet: a chat makes it, rounds are passes, a person
    #   says agreed, the agreed version goes to delivery/ and renders out
    YE = 640
    els += text("skE", XD, YE, "D \u00b7 how an sNN lives", 18, TITLE)
    els += shapes("skE_s", XD, YE + 26, "skill/how-it-lives.md  (not written yet)")
    STEPS = [("explore", OR), ("shaping", OR), ("agreed", GR), ("closed", ROOM)]
    for k, (st, ink) in enumerate(STEPS):
        x = XD + k * 150
        els += [_el("rectangle", f"lf{k}", x, YE + 76, 112, 40, ink, "#ffffff", roundness={"type": 3})]
        els += text(f"lf{k}_t", x + 56, YE + 86, st, 16, ink, "center")
        if k:
            els += arrow(f"lf{k}_a", [(x - 36, YE + 96), (x - 4, YE + 96)], INK)
    els += arrow("lf_loop", [(XD + 206, YE + 120), (XD + 206, YE + 160), (XD + 56, YE + 160), (XD + 56, YE + 120)], OR, dashed=True)
    els += text("lf_loop_t", XD + 70, YE + 166, "each round is a pass, passes/pNN-<MMDD>/", 13, OR)
    els += arrow("lf_out", [(XD + 356, YE + 120), (XD + 356, YE + 210)], GR, width=2)
    els += gift("lf_gift", XD + 330, YE + 214, 50, 38) + text("lf_out_t", XD + 392, YE + 220, "delivery/ \u2500render\u25b8 its home", 15, GR)
    els += sticky("ask_agreed", XD + 150, YE + 300, 260, 64, "? who says agreed", 16, 0.03, RED, RE)

    #   E: the skill's structure, the shape of what s01 delivers (JL 261030: "in the design, should have the E area, so that
    #   we can ... know the structure of the delivery of the skill, I mean what is the skill structure for it"): the
    #   haipipe-studio folder, and SKILL.md's sections in order, s01's own (rendered from its delivery/) in green; read
    #   from disk on every rebuild
    YS = 920
    els += text("skS", 690, YS, "E \u00b7 the skill's structure: haipipe-studio", 18, TITLE)
    els += shapes("skS_s", 690, YS + 26, "the whole skill; green = rendered from s01's delivery/")
    _sk = STUDIO_SKILL / "SKILL.md"
    _lines, _fence, _mine, _heads = _sk.read_text(encoding="utf-8").split("\n"), False, False, []
    _body = next(i for i in range(1, len(_lines)) if _lines[i] == "---") + 1 if _lines[0] == "---" else 0   # past front matter
    _start = None
    for _i in range(_body, len(_lines)):
        _ln = _lines[_i]
        if _ln.startswith("<!-- render b35-s01"):
            _mine, _start = True, (len(_heads), _ln.split()[3].rstrip(":"))
            continue
        if _ln.startswith("<!-- /render b35-s01"):
            if _start and len(_heads) == _start[0]:          # an s01 part with no heading of its own: list it by name
                _heads.append((_start[1].replace("-", " ") + " (no heading)", True))
            _mine, _start = False, None
            continue
        if _ln.startswith("```"):
            _fence = not _fence
            continue
        if _fence:
            continue
        if _ln.startswith("## "):
            _heads.append((_ln[3:].strip(), _mine))
        elif _i + 1 < len(_lines) and _re0.fullmatch(r"-{3,}", _lines[_i + 1]) and _ln.strip() and not _ln.startswith(("|", "<!--")):
            _heads.append((_ln.strip(), _mine))
    els += i_book("skS_book", 690, YS + 66) + text("skS_root", 746, YS + 70, "haipipe-studio/", 17, TITLE)
    els += text("skS_md", 720, YS + 116, "SKILL.md, its sections in order", 15, INK)
    for k, (head, mine) in enumerate(_heads):
        els += text(f"skS_h{k}", 740, YS + 144 + 22 * k, textwrap.shorten(head, 46, placeholder="\u2026"), 13, GR if mine else BODY)
    _fold = [(name, words) for name, words in (("scripts/", "new_topic.py, render_delivery.py, quick_draw.py, \u2026"),
                                               ("ref/", "topic contract, reader review, screen, chat, draw"),
                                               ("tests/", "test_haipipe_studio.py"), ("CHANGELOG.md", "its versions"))
             if (STUDIO_SKILL / name.rstrip("/")).exists()]
    for k, (name, words) in enumerate(_fold):
        y = YS + 116 + 52 * k
        els += text(f"skS_f{k}", 1140, y, name, 15, INK) + text(f"skS_f{k}_w", 1140, y + 20, words, 12, BODY)
    # below A to E: what one sNN holds, kept from the first sketches (JL 261030: "We should keep them"); the gallery,
    # once F1 and F2 here, is now its own two sNN: b35-s05 the studio gallery (each kind of sNN) and b35-s04 the
    # delivery gallery (the kinds of Block); JL 261030: "we might also have a sNN for the gallery of the deliveries,
    # and gallery of the studios"
    old = kept()
    top = max(e["y"] + e["height"] for e in els) + 140
    dx, dy = 690 - min(e["x"] for e in old), top + 100 - min(e["y"] for e in old)
    for e in old:
        e["id"], e["x"], e["y"] = "kept_" + e["id"], e["x"] + dx, e["y"] + dy
    els += text("kept_h", 690, top, "F \u00b7 what one sNN holds (kept)", 22, TITLE)
    els += shapes("kept_s", 690, top + 34, "skill/where-it-sits.md; the galleries moved to s04 and s05")
    els += line("kept_rule", [(690, top + 62), (2300, top + 62)], ROOM, 1, True)
    return els + old


def kept():
    """The earlier sketch kept here (JL 261030: "why the original content is gone? We should keep them"): what one sNN
    holds (old D's second tree). Old B, the catalogue of sNN kinds, is in b35-s05's builder; old C, the kinds of Block,
    in b35-s04's. Drawn below A to E by design(), their ids prefixed kept_."""
    els = []
    XC = 1560                                       # where old sketch D sat beside old C
    #   sketch D: the structure of the Studio (JL 261030: "after A, B, C, have a D, showing what is the structure of the
    #   studio"), from haipipe-studio SKILL.md's folder contract and b35-s02 / s04; below C, right of B's long rows
    XD, YD, NOTE = XC + 80, 1240, 330


    def tree(prefix, x, y, rows, step=32):
        """A folder tree drawn with lines: (depth, name, what it is, colour) per row."""
        out = []
        for k, (depth, name, note, color) in enumerate(rows):
            ry, lx = y + k * step, x + depth * 26
            if depth:
                out += line(f"{prefix}{k}_l", [(lx - 18, ry - 16), (lx - 18, ry + 9), (lx - 5, ry + 9)], ROOM, 1)
            out += text(f"{prefix}{k}", lx, ry, name, 15, color)
            if note:
                out += text(f"{prefix}{k}_n", x + NOTE, ry + 1, note, 13, BODY)
        return out


    els += text("skD", XD, YD, "D · the structure of the Studio (proposed)", 17, BODY)
    els += text("skD2", XD, YD + 24, "(haipipe-studio SKILL.md folder contract; b35-s02, s04; 261030)", 13, ROOM)
    # no studio/ folder: each sNN sits beside the Jobs or Tasks of the level it serves, its count capped per level
    # (JL 261030: "we just have sNN, along side with jNN"; "we might have many sNN, but we need to control the numbers")
    els += text("skD_a", XD, YD + 62, "where it sits: beside the Jobs or Tasks it serves; one numbering per Block", 14, PU)
    els += tree("dA", XD, YD + 96, [
        (0, "b35_studio/", "the Block", TITLE),
        (1, "s01-…/", "whole Block uses it · at most 9", NAVY),
        (1, "j01_…/", "a Job: makes what an sNN decided", TITLE),
        (2, "s08-…/", "one Job uses it · at most 5", NAVY),
        (2, "t03_…/", "a Task", TITLE),
        (3, "s09-…/", "one result · at most 3", NAVY),
        (1, "delivery/", "only the agreed version", GR)])
    YB = YD + 96 + 7 * 32 + 40
    els += text("skD_b", XD, YB, "what one sNN holds", 14, PU)
    els += tree("dB", XD, YB + 34, [
        (0, "sNN-<topic>/", "", TITLE),
        (1, "sNN-<topic>.md", "the face: For, Covers, Excluded, At, Decided, Open", NAVY),
        (1, "sNN-<topic>.excalidraw", "the drawing, to think on together", OR),
        (1, "sNN-<topic>.mindmap.md", "the mind map, a drawing per leaf", OR),
        (1, "ideas.md + slides/", "the ideas, and the deck's pictures", OR),
        (1, "passes/pNN-<MMDD>/", "one round: a session or a meeting", PU),
        (1, "result/", "working output; messy is fine", PU)])
    YEND = YB + 34 + 7 * 32 + 10
    els += arrow("dB_go", [(XD + 26, YEND), (XD + 26, YEND + 40), (XD + 90, YEND + 40)], GR, width=2)
    els += text("dB_go_t", XD + 100, YEND + 28, "agreed ▸ delivery/: the deck + the thing", 15, GR)
    els += sticky("ask_jobs", XD + 470, YEND + 100, 340, 70, "? a Block with 2+ Jobs keeps\none sNN that designs its Jobs", 15, -0.03, RED, RE)

    return [e for e in els if not e["id"].startswith(("dA", "skD"))]   # old D's first tree is today's sketch C; F names it


if __name__ == "__main__":
    five_parts.build(HERE, SPEC, design)
