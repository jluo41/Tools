#!/usr/bin/env python3
"""Split and recompose a Board Excalidraw scene as linked Group/Page sources.

The legacy scene stays untouched. ``split`` writes only new lowercase ``draw/``
directories beside each Page group. A Group scene owns its own elements and an
import manifest; every Page scene remains an ordinary, independently editable
Excalidraw file.

    python3 cli/draw.py split <board>             # read-only plan
    python3 cli/draw.py split <board> --apply     # create new draw/ sources
    python3 cli/draw.py compose <board> --output /tmp/board.excalidraw
    python3 cli/draw.py verify <board>

The compose command namespaces element references in its output, so duplicate
IDs in independently edited Page scenes cannot collide. ``verify`` deliberately
uses original IDs and source-order provenance to prove that the first split can
reconstruct the legacy scene exactly.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from src.body import LINKS  # noqa: E402
from src.parse import parse_dir  # noqa: E402


SCHEMA = "haipipe-linked-drawing/v1"
ID_REF_KEYS = {"frameId", "containerId", "elementId"}


class DrawError(RuntimeError):
    """An input scene cannot be split or composed without guessing."""


def read_scene(path: Path) -> dict:
    try:
        scene = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DrawError(f"scene does not exist: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise DrawError(f"cannot read Excalidraw scene {path}: {exc}") from exc
    if scene.get("type") != "excalidraw" or not isinstance(scene.get("elements"), list):
        raise DrawError(f"not an Excalidraw scene: {path}")
    return scene


def scene_text(scene: dict) -> str:
    return json.dumps(scene, indent=2, ensure_ascii=False) + "\n"


def write_scene(path: Path, scene: dict) -> None:
    path.write_text(scene_text(scene), encoding="utf-8")


def write_scene_atomic(path: Path, scene: dict) -> None:
    """Replace one existing scene without exposing a partial JSON file."""
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(scene_text(scene))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def write_scene_exclusive(path: Path, scene: dict) -> None:
    """Create one scene without a check/write race or a partial file."""
    descriptor = None
    created_here = False
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        created_here = True
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = None
            handle.write(scene_text(scene))
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        if descriptor is not None:
            os.close(descriptor)
        if created_here:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        raise


def group_id(label: str) -> str:
    token = label.split("·", 1)[0].strip()
    if not re.fullmatch(r"[A-Za-z0-9-]+", token):
        raise DrawError(f"group has no filesystem-safe id: {label!r}")
    return token


def board_inventory(board: Path):
    meta, pages, _ = parse_dir(board)
    pages = [page for page in pages if page.get("file")]
    by_id = {page["id"]: page for page in pages}
    by_file = {Path(page["file"]).as_posix(): page for page in pages}
    groups: dict[str, dict] = {}
    for page in pages:
        label = page.get("group") or "Ungrouped"
        gid = group_id(label)
        parent = Path(page["file"]).parent
        entry = groups.setdefault(gid, {"id": gid, "label": label, "parent": parent, "pages": []})
        if entry["label"] != label or entry["parent"] != parent:
            raise DrawError(f"group {gid} spans more than one label or folder")
        entry["pages"].append(page)

    aliases = {}
    for alias, target in LINKS.items():
        normalized = Path(target).as_posix()
        if normalized in by_file:
            aliases[alias] = by_file[normalized]
    return meta, pages, by_id, groups, aliases


def page_files(scene: dict, elements: list[dict]) -> dict:
    wanted = {element.get("fileId") for element in elements if element.get("fileId")}
    return {key: value for key, value in scene.get("files", {}).items() if key in wanted}


def translated(element: dict, dx: float, dy: float) -> dict:
    out = copy.deepcopy(element)
    if isinstance(out.get("x"), (int, float)):
        out["x"] += dx
    if isinstance(out.get("y"), (int, float)):
        out["y"] += dy
    return out


def transformed(element: dict, placement: dict) -> dict:
    """Apply a Group-owned portal transform while leaving the Page source local."""
    scale = placement.get("scale", 1)
    if not isinstance(scale, (int, float)) or scale <= 0:
        raise DrawError(f"invalid import scale: {scale!r}")
    dx, dy = placement.get("x", 0), placement.get("y", 0)
    if not all(isinstance(value, (int, float)) for value in (dx, dy)):
        raise DrawError(f"invalid import placement: x={dx!r}, y={dy!r}")
    if scale == 1:
        return translated(element, dx, dy)
    out = copy.deepcopy(element)
    for key in ("x", "y"):
        if isinstance(out.get(key), (int, float)):
            out[key] = out[key] * scale + (dx if key == "x" else dy)
    for key in ("width", "height", "fontSize", "strokeWidth"):
        if isinstance(out.get(key), (int, float)):
            out[key] *= scale
    if isinstance(out.get("points"), list):
        out["points"] = [
            [value * scale if isinstance(value, (int, float)) else value for value in point]
            if isinstance(point, list) else point
            for point in out["points"]
        ]
    for key in ("startBinding", "endBinding"):
        binding = out.get(key)
        if isinstance(binding, dict) and isinstance(binding.get("gap"), (int, float)):
            binding["gap"] *= scale
    roundness = out.get("roundness")
    if isinstance(roundness, dict) and isinstance(roundness.get("value"), (int, float)):
        roundness["value"] *= scale
    return out


def namespace_refs(
    value,
    owner: str,
    key: str | None = None,
    reference_owners: dict[str, str] | None = None,
    ambiguous_refs: set[str] | None = None,
):
    def ref(raw: str) -> str:
        if ambiguous_refs and raw in ambiguous_refs:
            raise DrawError(f"Group binding points at ambiguous imported id: {raw}")
        target_owner = (reference_owners or {}).get(raw, owner)
        return f"{target_owner}::{raw}"

    if isinstance(value, dict):
        out = {}
        for child_key, child in value.items():
            if child_key in ID_REF_KEYS and isinstance(child, str):
                out[child_key] = ref(child)
            elif child_key == "id" and key == "boundElements" and isinstance(child, str):
                out[child_key] = ref(child)
            elif child_key == "groupIds" and isinstance(child, list):
                out[child_key] = [f"{owner}::{item}" for item in child]
            else:
                out[child_key] = namespace_refs(
                    child, owner, child_key, reference_owners, ambiguous_refs
                )
        return out
    if isinstance(value, list):
        return [
            namespace_refs(item, owner, key, reference_owners, ambiguous_refs)
            for item in value
        ]
    return value


def namespace_element(
    element: dict,
    owner: str,
    reference_owners: dict[str, str] | None = None,
    ambiguous_refs: set[str] | None = None,
) -> dict:
    out = namespace_refs(element, owner, reference_owners=reference_owners,
                         ambiguous_refs=ambiguous_refs)
    out["id"] = f"{owner}::{element['id']}"
    return out


def runtime_element(element: dict, owner: str, kind: str) -> dict:
    """Mark a derived element so the live saver can route it to one owner."""
    out = copy.deepcopy(element)
    custom = copy.deepcopy(out.get("customData") or {})
    custom["haipipeRuntime"] = {
        "owner": owner,
        "kind": kind,
        "sourceId": element["id"],
    }
    out["customData"] = custom
    return out


def binding_ids(element: dict) -> set[str]:
    refs = set()
    for key in ("startBinding", "endBinding"):
        binding = element.get(key)
        if isinstance(binding, dict) and isinstance(binding.get("elementId"), str):
            refs.add(binding["elementId"])
    return refs


def reference_ids(value, key: str | None = None) -> set[str]:
    """Every element-id reference that the compositor is responsible for."""
    refs = set()
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key in ID_REF_KEYS and isinstance(child, str):
                refs.add(child)
            elif child_key == "id" and key == "boundElements" and isinstance(child, str):
                refs.add(child)
            else:
                refs.update(reference_ids(child, child_key))
    elif isinstance(value, list):
        for child in value:
            refs.update(reference_ids(child, key))
    return refs


def scene_shell(source: dict, elements: list[dict], files: dict, extension: dict) -> dict:
    return {
        "type": "excalidraw",
        "version": source.get("version", 2),
        "source": "haipipe-board/draw.py",
        "elements": elements,
        "appState": copy.deepcopy(source.get("appState", {})),
        "files": files,
        "haipipe": extension,
    }


def split_plan(board: Path, source_path: Path):
    source = read_scene(source_path)
    _, pages, by_id, groups, aliases = board_inventory(board)
    elements = source["elements"]
    positions = {element["id"]: index for index, element in enumerate(elements)}
    frames = {element["id"]: element for element in elements if element.get("type") == "frame"}

    page_frame: dict[str, dict] = {}
    frame_group: dict[str, str] = {}
    frame_page: dict[str, str] = {}
    for frame in frames.values():
        name = str(frame.get("name") or "").strip()
        page = by_id.get(name) or aliases.get(name)
        if not page:
            raise DrawError(f"frame {frame['id']} names unknown Page {name!r}")
        if page["id"] in page_frame:
            raise DrawError(f"Page {page['id']} has more than one frame")
        page_frame[page["id"]] = frame
        frame_group[frame["id"]] = group_id(page.get("group") or "Ungrouped")
        frame_page[frame["id"]] = page["id"]

    known_frames = set(frames)
    for element in elements:
        frame_id = element.get("frameId")
        if frame_id and frame_id not in known_frames:
            raise DrawError(f"element {element['id']} points at missing frame {frame_id}")

    element_group = dict(frame_group)
    element_page = dict(frame_page)
    for element in elements:
        if element.get("frameId"):
            element_group[element["id"]] = frame_group[element["frameId"]]
            element_page[element["id"]] = frame_page[element["frameId"]]

    all_ids = set(positions)
    for element in elements:
        unresolved = reference_ids(element) - all_ids
        if unresolved:
            raise DrawError(
                f"element {element['id']} has unresolved reference(s): "
                f"{', '.join(sorted(unresolved))}"
            )
        page_id = element_page.get(element["id"])
        if page_id:
            outside = {
                ref for ref in binding_ids(element)
                if element_page.get(ref) != page_id
            }
            if outside:
                raise DrawError(
                    f"Page element {element['id']} binds outside {page_id}: "
                    f"{', '.join(sorted(outside))}"
                )

    group_owner = {}
    labels = {entry["label"]: gid for gid, entry in groups.items()}
    pending = []
    for element in elements:
        if element.get("type") == "frame" or element.get("frameId"):
            continue
        text = element.get("text")
        explicit = element.get("customData", {}).get("haipipeOwner")
        if text in labels:
            group_owner[element["id"]] = labels[text]
        elif explicit:
            if explicit not in groups:
                raise DrawError(f"element {element['id']} names unknown Group owner {explicit!r}")
            group_owner[element["id"]] = explicit
        else:
            pending.append(element)

    element_group.update(group_owner)
    while pending:
        deferred, changed = [], False
        for element in pending:
            refs = binding_ids(element)
            if refs and refs <= element_group.keys():
                owners = {element_group[ref] for ref in refs}
                if len(owners) == 1:
                    owner = owners.pop()
                    group_owner[element["id"]] = owner
                    element_group[element["id"]] = owner
                    changed = True
                    continue
                raise DrawError(
                    f"unframed element {element['id']} binds across Groups: "
                    f"{', '.join(sorted(owners))}"
                )
            deferred.append(element)
        if not changed:
            element = deferred[0]
            raise DrawError(
                f"unframed element {element['id']} has no unambiguous Group owner; "
                "bind it within one Group or set customData.haipipeOwner"
            )
        pending = deferred

    for element in elements:
        owner = group_owner.get(element["id"])
        if not owner:
            continue
        endpoint_owners = {element_group[ref] for ref in binding_ids(element)}
        if endpoint_owners and endpoint_owners != {owner}:
            raise DrawError(
                f"Group element {element['id']} owned by {owner} binds across Groups: "
                f"{', '.join(sorted(endpoint_owners))}"
            )

    outputs = []
    for gid, group in groups.items():
        draw_dir = board / group["parent"] / "draw"
        own = [copy.deepcopy(element) for element in elements if group_owner.get(element["id"]) == gid]
        imports = []
        page_scenes = []
        for page in group["pages"]:
            frame = page_frame.get(page["id"])
            if frame:
                selected = [frame] + [
                    element for element in elements if element.get("frameId") == frame["id"]
                ]
                selected.sort(key=lambda element: positions[element["id"]])
                origin = {"x": frame.get("x", 0), "y": frame.get("y", 0)}
                local = [translated(element, -origin["x"], -origin["y"]) for element in selected]
            else:
                selected, local = [], []
                origin = {"x": 0, "y": 0}
            page_extension = {
                "schema": SCHEMA,
                "kind": "page",
                "page": {"id": page["id"], "markdown": page["file"]},
                "migration": {
                    "source": os.path.relpath(source_path, draw_dir),
                    "origin": origin,
                    "sourceIndexes": {element["id"]: positions[element["id"]] for element in selected},
                },
            }
            page_scene = scene_shell(source, local, page_files(source, selected), page_extension)
            page_name = f"{page['id']}.excalidraw"
            page_scenes.append((draw_dir / page_name, page_scene))
            imports.append({
                "page": page["id"],
                "source": page_name,
                "placement": {"x": origin["x"], "y": origin["y"], "scale": 1},
                "sourceFrame": frame["id"] if frame else None,
            })

        group_extension = {
            "schema": SCHEMA,
            "kind": "group",
            "group": {"id": gid, "name": group["label"]},
            "imports": imports,
            "migration": {
                "source": os.path.relpath(source_path, draw_dir),
                "sourceIndexes": {element["id"]: positions[element["id"]] for element in own},
            },
        }
        group_scene = scene_shell(source, own, page_files(source, own), group_extension)
        outputs.append((draw_dir / "group.excalidraw", group_scene))
        outputs.extend(page_scenes)
    return source, pages, groups, outputs


def split(board: Path, source_path: Path, apply: bool) -> int:
    source, pages, groups, outputs = split_plan(board, source_path)
    existing = [path for path, _ in outputs if path.exists()]
    if existing:
        sample = ", ".join(str(path.relative_to(board)) for path in existing[:4])
        raise DrawError(f"refusing to overwrite {len(existing)} linked source(s): {sample}")
    print(f"source: {source_path.relative_to(board)} · {len(source['elements'])} elements")
    print(f"plan  : {len(groups)} group draw/ folders · {len(pages)} Page sources")
    if not apply:
        print("dry run; add --apply to create the new lowercase draw/ sources")
        return 0
    created = []
    created_dirs = []
    try:
        for path, scene in outputs:
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=False)
                created_dirs.append(path.parent)
            write_scene_exclusive(path, scene)
            created.append(path)
    except Exception as exc:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise DrawError(f"split rolled back after write failure: {exc}") from exc
    print(f"wrote : {len(outputs)} new scenes; legacy source unchanged")
    return 0


def linked_group_paths(board: Path) -> list[Path]:
    _, _, _, groups, _ = board_inventory(board)
    return [board / group["parent"] / "draw" / "group.excalidraw" for group in groups.values()]


def sync_plan(board: Path):
    """Plan additive Page-source updates after board.md gains new Pages.

    Existing imports and sources are never rewritten or removed. A stale import
    that no longer belongs to the Board stops the operation for a human ruling.
    """
    _, _, _, groups, _ = board_inventory(board)
    plans = []
    for gid, group in groups.items():
        group_path = board / group["parent"] / "draw" / "group.excalidraw"
        group_scene = read_scene(group_path)
        ext = group_scene.get("haipipe", {})
        if ext.get("schema") != SCHEMA or ext.get("kind") != "group":
            raise DrawError(f"not a linked Group source: {group_path}")
        imports = ext.get("imports")
        if not isinstance(imports, list):
            raise DrawError(f"Group {gid} has no import manifest")
        by_page = {item.get("page"): item for item in imports}
        expected = [page["id"] for page in group["pages"]]
        stale = [page for page in by_page if page not in expected]
        if stale:
            raise DrawError(f"Group {gid} has stale imports: {', '.join(stale)}")
        missing = [page for page in group["pages"] if page["id"] not in by_page]
        if not missing:
            continue
        additions = []
        for page in missing:
            page_name = f"{page['id']}.excalidraw"
            page_path = group_path.parent / page_name
            if page_path.exists():
                raise DrawError(
                    f"refusing to adopt unmanifested Page source: {page_path}"
                )
            page_ext = {
                "schema": SCHEMA,
                "kind": "page",
                "page": {"id": page["id"], "markdown": page["file"]},
                "migration": {"sourceIndexes": {}},
            }
            page_scene = scene_shell(group_scene, [], {}, page_ext)
            additions.append((page_path, page_scene))
            by_page[page["id"]] = {
                "page": page["id"],
                "source": page_name,
                "placement": {"x": 0, "y": 0, "scale": 1, "visible": True},
                "sourceFrame": None,
            }
        updated = copy.deepcopy(group_scene)
        updated["haipipe"]["imports"] = [by_page[page] for page in expected]
        plans.append((group_path, group_scene, updated, additions))
    return plans


def sync(board: Path, apply: bool) -> int:
    plans = sync_plan(board)
    count = sum(len(additions) for _, _, _, additions in plans)
    print(f"plan  : {count} new Page source(s) across {len(plans)} Group manifest(s)")
    if not apply:
        print("dry run; add --apply to add only the missing linked sources")
        return 0
    created = []
    replaced = []
    try:
        for group_path, original, updated, additions in plans:
            original_bytes = group_path.read_bytes()
            for page_path, page_scene in additions:
                write_scene_exclusive(page_path, page_scene)
                created.append(page_path)
            if group_path.read_bytes() != original_bytes:
                raise DrawError(f"Group source changed during sync: {group_path}")
            write_scene_atomic(group_path, updated)
            replaced.append((group_path, original))
    except Exception as exc:
        for group_path, original in reversed(replaced):
            write_scene_atomic(group_path, original)
        for page_path in reversed(created):
            page_path.unlink(missing_ok=True)
        raise DrawError(f"sync rolled back after write failure: {exc}") from exc
    print(f"wrote : {count} new Page source(s); updated {len(plans)} manifest(s)")
    return 0


def merge_files(target: dict, incoming: dict, owner: str) -> None:
    for file_id, value in incoming.items():
        if file_id in target and target[file_id] != value:
            raise DrawError(f"file id {file_id} collides while composing {owner}")
        target[file_id] = copy.deepcopy(value)


def compose_group_data(group_path: Path, namespace: bool = True, runtime: bool = False) -> dict:
    """Compose one Group source with its Page imports for the live canvas."""
    group_scene = read_scene(group_path)
    ext = group_scene.get("haipipe", {})
    if ext.get("schema") != SCHEMA or ext.get("kind") != "group":
        raise DrawError(f"not a linked Group source: {group_path}")
    gid = ext.get("group", {}).get("id")
    if not gid:
        raise DrawError(f"Group source has no owner id: {group_path}")

    ordered, appended, files = [], [], {}
    migration = ext.get("migration", {}).get("sourceIndexes", {})
    merge_files(files, group_scene.get("files", {}), gid)
    loaded_pages = []
    reference_owners = {element["id"]: gid for element in group_scene["elements"]}
    ambiguous_refs = set()
    for item in ext.get("imports", []):
        page_id = item.get("page")
        source = item.get("source")
        if not page_id or not source:
            raise DrawError(f"Group {gid} has an incomplete import")
        page_path = group_path.parent / source
        page_scene = read_scene(page_path)
        page_ext = page_scene.get("haipipe", {})
        if page_ext.get("schema") != SCHEMA or page_ext.get("kind") != "page":
            raise DrawError(f"not a linked Page source: {page_path}")
        if page_ext.get("page", {}).get("id") != page_id:
            raise DrawError(f"import {page_id} points at a different Page source: {page_path}")
        loaded_pages.append((item, page_scene, page_ext.get("migration", {}).get("sourceIndexes", {})))
        for element in page_scene["elements"]:
            raw_id = element["id"]
            if raw_id in reference_owners and reference_owners[raw_id] != page_id:
                ambiguous_refs.add(raw_id)
            else:
                reference_owners[raw_id] = page_id

    for element in group_scene["elements"]:
        source = runtime_element(element, gid, "group") if runtime else element
        out = (
            namespace_element(source, gid, reference_owners, ambiguous_refs)
            if namespace else copy.deepcopy(source)
        )
        index = migration.get(element["id"])
        (ordered if index is not None else appended).append((index, out))

    for item, page_scene, indexes in loaded_pages:
        page_id = item["page"]
        placement = item.get("placement", {})
        if placement.get("visible", True) is False:
            continue
        local_ids = {element["id"] for element in page_scene["elements"]}
        page_reference_owners = dict(reference_owners)
        page_reference_owners.update({raw_id: page_id for raw_id in local_ids})
        page_ambiguous_refs = ambiguous_refs - local_ids
        for element in page_scene["elements"]:
            moved = transformed(element, placement)
            source = runtime_element(moved, page_id, "page") if runtime else moved
            out = (
                namespace_element(source, page_id, page_reference_owners, page_ambiguous_refs)
                if namespace else source
            )
            if runtime:
                out["locked"] = True
                out["groupIds"] = [f"portal::{page_id}"] + list(out.get("groupIds") or [])
            index = indexes.get(element["id"])
            (ordered if index is not None else appended).append((index, out))
        merge_files(files, page_scene.get("files", {}), page_id)

    ordered.sort(key=lambda pair: pair[0])
    elements = [element for _, element in ordered]
    elements.extend(element for _, element in appended)
    scene = {
        "type": "excalidraw",
        "version": group_scene.get("version", 2),
        "source": "haipipe-board/draw.py composed Group",
        "elements": elements,
        "appState": copy.deepcopy(group_scene.get("appState", {})),
        "files": files,
        "haipipe": {
            "schema": SCHEMA,
            "kind": "composed-group",
            "group": copy.deepcopy(ext["group"]),
            "imports": copy.deepcopy(ext.get("imports", [])),
        },
    }
    return scene


def compose_data(board: Path, namespace: bool = True) -> dict:
    ordered, appended, files, app_state = [], [], {}, None
    seen_ids = set()
    _, _, _, inventory_groups, _ = board_inventory(board)
    for group_path in linked_group_paths(board):
        group_scene = read_scene(group_path)
        ext = group_scene.get("haipipe", {})
        if ext.get("schema") != SCHEMA or ext.get("kind") != "group":
            raise DrawError(f"not a linked Group source: {group_path}")
        gid = ext["group"]["id"]
        expected_pages = [page["id"] for page in inventory_groups[gid]["pages"]]
        imported_pages = [item.get("page") for item in ext.get("imports", [])]
        if imported_pages != expected_pages:
            raise DrawError(
                f"Group {gid} imports do not match board.md: "
                f"expected {expected_pages}, found {imported_pages}"
            )
        migration = ext.get("migration", {}).get("sourceIndexes", {})
        merge_files(files, group_scene.get("files", {}), gid)
        app_state = app_state or copy.deepcopy(group_scene.get("appState", {}))

        loaded_pages = []
        reference_owners = {element["id"]: gid for element in group_scene["elements"]}
        ambiguous_refs = set()
        for item in ext.get("imports", []):
            page_id = item["page"]
            page_path = group_path.parent / item["source"]
            page_scene = read_scene(page_path)
            page_ext = page_scene.get("haipipe", {})
            if page_ext.get("schema") != SCHEMA or page_ext.get("kind") != "page":
                raise DrawError(f"not a linked Page source: {page_path}")
            if page_ext.get("page", {}).get("id") != page_id:
                raise DrawError(f"import {page_id} points at a different Page source: {page_path}")
            placement = item.get("placement", {})
            indexes = page_ext.get("migration", {}).get("sourceIndexes", {})
            loaded_pages.append((item, page_scene, indexes))
            for element in page_scene["elements"]:
                raw_id = element["id"]
                if raw_id in reference_owners and reference_owners[raw_id] != page_id:
                    ambiguous_refs.add(raw_id)
                else:
                    reference_owners[raw_id] = page_id

        for element in group_scene["elements"]:
            out = (
                namespace_element(element, gid, reference_owners, ambiguous_refs)
                if namespace else copy.deepcopy(element)
            )
            index = migration.get(element["id"])
            (ordered if index is not None else appended).append((index, out))

        for item, page_scene, indexes in loaded_pages:
            page_id = item["page"]
            placement = item.get("placement", {})
            if placement.get("visible", True) is False:
                continue
            local_ids = {element["id"] for element in page_scene["elements"]}
            page_reference_owners = dict(reference_owners)
            page_reference_owners.update({raw_id: page_id for raw_id in local_ids})
            page_ambiguous_refs = ambiguous_refs - local_ids
            for element in page_scene["elements"]:
                moved = transformed(element, placement)
                out = (
                    namespace_element(
                        moved, page_id, page_reference_owners, page_ambiguous_refs
                    )
                    if namespace else moved
                )
                index = indexes.get(element["id"])
                (ordered if index is not None else appended).append((index, out))
            merge_files(files, page_scene.get("files", {}), page_id)

    ordered.sort(key=lambda pair: pair[0])
    elements = [element for _, element in ordered]
    elements.extend(element for _, element in appended)
    for element in elements:
        if element["id"] in seen_ids:
            raise DrawError(f"duplicate element id after composition: {element['id']}")
        seen_ids.add(element["id"])
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "haipipe-board/draw.py composed",
        "elements": elements,
        "appState": app_state or {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": files,
        "haipipe": {"schema": SCHEMA, "kind": "composed-board"},
    }


def compose(board: Path, output: Path, replace: bool) -> int:
    if output.exists() and not replace:
        raise DrawError(f"refusing to overwrite output: {output}")
    scene = compose_data(board, namespace=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_scene(output, scene)
    print(f"wrote {output} · {len(scene['elements'])} namespaced elements")
    return 0


def verify(board: Path, source_path: Path) -> int:
    source = read_scene(source_path)
    restored = compose_data(board, namespace=False)
    if restored["elements"] != source["elements"]:
        raise DrawError("recomposed elements differ from the legacy source")
    if restored["files"] != source.get("files", {}):
        raise DrawError("recomposed files differ from the legacy source")
    print(
        f"verified exact round trip · {len(source['elements'])} elements · "
        f"{len(source.get('files', {}))} files · legacy source unchanged"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    split_ap = sub.add_parser("split", help="plan or create linked draw/ sources")
    split_ap.add_argument("board", type=Path)
    split_ap.add_argument("--source", type=Path, help="legacy scene; defaults to board.excalidraw")
    split_ap.add_argument("--apply", action="store_true", help="create sources after preflight")
    sync_ap = sub.add_parser("sync", help="add Page sources missing after board.md changed")
    sync_ap.add_argument("board", type=Path)
    sync_ap.add_argument("--apply", action="store_true", help="create missing sources and update manifests")
    compose_ap = sub.add_parser("compose", help="compose all Group and Page sources")
    compose_ap.add_argument("board", type=Path)
    compose_ap.add_argument("--output", type=Path, required=True)
    compose_ap.add_argument("--replace", action="store_true")
    verify_ap = sub.add_parser("verify", help="prove an exact legacy-scene round trip")
    verify_ap.add_argument("board", type=Path)
    verify_ap.add_argument("--source", type=Path, help="legacy scene; defaults to board.excalidraw")
    return ap


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    board = args.board.resolve()
    if not (board / "board.md").is_file():
        raise DrawError(f"not a Board folder: {board}")
    if args.command == "split":
        source = (args.source or board / "board.excalidraw").resolve()
        return split(board, source, args.apply)
    if args.command == "sync":
        return sync(board, args.apply)
    if args.command == "compose":
        return compose(board, args.output.resolve(), args.replace)
    source = (args.source or board / "board.excalidraw").resolve()
    return verify(board, source)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DrawError as exc:
        print(f"draw: {exc}", file=sys.stderr)
        raise SystemExit(2)
