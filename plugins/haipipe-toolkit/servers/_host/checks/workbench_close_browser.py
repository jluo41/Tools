#!/usr/bin/env python3
"""Read-only mobile-browser acceptance for the generic Workbench-tab close."""

import argparse

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="a rendered Board Page URL")
    parser.add_argument(
        "--engine", choices=("chromium", "webkit"), default="chromium",
        help="browser engine used for the mobile interaction",
    )
    parser.add_argument(
        "--workbenches", default="outline,evidence",
        help="comma-separated Workbench ids to close in order",
    )
    args = parser.parse_args()
    workbench_ids = [item.strip() for item in args.workbenches.split(",") if item.strip()]

    with sync_playwright() as playwright:
        browser = getattr(playwright, args.engine).launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True
        )
        page = context.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=30_000)

        for workbench_id in workbench_ids:
            tab = page.locator(f'.rpt[data-tab="{workbench_id}"]')
            tab.wait_for(timeout=30_000)
            # Tapping an already-active derived tab means "rebuild" in the
            # shell.  The close check must remain read-only.
            if tab.get_attribute("aria-selected") != "true":
                tab.tap()
            close = page.locator(f'.rptx[data-close="{workbench_id}"]')
            close.wait_for(timeout=10_000)
            box = close.bounding_box()
            if not box or box["width"] < 36 or box["height"] < 36:
                raise AssertionError(f"{workbench_id} close target is too small: {box}")

            close.tap()
            page.wait_for_timeout(150)
            if page.locator(f'.rpt[data-tab="{workbench_id}"]').count():
                raise AssertionError(f"{workbench_id} returned after close")
            active = page.locator('.rpt[aria-selected="true"]').get_attribute("data-tab")
            if active == workbench_id:
                raise AssertionError(f"{workbench_id} remained active after close")

            # A closed default must stay closed after a new shell paint.  This
            # catches rankDefault() silently resurrecting Outline.
            page.reload(wait_until="domcontentloaded")
            page.locator("#rptset .rpt").first.wait_for(timeout=30_000)
            if page.locator(f'.rpt[data-tab="{workbench_id}"]').count():
                raise AssertionError(f"{workbench_id} returned after reload")

        # The top Workbench picker is the explicit way back after a close.
        for workbench_id in workbench_ids:
            page.locator("#mplugbtn").click()
            row = page.locator(
                "#mplugmenu .mrow", has_text=workbench_id.capitalize()
            )
            row.wait_for(timeout=10_000)
            row.click()
            reopened = page.locator(f'.rpt[data-tab="{workbench_id}"]')
            reopened.wait_for(timeout=10_000)
            if reopened.get_attribute("aria-selected") != "true":
                raise AssertionError(f"Workbench picker did not activate {workbench_id}")

        # A saved set can outlive a Workbench registration.  Closing the default
        # must skip that stale neighbor and activate the next offerable tab.
        if "outline" in workbench_ids and "evidence" in workbench_ids:
            key = page.evaluate(
                "Object.keys(localStorage).find(k => "
                "k.startsWith('board-split-tabs:'))"
            )
            if not key:
                raise AssertionError("open-tab set was not persisted")
            page.evaluate(
                "([key, value]) => localStorage.setItem(key, JSON.stringify(value))",
                [key, ["outline", "retired-workbench", "evidence"]],
            )
            page.reload(wait_until="domcontentloaded")
            page.locator('.rpt[data-tab="outline"]').wait_for(timeout=30_000)
            page.locator('.rptx[data-close="outline"]').tap()
            page.wait_for_timeout(150)
            active = page.locator(
                '.rpt[aria-selected="true"]'
            ).get_attribute("data-tab")
            if active != "evidence":
                raise AssertionError(f"stale replacement was selected: {active}")

        print(
            f"mobile {args.engine} Workbench close OK · "
            "close/reload · picker reopen · stale skip · "
            + " · ".join(workbench_ids)
        )
        browser.close()


if __name__ == "__main__":
    main()
