import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ENGINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE))
from src.page_workspace import (build_page, create_page, load_page, read_source,
                                render_page, save_source)
from src.page_setup import run_setup, setup_markdown_page
from src.plan_shape import canonical_plan
from src.page_setup_check import validate_setup
from src.page_migration import migrate_embedded_drafts, migrate_global_paragraphs
from live.outline_preview import bullet_token, read_drafts
from src.plan_shape import iter_plan_bullets


def test_import_edit_build_portable(tmp_path):
    original = tmp_path / "input.md"
    original.write_text("# Notes\n\nOriginal sentence.\n", encoding="utf-8")
    page = create_page(original, tmp_path / "my-page")
    assert page.content.read_bytes() == original.read_bytes()
    assert not (page.folder / "board.md").exists()
    rel = page.content.relative_to(page.folder).as_posix()
    current = read_source(page, rel)
    save_source(page, rel, "# Notes\n\nEdited sentence.\n", current["sha256"])
    assert "Original sentence." in original.read_text()
    assert "Edited sentence." in render_page(page)
    with pytest.raises(ValueError, match="changed"):
        save_source(page, rel, "lost update", current["sha256"])
    output = build_page(page)
    assert 'data-live="false"' in output.read_text()
    assert 'id="static-workspace"' in output.read_text()
    assert (output.parent / rel).read_text() == page.content.read_text()
    marker = json.loads((output.parent / ".haipipe-page-export").read_text())
    assert marker["schema"] == "haipipe-page-export/v2"
    assert marker["source"] == page.source.relative_to(page.folder).as_posix()
    assert marker["source_sha256"] == hashlib.sha256(page.source.read_bytes()).hexdigest()
    relocated = tmp_path / "relocated"
    shutil.copytree(page.folder, relocated)
    assert "Edited sentence." in render_page(load_page(relocated))


def test_html_and_static_assets_preserved(tmp_path):
    original = tmp_path / "input.html"
    original.write_text('<html><link rel="stylesheet" href="assets/theme.css"><h1>Hello</h1></html>')
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets/theme.css").write_text("h1 { color: blue; }")
    page = create_page(original, tmp_path / "html-page")
    assert page.content.read_bytes() == original.read_bytes()
    assert (page.content.parent / "assets/theme.css").exists()
    html = render_page(page)
    assert 'sandbox="allow-scripts"' in html
    output = build_page(page)
    assert (output.parent / "outline/evidence/materials/assets/theme.css").exists()


def test_scope_and_overwrite_guards(tmp_path):
    original = tmp_path / "input.txt"
    original.write_text("hello")
    page = create_page(original, tmp_path / "my-page")
    with pytest.raises(ValueError, match="exists"):
        create_page(original, page.folder)
    with pytest.raises(ValueError):
        read_source(page, "../input.txt")
    (page.folder / "linked.txt").symlink_to(original)
    with pytest.raises(ValueError):
        read_source(page, "linked.txt")
    with pytest.raises(ValueError):
        build_page(page, page.folder)
    with pytest.raises(ValueError):
        build_page(page, tmp_path)


def test_missing_dependency_does_not_create_partial_folder(tmp_path):
    original = tmp_path / "input.md"
    original.write_text("![missing](absent.png)")
    with pytest.raises(ValueError, match="Missing"):
        create_page(original, tmp_path / "page")
    assert not (tmp_path / "page").exists()


def test_markdown_asset_rebase(tmp_path):
    original = tmp_path / "input.md"
    original.write_text("![Figure](image.svg)\n\n[Download](data.csv)")
    (tmp_path / "image.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
    (tmp_path / "data.csv").write_text("x\n1\n")
    page = create_page(original, tmp_path / "page")
    markup = render_page(page)
    assert 'src="outline/evidence/materials/image.svg"' in markup
    assert 'href="outline/evidence/materials/data.csv"' in markup


def test_imported_markdown_cannot_embed_external_files_or_execute_links(tmp_path):
    original = tmp_path / "input.md"
    original.write_text('![[outside-audit.txt]]\n\n[Audit](javascript: document.body.dataset.audit=1)\n')
    (tmp_path / "outside-audit.txt").write_text("SYNTHETIC_PRIVATE_MARKER")
    page = create_page(original, tmp_path / "page")
    markup = render_page(page)
    assert "SYNTHETIC_PRIVATE_MARKER" not in markup
    assert 'href="javascript:' not in markup
    assert 'href="#blocked-link"' in markup


def test_page_face_embed_cannot_escape_folder(tmp_path):
    original = tmp_path / "input.txt"
    original.write_text("Hello")
    (tmp_path / "outside-audit.txt").write_text("SYNTHETIC_PRIVATE_MARKER")
    page = create_page(original, tmp_path / "page")
    page.source.write_text(page.source.read_text().replace("## Content", "## Content\n\n![[outside-audit.txt]]\n\n[Audit](javascript: alert)\n"))
    markup = render_page(page)
    assert "SYNTHETIC_PRIVATE_MARKER" not in markup
    assert 'href="javascript:' not in markup


def test_render_revalidates_attachment_and_private_lanes(tmp_path):
    original = tmp_path / "input.txt"
    original.write_text("hello")
    page = create_page(original, tmp_path / "page")
    (page.folder / "studio").mkdir()
    (page.folder / "studio/private.txt").write_text("SYNTHETIC_PRIVATE_MARKER")
    face = page.source.read_text()
    page.source.write_text(face.replace("## Content", "## Content\n\n![[studio/private.txt]]\n"))
    assert "SYNTHETIC_PRIVATE_MARKER" not in render_page(page)
    (page.folder / ".hidden.txt").write_text("SYNTHETIC_PRIVATE_MARKER")
    page.source.write_text(face.replace("outline/evidence/materials/input.txt", ".hidden.txt"))
    with pytest.raises(ValueError):
        render_page(page)


SERVERS = ENGINE.parents[2] / "servers"


def isolated_runtime(tmp_path):
    """A copy of the workbench's Page skill plus its servers tree, and nothing else.

    No Board skill is copied: the Page engine must run with only its own
    grammar and the plugin-level servers (presenters and reader assets) that
    ``skills/page/haipipe-page`` reaches at ``../../../servers``.
    """
    workbench = tmp_path / "workbench"
    isolated = workbench / "skills" / "page" / "haipipe-page"
    shutil.copytree(ENGINE, isolated, ignore=shutil.ignore_patterns("__pycache__", "tests"))
    shutil.copytree(SERVERS, workbench / "servers",
                    ignore=shutil.ignore_patterns("__pycache__", "tests", "checks"))
    return isolated


def test_runtime_copied_without_board(tmp_path):
    isolated = isolated_runtime(tmp_path)
    source = tmp_path / "hello.txt"
    source.write_text("No Board installation required.")
    destination = tmp_path / "standalone"
    for args in (("init", "--file", str(source), "--dest", str(destination)),
                 ("build", str(destination))):
        result = subprocess.run([sys.executable, str(isolated / "cli/page.py"), *args],
                                cwd=tmp_path, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
    assert "No Board installation required." in (destination / "delivery/web/index.html").read_text()
    outline = destination / 'outline'
    outline.mkdir(exist_ok=True)
    (outline / 'standalone-outline-v0.1.md').write_text(
        '# Outline\napproved: ⬜\n\n## C1 · Source\n'
        '### C1.P1 · Source ownership\n'
        '- B1 · The imported source keeps its original bytes\n'
        '  Note: The source stays inside this Page Folder.\n'
        '  Evidence: none · internal definition\n')
    result = subprocess.run([sys.executable, str(isolated / "cli/page.py"), 'build', str(destination)],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    markup = (destination / 'delivery/web/index.html').read_text()
    # The standalone reader keeps the plan in Draft/Outline Space; the static
    # Page Face remains the minimal Opening → Content surface.
    assert 'C1.P1.B1' not in markup
    assert 'Opening' in markup
    assert 'Content' in markup
    assert 'id="static-workspace"' in markup


def test_setup_cli_accepts_file_then_folder(tmp_path):
    isolated = isolated_runtime(tmp_path)
    source = tmp_path / "working-note.md"
    source.write_text(
        "# Working Note\n\n## Problem\n\nA revision can lose context.\n\n"
        "## Requirement\n\nThe Page should preserve each decision.\n",
        encoding="utf-8",
    )
    cli = [sys.executable, str(isolated / "cli/page.py"), "setup"]
    created = subprocess.run([*cli, str(source)], cwd=tmp_path, capture_output=True, text=True)
    assert created.returncode == 0, created.stderr
    page = tmp_path / "working-note"
    assert (page / "delivery/web/index.html").is_file()
    assert (page / "results/r01_page-setup/report.md").is_file()
    runtime = (page / "results/r01_page-setup/runtime.yaml").read_text()
    assert "outcome: \"Created semantic records:" in runtime
    assert "inputs:\n  - path:" in runtime
    assert "supersedes: null" in runtime
    assert "failure: null" in runtime
    first_checks = json.loads((page / "results/r01_page-setup/checks.json").read_text())
    assert first_checks["blocking_gate"] == "pass"
    assert '"mode": "create-semantic-records"' in created.stdout

    resumed = subprocess.run([*cli, str(page)], cwd=tmp_path, capture_output=True, text=True)
    assert resumed.returncode == 0, resumed.stderr
    assert (page / "results/r02_page-setup/report.md").is_file()
    second_checks = json.loads((page / "results/r02_page-setup/checks.json").read_text())
    assert second_checks["blocking_gate"] == "pass"
    assert '"mode": "resume-and-build"' in resumed.stdout


def test_page_styles_are_shared_with_board(tmp_path):
    """One file per stylesheet part: the Board bundle reads the Page's own parts."""
    from src.page_assets import ASSETS, css
    import host_assets  # servers/_host, on sys.path via src/__init__.py
    board_parts = {part.name: part for part in host_assets.parts("css", ".css")}
    page_parts = sorted((ASSETS / "css").glob("*.css"))
    assert page_parts
    for part in page_parts:
        assert board_parts[part.name].resolve() == part.resolve()
    original = tmp_path / "input.txt"
    original.write_text("Shared appearance.")
    markup = render_page(create_page(original, tmp_path / "page"))
    assert css() in markup
    assert 'class="single split standalone"' in markup
    assert '<main id="reading" class="wrap">' in markup
    assert 'id="page-workbench-config"' in markup
    assert markup.index('📃 Page') < markup.index('📤 Delivery') < markup.index('📂 Folder')
    assert '⚙️ Runs' not in markup
    assert '>Evidence</a>' not in markup


def test_markdown_setup_populates_real_page_records(tmp_path):
    original = tmp_path / "argument.md"
    original.write_text(
        "# A Useful Argument\n\n```mermaid\nflowchart LR\nA --> B\n```\n\n"
        "## When revisions lose context\n\n"
        "Consider a narrow sentence edit. It can unexpectedly undo settled choices.\n\n"
        "> We want prior decisions to survive the next turn.\n\n"
        "## Preserve the decision\n\n"
        "The Page should keep feedback with the prose it changes.\n",
        encoding="utf-8",
    )
    page = create_page(original, tmp_path / "argument-page")
    result = setup_markdown_page(page)
    page = load_page(page.folder)

    assert result == {
        "title": "A Useful Argument", "divisions": 2, "paragraphs": 3,
        "bullets": 3, "source_sentences": 4,
        "plan": "outline/argument-page-outline-v0.1.md",
        "draft": "outline/argument-page-outline-v0.1.md", "run": "r01_page-setup",
        "delivery": "delivery/web/index.html", "mode": "create-semantic-records",
        "checks": {"pass": 10, "missing": 0, "deferred": 4, "untested": 2, "n/a": 1},
        "blocking_gate": "pass",
    }
    face = page.source.read_text(encoding="utf-8")
    assert "Working Page for" not in face
    assert "Setup complete; Outline review pending" in face
    assert "When revisions lose context" in face
    plan = page.folder / result["plan"]
    blocks = list(iter_plan_bullets(plan.read_text(encoding="utf-8")))
    drafts = read_drafts(page.source)
    assert len(blocks) == len(drafts) == 3
    assert all(block["address"] in drafts for block in blocks)
    assert [block["paragraph"] for block in blocks] == ["C1.P1", "C1.P2", "C2.P3"]
    assert drafts["C1.P1.B1"]["text"] == (
        "Consider a narrow sentence edit. It can unexpectedly undo settled choices."
    )
    assert "It can unexpectedly undo settled choices" in blocks[0]["head"]
    assert "[Example]" in plan.read_text(encoding="utf-8")
    assert "[Requirement]" in plan.read_text(encoding="utf-8")
    assert (page.folder / "outline/argument-page-context.md").is_file()
    assert (page.folder / "outline/argument-page-files.md").is_file()
    assert (page.folder / "results/r01_page-setup/report.md").is_file()
    audit = json.loads((page.folder / "results/r01_page-setup/checks.json").read_text())
    assert audit["blocking_gate"] == "pass"
    for name in ("page_face", "content", "shape", "content_draft", "static_delivery"):
        artifact = audit["artifacts"][name]
        path = page.folder / artifact["path"]
        assert artifact["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert {item["id"] for item in audit["checks"]} == {
        "source_configuration", "input_preservation", "opening", "outline_structure",
        "paragraph_global_order",
        "content_draft_mapping", "semantic_role_syntax", "content", "aims_structure",
        "bullet_head_readability", "static_delivery", "semantic_role_judgment",
        "outline_logic_judgment", "aim_targets",
        "human_shape_approval", "human_content_acceptance", "hosting",
    }

    markup = render_page(page)
    assert "The attached source is rendered here directly" not in markup
    assert "<h1>A Useful Argument</h1>" not in markup
    assert "<summary>When revisions lose context</summary>" in markup
    assert "Consider a narrow sentence edit" in markup
    # setup writes drafted Bullets Draft-first: the sentence on the dash line, the point in `Point:`
    assert "\n  Point: [" in (page.folder / result["draft"]).read_text(encoding="utf-8")
    assert "A Useful Argument" in build_page(page).read_text(encoding="utf-8")


def test_address_migration_preserves_drafts_and_makes_paragraphs_global(tmp_path):
    original = tmp_path / "argument.md"
    original.write_text(
        "# Argument\n\n## First\n\nThe first move establishes context.\n\n"
        "## Second\n\nThe second move closes the argument.\n",
        encoding="utf-8",
    )
    page = create_page(original, tmp_path / "page")
    setup_markdown_page(page)
    page = load_page(page.folder)
    plan = page.folder / "outline/page-outline-v0.1.md"
    plan.write_text(plan.read_text().replace("C2.P2", "C2.P1"), encoding="utf-8")

    result = migrate_global_paragraphs(page)

    assert result["changed_addresses"] == 1
    assert "### C2.P2 ·" in plan.read_text()
    assert read_drafts(page.source)["C2.P2.B1"]["text"] == (
        "The second move closes the argument."
    )


def test_migrate_legacy_preview_into_outline_is_content_preserving(tmp_path):
    original = tmp_path / "argument.md"
    original.write_text("# Argument\n\n## Claim\n\nA claim needs review.\n", encoding="utf-8")
    page = create_page(original, tmp_path / "page")
    setup_markdown_page(page)
    page = load_page(page.folder)
    plan = page.folder / "outline/page-outline-v0.1.md"
    records = read_drafts(page.source)
    plan.write_text(
        "\n".join(line for line in canonical_plan(plan.read_text()).splitlines()
                  if not line.startswith("  Draft:")) + "\n"
    )
    legacy = page.folder / "outline/page-preview.md"
    record = records["C1.P1.B1"]
    legacy.write_text(
        "# page · Content preview\n\nPlanning draft for discussion.\n\n"
        f"## C1.P1.B1\nplan: v0.1\nbullet-sha256: {record['bullet-sha256']}\n\n"
        f"{record['text']}\n",
        encoding="utf-8",
    )

    result = migrate_embedded_drafts(page)

    assert result["migrated"] == 1
    assert read_drafts(page.source)["C1.P1.B1"]["text"] == record["text"]
    assert not legacy.exists()
    assert (page.folder / "outline/_archive/legacy-outline-preview/page-preview.md").is_file()


def test_setup_never_clips_a_long_reader_move_to_a_word_limit(tmp_path):
    original = tmp_path / "argument.md"
    sentence = (
        "Appointment wait time indicates how quickly a clinic can offer an "
        "initial visit."
    )
    comparison = (
        "Patients may compare wait time when choosing among clinics that offer "
        "the same service."
    )
    limitation = (
        "Short waits do not guarantee that every patient can use the available "
        "appointment."
    )
    oxford = (
        "Transportation, work schedules, and insurance rules can still prevent "
        "practical access."
    )
    original.write_text(
        f"# Access\n\n## Availability\n\n{sentence}\n\n{comparison}\n\n"
        f"## Constraints\n\n{limitation}\n\n{oxford}\n",
        encoding="utf-8",
    )
    page = create_page(original, tmp_path / "page")
    result = setup_markdown_page(page)
    plan = (page.folder / result["plan"]).read_text(encoding="utf-8")
    assert sentence.rstrip(".") in plan
    assert comparison.rstrip(".") in plan
    assert limitation.rstrip(".") in plan
    assert oxford.rstrip(".") in plan
    assert "clinic can offer\n" not in plan
    assert "Transportation, work schedules\n" not in plan
    blocks = list(iter_plan_bullets(plan))
    assert [block["paragraph"] for block in blocks] == [
        "C1.P1", "C1.P2", "C2.P3", "C2.P4",
    ]
    assert "[Possibility] Patients may compare" in plan
    assert "[Possibility] Appointment wait time" not in plan
    assert "[Possibility] Short waits" not in plan
    assert "[Mechanism] Transportation, work schedules" in plan
    checks = json.loads((page.folder / "results/r01_page-setup/checks.json").read_text())
    readability = next(
        item for item in checks["checks"] if item["id"] == "bullet_head_readability"
    )
    assert readability["status"] == "pass"


def test_markdown_setup_refuses_to_replace_authored_records(tmp_path):
    original = tmp_path / "argument.md"
    original.write_text("# Argument\n\n## Claim\n\nA claim needs review.\n", encoding="utf-8")
    page = create_page(original, tmp_path / "page")
    setup_markdown_page(page)
    with pytest.raises(ValueError, match="already has authored/setup records"):
        setup_markdown_page(load_page(page.folder))


def test_setup_resume_builds_without_replacing_shape(tmp_path):
    from src.page_setup import run_setup

    original = tmp_path / "argument.md"
    original.write_text("# Argument\n\n## Claim\n\nA claim needs review.\n", encoding="utf-8")
    page = create_page(original, tmp_path / "page")
    setup_markdown_page(page)
    page = load_page(page.folder)
    plan = page.folder / "outline/page-outline-v0.1.md"
    before = plan.read_bytes()
    result = run_setup(page)
    assert result["mode"] == "resume-and-build"
    assert result["run"] == "r02_page-setup"
    assert result["delivery"] == "delivery/web/index.html"
    assert result["blocking_gate"] == "pass"
    assert result["source_sentences"] == 1
    assert plan.read_bytes() == before


def test_setup_resume_preserves_recorded_source_count_after_preview_normalization(tmp_path):
    original = tmp_path / "argument.md"
    original.write_text(
        "# Argument\n\n## Claim\n\nDetailed edition · Cartoon edition · Compare both series\n",
        encoding="utf-8",
    )
    page = create_page(original, tmp_path / "page")
    created = setup_markdown_page(page)
    page = load_page(page.folder)
    plan = page.folder / "outline/page-outline-v0.1.md"
    plan.write_text(
        plan.read_text(encoding="utf-8").replace(
            "Detailed edition · Cartoon edition · Compare both series",
            "Detailed edition . Cartoon edition . Compare both series",
        ),
        encoding="utf-8",
    )

    resumed = run_setup(page)

    assert created["source_sentences"] == 1
    assert resumed["source_sentences"] == 1


def test_setup_resume_rebinds_reviewed_head_without_changing_draft(tmp_path):
    original = tmp_path / "argument.md"
    original.write_text(
        "# Argument\n\n## Claim\n\nA rough draft exposes a hidden question. "
        "The next draft should preserve the answer.\n",
        encoding="utf-8",
    )
    page = create_page(original, tmp_path / "page")
    setup_markdown_page(page)
    page = load_page(page.folder)
    plan = page.folder / "outline/page-outline-v0.1.md"
    before = read_drafts(page.source)["C1.P1.B1"]["text"]
    plan.write_text(
        plan.read_text().replace(
            "[Requirement] The next draft should preserve the answer",
            "[Learning] Draft answers must survive the next revision",
        ),
        encoding="utf-8",
    )

    result = run_setup(page)
    block = iter_plan_bullets(plan.read_text())[0]
    rebound = read_drafts(page.source)["C1.P1.B1"]

    assert result["blocking_gate"] == "pass"
    assert rebound["text"] == before
    assert rebound["bullet-sha256"] == bullet_token(block)


def test_setup_resume_fails_gate_and_records_audit_when_content_draft_is_missing(tmp_path):
    from src.page_setup import run_setup

    original = tmp_path / "argument.md"
    original.write_text("# Argument\n\n## Claim\n\nA claim needs review.\n", encoding="utf-8")
    page = create_page(original, tmp_path / "page")
    setup_markdown_page(page, input_file=original)
    page = load_page(page.folder)
    plan = page.folder / "outline/page-outline-v0.1.md"
    plan.write_text(
        "\n".join(line for line in canonical_plan(plan.read_text()).splitlines()
                  if not line.startswith("  Draft:")) + "\n"
    )

    with pytest.raises(ValueError, match="setup validation failed"):
        run_setup(page)

    runtime = (page.folder / "results/r02_page-setup/runtime.yaml").read_text()
    audit = json.loads((page.folder / "results/r02_page-setup/checks.json").read_text())
    assert "status: failed" in runtime
    assert audit["blocking_gate"] == "fail"
    draft = next(item for item in audit["checks"] if item["id"] == "content_draft_mapping")
    assert draft["status"] == "missing"
    assert draft["blocking"] is True


def test_force_setup_allows_intentional_content_edit_without_recertifying_intake_hash(tmp_path):
    original = tmp_path / "argument.md"
    original.write_text("# Argument\n\n## Claim\n\nA claim needs review.\n", encoding="utf-8")
    page = create_page(original, tmp_path / "page")
    setup_markdown_page(page, input_file=original)
    page = load_page(page.folder)
    page.content.write_text(
        "# Argument\n\n## Claim\n\nAn intentionally revised claim still needs review.\n",
        encoding="utf-8",
    )

    result = setup_markdown_page(page, force=True, input_file=original)

    assert result["blocking_gate"] == "pass"
    audit = json.loads((page.folder / "results/r02_page-setup/checks.json").read_text())
    preservation = next(item for item in audit["checks"] if item["id"] == "input_preservation")
    assert preservation["status"] == "untested"
    assert preservation["blocking"] is False
