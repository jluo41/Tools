"""Tests for the Board-level Insight workbench: one dataset, four Spaces, one
High/Low table per partition (logic left, the runs that answer it right).

The fixture mirrors the real A00 board's shapes: an ASCII register grid with
one column per partition, a D page that names a run receipt, and a W page
with a signed handoff.  When the real A00 board is present it is read too,
because the parsers exist for that board's exact formatting.
"""

from __future__ import annotations

import unittest
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
    page_tickets,
    render_insight_board,
    render_insight_page,
    render_insight_run,
    work_runs,
)

# The SPACE root is the nearest folder holding env.sh (AGENTS.md rule 7: no
# absolute paths).  Tools may be a symlink, so the working directory is tried first.
REAL = next((p for p in (Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents)
             if (p / "env.sh").is_file()), Path("/nonexistent"))
REAL_BOARD = REAL / "examples-5-design/Project-Application-SMSDesign/insights/SMSR2v1-InsightBoard"


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
         "full          where: []  declared unfiltered      full.yaml   1-full/\n"
         "                     1,000 of 1,000 rows · 100.0000%\n"
         "young         age lt 40                          young.yaml  2-young/\n"
         "                       400 of 1,000 rows ·  40.0000%\n")
    page(board / "0-MT-meta" / "MT01-question-data", "MT01-question-data",
         "# Data questions\n\nstate: ✅ SETTLED · 1 question\npage-type: question\nquestion-rung: data\nowner: JL\n\n"
         "## Content\n\n```text\nid   question                 Gen-1   full   young\n"
         "QD1  what does the extract   Data/1  ✅ D01-full  🚫 full-only\n     hold?\n```\n")
    page(board / "0-MT-meta" / "MT04-question-wisdom", "MT04-question-wisdom",
         "# Wisdom questions\n\nstate: ✅ SETTLED\npage-type: question\nquestion-rung: wisdom\nowner: JL\n\n"
         "## Content\n\n```text\nid    question           Gen-1     partition   QW1\n"
         "QW1   what to send?      Wisdom/1  full    ✅ W01-full\n"
         "                                   young   🚫 full-only\n```\n")
    page(board / "1-full" / "D01-full-extract-shape", "D01-full-extract-shape",
         "# Extract shape\n\nstate: ✅ SETTLED · answers QD1\npage-type: data\nowner: JL\n\n## Opening\n\nWhat is in the extract?\n\n"
         "## Content\n\n```text\nrun receipt    results/full/runtime.yaml    status ok\n```\n\n```text\nD1   rows   1,000   counts.csv\n```\n"
         "\n### 📥 Input files\n- `../../_WorkSpace/Store/Demo-InsightBoard/T01_profile/01_shape/QA/1.md`\n\n## Log\n\n260901 · Created.\n")
    page(board / "1-full" / "W01-full-what-to-send", "W01-full-what-to-send",
         "# Send the one arm\n\nstate: ✅ SETTLED · answers QW1\npage-type: wisdom\nowner: JL\n\n## Opening\n\nSend `a`.\n\n"
         "## Content\n\n```text\nW1  ←  D01-full · D1   one row\n```\n\n```text\nW1   DO send `a`.        D01-full · D1\n```\n\n"
         "#### 4 · Forbidden Overreach\n\n```text\n❌ Do not say why.\n\nSERVES        QW1 · brief\n\nsigned: ✅ JL 260902\n```\n\n## Log\n\n260902 · Signed.\n")
    (board / "2-young").mkdir()          # registered partition, no page yet
    (board / "board.md").write_text(
        "# Demo Insight Board\n\nboard-kind: insight-board\nstore: _WorkSpace/Store/Demo-InsightBoard\n\n"
        "## Topic\n\nOne question, one extract.\n", encoding="utf-8")
    receipt = root / "_WorkSpace/Store/Demo-InsightBoard/T01_profile/01_shape/results/full/runtime.yaml"
    receipt.parent.mkdir(parents=True)
    receipt.write_text("status: ok\ncall: full\ntask: T01_profile/01_shape\nstarted: 2026-09-01T10:00:00Z\n"
                       "duration_s: 3\ngit_sha: abc1234\n", encoding="utf-8")
    return board


def current_handoff_fixture(board: Path, extra_dependency: Path | None = None):
    """Synthetic owner receipts; no real person approval or scientific claim.

    References are paths (and a version for the Page), never content hashes
    (JL 260928); staleness is file time.
    """
    source = board / "1-full/W01-full-what-to-send/W01-full-what-to-send.md"
    folder = source.parent

    def pin(path):
        return {"path": os.path.relpath(path, folder)}

    def log_record(path, anchor, data):
        body = "```yaml\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "```"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# Log\n\n### {anchor}\n\n{body}\n", encoding="utf-8")
        return {"path": os.path.relpath(path, folder) + "#" + anchor}

    page_pin = {**pin(source), "version": "v001"}
    dependencies = [pin(board / "0-MT-meta/MT00-meta/MT00-meta.md"),
                    pin(board / "1-full/D01-full-extract-shape/D01-full-extract-shape.md")]
    if extra_dependency:
        dependencies.append(pin(extra_dependency))
    common = {"status": "passed", "actor": "fixture-person", "workflow_runtime_id": "fixture-workflow",
              "page": page_pin}
    gi5 = log_record(folder / "outline/W01-full-what-to-send-log.md", "signed-fixture", {
        **common, "key": "GI5", "authority": "haipipe-insight-wisdom", "signature": "JL 260902",
        "dependencies": dependencies})
    gi6 = log_record(board / "0-MT-meta/MT04-question-wisdom/outline/MT04-question-wisdom-log.md",
                     "settled-fixture", {**common, "key": "GI6", "authority": "haipipe-insight-question",
                     "target": {"question": "QW1", "partition": "full"}, "signature_receipt": gi5})
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
            self.assertEqual(qd1["cells"]["full"]["page"], "D01-full")
            self.assertEqual(qd1["cells"]["young"]["raw"], "🚫 full-only")
            qw1 = snap["questions"][1]
            self.assertEqual(qw1["question"], "what to send?")
            self.assertEqual(qw1["cells"]["full"]["page"], "W01-full")
            self.assertEqual(qw1["cells"]["young"]["mark"], "🚫")
            self.assertEqual([(p["id"], p["rows"]) for p in snap["partitions"]],
                             [("full", "1,000"), ("young", "400")])
            self.assertIn("demo_dikw_input.parquet", snap["context"])

    def test_receipt_ladder_gates_and_handoff(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = board_snapshot(board, Path(td))
            self.assertEqual([(r["task"], r["status"], r["git"]) for r in snap["runs"]],
                             [("T01_profile/01_shape", "ok", "abc1234")])
            view = _cell_view(snap, "QW1", "full")
            self.assertEqual([p["id"] for p in view["primary"]], ["W01-full", "D01-full"])
            self.assertEqual(view["receipt"]["status"], "ok")
            gates = {g["key"]: g["state"] for g in view["gates"]}
            self.assertEqual(gates["GI5"], "held")  # historical signature alone is not current authority
            self.assertEqual(gates["GI6"], "passed")
            handoffs = handoff_records(board, snap["pages"])
            self.assertEqual([(h["signed"], h["signature"]) for h in handoffs], [(True, "JL 260902")])
            self.assertFalse(handoffs[0]["bindable"])
            refused = _cell_view(snap, "QW1", "young")
            self.assertIsNone(refused["page"])
            self.assertEqual(refused["cell"]["note"], "full-only")

    def test_render_every_space_and_short_link(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            apps = root / "examples-x" / "Project-Demo" / "applications"
            apps.mkdir(parents=True)
            board = board_fixture(apps)
            (apps / "_WorkSpace").mkdir(exist_ok=True)
            snap = board_snapshot(board, root)
            html = render_insight_board(snap, "insight", "QW1", "full")
            for space in ("scope", "insight", "check", "delivery"):
                self.assertIn(f'<section class=pane data-space="{space}">', html)
            for retired in ("run", "evidence"):            # 4 Spaces (studio drawing, JL 261001)
                self.assertNotIn(f'<section class=pane data-space="{retired}">', html)
            self.assertIn('<div class=dataset title="demo_dikw_input.parquet">', html)   # one dataset, every Space
            self.assertIn("Wisdom questions", html)        # logic: the questions, by level, no QW codes
            self.assertIn("Send the one arm", html)        # the answer opens as a pop-out
            self.assertIn('class="rp folded"', html)       # a Runs panel beside each Space, folded to a strip
            self.assertIn("signed", html.lower())
            self.assertEqual(insight_boards(root), [board])
            self.assertEqual(_board_by_name(root, "Demo-InsightBoard"), board)
            self.assertIsNone(_board_by_name(root, "%2Fexa"))
            groom = groom_snapshot(board, snap)
            self.assertFalse(groom["bindable_handoffs"])

    def test_insight_space_has_a_methods_subspace_with_cards_and_papers(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            apps = root / "examples-x" / "Project-Demo" / "applications"
            apps.mkdir(parents=True)
            board = board_fixture(apps)
            ref = root / "ref"
            (ref / "methods").mkdir(parents=True)
            (ref / "methods" / "01-by-look.md").write_text(
                "By look\n=======\n\nfamily: From the data: look first\nmove: Plot every field before asking.\n"
                "reads: data\nreturns: candidate patterns\ntest now: T0 spec\n\n"
                "What the literature says\n------------------------\n\nrationale: Look before you test [Tukey 1977].\n",
                encoding="utf-8")
            (ref / "discovery.md").write_text(
                "Discovery methods\n=================\n\n| family | method | card |\n|---|---|---|\n"
                "| From the data | By look | methods/01-by-look.md |\n", encoding="utf-8")
            (ref / "papers.md").write_text(
                "| group | role | key | paper | venue | doi | why here | pdf |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                "| by look | classic | ★ | Tukey 1977 · Exploratory Data Analysis | Addison-Wesley |  | look first |  |\n"
                "| by look | evidence |  | Doe, Roe & Poe 2020 · A test of looking | Management Science | 10.1/x | it was tested |  |\n",
                encoding="utf-8")
            with patch("live.insightboard.DISCOVERY_METHODS", ref / "discovery.md"), \
                    patch("live.insightboard.DESIGN_METHODS", ref / "missing.md"), \
                    patch("live.insightboard.METHOD_PAPERS", ref / "papers.md"):
                html = render_insight_board(board_snapshot(board, root), "insight", "QW1", "full")
            self.assertIn('data-view="methods">Methods</button>', html)        # a sub-space beside Questions
            for k in ("discovery", "design", "papers"):
                self.assertIn(f'data-mview="{k}"', html)
            self.assertIn('id="method-by-look"', html)                          # a card per index row
            self.assertIn("tested in 1 study", html)                             # its evidence row counts
            self.assertIn('class="cite to-paper"', html)                         # [Tukey 1977] opens its paper
            self.assertIn("No design methods file yet", html)                    # a missing file says so
            self.assertIn("2 papers · 1 key", html)
            self.assertIn("rp-utd", html)                                        # Management Science is UTD24
            self.assertIn("Add a paper", html)                                   # the Runs panel offers it

    def test_runtime_inventory_counts_shared_native_run_once_and_refreshes(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            self.assertEqual(board_snapshot(board, root)["workflow_runtimes"], [])
            path = board / "_runs/insight/demo-execution/runtime.yaml"
            path.parent.mkdir(parents=True)
            run = {
                "run_id": "board/page/rp-para-01_P01", "run_spec_id": "write.I01-young.P01",
                "owner": "haipipe-page-workflow", "status": "running",
                "participation": "managed", "target": "one paragraph",
                "consumers": [{"question": "QI3", "partition": "young"},
                              {"question": "QI4", "partition": "young"}],
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
            rendered = render_insight_board(snap, "run", "QD1", "full")
            self.assertIn("1 recorded Runs", rendered)
            self.assertIn(run["run_id"], rendered)
            self.assertEqual(path.read_bytes(), before, "presenter must not edit receipts")
            data.update(status="complete", runs=[], resource_controls=[{
                "key": "GI1", "target": {"question": "QI5", "partition": "young"},
                "status": "passed", "receipt": "register/outline/register-log.md#added-QI5",
            }])
            path.write_text(yaml.safe_dump(data))
            snap = board_snapshot(board, root)
            record = snap["workflow_runtimes"][0]
            self.assertEqual(record["status"], "complete")
            self.assertEqual(record["runs"], [])
            rendered = render_insight_board(snap, "run", "QD1", "full")
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
            qid, pids = register_question(board, "D", "how many rows per week?", "full,young",
                                          "curiosity-driven", "D01-full · D1")
            self.assertEqual((qid, pids), ("QD2", ["full", "young"]))
            snap = board_snapshot(board, Path(td))
            qd2 = next(q for q in snap["questions"] if q["id"] == "QD2")
            self.assertEqual(qd2["question"], "how many rows per week?")
            self.assertEqual(qd2["cells"]["full"]["raw"], "⬜ open")
            self.assertEqual(qd2["cells"]["young"]["raw"], "⬜ open")
            text = (board / "0-MT-meta/MT01-question-data/draft/records/MT01-question-data-log.md").read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^\d{6} · Registered `QD2` on full, young from the Insight Board · origin: curiosity-driven · born from: D01-full · D1")
            html = render_insight_board(snap, "insight", "QD2", "young")
            self.assertIn("No run names it under", html)    # Work: nothing answers it yet
            self.assertIn("No report yet", html)            # Report: nothing says it yet
            with self.assertRaises(ValueError):
                register_question(board, "W", "what to send next?", "young")   # MT04 is transposed
            with self.assertRaises(ValueError):
                register_question(board, "D", "no such column", "cross")

    @unittest.skipUnless(REAL_BOARD.is_dir(), "real A00 board not present")
    def test_append_row_to_a_copy_of_the_real_mt02(self):
        with TemporaryDirectory() as td:
            src = REAL_BOARD / "0-MT-meta/MT02-question-information/MT02-question-information.md"
            copy = Path(td) / "MT02-question-information.md"
            copy.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            qid, text = _prepare_question_row(copy, "I", "does send hour change the salience lead in the young-female cut?", "youngfemale")
            copy.write_text(text, encoding="utf-8")
            self.assertEqual(qid, "QI19")
            page = {"text": copy.read_text(encoding="utf-8"), "id": "MT02", "rung": "information",
                    "page_type": "question", "path": copy}
            rows = _parse_register(page, ["full", "youngmale", "youngfemale", "older", "midlifemale", "midlifefemale", "cross"])
            self.assertEqual(len(rows), 19)
            new = rows[-1]
            self.assertEqual(new["id"], "QI19")
            self.assertEqual(new["question"], "does send hour change the salience lead in the young-female cut?")
            self.assertEqual({k: v["raw"] for k, v in new["cells"].items()},
                             {"full": "·", "youngmale": "·", "youngfemale": "⬜ open", "older": "·", "midlifemale": "·", "midlifefemale": "·", "cross": "·"})
            self.assertEqual(rows[-2]["id"], "QI18")                       # QI18 row untouched
            self.assertEqual(rows[-2]["cells"]["youngfemale"]["raw"], "🟡 I16-youngfemale final")

    def test_empty_register_creates_first_question_and_zero_run_control_receipt(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            path = board / "0-MT-meta/MT01-question-data/MT01-question-data.md"
            path.write_text(path.read_text().replace(
                "QD1  what does the extract   Data/1  ✅ D01-full  🚫 full-only\n     hold?\n", ""))
            qid, _ = register_question(board, "D", "What observations are available?", "full")
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
            self.assertEqual("⬜ open", board_snapshot(board, Path(td))["questions"][0]["cells"]["full"]["raw"])

    def test_registration_indexes_existing_runtime_without_closing_it(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            runtime_path = board / "_runs/insight/session-one/runtime.yaml"
            runtime_path.parent.mkdir(parents=True)
            request = {"action": "register-question", "level": "D", "question": "What is missing?", "partitions": ["full"]}
            runtime = {"workflow_id": "haipipe-insight-workflow", "workflow_runtime_id": "session-one",
                       "status": "held", "requested_controls": [request], "resource_controls": [],
                       "requested_answer_targets": [{"question": "QD1", "partition": "full"}], "runs": []}
            runtime_path.write_text(yaml.safe_dump(runtime))
            register_question(board, "D", "What is missing?", "full", workflow_runtime_id="session-one", actor="fixture-agent")
            saved = yaml.safe_load(runtime_path.read_text())
            self.assertEqual("held", saved["status"])
            self.assertEqual(runtime["requested_answer_targets"], saved["requested_answer_targets"])
            self.assertEqual("fixture-agent", saved["resource_controls"][0]["actor"])
            with self.assertRaisesRegex(ValueError, "exact registration"):
                register_question(board, "D", "A different ask?", "full", workflow_runtime_id="session-one")

    def test_concurrent_registration_is_held(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            (board / ".insight-registration.lock").mkdir()
            with self.assertRaisesRegex(ValueError, "locked"):
                register_question(board, "D", "What is missing?", "full")
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
            register.write_text(register.read_text().replace("✅ W01-full", "⬜ open"))
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
                    register_question(board, "D", "Must not be written", "full")
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

    def test_current_handoff_requires_exact_receipts_and_unchanged_dependencies(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            external = root / "accepted-evidence.yaml"
            external.write_text("version: 1\n")
            _, index = current_handoff_fixture(board, external)
            snap = board_snapshot(board, root)
            self.assertTrue(snap["handoffs"][0]["bindable"])
            self.assertIn("1 signed Wisdom answer ready for design", render_insight_board(snap, "delivery", "QW1", "full"))
            # A change outside the board also invalidates the cached eligibility:
            # the dependency is now newer than the signed receipt (file time).
            later = external.stat().st_mtime + 5
            external.write_text("version: 2\n")
            os.utime(external, (later, later))
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

    def test_new_layout_board_in_insights_with_its_own_results(self):
        """One dataset, one board in insights/ (JL 261001): the config names the extract
        and the questions, never a store; the board's `_results/` holds the result."""
        with TemporaryDirectory() as td:
            root = Path(td)
            project = root / "examples-x" / "Project-Demo"
            board = board_fixture(project / "insights")
            text = (board / "board.md").read_text(encoding="utf-8")
            (board / "board.md").write_text(text.replace("store: _WorkSpace/Store/Demo-InsightBoard", "store: _results"),
                                            encoding="utf-8")
            task = project / "tasks/b51_demo_dikw/j11_data_extract/t01_extract_shape"
            (task / "scripts/config").mkdir(parents=True)
            (task / "scripts/config/r01_demo_full.yaml").write_text(
                "input:\n  parquet_path: _WorkSpace/Prep/demo_dikw_input.parquet\nanswers: [QD1]\n")
            (task / "scripts/config/r02_other_full.yaml").write_text(
                "input:\n  parquet_path: _WorkSpace/Prep/other_extract.parquet\nanswers: [QD1]\n")
            (task / "runs").mkdir()
            (task / "runs/r01_demo_full.sh").write_text("# fixture only\n")
            result = board / "_results/b51_demo_dikw/j11_data_extract/t01_extract_shape/results/r01_demo_full"
            result.mkdir(parents=True)
            (result / "runtime.yaml").write_text("status: ok\n")
            self.assertEqual(insight_boards(root), [board])            # found under insights/
            snap = board_snapshot(board, root)
            runs = work_runs(snap)
            self.assertEqual([(r["call"], r["answers"], r["status"]) for r in runs],
                             [("r01_demo_full", ["QD1"], "ok")])      # the other extract's config is not this board's
            self.assertFalse(any(p["rel"].startswith("_results") for p in snap["pages"]))
            html = render_insight_board(snap, "insight", "QD1", "full")
            for level in ("<div class=bj-b><span class=idtag>b51</span> demo_dikw</div>",          # Block
                          "<div class=bj-j><span class=idtag>j11</span> data_extract</div>",       # Job
                          "<span class=idtag>t01</span> extract_shape"):                          # Task
                self.assertIn(level, html)

    def test_page_folder_tickets_name_the_runs_it_rests_on(self):
        """A page folder is also a task folder (JL 261001): its runs/ tickets
        run_bNNjNNtNNrNN_<partition>_<task>.sh call task runs, and the Work column
        shows those runs even when no config's `answers:` names the question.  The
        result is the page's own results/<ticket>/."""
        with TemporaryDirectory() as td:
            root = Path(td)
            project = root / "examples-x" / "Project-Demo"
            board = board_fixture(project / "insights")
            text = (board / "board.md").read_text(encoding="utf-8")
            (board / "board.md").write_text(text.replace("store: _WorkSpace/Store/Demo-InsightBoard\n", ""),
                                            encoding="utf-8")                    # no board store: results are per page
            task = project / "tasks/b51_demo_dikw/j11_data_extract/t01_extract_shape"
            (task / "scripts/config").mkdir(parents=True)
            (task / "scripts/config/r01_demo_full.yaml").write_text("answers: []\n")   # no answers: join
            (task / "runs").mkdir()
            (task / "runs/r01_demo_full.sh").write_text("# fixture only\n")
            tickets = board / "1-full/D01-full-extract-shape/runs"
            tickets.mkdir()
            (tickets / "run_b51j11t01r01_full_extract_shape.sh").write_text(
                '#!/bin/bash\nPAGE="$(cd "$(dirname "$0")/.." && pwd)"\n'
                'export RESULT_DIR="${PAGE}/results/$(basename "$0" .sh)"\n'
                'exec "${PAGE}/../../../../tasks/b51_demo_dikw/j11_data_extract/t01_extract_shape/runs/r01_demo_full.sh"\n')
            result = board / "1-full/D01-full-extract-shape/results/run_b51j11t01r01_full_extract_shape"
            result.mkdir(parents=True)
            (result / "runtime.yaml").write_text("status: ok\n")
            snap = board_snapshot(board, root)
            self.assertEqual([(r["call"], r["task_run"], r["status"]) for r in page_tickets(snap, snap["by_id"]["D01-full"])],
                             [("run_b51j11t01r01_full_extract_shape", "r01_demo_full", "ok")])
            self.assertFalse(any("results/" in p["rel"] for p in snap["pages"]))   # a result is never a page
            html = render_insight_board(snap, "insight", "QD1", "full")
            self.assertIn("<span class=idtag>t01</span> extract_shape", html)
            self.assertIn("<span class=idtag>run_<wbr>b51j11t01r01_<wbr>full_<wbr>extract_<wbr>shape</span>", html)

    def test_page_opens_as_a_document(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = board_snapshot(board, Path(td))
            fw01 = snap["by_id"]["W01-full"]
            self.assertEqual(page_cells(snap, fw01), [("QW1", "full")])
            html = render_insight_page(snap, fw01)
            self.assertIn("Wisdom question 1 on Full", html)   # what it answers, in words
            self.assertIn("DO send", html)                     # its own text
            self.assertIn("W01-full", html)                    # W01-full spelled as its cut (JL 260918)
            self.assertIn('href="/Demo-InsightBoard/1-full/W01-full-what-to-send/', html)  # the source stays linked
            board_html = render_insight_board(snap, "insight", "QW1", "full")
            self.assertIn("/_board/insight?board=Demo-InsightBoard&amp;page=W01-full", board_html)

    def test_runs_answer_questions_through_their_config(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            board = board_fixture(root)
            task = root / "tasks/T01_profile/01_shape"
            (task / "configs").mkdir(parents=True)
            (task / "configs/full.yaml").write_text(
                "store: _WorkSpace/Store/Demo-InsightBoard\nanswers: [QD1]   # the extract's shape\n")
            (task / "configs/other.yaml").write_text("store: _WorkSpace/Store/Other-Board\nanswers: [QD1]\n")
            (task / "runs").mkdir()
            (task / "runs/_run.sh").write_text("# fixture only\n")
            (task / "runs/full.sh").symlink_to("_run.sh")
            (root / "_WorkSpace/Store/Demo-InsightBoard/T01_profile/01_shape/results/full/counts.csv").write_text(
                "level,n\nall,1000\n")
            mt01 = board / "0-MT-meta/MT01-question-data/MT01-question-data.md"
            mt01.write_text(mt01.read_text(encoding="utf-8") + "\n#### 2 · QD1 · Extract Shape\n\n"
                            "**The ask**: what does the extract hold, row by row?\n\n"
                            "**Why now**: every rate later divides by its rows.\n\n"
                            "**What would answer it**: the row grain and the column list.\n", encoding="utf-8")
            snap = board_snapshot(board, root)
            runs = work_runs(snap)
            self.assertEqual([(r["call"], r["partition"], r["answers"], r["status"]) for r in runs],
                             [("full", "full", ["QD1"], "ok")])      # other.yaml's store is another board
            html = render_insight_board(snap, "insight", "QD1", "full")
            self.assertIn("/_board/insight-run?board=Demo-InsightBoard&amp;task=T01_profile/01_shape&amp;call=full", html)
            self.assertIn("Answered on Full", html)            # QD1 on young: 🚫 full-only, said in words
            self.assertIn("<b class=q-name>Extract Shape</b>", html)          # the register division's name
            self.assertIn("<dt>The ask</dt><dd>What does the extract hold, row by row?</dd>", html)  # the long ask is folded
            self.assertIn("<dt>Why it matters</dt><dd>Every rate later divides by its rows.</dd>", html)
            self.assertIn("MT01 · question-data ↗", html)                     # the register it came from
            self.assertIn("Young", html)                       # partitions by name, not by letter
            self.assertIn("page D01-full", html)               # the answering page is the report (JL 261001)
            report = board / "reports/full/QD1.md"
            report.parent.mkdir(parents=True)
            report.write_text("# The extract holds one row per invitation\n\nquestion: QD1\npartition: F\n"
                              "runs: T01_profile/01_shape · full\nstrength: STRONG\n\n"
                              "1,000 rows. Each is one sent invitation. A third sentence stays out.\n")
            html = render_insight_board(board_snapshot(board, root), "insight", "QD1", "full")
            self.assertIn("The extract holds one row per invitation", html)   # Report column reads the file
            self.assertIn("1,000 rows. Each is one sent invitation.", html)
            self.assertNotIn("A third sentence", html)
            self.assertIn("report=full%3AQD1", html)                             # it opens as a document
            out = render_insight_run(snap, "T01_profile/01_shape", "full")
            self.assertIn("status: ok", out)                   # the receipt
            self.assertIn("counts.csv", out)                   # the run's own table
            self.assertIn("answers QD1", out)

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
        self.assertEqual(q["QI3"]["cells"]["youngmale"]["raw"], "🟡 I03-youngmale final")
        self.assertEqual(q["QI8"]["cells"]["youngmale"]["raw"], "🚫 thin")
        self.assertEqual(q["QD4"]["cells"]["cross"]["page"], "D01-cross")
        self.assertEqual(q["QI9"]["cells"]["midlifemale"]["raw"], "✅ I08-midlifemale")
        self.assertEqual(q["QK1"]["cells"]["midlifefemale"]["raw"], "🟡 K01-midlifefemale final")
        self.assertEqual(q["QI14"]["cells"]["cross"]["page"], "I01-cross")
        self.assertEqual(q["QW1"]["question"], "which messages should round 2 exploit?")
        self.assertEqual(q["QW1"]["cells"]["youngmale"]["raw"], "✅ W01-youngmale defers")
        self.assertEqual(q["QW2"]["cells"]["youngmale"]["raw"], "🚫 full-only")
        self.assertTrue(all(r["found"] for r in snap["runs"]), [r["rel"] for r in snap["runs"]])
        view = _cell_view(snap, "QW1", "full")
        self.assertEqual(view["primary"][0]["id"], "W01-full")
        self.assertEqual(view["primary"][-1]["level"], "data")
        self.assertEqual(view["ladder"][0]["rows"][0][0], "W1")


if __name__ == "__main__":
    unittest.main()
