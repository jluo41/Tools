"""s12 · The Individual scope: every view of the console with one (synthetic) human selected, as shot on the fixtures,
each with what it reads on disk under it. Redraw after `_build/shoot_console.py`; a person's marks are kept.

    python build_s12_individual_scope.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import GREEN, HIDDEN, VIEWS, Sheet, header, save, screens  # noqa: E402

CHANGES = [("261009", "Q05 decided: Internal, External and Annotate (placeholders here) leave the Individual rail"),
           ("261009", "Record chart: one lane per table; Health: setting names, never paths; picker: the store's cohort")]


def main():
    s = Sheet()
    f = s.frame("1 · Individual scope · every view", 0, 0, 3 * 620 + 60, 100)
    y = header(s, f, "s12 · The Individual scope: one human, every view",
               "One synthetic glucose human selected (SynthCGM_v0 · synth-cgm-001). The rail opens a view; the patient\n"
               "card and the as-of date stay on top. Under each screen: what it reads on disk, and the route that serves it.",
               CHANGES)
    hidden = [lab for k, _, lab, _ in VIEWS if "individual" in HIDDEN.get(k, [])]
    s.text(40, y - 8, "✎ 261009 hidden at Individual (placeholders): " + " · ".join(hidden), 18, f, GREEN)
    bottom = screens(s, f, 40, y + 30, HERE / "shots",
                     [k for k, *_ in VIEWS if "individual" not in HIDDEN.get(k, [])], scope="individual")
    save(s, f, bottom, HERE / "s12-individual-scope.excalidraw", "build_s12_individual_scope.py")


if __name__ == "__main__":
    main()
