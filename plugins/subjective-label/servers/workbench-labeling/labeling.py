"""🏷 Labeling · five Spaces over one page-local labeling/ job, plus one write door.

Data · Labeling · Quality · Run · Delivery are views over canonical files; the
overview never renders item text and never upgrades an observed file to a
passed gate.  Labeling → Label holds the label definitions.  Round item text
appears only in Labeling → Rounds, and only for items already shown to the
person; the labels come from the chat.  Every write through
``POST /_board/labeling/act`` goes through the
subjective-label engine (``job.confirm_meaning`` and ``calibration``), which
re-checks the caller-supplied configured authority id, HOLD, G0, the event
order, and sealed custody on each call. The local Board does not authenticate
the caller's identity. Studio Chat stays a separate tab.
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
from functools import lru_cache
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, quote, unquote, urlparse

from src.body import group_token as _grammar_group_token
from src.parse import parse_dir as _grammar_parse_dir


def _board_pages(board_dir) -> list[dict]:
    """The one place this workbench reads the Board grammar (haipipe-toolkit `src`).

    Everything else here works on the page dicts this returns, so a labeling
    host that stops depending on a Board replaces this function and nothing
    else moves.
    """
    _, pages, _ = _grammar_parse_dir(Path(board_dir))
    return pages


def group_token(heading: str) -> str:
    """`QA · words` -> `QA`; the builder's group law, through the same adapter seam."""
    return _grammar_group_token(heading)


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
    except (OSError, UnicodeError):
        return ""
    hit = re.search(r"(?m)^\s*%s:\s*([^#\n]+)" % re.escape(key), text)
    return hit.group(1).strip().strip("'\"") if hit else ""


def _yaml_top_scalar(path: Path, key: str) -> str:
    """Read one top-level (unindented) YAML scalar."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""
    hit = re.search(r"(?m)^%s:[ \t]*([^#\n]+)" % re.escape(key), text)
    return hit.group(1).strip().strip("'\"") if hit else ""


def _yaml_child_scalar(path: Path, parent: str, key: str) -> str:
    """Read one scalar from a direct child mapping in simple emitted YAML."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
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
                "p0_contract_integrity_valid": False,
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
            "p0_contract_integrity_valid": False,
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
    simulation = _truth(_yaml_top_scalar(config, "simulation_only"))
    human_id = _yaml_child_scalar(config, "authority", "human_id")
    authority_mode = _yaml_child_scalar(config, "authority", "mode")
    creates_gold = _yaml_child_scalar(config, "authority", "creates_human_gold")
    meaning_value = _yaml_child_scalar(config, "authority", "meaning_confirmed")
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
    if canonical and canonical.get("hold"):
        authority_hold = True
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
        next_action = "P0 Contract · the configured semantic authority must explicitly attest to the current meaning"
    elif meaning_open:
        next_action = ("P0 Contract · the configured semantic authority must explicitly attest to the target, "
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
        canonical and canonical.get("p0_contract_integrity_valid")
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
    try:
        state = inspect(page_src)
    except Exception:
        if _labeling_lane(page_src)[0].is_dir():
            return True, "HOLD · labeling receipts could not be safely inspected"
        return False, ""
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
        pages = _board_pages(board_dir)
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
        pages = _board_pages(Path(board_dir))
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


@lru_cache(maxsize=1)
def _calibration_module():
    """Load the subjective-label P1 writer (release, show/first/lock/reveal/final)."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    candidate = Path(job_module.__file__).with_name("calibration.py")
    if not candidate.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "haipipe_subjective_label_calibration_for_board", candidate
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _embedding_module():
    """Load the subjective-label embedding reader (``embedding_build.latest``)."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    candidate = Path(job_module.__file__).with_name("embedding_build.py")
    if not candidate.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "haipipe_subjective_label_embedding_for_board", candidate
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SPACES = (
    ("data", "Data", (("contract", "Contract"), ("schema", "Schema"), ("embedding", "Embedding"))),
    ("labeling", "Labeling", (("discussion", "Discussion"), ("label", "Label"), ("rounds", "Rounds"), ("guideline", "Guideline"))),
    ("quality", "Quality", (("test", "Test"), ("evaluation", "Evaluation"), ("audit", "Audit"))),
    ("run", "Run", (("runs", "Runs"), ("phases", "Phases"), ("workflow", "Workflow map"))),
    ("delivery", "Delivery", (("handoff", "Handoff"), ("final", "Final labels"))),
)


def _esc(value) -> str:
    return html.escape("" if value is None else str(value))


def _load_mapping(path: Path) -> dict:
    module = _canonical_job_module()
    if module is None or not path.is_file():
        return {}
    value, error = module.try_load_mapping(path)
    return {} if error else value


def _run_rows(root: Path) -> list[dict]:
    """One row per authored Ticket, with the runtime status beside it."""
    rows = []
    runs = root / "runs"
    if not runs.is_dir():
        return rows
    for ticket in sorted(runs.glob("*.yaml")):
        data = _load_mapping(ticket)
        runtime = _load_mapping(root / "results" / ticket.stem / "runtime.yaml")
        result = (root / "results" / ticket.stem / "result.yaml").is_file()
        status = str(runtime.get("status") or ("no runtime" if not runtime else "unknown"))
        if status == "complete" and not result:
            status = "complete · result.yaml missing"
        rows.append({
            "run": ticket.stem,
            "operation": str(data.get("operation") or "?"),
            "status": status,
            "outcome": str(runtime.get("outcome") or "")[:160],
        })
    return rows


def _row(label: str, value: str, cls: str = "") -> str:
    return (f'<div class=rr><b>{_esc(label)}</b>'
            f'<span class="{cls}">{value}</span></div>')


def _card(title: str, body: str, extra: str = "") -> str:
    return f'<div class="card {extra}"><h2>{_esc(title)}</h2>{body}</div>'


def _hold_words(reason) -> str:
    """Why a job is read-only, in words; the engine's reason names the missing authority."""
    reason = str(reason or "")
    if "imported source labels only" in reason:
        return "this job preserves imported source ratings; it does not collect local labels"
    if "human authority" in reason:
        return "no identified human labeler is assigned to this job"
    return reason


def _imported_reference_only(vm: dict) -> bool:
    """An import-only lane is a reference view, not a failed local labeling job."""
    state = vm.get("state") or {}
    if not state.get("authority_hold"):
        return False
    config = vm.get("config") or {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    canonical = vm.get("canonical") or {}
    reason = str(canonical.get("hold_reason") or state.get("authority_reason") or "")
    return (
        authority.get("mode") == "external_annotation_import"
        or "imported source labels only" in reason
    )


def _import_source_name(config: dict) -> str:
    """Find the human-readable source name without treating it as an authority."""
    imported = config.get("import") if isinstance(config.get("import"), dict) else {}
    source = imported.get("source_name")
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    if not source:
        source = corpus.get("source")
    if isinstance(source, dict):
        source = source.get("name")
    return str(source or "external source").strip()


def _later(phase: str) -> str:
    """Describe capability state without implying a completed lifecycle step."""
    code = phase.partition(" ")[0]
    if code == "P0":
        message = f"{phase} · no sealed-custody record is available"
    else:
        message = f"{phase} · not implemented · HOLD"
    return f'<p class=mut>{_esc(message)}.</p>'


def _when(value) -> str:
    """An ISO time as '16 Sep 2026, 3:13 pm'; anything else is returned as given."""
    from datetime import datetime  # noqa: PLC0415
    try:
        t = datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return str(value or "")
    return f"{t.day} {t:%b %Y}, {t.hour % 12 or 12}:{t:%M} {'am' if t.hour < 12 else 'pm'}"


def _round_words(round_id) -> str:
    """'round_01' -> 'round 1'."""
    m = re.fullmatch(r"round_0*(\d+)", str(round_id or ""))
    return f"round {m.group(1)}" if m else str(round_id or "")


_UNSURE_WORDS = {"low": "a little", "medium": "somewhat", "high": "very"}


def _unsure_words(level) -> str:
    """Unsure levels in words that do not collide with the answers high / low."""
    return _UNSURE_WORDS.get(str(level), str(level))


def _meaning_list(values: list, meanings: dict) -> str:
    items = "".join(
        f'<li><b>{_esc(v)}</b>{(" · " + _esc(meanings.get(v))) if meanings.get(v) else ""}</li>'
        for v in values
    )
    return f"<ul class=meanings>{items}</ul>" if items else "<p class=mut>not defined</p>"


def _view_model(page_src: Path) -> dict:
    root, location_note = _job_root(page_src)
    state = inspect(page_src)
    canonical = state.get("canonical_status") or {}
    config = _load_mapping(root / "config.yaml")
    cal_state = None
    if canonical and not state["canonical_integrity_errors"]:
        module = _calibration_module()
        if module is not None:
            try:
                cal_state = module.job_state(root)
            except Exception as error:  # the page must still render
                cal_state = {"error": type(error).__name__}
    return {
        "root": root, "location_note": location_note, "state": state,
        "canonical": canonical, "config": config, "cal": cal_state,
        "manifest": _read_json(root / "corpus" / "manifest.json"),
        "sealed": _read_json(root / "test" / "sealed" / "status.json"),
        "imported": _read_json(root / "corpus" / "imported_label_summary.json"),
        "runs": _run_rows(root),
        "embedding": _embedding_state(root),
    }


def _reap_when_done(proc) -> None:
    """Wait on a background build in a daemon thread, so a finished build never lingers as a zombie."""
    import threading  # noqa: PLC0415
    threading.Thread(target=proc.wait, name=f"embedding-build-{proc.pid}", daemon=True).start()


def _embedding_state(root: Path) -> dict | None:
    module = _embedding_module()
    if module is None or not root.is_dir():
        return None
    try:
        return {"builds": module.builds(root), "status": module.build_status(root)}
    except Exception as error:  # the page must still render
        return {"error": f"{type(error).__name__}: {error}"}


def _next_step(vm: dict) -> tuple[str, str]:
    """Plain words for the header line, and the Space that holds that step."""
    state, canonical, cal = vm["state"], vm["canonical"], vm["cal"] or {}
    root = vm["root"]
    if not root.exists():
        return "No labeling job on this Page yet. Ask Claude in Studio Chat to start one (/subjective-label).", "data"
    if state["canonical_integrity_errors"]:
        return "Repair needed: " + state["canonical_integrity_errors"][0], "run"
    if _imported_reference_only(vm):
        source = _import_source_name(vm["config"])
        return (
            f"{source}'s released ratings are here for reference. "
            "To collect new labels, use a separate job.",
            "data",
        )
    if state["authority_hold"]:
        return "Read-only: " + _hold_words(canonical.get("hold_reason") or state["authority_reason"]) + ".", "data"
    if canonical and canonical.get("phase") == "P0":
        if canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation":
            return "Step 1: read the label meanings and confirm them.", "data"
        return str(canonical.get("next_action") or "P0 Contract"), "data"
    if cal and cal.get("phase") == "P1":
        current = cal.get("current_round")
        if current:
            return (f"Label {_round_words(current['round_id'])}: {current['finals']} of "
                    f"{current['batch_size']} done."), "labeling"
        rounds = cal.get("rounds") or []
        if rounds and rounds[-1]["state"] == "judged":
            return (f"{_round_words(rounds[-1]['round_id']).capitalize()} is fully labeled. Next: learn the guideline and "
                    "close the round (Checkpoint Keeper, not built yet)."), "labeling"
        return "Start round 1 to begin labeling.", "labeling"
    return state["next_action"], "run"


def _data_space(vm: dict) -> dict[str, str]:
    config, manifest, sealed, imported = vm["config"], vm["manifest"], vm["sealed"], vm["imported"]
    state, canonical = vm["state"], vm["canonical"]
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    n_items = manifest.get("n_items")
    n_sealed = manifest.get("n_sealed", sealed.get("n_items"))
    n_dev = manifest.get("n_eligible")
    if n_dev is None and isinstance(n_items, int) and isinstance(n_sealed, int):
        n_dev = n_items - n_sealed

    corpus = _card("Data", "".join([
        _row("source", _esc(source.get("name") or (config.get("corpus") or {}).get("source") or "not recorded")),
        _row("items", _esc(n_items if n_items is not None else "not counted")),
        _row("to label", _esc(n_dev if n_dev is not None else "not counted")),
        _row("held back", _esc(f"{n_sealed} items for the final test; you never see them" if n_sealed is not None else "none")),
        _row("one item is", _esc((config.get("corpus") or {}).get("population") or "not described")),
        _row("embedding", _embedding_summary(vm.get("embedding"))),
    ]))
    question = construct.get("question") or construct.get("seed") or ""
    label = _card("Label", "".join([
        _row("target", f"<code>{_esc(construct.get('name') or 'not named')}</code>"),
        f'<p class=lead>{_esc(question)}</p>' if question else "",
        _meaning_list([str(v) for v in labels.get("values") or []],
                      labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}),
        (f'<p class=mut>How unsure: {_esc(" · ".join(_unsure_words(v) for v in uncertainty.get("levels") or []))}. '
         f'{_esc(uncertainty.get("meaning") or "")}</p>') if uncertainty.get("levels") else "",
    ]))

    if _imported_reference_only(vm):
        # The header carries the single source-only status. This job has no
        # local meaning gate to confirm, so don't repeat it as an alarm card.
        gate = ""
    elif state["authority_hold"]:
        gate = _card("Meaning", f'<p class=warn>Read-only: {_esc(_hold_words(canonical.get("hold_reason") or state["authority_reason"]))}.</p>'
                     '<p class=mut>Method state: <code>HOLD</code>.</p>'
                     '<p class=mut>No one can confirm a meaning or label on this job.</p>')
    elif canonical and canonical.get("meaning_receipt_valid") and canonical.get("g0_receipt_valid"):
        receipt = authority.get("meaning_receipt") if isinstance(authority.get("meaning_receipt"), dict) else {}
        gate = _card("Meaning confirmed ✓", f'<p class=ok>Caller attested as {_esc(receipt.get("human_id"))}, {_esc(_when(receipt.get("confirmed_at")))}.</p>'
                     '<p class=mut>The Board records this assertion but does not authenticate the caller\'s identity.</p>')
    elif canonical and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation":
        region_meanings = regions.get("meanings") if isinstance(regions.get("meanings"), dict) else {}
        gate = _card("Confirm the meaning", (
            "<p>Confirming records your attestation that these classes, boundary regions, "
            'and unsure levels match your intended meaning. The Board does not authenticate identity.</p>'
            '<details><summary>boundary regions</summary>'
            f'{_meaning_list([str(v) for v in regions.get("values") or []], region_meanings)}</details>'
            '<label class=attest><input type=checkbox data-confirm-attest> '
            'These meanings are what I mean.</label>'
            '<div class=actions><button class=primary type=button data-confirm-meaning disabled>Confirm meaning</button>'
            '<span class=msg role=status data-confirm-msg></span></div>'
        ), "focus")
    else:
        gate = _card("Meaning", f'<p class=mut>{_esc(state["first_failed"])}</p>')

    schema_rows = [
        _row("item id field", f"<code>{_esc(manifest.get('id_field') or (config.get('corpus') or {}).get('id_field') or 'item_id')}</code>"),
        _row("text field", f"<code>{_esc(manifest.get('text_field') or (config.get('corpus') or {}).get('text_field') or 'text')}</code>"),
        _row("context field", f"<code>{_esc(manifest.get('context_field') or (config.get('corpus') or {}).get('context_field') or '—')}</code>"),
        _row("where you read it", "items in a round: in Labeling → Rounds once shown to you; "
                                  "other items: on request in Data → Embedding (logged)", "mut"),
    ]
    imported_rows = []
    for key, value in imported.items():
        if isinstance(value, dict) and value.get("field") and isinstance(value.get("values"), dict):
            counts = " · ".join(f"{_esc(k)} {_esc(v)}" for k, v in value["values"].items())
            imported_rows.append(_row(str(value["field"]), counts))
    schema = _card("What one item holds", "".join(schema_rows))
    if imported_rows:
        unit = imported.get("unit") if isinstance(imported.get("unit"), dict) else {}
        schema += _card("Imported labels (other people's labels, not the right answer)", "".join(imported_rows) + (
            f'<p class=mut>Counted per {_esc(unit.get("row") or "source row")}.</p>'))
    reveal = (config.get("reveal") or {}).get("reference_observations") if isinstance(config.get("reveal"), dict) else None
    if isinstance(reveal, dict):
        schema += _card("What you see after you lock an answer", "".join([
            _row("from", _esc(reveal.get("label"))),
            _row("vote counts", ", ".join(f"<code>{_esc(f)}</code>" for f in reveal.get("count_fields") or [])),
            _row("other fields", ", ".join(f"<code>{_esc(f)}</code>" for f in reveal.get("item_fields") or [])),
        ]) + '<p class=mut>These are other people\'s ratings, shown to compare with yours; they are never the answer.</p>')
    return {
        "contract": label + corpus + gate,
        "schema": schema,
        "embedding": _embedding_view(vm),
    }


_GROUP_COLORS = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948",
                 "#b07aa1", "#ff9da7", "#9c755f", "#a0cbe8", "#d37295", "#bab0ac")
_LABEL_COLORS = ("var(--warn)", "var(--acc)", "var(--ok)", "#b07aa1", "#9c755f")


def _group_color(group) -> str:
    try:
        return _GROUP_COLORS[int(group) % len(_GROUP_COLORS)]
    except (TypeError, ValueError):
        return "var(--mut)"


def _model_name(model_id) -> str:
    return str(model_id or "").rsplit("/", 1)[-1]


def _thousands(value) -> str:
    return f"{value:,}" if isinstance(value, int) else str(value)


def _embedding_summary(emb: dict | None) -> str:
    builds = (emb or {}).get("builds") or []
    if not builds:
        return '<span class=mut>not built · choose a model in the Embedding view</span>'
    labels = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                             for b in builds])
    names = "<br>".join(_esc(labels[b["manifest"]["version"]]) for b in builds)
    return f'{names}<br><span class=mut>{len(builds)} built; open them in Data → Embedding</span>'


def _item_marks(root: Path) -> dict[str, dict]:
    """Which round drew each item, and its final label once the human gave one."""
    module = _calibration_module()
    marks: dict[str, dict] = {}
    if module is None:
        return marks
    try:
        for round_path in module._round_dirs(root):
            states = module._item_states(round_path)
            for row in module._read_jsonl(round_path / "human_batch.jsonl"):
                item_id = str(row.get("item_id"))
                final = (states.get(item_id) or {}).get("final")
                label = None
                if final:
                    label = (final.get("payload") or {}).get("class_label") or "unresolved"
                marks[item_id] = {"round": round_path.name, "final": label}
    except Exception:  # marks are decoration; the map renders without them
        return {}
    return marks


def _repo_relative(path: Path) -> str:
    for parent in path.resolve().parents:
        if (parent / "pyproject.toml").is_file() and (parent / "code").is_dir():
            return str(path.resolve().relative_to(parent))
    return str(path)


_SHORT_MODELS = {
    "all-MiniLM-L6-v2": "MiniLM", "all-mpnet-base-v2": "mpnet", "bge-m3": "bge-m3",
    "multilingual-e5-large-instruct": "e5-large", "Qwen3-Embedding-0.6B": "Qwen3 0.6B",
    "Qwen3-Embedding-4B": "Qwen3 4B", "Qwen3-Embedding-8B": "Qwen3 8B",
}
_TEXT_WORDS = {"reply_context": "reply + context", "reply": "reply only", "context": "context only"}


def _build_label(model_id, settings: dict | None, full: bool = True) -> str:
    """A build's name: model, which text, instruction; `full` adds groups, map, and seed when not default."""
    settings = settings or {}
    name = _model_name(model_id)
    tags = [_SHORT_MODELS.get(name, name), _TEXT_WORDS.get(settings.get("input") or "reply_context", "reply + context")]
    if settings.get("instruction"):
        tags.append("instruction")
    if not full:
        return " · ".join(tags)
    if settings.get("groups"):
        tags.append(f'{settings["groups"]} groups')
    if settings.get("map") == "pca":
        tags.append("PCA")
    if int(settings.get("seed") or 0):
        tags.append(f'seed {settings["seed"]}')
    return " · ".join(tags)


_STATE_PILL = {"built": ("ok", "built"), "building": ("acc", "building…"),
               "failed": ("warn", "failed"), "stopped": ("warn", "stopped")}


def _embedding_view(vm: dict) -> str:
    root, emb = vm["root"], vm.get("embedding")
    if emb is None:
        return _card("Embedding", "<p class=mut>The subjective-label embedding engine is not available here.</p>")
    if emb.get("error"):
        return _card("Embedding", f'<p class=warn>Could not read the embeddings: {_esc(emb["error"])}</p>')
    builds, status = emb["builds"], emb["status"]

    names = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                            for b in builds])
    chips = "".join(
        f'<button class="pill tog" type=button data-emb-show="{_esc(b["manifest"]["version"])}" '
        f'title="{_esc(b["manifest"]["model"]["id"])}: {_esc(_settings_text(b["manifest"].get("settings")))}">'
        f'{_esc(names[b["manifest"]["version"]])}</button>' for b in builds
    )
    catalog = [r for r in status if not r.get("variant") and r.get("params")]
    options = "".join(
        f'<option value="{_esc(r["id"])}" data-instruct="{"1" if r.get("instruct") else ""}"'
        f'{" selected" if r.get("recommended") else ""}>{_esc(_SHORT_MODELS.get(_model_name(r["id"]), _model_name(r["id"])))} · {_esc(r.get("download"))}'
        f'{" · recommended" if r.get("recommended") else ""}</option>'
        for r in catalog
    )
    model_info = {r["id"]: f'{r["id"]} · {r.get("note") or ""}' for r in catalog}
    form = (
        '<div class=embform data-emb-form>'
        '<div class=line><span class=lbl>Model</span><select data-emb-field=model>' + options + '</select>'
        '<button class=primary type=button data-emb-run>Run embedding</button></div>'
        '<p class="mut modelinfo" data-emb-modelinfo></p>'
        '<details class=embmore><summary>More settings</summary>'
        '<div class=line title="Which part of each item the model reads"><span class=lbl>Text</span>'
        '<button class="pill tog on" type=button data-emb-input=reply_context>Reply + context</button>'
        '<button class="pill tog" type=button data-emb-input=reply>Reply only</button>'
        '<button class="pill tog" type=button data-emb-input=context>Context only</button></div>'
        '<div class=line title="Qwen3 and e5-instruct only: tells the model what similar should mean">'
        '<span class=lbl>Instruction</span>'
        '<input class=reason data-emb-field=instruction maxlength=300 placeholder="optional"></div>'
        '<div class=line title="Leave empty and the engine picks the count"><span class=lbl>Number of groups</span>'
        '<input class="reason num" type=number min=2 max=20 data-emb-field=groups placeholder="auto"></div>'
        '<div class=line title="How the numbers are drawn flat"><span class=lbl>Map style</span>'
        '<button class="pill tog on" type=button data-emb-map=tsne>t-SNE</button>'
        '<button class="pill tog" type=button data-emb-map=pca>PCA</button></div>'
        '<div class=line title="Change it to get a different layout of the same items"><span class=lbl>Layout seed</span>'
        '<input class="reason num" type=number min=0 max=99999 value=0 data-emb-field=seed></div>'
        '</details>'
        '<p class=msg role=status data-emb-msg></p>'
        f'<script type=application/json class=embcatalog>{_script_json(model_info)}</script>'
        '</div>'
    )
    tried = []
    order = {b["manifest"]["version"]: i for i, b in enumerate(builds)}
    row_names = _unique_labels([(r["version"], r["id"], r.get("settings")) for r in status if (r.get("state") or "none") != "none"])
    for r in sorted(status, key=lambda r: order.get(r["version"], len(order))):
        state = r.get("state") or "none"
        if state == "none":
            continue
        cls, text = _STATE_PILL.get(state, ("mut", state))
        button = (f'<button class=ghost type=button data-emb-show="{_esc(r["version"])}">Show</button>'
                  if state == "built" else "")
        started, started_cls = _started_text(r.get("started")) if r.get("started") else ("not recorded", "mut")
        problem = ""
        if state in {"failed", "stopped"}:
            detail = " · ".join([str(r.get("failure") or "the build process ended early"), *(r.get("log_tail") or [])])
            problem = f'<div class=warn>{_esc(detail)}</div>'
        state_cell = ("" if state == "built" else
                      f'<span class="pill {cls} state">{_esc(text)}</span>')
        tried.append(
            f'<tr data-emb-row="{_esc(r["version"])}" data-state="{_esc(state)}">'
            f'<td title="{_esc(r.get("settings_summary") or "")}"><b>{_esc(row_names.get(r["version"]) or "")}</b>'
            f'{problem}<div class=mut><code>{_esc(r.get("run") or "")}</code></div></td>'
            f'<td class="{started_cls}">{_esc(started)}</td>'
            f'<td>{state_cell}</td><td>{button}</td></tr>'
        )
    runs_table = ('<div class=scroll><table class=runtable><thead><tr><th>Build</th><th>Started</th><th></th>'
                  '<th></th></tr></thead><tbody>' + "".join(tried) + '</tbody></table></div>') if tried else ""
    picker = (
        f'<div class="card{"" if builds else " focus"}"><h2>Embedding model<span class=tally>{len(builds)} built</span></h2>'
        + (f'<div class=line><span class=lbl>Showing</span>{chips}</div>' if builds else
           '<p>No embedding yet.</p>')
        + '<p class=mut>Nothing runs until you press <b>Run embedding</b>. Each run keeps its own folder.</p>'
        + f'<div class=runbox data-emb-formbox><h3>Run a new embedding</h3>{form}</div>'
        + (f'<details><summary>Runs on this job · {len(tried)}</summary>{runs_table}</details>' if tried else "")
        + '</div>'
    )
    started = {r["version"]: r.get("started") for r in status}
    panes = "".join(
        f'<div class=embpane data-emb="{_esc(b["manifest"]["version"])}"{"" if i == len(builds) - 1 else " hidden"}>'
        f'{_embedding_build_view(vm, {**b, "started": started.get(b["manifest"]["version"])})}</div>'
        for i, b in enumerate(builds)
    )
    return picker + panes


def _unique_labels(entries: list[tuple[str, str, dict | None]]) -> dict[str, str]:
    """key -> short build name; two builds that would read the same get their full names."""
    short = {key: _build_label(model, settings, full=False) for key, model, settings in entries}
    counts: dict[str, int] = {}
    for label in short.values():
        counts[label] = counts.get(label, 0) + 1
    return {key: (label if counts[label] == 1 else _build_label(model, settings))
            for (key, model, settings), label in zip(entries, short.values())}


def _settings_text(settings: dict | None) -> str:
    """The engine's plain sentence for a build's settings; older builds had the defaults."""
    module = _embedding_module()
    if module is None:
        return ""
    return module.settings_summary(settings or dict(module.DEFAULT_SETTINGS))


def _started_text(started: dict | None) -> tuple[str, str]:
    """Who asked for a build, in words, and the row class: a build nobody asked for is flagged."""
    started = started or {}
    person, note = started.get("person"), started.get("note")
    if started.get("via") == "run button":
        return (f"{person}, with the Run embedding button" if person
                else "with the Run embedding button (who pressed it was not recorded yet)"), ""
    if person:
        return f"from the terminal, for {person}" + (f" ({note})" if note else ""), ""
    return "from the terminal; no person's request is recorded", "warn"


_POOLING_WORDS = {
    "mean": "Average all word-piece vectors into one vector of {dim} numbers for the whole item.",
    "cls": "Keep the vector of the first word piece, where the model was trained to put a summary "
           "of the whole input: one vector of {dim} numbers.",
    "lasttoken": "Keep the vector of the last word piece, which has read the whole input: "
                 "one vector of {dim} numbers.",
}


_MAP_NAMES = {"tsne": "t-SNE", "pca": "PCA"}


def _piece(text) -> str:
    """A word piece as shown: a newline becomes ↵ and a bare space ␣, so no chip looks empty."""
    text = str(text).replace("\n", "↵")
    return text if text.strip() else "␣"


def _settings_flags(settings: dict) -> str:
    """The CLI flags that rebuild exactly these settings; defaults are left out."""
    import shlex  # noqa: PLC0415
    flags = []
    if settings.get("input") and settings["input"] != "reply_context":
        flags.append(f'--input {settings["input"]}')
    if settings.get("instruction"):
        flags.append(f'--instruction {shlex.quote(str(settings["instruction"]))}')
    if settings.get("groups"):
        flags.append(f'--groups {int(settings["groups"])}')
    if settings.get("map") and settings["map"] != "tsne":
        flags.append(f'--map {settings["map"]}')
    if int(settings.get("seed") or 0):
        flags.append(f'--seed {int(settings["seed"])}')
    return "".join(" " + f for f in flags)


def _embedding_build_view(vm: dict, emb: dict) -> str:
    root, config = vm["root"], vm["config"]
    m = emb["manifest"]
    model_id = str(m["model"]["id"])
    model_name = model_id.rsplit("/", 1)[-1]
    settings = m.get("settings") or {}
    command = ("python Tools/plugins/subjective-label/engine/embedding_build.py build "
               f"--job-root {_repo_relative(root)} --started-by <your name> --model {model_id}"
               + _settings_flags(settings))
    dim = m["model"]["dim"]
    pre = m.get("preprocessing") or {}
    enc = m.get("encoder") or {}
    pop = m.get("population") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    text_field = pre.get("text_field") or "text"
    context_field = pre.get("context_field") or "context"
    n = pop.get("eligible_embedded")

    steps = [
        ("Item", f'<code>{_esc(text_field)}</code> is the response to judge; '
                 f'<code>{_esc(context_field)}</code> is the conversation before it.'
                 + (f' <span class=mut>One item is {_esc(corpus.get("population"))}.</span>'
                    if corpus.get("population") else "")),
        ("Input", {"reply": "Use the reply only; the context is left out.",
                   "context": "Use the context only; the reply is left out."}.get(
                       pre.get("input"), "Join them: the response, a blank line, then the context. "
                                         "The response goes first, so a cut can never remove it.")),
    ]
    if pre.get("prompt"):
        steps.append(("Instruction", f'Put <code>{_esc(pre["prompt"])}</code> in front of every input, '
                                     'so the model reads each item with that task in mind.'))
    modules = {step.get("module"): step for step in enc.get("steps") or []}
    if enc.get("max_tokens"):
        cut = enc.get("items_cut") or 0
        steps.append(("Word pieces", (
            f'The tokenizer splits the input into word pieces. The model reads at most '
            f'{_esc(_thousands(enc["max_tokens"]))}. ' + (
                f'{_esc(cut)} of {_esc(n)} items are longer (longest {_esc(_thousands(enc.get("longest_tokens")))}), '
                'so the end of their context is cut.' if cut else 'No item is longer than that.'))))
    params = m["model"].get("params")
    steps.append(("Model", f'<code>{_esc(model_name)}</code>' + (f' ({_esc(params)} parameters)' if params else "")
                           + f' reads all word pieces together and gives each one {_esc(_thousands(dim))} numbers.'))
    if "Pooling" in modules:
        mode = str(modules["Pooling"].get("mode") or "mean")
        words = _POOLING_WORDS.get(mode, "Combine the word-piece vectors (" + mode + ") into one vector of {dim} numbers.")
        steps.append(("Pooling", _esc(words.format(dim=_thousands(dim)))))
    if "Normalize" in modules or pre.get("normalize") == "l2":
        steps.append(("Length 1", "Scale the vector to length 1, so the similarity of two items "
                                  "(0 unrelated, 1 the same) is a plain dot product."))
    steps.append(("Saved", f'Row r of <code>vectors.npy</code> ({_esc(n)} × {_esc(_thousands(dim))}) is row r of '
                           '<code>rows.jsonl</code> (item id, text hash, word-piece count).'))
    recipe_rows = "".join(_row(f"{i} · {name}", body) for i, (name, body) in enumerate(steps, start=1))
    recipe = (
        f'<div class="card"><h2>From item to vector<span class=tally>{_esc(model_name)} · {_esc(_thousands(dim))} numbers</span></h2>'
        f'{recipe_rows}'
        f'<p class=mut>The {_esc(pop.get("sealed_excluded", 0))} held-back test items are never embedded. '
        'A vector only says which items are near each other; it never sets a label.</p></div>'
    )

    ex = m.get("example") or {}
    example = ""
    if ex.get("input"):
        pieces = ex.get("word_pieces") or []
        numbers = ", ".join(f"{v:.4f}" for v in ex.get("vector_first") or [])
        example = (
            f'<div class="card"><h2>Worked example<span class=tally>made up, not a corpus item</span></h2>'
            + _row("1 · input", f'<code>{_esc(ex["input"])}</code>')
            + (_row(f"2 · {len(pieces)} word pieces",
                    '<span class=pieces>' + "".join(f'<code class=wp>{_esc(_piece(t))}</code>' for t in pieces) + '</span>')
               if pieces else "")
            + _row("3 · vector", f'<code>[{_esc(numbers)}, …]</code> '
                                 f'<span class=mut>first 8 of {_esc(_thousands(ex.get("dim")))} numbers</span>')
            + _row("4 · length", f'<code>{_esc(ex.get("length"))}</code>')
            + '</div>'
        )

    groups = emb.get("groups") or {}
    group_rows = groups.get("groups") or []
    points = emb.get("map") or []
    marks = _item_marks(root)
    schema_labels = [str(v) for v in ((config.get("labels") or {}).get("values") or [])] \
        if isinstance(config.get("labels"), dict) else []
    label_color = {v: _LABEL_COLORS[i % len(_LABEL_COLORS)] for i, v in enumerate(schema_labels)}
    label_color["unresolved"] = "var(--fg)"
    width, height, pad = 1000, 600, 16
    circles = []
    for point in points:
        item_id = str(point.get("item_id"))
        mark = marks.get(item_id) or {}
        x = pad + float(point.get("x") or 0) * (width - 2 * pad)
        y = pad + float(point.get("y") or 0) * (height - 2 * pad)
        g = point.get("group")
        final = mark.get("final")
        lc = label_color.get(final, "var(--mut)") if final else "var(--mut)"
        cls = "pt" + (" drawn" if mark else "") + (" done" if final else "")
        tip = f'item {item_id} · G{int(g) + 1 if isinstance(g, int) else "?"}'
        if mark:
            tip += f' · {mark["round"]}' + (f' · final: {final}' if final else " · not labeled yet")
        circles.append(
            f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="7" data-item="{_esc(item_id)}" '
            f'data-group="{_esc(g)}" style="--gc:{_group_color(g)};--lc:{lc}"><title>{_esc(tip)}</title></circle>'
        )
    drawn = sum(1 for p in points if str(p.get("item_id")) in marks)
    done = sum(1 for p in points if (marks.get(str(p.get("item_id"))) or {}).get("final"))
    group_legend = "".join(
        f'<button class=leg type=button data-group-pick="{int(r["group"])}">'
        f'<i class=dot style="background:{_group_color(r["group"])}"></i>G{int(r["group"]) + 1} '
        f'<span class=kw>{_esc(" · ".join(_clean_keywords(r.get("keywords"))[:2]))}</span></button>'
        for r in group_rows
    )
    pane_data = {
        "version": m.get("version"),
        "groups": {str(int(r["group"])): {"name": f'G{int(r["group"]) + 1}', "color": _group_color(r["group"]),
                                          "keywords": _clean_keywords(r.get("keywords")), "size": r.get("size")}
                   for r in group_rows},
        "marks": {item: {"round": mk.get("round"), "final": mk.get("final")} for item, mk in marks.items()},
        "label_colors": label_color,
        "points3d": [[str(r.get("item_id")), r.get("x"), r.get("y"), r.get("z"),
                      next((pt.get("group") for pt in points if str(pt.get("item_id")) == str(r.get("item_id"))), None)]
                     for r in emb.get("map3d") or []],
    }
    has3d = bool(pane_data["points3d"])
    label_legend = "".join(
        f'<span><i class=dot style="background:{c}"></i>{_esc(v)}</span>' for v, c in label_color.items()
        if v != "unresolved" or any((mk.get("final") == "unresolved") for mk in marks.values())
    ) + '<span><i class="dot faint"></i>not labeled</span>'
    mapcard = (
        f'<div class="card mapwrap" data-color=group><h2>Map<span class=tally>{_esc(len(points))} items · '
        f'{_esc(groups.get("k"))} groups</span></h2>'
        '<div class=line><span class=lbl>Color by</span>'
        '<button class="pill tog on" type=button data-map-color=group>Group</button>'
        '<button class="pill tog" type=button data-map-color=label>Your labels</button></div>'
        '<div class=line><span class=lbl>Show</span>'
        '<button class="pill tog on" type=button data-map-show=all>All items</button>'
        f'<button class="pill tog" type=button data-map-show=round title="Only the items a round picked for you to label">Picked for labeling ({_esc(drawn)})</button>'
        '<span class=zoomctl>'
        + ('<button class="pill tog on" type=button data-map-dim=2d>2D</button>'
           '<button class="pill tog" type=button data-map-dim=3d>3D</button>'
           '<button class="pill tog" type=button data-spin hidden>Spin</button>' if has3d else '')
        + '<button class="pill tog" type=button data-zoom=in aria-label="Zoom in" title="Zoom in (or pinch)">+</button>'
        '<button class="pill tog" type=button data-zoom=out aria-label="Zoom out" title="Zoom out">−</button>'
        '<button class="pill tog" type=button data-zoom=reset>Reset</button></span></div>'
        f'<svg class=map viewBox="0 0 {width} {height}" role=img title="Drag to move" '
        f'aria-label="Map of {_esc(len(points))} development items"><g class=zoom><g class=links></g>'
        f'{"".join(circles)}</g></svg>'
        + (f'<canvas class=map3d hidden role=img aria-label="3D map of {_esc(len(points))} development items"></canvas>'
           if has3d else '')
        + f'<div class="legend group">{group_legend}</div>'
        f'<div class="legend label">{label_legend}</div>'
        '<div class=pick data-pick hidden></div>'
        f'<ul class="mut notes"><li>Click a dot to see its group and the most similar items; click a group to light it up.'
        f'{" In 3D, drag to turn the cloud or press Spin." if has3d else ""}</li>'
        f'<li>A dark ring means a round picked it for you to label ({_esc(drawn)} picked, {_esc(done)} labeled).</li>'
        f'<li>Only distance matters: {_esc(_thousands(dim))} numbers are squeezed into 2{" (3 in 3D)" if has3d else ""} with '
        f'{_esc(_MAP_NAMES.get(str((m.get("map") or {}).get("method")), "t-SNE"))}, so the axes mean nothing.</li></ul>'
        f'<script type=application/json class=embdata>{_script_json(pane_data)}</script></div>'
    )

    records = []
    for r in group_rows:
        g = int(r["group"])
        ids = [str(p.get("item_id")) for p in points if p.get("group") == g]
        in_round = [marks[i] for i in ids if i in marks]
        finals = [mk["final"] for mk in in_round if mk.get("final")]
        tally = " · ".join(f"{v} {finals.count(v)}" for v in [*schema_labels, "unresolved"] if finals.count(v))
        records.append(
            f'<tr class=grp data-group-pick="{g}" tabindex=0>'
            f'<td><span class=rid><i class=dot style="background:{_group_color(g)}"></i>G{g + 1}</span></td>'
            f'<td><b>{_esc(" · ".join(_clean_keywords(r.get("keywords"))) or "no distinctive words")}</b>'
            f'<div class=exbox data-no-light><button class="pill tog" type=button data-ex-group="{g}">'
            f'Show typical items</button></div></td>'
            f'<td class=num data-label=items>{_esc(r.get("size"))}</td><td class=num data-label=picked>{len(in_round)}</td>'
            f'<td class=num data-label=labeled>{len(finals)}{f" <span class=mut>({_esc(tally)})</span>" if tally else ""}</td></tr>'
            f'<tr class=exrow hidden><td colspan=5 data-no-light><div class=exs data-ex-list="{g}"></div></td></tr>'
        )
    clarity = _group_clarity(groups)
    groupcard = (
        '<div class="card"><h2>Groups<span class=tally>k-means on the vectors</span></h2>'
        + clarity
        + '<div class=scroll><table class=grptable><thead><tr><th>Group</th><th>Keywords</th><th>Items</th>'
        '<th>Picked</th><th>Labeled</th></tr></thead><tbody>' + "".join(records) + '</tbody></table></div>'
        '<ul class="mut notes"><li>Click a row to light that group up on the map.</li>'
        '<li>Keywords are words more common in the group than overall; in item text they are highlighted.</li>'
        '<li><b>Show typical items</b> shows the items most similar to the group\'s centre. Items waiting in a round '
        'stay hidden until you label them; each item shown is logged in <code>exposure/group_examples.jsonl</code>.</li>'
        '<li>Groups never choose which items you label.</li></ul></div>'
    )

    files = ", ".join(f'<code>{_esc(f.get("path"))}</code>' for f in m.get("files") or [])
    scores = groups.get("silhouette_by_k") or {}
    started_words, started_cls = _started_text(emb.get("started"))
    record = _card("Build record", "".join([
        _row("run", f'<code>{_esc(m.get("run"))}</code>'),
        _row("built", _esc(_when(m.get("created_at")))),
        _row("started", _esc(started_words), started_cls),
        _row("model", f'<code>{_esc(model_id)}</code> · {_esc(m["model"].get("device"))} · '
                      f'{_esc(m["model"].get("dtype") or "float32")}'
                      + (f' · {_esc(m["model"]["license"])}' if m["model"].get("license") else "")),
        _row("folder", f'<code>{_esc(_repo_relative(emb["folder"]))}/</code>'),
        _row("files", f'<code>manifest.json</code>, {files}'),
        _row("map", f'{_esc((m.get("map") or {}).get("method"))}, seed {_esc((m.get("map") or {}).get("seed"))}'),
        _row("groups", f'k = {_esc(groups.get("k"))}, set in the run settings' if settings.get("groups") else
                       f'k = {_esc(groups.get("k"))}, the best of k = {_esc(min(scores, key=int) if scores else "?")} '
                       f'to {_esc(max(scores, key=int) if scores else "?")} by silhouette'),
        _row("rebuild", f'<code>{_esc(command)}</code> <span class=mut>(same settings and corpus: no change)</span>'),
    ]))
    who = (emb.get("started") or {}).get("person")
    built_line = f'built {_when(m.get("created_at"))}' + (f' by {who}' if who else "")
    return (mapcard + groupcard
            + f'<details class=fold><summary>How the map is made: from text to numbers</summary>{recipe}{example}</details>'
            + f'<details class=fold><summary>Technical details · {_esc(built_line)}</summary>{record}</details>')


def _round_draw(root: Path, round_id: str) -> dict:
    """What the draw froze for one round: how it was drawn, and which items it picked."""
    module = _calibration_module()
    path = root / "rounds" / round_id
    draw: dict = {"items": [], "card": {}, "manifest": {}}
    if module is None or not path.is_dir():
        return draw
    try:
        manifest = _load_mapping(path / "manifest.yaml")
        card = {}
        if (path / "card.md").is_file():
            for line in (path / "card.md").read_text(encoding="utf-8").splitlines():
                if ": " in line and not line.startswith(("#", "-", " ")):
                    key, value = line.split(": ", 1)
                    card[key.strip()] = value.strip()
        states = module._item_states(path)
        config = _load_mapping(root / "config.yaml")
        corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
        text_field = str(corpus.get("text_field") or "text")
        context_field = str(corpus.get("context_field") or "context_prev")
        rows = {str(r.get("item_id")): r for r in module._corpus_rows(root)}
        notes: dict = {}
        for note in module._read_jsonl(path / "sessions" / "feedback.jsonl"):
            notes.setdefault(str(note.get("item_id")), []).append(note)
        items = []
        for row in module._read_jsonl(path / "human_batch.jsonl"):
            item_id = str(row.get("item_id"))
            entry = states.get(item_id) or {}
            final = entry.get("final")
            shown = "show" in (entry.get("kinds") or [])
            source = rows.get(item_id) or {}
            items.append({
                "item_id": item_id, "order": row.get("order"),
                "probability": row.get("selection_probability"),
                "label": ((final or {}).get("payload") or {}).get("class_label") or ("unresolved" if final else None),
                "first": ((entry.get("first") or {}).get("payload") or {}).get("class_label"),
                "state": "labeled" if final else ("answered" if entry.get("first") else "waiting"),
                # text only once the person has been shown the item, so the table never shows it first
                "text": str(source.get(text_field) or "") if shown else None,
                "context": str(source.get(context_field) or "") if shown else None,
                "feedback": notes.get(item_id, []),
            })
        draw.update({"items": items, "card": card, "manifest": manifest})
    except Exception:  # the page must still render
        return draw
    return draw


def _turns_html(context: str) -> str:
    """Earlier conversation turns, one line per speaker, folded under an item's text."""
    out = []
    for line in str(context or "").splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z][A-Za-z_ ]{0,20}):\s?(.*)$", line)
        who, body = (m.group(1), m.group(2)) if m else ("", line)
        if who.strip().lower() in {"lamda", "assistant", "bot", "chatbot", "ai", "model", "gpt", "claude"}:
            who = "AI"
        out.append(f'<div class=turn>{f"<b>{_esc(who)}</b>" if who else ""}<span>{_esc(body)}</span></div>')
    return "".join(out)


def _draw_sentence(draw: dict, pool) -> str:
    parts = [f'{draw.get("method") or "random"} draw']
    if pool:
        parts.append(f"from the {pool} items to label")
    if draw.get("seed") is not None:
        parts.append(f'seed {draw["seed"]}')
    return ", ".join(parts)


_FRAGMENTS = {"don", "doesn", "didn", "isn", "wasn", "aren", "weren", "couldn", "wouldn", "shouldn",
              "haven", "hasn", "hadn", "won", "ain", "ll", "ve", "re"}


def _clean_keywords(words) -> list[str]:
    """Group keywords without contraction fragments (don, doesn) that read as typos."""
    return [str(w) for w in words or [] if str(w).lower() not in _FRAGMENTS]


def _policy_words(version) -> str:
    """'G_00' -> 'G_00, the first draft'; later versions keep their number."""
    version = str(version or "")
    return f"{version}, the first draft" if version == "G_00" else version


def _map_groups(vm: dict) -> tuple[dict, dict, str]:
    """Each item's group in the newest embedding build, each group's keywords, and the build's name."""
    builds = ((vm.get("embedding") or {}).get("builds")) or []
    if not builds:
        return {}, {}, ""
    newest = builds[-1]
    groups = {str(row.get("item_id")): row.get("group") for row in newest.get("map") or []}
    keywords = {int(g["group"]): " · ".join(_clean_keywords(g.get("keywords"))[:4])
                for g in (newest.get("groups") or {}).get("groups") or []}
    return groups, keywords, _build_label(newest["manifest"]["model"]["id"], newest["manifest"].get("settings"))


def _items_table(draw: dict, groups: dict, keywords: dict) -> str:
    """One row per drawn item: # · Item · Text · Group · State · Feedback."""
    records = []
    for item in draw["items"]:
        group = groups.get(item["item_id"])
        if item["state"] == "labeled":
            pill = f'<span class="pill ok">{_esc(item["label"])}</span>'
        elif item["state"] == "answered":
            pill = f'<span class="pill acc">first: {_esc(item["first"])}</span>'
        else:
            pill = '<span class="pill mut">waiting</span>'
        group_tag = (f'<span class="pill mut" title="{_esc(keywords.get(int(group), ""))}">'
                     f'<i class=dot style="background:{_group_color(group)}"></i>'
                     f'G{int(group) + 1}</span>') if group is not None else ""
        if item.get("text") is None:
            text_cell = '<span class=mut>not opened yet</span>'
        else:
            text_cell = (f'<div class=reply>{_esc(item["text"])}</div>'
                         + (f'<details class=ctx><summary>conversation before it</summary>'
                            f'<div class=convo>{_turns_html(item["context"])}</div></details>' if item.get("context") else ""))
        notes_cell = "".join(
            f'<div class=fb><b>{"Model" if n.get("author") == "model" else "You"}</b> {_esc(n.get("text"))}</div>'
            for n in item.get("feedback") or []) or '<span class=mut>—</span>'
        records.append(
            f'<tr><td class=num>#{_esc((item.get("order") or 0) + 1)}</td><td class=nowrap>item {_esc(item["item_id"])}</td>'
            f'<td>{text_cell}</td><td>{group_tag}</td><td>{pill}</td><td>{notes_cell}</td></tr>'
        )
    return ('<div class=scroll><table class=items><thead><tr><th>#</th><th>Item</th><th>Text</th><th>Group</th><th>State</th>'
            '<th>Feedback</th></tr></thead>'
            f'<tbody>{"".join(records)}</tbody></table></div>')


def _job_where(vm: dict) -> str:
    """The job folder relative to the repo, as a chat in this repo would type it."""
    root = vm["root"]
    module = _calibration_module()
    repo = module._repo_root(root) if module else None
    try:
        return str(root.relative_to(repo)) if repo else str(root)
    except ValueError:
        return str(root)


def _chat_prompt(vm: dict, current: dict, draw: dict) -> str:
    """The text to paste into a Claude chat to go on labeling this round; it writes nothing."""
    root, config = vm["root"], vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = (config.get("labels") or {}).get("values") if isinstance(config.get("labels"), dict) else None
    human = ((config.get("authority") or {}) if isinstance(config.get("authority"), dict) else {}).get("human_id") or "me"
    tag = lambda i: f'#{(i.get("order") or 0) + 1} item {i["item_id"]}'
    finals = [f'{tag(i)} (first: {i["first"]})' for i in draw["items"] if i["state"] == "answered"]
    todo = [tag(i) for i in draw["items"] if i["state"] == "waiting"][:5]
    lines = [
        f'Continue labeling {_round_words(current.get("round_id"))} of {root.parent.name} with me ({human}).',
        f"Job folder: {_job_where(vm)}",
        f'Question: {construct.get("question") or construct.get("name") or ""}'
        + (f'  Labels: {" · ".join(str(v) for v in labels)}' if labels else ""),
        f'Progress: {current.get("finals", 0)} of {current.get("batch_size", len(draw["items"]))} labeled.',
    ]
    if finals:
        lines.append("Waiting for my final: " + ", ".join(finals))
    if todo:
        lines.append("Next items: " + ", ".join(todo))
    lines += [
        "",
        'Follow /label-building-workflow, JUDGE "By chat" (engine/calibration.py):',
        "1. Show me the next items (conversation and AI reply); open_item for any item not shown yet.",
        "2. Record only what I say: record_first for my first answer, then show the raters' votes and your view.",
        "3. record_final when I keep or change; add_feedback for a note about an item.",
        "Never show the votes or your view before my first answer is recorded.",
    ]
    return "\n".join(lines)


def _definition_prompt(vm: dict, focus: str | None = None) -> str:
    """The text to paste into a Claude chat to define the labels better; it writes nothing."""
    config = vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    values = [str(v) for v in labels.get("values") or []]
    meanings = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    region_meanings = regions.get("meanings") if isinstance(regions.get("meanings"), dict) else {}
    between = [str(r) for r in regions.get("values") or [] if len(str(r)) > 1]
    lines = [
        f'Help me define the labels of {vm["root"].parent.name} better. I am {authority.get("human_id") or "the labeler"}, '
        "the person who decides what they mean.",
        f"Job folder: {_job_where(vm)}",
        f'Question: {construct.get("question") or construct.get("name") or ""}',
    ]
    rule = " ".join(str(x) for x in (construct.get("seed"), construct.get("scope")) if x)
    if rule:
        lines.append(f"Rule: {rule}")
    lines.append("Labels now:")
    lines += [f"- {v}: {meanings.get(v) or 'no meaning written yet'}" for v in values]
    if between:
        lines.append("In-between cases: " + "; ".join(f"{r} = {region_meanings.get(r) or r}" for r in between))
    if uncertainty.get("levels"):
        lines.append("How sure: " + " · ".join(_unsure_words(v) for v in uncertainty["levels"]) + " unsure. "
                     + str(uncertainty.get("meaning") or ""))
    current = vm["root"] / "policy" / "current"
    policy = current.read_text(encoding="utf-8").strip() if current.is_file() else ""
    if policy:
        lines.append(f"Guideline: policy/versions/{policy}/guideline.md")
    lines.append("")
    if focus in values:
        i = values.index(focus)
        near = [v for v in (values[i - 1] if i else None, values[i + 1] if i + 1 < len(values) else None) if v]
        lines.append(f'Focus on "{focus}". Ask me, one question at a time, what makes a reply {focus} and not '
                     f'{" or ".join(near) or "another label"}. Propose clearer wording, one example, and one counterexample.')
    elif focus == "between":
        lines.append("Focus on in-between cases. Ask me how to handle a reply that fits two labels, "
                     "and propose one boundary test for each pair.")
    else:
        lines.append("Ask me questions, one at a time, to find where these definitions are unclear. "
                     "Propose clearer wording, one change at a time.")
    lines += [
        "Write nothing until I approve. The meanings in config.yaml are confirmed (G0), so an approved change "
        "becomes a guideline patch in policy_draft/ for the LEARN step (/label-building-workflow), never an edit to config.yaml.",
        "Do not say how you would label any round item before my first answer for it is recorded.",
    ]
    return "\n".join(lines)


def _label_discussion_prompt(vm: dict) -> str:
    """A full, copyable brief for discussing this task in the user's chat."""
    config = vm.get("config") or {}
    project = config.get("project") if isinstance(config.get("project"), dict) else {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    source = corpus.get("source") if isinstance(corpus.get("source"), dict) else {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    reveal = config.get("reveal") if isinstance(config.get("reveal"), dict) else {}
    reference = reveal.get("reference_observations")
    reference = reference if isinstance(reference, dict) else {}
    meanings = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    task = project.get("board_page") or vm["root"].parent.name
    dataset = source.get("name") or corpus.get("source_name") or "the configured corpus"
    question = construct.get("question") or construct.get("name") or "the label question"
    lines = [
        "I want to discuss this labeling task with you, not label the whole dataset.",
        f"Task: {task}",
        f"Dataset: {dataset}",
    ]
    if corpus.get("population"):
        lines.append(f"Example unit: {corpus['population']}")
    lines.append(f"Question: {question}")
    if construct.get("seed"):
        lines.append(f"Judging instruction: {construct['seed']}")
    if construct.get("scope"):
        lines.append(f"Scope: {construct['scope']}")
    lines.append("Current labels and meanings:")
    lines.extend(
        f"- {value}: {meanings.get(value) or 'no meaning written yet'}"
        for value in labels.get("values") or []
    )
    if reference.get("label"):
        lines.append(
            f"Reference only: {reference['label']}; it is comparison data, not gold."
        )
    lines.extend([
        "Please help me discuss whether these definitions and boundaries are clear. "
        "Ask one question at a time. If I paste an example, discuss how the current "
        "definitions apply; do not record a label or change the labels, data, or guideline.",
    ])
    return "\n".join(str(line) for line in lines)


def _chat_icon(prompt: str, title: str) -> str:
    return f'<button class=cc type=button title="{_esc(title)}" data-copy="{_esc(prompt)}">⧉ chat</button>'


def _label_definitions(vm: dict) -> str:
    """Labeling → Label: what each label means, with chat prompts to define them better."""
    config = vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    values = [str(v) for v in labels.get("values") or []]
    if not values:
        return _card("Label definitions", "<p class=mut>No labels are written in config.yaml yet.</p>")
    meanings = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    region_meanings = regions.get("meanings") if isinstance(regions.get("meanings"), dict) else {}
    between = [str(r) for r in regions.get("values") or [] if len(str(r)) > 1]
    receipt = authority.get("meaning_receipt") if isinstance(authority.get("meaning_receipt"), dict) else {}
    confirmed = (f'by {_esc(receipt.get("human_id"))}, {_esc(_when(receipt.get("confirmed_at")))}'
                 if receipt.get("confirmed_at") else "not yet (Data → Contract)")
    rows = "".join(
        f'<tr><td class=nowrap><b>{_esc(v)}</b></td><td>{_esc(meanings.get(v) or "no meaning written yet")}</td>'
        f'<td>{_chat_icon(_definition_prompt(vm, v), f"Copy a chat prompt about {v}")}</td></tr>' for v in values)
    between_rows = "".join(
        f'<tr><td class=nowrap><code>{_esc(r)}</code></td><td>{_esc(region_meanings.get(r) or "")}</td></tr>'
        for r in between)
    return _card("Label definitions", "".join([
        _row("question", _esc(construct.get("question") or construct.get("name") or "")),
        '<div class=chatcopy><button class=primary type=button '
        'aria-label="Copy prompt to discuss here" title="Copy this prompt for your Codex chat" '
        f'data-copy="{_esc(_label_discussion_prompt(vm))}">⧉ Copy prompt to discuss here</button>'
        '<span class=mut>Copy, then paste into this Codex chat. Nothing is sent automatically.</span></div>',
        _row("judge", _esc(construct.get("seed"))) if construct.get("seed") else "",
        _row("scope", _esc(construct.get("scope"))) if construct.get("scope") else "",
        _row("confirmed", confirmed),
        '<div class=scroll><table class=defs><thead><tr><th>Label</th><th>What it means</th><th>Chat</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>',
        (f'<h3 class=sub>In-between cases {_chat_icon(_definition_prompt(vm, "between"), "Copy a chat prompt about in-between cases")}</h3>'
         '<div class=scroll><table class=defs><thead><tr><th>Case</th><th>What it means</th></tr></thead>'
         f'<tbody>{between_rows}</tbody></table></div>') if between else "",
        (f'<p class=mut>How sure: {_esc(" · ".join(_unsure_words(v) for v in uncertainty["levels"]))} unsure. '
         f'{_esc(uncertainty.get("meaning") or "")}</p>') if uncertainty.get("levels") else "",
        '<p class=mut>A change agreed in chat becomes a guideline patch for the LEARN step; '
        'these confirmed meanings stay as they are until then.</p>',
    ]))


def _discussion_prompt(vm: dict) -> str:
    """Safe, human-facing brief for one discussion; it never includes item text."""
    config = vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    mode = str(authority.get("mode") or "")
    question = construct.get("question") or construct.get("seed") or construct.get("name") or "the label meaning"
    if mode == "external_annotation_import":
        question = "How should we interpret the released source labels without changing their meaning?"
    values = [str(v) for v in labels.get("values") or []]
    lines = [
        f"Help me run one human-AI discussion for {vm['root'].parent.name}.",
        f"Discussion question: {question}",
        "Goal: use a small set of representative, boundary, and counterexample cases to clarify the meaning.",
        "Do not make a label decision before I have described what I notice.",
        "Ask one question at a time. After each answer, summarize the boundary you heard and ask whether it is right.",
        "At the end, propose one smallest guideline change, two reusable examples, and one unresolved question.",
        f"Label values currently visible: {' · '.join(values) if values else 'not defined'}.",
    ]
    if mode == "external_annotation_import":
        lines += [
            "This is an external annotation import. Treat source values as observations, not local human gold.",
            "Do not write policy/current, gold, or a checkpoint from this discussion.",
        ]
    else:
        lines.append("Any accepted semantic change must go through the guideline-learn and human gate; do not edit config.yaml in chat.")
    return "\n".join(lines)


def _discussion_view(vm: dict) -> str:
    """The discussion-first entry view for Labeling Space.

    This is intentionally a projection only: it plans a discussion and explains
    the future Run envelope without allocating a Run or promoting a label.
    """
    config = vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    mode = str(authority.get("mode") or "")
    hold = bool((vm.get("state") or {}).get("authority_hold"))
    cal = vm.get("cal") or {}
    current = cal.get("current_round") or {}
    question = construct.get("question") or construct.get("seed") or construct.get("name") or "Define the label meaning"
    if mode == "external_annotation_import":
        question = "How should we read the released DICES-350 safety labels without changing their meaning?"
        why = ("This page contains external rater observations. The first discussion is about separating "
               "source meanings, uncertainty, and expert reference—not about creating new local gold.")
        action = "Copy discussion brief"
        status = "Read-only discussion"
    elif current:
        why = "Continue the current discussion and record the decisions that should shape the next guideline version."
        action = "Continue discussion"
        status = "Discussion in progress"
    else:
        why = ("Start with a small case set. The purpose is to discover the semantic boundary before asking a person "
               "to label a larger batch.")
        action = "Copy discussion brief"
        status = "Ready to discuss"

    values = [str(v) for v in labels.get("values") or []]
    value_text = " · ".join(values) if values else "label values not written yet"
    cases = [
        ("01", "Representative", "A clear case that makes the current meaning concrete."),
        ("02", "Boundary", "A case where two readings are plausible and the rule needs a test."),
        ("03", "Counterexample", "A case that looks similar on the surface but should receive a different reading."),
    ]
    if mode == "external_annotation_import":
        cases[0] = ("01", "Source meaning", "What does the released Yes / No observation actually say?" )
        cases[1] = ("02", "Uncertainty", "Why does Unsure remain different from No or NONE?" )
        cases[2] = ("03", "Separate field", "How should degree of harm stay separate from overall safety?" )

    case_html = "".join(
        f'<article class=casecard><div class=caseid>Example {num}</div>'
        f'<h3>{_esc(kind)}</h3><p>{_esc(desc)}</p>'
        '<p class="mut">The item is opened in the discussion chat when you choose it.</p></article>'
        for num, kind, desc in cases
    )
    flow = "".join(
        f'<div class="flowstep {"now" if i == 1 else ""}"><b>{i}</b><strong>{_esc(title)}</strong><span>{_esc(desc)}</span></div>'
        for i, (title, desc) in enumerate((
            ("Choose the question", "name the uncertainty we want to resolve"),
            ("Discuss examples", "human speaks first; AI asks and compares"),
            ("Save decisions", "record the boundary and unresolved cases"),
            ("Learn the guideline", "draft the smallest rule change"),
        ), 1)
    )
    planned = [
        ("rlNN_round-prepare", "freeze the question and example packet", "planned"),
        ("rlNN_discussion-calibration", "the human-AI discussion", "main discussion"),
        ("rlNN_guideline-learn", "turn accepted discussion into a rule proposal", "after discussion"),
        ("rlNN_round-close", "close the round or name the next question", "checkpoint"),
    ]
    run_html = "".join(
        f'<div class=runplan><code>{_esc(name)}</code><span>{_esc(desc)}</span><em>{_esc(state)}</em></div>'
        for name, desc, state in planned
    )
    guard = ("This imported page can discuss the source, but it cannot create local gold or change the guideline."
             if hold else "A discussion draft is not a label. The configured semantic authority must review and explicitly attest before a semantic change is recorded. This Board does not authenticate the caller.")
    brief = _discussion_prompt(vm)
    return "".join([
        _card("Current discussion", (
            f'<div class=discstatus><span class=pill acc>{_esc(status)}</span>'
            f'<span class=mut>{_esc(value_text)}</span></div>'
            f'<h3 class=discquestion>{_esc(question)}</h3>'
            f'<p class=lead>{_esc(why)}</p>'
            '<div class=actions><button class=primary type=button '
            f'data-copy="{_esc(brief)}">{_esc(action)}</button>'
            '<span class=msg role=status data-discussion-msg></span></div>'
            '<p class=mut>Copy this brief into Studio Chat to start the conversation. The chat is the conversation; this page keeps the plan and receipt.</p>'
        ), "focus"),
        _card("How this works", f'<div class=flow>{flow}</div>'
              '<p class=mut>One discussion may use several examples. The examples are events inside one Run; they are not separate Runs.</p>'),
        _card("Example packet", '<p class=lead>Start small: one clear case, one boundary case, and one counterexample.</p>'
              f'<div class=casegrid>{case_html}</div>'),
        _card("What gets recorded", "".join([
            _row("discussion question", _esc(question)),
            _row("examples", "3 discussion cases · representative · boundary · counterexample"),
            _row("human input", "what you noticed, what changed your mind, and what remains unresolved"),
            _row("AI output", "a proposed rule patch and reusable examples; never automatic gold"),
            _row("next", "accept the patch, continue the discussion, or open a new round"),
            f'<p class=warn>{_esc(guard)}</p>',
        ])),
        _card("Run plan", '<p class=mut>These are the planned envelopes for the discussion. They are not allocated Tickets yet.</p>'
              f'<div class=runplans>{run_html}</div>'
              '<p class=mut>Use Run Space to audit the envelopes after a real operation starts.</p>'),
    ])


def _rounds_view(vm: dict) -> str:
    cal, root = vm["cal"] or {}, vm["root"]
    rounds = cal.get("rounds") or []
    if not rounds:
        return _card("Rounds", "<p class=mut>No round has started yet. "
                               "Round 1 picks items at random from the items to label.</p>")
    groups, keywords, model_name = _map_groups(vm)
    current = cal.get("current_round") or {}
    labeling_now = bool(current) and not (vm.get("canonical") or {}).get("hold")
    cards = []
    for r in reversed(rounds):
        draw = _round_draw(root, r["round_id"])
        chat = ""
        if labeling_now and r["round_id"] == current.get("round_id"):
            chat = ('<p>We label these together in chat. Tell me your label for an item, for example '
                    '<code>#1 none</code>; I record it and this table updates.</p>'
                    '<div class=chatcopy><button class=primary type=button '
                    f'data-copy="{_esc(_chat_prompt(vm, current, draw))}">Copy chat prompt</button>'
                    '<span class=mut>Paste it into a Claude chat in this repo to go on labeling.</span></div>'
                    f'<details class=ctx><summary>the prompt</summary><pre class=prompt>{_esc(_chat_prompt(vm, current, draw))}</pre></details>')
        manifest, card = draw["manifest"], draw["card"]
        drew = manifest.get("draw") if isinstance(manifest.get("draw"), dict) else {}
        pool = manifest.get("development_pool_size")
        probability = next((i["probability"] for i in draw["items"] if i.get("probability")), None)
        state_words = {"judging": "you are labeling", "judged": "all labeled; waiting to be closed",
                       "released": "ready to label"}.get(str(r["state"]), str(r["state"]))
        rows = [
            _row("state", _esc(state_words)),
            _row("started", _esc(", ".join(x for x in (card.get("released_by"), _when(card.get("released_at"))) if x)))
            if card.get("released_by") else "",
            _row("how drawn", _esc(_draw_sentence(drew, pool))) if drew or pool else "",
            _row("each item's chance", _esc(f'{probability * 100:.1f}% (1 in {round(1 / probability)})'))
            if isinstance(probability, (int, float)) and probability else "",
            _row("guideline", _esc(_policy_words(manifest.get("policy_version") or card.get("policy"))))
            if manifest.get("policy_version") or card.get("policy") else "",
        ]
        seen_groups = {int(groups[i["item_id"]]) for i in draw["items"] if groups.get(i["item_id"]) is not None}
        coverage = ""
        if groups and seen_groups:
            total_groups = len({g for g in groups.values() if g is not None})
            coverage = (f'<p class=mut>These items sit in {len(seen_groups)} of {total_groups} map groups '
                        f'({_esc(model_name)}). Groups did not choose them: the draw is random.</p>')
        elif not groups:
            coverage = ('<p class=mut>Build an embedding in Data → Embedding to see where these items sit '
                        'on the map.</p>')
        started_at = _when(card.get("released_at")) if card.get("released_at") else ""
        cards.append(
            f'<details class=roundbox{" open" if chat else ""}><summary><b>{_esc(_round_words(r["round_id"]).capitalize())}</b>'
            f'<span>{_esc(r["finals"])} of {_esc(r["batch_size"])} labeled</span>'
            f'<span class=mut>{_esc(state_words)}{" · started " + _esc(started_at) if started_at else ""}</span></summary>'
            f'{"".join(rows)}'
            f'<h3 class=sub>The items this round drew · {len(draw["items"])}</h3>'
            f'{chat}{_items_table(draw, groups, keywords)}'
            '<p class=mut>Text appears once an item has been shown to you. State shows your first answer, '
            'then your final label; Feedback holds the notes from our chat.</p>'
            f'{coverage}</details>'
        )
    return "".join(cards)


def _md_inline(text: str) -> str:
    text = _esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def _guideline_html(text: str) -> str:
    """Headings, bullet lists, paragraphs, bold and code; the leading # title is the card's own title."""
    out: list[str] = []
    para: list[str] = []
    items: list[str] = []

    def flush() -> None:
        if para:
            out.append(f'<p>{_md_inline(" ".join(para))}</p>')
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{_md_inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    for n, raw in enumerate(text.splitlines()):
        line = raw.rstrip()
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        if heading:
            flush()
            if not (len(heading.group(1)) == 1 and not out):
                out.append(f"<h3>{_md_inline(heading.group(2))}</h3>")
        elif bullet:
            if para:
                flush()
            items.append(bullet.group(1))
        elif not line.strip():
            flush()
        elif items and raw.startswith("  "):
            items[-1] += " " + line.strip()
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "".join(out)


def _labeling_space(vm: dict) -> dict[str, str]:
    root = vm["root"]
    cal = vm["cal"] or {}
    label = _label_definitions(vm)
    labeling_now = cal.get("current_round") and not (vm["canonical"] or {}).get("hold")
    app = "" if labeling_now else '<div id=label-app aria-live=polite><p class=mut>Loading…</p></div>'
    rounds_html = app + (_rounds_view(vm) if cal.get("rounds") else "")
    current = (root / "policy" / "current")
    policy = current.read_text(encoding="utf-8").strip() if current.is_file() else ""
    guideline = root / "policy" / "versions" / policy / "guideline.md" if policy else None
    if guideline and guideline.is_file():
        text = guideline.read_text(encoding="utf-8", errors="replace")[:20000]
        guide = _card(f"Guideline {policy}", f'<div class=guide>{_guideline_html(text)}</div>'
                      f'<p class=mut>From <code>policy/versions/{_esc(policy)}/guideline.md</code>.</p>')
    else:
        guide = _card("Guideline", "<p class=mut>No guideline version is readable yet.</p>")
    return {"discussion": _discussion_view(vm), "label": label, "rounds": rounds_html, "guideline": guide}


def _quality_space(vm: dict) -> dict[str, str]:
    root, sealed = vm["root"], vm["sealed"]
    frame = sealed.get("frame") if isinstance(sealed.get("frame"), dict) else {}
    if sealed:
        test = _card("Held-back test items", "".join([
            _row("items", _esc(sealed.get("n_items"))),
            _row("how drawn", _esc(frame.get("rule"))),
            _row("keeper", _esc(sealed.get("custodian"))),
            _row("state", _esc({"reserved-and-unexposed": "kept aside, never shown"}.get(str(sealed.get("status")), sealed.get("status")))),
            _row("locked for scoring", "yes" if (root / "test" / "final" / "lock.json").is_file() else "not yet"),
        ]) + '<p class=mut>These items are never drawn into a round, shown, or used for the comparison.</p>')
    else:
        test = _later("P0 Contract")
    evaluation = (_card("Evaluation", _row("registry", "present")) if (root / "evaluation" / "registry.yaml").is_file()
                  else _later("P3 Test"))
    audits = sorted((root / "audit").glob("final_*")) if (root / "audit").is_dir() else []
    audit = _card("Audit", _row("audits", _esc(len(audits)))) if audits else _later("P5 Audit")
    return {"test": test, "evaluation": evaluation, "audit": audit}


_RUN_WORDS = {  # the same words as the `in words` column of ref-space-mapping.md's Workflow map
    "corpus-contract": "Set up the job", "discovery-search": "Search outside evidence",
    "guideline-seed": "Draft the guideline", "test-reserve": "Hold back test items",
    "embedding-build": "Build a map", "round-prepare": "Draw a round", "weak-prelabel": "Weak models pre-label",
    "human-calibration": "You label a round", "guideline-learn": "Learn the guideline",
    "round-measure": "Measure a round", "round-close": "Close a round", "handoff-freeze": "Freeze the labels",
    "test-gold-lock": "Lock the test answers", "executor-predict": "A labeling model predicts the test",
    "executor-score": "Score a labeling model", "executor-select": "Pick the labeling model",
    "scan-preflight": "Check before labeling the corpus", "scan-shard": "Label one part of the corpus",
    "risk-route": "Send risky items to you", "human-review": "You review risky items",
    "reconcile": "Combine into final labels", "audit-sample": "Draw an audit sample",
    "audit-human-gold": "You label the audit sample", "audit-analyze": "Analyze the audit",
    "dstar-materialize": "Publish the final labeled corpus",
}


def _space_mapping_ref() -> Path | None:
    """subjective-label/ref/ref-space-mapping.md, found next to the engine the Board already loads."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    path = Path(job_module.__file__).resolve().parents[1] / "ref" / "ref-space-mapping.md"
    return path if path.is_file() else None


def _md_table(text: str, heading: str) -> tuple[list[str], list[list[str]]]:
    """The first `| … |` table under `## heading` in a Markdown file: headers and rows of raw cells."""
    headers: list[str] = []
    rows: list[list[str]] = []
    inside = False
    for line in text.splitlines():
        t = line.strip()
        if t.startswith("## "):
            if inside and headers:
                break
            inside = t[3:].strip() == heading
            continue
        if not inside or not t.startswith("|"):
            if inside and headers and not t.startswith("|"):
                break
            continue
        cells = [c.strip() for c in t.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        if not headers:
            headers = cells
        else:
            rows.append(cells)
    return headers, rows


def _workflow_map(vm: dict) -> str:
    """Run-type rows × Space columns, projected from ref-space-mapping.md, with this job's Run counts."""
    ref = _space_mapping_ref()
    if ref is None:
        return _card("Workflow map", "<p class=mut>ref-space-mapping.md is not reachable from this Board.</p>")
    headers, rows = _md_table(ref.read_text(encoding="utf-8"), "Workflow map")
    if not headers:
        return _card("Workflow map", "<p class=mut>ref-space-mapping.md has no Workflow map table.</p>")
    col = {h.lower(): i for i, h in enumerate(headers)}
    spaces = [h for h in headers if h in {"Data", "Labeling", "Quality", "Delivery"}]
    counts: dict[str, int] = {}
    for r in vm["runs"]:
        counts[str(r["operation"])] = counts.get(str(r["operation"]), 0) + 1
    names = dict(PHASES)
    labels = ["Run type", "Started by", *spaces, "Writes to", "On this job"]
    body, last = [], None
    for cells in rows:
        cell = lambda name: cells[col[name]] if name in col and col[name] < len(cells) else ""  # noqa: E731
        tag = cell("compatibility tag")
        if tag != last:
            group = f"{tag} · {names.get(tag, tag)} · compatibility capability"
            body.append(f'<tr class=phaserow><td colspan={len(labels)}>{_esc(group)}</td></tr>')
            last = tag
        op = cell("run type").strip("`")
        started = cell("started by")
        n = counts.get(op, 0)
        tds = [
            f'<td data-label="{labels[0]}"><b>{_esc(cell("in words"))}</b><div class=mut><code>{_esc(op)}</code></div></td>',
            f'<td data-label="{labels[1]}" class="{"mut" if started == "not built yet" else ""}">{_md_inline(started)}</td>',
            *(f'<td data-label="{sp}"{" class=empty" if cell(sp.lower()) in ("", "—") else ""}>'
              f'{_wf_cell(cell(sp.lower()))}</td>' for sp in spaces),
            f'<td data-label="{labels[-2]}">{_md_inline(cell("writes to"))}</td>',
            f'<td data-label="{labels[-1]}" class=num>{n if n else "<span class=mut>—</span>"}</td>',
        ]
        body.append(f'<tr{" class=live" if n else ""}>{"".join(tds)}</tr>')
    table = ('<div class=scroll><table class=wfmap><thead><tr>'
             + "".join(f"<th>{_esc(h)}</th>" for h in labels)
             + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>")
    return _card("Workflow map", (
        '<ul class="mut notes"><li>One row per Run type, one column per Space. <b>start</b>: a button there starts it; '
        '<b>shows</b>: its result is read there. Every Run is also listed in Runs.</li>'
        '<li>"not built yet" means no program can run it today. "On this job" counts the Runs this job already has.</li>'
        f'<li>A definition, not an inventory. Source: <code>{_esc(_repo_relative(ref))}</code>.</li></ul>' + table))


def _sop_state(op: str, vm: dict, runs_by_op: dict, not_built: set) -> str:
    """Where this job is on one SOP step: done, running, not yet, or not built yet."""
    if op == "gate G0":
        return "done" if (vm.get("canonical") or {}).get("meaning_receipt_valid") else "not yet"
    if op in ("", "—"):
        return "—"
    runs = runs_by_op.get(op) or []
    running = [r for r in runs if r["status"] == "running"]
    if running:
        return "running · " + ", ".join(r["run"].split("_")[0] for r in running)
    done = [r for r in runs if r["status"].startswith("complete")]
    if done:
        return "done · " + ", ".join(r["run"].split("_")[0] for r in done)
    if runs:
        return runs[-1]["status"]
    return "not built yet" if op in not_built else "not yet"


def _sop(vm: dict) -> str:
    """The SOP from ref-space-mapping.md: the steps one labeling job walks, and where this job is."""
    ref = _space_mapping_ref()
    if ref is None:
        return ""
    text = ref.read_text(encoding="utf-8")
    headers, rows = _md_table(text, "SOP")
    if not headers:
        return ""
    col = {h.lower(): i for i, h in enumerate(headers)}
    wf_headers, wf_rows = _md_table(text, "Workflow map")
    wf = {h.lower(): i for i, h in enumerate(wf_headers)}
    not_built = {r[wf["run type"]].strip("`") for r in wf_rows
                 if "run type" in wf and "started by" in wf and r[wf["started by"]] == "not built yet"}
    runs_by_op: dict = {}
    for r in vm.get("runs") or []:
        runs_by_op.setdefault(str(r["operation"]), []).append(r)
    labels = ["#", "Step", "You do", "The chat or engine does", "Where", "Run", "This job"]
    states = []
    for cells in rows:
        cell = lambda name, c=cells: c[col[name]] if name in col and col[name] < len(c) else ""  # noqa: E731
        states.append(_sop_state(cell("run type").strip("`"), vm, runs_by_op, not_built))
    now = next((i for i, st in enumerate(states) if st.startswith("running")), None)
    if now is None:
        now = next((i for i, st in enumerate(states) if st == "not yet"), None)
    body = []
    for i, cells in enumerate(rows):
        cell = lambda name, c=cells: c[col[name]] if name in col and col[name] < len(c) else ""  # noqa: E731
        st = states[i] + (" (now)" if i == now else "")
        cls = "now" if i == now else ("done" if st.startswith("done") else "")
        values = [cell("step"), f"<b>{_md_inline(cell('what happens'))}</b>", _md_inline(cell("you do")),
                  _md_inline(cell("the chat or engine does")), _md_inline(cell("where")),
                  _md_inline(cell("run type")), _esc(st)]
        body.append(f'<tr{f" class={cls}" if cls else ""}>' + "".join(
            f'<td data-label="{_esc(h)}"{" class=num" if h == "#" else ""}>{v}</td>' for h, v in zip(labels, values)) + "</tr>")
    table = ('<div class=scroll><table class="wfmap sop"><thead><tr>'
             + "".join(f"<th>{_esc(h)}</th>" for h in labels)
             + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>")
    return _card("SOP · how a labeling job runs", (
        '<ul class="mut notes"><li>The steps one labeling job walks, in order, and who does each one. '
        'The Workflow map below lists every Run type; this is the path.</li>'
        f'<li>"This job" is read from this job\'s Runs. Source: <code>{_esc(_repo_relative(ref))}</code>.</li></ul>' + table))


def _group_clarity(groups: dict) -> str:
    """How separated the groups really are, in words: a weak split must not read as real categories."""
    scores = groups.get("silhouette_by_k") or {}
    best = scores.get(str(groups.get("k")))
    if not isinstance(best, (int, float)):
        return ""
    if best >= 0.5:
        words, cls = "clear", "ok"
    elif best >= 0.25:
        words, cls = "some separation", "mut"
    else:
        words, cls = "weak. The items do not really fall into separate groups", "warn"
    return (f'<p class="{cls}">How clear are these groups: {_esc(words)} '
            f'<span class=mut>(score {best:.2f}; above 0.5 would be clear, below 0.25 is weak). '
            f'Use them to browse and to check coverage, not as categories.</span></p>')


def _wf_cell(text: str) -> str:
    """'start + shows · Embedding' with the verbs bold; '—' greyed."""
    text = str(text or "").strip()
    if text in {"", "—"}:
        return "<span class=mut>—</span>"
    verbs, _, where = text.partition(" · ")
    verbs_html = " + ".join(f"<b>{_esc(v.strip())}</b>" for v in verbs.split("+"))
    return verbs_html + (f" · {_md_inline(where)}" if where else "")
_STATUS_WORDS = {"complete": "done", "running": "in progress", "failed": "failed"}


def _run_title(run: dict, build_names: dict[str, str]) -> str:
    """'Build a map: MiniLM · reply + context', 'Draw a round: round 1'; the Run id stays under it."""
    op = str(run.get("operation") or "")
    words = _RUN_WORDS.get(op, op)
    m = re.fullmatch(r"rl\d+_" + re.escape(op) + r"_(.+)", str(run.get("run") or ""))
    target = m.group(1) if m else ""
    if op == "embedding-build" and target in build_names:
        return f"{words}: {build_names[target]}"
    if re.fullmatch(r"round-0*\d+", target):
        return f"{words}: {_round_words(target.replace('-', '_'))}"
    return words


def _outcome_words(text) -> str:
    """A Run's recorded outcome with the method's jargon softened for reading; the record is untouched."""
    text = str(text or "")
    if text == "P0 contract landed; human meaning confirmation remains open":
        return "Job set up; the meaning still had to be confirmed then"
    if text == "judging":
        return "you are labeling"
    text = re.sub(r"(\d+) items drawn from (\d+) eligible", r"\1 items picked from \2 to label", text)
    return (text.replace("development items embedded", "items embedded")
            .replace(" sealed left out", " held-back test items left out"))


def _blocked_words(text: str) -> str:
    """The first failed gate, said as what the job waits for."""
    text = str(text or "")
    if text.startswith("G1 Round close"):
        return "the current round to be fully labeled and then closed (closing a round is not built yet)"
    if "meaning confirmation" in text:
        return "you to read the label meanings and confirm them (Data → Contract)"
    return text


def _run_space(vm: dict) -> dict[str, str]:
    runs, state = vm["runs"], vm["state"]
    builds = ((vm.get("embedding") or {}).get("builds")) or []
    build_names = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                                  for b in builds])
    if runs:
        rows = "".join(
            '<tr>'
            f'<td><b>{_esc(_run_title(r, build_names))}</b>'
            f'<div class=mut><code>{_esc(r["run"])}</code></div></td>'
            f'<td class="{"ok" if r["status"] == "complete" else "warn"}">{_esc(_STATUS_WORDS.get(str(r["status"]), str(r["status"])))}</td>'
            f'<td class=mut>{_esc(_outcome_words(r["outcome"]))}</td></tr>'
            for r in runs
        )
        table = ('<div class=scroll><table class=runs><thead><tr><th>What ran</th><th>State</th>'
                 f'<th>Result</th></tr></thead><tbody>{rows}</tbody></table></div>')
    else:
        table = "<p class=mut>No Run ticket yet.</p>"
    canonical = vm["canonical"] or {}
    capability_rows = []
    for pid, name in PHASES:
        if pid == "P0":
            status = "contract valid" if canonical.get("p0_contract_integrity_valid") else "HOLD · contract"
        elif pid == "P1":
            status = "partial · G0 passed" if canonical.get("g0_passed") else "partial · blocked by G0"
        else:
            status = "not implemented · HOLD"
        capability_rows.append(_row(f"{pid} · {name}", _esc(status)))
    phases = _card("Compatibility capabilities · not lifecycle progress", "".join(capability_rows)
                   + _row("waiting for", _esc(_blocked_words(state["first_failed"])))
                   + f'<p class=mut>Code: <code>{_esc(state["first_failed"])}</code></p>')
    return {"runs": _card("Runs", table), "phases": phases, "workflow": _sop(vm) + _workflow_map(vm)}


def _delivery_space(vm: dict) -> dict[str, str]:
    state = vm["state"]
    handoff = (_card("Label handoff", _row("status", _esc(state["handoff_status"] or "present")))
               if state["handoff"].is_file() else _later("P2 Freeze"))
    final = (_card("Final labels", _row("D*", "materialized"))
             if state["dstar"].is_file() else _later("P5 Audit"))
    return {"handoff": handoff, "final": final}


def _script_json(value) -> str:
    return (json.dumps(value, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def render(page_src: Path, path_q: str, file_q: str, page_q: str, board_dir: Path) -> str:
    vm = _view_model(page_src)
    state, canonical, config = vm["state"], vm["canonical"], vm["config"]
    chat_page = studio_chat_page_url(path_q, file_q, page_q, board_dir)
    if not chat_page:
        raise ValueError("Labeling Studio Chat requires the matching generated Page URL")
    hold = bool(state["authority_hold"] or state["next_action"].startswith("HOLD"))
    chat_url = chat_page + "?pane=chat" + ("&labeling_hold=1" if hold else "")
    next_line, next_space = _next_step(vm)
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    title = construct.get("question") or construct.get("name") or page_src.stem

    panels = {
        "data": _data_space(vm), "labeling": _labeling_space(vm),
        "quality": _quality_space(vm), "run": _run_space(vm), "delivery": _delivery_space(vm),
    }
    space_buttons = "".join(
        f'<button class=space type=button role=tab id=tab-{sid} aria-controls=panel-{sid} '
        f'aria-selected=false data-space={sid}>{_esc(name)} Space</button>'
        for sid, name, _ in SPACES
    )
    sections = []
    for sid, name, views in SPACES:
        chips = "".join(
            f'<button class=chip type=button data-space={sid} data-view={vid}>{_esc(vname)}</button>'
            for vid, vname in views
        )
        panes = "".join(
            f'<div class=pane data-space={sid} data-view={vid} hidden>{panels[sid][vid]}</div>'
            for vid, _ in views
        )
        sections.append(
            f'<section class=panel id=panel-{sid} role=tabpanel aria-labelledby=tab-{sid} data-space={sid} hidden>'
            f'<div class=views role=group><span class=vlabel>View</span>{chips}</div>{panes}</section>'
        )

    cal = vm["cal"] or {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    boot = {
        "path": path_q, "file": file_q, "page": page_q,
        "identity": f"{path_q}|{file_q}",
        "human_id": authority.get("human_id") or "",
        "hold": hold,
        "phase": canonical.get("phase") if canonical else None,
        "g0_open": bool(canonical and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation"),
        "default_space": next_space,
        "question": construct.get("question") or construct.get("name") or "",
        "schema": cal.get("schema") or {},
        "rounds": cal.get("rounds") or [],
        "current_round": cal.get("current_round"),
        "batch_default": ((config.get("rounds") or {}).get("round1") or {}).get("human_batch_size") or 20,
        "spaces": {sid: [vid for vid, _ in views] for sid, _, views in SPACES},
    }
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Labeling · {_esc(page_src.stem)}</title><style>{_CSS}</style></head><body>'
        '<header>'
        f'<h1>🏷 {_esc(title)}</h1>'
        f'<div class=planmeta><a class=back href="/_board/labeling-board?path={_esc(quote(path_q))}">← All labeling jobs</a>'
        f'<span class=sep>·</span><span>{_esc(page_src.stem)}</span>'
        f'<span class=sep>·</span><a href="{_esc(chat_url)}" target=_blank rel=noopener>Open Studio Chat</a></div>'
        f'<p class="lead next{" hold" if hold and not _imported_reference_only(vm) else ""}"><b>Next:</b> {_esc(next_line)}</p>'
        '</header>'
        f'<nav class=spaces role=tablist aria-label="Labeling Spaces">{space_buttons}</nav>'
        + "".join(sections) +
        f'<script type=application/json id=labeling-boot>{_script_json(boot)}</script>'
        f'<script>{_JS}</script></body></html>'
    )


_CSS = """
:root{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44;--acc:#3e5c84;--soft:#f6f7f9}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;
 --mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87;
 --acc:#7d9cc4;--soft:#1b1d21}}
/* the hidden attribute always wins over a display rule below (SVG and canvas both lost to it once) */
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
h1{font-size:17px;margin:0 0 2px;overflow-wrap:anywhere} .mut{color:var(--mut);font-size:13px}
a{color:var(--acc)}
.planmeta{margin:2px 0 7px;color:var(--mut);font-size:12.5px;line-height:1.45}
.planmeta a{text-decoration:none}.planmeta a:hover{text-decoration:underline}
.sep{opacity:.45;padding:0 4px}
.lead{font-size:14.5px;margin:6px 0 0;color:var(--fg)}
.next.hold{color:var(--warn)}
.spaces{display:flex;gap:5px;margin:10px 0 6px;flex-wrap:wrap}
.space{font:600 11.5px -apple-system,sans-serif;border:1px solid var(--line);
 border-radius:8px;padding:3px 9px;cursor:pointer;background:var(--card);
 color:var(--fg);white-space:nowrap;flex:0 0 auto}
.space.on{border-color:var(--acc);color:var(--acc)}
.views{display:flex;align-items:center;gap:5px;margin:2px 0 12px;flex-wrap:wrap}
.vlabel{font:600 10px/1.5 system-ui,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.05em;margin-right:2px}
.chip{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 9px;cursor:pointer;
 background:var(--card);color:var(--mut)}
.chip.on{border-color:var(--acc);color:var(--acc)}
.ok{color:var(--ok);font-weight:600} .warn{color:var(--warn);font-weight:600}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:10px 14px;margin:0 0 10px}
.card.focus{border-color:var(--acc)}
.card h2{font-size:15px;margin:0 0 4px;display:flex;gap:8px;align-items:baseline}
.card h2 .tally{margin-left:auto;flex:none;font:600 11px ui-monospace,Menlo,monospace;color:var(--mut)}
.tally{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:10px 0 6px;font-size:12px}
details{margin:4px 0 0}
summary{cursor:pointer;font:600 12px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.03em;padding:3px 0;list-style:none}
summary::-webkit-details-marker{display:none}
summary:before{content:"▸ ";color:var(--mut)}
details[open]>summary:before{content:"▾ "}
summary:hover{color:var(--acc)}
.rec{padding:8px 0 6px;border-top:1px solid var(--line)}
.rec:first-of-type{border-top:0;padding-top:2px}
.rh{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.rid{flex:none;font:600 11px ui-monospace,Menlo,monospace;color:var(--acc);
 border:1px solid var(--line);border-radius:6px;padding:0 6px;white-space:nowrap}
.rt{flex:1;min-width:12em;font-size:14.5px;font-weight:600;line-height:1.4}
.pill{flex:none;font:600 10.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.04em;border-radius:999px;padding:1px 8px;border:1px solid currentColor;
 max-width:16em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pill.ok{color:var(--ok)} .pill.warn{color:var(--warn)}
.pill.mut{color:var(--mut)} .pill.acc{color:var(--acc)}
/* label/value rows read as table cells, the same shape as the Paper plugin's .kv table:
   a run of .rr siblings becomes one bordered table, the label column shaded */
.rrows{margin-top:6px}
.rr{display:grid;grid-template-columns:11em minmax(0,1fr);gap:0;font-size:14px;line-height:1.55;
 border:1px solid var(--line);border-top:0;background:var(--card)}
.rr>b{background:var(--soft);border-right:1px solid var(--line);padding:8px 12px;
 font:700 11px/1.45 -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.03em}
.rr>span{padding:7px 12px;min-width:0;overflow-wrap:anywhere}
:not(.rr)+.rr,.rr:first-child{border-top:1px solid var(--line);border-radius:9px 9px 0 0;margin-top:8px}
.rr:last-child,.rr:has(+ :not(.rr)){border-bottom-left-radius:9px;border-bottom-right-radius:9px;margin-bottom:8px}
.rgrp{margin:12px 0 4px;font:600 12px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.05em}
code{font:12px ui-monospace,Menlo,monospace}
.meanings{margin:6px 0 4px;padding-left:18px;font-size:14px}.meanings li{margin:2px 0}
.guide{font-size:14px;line-height:1.55}
.guide h3{font-size:14.5px;margin:14px 0 4px}.guide h3:first-child{margin-top:2px}
.guide p{margin:4px 0 8px}.guide ul{margin:2px 0 8px;padding-left:20px}.guide li{margin:2px 0}
.attest{display:block;margin:8px 0;font-size:14px}
.actions{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:8px}
button.primary,button.ghost{border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--fg);
 padding:4px 9px;cursor:pointer;font:600 12px system-ui,sans-serif}
button.primary{border-color:var(--acc);color:var(--acc)}
button.primary:disabled{opacity:.45;cursor:not-allowed}
.msg{font-size:12.5px;color:var(--mut)}.msg.err{color:var(--warn)}
.scroll{overflow-x:auto}
table{border-collapse:separate;border-spacing:0;width:100%;font-size:14px;line-height:1.5;
 border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:6px 0 8px;background:var(--card)}
th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}
th{background:var(--soft);font:700 11px/1.45 -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.03em}
th:last-child,td:last-child{border-right:0}
tbody tr:last-child td,tr.grp:has(+ tr.exrow[hidden]:last-child) td{border-bottom:0}
td.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.grptable tr.grp{cursor:pointer}
.grptable tr.grp:hover td,.grptable tr.grp.on td{background:color-mix(in srgb,var(--acc) 7%,var(--card))}
.grptable .exbox{margin:6px 0 0}
details.roundbox{border:1px solid var(--line);border-radius:12px;background:var(--card);margin:0 0 10px;padding:8px 14px}
details.roundbox>summary{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;cursor:pointer;
 font:14.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;text-transform:none;letter-spacing:0;color:var(--fg)}
details.roundbox>summary .mut{font-size:13px}
details.roundbox[open]>summary{margin-bottom:6px}
h3.sub{font-size:13px;margin:12px 0 2px}
table.items{width:auto;max-width:100%}
table.items td,table.items th{padding:3px 10px}
table.items td:not(:nth-child(3)):not(:nth-child(6)){white-space:nowrap}
table.items td.num{text-align:left}
table.items td:nth-child(3)>*{max-width:30em}
table.items td:nth-child(6)>*{max-width:18em}
table.items .pill{font-size:10px}
table.items td.nowrap{white-space:nowrap}
table.items .reply{font-weight:500}
table.items details.ctx summary{font-size:11.5px;text-transform:none;letter-spacing:0;margin-top:3px}
table.items .fb{margin:0 0 3px}
table.wfmap{font-size:13.5px}
table.wfmap tr.phaserow td{background:var(--soft);font:700 11.5px/1.4 -apple-system,sans-serif;color:var(--fg);
 text-transform:uppercase;letter-spacing:.03em}
table.wfmap tr.live td:first-child{box-shadow:inset 3px 0 0 var(--ok)}
table.wfmap td code{font-size:11.5px}
.grptable tr.exrow td{background:var(--bg)}
.steps{display:flex;gap:5px;flex-wrap:wrap;margin:2px 0 8px}
.stepline{font-size:14.5px;margin:2px 0 8px}
.step{font:600 11.5px -apple-system,sans-serif;border:1px solid var(--line);border-radius:7px;padding:3px 9px;color:var(--mut);background:var(--card)}
.step.on{border-color:var(--acc);color:var(--acc)}.step.past{color:var(--ok)}
.discstatus{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:2px 0 7px}
.discquestion{font-size:20px;line-height:1.3;margin:9px 0 5px;max-width:42em}
.flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin:8px 0 4px}
.flowstep{display:flex;flex-direction:column;gap:2px;border:1px solid var(--line);border-radius:8px;padding:8px 9px;background:var(--card);min-height:86px}
.flowstep b{font:700 11px ui-monospace,Menlo,monospace;color:var(--mut)}
.flowstep strong{font-size:13px;line-height:1.3}.flowstep span{font-size:12px;line-height:1.35;color:var(--mut)}
.flowstep.now{border-color:var(--acc);background:color-mix(in srgb,var(--acc) 7%,var(--card))}
.flowstep.now b,.flowstep.now strong{color:var(--acc)}
.casegrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:8px}
.casecard{border:1px solid var(--line);border-radius:8px;padding:9px 10px;background:var(--soft)}
.caseid{font:600 10px ui-monospace,Menlo,monospace;color:var(--acc);text-transform:uppercase;letter-spacing:.05em}
.casecard h3{font-size:14px;margin:2px 0 3px}.casecard p{font-size:13px;line-height:1.4;margin:3px 0}
.runplans{border-top:1px solid var(--line);margin-top:7px}
.runplan{display:grid;grid-template-columns:16em minmax(0,1fr) max-content;gap:8px;align-items:baseline;padding:8px 0;border-bottom:1px solid var(--line);font-size:13px}
.runplan code{color:var(--acc)}.runplan span{color:var(--fg)}.runplan em{font-style:normal;color:var(--mut);font-size:12px;white-space:nowrap}
/* conversation turns, option rows, chips */
table.sop tr.now td{background:var(--soft)} table.sop tr.now td:last-child{color:var(--acc);font-weight:600}
table.sop tr.done td:last-child{color:var(--ok)}
.chatcopy{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0 6px}
.cc{font:600 12px -apple-system,sans-serif;border:1px solid var(--line);border-radius:6px;background:var(--card);
 color:var(--acc);padding:1px 7px;cursor:pointer;white-space:nowrap;vertical-align:middle}
.cc:hover{border-color:var(--acc)}
h3 .cc{margin-left:6px}
table.defs{width:auto;max-width:100%}
table.defs td:nth-child(2){min-width:16em;max-width:44em}
#cc-toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--fg);color:var(--bg);
 font:600 12.5px -apple-system,sans-serif;padding:7px 14px;border-radius:8px;opacity:0;transition:opacity .15s;pointer-events:none;z-index:60;max-width:80vw}
#cc-toast.on{opacity:.95} #cc-toast.bad{background:var(--warn)}
pre.prompt{white-space:pre-wrap;overflow-wrap:anywhere;font:12.5px/1.5 ui-monospace,Menlo,monospace;background:var(--soft);
 border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:4px 0 10px}
.convo{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 14px;margin:0 0 10px;
 max-height:46vh;overflow:auto}
.turn{display:grid;grid-template-columns:5.4em 1fr;gap:6px;font-size:14px;line-height:1.55;padding:1px 0;overflow-wrap:anywhere}
.turn b{font:600 11px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.04em;padding-top:3px}
.line{display:flex;gap:5px;flex-wrap:wrap;align-items:center;margin:0 0 8px}
.line .lbl{font:600 10px/1.5 system-ui,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.05em;min-width:7em}
.pill.tog{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;text-transform:none;letter-spacing:0;
 border:1px solid var(--line);border-radius:7px;padding:3px 9px;cursor:pointer;background:var(--card);color:var(--mut);max-width:none}
.pill.tog.on{border-color:var(--acc);color:var(--acc)}
/* embedding view */
.pieces{display:flex;flex-wrap:wrap;gap:3px}
code.wp{border:1px solid var(--line);border-radius:5px;padding:0 4px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:4px;vertical-align:0}
.dot.faint{background:var(--mut);opacity:.3}
.rid .dot{width:8px;height:8px}
svg.map{display:block;width:100%;height:auto;margin:4px auto 6px;max-width:calc(72vh * 1000 / 600);border:1px solid var(--line);border-radius:8px;background:var(--bg)}
svg.map .pt{fill:var(--gc);fill-opacity:.85;stroke:var(--card);stroke-width:1.5}
svg.map .pt.drawn{stroke:var(--fg);stroke-width:2.5}
svg.map .pt:hover{stroke:var(--acc);stroke-width:3}
.mapwrap[data-color=label] svg.map .pt{fill:var(--mut);fill-opacity:.3}
.mapwrap[data-color=label] svg.map .pt.done{fill:var(--lc);fill-opacity:.95}
.embpane{margin-top:0}
svg.map{cursor:grab}
svg.map.dragging{cursor:grabbing}
svg.map .pt{cursor:pointer;transition:opacity .15s}
svg.map .pt.dim{opacity:.12}
svg.map .pt.sel{stroke:var(--acc);stroke-width:4}
svg.map .pt.nb{stroke:var(--acc);stroke-width:2.5}
svg.map .links line{stroke:var(--acc);stroke-opacity:.55;stroke-width:1.5}
.mapwrap[data-show=round] svg.map .pt:not(.drawn){opacity:.12}
.zoomctl{margin-left:auto;display:inline-flex;gap:5px;flex-wrap:wrap}
canvas.map3d{display:block;width:100%;margin:4px auto 6px;max-width:calc(72vh * 1000 / 600);border:1px solid var(--line);border-radius:8px;
 background:var(--bg);cursor:grab;touch-action:none}
canvas.map3d.dragging{cursor:grabbing}
.embform{margin:6px 0 2px}
.embform select{font:14px -apple-system,sans-serif;padding:3px 6px;border:1px solid var(--line);border-radius:7px;
 background:var(--card);color:var(--fg);max-width:100%}
.embform input.num{flex:0 0 7em;min-width:0}
.embform .modelinfo{margin:0 0 8px}
button.leg{font:inherit;color:inherit;background:none;border:1px solid transparent;border-radius:6px;padding:0 5px;cursor:pointer}
button.leg.on{border-color:var(--acc);color:var(--acc)}
.pick{border:1px solid var(--acc);border-radius:8px;padding:8px 12px;margin:8px 0 4px}
.pill.tog[data-emb-show]{white-space:normal;max-width:100%;flex:0 1 auto;text-align:left}
.runbox{border:1px solid var(--line);border-radius:8px;padding:6px 12px 8px;margin:8px 0 10px}
.runbox h3{font-size:14px;margin:4px 0 6px}
.embform select{margin-right:8px}
.embmore summary{font-size:12.5px;color:var(--mut);cursor:pointer;margin:2px 0 4px}
.embmore[open] summary{margin-bottom:6px}
.exbox{margin:4px 0 2px;cursor:auto}
details.fold{border:1px solid var(--line);border-radius:12px;background:var(--card);margin:0 0 12px;padding:10px 14px}
details.fold>summary{font:600 14px -apple-system,sans-serif;cursor:pointer}
details.fold[open]>summary{margin-bottom:8px}
details.fold .card{border:0;padding:0;margin:8px 0 0;background:none}
ul.notes{margin:6px 0 0;padding-left:18px;font-size:13px}ul.notes li{margin:2px 0}
button.leg .kw{opacity:.75}
.runtable td .mut code{font-size:11px}
.exs{margin-top:6px}
.ex{border-left:3px solid var(--line);padding:4px 0 4px 10px;margin:0 0 10px}
.exh{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:3px}
.ex .exctx .turn span{color:var(--mut)}
.ex [data-earlier]{margin:0 0 4px;font-size:12px}
.ex .exreply span{font-weight:500}
.ex mark{background:color-mix(in srgb,var(--acc) 22%,transparent);color:inherit;border-radius:3px;padding:0 1px}
.pktext{margin:6px 0 2px}
.pick .nbs{display:flex;flex-wrap:wrap;gap:5px;margin:4px 0}
.pick .rh button{margin-left:auto}
.rec .rh button{flex:none}
.legend{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:12.5px;color:var(--mut)}
.mapwrap[data-color=group] .legend.label,.mapwrap[data-color=label] .legend.group{display:none}
@media(max-width:560px){body{padding:12px}.rr,.turn{grid-template-columns:1fr;gap:0}
 .discquestion{font-size:18px}.flow,.casegrid{grid-template-columns:1fr}.flowstep{min-height:0}
 .runplan{grid-template-columns:1fr;gap:2px}.runplan em{white-space:normal}
 table.runs thead,table.runtable thead{display:none}
 table.runs tr,table.runtable tr{display:block;border-bottom:1px solid var(--line)}
 table.runs tbody tr:last-child,table.runtable tbody tr:last-child{border-bottom:0}
 table.runs td,table.runtable td{display:block;border:0;padding:4px 10px}
 table.wfmap thead{display:none}
 table.wfmap tr{display:block;border-bottom:1px solid var(--line)}
 table.wfmap td{display:block;border:0;padding:3px 10px}
 table.wfmap td[data-label]:not(:first-child)::before{content:attr(data-label) ": ";color:var(--mut);font-size:12px}
 table.wfmap td.num{text-align:left}
 table.wfmap td.empty{display:none}
 table.grptable thead{display:none}
 table.grptable tr{display:block;border-bottom:1px solid var(--line)}
 table.grptable tbody tr:last-child{border-bottom:0}
 table.grptable td{display:block;border:0;padding:4px 10px}
 table.grptable td.num{display:inline-block;padding-top:0}
 table.grptable td.num::before{content:attr(data-label) " ";color:var(--mut);font-size:12px}
 .planmeta{display:flex;flex-wrap:wrap;align-items:baseline}.planmeta a,.planmeta span{white-space:nowrap}
 .rr>b{border-right:0;border-bottom:1px solid var(--line);padding:5px 10px}.rr>span{padding:6px 10px}
 svg.map .pt{r:13px}}
"""


_JS = r"""
(function(){'use strict';
var boot=JSON.parse(document.getElementById('labeling-boot').textContent);
var spaces=boot.spaces, key='labeling-view:'+boot.identity;
function $(s,r){return (r||document).querySelector(s);} function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));}
function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
/* ── Space and view selection ─────────────────────────────── */
function select(space,view,remember){
 if(!spaces[space]){space=boot.default_space;}
 if(spaces[space].indexOf(view)<0){view=spaces[space][0];}
 $$('.space').forEach(function(b){var on=b.dataset.space===space;b.classList.toggle('on',on);b.setAttribute('aria-selected',on?'true':'false');b.tabIndex=on?0:-1;});
 $$('.panel').forEach(function(p){p.hidden=p.dataset.space!==space;});
 $$('.chip').forEach(function(c){if(c.dataset.space===space){c.classList.toggle('on',c.dataset.view===view);}});
 $$('.pane').forEach(function(p){p.hidden=!(p.dataset.space===space&&p.dataset.view===view);});
 if(remember){try{localStorage.setItem(key,JSON.stringify({space:space,view:view}));}catch(e){}
  try{var u=new URL(location.href);u.searchParams.set('space',space);u.searchParams.set('view',view);history.replaceState(null,'',u.toString());}catch(e){}}
 current={space:space,view:view};
}
var current={};
$$('.space').forEach(function(b){b.addEventListener('click',function(){select(b.dataset.space,null,true);});
 b.addEventListener('keydown',function(e){var ids=Object.keys(spaces),i=ids.indexOf(b.dataset.space);
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();var n=ids[(i+(e.key==='ArrowRight'?1:ids.length-1))%ids.length];select(n,null,true);$('#tab-'+n).focus();}});});
$$('.chip').forEach(function(c){c.addEventListener('click',function(){select(c.dataset.space,c.dataset.view,true);});});
$$('[data-map-color]').forEach(function(b){b.addEventListener('click',function(){var w=b.closest('.mapwrap');
 w.dataset.color=b.dataset.mapColor;$$('[data-map-color]',w).forEach(function(x){x.classList.toggle('on',x===b);});});});
/* ── embedding map: pick a dot, light a group, zoom and pan ── */
$$('.embpane').forEach(function(pane){
 var dataEl=$('.embdata',pane),svg=$('svg.map',pane);if(!dataEl||!svg){return;}
 var data=JSON.parse(dataEl.textContent),wrap=$('.mapwrap',pane),zoom=$('g.zoom',svg),links=$('g.links',svg),pick=$('[data-pick]',pane);
 var vb=svg.viewBox.baseVal,view={x:0,y:0,k:1},dots=$$('circle.pt',svg),focusGroup=null;
 function byId(id){return $('circle.pt[data-item="'+id+'"]',svg);}
 function apply(){zoom.setAttribute('transform','translate('+view.x+' '+view.y+') scale('+view.k+')');
  var r=7/Math.sqrt(view.k);dots.forEach(function(c){c.setAttribute('r',r.toFixed(2));});}
 function toSvg(cx,cy){var b=svg.getBoundingClientRect();return {x:(cx-b.left)*vb.width/b.width,y:(cy-b.top)*vb.height/b.height};}
 function zoomAt(px,py,factor){var k=Math.min(16,Math.max(1,view.k*factor));
  view.x=px-(px-view.x)*(k/view.k);view.y=py-(py-view.y)*(k/view.k);view.k=k;if(k===1){view.x=0;view.y=0;}apply();}
 $$('[data-zoom]',pane).forEach(function(b){b.addEventListener('click',function(){if(svg.hasAttribute('hidden')){return;}
  if(b.dataset.zoom==='reset'){view={x:0,y:0,k:1};apply();return;}zoomAt(vb.width/2,vb.height/2,b.dataset.zoom==='in'?1.5:1/1.5);});});
 svg.addEventListener('wheel',function(e){if(!e.ctrlKey){return;}e.preventDefault();var q=toSvg(e.clientX,e.clientY);zoomAt(q.x,q.y,e.deltaY<0?1.15:1/1.15);},{passive:false});
 var drag=null;
 svg.addEventListener('pointerdown',function(e){drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y,moved:false,touch:e.pointerType==='touch'};});
 svg.addEventListener('pointermove',function(e){if(!drag){return;}var dx=e.clientX-drag.x,dy=e.clientY-drag.y;
  if(!drag.moved&&Math.abs(dx)+Math.abs(dy)<5){return;}drag.moved=true;if(drag.touch){return;}svg.classList.add('dragging');
  var b=svg.getBoundingClientRect();view.x=drag.vx+dx*vb.width/b.width;view.y=drag.vy+dy*vb.height/b.height;apply();});
 function endDrag(e){if(!drag){return;}var moved=drag.moved;drag=null;svg.classList.remove('dragging');
  if(!moved&&e&&e.target&&e.target.classList&&e.target.classList.contains('pt')){choose(e.target.dataset.item);}}
 svg.addEventListener('pointerup',endDrag);svg.addEventListener('pointerleave',function(){drag=null;svg.classList.remove('dragging');});
 svg.addEventListener('pointercancel',function(){drag=null;svg.classList.remove('dragging');});
 function lightGroup(g){focusGroup=(focusGroup===g)?null:g;
  dots.forEach(function(c){c.classList.toggle('dim',focusGroup!==null&&c.dataset.group!==focusGroup);});
  $$('[data-group-pick]',pane).forEach(function(el){el.classList.toggle('on',el.dataset.groupPick===focusGroup);});
  if(pane.__setPick){pane.__setPick(pickStateOf());}
  if(focusGroup!==null){(svg.hasAttribute('hidden')?$('canvas.map3d',pane):svg).scrollIntoView({block:'nearest',behavior:'smooth'});}}
 function pickStateOf(){var s=$('circle.pt.sel',svg);if(!s){return null;}
  return {id:s.dataset.item,nbs:$$('circle.pt.nb',svg).map(function(c){return c.dataset.item;})};}
 $$('[data-group-pick]',pane).forEach(function(el){el.addEventListener('click',function(e){
   if(e.target.closest&&e.target.closest('[data-no-light]')){return;}lightGroup(el.dataset.groupPick);});
  el.addEventListener('keydown',function(e){if(e.target!==el){return;}
   if(e.key==='Enter'||e.key===' '){e.preventDefault();lightGroup(el.dataset.groupPick);}});});
 /* item text: typical items per group, or one picked dot; items waiting in a round never show here */
 var SPEAKER=/^\s*([A-Z][A-Z_ ]{1,20}):\s*/;
 function marked(text,words){var t=String(text||'');if(!words||!words.length){return esc(t);}
  var re=new RegExp('\\b('+words.join('|')+')\\b','gi'),out='',last=0,m;
  while((m=re.exec(t))){out+=esc(t.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length;}
  return out+esc(t.slice(last));}
 function clip(t,n){t=String(t||'').trim();return t.length>n?t.slice(0,n).replace(/\s+\S*$/,'')+' …':t;}
 function itemTextHtml(r,words){
  var turns=String(r.context||'').split('\n').filter(function(l){return l.trim();}),earlier=Math.max(0,turns.length-2);
  function turn(l){var m=l.match(SPEAKER),name=m?who(m[1]):'',body=m?l.slice(m[0].length):l;
   return '<div class=turn><b>'+esc(name)+'</b><span>'+marked(clip(body,260),words)+'</span></div>';}
  var ctx=(earlier?'<button class="pill tog" type=button data-earlier>Show '+earlier+' earlier turn'+(earlier>1?'s':'')+'</button>'+
    '<div class=earlier hidden>'+turns.slice(0,earlier).map(turn).join('')+'</div>':'')+turns.slice(earlier).map(turn).join('');
  return (ctx?'<div class=exctx>'+ctx+'</div>':'')+
   '<div class="turn exreply"><b>AI reply</b><span>'+marked(clip(r.text,600),words)+'</span></div>';}
 function exItem(e,words){var mk=data.marks[e.item_id];
  return '<div class=ex><div class=exh><button class="pill tog" type=button data-ex-item="'+esc(e.item_id)+'" title="Show this item on the map">item '+esc(e.item_id)+' · see on map</button>'+
   '<span class=mut>similarity to the group centre '+e.closeness.toFixed(2)+'</span>'+(mk&&mk.final?'<span class=pill>your label: '+esc(mk.final)+'</span>':'')+
   '</div>'+itemTextHtml(e,words)+'</div>';}
 function wireItems(root){$$('[data-ex-item]',root).forEach(function(b){if(b.__wired){return;}b.__wired=true;
  b.addEventListener('click',function(){choose(b.dataset.exItem);
   (svg.hasAttribute('hidden')?$('canvas.map3d',pane):svg).scrollIntoView({block:'center',behavior:'smooth'});});});}
 pane.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-earlier]');if(!b){return;}
  var box=b.nextElementSibling,open=box.hidden;box.hidden=!open;
  b.textContent=(open?'Hide ':'Show ')+box.children.length+' earlier turn'+(box.children.length>1?'s':'');});
 $$('[data-ex-group]',pane).forEach(function(btn){
  var g=btn.dataset.exGroup,list=$('[data-ex-list="'+g+'"]',pane),box=list.closest('tr')||list,offset=0,words=(data.groups[g]||{}).keywords||[];
  function more(){var b=$('[data-ex-more]',list);if(b){b.disabled=true;b.textContent='Loading…';}
   act('group_examples',{version:data.version,group_index:Number(g),k:3,offset:offset}).then(function(j){var r=j.result;
    if(b){b.remove();}
    if(offset===0&&r.hidden_waiting){list.insertAdjacentHTML('beforeend','<p class=mut>'+r.hidden_waiting+' item'+(r.hidden_waiting>1?'s':'')+
     ' of this group wait'+(r.hidden_waiting>1?'':'s')+' in '+esc(r.hidden_rounds.map(roundWords).join(', '))+' and '+(r.hidden_waiting>1?'are':'is')+
     ' not shown, so you first read them in Labeling → Rounds.</p>');}
    if(offset===0&&!r.examples.length){list.insertAdjacentHTML('beforeend','<p class=mut>No item of this group can be shown yet.</p>');}
    list.insertAdjacentHTML('beforeend',r.examples.map(function(e){return exItem(e,words);}).join(''));
    offset+=r.examples.length;
    if(r.more){list.insertAdjacentHTML('beforeend','<button class="pill tog" type=button data-ex-more>Show 3 more</button>');
     $('[data-ex-more]',list).addEventListener('click',more);}
    wireItems(list);})
   .catch(function(e){if(b){b.disabled=false;b.textContent='Show 3 more';}
    list.insertAdjacentHTML('beforeend','<p class=warn>'+esc(e.message)+'</p>');});}
  btn.addEventListener('click',function(){
   if(!box.hidden){box.hidden=true;btn.textContent='Show typical items';btn.classList.remove('on');return;}
   box.hidden=false;btn.textContent='Hide typical items';btn.classList.add('on');if(!offset&&!list.children.length){more();}});});
 function markText(id){var mk=data.marks[id];if(!mk){return 'not picked for labeling';}
  return roundWords(mk.round)+(mk.final?' · your label: '+mk.final:' · not labeled yet');}
 function groupTag(g){var info=data.groups[String(g)];if(!info){return '';}
  return '<span class="pill mut"><i class=dot style="background:'+info.color+'"></i>'+esc(info.name)+'</span>';}
 function clearPick(){$$('circle.pt.sel,circle.pt.nb',svg).forEach(function(c){c.classList.remove('sel','nb');});links.innerHTML='';
  if(pane.__setPick){pane.__setPick(null);}}
 function choose(id){
  clearPick();var c=byId(id);if(!c){return;}c.classList.add('sel');
  pick.hidden=false;pick.innerHTML='<p class=mut>Finding the nearest items…</p>';
  act('embedding_item',{version:data.version,item_id:id,k:6}).then(function(j){
   var r=j.result,info=data.groups[String(r.group)]||{},lines='';
   r.neighbors.forEach(function(n){var d=byId(n.item_id);if(!d){return;}d.classList.add('nb');
    lines+='<line x1="'+c.getAttribute('cx')+'" y1="'+c.getAttribute('cy')+'" x2="'+d.getAttribute('cx')+'" y2="'+d.getAttribute('cy')+'"/>';});
   links.innerHTML=lines;c.parentNode.appendChild(c);
   if(pane.__setPick){pane.__setPick({id:r.item_id,nbs:r.neighbors.map(function(n){return n.item_id;})});}
   pick.innerHTML='<div class=rh><span class=rid>item '+esc(r.item_id)+'</span><span class=mut>in group</span>'+groupTag(r.group)+'<span class=mut>'+esc((info.keywords||[]).slice(0,3).join(' · '))+'</span>'+
    '<button class=ghost type=button data-pick-close aria-label="Close">×</button></div>'+
    '<div class=rrows><div class=rr><b>round</b><span>'+esc(markText(r.item_id))+'</span></div>'+
    '<div class=rr><b>most similar 6</b><span class=nbs>'+r.neighbors.map(function(n){
      return '<button class="pill tog" type=button data-pick-item="'+esc(n.item_id)+'" title="'+esc(markText(n.item_id))+'">'+
       '<i class=dot style="background:'+((data.groups[String(n.group)]||{}).color||'var(--mut)')+'"></i>item '+esc(n.item_id)+' · '+n.similarity.toFixed(2)+
       (data.marks[n.item_id]&&data.marks[n.item_id].final?' · '+esc(data.marks[n.item_id].final):'')+'</button>';}).join('')+'</span></div></div>'+
    '<div class=pktext data-pick-text>'+(data.marks[r.item_id]&&!data.marks[r.item_id].final
      ?'<p class=mut>This item waits in '+esc(roundWords(data.marks[r.item_id].round))+'; its text appears in Labeling → Rounds.</p>'
      :'<button class="pill tog" type=button data-pick-show>Show its text</button>')+'</div>'+
    '<p class=mut>The number is similarity, from 0 (unrelated) to 1 (the same). Similar means similar words and topic, not the same label. The flat map can still draw similar items far apart. In item text, grey marks are the group\'s keywords.</p>';
   $('[data-pick-close]',pick).addEventListener('click',function(){clearPick();pick.hidden=true;});
   var show=$('[data-pick-show]',pick);if(show){show.addEventListener('click',function(){show.disabled=true;show.textContent='Loading…';
    act('embedding_item_text',{version:data.version,item_id:r.item_id}).then(function(t){
     $('[data-pick-text]',pick).innerHTML='<div class=ex>'+itemTextHtml(t.result,info.keywords||[])+'</div>';})
    .catch(function(e){$('[data-pick-text]',pick).innerHTML='<p class=warn>'+esc(e.message)+'</p>';});});}
   $$('[data-pick-item]',pick).forEach(function(b){b.addEventListener('click',function(){choose(b.dataset.pickItem);});});
  }).catch(function(e){pick.innerHTML='<p class=warn>'+esc(e.message)+'</p>';});
 }
 $$('[data-map-show]',pane).forEach(function(b){b.addEventListener('click',function(){wrap.dataset.show=b.dataset.mapShow;
  $$('[data-map-show]',pane).forEach(function(x){x.classList.toggle('on',x===b);});draw3d();});});
 /* 3D: the same items, turned and zoomed on a canvas */
 var canvas=$('canvas.map3d',pane),pts=data.points3d||[],cam={yaw:0.6,pitch:0.35,zoom:1},spin=false,raf=null,pickState=null,drag3=null;
 function cssColor(v){if(!v||v.indexOf('var(')!==0){return v||'#888';}
  return getComputedStyle(document.documentElement).getPropertyValue(v.slice(4,-1)).trim()||'#888';}
 function is3d(){return canvas&&!canvas.hidden;}
 function sizeCanvas(){if(!canvas){return;}var w=canvas.clientWidth||600,dpr=window.devicePixelRatio||1;
  canvas.width=Math.round(w*dpr);canvas.height=Math.round(w*0.6*dpr);canvas.style.height=Math.round(w*0.6)+'px';}
 function project(x,y,z){var cy=Math.cos(cam.yaw),sy=Math.sin(cam.yaw),cp=Math.cos(cam.pitch),sp=Math.sin(cam.pitch);
  var x1=x*cy-z*sy,z1=x*sy+z*cy,y1=y*cp-z1*sp,z2=y*sp+z1*cp,f=3.2/(3.2-z2*0.9),
   s=Math.min(canvas.width,canvas.height)*0.36*cam.zoom;
  return {x:canvas.width/2+x1*f*s,y:canvas.height/2-y1*f*s,z:z2,f:f};}
 function draw3d(){
  if(!is3d()){return;}var ctx=canvas.getContext('2d'),dpr=window.devicePixelRatio||1,W=canvas.width,H=canvas.height;
  ctx.clearRect(0,0,W,H);
  var line=cssColor('var(--line)'),fg=cssColor('var(--fg)'),acc=cssColor('var(--acc)');
  ctx.strokeStyle=line;ctx.lineWidth=1.2*dpr;ctx.beginPath();
  [[1,0,0],[0,1,0],[0,0,1]].forEach(function(a){var p1=project(-a[0],-a[1],-a[2]),p2=project(a[0],a[1],a[2]);
   ctx.moveTo(p1.x,p1.y);ctx.lineTo(p2.x,p2.y);});ctx.stroke();
  var byColor=wrap.dataset.color==='label',roundOnly=wrap.dataset.show==='round';
  var drawn=pts.map(function(p){var q=project(p[1],p[2],p[3]);q.id=p[0];q.group=p[4];return q;});
  drawn.sort(function(a,b){return a.z-b.z;});
  var nbs=pickState?pickState.nbs:[],selQ=null;
  if(pickState){var sq=drawn.filter(function(q){return q.id===pickState.id;})[0];
   if(sq){ctx.strokeStyle=acc;ctx.globalAlpha=0.6;ctx.lineWidth=1.5*dpr;
    drawn.forEach(function(q){if(nbs.indexOf(q.id)>=0){ctx.beginPath();ctx.moveTo(sq.x,sq.y);ctx.lineTo(q.x,q.y);ctx.stroke();}});ctx.globalAlpha=1;}}
  drawn.forEach(function(q){
   var mk=data.marks[q.id],g=data.groups[String(q.group)]||{},fill=byColor?(mk&&mk.final?cssColor(data.label_colors[mk.final]):cssColor('var(--mut)')):g.color;
   var faded=(focusGroup!==null&&String(q.group)!==focusGroup)||(roundOnly&&!mk)||(byColor&&!(mk&&mk.final));
   var r=Math.max(2,5.5*q.f*Math.sqrt(cam.zoom))*dpr;
   ctx.globalAlpha=faded?0.13:(0.55+0.45*(q.z+1)/2);ctx.fillStyle=fill;ctx.beginPath();ctx.arc(q.x,q.y,r,0,6.2832);ctx.fill();
   ctx.globalAlpha=faded?0.2:1;
   if(pickState&&q.id===pickState.id){ctx.strokeStyle=acc;ctx.lineWidth=3.5*dpr;ctx.stroke();selQ=q;}
   else if(nbs.indexOf(q.id)>=0){ctx.strokeStyle=acc;ctx.lineWidth=2*dpr;ctx.stroke();}
   else if(mk){ctx.strokeStyle=fg;ctx.lineWidth=1.6*dpr;ctx.stroke();}
   q.r=r;});
  ctx.globalAlpha=1;canvas.__pts=drawn;}
 function loop(){if(!spin||!is3d()){raf=null;return;}cam.yaw+=0.006;draw3d();raf=requestAnimationFrame(loop);}
 if(canvas){
  sizeCanvas();window.addEventListener('resize',function(){if(is3d()){sizeCanvas();draw3d();}});
  $$('[data-map-dim]',pane).forEach(function(b){b.addEventListener('click',function(){
   var three=b.dataset.mapDim==='3d';$$('[data-map-dim]',pane).forEach(function(x){x.classList.toggle('on',x===b);});
   svg.toggleAttribute('hidden',three);canvas.hidden=!three;$('[data-spin]',pane).hidden=!three;
   if(three){sizeCanvas();draw3d();}else{spin=false;$('[data-spin]',pane).classList.remove('on');}});});
  $('[data-spin]',pane).addEventListener('click',function(){spin=!spin;this.classList.toggle('on',spin);if(spin&&!raf){raf=requestAnimationFrame(loop);}});
  canvas.addEventListener('pointerdown',function(e){drag3={x:e.clientX,y:e.clientY,moved:false};canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener('pointermove',function(e){if(!drag3){return;}var dx=e.clientX-drag3.x,dy=e.clientY-drag3.y;
   if(!drag3.moved&&Math.abs(dx)+Math.abs(dy)<4){return;}drag3.moved=true;canvas.classList.add('dragging');
   cam.yaw+=dx*0.01;cam.pitch=Math.max(-1.45,Math.min(1.45,cam.pitch+dy*0.01));drag3.x=e.clientX;drag3.y=e.clientY;draw3d();});
  canvas.addEventListener('pointerup',function(e){var d=drag3;drag3=null;canvas.classList.remove('dragging');
   if(d&&!d.moved){var b=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1,mx=(e.clientX-b.left)*dpr,my=(e.clientY-b.top)*dpr,best=null,bd=1e9;
    (canvas.__pts||[]).forEach(function(q){var dd=Math.hypot(q.x-mx,q.y-my);if(dd<Math.max(q.r+4*dpr,10*dpr)&&(dd<bd||(best&&dd===bd&&q.z>best.z))){best=q;bd=dd;}});
    if(best){choose(best.id);}}});
  canvas.addEventListener('pointercancel',function(){drag3=null;canvas.classList.remove('dragging');});
  canvas.addEventListener('wheel',function(e){if(!e.ctrlKey){return;}e.preventDefault();cam.zoom=Math.max(0.5,Math.min(6,cam.zoom*(e.deltaY<0?1.12:1/1.12)));draw3d();},{passive:false});
  $$('[data-map-color]',pane).forEach(function(b){b.addEventListener('click',function(){draw3d();});});
 }
 $$('[data-zoom]',pane).forEach(function(b){b.addEventListener('click',function(){if(!is3d()){return;}
  if(b.dataset.zoom==='reset'){cam={yaw:0.6,pitch:0.35,zoom:1};}else{cam.zoom=Math.max(0.5,Math.min(6,cam.zoom*(b.dataset.zoom==='in'?1.3:1/1.3)));}draw3d();});});
 pane.__setPick=function(state){pickState=state;draw3d();};
});
/* ── embedding model: show one build, start a build, watch it ─ */
(function(){
 var panes=$$('.embpane');
 function showEmb(v,remember){
  if(!panes.length){return;}
  if(!panes.some(function(p){return p.dataset.emb===v;})){v=panes[panes.length-1].dataset.emb;}
  panes.forEach(function(p){p.hidden=p.dataset.emb!==v;});
  $$('.pill.tog[data-emb-show]').forEach(function(b){b.classList.toggle('on',b.dataset.embShow===v);});
  if(remember){try{var u=new URL(location.href);u.searchParams.set('emb',v);history.replaceState(null,'',u.toString());}catch(e){}}
 }
 var want=null;try{want=new URLSearchParams(location.search).get('emb');}catch(e){}
 showEmb(want,false);
 $$('[data-emb-show]').forEach(function(b){b.addEventListener('click',function(){showEmb(b.dataset.embShow,true);
  if(!b.classList.contains('tog')){var d=b.closest('details');if(d){d.open=false;}var pane=$('.embpane:not([hidden])');if(pane){pane.scrollIntoView({block:'start'});}}});});
 var timer=null,form=$('[data-emb-form]'),runBtn=$('[data-emb-run]'),runMsg=$('[data-emb-form] [data-emb-msg]');
 var info={};try{info=JSON.parse($('.embcatalog').textContent);}catch(e){}
 var choice={input_mode:'reply_context',map_method:'tsne'};
 function say(text,err){if(runMsg){runMsg.textContent=text;runMsg.className='msg'+(err?' err':'');}}
 function modelChanged(){if(!form){return;}var sel=$('[data-emb-field=model]',form),opt=sel.options[sel.selectedIndex],ins=$('[data-emb-field=instruction]',form);
  $('[data-emb-modelinfo]',form).textContent=info[sel.value]||'';ins.disabled=!(opt&&opt.dataset.instruct);
  ins.placeholder=ins.disabled?'this model takes no instruction':'optional, e.g. Represent this text by the trait being labeled';
  if(ins.disabled){ins.value='';}}
 if(form){
  modelChanged();$('[data-emb-field=model]',form).addEventListener('change',modelChanged);
  $$('[data-emb-input]',form).forEach(function(b){b.addEventListener('click',function(){choice.input_mode=b.dataset.embInput;
   $$('[data-emb-input]',form).forEach(function(x){x.classList.toggle('on',x===b);});});});
  $$('[data-emb-map]',form).forEach(function(b){b.addEventListener('click',function(){choice.map_method=b.dataset.embMap;
   $$('[data-emb-map]',form).forEach(function(x){x.classList.toggle('on',x===b);});});});
 }
 function watch(version){
  if(timer){return;}if(runBtn){runBtn.disabled=true;}
  timer=setInterval(function(){
   act('embedding_status',{}).then(function(j){
    (j.result.models||[]).forEach(function(r){
     if(r.version!==version){return;}
     if(r.state==='built'){clearInterval(timer);timer=null;
      if(current.space==='data'&&current.view==='embedding'){var u=new URL(location.href);u.searchParams.set('space','data');u.searchParams.set('view','embedding');u.searchParams.set('emb',r.version);location.href=u.toString();}
      else{say('Done: '+r.version+'. Reload the page to see it.');if(runBtn){runBtn.disabled=false;}}}
     else if(r.state==='failed'||r.state==='stopped'){clearInterval(timer);timer=null;
      say([r.failure||'The run ended early.'].concat(r.log_tail||[]).join(' · '),true);if(runBtn){runBtn.disabled=false;}}
    });
   }).catch(function(){});
  },3000);
 }
 if(runBtn){runBtn.addEventListener('click',function(){
  var g=$('[data-emb-field=groups]',form).value.trim(),seed=$('[data-emb-field=seed]',form).value.trim();
  var body={model:$('[data-emb-field=model]',form).value,input_mode:choice.input_mode,map_method:choice.map_method,
   instruction:$('[data-emb-field=instruction]',form).value.trim(),groups:g===''?null:+g,seed:seed===''?0:+seed};
  runBtn.disabled=true;say('Starting…');
  act('build_embedding',body).then(function(j){say('Running in the background as '+j.result.version+'. You can leave this view; labeling is not affected.');watch(j.result.version);})
  .catch(function(e){say(e.message,true);runBtn.disabled=false;});
 });}
 var busy=$('[data-emb-row][data-state=building]');
 if(busy){say('A run is in progress: '+busy.dataset.embRow+'.');watch(busy.dataset.embRow);}
})();
(function(){var s=null,v=null;try{var q=new URLSearchParams(location.search);s=q.get('space');v=q.get('view');}catch(e){}
 if(!s){try{var saved=JSON.parse(localStorage.getItem(key)||'null');if(saved){s=saved.space;v=saved.view;}}catch(e){}}
 select(s||boot.default_space,v,false);})();
/* ── server calls ─────────────────────────────────────────── */
var sessionId;try{sessionId=sessionStorage.getItem('labeling-session')||'';}catch(e){sessionId='';}
if(!sessionId){sessionId='s'+Date.now().toString(36)+Math.random().toString(36).slice(2,8);try{sessionStorage.setItem('labeling-session',sessionId);}catch(e){}}
function act(action,body){
 var payload=Object.assign({path:boot.path,file:boot.file,page:boot.page,action:action,
  human_id:boot.human_id,session_id:sessionId},body||{});
 if(action!=='confirm_meaning')payload.attest=true;
 return fetch('/_board/labeling/act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
  .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok){throw new Error(j.err||('HTTP '+r.status));}return j;});});
}
/* ── G0: confirm meaning ─────────────────────────────────── */
var attest=$('[data-confirm-attest]'),confirmBtn=$('[data-confirm-meaning]'),confirmMsg=$('[data-confirm-msg]');
if(attest&&confirmBtn){attest.addEventListener('change',function(){confirmBtn.disabled=!attest.checked;});
 confirmBtn.addEventListener('click',function(){
  if(!window.confirm('This records your caller attestation as '+boot.human_id+'. The Board does not verify your identity. Continue?'))return;
  confirmBtn.disabled=true;confirmMsg.textContent='Saving…';confirmMsg.className='msg';
  act('confirm_meaning',{attest:true}).then(function(){confirmMsg.textContent='Confirmed. Opening round 1…';
   var u=new URL(location.href);u.searchParams.set('space','labeling');u.searchParams.set('view','rounds');location.href=u.toString();})
  .catch(function(e){confirmMsg.textContent=e.message;confirmMsg.className='msg err';confirmBtn.disabled=false;});});}
/* ── Label: start a round; a round in progress is the server's table, labeled in chat ── */
/* chat prompts: any [data-copy] button copies its text; plain http needs the textarea fallback */
function toast(m,bad){var t=$('#cc-toast');if(!t){t=document.createElement('div');t.id='cc-toast';t.setAttribute('role','status');document.body.appendChild(t);}
 t.textContent=m;t.className='on'+(bad?' bad':'');clearTimeout(toast.t);toast.t=setTimeout(function(){t.className='';},2400);}
function legacyCopy(t){
 var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);
 a.focus();a.select();var ok=false;try{ok=document.execCommand('copy');}catch(e){}document.body.removeChild(a);
 return ok?Promise.resolve():Promise.reject(new Error('Legacy clipboard copy failed'));}
function copyText(t){
 if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).catch(function(){return legacyCopy(t);});}
 return legacyCopy(t);}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-copy]');if(!b){return;}
 copyText(b.dataset.copy).then(function(){toast('Copied — paste it into this chat to discuss.');},function(){toast('Copy failed. Check clipboard access and try again.',true);});});
var app=$('#label-app');
var AI_NAMES=/^(lamda|assistant|bot|chatbot|ai|model|system|gpt|chatgpt|claude|bard|gemini|agent)$/i;
function who(tag){return AI_NAMES.test(String(tag||'').trim())?'AI':String(tag||'');}
function roundWords(id){var m=String(id||'').match(/^round_0*(\d+)$/);return m?'round '+m[1]:String(id||'');}
function message(html){app.innerHTML='<div class=card>'+html+'</div>';}
function load(){
 if(!app){return;}
 if(boot.hold){message('<p class=warn>This job is read-only.</p><p class=mut>'+esc($('.next')?$('.next').textContent:'')+'</p>');return;}
 if(boot.phase!=='P1'){
  if(boot.g0_open){message('<p><b>Step 1 first:</b> confirm what the labels mean.</p><div class=actions><button class=primary type=button id=go-confirm>Go to Confirm meaning</button></div>');
   $('#go-confirm').addEventListener('click',function(){select('data','contract',true);});}
  else{message('<p class=mut>Labeling opens after P0 Contract passes.</p>');}
  return;}
 var cur=boot.current_round, rounds=boot.rounds||[];
 if(!cur&&rounds.length&&rounds[rounds.length-1].state==='judged'){
  var r=rounds[rounds.length-1];message('<p class=ok>'+esc(r.round_id)+' is done: '+r.finals+' of '+r.batch_size+' labeled.</p><p class=mut>Next the guideline is learned from your answers and the round is closed by the Checkpoint Keeper. That step is not built yet, so a new round cannot start.</p>');return;}
 if(!cur){
  var sizes=[10,20,30,50];if(sizes.indexOf(boot.batch_default)<0){sizes.push(boot.batch_default);sizes.sort(function(a,b){return a-b;});}
  message('<h2>Start round 1</h2><p>Round 1 picks items at random from the items to label. Held-back test items are never picked.</p>'+
   '<div class=line><span class=lbl>how many</span>'+sizes.map(function(n){return '<button type=button class="pill tog'+(n===boot.batch_default?' on':'')+'" data-size='+n+'>'+n+'</button>';}).join('')+'</div>'+
   '<div class=actions><button class=primary type=button id=start-round>Start round 1</button><span class=msg id=start-msg role=status></span></div>');
  var size=boot.batch_default;$$('[data-size]',app).forEach(function(b){b.addEventListener('click',function(){size=+b.dataset.size;$$('[data-size]',app).forEach(function(x){x.classList.toggle('on',x===b);});});});
  $('#start-round').addEventListener('click',function(){var btn=this;btn.disabled=true;$('#start-msg').textContent='Drawing…';
   act('release_round',{n:size}).then(function(){location.reload();})
   .catch(function(e){$('#start-msg').textContent=e.message;$('#start-msg').className='msg err';btn.disabled=false;});});
  return;}
}
load();
})();
"""


# ── Board level: every labeling job on one Board (zoom out) ───────────────────


def _board_root_url(path_q: str) -> str:
    path = urlparse(path_q or "").path
    return path[: -len("/board.md")] if path.endswith("/board.md") else path.rsplit("/", 1)[0]


def _job_urls(path_q: str, page: dict) -> tuple[str, str]:
    """(page-level Labeling URL, generated Board page URL) for one Board page."""
    root = _board_root_url(path_q)
    stem = Path(page.get("file") or page.get("id") or "").stem
    page_url = f"{root}/board/{group_token(page.get('group') or '') or '_ungrouped'}/{stem}.html"
    labeling_url = "/_board/labeling?path=%s&file=%s&page=%s" % (
        quote(path_q), quote(page.get("file") or ""), quote(page_url))
    return labeling_url, page_url


def _job_row(page_src: Path, page: dict, path_q: str) -> dict:
    vm = _view_model(page_src)
    state, canonical, cal, config = vm["state"], vm["canonical"], vm["cal"] or {}, vm["config"]
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    manifest, sealed = vm["manifest"], vm["sealed"]
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    rounds = cal.get("rounds") or []
    current = cal.get("current_round")
    labeled = sum(int(r.get("finals") or 0) for r in rounds)
    n_items = manifest.get("n_items")
    n_sealed = manifest.get("n_sealed", sealed.get("n_items"))
    n_dev = manifest.get("n_eligible")
    if n_dev is None and isinstance(n_items, int) and isinstance(n_sealed, int):
        n_dev = n_items - n_sealed
    if state["authority_hold"]:
        kind, badge, rank = "hold", "Read-only", 5
    elif state["canonical_integrity_errors"]:
        kind, badge, rank = "repair", "Needs repair", 4
    elif canonical and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation":
        kind, badge, rank = "confirm", "Confirm meaning", 1
    elif cal.get("phase") == "P1" and current:
        kind, badge, rank = "labeling", f"Labeling {current['finals']}/{current['batch_size']}", 0
    elif cal.get("phase") == "P1" and rounds and rounds[-1]["state"] == "judged":
        kind, badge, rank = "judged", f"{_round_words(rounds[-1]['round_id'])} done", 3
    elif cal.get("phase") == "P1":
        kind, badge, rank = "ready", "Start round 1", 2
    else:
        kind, badge, rank = "other", str(canonical.get("phase") or "P0"), 4
    next_line, _ = _next_step(vm)
    labeling_url, page_url = _job_urls(path_q, page)
    return {
        "id": page.get("id"), "title": page.get("title"), "file": page.get("file"),
        "target": construct.get("name") or "", "question": construct.get("question") or "",
        "source": source.get("name") or "", "n_dev": n_dev, "n_sealed": n_sealed,
        "human": authority.get("human_id") or "", "kind": kind, "badge": badge, "rank": rank,
        "labeled": labeled, "current": current, "rounds": len(rounds), "runs": len(vm["runs"]),
        "next": next_line, "labeling_url": labeling_url, "page_url": page_url,
    }


def board_jobs(board_dir: Path, path_q: str, probe: bool = False) -> dict:
    """Every Page on the Board that owns a labeling/ job, plus the ones that do not."""
    pages = _board_pages(Path(board_dir))
    jobs, empty = [], []
    for page in pages:
        page_src = Path(board_dir) / (page.get("file") or "")
        if not is_labeling_surface_page(page_src):
            continue
        lane, _ = _labeling_lane(page_src)
        if not (lane / "config.yaml").is_file():
            if page_src.name.startswith("S-Label-"):
                empty.append({"id": page.get("id"), "title": page.get("title")})
            continue
        if probe:
            jobs.append({"id": page.get("id")})
            continue
        try:
            jobs.append(_job_row(page_src, page, path_q))
        except Exception as error:  # one broken job must not hide the others
            labeling_url, page_url = _job_urls(path_q, page)
            jobs.append({"id": page.get("id"), "title": page.get("title"), "kind": "repair",
                         "badge": "Needs repair", "rank": 4, "next": type(error).__name__,
                         "labeling_url": labeling_url, "page_url": page_url})
    jobs.sort(key=lambda j: (j.get("rank", 9), str(j.get("id"))))
    return {"jobs": jobs, "empty": empty}


def render_board(board_dir: Path, path_q: str) -> str:
    data = board_jobs(board_dir, path_q)
    jobs = data["jobs"]
    waiting = [j for j in jobs if j["kind"] in {"labeling", "confirm", "ready"}]
    if not jobs:
        headline = "No Page on this Board has a labeling job yet."
    elif waiting:
        headline = f"{len(waiting)} of {len(jobs)} jobs wait for you. Start with {waiting[0]['id']}: {waiting[0]['badge'].lower()}."
    else:
        headline = f"{len(jobs)} jobs. None is waiting for you right now."
    def record(job: dict) -> str:
        pill = {"confirm": "acc", "labeling": "acc", "ready": "acc", "judged": "ok",
                "hold": "mut", "repair": "warn"}.get(job["kind"], "mut")
        data_bits = [x for x in (
            job.get("source") or "",
            f"{job['n_dev']} to label" if job.get("n_dev") is not None else "",
            f"{job['n_sealed']} held back for the test" if job.get("n_sealed") is not None else "",
            f"{job['labeled']} labeled" if job.get("labeled") else "",
        ) if x]
        rows = [
            _row("Target", f"<code>{_esc(job.get('target') or '')}</code>") if job.get("target") else "",
            _row("Data", _esc(" · ".join(data_bits))) if data_bits else "",
            _row("Labeler", _esc(job.get("human"))) if job.get("human") else "",
        ]
        rows.append(_row("Next", _esc(job["next"])))
        return (
            f'<a class="rec job {_esc(job["kind"])}" href="{_esc(job["labeling_url"])}" data-job="{_esc(job["id"])}">'
            f'<div class=rh><span class=rid>{_esc(job["id"])}</span>'
            f'<span class=rt>{_esc(job.get("question") or job.get("title") or job.get("target"))}</span>'
            f'<span class="pill {pill}">{_esc(job["badge"])}</span></div>'
            f'<div class=rrows>{"".join(rows)}</div></a>'
        )

    groups = ""
    if waiting:
        groups += '<div class=rgrp>Waiting for you</div>' + "".join(record(j) for j in waiting)
    others = [j for j in jobs if j not in waiting]
    if others:
        groups += '<div class=rgrp>Other jobs</div>' + "".join(record(j) for j in others)
    if not jobs:
        groups = f'<p class=mut>{_esc(headline)}</p>'
    empty = ""
    if data["empty"]:
        empty = ('<p class=mut>Pages with no labeling job yet: '
                 + ", ".join(_esc(e["id"]) for e in data["empty"])
                 + '. Ask Claude in Studio Chat to start one (/subjective-label).</p>')
    name = Path(board_dir).name
    tally = f'{len(waiting)} waiting · {len(jobs)} jobs'
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Labeling · {_esc(name)}</title><style>{_CSS}{_BOARD_CSS}</style></head><body>'
        '<h1>🏷 Labeling · all jobs</h1>'
        f'<p class="lead next"><b>Next:</b> {_esc(headline)}</p>'
        f'<div class=card style="margin-top:10px"><h2>Labeling jobs<span class=tally>{_esc(tally)}</span></h2>'
        f'<p class=mut>Board folder: <code>{_esc(name)}</code></p>'
        f'{groups}</div>{empty}'
        '<p class=mut>Click a job to open it. Inside a job, "← All labeling jobs" brings you back here.</p>'
        '</body></html>'
    )


_BOARD_CSS = """
a.rec{display:block;color:var(--fg);text-decoration:none;border-radius:6px;margin:0 -6px;padding:8px 6px 6px}
a.rec:hover,a.rec:focus-visible{background:color-mix(in srgb,var(--acc) 6%,var(--card));outline:none}
.rgrp:first-of-type{margin-top:4px}
"""


class LabelingMixin:
    """The 🏷 tab: five Spaces over one labeling/ lane, plus the labeling writer door."""

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

    def _labeling_board_target(self, path_q: str):
        got = self.target({"path": path_q, "file": "board.md"})
        if got[0] is None:
            return None, got[1]
        if Path(got[0]).name != "board.md":
            return None, "the Board-level Labeling view needs file=board.md"
        return got[1], None

    def labeling_board_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        board_dir, err = self._labeling_board_target(path_q)
        if board_dir is None:
            return self.reply(400, {"ok": False, "err": err})
        body = render_board(board_dir, path_q).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_labeling_board(self, p):
        path_q = p.get("path") or ""
        board_dir, err = self._labeling_board_target(path_q)
        if board_dir is None:
            return None, err
        count = len(board_jobs(board_dir, path_q, probe=True)["jobs"])
        return {"url": "/_board/labeling-board?path=%s" % quote(path_q), "jobs": count}, None

    def labeling_act(self, p):
        """The only write door: every action re-checks authority in the engine.

        ``human_id`` and ``attest`` are caller assertions, not authenticated
        identity evidence. The UI requires an explicit confirmation gesture;
        deployments that need identity assurance must add an authenticated
        principal provider before treating this receipt as verified.
        """
        origin = self.headers.get("Origin") or ""
        host = self.headers.get("Host") or ""
        if p.get("action") == "confirm_meaning" and not origin:
            return 403, {"ok": False, "err": "meaning confirmation requires the Board origin"}
        if origin and urlparse(origin).netloc != host:
            return 403, {"ok": False, "err": "cross-origin labeling write refused"}
        got = self.target(p)
        if got[0] is None:
            return 400, {"ok": False, "err": got[1]}
        page_src, board_dir = got
        if not is_labeling_surface_page(page_src):
            return 404, {"ok": False, "err": "Page has no labeling lane"}
        if not studio_chat_page_url(p.get("path") or "", p.get("file") or "",
                                    p.get("page") or "", board_dir):
            return 400, {"ok": False, "err": "missing or mismatched generated Page URL"}
        if p.get("attest") is not True:
            return 400, {"ok": False, "err": "labeling writes need an explicit caller attestation"}
        root, _ = _labeling_lane(page_src)
        if not (root / "gates" / "p0-contract" / "receipt.json").is_file():
            return 409, {"ok": False, "err": "this Page has no canonical labeling job"}
        cal = _calibration_module()
        jobmod = _canonical_job_module()
        if cal is None or jobmod is None:
            return 500, {"ok": False, "err": "subjective-label engine unavailable"}
        human = str(p.get("human_id") or "")
        session = re.sub(r"[^A-Za-z0-9_-]", "", str(p.get("session_id") or ""))[:40] or "browser"
        action = p.get("action")
        try:
            if action == "confirm_meaning":
                page_file = root.parent / page_src.name
                result = jobmod.confirm_meaning(
                    job_root=root, page_file=page_file, human_id=human,
                    confirmed_at=cal.now_iso(), accept_current_schema=True,
                    attest_as_human=p.get("attest") is True,
                    channel="board labeling screen")
            elif action == "release_round":
                result = cal.release_round(root, human_id=human, n=int(p.get("n") or 0) or None,
                                           channel="board labeling screen")
            elif action == "open_item":
                result = cal.open_item(root, str(p.get("round_id") or ""), human_id=human,
                                       session_id=session)
            elif action == "first":
                result = cal.record_first(
                    root, str(p.get("round_id") or ""), str(p.get("item_id") or ""),
                    human_id=human, session_id=session, class_label=p.get("class_label"),
                    region=p.get("region") or None, uncertainty=p.get("uncertainty"),
                    reason=str(p.get("reason") or ""))
            elif action == "final":
                result = cal.record_final(
                    root, str(p.get("round_id") or ""), str(p.get("item_id") or ""),
                    human_id=human, session_id=session, class_label=p.get("class_label"),
                    region=p.get("region") or None, uncertainty=p.get("uncertainty"),
                    change_type=str(p.get("change_type") or "none"),
                    reason=str(p.get("reason") or ""))
            elif action in {"build_embedding", "embedding_status", "embedding_item", "group_examples",
                            "embedding_item_text"}:
                embmod = _embedding_module()
                if embmod is None:
                    return 500, {"ok": False, "err": "subjective-label embedding engine unavailable"}
                if action == "embedding_item":
                    result = embmod.neighbors(root, str(p.get("version") or ""), str(p.get("item_id") or ""),
                                              k=int(p.get("k") or 6))
                elif action == "group_examples":
                    result = embmod.group_examples(root, str(p.get("version") or ""), int(p.get("group_index")),
                                                   k=int(p.get("k") or 3), offset=int(p.get("offset") or 0),
                                                   human_id=human, channel="board labeling screen")
                elif action == "embedding_item_text":
                    result = embmod.item_text(root, str(p.get("version") or ""), str(p.get("item_id") or ""),
                                              human_id=human, channel="board labeling screen")
                elif action == "build_embedding":
                    groups = p.get("groups")
                    proc, version = embmod.start_background_build(
                        root, str(p.get("model") or ""), channel="board labeling screen", started_by=human,
                        input_mode=str(p.get("input_mode") or "reply_context"),
                        instruction=p.get("instruction") or None,
                        groups=int(groups) if groups not in (None, "") else None,
                        map_method=str(p.get("map_method") or "tsne"), seed=int(p.get("seed") or 0))
                    _reap_when_done(proc)
                    result = {"version": version, "model": p.get("model")}
                else:
                    result = {"models": [{k: r.get(k) for k in ("id", "version", "state", "run", "failure", "log_tail")}
                                         for r in embmod.build_status(root)]}
            else:
                return 400, {"ok": False, "err": f"unknown labeling action: {action!r}"}
        except cal.LabelingRefused as error:
            return 409, {"ok": False, "err": str(error)}
        except RuntimeError as error:
            return 409, {"ok": False, "err": str(error)}
        except (ValueError, TypeError) as error:
            return 400, {"ok": False, "err": f"{type(error).__name__}: {error}"}
        return 200, {"ok": True, "result": result}
