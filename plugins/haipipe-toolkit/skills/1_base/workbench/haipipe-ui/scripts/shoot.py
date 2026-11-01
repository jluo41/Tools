"""Screenshot one live page for a /haipipe-ui review.

    uv run --with playwright python shoot.py <url> <out.png> [--width 1440] [--height 1000] [--viewport]

Opens the page in the installed Google Chrome (headless, through Playwright), waits for the network to settle, and writes the picture. The
default is the whole page, so nothing below the fold goes unscored (b16 s32 A and B's first live round lost it);
--viewport takes only the first screen (--width by --height).
"""
from __future__ import annotations

import argparse
import sys

from playwright.sync_api import sync_playwright


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("url")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=1000)
    ap.add_argument("--viewport", action="store_true", help="only the first screen, not the whole page")
    ap.add_argument("--full", action="store_true", help=argparse.SUPPRESS)   # the old flag; the whole page is the default now
    a = ap.parse_args()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")       # the installed Google Chrome: nothing to download
        page = browser.new_page(viewport={"width": a.width, "height": a.height})
        page.goto(a.url, wait_until="networkidle", timeout=60000)
        page.screenshot(path=a.out, full_page=not a.viewport)
        browser.close()
    print(a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
