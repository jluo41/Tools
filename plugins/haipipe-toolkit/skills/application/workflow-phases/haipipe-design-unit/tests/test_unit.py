"""Behavioral gates over real synthetic artifacts, not prose/heading matches."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import yaml

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "check_unit.py"
spec = importlib.util.spec_from_file_location("design_unit_gate", MODULE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class DesignUnitGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="design-unit-test-")
        self.owner = Path(self.tmp.name).resolve()
        self.approval = self.owner / "outline" / "release.md"
        self.write(self.approval, "# Synthetic test fixture approval\nNot a live release.\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def dump(self, path, obj):
        return self.write(path, yaml.safe_dump(obj, sort_keys=False, allow_unicode=True))

    def ref(self, path, root=None):
        return {"path": str(path.relative_to(root or self.owner)),
                "sha256": gate.digest(path)}

    def ticket(self, number=1, operation="generate", targets=None, updates=None):
        name = f"r{number:02}_design_{operation}_sms"
        config = {"goal": "Synthetic fixture", "kind": "sms", "mode": "compose",
                  "basis": "brief-only", "unit": {"shape": "single", "count": 1},
                  "max_iterations": 2,
                  "review_mode": "self" if operation == "generate" else "independent",
                  "criteria": [{"id": "length", "kind": "max_chars", "value": 160},
                               {"id": "link", "kind": "contains",
                                "value": "{confirmation_link}"}]}
        config.update(updates or {})
        cp = self.dump(self.owner / "scripts" / "config" / (name + ".yaml"), config)
        data = {"schema": "haipipe.design-ticket/v1", "run": name, "operation": operation,
                "worker": "haipipe-design-unit", "actor": "producer" if operation == "generate" else "reviewer",
                "target": "One synthetic SMS", "config": self.ref(cp),
                "approval": {"actor": "synthetic-test-person", "record": self.ref(self.approval)},
                "inputs": [], "targets": targets or []}
        ticket = self.dump(self.owner / "runs" / (name + ".yaml"), data)
        out = self.owner / "results" / name
        self.dump(out / "runtime.yaml", {
            "run": name, "family": "design", "operation": operation,
            "target": data["target"], "status": "planned",
            "ticket": "runs/" + ticket.name, "result": "results/" + name + "/",
            "ticket_sha256": gate.digest(ticket),
            "inputs": [data["config"], data["approval"]["record"]] + data["targets"],
            "worker": {"kind": "skill", "name": "haipipe-design-unit", "actor": data["actor"]}})
        return ticket

    def result(self, ticket, content="Please confirm at {confirmation_link}."):
        _, data, _, out, config, subjects = gate.context(ticket)
        artifacts = []
        if data["operation"] == "generate":
            path = self.write(out / "content" / "sms.txt", content)
            artifacts = [self.ref(path, out)]
            subjects = [("content/sms.txt", path)]
        checks = []
        for target, path in subjects:
            text = path.read_text()
            for c in config["criteria"]:
                passed = (len(text) <= c["value"] if c["kind"] == "max_chars"
                          else c["value"] in text if c["kind"] == "contains"
                          else c["value"] not in text if c["kind"] == "excludes" else True)
                checks.append({"target": target, "criterion": c["id"],
                               "status": "pass" if passed else "fail",
                               "evidence": "Synthetic fixture check of " + target})
        check_path = self.dump(out / "checks.yaml", {"checks": checks})
        verdict = "fail" if any(c["status"] == "fail" for c in checks) else "pass"
        result = self.dump(out / "result.yaml", {
            "schema": "haipipe.design-result/v1", "run": data["run"],
            "operation": data["operation"], "target": data["target"],
            "producer": data["actor"], "ticket_sha256": gate.digest(ticket),
            "config_sha256": data["config"]["sha256"], "artifacts": artifacts,
            "checks": self.ref(check_path, out), "targets": data["targets"],
            "verdict": verdict})
        if not gate.validate(ticket, result):
            runtime = gate.document(out / "runtime.yaml")
            runtime.update(status="complete", started_at="2026-09-07T00:00:00Z",
                           finished_at="2026-09-07T00:01:00Z", failure=None)
            self.dump(out / "runtime.yaml", runtime)
        return result

    def edit_checks(self, result, mutate):
        manifest = gate.document(result)
        cp = result.parent / manifest["checks"]["path"]
        checks = gate.document(cp)
        mutate(checks["checks"])
        self.dump(cp, checks)
        manifest["checks"] = self.ref(cp, result.parent)
        self.dump(result, manifest)

    def assert_bad(self, ticket, result=None, message=None):
        errors = gate.validate(ticket, result)
        self.assertTrue(errors)
        if message:
            self.assertIn(message, " ".join(errors))

    def test_valid_generation_and_inventory(self):
        ticket = self.ticket()
        result = self.result(ticket)
        self.assertEqual(gate.validate(ticket, result), [])
        self.assertEqual(gate.audit_folder(self.owner), [])

    def test_known_broken_actual_content_is_rejected(self):
        ticket = self.ticket()
        result = self.result(ticket, "Missing required confirmation link")
        self.assert_bad(ticket, result, "failing criteria")

    def test_dishonest_pass_does_not_override_actual_bytes(self):
        ticket = self.ticket()
        result = self.result(ticket, "No link")
        self.edit_checks(result, lambda rows: [r.update(status="pass") for r in rows])
        manifest = gate.document(result)
        manifest["verdict"] = "pass"
        self.dump(result, manifest)
        self.assert_bad(ticket, result, "actual artifact")

    def test_mutated_content_rejected_even_when_manifest_unchanged(self):
        ticket = self.ticket()
        result = self.result(ticket)
        self.write(result.parent / "content" / "sms.txt", "Changed")
        self.assert_bad(ticket, result, "hash mismatch")

    def test_stale_config_rejected(self):
        ticket = self.ticket()
        cp = self.owner / gate.document(ticket)["config"]["path"]
        self.write(cp, cp.read_text() + "\n# changed\n")
        self.assert_bad(ticket, message="hash mismatch")

    def test_missing_human_record_does_not_pass(self):
        ticket = self.ticket()
        self.approval.unlink()
        self.assert_bad(ticket, message="missing input")

    def test_growing_log_does_not_stale_individual_release(self):
        ticket = self.ticket()
        self.result(ticket)
        log = self.owner / "outline" / "DS01-log.md"
        self.write(log, "Release: release.md\n")
        self.assertEqual(gate.audit_folder(self.owner), [])
        self.write(log, "Release: release.md\nLater adoption: decision-02.yaml\n")
        self.assertEqual(gate.audit_folder(self.owner), [])

    def test_missing_check_coverage(self):
        ticket = self.ticket()
        result = self.result(ticket)
        self.edit_checks(result, lambda rows: rows.pop())
        self.assert_bad(ticket, result, "missing required")

    def test_duplicate_check_coverage(self):
        ticket = self.ticket()
        result = self.result(ticket)
        self.edit_checks(result, lambda rows: rows.append(dict(rows[0])))
        self.assert_bad(ticket, result, "duplicate")

    def test_unresolved_semantic_check_is_incomplete(self):
        ticket = self.ticket(updates={"criteria": [
            {"id": "tone", "kind": "semantic", "description": "Respectful"}]})
        result = self.result(ticket)
        self.edit_checks(result, lambda rows: rows[0].update(status="unresolved"))
        manifest = gate.document(result)
        manifest["verdict"] = "unresolved"
        self.dump(result, manifest)
        self.assert_bad(ticket, result, "unresolved")

    def test_verify_can_complete_with_rejecting_verdict(self):
        generation = self.ticket()
        du = self.result(generation)
        before = {p: p.read_bytes() for p in du.parent.rglob("*") if p.is_file()}
        review = self.ticket(2, "verify", [self.ref(du)],
                             {"criteria": [{"id": "tight", "kind": "max_chars", "value": 5}]})
        result = self.result(review)
        self.assertEqual(gate.document(result)["verdict"], "fail")
        self.assertEqual(gate.validate(review, result), [])
        self.assertEqual(gate.document(result.parent / "runtime.yaml")["status"], "complete")
        self.assertEqual(before, {p: p.read_bytes() for p in du.parent.rglob("*") if p.is_file()})
        self.assertEqual(gate.audit_folder(self.owner), [])

    def test_independent_reviewer_cannot_be_producer(self):
        du = self.result(self.ticket())
        ticket = self.ticket(2, "verify", [self.ref(du)])
        obj = gate.document(ticket)
        obj["actor"] = "producer"
        self.dump(ticket, obj)
        self.assert_bad(ticket, message="equals producer")

    def test_verify_detects_mutated_target_payload(self):
        du = self.result(self.ticket())
        ticket = self.ticket(2, "verify", [self.ref(du)])
        self.write(du.parent / "content" / "sms.txt", "tampered")
        self.assert_bad(ticket, message="hash mismatch")

    def test_verify_rejects_target_with_forged_run_pairing(self):
        du = self.result(self.ticket())
        manifest = gate.document(du)
        manifest["run"] = "r99_design_generate_imposter"
        self.dump(du, manifest)
        runtime_path = du.parent / "runtime.yaml"
        runtime = gate.document(runtime_path)
        runtime["run"] = manifest["run"]
        self.dump(runtime_path, runtime)
        ticket = self.ticket(2, "verify", [self.ref(du)])
        self.assert_bad(ticket, message="target Run/Result identity")

    def test_verify_cannot_replace_content(self):
        du = self.result(self.ticket())
        ticket = self.ticket(2, "verify", [self.ref(du)])
        result = self.result(ticket)
        obj = gate.document(result)
        obj["artifacts"] = [{"path": "content/replacement.txt", "sha256": "0" * 64}]
        self.dump(result, obj)
        self.assert_bad(ticket, result, "replacement")

    def test_artifact_escape_is_rejected(self):
        ticket = self.ticket()
        result = self.result(ticket)
        obj = gate.document(result)
        obj["artifacts"] = [{"path": "../../outside.txt", "sha256": "0" * 64}]
        self.dump(result, obj)
        self.assert_bad(ticket, result, "escapes")

    def test_revision_requires_actual_base_and_feedback(self):
        ticket = self.ticket(updates={"mode": "revise"})
        self.assert_bad(ticket, message="base and feedback")

    def test_evidence_informed_cannot_silently_be_brief_only(self):
        ticket = self.ticket(updates={"basis": "evidence-informed"})
        self.assert_bad(ticket, message="has no evidence")

    def test_duplicate_yaml_fields_rejected(self):
        ticket = self.ticket()
        self.write(ticket, ticket.read_text() + "\noperation: verify\n")
        self.assert_bad(ticket, message="duplicate YAML")

    def test_orphan_result_is_visible(self):
        orphan = self.owner / "results" / "r03_design_generate_orphan"
        orphan.mkdir(parents=True)
        self.assertIn("orphan Result", " ".join(gate.audit_folder(self.owner)))

    def test_planned_runtime_is_not_required_to_have_completed_result(self):
        self.ticket()
        self.assertEqual(gate.audit_folder(self.owner), [])

    def test_false_complete_receipt_requires_real_result(self):
        ticket = self.ticket()
        out = self.owner / "results" / ticket.stem
        runtime = gate.document(out / "runtime.yaml")
        runtime.update(status="complete", started_at="now", finished_at="later")
        self.dump(out / "runtime.yaml", runtime)
        self.assertTrue(gate.audit_folder(self.owner))

    def test_runtime_cannot_omit_source_or_worker_provenance(self):
        ticket = self.ticket()
        runtime_path = self.owner / "results" / ticket.stem / "runtime.yaml"
        runtime = gate.document(runtime_path)
        runtime.pop("worker")
        self.dump(runtime_path, runtime)
        self.assertIn("worker identity", " ".join(gate.audit_folder(self.owner)))
        runtime["worker"] = {"kind": "skill", "name": "haipipe-design-unit", "actor": "producer"}
        runtime["inputs"] = []
        self.dump(runtime_path, runtime)
        self.assertIn("input manifest", " ".join(gate.audit_folder(self.owner)))


if __name__ == "__main__":
    unittest.main()
