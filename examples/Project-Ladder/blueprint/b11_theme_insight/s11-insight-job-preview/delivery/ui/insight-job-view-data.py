"""Run: python3 insight-job-view-data.py <an insight Board folder> > insight-job-view-data.js.
Print the s11 Segment grid's data, read from the Board's folders: its Jobs (one question version x one data version),
their Tasks (one question each, grouped by DIKW level), each Task's segment Runs, its answer, and the Job's
comparison with the previous Job (reports/vs-jNN.md). Nothing is typed here; a field the Board lacks stays empty."""
import json, re, sys
from pathlib import Path

B = Path(sys.argv[1])
LEVELS = {"D": "🗂 Data", "I": "📈 Information", "K": "🧠 Knowledge", "W": "🧭 Wisdom", "X": "🎯 Executive"}
ANSWER = {"answered": "✅", "partial": "🔶", "open": "⬜"}
RUN = {"ok": "✅", "done": "✅", "running": "🏃", "failed": "❗", "refused": "❗", "planned": "⬜"}


def text(f):
    return f.read_text(errors="ignore") if f.is_file() else ""


def front(f):
    """The face's leading --- block as flat key: value pairs (nested takeaways kept as a dict)."""
    m = re.match(r"(?s)---\n(.*?)\n---", text(f))
    out, sub = {}, None
    for ln in (m.group(1).splitlines() if m else []):
        if re.match(r"^\s+\S", ln) and sub is not None:
            k, _, v = ln.strip().partition(":")
            out[sub][k.strip()] = v.strip().strip("'\"")
            continue
        k, _, v = ln.partition(":")
        v = v.strip().strip("'\"")
        sub = k.strip() if not v else None
        out[k.strip()] = {} if not v else v
    return out


def word(face, key):
    """A face field as text: an empty field (read as a nested block) is empty."""
    v = face.get(key, "")
    return v if isinstance(v, str) else ""


def line(f, key):
    return (re.search(rf"(?m)^{key}:\s*(.+)$", text(f)) or [None, ""])[1].strip().strip("'\"")


def book_segments(face):
    """The segments the Job's question version fixes (its partitions.md, in order), then cross."""
    rel = B.parent.parent / str(face.get("prototype") or "")
    names = re.findall(r"(?m)^- name: (\S+)", text(rel / "partitions.md"))
    return [n for n in dict.fromkeys(names) if n != "cross"] + ["cross"]


def segments(t, takeaways, order):
    """One row per segment Run (rNN_<segment>, a segment of the version or cross), in the version's segment order;
    a soft or collection Run (run-…, rNN_collect_…) is not a segment."""
    rows = []
    for r in (d for d in (t / "runs").glob("r[0-9][0-9]_*") if d.is_dir()):
        seg = r.name.split("_", 1)[1]
        if seg not in order:
            continue
        rt = r / "result" / "runtime.yaml"
        st = line(rt, "status") or line(r / "run.yaml", "status")
        why = line(rt, "reason") if st in ("refused", "failed") else ""
        rows.append([RUN.get(st, "⬜"), seg, r.name, why or takeaways.get(seg, "")])
    return sorted(rows, key=lambda x: order.index(x[1]))


def compare(j):
    """reports/vs-jNN.md: its heading, and each question's row (previous, this, held or changed, why)."""
    for f in sorted((j / "reports").glob("vs-j*.md")):
        t = text(f)
        title = (re.search(r"(?m)^#\s+(.+)$", t) or [None, ""])[1]
        rows = {}
        for m in re.finditer(r"(?m)^\| (\w\d\d) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", t):
            rows[m.group(1)] = [m.group(2), m.group(3), m.group(4), m.group(5)]
        return {"title": title, "against": str(front(f).get("compares") or "")[:3], "rows": rows}
    return {}


jobs = []
for j in sorted(B.glob("j[0-9][0-9]_*"), reverse=True):
    face = front(j / f"{j.name}.md")
    order = book_segments(face)
    tasks = []
    for t in sorted(j.glob("t[0-9][0-9]_*")):
        f = front(t / f"{t.name}.md")
        m = re.match(r"t(\d\d)_([A-Z])(\d\d)_(.+)", t.name)
        if not m:
            continue
        q = f"{m.group(2)}{m.group(3)}"
        title = (re.search(r"(?m)^#\s+\S+ · (.+)$", text(t / f"{t.name}.md")) or [None, m.group(4)])[1]
        tasks.append({"id": f"t{m.group(1)}", "q": q, "level": m.group(2), "name": title, "folder": t.name,
                      "mark": ANSWER.get(word(f, "answer-status") or "open", "⬜"), "ask": word(f, "goal"),
                      "answer": word(f, "answer"), "sure": word(f, "how-sure"),
                      "segments": segments(t, f.get("takeaways") or {}, order)})
    jn = j.name[:3]
    data = face.get("data", "")
    jobs.append({"id": jn, "release": face.get("release", ""), "data": data, "prep": face.get("prep", ""), "folder": j.name,
                 "closed": face.get("state") == "closed", "goal": face.get("goal", ""),
                 "moved": face.get("moved", ""), "previous": str(face.get("previous") or "")[:3],
                 "order": order, "tasks": tasks, "compare": compare(j)})

versions = {v: l for v, l in re.findall(r"(?m)^- version: (\S+)\n\s+label: (.+)$", text(B / "board.md"))}
print("window.INSIGHT = " + json.dumps({"board": B.name, "levels": LEVELS, "versions": versions, "jobs": jobs},
                                       ensure_ascii=False, indent=0) + ";")
