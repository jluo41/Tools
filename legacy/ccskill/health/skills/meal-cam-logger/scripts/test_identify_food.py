"""Smoke test for identify_food().

Runs a single Claude vision call on one image file. No camera, no loop.
Useful to verify the API wiring before running the full meal_cam_loop.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python test_identify_food.py <image.jpg>

Requires:
    pip install anthropic
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

# Make meal_cam_loop importable regardless of where we're invoked from
sys.path.insert(0, str(Path(__file__).parent))
from meal_cam_loop import identify_food


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: test_identify_food.py <image.jpg>", file=sys.stderr)
        return 2
    img = Path(sys.argv[1])
    if not img.is_file():
        print(f"image not found: {img}", file=sys.stderr)
        return 2

    b64 = base64.standard_b64encode(img.read_bytes()).decode("ascii")
    label = identify_food(b64, model="claude-sonnet-4-6")

    print(f"image:  {img.name}  ({img.stat().st_size // 1024} KB)")
    print(f"label:  {label!r}")
    return 0 if label is not None else 1


if __name__ == "__main__":
    sys.exit(main())
