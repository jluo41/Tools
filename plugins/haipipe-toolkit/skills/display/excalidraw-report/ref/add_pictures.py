"""Put pictures inside a built drawing (excalidraw-report rule 11, JL 261005: "some png can be put
into the excalidraw as well"): append one frame of images to the right of everything already drawn.

    python add_pictures.py <drawing.excalidraw> --base <dir> \
        --picture 'caption|path/to/a.png' [--picture 'caption|path/to/b.jpg' ...] [--frame Pictures]

A Block's make.sh runs it on the freshly built drawing, before the render, so the picture is read
from its source file on every build and a new screenshot reaches the drawing with the next make.
Paths are relative to --base (the Block folder). The long side is downscaled to at most 1600 px and
the image is stored once in the drawing's `files` as a PNG data URL; each picture gets a caption above
it and its source path in gray below. Copy this file into the Block's studio/_build/ next to the
builders that call it (each Block carries its own copy of its helpers).
"""
import argparse
import base64
import hashlib
import io
import json
import os
import random

from PIL import Image

INK, GRAY, LGRAY = "#1e1e1e", "#495057", "#adb5bd"
EM = 0.6


def element(kind, x, y, w, h, frame, **kw):
    key = "%s %s %s %s %s %s" % (kind, x, y, w, h, kw.get("text", ""))
    e = {"id": "pic-%s-%s" % (kind, hashlib.sha1(key.encode()).hexdigest()[:12]),
         "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": INK,
         "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
         "roughness": 0, "opacity": 100, "groupIds": [], "frameId": frame, "roundness": None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1790900000000, "link": None, "locked": False}
    e.update(kw)
    return e


def text(x, y, t, size, color, frame):
    return element("text", x, y, len(t) * size * EM, size * 1.25, frame, strokeColor=color, text=t, originalText=t,
                   fontSize=size, fontFamily=8, textAlign="left", verticalAlign="top", containerId=None,
                   autoResize=True, lineHeight=1.25)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("drawing")
    ap.add_argument("--picture", action="append", required=True, help="'caption|path' relative to --base")
    ap.add_argument("--base", default=".")
    ap.add_argument("--frame", default="Pictures")
    ap.add_argument("--width", type=int, default=1500)
    a = ap.parse_args()
    random.seed(11)
    doc = json.load(open(a.drawing))
    els, files = doc["elements"], doc.setdefault("files", {})
    live = [e for e in els if not e.get("isDeleted")]
    x0 = (max(e["x"] + e["width"] for e in live) + 120) if live else 0
    y0 = min(e["y"] for e in live) if live else 0
    fid_frame = "frame-pictures-" + hashlib.sha1(a.frame.encode()).hexdigest()[:8]
    new, y = [text(x0 + 60, y0 + 44, a.frame, 46, INK, fid_frame)], y0 + 112
    for item in a.picture:
        caption, sep, rel = item.partition("|")
        path = os.path.join(a.base, rel.strip())
        if not sep or not os.path.isfile(path):
            raise SystemExit(f"--picture must be 'caption|path' naming a file under {a.base}: {item}")
        im = Image.open(path).convert("RGB")
        k = min(1.0, 1600 / max(im.size))
        if k < 1:
            im = im.resize((round(im.width * k), round(im.height * k)))
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        raw = buf.getvalue()
        fid = hashlib.sha1(raw).hexdigest()
        files[fid] = {"mimeType": "image/png", "id": fid, "created": 1790900000000,
                      "dataURL": "data:image/png;base64," + base64.b64encode(raw).decode()}
        w = a.width - 120
        h = w * im.height / im.width
        new.append(text(x0 + 60, y, caption.strip(), 26, INK, fid_frame))
        new.append(element("rectangle", x0 + 58, y + 44, w + 4, h + 4, fid_frame, strokeColor=LGRAY,
                           backgroundColor="#ffffff", roundness={"type": 3}))
        new.append(element("image", x0 + 60, y + 46, w, h, fid_frame, fileId=fid, status="saved", scale=[1, 1],
                           strokeColor="transparent"))
        new.append(text(x0 + 60, y + 56 + h, rel.strip(), 15, GRAY, fid_frame))
        y += h + 120
    frame = element("frame", x0, y0, a.width, y - y0, None, id=fid_frame, name=a.frame, strokeColor="#bbbbbb")
    doc["elements"] = els + [frame] + new
    json.dump(doc, open(a.drawing, "w"), indent=1)
    print(f"added {len(a.picture)} picture(s) in frame '{a.frame}' to {os.path.basename(a.drawing)}")


if __name__ == "__main__":
    main()
