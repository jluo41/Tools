"""A display unit's picture as a reader meets it (must-check M-D18): the typeset float, the figure or table with its
caption, never a caption rebuilt in HTML.

    float_source(unit, run_dir)  the PDF to show: the unit's float.pdf (float.tex alone, cropped tight; written by
                                 hai-paper-evidence scripts/preview_display.py), else the display Run's
                                 result/float.pdf, else the unit's preview.pdf (its page 1 is the float on a paper page)
    float_png(pdf)               that PDF's page 1 as PNG: a float.pdf whole; a preview.pdf cut to its float (no
                                 running header, no page number, no wide margins). Cached outside the paper folders.

Rasterizers, in order: PyMuPDF (fitz) when importable, else poppler's pdftoppm. Without either, None, and the caller
falls back to the unit's preview.png or assets/figure.png.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

DPI = 170
BAND = 0.08                       # a page's top and bottom band: a running header, a page number
PAD = 4                           # points of white kept around the float
CACHE = Path(tempfile.gettempdir()) / "hai-float-cache"
NAMES = ("float.pdf", "preview.pdf")


def _fitz():
    try:
        import pymupdf as fitz            # noqa: F401
        return fitz
    except ImportError:
        try:
            import fitz                   # noqa: F401
            return fitz if hasattr(fitz, "open") else None
        except ImportError:
            return None


def _pdftoppm() -> str:
    return shutil.which("pdftoppm") or next((x for x in ("/opt/homebrew/bin/pdftoppm", "/usr/local/bin/pdftoppm",
                                                         "/usr/bin/pdftoppm") if Path(x).is_file()), "")


def can_rasterize() -> bool:
    return bool(_fitz() or _pdftoppm())


def run_dir(manifest, source: str):
    """The display Run's result/ a Result's `source:` names (a path from the Board, which sits above the Result)."""
    if not source or ".." in Path(source).parts or Path(source).is_absolute():
        return None
    return next((p / source for p in Path(manifest).resolve().parents if (p / source).is_dir()), None)


def float_source(unit, run=None):
    """float.pdf in the unit, else in its Run's result/, else the unit's preview.pdf; None when it has none."""
    for p in (Path(unit) / "float.pdf", Path(run) / "float.pdf" if run else None, Path(unit) / "preview.pdf"):
        if p is not None and p.is_file():
            return p
    return None


def float_png(pdf):
    """Page 1 of `pdf` (a float.pdf or a preview.pdf) as a PNG file in the cache; None when it cannot be made."""
    pdf = Path(pdf)
    try:
        stamp = pdf.stat().st_mtime_ns
    except OSError:
        return None
    if pdf.name not in NAMES:
        return None
    key = hashlib.sha1(str(pdf.resolve()).encode()).hexdigest()[:16]      # a cache name only, never shown on a page
    out = CACHE / f"{key}-{stamp}.png"
    if out.is_file():
        return out
    try:
        CACHE.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    tmp = CACHE / f"{key}-{stamp}.{os.getpid()}"
    whole = pdf.name == "float.pdf"
    try:
        made = _by_fitz(pdf, Path(f"{tmp}.png"), whole) if _fitz() else _by_pdftoppm(pdf, tmp, whole)
        if made and made.is_file():
            os.replace(made, out)
            for old in CACHE.glob(f"{key}-*.png"):       # an older render of the same file
                if old != out:
                    old.unlink(missing_ok=True)
            return out
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError):
        pass
    finally:
        for left in CACHE.glob(f"{tmp.name}*"):
            left.unlink(missing_ok=True)
    return None


def _by_fitz(pdf: Path, out: Path, whole: bool):
    fitz = _fitz()
    with fitz.open(str(pdf)) as doc:
        page = doc[0]
        clip = None if whole else _clip(fitz, page)
        page.get_pixmap(dpi=DPI, clip=clip).save(str(out))
    return out


def _clip(fitz, page):
    """The float on a paper page: its drawings, images and text, less the top and bottom bands, padded."""
    w, h = page.rect.width, page.rect.height
    band = fitz.Rect(0, h * BAND, w, h * (1 - BAND))
    r = fitz.Rect()
    rects = [d["rect"] for d in page.get_drawings() if not (d.get("fill") in ((1, 1, 1), (1.0, 1.0, 1.0)) and not d.get("color"))]
    rects += [fitz.Rect(i["bbox"]) for i in page.get_image_info()]
    rects += [fitz.Rect(b[:4]) for b in page.get_text("blocks")]
    for x in rects:
        x = x & band
        if not x.is_empty:
            r |= x
    return None if r.is_empty else (r + (-PAD, -PAD, PAD, PAD)) & page.rect


def _by_pdftoppm(pdf: Path, tmp: Path, whole: bool):
    tool = _pdftoppm()
    if not tool:
        return None
    base = [tool, "-f", "1", "-l", "1", "-singlefile"]
    crop = []
    if not whole:
        box = _ink_box(tool, pdf, tmp)
        if box:
            k = DPI / 50
            x0, y0, x1, y1 = box
            pad = PAD / 72 * DPI
            x, y = max(0, int(x0 * k - pad)), max(0, int(y0 * k - pad))
            crop = ["-x", str(x), "-y", str(y), "-W", str(int((x1 + 1) * k + pad) - x), "-H", str(int((y1 + 1) * k + pad) - y)]
    subprocess.run(base + ["-png", "-r", str(DPI)] + crop + [str(pdf), str(tmp)], capture_output=True, timeout=120)
    return Path(f"{tmp}.png")


def _ink_box(tool: str, pdf: Path, tmp: Path):
    """Where the ink is on page 1 at 50 dpi, the top and bottom bands left out: (x0, y0, x1, y1) in pixels."""
    stem = Path(f"{tmp}-ink")
    subprocess.run([tool, "-f", "1", "-l", "1", "-singlefile", "-gray", "-r", "50", str(pdf), str(stem)],
                   capture_output=True, timeout=120)
    pgm = Path(f"{stem}.pgm")
    if not pgm.is_file():
        return None
    data = pgm.read_bytes()
    m = re.match(rb"P5\s+(\d+)\s+(\d+)\s+(\d+)\s", data)
    if not m:
        return None
    w, h = int(m.group(1)), int(m.group(2))
    px = data[m.end():]
    top, bottom = int(h * BAND), int(h * (1 - BAND))
    rows, x0, x1 = [], w, -1
    light = bytes(range(240, 256))
    for y in range(top, bottom):
        row = px[y * w:(y + 1) * w]
        ink = row.rstrip(light)
        if not ink:
            continue
        rows.append(y)
        x0 = min(x0, len(row) - len(row.lstrip(light)))
        x1 = max(x1, len(ink) - 1)
    return (x0, rows[0], x1, rows[-1]) if rows else None


def alt_text(tex: str) -> str:
    """A caption's words for an image's alt only: LaTeX escapes read as their characters (\\% is %), commands and
    math marks dropped. Never shown as a caption."""
    t = re.sub(r"\\(?:textbf|textit|emph|mathrm|text|textsc|underline)\{([^{}]*)\}", r"\1", tex or "")
    t = re.sub(r"\\([%&#_$])", lambda m: {"$": "\0"}.get(m.group(1), m.group(1)), t)
    t = re.sub(r"\\[,;:! ]", " ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", t).replace("~", " ")
    return " ".join(re.sub(r"[{}$]", "", t).replace("\0", "$").split())
