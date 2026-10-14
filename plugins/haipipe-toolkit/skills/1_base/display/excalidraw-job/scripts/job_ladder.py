"""A Job as a staircase: the Job on top, each Task a step lower and further right, its Runs branching from its step;
each Task's results, as charts or a table, in a small block outside the frame, level with its step.

Asked 261013 on Physician-SPACE's LLMRec Blocks, with a hand sketch (a Job, then T1, T2, T3 each a step lower and
further right, a "T1 Results" box beside each, outside the frame):
- "先是 Job，下面跟着 Task 1、Task 2、Task 3，再往下就是各种各样的 Run，相当于一个阶梯状的图 … 右边就开始说明每一个具体的结果
  都是什么" and "current ones in the job sNN are very bad".
- "这个 frame 可以很大，但核心是留出足够的空白，不要太挤、太 compact"; "T1、T2、T3 你可以决定什么时候往右边移一格 … 有的
  时候 T2、T3 和 T4 排成一列也是可以的"; "T1、T2、T3 这些 result 可以很小，大小有致".
- "你的 results 应该是图和表格呀 … 如果你有 Python 画的图，也一起扔过来".
- "主次分明 … 一个很大的 frame，然后有一些小的 frame 是解释这些大的 frame 的"; "不能把东西写太满 … 你可以是棋盘，但
  棋盘上不能落满所有的子"; "你不能每一个都是朝左对齐".
Its model is Tools' blueprints/b10_project_workbench s01 ladder (build_ladder_v4.py): each layer a step down and right.

    ① 🪜 the staircase (the main frame, large, room between the steps)
       🎯 the reading
       🧱 Job: why · done when · answers ──▶ 📥 in · 📤 out
        └─▶ 🧩 t01 · its step ─ r01 · r02 (grey names) · r04 📌 current ─────────────▶ 📊 t01: a sentence + charts
              └─▶ 🧩 t02 · its step ─ its Runs ───────────────────────────────────────▶ 📊 t02: …
       ❓ what is open: what would close each is in ②
        │ its words
        └──▶ ② 📖 words to know · how sure · what is open (small: canvas.explains), stepped right
               └──▶ ③ in detail: design grids, models, chart, settings, pictures, detail: true (when asked)

Every word and number is read from disk on every build: the Job face (goal, close, answers), each Task page, each
Run's receipt and result (the face's `show` picks; else a `summary.headline` its result writes; else what files it
holds). Each chart is drawn with matplotlib from the result file the face's `charts:` names, into the topic's
`assets/` (generated, never edited). The face's `job:` yaml adds only what no file says; see SKILL.md.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import job_drawing as jd  # noqa: E402

jr, Drawing, canvas = jd.jr, jd.Drawing, jd.canvas
INK, RED, GREY = jd.INK, jd.RED, jd.GREY

PAD, MOST = 22, 6                           # inside a box; Runs drawn per Task before the rest fold into one row
TERMS = 16                                  # terms drawn in ② before the rest are counted, never dropped
SHIFT, NODE_W, CARD_W, RUN_W = 380, 1200, 1080, 960   # a step right; a Task's box, its card, a Run's box: wide, so
                                                    #   each says itself in two or three lines (JL 261013)
JOB_W, IO_W = 1400, 1000                    # the Job's box; its in and out (wide like the steps, 261013)
STEP_GAP, RES_GAP = 170, 220                # room between steps; from the frame out to the results
RUN_WORDS = 280                             # the words every Run card (title + sentence) shares in ① (check.py ⑨: 600)
RUN_COLS, RUN_GAP = 3, 28                   # a Task's Runs as a grid, up to 3 a row (JL 261013: "make it wider")
CHART_W, NW = 800, 1200                     # a results chart on the canvas; the words frame (② , secondary)
THUMB_W, THUMB_H = 320, 400                 # a Task topic's thumbnail, right of its results (left to right, 261014)
PAGE_W, PAGE_H = 300, 420                   # each page of a Run's highlighted transcript, as stored (readable)
SHOT_W, SHOT_H, MAX_SHOTS = 240, 200, 4     # beside it, its video's screenshots, each with its caption
NAME_W = 280                                # a Run's original name, left of its row
STAGGER = 520                               # every other results block sits this much further right (错落有致)
CASCADE_DX = 140                            # each Run's row a step further right: free style, not a column (261014)
T_TITLE, T_JOB, T_STEP, T_CARD, T_RUNS, T_RES = 64, 46, 38, 28, 28, 28   # 大小有致: the logic large, details smaller
PICTURES = (".png", ".jpg", ".jpeg")
QUESTION = re.compile(r"^(which|what|how|why|who|when|where|does|do|is|are|can|should)\b", re.I)   # a title that asks


# ── words, read from disk ────────────────────────────────────────────────────────────────────────────────────
def words(s: str, most: int) -> str:
    w = str(s).split()
    return " ".join(w[:most]) + (" …" if len(w) > most else "")


def run_label(rid: str) -> str:
    """`r04_fold00_six_models_p12` → `r04 · fold00 six models p12`."""
    m = re.match(r"^(r\d+)_(.*)$", rid)
    return f"{m.group(1)} · {m.group(2).replace('_', ' ')}" if m else rid.replace("_", " ")


def headline(result: Path, most: int = 20) -> str:
    """What a Run's result says of itself in a sentence (`summary.headline`, `headline`, `reading`), if it does."""
    for name in ("metrics.json", "summary.json", "result.json", "metrics.yaml", "summary.yaml", "runtime.yaml"):
        data = jr.load(result / name) if result else None
        for key in ("summary.headline", "headline", "summary.text", "reading", "summary"):
            v = jr.dig(data, key) if data is not None else None
            if isinstance(v, str) and len(v.split()) >= 4:
                return words(v, most)
    return ""


def holds(result: Path) -> str:
    """What a result folder holds, by kind, when nothing in it names a number: `📂 metrics.json · 9 .csv`."""
    if not result or not result.is_dir():
        return ""
    files = [p for p in result.rglob("*") if p.is_file() and not p.name.startswith(".")]
    if not files:
        return ""
    named = [p.name for p in files if p.name in ("metrics.json", "summary.json", "report.md")]
    kinds = Counter(p.suffix.lower() or p.name for p in files if p.name not in named)
    return "📂 " + " · ".join(named + [f"{n} {k}" for k, n in kinds.most_common(4)])


def run_entry(cfg: dict, task: str, rid: str):
    own = cfg.get("runs") or {}
    return own.get(f"{task}/{rid}") or own.get(rid)


def run_current(cfg: dict, task: str, rid: str) -> bool:
    """The face marks the Run a reader should read (`runs.<tNN_task>/<rNN_run>: {current: true}`)."""
    v = run_entry(cfg, task, rid)
    return isinstance(v, dict) and bool(v.get("current"))


def run_says(cfg: dict, task: str, rid: str) -> str:
    """The face's one sentence for a Run: what it is and what makes it differ (`says`), or a plain string."""
    v = run_entry(cfg, task, rid)
    return str((v.get("says") or v.get("found")) if isinstance(v, dict) else (v or ""))


def tells(r: dict, cfg: dict, task: str) -> bool:
    """A Run with something to report: numbers, a sentence, or files in its result."""
    return bool(r["values"] or run_says(cfg, task, r["name"]) or headline(r["result"]) or holds(r["result"]))


def shown_runs(t: dict, cfg: dict) -> tuple[list[dict], list[dict]]:
    """The Runs drawn as rows, and the rest folded into one row: a Run with nothing to report never takes a row of
    its own (b02 j05: 80 Runs whose results live outside the repository); past MOST, the 📌 current Runs always, then
    the latest that report (a current Run never folds away: found by the b03 s21 trial, 261013)."""
    now = [r for r in t["runs"] if run_current(cfg, t["name"], r["name"])]
    says = [r for r in t["runs"] if tells(r, cfg, t["name"]) and r not in now]
    room = max(MOST - 1 - len(now), 0)
    chosen = now + (says[-room:] if len(says) + len(now) > MOST and room else [] if len(says) + len(now) > MOST else says)
    keep = [r for r in t["runs"] if r in chosen]                       # in the Task's own order
    return keep, [r for r in t["runs"] if r not in keep]


def did_of(t: dict, cfg: dict) -> str:
    did = str(((cfg.get("tasks") or {}).get(t["name"]) or {}).get("did") or "")
    return re.sub(r"\s*Detail Page:.*$", "", did).strip()


def columns(n: int) -> list[int]:
    """The column each Task's step stands in: one step right per Task, up to four columns; past four Tasks, a few
    share a column ("有的时候 T2、T3 和 T4 排成一列也是可以的"), so the stairs stay staggered on one screen's width."""
    c = min(n, 4)
    return [i * c // n for i in range(n)] if n else []


def run_cols(n: int) -> int:
    """How many Runs stand side by side: one alone, two up to four, then RUN_COLS; a Task of six Runs is two rows,
    not a column six cards tall (JL 261013 on j01: "I don't want to make it very tall and narrow")."""
    return 1 if n <= 1 else 2 if n <= 4 else RUN_COLS


# ── a step that stands for a family of Tasks (asked 261014 on a 33-Task raw-data Job, drawn 14,780 px tall: "if
# possible, let's still be the steps / stairs"): a big Job keeps its staircase when one step holds several Tasks of
# one stage, lists them inside it, folds their Runs by what they do, and shows one result per Task outside ──────────
FAMILY_MIN, BIG_JOB = 3, 8                  # a family: 3 Tasks or more of one kind; grouped unasked past 8 Tasks
ADDRESS = re.compile(r"^\s*B\d+/J\d+/T\d+\s*[·:.\-]?\s*", re.I)     # "B00/J51/T14 · …": a page title's address


def bare(title: str) -> str:
    """A Task's title without the address its page may lead with: the drawing already says its id."""
    return ADDRESS.sub("", str(title))


def task_ids(spec, tasks: list[dict]) -> list[str]:
    """The Task ids a face step names: ids or folder names, or a range `t11-t13`."""
    out = []
    for it in spec if isinstance(spec, list) else [spec]:
        m = re.fullmatch(r"(t\d+)\s*[-–]\s*(t\d+)", str(it).strip())
        if m:
            lo, hi = int(m.group(1)[1:]), int(m.group(2)[1:])
            out += [t["id"] for t in tasks if lo <= int(t["id"][1:]) <= hi]
        else:
            out += [t["id"] for t in tasks if str(it) in (t["id"], t["name"])]
    return out


def kind_of(t: dict) -> str:
    """A Task's kind: the first word of its folder name after tNN_ (`t14_profile_signal_…` is a profile)."""
    return t["name"].split("_")[1] if t["name"].count("_") else ""


def family(members: list[dict], title: str, key: str, asked: str = "") -> dict:
    """One step for several Tasks: their Runs together, the Job's folder as its own, the question they share."""
    first, last = members[0], members[-1]
    qs = {m.get("question") or "" for m in members}
    return {**first, "id": f"{first['id']}–{last['id']}", "name": key, "title": title, "members": members,
            "runs": [r for m in members for r in m["runs"]], "row": {**first["row"], "task": first["row"]["task"].parent},
            "question": asked or (qs.pop() if len(qs) == 1 else ""), "lab": {}}


def step_groups(tasks: list[dict], cfg: dict) -> list[dict]:
    """The staircase's steps. The face's `steps: [{title, tasks: [t11-t13] or [t14, t15], key, asked}]` makes each
    a step in the place of its first Task; with none, past BIG_JOB Tasks, each run of FAMILY_MIN or more Tasks of one
    kind is one step. Every other Task is its own step."""
    named = cfg.get("steps") or []
    if named:
        at, seen = {}, set()
        for s in named:
            ms = [t for t in tasks if t["id"] in task_ids(s.get("tasks") or [], tasks) and t["id"] not in seen]
            if not ms:
                continue
            seen |= {t["id"] for t in ms}
            at[ms[0]["id"]] = ms[0] if len(ms) == 1 else \
                family(ms, str(s.get("title") or f"{kind_of(ms[0])} · {len(ms)} Tasks"),
                       str(s.get("key") or f"{ms[0]['id']}-{ms[-1]['id']}"), str(s.get("asked") or ""))
        return [at.get(t["id"], t) for t in tasks if t["id"] in at or t["id"] not in seen]
    if len(tasks) <= BIG_JOB:
        return tasks
    out, i = [], 0
    while i < len(tasks):
        j = i
        while j + 1 < len(tasks) and kind_of(tasks[i]) and kind_of(tasks[j + 1]) == kind_of(tasks[i]):
            j += 1
        ms = tasks[i:j + 1]
        out += [family(ms, f"{kind_of(ms[0])} · {len(ms)} Tasks", f"{ms[0]['id']}-{ms[-1]['id']}")] \
            if len(ms) >= FAMILY_MIN else ms
        i = j + 1
    return out


SPLIT_AT = 6                                # past this many steps, a Job is drawn as two staircases


def split_steps(steps: list[dict], cfg: dict) -> list[tuple[str, list[dict]]]:
    """A Job too large for one staircase is drawn as two, the second continuing the first (asked 261014: "if the
    job is too large, in the sNN jNN, you can have two frames to arrange that"): where the face's `parts: [{title},
    {title, from: t91}]` says, else past SPLIT_AT steps at the middle step. Each is named by what it holds, never
    "· 1", "· 2"."""
    parts = cfg.get("parts") or []
    if len(parts) >= 2 and parts[1].get("from"):
        at = next((i for i, s in enumerate(steps) if s["id"].split("–")[0] == str(parts[1]["from"])
                   or s["name"] == str(parts[1]["from"])), None)
        if at:
            return [(str(parts[0].get("title") or ""), steps[:at]), (str(parts[1].get("title") or ""), steps[at:])]
    if len(steps) <= SPLIT_AT:
        return [("", steps)]
    h = (len(steps) + 1) // 2
    name = lambda ss: f"its Tasks {ss[0]['id'].split('–')[0]} to {ss[-1]['id'].split('–')[-1]}"
    return [(name(steps[:h]), steps[:h]), (name(steps[h:]), steps[h:])]


def member_mark(m: dict) -> str:
    """A Task in a family, by its Runs: ✅ when every Run is, else the first Run's mark that is not; ⬜ with none."""
    marks = [r["mark"] for r in m["runs"]]
    return "⬜" if not marks else next((k for k in marks if k != "✅"), "✅")


def member_value(m: dict, cfg: dict, spec: dict, at: str):
    """One value from a family member's Run (`spec.run`, else its current or last Run with a result)."""
    result = chart_run(m, cfg, spec)
    data = jr.load(result / spec.get("file", "metrics.json")) if result else None
    return jr.dig(data, at) if data is not None and at else None


def member_label(m: dict, cfg: dict, spec: dict) -> str:
    """A member's row name: the value `spec.label` reads from its Run, else its title without its kind word."""
    lab = member_value(m, cfg, spec, str(spec.get("label") or ""))
    return str(lab) if lab not in (None, "") else re.sub(rf"^{kind_of(m)}\s+", "", bare(m["title"]), flags=re.I)


def member_rows(t: dict, cfg: dict, spec: dict) -> list[tuple]:
    """A family's chart: one bar per member, `value` read from each member's own Run (`members: true`)."""
    rows = [(member_label(m, cfg, spec), member_value(m, cfg, spec, str(spec.get("value") or "")), None, None)
            for m in t["members"]]
    rows = [r for r in rows if isinstance(r[1], (int, float)) and not isinstance(r[1], bool)]
    return sorted(rows, key=lambda r: -r[1]) if spec.get("sort", True) else rows


def family_step(d: Drawing, nx: float, y: float, t: dict, cfg: dict, spine_x: float) -> tuple[dict, float]:
    """A family's step: its box, the question each member asks, the members two a row with their marks, and their
    Runs folded by what they do (`r02 · profile semantics × 28`). Returns the step and the next step's y."""
    nh = card(d, nx, y, NODE_W, [(f"🧩 {t['id']} · {t['title']}", T_STEP, INK)], sw=2.5)
    asked = ((cfg.get("tasks") or {}).get(t["name"]) or {}).get("asked") or t.get("question") or ""
    did = did_of(t, cfg)
    head = [(f"Asks, of each: {words(asked, 24)}" if asked else "", T_CARD, INK),
            (f"Did: {words(did, 24)}" if did else "", T_CARD, INK)]
    chips = [f"{member_mark(m)} {m['id']} · "
             f"{jd.short(re.sub(rf'^{kind_of(m)}[ _]+', '', bare(m['title']), flags=re.I), 34)}" for m in t["members"]]
    half = (len(chips) + 1) // 2
    cx, cy, cw = nx + 36, y + nh + 16, (CARD_W - 2 * PAD) / 2
    yy = cy + PAD
    for s, size, color in head:
        if s:
            yy = d.para(cx + PAD, yy, s, CARD_W - 2 * PAD, size, color) + 6
    yy += 4
    low = yy
    for k, col in enumerate((chips[:half], chips[half:])):            # one line each, two columns
        cy2 = yy
        for chip in col:
            cy2 = d.para(cx + PAD + k * cw, cy2, chip, cw - 12, T_RUNS - 2, INK) + 4
        low = max(low, cy2)
    cardh = low - cy + PAD
    d.box(cx, cy, CARD_W, cardh, INK, 1.2)
    folds = {}
    for m in t["members"]:
        for r in m["runs"]:
            folds.setdefault(run_label(r["name"]), []).append(r)
    rx, ry, mids = nx + NODE_W + 110, y + nh + 24, []
    boxes = [([(f"{name} × {len(rs)}", T_RUNS, INK),
               (" · ".join(f"{n} {s}" for s, n in Counter(f"{r['mark']} {r['state']}" for r in rs).most_common()),
                T_RUNS, GREY)], RUN_W, 1.5, False) for name, rs in folds.items()]
    per = run_cols(len(boxes))
    for i in range(0, len(boxes), per):
        row = boxes[i:i + per]
        row_h = max(lines_h(lines, w) for lines, w, _, _ in row)
        for k, (lines, w, sw, dashed) in enumerate(row):
            card(d, rx + k * (RUN_W + RUN_GAP), ry, w, lines, dashed=dashed, sw=sw)
        mids.append(ry + 30)
        ry += row_h + 18
    if mids:
        bx = nx + NODE_W - 60
        d.line([(bx, y + nh), (bx, mids[-1])], arrow=False, sw=1.5)
        for m in mids:
            d.line([(bx, m), (rx - 8, m)], sw=1.5)
    mid = y + nh / 2
    d.line([(spine_x, mid), (nx - 8, mid)], sw=3)
    step = {"y": y, "mid": mid, "right": nx + NODE_W, "task": t, "found": jd.finding(t, cfg), "thumb": None}
    return step, max(y + nh + 16 + cardh + 16, ry) + STEP_GAP


# ── boxes ────────────────────────────────────────────────────────────────────────────────────────────────────
def lines_h(lines: list, w: float) -> float:
    return sum(Drawing.height(s, w - 2 * PAD, size) + 6 for s, size, _ in lines if s) + 2 * PAD - 6


def card(d: Drawing, x: float, y: float, w: float, lines: list, dashed: bool = False, sw: float = 1.5) -> float:
    """A box of lines [(words, size, colour)]; returns its height."""
    h = lines_h(lines, w)
    d.box(x, y, w, h, GREY if dashed else INK, sw, dashed=dashed)
    yy = y + PAD
    for s, size, color in lines:
        if s:
            yy = d.para(x + PAD, yy, s, w - 2 * PAD, size, color) + 6
    return h


# ── results as charts and tables, not words ──────────────────────────────────────────────────────────────────
def short_key(k: str) -> str:
    """A model folder name, short: `claude-claude-haiku-4-5-20251001` → `claude-haiku-4-5`; `a_tag` → `a tag`."""
    parts = re.sub(r"-\d{8}$", "", str(k)).split("-")
    if len(parts) > 1 and parts[0] == parts[1]:
        parts = parts[1:]
    return "-".join(parts).replace("-harness", "").replace("_", " ")


def chart_run(t: dict, cfg: dict, spec: dict) -> Path | None:
    """The result folder a chart reads: its `run`, else the Task's current Run, else its last Run with a result."""
    runs = t["runs"]
    pick = [r for r in runs if r["name"] == spec.get("run")] or \
           [r for r in runs if run_current(cfg, t["name"], r["name"])] or [r for r in runs if r["result"].is_dir()]
    return pick[-1]["result"] if pick else None


def chart_rows(spec: dict, result: Path) -> list[tuple]:
    """(label, value, low, high) per bar: `bars: [{label, at, low, high}]` (a CSV's row by `col=v&col2=v.estimate`,
    its interval by `….ci_lo`, `….ci_hi`: OpioidRx's Stata tables, 261013), or `each: <key>` (a mapping: a bar per
    entry) with `value`, `low`, `high` read inside each entry; `labels:` renames an entry; largest first unless
    `sort: false`."""
    if "_rows" in spec:                                                 # a family's bars, one per member Task
        return spec["_rows"]
    data = jr.load(result / spec.get("file", "metrics.json"))
    if spec.get("bars"):
        rows = [(str(b.get("label", b["at"])), jr.dig(data, b["at"]),
                 jr.dig(data, b["low"]) if b.get("low") else None,
                 jr.dig(data, b["high"]) if b.get("high") else None) for b in spec["bars"]]
    else:
        each = jr.dig(data, spec.get("each", "")) or {}
        names = spec.get("labels") or {}
        rows = []
        for k, v in (each.items() if isinstance(each, dict) else []):
            val = jr.dig(v, spec["value"]) if spec.get("value") else v
            lo = jr.dig(v, spec["low"]) if spec.get("low") else None
            hi = jr.dig(v, spec["high"]) if spec.get("high") else None
            rows.append((names.get(k) or short_key(k), val, lo, hi))
    rows = [r for r in rows if isinstance(r[1], (int, float)) and not isinstance(r[1], bool)]
    return sorted(rows, key=lambda r: -r[1]) if spec.get("sort", True) else rows


def chart_png(spec: dict, result: Path | None, out: Path) -> Path | None:
    """One series as horizontal bars (the dataviz skill: magnitude by category; one series, so no legend and the
    title names it): dark bars, thin 95% whiskers when `low`/`high` are given, a zero line when a value is negative,
    a value at each bar's end (a handful of bars), quiet axes. None when the result holds no values for it."""
    rows = chart_rows(spec, result) if result else []
    if not rows:
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pct = spec.get("fmt") == "pct"
    k = 100 if pct else 1
    digits = int(spec.get("digits", 1 if pct else (0 if spec.get("fmt") == "int" else 3)))
    big = not pct and max(abs(r[1]) for r in rows) >= 1e6              # 113.2M, not 113,219,741 run off the edge;
    short = (lambda v: f"{v / 1e6:,.1f}M" if abs(v) >= 1e6 else       # each bar its own unit, so 226,893 and
             f"{v / 1e3:,.0f}K" if abs(v) >= 1e4 else f"{v:,.{digits}f}")   # 222,433 stay apart (227K, 222K)
    show = (lambda v: f"{v:.{digits}f}%") if pct else short if big else (lambda v: f"{v:,.{digits}f}")
    n = len(rows)
    fig, ax = plt.subplots(figsize=(9, 0.62 * n + 0.9), dpi=100)
    ys = list(range(n))[::-1]
    vals = [r[1] * k for r in rows]
    ax.barh(ys, vals, height=0.56, color="#3b3b3b")
    ends = []
    for y, (_, v, lo, hi) in zip(ys, rows):
        if lo is not None and hi is not None:
            ax.errorbar(v * k, y, xerr=[[v * k - lo * k], [hi * k - v * k]], fmt="none", ecolor="#1e1e1e",
                        elinewidth=2, capsize=6)
        ends.append(max(v, hi if hi is not None else v) * k)
    lows = [min(0, r[1], r[2] if r[2] is not None else r[1]) * k for r in rows]
    span = max(ends + [0]) - min(lows + [0]) or 1
    for y, e, v in zip(ys, ends, vals):
        ax.text(max(e, 0) + span * 0.02, y, show(v), va="center", fontsize=22, color="#1e1e1e")
    if min(lows) < 0:
        ax.axvline(0, color="#1e1e1e", linewidth=1.2)
    ax.set_xlim(min(lows) - span * 0.05 if min(lows) < 0 else 0, max(ends + [0]) + span * 0.28)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=22, color="#1e1e1e")
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))                   # a few ticks, never run together
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%" if pct else f"{v / 1e6:g}M" if big else
                                               f"{v:,.0f}" if abs(v) >= 100 else f"{v:g}"))
    ax.tick_params(axis="x", labelsize=16, colors="#868e96")
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#adb5bd")
    ax.grid(axis="x", color="#e9ecef", linewidth=1)
    ax.set_axisbelow(True)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=100)
    plt.close(fig)
    return out


def task_pictures(t: dict, cfg: dict) -> list[Path]:
    """The figures a Task already holds (JL 261013: "for the task, we might want to add the figures and table from
    it"): the face's `figures: {<tNN_task>: [globs under the Task]}`, else the pictures in its Runs' results (the
    current Run's first), then in its draft's display units; two unless the face names more."""
    folder = t["row"]["task"]
    named = ((cfg.get("figures") or {}).get(t["name"]))
    if named:
        return [p for g in named for p in sorted(folder.glob(str(g))) if p.suffix.lower() in PICTURES]
    now = [r["result"] for r in t["runs"] if run_current(cfg, t["name"], r["name"])]
    found = []
    for base in now + [r["result"] for r in reversed(t["runs"])] + [folder / "draft"]:
        if base.is_dir():
            for p in sorted(base.rglob("*")):
                parts = p.relative_to(folder).parts[:-1]
                if p.suffix.lower() in PICTURES and p not in found and \
                        not any(q.startswith((".", "_")) or q in ("studio", "history", "read", "shots") for q in parts):
                    # read/ and shots/ are a video Run's transcript pages and screenshots, drawn beside it (261014)
                    found.append(p)
    return found[:2]


def task_tables(t: dict, cfg: dict) -> list[tuple[str, list[str], list[dict]]]:
    """The tables the face names from a Task's Run (`tables: {<tNN_task>: [{title, file, columns, rows, sort, run}]}`):
    a CSV under the Run's result, its named columns, its first `rows` rows (6), sorted by `sort` (`-col`: largest
    first), only the rows `where` picks (`col=v&col2=v`, as a chart's row selector: one model of a Stata table that
    holds several, OpioidRx 261013). Returns (title, columns, rows) each, read on every build."""
    out = []
    for spec in ((cfg.get("tables") or {}).get(t["name"]) or [])[:2]:
        if spec.get("members") and t.get("members"):                    # a family: a row per member Task, each
            cols = spec.get("columns") or []                            #   cell read from that Task's own Run
            out.append((str(spec.get("title", spec.get("file", ""))),
                        [str(spec.get("first", "Task"))] + [str(c.get("label", c.get("at"))) for c in cols],
                        [{"cells": [member_label(m, cfg, spec)] +
                          [jr.number(member_value(m, cfg, spec, str(c.get("at"))), str(c.get("fmt", ""))) for c in cols],
                          "dim": False} for m in t["members"]]))
            continue
        result = chart_run(t, cfg, spec)
        data = jr.load(result / spec["file"]) if result else None
        if isinstance(data, list) and spec.get("where"):
            want = dict(c.split("=", 1) for c in str(spec["where"]).split("&"))
            data = [r for r in data if isinstance(r, dict) and all(str(r.get(k)) == v for k, v in want.items())]
        if not isinstance(data, list) or not data:
            out.append((f"❓ table {spec.get('title', spec.get('file'))}: not in the result", [], []))
            continue
        cols = spec.get("columns") or list(data[0])[:4]
        key = str(spec.get("sort") or "")
        if key:
            data = sorted(data, key=lambda r: (r.get(key.lstrip("-")) is None, r.get(key.lstrip("-"))),
                          reverse=key.startswith("-"))
        names = spec.get("labels") or {}
        shown = [{"cells": [names.get(str(r.get(c)), short_key(r.get(c))) if i == 0 else jr.number(r.get(c), spec.get("fmt", ""))
                            for i, c in enumerate(cols)], "dim": False} for r in data[:int(spec.get("rows", 6))]]
        out.append((str(spec.get("title", spec["file"])), [str(c).replace("_", " ") for c in cols], shown))
    return out


def run_pages(topic: Path | None, t: dict) -> list[dict]:
    """Each Run's highlighted transcript, every page, and its video's screenshots with their captions, in the Task's
    Run order. Read from the Run's own result/ first (read/p<N>.jpg; shots/shots.yaml naming shots/t<sec>.jpg, as
    job_level3.py's carry writes them), so a Job draws its Tasks' results with no Task topic (JL 261014: "we will
    retire the sNN tNN"); else from the Task's topic while one is kept (assets/<rid>-transcript-p<N>.jpg, its
    face's videos.<rid>.shots, assets/<rid>-t<sec>.jpg)."""
    import yaml
    vids = {}
    if topic:
        try:
            m = re.search(r"```yaml\s*\n(task:.*?)```", (topic / f"{topic.name}.md").read_text(), re.S)
            vids = {str(k)[:3]: v or {} for k, v in
                    ((yaml.safe_load(m.group(1)) or {}).get("task", {}).get("videos") or {}).items()}
        except (OSError, AttributeError, yaml.YAMLError):
            vids = {}
    out = []
    for r in t["runs"]:
        rid, res = r["name"][:3], (Path(r["result"]) if r.get("result") else None)
        pages = sorted((res / "read").glob("p*.jpg"), key=lambda q: int(re.sub(r"\D", "", q.stem) or 0)) \
            if res and (res / "read").is_dir() else []
        shots = []
        if res and (res / "shots" / "shots.yaml").is_file():
            for sh in yaml.safe_load((res / "shots" / "shots.yaml").read_text()) or []:
                f = res / "shots" / str((sh or {}).get("file", ""))
                if f.is_file():
                    shots.append((f, str(sh.get("says") or "")))
        a = topic / "assets" if topic else None
        if a and not pages:
            pages = sorted(a.glob(f"{rid}-transcript-p*.jpg"), key=lambda q: int(re.search(r"-p(\d+)", q.name).group(1)))
        if a and not shots:
            for sh in (vids.get(rid) or {}).get("shots") or []:
                f = a / f"{rid}-t{int(sh.get('at', 0)):04d}.jpg" if isinstance(sh, dict) else None
                if f and f.is_file():
                    shots.append((f, str(sh.get("says") or "")))
        if pages:
            out.append({"rid": rid, "title": run_title(r), "pages": pages,   # every page: the whole transcript
                        "shots": shots[:MAX_SHOTS]})
    return out


def run_title(r: dict) -> str:
    """A Run's original name: its Result Card's title, a video's own title as filed (JL 261014: "show what is the
    original name for this run"); empty when the card's title is only the Run's id."""
    res = Path(r["result"]) if r.get("result") else None
    try:
        first = next(ln for ln in (res / f"{r['name']}.md").read_text().splitlines() if ln.startswith("# "))[2:].strip()
    except (OSError, StopIteration, TypeError):
        return ""
    return "" if first.lower().startswith((r["name"][:3].lower(), r["name"].lower())) else first


def clip(s: str, most: int) -> str:
    """At most `most` characters (a title may be Chinese, with no spaces to cut at)."""
    s = str(s).strip()
    return s if len(s) <= most else s[:most].rstrip() + "…"


def embed_page(d: Drawing, path: Path, x: float, y: float, w: float, fid: str, link: str | None) -> float:
    """A transcript page as stored (96 dpi, already small), not shrunk again, so its words read when zoomed
    (JL 261014: "could you make it a bit more readable?"). Returns its height."""
    import base64
    from PIL import Image
    with Image.open(path) as im:
        h = w * im.height / im.width
    d.files[fid] = {"mimeType": "image/jpeg", "id": fid, "created": 1,
                    "dataURL": "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()}
    d.box(x - 2, y - 2, w + 4, h + 4, GREY, 1)
    d.el("image", x, y, w, h, fileId=fid, status="saved", scale=[1, 1])
    if link:
        d.els[-1]["link"] = link
    return h


def results_block(d: Drawing, x: float, y: float, t: dict, cfg: dict, found: str,
                  assets: Path | None, thumb: tuple | None = None) -> tuple[float, bool]:
    """A Task's results, outside the frame, in this order: a small title; its finding in one sentence; the charts the
    face names (`charts:`, drawn here from its Run's result); the figures the Task holds (task_pictures: a figure
    Run's charts, JL 261013); the tables it names (`tables:`, rows from its Run's CSV); else its current Run's
    picked numbers as a table.
    Returns (height, open): open, dashed, when it shows none of these."""
    nn, png, link, pages = thumb or (None, None, None, [])
    row = max((NAME_W + 16 + len(g["pages"]) * (PAGE_W + 10) + (16 + len(g["shots"]) * (SHOT_W + 12) if g["shots"] else 0)
               for g in pages), default=0)
    right = (len(pages) - 1) * CASCADE_DX + row if pages else 0
    w = CHART_W + 2 * PAD + (right + 28 if right else 0)
    yy = d.para(x + PAD, y + PAD, f"📊 {t['id']} results", w - 2 * PAD, T_RES - 4, GREY) + 4
    side = yy
    if right:                                       # to the right of the results, so a block grows wide, not tall
        tx = x + PAD + CHART_W + 28                 # (JL 261014: "the results of the png can be from left to right")
        if pages:                                   # a Run a row, each a step further right: its transcript page,
            gy = side                               # then its screenshots with their captions (JL 261014)
            for k, g in enumerate(pages):
                gx = tx + k * CASCADE_DX
                low = d.para(gx, gy, f"{g['rid']} · {g['title']}" if g["title"] else g["rid"], NAME_W, T_RES - 4, INK)
                px = gx + NAME_W + 16                                  # its original name first, then its pages
                for n, page in enumerate(g["pages"], 1):           # the whole transcript, page by page
                    h = embed_page(d, page, px, gy, PAGE_W, f"page-{nn}-{g['rid']}-p{n}", None)
                    low = max(low, d.para(px, gy + h + 6, f"{g['rid']} · p{n}", PAGE_W, T_RES - 8, GREY))
                    px += PAGE_W + 10
                sx = px + 6
                for j, (shot, cap) in enumerate(g["shots"]):
                    sh = d.picture(shot, sx, gy, SHOT_W, SHOT_H, fid=f"shot-{nn}-{g['rid']}-{j}")
                    low = max(low, d.para(sx, gy + sh + 6, words(cap, 12), SHOT_W, 18, GREY))
                    sx += SHOT_W + 12
                gy = low + 40
            side = gy - 36
    if found:
        first = re.split(r"(?<=[.!?])\s+", str(found).strip())[0]      # one sentence; the charts carry the numbers
        yy = d.para(x + PAD, yy, f"💡 {words(first, 18)}", CHART_W, T_RES, INK) + 14
    drawn = 0
    for k, spec in enumerate(((cfg.get("charts") or {}).get(t["name"]) or [])[:3]):
        if spec.get("members") and t.get("members"):                    # a family: a bar per member Task
            spec = {**spec, "_rows": member_rows(t, cfg, spec)}
        src = t["row"]["task"] if "_rows" in spec else chart_run(t, cfg, spec)
        png = chart_png(spec, src, assets / f"chart-{t['name']}-{k}.png") if assets else None
        if not png:
            yy = d.para(x + PAD, yy, f"❓ chart {spec.get('title', k)}: no values in its result", CHART_W,
                        T_RES - 2, RED) + 8
            continue
        yy = d.para(x + PAD, yy, str(spec.get("title", "")), CHART_W, T_RES, INK) + 4
        yy += d.picture(png, x + PAD, yy, CHART_W, 900, fid=f"chart-{t['name']}-{k}") + 16
        drawn += 1
    charted = drawn
    for k, p in enumerate(task_pictures(t, cfg)):                       # its own figures, as its Runs drew them:
        yy += d.picture(p, x + PAD, yy, CHART_W, 640, fid=f"fig-{t['name']}-{k}") + 6   # a figure Run's charts
        yy = d.para(x + PAD, yy, str(p.relative_to(t["row"]["task"])), CHART_W, 20, GREY) + 16   # come first
        drawn += 1                                                      # (JL 261013), then the exact rows
    tabled = False
    for title, cols, rows in task_tables(t, cfg):                       # its tables, from its Run's own files
        if not rows:
            yy = d.para(x + PAD, yy, title, CHART_W, T_RES - 2, RED) + 8
            continue
        yy = d.para(x + PAD, yy, title, CHART_W, T_RES, INK) + 4
        first = CHART_W * 0.46
        rest = (CHART_W - first) / max(1, len(cols) - 1)
        yy = d.grid_table(x + PAD, yy, cols, rows, [first] + [rest] * (len(cols) - 1), 24, pad=20) + 16
        tabled = True
    if not charted and not tabled:
        now = [r for r in t["runs"] if run_current(cfg, t["name"], r["name"])]
        vals = [v for r in (now or [r for r in t["runs"] if r["values"]][-1:]) for v in r["values"]]
        if vals:                                                       # no chart or table named: its numbers, a table
            rows = [{"cells": list(v.rsplit(" ", 1)) if " " in v else [v, ""], "dim": False} for v in vals]
            yy = d.grid_table(x + PAD, yy, ["", ""], rows, [CHART_W * 0.62, CHART_W * 0.38], T_RES, pad=24) + 10
            tabled = True
    is_open = not (found or drawn or tabled)
    if is_open:
        yy = d.para(x + PAD, yy, "❓ nothing found yet" if t["runs"] else "⬜ no Run yet", CHART_W, T_RES,
                    RED if t["runs"] else GREY) + 8
    h = max(yy, side) - y + PAD - 8                                    # the taller of the two columns
    d.box(x, y, w, h, GREY if is_open else INK, 1.5, dashed=is_open)
    return h, is_open


# ── ① the staircase, the main frame ──────────────────────────────────────────────────────────────────────────
def ladder_frame(d: Drawing, info: dict, tasks: list[dict], cfg: dict, topics: dict | None = None,
                 mark: str = "①", assets: Path | None = None, part: str = "", cont: bool = False,
                 last: bool = True, grouped: bool = False) -> dict:
    """The Job as a staircase: the Job at the top, each Task a step lower and further right, its Runs branching to
    its right; each Task's results in a small block outside the frame, level with its step."""
    tasks = tasks if grouped else step_groups(tasks, cfg)               # a family of Tasks stands as one step
    n_runs = sum(len(t["runs"]) for t in tasks)
    tight = len(tasks) > 6 or sum(len(shown_runs(t, cfg)[0]) for t in tasks) > 14   # a big Job: fewer words a step
    shown = sum(len(shown_runs(t, cfg)[0]) for t in tasks)
    say_most = max(8, min(26, RUN_WORDS // max(1, shown)))      # every Job: its Run cards share one budget (261014)
    cols = columns(len(tasks))
    grid = max((run_cols(len(k) + bool(fo)) for k, fo in (shown_runs(t, cfg) for t in tasks)), default=1)
    runs_w = grid * RUN_W + (grid - 1) * RUN_GAP
    width = max(130 + max(cols, default=0) * SHIFT + NODE_W + 110 + runs_w + 60, 40 + JOB_W + 120 + IO_W + 60)
    title = f"🪜 {info['id']} · {part if cont and part else info['title']}"   # a second staircase: what it holds
    f = d.frame(f"{mark} {title}: " + ("its Tasks as steps, continued" if cont else "why it exists, its Tasks as steps"),
                width)
    Drawing.room(f)                         # the room between the steps is the point; measured over the boxes
    if width > canvas.FRAME_MAX[0]:
        canvas.large(f)
    d.text(40, 22, title, T_TITLE)
    sub = f"{info.get('block') or ''} · {jd.n_of(len(tasks), 'Task')} · {jd.n_of(n_runs, 'Run')}: " \
          f"{jd.states([r for t in tasks for r in t['runs']])}"
    d.para(40, 112, sub.strip(" ·"), width - 80, T_RUNS, GREY)
    if cont:                                                            # the staircase continued: no Job box
        spine_x, spine_top, most_open = 60, 180, 3                    #   again, its spine starts at the top
        y = 240
    else:
        y = 180
        reading = str(cfg.get("reading") or "")
        key = f"🎯 {reading}" if reading else "❓ no reading yet: write the face's job.reading (what this Job found)"
        kh = Drawing.height(key, width - 140, 34) + 44
        d.key(40, y, width - 80, kh)
        d.para(70, y + 22, key, width - 140, 34)
        y += kh + 80

        # the top step: the Job, why it exists and when it is done; what goes in and comes out branch to its right
        aim = str(cfg.get("aim") or info.get("goal") or "")
        jh = card(d, 40, y, JOB_W, [(f"🧱 {info['id']} · {info['title']}", T_JOB, INK)], sw=3)
        why = [(f"Why: {words(aim, 40)}" if aim else "❓ no aim: the Job face has no goal: line", T_CARD, None),
               (f"Done when: {words(info['close'], 34)}" if info.get("close") else   # 22 cut its end in four
                                                                                     # OpioidRx reviews (261013)
                "❓ close: not written on the Job face", T_CARD, None),
               (f"Answers: {info['answers']}" if info.get("answers") else "", T_CARD, INK)]
        ch = card(d, 110, y + jh + 20, JOB_W - 110, why)
        most_io, io_words, most_open = (2, 10, 3) if tight else (3, 14, 4)
        io_x, yy = 40 + JOB_W + 120, y
        for label, items in (("📥 In", (cfg.get("inputs") or [])[:most_io]), ("📤 Out", (cfg.get("outputs") or [])[:most_io])):
            if items:
                h = card(d, io_x, yy, IO_W, [(label, T_STEP - 6, INK)] + [(f"· {words(x, io_words)}", T_RUNS, INK) for x in items])
                d.line([(40 + JOB_W + 12, y + jh / 2), (io_x - 12, yy + 32)], sw=2)
                yy += h + 24
        spine_x, spine_top = 60, y + jh
        y = max(y + jh + 20 + ch, yy) + STEP_GAP

    steps = []
    for t, col in zip(tasks, cols):
        nx = 130 + col * SHIFT
        if t.get("members"):                                            # one step for a family of Tasks
            step, y = family_step(d, nx, y, t, cfg, spine_x)
            steps.append(step)
            continue
        name = re.sub(rf"^{t['id']}\s*[·:.\-]?\s*", "", bare(t["title"]), flags=re.I)   # "T01 Comparison …" says t01 twice
        nh = card(d, nx, y, NODE_W, [(f"🧩 {t['id']} · {name}", T_STEP, INK)], sw=2.5)
        found = jd.finding(t, cfg)
        asked = ((cfg.get("tasks") or {}).get(t["name"]) or {}).get("asked") or t.get("question") or ""
        own = (topics or {}).get(f"{t['row']['task'].parent.name}/{t['name']}")
        topic = assets.parent.parent / own if own and assets else None          # a Task topic, while one is kept
        pages = run_pages(topic, t)                                             # its Runs' results/ first
        thumb = (t["id"], None, None, pages) if pages else None                 # no links: the results are here
        ask_most = 12 if tight else 24                                  # a big Job: fewer words a step, and no Did
        under = [("" if not asked or QUESTION.match(name) else f"Asks: {words(asked, ask_most)}", T_CARD, INK),
                 (f"Did: {words(did_of(t, cfg), 24)}" if did_of(t, cfg) and not (tight and t["runs"]) else "",
                  T_CARD, INK),                                         # line beside Runs that already say it
                 ("" if t["runs"] else "⬜ no Run yet", T_CARD, GREY)]
        cardh = card(d, nx + 36, y + nh + 16, CARD_W, under) + 16 if any(s for s, _, _ in under) else 0
        # its Runs branch to the right, below the line that goes out to its results, as a grid (run_cols a row)
        keep, folded = shown_runs(t, cfg)
        rx, ry, said, mids = nx + NODE_W + 110, y + nh + 24, {}, []
        marked = any(run_current(cfg, t["name"], r["name"]) for r in t["runs"])
        boxes = []                                                      # (lines, width, stroke, dashed), in order
        for r in keep:
            if marked and not run_current(cfg, t["name"], r["name"]):   # a rerun the current Run replaces: its name
                boxes.append(([(f"{r['mark']} {run_label(r['name'])}", T_RUNS - 2, GREY)], RUN_W - 160, 1, False))
                continue
            title = run_title(r)                                        # its original name (JL 261014): the card's
            short = clip(title, 20 if say_most >= 20 else 10) if title else ""   # share holds it and its sentence
            own_say = run_says(cfg, t["name"], r["name"])
            if own_say:
                own_say = words(own_say, max(5, say_most - Drawing.words_in(short)))
            says = own_say or ("" if r["values"] else headline(r["result"], say_most))
            if says and says in said:                                   # a rerun that says the same: say so, once
                line = (f"↺ as {said[says]}", T_RUNS, GREY)
            else:
                line = (says if own_say else f"“{says}”", T_RUNS, INK) if says else \
                       ((f"📊 {len(r['values'])} numbers →", T_RUNS, GREY) if r["values"] else
                        (holds(r["result"]) or "⬜ nothing in result/ yet", T_RUNS, GREY))
                if says:
                    said[says] = r["name"][:3]
            now = run_current(cfg, t["name"], r["name"])
            label = (f"{r['name'][:3]} · {short}" if short else
                     r["name"][:3] if tight and own_say else run_label(r["name"]))
            boxes.append(([(f"{r['mark']} {label}{'  📌 current' if now else ''}", T_RUNS, INK), line],
                          RUN_W, 2.5 if now else 1.2, False))
        if folded:                                                      # one box: their names, their states
            tally = Counter(f"{r['mark']} {r['state']}" for r in folded)
            names = " · ".join(r["name"][:3] for r in folded[:5]) + (f" … {folded[-1]['name'][:3]}" if len(folded) > 5 else "")
            quiet = not any(tells(r, cfg, t["name"]) for r in folded)
            boxes.append(([(f"{jd.n_of(len(folded), 'more Run' if keep else 'Run')}: {names}", T_RUNS, GREY),
                           (" · ".join(f"{n} {s}" for s, n in tally.most_common()) +
                            (" · nothing in their local result/" if quiet else ""), T_RUNS, GREY)], RUN_W, 1.5, True))
        per = run_cols(len(boxes))
        for i in range(0, len(boxes), per):                             # a row of the grid: as tall as its tallest
            row = boxes[i:i + per]
            row_h = max(lines_h(lines, w) for lines, w, _, _ in row)
            for k, (lines, w, sw, dashed) in enumerate(row):
                card(d, rx + k * (RUN_W + RUN_GAP), ry, w, lines, dashed=dashed, sw=sw)
            mids.append(ry + 30)                                        # the branch meets each row's first card
            ry += row_h + 18
        if mids:                                                        # the step's branches to its Runs
            bx = nx + NODE_W - 60                                       # right of its card, so no line crosses it
            d.line([(bx, y + nh), (bx, mids[-1])], arrow=False, sw=1.5)
            for m in mids:
                d.line([(bx, m), (rx - 8, m)], sw=1.5)
        mid = y + nh / 2
        d.line([(spine_x, mid), (nx - 8, mid)], sw=3)                  # the stair from the spine to this step
        steps.append({"y": y, "mid": mid, "right": nx + NODE_W, "task": t, "found": found, "thumb": thumb})
        y = max(y + nh + 16 + cardh, ry) + STEP_GAP                       # a step is as tall as its own boxes: its
                                                                        # results hang outside on their own row and
                                                                        # bend down when taller (JL 261014: "I don't
                                                                        # want the margin between the two tasks be
                                                                        # too large")
    if steps:
        d.line([(spine_x, spine_top), (spine_x, steps[-1]["mid"])], arrow=False, sw=3)

    opens = [str(o.get("item") if isinstance(o, dict) else o) for o in (cfg.get("open") or []) if o] if last else []
    y -= STEP_GAP - 60
    if opens and has_notes(cfg):
        y = d.para(40, y, f"❓ {jd.n_of(len(opens), 'point')} still open: what would close each is in the frame below",
                   width - 80, T_CARD, RED) + 8
    elif opens:
        for o in opens[:most_open]:
            y = d.para(40, y, f"❓ {words(o, 18)}", width - 80, T_CARD, RED) + 8
    said_words = sum(Drawing.words_in(e.get("text", "")) for e in d.els if e.get("frameId") == f["id"] and e["type"] == "text")
    if said_words > jd.MAP_WORDS:           # past a map's 200 words: read up close, measured by words per million px
        Drawing.detail(f)
    f = jd.finish(d, f, y + 40)

    # outside the frame, to its right: each Task's results, small, level with its step (the sketch's "T1 Results")
    d.fid = None
    first = len(d.els)
    column = any(s["thumb"] for s in steps)    # transcripts and screenshots make tall results: their own column,
    tall = [results_block(Drawing(), 0, 0, s["task"], cfg, s["found"], assets, s["thumb"])[0] for s in steps] \
        if column else []                       # measured first, then centred on ①: it may rise above the Job's
    start = f["y"] + f["height"] / 2 - (sum(tall) + 120 * max(0, len(tall) - 1)) / 2   # frame (JL 261014: "the
    rx0, last = width + RES_GAP, (start - 120 if column else -1e9)   # results can above the job frame"), an elbow
    for k, s in enumerate(steps):                                       # to each step (JL 261014: "make it like this")
        top = last + 120 if column else max(s["y"], last + 40)
        bx = rx0 + (STAGGER if column and k % 2 else 0)                  # 错落有致: the blocks zig-zag, not one column
        h, is_open = results_block(d, bx, top, s["task"], cfg, s["found"], assets, s["thumb"])
        hit = top + 32
        pts = [(s["right"] + 10, s["mid"]), (width + 60, s["mid"])] + \
              ([(width + 60, hit)] if abs(hit - s["mid"]) > 4 else []) + [(bx - 12, hit)]
        d.line(pts, sw=2, dashed=is_open)
        last = top + h
    for e in d.els[first:]:                 # the results follow ① when a builder lays frames out (canvas.grid,
        e.setdefault("customData", {})["follows"] = f["id"]   # d.acts), so they never stay behind (261014)
    return f


# ── ② the words it uses, how sure, what would close each open point: small, it explains ① ───────────────────
def has_notes(cfg: dict) -> bool:
    return bool(cfg.get("terms") or cfg.get("sure") or any(isinstance(o, dict) and o.get("closer")
                                                           for o in cfg.get("open") or []))


def notes_frame(d: Drawing, info: dict, cfg: dict, mark: str = "②") -> dict | None:
    """Asked by the reader review of 261013 ("neither one defines its terms … or says how to close what is open"): the
    face's `terms`, `sure` and `open` (with each `closer`), in a small frame stepped below and right of the staircase
    (canvas.explains), so its short labels decode."""
    if not has_notes(cfg):
        return None
    f = d.frame(f"{mark} 📖 {info['id']}: the words it uses, how sure, what is open", NW)
    Drawing.room(f)
    d.text(40, 22, "📖 Words to know", 40)
    y = 100
    terms = [t for t in cfg.get("terms") or [] if (t.get("term") if isinstance(t, dict) else t)]
    for t in terms[:TERMS]:
        term, means = (t.get("term"), t.get("means")) if isinstance(t, dict) else (str(t), "")
        y = d.para(40, y, str(term), NW - 80, T_RES) + 2
        y = d.para(70, y, words(means, 25), NW - 110, 24) + 14 if means else y + 10
    if len(terms) > TERMS:                  # never drop a term silently (found on OpioidRx b02, 261013)
        y = d.para(40, y, f"… {jd.n_of(len(terms) - TERMS, 'more term')} in the face", NW - 80, 24, GREY) + 14
    if cfg.get("sure"):
        y += 24
        d.text(40, y, "🎯 How sure", 34)
        h = Drawing.height(words(cfg["sure"], 50), NW - 140, 24) + 40
        d.key(40, y + 60, NW - 80, h)
        y = d.para(70, y + 80, words(cfg["sure"], 50), NW - 140, 24) + 30
    opens = [o for o in cfg.get("open") or [] if o]
    if opens:
        y += 24
        d.text(40, y, "❓ What is open, and what would close it", 34, RED)
        y += 66
        for o in opens:
            item = o.get("item", "") if isinstance(o, dict) else str(o)
            y = d.para(40, y, f"❓ {words(item, 25)}", NW - 80, 24, RED) + 2
            if isinstance(o, dict) and o.get("closer"):
                y = d.para(70, y, f"→ close by: {words(o['closer'], 25)}", NW - 110, 24, INK)
            y += 14
    canvas.explains(f)                      # small on purpose: it explains the staircase (JL 261013)
    f["height"] = max(y + 40, 600)
    if f["height"] > canvas.FRAME_MAX[1]:   # a list read top to bottom: only its width must fit
        canvas.reads_down(f)
    return f


# ── the drawing ──────────────────────────────────────────────────────────────────────────────────────────────
def draw_job(job: Path, out: Path, cfg: dict | None = None, source: str = "") -> tuple[Path, list[dict]]:
    """① the staircase (the main frame); ② its words, small; then any frame the face asks for (design grids, model
    table, chart, settings, the Job's pictures, `detail: true`'s words from zero), "in detail". The frames after ①
    step down and to the right of it (canvas.stairs), never in a left-aligned column."""
    cfg = cfg or {}
    job = job.resolve()
    design = jd.design_of(job.parent, cfg["design"]) if cfg.get("design") else {"grids": [], "tally": {}}
    cfg = {**cfg, "_tally": design["tally"], "_runs_word": str((cfg.get("design") or {}).get("runs_word") or "Runs")}
    rows = jr.job_rows(job.parent, job, {"show": cfg.get("show") or {}})
    tasks = [jd.task_info(r, {"show": cfg.get("show") or {}}) for r in rows]
    info = jd.job_info(job)
    d = Drawing()
    parts = split_steps(step_groups(tasks, cfg), cfg)                   # a big Job: two staircases, one story
    marks = iter("①②③④⑤⑥⑦⑧⑨⑩")
    ladders = [ladder_frame(d, info, steps, cfg, jd.task_topics(job.parent), next(marks), out.parent / "assets",
                            part=title, cont=k > 0, last=k == len(parts) - 1, grouped=True)
               for k, (title, steps) in enumerate(parts)]
    ladder = ladders[0]
    notes = notes_frame(d, info, cfg, next(marks)) if has_notes(cfg) else None
    nxt = marks
    extra = [jd.design_frame(d, info, fr, design, next(nxt)) for fr in (cfg.get("design") or {}).get("frames") or []]
    if cfg.get("models"):
        extra.append(jd.matrix_frame(d, info, cfg["models"], job, next(nxt)))
    if cfg.get("chart"):
        extra.append(jd.chart_frame(d, info, cfg["chart"], job.parent, out.parent / "assets", next(nxt)))
    if cfg.get("settings"):
        extra.append(jd.settings_frame(d, info, cfg["settings"], job.parent, next(nxt)))
    folders = [t["row"]["task"] for t in tasks]
    pics = [p for p in jd.pictures(job) if not any(f in p.parents for f in folders)]   # a Task's are in its results
    if pics:
        extra.append(jd.shown_frame(d, info, pics, job))
    if cfg.get("detail") is True:
        extra.append(jd.detail_frame(d, info, tasks, jd.task_topics(job.parent), cfg, out.parent / "assets",
                                     next(nxt)))
    below = ladders[1:] + ([notes] if notes else []) + [x for x in extra if x]
    labels = ["continues"] * (len(ladders) - 1) + (["its words"] if notes else []) + ["in detail"] * len(below)
    placed = canvas.stairs(d.els, [ladder["id"]] + [(x["id"], 600 if k == 0 else 420) for k, x in enumerate(below)])
    d.fid = None
    for k, (a, b) in enumerate(zip(placed, placed[1:])):
        x = b["x"] + min(b["width"], 600) / 2
        d.line([(x, a["y"] + a["height"] + 14), (x, b["y"] - 14)], sw=5)
        d.text(x + 20, (a["y"] + a["height"] + b["y"]) / 2 - 24, labels[k], 36)
    d.write(out, source or f"excalidraw-job scripts/job_ladder.py {job.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out, rows


if __name__ == "__main__":                                              # python job_ladder.py <job> <out.excalidraw>
    draw_job(Path(sys.argv[1]), Path(sys.argv[2]))
