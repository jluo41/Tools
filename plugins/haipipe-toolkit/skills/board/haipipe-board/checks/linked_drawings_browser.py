#!/usr/bin/env python3
"""Read-only browser acceptance for the linked Group/Page Excalidraw controls."""

import argparse
import re
from urllib.parse import quote

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:5599")
    parser.add_argument("--group", required=True, help="Group source path below serve.py --root")
    parser.add_argument("--page", required=True, help="Page id to enter from the Group toolbar")
    parser.add_argument("--screenshot", help="optional screenshot path after Arrange opens")
    args = parser.parse_args()
    url = (f"{args.base}/_excalidraw/?board={quote(args.group, safe='/')}"
           "&edit=1&mode=group-source")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        writes = []
        page.on("request", lambda request: writes.append(request.url)
                if request.method == "POST" and request.url.endswith("/_board/excalidraw-save")
                else None)
        page.goto(url, wait_until="domcontentloaded")
        page.get_by_role("button", name=re.compile("Group layer")).wait_for()
        page.get_by_text("imported Pages are locked", exact=False).wait_for()
        page.locator("select").select_option(args.page)
        page.get_by_role("button", name=re.compile("Edit Page Source")).click()
        page.wait_for_url(re.compile(rf"board=.*{re.escape(args.page)}\.excalidraw"))
        page.get_by_text(f"page {args.page}", exact=True).wait_for()
        page.get_by_text("this file is the source", exact=False).wait_for()
        page.get_by_role("button", name=re.compile("Group")).click()
        page.wait_for_url(re.compile(r"mode=group-source"))
        page.get_by_role("button", name=re.compile("Arrange")).click()
        page.wait_for_url(re.compile(r"mode=arrange"))
        page.get_by_role("button", name="Save placement").wait_for()
        fields = page.locator('input[data-field="x"], input[data-field="y"], '
                              'input[data-field="scale"], input[data-field="visible"]')
        if fields.count() != 4:
            raise AssertionError(f"expected four placement controls, found {fields.count()}")
        page.wait_for_timeout(1800)  # exceed the autosave interval before judging
        if writes:
            raise AssertionError(f"navigation unexpectedly wrote a drawing: {writes}")
        if args.screenshot:
            page.screenshot(path=args.screenshot, full_page=True)
        print(f"linked drawing browser OK · Group layer · Arrange · Page {args.page} source · Back")
        browser.close()


if __name__ == "__main__":
    main()
