"""s60 · Skills: Studio: s60-skill-studio.excalidraw, drawn by this builder as pictures (hai-studio CONSTITUTION A04).

The logic of hai-studio: a blueprint Block designs a Studio Type and delivers it into the skill;
a Studio Type and a topic of it are the same screen, top and left; the type's right side
is a list of what must be shown, the topic's right side is the real thing. Below, the path of one topic, each stop a
picture. The big number is read on every build: how many topics of this Block follow the type they name.

How it looks: /hai-draw and hai-studio's icons.py. A rebuild keeps what a person drew on the canvas (canvas.write).

    <host venv python> build_s60_skill_studio.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPACE = next(p for p in HERE.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
KIT = SPACE / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts"
sys.path.insert(0, str(KIT))
import five_parts as fp  # noqa: E402
from five_parts import GR, OR, PU, RE, YE, NAVY, INK, SEM, _el, arrow, line, poly, text  # noqa: E402
from icons import big_number, document, shield  # noqa: E402
from icon_library import item  # noqa: E402

BLUE, WHITE = SEM["plain"][0], "#ffffff"


def screen(k, x, y, color, fill, buttons, tabs):
    """A workbench screen: buttons on top, tabs on the left, one pane on the right; returns (els, the pane's box)."""
    w, h = 640, 400
    els = [_el("rectangle", k, x, y, w, h, color, fill, strokeWidth=4, roundness={"type": 3}),
           _el("rectangle", k + "_in", x + 14, y + 14, w - 28, h - 28, color, WHITE, strokeWidth=1)]
    bx = x + 30
    for i, name in enumerate(buttons):
        bw = len(name) * 11 + 30
        els += [_el("rectangle", f"{k}_b{i}", bx, y + 30, bw, 36, NAVY, BLUE if i == 0 else WHITE, roundness={"type": 3})]
        els += text(f"{k}_b{i}_t", bx + bw / 2, y + 38, name, 16, NAVY, "center")
        bx += bw + 12
    for i, name in enumerate(tabs):
        ty = y + 88 + i * 44
        els += [_el("rectangle", f"{k}_t{i}", x + 30, ty, 176, 34, NAVY if i == 0 else fp.ROOM, BLUE if i == 0 else WHITE,
                    roundness={"type": 3})]
        els += text(f"{k}_t{i}_t", x + 42, ty + 8, name, 15, NAVY if i == 0 else INK)
    pane = (x + 222, y + 88, w - 252, h - 118)
    els += [_el("rectangle", k + "_pane", *pane, color, fill, strokeWidth=2, roundness={"type": 3})]
    els += poly(k + "_stand", [(x + w / 2 - 44, y + h), (x + w / 2 + 44, y + h), (x + w / 2 + 62, y + h + 40),
                               (x + w / 2 - 62, y + h + 40)], color, fill)
    els += [_el("rectangle", k + "_base", x + w / 2 - 110, y + h + 40, 220, 14, color, fill)]
    return els, pane


def following():
    """(topics that follow the type they name, topics that name one) in this Block, read now."""
    import type_follow
    found = [type_follow.problems(t) for t in type_follow.topics_of(HERE.parent)]
    named = [f for f in found if f is not None]
    return sum(not bad for bad, _ in named), len(named)


def build():
    els = fp.heading("hai-studio · a topic is its type, with the real thing on the right",
                     "the type says what a topic must show; a topic is started from its type and held to it")
    # who asks
    els += item("Ideation", "who", 20, 330, h=230, lib="stick-figures-collaboration", color=NAVY)   # two people, an idea
    els += fp.bubble("ask", 120, 170, 420, 150, "What should\nthis topic show?", 26)

    # the class and one instance of it: the same screen
    tabs = ["SKILL.md", "CONSTITUTION.md", "ref/", "scripts/", "tests/"]
    kind, (px, py, pw, ph) = screen("kind", 640, 200, OR, SEM["start"][0], ["〈skill〉", "Draw", "Check"],
                                    ["SKILL.md", "CONSTITUTION.md", "ref/", "scripts/", "〈folder〉/"])
    els += text("kind_h", 640, 138, "Studio Type", 36, OR) + kind
    els += text("kind_p", 870, 152, "types/skills/elements.md", 18, INK)
    for i in range(4):                                         # a list of what must be shown: boxes not ticked yet
        els += [_el("rectangle", f"must_b{i}", px + 30, py + 34 + i * 54, 26, 26, OR, WHITE, strokeWidth=2)]
        els += line(f"must_l{i}", [(px + 72, py + 47 + i * 54), (px + pw - 40 - (i % 2) * 70, py + 47 + i * 54)], OR, 4)
    els += text("must_t", px + pw / 2, py + ph - 44, "what must be shown", 22, OR, "center")
    topic, (qx, qy, qw, qh) = screen("topic", 1640, 200, GR, SEM["end"][0], ["hai-studio", "Draw", "Check"], tabs)
    els += text("topic_h", 1640, 138, "a topic", 36, GR) + topic
    els += text("topic_p", 1790, 152, "s60-skill-studio/", 18, INK)
    els += document("real", qx + 50, qy + 26, "ok", 130, 170)
    for i in range(3):                                         # the same list, kept
        els += fp.tick(f"real_tk{i}", qx + 230, qy + 40 + i * 54)
        els += line(f"real_l{i}", [(qx + 274, qy + 52 + i * 54), (qx + qw - 36, qy + 52 + i * 54)], GR, 4)
    els += text("real_t", qx + qw / 2, qy + qh - 44, "the real thing", 22, GR, "center")

    # between them
    els += arrow("same", [(1300, 330), (1620, 330)], NAVY, width=8)
    els += text("same_t", 1460, 250, "same top, same left", 24, NAVY, "center")
    els += arrow("names", [(1620, 500), (1300, 500)], OR, dashed=True, width=4)
    els += text("names_t", 1460, 516, "names its type", 20, OR, "center")
    els += fp.sticky("only", 1460, 418, 250, 96, "only the right\nside differs", 22, -0.05)

    # where a type comes from: a blueprint Block designs it, the skill keeps it
    els += [e for e in item("clipboard", "bp", 60, 560, h=150, lib="icons") if e["type"] != "text"]   # its own caption off
    els += text("bp_t", 115, 722, "blueprint Block", 24, OR, "center")
    els += text("bp_s", 115, 756, "designs the type", 17, INK, "center")
    els += arrow("deliver", [(200, 640), (360, 640)], OR, width=5)
    els += text("deliver_t", 280, 600, "delivers", 20, OR, "center")
    els += fp.gear("skill", 440, 640, 56)
    els += text("skill_t", 440, 712, "hai-studio", 30, PU, "center")
    els += text("skill_s", 440, 754, "keeps every type: types/", 17, INK, "center")
    els += arrow("skill_kind", [(510, 610), (640, 540)], PU, width=3)
    els += text("skill_kind_t", 590, 596, "types/skills/", 16, PU)

    # the path of one topic, each stop a picture
    y = 900
    els += fp.bulb("p_idea", 150, y, 46)
    els += item("Search", "p_lens", 470, y - 60, h=120, lib="basic-ux-wireframing-elements", color=NAVY)
    els += document("p_from", 860, y - 70, "wait", 86, 112) + arrow("p_copy", [(956, y - 10), (1000, y - 10)], OR, width=4)
    els += document("p_new", 1010, y - 70, "off", 86, 112)
    els += document("p_fill", 1330, y - 70, "ok", 86, 112)
    els += poly("p_pen", [(1404, y + 30), (1462, y - 56), (1482, y - 44), (1424, y + 42)], OR, "#ffe066")
    els += shield("p_hold", 1700, y - 78, "ok", 1.1)
    els += fp.gift("p_gift", 2110, y - 40, 120, 92)
    stops = [(150, "an open idea"), (520, "find its type"), (980, "start from the type"), (1400, "fill each part"),
             (1770, "hold it to the type"), (2170, "delivery")]
    for i, (cx, name) in enumerate(stops):
        els += text(f"p_n{i}", cx, y + 86, name, 24, INK, "center")
    for i, (a, b, c) in enumerate(((230, 420, OR), (620, 830, NAVY), (1120, 1300, OR), (1500, 1680, GR), (1870, 2080, GR))):
        els += arrow(f"p_a{i}", [(a, y), (b, y)], c, width=5)
    els += text("p_where", 520, y + 122, "in hai-studio: types/", 16, PU, "center")
    els += text("p_none", 520, y + 146, "none? design it in a blueprint Block", 16, RE, "center")
    els += text("p_cmd1", 980, y + 122, "type_follow.py new skills <topic>", 16, PU, "center")
    els += text("p_cmd2", 1770, y + 122, "type_follow.py check", 16, PU, "center")
    els += fp.sticky("fix", 1590, y + 210, 230, 84, "differs?\nfix, check again", 18, 0.05, fp.RED, RE)
    els += arrow("fix_back", [(1700, y + 150), (1700, y + 185), (1420, y + 185), (1420, y + 150)], RE, width=3)

    ok, named = following()
    els += big_number("follow", 1460, 590, f"{ok} of {named}", "topics of this Block follow\nthe type they name",
                      GR if ok == named else OR, 64)

    out = HERE / f"{HERE.name}.excalidraw"
    fp.marks_writer(out, els)
    subprocess.run([sys.executable, str(KIT / "render_png.py"), str(out), str(out.with_suffix(".png"))], check=True)
    print(out)


if __name__ == "__main__":
    build()
