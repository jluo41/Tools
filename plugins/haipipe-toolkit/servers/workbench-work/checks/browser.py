"""Exercise the synthetic demo in a browser; optional Playwright dependency.

Start checks/demo.py and the shared host first. This check changes only browser
preferences, writes screenshots, and never launches a Task Run.
"""
import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright, expect


def check(origin, screenshots):
    screenshots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1080}, color_scheme="light")
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(origin + "/", wait_until="networkidle")
        page.locator(".project-summary").click()
        page.get_by_text("Model comparison · demo", exact=True).click()
        expect(page.locator(".tw-task:visible")).to_have_count(6)
        page.screenshot(path=str(screenshots / "progress-desktop.png"), full_page=True)

        page.locator("#tw-state").select_option("attention")
        expect(page.locator(".tw-task:visible")).to_have_count(5)
        page.get_by_role("button", name="Clear", exact=True).click()
        page.locator("#tw-job").select_option("j02_model_training")
        expect(page.locator(".tw-task:visible")).to_have_count(2)
        page.locator("#tw-search").fill("Tune")
        expect(page.locator(".tw-task:visible")).to_have_count(1)
        page.locator("#b11j02t02 summary").click()
        expect(page.locator("#b11j02t02")).to_have_attribute("open", "")
        with page.expect_navigation(wait_until="networkidle"):
            page.get_by_role("button", name="Refresh", exact=True).click()
        expect(page.locator(".tw-task:visible")).to_have_count(1)
        expect(page.locator("#b11j02t02")).to_have_attribute("open", "")
        expect(page.locator("#tw-search")).to_have_value("Tune")
        page.screenshot(path=str(screenshots / "task-detail.png"), full_page=True)
        # Drill-downs use the existing Page presenters on a task,page host.
        for link in page.locator("#b11j02t02 .tw-links a").all():
            response = page.request.get(origin + link.get_attribute("href"))
            assert response.status == 200, (link.inner_text(), response.status)

        page.get_by_role("button", name="Clear", exact=True).click()
        page.locator('[data-space="runs"]').click()
        expect(page.locator(".tw-runs tbody tr:visible")).to_have_count(8)
        page.locator("#tw-state").select_option("failed")
        expect(page.locator(".tw-runs tbody tr:visible")).to_have_count(1)
        page.get_by_role("button", name="Clear", exact=True).click()
        page.screenshot(path=str(screenshots / "runs-desktop.png"), full_page=True)
        page.locator('[data-space="scope"]').click()
        expect(page.locator(".tw-toolbar")).to_be_hidden()
        expect(page.get_by_role("heading", name="Close condition")).to_be_visible()

        page.locator('[data-space="progress"]').click()
        page.locator("#b11j02t02 summary").click()
        page.set_viewport_size({"width": 390, "height": 844})
        page.screenshot(path=str(screenshots / "progress-mobile.png"), full_page=True)
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Mobile page overflows"
        page.locator('[data-space="runs"]').click()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Run table escapes its scroll container"
        page.emulate_media(color_scheme="dark")
        page.locator('[data-space="progress"]').click()
        page.screenshot(path=str(screenshots / "progress-mobile-dark.png"), full_page=True)
        assert not errors, errors
        browser.close()
    print("Browser checks passed: filters, details, refresh, drill-downs, spaces, desktop/mobile, dark mode.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", default="http://127.0.0.1:5652")
    parser.add_argument("--screenshots", type=Path, required=True)
    args = parser.parse_args()
    check(args.origin.rstrip("/"), args.screenshots)
