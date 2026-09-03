"""Typed Evidence Items · read, derive, count.

The authored ledger is ``outline/<stem>-evidence-items.md``. SHAPE specifies
each ``E<NN>-<TYPE>-<slug>``; SURVEY plans zero-to-many Supporting Runs,
zero-to-many exact PageX source bindings, and exactly one local Page Evidence
Item Run; LAND validates and freezes those inputs before binding the local
Result. This module is the single parser used by the generated evidence view
and phase strip, so the UI cannot invent a second status contract.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

LADDER = (
    "specified", "planned", "ready", "folded", "accepted", "stale",
    "deferred", "dropped", "blocked",
)
EMOJI = {
    "specified": "📝", "planned": "🔗", "ready": "🟢", "folded": "📌",
    "accepted": "✅", "stale": "⚠️", "deferred": "⏸", "dropped": "✖",
    "blocked": "⛔",
}
ACTIONS = (
    "reuse", "rerun", "registered", "new-run", "new-task", "new-job", "new-block",
)
ACTION_LABELS = {
    "reuse": "reuse",
    "rerun": "rerun",
    "registered": "registered",
    "new-run": "newrun",
    "new-task": "newtask",
    "new-job": "newjob",
    "new-block": "newblock",
}
OUTCOMES = ACTIONS  # compatibility import for callers; actions replaced outcomes
CYCLES = ("SHAPE", "SURVEY", "LAND", "EMBED", "WRITE")
ITEM_TYPES = ("VALUE", "CITE", "DISPLAY")
TYPE_KIND = {"VALUE": "value", "CITE": "cite", "DISPLAY": "display"}
MARKS = {"🧮": "value", "📚": "cite", "🖼": "display"}  # display-only compatibility

_ITEM_ID = r"E\d+-(?:VALUE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*"
_REC_RE = re.compile(
    rf"^###\s+({_ITEM_ID})\s*·\s*(C\d+\.P\d+\.B\d+)\s*·\s*(.*)$"
)
_LABEL_RE = re.compile(r"^-\s+\*\*([^*]+?)\*\*\s*[:：]\s*(.*)$")
_WALL_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]{0,11}$")
_EVIDENCE_RE = re.compile(rf"^\s*Evidence:\s*({_ITEM_ID})\s*·\s*(.+)$")
_GLOBAL_RUN_RE = re.compile(r"^b(\d+)\.?j(\d+)\.?t(\d+)\.?r(\d+)$")
_TASK_RE = re.compile(r"^b\d+\.?j\d+\.?t\d+(?:\.?r\d+)?$")
_PARENT_TASK_RE = re.compile(r"^b(\d+)\.?j(\d+)\.?t(\d+)$")
_JOB_RE = re.compile(r"^b\d+(?:\.?j\d+(?:\.?t\d+(?:\.?r\d+)?)?)?$")
_BLOCK_RE = re.compile(r"^b\d+(?:\.?j\d+(?:\.?t\d+(?:\.?r\d+)?)?)?$")


def compact_global_run(value: str) -> str:
    """Return the canonical compact global Run id, or ``\"\"`` when invalid."""
    match = _GLOBAL_RUN_RE.fullmatch((value or "").strip())
    if not match:
        return ""
    return "b%sj%st%sr%s" % match.groups()


def readable_global_run(value: str) -> str:
    """Return a human-readable dotted global Run id, or ``\"\"`` when invalid."""
    match = _GLOBAL_RUN_RE.fullmatch((value or "").strip())
    if not match:
        return ""
    return "b%s.j%s.t%s.r%s" % match.groups()


def readable_task(value: str) -> str:
    """Return a human-readable dotted B/J/T parent address, or ``\"\"``."""
    match = _PARENT_TASK_RE.fullmatch((value or "").strip())
    if not match:
        return ""
    return "b%s.j%s.t%s" % match.groups()


def readable_paper_route(value: str) -> str:
    """Return a Paper-Board-local relative address for a global route.

    One Paper Board is the local block. Its UI therefore shows the route below
    that block (``jNN.tNN[.rNN]``), while the authored ledger retains the full
    ``bNN...`` address for cross-folder lookup and migration safety.
    """
    full = _GLOBAL_RUN_RE.fullmatch((value or "").strip())
    if full:
        _block, job, task, run = full.groups()
        return "j%s.t%s.r%s" % (job, task, run)
    parent = _PARENT_TASK_RE.fullmatch((value or "").strip())
    if parent:
        _block, job, task = parent.groups()
        return "j%s.t%s" % (job, task)
    return ""


def action_label(action: str) -> str:
    """Return the compact reader-facing token for one authored action."""
    return ACTION_LABELS.get((action or "").lower(), "")


def planned_route_anchor(address: str, action: str, *, page_id: str = "",
                         item_id: str = "", layer: str = "") -> str:
    """Return one stable Run-Index fragment for an unallocated ``new-*`` route.

    A new Run has a parent address but no ``rNN``; a legacy local new Task may
    not even have a parent yet.  Both still need a durable, clickable plan
    card.  The action keeps otherwise identical parent addresses distinct.
    """
    action_part = re.sub(r"[^a-z0-9]+", "-", (action or "").lower()).strip("-")
    address_part = re.sub(r"[^a-z0-9]+", "", (address or "").lower())
    if address_part:
        return "plan-%s-%s" % (action_part or "route", address_part)
    fallback = "-".join(
        re.sub(r"[^a-z0-9]+", "-", part.lower()).strip("-")
        for part in (page_id, item_id, layer)
        if part
    )
    return "plan-%s-%s" % (action_part or "route", fallback or "unallocated")


RUN_STATUS_LABEL = {
    "planned": "Ready",
    "running": "Running",
    "complete": "Done",
    "failed": "Failed",
    "blocked": "Held",
    "superseded": "Historical",
    "rerun": "Rerun",
    "ticket": "Run only",
}


def _current_result_status(runtime: Path | None, *, result_files: set[str]) -> tuple[str, str]:
    """Classify one current Task receipt without treating it as evidence.

    A Ticket with no receipt is a real planned computation but has no Result:
    it is ``ticket`` (rendered ``Run only``).  A receipt from an attempted,
    incomplete, smoke, or fake-Stata execution is ``rerun``.  Only a completed
    receipt with a real aggregate artifact is ``complete``.
    """
    if runtime is None:
        return "ticket", ""
    text = runtime.read_text(encoding="utf-8", errors="replace")
    artifacts = {
        child.name for child in runtime.parent.iterdir()
        if child.is_file() and child.name not in result_files
    }
    complete = bool(re.search(r"^status:\s*complete\s*$", text, re.M))
    fake_worker = "fakestata" in text.lower()
    if complete and artifacts and not fake_worker:
        return "complete", str(runtime.parent)
    return "rerun", ""


def _add_current_task_tickets(root: Path, records: dict[str, dict[str, str]]):
    """Register active ``task/`` Tickets and audit their Result projection.

    ``task/`` is the current Project-Personality-OpioidRx tree.  Its run
    Tickets pre-date the generic receipt schema, so their b/j/t/r identity is
    derived from the path.  The audit distinguishes a Ticket without any
    receipt (``Run only``) from a smoke/incomplete attempt (``Rerun``); neither
    is presented as a usable Result.
    """
    for ticket in root.glob("examples/**/task/b*/j*/t*/runs/**/*.ps1"):
        try:
            rel = ticket.relative_to(root)
            at = rel.parts.index("task")
            block, job, task, runs = rel.parts[at + 1:at + 5]
        except (ValueError, IndexError):
            continue
        if runs != "runs":
            continue
        block_match = re.fullmatch(r"b(\d+)_.*", block)
        job_match = re.fullmatch(r"j(\d+)_.*", job)
        task_match = re.fullmatch(r"t(\d+)_.*", task)
        run_match = re.fullmatch(r"r(\d+)_.*", ticket.stem)
        if not all((block_match, job_match, task_match, run_match)):
            continue
        compact = "b%sj%st%sr%s" % (
            block_match.group(1), job_match.group(1),
            task_match.group(1), run_match.group(1),
        )
        job_root = root.joinpath(*rel.parts[:at + 3])
        result_root = job_root / "results" / task
        runtimes = sorted(result_root.glob("*/runtime.yaml")) if result_root.is_dir() else []
        matching_runtime = next(
            (runtime for runtime in runtimes
             if ticket.stem in runtime.read_text(encoding="utf-8", errors="replace")),
            None,
        )
        status, result_path = _current_result_status(
            matching_runtime,
            result_files={"runtime.yaml", "config_snapshot.do"},
        )
        result = (str(Path(result_path).relative_to(root)) if result_path else "")
        records[compact] = {
            "status": status,
            "label": RUN_STATUS_LABEL[status],
            "task_root": str(root.joinpath(*rel.parts[:at + 4]).relative_to(root)),
            "ticket": str(ticket.relative_to(root)),
            "runtime": (str(matching_runtime.relative_to(root))
                        if matching_runtime else ""),
            "result": result,
            "family": "Execution",
            "target": ticket.stem,
        }


def _add_discovery_tickets(root: Path, records: dict[str, dict[str, str]]):
    """Register actual Discovery Paper/Source Tickets with their Result gate.

    Legacy task-level ``sources.md``/``landscape.md`` files are deliberately
    not Results.  A Discovery Result is usable only when its same-stem Ticket,
    complete runtime, Result Card, Bib, and ``facts.md`` all exist.
    """
    for ticket in root.glob("examples/**/discoveries/b*/j*/t*/runs/*"):
        if not ticket.is_file() or ticket.suffix != ".sh":
            continue
        try:
            rel = ticket.relative_to(root)
            at = rel.parts.index("discoveries")
            block, job, task, runs = rel.parts[at + 1:at + 5]
        except (ValueError, IndexError):
            continue
        if runs != "runs":
            continue
        block_match = re.fullmatch(r"b(\d+)_.*", block)
        job_match = re.fullmatch(r"j(\d+)_.*", job)
        task_match = re.fullmatch(r"t(\d+)_.*", task)
        run_match = re.fullmatch(r"r(\d+)_.*", ticket.stem)
        if not all((block_match, job_match, task_match, run_match)):
            continue
        compact = "b%sj%st%sr%s" % (
            block_match.group(1), job_match.group(1),
            task_match.group(1), run_match.group(1),
        )
        task_root = root.joinpath(*rel.parts[:at + 4])
        result_dir = task_root / "results" / ticket.stem
        runtime = result_dir / "runtime.yaml"
        status, result = "ticket", ""
        if runtime.is_file():
            text = runtime.read_text(encoding="utf-8", errors="replace")
            complete = bool(re.search(r"^status:\s*complete\s*$", text, re.M))
            required = {
                result_dir / f"{ticket.stem}.md",
                result_dir / f"{ticket.stem}.bib",
                result_dir / "facts.md",
            }
            executable = bool(ticket.stat().st_mode & 0o111)
            if complete and executable and all(path.is_file() for path in required):
                status = "complete"
                result = str(result_dir.relative_to(root))
            elif re.search(r"^status:\s*(?:planned|running)\s*$", text, re.M):
                status = "ticket"
            else:
                status = "rerun"
        records[compact] = {
            "status": status,
            "label": RUN_STATUS_LABEL[status],
            "task_root": str(task_root.relative_to(root)),
            "ticket": str(ticket.relative_to(root)),
            "runtime": (str(runtime.relative_to(root)) if runtime.is_file() else ""),
            "result": result,
            "family": "Discovery",
            "target": ticket.stem,
        }


@lru_cache(maxsize=8)
def run_registry(root_text: str) -> dict[str, dict[str, str]]:
    """Read registered receipts plus the active Task and Discovery Tickets.

    This is a SURVEY inventory, not an evidence promotion.  A current Ticket
    with no Result receipt is ``Run only``; a smoke/incomplete attempt is
    ``Rerun``; only a usable completed Result is ``Done``.
    """
    root = Path(root_text)
    records: dict[str, dict[str, str]] = {}
    pattern = "examples/**/tasks/b*/j*/results/t*/r*/runtime.yaml"
    for runtime in root.glob(pattern):
        text = runtime.read_text(encoding="utf-8", errors="replace")

        def field(name: str) -> str:
            match = re.search(rf"^{re.escape(name)}:\s*(.+?)\s*$", text, re.M)
            return match.group(1).strip().strip('"') if match else ""

        compact = compact_global_run(field("global_id"))
        if not compact:
            continue
        ticket = field("ticket")
        ticket_path = root / ticket if ticket else None
        if not ticket_path or not ticket_path.is_file():
            continue
        status = field("status").lower()
        records[compact] = {
            "status": status,
            "label": RUN_STATUS_LABEL.get(status, "Unregistered"),
            "ticket": ticket,
            "runtime": str(runtime.relative_to(root)),
            "result": field("result"),
            "family": field("family"),
            "target": field("target"),
        }
    _add_current_task_tickets(root, records)
    _add_discovery_tickets(root, records)
    return records


def wall_label(item_id: str, item_type: str, name: str, label: str = "") -> str:
    """Return a bounded visual identity; authored ids remain unchanged.

    New and updated records author an explicit ``Label`` of at most twelve
    ASCII alphanumeric characters.  The derived fallback keeps legacy ledgers
    readable without allowing their full names to widen the Outline grid.
    """
    number = re.match(r"^E0*(\d+)", item_id)
    short_number = "E%s" % (number.group(1) if number else item_id)
    short_type = {"VALUE": "V", "CITE": "C", "DISPLAY": "D"}.get(
        item_type, item_type[:1]
    )
    authored = (label or "").strip()
    if _WALL_NAME_RE.fullmatch(authored):
        compact_name = authored
    else:
        words = re.findall(r"[A-Za-z0-9]+", name)
        derived = "".join(
            word if word.isupper() else word[:1].upper() + word[1:]
            for word in words
        ) or "Item"
        compact_name = derived[:12]
    return "%s%s.%s" % (short_number, short_type, compact_name)


def repo_root(start: Path) -> Path:
    """Return the first checkout ancestor holding pyproject.toml and code/."""
    for p in [start] + list(start.parents):
        if (p / "pyproject.toml").is_file() and (p / "code").is_dir():
            return p
    return start


def items_path(page_md: Path) -> Path:
    return page_md.parent / "outline" / f"{page_md.stem}-evidence-items.md"


def _parse_local(value: str) -> tuple[str, str, str]:
    """Return action, address, Result path from a Local Run field."""
    left, _, result = value.partition("→")
    if left.strip().lower() == "— design page evidence task":
        # Legacy paper wording for a local Page-Evidence task that has not
        # yet been allocated.  Preserve the authored text but expose the
        # current controlled action to renderers and the Plan Index.
        return "new-task", "", result.strip()
    parts = [p.strip() for p in left.split("·")]
    if len(parts) < 4 or [p.lower() for p in parts[:2]] != ["page", "evidence item"]:
        return "", "", result.strip()
    action = parts[2].lower() if parts[2].lower() in ACTIONS else ""
    return action, parts[3], result.strip()


def _valid_action_address(action: str, address: str) -> bool:
    if action in ("reuse", "rerun", "registered"):
        return bool(compact_global_run(address))
    if action == "new-run":
        return bool(_PARENT_TASK_RE.fullmatch(address))
    if action == "new-task":
        return bool(_JOB_RE.fullmatch(address))
    if action == "new-job":
        return bool(_BLOCK_RE.fullmatch(address))
    if action == "new-block":
        return bool(address)
    return False


def _valid_supporting(value: str) -> tuple[bool, int]:
    if value == "[]":
        return True, 0
    entries = [entry.strip() for entry in value.split(";") if entry.strip()]
    if not entries:
        return False, 0
    for entry in entries:
        parts = [part.strip() for part in entry.split("·")]
        if len(parts) < 3 or parts[0] not in ("Execution", "Discovery"):
            return False, len(entries)
        action = parts[1].lower()
        if not _valid_action_address(action, parts[2]):
            return False, len(entries)
    return True, len(entries)


def _registered_supports(value: str, registry: dict[str, dict[str, str]]) -> bool:
    """True only when every declared support has a registered Run receipt."""
    if value == "[]":
        return True
    entries = [entry.strip() for entry in value.split(";") if entry.strip()]
    for entry in entries:
        parts = [part.strip() for part in entry.split("·")]
        if len(parts) < 3 or parts[1].lower() not in ("reuse", "rerun", "registered"):
            return False
        if compact_global_run(parts[2]) not in registry:
            return False
    return bool(entries)


def _valid_pagex(value: str) -> tuple[bool, int]:
    """Validate exact cross-Folder source bindings; PageX is never a Run."""
    if value == "[]":
        return True, 0
    entries = [entry.strip() for entry in value.split(";") if entry.strip()]
    if not entries:
        return False, 0
    for entry in entries:
        path_text, separator, authority = entry.partition("·")
        path_text, authority = path_text.strip(), authority.strip()
        path = Path(path_text)
        if (
            not separator or not path_text or path_text.endswith("/")
            or path.is_absolute() or ".." in path.parts
            or not authority.lower().startswith("authority ")
            or not authority[len("authority "):].strip()
        ):
            return False, len(entries)
    return True, len(entries)


def read_items(page_md: Path) -> dict:
    """Return ``{item_id: row}`` from the authored Evidence Item table."""
    f = items_path(page_md)
    if not f.is_file():
        return {}
    labels = (
        "target", "label", "need", "expected", "acceptance", "supporting runs",
        "pagex bindings", "local input", "local run", "decide",
    )
    rows, cur = {}, None
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _REC_RE.match(line)
        if m:
            item_id, target, name = m.groups()
            cur = {k: "" for k in labels}
            cur.update({
                "item": item_id,
                "type": item_id.split("-", 2)[1],
                "target": target,
                "name": name.strip(),
            })
            rows[item_id] = cur
            continue
        if cur is None:
            continue
        m = _LABEL_RE.match(line)
        if m:
            key = m.group(1).strip().lower()
            if key in labels:
                cur[key] = m.group(2).strip()
    registry = run_registry(str(repo_root(page_md.parent)))
    for row in rows.values():
        row["supporting_runs"] = row.pop("supporting runs")
        row["pagex_bindings"] = row.pop("pagex bindings")
        row["local_input"] = row.pop("local input")
        row["local_run"] = row.pop("local run")
        action, address, result = _parse_local(row["local_run"])
        row.update({"action": action, "address": address, "result": result})
        supports_valid, support_count = _valid_supporting(row["supporting_runs"])
        row.update({"support_count": support_count, "supports_valid": supports_valid})
        pagex_valid, pagex_count = _valid_pagex(row["pagex_bindings"])
        row.update({"pagex_count": pagex_count, "pagex_valid": pagex_valid})
        d = row["decide"].lower()
        row["decision"] = (
            "make" if "☑" in d and "make" in d else
            "defer" if "☑" in d and "defer" in d else
            "drop" if "☑" in d and "drop" in d else ""
        )
        row["specified"] = all(
            row.get(k) for k in ("target", "need", "expected", "acceptance")
        )
        local_registered = (
            action in ("reuse", "rerun", "registered")
            and compact_global_run(address) in registry
        )
        row["runs_registered"] = _registered_supports(
            row["supporting_runs"], registry
        ) and local_registered
        row["planned"] = (
            supports_valid and pagex_valid and bool(row["local_input"])
            and (pagex_count == 0 or "pagex" in row["local_input"].lower())
            and _valid_action_address(action, address) and row["runs_registered"]
        )
    return rows


def resolve(path_str: str, root: Path, page_dir: Path):
    """Return the Result path a local binding points at, or None."""
    if not path_str:
        return None
    p = Path(path_str)
    candidates = [p] if p.is_absolute() else [root / p, page_dir / p, Path.cwd() / p]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def bullets(plan_text: str):
    """Yield one tuple per typed Evidence Item in the plan.

    Tuple: ``(item_id, target, bullet_head, item_type, expected, acceptance,
    folded)``. Several Evidence Items may share one bullet. ``folded`` is
    item-specific: its id must appear on an Answered or Drawn line.
    """
    lines = plan_text.splitlines()
    c = p = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^## C(\d+)\b", line)
        if m:
            c, p = int(m.group(1)), 0
            i += 1
            continue
        m = re.match(r"^### C(\d+)\.P(\d+)\b", line)
        if m:
            c, p = int(m.group(1)), int(m.group(2))
            i += 1
            continue
        if re.match(r"^## Aims\b", line):
            break
        m = re.match(r"^- (?:\[[ xX]\] )?[BS](\d+)\s*·\s*(.*)$", line)
        if not m:
            i += 1
            continue
        b, head = int(m.group(1)), m.group(2).strip()
        target = f"C{c}.P{p}.B{b}"
        body, j = [], i + 1
        while j < len(lines) and lines[j].startswith("  ") and not lines[j].lstrip().startswith("- "):
            body.append(lines[j].strip())
            j += 1
        i = j
        for n, body_line in enumerate(body):
            em = _EVIDENCE_RE.match(body_line)
            if not em:
                continue
            item_id, expected = em.groups()
            acceptance = ""
            if n + 1 < len(body) and body[n + 1].startswith("Accept:"):
                acceptance = body[n + 1].partition(":")[2].strip()
            folded = any(
                x.startswith(("Answered:", "Drawn:")) and item_id in x for x in body
            )
            yield (
                item_id, target, head, item_id.split("-", 2)[1],
                expected.strip(), acceptance, folded,
            )


def item_status(row, folded: bool, page_accepted: bool, plan_mtime: float,
                root: Path, page_dir: Path) -> str:
    """Derive one compact state from the authored row and local Result."""
    if row is None or not row.get("specified"):
        return "specified"
    if row["decision"] == "defer":
        return "deferred"
    if row["decision"] == "drop":
        return "dropped"
    result = resolve(row["result"], root, page_dir)
    if result and folded:
        if page_accepted:
            return "accepted"
        if result.stat().st_mtime > plan_mtime + 60:
            return "stale"
        return "folded"
    if result:
        return "ready"
    if row.get("planned") and row["decision"] == "make":
        return "planned"
    return "specified"


def cycle_now(approved: bool, rows: dict, statuses, n_items: int) -> str:
    """Derive the current Page cycle from the plan, table, and local Results."""
    if n_items == 0:
        return "WRITE" if approved else "SHAPE"
    if len(rows) < n_items or any(s == "specified" for s in statuses):
        return "SURVEY" if approved else "SHAPE"
    if any(r["decision"] == "" for r in rows.values()):
        return "SURVEY"
    if any(s in ("planned", "blocked") for s in statuses):
        return "LAND"
    if any(s in ("ready", "stale") for s in statuses):
        return "EMBED"
    return "WRITE" if approved else "SHAPE"


def summarize(page_md: Path, plan: Path, lane=None) -> dict:
    """Return compact item counts for the Page phase strip."""
    del lane  # typed items land only through their local Result binding
    plan_txt = plan.read_text(encoding="utf-8", errors="replace")
    page_txt = page_md.read_text(encoding="utf-8", errors="replace")
    approved = bool(re.search(r"^approved:\s*✅", plan_txt, re.M))
    page_accepted = bool(re.search(r"^accepted:\s*✅", page_txt, re.M))
    rows = read_items(page_md)
    root, page_dir = repo_root(page_md.parent), page_md.parent
    counts, statuses, n_items = {word: 0 for word in LADDER}, [], 0
    types = {item_type: 0 for item_type in ITEM_TYPES}
    for item_id, _target, _head, item_type, _expected, _acceptance, folded in bullets(plan_txt):
        n_items += 1
        types[item_type] += 1
        status = item_status(
            rows.get(item_id), folded, page_accepted, plan.stat().st_mtime,
            root, page_dir,
        )
        counts[status] += 1
        statuses.append(status)
    return {
        "marks": n_items,  # compatibility key used by the current strip
        "items": n_items,
        "rows": len(rows),
        "decided": sum(1 for row in rows.values() if row["decision"]),
        "counts": counts,
        "types": types,
        "cycle": cycle_now(approved, rows, statuses, n_items),
        "approved": approved,
    }
