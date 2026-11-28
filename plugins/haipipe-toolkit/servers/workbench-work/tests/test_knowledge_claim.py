"""The work theme claims a Block by what its face names, wherever it sits (work_theme.claims): a Work Block (Knowledge) in
knowledge/, a folder no theme owns by name, still opens as a work page, with the Studio's bands and folds (hai-ui A11)
and every section's emoji (hai-ui A12)."""
import re
import tempfile
from pathlib import Path

from live import frame, focus_page
from live.frame_base import theme_of
from live.section_icons import SECTION_ICONS
from live import work_theme

ROOT = Path(__file__).resolve().parents[5]                  # the SPACE: plugins/haipipe-toolkit/servers/workbench-work/tests
B18 = ROOT / "examples/Project-Ladder/knowledge/b18_a2ui_learning"


def test_claims_a_block_whose_face_names_work():
    with tempfile.TemporaryDirectory() as tmp:
        for face, want in (("theme: work\n", True), ("workbench: work\n", True), ("board-kind: prototype\n", True),
                           ("theme: paper\n", False), ("workbench: workbench-work\n", False), ("", False)):
            block = Path(tmp) / f"b{abs(hash(face)) % 1000}"
            block.mkdir()
            (block / "board.md").write_text("# b01 · A Block\n\n" + face)
            assert work_theme.claims(block) is want, face
        assert work_theme.claims(Path(tmp) / "no-face") is False


def test_knowledge_example_block_reads_as_work():
    assert theme_of(B18, ROOT) == "work"


def test_knowledge_studio_has_bands_folds_and_emojis():
    html = focus_page.render(frame.themes()["work"], ROOT, B18, "studio")
    assert 'class="studio-band"' in html                     # the bands, each with its topics' folds
    assert html.count("<details") >= 4
    menu = html.split('id="side-menu"', 1)[1].split("</div>", 1)[0]
    labels = [re.sub(r"<[^>]+>", "", m).strip() for m in re.findall(r'role="menuitem"[^>]*>(.*?)</button>', menu)]
    labels = [label for label in labels if label and not label.startswith("✕")]
    assert labels
    for label in labels:
        assert label.split(" ", 1)[0] in SECTION_ICONS.values() or label.startswith("<svg") or "Files" in label, label


def test_knowledge_block_names_its_type_and_use_case():
    html = focus_page.render(frame.themes()["work"], ROOT, B18, "studio")
    identity = html.split('class="job-identity"', 1)[1].split("</dl>", 1)[0]
    assert "📚 Work Block (Knowledge)" in identity and "🎓 Learn new concepts" in identity


def test_each_work_block_type_reads_from_its_folder():
    """A work-family Block's type is its Project folder, whichever theme draws its page; UI example config on a
    work/ Block does not make it a Blueprint."""
    from live.focus_base import read_face
    from live.focus_identity import page_identity_html
    ladder = ROOT / "examples/Project-Ladder"
    for rel, want in (("work/b01_example_work", "🧩 Work Block (Work)"),
                      ("blueprint/b17_theme_work", "📐 Work Block (Blueprint)"),
                      ("cowork/b01_example_cowork", "🤝 Work Block (CoWork)"),
                      ("discovery/b01_example_discovery", "🔎 Work Block (Discovery)"),
                      ("knowledge/b18_a2ui_learning", "📚 Work Block (Knowledge)")):
        block = ladder / rel
        theme = theme_of(block, ROOT)
        theme = theme if theme in frame.themes() else "vanilla"   # cowork and discovery draw on the plain page
        assert want in page_identity_html(theme, block, ROOT, read_face(block, ROOT)), rel
