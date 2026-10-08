"""Progress invariants and real HTTP integration of the Task Block workbench."""
import json
import base64
from pathlib import Path
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pytest
import yaml

from demo import add_task, build_demo, write
from host_registry import route_allowed
from live.home import render_home, resolve_workbench
from live.taskboard import task_board_snapshot, render_task_board, resolve_task_board
from serve import Handler


@pytest.fixture
def demo(tmp_path):
    return tmp_path, build_demo(tmp_path)


def test_snapshot_counts_task_runs_and_keeps_readings_separate(demo):
    root, board = demo
    snap = task_board_snapshot(board, root)
    assert snap["totals"] == {"jobs": 3, "tasks": 6, "complete": 4, "runs": 8, "attention": 5}
    tasks = {t["id"]: t for t in snap["tasks"]}
    assert len(tasks) == 6  # t01 under different Jobs cannot overwrite each other.
    assert tasks["b11j01t01"]["reading"]["signed"] == 1
    assert tasks["b11j01t02"]["execution"] == "complete"
    assert tasks["b11j01t02"]["reading"]["signed"] == 0
    assert "Runs complete; workflow report not recorded" in tasks["b11j01t02"]["issues"]
    assert tasks["b11j02t01"]["execution"] == "running"
    assert tasks["b11j02t02"]["execution"] == "attention"
    assert tasks["b11j03t02"]["runs"][0]["status"] == "missing"


def test_attempt_archives_and_superseded_runs_do_not_inflate_progress(demo):
    root, board = demo
    task = board / "j01_data_checks/t01_source_audit"
    write(task / "results/r01_example/attempts/000001/runtime.yaml", "run: r01_example\nstatus: failed\n")
    write(task / "runs/r02_previous.sh", "# previous\n")
    write(task / "results/r02_previous/runtime.yaml", "run: r02_previous\nstatus: superseded\n")
    row = task_board_snapshot(board, root)["tasks"][0]
    assert row["total"] == row["complete"] == 1
    assert len(row["runs"]) == 2
    assert {r["status"] for r in row["runs"]} == {"complete", "superseded"}


def test_external_declared_store_is_read_without_external_static_links(demo, tmp_path):
    root, board = demo
    task = board / "j01_data_checks/t01_source_audit"
    store = root.parent / (root.name + "-store")
    store.mkdir()
    external = store / board.name / task.parent.name / task.name / "results"
    external.parent.mkdir(parents=True)
    (task / "results").rename(external)
    write(task.parent / "src/config-defaults.yaml", yaml.safe_dump({"store": str(store)}))
    row = task_board_snapshot(board, root)["tasks"][0]
    assert row["complete"] == 1
    assert row["runs"][0]["receipt_url"] == ""
    assert str(store) not in json.dumps(row)


def test_missing_page_and_malformed_workflow_remain_visible(demo):
    root, board = demo
    task = board / "j01_data_checks/t01_source_audit"
    (task / (task.name + ".md")).unlink()
    write(task / "workflow/plan.yaml", "[not: valid")
    snap = task_board_snapshot(board, root)
    row = snap["tasks"][0]
    assert len(snap["tasks"]) == 6
    assert "Task Page missing or unreadable" in row["issues"]
    assert "Workflow plan contains invalid YAML" in row["issues"]
    assert row["page_url"] == ""


def test_orphan_results_and_unresolved_reading_are_attention(demo):
    root, board = demo
    task = board / "j01_data_checks/t01_source_audit"
    (task / "runs/r01_example.sh").unlink()
    row = task_board_snapshot(board, root)["tasks"][0]
    assert row["total"] == row["complete"] == 0
    assert row["runs"][0]["allocated"] is False
    assert any("Verdict Run" in msg for msg in row["issues"])


def test_open_page_run_is_not_a_missing_task_receipt(demo):
    root, board = demo
    task = board / "j01_data_checks/t01_source_audit"
    write(task / "runs/draft-manual-run/run-structure-1002-overview.md",
          "---\nfamily: page\noperation: interactive-writing\nstatus: open\n---\n# Overview\n")
    row = task_board_snapshot(board, root)["tasks"][0]
    assert row["total"] == 1
    page_run = next(r for r in row["runs"] if r["lane"] == "page")
    assert page_run["status"] == "running"
    assert page_run["recorded_status"] == "open (Ticket)"


def test_malformed_complete_receipt_is_not_counted_complete(demo):
    root, board = demo
    task = board / "j01_data_checks/t01_source_audit"
    write(task / "results/r01_example/runtime.yaml", "status: complete\nbroken: [\n")
    row = task_board_snapshot(board, root)["tasks"][0]
    assert row["complete"] == 0
    assert any("invalid YAML" in issue for issue in row["issues"])


def test_reading_before_current_result_is_flagged(demo):
    root, board = demo
    page = board / "j01_data_checks/t01_source_audit/t01_source_audit.md"
    page.write_text(page.read_text().replace("12:05:00Z", "12:00:00Z"))
    row = task_board_snapshot(board, root)["tasks"][0]
    assert row["reading"]["signed"] == 1  # Keep the declared signature visible.
    assert any("signature predates" in issue for issue in row["issues"])


def test_scope_and_links_are_confined_and_markup_escaped(demo):
    root, board = demo
    assert resolve_task_board(root, str(board.relative_to(root) / "board.md")) == board
    assert resolve_task_board(board, "/board.md") == board
    assert resolve_task_board(root, "/../../etc/passwd") is None
    outside = root.parent / (root.name + "-outside")
    write(outside / "board.md", "# Outside\nboard-kind: task-block\n")
    (root / "escape").symlink_to(outside, target_is_directory=True)
    assert resolve_task_board(root, "escape/board.md") is None
    snap = task_board_snapshot(board, root)
    snap["title"] = '<script>alert("injected")</script>'
    rendered = render_task_board(snap)
    assert '<script>alert("injected")' not in rendered
    assert "&lt;script&gt;" in rendered
    assert all(t["page_url"].startswith("/_board/") for t in snap["tasks"])


def test_named_question_ids_and_a_question_without_a_title(demo):
    """Q-<word>-<number> ids (JL 261004) read like Q01; a question with no title prints once."""
    from task_questions import replace_register
    root, board = demo
    head = board / "board.md"
    rows = [dict(id="Q-food-1", group="🍎 Food", question="What forms does the input come in?",
                 aim="Know every form the API must handle.", work=["j01_data_checks/t01_source_audit"],
                 report="reports/q-food-1_input_forms/q-food-1_input_forms.md"),
            dict(id="Q-Food-2", question="Upper case is not an id"),
            dict(id="Q1", question="One digit is not an id")]
    write(head, replace_register(head.read_text(), "Questions", "questions", rows))
    snap = task_board_snapshot(board, root)
    assert [q["id"] for q in snap["questions"]] == ["Q-food-1"]
    q = snap["questions"][0]
    assert q["group"] == "🍎 Food" and q["title"] == q["question"]
    assert q["report"]["issues"] == ["Report Page is missing, unreadable or outside its Block"]
    assert {"Invalid or duplicate Question: Q-Food-2", "Invalid or duplicate Question: Q1"} <= set(snap["source_issues"])
    rendered = render_task_board(snap)
    assert rendered.count("What forms does the input come in?</b>") == 1
    assert '<div class="q-text">What forms does the input come in?</div>' not in rendered
    assert ">Q-food-1</span>" in rendered
    assert q["aim"] == "Know every form the API must handle."
    assert '<div class="q-aim"><b>Aim</b> Know every form the API must handle.</div>' in rendered


def test_add_report_frames_a_registered_question_with_its_drawing(demo):
    """block_questions.py add-report: a report for a Question already in the register, with a
    studio drawing under Evidence that the Report column then shows."""
    import subprocess
    import sys
    from urllib.parse import quote
    from task_questions import replace_register
    root, board = demo
    head = board / "board.md"
    rows = [dict(id="Q-food-1", group="🍎 Food", question="What forms does the input come in?",
                 work=["j01_data_checks/t01_source_audit"])]
    write(head, replace_register(head.read_text(), "Questions", "questions", rows))
    drawing = sorted((board / "studio").glob("*.excalidraw"))[0]
    from host_paths import skill_dir
    helper = skill_dir("haipipe-question") / "ref/block_questions.py"
    run = lambda *extra: subprocess.run([sys.executable, str(helper), "add-report", str(board), "--id", "Q-food-1",
                                         "--slug", "input_forms", *extra], capture_output=True, text=True)
    done = run("--evidence", f"Food drawing|studio/{drawing.name}")
    assert done.returncode == 0, done.stderr
    page = board / "reports/q-food-1_input_forms/q-food-1_input_forms.md"
    assert page.is_file() and (page.parent / "page.toml").is_file()
    assert f"- [Food drawing](../../studio/{quote(drawing.name)})" in page.read_text()
    assert run().returncode == 1                                    # the Question now names its report
    q = task_board_snapshot(board, root)["questions"][0]
    assert q["report"]["present"] and q["report"]["status"] == "open"
    # linked but not yet read: Check says so until a reader sets results-read
    assert q["report"]["issues"] == ["Evidence review time is not recorded (results-read)"]
    assert [d["title"] for d in q["report"]["drawings"]] == ["Food drawing"]
    assert q["report"]["drawings"][0]["png"] == ""                  # no picture yet: a text link
    drawing.with_suffix(".png").write_bytes(b"\x89PNG\r\n\x1a\n")
    q = task_board_snapshot(board, root)["questions"][0]
    assert q["report"]["drawings"][0]["png"].endswith(".png")      # the preview picture beside it
    assert '<a class="rp-thumb"' in render_task_board(task_board_snapshot(board, root))
    other = subprocess.run([sys.executable, str(helper), "add-report", str(board), "--id", "Q-food-9",
                            "--slug", "x"], capture_output=True, text=True)
    assert other.returncode == 1 and "use add-question" in other.stderr


def test_home_and_short_url_work_before_a_static_build(demo):
    root, board = demo
    assert not (board / "board/index.html").exists()
    url, why = resolve_workbench(root, board.name)
    assert why == "ok"
    assert url.startswith("/_board/workbench?")                          # the base frame (261007)
    assert resolve_workbench(root, board.name, only={"work"})[0].startswith("/_board/work-board?")
    home = render_home(root)
    assert "Model comparison · demo" in home
    # the Space view's card opens the Block's short workbench address, which lands on the board
    from live.home import board_slug
    short = "/w/" + board_slug(board.name, board.parent.name)
    assert f'href="{short}"' in home
    assert resolve_workbench(root, short[3:])[0].startswith("/_board/workbench?")
    assert route_allowed("/_board/work-board", {"work"})
    assert route_allowed("/_board/task-board", {"task"})          # its name before 261007 still answers
    assert not route_allowed("/_board/task-board", {"paper"})
    # A task-only host omits Page links it cannot serve.
    assert all(not t["page_url"] for t in task_board_snapshot(board, root, {"task"})["tasks"])


def test_snapshot_reads_do_not_write_source_files(demo):
    root, board = demo
    before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in root.rglob("*") if p.is_file()}
    render_task_board(task_board_snapshot(board, root))
    after = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in root.rglob("*") if p.is_file()}
    assert before == after


@pytest.fixture
def server(demo):
    root, board = demo
    class TestHandler(Handler):
        def log_message(self, *_args):
            pass
    TestHandler.root = root
    TestHandler.only = frozenset({"work"})
    TestHandler.terminal_enabled = False
    TestHandler.auth_users = None
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), TestHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(httpd.server_port), board, root, TestHandler
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join()


def test_http_get_head_post_and_short_redirect(server):
    origin, board, root, _ = server
    path = (board.relative_to(root) / "board.md").as_posix()
    url = origin + "/_board/work-board?" + urlencode({"path": path})
    with urlopen(url) as response:
        body = response.read()
        assert response.status == 200
        assert response.headers["Cache-Control"] == "no-store"
    with urlopen(Request(url, method="HEAD")) as response:
        assert response.read() == b""
        assert int(response.headers["Content-Length"]) == len(body)
    with urlopen(url + "&format=json") as response:
        assert json.load(response)["totals"]["tasks"] == 6
    with urlopen(url.replace("/_board/work-board?", "/_board/task-board?")) as response:
        assert response.read() == body          # its name before 261007 opens the same page
    with urlopen(origin + "/w/" + board.name) as response:
        assert "/_board/work-board?" in response.url
    request = Request(origin + "/_board/work-board", data=json.dumps({"path": path}).encode(),
                      headers={"Content-Type": "application/json"})
    with urlopen(request) as response:
        assert json.load(response)["ok"]


def test_http_invalid_board_is_404_and_auth_still_applies(server):
    origin, _, _, handler = server
    with pytest.raises(HTTPError) as err:
        urlopen(origin + "/_board/work-board?path=/../../etc")
    assert err.value.code == 404
    handler.auth_users = {"example": "password"}
    handler.public_read = True
    with pytest.raises(HTTPError) as err:
        urlopen(origin + "/_board/work-board")
    assert err.value.code == 403  # Public-read mode refuses private surfaces without a login challenge.
    request = Request(origin + "/_board/work-board", headers={
        "Authorization": "Basic " + base64.b64encode(b"example:password").decode()})
    with urlopen(request) as response:
        assert response.status == 200
