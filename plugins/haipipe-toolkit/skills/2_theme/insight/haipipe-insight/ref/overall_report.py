"""overall_report.py <Board Job> [--no-pdf]

The Job's Overall Report in print (JL 261012: the high-level questions "also become the one-page PDF"; "before
the Full, we should have a Overall Report"): page 1, its Executive questions (X01, X02, ...) each with its answer and
how sure, read from the Job's Task faces and the release's question.md; page 2, each question's figure (JL 261013:
"figures to show it to quickly get the outcome"), drawn by overall_figures.py from the `figures:` its page names. The
workbench reads the same answers in full, figures beside them, as the Audience Report's Overall Report button. It
writes the Board's delivery part for the Job, never the Job itself:

    <Board>/delivery/<job>/figures/<X>-<name>.png  each figure (the folder is this script's: an old one is removed)
    <Board>/delivery/<job>/overall-report.html     the two pages, self-contained (the figures inlined)
    <Board>/delivery/<job>/overall-report.pdf      the same pages printed by a headless Chrome, Letter

Generated: never edit either file; change a Task's page and run this again. An X question with no written answer
prints "not written yet". Without Chrome it writes the HTML only and says so.
"""
import argparse
import base64
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import overall_figures as OF  # noqa: E402
import run_question as RQ  # noqa: E402
from open_job import JOB  # noqa: E402

TASK = re.compile(r"^t\d+_(X\d+)_")
CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "google-chrome-stable",
          "chromium", "chromium-browser", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
CSS = """
@page { size: Letter; margin: 0.55in 0.6in; }
body { font: 10.5pt/1.38 -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1b1f24; margin: 0; }
h1 { font-size: 17pt; margin: 0 0 2pt; }
.sub { color: #57606a; font-size: 9pt; margin: 0 0 12pt; }
.q { border-left: 3px solid #0969da; padding: 2pt 0 2pt 9pt; margin: 0 0 9pt; break-inside: avoid; }
.q h2 { font-size: 11.5pt; margin: 0 0 2pt; }
.q h2 span { color: #57606a; font-weight: 400; }
.q p { margin: 0 0 2pt; }
.sure { color: #57606a; font-size: 9pt; }
.foot { color: #57606a; font-size: 8pt; margin-top: 10pt; border-top: 1px solid #d0d7de; padding-top: 4pt; }
.figs { break-before: page; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10pt 16pt; }
.fig { break-inside: avoid; }
.fig h3 { font-size: 10pt; margin: 0 0 3pt; }
.fig h3 span { color: #57606a; font-weight: 400; }
.fig img { width: 100%; display: block; }
.fig p { color: #57606a; font-size: 7.5pt; margin: 1pt 0 0; }
"""


def _chrome():
    for c in CHROME:
        if Path(c).is_file() or shutil.which(c):
            return c if Path(c).is_file() else shutil.which(c)
    return None


def figures(job: Path, out: Path) -> dict:
    """Draw every Executive question's figures into out/ (cleared first: it is this script's); {qid: [(spec, path)]}."""
    job = Path(job).resolve()
    for old in out.glob("*.png") if out.is_dir() else []:
        old.unlink()
    got = {}
    for t in sorted((t for t in job.iterdir() if t.is_dir() and TASK.match(t.name)), key=lambda t: t.name):
        face, _ = RQ.front(t / f"{t.name}.md")
        if face.get("figures"):
            got[TASK.match(t.name).group(1)] = OF.draw(job, TASK.match(t.name).group(1), face["figures"], out)
    return got


def _inline(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(Path(path).read_bytes()).decode("ascii")


def summary(job: Path, figs: dict | None = None) -> tuple[str, list]:
    """The pages' HTML and its rows [(qid, question, answer, how sure)], X questions in id order; `figs` (from
    figures()) makes page 2."""
    job = Path(job).resolve()
    board = job.parent
    if not JOB.match(job.name):
        raise SystemExit(f"{job.name} is not a Board Job (jNN_prototype-pN-<slug>_data-<D>vM)")
    jface, _ = RQ.front(job / f"{job.name}.md")
    bface, _ = RQ.front(board / "board.md")
    proto = board.parent.parent / str(jface.get("prototype", ""))
    rows = []
    for t in sorted((t for t in job.iterdir() if t.is_dir() and TASK.match(t.name)), key=lambda t: TASK.match(t.name).group(1)):
        qid = TASK.match(t.name).group(1)
        face, _ = RQ.front(t / f"{t.name}.md")
        q, _ = RQ.front(proto / t.name / RQ.QFILE) if (proto / t.name / RQ.QFILE).is_file() else ({}, "")
        rows.append((qid, str(q.get("question") or q.get("name") or qid), str(face.get("answer") or "not written yet"),
                     str(face.get("how-sure") or "")))
    if not rows:
        raise SystemExit(f"{job.name} has no Executive question (tNN_X<NN>_<slug>/): add them to its release first")
    title = re.sub(r"^#\s*", "", next((line for line in (job / f"{job.name}.md").read_text(encoding="utf-8").splitlines()
                                       if line.startswith("# ")), job.name))
    ver = next((v for v in bface.get("versions") or [] if str(v.get("version")) == str(jface.get("data"))), {})
    sub = " · ".join(x for x in (f"Board {board.name}", f"Job {job.name}", str(ver.get("new") or "")) if x)
    blocks = "".join(f'<div class=q><h2>{html.escape(qid)} · {html.escape(qq[:1].upper() + qq[1:])}</h2>'
                     f'<p>{html.escape(a)}</p>' + (f'<p class=sure>How sure: {html.escape(s)}</p>' if s else "") + "</div>"
                     for qid, qq, a, s in rows)
    page = ("<!doctype html><html lang=en><head><meta charset=utf-8>"
            f"<title>Overall Report · {html.escape(job.name)}</title><style>{CSS}</style></head><body>"
            f"<h1>Overall Report · {html.escape(title)}</h1><p class=sub>{html.escape(sub)}</p>{blocks}"
            "<p class=foot>Each answer rests on the Data, Information, Knowledge and Wisdom questions below it, cited "
            f"on its page: {html.escape(board.name)}/{html.escape(job.name)}/tNN_X&lt;NN&gt;_&lt;slug&gt;/. "
            "Generated by haipipe-insight ref/overall_report.py; do not edit.</p>"
            + _figure_page(figs or {}) + "</body></html>")
    return page, rows


def _figure_page(figs: dict) -> str:
    cells = "".join(f'<div class=fig><h3>{html.escape(qid)} · <span>{html.escape(spec["title"])}</span></h3>'
                    f'<img src="{_inline(path)}" alt="{html.escape(spec["title"])}">'
                    f'<p>from {html.escape(OF.cite(spec))}</p></div>'
                    for qid in sorted(figs) for spec, path in figs[qid])
    return (f'<section class=figs><h1>The figures</h1><p class=sub>One picture per answer, each drawn from the result '
            f'table of the question it cites.</p><div class=grid>{cells}</div></section>') if cells else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("job")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()
    job = Path(a.job).resolve()
    out = job.parent / "delivery" / job.name
    out.mkdir(parents=True, exist_ok=True)
    figs = figures(job, out / "figures")
    page, rows = summary(job, figs)
    (out / "overall-report.html").write_text(page, encoding="utf-8")
    made = [p for qid in sorted(figs) for _, p in figs[qid]] + [out / "overall-report.html"]
    chrome = None if a.no_pdf else _chrome()
    if chrome:
        with tempfile.TemporaryDirectory() as profile:
            subprocess.run([chrome, "--headless", "--disable-gpu", f"--user-data-dir={profile}",
                            "--no-pdf-header-footer", f"--print-to-pdf={out / 'overall-report.pdf'}",
                            (out / "overall-report.html").as_uri()], check=True, capture_output=True, timeout=300)
        made.append(out / "overall-report.pdf")
    elif not a.no_pdf:
        print("no Chrome found: wrote the HTML only")
    root = RQ.space_root(job)
    for p in made:
        print(f"wrote {p.relative_to(root).as_posix()}")
    print(f"{len(rows)} Executive questions: {', '.join(r[0] for r in rows)}")


if __name__ == "__main__":
    main()
