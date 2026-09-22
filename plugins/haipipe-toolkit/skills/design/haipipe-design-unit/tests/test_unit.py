"""Behavioral gates over real synthetic artifacts, not prose/heading matches."""
import importlib.util
import json
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
        name = f"rd{number:02}_{operation}_sms"
        config = {"goal": "Synthetic fixture", "kind": "sms", "mode": "compose",
                  "basis": "brief-only", "unit": {"shape": "single", "count": 1},
                  "max_iterations": 2,
                  "review_mode": "self" if operation == "generate" else "independent",
                  "design_intent": {
                      "move": "Make the next action immediately legible",
                      "basis": "brief-only", "stance": "generate",
                      "expected_effect": None, "failure_condition": None},
                  "criteria": [{"id": "length", "kind": "max_chars", "value": 160},
                               {"id": "link", "kind": "contains",
                                "value": "{confirmation_link}"}]}
        config.update(updates or {})
        cp = self.dump(self.owner / "scripts" / "config" / (name + ".yaml"), config)
        data = {"schema": "haipipe.design-ticket/v2", "run": name, "operation": operation,
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
            "schema": gate.RESULT_SCHEMA, "run": data["run"],
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
        log = self.owner / "outline" / "Design-01-log.md"
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
            {"id": "tone", "kind": "semantic", "description": "Respectful",
             "observation": "Read as the intended recipient.",
             "pass_when": "The refusal route is clear.",
             "fail_when": "The message pressures the reader.",
             "not_verifiable_when": "The recipient/context is not supplied."}]})
        result = self.result(ticket)
        self.edit_checks(result, lambda rows: rows[0].update(status="unresolved"))
        manifest = gate.document(result)
        manifest["verdict"] = "unresolved"
        self.dump(result, manifest)
        self.assert_bad(ticket, result, "unresolved check needs a valid unresolved_reason")

    def test_semantic_rule_written_before_the_method_rule_stays_readable(self):
        """A closed run keeps the config it froze; the observation method came later."""
        old = {"id": "tone", "kind": "semantic", "description": "Respectful"}
        ticket = self.ticket(updates={"criteria": [old]})
        self.assertIn("criterion.observation", " ".join(gate.validate(ticket)))
        self.assertEqual(gate.validate(ticket, historical=True), [])
        half = self.ticket(2, updates={"criteria": [
            {**old, "observation": "Read as the intended recipient."}]})
        self.assertIn("criterion.pass_when", " ".join(gate.validate(half, historical=True)))

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
        manifest["run"] = "rd99_generate_imposter"
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
        ticket = self.ticket(updates={"basis": "evidence-informed",
                                      "design_intent": {
                                          "move": "Use the signed handoff",
                                          "basis": "evidence-informed",
                                          "stance": "follow",
                                          "expected_effect": None,
                                          "failure_condition": None}})
        self.assert_bad(ticket, message="has no evidence")

    def test_v2_requires_explicit_design_intent(self):
        ticket = self.ticket()
        cp = self.owner / gate.document(ticket)["config"]["path"]
        config = gate.document(cp)
        config.pop("design_intent")
        self.dump(cp, config)
        data = gate.document(ticket)
        data["config"] = self.ref(cp)
        self.dump(ticket, data)
        self.assert_bad(ticket, message="design_intent")

    def test_v1_is_rejected_even_when_other_fields_are_valid(self):
        ticket = self.ticket()
        cp = self.owner / gate.document(ticket)["config"]["path"]
        config = gate.document(cp)
        data = gate.document(ticket)
        data["schema"] = "haipipe.design-ticket/v1"
        self.dump(ticket, data)
        self.assert_bad(ticket, message="unsupported Ticket schema")

    def test_retired_run_identity_is_rejected(self):
        ticket = self.ticket()
        data = gate.document(ticket)
        old = ticket.with_name("r01_design_generate_sms.yaml")
        data["run"] = old.stem
        self.dump(old, data)
        self.assert_bad(old, message="invalid Design Run stem")
        self.assertIn("retired Design Run identity",
                      " ".join(gate.audit_folder(self.owner)))

    def test_brainstorm_cannot_smuggle_in_forecast(self):
        ticket = self.ticket(updates={"mode": "brainstorm",
                                      "design_intent": {
                                          "move": "Open distinct message directions",
                                          "basis": "brief-only",
                                          "stance": "explore",
                                          "expected_effect": "One direction will win",
                                          "failure_condition": None}})
        self.assert_bad(ticket, message="cannot smuggle")

    def test_theory_driven_requires_falsifiable_intent(self):
        ticket = self.ticket(updates={"mode": "theory-driven"})
        self.assert_bad(ticket, message="requires expected effect")

    def test_challenge_requires_challenge_stance(self):
        ticket = self.ticket(updates={"mode": "challenge"})
        self.assert_bad(ticket, message="challenge mode requires")

    def test_page_run_cannot_become_design_evidence(self):
        source = self.write(self.owner / "outline" / "page-step.md", "Page wording\n")
        ticket = self.ticket()
        data = gate.document(ticket)
        data["inputs"] = [{"role": "evidence", "run_id": "rp01_p01",
                           **self.ref(source)}]
        self.dump(ticket, data)
        self.assert_bad(ticket, message="only as frozen feedback")

    def test_page_run_feedback_routes_through_a_revision(self):
        base = self.write(self.owner / "inputs" / "base.txt", "Prior candidate\n")
        feedback = self.write(self.owner / "outline" / "candidate-feedback.md",
                              "Make the requested action more direct.\n")
        ticket = self.ticket(updates={"mode": "revise"})
        data = gate.document(ticket)
        data["inputs"] = [
            {"role": "base", **self.ref(base)},
            {"role": "feedback", "run_id": "rp01_p03", **self.ref(feedback)},
        ]
        self.dump(ticket, data)
        self.assertEqual(gate.validate(ticket), [])

    def test_duplicate_yaml_fields_rejected(self):
        ticket = self.ticket()
        self.write(ticket, ticket.read_text() + "\noperation: verify\n")
        self.assert_bad(ticket, message="duplicate YAML")

    def test_orphan_result_is_visible(self):
        orphan = self.owner / "results" / "rd03_generate_orphan"
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

    def test_decision_runs_are_paired_not_rejected(self):
        # Commission is current; Adopt is historical reader compatibility:
        # the folder audit checks their pairing, never worker semantics.
        run = "rd05_commission_sms"
        self.dump(self.owner / "runs" / f"{run}.yaml", {
            "schema": gate.TICKET_SCHEMA, "run": run, "operation": "commission",
            "target": "One SMS", "actor": {"mode": "human", "owner": "JL"}})
        self.dump(self.owner / "results" / run / "runtime.yaml",
                  {"run": run, "status": "complete", "finished_at": "later"})
        self.assertIn("decision", " ".join(gate.audit_folder(self.owner)))
        self.dump(self.owner / "results" / run / "decision.yaml",
                  {"run": run, "decision": "release", "actor": "JL"})
        self.assertEqual(gate.audit_folder(self.owner), [])
        bad = self.owner / "runs" / "rd06_adopt_sms.yaml"
        self.dump(bad, {"schema": gate.TICKET_SCHEMA, "run": "rd06_adopt_other",
                        "operation": "adopt"})
        self.assertIn("identity mismatch", " ".join(gate.audit_folder(self.owner)))

    def add_render(self, result, source, candidate, **changes):
        import os
        picture = self.write(result.parent / "render" / "screen.png", "synthetic picture bytes")
        path = result.parent / "render" / "manifest.json"
        row = {"item": "ITEM01", "candidate": candidate, "version": 1,
               "source": os.path.relpath(source, path.parent), "sha256": gate.digest(source),
               "render": picture.name, "render_sha256": gate.digest(picture)}
        row.update(changes)
        self.write(path, json.dumps([row]))
        manifest = gate.document(result)
        manifest["render_manifest"] = self.ref(path, result.parent)
        self.dump(result, manifest)
        return path, picture

    def test_render_evidence_does_not_change_content_count(self):
        ticket = self.ticket()
        result = self.result(ticket)
        self.add_render(result, result.parent / "content/sms.txt", ticket.stem)
        self.assertEqual(gate.validate(ticket, result), [])
        self.assertEqual(len(gate.document(result)["artifacts"]), 1)
        self.assertEqual(gate.audit_folder(self.owner), [])

    def test_render_picture_and_manifest_are_both_hash_bound(self):
        for changed in ("picture", "manifest"):
            with self.subTest(changed=changed):
                ticket = self.ticket()
                result = self.result(ticket)
                manifest, picture = self.add_render(result, result.parent / "content/sms.txt", ticket.stem)
                target = picture if changed == "picture" else manifest
                self.write(target, target.read_text() + " ")
                self.assert_bad(ticket, result, "hash mismatch")

    def test_render_rejects_wrong_source_candidate_and_version(self):
        ticket = self.ticket()
        result = self.result(ticket)
        outside = self.write(self.owner / "uncommissioned.html", "not a commissioned artifact")
        for source, candidate, changes, diagnostic in (
                (outside, ticket.stem, {}, "not a pinned content artifact"),
                (result.parent / "content/sms.txt", "rd99_generate_other", {}, "not a pinned content artifact"),
                (result.parent / "content/sms.txt", ticket.stem, {"version": 0}, "positive integer")):
            with self.subTest(diagnostic=diagnostic, candidate=candidate):
                self.add_render(result, source, candidate, **changes)
                self.assert_bad(ticket, result, diagnostic)

    def test_render_picture_cannot_escape_its_result(self):
        ticket = self.ticket()
        result = self.result(ticket)
        outside = self.write(self.owner / "outside.png", "outside picture")
        self.add_render(result, result.parent / "content/sms.txt", ticket.stem,
                        render="../../../outside.png", render_sha256=gate.digest(outside))
        self.assert_bad(ticket, result, "escapes Result")

    def test_render_requires_matching_item_when_ticket_names_one(self):
        ticket = self.ticket()
        data = gate.document(ticket)
        data["item"] = "ITEM02"
        self.dump(ticket, data)
        result = self.result(ticket)
        self.add_render(result, result.parent / "content/sms.txt", ticket.stem)
        self.assert_bad(ticket, result, "render item mismatch")

    def test_verify_render_is_local_and_reads_only_pinned_source(self):
        generate = self.ticket()
        generated = self.result(generate)
        self.add_render(generated, generated.parent / "content/sms.txt", generate.stem)
        before = {str(p): p.read_bytes() for p in generated.parent.rglob("*") if p.is_file()}
        verify = self.ticket(2, "verify", [self.ref(generated, self.owner)])
        verified = self.result(verify)
        self.add_render(verified, generated.parent / "content/sms.txt", generate.stem)
        self.assertEqual(gate.validate(verify, verified), [])
        self.assertEqual(gate.document(verified)["artifacts"], [])
        self.assertEqual(before, {str(p): p.read_bytes() for p in generated.parent.rglob("*") if p.is_file()})

    def test_verify_checks_target_render_integrity(self):
        generate = self.ticket()
        generated = self.result(generate)
        _, picture = self.add_render(generated, generated.parent / "content/sms.txt", generate.stem)
        verify = self.ticket(2, "verify", [self.ref(generated, self.owner)])
        self.write(picture, "changed after the target Result was pinned")
        self.assert_bad(verify, message="hash mismatch")


if __name__ == "__main__":
    unittest.main()
