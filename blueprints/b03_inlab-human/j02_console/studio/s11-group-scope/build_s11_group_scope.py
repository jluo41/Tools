"""s11 · The Group scope: every view of the console with the scope toggle on Group, as shot on the fixtures, each with
what it reads on disk. A view that is only a placeholder at this scope is hidden there (Q05, decided 261009) and
listed, not drawn.
Redraw after `_build/shoot_console.py`; a person's marks are kept.

    python build_s11_group_scope.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import GREEN, HIDDEN, VIEWS, Sheet, header, save, screens  # noqa: E402

CHANGES = [("261009", "Q05 decided: the seven placeholders leave the Group rail"),
           ("261009", "Case lists the case set's cases; Tasks reads the Block · Job · Task ladder")]


def main():
    s = Sheet()
    f = s.frame("1 · Group scope · every view", 0, 0, 3 * 620 + 60, 100)
    y = header(s, f, "s11 · The Group scope: the cohort, every view",
               "Scope toggle on Group (the dataset's whole cohort). The rail lists only what is built here: Case (the case\n"
               "set's cases across humans), Tasks (the cohort-level Tasks on the ladder), Annotate (the labeling forge) and\n"
               "Health. A view comes back to the Group rail the day it is built.",
               CHANGES)
    hidden = [lab for k, _, lab, _ in VIEWS if "group" in HIDDEN.get(k, [])]
    s.text(40, y - 8, "✎ 261009 hidden at Group (placeholders): " + " · ".join(hidden), 18, f, GREEN)
    bottom = screens(s, f, 40, y + 30, HERE / "shots", [k for k, *_ in VIEWS if "group" not in HIDDEN.get(k, [])],
                     scope="group")
    save(s, f, bottom, HERE / "s11-group-scope.excalidraw", "build_s11_group_scope.py")


if __name__ == "__main__":
    main()
