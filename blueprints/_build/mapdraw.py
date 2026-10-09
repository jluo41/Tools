"""The blueprint Blocks' shared drawing helpers: frames, text, lines and lines-only tables, written through
haipipe-studio's canvas.write (a person's marks are kept on every rebuild).

Used by each Block's map topics (b01 s01 · s02, b02 s01, b03 s01). A builder makes a Sheet, draws, and saves:

    sheet = Sheet()
    f = sheet.frame("1 · the map", 0, 0, 1600, 900)
    sheet.text(40, 30, "title", 34, f)
    y = sheet.table(40, 120, [("column", 300, 30), ...], rows, f)
    sheet.save(HERE / "sNN-x.excalidraw", "build_sNN_x.py")
"""
import sys
import textwrap
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED, GREEN = canvas.INK, canvas.RED, canvas.GREEN
LINE = 28                                           # one text line's height at 16 px, with room to spare


class Sheet:
    def __init__(self):
        self.els = []
        self.files = {}

    def image(self, path, x, y, w, frame=None, px=900, border=True):
        """A screenshot, embedded small: resized to at most `px` wide and stored as JPEG (quality 72), so a drawing
        with many shots stays a few MB. Returns its drawn height. A missing file draws nothing and returns 0."""
        import base64
        import hashlib
        import io
        from PIL import Image
        path = Path(path)
        if not path.is_file():
            return 0
        im = Image.open(path).convert("RGB")
        if im.width > px:
            im = im.resize((px, round(im.height * px / im.width)))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=72, optimize=True)
        raw = buf.getvalue()
        fid = hashlib.sha1(raw).hexdigest()[:20]
        self.files[fid] = {"mimeType": "image/jpeg", "id": fid, "created": 1,
                           "dataURL": "data:image/jpeg;base64," + base64.b64encode(raw).decode()}
        w = min(w, im.width)                       # never enlarge a small element: draw it at its own size
        h = im.height * w / im.width
        self._el("image", x, y, w, h, strokeColor="transparent", status="saved", fileId=fid, scale=[1, 1],
                 frameId=frame["id"] if frame else None)
        if border:
            self.box(x - 1, y - 1, w + 2, h + 2, frame)
        return h

    def _el(self, kind, x, y, w, h, **extra):
        e = {"id": f"e{len(self.els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
             "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
             "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None,
             "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
             "boundElements": [], "updated": 1, "link": None, "locked": False}
        e.update(extra)
        self.els.append(e)
        return e

    def frame(self, name, x, y, w, h):
        return self._el("frame", x, y, w, h, name=name)

    def text(self, x, y, s, size=16, frame=None, color=INK):
        lines = s.split("\n")
        return self._el("text", x, y, max(len(l) for l in lines) * size * 0.55, len(lines) * size * 1.25,
                        text=s, originalText=s, fontSize=size, fontFamily=1, textAlign="left",
                        verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25,
                        frameId=frame["id"] if frame else None, strokeColor=color)

    def line(self, x1, y1, x2, y2, frame=None, arrow=False):
        return self._el("arrow" if arrow else "line", x1, y1, x2 - x1, y2 - y1,
                        points=[[0, 0], [x2 - x1, y2 - y1]], frameId=frame["id"] if frame else None,
                        startBinding=None, endBinding=None, startArrowhead=None,
                        endArrowhead="arrow" if arrow else None, lastCommittedPoint=None)

    def box(self, x, y, w, h, frame=None):
        return self._el("rectangle", x, y, w, h, frameId=frame["id"] if frame else None)

    def table(self, x0, y0, cols, rows, frame=None, size=16, red=lambda row: False, green=lambda row: False):
        """A lines-only table: cols = [(head, width, chars per line)], rows = [[cell, ...]]; a row for which
        red(row) is true is written in red (an open point), one for which green(row) is true in green (a change
        we made). Returns the y under the last rule."""
        width = sum(w for _, w, _ in cols)
        x = x0
        for head, w, _ in cols:
            self.text(x + 8, y0, head, 18, frame)
            x += w
        y = y0 + 32
        self.line(x0, y, x0 + width, y, frame)
        for row in rows:
            wrapped = [textwrap.fill(str(c), cpl) or " " for c, (_, _, cpl) in zip(row, cols)]
            h = max(t.count("\n") + 1 for t in wrapped) * LINE + 14
            x = x0
            for t, (_, w, _) in zip(wrapped, cols):
                self.text(x + 8, y + 7, t, size, frame, RED if red(row) else GREEN if green(row) else INK)
                x += w
            y += h
            self.line(x0, y, x0 + width, y, frame)
        return y

    def save(self, out, source):
        for e in canvas.off_palette(self.els):
            print("off the studio palette:", e["type"], e.get("text", "")[:40])
        canvas.write(out, self.els, source, files=self.files)
