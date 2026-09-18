#!/usr/bin/env python3
"""P1 Round writer for one subjective-label job: release, prepare, judge.

This module is the Building side's item-level writer.  It owns exactly three
things, in the order ``label-building-workflow`` gives them:

    CARD     the identified human releases a round card        card.md
    PREPARE  a random development draw is frozen               rlNN_round-prepare_round-NN
    JUDGE    show → first → lock → reveal → final, per item    rlNN_human-calibration_round-NN

Every judgment is an append-only, hash-chained event in
``rounds/round_NN/sessions/events.jsonl``.  Nothing here promotes gold or a
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


def _next_run_number(job_root: Path) -> int:
    seen = [0]
    for folder in ("runs", "results"):
        base = job_root / folder
        if not base.is_dir():
            continue
        for path in base.iterdir():
            hit = re.match(r"^rl(\d+)_", path.name)
            if hit:
                seen.append(int(hit.group(1)))
    return max(seen) + 1


def _run_name(job_root: Path, operation: str, target: str) -> str:
    return f"rl{_next_run_number(job_root):02d}_{operation}_{target}"


def _find_run(job_root: Path, operation: str, target: str) -> str | None:
    runs = job_root / "runs"
    if not runs.is_dir():
        return None
    hits = sorted(
        path.stem for path in runs.glob(f"rl*_{operation}_{target}.yaml")
        if re.match(rf"^rl\d+_{re.escape(operation)}_{re.escape(target)}$", path.stem)
    )
    return hits[-1] if hits else None


def _repo_root(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        if (parent / "pyproject.toml").is_file() and (parent / "code").is_dir():
            return parent
    return None


# ── authority ────────────────────────────────────────────────────────────────


def require_human_p1(job_root: Path, human_id: str) -> dict:
    """Only the identified human, after G0, on a job not on HOLD."""
    state = job.status(job_root)
    if state.get("hold"):
        raise LabelingRefused(f"HOLD · {state.get('hold_reason')}")
    if state["phase"] != "P1":
        raise LabelingRefused(f"{state['first_blocked_frontier']} · {state['next_action']}")
    if not human_id or human_id != state.get("human_id"):
        raise LabelingRefused("only the identified human semantic authority may label this job")
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
        runtime = job_root / "results" / calibration_run / "runtime.yaml"
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
    policy_manifest = job_root / "policy" / "versions" / policy_version / "manifest.yaml"
    items_checksum = job.sha256_file(job_root / "corpus" / "items.jsonl")
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
        "policy_manifest_checksum": job.sha256_file(policy_manifest) if policy_manifest.is_file() else None,
        "corpus_items_checksum": items_checksum,
        "development_pool_size": len(pool),
        "draw": {"method": "uniform-random", "n": size, "seed": draw_seed},
        "candidate_pool_checksum": job.sha256_bytes(pool_bytes),
        "human_batch_checksum": job.sha256_bytes(batch_bytes),
        "card_checksum": job.sha256_bytes(card),
        "prelabels": "none (round 1 has no weak executors)",
    }
    evidence = (
        f"# {round_dir_name(t)} · evidence\n\n"
        f"- policy {policy_version}: `{manifest['policy_manifest_checksum']}`\n"
        f"- corpus items: `{items_checksum}`\n"
        f"- development pool: {len(pool)} eligible items (sealed items excluded by population_status)\n"
        f"- prior gold D_00: empty\n"
        f"- human batch: `{manifest['human_batch_checksum']}`\n"
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
        commission={"path": f"rounds/{round_dir_name(t)}/card.md", "sha256": job.sha256_bytes(card)},
        inputs=[{"path": "corpus/items.jsonl", "sha256": items_checksum}],
        worker={"kind": "engine", "name": "subjective-label.engine.calibration:release_round"},
        acceptance="batch frozen with seed and inclusion probability before any show event",
        status="complete", started_at=released_at, finished_at=now_iso(),
        outcome=f"{size} items drawn from {len(pool)} eligible",
        artifacts=[{"path": f"rounds/{round_dir_name(t)}/{rel}",
                    "sha256": job.sha256_file(round_path / rel)} for rel in rels],
    )
    return {"round_id": round_dir_name(t), "run": run, "batch_size": size, "pool": len(pool)}


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
    job.write_once(job_root / "runs" / f"{run}.yaml", job.yaml_bytes(ticket))
    runtime = {
        "run": run, "family": "labeling", "operation": operation, "target": target,
        "status": status, "ticket": f"runs/{run}.yaml", "result": f"results/{run}/result.yaml",
        "inputs": inputs, "outcome": outcome, "worker": worker,
        "started_at": started_at, "finished_at": finished_at, "supersedes": None, "failure": None,
    }
    runtime_path = job_root / "results" / run / "runtime.yaml"
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.write_bytes(job.yaml_bytes(runtime))  # lifecycle file: running -> complete
    if status == "complete":
        result = {
            "run": run, "family": "labeling", "operation": operation, "status": "complete",
            "outcome": outcome, "artifacts": artifacts,
            "promotion": {"performed": False, "reason": "only round-close promotes gold and policy"},
        }
        job.write_once(job_root / "results" / run / "result.yaml", job.yaml_bytes(result))


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
        return run
    run = _run_name(job_root, "human-calibration", round_target(t))
    started = now_iso()
    _write_run(
        job_root, run,
        operation="human-calibration", phase="P1", episode=round_path.name, target=round_target(t),
        commission={"path": f"rounds/{round_path.name}/human_batch.jsonl",
                    "sha256": job.sha256_file(round_path / "human_batch.jsonl")},
        inputs=[{"path": f"rounds/{round_path.name}/manifest.yaml",
                 "sha256": job.sha256_file(round_path / "manifest.yaml")}],
        worker={"kind": "human", "name": human_id, "surface": "labeling screen"},
        acceptance="every batch row has a final event; human_final.jsonl rehashes",
        status="running", started_at=started, finished_at=None,
        outcome="judging", artifacts=[],
    )
    return run


def _append_event(round_path: Path, event: dict) -> dict:
    path = round_path / "sessions" / "events.jsonl"
    existing = _read_jsonl(path)
    prev = existing[-1]["checksum"] if existing else None
    record = {
        "schema": EVENTS_SCHEMA,
        "seq": len(existing) + 1,
        "at": now_iso(),
        "prev_checksum": prev,
        **event,
    }
    record["checksum"] = job.canonical_hash({k: v for k, v in record.items() if k != "checksum"})
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
    return record


def verify_events(round_path: Path) -> list[str]:
    """Rehash the chain; return every defect."""
    errors = []
    prev = None
    for index, record in enumerate(_events(round_path), start=1):
        body = {k: v for k, v in record.items() if k != "checksum"}
        if record.get("seq") != index:
            errors.append(f"event {index}: sequence gap")
        if record.get("prev_checksum") != prev:
            errors.append(f"event {index}: broken chain")
        if job.canonical_hash(body) != record.get("checksum"):
            errors.append(f"event {index}: checksum mismatch")
        prev = record.get("checksum")
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
    run = _ensure_calibration_run(job_root, round_path, human_id)
    with _locked(round_path / "sessions" / ".lock"):
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
    run = _ensure_calibration_run(job_root, round_path, human_id)
    with _locked(round_path / "sessions" / ".lock"):
        kinds = _item_states(round_path).get(item_id, {}).get("kinds", [])
        if "show" not in kinds:
            raise LabelingRefused("an item must be shown before its first judgment")
        if "first" in kinds:
            raise LabelingRefused("the first judgment is already locked for this item")
        base = {"run": run, "round_id": round_id, "item_id": item_id,
                "human_id": human_id, "session_id": session_id}
        first = _append_event(round_path, {**base, "kind": "first",
                                           "payload": {**judgment, "prelabels_visible": False}})
        _append_event(round_path, {**base, "kind": "lock",
                                   "payload": {"first_checksum": first["checksum"]}})
        comparison = reveal_for(job_root, config, item_id)
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
    run = _ensure_calibration_run(job_root, round_path, human_id)
    with _locked(round_path / "sessions" / ".lock"):
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
            "first_pass": {"timestamp": first["at"], **{k: v for k, v in first["payload"].items()},
                           "checksum": first["checksum"]},
            "final": {"timestamp": final["at"], **final["payload"], "checksum": final["checksum"]},
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
    runtime = yaml.safe_load((job_root / "results" / run / "runtime.yaml").read_text(encoding="utf-8"))
    _write_run(
        job_root, run,
        operation="human-calibration", phase="P1", episode=round_path.name,
        target=round_target(_round_index(round_path.name)),
        commission=yaml.safe_load((job_root / "runs" / f"{run}.yaml").read_text())["commission"],
        inputs=runtime["inputs"], worker=runtime["worker"],
        acceptance="every batch row has a final event; human_final.jsonl rehashes",
        status="complete", started_at=runtime["started_at"], finished_at=now_iso(),
        outcome=f"{len(rows)} items judged",
        artifacts=[
            {"path": f"rounds/{round_path.name}/human_final.jsonl", "sha256": job.sha256_bytes(data)},
            {"path": f"rounds/{round_path.name}/sessions/events.jsonl",
             "sha256": job.sha256_file(round_path / "sessions" / "events.jsonl")},
        ],
    )
    return run


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
    stat = source.stat()
    key = job.sha256_bytes(f"{source}|{stat.st_size}|{int(stat.st_mtime)}|{json.dumps(ref, sort_keys=True)}".encode())[:16]
    cache = job_root / "cache" / "reveal" / f"{key}.json"
    if cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))
    eligible = set(_eligible_ids(job_root))  # never index a sealed id
    id_field = str(ref.get("id_field") or "item_id")
    count_fields = [str(f) for f in ref.get("count_fields") or []]
    item_fields = [str(f) for f in ref.get("item_fields") or []]
    index: dict[str, dict] = {}
    with source.open("r", encoding="utf-8") as handle:
        for line in handle:
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
    verify = sub.add_parser("verify", help="rehash one round's event chain")
    verify.add_argument("--job-root", type=Path, required=True)
    verify.add_argument("--round", required=True)
    args = parser.parse_args()
    if args.command == "state":
        print(json.dumps(job_state(args.job_root), indent=2, sort_keys=True, ensure_ascii=False))
    else:
        errors = verify_events(args.job_root.resolve() / "rounds" / args.round)
        print(json.dumps({"round": args.round, "errors": errors, "ok": not errors}, indent=2))


if __name__ == "__main__":
    main()
