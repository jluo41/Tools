"""🏷 Labeling · four Spaces over one page-local labeling/ job, a Runs panel beside each, plus one write door.

Data · Labeling · Quality · Delivery are views over canonical files; the
overview never renders item text and never upgrades an observed file to a
passed gate.  Labeling → Definition holds the label definitions and Confirm meaning.  Round item text
appears only in Labeling → Rounds, and only for items already shown to the
person; the labels come from the chat.  Every write through
``POST /_board/labeling/act`` goes through the
subjective-label engine (``job.confirm_meaning`` and ``calibration``), which
re-checks the caller-supplied configured authority id, HOLD, G0, the event
order, and sealed custody on each call. The Workbench does not authenticate
the caller's identity.
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
import shlex
import sys
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


def _page_folder_candidate(page_src: Path) -> Path:
    """The canonical Page file, whether the Board source is folded or flat."""
    if page_src.parent.name == page_src.stem:
        return page_src
    for ancestor in page_src.parents:
        if (ancestor / "board.md").is_file():
            return ancestor / "pages" / page_src.stem / page_src.name
    return page_src.parent / page_src.stem / page_src.name


def _labeling_lane(page_src: Path) -> tuple[Path, str]:
    """Resolve the page-folder lane even when Board renders a flat source.

    Some older Boards render ``<group>/<page>.md`` while keeping the page's
    task-side folder at ``pages/<page>/``.  The browser must follow that exact
    sidecar instead of silently reporting an empty lane beside the flat copy.
    """
    direct = page_src.parent / "labeling"
    folded_page = _page_folder_candidate(page_src)
    if folded_page != page_src and folded_page.is_file() and not folded_page.is_symlink():
        return folded_page.parent / "labeling", (
            "page-folder bridge from flat Board source · "
            f"pages/{page_src.stem}/labeling/"
        )
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
    keeps the presenter from maintaining a second integrity implementation and
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
    integrity and receipt failures instead of guessing from file presence.
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
        # file-presence heuristics, owns P0 integrity and receipt truth.
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
            "P0 contract and G0 meaning receipt validated"
            if g0_reported else
            "P0 is intact; human meaning confirmation/G0 receipt remains open"
        )
    else:
        g0_note = (
            "required files observed; P0 meaning confirmation remains open before G0 may be tested"
            if meaning_open else
            "required files observed; the canonical receipt is not present"
        )
    gate_rows = [
        ("G0", "Contract → Round", sum(p0.values()), len(p0), g0_reported, g0_note),
        ("G1", "Round close", len(checkpoints), len(round_dirs), False,
         (latest.get("state") or latest.get("closed") or "no checkpoint") if checkpoints else "no checkpoint"),
        ("G2", "Round → Freeze", 1 if g2_reported else 0, 1, g2_reported,
         "checkpoint reports four gates + human STOP" if g2_reported else "stopping evidence remains open"),
        ("G3", "Freeze → Test", 1 if handoff.is_file() and eval_registry.is_file() else 0, 1,
         handoff_status == "valid" and eval_registry.is_file(),
         "handoff + evaluation registry observed; handoff validation still owed"),
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
    it is not a prerequisite for opening a Page-local Workbench. The one control
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


def generated_page_url(
        path_q: str, file_q: str, page_q: str, board_dir: Path | None) -> str:
    """Validate and return the generated Page URL the Workbench belongs to.

    ``path_q`` is intentionally ``board.md`` because it resolves the source
    file.  It is not a browser Page.
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


@lru_cache(maxsize=1)
def _definition_module():
    """Load the definition-discussion Run writer (``definition_discussion.state``)."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    candidate = Path(job_module.__file__).with_name("definition_discussion.py")
    if not candidate.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "haipipe_subjective_label_definition_for_board", candidate
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


@lru_cache(maxsize=1)
def _preparation_module():
    domain = _canonical_job_module()
    if domain is None:
        return None
    candidate = Path(domain.__file__).with_name("corpus_preparation.py")
    if not candidate.is_file():
        return None
    spec = importlib.util.spec_from_file_location("subjective_label_preparation_for_board", candidate)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SPACES = (
    ("data", "Data", (("preparation", "Preparation"), ("contract", "Contract"), ("embedding", "Embedding"))),
    ("labeling", "Labeling", (("definition", "Definition"), ("rounds", "Rounds"), ("guideline", "Guideline"))),
    ("quality", "Quality", (("test", "Test"), ("evaluation", "Evaluation"), ("audit", "Audit"))),
    ("delivery", "Delivery", (("handoff", "Handoff"), ("scan", "Scan"), ("final", "Final labels"))),
)


def _esc(value) -> str:
    return html.escape("" if value is None else str(value))


def _load_mapping(path: Path) -> dict:
    module = _canonical_job_module()
    if module is None or not path.is_file():
        return {}
    value, error = module.try_load_mapping(path)
    return {} if error else value


def _run_rows(root: Path, *, owner: Path | None = None, family: str = "labeling") -> list[dict]:
    """One row per authored Ticket, with the runtime status beside it."""
    rows = []
    run_owner = owner or root.parent  # Labeling lives beside labeling/; Corpus owns its own runs/.
    runs = run_owner / "runs"
    if not runs.is_dir():
        return rows
    for ticket in sorted(runs.glob("*.yaml")):
        data = _load_mapping(ticket)
        if family == "corpus" and data.get("family") != "corpus":
            continue
        if family == "labeling" and not (
            data.get("family") == "labeling" or ticket.stem.startswith("rl")
            or re.match(r"r\d+_labeling", ticket.stem)
        ):
            continue
        runtime = _load_mapping(run_owner / "results" / ticket.stem / "runtime.yaml")
        result = (run_owner / "results" / ticket.stem / "result.yaml").is_file()
        status = str(runtime.get("status") or ("no runtime" if not runtime else "unknown"))
        if status == "complete" and not result:
            status = "complete · result.yaml missing"
        result_data = _load_mapping(run_owner / "results" / ticket.stem / "result.yaml") if result else {}
        commission = data.get("commission") if isinstance(data.get("commission"), dict) else {}
        worker = runtime.get("worker") or data.get("worker")
        worker = worker if isinstance(worker, dict) else {}
        rows.append({
            "run": ticket.stem,
            "family": family,
            "owner": str(run_owner),
            "operation": str(data.get("operation") or "?"),
            "target": str(data.get("target") or runtime.get("target") or ""),
            "status": status,
            "outcome": str(runtime.get("outcome") or "")[:160],
            "started_at": str(runtime.get("started_at") or ""),
            "finished_at": str(runtime.get("finished_at") or ""),
            "started_by": str(commission.get("started_by") or worker.get("name") or ""),
            "worker_kind": str(worker.get("kind") or ""),
            "artifacts": [str(a["path"]) for a in result_data.get("artifacts") or []
                          if isinstance(a, dict) and a.get("path")
                          and (family != "corpus" or ("private" not in str(a["path"])
                                                      and "protected" not in str(a["path"])))][:4],
            "ticket_mtime": ticket.stat().st_mtime_ns,
        })
    def order(row: dict):
        legacy = re.match(r"^rl(\d+)_", row["run"])
        return (row["started_at"], 0 if legacy else 1,
                int(legacy.group(1)) if legacy else row["ticket_mtime"], row["run"])
    rows.sort(key=order)
    seen: dict[tuple[str, str], int] = {}
    for r in rows:  # a rerun on the same target keeps the older run's plain name and counts up: -2, -3
        key = (r["operation"], r["target"] or r["run"])
        seen[key] = seen.get(key, 0) + 1
        suffix = f"-{seen[key]}" if seen[key] > 1 else ""
        r["name"] = r["run"] if r["run"].startswith("run-") else _run_name(r["run"]) + suffix
        r["label"] = (r["target"] or _run_name(r["run"])) + suffix
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
    """A view whose result does not exist yet stays blank (JL 260927: no placeholder lines)."""
    return ""


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
    page_candidate = _page_folder_candidate(page_src)
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
        "root": root, "page_src": page_src, "page_candidate": page_candidate,
        "page_ready": page_candidate.is_file() and not page_candidate.is_symlink(),
        "location_note": location_note, "state": state,
        "canonical": canonical, "config": config, "cal": cal_state,
        "manifest": _read_json(root / "corpus" / "manifest.json"),
        "sealed": _read_json(root / "test" / "sealed" / "status.json"),
        "imported": _read_json(root / "corpus" / "imported_label_summary.json"),
        "preparation": _preparation_state(root),
        "runs": _run_rows(root),
        "embedding": _embedding_state(root),
    }


def _preparation_state(root: Path) -> dict:
    owner_file = root / "preparation-owner.yaml"
    accepted_file = root / "preparation-ref.yaml"
    owner_ref = _load_mapping(owner_file)
    ref = _load_mapping(accepted_file)
    if (owner_file.is_file() and not owner_ref) or (accepted_file.is_file() and not ref):
        return {"attached": owner_file.is_file(), "linked": accepted_file.is_file(),
                "runs": [], "error": "preparation reference cannot be read"}
    if not ref:
        if not owner_ref:
            return {"attached": False, "linked": False, "runs": []}
        owner = Path(str(owner_ref.get("owner") or ""))
        source_id = str(owner_ref.get("source_id") or "")
        expected = {"schema": "subjective-label/preparation-owner-v1", "source_id": source_id}
        if (not owner.is_absolute() or owner.name != "corpus-preparation" or owner.is_symlink()
                or not source_id or _load_mapping(owner / "source.yaml") != expected
                or owner_ref != {**expected, "owner": str(owner)}):
            return {"attached": True, "linked": False, "owner_reference": owner_ref,
                    "runs": [], "error": "preparation owner reference is invalid or changed"}
        return {"attached": True, "linked": False, "owner_reference": owner_ref,
                "runs": _run_rows(root, owner=owner, family="corpus")}
    owner = Path(str(ref.get("owner") or ""))
    package = Path(str(ref.get("package") or ""))
    if (not owner.is_absolute() or owner.name != "corpus-preparation"
            or not package.is_relative_to(owner / "packages") or owner.is_symlink()):
        return {"attached": True, "linked": True, "reference": ref, "runs": [],
                "error": "preparation reference has an invalid owner or package path"}
    owner_record = _load_mapping(owner / "source.yaml")
    if owner_ref and (owner_ref != {**owner_record, "owner": str(owner)}
                      or owner_record.get("schema") != "subjective-label/preparation-owner-v1"):
        return {"attached": True, "linked": True, "reference": ref, "runs": [],
                "error": "preparation owner and accepted package references disagree"}
    module = _preparation_module()
    if module is None:
        return {"attached": True, "linked": True, "reference": ref, "runs": [],
                "error": "Corpus Preparation engine is unavailable"}
    try:
        receipt = module.verify_package(package)
        if ref != module.preparation_reference(owner, package, receipt):
            raise RuntimeError("Page preparation reference disagrees with its package or Runs")
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        return {"attached": True, "linked": True, "reference": ref, "runs": [],
                "error": f"{type(error).__name__}: {error}"}
    linked_run_names = {str(name) for name in ref["upstream_runs"]}
    runs = [run for run in _run_rows(root, owner=owner, family="corpus")
            if run["run"] in linked_run_names]
    return {"attached": True, "linked": True, "reference": ref, "runs": runs, "receipt": receipt}


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
    preparation = vm.get("preparation") or {}
    if not vm.get("page_ready", True) and not (root / "config.yaml").is_file():
        return "Create this Page's own folder before Corpus Preparation.", "data"
    if preparation.get("error"):
        return "Repair the Corpus Preparation reference before continuing.", "data"
    if preparation.get("attached") and not preparation.get("linked") and not (root / "config.yaml").is_file():
        completed = {run["operation"] for run in preparation.get("runs") or []
                     if run["status"] == "complete"}
        for operation in ("source-normalize", "unit-recipe", "unit-materialize",
                          "unit-check", "initial-group-reserve"):
            if operation not in completed:
                return f"Continue Corpus Preparation: {operation}.", "data"
        return "Review and link an accepted Corpus Preparation package to this Page.", "data"
    if preparation.get("linked") and not (root / "config.yaml").is_file():
        return "Corpus Preparation is accepted. Create this Page's Labeling Contract.", "data"
    if not root.exists():
        return "Prepare and link a corpus, then create this Page's Labeling Contract.", "data"
    if _imported_reference_only(vm):
        source = _import_source_name(vm["config"])
        return (
            f"{source}'s released ratings are here for reference. "
            "To collect new labels, use a separate job.",
            "data",
        )
    if state["authority_hold"]:
        return "Read-only: " + _hold_words(canonical.get("hold_reason") or state["authority_reason"]) + ".", "data"
    if _g0_retroactive_block(vm):
        return "A round was released without valid prior meaning confirmation. Keep this job as history; start a new job for new labels.", "labeling"
    if _g0_repair_request(vm):
        return "Restore the missing G0 receipt from the earlier human confirmation.", "labeling"
    if state["canonical_integrity_errors"]:
        return "Repair needed: " + state["canonical_integrity_errors"][0], "data"
    if _open_definition_run(vm) and _meaning_allowed(vm):
        return "Finish the open label-meaning discussion before releasing a round.", "labeling"
    if (_open_definition_run(vm) and canonical.get("phase") == "P0"
            and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation"):
        return "An earlier discussion cannot continue after round release. Review the current meanings, then confirm them.", "labeling"
    if canonical and canonical.get("phase") == "P0":
        if canonical.get("meaning_definitions_missing"):
            return "Define every label meaning in a Definition discussion before confirming G0.", "labeling"
        if canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation":
            return "Review or discuss the label meanings, then confirm them.", "labeling"
        return str(canonical.get("next_action") or "P0 Contract"), "data"
    if cal and cal.get("phase") == "P1":
        current = cal.get("current_round")
        if current:
            return (f"Label {_round_words(current['round_id'])}: {current['finals']} of "
                    f"{current['batch_size']} done."), "labeling"
        rounds = cal.get("rounds") or []
        if rounds and rounds[-1]["state"] == "judged" and rounds[-1].get("calibration_status") == "running":
            return (f"{_round_words(rounds[-1]['round_id']).capitalize()} has all final labels. "
                    "Finish its interrupted human-calibration Result from the Runs panel."), "labeling"
        if rounds and rounds[-1]["state"] == "judged":
            return (f"{_round_words(rounds[-1]['round_id']).capitalize()} is fully labeled. Next: learn the guideline and "
                    "close the round (Checkpoint Keeper, not built yet)."), "labeling"
        return "Start round 1 to begin labeling.", "labeling"
    return state["next_action"], "data"


def _data_space(vm: dict) -> dict[str, str]:
    config, manifest, sealed, imported = vm["config"], vm["manifest"], vm["sealed"], vm["imported"]
    preparation = vm.get("preparation") or {}
    if not (vm["root"] / "config.yaml").is_file():
        if not vm.get("page_ready", True):
            contract = _card("Labeling Contract", "<p>Create this Page's own folder, then "
                             "complete and link Corpus Preparation before Contract.</p>")
        elif preparation.get("linked") and not preparation.get("error"):
            package = (preparation.get("reference") or {}).get("package") or ""
            contract = _card("Labeling Contract", "".join([
                "<p>The Corpus Preparation package is accepted. Create this Page's "
                "Labeling Contract through the Runs panel.</p>",
                _row("accepted package", f"<code>{_esc(package)}</code>"),
            ]))
        else:
            contract = _card("Labeling Contract", "<p>Complete and link Corpus "
                             "Preparation before creating this Page's Contract.</p>")
        return {"preparation": _preparation_view(vm), "contract": contract,
                "embedding": _embedding_view(vm)}
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    n_items = manifest.get("n_items")
    n_sealed = manifest.get("n_sealed", sealed.get("n_items"))
    n_dev = manifest.get("n_eligible")
    if n_dev is None and isinstance(n_items, int) and isinstance(n_sealed, int):
        n_dev = n_items - n_sealed

    corpus = _card("Data", "".join([
        _row("source", _esc(source.get("name") or (config.get("corpus") or {}).get("source") or "")),
        _row("items", _esc(n_items)),
        _row("to label", _esc(n_dev)),
        _row("held back", _esc(f"{n_sealed} items for the final test; you never see them" if n_sealed is not None else "none")),
        _row("embedding", _embedding_summary(vm.get("embedding"))),
    ]))
    imported_rows = []
    for key, value in imported.items():
        if isinstance(value, dict) and value.get("field") and isinstance(value.get("values"), dict):
            counts = " · ".join(f"{_esc(k)} {_esc(v)}" for k, v in value["values"].items())
            imported_rows.append(_row(str(value["field"]), counts))
    schema = ""
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
        ]))
    return {"preparation": _preparation_view(vm), "contract": corpus + schema,
            "embedding": _embedding_view(vm)}


@lru_cache(maxsize=16)
def _corpus_shape(items: str, mtime_ns: int, size: int, text_field: str,
                  context_field: str) -> dict:
    """Word counts over the items to label only; held-back text is never read."""
    from statistics import median  # noqa: PLC0415
    text_words, context_words, meta = [], [], {}
    try:
        with open(items, encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(row, dict) or row.get("population_status") != "eligible":
                    continue
                if not meta and isinstance(row.get("source_metadata"), dict):
                    meta = row["source_metadata"]
                text_words.append(len(str(row.get(text_field) or "").split()))
                if context_field:
                    context_words.append(len(str(row.get(context_field) or "").split()))
    except OSError:
        return {}

    def spread(words: list[int]) -> str:
        return f"{median(words):g} words median, {min(words)} to {max(words)}" if words else ""

    return {"n": len(text_words), "text": spread(text_words), "context": spread(context_words),
            "no_context": sum(1 for n in context_words if n == 0), "meta": meta}


def _day_words(value) -> str:
    """'2026-09-16...' -> '16 Sep 2026'."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(value or ""))
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return f"{int(m.group(3))} {months[int(m.group(2)) - 1]} {m.group(1)}" if m else str(value or "")


def _bytes_words(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return ""


def _corpus_view_module():
    """Load the subjective-label corpus reader (``corpus_view``)."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    candidate = Path(job_module.__file__).with_name("corpus_view.py")
    if not candidate.is_file():
        return None
    spec = importlib.util.spec_from_file_location("haipipe_subjective_label_corpus_view", candidate)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _raw_corpus_card(vm: dict) -> str:
    """The raw source as a folder, and which raw column became which item field; no row values."""
    config, manifest = vm.get("config") or {}, vm.get("manifest") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    if not source and isinstance(corpus.get("source"), dict):
        source = corpus["source"]
    name = _esc(source.get("name") or "")
    if name and source.get("uri"):
        name = f'<a href="{_esc(source["uri"])}" target=_blank rel=noopener>{name}</a>'
    if name and source.get("license"):
        name += f' · {_esc(source["license"])}'
    module = _corpus_view_module()
    try:
        raw = module.raw_source(vm["root"]) if module else {}
    except (OSError, ValueError) as error:
        return _card("Raw corpus", _row("source", name) + f'<p class=warn>{_esc(error)}</p>')
    if not raw:
        return _card("Raw corpus", _row("source", name) + _row("folder", "not recorded"))
    folder = _row("folder", f'<code>{_esc(raw["folder"])}/</code>'
                  + ("" if raw["found"] else ' <span class=warn>not found on this machine</span>'))
    file_rows = []
    for f in raw["files"]:
        n_rows = f"{f['rows']:,}" if "rows" in f else ""
        file_rows.append(
            f'<tr><td><code>{_esc(f["path"])}</code></td><td class=num>{_esc(_bytes_words(f["bytes"]))}</td>'
            f'<td class=num>{_esc(n_rows)}</td><td class=num>{_esc(len(f.get("columns") or []) or "")}</td>'
            f'<td class=num>{_esc(f.get("keys") or "")}</td></tr>')
    files = "".join(file_rows)
    files_table = ('<div class=scroll><table class=items><thead><tr><th>File</th><th>Size</th><th>Rows</th>'
                   f'<th>Columns</th><th>Items</th></tr></thead><tbody>{files}</tbody></table></div>'
                   if files else "")
    main = next((f for f in raw["files"] if f["path"] == raw["file"]), {})
    used = raw["fields"]
    mapping = "".join(
        f'<tr><td><code>{_esc(col)}</code></td><td>→</td><td><code>{_esc(field)}</code></td></tr>'
        for col, field in used.items())
    others = [c for c in main.get("columns") or [] if c not in used]
    rows = [
        _row("source", name) if name else "",
        folder,
        files_table,
        _row("one row is", _esc(raw["one_row_is"])) if raw["one_row_is"] else "",
        _row("one item is", f'all rows with the same <code>{_esc(raw["item_key"])}</code>'
             + (f' ({_esc(main["keys"])} items)' if main.get("keys") else "")) if raw["item_key"] else "",
        _row("raw column → item field", f'<table class=map><tbody>{mapping}</tbody></table>') if mapping else "",
        (f'<details class=ctx><summary>other columns ({len(others)}), never shown before you label</summary>'
         f'<p class=mut>{", ".join(f"<code>{_esc(c)}</code>" for c in others)}</p></details>') if others else "",
        _row("built", _esc(" · ".join(x for x in (_day_words(raw["built_on"]), raw["built_by"]) if x)))
        if raw["built_on"] or raw["built_by"] else "",
    ]
    return _card("Raw corpus", "".join(rows))


def _items_card(vm: dict) -> str:
    """The items to label: what one item is, the counts, and a table you can page through."""
    config, manifest = vm.get("config") or {}, vm.get("manifest") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    population = manifest.get("population")
    pop = population if isinstance(population, dict) else {}
    unit = (pop.get("definition") or (population if isinstance(population, str) else "")
            or corpus.get("population") or "")
    text_field = manifest.get("text_field") or corpus.get("text_field") or "text"
    context_field = manifest.get("context_field") or corpus.get("context_field") or ""
    items = vm["root"] / (manifest.get("items_file") or "corpus/items.jsonl")
    try:
        stat = items.stat()
        shape = _corpus_shape(str(items), stat.st_mtime_ns, stat.st_size, text_field, context_field)
    except OSError:
        shape = {}
    n_sealed = manifest.get("n_sealed", (vm.get("sealed") or {}).get("n_items"))
    if n_sealed is None and isinstance(pop.get("sealed"), int):
        n_sealed = pop["sealed"]
    counts = " · ".join(x for x in (
        f'{shape["n"]} to label' if shape.get("n") else "",
        f"{n_sealed} held back, never shown" if n_sealed else "") if x)
    context = ""
    if context_field and shape.get("context"):
        context = f'<code>{_esc(context_field)}</code> · {_esc(shape["context"])}'
        if shape.get("no_context"):
            n = shape["no_context"]
            context += f' · {_esc(n)} {"item has" if n == 1 else "items have"} none'
    table = ""
    if shape.get("n") and not (vm.get("state") or {}).get("authority_hold"):
        table = ('<div class=actions><button type=button class=primary data-items-show>Show items</button></div>'
                 '<div class=scroll data-items-box hidden><table class="items itemtable"><thead><tr><th>Item</th>'
                 '<th>State</th><th>Conversation before it</th><th>Text to label</th></tr></thead>'
                 '<tbody data-items-rows></tbody></table></div><div data-items-more></div>')
    return _card("Items to label", "".join([
        _row("one item is", _esc(unit)) if unit else "",
        _row("items", _esc(counts)) if counts else "",
        _row("text", f'<code>{_esc(text_field)}</code> · {_esc(shape["text"])}') if shape.get("text") else "",
        _row("context", context) if context else "",
        _row("kept together", "no encounter is split across the held-back test")
        if pop.get("encounter_straddle_across_seal") == [] else "",
        table,
    ]))


def _preparation_view(vm: dict) -> str:
    prep = vm.get("preparation") or {}
    has_job = (vm["root"] / "config.yaml").is_file()
    if not vm.get("page_ready", True) and not has_job:
        source = vm["page_src"]
        target = vm["page_candidate"]
        prompt = (f"Use /haipipe-page to create the canonical Page folder for {source}. "
                  f"The Page file should be {target}. Preserve the Board source and its "
                  "existing content. Return to Data → Preparation after the Page folder exists.")
        return _card("Page folder needed", "".join([
            "<p>Corpus Preparation needs this Page's own folder. The current Board source "
            "is flat, so it cannot own an isolated <code>labeling/</code> lane yet.</p>",
            _row("Page file to create", f"<code>{_esc(target)}</code>"),
            f'<div class=actions><button type=button class=primary data-copy="{_esc(prompt)}">'
            "Copy Page-folder request</button></div>",
        ]))
    corpus = _raw_corpus_card(vm) + _items_card(vm) if has_job else ""
    if prep.get("error"):
        return corpus + _card("Corpus Preparation", f'<p class=warn>{_esc(prep["error"])}</p>')
    if not prep.get("linked"):
        if not prep.get("attached"):
            if corpus:
                return corpus
            prompt = ("Use /subjective-label-preparation for the Page whose labeling folder is at "
                      f"{_job_where(vm)}. Identify the transcript JSONL and source owner, attach "
                      "that owner to this Page, then work through the five Corpus Preparation "
                      "Run Types in order. Link the accepted package before creating a Labeling Contract.")
            return _card("Corpus Preparation", "<p>Attach a source preparation owner to this Page, "
                         "then use the Run Types on the right in order.</p>"
                         f'<div class=actions><button type=button class=primary data-copy="{_esc(prompt)}">'
                         "Copy setup request</button></div>")
        owner_ref = prep["owner_reference"]
        completed = len({run["operation"] for run in prep["runs"] if run["status"] == "complete"})
        return corpus + _card("Corpus Preparation", "".join([
            _row("source", f'<code>{_esc(owner_ref["source_id"])}</code>'),
            _row("owner", f'<code>{_esc(owner_ref["owner"])}</code>'),
            _row("Run Types finished", _esc(f"{completed} of 5")),
            _row("next", _esc(_next_step(vm)[0])),
        ]))
    receipt = prep["receipt"]
    ref = prep["reference"]
    rows = [
        _row("source", f'<code>{_esc(receipt["snapshot_id"])}</code>'),
        _row("recipe", f'<code>{_esc(receipt["recipe_id"])}</code>'),
        _row("item set", f'<code>{_esc(receipt["item_set_id"])}</code>'),
        _row("partition", f'<code>{_esc(receipt["partition_id"])}</code>'),
        _row("development", _esc(receipt["n_eligible"])),
        _row("held back", _esc(receipt["n_sealed"])),
        _row("status", '<span class=ok>accepted · whole source groups kept together</span>'),
        _row("owner", f'<code>{_esc(ref["owner"])}</code>'),
    ]
    return corpus + _card("Corpus Preparation", "".join(rows))


def _meaning_gate(vm: dict) -> str:
    """Confirm meaning (G0): the gate on the label meanings, so it sits in Labeling › Definition."""
    config, state, canonical = vm.get("config") or {}, vm.get("state"), vm.get("canonical") or {}
    if not state:
        return ""
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
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
        gate = _card("Meaning confirmed ✓", f'<p class=ok>Caller attested as {_esc(receipt.get("human_id"))}, {_esc(_when(receipt.get("confirmed_at")))}.</p>')
    elif _g0_retroactive_block(vm):
        gate = _card("Meaning confirmation unavailable", '<p class=warn>A round was released '
                     'without a valid earlier meaning confirmation. G0 cannot be confirmed '
                     'retroactively for that round. Keep this job as history and start a new '
                     'job for new labels.</p>')
    elif _open_definition_run(vm) and _meaning_allowed(vm):
        gate = _card("Meaning discussion open", '<p>Finish the open discussion in the Runs '
                     'panel before confirming the meanings.</p>')
    elif canonical.get("meaning_definitions_missing") and not canonical.get("g0_retroactive_block"):
        names = ", ".join(str(value) for value in canonical["meaning_definitions_missing"])
        gate = _card("Define label meanings first", f'<p>These labels still need meanings: {_esc(names)}. '
                     'Use the Definition discussion Run to decide their wording before confirming G0.</p>')
    elif _g0_repair_request(vm) or (canonical and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation"):
        repair = _g0_repair_request(vm)
        region_meanings = regions.get("meanings") if isinstance(regions.get("meanings"), dict) else {}
        gate = _card("Restore G0 receipt" if repair else "Confirm the meaning", (
            ("<p>An intact earlier human confirmation already records these meanings. "
             "Restore its missing G0 receipt; this does not create a new semantic decision.</p>"
             if repair else
             "<p>Confirming records your attestation that these classes, boundary regions, "
             "and unsure levels match your intended meaning. The Workbench does not authenticate identity.</p>") +
            '<details><summary>boundary regions</summary>'
            f'{_meaning_list([str(v) for v in regions.get("values") or []], region_meanings)}</details>'
            '<label class=attest><input type=checkbox data-confirm-attest> '
            'These meanings are what I mean.</label>'
            f'<div class=actions><button class=primary type=button data-confirm-meaning disabled>{"Restore G0 receipt" if repair else "Confirm meaning"}</button>'
            '<span class=msg role=status data-confirm-msg></span></div>'
        ), "focus")
    else:
        gate = _card("Meaning", f'<p class=mut>{_esc(state["first_failed"])}</p>')

    return gate


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
        return '<span class=mut>not built</span>'
    labels = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                             for b in builds])
    names = "<br>".join(_esc(labels[b["manifest"]["version"]]) for b in builds)
    return f'{names}<br><span class=mut>{len(builds)} built</span>'


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
        if state in {"none", "built"}:  # a finished build is listed in the Runs panel; only builds that need you stay here
            continue
        cls, text = _STATE_PILL.get(state, ("mut", state))
        button = (f'<button class=ghost type=button data-emb-show="{_esc(r["version"])}">Show</button>'
                  if state == "built" else "")
        started, started_cls = _started_text(r.get("started")) if r.get("started") else ("", "")
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
        + f'<div class=runbox data-emb-formbox><h3>Run a new embedding</h3>{form}</div>'
        + runs_table
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
    flags = []
    if settings.get("input") and settings["input"] != "reply_context":
        flags.append(f'--input {shlex.quote(str(settings["input"]))}')
    if settings.get("instruction"):
        flags.append(f'--instruction {shlex.quote(str(settings["instruction"]))}')
    if settings.get("groups"):
        flags.append(f'--groups {int(settings["groups"])}')
    if settings.get("map") and settings["map"] != "tsne":
        flags.append(f'--map {shlex.quote(str(settings["map"]))}')
    if int(settings.get("seed") or 0):
        flags.append(f'--seed {int(settings["seed"])}')
    return "".join(" " + f for f in flags)


def _engine_command(script: str, *args: str) -> str:
    """Build a replay command from this installed package and host Python."""
    path = Path(__file__).resolve().parents[2] / "engine" / script
    return " ".join(shlex.quote(part) for part in (sys.executable, str(path), *map(str, args)))


def _embedding_build_view(vm: dict, emb: dict) -> str:
    root, config = vm["root"], vm["config"]
    m = emb["manifest"]
    model_id = str(m["model"]["id"])
    model_name = model_id.rsplit("/", 1)[-1]
    settings = m.get("settings") or {}
    command = (_engine_command("embedding_build.py", "build", "--job-root", _repo_relative(root),
                               "--started-by", "<your name>", "--model", model_id)
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
        f'<p class=mut>held back, not embedded: {_esc(pop.get("sealed_excluded", 0))}</p></div>'
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
        f'<p class=mut>◯ picked {_esc(drawn)} · labeled {_esc(done)}</p>'
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
        '</div>'
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
        _row("rebuild", f'<code>{_esc(command)}</code>'),
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
            for n in item.get("feedback") or [])
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


def _chat_prompt(vm: dict, current: dict, draw: dict, *, run: dict | None = None) -> str:
    """The text to paste into a Claude chat to go on labeling this round; it writes nothing."""
    root, config = vm["root"], vm.get("config") or {}
    round_id = str(current.get("round_id") or "")
    page = vm.get("page_candidate") or vm.get("page_src") or root.parent / f"{root.parent.name}.md"
    board = next((folder / "board.md" for folder in page.parent.parents
                  if (folder / "board.md").is_file()), None)
    run_id = str((run or {}).get("run") or current.get("calibration_run") or "")
    matching = run or next((r for r in vm.get("runs") or [] if r.get("run") == run_id), None)
    run_state = str(matching.get("status") or "unknown") if matching else ("not started" if not run_id else "recorded")
    skills = _run_type_skills().get("human-calibration") or []
    card = draw.get("card") or {}
    released_card = bool(card.get("released_at") and card.get("released_by")
                         and (root / "rounds" / round_id / "card.md").is_file())
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = (config.get("labels") or {}).get("values") if isinstance(config.get("labels"), dict) else None
    human = ((config.get("authority") or {}) if isinstance(config.get("authority"), dict) else {}).get("human_id") or "me"
    tag = lambda i: f'#{(i.get("order") or 0) + 1} item {i["item_id"]}'
    finals = [f'{tag(i)} (first: {i["first"]})' for i in draw["items"] if i["state"] == "answered"]
    todo = [tag(i) for i in draw["items"] if i["state"] == "waiting"][:5]
    lines = [
        f'Continue labeling {_round_words(current.get("round_id"))} of {root.parent.name} with me ({human}).',
        f'Board: {_repo_relative(board) if board else "none (standalone Page)"}',
        f'Page: {_repo_relative(page)}',
        f'Folder: {_repo_relative(root.parent)}',
        f"Job folder: {_job_where(vm)}",
        f'Run Type: human-calibration · target: {round_id}',
        f'Declared Skills: {" · ".join(skills) if skills else "see Run Type map"}',
        f'Run: {run_id or "none yet"} · status: {run_state}',
        f'Prerequisite: G0 {"passed" if (vm.get("canonical") or {}).get("g0_passed") else "not verified"}; '
        f'released Card {"verified" if released_card else "not verified"}.',
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
        'Follow /subjective-label-rounds, JUDGE "By chat" (engine/calibration.py):',
        "1. Call open_item for the next unfinished item, even if it was shown earlier. Show me its conversation and AI reply.",
        "2. Record only what I say: record_first for my first answer, then show any available reference observations and your view.",
        "3. record_final when I keep or change; add_feedback for a note about an item.",
        "If first or lock was already recorded, open_item finishes a missing reveal; never repeat record_first.",
        "Never show reference observations or your view before my first answer is recorded.",
    ]
    return "\n".join(lines)


def _meaning_prompt(vm: dict, run: str | None = None) -> str:
    """The definition-discussion prompt: start a new discussion, or resume ``run``. It writes nothing itself."""
    config = vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    human = authority.get("human_id") or "me"
    values = [str(v) for v in labels.get("values") or []]
    meanings = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    where = _job_where(vm)
    tool = _engine_command("definition_discussion.py", "start", "--job-root", where,
                           "--human-id", human)
    lines = [
        f"Discuss what the labels of {vm['root'].parent.name} mean with me ({human}), one label at a time. "
        "I decide what each label means; you ask and propose.",
        f"Job folder: {where}",
        f'Question: {construct.get("question") or construct.get("name") or ""}',
    ]
    rule = " ".join(str(x) for x in (construct.get("seed"), construct.get("scope")) if x)
    if rule:
        lines.append(f"Rule: {rule}")
    lines.append("Labels now:")
    lines += [f"- {v}: {meanings.get(v) or ''}" for v in values]
    module = _definition_module()
    state = module.state(vm["root"], run) if (module and run) else None
    if state:
        settled = [f'{r["label"]} ({r["decision"]})' for r in state["labels"] if r["decision"]]
        lines.append(f"Run: {run} (open). Settled: {', '.join(settled) or 'none yet'}. "
                     f"Open: {', '.join(state['open']) or 'none'}.")
    else:
        lines.append("Start the Run: " + tool)
    lines += [
        "",
        "How (engine/definition_discussion.py):",
        "1. Take the next open label. Ask me one question at a time: what makes a response this label and not "
        "its neighbour? Propose clearer wording, one made-up example, and one made-up counterexample.",
        "2. Never use an item from a round as an example, and never say how you would label one.",
        "3. Keep the talk with say: --author model for your questions and proposals, --author human for my words.",
        "4. When I settle a label, record only my decision with decide: --keep, or --meaning with my wording, "
        "plus --reason in my words.",
        "5. When every label is settled, run close (add --open-question for anything we left open). "
        "If a wording changed, I press Confirm meaning again in Labeling > Definition.",
    ]
    return "\n".join(lines)


def _meaning_allowed(vm: dict) -> bool:
    """Match the discussion writer's Contract, authority, and round gates."""
    canonical = vm.get("canonical") or {}
    config = vm.get("config") or {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    module = _canonical_job_module()
    if (not canonical.get("p0_contract_integrity_valid") or canonical.get("hold")
            or not (labels or {}).get("values") or module is None):
        return False
    try:
        return (not module._judged_items(vm["root"])
                and not any((vm["root"] / "rounds").glob("round_*/card.md")))
    except (OSError, ValueError, KeyError, RuntimeError):
        return False


def _g0_retroactive_block(vm: dict) -> bool:
    canonical = vm.get("canonical") or {}
    if canonical.get("g0_passed") or not canonical.get("p0_contract_integrity_valid"):
        return False
    if canonical.get("g0_retroactive_block"):
        return True
    module = _canonical_job_module()
    if module is None:
        return False
    try:
        return not module.g0_repairable_after_round(vm["root"], vm.get("config") or {})
    except (OSError, ValueError, KeyError, RuntimeError):
        return True


def _g0_repair_request(vm: dict) -> bool:
    """Show the repair door only for an intact, already-confirmed meaning receipt."""
    canonical = vm.get("canonical") or {}
    return bool(canonical.get("p0_contract_integrity_valid")
                and canonical.get("meaning_receipt_valid")
                and not canonical.get("g0_receipt_valid")
                and not canonical.get("hold")
                and canonical.get("g0_integrity_errors") ==
                ["G0 receipt missing after semantic confirmation"]
                and not _g0_retroactive_block(vm))


def _open_definition_run(vm: dict) -> dict | None:
    """The active discussion owns Resume; a second Ticket is not available yet."""
    return next((run for run in reversed(vm.get("runs") or [])
                 if run.get("operation") == "definition-discussion"
                 and run.get("status") == "running"), None)


def _label_definitions(vm: dict) -> str:
    """Labeling → Definition: what each label means; discussing them is the definition-discussion Run."""
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
    still_valid = (vm.get("canonical") or {}).get("meaning_receipt_valid", True)  # a stale receipt is no confirmation
    confirmed = (f'by {_esc(receipt.get("human_id"))}, {_esc(_when(receipt.get("confirmed_at")))}'
                 if receipt.get("confirmed_at") and still_valid else "")
    rows = "".join(
        f'<tr><td class=nowrap><b>{_esc(v)}</b></td><td>{_esc(meanings.get(v) or "")}</td></tr>' for v in values)
    between_rows = "".join(
        f'<tr><td class=nowrap><code>{_esc(r)}</code></td><td>{_esc(region_meanings.get(r) or "")}</td></tr>'
        for r in between)
    return _card("Label definitions", "".join([
        _row("question", _esc(construct.get("question") or construct.get("name") or "")),
        _row("judge", _esc(construct.get("seed"))) if construct.get("seed") else "",
        _row("scope", _esc(construct.get("scope"))) if construct.get("scope") else "",
        _row("confirmed", confirmed),
        '<div class=scroll><table class=defs><thead><tr><th>Label</th><th>What it means</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>',
        ('<h3 class=sub>In-between cases</h3>'
         '<div class=scroll><table class=defs><thead><tr><th>Case</th><th>What it means</th></tr></thead>'
         f'<tbody>{between_rows}</tbody></table></div>') if between else "",
        (f'<p class=mut>How sure: {_esc(" · ".join(_unsure_words(v) for v in uncertainty["levels"]))} unsure. '
         f'{_esc(uncertainty.get("meaning") or "")}</p>') if uncertainty.get("levels") else "",
    ]))


def _discussion_view(vm: dict) -> str:
    """Each definition-discussion Run: every label before and after, and what stayed open.

    Starting or resuming a discussion is the Runs panel's `+ New Run` / `Resume` (JL 260927); this view
    shows what the discussions decided. The newest shows; picking a run in the panel shows that one.
    """
    module = _definition_module()
    runs = [r for r in vm.get("runs") or [] if r["operation"] == "definition-discussion"]
    records = []
    for i, run in enumerate(reversed(runs)):  # newest first, shown
        try:
            state = module.state(vm["root"], run["run"]) if module else None
        except (OSError, ValueError, KeyError):
            state = None
        if not state:
            continue
        rows = "".join(
            f'<tr><td class=nowrap><b>{_esc(r["label"])}</b></td><td>{_esc(r["before"])}</td>'
            f'<td class="{"changed" if r["decision"] == "change" else "mut"}">'
            f'{_esc(r["after"] if r["decision"] == "change" else ("kept" if r["decision"] else ""))}</td>'
            f'<td>{_esc(r["reason"])}</td></tr>' for r in state["labels"])
        questions = "".join(f"<li>{_esc(q)}</li>" for q in state["open_questions"])
        records.append(
            f'<div class=discrec data-target="{_esc(run.get("target") or "")}"{" hidden" if i else ""}>'
            '<div class=scroll><table class=defs><thead><tr><th>Label</th><th>Before</th><th>After</th>'
            f'<th>Why</th></tr></thead><tbody>{rows}</tbody></table></div>'
            + (f'<h3 class=sub>Still open</h3><ul>{questions}</ul>' if questions else "") + '</div>')
    return _card("Discussion", "".join(records)) if records else ""


def _rounds_view(vm: dict) -> str:
    cal, root = vm["cal"] or {}, vm["root"]
    rounds = cal.get("rounds") or []
    if not rounds:
        return _card("Rounds", "<p class=mut>No round yet.</p>")
    groups, keywords, model_name = _map_groups(vm)
    current = cal.get("current_round") or {}
    labeling_now = bool(current) and not (vm.get("canonical") or {}).get("hold")
    cards = []
    for r in reversed(rounds):
        draw = _round_draw(root, r["round_id"])
        is_current = labeling_now and r["round_id"] == current.get("round_id")
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
            coverage = f'<p class=mut>map groups {len(seen_groups)} / {total_groups} · {_esc(model_name)}</p>'
        started_at = _when(card.get("released_at")) if card.get("released_at") else ""
        cards.append(
            f'<details class=roundbox data-target="{_esc(str(r["round_id"]).replace("_", "-"))}"{" open" if is_current else ""}><summary><b>{_esc(_round_words(r["round_id"]).capitalize())}</b>'
            f'<span>{_esc(r["finals"])} of {_esc(r["batch_size"])} labeled</span>'
            f'<span class=mut>{_esc(state_words)}{" · started " + _esc(started_at) if started_at else ""}</span></summary>'
            f'{"".join(rows)}'
            f'<h3 class=sub>The items this round drew · {len(draw["items"])}</h3>'
            f'{_items_table(draw, groups, keywords)}'
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
        guide = _card(f"Guideline {policy}", f'<div class=guide>{_guideline_html(text)}</div>')
    else:
        guide = _card("Guideline", "<p class=mut>No guideline version is readable yet.</p>")
    return {"definition": label + _discussion_view(vm) + _meaning_gate(vm), "rounds": rounds_html, "guideline": guide}


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
        ]))
    else:
        test = _later("P0 Contract")
    evaluation = (_card("Evaluation", _row("registry", "present")) if (root / "evaluation" / "registry.yaml").is_file()
                  else _later("P3 Test"))
    audits = sorted((root / "audit").glob("final_*")) if (root / "audit").is_dir() else []
    audit = _card("Audit", _row("audits", _esc(len(audits)))) if audits else _later("P5 Audit")
    return {"test": test, "evaluation": evaluation, "audit": audit}


_RUN_WORDS = {  # the same words as the `in words` column of ref-space-mapping.md's Workflow map
    "corpus-contract": "Set up the job", "definition-discussion": "Discuss the label meanings",
    "discovery-search": "Search outside evidence",
    "guideline-seed": "Draft a guideline candidate", "test-reserve": "Hold back test items",
    "embedding-build": "Build a map", "round-prepare": "Draw one round",
    "weak-prelabel": "Pre-label one prepared round", "human-calibration": "You label one round",
    "guideline-learn": "Draft a guideline from accepted judgments",
    "round-measure": "Measure one completed judgment set", "round-close": "Close a measured round",
    "handoff-freeze": "Freeze a stopped labeling lineage", "test-gold-lock": "Lock blind answers for the final test",
    "executor-predict": "Have one registered model predict the test",
    "executor-score": "Score one closed set of predictions",
    "executor-select": "Select from the complete scorecard set", "scan-preflight": "Check one frozen production plan",
    "scan-shard": "Label one frozen corpus shard", "risk-route": "Route risky production items to review",
    "human-review": "Review one frozen production risk queue",
    "reconcile": "Reconcile reviewed items into a candidate corpus",
    "audit-sample": "Draw from one frozen audit design", "audit-human-gold": "Blind-label one audit sample",
    "audit-analyze": "Analyze one completed audit sample", "dstar-materialize": "Publish an accepted audited corpus",
}



def _space_mapping_ref() -> Path | None:
    """skills/label-building/ref/ref-space-mapping.md, found next to the engine the Board already loads."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    plugin = Path(job_module.__file__).resolve().parents[1]
    for path in (plugin / "skills" / "label-building" / "ref" / "ref-space-mapping.md",
                 plugin / "ref" / "ref-space-mapping.md"):
        if path.is_file():
            return path
    return None


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
    mapping_text = ref.read_text(encoding="utf-8")
    headers, rows = _md_table(mapping_text, "Workflow map")
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
            f'<td data-label="{labels[-1]}" class=num>{n or ""}</td>',
        ]
        body.append(f'<tr{" class=live" if n else ""}>{"".join(tds)}</tr>')
    table = ('<div class=scroll><table class=wfmap><thead><tr>'
             + "".join(f"<th>{_esc(h)}</th>" for h in labels)
             + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>")
    prep_headers, prep_rows = _md_table(mapping_text, "Corpus Preparation Run Types")
    prep_col = {h.lower(): i for i, h in enumerate(prep_headers)}
    prep_counts: dict[str, int] = {}
    for run in (vm.get("preparation") or {}).get("runs") or []:
        prep_counts[run["operation"]] = prep_counts.get(run["operation"], 0) + 1
    prep_body = []
    for cells in prep_rows:
        operation = cells[prep_col["run type"]].strip("`")
        prep_body.append("<tr>" + "".join((
            f'<td><b>{_esc(cells[prep_col["in words"]])}</b><div class=mut><code>{_esc(operation)}</code></div></td>',
            '<td>source owner · Data → Preparation</td>',
            f'<td><code>{_esc(cells[prep_col["skill"]].strip("`"))}</code></td>',
            f'<td class=num>{prep_counts.get(operation) or ""}</td>',
        )) + "</tr>")
    prep_table = ('<div class=scroll><table class=wfmap><thead><tr>'
                  '<th>Run type</th><th>Owner and view</th><th>Skill</th><th>On this source</th>'
                  '</tr></thead><tbody>' + "".join(prep_body) + '</tbody></table></div>')
    return _card("Corpus Preparation Runs", prep_table) + _card("Workflow map", table)


def _sop_state(op: str, vm: dict, runs_by_op: dict, not_built: set) -> str:
    """Where this job is on one SOP step: done, running, not yet, or not built yet."""
    if op == "gate G0":
        return "done" if (vm.get("canonical") or {}).get("meaning_receipt_valid") else "not yet"
    if op in ("", "—"):
        return ""
    preparation = _preparation_module()
    root = vm.get("root")
    established_job = bool(vm.get("canonical")) or (root is not None and (root / "config.yaml").is_file())
    if (preparation and op in preparation.RUN_TYPES
            and not (vm.get("preparation") or {}).get("linked")
            and established_job):
        return "legacy source"
    runs = runs_by_op.get(op) or []
    running = [r for r in runs if r["status"] == "running"]
    if running:
        return "running · " + ", ".join(_run_name(r["run"]) for r in running)
    done = [r for r in runs if r["status"].startswith("complete")]
    if done:
        return "done · " + ", ".join(_run_name(r["run"]) for r in done)
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
    for r in (vm.get("runs") or []) + ((vm.get("preparation") or {}).get("runs") or []):
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
    return _card("SOP · how a labeling job runs", table)


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
        words, cls = "weak", "warn"
    return f'<p class="{cls}">groups: {_esc(words)} <span class=mut>(score {best:.2f})</span></p>'


def _wf_cell(text: str) -> str:
    """'start + shows · Embedding' with the verbs bold; '—' (nothing in this Space) is left blank."""
    text = str(text or "").strip()
    if text in {"", "—"}:
        return ""
    verbs, _, where = text.partition(" · ")
    verbs_html = " + ".join(f"<b>{_esc(v.strip())}</b>" for v in verbs.split("+"))
    return verbs_html + (f" · {_md_inline(where)}" if where else "")
_STATUS_WORDS = {"complete": "done", "running": "in progress", "failed": "failed"}


def _run_title(run: dict, build_names: dict[str, str]) -> str:
    """'Build a map: MiniLM · reply + context', 'Draw a round: round 1'; the Run id stays under it."""
    op = str(run.get("operation") or "")
    words = _RUN_WORDS.get(op, op)
    target = str(run.get("target") or "")
    if not target:
        old = re.match(r"^rl\d+_[^_]+_(.+)$", str(run.get("run") or ""))
        target = old.group(1) if old else ""
    target = target.replace("_", "-")
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
        return "you to read the label meanings and confirm them (Labeling → Definition)"
    return text


def _run_table(vm: dict) -> str:
    """Page-local and linked source-owned Runs: what ran, its state, its result."""
    runs = ((vm.get("preparation") or {}).get("runs") or []) + vm["runs"]
    if not runs:
        return ""
    builds = ((vm.get("embedding") or {}).get("builds")) or []
    build_names = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                                  for b in builds])
    rows = "".join(
        '<tr>'
        f'<td><b>{_esc(_run_title(r, build_names))}</b>'
        f'<div class=mut><code>{_esc(r["run"])}</code></div></td>'
        f'<td class="{"ok" if r["status"] == "complete" else "warn"}">{_esc(_STATUS_WORDS.get(str(r["status"]), str(r["status"])))}</td>'
        f'<td class=mut>{_esc(_outcome_words(r["outcome"]) or ("results/" + r["run"] + "/" if r.get("family") == "corpus" else ""))}</td></tr>'
        for r in runs
    )
    return ('<div class=scroll><table class=runs><thead><tr><th>What ran</th><th>State</th>'
            f'<th>Result</th></tr></thead><tbody>{rows}</tbody></table></div>')


def _drawers(vm: dict) -> dict[str, str]:
    """Workflow (Phases, SOP, map) and All runs; no button opens them, only ?drawer=workflow|allruns."""
    state, canonical = vm["state"], vm["canonical"] or {}
    capability_rows = []
    for pid, name in PHASES:
        if pid == "P0":
            status = "contract valid" if canonical.get("p0_contract_integrity_valid") else "HOLD · contract"
        elif pid == "P1":
            status = "partial · G0 passed" if canonical.get("g0_passed") else "partial · blocked by G0"
        else:
            status = ""
        capability_rows.append(_row(f"{pid} · {name}", _esc(status)))
    phases = _card("Phases", "".join(capability_rows)
                   + _row("waiting for", _esc(_blocked_words(state["first_failed"])))
                   + _row("code", f'<code>{_esc(state["first_failed"])}</code>'))
    return {"workflow": phases + _sop(vm) + _workflow_map(vm),
            "allruns": _card("All runs", _run_table(vm))}


def _run_types(vm: dict) -> dict[str, list[dict]]:
    """Each Space's built Run types and the views that list them, from the Workflow map's `view` column.

    A view shows only its own types (JL 260927). A type the map marks `not built yet` stays in the map
    only, unless this job already has a Run of it; a type with no view yet (`Scan (future)`) shows nowhere.
    """
    ref = _space_mapping_ref()
    mapping_text = ref.read_text(encoding="utf-8") if ref else ""
    headers, rows = _md_table(mapping_text, "Workflow map") if ref else ([], [])
    col = {h.lower(): i for i, h in enumerate(headers)}
    runs_by_op: dict[str, list[dict]] = {}
    for r in vm["runs"]:
        runs_by_op.setdefault(str(r["operation"]), []).append(r)
    space_ids = {name: sid for sid, name, _ in SPACES}
    view_ids = {sid: {vname: vid for vid, vname in views} for sid, _, views in SPACES}
    skills = _run_type_skills()
    out: dict[str, list[dict]] = {sid: [] for sid, _, _ in SPACES}
    for cells in rows:
        def cell(name, c=cells):
            return c[col[name]].strip() if name in col and col[name] < len(c) else ""
        op = cell("run type").strip("`")
        space_name, _, view_names = cell("view").partition(" · ")
        sid = space_ids.get(space_name.strip())
        views = [view_ids[sid][v.strip()] for v in view_names.split(",") if sid and v.strip() in view_ids[sid]]
        if not op or not views or (cell("started by") == "not built yet" and op not in runs_by_op):
            continue
        out[sid].append({"op": op, "words": cell("in words") or _RUN_WORDS.get(op, op),
                         "views": views, "runs": runs_by_op.get(op, []),
                         "skills": skills.get(op, []), "built": cell("started by") != "not built yet",
                         "step": int(cell("step")) if cell("step").isdigit() else 99})
    prep_runs: dict[str, list[dict]] = {}
    for run in (vm.get("preparation") or {}).get("runs") or []:
        prep_runs.setdefault(run["operation"], []).append(run)
    prep_headers, prep_rows = _md_table(mapping_text, "Corpus Preparation Run Types") if ref else ([], [])
    prep_col = {h.lower(): i for i, h in enumerate(prep_headers)}
    for cells in prep_rows:
        if (vm["root"] / "config.yaml").is_file() and not (vm.get("preparation") or {}).get("attached"):
            continue  # an existing legacy job cannot acquire retrospective source-owned Runs
        op = cells[prep_col["run type"]].strip("`")
        words = cells[prep_col["in words"]]
        skill = cells[prep_col["skill"]].strip("`")
        step = int(cells[prep_col["step"]])
        out["data"].append({"op": op, "words": words, "views": ["preparation"],
                            "runs": prep_runs.get(op, []), "family": "corpus",
                            "skills": [skill], "built": True, "step": step - 100})
    for types in out.values():
        types.sort(key=lambda t: t["step"])
    return out


def _run_type_skills() -> dict[str, list[str]]:
    """Run Type -> declared Skills from ref-space-mapping.md; these do not prove historical usage."""
    ref = _space_mapping_ref()
    headers, rows = _md_table(ref.read_text(encoding="utf-8"), "Run Type skills") if ref else ([], [])
    col = {h.lower(): i for i, h in enumerate(headers)}
    if "run type" not in col or "declared skills" not in col:
        return {}
    out: dict[str, list[str]] = {}
    for cells in rows:
        if max(col["run type"], col["declared skills"]) >= len(cells):
            continue
        op = cells[col["run type"]].strip().strip("`")
        if op:
            out[op] = re.findall(r"`([^`]+)`", cells[col["declared skills"]])
    return out


def _run_name(run_id: str) -> str:
    """Keep new full names verbatim; expand old Labeling addresses for display."""
    if run_id.startswith("run-"):
        return run_id
    return "run-labeling-" + re.sub(r"^rl\d+_", "", run_id).replace("_", "-")


def _run_ask(vm: dict, run: dict) -> str:
    """The Run's prompt: what it did and where its Ticket and Result are."""
    if run.get("family") == "corpus":
        return (f"Review Corpus Preparation Run {run['run']} at {run['owner']}. "
                f"Ticket: runs/{run['run']}.yaml · Result: results/{run['run']}/")
    words = _RUN_WORDS.get(run["operation"], run["operation"])
    return (f"{words}{' · ' + run['target'] if run.get('target') else ''} on the labeling job at {_job_where(vm)}. "
            f"Run {run['run']} · Ticket: runs/{run['run']}.yaml · Result: results/{run['run']}/")


def _run_again(vm: dict, run: dict, *, built: bool = True) -> tuple[str, str]:
    """Resume an open Run or Rerun a closed one; both only copy a prompt."""
    if not built:
        return "", ""  # historical Ticket remains readable; this build has no worker
    if run.get("family") != "corpus" and _g0_retroactive_block(vm):
        return "", ""  # a released round without earlier confirmation is history
    if run["operation"] == "corpus-contract" and run.get("family") != "corpus":
        return "", ""  # the Page's Contract is already bound to this job
    if run.get("family") == "corpus":
        prep = vm.get("preparation") or {}
        if (not vm.get("page_ready", True) or prep.get("error") or prep.get("linked")
                or (vm["root"] / "config.yaml").is_file()):
            return "", ""
        action = "Resume" if run["status"] == "running" else "Rerun"
        return action, (f"{action} the {run['operation']} Corpus Preparation Run for {run['target']} "
                        f"at {run['owner']} through /subjective-label-preparation. "
                        + (f"Keep Ticket {run['run']}." if action == "Resume" else
                           f"Reuse {run['run']} for identical accepted inputs, or allocate a new full run-corpus name for changed inputs."))
    where = _job_where(vm)
    if run["operation"] == "definition-discussion":
        if not _meaning_allowed(vm):
            return "", ""
        active = _open_definition_run(vm)
        if active:
            return (("Resume", _meaning_prompt(vm, run["run"]))
                    if active["run"] == run["run"] else ("", ""))
        return "Rerun", _meaning_prompt(vm)
    if run["operation"] == "human-calibration":
        cal = vm.get("cal") or {}
        current = cal.get("current_round") or {}
        round_id = current.get("round_id") or ""
        if (run["status"] == "running" and current.get("open_item")
                and run.get("target") == round_id.replace("_", "-")
                and not (vm.get("canonical") or {}).get("hold")):
            return "Resume", _chat_prompt(vm, current, _round_draw(vm["root"], round_id), run=run)
        judged = next((r for r in cal.get("rounds") or []
                       if r.get("round_id", "").replace("_", "-") == run.get("target")
                       and r.get("state") == "judged" and r.get("calibration_status") == "running"), None)
        if run["status"] == "running" and judged and not (vm.get("canonical") or {}).get("hold"):
            config = vm.get("config") or {}
            authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
            command = _engine_command("calibration.py", "finalize", "--job-root", where,
                                      "--round", judged["round_id"], "--human-id",
                                      (authority or {}).get("human_id") or "<configured-human-id>")
            return "Resume", (f"Finish the interrupted {run['run']} Result. All items in "
                              f"{judged['round_id']} have final events, but its runtime is still running. "
                              f"Verify the event log, then run: {command}. Do not repeat a judgment.")
        return "", ""  # a stale or finished batch cannot be resumed or rerun
    if run["operation"] in {"round-prepare", "embedding-build"}:
        return "", ""  # these start through checked view actions, not a generic prompt
    if run["status"] == "running":
        return "Resume", (f"Resume Run {run['run']} on the labeling job at {where} through /subjective-label. "
                          "Keep the same Ticket and Result name.")
    return "Rerun", (f"Start a new {run['operation']} Run{' for target ' + run['target'] if run.get('target') else ''} on the labeling job "
                     f"at {where} through /subjective-label. Give it a new full run-labeling name; {run['run']} stays as it is.")


def _skills_line(skills: list[str]) -> str:
    if not skills:
        return ""
    names = " · ".join(f"<code>{_esc(skill)}</code>" for skill in skills)
    return f'<p class=run-skill>Run Type skills {names}</p>'


def _run_card(vm: dict, run: dict, skills: list[str] | None = None, *, built: bool = True) -> str:
    action, again = _run_again(vm, run, built=built)
    ask = again or _run_ask(vm, run)
    status = str(run["status"])
    blocked_g0 = run.get("family") != "corpus" and _g0_retroactive_block(vm)
    blocked_discussion = (run["operation"] == "definition-discussion" and status == "running"
                          and not _meaning_allowed(vm))
    blocked_history = status == "running" and (blocked_discussion or blocked_g0)
    words = "blocked history" if blocked_history else _STATUS_WORDS.get(status, status)
    times = " → ".join(x for x in (_when(run.get("started_at")), _when(run.get("finished_at"))) if x)
    process = " · ".join(x for x in (times, _outcome_words(run.get("outcome"))) if x)
    files = "".join(f"<li><code>{_esc(p)}</code></li>" for p in run.get("artifacts") or [])
    legacy = (f'<p class=run-skill>Legacy Ticket on disk <code>{_esc(run["run"])}</code></p>'
              if run["name"] != run["run"] else "")
    action_button = (f'<button type=button class=run-copy data-copy="{_esc(again)}">{action}</button>'
                     if again else "")
    blocked_note = ('<p class=warn>This discussion cannot continue after round release. '
                    'Its earlier turns remain on disk.</p>'
                    if blocked_discussion else
                    '<p class=warn>This Run cannot continue: G0 cannot authorize the released round. '
                    'Its Ticket and Result remain on disk.</p>' if blocked_g0 else "")
    review_only = not built or bool(blocked_note) or not again
    prompt_header = ('<details class=run-prompt-box><summary>Record</summary>' if review_only else
                     '<details class=run-prompt-box><summary>Prompt '
                     f'<button type=button class=run-copy data-copy="{_esc(ask)}">Copy</button></summary>')
    return (
        f'<article class=run-card data-op="{_esc(run["operation"])}" data-run="{_esc(run["run"])}" '
        f'data-name="{_esc(run["label"])}" data-target="{_esc(run.get("target") or "")}" hidden>'
        f'<header><b title="{_esc(run["run"])}">{_esc(run["name"])}</b>'
        f'<span class="run-state st-{_esc("blocked" if blocked_history else status.split(" ")[0])}">{_esc(words)}</span>'
        f'{action_button}</header>{blocked_note}'
        f'{_skills_line(skills or [])}{legacy}'
        f'{prompt_header}'
        f'<pre class=run-prompt>{_esc(ask)}</pre></details>'
        f'<h4>Running process</h4><div class=run-process>{_esc(process)}</div>'
        f'<h4>Results</h4><div class=run-results><code>{_esc(run.get("owner") + "/" if run.get("family") == "corpus" else "")}results/{_esc(run["run"])}/</code>'
        f'{f"<ul>{files}</ul>" if files else ""}</div>'
        '</article>'
    )


_CORPUS_ORDER = ("source-normalize", "unit-recipe", "unit-materialize",
                 "unit-check", "initial-group-reserve")


def _next_preparation_operation(vm: dict) -> str | None:
    prep = vm.get("preparation") or {}
    if (not vm.get("page_ready", True) or not prep.get("attached") or prep.get("linked")
            or prep.get("error") or (vm["root"] / "config.yaml").is_file()):
        return None
    completed = {r.get("operation") for r in prep.get("runs") or [] if r.get("status") == "complete"}
    return next((op for op in _CORPUS_ORDER if op not in completed), None)


def _runs_panel(vm: dict, sid: str, types: list[dict]) -> str:
    """One Space's Runs panel, on the right: the current view's Run types, then the selected Run."""
    where = _job_where(vm)
    buttons, cards = [], []
    for t in types:
        runs = list(reversed(t["runs"]))  # newest first
        waiting = sum(1 for r in runs if r["status"] == "running" and r.get("worker_kind") == "human")
        if t.get("family") == "corpus":
            prep = vm.get("preparation") or {}
            owner = (prep.get("reference") or prep.get("owner_reference") or {}).get("owner")
            prompt = (f"Start the next {t['op']} Corpus Preparation Run for the Page at {where} "
                      f"through /subjective-label-preparation. "
                      + (f"Source owner: {owner}. " if owner else
                         "First attach the source preparation owner to this Page. ")
                      + "Record a full run-corpus Ticket and Result.")
            if t["op"] != _next_preparation_operation(vm):
                prompt = ""
        elif t["op"] == "corpus-contract":
            prep = vm.get("preparation") or {}
            if (prep.get("linked") and not prep.get("error")
                    and not (vm["root"] / "config.yaml").is_file()):
                package = (prep.get("reference") or {}).get("package") or ""
                prompt = (f"Use /subjective-label to create the Labeling Contract for the Page "
                          f"in {vm['root'].parent} from the accepted Corpus Preparation package "
                          f"at {package}. Labeling folder: {where}. Confirm the target trait, "
                          "job ID, identified semantic human, and sealed-test custodian; "
                          "validate the package and custody boundary before writing one "
                          "run-labeling-corpus-contract Ticket and Result. Do not show protected IDs.")
            else:
                prompt = ""
        elif t["op"] == "definition-discussion":
            prompt = _meaning_prompt(vm) if _meaning_allowed(vm) and not _open_definition_run(vm) else ""
        elif t["op"] == "human-calibration":
            current = (vm.get("cal") or {}).get("current_round") or {}
            prompt = (_chat_prompt(vm, current, _round_draw(vm["root"], current["round_id"]))
                      if current.get("round_id") and current.get("open_item")
                      and not current.get("calibration_run")
                      and not (vm.get("canonical") or {}).get("hold") else "")
        else:
            prompt = ""  # embedding-build and round-prepare start through checked view actions
        buttons.append(
            f'<button type=button class=run-type data-op="{_esc(t["op"])}" data-views="{_esc(" ".join(t["views"]))}" '
            f'data-waiting="{waiting}" data-prompt="{_esc(prompt)}" data-skills="{_esc("|".join(t.get("skills") or []))}" '
            f'title="{_esc(t["op"])}">'
            f'{_esc(t["words"])} <span class=run-count>{len(runs)}</span></button>')
        cards.extend(_run_card(vm, r, t.get("skills") or [], built=t.get("built", True)) for r in runs)
    return (
        f'<section class=runs-panel data-space={sid}>'
        '<div class=runs-bar><button type=button class=runs-fold title="Fold or open">▸</button><b>Runs</b></div>'
        f'<div class=runs-body><div class=runs-types>{"".join(buttons)}'
        '<button type=button class="run-type run-new">+ New Run</button></div>'
        f'<div class=runs-detail><div class=run-list hidden></div>{"".join(cards)}'
        '<article class="run-card run-card-new" hidden><header><b>New run</b></header>'
        '<p class=run-skill hidden></p><details class=run-prompt-box open><summary>Prompt '
        '<button type=button class=run-copy data-copy="">Copy</button></summary>'
        '<pre class=run-prompt></pre></details></article>'
        '<div class=run-empty hidden>No runs yet.</div></div></div></section>'
    )


def _delivery_space(vm: dict) -> dict[str, str]:
    state = vm["state"]
    handoff = (_card("Label handoff", _row("status", _esc(state["handoff_status"] or "present")))
               if state["handoff"].is_file() else _later("P2 Freeze"))
    final = (_card("Final labels", _row("D*", "materialized"))
             if state["dstar"].is_file() else _later("P5 Audit"))
    runs = sorted((vm["root"] / "production").glob("run_*")) if (vm["root"] / "production").is_dir() else []
    scan = _card("Scan", _row("production runs", _esc(len(runs)))) if runs else _later("P4 Scan")
    return {"handoff": handoff, "scan": scan, "final": final}


def _script_json(value) -> str:
    return (json.dumps(value, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def render(page_src: Path, path_q: str, file_q: str, page_q: str,
           board_dir: Path | None, *, standalone: bool = False) -> str:
    vm = _view_model(page_src)
    state, canonical, config = vm["state"], vm["canonical"], vm["config"]
    if not standalone and not generated_page_url(path_q, file_q, page_q, board_dir):
        raise ValueError("Labeling Workbench requires the matching generated Page URL")
    hold = bool(state["authority_hold"] or state["next_action"].startswith("HOLD"))
    next_line, next_space = _next_step(vm)
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    title = construct.get("question") or construct.get("name") or page_src.stem

    panels = {
        "data": _data_space(vm), "labeling": _labeling_space(vm),
        "quality": _quality_space(vm), "delivery": _delivery_space(vm),
    }
    types = _run_types(vm)
    drawers = _drawers(vm)
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
            f'<div class=space-split><div class=space-main><div class=views role=group>{chips}</div>{panes}</div>'
            f'{_runs_panel(vm, sid, types[sid])}</div></section>'
        )

    cal = vm["cal"] or {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    boot = {
        "mode": "page" if standalone else "board",
        "path": path_q, "file": file_q, "page": page_q,
        "identity": f"{path_q}|{file_q}",
        "human_id": authority.get("human_id") or "",
        "hold": hold,
        "next": next_line,
        "phase": canonical.get("phase") if canonical else None,
        "g0_open": bool(canonical and (canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation"
                                       or canonical.get("first_blocked_frontier") == "G0 · label meanings missing"
                                       or canonical.get("g0_retroactive_block") or _g0_repair_request(vm))),
        "g0_retroactive_block": _g0_retroactive_block(vm),
        "g0_repair_request": _g0_repair_request(vm),
        "missing_meanings": canonical.get("meaning_definitions_missing") or [],
        "definition_open": bool(_open_definition_run(vm) and _meaning_allowed(vm)),
        "default_space": next_space,
        "question": construct.get("question") or construct.get("name") or "",
        "schema": cal.get("schema") or {},
        "rounds": cal.get("rounds") or [],
        "current_round": cal.get("current_round"),
        "batch_default": ((config.get("rounds") or {}).get("round1") or {}).get("human_batch_size") or 20,
        "spaces": {sid: [vid for vid, _ in views] for sid, _, views in SPACES},
    }
    back_link = ('' if standalone else
                 f'<a class=back href="/_board/labeling-board?path={_esc(quote(path_q))}" title="All labeling jobs">←</a>')
    document = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Labeling · {_esc(page_src.stem)}</title><style>{_CSS}</style></head><body>'
        f'<h1 class=pagetitle title="{_esc(next_line)}">'
        f'{back_link}'
        f' 🏷 {_esc(title)}</h1>'
        f'<section class=drawer data-drawer-panel=workflow hidden>{drawers["workflow"]}</section>'
        f'<section class=drawer data-drawer-panel=allruns hidden>{drawers["allruns"]}</section>'
        f'<nav class=spaces role=tablist aria-label="Labeling Spaces">{space_buttons}</nav>'
        + "".join(sections) +
        f'<script type=application/json id=labeling-boot>{_script_json(boot)}</script>'
        f'<script>{_JS}</script></body></html>'
    )
    from live.workbench_guide import mount_guide
    return mount_guide(document, "labeling", {"path": path_q, "file": file_q},
                       "nav.spaces", "section.panel")


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
details.roundbox.on{border-color:var(--acc)}
.run-skill{margin:6px 0 0;color:var(--mut);font-size:12px}.run-skill code{font-size:11.5px;color:var(--fg)}
.discrec td.changed{color:var(--ok)}
h3.sub{font-size:13px;margin:12px 0 2px}
table.items{width:auto;max-width:100%}
table.map{width:auto;border-collapse:collapse}
table.map td{padding:1px 10px 1px 0;border:0;background:none}
table.items td,table.items th{padding:3px 10px}
table.items td:not(:nth-child(3)):not(:nth-child(6)){white-space:nowrap}
table.items td.num{text-align:left}
table.items td:nth-child(3)>*{max-width:30em}
table.items td:nth-child(6)>*{max-width:18em}
table.items .pill{font-size:10px}
table.items td.nowrap{white-space:nowrap}
table.items .reply{font-weight:500}
table.items.itemtable td:nth-child(3),table.items.itemtable td:nth-child(4){white-space:normal}
table.items.itemtable td:nth-child(3)>*{max-width:26em}
table.items.itemtable td:nth-child(4)>*{max-width:40em}
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
.discquestion{font-size:20px;line-height:1.3;margin:9px 0 5px;max-width:42em}
.flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin:8px 0 4px}
.flowstep{display:flex;flex-direction:column;gap:2px;border:1px solid var(--line);border-radius:8px;padding:8px 9px;background:var(--card);min-height:86px}
.flowstep b{font:700 11px ui-monospace,Menlo,monospace;color:var(--mut)}
.flowstep strong{font-size:13px;line-height:1.3}.flowstep span{font-size:12px;line-height:1.35;color:var(--mut)}
.flowstep.now{border-color:var(--acc);background:color-mix(in srgb,var(--acc) 7%,var(--card))}
.flowstep.now b,.flowstep.now strong{color:var(--acc)}
/* conversation turns, option rows, chips */
table.sop tr.now td{background:var(--soft)} table.sop tr.now td:last-child{color:var(--acc);font-weight:600}
table.sop tr.done td:last-child{color:var(--ok)}
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
 .discquestion{font-size:18px}.flow{grid-template-columns:1fr}.flowstep{min-height:0}
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


_CSS += """/* v3 (JL 260927, as the Page workbench): no page bar; each Space is its content on the left and its
   Runs panel on the right at every width. The panel stays in view while the page scrolls; folded, it
   is a thin strip. A view lists only its own Run types. */
.pagetitle{display:flex;align-items:center;gap:8px;margin:0 0 6px}
.pagetitle .back{text-decoration:none;font-weight:700}
.drawer{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:8px 0 0;background:var(--card)}
.space-split{display:flex;align-items:flex-start;gap:16px}
.space-main{flex:1 1 auto;min-width:0}
.runs-panel{flex:0 0 clamp(260px,30vw,600px);position:sticky;top:8px;max-height:calc(100vh - 16px);
 display:flex;flex-direction:column;overflow:hidden;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.runs-panel button{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 9px;cursor:pointer;background:var(--card);color:var(--fg)}
.runs-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;font:13px/1.4 system-ui,sans-serif}
.runs-bar .runs-fold{padding:0 7px}
.runs-body{overflow:auto;min-height:0;display:flex;flex-direction:column;gap:10px;padding:0 12px 12px}
.runs-types{display:flex;flex-wrap:wrap;gap:6px}
.run-type{display:flex;gap:8px;align-items:center}
.run-type.on{border-color:var(--acc)!important;color:var(--acc)!important}
.run-type .run-count{color:var(--mut);font-weight:500}
.run-new{border-style:dashed!important}
.runs-detail{border:1px solid var(--line);border-radius:9px;padding:10px 12px;min-width:0}
.run-list{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:4px;margin-bottom:8px;padding-bottom:2px}
.run-list button{flex:none;font:500 11px ui-monospace,Menlo,monospace!important;padding:1px 6px!important}
.run-list button.on{border-color:var(--acc);color:var(--acc)}
.run-card header{display:flex;align-items:center;gap:8px}
.run-card header b{font-size:13px;overflow-wrap:anywhere}
.run-card header .run-copy{margin-left:auto}
.run-prompt-box{margin:0}
.run-prompt-box>summary{display:flex;align-items:center;gap:6px;margin:10px 0 4px;padding:0;cursor:pointer;list-style:none;
 font:600 12px system-ui,sans-serif;text-transform:none;letter-spacing:normal;color:var(--fg)}
.run-prompt-box>summary::-webkit-details-marker{display:none}
.run-prompt-box>summary:before{content:"▸";color:var(--acc);width:10px}
.run-prompt-box[open]>summary:before{content:"▾"}
.run-prompt-box>summary .run-copy{margin-left:auto}
.run-card h4{margin:10px 0 4px;font:600 12px system-ui,sans-serif}
.run-process{color:var(--mut);font-size:12px;line-height:1.5;overflow-wrap:anywhere}
.run-prompt{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:7px 9px;border-radius:7px;max-height:40vh;overflow:auto;
 background:var(--soft);font:12px/1.5 ui-monospace,Menlo,monospace}
.run-results{font-size:12px;overflow-wrap:anywhere}.run-results ul{margin:4px 0 0;padding-left:18px}
.run-state{font:600 10.5px/1.4 system-ui,sans-serif;border-radius:5px;padding:1px 6px;border:1px solid var(--line);color:var(--mut)}
.run-state.st-running{color:var(--ok);border-color:var(--ok)}
.run-state.st-blocked{color:var(--warn);border-color:var(--warn)}
.run-state.st-failed{color:var(--warn);border-color:var(--warn)}
.run-empty{color:var(--mut);font-size:12px}
.runs-panel.folded{flex-basis:42px;cursor:pointer}
.runs-panel.folded .runs-body{display:none}
.runs-panel.folded .runs-bar{writing-mode:vertical-rl;padding:10px 9px;gap:10px}
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
 runsFor(space,view);
 if(remember){try{localStorage.setItem(key,JSON.stringify({space:space,view:view}));}catch(e){}
  try{var u=new URL(location.href);u.searchParams.set('space',space);u.searchParams.set('view',view);history.replaceState(null,'',u.toString());}catch(e){}}
 current={space:space,view:view};
}
var current={};
$$('.space').forEach(function(b){b.addEventListener('click',function(){select(b.dataset.space,null,true);});
 b.addEventListener('keydown',function(e){var ids=Object.keys(spaces),i=ids.indexOf(b.dataset.space);
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();var n=ids[(i+(e.key==='ArrowRight'?1:ids.length-1))%ids.length];select(n,null,true);$('#tab-'+n).focus();}});});
$$('.chip').forEach(function(c){c.addEventListener('click',function(){select(c.dataset.space,c.dataset.view,true);});});
/* ── Runs panel, right of each Space: a view lists only its own Run types; pick a type, then a run ── */
function runsRender(p){
 var on=$('.run-type.on',p),newMode=on&&on.classList.contains('run-new'),list=$('.run-list',p),empty=$('.run-empty',p);
 var source=newMode?$('.run-type[data-op="'+p.dataset.lastOp+'"]',p):on;
 $('.run-new',p).hidden=!source||!source.dataset.prompt;
 $$('.run-card',p).forEach(function(c){c.hidden=true;});list.innerHTML='';list.hidden=true;empty.hidden=true;
 var op=newMode?p.dataset.lastOp:(on?on.dataset.op:'');
 if(newMode){var src=$('.run-type[data-op="'+op+'"]',p),card=$('.run-card-new',p),text=src?src.dataset.prompt:'';
  $('.run-prompt',card).textContent=text;$('.run-copy',card).dataset.copy=text;
  var sk=$('.run-skill',card),skills=src&&src.dataset.skills?src.dataset.skills.split('|'):[];
  sk.innerHTML=skills.length?'Run Type skills '+skills.map(function(skill){return '<code>'+esc(skill)+'</code>';}).join(' · '):'';
  sk.hidden=!skills.length;
  card.hidden=false;return;}
 p.dataset.lastOp=op||'';
 var cards=op?$$('.run-card[data-op="'+op+'"]',p):[];
 if(!cards.length){var pendingSkills=on&&on.dataset.skills?on.dataset.skills.split('|'):[];
  empty.innerHTML='No runs yet.'+(pendingSkills.length?'<p class=run-skill>Run Type skills '+
   pendingSkills.map(function(skill){return '<code>'+esc(skill)+'</code>';}).join(' · ')+'</p>':'');
  empty.hidden=false;return;}
 var first=cards.filter(function(c){return c.dataset.target&&c.dataset.target===p.dataset.want;})[0]||cards[0];
 function show(c){cards.forEach(function(x){x.hidden=x!==c;});}
 cards.forEach(function(c){var b=document.createElement('button');b.type='button';b.textContent=c.dataset.name;b.title=c.dataset.run;
  b.addEventListener('click',function(){show(c);$$('button',list).forEach(function(x){x.classList.toggle('on',x===b);});
   p.dataset.want=c.dataset.target||'';
   document.dispatchEvent(new CustomEvent('labeling:run',{detail:{space:p.dataset.space,op:c.dataset.op,target:c.dataset.target||''}}));});
  if(c===first){b.classList.add('on');}list.appendChild(b);});
 list.hidden=cards.length<2;show(first);}
/* the content picks its run: a build or a round selects the matching run in the panel (as the Page's Card ↔ Runs) */
function runsWant(space,target){var p=$('.runs-panel[data-space="'+space+'"]');if(!p||!target){return;}
 var shown=$$('.run-card[data-op]',p).filter(function(c){return !c.hidden;})[0];
 p.dataset.want=target;if(shown&&shown.dataset.target===target){return;}
 function has(b){return b&&!b.hidden&&b.dataset.op&&$$('.run-card[data-op="'+b.dataset.op+'"]',p).some(function(c){return c.dataset.target===target;});}
 var on=$('.run-type.on',p);
 if(on&&!on.classList.contains('run-new')&&!has(on)){var alt=$$('.run-type[data-op]',p).filter(has)[0];
  if(alt){$$('.run-type',p).forEach(function(x){x.classList.toggle('on',x===alt);});}}
 if($('.run-type.on',p)){runsRender(p);}}
function runsFor(space,view){var p=$('.runs-panel[data-space="'+space+'"]');if(!p){return;}
 var best=null;
 $$('.run-type[data-op]',p).forEach(function(b){b.hidden=(b.dataset.views||'').split(' ').indexOf(view)<0;
  if(!b.hidden&&(!best||+b.dataset.waiting>+best.dataset.waiting)){best=b;}});
 $('.run-new',p).hidden=!best||!best.dataset.prompt;
 $$('.run-type',p).forEach(function(b){b.classList.toggle('on',b===best);});
 runsRender(p);}
$$('.runs-panel').forEach(function(p){
 $$('.run-type',p).forEach(function(b){b.addEventListener('click',function(){
  $$('.run-type',p).forEach(function(x){x.classList.toggle('on',x===b);});runsRender(p);
  var c=$$('.run-card[data-op]',p).filter(function(x){return !x.hidden;})[0];
  if(c&&c.dataset.target){document.dispatchEvent(new CustomEvent('labeling:run',{detail:{space:p.dataset.space,op:c.dataset.op,target:c.dataset.target}}));}});});
 var fold=$('.runs-fold',p),foldKey='labeling-runs-fold:'+p.dataset.space;
 function setFold(on,remember){p.classList.toggle('folded',on);fold.textContent=on?'◂':'▸';
  if(remember){try{localStorage.setItem(foldKey,on?'1':'0');}catch(e){}}}
 fold.addEventListener('click',function(ev){ev.stopPropagation();setFold(!p.classList.contains('folded'),true);});
 $('.runs-bar',p).addEventListener('click',function(){if(p.classList.contains('folded')){setFold(false,true);}});
 try{if(localStorage.getItem(foldKey)==='1'){setFold(true,false);}}catch(e){}});
function roundLight(target){$$('details.roundbox').forEach(function(d){d.classList.toggle('on',d.dataset.target===target);});}
$$('details.roundbox').forEach(function(d){d.addEventListener('toggle',function(){
 if(d.open){roundLight(d.dataset.target);runsWant('labeling',d.dataset.target);}});});
document.addEventListener('labeling:run',function(e){var d=$$('details.roundbox').filter(function(x){return x.dataset.target===e.detail.target;})[0];
 if(!d){return;}d.open=true;roundLight(d.dataset.target);if(d.getBoundingClientRect().top>innerHeight||d.getBoundingClientRect().bottom<0){d.scrollIntoView({block:'start'});}});
document.addEventListener('labeling:run',function(e){if(e.detail.op!=='definition-discussion'){return;}
 var recs=$$('.discrec');if(!recs.some(function(r){return r.dataset.target===e.detail.target;})){return;}
 recs.forEach(function(r){r.hidden=r.dataset.target!==e.detail.target;});});
/* a Copy inside a folded Prompt summary copies without opening it */
document.addEventListener('click',function(ev){if(ev.target.closest&&ev.target.closest('summary [data-copy]')){ev.preventDefault();}},true);
/* Workflow (Phases, SOP, map) and All runs open only from ?drawer=workflow|allruns; Esc closes */
(function(){var d=null;try{d=new URLSearchParams(location.search).get('drawer');}catch(e){}
 $$('[data-drawer-panel]').forEach(function(x){x.hidden=x.dataset.drawerPanel!==d;});})();
document.addEventListener('keydown',function(e){if(e.key==='Escape'){$$('[data-drawer-panel]').forEach(function(x){x.hidden=true;});}});
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
    if(offset===0&&r.hidden_waiting){list.insertAdjacentHTML('beforeend','<p class=mut>hidden, waiting in '+esc(r.hidden_rounds.map(roundWords).join(', '))+': '+r.hidden_waiting+'</p>');}
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
      ?'<p class=mut>waits in '+esc(roundWords(data.marks[r.item_id].round))+'</p>'
      :'<button class="pill tog" type=button data-pick-show>Show its text</button>')+'</div>';
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
  runsWant('data',v);
  if(remember){try{var u=new URL(location.href);u.searchParams.set('emb',v);history.replaceState(null,'',u.toString());}catch(e){}}
 }
 var want=null;try{want=new URLSearchParams(location.search).get('emb');}catch(e){}
 showEmb(want,false);
 $$('[data-emb-show]').forEach(function(b){b.addEventListener('click',function(){showEmb(b.dataset.embShow,true);
  if(!b.classList.contains('tog')){var d=b.closest('details');if(d){d.open=false;}var pane=$('.embpane:not([hidden])');if(pane){pane.scrollIntoView({block:'start'});}}});});
 document.addEventListener('labeling:run',function(e){if(e.detail.op==='embedding-build'){showEmb(e.detail.target,true);}});
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
 var payload=Object.assign({mode:boot.mode,path:boot.path,file:boot.file,page:boot.page,action:action,
  human_id:boot.human_id,session_id:sessionId},body||{});
 if(action!=='confirm_meaning')payload.attest=true;
 return fetch('/_board/labeling/act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
  .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok){throw new Error(j.err||('HTTP '+r.status));}return j;});});
}
/* ── Data → Preparation: items to label, a page at a time (each page is an exposure) ── */
(function(){var btn=$('[data-items-show]');if(!btn){return;}
 var box=$('[data-items-box]'),rows=$('[data-items-rows]'),more=$('[data-items-more]'),offset=0,k=20;
 function turns(c){return String(c||'').split('\n').filter(function(l){return l.trim();}).map(function(l){
  var m=l.match(/^([A-Za-z][A-Za-z_ ]{0,20}):\s?(.*)$/),who=m?m[1]:'',body=m?m[2]:l;
  if(/^(lamda|assistant|bot|chatbot|ai|model|gpt|claude)$/i.test(who.trim())){who='AI';}
  return '<div class=turn>'+(who?'<b>'+esc(who)+'</b>':'')+'<span>'+esc(body)+'</span></div>';}).join('');}
 function nTurns(c){return String(c||'').split('\n').filter(function(l){return l.trim();}).length;}
 function row(it){var waiting=/^waiting in /.test(it.state);
  var state=waiting?it.state.replace(/^waiting in (\S+)$/,function(_,r){return 'in '+roundWords(r)+', open it in Labeling › Rounds';}):
   it.state.replace(/^labeled in (\S+)$/,function(_,r){return 'labeled in '+roundWords(r);});
  return '<tr><td class=nowrap>item '+esc(it.item_id)+'</td><td><span class="pill'+(it.state==='to label'?'':' mut')+'">'+esc(state)+'</span></td>'+
   '<td>'+(waiting||!it.context?'':'<details class=ctx><summary>'+nTurns(it.context)+' turn'+(nTurns(it.context)===1?'':'s')+'</summary><div class=convo>'+turns(it.context)+'</div></details>')+'</td>'+
   '<td>'+(waiting?'':'<div class=reply>'+esc(it.text)+'</div>')+'</td></tr>';}
 function load(){btn.disabled=true;var m=$('button',more);if(m){m.disabled=true;m.textContent='Loading…';}
  act('item_page',{offset:offset,k:k}).then(function(j){var r=j.result;box.hidden=false;btn.hidden=true;
   rows.insertAdjacentHTML('beforeend',r.items.map(row).join(''));offset+=r.items.length;
   more.innerHTML=r.more?'<button type=button class="pill tog">Show '+Math.min(k,r.total-offset)+' more ('+offset+' of '+r.total+' shown)</button>':
    '<p class=mut>All '+r.total+' items shown.</p>';
   var b=$('button',more);if(b){b.addEventListener('click',load);}})
  .catch(function(e){btn.disabled=false;more.innerHTML='<p class=warn>'+esc(e.message)+'</p>';});}
 btn.addEventListener('click',load);})();
/* ── G0: confirm meaning ─────────────────────────────────── */
var attest=$('[data-confirm-attest]'),confirmBtn=$('[data-confirm-meaning]'),confirmMsg=$('[data-confirm-msg]');
if(attest&&confirmBtn){attest.addEventListener('change',function(){confirmBtn.disabled=!attest.checked;});
 confirmBtn.addEventListener('click',function(){
  var ask=boot.g0_repair_request?
   'This restores the missing G0 receipt from the earlier human confirmation. The Workbench does not verify your identity. Continue?':
   'This records your caller attestation as '+boot.human_id+'. The Workbench does not verify your identity. Continue?';
  if(!window.confirm(ask))return;
  confirmBtn.disabled=true;confirmMsg.textContent='Saving…';confirmMsg.className='msg';
  act('confirm_meaning',{attest:true}).then(function(){confirmMsg.textContent=boot.g0_repair_request?'G0 receipt restored. Opening the round…':'Confirmed. Opening round 1…';
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
 copyText(b.dataset.copy).then(function(){toast('Copied');},function(){toast('Copy failed. Check clipboard access and try again.',true);});});
var app=$('#label-app');
var AI_NAMES=/^(lamda|assistant|bot|chatbot|ai|model|system|gpt|chatgpt|claude|bard|gemini|agent)$/i;
function who(tag){return AI_NAMES.test(String(tag||'').trim())?'AI':String(tag||'');}
function roundWords(id){var m=String(id||'').match(/^round_0*(\d+)$/);return m?'round '+m[1]:String(id||'');}
function message(html){app.innerHTML='<div class=card>'+html+'</div>';}
function load(){
 if(!app){return;}
 if(boot.hold){message('<p class=warn>Read-only · '+esc(boot.next||'')+'</p>');return;}
 if(boot.phase!=='P1'){
  if(boot.g0_open){
   if(boot.g0_retroactive_block){message('<p>A round was released without valid prior meaning confirmation. Keep this job as history; start a new job for new labels.</p>');}
   else if(boot.g0_repair_request){message('<p>Restore the missing G0 receipt from the earlier human confirmation.</p><div class=actions><button class=primary type=button id=go-confirm>Go to Definition</button></div>');
    $('#go-confirm').addEventListener('click',function(){select('labeling','definition',true);});}
   else if(boot.missing_meanings.length){message('<p>Define every label meaning in a Definition discussion before confirming G0.</p><div class=actions><button class=primary type=button id=go-confirm>Go to Definition</button></div>');
    $('#go-confirm').addEventListener('click',function(){select('labeling','definition',true);});}
   else{message('<p><b>Step 1 first:</b> '+(boot.definition_open?'finish the open label-meaning discussion.':'review or discuss the label meanings, then confirm them.')+'</p><div class=actions><button class=primary type=button id=go-confirm>Go to Definition</button></div>');
    $('#go-confirm').addEventListener('click',function(){select('labeling','definition',true);});}}
  else{message('<p class=mut>Labeling opens after P0 Contract passes.</p>');}
  return;}
 var cur=boot.current_round, rounds=boot.rounds||[];
 if(boot.definition_open){message('<p>Finish the open label-meaning discussion before releasing a round.</p>');return;}
 if(!cur&&rounds.length&&rounds[rounds.length-1].state==='judged'){
  var r=rounds[rounds.length-1];message('<p class=ok>'+esc(r.round_id)+' is done: '+r.finals+' of '+r.batch_size+' labeled.</p>');return;}
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
    prep = vm.get("preparation") or {}
    if prep.get("error"):
        kind, badge, rank = "repair", "Needs repair", 4
    elif prep.get("attached") and not (vm["root"] / "config.yaml").is_file():
        kind, badge, rank = ("preparing", "Create Contract" if prep.get("linked") else "Prepare corpus", 1)
        receipt = prep.get("receipt") or {}
        source = {"name": (prep.get("owner_reference") or {}).get("source_id")
                  or receipt.get("snapshot_id") or ""}
        n_dev, n_sealed = receipt.get("n_eligible"), receipt.get("n_sealed")
    elif state["authority_hold"]:
        kind, badge, rank = "hold", "Read-only", 5
    elif _g0_retroactive_block(vm):
        kind, badge, rank = "repair", "Invalid G0", 4
    elif _g0_repair_request(vm):
        kind, badge, rank = "confirm", "Restore G0", 1
    elif state["canonical_integrity_errors"]:
        kind, badge, rank = "repair", "Needs repair", 4
    elif _open_definition_run(vm) and _meaning_allowed(vm):
        kind, badge, rank = "confirm", "Discuss meanings", 1
    elif canonical.get("meaning_definitions_missing"):
        kind, badge, rank = "confirm", "Define meanings", 1
    elif canonical and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation":
        kind, badge, rank = "confirm", "Confirm meaning", 1
    elif cal.get("phase") == "P1" and current:
        kind, badge, rank = "labeling", f"Labeling {current['finals']}/{current['batch_size']}", 0
    elif (cal.get("phase") == "P1" and rounds and rounds[-1]["state"] == "judged"
          and rounds[-1].get("calibration_status") == "running"):
        kind, badge, rank = "labeling", "Finish Run", 1
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
        "labeled": labeled, "current": current, "rounds": len(rounds),
        "runs": len(vm["runs"]) + len(prep.get("runs") or []),
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
        if (not (lane / "config.yaml").is_file()
                and not (lane / "preparation-ref.yaml").is_file()
                and not (lane / "preparation-owner.yaml").is_file()):
            if page_src.name.startswith("S-Label-"):
                labeling_url, _ = _job_urls(path_q, page)
                candidate = _page_folder_candidate(page_src)
                ready = candidate.is_file() and not candidate.is_symlink()
                empty.append({"id": page.get("id"), "title": page.get("title"),
                              "labeling_url": labeling_url + "&space=data&view=preparation",
                              "badge": "Prepare corpus" if ready else "Create Page folder"})
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
    waiting = [j for j in jobs if j["kind"] in {"labeling", "confirm", "ready", "preparing"}]
    if not jobs:
        headline = "No Page on this Board has a labeling job yet."
    elif waiting:
        headline = f"{len(waiting)} of {len(jobs)} jobs wait for you. Start with {waiting[0]['id']}: {waiting[0]['badge'].lower()}."
    else:
        headline = f"{len(jobs)} jobs. None is waiting for you right now."
    def record(job: dict) -> str:
        pill = {"preparing": "acc", "confirm": "acc", "labeling": "acc", "ready": "acc", "judged": "ok",
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
        links = "".join(
            f'<a class="rec job" href="{_esc(e["labeling_url"])}">'
            f'<div class=rh><span class=rid>{_esc(e["id"])}</span>'
            f'<span class=rt>{_esc(e.get("title") or e["id"])}</span>'
            f'<span class="pill mut">{_esc(e["badge"])}</span></div></a>'
            for e in data["empty"]
        )
        empty = f'<div class=card><h2>Pages before Contract</h2>{links}</div>'
    name = Path(board_dir).name
    tally = f'{len(waiting)} waiting · {len(jobs)} jobs'
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Labeling · {_esc(name)}</title><style>{_CSS}{_BOARD_CSS}</style></head><body>'
        '<h1>🏷 Labeling · all jobs</h1>'
        f'<p class="lead next"><b>Next:</b> {_esc(headline)}</p>'
        f'<div class=card style="margin-top:10px"><h2>Labeling jobs<span class=tally>{_esc(tally)}</span></h2>'
        f'{groups}</div>{empty}'
        '</body></html>'
    )


_BOARD_CSS = """
a.rec{display:block;color:var(--fg);text-decoration:none;border-radius:6px;margin:0 -6px;padding:8px 6px 6px}
a.rec:hover,a.rec:focus-visible{background:color-mix(in srgb,var(--acc) 6%,var(--card));outline:none}
.rgrp:first-of-type{margin-top:4px}
"""


class LabelingMixin:
    """The 🏷 tab: four Spaces over one labeling/ lane, plus the labeling writer door."""

    def _labeling_page_target(self, file_q: str):
        """Resolve a canonical Page folder only on the dedicated labeling host."""
        if getattr(self, "only", None) != frozenset({"labeling"}):
            return None, "standalone Labeling Page requires the dedicated labeling host"
        if not isinstance(file_q, str):
            return None, "file must be a string"
        if (not file_q or file_q.startswith("/") or "\\" in file_q
                or ":" in file_q or "\x00" in file_q):
            return None, "unsafe Page folder path"
        parts = PurePosixPath(file_q).parts
        if (any(part in {"", ".", ".."} for part in file_q.split("/"))
                or not file_q.endswith(".md")):
            return None, "unsafe Page folder path"
        root = self.root.resolve()
        candidate = root
        for part in parts:
            candidate = candidate / part
            if candidate.is_symlink():
                return None, "Page folder may not use symlinks"
        if candidate.parent.name != candidate.stem or not candidate.is_file():
            return None, "file must be a canonical <Page>/<Page>.md"
        try:
            candidate.resolve().relative_to(root)
        except (ValueError, OSError, RuntimeError):
            return None, "Page folder is outside the served root"
        if not is_labeling_surface_page(candidate):
            return None, "Page has no labeling lane"
        return candidate, None

    def labeling_page_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        page_src, err = self._labeling_page_target((q.get("file") or [""])[0])
        if page_src is None:
            return self.reply(400, {"ok": False, "err": err})
        file_q = page_src.relative_to(self.root.resolve()).as_posix()
        body = render(page_src, "", file_q, "", None, standalone=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

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
        if not generated_page_url(path_q, file_q, page_q, got[1]):
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
        if not generated_page_url(path_q, file_q, page_q, got[1]):
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
        standalone = p.get("mode") == "page"
        if p.get("mode") not in (None, "board", "page"):
            return 400, {"ok": False, "err": "unknown Labeling workbench mode"}
        if (standalone or p.get("action") == "confirm_meaning") and not origin:
            needed = "Workbench origin" if standalone else "Board origin"
            return 403, {"ok": False, "err": f"labeling write requires the {needed}"}
        if origin and urlparse(origin).netloc != host:
            return 403, {"ok": False, "err": "cross-origin labeling write refused"}
        got = (self._labeling_page_target(p.get("file")) if standalone else self.target(p))
        if got[0] is None:
            return 400, {"ok": False, "err": got[1]}
        page_src, board_dir = got
        if not is_labeling_surface_page(page_src):
            return 404, {"ok": False, "err": "Page has no labeling lane"}
        if not standalone and not generated_page_url(p.get("path") or "", p.get("file") or "",
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
        channel = "labeling workbench screen" if standalone else "board labeling screen"
        try:
            if action == "confirm_meaning":
                page_file = root.parent / page_src.name
                result = jobmod.confirm_meaning(
                    job_root=root, page_file=page_file, human_id=human,
                    confirmed_at=cal.now_iso(), accept_current_schema=True,
                    attest_as_human=p.get("attest") is True,
                    channel=channel)
            elif action == "release_round":
                result = cal.release_round(root, human_id=human, n=int(p.get("n") or 0) or None,
                                           channel=channel)
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
                                                   human_id=human, channel=channel)
                elif action == "embedding_item_text":
                    result = embmod.item_text(root, str(p.get("version") or ""), str(p.get("item_id") or ""),
                                              human_id=human, channel=channel)
                elif action == "build_embedding":
                    groups = p.get("groups")
                    proc, version = embmod.start_background_build(
                        root, str(p.get("model") or ""), channel=channel, started_by=human,
                        input_mode=str(p.get("input_mode") or "reply_context"),
                        instruction=p.get("instruction") or None,
                        groups=int(groups) if groups not in (None, "") else None,
                        map_method=str(p.get("map_method") or "tsne"), seed=int(p.get("seed") or 0))
                    _reap_when_done(proc)
                    result = {"version": version, "model": p.get("model")}
                else:
                    result = {"models": [{k: r.get(k) for k in ("id", "version", "state", "run", "failure", "log_tail")}
                                         for r in embmod.build_status(root)]}
            elif action == "item_page":
                viewmod = _corpus_view_module()
                if viewmod is None:
                    return 500, {"ok": False, "err": "subjective-label corpus reader unavailable"}
                result = viewmod.item_page(root, offset=int(p.get("offset") or 0), k=int(p.get("k") or 20),
                                           human_id=human, channel=channel)
            else:
                return 400, {"ok": False, "err": f"unknown labeling action: {action!r}"}
        except cal.LabelingRefused as error:
            return 409, {"ok": False, "err": str(error)}
        except RuntimeError as error:
            return 409, {"ok": False, "err": str(error)}
        except (ValueError, TypeError) as error:
            return 400, {"ok": False, "err": f"{type(error).__name__}: {error}"}
        return 200, {"ok": True, "result": result}
