"""s52 · Host and share with the team: s52-host-and-share.excalidraw, the current setup in three acts, and a Later frame at the right.

Every word is the face's `frames:` yaml (s52-host-and-share.md); this script only lays it out: each frame one
screen-sized map of boxes joined by named arrows (haipipe-studio scripts/topic_map.py), the frames in acts (a row each,
its `act:` title in a margin; b10 studio/_build/story.py), and between them the story's own arrows, each named by
its frame's `bridge:` line (JL 261012: "one frame should be as
large as possible, within the frame, we want the workflow map or the mindmap, the frames should be well arrange to
form the narrative"). Written through canvas.write, so a person's marks survive a rebuild.

    python build_s52_host_and_share.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parents[3] / "plugins" / "haipipe-toolkit" / "skills" / "1_base" / "project" / "haipipe-studio" / "scripts"
sys.path.insert(0, str(STUDIO))
sys.path.insert(0, str(HERE.parent / "_build"))
import canvas  # noqa: E402
import story  # noqa: E402  (b10 studio/_build: frames as acts, JL 261012)
import topic_map as M  # noqa: E402


def main():
    frames = M.frames_of(HERE / f"{HERE.name}.md")
    els: list = []
    M.draw_frames(els, frames, "s52")
    ids = [e["id"] for e in els if e["type"] == "frame"]
    acts, aside = [], {"title": "", "frames": []}
    for fid, fr in zip(ids, frames):
        if fr.get("aside"):                           # outside the story: one column at the right (later)
            aside["title"] = aside["title"] or fr["aside"]
            aside["frames"].append(fid)
            continue
        if fr.get("act") or not acts:                 # a frame with `act:` starts a new row
            acts.append({"title": fr.get("act", ""), "frames": []})
        acts[-1]["frames"].append(fid)
    story.arrange(els, acts, [f.get("bridge", "") for f in frames if not f.get("aside")], aside)
    out = HERE / f"{HERE.name}.excalidraw"
    canvas.write(out, els, "build_s52_host_and_share.py")
    from render_png import render
    render(out, out.with_suffix(".png"))


if __name__ == "__main__":
    main()
