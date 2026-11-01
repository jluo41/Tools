"""A paper Board's evidence layer (j01 displays, j02 values, j03 citations): each item's drawn file, its body to
read, and the LaTeX table as HTML. haipipe-paper-evidence's build_displays_pdf.py reads the same files through here."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc, face
from live.ui_parts import _section
from live.board_read import _field, _num, _task_url, is_version
from live.board_interactions import IX_CSS


# ── the evidence layer (JL 261031: command → creation → evidence → writing; "I agree"): one Job of the paper Board
# beside the versions, holding Values, Citations and Displays; it reads work's returned Results, never raw data, and
# every version quotes it. Its bands: Displays t01-t19 main, t51-t59 appendix; Values t61-t69; Citations t71-t79. The
# older split Jobs (j21_displays, j22_citations) read the same way until they are merged ────────────────────────────
EVIDENCE_KINDS = (("Displays", r"display"), ("Values", r"value"), ("Citations", r"cite|citation"))


def evidence_html(board: Path, root: Path) -> str:
    """One section per evidence Job (JL 261031: "could we sepearte them? like job-evidence-cite, job-evidence-value,
    job-evidence-display"; evidence is independent of the writing and the venue, so it sits beside the versions). A
    display Job lists its main displays (t01-t49) then its appendix ones (t50 on); the others list their Tasks."""
    jobs = [d for d in sorted(board.glob("j[0-9]*_*")) if d.is_dir() and not is_version(d)]
    # a combined evidence Job (j21_evidence) splits by its bands: displays t01-t59, values t61-t69, citations t71-t79
    band = {"Displays": (1, 59), "Values": (61, 69), "Citations": (71, 79)}
    out = ""
    for kind, pat in EVIDENCE_KINDS:
        for job in (j for j in jobs if re.search(pat, j.name, re.I) or not any(re.search(q, j.name, re.I) for _, q in EVIDENCE_KINDS)):
            tasks = sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir()), key=_num)
            if not re.search(pat, job.name, re.I):
                tasks = [x for x in tasks if band[kind][0] <= _num(x) <= band[kind][1]]
            if kind == "Displays":
                main = [x for x in tasks if _num(x) < 50]
                app = [x for x in tasks if _num(x) >= 50]
                body = ("<h4 class=pb-part>Main</h4>" + "".join(evidence_item(x, root) for x in main) if main else "") + \
                       ("<h4 class=pb-part>Appendix</h4>" + "".join(evidence_item(x, root) for x in app) if app else "")
            else:
                body = "".join(evidence_item(x, root) for x in tasks)
            if not body:
                md = face(job)
                state = (_field(md.read_text(encoding="utf-8", errors="ignore"), "state") if md else "") or "no Tasks yet"
                body = f'<p class=mut>{esc(state)}</p>'
            out += _section(f"{kind} · {job.name}", body + f'<p><a class=fd-btn href="{esc(_task_url(job, root))}">Open {esc(job.name)} ↗</a></p>')
    return out or '<p class=mut>No evidence Job yet.</p>'


# ── each evidence opens to show itself (JL 261031: "how could we preview these evidences? to be collapse open and
# close, them to see all of them"): a folded row per display, value or citation; open, its picture or table (the
# Task's own Run result, else the work Run its made-by names), or its list of values, then its facts ────────────────
PREVIEW_EXT = (".png", ".svg", ".jpg", ".jpeg", ".pdf", ".html")


EV_FACTS = ("answers", "cited-in", "layout", "sources", "made-by", "caption")


def _evidence_file(task: Path, text: str) -> Path | None:
    """The drawn display: the newest picture in the Task's own Runs, else in the work Run its `made-by:` names."""
    def best(files):
        files = [f for f in files if f.suffix.lower() in PREVIEW_EXT and f.is_file()]
        return min(files, key=lambda f: (PREVIEW_EXT.index(f.suffix.lower()), -f.stat().st_mtime)) if files else None
    own = best(list(task.glob("runs/*/result/**/*")) + list(task.glob("result/**/*")))
    if own:
        return own
    m = re.search(r"(?mi)^made-by:.*?\bb(\d+)\.j(\d+)\.t(\d+)\.r(\d+)", text)
    project = next((d for d in task.parents if (d / "work").is_dir()), None)
    if not m or project is None:                # drawn inside a Section's display/ unit (status: drawn in tNN's draft)
        slug = re.sub(r"[^a-z0-9]", "", _field(text, "label").lower())
        board = task.parent.parent
        units = [u for u in board.glob("j*_*/t*_*/display/*")      # a whole name part: "table1" is not in "etable1"
                 if u.is_dir() and slug and slug in re.split(r"[^a-z0-9]+", u.name.lower())]
        for u in units:
            pic = best(list(u.rglob("*")))
            if pic:
                return pic
            if (u / "float.tex").is_file():
                return u / "float.tex"
        return None
    b, j, k, r = m.groups()
    return best([f for d in project.glob(f"work/b{b}_*/j{j}_*/t{k}_*/runs/r{r}_*/result") for f in d.rglob("*")])


def evidence_item(task: Path, root: Path) -> str:
    label, status, body = evidence_body(task, root)
    return (IX_CSS + f'<details class=ix-fold><summary><b>{esc(task.name)}</b><span class=ix-state>{esc(label)}</span>'
            f'<span class=ix-state>{esc(status)}</span></summary><div class=ix-body>{body}</div></details>')


def evidence_body(task: Path, root: Path):
    """(label, status, body) of one evidence Task: its picture or table, its values, its facts, its Open button."""
    md = face(task)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    label, status = _field(text, "label"), _field(text, "status")
    url = lambda f: "/" + quote(ds._rel(f, root))
    body = ""
    # a display's newest version shows as its preview.pdf, both pages: the display with its caption, then how it was
    # made (haipipe-display scripts/build_preview.py; JL 261101: "I want to make this to be things like the pdf")
    previews = sorted(task.glob("runs/*/result/preview.pdf")) + sorted(task.glob("display/*/preview.pdf"))
    preview = previews[-1] if previews else None
    # the face's `printed: <run> [· <stem>]` names the version the paper prints; it wins over the newest alternative
    # (JL 261101: Figure 1 showed its r02 alternative, Table 1 an unprinted table1-patients)
    printed = re.match(r"(\S+)(?:\s*·\s*(\S+))?", _field(text, "printed") or "")
    if printed:
        res = task / "runs" / printed.group(1) / "result"
        pre = f"{printed.group(2)}-" if printed.group(2) else ""
        pick = next((f for f in (res / f"{pre}preview.pdf", res / f"{pre}preview.png") if f.is_file()), None)
        if pick is not None and pick.suffix == ".pdf":
            preview = pick
        elif pick is not None:
            preview, forced = None, pick
    shown = None if preview else (locals().get("forced") or _evidence_file(task, text))
    if preview is not None:
        body += (f'<div class=pb-ptop><span class=pb-state>{esc(preview.parent.parent.name)} · the display, then how it was made</span>'
                 f'<a class=fd-btn data-pop="{esc(label or task.name)} · preview" href="{esc(url(preview))}">⤢ Pop out</a></div>'
                 f'<iframe class=pb-pdf src="{esc(url(preview))}#view=FitH" loading=lazy title="{esc(label or task.name)}"></iframe>')
    if shown is not None:
        if shown.suffix == ".tex":               # a LaTeX table, shown as a table
            body += latex_table_html(shown.read_text(encoding="utf-8", errors="ignore"))
        elif shown.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg"):
            body += (f'<a data-pop="{esc(task.name)}" href="{esc(url(shown))}"><img src="{esc(url(shown))}" alt="{esc(label)}" '
                     f'style="display:block;max-width:100%;max-height:440px;border:1px solid var(--line);border-radius:6px"></a>')
        else:
            body += (f'<iframe src="{esc(url(shown))}" loading=lazy title="{esc(label)}" style="width:100%;height:460px;'
                     f'border:1px solid var(--line);border-radius:6px;background:#fff"></iframe>')
        body += f'<p class=mut>{esc(shown.name)} · <a data-pop="{esc(task.name)}" href="{esc(url(shown))}">Open ↗</a></p>'
    values = re.search(r"(?ms)^## Values\s*\n(.*?)(?=^## |\Z)", text)
    if values:                                   # a value Task: each printed number and where it comes from
        items = re.findall(r"(?m)^- (.+)\n(?:\s+(.+)\n?)?", values.group(1))
        body += "<ol>" + "".join(f'<li>{esc(a)}' + (f'<br><span class=mut>{esc(b)}</span>' if b else '') + '</li>' for a, b in items) + "</ol>"
    papers = re.search(r"(?ms)^## Papers\s*\n(.*?)(?=^## |\Z)", text)
    if papers:                                   # a citation Task: each paper, its check, where the text cites it
        rows = [[c.strip() for c in ln[2:].split("·")] for ln in papers.group(1).splitlines() if ln.startswith("- ")]
        body += "".join(f'<div class=fd-row><span class=n>{esc(r[1] if len(r) > 1 else r[0])}</span><span class=d>{esc(r[3] if len(r) > 3 else "")}</span>'
                        f'<span class=w>{esc(r[2] if len(r) > 2 else "")}</span></div>' for r in rows)
        values = values or papers
    facts = [(k, _field(text, k)) for k in EV_FACTS if _field(text, k)]
    body += "".join(f'<div class=fd-row><span class=n>{esc(k)}</span><span class=d>{esc(v)}</span></div>' for k, v in facts)
    body += f'<p><a class=fd-btn href="{esc(_task_url(task, root))}">Open {esc(task.name)} ↗</a></p>'
    if shown is None and preview is None and not values:
        body = '<p class=mut>Not drawn yet.</p>' + body
    return label, status, body


def _tex_plain(s: str) -> str:
    s = re.sub(r"\\(?:textbf|textit|emph|mathrm|text)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(?:multicolumn|multirow)\{[^{}]*\}\{[^{}]*\}\{([^{}]*)\}", r"\1", s)
    s = s.replace(r"\%", "%").replace(r"\&", "&").replace("~", " ").replace("--", "–").replace(r"\,", " ")
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", "", s)
    return re.sub(r"[{}$]", "", s).strip()


def latex_table_html(tex: str) -> str:
    """A LaTeX table's caption and rows as a small HTML table, so a drawn table previews in place."""
    cap = re.search(r"\\caption\{(.*?)\}\s*\n", tex, re.S)
    body = re.search(r"\\begin\{tabular\}.*?\n(.*?)\\end\{tabular\}", tex, re.S)
    rows = []
    for line in re.split(r"\\\\", body.group(1) if body else ""):
        line = re.sub(r"\\(?:toprule|midrule|bottomrule|hline|cmidrule(?:\([^)]*\))?\{[^}]*\})", "", line).strip()
        if line and not line.startswith("%"):
            rows.append([_tex_plain(c) for c in line.split("&")])
    if not rows:
        return '<p class=mut>A LaTeX table with no rows read.</p>'
    head, rest = rows[0], rows[1:]
    return ((f'<p><b>{esc(_tex_plain(cap.group(1)))}</b></p>' if cap else '')
            + '<table style="border-collapse:collapse;font-size:13px;margin:0 0 8px"><tr>'
            + "".join(f'<th style="text-align:left;border-bottom:1px solid var(--line);padding:4px 8px">{esc(c)}</th>' for c in head)
            + "</tr>" + "".join("<tr>" + "".join(f'<td style="border-bottom:1px solid var(--line);padding:4px 8px;vertical-align:top">{esc(c)}</td>'
                                                 for c in r) + "</tr>" for r in rest) + "</table>")
