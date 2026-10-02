"""🎨 Design · live Page-Folder presenter for ``haipipe-workbench-design``.

It reads only the current Design Folder's contract files: the Design Item
register, ``run-design-*`` Tickets, runtime receipts, ``checks.yaml``, content
artifacts, and ``decision.yaml``.  Every state on the page is derived from
those bytes at read time.  The only writes it exposes are the Design
contract's Commission release, the queueing of agent Tickets (Generate,
Verify), and a new register row; they live in
``servers/workbench-design/design_actions.py`` and write exactly the contract files.
"""
from __future__ import annotations

import difflib
import html
import importlib.util
import re
from pathlib import Path

from host_paths import HOST, SKILLS
from urllib.parse import parse_qs, quote, urlparse

try:
    import yaml
except ImportError:  # the presenter must still explain itself without PyYAML
    yaml = None

from live.insightboard import display_id, handoff_records, is_insight_board


_DESIGN_MARKER = re.compile(r"(?m)^\s*folder-kind:\s*design\s*$", re.I)
_LEGACY_RUN = re.compile(r"^r\d+_design(?:_|$)", re.I)
_RUN_FILE = re.compile(
    r"^(rd(\d+)_(commission|generate|verify|adopt)_[A-Za-z0-9][A-Za-z0-9_-]*)\.ya?ml$", re.I)
# the current name (JL 261001): run-design-<step>-<MMDD>-design-<N>[-2]; order is `sequence:`
_RUN_FILE_NEW = re.compile(
    r"^(run-design-(commission|generate|verify|adopt)-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*)\.ya?ml$")
_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_READS = re.compile(r"(?im)^\s*reads:\s*(.*?)\s*$")
_ITEM_HEAD = re.compile(r"^##\s+(ITEM\d+)\s*[·:-]\s*(.+?)\s*$")
_FIELD = re.compile(r"^([a-z][a-z-]*):\s*(.*?)\s*$")
_SIGNED = re.compile(r"(?im)^\s*signed:\s*(✅|⬜)\s*(.*?)\s*$")
_UNIT_CHECKER = (SKILLS / "design"
                 / "haipipe-design-unit" / "scripts" / "check_unit.py")
_STEP = {"commission": "Commission", "generate": "Generate",
         "verify": "Verify", "adopt": "Adopt (historical)"}
_ITEM_FIELDS = ("type", "audience", "job", "goal", "stance", "basis", "mode",
                "expected", "falsified", "because")
_ITEM_LISTS = ("acceptance", "evidence")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _escape(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def _yaml(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    try:
        data = yaml.safe_load(_read(path))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _legacy_reason(page_src: Path, text: str = "") -> str:
    folder = page_src.parent
    if folder.parent.name == "2-DS-design":
        return "legacy 2-DS-design/DS* folder is not a current Design Folder"
    if (folder / "design").is_dir():
        return "legacy design/DU* storage is not a current Design Folder"
    runs = folder / "runs"
    if runs.is_dir() and any(_LEGACY_RUN.match(p.name) for p in runs.iterdir()):
        return "legacy rNN_design_* Run storage is not supported"
    if re.search(r"(?im)^\s*(?:schema|contract-version):\s*v?1(?:\.0)?\s*$", text):
        return "legacy v1 Page/Ticket/Result storage is not supported"
    return ""


def design_contract_status(page_src: Path) -> tuple[bool, str]:
    """Return whether ``page_src`` is a current Design Page-Folder."""
    text = _read(page_src)
    if not page_src.is_file():
        return False, "Design Page source is missing"
    reason = _legacy_reason(page_src, text)
    if reason:
        return False, reason
    if not _DESIGN_MARKER.search(text):
        return False, "the Page source has no folder-kind: design marker"
    return True, ""


def is_current_design_page(page_src: Path) -> bool:
    return design_contract_status(page_src)[0]


def _relative_href(root: Path, path: Path) -> str:
    """A safe static path for a file inside the server root."""
    try:
        rel = path.resolve().relative_to(root.resolve())
    except (OSError, ValueError, RuntimeError):
        return ""
    return "/" + "/".join(quote(part) for part in rel.parts)


def _nearest_board(page_src: Path) -> Path | None:
    for candidate in (page_src.parent, *page_src.parents):
        if (candidate / "board.md").is_file():
            return candidate
    return None


def _declared_insight_boards(board_root: Path, names: list[str] | None = None) -> list[Path]:
    """Resolve the Insight boards named by the DesignBoard ``reads:`` line, or by ``names``."""
    if board_root is None:
        return []
    if names is None:
        text = _read(board_root / "board.md")
        match = _READS.search(text)
        if not match:
            return []
        names = re.split(r"\s*·\s*", match.group(1))
    found = {}
    for raw in names:
        name = raw.strip().strip("`'\"")
        if not name:
            continue
        for candidate in (board_root.parent / name, board_root / name):
            try:
                candidate = candidate.resolve()
            except OSError:
                continue
            if (candidate / "board.md").is_file() and is_insight_board(candidate):
                found[candidate] = candidate
    return sorted(found.values(), key=lambda path: path.as_posix())


def _insight_bindings(page_src: Path, server_root: Path, names: list[str] | None = None) -> dict:
    """Read the DesignBoard -> Insight board -> signed page binding chain.

    ``names`` overrides the board's ``reads:`` line (a Brief line may name the
    Insight board its design task draws from)."""
    design_board = _nearest_board(page_src)
    requested = [n.strip() for n in (names or []) if n and n.strip()]
    boards = []
    for board in _declared_insight_boards(design_board, requested or None):
        try:
            relative = board.resolve().relative_to(Path(server_root).resolve()).as_posix()
        except (OSError, ValueError, RuntimeError):
            live_url = ""
        else:
            live_url = "/_board/insight-board?path=%s" % quote(relative, safe="")
        records = handoff_records(board)
        boards.append({
            "board": board, "title": board.name, "live_url": live_url,
            "handoffs": records,
            "bindable": [row for row in records if row["bindable"]],
        })
    bindable = [row for board in boards for row in board["bindable"]]
    return {
        "design_board": design_board, "boards": boards, "bindable": bindable, "requested": requested,
        "status": ("bound" if bindable else "blocked" if boards
                   else "missing" if requested else "not-declared"),
    }


# ---------------------------------------------------------------- register --

def plan_folder(folder: Path) -> Path:
    """A Design Page's plan folder: ``draft/`` since Page layout 0.118, else the older ``outline/``."""
    draft = folder / "draft"
    return draft if draft.is_dir() or not (folder / "outline").is_dir() else folder / "outline"


def _register(folder: Path, stem: str) -> tuple[list[dict], Path]:
    """Parse ``draft/<stem>-design-items.md`` (``outline/`` before 0.118): one block per Design Item.

    The register is the bet and its rules (type, audience, job, goal,
    stance, basis, mode, expected, falsified, evidence, acceptance).  State is
    never read from it; it is derived from the Runs that name the item.
    """
    path = plan_folder(folder) / f"{stem}-design-items.md"
    items: list[dict] = []
    current = None
    for line in _read(path).splitlines():
        head = _ITEM_HEAD.match(line.strip())
        if head:
            current = {"id": head.group(1), "title": head.group(2), "_list": None,
                       **{key: "" for key in _ITEM_FIELDS}, **{key: [] for key in _ITEM_LISTS}}
            items.append(current)
            continue
        if current is None:
            continue
        if line.startswith("- ") and current["_list"]:
            current[current["_list"]].append(line[2:].strip())
            continue
        field = _FIELD.match(line.strip())
        if field:
            key, value = field.group(1), field.group(2)
            if key in _ITEM_LISTS and not value:
                current["_list"] = key
            elif key in _ITEM_FIELDS:
                current[key] = value
                current["_list"] = None
    for item in items:
        item.pop("_list", None)
    return items, path


# -------------------------------------------------------------------- runs --

def _actor(*records) -> tuple[str, str]:
    """Return (name, mode) from the first record that names an actor."""
    for record in records:
        if not isinstance(record, dict):
            continue
        actor = record.get("actor")
        if isinstance(actor, dict) and actor.get("owner"):
            return str(actor["owner"]), str(actor.get("mode") or "")
        if isinstance(actor, str) and actor:
            return actor, ""
        worker = record.get("worker")
        if isinstance(worker, dict) and worker.get("actor"):
            return str(worker["actor"]), "agent"
    return "", ""


def _when(value) -> str:
    text = str(value or "")
    text = text.replace("T", " ").rstrip("Z")
    return text[:16]


def _load_runs(folder: Path) -> list[dict]:
    runs_dir = folder / "runs"
    if not runs_dir.is_dir():
        return []
    rows = []
    for ticket_path in sorted(runs_dir.iterdir()):
        hit = _RUN_FILE.match(ticket_path.name)
        new = None if hit else _RUN_FILE_NEW.match(ticket_path.name)
        if not hit and not new:
            continue
        ticket = _yaml(ticket_path)
        if hit:
            run_id, number, kind = hit.group(1), int(hit.group(2)), hit.group(3).lower()
        else:
            run_id, kind = new.group(1), new.group(2)
            try:
                number = int(ticket.get("sequence") or 0)
            except (TypeError, ValueError):
                number = 0
        result_dir = folder / "results" / run_id
        runtime = _yaml(result_dir / "runtime.yaml")
        result = _yaml(result_dir / "result.yaml")
        decision = _yaml(result_dir / "decision.yaml")
        checks = _yaml(result_dir / "checks.yaml").get("checks") or []
        config_ref = ticket.get("config") if isinstance(ticket.get("config"), dict) else next(
            (r for r in ticket.get("inputs") or []           # a Commission pins its config among its inputs
             if isinstance(r, dict) and str(r.get("path", "")).startswith("scripts/config/")), {})
        config = _yaml(folder / str(config_ref.get("path", ""))) if config_ref.get("path") else {}
        name, mode = _actor(decision, runtime, ticket)
        mode = mode or ("human" if kind in ("commission", "adopt") else "agent")
        artifacts = []
        for ref in result.get("artifacts") or []:
            if isinstance(ref, dict) and ref.get("path"):
                path = result_dir / str(ref["path"])
                artifacts.append({"path": path, "text": _read(path).strip()})
        inputs = []
        for ref in ticket.get("inputs") or []:
            if isinstance(ref, dict) and ref.get("path") and ref.get("role"):
                inputs.append({"role": str(ref["role"]), "path": str(ref["path"]),
                               "run_id": str(ref.get("run_id") or ""),
                               "file": (folder / str(ref["path"])).resolve()})
        status = str(runtime.get("status") or ("complete" if decision else "planned"))
        stale = []
        if status == "planned" and kind in ("generate", "verify"):
            from live.design_actions import stale_inputs
            stale = stale_inputs(folder, run_id)
        verdict = str(result.get("verdict") or "")
        outcome = str(decision.get("decision") or runtime.get("terminal_outcome") or verdict)
        passed = sum(1 for c in checks if isinstance(c, dict) and c.get("status") == "pass")
        intent = config.get("design_intent") if isinstance(config.get("design_intent"), dict) else {}
        rows.append({
            "id": run_id, "number": number, "kind": kind, "step": _STEP[kind],
            "item": str(ticket.get("item") or config.get("item") or runtime.get("item") or ""),
            "target": str(ticket.get("target") or ""),
            "actor": name or "not recorded", "mode": mode,
            "status": status, "verdict": verdict, "outcome": outcome,
            "route": str(runtime.get("route") or ""),
            "started": _when(runtime.get("started_at")),
            "finished": _when(runtime.get("finished_at") or decision.get("at") or runtime.get("queued_at")),
            "failure": str(runtime.get("failure") or ""), "stale": stale,
            "words": str(decision.get("words") or ""),
            "checks": [c for c in checks if isinstance(c, dict)],
            "checks_passed": passed,
            "artifacts": artifacts, "inputs": inputs,
            "targets": [t for t in (ticket.get("targets") or []) if isinstance(t, dict)],
            "candidate": decision.get("candidate") if isinstance(decision.get("candidate"), dict) else {},
            "verification": decision.get("verification") if isinstance(decision.get("verification"), dict) else {},
            "preview": decision.get("preview") if isinstance(decision.get("preview"), dict) else {},
            "intent": {k: intent.get(k) for k in ("move", "basis", "stance", "expected_effect", "failure_condition")},
            "design_mode": str(config.get("mode") or ""),
            "criteria": config.get("criteria") or [],
            "acceptance": config.get("acceptance") if isinstance(config.get("acceptance"), list) else None,
            "ticket_path": ticket_path, "result_dir": result_dir,
        })
    rows.sort(key=lambda row: row["number"])
    return rows


def _fold_state(runs: list[dict], human: str = "person") -> tuple[str, str, str]:
    """Walk an item's Runs in order and return (state, glyph, waiting-on).

    "agent" is waited on only while a run is queued or running; a step that needs a
    click says "you" and never a name (JL 260921: a name here reads as the person who
    signed the last record, which is a different fact). `human` is kept for callers
    that still pass it and is no longer written to a surface."""
    state, glyph, waiting = "not commissioned", "⬜", "you · commission"
    for run in runs:
        if run["status"] == "superseded":
            continue
        if run["status"] == "blocked":
            state, glyph, waiting = "blocked", "⏸", f"you · resolve {run['id']}: {run['failure'] or 'blocked; inspect the Run record'}"
            continue
        if run["kind"] == "commission":
            if run["outcome"] == "release":
                state, glyph, waiting = "commissioned", "⬜", "you · queue the draft"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "commission held", "⏸", "you · release or hold"
            else:
                state, glyph, waiting = "commission open", "⬜", "you · release or hold"
        elif run["kind"] == "generate":
            if run["status"] == "complete":
                state, glyph, waiting = "generated", "⬜", "you · queue the review"
            elif run["status"] == "failed":
                state, glyph, waiting = "generate failed", "✗", "you · queue a revise"
            elif run["status"] == "planned" and run.get("stale"):
                state, glyph, waiting = "queued run out of date", "⚠", "you · queue again"
            elif run["status"] == "planned":
                state, glyph, waiting = "generate queued", "⬜", "agent · generate"
            else:
                state, glyph, waiting = "generating", "⬜", "agent · running"
        elif run["kind"] == "verify":
            if run["status"] == "complete" and run["verdict"] == "pass":
                state, glyph, waiting = "ready", "✅", ""
            elif run["status"] == "complete" and run["verdict"] == "unresolved":
                owners = sorted({str(c.get("next_owner")) for c in run["checks"]
                                 if c.get("status") == "unresolved" and c.get("next_owner")})
                owner_text = ", ".join(owners) if owners else "you"
                state, glyph, waiting = "verify unresolved", "⏸", (
                    f"{owner_text} · resolve the recorded evidence/criterion gap; "
                    "preserve this Result and review only after inputs or criteria change")
            elif run["status"] == "complete":
                state, glyph, waiting = "verify failed", "✗", "you · queue a revise"
            elif run["status"] == "failed":
                # The review itself did not pass the gate: redo the review, not the candidate.
                state, glyph, waiting = "verify invalid", "✗", "you · queue the review again"
            elif run["status"] == "planned" and run.get("stale"):
                state, glyph, waiting = "queued run out of date", "⚠", "you · queue again"
            elif run["status"] == "planned":
                state, glyph, waiting = "verify queued", "⬜", "agent · verify"
            else:
                state, glyph, waiting = "verifying", "⬜", "agent · running"
        elif run["kind"] == "adopt":
            # Historical adoption records are read as an already-ready delivery.
            # New records never create this kind; the user-facing workflow ends at Verify.
            if run["outcome"] == "adopt":
                state, glyph, waiting = "ready", "✅", ""
            elif run["outcome"] == "decline":
                state, glyph, waiting = "declined", "🚫", ""
            elif run["outcome"] == "revise":
                state, glyph, waiting = "generated", "⬜", "you · queue the review"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "legacy hold", "⏸", "you · historical decision; register a new item to continue"
            else:
                state, glyph, waiting = "generated", "⬜", "you · queue the review"
    return state, glyph, waiting


def _unit_gate():
    spec = importlib.util.spec_from_file_location("design_unit_gate", _UNIT_CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _audit(folder: Path) -> list[str]:
    """Run the Design Unit gate read-only; a missing checker is reported, not hidden."""
    if not _UNIT_CHECKER.is_file():
        return ["check_unit.py not found beside haipipe-design-unit"]
    try:
        module = _unit_gate()
        return [str(issue).replace(str(folder) + "/", "") for issue in module.audit_folder(folder)]
    except Exception as exc:  # noqa: BLE001 - a presenter never crashes on the checker
        return [f"checker unavailable: {exc}"]


def _relocated(folder: Path, rel: str) -> Path | None:
    """A cited page whose Insight board has moved: found by its last three path parts
    (`1-F-full/FW01-send-salience/FW01-send-salience.md`) under the nearest Project's
    `insights/` world. The register keeps its old path, so no released Run goes stale."""
    tail = "/".join(Path(rel).parts[-3:])
    for up in folder.parents:
        world = up / "insights"
        if world.is_dir():
            hits = sorted(world.glob(f"*/{tail}"))
            return hits[0].resolve() if hits else None
    return None


def _evidence_rows(folder: Path, item: dict) -> list[dict]:
    """Merge register evidence lines with the roles the item's Tickets pinned."""
    rows: dict[str, dict] = {}
    from live.design_actions import split_evidence
    for line in item["evidence"]:
        role, rel = split_evidence(line)
        rows[rel] = {"role": role, "path": rel, "file": (folder / rel).resolve(), "pinned": False}
    for run in item["runs"]:
        if run["status"] == "superseded":
            continue
        for ref in run["inputs"]:
            if ref["role"] in ("base", "feedback"):
                continue
            if ref["path"].startswith("scripts/config/"):
                continue
            row = rows.setdefault(ref["path"], {"role": ref["role"], "path": ref["path"],
                                                "file": ref["file"], "pinned": False})
            row["pinned"] = True
    out = []
    for row in rows.values():
        if not row["file"].is_file():
            row["file"] = _relocated(folder, row["path"]) or row["file"]
        text = _read(row["file"]) if row["file"].is_file() else ""
        signed = _SIGNED.search(text)
        row["exists"] = row["file"].is_file()
        row["name"] = Path(row["path"]).name
        row["signed"] = (f"signed ✅ {signed.group(2)}".strip() if signed and signed.group(1) == "✅"
                         else "unsigned ⬜" if signed else "")
        out.append(row)
    return out


# `because: W01-full · W1, W3` (or the older `FW02 · W1`): the insight rows a design acts on.
_BECAUSE = re.compile(r"^([DIKW]\d{2}-[a-z]+|[A-Z][DIKW]\d{2})\s*[·:\s]\s*([A-Z]\d+(?:\s*,\s*[A-Z]\d+)*)$")


def because_rule(item: dict) -> dict:
    """The one insight rule an item says it acts on: register line `because: FW02 · W1`.

    state is "rule" (found; `rule` holds its DO / DO NOT sentence), "unknown" (named
    but not on the cited page), "ai" (`because: none`, or built from the Brief only:
    an AI idea, not from an insight) or "unnamed" (built on evidence, no rule named).
    The page is looked up among the item's evidence first, then on the same Insight board."""
    raw = (item.get("because") or "").strip()
    out = {"state": "unnamed", "ref": raw, "page": None, "rule": None}
    if raw.lower() in ("none", "no insight", "-") or (not raw and item.get("basis") != "evidence-informed"):
        return {**out, "state": "ai"}
    hit = _BECAUSE.match(raw.split(";")[0].strip())
    if not hit:
        return out if not raw else {**out, "state": "unknown"}
    pid, rid = hit.group(1), re.split(r"\s*,\s*", hit.group(2))[0]
    out["ref"] = f"{pid} · {rid}"
    page = _cited_page(item, pid)
    if page is None:
        return {**out, "state": "unknown"}
    from live.design_actions import counsel_lines
    rule = next((r for r in counsel_lines(_read(page)) if r["id"] == rid), None)
    return {**out, "state": "rule" if rule else "unknown", "page": page, "rule": rule}


def because_words(item: dict) -> str:
    """The because line as plain text, for the csv: `FW02 · W1: DO run a factorial round …`."""
    b = item.get("because_rule") or because_rule(item)
    if b["state"] == "rule":
        return f'{b["ref"]}: {"DO" if b["rule"]["do"] else "DO NOT"} {b["rule"]["text"]}'
    return {"ai": "AI idea, not from an insight", "unnamed": ""}.get(b["state"], f'{b["ref"]} (not found)')


_TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
_HANDOFF_KEY = re.compile(r"^(FINDING|STRENGTH|BOUNDARY|CONSEQUENCE|OVERREACH)\s{2,}(.*)$")
_ROLE_WORDS = {"handoff": "signed insight", "evidence": "evidence", "inspiration": "inspiration",
               "reference": "reference", "avoid": "avoid"}


def brief_page(board_root: Path | None) -> Path | None:
    """The Brief page under 0-BR-brief/: the list of what the board asks Design for."""
    if board_root is None:
        return None
    for page in sorted(Path(board_root).glob("0-BR-brief/*/*.md")):
        if page.name == f"{page.parent.name}.md":
            return page
    return None


def is_task_header(cells: list[str]) -> bool:
    """The Brief's design-task table names audience, job and venue in its header;
    an audience table elsewhere in the Brief is never read as the task list."""
    low = [c.strip().lower() for c in cells]
    return all(any(word in c for c in low) for word in ("audience", "job", "venue"))


def brief_rows(brief_text: str) -> list[dict]:
    """The Brief's list: one line per audience × job × venue, columns matched by header word.

    The first Markdown table whose header names ``audience``, ``job`` and ``venue`` is the list.  A
    ``folder`` cell of ``—`` or empty means no Design Folder exists yet; a
    ``designs`` cell says how many designs the line asks for.
    """
    rows: list[dict] = []
    header: list[str] | None = None
    for line in brief_text.splitlines():
        hit = _TABLE_ROW.match(line)
        if not hit:
            if header is not None and rows:
                break
            header = None
            continue
        cells = [c.strip() for c in hit.group(1).split("|")]
        if header is None:
            if is_task_header(cells):
                header = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        row = {"id": "", "audience": "", "job": "", "venue": "", "folder": "", "designs": 0, "insight": ""}
        for key, value in zip(header, cells):
            for name in ("audience", "job", "venue", "folder", "insight"):
                if name in key:
                    row[name] = value
            if "design" in key or "wanted" in key or "how many" in key:
                row["designs"] = int(value) if value.strip().isdigit() else 0
            if key in ("row", "id", "#", "line", "page"):
                row["id"] = value
        if row["folder"] in ("—", "-", "–", "none", "(none)"):
            row["folder"] = ""
        row["folder"] = row["folder"].strip("`")
        row["insight"] = row["insight"].strip("`")
        if row["insight"] in ("—", "-", "–", "none", "(none)", "(board default)"):
            row["insight"] = ""
        if not row["id"]:
            row["id"] = f"R{len(rows) + 1}"
        rows.append(row)
    return rows


_VENUE_WORDS = {"sms": "SMS", "ui-card": "app card", "push": "push message", "email": "email"}


def venue_word(venue: str) -> str:
    """A Brief venue in reader words: sms -> SMS, ui-card -> app card."""
    venue = (venue or "").strip()
    return _VENUE_WORDS.get(venue.lower(), venue.replace("-", " "))


def design_title(row: dict) -> str:
    """A Design Folder's title as one plain phrase from its Brief line: 'Prescription review SMS for all patients'."""
    job = (row.get("job") or "").strip()
    head = " ".join(x for x in (job[:1].upper() + job[1:], venue_word(row.get("venue", ""))) if x) or "Design"
    audience = (row.get("audience") or "").strip()
    return f"{head} for {audience}" if audience else head


LINK_SLOT = "{LINK}"


def with_link(text: str) -> str:
    """Show `{LINK}` where the platform puts the link: right after the ask's colon, before
    the opt-out (JL 261001). The stored text is unchanged; a text that already carries
    `{LINK}` is shown as it is."""
    if not text or LINK_SLOT in text:
        return text
    stop = text.rfind("Reply STOP")
    colon = (text[:stop] if stop > 0 else text).rfind(":")
    return text if colon < 0 else text[:colon + 1] + " " + LINK_SLOT + text[colon + 1:]


# The design input (JL 261001): Theory of Design §2 says a design starts from an aim,
# constraints and resources. The board's `design-goal.md` states them once; a task
# section overrides a line; the venue profile gives the channel's own defaults.
_INPUT_BLOCKS = ("Aim", "Venue", "Rules", "Resources", "Leave out")
_VENUE_DIR = SKILLS / "design" / "venue"
_VENUE_LABEL = {"length": "Length", "cta": "Call to action", "opt-out": "Opt-out", "personalization": "Personalization",
                "links": "Link", "language": "Reading level"}


def _input_sections(text: str) -> list[tuple[str, list[tuple[str, str, str]]]]:
    """ASCII doc -> [(title, [(key, value, source)])]; a title is a line underlined by --- or ===."""
    lines, out, i = text.splitlines(), [], 0
    while i < len(lines):
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if lines[i].strip() and re.fullmatch(r"[-=]{3,}", nxt):
            out.append((lines[i].strip(), []))
            i += 2
            continue
        m = re.match(r"^([A-Za-z][\w -]*?):\s*(.*?)\s*(?:<-\s*(.*))?$", lines[i])
        if m and out:
            out[-1][1].append((m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()))
        i += 1
    return out


def venue_defaults(venue: str) -> dict[str, str]:
    """`- **Length:** 160 chars ...` lines under a venue README's `## Constraints`."""
    path = _VENUE_DIR / f"venue-{(venue or '').strip().lower()}" / "README.md"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    part = text.split("## Constraints", 1)[1].split("\n## ", 1)[0] if "## Constraints" in text else ""
    return {m.group(1).strip().lower(): m.group(2).strip()
            for m in re.finditer(r"(?m)^-\s+\*\*(.+?):\*\*\s*(.+?)\s*$", part)}


def design_input(board: Path | None, folder: Path) -> dict:
    """The board's design input with this folder's overrides: {block: [(key, value, source)]}."""
    path = board / "design-goal.md" if board else None
    if not path or not path.is_file():
        return {"path": None, "blocks": {}}
    sections = _input_sections(path.read_text(encoding="utf-8", errors="replace"))
    blocks = {title: list(rows) for title, rows in sections if title in _INPUT_BLOCKS}
    for title, rows in sections:
        if title == f"Task · {folder.name}":
            for key, value, source in rows:
                for name, lines in blocks.items():
                    if any(k == key for k, _, _ in lines):
                        blocks[name] = [(k, value, source) if k == key else (k, v, s) for k, v, s in lines]
                        break
                else:
                    blocks.setdefault("Aim", []).append((key, value, source))
    return {"path": path, "blocks": blocks}


def _input_html(root: Path, row: dict, inp: dict, counts: str, rules: list[str]) -> str:
    """The Design Goal Space: the task's design input as column tables, as in the Paper workbench."""
    # The screen shows the specification only; where each line came from stays in the
    # file after `<-` (JL 261001: no source column, no file ids on screen).
    blocks = inp["blocks"]

    def cell(value: str) -> str:
        return '<span class=mut>Not specified</span>' if value in ("", "?") else _escape(value)

    def grid(title: str, heads: tuple[str, ...], rows: list[str]) -> str:
        head = "".join(f"<th>{_escape(h)}</th>" for h in heads)
        return f'<h3>{title}</h3><table class="grid input"><tr>{head}</tr>{"".join(rows)}</table>'

    def line(key: str, value: str) -> str:
        return f'<tr><td class=key>{_escape(key[:1].upper() + key[1:])}</td><td>{cell(value)}</td></tr>'

    job = (row["job"] or "").strip()
    out = []
    aim = [line(k, v) for k, v, _ in blocks.get("Aim", [])]
    if job and not any(k.lower() == "patient task" for k, _, _ in blocks.get("Aim", [])):
        aim.insert(1, line("Patient task", job[:1].upper() + job[1:]))
    aim.append(f'<tr><td class=key>Deliverables</td><td>{counts}</td></tr>')
    out.append(grid("Aim", ("Item", "Specification"), aim))
    venue = row["venue"] or ""
    defaults = {k: v[:1].upper() + v[1:] for k, v in venue_defaults(venue).items()}
    used, rows = set(), []
    for key, value, _ in blocks.get("Venue", []):
        used.add(key.lower())
        rows.append(f'<tr><td class=key>{_escape(_VENUE_LABEL.get(key.lower(), key))}</td><td>{cell(value)}</td>'
                    f'<td class=mut>{_escape(defaults.get(key.lower(), "—"))}</td></tr>')
    rows += [f'<tr><td class=key>{_escape(_VENUE_LABEL.get(k, k))}</td><td class=mut>As the channel standard</td>'
             f'<td class=mut>{_escape(v)}</td></tr>' for k, v in defaults.items() if k not in used]
    name = venue.upper() if len(venue) <= 4 else venue.title()
    out.append(grid(f"Channel requirements · {_escape(name)}", ("Requirement", "This task", f"{name} standard"), rows)
               if rows else f'<h3>Channel requirements · {_escape(name)}</h3><div class=empty>No channel profile for {_escape(venue)}.</div>')
    rule_rows = [line(k, v) for k, v, _ in blocks.get("Rules", [])]
    if rules:
        rule_rows.append(f'<tr><td class=key>Acceptance checks</td><td>{"<br>".join(_escape(r) for r in rules)}</td></tr>')
    out.append(grid("Requirements", ("Item", "Specification"), rule_rows))
    for title, heading in (("Resources", "Inputs and resources"), ("Leave out", "Exclusions")):
        if blocks.get(title):
            out.append(grid(heading, ("Item", "Specification"), [line(k, v) for k, v, _ in blocks[title]]))
    if not inp["path"]:
        out.append('<div class=bad>No design-goal.md beside board.md: only the task line is shown.</div>')
    return "".join(out)


def _goal(folder: Path, board_root: Path | None, items: list[dict]) -> dict:
    """Goal Space: the Brief line that names this folder, and the counts against it."""
    brief = brief_page(board_root)
    rows = brief_rows(_read(brief)) if brief else []
    row = next((r for r in rows if r["folder"] == folder.name), None)
    sentence = ""
    if row:
        wanted = row["designs"]
        what = " ".join(x for x in (row["job"].strip(), venue_word(row["venue"])) if x)
        head = f"{wanted} {what} design{'s' if wanted != 1 else ''}" if wanted else f"{what} designs"
        sentence = f"{head} for {row['audience'].strip()}"
    return {"brief": brief, "row": row, "sentence": sentence, "insight": row["insight"] if row else "",
            "wanted": row["designs"] if row else 0, "registered": len(items),
            "ready": sum(1 for i in items if i.get("ready"))}


def _verified_design(item: dict) -> dict | None:
    """Return the candidate whose latest independent Verify passed.

    Delivery is deliberately derived from the Verify record, not from a
    separate human decision.  Historical ``run-design-adopt-*`` records may still
    be present, but they are not required for a design to be ready.
    """
    if item.get("state") != "ready":
        return None
    runs = item.get("runs") or []
    verify = next((r for r in reversed(runs)
                   if r["kind"] == "verify" and r["status"] == "complete"
                   and r.get("verdict") == "pass"), None)
    if verify is None:
        return None
    targets = verify.get("targets") or []
    target_path = str(targets[0].get("path") or "") if targets else ""
    target_file = (verify["ticket_path"].parent.parent / target_path).resolve() if target_path else None
    candidate = next((r for r in reversed(runs)
                      if r["kind"] == "generate" and r["status"] == "complete"
                      and r.get("artifacts")
                      and target_file == (r["result_dir"] / "result.yaml").resolve()), None)
    if candidate is None:
        return None
    # A completion receipt describes a past event; Delivery must still bind
    # the reviewed files. Recheck the two Results before exporting them.
    try:
        gate = _unit_gate()
        for run in (candidate, verify):
            problems = gate.validate(run["ticket_path"], run["result_dir"] / "result.yaml", historical=True)
            if problems:
                raise ValueError(f"{run['id']}: {'; '.join(problems)}")
        _, _, _, _, config, _ = gate.context(verify["ticket_path"], historical=True)
        if config["review_mode"] != "independent":
            raise ValueError(f"{verify['id']}: Delivery requires independent review")
    except (OSError, ImportError, AttributeError, TypeError, KeyError) as exc:
        raise ValueError(f"Delivery records check unavailable: {exc}") from exc
    art = candidate["artifacts"][0]
    return {"run": candidate["id"], "text": art["text"], "verification": verify["id"]}


_LEVEL_WORD = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_INSIGHT_PAGE = re.compile(r"^([A-Z][DIKW]\d{2})-(.+)$")
_INSIGHT_REF = re.compile(r"\b([A-Z][DIKW]\d{2})\b")


def _partitions_of(board_root: Path) -> dict[str, str]:
    """`1-F-full` -> {"F": "full"}: the data cuts an Insight board declares by folder."""
    out = {}
    for folder in board_root.glob("*"):
        cut = re.match(r"^\d+-([A-Z])-(.+)$", folder.name)
        if cut and folder.is_dir():
            out[cut.group(1)] = cut.group(2)
    return out


def insight_label(page: Path) -> dict:
    """`1-F-full/FW01-send-salience/FW01-send-salience.md` said in words:
    id `FW01`, shown `full-W01`, words "send salience", level "Wisdom"
    (JL 260918: "FW is very hard to understand", "FD02 to be full-D02")."""
    hit = _INSIGHT_PAGE.match(page.stem)
    if not hit:
        return {"id": "", "shown": "", "words": page.stem.replace("-", " "), "level": ""}
    pid, slug = hit.groups()
    shown = display_id(pid, _partitions_of(page.parent.parent.parent))
    return {"id": pid, "shown": shown, "words": slug.replace("-", " "), "level": _LEVEL_WORD[pid[1]]}


def insight_caption(page: Path) -> str:
    """`Wisdom · full-W01`, or the file name for a non-insight file."""
    lab = insight_label(page)
    return f'{lab["level"]} · {lab["shown"]}' if lab["id"] else page.name


def name_refs(escaped: str, page: Path) -> str:
    """Name the pages a finding cites, in already-escaped text:
    `(FK03 · K1, K3)` becomes `(no generative rule · K1, K3)`, `full-K03` on hover."""
    root = page.parent.parent.parent
    parts, names = _partitions_of(root), {}
    for folder in root.glob("*/*"):
        hit = _INSIGHT_PAGE.match(folder.name)
        if hit and folder.is_dir():
            names[hit.group(1)] = hit.group(2).replace("-", " ")
    return _INSIGHT_REF.sub(lambda m: (f'<span title="{display_id(m.group(1), parts)}">{html.escape(names[m.group(1)])}</span>'
                                       if m.group(1) in names else display_id(m.group(1), parts)), escaped)


def _handoff_says(text: str) -> dict:
    """FINDING and CONSEQUENCE of a Design Handoff block, continuation lines joined;
    falls back to the first line under ## Opening."""
    from live.design_actions import counsel_lines
    out = {"finding": "", "consequence": "", "counsel": counsel_lines(text)}
    key = None
    for line in text.splitlines():
        hit = _HANDOFF_KEY.match(line)
        if hit:
            key = hit.group(1).lower()
            if key in out:
                out[key] = hit.group(2).strip()
            continue
        if key in out and line.startswith("  ") and line.strip():
            out[key] += " " + line.strip()
        elif not line.startswith("  "):
            key = None
    if not out["finding"]:
        title = _TITLE.search(text)
        opening = re.search(r"(?ms)^## Opening\s*\n(.*?)(?=^## |\Z)", text)
        first = next((l.strip() for l in opening.group(1).splitlines() if l.strip()), "") if opening else ""
        # the opening line is a question on most pages; the title says what the page found
        out["finding"] = first if first and not first.endswith("?") else (title.group(1).strip() if title else first)
    return out


def _insight_space(items: list[dict], insight: dict) -> dict:
    """Insight Space: per item, the insights that support it; then what the board offers unused."""
    used: set[Path] = set()
    per_item = []
    for item in items:
        rows = []
        for r in item["evidence_rows"]:
            says = (_handoff_says(_read(r["file"])) if r["exists"] and r["role"] in ("handoff", "evidence")
                    else {"finding": "", "consequence": "", "counsel": []})
            rows.append({**r, **says, "word": _ROLE_WORDS.get(r["role"], r["role"])})
            if r["exists"]:
                try:
                    used.add(r["file"].resolve())
                except OSError:
                    pass
        per_item.append({"item": item, "rows": rows,
                         "needed": item["basis"] == "evidence-informed" and not rows})
    unused = []
    for board in insight["boards"]:
        for h in board["handoffs"]:
            page = Path(h["page"])
            if not page.is_absolute():
                page = Path(board["board"]) / page
            try:
                resolved = page.resolve()
            except OSError:
                continue
            if resolved not in used:
                unused.append({"title": h["title"], "name": page.name, "file": page,
                               "signed": h["signature"] if h["signed"] else ""})
    return {"items": per_item, "unused": unused}


_PICTURE = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")


def _renders(folder: Path, runs: list[dict]) -> dict[str, list[dict]]:
    """Read Result-local evidence first; retain old Delivery manifests as history."""
    try:
        import json
        rows = json.loads(_read(folder / "delivery" / "render" / "manifest.json") or "[]")
    except ValueError:
        rows = []
    out: dict[str, list[dict]] = {}
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict) and row.get("item") and row.get("render"):
            path = folder / "delivery" / "render" / str(row["render"])
            out.setdefault(str(row["item"]), []).append(
                {**row, "path": path, "picture": path.suffix.lower() in _PICTURE and path.is_file()})
    gate = None
    for run in runs:
        if run["kind"] != "generate" or run["status"] != "complete":
            continue
        result_path = run["result_dir"] / "result.yaml"
        manifest = _yaml(result_path)
        if "render_manifest" not in manifest:
            continue
        # An invalid current manifest must not silently fall back to an old picture.
        for item_rows in out.values():
            item_rows[:] = [row for row in item_rows if row.get("candidate") != run["id"]]
        try:
            gate = gate or _unit_gate()
            # Same rule as the records check: a file newer than result.yaml is stale (file time, no hash).
            subjects = {path: run["id"] for _, path in
                        gate.artifact_records(run["result_dir"], manifest.get("artifacts"), record=result_path)}
            for row in gate.render_records(run["result_dir"], manifest, subjects, run["item"],
                                           record=result_path):
                out.setdefault(run["item"], []).append(
                    {**row, "picture": row["path"].suffix.lower() in _PICTURE})
        except (OSError, ValueError, TypeError, KeyError, ImportError, AttributeError):
            # The folder audit reports the error; the presenter shows no false preview.
            continue
    return out


def _render_for(rows: list[dict], run: str) -> dict | None:
    """The picture of exactly this draft; a picture of an older draft is never shown for a newer one."""
    def version(row):
        # Historical Delivery manifests also used numeric strings or no version.
        # New Result manifests already enforce a positive integer in the gate.
        try:
            return int(row.get("version") or 0)
        except (TypeError, ValueError, OverflowError):
            return -1
    hits = [r for r in rows if r.get("candidate") == run and r["picture"]
            and version(r) >= 0]
    return max(hits, key=version) if hits else None


def design_picture(root: Path, item: dict, alt: str = "") -> str:
    """An <img> of the item's rendered screen, or '' when its design is text only."""
    render = item.get("render")
    if not render:
        return ""
    src = _relative_href(Path(root), render["path"])
    if not src:
        import base64
        kind = "svg+xml" if render["path"].suffix.lower() == ".svg" else render["path"].suffix.lower().lstrip(".").replace("jpg", "jpeg")
        src = f"data:image/{kind};base64," + base64.b64encode(render["path"].read_bytes()).decode("ascii")
    return (f'<img class=shot src="{_escape(src)}" alt="{_escape(alt or item.get("title", ""))}" loading=lazy>')


def _open_request(folder: Path, stem: str) -> dict | None:
    from live.design_actions import open_draft_request
    try:
        return open_draft_request(folder, stem)
    except (OSError, ValueError):
        return None


def design_snapshot(page_src: Path, server_root: Path | None = None) -> dict:
    """Collect the read-only Design Folder projection."""
    page_src = Path(page_src)
    folder = page_src.parent
    current, reason = design_contract_status(page_src)
    root = Path(server_root or folder)
    text = _read(page_src)
    title = (_TITLE.search(text).group(1).strip() if _TITLE.search(text) else page_src.stem)
    items, register_path = _register(folder, page_src.stem)
    runs = _load_runs(folder) if current else []
    human = next((r["actor"] for r in runs if r["mode"] == "human" and r["actor"] != "not recorded"), "person")
    known = {item["id"] for item in items}
    renders = _renders(folder, runs)
    for item in items:
        item["runs"] = [run for run in runs if run["item"] == item["id"]]
        item["state"], item["glyph"], item["waiting"] = _fold_state(item["runs"], human)
        item["evidence_rows"] = _evidence_rows(folder, item)
        item["because_rule"] = because_rule(item)
        latest = next((r for r in reversed(item["runs"])
                       if r["kind"] == "generate" and r["artifacts"] and r["status"] == "complete"), None)
        item["latest"] = ({"run": latest["id"], "text": latest["artifacts"][0]["text"],
                           "status": latest["status"], "verdict": latest["verdict"]} if latest else None)
        # A passed Verify is the delivery gate.  Keep the old projection for
        # callers that still inspect it, but never use it as a new workflow.
        try:
            item["ready"] = _verified_design(item)
            delivery_error = "no valid independent Verify target" if item["state"] == "ready" and not item["ready"] else ""
        except ValueError as exc:
            item["ready"], delivery_error = None, str(exc)
        if delivery_error:
            item["state"], item["glyph"] = "records invalid", "⚠"
            item["waiting"] = f"you · the records for this item do not line up: {delivery_error}"
        item["adopted"] = None
        shown = shown_design(item)
        item["render"] = _render_for(renders.get(item["id"], []), shown["run"]) if shown else None
    goal = _goal(folder, _nearest_board(page_src), items)
    insight = _insight_bindings(page_src, root, [goal["insight"]] if goal["insight"] else None)
    return {
        "current": current, "reason": reason, "title": title, "page": page_src,
        "folder": folder, "root": root, "items": items, "register": register_path,
        "runs": runs, "unassigned": [run for run in runs if run["item"] not in known],
        "insight": insight,
        "goal": goal,
        "draft_request": _open_request(folder, page_src.stem),
        "insight_space": _insight_space(items, insight),
        "audit": _audit(folder) if current else [],
        "human": human, "yaml": yaml is not None,
    }


# ------------------------------------------------------------------ render --

_CSS = """
:root{--fg:#1c1c1c;--mut:#6f6f6b;--line:#e4e4e7;--bg:#fff;--acc:#3e5c84;--bad:#b3541e;--ok:#3a7d44;--soft:#f5f6f8}
@media(prefers-color-scheme:dark){:root{--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--bg:#161719;--acc:#7d9cc4;--bad:#e0955a;--ok:#7dbb87;--soft:#20242a}}
*{box-sizing:border-box}body{margin:0;padding:16px 18px;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1100px}
h1{font-size:17px;margin:0 0 2px;font-weight:650}h2{font-size:14px;margin:18px 0 6px;font-weight:650}
.mut{color:var(--mut);font-size:12.5px}.bad{color:var(--bad)}.ok{color:var(--ok)}
.tabs{display:flex;gap:4px;margin:12px 0 4px;border-bottom:1px solid var(--line)}
.tabs button{font:600 12.5px -apple-system,sans-serif;border:0;border-bottom:2px solid transparent;padding:6px 10px;cursor:pointer;background:transparent;color:var(--mut)}
.tabs button.on{color:var(--fg);border-bottom-color:var(--acc)}
.pane{display:none}.pane.on{display:block}
table{border-collapse:collapse;width:100%;margin:4px 0 8px}td,th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.03em}
code{font:12px ui-monospace,Menlo,monospace;word-break:break-word}a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
details{margin:2px 0}summary{cursor:pointer;color:var(--acc);font-size:12.5px}
ul.rules{margin:2px 0 0 16px;padding:0}ul.rules li{margin:1px 0}
.item{border-top:2px solid var(--line);padding:12px 0 14px;margin:0}.item.sel{background:var(--soft);margin:0 -10px;padding:12px 10px 14px}
.item .head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline}
.item .head b{font-size:15px}
pre.text{margin:8px 0;padding:10px 12px;background:var(--soft);border-left:3px solid var(--acc);font:15px/1.45 -apple-system,sans-serif;white-space:pre-wrap;word-break:break-word}
table.kv{margin:6px 0}table.kv th{width:88px;text-transform:none;letter-spacing:0;font-size:12px;color:var(--mut);border-bottom:0;padding:3px 8px 3px 0}
table.kv td{border-bottom:0;padding:3px 0}
.card{border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:8px 0}
.card .head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.act{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
table.designs td.who{width:230px}.design{white-space:pre-wrap;word-break:break-word;font-size:14.5px}details.decide{margin-top:8px}details.decide .act{margin-top:6px}
.act input,.act textarea,.form input,.form textarea,.form select{font:13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:4px;padding:4px 6px;background:var(--bg);color:var(--fg)}
.act input.name{width:90px}.act input.words{width:min(420px,100%)}
button.do{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);border-radius:4px;padding:4px 10px;background:var(--bg);color:var(--acc);cursor:pointer}
button.do:hover{background:var(--soft)}button.do.bad{border-color:var(--bad);color:var(--bad)}
.msg{font-size:12.5px;margin-top:4px}.msg.bad{color:var(--bad)}.msg.ok{color:var(--ok)}
.form{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;max-width:760px;margin:6px 0}.form label{color:var(--mut);font-size:12px;padding-top:5px}
.form textarea{min-height:56px}.form .full{grid-column:1/3}
.empty{color:var(--mut);padding:10px 0}
.pair{display:flex;gap:22px;align-items:flex-start}.pair .pic{flex:0 0 260px;min-width:0}.pair .facts{flex:1;min-width:0}
.pair.text .pic{flex:0 0 min(300px,38%)}.pair.text pre.text{margin-top:4px}.pair .facts table.kv{margin-top:0}
.phone{border:1px solid var(--line);border-radius:18px;padding:12px 12px 16px;margin:8px 0 4px;background:var(--bg);max-width:280px}
.phone .from{font-size:11px;color:var(--mut);text-align:center;margin-bottom:10px}
.bubble{background:var(--soft);border-radius:16px 16px 16px 4px;padding:8px 11px;font:14.5px/1.42 -apple-system,sans-serif;white-space:pre-wrap;word-break:break-word}
.bubble .link{color:var(--acc);text-decoration:underline}
.item{padding:0}.item.sel{margin:0;padding:0;background:none}.item.sel>details>summary{box-shadow:inset 3px 0 0 var(--acc)}.foldbar{margin:6px 0 2px;text-align:right}
details.itemfold.cardrow>summary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;height:auto;min-height:34px;align-items:center;padding:9px 4px;font-size:13px}
details.itemfold.cardrow>summary::before{display:none}details.itemfold.cardrow>summary>span{min-width:0;display:flex;flex-direction:column;gap:2px;overflow:hidden}
details.itemfold.cardrow>summary .c1 b{max-width:none;white-space:normal}details.itemfold.cardrow>summary .c1 .line>b:first-child::before{content:"▸ ";color:var(--mut)}
details.itemfold.cardrow[open]>summary .c1 .line>b:first-child::before{content:"▾ "}details.itemfold.cardrow .peek{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
details.itemfold.cardrow .move{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
details.itemfold.cardrow .sup,details.itemfold.cardrow .wrong{font-size:12.5px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cardgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;padding:6px 4px 14px;align-items:start}
.cardgrid>.col{min-width:0}
h4.colh{margin:12px 0 4px;font:650 11px -apple-system,sans-serif;letter-spacing:.05em;text-transform:uppercase;color:var(--mut)}
.cardgrid>.col>h4.colh:first-child{margin-top:2px}
details.sub{border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:6px 10px}details.sub>summary{font-size:13px;color:var(--fg);font-weight:600}
details.sub[open]>summary{margin-bottom:6px}ul.notes{margin:0;padding-left:18px;font-size:13px;line-height:1.5}ul.notes li{margin:3px 0}
@media(max-width:860px){.cardgrid{grid-template-columns:1fr}.cardgrid>.col.pic{position:static}}
details.runsfold{margin:6px 0 8px}details.runsfold>summary{font-size:12px;color:var(--mut);font-weight:400}
details.runsfold[open]>summary{margin-bottom:4px}
details.itemfold.cardrow .line{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.runs{list-style:none;margin:0;padding:0}ul.runs li{padding:6px 0;border-bottom:1px dashed var(--line)}ul.runs li:last-child{border-bottom:0}
ul.runs .rl{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline;font-size:13px}ul.runs .rid{font-size:11px;color:var(--mut)}
ul.runs .said{font-size:12.5px;color:var(--mut);font-style:italic;margin:2px 0}ul.runs li.old{opacity:.6}
.chain{margin:2px 0 8px}.chain .node,.node.limit{padding:3px 0}.chain .step{font-size:11px;color:var(--mut);margin:1px 0 1px 4px}
.node .rid{font:650 12px ui-monospace,Menlo,monospace;margin-right:6px}.node .says{font-size:13px;line-height:1.45}
.node .pg{font-size:12px;color:var(--mut);margin-left:0}.also{font-size:12px;color:var(--mut);margin:2px 0 4px;line-height:1.45}
.cardgrid table.elems{display:table;table-layout:fixed;overflow:visible;width:100%;border-collapse:collapse;font-size:13px;margin:2px 0 6px}table.elems th{text-align:left;font-size:11px;color:var(--mut);font-weight:600;border-bottom:1px solid var(--line);padding:3px 4px}
table.elems td{vertical-align:top;padding:4px;border-bottom:1px dashed var(--line);line-height:1.4;overflow-wrap:anywhere}table.elems th:last-child,table.elems td.elsup{width:34%}
table.elems .ids{display:block;font-size:11.5px;color:var(--mut)}.el-new{color:var(--bad);font-weight:600}s.el-gone{color:var(--mut)}
.elmatrix{margin:8px 0 12px}.elmatrix>summary{font-weight:600;color:var(--fg)}.elscroll{overflow-x:auto}table.elmat{border-collapse:collapse;font-size:12.5px;margin:6px 0;width:100%}table.elmat th,table.elmat td{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}table.elmat th{font-size:11px;color:var(--mut);font-weight:600;white-space:nowrap}table.elmat td.el-same{color:var(--mut);text-align:center}table.elmat td.el-changed{color:var(--bad);font-weight:600}table.elmat td.el-removed{color:var(--mut)}table.elmat td.el-missing{color:var(--mut);text-align:center}table.elmat tr.elcount td{color:var(--mut);font-size:11.5px}
.el-from{font-weight:600}.el-from.requirements{color:var(--acc)}.el-from.internal{color:var(--ok)}.el-from.external{color:#7048e8}.el-from.intuition{color:var(--bad)}.el-how{color:var(--mut)}
.task .tl{display:flex;gap:10px;margin:2px 0}.task .tl>.mut{flex:0 0 130px}
span.link{font:600 12px ui-monospace,Menlo,monospace;color:var(--acc);background:color-mix(in srgb,var(--acc) 10%,transparent);border-radius:4px;padding:0 3px}
.cardhead{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;padding:4px;color:var(--mut);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.03em;border-bottom:1px solid var(--line)}
.task{border:1px solid var(--acc);border-radius:8px;background:var(--soft);padding:10px 14px;margin:6px 0 12px;line-height:1.55}.taskhead{font-weight:650;color:var(--acc);font-size:15px}
details.inner{margin:8px 0 0}
@media(max-width:860px){details.itemfold.cardrow>summary,.cardhead{grid-template-columns:1fr}.cardhead span+span{display:none}}
details.itemfold>summary{list-style:none;display:flex;gap:12px;align-items:center;height:46px;cursor:pointer;color:var(--fg);font-size:14px;overflow:hidden}
details.itemfold>summary::-webkit-details-marker{display:none}details.itemfold>summary::before{content:"▸";color:var(--mut);flex:0 0 10px}
details.itemfold[open]>summary::before{content:"▾"}details.itemfold>summary:hover{background:var(--soft)}
details.itemfold>summary b{flex:0 1 auto;max-width:42%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.peek{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--mut);font-size:13px}.st{flex:0 0 auto;white-space:nowrap}
table.grid{width:100%;border:1px solid var(--line);border-radius:9px;border-collapse:separate;border-spacing:0;overflow:hidden;margin:4px 0 12px}
table.grid th{background:var(--soft);padding:7px 10px;border-bottom:1px solid var(--line);border-right:1px solid var(--line)}
table.grid td{padding:7px 10px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}
table.grid th:last-child,table.grid td:last-child{border-right:0}table.grid tr:last-child td{border-bottom:0}
table.input td.key{width:170px;font-weight:600}table.input td.src{width:170px;font-size:12px;color:var(--mut)}
h3{font-size:13px;margin:18px 0 2px;font-weight:650}
.itembody{height:560px;overflow:auto;padding:2px 8px 14px 0;border-top:1px dashed var(--line)}
.itembody .pair .pic{position:sticky;top:6px;max-height:540px;overflow:auto}
table.explain{border:1px solid var(--line);border-radius:10px;border-collapse:separate;border-spacing:0;overflow:hidden;margin:6px 0 0}table.explain th{width:160px;background:var(--soft);font-size:11px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:var(--mut);padding:12px 14px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}table.explain td{padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.5}table.explain tr:last-child th,table.explain tr:last-child td{border-bottom:0}table.explain td>.mut:first-child{margin-bottom:4px}@media(max-width:720px){table.explain th{width:110px;padding:10px}}
.explain p.goal{margin:0 0 2px;font-size:14.5px;line-height:1.5}
ol.flow{list-style:none;margin:0;padding:0}ol.flow li.lv{display:flex;gap:10px;align-items:baseline}
ol.flow .rung{flex:0 0 96px;font-size:11.5px;color:var(--mut)}ol.flow .nodes{flex:1;min-width:0}ol.flow .node{display:block;margin:1px 0;line-height:1.4}
ol.flow li.down{padding-left:118px;color:var(--mut);font-size:12px;line-height:1.2}ol.flow li.me .rung{color:var(--acc);font-weight:600}
.betl{display:flex;gap:10px;margin:2px 0;line-height:1.45}.betl .k{flex:0 0 64px;font-size:12px;font-weight:600}
ul.checks{list-style:none;margin:0;padding:0}ul.checks li{margin:2px 0;padding-left:20px;text-indent:-20px;line-height:1.4}ul.checks .g{display:inline-block;width:20px;text-indent:0;font-weight:700}
@media(max-width:720px){.pair{display:block}.itembody .pair .pic{position:static;max-height:none}
main table:not(.explain){display:block;max-width:100%;overflow-x:auto}main table:not(.explain) code{white-space:nowrap;word-break:normal}.peek{display:none}
details.itemfold>summary b{max-width:none;flex:1 1 auto}}
img.shot{display:block;width:250px;max-width:100%;height:auto;margin:8px 0 4px;border:1px solid var(--line);border-radius:18px;background:#fff}
pre.src{margin:6px 0;padding:8px 10px;background:var(--soft);font:11.5px/1.4 ui-monospace,Menlo,monospace;white-space:pre-wrap;word-break:break-word;max-height:360px;overflow:auto}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:20px 18px;margin:10px 0}
details.retired{margin-top:18px}.gallery figure{margin:0}.gallery img.shot{width:100%;margin:0 0 6px}.gallery figcaption{font-size:13px;line-height:1.35}
@media(max-width:640px){body{padding:12px}td,th{padding:5px 6px}.form{grid-template-columns:1fr}.form .full{grid-column:1}}
"""


def _href(root: Path, path: Path | None, label: str) -> str:
    if path is None:
        return f"<code>{_escape(label)}</code>"
    href = _relative_href(root, path)
    if not href:
        return f"<code>{_escape(label)}</code>"
    return f'<a href="{_escape(href)}"><code>{_escape(label)}</code></a>'


def _whole_word(word: str, flags: int = 0) -> re.Pattern:
    """The word standing alone, never a piece of a hyphenated compound."""
    return re.compile(rf"(?<![\w-]){word}(?![\w-])", flags)


_CONTRACT_WORDS = ((_whole_word("candidates", re.I), "drafts"),
                   (_whole_word("candidate", re.I), "draft"),
                   (_whole_word("Tickets"), "run records"),
                   (_whole_word("Ticket"), "run record"))


def plain_words(recorded: str) -> str:
    """Read a recorded sentence in the reader's words.

    A Run's target, written when the files said `candidate`, keeps its own
    bytes; the surface says `draft` (JL 260916).
    """
    for pattern, word in _CONTRACT_WORDS:
        recorded = pattern.sub(word, recorded or "")
    return recorded


def _signal_line(insight: dict) -> str:
    if insight["status"] == "not-declared":
        return "no Insight board declared by the owning board"
    parts = []
    for board in insight["boards"]:
        label = _escape(board["title"])
        if board["live_url"]:
            label = f'<a href="{_escape(board["live_url"])}">{label}</a>'
        parts.append(f'{label} · {len(board["bindable"])} of {len(board["handoffs"])} insights currently eligible')
    line = " · ".join(parts)
    if insight["status"] == "blocked":
        line += ' · <span class=bad>no current signed and settled insight, design stays blocked</span>'
    return line


def _rule_words(run: dict, acceptance: list[str]) -> dict[str, str]:
    """criterion id -> the rule as a reader wrote it (rNN -> rule N), else the criterion in words."""
    words = {}
    for c in run["criteria"]:
        cid = str(c.get("id"))
        hit = re.match(r"^r(\d{2})[a-z]?$", cid)
        n = int(hit.group(1)) if hit else 0
        words[cid] = acceptance[n - 1] if hit and 0 < n <= len(acceptance) else _criterion_words(c)
    return words


def _checks_details(run: dict, acceptance: list[str] | None = None) -> str:
    if not run["checks"]:
        return ""
    words = _rule_words(run, acceptance or [])
    failed = any(c.get("status") != "pass" for c in run["checks"])
    rows = "".join(
        f'<tr><td>{_escape(words.get(str(c.get("criterion")), c.get("criterion")))}</td>'
        f'<td class="{"ok" if c.get("status") == "pass" else "bad"}">{_escape(c.get("status"))}</td>'
        f'<td class=mut>{_escape(c.get("evidence"))}</td></tr>'
        for c in run["checks"])
    return (f'<details{" open" if failed else ""}><summary>checks {run["checks_passed"]}/{len(run["checks"])}</summary>'
            f'<table><tr><th>rule</th><th>status</th><th>why</th></tr>{rows}</table></details>')


def _artifact_details(run: dict) -> str:
    if not run["artifacts"]:
        return ""
    art = run["artifacts"][0]
    return f'<details><summary>draft text</summary><pre class=text>{_escape(art["text"])}</pre></details>'


def _revise_of(run: dict) -> tuple[str, str]:
    """(base run, feedback text) when a Generate revises an earlier draft."""
    base = next((i for i in run["inputs"] if i["role"] == "base"), None)
    note = next((i for i in run["inputs"] if i["role"] == "feedback"), None)
    text = _read(note["file"]).split("\n\n", 2)[-1].strip() if note and note["file"].is_file() else ""
    return (base["run_id"] if base else "", text)


def run_short(run_id: str) -> str:
    """A run said briefly: `rd13` for an old name, `verify 09-18` for a current one."""
    hit = re.match(r"^run-design-([a-z]+)-(\d{2})(\d{2})-", str(run_id))
    return f"{hit.group(1)} {hit.group(2)}-{hit.group(3)}" if hit else str(run_id).split("_")[0]


def _run_rows(root: Path, runs: list[dict], acceptance: list[str] | None = None) -> str:
    rows = []
    for run in runs:
        status = run["status"]
        status_cls = ("bad" if status in ("failed", "blocked") or (run["kind"] == "verify" and run["verdict"] == "fail")
                      else "mut" if status == "superseded" else ("ok" if status == "complete" else ""))
        status_text = "planned · queued for agent" if status == "planned" and run["mode"] == "agent" else status
        # Explain historical outcomes without changing the recorded Run identity.
        outcome = {"adopt": "ready", "decline": "not delivered"}.get(run["outcome"], run["outcome"])
        if run["kind"] in ("generate", "verify") and run["checks"]:
            outcome = f'{run["verdict"] or status} {run["checks_passed"]}/{len(run["checks"])}'
        next_step = {"adopt": "delivery"}.get(run["route"], run["route"] or "")
        if run["status"] == "complete" and run["kind"] == "adopt" and run["outcome"] in ("adopt", "decline"):
            next_step = "closed"
        detail = _checks_details(run, acceptance) + _artifact_details(run)
        base, why = _revise_of(run) if run["kind"] == "generate" else ("", "")
        if why:
            detail = f'<div class=mut>feedback: “{_escape(why)}”</div>' + detail
        if run["failure"]:
            detail = f'<div class={"mut" if status == "superseded" else "bad"}>{_escape(run["failure"])}</div>' + detail
        if run["words"] and run["kind"] != "adopt":
            detail = f'<div class=mut>“{_escape(run["words"])}”</div>' + detail
        rows.append(
            f'<tr><td>{_href(root, run["ticket_path"], run["id"])}</td>'
            f'<td>{_escape(run["step"])}{(" · revise of " + _escape(run_short(base))) if base else ""}'
            f'<div class=mut><code>Design.{_escape(run["kind"])}</code> · {_escape(plain_words(run["target"]))}</div></td>'
            f'<td>{_escape(run["actor"])} <span class=mut>{_escape(run["mode"])}</span></td>'
            f'<td class=mut>{_escape(run["finished"] or run["started"] or "—")}</td>'
            f'<td class="{status_cls}">{_escape(status_text)}</td><td class="{"bad" if run["verdict"] == "fail" else ""}">{_escape(outcome)}</td>'
            f'<td class=mut>{_escape(next_step)}</td></tr>'
            + (f'<tr><td></td><td colspan=6>{detail}</td></tr>' if detail else ""))
    return "".join(rows)


def _held_at(item: dict) -> str:
    """For an item on hold: the Commission that held it, else ``""``."""
    if item["state"] != "commission held":
        return ""
    last = next((r for r in reversed(item["runs"]) if r["kind"] == "commission"
                 and r["status"] != "superseded"), None)
    return last["kind"] if last and last["outcome"] == "hold" else ""


def _stale_names(item: dict) -> list[str]:
    return [name for r in item["runs"] for name in r.get("stale") or []]


# Design-only presentation of the owner contract; these are types, not allocated Runs.
_DESIGN_RUN_GUIDE = {
    "commission": {
        "name": "Commission", "type": "Design.commission", "actor": "person",
        "purpose": "Release or hold one item's exact goal, rules and source inputs.",
        "worker": "none · the named person decides",
        "requires": "A registered item, explicit goal and rules, allowed sources, and a named person. At most one release per item.",
    },
    "generate": {
        "name": "Generate", "type": "Design.generate", "actor": "agent",
        "purpose": "Create or revise the commissioned design and check it against every released rule.",
        "worker": "haipipe-design-unit · through haipipe-designer-agent",
        "requires": "A released Commission, frozen config and inputs not edited since the run record was written. A revision also needs its exact base and feedback; no second open Run for the item.",
    },
    "verify": {
        "name": "Verify", "type": "Design.verify", "actor": "independent agent",
        "purpose": "Review the exact completed draft against every released rule and record pass, fail or unresolved gaps.",
        "worker": "haipipe-design-unit · through a fresh haipipe-designer-agent context",
        "requires": "A complete Generate Result, pinned sources and criteria, and a reviewer independent of its producer. An already completed valid review cannot be repeated unchanged.",
    },
}


# The Runs panel beside each Space (JL 261001): like the Paper and Page workbenches,
# work is started from a run type and its prompt, copied into a Claude or Codex
# session, never from a form on the page. The run types are the Design run cards,
# the Workbench Table written as cards (one per button: agent, skill, signs, prompt).
_RUN_CARDS = SKILLS / "design" / "haipipe-design-workflow" / "references" / "run-cards.md"
_CARD_SPACE = {"Tasks": "tasks", "Theory": "theory", "Goal": "goal", "Design": "design", "Delivery": "delivery"}


def design_run_types(path: Path = _RUN_CARDS) -> dict[str, list[dict]]:
    """The Design run cards -> {space: [{label, pattern, agent, skills, signs, prompt}]}, in card order."""
    out: dict[str, list[dict]] = {}
    card = None
    for line in _read(path).splitlines() if path.is_file() else []:
        m = re.match(r"^🔘 BUTTON\s+(.+?)\s+·\s+(\w+)\s+·\s+(\S.*?)(?:\s+·\s+views\s+.*)?$", line)
        if m:
            card = {"label": m.group(1), "pattern": m.group(3).strip(), "agent": "", "skills": [],
                    "signs": "", "prompt": ""}
            out.setdefault(_CARD_SPACE.get(m.group(2), m.group(2).lower()), []).append(card)
            continue
        if card is None:
            continue
        for mark, key in (("🤖 AGENT", "agent"), ("🧩 SKILL", "skills"), ("✍️ SIGNS", "signs"), ("💬 PROMPT", "prompt")):
            if line.startswith(mark):
                value = line[len(mark):].strip()
                card[key] = [value] if key == "skills" else value
    for cards in out.values():
        for card in cards:
            # the panel names the skill on every run; the prompt names the agent that runs it
            if card["agent"] and card["agent"] != "none":
                card["prompt"] = f'Run with {card["agent"]}. {card["prompt"]}'
            if card["signs"] and card["signs"] != "none":
                card["prompt"] += f' I sign {card["signs"]}.'
    return out


_PANEL_STATUS = {"complete": "done", "running": "running", "planned": "open", "failed": "held", "blocked": "held"}


def design_runs_panel(space: str, runs: list[dict], *, root: Path, page: str, board: str,
                      whole: str) -> str:
    """The Runs panel for one Space: its run types, each run's prompt, process and result."""
    import re as _re
    from live.runs_panel import panel_markup
    kinds = design_run_types().get(space, [])
    buckets = [[] for _ in kinds]
    for run in sorted(runs, key=lambda r: (r.get("finished") or r.get("started") or "", r["id"]), reverse=True):
        if space == "delivery" and run["outcome"] != "pass":
            continue
        hit = next((i for i, k in enumerate(kinds) if k["pattern"] != "-" and _re.search(k["pattern"], run["id"])), None)
        if hit is None:
            continue
        name = design_number(run["item"]) if run["item"] else run["id"]
        buckets[hit].append({
            "run_id": run["id"], "global_id": run["id"], "status": _PANEL_STATUS.get(run["status"], run["status"]),
            "target": " · ".join(x for x in (run.get("folder"), run["item"]) if x) or "the folder",
            "ticket": str(run["ticket_path"]), "runtime": str(run["result_dir"] / "runtime.yaml"),
            "result_path": str(run["result_dir"]), "_views": "", "_keys": run["item"],
            "_display": f'{name} · {kinds[hit]["label"]}',
            "goal": " · ".join(x for x in (run["actor"], run["outcome"], run.get("finished") or "") if x),
        })
    return panel_markup(space, kinds, buckets, base=Path(root), fill=lambda row: {"page": page, "board": board},
                        whole=whole)


def runs_panel_assets() -> tuple[str, str]:
    """The shared panel's CSS (plus this workbench's side-by-side layout) and its script."""
    from live.runs_panel import PANEL_CSS, PANEL_JS
    css = PANEL_CSS + """
:root{--card:var(--bg)}
body{max-width:1560px}
.pane.on.split{display:flex;align-items:flex-start;gap:16px}
.split>.space-main{flex:1 1 auto;min-width:0}
.split>.runs-panel{flex:0 0 clamp(260px,28vw,440px);margin:0;position:sticky;top:8px;
 max-height:calc(100vh - 16px);display:flex;flex-direction:column;overflow:hidden}
.split>.runs-panel .runs-bar{flex-wrap:wrap}
.split>.runs-panel .runs-body{overflow:auto;min-height:0;grid-template-columns:1fr}
.split>.runs-panel .runs-types{flex-direction:row;flex-wrap:wrap}
.split>.runs-panel .run-type{gap:8px}
.split>.runs-panel.folded{flex-basis:42px}
.split>.runs-panel.folded .runs-bar{writing-mode:vertical-rl;flex-wrap:nowrap;padding:10px 9px;gap:10px}
@media(max-width:900px){.pane.on.split{display:block}.split>.runs-panel{position:static;max-height:none;margin-top:14px}
 .split>.runs-panel.folded .runs-bar{writing-mode:horizontal-tb}}
"""
    return css, "<script>" + PANEL_JS + "</script>"


def _next_design_run(item: dict) -> tuple[str, str]:
    """Return the native action and Run kind its state exposes; never allocate."""
    if _held_at(item) == "commission":
        return "commission-release", "commission"
    for action, kind in (("commission-release", "commission"), ("queue-generate", "generate"),
                         ("queue-revise", "generate"), ("queue-verify", "verify")):
        if item["state"] in _ALLOWED[action]:
            return action, kind
    if item["state"] in _ALLOWED["requeue"]:
        stale = next((r for r in reversed(item["runs"])
                      if r["status"] == "planned" and r.get("stale")), None)
        if stale and stale["kind"] in ("generate", "verify"):
            return "requeue", stale["kind"]
    return "", ""


def design_chat_action(item: dict) -> tuple[str, str]:
    queued_kind = {"generate queued": "generate", "verify queued": "verify"}.get(item["state"])
    return ("dispatch-existing", queued_kind) if queued_kind else _next_design_run(item)


def design_chat_prompt(snapshot: dict, item: dict) -> str:
    """A bounded chat request for safe worker work; constructing it only reads the snapshot."""
    if (not snapshot.get("current") or not snapshot.get("yaml") or snapshot.get("static")
            or snapshot.get("audit") or snapshot["insight"]["status"] in ("blocked", "missing")):
        return ""
    action, kind = design_chat_action(item)
    if action not in ("queue-generate", "queue-verify", "dispatch-existing"):
        return ""
    opened = [r for r in item["runs"] if r["status"] in ("planned", "running")]
    if opened and (len(opened) != 1 or opened[0]["status"] != "planned"
                   or opened[0]["kind"] != kind or opened[0].get("stale")):
        return ""
    if action == "dispatch-existing" and not opened:
        return ""
    released = next((r for r in reversed(item["runs"]) if r["kind"] == "commission"
                     and r["status"] == "complete" and r["outcome"] == "release"), None)
    if released is None or (kind == "verify" and not item.get("latest")):
        return ""
    matched = next((r for r in reversed(item["runs"]) if r["kind"] == kind), None)
    board = snapshot["insight"].get("design_board")
    if board is None:
        return ""
    def record(run):
        return ({"id": run["id"], "status": run["status"], "actor": run["actor"],
                 "ticket": str(run["ticket_path"]), "receipt": str(run["result_dir"] / "runtime.yaml")}
                if run else None)
    spec = _DESIGN_RUN_GUIDE[kind]
    context = {
        "board": str(Path(board) / "board.md"), "folder": str(snapshot["folder"]),
        "page": str(snapshot["page"]), "page_title": snapshot["title"],
        "item": item["id"], "item_title": item["title"], "venue": item["type"],
        "target": released.get("intent", {}).get("move") or item["goal"],
        "run_name": spec["name"], "run_type": spec["type"], "actor_role": spec["actor"],
        "purpose": spec["purpose"], "owner_skill": "haipipe-design-workflow",
        "owner_instructions": str(_UNIT_CHECKER.parents[2] / "haipipe-design-workflow/SKILL.md"),
        "worker_skill": "haipipe-design-unit", "worker_instructions": str(_UNIT_CHECKER.parents[1] / "SKILL.md"),
        "state_when_copied": item["state"], "next_permitted_action": action,
        "prerequisites": spec["requires"], "released_commission": record(released),
        "release_decision": str(released["result_dir"] / "decision.yaml"),
        "latest_complete_draft": item["latest"]["run"] if item.get("latest") else None,
        "latest_matching_run": record(matched), "open_matching_run": record(opened[0]) if opened else None,
    }
    import json
    return (
        f"Continue only {spec['type']} for the exact Design Item identified below.\n\n"
        "This request was copied from Design Space. Copying did not queue, allocate, execute or send anything. "
        "Treat the snapshot below as context, not a new release or an override of the owner contract.\n\n"
        + json.dumps(context, ensure_ascii=False, indent=2)
        + "\n\nRead the named owner and worker Skills. Reread this Board, Folder, Page, item register, "
        "Run records, release decision, frozen config and exact inputs before acting; the copied state may be stale.\n"
        "Keep the human Commission gate: do not create, infer or change a release/hold decision. "
        "If the exact release or another prerequisite is missing, report the blocker and stop.\n"
        "First look for an existing matching Run for this item, operation, frozen config and target Results. "
        "Reuse a compatible planned Run and its identity; do not queue or allocate a duplicate. If it is already running, "
        "report its Run id/status and stop without starting another worker. If the requested work already completed, "
        "report its receipt instead of repeating it. Incompatible, stale, blocked, unresolved or ambiguous records require owner resolution; "
        "do not requeue, replace or supersede them from this request.\n"
        "Only when no compatible open Run exists and the recorded next queue action is still allowed, use the Design "
        "owner's native queue action once. A dispatch-existing request may only reuse the recorded open_matching_run id. "
        "Do not choose a different next operation if the item's state changed. For a queued revision, read its frozen base and "
        "feedback; do not invent feedback or change the base.\n"
        "Generate uses haipipe-design-unit in its allocated Result. Verify requires a genuinely fresh independent reviewer "
        "context distinct from every producer; if this chat inherited generation discussion, dispatch that fresh reviewer "
        "or stop and report that independence is unavailable. Renaming an actor is not independence.\n"
        "The worker writes only its paired Result, excluding runtime.yaml. The caller validates the Result and closes its "
        "runtime receipt through the owner workflow. Preserve old Results and stop after this one requested Run; "
        "do not auto-advance to another Run or write Delivery. Report the actual Run id, Ticket path, Result path, "
        "runtime receipt path, status, verdict/route and any remaining prerequisite or blocker."
    )


def design_chat_copy(prompt: str) -> str:
    if not prompt:
        return ""
    return ('<div><p><b>Chat option · Copy request → paste and send</b></p>'
            f'<button type=button data-design-prompt="{_escape(prompt)}">Copy prompt to chat</button> '
            '<span class=mut role=status data-design-copy-status>Copy only; nothing starts until you paste and send.</span>'
            f'<details><summary>Review chat prompt</summary><pre class=text>{_escape(prompt)}</pre></details></div>')


def design_chat_copy_script() -> str:
    """Reuse the existing clipboard helper unchanged; no action endpoint is involved."""
    helper = _read(HOST / "assets" / "js" / "05-prompt-copy.js")
    return ('<script>' + helper + '\n'
            "document.querySelectorAll('button[data-design-prompt]').forEach(function(b){"
            "b.onclick=async function(){var st=b.parentNode.querySelector('[data-design-copy-status]');"
            "if(!window.__boardCopyPrompt){st.textContent='Copy unavailable; select the reviewed prompt manually.';return}"
            "var ok=await window.__boardCopyPrompt(b,b.dataset.designPrompt);"
            "st.textContent=ok?'Copied. Paste and send in chat; nothing has started here.':'Copy failed; select the reviewed prompt manually.'"
            "}});</script>")


_RUNNING_STATES = ("generate queued", "generating", "verify queued", "verifying")


def design_next_run(item: dict, human: str, *, writable: bool = False, compact: bool = False) -> str:
    """Explain this item's next native action, separately from its actual history.

    An item with nothing to start says nothing here (JL 260921): its own line
    already carries the state, and its Runs are in the card's Runs fold.
    """
    action, kind = _next_design_run(item)
    if not action and item["state"] not in _RUNNING_STATES:
        return ""
    latest = next((r for r in reversed(item["runs"]) if r["status"] != "superseded"), None)
    lead = "Next eligible Run" if action else "Current Run"
    if not kind:
        kind = latest["kind"] if latest else ""
    spec = _DESIGN_RUN_GUIDE.get(kind)
    capability = "You can start it from this card" if action and writable else "Read only on this page"
    heading = (f'{lead}: {spec["name"]} · {spec["actor"]}' if spec and (action or lead == "Current Run") else lead)
    matches = [r for r in item["runs"] if r["kind"] == kind]
    match = matches[-1] if matches else None
    current = (f'{match["id"]} · {match["status"]} · {match["outcome"] or "no outcome yet"} · {match["actor"]}'
               if match else "none allocated for this type")
    if action:
        instruction = {
            "commission-release": "You record Release or Hold with the native controls; a held decision stays on record.",
            "queue-generate": "The person queues Generate; the dispatcher assigns the agent before it works.",
            "queue-revise": "Supply feedback and queue a new Generate Run; keep the previous draft unchanged.",
            "queue-verify": "The person queues Verify; the dispatcher assigns a fresh independent reviewer.",
            "requeue": "Queue again replaces the stale queued Run and keeps its superseded record.",
        }[action]
        if not writable:
            instruction += " Open this item's Design Space for its native control."
    else:
        instruction = item.get("waiting") or "The agent is working; nothing to start here."
    facts = (f'<p><b>{_escape(heading)}</b><br>{_escape(capability)}</p>'
             f'<p>{_escape(instruction)}</p>')
    # Everything a reader needs to start is above; the type, the Skills and the
    # exact run ids sit behind one fold, so a card is not a wall of records.
    detail = f'<div class=mut>{_escape(spec["purpose"])}</div>' if spec else ""
    if spec:
        detail += (f'<p>Run Type: <code>{_escape(spec["type"])}</code><br>'
                   f'Target: {_escape(item["id"])} · {_escape(item["title"])}</p>'
                   '<p>Owner Skill: <code>haipipe-design-workflow</code><br>'
                   f'Worker Skill: {_escape(spec["worker"])}</p>'
                   f'<p>Prerequisites: {_escape(spec["requires"])}</p>'
                   '<p>The native control checks these prerequisites again before writing.</p>')
    released = next((r for r in reversed(item["runs"])
                     if r["kind"] == "commission" and r["outcome"] == "release"), None)
    if spec and kind in ("generate", "verify"):
        detail += f'<div class=mut>Released Commission: {_escape(released["id"] if released else "none recorded")}</div>'
        if item.get("latest"):
            detail += f'<div class=mut>Latest complete draft: {_escape(item["latest"]["run"])}</div>'
    detail += f'<div class=mut>Latest matching record: {_escape(current)}</div>'
    facts += f'<details><summary>Run type, Skills and prerequisites</summary>{detail}</details>'
    return f'<details><summary>{_escape(heading)}</summary>{facts}</details>' if compact else facts


def _actions(item: dict, human: str) -> tuple[str, str]:
    """The buttons an item's state licenses, and the line that folds them.

    A form that asks for a name, words, or feedback is folded under its line
    (closed by default); a single agent-queue button has no line and stays in view.
    """
    state = item["state"]
    person = f'<input class=name name=actor placeholder="your name" value="{_escape(human if human != "person" else "")}">'
    words = '<input class=words name=words placeholder="your words, one sentence (kept on record)">'
    feedback = '<input class=words name=feedback placeholder="what to change (feedback for the revise Run)">'
    held_at = _held_at(item)
    if state in ("not commissioned", "commission open") or held_at == "commission":
        return (f'{person}{words}<button class=do data-action=commission-release>Release commission</button>'
                f'<button class="do bad" data-action=commission-hold>Hold</button>'), "Release or hold the commission"
    if state in ("commissioned", "revise requested"):
        return '<button class=do data-action=queue-generate>Queue Generate · agent</button>', ""
    if state in ("generated", "verify invalid"):
        return '<button class=do data-action=queue-verify>Queue Verify · independent agent</button>', ""
    if state == "queued run out of date":
        return ('<button class=do data-action=requeue>Queue again with today\'s insight files</button>'
                f'<div class=mut>changed since it was queued: {_escape(", ".join(_stale_names(item)))}</div>'), ""
    if state in ("generate failed", "verify failed"):
        return f'{feedback}<button class=do data-action=queue-revise>Queue revise · agent</button>', "Queue a revise, with feedback"
    if state == "ready":
        return '<span class="ok">ready for Delivery</span>', ""
    if state == "blocked":
        return (f'<span class=bad>{_escape(item["waiting"])}</span>'
                '<span class=mut>Repair the named inputs or records through the Design workflow; '
                'the caller must resolve the blocked Run before work resumes.</span>'), ""
    if state == "records invalid":
        return (f'<span class=bad>{_escape(item["waiting"])}</span>'
                '<span class=mut>Inspect the records check before handing off this design. '
                'Preserve the recorded versions; changed content needs a new Run.</span>'), ""
    if state == "legacy hold":
        return '<span class=mut>Historical decision; register a new Design Item to continue.</span>', ""
    if state in ("generate queued", "verify queued", "generating", "verifying"):
        return '<span class=mut>queued for the agent</span>', ""
    return "", ""


def _page_name(root: Path, row: dict) -> str:
    """An evidence page as a reader names it: its label and title, linked to the Insight view."""
    lab = insight_label(row["file"])
    hit = _H1.search(_read(row["file"]))
    title = hit.group(1).strip() if hit else lab["words"]
    href = _insight_href(root, row["file"]) if lab["id"] else ""
    text = (f"<b>{_escape(lab['shown'])}</b> " if lab["id"] else "") + _escape(title)
    return f'<a href="{_escape(href)}">{text}</a>' if href else _href(root, row["file"], title)


def _insight_href(root: Path | None, page: Path) -> str:
    """The Insight workbench's view of one page, when this server can serve it; '' when the
    page lies outside the server root (the label then shows without a link, audit N1)."""
    board = page.parent.parent.parent
    if root is None or not (board / "board.md").is_file():
        return ""
    try:
        rel_board = board.resolve().relative_to(Path(root).resolve()).as_posix()
        rel_page = page.resolve().relative_to(board.resolve()).as_posix()
    except (OSError, ValueError, RuntimeError):
        return ""
    return ("/_board/insight?path=" + quote("/" + ("" if rel_board == "." else rel_board + "/") + "board.md", safe="")
            + "&file=" + quote(rel_page, safe=""))


_RUNG = re.compile(r"^([A-Z])([DIKW])(\d{2})\b")
_RUNG_WORD = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_H1 = re.compile(r"(?m)^#\s+(.+?)\s*$")


def _insight_flow(item: dict, root: Path | None = None) -> str:
    """The insights an item rests on, as a flow: Data → Information → Knowledge → Wisdom → this design.

    Each node is one page, named by its own title (the page's finding in a line),
    linked to the Insight workbench's view of that page (JL 260918: a flow, not a list of ids).
    """
    levels: dict[str, list[str]] = {}
    for r in item["evidence_rows"]:
        stem = Path(r["name"]).stem
        hit = _RUNG.match(stem)
        rung = hit.group(2) if hit else "?"
        page_id = stem.split("-")[0]
        title = ""
        if r["exists"]:
            m = _H1.search(_read(r["file"]))
            title = m.group(1).strip() if m else ""
        # an insight page is named by its id and its title; any other source by its title alone
        shown = insight_label(r["file"])["shown"] if r["exists"] and hit else ""
        label = f"<b>{_escape(shown or page_id)}</b>" if hit else ""   # full-D02 on screen, FD02 in the file
        href = _insight_href(root, r["file"]) if r["exists"] and hit else ""
        if href:
            label = f'<a href="{_escape(href)}">{label}</a>'
        mark = (' <span class=ok>✅ signed</span>' if r["signed"].startswith("signed")
                else ' <span class=bad>⬜ unsigned</span>' if r["signed"] else "")
        missing = "" if r["exists"] else ' <span class=bad>missing</span>'
        if r["role"] == "avoid":
            mark += ' <span class=bad>· avoid</span>'
        levels.setdefault(rung, []).append(
            f'<span class=node>{label + " " if label else ""}{_escape(title) or _escape(stem)}{mark}{missing}</span>')
    if not levels:
        return ('<div class=mut>from the design task only · no insight needed</div>' if item["basis"] != "evidence-informed"
                else '<div class=bad>needs an insight · none named yet</div>')
    rows = [(_RUNG_WORD.get(k, "Also read"), levels[k]) for k in ("D", "I", "K", "W", "?") if k in levels]
    rows.append(("This design", [f'<span class=node><b>{_escape(item["id"])}</b> {_escape(item["title"])}</span>']))
    out = []
    for i, (word, nodes) in enumerate(rows):
        if i:
            out.append('<li class=down>↓</li>')
        me = " me" if word == "This design" else ""
        out.append(f'<li class="lv{me}"><span class=rung>{word}</span><span class=nodes>{"".join(nodes)}</span></li>')
    return f'<ol class=flow>{"".join(out)}</ol>'


def _rule_checks(item: dict) -> tuple[str, str]:
    """Each acceptance rule with the mark the review of the SHOWN draft gave it.

    The review is the Verify whose target is the draft on the card, else that
    draft's own self-check, else nothing (audit N2).  Rule N is criterion rNN,
    plus rNNb, rNNc when the rule quoted several phrases; a hand-written config
    with its own criterion names is matched by order when the counts agree."""
    shown = shown_design(item)
    source, word = None, ""
    if shown:
        for r in reversed(item["runs"]):
            if (r["kind"] == "verify" and r["status"] == "complete" and r["checks"]
                    and any(str(t.get("path", "")).startswith(f'results/{shown["run"]}/') for t in r["targets"])):
                source, word = r, "independent review"
                break
        if source is None:
            own = next((r for r in item["runs"] if r["id"] == shown["run"] and r["checks"]), None)
            source, word = (own, "self-check") if own else (None, "")
    checks = source["checks"] if source else []
    by_id: dict[str, list[str]] = {}
    for c in checks:
        hit = re.match(r"^(r\d{2})[a-z]?$", str(c.get("criterion")))
        if hit:
            by_id.setdefault(hit.group(1), []).append(str(c.get("status")))
    if checks and not by_id and source["criteria"]:
        # a hand-written config names its own criteria (length, optout): show those, by name
        status = {str(c.get("criterion")): str(c.get("status")) for c in checks}
        lines = [(_criterion_words(c), [status.get(str(c.get("id")), "")]) for c in source["criteria"]]
    else:
        lines = [(rule, by_id.get(f"r{i:02d}", [])) for i, rule in enumerate(item["acceptance"], start=1)]
    rows, passed = [], 0
    for rule, marks in lines:
        s_ = ("fail" if "fail" in marks else "pass" if marks and all(m == "pass" for m in marks)
              else "unresolved" if any(marks) else "")
        passed += s_ == "pass"
        glyph = ('<span class="g ok">✓</span>' if s_ == "pass" else '<span class="g bad">✗</span>' if s_ == "fail"
                 else '<span class="g mut">·</span>')
        rows.append(f"<li>{glyph}{_escape(rule)}</li>")
    head = (f'{passed} of {len(lines)} pass <span class=mut>· {word} '
            f'{_escape(run_short(source["id"]))}</span>') if source else '<span class=mut>not checked yet</span>'
    released = next((r for r in item["runs"] if r["kind"] == "commission" and r["outcome"] == "release"), None)
    if released and _bet_changed(item, released):
        head += (f' <span class=bad>· the register changed after release ({_escape(run_short(released["id"]))}); '
                 'drafts still follow the released goal and rules</span>')
    return head, "".join(rows) or "<li class=mut>none</li>"


_CRITERION_WORDS = {"max_chars": "≤ {v} characters", "contains": "contains '{v}'", "excludes": "does not contain '{v}'",
                    "starts_with": "starts with '{v}'", "ends_with": "ends with '{v}'"}


def _criterion_words(c: dict) -> str:
    """One compiled criterion as a reader says it."""
    form = _CRITERION_WORDS.get(str(c.get("kind")))
    return form.format(v=c.get("value")) if form else str(c.get("description") or c.get("id") or "")


def _bet_changed(item: dict, released: dict) -> bool:
    """Whether the register's goal, bet or rules differ from what the Commission froze."""
    intent = released["intent"] or {}
    frozen_rules = released.get("acceptance")
    return bool(
        (intent.get("move") and intent["move"] not in (item["goal"], item["title"]))
        or (intent.get("move") and (intent.get("expected_effect") or "") != (item["expected"] or "")
            and released["design_mode"] != "brainstorm")
        or (frozen_rules is not None and list(frozen_rules) != list(item["acceptance"])))


# ------------------------------------------------------------ evidence chain --
# The Rationale column says why a design is what it is (JL 261001), in two folds: the
# evidence chain, from the insight rows the design acts on down to the data, and each
# element of the design with what supports it. Every line is a row quoted from an insight
# page by its id, and every link between rows is one the insight pages already record.

_LINEAGE = re.compile(r"^(?:([DIKW]\d+(?:\.\.[DIKW]\d+)?)|\s+)\s*←\s+(.+?)\s*$")
_REF_TOKEN = re.compile(r"(?<![\w-])(?:([DIKW]\d{2}-[a-z]+)(?![a-z0-9])|([DIKW]\d+(?:\.\.[DIKW]?\d+)?)(?![\w-]))")
_PAGE_STEM_ID = re.compile(r"^([DIKW]\d{2}-[a-z]+|[A-Z][DIKW]\d{2})-")
_STEP_WORD = {"K": "because", "I": "shown by", "D": "counted from"}


def _page_id(page: Path) -> str:
    """`W01-full-send-salience.md` -> `W01-full`; the older `FW01-send-salience.md` -> `FW01`."""
    hit = _PAGE_STEM_ID.match(page.stem)
    return hit.group(1) if hit else page.stem


def _level(pid: str) -> str:
    return pid[0] if re.match(r"^[DIKW]\d", pid) else pid[1:2]


def _expand(token: str) -> list[str]:
    """`I4..I12` -> I4 … I12; any other token as it is."""
    hit = re.match(r"^([DIKW])(\d+)\.\.[DIKW]?(\d+)$", token)
    if not hit or not 0 <= int(hit.group(3)) - int(hit.group(2)) <= 60:
        return [token]
    return [f"{hit.group(1)}{n}" for n in range(int(hit.group(2)), int(hit.group(3)) + 1)]


def _row_lineage(text: str) -> dict[str, list[tuple[str, list[str]]]]:
    """`K1  ←  I02-full · I1, I2, I13-full   note` lines: row id -> [(page id, [row ids])].
    A line that starts with `←` goes on with the row above; a whole page cited has no rows."""
    out: dict[str, list[tuple[str, list[str]]]] = {}
    ids: list[str] = []
    for line in text.splitlines():
        hit = _LINEAGE.match(line)
        if not hit:
            ids = []
            continue
        if hit.group(1):
            ids = _expand(hit.group(1))
        found, cur = [], None
        for page, row in _REF_TOKEN.findall(re.split(r"\s{2,}", hit.group(2))[0]):
            if page:
                cur = (page, [])
                found.append(cur)
            elif cur is not None:
                cur[1].extend(_expand(row))
        for rid in ids:
            out.setdefault(rid, []).extend(found)
    return out


def _row_texts(text: str) -> dict[str, str]:
    """Row id -> its words on the page. A row of a fenced grid, its wrapped lines joined; a
    table row (one line, numbers in its cells) is read with its column names; else a
    paragraph that opens with the id in bold (`**D8, the cell grid.**`)."""
    rows: dict[str, str] = {}
    for block in re.findall(r"(?ms)^```\w*\n(.*?)^```", text):
        header, last, col, raw = [], None, 0, {}
        for line in block.splitlines():
            if re.match(r"^id\s{2,}", line):
                header = re.split(r"\s{2,}", line.strip())[1:]
                continue
            hit = re.match(r"^([DIKW]\d+)\s{2,}(.+?)\s*$", line)
            if hit and "←" not in line:
                last = None
                if hit.group(1) in rows or hit.group(1) in raw:
                    continue
                raw[hit.group(1)] = {"cells": re.split(r"\s{2,}", hit.group(2)), "more": [], "header": header}
                last, col = hit.group(1), hit.start(2)
            elif last and "←" not in line and line.strip() and not line[:col].strip() and line[col:col + 1].strip():
                raw[last]["more"].append(re.split(r"\s{2,}", line[col:].strip())[0])
            else:
                last = None
        for rid, r in raw.items():
            cells, head = r["cells"], r["header"]
            numbers = all(re.search(r"\d|^[—✅❌🟡🚫⬜]$", c) for c in cells[1:])
            if not r["more"] and len(cells) >= 3 and len(head) == len(cells) and numbers:
                pairs = [f"{h} {c}" for h, c in zip(head[1:], cells[1:])
                         if h.lower() not in ("file", "from", "source", "run")]
                rows[rid] = " · ".join([cells[0], *pairs])
            else:
                rows[rid] = " ".join([cells[0], *r["more"]])
    for hit in re.finditer(r"\*\*`?([DIKW]\d+)`?([^*\n]*)\*\*", text):
        rows.setdefault(hit.group(1), (hit.group(1) + hit.group(2)).strip())
    return rows


def _compact(rows: list[str]) -> str:
    """[I2, I3, I4, I7] -> `I2..I4, I7`: a run of rows said as a range, as the pages write it."""
    out, i = [], 0
    while i < len(rows):
        j = i
        while (j + 1 < len(rows) and re.match(r"^[DIKW]\d+$", rows[j]) and rows[j + 1][:1] == rows[j][:1]
               and rows[j + 1][1:].isdigit() and int(rows[j + 1][1:]) == int(rows[j][1:]) + 1):
            j += 1
        out.append(f"{rows[i]}..{rows[j]}" if j - i >= 2 else ", ".join(rows[i:j + 1]))
        i = j + 1
    return ", ".join(out)


def _board_page(board: Path | None, pid: str) -> Path | None:
    hits = sorted(board.glob(f"*/{pid}-*/{pid}-*.md")) if board else []
    return hits[0] if hits else None


def _cited_page(item: dict, pid: str) -> Path | None:
    """An insight page by its id: among the item's evidence first, then on the same board."""
    files = [r["file"] for r in item.get("evidence_rows", []) if r["exists"]]
    page = next((f for f in files if f.stem.startswith(pid + "-")), None)
    for f in files if page is None else ():
        page = _board_page(_nearest_board(f), pid)
        if page:
            break
    return page


def because_rows(item: dict, missing: list[str] | None = None) -> list[dict]:
    """Every insight row the `because:` line names, in order (`W01-full · W1, W3`; pages
    split by `;`): {page, pid, id, do, text}, `do` None for a row that is not counsel.
    A named row not found on its page is left out and, given `missing`, listed there."""
    from live.design_actions import counsel_lines
    out = []
    for part in (item.get("because") or "").split(";"):
        part = part.strip()
        if not part or part.lower() in ("none", "no insight", "-"):
            continue
        hit = _BECAUSE.match(part)
        page = _cited_page(item, hit.group(1)) if hit else None
        if page is None:
            missing is not None and missing.append(part)
            continue
        text = _read(page)
        counsel, rows = {c["id"]: c for c in counsel_lines(text)}, _row_texts(text)
        for rid in re.split(r"\s*,\s*", hit.group(2)):
            c = counsel.get(rid)
            words = (("DO " if c["do"] else "DO NOT ") + c["text"]) if c else rows.get(rid, "")
            if words:
                out.append({"page": page, "pid": hit.group(1), "id": rid, "do": c["do"] if c else None, "text": words})
            elif missing is not None:
                missing.append(f"{hit.group(1)} · {rid}")
    return out


def _chain_heads(item: dict) -> tuple[list[dict], bool]:
    """The rows a chain starts from: the `because:` rows, else the DO rows of the cited
    Wisdom pages (False: the register names no rows)."""
    named = because_rows(item)
    if named or (item.get("because") or "").strip():
        return named, True
    from live.design_actions import counsel_lines
    heads = []
    for r in item.get("evidence_rows", []):
        if r["role"] == "handoff" and r["exists"]:
            heads += [{"page": r["file"], "pid": _page_id(r["file"]), "id": c["id"], "do": True,
                       "text": "DO " + c["text"]} for c in counsel_lines(_read(r["file"])) if c["do"]]
    return heads, False


def _walk(page: Path, rid: str, limit: int = 5) -> list[dict]:
    """One row and its first-cited parents down to the data, the way the insight board walks
    a cell: [{page, pid, id, text, also}], `also` the other parents of each row as
    (page id, page file or None, its rows)."""
    board, out, seen = _nearest_board(page), [], set()
    while page is not None and len(out) < limit and (page, rid) not in seen:
        seen.add((page, rid))
        text = _read(page)
        node = {"page": page, "pid": _page_id(page), "id": rid, "also": [],
                "text": _row_texts(text).get(rid, "") if rid else ""}
        out.append(node)
        nxt = None
        for ref, rows in (_row_lineage(text).get(rid, []) if rid else []):
            target = _board_page(board, ref)
            if nxt is None and target is not None:
                nxt = (target, rows[0] if rows else "")
                node["also"] += [(ref, target, _compact(rows[1:]))] if rows[1:] else []
            else:
                node["also"].append((ref, target, _compact(rows)))
        if nxt is None:
            break
        page, rid = nxt
    return out


def _code(escaped: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def _page_link(root: Path | None, page: Path) -> str:
    name = _escape(_page_words({"name": page.name}))
    href = _insight_href(root, page)
    signed = _SIGNED.search(_read(page))
    mark = " · signed" if signed and signed.group(1) == "✅" else ""
    return (f'<a href="{_escape(href)}">{name}</a>' if href else name) + f'<span class=mut>{mark}</span>'


def evidence_chain(item: dict) -> dict:
    """{chains: [[node]], limits: [row], named, also: [evidence row]} for the Rationale column."""
    heads, named = _chain_heads(item)
    missing: list[str] = []
    because_rows(item, missing)
    chains, limits = [], []
    for h in heads:
        if h["do"] is False:
            limits.append(h)
            continue
        nodes = _walk(h["page"], h["id"])
        if nodes:
            nodes[0]["text"] = h["text"]
            chains.append(nodes)
    on_chain = {n["page"].resolve() for c in chains for n in c} | {h["page"].resolve() for h in limits}
    also = [r for r in item.get("evidence_rows", []) if r["role"] in _SUPPORT_ROLES
            and r["exists"] and r["file"].resolve() not in on_chain]
    return {"chains": chains, "limits": limits, "named": named, "also": also, "missing": missing,
            "backing": [h for h in heads if h["do"]]}


def _chain_html(item: dict, root: Path | None, ev: dict) -> tuple[str, str]:
    """(summary, body) of the Evidence chain fold."""
    bad = "".join(f'<div class=bad>{_escape(m)} · no such row on the cited page</div>' for m in ev["missing"])
    if not ev["chains"] and not ev["limits"] and bad:
        return "row not found", bad
    if not ev["chains"] and not ev["limits"]:
        b = item.get("because_rule") or because_rule(item)
        if b["state"] == "ai":
            return "none", '<div class=mut>An AI idea, not from an insight: no insight row stands behind it.</div>'
        return "none", ('<div class=mut>No insight row named yet. A line '
                        '<code>because: &lt;page&gt; · &lt;row&gt;</code> for this design starts the chain.</div>')
    parts = [bad] if bad else []
    if not ev["named"]:
        parts.append('<div class=mut>No row is named for this design, so these are the DO rows of the cited Wisdom pages.</div>')
    if item.get("stance") == "challenge":
        parts.append('<div class=mut>Written to test this rule: if it loses, the rule holds.</div>')
    for chain in ev["chains"]:
        steps = []
        for i, n in enumerate(chain):
            step = (f'<div class=step>▲ {_STEP_WORD.get(_level(n["pid"]), "rests on")}</div>' if i else "")
            says = f'<span class=says>{_code(name_refs(_escape(n["text"]), n["page"]))}</span>' if n["text"] else ""
            rid = f'<span class=rid>{_escape(n["id"])}</span>' if n["id"] else ""
            also = ('<div class=also>also rests on ' + " · ".join(
                (_page_link(root, page) if page else _escape(ref)) + (f" {_escape(rows)}" if rows else "")
                for ref, page, rows in n["also"]) + '</div>' if n["also"] else "")
            steps.append(f'{step}<div class=node>{rid}{says}<div class=pg>{_page_link(root, n["page"])}</div>{also}</div>')
        parts.append(f'<div class=chain>{"".join(steps)}</div>')
    if ev["limits"]:
        parts.append('<h4 class=colh>Limits</h4>' + "".join(
            f'<div class="node limit"><span class=rid>{_escape(h["id"])}</span>'
            f'<span class=says>{_code(name_refs(_escape(h["text"]), h["page"]))}</span>'
            f'<div class=pg>{_page_link(root, h["page"])}</div></div>' for h in ev["limits"]))
    if ev["also"]:
        parts.append('<div class=also><b>Also cited</b> · ' + " · ".join(
            f'{_page_link(root, r["file"])} <span class=mut>({_RUNG_WORD.get(_rung(r), "source")})</span>'
            for r in ev["also"]) + '</div>')
    chains = ev["chains"]
    summary = (" → ".join(n["id"] or _page_id(n["page"]) for n in chains[0]) if len(chains) == 1
               else f'{len(chains)} chains' if chains else "limits only")
    return summary, "".join(parts)


# ------------------------------------------------------------ design elements --

_SLOT_TOKEN = re.compile(r"^\{[A-Z]+\}$")
_ABBREV = {"dr.", "mr.", "mrs.", "ms.", "st.", "jr.", "sr.", "e.g.", "i.e."}


def _norm(token: str) -> str:
    return token.lower().strip(".,:;!?\"'“”‘’")


def design_elements(base: str, text: str, opt_out: str = "") -> list[dict]:
    """The design split into its elements against the starting text (JL 261001): one per
    sentence, clause or slot of the design, [{kind, parts: [(kind, words)]}]. An element is
    kept (the starting text's own words), new, removed, goal (a slot such as {LINK}, or the
    opt-out, that the design goal requires) or changed. A sentence is cut into its kept and
    new parts only when every part has three words or more; otherwise it stays whole,
    `changed`, with its new and removed words marked inside it."""
    a, b = base.split(), with_link(text.strip()).split()
    match = difflib.SequenceMatcher(None, [_norm(t) for t in a], [_norm(t) for t in b], autojunk=False)
    stream = []
    for op, i1, i2, j1, j2 in match.get_opcodes():
        stream += ([(t, "kept") for t in b[j1:j2]] if op == "equal"
                   else [(t, "removed") for t in a[i1:i2]] + [(t, "new") for t in b[j1:j2]])
    sentences, cur = [], []
    for tok, kind in stream:
        if kind != "removed" and _SLOT_TOKEN.match(tok):
            sentences += ([cur] if cur else []) + [[(tok, kind)]]
            cur = []
            continue
        cur.append((tok, kind))
        if kind != "removed" and re.search(r"[.:!?]$", tok) and tok.lower() not in _ABBREV:
            sentences.append(cur)
            cur = []
    sentences += [cur] if cur else []
    out = []
    for sentence in sentences:
        runs: list[tuple[str, list[str]]] = []
        for tok, kind in sentence:
            if runs and runs[-1][0] == kind:
                runs[-1][1].append(tok)
            else:
                runs.append((kind, [tok]))
        if len(runs) == 1 or all(len(toks) >= 3 for _, toks in runs):
            for kind, toks in runs:
                words = " ".join(toks)
                goal = kind == "new" and (_SLOT_TOKEN.match(words) or (opt_out and words == opt_out))
                out.append({"kind": "goal" if goal else kind, "parts": [(kind, words)]})
        else:
            out.append({"kind": "changed", "parts": [(kind, " ".join(toks)) for kind, toks in runs]})
    return out


def _ids(rows: list[dict]) -> str:
    """Row ids for the Support column; with their page when the rows sit on more than one."""
    pages = {r["pid"] for r in rows}
    return " · ".join(r["id"] if len(pages) == 1 else f'{r["pid"]} · {r["id"]}' for r in rows)


_FROM = {"requirements": "requirements", "internal": "internal insight", "external": "external insight",
         "intuition": "intuition"}


def element_record(item: dict) -> list[dict]:
    """The designer's own element record for the shown draft (JL 261002: "how to choose each
    element … the reasoning of the designer … sometimes the element might come from the
    intuitive … we can document both"): `elements.yaml`, named in its result.yaml as
    `elements`, one entry per element with its words, where it came from, the rule, row or
    theory it rests on, and whether it was reasoned or intuitive. Empty when there is none."""
    shown = shown_design(item)
    run = next((r for r in item.get("runs") or [] if shown and r["id"] == shown.get("run")), None)
    if run is None or yaml is None:
        return []
    ref = _yaml(run["result_dir"] / "result.yaml").get("elements")
    path = run["result_dir"] / str(ref.get("path")) if isinstance(ref, dict) and ref.get("path") else None
    if path is None or not path.is_file():
        return []
    try:
        data = yaml.safe_load(_read(path))
    except yaml.YAMLError:
        return []
    return [e for e in data if isinstance(e, dict)] if isinstance(data, list) else []


def _record_html(record: list[dict]) -> str:
    """The element record as the designer wrote it: words, where each came from, how it was chosen."""
    rows = []
    for e in record:
        frm = str(e.get("from") or "").strip().lower()
        how = str(e.get("thinking") or "").strip().lower()
        src = str(e.get("source") or "").strip()
        why = str(e.get("because") or "").strip()
        alts = e.get("alternatives") if isinstance(e.get("alternatives"), list) else []
        role = str(e.get("element") or "").strip()
        rows.append(
            f'<tr><td>{f"<span class=ids>{_escape(role)}</span>" if role else ""}{_escape(str(e.get("words") or ""))}</td>'
            f'<td class=elsup><span class="el-from {_escape(frm)}">{_escape(_FROM.get(frm, frm or "not said"))}</span>'
            f'{f" · <span class=el-how>{_escape(how)}</span>" if how else ""}'
            f'{f"<span class=ids>{_escape(src)}</span>" if src and src.lower() != "none" else ""}'
            f'{f"<span class=ids>because {_escape(why)}</span>" if why else ""}'
            f'{"<span class=ids>weighed: " + _escape(" · ".join(map(str, alts))) + "</span>" if alts else ""}</td></tr>')
    reasoned = sum(str(e.get("thinking") or "").lower() == "reasoned" for e in record)
    intuitive = sum(str(e.get("thinking") or "").lower() == "intuitive" for e in record)
    return ('<div class=mut>As the designer recorded it: where each element came from, and whether it was '
            f'reasoned (System 2) or intuitive (System 1). {reasoned} reasoned · {intuitive} intuitive.</div>'
            f'<table class=elems><tr><th>Element</th><th>From · how</th></tr>{"".join(rows)}</table>')


def _elements_html(item: dict, goal: dict, ev: dict) -> tuple[str, str]:
    """(summary, body) of the Design elements fold: each element of the design and what supports it.

    A kept element rests on the chain when the design follows the evidence (stance follow);
    otherwise it is the starting text as sent. A new, removed or changed element is licensed
    by the named rows when the design explores; a design that follows the evidence has no
    row for its change, and its limits are said beside it."""
    shown = shown_design(item)
    base = (goal or {}).get("starting text", "")
    if not shown or not (shown.get("text") or "").strip():
        return "after the first draft", '<div class=mut>Shown once a draft exists, element by element against the starting text.</div>'
    if not base:
        record = element_record(item)          # the designer's own record needs no starting text
        return (f"{len(record)} recorded" if record else "no starting text"), (_record_html(record) if record else "") + (
            '<div class=mut>The design goal names no starting text '
            '(<code>Starting text:</code> under Resources), so the elements cannot be compared.</div>')
    quoted = re.search(r'"([^"]+)"', (goal or {}).get("opt-out", ""))
    opt_out = quoted.group(1) if quoted else ""
    elements = design_elements(base, shown["text"], opt_out)
    follow, backing = item.get("stance") == "follow", ev["backing"]
    measured = [n["id"] for c in ev["chains"] for n in c if _level(n["pid"]) == "I" and n["id"]][:1]
    if follow:
        change = "none" + "".join(f" · {h['id']}" for h in ev["limits"])
    else:
        change = ("licensed · " + _ids(backing)) if backing and ev["named"] else "not named" if backing else "none"
    rows, kept_rows = [], False
    for e in elements:
        words = " ".join(w for k, w in e["parts"] if k != "removed")
        cell = " ".join(f'<span class=el-new>{_escape(w)}</span>' if k == "new"
                        else f'<s class=el-gone>{_escape(w)}</s>' if k == "removed" else _escape(w)
                        for k, w in e["parts"]) if e["kind"] in ("new", "removed", "changed") else _escape(words)
        if e["kind"] == "goal":
            why = "<span class=ids>Design Goal</span>"
        elif e["kind"] == "kept":
            ids = ("Design Goal" if opt_out and words == opt_out
                   else " · ".join([_ids(backing)] + measured) if follow and backing else "as sent")
            kept_rows |= ids not in ("Design Goal", "as sent")
            why = f'kept<span class=ids>{_escape(ids)}</span>'
        else:
            why = f'<span class=el-new>★ {e["kind"]}</span><span class=ids>{_escape(change)}</span>'
        rows.append(f'<tr><td>{cell}</td><td class=elsup>{why}</td></tr>')
    counts = " · ".join(f"{n} {k}" for k in ("new", "changed", "removed")
                        if (n := sum(e["kind"] == k for e in elements)))
    summary = f"{counts} of {len(elements)}" if counts else "all kept"
    note = ('<div class=mut>Kept parts are backed as part of the message as it was tested, not one by one.</div>'
            if kept_rows else "")
    record = element_record(item)
    if record:
        summary += f" · {len(record)} recorded"
    against = ('<div class=mut>Against the starting text:</div>' if record else "")
    return summary, (_record_html(record) if record else "") + (
        f'{against}<table class=elems><tr><th>Element</th><th>Support</th></tr>{"".join(rows)}</table>{note}')


def _review_notes(item: dict) -> str:
    """The independent reviewer's own words on the shown draft (its `review.md`), one per line."""
    shown = shown_design(item)
    if not shown:
        return ""
    for r in reversed(item["runs"]):
        if (r["kind"] == "verify" and r["status"] == "complete"
                and any(str(t.get("path", "")).startswith(f'results/{shown["run"]}/') for t in r["targets"])):
            path = r["result_dir"] / "review.md"
            if not path.is_file():
                return ""
            lines = [re.sub(r"^[-*]\s+|^\d+[.)]\s+", "", ln.strip()) for ln in _read(path).splitlines()
                     if ln.strip() and not ln.lstrip().startswith("#")]
            return "".join(f"<li>{_escape(ln)}</li>" for ln in lines[:8])
    return ""



def _design_runs_list(item: dict) -> str:
    """This design's own runs as a short list that fits the column (JL 261001): the step,
    its outcome, who and when, the person's words when they gave a decision; the run id
    small underneath. The insight board's runs sit behind its pages, not here."""
    rows = []
    for r in item["runs"]:
        bad = r["status"] in ("failed", "blocked")
        outcome = r["outcome"] or ("planned · queued for agent" if r["status"] == "planned" and r["mode"] == "agent"
                                   else r["status"])
        if r["checks"]:
            outcome += f' {r["checks_passed"]}/{len(r["checks"])}'
        when = r["finished"] or r["started"] or ""
        words = f'<div class=said>“{_escape(r["words"])}”</div>' if r["words"] else ""
        rows.append(f'<li{" class=old" if r["status"] == "superseded" else ""}><div class=rl>'
                    f'<b>{_escape(_STEP.get(r["kind"], r["kind"]))}</b>'
                    f'<span class="{"bad" if bad else "ok" if r["status"] == "complete" else "mut"}">{_escape(outcome)}</span>'
                    f'<span class=mut>{_escape(r["actor"])} · {_escape(when)}</span></div>'
                    f'{words}<code class=rid>{_escape(r["id"])}</code></li>')
    return f'<ul class=runs>{"".join(rows)}</ul>' if rows else ""


def _rationale_col(item: dict, root: Path | None, goal: dict | None = None) -> str:
    """The open card's middle column (JL 261001): why this design. The design move stays open;
    under it two folds: first the Design elements, each part of the design and what supports
    it, then the Evidence chain those supports come from. How the design was made (its Design
    Runs) sits with the design, in the first column."""
    out = ('<h4 class=colh>Design move</h4>'
           f'<p class=goal>{_escape(item["goal"]) or "<span class=mut>No design move recorded.</span>"}</p>')
    ev = evidence_chain(item)
    for label, (summary, body) in (("Design elements", _elements_html(item, goal or {}, ev)),
                                   ("Evidence chain", _chain_html(item, root, ev))):
        out += f'<details class=sub><summary>{label} · <span class=mut>{_escape(summary)}</span></summary>{body}</details>'
    return out


def _evaluation_col(item: dict, aim: dict | None = None) -> str:
    """The open card's right column (JL 261001): Evaluation, of two kinds. Acceptance is
    judged now, by the independent Verify; the expected effect is judged later, by the send."""
    aim = aim or {}
    head, rules = _rule_checks(item)
    notes = _review_notes(item)
    out = (f'<details class=sub><summary>Acceptance · {head}</summary><ul class=checks>{rules}</ul></details>')
    if notes:
        out += f'<details class=sub><summary>Review notes</summary><ul class=notes>{notes}</ul></details>'
    effect = ""
    for label, value in (("Expected", item["expected"]), ("Wrong if", item["falsified"]),
                         ("Against", aim.get("baseline", "")), ("Measured by", aim.get("success metrics", ""))):
        if value:
            tone = {"Expected": "ok", "Wrong if": "bad"}.get(label, "mut")
            effect += f'<div class=betl><span class="k {tone}">{label}</span>{_escape(value)}</div>'
    out += ('<details class=sub><summary>Expected effect · <span class=mut>not tested yet, judged at the send</span></summary>'
            + (effect or '<div class=mut>No expected effect recorded.</div>') + '</details>')
    return out


_OPT_OUT = ": Reply STOP to opt-out"


def _sms_bubble(text: str) -> str:
    """The SMS as the patient sees it, with the `{LINK}` slot where the platform puts the link."""
    return _escape(with_link(text.strip())).replace(LINK_SLOT, f'<span class=link>{LINK_SLOT}</span>')


def design_number(item_id: str) -> str:
    """`ITEM03` said on screen: `Design 3` (JL 261001: Design N on screen, ITEMNN in the files)."""
    hit = re.match(r"^ITEM0*(\d+)$", str(item_id))
    return f"Design {hit.group(1)}" if hit else str(item_id)


# ----------------------------------------------------------- element matrix --
# JL 261002: "how to make the design element be the first citizen", "I want to see how design
# element played an important role here". The Design Goal names the starting text's parts
# (Resources › Elements); every design is read slot by slot against them, so the page shows
# which elements each design changed, and which the task explored at all.

_SLOT_PART = re.compile(r'([A-Za-z][A-Za-z -]*?)\s*=\s*"([^"]+)"')


def element_slots(aim: dict) -> list[tuple[str, str]]:
    """The Design Goal's `Elements:` line, `greeting = "Hi," · sender = "…"`: the starting
    text named part by part, in reading order."""
    return [(m.group(1).strip(), m.group(2)) for m in _SLOT_PART.finditer((aim or {}).get("elements", ""))]


def slot_reading(base: str, slots: list[tuple[str, str]], text: str) -> dict:
    """One design read slot by slot against the starting text: {"slots": {name: (status,
    words)}, "added": [(after, words)]}. A slot is same (its words kept), changed (other
    words in its place), or removed; words the design adds between two slots are added
    after the slot before them. A slot whose words are not in the starting text is missing."""
    a, b = with_link(base).split(), with_link(text.strip()).split()
    na, nb = [_norm(t) for t in a], [_norm(t) for t in b]
    span, pos = {}, 0
    for name, phrase in slots:                        # where each slot sits in the starting text
        words = [_norm(t) for t in phrase.split()]       # as written: a colon here takes no {LINK}
        for k in range(pos, len(na) - len(words) + 1):
            if na[k:k + len(words)] == words:
                span[name], pos = (k, k + len(words)), k + len(words)
                break
    owner = {i: name for name, (s, e) in span.items() for i in range(s, e)}
    kept = {name: [] for name in span}
    words_of = {name: [] for name in span}
    changed, added = set(), []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, na, nb, autojunk=False).get_opcodes():
        if op == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                if i in owner:
                    words_of[owner[i]].append(b[j])
                    kept[owner[i]].append(i)
            continue
        hit = [owner[i] for i in range(i1, i2) if i in owner]
        if op == "insert":
            inside = owner.get(i1) if owner.get(i1) and owner.get(i1 - 1) == owner.get(i1) else None
            if inside:
                changed.add(inside)
                words_of[inside] += b[j1:j2]
            else:
                added.append((owner.get(i1 - 1, "start"), " ".join(b[j1:j2])))
            continue
        for name in dict.fromkeys(hit):
            changed.add(name)
        if hit and j2 > j1:
            words_of[hit[0]] += b[j1:j2]
    out = {}
    for name, _ in slots:
        if name not in span:
            out[name] = ("missing", "")
        elif name not in changed:
            out[name] = ("same", " ".join(words_of[name]))
        else:
            words = " ".join(words_of[name]).strip()
            out[name] = ("changed", words) if words else ("removed", "")
    return {"slots": out, "added": added}


def _element_matrix_html(items: list[dict], aim: dict) -> str:
    """The page's designs, one row each, read slot by slot against the starting text: ★ what
    a design changed, · what it kept, and a last row counting how many designs changed each slot."""
    slots = element_slots(aim)
    base = (aim or {}).get("starting text", "")
    drafts = [(i, shown_design(i)) for i in items if i["state"] != "declined"]
    drafts = [(i, d) for i, d in drafts if d and (d.get("text") or "").strip()]
    if not slots or not base:
        return ""
    if not drafts:
        return ('<details class=elmatrix><summary>Design elements · no draft yet</summary><div class=mut>'
                'Once a design has a draft, it is read here slot by slot against the starting text.</div></details>')
    head = "".join(f"<th>{_escape(name)}</th>" for name, _ in slots) + "<th>added</th>"
    rows, counts = [], {name: 0 for name, _ in slots}
    added_n = 0
    for item, draft in drafts:
        reading = slot_reading(base, slots, draft["text"])
        record = {str(e.get("element") or "").strip().lower(): e for e in element_record(item)}
        cells = []
        for name, _ in slots:
            status, words = reading["slots"][name]
            rec = record.get(name.lower())
            tag = ""
            if rec:
                frm, how = str(rec.get("from") or "").lower(), str(rec.get("thinking") or "").lower()
                tag = (f'<span class="ids el-from {_escape(frm)}">{_escape(_FROM.get(frm, frm))}'
                       f'{" · " + _escape(how) if how else ""}</span>')
            if status in ("changed", "removed"):
                counts[name] += 1
            cells.append(f'<td class="el-{status}" title="{_escape(words)}">'
                         + ({"same": "·", "missing": "–", "removed": "<s>removed</s>"}.get(status)
                            or f"★ {_escape(words)}") + tag + "</td>")
        extra = reading["added"]
        added_n += bool(extra)
        cells.append('<td class="el-changed">' + "<br>".join(f"★ {_escape(w)}" for _, w in extra) + "</td>"
                     if extra else '<td class="el-same">·</td>')
        rows.append(f'<tr><th><a href="#item-{_escape(item["id"])}" data-item="{_escape(item["id"])}">'
                    f'{_escape(design_number(item["id"]))}</a> <span class=glyph>{item.get("glyph", "")}</span></th>'
                    + "".join(cells) + "</tr>")
    total = len(drafts)
    foot = ("".join(f"<td>{counts[name]} of {total}</td>" for name, _ in slots) + f"<td>{added_n} of {total}</td>")
    explored = sum(1 for n in counts.values() if n) + (1 if added_n else 0)
    return ('<details class=elmatrix open><summary>Design elements · '
            f'{total} design{"s" if total != 1 else ""} × {len(slots)} slots · {explored} explored</summary>'
            '<div class=mut>Each design read slot by slot against the starting text (Design Goal › Resources › '
            'Elements): ★ what it changed, · what it kept. Where a design recorded its elements, each cell says '
            'where the element came from and how it was chosen.</div>'
            f'<div class=elscroll><table class=elmat><tr><th>design</th>{head}</tr>{"".join(rows)}'
            f'<tr class=elcount><th>changed in</th>{foot}</tr></table></div></details>')


def shared_rules(items: list[dict]) -> list[str]:
    """The rules every live design keeps, in the order the first one lists them."""
    live = [i for i in items if i["state"] != "declined" and i["acceptance"]]
    if not live:
        return []
    return [r for r in live[0]["acceptance"] if all(r in i["acceptance"] for i in live[1:])]


def _task_block(snapshot: dict, items: list[dict], aim: dict | None = None) -> str:
    """The Design Goal in brief, above the cards (JL 261001): the task, then the objective,
    the audience, how success is measured and the baseline every design is read against,
    then the acceptance checks every design keeps. The full input is the Design Goal Space."""
    row, aim = snapshot["goal"]["row"], aim or {}
    rules = shared_rules(items)
    head = _escape(design_title(row)) if row else _escape(snapshot["title"])
    lines = [(label, aim.get(key, "")) for label, key in (("Objective", "objective"), ("Audience", "target audience"),
                                                           ("Measured by", "success metrics"), ("Baseline", "baseline"))]
    if not any(v for _, v in lines) and row:
        lines = [("Audience", row["audience"]), ("Patient task", row["job"]), ("Channel", row["venue"])]
    if not row:
        lines = [("", "No design task line names this folder yet.")]
    if rules:
        lines.append(("Every design keeps", " · ".join(rules)))
    body = "".join(f'<div class=tl><span class=mut>{_escape(k)}</span>{_escape(v)}</div>' for k, v in lines if v)
    return f'<div class=task><div class=taskhead>{head}</div>{body}</div>'


_SUPPORT_ROLES = ("handoff", "evidence", "inspiration", "reference", "avoid")


def _page_words(row: dict) -> str:
    """An insight page by its name in words: `FW01-send-salience` -> `Send salience`."""
    # both page-id schemes: `FW01-send-salience` and `W01-full-send-salience`
    words = re.sub(r"^(?:[A-Z][DIKW]\d{2}|[DIKW]\d{2}-[a-z0-9]+)-", "", Path(row["name"]).stem).replace("-", " ").strip()
    return words[:1].upper() + words[1:]


def _rung(row: dict) -> str:
    stem = Path(row["name"]).stem
    hit = _RUNG.match(stem) or re.match(r"^()([DIKW])\d{2}-[a-z0-9]+-", stem)
    return hit.group(2) if hit else "?"


def _card_columns(item: dict, text: str, picture: bool) -> str:
    """One card's closed row (JL 261001): one short line per column, Design · Rationale ·
    Evaluation. The sentences behind each line are the open card's; the closed row only
    names the design, what it rests on, and where its evaluation stands."""
    pages = sorted((r for r in item.get("evidence_rows", []) if r["role"] in _SUPPORT_ROLES),
                   key=lambda r: "WKID?".index(_rung(r)))
    rests = (f'<span class=mut>Rests on</span> {_escape(_page_words(pages[0]))}'
             + (f' <span class=mut>· +{len(pages) - 1}</span>' if len(pages) > 1 else "")
             if pages else '<span class=mut>From the design goal alone</span>')
    head, _rules = _rule_checks(item)
    count = re.match(r"(\d+) of (\d+) pass", head)
    accept = (f'<span class="{"ok" if count.group(1) == count.group(2) else "bad"}">✓ {count.group(1)}/{count.group(2)}</span> '
              '<span class=mut>acceptance</span>' if count else '<span class=mut>acceptance not checked</span>')
    effect = ' <span class=mut>· effect not tested yet</span>' if item["expected"] else ""
    # The state's emoji sits right after the number (JL 261001), so six rows scan at a glance;
    # the word is said only when the emoji alone does not say it (ready needs no word).
    word = "" if item["state"] == "ready" else item["state"]
    word += (" · waiting on " + item["waiting"]) if item["waiting"] else ""
    return (f'<span class=c1><span class=line><b>{_escape(design_number(item["id"]))}</b>'
            f' <span class=glyph title="{_escape(item["state"])}">{_escape(item["glyph"])}</span>'
            f' <b>· {_escape(item["title"])}</b>'
            f'{(" <span class=\"mut st\">" + _escape(word.strip(" ·")) + "</span>") if word else ""}</span></span>'
            f'<span class=c2><span class=line>{rests}</span></span>'
            f'<span class=c3><span class=line>{accept}{effect}</span></span>')


def _item_card(root: Path, item: dict, human: str, selected: bool, *, writable: bool = True, chat_prompt: str = "",
               extra: str = "", aim: dict | None = None) -> str:
    meta = " · ".join(x for x in (item["type"], item["audience"], item["job"]) if x)
    if item.get("ready"):
        ready = item["ready"]
        size = len(ready["text"].strip().replace(LINK_SLOT, ""))
        text, note = ready["text"], f'Ready for Delivery · {size} characters · passed independent review'

    elif item["latest"]:
        lat = item["latest"]
        verdict = f' · {lat["verdict"]}' if lat["verdict"] and lat["status"] == "complete" else ""
        text, note = lat["text"], f'Latest draft · {_escape(lat["status"])}{_escape(verdict)}'

    else:
        text, note = "", "No draft yet"
    picture = design_picture(root, item)
    if picture:
        # A screen is read as its picture; its source stays one click away.
        design = (picture + f'<div class=mut>{note}</div>'
                  f'<details><summary>the HTML behind this screen</summary><pre class=src>{_escape(text)}</pre></details>')
    elif text and (item["type"] or "").lower() == "sms":
        # An SMS is read as the patient sees it: one bubble on a phone, the link where the system puts it.
        design = (f'<div class=phone><div class=from>Text message</div><div class=bubble>{_sms_bubble(text)}</div></div>'
                  f'<div class=mut>{note}</div>')
    else:
        design = (f'<pre class=text>{_escape(text)}</pre>' if text else "") + f'<div class=mut>{note}</div>'
    actions, fold = _actions(item, human) if writable else ("", "")
    # just "Design Runs" (JL 261001): the emoji and the acceptance count already say how far it got
    runs = (f'<details class=runsfold><summary>Design Runs</summary>'
            f'{_design_runs_list(item) or "<div class=mut>No run yet.</div>"}</details>')
    if actions and fold:
        actions = (f'<details class=decide{" open" if selected else ""}><summary>{_escape(fold)}</summary>'
                   f'<div class=act>{actions}</div></details>')
    elif actions:
        actions = f'<div class=act>{actions}</div>'
    # Open, the card keeps the closed row's three columns (JL 261001): the design with its
    # buttons, then its rationale, then its evaluation. The design column stays in view.
    body = (f'<div class=cardgrid><div class="col pic">{design}{runs}{actions}<div class=msg></div></div>'
            f'<div class="col why">{_rationale_col(item, root, aim)}</div>'
            f'<div class="col eval">{_evaluation_col(item, aim)}</div></div>')
    # One fixed-height row per item that opens into a fixed-height card (JL 260918): the row
    # names the item, previews the design in one line, and says where it stands.
    return (
        f'<section class="item{" sel" if selected else ""}" id="item-{_escape(item["id"])}" data-item="{_escape(item["id"])}">'
        f'<details class="itemfold cardrow"{" open" if selected else ""}><summary>{_card_columns(item, text, bool(picture))}</summary>'
        f'<div class=itembody><div class=mut>{_escape(meta)} · <code>{_escape(item["id"])}</code> in the files</div>'
        f'{design_next_run(item, human, writable=writable)}{design_chat_copy(chat_prompt)}{body}{extra}</div></details></section>'
    )


# There is no bar that acts on every item at once. JL asked on 260921 for it to go:
# one decision, one item, one sentence on the record. The all-items writers in
# design_actions are no longer reachable from a surface, and perform_action refuses
# the `-all` actions the way it already refuses `adopt-all`.


def render_design(snapshot: dict, space: str = "goal", selected_item: str = "",
                  flow_space: str | None = None, query: dict | None = None) -> str:
    """Three Spaces (JL 261001): Goal (the one design task, stated once), Design (the task
    again, then one card per design: Design · Rationale · Supporting work · Expectation, with
    its insight pages and its runs folded inside), Delivery (designs whose Verify passed).
    The old Insight and Run Spaces open the Design Space."""
    root = snapshot["root"]
    page = snapshot["page"]
    items = snapshot["items"]
    human = snapshot.get("human", "person")
    aliases = {"frame": "goal", "plan": "goal", "brief": "goal", "ask": "goal",
               "intent": "design", "draft": "design", "items": "design",
               "insight": "design", "signal": "design", "evidence": "design", "insights": "design",
               "run": "design", "runs": "design", "shape": "design", "workflow": "design", "runtime": "design",
               "create": "design", "review": "design", "launch": "delivery", "commit": "delivery"}
    selected = aliases.get(space, space) if space else "goal"
    if selected not in ("goal", "design", "delivery"):
        selected = "goal"
    ids = [item["id"] for item in items]
    if selected_item not in ids:
        selected_item = ""
    q = query or {}
    board_link = (f' · <a href="/_board/design-board?path={quote(str(q["path"]), safe="")}">↑ Board level</a>'
                  if q.get("path") else "")
    header = (
        f'<h1>🎨 {_escape(snapshot["title"])}</h1>'
        f'<div class=mut>Page level · <code>{_escape(snapshot["folder"].name)}</code>{board_link}</div>'
    )
    if not snapshot["current"]:
        header += f'<div class=bad>{_escape(snapshot["reason"])}</div>'
    if snapshot["insight"]["status"] == "blocked":
        header += f'<div class=bad>{_signal_line(snapshot["insight"])}</div>'
    if not snapshot["yaml"]:
        header += '<div class=bad>PyYAML is not installed for this server; Run records cannot be read.</div>'

    # Goal Space -------------------------------------------------------------
    goal = snapshot["goal"]
    missing = max(goal["wanted"] - goal["registered"], 0)
    request = snapshot.get("draft_request")
    if goal["row"]:
        row = goal["row"]
        # counts is HTML from here on: the text is escaped once, the button below is markup
        declined = sum(1 for i in items if i["state"] == "declined")
        counts = _escape((f'{goal["wanted"]} designs requested · ' if goal["wanted"] else "") +
                         f'{goal["registered"]} registered · {goal["ready"]} ready'
                         + (f' · {declined} declined' if declined else ""))
        if missing and request:
            counts += (f' · <span class=mut>draft request open: {request["items"]} item(s) asked by '
                       f'{_escape(request["asked_by"])} {_escape(request["asked_at"][:16])}</span>')
        elif missing and snapshot["current"] and not snapshot.get("static"):
            counts += (f' <span class=act data-item="__all__"><button class=do data-action=draft-request>'
                       f'Ask the agent to draft the missing {missing}</button><span class=msg></span></span>')
        board_dir = Path(snapshot["folder"]).parent.parent
        goal_html = ('<h2>The design task</h2>'
                     f'<pre class=text>{_escape(goal["sentence"])}</pre>'
                     + _input_html(root, row, design_input(board_dir, Path(snapshot["folder"])), counts,
                                   shared_rules(items)))
    elif goal["brief"]:
        goal_html = (f'<div class=empty>No line in {_href(root, goal["brief"], goal["brief"].name)} names this folder yet; '
                     'add a row (audience · job · venue · designs · folder) and the goal appears here.</div>')
    else:
        goal_html = '<div class=empty>No design task file under 0-BR-brief/ on the owning board; the goal has nowhere to be read from.</div>'

    # Design Space -----------------------------------------------------------
    writable = snapshot["current"] and not snapshot.get("static")
    chat_prompts = {item["id"]: design_chat_prompt(snapshot, item) for item in items}
    inp = design_input(Path(snapshot["folder"]).parent.parent, Path(snapshot["folder"]))
    # every design-input line by its key: the aim, and the starting text and opt-out the elements read
    aim = {k.lower(): v for block in ("Venue", "Resources", "Aim") for k, v, _ in inp["blocks"].get(block, [])}
    design_html = _task_block(snapshot, items, aim)
    design_html += _element_matrix_html(items, aim)

    if items:
        # A declined item is retired: its card stays for the record, folded after the live ones.
        live = [item for item in items if item["state"] != "declined"]
        retired = [item for item in items if item["state"] == "declined"]
        design_html += ('<div class="mut foldbar"><a href=# data-fold=open>open all</a> · '
                        '<a href=# data-fold=close>close all</a></div>'
                        '<div class=cardhead><span>Design</span><span>Rationale</span>'
                        '<span>Evaluation</span></div>')
        design_html += "".join(_item_card(root, item, human, item["id"] == selected_item, writable=writable,
                                         chat_prompt=chat_prompts[item["id"]], aim=aim)
                               for item in live)
        if retired:
            opened = " open" if selected_item in {item["id"] for item in retired} else ""
            design_html += (f'<details class=retired{opened}><summary>Declined, kept for the record · {len(retired)}</summary>'
                            + "".join(_item_card(root, item, human, item["id"] == selected_item, writable=writable,
                                                 aim=aim) for item in retired)
                            + '</details>')
    else:
        design_html = (f'<div class=empty>No Design Item register yet. Add the first item below; it writes '
                       f'<code>{_escape(snapshot["register"].relative_to(snapshot["folder"]).as_posix())}</code>.</div>')
    if snapshot["unassigned"]:
        design_html += ('<h2>Runs without an item</h2>'
                        '<table><tr><th>run</th><th>Run type</th><th>who</th><th>when</th><th>status</th><th>outcome</th><th>next</th></tr>'
                        f'{_run_rows(root, snapshot["unassigned"])}</table>')

    # Design Space, continued: runs that name no item, and the records check -----
    if not items and not snapshot["runs"]:
        design_html += '<div class=empty>No Design Run records are present in this folder.</div>'
    if not items and snapshot["runs"]:
        design_html += ('<h2>Runs</h2><table><tr><th>run</th><th>Run type</th><th>who</th><th>when</th><th>status</th><th>outcome</th><th>next</th></tr>'
                        f'{_run_rows(root, snapshot["runs"])}</table>')
    audit = snapshot["audit"]
    if snapshot["current"]:
        if audit:
            design_html += (f'<details><summary class=bad>records check: {len(audit)} finding(s)</summary><ul class=rules>'
                            + "".join(f"<li><code>{_escape(issue)}</code></li>" for issue in audit) + '</ul></details>')
        else:
            design_html += '<div class="mut ok">records check: PASS · every run has its result and receipt</div>'

    # Delivery Space ---------------------------------------------------------
    # A quick overview of what is ready to hand to the next team: one row per
    # item whose independent Verify passed.
    def listing(group: list[dict]) -> str:
        rows, tiles = [], []
        for item in (item for item in group if item.get("ready")):
            design = item.get("ready")
            label = _escape(design_number(item["id"]))
            if q.get("path") and q.get("file"):
                label = (f'<a href="?path={quote(str(q["path"]), safe="")}&amp;file={quote(str(q["file"]), safe="")}'
                         f'&amp;space=design&amp;item={_escape(item["id"])}">{label}</a>')
            sent = with_link(design["text"]) if design else ""
            text_html = (_sms_bubble(sent) if design and (item["type"] or "").lower() == "sms"
                         else _escape(sent) if design else "")
            body = (f"<div class=design>{text_html}</div>" if design else "<span class=mut>not ready for Delivery yet</span>")
            rows.append(f'<tr><td class=who><b>{label}</b><div class=mut>{_escape(item["title"])}</div></td><td>{body}</td></tr>')
            tiles.append(f'<figure>{design_picture(root, item) or body}'
                         f'<figcaption><b>{label}</b> {_escape(item["title"])}</figcaption></figure>')
        if any(item.get("render") and item.get("ready") for item in group):
            # Screens read side by side as pictures; text designs keep the table.
            return f'<div class=gallery>{"".join(tiles)}</div>'
        return ('<table class=designs><tr><th>design</th><th>the text, word for word</th></tr>' + "".join(rows) + '</table>') if rows else ""

    # A declined item is retired, like a retired Evidence Item: kept for the record, out of the overview.
    live = [item for item in items if item["state"] != "declined"]
    retired = [item for item in items if item["state"] == "declined"]
    delivery_html = [listing(live) or '<div class=empty>No design is ready yet. A design appears here after Verify passes.</div>']
    if retired:
        delivery_html.append(f'<details class=retired><summary>Declined, kept for the record · {len(retired)}</summary>'
                             f'{listing(retired)}</details>')

    if snapshot.get("csv_url") and any(item.get("ready") for item in live):
        delivery_html.append(f'<div class=mut><a href="{_escape(snapshot["csv_url"])}">↓ This design task\'s designs · '
                             f'{sum(1 for item in live if item.get("ready"))} · csv</a></div>')
    panes = {"goal": goal_html, "design": design_html, "delivery": "".join(delivery_html)}
    def _rel(path) -> str:
        try:
            return str(Path(path).resolve().relative_to(Path(root).resolve()))
        except (TypeError, ValueError):
            return str(path or "")
    page_rel = _rel(snapshot["page"])
    board_rel = _rel(Path(snapshot["insight"].get("design_board") or Path(snapshot["folder"]).parent.parent) / "board.md")
    for key in panes:
        panel = design_runs_panel(key, snapshot["runs"], root=root, page=page_rel, board=board_rel,
                                  whole="this design task")
        panes[key] = f'<div class=space-main>{panes[key]}</div>{panel}'
    panel_css, panel_js = runs_panel_assets()
    tabs = "".join(f'<button type=button data-space="{key}"{" class=on" if key == selected else ""}>{label}</button>'
                   for key, label in (("goal", "Design Goal Space"), ("design", "Design Space"), ("delivery", "Delivery Space")))
    pane_html = "".join(f'<section class="pane split{" on" if key == selected else ""}" data-space="{key}">{value}</section>'
                        for key, value in panes.items())
    ctx = {"path": str(q.get("path") or ""), "file": str(q.get("file") or "")}
    script = (
        "<script>(function(){var CTX=" + _json(ctx) + ";"
        "var bs=[].slice.call(document.querySelectorAll('.tabs button')),ps=[].slice.call(document.querySelectorAll('.pane'));"
        "function sel(s,w){bs.forEach(function(b){b.classList.toggle('on',b.dataset.space===s)});"
        "ps.forEach(function(p){p.classList.toggle('on',p.dataset.space===s)});"
        "if(w){var u=new URL(location.href);u.searchParams.set('space',s);history.replaceState({},'',u)}}"
        "bs.forEach(function(b){b.onclick=function(){sel(b.dataset.space,true)}});"
        "var me=document.querySelector('.pane.on .item.sel');if(me)me.scrollIntoView({block:'start'});"
        "document.querySelectorAll('[data-fold]').forEach(function(a){a.onclick=function(e){e.preventDefault();"
        "document.querySelectorAll('details.itemfold').forEach(function(d){d.open=a.dataset.fold==='open'})}});"
        "document.querySelectorAll('button.do').forEach(function(b){b.onclick=function(){"
        "var box=b.closest('[data-item]'),msg=box.querySelector('.msg'),body={path:CTX.path,file:CTX.file,action:b.dataset.action,item:box.dataset.item};"
        "box.querySelectorAll('input,textarea,select').forEach(function(f){if(f.name)body[f.name]=f.value});"
        "msg.className='msg';msg.textContent='writing…';b.disabled=true;"
        "fetch('/_board/design-act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})"
        ".then(function(r){return r.json()}).then(function(j){if(!j.ok){msg.className='msg bad';msg.textContent=j.err||'refused';b.disabled=false;return}"
        "msg.className='msg ok';msg.textContent='written '+(j.run||j.item||'');location.href=j.url})"
        ".catch(function(e){msg.className='msg bad';msg.textContent=String(e);b.disabled=false})}});})();</script>"
    )
    return (
        '<!doctype html><html lang=en><head><meta charset=utf-8>'
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        f'<title>🎨 Design · {_escape(snapshot["title"])}</title><style>{_CSS}{panel_css}</style></head><body>'
        f'<header>{header}</header><nav class=tabs>{tabs}</nav><main>{pane_html}</main>{script}{panel_js}{design_chat_copy_script()}</body></html>'
    )


def _json(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


_OLD_GROUP = re.compile(r"(^|/)2-DS-design(/|$)")
_OLD_FOLDER = re.compile(r"(^|/)DS(\d{2})-")


def modern_file(file: str) -> str:
    """Old links said 2-DS-design/DS01-…; the folders are 2-Design/Design-01-… now (JL 260916)."""
    out = _OLD_GROUP.sub(r"\g<1>2-Design\2", file or "")
    out = _OLD_FOLDER.sub(r"\g<1>Design-\2-", out)
    return _OLD_FOLDER.sub(r"\g<1>Design-\2-", out)      # the page file name carries the id twice


def _pick_board_page(root: Path, short: str, boards: list[Path], held: bool) -> bytes:
    """The answer to a short link that names no board and fits several, or none."""
    from urllib.parse import urlencode
    rows = []
    for b in boards:
        rel = b.resolve().relative_to(root.resolve()).as_posix()
        name = renamed_folder(b, short) if held else ""
        href = "/_board/design?" + urlencode({"folder": short, "board": b.name}) if held else \
               "/_board/design-board?" + urlencode({"board": b.name})
        rows.append(f'<li><a href="{_escape(href)}">{_escape(b.name)}</a>'
                    f'{(" · " + _escape(name)) if name else ""} <span class=mut>{_escape(rel)}</span></li>')
    head = (f"<code>{_escape(short)}</code> is on {len(boards)} DesignBoards; pick one, or add <code>&amp;board=</code> to the link:"
            if held else f"No DesignBoard here has a folder <code>{_escape(short)}</code>. The boards:")
    return (f'<!doctype html><meta charset=utf-8><title>🎨 Design · pick a board</title><style>{_CSS}</style>'
            f'<h1>🎨 Design</h1><p>{head}</p><ul>{"".join(rows)}</ul>').encode("utf-8")


_FOLDER_FILE = re.compile(r"^2-Design/(Design-\d+-[^/]+)/\1\.md$")


def shown_design(item: dict) -> dict | None:
    """The design an item has: its ready candidate, else its latest draft."""
    return item.get("ready") or item.get("latest")


def renamed_folder(board: Path | None, name: str) -> str:
    """A folder renamed to say its goal keeps its Design-NN id: an old name finds the one folder with that id."""
    hit = re.match(r"^Design-(\d+)(?:-|$)", name or "")  # the bare id works too: Design-04, Design-4
    group = Path(board) / "2-Design" if board is not None else None
    if group is None or not hit or (group / name).is_dir():
        return name
    found = [p.name for p in group.glob(f"Design-{int(hit.group(1)):02d}-*") if p.is_dir()]
    return found[0] if len(found) == 1 else name


class DesignMixin:
    """GET/HEAD/POST surface for a current Design Page-Folder."""

    def design_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        short = (query.pop("folder", None) or [""])[0].strip("/")
        if short and not query.get("file"):
            # short link: ?folder=Design-01-… names the Design Folder; the board is the one given or the only one
            from urllib.parse import urlencode
            from live.designboard import DESIGN_GROUP, design_boards, resolve_board
            root = Path(self.root)
            named_board = (query.get("path") or query.pop("board", None) or [""])[0]
            board = resolve_board(root, named_board)
            if board is None and not named_board:
                # several DesignBoards: the folder picks its board when exactly one holds it,
                # by its exact name first (every board has a Design-01), then by an old name
                boards = design_boards(root)
                holders = [b for b in boards if (b / DESIGN_GROUP / short).is_dir()] or \
                          [b for b in boards if (b / DESIGN_GROUP / renamed_folder(b, short)).is_dir()]
                board = holders[0] if len(holders) == 1 else None
                if board is None:
                    # never guess: two boards' Design-01 are unrelated designs (audit N5)
                    return self._design_send(_pick_board_page(root, short, holders or boards, bool(holders)),
                                             404, head_only)
            short = renamed_folder(board, short)
            if board is not None and (board / DESIGN_GROUP / short / f"{short}.md").is_file():
                rel = board.resolve().relative_to(root.resolve()).as_posix()
                query.pop("board", None)
                query["path"] = ["/" + ("" if rel == "." else rel + "/") + "board.md"]
                query["file"] = [f"{DESIGN_GROUP}/{short}/{short}.md"]
                self.send_response(302)
                self.send_header("Location", "/_board/design?" + urlencode(query, doseq=True))
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
        payload = {"path": (query.get("path") or [""])[0],
                   "file": (query.get("file") or [""])[0]}
        from live.designboard import resolve_board
        board = resolve_board(Path(self.root), payload["path"])
        asked_exists = board is not None and bool(payload["file"]) and (board / payload["file"]).is_file()
        modern = payload["file"] if asked_exists else modern_file(payload["file"])
        named = _FOLDER_FILE.match(modern)
        if named and not asked_exists:
            current = renamed_folder(board, named.group(1))
            modern = f"2-Design/{current}/{current}.md"
        if board is not None and not (board / modern).is_file():
            # no folder of that name today: read the link as given, so a legacy
            # folder is named unsupported (410) instead of answering a bare 404
            modern = payload["file"]
        if modern != payload["file"]:
            # an old bookmark: send the browser to the current folder name so the URL updates too
            from urllib.parse import urlencode
            query["file"] = [modern]
            self.send_response(302)
            self.send_header("Location", "/_board/design?" + urlencode(query, doseq=True))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        got = self.target(payload)
        if got[0] is None:
            body = f"<h1>🎨 design</h1><p>{_escape(got[1])}</p>".encode("utf-8")
            return self._design_send(body, 404, head_only)
        page_src = Path(got[0])
        snapshot = design_snapshot(page_src, self.root)
        if payload["path"]:
            snapshot["csv_url"] = (f'/_board/design-bundle?path={quote(payload["path"], safe="")}'
                                   f'&folder={quote(snapshot["folder"].name, safe="")}')
        code = 200 if snapshot["current"] else 410
        body = render_design(
            snapshot,
            (query.get("space") or ["goal"])[0],
            (query.get("item") or [""])[0],
            query=payload,
        ).encode("utf-8")
        return self._design_send(body, code, head_only)

    def _design_send(self, body: bytes, code: int, head_only: bool):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_design(self, payload):
        payload = dict(payload, file=modern_file(str(payload.get("file") or "")))
        got = self.target(payload)
        if got[0] is None:
            return None, got[1]
        page_src = Path(got[0])
        current, reason = design_contract_status(page_src)
        if not current:
            return None, reason
        return {
            "url": "/_board/design?path=%s&file=%s"
            % (quote(payload.get("path") or ""), quote(payload.get("file") or "")),
        }, None

    def design_act(self, payload):
        """One Design action: a human decision Run, an agent queue Ticket, or a register row."""
        payload = dict(payload, file=modern_file(str(payload.get("file") or "")))
        got = self.target(payload)
        if got[0] is None:
            return None, got[1]
        page_src = Path(got[0])
        current, reason = design_contract_status(page_src)
        if not current:
            return None, reason
        result, err = perform_action(page_src, payload)
        if err:
            return None, err
        item = result.get("item") or ""
        if item == "__all__":
            item = ""
        action = payload.get("action")
        space = "goal" if action == "draft-request" else "design"
        result["url"] = ("/_board/design?path=%s&file=%s&space=%s&item=%s"
                         % (quote(payload.get("path") or ""), quote(payload.get("file") or ""), space, quote(item)))
        return result, None


_ALLOWED = {
    "commission-release": ("not commissioned", "commission open"),
    "commission-hold": ("not commissioned", "commission open"),
    "queue-generate": ("commissioned", "revise requested"),
    "queue-revise": ("generate failed", "verify failed"),
    "queue-verify": ("generated", "verify invalid"),
    "requeue": ("queued run out of date",),
}


def perform_action(page_src: Path, payload: dict) -> tuple[dict | None, str | None]:
    """Route one action to ``live.design_actions``; refusals come back as text."""
    from live import design_actions as acts

    folder = page_src.parent
    stem = page_src.stem
    action = str(payload.get("action") or "")
    if action in {"adopt", "decline", "revise", "hold", "adopt-all", "release-all", "queue-all"}:
        return None, f"unknown action {action!r}"
    snapshot = design_snapshot(page_src, folder)
    items = {item["id"]: item for item in snapshot["items"]}
    item_id = str(payload.get("item") or "")
    actor = str(payload.get("actor") or "")
    words = str(payload.get("words") or "")
    human = snapshot.get("human", "person")
    try:
        if action == "add-item":
            out = acts.add_item(folder, stem, payload)
            return {"item": out["item"], "register": out["register"], "audit": _audit(folder)}, None
        if action == "draft-request":
            goal = snapshot["goal"]
            rows = [r for block in snapshot["insight_space"]["items"] for r in block["rows"]]
            if not rows:
                rows = [{"word": "signed insight", "path": u["name"], "signed": u["signed"], **_handoff_says(_read(u["file"]))}
                        for u in snapshot["insight_space"]["unused"] if u["signed"]]
            out = acts.request_draft(folder, stem, goal, rows, max(goal["wanted"] - goal["registered"], 0), actor or human)
            return {**out, "item": "", "audit": _audit(folder)}, None
        item = items.get(item_id)
        if item is None:
            return None, f"unknown Design Item {item_id!r}; add it to the register first"
        allowed = _ALLOWED.get(action)
        held = _held_at(item)
        if allowed is not None and item["state"] not in allowed and not (
                held == "commission" and action.startswith("commission-")):
            return None, (f'{item_id} is "{item["state"]}"; '
                          f'{"it waits on " + item["waiting"] if item["waiting"] else "nothing is waiting"}, not {action}')
        if action in ("commission-release", "commission-hold"):
            out = acts.commission(folder, stem, item, actor, words, action.split("-")[1])
        elif action == "queue-generate":
            out = acts.queue_generate(folder, stem, item, item["runs"])
        elif action == "queue-revise":
            out = acts.queue_generate(folder, stem, item, item["runs"],
                                      feedback=str(payload.get("feedback") or words or "revise"))
        elif action == "queue-verify":
            out = acts.queue_verify(folder, stem, item, item["runs"])
        elif action == "requeue":
            out = acts.requeue(folder, stem, item, item["runs"])
        else:
            return None, f"unknown action {action!r}"
    except acts.ActionError as exc:
        return None, str(exc)
    except (OSError, ValueError, KeyError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    out["item"] = item_id
    out["audit"] = _audit(folder)
    return out, None
