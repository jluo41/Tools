#!/usr/bin/env python3
"""Read-only mobile-browser smoke for anonymously shared Board routes.

This reproduces the reader path that exposed unread rejected-POST bodies being
parsed as the next HTTP/1.1 request: open a short Board route, enter its first
Page, and open one Plugin from the picker.  It records a screenshot per Board
and fails on a browser-visible 400/501 document response or error page.
"""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:5599")
    parser.add_argument("--board", action="append", required=True)
    parser.add_argument("--out", default="/tmp/board-public-read-smoke")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
        )
        for board_name in args.board:
            page = context.new_page()
            bad_documents = []
            page.on(
                "response",
                lambda response: bad_documents.append(
                    (response.status, response.url)
                )
                if response.request.resource_type == "document"
                and response.status in {400, 501}
                else None,
            )

            page.goto(
                f"{args.base.rstrip('/')}/b/{board_name}",
                wait_until="domcontentloaded",
                timeout=30_000,
            )
            page.wait_for_timeout(1_000)
            surface = page.frame(name="page") or page.main_frame
            task_link = surface.locator("a.ir").first
            if not task_link.count():
                excerpt = surface.locator("body").inner_text()[:240]
                raise AssertionError(
                    f"{board_name}: no Task Page link at {surface.url}: {excerpt!r}"
                )
            task_link.scroll_into_view_if_needed()
            task_link.tap()
            page.wait_for_timeout(1_000)

            surface = page.frame(name="page") or page.main_frame
            plugin_button = surface.locator("#mplugbtn")
            if plugin_button.count():
                plugin_button.tap()
                plugin_row = surface.locator("#mplugmenu .mrow").first
                plugin_row.wait_for(timeout=10_000)
                plugin_row.tap()
                page.wait_for_timeout(1_000)

            body = surface.locator("body").inner_text()
            if "Error response" in body or "Unsupported method" in body:
                raise AssertionError(f"{board_name}: browser-visible server error")
            if bad_documents:
                raise AssertionError(f"{board_name}: bad document responses {bad_documents}")
            if "/D-" not in surface.url:
                raise AssertionError(
                    f"{board_name}: Task Page did not open: {surface.url}"
                )

            shot = out / f"{board_name}.png"
            page.screenshot(path=str(shot), full_page=True)
            print(f"PASS {board_name} · Task Page + Plugin · {surface.url} · {shot}")
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
