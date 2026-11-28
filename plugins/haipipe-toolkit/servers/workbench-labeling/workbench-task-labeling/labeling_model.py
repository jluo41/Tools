"""The view model of one labeling page: its Spaces, Run rows, next step, gate checks and small text helpers."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from live.labeling_job import _canonical_job_module, _job_root, _page_folder_candidate, _read_json, inspect
from live.labeling_hold import _calibration_module, _embedding_module, _labeling_job, _preparation_module, _stored


SPACES = (
    ("data", "Data", (("preparation", "Preparation"), ("contract", "Contract"), ("embedding", "Embedding"))),
    ("labeling", "Labeling", (("definition", "Definition"), ("rounds", "Rounds"), ("guideline", "Guideline"))),
    ("quality", "Quality", (("test", "Test"), ("evaluation", "Evaluation"), ("audit", "Audit"))),
    ("delivery", "Delivery", (("handoff", "Handoff"), ("scan", "Scan"), ("final", "Final labels"))),
)


def _spaces(vm: dict) -> tuple:
    """SPACES, plus Quality → External gold when this Page's Job has a Task that holds or scores
    against the dataset's own labels: a view exists only because Runs live in it (JL 260928)."""
    if not any(t["role"] == "gold" for t in (vm.get("job") or {}).get("tasks", [])):
        return SPACES
    return tuple((sid, name, views + (("gold", "External gold"),)) if sid == "quality"
                 else (sid, name, views) for sid, name, views in SPACES)


def _job_tasks_card(vm: dict, role: str, title: str) -> str:
    """The Job's other Tasks of one role, each with its latest Run's state and headline."""
    rows = []
    for task in (vm.get("job") or {}).get("tasks", []):
        if task["role"] != role:
            continue
        last = task["runs"][-1] if task["runs"] else None
        if last:
            cls, word = _STEP_STATE.get(last["status"], ("mut", last["status"]))
            value = (f'<span class={cls}>{_esc(word)}</span> · <code>{_esc(last["run"])}</code>'
                     + (f' · {_esc(last["headline"])}' if last["headline"] else ""))
        else:
            value = '<span class=mut>no Run yet</span>'
        rows.append(_row(task["title"], value))
    return _card(title, "".join(rows)) if rows else ""


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
        "job": _labeling_job(page_src),
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
        owner = _stored(owner_ref.get("owner"), owner_file)
        source_id = str(owner_ref.get("source_id") or "")
        expected = {"schema": "subjective-label/preparation-owner-v1", "source_id": source_id}
        if (not owner.is_absolute() or owner.name != "corpus-preparation" or owner.is_symlink()
                or not source_id or _load_mapping(owner / "source.yaml") != expected
                or set(owner_ref) != {*expected, "owner"}
                or any(owner_ref.get(k) != v for k, v in expected.items())):
            return {"attached": True, "linked": False, "owner_reference": owner_ref,
                    "runs": [], "error": "preparation owner reference is invalid or changed"}
        return {"attached": True, "linked": False, "owner_reference": owner_ref,
                "runs": _run_rows(root, owner=owner, family="corpus")}
    owner = _stored(ref.get("owner"), accepted_file)
    package = _stored(ref.get("package"), accepted_file)
    if (not owner.is_absolute() or owner.name != "corpus-preparation"
            or not package.is_relative_to(owner / "packages") or owner.is_symlink()):
        return {"attached": True, "linked": True, "reference": ref, "runs": [],
                "error": "preparation reference has an invalid owner or package path"}
    owner_record = _load_mapping(owner / "source.yaml")
    if owner_ref and (set(owner_ref) != {*owner_record, "owner"}
                      or any(owner_ref.get(k) != v for k, v in owner_record.items())
                      or _stored(owner_ref.get("owner"), owner_file).resolve() != owner.resolve()
                      or owner_record.get("schema") != "subjective-label/preparation-owner-v1"):
        return {"attached": True, "linked": True, "reference": ref, "runs": [],
                "error": "preparation owner and accepted package references disagree"}
    module = _preparation_module()
    if module is None:
        return {"attached": True, "linked": True, "reference": ref, "runs": [],
                "error": "Corpus Preparation engine is unavailable"}
    try:
        receipt = module.verify_package(package)
        if not module.same_reference(ref, module.preparation_reference(owner, package, receipt), accepted_file):
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


_FRAGMENTS = {"don", "doesn", "didn", "isn", "wasn", "aren", "weren", "couldn", "wouldn", "shouldn",
              "haven", "hasn", "hadn", "won", "ain", "ll", "ve", "re"}


def _clean_keywords(words) -> list[str]:
    """Group keywords without contraction fragments (don, doesn) that read as typos."""
    return [str(w) for w in words or [] if str(w).lower() not in _FRAGMENTS]


def _job_where(vm: dict) -> str:
    """The job folder relative to the repo, as a chat in this repo would type it."""
    root = vm["root"]
    module = _calibration_module()
    repo = module._repo_root(root) if module else None
    try:
        return str(root.relative_to(repo)) if repo else str(root)
    except ValueError:
        return str(root)


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


def _md_inline(text: str) -> str:
    text = _esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)



def _space_mapping_ref() -> Path | None:
    """hai-labeling-building/ref/ref-space-mapping.md, found next to the engine the Board already loads."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    labeling = Path(job_module.__file__).resolve().parents[1]      # skills/3_theme/labeling
    for path in (labeling / "hai-labeling-building" / "ref" / "ref-space-mapping.md",
                 labeling / "ref" / "ref-space-mapping.md"):
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


def _run_name(run_id: str) -> str:
    """Keep new full names verbatim; expand old Labeling addresses for display."""
    if run_id.startswith("run-"):
        return run_id
    return "run-labeling-" + re.sub(r"^rl\d+_", "", run_id).replace("_", "-")


def _current_policy(root: Path) -> str:
    current = root / "policy" / "current"
    return current.read_text(encoding="utf-8").strip() if current.is_file() else ""


_STEP_STATE = {"complete": ("ok", "done"), "running": ("acc", "in progress"), "failed": ("warn", "failed")}


def _script_json(value) -> str:
    return (json.dumps(value, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))
