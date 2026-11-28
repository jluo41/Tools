#!/usr/bin/env python3
"""The decision-report store of one labeling job lane J: publish, draft, submit, read.

Every record lives under ``J/meaning/`` (s03 implementation-plan CONTRACTS.md version 2, sections 1, 5, 6
and 14); nothing here writes anywhere else:

    reports/<report_id>/vNN.json         one published report revision, immutable
    drafts/<report_id>/<actor_id>.json   one person's draft of one report, the only mutable record
    feedback/<submission_id>.json        one submitted bundle, immutable
    events/<NNNNNN>-<event_id>.json      one lifecycle event (published, submitted), immutable, numbered

A write holds the lane's lock (``J/meaning/.lock``, POSIX fcntl) and is atomic: a temp file in the same
folder, flushed and fsynced, then os.replace.  A refused call writes nothing.  A draft saves by
compare-and-swap on its draft_revision.  A submission is idempotent on its request_id: the same request,
compared by exact JSON value with the one first committed, returns the first receipt.  Submitting records
what the person said; it never changes a guideline, a label or a report.  Status is computed from the
committed records, never from an index, and an event a crash left unwritten is written at the next write.
No record carries a content hash: versions are explicit numbers.

The workbench loads this file by path, without the engine folder on sys.path, so the sibling
meaning_contracts.py is imported normally when it can be and loaded by path otherwise.  Its error classes are
exposed here (MeaningError, ValidationError, StaleRevision, DuplicateRequest), so a caller needs this module
alone.
"""

from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    import fcntl
except ImportError:  # not POSIX: reads still work, writes refuse with a MeaningError
    fcntl = None


def _load_contracts():
    """The sibling meaning_contracts.py: a normal import when that resolves to the sibling, else by path."""
    sibling = Path(__file__).resolve().with_name("meaning_contracts.py")
    try:
        import meaning_contracts as module
    except ImportError:
        module = None
    found = getattr(module, "__file__", None) if module is not None else None
    if found and Path(found).resolve() == sibling:
        return module
    spec = importlib.util.spec_from_file_location("haipipe_labeling_meaning_contracts", sibling)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {sibling}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contracts = _load_contracts()
MeaningError = contracts.MeaningError
ValidationError = contracts.ValidationError
StaleRevision = contracts.StaleRevision
DuplicateRequest = contracts.DuplicateRequest

DRAFT_SCHEMA = "labeling.decision_draft"
SUBMISSION_SCHEMA = "labeling.decision_submission"
EVENT_SCHEMA = "labeling.meaning_event"
SCHEMA_VERSION = 1
VERIFICATION_MODES = ("local_attestation", "authenticated_session")
LOCK_NAME = ".lock"

_REVISION_FILE = re.compile(r"v(\d{2,})\.json")
_SUBMISSION_FILE = re.compile(r"sub-(\d{6,})\.json")
_EVENT_FILE = re.compile(r"(\d{6,})-" + contracts.IDENTIFIER_PATTERN + r"\.json")
_ANSWERED = ("chosen", "rejected_options", "custom_proposal")


# ── paths, reads, atomic writes ──────────────────────────────────────────────


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _lane(J: Any) -> Path:
    if not isinstance(J, (str, os.PathLike)):
        raise ValidationError(f"J must be the path of a job lane, not {type(J).__name__}")
    return Path(J)


def _meaning(J: Any) -> Path:
    return _lane(J) / "meaning"


def _whole(value: Any, field: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValidationError(f"{field} must be a whole number >= {minimum}, not {value!r:.60}")
    return value


def _rel(meaning: Path, path: Path) -> str:
    try:
        return path.relative_to(meaning.parent).as_posix()
    except ValueError:
        return path.name


def _inside(meaning: Path, path: Path) -> Path:
    """Refuse a path that leaves J/meaning, for instance through a symlinked folder."""
    if meaning.is_symlink():
        raise MeaningError("refusing a symlinked J/meaning")
    root, target = meaning.resolve(), path.resolve()
    if target != root and root not in target.parents:
        raise MeaningError(f"refusing {_rel(meaning, path)}: it resolves outside J/meaning")
    return path


def _read_json(meaning: Path, path: Path) -> dict:
    _inside(meaning, path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        raise MeaningError(f"cannot read {_rel(meaning, path)}: {type(error).__name__}") from None
    if not isinstance(value, dict):
        raise MeaningError(f"{_rel(meaning, path)} does not hold an object")
    return value


def _fsync_folder(folder: Path) -> None:
    try:
        handle = os.open(folder, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(handle)
    except OSError:
        pass
    finally:
        os.close(handle)


def _write(meaning: Path, path: Path, record: dict, *, immutable: bool) -> None:
    """Write one record atomically: temp file in the same folder, flush, fsync, os.replace."""
    _inside(meaning, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or (immutable and path.exists()):
        raise MeaningError(f"refusing to overwrite {_rel(meaning, path)}")
    data = (json.dumps(record, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    descriptor, temp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(temp)
        raise
    _fsync_folder(path.parent)


@contextlib.contextmanager
def _locked(J: Any, *, create: bool) -> Iterator[Path]:
    """Hold the lane's one write lock, J/meaning/.lock; yield J/meaning."""
    meaning = _meaning(J)
    lock = meaning / LOCK_NAME
    if meaning.is_symlink() or lock.is_symlink():
        raise MeaningError("refusing a symlinked J/meaning or lock file")
    if fcntl is None:
        raise MeaningError("writing needs POSIX file locks (fcntl), which this platform lacks")
    if create:
        meaning.mkdir(parents=True, exist_ok=True)
    elif not meaning.is_dir():
        raise MeaningError("no decision report is published in this lane")
    with open(lock, "a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield meaning
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


# ── committed records ────────────────────────────────────────────────────────


def _revision_name(revision: int) -> str:
    return f"v{revision:02d}.json"


def _revisions(meaning: Path, report_id: str) -> list[int]:
    folder = meaning / "reports" / report_id
    if not folder.is_dir():
        return []
    found = []
    for path in folder.iterdir():
        hit = _REVISION_FILE.fullmatch(path.name)
        if hit and path.name == _revision_name(int(hit.group(1))) and path.is_file():
            found.append(int(hit.group(1)))
    return sorted(found)


def _report_ids(meaning: Path) -> list[str]:
    folder = meaning / "reports"
    if not folder.is_dir():
        return []
    return sorted(
        path.name for path in folder.iterdir()
        if contracts.is_identifier(path.name) and path.is_dir() and _revisions(meaning, path.name)
    )


def _stored_report(meaning: Path, report_id: str, revision: int | None = None) -> dict:
    revisions = _revisions(meaning, report_id)
    if not revisions:
        raise MeaningError(f"no published report {report_id!r}")
    if revision is None:
        revision = revisions[-1]
    elif revision not in revisions:
        raise MeaningError(f"report {report_id!r} has no published revision {revision}")
    path = meaning / "reports" / report_id / _revision_name(revision)
    record = _read_json(meaning, path)
    try:
        report = contracts.validate_report(record)
    except ValidationError as error:
        raise MeaningError(f"{_rel(meaning, path)} is not a valid report: {error}") from None
    if report["report_id"] != report_id or report["report_revision"] != revision:
        raise MeaningError(f"{_rel(meaning, path)} holds another report than its address names")
    return report


def _draft_path(meaning: Path, report_id: str, actor_id: str) -> Path:
    return meaning / "drafts" / report_id / f"{actor_id}.json"


def _stored_draft(meaning: Path, report_id: str, actor_id: str) -> dict | None:
    path = _draft_path(meaning, report_id, actor_id)
    if not path.is_file():
        return None
    draft = _read_json(meaning, path)
    stored_actor = draft.get("actor_id")
    if stored_actor != actor_id:
        if isinstance(stored_actor, str) and stored_actor.lower() == actor_id.lower():
            raise ValidationError(f"actor_id {actor_id!r} and the stored draft of {stored_actor!r} differ only "
                                  "by letter case and share one file on this disk; use the same spelling")
        raise MeaningError(f"{_rel(meaning, path)} holds another person's draft than its address names")
    revision = draft.get("draft_revision")
    if draft.get("report_id") != report_id or isinstance(revision, bool) or not isinstance(revision, int) \
            or revision < 1:
        raise MeaningError(f"{_rel(meaning, path)} is not a valid draft")
    return draft


def _drafts(meaning: Path, report_id: str) -> list[dict]:
    folder = meaning / "drafts" / report_id
    if not folder.is_dir():
        return []
    return [
        _read_json(meaning, path) for path in sorted(folder.iterdir())
        if path.suffix == ".json" and contracts.is_identifier(path.stem) and path.is_file()
    ]


def _bundle_paths(meaning: Path) -> list[tuple[int, Path]]:
    folder = meaning / "feedback"
    if not folder.is_dir():
        return []
    numbered = []
    for path in folder.iterdir():
        hit = _SUBMISSION_FILE.fullmatch(path.name)
        if hit and path.is_file():
            numbered.append((int(hit.group(1)), path))
    return sorted(numbered)


def _bundles(meaning: Path) -> list[dict]:
    return [_read_json(meaning, path) for _, path in _bundle_paths(meaning)]


def _event_paths(meaning: Path) -> list[tuple[int, Path]]:
    folder = meaning / "events"
    if not folder.is_dir():
        return []
    numbered = []
    for path in folder.iterdir():
        hit = _EVENT_FILE.fullmatch(path.name)
        if hit and path.is_file():
            numbered.append((int(hit.group(1)), path))
    return sorted(numbered)


# ── lifecycle events ─────────────────────────────────────────────────────────


def _report_target(report: dict) -> dict:
    return {"kind": "report", "report_id": report["report_id"], "report_revision": report["report_revision"]}


def _submission_target(bundle: dict) -> dict:
    return {"kind": "submission", "submission_id": bundle["submission_id"], "report_id": bundle["report_id"],
            "report_revision": bundle["report_revision"]}


def _event_key(event: dict) -> tuple:
    target = event.get("target") if isinstance(event.get("target"), dict) else {}
    if target.get("kind") == "report":
        return event.get("transition"), "report", target.get("report_id"), target.get("report_revision")
    return event.get("transition"), "submission", target.get("submission_id")


def _append_event(meaning: Path, *, job_id: str, transition: str, actor: str, target: dict, reason: str,
                  repaired: bool = False) -> dict:
    """Write the next numbered event; prior_event_id is the previous event about the same report."""
    numbered = _event_paths(meaning)
    sequence = numbered[-1][0] + 1 if numbered else 1
    prior = None
    for _, path in reversed(numbered):
        earlier = _read_json(meaning, path)
        if isinstance(earlier.get("target"), dict) and earlier["target"].get("report_id") == target["report_id"]:
            prior = earlier.get("event_id")
            break
    event_id = f"evt-{uuid.uuid4().hex}"
    record = {
        "schema": EVENT_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "job_id": job_id,
        "event_id": event_id,
        "sequence": sequence,
        "transition": transition,
        "actor": actor,
        "created_at": _now(),
        "target": target,
        "prior_event_id": prior,
        "reason": reason,
        "repaired": repaired,
    }
    _write(meaning, meaning / "events" / f"{sequence:06d}-{event_id}.json", record, immutable=True)
    return record


def _ensure_events(meaning: Path) -> None:
    """Write the missing event of any committed report or submission (a crash between record and event)."""
    seen = {_event_key(_read_json(meaning, path)) for _, path in _event_paths(meaning)}
    for report_id in _report_ids(meaning):
        for revision in _revisions(meaning, report_id):
            if ("published", "report", report_id, revision) not in seen:
                report = _stored_report(meaning, report_id, revision)
                _append_event(meaning, job_id=report["job_id"], transition="published",
                              actor=report["publication_actor"], target=_report_target(report),
                              reason="repaired: the published report had no event", repaired=True)
    for bundle in _bundles(meaning):
        if ("submitted", "submission", bundle.get("submission_id")) not in seen:
            _append_event(meaning, job_id=bundle["job_id"], transition="submitted",
                          actor=bundle["actor"]["principal_id"], target=_submission_target(bundle),
                          reason="repaired: the received submission had no event", repaired=True)


# ── public API ───────────────────────────────────────────────────────────────


def publish_report(J: Path, report: dict, actor: str) -> dict:
    """Publish one immutable report revision at J/meaning/reports/<report_id>/vNN.json.

    The store stamps ``published_at`` (the real clock, UTC) and ``publication_actor`` (``actor``) over
    whatever the input carried, then validates the report.  The revision must be the next one: a published
    or older revision raises StaleRevision (nothing is ever overwritten), a skipped one ValidationError.  One
    lane holds one job.  Writes the report and a "published" event; returns
    ``{"report_id", "report_revision", "path"}``, the path relative to J.
    """
    lane = _lane(J)
    contracts.validate_identifier(actor, "actor")
    if not isinstance(report, dict):
        raise ValidationError("report must be an object")
    record = contracts.validate_report(dict(report, published_at=_now(), publication_actor=actor))
    report_id, revision = record["report_id"], record["report_revision"]
    with _locked(lane, create=True) as meaning:
        for other in _report_ids(meaning):
            if other != report_id and other.lower() == report_id.lower():
                raise ValidationError(f"report_id {report_id!r} differs from the published {other!r} only by "
                                      "letter case")
            stored = _stored_report(meaning, other)
            if stored["job_id"] != record["job_id"]:
                raise ValidationError(f"this lane holds job {stored['job_id']!r}; a report of job "
                                      f"{record['job_id']!r} belongs in its own lane")
        revisions = _revisions(meaning, report_id)
        newest = revisions[-1] if revisions else 0
        if revision <= newest:
            raise StaleRevision(f"report {report_id} v{revision:02d} is already published or superseded; "
                                f"the next revision is {newest + 1}")
        if revision != newest + 1:
            raise ValidationError(f"the next revision of report {report_id} is {newest + 1}, not {revision}")
        _ensure_events(meaning)
        path = meaning / "reports" / report_id / _revision_name(revision)
        _write(meaning, path, record, immutable=True)
        _append_event(meaning, job_id=record["job_id"], transition="published", actor=actor,
                      target=_report_target(record), reason=f"report {report_id} v{revision:02d} published")
    return {"report_id": report_id, "report_revision": revision, "path": path.relative_to(lane).as_posix()}


def load_report(J: Path, report_id: str, revision: int | None = None) -> dict:
    """Return one published report: its newest revision when ``revision`` is None.  Missing: MeaningError."""
    contracts.validate_identifier(report_id, "report_id")
    if revision is not None:
        _whole(revision, "revision", 1)
    return _stored_report(_meaning(J), report_id, revision)


def list_reports(J: Path) -> list[dict]:
    """One summary per report (its newest revision), sorted by round_id then report_id.

    ``status`` comes from the records bound to that newest revision: "submitted" when a submission exists,
    "draft" when only a draft does, else "open".  ``counts`` (answered, deferred, waiting) come from the
    newest submission, else the most recently saved draft, else every card waits.
    """
    meaning = _meaning(J)
    if not meaning.is_dir():
        return []
    bundles = _bundles(meaning)
    summaries = []
    for report_id in _report_ids(meaning):
        report = _stored_report(meaning, report_id)
        revision = report["report_revision"]
        submitted = [b for b in bundles if b.get("report_id") == report_id and b.get("report_revision") == revision]
        drafts = [d for d in _drafts(meaning, report_id) if d.get("report_revision") == revision]
        if submitted:
            status, dispositions = "submitted", list(submitted[-1]["dispositions"].values())
        elif drafts:
            newest = max(drafts, key=lambda d: (_when(d.get("last_saved_at")), str(d.get("actor_id"))))
            status = "draft"
            dispositions = [contracts.DISPOSITIONS[a["kind"]] for a in newest["answers"].values()]
        else:
            status, dispositions = "open", ["unanswered"] * len(report["cards"])
        summaries.append({
            "report_id": report_id,
            "report_revision": revision,
            "round_id": report["round_id"],
            "title": report["title"],
            "published_at": report["published_at"],
            "cards": len(report["cards"]),
            "status": status,
            "counts": {
                "answered": sum(d in _ANSWERED for d in dispositions),
                "deferred": sum(d == "deferred" for d in dispositions),
                "waiting": sum(d == "unanswered" for d in dispositions),
            },
        })
    return sorted(summaries, key=lambda s: (s["round_id"], s["report_id"]))


def _when(value: Any) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def load_draft(J: Path, report_id: str, actor_id: str) -> dict | None:
    """Return this person's draft of this report, or None.  It may be bound to an older report revision."""
    contracts.validate_identifier(report_id, "report_id")
    contracts.validate_identifier(actor_id, "actor_id")
    meaning = _meaning(J)
    if not meaning.is_dir():
        return None
    return _stored_draft(meaning, report_id, actor_id)


def save_draft(J: Path, report_id: str, report_revision: int, actor_id: str, answers: dict,
               expected_draft_revision: int, comments: str = "") -> dict:
    """Save this person's draft by compare-and-swap, and return the new draft.

    ``expected_draft_revision`` must equal the stored draft_revision (0 when there is none), else
    StaleRevision: another tab saved first.  The draft is bound to ``report_revision``, which must be the
    newest published revision, else StaleRevision.  Answers are validated against that revision; answers and
    comments are kept exactly as given.  Saving a draft approves nothing.
    """
    lane = _lane(J)
    contracts.validate_identifier(report_id, "report_id")
    contracts.validate_identifier(actor_id, "actor_id")
    _whole(report_revision, "report_revision", 1)
    _whole(expected_draft_revision, "expected_draft_revision", 0)
    if not isinstance(comments, str) or len(comments) > contracts.MAX_TEXT:
        raise ValidationError(f"comments must be text of at most {contracts.MAX_TEXT} characters")
    if not _revisions(_meaning(lane), report_id):
        raise MeaningError(f"no published report {report_id!r}")
    with _locked(lane, create=False) as meaning:
        report = _stored_report(meaning, report_id, report_revision)
        normalized = contracts.validate_answers(report, answers)
        newest = _revisions(meaning, report_id)[-1]
        if report_revision != newest:
            raise StaleRevision(f"report {report_id} v{report_revision:02d} was superseded by v{newest:02d}; "
                                "reload it before saving")
        stored = _stored_draft(meaning, report_id, actor_id)
        current = stored["draft_revision"] if stored else 0
        if expected_draft_revision != current:
            raise StaleRevision(f"the draft is at revision {current}, not {expected_draft_revision}: "
                                "another tab saved first; reload it")
        now = _now()
        draft = {
            "schema": DRAFT_SCHEMA,
            "schema_version": SCHEMA_VERSION,
            "job_id": report["job_id"],
            "report_id": report_id,
            "report_revision": report_revision,
            "actor_id": actor_id,
            "draft_revision": current + 1,
            "answers": normalized,
            "comments": comments,
            "base_meaning_version": report["base"]["meaning_version"],
            "created_at": stored.get("created_at", now) if stored else now,
            "last_saved_at": now,
        }
        _write(meaning, _draft_path(meaning, report_id, actor_id), draft, immutable=False)
    return draft


def _receipt(bundle: dict) -> dict:
    return {"submission_id": bundle["submission_id"], "request_id": bundle["request_id"],
            "status": bundle["status"], "submitted_at": bundle["submitted_at"]}


def submit_feedback(J: Path, report_id: str, report_revision: int, actor_id: str, request_id: str,
                    answers: dict, confirmed: bool, verification_mode: str = "local_attestation") -> dict:
    """Receive one person's confirmed answers as an immutable bundle; return its receipt.

    Needs ``confirmed`` True.  The request_id is looked up first: the same request (report, revision, actor,
    verification mode and normalized answers, compared by exact JSON value) returns its original receipt,
    even after the draft advanced or the report was superseded; a different request under that id raises
    DuplicateRequest.  A new request must answer the newest revision, else StaleRevision.  Unanswered cards
    stay open.  The bundle at J/meaning/feedback/<submission_id>.json keeps each card's visible options, the
    dispositions and the bound draft's comments; a "submitted" event follows.  Nothing else changes: no
    guideline, no label, no report.  Returns ``{"submission_id", "request_id", "status", "submitted_at"}``.
    """
    lane = _lane(J)
    contracts.validate_identifier(report_id, "report_id")
    contracts.validate_identifier(actor_id, "actor_id")
    contracts.validate_identifier(request_id, "request_id")
    _whole(report_revision, "report_revision", 1)
    if confirmed is not True:
        raise ValidationError("a submission needs the person's explicit confirmation (confirmed=True)")
    if verification_mode not in VERIFICATION_MODES:
        raise ValidationError(f"verification_mode must be one of {', '.join(VERIFICATION_MODES)}, "
                              f"not {verification_mode!r:.60}")
    if not _revisions(_meaning(lane), report_id):
        raise MeaningError(f"no published report {report_id!r}")
    with _locked(lane, create=False) as meaning:
        report = _stored_report(meaning, report_id, report_revision)
        normalized = contracts.validate_answers(report, answers)
        request = {"report_id": report_id, "report_revision": report_revision, "principal_id": actor_id,
                   "verification_mode": verification_mode, "answers": normalized}
        numbered = _bundle_paths(meaning)
        for _, path in numbered:
            committed = _read_json(meaning, path)
            if committed.get("request_id") == request_id:
                if committed.get("request") != request:
                    raise DuplicateRequest(f"request {request_id} already committed a different submission; "
                                           "a new submission needs a new request id")
                _ensure_events(meaning)
                return _receipt(committed)
        newest = _revisions(meaning, report_id)[-1]
        if report_revision != newest:
            raise StaleRevision(f"report {report_id} v{report_revision:02d} was superseded by v{newest:02d}; "
                                "reload it before submitting")
        draft = _stored_draft(meaning, report_id, actor_id)
        bound = draft if draft is not None and draft.get("report_revision") == report_revision else None
        number = numbered[-1][0] + 1 if numbered else 1
        submission_id = f"sub-{number:06d}"
        snapshot = {}
        for card in report["cards"]:
            snapshot[card["decision_id"]] = dict(normalized[card["decision_id"]], card={
                "short_title": card["short_title"],
                "question": card["question"],
                "question_type": card["question_type"],
                "approval_scope": card["approval_scope"],
                "options": [dict(option) for option in card["options"]],
                "source_ids": list(card["source_ids"]),
                "evidence_refs": [{"item_ref": row["item_ref"], "split": row["split"], "role": row["role"]}
                                  for row in card["evidence"]],
                "origin": card["origin"],
            })
        bundle = {
            "schema": SUBMISSION_SCHEMA,
            "schema_version": SCHEMA_VERSION,
            "job_id": report["job_id"],
            "submission_id": submission_id,
            "request_id": request_id,
            "report_id": report_id,
            "report_revision": report_revision,
            "draft_revision": bound["draft_revision"] if bound else 0,
            "actor": {"principal_id": actor_id, "verification_mode": verification_mode},
            "base": dict(report["base"]),
            "request": request,
            "answers": snapshot,
            "dispositions": {d: contracts.DISPOSITIONS[a["kind"]] for d, a in normalized.items()},
            "comments": bound.get("comments", "") if bound else "",
            "confirmed": True,
            "synthetic": report["synthetic"],
            "submitted_at": _now(),
            "status": "received",
        }
        _ensure_events(meaning)
        _write(meaning, meaning / "feedback" / f"{submission_id}.json", bundle, immutable=True)
        _append_event(meaning, job_id=report["job_id"], transition="submitted", actor=actor_id,
                      target=_submission_target(bundle), reason=f"feedback {submission_id} received")
    return _receipt(bundle)


def read_submission(J: Path, submission_id: str) -> dict:
    """Return one submitted bundle.  Missing: MeaningError."""
    contracts.validate_identifier(submission_id, "submission_id")
    meaning = _meaning(J)
    path = meaning / "feedback" / f"{submission_id}.json"
    if not _SUBMISSION_FILE.fullmatch(path.name) or not path.is_file():
        raise MeaningError(f"no submission {submission_id!r}")
    bundle = _read_json(meaning, path)
    if bundle.get("submission_id") != submission_id:
        raise MeaningError(f"{_rel(meaning, path)} holds another submission than its address names")
    return bundle


def list_submissions(J: Path, report_id: str) -> list[dict]:
    """Every submitted bundle of one report, any revision, oldest first."""
    contracts.validate_identifier(report_id, "report_id")
    return [bundle for bundle in _bundles(_meaning(J)) if bundle.get("report_id") == report_id]


def list_events(J: Path) -> list[dict]:
    """Every lifecycle event of the lane, in sequence order."""
    meaning = _meaning(J)
    return [_read_json(meaning, path) for _, path in _event_paths(meaning)]
