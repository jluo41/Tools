"""s02 · The theme matrix: s02-theme-matrix.excalidraw, drawn by this builder from disk (haipipe-studio).

The seven themes side by side: each theme's Block, its skills, its workbench server, and which of the shared
studio topics its Block has drawn (s01 or consolidated s05 ladder, s11 · s12 · s13 the three levels, s21 runs and skills, s31 Guide,
s32 element UI, s33 UI issues), with its question count. A gap is red: the place where a theme has not yet drawn
what the others have (Q02 "Does every theme follow one ladder?"). A rebuild keeps whatever a person drew.

    python build_s02_theme_matrix.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(BLOCK.parent / "_build"))
from mapdraw import GREEN, Sheet  # noqa: E402

TK = BLOCK.parents[1] / "plugins" / "haipipe-toolkit"
TOPICS = ("s01", "s11", "s12", "s13", "s21", "s31", "s32", "s33")
CHANGES = [("261010", "Read the seven independent Theme Blocks b11–b17.")]                                          # (YYMMDD, what changed): a green note each


def row(block: Path):
    theme = block.name.split("_", 2)[-1]
    studio = {p.name[:3] for p in (block / "studio").iterdir() if p.is_dir()} if (block / "studio").is_dir() else set()
    skills = sum(1 for _ in (TK / "skills/2_theme" / theme).rglob("SKILL.md"))
    server = "yes" if (TK / "servers" / f"workbench-{theme}").is_dir() else "? none"
    reports = len([p for p in (block / "reports").iterdir() if p.is_dir()]) if (block / "reports").is_dir() else 0
    marks = ["✓" if t in studio or (t == "s01" and "s05" in studio) else "?" for t in TOPICS]
    return [theme, block.name, str(skills), server, *marks, str(reports)], "?" in marks or server.startswith("?")


def main():
    s = Sheet()
    built = [row(j) for j in sorted(BLOCK.parent.glob("b1*_theme_*"))]
    cols = ([("theme", 130, 12), ("its Block", 220, 22), ("skills", 80, 6), ("workbench", 120, 10)]
            + [("ladder" if t == "s01" else t, 64, 6) for t in TOPICS] + [("questions", 110, 8)])
    width = sum(w for _, w, _ in cols)
    f = s.frame("1 · The theme matrix", 0, 0, width + 80, 100)
    s.text(40, 30, "s02 · The theme matrix: the seven themes, side by side", 30, f)
    s.text(40, 80, "✓ the Block has drawn that studio topic · ? not yet (red row: a theme with a gap). "
                   "ladder: s01 or s05 · s11 s12 s13 levels · s21 runs and skills · s31 Guide · s32 element UI · s33 UI issues",
           16, f)
    for i, (date, what) in enumerate(CHANGES):
        s.text(40, 112 + i * 26, f"✎ {date} {what}", 16, f, GREEN)
    gaps = {tuple(r) for r, gap in built if gap}
    y = s.table(40, 150 + len(CHANGES) * 26, cols, [r for r, _ in built], f, red=lambda r: tuple(r) in gaps)
    f["height"] = y + 40
    s.save(HERE / "s02-theme-matrix.excalidraw", "build_s02_theme_matrix.py")


if __name__ == "__main__":
    main()
