"""Validate Design Studio content and bindings to the existing mindmap renderer.

Maps are authored .mindmap.md files: this checker never regenerates them or a human's
canvas. Folder and historical drawing artifacts keep their existing paths.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlsplit

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "PRINCIPLE.md").is_file())
BLOCK = Path(__file__).resolve().parent.parent
TOPICS = {"s01-design": ("Design Board", "Design-Example"),
          "s02-workbench-ui": ("Design Method Book", "DesignMethodBook-Example")}
VIEWS = ["Structure", "Draw", "Examples", "Skills"]


def check():
    sys.path.insert(0, str(ROOT / "plugins/haipipe-toolkit/servers/_host"))
    from host_paths import bootstrap
    bootstrap()
    from live import frame, studio_views
    mm = frame.mindmap_module()
    import mmtree
    import mapview
    for slug, (title, example) in TOPICS.items():
        topic = BLOCK / slug
        book = slug == "s02-workbench-ui"
        manifest = json.loads((topic / "studio-views.json").read_text())
        assert [v["name"] for v in manifest["views"]] == VIEWS
        structure = manifest["views"][0]["items"]
        assert [i["name"] for i in structure] == ["Jobs / Tasks", "Folder", "Studio"]
        assert manifest["views"][1]["items"][0] == structure[0]
        assert structure[0]["fragment"] == "organization"
        assert structure[2]["fragment"] == "studio"
        examples = manifest["views"][2]["items"]
        assert examples[0]["fragment"] == "example"
        assert examples[1] == {"name": "Example 1", "block": f"examples/Project-Ladder/design/{example}"}
        for name in ("organization", "example", "studio"):
            path = topic / "delivery" / f"{name}.mindmap.md"
            tree = mmtree.load(path)
            nodes = [n for n, *_ in mmtree.walk(tree.root)]
            assert len({n.id for n in nodes}) == len(nodes)
            assert tree.meta.get("written")
            for n in nodes:
                for _label, target in mm.LINK.findall(n.text + " " + " ".join(n.note)):
                    resolved = (path.parent / target).resolve()
                    assert resolved.is_relative_to(ROOT) and resolved.is_file(), target
            if name != "studio":
                roles = [mm.split_role(n.text)[0] for n in nodes]
                if book:
                    assert set(roles) == {"", "Job Type", "Job Name"}
                    assert all(not n.children for n in nodes if mm.split_role(n.text)[0] == "Job Name")
                else:
                    assert roles.count("Job Type") == 1 and roles.count("Job Name") == 1
                    assert roles.count("Task Type") == 3
                    assert roles.count("Task Name") == (4 if name == "example" else 3)
                if name == "example":
                    text = path.read_text()
                    expected = ("M01 · goal only", "M02 · overall performance") if book else (
                        "Confirm by reply, by Overall performance", "reason ideas", "reply-first-short",
                        "reminder-one-ask", "review whole")
                    assert all(word in text for word in expected)
            html = mm.fragment(path, str(path.relative_to(ROOT)), editable=False,
                               url_of=lambda p: frame._file_url(p, ROOT))
            assert mapview.CSS in html and mapview.JS.replace(' contenteditable=plaintext-only', '') in html
            assert 'pm-folds' in html and 'data-foldall=0' in html
            assert 'contenteditable=plaintext-only' not in html
        rendered, parts = studio_views.read_views(topic, ROOT)
        assert [v[0] for v in rendered] == VIEWS
        for view, i in (("Structure", 0), ("Structure", 2), ("Draw", 0), ("Examples", 0)):
            item = next(v for v in manifest["views"] if v["name"] == view)["items"][i]
            assert item["path"].endswith("/delivery/mindmap.html")
            bridge = (ROOT / item["path"]).read_text()
            targets = json.loads(re.search(r"const maps = (.*);", bridge)[1])
            query = parse_qs(urlsplit(targets[item["fragment"]]).query)
            assert query.get("view") == ["focus-map"] and query.get("fit") == ["1"]
            assert query.get("path") == [str((topic / "delivery" / (item["fragment"] + ".mindmap.md")).relative_to(ROOT))]
            assert 'location.replace(maps[key] || maps.organization)' in bridge
            assert '<svg' not in bridge and '<style' not in bridge, "Bridge must not render a second map"
        assert parts["Draw"][-1][1].startswith("/_excalidraw/?board=")
        for view in manifest["views"]:
            for item in view["items"]:
                path = item.get("block", item.get("path"))
                assert path and not Path(path).is_absolute() and ":" not in path
                target = (ROOT / path).resolve()
                assert target.is_relative_to(ROOT) and target.exists(), path
                assert (target / "board.md").is_file() if "block" in item else target.is_file()
        source = json.loads((topic / "delivery/structure.excalidraw").read_text())
        ids = [e["id"] for e in source["elements"]]
        assert len(set(ids)) == len(ids), slug
        labels = [e.get("text", "") for e in source["elements"] if not e.get("isDeleted")]
        for field in ("Job Type", "Job Name", "Task Type", "Task Name"):
            assert field in labels, (slug, field)
            assert field in (topic / "delivery/structure.md").read_text(), (slug, field)
        assert not any(label in labels for label in ("Job 1", "Task 1", "Job topic 1", "Task topic 1"))
        if slug == "s02-workbench-ui":
            assert "No Task layer" in labels
            for mid, name, version in (("M01", "goal only", "m2"), ("M02", "overall performance", "m1")):
                job = next((ROOT / "examples/Project-Ladder/design" / example).glob(f"j*_{mid}-*"))
                face = (job / f"{job.name}.md").read_text()
                assert f"title: {name}" in face and (job / f"{version}.md").is_file()
                assert f"{mid} · {name}" in labels
                assert not list(job.glob("t[0-9][0-9]*")), "Book has acquired Tasks: revisit the contract"
        else:
            for label in ("Design execution", "Reason ideas", "Design", "Review whole"):
                assert label in labels
            for i in (0, 1):
                assert f"design-name-{i}" in ids and f"design-name-edge-{i}" in ids
            job = ROOT / "examples/Project-Ladder/design/Design-Example/j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2"
            assert "# Confirm by reply, by Overall performance" in (job / f"{job.name}.md").read_text()
            for folder, name in (("t01_d01_reply-first-short", "reply-first-short"),
                                 ("t02_d02_reminder-one-ask", "reminder-one-ask")):
                assert f"name: {name}" in (job / folder / f"{folder}.md").read_text()
                assert any(name in label for label in labels)
            assert (job / "t00_reason-ideas").is_dir() and (job / "t99_review-whole").is_dir()
        from PIL import Image
        with Image.open(topic / "delivery/structure.png") as pic:
            pic.verify()
        assert title in (topic / f"{slug}.md").read_text().splitlines()[0]
        assert (topic / f"{slug}.excalidraw").is_file(), "historical canvas missing"
    assert (BLOCK / "s02-workbench-ui/design-workbench-ui.excalidraw").is_file()
    print("Both Design Studios: native mindmaps, source links, names and shared bindings pass.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate only; authored maps are never overwritten")
    parser.parse_args()
    check()
