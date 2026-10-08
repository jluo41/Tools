"""The Discovery Block workbench over a small Block: Task Pages and Paper Runs through the Task
reader, each Result card and receipt, every View, the file reader, the Project view, and real HTTP."""
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pytest

from live.discoveryboard import block_snapshot, projects_snapshot, render_file
from live.discovery_views import render_block, spaces
from serve import Handler


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def panel(page: str, key: str) -> str:
    """One View's own section: every page carries all its Views, so a check looks inside one."""
    return page.split(f'data-panel="{key}">', 1)[1].split("</section>", 1)[0]


def run(task: Path, name: str, title: str, status: str, verification: str, support: str, bib: bool):
    write(task / "runs" / f"{name}.sh", "#!/usr/bin/env bash\necho read\n")
    result = task / "results" / name
    write(result / f"{name}.md", f"# {title}\n\n- run: {name}\n- cite: @{name}\n- subject: https://example.org/{name}\n"
                                 f"- venue: Test venue\n- verification: {verification}\n\n## Question\n\nWhat?\n\n"
                                 "## Readout\n\nThe paper says one clear thing.\n\nMore.\n")
    write(result / "facts.md", "- fact\n")
    write(result / "runtime.yaml", f"run: {name}\nfamily: discovery\nstatus: {status}\nsubject:\n  kind: paper\n"
                                   f"  title: \"{title}\"\nanalysis:\n  reading_depth: full-text\n  claim_support: {support}\n"
                                   + ("failure: \"citation not confirmed\"\n" if status == "blocked" else ""))
    if bib:
        write(result / f"{name}.bib", f"@article{{{name},\n  title = {{{title}}}\n}}\n")


@pytest.fixture
def demo(tmp_path):
    block = tmp_path / "examples-t/Proj-Test/discoveries/b03_cgm_forecasting"
    write(block / "board.md", "# CGM forecasting\nboard-kind: discovery-block\nstate: 🟡 DESIGN\nowner: JL\n"
          "spine: Papers on CGM glucose forecasting.\nclose: Each Task has a synthesis.\n\n## Topic\n\nText.\n\n"
          "## Questions\n\n```yaml\nquestions:\n- id: Q01\n  title: Best forecaster\n  question: Which model forecasts best?\n"
          "  work:\n  - j01_models/t01_transformers\n```\n")
    task = block / "j01_models/t01_transformers"
    write(task / "t01_transformers.md", "---\nfolder-kind: discovery\nstate: 🟡\n---\n# Transformer forecasters\n\n## Opening\n\nWhy.\n")
    write(task / "discovery.yaml", "version: 6\nkind: discovery\ndiscovery_type: topic-summary\njob:\n  id: j01\n  title: \"Model families\"\n")
    write(task / "summary.md", "# Summary\n")
    run(task, "r01_lee2022_glucose_transformer", "Glucose Transformer", "complete", "VERIFIED", "supported", True)
    run(task, "r02_kim2023_cgm_survey", "CGM Survey", "blocked", "NEEDS-VERIFICATION", "pending", False)
    write(block / "studio/map.excalidraw", json.dumps({"type": "excalidraw", "elements": []}))
    return tmp_path, block


def test_papers_come_from_result_cards_and_receipts(demo):
    root, block = demo
    snap = block_snapshot(block, root)
    assert snap["totals"] == {"jobs": 1, "tasks": 1, "papers": 2, "complete": 1, "blocked": 1, "needs_person": 1, "bib": 1}
    assert snap["jobs"][0]["title"] == "Model families"
    task = snap["tasks"][0]
    assert task["discovery_type"] == "topic-summary" and [s["name"] for s in task["synthesis"]] == ["summary.md"]
    assert not any("READING" in i for i in task["issues"])            # a Task-Page-only finding is left out
    first, second = snap["papers"]
    assert (first["title"], first["status"], first["verification"], first["needs_person"]) == (
        "Glucose Transformer", "complete", "VERIFIED", False)
    assert first["readout"] == "The paper says one clear thing." and first["bib"].startswith("@article")
    assert (second["status"], second["needs_person"]) == ("blocked", True)
    assert snap["questions"][0]["work"][0]["task"]["name"] == "t01_transformers"
    assert snap["source_issues"] == []


def test_every_view_renders_and_says_what_matters(demo):
    root, block = demo
    snap = block_snapshot(block, root)
    for _, _, views in spaces():
        for key, _ in views:
            assert "<html" in render_block(snap, key)
    assert "Glucose Transformer" in render_block(snap, "papers")
    citations = panel(render_block(snap, "citations"), "citations")
    assert "CGM Survey" in citations and "Glucose Transformer" not in citations
    assert "citation not confirmed" in render_block(snap, "runs")
    assert "@article{r01_lee2022_glucose_transformer" in render_block(snap, "bib")
    assert "summary.md" in render_block(snap, "tasks")


def test_file_reader_and_project_view(demo):
    root, block = demo
    code, body = render_file(block, root, "j01_models/t01_transformers/results/r01_lee2022_glucose_transformer/runtime.yaml", "b/board.md")
    assert code == 200 and "full-text" in body
    assert render_file(block, root, "../../../../etc/hosts", "b/board.md")[0] == 404
    assert render_file(block, root, "studio/map.excalidraw", "b/board.md")[0] == 404
    [group] = projects_snapshot(root, block.parent)
    assert group["blocks"][0]["papers"] == 2 and group["blocks"][0]["tasks"] == 1


@pytest.fixture
def server(demo):
    root, block = demo
    class TestHandler(Handler):
        def log_message(self, *_args):
            pass
    TestHandler.root = root
    TestHandler.only = frozenset({"discovery"})
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
    url = origin + "/_board/discovery-board?" + urlencode({"path": path})
    with urlopen(url) as response:
        assert response.status == 200 and b"Glucose Transformer" in response.read()
    with urlopen(origin + "/w/b03_cgm_forecasting") as response:     # an --only host: its own page
        assert response.status == 200 and b"Papers" in response.read()
    with pytest.raises(HTTPError) as err:
        urlopen(origin + "/_board/discovery-board?" + urlencode({"path": "nowhere/board.md"}))
    assert err.value.code == 404
    body = json.dumps({"path": path, "action": "add-resource", "title": "Review guide", "url": "https://example.org/r",
                       "questions": ["Q01"], "contribution": "how to review", "notes": ""}).encode()
    with urlopen(Request(origin + "/_board/discovery-board", data=body, method="POST",
                         headers={"Content-Type": "application/json"})) as response:
        assert json.loads(response.read())["ok"] is True
    assert "Review guide" in (block / "board.md").read_text(encoding="utf-8")
