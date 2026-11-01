"""The real page behind each of j02's nine UI cells (s11 to s19): one screenshot per level and section, saved as
`<cell>/screen.png`, which `studio_ui_cells.py` puts in the cell's Design (JL 261031: "please add more subgroup of the
UI ... to direct others how to make the UI for the report and work"; show the thing itself, never a redesign).

    python3 shoot_screens.py [--host http://100.121.165.84:5623]

Runs under the system python3, which has Playwright; the pages are b35's own on the Tools host (a public blueprint).
"""
import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parent
PAGE = {"block": BLOCK, "job": HERE, "task": HERE / "t02_block_page"}      # the real page of each level
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())


def cells():
    for face in sorted(HERE.glob("t0[234]_*/s1[1-9]-*-ui-*/")):
        nn, level, _, section = face.name.split("-")
        yield face, level, section


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--host", default="http://100.121.165.84:5623")
    a = ap.parse_args()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1400, "height": 900}, device_scale_factor=1)
        for cell, level, section in cells():
            rel = PAGE[level].relative_to(TOOLS).as_posix()
            page.goto(f"{a.host}/_board/workbench?layout=focus&path={rel}&section={section}", wait_until="load")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(cell / "screen.png"), clip={"x": 240, "y": 0, "width": 920, "height": 900})
            print(cell.relative_to(BLOCK) / "screen.png")
        browser.close()


if __name__ == "__main__":
    main()
