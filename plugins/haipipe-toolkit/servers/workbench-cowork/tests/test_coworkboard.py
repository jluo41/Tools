"""The CoWork Block workbench over a small Block built from the haipipe-cowork templates:
Jobs from their page headers, every View, the file reader, the Project view, the
resource form over real HTTP, and the Project audit's Block rule."""
import importlib.util
import json
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pytest

from live.coworkboard import block_snapshot, projects_snapshot, render_file
from live.cowork_views import render_block, spaces
from serve import Handler
from host_paths import skill_dir

AUDIT = skill_dir("haipipe-project") / "scripts/audit_projects.py"


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def job_page(title, state, waiting, since, nxt, extra=""):
    return (f"# {title}\njob-kind: cowork-job\nstate: {state}\nwaiting-on: {waiting}\nsince: {since}\n"
            f"next: {nxt}\n{extra}\nWhat we asked for.\n")


@pytest.fixture
def demo(tmp_path):
    block = tmp_path / "examples-t/Proj-Test/cowork/b11_cloud"
    write(block / "board.md", "# Cloud · where the data lands\nboard-kind: cowork-block\nstate: 🟡 ACTIVE\nowner: JL\n"
          "spine: One cloud request.\nclose: The group exists.\nstatus: 2026-10-04 testing\n\nThe text.\n\n"
          "## Questions\n\n```yaml\nquestions:\n- id: Q01\n  title: Cloud ready\n  question: Is the group ready?\n"
          "  work:\n  - j01_cloud_group/j01_cloud_group.md\n```\n")
    write(block / "j00_people/j00_people.md", job_page("People · who to ask", "📇 REFERENCE", "nobody", "2026-10-04",
                                                        "add people") + "\n  Nick   Research IT\n")
    write(block / "j01_cloud_group/j01_cloud_group.md",
          job_page("Cloud group · IT-1042", "🟡 ACTIVE", "Nick", "2026-10-01", "wait for Nick",
                   "ticket: IT-1042\nurl: https://example.org/IT-1042\n"))
    write(block / "j01_cloud_group/CHECKLIST.md", "- [x] 1. Ask for the group.\n- [ ] 2. Send the diagram\n"
                                                  "  before Monday.\n  - Why: they asked.\n")
    write(block / "j01_cloud_group/Timeline.md", "Timeline\n========\n\n  2026-10-01  asked\n")
    write(block / "j01_cloud_group/emails/2026-10-03-draft-to-nick.md", "status: draft\nHi Nick\n")
    write(block / "j01_cloud_group/meetings/2026-10-02-review.md", "# Review\nnotes\n")
    write(block / "j01_cloud_group/design/plan.md", "# Plan\n")
    write(block / "j02_closed/j02_closed.md", job_page("Old request", "✅ DONE", "nobody", "2026-09-01", "none"))
    write(block / "studio/flow.excalidraw", json.dumps({"type": "excalidraw", "elements": []}))
    return tmp_path, block


def test_jobs_come_from_their_page_headers(demo):
    root, block = demo
    snap = block_snapshot(block, root)
    jobs = {j["name"]: j for j in snap["jobs"]}
    assert list(jobs) == ["j00_people", "j01_cloud_group", "j02_closed"]
    assert [j["open"] for j in snap["jobs"]] == [False, True, False]      # 📇 REFERENCE and ✅ DONE are not open work
    group = jobs["j01_cloud_group"]
    assert (group["waiting"], group["since"], group["ticket"]) == ("Nick", "2026-10-01", "IT-1042")
    assert group["url"] == "https://example.org/IT-1042" and group["days"] is not None
    assert [(s["number"], s["done"], s["text"]) for s in group["steps"]] == [
        ("1", True, "Ask for the group."), ("2", False, "Send the diagram before Monday.")]   # wrapped line joined
    assert [e["name"] for e in snap["emails"] if e["draft"]] == ["2026-10-03-draft-to-nick.md"]
    assert snap["emails"][0]["job"] == "j01_cloud_group" and len(snap["meetings"]) == 1
    assert "Nick" in snap["people"] and "j00_people" in snap["people_url"]
    assert snap["questions"][0]["work"][0]["path"] == "j01_cloud_group/j01_cloud_group.md"
    assert snap["source_issues"] == []


def test_every_view_renders_and_says_what_matters(demo):
    root, block = demo
    snap = block_snapshot(block, root)
    for _, _, views in spaces():
        for key, _ in views:
            assert "<html" in render_block(snap, key)
    jobs = render_block(snap, "jobs")
    assert "j01_cloud_group" in jobs and "wait for Nick" in jobs and "IT-1042" in jobs
    assert "Old request" in render_block(snap, "done")
    assert "Send the diagram before Monday." in render_block(snap, "drafts")
    assert "Nick" in render_block(snap, "waiting")
    assert render_block(snap, "tickets") == render_block(snap, "jobs")      # the old view name still lands


def test_file_reader_shows_block_text_and_refuses_escapes(demo):
    root, block = demo
    code, body = render_file(block, root, "j01_cloud_group/CHECKLIST.md", "b/board.md")
    assert code == 200 and "Ask for the group." in body
    for bad in ("../../../../etc/hosts", "j01_cloud_group/design/../../../board.md/../../x", "studio/flow.excalidraw"):
        assert render_file(block, root, bad, "b/board.md")[0] == 404


def test_project_view_counts_open_jobs(demo):
    root, block = demo
    [group] = projects_snapshot(root, block.parent)
    [entry] = group["blocks"]
    assert entry["block"] == "b11_cloud" and entry["open"] == 1 and entry["jobs"][0]["waiting"] == "Nick"


@pytest.fixture
def server(demo):
    root, block = demo
    class TestHandler(Handler):
        def log_message(self, *_args):
            pass
    TestHandler.root = root
    TestHandler.only = frozenset({"cowork"})
    TestHandler.terminal_enabled = False
    TestHandler.auth_users = None
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), TestHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(httpd.server_port), block, root
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join()


def test_http_views_short_address_and_resource_form(server):
    origin, block, root = server
    path = (block.relative_to(root) / "board.md").as_posix()
    url = origin + "/_board/cowork-board?" + urlencode({"path": path})
    with urlopen(url) as response:
        assert response.status == 200 and b"j01_cloud_group" in response.read()
    with urlopen(origin + "/w/b11_cloud") as response:                       # /w/ adds file=board.md: still the Block
        assert response.status == 200 and b"Work" in response.read()
    with urlopen(url + "&" + urlencode({"show": "j01_cloud_group/Timeline.md"})) as response:
        assert b"asked" in response.read()
    with pytest.raises(HTTPError) as err:
        urlopen(origin + "/_board/cowork-board?" + urlencode({"path": "nowhere/board.md"}))
    assert err.value.code == 404
    body = json.dumps({"path": path, "action": "add-resource", "title": "IT guide", "url": "https://example.org/guide",
                       "questions": ["Q01"], "contribution": "how to ask", "notes": ""}).encode()
    with urlopen(Request(origin + "/_board/cowork-board", data=body, method="POST",
                         headers={"Content-Type": "application/json"})) as response:
        assert json.loads(response.read())["ok"] is True
    assert "IT guide" in (block / "board.md").read_text(encoding="utf-8")


def test_the_project_audit_accepts_the_block_and_flags_old_layouts(demo):
    root, block = demo
    spec = importlib.util.spec_from_file_location("audit_projects", AUDIT)
    audit = importlib.util.module_from_spec(spec)
    sys.modules["audit_projects"] = audit       # its dataclasses look their module up
    spec.loader.exec_module(audit)
    assert audit.cowork_topic_findings(block.parent) == []
    write(block / "PEOPLE.md", "x")
    write(block / "design/old.md", "x")
    write(block / "j03_no_page/emails/a.md", "x")
    found = " | ".join(audit.cowork_topic_findings(block.parent))
    assert "PEOPLE.md" in found and "design/ is not a Block folder" in found and "no job page" in found


def test_a_reports_drawing_lives_in_its_report_folder(demo):
    """The rule (JL 261004): a drawing that belongs to one report is saved in reports/<id>_topic/studio/;
    the helper makes it there and the workbench shows it with the report."""
    from argparse import Namespace
    root, block = demo
    helper = skill_dir("haipipe-question") / "ref/block_questions.py"
    spec = importlib.util.spec_from_file_location("block_questions_rule", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.update(Namespace(command="add-report", block=block, id="Q01", slug="cloud_ready", title=None,
                            evidence=[], drawing=["data_flow"]))
    drawing = block / "reports/q01_cloud_ready/studio/data_flow.excalidraw"
    assert json.loads(drawing.read_text(encoding="utf-8"))["type"] == "excalidraw"
    write(block / "reports/q01_cloud_ready/studio/extra_sketch.excalidraw", json.dumps({"type": "excalidraw", "elements": []}))
    report = block_snapshot(block, root)["questions"][0]["report"]
    titles = [d["title"] for d in report["drawings"]]
    assert titles == ["Data flow"]                                       # one Question, one drawing (JL 261005)
    assert "reports/q01_cloud_ready/studio/" in report["drawings"][0]["url"].replace("%2F", "/")
    assert any("one drawing" in i and "Extra sketch" in i for i in report["issues"])   # the second is a finding


def test_one_question_shows_one_drawing_and_a_picture_goes_inside_it(demo):
    """JL 261005: "for each question we should just have one excalidraw"; "some png can be put into the
    excalidraw as well". The Report column shows the report's first drawing only; a second drawing and a
    linked picture are findings in Check, not more thumbs."""
    root, block = demo
    write(block / "j01_cloud_group/materials/card.png", "png")
    write(block / "studio/flow.png", "png")
    write(block / "studio/second.excalidraw", json.dumps({"type": "excalidraw", "elements": []}))
    write(block / "reports/q01_cloud_ready/q01_cloud_ready.md",
          "# Cloud ready\nanswers: Q01\nanswer-status: open\n\n## Content\n\n### Evidence\n\n"
          "- [Flow](../../studio/flow.excalidraw)\n- [Second](../../studio/second.excalidraw)\n"
          "- [The desk card](../../j01_cloud_group/materials/card.png)\n")
    board = (block / "board.md").read_text(encoding="utf-8")
    write(block / "board.md", board.replace("  work:\n", "  report: reports/q01_cloud_ready/q01_cloud_ready.md\n  work:\n"))
    report = block_snapshot(block, root)["questions"][0]["report"]
    assert [t["title"] for t in report["thumbs"]] == ["Flow"] and report["thumbs"][0]["png"].endswith("flow.png")
    found = " | ".join(report["issues"])
    assert "one drawing" in found and "Second" in found
    assert "inside the report's drawing" in found and "The desk card" in found
    row = render_block(block_snapshot(block, root), "questions")
    assert row.count('class="rp-thumb"') == 1 and "The desk card" not in row.split('class="hl-p"', 1)[1].split("</div>", 1)[0]


def test_a_studio_item_folder_drawing_is_listed(demo):
    """JL 261008: studio/ may hold numbered items, rNN_<topic>/ (a reference) and sNN_<topic>/ (a drawing
    about it). A drawing one folder down is listed; scripts in _build/ and replaced work in _old/ are not."""
    root, block = demo
    write(block / "studio/s01_pilot/s01_pilot.excalidraw",
          json.dumps({"type": "excalidraw", "source": "studio/_build/build_s01.py", "elements": []}))
    write(block / "studio/_build/scratch.excalidraw", json.dumps({"type": "excalidraw", "elements": []}))
    write(block / "studio/_old/old.excalidraw", json.dumps({"type": "excalidraw", "elements": []}))
    found = {d["path"].rsplit("/studio/", 1)[1]: d for d in block_snapshot(block, root)["drawings"]}
    assert set(found) == {"flow.excalidraw", "s01_pilot/s01_pilot.excalidraw"}
    assert found["s01_pilot/s01_pilot.excalidraw"]["source"] == "studio/_build/build_s01.py"   # view only
