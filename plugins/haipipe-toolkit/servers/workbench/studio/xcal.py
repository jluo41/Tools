"""QC8 · the canvas round-trip (QB4b, QD5): frames, scenes, embedded files.

Moved out of serve.py on 2026-07-31 under the gate_live.py response-identical gate.
QC3's Law: a refactor moves code, features never ride along.

Split by responsibility on 2026-11-13, behaviour unchanged:
  xcal_linked.py   linked Page and Group sources: compose, revision, owner saves
  xcal_outline.py  the Excalidraw+ link in a page's ## Outline
  xcal.py          XcalMixin: serve a scene or frame, mint, save, embedded files
This module re-exports every name that used to live here.
"""

import base64
import json
import re
import urllib.parse
from pathlib import Path
from urllib.parse import unquote

from . import base
from .excalidraw_proxy import ExcalidrawProxyMixin
from .xcal_linked import (XcalLinkedMixin, _DRAW_LOCK_GUARD, _DRAW_LOCKS,  # noqa: F401 (re-exported)
                          legacy_folded_page_scene)
from .xcal_outline import XcalOutlineMixin
from cli.draw import (DrawError, SCHEMA, compose_group_data, read_scene,  # noqa: F401
                      reference_ids, scene_text, write_scene_atomic,
                      write_scene_exclusive)


def under_root(root, rel, resolved):
    """Is `resolved` (the file `rel` names) inside --root? A folder linked in at the root
    itself counts as inside: the owner put it there (`Tools` -> `../Tools-SPACE`, where the
    design workbench keeps its methods drawing). A link deeper down is not followed out."""
    root = Path(root)
    try:
        resolved.relative_to(root.resolve())
        return True
    except ValueError:
        pass
    parts = Path(rel).parts
    link = root / parts[0] if parts else None
    if link is None or parts[0] in ("..", ".") or not link.is_symlink():
        return False
    try:
        resolved.relative_to(link.resolve())
        return True
    except ValueError:
        return False




class XcalMixin(XcalLinkedMixin, XcalOutlineMixin, ExcalidrawProxyMixin):
    def hydrate_files(self, scene, els, base):
        """scene pointers -> the dataURLs the editor expects, for these elements."""
        want = {e.get("fileId") for e in els
                if e.get("type") == "image" and e.get("fileId")}
        out = {}
        for fid in sorted(want):
            rec = (scene.get("files") or {}).get(fid)
            if not isinstance(rec, dict):
                continue
            if rec.get("dataURL"):          # an older scene with the bytes inline
                out[fid] = rec
                continue
            p = (base / rec.get("path", "")).resolve()
            try:
                p.relative_to(base.resolve())
            except ValueError:
                continue
            if not p.exists():
                continue
            mime = rec.get("mimeType") or "image/png"
            b64 = base64.b64encode(p.read_bytes()).decode()
            out[fid] = {"id": fid, "mimeType": mime, "created": rec.get("created", 0),
                        "dataURL": f"data:{mime};base64,{b64}"}
        return out

    def stash_files(self, scene, files, base, relative_to=None):
        """the editor's dataURLs -> files on disk + pointers in the scene."""
        keep = dict(scene.get("files") or {})
        wrote = []
        relative_to = (relative_to or base.parent).resolve()
        for fid, rec in (files or {}).items():
            if not isinstance(rec, dict):
                continue
            m = re.match(r"^data:([^;,]+);base64,(.+)$", rec.get("dataURL") or "", re.S)
            if not m:
                continue
            mime, b64 = m.group(1), m.group(2)
            name = re.sub(r"[^A-Za-z0-9_.-]", "_", fid) + self.XMIME.get(mime, ".bin")
            base.mkdir(parents=True, exist_ok=True)
            try:
                (base / name).write_bytes(base64.b64decode(b64))
            except Exception:
                continue
            rel = (base / name).resolve().relative_to(relative_to).as_posix()
            keep[fid] = {"id": fid, "mimeType": mime, "path": rel,
                         "created": rec.get("created", 0)}
            wrote.append(name)
        scene["files"] = keep
        return wrote

    def save_excalidraw(self, d):
        """POST /_board/excalidraw-save {board, frame, elements} -> the scene file.

        The half `#url=` never had. With `frame`, this MERGES: that frame's slice
        is replaced and every other page's frame is left exactly as it was, which
        is what lets one file be edited from any page without the pages fighting.
        Without `frame`, the whole scene is replaced, because that edit was made
        with the whole scene on screen.
        """
        rel = (d.get("board") or "").lstrip("/")
        frame = (d.get("frame") or "").strip()
        els = d.get("elements")
        if not isinstance(els, list):
            return {"ok": False, "err": "elements must be a list"}
        f = (self.root / rel).resolve()
        if not under_root(self.root, rel, f):
            return {"ok": False, "err": "outside --root"}
        if f.suffix != ".excalidraw" or not f.exists():
            return {"ok": False, "err": f"no scene at {rel!r}"}
        if legacy_folded_page_scene(f):
            return {"ok": False, "err": "legacy folded-Page draw/ is read-only; "
                    "open the canonical studio/draw scene to migrate and edit"}
        try:
            scene = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            return {"ok": False, "err": f"{f.name} is not a scene: {e}"}
        if scene.get("haipipe", {}).get("schema") == SCHEMA:
            return self.save_linked_excalidraw(d, f, scene)
        old = scene.get("elements", [])
        els = [e for e in els if isinstance(e, dict) and not e.get("isDeleted")]
        if not frame:
            scene["elements"] = els
        else:
            fid = next((e.get("id") for e in old
                        if e.get("type") == "frame" and e.get("name") == frame), None)
            if fid is None:
                names = [e.get("name") for e in old if e.get("type") == "frame"]
                return {"ok": False, "err": f"no frame named {frame!r}. Frames: {names}"}
            rest = [e for e in old if e.get("id") != fid and e.get("frameId") != fid]
            slice_ = []
            for e in els:
                if e.get("type") == "frame":
                    # keep the frame's identity whatever the editor renamed it to:
                    # the name IS the page's link, so losing it breaks that page
                    e["id"], e["name"] = fid, frame
                else:
                    e["frameId"] = fid
                slice_.append(e)
            if not any(e.get("id") == fid for e in slice_):
                orig = next(e for e in old if e.get("id") == fid)
                slice_.insert(0, orig)      # the frame was deleted; put it back
            scene["elements"] = rest + slice_
        imgs = self.stash_files(scene, d.get("files"), f.parent / "assets")
        tmp = f.with_name(f.name + ".tmp")
        tmp.write_text(scene_text(scene), encoding="utf-8")
        tmp.replace(f)
        return {"ok": True, "wrote": len(els), "total": len(scene["elements"]),
                "images": imgs, "frame": frame or "(whole board)"}

    def serve_frame(self):
        """Legacy `…/board.excalidraw?frame=QA4a` projection, that frame only.

        This route implements the retired one-scene source contract for Boards
        that have not moved to QD5a's linked Group/Page sources. Inside this
        legacy route the frame is not a separate file. New linked drawing work
        uses one Page source plus a Group composition instead, and must not be
        connected here until its ownership-aware live save path lands.

        A per-frame URL is needed anyway, because a page's Diagram should open at
        ITS frame rather than at the whole board. The hosted `?element=<id>` anchor
        is an Excalidraw+ feature; the open-source app reads only `id`,
        `resourcekey`, `start` and `t` from the query string, so the anchor has to
        come from this side. It is a projection, computed per request:

            …/fig/board.excalidraw                 the whole board, for drawing
            …/fig/board.excalidraw?frame=QA4a      that frame, for the page

        Both are the same file on disk. Editing happens on the first.
        """
        path, _, qs = self.path.partition("?")
        want = urllib.parse.parse_qs(qs).get("frame", [""])[0]
        # `?frame=` narrows to one page; no frame means the whole board, and
        # BOTH need their images turned back into dataURLs on the way out.
        raw = unquote(path).lstrip("/")
        # a drawing only: `/_x.excalidraw/../labeling/…/gold.private.json` once read any JSON under the root, sealed
        # labels and .server_config included (toolkit review 261031); no `..`, no dot folder, no private name
        bits = raw.split("/")
        if (not raw.endswith(".excalidraw") or ".." in bits or any(b.startswith(".") for b in bits)
                or ".private." in bits[-1] or ".protected." in bits[-1]):
            return self.reply(404, {"ok": False, "err": "not a drawing"})
        f = (self.root / raw).resolve()
        try:
            f.relative_to(self.root.resolve())
        except ValueError:
            return self.reply(403, {"ok": False, "err": "outside --root"})
        if not f.exists():
            # 🪄 A PAGE SCENE IS MINTED THE FIRST TIME IT IS OPENED (QPf2 §3:
            # an empty Page still gets a source file — existence never depends
            # on whether someone has drawn the first shape). The 404 this used
            # to return was worse than empty: the boot then skipped seeding and
            # the app woke on BROWSER-STORAGE leftovers, so a new page's Draw
            # split showed the LAST page's drawing, one armed save away from
            # landing in the wrong file (JL 260815, seen on QPf4).
            scene = self.mint_page_scene(f)
            if scene is None:
                scene = self.mint_board_scene(f)
            if scene is None:
                return self.reply(404, {"ok": False, "err": f"no {path}"})
        else:
            try:
                scene = json.loads(f.read_text(encoding="utf-8"))
            except Exception as e:
                return self.reply(400, {"ok": False, "err": f"{f.name} is not a scene: {e}"})

        try:
            linked = self.linked_runtime_scene(f, scene)
        except DrawError as e:
            return self.reply(409, {"ok": False, "err": f"cannot compose linked drawing: {e}"})
        if linked is not None:
            return self.reply_scene(linked)

        els = scene.get("elements", [])
        if not want:
            scene["files"] = self.hydrate_files(scene, els, f.parent)
            return self.reply_scene(scene)
        frame = next((e for e in els
                      if e.get("type") == "frame" and e.get("name") == want), None)
        if frame is None:
            names = [e.get("name") for e in els if e.get("type") == "frame"]
            return self.reply(404, {"ok": False,
                                    "err": f"no frame named {want!r}. Frames: {names}"})
        fid = frame.get("id")
        keep = [e for e in els if e.get("frameId") == fid or e.get("id") == fid]
        scene["elements"] = keep
        scene["files"] = self.hydrate_files(scene, keep, f.parent)
        return self.reply_scene(scene)

    def mint_page_scene(self, f):
        """<page>/draw/<id>.excalidraw -> mint EMPTY and return it.

        Only a real page's own canonical scene qualifies: the file must sit in
        `draw/` beside the face of a page folder carrying `<name>/<name>.md`
        (studio/ folders are gone, JL 261031; an old studio/draw/ copy is the
        retired source copied in on first open), and
        `group.excalidraw` is never minted here (a group view is composed from
        page sources, not authored). Anything else returns None and the caller
        404s exactly as before. If a retired flat Page scene exists, first open
        copies its content into this canonical address without changing the old
        file; otherwise the canonical scene starts empty. The write is the point:
        revision checks, the shell's watcher, and the first save all want the
        file to be real."""
        if f.suffix != ".excalidraw" or f.parent.name != "draw" or f.parent.parent.name == "studio":
            return None
        if f.name == "group.excalidraw":
            return None
        page_dir = f.parent.parent
        md = page_dir / f"{page_dir.name}.md"
        if not md.is_file():
            return None
        legacy = page_dir / "studio" / "draw" / f.name
        if legacy.is_file():
            scene = read_scene(legacy)
            f.parent.mkdir(parents=True, exist_ok=True)
            try:
                write_scene_exclusive(f, scene)
            except FileExistsError:
                scene = read_scene(f)
            return scene
        try:
            md_rel = str(md.resolve().relative_to(self.root.resolve()))
        except ValueError:
            md_rel = ""
        scene = {"type": "excalidraw", "version": 2,
                 "source": "haipipe-block/mint",
                 "elements": [],
                 "appState": {"gridSize": None,
                              "viewBackgroundColor": "#ffffff"},
                 "files": {},
                 "haipipe": {"schema": "haipipe-linked-drawing/v1",
                             "kind": "page",
                             "page": {"id": f.stem, "markdown": md_rel}}}
        f.parent.mkdir(parents=True, exist_ok=True)
        try:
            write_scene_exclusive(f, scene)
        except FileExistsError:
            scene = read_scene(f)
        return scene

    def mint_board_scene(self, f):
        """<board>/<name>.excalidraw -> mint EMPTY and return it.

        A Board's own drawing sits beside its `board.md` (no studio/, JL 261031); the Paper
        Workbench's Story › RoadMap Draw opens one there (JL 260930). Like a Page
        scene it is written the first time it is opened, so the first save has a
        file to land in. It is a plain scene, not a linked Page source, so a save
        replaces its elements. Anything else returns None."""
        if f.suffix != ".excalidraw" or not (f.parent / "board.md").is_file():
            return None
        scene = {"type": "excalidraw", "version": 2,
                 "source": "haipipe-block/mint",
                 "elements": [],
                 "appState": {"gridSize": None,
                              "viewBackgroundColor": "#ffffff"},
                 "files": {}}
        f.parent.mkdir(parents=True, exist_ok=True)
        try:
            write_scene_exclusive(f, scene)
        except FileExistsError:
            scene = read_scene(f)
        return scene

    def reply_scene(self, scene):
        body = json.dumps(scene).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
