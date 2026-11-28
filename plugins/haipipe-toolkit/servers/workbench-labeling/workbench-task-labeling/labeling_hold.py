"""When the chat and the drawing must hold, where a job's generated page lives, and the engine modules it
loads."""
from __future__ import annotations

import importlib.util
import re
from functools import lru_cache
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, unquote, urlparse

from live.labeling_job import (_board_pages, _canonical_job_module, _labeling_lane, _read_json, _yaml_top_scalar,
    inspect, is_labeling_surface_page)


# The labelings/ Job (hai-project 0.10.0, JL 261005: "for a data + labeling, it should be
# a job ... for this job, we will have many tasks"). A labeling Page at
# labelings/bNN_<block>/jNN_<dataset>_<label>/tNN_<task>/ belongs to that Job: one dataset with
# one label. The workbench is the Job's: its card carries the Job address, Data → Preparation
# lists the Job's data Tasks, and Quality gains External gold when a Task scores against the
# dataset's own labels. labeling/ stays in the labeling Task, so the engine reads nothing new.
_GOLD_TASK = re.compile(r"ground_truth|gold|scor")


def _page_heading(page: Path) -> str:
    try:
        lines = page.read_text(encoding="utf-8", errors="ignore").splitlines()[:5]
    except OSError:
        return ""
    return next((line[2:].strip() for line in lines if line.startswith("# ")), "")


def _task_runs(task: Path) -> list[dict]:
    """One row per Run of a Task: its state and headline, from its Result. A Run is one folder,
    runs/<run>/<run>.sh with runs/<run>/result/ (since 261010); a flat runs/<run>.sh with
    results/<run>/ still reads."""
    runs, results = task / "runs", {}
    for folder in sorted(runs.glob("r[0-9][0-9]_*/")) if runs.is_dir() else []:
        if (folder / f"{folder.name}.sh").is_file() or (folder / "run.yaml").is_file():
            results[folder.name] = folder / "result"
    for ticket in sorted(runs.glob("r[0-9][0-9]_*.sh")) if runs.is_dir() else []:
        results.setdefault(ticket.stem, task / "results" / ticket.stem)
    rows = []
    for name in sorted(results):
        result = results[name]
        summary = _read_json(result / "metrics.json").get("summary")
        rows.append({"run": name,
                     "status": _yaml_top_scalar(result / "runtime.yaml", "status") or "not run",
                     "headline": str((summary or {}).get("headline") or "") if isinstance(summary, dict) else ""})
    return rows


def _labeling_job(page_src: Path) -> dict | None:
    """The Job this labeling Page sits in, with all its Tasks; None outside labeling/ (or the older labelings/).

    A Task is `data` before the labeling Task, `gold` when it holds or scores against the
    dataset's own labels (its name says ground_truth, gold or scoring) or comes after it.
    """
    task, job = page_src.parent, page_src.parent.parent
    block = job.parent
    if (block.parent.name not in ("labeling", "labelings") or page_src.stem != task.name
            or not re.match(r"b\d{2}_", block.name) or not re.match(r"j\d{2}_", job.name)
            or not re.match(r"t\d{2}_", task.name)):
        return None
    tasks = []
    for folder in sorted(f for f in job.iterdir() if f.is_dir() and re.match(r"t\d{2}_", f.name)):
        page = folder / f"{folder.name}.md"
        if not page.is_file():
            continue
        role = ("labeling" if folder == task else
                "gold" if _GOLD_TASK.search(folder.name) or folder.name > task.name else "data")
        tasks.append({"name": folder.name, "title": _page_heading(page) or folder.name,
                      "role": role, "runs": _task_runs(folder)})
    return {"id": block.name[:3] + job.name[:3], "name": job.name, "tasks": tasks}


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
    """Validate and return the Page URL the Workbench belongs to.

    ``path_q`` is intentionally ``board.md`` because it resolves the source
    file.  It is not a browser Page.
    ``page_q`` is that Page in the live reader, ``/_board/page?path=<board>/<file>``
    (the Board's built site is retired, JL 261005): its ``path`` must name exactly
    ``file_q`` under the same Board, and ``file_q`` must be one of the Board's
    Pages.  A same-basename file elsewhere is therefore not sufficient.
    """
    parsed = urlparse(page_q or "")
    if parsed.scheme or parsed.netloc or parsed.fragment or parsed.path != "/_board/page":
        return ""
    target = unquote((parse_qs(parsed.query).get("path") or [""])[0])
    decoded_board = unquote(urlparse(path_q or "").path)
    if not decoded_board.endswith("/board.md") or board_dir is None:
        return ""
    # a path= with or without its leading "/" names the same Board (the frame's links have none; 261008)
    board_root = "/" + decoded_board.rsplit("/", 1)[0].strip("/")
    if ".." in PurePosixPath(target).parts or ".." in PurePosixPath(file_q or "").parts:
        return ""
    if "/" + target.lstrip("/") != f"{board_root}/{file_q}":
        return ""
    try:
        pages = _board_pages(Path(board_dir))
    except (OSError, ValueError, TypeError):
        return ""
    if sum(1 for q in pages if q.get("file") == file_q) != 1:
        return ""
    if not (Path(board_dir) / file_q).is_file():
        return ""
    return page_q


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
def _meaning_store_module():
    """Load the decision-report store (``meaning_store``: published reports, drafts, submissions), the record behind a
    building Task's Decide view (b15 j01 s58 C2; s03 implementation-plan CONTRACTS.md version 2, sections 5 and 6)."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    candidate = Path(job_module.__file__).with_name("meaning_store.py")
    if not candidate.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "haipipe_subjective_label_meaning_store_for_board", candidate
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _stored(value, anchor: Path) -> Path:
    """A path a preparation record keeps, back to a real one: new records keep it relative to the
    SPACE root (AGENTS.md rule 7); an old absolute record reads as is."""
    module = _preparation_module()
    if module is not None and hasattr(module, "resolve_stored"):
        return module.resolve_stored(value, anchor)
    return Path(str(value or ""))


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
