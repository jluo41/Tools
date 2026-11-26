"""Run: python3 job-view-topics-data.py <the Block folder> > job-view-topics-data.js. Print the s11 preview's FEW data, read from b17's folders: names, rounds, marks, summaries, dates."""
import json, re, sys
from pathlib import Path
B = Path(sys.argv[1])
MARK = {"done": "✅", "complete": "✅", "completed": "✅", "ok": "✅", "waiting": "🙋", "running": "⏳",
        "failed": "❌", "blocked": "🔶", "planned": "⬜"}
def head(f):
    t = f.read_text(errors="ignore") if f.is_file() else ""
    h = (re.search(r"(?m)^#\s+(.+)$", t) or [None, ""])[1].strip()
    return h.split(" · ", 1)[1].strip() if " · " in h else h
def line(f, key):
    t = f.read_text(errors="ignore") if f.is_file() else ""
    return (re.search(rf"(?m)^{key}:\s*(.+)$", t) or [None, ""])[1].strip()
def status(r):
    for f in (r / "result" / "runtime.yaml", r / "run.yaml"):
        s = line(f, "status").strip("'\"")
        if s: return s
    return ""
def rounds(t):
    out = []
    for r in sorted((d for d in (t / "runs").glob("*") if d.is_dir() and not d.name.startswith((".", "_"))), reverse=True):
        mk = MARK.get(status(r), "⬜")
        ps = sorted((d for d in (r / "passes").glob("*") if d.is_dir()), reverse=True) if (r / "passes").is_dir() else []
        for i, d in enumerate(ps):
            txt = (d / "pass.md").read_text(errors="ignore") if (d / "pass.md").is_file() else ""
            title = (re.search(r"(?m)^#\s+(.+)$", txt) or [None, d.name])[1].strip()
            summ = (re.search(r"(?ms)^## Summary\s*\n(.*?)(?=^## |\Z)", txt) or [None, ""])[1]
            summ = re.split(r"(?<=[.!?])\s+", " ".join(summ.split()), maxsplit=1)[0]
            k, _, md = d.name.partition("-")
            out.append([mk if i == 0 else "✅", re.sub(r"^p\d+-\d+ · ", "", title), f"{k} · {md[:2]}-{md[2:]}" if len(md) == 4 else k, summ])
        if not ps:
            hl = line(r / "result" / "runtime.yaml", "headline").strip("'\"")
            out.append([mk, hl or r.name, r.name, hl])
    return out
bands = line(B / "board.md", "bands")
topics = [[m.group(1), m.group(2).strip()] for m in re.finditer(r"j(\d)N\s+([^·]+)", bands)]
topics.sort(key=lambda x: -int(x[0]))
jobs, tnames, R = [], {}, {}
for j in sorted(B.glob("j[0-9][0-9]_*")):
    face = j / f"{j.name}.md"
    jn = j.name[:3]
    tb = line(face, "bands")
    tnames[jn] = {m.group(1): m.group(2).strip() for m in re.finditer(r"t(\d)N\s+([^·]+)", tb)}
    ts = []
    for t in sorted(j.glob("t[0-9][0-9]_*")):
        tn = t.name[:3]
        rr = rounds(t)
        R[f"{jn}/{tn}"] = rr
        ts.append([tn, head(t / f"{t.name}.md") or t.name, t.name])
    jobs.append([jn, head(face) or j.name, ts, line(face, "goal"), line(face, "close")])
print("window.FEW = " + json.dumps({"topics": [[a, b] for a, b in topics], "ttopics": {}, "rounds": R,
      "taskTopicNames": tnames, "jobs": jobs}, ensure_ascii=False, indent=0) + ";")
