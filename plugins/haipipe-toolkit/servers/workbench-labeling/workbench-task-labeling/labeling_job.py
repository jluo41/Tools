"""Read one labeling job from disk: its lane, its canonical status, and what `inspect` reports about it."""
from __future__ import annotations

import importlib.util
import json
import re
from functools import lru_cache
from pathlib import Path
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

    The engine lives with the labeling skills (``skills/3_theme/labeling/engine``),
    found by folder name.  Loading the small, dependency-stable ``job.py``
    module by path keeps the presenter from maintaining a second integrity
    implementation and from depending on the engine's Python package layout.
    """
    from host_paths import skill_dir
    candidate = skill_dir("labeling") / "engine" / "job.py"
    if not candidate.is_file():
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
        next_action = "P0 Contract · create the page-local labeling/ job through /hai-labeling"
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


def is_labeling_corpus_page(page_src: Path) -> bool:
    """A Page meant to hold one labeling job before it has one: an `S-Label-*` Page, or a
    Task Page of a labeling Block (`task-type: labeling` or `page-type: labeling`)."""
    if page_src.name.startswith("S-Label-") and page_src.name != "S-Label-Dash.md":
        return True
    try:
        head = page_src.read_text(encoding="utf-8", errors="ignore")[:4096]
    except OSError:
        return False
    return bool(re.search(r"(?m)^(task-type|page-type):\s*labeling\s*$", head))


def is_labeling_surface_page(page_src: Path) -> bool:
    """True for every real Page that can own an optional labeling/ lane.

    A specialized ``page-type: labeling`` changes the Page's prose grammar;
    it is not a prerequisite for opening a Page-local Workbench. The one control
    dashboard is excluded because it inventories jobs and owns no job itself.
    """
    return page_src.is_file() and page_src.name != "S-Label-Dash.md"
