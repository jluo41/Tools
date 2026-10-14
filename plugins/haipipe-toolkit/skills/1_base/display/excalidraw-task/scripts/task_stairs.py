"""A Task as a staircase, the same idea as excalidraw-job's (job_ladder.py): the Task's question on top, each Run or
video a step lower and further right in reading order, and each step's results outside the frame, small: charts,
its numbers as a table, its curves, its figures, a video's screenshots. A small frame explains it (words to know,
formulas, what to be ready to answer, what is open); a source's full transcript frames only when the face asks.

Asked 261013 (JL: "you should also think about how to update the /excalidraw-task as well, we try to follow the same
idea"), after the Job drawing became a staircase: "主次分明 … 一个很大的 frame，然后有一些小的 frame 是解释这些大的 frame
的", "一定要用阶梯状的结构 … 留出足够的空白", "你的 results 应该是图和表格呀", "你不能每一个都是朝左对齐".

    ① 🪜 t02 · its question (the main frame, large)
       🎯 the reading
       🧩 t02 · what it is · why it matters
        └─▶ ✅ r01 · first pass (grey once a Run is marked current)
              └─▶ ✅ r04 📌 · ⚙️ what it ran ───────────────────▶ 📊 its charts · its numbers · 📈 its curves
                    └─▶ ⬜ r05 · … ───────────────────────────────▶ 🖼️ a video's screenshots · say it
     └──▶ ② 📖 words to know · formulas · be ready to answer · open (small, canvas.explains)
            └──▶ ③ in detail: each source's transcript and full frame (detail: true)

Every word comes from the face's `task:` yaml or the Task page, every number from a Run's result, on every build. The
face's fields keep their meaning: `idea` (question, intro/what, why, terms, formula, questions), `runs.<rNN>` and
`videos.<rNN>` (name, says, config, show, plot, table, shots, hook, check, current), `order`, `reading`, `open`; and,
as excalidraw-job's, `charts: {<rNN>: [ … ]}`. `layout: rows` keeps the old frames.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parents[0].parent / "excalidraw-job" / "scripts"))
import task_drawing as td  # noqa: E402
import job_ladder as jl  # noqa: E402

jr, Drawing, canvas = td.jr, td.Drawing, td.canvas
INK, RED, GREY = jl.INK, jl.RED, jl.GREY
words, card, lines_h = jl.words, jl.card, jl.lines_h
PAD = jl.PAD
SHIFT, NODE_W, CARD_W, TASK_W = 380, 820, 660, 1100
STEP_GAP, RES_GAP, RES_W = 170, 220, 820
T_TITLE, T_TASK, T_STEP, T_CARD, T_RES = 64, 46, 34, 28, 26     # in the frame nothing under 28 px (⑦ for a Task)


def entry(cfg: dict, rid: str) -> dict:
    """The face's words for one source: `runs.<rid>` or `videos.<rid>`."""
    w = {**((cfg.get("videos") or {}).get(rid) or {}), **((cfg.get("runs") or {}).get(rid) or {})}
    return w if isinstance(w, dict) else {}


def first_sentence(s: str) -> str:
    return re.split(r"(?<=[.!?])\s+", str(s).strip())[0] if s else ""


# ── a step's results, outside the frame ──────────────────────────────────────────────────────────────────────
def results_block(d: Drawing, x: float, y: float, r: dict, w: dict, cfg: dict, assets: Path) -> tuple[float, bool]:
    """One source's results, small: charts (`charts: {<rid>: [...]}`, or the entry's `charts`), its `show` numbers
    as a table, its `plot` curves, the pictures its result holds; a video's screenshots (`shots`) and what to say.
    Returns (height, open): open, dashed, when it shows none of these."""
    cw = jl.CHART_W
    width = cw + 2 * PAD
    yy = d.para(x + PAD, y + PAD, f"📊 {r['rid'][:3] if re.match(r'^r\d\d_', r['rid']) else r['rid']} results",
                width - 2 * PAD, T_RES - 2, GREY) + 4
    shown = 0
    specs = list((cfg.get("charts") or {}).get(r["rid"]) or w.get("charts") or [])
    for k, spec in enumerate(specs[:3]):
        png = jl.chart_png(spec, r.get("result"), assets / f"chart-{r['rid']}-{k}.png") if r.get("result") else None
        if png:
            yy = d.para(x + PAD, yy, str(spec.get("title", "")), width - 2 * PAD, T_RES, INK) + 4
            yy += d.picture(png, x + PAD, yy, cw, 900, fid=f"chart-{r['rid']}-{k}") + 14
            shown += 1
    nums = td.picks_lines(r, w.get("show")) if r.get("result") and w.get("show") else []
    if nums and not shown:                                             # its numbers as a table, never a sentence
        rows = [{"cells": list(v.rsplit(" ", 1)) if " " in v else [v, ""], "dim": False} for v in nums]
        yy = d.grid_table(x + PAD, yy, ["", ""], rows, [cw * 0.62, cw * 0.38], T_RES, pad=22) + 10
        shown += 1
    for k, spec in enumerate((w.get("plot") or [])[:2]):               # its curves, as the Run logged them
        png = td.plot_png(r, spec, assets, k) if r.get("result") and isinstance(spec, dict) else None
        if png:
            yy = d.para(x + PAD, yy, f"📈 {spec.get('title', '')}", width - 2 * PAD, T_RES, INK) + 4
            yy += d.picture(png, x + PAD, yy, cw, 520, fid=f"plot-{r['rid']}-{k}") + 14
            shown += 1
    shots = td.shot_files(r, w, assets)[:2] if w.get("shots") else []   # two: results stay small beside the stairs
    for k, (png, cap) in enumerate(shots):                             # a video: what the screen showed
        yy += d.picture(png, x + PAD, yy, cw, 300, fid=f"shot-{r['rid']}-{k}") + 4
        yy = d.para(x + PAD, yy, cap, width - 2 * PAD, 22, GREY) + 12
        shown += 1
    if not shown and r.get("result") and Path(r["result"]).is_dir():   # the figures its Run already drew
        pics = [p for p in sorted(Path(r["result"]).rglob("*")) if p.suffix.lower() in (".png", ".jpg", ".jpeg")]
        for k, p in enumerate(pics[:2]):
            yy += d.picture(p, x + PAD, yy, cw, 560, fid=f"fig-{r['rid']}-{k}") + 4
            yy = d.para(x + PAD, yy, p.name, width - 2 * PAD, 20, GREY) + 12
            shown += 1
    if not shown and r.get("result") and Path(r["result"]).is_dir():   # no face words: what the Run says itself
        found = jr.found_values(r)
        if found:
            rows = [{"cells": list(v.rsplit(" ", 1)) if " " in v else [v, ""], "dim": False} for v in found[:6]]
            yy = d.grid_table(x + PAD, yy, ["", ""], rows, [cw * 0.62, cw * 0.38], T_RES, pad=22) + 10
            shown += 1
        else:
            said = jl.headline(Path(r["result"]), 24) or jl.holds(Path(r["result"]))
            if said:
                yy = d.para(x + PAD, yy, said if said.startswith("📂") else f"“{said}”", width - 2 * PAD, T_RES,
                            GREY if said.startswith("📂") else INK) + 8
                shown += 1
    hook = w.get("hook") or r.get("hook")
    if hook and shown:
        yy = d.para(x + PAD, yy, f"🎤 {words(hook, 20)}", width - 2 * PAD, T_RES, INK) + 6
    checks = w.get("check") or ([first_sentence(r["check"])] if r.get("check") else [])
    for c in checks[:2]:                                               # what to confirm against the source, in red
        yy = d.para(x + PAD, yy, f"❓ {words(c, 12)}", width - 2 * PAD, T_RES - 2, RED) + 4
    if r.get("url"):
        yy = d.para(x + PAD, yy, f"🔗 {r['url']}", width - 2 * PAD, 22, GREY) + 4
    is_open = not (shown or checks)
    if is_open:
        yy = d.para(x + PAD, yy, "❓ nothing to show yet" if r.get("result") else "⬜ no result on disk",
                    width - 2 * PAD, T_RES, RED if r.get("result") else GREY) + 8
    h = yy - y + PAD - 8
    d.box(x, y, width, h, GREY if is_open else INK, 1.5, dashed=is_open)
    return h, is_open


# ── ① the staircase ──────────────────────────────────────────────────────────────────────────────────────────
def stairs_frame(d: Drawing, task: dict, folder: Path, runs: list, cfg: dict, assets: Path) -> dict:
    idea = cfg.get("idea") or {}
    tid = folder.name[:3]
    noun = "Run" if task.get("work") or any(r.get("work") for r in runs) else "video"
    cols = jl.columns(len(runs))
    title = f"🪜 {tid} · {task['title']}"
    width = max(130 + max(cols, default=0) * SHIFT + NODE_W + 60, 40 + TASK_W + 60,
                Drawing.measure(title, T_TITLE) + 760)                 # the title and the badge side by side
    f = d.frame(f"① {title}: its {noun}s as steps", width)
    Drawing.room(f)
    if width > canvas.FRAME_MAX[0]:
        canvas.large(f)
    d.text(40, 22, title, T_TITLE)
    states = jl.jd.states([{"state": r.get("state") or "?"} for r in runs]) if runs else f"no {noun} yet"
    d.para(40, 112, f"{folder.parent.name} · {jl.jd.n_of(len(runs), noun)}: {states}", width - 80, T_CARD, GREY)
    y = 180
    reading = str(cfg.get("reading") or idea.get("question") or task.get("question") or "")
    key = f"🎯 {words(reading, 45)}" if reading else "❓ no reading yet: write the face's task.reading"
    kh = Drawing.height(key, width - 140, 34) + 44
    d.key(40, y, width - 80, kh)
    d.para(70, y + 22, key, width - 140, 34)
    y += kh + 80

    # the top step: the Task, what it is and why it matters
    th = card(d, 40, y, TASK_W, [(f"🧩 {tid} · {task['title']}", T_TASK, INK)], sw=3)
    what = idea.get("intro") or idea.get("what") or task.get("what") or ""
    why = idea.get("why") or task.get("why") or ""
    under = [(f"What it is: {words(first_sentence(what), 30)}" if what else "", T_CARD, INK),
             (f"Why it matters: {words(first_sentence(why), 30)}" if why else "", T_CARD, INK)]
    ch = card(d, 110, y + th + 20, TASK_W - 110, under) if any(s for s, _, _ in under) else 0
    spine_x, spine_top = 60, y + th
    y = y + th + 20 + ch + STEP_GAP

    marked = any(entry(cfg, r["rid"]).get("current") for r in runs)
    steps = []
    for r, col in zip(runs, cols):
        w = entry(cfg, r["rid"])
        nx = 130 + col * SHIFT
        now = bool(w.get("current"))
        quiet = marked and not now                                     # a rerun the current Run replaces: its name
        name = w.get("name") or r.get("short") or r["rid"]
        rid = r["rid"][:3] if re.match(r"^r\d\d_", r["rid"]) else r["rid"]      # a work Run's folder: its number
        label = f"{jr.mark(r.get('state') or '?')} {rid} · {name}{'  📌 current' if now else ''}"
        if r.get("star"):
            label += " ★"
        nh = card(d, nx, y, NODE_W - (160 if quiet else 0), [(label, T_STEP - (6 if quiet else 0), GREY if quiet else INK)],
                  sw=1 if quiet else (2.5 if now else 1.8))
        lines = []
        if not quiet:
            says = w.get("says") or first_sentence(r.get("summary") or "")
            lines.append((words(says, 22) if says else "", T_CARD, INK))
            for c in (td.picks_lines(r, w.get("config")) if r.get("result") and w.get("config") else [])[:3]:
                lines.append((f"⚙️ {c}", T_CARD, INK))
        cardh = card(d, nx + 36, y + nh + 14, CARD_W, lines) + 14 if any(s for s, _, _ in lines) else 0
        mid = y + nh / 2
        d.line([(spine_x, mid), (nx - 8, mid)], sw=3)
        lead = f"then {r['rid']}: {w['role']}" if w.get("role") else td.role(task, r["rid"])
        if steps and not quiet and ":" in lead:                        # what this source does in the reading order
            d.para(nx, y - 48, words(lead, 9), NODE_W, T_CARD, GREY)
        steps.append({"y": y, "mid": mid, "right": nx + NODE_W - (160 if quiet else 0), "r": r, "w": w,
                      "quiet": quiet})
        res_h = 0 if quiet else results_block(Drawing(), 0, 0, r, w, cfg, assets)[0]   # measured, so the step stays
        y = max(y + nh + 14 + cardh, y + res_h) + (STEP_GAP // 2 if quiet else STEP_GAP)   # level with its results
    if steps:
        d.line([(spine_x, spine_top), (spine_x, steps[-1]["mid"])], arrow=False, sw=3)

    opens = [str(o.get("item") if isinstance(o, dict) else o) for o in (cfg.get("open") or []) if o]
    y -= STEP_GAP - 60
    if opens:
        y = d.para(40, y, f"❓ {jl.jd.n_of(len(opens), 'point')} still open: they are in the frame below", width - 80,
                   T_CARD, RED) + 8
    said = sum(Drawing.words_in(e.get("text", "")) for e in d.els if e.get("frameId") == f["id"] and e["type"] == "text")
    if said > jl.jd.MAP_WORDS:
        Drawing.detail(f)
    f["height"] = max(y + 40, 600)
    if f["height"] > canvas.FRAME_MAX[1]:
        canvas.reads_down(f)
    d.fid = f["id"]
    d.badge(f)

    # outside the frame, to its right: each step's results, small, level with it (a quiet rerun shows none)
    d.fid = None
    rx0, last = width + RES_GAP, -1e9
    for s in steps:
        if s["quiet"]:
            continue
        top = max(s["y"], last + 40)
        h, is_open = results_block(d, rx0, top, s["r"], s["w"], cfg, assets)
        hit = top + 32
        pts = [(s["right"] + 10, s["mid"]), (width + 60, s["mid"])] + \
              ([(width + 60, hit)] if abs(hit - s["mid"]) > 4 else []) + [(rx0 - 12, hit)]
        d.line(pts, sw=2, dashed=is_open)
        last = top + h
    return f


# ── ② the words, formulas and open points: small, it explains ① ─────────────────────────────────────────────
def notes_frame(d: Drawing, task: dict, cfg: dict, assets: Path) -> dict | None:
    idea = cfg.get("idea") or {}
    terms = [t for t in idea.get("terms") or [] if isinstance(t, dict) and t.get("term")]
    formulas = [x for x in idea.get("formula") or [] if isinstance(x, dict) and x.get("tex")]
    qs = idea.get("questions") or task.get("questions") or []
    opens = [o for o in cfg.get("open") or [] if o]
    if not (terms or formulas or qs or opens):
        return None
    W = 1200
    f = d.frame("② 📖 the words it uses, its formulas, what is open", W)
    Drawing.room(f)
    y = 22
    if terms:
        d.text(40, y, "📖 Words to know", 40)
        y += 80
        for t in terms[:10]:
            y = d.para(40, y, str(t["term"]), W - 80, 28) + 2
            y = d.para(70, y, words(t.get("means", ""), 25), W - 110, 24) + 14
    for fm in formulas[:2]:
        y += 16
        d.text(40, y, f"🧮 {fm.get('name', '')}", 34)
        y += 56
        png = td.tex_png(str(fm["tex"]), assets)
        if png:
            y += d.picture(png, 40, y, W - 80, 160, fid=f"tex-{abs(hash(fm['tex'])) % 10**8}") + 8
        y = d.para(40, y, words(fm.get("means", ""), 30), W - 80, 24) + 14
    if qs:
        y += 16
        d.text(40, y, "🎤 Be ready to answer", 34)
        y += 56
        for q in qs[:4]:
            q = q.get("q", "") if isinstance(q, dict) else str(q)
            y = d.para(40, y, f"· {words(q, 14)}", W - 80, 24) + 8
    if opens:
        y += 16
        d.text(40, y, "❓ What is open", 34, RED)
        y += 56
        for o in opens:
            item = o.get("item", "") if isinstance(o, dict) else str(o)
            y = d.para(40, y, f"❓ {words(item, 25)}", W - 80, 24, RED) + 2
            if isinstance(o, dict) and o.get("closer"):
                y = d.para(70, y, f"→ close by: {words(o['closer'], 25)}", W - 110, 24, INK)
            y += 12
    canvas.explains(f)
    f["height"] = max(y + 40, 600)
    if f["height"] > canvas.FRAME_MAX[1]:
        canvas.reads_down(f)
    return f


# ── the drawing ──────────────────────────────────────────────────────────────────────────────────────────────
def draw_task(folder: Path, out: Path, cfg: dict | None = None, source: str = "") -> tuple[Path, list[dict]]:
    """① the staircase, ② its words, small; with `detail: true`, each source's transcript and full frame after
    them ("in detail"). The frames after ① step down and to the right of it (canvas.stairs)."""
    cfg = cfg or {}
    task = td.parse(td.task_page(folder))
    runs = td.reading_order(task, cfg.get("order"))
    for r in runs:                                     # the face's state wins: a crash its receipt calls completed
        if entry(cfg, r["rid"]).get("state"):
            r["state"] = str(entry(cfg, r["rid"])["state"])
    d = Drawing()
    assets = out.parent / "assets"
    main = stairs_frame(d, task, folder, runs, cfg, assets)
    notes = notes_frame(d, task, cfg, assets)
    extra = []
    if cfg.get("detail") is True:                      # the old full frames, read up close, only when asked
        for r in runs:
            w = entry(cfg, r["rid"])
            bd = None if r.get("work") else td.board_frame(d, r, w, assets)
            t = None if r.get("work") else td.transcript_frame(d, r, w, assets)
            extra += [x for x in (bd, t) if x] + [td.source_frame(d, r, w, assets, True, passages=t is None)]
    below = ([notes] if notes else []) + extra
    placed = canvas.stairs(d.els, [main["id"]] + [(x["id"], 600 if k == 0 else 420) for k, x in enumerate(below)])
    d.fid = None
    for k, (a, b) in enumerate(zip(placed, placed[1:])):
        x = b["x"] + min(b["width"], 600) / 2
        d.line([(x, a["y"] + a["height"] + 14), (x, b["y"] - 14)], sw=5)
        d.text(x + 20, (a["y"] + a["height"] + b["y"]) / 2 - 24, "its words" if (k == 0 and notes) else "in detail", 36)
    d.write(out, source or f"excalidraw-task scripts/task_stairs.py {folder.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out, runs


if __name__ == "__main__":                                              # python task_stairs.py <task> <out.excalidraw>
    draw_task(Path(sys.argv[1]), Path(sys.argv[2]))
