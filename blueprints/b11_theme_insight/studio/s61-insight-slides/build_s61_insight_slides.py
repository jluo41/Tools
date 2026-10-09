"""s61 · Insight slides: s61-insight-slides.excalidraw: the deck's logic, then its slides.

The insight side of b12's s61-design-slides, in the same shape (JL 261007: b12's "is much better"). Three
frames, all read from slides.py:

    logic flow    one box per slide, top to bottom, its claim and what it is drawn from; the words on
                  each arrow say why the next slide follows; the groups (why · what · how · learn · now)
                  bracket them on the left
    storyboard    every slide as it will show, drawn by b12's slide_kit.py, the same layout build_deck.py
                  writes into the deck; under each, the drawings it comes from
    open          what is still to decide, in red

Marks a person adds are kept on rebuild (canvas.write). The deck itself is build_deck.py's.

    python build_s61_insight_slides.py [out.excalidraw]
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESIGNS = HERE.parents[2]
B03 = DESIGNS / "b03_project_workbench" / "studio"              # the shared drawing helpers and canvas.write
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
sys.path.insert(0, str(HERE))
import build_ladder_v4 as L  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
from slides import GROUPS, SLIDES, THESIS  # noqa: E402


def kit():
    """b12's slide layout (one slide, drawn for any pen), loaded by path so its own slides.py never shadows ours."""
    spec = importlib.util.spec_from_file_location(
        "slide_kit", DESIGNS / "b12_theme_design" / "studio" / "s61-design-slides" / "slide_kit.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


K = kit()
SUB_INK = "#495057"
NOTE = ("✎ 261007 rebuilt in b12's s61 shape: the logic first, then each slide drawn as it will show; build_deck.py "
        "writes the same slides into delivery/insight-slides/ (.pptx · .pdf · svg/)")
OPEN = ["who is it for: the people who run insight Boards, or a wider room? it decides the depth ?",
        "slide 12's example is illustrative; swap in a real Board's four Jobs once one exists ?",
        "slide 19 dates itself (2026-10-07): rebuild the deck before each showing ?",
        "one slide kit for both decks: slide_kit.py lives in b12's s61; move it to a shared place ?"]


class ExcalPen:
    """slide_kit's pen, sketched: slide units scaled by k from (ox, oy); plain ink, no colour (as b12's)."""
    cw = 0.56
    ROLE = {"ink": L.INK, "sub": SUB_INK, "mut": L.GRAY, "acc": L.INK, "border": L.GRAY, "warn": L.RED}

    def __init__(self, ox, oy, k):
        self.ox, self.oy, self.k = ox, oy, k

    def _p(self, x, y):
        return self.ox + x * self.k, self.oy + y * self.k

    def rect(self, x, y, w, h, role="border", dashed=False, sw=1, fill=None):
        px, py = self._p(x, y)
        L.base("rectangle", px, py, w * self.k, h * self.k, self.ROLE[role], sw, dashed)

    def line(self, x1, y1, x2, y2, role="border"):
        L.path([self._p(x1, y1), self._p(x2, y2)], arrow=False, color=self.ROLE[role])

    def text(self, x, y, s, fs, role="ink", bold=False, anchor="start"):
        size = round(fs * self.k, 1)
        px, py = self._p(x, y)
        wide = len(s) * size * 0.55
        px -= wide / 2 if anchor == "middle" else wide if anchor == "end" else 0
        L.text(px, py, s, size, self.ROLE[role])

    def arrow(self, pts, role="ink"):
        L.path([self._p(x, y) for x, y in pts], arrow=True, color=self.ROLE[role])


def logic_flow():
    """One box per slide, joined by the reason the next one follows; the groups bracket them."""
    fr = L.open_frame("logic flow")
    L.text(0, 0, "s61 · Insight slides: the logic first, then the slides", 30)
    words = THESIS.split()
    L.text(0, 48, "One idea runs through the deck: " + " ".join(words[:14]), 17)
    L.text(0, 72, " ".join(words[14:]), 17)
    L.text(0, 108, NOTE, 14, L.GREEN)
    x, w, h, gap, y = 300, 860, 70, 58, 170
    spans = {}
    for i, s in enumerate(SLIDES):
        L.base("rectangle", x, y, w, h, L.INK, 1.5)
        L.text(x + 18, y + 12, f"{s['n']:02d}", 20, L.GRAY)
        L.text(x + 64, y + 12, s["title"], 18, L.INK)
        kind = s["picture"][0] if s.get("picture") else "title only"
        L.text(x + 64, y + 42, f"picture: {kind}  ·  from {s['src']}", 13, L.TEAL)
        top, bot = spans.get(s["group"], (y, y + h))
        spans[s["group"]] = (min(top, y), y + h)
        if s.get("lead") and i < len(SLIDES) - 1:
            L.path([(x + 40, y + h + 4), (x + 40, y + h + gap - 4)], color=L.INK)
            L.text(x + 56, y + h + 18, s["lead"], 15, L.GRAY)
        y += h + gap
    for name, desc in GROUPS:
        top, bot = spans[name]
        L.path([(260, top + 6), (244, top + 6), (244, bot - 6), (260, bot - 6)], arrow=False, color=L.GRAY)
        L.text(0, top + 6, name, 20, L.INK)
        L.text(0, top + 34, desc, 13, L.GRAY)
    L.close_frame(fr, pad=60)
    return y


def storyboard(x0, y0):
    """Every slide at half size, three to a row, drawn by the deck's own layout."""
    fr = L.open_frame("storyboard")
    L.text(x0, y0, "storyboard: each slide as build_deck.py draws it (b12's slide_kit.py), at half size", 24)
    k, sw, sh, cg, rg = 0.5, 640, 360, 70, 130
    for i, s in enumerate(SLIDES):
        sx, sy = x0 + (i % 3) * (sw + cg), y0 + 70 + (i // 3) * (sh + rg)
        L.text(sx, sy - 4, f"{s['n']:02d} · {s['slug']}", 15, L.GRAY)
        L.base("rectangle", sx, sy + 22, sw, sh, L.INK, 1.5)
        K.draw_slide(ExcalPen(sx, sy + 22, k), s)
        L.text(sx, sy + sh + 32, f"from {s['src']}", 13, L.TEAL)
    L.close_frame(fr, pad=60)


def open_points(y0):
    fr = L.open_frame("open")
    L.text(0, y0, "open", 22, L.RED)
    for i, line in enumerate(OPEN):
        L.text(0, y0 + 40 + i * 28, line, 15, L.RED)
    L.close_frame(fr, pad=60)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s61-insight-slides.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    bottom = logic_flow()
    open_points(bottom + 120)
    storyboard(1360, 0)
    canvas.write(out, list(L.els), "build_s61_insight_slides.py")


if __name__ == "__main__":
    main()
