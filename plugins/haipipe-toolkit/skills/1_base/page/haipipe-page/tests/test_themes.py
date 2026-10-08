"""The Theme table: singular Theme folders, and the old plural ones read as aliases (b03 s01-D28, D29)."""
from pathlib import Path

from src.common import mounted_folder_kind
from src.themes import folder_names, kind_of, theme_dir, theme_dirs


def test_every_theme_has_a_singular_folder_and_reads_its_old_name():
    assert kind_of("work") == kind_of("tasks") == "task"
    assert kind_of("discovery") == kind_of("discoveries") == "discovery"
    assert kind_of("paper") == kind_of("papers") == "paper"
    assert kind_of("labeling") == kind_of("labelings") == "labeling"
    assert kind_of("cowork") == "cowork" and kind_of("Tasks") == "" and kind_of("runs") == ""
    assert folder_names("task") == ("work", "tasks") and folder_names("cowork") == ("cowork",)


def test_the_new_folder_wins_and_an_old_layout_still_resolves(tmp_path):
    old, new, both = tmp_path / "old", tmp_path / "new", tmp_path / "both"
    (old / "tasks").mkdir(parents=True)
    (new / "work").mkdir(parents=True)
    (both / "work").mkdir(parents=True)
    (both / "tasks").mkdir()
    assert theme_dir(old, "task") == old / "tasks"
    assert theme_dir(new, "task") == new / "work"
    assert theme_dirs(both, "task") == [both / "work", both / "tasks"]
    assert theme_dir(tmp_path / "empty", "discovery") == tmp_path / "empty" / "discovery"


def _task_page(project: Path, theme: str) -> Path:
    page = project / theme / "b01_x" / "j01_y" / "t01_z" / "t01_z.md"
    page.parent.mkdir(parents=True)
    page.write_text("# t01 z\n", encoding="utf-8")
    return page


def test_a_task_page_reads_its_kind_from_either_theme_folder(tmp_path):
    assert mounted_folder_kind(_task_page(tmp_path / "a", "tasks")) == "task"
    assert mounted_folder_kind(_task_page(tmp_path / "b", "work")) == "task"
    assert mounted_folder_kind(_task_page(tmp_path / "c", "discoveries")) == "discovery"
    assert mounted_folder_kind(_task_page(tmp_path / "d", "discovery")) == "discovery"
