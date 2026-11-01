"""b35-s03:studio @ mindmap_leaf_drawing, its drawing: the five parts (haipipe-studio scripts/five_parts.py) with s03's
own facts and its Design: one leaf, one drawing; the map wraps; haipipe-mindmap's structure."""
import sys
from pathlib import Path

STUDIO_SKILL = Path("/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio")
sys.path.insert(0, str(STUDIO_SKILL / "scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402  (underscore names skip the star import)
import five_parts  # noqa: E402

HERE = Path(__file__).resolve().parent
MM = Path("/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/1_base/project/haipipe-mindmap")
_md = (MM / "SKILL.md").read_text(encoding="utf-8")
SPEC = {
    "title": "One leaf, one drawing: the mind map, its drawings and slides",
    "why": {"question": "why do we need s03?",
            "notes": ["a map's leaves had\nno drawing", "map, drawings and\nslides were apart", "it took three\ntries to say"],
            "quote": "JL 261029 (translated): “one leaf, one drawing, and it can hold several slides”"},
    "what": {"head": "② what s03 hands over: one skill", "icon": "book", "name": "haipipe-mindmap", "type": "skill",
             "deck_why": "stays in s03's delivery/deck/, so anyone gets it in a minute",
             "parts": [  # (icon, part, why, on disk now)
                 ("doc", "SKILL.md: one drawing per leaf", "so every point can be drawn and talked over",
                  "each leaf under it has one drawing" in _md),
                 ("doc", "SKILL.md: the map wraps", "so a wide map still reads on a card", "map wraps to its card's width" in _md),
                 ("code", "mmsketch.py: seeds each leaf's drawing", "so a leaf's drawing is there before anyone asks",
                  (MM / "scripts/mmsketch.py").is_file()),
                 ("code", "mmmap.py: the ✎ link on each leaf", "so a click on a leaf opens its drawing",
                  "✎" in (MM / "scripts/mmmap.py").read_text(encoding="utf-8"))]},
    "job": None,
    "target": "haipipe-mindmap SKILL.md",
    "missing": [("skill/one-leaf-one-drawing.md", "a haipipe-mindmap SKILL.md section, not written yet")],
}


def design():
    els = []
    #   A: one leaf, one drawing: the map, a leaf, and the drawing it opens, holding its slides
    els += text("skA", 690, 280, "A · one leaf, one drawing", 18, TITLE)
    els += shapes("skA_s", 690, 306, "skill/one-leaf-one-drawing.md")
    els += [_el("rectangle", "mA_root", 690, 470, 150, 44, INK, "#ffffff", roundness={"type": 3})] + text("mA_root_t", 765, 482, "The total workflow", 12, INK, "center")
    for s, (nm, y) in enumerate((("section 1", 380), ("section 2", 560))):
        els += line(f"mA_s{s}_l", [(840, 492), (900, y + 18)], ROOM, 1)
        els += [_el("rectangle", f"mA_s{s}", 900, y, 110, 36, INK, "#ffffff", roundness={"type": 3})] + text(f"mA_s{s}_t", 955, y + 10, nm, 12, INK, "center")
        for k in range(3):
            ly = y - 40 + k * 40
            here = s == 0 and k == 1
            els += line(f"mA_l{s}{k}_c", [(1010, y + 18), (1060, ly + 12)], ROOM, 1)
            els += text(f"mA_l{s}{k}", 1066, ly + 2, "a leaf  ✎", 13, OR if here else BODY)
    els += arrow("mA_open", [(1150, 382), (1230, 382)], OR, width=2)
    els += [_el("rectangle", "mA_draw", 1236, 330, 300, 200, OR, "#fff9db", roundness={"type": 3})]
    els += text("mA_draw_t", 1250, 340, "its one drawing", 14, OR)
    for k in range(2):                                    # the drawing holds its slides
        els += [_el("rectangle", f"mA_sl{k}", 1260 + k * 130, 390, 112, 70, OR, "#ffffff")] + text(f"mA_sl{k}_t", 1270 + k * 130, 412, f"slide {k + 1}", 12, OR)
    els += text("mA_n", 1250, 480, "a drawing can hold several slides", 12, BODY)
    els += sticky("ask_every", 1380, 620, 320, 64, "? every leaf gets a drawing,\nor only a leaf with a slide", 14, 0.03, RED, RE)

    #   B: the map wraps to the page, so a wide map still reads
    YB = 720
    els += text("skB", 690, YB, "B · the map wraps", 18, TITLE)
    els += shapes("skB_s", 690, YB + 26, "SKILL.md: a topic's map wraps to its card's width")
    for k in range(6):                                    # too wide: one long row
        els += [_el("rectangle", f"mB_w{k}", 690 + k * 110, YB + 70, 96, 30, ROOM, "#ffffff", roundness={"type": 3})]
    els += text("mB_w_t", 690, YB + 108, "too wide: off the card", 12, RE)
    for k in range(6):                                    # wrapped: two rows
        els += [_el("rectangle", f"mB_r{k}", 690 + (k % 3) * 110, YB + 140 + (k // 3) * 42, 96, 30, GR, "#ebfbee", roundness={"type": 3})]
    els += text("mB_r_t", 690, YB + 230, "wrapped: fits the card", 12, GR)

    #   C: haipipe-mindmap's structure: SKILL.md's sections in order, and its scripts; s03's parts in green
    XC = 1440
    els += text("skC", XC, YB, "C · the skill's structure: haipipe-mindmap", 18, TITLE)
    els += shapes("skC_s", XC, YB + 26, "the whole skill; green = s03's parts")
    heads = headings(MM / "SKILL.md")
    els += listing("cC_md", XC, YB + 66, "SKILL.md, its sections in order", heads or ["(no sections)"], lambda r: "leaf" in r.lower() or "wrap" in r.lower())
    scripts = sorted(p.name for p in (MM / "scripts").glob("*.py"))
    els += listing("cC_sc", XC + 360, YB + 66, "scripts/", scripts, lambda r: r in ("mmsketch.py", "mmmap.py"))
    return els


if __name__ == "__main__":
    def with_kept():
        els = design()
        return els + kept_first(HERE, max(e["y"] + e["height"] for e in els) + 120)
    five_parts.build(HERE, SPEC, with_kept)
