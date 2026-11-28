"""Reading a folder's work records: faces, Run cards and receipts, cached by file date, and their states and roles."""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import re

import yaml
from live import frame

VIEWS = ("Goal", "Plan", "Execution", "Results")
MODES = ("Audience Report", "Work Details")
PURPOSES = {
    "asset-contract": "Define output fields and usage rules",
    "asset-build": "Build a reference table from raw inputs",
    "asset-freeze": "Save service answers for a specific version for later reuse",
    "asset-validate": "Check output tables against field and data rules",
    "asset-parity": "Check whether frozen answers match the corresponding service answers",
    "asset-compare": "Compare outputs from two versions",
    "asset-release": "Pin the exact version of each table in the release",
    "asset-gallery": "Check outputs for different input types across the full workflow",
    "unit-test": "Check shared code behavior and compatibility",
    "eval-ab": "Compare results with and without a specific change",
    "external-corpus": "Check method performance on external data",
}
e = frame.esc


_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)          # libyaml when present: about ten times faster
_READ = {}
_TTL = {}


def read_yaml(path):
    """A YAML or JSON file as a dict, parsed once until the file changes (JL 261021: "每一次 change 的时候，它都会花很长时间")."""
    try:
        if not path:
            return {}
        st = path.stat()
        if st.st_size > 2_000_000:
            return {}
        key = (str(path), st.st_mtime_ns, st.st_size)
        if key not in _READ:
            text = path.read_text(encoding="utf-8")
            try:
                value = json.loads(text) if path.suffix == ".json" else yaml.load(text, Loader=_LOADER)
            except yaml.YAMLError:
                value = top_level(text)
            _READ[key] = value if isinstance(value, dict) else {}
        return _READ[key]
    except (OSError, ValueError, yaml.YAMLError):
        return {}


def top_level(text):
    """A receipt YAML cannot parse still has its top-level `key: value` lines: an older receipt wrote an unquoted
    headline with a colon in it (`headline: B1 food: FAIL, ...`), and dropping the whole file read a complete Run as
    "Not recorded" (b51 j01 t12-t15, 261021)."""
    out = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*?)[ \t]*$", line)
        if m and m.group(2) and m.group(2) not in ("|", ">", "|-", ">-"):
            out.setdefault(m.group(1), None if m.group(2) == "null" else m.group(2).strip("\"'"))
    return out


def kept(key, make, seconds=8.0):
    """A value kept for a few seconds, so one page and its own 20-second refresh never rebuild it twice."""
    now = time.monotonic()
    hit = _TTL.get(key)
    if hit and now - hit[0] < seconds:
        return hit[1]
    value = make()
    _TTL[key] = (now, value)
    return value


def receipt_of(path):
    """A Run's receipt with its times under one name: a Databricks ticket's receipt says `started` and `ended`, read
    here as `started_at` and `finished_at`."""
    rec = read_yaml(path)
    alias = {k: rec[v] for k, v in (("started_at", "started"), ("finished_at", "ended")) if not rec.get(k) and rec.get(v)}
    return dict(rec, **alias) if alias else rec


def summary_line(summary):
    """A receipt's `summary:` said as one line, number first (28 tables · 1,562,150,228 rows total), when the receipt
    writes no headline of its own."""
    if not isinstance(summary, dict):
        return ""
    out = []
    for k, v in summary.items():
        words = str(k).replace("_", " ")
        if isinstance(v, bool) or v in (None, "", [], {}):
            continue
        if isinstance(v, (int, float)):
            out.append(f"{v:,} {words}")
        elif isinstance(v, str) and len(v) <= 40:
            out.append(f"{words} {v}")
        elif isinstance(v, list) and all(isinstance(x, (str, int, float)) for x in v):
            out.append(f"{words}: {', '.join(map(str, v[:3]))}" + (" …" if len(v) > 3 else ""))
    return " · ".join(out[:6])[:240]


def said_of(receipt, result):
    """A Run's key result from its own numbers when it writes no headline: its receipt's `summary:` or `counts:`, the
    tables its `outputs:` lists (patient_universe: 466,745 rows · 7 columns), else its result/metrics.json."""
    for key in ("summary", "counts"):
        line = summary_line(receipt.get(key))
        if line:
            return line
    outs = [o for o in receipt.get("outputs") or [] if isinstance(o, dict)] if isinstance(receipt.get("outputs"), list) else []
    if outs:
        return " · ".join(f"{o.get('table') or o.get('name') or 'output'}: "
                          + summary_line({k: o[k] for k in ("rows", "columns") if k in o}) for o in outs[:3])[:240]
    return summary_line(read_yaml(result / "metrics.json")) if result else ""


def text_of(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace") if path else ""
    except OSError:
        return ""


def section(text, name):
    match = re.search(rf"(?ims)^##\s+{re.escape(name)}\s*\n(.*?)(?=^##\s|\Z)", text)
    return match.group(1).strip() if match else ""


def face_fields(folder):
    md = frame.face(folder)
    if not md:
        return {}
    return dict(frame.fields(md, keys=(
        "goal", "spine", "develops", "close", "input", "output", "state",
        "goal-status", "goal-scope", "workbench-layout", "emoji")))


def enabled(folder, root):
    block = frame.chain(folder, root).get("Block")
    return bool(block and face_fields(block).get("workbench-layout") == "workflow")


def goal(folder):
    fields = {k: v for k, v in face_fields(folder).items()          # a new face's `goal: open` is a placeholder, not
              if str(v).strip().lower() not in ("open", "<open>", "none", "-")}   # a goal (212 work Jobs, 261021)
    opening = section(text_of(frame.face(folder)), "Opening")
    return (fields.get("goal") or fields.get("spine") or fields.get("develops")
            or frame._first_sentence(opening, 300) or "Goal not yet specified")


def task_folders(level, folder):
    if level == "Task":
        return [folder]
    kids = frame.children(folder, level)
    return [t for j in kids for t in frame.children(j, "Job")] if level == "Block" else kids


def first_line(path):
    """A Run's own one-line result, `result/headline.txt` (frame.py's Run reader reads the same file)."""
    text = text_of(path) if path and path.is_file() else ""
    return text.strip().splitlines()[0][:240] if text.strip() else ""


_RECORDS = {}


def records(task):
    """A Task's Run records, rebuilt only when one of its Run cards or receipts changed (reading them is most of a
    page's time; a file's date is cheap to check)."""
    stamp = []
    runs = task / "runs"
    for run in sorted(runs.iterdir()) if runs.is_dir() else []:
        for f in (run / "run.yaml", run / "result/runtime.yaml", run / "result/headline.txt"):
            try:
                stamp.append((run.name, f.name, f.stat().st_mtime_ns))
            except OSError:
                pass
    face = frame.face(task)
    key = (tuple(stamp), face.stat().st_mtime_ns if face else 0)
    hit = _RECORDS.get(str(task))
    if not hit or hit[0] != key:
        hit = _RECORDS[str(task)] = (key, _records(task))
    return hit[1]


def _records(task):
    """Join cards to the shared native reader, including redirected Result stores."""
    from live.runs import local_runs
    md = frame.face(task)
    native = local_runs(md) if md else []
    by_name = {r["ticket"].stem: r for r in native if r.get("ticket")}
    result, seen = [], set()
    for row in frame.runs_of(task):
        if row["kind"] != "hard" or row["run"] in seen:
            continue
        seen.add(row["run"])
        path = row["path"]
        card = read_yaml(path / "run.yaml") if path.is_dir() else {}
        if card.get("kind") == "soft":
            continue
        source = by_name.get(row["run"], {})
        receipt_path = source.get("runtime") or (path / "result/runtime.yaml" if path.is_dir() else None)
        receipt = receipt_of(receipt_path)
        types = card.get("type") or receipt.get("operation") or source.get("operation") or []
        types = types if isinstance(types, list) else [types]
        purpose = (card.get("goal") or card.get("aim") or source.get("goal")   # hai-draw job writes a Run's purpose as aim
                   or next((PURPOSES[t] for t in types if t in PURPOSES), ""))
        result.append(dict(row, task=task, card=card, receipt=receipt, receipt_path=receipt_path,
                           source=source, types=types, purpose=purpose,
                           status=str(receipt.get("status") or card.get("status") or "Not recorded"),
                           target=receipt.get("target") or card.get("target") or source.get("target") or "",
                           headline=receipt.get("headline") or source.get("outcome") or first_line(path / "result/headline.txt")
                           or said_of(receipt, Path(receipt_path).parent if receipt_path else None)))
    return result


def snapshot(level, folder):
    return {task: records(task) for task in task_folders(level, folder)}


def show(value):
    if value is None or value == "" or value == [] or value == {}:
        return "Not recorded"
    if isinstance(value, (dict, list)):
        return yaml.safe_dump(value, allow_unicode=True, sort_keys=False).strip()
    return str(value)


def moment(value):
    try:
        return value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def elapsed(receipt):
    start, end = moment(receipt.get("started_at")), moment(receipt.get("finished_at"))
    live = bool(start and not end and str(receipt.get("status")).lower() == "running")
    if live and start.tzinfo:
        end = datetime.now(timezone.utc)
    if not start or not end:
        return "Not recorded"
    try:
        seconds = int((end - start).total_seconds())
    except TypeError:
        return "Not recorded"
    if seconds < 0:
        return "Conflicting timestamps"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return ("Elapsed " if live else "") + (f"{h} h " if h else "") + (f"{m} min " if m else "") + f"{s} s"


def location(receipt):
    execution = receipt.get("execution") or {}
    execution = execution if isinstance(execution, dict) else {}
    return next((receipt[k] for k in ("host", "hostname", "machine", "platform") if receipt.get(k)),
                execution.get("host") or execution.get("platform") or "Not recorded")


def plan_data(folder):
    plan = read_yaml(folder / "workflow/plan.yaml")
    specs = plan.get("run_specs") or []
    return plan, [s for s in specs if isinstance(s, dict)] if isinstance(specs, list) else []


def clock(value):
    """A receipt's time to the minute, as a reader says it (2026-10-21 01:43)."""
    return str(value)[:16].replace("T", " ") if value else "Not recorded"


ROLES = (("trial", "🧪 trial", "a small try before the full Run"),
         ("make", "🔨 make", "makes the Task's output"),
         ("fix", "🔁 retry or fix", "asks again what a Run missed, or repairs it"),
         ("check", "🔎 check", "audits or compares an output"),
         ("describe", "📋 describe", "says what an output holds"),
         ("figures", "📊 figures", "draws results as charts"),
         ("evidence", "🧾 evidence", "one value or display for a page"),
         ("publish", "📤 publish", "releases or delivers an output"))
ROLE_ORDER = {k: i for i, (k, _, _) in enumerate(ROLES)}


def role_of(row):
    """The one job a Run does in its Task (JL 261020: "各司其职"): its card's `role:`, else what its run_type says."""
    card_ = row.get("card") or {}
    role = str(card_.get("role") or {"main": "make", "figures": "figures", "delivery": "publish"}.get(str(card_.get("run_type")), ""))
    return role if role in ROLE_ORDER else "other"


STATE = (("running", "🏃 running", ("running", "started", "in_progress")),
         ("finished", "✅ finished", ("complete", "completed", "done", "ok", "passed")),
         ("partial", "🔶 partial", ("partial",)),      # some rows stored, the rest not (b02's binder writes it)
         ("failed", "❌ failed", ("failed", "error", "crashed")),
         ("blocked", "⛔ blocked", ("blocked",)),
         ("waiting", "◌ waiting", ("proposed", "ready", "queued", "planned")))


def state_of(row):
    """A Run's recorded status, in one of five words (or no record): what its receipt or card says, never guessed."""
    s = str(row.get("status") or "").strip().lower()
    return next((k for k, _, words in STATE if s in words), "no record")


def last_finish(rows):
    done = [(str(r["receipt"].get("finished_at") or ""), r["run"]) for r in rows if r["receipt"].get("finished_at")]
    return max(done) if done else ("", "")
