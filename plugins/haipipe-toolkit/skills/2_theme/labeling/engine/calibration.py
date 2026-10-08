#!/usr/bin/env python3
"""P1 Round writer for one subjective-label job: release, prepare, judge.

This module is the Building side's item-level writer.  It owns exactly three
things, in the order ``haipipe-labeling-building`` gives them:

    CARD     the identified human releases a round card        card.md
    PREPARE  a random development draw is frozen               run-labeling-round-prepare-...
    JUDGE    show → first → lock → reveal → final, per item    run-labeling-human-calibration-...

Every judgment is an append-only, sequence-numbered event in
``rounds/round_NN/sessions/events.jsonl``; no record carries a content hash.  Nothing here promotes gold or a
policy version: that is ``round-close`` and the Checkpoint Keeper.  A sealed
item is never drawn, indexed, shown, or revealed.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import importlib.util
import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import yaml


HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("subjective_label_job_for_calibration", HERE / "job.py")
job = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(job)

EVENT_KINDS = ("show", "first", "lock", "reveal", "final")
CHANGE_TYPES = ("none", "correction", "clarification", "concept_revision", "unresolved")
EVENTS_SCHEMA = "subjective-label-calibration-event/v1"
EVENT_FIELDS = ("schema", "seq", "at", "run", "round_id", "item_id", "kind", "human_id", "session_id", "payload")
CALIBRATION_ACCEPTANCE = "every batch row has a final event; the event log verifies"
DEFAULT_BATCH = 20
MAX_BATCH = 200


class LabelingRefused(RuntimeError):
    """A write the method forbids at this state; the message names why."""


# ── small helpers ────────────────────────────────────────────────────────────


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def round_dir_name(t: int) -> str:
    return f"round_{t:02d}"


def round_target(t: int) -> str:
    return f"round-{t:02d}"


def _round_index(name: str) -> int:
    hit = re.fullmatch(r"round_(\d+)", name)
    if not hit:
        raise LabelingRefused(f"unknown round id: {name!r}")
    return int(hit.group(1))


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _jsonl_bytes(rows: list[dict]) -> bytes:
    return "".join(
        json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows
    ).encode("utf-8")


@contextlib.contextmanager
def _locked(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _config(job_root: Path) -> dict:
    return job.load_mapping(job_root / "config.yaml")


def _schema(config: dict) -> dict:
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    return {
        "labels": [str(v) for v in labels.get("values") or []],
        "label_meanings": labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {},
        "regions": [str(v) for v in regions.get("values") or []],
        "region_meanings": regions.get("meanings") if isinstance(regions.get("meanings"), dict) else {},
        "uncertainty": [str(v) for v in uncertainty.get("levels") or []],
    }


def _run_name(job_root: Path, operation: str, target: str) -> str:
    return job.mint_labeling_run(job_root, operation, target)


def _find_run(job_root: Path, operation: str, target: str) -> str | None:
    hits = job.matching_runs(job_root, operation, target)
    return hits[-1] if hits else None


def _repo_root(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        if (parent / "pyproject.toml").is_file() and (parent / "code").is_dir():
            return parent
    return None


# ── authority ────────────────────────────────────────────────────────────────


def require_human_p1(job_root: Path, human_id: str) -> dict:
    """Require the configured caller id after G0 on a job not on HOLD.

    The local engine checks the supplied id against project configuration; it
    does not authenticate the caller's identity.
    """
    state = job.status(job_root)
    if state.get("hold"):
        raise LabelingRefused(f"HOLD · {state.get('hold_reason')}")
    if state["phase"] != "P1":
        raise LabelingRefused(f"{state['first_blocked_frontier']} · {state['next_action']}")
    if not human_id or human_id != state.get("human_id"):
        raise LabelingRefused(
            "caller-supplied human_id must match the configured semantic authority"
        )
    return state


# ── corpus ───────────────────────────────────────────────────────────────────


def _corpus_rows(job_root: Path) -> list[dict]:
    return _read_jsonl(job_root / "corpus" / "items.jsonl")


def _eligible_ids(job_root: Path) -> list[str]:
    """Development pool: only rows explicitly marked eligible.  Sealed never enters."""
    return sorted(
        str(row["item_id"]) for row in _corpus_rows(job_root)
        if row.get("population_status") == "eligible" and row.get("item_id") is not None
    )


def _item(job_root: Path, item_id: str, config: dict) -> dict:
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    text_field = str(corpus.get("text_field") or "text")
    context_field = str(corpus.get("context_field") or "context_prev")
    for row in _corpus_rows(job_root):
        if str(row.get("item_id")) == item_id:
            if row.get("population_status") != "eligible":
                raise LabelingRefused("this item is not in the development pool")
            return {
                "item_id": item_id,
                "text": row.get(text_field) or "",
                "context": row.get(context_field) or "",
                "text_hash": row.get("text_hash"),
            }
    raise LabelingRefused(f"item not found: {item_id}")


# ── rounds: read side ────────────────────────────────────────────────────────


def _round_dirs(job_root: Path) -> list[Path]:
    base = job_root / "rounds"
    if not base.is_dir():
        return []
    return sorted(
        (p for p in base.iterdir() if p.is_dir() and re.fullmatch(r"round_\d+", p.name)),
        key=lambda p: _round_index(p.name),
    )


def _events(round_path: Path) -> list[dict]:
    return _read_jsonl(round_path / "sessions" / "events.jsonl")


def _item_states(round_path: Path) -> dict[str, dict]:
    states: dict[str, dict] = {}
    for event in _events(round_path):
        entry = states.setdefault(str(event["item_id"]), {"kinds": [], "first": None, "reveal": None, "final": None})
        entry["kinds"].append(event["kind"])
        if event["kind"] in {"first", "reveal", "final"}:
            entry[event["kind"]] = event
    return states


def round_summary(job_root: Path, round_path: Path) -> dict:
    t = _round_index(round_path.name)
    batch = _read_jsonl(round_path / "human_batch.jsonl")
    states = _item_states(round_path)
    finals = sum(1 for row in batch if states.get(str(row["item_id"]), {}).get("final"))
    prepare_run = _find_run(job_root, "round-prepare", round_target(t))
    calibration_run = _find_run(job_root, "human-calibration", round_target(t))
    calibration_status = None
    if calibration_run:
        runtime = job.results_dir(job_root) / calibration_run / "runtime.yaml"
        if runtime.is_file():
            calibration_status = (yaml.safe_load(runtime.read_text(encoding="utf-8")) or {}).get("status")
    if (round_path / "checkpoint.json").is_file():
        state = "closed"
    elif batch and finals == len(batch):
        state = "judged"
    elif calibration_run:
        state = "judging"
    elif batch:
        state = "prepared"
    elif (round_path / "card.md").is_file():
        state = "released"
    else:
        state = "empty"
    open_item = next(
        (str(row["item_id"]) for row in batch if not states.get(str(row["item_id"]), {}).get("final")),
        None,
    )
    return {
        "round_id": round_path.name,
        "index": t,
        "state": state,
        "batch_size": len(batch),
        "finals": finals,
        "open_item": open_item,
        "prepare_run": prepare_run,
        "calibration_run": calibration_run,
        "calibration_status": calibration_status,
    }


def job_state(job_root: Path) -> dict:
    """Status plus every round's derived state; never writes."""
    job_root = job_root.resolve()
    state = job.status(job_root)
    rounds = [round_summary(job_root, p) for p in _round_dirs(job_root)] if state["phase"] == "P1" else []
    current = next((r for r in rounds if r["state"] in {"released", "prepared", "judging"}), None)
    if state["phase"] != "P1":
        next_step = state["next_action"]
    elif current:
        next_step = f"label {current['round_id']}: {current['finals']}/{current['batch_size']} done"
    elif rounds and rounds[-1]["state"] == "judged" and rounds[-1]["calibration_status"] == "running":
        next_step = f"finalize the interrupted human-calibration Result for {rounds[-1]['round_id']}"
    elif rounds and rounds[-1]["state"] == "judged":
        next_step = (
            f"{rounds[-1]['round_id']} judged · next: guideline-learn, round-measure, "
            "round-close (Checkpoint Keeper)"
        )
    elif rounds and rounds[-1]["state"] == "closed":
        next_step = "release the next round card"
    else:
        next_step = "release round_01"
    config = job.try_load_mapping(job_root / "config.yaml")[0]
    return {**state, "rounds": rounds, "current_round": current, "next_step": next_step,
            "schema": _schema(config) if config else {}}


# ── CARD + PREPARE ───────────────────────────────────────────────────────────


def _unfinished_definition_discussion(job_root: Path) -> str | None:
    """A round cannot freeze its policy while a meaning discussion is open."""
    try:
        return job.unfinished_definition_discussion(job_root)
    except RuntimeError as error:
        raise LabelingRefused(str(error)) from error


def release_round(
    job_root: Path,
    *,
    human_id: str,
    n: int | None = None,
    seed: int | None = None,
    channel: str = "cli",
) -> dict:
    """The human releases the next round card; round-prepare then freezes a random batch.

    Only a random development draw is implemented, which is exactly round 1's
    arm.  A later round needs the previous checkpoint and a candidate pool; it
    is refused until round-close exists.
    """
    job_root = job_root.resolve()
    require_human_p1(job_root, human_id)
    discussion = _unfinished_definition_discussion(job_root)
    if discussion:
        raise LabelingRefused(f"close definition discussion {discussion} before releasing a round")
    config = _config(job_root)
    rounds_cfg = config.get("rounds") if isinstance(config.get("rounds"), dict) else {}
    round1 = rounds_cfg.get("round1") if isinstance(rounds_cfg.get("round1"), dict) else {}
    existing = _round_dirs(job_root)
    if existing:
        last = round_summary(job_root, existing[-1])
        if last["state"] != "closed":
            raise LabelingRefused(
                f"{last['round_id']} is {last['state']}; finish and close it before releasing another round"
            )
        raise LabelingRefused(
            "a later round needs a candidate pool around open register cells; "
            "only round_01's random draw is implemented"
        )
    t = 1
    size = int(n if n is not None else round1.get("human_batch_size") or DEFAULT_BATCH)
    if size < 1 or size > MAX_BATCH:
        raise LabelingRefused(f"batch size must be between 1 and {MAX_BATCH}")
    draw_seed = int(seed if seed is not None else round1.get("seed") or 42)
    pool = _eligible_ids(job_root)
    if len(pool) < size:
        raise LabelingRefused(f"development pool has {len(pool)} items; asked for {size}")

    round_path = job_root / "rounds" / round_dir_name(t)
    released_at = now_iso()
    policy_version = (job_root / "policy" / "current").read_text(encoding="utf-8").strip() \
        if (job_root / "policy" / "current").is_file() else "G_00"
    card = (
        f"# {round_dir_name(t)} · card\n\n"
        f"state: released\n"
        f"released_by: {human_id}\n"
        f"released_at: {released_at}\n"
        f"channel: {channel}\n"
        f"policy: {policy_version}\n"
        f"arm: random development draw\n"
        f"n: {size}\n"
        f"seed: {draw_seed}\n"
        f"targets: none (round 1 names no register cell)\n"
        f"expected: no forecast; round 1 learns where the boundary questions are\n"
    ).encode("utf-8")
    job.write_once(round_path / "card.md", card)

    drawn = random.Random(draw_seed).sample(pool, size)
    probability = size / len(pool)
    n_corpus_rows = len(_corpus_rows(job_root))
    candidate_rows = [
        {
            "round_id": round_dir_name(t), "item_id": item_id, "source_pool": "random",
            "scores": {}, "ranker": {"name": "uniform-random", "version": "1"},
            "selection_reason": "round 1 random development draw",
            "seed": draw_seed, "inclusion_probability": probability,
        }
        for item_id in drawn
    ]
    batch_rows = [
        {
            "round_id": round_dir_name(t), "order": index, "item_id": item_id,
            "primary_role": "audit", "source_pool": "random", "stratum": {},
            "selection_probability": probability, "seed": draw_seed,
            "blind_access_state": "sealed",
        }
        for index, item_id in enumerate(drawn)
    ]
    pool_bytes = _jsonl_bytes(candidate_rows)
    batch_bytes = _jsonl_bytes(batch_rows)
    manifest = {
        "schema": "subjective-label-round-manifest/v1",
        "round_id": round_dir_name(t),
        "policy_version": policy_version,
        "development_pool_size": len(pool),
        "draw": {"method": "uniform-random", "n": size, "seed": draw_seed},
        "prelabels": "none (round 1 has no weak executors)",
    }
    evidence = (
        f"# {round_dir_name(t)} · evidence\n\n"
        f"- policy: {policy_version}\n"
        f"- corpus items: {n_corpus_rows} rows in corpus/items.jsonl\n"
        f"- development pool: {len(pool)} eligible items (sealed items excluded by population_status)\n"
        f"- prior gold D_00: empty\n"
        f"- human batch: {size} items in human_batch.jsonl, seed {draw_seed}\n"
    ).encode("utf-8")
    prospect = (
        f"# {round_dir_name(t)} · prospect\n\n"
        "Written before the first item is shown.\n\n"
        "- Round 1 is a random draw with no prelabels, so there is no disagreement forecast.\n"
        "- Expected finding: the first boundary questions and which register cells stay open.\n"
    ).encode("utf-8")
    readme = (
        f"# {round_dir_name(t)}\n\n"
        f"id: {round_dir_name(t)}\nlineage: {policy_version} -> (G_01 at close)\n"
        f"serves: first calibration round\nstate: prepared\n"
    ).encode("utf-8")

    run = _find_run(job_root, "round-prepare", round_target(t)) or _run_name(
        job_root, "round-prepare", round_target(t)
    )
    artifacts = {
        round_path / "candidate_pool.jsonl": pool_bytes,
        round_path / "human_batch.jsonl": batch_bytes,
        round_path / "manifest.yaml": job.yaml_bytes(manifest),
        round_path / "evidence.md": evidence,
        round_path / "prospect.md": prospect,
        round_path / "README.md": readme,
    }
    for path, data in artifacts.items():
        job.write_once(path, data)
    (round_path / "sessions").mkdir(exist_ok=True)
    rels = ["card.md", "candidate_pool.jsonl", "human_batch.jsonl", "manifest.yaml", "evidence.md", "prospect.md"]
    _write_run(
        job_root, run,
        operation="round-prepare", phase="P1", episode=round_dir_name(t), target=round_target(t),
        commission={"path": job.page_path(job_root, f"rounds/{round_dir_name(t)}/card.md")},
        inputs=[{"path": job.page_path(job_root, "corpus/items.jsonl")}],
        worker={"kind": "engine", "name": "subjective-label.engine.calibration:release_round"},
        acceptance="batch frozen with seed and inclusion probability before any show event",
        status="complete", started_at=released_at, finished_at=now_iso(),
        outcome=f"{size} items drawn from {len(pool)} eligible",
        artifacts=[{"path": job.page_path(job_root, f"rounds/{round_dir_name(t)}/{rel}")} for rel in rels],
    )
    return {"round_id": round_dir_name(t), "run": run, "batch_size": size, "pool": len(pool)}


def _write_once_mapping(path: Path, value: dict) -> None:
    """Write one immutable YAML record; an existing one must hold the same values (any formatting)."""
    if path.is_file() and not path.is_symlink():
        existing = yaml.safe_load(path.read_text(encoding="utf-8"))
        if existing == value:
            return
        raise RuntimeError(f"refusing to overwrite changed artifact: {path}")
    job.write_once(path, job.yaml_bytes(value))


def _write_run(job_root: Path, run: str, *, operation: str, phase: str, episode: str,
               target: str, commission: dict, inputs: list, worker: dict, acceptance: str,
               status: str, started_at: str, finished_at: str | None, outcome: str,
               artifacts: list) -> None:
    ticket = {
        "run": run, "family": "labeling", "domain": "subjective-label", "phase": phase,
        "operation": operation, "episode": episode, "target": target,
        "commission": commission, "inputs": inputs, "worker": worker,
        "acceptance": acceptance, "supersedes": None,
    }
    _write_once_mapping(job.runs_dir(job_root) / f"{run}.yaml", ticket)
    runtime = {
        "run": run, "family": "labeling", "operation": operation, "target": target,
        "status": status, "ticket": f"runs/{run}.yaml", "result": f"results/{run}/result.yaml",
        "inputs": inputs, "outcome": outcome, "worker": worker,
        "started_at": started_at, "finished_at": finished_at, "supersedes": None, "failure": None,
    }
    runtime_path = job.results_dir(job_root) / run / "runtime.yaml"
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.write_bytes(job.yaml_bytes(runtime))  # lifecycle file: running -> complete
    if status == "complete":
        result = {
            "run": run, "family": "labeling", "operation": operation, "status": "complete",
            "outcome": outcome, "artifacts": artifacts,
            "promotion": {"performed": False, "reason": "only round-close promotes gold and policy"},
        }
        _write_once_mapping(job.results_dir(job_root) / run / "result.yaml", result)


# ── JUDGE ────────────────────────────────────────────────────────────────────


def _round_for_judging(job_root: Path, round_id: str) -> tuple[Path, list[dict]]:
    round_path = job_root / "rounds" / round_id
    _round_index(round_id)
    batch = _read_jsonl(round_path / "human_batch.jsonl")
    if not batch:
        raise LabelingRefused(f"{round_id} has no frozen batch")
    if (round_path / "checkpoint.json").is_file():
        raise LabelingRefused(f"{round_id} is closed")
    return round_path, batch


def _ensure_calibration_run(job_root: Path, round_path: Path, human_id: str) -> str:
    t = _round_index(round_path.name)
    run = _find_run(job_root, "human-calibration", round_target(t))
    if run:
        runtime_path = job.results_dir(job_root) / run / "runtime.yaml"
        try:
            runtime = yaml.safe_load(runtime_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            raise LabelingRefused(f"calibration Run {run} has no readable runtime") from error
        if not isinstance(runtime, dict) or runtime.get("status") != "running":
            raise LabelingRefused(f"calibration Run {run} is not running; repair its lifecycle before judging")
        return run
    run = _run_name(job_root, "human-calibration", round_target(t))
    started = now_iso()
    _write_run(
        job_root, run,
        operation="human-calibration", phase="P1", episode=round_path.name, target=round_target(t),
        commission={"path": job.page_path(job_root, f"rounds/{round_path.name}/human_batch.jsonl")},
        inputs=[{"path": job.page_path(job_root, f"rounds/{round_path.name}/manifest.yaml")}],
        worker={"kind": "human", "name": human_id, "surface": "labeling screen"},
        acceptance=CALIBRATION_ACCEPTANCE,
        status="running", started_at=started, finished_at=None,
        outcome="judging", artifacts=[],
    )
    return run


def _append_event(round_path: Path, event: dict) -> dict:
    path = round_path / "sessions" / "events.jsonl"
    existing = _read_jsonl(path)
    record = {
        "schema": EVENTS_SCHEMA,
        "seq": len(existing) + 1,
        "at": now_iso(),
        **event,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
    return record


# The kind an item must already have before each event kind may be recorded.
EVENT_REQUIRES = {"first": "show", "lock": "first", "reveal": "lock", "final": "reveal"}


def verify_events(round_path: Path) -> list[str]:
    """Check the event log by content; return every defect.

    Sequence numbers run 1, 2, 3 with no gap; every event carries the required
    fields and a known kind; per item, first follows show, lock follows first,
    reveal follows lock, final follows reveal, and first and final happen once.
    A lock names its first event by ``first_seq``.  Legacy ``checksum`` and
    ``prev_checksum`` fields, if present, are ignored.
    """
    errors = []
    kinds_by_item: dict[str, list[str]] = {}
    first_seq_by_item: dict[str, int] = {}
    for index, record in enumerate(_events(round_path), start=1):
        if record.get("seq") != index:
            errors.append(f"event {index}: sequence gap")
        absent = [field for field in EVENT_FIELDS if field not in record]
        if absent:
            errors.append(f"event {index}: missing {', '.join(absent)}")
            continue
        kind, item_id = record.get("kind"), str(record.get("item_id"))
        if kind not in EVENT_KINDS:
            errors.append(f"event {index}: unknown kind {kind!r}")
            continue
        seen = kinds_by_item.setdefault(item_id, [])
        needed = EVENT_REQUIRES.get(kind)
        if needed and needed not in seen:
            errors.append(f"event {index}: {kind} for item {item_id} before any {needed}")
        if kind in {"first", "final"} and kind in seen:
            errors.append(f"event {index}: second {kind} for item {item_id}")
        payload = record.get("payload") if isinstance(record.get("payload"), dict) else {}
        if kind == "first":
            first_seq_by_item[item_id] = record.get("seq")
        if kind == "lock" and "first_seq" in payload and payload["first_seq"] != first_seq_by_item.get(item_id):
            errors.append(f"event {index}: lock does not name item {item_id}'s first event")
        seen.append(kind)
    return errors


def _judgment(schema: dict, class_label: str | None, region: str | None,
              uncertainty: str | None, reason: str, rejected: str | None,
              allow_unresolved: bool = False) -> dict:
    if class_label is None and allow_unresolved:
        pass
    elif class_label not in schema["labels"]:
        raise LabelingRefused(f"class must be one of {schema['labels']}")
    if region is not None and region not in schema["regions"]:
        raise LabelingRefused(f"region must be one of {schema['regions']}")
    if uncertainty not in schema["uncertainty"]:
        raise LabelingRefused(f"uncertainty must be one of {schema['uncertainty']}")
    if rejected is not None and rejected not in schema["labels"]:
        raise LabelingRefused("rejected alternative must be a class value")
    return {
        "class_label": class_label,
        "diagnostic_region": region,
        "uncertainty": {"level": uncertainty},
        "rationale": {"reason": (reason or "").strip()[:2000], "rejected_label": rejected},
    }


def open_item(job_root: Path, round_id: str, *, human_id: str, session_id: str,
              item_id: str | None = None) -> dict:
    """Return the resume item (or a named batch item) and record its show event."""
    job_root = job_root.resolve()
    require_human_p1(job_root, human_id)
    config = _config(job_root)
    round_path, batch = _round_for_judging(job_root, round_id)
    with _locked(round_path / "sessions" / ".lock"):
        run = _ensure_calibration_run(job_root, round_path, human_id)
        states = _item_states(round_path)
        ids = [str(row["item_id"]) for row in batch]
        if item_id is None:
            item_id = next((i for i in ids if not states.get(i, {}).get("final")), None)
        if item_id is None:
            return {"round_id": round_id, "run": run, "done": True,
                    **_progress(batch, states)}
        if item_id not in ids:
            raise LabelingRefused("item is not in this round's frozen batch")
        entry = states.get(item_id, {"kinds": []})
        shown_here = any(
            e.get("session_id") == session_id and str(e["item_id"]) == item_id and e["kind"] == "show"
            for e in _events(round_path)
        )
        if "first" not in entry["kinds"] and not shown_here:
            _append_event(round_path, {"run": run, "round_id": round_id, "item_id": item_id,
                                       "kind": "show", "human_id": human_id, "session_id": session_id,
                                       "payload": {"prelabels_visible": False}})
        if entry.get("first") and not entry.get("reveal") and not entry.get("final"):
            # A stopped writer may have recorded first or lock without the reveal.
            # Finish that same first answer; never ask the person to answer again.
            first_seq = entry["first"].get("seq")
            if not isinstance(first_seq, int) or first_seq < 1:
                raise LabelingRefused("first judgment has no valid event sequence")
            comparison = reveal_for(job_root, config, item_id)
            base = {"run": run, "round_id": round_id, "item_id": item_id,
                    "human_id": human_id, "session_id": session_id}
            if "lock" not in entry["kinds"]:
                _append_event(round_path, {**base, "kind": "lock", "payload": {"first_seq": first_seq}})
            _append_event(round_path, {**base, "kind": "reveal", "payload": comparison})
        states = _item_states(round_path)
    entry = states.get(item_id, {})
    stage = "final" if entry.get("final") else "reveal" if entry.get("reveal") else "first"
    return {
        "round_id": round_id, "run": run, "done": False, "stage": stage,
        "item": _item(job_root, item_id, config),
        "position": [str(row["item_id"]) for row in batch].index(item_id) + 1,
        "first": (entry.get("first") or {}).get("payload"),
        "reveal": (entry.get("reveal") or {}).get("payload"),
        "final": (entry.get("final") or {}).get("payload"),
        **_progress(batch, states),
    }


def _progress(batch: list[dict], states: dict) -> dict:
    finals = sum(1 for row in batch if states.get(str(row["item_id"]), {}).get("final"))
    return {"batch_size": len(batch), "finals": finals}


def record_first(job_root: Path, round_id: str, item_id: str, *, human_id: str, session_id: str,
                 class_label: str, region: str | None, uncertainty: str, reason: str = "",
                 rejected_label: str | None = None) -> dict:
    """first → lock → reveal, as three events.  Returns the reveal payload."""
    job_root = job_root.resolve()
    require_human_p1(job_root, human_id)
    config = _config(job_root)
    schema = _schema(config)
    round_path, batch = _round_for_judging(job_root, round_id)
    if item_id not in {str(row["item_id"]) for row in batch}:
        raise LabelingRefused("item is not in this round's frozen batch")
    judgment = _judgment(schema, class_label, region or _pure_region(schema, class_label),
                         uncertainty, reason, rejected_label)
    with _locked(round_path / "sessions" / ".lock"):
        run = _ensure_calibration_run(job_root, round_path, human_id)
        kinds = _item_states(round_path).get(item_id, {}).get("kinds", [])
        if "show" not in kinds:
            raise LabelingRefused("an item must be shown before its first judgment")
        if "first" in kinds:
            raise LabelingRefused("the first judgment is already locked for this item")
        base = {"run": run, "round_id": round_id, "item_id": item_id,
                "human_id": human_id, "session_id": session_id}
        comparison = reveal_for(job_root, config, item_id)
        first = _append_event(round_path, {**base, "kind": "first",
                                           "payload": {**judgment, "prelabels_visible": False}})
        _append_event(round_path, {**base, "kind": "lock",
                                   "payload": {"first_seq": first["seq"]}})
        _append_event(round_path, {**base, "kind": "reveal", "payload": comparison})
    return {"first": judgment, "reveal": comparison}


def _pure_region(schema: dict, class_label: str | None) -> str | None:
    if not class_label:
        return None
    letter = class_label[:1].upper()
    return letter if letter in schema["regions"] else None


def record_final(job_root: Path, round_id: str, item_id: str, *, human_id: str, session_id: str,
                 class_label: str | None, region: str | None, uncertainty: str,
                 change_type: str = "none", reason: str = "") -> dict:
    job_root = job_root.resolve()
    require_human_p1(job_root, human_id)
    config = _config(job_root)
    schema = _schema(config)
    round_path, batch = _round_for_judging(job_root, round_id)
    if change_type not in CHANGE_TYPES:
        raise LabelingRefused(f"change type must be one of {list(CHANGE_TYPES)}")
    unresolved = change_type == "unresolved"
    judgment = _judgment(schema, None if unresolved else class_label,
                         region or _pure_region(schema, class_label), uncertainty, reason,
                         None, allow_unresolved=unresolved)
    with _locked(round_path / "sessions" / ".lock"):
        run = _ensure_calibration_run(job_root, round_path, human_id)
        states = _item_states(round_path)
        entry = states.get(item_id, {"kinds": []})
        if "lock" not in entry["kinds"] or "reveal" not in entry["kinds"]:
            raise LabelingRefused("final comes only after first, lock, and reveal")
        if "final" in entry["kinds"]:
            raise LabelingRefused("this item already has a final judgment")
        first = entry["first"]["payload"]
        same = (first.get("class_label") == judgment["class_label"]
                and first.get("diagnostic_region") == judgment["diagnostic_region"])
        if change_type == "none" and not same:
            raise LabelingRefused("the final differs from the first; name the change type")
        _append_event(round_path, {"run": run, "round_id": round_id, "item_id": item_id,
                                   "kind": "final", "human_id": human_id, "session_id": session_id,
                                   "payload": {**judgment, "change_type": change_type,
                                               "terminal_disposition": "unresolved" if unresolved else "labeled"}})
        states = _item_states(round_path)
        progress = _progress(batch, states)
        closed = None
        if progress["finals"] == progress["batch_size"]:
            closed = _close_calibration(job_root, round_path, batch, states, run, config)
    return {**progress, "closed_run": closed}


FEEDBACK_FILE = "feedback.jsonl"   # rounds/round_NN/sessions/: notes from the chat about an item
FEEDBACK_AUTHORS = ("human", "model")


def add_feedback(job_root: Path, round_id: str, item_id: str, *, human_id: str, author: str, text: str,
                 session_id: str = "") -> dict:
    """Append one note from the chat about an item; a note is never a label."""
    job_root = job_root.resolve()
    require_human_p1(job_root, human_id)
    round_path, batch = _round_for_judging(job_root, round_id)
    if item_id not in {str(row["item_id"]) for row in batch}:
        raise LabelingRefused("item is not in this round's frozen batch")
    if author not in FEEDBACK_AUTHORS:
        raise LabelingRefused(f"author must be one of {list(FEEDBACK_AUTHORS)}")
    text = " ".join(str(text or "").split())[:2000]
    if not text:
        raise LabelingRefused("feedback needs text")
    note = {"at": now_iso(), "round_id": round_id, "item_id": item_id, "author": author, "text": text,
            "human_id": human_id, "session_id": session_id}
    with _locked(round_path / "sessions" / ".lock"):
        with (round_path / "sessions" / FEEDBACK_FILE).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(note, sort_keys=True, ensure_ascii=False) + "\n")
    return note


def _close_calibration(job_root: Path, round_path: Path, batch: list[dict], states: dict,
                       run: str, config: dict) -> str:
    errors = verify_events(round_path)
    if errors:
        raise LabelingRefused("event chain failed verification: " + "; ".join(errors[:3]))
    policy_version = (yaml.safe_load((round_path / "manifest.yaml").read_text(encoding="utf-8")) or {}).get("policy_version")
    rows = []
    for row in batch:
        item_id = str(row["item_id"])
        entry = states[item_id]
        first, final = entry["first"], entry["final"]
        rows.append({
            "item_id": item_id,
            "round_id": round_path.name,
            "human_id": final["human_id"],
            "policy_version": policy_version,
            "first_pass": {"timestamp": first["at"], **first["payload"], "seq": first["seq"]},
            "final": {"timestamp": final["at"], **final["payload"], "seq": final["seq"]},
            "prelabel_comparison": {},
            "reference_comparison": (entry.get("reveal") or {}).get("payload", {}),
            "backward_impact_ids": [],
        })
    data = _jsonl_bytes(rows)
    job.write_once(round_path / "human_final.jsonl", data)
    readme = round_path / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8").replace("state: prepared", "state: judged")
        readme.write_text(text, encoding="utf-8")
    runtime = yaml.safe_load((job.results_dir(job_root) / run / "runtime.yaml").read_text(encoding="utf-8"))
    ticket = yaml.safe_load((job.runs_dir(job_root) / f"{run}.yaml").read_text(encoding="utf-8"))
    _write_run(
        job_root, run,
        operation="human-calibration", phase="P1", episode=round_path.name,
        target=round_target(_round_index(round_path.name)),
        commission=ticket["commission"],
        inputs=ticket["inputs"], worker=ticket["worker"],
        acceptance=ticket.get("acceptance") or CALIBRATION_ACCEPTANCE,  # the Ticket's own words, as written
        status="complete", started_at=runtime["started_at"], finished_at=now_iso(),
        outcome=f"{len(rows)} items judged",
        artifacts=[
            {"path": job.page_path(job_root, f"rounds/{round_path.name}/human_final.jsonl")},
            {"path": job.page_path(job_root, f"rounds/{round_path.name}/sessions/events.jsonl")},
        ],
    )
    return run


def finalize_calibration(job_root: Path, round_id: str, *, human_id: str) -> dict:
    """Finish a Run whose last final event was recorded before its Result closed."""
    job_root = job_root.resolve()
    require_human_p1(job_root, human_id)
    round_path, batch = _round_for_judging(job_root, round_id)
    with _locked(round_path / "sessions" / ".lock"):
        if not _find_run(job_root, "human-calibration", round_target(_round_index(round_id))):
            raise LabelingRefused("this round has no calibration Run to finalize")
        run = _ensure_calibration_run(job_root, round_path, human_id)
        states = _item_states(round_path)
        if any(not states.get(str(row["item_id"]), {}).get("final") for row in batch):
            raise LabelingRefused("the frozen batch still has items without final judgments")
        _close_calibration(job_root, round_path, batch, states, run, _config(job_root))
    return {"round_id": round_id, "run": run, "status": "complete", "finals": len(batch)}


# ── REVEAL: external reference observations, after lock only ────────────────


def reveal_for(job_root: Path, config: dict, item_id: str) -> dict:
    reveal = config.get("reveal") if isinstance(config.get("reveal"), dict) else {}
    ref = reveal.get("reference_observations") if isinstance(reveal.get("reference_observations"), dict) else None
    if not ref:
        return {"kind": "none", "note": "no comparison source for this job"}
    index = _reference_index(job_root, ref)
    return {"kind": "reference_observations", "label": ref.get("label") or "reference observations",
            "not_gold": True, **(index.get(item_id) or {"missing": True})}


def _reference_index(job_root: Path, ref: dict) -> dict:
    root = _repo_root(job_root) or job_root
    source = (root / str(ref.get("file") or "")).resolve()
    if not source.is_file():
        return {}
    # Read the source once, then key and build the index from the same bytes.
    # Size and mtime are not content identities: an in-place replacement can
    # preserve both and otherwise replay a stale reveal into an immutable event.
    # The hash below only names the cache file; it is never written to a record.
    source_bytes = source.read_bytes()
    corpus_path = job_root / "corpus" / "items.jsonl"
    corpus_bytes = corpus_path.read_bytes() if corpus_path.is_file() else b""
    key_material = {
        "source": str(source),
        "source_sha256": job.sha256_bytes(source_bytes),
        "corpus_sha256": job.sha256_bytes(corpus_bytes),
        "reference": ref,
    }
    key = job.sha256_bytes(
        json.dumps(
            key_material, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    )
    cache = job_root / "cache" / "reveal" / f"{key}.json"
    if cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))
    eligible = set(_eligible_ids(job_root))  # never index a sealed id
    id_field = str(ref.get("id_field") or "item_id")
    count_fields = [str(f) for f in ref.get("count_fields") or []]
    item_fields = [str(f) for f in ref.get("item_fields") or []]
    index: dict[str, dict] = {}
    for line in source_bytes.decode("utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        item_id = str(row.get(id_field))
        if item_id not in eligible:
            continue
        entry = index.setdefault(item_id, {"rows": 0, "counts": {f: {} for f in count_fields},
                                           "fields": {}})
        entry["rows"] += 1
        for field in count_fields:
            value = str(row.get(field))
            entry["counts"][field][value] = entry["counts"][field].get(value, 0) + 1
        for field in item_fields:
            entry["fields"].setdefault(field, row.get(field))
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(index, sort_keys=True), encoding="utf-8")
    return index


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="subjective-label P1 Round writer")
    sub = parser.add_subparsers(dest="command", required=True)
    state = sub.add_parser("state", help="derive rounds without writing")
    state.add_argument("--job-root", type=Path, required=True)
    verify = sub.add_parser("verify", help="check one round's event log")
    verify.add_argument("--job-root", type=Path, required=True)
    verify.add_argument("--round", required=True)
    finalize = sub.add_parser("finalize", help="close a fully judged calibration Run left running")
    finalize.add_argument("--job-root", type=Path, required=True)
    finalize.add_argument("--round", required=True)
    finalize.add_argument("--human-id", required=True)
    args = parser.parse_args()
    if args.command == "state":
        print(json.dumps(job_state(args.job_root), indent=2, sort_keys=True, ensure_ascii=False))
    elif args.command == "verify":
        errors = verify_events(args.job_root.resolve() / "rounds" / args.round)
        print(json.dumps({"round": args.round, "errors": errors, "ok": not errors}, indent=2))
    else:
        print(json.dumps(finalize_calibration(args.job_root, args.round, human_id=args.human_id),
                         indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
