"""Behavioral checks for immutable, instance-scoped Insight item evidence."""
from contextlib import redirect_stdout, redirect_stderr
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import yaml

import insight_items as app


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def fixture(root, patient="patient-a", *, add_open=True):
    folder = root / patient
    data = folder / "outline/evidence/materials/snapshot-01.yaml"
    write(data, {"snapshot": "immutable-01", "subject": patient, "tables": ["messages", "events"]})
    ds = {"id": patient, "version": "snapshot-01", "manifest": str(data), "sha256": app.digest(data)}
    item = {"run": "r01_description", "question": "What tables are available?", "target": "wisdom",
            "datasets": [f"{patient}@snapshot-01"], "expected": "Sourced inventory and boundaries",
            "acceptance": "All inventory claims trace to the frozen manifest"}
    manifest = {"schema": "haipipe.insight-instance/v1", "instance": f"study/{patient}",
                "topic": "Longitudinal data understanding", "datasets": [ds], "items": [item]}
    if add_open:
        other = dict(item, run="r02_temporal", question="What changes over time?")
        manifest["items"].append(other)
    write(folder / "workflow/insight.yaml", manifest)
    (folder / "runs").mkdir(parents=True)
    (folder / "runs/r01_description.sh").write_text("#!/bin/sh\n# fixture ticket; no real analysis\nexit 0\n")
    directory = folder / "results/r01_description/v001"
    frozen = {"schema": "haipipe.insight-input/v1", "instance": manifest["instance"],
              "run": item["run"], "version": "v001", "question": item["question"],
              "target": item["target"], "acceptance": item["acceptance"], "datasets": [ds],
              "supporting_results": [], "recipe_calls": []}
    write(directory / "input.yaml", frozen)
    ident = app.full_id(manifest["instance"], item["run"], "v001")
    result = {"schema": "haipipe.insight-result/v1", "execution": ident, "target": "wisdom",
              "outcome": "accepted", "review": {"verdict": "pass", "receipt": "review.yaml"},
              "D": [{"id": "D1", "text": "Snapshot inventory lists messages and events", "parents": ["dataset:0"]}],
              "I": [{"id": "I1", "text": "Two table kinds are listed", "parents": ["D1"]}],
              "K": [{"id": "K1", "text": "The inventory exposes two table kinds", "parents": ["I1"],
                     "strength": "inventory-only", "rivals": ["Contents may be incomplete"], "boundary": "This manifest only"}],
              "W": [{"id": "W1", "text": "Inspect coverage before using content", "parents": ["K1"]}],
              "RF": [{"id": "RF1", "text": "Two table kinds are declared, coverage unverified", "parents": ["W1"],
                      "strength": "inventory-only", "boundary": "This manifest only"}]}
    write(directory / "result.yaml", result)
    write(directory / "review.yaml", {"schema": "haipipe.insight-review/v1", "verdict": "pass",
          "author": "fixture-author", "reviewer": "fixture-reviewer", "checked": ["synthetic parser fixture only"],
          "candidate_sha256": app.candidate_digest(result), "input_sha256": app.digest(directory / "input.yaml")})
    (directory / "review.md").write_text("Nonclinical parser fixture; not a scientific review.\n")
    (directory / "evidence.md").write_text("Manifest identity and table inventory checked.\n")
    runtime = {"schema": "haipipe.insight-runtime/v1", "execution": ident, "family": "insight",
               "operation": "item", "status": "complete", "input_sha256": app.digest(directory / "input.yaml"),
               "result_sha256": app.digest(directory / "result.yaml"), "attempts": [{"attempt": 1, "status": "complete"}],
               "checkpoints": {key: {"at": "2026-09-07T12:00:00Z", "receipt": receipt}
                               for key, receipt in zip(app.STAGES, ("input.yaml", "evidence.md", "review.yaml", "result.yaml"))}}
    write(directory / "runtime.yaml", runtime)
    return folder, directory


class InsightItemsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.folder, self.execution = fixture(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def mutate_result(self, edit, reseal=True):
        path = self.execution / "result.yaml"
        result = app.read_yaml(path)
        edit(result)
        write(path, result)
        if reseal:
            review_path = self.execution / "review.yaml"
            review = app.read_yaml(review_path)
            review["candidate_sha256"] = app.candidate_digest(result)
            write(review_path, review)
            runtime = app.read_yaml(self.execution / "runtime.yaml")
            runtime["result_sha256"] = app.digest(path)
            write(self.execution / "runtime.yaml", runtime)

    def faults(self):
        return app.inspect(self.folder)[2]

    def test_broken_skipping_claim_is_rejected_before_valid_fixture_is_trusted(self):
        self.mutate_result(lambda r: r["K"][0].update(parents=["D1"]))
        self.assertTrue(any("skips rung" in e for e in self.faults()))

    def test_valid_instance_keeps_open_sibling_without_blocking_completed_item(self):
        manifest, rows, errors = app.inspect(self.folder)
        self.assertEqual([], errors)
        self.assertEqual(2, len(rows))
        self.assertEqual([], rows[1]["versions"])
        output = io.StringIO()
        with redirect_stdout(output):
            status = app.main(["cite", str(self.folder), "--item", "r01_description", "--version", "v001", "--finding", "RF1"])
        self.assertEqual(0, status)
        packet = json.loads(output.getvalue())
        self.assertEqual(manifest["instance"], packet["instance"])
        self.assertEqual(app.digest(self.execution / "result.yaml"), packet["sha256"])

    def test_patient_instances_share_item_name_without_identity_collision(self):
        other, _ = fixture(self.root, "patient-b")
        a = app.inspect(self.folder)
        b = app.inspect(other)
        self.assertEqual([], a[2] + b[2])
        self.assertNotEqual(a[1][0]["versions"][0]["execution"], b[1][0]["versions"][0]["execution"])

    def test_wrong_patient_result_is_rejected_even_with_resealed_hash(self):
        self.mutate_result(lambda r: r.update(execution="study/patient-b#r01_description@v001"))
        self.assertTrue(any("Result execution identity mismatch" in e for e in self.faults()))

    def test_modified_result_payload_breaks_pinned_hash(self):
        self.mutate_result(lambda r: r["RF"][0].update(text="Different finding"), reseal=False)
        self.assertTrue(any("Result hash mismatch" in e for e in self.faults()))

    def test_changed_dataset_in_place_is_detected(self):
        data = self.folder / "outline/evidence/materials/snapshot-01.yaml"
        write(data, {"snapshot": "actually-new-data"})
        self.assertTrue(any("hash mismatch" in e for e in self.faults()))

    def test_result_without_ticket_is_orphaned(self):
        (self.folder / "runs/r01_description.sh").unlink()
        self.assertTrue(any("no local ticket" in e for e in self.faults()))

    def test_checkpoint_cannot_jump_to_publish(self):
        path = self.execution / "runtime.yaml"
        runtime = app.read_yaml(path)
        del runtime["checkpoints"]["evidence"]
        write(path, runtime)
        self.assertTrue(any("skips a predecessor" in e for e in self.faults()))

    def test_no_answer_is_terminal_but_not_published_evidence(self):
        self.mutate_result(lambda r: r.update(outcome="insufficient", reason="No observations available", RF=[]))
        path = self.execution / "runtime.yaml"
        runtime = app.read_yaml(path)
        del runtime["checkpoints"]["published"]
        write(path, runtime)
        self.assertEqual([], self.faults())
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(1, app.main(["cite", str(self.folder), "--item", "r01_description", "--version", "v001", "--finding", "RF1"]))

    def test_unreviewed_claim_cannot_be_published(self):
        self.mutate_result(lambda r: r.update(review={"verdict": "pending", "receipt": "review.md"}))
        self.assertTrue(any("passing review" in e for e in self.faults()))

    def test_new_version_does_not_hide_accepted_historical_result(self):
        before = app.digest(self.execution / "result.yaml")
        newer = self.execution.parent / "v002"
        runtime = {"schema": "haipipe.insight-runtime/v1", "execution": "study/patient-a#r01_description@v002",
                   "family": "insight", "operation": "item", "status": "planned", "checkpoints": {},
                   "attempts": [{"attempt": 1, "status": "planned"}]}
        write(newer / "runtime.yaml", runtime)
        _, rows, errors = app.inspect(self.folder)
        self.assertEqual([], errors)
        rendered = app.table(rows)
        self.assertIn("@v002", rendered)
        self.assertIn("@v001 / RF1", rendered)
        self.assertEqual(before, app.digest(self.execution / "result.yaml"))

    def test_new_snapshot_marks_old_binding_stale_without_destroying_result(self):
        path = self.folder / "workflow/insight.yaml"
        manifest = app.read_yaml(path)
        data = self.folder / "outline/evidence/materials/snapshot-02.yaml"
        write(data, {"snapshot": "immutable-02"})
        manifest["datasets"].append({"id": "patient-a", "version": "snapshot-02", "manifest": str(data), "sha256": app.digest(data)})
        manifest["items"][0]["datasets"] = ["patient-a@snapshot-02"]
        write(path, manifest)
        _, rows, errors = app.inspect(self.folder)
        self.assertEqual([], errors)
        self.assertIn("input binding stale", app.table(rows))

    def test_bare_local_support_id_is_rejected(self):
        path = self.execution / "input.yaml"
        frozen = app.read_yaml(path)
        frozen["supporting_results"] = [{"run": "r01", "path": str(self.execution / "review.md"),
                                          "sha256": app.digest(self.execution / "review.md")}]
        write(path, frozen)
        runtime = app.read_yaml(self.execution / "runtime.yaml")
        runtime["input_sha256"] = app.digest(path)
        write(self.execution / "runtime.yaml", runtime)
        self.assertTrue(any("unqualified Supporting Run" in e for e in self.faults()))

    def test_wrong_patient_support_is_rejected_even_with_correct_file_hash(self):
        _, other = fixture(self.root, "patient-b")
        path = self.execution / "input.yaml"
        frozen = app.read_yaml(path)
        frozen["supporting_results"] = [{"run": "study/patient-c#r01_description@v001",
                                          "path": str(other / "result.yaml"),
                                          "sha256": app.digest(other / "result.yaml")}]
        write(path, frozen)
        runtime = app.read_yaml(self.execution / "runtime.yaml")
        runtime["input_sha256"] = app.digest(path)
        write(self.execution / "runtime.yaml", runtime)
        self.assertTrue(any("Supporting Result execution identity mismatch" in e for e in self.faults()))

    def test_escaped_review_path_cannot_qualify(self):
        self.mutate_result(lambda r: r.update(review={"verdict": "pass", "receipt": "../../../../workflow/insight.yaml"}))
        self.assertTrue(any("inside execution directory" in e for e in self.faults()))

    def test_latest_is_not_a_citation_version(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(1, app.main(["cite", str(self.folder), "--item", "r01_description", "--version", "latest", "--finding", "RF1"]))

    def test_ticket_requires_receipt_but_proposed_item_does_not(self):
        (self.folder / "runs/r02_temporal.sh").write_text("exit 78\n")
        self.assertTrue(any("no runtime receipt" in e for e in self.faults()))

    def test_local_dependency_is_not_an_insight_item(self):
        (self.folder / "runs/r03_evidence.sh").write_text("exit 78\n")
        write(self.folder / "results/r03_evidence/runtime.yaml", {
            "run": "r03_evidence", "family": "page", "operation": "evidence-item", "status": "blocked"})
        self.assertEqual([], self.faults())
        self.assertEqual(2, len(app.inspect(self.folder)[1]))

    def test_later_invalid_version_does_not_break_old_pin(self):
        write(self.execution.parent / "v002/runtime.yaml", {"broken": True})
        self.assertTrue(self.faults())
        with redirect_stdout(io.StringIO()):
            self.assertEqual(0, app.main(["cite", str(self.folder), "--item", "r01_description", "--version", "v001", "--finding", "RF1"]))

    def test_historical_resolution_does_not_approve_current_applicability(self):
        path = self.folder / "workflow/insight.yaml"
        manifest = app.read_yaml(path)
        manifest["items"][0]["question"] = "A different question"
        write(path, manifest)
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(0, app.main(["cite", str(self.folder), "--item", "r01_description", "--version", "v001", "--finding", "RF1", "--historical"]))
        self.assertEqual("historical-needs-recheck", json.loads(output.getvalue())["applicability"])

    def test_review_must_bind_exact_candidate(self):
        path = self.execution / "review.yaml"
        review = app.read_yaml(path)
        review["candidate_sha256"] = "0" * 64
        write(path, review)
        self.assertTrue(any("exact candidate" in e for e in self.faults()))

    def test_self_review_is_rejected(self):
        path = self.execution / "review.yaml"
        review = app.read_yaml(path)
        review["reviewer"] = review["author"]
        write(path, review)
        self.assertTrue(any("reviewer must differ" in e for e in self.faults()))


if __name__ == "__main__":
    unittest.main()
