"""Reading feedback back: the plan's paragraphs, the Run inventory, and the notes saved against them."""
from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path
from src.outline_version import plan_dir, latest_outline
from src.run_folders import result_dir, result_roots
from src import run_names

KINDS = ("explore", "wording", "accept")
OPEN_STATUSES = {"", "ready", "running", "waiting-for-feedback", "open"}
# A Feedback item aimed at more paragraphs than this is Section-level history;
# it belongs to Run Space, not to one paragraph's note thread.
MAX_GROUP = 4
_ID_RE = re.compile(r"fb-[0-9a-f]{8,32}")
_PARAGRAPH_RE = re.compile(r"C\d+\.P\d+")
_BULLET_RE = re.compile(r"C\d+\.P\d+\.B\d+")


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%y%m%d %H%M UTC")


def _saved(path: Path) -> str:
    """A file's version is its name and saved time, never a content hash (JL 260928)."""
    return dt.datetime.fromtimestamp(path.stat().st_mtime).strftime("%y%m%d %H%M")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def plan_path(page: Path) -> Path | None:
    return latest_outline(plan_dir(page.parent), page.stem)


# ── the plan's paragraphs ──────────────────────────────────────────────────

def paragraphs(page: Path) -> dict[str, dict]:
    """Return `C<n>.P<m>` → {address, p, brief, bullets} from the current plan."""
    plan = plan_path(page)
    out: dict[str, dict] = {}
    if plan is None or not plan.is_file():
        return out
    cn = 0
    current = ""
    for line in _read(plan).splitlines():
        division = re.match(r"^## C(\d+)\b", line)
        if division:
            cn = int(division.group(1))
            current = ""
            continue
        if line.startswith("## "):
            # Any other `## ` heading ends the plan's divisions.
            if cn:
                break
            continue
        heading = re.match(r"^### C(\d+)\.P(\d+)\s*·\s*(.*)$", line)
        if heading:
            cn = int(heading.group(1))
            p = int(heading.group(2))
            brief = re.sub(r"\s*·\s*[Ss]\d+\s+to\s+[Ss]\d+\s*$", "", heading.group(3)).strip()
            current = "C%d.P%d" % (cn, p)
            out[current] = {"address": current, "p": p, "brief": brief, "bullets": []}
            continue
        bullet = re.match(r"^- (?:\[[ xX]\]\s*)?B(\d+)\s*·", line)
        if bullet and current:
            out[current]["bullets"].append("%s.B%s" % (current, bullet.group(1)))
    return out


# ── Run inventory · RP tickets paired with results/<run>/ ──────────────────

def _front(text: str) -> dict[str, str]:
    """Read `key: value` lines from a front matter block or a flat YAML file."""
    front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    body = front.group(1) if front else text
    fields = {}
    for match in re.finditer(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)[ \t]*$", body, re.M):
        fields.setdefault(match.group(1), match.group(2).strip().strip("\"'"))
    return fields


def _prange(fields: dict[str, str], every: set[int]) -> set[int]:
    text = fields.get("paragraphs", "")
    found: set[int] = set()
    for a, b in re.findall(r"P(\d+)(?:\s*[-–]\s*P(\d+))?", text):
        lo, hi = int(a), int(b or a)
        found.update(range(min(lo, hi), max(lo, hi) + 1))
    if found:
        return found
    target = fields.get("target", "")
    if re.search(r"whole\s+page", target, re.I) or re.search(r"whole\s+page", text, re.I):
        return set(every)
    ps = [int(x) for x in re.findall(r"\.P(\d+)", target)]
    if len(ps) >= 2:
        return set(range(min(ps), max(ps) + 1))
    if ps:
        return {ps[0]}
    return set()


_WRITING_KIND = {"paragraph": "para", "section": "sec", "structure": "struct"}


def _kind_of(stem: str) -> str:
    """The writing kind of a full Page Run name (`run-paragraph-…` → `para`), else ""."""
    return _WRITING_KIND.get(run_names.kind_of(stem) or "", "")


def run_rows(page: Path, every: set[int]) -> list[dict]:
    """Enumerate Page Writing Runs with status, version, and covered paragraphs."""
    runs_dir = page.parent / "runs"
    rows = []
    if not runs_dir.is_dir():
        return rows
    # A full name carries its day (`run-paragraph-0901-p02`); the order of the
    # names is the order the runs opened, so `nn` is that position.
    tickets = sorted(runs_dir.rglob("run-*.md"), key=lambda t: t.stem)
    for nn, ticket in enumerate(tickets, 1):
        stem = ticket.stem
        kind = _kind_of(stem)
        if not kind:
            continue
        if ticket.parent != runs_dir and ticket.parent.name != stem:
            continue                                   # a file inside a run's pass, not a ticket
        ticket_fields = _front(_read(ticket))
        own = result_dir(page.parent, stem)            # its latest pass, or results/<run>/ (older)
        runtime = own / "runtime.yaml"
        runtime_fields = _front(_read(runtime)) if runtime.is_file() else {}
        fields = dict(ticket_fields)
        fields.update({k: v for k, v in runtime_fields.items() if v})
        versions = sorted(own.glob("v[0-9][0-9][0-9].md")) if own.is_dir() else []
        version = runtime_fields.get("version") or (versions[-1].stem if versions else "")
        rows.append({
            "id": stem,
            "kind": kind,
            "nn": nn,
            "ticket": ticket,
            "results": own,
            "runtime": runtime,
            "status": (fields.get("status") or "").lower(),
            "version": version,
            "step": runtime_fields.get("step", ""),
            "covers": _prange(fields, every),
        })
    return rows


def _owning_run(rows: list[dict], p: int) -> tuple[dict | None, str]:
    def covers(row):
        return p in row["covers"]
    open_rows = [r for r in rows if r["status"] in OPEN_STATUSES]
    for kind in ("para", "struct", "sec"):
        candidates = [r for r in open_rows if r["kind"] == kind and covers(r)]
        if candidates:
            return max(candidates, key=lambda r: r["nn"]), "append"
    finished = [r for r in rows if r["kind"] == "para" and covers(r)]
    if finished:
        return max(finished, key=lambda r: r["nn"]), "reopen"
    return None, "allocate"


# ── reading the note thread back ───────────────────────────────────────────

def _section_body(text: str, heading: str) -> str:
    hit = re.search(
        rf"^###[ \t]+{re.escape(heading)}[ \t]*$\n(.*?)(?=^###[ \t]+|^##[ \t]+|\Z)",
        text, re.M | re.S)
    return hit.group(1) if hit else ""


def _target_paragraphs(target: str, every: dict[int, str]) -> list[int]:
    found: set[int] = set()
    addressed = [int(x) for x in re.findall(r"C\d+\.P(\d+)", target)]
    if re.search(r"C\d+\.P\d+(?:\.B\d+(?:\s*[-–]\s*B\d+)?)?\s*[-–]\s*C\d+\.P\d+", target) \
            and len(addressed) >= 2:
        found.update(range(min(addressed), max(addressed) + 1))
    else:
        found.update(addressed)
    for a, b in re.findall(r"(?<![.\w])P(\d{2,})(?:\s*[-–]\s*P(\d{2,}))?", target):
        lo, hi = int(a), int(b or a)
        found.update(range(min(lo, hi), max(lo, hi) + 1))
    return sorted(p for p in found if p in every)


def feedback_items(page: Path) -> dict[str, list[dict]]:
    """Return `C<n>.P<m>` → Feedback items from every Page writing Run's Version journal."""
    paras = paragraphs(page)
    every = {v["p"]: k for k, v in paras.items()}
    out: dict[str, list[dict]] = {k: [] for k in paras}
    roots = [r for r in result_roots(page.parent)       # results/run-*/ and every run's pass
             if (r.name if r.parent.name == "results" else r.parent.parent.name).startswith("run-")]
    if not roots:
        return out
    for vfile in [v for r in roots for v in sorted(r.glob("v[0-9][0-9][0-9].md"))]:
        text = _read(vfile)
        steps = list(re.finditer(r"^##[ \t]+Step[ \t]+(s\d{3})\b.*$", text, re.M))
        closure = re.search(r"^##[ \t]+Version closure[ \t]*$", text, re.M)
        for index, match in enumerate(steps):
            end = steps[index + 1].start() if index + 1 < len(steps) else (
                closure.start() if closure and closure.start() > match.end() else len(text))
            section = text[match.end():end]
            human = _section_body(section, "Human feedback")
            saved = _section_body(section, "Saved result")
            pending = bool(human.strip()) and not saved.strip()
            dispositions = dict(re.findall(r"^\|[ \t]*(F\d+)[ \t]*\|[ \t]*([^|]*?)[ \t]*\|", saved, re.M))
            source = re.search(r"^Source:[ \t]*(.*)$", human, re.M)
            for item in re.finditer(r"^####[ \t]+Feedback[ \t]+(F\d+)[ \t]*$\n(.*?)(?=^####[ \t]+|\Z)",
                                    human, re.M | re.S):
                label, body = item.group(1), item.group(2)
                fields = {k.strip(): v.strip() for k, v in
                          re.findall(r"^- ([A-Za-z][A-Za-z /]*?):[ \t]*(.*)$", body, re.M)}
                targets = _target_paragraphs(fields.get("Target", ""), every)
                if not targets or len(targets) > MAX_GROUP:
                    continue
                by = fields.get("By", "")
                origin = source.group(1).strip() if source else ""
                date = re.search(r"\d{6} \d{4} UTC", by or origin)
                # A composer note is signed `By: <name> · <date>`; a historical
                # chat Step carries only its Source line, so it reads as `chat`.
                author = re.split(r"\s*·\s*", by)[0].strip() if by else "chat"
                record = {
                    "run": vfile.parent.name, "version": vfile.stem, "step": match.group(1),
                    "label": label, "id": fields.get("Id", ""),
                    "kind": (fields.get("Kind") or "feedback").lower(),
                    "author": author, "date": date.group(0) if date else "",
                    "target": fields.get("Target", ""),
                    "comment": fields.get("Human comment", "").strip("`"),
                    "group": targets,
                    "pending": pending,
                    "disposition": "pending" if pending else (dispositions.get(label) or "recorded"),
                }
                for p in targets:
                    out[every[p]].append(record)
    return out
