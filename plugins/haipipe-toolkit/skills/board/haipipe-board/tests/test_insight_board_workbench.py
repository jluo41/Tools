"""Tests for the Board-level Insight workbench: one selected cell, five Spaces.

The fixture mirrors the real A00 board's shapes: an ASCII register grid with
one column per partition, a D page that names a run receipt, and a W page
with a signed handoff.  When the real A00 board is present it is read too,
because the parsers exist for that board's exact formatting.
"""

from __future__ import annotations

import unittest
import hashlib
import os
import yaml
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from live.insightboard import (
    _prepare_question_row,
    _task_calls,
    _board_by_name,
    _cell_view,
    _parse_register,
    register_question,
    board_snapshot,
    groom_snapshot,
    handoff_records,
    insight_boards,
    is_insight_board,
    page_cells,
    render_insight_board,
    render_page_insight,
)

REAL = Path("/Users/jluo41/Desktop/DrFirst-SPACE")
REAL_BOARD = REAL / "examples-5-design/Project-Application-SMSDesign/applications/A00_InsightBoard-SMSR2v1-260821"


def page(folder: Path, stem: str, body: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{stem}.md"
    path.write_text(body, encoding="utf-8")
    return path


def board_fixture(root: Path) -> Path:
    board = root / "Demo-InsightBoard"
    page(board / "0-MT-meta" / "MT00-meta", "MT00-meta",
         "# Meta\n\nstate: ✅ SETTLED\npage-type: meta\nowner: JL\n\n## Content\n"
         "extract  demo_dikw_input.parquet\n"
         "F      full          where: []  declared unfiltered      full.yaml   1-F-full/\n"
         "                     1,000 of 1,000 rows · 100.0000%\n"
         "B      young         age lt 40                          young.yaml  2-B-young/\n"
         "                       400 of 1,000 rows ·  40.0000%\n")
    page(board / "0-MT-meta" / "MT01-question-data", "MT01-question-data",
         "# Data questions\n\nstate: ✅ SETTLED · 1 question\npage-type: question\nquestion-rung: data\nowner: JL\n\n"
         "## Content\n\n```text\nid   question                 Gen-1   F·full   B·young\n"
         "QD1  what does the extract   Data/1  ✅ FD01  🚫 F-only\n     hold?\n```\n")
    page(board / "0-MT-meta" / "MT04-question-wisdom", "MT04-question-wisdom",
         "# Wisdom questions\n\nstate: ✅ SETTLED\npage-type: question\nquestion-rung: wisdom\nowner: JL\n\n"
         "## Content\n\n```text\nid    question           Gen-1     partition   QW1\n"
         "QW1   what to send?      Wisdom/1  F · full    ✅ FW01\n"
         "                                   B · young   🚫 F-only\n```\n")
    page(board / "1-F-full" / "FD01-extract-shape", "FD01-extract-shape",
         "# Extract shape\n\nstate: ✅ SETTLED · answers QD1\npage-type: data\nowner: JL\n\n## Opening\n\nWhat is in the extract?\n\n"
         "## Content\n\n```text\nrun receipt    results/full/runtime.yaml    status ok\n```\n\n```text\nD1   rows   1,000   counts.csv\n```\n"
         "\n### 📥 Input files\n- `../../_WorkSpace/Store/Demo-InsightBoard/T01_profile/01_shape/QA/1.md`\n\n## Log\n\n260901 · Created.\n")
    page(board / "1-F-full" / "FW01-what-to-send", "FW01-what-to-send",
         "# Send the one arm\n\nstate: ✅ SETTLED · answers QW1\npage-type: wisdom\nowner: JL\n\n## Opening\n\nSend `a`.\n\n"
         "## Content\n\n```text\nW1  ←  FD01 · D1   one row\n```\n\n```text\nW1   DO send `a`.        FD01 · D1\n```\n\n"
         "#### 4 · Forbidden Overreach\n\n```text\n❌ Do not say why.\n\nSERVES        QW1 · brief\n\nsigned: ✅ JL 260902\n```\n\n## Log\n\n260902 · Signed.\n")
    (board / "2-B-young").mkdir()          # registered partition, no page yet
    (board / "board.md").write_text(
        "# Demo Insight Board\n\nboard-kind: insight-board\nstore: _WorkSpace/Store/Demo-InsightBoard\n\n"
        "## Topic\n\nOne question, one extract.\n", encoding="utf-8")
    receipt = root / "_WorkSpace/Store/Demo-InsightBoard/T01_profile/01_shape/results/full/runtime.yaml"
    receipt.parent.mkdir(parents=True)
    receipt.write_text("status: ok\ncall: full\ntask: T01_profile/01_shape\nstarted: 2026-09-01T10:00:00Z\n"
                       "duration_s: 3\ngit_sha: abc1234\n", encoding="utf-8")
    return board


def current_handoff_fixture(board: Path, extra_dependency: Path | None = None):
    """Synthetic owner receipts; no real person approval or scientific claim."""
    source = board / "1-F-full/FW01-what-to-send/FW01-what-to-send.md"
    folder = source.parent

    def pin(path):
        return {"path": os.path.relpath(path, folder), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def log_record(path, anchor, data):
        body = "```yaml\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "```"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# Log\n\n### {anchor}\n\n{body}\n", encoding="utf-8")
        return {"path": os.path.relpath(path, folder) + "#" + anchor,
                "sha256": hashlib.sha256(body.encode()).hexdigest()}

    page_pin = {**pin(source), "version": "v001"}
    dependencies = [pin(board / "0-MT-meta/MT00-meta/MT00-meta.md"),
                    pin(board / "1-F-full/FD01-extract-shape/FD01-extract-shape.md")]
    if extra_dependency:
        dependencies.append(pin(extra_dependency))
    common = {"status": "passed", "actor": "fixture-person", "workflow_runtime_id": "fixture-workflow",
              "page": page_pin}
    gi5 = log_record(folder / "outline/FW01-what-to-send-log.md", "signed-fixture", {
        **common, "key": "GI5", "authority": "haipipe-insight-wisdom", "signature": "JL 260902",
        "dependencies": dependencies})
    gi6 = log_record(board / "0-MT-meta/MT04-question-wisdom/outline/MT04-question-wisdom-log.md",
                     "settled-fixture", {**common, "key": "GI6", "authority": "haipipe-insight-question",
                     "target": {"question": "QW1", "partition": "F"}, "signature_receipt": gi5})
    index = folder / "workflow/handoff.yaml"
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(yaml.safe_dump({"schema": "haipipe.insight-handoff/v1", "page": page_pin,
                                    "dependencies": dependencies, "gi5": gi5, "gi6": [gi6]},
                                   sort_keys=False), encoding="utf-8")
    return source, index


class InsightBoardWorkbenchTest(unittest.TestCase):
    def test_register_cells_and_partitions(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            self.assertTrue(is_insight_board(board))
            snap = board_snapshot(board, Path(td))
            self.assertEqual(snap["question_ids"], ["QD1", "QW1"])
            qd1 = snap["questions"][0]
            self.assertEqual(qd1["question"], "what does the extract hold?")
            self.assertEqual(qd1["cells"]["F"]["page"], "FD01")
            self.assertEqual(qd1["cells"]["B"]["raw"], "🚫 F-only")
            qw1 = snap["questions"][1]
            self.assertEqual(qw1["question"], "what to send?")
            self.assertEqual(qw1["cells"]["F"]["page"], "FW01")
            self.assertEqual(qw1["cells"]["B"]["mark"], "🚫")
            self.assertEqual([(p["id"], p["rows"]) for p in snap["partitions"]],
                             [("F", "1,000"), ("B", "400")])
            self.assertIn("demo_dikw_input.parquet", snap["context"])

    def test_receipt_ladder_gates_and_handoff(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = board_snapshot(board, Path(td))
            self.assertEqual([(r["task"], r["status"], r["git"]) for r in snap["runs"]],
                             [("T01_profile/01_shape", "ok", "abc1234")])
            view = _cell_view(snap, "QW1", "F")
            self.assertEqual([p["id"] for p in view["primary"]], ["FW01", "FD01"])
            self.assertEqual(view["receipt"]["status"], "ok")
            gates = {g["key"]: g["state"] for g in view["gates"]}
            self.assertEqual(gates["GI5"], "held")  # historical signature alone is not current authority
            self.assertEqual(gates["GI6"], "passed")
            handoffs = handoff_records(board, snap["pages"])
            self.assertEqual([(h["signed"], h["signature"]) for h in handoffs], [(True, "JL 260902")])
            self.assertFalse(handoffs[0]["bindable"])
            refused = _cell_view(snap, "QW1", "B")
            self.assertIsNone(refused["page"])
            self.assertEqual(refused["cell"]["note"], "F-only")

    def test_render_every_space_and_short_link(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            apps = root / "examples-x" / "Project-Demo" / "applications"
            apps.mkdir(parents=True)
            board = board_fixture(apps)
            (apps / "_WorkSpace").mkdir(exist_ok=True)
            snap = board_snapshot(board, root)
            html = render_insight_board(snap, "insight", "QW1", "F")
            for space in ("scope", "run", "insight", "evidence", "check"):
                self.assertIn(f'data-space="{space}"', html)
            self.assertIn("DO send", html)                 # the answer's rows are shown
            self.assertIn("signed", html.lower())
            self.assertIn("Workflow map", html)
            self.assertIn("Run Spec templates", html)
            self.assertIn("Wisdom", html)
            self.assertNotIn("I5 Wisdom", html)
            self.assertIn("Folder on this board", html)
            self.assertIn("Folder tree × Folder kind", html)
            self.assertIn("0-MT-meta/MT00-meta/", html)
            self.assertNotIn('data-view="folders"', html)
            self.assertNotIn("Identity chain", html)
            self.assertEqual(insight_boards(root), [board])
            self.assertEqual(_board_by_name(root, "Demo-InsightBoard"), board)
            self.assertIsNone(_board_by_name(root, "%2Fexa"))
            groom = groom_snapshot(board, snap)
            self.assertFalse(groom["bindable_handoffs"])

    def test_runtime_inventory_counts_shared_native_run_once_and_refreshes(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            self.assertEqual(board_snapshot(board, root)["workflow_runtimes"], [])
            path = board / "_runs/insight/demo-execution/runtime.yaml"
            path.parent.mkdir(parents=True)
            run = {
                "run_id": "board/page/rp-para-01_P01", "run_spec_id": "write.BI01.P01",
                "owner": "haipipe-page-workflow", "status": "running",
                "participation": "managed", "target": "one paragraph",
                "consumers": [{"question": "QI3", "partition": "B"},
                              {"question": "QI4", "partition": "B"}],
                "ticket": "page/runs/rp-para-01_P01.yaml",
                "result": "page/results/rp-para-01_P01/",
                "receipt": "page/results/rp-para-01_P01/runtime.yaml",
            }
            data = {"schema": "haipipe.workflow-runtime/v1",
                    "workflow_id": "haipipe-insight-workflow",
                    "workflow_runtime_id": "demo-execution", "status": "running",
                    "definition_ref": "definition-v001.yaml", "runs": [run], "frontier": []}
            path.write_text(yaml.safe_dump(data))
            before = path.read_bytes()
            snap = board_snapshot(board, root)
            record = snap["workflow_runtimes"][0]
            self.assertEqual(record["error"], "")
            self.assertEqual(len(record["runs"]), 1)
            rendered = render_insight_board(snap, "run", "QD1", "F")
            self.assertIn("1 recorded Runs", rendered)
            self.assertIn(run["run_id"], rendered)
            self.assertEqual(path.read_bytes(), before, "presenter must not edit receipts")
            data.update(status="complete", runs=[], resource_controls=[{
                "key": "GI1", "target": {"question": "QI5", "partition": "B"},
                "status": "passed", "receipt": "register/outline/register-log.md#added-QI5",
            }])
            path.write_text(yaml.safe_dump(data))
            snap = board_snapshot(board, root)
            record = snap["workflow_runtimes"][0]
            self.assertEqual(record["status"], "complete")
            self.assertEqual(record["runs"], [])
            rendered = render_insight_board(snap, "run", "QD1", "F")
            self.assertIn("0 recorded Runs", rendered)
            self.assertIn("register/outline/register-log.md#added-QI5", rendered)
            path.unlink()
            self.assertEqual(board_snapshot(board, root)["workflow_runtimes"], [])

    def test_invalid_runtime_never_presents_duplicate_or_unallocated_rows_as_runs(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            path = board / "_runs/insight/demo-execution/runtime.yaml"
            path.parent.mkdir(parents=True)
            run = {"run_id": "task/r01", "run_spec_id": "support.target",
                   "owner": "haipipe-task", "status": "complete",
                   "ticket": "runs/r01.sh", "result": "results/r01/",
                   "receipt": "results/r01/runtime.yaml"}
            base = {"schema": "haipipe.workflow-runtime/v1",
                    "workflow_id": "haipipe-insight-workflow",
                    "workflow_runtime_id": "demo-execution", "frontier": []}
            for rows in ([run, run], [{"run_spec_id": "support.target"}], "invalid"):
                with self.subTest(rows=rows):
                    path.write_text(yaml.safe_dump(dict(base, runs=rows)))
                    snap = board_snapshot(board, root)
                    self.assertTrue(snap["workflow_runtimes"][0]["error"])
                    self.assertEqual(snap["workflow_runtimes"][0]["runs"], [])
            path.write_text("runs: [\n")
            self.assertTrue(board_snapshot(board, root)["workflow_runtimes"][0]["error"])

    def test_current_folder_kind_register_is_read_without_legacy_page_type(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            path = board / "0-MT-meta/MT01-question-data/MT01-question-data.md"
            path.write_text(path.read_text().replace("page-type: question", "folder-kind: question"))
            snap = board_snapshot(board, root)
            self.assertEqual(snap["by_id"]["MT01"]["page_type"], "question")
            self.assertIn("QD1", snap["question_ids"])

    def test_register_question_appends_a_grid_row_and_a_log_line(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            qid, pids = register_question(board, "D", "how many rows per week?", "F,B",
                                          "curiosity-driven", "FD01 · D1")
            self.assertEqual((qid, pids), ("QD2", ["F", "B"]))
            snap = board_snapshot(board, Path(td))
            qd2 = next(q for q in snap["questions"] if q["id"] == "QD2")
            self.assertEqual(qd2["question"], "how many rows per week?")
            self.assertEqual(qd2["cells"]["F"]["raw"], "⬜ open")
            self.assertEqual(qd2["cells"]["B"]["raw"], "⬜ open")
            text = (board / "0-MT-meta/MT01-question-data/outline/MT01-question-data-log.md").read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^\d{6} · Registered `QD2` on F, B from the Insight Board · origin: curiosity-driven · born from: FD01 · D1")
            self.assertIn("give Claude Code", render_insight_board(snap, "insight", "QD2", "B"))
            with self.assertRaises(ValueError):
                register_question(board, "W", "what to send next?", "B")   # MT04 is transposed
            with self.assertRaises(ValueError):
                register_question(board, "D", "no such column", "X")

    @unittest.skipUnless(REAL_BOARD.is_dir(), "real A00 board not present")
    def test_append_row_to_a_copy_of_the_real_mt02(self):
        with TemporaryDirectory() as td:
            src = REAL_BOARD / "0-MT-meta/MT02-question-information/MT02-question-information.md"
            copy = Path(td) / "MT02-question-information.md"
            copy.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            qid, text = _prepare_question_row(copy, "I", "does send hour change the salience lead in the young-female cut?", "C")
            copy.write_text(text, encoding="utf-8")
            self.assertEqual(qid, "QI19")
            page = {"text": copy.read_text(encoding="utf-8"), "id": "MT02", "rung": "information",
                    "page_type": "question", "path": copy}
            rows = _parse_register(page, ["F", "B", "C", "D", "E", "G", "X"])
            self.assertEqual(len(rows), 19)
            new = rows[-1]
            self.assertEqual(new["id"], "QI19")
            self.assertEqual(new["question"], "does send hour change the salience lead in the young-female cut?")
            self.assertEqual({k: v["raw"] for k, v in new["cells"].items()},
                             {"F": "·", "B": "·", "C": "⬜ open", "D": "·", "E": "·", "G": "·", "X": "·"})
            self.assertEqual(rows[-2]["id"], "QI18")                       # QI18 row untouched
            self.assertEqual(rows[-2]["cells"]["C"]["raw"], "🟡 CI16 final")

    def test_empty_register_creates_first_question_and_zero_run_control_receipt(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            path = board / "0-MT-meta/MT01-question-data/MT01-question-data.md"
            path.write_text(path.read_text().replace(
                "QD1  what does the extract   Data/1  ✅ FD01  🚫 F-only\n     hold?\n", ""))
            qid, _ = register_question(board, "D", "What observations are available?", "F")
            self.assertEqual("QD1", qid)
            runtime_path, = (board / "_runs/insight").glob("*/runtime.yaml")
            runtime = yaml.safe_load(runtime_path.read_text())
            self.assertEqual([], runtime["runs"])
            self.assertEqual([], runtime["requested_answer_targets"])
            self.assertEqual("complete", runtime["status"])
            self.assertEqual("passed", runtime["output"]["acceptance"])
            control, = runtime["resource_controls"]
            self.assertEqual("registration", control["key"])
            log_path, anchor = control["receipt"].split("#")
            log = (board / log_path).read_text()
            self.assertIn(f"### {anchor}", log)
            self.assertIn(runtime["workflow_runtime_id"], log)
            self.assertIn("actor: board-ask", log)
            self.assertEqual("⬜ open", board_snapshot(board, Path(td))["questions"][0]["cells"]["F"]["raw"])

    def test_registration_indexes_existing_runtime_without_closing_it(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            runtime_path = board / "_runs/insight/session-one/runtime.yaml"
            runtime_path.parent.mkdir(parents=True)
            request = {"action": "register-question", "level": "D", "question": "What is missing?", "partitions": ["F"]}
            runtime = {"workflow_id": "haipipe-insight-workflow", "workflow_runtime_id": "session-one",
                       "status": "held", "requested_controls": [request], "resource_controls": [],
                       "requested_answer_targets": [{"question": "QD1", "partition": "F"}], "runs": []}
            runtime_path.write_text(yaml.safe_dump(runtime))
            register_question(board, "D", "What is missing?", "F", workflow_runtime_id="session-one", actor="fixture-agent")
            saved = yaml.safe_load(runtime_path.read_text())
            self.assertEqual("held", saved["status"])
            self.assertEqual(runtime["requested_answer_targets"], saved["requested_answer_targets"])
            self.assertEqual("fixture-agent", saved["resource_controls"][0]["actor"])
            with self.assertRaisesRegex(ValueError, "exact registration"):
                register_question(board, "D", "A different ask?", "F", workflow_runtime_id="session-one")

    def test_concurrent_registration_is_held(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            (board / ".insight-registration.lock").mkdir()
            with self.assertRaisesRegex(ValueError, "locked"):
                register_question(board, "D", "What is missing?", "F")
            self.assertFalse((board / "_runs").exists())

    def test_handoff_receipt_append_is_stable_but_duplicate_anchor_is_invalid(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            source, index = current_handoff_fixture(board)
            record = yaml.safe_load(index.read_text())
            log = source.parent / record["gi5"]["path"].split("#")[0]
            with log.open("a") as stream:
                stream.write("\n### unrelated-record\n\nAn unrelated owner action.\n")
            self.assertTrue(handoff_records(board)[0]["bindable"])
            with log.open("a") as stream:
                stream.write("\n### signed-fixture\n\nDuplicate anchor.\n")
            self.assertFalse(handoff_records(board)[0]["bindable"])

    def test_reopened_queue_blocks_old_gi6_even_when_signed_page_is_unchanged(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            current_handoff_fixture(board)
            self.assertTrue(board_snapshot(board, Path(td))["handoffs"][0]["bindable"])
            register = board / "0-MT-meta/MT04-question-wisdom/MT04-question-wisdom.md"
            register.write_text(register.read_text().replace("✅ FW01", "⬜ open"))
            result = board_snapshot(board, Path(td))["handoffs"][0]
            self.assertFalse(result["bindable"])
            self.assertIn("register cell", result["eligibility_reason"])

    def test_identity_errors_block_ask_without_changing_page_or_log(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            path = board / "0-MT-meta/MT01-question-data/MT01-question-data.md"
            path.write_text(path.read_text().replace("page-type: question", "folder-kind: question"))
            identity = path.parent / "workflow/folder.yaml"
            identity.parent.mkdir()
            before = path.read_bytes()
            for text in ("current: [\n", "current:\n  folder-kind: wisdom\n"):
                identity.write_text(text)
                with self.assertRaises(ValueError):
                    register_question(board, "D", "Must not be written", "F")
                self.assertEqual(before, path.read_bytes())
                self.assertFalse((path.parent / "outline/MT01-question-data-log.md").exists())
                snap = board_snapshot(board, Path(td))
                self.assertTrue(snap["by_id"]["MT01"]["identity_error"])
                checks = groom_snapshot(board, snap)["checks"]
                self.assertTrue(any(c["code"] == "folder-identity-invalid" for c in checks))
                self.assertFalse(any(c["code"] == "insight-check-clean" for c in checks))

    def test_identity_only_changes_and_removal_refresh_board(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            path = board / "0-MT-meta/MT01-question-data/workflow/folder.yaml"
            path.parent.mkdir()
            path.write_text("current:\n    folder-kind: question\n")
            self.assertIn("QD1", board_snapshot(board, Path(td))["question_ids"])
            path.write_text("current: [\n")
            self.assertNotIn("QD1", board_snapshot(board, Path(td))["question_ids"])
            path.unlink()
            self.assertIn("QD1", board_snapshot(board, Path(td))["question_ids"])

    def test_current_handoff_requires_exact_receipts_and_dependency_bytes(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            external = root / "accepted-evidence.yaml"
            external.write_text("version: 1\n")
            _, index = current_handoff_fixture(board, external)
            snap = board_snapshot(board, root)
            self.assertTrue(snap["handoffs"][0]["bindable"])
            self.assertIn("1 Wisdom page ready for design", render_insight_board(snap, "delivery", "QW1", "F"))
            # A change outside the board also invalidates the cached eligibility.
            external.write_text("version: 2\n")
            snap = board_snapshot(board, root)
            self.assertFalse(snap["handoffs"][0]["bindable"])
            self.assertTrue(snap["handoffs"][0]["signed"])
            self.assertIn("changed", snap["handoffs"][0]["eligibility_reason"])
            current_handoff_fixture(board, external)
            data = yaml.safe_load(index.read_text())
            data["gi6"] = []
            index.write_text(yaml.safe_dump(data))
            self.assertFalse(board_snapshot(board, root)["handoffs"][0]["bindable"])

    def test_held_page_with_historical_signature_is_not_design_bound(self):
        from live.design import _insight_bindings
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            source, _ = current_handoff_fixture(board)
            with patch("live.design._declared_insight_boards", return_value=[board]):
                self.assertEqual("bound", _insight_bindings(board / "board.md", root)["status"])
                source.write_text(source.read_text().replace("state: ✅ SETTLED", "state: 🛑 held"))
                self.assertEqual("blocked", _insight_bindings(board / "board.md", root)["status"])
            handoff = handoff_records(board)[0]
            self.assertTrue(handoff["signed"])
            self.assertEqual("stale", handoff["eligibility"])

    def test_modern_task_config_uses_job_store_and_native_override_addresses(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            job = root / "tasks/b01_block/j01_job"
            task = job / "t01_task"
            config = task / "scripts/config/r01_counts.yaml"
            config.parent.mkdir(parents=True)
            config.write_text("store: stale-config-value\n")
            (job / "src").mkdir()
            (job / "src/config-defaults.yaml").write_text("store: _WorkSpace/Store/Demo-InsightBoard\n")
            ticket = task / "runs/r01_counts.sh"
            ticket.parent.mkdir()
            ticket.write_text("# fixture only\n")
            receipt = root / "_WorkSpace/Store/Demo-InsightBoard/b01_block/j01_job/t01_task/results/r01_counts/runtime.yaml"
            receipt.parent.mkdir(parents=True)
            receipt.write_text("status: complete\n")
            snap = board_snapshot(board, root)
            calls = _task_calls(snap)
            self.assertEqual(1, len(calls))
            self.assertEqual(receipt, calls[0]["receipt"])
            self.assertTrue(calls[0]["ran"])
            override = root / "other-store/exact/runtime.yaml"
            override.parent.mkdir(parents=True)
            override.write_text("status: complete\n")
            snap["workflow_runtimes"] = [{"runs": [{"ticket": str(ticket), "receipt": str(override)}]}]
            calls = _task_calls(snap)
            self.assertEqual(1, len(calls))
            self.assertEqual(override, calls[0]["receipt"])
            self.assertEqual("native-receipt", calls[0]["source"])

    def test_page_level_insight_surface(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = board_snapshot(board, Path(td))
            fw01 = snap["by_id"]["FW01"]
            self.assertEqual(page_cells(snap, fw01), [("QW1", "F")])
            html = render_page_insight(snap, fw01, "/Demo-InsightBoard/board.md")
            self.assertIn("QW1 × F", html)                 # the cell this page answers
            self.assertIn("DO send", html)                 # its own rows
            self.assertRegex(html, r">full-D01[ <]")       # what it cites: FD01 spelled full-D01 (JL 260918)
            self.assertIn('href="/Demo-InsightBoard/1-F-full/FW01-what-to-send/', html)  # links keep the code
            self.assertIn("<code>Demo-InsightBoard/1-F-full/FW01-what-to-send/", html)  # so do paths
            fd01 = snap["by_id"]["FD01"]
            html = render_page_insight(snap, fd01, "/Demo-InsightBoard/board.md")
            self.assertRegex(html, r">full-W01[ <]")       # cited by
            self.assertIn("open this page", render_insight_board(snap, "insight", "QW1", "F"))

    def test_ordinary_board_is_not_promoted(self):
        with TemporaryDirectory() as td:
            ordinary = Path(td) / "Demo-Board"
            ordinary.mkdir()
            (ordinary / "board.md").write_text("# Ordinary Board\n", encoding="utf-8")
            self.assertFalse(is_insight_board(ordinary))

    @unittest.skipUnless(REAL_BOARD.is_dir(), "real A00 board not present")
    def test_real_a00_board(self):
        snap = board_snapshot(REAL_BOARD, REAL)
        self.assertEqual(len(snap["question_ids"]), 40)
        q = {row["id"]: row for row in snap["questions"]}
        self.assertEqual(q["QI3"]["cells"]["B"]["raw"], "🟡 BI03 final")
        self.assertEqual(q["QI8"]["cells"]["B"]["raw"], "🚫 thin")
        self.assertEqual(q["QD4"]["cells"]["X"]["page"], "XD01")
        self.assertEqual(q["QI9"]["cells"]["E"]["raw"], "✅ EI08")
        self.assertEqual(q["QK1"]["cells"]["G"]["raw"], "🟡 GK01 final")
        self.assertEqual(q["QI14"]["cells"]["X"]["page"], "XI01")
        self.assertEqual(q["QW1"]["question"], "which messages should round 2 exploit?")
        self.assertEqual(q["QW1"]["cells"]["B"]["raw"], "✅ BW01 defers")
        self.assertEqual(q["QW2"]["cells"]["B"]["raw"], "🚫 F-only")
        self.assertTrue(all(r["found"] for r in snap["runs"]), [r["rel"] for r in snap["runs"]])
        view = _cell_view(snap, "QW1", "F")
        self.assertEqual(view["primary"][0]["id"], "FW01")
        self.assertEqual(view["primary"][-1]["level"], "data")
        self.assertEqual(view["ladder"][0]["rows"][0][0], "W1")


if __name__ == "__main__":
    unittest.main()
