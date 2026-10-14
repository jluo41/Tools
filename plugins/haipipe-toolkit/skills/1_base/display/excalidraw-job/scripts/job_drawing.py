"""A Job as one drawing: why it exists, what goes in and comes out, what it concluded, and its tables and pictures.
Asked 261012, on b01_ml_foundations' s21 to s23, which showed only their Runs' states: "我想在这个桌上把这个 job 的所有
内容都展示出来" (1. 输入什么、输出是什么？ 2. 得到什么结论？ 3. 相关的图表有哪些？).

    python job_drawing.py make <job folder> [--nn NN] [--dry-run]   the Block's topic sNN-<jNN>-<job>, drawn
    python job_drawing.py draw <topic folder>                       redraw one (what its builder calls)
    python job_drawing.py adopt <topic folder>                      a one-Job results topic (job_results.py) redrawn here
    python job_drawing.py preview <job folder> <out.excalidraw>     draw a Job anywhere; its Block is not touched

Four frames in two acts, by excalidraw-studio's principles:

    Act 1 · what the Job is for   ① 🎯 why: a mind map  ─planned as─▶  ② 🔁 in → Tasks → out: a workflow map
                                    │ found
    Act 2 · what it found         ③ 💡 what it concluded ─shown in─▶  ④ 📊 its tables, formulas and pictures

Every word is read from disk on every build: the Job face (goal, close, answers, ## Topic), the Block's board, each
Task's page (## Opening, its labelled paragraphs, the questions it answers, ## Aims, its tables, its formulas), each
Run's receipt (state, subject) and the pictures in the Job's folders. The topic face's `job:` yaml holds only what no
file says: the aim in one sentence, the reading (③'s key point), lines that replace a Task's conclusions, open points.
The writer is haipipe-studio's canvas.write, so a person's marks survive a rebuild.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[2]                                      # skills/1_base
sys.path.insert(0, str(SKILLS / "project/haipipe-studio/scripts"))
sys.path.insert(0, str(SKILLS / "display/excalidraw-studio/scripts"))
sys.path.insert(1, str(SKILLS / "display/excalidraw-task/scripts"))   # ③ uses excalidraw-task's boxes
import canvas  # noqa: E402
import job_results as jr  # noqa: E402
from draw import GREY, INK, MAP_WORDS, RED, T_ACT, W, Drawing  # noqa: E402

MAP_BUDGET = MAP_WORDS - 8                # ② stays under ⑦ with room for the badge's change of words

try:
    import yaml
except ImportError:                                           # the drawing still reads from disk; the face's yaml needs it
    yaml = None

GAP = 130
MOST_RUNS, MOST_TASKS, MOST_PICTURES, MOST_ROWS = 8, 14, 4, 14
PICTURES = (".png", ".jpg", ".jpeg")
FOUND = re.compile(r"(?i)^(answers?|conclusions?|findings?|results?|takeaways?|key points?)$")
BEGIN, END = jr.BEGIN, jr.END


# ── reading a page ───────────────────────────────────────────────────────────────────────────────────────────
def section(text: str, name: str) -> str:
    """The body of `## <name>`, up to the next `## ` heading."""
    m = re.search(rf"(?ms)^##\s+{re.escape(name)}\s*$\n(.*?)(?=^##\s|\Z)", text)
    return m.group(1).strip() if m else ""


def plain(s: str) -> str:
    return " ".join(re.sub(r"\*\*|`", "", str(s)).split())


def sentences(s: str, n: int) -> str:
    parts = re.split(r"(?<=[.!?。！？])\s+", plain(s))
    return " ".join(parts[:n])


def first_para(s: str) -> str:
    for block in re.split(r"\n\s*\n", s.strip()):
        b = plain(" ".join(ln for ln in block.splitlines() if not ln.strip().startswith(("```", "|", "<"))))
        if b and not b.lower().startswith("open:"):
            return b
    return ""


def labelled(text: str) -> dict:
    """The page's labelled paragraphs in order, `**What it is**: …`: its words (they may run past the label's own
    line) and the list under it (it may start after a blank line, and an item may wrap). Found by the Proj10
    session (261012): `**How it works**:`, a blank line, then its steps, read as no steps at all."""
    out, lines, i = {}, text.splitlines(), 0
    starts = ("- ", "* ", "**", "#", "|", "```", "<")
    while i < len(lines):
        m = re.match(r"^\*\*([^*]{2,40})\*\*\s*:?\s*(.*)$", lines[i].strip())
        if not m:
            i += 1
            continue
        body, j = [m.group(2).strip()], i + 1
        while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith(starts):
            body.append(lines[j].strip())                      # the paragraph runs on
            j += 1
        k = j
        while k < len(lines) and not lines[k].strip() and not body[0]:
            k += 1                                             # a label with no words of its own: its list may follow a blank
        items = []
        if k < len(lines) and lines[k].strip().startswith(("- ", "* ")):
            j = k
            while j < len(lines) and lines[j].strip() and \
                    (lines[j].strip().startswith(("- ", "* ")) or (items and lines[j].startswith((" ", "\t")))):
                if lines[j].strip().startswith(("- ", "* ")):
                    items.append(lines[j].strip()[2:])
                else:
                    items[-1] += " " + lines[j].strip()        # a wrapped item
                j += 1
        out.setdefault(m.group(1).strip().rstrip(":"), {"body": " ".join(x for x in body if x), "items": items})
        i = max(j, i + 1)
    return out


def concept(page: str) -> str:
    """Where a page states what it found: its first numbered division (`### 1 · …`) when it is cut into divisions
    (a discovery page's later divisions are one Run each), else its ## Content, else the whole page."""
    content = section(page, "Content") or page
    m = re.search(r"(?ms)^###\s+1\s*·.*?(?=^###\s+\d+\s*·|\Z)", content)
    return m.group(0) if m else content


def tables(text: str) -> list[dict]:
    """Every markdown table: its caption (the bold label or heading just above it), its head and its rows."""
    out, lines, i = [], text.splitlines(), 0
    cells = lambda ln: [plain(c) for c in ln.strip().strip("|").split("|")]          # noqa: E731
    while i < len(lines) - 1:
        if lines[i].strip().startswith("|") and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            cap = ""
            for k in range(i - 1, max(i - 6, -1), -1):
                m = re.match(r"^\*\*([^*]+)\*\*|^#+\s+(.+)", lines[k].strip())
                if m:
                    cap = (m.group(1) or m.group(2)).strip().rstrip(":")
                    break
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(cells(lines[j]))
                j += 1
            k = j
            while k < len(lines) and not lines[k].strip():
                k += 1
            m = re.match(r"^\*\*([^*]+)\*\*\s*:?\s*(.+)$", lines[k].strip()) if k < len(lines) else None
            out.append({"caption": cap, "head": cells(lines[i]), "rows": rows,
                        "note": (m.group(1).strip().rstrip(":"), sentences(m.group(2), 3)) if m else None})
            i = j
            continue
        i += 1
    return out


def aims(text: str) -> dict:
    """`## Aims`: each aim (its mark, id, words), its Done when lines and its Now lines."""
    body = section(text, "Aims")
    return {"items": re.findall(r"(?m)^\s*-\s*(\S+)\s+(A\d+(?:\.\d+)?)\s*·\s*(.+)$", body),
            "done_when": list(dict.fromkeys(plain(x) for x in re.findall(r"\*\*Done when:\*\*\s*(.+)", body))),
            "now": [plain(x) for x in re.findall(r"\*\*Now:\*\*\s*(.+)", body)]}


def source_of(run: dict) -> dict:
    """What a Run read: its subject's title, creator and platform, and the word for it (video, paper, source)."""
    data = jr.load(run["result"] / "runtime.yaml") or jr.load(run["dir"] / "run.yaml") or {}
    s = data.get("subject") if isinstance(data, dict) else None
    t = data.get("trigger") if isinstance(data, dict) else None
    s, t = (s if isinstance(s, dict) else {}), (t if isinstance(t, dict) else {})
    kind = f"{t.get('kind', '')} {s.get('kind', '')}".lower()
    word = "video" if "video" in kind or s.get("platform") in ("Bilibili", "YouTube") else \
        "paper" if "paper" in kind else "source" if s else "Run"
    return {"creator": str(s.get("creator", "")).strip(), "platform": str(s.get("platform", "")).strip(), "word": word}


# ── reading the Job ──────────────────────────────────────────────────────────────────────────────────────────
def job_info(job: Path) -> dict:
    block = job.parent
    face = jr.read(jr.face_of(job)) if jr.face_of(job) else ""
    return {"id": job.name[:3], "title": jr.title_of(job), "goal": jr.field(job, "goal"),
            "close": jr.field(job, "close"), "answers": jr.field(job, "answers"),
            "topic": first_para(section(face, "Topic")), "block": jr.title_of(block),
            "spine": jr.field(block, "spine") or sentences(first_para(section(jr.read(block / "board.md"), "Opening")), 1)
            or sentences(first_para(section(jr.read(block / "board.md"), "Topic")), 1),
            "block_close": jr.field(block, "close")}


def picked_values(row: dict, cfg: dict | None) -> list[str]:
    """The face's show: picks for two or more Runs of this Task: each picked Run's own values, named by its Run."""
    picked = [r for r in row["runs"] if r["values"] and cfg and jr.picks_for(cfg, row["task"], r)]
    if len(picked) < 2:
        return []
    picked.sort(key=lambda r: r["mark"] != "✅")              # finished Runs first
    clash = len({r["name"][:3] for r in picked}) < len(picked)  # five r01_* Runs: name each by the rest of its name
    tag = (lambda r: re.sub(r"^r\d+[a-z]?_", "", r["name"]).replace("_", " ")) if clash else (lambda r: r["name"][:3])
    out = []
    for r in picked:                                         # labels that name their Run stay; else one item per Run
        if not clash and re.match(r"^r\d", r["values"][0]):    # its first label names the Run already
            out += r["values"]
        else:
            out.append(f"{tag(r)}: {', '.join(r['values'])}")
    return out


def task_info(row: dict, cfg: dict | None = None) -> dict:
    task = row["task"]
    page_path = jr.face_of(task)
    page = jr.read(page_path) if page_path else ""
    found = concept(page)
    lab = labelled(found)
    question = sentences(first_para(section(page, "Opening")), 1) or jr.field(task, "goal") or \
        (f"develops: {jr.field(task, 'develops')}" if jr.field(task, "develops") else "")   # a work Task's purpose
    sources = [source_of(r) for r in row["runs"]]
    m = re.search(r"(?m)^Sources\s*→\s*(.+)$", page)
    qs = next((v for k, v in lab.items() if "question" in k.lower()), {"items": []})
    qa = []
    for it in qs["items"]:
        m2 = re.match(r"\*\*(.+?)\*\*\s*(.*)", it)
        if m2:
            a = sentences(m2.group(2), 1)
            qa.append((plain(m2.group(1)), a if len(a) >= 40 else sentences(m2.group(2), 2)))
    kinds = Counter(p.suffix.lower() or p.name for r in row["runs"] if r["result"].is_dir()
                    for p in r["result"].iterdir() if p.is_file())
    cards = sum((r["result"] / f"{r['name']}.md").is_file() for r in row["runs"])
    return {"id": task.name[:3], "name": task.name, "title": str(row["title"]).rstrip(". "), "runs": row["runs"], "row": row,
            "input": jr.field(task, "input"), "output": jr.field(task, "output"),
            "values": picked_values(row, cfg) or next((r["values"] for r in row["runs"] if r["values"] and r["mark"] == "✅"),
                                                      next((r["values"] for r in row["runs"] if r["values"]), [])),
            "page": page_path.name if page_path else "", "question": question, "lab": lab, "qa": qa,
            "aims": aims(page), "tables": tables(found),
            "formulas": formulas(lab), "sources_line": plain(m.group(1)) if m else "", "sources": sources,
            "divisions": len(re.findall(r"(?m)^###\s+\d+\s*·", page)), "cards": cards, "kinds": kinds}


def formulas(lab: dict) -> list[str]:
    """The formulas a page writes in code (`H(P, Q) = …`), from its labelled paragraphs, once each."""
    out = []
    for v in lab.values():
        for s in [v["body"], *v["items"]]:
            out += [f.strip() for f in re.findall(r"`([^`]{3,120})`", s) if re.search(r"[=∇Σ∫≈]", f)]
    return list(dict.fromkeys(out))[:8]


def pictures(job: Path) -> list[Path]:
    """The pictures in the Job's own folders and Results (not a studio/ or a hidden or _ folder)."""
    out = []
    for p in sorted(job.rglob("*")):
        parts = p.relative_to(job).parts[:-1]
        if p.suffix.lower() in PICTURES and p.is_file() and \
                not any(q.startswith((".", "_")) or q in ("studio", "history") for q in parts):
            out.append(p)
    return out


def conclusions(t: dict, override: list | None) -> list[tuple[str, list[str]]]:
    """What a Task's page concluded: its labelled paragraphs, a list's items each its first sentence."""
    if override:
        return [("", [str(x) for x in override])]
    out = []
    for name, v in t["lab"].items():
        if name in ("What it is", "How it works", "Why it matters") or (FOUND.match(name) and len(out) < 4):
            lines = [sentences(v["body"], 2)] if v["body"] else [sentences(x, 1) for x in v["items"][:4]]
            out.append((name, [x for x in lines if x]))
    return out


# ── drawing helpers that measure Chinese as full width (job_results.wrap) ───────────────────────────────────
def para(d, x, y, s, width, size, color=None):
    return jr.para(d, x, y, s, width, size, color)


def flow(d: Drawing, steps: list[dict], x: float, y: float, w: float, labels: list[str], title=34, leaf=28):
    """A workflow in one row: a box per step, the key step in the key colour, a named arrow between each."""
    unit = (w - GAP * (len(steps) - 1)) / sum(s.get("weight", 1) for s in steps)
    ws = [unit * s.get("weight", 1) for s in steps]
    hh = max(18 + jr.tall(s["title"], bw - 40, title) + 12 +
             sum(jr.tall(ln, bw - 40, leaf) + 6 for ln in s["lines"]) + 16 for s, bw in zip(steps, ws))
    bx = x - GAP
    for i, (s, bw) in enumerate(zip(steps, ws)):
        bx += (ws[i - 1] if i else 0) + GAP
        if s.get("key"):
            d.key(bx, y, bw, hh)
        else:
            d.box(bx, y, bw, hh, INK, 2.5)
        yy = para(d, bx + 20, y + 18, s["title"], bw - 40, title) + 12
        for ln in s["lines"]:
            yy = para(d, bx + 20, yy, ln, bw - 40, leaf) + 6
        if i:
            d.line([(bx - GAP + 6, y + 56), (bx - 6, y + 56)], sw=3)
            d.text(bx - GAP + 8, y + 10, labels[i - 1], 28)
    return y + hh


def table(d: Drawing, x: float, y: float, w: float, t: dict, size=20) -> float:
    """A page's table as a grid: columns as wide as their words, the widest ones wrapped to fit `w`."""
    head, rows = t["head"], t["rows"][:MOST_ROWS]
    n = len(head)
    cell = lambda r, i: r[i] if i < len(r) else ""                                    # noqa: E731
    wide = [max(sum(jr.char_w(c, size) for c in cell(r, i)) for r in [head] + rows) + 28 for i in range(n)]
    if sum(wide) > w:
        fair = w / n
        big = [i for i in range(n) if wide[i] > fair]
        room = w - sum(wide[i] for i in range(n) if i not in big)
        total = sum(wide[i] for i in big)
        for i in big:
            wide[i] = max(70, wide[i] * room / total)
    tw, yy = sum(wide), y
    for k, r in enumerate([head] + rows):
        hh = max(jr.tall(cell(r, i) or " ", wide[i] - 24, size) for i in range(n)) + 16
        cx = x
        for i in range(n):
            para(d, cx + 12, yy + 8, cell(r, i), wide[i] - 24, size)
            cx += wide[i]
        yy += hh
        d.line([(x, yy), (x + tw, yy)], arrow=False, sw=2.5 if k == 0 else 1)
    d.box(x, y, tw, yy - y, INK, 1.5)
    if len(t["rows"]) > MOST_ROWS:
        yy = para(d, x, yy + 8, f"… {len(t['rows']) - MOST_ROWS} more rows on the page", w, 20)
    return yy


def finish(d: Drawing, f: dict, bottom: float) -> dict:
    """As tall as its content (a thin frame is not padded); read down past the screen's height; its badge."""
    f["height"] = max(bottom + 40, 600)
    if f["height"] > canvas.FRAME_MAX[1]:
        canvas.reads_down(f)
    d.fid = f["id"]
    d.badge(f)
    return f


def tally_of(runs: list[dict]) -> str:
    return jr.tally([{"runs": runs}])


def n_of(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def states(runs: list[dict]) -> str:
    c = Counter(r["state"] for r in runs)
    return ", ".join(f"{n} {s}" for s, n in c.most_common()) if c else "no Run yet"


# ── the frames: few words in a map (excalidraw-studio ⑦); a Task's detail is its own topic (excalidraw-task) ───
def task_topics(block: Path) -> dict:
    """Which topic draws each Task: a face's `task:` yaml names it, `<jNN_job>/<tNN_task>` (excalidraw-task's)."""
    out = {}
    for face in sorted((block / "studio").glob("s*/*.md")):
        m = re.search(r"```yaml\s*\n(task:.*?)```", jr.read(face), re.S)
        if m and yaml:
            try:
                name = ((yaml.safe_load(m.group(1)) or {}).get("task") or {}).get("name")
            except Exception:
                name = None
            if name:
                out[str(name)] = face.parent.name
    return out


def open_line(o, closer: bool = True) -> str:
    """One open item: the face's {item, closer} as "item → close by: closer" (a map: the item alone), or its words."""
    if isinstance(o, dict):
        return f"❓ {o.get('item', '')}" + (f" → close by: {o['closer']}" if closer and o.get("closer") else "")
    return "❓ " + str(o).lstrip("❓ ")


def why_frame(d: Drawing, info: dict, tasks: list[dict], cfg: dict) -> dict:
    """① its aim in the centre, each Task's question around it; the questions shorten until ⑦'s words fit."""
    f = d.frame(f"① 🎯 Why {info['id']}: {info['title']}")
    start = len(d.els)
    aim = str(cfg.get("aim") or "").strip() or info["goal"] or "❓ No aim yet: the Job face's goal: is open"
    for most in (400, 110, 70, 45):
        del d.els[start:]
        bottom = why_once(d, f, info, tasks, aim, most, cfg.get("tasks") or {})
        if Drawing.words_small(d.els, f["id"])[0] <= MAP_BUDGET:
            break
    return finish(d, f, bottom)


def why_once(d: Drawing, f: dict, info: dict, tasks: list[dict], aim: str, most: int, words: dict) -> float:
    d.fid = f["id"]
    asked = {t["name"]: str((words.get(t["name"]) or words.get(t["id"]) or {}).get("asked") or t["question"])
             for t in tasks}
    top = jr.heading(d, f"🎯 Why {info['id']} · {info['title']}", "its aim, each Task's question, when it is done")
    branches = [{"title": f"🧩 {t['id']} · {t['title']}", "by": "standing",
                 "summary": short(asked[t["name"]], most) if asked[t["name"]] else "❓ no question on its page"}
                for t in tasks[:5]] or [{"title": "⬜ No Task yet", "by": "standing",
                                         "summary": "the Job face lists none; its workflow is drawn once it has one"}]
    if len(tasks) > 5:
        branches.append({"title": f"🧩 {len(tasks) - 5} more Tasks", "by": "standing",
                         "summary": ", ".join(t["id"] for t in tasks[5:12])})
    branches.insert(min(3, len(branches)), {
        "title": "🏁 Done when", "by": "standing", "summary": info["close"] or "❓ close: not written on the Job face",
        "leaves": [] if info["answers"] else ["❓ answers: no Question named"]})
    branches.insert(min(4, len(branches)), {"title": f"🧱 Its Block · {info['block']}", "by": "standing",
                                            "summary": short(info["spine"].replace(" — ", ": "), most) if info["spine"] else "❓ no spine on the board"})
    return d.mind_map(aim, branches[:8], top=top)


def finding(t: dict, cfg: dict) -> str:
    """A Task's finding in one sentence: the face's own line, else its page's Why it matters, Answer or What it is."""
    over = (cfg.get("conclusions") or {})
    own = over.get(t["name"]) or over.get(t["id"]) or ((cfg.get("tasks") or {}).get(t["name"]) or {}).get("found")
    if own:
        return str(own[0] if isinstance(own, list) else own)
    for name in ("Why it matters", "Answer", "Answers", "Findings", "Conclusion", "What it is"):
        v = t["lab"].get(name)
        if v and (v["body"] or v["items"]):
            return sentences(v["body"] or v["items"][0], 1)
    return ""


def short(s: str, most: int = 70) -> str:
    """At most `most` characters: whole phrases when a ; , or : falls past half of it, else whole words."""
    s = plain(s)
    if len(s) <= most:
        return s
    cut = max(s.rfind(c, 0, most) for c in ("; ", ", ", ": "))          # never inside 1,319
    return (s[:cut] if cut > most // 2 else s[:most].rsplit(" ", 1)[0]) + " …"


def task_lines(t: dict, cfg: dict, topics: dict, word: str, level: int) -> list[str]:
    """A Task box's lines, fullest at level 0: its Runs' state, input, output, numbers, finding, its own topic.
    Each level drops some detail; the detail stays in the Task's own topic (→ sNN)."""
    here = topics.get(f"{t['row']['task'].parent.name}/{t['name']}")
    own = (cfg.get("tasks") or {}).get(t["name"]) or (cfg.get("tasks") or {}).get(t["id"]) or {}
    put, got = own.get("input") or t["input"], own.get("output") or t["output"]   # the face's words, else its page's
    found = finding(t, cfg)
    if found and level >= 2:
        found = short(found, 90 if level == 2 else 50)
    tal = (cfg.get("_tally") or {}).get(t["name"])
    if level >= 5:                                           # the tightest: its marks, its count, its topic
        if not t["runs"] and tal and tal["runs"]:            # no Run of its own: the design's count (261013)
            marks = "".join(MARKS[k] for k in ("done", "part", "ticket", "failed") if tal[k])
            return [f"{marks}{'' if level >= 7 else ' ' + n_of(tal['runs'], 'Run')}" + (f" → {here[:3]}" if here else "")]
        marks = "".join(sorted({r["mark"] for r in t["runs"]})) or "⬜"
        return [f"{marks}{'' if level >= 7 else ' ' + n_of(len(t['runs']), word)}" + (f" → {here[:3]}" if here else "")]
    lines = [f"{n_of(len(t['runs']), word)}: {states(t['runs'])}" if t["runs"] else
             tally_line(tal, cfg.get("_runs_word", "Runs")) if tal and tal["runs"] else "⬜ no Run yet"]
    if level == 0:
        lines += ([f"📥 {short(put)}"] if put else []) + ([f"📤 {short(got)}"] if got else [])
    if t["values"] and level <= 3:
        lines.append(f"📈 {' · '.join(t['values'][:3 if level <= 1 else 2])}")
    if found and level <= 3:
        lines.append(f"💡 {found}")
    if not (found or t["values"]) and t["runs"] and level <= 3 and not any(r["mark"] == "✅" for r in t["runs"]):
        lines.append("⬜ no result yet")
    return lines + ([f"→ details: {here[:3]}"] if here else [])


def plan_frame(d: Drawing, info: dict, tasks: list[dict], topics: dict, cfg: dict) -> dict:
    """② what goes in, each Task in order with what it found, what comes out; the reading is the key point.
    Every Task is its own box, four to a row; the boxes hold as much as ⑦'s 200 words allow, fullest first."""
    runs = [r for t in tasks for r in t["runs"]]
    srcs = [s for t in tasks for s in t["sources"]]
    word = srcs[0]["word"] if srcs else "Run"
    platforms = sorted({s["platform"] for s in srcs if s["platform"]})
    stand = next((t for t in tasks if any(r["mark"] != "✅" for r in t["runs"]) or not t["runs"]), None)
    pages = sum(1 for t in tasks if t["page"])
    cards = sum(t["cards"] for t in tasks)
    reading = str(cfg.get("reading") or "").strip() or \
        "❓ No reading yet: write what this Job found, in one or two sentences, in the face's job: yaml (reading)."
    opens = [open_line(o, closer=False) for o in (cfg.get("open") or [])]
    start = len(d.els)
    for step in range(13):                                   # in and out shorten first, then the Task boxes
        del d.els[start:]
        io, level = min(step, 4), max(0, step - 4)
        f = d.frame(f"② 🔁 In → Tasks → out: what {info['id']} found")
        top = jr.heading(d, "🔁 In → Tasks → out, and what it found", "📍 where the Job stands; → a Task's own topic")
        ins, outs = ([re.sub(r"\s*\([^)]*\)", "", str(x)) for x in cfg.get(k) or []]    # a map: no asides
                     for k in ("inputs", "outputs"))
        most, keep = [(400, 4), (200, 3), (140, 2), (100, 2), (100, 1)][io]
        seq = [{"title": "📥 What goes in", "lines": [short(x, most) for x in ins[:keep]], "weight": 1}
               if ins else {"title": f"📥 {n_of(len(runs), word)}",
                            "lines": [f"from {', '.join(platforms)}"] if platforms else [], "weight": 0.7}]
        for t in tasks:
            seq.append({"title": f"{'📍' if t is stand else '🧩'} {t['id']} · {t['title'] if level < 4 else short(t['title'], 28)}",
                        "lines": task_lines(t, cfg, topics, word, level), "weight": 1.5})
        seq.append({"title": "📤 What comes out", "lines": [short(x, most) for x in outs[:keep]],
                    "weight": 1} if outs else
                   {"title": f"📤 {pages} page{'s' if pages != 1 else ''}" + (f", {cards} Result Cards" if cards else ""),
                    "lines": [], "weight": 0.7})
        per = 5 if len(seq) <= 5 else 4
        y = top
        for k in range(0, len(seq), per):
            row = seq[k:k + per]
            if k:                                            # the next row follows on: a line down from the last box
                d.line([(W - 120, y - 70), (W - 120, y - 40), (120, y - 40), (120, y - 6)], sw=3)
                d.text(140, y - 70, "then", 28)
            labels = ["read by" if k + n == 0 else "writes" if k + n + 1 == len(seq) - 1 else "then"
                      for n in range(len(row) - 1)]
            y = flow(d, row, 40, y, W - 80, labels) + 110
        y -= 110
        d.line([(W / 2, y + 6), (W / 2, y + 66)], sw=3)                    # what the Tasks found, into the reading
        d.text(W / 2 + 16, y + 14, "found", 28)
        y += 70
        said = reading if level < 8 or reading.startswith("❓") else sentences(reading, 1) + " …"   # the rest in the face
        kh = jr.tall("🎯 " + said, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, ("" if said.startswith("❓") else "🎯 ") + said, W - 140, 30)
        y += kh + 24
        total = sum((cfg.get("_tally") or {}).values(), Counter())
        stand_line = (f"📍 {n_of(len(runs), 'Run')}: {states(runs)}." if runs or not total["runs"] else
                      f"📍 {tally_line(total, cfg.get('_runs_word', 'Runs'))}, read from the design grids (Act 2).")
        y = para(d, 40, y, stand_line +
                 (f"  {opens[0]}" + (f" (+{len(opens) - 1} more open)" if len(opens) > 1 else "")
                  if opens and level < 6 else ""), W - 80, 28) + 8
        if Drawing.words_small(d.els, f["id"])[0] <= MAP_BUDGET:
            break
    return finish(d, f, y)


def detail_frame(d: Drawing, info: dict, tasks: list[dict], topics: dict, cfg: dict, assets: Path, mark: str = "③",
                 steps=None) -> dict:
    """③ the Job explained from zero (asked 261012: "this is very thin … If I am a reader, will this answer my
    questions for this job"): what it is for and the words to know; what goes in and what comes out; its core formula;
    each Task (asked, did, found, its numbers, → its topic); what it concluded and how sure; what is open and what
    would close it. Words from the face's job: yaml; numbers and states from disk. Built with excalidraw-task's boxes.
    `steps(d, f, y, boxes)`, given by layout: explained, draws the Tasks itself, as stairs, and returns the y below."""
    import task_drawing as td
    f = d.frame(f"{mark} 📚 {info['id']} · {info['title']}: explained from zero", td.W, 1600)   # the next free mark
    runs = [r for t in tasks for r in t["runs"]]
    y = td.heading(d, f"📚 {info['id']} · {info['title']}, explained from zero",
                   f"{info['block']} · {n_of(len(tasks), 'Task')} · {n_of(len(runs), 'Run')}: {states(runs)}",
                   str(cfg.get("reading") or cfg.get("aim") or info["goal"] or "❓ no reading yet"))
    intro = str(cfg.get("intro") or cfg.get("aim") or info["goal"] or info["topic"] or "❓ no aim on the Job face")
    terms = td.terms_items(cfg.get("terms"))
    ins = [f"· {x}" for x in cfg.get("inputs") or []] or \
        [f"· {t['id']}: {short(t['input'], 120)}" for t in tasks if t["input"]] or ["❓ inputs not written"]
    outs = [f"· {x}" for x in cfg.get("outputs") or []] or \
        [f"· {t['id']}: {short(t['output'], 120)}" for t in tasks if t["output"]] or ["❓ outputs not written"]
    formulas = td.formula_items(cfg.get("formula"), assets)
    words = cfg.get("tasks") or {}
    boxes = []
    for t in tasks:
        w = words.get(t["name"]) or words.get(t["id"]) or {}
        here = topics.get(f"{t['row']['task'].parent.name}/{t['name']}")
        body = [f"Asked: {w['asked']}" if w.get("asked") else f"Asked: {t['question'] or '❓ no question on its page'}"]
        if w.get("did"):
            body.append(f"Did: {w['did']}")
        tal = (cfg.get("_tally") or {}).get(t["name"])
        body.append(f"{n_of(len(t['runs']), 'Run')}: {states(t['runs'])}" if t["runs"] else
                    f"⬜ no Run folder in the Task yet; its {tal['runs']} {cfg.get('_runs_word', 'Runs')} are read from "
                    "the design's tickets and evals" if tal and tal["runs"] else "⬜ no Run yet")
        if t["values"]:
            body.append("📈 " + " · ".join(t["values"][:6]))
        found = w.get("found") or finding(t, cfg)
        body.append(f"Found: {found}" if found else "❓ no finding written")
        if here:
            body.append(f"→ details: its own topic, studio/{here}/; the Task page, "
                        f"{t['row']['task'].parent.name}/{t['name']}/{t['name']}.md")
        boxes.append((f"🧩 {t['id']} · {t['title']}", body, INK))
    task_rows = [boxes[k:k + 2] for k in range(0, len(boxes), 2)]
    opens = [open_line(o) for o in cfg.get("open") or []]
    concluded = [str(cfg.get("reading") or "❓ no reading yet")] + ([f"How sure: {cfg['sure']}"] if cfg.get("sure") else [])
    middle = ([("📖 Words to know first", terms, INK, 1.2)] if terms else []) + \
        [("📥 What goes in", ins, INK, 1), ("📤 What comes out", outs, INK, 1)]
    top = [[("💡 What this Job is for", [intro], INK, 1), ("🎯 What it concluded, and how sure", concluded, INK, 1)],
           middle] + ([[("🧮 The core formula, explained", formulas, INK)]] if formulas else [])
    said = ["so it found", "the words first" if terms else "what goes in"] + \
        (["what goes in"] if terms else []) + ["comes out"] + (["the math"] if formulas else [])
    still = [("❓ What is open, and what would close it", opens or ["nothing open is listed"], RED)]
    if steps:                                   # layout: explained: the Tasks as stairs, their results beside them
        y = steps(d, f, td.rows_of(d, y, top, said) + 190, boxes)
        return td.fit(d, f, td.rows_of(d, y, [still], []), detail=True)
    rows = top + task_rows + [still]
    labels = said + ["the Tasks"] + ["then"] * max(0, len(boxes) - 1) + ["still open"]
    bottom = td.rows_of(d, y, rows, labels)
    return td.fit(d, f, bottom, detail=True)


def shown_frame(d: Drawing, info: dict, pics: list[Path], job: Path) -> dict:
    """The Job's pictures, when it has any; a Task's tables and formulas are its own topic's."""
    f = d.frame(f"④ 🖼️ {info['id']}'s pictures")
    top = jr.heading(d, "🖼️ Its pictures", f"{len(pics)} in the Job's folders and Results")
    pw = (W - 80 - 40 * (MOST_PICTURES - 1)) / MOST_PICTURES
    hs = []
    for i, p in enumerate(pics[:MOST_PICTURES]):
        px = 40 + i * (pw + 40)
        h = d.picture(p, px, top, pw, 900)
        para(d, px, top + h + 10, Path(os.path.relpath(p, job)).as_posix(), pw, 22)
        hs.append(h + 50)
    return finish(d, f, top + max(hs) + 20)


NB_LINE = re.compile(r"^\s*([\w.\-]+):\s*(\{.*\})\s*$")


def read_data(path: Path):
    """A file's data for an `at`: job_results.load (JSON, YAML, CSV up to 4 MB); a larger JSON still (one value is
    worth reading: j03 t01's 7 MB token counts); an executed notebook's printed results, each output line
    `<name>: {…}` a key (the legacy finetune notebooks print `test-id: {'kl': 0.19, …}`, 261013)."""
    data = jr.load(path)
    if data is not None or not path.is_file():
        return data
    try:
        if path.suffix == ".json" and path.stat().st_size < 200_000_000:
            import json
            return json.loads(path.read_text(encoding="utf-8"))
        if path.suffix == ".ipynb":
            import ast
            import json
            out = {}
            for cell in json.loads(path.read_text(encoding="utf-8")).get("cells") or []:
                for o in cell.get("outputs") or []:
                    text = "".join(o.get("text") or (o.get("data") or {}).get("text/plain") or [])
                    for line in text.splitlines():
                        m = NB_LINE.match(line)
                        if m:
                            try:
                                out[m.group(1)] = ast.literal_eval(m.group(2))
                            except (ValueError, SyntaxError):
                                pass
            return out or None
    except (OSError, ValueError):
        return None
    return None


def chart_value(block: Path, at: str):
    """`<path under the Block>:<key.inside>`, read from disk: a chart's numbers are never typed."""
    path, _, key = str(at).partition(":")
    v = jr.dig(read_data(block / path), key)
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def bars_png(block: Path, bars: list, out: Path, legend: list | None = None) -> Path | None:
    """Per row, before (grey) → after (black; a contrast row lighter), or one value alone (black); each value printed at
    its end (the s24 pilot). `legend`: the two bars' names (default before, after)."""
    rows = []
    for b in bars:
        at = b.get("at") or []
        vals = [chart_value(block, a) for a in (at if isinstance(at, list) else [at])]
        if vals and None not in vals:
            rows.append((str(b.get("label", "")), vals[0] if len(vals) == 2 else None, vals[-1], bool(b.get("contrast"))))
    if not rows:
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    plt.rcParams.update({"font.size": 26, "axes.spines.top": False, "axes.spines.right": False})
    pct = all(0 <= v <= 1 for r in rows for v in r[1:3] if v is not None)
    k = 100 if pct else 1
    top = max(v for r in rows for v in r[1:3] if v is not None) * k
    low = min(0.0, min(v for r in rows for v in r[1:3] if v is not None) * k)   # a negative value draws left of 0
    fig, ax = plt.subplots(figsize=(24, 1.9 * len(rows) + 1.2), dpi=100)
    fmt = (lambda v: f"{v * 100:.1f}%") if pct else (lambda v: f"{v:,.0f}" if abs(v) >= 1000 else f"{v:,.3g}")
    for i, (label, before, after, contrast) in enumerate(reversed(rows)):
        dy = 0.2 if before is not None else 0
        if before is not None:
            ax.barh(i + dy, before * k, height=0.36, color="#b8b8b8")
            ax.text(before * k + top * 0.01, i + dy, fmt(before), va="center", fontsize=26, color="#555")
        ax.barh(i - dy, after * k, height=0.36 if dy else 0.55, color="#8a8a8a" if contrast else "#2b2b2b")
        ax.text(after * k + top * 0.01, i - dy, fmt(after), va="center", fontsize=30, weight="bold")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in reversed(rows)], fontsize=28)
    ax.set_xlim(low * 1.15 if low < 0 else 0, 100 if pct else top * 1.15)
    if low < 0:
        ax.axvline(0, color="#1e1e1e", linewidth=1)
    if any(r[1] is not None for r in rows):
        names = list(legend or ["before", "after"])
        ax.legend(handles=[Patch(color="#b8b8b8", label=names[0]), Patch(color="#2b2b2b", label=names[1])],
                  loc="lower right", bbox_to_anchor=(1.0, 1.0), ncol=2, fontsize=26, frameon=False)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return out


STATES = {"done": "✅", "planned": "⬜", "blocked": "❌", "running": "🔶", "selected": "☑", "candidate": "☐"}


def cell_text(block: Path, c) -> str:
    """A table cell: plain words, or {label, at, fmt} read from a Run's receipt (a list of `at` joins with ' / ')."""
    if not isinstance(c, dict):
        return str(c)
    if not c.get("at"):
        return str(c.get("text", ""))
    vals = [chart_value(block, a) for a in (c["at"] if isinstance(c["at"], list) else [c["at"]])]
    pct = c.get("fmt") == "pct"
    shown = " / ".join("?" if v is None else f"{v * 100:.1f}%" if pct else (f"{v:,.0f}" if abs(v) >= 1000 else f"{v:,.4g}") for v in vals)
    return f"{c.get('label', '')} {shown}".strip()


def settings_frame(d: Drawing, info: dict, spec: dict, block: Path, mark: str = "③") -> dict:
    """A Job's Runs and their experiment settings, done and planned, one row each (asked 261012 on j02: "could you also
    list what are the runs and experiment settings we want to do? should we have a table for that?"): a real table,
    its columns compared across rows; a planned row dashed; a result cell read from the Run's receipt."""
    cols, rows = [str(c) for c in spec["columns"]], spec.get("rows") or []
    title = str(spec.get("title") or f"🧪 {info['id']}'s Runs and their settings")
    f = d.frame(f"{mark} {title}")
    d.detail(f)
    d.room(f)
    d.heading(title)
    y = (d.para(40, 112, str(spec["sub"]), W - 680, 28) + 24) if spec.get("sub") else 130
    if spec.get("key"):
        kh = Drawing.height(str(spec["key"]), W - 140, 34) + 40
        d.key(40, y, W - 80, kh)
        d.para(70, y + 20, str(spec["key"]), W - 140, 34)
        y += kh + 40
    body = [[(f"{STATES.get(str(r.get('state', '')), '')} " if k == 0 else "") + cell_text(block, c)
             for k, c in enumerate(r.get("cells") or [])] for r in rows]
    need = [max([Drawing.measure(h, 28)] + [min(Drawing.measure(b[k], 28), 900) for b in body if k < len(b)]) + 50
            for k, h in enumerate(cols)]
    widths = [n * (W - 80) / sum(need) for n in need]
    y = d.grid_table(40, y, cols, [{"cells": b, "dim": str(r.get("state")) in ("planned", "candidate")}   # b03's grid
                                   for r, b in zip(rows, body)], widths, 28)
    if spec.get("caption"):
        y = d.para(40, y + 24, str(spec["caption"]), W - 80, 28)
    return finish(d, f, y)


def models_spec(block: Path, spec: dict) -> dict:
    """A Job's model list (a yaml under the Block: models: [{id, family, params_b, license, gated, used, why, select}])
    as a settings table: selected first, each row ☑ or ☐ (asked 261012: "setup the list of models and we can select")."""
    import yaml as _yaml
    models = (_yaml.safe_load((block / spec["file"]).read_text()) or {}).get("models") or []
    models = sorted(models, key=lambda m: (not m.get("select"), float(m.get("params_b") or 0)))
    rows = [{"state": "selected" if m.get("select") else "candidate",
             "cells": [str(m.get("id", "")), str(m.get("family", "")), f"{float(m.get('params_b') or 0):.2f}B",
                       str(m.get("license", "")) + (" · gated" if m.get("gated") not in (False, None, "false") else ""),
                       str(m.get("used", "")), str(m.get("why", ""))]} for m in models]
    picked = sum(1 for m in models if m.get("select"))
    return {"title": spec.get("title") or "🧭 Models to choose from", "sub": spec.get("sub") or
            f"from {spec['file']}: set select: true or false there; each selected model runs t02 and t03",
            "key": spec.get("key") or f"{picked} of {len(models)} selected; every model checked on the Hugging Face Hub.",
            "columns": ["Model (Hugging Face id)", "Family", "Size", "Licence", "Used in Proj10", "Why measure it"],
            "rows": rows, "caption": "☑ selected · ☐ a candidate (dashed). Sizes are parameter counts from the Hub."}


def run_model(run: Path) -> str:
    """The model a Run measured: its run.yaml's `model:`, else a `model` in its result's JSON files."""
    import yaml as _yaml
    rec = run / "run.yaml"
    m = (_yaml.safe_load(rec.read_text()) or {}).get("model") if rec.is_file() else None
    for js in sorted((run / "result").glob("*.json")) if not m else []:
        m = (jr.load(js) or {}).get("model") if isinstance(jr.load(js), dict) else None
        if m:
            break
    return str(m or "")


def matrix_frame(d: Drawing, info: dict, spec: dict, job: Path, mark: str = "③") -> dict:
    """Models × measures, drawn as b03's model × engine grid (asked 261012: "I want the tables like this"; "setup the
    list of models and we can select and explore"): one row per model in the list file, ☑ selected first, ☐ a
    candidate grey; one column per measure; each cell the measured number large, its mark and Run small under it,
    read from the Run whose model it is; a selected model not yet run shows ⬜ to run."""
    import yaml as _yaml
    models = (_yaml.safe_load((job.parent / spec["file"]).read_text()) or {}).get("models") or []
    models = sorted(models, key=lambda m: (not m.get("select"), float(m.get("params_b") or 0)))
    measures = spec.get("measures") or []
    found = {}                                                          # (model, measure k) -> (value, run, state)
    for k, ms in enumerate(measures):
        for run in sorted((job / str(ms["task"]) / "runs").glob("*/")):
            v = chart_value(job.parent, f"{run.relative_to(job.parent)}/result/{ms['at']}") \
                if (run / "result").is_dir() else None
            if v is not None:
                found.setdefault((run_model(run), k), (v, run.name))
    rows = []
    for m in models:
        mid, picked = str(m.get("id", "")), bool(m.get("select"))
        size = f"{float(m.get('params_b') or 0):.2f}B"
        gated = " · gated" if m.get("gated") not in (False, None, "false") else ""
        cells = [f"{'☑' if picked else '☐'} {mid}\n{size} · {m.get('family', '')}{gated}"]
        for k, ms in enumerate(measures):
            hit = found.get((mid, k))
            if hit:
                v, rid = hit
                cells.append({"big": f"{v * 100:.1f}%" if ms.get("fmt") == "pct" else (f"{v:,.0f}" if abs(v) >= 1000 else f"{v:,.4g}"), "tag": f"✅ {rid[:3]}"})
            else:
                cells.append({"tag": "⬜ to run"} if picked else "")
        rows.append({"cells": cells, "dim": not picked})
    title = str(spec.get("title") or f"🧭 {info['id']}: each model, each measure")
    f = d.frame(f"{mark} {title}")
    d.room(f)
    d.heading(title)
    picked = sum(1 for m in models if m.get("select"))
    sub_ = str(spec.get("sub") or f"rows from {spec['file']} (select: true runs it); every cell read from a Run's result")
    y = d.para(40, 112, sub_, W - 680, 28) + 24
    key = str(spec.get("key") or f"{picked} of {len(models)} models selected; {len(found)} cells measured so far.")
    kh = Drawing.height(key, W - 140, 34) + 40
    d.key(40, y, W - 80, kh)
    d.para(70, y + 20, key, W - 140, 34)
    y += kh + 40
    cols = [str(spec.get("first") or "model")] + [str(ms.get("label", "")) for ms in measures]
    first = 720
    y = d.grid_table(40, y, cols, rows, [first] + [(W - 80 - first) / max(1, len(measures))] * len(measures), 28)
    cap = str(spec.get("caption") or "☑ selected · ☐ a candidate (grey) · ✅ measured, its Run below the number · ⬜ selected, not run yet")
    y = d.para(40, y + 24, cap, W - 80, 28)
    return finish(d, f, y)


def chart_frame(d: Drawing, info: dict, spec: dict, block: Path, assets: Path, mark: str = "③") -> dict | None:
    """What the Job found, as a picture (asked 261012 of a text-wall ③: "so rigid, not vivid, no one have the incentive
    to zoom in and read"): its key point, then before → after bars read from disk, one short caption."""
    png = bars_png(block, spec.get("bars") or [], assets / f"chart_{info['id']}.png", spec.get("legend"))
    if not png:
        return None
    title = str(spec.get("title") or f"📈 What {info['id']} found")
    f = d.frame(f"{mark} {title}")
    d.heading(title)
    y = (d.para(40, 112, str(spec["sub"]), W - 680, 28) + 24) if spec.get("sub") else 130
    key = str(spec.get("key") or "")
    if key:
        kh = Drawing.height(key, W - 140, 34) + 40
        d.key(40, y, W - 80, kh)
        d.para(70, y + 20, key, W - 140, 34)
        y += kh + 40
    cap = str(spec.get("caption") or "")
    h = d.picture(png, 40, y, W - 80, 1440 - y - (Drawing.height(cap, W - 80, 28) + 60 if cap else 40))
    bottom = d.para(40, y + h + 24, cap, W - 80, 28) if cap else y + h
    return finish(d, f, bottom)


# ── the design: each Task's Runs as grids, one mark per Run ─────────────────────────────────────────────────
MARKS = {"done": "✅", "part": "🔶", "ticket": "⬜", "failed": "❌", "none": "·"}
MARK_WORDS = {"done": "every eval found", "part": "some evals found", "ticket": "a ticket, no eval found",
              "failed": "listed as failed (why: the caption)", "none": "(a dot) not in the design"}


def _found(block: Path, pat: str) -> bool:
    """`<path under the Block>` exists, or `<path>:<key.inside>` holds a value: read from disk on every build."""
    path, _, key = pat.partition(":")
    p = block / path
    if not key:
        return p.exists()
    return jr.dig(read_data(p), key) is not None if p.is_file() else False


def design_of(block: Path, spec: dict) -> dict:
    """A Job's design (asked 261013 of Proj11 b01 s21: "How could I see in a glance about the design for each task and
    their runs? … and for these runs, what are their status?"): per grid, its rows × columns of Runs, each cell's state
    from disk (a ticket, its evals, a listed failure); per Task, a tally. `{row}`, `{col}` and a column's own fields fill
    the patterns; a pattern `<path>:<key>` asks for a value inside a file."""
    grids, tally = [], {}
    for fr in spec.get("frames") or []:
        for g in fr.get("grids") or []:
            rows = [str(r) for r in g.get("rows") or []]
            cols = [c if isinstance(c, dict) else {"label": str(c)} for c in g.get("cols") or []]
            evals = g.get("evals") or []
            cells = {}
            t = tally.setdefault(str(g.get("task", "")), Counter())
            for r in rows:
                for c in cols:
                    v = {k: str(x) for k, x in c.items()}
                    v.setdefault("col", v["label"])
                    v["row"] = r
                    ticket = bool(g.get("ticket")) and _found(block, str(g["ticket"]).format(**v))
                    found = sum(_found(block, str(e).format(**v)) for e in evals)
                    failed = any(str(f.get("row", "*")) in (r, "*") and str(f.get("col", "*")) in (v["label"], "*")
                                 for f in g.get("failed") or [])
                    state = ("failed" if failed and (ticket or found) else "done" if evals and found == len(evals)
                             else "part" if found else "ticket" if ticket else "none")
                    bare = bool(g.get("ticket")) and not ticket and state in ("done", "part", "failed")
                    cells[(r, v["label"])] = (state, bare)             # bare: evaluated, but no ticket in the design
                    if state != "none":
                        t[state] += 1
                        t["runs"] += 1
                        t["no ticket"] += bare
            grids.append({"g": g, "rows": rows, "cols": [c["label"] for c in cols], "cells": cells})
    return {"grids": grids, "tally": tally}


def tally_line(t: Counter, word: str = "Runs") -> str:
    marks = " · ".join(f"{t[k]} {MARKS[k]}" for k in ("done", "part", "ticket", "failed") if t[k])
    return f"{t['runs']} {word}: {marks}" + (f" ({t['no ticket']} with no ticket, marked *)" if t["no ticket"] else "")


def grid_size(rows: list, cols: list, title: str, size: float = 28, small: float = 24) -> tuple[float, float]:
    lw = max([Drawing.measure(r, size) for r in rows] + [60]) + 30
    cw = [max(Drawing.measure(c, small) + 26, 66) for c in cols]
    return max(lw + sum(cw), Drawing.measure(title, 32) + 20), 56 + 44 + len(rows) * size * 1.55 + 10


def grid_note(gr: dict) -> str:
    g = gr["g"]
    return f"rows: {g.get('row_name', '')} · columns: {g.get('col_name', '')}" if g.get("col_name") or g.get("row_name") else ""


def mark_grid(d: Drawing, x: float, y: float, gr: dict, size: float = 28, small: float = 24) -> None:
    """One grid: its title, its column names small and grey, a row per row value, a mark per Run (❌ red); what its
    rows and columns are, wrapped to the grid's own width so it never runs into the next grid."""
    rows, cols, cells = gr["rows"], gr["cols"], gr["cells"]
    lw = max([Drawing.measure(r, size) for r in rows] + [60]) + 30
    cw = [max(Drawing.measure(c, small) + 26, 66) for c in cols]
    d.text(x, y, str(gr["g"].get("title", "")), 32)
    if grid_note(gr):
        gw = grid_size(rows, cols, str(gr["g"].get("title", "")), size, small)[0]
        d.para(x, y + 100 + len(rows) * size * 1.55, grid_note(gr), gw, small if small >= 28 else small - 4, GREY)
    cx = x + lw
    for c, w in zip(cols, cw):
        d.text(cx, y + 56, c, small, GREY)
        cx += w
    yy = y + 100
    for r in rows:
        d.text(x, yy, r, size)
        cx = x + lw
        for c, w in zip(cols, cw):
            st, bare = cells[(r, c)]
            d.text(cx + 10, yy, MARKS[st], size, RED if st == "failed" else (GREY if st == "none" else INK))
            if bare:                                                    # evaluated, yet no ticket: findable
                d.text(cx + 10 + size * 1.15, yy - 6, "*", size, GREY)
            cx += w
        yy += size * 1.55


def lay_grids(d: Drawing, x0: float, y: float, mine: list, right: float, gap: float = 110, small: float = 24) -> float:
    """Grids left to right, wrapped at `right`; returns the y below them."""
    x, row_h = x0, 0
    for gr in mine:
        gw, gh = grid_size(gr["rows"], gr["cols"], str(gr["g"].get("title", "")), small=small)
        gh += (Drawing.height(grid_note(gr), gw, small if small >= 28 else small - 4) + 6) if grid_note(gr) else 0
        if x > x0 and x + gw > right:
            x, y, row_h = x0, y + row_h + 60, 0
        mark_grid(d, x, y, gr, small=small)
        x, row_h = x + gw + gap, max(row_h, gh)
    return y + row_h + 30


def design_frame(d: Drawing, info: dict, fr: dict, design: dict, mark: str) -> dict:
    """A frame of grids: its title, a key point with each Task's tally, the grids laid left to right and wrapped, then
    what each mark means and the frame's own caption."""
    title = str(fr.get("title") or f"🧭 {info['id']}'s Runs: the design and where each stands")
    f = d.frame(f"{mark} {title}")
    d.room(f)
    d.heading(title)
    y = (d.para(40, 112, str(fr["sub"]), W - 680, 28) + 24) if fr.get("sub") else 130
    mine = [gr for gr in design["grids"] if any(gr["g"] is g for g in fr.get("grids") or [])]
    tasks = list(dict.fromkeys(str(gr["g"].get("task", "")) for gr in mine))
    word = str(fr.get("runs_word") or "Runs")
    key = str(fr.get("key") or "") or " · ".join(f"{t[:3]}: {tally_line(design['tally'][t], word)}" for t in tasks)
    kh = Drawing.height(key, W - 140, 34) + 40
    d.key(40, y, W - 80, kh)
    d.para(70, y + 20, key, W - 140, 34)
    y += kh + 50
    y = lay_grids(d, 40, y, mine, W - 40)
    legend = "   ".join(f"{MARKS[k]} {MARK_WORDS[k]}" for k in ("done", "part", "ticket", "failed", "none"))
    if any(b for gr in mine for _, b in gr["cells"].values()):
        legend += "   * evaluated, but no ticket in the design's folder"
    y = d.para(40, y, legend, W - 80, 26) + 10
    if fr.get("caption"):
        y = d.para(40, y, str(fr["caption"]), W - 80, 26)
    return finish(d, f, y)


# ── layout: explained · the staircase (job_ladder, JL's s27 and sketch), titled "explained from zero": ① the Job and
#    its Tasks as steps, each Task's results a small chart inside ① on the right; ② its words, ③ its formula and the
#    design grids small, stepping down and right ────────────────────────────────────────────────────────────────────
BIG, MID, JOB_TABLE_W = 120, 80, 1900                          # the skeleton's type (JL 261013: "make this 10% to be the same size
                                            #   of 40% or 50%"): read at 10% zoom as 28 px reads at about 45%; the
                                            #   detail stays 24 to 32 px, read when zoomed in


def fmt_value(v) -> str:
    """A number short enough for its cell: 2.02B, 51.6M, 34K; 3 places under 1 (0.192 and 0.187 stay apart)."""
    if v is None:
        return "?"
    a = abs(v)
    return (f"{v / 1e9:.2f}B" if a >= 1e9 else f"{v / 1e6:.1f}M" if a >= 1e6 else f"{v / 1e3:.0f}K" if a >= 1e4 else
            f"{v:,.0f}" if a >= 1000 else f"{v:.1f}" if a >= 100 else f"{v:.2f}" if a >= 1 else f"{v:.3f}")


def results_card(d: Drawing, x: float, y: float, title: str, found: str, table: tuple | None, empty: str,
                 w: float = 1150) -> tuple[float, bool]:
    """A step's results as a table, not a figure (JL 261013: "I think we can have the things like table, not this
    figure"): its title large (MID), its finding in one sentence, then the table (cols, rows, widths); dashed with
    `empty` in red when it has no row."""
    import job_ladder as jl
    pad = jl.PAD
    yy = d.para(x + pad, y + pad, title, w - 2 * pad, MID) + 8
    if found:
        yy = d.para(x + pad, yy, f"💡 {jl.words(jr_first_sentence(found), 26)}", w - 2 * pad, 30) + 14
    is_open = not (table and table[1])
    if not is_open:
        cols, rows, widths = table
        yy = d.grid_table(x + pad, yy, cols, rows, widths, 28, pad=24) + 16
    else:
        yy = d.para(x + pad, yy, empty, w - 2 * pad, 30, RED) + 8
    h = yy - y + pad - 8
    d.box(x, y, w, h, GREY if is_open else INK, 1.5, dashed=is_open)
    return h, is_open


RUN_CARD_W = 760                            # a Run card beside its step


def run_cards(t: dict, design: dict, cfg: dict) -> list[dict]:
    """A step's Runs, every one shown (JL 261013: "for the tasks, I want the runs to be fully displayed here, so I can
    know for this task what are the runs we have"): its Run folders, a card each (its mark, its name, its state);
    when the Task holds none yet, a card per design grid (a sweep) holding the whole grid, a mark per Run, its row and
    column naming it, with its count by state, why a mark is red, and where its tickets are. [{lines, grid, dashed}]."""
    import job_ladder as jl
    if t["runs"]:
        return [{"lines": [(f"{r['mark']} {jl.run_label(r['name'])}", jl.T_RUNS, INK),
                           (str(r.get("state") or ""), jl.T_RUNS - 4, GREY)], "grid": None, "dashed": False}
                for r in t["runs"]]
    cards = []
    for gr in design["grids"]:
        g = gr["g"]
        if str(g.get("task", "")) != t["name"]:
            continue
        c = Counter(st for st, _ in gr["cells"].values() if st != "none")
        n = sum(c.values())
        status = " · ".join(f"{c[k]} {MARKS[k]}" for k in ("done", "part", "ticket", "failed") if c[k])
        title = re.sub(rf"^{t['id']}\s*·\s*", "", str(g.get("title", "")))
        after = []
        for fl in g.get("failed") or []:
            at = ", ".join(str(fl.get(k)) for k in ("row", "col") if str(fl.get(k, "*")) != "*") or "all"
            after.append((f"❌ {at}: {jl.words(str(fl.get('why', '')), 9)}", jl.T_RUNS - 4, RED))
        if g.get("ticket"):
            unit = str(g["ticket"]).split("/runs/")[0].rstrip("/").split("/")[-1]
            after.append((f"tickets: {unit}/runs/", jl.T_RUNS - 6, GREY))
        cards.append({"lines": [(f"{n_of(n, 'Run')}: {status}" if status else "⬜ none on disk", jl.T_RUNS - 2, INK)],
                      "grid": {**gr, "g": {**g, "title": f"🧪 {title}"}}, "after": after, "dashed": not c["done"]})
    return cards or [{"lines": [("⬜ no Run yet", jl.T_RUNS, GREY)], "grid": None, "dashed": True}]


GRID_COLOURS = {"done": "#2f9e44", "part": "#f08c00", "ticket": "#ced4da", "failed": "#e03131", "none": "#ffffff"}


def grid_png(gr: dict, out: Path) -> Path:
    """A sweep's Runs as a picture: a square per Run, its row and column naming it, coloured by where it stands (green
    evaluated, orange half, grey a ticket not evaluated, red failed, white not in the design; a dot: evaluated with no
    ticket). A picture, so a step's every Run shows without a wall of words."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    rows, cols, cells = gr["rows"], gr["cols"], gr["cells"]
    cell, lab = 0.5, 0.12 * max(len(r) for r in rows) + 0.3
    tilt = max(len(str(c)) for c in cols) > 3                           # a long column name stands tilted, never on
    top = 0.13 * max(len(str(c)) for c in cols) + 0.35 if tilt else 0.45   # its neighbour
    fig = plt.figure(figsize=(lab + cell * len(cols) + (0.6 if tilt else 0.15), top + cell * len(rows) + 0.1), dpi=100)
    ax = fig.add_axes([lab / fig.get_figwidth(), 0.1 / fig.get_figheight(),
                       cell * len(cols) / fig.get_figwidth(), cell * len(rows) / fig.get_figheight()])
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            st, bare = cells[(r, c)]
            ax.add_patch(Rectangle((j + 0.08, len(rows) - 1 - i + 0.08), 0.84, 0.84, color=GRID_COLOURS[st],
                                   ec="#adb5bd" if st == "none" else "none", lw=1))
            if bare:
                ax.plot(j + 0.5, len(rows) - 1 - i + 0.5, "o", color="white", ms=4)
    ax.set_xlim(0, len(cols))
    ax.set_ylim(0, len(rows))
    ax.set_xticks([j + 0.5 for j in range(len(cols))])
    ax.set_xticklabels(cols, fontsize=15, color="#495057", rotation=40 if tilt else 0, ha="left" if tilt else "center")
    ax.xaxis.tick_top()
    ax.set_yticks([len(rows) - 1 - i + 0.5 for i in range(len(rows))])
    ax.set_yticklabels(rows, fontsize=15, color="#1e1e1e")
    ax.tick_params(length=0, pad=3)
    for side in ax.spines.values():
        side.set_visible(False)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=100)
    plt.close(fig)
    return out


def run_card(d: Drawing, x: float, y: float, card: dict, assets: Path) -> tuple[float, float]:
    """One Run card: its title and count by state, then its grid as a picture (every Run a square), what its rows and
    columns are, why a square is red, where its tickets are; returns (width, height)."""
    import job_ladder as jl
    gr, pad = card.get("grid"), jl.PAD
    png = grid_png(gr, assets / f"runs-{re.sub(r'[^a-z0-9]+', '-', str(gr['g'].get('title', '')).lower()).strip('-')}"
                               f".png") if gr else None
    pw = 0
    if png:
        from PIL import Image
        with Image.open(png) as im:
            pw, ph = im.size
    head = ([(str(gr["g"].get("title", "")), jl.T_RUNS, INK)] if gr else []) + card["lines"]
    tail = ([(grid_note(gr), 20, GREY)] if gr and grid_note(gr) else []) + card.get("after", [])
    w = max(RUN_CARD_W if not gr else 0, pw + 2 * pad, 420)
    yy = y + pad
    for s_, z, col in head:
        yy = d.para(x + pad, yy, s_, w - 2 * pad, z, col) + 6
    if png:
        yy += d.picture(png, x + pad, yy + 4, pw, ph, fid=f"runs-{png.stem}") + 10
    for s_, z, col in tail:
        yy = d.para(x + pad, yy, s_, w - 2 * pad, z, col) + 6
    h = yy - y + pad - 6
    d.box(x, y, w, h, GREY if card.get("dashed") else INK, 1.2, dashed=card.get("dashed"))
    return w, h


SAY_STATE = {"done": "evaluated", "part": "half evaluated", "ticket": "not evaluated", "failed": "failed"}


def jr_first_sentence(s: str) -> str:
    return re.split(r"(?<=[.!?])\s+", str(s).strip())[0]


def formula_frame(d: Drawing, info: dict, cfg: dict, assets: Path, mark: str) -> dict | None:
    """The face's formula, small, explaining ①: the law, in words, its symbols, a worked example."""
    import task_drawing as td
    items = td.formula_items(cfg.get("formula"), assets)
    if not items:
        return None
    f = d.frame(f"{mark} 🧮 {info['id']}: the formula behind it", 1500)
    Drawing.room(f)
    h = td.card_height("🧮 The core formula, explained", items, 1400)
    td.card(d, 40, 40, 1400, h, "🧮 The core formula, explained", items, INK)
    canvas.explains(f)
    f["height"] = h + 80
    return f


def draw_explained(job: Path, out: Path, cfg: dict, source: str = "") -> tuple[Path, list[dict]]:
    """layout: explained (asked 261013 of Proj11 b01's s21: "make ⑦ 📚 j01 · pretrain: explained from zero to be the
    main … others to support it", "make it to be per tasks", "each task to a row", "make the main frame to be wider",
    then "read [the Paper-LLMRecPhy-work] session": the staircase JL drew and approved there, LLMRec b04 s27).
    ① the main frame, large and roomy: the reading; the Job (why, done when) with its In and Out; each Task a step
    lower and further right on a spine (job_ladder.columns), a small card under it (asks, did, → its topic) and its
    Runs as one small card branching right (a design's tally when its Runs are not yet in the Task); inside ① on its
    right, level with each step, its results as a small card: one sentence and a chart (a Task's: each settings row's
    low end → high end, the row's first cell naming the Task; the Job's: the face's chart, two series). Then the
    small frames that explain ①, stepping down and right (canvas.stairs): ② its words, how sure, what is open and
    what closes it (job_ladder.notes_frame); ③ its formula; then the design grids, every Run a mark."""
    import job_ladder as jl
    job = job.resolve()
    design = design_of(job.parent, cfg["design"]) if cfg.get("design") else {"grids": [], "tally": {}}
    cfg = {**cfg, "_tally": design["tally"], "_runs_word": str((cfg.get("design") or {}).get("runs_word") or "Runs")}
    rows = jr.job_rows(job.parent, job, {"show": cfg.get("show") or {}})
    tasks = [task_info(r, {"show": cfg.get("show") or {}}) for r in rows]
    info = job_info(job)
    assets = out.parent / "assets"
    topics = task_topics(job.parent)
    words_of = cfg.get("tasks") or {}
    table = (cfg.get("settings") or {}).get("rows") or []
    has_notes, has_formula = jl.has_notes(cfg), bool(cfg.get("formula"))
    marks = iter("②③④⑤⑥⑦⑧⑨⑩")
    m_notes = next(marks) if has_notes else ""
    m_formula = next(marks) if has_formula else ""
    cols_all = [str(c) for c in (cfg.get("settings") or {}).get("columns") or []]

    def task_table(t: dict) -> tuple | None:
        """Its settings rows as a table: the sweep, then each measure's low end → high end, the numbers large and
        the settings they come from small under them."""
        mine = [r for r in table if str((r.get("cells") or [""])[0]).strip() == t["id"]]
        if not mine:
            return None
        pairs = (max(len(r.get("cells") or []) for r in mine) - 3) // 2
        own = next((r["heads"] for r in mine if r.get("heads")), None)   # a Task measuring other things names them
        heads = ["Sweep"] + [(str(own[k]) if own and k < len(own) else
                              re.sub(r"(?i)^low( end)?:?\s*", "", cols_all[3 + 2 * k]) if 3 + 2 * k < len(cols_all)
                              else "") + ": low → high" for k in range(pairs)]
        rows_ = []
        for r in mine:
            c = list(r.get("cells") or []) + [""] * 8
            cells = [str(c[1])]
            for k in range(pairs):
                lo, hi = c[3 + 2 * k], c[4 + 2 * k]
                if isinstance(lo, dict) and isinstance(hi, dict):
                    vals = [chart_value(job.parent, x_["at"]) if x_.get("at") else None for x_ in (lo, hi)]
                    cells.append({"big": f"{fmt_value(vals[0])} → {fmt_value(vals[1])}", "size": 38,
                                  "tag": f"{lo.get('label', '')} → {hi.get('label', '')}"})
                else:
                    cells.append(str(lo or ""))
            rows_.append({"cells": cells, "dim": str(r.get("state")) in ("planned", "candidate")})
        if all(not any(isinstance(x_, dict) for x_ in r_["cells"]) for r_ in rows_):
            return None                                                 # only planned rows: nothing measured yet
        inner = 1150 - 2 * jl.PAD
        widths = [inner * 0.34] + [inner * 0.66 / max(1, pairs)] * pairs
        return heads, rows_, widths

    def job_table(chart: dict) -> tuple | None:
        """The face's chart as a table: one row per series, a column per bar."""
        bars = chart.get("bars") or []
        if not bars:
            return None
        names = list(chart.get("legend") or ["first", "second"])
        vals = [[chart_value(job.parent, a_) for a_ in (b_.get("at") if isinstance(b_.get("at"), list)
                                                       else [b_.get("at")])] for b_ in bars]
        rows_ = [{"cells": [names[k] if k < len(names) else ""] + [fmt_value(v[k]) if k < len(v) else "" for v in vals],
                  "dim": False} for k in range(max(len(v) for v in vals))]
        inner = JOB_TABLE_W - 2 * jl.PAD
        first = 260
        return [""] + [str(b_.get("label", "")) for b_ in bars], rows_, [first] + [(inner - first) / len(bars)] * len(bars)

    # JL's sketch (WellDoc-SPACE image.png, 261013): a wide, low frame; JOB at its top left; Task 1, 2, 3 each a step
    # lower and further right; from each, one long line out through the frame's right edge to its result, outside,
    # level with it. Measured first (each row as tall as its step or its result), then the frame is made wide.
    d = Drawing()
    STEP_X, ROW_GAP, OUT_GAP = 560, 150, 240                           # a step right; between rows; frame to results
    f = d.frame(f"① 📚 {info['id']} · {info['title']}: explained from zero", 4000)
    Drawing.room(f)
    d.text(40, 30, f"📚 {info['id']} · {info['title']}, explained from zero", 160)
    d.para(40, 250, f"{info.get('block') or ''} · {n_of(len(tasks), 'Task')}, a step each; each one's result outside, "
           "on the right; each square one Run: green evaluated · orange half · grey not evaluated · red failed · "
           "a dot no ticket" +
           (f"; below: {m_notes} its words, {m_formula} its formula" if m_notes and m_formula else ""), 3500,
           jl.T_RUNS, GREY)
    y = 340
    reading = str(cfg.get("reading") or "")
    head = f"🎯 {jr_first_sentence(reading)}" if reading else "❓ no reading yet: write the face's job.reading"
    rest = reading[len(jr_first_sentence(reading)):].strip() if reading else ""
    kh = Drawing.height(head, 3600 - 140, MID) + (Drawing.height(rest, 3600 - 140, 34) + 14 if rest else 0) + 50
    key_box = d.key(40, y, 3600 - 80, kh)
    yk = d.para(70, y + 22, head, 3600 - 140, MID) + 14
    if rest:
        d.para(70, yk, rest, 3600 - 140, 34)
    y += kh + 110

    rows_out = []                                                       # (line y, from x, title, found, png, empty)
    aim = str(cfg.get("intro") or cfg.get("aim") or info.get("goal") or "")
    job_label = f"🧱 {info['id']} · {info['title']}"
    job_w = max(jl.JOB_W, Drawing.measure(job_label, BIG) + 2 * jl.PAD + 30)
    jh = jl.card(d, 40, y, job_w, [(job_label, BIG, INK)], sw=3)
    why = [(f"Why: {jl.words(aim, 40)}" if aim else "❓ no aim: the Job face has no goal: line", jl.T_CARD, None),
           (f"Done when: {jl.words(info['close'], 34)}" if info.get("close") else "", jl.T_CARD, None)]
    ch = jl.card(d, 110, y + jh + 20, jl.JOB_W - 110, why)
    io_x, yy = 40 + job_w + 120, y
    for label, items in (("📥 In", (cfg.get("inputs") or [])[:3]), ("📤 Out", (cfg.get("outputs") or [])[:3])):
        if items:
            h = jl.card(d, io_x, yy, jl.IO_W, [(label, jl.T_STEP - 6, INK)] +
                        [(f"· {jl.words(x, 14)}", jl.T_RUNS, INK) for x in items])
            d.line([(40 + job_w + 12, y + jh / 2), (io_x - 12, yy + 32)], sw=2)
            yy += h + 24
    right = io_x + jl.IO_W
    chart = cfg.get("chart") or {}
    job_res = 0
    if chart:
        spec = (f"📊 {info['id']} result", f"{chart.get('title', '')}: {chart.get('key', '')}".strip(": "),
                job_table(chart), "❓ no value on disk for its table", JOB_TABLE_W)
        job_res = results_card(Drawing(), 0, 0, *spec)[0]
        rows_out.append((y + 60, io_x + jl.IO_W, *spec))
    spine_x, spine_top = 60, y + jh
    y = max(y + jh + 20 + ch, yy, y + job_res) + ROW_GAP

    prev = (spine_x, spine_top)                                        # where the next stair hangs from
    for i, t in enumerate(tasks):
        w = words_of.get(t["name"]) or {}
        nx = 130 + i * STEP_X
        name = re.sub(rf"^{t['id']}\s*[·:.\-]?\s*", "", t["title"], flags=re.I)
        short = re.sub(rf"^{t['id']}_", "", t["name"]).replace("_", " ")   # its folder's words: short, so large
        label = f"🧩 {t['id']} · {short}"
        node_w = max(jl.NODE_W, Drawing.measure(label, BIG) + 2 * jl.PAD + 30)
        nh = jl.card(d, nx, y, node_w, [(label, BIG, INK)], sw=2.5)
        own = topics.get(f"{t['row']['task'].parent.name}/{t['name']}")
        full = str(w.get("title") or ("" if re.match(r"(?i)\W*scaffold", name) else name))   # a placeholder is no title
        under = [(full, 34, INK),
                 (f"Asks: {jl.words(w.get('asked') or t.get('question') or '', 22)}" if (w.get("asked") or
                  t.get("question")) else "", jl.T_CARD, INK),
                 (f"Did: {jl.words(str(w.get('did') or ''), 22)}" if w.get("did") else "", jl.T_CARD, INK),
                 (f"→ details: {own[:3]}" if own else "", jl.T_CARD - 2, GREY)]
        cardh = jl.card(d, nx + 36, y + nh + 16, jl.CARD_W, under) + 16
        # its Runs and where each stands, branching right below the line out (JL 261013: "how could you list the
        # runs and the running status as well"): its Run folders, else one card per design grid (a sweep)
        cards = run_cards(t, design, cfg)
        rxr, ry, row_h = nx + node_w + 110, y + nh + 24, 0
        xx = rxr
        for c_ in cards:                                                # one row: the frame grows wide, not tall
            cw, chh = run_card(d, xx, ry, c_, assets)
            xx, row_h = xx + cw + 40, max(row_h, chh)
        if cards:
            bx = nx + node_w - 60                                       # right of its card, so no line crosses it
            d.line([(bx, y + nh), (bx, ry + 30)], arrow=False, sw=1.5)
            d.line([(bx, ry + 30), (rxr - 8, ry + 30)], sw=1.5)
            right = max(right, xx - 40)
            ry += row_h
        mid = y + nh / 2
        d.line([prev, (prev[0], mid), (nx - 8, mid)], sw=4)            # the stair: down from the last, right into it
        prev = (nx - 20, mid)                                           # the next hangs off this stair, left of the box
        right = max(right, nx + node_w)
        found = str(w.get("found") or finding(t, cfg) or "")
        spec = (f"📊 {t['id']} result", found, task_table(t), "❓ never evaluated: no number on disk yet", 1150)
        res = results_card(Drawing(), 0, 0, *spec)[0]
        rows_out.append((mid, nx + node_w, *spec))
        y = max(y + nh + 16 + cardh, ry, y + res - 20) + ROW_GAP
    opens = [o for o in cfg.get("open") or [] if o]
    y -= ROW_GAP - 60
    if opens:
        y = d.para(40, y, f"❓ {n_of(len(opens), 'point')} still open" + (f": what would close each is in {m_notes}"
                   if m_notes else ""), 3000, jl.T_CARD, RED) + 8
    height = y + 60
    width = max(right + 120, 3600)                                     # the frame ends where its widest step ends
                                                                        #   (JL 261013: "too much margin … the width of
                                                                        #   the frame … the same width [as] the last
                                                                        #   tasks"); the room is between the steps
    f["width"], f["height"] = width, height
    key_box["width"] = width - 80
    canvas.large(f)
    if Drawing.words_small(d.els, f["id"])[0] > MAP_WORDS:              # read up close, as job_ladder's ① is
        Drawing.detail(f)
    d.badge(f)
    main = f
    d.fid = None                                                        # the lines cross the frame's edge
    rx = width + OUT_GAP
    for ly, fx, title, found, tbl, empty, cw in rows_out:
        top = ly - 60
        h, open_ = results_card(d, rx, top, title, found, tbl, empty, cw)
        d.line([(fx + 16, ly), (rx - 14, ly)], sw=4, dashed=open_)

    below = [x for x in ([jl.notes_frame(d, info, cfg, m_notes)] if has_notes else []) +
             ([formula_frame(d, info, cfg, assets, m_formula)] if has_formula else []) +
             [] if x]
    placed = canvas.stairs(d.els, [main["id"]] + [(x["id"], 600 if k == 0 else 420) for k, x in enumerate(below)])
    d.fid = None
    names = ["its words" if has_notes else "in detail", "its formula" if has_formula else "in detail"]
    for k, (a_, b_) in enumerate(zip(placed, placed[1:])):
        x = b_["x"] + min(b_["width"], 600) / 2
        d.line([(x, a_["y"] + a_["height"] + 14), (x, b_["y"] - 14)], sw=5)
        d.text(x + 20, (a_["y"] + a_["height"] + b_["y"]) / 2 - 24, names[k] if k < 2 else "every Run", 36)
    d.write(out, source or f"excalidraw-job scripts/job_drawing.py {job.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out, rows


# ── the drawing ──────────────────────────────────────────────────────────────────────────────────────────────
def draw_job(job: Path, out: Path, cfg: dict | None = None, source: str = "") -> tuple[Path, list[dict]]:
    """Draw one Job into `out` (and its preview beside it); returns the drawing and its Task rows."""
    cfg = cfg or {}
    if str(cfg.get("layout") or "ladder") == "ladder":                 # asked 261013: Job → Tasks → Runs, each
        import job_ladder                                               # row's result to its right (job_ladder.py)
        return job_ladder.draw_job(Path(job), out, cfg, source)
    if str(cfg.get("layout")) == "explained":                          # asked 261013: ⑦ explained from zero
        return draw_explained(job, out, cfg, source)                    # is the main; the others back it
    job = job.resolve()
    design = design_of(job.parent, cfg["design"]) if cfg.get("design") else {"grids": [], "tally": {}}
    cfg = {**cfg, "_tally": design["tally"], "_runs_word": str((cfg.get("design") or {}).get("runs_word") or "Runs")}
    rows = jr.job_rows(job.parent, job, {"show": cfg.get("show") or {}})
    tasks = [task_info(r, {"show": cfg.get("show") or {}}) for r in rows]
    info = job_info(job)
    d = Drawing()
    topics = task_topics(job.parent)
    pics = pictures(job)
    fs = [why_frame(d, info, tasks, cfg)] + ([plan_frame(d, info, tasks, topics, cfg)] if tasks else [])  # no Task: no workflow
    if pics:
        fs.append(shown_frame(d, info, pics, job))
    plain = str(cfg.get("layout") or "") == "plain"                    # tables first, no arrows between frames
    nxt = iter("③④⑤⑥⑦⑧⑨⑩")
    designs = [design_frame(d, info, fr, design, next(nxt)) for fr in (cfg.get("design") or {}).get("frames") or []]
    if plain:                                                           # (asked 261012: "I want the tables like
        pick = matrix_frame(d, info, cfg["models"], job, next(nxt)) if cfg.get("models") else None   # this")
        found = chart_frame(d, info, cfg["chart"], job.parent, out.parent / "assets", next(nxt)) if cfg.get("chart") else None
        plan = settings_frame(d, info, cfg["settings"], job.parent, next(nxt)) if cfg.get("settings") else None
    else:
        plan = settings_frame(d, info, cfg["settings"], job.parent, next(nxt)) if cfg.get("settings") else None
        pick = settings_frame(d, info, models_spec(job.parent, cfg["models"]), job.parent, next(nxt)) \
            if cfg.get("models") else None
        found = chart_frame(d, info, cfg["chart"], job.parent, out.parent / "assets", next(nxt)) \
            if cfg.get("chart") else None
    # ③ "explained from zero" (a frame of text boxes) only when a face asks for it: asked 261012, "things like this
    # should be forbiden, so rigid, not vivid, no one have the incentive to zoom in and read". Its words stay in the face.
    detail = detail_frame(d, info, tasks, topics, cfg, out.parent / "assets", next(nxt)) if cfg.get("detail") is True else None
    acts = [{"name": "Act 1 · the Job: why, what it did, what it found", "frames": [f["id"] for f in fs],
             "arrow": ["planned as", "shown in"][:len(fs) - 1]}]
    later = [x for x in ((pick, found, plan, detail) if plain else (plan, pick, found, detail)) if x]
    later = designs + later                                             # the design first: what was planned, and its state
    if plain:                                                           # named acts, no arrow between frames
        acts[0]["arrow"] = []
        if later:
            acts.append({"name": "Act 2 · each model, what it found, the Runs", "frames": [x["id"] for x in later],
                         "arrow": []})
        later = []
    between = []
    if later and designs:                                               # the design is its own act (asked 261013):
        acts.append({"name": "Act 2 · what each Task ran: its Runs, and where each stands",   # every Run at a glance
                     "frames": [x["id"] for x in designs], "arrow": ["then"] * (len(designs) - 1)})
        between.append((fs[0]["id"], designs[0]["id"], "its Runs"))
    rest = [x for x in later if all(x is not g for g in designs)]
    if rest:
        words = {id(pick): "chosen from", id(found): "so it found", id(detail): "in words", id(plan): "at each end"}
        acts.append({"name": f"Act {len(acts) + 1} · what it ran, and what it found" if not designs else
                     f"Act {len(acts) + 1} · what the Runs found", "frames": [x["id"] for x in rest],
                     "arrow": [words[id(x)] for x in rest[1:]]})
        between.append((designs[0]["id"], rest[0]["id"], "what they found") if designs else
                       (fs[0]["id"], rest[0]["id"], "the Runs" if plan else "what it found"))
    d.acts(acts, between=between)
    # plain: `later` was emptied above, so no arrow runs down between the acts either
    d.write(out, source or f"excalidraw-job scripts/job_drawing.py {job.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out, rows


# ── the topic ────────────────────────────────────────────────────────────────────────────────────────────────
def face_cfg(face: Path) -> dict:
    """The face's `job:` yaml, with a results topic's `results:` yaml (job_results.py) read as its fallback."""
    m = re.search(r"```yaml\s*\n(job:.*?)```", jr.read(face), re.S)
    job = {}
    if m and yaml:
        try:
            job = (yaml.safe_load(m.group(1)) or {}).get("job") or {}
        except Exception as err:                              # a typo in the face is said, not hidden
            print(f"{face.name}: its job: yaml does not read ({err})", file=sys.stderr)
    res = jr.results_yaml(face)
    name = job.get("name") or next(iter(res.get("jobs") or []), None) or next(iter(res.get("reading") or {}), None)
    return {**job, "name": name,
            "reading": job.get("reading") or (res.get("reading") or {}).get(name or "", ""),
            "show": {**(res.get("show") or {}), **(job.get("show") or {})},
            "open": list(job.get("open") or []) + [o for o in (res.get("open") or []) if o not in (job.get("open") or [])]}


def draw(topic: Path) -> Path:
    """Redraw one Job topic from its face and the disk; refresh the face's Runs list when it has one."""
    topic = topic.resolve()
    face = topic / f"{topic.name}.md"
    cfg = face_cfg(face)
    job = topic.parents[1] / str(cfg.get("name") or "")
    if not cfg.get("name") or not job.is_dir():
        raise SystemExit(f"{face}: its job: yaml names no Job of {topic.parents[1].name} (job.name)")
    out, rows = draw_job(job, topic / f"{topic.name}.excalidraw", cfg,
                         f"excalidraw-job scripts/job_drawing.py {topic.name}")
    text = jr.read(face)
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        face.write_text(head + jr.ledger(topic, [job], {job.name: rows}) + rest.split(END, 1)[1], encoding="utf-8")
    return out


def scripts_from(topic: Path) -> str:
    """This folder, relative to the topic: through the SPACE's Tools link, or inside the Tools SPACE itself."""
    here_rel = HERE.relative_to(SKILLS.parents[3])            # plugins/haipipe-toolkit/skills/1_base/display/...
    for p in (topic, *topic.parents):
        for base in (p / "Tools", p):
            if (base / here_rel).is_dir():
                return jr.rel(base / here_rel, topic)
    return str(HERE)


def builder_text(topic: Path, title: str, script: str) -> str:
    return (f'"""{title}: drawn by excalidraw-job\'s job_drawing.py from the Job on disk and this face\'s job: '
            f"yaml; a person's marks on the drawing are kept.\n\n    python {script}\n\"\"\"\n"
            "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
            f'sys.path.insert(0, str((HERE / "{scripts_from(topic)}").resolve()))\n'
            "import job_drawing  # noqa: E402\n\nif __name__ == \"__main__\":\n    job_drawing.draw(HERE)\n")


WORDS = ("What no file says: `aim` (the Job's meaning in one sentence; empty: its face's goal: line), `reading` (what it "
         "concluded, ③'s key point), `conclusions` (per Task, lines that replace what its page says), `open` (open "
         "points, red in ③), `show` (per Run, values to read from its result, as in job_results.py).")


def job_yaml(name: str, aim: str = "", reading: str = "", open_: list | None = None) -> list[str]:
    q = lambda s: '"' + str(s).replace('"', "'") + '"'                                 # noqa: E731
    return ["```yaml", "job:", f"  name: {name}", f"  aim: {q(aim)}", f"  reading: {q(reading)}", "  conclusions: {}",
            "  open:" + ("" if open_ else " []"), *[f"    - {q(o)}" for o in (open_ or [])], "  show: {}", "```"]


def files_block(topic: Path, builder: str) -> list[str]:
    return ["```text", f"{topic.name}/", f"├── {topic.name}.md   this face",
            f"├── {topic.name}.excalidraw   four frames in two acts; a person's marks are kept",
            f"├── {topic.name}.png   its preview", f"└── {builder}   calls excalidraw-job's job_drawing.py", "```"]


def make(job: Path, nn: int | None = None, dry: bool = False) -> Path:
    job = job.resolve()
    block = job.parent
    if job.name in jr.covered(block):                         # one topic per Job: a results or a whole-Job topic
        have = [f.parent.name for f in (block / "studio").glob("s*/*.md")
                if job.name in (jr.results_yaml(f).get("jobs") or []) or face_cfg(f).get("name") == job.name]
        raise SystemExit(f"{job.name} already has a topic: {', '.join(have)}; redraw it (draw), or adopt a results topic")
    taken = jr.used(block)
    nn = nn or next((n for n in range(jr.BAND[0], jr.BAND[1] + 1) if n not in taken), None)
    if nn is None or nn in taken:
        raise SystemExit(f"{block.name}: no free number in s{jr.BAND[0]}-s{jr.BAND[1]}; name one with --nn")
    slug = re.sub(r"[^a-z0-9]+", "-", job.name.lower()).strip("-")[:48].rstrip("-")
    topic = block / "studio" / f"s{nn:02d}-{slug}"
    if dry:
        print(f"would make {topic.relative_to(block)}  ← {job.name}")
        return topic
    topic.mkdir(parents=True)
    builder = f"build_s{nn:02d}_{slug.replace('-', '_')}.py"
    title = f"s{nn:02d} · {job.name[:3]} · {jr.title_of(job)}: the whole Job"
    feeds = sorted(set(re.findall(r"q\d\d_[A-Za-z0-9_]+", jr.field(job, "answers"))))
    face = [title, "=" * len(title), "", "**Tags:** `Jobs`", "", "**Stage:** explore", "",
            f"**Topic:** The Job `{job.name}` as one drawing: why it exists, what goes in and comes out, what it "
            "concluded, and its tables, formulas and pictures, read from its face, its Task pages and its Runs on "
            "every build (excalidraw-job).", "",
            f"**Feeds:** `reports/` {' · '.join(feeds)}" if feeds else "**Feeds:** none yet; the Job's face names no Question.",
            "", f"**Job:** [{job.name}]({jr.rel(jr.face_of(job) or job, topic)})", "", "",
            "Words", "-----", "", WORDS, "", *job_yaml(job.name), "", BEGIN, END, "", "",
            "Files", "-----", "", *files_block(topic, builder), "", "", "Decided", "-------", "",
            f"s{nn:02d}-D01 · One Block topic draws the whole Job: why, in and out, what it concluded, its tables and "
            "pictures (asked 261012)", "", "", "Open", "----", "",
            "1. Write the Job's aim and its reading in the yaml above.", "",
            "(write here, or mark the drawing in red)", ""]
    (topic / f"{topic.name}.md").write_text("\n".join(face), encoding="utf-8")
    (topic / builder).write_text(builder_text(topic, title, builder), encoding="utf-8")
    groups = block / "studio" / "_groups.txt"
    lines = jr.read(groups).splitlines() if groups.is_file() else [
        "# Studio groups of this Block, in button order. The workbench writes this file when a group is",
        "# made, moved or deleted; a group's topics are the ones whose **Tags:** line names it."]
    if "Jobs" not in lines:
        groups.write_text("\n".join(lines + ["Jobs"]) + "\n", encoding="utf-8")
    return draw(topic)


def adopt(topic: Path, aim: str = "") -> Path:
    """A one-Job results topic made by job_results.py, redrawn as the whole Job: its builder now calls this script, its
    face gains the job: yaml (the results: yaml's reading and open points carried over) and says what it draws."""
    topic = topic.resolve()
    face = topic / f"{topic.name}.md"
    text = jr.read(face)
    res = jr.results_yaml(face)
    jobs = [str(j) for j in (res.get("jobs") or [])]
    if len(jobs) != 1:
        raise SystemExit(f"{face.name}: adopt takes a one-Job results topic; it names {len(jobs)} Jobs")
    name = jobs[0]
    if "```yaml\njob:" not in text:
        block_yaml = "\n".join(job_yaml(name, aim, (res.get("reading") or {}).get(name, ""), res.get("open") or []))
        m = re.search(r"```yaml\s*\nresults:.*?```", text, re.S)
        text = text[:m.start()] + block_yaml + text[m.end():] if m else text.replace(BEGIN, block_yaml + "\n\n" + BEGIN, 1)
    text = re.sub(r"(?m)^\*\*Topic:\*\*.*$", f"**Topic:** The Job `{name}` as one drawing: why it exists, what goes in "
                  "and comes out, what it concluded, and its tables, formulas and pictures, read from its face, its Task "
                  "pages and its Runs on every build (excalidraw-job).", text, count=1)
    text = re.sub(r"(?ms)^Results\n-------\n\n.*?(?=```yaml)", "Words\n-----\n\n" + WORDS + "\n\n", text, count=1)
    builder = next(topic.glob("build_*.py"))
    text = re.sub(r"(?ms)^```text\n" + re.escape(topic.name) + r"/\n.*?^```", "\n".join(files_block(topic, builder.name)),
                  text, count=1)
    first = text.splitlines()[0]
    if first.endswith(": current results"):
        new = first[: -len(": current results")] + ": the whole Job"
        text = text.replace(first + "\n" + "=" * len(first), new + "\n" + "=" * len(new), 1)
    face.write_text(text, encoding="utf-8")
    builder.write_text(builder_text(topic, text.splitlines()[0], builder.name), encoding="utf-8")
    return draw(topic)


# ── what each Task holds, as a table, and the Job's figures ──────────────────────────────────────────────────
# Asked 261013 on Proj01 b00_rawdata, 14 raw drops of 310 Tasks: "describe for each task, what we have done, what are
# the content, I might want more figures and tables, to understand what I have". A Job's words (a group face's per-Job
# entry, or `each:` for every Job) may hold `flow` (its steps; each line filled from disk), `table` (one row per Task,
# every cell read from that Task's own files), `figures` (bars made from the table, and pictures already in the Job's
# Results) and `scans` (named Tasks' own pictures). Every number is read on every build; the face holds paths and words.
SLOT = re.compile(r"\{([^{}]+)\}")


def first_match(folder: Path, pattern: str) -> Path | None:
    """`pattern` under `folder`, a glob allowed: its first match."""
    if any(c in pattern for c in "*?["):
        return next(iter(sorted(folder.glob(pattern))), None)
    p = folder / pattern
    return p if p.exists() else None


def raw_at(folder: Path, at: str, default: str = ""):
    """`<file under folder>:<key.inside>`, or `<key.inside>` in the default file: the value as stored."""
    path, sep, key = str(at).partition(":")
    if not sep:
        path, key = default, str(at)
    p = first_match(folder, path) if path else None
    if not p or not p.is_file():
        return None
    data = jr.load(p)
    return jr.dig(data, key) if key else data


def shown(v, col: dict) -> str:
    """A stored value as words: names joined, a count (`fmt: count`), a size (`gb`), words for a code (`words`);
    `only` keeps the rows of a list that match, `pick` takes one field of each, `most` keeps the first few; `none`
    when nothing is left."""
    fmt = str(col.get("fmt") or "")
    if isinstance(v, list) and col.get("only"):
        want = {k: [str(x) for x in (xs if isinstance(xs, list) else [xs])] for k, xs in col["only"].items()}
        v = [r for r in v if isinstance(r, dict) and all(str(r.get(k)) in xs for k, xs in want.items())]
    if isinstance(v, list) and col.get("pick"):
        v = [r.get(col["pick"]) if isinstance(r, dict) else r for r in v]
    if isinstance(v, list) and col.get("most") and len(v) > int(col["most"]):   # the first few, then how many more
        v = v[:int(col["most"])] + [f"+{len(v) - int(col['most'])} more"]
    if fmt == "count" and isinstance(v, (list, dict)):
        v = len(v)
    if v is None or v == "" or v == [] or isinstance(v, dict):
        return str(col.get("none", "—"))
    if fmt == "gb" and isinstance(v, (int, float)):
        return f"{v / 1e9:,.2f} GB"
    if isinstance(v, list):
        v = ", ".join(dict.fromkeys(str(x) for x in v if x not in (None, "")))
    if fmt == "words":
        return str(v).replace("_", " ")
    if isinstance(v, str):
        return v
    return jr.number(v, fmt if fmt in ("pct", "int") else "")


def fill(text, folder: Path) -> str:
    """Words with slots read from disk under `folder`: `{<file>:<key>|<fmt>|<words when empty>}` (a glob allowed),
    `{count:<glob>}`."""
    def one(m):
        body, *how = m.group(1).split("|")
        kind, _, rest = body.partition(":")
        if kind == "count":
            return f"{len(list(folder.glob(rest))):,}"
        return shown(raw_at(folder, body), {"fmt": how[0] if how else "", "none": how[1] if len(how) > 1 else "?"})
    return SLOT.sub(one, str(text))


def marks_of(runs: list[dict], named: bool = True) -> str:
    """What was done: each Run's number and mark (`r02 ✅  r07 ✅`), or for many Runs their marks counted."""
    if not runs:
        return "⬜ no Run"
    if named:                                                   # one mark per state, then its Runs: ✅ r02 r07
        by = {}
        for r in runs:
            by.setdefault(r["mark"], []).append(r["name"][:3])
        return "  ".join(f"{m} {' '.join(ns)}" for m, ns in by.items())
    c = Counter(r["mark"] for r in runs)
    return "  ".join(f"{n} {m}" for m, n in c.most_common())


def cell(folder: Path, col: dict, default: str, marks: str, title: str) -> tuple[str, object]:
    """One cell's words and the value it sorts by: `runs` (what was done), `count` (files matching a glob), `at` (a
    value, or a list of them joined by `join`); `else: title` puts the folder's title where the value is missing."""
    if col.get("runs"):
        return marks, None
    if col.get("count"):
        n = len(list(folder.glob(str(col["count"]))))
        return f"{n:,}", n
    ats = col.get("at")
    if isinstance(ats, list):
        vals = [raw_at(folder, a, default) for a in ats]
        if all(v in (None, "", []) for v in vals):
            return (title if col.get("else") == "title" else str(col.get("none", "—"))), None
        return str(col.get("join", " → ")).join(shown(v, {**col, "none": "?"}) for v in vals), vals[0]
    v = raw_at(folder, str(ats), default) if ats else None
    if v in (None, "", []) and col.get("else") == "title":
        return title, None
    return shown(v, col), v


def table_rows(folders: list[tuple[Path, list[dict], str]], spec: dict) -> list[dict]:
    """One row per folder the spec keeps (`rows`, a glob; `skip`, globs): its id, each column's words and values,
    sorted by `sort` (`-Rows`: the column Rows, largest first)."""
    import fnmatch
    want, skip = str(spec.get("rows") or "*"), [str(s) for s in spec.get("skip") or []]
    named = all(len(runs) <= MOST_RUNS for _, runs, _ in folders)
    out = []
    for folder, runs, title in folders:
        if not fnmatch.fnmatch(folder.name, want) or any(fnmatch.fnmatch(folder.name, s) for s in skip):
            continue
        marks, cells, vals = marks_of(runs, named), [], {}
        for col in spec.get("columns") or []:
            words, v = cell(folder, col, str(spec.get("file") or ""), marks, title)
            cells.append(words)
            vals[str(col.get("label", ""))] = v
        has = not spec.get("file") or first_match(folder, str(spec["file"])) is not None
        out.append({"folder": folder, "id": folder.name[:3], "cells": cells, "vals": vals, "has": has})
    by = str(spec.get("sort") or "")
    if by:
        key, down = by.lstrip("-"), by.startswith("-")
        num = lambda v: v if isinstance(v, (int, float)) and not isinstance(v, bool) else None   # noqa: E731
        out.sort(key=lambda r: (num(r["vals"].get(key)) is None,
                                -(num(r["vals"].get(key)) or 0) if down else (num(r["vals"].get(key)) or 0)))
    return out


def widths_of(cols: list[str], cells: list[list[str]], total: float, size: float) -> list[float]:
    """Columns as wide as their words (an emoji counted a full em; one column at most 760 px), filling `total`: when
    they do not fit, only the widest ones give room and wrap, so a short value (a month, a count) stays on one line."""
    em = lambda s: len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", s)) * size * 0.5      # noqa: E731
    need = [max([Drawing.measure(c, 28)] + [min(Drawing.measure(r[k], size) + em(r[k]), 760) for r in cells]) + 44
            for k, c in enumerate(cols)]
    if sum(need) <= total:
        return [n * total / sum(need) for n in need]
    lo, hi = 120.0, max(need)                                   # one cap for the widest columns: they alone wrap
    for _ in range(40):
        cap = (lo + hi) / 2
        lo, hi = (cap, hi) if sum(min(n, cap) for n in need) < total else (lo, cap)
    return [min(n, lo) for n in need]


def name_of(info: dict) -> str:
    return info["title"] if info["title"].startswith(info["id"]) else f"{info['id']} · {info['title']}"


def table_frame(d: Drawing, info: dict, w: dict, job: Path, rows: list[dict], assets: Path,
                mark: str = "①") -> tuple[dict, list]:
    """A Job's Tasks as a table: its steps first (what was done, with its numbers), its reading as the key point, then
    one row per Task (what it holds), the columns marked `bar` drawn as bars beside it, row by row, on a log scale (a
    scoreboard, not a wall of numbers); its open points in red."""
    spec = w["table"]
    body = table_rows([(r["task"], r["runs"], str(r["title"])) for r in rows], spec)
    title = fill(spec.get("title") or f"📋 {name_of(info)}: what each Task holds", job)
    f = d.frame(f"{info['id']} {mark} {title}")
    y = jr.heading(d, title, fill(spec.get("sub") or "one row per Task, each cell read from its own files on every build", job))
    steps = w.get("flow") or []
    if steps:
        seq = [{"title": fill(s.get("title", ""), job), "lines": [fill(x, job) for x in s.get("lines") or []],
                "key": bool(s.get("key"))} for s in steps]
        labels = [fill(x, job) for x in (w.get("arrows") or [])] + ["then"] * len(seq)
        y = flow(d, seq, 40, y, W - 80, labels, title=32, leaf=28) + 50
    reading = fill(w.get("reading") or "", job).strip()
    if reading:
        kh = jr.tall("🎯 " + reading, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + reading, W - 140, 30)
        y += kh + 40
    specs = spec.get("columns") or []
    keep = [k for k, c in enumerate(specs) if not c.get("bar")]
    bars = [str(c.get("label", "")) for c in specs if c.get("bar")]
    cols = ["Task"] + [str(specs[k].get("label", "")) for k in keep]
    cells = [[b["id"]] + [b["cells"][k] for k in keep] for b in body]
    room = 620 if bars and body else 0                                  # the bars, at the right of the table
    head = y
    y = d.grid_table(40, y, cols, [{"cells": c, "dim": not b["has"]} for c, b in zip(cells, body)],
                     widths_of(cols, cells, W - 80 - room, 28), 28, pad=18)
    if room:
        top = d.rows_at[0][0]
        bx = W - 40 - room + 30
        para(d, bx, head, f"{' and '.join(bars)}, on a log scale", room - 30, 28, GREY)
        png = bars_png_rows(body, bars, [(t - top, h) for t, h in d.rows_at], room - 30, y - top,
                            assets / f"bars_{job.name[:3]}.png")
        d.picture(png, bx, top, room - 30, y - top, fid=f"img-{job.name[:3]}-bars")
    if spec.get("caption"):
        y = para(d, 40, y + 16, fill(spec["caption"], job), W - 80, 24)
    for o in w.get("open") or []:
        o = {k: fill(v, job) for k, v in o.items()} if isinstance(o, dict) else fill(o, job)
        y = para(d, 40, y + 16, open_line(o), W - 80, 28)
    return finish(d, f, y), body


def bars_png_rows(body: list[dict], bars: list[str], at: list[tuple], wpx: float, hpx: float, out: Path) -> Path:
    """Bars that line up with a table's rows (`at`: each row's top and height, from its first row): one panel per
    column in `bars`, side by side, log scale, each number at its bar's end, at the table's own type size."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(wpx / 100, hpx / 100), dpi=100)
    gap = 0.05
    cols = [[v if isinstance(v, (int, float)) and not isinstance(v, bool) else None for v in
             (b["vals"].get(label) for b in body)] for label in bars]
    span = [len(f"{max([v for v in vs if v] or [1]):,.0f}") + 4 for vs in cols]   # a panel as wide as its numbers need
    widths = [(1 - gap * (len(bars) - 1)) * s / sum(span) for s in span]
    for j, (label, vals) in enumerate(zip(bars, cols)):
        ax = fig.add_axes([sum(widths[:j]) + gap * j, 0, widths[j], 1])
        top = max([v for v in vals if v] or [1])
        colour = "#2b2b2b" if j == 0 else "#8a8a8a"
        for (y, h), v in zip(at, vals):
            mid = y + h / 2
            if v:
                ax.barh(mid, v, height=min(h * 0.6, 34), color=colour, left=0.8)
            ax.text((v or 1) * 1.25 if v else 1.0, mid, f"{v:,.0f}" if v else ("0" if v == 0 else "—"),
                    va="center", fontsize=19, color="#1e1e1e")
        ax.set_xscale("log")
        ax.set_xlim(0.8, 0.8 * (max(top, 2) / 0.8) ** (1 / 0.5))   # the longest bar ends half way: room for its number
        ax.set_ylim(hpx, 0)
        ax.axis("off")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=100)
    plt.close(fig)
    return out


def figures_frame(d: Drawing, info: dict, w: dict, job: Path, body: list, mark: str = "②") -> dict | None:
    """The Job in pictures: what its Runs drew for the whole Job (`figures.pictures`, a timeline) on the left, its main
    Tasks' own pictures (`scans`, each at `scan.file` in the Task) on the right, each under its caption; the key point
    is the face's `shows`."""
    fig, scan = w.get("figures") or {}, w.get("scan") or {}
    left = []
    for p in fig.get("pictures") or []:
        hit = first_match(job, str(p.get("file", "")))
        if hit:
            left.append((hit, fill(p.get("caption") or Path(os.path.relpath(hit, job)).as_posix(), job)))
    named = {b["folder"].name: b for b in body}
    right = []
    for t in w.get("scans") or []:
        task = job / str(t)
        hit = first_match(task, str(scan.get("file") or "")) if scan.get("file") and task.is_dir() else None
        if hit:
            b = named.get(task.name)
            name = f"{task.name[:3]} · {b['cells'][0] if b else task.name}"
            right.append((hit, f"{name}: {fill(scan['caption'], task)}" if scan.get("caption") else name))
    if not (left or right):
        return None
    title = fill(fig.get("title") or f"📊 {name_of(info)} in pictures", job)
    f = d.frame(f"{info['id']} {mark} {title}")
    y = jr.heading(d, title, fill(fig.get("sub") or "the figures its Runs drew, read from disk on every build", job))
    shows = fill(w.get("shows") or "", job).strip()
    if shows:
        kh = jr.tall("🎯 " + shows, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + shows, W - 140, 30)
        y += kh + 40
    cols = [c for c in (left, right) if c]
    pw = (W - 80 - 60 * (len(cols) - 1)) / len(cols)
    ends = []
    for i, pics in enumerate(cols):
        px, yy = 40 + i * (pw + 60), y
        for k, (p, cap) in enumerate(pics):
            yy = para(d, px, yy, cap, pw, 28) + 12
            yy += d.picture(p, px, yy, pw, 1500, fid=f"img-{job.name[:3]}-{i}{k}-{p.parents[3].name[:3]}-{p.stem}") + 50
        ends.append(yy - 50)
    return finish(d, f, max(ends))


def jobs_frame(d: Drawing, title: str, jobs: list[Path], spec: dict, all_rows: dict) -> dict:
    """A family's Jobs as a table, one row per Job, each cell read from that Job's own files."""
    rows = [(j, [r for t in all_rows[j.name] for r in t["runs"]], jr.title_of(j)) for j in jobs]
    body = table_rows(rows, spec)
    head = str(spec.get("title") or f"📋 {title}: the Jobs side by side")
    f = d.frame(f"⓪ {head}")
    d.detail(f)
    y = jr.heading(d, head, str(spec.get("sub") or "one row per Job, each cell read from its own files on every build"))
    if spec.get("key"):                                                  # its slots read under the Block
        key = fill(spec["key"], jobs[0].parent)
        kh = jr.tall("🎯 " + key, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + key, W - 140, 30)
        y += kh + 40
    cols = ["Job"] + [str(c.get("label", "")) for c in spec.get("columns") or []]
    cells = [[b["id"]] + b["cells"] for b in body]
    y = d.grid_table(40, y, cols, [{"cells": c} for c in cells], widths_of(cols, cells, W - 80, 30), 30, pad=26)
    if spec.get("caption"):
        y = para(d, 40, y + 16, str(spec["caption"]), W - 80, 24)
    return finish(d, f, y)


def table_acts(d: Drawing, title: str, jobs: list[Path], all_rows: dict, words: dict, res: dict,
               assets: Path) -> tuple[list, list]:
    """One act per Job: ① its table (its steps, its reading, a row per Task with bars beside), ② its pictures; before
    them, for several Jobs, the family at a glance (a box per Job, then the Jobs as a table)."""
    each = words.get("each") or {}
    acts = []
    if len(jobs) > 1:
        row = [group_overview(d, title, jobs, all_rows, words, res)["id"]]
        if words.get("jobs_table"):
            row.append(jobs_frame(d, title, jobs, words["jobs_table"], all_rows)["id"])
        acts.append({"name": "Act 1 · the family at a glance", "frames": row, "arrow": ["side by side"]})
    for job in jobs:
        w = {**each, **(words.get(job.name) or {})}
        info = job_info(job)
        tf, body = table_frame(d, info, w, job, all_rows[job.name], assets)
        row, arrows = [tf["id"]], []
        if w.get("chart"):                                              # bars read from the Job's Runs, its words filled
            spec = {**w["chart"], **{k: fill(w["chart"][k], job) for k in ("title", "sub", "key", "caption")
                                     if w["chart"].get(k)}}
            cf = chart_frame(d, info, spec, job.parent, assets, f"{info['id']} ②")
            if cf:
                row.append(cf["id"])
                arrows.append("in a chart")
        ff = figures_frame(d, info, w, job, body, f"{'③' if len(row) > 1 else '②'}")
        if ff:
            row.append(ff["id"])
            arrows.append("in pictures")
        acts.append({"name": f"Act {len(acts) + 1} · {name_of(info)}", "frames": row, "arrow": arrows})
    between = [(a["frames"][0], b["frames"][0], "each Job" if i == 0 and len(jobs) > 1 else "next Job")
               for i, (a, b) in enumerate(zip(acts, acts[1:]))]
    return acts, between


# ── a family of Jobs in one topic (work/b03's s21-s25): an overview, then each Job explained from zero ───────
def group_cfg(face: Path) -> dict:
    """The face's `group:` yaml: per Job folder, the same words as a one-Job face's `job:` (intro, terms, inputs,
    outputs, formula, tasks, reading, sure, open)."""
    m = re.search(r"```yaml\s*\n(group:.*?)```", jr.read(face), re.S)
    if not (m and yaml):
        return {}
    try:
        return (yaml.safe_load(m.group(1)) or {}).get("group") or {}
    except Exception as err:
        print(f"{face.name}: its group: yaml does not read ({err})", file=sys.stderr)
        return {}


def group_overview(d: Drawing, title: str, jobs: list[Path], all_rows: dict, words: dict, res: dict) -> dict:
    """A family's first frame, a map: its key point, then one box per Job (its name, its Runs, what it concluded),
    three to a row at 28 px or more, joined to the key point as a tree; the conclusions shorten until ⑦'s words fit.
    Each Job's detail is its ③ frame below."""
    reading = res.get("reading") or {}
    key = str(reading.get("overview") or "").strip() or \
        f"{n_of(len(jobs), 'Job')}; each is explained from zero in its own frame below."
    start, per, gap = len(d.els), 3, 40
    for most, tell in ((200, 2), (140, 2), (140, 1), (100, 1), (70, 1), (45, 1), (0, 1), (0, 0)):
        del d.els[start:]                                    # the Runs' states go short before the conclusions do
        f = d.frame(f"⓪ {title}: every Job at a glance")
        y = jr.heading(d, title, "one box per Job: its Runs and what it concluded; each Job is explained from zero below")
        kh = jr.tall("🎯 " + key, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + key, W - 140, 30)
        above, y = (W / 2, y + kh), y + kh + 70
        boxes = []
        for job in jobs:
            runs = [r for t in all_rows[job.name] for r in t["runs"]]
            w = words.get(job.name) or {}                        # `gist`: the box's own short line, else the reading
            said = fill(w.get("gist") or w.get("reading") or reading.get(job.name) or "", job).strip()
            lines = ([f"{n_of(len(runs), 'Run')}: {states(runs)}" if tell == 2 else n_of(len(runs), "Run")]
                     if runs else ["⬜ no Run yet"]) if tell else []
            lines += [short(said, most)] if said and most else []
            name = str((res.get("labels") or {}).get(job.name) or jr.title_of(job))
            boxes.append((name if name.startswith(job.name[:3]) else f"{job.name[:3]} · {name}", lines))
        bw = (W - 80 - gap * (per - 1)) / per
        for k in range(0, len(boxes), per):
            row = boxes[k:k + per]
            hh = max(18 + jr.tall(t, bw - 40, 30) + 12 + sum(jr.tall(ln, bw - 40, 28) + 6 for ln in ls) + 16
                     for t, ls in row)
            mids = [40 + i * (bw + gap) + bw / 2 for i in range(len(row))]
            bus = y - 34                                     # the tree: from the key point (or the row above) to each Job
            d.line([(above[0], above[1] + 6), (above[0], bus)], sw=3)
            d.line([(min(mids + [above[0]]), bus), (max(mids + [above[0]]), bus)], sw=3)
            for m in mids:
                d.line([(m, bus), (m, y - 6)], sw=3)
            above = (mids[0], y + hh)
            for i, (t, ls) in enumerate(row):
                bx = 40 + i * (bw + gap)
                d.box(bx, y, bw, hh, INK, 2.5)
                yy = para(d, bx + 20, y + 18, t, bw - 40, 30) + 12
                for ln in ls:
                    yy = para(d, bx + 20, yy, ln, bw - 40, 28) + 6
            y += hh + 80
        if Drawing.words_small(d.els, f["id"])[0] <= MAP_BUDGET:
            break
    return finish(d, f, y - 80)


def draw_group(topic: Path) -> Path:
    """Redraw a family topic: job_results' overview (one row per Job, its numbers from disk), then one ③ frame per
    Job, three to a row; refresh the face's Runs ledger and the preview. The Jobs come from the face's results: yaml."""
    topic = topic.resolve()
    block = topic.parents[1]
    face = topic / f"{topic.name}.md"
    res = jr.results_yaml(face)
    jobs = [block / str(n) for n in (res.get("jobs") or []) if (block / str(n)).is_dir()]
    if not jobs:
        raise SystemExit(f"{face}: its results: yaml names no Job (results.jobs)")
    words = group_cfg(face)
    all_rows = {j.name: jr.job_rows(block, j, res) for j in jobs}
    topics = task_topics(block)
    title = re.sub(r"^s\d+\s*·\s*", "", jr.read(face).splitlines()[0])
    d = Drawing()
    if (words.get("each") or {}).get("table") or any((words.get(j.name) or {}).get("table") for j in jobs):
        acts, between = table_acts(d, title, jobs, all_rows, words, res, topic / "assets")   # a table per Job (261013)
        return finish_group(d, topic, face, acts, between, jobs, all_rows)
    ov = group_overview(d, title, jobs, all_rows, words, res)
    frames = []
    for job in jobs:
        w = dict(words.get(job.name) or {})
        w.setdefault("reading", ((res.get("reading") or {}).get(job.name) or ""))
        tasks = [task_info(r, res) for r in all_rows[job.name]]
        made = chart_frame(d, job_info(job), w["chart"], block, topic / "assets") if w.get("chart") else None
        if made is None and w.get("detail") is True:            # a text frame only when the face asks (261012)
            made = detail_frame(d, job_info(job), tasks, topics, w, topic / "assets")
        if made:
            frames.append(made["id"])
    acts = [{"name": "Act 1 · the family at a glance", "frames": [ov["id"]]}]
    for k in range(0, len(frames), 3):
        acts.append({"name": f"Act {len(acts) + 1} · what they found",
                     "frames": frames[k:k + 3], "arrow": "next Job"})
    between = [(ov["id"], frames[0], "each Job")] if frames else []
    between += [(acts[i]["frames"][0], acts[i + 1]["frames"][0], "next Jobs") for i in range(1, len(acts) - 1)]
    return finish_group(d, topic, face, acts, between, jobs, all_rows)


def finish_group(d: Drawing, topic: Path, face: Path, acts: list, between: list, jobs: list, all_rows: dict) -> Path:
    """Lay the acts out, write the drawing (a person's marks kept) and its preview, refresh the face's Runs ledger."""
    d.acts(acts, between=between, gap=700)
    out = topic / f"{topic.name}.excalidraw"
    d.write(out, f"excalidraw-job scripts/job_drawing.py group {topic.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    text = jr.read(face)
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        face.write_text(head + jr.ledger(topic, jobs, all_rows) + rest.split(END, 1)[1], encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make", help="the Block's topic for one Job, drawn")
    m.add_argument("job", type=Path)
    m.add_argument("--nn", type=int)
    m.add_argument("--dry-run", action="store_true")
    sub.add_parser("draw", help="redraw one Job topic").add_argument("topic", type=Path)
    a_ = sub.add_parser("adopt", help="a one-Job results topic, redrawn as the whole Job")
    a_.add_argument("topic", type=Path)
    a_.add_argument("--aim", default="")
    sub.add_parser("group", help="redraw a family topic: an overview, then each Job explained").add_argument(
        "topic", type=Path)
    p = sub.add_parser("preview", help="draw a Job anywhere; its Block is not touched")
    p.add_argument("job", type=Path)
    p.add_argument("out", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "make":
        print(make(a.job, a.nn, a.dry_run))
    elif a.cmd == "draw":
        print(draw(a.topic))
    elif a.cmd == "adopt":
        print(adopt(a.topic, a.aim))
    elif a.cmd == "group":
        print(draw_group(a.topic))
    else:
        print(draw_job(a.job, a.out.resolve())[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
