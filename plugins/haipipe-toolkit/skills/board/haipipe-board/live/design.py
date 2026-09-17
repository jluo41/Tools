"""🎨 Design · live Page-Folder presenter for ``haipipe-plugin-design``.

It reads only the current Design Folder's contract files: the Design Item
register, ``rdNN_*`` Tickets, runtime receipts, ``checks.yaml``, content
artifacts, and ``decision.yaml``.  Every state on the page is derived from
those bytes at read time.  The only writes it exposes are the Design
contract's own human decisions (Commission, Adopt), the queueing of agent
Tickets (Generate, Verify), and a new register row; they live in
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

from live.insightboard import handoff_records, is_insight_board


_DESIGN_MARKER = re.compile(r"(?m)^\s*folder-kind:\s*design\s*$", re.I)
_LEGACY_RUN = re.compile(r"^r\d+_design(?:_|$)", re.I)
_RUN_FILE = re.compile(
    r"^(rd(\d+)_(commission|generate|verify|adopt)_[A-Za-z0-9][A-Za-z0-9_-]*)\.ya?ml$", re.I)
_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_READS = re.compile(r"(?im)^\s*reads:\s*(.*?)\s*$")
_ITEM_HEAD = re.compile(r"^##\s+(ITEM\d+)\s*[·:-]\s*(.+?)\s*$")
_FIELD = re.compile(r"^([a-z][a-z-]*):\s*(.*?)\s*$")
_SIGNED = re.compile(r"(?im)^\s*signed:\s*(✅|⬜)\s*(.*?)\s*$")
_UNIT_CHECKER = (Path(__file__).resolve().parents[3] / "application"
                 / "haipipe-design-unit" / "scripts" / "check_unit.py")
_STEP = {"commission": "Commission", "generate": "Generate",
         "verify": "Verify", "adopt": "Adopt"}
_ITEM_FIELDS = ("type", "audience", "job", "goal", "stance", "basis", "mode",
                "expected", "falsified")
_ITEM_LISTS = ("acceptance", "evidence")
# contract words -> what a reader understands at first glance (the contract word stays in parentheses)
_PLAIN = {
    ("stance", "follow"): "follows the evidence", ("stance", "challenge"): "challenges the evidence",
    ("stance", "explore"): "explores a new direction", ("stance", "generate"): "new design from the brief",
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
        config_ref = ticket.get("config") if isinstance(ticket.get("config"), dict) else {}
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
            "failure": str(runtime.get("failure") or ""),
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
            "ticket_path": ticket_path, "result_dir": result_dir,
        })
    rows.sort(key=lambda row: row["number"])
    return rows


def _fold_state(runs: list[dict], human: str = "person") -> tuple[str, str, str]:
    """Walk an item's Runs in order and return (state, glyph, waiting-on)."""
    state, glyph, waiting = "not commissioned", "⬜", f"{human} · commission"
    for run in runs:
        owner = run["actor"] if run["actor"] != "not recorded" else human
        if run["status"] == "blocked":
            state, glyph, waiting = "hold", "⏸", f"{human} · {run['failure'] or 'blocked'}"
            continue
        if run["kind"] == "commission":
            if run["outcome"] == "release":
                state, glyph, waiting = "commissioned", "⬜", "agent · generate"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "hold", "⏸", f"{owner} · commission"
            else:
                state, glyph, waiting = "commission open", "⬜", f"{owner} · release or hold"
        elif run["kind"] == "generate":
            if run["status"] == "complete":
                state, glyph, waiting = "generated", "⬜", "agent · verify"
            elif run["status"] == "failed":
                state, glyph, waiting = "generate failed", "✗", "agent · revise"
            elif run["status"] == "planned":
                state, glyph, waiting = "generate queued", "⬜", "agent · generate"
            else:
                state, glyph, waiting = "generating", "⬜", "agent · running"
        elif run["kind"] == "verify":
            if run["status"] == "complete" and run["verdict"] == "pass":
                state, glyph, waiting = "verified", "⬜", f"{human} · adopt"
            elif run["status"] == "complete":
                state, glyph, waiting = "verify failed", "✗", "agent · revise"
            elif run["status"] == "failed":
                # The review itself did not pass the gate: redo the review, not the candidate.
                state, glyph, waiting = "verify invalid", "✗", "agent · verify"
            elif run["status"] == "planned":
                state, glyph, waiting = "verify queued", "⬜", "agent · verify"
            else:
                state, glyph, waiting = "verifying", "⬜", "agent · running"
        elif run["kind"] == "adopt":
            if run["outcome"] == "adopt":
                state, glyph, waiting = "adopted", "✅", ""
            elif run["outcome"] == "decline":
                state, glyph, waiting = "declined", "🚫", ""
            elif run["outcome"] == "revise":
                state, glyph, waiting = "revise requested", "⬜", "agent · generate"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "hold", "⏸", f"{owner} · adopt"
            else:
                state, glyph, waiting = "adoption open", "⬜", f"{owner} · adopt"
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
    for line in item["evidence"]:
        parts = [p.strip() for p in re.split(r"\s*·\s*", line, maxsplit=1)]
        role, rel = (parts[0], parts[1]) if len(parts) == 2 else ("evidence", parts[0])
        rows[rel] = {"role": role, "path": rel, "file": (folder / rel).resolve(), "pinned": False}
    for run in item["runs"]:
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


def brief_rows(brief_text: str) -> list[dict]:
    """The Brief's list: one line per audience × job × venue, columns matched by header word.

    The first Markdown table whose header names ``audience`` is the list.  A
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
            if any("audience" in c.lower() for c in cells):
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


def _goal(folder: Path, board_root: Path | None, items: list[dict]) -> dict:
    """Goal Space: the Brief line that names this folder, and the counts against it."""
    brief = brief_page(board_root)
    rows = brief_rows(_read(brief)) if brief else []
    row = next((r for r in rows if r["folder"] == folder.name), None)
    sentence = ""
    if row:
        wanted = row["designs"]
        head = (f"{wanted} {row['venue']} design{'s' if wanted != 1 else ''}" if wanted
                else f"{row['venue']} designs")
        sentence = f"{head} for {row['audience']}, {row['job']}"
    return {"brief": brief, "row": row, "sentence": sentence, "insight": row["insight"] if row else "",
            "wanted": row["designs"] if row else 0, "registered": len(items),
            "adopted": sum(1 for i in items if i["adopted"])}


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
        opening = re.search(r"(?ms)^## Opening\s*\n(.*?)(?=^## |\Z)", text)
        if opening:
            first = next((l.strip() for l in opening.group(1).splitlines() if l.strip()), "")
            out["finding"] = first
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
    for item in items:
        item["runs"] = [run for run in runs if run["item"] == item["id"]]
        item["state"], item["glyph"], item["waiting"] = _fold_state(item["runs"], human)
        item["evidence_rows"] = _evidence_rows(folder, item)
        latest = next((r for r in reversed(item["runs"]) if r["kind"] == "generate" and r["artifacts"]), None)
        item["latest"] = ({"run": latest["id"], "text": latest["artifacts"][0]["text"],
                           "sha256": latest["artifacts"][0]["sha256"], "status": latest["status"],
                           "verdict": latest["verdict"]} if latest else None)
        adopt = next((r for r in reversed(item["runs"]) if r["kind"] == "adopt" and r["outcome"] == "adopt"), None)
        item["adopted"] = None
        if adopt:
            cand = adopt["candidate"]
            source = next((r for r in runs if r["id"] == cand.get("run")), None)
            text_out = ""
            if source and source["artifacts"]:
                text_out = source["artifacts"][0]["text"]
            elif cand.get("path"):
                text_out = _read(folder / str(cand["path"])).strip()
            item["adopted"] = {
                "run": adopt["id"], "actor": adopt["actor"], "when": adopt["finished"],
                "words": adopt["words"], "candidate": cand.get("run", ""),
                "sha256": str(cand.get("sha256") or ""), "text": text_out,
                "verification": adopt["verification"].get("run", ""),
                "preview": str(adopt["preview"].get("path") or ""),
            }
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
.act input,.act textarea,.form input,.form textarea,.form select{font:13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:4px;padding:4px 6px;background:var(--bg);color:var(--fg)}
.act input.name{width:90px}.act input.words{width:min(420px,100%)}
button.do{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);border-radius:4px;padding:4px 10px;background:var(--bg);color:var(--acc);cursor:pointer}
button.do:hover{background:var(--soft)}button.do.bad{border-color:var(--bad);color:var(--bad)}
.msg{font-size:12.5px;margin-top:4px}.msg.bad{color:var(--bad)}.msg.ok{color:var(--ok)}
.form{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;max-width:760px;margin:6px 0}.form label{color:var(--mut);font-size:12px;padding-top:5px}
.form textarea{min-height:56px}.form .full{grid-column:1/3}
.empty{color:var(--mut);padding:10px 0}
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


def _checks_details(run: dict) -> str:
    if not run["checks"]:
        return ""
    rows = "".join(
        f'<tr><td><code>{_escape(c.get("criterion"))}</code></td>'
        f'<td class="{"ok" if c.get("status") == "pass" else "bad"}">{_escape(c.get("status"))}</td>'
        f'<td class=mut>{_escape(c.get("evidence"))}</td></tr>'
        for c in run["checks"])
    return (f'<details><summary>checks {run["checks_passed"]}/{len(run["checks"])}</summary>'
            f'<table><tr><th>criterion</th><th>status</th><th>evidence</th></tr>{rows}</table></details>')


def _artifact_details(run: dict) -> str:
    if not run["artifacts"]:
        return ""
    art = run["artifacts"][0]
    return (f'<details><summary>draft text</summary><pre class=text>{_escape(art["text"])}</pre>'
            f'<div class=mut>sha256 <code>{_escape(_short(art["sha256"]))}</code></div></details>')


def _run_rows(root: Path, runs: list[dict]) -> str:
    rows = []
    for run in runs:
        status = run["status"]
        status_cls = "bad" if status in ("failed", "blocked") else ("ok" if status == "complete" else "")
        status_text = "planned · queued for agent" if status == "planned" and run["mode"] == "agent" else status
        outcome = run["outcome"]
        if run["kind"] in ("generate", "verify") and run["checks"]:
            outcome = f'{run["verdict"] or status} {run["checks_passed"]}/{len(run["checks"])}'
        next_step = run["route"] or ""
        if run["status"] == "complete" and run["kind"] == "adopt" and run["outcome"] in ("adopt", "decline"):
            next_step = "closed"
        detail = _checks_details(run) + _artifact_details(run)
        if run["failure"]:
            detail = f'<div class=bad>{_escape(run["failure"])}</div>' + detail
        if run["words"]:
            detail = f'<div class=mut>“{_escape(run["words"])}”</div>' + detail
        rows.append(
            f'<tr><td>{_href(root, run["ticket_path"], run["id"])}</td><td>{_escape(run["step"])}</td>'
            f'<td>{_escape(run["actor"])} <span class=mut>{_escape(run["mode"])}</span></td>'
            f'<td class=mut>{_escape(run["finished"] or run["started"] or "—")}</td>'
            f'<td class="{status_cls}">{_escape(status_text)}</td><td>{_escape(outcome)}</td>'
            f'<td class=mut>{_escape(next_step)}</td></tr>'
            + (f'<tr><td></td><td colspan=6>{detail}</td></tr>' if detail else ""))
    return "".join(rows)


def _actions(item: dict, human: str) -> str:
    """The buttons an item's state licenses: the two human gates, the agent queue."""
    state = item["state"]
    person = f'<input class=name name=actor placeholder="your name" value="{_escape(human if human != "person" else "")}">'
    words = '<input class=words name=words placeholder="your words, one sentence (kept on record)">'
    feedback = '<input class=words name=feedback placeholder="what to change (feedback for the revise Run)">'
    if state in ("not commissioned", "commission open"):
        return (f'{person}{words}<button class=do data-action=commission-release>Release commission</button>'
                f'<button class="do bad" data-action=commission-hold>Hold</button>')
    if state in ("commissioned", "revise requested"):
        return '<button class=do data-action=queue-generate>Queue Generate · agent</button>'
    if state in ("generated",):
        return '<button class=do data-action=queue-verify>Queue Verify · independent agent</button>'
    if state in ("generate failed", "verify failed"):
        return f'{feedback}<button class=do data-action=queue-revise>Queue revise · agent</button>'
    if state == "verified":
        return (f'{person}{words}<button class=do data-action=adopt>Adopt</button>'
                f'<button class="do bad" data-action=decline>Decline</button>'
                f'<button class=do data-action=revise>Revise</button>'
                f'<button class=do data-action=hold>Hold</button>')
    if state in ("generate queued", "verify queued", "generating", "verifying"):
        return '<span class=mut>queued for the agent</span>'
    return ""


def _item_card(root: Path, item: dict, human: str, selected: bool) -> str:
    meta = " · ".join(x for x in (item["type"], item["audience"], item["job"]) if x)
    if item["adopted"]:
        text, note = item["adopted"]["text"], (f'adopted · <code>{_escape(item["adopted"]["candidate"])}</code> · '
                                              f'sha256 <code>{_escape(_short(item["adopted"]["sha256"]))}</code>')
    elif item["latest"]:
        lat = item["latest"]
        verdict = f' · {lat["verdict"]}' if lat["verdict"] else ""
        text, note = lat["text"], (f'latest draft · <code>{_escape(lat["run"])}</code> · {_escape(lat["status"])}{_escape(verdict)}'
                                   f' · sha256 <code>{_escape(_short(lat["sha256"]))}</code>')
    else:
        text, note = "", "no draft yet"
    design = (f'<pre class=text>{_escape(text)}</pre>' if text else "") + f'<div class=mut>{note}</div>'
    goal = _escape(item["goal"]) or "<span class=mut>no goal recorded</span>"
    pairs = [(k, v) for k, v in (("stance", item["stance"]), ("basis", item["basis"])) if v]
    bet = " · ".join(_PLAIN.get((k, v), f"{k} {_escape(v)}") for k, v in pairs)
    if pairs:
        bet += f' <span class=mut>({" · ".join(_escape(v) for _, v in pairs)})</span>'
    if item["evidence_rows"]:
        pointer = " · ".join(
            f'{_escape(Path(r["name"]).stem)} {"✅" if r["signed"].startswith("signed") else "⬜" if r["signed"] else ""}'.strip()
            + ("" if r["exists"] else ' <span class=bad>missing</span>')
            for r in item["evidence_rows"])
        insight_cell = f'supported by {pointer} <span class=mut>· see Insight Space</span>'
    else:
        insight_cell = ('<span class=mut>Brief only · no insight needed</span>' if item["basis"] != "evidence-informed"
                        else '<span class=bad>needs an insight · none named yet</span>')
    predict = ""
    if item["expected"]:
        predict += f'expected: {_escape(item["expected"])}'
    if item["falsified"]:
        predict += f'{"<br>" if predict else ""}falsified if: {_escape(item["falsified"])}'
    predict = predict or '<span class=mut>no forecast · legal for compose, required for challenge/theory-driven</span>'
    rules = "".join(f"<li>{_escape(r)}</li>" for r in item["acceptance"]) or "<li class=mut>none</li>"
    runs = " · ".join(
        f'<code>{_escape(r["id"].split("_")[0])}</code> {_escape(r["step"])} '
        f'{_escape(r["outcome"] or r["status"])}' for r in item["runs"]) or '<span class=mut>none yet</span>'
    actions = _actions(item, human)
    return (
        f'<section class="item{" sel" if selected else ""}" id="item-{_escape(item["id"])}" data-item="{_escape(item["id"])}">'
        f'<div class=head><b>{_escape(item["id"])} · {_escape(item["title"])}</b>'
        f'<span class=mut>{_escape(item["glyph"])} {_escape(item["state"])}'
        f'{(" · waiting on " + _escape(item["waiting"])) if item["waiting"] else ""}</span></div>'
        f'<div class=mut>{_escape(meta)}</div>{design}'
        f'<table class=kv>'
        f'<tr><th>goal</th><td>{goal}</td></tr>'
        f'{("<tr><th>why</th><td>" + bet + "</td></tr>") if bet else ""}'
        f'<tr><th>insight</th><td>{insight_cell}</td></tr>'
        f'<tr><th>predict</th><td>{predict}</td></tr>'
        f'<tr><th>rules</th><td><ul class=rules>{rules}</ul></td></tr>'
        f'<tr><th>runs</th><td>{runs}</td></tr></table>'
        f'{("<div class=act>" + actions + "</div>") if actions else ""}<div class=msg></div></section>'
    )


def _batch_bar(items: list[dict], human: str) -> str:
    """One row of batch buttons: each appears only when it has something to act on."""
    releasable = [i for i in items if i["state"] in ("not commissioned", "commission open")]
    queueable = [i for i in items if i["state"] in ("commissioned", "revise requested", "generated")]
    adoptable = [i for i in items if i["state"] == "verified"]
    if not (releasable or queueable or adoptable):
        return ""
    person = f'<input class=name name=actor placeholder="your name" value="{_escape(human if human != "person" else "")}">'
    words = '<input class=words name=words placeholder="one sentence for all of them (kept on record)">'
    parts = []
    if releasable:
        parts.append(f'<button class=do data-action=release-all>Release all · {len(releasable)}</button>')
    if queueable:
        parts.append(f'<button class=do data-action=queue-all>Queue all · {len(queueable)} · agent</button>')
    if adoptable:
        parts.append(f'<button class=do data-action=adopt-all>Adopt all verified · {len(adoptable)}</button>')
    needs_person = bool(releasable or adoptable)
    return (f'<div class="act batch" data-item="__all__">{(person + words) if needs_person else ""}'
            + "".join(parts) + '<span class=msg></span></div>')


def _new_item_form(next_id: str) -> str:
    return (
        '<details class=newitem><summary>New Design Item</summary><div class=form data-item="__new__">'
        f'<label>id</label><input name=id value="{_escape(next_id)}">'
        '<label>title</label><input name=title placeholder="what is being designed, in one line">'
        '<label>type</label><input name=type value=sms placeholder="sms · ui-card · email · push · …">'
        '<label>audience</label><input name=audience placeholder="who receives it">'
        '<label>job</label><input name=job placeholder="what the recipient is trying to do">'
        '<label>goal</label><input name=goal placeholder="what this design tries to do, one sentence">'
        '<label>stance</label><select name=stance><option>generate</option><option>follow</option><option>challenge</option><option>explore</option></select>'
        '<label>basis</label><select name=basis><option>brief-only</option><option>evidence-informed</option></select>'
        '<label>expected</label><input name=expected placeholder="what you predict will happen, for whom">'
        '<label>falsified</label><input name=falsified placeholder="what result would prove it wrong">'
        '<label>evidence</label><textarea name=evidence placeholder="one per line: role · relative/path (roles: evidence handoff inspiration reference avoid)"></textarea>'
        '<label>acceptance</label><textarea name=acceptance placeholder="one rule per line; ≤ N characters, quoted must-contain text and {PLACEHOLDER}s become mechanical checks"></textarea>'
        '<div class=full><button class=do data-action=add-item>Add item to register</button> <span class=msg></span></div>'
        '</div></details>'
    )


def render_design(snapshot: dict, space: str = "goal", selected_item: str = "",
                  flow_space: str | None = None, query: dict | None = None) -> str:
    """Five Spaces: Goal (the ask), Design (items), Insight (what supports them),
    Run (timeline per item), Delivery (adopted)."""
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
        counts = (f'{goal["wanted"]} wanted · ' if goal["wanted"] else "") + \
                 f'{goal["registered"]} registered · {goal["adopted"]} adopted'
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
            f'<tr><th>how many</th><td>{_escape(counts)}</td></tr>'
            f'<tr><th>from</th><td>{_href(root, goal["brief"], goal["brief"].name)} · line {_escape(row["id"])}</td></tr>'
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
        design_html += "".join(_item_card(root, item, human, item["id"] == selected_item) for item in items)
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
    insight_html = []
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
                f'<tr><td>{_escape(r["word"])} · {_href(root, r["file"], r["name"]) if r["exists"] else "<code class=bad>" + _escape(r["name"]) + " missing</code>"}</td>'
                f'<td>{_escape(r["signed"]) if r["signed"] else "<span class=mut>—</span>"}</td>'
                f'<td>{_escape(r["finding"]) if r["finding"] else "<span class=mut>—</span>"}'
                f'{("<div class=mut>then: " + _escape(r["consequence"]) + "</div>") if r["consequence"] else ""}'
                f'{("<div class=mut>rules it implies: " + " · ".join(("DO " if c["do"] else "DO NOT ") + _escape(c["text"]) for c in r["counsel"]) + "</div>") if r.get("counsel") else ""}</td>'
                f'<td>{"in the run record" if r["pinned"] else "<span class=mut>not yet</span>"}</td></tr>'
                for r in block["rows"]) + '</table>')
    if not insight_html:
        insight_html.append('<div class=empty>No Design Item yet, so nothing to support.</div>')
    unused = snapshot["insight_space"]["unused"]
    if unused and not selected_item:
        insight_html.append('<h2>Available, unused</h2><div class=mut>' + " · ".join(
            f'{_href(root, u["file"], u["name"])} {"✅ " + _escape(u["signed"]) if u["signed"] else "⬜ unsigned"}'
            for u in unused) + '</div>')

    # Run Space --------------------------------------------------------------
    run_html = []
    for item in items:
        if selected_item and item["id"] != selected_item:
            continue
        run_html.append(f'<h2>{_escape(item["id"])} · {_escape(item["title"])} '
                        f'<span class=mut>{_escape(item["glyph"])} {_escape(item["state"])}'
                        f'{(" · waiting on " + _escape(item["waiting"])) if item["waiting"] else ""}</span></h2>')
        if item["runs"]:
            run_html.append('<table><tr><th>run</th><th>step</th><th>who</th><th>when</th>'
                            f'<th>status</th><th>outcome</th><th>next</th></tr>{_run_rows(root, item["runs"])}</table>')
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
    delivery_html = []
    for item in items:
        adopted = item["adopted"]
        if adopted:
            delivery_html.append(
                f'<div class=card><div class=head><b>{_escape(item["id"])} · {_escape(item["title"])}</b>'
                f'<span class=mut>✅ adopted · {_escape(adopted["actor"])} · {_escape(adopted["when"])}</span></div>'
                f'<pre class=text>{_escape(adopted["text"] or "(draft text not readable)")}</pre>'
                f'<div class=mut>draft <code>{_escape(adopted["candidate"])}</code> · sha256 <code>{_escape(_short(adopted["sha256"]))}</code>'
                f' · verified by <code>{_escape(adopted["verification"] or "—")}</code>'
                f'{(" · preview <code>" + _escape(Path(adopted["preview"]).name) + "</code>") if adopted["preview"] else ""}</div>'
                f'{("<div class=mut>“" + _escape(adopted["words"]) + "”</div>") if adopted["words"] else ""}</div>')
        else:
            delivery_html.append(f'<div class=mut>{_escape(item["id"])} · {_escape(item["title"])} · not adopted · '
                                 f'{_escape(item["glyph"])} {_escape(item["state"])}'
                                 f'{(" · waiting on " + _escape(item["waiting"])) if item["waiting"] else ""}</div>')
    if not delivery_html:
        delivery_html.append('<div class=empty>Nothing adopted. Adoption is a person\'s decision Run.</div>')

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


class DesignMixin:
    """GET/HEAD/POST surface for a current Design Page-Folder."""

    def design_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        short = (query.pop("folder", None) or [""])[0].strip("/")
        if short and not query.get("file"):
            # short link: ?folder=Design-01-… names the Design Folder; the board is the one given or the only one
            from urllib.parse import urlencode
            from live.designboard import DESIGN_GROUP, resolve_board
            root = Path(self.root)
            board = resolve_board(root, (query.get("path") or query.pop("board", None) or [""])[0])
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
        modern = modern_file(payload["file"])
        if modern != payload["file"]:
            # an old bookmark: send the browser to the full-name path so the URL updates too
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
        space = ("design" if action in ("add-item", "release-all") else "goal" if action == "draft-request"
                 else "delivery" if action == "adopt-all" else "run")
        result["url"] = ("/_board/design?path=%s&file=%s&space=%s&item=%s"
                         % (quote(payload.get("path") or ""), quote(payload.get("file") or ""), space, quote(item)))
        return result, None


def perform_action(page_src: Path, payload: dict) -> tuple[dict | None, str | None]:
    """Route one action to ``live.design_actions``; refusals come back as text."""
    from live import design_actions as acts

    folder = page_src.parent
    stem = page_src.stem
    action = str(payload.get("action") or "")
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
        if action == "adopt-all":
            out = acts.adopt_all(folder, stem, snapshot["items"], actor, words)
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
        if action in ("commission-release", "commission-hold"):
            out = acts.commission(folder, stem, item, actor, words, action.split("-")[1])
        elif action == "queue-generate":
            out = acts.queue_generate(folder, stem, item, item["runs"])
        elif action == "queue-revise":
            out = acts.queue_generate(folder, stem, item, item["runs"],
                                      feedback=str(payload.get("feedback") or words or "revise"))
        elif action == "queue-verify":
            out = acts.queue_verify(folder, stem, item, item["runs"])
        elif action in ("adopt", "decline", "revise", "hold"):
            out = acts.adopt(folder, stem, item, item["runs"], action, actor, words)
        else:
            return None, f"unknown action {action!r}"
    except acts.ActionError as exc:
        return None, str(exc)
    except (OSError, ValueError, KeyError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    out["item"] = item_id
    out["audit"] = _audit(folder)
    return out, None
