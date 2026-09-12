"""Board consumes registered Page Folders without owning their source shape."""
import json
import re
import runpy
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

import pytest

from live.base import BaseMixin
from src.common import page_files, registered_page_source
from src.parse import parse_dir, parse_file


ENGINE = Path(__file__).resolve().parents[1]
PAGE = ENGINE.parents[1] / "page" / "haipipe-page"
CONTENT = "outline/evidence/materials/input.md"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def register(folder, **overrides):
    source = write(folder / f"{folder.name}.md",
                   f"# Imported notes\nsource-content: {CONTENT}\n\n"
                   "## Opening\nOne imported source.\n\n## Content\n\n## Aims\n")
    write(folder / CONTENT, "# Original source\nOriginal bytes.\n")
    data = dict(version=1, source=source.name, content=CONTENT, title="Imported notes")
    data.update(overrides)
    write(folder / "page.toml", "\n".join(
        f"{key} = {json.dumps(value, ensure_ascii=False)}" for key, value in data.items()))
    return source


def handler(root):
    result = BaseMixin()
    result.root = root
    return result


def test_board_packages_extend_to_page_in_fresh_process():
    code = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import src, live
from src import page_parse
assert str(Path(sys.argv[2]) / 'src') in src.__path__
assert str(Path(sys.argv[2]) / 'live') in live.__path__
assert Path(page_parse.__file__).resolve().parent == Path(sys.argv[2]) / 'src'
"""
    subprocess.run([sys.executable, "-B", "-c", code, str(ENGINE), str(PAGE)],
                   cwd=ENGINE, check=True, capture_output=True, text=True)


def test_missing_tomllib_keeps_legacy_imports_and_discovery(tmp_path):
    register(tmp_path / "ordinary")
    write(tmp_path / "Q1-legacy.md", "# Legacy\n## Opening\nText.\n")
    code = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
sys.modules['tomllib'] = None
from src.common import registered_page_source, page_files
from src.parse import parse_file
root = Path(sys.argv[2])
assert registered_page_source(root / 'ordinary') is None
assert list(page_files(root)) == [root / 'Q1-legacy.md']
meta, pages, warnings = parse_file('[BOARD]\\n# Legacy\\n[Q1]\\n# Question\\n## Opening\\nText.')
assert meta['title'] == 'Legacy'
assert [page['id'] for page in pages] == ['Q1']
assert not warnings
"""
    subprocess.run([sys.executable, "-B", "-c", code, str(ENGINE), str(tmp_path)],
                   cwd=ENGINE, check=True, capture_output=True, text=True)


def test_registered_generic_and_legacy_board_pages(tmp_path):
    board = tmp_path / "board-source"
    source = register(board / "group" / "ordinary-notes")
    legacy = write(board / "legacy" / "QA1-old.md", "# Old question\n## Opening\nOld.\n")
    stage = write(board / "S-Main-1-introduction.md", "# Introduction\n## Content\nText.\n")
    write(board / "unregistered.md", "# Not a Page\n")
    write(board / "board.md", "# Board\n## Pages\n### QA · Reading\n"
          "group/ordinary-notes/ordinary-notes.md\nQA1-old.md\nS-Main-1-introduction.md\n")
    discovered = list(page_files(board))
    assert set(discovered) == {source, legacy, stage}
    assert len(discovered) == 3
    _, pages, warnings = parse_dir(board)
    assert not warnings
    assert [p["id"] for p in pages] == ["ordinary-notes", "QA1", "S-Main-1"]
    # The existing application matcher precedes the Q matcher for QA1-*.
    assert [p["kind"] for p in pages] == ["page", "application", "stage"]
    assert pages[0]["file"] == "group/ordinary-notes/ordinary-notes.md"
    assert pages[0]["source_content"] == CONTENT
    assert handler(tmp_path).target({"path": "/board-source/board/QA/ordinary-notes.html",
                                     "file": pages[0]["file"]}) == (source, board)


def test_registered_q_keeps_legacy_identity_and_bare_roster_name(tmp_path):
    source = register(tmp_path / "QA1-imported")
    write(tmp_path / "board.md", "# Board\n## Pages\nQA1-imported.md\n")
    _, pages, warnings = parse_dir(tmp_path)
    assert not warnings
    assert [(p["id"], p["kind"]) for p in pages] == [("QA1", "application")]
    assert list(page_files(tmp_path)) == [source]


def test_single_file_legacy_board_still_parses():
    meta, pages, warnings = parse_file("[BOARD]\n# Old Board\n[Q1]\n# Question\n## Opening\nText.")
    assert meta["title"] == "Old Board"
    assert [p["id"] for p in pages] == ["Q1"]
    assert not warnings


def test_authored_manifest_without_content_discovers_and_builds(tmp_path):
    board = tmp_path / "board-source"
    source = write(board / "authored" / "authored.md",
                   "# Authored Page\n## Opening\nAuthored source without an import.\n"
                   "## Content\n### 1 · Observations\n" +
                   "\n\n".join(f"Observation {i}: authored Page content remains readable "
                                "through both Board and standalone rendering."
                                for i in range(20)) + "\n## Aims\nReview the observations.\n")
    write(source.parent / "page.toml",
          'version = 1\nsource = "authored.md"\ntitle = "Authored Page"\n')
    write(board / "board.md", "# Board\n## Pages\nauthored/authored.md\n")
    assert registered_page_source(source.parent) == source
    assert list(page_files(board)) == [source]
    _, pages, warnings = parse_dir(board)
    assert not warnings
    assert pages[0]["file"] == "authored/authored.md"
    assert pages[0]["source_content"] == ""
    assert not (source.parent / "outline/evidence/materials").exists()
    server = handler(tmp_path)
    server.rebuild(board)
    assert "Authored source without an import." in (
        board / "board/_ungrouped/authored.html").read_text(encoding="utf-8")
    server.rebuild(source)
    assert "Authored source without an import." in (
        source.parent / "delivery/web/index.html").read_text(encoding="utf-8")
    source.unlink()
    assert registered_page_source(source.parent) is None


@pytest.mark.parametrize("override", [
    {"version": 2}, {"version": True}, {"source": "../escape.md"},
    {"source": "/absolute.md"}, {"source": "other.md"},
    {"content": "outline/evidence/materials/../../escape.md"},
    {"content": "/outside.md"}, {"content": "outline/evidence/materials/missing.md"},
    {"content": ""},
    {"title": 42},
])
def test_invalid_manifest_does_not_register_generic_page(tmp_path, override):
    source = register(tmp_path / "ordinary", **override)
    assert registered_page_source(source.parent) is None
    assert source not in list(page_files(tmp_path))
    assert handler(tmp_path).target({"path": "/ordinary/page/index.html",
                                     "file": "ordinary.md"})[0] is None


def test_malformed_manifest_and_symlink_escapes_are_rejected(tmp_path):
    root = tmp_path / "root"
    source = register(root / "ordinary")
    outside = write(tmp_path / "outside.md", "# Outside\n")
    material = source.parent / CONTENT
    material.unlink()
    material.symlink_to(outside)
    assert registered_page_source(source.parent) is None
    material.unlink()
    write(material, "Inside")
    source.unlink()
    source.symlink_to(outside)
    assert registered_page_source(source.parent) is None
    assert handler(root).target({"path": "/ordinary/page/index.html", "file": source.name})[0] is None
    source.unlink()
    write(source, "# Inside")
    write(source.parent / "page.toml", "version = [broken")
    assert registered_page_source(source.parent) is None


@pytest.mark.parametrize("prefix", ["_archive", ".hidden", "board", "fig", "parent/outline/materials"])
def test_registration_respects_discovery_boundaries(tmp_path, prefix):
    if prefix.startswith("parent/"):
        register(tmp_path / "parent")
    source = register(tmp_path / prefix / "ordinary")
    assert source not in list(page_files(tmp_path))


def test_standalone_resolves_registered_and_same_stem_faces(tmp_path):
    source = register(tmp_path / "ordinary")
    server = handler(tmp_path)
    for url in ("/ordinary/ordinary.md", "/ordinary/page/index.html", "/ordinary/board.md"):
        assert server.target({"path": url, "file": source.name}) == (source, source)
    face = write(tmp_path / "existing" / "existing.md", "# Existing\n## Opening\nText.\n")
    assert server.target({"path": "/existing/index.html", "file": face.name}) == (face, face)
    stray = write(face.parent / "QA1-stray.md", "# Stray")
    assert server.target({"path": "/existing/index.html", "file": stray.name})[0] is None
    plain = write(tmp_path / "notes" / "notes.md", "# Ordinary document")
    assert server.target({"path": "/notes/index.html", "file": plain.name})[0] is None


def test_page_folder_root_does_not_discover_its_imported_materials(tmp_path):
    source = register(tmp_path / "ordinary")
    write(source.parent / "outline/evidence/materials/QA1-input.md", "# Imported")
    assert list(page_files(source.parent)) == [source]


def test_board_and_standalone_build_the_same_registered_source(tmp_path):
    board = tmp_path / "board-source"
    source = register(board / "ordinary")
    # Board's existing CLI enforces >1200 rendered characters even for a Page.
    asset = write(source.parent / "outline/evidence/materials/figure.svg",
                  '<svg xmlns="http://www.w3.org/2000/svg"><rect width="8" height="8"/></svg>')
    write(source.parent / CONTENT, "# Original source\nOriginal bytes.\n\n"
          "![Imported figure](figure.svg)\n\n" +
          "\n\n".join(f"Observation {i}: the source document retains its details "
                       "when rendered independently and as a registered Board Page."
                       for i in range(20)))
    write(board / "Q1-legacy.md", "# Legacy question\n## Opening\nLegacy content remains readable.\n"
          + "\n\n".join(f"Legacy observation {i} remains part of the scholarly Board source."
                        for i in range(20)))
    write(board / "board.md", "# Board\n## Pages\nordinary/ordinary.md\nQ1-legacy.md\n")
    server = handler(tmp_path)
    server.rebuild(board)
    rendered = board / "board/_ungrouped/ordinary.html"
    markup = rendered.read_text(encoding="utf-8")
    assert "Original bytes." in markup

    class Images(HTMLParser):
        def __init__(self):
            super().__init__()
            self.urls = []

        def handle_starttag(self, tag, attrs):
            if tag == "img":
                self.urls.append(dict(attrs).get("src", ""))

    images = Images()
    images.feed(markup)
    asset_url = next(url for url in images.urls if urlsplit(url).path.endswith("figure.svg"))
    assert asset_url == "../../ordinary/outline/evidence/materials/figure.svg"
    assert (rendered.parent / unquote(urlsplit(asset_url).path)).resolve() == asset.resolve()
    assert "Legacy content remains readable." in (
        board / "board/_ungrouped/Q1-legacy.html").read_text(encoding="utf-8")
    server.rebuild(source)
    standalone = source.parent / "delivery/web/index.html"
    assert "Original bytes." in standalone.read_text(encoding="utf-8")
    images = Images()
    images.feed(standalone.read_text(encoding="utf-8"))
    asset_url = next(url for url in images.urls if urlsplit(url).path.endswith("figure.svg"))
    exported_asset = standalone.parent / unquote(urlsplit(asset_url).path)
    assert exported_asset.read_bytes() == asset.read_bytes()
    assert not (source.parent / "board.md").exists()


@pytest.mark.parametrize("suffix,content", [
    (".md", "Tiny imported sentinel.\n"),
    (".txt", "Tiny imported sentinel.\n"),
    (".html", "<!doctype html><html><body>Tiny imported sentinel.</body></html>"),
])
def test_fresh_official_init_tiny_board_build_and_checker(tmp_path, suffix, content):
    original = write(tmp_path / ("tiny" + suffix), content)
    board = tmp_path / "reading-board"
    folder = board / "1-G1-reading" / "independent-note"

    def cli(script, *args):
        return subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                              cwd=ENGINE, capture_output=True, text=True)

    result = cli(PAGE / "cli/page.py", "init", "--file", original, "--dest", folder,
                 "--title", "An imported technical source with a deliberately long title")
    assert result.returncode == 0, result.stdout + result.stderr
    source = folder / "independent-note.md"
    manifest = folder / "page.toml"
    material = folder / "outline/evidence/materials" / original.name
    snapshots = {p: (p.read_bytes(), p.stat().st_ino)
                 for p in (source, manifest, material, original)}
    face = source.read_text()
    assert "owner: unassigned" in face
    assert "### A1 · Source" in face and "⬜ A1.1" in face
    write(board / "board.md", "# Reading Board\nspine: read the imported source\n"
          "close: the source is reviewed\n## Topic\nA synthetic technical import.\n"
          "## Pipeline\nImport then review.\n## Pages\n### G1 · Reading\n"
          "Discuss the imported source.\n1-G1-reading/independent-note/independent-note.md\n")
    result = cli(ENGINE / "cli/build.py", board)
    assert result.returncode == 0, result.stdout + result.stderr
    result = subprocess.run([sys.executable, "-B", str(ENGINE / "cli/build.py"), "."],
                            cwd=board, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    rendered = board / "board/G1/independent-note.html"
    html = rendered.read_text()
    bare = re.sub(r"<script.*?</script>", "", html, flags=re.S)
    assert 'data-file="1-G1-reading/independent-note/independent-note.md"' in bare
    if suffix != ".html":
        assert "Tiny imported sentinel." in bare
    else:
        assert "iframe" in bare and "tiny.html" in bare
    # A compact source must actually exercise the former failing threshold.
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", bare.split("<body", 1)[-1])).strip()
    assert len(plain) < 1200
    result = cli(ENGINE / "cli/check.py", board, "--strict", "--no-template")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR" not in result.stdout and "WARN" not in result.stdout, result.stdout
    assert snapshots == {p: (p.read_bytes(), p.stat().st_ino) for p in snapshots}


def test_registered_checker_preserves_legacy_and_checks_import_binding(tmp_path):
    checker = runpy.run_path(str(ENGINE / "cli/check.py"))
    source = register(tmp_path / "ordinary")
    # Registration is not permission to point the rendered face elsewhere.
    write(source, source.read_text().replace(CONTENT, "different.md"))
    rep = checker["Report"]()
    checker["check_face"](source, source.name, rep, {}, set())
    codes = {row[1] for row in rep.rows}
    assert "source-content-mismatch" in codes and "no-owner" in codes
    assert "opening-lead-not-a-question" not in codes
    legacy = write(tmp_path / "Q1-legacy.md", source.read_text().replace(
        "## Content\n", "## Content\n### 1 · Source\nTechnical source.\n"))
    rep = checker["Report"]()
    checker["check_face"](legacy, legacy.name, rep, {}, set())
    codes = {row[1] for row in rep.rows}
    assert {"no-owner", "opening-lead-not-a-question", "division-no-figure"} <= codes
    # An explicit scholarly variant must not inherit the base import exemption.
    write(source, "page-type: research\n" + legacy.read_text())
    rep = checker["Report"]()
    checker["check_face"](source, source.name, rep, {}, set())
    assert "opening-lead-not-a-question" in {row[1] for row in rep.rows}


def test_registered_html_gate_rejects_missing_or_script_only_face():
    check = runpy.run_path(str(ENGINE / "cli/build.py"))["check_registered_html"]
    def document(content, file="ordinary/ordinary.md"):
        return ('<!doctype html><html><head><title>Page</title></head><body>'
                f'<section class="slide q" data-file="{file}">{content}</section></body></html>')
    check(document("Tiny."), "ordinary/ordinary.md")
    for html in ("", document(""), document("<script>text</script>"),
                 document("<style>text</style>"), document("Tiny.", "wrong.md"),
                 document("Tiny.").replace("</section>", "")):
        with pytest.raises(AssertionError, match="static Page Face"):
            check(html, "ordinary/ordinary.md")


def test_registered_html_assets_reroot_without_changing_board_navigation(tmp_path):
    from src.page_board import tree_reroot
    folder = tmp_path / "group" / "ordinary"
    write(folder / "outline/evidence/materials/input file.html", "<p>Source</p>")
    # Real generated output is not a source asset, despite also being .html.
    write(tmp_path / "board/G1/ordinary.html", "<p>Generated</p>")
    write(tmp_path / "other/unrelated.html", "<p>Another Page's source</p>")
    asset = "group/ordinary/outline/evidence/materials/input%20file.html?view=1#part"
    markup = (f'<a href="{asset}">Source</a><iframe src="{asset}"></iframe>'
              f'<object data="{asset}"></object>'
              '<a href="../G1/ordinary.html">Page</a><a href="../index.html">Index</a>'
              '<a href="other/unrelated.html">Other</a>')
    result = tree_reroot(markup, "../../", src_dir=folder, board_root=tmp_path)
    for attr in ("href", "src", "data"):
        assert f'{attr}="../../{asset}"' in result
    assert 'href="../G1/ordinary.html"' in result
    assert 'href="../index.html"' in result
    assert 'href="other/unrelated.html"' in result


def test_board_resolution_preserves_legacy_and_rejects_unregistered_and_escape(tmp_path):
    board = tmp_path / "board-source"
    face = write(board / "QA1-old.md", "# Old")
    marker = write(board / "board.md", "# Board")
    write(board / "ordinary.md", "# Unregistered")
    server = handler(tmp_path)
    context = {"path": "/board-source/board/QA/QA1-old.html"}
    assert server.target(dict(context, file=face.name)) == (face, board)
    assert server.target(dict(context, file="board.md")) == (marker, board)
    for name in ("ordinary.md", "../QA1-old.md", "/QA1-old.md", "outline/../QA1-old.md"):
        assert server.target(dict(context, file=name))[0] is None
    outside = write(tmp_path / "QA2-outside.md", "# Outside Board")
    (board / "QA2-link.md").symlink_to(outside)
    assert server.target(dict(context, file="QA2-link.md"))[0] is None
    assert server.target({"path": "/../../outside.html", "file": face.name})[0] is None


def test_rebuild_dispatches_page_and_board_and_surfaces_failure(tmp_path, monkeypatch):
    board = tmp_path / "board-source"
    marker = write(board / "board.md", "# Board")
    source = register(tmp_path / "ordinary")
    calls = []

    def run(cmd, **kwargs):
        calls.append((cmd, kwargs))
        return SimpleNamespace(returncode=0, stdout="built\n", stderr="")

    monkeypatch.setattr("live.base.subprocess.run", run)
    server = handler(tmp_path)
    for target in (board, marker):
        assert server.rebuild(target) == "built"
        assert calls[-1][0] == [sys.executable, str(ENGINE / "cli/build.py"), str(board)]
    for target in (source, source.parent):
        assert server.rebuild(target) == "built"
        assert calls[-1][0] == [sys.executable, str(PAGE / "cli/page.py"), "build", str(target)]
        assert calls[-1][1]["cwd"] == str(source.parent)
    monkeypatch.setattr("live.base.subprocess.run", lambda *a, **kw:
                        SimpleNamespace(returncode=7, stdout="partial", stderr="failure detail"))
    with pytest.raises(RuntimeError, match=r"exit 7.*partial\nfailure detail"):
        server.rebuild(source)
