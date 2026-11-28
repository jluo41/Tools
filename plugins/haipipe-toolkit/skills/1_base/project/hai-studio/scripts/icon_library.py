"""Draw an item of a downloaded Excalidraw library by its name (hai-studio A04: a Design is pictures).

    from icon_library import item
    els += item("clipboard", "a_clip", x, y, w=120)            # scaled to 120 wide, its top-left at (x, y)
    els += item("Ideation", "a_team", x, y, h=200, lib="stick-figures-collaboration", color="#047857")

    python icon_library.py --list [words]     every item, by library; `words` keeps the names that hold them
    python icon_library.py --gallery          writes ../ref/icons/libraries.excalidraw and libraries.png: every item, named

The libraries are the `.excalidrawlib` files in `../ref/icons/libraries/` (and `../ref/icons/`), as downloaded from
the Excalidraw public libraries; where each came from is in ref/icon-libraries.md. Adding icons is adding a file
there: no function per icon. An item is shapes and lines, so it scales and takes a colour like the icons in
icons.py. Names are matched without case; a name two libraries share needs `lib=`.
"""
from __future__ import annotations

import copy
import difflib
import json
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDERS = (HERE.parent / "ref/icons/libraries", HERE.parent / "ref/icons")
POINTED = ("line", "arrow", "freedraw", "draw")


@lru_cache(maxsize=None)
def libraries(folders: tuple = FOLDERS) -> dict:
    """{library name: {item name: its elements}}, the library named by its file."""
    out = {}
    for folder in folders:
        for path in sorted(Path(folder).glob("*.excalidrawlib")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            items = {}
            for n, entry in enumerate(data.get("libraryItems") or data.get("library") or []):
                elements = entry.get("elements", []) if isinstance(entry, dict) else entry
                name = (entry.get("name") if isinstance(entry, dict) else "") or f"item {n + 1}"
                while name in items:                              # two items of one name: the later gets a number
                    name += " 2"
                items[name] = [e for e in elements if not e.get("isDeleted")]
            out.setdefault(path.stem, items)
    return out


def names(words: str = "", folders: tuple = FOLDERS) -> list[tuple[str, str]]:
    """[(library, item name)] in library order; `words` keeps the names that hold them."""
    return [(lib, name) for lib, items in libraries(folders).items() for name in items
            if words.casefold() in name.casefold()]


def _box(elements: list) -> tuple[float, float, float, float]:
    xs, ys = [], []
    for e in elements:
        if e.get("type") in POINTED and e.get("points"):
            xs += [e["x"] + p[0] for p in e["points"]]
            ys += [e["y"] + p[1] for p in e["points"]]
        else:
            xs += [e["x"], e["x"] + e.get("width", 0)]
            ys += [e["y"], e["y"] + e.get("height", 0)]
    return min(xs), min(ys), max(xs), max(ys)


def find(name: str, lib: str | None = None, folders: tuple = FOLDERS) -> list:
    """The elements of the named item; KeyError with the nearest names when there is none or it is ambiguous."""
    hits = [(k, items[n]) for k, items in libraries(folders).items() if lib in (None, k)
            for n in items if n.casefold() == name.casefold()]
    if len(hits) == 1 or (hits and lib):
        return hits[0][1]
    if hits:
        raise KeyError(f"{name!r} is in several libraries ({', '.join(k for k, _ in hits)}); pass lib=")
    near = difflib.get_close_matches(name, [n for _, n in names(folders=folders)], 5, 0.5)
    raise KeyError(f"no library item named {name!r}" + (f"; near: {', '.join(near)}" if near else ""))


def item(name: str, eid: str, x: float, y: float, w: float | None = None, h: float | None = None,
         lib: str | None = None, color: str | None = None, folders: tuple = FOLDERS) -> list:
    """The item's elements with its top-left at (x, y), scaled to fit `w` and `h` (one of them is enough; neither
    keeps its size), ids `<eid>_<n>`, in one group, in `color` when given (lines and outlines; fills stay)."""
    els = copy.deepcopy(find(name, lib, folders))
    x0, y0, x1, y1 = _box(els)
    fits = [side / have for side, have in ((w, x1 - x0), (h, y1 - y0)) if side and have]
    s = min(fits) if fits else 1.0
    ids = {e["id"]: f"{eid}_{n}" for n, e in enumerate(els)}
    for e in els:
        e.update(id=ids[e["id"]], x=x + (e["x"] - x0) * s, y=y + (e["y"] - y0) * s, width=e.get("width", 0) * s,
                 height=e.get("height", 0) * s, groupIds=[eid], frameId=None, locked=False, link=None)
        if e.get("points"):
            e["points"] = [[p[0] * s, p[1] * s, *p[2:]] for p in e["points"]]
        if e.get("fontSize"):
            e["fontSize"] = e["fontSize"] * s
        e["containerId"] = ids.get(e.get("containerId")) if e.get("containerId") else e.get("containerId")
        e["boundElements"] = [dict(b, id=ids[b["id"]]) for b in e.get("boundElements") or [] if b.get("id") in ids] or None
        for end in ("startBinding", "endBinding"):
            if e.get(end):
                e[end] = None
        if color and e.get("strokeColor") not in (None, "transparent"):
            e["strokeColor"] = color
    return els


def gallery(out_dir: Path = HERE.parent / "ref/icons", cell=(210, 190), cols=10) -> Path:
    """Every item of every library on one canvas, its name under it, a library per band."""
    sys.path.insert(0, str(HERE))
    from quick_draw import TITLE, BODY, text, write
    els, y, n = [], 0, 0
    for lib, items in libraries().items():
        els += text(f"h_{n}", 0, y, lib, 30, TITLE)
        y += 60
        for k, name in enumerate(items):
            cx, cy = (k % cols) * cell[0], y + (k // cols) * cell[1]
            try:
                els += item(name, f"g{n}_{k}", cx + 20, cy, 150, 110, lib)
            except (KeyError, ValueError):
                continue
            els += text(f"g{n}_{k}_n", cx + 95, cy + 124, name[:22], 14, BODY, "center")
        y += (len(items) + cols - 1) // cols * cell[1] + 50
        n += 1
    return write(Path(out_dir) / "libraries.excalidraw", els)


if __name__ == "__main__":
    if "--gallery" in sys.argv:
        import subprocess
        made = gallery()
        subprocess.run([sys.executable, str(HERE / "render_png.py"), str(made), str(made.with_suffix(".png"))], check=True)
        print(made)
    elif "--list" in sys.argv:
        words = " ".join(a for a in sys.argv[1:] if not a.startswith("--"))
        last = None
        for lib, name in names(words):
            if lib != last:
                print(f"\n{lib}")
                last = lib
            print(f"  {name}")
    else:
        print(__doc__)
