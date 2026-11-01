"""b35-s05:studio @ studio_gallery, its drawing: the five parts (haipipe-studio scripts/five_parts.py) with s05's own
facts, and its Design: where the sNN sit today, counted by gallery_scan.py on every rebuild, and the catalogue of sNN
kinds (b35-s01's sketch F1 until 261030; JL 261030: "we might also have a sNN for the gallery of the deliveries, and
gallery of the studios, as the new sNN")."""
import collections
import sys
from pathlib import Path

STUDIO_SKILL = Path("/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio")
sys.path.insert(0, str(STUDIO_SKILL / "scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402,F401  (underscore names skip the star import)
import five_parts  # noqa: E402
import gallery_scan  # noqa: E402

HERE = Path(__file__).resolve().parent
ROWS_ = gallery_scan.studios()
SPACES = collections.Counter(r["space"] for r in ROWS_)
_gal = STUDIO_SKILL / "ref" / "gallery.md"
_g = _gal.read_text(encoding="utf-8") if _gal.is_file() else ""
SPEC = {
    "title": "The studio gallery: every kind of sNN, a real one each",
    "why": {"question": "why do we need s05?",
            "notes": [f"{len(ROWS_)} sNN in\n{len(SPACES)} SPACEs, no place\nto see them", "a new sNN\nstarts from\nnothing",
                      "s01's gallery\nwas a side\nsketch"],
            "quote": "JL 261030: \u201cwe might also have a sNN for ... gallery of the studios\u201d"},
    "what": {"head": "\u2461 what s05 hands over: one skill page", "icon": "book", "name": "haipipe-studio/", "type": "skill",
             "deck_why": "stays in s05's delivery/deck/, so anyone gets it in a minute",
             "parts": [  # (icon, file: part, what it is: why, on disk now)
                 ("doc", "ref/gallery.md: one real sNN per kind", "so a new sNN copies a good one", "## Each kind of sNN" in _g),
                 ("doc", "ref/gallery.md: where they sit", "how many, by level and Theme", "## Where they sit" in _g),
                 ("code", "scripts/gallery_scan.py: finds every sNN", "so the gallery is counted, never typed",
                  (STUDIO_SKILL / "scripts/gallery_scan.py").is_file())]},
    "job": None,
    "target": "haipipe-studio ref/gallery.md",
}
LEVELS = ["Project", "Block", "Job", "Task"]
THEMES = ["work", "paper", "discovery", "cowork", "insight", "design", "labeling", "project"]


def where_they_sit(x, y):
    """A: the scan, as a table: a row per level, a column per Theme, the count in each cell."""
    els = text("skA", x, y, f"A \u00b7 where the {len(ROWS_)} sNN sit today", 18, TITLE)
    els += shapes("skA_s", x, y + 26, "ref/gallery.md: where they sit")
    n = collections.Counter((r["level"], r["theme"]) for r in ROWS_)
    W, top = 88, y + 80
    for c, th in enumerate(THEMES):
        els += text(f"gA_c{c}", x + 110 + c * W + W / 2, top, th, 13, BODY, "center")
    for r, lv in enumerate(LEVELS):
        ry = top + 30 + r * 38
        els += text(f"gA_r{r}", x, ry + 6, lv, 15, PU)
        els += line(f"gA_rl{r}", [(x, ry - 4), (x + 110 + W * len(THEMES), ry - 4)], GHOST, 1)
        for c, th in enumerate(THEMES):
            k = n[(lv, th)]
            els += text(f"gA_{r}_{c}", x + 110 + c * W + W / 2, ry + 4, str(k) if k else "\u00b7", 17 if k else 13,
                        INK if k else ROOM, "center")
    y2 = top + 30 + len(LEVELS) * 38 + 10
    side = sum(r["beside"] for r in ROWS_)
    els += text("gA_side", x, y2, f"{side} sit beside their Jobs \u00b7 {len(ROWS_) - side} still in a studio/ folder", 14, OR)
    els += text("gA_sp", x, y2 + 26, " \u00b7 ".join(f"{s} {k}" for s, k in SPACES.most_common()), 13, BODY)
    els += text("gA_note", x, y2 + 50, "counted by gallery_scan.py, folder names only \u00b7 redrawn every time", 12, ROOM)
    return els, y2 + 80


def catalogue(dy):
    """B: each kind of sNN at its level, a real one each, and what it hands over (b35-s01's sketch F1 until 261030)."""
    els = []
    #   the catalogue of sNN kinds, by level (kept as drawn in b35-s01)
    CX = 720
    els += text("skB", CX - 30, 430, "B \u00b7 each kind of sNN, by level and Theme: what it hands over", 18, TITLE)
    els += i_slides("all_deck", CX + 10, 512) + text("all_t", CX + 70, 500, "every sNN: a deck, always", 18, OR)
    def i_label(eid, x, y, c=NAVY):
        """A label: a tag."""
        return poly(eid, [(x, y + 6), (x + 30, y + 6), (x + 44, y + 20), (x + 30, y + 34), (x, y + 34)], c, "#fff3bf")


    # labeling's own sNN (JL 261030: "for the Labeling, it should have many"; b15 s13: a labeling Job is one dataset ×
    # one label, its Tasks one of five types)
    LAB = "Physician dices350"
    # each row's Theme (JL 261030: "could you say what are the theme they are?"), drawn as one brace per Theme below;
    # the line under a row is the SPACE and the sNN folder, checked on disk 261030
    def i_bulb(eid, x, y):
        """An idea, small: a lit bulb."""
        return bulb(eid, x + 22, y + 14, 13)


    THEME = {"design": ("#c2255c", "#fff0f6"), "work": ("#1864ab", "#e7f5ff"), "paper": ("#d9480f", "#fff4e6"), "labeling": ("#8a6d00", "#fff3bf"),
             "cowork": ("#7048e8", "#f3f0ff"), "insight": ("#0b7285", "#e3fafc")}
    ROWS = [("Block", "the design question", [
                (i_book, "story", "paper", "DrFirst s02-story-insight-carryover", i_doc, "story, Section plan"),
                (i_lens, "question map", "insight", "WellDoc Prototype-b02-CGMPerson", i_page, "the questions + their scripts"),
                (i_code, "skill design", "work", "Tools b35 s02-studio-pages", i_doc, "skill, tool change"),
                (i_mail, "ask", "cowork", "Physician s01-cir-medicare-claims", i_mail, "letter, meeting note"),
                (i_flow, "design goals", "design", "WellDoc Design-PreVisitChecklist", i_doc, "signed goals, rules, inputs")]),
            ("Job", "how its Tasks fit", [
                (i_flow, "run plan", "paper", "DrFirst s04-paper-workflow", i_code, "server package, code"),
                (i_grid, "table contract", "work", "Tools b03 j02 s13-case-builder", i_grid, "data table"),
                (i_papers, "paper version", "paper", "Physician Paper-AgreeableOpioid-Jama j01_v1130", i_papers, "full paper, Word + PDF"),
                (i_label, "label contract", "labeling", LAB + " j01_dices350_response_safety", i_doc, "schema.yaml + label contract"),
                # insight (haipipe-insight): a Prototype Job is one release, a Board Job one release on one data freeze
                (i_flow, "analysis plan", "insight", "WellDoc Prototype-b02 j01_p1_first-ladder", i_doc, "a signed release"),
                (i_grid, "release on a freeze", "insight", "WellDoc Insight-S1023 j01_p1_s1023v1", i_page, "each question answered"),
                # design (haipipe-design): one goal x one method version x one inputs version -> N designs
                (i_flow, "design Job", "design", "WellDoc PreVisitChecklist j02_prepare-…", i_papers, "released designs.json")]),
            ("Task", "one result to agree: a figure, a Section, a label set, an answer, a design", [
                (i_bars, "display", ("work", "paper"), "WellDoc s21-j09-manuscript-figures", i_bars, "figure"),
                (i_write, "section", "paper", "DrFirst s12-t02-literature-review", i_doc, "written Section, LaTeX + Word"),
                (i_grid, "items", "labeling", LAB + " t01_dices350_items", i_grid, "item set + sealed test"),
                (i_bars, "ground truth", "labeling", LAB + " t02_..._ground_truth_profile", i_bars, "the dataset's own labels, fenced"),
                (i_label, "building", "labeling", LAB + " t03 (building side)", i_doc, "signed Label Handoff"),
                (i_lens, "scanning", "labeling", LAB + " t03 (scanning side)", i_label, "final labels + audit"),
                (i_bars, "score", "labeling", "Tools b15 s13 · its score Task", i_bars, "score against the gold"),
                # insight: a Task is one question at one level (JL 261030: "how about the insights and the design?")
                (i_grid, "Data level", "insight", "WellDoc S1023 t01_D01_extract-and-clock", i_grid, "what the data holds"),
                (i_bars, "Information level", "insight", "WellDoc S1023 t05_I01_glucose-control", i_bars, "rates, contrasts in a cut"),
                (i_book, "Knowledge level", "insight", "WellDoc S1023 t10_K01_control-and-timing", i_doc, "what holds across cuts"),
                (i_bulb, "Wisdom level", "insight", "WellDoc S1023 t15_W01_first-focus", i_doc, "signed counsel for Design"),
                # design: three Task types in every design Job ("for the design, there are should be different types of tasks")
                (i_bulb, "reason ideas", "design", "WellDoc PreVisitChecklist j02 t00_reason-ideas", i_doc, "ideas.yaml, one per design"),
                (i_page, "one design", "design", "WellDoc PreVisitChecklist j02 t07_d07_bring-to-…", i_page, "a draft that passed verify"),
                (i_bars, "review whole", "design", "WellDoc PreVisitChecklist j02 t99_review-whole", i_bars, "ranking, an effect each")])]
    SRC = {"question map": NAVY, "skill design": NAVY, "design goals": PU, "analysis plan": PU, "release on a freeze": NAVY,
           "design Job": PU, "Data level": NAVY, "Information level": YE, "one design": NAVY, "review whole": YE, "label contract": NAVY, "items": NAVY, "ground truth": YE, "building": NAVY, "score": YE, "paper version": NAVY, "section": NAVY, "story": OR, "question": NAVY, "table contract": NAVY, "display": YE, "run plan": PU, "design": NAVY, "ask": NAVY}
    y, i = 560, 0
    for rung, what, rows in ROWS:                       # each kind on its natural rung (JL 261030: "block level, job level, and task level?")
        els += line(f"rung_{rung}", [(CX - 30, y + 14), (CX + 700, y + 14)], ROOM, 1, True)
        els += text(f"rung_{rung}_t", CX - 30, y - 8, f"{rung} · {what}", 15, PU)
        y += 34
        order = list(dict.fromkeys(r[2] for r in rows))   # rows of one Theme sit together under one brace
        for theme in order:
            top = y
            for icon, kind, _, eg, dicon, dname in [r for r in rows if r[2] == theme]:
                els += icon(f"k{i}", CX, y) if icon in (i_book, i_lens, i_bulb) else icon(f"k{i}", CX, y, PU if icon is i_flow else SRC[kind])
                els += text(f"k{i}_t", CX + 62, y - 2, kind, 18, TITLE) + text(f"k{i}_eg", CX + 62, y + 22, eg, 12, BODY)
                els += arrow(f"k{i}_a", [(CX + 400, y + 16), (CX + 470, y + 16)], GR)
                els += dicon(f"d{i}", CX + 480, y, GR) if dicon is i_papers else dicon(f"d{i}", CX + 480, y)
                els += text(f"d{i}_t", CX + 540, y + 6, dname, 17, GR)
                y, i = y + 62, i + 1
            # one brace per Theme, its name once at the tip (JL 261030: "what I mean is you can add this one", a brace
            # drawn over the five labeling rows)
            # a kind in two Themes keeps one brace with both names (JL 261030: "display is also like the paper things, we
            # can also treat it as the work, both works")
            names = theme if isinstance(theme, tuple) else (theme,)
            ink, a, b = (THEME[names[0]][0] if len(names) == 1 else INK), top - 4, y - 18
            mid, bx = (a + b) / 2, CX - 14
            els += line(f"br_{rung}_{'_'.join(names)}", [(bx, a), (bx - 7, a + 8), (bx - 7, mid - 7), (bx - 14, mid), (bx - 7, mid + 7),
                                              (bx - 7, b - 8), (bx, b)], ink, 2)
            for n, name in enumerate(names):
                w, ny = len(name) * 15 * 0.62, mid - 10 + (n - (len(names) - 1) / 2) * 20
                els += text(f"br_{rung}_{'_'.join(names)}_t{n}", bx - 20 - w, ny, name, 15, THEME[name][0])
        y += 18
    els += sticky("ask_kinds", 900, y + 40, 230, 70, "? are these\nthe kinds", 16, -0.05, RED, RE)
    els += sticky("ask_rung", 1230, y + 45, 300, 70, "? is each kind on\nits right level", 16, 0.04, RED, RE)

    for e in els:
        e["y"] += dy
    return els + shapes("skB_s", 690, 456 + dy, "ref/gallery.md: one real sNN per kind")


def design():
    els, bottom = where_they_sit(690, 280)
    els += sticky("ask_studio", 1700, 420, 300, 70, "? move the studio/ ones\nbeside their Jobs", 15, 0.03, RED, RE)
    return els + catalogue(bottom - 380)


if __name__ == "__main__":
    print(gallery_scan.write(HERE, "studio"))       # the delivery, the newest of each kind (JL 261030: "go ahead and do it")
    five_parts.build(HERE, SPEC, design)
