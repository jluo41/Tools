"""s11 · The Group scope: every view of the console with the scope toggle on Group, as shot on the fixtures, each with
what it reads on disk. Most views are still a placeholder at this scope (ScopeStub); that is what Q05 asks about.
Redraw after `_build/shoot_console.py`; a person's marks are kept.

    python build_s11_group_scope.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import RED, VIEWS, Sheet, header, save, screens  # noqa: E402

CHANGES = []                                          # (YYMMDD, what changed): a green note each


def main():
    s = Sheet()
    f = s.frame("1 · Group scope · every view", 0, 0, 3 * 620 + 60, 100)
    y = header(s, f, "s11 · The Group scope: the cohort, every view",
               "Scope toggle on Group (the dataset's whole cohort). Only Case (cases across humans) and Annotate (the labeling\n"
               "forge) are built; Raw, Source, Record, Internal, External, Model and Checklist show the placeholder that says\n"
               "what they will hold here; Tasks shows nothing until INLAB_PROJECTS_ROOT is mounted; Health is the same at both.",
               CHANGES)
    s.text(40, y - 8, "? seven placeholders at Group: build each, or drop it from the Group rail (Q05)", 18, f, RED)
    bottom = screens(s, f, 40, y + 30, HERE / "shots", [k for k, *_ in VIEWS])
    save(s, f, bottom, HERE / "s11-group-scope.excalidraw", "build_s11_group_scope.py")


if __name__ == "__main__":
    main()
