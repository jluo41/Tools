import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ENGINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE))
from src.page_workspace import (build_page, create_page, load_page, read_source,
                                render_page, save_source)


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


def test_runtime_copied_without_board(tmp_path):
    isolated = tmp_path / "runtime"
    shutil.copytree(ENGINE, isolated, ignore=shutil.ignore_patterns("__pycache__", "tests"))
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
    assert 'C1.P1.B1' in markup
    assert 'id="static-workspace"' in markup


def test_page_styles_are_shared_with_board(tmp_path):
    from src.page_assets import css
    board_assets = ENGINE.parents[1] / "board/haipipe-board/assets/css"
    for part in (ENGINE / "assets/css").glob("*.css"):
        adapter = board_assets / part.name
        assert adapter.is_symlink()
        assert adapter.resolve() == part.resolve()
    original = tmp_path / "input.txt"
    original.write_text("Shared appearance.")
    markup = render_page(create_page(original, tmp_path / "page"))
    assert css() in markup
    assert 'class="single split standalone"' in markup
    assert '<main id="reading" class="wrap">' in markup
    assert 'id="page-plugin-config"' in markup
    assert markup.index('🧭 Outline') < markup.index('⚙️ Runs') < markup.index('📤 Delivery') < markup.index('📂 Folder')
    assert '>Evidence</a>' not in markup
