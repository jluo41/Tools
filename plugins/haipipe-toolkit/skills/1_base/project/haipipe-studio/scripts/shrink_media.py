"""Shrink a folder's Studio media in place, to the sizes the builders now write (haipipe-studio; JL 261013).

    python shrink_media.py <folder> [--dry]

Three kinds, each only when it is bigger than the target:
  topic preview  <topic>/<topic>.png        -> render_png.save_preview: 2400 px wide, 256-colour palette
  transcript     assets/*-transcript-p*.jpg -> 96 dpi (0.48x of the old 200 dpi), JPEG q50
  drawing        *.excalidraw               -> each embedded JPEG at most 800 px wide, q50 (kept if it saves <20%)
A drawing keeps every element, so a person's marks are untouched; only its picture bytes get smaller.
"""
import base64
import io
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from render_png import PREVIEW_W, save_preview  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
EMBED_W, Q = 800, 50


def jpeg(im, w):
    if im.width > w:
        im = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=Q, optimize=True, progressive=True)
    return buf.getvalue()


def preview(p, dry):
    with Image.open(p) as im:
        if im.mode == "P" and im.width <= PREVIEW_W:
            return 0
        im = im.convert("RGB")
    before = p.stat().st_size
    if not dry:
        save_preview(im, p)
    return before - (p.stat().st_size if not dry else before)


def transcript(p, dry):
    with Image.open(p) as im:
        if im.width < 1600:          # already shrunk (96 dpi)
            return 0
        data = jpeg(im, round(im.width * 96 / 200))
    before = p.stat().st_size
    if not dry:
        p.write_bytes(data)
    return before - len(data)


def drawing(p, dry):
    doc = json.loads(p.read_text())
    saved = 0
    for f in doc.get("files", {}).values():
        url = f.get("dataURL", "")
        if not url.startswith("data:image/") or ";base64," not in url:
            continue
        raw = base64.b64decode(url.split(",", 1)[1])
        with Image.open(io.BytesIO(raw)) as im:
            if im.format != "JPEG":            # a real png (a crisp formula) stays as it is
                continue
            data = jpeg(im, EMBED_W)
        if len(data) < 0.8 * len(raw):         # already small (an earlier pass) stays as it is
            f["mimeType"] = "image/jpeg"       # task_drawing once labelled its jpeg pages image/png
            f["dataURL"] = "data:image/jpeg;base64," + base64.b64encode(data).decode()
            saved += (len(raw) - len(data)) * 4 // 3
    if saved and not dry:
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=1))
    return saved


def main(root, dry=False):
    total = {"preview": [0, 0], "transcript": [0, 0], "drawing": [0, 0]}
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        kind = ("preview" if p.suffix == ".png" and p.stem == p.parent.name else
                "transcript" if p.suffix == ".jpg" and p.parent.name == "assets" and "-transcript-p" in p.name else
                "drawing" if p.suffix == ".excalidraw" else None)
        if kind:
            s = {"preview": preview, "transcript": transcript, "drawing": drawing}[kind](p, dry)
            if s > 0:
                total[kind][0] += 1
                total[kind][1] += s
    for k, (n, s) in total.items():
        print(f"{k:10s} {n:5d} files  {s / 1e6:8.1f} MB {'would be ' if dry else ''}saved")


if __name__ == "__main__":
    main(Path(sys.argv[1]), "--dry" in sys.argv)
