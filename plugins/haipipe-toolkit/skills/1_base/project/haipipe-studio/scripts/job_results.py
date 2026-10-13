"""A Job's current results as a Studio topic, read from its Runs on every build (JL 261012: "for each jNN, make
the sNN to show what are the current results").

    python job_results.py <block> [--dry-run]                    one topic per Job the Block's results topics miss
    python job_results.py <block> --jobs j11_x,j12_y --slug <s> --title '<t>'   one topic for a group of Jobs
    python job_results.py --draw <topic folder>                 redraw one topic (what its builder calls)

The topic is the Block's (`studio/sNN-<jNN>-<job>-results/`, numbered in the runs band s21-s29): Block, Job and Task
views share it, and a Job keeps no studio/ of its own. A Block with more Jobs than the band holds groups them, one
topic per group of Jobs that share their Tasks, one frame per Job inside it.

What is read from disk on every build, never typed: each Task of the Job, each of its Runs (`runs/<run>/` with
`result/`, or the older `runs/<run>.sh` with `results/<run>/`), the Run's state (`result/runtime.yaml`, else
`run.yaml`), its headline values and, for a source Run, its subject's title. What the face holds, in its `results:`
yaml: per Job a `reading` (the frame's key point: what the results say now), per Run the values to `show` (a file in
its result and a key inside it), and the `open` points. A Run the face names no values for shows the numbers its
receipts name by a known key (accuracy, pass rate, tok/s, latency, loss), at most three.

How it looks: excalidraw-studio's principles and draw.py (one screen-sized frame per Job, the reading as its key
point, the Tasks as a map of boxes joined by arrows, the density badge). The writer is canvas.write: a person's marks
survive a rebuild.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "display" / "excalidraw-studio" / "scripts"))
import canvas  # noqa: E402
from draw import INK, RED, W, Drawing  # noqa: E402

try:
    import yaml
except ImportError:                       # the receipts still read as JSON; a face's yaml needs PyYAML
    yaml = None

BAND = (21, 29)                           # s21-s29, runs and skills: a Run's results
JOB = re.compile(r"^j\d+[_-]")
TASK = re.compile(r"^t\d+[_-]")
RUN = re.compile(r"^r\d+[_-]")
BEGIN, END = "<!-- job-results:start -->", "<!-- job-results:end -->"
CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
DONE = {"completed", "complete", "done", "success", "succeeded", "ok", "finished", "pass", "passed", "closed",
        "answered", "reviewed", "read"}
FAILED = {"failed", "error", "crashed", "oom", "killed", "timeout", "invalid"}
PARTLY = {"blocked", "partial", "partly", "running", "in_progress", "active", "receipt present", "draft",
          "needs_review", "pending_review", "legacy_import"}
TASK_TEXT, RUN_TEXT, MOST_RUNS, TASKS_A_ROW = 30, 22, 12, 4


# ── reading the work ─────────────────────────────────────────────────────────────────────────────────────────
def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def load(path: Path):
    """A receipt's data: JSON, or YAML when PyYAML is there; None when unreadable or too large."""
    if not path.is_file() or path.stat().st_size > 4_000_000:
        return None
    text = read(path)
    try:
        if path.suffix == ".json":
            return json.loads(text)
        if path.suffix in (".yaml", ".yml") and yaml:
            return yaml.safe_load(text)
    except Exception:                     # a broken receipt reads as missing, never stops the build
        return None
    return None


def face_of(folder: Path) -> Path | None:
    for name in (f"{folder.name}.md", "board.md", "job.md", "task.md", "README.md"):
        if (folder / name).is_file():
            return folder / name
    return None


def title_of(folder: Path) -> str:
    """The face's own title (a `# ` heading, a `title:` line, or an ASCII heading), else the folder's words; a title
    that only repeats the folder name gives way to the face's first sentence."""
    face = face_of(folder)
    lines = read(face).splitlines() if face else []
    plain = re.sub(r"^[a-z]\d+[_-]", "", folder.name).replace("_", " ")
    for i, line in enumerate(lines):
        m = re.match(r"^#\s+(.+?)\s*$", line) or re.match(r"^title:\s*(.+?)\s*$", line)
        ascii_ = not m and i + 1 < len(lines) and re.fullmatch(r"=+", lines[i + 1].strip() or "-") and line.strip()
        if ascii_:
            m = re.match(r"^(.+?)\s*$", line)
        if m:
            title = re.sub(r"^[a-z]\d+\s*[·:-]\s*", "", m.group(1).strip().strip('"'))
            if title == folder.name and not ascii_:         # `# j08_x`: the folder's words, never its prose
                return plain
            if title == folder.name:                        # an ASCII heading that is only the folder name
                line = first_line(lines[i + 1:])
                return line if len(line) > 12 else plain
            return title
    return plain


def first_line(lines: list[str]) -> str:
    """The first sentence of prose: not a heading, a rule, a field line or a list item."""
    for line in lines:
        t = line.strip()
        if t.startswith("#"):
            break
        if (t.startswith("<") and t.endswith(">")) or t.startswith(">"):
            continue                                        # a template's placeholder, not the face's words                                           # the next section: no prose under the title
        if not t or re.fullmatch(r"[=\-`~]+.*", t) or re.match(r"^[A-Za-z_ -]+:\s", t) or re.match(r"^([-*|]|\d+\.)\s", t):
            continue
        return re.split(r"(?<=[.!?])\s", t)[0][:110]
    return ""


def field(folder: Path, name: str) -> str:
    m = re.search(rf"(?im)^\**{name}:?\**:?\s*(.+?)\s*$", read(face_of(folder)) if face_of(folder) else "")
    value = (m.group(1).strip().strip('"') if m else "")
    return "" if value.lower() in ("open", "<open>", "none", "-") else value


def kids(folder: Path, pattern) -> list[Path]:
    return sorted(p for p in folder.iterdir() if p.is_dir() and pattern.match(p.name)) if folder.is_dir() else []


def runs_of(task: Path) -> list[dict]:
    """Each Run of a Task: its name, folder, result folder; the one-folder layout first, then the older one."""
    found: dict[str, dict] = {}
    runs, results = task / "runs", task / "results"
    for p in sorted(runs.iterdir()) if runs.is_dir() else []:
        if p.is_dir() and RUN.match(p.name):
            result = p / "result" if (p / "result").is_dir() else results / p.name
            found[p.name] = {"name": p.name, "dir": p, "result": result}
        elif p.suffix == ".sh" and RUN.match(p.stem) and p.stem not in found:
            found[p.stem] = {"name": p.stem, "dir": runs, "result": results / p.stem}
    for p in sorted(results.iterdir()) if results.is_dir() else []:
        if p.is_dir() and RUN.match(p.name) and p.name not in found:
            found[p.name] = {"name": p.name, "dir": p, "result": p}
    return [found[k] for k in sorted(found)]


def exit_code(result: Path):
    """A nonzero returncode in the Run's metrics.json, else None."""
    data = load(result / "metrics.json") if (result / "metrics.json").is_file() else None
    if isinstance(data, dict):
        for k in ("returncode", "return_code", "exit_code"):
            if isinstance(data.get(k), int) and data[k] != 0:
                return data[k]
    return None


def state_of(run: dict) -> str:
    """The Run's state word: its runtime receipt first (closest to the result), then its card."""
    result = run["result"]
    for path in (result / "runtime.yaml", run["dir"] / "run.yaml"):
        data = load(path) if yaml else None
        if data is None and path.is_file():                     # no PyYAML: read the one line
            m = re.search(r"(?m)^status:\s*(\S+)", read(path))
            data = {"status": m.group(1)} if m else None
        if isinstance(data, dict) and data.get("status"):
            state = str(data["status"]).strip().lower()
            code = exit_code(result) if state in DONE else None
            return f"failed (exit {code})" if code else state     # completed, yet its metrics say it exited nonzero
        if isinstance(data, dict) and isinstance(data.get("return_code"), int):
            return "completed" if data["return_code"] == 0 else "failed"
    if result.is_dir() and any(f.is_file() for f in result.iterdir()):
        return "receipt present"
    return "no result yet"


def mark(state: str) -> str:
    s = state.replace("-", "_")
    if s in DONE:
        return "✅"
    if s in FAILED or s.startswith("fail"):
        return "❌"
    if s in PARTLY or s.startswith(("block", "partial", "running")):
        return "🔶"
    return "⬜"


def subject_of(run: dict) -> str:
    """A source Run's subject: what was read, by its own title."""
    data = load(run["result"] / "runtime.yaml") or load(run["dir"] / "run.yaml") or {}
    subject = data.get("subject") if isinstance(data, dict) else None
    if isinstance(subject, dict) and subject.get("title"):
        return str(subject["title"]).strip()
    card = run["result"] / f"{run['name']}.md"
    for line in read(card).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


# ── values: named by the face, else found by a known key ─────────────────────────────────────────────────────
def dig(data, key: str):
    for part in key.split(".") if key else []:
        if isinstance(data, dict):
            data = data.get(part)
        elif isinstance(data, list) and part.lstrip("-").isdigit():
            i = int(part)
            data = data[i] if -len(data) <= i < len(data) else None
        else:
            return None
    return data


def number(v, fmt: str = "") -> str:
    if isinstance(v, bool) or v is None:
        return "—" if v is None else str(v)
    if not isinstance(v, (int, float)):
        return str(v)
    if fmt == "pct":
        v = v * 100 if -1.0 <= v <= 1.0 else v
        return f"{v:.1f}%"
    if fmt == "int" or (isinstance(v, int) and abs(v) >= 1):
        return f"{int(round(v)):,}"
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    if abs(v) >= 100:
        return f"{v:.1f}"
    if abs(v) >= 10:
        return f"{v:.1f}"
    return f"{v:.3g}"


def at_value(result: Path, at: str, fmt: str):
    """`file:key.inside` read from the Run's result folder (a glob picks the first match)."""
    file, _, key = at.partition(":")
    paths = sorted(result.glob(file.strip())) if any(c in file for c in "*?[") else [result / file.strip()]
    for path in paths:
        v = dig(load(path), key.strip())
        if v is not None and not isinstance(v, (dict, list)):
            return number(v, fmt)
    return None


def shown(run: dict, picks: list) -> list[str]:
    """The face's picks for this Run, each `label value` (a list of `at` reads as before → after)."""
    out = []
    for p in picks:
        ats = p.get("at") if isinstance(p.get("at"), list) else [p.get("at", "")]
        vals = [at_value(run["result"], a, str(p.get("fmt", ""))) for a in ats]
        unit = f" {p['unit']}" if p.get("unit") else ""
        if all(v is None for v in vals):
            out.append(f"❓ {p.get('label', ats[0])}: not in the result")
        else:
            out.append(f"{p.get('label', '')} {' → '.join(v or '—' for v in vals)}{unit}".strip())
    return out


KNOWN = [   # (rank, key pattern, label, format, unit): the numbers a receipt names by a known key
    (0, r"(^|[._])(acc|accuracy|exact_match|em|strict_acc)$", "acc", "pct", ""),
    (0, r"(pass_rate|pass@1|passrate|win_rate|score_mean)$", "pass rate", "pct", ""),
    (1, r"(decode|gen|generation)[a-z_]*(tok_s|tokens_per_s(ec(ond)?)?|tps)$", "decode", "", "tok/s"),
    (1, r"prefill[a-z_]*(tok_s|tokens_per_s(ec(ond)?)?|tps)$", "prefill", "", "tok/s"),
    (2, r"(throughput|output)[a-z_]*(tok_s|tokens_per_s(ec(ond)?)?|tps)$", "throughput", "", "tok/s"),
    (2, r"(^|[._])(tok_s|tokens_per_s(ec(ond)?)?|tps|avg_ts)([._]|$)", "speed", "", "tok/s"),
    (3, r"ttft[a-z_]*(ms|_s)?$", "TTFT", "", ""),
    (3, r"(e2e|latency)(?!.*(tok|tps))[a-z_0-9]*$", "latency", "", ""),
    (4, r"(loss_last|final_loss|eval_loss|train_loss)$", "loss", "", ""),
    (5, r"(peak_gpu_gb|peak_vram_gb|vram_gb)$", "peak GPU", "", "GB"),
]
SKIP_KEY = re.compile(r"(^|[._])(config|args|hparams|hyperparameters|generate|sampling|cfg)([._]|$)")


def flat(data, prefix=""):
    if isinstance(data, dict):
        for k, v in data.items():
            yield from flat(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(data, (int, float)) and not isinstance(data, bool):
        yield prefix, data


PAIRS = (("base", "trained"), ("before", "after"), ("pre", "post"), ("baseline", "finetuned"))


def known(key: str):
    """(rank, label, format, unit) when a key names a known kind of number, else None."""
    low = key.lower()
    for rank, pat, label, fmt, unit in KNOWN:
        if re.search(pat, low):
            return rank, label, fmt, unit
    return None


def found_values(run: dict, most: int = 3) -> list[str]:
    """Numbers named by a known key in the Run's JSON and runtime receipts, the most telling first: a before and
    after pair as one value (`acc 26.1% → 41.0%`), then the rest; a delta is left out, the pair already says it."""
    result, data = run["result"], {}
    files = sorted(result.glob("*.json")) + [result / "runtime.yaml"] if result.is_dir() else []
    for path in files:
        for key, v in flat(load(path)):
            if not SKIP_KEY.search(key.lower()) and "delta" not in key.lower() and key.count(".") <= 2:
                data.setdefault(key, v)
    best, used_ = {}, set()
    for key, v in data.items():
        for x, y in PAIRS:
            hits = list(re.finditer(rf"(^|[._]){x}([._]|$)", key))
            if not hits:
                continue
            hit = hits[-1]                                  # the marker nearest the value: paired.A.base_acc
            other = key[:hit.start()] + hit.group(1) + y + hit.group(2) + key[hit.end():]
            stem = (key[:hit.start()] + (hit.group(2) if hit.group(1) == "" else hit.group(1)) + key[hit.end():]).strip("._")
            k = known(stem) or known(stem.split(".")[-1])
            if other in data and k:
                rank, label, fmt, unit = k
                parts = stem.split(".")
                lab = parts[-1] if label in ("acc", "pass rate") else label
                lab = (" ".join(parts[-2:-1] + [lab]) if len(parts) > 1 else lab).replace("_", " ")
                best.setdefault(lab, ((-1, stem.count("."), rank), f"{lab} {number(v, fmt)} → "
                                      f"{number(data[other], fmt)}{(' ' + unit) if unit else ''}"))
                used_ |= {key, other}
            break
    for key, v in data.items():
        k = known(key)
        if key in used_ or not k:
            continue
        rank, label, fmt, unit = k
        lab = label if label not in ("acc", "pass rate") or "." not in key else key.split(".")[-2] + " " + label
        lab = lab.replace("_", " ")
        cand = ((rank, key.count("."), 0), f"{lab} {number(v, fmt)}{(' ' + unit) if unit else ''}")
        if lab not in best or cand[0] < best[lab][0]:
            best[lab] = cand
    return [s_ for _, s_ in sorted(best.values())][:most]


# ── the topic's face ─────────────────────────────────────────────────────────────────────────────────────────
def results_yaml(face: Path) -> dict:
    m = re.search(r"```yaml\s*\n(results:.*?)```", read(face), re.S)
    if not (m and yaml):
        return {}
    try:
        return (yaml.safe_load(m.group(1)) or {}).get("results") or {}
    except Exception as err:              # a typo in the face is said, not hidden
        print(f"{face.name}: its results: yaml does not read ({err}); drawing from disk only", file=sys.stderr)
        return {}


def picks_for(cfg: dict, task: Path, run: dict) -> list:
    show = cfg.get("show") or {}
    return show.get(f"{task.parent.name}/{task.name}/{run['name']}") or show.get(f"{task.name}/{run['name']}") \
        or show.get(run["name"]) or []


def shared_tickets(runs: list[dict]) -> set[str]:
    """Run folders whose ticket other Runs of the Task call (`exec ../<run>/<run>.sh`): a worker, not a result."""
    called = set()
    for run in runs:
        ticket = run["dir"] / f"{run['name']}.sh"
        called |= set(re.findall(r"\.\./(r\d+[A-Za-z0-9_.-]*)/\1\.sh", read(ticket)))
    return called


def job_rows(block: Path, job: Path, cfg: dict) -> list[dict]:
    rows = []
    for task in kids(job, TASK):
        runs, all_runs = [], runs_of(task)
        shared = shared_tickets(all_runs)
        for run in all_runs:
            if run["name"] in shared and not (run["result"].is_dir() and any(run["result"].iterdir())):
                continue                                  # named once on the Task's box instead
            st = state_of(run)
            picks = picks_for(cfg, task, run)
            vals = shown(run, picks) if picks else found_values(run)
            subj = "" if vals else subject_of(run)
            runs.append({**run, "state": st, "mark": mark(st), "values": vals, "subject": subj})
        rows.append({"task": task, "title": title_of(task), "runs": runs, "shared": sorted(shared),
                     "develops": field(task, "develops")})
    return rows


def run_line(r: dict, with_name: bool = True) -> str:
    name = re.sub(r"^(r\d+)_", r"\1 ", r["name"]) if with_name else ""
    what = " · ".join(r["values"]) if r["values"] else (r["subject"] or r["state"])
    return f"{r['mark']} {name} · {what}".replace("  ", " ")


def tally(rows: list[dict]) -> str:
    runs = [r for t in rows for r in t["runs"]]
    if not runs:
        return "no Run yet"
    parts = [(sum(r["mark"] == m for r in runs), w) for m, w in
             (("✅", "done"), ("🔶", "partly"), ("❌", "failed"), ("⬜", "not run"))]
    return f"{len(runs)} Run{'s' if len(runs) > 1 else ''}: " + ", ".join(f"{n} {w}" for n, w in parts if n)


def rel(path: Path, base: Path) -> str:
    return Path(os.path.relpath(path, base)).as_posix()


def ledger(topic: Path, jobs: list[Path], all_rows: dict) -> str:
    """The face's generated part: every Run with its state, its values and a link to its result."""
    out = [BEGIN, "", "Runs on disk", "------------", "",
           "Read from each Run's receipts on every build; edit the `results:` yaml above, never this list.", ""]
    for job in jobs:
        out += [f"**[{job.name}]({rel(face_of(job) or job, topic)})** · {tally(all_rows[job.name])}", ""]
        for t in all_rows[job.name]:
            out.append(f"- [{t['task'].name}]({rel(t['task'], topic)}/): {t['title']}")
            for r in t["runs"]:
                link = r["result"] if r["result"].is_dir() else r["dir"]
                out.append(f"  - {r['mark']} [{r['name']}]({rel(link, topic)}/) · "
                           f"{' · '.join(r['values']) or r['subject'] or r['state']}")
            if not t["runs"]:
                out.append("  - ⬜ no Run yet")
        out.append("")
    return "\n".join(out + [END])


def new_face(nn: int, slug: str, title: str, jobs: list[Path], topic: Path) -> str:
    name = f"s{nn:02d} · {title}"
    tasks = sum(len(kids(j, TASK)) for j in jobs)
    which = ", ".join(f"`{j.name}`" for j in jobs)
    feeds = sorted({q for j in jobs for q in re.findall(r"q\d\d_[A-Za-z0-9_]+", field(j, "answers"))})
    yml = ["results:", "  reading:"] + [f"    {j.name}: ''" for j in jobs] + \
          ["  show: {}", "  open: []"]
    return "\n".join([
        name, "=" * len(name), "",
        "**Tags:** `Results`", "",
        "**Stage:** explore", "",
        f"**Topic:** What {which} has produced so far: each of its {tasks} Tasks, every Run's state and its headline "
        "values, read from the Runs' receipts on every build.", "",
        f"**Feeds:** `reports/` {' · '.join(feeds)}" if feeds else "**Feeds:** none yet; the Job's face names no Question.",
        "", f"**Job:** {' · '.join(f'[{j.name}]({rel(face_of(j) or j, topic)})' for j in jobs)}", "",
        "", "Results", "-------", "",
        "The words the drawing shows: per Job its `reading` (the key point, what the results say now), per Run the "
        "values to `show` (`at: <file in its result>:<key.inside>`, a list for before → after; `fmt: pct`), and the "
        "`open` points. A Run with no `show` lists the numbers its receipts name by a known key.", "",
        "```yaml", *yml, "```", "",
        BEGIN, END, "",
        "", "Files", "-----", "",
        "```text", f"{topic.name}/", f"├── {topic.name}.md           this face",
        f"├── {topic.name}.excalidraw   one frame per Job; a person's marks are kept",
        f"├── {topic.name}.png          its preview",
        f"└── build_s{nn:02d}_{slug.replace('-', '_')}.py   calls haipipe-studio's job_results.py", "```", "",
        "", "Decided", "-------", "",
        f"s{nn:02d}-D01 · One Block topic per Job shows its current results, read from its Runs on every build "
        "(JL 261012)", "",
        "", "Open", "----", "",
        "1. Write each Job's reading: what its results say now, in one or two sentences.", "",
        "(write here, or mark the drawing in red)", ""])


def builder_text(topic: Path, nn: int, title: str, script: str) -> str:
    """The topic's builder: a few lines that call this generator through the SPACE's Tools link, as s00's does."""
    space = next((p for p in (topic, *topic.parents) if (p / "env.sh").is_file() and (p / "Tools").exists()), None)
    scripts = space / "Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts" if space else HERE
    return (f'"""s{nn:02d} · {title}: drawn by haipipe-studio\'s job_results.py from the Runs on disk and this '
            f"face's results: yaml; a person's marks on the drawing are kept.\n\n    python {script}\n\"\"\"\n"
            "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
            f'sys.path.insert(0, str((HERE / "{rel(scripts, topic)}").resolve()))\n'
            "import job_results  # noqa: E402\n\nif __name__ == \"__main__\":\n    job_results.draw(HERE)\n")


# ── the drawing ──────────────────────────────────────────────────────────────────────────────────────────────
WIDE = re.compile(r"[\u2e80-\u303f\u3040-\u9fff\uac00-\ud7af\uf900-\ufaff\uff00-\uffef]")
TOKEN = re.compile(r"[\u2e80-\u303f\u3040-\u9fff\uac00-\ud7af\uf900-\ufaff\uff00-\uffef]|\s+|"
                   r"[^\s\u2e80-\u303f\u3040-\u9fff\uac00-\ud7af\uf900-\ufaff\uff00-\uffef]+")


def char_w(ch: str, size: float) -> float:
    """A character's width: Chinese, Japanese and Korean are full width, an emoji a little more."""
    return size * (1.15 if ord(ch) >= 0x1F000 else 1.0 if WIDE.match(ch) else 0.53)


def wrap(s: str, width: float, size: float) -> list[str]:
    """Lines that fit `width`: a Latin word stays whole, Chinese breaks between any two characters (draw.py's wrap
    counts every character as narrow, so a Chinese title ran past its box)."""
    lines, cur, cur_w = [], "", 0.0
    for tok in TOKEN.findall(" ".join(str(s).split())):
        if tok.isspace():
            if cur:
                cur, cur_w = cur + " ", cur_w + size * 0.3
            continue
        tw = sum(char_w(c, size) for c in tok)
        if cur.strip() and cur_w + tw > width:
            lines.append(cur.rstrip())
            cur, cur_w = "", 0.0
        while tw > width and len(tok) > 1:                 # one token wider than the box: cut it
            cut, w_ = 0, 0.0
            while cut < len(tok) and w_ + char_w(tok[cut], size) <= width:
                w_ += char_w(tok[cut], size)
                cut += 1
            lines.append(tok[:max(cut, 1)])
            tok = tok[max(cut, 1):]
            tw = sum(char_w(c, size) for c in tok)
        cur, cur_w = cur + tok, cur_w + tw
    if cur.strip() or not lines:
        lines.append(cur.rstrip())
    return lines


def tall(s: str, width: float, size: float) -> float:
    return len(wrap(s, width, size)) * size * 1.25


def para(d: Drawing, x: float, y: float, s: str, width: float, size: float, color=None) -> float:
    """Wrapped text, red when it opens with ❓ or ❌; returns the y below it."""
    color = color or (RED if str(s).lstrip().startswith(("❓", "❌")) else INK)
    lines = wrap(s, width, size)
    e = d.text(x, y, "\n".join(lines), size, color)
    e["width"] = min(width, max(sum(char_w(c, size) for c in ln) for ln in lines))   # measured, not len x 0.55
    return y + e["height"]


def layout(rows: list[dict], most: int) -> list[tuple]:
    """The Task rows: (chunk, box width, [(title, lines)], row height), at most `most` Runs listed in a box."""
    out, gap = [], 70
    for i in range(0, len(rows), TASKS_A_ROW):
        chunk = rows[i:i + TASKS_A_ROW]
        bw = (W - 80 - gap * (len(chunk) - 1)) / len(chunk)
        bodies = []
        for t in chunk:
            lines = ([f"develops: {t['develops']}"] if t["develops"] else []) + \
                [run_line(r) for r in t["runs"][:most]]
            if not t["runs"]:
                lines.append("⬜ no Run yet")
            if len(t["runs"]) > most:
                lines.append(f"… {len(t['runs']) - most} more Runs, listed in the face")
            if t["shared"]:
                lines.append(f"🧩 shared ticket: {', '.join(t['shared'])}, called by the Runs above")
            bodies.append((f"{t['task'].name[:3]} · {t['title']}", lines))
        hh = max(24 + tall(ti, bw - 44, TASK_TEXT) + 14 +
                 sum(tall(ln, bw - 44, RUN_TEXT) + 8 for ln in ls) + 18 for ti, ls in bodies)
        out.append((chunk, bw, bodies, hh))
    return out


def task_boxes(d: Drawing, rows: list[dict], y: float, room: float = 1e9) -> float:
    """The Tasks as boxes, four a row, joined by arrows in their order; each box lists its Runs, fewer of them when
    the frame would pass FRAME_MAX's height (`room`, the height left). Returns the y below them."""
    for most in (MOST_RUNS, 9, 7, 5, 3):
        rows_ = layout(rows, most)
        if sum(hh + 60 for *_, hh in rows_) <= room:
            break
    gap = 70
    for n, (chunk, bw, bodies, hh) in enumerate(rows_):
        for k, (ti, ls) in enumerate(bodies):
            bx = 40 + k * (bw + gap)
            d.box(bx, y, bw, hh, INK, 2.5)
            yy = para(d, bx + 22, y + 18, ti, bw - 44, TASK_TEXT) + 14
            for ln in ls:
                yy = para(d, bx + 22, yy, ln, bw - 44, RUN_TEXT) + 8
            if k:
                d.line([(bx - gap + 6, y + 44), (bx - 6, y + 44)], sw=3)
                d.text(bx - gap + 8, y + 8, "then", 20)
        if n + 1 < len(rows_):                           # the next row follows on: a line down and back
            mid = y + hh + 30
            d.line([(40 + (len(chunk) - 1) * (bw + gap) + bw / 2, y + hh + 4),
                    (40 + (len(chunk) - 1) * (bw + gap) + bw / 2, mid), (40 + bw / 2, mid),
                    (40 + bw / 2, mid + 26)], sw=3)
        y += hh + 60
    return y


def heading(d: Drawing, title: str, sub: str) -> float:
    """The frame's title at 60 px and its line below, both wrapped clear of the density badge; returns the y below."""
    y = para(d, 40, 22, title, W - 700, 60) + 10
    return para(d, 40, y, sub, W - 700, 21) + 28


def job_frame(d: Drawing, mark_: str, job: Path, rows: list[dict], cfg: dict) -> dict:
    f = d.frame(f"{mark_} {job.name[:3]} · {title_of(job)}")
    top = heading(d, f"{job.name[:3]} · {title_of(job)}",
                  f"{field(job, 'goal') or 'goal: not written on the Job face'}   ·   {tally(rows)}")
    reading = str((cfg.get("reading") or {}).get(job.name) or "").strip()
    if not reading:
        reading = "❓ No reading yet: write what these results say in the face's results: yaml. " + tally(rows) + "."
    kh = tall("🎯 " + reading, W - 140, 30) + 44
    d.key(40, top, W - 80, kh)
    para(d, 70, top + 22, ("" if reading.startswith("❓") else "🎯 ") + reading, W - 140, 30)
    opens = opens_of(cfg, job)
    below = sum(tall("❓ " + o, W - 80, 24) + 8 for o in opens)
    y = task_boxes(d, rows, top + kh + 40, 1600 - 30 - below - (top + kh + 40))
    for o in opens:
        y = para(d, 40, y, o if o.startswith("❓") else "❓ " + o, W - 80, 24, RED) + 8
    f["height"] = max(y + 30, 500)                      # as tall as its content: a thin frame is not padded
    if f["height"] > 1600:
        canvas.reads_down(f)
    d.badge(f)
    return f


def opens_of(cfg: dict, job: Path) -> list[str]:
    """The face's open points for this Job: those naming it (`j11: …`), and those naming no Job."""
    out = []
    for o in (cfg.get("open") or []):
        m = re.match(r"^(j\d+[A-Za-z0-9_]*)\s*:", str(o))
        if not m or m.group(1) == job.name or (m.group(1) == job.name[:3]):   # the full name, where two share a jNN
            out.append(str(o))
    return out[:6]


def overview_frame(d: Drawing, title: str, jobs: list[Path], all_rows: dict, cfg: dict) -> dict:
    """A group's first frame: its key point (`reading.overview`, else which Jobs have results), then one row per
    Job: its tally, its reading, the first values of its done Runs, and the open points of a Job with no frame."""
    f = d.frame(f"⓪ {title}: every Job at a glance")
    y = heading(d, title, "every Job at a glance: one row per Job; a Job with Runs opens as its own frame below")
    has = [j.name[:3] for j in jobs if any(t["runs"] for t in all_rows[j.name])]
    key = str((cfg.get("reading") or {}).get("overview") or "").strip() or (
        f"Results so far in {', '.join(has)}; no Run yet in "
        f"{', '.join(j.name[:3] for j in jobs if j.name[:3] not in has) or 'none'}." if has else
        f"No Run yet in any of these {len(jobs)} Jobs.")
    kh = tall("🎯 " + key, W - 140, 30) + 44
    d.key(40, y, W - 80, kh)
    para(d, 70, y + 22, "🎯 " + key, W - 140, 30)
    y, lw = y + kh + 30, 620
    for job in jobs:
        rows = all_rows[job.name]
        done = [r for t in rows for r in t["runs"] if r["mark"] == "✅" and r["values"]]
        reading = str((cfg.get("reading") or {}).get(job.name) or "").strip() or "❓ no reading yet"
        runs = [r for t in rows for r in t["runs"]]
        right = [reading] + ([" · ".join(done[0]["values"][:3])] if done else []) + \
            ([] if runs else ["⬜ no Run yet, so no frame below; Tasks: " +
                              ", ".join(f"{t['task'].name[:3]} {t['title']}" for t in rows)] +
             ["❓ " + re.sub(r"^j\d+[A-Za-z0-9_]*\s*:\s*", "", o) for o in opens_of(cfg, job) if re.match(r"^j\d+", o)])
        h = max(tall(f"{job.name[:3]} · {title_of(job)}", lw - 40, 28) + tall(tall_ := tally(rows), lw - 40, 22),
                sum(tall(s_, W - lw - 160, 22) + 6 for s_ in right)) + 36
        d.box(40, y, W - 80, h, INK, 1.5)
        yy = para(d, 60, y + 16, f"{job.name[:3]} · {title_of(job)}", lw - 40, 28)
        para(d, 60, yy + 4, tall_, lw - 40, 22)
        d.line([(40 + lw, y + 30), (40 + lw + 60, y + 30)], sw=2)
        yy = y + 16
        for s_ in right:
            yy = para(d, 40 + lw + 80, yy, s_, W - lw - 160, 22) + 6
        y += h + 16
    f["height"] = max(y + 30, 500)
    if f["height"] > 1600:
        canvas.reads_down(f)
    d.badge(f)
    return f


def draw(topic: Path) -> Path:
    """Redraw one results topic from its face and the Runs on disk; refresh the face's ledger and the preview."""
    topic = topic.resolve()
    block = topic.parents[1]
    face = topic / f"{topic.name}.md"
    cfg = results_yaml(face)
    names = [str(j) for j in (cfg.get("jobs") or [])] or list((cfg.get("reading") or {}).keys())
    jobs = [block / n for n in names if (block / n).is_dir()]
    if not jobs:
        raise SystemExit(f"{face}: its results: yaml names no Job of {block.name} (results.jobs)")
    all_rows = {j.name: job_rows(block, j, cfg) for j in jobs}
    d = Drawing()
    frames = []
    title = re.sub(r"^s\d+\s*·\s*", "", read(face).splitlines()[0]) if face.is_file() else topic.name
    if len(jobs) > 1:
        frames.append(overview_frame(d, title, jobs, all_rows, cfg))
    shown_jobs = [j for j in jobs if len(jobs) == 1 or any(t["runs"] for t in all_rows[j.name])]
    for i, job in enumerate(shown_jobs):
        frames.append(job_frame(d, CIRCLED[i] if i < len(CIRCLED) else f"({i + 1})", job, all_rows[job.name], cfg))
    ids = [f["id"] for f in frames]
    if len(jobs) == 1:
        d.acts([{"name": "Act 1 · what the Job has now", "frames": ids}])
    else:
        acts = [{"name": "Act 1 · the Jobs side by side", "frames": ids[:1]}]
        for k in range(1, len(ids), 3):
            row = ids[k:k + 3]
            first, last = shown_jobs[k - 1].name[:3], shown_jobs[k - 2 + len(row)].name[:3]
            acts.append({"name": f"Act {len(acts) + 1} · {first}" + (f" to {last}" if last != first else ""),
                         "frames": row, "arrow": "next Job"})
        d.acts(acts, between=[(ids[0], ids[1], "a Job with Runs, its own frame")] if len(ids) > 1 else [])
    out = topic / f"{topic.name}.excalidraw"
    d.write(out, f"haipipe-studio scripts/job_results.py {topic.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    text = read(face)
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        face.write_text(head + ledger(topic, jobs, all_rows) + rest.split(END, 1)[1], encoding="utf-8")
    return out


# ── making the topics ────────────────────────────────────────────────────────────────────────────────────────
def covered(block: Path) -> set[str]:
    """The Jobs a topic of this Block already draws: a results topic's `results: jobs`, or a whole-Job topic's
    `job: name` (excalidraw-job's job_drawing.py adopts a results topic into one)."""
    out = set()
    for face in (block / "studio").glob("s*/*.md"):
        cfg = results_yaml(face)
        out |= {str(j) for j in (cfg.get("jobs") or [])}
        m = re.search(r"```yaml\s*\n(job:.*?)```", read(face), re.S)
        if m and yaml:
            try:
                name = ((yaml.safe_load(m.group(1)) or {}).get("job") or {}).get("name")
            except Exception:
                name = None
            if name:
                out.add(str(name))
    return out


def used(block: Path) -> set[int]:
    return {int(m.group(1)) for p in (block / "studio").iterdir() if p.is_dir()
            for m in [re.match(r"^s(\d+)[-_]", p.name)] if m} if (block / "studio").is_dir() else set()


def make(block: Path, jobs: list[Path], slug: str, title: str, nn: int | None = None, dry: bool = False) -> Path:
    taken = used(block)
    nn = nn or next((n for n in range(BAND[0], BAND[1] + 1) if n not in taken), None)
    if nn is None or nn in taken:
        raise SystemExit(f"{block.name}: no free number in s{BAND[0]}-s{BAND[1]}; group the Jobs (--jobs) instead")
    topic = block / "studio" / f"s{nn:02d}-{slug}"
    if dry:
        print(f"would make {topic.relative_to(block)}  ← {', '.join(j.name for j in jobs)}")
        return topic
    topic.mkdir(parents=True)
    face = topic / f"{topic.name}.md"
    face.write_text(new_face(nn, slug, title, jobs, topic).replace(
        "results:\n", "results:\n  jobs: [" + ", ".join(j.name for j in jobs) + "]\n", 1), encoding="utf-8")
    builder = topic / f"build_s{nn:02d}_{slug.replace('-', '_')}.py"
    builder.write_text(builder_text(topic, nn, title, builder.name), encoding="utf-8")
    groups = block / "studio" / "_groups.txt"
    lines = read(groups).splitlines() if groups.is_file() else [
        "# Studio groups of this Block, in button order. The workbench writes this file when a group is",
        "# made, moved or deleted; a group's topics are the ones whose **Tags:** line names it."]
    if "Results" not in lines:
        groups.write_text("\n".join(lines + ["Results"]) + "\n", encoding="utf-8")
    return draw(topic)


def slug_of(job: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", job.name.lower()).strip("-")[:48].rstrip("-") + "-results"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("block", type=Path, nargs="?")
    ap.add_argument("--jobs", default="", help="one topic for these Jobs (comma separated)")
    ap.add_argument("--slug", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--nn", type=int)
    ap.add_argument("--draw", type=Path, metavar="TOPIC", help="redraw one results topic")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if a.draw:
        print(draw(a.draw))
        return 0
    if not a.block:
        ap.error("name a Block, or --draw <topic>")
    block = a.block.resolve()
    if a.jobs:
        jobs = [block / j.strip() for j in a.jobs.split(",") if j.strip()]
        missing = [j.name for j in jobs if not j.is_dir()]
        if missing:
            ap.error(f"no such Job in {block.name}: {', '.join(missing)}")
        print(make(block, jobs, a.slug or slug_of(jobs[0]), a.title or f"{title_of(jobs[0])} and more: results",
                   a.nn, a.dry_run))
        return 0
    todo = [j for j in kids(block, JOB) if j.name not in covered(block)]
    free = [n for n in range(BAND[0], BAND[1] + 1) if n not in used(block)]
    if len(todo) > len(free):
        ap.error(f"{block.name}: {len(todo)} Jobs, {len(free)} free numbers in s21-s29: group them with --jobs")
    for job, nn in zip(todo, free):
        print(make(block, [job], slug_of(job), f"{job.name[:3]} · {title_of(job)}: current results", nn, a.dry_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
