"""r01's option previews for s57 · Task UI: Report (JL 261031: "propose different UI's view list and view's
subsection ... make detailed interaction"): one small page per option, drawn in the workbench's own look (its real
focus.css inlined), so each option shows its screen; the part an option changes carries class="diff", which the form
boxes in orange.

Two Tasks are drawn:
  - a soft-Run Task, real: b35's j01_studio_delivery_type/t01_skill_section, its run-write-skill-section and its pass
    p01-1030, and the haipipe-studio SKILL.md section that pass wrote, all read from disk on each build;
  - a hard-Run Task with placeholder names and values (t01_fit_model, r01 to r05), since no public Tools Task holds a
    hard Run with a result/ yet (b17's own Tasks hold soft Runs only). Its values are placeholders (0.7x, x,xxx).

The form shows a preview at half size in a frame 600 page pixels tall, so what differs sits in that height: no Aim
line and no right rail (no option changes them), compact rows with a hard Run's small table on the right (as a
kid-row's picture), and two places side by side when an option moves something between them.

Writes runs/r01_collect_task_report_views/option-q<N>-<k>.html; question_collection.md links each one under its
option. Rerun after changing anything here, never edit the pages:

    python build_r01_previews.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]                       # t03_task_page
RUN = TASK / "runs" / "r01_collect_task_report_views"
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
STUDIO_SKILL = TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/SKILL.md"
B35_TASK = TOOLS / "blueprints/Project-PageParts/work/b35_studio/j01_studio_delivery_type/t01_skill_section"
B35_RUN = B35_TASK / "runs" / "run-write-skill-section"

CAPTIONS = {"MindMap": "The Task as a map: its aim, its topics, and what each Run found.",
            "type": "What this Task makes, one row per Run: the thing itself, its version, its parts.",
            "Display": "The charts its figures Runs drew, one row per Run."}
ROLES =(("make", "🔨 make"), ("fix", "🔁 fix"), ("check", "🔎 check"), ("describe", "📋 describe"),
         ("figures", "📊 figures"), ("evidence", "🧾 evidence"), ("publish", "📤 publish"), ("trial", "🧪 trial"))

# ── the hard-Run Task: placeholder names and values ──────────────────────────────────────────────────────────────
FIT = {"name": "t01_fit_model", "title": "Fit the model on each fold",
       "crumb": "Project-Demo / work / b01_demo / j01_fit / t01_fit_model",
       "aim": "One fit per fold of the Job's data version.",
       "close": "Every fold has a done Run and its audit passes."}


def fold_table(fold: str) -> list:
    return [("metric", fold), ("score", "0.7x"), ("rows", "x,xxx")]


RUNS = [
    {"run": "r02_fit_fold00", "role": "make", "word": "r02", "fold": "fold00",
     "line": "fold00: score 0.7x on x,xxx rows; no row dropped.", "table": fold_table("fold00"),
     "tags": ["RUN-REPORT", "Tables"]},
    {"run": "r03_fit_fold01", "role": "make", "word": "r03", "fold": "fold01",
     "line": "fold01: score 0.7x on x,xxx rows; no row dropped.", "table": fold_table("fold01"),
     "tags": ["RUN-REPORT", "Tables"]},
    {"run": "r04_audit_folds", "role": "check", "word": "r04",
     "line": "Both folds pass the row and field checks.",
     "table": [("check", "fold00", "fold01"), ("rows match the split", "pass", "pass"),
               ("fields in range", "pass", "pass")], "tags": ["RUN-REPORT", "Tables"]},
    {"run": "r05_figures_folds", "role": "figures", "word": "r05",
     "line": "Two charts: score by fold, calibration by fold.", "charts": True, "tags": ["Figures"]},
    {"run": "r01_smoke_fit", "role": "trial", "word": "r01",
     "line": "200 rows ran end to end; every output file written.",
     "table": [("check", "result"), ("rows", "200"), ("files written", "all")], "tags": ["RUN-REPORT"]},
]
NEWEST_MAKE = RUNS[1]                                             # r03_fit_fold01: the newest make Run
REPORT_SECTIONS = {                                               # each make Run's RUN-REPORT.md, its sections
    "fold00": [("Data", "The frozen fold00 split of the Job's data version; x,xxx rows, none dropped."),
               ("Method", "One fit with this Run's config.yaml; its seed is fixed."),
               ("Result", "fold00 scores 0.7x; its calibration slope is 0.9x.")],
    "fold01": [("Data", "The frozen fold01 split of the Job's data version; x,xxx rows, none dropped."),
               ("Method", "One fit with this Run's config.yaml; its seed is fixed."),
               ("Result", "fold01 scores 0.7x; its calibration slope is 0.9x.")],
}

PREVIEW_CSS = """
/* preview only: the page without its fixed rails (no option changes them) */
.focus-page.pv{max-width:960px;padding:14px 22px 30px}.pv h1{margin:6px 0 8px}
.ph{font-size:11px;color:#b35c00;margin-left:8px}
.pv .section-views{flex-wrap:wrap;gap:6px}
.pv .section-views span{font-size:13px;border:1px solid var(--line);border-radius:6px;padding:3px 11px;color:var(--muted)}
.pv .section-views span.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .view-caption{margin:0 0 8px;font-size:13px;color:var(--muted)}
.screens{display:grid;grid-template-columns:1fr;gap:14px;align-items:start;margin-top:10px}
.screen{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--paper);min-width:0}
.screen-title{font-size:15px;font-weight:700;margin:0 0 6px}.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:13px}
.screen .section-views{gap:5px;margin:0 0 6px}.screen .section-views span{font-size:11px;padding:1px 7px}
.screen .view-caption{font-size:11.5px;margin:0 0 6px}
.role-h{font-size:11.5px;font-weight:600;letter-spacing:.03em;color:var(--muted);margin:8px 0 4px}
.rs:first-child .role-h{margin-top:0}
.rr{border:1px solid var(--line);border-radius:10px;padding:7px 11px;margin:0 0 6px;background:var(--paper)}
.rr.side{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 18px;align-items:start}
.rr-thing{margin-top:2px}
.rr-head{display:flex;align-items:baseline;gap:8px}.rr-head b{font-size:13.5px}
.rr-word{margin-left:auto;font-size:11.5px;border:1px solid var(--line);border-radius:9px;padding:0 8px;color:var(--muted)}
.rr-line{font-size:12.5px;margin:1px 0 3px}
.rr-body{margin:4px 0 2px}
.rr-tags{display:flex;gap:6px;margin-top:4px}.rr-tags span{font-size:11.5px;border:1px solid var(--line);border-radius:7px;padding:0 8px}
.tbl{font-size:11px;border-collapse:collapse;display:table!important}.tbl td,.tbl th{padding:1px 10px 1px 0;border-bottom:1px solid var(--line);text-align:left;font-weight:400}
.tbl th{color:var(--muted)}
.charts{display:flex;gap:8px}.charts svg{display:block;border:1px solid var(--line);border-radius:5px;background:#fff}
.doc{border:1px solid var(--line);border-radius:6px;padding:7px 10px;font-size:12px;background:var(--bg);margin:2px 0}
.doc-file{font:11px ui-monospace,Menlo,monospace;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:3px;margin-bottom:5px}
.doc h4{margin:0 0 3px;font-size:13px}.doc h5{margin:6px 0 1px;font-size:11.5px}.doc p{margin:0 0 4px}
.doc ul{margin:0 0 4px;padding-left:18px}.doc code{font-size:10.5px}
.one{display:flex;gap:10px;align-items:baseline;padding:5px 0;border-bottom:1px solid var(--line);font-size:12.5px}
.one b{font-size:12.5px;min-width:140px}.one .mut{margin-left:auto}
.away{font-size:12px;color:var(--muted);margin:8px 0 0}
.mm{display:grid;grid-template-columns:180px minmax(0,1fr);gap:0 22px;align-items:center;border:1px solid var(--line);border-radius:10px;padding:12px;background:var(--paper)}
.mm-root{border:1.5px solid var(--ink);border-radius:10px;padding:8px 10px}
.mm-root b{display:block;font-size:13px;margin:4px 0 0}.mm-root p{margin:4px 0 0;font-size:11px;color:var(--muted);line-height:1.45}
.mm-br{border-left:1.5px solid var(--line);padding-left:14px;display:flex;flex-direction:column;gap:6px}
.mm-g{display:grid;grid-template-columns:118px minmax(0,1fr);gap:0 12px;align-items:start}
.mm-gn{border:1px solid var(--line);border-radius:8px;padding:3px 7px;font-size:11.5px;font-weight:600;margin-top:1px;overflow-wrap:anywhere}
.mm-leaf{margin:0 0 5px}.mm-leaf:last-child{margin:0}
.mm-pill{display:inline-block;font-size:10.5px;border-radius:9px;padding:0 7px;background:var(--soft);color:var(--accent);font-weight:600;margin-right:6px}
.mm-t{font-size:12px;font-weight:600}
.mm-box{margin:2px 0 0;padding:4px 8px;background:var(--wash);border-radius:6px;font-size:11px;line-height:1.45}
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


def inline_md(text: str) -> str:
    """A line of Markdown, escaped, with `code` and **bold**."""
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)


# ── the soft-Run Task, read from disk ────────────────────────────────────────────────────────────────────────────
def field(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.+)$", text)
    return m.group(1).strip() if m else ""


def md_part(text: str, name: str) -> str:
    """One `## <name>` part of a pass.md, as its lines joined."""
    m = re.search(rf"(?ms)^##\s+{re.escape(name)}\s*\n(.*?)(?=^##\s|\Z)", text)
    return " ".join(line.strip() for line in m.group(1).strip().splitlines()) if m else ""


def soft_task() -> dict:
    face = (B35_TASK / f"{B35_TASK.name}.md").read_text(encoding="utf-8")
    card = (B35_RUN / "run.yaml").read_text(encoding="utf-8")
    passes = re.findall(r"(?m)^-\s*(p\d+-\d{4})\s*$", card)
    newest = passes[-1] if passes else ""
    pass_md = (B35_RUN / "passes" / newest / "pass.md").read_text(encoding="utf-8") if newest else ""
    skill = STUDIO_SKILL.read_text(encoding="utf-8")
    block = re.search(r"(?s)<!-- render b35-s01 one-delivery:.*?-->\n(.*?)<!-- /render b35-s01 one-delivery -->", skill)
    lines = [line for line in (block.group(1) if block else "").splitlines()]
    heading = next((line.strip() for line in lines if line.strip()), "")
    paras, cur = [], []
    for line in lines[lines.index(heading) + 2:] if heading in lines else []:   # past the heading and its underline
        if line.strip():
            cur.append(line.strip())
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    if cur:
        paras.append(" ".join(cur))
    writes = re.findall(r"(?m)^-\s*(\S+SKILL\.md)\s*$", card)
    return {"name": B35_TASK.name, "title": face.splitlines()[0].split(" · ", 1)[-1].strip(),
            "crumb": "Tools-SPACE / blueprints / Project-PageParts / work / b35_studio / j01_studio_delivery_type / "
                     + B35_TASK.name,
            "aim": field(face, "goal"), "close": field(face, "close"), "run": B35_RUN.name, "pass": newest,
            "pass_title": (pass_md.splitlines()[0].lstrip("# ").strip() if pass_md else ""),
            "ask": md_part(pass_md, "Ask"), "summary": md_part(pass_md, "Summary"),
            "changed": [c.strip("- `") for c in md_part(pass_md, "Changed").split(" - ")],
            "file": writes[0] if writes else "SKILL.md", "heading": heading, "paras": paras[:2]}


# ── the page and its parts ───────────────────────────────────────────────────────────────────────────────────────
def views(names: list, on: str, mark: bool = False) -> str:
    buttons = "".join(f'<span class="{"on" if n == on else ""}">{esc(n)}</span>' for n in names)
    return f'<nav class="section-views{diff(mark)}" aria-label="Views">{buttons}</nav>'


def page(title: str, task: dict, body: str, *, bar: str = "", caption: str = "", heading: bool = True,
         placeholder: bool = False) -> str:
    """One preview page: the path, then (heading) the title with its section, its view buttons and the caption."""
    note = '<span class="ph">placeholder names and values</span>' if placeholder else ""
    top = (f'<h1>{esc(task["name"])}<span class="h1-section">Report</span></h1>{bar}'
           + (f'<p class="view-caption">{esc(caption)}</p>' if caption else "")) if heading else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            f"<body><main class=\"focus-page pv\"><div class=\"focus-crumb\">{esc(task['crumb'])}{note}</div>"
            f"{top}{body}</main></body></html>")


def screen(task: dict, view_names: list, on: str, inner: str, *, caption: str = "", mark: bool = False,
           mark_bar: bool = False) -> str:
    """One view of the page drawn small, so two can sit side by side."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">{esc(task["name"])}<span>Report · '
            f'{esc(on)}</span></div>{views(view_names, on, mark_bar)}{cap}{inner}</section>')


def table(rows: list) -> str:
    head, *body = rows
    return ('<table class="tbl"><tr>' + "".join(f"<th>{esc(c)}</th>" for c in head) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in body) + "</table>")


def charts(big: bool = False) -> str:
    """The figures Run's two charts, drawn as plain placeholder shapes."""
    w, h = (210, 120) if big else (128, 73)
    bars = (f'<svg width="{w}" height="{h}" viewBox="0 0 150 86" aria-label="score by fold">'
            '<text x="6" y="12" font-size="8" fill="#6f6f6b">score by fold</text>'
            '<rect x="30" y="26" width="34" height="48" fill="#1864ab"/><rect x="84" y="30" width="34" height="44" fill="#74a9d8"/>'
            '<line x1="20" y1="74" x2="136" y2="74" stroke="#adb5bd"/>'
            '<text x="34" y="83" font-size="7" fill="#6f6f6b">fold00</text><text x="88" y="83" font-size="7" fill="#6f6f6b">fold01</text></svg>')
    cal = (f'<svg width="{w}" height="{h}" viewBox="0 0 150 86" aria-label="calibration by fold">'
           '<text x="6" y="12" font-size="8" fill="#6f6f6b">calibration by fold</text>'
           '<line x1="20" y1="76" x2="136" y2="18" stroke="#ced4da" stroke-dasharray="3 3"/>'
           '<polyline points="20,74 50,62 80,46 110,33 136,22" fill="none" stroke="#1864ab" stroke-width="1.6"/>'
           '<polyline points="20,76 50,60 80,49 110,30 136,20" fill="none" stroke="#74a9d8" stroke-width="1.6"/></svg>')
    return f'<div class="charts">{bars}{cal}</div>'


def tags(names: list) -> str:
    return '<nav class="rr-tags">' + "".join(f"<span>{esc(n)}</span>" for n in names) + "</nav>"


def row(r: dict, mode: str = "thing", mark: bool = False, big: bool = False) -> str:
    """A hard Run's row. mode: "thing" (its first table, or its charts, small, on the right), "report" (its
    RUN-REPORT.md whole, in place, under its line), "none" (its line only); its tags under its line every time."""
    head = f'<header class="rr-head"><b>{esc(r["run"])}</b><span class="rr-word">{esc(r["word"])}</span></header>'
    text = f'{head}<p class="rr-line">{esc(r["line"])}</p>'
    if mode == "thing" and big and r.get("charts"):        # a view of its own (Display): the charts large, under it
        return (f'<article class="rr{diff(mark)}">{text}<div class="rr-body">{charts(True)}</div>'
                f'{tags(r["tags"])}</article>')
    if mode == "thing":
        thing = charts(big) if r.get("charts") else table(r["table"]) if r.get("table") else ""
        return (f'<article class="rr side{diff(mark)}"><div>{text}{tags(r["tags"])}</div>'
                f'<div class="rr-thing">{thing}</div></article>')
    body = f'<div class="rr-body">{run_report(r)}</div>' if mode == "report" and "fold" in r else ""
    return f'<article class="rr{diff(mark)}">{text}{body}{tags(r["tags"])}</article>'


def by_role(runs: list, mode: str = "thing", mark_roles: tuple = (), big: bool = False) -> str:
    """The rows in role sections, make first and trial last, a heading each."""
    out = ""
    for role, label in ROLES:
        mine = [r for r in runs if r["role"] == role]
        if mine:
            out += (f'<section class="rs{diff(role in mark_roles)}"><h3 class="role-h">{esc(label)}</h3>'
                    + "".join(row(r, mode, big=big) for r in mine) + "</section>")
    return out


def run_report(r: dict, compact: bool = False) -> str:
    """A make Run's result/RUN-REPORT.md, rendered (placeholder words)."""
    parts = REPORT_SECTIONS[r["fold"]]
    other = next(x["run"] for x in RUNS if x.get("fold") and x["fold"] != r["fold"])
    sections = "".join(f"<h5>{esc(name)}</h5><p>{esc(words)}</p>" for name, words in parts[:2])
    return (f'<div class="doc"><div class="doc-file">{esc(r["run"])} · result/RUN-REPORT.md</div>'
            f'<h4>{esc(r["run"])} · Run report</h4><p><b>Headline.</b> {esc(r["line"])}</p>{sections}'
            f'<h5>Result</h5>{table(r["table"])}'
            + ("" if compact else f'<h5>Caveats</h5><p>One fold; the other is {esc(other)}.</p>') + "</div>")


def one_line(r: dict) -> str:
    label = dict(ROLES)[r["role"]]
    return (f'<div class="one"><b>{esc(r["run"])}</b><span>{esc(r["line"])}</span>'
            f'<span class="mut">{esc(label)} · {esc(r["word"])}</span></div>')


# ── the map ──────────────────────────────────────────────────────────────────────────────────────────────────────
def mm_root(task: dict) -> str:
    return (f'<div class="mm-root"><span class="mm-pill">{esc(task["name"])}</span><b>{esc(task["title"])}</b>'
            f'<p>Aim: {esc(task["aim"])} Close: {esc(task["close"])}</p></div>')


def mm_leaf(pill: str, title: str, box: str) -> str:
    """A map point as the draft map draws one: its pill, its short title (none when the pill says it), its box."""
    return (f'<div class="mm-leaf"><span class="mm-pill">{esc(pill)}</span>'
            + (f'<span class="mm-t">{esc(title)}</span>' if title else "") + f'<p class="mm-box">{esc(box)}</p></div>')


def mindmap_runs(task: dict, runs: list, mark: bool = False) -> str:
    groups = ""
    for role, label in ROLES:
        mine = [r for r in runs if r["role"] == role]
        if mine:
            groups += (f'<div class="mm-g"><div class="mm-gn">{esc(label)}</div><div>'
                       + "".join(mm_leaf(r["word"], r["run"], r["line"]) for r in mine) + "</div></div>")
    return f'<div class="mm">{mm_root(task)}<div class="mm-br{diff(mark)}">{groups}</div></div>'


def mindmap_content(task: dict, runs: list, mark: bool = False) -> str:
    groups = ""
    for r in (x for x in runs if x["role"] == "make"):
        groups += (f'<div class="mm-g"><div class="mm-gn"><span class="mm-pill">{esc(r["word"])}</span>'
                   f'{esc(r["run"])}</div><div>'
                   + "".join(mm_leaf(name, "", words) for name, words in REPORT_SECTIONS[r["fold"]])
                   + "</div></div>")
    return f'<div class="mm">{mm_root(task)}<div class="mm-br{diff(mark)}">{groups}</div></div>'


# ── the soft-Run row ─────────────────────────────────────────────────────────────────────────────────────────────
def section_doc(s: dict) -> str:
    """The SKILL.md section the soft Run wrote, as it reads now."""
    paras = "".join(f"<p>{inline_md(p)}</p>" for p in s["paras"])
    return (f'<div class="doc"><div class="doc-file">haipipe-studio · SKILL.md</div><h4>{esc(s["heading"])}</h4>'
            f'{paras}</div>')


def pass_doc(s: dict) -> str:
    """Its newest pass, passes/<pass>/pass.md."""
    changed = "".join(f"<li><code>{esc(c)}</code></li>" for c in s["changed"] if c)
    return (f'<div class="doc"><div class="doc-file">{esc(s["run"])} · passes/{esc(s["pass"])}/pass.md</div>'
            f'<h4>{esc(s["pass_title"])}</h4><h5>Ask</h5><p>{esc(s["ask"])}</p>'
            f'<h5>Changed</h5><ul>{changed}</ul></div>')


def soft_row(s: dict, mode: str) -> str:
    """mode: "thing" (the section), "pass" (its newest pass), "both"."""
    body = {"thing": section_doc(s), "pass": pass_doc(s), "both": section_doc(s) + pass_doc(s)}[mode]
    names = ["SKILL.md", s["pass"], "Ticket"] if mode != "pass" else ["SKILL.md", "Ticket"]
    head = f'<header class="rr-head"><b>{esc(s["run"])}</b><span class="rr-word">{esc(s["pass"])}</span></header>'
    return (f'<article class="rr diff">{head}<p class="rr-line">{esc(s["summary"])}</p>'
            f'<div class="rr-body">{body}</div>{tags(names)}</article>')


# ── the previews ─────────────────────────────────────────────────────────────────────────────────────────────────
def previews() -> dict:
    out = {}
    type_view = dict(bar=views(["MindMap", "Data"], "Data"), caption=CAPTIONS["type"], placeholder=True)

    # Q1 · the view list: one type view with the charts inside it, or Data and Display side by side
    out["q1-a"] = page("Q1 A", FIT, by_role(RUNS, mark_roles=("figures",)),
                       bar=views(["MindMap", "Data"], "Data", mark=True), caption=CAPTIONS["type"], placeholder=True)
    names = ["MindMap", "Data", "Display"]
    out["q1-b"] = page("Q1 B", FIT, '<div class="screens">'
                       + screen(FIT, names, "Data", by_role([r for r in RUNS if r["role"] != "figures"]),
                                caption=CAPTIONS["type"], mark_bar=True)
                       + screen(FIT, names, "Display", by_role([r for r in RUNS if r["role"] == "figures"], big=True),
                                caption=CAPTIONS["Display"], mark=True, mark_bar=True)
                       + "</div>", heading=False, placeholder=True)

    # Q2 · which Runs: every current Run a row; the newest make Run whole; or that, then one line each
    others = [r for r in RUNS if r is not NEWEST_MAKE]
    out["q2-a"] = page("Q2 A", FIT, f'<div class="diff">{by_role(RUNS)}</div>', **type_view)
    out["q2-b"] = page("Q2 B", FIT, f'<div class="diff">{run_report(NEWEST_MAKE)}{charts()}</div>'
                       '<p class="away">Its other Runs: in Work.</p>', **type_view)
    out["q2-c"] = page("Q2 C", FIT, f'<div class="diff">{run_report(NEWEST_MAKE, compact=True)}</div>'
                       f'<div class="diff">{"".join(one_line(r) for r in others)}</div>', **type_view)

    # Q3 · what leads one hard Run's row: its headline and first table; its RUN-REPORT.md whole; its headline only
    makes = [r for r in RUNS if r["role"] == "make"]
    for key, mode in (("a", "thing"), ("b", "report"), ("c", "none")):
        rows = "".join(row(r, mode, mark=(r is makes[0])) for r in makes)
        out[f"q3-{key}"] = page(f"Q3 {key.upper()}", FIT, f'<section class="rs"><h3 class="role-h">🔨 make</h3>{rows}'
                                "</section>", **type_view)

    # Q4 · a soft Run's row (real: b35's t01_skill_section): the section it wrote; its newest pass; both
    soft = soft_task()
    for key, mode in (("a", "thing"), ("b", "pass"), ("c", "both")):
        out[f"q4-{key}"] = page(f"Q4 {key.upper()}", soft, soft_row(soft, mode),
                                bar=views(["MindMap", "Skill"], "Skill"), caption=CAPTIONS["type"])

    # Q5 · the MindMap: the Runs by role, each boxed with what it found; or each report's sections
    mind = dict(bar=views(["MindMap", "Data"], "MindMap"), caption=CAPTIONS["MindMap"], placeholder=True)
    out["q5-a"] = page("Q5 A", FIT, mindmap_runs(FIT, RUNS, mark=True), **mind)
    out["q5-b"] = page("Q5 B", FIT, mindmap_content(FIT, RUNS, mark=True), **mind)
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/")


if __name__ == "__main__":
    main()
