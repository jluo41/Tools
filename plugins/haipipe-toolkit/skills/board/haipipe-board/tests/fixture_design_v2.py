"""Build a current (v0.4.0 / v2) Design Folder from a few item specs.

One source of fixture truth for the Design presenter tests AND the demo board
under ``skills/diagrams/DesignPlugin-Demo-260916-DesignBoard``.  Every Ticket,
Result, and receipt it writes satisfies ``haipipe-design-unit/scripts/check_unit.py``
so the presenter is exercised on contract-valid bytes, never on stubs.

    python3 tests/fixture_design_v2.py --demo     # regenerate the demo boards
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[2]
DEMO_BOARD = SKILLS / "diagrams" / "DesignPlugin-Demo-260916-DesignBoard"
DEMO_INSIGHT = SKILLS / "diagrams" / "DesignPlugin-Demo-260916-InsightBoard"
UNIT_CHECKER = SKILLS / "design" / "haipipe-design-unit" / "scripts" / "check_unit.py"

STAGES = ("commissioned", "generate-failed", "generated", "verified", "adopted", "declined")
HANDOFF_REL = "../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp(minutes: int) -> str:
    return f"2026-09-16T13:{minutes:02d}:00Z"


@dataclass
class ItemSpec:
    """One Design Item, its bet, its evidence, and how far its Runs progressed."""

    id: str
    title: str
    kind: str                      # venue kind: sms · ui-card · ...
    goal: str                      # what this design tries to do (design_intent.move)
    audience: str
    job: str
    content: str                   # the candidate text the Generate Run produces
    criteria: list[dict]           # v2 criteria rows
    acceptance: list[str]          # human-readable acceptance rules for the register
    stance: str = "generate"       # follow | challenge | explore | generate
    basis: str = "brief-only"      # brief-only | evidence-informed
    mode: str = ""                 # compose | revise | brainstorm | theory-driven | challenge
    expected: str = ""             # typed forecast: what should happen, for whom
    falsified: str = ""            # what observation would refute the bet
    evidence: list[str] = field(default_factory=list)   # "role · relative/path" lines
    stage: str = "adopted"         # historical demo default; current cases choose "verified"
    slug: str = ""
    human: str = "JL"
    designer: str = "designer-context-01"
    reviewer: str = "reviewer-context-02"
    words: str = ""                # the person's adoption/decline words


class FolderBuilder:
    def __init__(self, folder: Path, stem: str):
        self.folder = Path(folder)
        self.stem = stem
        self.counter = 0

    # -- primitives -------------------------------------------------------
    def write(self, rel: str, text: str) -> Path:
        path = self.folder / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def dump(self, rel: str, obj) -> Path:
        return self.write(rel, yaml.safe_dump(obj, sort_keys=False, allow_unicode=True))

    def ref(self, path: Path, root: Path | None = None) -> dict:
        root = (root or self.folder).resolve()
        rel = os.path.relpath(path.resolve(), root)
        return {"path": Path(rel).as_posix(), "sha256": digest(path)}

    def next_run(self, operation: str, slug: str) -> str:
        self.counter += 1
        return f"rd{self.counter:02d}_{operation}_{slug}"

    def evidence_inputs(self, spec: ItemSpec) -> list[dict]:
        rows = []
        for line in spec.evidence:
            role, rel = [p.strip() for p in line.split("·", 1)]
            path = (self.folder / rel).resolve()
            if not path.is_file():
                raise FileNotFoundError(f"{spec.id}: evidence file missing: {rel}")
            rows.append({"role": role, "path": rel, "sha256": digest(path)})
        return rows

    # -- decision Runs (human) ---------------------------------------------
    def commission(self, spec: ItemSpec, config_path: Path, decision: str = "release") -> str:
        run = self.next_run("commission", spec.slug)
        inputs = [self.ref(config_path)] + self.evidence_inputs(spec)
        ticket = {
            "schema": "haipipe.design-ticket/v2", "run": run,
            "run_type": "Design.commission", "operation": "commission",
            "item": spec.id, "target": spec.title,
            "actor": {"mode": "human", "owner": spec.human},
            "action": "release or hold the frozen commission", "inputs": inputs,
            "entry_gate": "the Design Item is registered",
            "exit_gate": {"mode": "human", "assertion": "decision names the exact config hash"},
            "routes": {"release": "generate", "hold": "HOLD"},
            "result": f"results/{run}/", "receipt": f"results/{run}/runtime.yaml",
        }
        ticket_path = self.dump(f"runs/{run}.yaml", ticket)
        self.dump(f"results/{run}/decision.yaml", {
            "run": run, "item": spec.id, "decision": decision, "actor": spec.human,
            "words": (f"Release {spec.id}: {spec.goal}" if decision == "release" else f"Hold {spec.id}"),
            "target": spec.title, "inputs": inputs, "at": stamp(1),
        })
        self.dump(f"results/{run}/runtime.yaml", {
            "run": run, "run_type": "Design.commission", "operation": "commission",
            "item": spec.id, "family": "design", "target": spec.title,
            "actor": {"mode": "human", "owner": spec.human}, "action": decision,
            "status": "complete", "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
            "ticket_sha256": digest(ticket_path), "inputs": inputs,
            "entry_gate": {"status": "passed", "assertion": "the Design Item is registered"},
            "exit_gate": {"status": "passed", "assertion": "decision recorded"},
            "route": "generate" if decision == "release" else "HOLD",
            "terminal_outcome": decision,
            "started_at": stamp(0), "finished_at": stamp(1), "failure": None,
        })
        return run

    def adopt(self, spec: ItemSpec, gen_run: str, ver_run: str, decision: str, preview: Path) -> str:
        run = self.next_run("adopt", spec.slug)
        gen_result = self.folder / "results" / gen_run / "result.yaml"
        ver_result = self.folder / "results" / ver_run / "result.yaml"
        artifact = self.folder / "results" / gen_run / "content" / f"{spec.kind}.txt"
        inputs = [self.ref(gen_result), self.ref(ver_result), self.ref(preview)]
        ticket = {
            "schema": "haipipe.design-ticket/v2", "run": run,
            "run_type": "Design.adopt", "operation": "adopt",
            "item": spec.id, "target": f"{spec.title} · exact verified candidate",
            "actor": {"mode": "human", "owner": spec.human},
            "action": "adopt, decline, revise, or hold the exact candidate", "inputs": inputs,
            "candidates": [{"run": gen_run, **self.ref(artifact)}],
            "verification": [{"run": ver_run, **self.ref(ver_result)}],
            "preview": self.ref(preview),
            "entry_gate": "independent verify passed",
            "exit_gate": {"mode": "human", "assertion": "decision names candidate hash"},
            "routes": {"adopt": "CLOSE", "decline": "CLOSE", "revise": "generate", "hold": "HOLD"},
            "result": f"results/{run}/", "receipt": f"results/{run}/runtime.yaml",
        }
        ticket_path = self.dump(f"runs/{run}.yaml", ticket)
        self.dump(f"results/{run}/decision.yaml", {
            "run": run, "item": spec.id, "decision": decision, "actor": spec.human,
            "words": spec.words or f"{decision.title()} {spec.id} v1",
            "candidate": {"run": gen_run, **self.ref(artifact)},
            "verification": {"run": ver_run, **self.ref(ver_result)},
            "preview": self.ref(preview), "at": stamp(9),
        })
        self.dump(f"results/{run}/runtime.yaml", {
            "run": run, "run_type": "Design.adopt", "operation": "adopt",
            "item": spec.id, "family": "design", "target": ticket["target"],
            "actor": {"mode": "human", "owner": spec.human}, "action": decision,
            "status": "complete", "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
            "ticket_sha256": digest(ticket_path), "inputs": inputs,
            "entry_gate": {"status": "passed", "assertion": "independent verify passed"},
            "exit_gate": {"status": "passed", "assertion": "decision recorded"},
            "route": "CLOSE" if decision in ("adopt", "decline") else decision,
            "terminal_outcome": decision,
            "started_at": stamp(8), "finished_at": stamp(9), "failure": None,
        })
        return run

    # -- worker Runs (agent) ------------------------------------------------
    def config(self, spec: ItemSpec, run: str, review_mode: str) -> Path:
        mode = spec.mode or ("challenge" if spec.stance == "challenge" else "compose")
        return self.dump(f"scripts/config/{run}.yaml", {
            "goal": spec.goal, "kind": spec.kind, "mode": mode, "basis": spec.basis, "item": spec.id,
            "design_intent": {"move": spec.goal, "basis": spec.basis, "stance": spec.stance,
                              "expected_effect": spec.expected or None,
                              "failure_condition": spec.falsified or None},
            "unit": {"shape": "single", "count": 1}, "max_iterations": 2,
            "review_mode": review_mode, "criteria": spec.criteria,
        })

    def worker_ticket(self, spec: ItemSpec, run: str, operation: str, actor: str,
                      config_path: Path, approval: Path, targets: list[dict]) -> Path:
        inputs = self.evidence_inputs(spec)
        data = {
            "schema": "haipipe.design-ticket/v2", "run": run, "operation": operation,
            "worker": "haipipe-design-unit", "actor": actor, "item": spec.id,
            "target": spec.title, "config": self.ref(config_path),
            "approval": {"actor": spec.human, "record": self.ref(approval)},
            "inputs": inputs, "targets": targets,
        }
        ticket = self.dump(f"runs/{run}.yaml", data)
        self.dump(f"results/{run}/runtime.yaml", {
            "run": run, "family": "design", "operation": operation, "item": spec.id,
            "target": spec.title, "status": "planned",
            "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
            "ticket_sha256": digest(ticket),
            "inputs": [data["config"], data["approval"]["record"]] + inputs + targets,
            "worker": {"kind": "skill", "name": "haipipe-design-unit", "actor": actor},
        })
        return ticket

    def finish(self, run: str, status: str, minute: int, failure: str | None = None,
               route: str | None = None):
        path = self.folder / "results" / run / "runtime.yaml"
        runtime = yaml.safe_load(path.read_text(encoding="utf-8"))
        runtime.update(status=status, started_at=stamp(minute - 1), finished_at=stamp(minute),
                       failure=failure)
        if route:
            runtime["route"] = route
        self.dump(f"results/{run}/runtime.yaml", runtime)

    @staticmethod
    def evaluate(text: str, criterion: dict) -> str:
        kind = criterion["kind"]
        if kind == "max_chars":
            return "pass" if len(text) <= criterion["value"] else "fail"
        if kind == "contains":
            return "pass" if criterion["value"] in text else "fail"
        if kind == "excludes":
            return "pass" if criterion["value"] not in text else "fail"
        return "pass"

    @staticmethod
    def evidence(text: str, criterion: dict, status: str) -> str:
        kind = criterion["kind"]
        if kind == "max_chars":
            return f"{len(text)} characters; configured maximum is {criterion['value']}"
        if kind in ("contains", "excludes"):
            return f"'{criterion['value']}' {'found' if (criterion['value'] in text) else 'absent'} in the artifact"
        return f"read against: {criterion.get('description', criterion['id'])} · {status}"

    def generate(self, spec: ItemSpec, approval: Path) -> tuple[str, Path]:
        run = self.next_run("generate", spec.slug)
        config_path = self.config(spec, run, "self")
        ticket = self.worker_ticket(spec, run, "generate", spec.designer, config_path, approval, [])
        out = self.folder / "results" / run
        artifact = self.write(f"results/{run}/content/{spec.kind}.txt", spec.content)
        checks = [{"target": f"content/{spec.kind}.txt", "criterion": c["id"],
                   "status": self.evaluate(spec.content, c),
                   "evidence": self.evidence(spec.content, c, self.evaluate(spec.content, c))}
                  for c in spec.criteria]
        check_path = self.dump(f"results/{run}/checks.yaml", {"checks": checks})
        verdict = "fail" if any(c["status"] == "fail" for c in checks) else "pass"
        self.dump(f"results/{run}/result.yaml", {
            "schema": "haipipe.design-result/v2", "run": run, "operation": "generate",
            "target": spec.title, "producer": spec.designer,
            "ticket_sha256": digest(ticket), "config_sha256": self.ref(config_path)["sha256"],
            "artifacts": [self.ref(artifact, out)], "checks": self.ref(check_path, out),
            "targets": [], "verdict": verdict,
        })
        if verdict == "fail":
            # The failure reason is the failing checks' own evidence, never a
            # hand-typed number that can drift from the bytes.
            failing = [f"{c['criterion']}: {c['evidence']}" for c in checks if c["status"] == "fail"]
            self.finish(run, "failed", 4, "; ".join(failing) + " · route revise", route="generate")
        else:
            self.finish(run, "complete", 4, route="verify")
        return run, out / "result.yaml"

    def verify(self, spec: ItemSpec, approval: Path, gen_result: Path) -> str:
        run = self.next_run("verify", spec.slug)
        config_path = self.config(spec, run, "independent")
        targets = [self.ref(gen_result)]
        ticket = self.worker_ticket(spec, run, "verify", spec.reviewer, config_path, approval, targets)
        out = self.folder / "results" / run
        text = (gen_result.parent / "content" / f"{spec.kind}.txt").read_text(encoding="utf-8")
        checks = [{"target": f"{targets[0]['path']}::content/{spec.kind}.txt",
                   "criterion": c["id"], "status": self.evaluate(text, c),
                   "evidence": self.evidence(text, c, self.evaluate(text, c))}
                  for c in spec.criteria]
        check_path = self.dump(f"results/{run}/checks.yaml", {"checks": checks})
        verdict = "fail" if any(c["status"] == "fail" for c in checks) else "pass"
        self.dump(f"results/{run}/result.yaml", {
            "schema": "haipipe.design-result/v2", "run": run, "operation": "verify",
            "target": spec.title, "producer": spec.reviewer,
            "ticket_sha256": digest(ticket), "config_sha256": self.ref(config_path)["sha256"],
            "artifacts": [], "checks": self.ref(check_path, out), "targets": targets,
            "verdict": verdict,
        })
        self.finish(run, "complete", 6, route=("delivery" if spec.stage == "verified" else "adopt")
                    if verdict == "pass" else "generate")
        return run

    # -- one item, end to end -------------------------------------------------
    def item(self, spec: ItemSpec) -> dict:
        assert spec.stage in STAGES, spec.stage
        spec.slug = spec.slug or spec.id.lower()
        pre_config = self.config(spec, f"commission_{spec.slug}", "self")
        commission = self.commission(spec, pre_config)
        approval = self.folder / "results" / commission / "decision.yaml"
        record = {"item": spec.id, "commission": commission}
        if spec.stage == "commissioned":
            return record
        gen_run, gen_result = self.generate(spec, approval)
        record["generate"] = gen_run
        if spec.stage in ("generate-failed", "generated"):
            return record
        ver_run = self.verify(spec, approval, gen_result)
        record["verify"] = ver_run
        if spec.stage == "verified":
            return record
        preview = self.write(f"delivery/render/{self.stem}-{spec.id}-v1.txt", spec.content)
        manifest = self.folder / "delivery" / "render" / "manifest.json"
        entries = json.loads(manifest.read_text()) if manifest.is_file() else []
        entries.append({"item": spec.id, "render": preview.name, "candidate": gen_run,
                        "sha256": digest(preview), "version": 1})
        self.write("delivery/render/manifest.json", json.dumps(entries, indent=2))
        decision = "adopt" if spec.stage == "adopted" else "decline"
        record["adopt"] = self.adopt(spec, gen_run, ver_run, decision, preview)
        return record

    def register(self, title: str, specs: list[ItemSpec]) -> Path:
        lines = [f"# {title} · Design Items", "",
                 "One block per design target: the bet, its evidence, and its acceptance rules.",
                 "Runs name an item through `item:`; state is derived from those Runs, never typed here.", ""]
        for spec in specs:
            lines += [f"## {spec.id} · {spec.title}", f"type: {spec.kind}",
                      f"audience: {spec.audience}", f"job: {spec.job}",
                      f"goal: {spec.goal}", f"stance: {spec.stance}", f"basis: {spec.basis}",
                      f"mode: {spec.mode or ('challenge' if spec.stance == 'challenge' else 'compose')}"]
            if spec.expected:
                lines.append(f"expected: {spec.expected}")
            if spec.falsified:
                lines.append(f"falsified: {spec.falsified}")
            if spec.evidence:
                lines.append("evidence:")
                lines += [f"- {line}" for line in spec.evidence]
            lines.append("acceptance:")
            lines += [f"- {rule}" for rule in spec.acceptance]
            lines.append("")
        return self.write(f"outline/{self.stem}-design-items.md", "\n".join(lines))


def build_design_folder(folder: Path, stem: str, title: str, opening: str,
                        specs: list[ItemSpec], wipe: bool = True) -> dict:
    """Write a complete current Design Folder and return the run ids per item."""
    folder = Path(folder)
    if wipe and folder.exists():
        for sub in ("runs", "results", "delivery", "scripts", "outline", "workflow"):
            shutil.rmtree(folder / sub, ignore_errors=True)
    builder = FolderBuilder(folder, stem)
    builder.write(f"{stem}.md", (
        f"# {title}\nfolder-kind: design\n\n## Opening\n\n{opening}\n\n"
        "## Outline\n\nDesign Items are registered in `outline/" + stem + "-design-items.md`;\n"
        "their Commission, Generate and Verify records are `rdNN_*` Runs.\n"
        "Some fixtures also contain historical Adopt records for reader compatibility.\n\n"
        "## Content\n\nCandidate wording lives in immutable Design Run Results, never here.\n\n"
        "## Aims\n\n### A1 · Every registered item has a truthful state\n\n"
        "- ⬜ A1.1 · independently verified and ready, or a named wait/failure.\n"
    ))
    builder.register(title, specs)
    return {spec.id: builder.item(spec) for spec in specs}


def bind_insight_handoff(page: Path, signature: str = "JL 260828"):
    """Synthetic owner receipts for the current exact-hash handoff contract."""
    folder = page.parent
    board = folder.parent.parent
    register = board / "0-MT-meta/MT04-question-wisdom/MT04-question-wisdom.md"
    register.parent.mkdir(parents=True, exist_ok=True)
    page_id = page.stem.split("-", 1)[0]
    register.write_text(
        "# Synthetic Wisdom register\nfolder-kind: question\nquestion-rung: wisdom\n\n"
        "```text\nid   question          Gen-1   F·full\n"
        f"QW1  What counsel?     (none)  ✅ {page_id}\n```\n", encoding="utf-8")
    workflow = folder / "workflow"
    workflow.mkdir(exist_ok=True)
    dependency = workflow / "synthetic-evidence.txt"
    dependency.write_text("Synthetic accepted evidence for isolated tests only.\n", encoding="utf-8")
    pin = {"path": page.name, "version": "fixture-v1", "sha256": digest(page)}
    dependencies = [{"path": "workflow/synthetic-evidence.txt", "sha256": digest(dependency)}]
    def receipt(path, anchor, payload):
        import os
        body = "```yaml\n" + yaml.safe_dump(payload, sort_keys=False) + "```"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# Synthetic owner log\n\n### {anchor}\n\n{body}\n", encoding="utf-8")
        return {"path": os.path.relpath(path, folder) + "#" + anchor,
                "sha256": hashlib.sha256(body.encode()).hexdigest()}

    signed = receipt(folder / "outline" / f"{page.stem}-log.md", "signed-fixture", {
        "key": "GI5", "status": "passed", "actor": "synthetic-owner",
        "authority": "haipipe-insight-wisdom", "workflow_runtime_id": "fixture-workflow",
        "page": pin, "signature": signature, "dependencies": dependencies})
    settled = receipt(register.parent / "outline" / f"{register.stem}-log.md", "settled-fixture", {
        "key": "GI6", "status": "passed", "actor": "synthetic-owner",
        "authority": "haipipe-insight-question", "workflow_runtime_id": "fixture-workflow",
        "page": pin, "signature_receipt": signed,
        "target": {"partition": "F", "question": "QW1"}})
    (workflow / "handoff.yaml").write_text(yaml.safe_dump({
        "schema": "haipipe.insight-handoff/v1", "page": pin, "dependencies": dependencies,
        "gi5": signed, "gi6": [settled]}), encoding="utf-8")



def build_insight_board(board: Path) -> Path:
    """The one-page InsightBoard the demo DesignBoard reads: one signed W handoff."""
    board = Path(board)
    page = board / "1-F-full" / "FW01-send-salience" / "FW01-send-salience.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    (board / "board.md").write_text(
        "# Design Plugin Playground · InsightBoard\nboard-kind: insight-board\n"
        "spine: One signed Wisdom handoff that the sibling DesignBoard reads.\n"
        "close: The one W page is signed; nothing else is asked of this fixture.\n"
        "store: results/demo-insight\n\n## Topic\n\nA one-page InsightBoard fixture: it exists so the "
        "Design demo has a real,\nsigned Wisdom handoff to bind. Its finding is condensed from the SMSR2v1 board.\n\n"
        "## Pages\n\n### F · Full ladder\n1-F-full/FW01-send-salience/FW01-send-salience.md\n",
        encoding="utf-8")
    page.write_text(
        "# Send salience, and stop calling the rest a slate\n\n"
        "state: ✅ SETTLED · answers QW1 · handoff released\nfolder-kind: wisdom\n"
        "question-rung: wisdom\nowner: JL\n\n## Opening\n\n"
        "Which messages should round 2 send to exploit what round 1 established, if any?\n\n"
        "One: keep sending `salience`. The answer is narrow because the evidence is narrow.\n\n"
        "## Content\n\n### 3 · Counsel\n\n```text\n"
        "id   counsel                                                       from\n"
        "W1   DO send `salience` to the whole population.                   FK01 · K1\n"
        "W2   DO NOT vary the message by age, gender, send day or region.   FK02 · K1\n"
        "W3   DO NOT ship a message this experiment never ran.              FK03 · K1\n```\n\n"
        "### 5 · Design Handoff\n\n```text\n"
        "FINDING       Of thirteen arms fielded on 444,691 invitations, `salience`\n"
        "              leads at 66.06% click [65.56, 66.56] and also leads on\n"
        "              authentication. The nine middle arms are not separable.\n"
        "STRENGTH      STRONG on the two extremes. STRONG on the segmentation null.\n"
        "BOUNDARY      444,691 invitations, 2025-06-16 to 2025-07-03, SMS\n"
        "              prescription-review only; click and authentication only.\n"
        "CONSEQUENCE   Design may field `salience` verbatim; it may not segment,\n"
        "              and it may not predict a lift for any untested message.\n"
        "OVERREACH     No new message is warranted by this board.\n```\n\n"
        "SERVES        QW1 · BR00-brief A6.1 · Design-01\n\nsigned: ✅ JL 260828\n",
        encoding="utf-8")
    bind_insight_handoff(page)
    return board


SMS_SALIENCE = ("Hi, it's Dr. {NAME}'s office. New prescription details require "
                "your review: Reply STOP to opt-out")
SMS_ATTRIBUTION = ("New prescription details require your review. Please check your "
                   "patient portal today to confirm the change with your care team: "
                   "Reply STOP to opt-out")


def sms_criteria(max_chars: int = 160) -> list[dict]:
    return [
        {"id": "length", "kind": "max_chars", "value": max_chars},
        {"id": "optout", "kind": "contains", "value": "Reply STOP to opt-out"},
        {"id": "nolift", "kind": "excludes", "value": "%"},
        {"id": "tone", "kind": "semantic",
         "description": "The recipient can decline the prescription review without pressure.",
         "observation": "Read the whole SMS as a recipient and inspect its stated STOP path.",
         "pass_when": "Review request and opt-out are clear; no penalty or false urgency is stated.",
         "fail_when": "The text hides refusal, threatens a consequence, or falsely claims urgency.",
         "not_verifiable_when": "The consequences of stopping depend on information absent from the pinned source."},
    ]


def demo_specs() -> dict[str, dict]:
    """The demo board: Design-01 (two items, one adopted, one failed) and Design-02 (verify owed)."""
    return {
        "Design-01-all-patients-prescription-review-sms": dict(
            title="Prescription review SMS for all patients",
            opening=("Design for all patients (prescription review, sms), "
                     "listed in the Brief's design tasks."),
            specs=[
                ItemSpec(id="ITEM01", title="Send the tested winner, verbatim", kind="sms",
                         goal="Field the salience template exactly as round 1 sent it",
                         audience="all patients",
                         job="prescription review", content=SMS_SALIENCE,
                         stance="follow", basis="evidence-informed",
                         expected=("salience stays the best arm on click and authentication "
                                   "when re-fielded against any concurrent arm"),
                         falsified=("a concurrently fielded round-2 arm beats it on click "
                                    "outside overlapping intervals"),
                         evidence=[f"handoff · {HANDOFF_REL}"],
                         criteria=sms_criteria() + [
                             {"id": "provider", "kind": "contains", "value": "{NAME}"}],
                         acceptance=["≤ 160 characters including the opt-out suffix",
                                     "ends with 'Reply STOP to opt-out' verbatim",
                                     "carries the provider-name placeholder {NAME}",
                                     "no predicted-lift text",
                                     "byte-identical to the fielded salience template"],
                         stage="adopted",
                         words="Adopt ITEM01 v1: byte-identical to the fielded salience template, warrant P01"),
                ItemSpec(id="ITEM02", title="Attribution removed", kind="sms",
                         goal="Test whether the message works without the provider attribution",
                         audience="all patients",
                         job="prescription review", content=SMS_ATTRIBUTION,
                         stance="challenge", basis="evidence-informed", mode="challenge",
                         expected="click does not fall when the provider attribution is removed",
                         falsified="click falls outside the attributed arm's interval",
                         evidence=[f"evidence · {HANDOFF_REL}"],
                         criteria=sms_criteria(max_chars=120),
                         acceptance=["≤ 120 characters including the opt-out suffix",
                                     "ends with 'Reply STOP to opt-out' verbatim",
                                     "no provider name and no {NAME} placeholder",
                                     "no predicted-lift text"],
                         stage="generate-failed"),
            ]),
        "Design-02-patients-refill-due-refill-review-ui-card": dict(
            title="Refill review app card for patients with a refill due within 7 days",
            opening=("Design for patients with a refill due within 7 days (refill review, ui-card), "
                     "listed in the Brief's design tasks."),
            specs=[
                ItemSpec(id="ITEM01", title="Refill approaching card", kind="ui-card",
                         goal="Make the refill date and the one next action visible at a glance",
                         audience="patients with a refill due within 7 days",
                         job="refill review", slug="refill-card",
                         content=("Your refill is coming up soon.\nReview options\n"
                                  "Refill due: {REFILL_DATE}"),
                         criteria=[
                             {"id": "date", "kind": "contains", "value": "{REFILL_DATE}"},
                             {"id": "cta", "kind": "contains", "value": "Review options"},
                             {"id": "length", "kind": "max_chars", "value": 200},
                             {"id": "layout", "kind": "visual",
                              "description": "one heading, one action, one date; fits a 320px card",
                              "observation": "Inspect the pinned 320px-wide render at 100% scale.",
                              "pass_when": "The date, one action, and one heading are visible without horizontal scrolling.",
                              "fail_when": "Any required element is clipped, hidden, or overlaps another.",
                              "not_verifiable_when": "The exact render or viewport measurement is missing."}],
                         acceptance=["shows the refill date placeholder {REFILL_DATE}",
                                     "exactly one action: 'Review options'",
                                     "fits a 320px card with one heading"],
                         stage="generated"),
            ]),
    }


def demo_runs_at_risk(board: Path = DEMO_BOARD) -> dict[str, int]:
    """Run records on the demo that a rebuild would delete, by folder (audit H10)."""
    out = {}
    for stem in demo_specs():
        runs = board / "2-Design" / stem / "runs"
        count = len(list(runs.glob("rd*_*.yaml"))) if runs.is_dir() else 0
        if count:
            out[stem] = count
    return out


def build_demo(board: Path = DEMO_BOARD, insight: Path = DEMO_INSIGHT, force: bool = False) -> dict:
    """Rebuild the demo boards from the fixture.  The demo also holds runs people made
    by clicking on it, so a rebuild over existing runs is refused unless forced."""
    at_risk = demo_runs_at_risk(board)
    if at_risk and not force:
        raise SystemExit("refused: rebuilding would delete " + ", ".join(f"{n} runs in {k}" for k, n in at_risk.items())
                         + "; pass --force only if those runs may go")
    build_insight_board(insight)
    out = {}
    for stem, spec in demo_specs().items():
        folder = board / "2-Design" / stem
        out[stem] = build_design_folder(folder, stem, spec["title"], spec["opening"], spec["specs"])
    return out


def audit(folder: Path) -> list[str]:
    import importlib.util
    spec = importlib.util.spec_from_file_location("design_unit_gate", UNIT_CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit_folder(Path(folder))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="regenerate the demo boards")
    parser.add_argument("--force", action="store_true", help="delete the demo's existing runs while rebuilding")
    args = parser.parse_args()
    if not args.demo:
        parser.error("choose --demo")
    built = build_demo(force=args.force)
    for stem, runs in built.items():
        issues = audit(DEMO_BOARD / "2-Design" / stem)
        print(stem, "· audit:", "PASS" if not issues else issues)
