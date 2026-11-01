from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("labeling_meaning_store_test", HERE / "meaning_store.py")
assert SPEC and SPEC.loader
store = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(store)

DEMO = HERE / "fixtures" / "decision_report_demo.json"
CHOSEN = {"D01": {"kind": "chosen", "option_id": "A", "comment": "  only for adults  "}}


def demo(**changes) -> dict:
    report = json.loads(DEMO.read_text(encoding="utf-8"))
    report.update(changes)
    return report


def revised(report: dict, revision: int = 2) -> dict:
    """The report as its next revision, with card D01's option ids changed (A becomes A2)."""
    report = copy.deepcopy(report)
    report["report_revision"] = revision
    for option in report["cards"][0]["options"]:
        option["option_id"] += "2"
    return report


def lane(tmp_path: Path) -> Path:
    return tmp_path / "Project-X" / "t03_demo_building" / "labeling"


def published(tmp_path: Path, report: dict | None = None) -> Path:
    J = lane(tmp_path)
    store.publish_report(J, report if report is not None else demo(), "meaning-agent")
    return J


def files(root: Path) -> dict[str, bytes]:
    """Every file under root but the lock, with its bytes."""
    if not root.exists():
        return {}
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(root.rglob("*"))
            if path.is_file() and not path.name.endswith(".lock")}


def submit(J: Path, request_id: str = "req-0001-demo", answers: dict | None = None, actor: str = "Reviewer-One",
           revision: int = 1, report_id: str = "report-01") -> dict:
    return store.submit_feedback(J, report_id, revision, actor, request_id,
                                 copy.deepcopy(CHOSEN if answers is None else answers), True)


# ── publish, load, list ──────────────────────────────────────────────────────


def test_publish_then_load_and_list(tmp_path: Path) -> None:
    J = lane(tmp_path)
    before = datetime.now(timezone.utc)
    receipt = store.publish_report(J, demo(), "meaning-agent")
    assert receipt == {"report_id": "report-01", "report_revision": 1, "path": "meaning/reports/report-01/v01.json"}

    report = store.load_report(J, "report-01")
    assert report == json.loads((J / receipt["path"]).read_text(encoding="utf-8"))
    assert report == store.load_report(J, "report-01", 1)
    assert report["publication_actor"] == "meaning-agent"          # the store stamps who published, and when
    published_at = datetime.fromisoformat(report["published_at"])
    assert published_at.tzinfo is not None and before <= published_at <= datetime.now(timezone.utc)
    stamped = ("published_at", "publication_actor")
    assert {k: v for k, v in report.items() if k not in stamped} == {k: v for k, v in demo().items()
                                                                       if k not in stamped}

    assert store.list_reports(J) == [{
        "report_id": "report-01", "report_revision": 1, "round_id": "round-01", "title": demo()["title"],
        "published_at": report["published_at"], "cards": 6, "status": "open",
        "counts": {"answered": 0, "deferred": 0, "waiting": 6},
    }]
    [event] = store.list_events(J)
    assert (event["sequence"], event["transition"], event["actor"], event["repaired"]) == \
        (1, "published", "meaning-agent", False)
    assert event["target"] == {"kind": "report", "report_id": "report-01", "report_revision": 1}
    assert sorted(files(J)) == [f"meaning/events/000001-{event['event_id']}.json",
                                "meaning/reports/report-01/v01.json"]


def test_a_published_revision_is_never_overwritten_or_skipped(tmp_path: Path) -> None:
    J = published(tmp_path)
    first = files(J)
    with pytest.raises(store.StaleRevision, match="already published"):
        store.publish_report(J, demo(title="Changed in place"), "meaning-agent")
    with pytest.raises(store.ValidationError, match="next revision of report report-01 is 2, not 3"):
        store.publish_report(J, revised(demo(), 3), "meaning-agent")
    assert files(J) == first

    store.publish_report(J, revised(demo()), "meaning-agent")
    with pytest.raises(store.StaleRevision):
        store.publish_report(J, demo(), "meaning-agent")             # v01 is older than the newest
    assert store.load_report(J, "report-01")["report_revision"] == 2
    assert store.load_report(J, "report-01", 1)["cards"][0]["options"][0]["option_id"] == "A"
    assert (J / "meaning/reports/report-01/v01.json").read_bytes() == first["meaning/reports/report-01/v01.json"]


def test_an_invalid_report_is_refused_before_anything_is_written(tmp_path: Path) -> None:
    J = lane(tmp_path)
    preselected = demo()
    preselected["cards"][0]["options"][0]["selected"] = True
    with pytest.raises(store.ValidationError, match="never preselected"):
        store.publish_report(J, preselected, "meaning-agent")
    with pytest.raises(store.ValidationError, match="actor must match"):
        store.publish_report(J, demo(), "../agent")
    with pytest.raises(store.ValidationError, match="report must be an object"):
        store.publish_report(J, [demo()], "meaning-agent")
    assert not (tmp_path / "Project-X").exists()


def test_one_lane_holds_one_job(tmp_path: Path) -> None:
    J = published(tmp_path)
    with pytest.raises(store.ValidationError, match="this lane holds job 'demo_job'"):
        store.publish_report(J, demo(job_id="other_job", report_id="report-02"), "meaning-agent")
    with pytest.raises(store.ValidationError, match="only by letter case"):
        store.publish_report(J, demo(report_id="Report-01"), "meaning-agent")
    store.publish_report(J, demo(report_id="report-02"), "meaning-agent")
    assert [summary["report_id"] for summary in store.list_reports(J)] == ["report-01", "report-02"]


def test_missing_records_raise_a_plain_meaning_error(tmp_path: Path) -> None:
    empty = lane(tmp_path)
    assert store.list_reports(empty) == [] and store.list_submissions(empty, "report-01") == []
    assert store.load_draft(empty, "report-01", "Reviewer-One") is None and store.list_events(empty) == []
    for call in (
        lambda: store.load_report(empty, "report-01"),
        lambda: store.read_submission(empty, "sub-000001"),
        lambda: store.save_draft(empty, "report-01", 1, "Reviewer-One", {}, 0),
        lambda: submit(empty),
    ):
        with pytest.raises(store.MeaningError) as caught:
            call()
        assert not isinstance(caught.value, store.ValidationError)   # the workbench answers 404, not 422
    assert not (tmp_path / "Project-X").exists()                     # a refusal writes nothing

    J = published(tmp_path)
    with pytest.raises(store.MeaningError, match="no published revision 2"):
        store.load_report(J, "report-01", 2)
    with pytest.raises(store.MeaningError, match="no published report 'report-02'"):
        store.save_draft(J, "report-02", 1, "Reviewer-One", {}, 0)
    with pytest.raises(store.MeaningError, match="no submission 'sub-000009'"):
        store.read_submission(J, "sub-000009")


# ── drafts ───────────────────────────────────────────────────────────────────


def test_two_tabs_cannot_overwrite_each_other(tmp_path: Path) -> None:
    J = published(tmp_path)
    assert store.load_draft(J, "report-01", "Reviewer-One") is None
    tab_a = store.save_draft(J, "report-01", 1, "Reviewer-One", CHOSEN, 0, comments="first tab")
    assert (tab_a["draft_revision"], tab_a["report_revision"], tab_a["actor_id"]) == (1, 1, "Reviewer-One")
    assert (tab_a["schema"], tab_a["job_id"], tab_a["base_meaning_version"]) == \
        ("labeling.decision_draft", "demo_job", "m01")
    assert tab_a["created_at"] == tab_a["last_saved_at"] and tab_a["comments"] == "first tab"
    assert list(tab_a["answers"]) == ["D01", "D02", "D03", "D04", "D05", "D06"]

    saved = files(J)
    with pytest.raises(store.StaleRevision, match="another tab saved first"):
        store.save_draft(J, "report-01", 1, "Reviewer-One", {"D01": {"kind": "defer"}}, 0, comments="tab B")
    assert files(J) == saved and store.load_draft(J, "report-01", "Reviewer-One") == tab_a

    tab_a2 = store.save_draft(J, "report-01", 1, "Reviewer-One", {"D02": {"kind": "defer"}}, 1)
    assert tab_a2["draft_revision"] == 2 and tab_a2["created_at"] == tab_a["created_at"]
    assert datetime.fromisoformat(tab_a2["last_saved_at"]) >= datetime.fromisoformat(tab_a["last_saved_at"])
    assert tab_a2["answers"]["D01"]["kind"] == "unanswered" and tab_a2["answers"]["D02"]["kind"] == "defer"
    assert store.save_draft(J, "report-01", 1, "Reviewer-Two", CHOSEN, 0)["draft_revision"] == 1

    for bad in (-1, True, "1", None):
        with pytest.raises(store.ValidationError, match="expected_draft_revision"):
            store.save_draft(J, "report-01", 1, "Reviewer-One", {}, bad)


def test_a_save_race_has_exactly_one_winner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    J = published(tmp_path)
    start = threading.Barrier(2)
    read = store._stored_draft

    def slow_read(*args):
        draft = read(*args)
        time.sleep(0.01)                                              # widen the window between read and write
        return draft

    monkeypatch.setattr(store, "_stored_draft", slow_read)

    def save(kind: str):
        start.wait()
        try:
            return store.save_draft(J, "report-01", 1, "Reviewer-One", {"D01": {"kind": kind}}, 0)
        except store.StaleRevision as error:
            return error

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(save, ["defer", "unanswered"]))
    winners = [outcome for outcome in outcomes if isinstance(outcome, dict)]
    assert len(winners) == 1 and sum(isinstance(outcome, store.StaleRevision) for outcome in outcomes) == 1
    assert store.load_draft(J, "report-01", "Reviewer-One") == winners[0]


def test_answers_are_bound_to_the_newest_report_revision(tmp_path: Path) -> None:
    J = published(tmp_path)
    store.save_draft(J, "report-01", 1, "Reviewer-One", CHOSEN, 0)
    store.publish_report(J, revised(demo()), "meaning-agent")
    saved = files(J)
    with pytest.raises(store.StaleRevision, match="superseded by v02"):
        store.save_draft(J, "report-01", 1, "Reviewer-One", CHOSEN, 1)
    with pytest.raises(store.StaleRevision, match="superseded by v02"):
        submit(J, "req-old-tab-01")
    with pytest.raises(store.ValidationError, match="names one option of this card"):
        store.save_draft(J, "report-01", 2, "Reviewer-One", CHOSEN, 1)   # old option A is never mapped onto A2
    assert files(J) == saved

    stale = store.load_draft(J, "report-01", "Reviewer-One")             # still recoverable, still on v01
    assert stale["report_revision"] == 1 and stale["answers"]["D01"]["option_id"] == "A"
    rebased = store.save_draft(J, "report-01", 2, "Reviewer-One", {"D01": {"kind": "chosen", "option_id": "A2"}}, 1)
    assert (rebased["report_revision"], rebased["draft_revision"]) == (2, 2)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX file locks")
def test_a_case_variant_actor_cannot_take_another_persons_draft(tmp_path: Path) -> None:
    probe = tmp_path / "CaseProbe"
    probe.write_text("")
    if not (tmp_path / "caseprobe").exists():
        pytest.skip("this filesystem tells letter case apart, so the two actors have two files")
    J = published(tmp_path)
    store.save_draft(J, "report-01", 1, "Reviewer-One", CHOSEN, 0)
    with pytest.raises(store.ValidationError, match="only by letter case"):
        store.save_draft(J, "report-01", 1, "reviewer-one", {}, 1)
    with pytest.raises(store.ValidationError, match="only by letter case"):
        store.load_draft(J, "report-01", "reviewer-one")


# ── submissions ──────────────────────────────────────────────────────────────


def test_a_repeated_submit_returns_one_receipt_and_one_bundle(tmp_path: Path) -> None:
    J = published(tmp_path)
    first = submit(J)
    assert set(first) == {"submission_id", "request_id", "status", "submitted_at"}
    assert (first["request_id"], first["status"]) == ("req-0001-demo", "received")
    assert submit(J) == first
    assert [bundle["submission_id"] for bundle in store.list_submissions(J, "report-01")] == [first["submission_id"]]
    assert [event["transition"] for event in store.list_events(J)] == ["published", "submitted"]

    saved = files(J)
    with pytest.raises(store.DuplicateRequest):
        submit(J, answers={"D01": {"kind": "defer"}})
    with pytest.raises(store.DuplicateRequest):                       # an edited comment is another request
        submit(J, answers={"D01": dict(CHOSEN["D01"], comment="only for adults")})
    with pytest.raises(store.DuplicateRequest):                       # another person cannot claim its receipt
        submit(J, actor="Reviewer-Two")
    assert files(J) == saved
    assert store.read_submission(J, first["submission_id"])["submitted_at"] == first["submitted_at"]


def test_a_lost_response_is_recovered_after_the_draft_advanced_and_the_report_moved_on(tmp_path: Path) -> None:
    J = published(tmp_path)
    receipt = submit(J, "req-lost-0001")
    store.save_draft(J, "report-01", 1, "Reviewer-One", {"D02": {"kind": "defer"}}, 0)
    store.publish_report(J, revised(demo()), "meaning-agent")
    assert submit(J, "req-lost-0001") == receipt
    assert len(store.list_submissions(J, "report-01")) == 1
    with pytest.raises(store.StaleRevision):                          # a new request needs the newest revision
        submit(J, "req-new-00002")


@pytest.mark.parametrize("confirmed", [False, None, 1, "yes", "true"])
def test_submitting_needs_explicit_confirmation(tmp_path: Path, confirmed) -> None:
    J = published(tmp_path)
    saved = files(J)
    with pytest.raises(store.ValidationError, match="explicit confirmation"):
        store.submit_feedback(J, "report-01", 1, "Reviewer-One", "req-0001-demo", CHOSEN, confirmed)
    with pytest.raises(store.ValidationError, match="verification_mode"):
        store.submit_feedback(J, "report-01", 1, "Reviewer-One", "req-0001-demo", CHOSEN, True, "verified_identity")
    assert files(J) == saved and store.list_submissions(J, "report-01") == []


def test_a_partial_submission_keeps_every_card_and_the_options_it_showed(tmp_path: Path) -> None:
    J = published(tmp_path)
    store.save_draft(J, "report-01", 1, "Reviewer-One", {"D01": {"kind": "defer"}}, 0,
                     comments="Mostly I care about tone.")
    answers = {
        "D01": {"kind": "chosen", "option_id": "A", "comment": "  only for adults  "},
        "D02": {"kind": "reject_options", "comment": "Neither; it depends on the person."},
        "D03": {"kind": "custom", "text": "Ask for the earlier message first."},
        "D04": {"kind": "defer"},
    }
    receipt = submit(J, "req-partial-01", answers)
    bundle = store.read_submission(J, receipt["submission_id"])
    assert bundle["dispositions"] == {"D01": "chosen", "D02": "rejected_options", "D03": "custom_proposal",
                                      "D04": "deferred", "D05": "unanswered", "D06": "unanswered"}
    assert (bundle["schema"], bundle["job_id"], bundle["status"], bundle["confirmed"], bundle["synthetic"]) == \
        ("labeling.decision_submission", "demo_job", "received", True, True)
    assert bundle["actor"] == {"principal_id": "Reviewer-One", "verification_mode": "local_attestation"}
    assert (bundle["report_id"], bundle["report_revision"], bundle["draft_revision"]) == ("report-01", 1, 1)
    assert bundle["base"] == demo()["base"] and bundle["comments"] == "Mostly I care about tone."
    assert bundle["request_id"] == "req-partial-01" and bundle["submitted_at"] == receipt["submitted_at"]
    for index, decision_id in enumerate(["D01", "D02", "D03", "D04", "D05", "D06"]):
        seen = bundle["answers"][decision_id]["card"]
        assert seen["options"] == demo()["cards"][index]["options"]    # the exact labels the person saw
        assert seen["approval_scope"] == demo()["cards"][index]["approval_scope"]
    assert bundle["answers"]["D03"]["text"] == "Ask for the earlier message first."
    assert bundle["answers"]["D05"]["kind"] == "unanswered"

    later = submit(J, "req-partial-02", {"D05": {"kind": "chosen", "option_id": "A"}})   # the open cards stay open
    assert [b["submission_id"] for b in store.list_submissions(J, "report-01")] == \
        [receipt["submission_id"], later["submission_id"]] == ["sub-000001", "sub-000002"]


def test_comments_are_kept_exactly_as_written(tmp_path: Path) -> None:
    J = published(tmp_path)
    comment = "  only for adults \n\t(not in group chats), “quoted”  "
    general = "\nSee my note on D01.  "
    answers = {"D01": {"kind": "chosen", "option_id": "A", "comment": comment}}
    draft = store.save_draft(J, "report-01", 1, "Reviewer-One", answers, 0, comments=general)
    assert draft["answers"]["D01"]["comment"] == comment and draft["comments"] == general
    reloaded = store.load_draft(J, "report-01", "Reviewer-One")
    assert reloaded["answers"]["D01"]["comment"] == comment and reloaded["comments"] == general
    bundle = store.read_submission(J, submit(J, "req-comment-1", answers)["submission_id"])
    assert bundle["answers"]["D01"]["comment"] == comment
    assert bundle["request"]["answers"]["D01"]["comment"] == comment and bundle["comments"] == general


def test_submitting_changes_no_guideline_label_or_report(tmp_path: Path) -> None:
    J = published(tmp_path)
    (J / "policy/versions/G_00").mkdir(parents=True)
    (J / "policy/versions/G_00/guideline.md").write_text("# G_00\nLabel supportive replies.\n", encoding="utf-8")
    (J / "gold/versions/l01").mkdir(parents=True)
    (J / "gold/versions/l01/references.jsonl").write_text('{"item_id": "L01", "label": "supportive"}\n',
                                                          encoding="utf-8")
    store.save_draft(J, "report-01", 1, "Reviewer-One", CHOSEN, 0)
    before = files(J)
    submit(J)
    after = files(J)
    assert {name: data for name, data in after.items() if name in before} == before
    assert all(name.startswith(("meaning/feedback/", "meaning/events/")) for name in set(after) - set(before))


# ── identifiers, symlinks, crashes ───────────────────────────────────────────


UNSAFE = ["../report-01", "report-01/../../x", "..", ".hidden", "a b", "x" * 65, "report-01\n", "%2e%2e",
          "a\\b", ""]


@pytest.mark.parametrize("bad", UNSAFE)
def test_unsafe_identifiers_are_refused_and_write_nothing(tmp_path: Path, bad: str) -> None:
    J = published(tmp_path)
    submit(J)
    saved = files(tmp_path)                                           # the whole tree, so a write outside J shows
    for call in (
        lambda: store.load_report(J, bad),
        lambda: store.load_draft(J, bad, "Reviewer-One"),
        lambda: store.load_draft(J, "report-01", bad),
        lambda: store.save_draft(J, bad, 1, "Reviewer-One", {}, 0),
        lambda: store.save_draft(J, "report-01", 1, bad, {}, 0),
        lambda: submit(J, actor=bad),
        lambda: submit(J, request_id=bad),
        lambda: store.read_submission(J, bad),
        lambda: store.list_submissions(J, bad),
        lambda: store.publish_report(J, demo(report_id=bad), "meaning-agent"),
        lambda: store.publish_report(J, revised(demo()), bad),
    ):
        with pytest.raises(store.ValidationError, match="must match"):
            call()
    assert files(tmp_path) == saved


def test_a_symlink_out_of_the_lane_is_refused(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    J = lane(tmp_path)
    (J / "meaning").mkdir(parents=True)
    (J / "meaning" / "reports").symlink_to(outside, target_is_directory=True)
    with pytest.raises(store.MeaningError, match="outside J/meaning"):
        store.publish_report(J, demo(), "meaning-agent")
    other = lane(tmp_path / "second")
    other.mkdir(parents=True)
    (other / "meaning").symlink_to(outside, target_is_directory=True)
    with pytest.raises(store.MeaningError, match="symlinked"):
        store.publish_report(other, demo(), "meaning-agent")
    assert list(outside.iterdir()) == []


def _crash_on(folder: str):
    real_replace = os.replace

    def replace(source, target):
        if f"/{folder}/" in str(target):
            raise OSError(f"simulated crash before the {folder} replace")
        return real_replace(source, target)

    return replace


def test_a_crash_between_the_temp_write_and_the_replace_leaves_no_committed_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    J = published(tmp_path)
    saved = files(J)
    with monkeypatch.context() as patch:
        patch.setattr(store.os, "replace", _crash_on("feedback"))
        with pytest.raises(OSError, match="simulated crash"):
            submit(J)
    assert files(J) == saved                                          # no bundle, no temp file, no event
    assert store.list_submissions(J, "report-01") == [] and store.list_reports(J)[0]["status"] == "open"
    assert submit(J)["submission_id"] == "sub-000001"                 # the retry commits exactly one bundle
    assert len(store.list_submissions(J, "report-01")) == 1


def test_a_temp_file_left_by_a_killed_writer_is_never_read(tmp_path: Path) -> None:
    J = published(tmp_path)
    (J / "meaning/feedback").mkdir(parents=True)
    (J / "meaning/feedback/.sub-000001.json.k3j2.tmp").write_text('{"half": ', encoding="utf-8")
    (J / "meaning/reports/report-01/.v02.json.x9.tmp").write_text("{}", encoding="utf-8")
    (J / "meaning/drafts/report-01").mkdir(parents=True)
    (J / "meaning/drafts/report-01/.Reviewer-One.json.q1.tmp").write_text("{", encoding="utf-8")
    assert store.list_submissions(J, "report-01") == [] and store.load_draft(J, "report-01", "Reviewer-One") is None
    assert store.list_reports(J)[0]["status"] == "open" and store.load_report(J, "report-01")["report_revision"] == 1
    assert submit(J)["submission_id"] == "sub-000001"


def test_a_crash_between_the_bundle_and_its_event_is_repaired_on_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    J = published(tmp_path)
    with monkeypatch.context() as patch:
        patch.setattr(store.os, "replace", _crash_on("events"))
        with pytest.raises(OSError, match="simulated crash"):
            submit(J)
    [bundle] = store.list_submissions(J, "report-01")                 # received and durable, though the call failed
    assert [event["transition"] for event in store.list_events(J)] == ["published"]

    assert submit(J) == {"submission_id": bundle["submission_id"], "request_id": "req-0001-demo",
                         "status": "received", "submitted_at": bundle["submitted_at"]}
    events = store.list_events(J)
    assert [(e["sequence"], e["transition"], e["repaired"]) for e in events] == \
        [(1, "published", False), (2, "submitted", True)]
    assert events[1]["target"]["submission_id"] == bundle["submission_id"]
    assert events[1]["prior_event_id"] == events[0]["event_id"]
    submit(J)
    assert len(store.list_events(J)) == 2                             # repaired once, never twice


# ── status and events ────────────────────────────────────────────────────────


def test_list_reports_status_and_counts(tmp_path: Path) -> None:
    J = published(tmp_path, demo(report_id="report-c", round_id="round-02"))
    store.publish_report(J, demo(report_id="report-b"), "meaning-agent")
    store.publish_report(J, demo(report_id="report-a"), "meaning-agent")
    store.save_draft(J, "report-b", 1, "Reviewer-One", {"D01": {"kind": "chosen", "option_id": "A"},
                                                        "D02": {"kind": "custom", "text": "Only with consent."},
                                                        "D03": {"kind": "defer"}}, 0)
    submit(J, "req-a-000001", {"D01": {"kind": "reject_options"}, "D02": {"kind": "defer"}}, report_id="report-a")
    store.save_draft(J, "report-a", 1, "Reviewer-Two", {d: {"kind": "defer"} for d in ("D01", "D02", "D03")}, 0)

    summaries = store.list_reports(J)
    assert [(s["round_id"], s["report_id"]) for s in summaries] == \
        [("round-01", "report-a"), ("round-01", "report-b"), ("round-02", "report-c")]
    status = {s["report_id"]: (s["status"], s["counts"]) for s in summaries}
    assert status["report-a"] == ("submitted", {"answered": 1, "deferred": 1, "waiting": 4})  # a later draft hides nothing
    assert status["report-b"] == ("draft", {"answered": 2, "deferred": 1, "waiting": 3})
    assert status["report-c"] == ("open", {"answered": 0, "deferred": 0, "waiting": 6})

    store.save_draft(J, "report-b", 1, "Reviewer-Two", {"D01": {"kind": "defer"}}, 0)    # the newest draft counts
    assert store.list_reports(J)[1]["counts"] == {"answered": 0, "deferred": 1, "waiting": 5}

    store.publish_report(J, revised(demo(report_id="report-a")), "meaning-agent")       # a new revision starts open
    first = store.list_reports(J)[0]
    assert (first["report_id"], first["report_revision"], first["status"], first["counts"]) == \
        ("report-a", 2, "open", {"answered": 0, "deferred": 0, "waiting": 6})


def test_events_are_numbered_chained_per_report_and_carry_no_hash(tmp_path: Path) -> None:
    J = published(tmp_path)
    store.publish_report(J, demo(report_id="report-02"), "meaning-agent")
    submit(J)
    store.publish_report(J, revised(demo()), "meaning-agent")
    events = store.list_events(J)
    assert [(e["sequence"], e["transition"]) for e in events] == \
        [(1, "published"), (2, "published"), (3, "submitted"), (4, "published")]
    assert events[1]["prior_event_id"] is None                        # report-02 has its own chain
    assert events[2]["prior_event_id"] == events[0]["event_id"]
    assert events[3]["prior_event_id"] == events[2]["event_id"]
    assert sorted(path.name for path in (J / "meaning/events").iterdir()) == \
        [f"{e['sequence']:06d}-{e['event_id']}.json" for e in events]
    assert all(datetime.fromisoformat(e["created_at"]).tzinfo is not None for e in events)

    def keys(value):
        if isinstance(value, dict):
            for key, item in value.items():
                yield key
                yield from keys(item)
        elif isinstance(value, list):
            for item in value:
                yield from keys(item)

    for name, data in files(J).items():
        for key in keys(json.loads(data)):
            assert not any(word in key.lower() for word in ("hash", "sha", "checksum", "fingerprint")), (name, key)


def test_the_store_loads_by_file_path_without_the_engine_on_sys_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "path", [entry for entry in sys.path if Path(entry or ".").resolve() != HERE])
    monkeypatch.delitem(sys.modules, "meaning_contracts", raising=False)
    spec = importlib.util.spec_from_file_location("haipipe_meaning_store_by_path_test", HERE / "meaning_store.py")
    assert spec and spec.loader
    fresh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fresh)

    assert fresh.contracts.__name__ != "meaning_contracts"            # loaded by path, not imported
    assert Path(fresh.contracts.__file__).resolve() == HERE / "meaning_contracts.py"
    for name in ("MeaningError", "ValidationError", "StaleRevision", "DuplicateRequest"):
        assert getattr(fresh, name) is getattr(fresh.contracts, name)
    assert fresh.list_reports(tmp_path / "empty-lane") == []
    assert not (tmp_path / "empty-lane").exists()

    J = tmp_path / "lane"
    fresh.publish_report(J, demo(), "test")
    with pytest.raises(fresh.StaleRevision):
        fresh.publish_report(J, demo(), "test")
    with pytest.raises(fresh.ValidationError):
        fresh.save_draft(J, "report-01", 1, "Reviewer-One", {"no-such-card": {"kind": "defer"}}, 0)
