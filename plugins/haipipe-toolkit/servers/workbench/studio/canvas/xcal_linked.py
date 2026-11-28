"""Linked drawings (QD5a): one Page source or a composed Group view, read and saved by owner.

Split out of xcal.py (2026-11-13) by responsibility; behaviour unchanged.
XcalMixin in xcal.py inherits XcalLinkedMixin, so serve.py still composes `XcalMixin`.
"""

import hashlib
import threading
from pathlib import Path

from cli.draw import (DrawError, SCHEMA, compose_group_data, read_scene,
                      reference_ids, write_scene_atomic)


_DRAW_LOCK_GUARD = threading.Lock()
_DRAW_LOCKS = {}


def legacy_folded_page_scene(path):
    """Whether ``path`` is a retired studio/draw/ lane beneath a folded Page (studio/ folders are gone, JL 261031)."""
    path = Path(path)
    if path.parent.name != "draw" or path.parent.parent.name != "studio":
        return False
    page_dir = path.parent.parent.parent
    return (page_dir / f"{page_dir.name}.md").is_file()


class XcalLinkedMixin:
    def draw_lock(self, path):
        """One compare-and-save critical section per linked source."""
        key = str(path.resolve())
        with _DRAW_LOCK_GUARD:
            return _DRAW_LOCKS.setdefault(key, threading.Lock())

    @staticmethod
    def scene_revision(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def group_revision(self, group_path, scene=None):
        """Revision of the derived view: Group manifest plus every Page source."""
        group_path = group_path.resolve()
        scene = scene or read_scene(group_path)
        digest = hashlib.sha256()
        for path in [group_path] + [
            group_path.parent / item["source"]
            for item in scene.get("haipipe", {}).get("imports", [])
        ]:
            resolved = path.resolve()
            # The containment bound is the GROUP FOLDER, not the group's own
            # draw/. `cli/draw.py` splits a FOLDED page's scene into that
            # page's own studio/draw/ lane and writes the manifest source relative
            # to the group draw dir, so the path is `../<page>/studio/draw/<id>
            # .excalidraw` and it legitimately leaves draw/ — draw.py:415-418
            # says both forms must resolve "through the same join". Bounding at
            # draw/ refused every folded page: a manifest the CLI writer had
            # just produced could not be opened by the live editor at all, and
            # the error blamed the manifest. Traversal is still refused, one
            # level out (found 260823 on the first folded page to get a scene).
            try:
                resolved.relative_to(group_path.parent.parent.resolve())
            except ValueError as exc:
                raise DrawError(
                    f"import leaves the Group folder: {path}") from exc
            digest.update(path.name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
        return digest.hexdigest()

    def linked_runtime_scene(self, f, scene):
        """Return one Page source or a freshly composed Group view with owner data."""
        f = f.resolve()
        ext = scene.get("haipipe", {})
        rel = f.relative_to(self.root.resolve()).as_posix()
        if ext.get("schema") != SCHEMA:
            return None
        if ext.get("kind") == "page":
            owner = ext.get("page", {}).get("id")
            scene["haipipe"] = dict(ext)
            scene["haipipe"]["runtime"] = {
                "ownerKind": "page", "owner": owner, "source": rel,
                "revision": self.scene_revision(f),
            }
            scene["files"] = self.hydrate_files(scene, scene.get("elements", []), f.parent)
            return scene
        if ext.get("kind") != "group":
            return None
        composed = compose_group_data(f, namespace=True, runtime=True)
        imports = []
        for item in composed["haipipe"].get("imports", []):
            entry = dict(item)
            entry["board"] = (f.parent / item["source"]).relative_to(
                self.root.resolve()).as_posix()
            imports.append(entry)
        composed["haipipe"]["imports"] = imports
        composed["haipipe"]["runtime"] = {
            "ownerKind": "group",
            "owner": ext.get("group", {}).get("id"),
            "source": rel,
            "revision": self.group_revision(f, scene),
            "modes": ["group-source", "arrange", "page-source"],
        }
        composed["files"] = self.hydrate_files(
            composed, composed.get("elements", []), f.parent
        )
        return composed

    @staticmethod
    def strip_runtime_element(element, owners):
        """Turn one namespaced derived Group element back into source form."""
        def raw_id(value):
            if not isinstance(value, str) or "::" not in value:
                return value
            owner, _, rest = value.partition("::")
            return rest if owner in owners else value

        def clean(value, key=None):
            if isinstance(value, dict):
                out = {}
                for child_key, child in value.items():
                    if child_key == "haipipeRuntime" and key == "customData":
                        continue
                    if child_key in ("id", "frameId", "containerId", "elementId"):
                        out[child_key] = raw_id(child)
                    elif child_key == "groupIds" and isinstance(child, list):
                        out[child_key] = [raw_id(item) for item in child
                                          if not str(item).startswith("portal::")]
                    else:
                        out[child_key] = clean(child, child_key)
                return out
            if isinstance(value, list):
                return [clean(child, key) for child in value]
            return value
        return clean(element)

    def conflict(self, current):
        return {"ok": False, "conflict": True,
                "err": "drawing changed after this editor opened; reload before saving",
                "current_revision": current}

    def save_linked_page(self, d, f, scene):
        if legacy_folded_page_scene(f):
            return {"ok": False, "err": "legacy folded-Page draw/ is read-only; "
                    "migrate it to studio/draw before editing"}
        ext = scene.get("haipipe", {})
        owner = ext.get("page", {}).get("id")
        if d.get("owner_kind") != "page" or d.get("owner_id") != owner:
            return {"ok": False, "err": f"save owner does not match Page {owner}"}
        elements = d.get("elements")
        if not isinstance(elements, list):
            return {"ok": False, "err": "elements must be a list"}
        with self.draw_lock(f):
            current = self.scene_revision(f)
            if not d.get("base_revision") or d.get("base_revision") != current:
                return self.conflict(current)
            scene = read_scene(f)
            scene["elements"] = [e for e in elements
                                 if isinstance(e, dict) and not e.get("isDeleted")]
            images = self.stash_files(
                scene, d.get("files"), f.parent / "assets" / owner, f.parent
            )
            write_scene_atomic(f, scene)
            revision = self.scene_revision(f)
        return {"ok": True, "owner": owner, "owner_kind": "page",
                "wrote": len(scene["elements"]), "images": images,
                "revision": revision}

    def validate_group_elements(self, group_path, group_scene, elements):
        """Reject unresolved/ambiguous bindings before replacing a Group layer."""
        gid = group_scene["haipipe"]["group"]["id"]
        page_ids = [item["page"] for item in group_scene["haipipe"].get("imports", [])]
        owners = {gid, *page_ids}
        clean = []
        for element in elements:
            if not isinstance(element, dict) or element.get("isDeleted"):
                continue
            runtime = (element.get("customData") or {}).get("haipipeRuntime") or {}
            if runtime.get("kind") == "page" or (
                runtime.get("owner") and runtime.get("owner") != gid
            ):
                continue
            clean.append(self.strip_runtime_element(element, owners))
        ids = [element.get("id") for element in clean]
        if any(not item for item in ids) or len(ids) != len(set(ids)):
            raise DrawError("Group layer contains a missing or duplicate element id")
        group_ids = set(ids)
        page_owners = {}
        for item in group_scene["haipipe"].get("imports", []):
            page = read_scene(group_path.parent / item["source"])
            for element in page["elements"]:
                page_owners.setdefault(element["id"], set()).add(item["page"])
        for element in clean:
            for ref in reference_ids(element):
                if ref in group_ids:
                    continue
                matches = page_owners.get(ref, set())
                if len(matches) != 1:
                    why = "ambiguous" if matches else "unresolved"
                    raise DrawError(
                        f"Group element {element['id']} has {why} reference {ref}"
                    )
        return clean

    def save_linked_group(self, d, f, scene):
        ext = scene.get("haipipe", {})
        owner = ext.get("group", {}).get("id")
        if d.get("owner_kind") != "group" or d.get("owner_id") != owner:
            return {"ok": False, "err": f"save owner does not match Group {owner}"}
        mode = d.get("mode")
        if mode not in ("group-source", "arrange"):
            return {"ok": False, "err": f"unsupported Group edit mode: {mode!r}"}
        with self.draw_lock(f):
            scene = read_scene(f)
            current = self.group_revision(f, scene)
            if not d.get("base_revision") or d.get("base_revision") != current:
                return self.conflict(current)
            images = []
            if mode == "arrange":
                placement = d.get("placement") or {}
                page_id = placement.get("page")
                item = next((entry for entry in scene["haipipe"].get("imports", [])
                             if entry.get("page") == page_id), None)
                if item is None:
                    return {"ok": False, "err": f"Group {owner} does not import {page_id!r}"}
                try:
                    x, y, scale = (float(placement["x"]), float(placement["y"]),
                                   float(placement["scale"]))
                except (KeyError, TypeError, ValueError):
                    return {"ok": False, "err": "placement needs numeric x, y, and scale"}
                if not 0.05 <= scale <= 20:
                    return {"ok": False, "err": "scale must be between 0.05 and 20"}
                item["placement"] = {
                    "x": x, "y": y, "scale": scale,
                    "visible": bool(placement.get("visible", True)),
                }
                wrote = 1
            else:
                elements = d.get("elements")
                if not isinstance(elements, list):
                    return {"ok": False, "err": "elements must be a list"}
                try:
                    clean = self.validate_group_elements(f, scene, elements)
                except DrawError as exc:
                    return {"ok": False, "err": str(exc)}
                scene["elements"] = clean
                images = self.stash_files(
                    scene, d.get("files"), f.parent / "assets" / "group", f.parent
                )
                wrote = len(clean)
            write_scene_atomic(f, scene)
            revision = self.group_revision(f, scene)
        return {"ok": True, "owner": owner, "owner_kind": "group", "mode": mode,
                "wrote": wrote, "images": images, "revision": revision}

    def save_linked_excalidraw(self, d, f, scene):
        kind = scene.get("haipipe", {}).get("kind")
        if kind == "page":
            return self.save_linked_page(d, f, scene)
        if kind == "group":
            return self.save_linked_group(d, f, scene)
        return {"ok": False, "err": f"not a linked drawing source: {f.name}"}
