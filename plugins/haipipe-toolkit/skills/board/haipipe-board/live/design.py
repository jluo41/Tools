"""🎨 Design · live Page-Folder presenter for ``haipipe-plugin-design``.

It reads only the current Design Folder's contract files: the Design Item
register, ``rdNN_*`` Tickets, runtime receipts, ``checks.yaml``, content
artifacts, and ``decision.yaml``.  Every state on the page is derived from
those bytes at read time.  The only writes it exposes are the Design
contract's Commission release, the queueing of agent Tickets (Generate,
Verify), and a new register row; they live in
``live/design_actions.py`` and write exactly the contract files.
"""
from __future__ import annotations

import html
import importlib.util
import re
from pathlib import Path
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
_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_READS = re.compile(r"(?im)^\s*reads:\s*(.*?)\s*$")
_ITEM_HEAD = re.compile(r"^##\s+(ITEM\d+)\s*[·:-]\s*(.+?)\s*$")
_FIELD = re.compile(r"^([a-z][a-z-]*):\s*(.*?)\s*$")
_SIGNED = re.compile(r"(?im)^\s*signed:\s*(✅|⬜)\s*(.*?)\s*$")
_UNIT_CHECKER = (Path(__file__).resolve().parents[3] / "design"
                 / "haipipe-design-unit" / "scripts" / "check_unit.py")
_STEP = {"commission": "Commission", "generate": "Generate",
         "verify": "Verify", "adopt": "Delivery"}  # adopt is legacy storage only
_ITEM_FIELDS = ("type", "audience", "job", "goal", "stance", "basis", "mode",
                "expected", "falsified")
_ITEM_LISTS = ("acceptance", "evidence")
# contract words -> what a reader understands at first glance; the contract word stays in the files
_PLAIN = {
    ("stance", "follow"): "follows the evidence", ("stance", "challenge"): "challenges the evidence",
    ("stance", "explore"): "explores a new direction", ("stance", "generate"): "a new design",
    ("basis", "evidence-informed"): "built on evidence", ("basis", "brief-only"): "from the brief only",
    ("mode", "compose"): "written fresh", ("mode", "revise"): "revised from an earlier draft",
    ("mode", "challenge"): "written to test the evidence", ("mode", "brainstorm"): "many rough options",
    ("mode", "theory-driven"): "derived from a stated theory",
}


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
    if (folder / "pagex").exists() or re.search(r"(?im)^\s*pagex\s*:", text):
        return "legacy PageX storage is not supported"
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

def _register(folder: Path, stem: str) -> tuple[list[dict], Path]:
    """Parse ``outline/<stem>-design-items.md``: one block per Design Item.

    The register is the bet and its rules (type, audience, job, goal,
    stance, basis, mode, expected, falsified, evidence, acceptance).  State is
    never read from it; it is derived from the Runs that name the item.
    """
    path = folder / "outline" / f"{stem}-design-items.md"
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
        if not hit:
            continue
        run_id, number, kind = hit.group(1), int(hit.group(2)), hit.group(3).lower()
        ticket = _yaml(ticket_path)
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
                artifacts.append({"path": path, "text": _read(path).strip(),
                                  "sha256": str(ref.get("sha256") or "")})
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

    "agent" is waited on only while a run is queued or running; a step that
    needs a click names the person (audit H4, 260918)."""
    state, glyph, waiting = "not commissioned", "⬜", f"{human} · commission"
    for run in runs:
        owner = run["actor"] if run["actor"] != "not recorded" else human
        if run["status"] == "superseded":
            continue
        if run["status"] == "blocked":
            state, glyph, waiting = "hold", "⏸", f"{human} · {run['failure'] or 'blocked'}"
            continue
        if run["kind"] == "commission":
            if run["outcome"] == "release":
                state, glyph, waiting = "commissioned", "⬜", f"{owner} · queue the draft"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "hold", "⏸", f"{owner} · release or hold"
            else:
                state, glyph, waiting = "commission open", "⬜", f"{owner} · release or hold"
        elif run["kind"] == "generate":
            if run["status"] == "complete":
                state, glyph, waiting = "generated", "⬜", f"{human} · queue the review"
            elif run["status"] == "failed":
                state, glyph, waiting = "generate failed", "✗", f"{human} · queue a revise"
            elif run["status"] == "planned" and run.get("stale"):
                state, glyph, waiting = "queued run out of date", "⚠", f"{human} · queue again"
            elif run["status"] == "planned":
                state, glyph, waiting = "generate queued", "⬜", "agent · generate"
            else:
                state, glyph, waiting = "generating", "⬜", "agent · running"
        elif run["kind"] == "verify":
            if run["status"] == "complete" and run["verdict"] == "pass":
                state, glyph, waiting = "ready", "✅", ""
            elif run["status"] == "complete":
                state, glyph, waiting = "verify failed", "✗", f"{human} · queue a revise"
            elif run["status"] == "failed":
                # The review itself did not pass the gate: redo the review, not the candidate.
                state, glyph, waiting = "verify invalid", "✗", f"{human} · queue the review again"
            elif run["status"] == "planned" and run.get("stale"):
                state, glyph, waiting = "queued run out of date", "⚠", f"{human} · queue again"
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
                state, glyph, waiting = "generated", "⬜", f"{human} · queue the review"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "hold", "⏸", f"{owner} · release or hold"
            else:
                state, glyph, waiting = "generated", "⬜", f"{human} · queue the review"
    return state, glyph, waiting


def _audit(folder: Path) -> list[str]:
    """Run the Design Unit gate read-only; a missing checker is reported, not hidden."""
    if not _UNIT_CHECKER.is_file():
        return ["check_unit.py not found beside haipipe-design-unit"]
    try:
        spec = importlib.util.spec_from_file_location("design_unit_gate", _UNIT_CHECKER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return [str(issue).replace(str(folder) + "/", "") for issue in module.audit_folder(folder)]
    except Exception as exc:  # noqa: BLE001 - a presenter never crashes on the checker
        return [f"checker unavailable: {exc}"]


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
        text = _read(row["file"]) if row["file"].is_file() else ""
        signed = _SIGNED.search(text)
        row["exists"] = row["file"].is_file()
        row["name"] = Path(row["path"]).name
        row["signed"] = (f"signed ✅ {signed.group(2)}".strip() if signed and signed.group(1) == "✅"
                         else "unsigned ⬜" if signed else "")
        out.append(row)
    return out


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
    separate human decision.  Historical ``rdNN_adopt_*`` records may still
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
    candidate = next((r for r in reversed(runs)
                      if r["kind"] == "generate" and r["status"] == "complete"
                      and r.get("artifacts")
                      and (not target_path or target_path.startswith(f"results/{r['id']}/"))), None)
    if candidate is None:
        return None
    art = candidate["artifacts"][0]
    return {"run": candidate["id"], "text": art["text"], "sha256": art["sha256"],
            "verification": verify["id"]}


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


def _renders(folder: Path) -> dict[str, list[dict]]:
    """delivery/render/manifest.json: the rendered pictures of drafts, by item (a UI screen's picture)."""
    try:
        import json
        rows = json.loads(_read(folder / "delivery" / "render" / "manifest.json") or "[]")
    except ValueError:
        return {}
    out: dict[str, list[dict]] = {}
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict) and row.get("item") and row.get("render"):
            path = folder / "delivery" / "render" / str(row["render"])
            out.setdefault(str(row["item"]), []).append(
                {**row, "path": path, "picture": path.suffix.lower() in _PICTURE and path.is_file()})
    return out


def _render_for(rows: list[dict], run: str) -> dict | None:
    """The picture of exactly this draft; a picture of an older draft is never shown for a newer one."""
    hits = [r for r in rows if r.get("candidate") == run and r["picture"]]
    return max(hits, key=lambda r: int(r.get("version") or 0)) if hits else None


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
    renders = _renders(folder)
    for item in items:
        item["runs"] = [run for run in runs if run["item"] == item["id"]]
        item["state"], item["glyph"], item["waiting"] = _fold_state(item["runs"], human)
        item["evidence_rows"] = _evidence_rows(folder, item)
        latest = next((r for r in reversed(item["runs"])
                       if r["kind"] == "generate" and r["artifacts"] and r["status"] == "complete"), None)
        item["latest"] = ({"run": latest["id"], "text": latest["artifacts"][0]["text"],
                           "sha256": latest["artifacts"][0]["sha256"], "status": latest["status"],
                           "verdict": latest["verdict"]} if latest else None)
        # A passed Verify is the delivery gate.  Keep the old projection for
        # callers that still inspect it, but never use it as a new workflow.
        item["ready"] = _verified_design(item)
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
.act{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}.act.batch{margin:8px 0 4px;padding:8px 10px;background:var(--soft);border-radius:6px}
table.designs td.who{width:230px}.design{white-space:pre-wrap;word-break:break-word;font-size:14.5px}details.decide{margin-top:8px}details.decide .act{margin-top:6px}details.batchfold{margin:8px 0 4px}details.batchfold .act.batch{margin:6px 0 0}
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
details.itemfold>summary{list-style:none;display:flex;gap:12px;align-items:center;height:46px;cursor:pointer;color:var(--fg);font-size:14px;overflow:hidden}
details.itemfold>summary::-webkit-details-marker{display:none}details.itemfold>summary::before{content:"▸";color:var(--mut);flex:0 0 10px}
details.itemfold[open]>summary::before{content:"▾"}details.itemfold>summary:hover{background:var(--soft)}
details.itemfold>summary b{flex:0 1 auto;max-width:42%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.peek{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--mut);font-size:13px}.st{flex:0 0 auto;white-space:nowrap}
.itembody{height:560px;overflow:auto;padding:2px 8px 14px 0;border-top:1px dashed var(--line)}
.itembody .pair .pic{position:sticky;top:6px;max-height:540px;overflow:auto}
table.explain{border:1px solid var(--line);border-radius:10px;border-collapse:separate;border-spacing:0;overflow:hidden;margin:6px 0 0}table.explain th{width:160px;background:var(--soft);font-size:11px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:var(--mut);padding:12px 14px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}table.explain td{padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.5}table.explain tr:last-child th,table.explain tr:last-child td{border-bottom:0}table.explain td>.mut:first-child{margin-bottom:4px}@media(max-width:720px){table.explain th{width:110px;padding:10px}}
.explain p.goal{margin:0 0 2px;font-size:14.5px;line-height:1.5}
ol.flow{list-style:none;margin:0;padding:0}ol.flow li.lv{display:flex;gap:10px;align-items:baseline}
ol.flow .rung{flex:0 0 96px;font-size:11.5px;color:var(--mut)}ol.flow .nodes{flex:1;min-width:0}ol.flow .node{display:block;margin:1px 0;line-height:1.4}
ol.flow li.down{padding-left:118px;color:var(--mut);font-size:12px;line-height:1.2}ol.flow li.me .rung{color:var(--acc);font-weight:600}
.betl{display:flex;gap:10px;margin:2px 0;line-height:1.45}.betl .k{flex:0 0 64px;font-size:12px;font-weight:600}
ul.checks{list-style:none;margin:0;padding:0}ul.checks li{margin:2px 0;padding-left:20px;text-indent:-20px;line-height:1.4}ul.checks .g{display:inline-block;width:20px;text-indent:0;font-weight:700}
.steps{line-height:1.8}.steps .s{white-space:nowrap;background:var(--soft);border-radius:10px;padding:1px 8px;font-size:12.5px}.steps .s.next{background:none;color:var(--acc);font-weight:600}
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


def _short(sha: str) -> str:
    return sha[:12] if sha else ""


def _signal_line(insight: dict) -> str:
    if insight["status"] == "not-declared":
        return "no Insight board declared by the owning board"
    parts = []
    for board in insight["boards"]:
        label = _escape(board["title"])
        if board["live_url"]:
            label = f'<a href="{_escape(board["live_url"])}">{label}</a>'
        parts.append(f'{label} · {len(board["bindable"])} of {len(board["handoffs"])} insights signed')
    line = " · ".join(parts)
    if insight["status"] == "blocked":
        line += ' · <span class=bad>no signed insight, design stays blocked</span>'
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
    return (f'<details><summary>draft text</summary><pre class=text>{_escape(art["text"])}</pre>'
            f'<div class=mut>sha256 <code>{_escape(_short(art["sha256"]))}</code></div></details>')


def _revise_of(run: dict) -> tuple[str, str]:
    """(base run, feedback text) when a Generate revises an earlier draft."""
    base = next((i for i in run["inputs"] if i["role"] == "base"), None)
    note = next((i for i in run["inputs"] if i["role"] == "feedback"), None)
    text = _read(note["file"]).split("\n\n", 2)[-1].strip() if note and note["file"].is_file() else ""
    return (base["run_id"] if base else "", text)


def _run_rows(root: Path, runs: list[dict], acceptance: list[str] | None = None) -> str:
    rows = []
    for run in runs:
        status = run["status"]
        status_cls = ("bad" if status in ("failed", "blocked") or (run["kind"] == "verify" and run["verdict"] == "fail")
                      else "mut" if status == "superseded" else ("ok" if status == "complete" else ""))
        status_text = "planned · queued for agent" if status == "planned" and run["mode"] == "agent" else status
        # ``adopt`` is a historical Run kind. Render it as Delivery so old
        # records remain readable without reviving the removed workflow.
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
            f'<tr><td>{_href(root, run["ticket_path"], run["id"].replace("_adopt_", "_delivery_"))}</td>'
            f'<td>{_escape(run["step"])}{(" · revise of " + _escape(base.split("_")[0])) if base else ""}</td>'
            f'<td>{_escape(run["actor"])} <span class=mut>{_escape(run["mode"])}</span></td>'
            f'<td class=mut>{_escape(run["finished"] or run["started"] or "—")}</td>'
            f'<td class="{status_cls}">{_escape(status_text)}</td><td class="{"bad" if run["verdict"] == "fail" else ""}">{_escape(outcome)}</td>'
            f'<td class=mut>{_escape(next_step)}</td></tr>'
            + (f'<tr><td></td><td colspan=6>{detail}</td></tr>' if detail else ""))
    return "".join(rows)


def _held_at(item: dict) -> str:
    """For an item on hold: the Commission that held it, else ``""``."""
    if item["state"] != "hold":
        return ""
    last = next((r for r in reversed(item["runs"]) if r["kind"] == "commission"
                 and r["status"] != "superseded"), None)
    return last["kind"] if last and last["outcome"] == "hold" else ""


def _stale_names(item: dict) -> list[str]:
    return [name for r in item["runs"] for name in r.get("stale") or []]


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
    """The Insight plugin's view of one page, when this server can serve it; '' when the
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
    linked to the Insight plugin's view of that page (JL 260918: a flow, not a list of ids).
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
        return ('<div class=mut>from the Brief only · no insight needed</div>' if item["basis"] != "evidence-informed"
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
            f'{_escape(source["id"].split("_")[0])}</span>') if source else '<span class=mut>not checked yet</span>'
    released = next((r for r in item["runs"] if r["kind"] == "commission" and r["outcome"] == "release"), None)
    if released and _bet_changed(item, released):
        head += (f' <span class=bad>· the register changed after release ({_escape(released["id"].split("_")[0])}); '
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


def _step_chain(item: dict) -> str:
    """Commission → Generate → Verify → Adopt as it happened, then who is waited on."""
    chips = []
    for r in item["runs"]:
        if r["status"] == "superseded":
            continue
        out = str(r["outcome"] or r["verdict"] or r["status"] or "")
        glyph = ("✗" if r["status"] in ("failed", "blocked") else
                 "…" if r["status"] in ("planned", "running") else
                 "✓" if out in ("release", "pass", "adopt", "complete") else
                 "✗" if out in ("fail", "failed", "decline", "blocked") else
                 "↺ revise" if out == "revise" else "⏸ hold" if out == "hold" else "…")
        who = f' {_escape(r["actor"])}' if r["mode"] == "human" else ""
        chips.append(f'<span class=s title="{_escape(r["id"].replace("_adopt_", "_delivery_"))}">{_escape(r["step"])} {glyph}{who}</span>')
    if item["waiting"]:
        chips.append(f'<span class="s next">next: {_escape(item["waiting"])}</span>')
    return " → ".join(chips) or '<span class=mut>not started</span>'


def _explain(item: dict, root: Path | None = None) -> str:
    """The right-hand side of a card, as a two-column table (JL 260918): a small label on
    the left, the content on the right: why this design, where its insight came from,
    the bet, the rules, the steps."""
    pairs = [(k, v) for k, v in (("stance", item["stance"]), ("basis", item["basis"])) if v]
    why = " · ".join(_PLAIN.get((k, v), f"{k} {_escape(v)}") for k, v in pairs)
    rows = [("Why this design",
             f'<p class=goal>{_escape(item["goal"]) or "<span class=mut>no goal recorded</span>"}</p>'
             + (f'<div class=mut>{why}</div>' if why else "")),
            ("From insight to design", _insight_flow(item, root))]
    if item["expected"] or item["falsified"]:
        bet = ""
        if item["expected"]:
            bet += f'<div class=betl><span class="k ok">expected</span>{_escape(item["expected"])}</div>'
        if item["falsified"]:
            bet += f'<div class=betl><span class="k bad">wrong if</span>{_escape(item["falsified"])}</div>'
        rows.append(("The bet", bet))
    head, rules = _rule_checks(item)
    rows.append(("Rules", f'<div class=mut>{head}</div><ul class=checks>{rules}</ul>'))
    rows.append(("Steps", f'<div class=steps>{_step_chain(item)}</div>'))
    return ("<table class=explain>" + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
            + "</table>")


_OPT_OUT = ": Reply STOP to opt-out"


def _sms_bubble(text: str) -> str:
    """The SMS as the patient sees it: the sending system puts the link just before the opt-out suffix."""
    body = _escape(text.strip())
    cut = body.rfind(_OPT_OUT)
    if cut < 0:
        return body
    return body[:cut] + ': <span class=link>link</span> ' + body[cut + 2:]


def _item_card(root: Path, item: dict, human: str, selected: bool) -> str:
    meta = " · ".join(x for x in (item["type"], item["audience"], item["job"]) if x)
    if item.get("ready"):
        ready = item["ready"]
        text, note = ready["text"], (f'ready for Delivery · <code>{_escape(ready["run"])}</code> · '
                                     f'verified by <code>{_escape(ready["verification"])}</code> · '
                                     f'sha256 <code>{_escape(_short(ready["sha256"]))}</code>')
    elif item["latest"]:
        lat = item["latest"]
        verdict = f' · {lat["verdict"]}' if lat["verdict"] and lat["status"] == "complete" else ""
        text, note = lat["text"], (f'latest draft · <code>{_escape(lat["run"])}</code> · {_escape(lat["status"])}{_escape(verdict)}'
                                   f' · sha256 <code>{_escape(_short(lat["sha256"]))}</code>')
    else:
        text, note = "", "no draft yet"
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
    actions, fold = _actions(item, human)
    facts = _explain(item, root)
    # The design on the left, its explanation on the right (JL 260918): a screen as its
    # picture, a text design (an SMS) as the message itself. The design stays in view while
    # the explanation scrolls beside it.
    pair = "<div class=pair>" if picture else '<div class="pair text">'
    if actions and fold:
        actions = (f'<details class=decide{" open" if selected else ""}><summary>{_escape(fold)}</summary>'
                   f'<div class=act>{actions}</div></details>')
    elif actions:
        actions = f'<div class=act>{actions}</div>'
    # The buttons sit under the design, in the column that stays in view (audit N6).
    body = (f'{pair}<div class=pic>{design}{actions}<div class=msg></div></div>'
            f'<div class=facts>{facts}</div></div>')
    # One fixed-height row per item that opens into a fixed-height card (JL 260918): the row
    # names the item, previews the design in one line, and says where it stands.
    peek = _escape(item["goal"]) if picture else _escape(" ".join(text.split()))
    return (
        f'<section class="item{" sel" if selected else ""}" id="item-{_escape(item["id"])}" data-item="{_escape(item["id"])}">'
        f'<details class=itemfold{" open" if selected else ""}><summary>'
        f'<b>{_escape(item["id"])} · {_escape(item["title"])}</b><span class=peek>{peek}</span>'
        f'<span class="mut st">{_escape(item["glyph"])} {_escape(item["state"])}'
        f'{(" · waiting on " + _escape(item["waiting"])) if item["waiting"] else ""}</span></summary>'
        f'<div class=itembody><div class=mut>{_escape(meta)}</div>{body}</div></details></section>'
    )


def _batch_bar(items: list[dict], human: str) -> str:
    """One row of batch buttons: each appears only when it has something to act on."""
    releasable = [i for i in items if i["state"] in ("not commissioned", "commission open")]
    queueable = [i for i in items if i["state"] in ("commissioned", "revise requested", "generated",
                                                     "verify invalid", "queued run out of date")]
    if not (releasable or queueable):
        return ""
    person = f'<input class=name name=actor placeholder="your name" value="{_escape(human if human != "person" else "")}">'
    words = '<input class=words name=words placeholder="one sentence for all of them (kept on record)">'
    parts, names = [], []
    if releasable:
        parts.append(f'<button class=do data-action=release-all>Release all · {len(releasable)}</button>')
        names.append(f"release {len(releasable)}")
    if queueable:
        parts.append(f'<button class=do data-action=queue-all>Queue all · {len(queueable)} · agent</button>')
        names.append(f"queue {len(queueable)}")
    needs_person = bool(releasable)
    bar = (f'<div class="act batch" data-item="__all__">{(person + words) if needs_person else ""}'
           + "".join(parts) + '<span class=msg></span></div>')
    if not needs_person:
        return bar
    return f'<details class=batchfold><summary>For all items at once: {", ".join(names)}</summary>{bar}</details>'


def _new_item_form(next_id: str) -> str:
    return (
        '<details class=newitem><summary>New Design Item</summary><div class=form data-item="__new__">'
        f'<label>id</label><input name=id value="{_escape(next_id)}">'
        '<label>title</label><input name=title placeholder="what is being designed, in one line">'
        '<label>type</label><input name=type value=sms placeholder="sms · ui-card · email · push · …">'
        '<label>audience</label><input name=audience placeholder="who receives it">'
        '<label>job</label><input name=job placeholder="what the recipient is trying to do">'
        '<label>goal</label><input name=goal placeholder="what this design tries to do, one sentence">'
        # plain words on screen, the contract word as the option's value (audit L2)
        '<label>approach</label><select name=stance>'
        + "".join(f'<option value={k}>{_escape(_PLAIN[("stance", k)])}</option>' for k in ("generate", "follow", "challenge", "explore"))
        + '</select>'
        '<label>built on</label><select name=basis>'
        + "".join(f'<option value={k}>{_escape(_PLAIN[("basis", k)])}</option>' for k in ("brief-only", "evidence-informed"))
        + '</select>'
        '<label>expected</label><input name=expected placeholder="what you expect a reader to do or feel (needed when the approach challenges the evidence)">'
        '<label>wrong if</label><input name=falsified placeholder="what would show the expectation wrong">'
        '<label>insights</label><textarea name=evidence placeholder="one per line: evidence · path from this folder to the insight page (other words: inspiration, reference, avoid)"></textarea>'
        '<label>rules</label><textarea name=acceptance placeholder="one rule per line. Checked by machine: ≤ N characters; a quoted phrase must appear; no \'X\' or does not say \'X\' must not; ends with \'X\'; a {PLACEHOLDER}. Anything else is judged by the reviewer."></textarea>'
        '<div class=full><button class=do data-action=add-item>Add item to register</button> <span class=msg></span></div>'
        '</div></details>'
    )


def render_design(snapshot: dict, space: str = "goal", selected_item: str = "",
                  flow_space: str | None = None, query: dict | None = None) -> str:
    """Five Spaces: Goal (the ask), Design (items), Insight (what supports them),
    Run (timeline per item), Delivery (designs whose Verify passed)."""
    root = snapshot["root"]
    page = snapshot["page"]
    items = snapshot["items"]
    human = snapshot.get("human", "person")
    aliases = {"frame": "goal", "plan": "goal", "brief": "goal", "ask": "goal",
               "intent": "design", "draft": "design", "items": "design",
               "signal": "insight", "evidence": "insight", "insights": "insight",
               "runs": "run", "shape": "run", "workflow": "run", "runtime": "run", "create": "run", "review": "run",
               "launch": "delivery", "commit": "delivery"}
    selected = aliases.get(space, space) if space else "goal"
    if selected not in ("goal", "design", "insight", "run", "delivery"):
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
        counts = _escape((f'{goal["wanted"]} wanted · ' if goal["wanted"] else "") +
                         f'{goal["registered"]} registered · {goal["ready"]} ready'
                         + (f' · {declined} declined' if declined else ""))
        if missing and request:
            counts += (f' · <span class=mut>draft request open: {request["items"]} item(s) asked by '
                       f'{_escape(request["asked_by"])} {_escape(request["asked_at"][:16])}</span>')
        elif missing and snapshot["current"] and not snapshot.get("static"):
            counts += (f' <span class=act data-item="__all__"><button class=do data-action=draft-request>'
                       f'Ask the agent to draft the missing {missing}</button><span class=msg></span></span>')
        goal_html = (
            f'<pre class=text>{_escape(goal["sentence"])}</pre>'
            '<table class=kv>'
            f'<tr><th>venue</th><td>{_escape(row["venue"])}</td></tr>'
            f'<tr><th>who</th><td>{_escape(row["audience"])}</td></tr>'
            f'<tr><th>their job</th><td>{_escape(row["job"])}</td></tr>'
            f'<tr><th>how many</th><td>{counts}</td></tr>'
            f'<tr><th>from</th><td>{_href(root, goal["brief"], goal["brief"].name)} · design tasks</td></tr>'
            '</table>')
    elif goal["brief"]:
        goal_html = (f'<div class=empty>No line in {_href(root, goal["brief"], goal["brief"].name)} names this folder yet; '
                     'add a row (audience · job · venue · designs · folder) and the goal appears here.</div>')
    else:
        goal_html = '<div class=empty>No Brief under 0-BR-brief/ on the owning board; the goal has nowhere to be read from.</div>'
    ins = snapshot["insight"]
    if ins["status"] == "not-declared":
        goal_html += '<h2>Insight board</h2><div class=mut>none declared by the owning board · this folder designs from the Brief only</div>'
    elif ins["status"] == "missing":
        goal_html += (f'<h2>Insight board</h2><div class=bad>{_escape(", ".join(ins["requested"]))} · named on the Brief line '
                      'but not found beside this board</div>')
    else:
        goal_html += f'<h2>Insight board</h2><div class={"bad" if ins["status"] == "blocked" else "mut"}>{_signal_line(ins)}</div>'

    # Design Space -----------------------------------------------------------
    design_html = _batch_bar(items, human) if (items and snapshot["current"] and not snapshot.get("static")) else ""
    if items:
        # A declined item is retired: its card stays for the record, folded after the live ones.
        live = [item for item in items if item["state"] != "declined"]
        retired = [item for item in items if item["state"] == "declined"]
        design_html += ('<div class="mut foldbar"><a href=# data-fold=open>open all</a> · '
                        '<a href=# data-fold=close>close all</a></div>')
        design_html += "".join(_item_card(root, item, human, item["id"] == selected_item) for item in live)
        if retired:
            opened = " open" if selected_item in {item["id"] for item in retired} else ""
            design_html += (f'<details class=retired{opened}><summary>Declined, kept for the record · {len(retired)}</summary>'
                            + "".join(_item_card(root, item, human, item["id"] == selected_item) for item in retired)
                            + '</details>')
    else:
        design_html = (f'<div class=empty>No Design Item register yet. Add the first item below; it writes '
                       f'<code>{_escape(snapshot["register"].relative_to(snapshot["folder"]).as_posix())}</code>.</div>')
    if snapshot["unassigned"]:
        design_html += ('<h2>Runs without an item</h2>'
                        '<table><tr><th>run</th><th>step</th><th>who</th><th>when</th><th>status</th><th>outcome</th><th>next</th></tr>'
                        f'{_run_rows(root, snapshot["unassigned"])}</table>')
    if snapshot["current"]:
        numbers = [int(i[4:]) for i in ids if i[4:].isdigit()]
        design_html += _new_item_form(f"ITEM{max(numbers, default=0) + 1:02d}")

    # Insight Space ----------------------------------------------------------
    narrowed = ""
    if selected_item and q.get("path") and q.get("file"):
        base = f'?path={quote(str(q["path"]), safe="")}&amp;file={quote(str(q["file"]), safe="")}'
        narrowed = (f'<div class=mut>showing {_escape(selected_item)} only · '
                    f'<a href="{base}&amp;space=SPACE">show every item</a></div>')
    insight_html = [narrowed.replace("SPACE", "insight")] if narrowed else []
    for block in snapshot["insight_space"]["items"]:
        item = block["item"]
        if selected_item and item["id"] != selected_item:
            continue
        insight_html.append(f'<h2>{_escape(item["id"])} · {_escape(item["title"])}</h2>')
        if block["needed"]:
            insight_html.append('<div class=bad>built on evidence, but no insight is named yet · add an evidence line to the register</div>')
        elif not block["rows"]:
            insight_html.append('<div class=mut>Brief only · no insight needed</div>')
        else:
            insight_html.append('<table><tr><th>insight</th><th>signed</th><th>what it says</th><th>pinned</th></tr>' + "".join(
                f'<tr><td>{_page_name(root, r) if r["exists"] else "<code class=bad>" + _escape(r["name"]) + " missing</code>"}'
                f'<div class=mut>{_escape(r["word"])} · {_escape(insight_caption(r["file"]))}</div></td>'
                f'<td>{_escape(r["signed"]) if r["signed"] else "<span class=mut>—</span>"}</td>'
                f'<td>{name_refs(_escape(r["finding"]), r["file"]) if r["finding"] else "<span class=mut>—</span>"}'
                f'{("<div class=mut>then: " + name_refs(_escape(r["consequence"]), r["file"]) + "</div>") if r["consequence"] else ""}'
                f'{("<div class=mut>rules it implies: " + " · ".join(("DO " if c["do"] else "DO NOT ") + name_refs(_escape(c["text"]), r["file"]) for c in r["counsel"]) + "</div>") if r.get("counsel") else ""}</td>'
                f'<td>{"in the run record" if r["pinned"] else "<span class=mut>not yet</span>"}</td></tr>'
                for r in block["rows"]) + '</table>')
    if not insight_html:
        insight_html.append('<div class=empty>No Design Item yet, so nothing to support.</div>')
    unused = snapshot["insight_space"]["unused"]
    if not unused and not selected_item and snapshot["insight"]["boards"]:
        insight_html.append('<h2>Available, unused</h2><div class=mut>none · every signed insight is used by an item</div>')
    if unused and not selected_item:
        insight_html.append('<h2>Available, unused</h2><div class=mut>' + " · ".join(
            f'{_href(root, u["file"], insight_label(u["file"])["words"])} ({_escape(insight_caption(u["file"]))}) {"✅ " + _escape(u["signed"]) if u["signed"] else "⬜ unsigned"}'
            for u in unused) + '</div>')

    # Run Space --------------------------------------------------------------
    run_html = [narrowed.replace("SPACE", "run")] if narrowed else []
    for item in items:
        if selected_item and item["id"] != selected_item:
            continue
        run_html.append(f'<h2>{_escape(item["id"])} · {_escape(item["title"])} '
                        f'<span class=mut>{_escape(item["glyph"])} {_escape(item["state"])}'
                        f'{(" · waiting on " + _escape(item["waiting"])) if item["waiting"] else ""}</span></h2>')
        if item["runs"]:
            run_html.append('<table><tr><th>run</th><th>step</th><th>who</th><th>when</th>'
                            f'<th>status</th><th>outcome</th><th>next</th></tr>{_run_rows(root, item["runs"], item["acceptance"])}</table>')
        else:
            run_html.append('<div class=empty>No Run yet. The first Run is a Commission a person releases.</div>')
    if not items and snapshot["runs"]:
        run_html.append('<table><tr><th>run</th><th>step</th><th>who</th><th>when</th><th>status</th><th>outcome</th><th>next</th></tr>'
                        f'{_run_rows(root, snapshot["runs"])}</table>')
    if not run_html:
        run_html.append('<div class=empty>No Design Run records are present in this folder.</div>')
    audit = snapshot["audit"]
    if snapshot["current"]:
        if audit:
            run_html.append(f'<details><summary class=bad>records check: {len(audit)} finding(s)</summary><ul class=rules>'
                            + "".join(f"<li><code>{_escape(issue)}</code></li>" for issue in audit) + '</ul></details>')
        else:
            run_html.append('<div class="mut ok">records check: PASS · every run has its result and receipt</div>')

    # Delivery Space ---------------------------------------------------------
    # A quick overview of what is ready to hand to the next team: one row per
    # item whose independent Verify passed.
    def listing(group: list[dict]) -> str:
        rows, tiles = [], []
        for item in (item for item in group if item.get("ready")):
            design = item.get("ready")
            label = _escape(item["id"])
            if q.get("path") and q.get("file"):
                label = (f'<a href="?path={quote(str(q["path"]), safe="")}&amp;file={quote(str(q["file"]), safe="")}'
                         f'&amp;space=design&amp;item={_escape(item["id"])}">{label}</a>')
            text_html = (_sms_bubble(design["text"]) if design and (item["type"] or "").lower() == "sms"
                         else _escape(design["text"]) if design else "")
            body = (f"<div class=design>{text_html}</div>" if design else "<span class=mut>not ready for Delivery yet</span>")
            rows.append(f'<tr><td class=who><b>{label}</b><div class=mut>{_escape(item["title"])}</div></td><td>{body}</td></tr>')
            tiles.append(f'<figure>{design_picture(root, item) or body}'
                         f'<figcaption><b>{label}</b> {_escape(item["title"])}</figcaption></figure>')
        if any(item.get("render") and item.get("ready") for item in group):
            # Screens read side by side as pictures; text designs keep the table.
            return f'<div class=gallery>{"".join(tiles)}</div>'
        return ('<table class=designs><tr><th>item</th><th>design</th></tr>' + "".join(rows) + '</table>') if rows else ""

    # A declined item is retired, like a retired Evidence Item: kept for the record, out of the overview.
    live = [item for item in items if item["state"] != "declined"]
    retired = [item for item in items if item["state"] == "declined"]
    delivery_html = [listing(live) or '<div class=empty>No design is ready yet. A design appears here after Verify passes.</div>']
    if retired:
        delivery_html.append(f'<details class=retired><summary>Declined, kept for the record · {len(retired)}</summary>'
                             f'{listing(retired)}</details>')

    panes = {"goal": goal_html, "design": design_html, "insight": "".join(insight_html),
             "run": "".join(run_html), "delivery": "".join(delivery_html)}
    tabs = "".join(f'<button type=button data-space="{key}"{" class=on" if key == selected else ""}>{label}</button>'
                   for key, label in (("goal", "Goal Space"), ("design", "Design Space"), ("insight", "Insight Space"),
                                      ("run", "Run Space"), ("delivery", "Delivery Space")))
    pane_html = "".join(f'<section class="pane{" on" if key == selected else ""}" data-space="{key}">{value}</section>'
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
        f'<title>🎨 Design · {_escape(snapshot["title"])}</title><style>{_CSS}</style></head><body>'
        f'<header>{header}</header><nav class=tabs>{tabs}</nav><main>{pane_html}</main>{script}</body></html>'
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
    if action in {"adopt", "decline", "revise", "hold", "adopt-all"}:
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
        if action == "release-all":
            out = acts.release_all(folder, stem, snapshot["items"], actor, words)
            return {**out, "item": "", "audit": _audit(folder)}, None
        if action == "queue-all":
            out = acts.queue_all(folder, stem, snapshot["items"])
            return {**out, "item": "", "audit": _audit(folder)}, None
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
