"""Read one paper's PDF onto an Excalidraw canvas: its logic, its key passages shot with the quoted
words highlighted, a comment on each, and how each links to our paper (excalidraw-read).

    python read_paper.py text  <paper.pdf> --out <folder>   # paper.txt, page-marked, for reading
    python read_paper.py boxes <paper.pdf> --page N [--find s]  # each line's box in PDF points (tables, figures)
    python read_paper.py shoot <folder>/reading.yaml        # shots/<id>-p<N>.jpg, quotes highlighted
    python read_paper.py draw  <folder>/reading.yaml        # <folder>/<stem>.excalidraw + .png preview
    python read_paper.py all   <folder>/reading.yaml        # shoot, then draw

The agent reads paper.txt, writes reading.yaml (ref/reading-spec.md), then runs `all`. Needs poppler
(`pdftotext`, `pdftoppm`), Pillow and PyYAML. The drawing is written with haipipe-studio's merge-safe
`canvas.write`, so a person's marks on the canvas survive a rebuild.
"""
import argparse
import base64
import difflib
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import textwrap
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from PIL import Image, ImageChops, ImageDraw

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parents[2] / "project" / "haipipe-studio" / "scripts"   # 1_base/project/haipipe-studio
DPI = 200
HIGHLIGHT = (255, 232, 110)        # multiplied onto the page: a marker-pen yellow that keeps the ink black
NS = "{http://www.w3.org/1999/xhtml}"
RELATIONS = ("supports", "contrasts", "borrows", "cites", "gap")


# ---------------------------------------------------------------- text: what the agent reads

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"{cmd[0]} failed: {r.stderr.strip()[:300]}")
    return r.stdout


def words_of(pdf):
    """Every word with its box, by page > block > line, from `pdftotext -bbox-layout` (PDF points)."""
    xml = run(["pdftotext", "-bbox-layout", str(pdf), "-"])
    root = ET.fromstring(re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", xml))   # math fonts leak control chars
    pages = []
    for pg in root.iter(NS + "page"):
        blocks = []
        for bl in pg.iter(NS + "block"):
            lines = []
            for ln in bl.iter(NS + "line"):
                ws = [{"t": w.text or "", "b": [float(w.get(k)) for k in ("xMin", "yMin", "xMax", "yMax")]}
                      for w in ln.iter(NS + "word")]
                if ws:
                    lines.append({"b": [float(ln.get(k)) for k in ("xMin", "yMin", "xMax", "yMax")], "w": ws})
            if lines:
                blocks.append({"b": [float(bl.get(k)) for k in ("xMin", "yMin", "xMax", "yMax")], "l": lines})
        pages.append({"w": float(pg.get("width")), "h": float(pg.get("height")), "blocks": blocks})
    return pages


def cmd_text(a):
    pdf, out = Path(a.pdf).resolve(), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    layout = run(["pdftotext", "-layout", str(pdf), "-"]).split("\f")
    body = "".join(f"\n=== page {i} ===\n{p}" for i, p in enumerate(layout, 1) if p.strip())
    (out / "paper.txt").write_text(body)
    pages = words_of(pdf)
    heads = [(i, ln.strip()) for i, p in enumerate(layout, 1) for ln in p.splitlines()
             if re.match(r"^\s*(Fig(ure)?\.?|Table)\s*\d+[.:]", ln)]
    print(f"{pdf.name}: {len(pages)} pages, {sum(len(l['w']) for p in pages for b in p['blocks'] for l in b['l'])} "
          f"words -> {out / 'paper.txt'}")
    for i, h in heads[:30]:
        print(f"  p{i}: {h[:90]}")


def cmd_boxes(a):
    """Every text line of one page with its box, so a reading can give a table or figure a `crop` box and
    `mark` boxes. A table prints cell by cell; a row is the cells that share a y."""
    page = words_of(Path(a.pdf))[a.page - 1]
    print(f"page {a.page}: {page['w']:.0f} x {page['h']:.0f} pt   x0 y0 x1 y1  text")
    for bl in page["blocks"]:
        for ln in bl["l"]:
            t = " ".join(w["t"] for w in ln["w"])
            if not a.find or a.find.lower() in t.lower():
                print("  %5.0f %5.0f %5.0f %5.0f  %s" % (*ln["b"], t[:90]))


# ---------------------------------------------------------------- shoot: find, highlight, crop

def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[^0-9a-z%.]+", "", s.replace("’", "'")).strip(".")


def page_tokens(page):
    """Normalized tokens of a page in reading order, each with the words it covers. A word broken by a
    hyphen at a line end is joined to the next line's first word."""
    flat = []
    for bi, bl in enumerate(page["blocks"]):
        for li, ln in enumerate(bl["l"]):
            for wi, w in enumerate(ln["w"]):
                flat.append((w, bi, li, wi == len(ln["w"]) - 1))
    toks, i = [], 0
    while i < len(flat):
        w, bi, li, last = flat[i]
        if last and w["t"].endswith("-") and i + 1 < len(flat):
            nxt = flat[i + 1]
            toks.append((norm(w["t"][:-1] + nxt[0]["t"]), [(w, bi, li), (nxt[0], nxt[1], nxt[2])]))
            i += 2
            continue
        toks.append((norm(w["t"]), [(w, bi, li)]))
        i += 1
    return [t for t in toks if t[0]]


def find(page, quote):
    """(ratio, matched [(word, block, line)]) for the quote on this page. The match runs on characters with
    the spaces taken out, so a word the PDF splits or joins differently from paper.txt (`CI95` as `CI` + `95`,
    `behavior82,83` as two words) still matches end to end: exact first, then the closest stretch."""
    toks = page_tokens(page)
    qs = "".join(norm(x) for x in quote.split())
    if not qs or not toks:
        return 0.0, []
    text, owner = "", []
    for i, (key, _) in enumerate(toks):
        text += key
        owner += [i] * len(key)

    def words(c0, c1):                                # the tokens covering characters c0..c1-1
        return [m for t in toks[owner[c0]:owner[c1 - 1] + 1] for m in t[1]]
    at = text.find(qs)
    if at >= 0:
        return 1.0, words(at, at + len(qs))
    best, b0 = 0.0, None                              # coarse: the stretch of the same length sharing most
    probe = qs[:: max(1, len(qs) // 40)]
    for c in range(0, max(1, len(text) - len(qs) + 1), 8):
        r = difflib.SequenceMatcher(None, text[c:c + len(qs)], probe, autojunk=False).ratio() if \
            sum(ch in text[c:c + len(qs)] for ch in set(probe)) >= 0.8 * len(set(probe)) else 0
        if r > best:
            best, b0 = r, c
    if b0 is None:
        return 0.0, []
    lo, hi = max(0, b0 - 40), min(len(text), b0 + len(qs) + 40)   # fine: align the quote inside that stretch
    sm = difflib.SequenceMatcher(None, text[lo:hi], qs, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]
    if not blocks:
        return 0.0, []
    ratio = sum(b.size for b in blocks) / len(qs)
    c0, c1 = lo + blocks[0].a, lo + blocks[-1].a + blocks[-1].size
    return round(ratio, 3), words(c0, c1)


def union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


def crop_box(page, hits, crop):
    """The region to shoot, in PDF points: the quote's lines and N lines around it (default 3), the
    blocks it sits in, the whole page, or a box the reading gives (a figure)."""
    if isinstance(crop, list) and len(crop) == 4:
        return [float(v) for v in crop]
    if crop == "page":
        return [0, 0, page["w"], page["h"]]
    if crop == "block":
        return union([page["blocks"][bi]["b"] for bi in sorted({bi for _, bi, _ in hits})])
    m = re.match(r"lines:(\d+)", str(crop))
    n = int(m.group(1)) if m else 3
    hit = {(b, l) for _, b, l in hits}
    qx0, _, qx1, _ = union([page["blocks"][b]["l"][l]["b"] for b, l in hit])

    def same_column(b):                               # on a two-column page, never the other column
        return min(b[2], qx1) - max(b[0], qx0) >= 0.5 * min(b[2] - b[0], qx1 - qx0)
    col = sorted(((bi, li, ln["b"]) for bi, bl in enumerate(page["blocks"]) for li, ln in enumerate(bl["l"])
                  if (bi, li) in hit or same_column(ln["b"])), key=lambda t: (t[2][1] + t[2][3], t[2][0]))
    idx = [k for k, (bi, li, _) in enumerate(col) if (bi, li) in hit]
    lo, hi = max(0, min(idx) - n), min(len(col), max(idx) + n + 1)   # whole lines, in order of their middles
    box = union([b for _, _, b in col[lo:hi]])
    # pdftotext's line boxes overlap their neighbours by about 2 pt, so the cut between two lines is the
    # middle of the first's bottom and the next's top, never a fixed pad past the box (Matz 261010)
    top, bottom = box[1] - 3, box[3] + 3
    if lo > 0:
        top = max(top, (col[lo - 1][2][3] + box[1]) / 2)
    if hi < len(col):
        bottom = min(bottom, (box[3] + col[hi][2][1]) / 2)
    return [box[0], top, box[2], bottom]


def page_png(pdf, n, cache):
    p = cache / f"p{n:03d}.png"
    if not p.exists():
        cache.mkdir(parents=True, exist_ok=True)
        run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", str(DPI), "-png", "-singlefile", str(pdf),
             str(p.with_suffix(""))])
    return Image.open(p).convert("RGB")


def shoot_one(pdf, pages, ex, shots, cache):
    """Highlight the quote's words (or the `mark` boxes) and crop around them; returns the shot's record."""
    if not ex.get("quote"):                           # a table or figure: a given box, marked by boxes
        return shoot_region(pdf, ex, shots, cache)
    order = [ex["page"]] if ex.get("page") else []
    order += [i for i in range(1, len(pages) + 1) if i not in order]
    r, n, hits = 0.0, order[0], []
    for p in order:                                   # the page the reading names first, then the rest
        rp, hp = find(pages[p - 1], ex["quote"])
        if rp > r:
            r, n, hits = rp, p, hp
        if r >= 0.8:
            break
    rec = {"id": ex["id"], "page": n, "match": round(r, 2), "asked_page": ex.get("page")}
    if r < 0.8:
        rec["status"] = "not found"
        return rec
    page = pages[n - 1]
    k = DPI / 72
    im = page_png(pdf, n, cache)
    mask = Image.new("RGB", im.size, (255, 255, 255))
    d = ImageDraw.Draw(mask)
    by_line = {}
    for w, bi, li in hits:
        by_line.setdefault((bi, li), []).append(w["b"])
    for boxes in list(by_line.values()) + [[b] for b in ex.get("mark", [])]:
        x0, y0, x1, y1 = union(boxes)
        d.rectangle([x0 * k - 2, y0 * k - 1, x1 * k + 2, y1 * k + 2], fill=HIGHLIGHT)
    im = ImageChops.multiply(im, mask)
    out = save_shot(im, crop_box(page, hits, ex.get("crop")), shots / f"{ex['id']}-p{n}.jpg")
    rec.update(status="ok" if n == ex.get("page") or not ex.get("page") else "found on another page",
               shot=str(out.relative_to(shots.parent)), lines=len(by_line))
    return rec


def save_shot(im, box_pt, out):
    """Crop a page render to a box in PDF points and save it as a JPEG: a page shot is text on white, and a
    JPEG of it is a third of the PNG's size (Project11-TimeSeries 261010: one reading was 4 MB)."""
    k = DPI / 72
    x0, y0, x1, y1 = box_pt
    px, py = 10, 0                                    # crop_box already padded y by at most half a line gap
    box = [max(0, int((x0 - px) * k)), max(0, int((y0 - py) * k)),
           min(im.width, int((x1 + px) * k)), min(im.height, int((y1 + py) * k))]
    im.crop(box).save(out, "JPEG", quality=85, optimize=True)
    return out


def shoot_region(pdf, ex, shots, cache):
    """A table row or a figure: pdftotext reads a table cell by cell down each column, so a row is never one
    run of words. The reading gives `page`, a `crop` box and `mark` boxes (from `boxes`) instead of a quote."""
    rec = {"id": ex["id"], "page": ex.get("page"), "match": 1.0, "asked_page": ex.get("page")}
    crop = ex.get("crop")
    if not ex.get("page") or not (isinstance(crop, list) and len(crop) == 4):
        rec.update(match=0.0, status="no quote: give page and a crop box")
        return rec
    n, k = ex["page"], DPI / 72
    im = page_png(pdf, n, cache)
    mask = Image.new("RGB", im.size, (255, 255, 255))
    d = ImageDraw.Draw(mask)
    for x0, y0, x1, y1 in ex.get("mark", []):
        d.rectangle([x0 * k - 2, y0 * k - 1, x1 * k + 2, y1 * k + 2], fill=HIGHLIGHT)
    out = save_shot(ImageChops.multiply(im, mask), [float(v) for v in crop], shots / f"{ex['id']}-p{n}.jpg")
    rec.update(status="ok (region)", shot=str(out.relative_to(shots.parent)), lines=len(ex.get("mark", [])))
    return rec


def load(spec_path):
    spec_path = Path(spec_path).resolve()
    spec = yaml.safe_load(spec_path.read_text())
    pdf = Path(spec["paper"]["pdf"]).expanduser()
    pdf = pdf if pdf.is_absolute() else (spec_path.parent / pdf).resolve()
    if not pdf.exists():
        raise SystemExit(f"paper.pdf not found: {pdf}")
    ids = [e["id"] for e in spec.get("excerpts", [])]
    if len(set(ids)) != len(ids):
        raise SystemExit(f"excerpt ids repeat: {ids}")
    targets = {t["id"] for t in (spec.get("ours") or {}).get("targets", [])}
    for e in spec.get("excerpts", []):
        link = e.get("link") or {}
        if link and link.get("to") not in targets:
            raise SystemExit(f"{e['id']}: link.to {link.get('to')!r} is not one of ours.targets {sorted(targets)}")
        if link and link.get("relation") not in RELATIONS:
            raise SystemExit(f"{e['id']}: link.relation must be one of {RELATIONS}")
    return spec_path, spec, pdf


def cmd_shoot(a):
    spec_path, spec, pdf = load(a.spec)
    folder = spec_path.parent
    pages = words_of(pdf)
    shots = folder / "shots"
    shots.mkdir(exist_ok=True)
    for old in list(shots.glob("*.png")) + list(shots.glob("*.jpg")):   # renamed or removed excerpts
        old.unlink()
    with tempfile.TemporaryDirectory() as tmp:        # full-page renders stay out of the reading folder
        recs = [shoot_one(pdf, pages, ex, shots, Path(tmp)) for ex in spec.get("excerpts", [])]
    (shots / "index.json").write_text(json.dumps(recs, indent=1))
    for r in recs:
        print(f"  {r['id']:<4} p{r['page']:<3} match {r['match']:.2f}  {r['status']}  {r.get('shot', '')}")
    bad = [r for r in recs if r["match"] < 0.8]
    if bad:
        print(f"{len(bad)} excerpt(s) not shot: copy the quote exactly from paper.txt, one sentence within one "
              "page; for a table row or figure, give page + crop box + mark boxes (`boxes` prints them)")
    return recs


# ---------------------------------------------------------------- draw: the canvas

sys.path.insert(0, str(STUDIO))
INK, GRAY, RED = "#1e1e1e", "#868e96", "#e03131"
FONT, CODE = 6, 3
els, FILES, FRAME = [], {}, [None]


def base(kind, x, y, w, h, stroke=INK, sw=2, dashed=False, rough=1):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": rough, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": {"type": 3} if kind == "rectangle" else None, "seed": len(els) + 1,
         "version": 1, "versionNonce": len(els) + 1, "isDeleted": False, "boundElements": [], "updated": 1,
         "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=22, color=INK, font=FONT, link=None):
    lines = s.split("\n")
    e = base("text", x, y, max(len(l) for l in lines) * size * (0.6 if font == CODE else 0.55),
             len(lines) * size * 1.25, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=None, autoResize=True, lineHeight=1.25, link=link)
    return e


def wrap(s, width_px, size):
    return "\n".join(textwrap.wrap(" ".join(str(s).split()), max(10, int(width_px / (size * 0.55)))))


def path_lines(s, width_px, size):
    """A long path broken after a "/" so it stays inside its frame."""
    room, out, cur = max(10, int(width_px / (size * 0.6))), [], ""
    for part in re.split(r"(?<=/)", str(s)):
        if cur and len(cur) + len(part) > room:
            out.append(cur)
            cur = ""
        cur += part
    return "\n".join(out + [cur])


def para(x, y, s, width, size=22, color=INK):
    t = text(x, y, wrap(s, width, size), size, color)
    return y + t["height"]


def arrow(x0, y0, x1, y1, color=INK, dashed=False):
    e = base("arrow", x0, y0, abs(x1 - x0) or 1, abs(y1 - y0) or 1, color, dashed=dashed)
    e.update(points=[[0, 0], [x1 - x0, y1 - y0]], lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead="arrow")


def picture(x, y, path, width):
    im = Image.open(path).convert("RGB")
    k = min(1.0, 1600 / max(im.size))
    if k < 1:
        im = im.resize((round(im.width * k), round(im.height * k)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85, optimize=True)
    raw = buf.getvalue()
    fid = hashlib.sha1(raw).hexdigest()
    FILES[fid] = {"mimeType": "image/jpeg", "id": fid, "created": 1790900000000,
                  "dataURL": "data:image/jpeg;base64," + base64.b64encode(raw).decode()}
    h = width * im.height / im.width
    base("rectangle", x - 2, y - 2, width + 4, h + 4, GRAY, sw=1, rough=0)
    e = base("image", x, y, width, h, "transparent", rough=0)
    e.update(fileId=fid, status="saved", scale=[1, 1], roundness=None)
    return y + h


def frame(name, w, h=10):
    FRAME[0] = None
    e = base("frame", 0, 0, w, h, "#bbbbbb", rough=0)
    e.update(name=name, roundness=None)
    FRAME[0] = e["id"]
    return e


def draw_logic(spec, x=60, w=1240):
    fr = frame("Paper logic", w + 120)
    p = spec["paper"]
    y = para(x, 40, p.get("title", ""), w, 34)
    y = para(x, y + 10, p.get("cite", ""), w, 22, GRAY)
    if p.get("link"):
        y += 6 + text(x, y + 6, path_lines(p["link"], w, 20), 20, GRAY, CODE, link=p["link"])["height"] + 6
    y += 40
    for i, node in enumerate(spec.get("logic", [])):
        if i:
            arrow(x + 60, y - 46, x + 60, y - 8)
        top = y
        refs = "  ".join(node.get("excerpts", []))
        text(x + 24, y + 14, f"{node.get('role', '').upper()}" + (f"   ·   {refs}" if refs else ""), 22, GRAY)
        bottom = para(x + 24, y + 48, node["text"], w - 60, 24)
        base("rectangle", x, top, w, bottom - top + 22)
        y = bottom + 22 + 54
    fr["height"] = y
    return fr


def draw_ours(spec, recs, x=60, w=1480):
    ours = spec.get("ours") or {}
    fr = frame("Link to our paper", w + 120)
    y = para(x, 40, "Our paper: " + ours.get("title", "(not named)"), w, 30)
    if ours.get("source"):
        y += 6 + text(x, y + 6, path_lines(ours["source"], w, 20), 20, GRAY, CODE)["height"] + 6
    y += 30
    exs = spec.get("excerpts", [])
    for t in ours.get("targets", []):
        top = y
        y = para(x + 24, y + 16, f"{t['id']}  {t.get('label', '')}", w - 60, 26)
        linked = [e for e in exs if (e.get("link") or {}).get("to") == t["id"]]
        if not linked:
            y = para(x + 48, y + 8, "no excerpt links here yet", w - 100, 22, RED)
        for e in linked:
            ln = e["link"]
            y = para(x + 48, y + 8, f"{e['id']} {ln['relation']}: {ln.get('how', '')}", w - 100, 22)
        base("rectangle", x, top, w, y - top + 18)
        y += 48
    loose = [e for e in exs if not e.get("link")]
    if loose:
        y = para(x, y, "Not linked: " + ", ".join(e["id"] for e in loose), w, 22, RED) + 20
    fr["height"] = y + 20
    return fr


def draw_excerpts(spec, recs, x=60, card=1220, gap=80):
    canvas = __import__("canvas")
    fr = canvas.reads_down(frame("Excerpts", 2 * card + gap + 120))
    by_id = {r["id"]: r for r in recs}
    folder = Path(spec["_folder"])
    y_row, col = 40, 0
    row_bottom = 40
    for ex in spec.get("excerpts", []):
        cx = x + col * (card + gap)
        rec = by_id.get(ex["id"], {})
        y = para(cx, y_row, f"{ex['id']}  ·  p.{rec.get('page', ex.get('page', '?'))}  ·  {ex.get('label', '')}",
                 card, 26)
        if rec.get("shot"):
            y = picture(cx, y + 12, folder / rec["shot"], card) + 18
        else:
            miss = f"quote not found in the PDF: \"{ex['quote'][:120]}\"" if ex.get("quote") else rec.get(
                "status", "not shot")
            y = para(cx, y + 12, miss, card, 22, RED) + 12
        if ex.get("says"):
            y = para(cx, y, "Says: " + ex["says"], card, 22)
        if ex.get("comment"):
            y = para(cx, y + 8, "Comment: " + ex["comment"], card, 22)
        ln = ex.get("link")
        if ln:
            y = para(cx, y + 8, f"-> Ours {ln['to']} ({ln['relation']}): {ln.get('how', '')}", card, 22)
        row_bottom = max(row_bottom, y)
        col += 1
        if col == 2:
            col, y_row = 0, row_bottom + 90
    fr["height"] = row_bottom + 60
    return fr


def draw_questions(spec, x=60, w=900):
    fr = frame("Questions", w + 120)
    y = 40
    for q in spec.get("open", []) or ["(none yet)"]:
        top = y
        y = para(x + 20, y + 14, q, w - 40, 24, RED)
        base("rectangle", x, top, w, y - top + 16, RED, sw=1)
        y += 44
    fr["height"] = y + 200                                   # room to answer beside each question
    return fr


def cmd_draw(a, recs=None):
    spec_path, spec, _ = load(a.spec)
    folder = spec_path.parent
    spec["_folder"] = str(folder)
    if recs is None:
        idx = folder / "shots" / "index.json"
        recs = json.loads(idx.read_text()) if idx.exists() else cmd_shoot(a)
    canvas = __import__("canvas")
    logic, ours, qs = draw_logic(spec), draw_ours(spec, recs), draw_questions(spec)
    exc = draw_excerpts(spec, recs)
    FRAME[0] = None
    canvas.grid(els, [[logic["id"], ours["id"], qs["id"]], [exc["id"]]])
    out = folder / f"{a.name or folder.name}.excalidraw"
    canvas.write(out, els, "excalidraw-read/ref/read_paper.py", files=FILES)
    png = out.with_suffix(".png")
    subprocess.run([sys.executable, str(STUDIO / "render_png.py"), str(out), str(png), "0.45"], check=False)
    if png.exists():                                  # a preview, not the drawing: 256 colours keep it light
        Image.open(png).convert("RGB").quantize(256).save(png, optimize=True)
    print(f"drew {len(spec.get('logic', []))} logic steps, {len(recs)} excerpts -> {out}")


def main():
    sys.stdout.reconfigure(line_buffering=True)       # shoot's lines print before the preview's, when piped
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("text")
    t.add_argument("pdf")
    t.add_argument("--out", required=True)
    b = sub.add_parser("boxes")
    b.add_argument("pdf")
    b.add_argument("--page", type=int, required=True)
    b.add_argument("--find", help="only lines containing this text")
    for name in ("shoot", "draw", "all"):
        s = sub.add_parser(name)
        s.add_argument("spec")
        s.add_argument("--name", help="drawing name; default: the folder's name")
    a = ap.parse_args()
    if a.cmd == "text":
        cmd_text(a)
    elif a.cmd == "boxes":
        cmd_boxes(a)
    elif a.cmd == "shoot":
        cmd_shoot(a)
    elif a.cmd == "draw":
        cmd_draw(a)
    else:
        cmd_draw(a, cmd_shoot(a))


if __name__ == "__main__":
    main()
