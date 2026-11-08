"""Record the walk of every example page a theme Block names, one per kind (JL 261105: "they are all the task, but
different UI"; "the walk should be left tab and right content as well").

    python walk_all.py <theme Block folder> [--origin http://127.0.0.1:5623] [--levels block,job,task] [--max-frames 30]

For each `ui-block:` / `ui-job:` / `ui-task:` line of the Block's face (a path from the Tools root), runs walk_shoot.py on
that page through a server rooted at Tools (so the page's path names no SPACE), then walk_player.py, writing
<Block>/walks/<level>-<folder>.html, and the first kind's also <Block>/walks/<level>.html. The Block's Report shows each
under its Block UI · Job UI · Task UI; its Work lists the kinds still without one. Rerun it after every review round.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def refs(block: Path) -> dict:
    face = (block / "board.md").read_text(encoding="utf-8")
    return {k: re.findall(rf"(?m)^ui-{k}:\s*(\S+)\s*$", face) for k in ("block", "job", "task")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("block", type=Path)
    ap.add_argument("--origin", default="http://127.0.0.1:5623")
    ap.add_argument("--levels", default="block,job,task")
    ap.add_argument("--max-frames", type=int, default=30)
    ap.add_argument("--frames-root", type=Path, default=None, help="where the raw frames go (default: a temp folder)")
    a = ap.parse_args()
    block = a.block.resolve()
    uv = shutil.which("uv") or str(Path.home() / ".local/bin/uv")
    tmp = a.frames_root or Path(subprocess.check_output(["mktemp", "-d"], text=True).strip())
    tmp.mkdir(parents=True, exist_ok=True)
    (block / "walks").mkdir(exist_ok=True)
    made = []
    for level in a.levels.split(","):
        for k, ref in enumerate(refs(block).get(level, [])):
            name = ref.rstrip("/").rsplit("/", 1)[-1]
            frames = tmp / f"{level}-{name}"
            url = f"{a.origin}/_board/workbench?layout=focus&path={ref}"
            subprocess.run([uv, "run", "--no-project", "--with", "playwright", "python", str(HERE / "walk_shoot.py"), url,
                            str(frames), "--max-frames", str(a.max_frames), "--sections", "report,work"],
                           check=True, cwd=str(tmp))
            if not any(frames.glob("*.jpg")):          # an empty recording never replaces a walk
                print(f"❌ {level} {name}: no frames, see {frames / 'notes.md'}; its walk is kept as it was")
                continue
            outs = [block / "walks" / f"{level}-{name}.html"] + ([block / "walks" / f"{level}.html"] if k == 0 else [])
            for out in outs:
                subprocess.run([sys.executable, str(HERE / "walk_player.py"), str(frames), str(out),
                                "--title", f"{name}, walked ({level}, placeholder)"], check=True)
            made.append(outs[0].relative_to(block).as_posix())
    print(f"{len(made)} walks in {block.name}/walks: " + ", ".join(made))
    return 0


if __name__ == "__main__":
    sys.exit(main())
