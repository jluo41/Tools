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
    """Letters and digits only, so line breaks, spacing and punctuation never block a match. Chinese, Japanese
    and Korean characters are kept (b11 s47, 261012: a Chinese quote shrank to its few ASCII words and
    'matched' a title)."""
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[^0-9a-z%.\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]+", "", s.replace("’", "'")).strip(".")


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


def trim(word, k0, k1):
    """The word with its box narrowed to its normalized characters k0..k1-1: a run of Chinese text is one
    pdftotext word, so a quote that starts or ends inside it highlights only its own characters. Widths are
    weighed per character (a wide East Asian character 1, any other 0.55); the whole word when unsure."""
    raw, pos = word["t"], []
    for i, ch in enumerate(raw):
        pos += [i] * len(re.sub(r"[^0-9a-z%.\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]+", "",
                                unicodedata.normalize("NFKC", ch).lower()))
    if not raw or k1 <= k0 or k1 > len(pos):
        return word
    wide = [1.0 if unicodedata.east_asian_width(ch) in "WF" else 0.55 for ch in raw]
    cum = [0.0]
    for v in wide:
        cum.append(cum[-1] + v)
    a, b = pos[k0], pos[k1 - 1] + 1
    x0, y0, x1, y1 = word["b"]
    return dict(word, b=[x0 + (x1 - x0) * cum[a] / cum[-1], y0, x0 + (x1 - x0) * cum[b] / cum[-1], y1])


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

    starts = []
    for key, _ in toks:
        starts.append(len("".join(k for k, _ in toks[:len(starts)])) if not starts else starts[-1] + len(toks[len(starts) - 1][0]))

    def words(c0, c1):                                # the tokens covering characters c0..c1-1, the ends trimmed
        i0, i1 = owner[c0], owner[c1 - 1]
        out = []
        for i in range(i0, i1 + 1):
            ms = toks[i][1]
            if len(ms) == 1 and (i == i0 or i == i1):  # a one-word token the quote enters or leaves partway
                k0 = c0 - starts[i] if i == i0 else 0
                k1 = c1 - starts[i] if i == i1 else len(toks[i][0])
                w, bi, li = ms[0]
                out.append((trim(w, k0, k1), bi, li))
            else:
                out += ms
        return out
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


def best_page(pages, ex):
    """(ratio, page number, hits) of the excerpt's quote: the page the reading names first, then the rest."""
    order = [ex["page"]] if ex.get("page") else []
    order += [i for i in range(1, len(pages) + 1) if i not in order]
    r, n, hits = 0.0, order[0], []
    for p in order:
        rp, hp = find(pages[p - 1], ex["quote"])
        if rp > r:
            r, n, hits = rp, p, hp
        if r >= 0.8:
            break
    return r, n, hits


def shoot_one(pdf, pages, ex, shots, cache):
    """Highlight the quote's words (or the `mark` boxes) and crop around them; returns the shot's record."""
    if not ex.get("quote"):                           # a table or figure: a given box, marked by boxes
        return shoot_region(pdf, ex, shots, cache)
    r, n, hits = best_page(pages, ex)
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


# ---------------------------------------------------------------- pages: the source whole, its passages in place

PAGE_DPI = 150        # a page shown whole: legible at 100% zoom, a nine-page Section near 2 MB
LONG_PDF = 4          # past this many pages and no `section:`, only the pages with passages, each cut to them


def locate(pages, ex):
    """(page number, [line boxes in PDF points]) where an excerpt stands, or (None, []): a quote by its words, a
    table or figure by its `mark` boxes (else its `crop` box)."""
    if not ex.get("quote"):
        crop = ex.get("crop")
        boxes = [[float(v) for v in b] for b in ex.get("mark") or []] or \
            ([[float(v) for v in crop]] if isinstance(crop, list) and len(crop) == 4 else [])
        return (ex["page"], boxes) if ex.get("page") and boxes else (None, [])
    r, n, hits = best_page(pages, ex)
    if r < 0.8:
        return None, []
    by_line = {}
    for w, bi, li in hits:
        by_line.setdefault((bi, li), []).append(w["b"])
    return n, sorted((union(b) for b in by_line.values()), key=lambda b: (b[1], b[0]))


def line_tops(page):
    """Every text line of a page as (top, bottom, its words), top to bottom, in PDF points."""
    return sorted((ln["b"][1], ln["b"][3], " ".join(w["t"] for w in ln["w"])) for bl in page["blocks"] for ln in bl["l"])


def heading_top(page, s, after=-1.0):
    """The top of the first row of the page, below `after`, that starts with s (spacing and punctuation ignored), or
    None. A row is the lines that share a height, left to right: pdftotext gives a heading's number and its words as
    two lines."""
    want, rows = norm(s), []
    for bl in page["blocks"]:
        for ln in bl["l"]:
            mid = (ln["b"][1] + ln["b"][3]) / 2
            row = next((r for r in rows if abs(r["mid"] - mid) < 3), None)
            if row is None:
                rows.append(row := {"mid": mid, "top": ln["b"][1], "lines": []})
            row["top"] = min(row["top"], ln["b"][1])
            row["lines"].append((ln["b"][0], " ".join(w["t"] for w in ln["w"])))
    for r in sorted(rows, key=lambda r: r["top"]):
        if r["top"] > after and want and norm(" ".join(t for _, t in sorted(r["lines"]))).startswith(want):
            return r["top"]
    return None


def gap_above(page, at):
    """Where to cut above a heading at `at`: 16 pt above it, but never through the line before it."""
    before = [e for _, e, _ in line_tops(page) if e < at - 1]
    return max(at - 16, (max(before) + 2) if before else 0.0)


def shoot_pages(pdf, pages, spec, shots, cache):
    """The pages the drawing shows on its left, every passage highlighted where it stands (JL 261014: "what we want
    is still the screenshot in the left, and the comments in the right"). A reading's `section:` shows its pages
    whole, the first from its `from` heading and the last up to its `until` heading (a Section of our own paper,
    read whole); its `parts`, the subsection headings in order, cut it into parts, each from its heading to the next
    one's (JL 261014: "for the section like s15, we have more subsection ... use the stair to show each subsection
    as well, to seperate them"), and the words between the Section's heading and its first part are its opening.
    Without `section:`, every page holding a passage, whole for a short paper and cut to its passages past LONG_PDF
    pages. Writes shots/page-p<N>[-<k>].jpg and shots/pages.json: {parts: [{name, cuts: [{page, shot, size, marks:
    [{id, top}]}]}]}, each passage's top in its shot's pixels."""
    marks = {}
    for ex in spec.get("excerpts", []):
        n, boxes = locate(pages, ex)
        if n:
            marks.setdefault(n, []).append((ex["id"], boxes))
    sec = spec.get("section") or {}
    span = [int(v) for v in sec.get("pages") or []]
    shown = sorted(set(range(span[0], span[-1] + 1) if span else []) | set(marks))
    whole = bool(span) or len(pages) <= LONG_PDF

    def body(page):                                   # the page's words, not its page number
        return [bl["b"] for bl in page["blocks"] if not "".join(w["t"] for ln in bl["l"] for w in ln["w"]).isdigit()]
    edges = [b for n in shown for b in body(pages[n - 1])]
    x0 = max(0.0, min((b[0] for b in edges), default=0.0) - 14)
    x1 = max((b[2] for b in edges), default=pages[0]["w"]) + 14
    heads = {line_tops(pages[n - 1])[0][2] if line_tops(pages[n - 1]) else "" for n in shown}
    running = len(shown) > 1 and len(heads) == 1 and heads != {""}   # a header every page repeats ("DRAFT")

    def limits(n):                                    # a page's own cut: under a running header, above its number
        page, rows = pages[n - 1], line_tops(pages[n - 1])
        return (rows[0][1] + 4 if running and len(rows) > 1 else 0.0,   # just under it: a picture is never cut
                max((b[3] for b in body(page)), default=page["h"]) + 18)

    names, cuts = [], []                              # cuts: [part index, page, top, bottom] in PDF points
    if span:
        n, t = span[0], limits(span[0])[0]
        if sec.get("from"):
            at = heading_top(pages[n - 1], sec["from"])
            t = max(0.0, at - 16) if at is not None else t
        starts = [[sec.get("name") or "", n, t]]      # the opening
        for name in sec.get("parts") or []:
            hit = next(((m, gap_above(pages[m - 1], at)) for m in range(starts[-1][1], span[-1] + 1)
                        if (at := heading_top(pages[m - 1], name, starts[-1][2] if m == starts[-1][1] else -1))
                        is not None), None)
            if hit is None:
                print(f"  part not found on pages {span[0]}-{span[-1]}: {name!r}")
                continue
            between = hit[0] > starts[-1][1] or any(starts[-1][2] + 20 < t < hit[1] + 14
                                                    for t, _, _ in line_tops(pages[hit[0] - 1]))
            if not between:                           # the heading right under the last one: the part starts there
                starts[-1][0] = name
            else:
                starts.append([name, *hit])
        end = [span[-1], limits(span[-1])[1]]
        if sec.get("until"):
            at = heading_top(pages[span[-1] - 1], sec["until"])
            end[1] = at - 8 if at is not None else end[1]
        for k, (name, n, t) in enumerate(starts):
            n2, t2 = (starts[k + 1][1:] if k + 1 < len(starts) else end)
            names.append(name)
            for m in range(n, n2 + 1):
                top, bottom = (t if m == n else limits(m)[0]), (t2 if m == n2 else limits(m)[1])
                if bottom - top > 24:                 # two lines at least: never a sliver of the next page
                    cuts.append([k, m, top, bottom])
    else:
        names = [None]
        for n in shown:
            top, bottom = limits(n)
            here = [b for _, bx in marks.get(n, []) for b in bx]
            if not whole:                             # cut between whole lines: 6 above the first passage, 4 below
                rows = line_tops(pages[n - 1])
                above = [t for t, _, _ in rows if t < min(b[1] for b in here)][-6:]
                below = [e for _, e, _ in rows if e > max(b[3] for b in here)][:4]
                top = max(0.0, (above[0] if above else min(b[1] for b in here)) - 4)
                bottom = (below[-1] if below else max(b[3] for b in here)) + 6
            cuts.append([0, n, top, bottom])
    held = {k: [] for k in range(len(cuts))}          # each passage in the cut that holds its first line
    for n, found in marks.items():
        for i, bx in found:
            same = [k for k, c in enumerate(cuts) if c[1] == n]
            if not same:                              # outside the Section: its own cut, in the last part
                cuts.append([len(names) - 1, n, *limits(n)])
                held[len(cuts) - 1], same = [], [len(cuts) - 1]
            k = min(same, key=lambda k: 0 if cuts[k][2] <= bx[0][1] < cuts[k][3] else
                    min(abs(bx[0][1] - cuts[k][2]), abs(bx[0][1] - cuts[k][3])))
            held[k].append((i, bx))
            cuts[k][2] = min(cuts[k][2], min(b[1] for b in bx) - 16)
            cuts[k][3] = max(cuts[k][3], max(b[3] for b in bx) + 8)
    if len(names) > 1 and not any(held[k] for k, c in enumerate(cuts) if c[0] == 0):
        names[1] = f"opening and {names[1]}"          # an opening with no passage read: it joins the first part
        names.pop(0)
        for c in cuts:
            c[0] = max(0, c[0] - 1)
    many = {n for n in {c[1] for c in cuts} if sum(c[1] == n for c in cuts) > 1}
    k_pt, s = DPI / 72, PAGE_DPI / 72
    parts = [{"name": name, "cuts": []} for name in names]
    for k, (part, n, top, bottom) in sorted(enumerate(cuts), key=lambda c: (c[1][0], c[1][1], c[1][2])):
        im = page_png(pdf, n, cache)
        mask = Image.new("RGB", im.size, (255, 255, 255))
        d = ImageDraw.Draw(mask)
        for bx0, by0, bx1, by1 in (b for _, bx in held[k] for b in bx):
            d.rectangle([bx0 * k_pt - 2, by0 * k_pt - 1, bx1 * k_pt + 2, by1 * k_pt + 2], fill=HIGHLIGHT)
        im = ImageChops.multiply(im, mask).crop((int(x0 * k_pt), max(0, int(top * k_pt)),
                                                 min(im.width, int(x1 * k_pt)), min(im.height, int(bottom * k_pt))))
        im = im.resize((round(im.width * PAGE_DPI / DPI), round(im.height * PAGE_DPI / DPI)), Image.LANCZOS)
        dst = shots / (f"page-p{n}-{part + 1}.jpg" if n in many else f"page-p{n}.jpg")
        im.save(dst, "JPEG", quality=60, optimize=True)
        parts[part]["cuts"].append({"page": n, "shot": str(dst.relative_to(shots.parent)), "size": list(im.size),
                                    "marks": [{"id": i, "top": round((bx[0][1] - top) * s, 1)}
                                              for i, bx in sorted(held[k], key=lambda h: h[1][0][1])]})
    (shots / "pages.json").write_text(json.dumps({"parts": parts}, indent=1))
    return [c for p in parts for c in p["cuts"]]


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
        shown = shoot_pages(pdf, pages, spec, shots, Path(tmp))
    (shots / "index.json").write_text(json.dumps(recs, indent=1))
    for r in recs:
        print(f"  {r['id']:<4} p{r['page']:<3} match {r['match']:.2f}  {r['status']}  {r.get('shot', '')}")
    print(f"  pages shown: {', '.join('p%d' % p['page'] for p in shown) or 'none'}")
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


def picture(x, y, path, width, as_is=False):
    """An image `width` wide; `as_is` embeds a JPEG this script already sized and compressed (a shown page)."""
    im = Image.open(path).convert("RGB")
    if as_is:
        raw = Path(path).read_bytes()
    else:
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


T_TITLE, T_KEY, T_HEAD, T_NODE, T_TEXT, T_ACT = 60, 38, 44, 30, 28, 40   # excalidraw-studio ⑤ ⑦: none a reader needs under 28
VERDICTS = {"KEEP": "✅", "REWRITE": "✏️", "CUT": "✂️", "MOVE": "➡️"}
ROLES = {"question": "🔎", "gap": "🕳️", "method": "🛠️", "result": "📊", "claim": "💬", "limit": "⚠️"}
POINTS = re.compile(r"^((?:[A-Z]\d+(?:\.\d+)?)(?:,\s*[A-Z]\d+(?:\.\d+)?)*):\s*")
W_FRAME = 2750                                       # every frame one width: a page's column and its notes'
PAGE_W, NOTE_W = 1300, 1100                          # a shown page's width on the canvas; a note's


def circled(n):
    return chr(0x2460 + n - 1) if 1 <= n <= 20 else f"({n})"


def numbers(spec):
    """Each excerpt's number: E3 is 3; any other id, its place in the reading."""
    return {e["id"]: (int(e["id"][1:]) if re.fullmatch(r"E\d+", str(e["id"])) else k)
            for k, e in enumerate(spec.get("excerpts", []), 1)}


def verdict_of(ex):
    """KEEP, REWRITE, CUT or MOVE when the comment begins with one (a Section of our own paper read for a
    redesign), else ''."""
    m = re.match(r"\s*(KEEP|REWRITE|CUT|MOVE)\b", str(ex.get("comment", "")))
    return m.group(1) if m else ""


def target_name(spec, tid):
    """A target as the drawing names it: our own new Section by its label's head ("The new §1"), else its id."""
    t = next((t for t in (spec.get("ours") or {}).get("targets", []) if t["id"] == tid), {})
    label = str(t.get("label", ""))
    return label.split(":")[0] if str(tid).startswith("new-") and label else str(tid)


def why_line(spec, ex):
    """A note's second line: what the passage answers to, by its target's name and the review points cited."""
    ln = ex.get("link") or {}
    if not ln.get("to"):
        return "not linked to our paper"
    name = target_name(spec, ln["to"])
    if str(ln["to"]).startswith("new-"):
        return f"{'carried into' if ln.get('relation') in ('borrows', 'supports', 'cites') else 'what is missing in'} {name}"
    m = POINTS.match(str(ln.get("how", "")))
    return f"{name} · {m.group(1)}" if m else name


def box_start(x, y, w, color=INK, fill=None, dashed=False):
    """A box drawn before its words, so a filled one never covers them; its height is set once they are drawn."""
    b = base("rectangle", x, y, w, 10, color, dashed=dashed)
    if fill:
        b.update(backgroundColor=fill, fillStyle="solid")
    return b


def draw_overview(spec, x=60):
    """Act 1, the map: the key point (how much of the Section changes, in the key-point yellow), the argument as a
    flow of steps, each naming its passages, and what each passage answers to. Every passage's says and comment stay
    in reading.yaml and the face (excalidraw-studio ⑦ few words in a map, ⑨ never a wall of text)."""
    canvas = __import__("canvas")
    sec, p, num = spec.get("section") or {}, spec["paper"], numbers(spec)
    exs = spec.get("excerpts", [])
    fr = frame(f"① {sec['name']}: how much changes" if sec.get("name") else "① Its logic, and our link", W_FRAME)
    y = para(x, 30, f"{sec['name']} as submitted" if sec.get("name") else p.get("title", ""), W_FRAME - 2 * x, T_TITLE)
    key = spec.get("key") or sec.get("key")
    if key:
        lines = key if isinstance(key, list) else [key]
        b = box_start(x, y + 20, W_FRAME - 2 * x, fill=canvas.KEY)
        first = re.sub(r"\b(\d+) (KEEP|REWRITE|CUT|MOVE)\b", lambda m: f"{m[1]} {VERDICTS[m[2]]} {m[2]}", lines[0])
        yy = para(x + 30, y + 38, first, W_FRAME - 2 * x - 60, T_KEY)       # the verdicts' emoji, named once
        for more in lines[1:]:
            yy = para(x + 30, yy + 6, more, W_FRAME - 2 * x - 60, T_NODE)
        b["height"] = yy - (y + 20) + 18
        y = yy + 18
    lw, rx = 1300, x + 1300 + 130
    rw = W_FRAME - x - rx
    yl = para(x, y + 36, "🧭 its argument", lw, T_HEAD) + 18
    for i, st in enumerate(spec.get("logic", [])):    # one box a step: its role, its passages, its words
        if i:
            arrow(x + 60, yl - 34, x + 60, yl - 4)
        refs = " ".join(circled(num[e]) for e in st.get("excerpts", []) if e in num)
        b = box_start(x, yl, lw)
        yy = para(x + 24, yl + 12, f"{ROLES.get(st.get('role'), '▪')} {st.get('role', '')} {refs}: {st['text']}",
                  lw - 48, T_NODE)
        for h in st.get("how") or []:                 # how this step was done, inside the step (JL 261019)
            yy = para(x + 48, yy + 4, h if re.match(r"[^:]{1,24}: ", str(h)) else f"· {h}", lw - 72, T_TEXT)
        b["height"] = yy - yl + 12
        yl = yy + 12 + 32
    yr = para(rx, y + 36, "🎯 what each answers to", rw, T_HEAD) + 18
    seen = []
    for ex in exs:
        to = (ex.get("link") or {}).get("to")
        if to and to not in seen:
            seen.append(to)
    for to in seen + ([None] if any(not ex.get("link") for ex in exs) else []):
        mine = [ex for ex in exs if (ex.get("link") or {}).get("to") == to]
        b = box_start(rx, yr, rw, INK if to else RED)
        yy = para(rx + 24, yr + 14, target_name(spec, to) if to else "not linked yet", rw - 48, T_NODE, INK if to else RED)
        yy = para(rx + 24, yy + 6, "   ".join(f"{circled(num[ex['id']])} " + (VERDICTS[verdict_of(ex)] if verdict_of(ex)
                                             else (ex.get('link') or {}).get('relation', '')) for ex in mine), rw - 48, T_TEXT)
        b["height"] = yy - yr + 14
        yr = yy + 14 + 22
    fr["height"] = max(yl, yr) + 20
    if any(st.get("how") for st in spec.get("logic", [])):   # steps that say how they were done are read up close:
        fr.setdefault("customData", {})["detail"] = True     #   excalidraw-studio ⑦ sends detail to a detail frame
        fr["customData"]["room"] = True                       #   ⑧ room between its boxes: ⑥ counts over the boxes
        canvas.reads_down(fr)                                 #   and a frame read top to bottom may grow down
    return fr


def draw_questions(spec, x=60, w=1500):
    """Act 2, small on purpose (canvas.explains): the person's open choices, in red, with room to answer."""
    canvas = __import__("canvas")
    fr = canvas.explains(frame("② 🙋 Your call", w + 2 * x))
    y = para(x, 40, "🙋 Your call: mark the drawing in red, or answer in the face's Open", w, T_HEAD) + 30
    for q in spec.get("open", []) or ["(none yet)"]:
        b = box_start(x, y, w, RED)
        yy = para(x + 24, y + 14, q, w - 48, T_TEXT, RED)
        b["height"] = yy - y + 16
        y = yy + 16 + 30
    fr["height"] = y + 120                                   # room to answer under the last question
    return fr


def badge(x, y, n, size=56):
    """A passage's number in a circle of the key-point yellow, beside the passage and beside its note, so no
    arrow has to cross between them (excalidraw-task's transcript_frame does the same)."""
    e = base("ellipse", x, y, size, size, INK, sw=2, rough=0)
    e.update(backgroundColor=__import__("canvas").KEY, fillStyle="solid", roundness=None)
    s = str(n)
    text(x + (size - len(s) * 30 * 0.55) / 2, y + (size - 30 * 1.25) / 2, s, 30)


def part_title(spec, part, many):
    sec = spec.get("section") or {}
    whole = sec.get("name") or "The paper"
    if not part.get("name") or part["name"] == whole:
        return f"{whole}: opening" if many else f"{whole}, read"
    head = whole.split()[0] if whole.startswith("§") else whole
    return f"{head} · {part['name']}"


def draw_part(spec, part, mark, many, x=60):
    """One part of the reading (a subsection of a Section, or the paper read whole): its pages on the left, every
    passage highlighted where it stands and numbered in the margin, and on the right one note per passage, level
    with it, in three short lines: its verdict and name, what it answers to, what the new paper does (`next`).
    A passage the PDF does not hold is a red note under the last one, never hidden."""
    canvas = __import__("canvas")
    folder, num = Path(spec["_folder"]), numbers(spec)
    exs = {e["id"]: e for e in spec.get("excerpts", [])}
    title = part_title(spec, part, many)
    fr = canvas.reads_down(frame(f"{mark} {title}", W_FRAME))
    cuts = part["cuts"]
    pages = sorted({c["page"] for c in cuts})
    ids = [m["id"] for c in cuts for m in c["marks"] if m["id"] in exs]
    y = para(x, 40, title, W_FRAME - 2 * x, T_HEAD)
    where = (f"page {pages[0]}" if len(pages) == 1 else f"pages {pages[0]}-{pages[-1]}") if pages else "no page"
    tally = [(v, sum(verdict_of(exs[i]) == v for i in ids)) for v in VERDICTS]
    say = " · ".join(f"{VERDICTS[v]} {n} {v}" for v, n in tally if n) if any(n for _, n in tally) else \
        f"{len(ids)} passage{'s' if len(ids) != 1 else ''} read" if ids else "no passage read here: see the face's table"
    b = box_start(x, y + 14, W_FRAME - 2 * x, fill=canvas.KEY)  # its key point: what happens to this part
    yy = para(x + 24, y + 26, f"{where} · {say}", W_FRAME - 2 * x - 48, T_NODE)
    b["height"] = yy - (y + 14) + 12
    y = yy + 40
    px, nx = x + 90, x + 90 + PAGE_W + 140
    top, notes = y, []
    for c in cuts:
        w, h = c["size"]
        sc = PAGE_W / w
        text(x, top + 4, f"p.{c['page']}", T_TEXT, GRAY)
        picture(px, top, folder / c["shot"], PAGE_W, as_is=True)
        notes += [(top + m["top"] * sc, c["page"], exs[m["id"]]) for m in c["marks"] if m["id"] in exs]
        top += h * sc + 50
    below, margin = y, y - 100
    for at, n, ex in sorted(notes, key=lambda t: t[0]):
        margin = max(at - 10, margin + 62)           # passages on touching lines: their badges stack, never overlap
        badge(px - 70, margin, num[ex["id"]])
        ny = max(at - 16, below)                     # level with its passage, else just under the note above
        badge(nx - 72, ny + 4, num[ex["id"]])
        ln, v = ex.get("link"), verdict_of(ex)
        b = box_start(nx, ny, NOTE_W, INK if ln else RED)
        yy = para(nx + 24, ny + 14, f"{VERDICTS.get(v, '')} {v} · {ex.get('label', '')}" if v else ex.get("label", ""),
                  NOTE_W - 48, 34)
        yy = para(nx + 24, yy + 8, why_line(spec, ex), NOTE_W - 48, T_TEXT, INK if ln else RED)
        if ex.get("next"):
            yy = para(nx + 24, yy + 6, "→ " + ex["next"], NOTE_W - 48, T_TEXT)
        b["height"] = yy - ny + 18
        below = yy + 18 + 36
    fr["height"] = max(top, below) + 40
    return fr


def draw_missing(spec, placed, x=60):
    """The excerpts no page shows (a quote the PDF does not hold), red, so none is hidden; None when every one shows."""
    lost = [e for e in spec.get("excerpts", []) if e["id"] not in placed]
    if not lost:
        return None
    fr = frame("❓ Not found in the PDF", 1500 + 2 * x)
    y = 40
    for ex in lost:
        b = box_start(x, y, 1500, RED, dashed=True)
        yy = para(x + 24, y + 14, f"{ex['id']} · copy its quote again from paper.txt", 1452, T_NODE, RED)
        yy = para(x + 24, yy + 8, f"Quote: {ex.get('quote', '')}", 1452, T_TEXT, RED)
        b["height"] = yy - y + 16
        y = yy + 16 + 30
    fr["height"] = y + 20
    return fr


def cmd_draw(a, recs=None):
    """The reading as stairs (excalidraw-studio ③: each frame lower and further right, an act named at its left,
    a named arrow down to the next): ① the map of how much changes, ② the person's open choices, then one frame
    per part of the paper, each part's pages beside its short notes."""
    spec_path, spec, _ = load(a.spec)
    folder = spec_path.parent
    spec["_folder"] = str(folder)
    idx = folder / "shots" / "pages.json"
    if recs is None:
        old = json.loads(idx.read_text()) if idx.exists() else None
        recs = cmd_shoot(a) if not isinstance(old, dict) else json.loads((folder / "shots" / "index.json").read_text())
    canvas = __import__("canvas")
    parts = [p for p in json.loads(idx.read_text())["parts"] if p["cuts"]]
    order = [draw_overview(spec)]
    acts = ["Act 1 · how much changes" if (spec.get("section") or {}).get("name") else "Act 1 · its logic"]
    words = []
    order.append(draw_questions(spec))
    acts.append("Act 2 · your call")
    words += ["what to decide", "its pages, part by part" if len(parts) > 1 else "its pages"]
    for k, part in enumerate(parts):
        order.append(draw_part(spec, part, circled(k + 3), len(parts) > 1))
        acts.append(f"Act {k + 3} · {part_title(spec, part, len(parts) > 1)}")
        words.append("next part")
    placed = {m["id"] for p in parts for c in p["cuts"] for m in c["marks"]}
    lost = draw_missing(spec, placed)
    if lost:
        order.append(lost)
        acts.append(f"Act {len(acts) + 1} · not found")
    FRAME[0] = None
    canvas.stairs(els, [f["id"] for f in order], gap=300, step=520)
    for f, name in zip(order, acts):                   # each act named at the left of its frame
        para(f["x"] - 840, f["y"] + 20, name, 760, T_ACT)
    for f, g, w in zip(order, order[1:], words):        # a named arrow down the gap to the next step
        ax = g["x"] + 160
        arrow(ax, f["y"] + f["height"] + 16, ax, g["y"] - 16)
        para(ax + 28, (f["y"] + f["height"] + g["y"]) / 2 - 26, w, 900, 36)
    out = folder / f"{a.name or folder.name}.excalidraw"
    canvas.write(out, els, "excalidraw-read/ref/read_paper.py", files=FILES)
    png = out.with_suffix(".png")
    subprocess.run([sys.executable, str(STUDIO / "render_png.py"), str(out), str(png), "0.45"], check=False)
    if png.exists():                                  # a preview, not the drawing: 256 colours keep it light
        Image.open(png).convert("RGB").quantize(256).save(png, optimize=True)
    print(f"drew {len(spec.get('logic', []))} logic steps, {len(recs)} excerpts, {len(parts)} parts -> {out}")


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
