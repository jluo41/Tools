"""Writes every q<N>-<key>.html preview of this Run (r02_collect_task_work_views); rerun it, never edit them.

Each preview is the real Task Work page's look (its CSS fetched from 5623), shown twice side by side: left
t01_build_studio_pages (soft Runs, done), right t02_block_page (collection Runs). Only the view bar and the content
change between options; every name and field is read from the Runs' own run.yaml and pass.md.
"""
import html
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE.parents[2]                     # j02_studio_pages
BASE = "http://100.121.165.84:5623/_board/workbench?layout=focus&path=blueprints/Project-PageParts/work/b35_studio/j02_studio_pages/"
TASKS = ["t01_build_studio_pages", "t02_block_page"]
MARK = {"done": "✅", "planned": "⬜", "waiting": "🙋", "running": "⏳"}
e = html.escape


def field(text, key):
    m = re.search(rf"(?m)^{key}:\s*(.*)$", text)
    return (m.group(1).strip() if m else "") or ""


def runs(task):
    out = []
    for p in sorted((JOB / task / "runs").iterdir()):
        if not (p / "run.yaml").is_file():
            continue
        y = (p / "run.yaml").read_text()
        passes = sorted((p / "passes").glob("p*/pass.md")) if (p / "passes").is_dir() else []
        last = passes[-1] if passes else None
        writes = re.findall(r"(?m)^- (.+)$", y.split("writes:")[1].split("feeds:")[0]) if "writes:" in y else []
        tgt = field(y, "target")
        snn = re.search(r"-(s\d\d)", tgt)
        out.append(dict(name=p.name, status=field(y, "status"), agent=field(y, "agent"), skill=field(y, "skill"),
                        kind=field(y, "kind"), type=field(y, "type"), ticket=field(y, "ticket"), target=tgt,
                        snn=snn.group(1) if snn else "",
                        pass_title=last.read_text().splitlines()[0].lstrip("# ").strip() if last else "",
                        pass_name=last.parent.name if last else "", writes=writes,
                        ticket_text=(p / field(y, "ticket")).read_text() if field(y, "ticket").endswith(".md")
                        and (p / field(y, "ticket")).is_file() else "",
                        result=sorted(x.name for x in (p / "result").iterdir()) if (p / "result").is_dir() else []))
    # a waiting form first, then by name
    return sorted(out, key=lambda r: (r["status"] != "waiting", r["name"]))


def css():
    page = urllib.request.urlopen(BASE + TASKS[0] + "&section=work", timeout=20).read().decode()
    return re.search(r"<style>(.*?)</style>", page, re.S).group(1)


def meta(r):
    return f'{MARK.get(r["status"], "")} {e(r["status"])} · {e(r["agent"])} · {e(r["skill"])}'


def row(r, parts=("meta",), diff=()):
    bits = [f'<span class="row-name">{e(r["name"])}</span>']
    for p in parts:
        cls = ' class="diff"' if p in diff else ''
        if p == "meta":
            bits.append(f'<p class="row-meta">{meta(r)}</p>')
        elif p == "pass":
            bits.append(f'<p class="row-line"{cls}>{e(r["pass_title"]) + " · " + e(r["pass_name"]) if r["pass_title"] else "No pass yet."}</p>')
        elif p == "wrote":
            what = ", ".join(w.split("/")[-1] for w in r["writes"]) if r["kind"] == "soft" else \
                (", ".join(r["result"]) if r["result"] else "result/ not written yet")
            bits.append(f'<p class="row-meta"{cls}>{"wrote" if r["kind"] == "soft" else "result"}: {e(what)}</p>')
        elif p == "snn":
            bits.append(f'<p class="row-meta"{cls}>{"for " + r["snn"] if r["snn"] else "for no sNN"}</p>')
        elif p == "buttons":
            b = ["Ticket"] + (["Result"] if r["kind"] == "hard" else []) + (["Passes"] if r["pass_name"] else [])
            bits.append(f'<p class="row-verbs"{cls}>' + "".join(f'<a class="row-verb">{x}</a>' for x in b) + '</p>')
    return '<article class="status-row">' + "".join(bits) + '</article>'


def page(task, bar, content, caption="Its Runs, one per row."):
    goal = re.search(r"(?m)^goal:\s*(.*)$", (JOB / task / f"{task}.md").read_text())
    goal = goal.group(1) if goal else ""
    nav = '<nav class="section-views" aria-label="Views">' + "".join(
        f'<a{" aria-current=page" if i == 0 else ""}>{e(b)}</a>' for i, b in enumerate(bar)) + '</nav>'
    return (f'<main class="focus-page"><div class="focus-crumb">… / j02_studio_pages / <span>{task}</span></div>'
            f'<h1>{task}<span class="h1-section">Work</span></h1>{nav}'
            f'<div class="focus-goal"><span class="goal-word">Aim</span><p>{e(goal[:150])}</p></div>'
            f'<section class="focus-card"><div class="focus-content"><p class="view-caption">{e(caption)}</p>'
            f'{content}</div></section></main>')


def doc(style, left, right, note, overlay=""):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>preview</title>'
            f'<style>{style}</style><style>.two{{display:flex;gap:18px;padding:0 12px}}.two>.focus-page{{flex:1;'
            'min-width:0;max-width:none;padding:14px 10px}}.pnote{font-size:13px;color:var(--muted);padding:10px 22px 0}'
            '.panel-h{font-size:12px;font-weight:700;color:var(--muted);margin:14px 0 6px}.panel-h:first-of-type{margin-top:0}'
            '.pop{position:fixed;inset:40px 60px;background:var(--paper);border:1px solid var(--line);border-radius:10px;'
            'box-shadow:0 10px 30px #0003;padding:14px 20px;overflow:auto;font-size:13px}.pop h3{margin:0 0 6px}'
            '.pop pre{white-space:pre-wrap;font-size:12px;background:var(--wash);padding:8px;border-radius:6px}'
            f'</style></head><body><p class="pnote">{e(note)}</p><div class="two">{left}{right}</div>{overlay}</body></html>')


def main():
    style = css()
    R = {t: runs(t) for t in TASKS}
    out = {}
    full = ("meta", "pass")

    # Q1 · view list (each preview: its first view open; a split view shows each of its views as a small panel)
    out["q1-a"] = [page(t, ["Runs"], "".join(row(r, full) for r in R[t])) for t in TASKS]
    def by(t, key, label):
        groups = {}
        for r in R[t]:
            groups.setdefault(label(r[key]), []).append(r)
        bar = list(groups)
        body = "".join(f'<h4 class="panel-h diff">view: {g}</h4>' + "".join(row(r, full) for r in rs) for g, rs in groups.items())
        return page(t, bar, body)
    out["q1-b"] = [by(t, "kind", lambda k: "Hard" if k == "hard" else "Soft") for t in TASKS]
    def parts(t):
        rs = R[t]
        res = [r for r in rs if r["result"]]
        body = ('<h4 class="panel-h diff">view: Runs</h4>' + "".join(row(r) for r in rs)
                + '<h4 class="panel-h diff">view: Results</h4>'
                + ("".join(f'<p class="row-meta">{e(r["name"])}: {e(", ".join(r["result"]))}</p>' for r in res)
                   or '<p class="mut">No result/ yet.</p>')
                + '<h4 class="panel-h diff">view: Passes</h4>'
                + ("".join(f'<p class="row-meta">{e(r["pass_name"])} · {e(r["name"])} · {e(r["pass_title"])}</p>'
                           for r in rs if r["pass_name"]) or '<p class="mut">No passes yet.</p>'))
        return page(t, ["Runs", "Results", "Passes"], body)
    out["q1-c"] = [parts(t) for t in TASKS]
    out["q1-d"] = [by(t, "type", lambda k: k.title()) for t in TASKS]

    # Q2 · the Runs view, top to bottom
    out["q2-a"] = [page(t, ["Runs"], "".join(row(r, full) for r in R[t])) for t in TASKS]
    def waits(t):
        w = [r for r in R[t] if r["status"] == "waiting"]
        rest = [r for r in R[t] if r["status"] != "waiting"]
        return page(t, ["Runs"], (f'<h4 class="panel-h diff">Waits on you</h4>' + "".join(row(r, full) for r in w) if w else "")
                    + '<h4 class="panel-h diff">Runs</h4>' + "".join(row(r, full) for r in rest))
    out["q2-b"] = [waits(t) for t in TASKS]
    def states(t):
        order = ["waiting", "running", "planned", "done"]
        body = ""
        for s in order:
            rs = [r for r in R[t] if r["status"] == s]
            if rs:
                body += f'<h4 class="panel-h diff">{MARK[s]} {s}</h4>' + "".join(row(r, full) for r in rs)
        return page(t, ["Runs"], body)
    out["q2-c"] = [states(t) for t in TASKS]

    # Q3 · one Run's row
    out["q3-a"] = [page(t, ["Runs"], "".join(row(r, ("meta",)) for r in R[t])) for t in TASKS]
    out["q3-b"] = [page(t, ["Runs"], "".join(row(r, full, diff=("pass",)) for r in R[t])) for t in TASKS]
    out["q3-c"] = [page(t, ["Runs"], "".join(row(r, full + ("wrote",), diff=("wrote",)) for r in R[t])) for t in TASKS]
    out["q3-d"] = [page(t, ["Runs"], "".join(row(r, full + ("snn",), diff=("snn",)) for r in R[t])) for t in TASKS]

    # Q4 · a click on a Run's name
    first = R[TASKS[0]][0]
    base = [page(t, ["Runs"], "".join(row(r, full) for r in R[t])) for t in TASKS]
    card = "\n".join(f"{k}: {first[k]}" for k in ("kind", "type", "target", "ticket", "skill", "agent", "status"))
    pop_a = (f'<div class="pop diff"><h3>{e(first["name"])}</h3><p class="mut">pop-out: the Run folder, top to bottom</p>'
             f'<h4 class="panel-h">run.yaml</h4><pre>{e(card)}</pre>'
             f'<h4 class="panel-h">ticket · {e(first["ticket"])}</h4><pre>{e(first["ticket_text"][:400])}</pre>'
             f'<h4 class="panel-h">result/</h4><p class="mut">none: a soft Run writes into its scope</p>'
             f'<h4 class="panel-h">passes</h4><p>{e(first["pass_name"])} · {e(first["pass_title"])}</p></div>')
    pop_b = (f'<div class="pop diff"><h3>{e(first["ticket"])}</h3><p class="mut">pop-out: its ticket only</p>'
             f'<pre>{e(first["ticket_text"][:600])}</pre></div>')
    out["q4-a"] = base + [pop_a]
    out["q4-b"] = base + [pop_b]
    out["q4-c"] = [page(t, ["Runs"], "".join(row(r, full + ("buttons",), diff=("buttons",)) for r in R[t])) for t in TASKS]

    note = "Left: t01_build_studio_pages (soft Runs). Right: t02_block_page (collection Runs). Real run.yaml and pass.md."
    for key, parts_ in out.items():
        (HERE / f"{key}.html").write_text(doc(style, parts_[0], parts_[1], note, parts_[2] if len(parts_) > 2 else ""))
    print("wrote", len(out), "previews")


if __name__ == "__main__":
    sys.exit(main())
