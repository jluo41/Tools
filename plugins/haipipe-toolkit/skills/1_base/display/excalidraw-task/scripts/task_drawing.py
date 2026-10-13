"""A Task as one drawing: its idea first, then one frame per source saying what that source told.
Asked 261012, on Proj10 discovery/b51_llm_serve: "should we have each task to be a sNN and each frame to describe
what is the video told about", after "I cannot still read the content of it".

    python task_drawing.py make <task folder | job folder> [--nn NN] [--dry-run]   one topic per Task, drawn
    python task_drawing.py draw <topic folder>                                    redraw one (what its builder calls)
    python task_drawing.py preview <task folder> <out.excalidraw> [--words w.yaml]  draw a Task anywhere (with words)

A Discovery Task page files several sources (videos, papers): a concept division first (What it is, How it works,
Why it matters, How the videos fit, Interview questions), then one division per source (`### N · rNN · …`: its
summary line, Key points, Interview hook, Check before reuse). Drawn by excalidraw-studio's principles, ⑦ above all
(few words, none under 28 px):

    Act 1 · the idea     ⓪ the question as the key point; What it is ─▶ How it works ─▶ Why it matters,
                           then the videos in reading order ─▶ the questions to be ready for
    Act 2 · the videos   one frame each: what it says as the key point; its points in order ─▶ how to say it ─▶
                           what to check against the video (red); the arrow into a frame says what that video does

The page keeps the full text. The topic face's `task:` yaml holds the short words the drawing shows (`idea`,
`videos`); anything it leaves out is read from the page. The writer is haipipe-studio's canvas.write, so a person's
marks survive a rebuild.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[2]                                      # skills/1_base
sys.path.insert(0, str(SKILLS / "project/haipipe-studio/scripts"))
sys.path.insert(0, str(SKILLS / "display/excalidraw-studio/scripts"))
sys.path.insert(0, str(SKILLS / "display/excalidraw-job/scripts"))
import canvas  # noqa: E402
import job_drawing as jd  # noqa: E402   the page readers: section(), concept(), first_para(), plain()
import job_results as jr  # noqa: E402   measured wrapping (Chinese a character at a time), read(), title_of()
sys.path.insert(0, str(HERE))
from draw import INK, KEY, RED, Drawing  # noqa: E402

try:
    import yaml
except ImportError:                                           # the drawing still reads the page; the face needs yaml
    yaml = None

W, TALLEST, GAP = 2800, 1600, 700                             # ① the widest a frame may be
NARROW = 2000                                                 # a video frame of words only: ⑥'s floor needs it fuller
STEP_W, STEP_GAP = 860, 130                                   # one step's box, and rows_of's gap between boxes
T_TITLE, T_SUB, T_KEY, T_HEAD, T_BODY, T_ARROW = 60, 28, 36, 36, 30, 28   # ⑦: nothing a person reads under 28 px
BAND_RUN, BAND_CONCEPT = range(21, 30), range(1, 10)
BEGIN, END = "<!-- task-drawing:start -->", "<!-- task-drawing:end -->"
CIRCLED = "①②③④⑤⑥⑦⑧⑨"


# ── reading the Task page ────────────────────────────────────────────────────────────────────────────────────
def plain(s: str) -> str:
    """Markdown to plain words: bold, italic, code and link marks dropped, spaces folded."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", str(s))
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", s.replace("**", ""))
    return jd.plain(s)


def sentences(s: str) -> list[str]:
    """Sentences, not cut at e.g., i.e., vs. or a decimal point."""
    out = []
    for p in re.split(r"(?<=[.!?。！？])\s+(?=[A-Z0-9\"“(一-鿿])", plain(s)):
        if out and re.search(r"\b(e\.g|i\.e|vs|etc|Fig|al)\.$", out[-1]):
            out[-1] += " " + p
        elif p:
            out.append(p)
    return out


def first(s: str, most: int) -> str:
    """Whole sentences up to about `most` characters (at least one)."""
    out = ""
    for sen in sentences(s):
        if out and len(out) + len(sen) + 1 > most:
            break
        out = (out + " " + sen).strip()
    return out


def field(text: str, name: str) -> str:
    """A `**Name**: …` (or `**Name:** …`) paragraph, every line of it, to the next blank line, bold field, heading or fenced block
    (job_drawing's labelled() keeps only the label's own line)."""
    m = re.search(rf"\*\*{re.escape(name)}:?\*\*\s*:?\s*(.*?)(?=\n\s*\n|\n- \*\*|\n\*\*[A-Z]|\n#|\n```|\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def items(text: str, name: str) -> list[str]:
    """The list under a `**Name**` field, bulleted (`- `) or numbered (`1. `), a blank line before it allowed, up to the
    next field or heading. A numbered list matters: a page's How it works is often its steps in order."""
    m = re.search(rf"\*\*{re.escape(name)}:?\*\*.*?\n(.*?)(?=\n\*\*[A-Z][^*]*\*\*\s*:|\n\*\*[A-Z][^*]*:\*\*|\n#|\Z)", text, re.S)
    out = []
    for ln in (m.group(1).splitlines() if m else []):
        mm = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*)$", ln)
        if mm:
            out.append(mm.group(1).strip())
    return out


def point_why(item: str) -> dict:
    """`**Project.** Three learned …` as a step: its bold lead (or first sentence) is the point, the rest why."""
    m = re.match(r"^\*\*(.+?)\*\*[.:]?\s*(.*)$", item.strip())
    if m:
        return {"point": plain(m.group(1)).rstrip(".:"), "why": plain(m.group(2))}
    sens = sentences(item)
    return {"point": sens[0].rstrip(".") if sens else plain(item), "why": " ".join(sens[1:])}


def video_checked(state: str) -> bool:
    """A source checked against its video: the state says the video (or its claims) was checked, and nothing in it is
    still pending; "paper sections checked … video review pending" is not (b12 t07 r05, 261012)."""
    s = str(state).lower()
    if re.search(r"not checked|unchecked|pending|not yet", s):
        return False
    return bool(re.search(r"checked against the video|\b(video|claims?)\b[^;]*\bchecked\b", s))


def run_result(folder: Path, rid: str):
    """A source's result folder when its page division names none: the one runs/<rid>_…/result/ on disk."""
    hits = [p for p in sorted(folder.glob(f"runs/{rid}*/result"))
            if p.is_dir() and re.match(rf"{re.escape(rid)}(_|$)", p.parent.name)]
    return hits[0].resolve() if len(hits) == 1 else None


def run_url(result) -> str:
    """A video Run's link from its own receipt (result/runtime.yaml, then the Run's run.yaml): b11 s46's page names its
    video Run with no "Video →" line, so its screenshots had no video to come from."""
    if not result:
        return ""
    for f in (Path(result) / "runtime.yaml", Path(result).parent / "run.yaml"):
        m = f.is_file() and re.search(r"https?://(?:www\.)?(?:bilibili\.com/video|youtube\.com/watch|youtu\.be)/?[^\s\"']*",
                                      f.read_text(errors="ignore"))
        if m:
            return m.group(0)
    return ""


def parse(page: Path) -> dict:
    """The Task page: its title, question, concept paragraphs, and each source's division."""
    text = jr.read(page)
    title = (re.search(r"^# (.+)$", text, re.M) or [None, page.stem])[1].strip()
    if title == page.stem:                                      # titled by its folder: a short line under it names it
        m = re.match(rf"\s*{re.escape(page.stem)}\s*\n[=-]+\s*\n\s*\n?(.+)\n", text)
        line = m.group(1).strip().rstrip(".") if m else ""
        if line and len(line.split()) <= 12 and not re.match(r"^[\w-]+:\s", line) and not line.startswith(("#", "|")):
            title = line
    opening = next((ln.strip() for ln in jd.section(text, "Opening").splitlines() if ln.strip()), "")
    con = jd.concept(text)
    table = {m.group(1): {"video": m.group(2).strip(), "length": m.group(3).strip(), "star": "★" in m.group(4),
                          "state": m.group(5).strip()}
             for m in re.finditer(r"^\|\s*\d+\s*\|\s*(r\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|", text, re.M)}
    runs = []
    parts = re.split(r"^### (\d+) · (r\d+)\b ?·? ?(.*)$", jd.section(text, "Content") or text, flags=re.M)
    for k in range(1, len(parts) - 3, 4):
        _, rid, short, body = parts[k:k + 4]
        meta = dict(re.findall(r"^(\w+)\s+→\s+(.+)$", body, re.M))
        row = table.get(rid, {})
        runs.append({
            "rid": rid, "short": short.strip() or row.get("video", rid),
            "summary": plain(field(body, rid)), "key": field(body, "Key points"),
            "key_items": items(body, "Key points"),                  # its bullets, one step box each when no face words
            "hook": plain(field(body, "Interview hook")), "check": plain(field(body, "Check before reuse")),
            "url": meta.get("Video", ""), "title": meta.get("Title", ""), "creator": meta.get("Creator", ""),
            "state": meta.get("State", row.get("state", "")), "star": row.get("star", False),
            "result": (page.parent / meta["Result"]).resolve() if meta.get("Result") else run_result(page.parent, rid),
            "length": row.get("length", ""),
            "card": (re.search(r"\[Result Card\]\(([^)]+)\)", body) or [None, ""])[1]})
    for r in runs:                                              # no "Video →" line: the Run's own receipt has it
        if not r["url"]:
            r["url"] = run_url(r["result"])
    work = not runs                                             # no video divisions: a work Task
    if not runs:                                                # a work Task: its Runs are folders with results
        tickets = jr.runs_of(page.parent)
        shared = jr.shared_tickets(tickets)
        for r in tickets:
            if r["name"] in shared and not (r["result"].is_dir() and any(r["result"].iterdir())):
                continue
            runs.append({"rid": r["name"], "short": re.sub(r"^r\d+[a-z]?_", "", r["name"]).replace("_", " "),
                         "summary": "", "key": "", "hook": "", "check": "", "url": "", "title": "", "creator": "",
                         "state": jr.state_of(r), "star": False, "length": "", "card": "", "result": r["result"],
                         "dir": r["dir"], "work": True})
        if title == page.stem:                                  # a page titled by its folder: the folder's own words
            title = re.sub(r"^t\d+_", "", page.stem).replace("_", " ").capitalize()
        opening = opening or jd.first_para(jd.section(text, "Develops")) or jr.field(page.parent, "develops")
    return {"title": title, "question": plain(opening),
            "what": plain(field(con, "What it is")), "how": plain(field(con, "How it works")),
            "how_points": [plain(b) for b in items(con, "How it works")],
            "how_steps": [point_why(b) for b in items(con, "How it works")],
            "details": [point_why(b) for b in items(con, "Design details")],
            "why_points": [plain(b) for b in items(con, "Why it matters")],
            "mental": plain(field(con, "Mental model")), "outcome": plain(field(con, "Learning outcome")),
            "prereq": plain(field(con, "Prerequisites")), "path": plain(field(con, "Core path")),
            "sketch": sketch_of(text),                               # the concept division ends at its ####
            "why": plain(field(con, "Why it matters")), "fit": plain(field(con, "How the videos fit")),
            "questions": [plain(b) for b in items(con, "Interview questions")], "runs": runs, "work": work,
            "limits": limits_of(text)}


def limits_of(text: str) -> list[str]:
    """The page's "### N · Limits" division: each `Label → what` line, then its closing sentence."""
    m = re.search(r"(?ms)^###\s+\d+\s*·\s*Limits\b.*?\n(.*?)(?=^###\s|^##\s|\Z)", text)
    if not m:
        return []
    body = re.sub(r"(?s)\*\*Limits:?\*\*:?[^\n]*\n", "", m.group(1))
    out = [f"{plain(a)}: {plain(b)}" for a, b in re.findall(r"(?m)^([A-Z][\w ]{2,20}?)\s+→\s+(.+)$", body)]
    tail = [plain(b) for b in re.split(r"\n\s*\n", body) if b.strip() and "→" not in b and not b.strip().startswith("```")]
    return out[:6] + tail[-1:]


def qa_items(qs) -> list:
    """Interview questions, each with its answer under it: `{q, a}`, or a page line "*Question?* answer"."""
    out = []
    for q in qs or []:
        if isinstance(q, dict):
            ques, ans = str(q.get("q") or ""), str(q.get("a") or "")
        else:
            m = re.match(r"^(.+?\?)\s*(.*)$", plain(str(q)))
            ques, ans = (m.group(1), m.group(2)) if m else (plain(str(q)), "")
        out.append(text_item(f"▪ {ques}", T_BODY + 1, after=4))
        if ans:
            out.append(text_item(first(ans, 220), T_BODY, indent=34, after=14))
    return out


def reading_order(task: dict, order=None) -> list[dict]:
    """The face's order, else the order "How the videos fit" names them, then the rest by number."""
    by = {r["rid"]: r for r in task["runs"]}
    named = [str(x) for x in (order or [])] or re.findall(r"\b(r\d\d)\b", task["fit"])
    out = []
    for rid in named + sorted(by):
        if rid in by and by[rid] not in out:
            out.append(by[rid])
    return out


def role(task: dict, rid: str) -> str:
    """What "How the videos fit" says a source does, in a few words: the arrow into its frame."""
    for clause in re.split(r"(?<=[.;])\s+|,\s+and\s+(?=r\d\d)", task["fit"]):
        if re.search(rf"\b{rid}\b", clause):
            words = re.sub(r"\b(r\d\d)(\s*(,|and)\s*r\d\d)*\b", "", clause).strip(" .;,")
            words = re.sub(r"^(and|then)\s+", "", words)
            if len(words) > 60:
                words = words[:58].rsplit(" ", 1)[0] + " …"
            return f"then {rid}: {words}"
    return f"then {rid}"


# ── drawing pieces ───────────────────────────────────────────────────────────────────────────────────────────
def heading(d: Drawing, title: str, sub: str, key: str, width: float = W) -> float:
    """Title, its line, and the key point in the one slight colour; returns the y below."""
    y = jr.para(d, 40, 22, title, width - 700, T_TITLE) + 10
    y = jr.para(d, 40, y, sub, width - 700, T_SUB) + 26
    kh = jr.tall("🎯 " + key, width - 140, T_KEY) + 46
    d.key(40, y, width - 80, kh)
    jr.para(d, 70, y + 23, "🎯 " + key, width - 140, T_KEY)
    return y + kh + 50


# ── what a box holds: text, a formula, a symbol and its meaning, screenshots ─────────────────────────────────
FONT_GAPS = str.maketrans({"ᵀ": "^T", "ᵗ": "^t", "ᴴ": "^H", "⁻": "^-", "₍": "(", "₎": ")"})   # Nunito lacks these


def sketch_of(con: str) -> str:
    """The ```text sketch right after the page's **Mental model** line (a #### heading may sit between), else ''."""
    m = re.search(r"\*\*Mental model:?\*\*[^\n]*\n(?:#{2,6} [^\n]*\n)?```text\n(.*?)\n```", con, re.S)
    return m.group(1).rstrip() if m else ""


def code_item(s: str, size: float = T_BODY, indent: float = 34, after: float = 14):
    """A text sketch kept as drawn: monospace, its lines and spacing as on the page, smaller only if too wide."""
    s = s.translate(FONT_GAPS)
    lines = s.split("\n")
    widest = max(len(ln) for ln in lines) or 1

    def fit(w):
        return min(size, (w - indent) / (0.62 * widest))

    def h(w):
        return len(lines) * fit(w) * 1.25 + after

    def draw(d, x, y, w):
        d.text(x + indent, y, s, fit(w), code=True)
        return y + h(w)
    return h, draw


def text_item(s: str, size: float = T_BODY, color=None, indent: float = 0, after: float = 10):
    """Wrapped text; returns (height for a width, draw)."""
    s = str(s).translate(FONT_GAPS)
    def h(w):
        return jr.tall(s, w - indent, size) + after

    def draw(d, x, y, w):
        jr.para(d, x + indent, y, s, w - indent, size, color)
        return y + h(w)
    return h, draw


def tex_png(tex: str, assets: Path, size: int = 30) -> Path | None:
    """A formula drawn by matplotlib's mathtext into assets/ (cached by its text); None when it does not parse."""
    import hashlib
    assets.mkdir(parents=True, exist_ok=True)
    out = assets / f"tex-{hashlib.md5(f'{tex}|{size}'.encode()).hexdigest()[:12]}.png"
    if out.is_file():
        return out
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, f"${tex}$", fontsize=size, color="#1e1e1e")
        fig.savefig(out, dpi=200, bbox_inches="tight", pad_inches=0.06, facecolor="white")
        plt.close(fig)
        return out
    except Exception as err:                                   # a formula mathtext cannot read is drawn as text
        print(f"formula not drawn ({err.__class__.__name__}): {tex}", file=sys.stderr)
        plt.close("all")
        out.unlink(missing_ok=True)
        return None


def embed(d: Drawing, path: Path, x: float, y: float, w: float, h: float) -> None:
    """A picture as it is (a formula stays a crisp png), no border."""
    import base64
    fid = "img-" + path.stem
    d.files[fid] = {"mimeType": "image/png", "id": fid, "created": 1,
                    "dataURL": "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()}
    d.el("image", x, y, w, h, fileId=fid, status="saved", scale=[1, 1])


def size_of(path: Path) -> tuple[int, int]:
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def tex_item(tex: str, assets: Path, height: float = 130):
    """A formula, as tall as `height` (narrower when the box is), else its text in code type."""
    png = tex_png(tex, assets)
    if not png:
        return text_item(tex, T_BODY)
    iw, ih = size_of(png)

    def scale(w):
        return min(height / ih, w / iw)

    def h(w):
        return ih * scale(w) + 18

    def draw(d, x, y, w):
        embed(d, png, x, y, iw * scale(w), ih * scale(w))
        return y + h(w)
    return h, draw


def sym_item(tex: str, means: str, assets: Path):
    """A symbol drawn as math, and what it means in plain words beside it."""
    png = tex_png(tex, assets)
    col = 250

    def h(w):
        return max(62, jr.tall(means, w - col, T_BODY)) + 12

    def draw(d, x, y, w):
        if png:
            iw, ih = size_of(png)
            sc = min(58 / ih, (col - 30) / iw)
            embed(d, png, x, y + 2, iw * sc, ih * sc)
        else:
            d.text(x, y, tex, T_BODY, code=True)
        jr.para(d, x + col, y, means, w - col, T_BODY)
        return y + h(w)
    return h, draw


def shots_item(shots: list, tallest: float = 620, per_row: int = 4):
    """Screenshots side by side, each with its time and what it shows under it; more than `per_row` wrap to a
    second row of the same size."""
    gap = 26
    nrows = max(1, -(-len(shots) // per_row))
    cols = max(1, -(-len(shots) // nrows))                         # balanced: 5 draw 3 + 2, not 4 + 1
    rows = [shots[k:k + cols] for k in range(0, len(shots), cols)]

    def geo(w, row):
        cw = (w - gap * (cols - 1)) / cols
        out = []
        for path, caption in row:
            iw, ih = size_of(path)
            sc = min(cw / iw, tallest / ih)
            out.append((cw, iw * sc, ih * sc, caption))
        return out

    def row_h(w, row):
        g = geo(w, row)
        return max(ih for _, _, ih, _ in g) + 14 + max(jr.tall(c, cw, 28) for cw, _, _, c in g) + 16

    def h(w):
        return sum(row_h(w, row) for row in rows)

    def draw(d, x, y, w):
        for row in rows:
            g = geo(w, row)
            top = max(ih for _, _, ih, _ in g)
            for k, ((path, _), (cw, iw, ih, cap)) in enumerate(zip(row, g)):
                cx = x + k * (cw + gap)
                d.picture(path, cx + (cw - iw) / 2, y, iw, ih)
                jr.para(d, cx, y + top + 14, cap, cw, 28)
            y += row_h(w, row)
        return y
    return h, draw, cols * 880 + gap * (cols - 1)                  # how wide it wants: full-size shots, not squeezed


def as_item(x):
    return text_item(x) if isinstance(x, str) else x


def card(d: Drawing, x: float, y: float, w: float, h: float, title: str, body: list, color=INK, dashed=False) -> None:
    """A box: its title, then what it holds; never cut (its height comes from card_height)."""
    body = [it.translate(FONT_GAPS) if isinstance(it, str) else it for it in body]
    if color is not None:                                          # None: no box, a table in the open (b03's grid)
        d.box(x, y, w, h, color, 2.5, dashed=dashed)
    yy = (jr.para(d, x + 28, y + 22, title, w - 56, T_HEAD, color or INK) + 16) if title else y + 24
    for it in body:
        if isinstance(it, str):
            yy = jr.para(d, x + 28, yy, it, w - 56, T_BODY, color if color == RED else None) + 10
        else:
            yy = it[1](d, x + 28, yy, w - 56)


def card_height(title: str, body: list, w: float) -> float:
    body = [it.translate(FONT_GAPS) if isinstance(it, str) else it for it in body]
    return (22 + jr.tall(title, w - 56, T_HEAD) + 16 if title else 24) + sum(as_item(it)[0](w - 56) for it in body) + 24


def natural_width(b, most: float) -> float:
    """A box as wide as its words need (560 px at least, 1,300 for a list of drawn items), never more than `most`."""
    lines = [b[0]] + [ln for it in b[1] if isinstance(it, str) for ln in str(it).split("\n")]
    need = max([Drawing.measure(ln, T_BODY) for ln in lines] or [0]) + 70
    for it in b[1]:
        if not isinstance(it, str):
            need = max(need, it[2] + 56 if len(it) > 2 else 1300)   # an item may say how wide it wants to be
    return max(560, min(need, most))


STEP = 240                                                      # stairs: how far each row steps right
VIDEO_W = 6400                                                  # a video frame: wider, so fewer rows (JL 261012:
                                                                # "for each frame it can be even wider and less high")


def rows_of(d: Drawing, y: float, rows: list, labels: list, width: float = W, stairs: bool = True) -> float:
    """Boxes in rows, joined in reading order by named arrows; `rows`: [[(title, body, colour[, share]), …], …].
    Stairs, the default (⑧, asked 261012: "leave some rooms, not all the things nested together"; "I don't want this
    circle back line any more, give me the stair version"): each box only as wide as its words need, room between,
    each row stepped right of the one above and hanging off its first box by a short straight drop, never a line
    circling back across the frame; the frame is marked Drawing.room and fit() trims it to its boxes. stairs=False:
    the old rows, each as wide as the frame, the last box of a row leading back to the next row's first."""
    plain = getattr(d, "plain", False)                  # a face's layout: plain (asked 261012: "no need to have the
    gap, vgap = (120, 100) if plain else (180, 190) if stairs else (130, 110)   # --> all the time"): room, no arrows
    if (stairs or plain) and hasattr(d, "room"):
        frame = next((e for e in d.els if e.get("id") == getattr(d, "fid", None) and e["type"] == "frame"), None)
        if frame:
            d.room(frame)
    n, prev, first = 0, None, None
    for r, row in enumerate(rows):
        shares = [b[3] if len(b) > 3 else 1 for b in row]
        x0 = 40 + (min(r, 3) * STEP if stairs and not plain and len(rows) > 1 else 0)   # three steps right at most
        room = width - 40 - x0 - gap * (len(row) - 1)
        widths = [room * s_ / sum(shares) for s_ in shares]
        if stairs or plain:
            widths = [natural_width(b, bw * 0.9) for b, bw in zip(row, widths)]
        hh = max(card_height(b[0], b[1], bw) for b, bw in zip(row, widths))
        x = x0
        for k, (b, bw) in enumerate(zip(row, widths)):
            t, body, c = b[:3]
            card(d, x, y, bw, hh, t, body, c, dashed=c == RED)
            if prev is not None and not plain:
                px, py, pw, ph = prev
                words = labels[n - 1] if n - 1 < len(labels) else ""
                if k:                                           # side by side
                    d.line([(px + pw + 8, py + 46), (x - 8, y + 46)], sw=4)
                    if words:
                        jr.para(d, px + pw + 14, py + 60, words, gap - 24, T_ARROW)
                elif stairs and first:                          # stairs: a short straight drop from the row above's
                    fx, fy, fw, fh = first                      # first box into this row's first, stepped right
                    xc = min(x + 70, fx + fw - 30)
                    d.line([(xc, fy + fh + 6), (xc, y - 6)], sw=4)
                    if words:
                        jr.para(d, xc + 20, fy + fh + vgap / 2 - 18, words, bw, T_ARROW)
                else:                                           # the row's last box down to the next row's first
                    mid = py + ph + 55
                    d.line([(px + pw / 2, py + ph + 6), (px + pw / 2, mid), (x + bw / 2, mid), (x + bw / 2, y - 6)],
                           sw=4)
                    if words:
                        jr.para(d, x + bw / 2 + 20, mid + 6, words, bw, T_ARROW)
            prev, n = (x, y, bw, hh), n + 1
            if k == 0:
                row_first = (x, y, bw, hh)
            x += bw + gap
        first = row_first
        y += hh + vgap
    return y - vgap


def fit(d: Drawing, f: dict, bottom: float, detail: bool = False) -> dict:
    """The frame as tall as what is drawn in it, its badge in its corner; past one screen it reads down. A frame that
    teaches (terms, formulas, steps, shots) is where ⑦ sends the detail: marked so, it is held to ⑥'s text floor."""
    if detail and hasattr(d, "detail"):
        d.detail(f)
    if (f.get("customData") or {}).get("room"):                     # ⑧: the frame ends where its boxes end
        mine = [e for e in d.els if e.get("frameId") == f["id"]]
        wide_keys = [e for e in mine if e.get("backgroundColor") == KEY and e["width"] >= 0.8 * f["width"] - 80]
        boxes = [e for e in mine if e["type"] in ("rectangle", "image", "line") and e not in wide_keys
                 and not (e.get("customData") or {}).get("aside")]
        top = min((e["y"] for e in boxes), default=0)
        right = max((e["x"] + e["width"] for e in boxes), default=f["width"] - 60)
        said = max((e["x"] + max(Drawing.measure(ln, e.get("fontSize", T_BODY)) for ln in str(e.get("text", "")).split("\n"))
                    for e in mine if e["type"] == "text" and e["y"] < top), default=0)   # the heading's words, not their wrap box
        f["width"] = new = max(NARROW, right + 60, said + 100)   # shrink to the boxes, or grow to hold them
        for k in wide_keys:
            k["width"] = new - 2 * k["x"]
    f["height"] = max(bottom + 40, 700)
    if f["height"] > TALLEST:
        canvas.reads_down(f)
    if f["width"] > W and hasattr(canvas, "large"):                 # a chain of step boxes wider than a screen
        canvas.large(f)
    d.badge(f)
    return f


# ── the words a beginner needs: terms, formulas, steps ─────────────────────────────────────────────────────
def terms_items(terms) -> list:
    """Words to know first: each term, then what it means in plain words."""
    out = []
    for t in terms or []:
        term, means = (t.get("term"), t.get("means")) if isinstance(t, dict) else (t, "")
        out.append(text_item(f"▪ {term}", T_BODY + 2, after=4))
        if means:
            out.append(text_item(str(means), T_BODY, indent=34, after=14))
    return out


def formula_items(formulas, assets: Path) -> list:
    """Each formula: drawn as math, what it says in words, each symbol, and a worked example with numbers."""
    out = []
    for k, fm in enumerate(formulas or []):
        if not isinstance(fm, dict) or not fm.get("tex"):
            continue
        if k:
            out.append(text_item(" ", 20, after=10))
        if fm.get("name"):
            out.append(text_item(str(fm["name"]), T_BODY + 2, after=8))
        out.append(tex_item(str(fm["tex"]), assets))
        if fm.get("means"):
            out.append(text_item(f"In words: {fm['means']}", T_BODY, after=14))
        for sym in fm.get("symbols") or []:
            if isinstance(sym, (list, tuple)) and len(sym) == 2:
                out.append(sym_item(str(sym[0]), str(sym[1]), assets))
        if fm.get("example"):
            out.append(text_item(f"Worked example: {fm['example']}", T_BODY, after=10))
    return out


def steps_items(steps, fallback: list) -> list:
    """The steps in order: each a short point, then why it holds in plain words."""
    out = []
    for i, st in enumerate(steps or []):
        point, why = (st.get("point"), st.get("why")) if isinstance(st, dict) else (st, "")
        out.append(text_item(f"{CIRCLED[i % len(CIRCLED)]} {point}", T_BODY + 2, after=4))
        if why:
            out.append(text_item(str(why), T_BODY, indent=40, after=16))
    return out or [text_item(f"{CIRCLED[i]} {p}", T_BODY + 2, after=12) for i, p in enumerate(fallback[:len(CIRCLED)])]


def step_rows(steps, fallback: list, mark: str, per_row: int = 0, lead: list | None = None) -> list:
    """Each step its own box, "① point" over its why, in reading order, joined by rows_of's arrows; one row unless
    `per_row` is given (then balanced: 5 draw 3 + 2). Asked 261012: "make the concept to be the box and use --> to
    link them" and "don't limited yourself of the size of the frame": the frame widens to the chain (chain_width).
    A page point with " - " sub-points keeps its lead as the title and lists each sub-point on its own line."""
    items = []
    for i, st in enumerate(steps or []):
        point, why = (st.get("point"), st.get("why")) if isinstance(st, dict) else (st, "")
        items.append((f"{CIRCLED[i % len(CIRCLED)]} {point}", [str(why)] if why else []))
    for k, (t, b) in enumerate(items):                               # a long point with no why: its number heads it
        words = t.split(" ", 1)
        if not b and len(t.split()) > 12 and len(words) > 1:
            items[k] = (words[0], [words[1]])
    if not items:
        for i, pt in enumerate(fallback[:len(CIRCLED)]):
            parts = [x.strip() for x in re.split(r"\s+-\s+(?=[A-Z])", str(pt)) if x.strip()]
            items.append((f"{CIRCLED[i]} {parts[0]}", [f"· {x}" for x in parts[1:]]))
    if not items:
        return []
    if lead:                                                          # the page's lead line: its own first box
        items.insert(0, (f"{mark} How it works", lead))
    else:
        items[0] = (f"{mark} {items[0][0]}", items[0][1])           # the chain's first box carries its section mark
    per_row = per_row or len(items)
    nrows = -(-len(items) // per_row)
    cols = -(-len(items) // nrows)
    boxes = [(t, b, INK) for t, b in items]
    return [boxes[k:k + cols] for k in range(0, len(boxes), cols)]


def chain_width(rows: list) -> float:
    """How wide a frame must be for its widest row of step boxes, each STEP_W, never under W."""
    n = max((len(r) for r in rows), default=0)
    return max(W, 80 + n * STEP_W + max(n - 1, 0) * STEP_GAP)


def pdf_pages(run: dict, assets: Path, name: str = "transcript-article.pdf", dpi: int = 110) -> list:
    """The pages of a Run's transcript PDF as pictures for its frame: rendered once by pdftoppm into assets/
    (rNN-article-pN.png), again only when the PDF is newer. Asked 261012 on b11 s47: "where is the screen shot
    of the transcripts pdf here?" Returns [(png, caption)], empty when the Run has no such PDF."""
    res = run.get("result")
    pdf = Path(res) / name if res else None
    if not pdf or not pdf.is_file() or not shutil.which("pdftoppm"):
        return []
    stem = f"{run['rid']}-article"
    have = sorted(assets.glob(f"{stem}-p*.png"))
    if not have or min(p.stat().st_mtime for p in have) < pdf.stat().st_mtime:
        assets.mkdir(parents=True, exist_ok=True)
        for old in have:
            old.unlink()
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(assets / f"{stem}-p")], check=True)
        have = sorted(assets.glob(f"{stem}-p*.png"), key=lambda p: int(re.sub(r"\D", "", p.stem.split("-p")[-1]) or 0))
    have = sorted(have, key=lambda p: int(re.sub(r"\D", "", p.stem.split("-p")[-1]) or 0))
    return [(png, f"page {k + 1} of {len(have)} · {name}") for k, png in enumerate(have)]


def picture_item(path: Path, tallest: float = 900):
    """One picture as a box item: as wide as the box allows, at most `tallest` high."""
    def h(w):
        iw, ih = size_of(path)
        return min(w / iw, tallest / ih) * ih + 14

    def draw(d, x, y, w):
        iw, ih = size_of(path)
        sc = min(w / iw, tallest / ih)
        d.picture(path, x, y, iw * sc, ih * sc)
        return y + h(w)
    return h, draw


ROLE_MARK = {"question": "❓", "gap": "🕳️", "method": "🛠️", "result": "📊", "claim": "💬", "limit": "⚠️"}


def reading_rows(run: dict, assets: Path, passages: bool = True) -> tuple[list, list]:
    """The video's transcript read with /excalidraw-read (the topic's reads/<rid>-*/reading.yaml and its shots):
    its logic as a chain of boxes, then each highlighted passage as a card, Says · Comment · → this Task.
    Asked 261012 on b11 s47: "please read /excalidraw-read But we need to prepare the pdf of each video first".
    Returns (rows, labels for the arrows into each box); none when the Run has no reading. passages=False: the logic
    only, when the video's transcript frame shows the passages on its pages instead."""
    found = sorted((assets.parent / "reads").glob(f"{run['rid']}-*/reading.yaml"))
    if not found or yaml is None:
        return [], []
    folder = found[0].parent
    spec = yaml.safe_load(found[0].read_text()) or {}
    try:
        shots = {r["id"]: r for r in json.loads((folder / "shots" / "index.json").read_text())}
    except (OSError, ValueError):
        shots = {}
    targets = {t["id"]: t.get("label", t["id"]) for t in (spec.get("ours") or {}).get("targets") or []}
    logic = [(f"{ROLE_MARK.get(st.get('role'), '▪')} {st.get('role', '')} · " +   # E2 as ②, the transcript frame's number
              ", ".join(circled(excerpt_number(e, 0)) if re.fullmatch(r"E\d+", str(e)) else str(e)
                        for e in st.get("excerpts") or []), [str(st.get("text", ""))], INK) for st in spec.get("logic") or []]
    cards = []
    for ex in (spec.get("excerpts") or []) if passages else []:
        rec = shots.get(ex["id"]) or {}
        body = []
        if rec.get("shot") and (folder / rec["shot"]).is_file():
            dst = assets / f"{run['rid']}-read-{ex['id']}.jpg"           # one name per video: pictures are keyed by name
            assets.mkdir(parents=True, exist_ok=True)
            if not dst.is_file() or dst.stat().st_mtime < (folder / rec["shot"]).stat().st_mtime:
                shutil.copy(folder / rec["shot"], dst)
            body.append(picture_item(dst))
        else:
            body.append(f"❓ {ex['id']}: the quote was not found in the PDF")
        body += [f"Says: {ex.get('says', '')}", f"Comment: {ex.get('comment', '')}"]
        link = ex.get("link") or {}
        if link.get("to"):
            body.append(f"→ This Task, {targets.get(link['to'], link['to'])} ({link.get('relation', '')}): {link.get('how', '')}")
        cards.append((f"{ex['id']} · p.{rec.get('page', ex.get('page', '?'))} · {ex.get('label', '')}", body,
                      INK if rec.get("shot") else RED))
    rows = [logic[k:k + 4] for k in range(0, len(logic), 4)] + [cards[k:k + 5] for k in range(0, len(cards), 5)]
    labels = (["read the transcript"] + [""] * (len(logic) - 1) if logic else []) + \
        (["its passages"] + [""] * (len(cards) - 1) if cards else [])
    return rows, labels


def shot_files(run: dict, w: dict, assets: Path) -> list:
    """The screenshots the face picks (`shots: [{at: seconds, says: …}]`), copied once from the video's frames into
    assets/, the slide's empty margins cropped; returns [(file, caption)]."""
    import video_frames as vf
    out = []
    for sh in w.get("shots") or []:
        at = float(sh.get("at", 0)) if isinstance(sh, dict) else float(sh)
        dst = assets / f"{run['rid']}-t{int(at):04d}.jpg"
        if not dst.is_file() and run["url"]:
            try:
                src = vf.nearest(vf.cache_of(run["url"], run.get("result") or assets), at)   # from the Run, not a preview's scratch
            except SystemExit:
                src = None
            if src:
                assets.mkdir(parents=True, exist_ok=True)
                crop_band(src).save(dst, quality=85)
        if dst.is_file():
            cap = f"{int(at) // 60}:{int(at) % 60:02d} · {sh.get('says', '') if isinstance(sh, dict) else ''}"
            out.append((dst, cap.rstrip(" ·")))
    return out


def crop_band(path: Path):
    """A slide video's frame without its empty top and bottom: from the first to the last band of rows with marks,
    leaving out a channel's watermark (a band wholly in the top tenth)."""
    import numpy as np
    from PIL import Image
    img = Image.open(path).convert("RGB")
    a = np.asarray(img.convert("L"), dtype=float)
    rows_h = a.shape[0]
    marked = (a > 110).sum(axis=1) > a.shape[1] * 0.01
    bands, start, last = [], None, None
    gap_ok = max(4, int(rows_h * 0.04))
    for i, b in enumerate(marked):
        if b:
            if start is None:
                start = i
            elif i - last > gap_ok:
                bands.append((start, last))
                start = i
            last = i
    if start is not None:
        bands.append((start, last))
    bands = [bd for bd in bands if bd[1] > rows_h * 0.10 and bd[1] - bd[0] > 3]
    if not bands:
        return img
    lo, hi = bands[0][0], bands[-1][1]
    if hi - lo > rows_h * 0.85:
        return img
    pad = int(rows_h * 0.025)
    return img.crop((0, max(0, lo - pad), a.shape[1], min(rows_h, hi + pad)))


# ── the frames ───────────────────────────────────────────────────────────────────────────────────────────────
def idea_frame(d: Drawing, task: dict, folder: Path, runs: list, cfg: dict, assets: Path) -> dict:
    """The Task for someone who knows nothing yet: its question; what it is and the words to know first; the core
    formula explained and how it works; why it matters, the videos in reading order, the questions to be ready for."""
    idea, words = cfg.get("idea") or {}, {**(cfg.get("videos") or {}), **(cfg.get("runs") or {})}
    tid = folder.name[:3]
    noun = "Runs" if task.get("work") or any(r.get("work") for r in runs) else "videos"
    mech = idea.get("mechanism") or [{"point": h, "why": ""} for h in idea.get("how") or []]
    lead = [] if mech else [first(task["how"], 300)]                # from the page: its lead line, then its steps
    mech = mech or task["how_steps"]
    wide = noun != "Runs"                                           # one long chain only for a video Task (JL, b11)
    how = step_rows(mech, [], "⚙️", per_row=0 if wide else 3, lead=[x for x in lead if x]) if mech else []
    width = chain_width(how) if wide else W                         # a work Task keeps ⑥'s density at W
    title = re.sub(r"^t\d+\s*·\s*", "", task["title"])          # a page titled "t05 · …" would say t05 twice
    f = d.frame(f"⓪ {tid} · {title}: the idea and its {len(runs)} {noun}", width, TALLEST)
    done = sum(video_checked(r["state"]) for r in task["runs"])
    key = str(cfg.get("reading") or idea.get("question") or task["question"] or task["title"])
    y = heading(d, f"{tid} · {title}", f"{folder.parent.name} · {len(task['runs'])} {noun}" +
                ("" if noun == "Runs" else f" · {done} checked against the video"), key, width)
    work = noun == "Runs"
    det = steps_items(idea.get("details") or task["details"], [])
    vids = [f"{jr.mark(r['state']) if work else '★' if r['star'] else '🎬'} {r['rid'] if not work else r['rid'][:3]} · "
            f"{(words.get(r['rid']) or {}).get('name') or r['short']}" for r in runs]
    if not vids:                                                   # an empty box says why it is empty
        vids = ["⬜ no Run in this Task yet"] if work else ["❓ no video listed on the page"]
    if not work and any(r["star"] for r in runs):                  # what the marks shown mean
        vids.append("★ tagged a frequent interview question" + (" · 🎬 the others" if not all(r["star"] for r in runs) else ""))
    qs = qa_items(idea.get("questions")) or qa_items(task["questions"][:6])
    what = str(idea.get("intro") or " ".join(x for x in (first(task["what"], 400), task["mental"]) if x) or task["question"])
    page = [f"{icon} {label}: {first(task[k], 300)}" for k, icon, label in      # the page's own frame for the reader
            (("mental", "🧠", "Picture it"), ("outcome", "✅", "After this you can"), ("path", "🧭", "Core path"))
            if task.get(k) and (k != "mental" or idea.get("intro"))]
    why = [str(idea["why"])] if idea.get("why") else [first(task["why"], 300)] + [f"· {first(x, 160)}" for x in task["why_points"][:5]]
    terms, formulas = terms_items(idea.get("terms")), formula_items(idea.get("formula"), assets)
    if task.get("sketch"):                                           # the page's own sketch, under Picture it
        at = next((k + 1 for k, ln in enumerate(page) if ln.startswith("🧠")), 0)
        page = page[:at] + [code_item(task["sketch"])] + page[at:]
    how = how or [[("⚙️ How it works, step by step", lead or ["❓ no steps written on the page"], INK)]]
    rows = [[("💡 What it is", [what] + page, INK, 1)] + ([("📖 Words to know first", terms, INK, 1)] if terms else [])] + \
        ([[("🧮 The core formula, explained", formulas, INK)]] if formulas else []) + how + \
        ([[("🔍 Why it is built this way", det, INK)]] if det else []) + \
        [[("🎯 Why it matters", why, INK), (f"🧪 The {len(runs)} Runs, in order" if work else
                                            f"🎬 The {len(runs)} videos, in reading order", vids, INK),
          ("🎤 Be ready to answer", qs or ["❓ none written on the page"], INK)]]
    labels = ["the words first"] if terms else []
    labels += (["the math", "how it runs"] if formulas else ["how it runs"]) + [""] * (sum(map(len, how)) - 1) + \
        (["why so"] if det else []) + \
        ["why it matters", "its Runs" if work else "watch", "then answer"]   # a work Task has Runs, not videos
    opens = [f"❓ {str(o).lstrip('❓ ')}" for o in cfg.get("open") or []] or [f"❓ {x}" for x in task.get("limits") or []]
    if opens:
        rows.append([("❓ What is not checked yet, and what comes next", opens, RED)])
        labels.append("still open")
    bottom = rows_of(d, y, rows, labels, width)
    return fit(d, f, bottom, detail=bool(any(idea.get(k) for k in ("intro", "terms", "formula", "mechanism")) or det))


def failure_line(fail, most: int = 160) -> str:
    """Why a Run failed, in one line: a receipt's {type, message} as its type and the message's last line (a
    traceback ends on the error itself), never the whole traceback."""
    if not fail:
        return ""
    if isinstance(fail, dict):
        msg = str(fail.get("message") or "").replace("\\n", "\n")
        lines = [re.sub(r"^\(\w+ pid=\d+\)\s*", "", ln.strip()) for ln in msg.splitlines()]
        lines = [ln for ln in lines if ln and not set(ln) <= set("^~") and "further information" not in ln]
        last = next((ln for ln in reversed(lines) if re.search(r"error|exception", ln, re.I)), lines[-1] if lines else "")
        line = ": ".join(x for x in (str(fail.get("type") or ""), last) if x)
    else:
        line = first(str(fail), most)
    line = " ".join(line.split())
    return line if len(line) <= most else line[:most].rsplit(" ", 1)[0] + " …"


def run_lines(run: dict) -> list[str]:
    """The Run itself, from its receipts: address and date, state, worker, transcript, result files."""
    res = run.get("result")
    if not res or not res.is_dir():
        return [f"❓ no result folder on disk for {run['rid']}"]
    try:
        rt = yaml.safe_load(jr.read(res / "runtime.yaml")) or {} if yaml else {}
    except Exception:
        rt = {}
    facts = dict(re.findall(r"^-\s*([^:]+):\s*(.+)$", jr.read(res / "facts.md"), re.M))
    when = str(rt.get("executed_at") or rt.get("started_at") or "")[:10]
    out = [f"{rt.get('address') or run['rid']}{' · run ' + when if when else ''}"]
    state = str(run.get("state") or rt.get("status") or "?")      # the face's state or the receipt's, as the header
    why = failure_line(rt.get("failure")).replace("Automatic ASR", "ASR (automatic speech recognition)")
    out.append(f"{jr.mark(state)} {state}{': ' + why if why else ''}")
    worker = (rt.get("worker") or {}).get("name") if isinstance(rt.get("worker"), dict) else rt.get("worker")
    segs = facts.get("Segment count")
    if worker:
        gloss = " (the speech-to-text model)" if "whisper" in str(worker).lower() else ""
        out.append(f"worker: {worker}{gloss}{f' · {segs} transcript segments' if segs else ''}")
    if run.get("transcript_file"):                                   # the topic's own copy, next to its screenshots
        out.append(f"transcript: {run['transcript_file']} (in this topic)")
    elif rt.get("transcript"):
        out.append(f"transcript: {Path(str(rt['transcript'])).name} (outside git, in _WorkSpace)")
    files = sorted(p.name for p in res.iterdir() if p.is_file())
    said = {"facts.md": "facts.md (its numbers)", "runtime.yaml": "runtime.yaml (the run's record)",
            "Result Card": "Result Card (its summary page)",                # what each receipt is, for a newcomer
            "transcript-article.pdf": "transcript-article.pdf (the video as an article)",
            "transcript-original.pdf": "transcript-original.pdf (every word, timed)"}
    out.append("files: " + " · ".join(said.get(n, n) for n in
                                      (("Result Card" if f.startswith(run["rid"] + "_") else f) for f in files)))
    try:
        out.append(f"folder: {Path(res).relative_to(Path(res).parents[3]).as_posix()}/")
    except (ValueError, IndexError):
        pass
    return out


def plot_png(run: dict, spec: dict, assets: Path, k: int) -> Path | None:
    """A curve from a Run's result: `key` (a list in a json, or a list of {x, y}) or `regex` over a log (x and y, or
    y alone); drawn by matplotlib into assets/."""
    import json as _json
    res = run["result"]
    path = res / str(spec.get("file", ""))
    if not path.is_file():
        return None
    xs, ys = [], []
    if spec.get("regex"):
        for m in re.finditer(spec["regex"], jr.read(path)):
            g = m.groups()
            try:
                if len(g) >= 2:
                    xs.append(float(g[0])); ys.append(float(g[1]))
                else:
                    ys.append(float(g[0]))
            except ValueError:
                continue
    else:
        try:
            seq = jd_dig(_json.loads(jr.read(path)), str(spec.get("key", "")))
        except Exception:
            seq = None
        for i, v in enumerate(seq or []):
            if isinstance(v, dict):
                xs.append(float(v.get(spec.get("x", "x"), i))); ys.append(float(v.get(spec.get("y", "y"), 0)))
            elif isinstance(v, (int, float)):
                ys.append(float(v))
    if len(ys) < 2:
        return None
    xs = xs or list(range(1, len(ys) + 1))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    assets.mkdir(parents=True, exist_ok=True)
    out = assets / f"plot-{run['rid']}-{k}.png"
    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=150)
    ax.plot(xs, ys, color="#1e1e1e", linewidth=2)
    ax.set_xlabel(str(spec.get("x_label", "step")), fontsize=13)
    ax.set_ylabel(str(spec.get("y_label", spec.get("title", ""))), fontsize=13)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


def jd_dig(data, key: str):
    for part in [p for p in key.split(".") if p]:
        data = data.get(part) if isinstance(data, dict) else None
    return data


def picks_lines(run: dict, picks) -> list[str]:
    """`{label, at, fmt, unit}` read from the Run's result (job_results' readers); a list of `at` is before → after.
    `{label, file, regex, which, fmt, unit}` reads the regex's first group from a text file there (a log), first match
    unless `which: last`: a Run whose numbers live only in its log."""
    out = []
    for p in picks or []:
        if not isinstance(p, dict):
            continue
        if p.get("regex") and p.get("file"):
            hits = re.findall(str(p["regex"]), jr.read(run["result"] / str(p["file"])))
            hit = (hits[-1] if p.get("which") == "last" else hits[0]) if hits else None
            hit = hit[0] if isinstance(hit, tuple) else hit
            try:
                hit = float(hit) if hit is not None else None
            except ValueError:
                pass
            unit = f" {p['unit']}" if p.get("unit") else ""
            out.append(f"{p.get('label', '')} {jr.number(hit, str(p.get('fmt', '')))}{unit} ({p['file']})".strip()
                       if hit is not None else f"❓ {p.get('label', '')}: not in {p['file']}")
        else:
            out += jr.shown(run, [p])
    return out


CELL = 470                                                      # one scoreboard cell's width


def big_values(values: list) -> list:
    """The measured values as a scoreboard (asked 261012: "for a task, we want to salient show the numbers and the
    values"): side by side, each its label at body size over its number large; a value with no number stays a line."""
    cells, plain_ = [], []
    for v in values:
        num = r"[-−]?\d[\d,.]*\s*(?:%|s|GB|MB|tok/s|x)?"              # the value is the number at the end
        m = re.match(rf"^(.*?)\s*((?:{num}\s*→\s*)*{num})\s*(\([^)]*\))?\s*$", str(v))
        if m and m.group(1) and not str(v).startswith("❓"):
            cells.append((m.group(1) + (f" {m.group(3)}" if m.group(3) else ""), m.group(2)))
        else:
            plain_.append(str(v))
    if not cells:
        return plain_

    def layout(w):
        per = max(1, min(len(cells), int(w // CELL)))
        rows = [cells[k:k + per] for k in range(0, len(cells), per)]
        return per, rows, [max(jr.tall(a, CELL - 30, T_BODY) + jr.tall(b, CELL - 30, 56) for a, b in r) + 30 for r in rows]

    def h(w):
        return sum(layout(w)[2])

    def draw(d, x, y, w):
        per, rows, hs = layout(w)
        for r, hh in zip(rows, hs):
            for k, (a, b) in enumerate(r):
                cx = x + k * CELL
                yy = jr.para(d, cx, y, a, CELL - 30, T_BODY)
                jr.para(d, cx, yy + 2, b, CELL - 30, 56)
            y += hh
        return y
    return [(h, draw, min(len(cells), 4) * CELL)] + plain_


TABLE_W = 2200                                                  # a Run's table, nearly a screen wide


def table_item(run: dict, spec: dict):
    """A Run's measured values as b03's grid (asked 261012: "I want the tables like this"): `{columns, rows: [{label,
    cells: [{at, fmt, unit} | words], dim}], caption}`; each value read from the Run's result, its number large. A dim
    row (a reference typed in, not measured here) is grey."""
    cols = [str(c) for c in spec.get("columns") or []]
    rows = []
    for r in spec.get("rows") or []:
        cells = [str(r.get("label", ""))]
        for c in r.get("cells") or []:
            if isinstance(c, dict) and c.get("at"):
                v = jr.at_value(run["result"], str(c["at"]), str(c.get("fmt", "")))
                cells.append({"big": f"{v}{(' ' + c['unit']) if c.get('unit') else ''}" if v is not None else "?",
                              "tag": str(c.get("tag", "")), "color": RED if v is None else None})
            else:
                cells.append(str(c.get("text", "")) if isinstance(c, dict) else ("" if c is None else str(c)))
        rows.append({"cells": cells, "dim": bool(r.get("dim"))})
    cap = str(spec.get("caption") or "")

    def widths(w):
        first = max([Drawing.measure(str(r["cells"][0]), T_BODY) for r in rows] + [300]) + 40
        first = min(first, w * 0.42)
        return [first] + [(w - first) / max(1, len(cols) - 1)] * (len(cols) - 1)

    def h(w):
        return Drawing().grid_table(0, 0, cols, rows, widths(w), T_BODY) + (jr.tall(cap, w, 28) + 20 if cap else 0)

    def draw(d, x, y, w):
        y = d.grid_table(x, y, cols, rows, widths(w), T_BODY)
        return jr.para(d, x, y + 16, cap, w, 28) if cap else y
    return (h, draw, TABLE_W)


def work_rows(run: dict, w: dict, assets: Path, big: bool = False) -> list:
    """A work Run's first rows: ⚙️ what it ran ─▶ 📊 what it measured, then 📈 its curves. `big`: the numbers large."""
    ran = picks_lines(run, w.get("config"))
    measured = picks_lines(run, w.get("show")) or jr.found_values(run) or [f"❓ no known number in {run['rid']}'s result"]
    shown = big_values(measured) if big else [f"· {x}" for x in measured]
    first = ([("⚙️ What it ran", [f"· {x}" for x in ran], INK, 1)] if ran else []) + \
        [("📊 What it measured", shown, INK, 1.2)]
    if w.get("table"):                                             # the table first, in the open; what it ran below
        first = [[("📊 What it measured", [table_item(run, w["table"])], None)]] + \
            ([[("⚙️ What it ran", [f"· {x}" for x in ran], INK, 1)]] if ran else [])
        return first
    curves = []
    for k, spec in enumerate(w.get("plot") or []):
        png = plot_png(run, spec, assets, k) if isinstance(spec, dict) else None
        if png:
            curves.append((png, str(spec.get("title", ""))))
    return [first] + ([[("📈 How it moved during the Run", [shots_item(curves, 520)], INK)]] if curves else [])


PAGE_W, NOTE_W = 1500, 2300                                     # a transcript page's width; a note's, wide so short
LONG_PDF = 4                                                    # past this many pages, only the pages with passages
MARKER = "#ffe86e"                                              # read_paper's HIGHLIGHT, the yellow on the pages


def excerpt_number(ex_id: str, k: int) -> int:
    """An excerpt's number: E3 is 3; any other id, its place in reading order."""
    m = re.fullmatch(r"E(\d+)", str(ex_id))
    return int(m.group(1)) if m else k


def circled(n: int) -> str:
    return chr(0x2460 + n - 1) if 1 <= n <= 20 else f"({n})"


def number_badge(d: Drawing, x: float, y: float, n: int, size: float = 66) -> None:
    """A passage's number in a circle of the highlight's own yellow, drawn beside the passage and beside its note
    (JL 261012: "for the index, why not with 1, 2, 3, 4, with the circles"), so no arrow has to cross between them."""
    d.el("ellipse", x, y, size, size, strokeColor=INK, strokeWidth=2.5, backgroundColor=MARKER, fillStyle="solid")
    s, fs = str(n), 36
    d.text(x + (size - Drawing.measure(s, fs) - 4) / 2, y + (size - fs * 1.25) / 2, s, fs)


def read_of(run: dict, assets: Path):
    """A video's /excalidraw-read reading (the topic's reads/<rid>-*/reading.yaml): (its folder, the spec), or None."""
    found = sorted((assets.parent / "reads").glob(f"{run['rid']}-*/reading.yaml"))
    if not found or yaml is None:
        return None
    return found[0].parent, yaml.safe_load(found[0].read_text()) or {}


def transcript_pages(run: dict, assets: Path, dpi: int = 200) -> tuple[list, list, int]:
    """The reading's PDF (the Run's transcript-article.pdf), each page whole, its excerpts' quotes highlighted in
    place as /excalidraw-read shoots them (read_paper's find, the same marker yellow multiplied onto the page):
    assets/<rid>-transcript-p<N>.jpg, rendered again when the PDF or the reading is newer. A transcript of more than
    LONG_PDF pages (b11 s39 r08, a 2h 26m video, has 42) shows only its pages with passages, each cut from a few
    lines above its first passage to a few below its last (<rid>-transcript-p<N>-band.jpg). Returns
    ([(picture, (width, height), [(excerpt, [line boxes in the picture's pixels])], page number)], excerpts not
    found, the PDF's page count)."""
    got = read_of(run, assets)
    if not got:
        return [], [], 0
    folder, spec = got
    pdf = (folder / str((spec.get("paper") or {}).get("pdf") or "")).resolve()
    if not pdf.is_file() or not shutil.which("pdftoppm"):
        return [], [], 0
    sys.path.insert(0, str(SKILLS / "display/excalidraw-read/ref"))
    import read_paper as rp
    from PIL import Image, ImageChops, ImageDraw
    pages, k = rp.words_of(pdf), dpi / 72
    marks, missing = {}, []
    for ex in spec.get("excerpts") or []:
        order = ([int(ex["page"])] if ex.get("page") else []) + \
            [n for n in range(1, len(pages) + 1) if n != ex.get("page")]
        best = (0.0, None, [])
        for n in order:                                         # the page the reading names first, then the rest
            r, hits = rp.find(pages[n - 1], ex.get("quote") or "")
            if r > best[0]:
                best = (r, n, hits)
            if best[0] >= 0.8:
                break
        if best[0] < 0.8:
            missing.append(ex)
            continue
        lines = {}
        for w_, bi, li in best[2]:
            lines.setdefault((bi, li), []).append(w_["b"])
        boxes = sorted(([v * k for v in rp.union(b)] for b in lines.values()), key=lambda b: (b[1], b[0]))
        marks.setdefault(best[1], []).append((ex, boxes))
    newest = max(pdf.stat().st_mtime, (folder / "reading.yaml").stat().st_mtime)
    out, long, line = [], len(pages) > LONG_PDF, 19 * k              # line: the article's 18.5 pt leading
    for n, page in enumerate(pages, 1):
        if long and n not in marks:
            continue
        band = None
        if long:                                                      # cut between whole lines, never through one
            want = (min(b[1] for _, bx in marks[n] for b in bx) - 6 * line, max(b[3] for _, bx in marks[n] for b in bx) + 4 * line)
            rows = sorted((ln["b"][1] * k, ln["b"][3] * k) for bl in page["blocks"] for ln in bl["l"])
            band = (max(0, int(max([t for t, _ in rows if t <= want[0]], default=want[0]) - 0.3 * line)),
                    int(min([e for _, e in rows if e >= want[1]], default=want[1]) + 0.3 * line))
        dst = assets / f"{run['rid']}-transcript-p{n}{'-band' if long else ''}.jpg"
        if not dst.is_file() or dst.stat().st_mtime < newest:
            assets.mkdir(parents=True, exist_ok=True)
            tmp = assets / f".{dst.stem}"
            subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", str(dpi), "-png", "-singlefile", str(pdf),
                            str(tmp)], check=True)
            im = Image.open(tmp.with_suffix(".png")).convert("RGB")
            tmp.with_suffix(".png").unlink()
            mask = Image.new("RGB", im.size, (255, 255, 255))
            dr = ImageDraw.Draw(mask)
            for _, boxes in marks.get(n, []):
                for x0, y0, x1, y1 in boxes:
                    dr.rectangle([x0 - 2, y0 - 1, x1 + 2, y1 + 2], fill=rp.HIGHLIGHT)
            im = ImageChops.multiply(im, mask)
            ends = [b["b"][3] for b in page["blocks"]                # a short page ends where its words end,
                    if not "".join(w_["t"] for ln in b["l"] for w_ in ln["w"]).isdigit()]   # not at its page number
            if band:
                im = im.crop((0, band[0], im.width, min(im.height, band[1])))
            elif ends:
                im = im.crop((0, 0, im.width, min(im.height, int((max(ends) + 30) * k))))
            im.save(dst, "JPEG", quality=85, optimize=True)
        here = marks.get(n, [])
        if band:                                                      # the boxes, measured from the band's top
            here = [(ex, [(x0, y0 - band[0], x1, y1 - band[0]) for x0, y0, x1, y1 in bx]) for ex, bx in here]
        out.append((dst, size_of(dst), here, n))
    return out, missing, len(pages)


def transcript_frame(d: Drawing, run: dict, w: dict, assets: Path, noun: str = "transcript",
                     us: str = "This Task") -> dict | None:
    """The video's transcript as /excalidraw-read reads a paper (JL 261012 on b11 s47: "the pdf of the transcript
    should be looks like what we did in the /excalidraw-read, to put them in the most left, and highlight them, and
    in the right, we give the comments"): its PDF pages whole on the left, each read passage highlighted where it
    stands, and to their right one note per passage, level with it (Says · Comment · → this Task), in one column in
    the passages' order. Each passage and its note carry the same number in a yellow circle, the passage's in the
    page's margin; no arrows (JL 261012, after long slanted ones: "this looks ugly"). None when the video has no
    reading. `noun` and `us` name the source and what it links to: a related paper reads "The paper, read" and
    "→ Our paper" (excalidraw-read's topic_drawing.py)."""
    pages, missing, total = transcript_pages(run, assets)
    if not pages:
        return None
    _, spec = read_of(run, assets)
    targets = {t["id"]: t.get("label", t["id"]) for t in (spec.get("ours") or {}).get("targets") or []}
    pdf_name = Path(str((spec.get("paper") or {}).get("pdf") or "")).name
    name = f"{run['rid']} · The {noun}, read"
    f = d.frame(name, W, TALLEST)
    d.room(f)
    shown = (f"{total} pages, the {len(pages)} with passages shown, each cut to them" if total > len(pages) else
             f"{total} page{'s' if total > 1 else ''}")
    sub = f"📄 {pdf_name} · {shown} · each yellow passage is numbered; its note on the right carries the same number"
    y = heading(d, name, sub, str(w.get("says") or run["summary"] or f"❓ no summary for {run['rid']}"), W)
    px, notes, top = 150, [], y
    for img, (iw, ih), marks, n in pages:
        sc = PAGE_W / iw
        d.box(px - 2, top - 2, PAGE_W + 4, ih * sc + 4, INK, 1)
        embed(d, img, px, top, PAGE_W, ih * sc)
        d.files["img-" + img.stem]["mimeType"] = "image/jpeg"
        for ex, boxes in marks:
            notes.append((top + boxes[0][1] * sc, n, ex))
        top += ih * sc + 60
    nx, below = px + PAGE_W + 200, y
    for k, (at, n, ex) in enumerate(sorted(notes, key=lambda t: t[0]), 1):
        num = excerpt_number(ex["id"], k)
        number_badge(d, 50, at - 10, num)                           # beside the passage, in the page's margin
        link = ex.get("link") or {}
        body = [f"Says: {ex.get('says', '')}", f"Comment: {ex.get('comment', '')}"] + \
            ([f"→ {us}, {targets.get(link['to'], link['to'])} ({link.get('relation', '')}): {link.get('how', '')}"]
             if link.get("to") else [f"❓ not linked to {us.lower()}"])
        title = f"{ex.get('label', '')} · p.{n}"
        hh = card_height(title, body, NOTE_W)
        ny = max(at - 20, below)                                    # level with its passage, else just below the last
        number_badge(d, nx - 96, ny + 10, num)                      # and beside its note
        card(d, nx, ny, NOTE_W, hh, title, body, INK if link.get("to") else RED)
        below = ny + hh + 40
    bottom = max(top - 60, below)
    for ex in missing:                                              # a quote the PDF does not hold: red, never hidden
        bottom += 40
        body = [f"Quote: {ex.get('quote', '')}", f"Says: {ex.get('says', '')}"]
        hh = card_height(f"❓ {ex['id']} · not found in the PDF", body, NOTE_W)
        card(d, nx, bottom, NOTE_W, hh, f"❓ {ex['id']} · not found in the PDF", body, RED, dashed=True)
        bottom += hh
    return fit(d, f, bottom, detail=True)


def source_frame(d: Drawing, run: dict, w: dict, assets: Path, stairs: bool = True, passages: bool = True) -> dict:
    """One video for someone who knows nothing yet: what it says; what the screen shows and the words to know
    first; its formula explained and its steps, each with why; how to say it and what to check (red)."""
    name = f"{run['rid']} · {w.get('name') or run['short']}"
    work = run.get("work")
    mine = sorted((assets.parent / "transcripts").glob(f"{run['rid']}-*.md"))
    if mine:
        run["transcript_file"] = f"transcripts/{mine[0].name}"
    shots = [] if work else shot_files(run, w, assets)
    formulas = formula_items(w.get("formula"), assets)
    top = work_rows(run, w, assets, big=stairs) if work else []
    pts = [str(p) for p in w.get("points") or []] or [first(s_, 400) for s_ in sentences(run["key"])][:5] or \
        ["❓ no key points written yet"]
    bullets = []
    for item in run.get("key_items") or []:                        # the page's bullets, up to its hook and checks
        if re.match(r"\*\*(Interview hook|Check before reuse)", item.strip()):
            break
        bullets.append(item)
    from_page = [] if w.get("steps") or w.get("points") else [point_why(b) for b in bullets]
    narrow = not (shots or formulas or len(top) > 1)               # a work Run's words-only frame, as before
    steps = step_rows(w.get("steps") or from_page, pts, "🪜",       # the face's, else the page's
                      per_row=6 if not work else 3 if stairs else (2 if narrow else 3))   # a video: 6 to a row
    read_rows, read_labels = ([], []) if work else reading_rows(run, assets, passages)
    width = (NARROW if narrow else W) if work else VIDEO_W        # stairs sizes the room to its boxes
    f = d.frame(name, width, TALLEST)
    if hasattr(d, "room"):                                         # boxes joined by arrows, room between (⑧):
        d.room(f)                                                  # ⑥ measures its words over its boxes
    who = " · ".join(x for x in (run["creator"].split(" · ")[0], run["length"]) if x)
    checked = video_checked(run["state"])
    sub = f"🎬 {run['title'] or run['short']} · {who}{' · ★ interview' if run['star'] else ''} · " + \
        ("✅ checked against the video" if checked else "🔶 from the transcript, not yet checked")
    if work:
        sub = f"🧪 {run['rid']} · {jr.mark(run['state'])} {run['state']}"
    y = heading(d, name, sub, str(w.get("says") or run["summary"] or f"❓ no summary for {run['rid']}"), width)
    checks = [f"❓ {c}" for c in w.get("check") or []] or \
        [f"❓ {c.strip().strip('- ').rstrip('.')}" for c in re.split(r";\s+(?![^()]*\))|\s+-\s+(?=[A-Z])", run["check"])
         if c.strip().strip('- ')]                                     # the page's "- " list: one check per line
    terms = terms_items(w.get("terms"))
    middle = ([("📖 Words to know first", terms, INK, 1)] if terms else []) + \
        ([("🧮 The formula, explained", formulas, INK, 1.25)] if formulas else [])
    steps = steps or [[("🪜 What the Run did, step by step" if work else "🪜 What the video says, step by step",
                        ["❓ no steps written yet"], INK)]]
    rows = top + ([[("📸 What the screen shows", [shots_item(shots, 760, per_row=4 if work else 6)], INK)]] if shots else []) + \
        ([middle] if middle else []) + steps + read_rows + \
        [[("🎤 What it means" if work else "🎤 Say it in an interview",
           [str(w.get("hook") or run["hook"] or "❓ no reading written")], INK, 1),
          ("❓ Still to check" if work else "❓ Check against the video", checks or ["❓ nothing listed"], RED, 1.1),
          ("🧾 The Run", run_lines(run), INK, 1.5)]]                # its long paths need the room
    pages = [] if work or read_rows else pdf_pages(run, assets)     # a read transcript shows its passages instead
    if pages:                                                        # the whole video, read as an article
        rows.append([("📄 The whole video, as an article (its transcript, arranged; not checked line by line)",
                      [shots_item(pages, 2200, per_row=4)], INK)])
    labels = (["measured"] if top and len(top[0]) > 1 else []) + (["the curve"] if len(top) > 1 else []) + \
        (["the words"] if top and middle else []) + \
        (["the words first"] if shots and middle else []) + \
        (["the math"] if terms and formulas else []) + (["step by step"] if middle or shots or top else []) + \
        [""] * (sum(map(len, steps)) - 1) + read_labels + ["so it means" if work else "say it as", "check first",
                                                            "from the Run"] + (["read it all"] if pages else [])
    bottom = rows_of(d, y, rows, labels, width, stairs=stairs)       # fit() trims a stairs frame to its boxes
    if run["url"]:
        bottom = jr.para(d, 40, bottom + 24, "🔗 " + run["url"], width - 80, T_BODY)
    return fit(d, f, bottom, detail=any(w.get(k) for k in ("shots", "terms", "formula", "steps", "show", "config")))


def draw_task(folder: Path, out: Path, cfg: dict | None = None, source: str = "") -> tuple[Path, list[dict]]:
    """Draw one Task into `out` (canvas.write keeps a person's marks); returns the drawing and its sources in order."""
    cfg = cfg or {}
    task = parse(task_page(folder))
    runs = reading_order(task, cfg.get("order"))
    words = {str(k): v or {} for k, v in {**(cfg.get("videos") or {}), **(cfg.get("runs") or {})}.items()}
    for r in runs:                                     # the face's state wins: a crash its receipt calls completed
        if (words.get(r["rid"]) or {}).get("state"):
            r["state"] = str(words[r["rid"]]["state"])
    noun = "Runs" if task.get("work") or any(r.get("work") for r in runs) else "Videos"
    d = Drawing()
    d.plain = str(cfg.get("layout") or "") == "plain"              # boxes with room, no arrows (asked 261012)
    assets = out.parent / "assets"
    idea = idea_frame(d, task, folder, runs, cfg, assets)
    stairs = str(cfg.get("layout") or "") != "rows"                # stairs by default (⑧); a face may keep rows
    groups = []                                                    # per source: its transcript, read, then its frame
    for r in runs:
        ww = words.get(r["rid"]) or {}
        t = None if r.get("work") else transcript_frame(d, r, ww, assets)
        groups.append(([t["id"]] if t else []) + [source_frame(d, r, ww, assets, stairs, passages=t is None)["id"]])
    acts = [{"name": "Act 1 · The idea", "frames": [idea["id"]]}]
    if noun == "Runs":                                             # three Runs to a row
        frames = [g[0] for g in groups]
        for k in range(0, len(frames), 3):
            last = min(k + 3, len(frames))
            acts.append({"name": f"Act {len(acts) + 1} · " + (f"Run {last} · {runs[k]['rid']}" if last == k + 1 else
                                                             f"Runs {k + 1} to {last}"), "frames": frames[k:k + 3]})
    else:                                                          # a video is its own row (JL 261012): its
        for k, g in enumerate(groups):                             # transcript on the left, then what it says
            acts.append({"name": f"Act {len(acts) + 1} · Video {k + 1} · {runs[k]['rid']}", "frames": g,
                         "arrow": "read, then explained"})
    frames = [a["frames"][0] for a in acts[1:]]
    between = [(idea["id"], frames[0], f"one frame per {noun[:-1].lower()}, in order")] if frames else []
    per_act = 3 if noun == "Runs" else 1
    def into(rid):                                                  # what the next video does, on the arrow into it
        said = (words.get(rid) or {}).get("role")
        return f"then {rid}: {said}" if said else role(task, rid)
    between += [(acts[i]["frames"][0], acts[i + 1]["frames"][0],
                 into(runs[i]["rid"]) if per_act == 1 else f"next {noun.lower()}") for i in range(1, len(acts) - 1)]
    if d.plain:                                                    # acts named, no arrow between frames
        between = []
    d.acts(acts, between=between, gap=GAP)
    at = {e["id"]: e for e in d.els if e["type"] == "frame"}
    d.fid = None
    for a in acts[1:] if noun == "Runs" and not d.plain else []:                # into each Run's frame: what that Run does
        for fa, fb in zip(a["frames"], a["frames"][1:]):
            A, B = at[fa], at[fb]
            rid = B["name"].split(" · ")[0]
            said = (words.get(rid) or {}).get("role")
            label = f"then {rid}: {said}" if said else role(task, rid)
            ay = A["y"] + min(A["height"], B["height"]) / 2
            lines = jr.wrap(label, GAP - 90, 40)
            jr.para(d, A["x"] + A["width"] + 45, ay - 24 - len(lines) * 50, label, GAP - 90, 40)
    d.write(out, source or f"excalidraw-task scripts/task_drawing.py {folder.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out, runs


# ── the topic ────────────────────────────────────────────────────────────────────────────────────────────────
def task_page(folder: Path) -> Path:
    return folder / f"{folder.name}.md"


def face_cfg(face: Path) -> dict:
    """The face's `task:` yaml (name, order, reading, idea, videos, open)."""
    m = re.search(r"```yaml\s*\n(task:.*?)```", jr.read(face), re.S)
    if not (m and yaml):
        return {}
    try:
        return (yaml.safe_load(m.group(1)) or {}).get("task") or {}
    except Exception as err:                                   # a typo in the face is said, not hidden
        print(f"{face.name}: its task: yaml does not read ({err}); drawing from the page only", file=sys.stderr)
        return {}


def ledger(topic: Path, folder: Path, runs: list) -> str:
    """The face's generated part: each source with its length, state and links."""
    rel = lambda p: Path(os.path.relpath(p, topic)).as_posix()    # noqa: E731
    out = [BEGIN, "", "The videos on disk", "------------------", "",
           "Read from the Task page on every build; edit the `task:` yaml above or the Task page, never this list.", ""]
    for r in runs:
        out.append(f"- {'★ ' if r['star'] else ''}**{r['rid']}** · {r['short']} · {r['length'] or '?'} · "
                   f"{r['state'] or 'no state'}" + (f" · [video]({r['url']})" if r["url"] else "") +
                   (f" · [Result Card]({rel(folder / r['card'])})" if r["card"] else ""))
    return "\n".join(out + ["", END])


def draw(topic: Path) -> Path:
    """Redraw one Task topic from its face and its Task page; refresh the face's list of videos and the preview."""
    topic = topic.resolve()
    face = topic / f"{topic.name}.md"
    cfg = face_cfg(face)
    folder = topic.parents[1] / str(cfg.get("name", ""))
    if not task_page(folder).is_file():
        raise SystemExit(f"{face}: task.name names no Task page under {topic.parents[1].name}")
    out, runs = draw_task(folder, topic / f"{topic.name}.excalidraw", cfg,
                          f"excalidraw-task scripts/task_drawing.py {topic.name}")
    text = jr.read(face)
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        face.write_text(head + ledger(topic, folder, runs) + rest.split(END, 1)[1], encoding="utf-8")
    return out


def drawn_tasks(block: Path) -> dict[str, Path]:
    """{`jNN_job/tNN_task`: topic} for the Block's topics whose face names a Task."""
    out = {}
    for face in (block / "studio").glob("s*/s*.md"):
        name = face_cfg(face).get("name")
        if name:
            out[str(name)] = face.parent
    return out


def free_numbers(block: Path, n: int, start: int | None) -> list[int]:
    """`n` free topic numbers: from `start` if given, else the runs band (s21-s29), then the concepts (s01-s09)."""
    used = {int(m.group(1)) for p in (block / "studio").iterdir() if p.is_dir()
            for m in [re.match(r"^s(\d+)[-_]", p.name)] if m} if (block / "studio").is_dir() else set()
    pool = range(start, start + 100) if start else [*BAND_RUN, *BAND_CONCEPT]
    out = [nn for nn in pool if nn not in used][:n]
    if len(out) < n:
        raise SystemExit(f"{block.name}: only {len(out)} free numbers in s21-s29 and s01-s09 for {n} Tasks; pass --nn")
    if start and out != list(range(start, start + n)):
        raise SystemExit(f"{block.name}: s{start:02d} to s{start + n - 1:02d} are not all free; pick another --nn")
    return out


def scripts_from(topic: Path) -> str:
    """This skill's scripts as the topic reaches them: through its SPACE's Tools link when it has one."""
    space = next((p for p in (topic, *topic.parents) if (p / "Tools").exists()), None)
    to = space / "Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-task/scripts" if space else HERE
    return Path(os.path.relpath(to, topic)).as_posix()


def builder_text(topic: Path, title: str, script: str) -> str:
    return (f'"""{title}: drawn by excalidraw-task\'s task_drawing.py from the Task page and this face\'s task: yaml; '
            f"a person's marks on the drawing are kept.\n\n    python {script}\n\"\"\"\n"
            "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
            f'sys.path.insert(0, str((HERE / "{scripts_from(topic)}").resolve()))\n'
            "import task_drawing  # noqa: E402\n\nif __name__ == \"__main__\":\n    task_drawing.draw(HERE)\n")


WORDS = ("The short words the drawing shows, so each frame reads at a glance (excalidraw-studio ⑦: at most 200 words "
         "a frame, none under 28 px). Anything left out is read from the Task page, which keeps the full text.")


def new_face(nn: int, topic: Path, folder: Path, task: dict, tag: str) -> str:
    title = re.sub(r"^t\d+\s*·\s*", "", task["title"])          # a page titled "t01 · …" would say t01 twice
    if task.get("work"):                                        # a work Task: its Job names the model, no videos
        name = f"s{nn:02d} · {jr.title_of(folder.parent)} · {title}"
        topic_line = (f"**Topic:** What the {len(task['runs'])} Runs under `{folder.name}` measured. The first frame "
                      "is the Task's idea; then one frame per Run: what it ran, what it measured, and what is open.")
    else:
        name = f"s{nn:02d} · {folder.name[:3]} · {title}: what each video told"
        topic_line = (f"**Topic:** What the {len(task['runs'])} videos filed under `{folder.name}` say. The first "
                      "frame is the Task's idea: what it is, how it works, why it matters, and the videos in reading "
                      "order. Then one frame per video: what it says, its points in order, how to say it in an "
                      "interview, and what to check against the video before reuse.")
    rel = Path(os.path.relpath(task_page(folder), topic)).as_posix()
    return "\n".join([
        name, "=" * len(name), "",
        f"**Label:** {name}", "",                                 # the Studio card's title; else the folder name
        f"**Tags:** `{tag}`", "",
        "**Stage:** explore", "",
        topic_line, "",
        "**Feeds:** none yet.", "",
        f"**Task:** [{folder.name}]({rel})", "", "",
        "Task", "----", "",
        WORDS, "",
        "1. **name** and **order**: the Task (`jNN_job/tNN_task`, from the Block) and its Runs in drawing order "
        "(empty: the order How the videos fit names them).",
        "2. **reading**: the idea frame's key point (empty: `idea.question`, else the page's Opening).",
        "3. **idea**: `question` (14 words or fewer), `what` and `why` (one sentence each, 20 words or fewer), `how` "
        "(3 to 5 steps, 8 words or fewer each), `questions` (3 to 5 interview questions, short).",
        "4. **videos**, per Run: `name` (the frame's title, 6 words or fewer), `says` (the key point, 20 words or "
        "fewer), `points` (3 to 5, in the video's order, 10 words or fewer each), `hook` (16 words or fewer), "
        "`check` (1 to 3, 8 words or fewer each), `role` (the arrow into its frame, 5 words or fewer).",
        "5. **open**: open points, drawn red under the idea.", "",
        "```yaml", "task:", f"  name: {folder.relative_to(topic.parents[1]).as_posix()}", "  order: []",
        "  reading: ''", "  idea: {}", "  videos: {}", "  open: []", "```", "",
        BEGIN, END, "", "",
        "Files", "-----", "",
        "```text", f"{topic.name}/", f"├── {topic.name}.md           this face",
        f"├── {topic.name}.excalidraw   the idea, then one frame per video; a person's marks are kept",
        f"├── {topic.name}.png          its preview",
        f"└── build_s{nn:02d}_{folder.name}.py   calls excalidraw-task's task_drawing.py", "```", "", "",
        "Decided", "-------", "",
        f"s{nn:02d}-D01 · One topic per Task: the idea first, then one frame per video saying what it told, in few "
        "words and large type (JL 261012)", "", "",
        "Open", "----", "",
        "1. Every video's points are drafted from an automatic transcript; each waits for a person to check it "
        "against the video before reuse.", "",
        "(write here, or mark the drawing in red)", ""])


def tasks_of(target: Path) -> list[Path]:
    """A Task folder (tNN_…), or every Task of a Job folder (jNN_…) in order; a Job's own face is not a Task."""
    if re.match(r"^t\d+_", target.name) and task_page(target).is_file():
        return [target]
    if re.match(r"^j\d+_", target.name):
        return sorted(t for t in target.glob("t[0-9]*_*") if task_page(t).is_file())
    return []


def job_tag(block: Path, job: Path) -> str:
    """A new Task topic's group: the tag its Job's other topics carry most (a person's regrouping holds), else the
    Job's own words for its first topic. Tagging every topic by its Job made b03's 30 Jobs 30 groups (JL 261012:
    "the groups here are too many … the group tags here are fixed, do you get the reason why?")."""
    from collections import Counter
    seen = Counter()
    for name, topic in drawn_tasks(block).items():
        if name.split("/")[0] == job.name:
            line = re.search(r"(?m)^\*\*Tags:\*\*\s*(.+)$", jr.read(topic / f"{topic.name}.md"))
            seen.update(re.findall(r"`([^`]+)`", line.group(1)) if line else [])
    seen.pop("Results", None)                                   # a results topic's shared group is not the Job's
    return seen.most_common(1)[0][0] if seen else f"{job.name[:3]} {jr.title_of(job)}"


def make(target: Path, nn: int | None = None, dry: bool = False) -> list[Path]:
    """One topic per Task (a Job folder: each of its Tasks), in the Block's studio; refuses a Task already drawn."""
    target = target.resolve()
    tasks = tasks_of(target)
    if not tasks:
        raise SystemExit(f"{target}: no Task page here (a Task folder holds <name>/<name>.md)")
    block = tasks[0].parents[1]
    drawn = drawn_tasks(block)
    for t in tasks:
        name = t.relative_to(block).as_posix()
        if name in drawn:
            raise SystemExit(f"{name} is drawn already: {drawn[name].relative_to(block)}; redraw it with draw")
    out = []
    for t, k in zip(tasks, free_numbers(block, len(tasks), nn)):
        task = parse(task_page(t))
        topic = block / "studio" / f"s{k:02d}-{t.name.replace('_', '-')}"
        if dry:
            print(f"would make {topic.relative_to(block)}  ← {t.relative_to(block)}")
            out.append(topic)
            continue
        tag = job_tag(block, t.parent)
        topic.mkdir(parents=True)
        (topic / f"{topic.name}.md").write_text(new_face(k, topic, t, task, tag), encoding="utf-8")
        builder = topic / f"build_s{k:02d}_{t.name}.py"
        builder.write_text(builder_text(topic, f"s{k:02d} · {t.name[:3]} · {task['title']}", builder.name),
                           encoding="utf-8")
        groups = block / "studio" / "_groups.txt"
        lines = jr.read(groups).splitlines() if groups.is_file() else [
            "# Studio groups of this Block, in button order. The workbench writes this file when a group is",
            "# made, moved or deleted; a group's topics are the ones whose **Tags:** line names it."]
        if tag not in lines:
            groups.write_text("\n".join(lines + [tag]) + "\n", encoding="utf-8")
        out.append(draw(topic))
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make")
    m.add_argument("target", type=Path)
    m.add_argument("--nn", type=int)
    m.add_argument("--dry-run", action="store_true")
    sub.add_parser("draw").add_argument("topic", type=Path)
    pv = sub.add_parser("preview")
    pv.add_argument("task", type=Path)
    pv.add_argument("out", type=Path)
    pv.add_argument("--words", type=Path, help="a yaml with idea: and videos: or runs:, drawn as a face would")
    a = p.parse_args(argv)
    if a.cmd == "make":
        for out in make(a.target, a.nn, a.dry_run):
            print(out)
    elif a.cmd == "draw":
        print(draw(a.topic))
    else:
        cfg = yaml.safe_load(a.words.read_text()) if a.words and yaml else None
        a.out.parent.mkdir(parents=True, exist_ok=True)
        print(draw_task(a.task.resolve(), a.out.resolve(), cfg)[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
