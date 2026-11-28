"""Run: python3 book-job-view-data.py <a Question Book folder> > book-job-view-data.js  (needs PyYAML).
Print the s12 preview's data, read from the Question Book's folders: its Jobs (one question version each), the
questions each version holds (release.yaml: kept from an earlier version or new in this one), each question's ask,
method, needs and segments (question.md), the version's segments (partitions.md) and the open proposals. Nothing is
typed here; a field the Book lacks stays empty."""
import json
import re
import sys
from pathlib import Path

import yaml

B = Path(sys.argv[1])
LEVELS = {"D": "🗂 Data", "I": "📈 Information", "K": "🧠 Knowledge", "W": "🧭 Wisdom", "X": "🎯 Executive"}


def front(f):
    m = re.match(r"(?s)---\n(.*?)\n---", f.read_text(errors="ignore")) if f.is_file() else None
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def body_line(f):
    """The first prose paragraph under the face's heading, as one line."""
    t = re.sub(r"(?s)^---\n.*?\n---\n", "", f.read_text(errors="ignore")) if f.is_file() else ""
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip() and not p.lstrip().startswith("#")]
    return " ".join(paras[0].split()) if paras else ""


def question(task: Path, change: str):
    q = front(task / "question.md")
    m = re.match(r"t(\d\d)_([A-Z])(\d\d)_", task.name)
    parts = q.get("partitions") or {}
    return {"id": f"t{m.group(1)}", "q": f"{m.group(2)}{m.group(3)}", "level": m.group(2), "name": q.get("name", ""),
            "question": q.get("question", ""), "ask": q.get("ask", ""), "change": change,
            "home": task.parent.name[:3], "method": q.get("method") or {},
            "needs": [[k, v.get("kind", ""), v.get("what", "")] for k, v in (q.get("needs") or {}).items()],
            "asked": parts.get("asked", "") if isinstance(parts, dict) else "",
            "agreed": str(q.get("agreed") or "")}


jobs = []
for j in sorted(B.glob("j[0-9][0-9]_*"), reverse=True):
    face = front(j / f"{j.name}.md")
    rel = yaml.safe_load((j / "release.yaml").read_text()) if (j / "release.yaml").is_file() else {}
    qs = [question((j / v["task"]).resolve(), v.get("change", "")) for v in (rel.get("questions") or {}).values()
          if (j / v["task"]).is_dir()]
    segs = front(j / "partitions.md").get("partitions") or []
    jobs.append({"id": j.name[:3], "release": face.get("release", ""), "folder": j.name, "title": face.get("title", ""),
                 "closed": face.get("state") == "closed", "signed": str(face.get("signed") or ""),
                 "from": face.get("from") or "", "goal": face.get("goal", ""), "about": body_line(j / f"{j.name}.md"),
                 "segments": [[s.get("name", ""), s.get("why", "")] for s in segs], "tasks": qs})

proposals = [[p.stem, body_line(p)] for p in sorted((B / "proposals").glob("*.md")) if p.name != "README.md"]
print("window.BOOK = " + json.dumps({"book": B.name, "levels": LEVELS, "jobs": jobs, "proposals": proposals},
                                    ensure_ascii=False, indent=0) + ";")
