import hashlib
import re
import tempfile
import unittest
from pathlib import Path

from src.page_lifecycle import LEGAL_ROUTES, audit_artifacts, audit_run, traversed_edges


HERE = Path(__file__).resolve().parent.parent


def version(label):
    if ":" in label:
        return label
    source = hashlib.sha256(f"source:{label}".encode()).hexdigest()
    render = hashlib.sha256(f"render:{label}".encode()).hexdigest()
    return f"{source}:{render}"


def producer(
    step,
    phase,
    before,
    after,
    route,
    *,
    round=1,
    actor=None,
    builder="fresh-builder",
    reopens=False,
):
    before = version(before)
    after = version(after)
    source_sha256, render_sha256 = after.split(":")
    return {
        "step": step,
        "round": round,
        "phase": phase,
        "actor": actor or f"producer-{phase.lower()}",
        "role": "producer",
        "builder_actor": builder,
        "status": "ok",
        "version_before": before,
        "version_after": after,
        "checked_version": "",
        "source_sha256": source_sha256,
        "render_sha256": render_sha256,
        "mechanical_errors": 0,
        "mechanical_warnings": 0,
        "verdict": "",
        "route": route,
        "requested_route": route,
        "reopens_promise": reopens,
        "reason": f"{phase} exercised its declared authority",
        "artifacts": ["page.md"],
        "evidence": ["page.md"],
        "findings": [],
        "human_gate": {"required": False, "status": "not-required", "evidence": []},
    }


def check(
    step,
    checked_version,
    route="CLOSE",
    *,
    round=1,
    actor="fresh-judge",
    builder="fresh-builder",
    verdict=None,
    gate=None,
    reopens=False,
):
    if verdict is None:
        verdict = "pass" if route == "CLOSE" else "revise"
    checked_version = version(checked_version)
    source_sha256, render_sha256 = checked_version.split(":")
    return {
        "step": step,
        "round": round,
        "phase": "CHECK",
        "actor": actor,
        "role": "judge",
        "builder_actor": builder,
        "status": "blocked" if verdict == "blocked" else "ok",
        "version_before": checked_version,
        "version_after": checked_version,
        "checked_version": checked_version,
        "source_sha256": source_sha256,
        "render_sha256": render_sha256,
        "mechanical_errors": 0,
        "mechanical_warnings": 0,
        "verdict": verdict,
        "route": route,
        "requested_route": route,
        "reopens_promise": reopens,
        "reason": "fresh judgment routed the exact version",
        "artifacts": [],
        "evidence": ["rendered-page.html"],
        "findings": [] if verdict == "pass" else ["named finding"],
        "human_gate": gate or {"required": False, "status": "not-required", "evidence": []},
    }


def run(
    receipts,
    status="closed",
    final_version=None,
    max_steps=12,
    *,
    gate_required=None,
):
    if gate_required is None:
        gate_required = any(
            receipt.get("human_gate", {}).get("required") is True for receipt in receipts
        )
    return {
        "status": status,
        "run_id": "fixture",
        "board": "board",
        "page": "page.md",
        "packet": {
            "run_id": "fixture",
            "board": "board",
            "page": "page.md",
            "start_phase": receipts[0]["phase"],
            "intent": "exercise the Page lifecycle contract",
            "human_gate": {"required": gate_required, "rule": "fixture gate"},
            "limits": {"max_steps": max_steps, "max_rounds": 3},
        },
        "limits": {"max_steps": max_steps, "max_rounds": 3},
        "final_version": version(final_version) if final_version else receipts[-1]["version_after"],
        "receipts": receipts,
    }


class PageLifecycleAuditTest(unittest.TestCase):
    def assertClean(self, value):
        self.assertEqual([], audit_run(value))

    def codes(self, value):
        return {finding.code for finding in audit_run(value)}

    def test_direct_draft_check_close(self):
        value = run(
            [
                producer(1, "DRAFT", "v0", "v1", "CHECK"),
                check(2, "v1"),
            ]
        )
        self.assertClean(value)
        self.assertEqual(["DRAFT->CHECK", "CHECK->CLOSE"], traversed_edges(value["receipts"]))

    def test_full_optional_probe_route_closes(self):
        """DRAFT may send back to PROBE; the detour returns through the plan.

        Pre-260819 this fixture walked PROBE->REVISE, an edge the PREPARE loop
        removed: PROBE routes only sideways or back, and the loop's one door
        out is OUTLINE's gate."""
        value = run(
            [
                producer(1, "DRAFT", "v0", "v1", "PROBE"),
                producer(2, "PROBE", "v1", "v1", "EVIDENCE"),
                producer(3, "EVIDENCE", "v1", "v1", "OUTLINE"),
                producer(4, "OUTLINE", "v1", "v1", "DRAFT"),
                producer(5, "DRAFT", "v1", "v2", "CHECK"),
                check(6, "v2"),
            ]
        )
        self.assertClean(value)

    def test_full_outline_to_compile_route_closes(self):
        """The 260819 happy path: the PREPARE loop converges, then the linear
        tail runs to CLOSE. The pre-260819 fixture walked EVIDENCE->REVISE,
        which the loop removed."""
        value = run(
            [
                producer(1, "OUTLINE", "v0", "v1", "PROBE"),
                producer(2, "PROBE", "v1", "v1", "EVIDENCE"),
                producer(3, "EVIDENCE", "v1", "v1", "OUTLINE"),
                producer(4, "OUTLINE", "v1", "v1", "DRAFT"),
                producer(5, "DRAFT", "v1", "v2", "REVISE"),
                producer(6, "REVISE", "v2", "v3", "COMPILE"),
                producer(7, "COMPILE", "v3", "v3", "CHECK"),
                check(8, "v3"),
            ]
        )
        self.assertClean(value)

    def test_check_can_route_to_outline(self):
        value = run(
            [
                check(1, "v1", "OUTLINE"),
                producer(2, "OUTLINE", "v1", "v2", "DRAFT"),
                producer(3, "DRAFT", "v2", "v3", "CHECK"),
                check(4, "v3"),
            ]
        )
        self.assertClean(value)

    def test_check_revise_requires_a_new_check(self):
        value = run(
            [
                check(1, "v1", "REVISE"),
                producer(2, "REVISE", "v1", "v2", "CHECK"),
                check(3, "v2"),
            ]
        )
        self.assertClean(value)

    def test_check_can_route_to_probe(self):
        value = run(
            [
                check(1, "v1", "PROBE"),
                producer(2, "PROBE", "v1", "v1", "EVIDENCE"),
                producer(3, "EVIDENCE", "v1", "v1", "OUTLINE"),
                producer(4, "OUTLINE", "v1", "v1", "DRAFT"),
                producer(5, "DRAFT", "v1", "v2", "CHECK"),
                check(6, "v2"),
            ]
        )
        self.assertClean(value)

    def test_check_can_route_to_evidence(self):
        """The current phase token, under its current name."""
        value = run(
            [
                check(1, "v1", "EVIDENCE"),
                producer(2, "EVIDENCE", "v1", "v1", "OUTLINE"),
                producer(3, "OUTLINE", "v1", "v1", "DRAFT"),
                producer(4, "DRAFT", "v1", "v2", "CHECK"),
                check(5, "v2"),
            ]
        )
        self.assertClean(value)

    def test_probe_and_evidence_audit_identically(self):
        """A receipt written before the 260816 rename still audits.

        `_runs/page/` receipts are immutable by contract, so the auditor
        normalizes the retired token instead of failing the run that used it.
        The two runs differ only in that token and must produce the same
        findings AND the same traversed edges.
        """
        def build(token):
            return run(
                [
                    producer(1, "DRAFT", "v0", "v1", token),
                    producer(2, token, "v1", "v1", "REVISE"),
                    producer(3, "REVISE", "v1", "v2", "CHECK"),
                    check(4, "v2", "CLOSE", verdict="pass"),
                ]
            )

        old, new = build("PROBE"), build("EVIDENCE")
        self.assertEqual(audit_run(old), audit_run(new))
        self.assertEqual(traversed_edges(old["receipts"]),
                         traversed_edges(new["receipts"]))
        self.assertIn("EVIDENCE", " ".join(traversed_edges(old["receipts"])))

    def test_check_to_draft_begins_a_new_round(self):
        value = run(
            [
                check(1, "v1", "DRAFT", reopens=True),
                producer(2, "DRAFT", "v1", "v2", "CHECK", round=2),
                check(3, "v2", round=2),
            ]
        )
        self.assertClean(value)

    def test_failure_injection_catches_self_approval(self):
        value = run(
            [
                producer(1, "REVISE", "v1", "v2", "CHECK", actor="same-agent"),
                check(2, "v2", actor="same-agent"),
            ]
        )
        self.assertIn("self-approval", self.codes(value))

    def test_failure_injection_catches_change_after_check(self):
        value = run([check(1, "v1")], final_version="v2")
        self.assertIn("changed-after-check", self.codes(value))

    def test_failure_injection_catches_illegal_route(self):
        receipt = producer(1, "DRAFT", "v0", "v1", "CHECK")
        receipt["route"] = "CLOSE"
        value = run([receipt])
        codes = self.codes(value)
        self.assertIn("illegal-route", codes)
        self.assertIn("producer-closed", codes)

    def test_required_human_gate_cannot_be_fabricated(self):
        gate = {"required": True, "status": "pending", "evidence": []}
        value = run([check(1, "v1", gate=gate)])
        self.assertIn("human-gate-fabricated", self.codes(value))

    def test_required_human_gate_with_evidence_can_close(self):
        gate = {"required": True, "status": "passed", "evidence": ["JL 260804: approved"]}
        value = run([check(1, "v1", gate=gate)])
        self.assertClean(value)

    def test_explicit_hold_is_a_valid_terminal(self):
        receipt = check(1, "v1", "HOLD", verdict="blocked")
        value = run([receipt], status="blocked")
        self.assertClean(value)

    def test_max_steps_and_nonterminal_trace_are_detected(self):
        receipts = [producer(1, "DRAFT", "v0", "v1", "DRAFT")]
        value = run(receipts, status="hold", max_steps=0)
        value["limits"]["max_steps"] = 0
        self.assertIn("trace-not-terminal", self.codes(value))

    def test_receipts_cannot_exceed_declared_max_steps(self):
        value = run(
            [
                producer(1, "DRAFT", "v0", "v1", "CHECK"),
                check(2, "v1"),
            ],
            max_steps=1,
        )
        self.assertIn("max-steps-exceeded", self.codes(value))

    def test_route_phase_and_round_mismatches_are_detected(self):
        value = run(
            [
                check(1, "v1", "DRAFT", reopens=True),
                producer(2, "REVISE", "v1", "v2", "CHECK", round=1),
                check(3, "v2"),
            ]
        )
        codes = self.codes(value)
        self.assertIn("route-phase-mismatch", codes)
        self.assertIn("round-sequence", codes)

    def test_blocked_worker_must_hold(self):
        receipt = producer(1, "PROBE", "v1", "v1", "PROBE")
        receipt["status"] = "blocked"
        value = run([receipt], status="blocked")
        self.assertIn("failed-work-not-held", self.codes(value))

    def test_mutating_checked_version_is_detected(self):
        receipt = check(1, "v1")
        receipt["version_after"] = version("v2")
        value = run([receipt], final_version="v2")
        self.assertIn("checked-version-mismatch", self.codes(value))

    def test_symbolic_version_is_rejected(self):
        receipt = check(1, "v1")
        receipt["version_before"] = "source-v1:render-v1"
        receipt["version_after"] = "source-v1:render-v1"
        receipt["checked_version"] = "source-v1:render-v1"
        value = run([receipt], final_version="source-v1:render-v1")
        self.assertIn("invalid-version-format", self.codes(value))
        self.assertIn("invalid-final-version-format", self.codes(value))

    def test_builder_must_be_separate_from_producer_and_judge(self):
        producer_receipt = producer(
            1, "DRAFT", "v0", "v1", "CHECK", actor="same-builder", builder="same-builder"
        )
        judge_receipt = check(2, "v1", actor="same-builder", builder="same-builder")
        codes = self.codes(run([producer_receipt, judge_receipt]))
        self.assertIn("producer-is-builder", codes)
        self.assertIn("judge-is-builder", codes)

    def test_receipt_versions_must_be_continuous(self):
        value = run(
            [
                producer(1, "DRAFT", "v0", "v1", "PROBE"),
                producer(2, "PROBE", "v2", "v2", "CHECK"),
                check(3, "v2"),
            ]
        )
        self.assertIn("version-continuity", self.codes(value))

    def test_packet_identity_and_gate_must_match_the_run(self):
        gate = {"required": True, "status": "passed", "evidence": ["approval"]}
        value = run([check(1, "v1", gate=gate)], gate_required=False)
        value["packet"]["page"] = "another-page.md"
        codes = self.codes(value)
        self.assertIn("packet-run-mismatch", codes)
        self.assertIn("human-gate-contract-mismatch", codes)

    def test_missing_packet_is_rejected(self):
        value = run([check(1, "v1")])
        value.pop("packet")
        self.assertIn("missing-packet", self.codes(value))

    def test_packet_start_phase_must_match_first_receipt(self):
        value = run([check(1, "v1")])
        value["packet"]["start_phase"] = "DRAFT"
        self.assertIn("start-phase-mismatch", self.codes(value))

    def test_receipt_round_cannot_exceed_declared_bound(self):
        receipt = check(1, "v1", "HOLD", round=4, verdict="blocked")
        value = run([receipt], status="blocked")
        self.assertIn("max-rounds-exceeded", self.codes(value))

    def test_artifact_verification_recomputes_source_and_render_hashes(self):
        with tempfile.TemporaryDirectory() as temporary:
            board = Path(temporary)
            page = board / "QF1-page.md"
            rendered = board / "board/QF/QF1-page.html"
            rendered.parent.mkdir(parents=True)
            page.write_text("# exact source\n", encoding="utf-8")
            rendered.write_text("<h1>exact render</h1>\n", encoding="utf-8")
            actual = (
                f"{hashlib.sha256(page.read_bytes()).hexdigest()}:"
                f"{hashlib.sha256(rendered.read_bytes()).hexdigest()}"
            )
            value = run([check(1, actual)], final_version=actual)
            value.update({"board": str(board), "page": str(page)})
            self.assertEqual([], audit_artifacts(value))
            page.write_text("# changed source\n", encoding="utf-8")
            self.assertEqual(
                {"artifact-version-mismatch"},
                {finding.code for finding in audit_artifacts(value)},
            )

    def test_prepare_pause_allows_the_next_pass_after_hold(self):
        """260819 pause rule: a HOLD from OUTLINE/PROBE/EVIDENCE with an open
        required gate is a PAUSE between passes of one round, not a terminal.
        The live 260819 round appended one receipt per pass and 10 of 12 legal
        passes audited as receipt-after-terminal before this rule existed."""
        gate = {"required": True, "status": "pending",
                "evidence": ["outline approved: line, unticked"]}
        steps = []
        for i, phase in enumerate(("OUTLINE", "PROBE", "EVIDENCE", "OUTLINE"), 1):
            r = producer(i, phase, "v1", "v1", "HOLD")
            r["human_gate"] = dict(gate)
            steps.append(r)
        value = run(steps, status="hold", gate_required=True)
        self.assertNotIn("receipt-after-terminal", self.codes(value))

    def test_prepare_pause_still_requires_a_legal_next_phase(self):
        gate = {"required": True, "status": "pending",
                "evidence": ["outline approved: line, unticked"]}
        r1 = producer(1, "OUTLINE", "v1", "v1", "HOLD")
        r1["human_gate"] = dict(gate)
        r2 = producer(2, "REVISE", "v1", "v1", "HOLD")
        r2["human_gate"] = dict(gate)
        value = run([r1, r2], status="hold", gate_required=True)
        self.assertIn("route-phase-mismatch", self.codes(value))

    def test_cold_check_is_legal_from_a_prepare_pause(self):
        gate = {"required": True, "status": "pending",
                "evidence": ["outline approved: line, unticked"]}
        r1 = producer(1, "OUTLINE", "v0", "v1", "HOLD")
        r1["human_gate"] = dict(gate)
        r2 = check(2, "v1", "REVISE")
        value = run([r1, r2], status="revise", gate_required=True)
        codes = self.codes(value)
        self.assertNotIn("receipt-after-terminal", codes)
        self.assertNotIn("route-phase-mismatch", codes)

    def test_close_stays_terminal_even_with_an_open_gate(self):
        gate = {"required": True, "status": "pending",
                "evidence": ["outline approved: line, unticked"]}
        r1 = producer(1, "OUTLINE", "v0", "v1", "HOLD")
        r1["human_gate"] = dict(gate)
        r2 = check(2, "v1")
        r3 = producer(3, "OUTLINE", "v1", "v1", "HOLD")
        r3["human_gate"] = dict(gate)
        value = run([r1, r2, r3], status="hold", gate_required=True)
        self.assertIn("receipt-after-terminal", self.codes(value))



class PageLifecycleWorkflowContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (HERE / "ref/page-lifecycle.workflow.js").read_text(encoding="utf-8")

    def test_js_legal_table_matches_python(self):
        """The two route tables agree only by hand until this test: parse the
        js LEGAL block and compare it to src.page_lifecycle.LEGAL_ROUTES."""
        m = re.search(r"const LEGAL = \{(.*?)\n\}", self.script, re.S)
        self.assertIsNotNone(m)
        js = {}
        for row in re.finditer(r"(\w+): \[([^\]]*)\]", m.group(1)):
            js[row.group(1)] = set(re.findall(r"'([A-Z]+)'", row.group(2)))
        self.assertEqual({k: set(v) for k, v in LEGAL_ROUTES.items()}, js)

    def test_workflow_separates_producer_and_reviewer_agents(self):
        # One producer agent per phase since 260819; the base agent is the
        # dispatch FALLBACK, and the judge is never in the producer map.
        self.assertIn("const PRODUCER_AGENTS = {", self.script)
        for agent_name in (
            "haipipe-page-outline-agent",
            "haipipe-page-probe-agent",
            "haipipe-page-evidence-agent",
            "haipipe-page-draft-agent",
            "haipipe-page-revise-agent",
        ):
            self.assertIn(agent_name, self.script)
        self.assertIn(
            "agentType: PRODUCER_AGENTS[current] || 'haipipe-page-creator-agent'",
            self.script)
        self.assertIn("agentType: 'haipipe-page-check-agent'", self.script)
        self.assertNotIn("haipipe-page-check-agent'", str(
            self.script.split("const PRODUCER_AGENTS = {", 1)[1].split("}", 1)[0]))
        self.assertIn("Do not edit, rebuild, or cure a finding", self.script)

    def test_workflow_is_bounded_and_versions_every_check(self):
        self.assertIn("max_steps", self.script)
        self.assertIn("max_rounds", self.script)
        self.assertIn("checked_version", self.script)
        self.assertIn("version_id exactly as <source_sha256>:<render_sha256>", self.script)

    def test_workflow_uses_routes_not_a_fixed_phase_sequence(self):
        self.assertIn("let current = startPhase", self.script)
        self.assertIn("current = route", self.script)
        self.assertNotIn("DRAFT → PROBE → REVISE → CHECK", self.script)

    def test_mechanical_error_repair_routes_are_legal_from_every_phase(self):
        match = re.search(
            r"const MECHANICAL_REPAIR_ROUTE = \{(.*?)\n\}", self.script, re.S
        )
        self.assertIsNotNone(match)
        repair = dict(
            re.findall(r"(\w+):\s*'([A-Z]+)'", match.group(1))
        )
        self.assertEqual(set(LEGAL_ROUTES), set(repair))
        for phase, route in repair.items():
            with self.subTest(phase=phase, route=route):
                self.assertIn(route, LEGAL_ROUTES[phase])
        for phase in ("OUTLINE", "PROBE", "EVIDENCE"):
            self.assertEqual(phase, repair[phase])
        self.assertIn(
            "route = MECHANICAL_REPAIR_ROUTE[current] || 'HOLD'", self.script
        )


if __name__ == "__main__":
    unittest.main()
