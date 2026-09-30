from __future__ import annotations

import copy
import importlib.util
import re
import sys
import types
from pathlib import Path

import test_corpus_preparation as fixtures
import test_calibration as calibration_fixtures
import test_definition_discussion as discussion_fixtures
import yaml

PLUGIN = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "subjective_label_workbench_preparation_test",
    PLUGIN / "servers" / "workbench-labeling" / "labeling.py",
)
assert SPEC and SPEC.loader
workbench = importlib.util.module_from_spec(SPEC)
# The presenter imports the Board parser at module load. This focused test
# supplies its two adapter functions so it can run in the package's Python 3.9
# engine test environment; host tests exercise the real Board parser.
prior = {name: sys.modules.get(name) for name in ("src", "src.body", "src.parse")}
src = types.ModuleType("src")
src.__path__ = []
body = types.ModuleType("src.body")
body.group_token = lambda heading: heading.split(" · ", 1)[0]
parse = types.ModuleType("src.parse")
parse.parse_dir = lambda _: (None, [], None)
sys.modules.update({"src": src, "src.body": body, "src.parse": parse})
try:
    SPEC.loader.exec_module(workbench)
finally:
    for name, old in prior.items():
        if old is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = old


def test_attached_page_shows_each_source_run_before_package_link(tmp_path, monkeypatch) -> None:
    raw, _, owner, page = fixtures._fixture(tmp_path)
    fixtures.prep.attach(owner, "transcripts", page)
    board = page.parents[2]
    (board / "board.md").write_text("# Board\n", encoding="utf-8")
    monkeypatch.setattr(workbench, "_board_pages", lambda _: [{
        "id": "Label-1", "title": "Labeling job", "file": "pages/Label-1/Label-1.md", "group": "Data"
    }])
    jobs = workbench.board_jobs(board, "/board/board.md")
    assert jobs["jobs"][0]["badge"] == "Prepare corpus"
    assert workbench._view_model(page)["preparation"]["runs"] == []

    fixtures.prep.normalize(owner, raw, "transcripts")
    vm = workbench._view_model(page)
    assert len(vm["preparation"]["runs"]) == 1
    assert workbench._next_step(vm)[0].endswith("unit-recipe.")
    assert "1 of 5" in workbench._data_space(vm)["preparation"]
    assert "run-corpus-source-normalize-" in workbench._run_table(vm)
    assert all(len(t["runs"]) == (1 if t["op"] == "source-normalize" else 0)
               for t in workbench._run_types(vm)["data"] if t.get("family") == "corpus")


def test_preparation_new_run_only_follows_the_next_completed_step(tmp_path) -> None:
    raw, _, owner, page = fixtures._fixture(tmp_path)
    fixtures.prep.attach(owner, "transcripts", page)
    vm = workbench._view_model(page)
    types = workbench._run_types(vm)["data"]
    panel = workbench._runs_panel(vm, "data", types)
    assert re.search(r'data-op="source-normalize"[^>]*data-prompt="Start the next', panel)
    for op in ("unit-recipe", "unit-materialize", "unit-check", "initial-group-reserve"):
        assert re.search(rf'data-op="{op}"[^>]*data-prompt=""', panel)

    fixtures.prep.normalize(owner, raw, "transcripts")
    vm = workbench._view_model(page)
    panel = workbench._runs_panel(vm, "data", workbench._run_types(vm)["data"])
    assert re.search(r'data-op="source-normalize"[^>]*data-prompt=""', panel)
    assert re.search(r'data-op="unit-recipe"[^>]*data-prompt="Start the next', panel)


def test_open_discussion_uses_resume_and_hides_a_second_new_run(tmp_path) -> None:
    root, page = calibration_fixtures.confirmed_job(tmp_path)
    opened = discussion_fixtures.dd.start(root, human_id="JL")
    vm = workbench._view_model(page)
    panel = workbench._runs_panel(vm, "labeling", workbench._run_types(vm)["labeling"])
    assert re.search(r'data-op="definition-discussion"[^>]*data-prompt=""', panel)
    run = next(r for r in vm["runs"] if r["operation"] == "definition-discussion")
    assert run["run"] == opened["run"]
    assert workbench._run_again(vm, run)[0] == "Resume"
    assert workbench._next_step(vm)[0] == "Finish the open label-meaning discussion before releasing a round."


def test_legacy_discussion_after_round_release_has_no_resume(tmp_path, monkeypatch) -> None:
    root, page = calibration_fixtures.confirmed_job(tmp_path)
    discussion_fixtures.dd.start(root, human_id="JL")
    monkeypatch.setattr(discussion_fixtures.cal, "_unfinished_definition_discussion", lambda _: None)
    discussion_fixtures.cal.release_round(root, human_id="JL")
    vm = workbench._view_model(page)
    panel = workbench._runs_panel(vm, "labeling", workbench._run_types(vm)["labeling"])
    assert "This discussion cannot continue after round release" in panel
    assert "blocked history" in panel
    assert re.search(r'data-op="definition-discussion"[^>]*data-prompt=""', panel)
    assert "Resume</button>" not in panel


def test_historical_unbuilt_run_is_review_only(tmp_path) -> None:
    root = tmp_path / "Page" / "labeling"
    root.mkdir(parents=True)
    run = {"run": "rl99_guideline-learn_round-01", "name": "guideline-learn",
           "label": "round-01", "operation": "guideline-learn", "target": "round-01",
           "status": "running", "owner": str(root.parent), "outcome": "",
           "artifacts": [], "started_at": "", "finished_at": ""}
    vm = {"root": root, "config": {}, "preparation": {}, "runs": [run], "canonical": {}, "cal": {}}
    types = [t for t in workbench._run_types(vm)["labeling"] if t["op"] == "guideline-learn"]
    assert len(types) == 1 and types[0]["built"] is False
    panel = workbench._runs_panel(vm, "labeling", types)
    assert "rl99_guideline-learn_round-01" in panel
    assert "Resume</button>" not in panel and "Rerun</button>" not in panel
    card = re.search(r'<article class=run-card data-op="guideline-learn".*?</article>', panel)
    assert card and "<summary>Record</summary>" in card.group()
    assert "<summary>Prompt " not in card.group()


def test_prepared_page_is_discovered_before_contract_and_has_live_runs(tmp_path, monkeypatch) -> None:
    state = fixtures._prepare(tmp_path)
    page, owner = state["page"], state["owner"]
    fixtures.prep.link(owner, Path(state["package"]), page)
    board = page.parents[2]
    (board / "board.md").write_text("# Board\n", encoding="utf-8")
    page_entry = {"id": "Label-1", "title": "Labeling job", "file": "pages/Label-1/Label-1.md",
                  "group": "Data"}
    monkeypatch.setattr(workbench, "_board_pages", lambda _: [page_entry])

    jobs = workbench.board_jobs(board, "/board/board.md")
    assert len(jobs["jobs"]) == 1
    assert jobs["jobs"][0]["kind"] == "preparing"
    assert jobs["jobs"][0]["badge"] == "Create Contract"

    vm = workbench._view_model(page)
    assert vm["preparation"]["receipt"]["group_disjointness"] == "passed"
    types = workbench._run_types(vm)["data"]
    prep_types = [t for t in types if t.get("family") == "corpus"]
    assert len(prep_types) == 5
    assert all(len(t["runs"]) == 1 for t in prep_types)
    panel = workbench._runs_panel(vm, "data", types)
    assert "run-corpus-unit-materialize-" in panel
    assert "subjective-label-preparation" in panel
    assert "PRIVATE_REPLY" not in panel
    view = workbench._data_space(vm)["preparation"]
    assert state["partition_id"] in view
    assert "PRIVATE_REPLY" not in view

    generated = board / "board" / "Data" / "Label-1.html"
    generated.parent.mkdir(parents=True)
    generated.write_text('<section data-file="pages/Label-1/Label-1.md"></section>', encoding="utf-8")
    html = workbench.render(page, "/board/board.md", "pages/Label-1/Label-1.md",
                            "/board/board/Data/Label-1.html", board)
    assert 'data-view=preparation' in html
    assert "run-corpus-initial-group-reserve-" in html
    assert "PRIVATE_REPLY" not in html


def test_labeling_panel_uses_disk_names_and_keeps_legacy_readable(tmp_path) -> None:
    state = fixtures._prepare(tmp_path)
    page = state["page"]
    fixtures.prep.link(state["owner"], Path(state["package"]), page)
    fixtures.job.create_contract(source_job=Path(state["package"]),
                                 job_root=page.parent / "labeling", page_file=page,
                                 job_id="example", target="example", human_id="human",
                                 created_at="2026-09-29")
    runs = page.parent / "runs"
    legacy = "rl99_human-calibration_round-03"
    (runs / f"{legacy}.yaml").write_text(yaml.safe_dump({
        "run": legacy, "family": "labeling", "operation": "human-calibration", "target": "round-03"
    }), encoding="utf-8")
    (runs / "run-section-0929-unrelated.yaml").write_text(yaml.safe_dump({
        "run": "run-section-0929-unrelated", "operation": "section"
    }), encoding="utf-8")
    rows = workbench._run_rows(page.parent / "labeling")
    names = {row["run"]: row["name"] for row in rows}
    assert names["run-labeling-corpus-contract-0929-job-v1"] == "run-labeling-corpus-contract-0929-job-v1"
    assert names[legacy] == "run-labeling-human-calibration-round-03"
    assert "run-section-0929-unrelated" not in names
    card = workbench._run_card({"root": page.parent / "labeling", "config": {}},
                               next(row for row in rows if row["run"] == legacy))
    assert "Legacy Ticket on disk" in card
    assert legacy in card


def test_legacy_job_does_not_offer_retroactive_preparation_runs(tmp_path) -> None:
    (tmp_path / "config.yaml").write_text("schema_version: subjective-label/v2\n", encoding="utf-8")
    vm = {"root": tmp_path, "runs": [], "preparation": {"attached": False, "linked": False}}
    view = workbench._preparation_view(vm)
    assert "<h2>Corpus</h2>" in view
    assert "before Corpus Preparation Runs existed" in view
    assert not [t for t in workbench._run_types(vm)["data"] if t.get("family") == "corpus"]


def test_new_page_offers_a_copyable_preparation_setup_request(tmp_path) -> None:
    vm = {"root": tmp_path / "labeling", "preparation": {"attached": False, "linked": False}}
    view = workbench._preparation_view(vm)
    assert "Copy setup request" in view
    assert "data-copy=" in view
    assert "/subjective-label-preparation" in view


def test_flat_board_page_first_requires_its_own_page_folder(tmp_path, monkeypatch) -> None:
    board = tmp_path / "board"
    (board / "SL").mkdir(parents=True)
    (board / "board.md").write_text("# Board\n", encoding="utf-8")
    flat = board / "SL" / "S-Label-2.md"
    flat.write_text("# S-Label-2\n", encoding="utf-8")
    monkeypatch.setattr(workbench, "_board_pages", lambda _: [{
        "id": "S-Label-2", "title": "New Labeling Page", "file": "SL/S-Label-2.md", "group": "SL"
    }])
    vm = workbench._view_model(flat)
    assert not vm["page_ready"]
    assert vm["root"] == flat.parent / "labeling"
    assert "Create this Page's own folder" in workbench._next_step(vm)[0]
    view = workbench._data_space(vm)["preparation"]
    assert "Copy Page-folder request" in view
    assert "Copy setup request" not in view
    assert "S-Label-2/S-Label-2.md" in view
    panel = workbench._runs_panel(vm, "data", workbench._run_types(vm)["data"])
    assert re.search(r'data-op="source-normalize"[^>]*data-prompt=""', panel)
    assert "Create Page folder" in workbench.render_board(board, "board/board.md")
    assert workbench.board_jobs(board, "board/board.md")["empty"][0]["labeling_url"].endswith(
        "&space=data&view=preparation")

    folded = board / "pages" / "S-Label-2" / "S-Label-2.md"
    folded.parent.mkdir(parents=True)
    folded.write_text("# S-Label-2\n", encoding="utf-8")
    vm = workbench._view_model(flat)
    assert vm["page_ready"]
    assert vm["root"] == folded.parent / "labeling"
    assert "Copy setup request" in workbench._data_space(vm)["preparation"]
    assert "Prepare corpus" in workbench.render_board(board, "board/board.md")


def test_contract_prompt_requires_an_accepted_preparation_package(tmp_path, monkeypatch) -> None:
    state = fixtures._prepare(tmp_path)
    page = state["page"]
    vm = workbench._view_model(page)
    assert not workbench._meaning_allowed(vm)
    panel = workbench._runs_panel(vm, "data", workbench._run_types(vm)["data"])
    assert re.search(r'data-op="corpus-contract"[^>]*data-prompt=""', panel)
    assert "Complete and link Corpus Preparation" in workbench._data_space(vm)["contract"]

    fixtures.prep.link(state["owner"], Path(state["package"]), page)
    vm = workbench._view_model(page)
    assert not workbench._meaning_allowed(vm)
    panel = workbench._runs_panel(vm, "data", workbench._run_types(vm)["data"])
    assert "Use /subjective-label to create the Labeling Contract" in panel
    assert str(state["package"]) in panel
    assert "run-labeling-corpus-contract Ticket and Result" in panel
    assert "accepted package" in workbench._data_space(vm)["contract"]

    fixtures.job.create_contract(source_job=Path(state["package"]),
                                 job_root=page.parent / "labeling", page_file=page,
                                 job_id="example", target="example", human_id="human",
                                 created_at="2026-09-29")
    vm = workbench._view_model(page)
    assert workbench._meaning_allowed(vm)
    panel = workbench._runs_panel(vm, "data", workbench._run_types(vm)["data"])
    assert re.search(r'data-op="corpus-contract"[^>]*data-prompt=""', panel)
    contract_card = re.search(r'<article class=run-card data-op="corpus-contract".*?</article>', panel)
    assert contract_card and "Rerun" not in contract_card.group()
    with monkeypatch.context() as patch:
        patch.setattr(workbench._canonical_job_module(), "_judged_items", lambda _: {"i01"})
        assert not workbench._meaning_allowed(vm)
    round_card = page.parent / "labeling" / "rounds" / "round_01" / "card.md"
    round_card.parent.mkdir(parents=True)
    round_card.write_text("# released\n", encoding="utf-8")
    assert not workbench._meaning_allowed(vm)
    assert workbench._g0_retroactive_block(vm)
    definition = workbench._labeling_space(vm)["definition"]
    assert "Meaning confirmation unavailable" in definition
    assert "data-confirm-meaning" not in definition


def test_open_definition_discussion_hides_g0_confirmation_button(tmp_path) -> None:
    root, page = calibration_fixtures.build_job(tmp_path)
    discussion_fixtures.dd.start(root, human_id="JL")
    vm = workbench._view_model(page)
    definition = workbench._labeling_space(vm)["definition"]
    assert "Meaning discussion open" in definition
    assert "data-confirm-meaning" not in definition


def test_blank_label_meanings_guide_discussion_before_confirmation(tmp_path) -> None:
    config = copy.deepcopy(calibration_fixtures.CONFIG)
    del config["labels"]["meanings"]
    _, page = calibration_fixtures.build_job(tmp_path, config)
    vm = workbench._view_model(page)
    assert workbench._next_step(vm) == (
        "Define every label meaning in a Definition discussion before confirming G0.", "labeling")
    definition = workbench._labeling_space(vm)["definition"]
    assert "Define label meanings first" in definition
    assert "data-confirm-meaning" not in definition
    panel = workbench._runs_panel(vm, "labeling", workbench._run_types(vm)["labeling"])
    assert "<button type=button class=\"run-type run-new\">+ New Run</button>" in panel
    assert "definition-discussion" in panel
    assert '"missing_meanings": ["high", "low", "none"]' in workbench.render(
        page, "", "", "", None, standalone=True)
    row = workbench._job_row(page, {"file": page.name}, "")
    assert row["badge"] == "Define meanings"


def test_missing_g0_receipt_from_prior_attestation_has_restore_door(tmp_path, monkeypatch) -> None:
    root, page = calibration_fixtures.confirmed_job(tmp_path)
    calibration_fixtures.cal.release_round(root, human_id="JL")
    (root / "gates" / "g0" / "receipt.json").unlink()
    vm = workbench._view_model(page)
    assert workbench._g0_repair_request(vm)
    assert workbench._next_step(vm) == (
        "Restore the missing G0 receipt from the earlier human confirmation.", "labeling")
    definition = workbench._labeling_space(vm)["definition"]
    assert "Restore G0 receipt" in definition
    assert "data-confirm-meaning" in definition
    rendered = workbench.render(page, "", "", "", None, standalone=True)
    assert '"g0_repair_request": true' in rendered
    monkeypatch.setattr(workbench, "_job_urls", lambda *_: ("/labeling", "/page"))
    row = workbench._job_row(page, {"file": page.name}, "")
    assert row["badge"] == "Restore G0"


def test_post_release_g0_is_read_only_even_when_its_receipt_matches(tmp_path) -> None:
    root, page = calibration_fixtures.confirmed_job(tmp_path)
    card = root / "rounds" / "round_01" / "card.md"
    card.parent.mkdir(parents=True)
    card.write_text("# round_01\nreleased_at: 2026-09-15T12:00:00+00:00\n", encoding="utf-8")
    vm = workbench._view_model(page)
    assert workbench._g0_retroactive_block(vm)
    assert not workbench._g0_repair_request(vm)
    assert workbench._next_step(vm)[1] == "labeling"
    definition = workbench._labeling_space(vm)["definition"]
    assert "Meaning confirmation unavailable" in definition
    assert "data-confirm-meaning" not in definition
    historical_run = {"run": "rl04_human-calibration_round-01", "name": "human-calibration",
                      "label": "round-01", "operation": "human-calibration", "target": "round-01",
                      "status": "running", "owner": str(root.parent), "outcome": "",
                      "artifacts": [], "started_at": "", "finished_at": ""}
    run_card = workbench._run_card(vm, historical_run, ["subjective-label-rounds"])
    assert "blocked history" in run_card
    assert "<summary>Record</summary>" in run_card
    assert "data-copy=" not in run_card


def test_human_calibration_first_run_prompt_needs_an_open_round(tmp_path, monkeypatch) -> None:
    root = tmp_path / "Label-1" / "labeling"
    root.mkdir(parents=True)
    page = root.parent / "Label-1.md"
    page.write_text("# Label-1\n", encoding="utf-8")
    board = tmp_path / "board.md"
    board.write_text("# Board\n", encoding="utf-8")
    types = [
        {"op": "round-prepare", "views": ["rounds"], "words": "Draw one round", "runs": []},
        {"op": "human-calibration", "views": ["rounds"], "words": "You label one round", "runs": []},
    ]
    vm = {"root": root, "page_candidate": page,
          "config": {"construct": {"question": "How unsafe?"}},
          "cal": {"current_round": None}, "canonical": {"hold": False, "g0_passed": True}}
    panel = workbench._runs_panel(vm, "labeling", types)
    assert re.search(r'data-op="human-calibration"[^>]*data-prompt=""', panel)
    assert re.search(r'data-op="round-prepare"[^>]*data-prompt=""', panel)

    vm["cal"]["current_round"] = {"round_id": "round_01", "state": "prepared",
                                  "batch_size": 1, "finals": 0, "open_item": "i01"}
    card = root / "rounds" / "round_01" / "card.md"
    card.parent.mkdir(parents=True)
    card.write_text("# Round 1\n", encoding="utf-8")
    monkeypatch.setattr(workbench, "_round_draw", lambda *_: {
        "items": [{"item_id": "i01", "order": 0, "state": "waiting", "first": None}],
        "card": {"released_at": "2026-09-29T12:00:00+00:00", "released_by": "human"}})
    panel = workbench._runs_panel(vm, "labeling", types)
    assert "Continue labeling round 1" in panel
    assert "Next items: #1 item i01" in panel
    assert "Call open_item for the next unfinished item" in panel
    assert f"Board: {board}" in panel
    assert f"Page: {page}" in panel
    assert "Run Type: human-calibration · target: round_01" in panel
    assert "Run: none yet · status: not started" in panel
    assert "Prerequisite: G0 passed; released Card verified." in panel
    assert re.search(r'data-op="round-prepare"[^>]*data-prompt=""', panel)

    vm["cal"]["current_round"]["calibration_run"] = "run-labeling-human-calibration-0929-round-01"
    panel = workbench._runs_panel(vm, "labeling", types)
    assert re.search(r'data-op="human-calibration"[^>]*data-prompt=""', panel)
    vm["cal"]["current_round"].pop("calibration_run")
    vm["canonical"]["hold"] = True
    panel = workbench._runs_panel(vm, "labeling", types)
    assert re.search(r'data-op="human-calibration"[^>]*data-prompt=""', panel)


def test_human_calibration_resume_only_for_the_current_open_batch(tmp_path, monkeypatch) -> None:
    root = tmp_path / "Label-1" / "labeling"
    root.mkdir(parents=True)
    run = {"operation": "human-calibration", "status": "running",
           "run": "run-labeling-human-calibration-0929-round-01", "target": "round-01"}
    vm = {"root": root, "config": {}, "canonical": {"hold": False},
          "cal": {"current_round": None}}
    assert workbench._run_again(vm, run) == ("", "")

    vm["cal"]["current_round"] = {"round_id": "round_01", "open_item": "i01"}
    monkeypatch.setattr(workbench, "_round_draw", lambda *_: {"items": []})
    action, prompt = workbench._run_again(vm, run)
    assert action == "Resume" and "Continue labeling round 1" in prompt

    run["target"] = "round-02"
    assert workbench._run_again(vm, run) == ("", "")
    run["target"] = "round-01"
    run["status"] = "complete"
    assert workbench._run_again(vm, run) == ("", "")

    run["status"] = "running"
    vm["cal"] = {"current_round": None, "rounds": [{"round_id": "round_01",
                  "state": "judged", "calibration_status": "running"}]}
    vm["config"] = {"authority": {"human_id": "H"}}
    action, prompt = workbench._run_again(vm, run)
    assert action == "Resume"
    assert "calibration.py finalize" in prompt
    assert "Do not repeat a judgment" in prompt


def test_interrupted_finalization_is_the_next_page_and_board_step(tmp_path, monkeypatch) -> None:
    root, page = calibration_fixtures.confirmed_job(tmp_path)
    calibration_fixtures.cal.release_round(root, human_id="JL")
    for index in range(4):
        opened = calibration_fixtures.cal.open_item(root, "round_01", human_id="JL", session_id="s")
        item_id = opened["item"]["item_id"]
        calibration_fixtures.cal.record_first(root, "round_01", item_id, human_id="JL",
                                              session_id="s", class_label="low", region=None,
                                              uncertainty="low")
        if index == 3:
            with monkeypatch.context() as patch:
                def interrupted(*_args, **_kwargs):
                    raise RuntimeError("interrupted close")
                patch.setattr(calibration_fixtures.cal, "_close_calibration", interrupted)
                try:
                    calibration_fixtures.cal.record_final(root, "round_01", item_id,
                                                          human_id="JL", session_id="s",
                                                          class_label="low", region=None,
                                                          uncertainty="low")
                except RuntimeError as error:
                    assert str(error) == "interrupted close"
                else:
                    raise AssertionError("last Result close should have been interrupted")
        else:
            calibration_fixtures.cal.record_final(root, "round_01", item_id,
                                                  human_id="JL", session_id="s",
                                                  class_label="low", region=None,
                                                  uncertainty="low")
    vm = workbench._view_model(page)
    assert "Finish its interrupted human-calibration Result" in workbench._next_step(vm)[0]
    run = next(r for r in vm["runs"] if r["operation"] == "human-calibration")
    assert "calibration.py finalize" in workbench._run_again(vm, run)[1]
    row = workbench._job_row(page, {"id": "S-Label-9", "title": "Labeling job",
                                    "file": "pages/S-Label-9/S-Label-9.md", "group": "Data"},
                             "/board/board.md")
    assert row["badge"] == "Finish Run" and row["kind"] == "labeling"


def test_dedicated_host_opens_a_canonical_page_without_a_board(tmp_path) -> None:
    page = tmp_path / "pages" / "Label-1" / "Label-1.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Labeling Page\n", encoding="utf-8")
    handler = workbench.LabelingMixin()
    handler.root = tmp_path
    handler.only = frozenset({"labeling"})
    resolved, err = handler._labeling_page_target("pages/Label-1/Label-1.md")
    assert (resolved, err) == (page, None)
    html = workbench.render(page, "", "pages/Label-1/Label-1.md", "", None,
                            standalone=True)
    assert '"mode": "page"' in html
    assert "Studio Chat</a>" not in html
    assert "All labeling jobs" not in html
    assert 'data-view=preparation' in html
    assert "Copy setup request" in html


def test_standalone_page_target_rejects_flat_traversal_and_symlink(tmp_path) -> None:
    page = tmp_path / "pages" / "Label-1" / "Label-1.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Labeling Page\n", encoding="utf-8")
    flat = tmp_path / "pages" / "Label-2.md"
    flat.write_text("# Flat\n", encoding="utf-8")
    (tmp_path / "linked").symlink_to(page.parent, target_is_directory=True)
    handler = workbench.LabelingMixin()
    handler.root = tmp_path
    handler.only = frozenset({"labeling"})
    for value in ("pages/Label-2.md", "../outside/Outside.md", "/absolute/Label-1.md",
                  "pages//Label-1/Label-1.md", "linked/Label-1.md",
                  "pages/Label-1/../Label-1/Label-1.md", "pages\\Label-1\\Label-1.md"):
        assert handler._labeling_page_target(value)[0] is None, value
    handler.only = frozenset()
    assert handler._labeling_page_target("pages/Label-1/Label-1.md")[0] is None


def test_standalone_write_requires_same_origin_then_engine_contract(tmp_path) -> None:
    page = tmp_path / "pages" / "Label-1" / "Label-1.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Labeling Page\n", encoding="utf-8")
    handler = workbench.LabelingMixin()
    handler.root = tmp_path
    handler.only = frozenset({"labeling"})
    payload = {"mode": "page", "file": "pages/Label-1/Label-1.md",
               "action": "release_round", "human_id": "H", "attest": True}
    handler.headers = {"Host": "127.0.0.1:5601"}
    assert handler.labeling_act(payload)[0] == 403
    handler.headers["Origin"] = "http://evil.example"
    assert handler.labeling_act(payload)[0] == 403
    handler.headers["Origin"] = "http://127.0.0.1:5601"
    code, result = handler.labeling_act(payload)
    assert code == 409 and "no canonical labeling job" in result["err"]
    handler.only = frozenset()
    assert handler.labeling_act(payload)[0] == 400
