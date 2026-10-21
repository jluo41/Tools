"""A Job as a staircase: the Job on top, each Task a step lower and further right, its Runs branching from its step;
each Task's results, its charts and tables side by side, in a block outside the frame; the blocks stay inside the
frame's top and bottom, or pass both by the same amount (JL 261014: "超出部分一定要对称、均匀").

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
        └─▶ 🧩 t01 · its step ─ r01 · r02 (grey names) · r04 📌 current ─────────────▶ 📊 t01: a sentence, then
              └─▶ 🧩 t02 · its step ─ its Runs ───────────────────────────────────────▶ 📊 t02: charts | tables
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

import os
import re
from fnmatch import fnmatch
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import job_drawing as jd  # noqa: E402

jr, Drawing, canvas = jd.jr, jd.Drawing, jd.canvas
INK, RED, GREY = jd.INK, jd.RED, jd.GREY

PAD, MOST = 22, 24                          # inside a box; Runs drawn per Task before the rest fold into one row
                                            # (8, was 6: a Job keeps to about 12 Runs now, so its Tasks' Runs show)
TERMS = 16                                  # terms drawn in ② before the rest are counted, never dropped
SHIFT, NODE_W, CARD_W, RUN_W = 380, 1200, 1080, 960   # a step right; a Task's box, its card, a Run's box: wide, so
                                                    #   each says itself in two or three lines (JL 261013)
JOB_W, IO_W = 1400, 1000                    # the Job's box; its in and out (wide like the steps, 261013)
STEP_GAP = 170                              # room between steps
RUN_WORDS = 280                             # the words every Run card (title + sentence) shares in ① (check.py ⑨: 600)
RUN_COLS, RUN_GAP = 3, 28                   # a Task's Runs as a grid, up to 3 a row (JL 261013: "make it wider")
CHART_W, NW = 1200, 1200                    # a results chart on the canvas (JL 261019: "the results can be larger,
                                            #   no need to be small", was 800); the words frame (② , secondary)
NOTE_W = 620                                # the notes beside a results block: how to read its chart or table
THUMB_W, THUMB_H = 320, 400                 # a Task topic's thumbnail, right of its results (left to right, 261014)
PAGE_W, PAGE_H = 300, 420                   # each page of a Run's highlighted transcript, as stored (readable)
SHOT_W, SHOT_H, MAX_SHOTS = 240, 200, 4     # beside it, its video's screenshots, each with its caption
NAME_W = 280                                # a Run's original name, left of its row
STAGGER = 240                               # every other results block sits this much further right (错位, 261014)
RES_COLS, PANEL_GAP, RES_VGAP = 3, 48, 90   # a results block's panels a row, at most; between panels; between blocks
TABLE_PART = 4                              # rows, at least, in each part of a long table split side by side
SPILL, COL_GAP = 2.0, 140                   # results past twice ①'s height stand in columns; between two columns
LANE_X, LANE_W = 60, 30                     # the first lane right of ① for a results link that bends; one lane's room
CASCADE_DX = 140                            # each Run's row a step further right: free style, not a column (261014)
T_TITLE, T_JOB, T_STEP, T_CARD, T_RUNS, T_RES = 64, 46, 38, 28, 28, 28   # 大小有致: the logic large, details smaller
PICTURES = (".png", ".jpg", ".jpeg")
QUESTION = re.compile(r"^(which|what|how|why|who|when|where|does|do|is|are|can|should)\b", re.I)   # a title that asks


# ── words, read from disk ────────────────────────────────────────────────────────────────────────────────────
def words(s: str, most: int) -> str:
    w = str(s).split()
    return " ".join(w[:most]) + (" …" if len(w) > most else "")


def run_label(rid: str) -> str:
    """A Run as the drawing names it: its folder name, exactly (`r04_fold00_six_models_p12`). JL 261019: "why the
    name here used is not the same as the task folder name or the run folder name? we don't need to create the new
    named to add the cognitive burden to us"."""
    return str(rid)


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


STATE_MARK = {"completed": "✅", "failed": "❌", "running": "🔶", "ready": "⬜", "proposed": "◌"}   # ref/propose-tree.md


def run_yaml(r: dict) -> dict:
    """The Run's card, `run.yaml`, as a mapping (empty when it has none)."""
    card = Path(r["dir"]) / "run.yaml" if r.get("dir") else None    # a Run read without its folder has no card
    data = jr.load(card) if card and card.is_file() else None
    return data if isinstance(data, dict) else {}


def card_state(r: dict) -> str:
    """One of completed · failed · running · ready · proposed (asked 261019: crosses, ticks, dashed boxes)."""
    if str(run_yaml(r).get("status") or "").lower() == "proposed" or str(r.get("state") or "").lower() == "proposed":
        return "proposed"
    return {"✅": "completed", "❌": "failed", "🔶": "running"}.get(r["mark"], "ready")


def run_why(r: dict, kind: str) -> str:
    """Why a failed Run stopped (its receipt's `failure:`), or what a proposed Run is for."""
    card = run_yaml(r)
    if kind == "failed":
        rt = jr.load(Path(r["result"]) / "runtime.yaml") if (Path(r["result"]) / "runtime.yaml").is_file() else None
        why = (rt or {}).get("failure") if isinstance(rt, dict) else None
        return str(why or card.get("failure") or "").split("(")[0].strip()
    if kind == "proposed":
        return str(card.get("says") or "")
    return ""


def run_files(r: dict, task: Path) -> str:
    """The files a Run stands on, by name (asked 261019: "for the run, could you also show what are the related
    files"): its ticket and its config; what it read and wrote are `run_io`'s lines."""
    name, rdir = r["name"], Path(r["dir"])
    parts = []
    if (rdir / f"{name}.sh").is_file() or (rdir / f"{name}.yaml").is_file():
        parts.append(f"🧾 {name}.sh")
    if run_config(r, task):
        parts.append(f"⚙ {run_config(r, task).name}")
    return " · ".join(parts)


def run_config(r: dict, task: Path) -> Path | None:
    """A Run's config: its own folder's config.yaml (one folder per Run), else the Task's scripts/config/<run>.yaml."""
    for p in (Path(r["dir"]) / "config.yaml", task / "scripts" / "config" / f"{r['name']}.yaml"):
        if p.is_file():
            return p
    return None


def fit_line(lead: str, items: list, width: float, size: int) -> str:
    """`lead`, then the first item and `+k` for the rest, on ONE line of `width`: a path keeps its last parts whole
    (`…/1-CandidatePool/v2026-08/grid_folds.parquet`, never cut inside a name); a listing `result/: a, b, c` keeps
    as many names as fit. Empty: `not recorded`."""
    if not items:
        return f"{lead}not recorded"
    more = f" +{len(items) - 1}" if len(items) > 1 else ""
    first = str(items[0]).strip()
    if ": " in first:                                           # a listing: its folder, then as many names as fit
        head, names = first.split(": ", 1)
        names = [n for n in names.split(", ") if n]
        for k in range(len(names), 0, -1):
            line = f"{lead}{head}: {', '.join(names[:k])}" + (f" +{len(names) - k}" if k < len(names) else "")
            if Drawing.measure(line, size) <= width:
                return line
        return f"{lead}{head}: {jd.n_of(len(names), 'file')}"    # not even one name fits: how many
    parts = [x for x in first.rstrip("/").split("/") if x]
    slash = "/" if first.endswith("/") else ""
    cuts = ["_WorkSpace/…/", "…/"] if parts[0] == "_WorkSpace" else ["…/"]   # a store path says it is the store's,
    for k in range(min(3, len(parts)), 0, -1):                  # when it fits; its last three parts, two, one: whole names
        for cut in cuts:
            line = f"{lead}{cut if k < len(parts) else ''}{'/'.join(parts[-k:])}{slash}{more}"
            if Drawing.measure(line, size) <= width:
                return line
    return f"{lead.split()[0]} {parts[-1]}{slash}{more}" if parts else line   # a long name alone: its mark, then
                                                                              #   the name whole (LLMRec b02 campaigns)


def run_io(r: dict, task: Path, cfg: dict, tname: str, width: float = RUN_W, size: int = T_RUNS) -> list[str]:
    """What a Run read and what it wrote, briefly (JL 261019: "for this run, we might want to show briefly about its
    input and output"). In: the face's `runs: {tNN/rNN: {in: …}}`, else its run.yaml `reads:`, else its config's
    `_meta.input`, `input`, `inputs`, `input_csv`, `grid_path`, `source`, `sources`, `source_root`, else its receipt's
    `reads:`. Out: the face's `out:`, else run.yaml `writes:` past result/, its heavy.yaml files, its config's
    `output_dir`, `output_root` or `final_root`, then what its result/ holds. Nothing is typed: an empty side says `not recorded`. Each side is one
    line of the card's `width` (`fit_line`), so a path never breaks inside a name."""
    own = ((cfg.get("runs") or {}).get(f"{tname}/{r['name']}") or {})
    card = run_yaml(r)
    conf_path = run_config(r, task)
    conf = jr.load(conf_path) if conf_path else {}
    conf = conf if isinstance(conf, dict) else {}
    res = Path(r["result"]) if r.get("result") else None
    rt = jr.load(res / "runtime.yaml") if res and (res / "runtime.yaml").is_file() else {}
    rt = rt if isinstance(rt, dict) else {}

    def as_list(v) -> list:                                     # a path, without the words a config adds after
        bare = lambda x: str(x).split(" (")[0].split(" + ")[0].strip()   # it: `… (frozen draw)`, `… + API_KEY`  # noqa
        if isinstance(v, dict):
            return [bare(x) for x in v.values() if isinstance(x, str)]
        return [bare(x) for x in v] if isinstance(v, list) else [bare(v)] if isinstance(v, str) else []

    ins = as_list(own.get("in")) or as_list(card.get("reads")) or \
        as_list((conf.get("_meta") or {}).get("input") if isinstance(conf.get("_meta"), dict) else None) or \
        next((as_list(conf[k]) for k in ("input", "inputs", "input_csv", "grid_path", "source", "sources", "source_root")
              if as_list(conf.get(k))), []) or as_list(rt.get("reads"))
    rows = conf.get("smoke_rows")                               # a smoke test whose queries sit in its config
    if isinstance(rows, list) and rows and (not ins or len(rows) == conf.get("expected_rows")):
        ins = [f"{len(rows)} {'query' if len(rows) == 1 else 'queries'} written in its config"]
    outs = as_list(own.get("out")) or [w for w in as_list(card.get("writes")) if w.rstrip("/") != "result"]
    heavy = jr.load(res / "heavy.yaml") if res and (res / "heavy.yaml").is_file() else None
    if not outs and isinstance(heavy, dict):
        held = {p.name for p in res.iterdir()} if res.is_dir() else set()
        outs = [h["file"] for h in heavy.get("heavy") or [] if isinstance(h, dict) and h.get("file") not in held]
        outs = [f"{Path(heavy['heavy'][0]['path']).parent.name}/: " + ", ".join(outs)] if outs else []
    if not outs:                                                # a store the Run wrote (LLMRec b02: the CallStore)
        outs = as_list(conf.get("output_dir")) + as_list(conf.get("output_root")) + as_list(conf.get("final_root"))
    if not outs and res and res.is_dir():
        files = sorted(p.name for p in res.iterdir() if p.is_file() and not p.name.startswith("."))
        dirs = sorted(p.name + "/" for p in res.iterdir() if p.is_dir() and not p.name.startswith("."))
        outs = ["result/: " + ", ".join(files + dirs)] if files + dirs else []
    room = width - 2 * PAD - 40                                 # wrap measures a little wider than measure()
    return [fit_line("📥 in: ", ins, room, size), fit_line("📤 out: ", outs, room, size)]


RUN_WIDE = 1700                             # a Run card with its plan: one a row, wide (JL 261019: "一个 run 占一行")


def run_plan(r: dict) -> list:
    """What a reader needs before saying yes to a Run (asked 261019: "每一个 run 的 aim 是什么？为什么要这样做？… 数据集有多
    大 … 你想在哪里 run？"): from its run.yaml, `aim`, `why`, `settings` (a mapping, drawn `key value · …`), and
    `host`, `time`, `after`. Empty when the card holds none of them."""
    c = run_yaml(r)
    out = []
    if c.get("aim"):
        out.append((f"🎯 aim: {c['aim']}", T_RUNS, INK))
    if c.get("why"):
        out.append((f"❔ why: {c['why']}", T_RUNS - 2, INK))
    st = c.get("settings")
    if isinstance(st, dict) and st:
        out.append(("⚙ " + " · ".join(f"{k} {v}" for k, v in st.items()), T_RUNS - 2, INK))
    where = [f"▶ {c['host']}" if c.get("host") else "", f"⏱ {c['time']}" if c.get("time") else "",
             f"after {c['after']}" if c.get("after") else ""]
    if any(where):
        out.append((" · ".join(w for w in where if w), T_RUNS - 2, GREY))
    if str(c.get("status") or "").lower() == "proposed" and c.get("needs"):   # a proposal's ticket is a stub: what
        out.append((f"🧩 needs first: {c['needs']}", T_RUNS - 2, INK))          #   it still needs (b01 s21 review)
    return out


def task_proposed(t: dict) -> bool:
    """A Task whose face says `state: ◌ proposed` draws its step dashed."""
    face = t["row"]["task"] / f"{t['name']}.md"
    head = face.read_text(errors="ignore")[:1500] if face.is_file() else ""
    return bool(re.search(r"(?m)^state:\s*(◌|proposed)", head))


def tells(r: dict, cfg: dict, task: str) -> bool:
    """A Run with something to report: numbers, a sentence, or files in its result."""
    return bool(r["values"] or run_says(cfg, task, r["name"]) or headline(r["result"]) or holds(r["result"]))


SERIES = re.compile(r"(?<=[a-z])(\d{2})(?=_|$)")   # the counter in r42_fold07_google_retry_v3: fold07
FOLD_LINES = 12                                     # Runs a folded card lists before it stands in parts
SPAN = re.compile(r"r\d+-r\d+")                    # the label of a part of leftovers: r01-r12


def series_of(rid: str) -> str:
    """A Run's series: its name past `rNN_` with its two-digit counter (a fold, a seed) as ##; '' when it has none."""
    slug = re.sub(r"^r\d+_", "", rid)
    key = SERIES.sub("##", slug, count=1)
    return key if key != slug else ""


def named_folds(t: dict, cfg: dict) -> list[tuple[str, list[str]]]:
    """The face's own folds for a Task: `folds: {tNN_task: [{title, runs: "<glob>" | [globs]}]}`, each one card
    whatever the Task's size (LLMRec b01 j03 t04: r01-r09 only bind t05's receipts, s23 reader review 261019)."""
    spec = (cfg.get("folds") or {}).get(t["name"]) or []
    return [(str(f.get("title") or ""), [f["runs"]] if isinstance(f["runs"], str) else [str(g) for g in f["runs"]])
            for f in spec if isinstance(f, dict) and f.get("runs")]


def fold_cards(t: dict, cfg: dict, runs: list[dict]) -> list[tuple[str, list[dict]]]:
    """`fold_groups` for one Task, the face's own folds first."""
    return fold_groups(runs, len(t["runs"]), named_folds(t, cfg))


def fold_groups(folded: list[dict], whole: int = 0, named=()) -> list[tuple[str, list[dict]]]:
    """The folded Runs as cards by what they do: a series of 3 or more (one setting across its folds) is one card
    titled by its range, `fold01-09 brave v1`; what is left is one card. b01 j02 t02's 57 Runs had shown the newest
    20, folds 06-09, and folded folds 00-05 out of sight (JL 261019: "I don't think these sNN jNN well structured")."""
    cards, rest, pool = [], [], list(folded)
    for title, globs in named:                                          # the face's own folds, by its title
        runs = [r for r in pool if any(fnmatch(r["name"], g) for g in globs)]
        if runs:
            cards.append((title or f"{runs[0]['name'][:3]}-{runs[-1]['name'][:3]}", runs))
            pool = [r for r in pool if r not in runs]
    by: dict[str, list[dict]] = {}
    for r in pool:
        by.setdefault(series_of(r["name"]), []).append(r)
    for key, runs in by.items():
        if key and len(runs) >= 3:
            nums = sorted(m.group(1) for r in runs for m in [SERIES.search(re.sub(r"^r\d+_", "", r["name"]))] if m)
            cards.append((key.replace("##", f"{nums[0]}-{nums[-1]}", 1).replace("_", " "), runs))
        else:
            rest += runs
    first: dict[str, list[dict]] = {}                                   # a family by its first word, no digit in it:
    for r in rest:                                                      #   34 page-evidence-item Runs of b01 j03 t04
        first.setdefault(re.sub(r"^r\d+_", "", r["name"]).split("_")[0], []).append(r)
    for word, runs in first.items():
        if not re.search(r"\d", word) and 5 <= len(runs) < (whole or len(folded)):   # never all of a Task's Runs
            cards.append((word, runs))
            rest = [r for r in rest if r not in runs]
    if rest:
        cards.append(("", [r for r in folded if r in rest]))
    out = []                                                            # a long card stands in parts of at most
    for label, runs in cards:                                           #   FOLD_LINES, so a row of cards fills its
        k = -(-len(runs) // FOLD_LINES)                                 #   width (b01 j03 t04: 35 page-evidence-item
        size = -(-len(runs) // k)                                       #   Runs beside two empty columns, 261019)
        for i in range(0, len(runs), size):
            part = runs[i:i + size]
            span = f"{part[0]['name'][:3]}-{part[-1]['name'][:3]}"
            out.append(((f"{label} · {span}" if label else span) if k > 1 else label, part))
    return out


def shown_runs(t: dict, cfg: dict) -> tuple[list[dict], list[dict]]:
    """The Runs drawn as cards, and the rest folded. Every Run is its own card, named, with its state,
    whether or not it ran (JL 261019 on b13 s21, three planned Runs drawn as one grey "3 Runs: r01 · r02 · r03":
    "you should show me the tasks and runs to be very explicit"). Only past MOST does a Task fold (b02 j05: 80 Runs);
    first by series (`fold_groups`): every Run outside a series keeps its card and each series folds into one;
    when that is still too many, the 📌 current Runs always, then the latest that report, then the latest planned
    ones. A folded card names every Run in full, with its state (a current Run never folds away: b03 s21, 261013)."""
    now = [r for r in t["runs"] if run_current(cfg, t["name"], r["name"]) or card_state(r) == "proposed"]   # a
    says = [r for r in t["runs"] if tells(r, cfg, t["name"]) and r not in now]   #   proposal keeps its card (b01 s22)
    rest = [r for r in t["runs"] if r not in now and r not in says]
    named = [r for r in t["runs"] if r not in now and any(fnmatch(r["name"], g) for _, gs in named_folds(t, cfg)
                                                          for g in gs)]
    if len(t["runs"]) <= MOST:
        return [r for r in t["runs"] if r not in named], named
    series = [r for k, runs in fold_cards(t, cfg, [r for r in t["runs"] if r not in now])
              if k and not SPAN.fullmatch(k) for r in runs]                     # a series or a family, not leftovers
    singles = [r for r in t["runs"] if r not in series]
    if series and len(singles) + len(fold_cards(t, cfg, series)) <= MOST:
        return singles, series
    room = max(MOST - 1 - len(now), 0)
    chosen = now + says[-room:] if room else now
    room = max(MOST - 1 - len(chosen), 0)
    chosen = chosen + (rest[-room:] if room else [])
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
                dict(family(ms, str(s.get("title") or f"{kind_of(ms[0])} · {len(ms)} Tasks"),
                            str(s.get("key") or f"{ms[0]['id']}-{ms[-1]['id']}"), str(s.get("asked") or "")),
                     frame=s.get("frame") or False, reading=str(s.get("reading") or ""))   # frame: its own staircase
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
    "· 1", "· 2". Three parts or more cut where each `from:` says (LLMRec b01 j02, 261019: 73 Runs named in full
    fill one staircase past check.py's 600 words; one per kind of source keeps each readable)."""
    parts = cfg.get("parts") or []
    at = [next((i for i, s in enumerate(steps) if s["id"].split("–")[0] == str(p.get("from"))
                or s["name"] == str(p.get("from"))), None) for p in parts[1:]]
    if len(parts) >= 2 and all(at) and at == sorted(set(at)):
        cut = [0] + at + [len(steps)]
        return [(str(p.get("title") or ""), steps[a:b]) for p, a, b in zip(parts, cut, cut[1:])]
    if len(steps) <= SPLIT_AT:
        return [("", steps)]
    h = (len(steps) + 1) // 2
    name = lambda ss: f"its Tasks {ss[0]['id'].split('–')[0]} to {ss[-1]['id'].split('–')[-1]}"
    return [(name(steps[:h]), steps[:h]), (name(steps[h:]), steps[h:])]


def expand_each(job: Path, cfg: dict) -> dict:
    """A family step's `show_each: [{label, at}]` with its `run:` gives every member Task the same picks from its own
    Run, so a family drawn as its own staircase (`frame: true`) shows each Task's numbers beside it."""
    names = sorted(p.name for p in job.glob("t[0-9][0-9]_*") if p.is_dir())
    pseudo = [{"id": n[:3], "name": n} for n in names]
    show = dict(cfg.get("show") or {})
    for st in cfg.get("steps") or []:
        if st.get("show_each") and st.get("run"):
            for tid in task_ids(st.get("tasks") or [], pseudo):
                name = next(q["name"] for q in pseudo if q["id"] == tid)
                show.setdefault(f"{name}/{st['run']}", st["show_each"])
    return {**cfg, "show": show}


def story_segments(groups: list[dict], cfg: dict) -> list[tuple[str, list[dict]]]:
    """The staircases when a family stands in its place (`frame: in place`, asked 261019: "你为什么不把之前最大那个地方给删掉，
    然后把这个东西移到上面去？这样的话就不会重复了"): the plain steps before it, the family as its own staircase, the steps after
    it, in the Job's order; each Task drawn once. A plain run after the first is named by the face's `parts:` entry
    whose `from` is its first step, else by its Tasks."""
    segs, cur = [], []
    for st in groups:
        if st.get("members") and st.get("frame") == "in place":
            if cur:
                segs.append(cur)
                cur = []
            segs.append([st])
        else:
            cur.append(st)
    if cur:
        segs.append(cur)
    out = []
    for k, seg in enumerate(segs):
        if len(seg) == 1 and seg[0].get("members") and seg[0].get("frame") == "in place":
            out.append((seg[0]["title"], seg))
            continue
        named = next((str(q.get("title") or "") for q in cfg.get("parts") or []
                      if str(q.get("from")) in (seg[0]["id"].split("–")[0], seg[0]["name"])), "")
        out.append(("" if k == 0 else named or f"its Tasks {seg[0]['id']} to {seg[-1]['id']}", seg))
    return out


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
            (f"Did: {words(did, 24)}" if did else "", T_CARD, INK),
            (f"→ each Task: frame {t['detail_mark']}" if t.get("detail_mark") else "",
             T_CARD, INK)]
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
    boxes = [([(f"{member_mark({'runs': rs})} {name} × {len(rs)}", T_RUNS, INK),   # its state mark (0.9.0)
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


def path_text(path: str, width: float, size: int) -> str:
    """A path broken only after a slash, each line within `width`, so it reads exactly as it is on disk."""
    lines, cur = [], ""
    for part in re.split(r"(?<=/)", str(path)):
        if cur and Drawing.measure(cur + part, size, code=True) > width:
            lines.append(cur)
            cur = part
        else:
            cur += part
    return "\n".join(lines + [cur])


def io_found(path: str, job: Path | None) -> bool:
    """Whether an In or Out path is on this machine: under the Job, or under any folder above it (`_WorkSpace/…`
    under the SPACE root, `work/b01_…/…` under the Project)."""
    if job is None:
        return True
    return any((base / str(path).rstrip("/")).exists() for base in [job, *job.parents])


def io_card(d: Drawing, x: float, y: float, w: float, label: str, items: list, most: int,
            job: Path | None) -> float:
    """📥 In or 📤 Out: each item one line, its path under it in grey (JL 261019: "could you also show the path for
    these data"); a path not found on this machine is red. An item is a string or {item, path}, its path one or a
    list; returns the height."""
    inner, size = w - 2 * PAD, T_RUNS - 6
    parts = [(label, T_STEP - 6, INK, False)]
    for it in items:
        text, paths = (it.get("item", ""), it.get("path")) if isinstance(it, dict) else (it, None)
        parts.append((f"· {words(text, most)}", T_RUNS, INK, False))
        for path in ([paths] if isinstance(paths, str) else paths or []):
            found = io_found(path, job)
            lead = "📂 " if found else "❓ not on this machine: "
            parts.append((path_text(lead + str(path), inner - 30, size), size, GREY if found else RED, True))
    h = PAD * 2 + sum((s.count("\n") + 1) * sz * 1.25 if code else Drawing.height(s, inner, sz) for s, sz, _, code
                      in parts) + 6 * len(parts)
    d.box(x, y, w, h, INK, 1.5)
    yy = y + PAD
    for s, sz, color, code in parts:
        if code:
            yy += d.text(x + PAD + 30, yy, s, sz, color, code=True)["height"] + 6
        else:
            yy = d.para(x + PAD, yy, s, inner, sz, color) + 6
    return h


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


_CHARTS: dict = {}                          # each chart drawn once a build: the layout measures a block at several widths


def chart_png(spec: dict, result: Path | None, out: Path) -> Path | None:
    key = (str(out), repr(spec), str(result))
    if key not in _CHARTS:
        _CHARTS[key] = bar_png(spec, result, out)
    return _CHARTS[key]


def bar_png(spec: dict, result: Path | None, out: Path) -> Path | None:
    """Horizontal bars, each labelled (the dataviz skill: magnitude by category; no legend, the title names it): each
    bar in its colour (jd.bar_colors; never all dark, JL 261019), thin 95% whiskers when `low`/`high` are given, a
    zero line when a value is negative,
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
    ax.barh(ys, vals, height=0.56, color=jd.bar_colors(spec, [r[0] for r in rows], spec.get("_colors")))
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
    room = 0.06 + 0.04 * max(len(show(v)) for v in vals)              # a value's label fits past its bar
    ax.set_xlim(min(lows) - span * 0.05 if min(lows) < 0 else 0, max(ends + [0]) + span * room)
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


def csv_where(path: Path, want: dict) -> list[dict] | None:
    """The rows of a CSV that `where` picks, read a row at a time: a Result's table may pass job_results.load's 4 MB
    (LLMRec b04 j08 t04's key_npi_lists.csv, 15,864 rows of NPI lists); numbers as numbers, as load reads them."""
    import csv
    if not path.is_file():
        return None
    def num(v):
        try:
            return float(v) if any(c in v for c in ".eE") else int(v)
        except (TypeError, ValueError):
            return v
    with path.open(newline="", encoding="utf-8") as f:
        return [{k: num(v) for k, v in row.items()} for row in csv.DictReader(f)
                if all(str(row.get(k)) == v for k, v in want.items())]


def table_cell(v, col: dict, spec: dict) -> str:
    """One cell of a CSV table: a number as `fmt` says; with `items: n`, a joined list (`sep`, default ";") shows its
    first n items, one a line, then how many more (LLMRec b04 s27, 261019: the key × engine table's NPI lists)."""
    if v is None or (isinstance(v, float) and v != v) or str(v) in ("", "nan", "None"):
        return "–"
    name = str(col.get("at") or col.get("label") or "")
    if str(col.get("fmt")) == "id" or re.search(r"(^|_)(npi|id)$", name):   # an id as written, never 1,619,084,993
        return str(int(v)) if isinstance(v, float) and v == int(v) else str(v)   # (LLMRec b01 s27 item2npi, 261019)
    if col.get("words") and isinstance(v, str):                          # a long text cell, cut to its first words
        return words(v, int(col["words"]))                               #   (LLMRec b01 t03 Table Card, 261020)
    if col.get("items"):
        items = [x for x in str(v).split(str(col.get("sep", ";"))) if x.strip()]
        n = int(col["items"])
        return " · ".join(items[:n]) + (f" · +{len(items) - n} more" if len(items) > n else "")
    return jr.number(v, str(col.get("fmt") or spec.get("fmt", "")))


def table_source(t: dict, cfg: dict, spec: dict) -> str:
    """Where a table's rows come from, under the Task: `runs/<run>/result/<file>`, so a reader knows which Run made
    it (JL 261019: "我想知道在处理的时候，它是哪一个 run"); empty for a row-per-Run or a family table."""
    if spec.get("runs") or spec.get("members"):
        return ""
    if spec.get("path"):
        return str(spec["path"])
    result = chart_run(t, cfg, spec)
    try:
        return f"{result.relative_to(t['row']['task']).as_posix()}/{spec['file']}" if result and spec.get("file") else ""
    except ValueError:
        return f"{result}/{spec['file']}"


def task_tables(t: dict, cfg: dict) -> list[tuple[str, list[str], list[dict]]]:
    """The tables the face names from a Task's Run (`tables: {<tNN_task>: [{title, file, columns, rows, sort, run}]}`):
    a CSV under the Run's result, its named columns, its first `rows` rows (6), sorted by `sort` (`-col`: largest
    first), only the rows `where` picks (`col=v&col2=v`, as a chart's row selector: one model of a Stata table that
    holds several, OpioidRx 261013). Returns (title, columns, rows) each, read on every build."""
    out = []
    for spec in ((cfg.get("tables") or {}).get(t["name"]) or [])[:2]:
        if spec.get("runs"):                                            # a row per Run, each cell read from that
            out.append(run_rows(t, cfg, spec))                          #   Run's own result (a paper per Run)
            continue
        if spec.get("members") and t.get("members"):                    # a family: a row per member Task, each
            cols = spec.get("columns") or []                            #   cell read from that Task's own Run
            out.append((str(spec.get("title", spec.get("file", ""))),
                        [str(spec.get("first", "Task"))] + [str(c.get("label", c.get("at"))) for c in cols],
                        [{"cells": [member_label(m, cfg, spec)] +
                          [jr.number(member_value(m, cfg, spec, str(c.get("at"))), str(c.get("fmt", ""))) for c in cols],
                          "dim": False} for m in t["members"]]))
            continue
        result = chart_run(t, cfg, spec)
        block = t["row"]["task"].parents[1] if spec.get("path") else None   # `path:` a file anywhere in the
        src = (block / spec["path"]) if block else (result / spec["file"]) if result else None
        want = dict(c.split("=", 1) for c in str(spec["where"]).split("&")) if spec.get("where") else {}
        data = csv_where(src, want) if want and src and src.suffix == ".csv" else jr.load(src) if src else None
        if isinstance(data, list) and want:                             #   Block (a Task whose Runs keep nothing)
            data = [r for r in data if isinstance(r, dict) and all(str(r.get(k)) == v for k, v in want.items())]
        if not isinstance(data, list) or not data:
            out.append((f"❓ table {spec.get('title', spec.get('file'))}: not in the result", [], []))
            continue
        cols = spec.get("columns") or list(data[0])[:4]
        cols = [c if isinstance(c, dict) else {"at": c} for c in cols]   # a column: a name, or {at, label, items,
        key = str(spec.get("sort") or "")                               #   sep}: a list cell shows its first items
        if key:
            data = sorted(data, key=lambda r: (r.get(key.lstrip("-")) is None, r.get(key.lstrip("-"))),
                          reverse=key.startswith("-"))
        names = spec.get("labels") or {}
        shown = [{"cells": [names.get(str(r.get(c["at"])), short_key(r.get(c["at"]))) if i == 0 else table_cell(r.get(c["at"]), c, spec)
                            for i, c in enumerate(cols)], "dim": False} for r in data[:int(spec.get("rows", 6))]]
        out.append((str(spec.get("title") or spec.get("file") or spec.get("path")),
                     [str(c.get("label") or c["at"]).replace("_", " ") for c in cols], shown))
    return out


def run_rows(t: dict, cfg: dict, spec: dict) -> tuple[str, list[str], list[dict]]:
    """A Task whose every Run is one subject (a paper, a source) as a table, one row per Run (`runs: true`; LLMRec
    261014: "make the report of the task to be shown as the table"): the Run's id, then each column's `at`, read from
    that Run's result (`<file>:<key>`, as `show:`), or `says` for the face's sentence on it. `rows` caps it (12); the
    rest are counted, never dropped silently."""
    cols = spec.get("columns") or [{"label": "says", "at": "says"}]
    only = spec.get("only") or ["*"]                                    # `only:` globs on the Run folder names
    only = [only] if isinstance(only, str) else only
    runs = [r for r in t["runs"] if r["result"].is_dir() and any(fnmatch(r["name"], g) for g in only)]
    most = int(spec.get("rows", 12))

    def cell(r: dict, c: dict) -> str:
        at = str(c.get("at", ""))
        if at == "says":
            v = run_says(cfg, t["name"], r["name"])
        else:
            file, _, key = at.rpartition(":")
            v = jr.dig(jr.load(r["result"] / (file or "runtime.yaml")), key)
        return words(str(v), int(c.get("words", 12))) if isinstance(v, str) else jr.number(v, str(c.get("fmt", "")))

    rows = [{"cells": [r["name"][:3]] + [cell(r, c) for c in cols], "dim": False} for r in runs]
    rows = [row for row in rows if any(c not in ("", "—") for c in row["cells"][1:])]   # a Run with nothing in
    n = len(rows)                                                                         #   these columns: no row
    rows = rows[:most]
    if n > most:
        rows.append({"cells": [f"+{n - most}"] + [f"{jd.n_of(n - most, 'more Run')}, not shown"] +
                     [""] * (len(cols) - 1), "dim": True})
    title = str(spec.get("title") or f"{jd.n_of(n, 'Run')}, one row each")
    return (title, ["Run"] + [str(c.get("label", c.get("at"))) for c in cols], rows) if n else \
        (f"❓ table {title}: no Run with a result", [], [])


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


WIDE_W = 2 * 1200 + 48                     # a wide picture's room: two panels and their gap
WIDE = 1.9                                  # a picture this many times wider than tall spans a results row


def is_wide(p: Path) -> bool:
    """A picture much wider than tall: a screenshot of a data table, drawn across the whole results row."""
    try:
        from PIL import Image
        with Image.open(p) as im:
            return im.width >= WIDE * im.height
    except Exception:
        return False


def results_block(d: Drawing, x: float, y: float, t: dict, cfg: dict, found: str,
                  assets: Path | None, thumb: tuple | None = None, cols: int = 1) -> tuple[float, float, bool]:
    """A Task's results, outside the frame: a small title and its finding in one sentence across the top; under them
    its panels side by side, up to `cols` a row, each under the shortest column so far (asked 261014: "这个 result
    右边有这么多的空位你都不用，非要挤着那么一块"): the charts the face names (`charts:`, drawn here from its Run's
    result); the figures the Task holds (task_pictures: a figure Run's charts, JL 261013); the tables it names
    (`tables:`, rows from its Run's CSV); else its current Run's picked numbers as a table.
    Returns (width, height, open): open, dashed, when it shows none of these."""
    nn, png, link, pages = thumb or (None, None, None, [])
    panels = []                                     # each draws itself at (px, py), CHART_W wide; returns its bottom
    drawn = 0
    for k, spec in enumerate(((cfg.get("charts") or {}).get(t["name"]) or [])[:3]):
        if spec.get("members") and t.get("members"):                    # a family: a bar per member Task
            spec = {**spec, "_rows": member_rows(t, cfg, spec)}
        src = t["row"]["task"] if "_rows" in spec else chart_run(t, cfg, spec)
        spec = {**spec, "_colors": cfg.get("colors")}                   # one source, one hue, every chart
        png = chart_png(spec, src, assets / f"chart-{t['name']}-{k}.png") if assets else None
        if not png:
            panels.append(lambda px, py, k=k, spec=spec: d.para(
                px, py, f"❓ chart {spec.get('title', k)}: no values in its result", CHART_W, T_RES - 2, RED) + 8)
            continue

        def chart(px, py, k=k, spec=spec, png=png):
            py = d.para(px, py, str(spec.get("title", "")), CHART_W, T_RES, INK) + 4
            return py + d.picture(png, px, py, CHART_W, 900, fid=f"chart-{t['name']}-{k}") + 16
        panels.append(chart)
        drawn += 1
    charted = drawn
    wides = []                                      # a wide picture (a screenshot of real rows) spans the row
    for k, p in enumerate(task_pictures(t, cfg)):                       # its own figures, as its Runs drew them:
        if is_wide(p):                                                  #   (JL 261019: "could you make this wide?")
            def wide(px, py, ww, k=k, p=p):
                py += d.picture(p, px, py, ww, 1400, fid=f"fig-{t['name']}-{k}") + 6
                return d.para(px, py, str(p.relative_to(t["row"]["task"])), ww, 20, GREY) + 20
            wides.append(wide)
            drawn += 1
            continue
        def figure(px, py, k=k, p=p):                                   #   a figure Run's charts come first
            py += d.picture(p, px, py, CHART_W, 640, fid=f"fig-{t['name']}-{k}") + 6   # (JL 261013), then the
            return d.para(px, py, str(p.relative_to(t["row"]["task"])), CHART_W, 20, GREY) + 16   # exact rows
        panels.append(figure)
        drawn += 1
    tabled, tabs = False, []                        # (title, head, rows, widths, size, pad, after): a long one may
    specs = ((cfg.get("tables") or {}).get(t["name"]) or [])[:2]
    for (title, head, rows), spec in zip(task_tables(t, cfg), specs):  #   stand in parts, side by side, where
        if not rows:                                                    #   columns are free; its tables, from its
            panels.append(lambda px, py, title=title: d.para(px, py, title, CHART_W, T_RES - 2, RED) + 8)
            continue                                                    #   Run's own files
        first = CHART_W * (0.1 if head[0] == "Run" else 0.46)          # a row per Run: its id is short
        rest = (CHART_W - first) / max(1, len(head) - 1)
        ws = spec.get("widths") if isinstance(spec.get("widths"), list) and len(spec["widths"]) == len(head) else None
        widths = [CHART_W * f / sum(ws) for f in ws] if ws else [first] + [rest] * (len(head) - 1)   # the face's shares
        src = "\n".join([table_source(t, cfg, spec)] + [f"↳ {c}" for c in (spec.get("cite") or [])])   # each column
        tabs.append((title, head, rows, widths, 24, 20, 16, src.strip()))   #   group's own source (JL 261019)
        tabled = True
    if not charted and not tabled:
        now = [r for r in t["runs"] if run_current(cfg, t["name"], r["name"])]
        vals = [v for r in (now or [r for r in t["runs"] if r["values"]][-1:]) for v in r["values"]]
        if vals:                                                       # no chart or table named: its numbers, a table
            labels = sorted({str(k.get("label") or "") for key, picks in (cfg.get("show") or {}).items()
                             if str(key).startswith(f"{t['name']}/") for k in picks or [] if isinstance(k, dict)},
                            key=len, reverse=True)              # the face's own label, so a unit stays with its
            def split(v: str) -> list[str]:                     #   number ("1,326 chars", reader review 261014)
                lab = next((x for x in labels if x and v.startswith(x + " ")), None)
                return [lab, v[len(lab):].strip()] if lab else v.rsplit(" ", 1) if " " in v else [v, ""]
            rows = [{"cells": split(v), "dim": False} for v in vals]
            src = [r["name"] for r in (now or [r for r in t["runs"] if r["values"]][-1:]) if r["values"]]
            head = [f"measure ({run_label(src[0])})" if len(src) == 1 else "measure", "value"]
            tabs.append(("", head, rows, [CHART_W * 0.62, CHART_W * 0.38], T_RES, 24, 10, ""))
            tabled = True
    spare, parts = cols - len(panels) - len(tabs), [1] * len(tabs)     # columns no panel would fill: the longest
    for i in sorted(range(len(tabs)), key=lambda i: -len(tabs[i][2])):  #   tables take them, in parts of at least
        n = min(1 + max(0, spare), len(tabs[i][2]) // TABLE_PART)        #   TABLE_PART rows (a paper table of 12
        if n > 1:                                                       #   rows, three parts of 4, JL 261014)
            parts[i], spare = n, spare - (n - 1)
    for (title, head, rows, widths, size, pad, after, src), n in zip(tabs, parts):
        per = -(-len(rows) // n)
        for j in range(n):
            def table(px, py, title=title, head=head, rows=rows[j * per:(j + 1) * per], widths=widths, size=size,
                      pad=pad, after=after, j=j, src=src if j == n - 1 else ""):
                if title and not j:
                    py = d.para(px, py, title, CHART_W, T_RES, INK) + 4
                elif title:                                             # a part: its header level with the first's
                    d.para(px, py, "(continued)", CHART_W, T_RES - 4, GREY)
                    py += Drawing.height(title, CHART_W, T_RES) + 4
                py = d.grid_table(px, py, head, rows, widths, size if len(head) < 6 else size - 2, pad=pad,
                                  head=28 if len(head) < 6 else 22)    # six columns or more: smaller type
                for k, line in enumerate(src.split("\n") if src else []):   # its Run, as a figure does; then one
                    py = d.para(px, py + (6 if not k else 2), line, CHART_W, 20, GREY)   #   line per cited source
                return py + after
            panels.append(table)

    cols = max(1, min(cols, len(panels))) if panels else max(1, cols)   # never a column with nothing in it
    area = cols * CHART_W + (cols - 1) * PANEL_GAP
    if wides:                                       # a wide picture needs at least two panels' room
        area = max(area, WIDE_W)
    row = max((NAME_W + 16 + len(g["pages"]) * (PAGE_W + 10) + (16 + len(g["shots"]) * (SHOT_W + 12) if g["shots"] else 0)
               for g in pages), default=0)
    right = (len(pages) - 1) * CASCADE_DX + row if pages else 0
    under = bool(pages) and not panels              # transcripts only: its title and finding across the top, the Runs'
    w = right + 2 * PAD if under else area + 2 * PAD + (right + 28 if right else 0)   # rows under them, no empty
    notes = [] if under else list((cfg.get("notes") or {}).get(t["name"]) or [])   # how to read it, to the right
    if notes:                                       #   (asked 261019: "在这两个图的右边再加一些注释吧")
        w += NOTE_W + 28
    name = re.sub(rf"^{re.escape(t['id'])}\s*[·:.\-]?\s*", "", bare(t["title"]), flags=re.I)   # column (261014); a
    head = t["name"] if not t.get("members") else f"{t['id']} · {t['title']}"   # a Task by its folder; a family
    yy = d.para(x + PAD, y + PAD, f"📊 {head}: results", right if under else area, T_RES + 2, INK) + 6   # by its face
    if under and found:                             # block reads as its step's without its line (261014)
        first = re.split(r"(?<=[.!?])\s+", str(found).strip())[0]
        yy = d.para(x + PAD, yy, f"💡 {words(first, 30)}", min(right, 1800), T_RES, INK) + 24
    side = yy
    if right:                                       # to the right of the results, so a block grows wide, not tall
        tx = x + PAD + (0 if under else area + 28)                    # (JL 261014: "the results of the png can be from left to right")
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
                    low = max(low, d.para(sx, gy + sh + 6, words(cap, 20), SHOT_W, 20, GREY))   # whole, readable
                    sx += SHOT_W + 12
                gy = low + 40
            side = gy - 36
    if found and not under:                         # one sentence; the panels carry the numbers
        first = re.split(r"(?<=[.!?])\s+", str(found).strip())[0]
        yy = d.para(x + PAD, yy, f"💡 {words(first, 18 if cols == 1 else 30)}", area, T_RES, INK) + 14
    for wide in wides:                              # across the whole row, before the panels
        yy = wide(x + PAD, yy, area)
    tops = [yy] * cols
    if notes:                                       # a column of short notes beside the panels, smaller: it explains
        nx = x + PAD + area + 28 + (right + 28 if right else 0)
        ny = d.para(nx, yy, "📖 how to read it", NOTE_W, T_RES - 2, INK) + 6
        for n in notes:
            line = f"{n.get('term')}: {n.get('means')}" if isinstance(n, dict) else str(n)
            ny = d.para(nx, ny, f"· {line}", NOTE_W, T_RES - 6, INK) + 8
            canvas.aside(d.els[-1])
        side = max(side, ny)
    for panel in panels:                            # reading order, each under the shortest column so far
        c = min(range(cols), key=lambda i: (tops[i], i))
        tops[c] = panel(x + PAD + c * (CHART_W + PANEL_GAP), tops[c])
    yy = max(tops)
    is_open = not (found or drawn or tabled)
    if is_open:
        planned = t["runs"] and all(card_state(r) in ("proposed", "ready") for r in t["runs"])   # nothing ran: a plan,
        yy = d.para(x + PAD, yy, ("◌ proposed: nothing has run" if task_proposed(t) else "⬜ nothing has run yet")   # not a
                    if planned else "❓ nothing found yet" if t["runs"] else "⬜ no Run yet", area, T_RES,   # gap (261019)
                    RED if t["runs"] and not planned else GREY) + 8
    h = max(yy, side) - y + PAD - 8                                    # the taller of the two columns
    d.box(x, y, w, h, GREY if is_open else INK, 1.5, dashed=is_open)
    return w, h, is_open


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
    grid = max((run_cols(len({run_label(r["name"]) for r in t["runs"]})) if t.get("members") else   # a family:
                run_cols(len(k) + len(fold_cards(t, cfg, fo))) for t in tasks for k, fo in [shown_runs(t, cfg)]), default=1)
    runs_w = grid * RUN_W + (grid - 1) * RUN_GAP
    width = max(130 + max(cols, default=0) * SHIFT + NODE_W + 110 + runs_w + 60, 40 + JOB_W + 120 + IO_W + 60)
    title = f"🪜 {jd.name_of(info)}" + (f" · {part}" if cont and part else "")   # a second staircase: what it holds
    f = d.frame(f"{mark} {title}: " + ("its Tasks as steps, continued" if cont else "why it exists, its Tasks as steps"),
                width)
    Drawing.room(f)                         # the room between the steps is the point; measured over the boxes
    if width > canvas.FRAME_MAX[0]:
        canvas.large(f)
    d.text(40, 22, title, T_TITLE)
    n_tasks = sum(len(t.get("members") or [t]) for t in tasks)          # a family's Tasks, not its one step
    sub = f"{info.get('block') or ''} · {jd.n_of(n_tasks, 'Task')}" + \
          (f" in {jd.n_of(len(tasks), 'step')}" if n_tasks > len(tasks) else "") + f" · {jd.n_of(n_runs, 'Run')}: " \
          f"{jd.states([r for t in tasks for r in t['runs']])}"
    rows = (cfg.get("settings") or {}).get("rows") or []      # the face's to-finish table, when it has one
    if rows and not cont:                                      # (JL 261019: "how could we quickly know the status?")
        c = Counter(str(r.get("state") or "") for r in rows)
        sub += f" · 🧪 to finish: ✅ {c['done']} done" + (f", ❌ {c['blocked']} failed" if c["blocked"] else "") + \
            f", ⬜ {c['planned']} left" + (" · Job not closed" if c["planned"] else " · nothing left")
    d.para(40, 112, sub.strip(" ·"), width - 80, T_RUNS, GREY)
    if cont:                                                            # the staircase continued: no Job box
        spine_x, spine_top, most_open = 60, 180, 3                    #   again; its key point is what it holds
        said = next((str(q.get("key") or "") for q in cfg.get("parts") or [] if str(q.get("title")) == part), "") or \
            next((str(q.get("reading") or "") for q in cfg.get("steps") or [] if str(q.get("title")) == part), "")
        key = f"🎯 {said or part or 'its Tasks, continued'}"
        kh = Drawing.height(key, width - 140, 34) + 44
        d.key(40, 180, width - 80, kh)
        d.para(70, 202, key, width - 140, 34)
        spine_top = 180 + kh + 40
        spec = next((q for q in cfg.get("steps") or [] if str(q.get("title")) == part), None)   # a family's frame:
        fkey = str((spec or {}).get("key") or ((spec or {}).get("tasks") if isinstance((spec or {}).get("tasks"), str)
                                               else ""))               #   its notes under its key point
        fnotes = list((cfg.get("notes") or {}).get(fkey) or []) if fkey else []
        if fnotes:
            ny = d.para(70, spine_top - 16, "📖 how to read it", width - 140, T_RES - 2, INK) + 6
            half, cw = (len(fnotes) + 1) // 2, (width - 160) / 2
            low = ny
            for c, col in enumerate((fnotes[:half], fnotes[half:])):
                cy = ny
                for n in col:
                    line = f"{n.get('term')}: {n.get('means')}" if isinstance(n, dict) else str(n)
                    cy = d.para(70 + c * (cw + 20), cy, f"· {line}", cw, T_RES - 4, INK) + 8
                    canvas.aside(d.els[-1])
                low = max(low, cy)
            spine_top = low + 30
        y = spine_top + 60
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
        jh = card(d, 40, y, JOB_W, [(f"🧱 {jd.name_of(info)}", T_JOB, INK)], sw=3)   # its folder name (261019)
        why = [(f"Why: {words(aim, 40)}" if aim else "❓ no aim: the Job face has no goal: line", T_CARD, None),
               (f"Done when: {words(info['close'], 34)}" if info.get("close") else   # 22 cut its end in four
                                                                                     # OpioidRx reviews (261013)
                "❓ close: not written on the Job face", T_CARD, None),
               (f"Answers: {info['answers']}" if info.get("answers") else "", T_CARD, INK)]
        ch = card(d, 110, y + jh + 20, JOB_W - 110, why)
        most_io, io_words, most_open = (4, 16, 3) if tight else (6, 26, 4)      # every input, whole, with its path
                                                                                #   (261019: "not complete")
        io_x, yy = 40 + JOB_W + 120, y
        job_dir = next((t["row"]["task"].parent for t in tasks if t.get("row")), None)
        for label, items in (("📥 In", (cfg.get("inputs") or [])[:most_io]), ("📤 Out", (cfg.get("outputs") or [])[:most_io])):
            if items:
                h = io_card(d, io_x, yy, IO_W, label, items, io_words, job_dir)
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
        proposed = task_proposed(t)                                     # a proposed Task: its step dashed
        nh = card(d, nx, y, NODE_W, [(f"{'◌' if proposed else '🧩'} {t['name']}" + (" · proposed" if proposed
                                      else ""), T_STEP, INK)], sw=1.5 if proposed else 2.5, dashed=proposed)
        found = jd.finding(t, cfg)
        asked = ((cfg.get("tasks") or {}).get(t["name"]) or {}).get("asked") or t.get("question") or ""
        own = (topics or {}).get(f"{t['row']['task'].parent.name}/{t['name']}")
        topic = assets.parent.parent / own if own and assets else None          # a Task topic, while one is kept
        pages = run_pages(topic, t)                                             # its Runs' results/ first
        thumb = (t["id"], None, None, pages) if pages else None                 # no links: the results are here
        ask_most = 12 if tight else 24                                  # a big Job: fewer words a step, and no Did
        under = [("" if not asked else f"Asks: {words(asked, ask_most)}", T_CARD, INK),   # the step shows its
                                                                        #   folder name, so its question is said here
                 (f"Did: {words(did_of(t, cfg), 24)}" if did_of(t, cfg) and not (tight and t["runs"]) else "",
                  T_CARD, INK)]                                         # line beside Runs that already say it;
        # no "⬜ no Run yet" line: the subtitle counts the Runs and the results block says it (JL 261014: "do we
        # need this? maybe we can delete this one")
        page = t["row"]["task"] / f"{t['name']}.md"                     # where its detail lives (reader review
        if page.is_file():                                              #   261014: "no Task page is named")
            under.append((f"📄 page: {t['name']}/{page.name}", T_CARD - 4, GREY))
        cardh = card(d, nx + 36, y + nh + 16, CARD_W, under) + 16 if any(s for s, _, _ in under) else 0
        if page.is_file() and assets:                                   # the line opens the page
            for e in reversed(d.els):
                if e["type"] == "text" and e.get("text", "").startswith("📄 page:"):
                    e["link"] = os.path.relpath(page, assets.parent)
                    break
        # its Runs branch to the right, below the line that goes out to its results, as a grid (run_cols a row)
        keep, folded = shown_runs(t, cfg)
        rx, ry, said, mids = nx + NODE_W + 110, y + nh + 24, {}, []
        marked = any(run_current(cfg, t["name"], r["name"]) for r in t["runs"])
        boxes = []                                                      # (lines, width, stroke, dashed), in order
        detailed = cfg.get("run_cols") == 1                             # the face asks: one wide card a row; else
                                                                        #   only a card with a plan stands alone
        for r in keep:
            kind = card_state(r)                                        # ✅ ❌ 🔶 ⬜ ◌, dashed until it ran
            r = {**r, "mark": STATE_MARK.get(kind, r["mark"])}          #   (ref/propose-tree.md, 261019)
            dashed, why, files = kind in ("ready", "proposed"), run_why(r, kind), run_files(r, t["row"]["task"])
            quiet_w = min(RUN_W, max(RUN_W - 160, Drawing.measure(f"{r['mark']} {r['name']}", T_RUNS - 2)
                                     + 2 * PAD + 30))                   # wide enough for its whole folder name;
                                                                        #   📥 in · 📤 out, at the card's size
            io_of = lambda w_: [(s_, T_RUNS, GREY) for s_ in run_io(r, t["row"]["task"], cfg, t["name"], w_)] + [
                (f_, T_RUNS - 6, GREY) for f_ in ([files] if Drawing.measure(files, T_RUNS - 6) <= w_ - 2 * PAD - 40
                                                  else files.split(" · "))]   # noqa: E731  ticket, config: a line
                                                                        #   each when together they would break a name
            if any(Drawing.measure(s_, T_RUNS) > quiet_w - 2 * PAD - 8 for s_, _, _ in io_of(quiet_w)[:2]):
                quiet_w = RUN_W                                         # a name too long for 📥 or 📤: full width
            plan = run_plan(r)
            if marked and not run_current(cfg, t["name"], r["name"]) and not plan:   # a rerun the current Run replaces: quiet,
                st = str(r["state"] or "") if str(r["state"] or "") not in ("None", "null") else ""   # but it still
                st = st or ("proposed" if kind == "proposed" else "not run yet")                     # says its state,
                boxes.append(([(f"{r['mark']} {run_label(r['name'])}", T_RUNS - 2, GREY),            # why it failed
                               (st + (f" · {words(why, 12)}" if why else ""), T_RUNS - 4, GREY)] +   # or what it is
                              io_of(quiet_w), quiet_w, 1, dashed))                                    # for, its files
                continue
            title = run_title(r)                                        # its original name (JL 261014): the card's
            whole = title and Drawing.words_in(title) <= say_most           # share holds it and its sentence: the
            short = title if whole else clip(title, 20 if say_most >= 20 else 10) if title else ""   # whole name
            own_say = run_says(cfg, t["name"], r["name"])               #   when it fits (JL 261014: "why here the
            left = say_most - Drawing.words_in(short)                   #   run's name is not full?"), its sentence
            if own_say:                                                 #   in what is left, none when too little
                own_say = words(own_say, max(5, left)) if left >= 4 or not whole else ""
            quiet = bool(whole and run_says(cfg, t["name"], r["name"]) and not own_say)   # its name took the room:
            says = own_say or ("" if r["values"] or quiet else headline(r["result"], say_most))   # no file counts
            if quiet:                                                   #   in place of its sentence (b61, 261015)
                line = ("", T_RUNS, INK)
            elif says and says in said:                                   # a rerun that says the same: say so, once
                line = (f"↺ as {said[says]}", T_RUNS, GREY)
            else:
                line = (says if own_say else f"“{says}”", T_RUNS, INK) if says else \
                       ((f"📊 {len(r['values'])} numbers →", T_RUNS, GREY) if r["values"] else
                        (holds(r["result"]) or f"⬜ {r['state'] if str(r['state'] or '') not in ('', 'None', 'null') else 'not run yet'}", T_RUNS, GREY))
                if says:
                    said[says] = r["name"][:3]
            now = run_current(cfg, t["name"], r["name"])
            label = r["name"]                                           # its folder name, exactly (JL 261019)
            if short:                                                   # a paper's or video's own title, filed
                line = (f"📄 {short}" + (f" · {line[0]}" if line[0] else ""), line[1], line[2])   # on its Result Card
            if kind == "proposed":                                      # a proposal says what it is for, when it
                when = str(run_yaml(r).get("proposed") or "")           #   was proposed, and that it waits for a yes
                line = (f"◌ proposed {when} · waits for a yes" + (f" · {words(why, 16)}" if why and not plan else ""),
                        T_RUNS, INK)                                    #   (its plan says why once, below)
            elif why and kind == "failed" and why not in str(line[0]):
                line = (f"{line[0]} · {words(why, 12)}".strip(" ·"), line[1], line[2])
            card_w = RUN_WIDE if detailed or plan else RUN_W
            boxes.append(([(f"{r['mark']} {label}{'  📌 current' if now else ''}", T_RUNS, INK), line] + plan +
                          io_of(card_w), card_w, 2.5 if now else 1.2,
                          dashed))
        for label, runs in fold_cards(t, cfg, folded):                  # a box a series: each Run on its own line,
            marks = [STATE_MARK.get(card_state(r), r["mark"]) for r in runs]   #   named in full, with its state
            tally = Counter(f"{m} {r['state']}" for m, r in zip(marks, runs))
            quiet = not any(tells(r, cfg, t["name"]) for r in runs)
            head = (f"🔁 {label} · {jd.n_of(len(runs), 'Run')}" if label and not SPAN.fullmatch(label)
                    else jd.n_of(len(runs), 'more Run' if keep else 'Run') + (f" · {label}" if label else ""))
            lines = [(head, T_RUNS, INK)] + [(f"{m} {r['name']}", T_RUNS - 4, GREY)
                                             for m, r in zip(marks, runs)] + \
                    [(" · ".join(f"{n} {s}" for s, n in tally.most_common()) +
                      (" · nothing in their local result/" if quiet else ""), T_RUNS - 6, GREY)]
            fit = max(Drawing.measure(w, z) for w, z, _ in lines) + 2 * PAD + 8      # a list card as wide as its
            unrun = all(card_state(r) in ("ready", "proposed") for r in runs)        #   longest line; dashed only
            boxes.append((lines, min(RUN_W, max(RUN_W * 0.5, fit)), 1.5, unrun))      #   when none of it has run
        grid_rows, cur = [], []                                         # the grid, run_cols a row; a card with its
        per = 1 if detailed else run_cols(len([b for b in boxes if b[1] < RUN_WIDE]) or 1)   # plan (RUN_WIDE) takes
        for b in boxes:                                                 #   a row of its own (JL 261019: "一个 run 占
            if b[1] >= RUN_WIDE:                                        #   一行"), so one proposal no longer stretches
                grid_rows += [cur, [b]] if cur else [[b]]               #   every card of its Task (b01 j02 t02, 261019)
                cur = []
                continue
            cur.append(b)
            if len(cur) == per:
                grid_rows.append(cur)
                cur = []
        grid_rows += [cur] if cur else []
        for row in grid_rows:                                                # a row of the grid: as tall as its tallest
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

    # outside the frame, to its right: each Task's results, level with its step (the sketch's "T1 Results")
    d.fid = None
    first = len(d.els)
    place_results(d, f, width, steps, cfg, assets)
    for e in d.els[first:]:                 # the results follow ① when a builder lays frames out (canvas.grid,
        e.setdefault("customData", {})["follows"] = f["id"]   # d.acts), so they never stay behind (261014)
    return f


def results_layout(tops_wanted: list[float], hs: list[float], top: float, bottom: float, gap: float) -> list[float]:
    """Where each results block's top goes, in step order, no two overlapping. JL 261014: "以 job frame 的上下为界限
    … 最上面和最下面的 frame 可以超过 job frame 的最上和最下，但超出部分一定要对称、均匀". Taller together than the frame:
    one run of blocks, centred on it, so what rises above it equals what hangs below. Shorter: each as near its own
    step as it can be, and none past the frame's top or bottom."""
    total = sum(hs) + gap * (len(hs) - 1)
    if total >= bottom - top:
        y, out = (top + bottom) / 2 - total / 2, []
        for h in hs:
            out.append(y)
            y += h + gap
        return out
    out = []
    for want, h in zip(tops_wanted, hs):                                # down: level with its step, below the last
        out.append(max(want, top, out[-1] + hs[len(out) - 1] + gap if out else top))
    for k in range(len(out) - 1, -1, -1):                               # up: inside the frame's bottom
        out[k] = min(out[k], (out[k + 1] - gap if k + 1 < len(out) else bottom) - hs[k])
    return out


def results_lanes(links: list[tuple[float, float]]) -> dict[int, int]:
    """Each bent link's lane, left to right, between the frame and the results, so no two links cross. `links`, in
    step order: (the step's middle, where the link meets its block). Of two links, the earlier one's lane is left,
    unless both turn down: then it is right. Where no order keeps every pair, the fewest crossings."""
    down = [h > m for m, h in links]
    order: list[int] = []
    for k, (m, h) in enumerate(links):
        if abs(h - m) < 1:                                              # straight: no lane
            continue
        def crossed(i: int) -> int:                                     # pairs it would cross, put at i
            return sum((down[a] and down[k]) for a in order[:i]) + sum(not (down[a] and down[k]) for a in order[i:])
        order.insert(min(range(len(order) + 1), key=lambda i: (crossed(i), -i)), k)
    return {k: n for n, k in enumerate(order)}


def place_results(d: Drawing, f: dict, width: float, steps: list[dict], cfg: dict, assets: Path | None) -> None:
    """Each Task's results block, right of frame ①, joined to its step by a line. The blocks are as wide as the room
    allows (their panels side by side, up to RES_COLS a row), so together they stand about as tall as the frame
    (JL 261014: "我觉得你想想这个 results … 你到底想好去怎么 display 是非常重要的"); every other one steps right
    (错位); results_layout keeps them inside the frame's top and bottom, or over both by the same amount."""
    if not steps:
        return
    top, bottom = f["y"], f["y"] + f["height"]
    sizes = {c: [results_block(Drawing(), 0, 0, s["task"], cfg, s["found"], assets, s["thumb"], c)[:2]
                 for s in steps] for c in range(1, RES_COLS + 1)}       # measured at each width first
    tall = {c: sum(h for _, h in sz) + RES_VGAP * (len(sz) - 1) for c, sz in sizes.items()}
    cols = next((c for c in sorted(tall) if tall[c] <= bottom - top), min(tall, key=lambda c: (tall[c], c)))
    hs = [h for _, h in sizes[cols]]
    if sum(hs) + RES_VGAP * (len(hs) - 1) > SPILL * (bottom - top):    # one run would stand far past the frame:
        groups = results_columns(hs, SPILL * (bottom - top), RES_VGAP)  #   side-by-side columns instead (261014)
        if len(groups) > 1:
            return results_in_columns(d, f, width, steps, cfg, assets, cols, sizes[cols], groups)
    tops = results_layout([s["y"] for s in steps], hs, top, bottom, RES_VGAP)
    links = [(s["mid"], s["mid"] if y + 40 <= s["mid"] <= y + h - 40 else y + 40)   # level: straight; else it
             for s, y, h in zip(steps, tops, hs)]                       #   meets the block at its title
    lanes = results_lanes(links)
    x0 = width + LANE_X + LANE_W * len(lanes) + 60                      # right of the frame and its links' lanes
    for k, (s, y, (m, hit)) in enumerate(zip(steps, tops, links)):
        bx = x0 + (STAGGER if k % 2 else 0)                             # 错位: every other block a step right
        _, h, is_open = results_block(d, bx, y, s["task"], cfg, s["found"], assets, s["thumb"], cols)
        if k in lanes:                                                  # it bends: out, along its lane, in
            lx = width + LANE_X + LANE_W * lanes[k]
            pts = [(s["right"] + 10, m), (lx, m), (lx, hit), (bx - 12, hit)]
        else:                                                           # its step's middle meets its block: straight
            pts = [(s["right"] + 10, m), (bx - 12, m)]
        d.line(pts, sw=2, dashed=is_open)


def results_columns(hs: list[float], limit: float, gap: float) -> list[list[int]]:
    """The blocks, in step order, cut into the fewest columns whose tallest stands within `limit` (or within the
    tallest block, when one alone is taller); each cut so its tallest column is as short as it can be."""
    n, pre = len(hs), [0.0]
    for h in hs:
        pre.append(pre[-1] + h)

    def run(a: int, b: int) -> float:                                   # blocks a..b-1 stacked
        return pre[b] - pre[a] + gap * (b - a - 1)

    for m in range(1, n + 1):
        best = [[float("inf")] * (m + 1) for _ in range(n + 1)]
        cut = [[0] * (m + 1) for _ in range(n + 1)]
        best[0][0] = 0.0
        for i in range(1, n + 1):
            for k in range(1, min(m, i) + 1):
                for j in range(k - 1, i):
                    v = max(best[j][k - 1], run(j, i))
                    if v < best[i][k]:
                        best[i][k], cut[i][k] = v, j
        if best[n][m] <= max(limit, max(hs)):
            groups, i = [], n
            for k in range(m, 0, -1):
                groups.insert(0, list(range(cut[i][k], i)))
                i = cut[i][k]
            return groups
    return [[k] for k in range(n)]


def results_in_columns(d: Drawing, f: dict, width: float, steps: list[dict], cfg: dict, assets: Path | None,
                       cols: int, sizes: list[tuple[float, float]], groups: list[list[int]]) -> None:
    """Results too tall for one run beside ① (JL 261014: "这个 result 右边有这么多的空位你都不用，非要挤着那么一块"): its
    blocks in columns left to right, in step order, each column centred on ① so what rises above it equals what
    hangs below. The first column's links bend in lanes beside ① (results_lanes); a later column's link goes
    down beside ①, under the columns before it, and up the gap left of its own column, so no two links cross."""
    top, bottom = f["y"], f["y"] + f["height"]
    middle = (top + bottom) / 2
    hs = [h for _, h in sizes]
    tops = [0.0] * len(steps)
    for g in groups:                                                    # each column centred on ①
        y = middle - (sum(hs[k] for k in g) + RES_VGAP * (len(g) - 1)) / 2
        for k in g:
            tops[k] = y
            y += hs[k] + RES_VGAP
    hit = [min(max(steps[k]["mid"], tops[k] + 40), tops[k] + hs[k] - 40) for k in range(len(steps))]
    later = [k for g in groups[1:] for k in g]
    lanes = results_lanes([(steps[k]["mid"], hit[k]) for k in groups[0]])
    below = {k: width + LANE_X + LANE_W * (len(later) - 1 - i) for i, k in enumerate(later)}   # a lower step nearer ①
    x0 = width + LANE_X + LANE_W * (len(later) + len(lanes)) + 60
    floor = max(tops[k] + hs[k] for k in range(len(steps))) + 80        # under every column
    xs, x = {}, x0
    for c, g in enumerate(groups):
        if c:
            x += LANE_W * len(g)                                        # the lanes up into this column
        for p, k in enumerate(g):
            xs[k] = x + (STAGGER // 2 if p % 2 else 0)                  # 错位 inside a column
        x = max(xs[k] + sizes[k][0] for k in g) + COL_GAP
    for c, g in enumerate(groups):
        for p, k in enumerate(g):
            s, bx = steps[k], xs[k]
            _, h, is_open = results_block(d, bx, tops[k], s["task"], cfg, s["found"], assets, s["thumb"], cols)
            m = s["mid"]
            if c == 0 and p in lanes:                                   # first column: out, along its lane, in
                lx = width + LANE_X + LANE_W * (len(later) + lanes[p])
                pts = [(s["right"] + 10, m), (lx, m), (lx, hit[k]), (bx - 12, hit[k])]
            elif c == 0:
                pts = [(s["right"] + 10, m), (bx - 12, m)]
            else:                                                       # down, under the columns before, up its gap
                low = floor + 40 * later.index(k)
                gx = min(xs[q] for q in g) - 60 - LANE_W * (len(g) - 1 - p)
                pts = [(s["right"] + 10, m), (below[k], m), (below[k], low), (gx, low), (gx, hit[k]),
                       (bx - 12, hit[k])]
            d.line(pts, sw=2, dashed=is_open)


# ── ② the words it uses, how sure, what would close each open point: small, it explains ① ───────────────────
def has_notes(cfg: dict) -> bool:
    return bool(cfg.get("terms") or cfg.get("sure") or cfg.get("later") or
                any(isinstance(o, dict) and o.get("closer") for o in cfg.get("open") or []))


def notes_frame(d: Drawing, info: dict, cfg: dict, mark: str = "②") -> dict | None:
    """Asked by the reader review of 261013 ("neither one defines its terms … or says how to close what is open"): the
    face's `terms`, `sure` and `open` (with each `closer`), in a small frame stepped below and right of the staircase
    (canvas.explains), so its short labels decode."""
    if not has_notes(cfg):
        return None
    rest = "what is open" if cfg.get("open") else "what waits for later" if cfg.get("later") else "what is open"
    f = d.frame(f"{mark} 📖 {info['id']}: the words it uses, how sure, {rest}", NW)
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
    later = [o for o in cfg.get("later") or [] if o]
    if later:                               # an agreed topic's open points, moved to Later: plain, never red (the
        y += 24                             #   stage contract: agreed = no red ? and no open point; b31 s06-D07)
        d.text(40, y, "⏳ Later, and what would start it", 34)
        y += 66
        for o in later:
            item = o.get("item", "") if isinstance(o, dict) else str(o)
            y = d.para(40, y, f"⏳ {words(item, 25)}", NW - 80, 24, INK) + 2
            if isinstance(o, dict) and o.get("closer"):
                y = d.para(70, y, f"→ when: {words(o['closer'], 25)}", NW - 110, 24, GREY)
            y += 14
    canvas.explains(f)                    # small on purpose: it explains the staircase (JL 261013)
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
    _CHARTS.clear()
    job = job.resolve()
    design = jd.design_of(job.parent, cfg["design"]) if cfg.get("design") else {"grids": [], "tally": {}}
    cfg = {**cfg, "_tally": design["tally"], "_runs_word": str((cfg.get("design") or {}).get("runs_word") or "Runs")}
    cfg = expand_each(job, cfg)                                         # a family's picks, one per member Task
    rows = jr.job_rows(job.parent, job, {"show": cfg.get("show") or {}})
    tasks = [jd.task_info(r, {"show": cfg.get("show") or {}}) for r in rows]
    info = jd.job_info(job)
    d = Drawing()
    groups = step_groups(tasks, cfg)
    if any(st.get("members") and st.get("frame") == "in place" for st in groups):
        parts = story_segments(groups, cfg)    # a family in its place: its own staircase, never also a step in ①
    else:
        parts = split_steps(groups, cfg)                                # a big Job: two staircases, one story
    fams = [st for _, ss in parts for st in ss if st.get("members") and st.get("frame") is True]   # a family as its own
    MARKS = "①②③④⑤⑥⑦⑧⑨⑩"                                                 #   staircase (asked 261014: "we can make
    for i, fam in enumerate(fams):                                      #   them into different job frames")
        fam["detail_mark"] = MARKS[len(parts) + i]
    marks = iter(MARKS)
    def story_frame(k, title, steps):
        fam = steps[0] if len(steps) == 1 and steps[0].get("members") and steps[0].get("frame") == "in place" else None
        if fam:                                                         # a family in its place: its Tasks as steps,
            same = fam.get("question") or ""                            #   their shared question said once
            steps = [dict(m, question="" if (m.get("question") or "") == same else m.get("question"))
                     for m in fam["members"]]
        return ladder_frame(d, info, steps, cfg, jd.task_topics(job.parent), next(marks), out.parent / "assets",
                            part=title, cont=k > 0, last=k == len(parts) - 1, grouped=True)
    ladders = [story_frame(k, title, steps) for k, (title, steps) in enumerate(parts)]
    for fam in fams:                                                    # its Tasks as steps; the question they share
        same = fam.get("question") or ""                                #   is said once, in its key point
        members = [dict(m, question="" if (m.get("question") or "") == same else m.get("question"))
                   for m in fam["members"]]
        ladders.append(ladder_frame(d, info, members, cfg, jd.task_topics(job.parent), next(marks),
                                    out.parent / "assets", part=fam["title"], cont=True, last=False, grouped=True))
    ladder = ladders[0]
    notes = notes_frame(d, info, cfg, next(marks)) if has_notes(cfg) else None
    nxt = marks
    extra = [jd.design_frame(d, info, fr, design, next(nxt)) for fr in (cfg.get("design") or {}).get("frames") or []]
    if cfg.get("models"):
        extra.append(jd.matrix_frame(d, info, cfg["models"], job, next(nxt)))
    side = []                                                           # what the Runs found and what is left:
    if cfg.get("chart"):                                                #   beside the Runs' results, on the right
        side.append(jd.chart_frame(d, info, cfg["chart"], job.parent, out.parent / "assets", next(nxt)))
    if cfg.get("settings"):                                             #   (JL 261019: "It should be in the right
        side.append(jd.settings_frame(d, info, cfg["settings"], job.parent, next(nxt)))   # of the runs' results")
    folders = [t["row"]["task"] for t in tasks]
    pics = [p for p in jd.pictures(job) if not any(f in p.parents for f in folders)]   # a Task's are in its results
    if pics:
        extra.append(jd.shown_frame(d, info, pics, job))
    if cfg.get("detail") is True:
        extra.append(jd.detail_frame(d, info, tasks, jd.task_topics(job.parent), cfg, out.parent / "assets",
                                     next(nxt)))
    below = ladders[1:] + ([notes] if notes else []) + [x for x in extra if x]
    labels = ["continues"] * (len(parts) - 1) + [f"each Task: {f['title']}" for f in fams] + \
        (["its words"] if notes else []) + ["in detail"] * len(below)
    side = [x for x in side if x]
    order = [ladder["id"]] + [(x["id"], 600 if k == 0 else 420) for k, x in enumerate(below + side)]
    placed = canvas.stairs(d.els, order)[:1 + len(below)]
    right = max([ladder["x"] + ladder["width"]] + [e["x"] + e.get("width", 0) for e in d.els   # the results block
                 if not e.get("frameId") and e["type"] != "frame" and e["y"] < ladder["y"] + ladder["height"]
                 and e["x"] >= ladder["x"] + ladder["width"]])
    sy = ladder["y"]
    for f in side:                                                      # each in turn, top-aligned with ①
        dx, dy = right + 240 - f["x"], sy - f["y"]
        for e in d.els:
            if e["id"] == f["id"] or e.get("frameId") == f["id"] or (e.get("customData") or {}).get("follows") == f["id"]:
                e["x"], e["y"] = e["x"] + dx, e["y"] + dy
        sy += f["height"] + 160
    d.fid = None
    for f in side:                                                      # a named arrow from the results to it
        d.line([(right + 30, f["y"] + 80), (f["x"] - 14, f["y"] + 80)], sw=5)
        d.text(right + 40, f["y"] + 20, "what the Runs found" if f is (side[0] if cfg.get("chart") else None)
               else "each Run, and what is left", 30)
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
