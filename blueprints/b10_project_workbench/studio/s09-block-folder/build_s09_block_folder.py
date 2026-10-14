"""s09 · Block folder: what the Block's folder holds: s09-block-folder.excalidraw, two frames in one act, drawn by this builder.

    ① The Folder on screen   the Studio's fifth folding part, drawn from this Block's own folder on every build and
                              read through the server's own helpers (frame.folder_word, _size, _when), in the
                              workbench's colours (canvas.ui_frame); studio/ and this topic's folder are opened
    ② How a row is read      every word is the face's `frames:` yaml: boxes joined by named arrows (topic_map), the
                              Block's own counts put in at build time

The story's arrow between them is named; the map's key point is the box the yaml marks `key: true`
(excalidraw-studio principle 5). Written through canvas.write, so a person's marks survive a rebuild; the preview is
rendered too.

    python build_s09_block_folder.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
ROOT = HERE.parents[3]                                  # Tools/: the root the workbench serves
SKILLS = ROOT / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str(SKILLS / "project/haipipe-studio/scripts"))
sys.path.insert(0, str(HERE.parent / "_build"))
sys.path.insert(0, str(ROOT / "plugins/haipipe-toolkit/servers/_host"))
import canvas  # noqa: E402
import story  # noqa: E402  (b10 studio/_build: frames as acts, the key point, big titles)
import topic_map as M  # noqa: E402
from host_paths import bootstrap  # noqa: E402
bootstrap()
from live import frame  # noqa: E402  (the workbench's own reader: the drawing shows what the screen shows)

OPEN = ("studio", HERE.name)                            # the folders drawn open, as a person would open them
UI = canvas.UI
NAME, META, STEP, INDENT = 26, 22, 44, 46               # row sizes: a name, its count or size, a row, a level


def rows_of(folder: Path, depth: int = 0) -> list:
    """(depth, name, count or size, what it is for or its day, is a folder, is open), as folder_rows lists them."""
    out = []
    for p in sorted((p for p in folder.iterdir() if frame._shown(p)), key=lambda p: (not p.is_dir(), p.name.casefold())):
        if p.is_dir():
            n = sum(1 for c in p.iterdir() if frame._shown(c))
            out.append((depth, p.name + "/", str(n), frame.folder_word(p), True, p.name in OPEN))
            if p.name in OPEN:
                out += rows_of(p, depth + 1)
        else:
            st = p.stat()
            out.append((depth, p.name, frame._size(st.st_size), frame._when(st.st_mtime), False, False))
    return out


def el(kind: str, eid: str, x, y, w, h, fid: str, **extra) -> dict:
    e = {"id": eid, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0, "strokeColor": UI["line"],
         "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
         "roughness": 0, "opacity": 100, "groupIds": [], "frameId": fid, "roundness": None, "seed": 1, "version": 1,
         "versionNonce": 1, "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False,
         "customData": {"ui": True}}                     # coloured here, as on screen; colour_ui leaves it
    e.update(extra)
    return e


def line(els: list, fid: str, x, y, dx, dy) -> None:
    els.append(el("line", f"scr-{len(els)}", x, y, max(1, dx), max(1, dy), fid, points=[[0, 0], [dx, dy]],
                  lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None))


def text(els: list, fid: str, x, y, s: str, size: int, colour: str, code: bool = False) -> dict:
    e, _ = canvas.tree_text(x, y, s, size, 2400, fid)
    e.update(id=f"scr-{len(els)}", strokeColor=colour, customData={"ui": True},
             **({"fontFamily": canvas.CODE_FONT} if code else {}))
    els.append(e)
    return e


def screen(els: list) -> None:
    """① The Folder on screen: Studio › Folder opened, its tree read from this Block's folder now."""
    fid = "frame-s09-screen"
    f = M.frame_el(fid, "s09 · ① The Folder on screen", 2560, 1)
    canvas.ui_frame(f)
    els.append(f)
    t, h = canvas.tree_text(40, 28, "① The Folder on screen", M.FRAME_SIZE, 2400, fid)
    t["id"] = "scr-title"
    els.append(t)
    sub, h2 = canvas.tree_text(40, 28 + h + 10, "Studio › Folder, under the topic cards, Related, Delivery and Timeline: this "
                               "Block's own folder, read at build time, studio/ and this topic opened", 22, 2400, fid)
    sub["id"] = "scr-sub"
    els.append(sub)
    top = 28 + h + 10 + h2 + 36
    card = el("rectangle", "scr-card", 40, top, 2480, 1, fid, backgroundColor=UI["box"], roundness={"type": 3})
    els.append(card)                                    # first, so it lies behind the rows
    text(els, fid, 70, top + 18, "▾ Folder", 30, UI["text"])
    line(els, fid, 40, top + 72, 2480, 0)
    text(els, fid, 80, top + 92, frame._rel(BLOCK, ROOT) + "/", 20, UI["mut"], code=True)
    y = top + 140
    for depth, name, n, word, is_dir, is_open in rows_of(BLOCK):
        x = 90 + depth * INDENT
        for d in range(depth):                          # the guide lines down an open folder's rows
            line(els, fid, 90 + d * INDENT + 14, y - 6, 0, STEP)
        icon = ("📂 " if is_open else "📁 ") if is_dir else frame.FILE_ICONS.get(Path(name).suffix.lower(), "📄") + " "
        e = text(els, fid, x, y, icon + name, NAME, UI["text"])
        e2 = text(els, fid, x + e["width"] + 22, y + 4, n, META, UI["mut"])
        if word:
            text(els, fid, e2["x"] + e2["width"] + 22, y + 4, word, META, UI["mut"])
        y += STEP
    card["height"] = y - top + 20
    f["height"] = y + 60


def fill(frames: list) -> list:
    """The Block's own counts into the map's words: {block}, {files}, {dirs}."""
    files = sum(1 for p in BLOCK.rglob("*") if p.is_file() and not any(q.startswith(".") for q in p.relative_to(BLOCK).parts))
    dirs = sum(1 for p in BLOCK.rglob("*") if p.is_dir() and not any(q.startswith(".") for q in p.relative_to(BLOCK).parts))
    facts = {"{block}": frame._rel(BLOCK, ROOT), "{files}": f"{files:,}", "{dirs}": f"{dirs:,}"}

    def put(v):
        if isinstance(v, str):
            for k, x in facts.items():
                v = v.replace(k, x)
            return v
        if isinstance(v, list):
            return [put(x) for x in v]
        if isinstance(v, dict):
            return {k: put(x) for k, x in v.items()}
        return v
    return put(frames)


def main():
    frames = fill(M.frames_of(HERE / f"{HERE.name}.md"))
    els: list = []
    screen(els)
    M.draw_frames(els, frames, "s09")
    ids = [e["id"] for e in els if e["type"] == "frame"]
    for fid, fr in zip(ids[1:], frames):                # principle 5: the box marked `key: true`, in the slight colour
        for b in fr.get("boxes") or []:
            if b.get("key"):
                story.key_point(els, fid, b["title"])
    story.big_titles(els)
    story.arrange(els, [{"title": "Act 1 · What the Block folder holds", "frames": ids}], ["each row is read like this"])
    out = HERE / f"{HERE.name}.excalidraw"
    canvas.write(out, els, "build_s09_block_folder.py", palette=False)   # keeps the key point's fill
    from render_png import render
    render(out, out.with_suffix(".png"))


if __name__ == "__main__":
    main()
