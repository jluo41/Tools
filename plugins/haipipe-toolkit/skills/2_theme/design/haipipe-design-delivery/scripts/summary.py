"""Build a design Block's one-page summary for leaders: delivery/summary.html and delivery/summary.pdf.

    python summary.py <block folder> [--example jNN:dNN] [--no-pdf]

(JL 261012, from the 10-08 demo: "add an executive summary, a one-page PDF-style overview", and "a drive-home
example".) Reads only what the Runs wrote: board.md (title, goals, questions), each Job's face (method, state, hold),
its t99 ranking, its run-release card (`signed:`), the Block's delivery/designs.json, and the Opening of each question
whose report is partly or fully answered. It claims nothing new. The example is one released design traced from what
it came from to its frozen prediction; by default the rank-1 design with the narrowest predicted range. The PDF is
printed by a local Chrome, headless; without one only the HTML is written. Prints what it wrote.
"""
import argparse
import csv
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import yaml

METHODS = Path(__file__).resolve().parents[2] / "haipipe-design-method" / "methods"
NUM = r"[+-−]?\d+(?:\.\d+)?"
CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium", "chromium-browser")
esc = html.escape


def front(md: Path) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8")) if md.is_file() else None
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def block_yaml(md: Path, heading: str, key: str) -> list:
    m = re.search(rf"(?ms)^##\s+{heading}\s*\n.*?```yaml\n(.*?)```", md.read_text(encoding="utf-8"))
    data = yaml.safe_load(m.group(1)) if m else {}
    return (data or {}).get(key, []) if isinstance(data, dict) else []


def method_name(pin: str) -> str:
    mid = str(pin).split()[0] if pin else ""
    md = next(iter(sorted(METHODS.glob(f"{mid}-*/method.md"))), None) if mid else None
    return str(front(md).get("name") or mid) if md else mid


def width(predicted: str) -> float:
    """The predicted range's width, for picking the most certain design; no range sorts last."""
    r = re.search(rf"\[\s*({NUM})\s*%?\s*[;,]\s*({NUM})", str(predicted).replace("−", "-"))
    return abs(float(r.group(2)) - float(r.group(1))) if r else 1e9


def report_of(block: Path, q: dict) -> Path | None:
    rep = block / str(q.get("report", "")).rstrip("/") if q.get("report") else None
    if rep and rep.is_file():
        return rep
    return next(iter(sorted(rep.glob("*.md"))), None) if rep and rep.is_dir() else None


def answers(block: Path, questions: list) -> list:
    """(title, status, Opening) of each question answered or partly answered, by its report's header."""
    out = []
    for q in questions:
        page = report_of(block, q)
        text = page.read_text(encoding="utf-8") if page else ""
        m = re.search(r"(?m)^answer-status:\s*(\w+)", text)
        status = str(q.get("answer-status") or (m.group(1) if m else "open"))
        if status in ("partial", "answered") and page:
            opening = next((p.strip() for p in text.split("\n\n")[1:] if p.strip() and not p.lstrip().startswith(("#", "---"))), "")
            out.append((str(q.get("title", "")), status, opening))
    return out


def jobs(block: Path, released: list) -> list:
    out = []
    for jdir in sorted(p for p in block.iterdir() if p.is_dir() and re.match(r"^j\d+_", p.name)):
        face = front(jdir / f"{jdir.name}.md")
        if not face.get("method"):
            continue
        jid = jdir.name.split("_")[0]
        rank = jdir / "t99_review-whole" / "runs" / "run-rank-t99" / "result" / "ranking.csv"
        rows = list(csv.DictReader(rank.open(encoding="utf-8"))) if rank.is_file() else []
        kept = sorted((r for r in rows if str(r.get("kept", "")).strip().lower() == "yes"),
                      key=lambda r: int(r["rank"]) if str(r.get("rank", "")).isdigit() else 999)
        mine = {d["design"]: d for d in released if d.get("job") == jid}
        top = mine.get(kept[0]["design"]) if kept else None
        card = jdir / "runs" / f"run-release-{jid}" / "run.yaml"
        signed = str((yaml.safe_load(card.read_text(encoding="utf-8")) or {}).get("signed", "")) if card.is_file() else ""
        hold = re.search(r"(?ms)^## Hold\s*\n(.*?)(?=^##\s|\Z)", (jdir / f"{jdir.name}.md").read_text(encoding="utf-8"))
        out.append({"id": jid, "name": jdir.name, "method": method_name(face["method"]), "pin": face["method"],
                    "state": str(face.get("state", "")), "released": len(mine), "top": top, "signed": signed,
                    "hold": re.split(r"(?<=[.!?])\s", " ".join(hold.group(1).split()))[0] if hold else ""})
    return out


def pick(js: list, released: list, example: str) -> dict | None:
    if example:
        jid, did = (example.split(":") + [""])[:2]
        return next((d for d in released if d.get("job") == jid and d.get("design") == did), None)
    tops = [j["top"] for j in js if j["top"]]
    return min(tops, key=lambda d: width(d.get("predicted", ""))) if tops else None


def page(block: Path, example: str) -> str:
    md = block / "board.md"
    title = md.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").split(" · ", 1)[-1]
    goals = block_yaml(md, "Goals", "goals")
    dj = block / "delivery" / "designs.json"
    released = json.loads(dj.read_text(encoding="utf-8")).get("designs", []) if dj.is_file() else []
    js = jobs(block, released)
    ex = pick(js, released, example)
    observed = (block / "observed").is_dir() and any((block / "observed").glob("e*/arms.csv"))
    goal = "".join(f'<p class=goal><b>{esc(str(g.get("aim", "")))}</b> · {esc(str(g.get("who", "")))} · '
                   f'{esc(str(g.get("venue", "")))} · {esc(str(g.get("n", "")))} designs a method</p>' for g in goals)
    lines = "".join(f'<p><b>{esc(t)}</b> <span class=mut>({"answered" if s == "answered" else "partly answered"})</span> '
                    f'{esc(o)}</p>' for t, s, o in answers(block, block_yaml(md, "Questions", "questions")))
    held = [j for j in js if j["state"] == "held"]
    counts = (f'{len(js)} methods · {sum(j["released"] for j in js)} designs released · '
              + (f'{len(held)} held · ' if held else "") + ("experiment results in" if observed else "no experiment result yet"))
    rows = "".join(
        f'<tr><td>{esc(j["name"])}</td><td>{esc(j["method"])}</td>'
        + (f'<td colspan=3 class=mut>{esc(j["hold"]) or "held"}</td>' if j["state"] == "held"
           else f'<td>{j["released"]} released</td>'
                f'<td>{esc(j["top"]["design"] + " · " + j["top"]["name"]) if j["top"] else "—"}</td>'
                f'<td class=num>{esc(j["top"]["predicted"]) if j["top"] else "—"}</td>') + "</tr>" for j in js)
    signs = sorted({j["signed"] for j in js if j["signed"]})
    how = "; ".join(f'by {x.replace(" · ", ", ", 1)}' for x in signs)
    trace = ""
    if ex:
        job = next((j for j in js if j["id"] == ex["job"]), {})
        trace = (f'<h2>One design, traced</h2><p class=mut>{esc(ex.get("job_name", ""))} · {esc(ex["design"])} · '
                 f'{esc(ex.get("name", ""))} · made by {esc(job.get("method", ""))}</p>'
                 f'<div class=sms>{esc(ex.get("words", ""))}</div>'
                 f'<p><b>Where it comes from:</b> {esc(ex.get("why", ""))}</p>'
                 f'<p><b>Predicted:</b> {esc(ex.get("predicted", ""))} against {esc(ex.get("against", "the control"))}, '
                 f'frozen {esc(str(ex.get("released", "")))}, before anything it predicts was observed.</p>'
                 f'<p><b>Tested by:</b> the next experiment; its result is scored against this prediction.</p>')
    nxt = ("Score each tested design against its frozen prediction." if observed
           else "Launch the experiment with the released designs; each arm's result comes back to this Block.")
    return f"""<!doctype html><html><head><meta charset=utf-8><title>{esc(title)} · summary</title><style>
@page {{ size: Letter landscape; margin: 0.45in; }}
body {{ font: 10.5pt/1.38 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1a1a1a; margin: 0; }}
h1 {{ font-size: 19pt; margin: 0 0 2px; }} h2 {{ font-size: 12pt; margin: 14px 0 4px; border-bottom: 1px solid #ccc; }}
p {{ margin: 4px 0; }} .mut {{ color: #666; }} .goal {{ font-size: 11.5pt; }}
.cols {{ display: grid; grid-template-columns: 1.55fr 1fr; gap: 26px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }} th, td {{ text-align: left; padding: 3px 6px 3px 0;
border-bottom: 1px solid #e3e3e3; vertical-align: top; }} th {{ color: #666; font-weight: 600; }} .num {{ white-space: nowrap; }}
.sms {{ background: #e9e9eb; border-radius: 14px; padding: 9px 13px; margin: 6px 0 8px; font-size: 11pt; max-width: 92%; }}
.foot {{ position: fixed; bottom: 0; font-size: 8pt; color: #888; }}
</style></head><body>
<h1>{esc(title)}</h1>{goal}
<div class=cols><div>
<h2>Bottom line</h2>{lines or '<p class=mut>No question answered yet.</p>'}
<h2>What was made</h2><p>{esc(counts)}</p>
<table><thead><tr><th>Job</th><th>method</th><th>designs</th><th>top design</th><th>predicted</th></tr></thead><tbody>{rows}</tbody></table>
<p class=mut>Predicted: as each method wrote it, against the control; scored in percentage points.</p>
{f'<p class=mut>Approved {esc(how)}.</p>' if how else ""}
</div><div>{trace}<h2>Next</h2><p>{esc(nxt)}</p></div></div>
<p class=foot>Built {date.today():%Y-%m-%d} by haipipe-design-delivery summary.py from {esc(block.name)}: board.md,
delivery/designs.json, each Job's ranking and release card, the question reports. Each design's full record is in the workbench.</p>
</body></html>"""


def print_pdf(html_path: Path, pdf: Path) -> int | None:
    """Print the page with a local Chrome, headless, in a throwaway profile; return the page count, or None."""
    exe = next((c for c in CHROME if Path(c).is_file() or shutil.which(c)), None)
    if not exe:
        return None
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={prof}",
                        f"--print-to-pdf={pdf}", html_path.resolve().as_uri()], capture_output=True, timeout=90)
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes())) if pdf.is_file() else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("block")
    ap.add_argument("--example", default="", help="the design to trace, jNN:dNN (default: the narrowest predicted range)")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()
    block = Path(a.block).resolve()
    if not (block / "board.md").is_file():
        sys.exit(f"no board.md in {a.block}")
    out = block / "delivery"
    out.mkdir(exist_ok=True)
    (out / "summary.html").write_text(page(block, a.example), encoding="utf-8")
    print(f"wrote delivery/summary.html")
    if not a.no_pdf:
        n = print_pdf(out / "summary.html", out / "summary.pdf")
        print("no Chrome found: summary.pdf not written" if n is None else
              f"wrote delivery/summary.pdf: {n} page{'s' if n != 1 else ''}" + ("" if n == 1 else " (more than one: shorten the inputs)"))


if __name__ == "__main__":
    main()
