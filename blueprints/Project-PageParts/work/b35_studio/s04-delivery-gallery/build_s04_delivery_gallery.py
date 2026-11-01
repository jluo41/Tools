"""b35-s04:studio @ delivery_gallery, its drawing: the five parts (haipipe-studio scripts/five_parts.py) with s04's own
facts, and its Design: the kinds of delivery on disk and whose they are, counted by haipipe-studio's gallery_scan.py on
every rebuild, and the kinds of Block (b35-s01's sketch F2 until 261030; JL 261030: "we might also have a sNN for the
gallery of the deliveries, and gallery of the studios, as the new sNN")."""
import collections
import sys
from pathlib import Path

STUDIO_SKILL = Path("/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio")
DELIVERY_SKILL = STUDIO_SKILL.parent / "haipipe-delivery"
sys.path.insert(0, str(STUDIO_SKILL / "scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402  (underscore names skip the star import)
import five_parts  # noqa: E402
import gallery_scan  # noqa: E402

HERE = Path(__file__).resolve().parent
ROWS_ = gallery_scan.deliveries()
KIND = collections.Counter(r["kind"] for r in ROWS_)
_gal = DELIVERY_SKILL / "ref" / "gallery.md"
_g = _gal.read_text(encoding="utf-8") if _gal.is_file() else ""
SPEC = {
    "title": "The delivery gallery: every kind of delivery, a real one each",
    "why": {"question": "why do we need s04?",
            "notes": [f"{len(ROWS_)} delivery/\nfolders, never\nside by side", f"{KIND['empty']} are empty,\n{KIND['deck']} hold a deck",
                      "a new one can't\nsee what a good\ndelivery looks like"],
            "quote": "JL 261030: \u201cwe might also have a sNN for the gallery of the deliveries\u201d"},
    "what": {"head": "\u2461 what s04 hands over: one skill page", "icon": "book", "name": "haipipe-delivery/", "type": "skill",
             "deck_why": "stays in s04's delivery/deck/, so anyone gets it in a minute",
             "parts": [  # (icon, file: part, what it is: why, on disk now)
                 ("doc", "ref/gallery.md: one real delivery per kind", "so a new delivery copies a good one", "## Each kind of delivery" in _g),
                 ("doc", "ref/gallery.md: whose delivery", "a Page's, a Task's, a Block's, an sNN's", "## Whose delivery" in _g),
                 ("code", "haipipe-studio gallery_scan.py: finds each", "so the gallery is counted, never typed",
                  (STUDIO_SKILL / "scripts/gallery_scan.py").is_file())]},
    "job": None,
    "target": "haipipe-delivery ref/gallery.md",
}
def cut(s, n):
    """A path cut to n characters from its end, so the folder that names it stays: 'REACH …/t01_x/delivery'."""
    if len(s) <= n:
        return s
    sp, rest = s.split(" ", 1)
    return f"{sp} \u2026{rest[-(n - len(sp) - 2):]}"


COLOR = {"Word + PDF": NAVY, "LaTeX + PDF": NAVY, "PDF": NAVY, "web page": TEAL, "deck": OR, "skill": GR, "ui": GR,
         "table": PU, "figure": YE, "text": INK, "empty": RE}


def kinds(x, y):
    """A: each kind of delivery on disk, a bar for its count, and the newest one under it."""
    els = text("skA", x, y, f"A \u00b7 the kinds of delivery: {len(ROWS_)} delivery/ folders today", 18, TITLE)
    els += shapes("skA_s", x, y + 26, "ref/gallery.md: each kind of delivery")
    top, most = y + 76, max(KIND.values())
    for k, kind in enumerate(gallery_scan.KINDS):
        ry, n = top + k * 50, KIND[kind]
        els += text(f"gA_k{k}", x, ry, kind, 15, COLOR[kind] if n else ROOM)
        if n:
            els += [_el("rectangle", f"gA_b{k}", x + 130, ry + 2, max(4, 300 * n / most), 16, COLOR[kind], "#ffffff")]
        els += text(f"gA_n{k}", x + 130 + (300 * n / most if n else 0) + 10, ry, str(n) if n else "none yet", 14, INK if n else ROOM)
        eg = gallery_scan.newest(ROWS_, "kind", kind)
        if eg:
            els += text(f"gA_e{k}", x + 130, ry + 22, cut(gallery_scan.short(eg["path"], eg["space"]), 78), 11, BODY)
    yb = top + len(gallery_scan.KINDS) * 50
    els += text("gA_note", x, yb, "counted by gallery_scan.py, file names only \u00b7 the newest of each kind \u00b7 redrawn every time", 12, ROOM)
    return els, yb + 60


def whose(x, y):
    """B: whose delivery it is: a row per level, its count, the newest one."""
    els = text("skB", x, y, "B \u00b7 whose delivery it is", 18, TITLE)
    els += shapes("skB_s", x, y + 26, "ref/gallery.md: whose delivery")
    n = collections.Counter(r["whose"] for r in ROWS_)
    for k, lv in enumerate(["Page", "Task", "Job", "Block", "sNN", "Project"]):
        ry = y + 76 + k * 46
        els += text(f"gB_l{k}", x, ry, lv, 15, PU) + text(f"gB_n{k}", x + 100, ry, str(n[lv]) if n[lv] else "\u00b7", 15, INK)
        eg = gallery_scan.newest(ROWS_, "whose", lv)
        if eg:
            els += text(f"gB_e{k}", x + 150, ry + 2, cut(gallery_scan.short(eg["path"], eg["space"]), 78), 11, BODY)
    return els, y + 76 + 6 * 46


def block_kinds():
    """C: the kinds of Block and what each hands over (b35-s01's sketch F2 until 261030)."""
    els = []
    #   the kinds of Block, what each hands over, its s01 (proposed; kept as drawn in b35-s01)
    XC = 1560


    def i_net(eid, x, y, c=NAVY):
        """A model: a small network."""
        L, R = [(x + 4, y + 6), (x + 4, y + 20), (x + 4, y + 34)], [(x + 40, y + 12), (x + 40, y + 28)]
        els_ = []
        for k, a_ in enumerate(L):
            for m, b_ in enumerate(R):
                els_ += line(f"{eid}_e{k}{m}", [a_, b_], c, 1)
        return els_ + [_el("ellipse", f"{eid}_n{k}", px - 5, py - 5, 10, 10, c, SEM["plain"][0]) for k, (px, py) in enumerate(L + R)]


    def i_func(eid, x, y, c=NAVY):
        """An algorithm: a function, f(x)."""
        return [_el("rectangle", eid, x, y + 2, 46, 34, c, "#fff3bf")] + text(eid + "_glyph", x + 23, y + 9, "f(x)", 15, c, "center")


    def i_tag(eid, x, y, c=NAVY):
        return poly(eid, [(x, y + 6), (x + 30, y + 6), (x + 44, y + 20), (x + 30, y + 34), (x, y + 34)], c, "#fff3bf")


    els += text("skC", XC, 280, "C \u00b7 the kinds of Block: what each hands over (proposed)", 18, TITLE)
    els += shapes("skC_s", XC, 306, "ref/gallery.md: whose delivery, a Block's")
    els += text("skC2", XC, 334, "(309 Blocks in 8 SPACEs; their names say data ~55, model and algorithm ~39, analysis ~14, endpoint 6, tool 10)", 13, ROOM)
    BLOCKS = [(i_grid, "Data", "DrFirst b01_A_click_prediction_dataset", "dataset version + data card", "table contract"),
              (i_func, "Algorithm", "WellDoc Proj13 b01_glucodiffusion_pipeline", "algorithm code + tuner", "design · hainn L1-L2"),
              (i_net, "Model", "DrFirst b02_B_click_prediction_models", "trained model + eval report", "experiment plan · hainn L3-L4"),
              (i_bars, "Analysis", "Physician b51_jama_results_analysis", "result tables + figures", "run plan"),
              (i_page, "Endpoint", "REACH b31_endpoint_reachpd2d", "running service + its tests", "service design"),
              (i_code, "Tool", "Tools b35_studio", "skill or workbench change", "design"),
              (i_papers, "Paper", "Paper-AgreeableOpioid-Jama", "full paper, Word + PDF", "story"),
              (i_lens, "Discovery", "Physician discovery b01", "evidence synthesis + bib", "question"),
              (i_mail, "CoWork", "Physician cowork b01 IRB", "letters, meeting notes", "ask"),
              (i_tag, "Labeling", "Physician labeling", "labeled dataset + guideline", "guideline")]
    for k, (icon, name, eg, gives, kind) in enumerate(BLOCKS):
        y = 360 + k * 72
        els += icon(f"bt{k}", XC, y) if icon is i_lens else icon(f"bt{k}", XC, y, NAVY)
        els += text(f"bt{k}_n", XC + 60, y - 2, name, 18, TITLE) + text(f"bt{k}_eg", XC + 60, y + 22, eg, 12, BODY)
        els += arrow(f"bt{k}_a", [(XC + 400, y + 16), (XC + 460, y + 16)], GR)
        els += text(f"bt{k}_g", XC + 472, y - 2, gives, 16, GR) + text(f"bt{k}_k", XC + 472, y + 22, "its s01: " + kind, 13, PU)
    els += sticky("ask_type", XC + 330, 1122, 320, 70, "? every Block lists\nits ## Deliveries", 16, -0.04, RED, RE)

    return els


def design():
    """A, B and C in one column, so the Design stays left of Process."""
    els, yb = kinds(690, 280)
    more, yc = whose(690, yb)
    els += more + sticky("ask_two", 1460, 560, 300, 70, "? Word + PDF and LaTeX\n+ PDF: one kind or two", 15, 0.03, RED, RE)
    c = block_kinds()                                   # drawn at its old place in b35-s01, moved under B
    dx, dy = 690 - min(e["x"] for e in c), yc + 60 - min(e["y"] for e in c)
    for e in c:
        e["x"], e["y"] = e["x"] + dx, e["y"] + dy
    return els + c


if __name__ == "__main__":
    print(gallery_scan.write(HERE, "delivery"))       # the delivery, the newest of each kind (JL 261030: "go ahead and do it")
    five_parts.build(HERE, SPEC, design)
