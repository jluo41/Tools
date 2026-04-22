"""Render inventory .excalidraw files to PNG.

Thin wrapper around Tools/plugins/excalidraw-diagram-skill/references/render_excalidraw.py.
No parallel CDN / template — we use the shared renderer so any fix there (e.g. the
jsdelivr-vs-esm.sh CDN switch) benefits both the excalidraw skill and us.

Usage:
    python render.py one.excalidraw two.excalidraw
    python render.py --all <dir>     # recursively render every .excalidraw under <dir>

Exit code 0 on full success; non-zero if any render failed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = Path("/home/jluo41/WellDoc-SPACE/Tools/plugins/excalidraw-diagram-skill/references")
RENDER_SCRIPT = SKILL_DIR / "render_excalidraw.py"


def _render_one(src: Path) -> Path | None:
    dst = src.with_suffix(".png")
    cmd = ["uv", "run", "python", str(RENDER_SCRIPT),
           str(src), "--output", str(dst), "--scale", "2"]
    r = subprocess.run(cmd, cwd=SKILL_DIR, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(f"  ERROR {src}: {r.stderr.strip()}\n")
        return None
    return dst


def main() -> None:
    ap = argparse.ArgumentParser(description="Render inventory .excalidraw → .png via excalidraw-diagram-skill")
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--all", type=Path, default=None,
                    help="Render every .excalidraw under this directory")
    args = ap.parse_args()

    sources: list[Path] = []
    if args.all:
        sources.extend(sorted(args.all.rglob("*.excalidraw")))
    sources.extend(p.resolve() for p in args.paths)
    sources = [s for s in sources if s.exists()]

    if not sources:
        sys.stderr.write("No .excalidraw files to render.\n")
        sys.exit(1)

    failures = 0
    for src in sources:
        out = _render_one(src)
        if out is None:
            failures += 1
        else:
            print(f"  {src.name} → {out.name}  ({out.stat().st_size/1024:.0f} KB)")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
