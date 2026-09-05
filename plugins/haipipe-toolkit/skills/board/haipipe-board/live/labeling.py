"""🏷 Labeling · live, receipt-first view of one page-local labeling/ job.

The surface is deliberately read-only.  It reports metadata from canonical
artifacts, never protected item text, and it never upgrades an observed file
to a passed gate.  The embedded page chat is transport; the subjective-label
workflow remains the only writer of labeling events and receipts.
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
from functools import lru_cache
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, quote, unquote, urlparse

from src.body import group_token
from src.parse import parse_dir


PHASES = (
    ("P0", "Contract"), ("P1", "Round"), ("P2", "Freeze"),
    ("P3", "Test"), ("P4", "Scan"), ("P5", "Audit"),
)

P0_FILES = (
    "config.yaml", "corpus/manifest.json", "test/sealed/status.json",
    "register.md", "policy/versions/G_00/manifest.yaml",
)


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def _yaml_scalar(path: Path, key: str) -> str:
    """Read one simple YAML scalar without introducing a runtime dependency."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    hit = re.search(r"(?m)^\s*%s:\s*([^#\n]+)" % re.escape(key), text)
    return hit.group(1).strip().strip("'\"") if hit else ""


def _yaml_child_scalar(path: Path, parent: str, key: str) -> str:
    """Read one scalar from a direct child mapping in simple emitted YAML."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    parent_indent = None
    for line in lines:
        hit = re.match(r"^(\s*)%s:\s*(?:#.*)?$" % re.escape(parent), line)
        if hit:
            parent_indent = len(hit.group(1))
            continue
        if parent_indent is None or not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= parent_indent:
            break
        hit = re.match(r"^\s*%s:\s*([^#\n]+)" % re.escape(key), line)
        if hit:
            return hit.group(1).strip().strip("'\"")
    return ""


def _truth(value) -> bool:
    return value is True or str(value).strip().lower() in {
        "true", "yes", "pass", "passed", "valid", "confirmed",
    }


def _labeling_lane(page_src: Path) -> tuple[Path, str]:
    """Resolve the page-folder lane even when Board renders a flat source.

    Some older Boards render ``<group>/<page>.md`` while keeping the page's
    task-side folder at ``pages/<page>/``.  The browser must follow that exact
    sidecar instead of silently reporting an empty lane beside the flat copy.
    """
    direct = page_src.parent / "labeling"
    if direct.is_dir():
        return direct, "canonical page-local lane"
    for ancestor in page_src.parents:
        if not (ancestor / "board.md").is_file():
            continue
        folded_page = ancestor / "pages" / page_src.stem / page_src.name
        folded_lane = folded_page.parent / "labeling"
        if folded_page.is_file() and folded_lane.is_dir():
            return folded_lane, (
                "page-folder bridge from flat Board source · "
                f"pages/{page_src.stem}/labeling/"
            )
        break
    return direct, "canonical page-local lane"


def _job_root(page_src: Path) -> tuple[Path, str]:
    """Return the canonical root, with explicit read-only compatibility bridges."""
    lane, location_note = _labeling_lane(page_src)
    if (lane / "config.yaml").is_file() or not lane.is_dir():
        return lane, location_note
    legacy = sorted(lane.glob("field-tests/*/run/config.yaml"))
    if legacy:
        return legacy[-1].parent, (
            location_note + " · legacy nested field-test · migrate receipts to labeling/"
        )
    return lane, location_note


@lru_cache(maxsize=1)
def _canonical_job_module():
    """Load the subjective-label writer's read-only status API.

    The Board engine and the domain plugin are deliberately separate plugin
    roots.  Loading the small, dependency-stable ``job.py`` module by path
    keeps the presenter from maintaining a second checksum implementation and
    avoids making either plugin depend on the other's Python package layout.
    """
    here = Path(__file__).resolve()
    candidate = next(
        (parent / "subjective-label" / "engine" / "job.py"
         for parent in here.parents
         if (parent / "subjective-label" / "engine" / "job.py").is_file()),
        None,
    )
    if candidate is None:
        return None
    spec = importlib.util.spec_from_file_location(
        "haipipe_subjective_label_job_for_board", candidate
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _canonical_status(root: Path) -> dict | None:
    """Return the canonical P0 frontier when this is a real v2 job.

    Older field-test fixtures often contain only placeholder P0 files.  They
    remain readable through the compatibility presenter, but once a canonical
    receipt exists the Board must defer to the domain engine and surface its
    checksum/receipt failures instead of guessing from file presence.
    """
    if not any(
        (root / rel).is_file()
        for rel in ("gates/p0-contract/receipt.json", "gates/g0/receipt.json")
    ):
        return None
    try:
        module = _canonical_job_module()
        if module is None:
            return {
                "phase": "P0",
                "missing": [],
                "integrity_errors": ["canonical subjective-label status API unavailable"],
                "meaning_confirmed": False,
                "meaning_receipt_valid": False,
                "g0_integrity": False,
                "g0_receipt_valid": False,
                "next_action": "repair canonical status API before proceeding",
            }
        return module.status(root)
    except Exception as error:  # the surface must fail closed, not crash the Board
        return {
            "phase": "P0",
            "missing": [],
            "integrity_errors": [f"canonical status could not be derived: {type(error).__name__}"],
            "meaning_confirmed": False,
            "meaning_receipt_valid": False,
            "g0_integrity": False,
            "g0_receipt_valid": False,
            "next_action": "repair canonical P0 status before proceeding",
        }


def inspect(page_src: Path) -> dict:
    root, location_note = _job_root(page_src)
    p0 = {rel: (root / rel).is_file() for rel in P0_FILES}
    canonical = _canonical_status(root)
    if canonical:
        # Once a canonical receipt exists, the domain engine—not this view's
        # file-presence heuristics—owns P0 checksum and receipt truth.
        p0 = {
            rel: bool((canonical.get("p0_files") or {}).get(rel, present))
            for rel, present in p0.items()
        }
    round_dirs = sorted(
        (p for p in (root / "rounds").glob("round_*") if p.is_dir()),
        key=lambda p: p.name,
    ) if (root / "rounds").is_dir() else []
    checkpoints = [(r, _read_json(r / "checkpoint.json"))
                   for r in round_dirs if (r / "checkpoint.json").is_file()]
    open_rounds = [r.name for r in round_dirs if not (r / "checkpoint.json").is_file()]
    latest_round, latest = checkpoints[-1] if checkpoints else (None, {})

    handoff = root / "handoff" / "label-v1.yaml"
    handoff_status = _yaml_scalar(handoff, "status") if handoff.is_file() else ""
    eval_lock = root / "test" / "final" / "lock.json"
    eval_registry = root / "evaluation" / "registry.yaml"
    eval_summary = root / "evaluation" / "summary.md"
    prod_runs = sorted(p for p in (root / "production").glob("run_*") if p.is_dir()) \
        if (root / "production").is_dir() else []
    audits = sorted(p for p in (root / "audit").glob("final_*") if p.is_dir()) \
        if (root / "audit").is_dir() else []
    latest_prod = prod_runs[-1] if prod_runs else None
    latest_audit = audits[-1] if audits else None
    dstar = root / "corpus" / "final" / "D_star.jsonl"
    dstar_manifest = root / "corpus" / "final" / "manifest.yaml"

    if latest_audit and (latest_audit / "receipt.json").is_file():
        phase_i = 5
    elif latest_prod:
        phase_i = 4
    elif eval_lock.is_file() or eval_summary.is_file():
        phase_i = 3
    elif handoff.is_file():
        phase_i = 2
    elif checkpoints or round_dirs or all(p0.values()):
        phase_i = 1
    else:
        phase_i = 0

    config = root / "config.yaml"
    simulation = _truth(_yaml_scalar(config, "simulation_only"))
    human_id = _yaml_scalar(config, "human_id")
    authority_mode = _yaml_scalar(config, "mode")
    creates_gold = _yaml_scalar(config, "creates_human_gold")
    meaning_value = _yaml_scalar(config, "meaning_confirmed")
    meaning_confirmed = _truth(meaning_value)
    meaning_receipt_valid = bool(
        meaning_confirmed
        and _truth(_yaml_child_scalar(config, "meaning_receipt", "status"))
        and _yaml_child_scalar(config, "meaning_receipt", "human_id") == human_id
        and _yaml_child_scalar(config, "meaning_receipt", "confirmed_at")
    )
    if canonical:
        meaning_confirmed = bool(canonical.get("meaning_confirmed"))
        meaning_receipt_valid = bool(canonical.get("meaning_receipt_valid"))
    missing_human = all(p0.values()) and not human_id
    authority_hold = missing_human or simulation or "simulation" in authority_mode.lower() \
        or (creates_gold and not _truth(creates_gold))
    authority_reason = ("config does not name one identified human semantic authority"
                        if missing_human else
                        "a simulation/proxy cannot create human gold or sign Freeze")

    gates = latest.get("stopping_gates") or latest.get("gates") or {}
    gate_pass = {name: _truth((gates.get(name) or {}).get("pass"))
                 for name in ("quality", "stability", "coverage", "risk")}
    stop_signoff = _truth(latest.get("human_stop_signoff")) \
        or _truth((latest.get("stopping_gates") or {}).get("human_stop_signoff"))

    open_cells = ((latest.get("coverage") or {}).get("open_cells") or
                  ((gates.get("coverage") or {}).get("open_cells")) or [])
    open_cells = [str(x) for x in open_cells]
    checkpoint_rel = ((latest_round / "checkpoint.json").relative_to(root).as_posix()
                      if latest_round else "P0 Contract artifacts")

    missing = [rel for rel, present in p0.items() if not present]
    canonical_integrity_errors = [
        str(error) for error in (canonical or {}).get("integrity_errors", [])
    ]
    meaning_open = (all(p0.values()) and not authority_hold and bool(meaning_value)
                    and not meaning_receipt_valid)
    if canonical and (
        canonical_integrity_errors
        or not canonical.get("meaning_receipt_valid")
        or not canonical.get("g0_receipt_valid")
    ):
        phase_i = 0
    if meaning_open and not checkpoints and not round_dirs:
        phase_i = 0
    if not root.exists():
        next_action = "P0 Contract · create the page-local labeling/ job through /subjective-label"
    elif canonical_integrity_errors:
        next_action = "P0 Contract · " + str(
            canonical.get("next_action") or "repair canonical P0 integrity"
        )
    elif missing:
        next_action = "P0 Contract · supply: " + ", ".join(missing)
    elif authority_hold:
        target = (" · target register cell(s): " + ", ".join(open_cells)) if open_cells else ""
        next_action = ("HOLD · owner: one identified real human semantic authority + "
                       "Checkpoint Keeper · preserve: %s · next: start a new "
                       "real-authority Building lineage%s" % (checkpoint_rel, target))
    elif canonical and not canonical.get("meaning_receipt_valid"):
        next_action = "P0 Contract · the identified human must confirm the current meaning"
    elif meaning_open:
        next_action = ("P0 Contract · the identified human must confirm the target, "
                       "class meanings, regions, uncertainty, and unresolved disposition")
    elif open_rounds:
        next_action = "P1 Round · resume " + open_rounds[0] + " at its first missing canonical event"
    elif not checkpoints:
        next_action = "P1 Round · propose and obtain human release for the first round card"
    elif checkpoints and not (all(gate_pass.values()) and stop_signoff):
        next_action = "P1 Round · derive one bounded next action from the newest checkpoint and register"
    elif not handoff.is_file():
        next_action = "P2 Freeze · the identified human and Keeper must sign one immutable Label Handoff"
    elif handoff_status and handoff_status != "valid":
        next_action = "HOLD · Label Handoff is present but does not declare status: valid"
    elif not (eval_registry.is_file() and eval_lock.is_file() and eval_summary.is_file()):
        next_action = "P3 Test · freeze the evaluation registry, lock T*, then score closed predictions"
    elif not latest_prod:
        next_action = "P4 Scan · freeze one production manifest before attempts begin"
    elif not latest_audit:
        next_action = "P5 Audit · freeze and run the independent probability audit"
    elif not (dstar.is_file() and dstar_manifest.is_file()):
        next_action = "P5 Audit · close repairs and materialize D* from reconciled terminal rows"
    else:
        next_action = "COMPLETE candidate · rehash G6 and verify the audit receipt before claiming D*"

    if canonical_integrity_errors:
        first_failed = "G0 Contract integrity · " + "; ".join(canonical_integrity_errors[:3])
    elif missing:
        first_failed = "G0 Contract → Round · missing " + ", ".join(missing)
    elif missing_human:
        first_failed = "G0 Contract → Round · " + authority_reason
    elif canonical and not canonical.get("meaning_receipt_valid"):
        first_failed = "P0 Contract · human meaning confirmation remains open"
    elif meaning_open:
        first_failed = "P0 Contract · human meaning confirmation remains open"
    elif not checkpoints:
        first_failed = "G1 Round close · no Keeper-closed checkpoint exists"
    elif not (all(gate_pass.values()) and stop_signoff) or authority_hold:
        failed = [name for name, passed in gate_pass.items() if not passed]
        if not stop_signoff:
            failed.append("human STOP signoff")
        if authority_hold:
            failed.append(authority_reason)
        first_failed = "G2 Round → Freeze · " + ", ".join(failed) + " remains open"
    elif not (handoff.is_file() and handoff_status == "valid" and eval_registry.is_file()):
        owed = []
        if not handoff.is_file():
            owed.append("Label Handoff absent")
        elif handoff_status != "valid":
            owed.append("Label Handoff status is not valid")
        if not eval_registry.is_file():
            owed.append("evaluation registry absent")
        first_failed = "G3 Freeze → Test · " + ", ".join(owed)
    elif not (eval_lock.is_file() and eval_summary.is_file()):
        first_failed = "G4 Test → Scan · T* lock and passing evaluation summary are required"
    elif not latest_prod or not (latest_prod / "run_report.md").is_file():
        first_failed = "G5 Scan → Audit · reconciled production run report absent"
    elif not latest_audit or not (latest_audit / "receipt.json").is_file() \
            or not (dstar.is_file() and dstar_manifest.is_file()):
        first_failed = "G6 Audit → Complete · valid audit receipt and D* manifest are required"
    else:
        first_failed = "None observed · G6 still requires workflow rehash before a completion claim"

    g2_reported = bool(checkpoints and all(gate_pass.values()) and stop_signoff)
    g0_reported = bool(
        canonical and canonical.get("g0_integrity")
        and canonical.get("meaning_receipt_valid")
        and canonical.get("g0_receipt_valid")
    )
    if canonical_integrity_errors:
        g0_note = "; ".join(canonical_integrity_errors[:3])
    elif canonical:
        g0_note = (
            "canonical P0 checksums and G0 meaning receipt validated"
            if g0_reported else
            "P0 is intact; human meaning confirmation/G0 receipt remains open"
        )
    else:
        g0_note = (
            "required files observed; P0 meaning confirmation remains open before G0 may be tested"
            if meaning_open else
            "required files observed; canonical receipt/checksum validation is not present"
        )
    gate_rows = [
        ("G0", "Contract → Round", sum(p0.values()), len(p0), g0_reported, g0_note),
        ("G1", "Round close", len(checkpoints), len(round_dirs), False,
         (latest.get("state") or latest.get("closed") or "no checkpoint") if checkpoints else "no checkpoint"),
        ("G2", "Round → Freeze", 1 if g2_reported else 0, 1, g2_reported,
         "checkpoint reports four gates + human STOP" if g2_reported else "stopping evidence remains open"),
        ("G3", "Freeze → Test", 1 if handoff.is_file() and eval_registry.is_file() else 0, 1,
         handoff_status == "valid" and eval_registry.is_file(),
         "handoff + evaluation registry observed; checksum validation still owed"),
        ("G4", "Test → Scan", sum(p.is_file() for p in (eval_lock, eval_summary)), 2, False,
         "T* lock and evaluation summary must both exist"),
        ("G5", "Scan → Audit", 1 if latest_prod and (latest_prod / "run_report.md").is_file() else 0, 1, False,
         "latest production run report observed" if latest_prod else "no production run"),
        ("G6", "Audit → Complete", 1 if latest_audit and (latest_audit / "receipt.json").is_file() else 0, 1, False,
         "audit receipt observed; this view never certifies it" if latest_audit else "no final audit"),
    ]

    return {
        "root": root, "location_note": location_note, "phase_i": phase_i,
        "canonical_status": canonical,
        "canonical_integrity_errors": canonical_integrity_errors,
        "p0": p0, "round_dirs": round_dirs, "checkpoints": checkpoints,
        "open_rounds": open_rounds, "latest_round": latest_round,
        "latest": latest, "handoff": handoff, "handoff_status": handoff_status,
        "prod_runs": prod_runs, "audits": audits, "dstar": dstar,
        "meaning_confirmed": meaning_confirmed,
        "meaning_receipt_valid": meaning_receipt_valid,
        "dstar_manifest": dstar_manifest, "human_id": human_id,
        "authority_mode": authority_mode, "authority_hold": authority_hold,
        "authority_reason": authority_reason,
        "simulation": simulation, "gate_pass": gate_pass,
        "stop_signoff": stop_signoff, "gate_rows": gate_rows,
        "next_action": next_action, "first_failed": first_failed,
    }


def is_labeling_run_page(page_src: Path) -> bool:
    """True only for a labeling run Page; the dashboard owns no job lane."""
    if not page_src.is_file() or page_src.name == "S-Label-Dash.md":
        return False
    try:
        head = page_src.read_text(encoding="utf-8", errors="ignore")[:4096]
    except OSError:
        return False
    return bool(re.search(r"(?m)^page-type:\s*labeling\s*$", head))


def is_labeling_surface_page(page_src: Path) -> bool:
    """True for every real Page that can own an optional labeling/ lane.

    A specialized ``page-type: labeling`` changes the Page's prose grammar;
    it is not a prerequisite for opening a Page-local plugin.  The one control
    dashboard is excluded because it inventories jobs and owns no job itself.
    """
    return page_src.is_file() and page_src.name != "S-Label-Dash.md"


def labeling_chat_hold(page_src: Path) -> tuple[bool, str]:
    """Server-side Chat guard; no browser flag can turn a labeling HOLD off."""
    if not is_labeling_surface_page(page_src):
        return False, ""
    state = inspect(page_src)
    action = state["next_action"]
    held = action.startswith("HOLD")
    return held, action if held else ""


def labeling_hold_for_scene(root: Path, scene_q: str) -> tuple[bool, str]:
    """Bind one Draw scene to its Board Page, then derive Labeling HOLD.

    Draw addresses a scene rather than a Page source, so it cannot use the
    ordinary ``path`` + ``file`` resolver. The builder's ownership law gives
    us the canonical inverse ``<folded-page>/studio/draw/<page-id>.excalidraw``;
    a flat legacy Page remains in its Group ``draw/``. Reparse the closest Board
    and accept only those mappings; a caller-supplied browser flag can neither
    invent nor disable the hold.
    """
    root = Path(root).resolve()
    scene = (root / (scene_q or "").strip().lstrip("/")).resolve()
    try:
        scene.relative_to(root)
    except ValueError:
        return False, ""
    board_dir = None
    for parent in scene.parents:
        if (parent / "board.md").is_file():
            board_dir = parent
            break
        if parent == root:
            break
    if board_dir is None:
        return False, ""
    try:
        _, pages, _ = parse_dir(board_dir)
    except (OSError, ValueError, TypeError):
        return False, ""
    for page in pages:
        file_q = page.get("file") or ""
        page_source = board_dir / file_q
        page_home = page_source.parent
        folded = page_home.name == page_source.stem
        expected = (
            page_home / "studio" / "draw" /
            (str(page.get("id") or "") + ".excalidraw")
            if folded else
            page_home / "draw" /
            (str(page.get("id") or "") + ".excalidraw")
        ).resolve()
        legacy = (page_home / "draw" /
                  (str(page.get("id") or "") + ".excalidraw")).resolve()
        if scene not in ({expected, legacy} if folded else {expected}):
            continue
        page_src = board_dir / file_q
        if not is_labeling_surface_page(page_src):
            return False, ""
        try:
            return labeling_chat_hold(page_src)
        except Exception:
            return True, "HOLD · labeling receipts could not be safely inspected"
    return False, ""


def studio_chat_page_url(
        path_q: str, file_q: str, page_q: str, board_dir: Path | None) -> str:
    """Validate and return the generated Page URL Studio binds Chat to.

    ``path_q`` is intentionally ``board.md`` because it resolves the source
    file.  It is not a browser Page and must never receive ``?pane=chat``.
    ``page_q`` comes from the current page frame's ``location.pathname`` and
    must name the matching generated HTML beneath that same Board.  The Board
    source is parsed with the same group-token law as the builder, then the
    generated file must still identify ``file_q`` in its Page section.  A
    same-basename file under a forged subgroup is therefore not sufficient.
    """
    parsed = urlparse(page_q or "")
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return ""
    page_path = parsed.path
    board_path = urlparse(path_q or "").path
    decoded_page = unquote(page_path)
    decoded_board = unquote(board_path)
    if not decoded_board.endswith("/board.md"):
        return ""
    if ".." in PurePosixPath(decoded_page).parts:
        return ""
    board_root = decoded_board.rsplit("/", 1)[0]
    generated_root = board_root.rstrip("/") + "/board/"
    if board_dir is None or not decoded_page.startswith(generated_root):
        return ""
    relative_page = PurePosixPath(decoded_page[len(generated_root):])
    if relative_page.is_absolute() or len(relative_page.parts) != 2:
        return ""
    try:
        _, pages, _ = parse_dir(Path(board_dir))
    except (OSError, ValueError, TypeError):
        return ""
    matches = [q for q in pages if q.get("file") == file_q]
    if len(matches) != 1:
        return ""
    source = matches[0]
    expected_relative = PurePosixPath(
        group_token(source.get("group") or "") or "_ungrouped",
        Path(source.get("file") or source["id"]).stem + ".html",
    )
    if relative_page != expected_relative:
        return ""
    generated_file = Path(board_dir) / "board" / Path(*relative_page.parts)
    if not generated_file.is_file():
        return ""
    try:
        generated_head = generated_file.read_text(
            encoding="utf-8", errors="ignore")[:262144]
    except OSError:
        return ""
    marker = re.search(r'<section\b[^>]*\bdata-file="([^"]*)"', generated_head, re.I)
    if not marker or html.unescape(marker.group(1)) != file_q:
        return ""
    return page_path


_CSS = """
:root{--bg:#ffffff;--fg:#202124;--mut:#72747b;--line:#dddeda;--card:#f7f7f8;
 --accent:#8055a5;--accent-soft:#f1eaf7;--ok:#26734d;--hold:#a34b24}
@media(prefers-color-scheme:dark){:root{--bg:#17181a;--fg:#ececea;--mut:#a1a19c;
 --line:#303238;--card:#202226;--accent:#c59be8;--accent-soft:#2b2332;
 --ok:#72c796;--hold:#ee956f}}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);
 font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;height:100vh;
 display:grid;grid-template-rows:minmax(0,58fr) 8px minmax(120px,42fr);overflow:hidden}
#work{min-height:0;display:flex;flex-direction:column;overflow:hidden}
header{display:flex;justify-content:space-between;gap:12px;align-items:start;
 padding:12px 16px 9px;border-bottom:1px solid var(--line)}
h1{font-size:17px;margin:0}.mut{color:var(--mut);font-size:12px}.path{font:12px ui-monospace,Menlo,monospace}
.statusline{display:flex;gap:7px;flex-wrap:wrap;margin-top:5px;align-items:center}
.tag{border:1px solid var(--line);border-radius:5px;padding:2px 6px;background:var(--card);
 font:11px ui-monospace,Menlo,monospace}.tag.now{border-color:var(--accent);color:var(--accent)}
.spacebar{display:flex;gap:3px;overflow:auto;padding:7px 10px 0;border-bottom:1px solid var(--line)}
.space{appearance:none;border:0;border-bottom:2px solid transparent;background:transparent;
 color:var(--mut);padding:7px 10px 8px;white-space:nowrap;font:600 12px -apple-system,sans-serif;
 cursor:pointer}.space:hover{color:var(--fg)}.space.on{color:var(--accent);border-bottom-color:var(--accent)}
#spaces{min-height:0;flex:1;overflow:auto;padding:12px 16px 18px}.workspace{display:none}
.workspace.on{display:block}.workspace-head{display:flex;align-items:baseline;gap:8px;margin-bottom:10px}
.workspace-head h2{font-size:15px;margin:0}.workspace-head span{color:var(--mut);font-size:12px}
.phase{display:grid;grid-template-columns:repeat(6,minmax(72px,1fr));gap:5px;margin:12px 0}
.ph{border:1px solid var(--line);border-radius:8px;padding:7px;background:var(--card);color:var(--mut)}
.ph.now{border-color:var(--accent);color:var(--accent);font-weight:700}.ph.past{color:var(--ok)}
.decision{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}
.next,.failed{background:var(--card);padding:9px 11px;border-radius:5px}
.next{border-left:4px solid var(--accent)}.failed{border-left:4px solid var(--hold)}
.grid{display:grid;grid-template-columns:repeat(2,minmax(240px,1fr));gap:10px}
.grid.four{grid-template-columns:repeat(4,minmax(155px,1fr))}
.box{border:1px solid var(--line);border-radius:9px;padding:9px 11px;background:var(--card)}
.box h3{font-size:13px;margin:0 0 6px}.box p{margin:5px 0}.gate{display:grid;grid-template-columns:34px minmax(120px,1fr) auto;gap:7px;
 padding:5px 0;border-top:1px solid var(--line);align-items:baseline}.gate:first-of-type{border-top:0}
.obs{color:var(--mut);font-size:11px}.hold{color:var(--hold)}.ok{color:var(--ok)}
.metric{display:flex;justify-content:space-between;gap:12px;padding:5px 0;border-top:1px solid var(--line)}
.metric:first-of-type{border-top:0}.metric b{text-align:right}.empty{color:var(--mut)}
.round{display:grid;grid-template-columns:minmax(100px,1fr) auto;gap:10px;padding:6px 0;
 border-top:1px solid var(--line)}.round:first-of-type{border-top:0}
.guard{margin-top:10px;border:1px dashed var(--line);border-radius:8px;padding:10px;color:var(--mut)}
#splitter{background:var(--line);cursor:row-resize;touch-action:none;position:relative;z-index:2}
#splitter:after{content:"";position:absolute;left:calc(50% - 22px);top:2px;width:44px;height:3px;border-radius:4px;background:var(--mut);opacity:.55}
#studio-chat{min-height:0;overflow:hidden;border-top:2px solid var(--line)}
#chat{border:0;width:100%;height:100%;display:block}
@media(max-width:900px){.grid.four{grid-template-columns:repeat(2,minmax(155px,1fr))}}
@media(max-width:700px){body{grid-template-rows:minmax(0,55fr) 8px minmax(120px,45fr)}
 .grid,.grid.four,.decision{grid-template-columns:1fr}.phase{overflow:auto;grid-template-columns:repeat(6,96px)}
 header{padding-right:10px}.path{display:none}}
@media(max-height:420px){body{grid-template-rows:minmax(0,52fr) 8px minmax(110px,48fr)}
 #spaces{padding-bottom:8px}header{padding-top:7px;padding-bottom:5px}}
"""


def render(
        page_src: Path, path_q: str, file_q: str, page_q: str,
        board_dir: Path) -> str:
    state = inspect(page_src)
    phase = "".join(
        '<div class="ph %s"><b>%s</b><br>%s</div>' %
        ("past" if i < state["phase_i"] else "now" if i == state["phase_i"] else "",
         pid, name)
        for i, (pid, name) in enumerate(PHASES)
    )
    gates = "".join(
        '<div class=gate><b>%s</b><span>%s<div class=obs>%s</div></span>'
        '<span class="%s">%s/%s observed</span></div>' %
        (gid, html.escape(name), html.escape(str(note)), "ok" if reported else "obs", seen, total)
        for gid, name, seen, total, reported, note in state["gate_rows"]
    )
    latest = state["latest"]
    authority = state["human_id"] or "not declared/readable"
    if state["authority_mode"]:
        authority += " · " + state["authority_mode"]
    hold_class = "hold" if state["authority_hold"] else ""
    root_display = str(state["root"].relative_to(page_src.parent)) \
        if state["root"].is_relative_to(page_src.parent) else str(state["root"])
    artifact = (
        f"{len(state['checkpoints'])} closed checkpoint(s) · "
        f"{len(state['open_rounds'])} open round(s) · "
        f"handoff {'present' if state['handoff'].is_file() else 'absent'} · "
        f"production {len(state['prod_runs'])} · audits {len(state['audits'])}"
    )
    hard_hold = state["next_action"].startswith("HOLD")
    chat_page = studio_chat_page_url(path_q, file_q, page_q, board_dir)
    if not chat_page:
        raise ValueError("Labeling Studio Chat requires the matching generated Page URL")
    chat_url = chat_page + "?pane=chat"
    if hard_hold:
        chat_url += "&labeling_hold=1"

    # Include the Board source and Page file in client preferences.  A stem is
    # not globally unique: two Boards can legitimately contain the same Page
    # name, and their selected Workspace/split must not bleed into each other.
    identity = f"{path_q}|{file_q}"
    def js_string(value: str) -> str:
        # JSON handles quotes/backslashes; escaping HTML-significant characters
        # keeps an untrusted URL component from terminating this inline script.
        return (json.dumps(value, ensure_ascii=False)
                .replace("<", "\\u003c")
                .replace(">", "\\u003e")
                .replace("&", "\\u0026"))

    workspace_key = js_string("labeling-workspace:" + identity)
    split_key = js_string("labeling-split:" + identity)

    root = state["root"]
    run_tickets = sorted((root / "runs").glob("*.yaml")) \
        if (root / "runs").is_dir() else []
    run_results = sorted(p for p in (root / "results").iterdir() if p.is_dir()) \
        if (root / "results").is_dir() else []
    run_rows = "".join(
        '<div class=round><span><b>%s</b><br><span class=obs>Ticket</span></span>'
        '<b class="%s">%s</b></div>' % (
            html.escape(ticket.stem),
            "ok" if (root / "results" / ticket.stem).is_dir() else "hold",
            "result present" if (root / "results" / ticket.stem).is_dir()
            else "awaiting result",
        )
        for ticket in run_tickets
    ) or '<div class=empty>No allocated Run Ticket is present.</div>'
    embedding_versions = sorted(p.name for p in (root / "cache" / "embeddings").iterdir()
                                if p.is_dir()) \
        if (root / "cache" / "embeddings").is_dir() else []
    policy_versions = sorted(p for p in (root / "policy" / "versions").iterdir()
                             if p.is_dir()) \
        if (root / "policy" / "versions").is_dir() else []
    latest_policy = policy_versions[-1] if policy_versions else None
    policy_parts = ("guideline.md", "boundaries.yaml", "procedure.yaml",
                    "uncertainty.yaml", "casebook.jsonl", "diff.yaml",
                    "regression.jsonl", "cheatsheet.md", "gallery.md")
    policy_seen = sum((latest_policy / name).is_file() for name in policy_parts) \
        if latest_policy else 0
    prediction_count = len(list((root / "evaluation" / "predictions").glob("*"))) \
        if (root / "evaluation" / "predictions").is_dir() else 0
    scorecard_count = len(list((root / "evaluation" / "scorecards").glob("*"))) \
        if (root / "evaluation" / "scorecards").is_dir() else 0

    def present(flag: bool, yes="observed", no="not yet") -> str:
        return '<span class="%s">%s</span>' % (
            "ok" if flag else "empty", html.escape(yes if flag else no))

    def metric(label: str, value: str) -> str:
        return '<div class=metric><span>%s</span><b>%s</b></div>' % (
            html.escape(label), value)

    round_rows = "".join(
        '<div class=round><span>%s</span><b class="%s">%s</b></div>' % (
            html.escape(round_dir.name),
            "ok" if (round_dir / "checkpoint.json").is_file() else "hold",
            "checkpoint closed" if (round_dir / "checkpoint.json").is_file() else "open",
        ) for round_dir in reversed(state["round_dirs"])
    ) or '<div class=empty>No calibration round has been allocated.</div>'

    quality_gates = "".join(
        '<div class=gate><b>%s</b><span>%s<div class=obs>%s</div></span>'
        '<span class="%s">%s/%s observed</span></div>' %
        (gid, html.escape(name), html.escape(str(note)),
         "ok" if reported else "obs", seen, total)
        for gid, name, seen, total, reported, note in state["gate_rows"]
        if gid in {"G3", "G4", "G5", "G6"}
    )

    active_phase = PHASES[state["phase_i"]]
    return f"""<!doctype html><meta charset=utf-8>
<title>🏷 Labeling · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<section id=work>
<header><div><h1>🏷 Labeling · {html.escape(page_src.stem)}</h1>
<div class=statusline><span class="tag now">{active_phase[0]} · {active_phase[1]}</span>
<span class=tag>👤 {html.escape(authority)}</span>
<span class=tag>⚙ {len(run_tickets)} Runs</span>
<span class="tag {'hold' if hard_hold else ''}">{'HOLD' if hard_hold else 'receipt-first'}</span></div></div>
<div class="path mut">{html.escape(root_display)}/<br>{html.escape(state['location_note'])}</div></header>
<nav class=spacebar role=tablist aria-label="Labeling workspaces">
 <button class="space on" role=tab aria-selected=true data-space=workflow>🧭 Workflow</button>
 <button class=space role=tab aria-selected=false data-space=data>🗃 Data</button>
 <button class=space role=tab aria-selected=false data-space=guideline>📘 Guideline</button>
 <button class=space role=tab aria-selected=false data-space=human>🧑 Human</button>
 <button class=space role=tab aria-selected=false data-space=quality>🧪 Quality</button>
</nav>
<div id=spaces>
 <section class="workspace on" data-workspace=workflow>
  <div class=workspace-head><h2>🧭 Workflow Workspace</h2><span>P0–P5 are state, not navigation</span></div>
  <div class=phase>{phase}</div>
  <div class=decision><div class=failed><b>First failed / blocked gate</b><br>{html.escape(state['first_failed'])}</div>
  <div class=next><b>One honest next action</b><br>{html.escape(state['next_action'])}</div></div>
  <div class=grid>
   <div class=box><h3>Gates · observed files are not certified passes</h3>{gates}</div>
   <div class=box><h3>Authority and operation</h3>
    <p class="{hold_class}"><b>Human authority:</b> {html.escape(authority)}</p>
    <p><b>Latest checkpoint:</b> {html.escape(state['latest_round'].name if state['latest_round'] else 'none')}</p>
    <p><b>Reported Building gates:</b> {html.escape(', '.join(k + (' ✓' if v else ' ·') for k,v in state['gate_pass'].items()) or 'none')}</p>
    <p><b>Inventory:</b> {html.escape(artifact)}</p>
    <p><b>Run envelopes:</b> {len(run_tickets)} Ticket(s) · {len(run_results)} Result folder(s)</p>
   </div>
  </div>
  <div class=box style="margin-top:10px"><h3>Run envelopes · read-only</h3>
   <p class=mut>One row per authored Ticket; a round, phase, Chat turn, or retry is not an extra Run.</p>
   {run_rows}
  </div>
 </section>

 <section class=workspace data-workspace=data>
  <div class=workspace-head><h2>🗃 Data Workspace</h2><span>corpus → embeddings → batches → audited D*</span></div>
  <div class="grid four">
   <div class=box><h3>Corpus snapshot</h3>
    {metric('manifest.json', present((root / 'corpus' / 'manifest.json').is_file()))}
    {metric('items.jsonl', present((root / 'corpus' / 'items.jsonl').is_file(), 'protected', 'not imported'))}
   </div>
   <div class=box><h3>Embeddings</h3>
    {metric('versions', html.escape(str(len(embedding_versions))))}
    <p class=mut>{html.escape(', '.join(embedding_versions[-3:]) or 'No embedding cache')}</p>
   </div>
   <div class=box><h3>Working batches</h3>
    {metric('calibration rounds', html.escape(str(len(state['round_dirs']))))}
    {metric('production episodes', html.escape(str(len(state['prod_runs']))))}
   </div>
   <div class=box><h3>Final corpus</h3>
    {metric('D_star.jsonl', present(state['dstar'].is_file(), 'materialized'))}
    {metric('manifest.yaml', present(state['dstar_manifest'].is_file(), 'observed'))}
   </div>
  </div>
  <div class=guard>Protected item text, sealed ids, and private judgments never render in this general workspace.</div>
 </section>

 <section class=workspace data-workspace=guideline>
  <div class=workspace-head><h2>📘 Guideline Workspace</h2><span>the current human meaning, its boundaries, and version lineage</span></div>
  <div class=grid>
   <div class=box><h3>Policy versions</h3>
    {metric('versions', html.escape(str(len(policy_versions))))}
    {metric('current closed candidate', html.escape(latest_policy.name if latest_policy else 'none'))}
    {metric('components', html.escape(f'{policy_seen}/{len(policy_parts)} observed'))}
   </div>
   <div class=box><h3>Meaning and regions</h3>
    {metric('meaning receipt', present(state['meaning_receipt_valid'], 'human-confirmed'))}
    {metric('seven-region register', present((root / 'register.md').is_file()))}
    {metric('cumulative gold view', present((root / 'gold' / 'cumulative.md').is_file()))}
   </div>
  </div>
  <div class=grid style="margin-top:10px">
   <div class=box><h3>Latest version components</h3>
    <p class=mut>{html.escape(' · '.join(name for name in policy_parts if latest_policy and (latest_policy / name).is_file()) or 'No policy version is readable yet.')}</p>
   </div>
   <div class=box><h3>Crossing</h3>
    {metric('Label Handoff', present(state['handoff'].is_file(), state['handoff_status'] or 'observed'))}
    <p class=mut>Handoff binds the frozen guideline; Scanning never edits it.</p>
   </div>
  </div>
 </section>

 <section class=workspace data-workspace=human>
  <div class=workspace-head><h2>🧑 Human Workspace</h2><span>the identified person’s bounded work, never model consensus</span></div>
  <div class=grid>
   <div class=box><h3>Authority</h3>
    <p class="{hold_class}"><b>{html.escape(authority)}</b></p>
    {metric('meaning confirmation', present(state['meaning_receipt_valid'], 'confirmed'))}
    {metric('STOP signoff', present(state['stop_signoff'], 'reported by checkpoint'))}
   </div>
   <div class=box><h3>Current human work</h3>
    <p>{html.escape(state['next_action'])}</p>
    <p class=mut>A protected Judge surface may open only for a commissioned human-work Run with an end-to-end event writer.</p>
   </div>
  </div>
  <div class=grid style="margin-top:10px">
   <div class=box><h3>Round ledger</h3>{round_rows}</div>
   <div class=box><h3>Human gold</h3>
    {metric('cumulative.jsonl', present((root / 'gold' / 'cumulative.jsonl').is_file(), 'checkpoint-owned'))}
    {metric('test human gold', present((root / 'test' / 'final' / 'human_gold.jsonl').is_file(), 'custodian-owned'))}
    {metric('audit human gold', present(any((p / 'human_gold.jsonl').is_file() for p in state['audits']), 'audit-owned'))}
   </div>
  </div>
  <div class=guard>Chat may explain or route this work. It cannot write first/final judgment, STOP, Freeze, or human gold.</div>
 </section>

 <section class=workspace data-workspace=quality>
  <div class=workspace-head><h2>🧪 Quality Workspace</h2><span>sealed Test → executor qualification → Scan → independent Audit</span></div>
  <div class="grid four">
   <div class=box><h3>Sealed test</h3>
    {metric('reservation', present((root / 'test' / 'sealed' / 'status.json').is_file()))}
    {metric('T* lock', present((root / 'test' / 'final' / 'lock.json').is_file(), 'locked'))}
   </div>
   <div class=box><h3>Executors</h3>
    {metric('registry', present((root / 'evaluation' / 'registry.yaml').is_file()))}
    {metric('predictions', html.escape(str(prediction_count)))}
    {metric('scorecards', html.escape(str(scorecard_count)))}
   </div>
   <div class=box><h3>Production scan</h3>
    {metric('episodes', html.escape(str(len(state['prod_runs']))))}
    {metric('latest report', present(bool(state['prod_runs']) and (state['prod_runs'][-1] / 'run_report.md').is_file()))}
   </div>
   <div class=box><h3>Final audit</h3>
    {metric('audits', html.escape(str(len(state['audits']))))}
    {metric('D*', present(state['dstar'].is_file(), 'candidate materialized'))}
   </div>
  </div>
  <div class=box style="margin-top:10px"><h3>Scanning gates</h3>{quality_gates}</div>
 </section>
</div></section>
<div id=splitter role=separator aria-label="Resize Labeling workspaces and Studio Chat"
 aria-controls="spaces studio-chat" aria-valuemin="20" aria-valuemax="80" tabindex=0></div>
<section id=studio-chat><iframe id=chat src="{html.escape(chat_url, quote=True)}"
 title="Studio Page Chat"></iframe></section>
<script>(function(){{'use strict';
 var key={workspace_key};
 var splitKey={split_key};
 var shell=document.body, splitter=document.getElementById('splitter');
 var buttons=Array.prototype.slice.call(document.querySelectorAll('.space'));
 var workspaces=Array.prototype.slice.call(document.querySelectorAll('.workspace'));
 function showSpace(name){{
   if(!workspaces.some(function(w){{return w.dataset.workspace===name;}})) name='workflow';
   buttons.forEach(function(b){{var on=b.dataset.space===name;b.classList.toggle('on',on);b.setAttribute('aria-selected',on?'true':'false');}});
   workspaces.forEach(function(w){{w.classList.toggle('on',w.dataset.workspace===name);}});
   try{{localStorage.setItem(key,name);}}catch(e){{}}
 }}
 buttons.forEach(function(b){{b.addEventListener('click',function(){{showSpace(b.dataset.space);}});}});
 try{{showSpace(localStorage.getItem(key)||'workflow');}}catch(e){{showSpace('workflow');}}
 function clampTop(value){{
   var h=window.innerHeight, gap=8, minChat=Math.min(120, Math.max(72, h*.25));
   var maxTop=Math.max(0, h-gap-minChat), minTop=Math.min(160, Math.max(72, h*.35));
   return Math.max(Math.min(minTop,maxTop), Math.min(maxTop, value));
 }}
 function applySplit(value, persist){{
   var top=clampTop(value), chat=Math.max(0, window.innerHeight-top-8);
   shell.style.gridTemplateRows=top+'px 8px '+chat+'px';
   splitter.setAttribute('aria-valuenow', String(Math.round(top/window.innerHeight*100)));
   if(persist){{try{{localStorage.setItem(splitKey,String(Math.round(top)));}}catch(e){{}}}}
 }}
 var savedSplit=0;
 try{{savedSplit=parseInt(localStorage.getItem(splitKey)||'',10)||0;}}catch(e){{}}
 if(savedSplit>0) applySplit(savedSplit,false);
 var dragging=false;
 splitter.addEventListener('pointerdown',function(ev){{
   dragging=true; splitter.setPointerCapture(ev.pointerId); ev.preventDefault();
 }});
 splitter.addEventListener('pointermove',function(ev){{
   if(dragging) applySplit(ev.clientY,true);
 }});
 splitter.addEventListener('pointerup',function(ev){{
   dragging=false; try{{splitter.releasePointerCapture(ev.pointerId);}}catch(e){{}}
 }});
 splitter.addEventListener('pointercancel',function(){{dragging=false;}});
 splitter.addEventListener('keydown',function(ev){{
   var rows=getComputedStyle(shell).gridTemplateRows.split(/\x5cs+/), top=parseFloat(rows[0])||window.innerHeight*.58;
   if(ev.key==='ArrowUp'){{applySplit(top-24,true);ev.preventDefault();}}
   if(ev.key==='ArrowDown'){{applySplit(top+24,true);ev.preventDefault();}}
   if(ev.key==='Home'){{applySplit(window.innerHeight*.35,true);ev.preventDefault();}}
   if(ev.key==='End'){{applySplit(window.innerHeight*.75,true);ev.preventDefault();}}
 }});
 window.addEventListener('resize',function(){{
   if(!dragging){{var rows=getComputedStyle(shell).gridTemplateRows.split(/\x5cs+/), top=parseFloat(rows[0])||0;
     if(top) applySplit(top,false);}}
 }});
 /* The framed document is Studio's exact Page Chat.  Its composer asks its
    parent for the optional Draw controls, so relay those calls to the outer
    split shell when Labeling itself is the registry frame. */
 ['__studioDrawIt','__studioToggleDraw','__studioDrawShown'].forEach(function(n){{
   window[n]=function(){{
     try{{if(parent!==window&&typeof parent[n]==='function')
       return parent[n].apply(parent,arguments);}}catch(e){{}}
     return false;
   }};
 }});
}})();</script>"""


class LabelingMixin:
    """The 🏷 tab. Read-only presenter over the labeling/ lane."""

    def labeling_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        file_q = (q.get("file") or [""])[0]
        page_q = (q.get("page") or [""])[0]
        got = self.target({"path": path_q, "file": file_q})
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        if not is_labeling_surface_page(got[0]):
            return self.reply(404, {"ok": False, "err": "Page has no labeling lane"})
        if not studio_chat_page_url(path_q, file_q, page_q, got[1]):
            return self.reply(400, {"ok": False,
                                    "err": "missing or mismatched generated Page URL"})
        body = render(got[0], path_q, file_q, page_q, got[1]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_labeling(self, p):
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        if not is_labeling_surface_page(got[0]):
            return None, "Page has no labeling lane"
        path_q = p.get("path") or ""
        file_q = p.get("file") or ""
        page_q = p.get("page") or ""
        if not studio_chat_page_url(path_q, file_q, page_q, got[1]):
            return None, "missing or mismatched generated Page URL"
        return {"url": "/_board/labeling?path=%s&file=%s&page=%s" %
                (quote(path_q), quote(file_q), quote(page_q))}, None
