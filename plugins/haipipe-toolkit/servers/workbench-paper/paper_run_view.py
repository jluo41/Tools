"""One Run's results as a pop-out page (GET /_board/run-result): which files the Run wrote, with light Markdown and CSV views.
Moved from paper.py, which re-exports every name here so `from live.paper import _md_view` keeps working."""
import re
from pathlib import Path
from urllib.parse import quote

from live.paper import _size, esc, inline
from live.paper_pages import _RESULT_PAGE


# ---- one run's results, in a pop-out (JL 260930: "for a run, how could we have a popout
# window to show the results of that run's results") -------------------------------------
_IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
_TAB_EXT = {".csv", ".tsv"}
_DOC_EXT = {".md", ".markdown", ".txt"}
_MAX_FILES, _MAX_ROWS, _MAX_DOC = 300, 50, 200_000


def run_result_url(root, task_dir, run=""):
    """`/_board/run-result?task=<Task folder>&run=<run stem>`; '' outside the root."""
    try:
        rel = Path(task_dir).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return ""
    return "/_board/run-result?task=%s%s" % (quote(rel, safe="/"), ("&run=" + quote(run, safe="")) if run else "")


def run_files(task_dir, run=""):
    """(where, files) for one run of a Task. Its own `results/<run>/` when there is one;
    else the files in `results/` named after it (`run_6a2_f01.sh` wrote
    `figures/6a2_f01_horizon_fairness_growth.png`), which is how a Task keeping one shared
    `results/` tells its runs apart; else the files whose path holds every word of that name
    (`run_fit_forecast.sh` wrote `fits_forecast/…`); else all of `results/`, said so. No
    run: all of it."""
    own = Path(task_dir) / "runs" / run / "result" if run else None
    if own is not None and own.is_dir():                     # one folder per Run (hai-run 0.31.0)
        return "runs/%s/result/" % run, sorted((f for f in own.rglob("*") if f.is_file() and not f.name.startswith(".")),
                                              key=lambda f: f.relative_to(own).as_posix())
    res = Path(task_dir) / "results"
    if not res.is_dir():
        return "no results/ folder yet", []
    every = lambda base: sorted((f for f in base.rglob("*") if f.is_file() and not f.name.startswith(".")),
                                key=lambda f: f.relative_to(res).as_posix())
    if not run:
        return "results/", every(res)
    if (res / run).is_dir():
        return "results/%s/" % run, every(res / run)
    key = re.sub(r"^run[_-]", "", run)
    named = [f for f in every(res) if key and key in f.name]
    if named:
        return "the files in results/ whose name holds %s" % key, named
    words = [w for w in key.split("_") if w]
    worded = [f for f in every(res) if words and all(w in f.relative_to(res).as_posix() for w in words)]
    if worded:
        return "the files in results/ whose path holds %s" % " and ".join(words), worded
    return "all of results/: this Task keeps one folder for every run, and no file there is named after %s" % key, every(res)


def _md_view(text, base=None):
    """Enough Markdown for a result summary: headings, bullets, pipe tables, fences, bold
    and code. Raw HTML is escaped, never run. With `base` (the URL folder of the .md), a
    line that is only `![alt](relative.png)` shows that image, resolved against it."""
    from urllib.parse import urljoin, urlsplit
    out, lines, i, para = [], text.split("\n"), 0, []

    def flush():                                  # a line break inside a paragraph stays
        if para:
            out.append("<p>%s</p>" % "<br>".join(inline(x) for x in para))
            para.clear()
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            out.append("<pre>%s</pre>" % esc("\n".join(lines[i + 1:j])))
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        img = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", s) if base else None
        if img and not urlsplit(img.group(2)).scheme and not img.group(2).startswith("/"):
            flush()
            src = esc(urljoin(base, img.group(2)))
            out.append('<figure><a href="%s" target="_blank" rel="noopener"><img loading="lazy" src="%s" alt="%s"></a>'
                       '</figure>' % (src, src, esc(img.group(1))))
        elif m:
            flush()
            out.append("<h%d>%s</h%d>" % (len(m.group(1)) + 2, inline(m.group(2)), len(m.group(1)) + 2))
        elif s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            flush()
            cells = lambda row: [c.strip() for c in row.strip().strip("|").split("|")]
            head, j, body = cells(s), i + 2, []
            while j < len(lines) and lines[j].strip().startswith("|"):
                body.append(cells(lines[j]))
                j += 1
            out.append("<table><tr>%s</tr>%s</table>" % ("".join("<th>%s</th>" % inline(c) for c in head),
                       "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in body)))
            i = j
            continue
        elif re.match(r"^[-*]\s+", s):
            flush()
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\s*[-*]\s+", "", lines[i])))
                i += 1
            out.append("<ul>%s</ul>" % "".join(items))
            continue
        elif not s:
            flush()
        else:
            para.append(s)
        i += 1
    flush()
    return "".join(out)


def _csv_view(f):
    """The first rows of a table, and how many there are."""
    import csv
    import itertools
    delim = "\t" if f.suffix == ".tsv" else ","
    try:
        with f.open(encoding="utf-8", errors="replace", newline="") as fh:
            rows = list(itertools.islice(csv.reader(fh, delimiter=delim), _MAX_ROWS + 1))
        n = None
        if f.stat().st_size < 20_000_000:
            with f.open("rb") as fh:
                n = max(sum(1 for _ in fh) - 1, 0)
    except OSError as exc:
        return '<p class="mut">cannot read: %s</p>' % esc(exc)
    if not rows:
        return '<p class="mut">empty</p>'
    head, body = rows[0], rows[1:_MAX_ROWS + 1]
    note = ("%d rows" % n if n is not None else "a large file") + (", the first %d shown" % len(body) if n is None or n > len(body) else "")
    return ('<p class="mut">%s · %d columns</p><div class="tw"><table><tr>%s</tr>%s</table></div>'
            % (esc(note), len(head), "".join("<th>%s</th>" % esc(c) for c in head),
               "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % esc(c) for c in r) for r in body)))


def render_run_result(root, task_rel, run=""):
    """One run's results as a page: where they are, then its summaries, figures, tables
    and every other file, each opening raw. Reads only inside the root."""
    root = Path(root).resolve()
    tdir = (root / task_rel.strip("/")).resolve()
    tdir.relative_to(root)                                   # outside the root: ValueError
    if not tdir.is_dir():
        raise FileNotFoundError(task_rel)
    raw = lambda f: "/" + quote(f.resolve().relative_to(root).as_posix(), safe="/")
    where, files = run_files(tdir, run)
    from host_registry import static_path_allowed       # sealed labels, *.private.*, dot folders stay hidden (review 261031)
    files = [f for f in files if static_path_allowed(root, f)]
    more = max(len(files) - _MAX_FILES, 0)
    files = files[:_MAX_FILES]
    res = tdir / "runs" / run / "result" if run and (tdir / "runs" / run / "result").is_dir() else tdir / "results"
    shown = lambda f: f.relative_to(res).as_posix() if res in f.parents else f.name
    runs = tdir / "runs"
    ticket = next((f for f in sorted(runs.rglob(run + ".*")) if f.is_file()), None) if run and runs.is_dir() else None
    nb = tdir / "notebooks" / (run + ".ipynb") if run else None
    links = [('<a href="%s" target="_blank" rel="noopener">Run script ↗</a>' % esc(raw(ticket))) if ticket else "",
             ('<a href="%s" target="_blank" rel="noopener">Executed notebook ↗</a>' % esc(raw(nb))) if nb and nb.is_file() else "",
             ('<a href="%s" target="_blank" rel="noopener">Task page ↗</a>' % esc(raw(tdir / (tdir.name + ".md"))))
             if (tdir / (tdir.name + ".md")).is_file() else ""]
    body = ['<h1>%s</h1>' % esc(run or tdir.name),
            '<p class="where mut"><code>%s</code> · %s</p>' % (esc(tdir.relative_to(root).as_posix()), esc(where)),
            '<div class="links">%s</div>' % "".join(x for x in links if x)]
    rt = res / run / "runtime.yaml" if run else None
    if rt is not None and rt.is_file():
        body.append('<h2>Receipt</h2><pre>%s</pre>' % esc(rt.read_text(encoding="utf-8", errors="replace")[:4000]))
    docs = [f for f in files if f.suffix.lower() in _DOC_EXT and f.name != "runtime.yaml"]
    figs = [f for f in files if f.suffix.lower() in _IMG_EXT]
    tabs = [f for f in files if f.suffix.lower() in _TAB_EXT]
    rest = [f for f in files if f not in docs and f not in figs and f not in tabs and f != rt]
    if docs:
        body.append("<h2>Summaries · %d</h2>" % len(docs))
        for f in docs:
            text = f.read_text(encoding="utf-8", errors="replace") if f.stat().st_size <= _MAX_DOC else ""
            # a .md with no Markdown mark (heading, table row, bullet) is plain text laid out by
            # line, as fit_summary.md is (JL 260930: "How to handle this markdown render?"):
            # it shows as written
            marked = f.suffix.lower() != ".txt" and re.search(r"(?m)^(#{1,6}\s|\s*\|.*\||\s*[-*]\s)", text)
            inner = (_md_view(text) if marked else "<pre>%s</pre>" % esc(text)) if text else \
                '<p class="mut">too long to show here</p>'
            body.append('<div class="doc"><h3><a href="%s" target="_blank" rel="noopener">%s</a></h3>%s</div>'
                        % (esc(raw(f)), esc(shown(f)), inner))
    if figs:
        body.append('<h2>Figures · %d</h2><div class="figs">%s</div>' % (len(figs), "".join(
            '<figure><a href="%s" target="_blank" rel="noopener"><img loading="lazy" src="%s" alt="%s"></a>'
            '<figcaption>%s</figcaption></figure>' % (esc(raw(f)), esc(raw(f)), esc(f.name), esc(shown(f))) for f in figs)))
    for f in tabs:
        if f is tabs[0]:
            body.append("<h2>Tables · %d</h2>" % len(tabs))
        body.append('<h3><a href="%s" target="_blank" rel="noopener">%s</a></h3>%s' % (esc(raw(f)), esc(shown(f)), _csv_view(f)))
    if rest:
        body.append('<h2>Other files · %d</h2><ul class="files">%s</ul>' % (len(rest), "".join(
            '<li><a href="%s" target="_blank" rel="noopener">%s</a> <span class="mut">%s</span></li>'
            % (esc(raw(f)), esc(shown(f)), esc(_size(f))) for f in rest)))
    if more:
        body.append('<p class="mut">and %d more files, not shown</p>' % more)
    if not files:
        body.append('<p class="mut">No result file yet.</p>')
    return _RESULT_PAGE.format(title=esc(run or tdir.name), body="\n".join(body))
