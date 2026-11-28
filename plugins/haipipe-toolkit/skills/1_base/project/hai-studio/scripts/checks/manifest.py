"""Check actual bindings before asking any generator to read them."""
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from checks.paths import owner, contained
from checks.results import Result

LIVE = "/_board/workbench?"   # a live workbench page as an item (studio_views.py: "url"), its path= inside the SPACE


def read(topic: Path, root: Path) -> tuple[dict | None, list[Result]]:
    path = topic / "studio-views.json"
    errors = []
    if not path.resolve().is_relative_to(root.resolve()):
        return None, [Result("FAIL", "bindings", path, "manifest leaves the SPACE")]

    def fail(detail):
        errors.append(Result("FAIL", "bindings", path, detail))

    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        return None, [Result("FAIL", "bindings", path, f"cannot read manifest: {error}")]
    if not isinstance(data, dict) or not isinstance(data.get("views"), list) or not data["views"]:
        return None, [Result("FAIL", "bindings", path, "views must be a nonempty list")]
    names = set()
    for view in data["views"]:
        if not isinstance(view, dict) or not isinstance(view.get("name"), str) or not view["name"]:
            fail("each view needs a nonempty name")
            continue
        if view["name"] in names:
            fail(f"duplicate view: {view['name']}")
        names.add(view["name"])
        items = view.get("items")
        if not isinstance(items, list) or not items:
            fail(f"{view['name']}: items must be a nonempty list")
            continue
        item_names = set()
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"]:
                fail(f"{view['name']}: each item needs a nonempty name")
                continue
            if item["name"] in item_names:
                fail(f"{view['name']}: duplicate item {item['name']}")
            item_names.add(item["name"])
            fields = [key for key in ("path", "folder", "block", "url") if key in item]
            if len(fields) != 1:
                fail(f"{view['name']}/{item['name']}: expected one path, folder, block or url binding")
                continue
            key = fields[0]
            try:
                if key == "url":
                    if not isinstance(item[key], str) or not item[key].startswith(LIVE):
                        raise ValueError(f"url must start with {LIVE}")
                    source = contained(root, (parse_qs(urlsplit(item[key]).query).get("path") or [""])[0].lstrip("/"))
                    if not source.exists():
                        fail(f"{view['name']}/{item['name']}: missing page {source.relative_to(root.resolve())}; fix the url")
                    continue
                source = contained(root, item[key])
                valid = source.is_file() if key == "path" else source.is_dir()
                if key == "block":
                    valid = valid and (source / "board.md").is_file()
                if not valid:
                    fail(f"{view['name']}/{item['name']}: missing {key} {item[key]}; fix the source binding")
            except ValueError as error:
                fail(f"{view['name']}/{item['name']}: {error}")
    if "Check" in names and not data.get("check_type"):
        fail("Check needs check_type; bind its owning type rather than a copied checklist")
    if "check_type" in data:
        try:                                         # a type's name, or a SPACE-relative type topic
            owner("check_views").owned(root, data["check_type"])
        except ValueError as error:
            fail(f"check_type: {error}")
    return (None, errors) if errors else (data, [Result("PASS", "bindings", path, "source bindings exist")])
