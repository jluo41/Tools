"""Exercise the generated Paragraph Run view without changing a real Page.

Requires Playwright and its Chromium/WebKit browsers. Uses synthetic files in
a TemporaryDirectory, no live listener or research content. Optional screenshots
are generated artifacts, not a second Page source.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from live.runs import render


def fixture(directory: Path) -> Path:
    page = directory / "S-Test.md"
    page.write_text("# Synthetic paragraph writing\n", encoding="utf-8")
    stem = "r01_page-writing_c01-p01"
    run = directory / "runs" / (stem + ".md")
    run.parent.mkdir()
    run.write_text(
        "---\nfamily: page\noperation: paragraph-writing\ntarget: C1.P1\n---\n"
        "## Prompt\nExplain the empty-field convention using the approved Context.\n"
        "<script>window.previewInjected = true</script>\n", encoding="utf-8")
    result = directory / "results" / stem
    result.mkdir(parents=True)
    (result / "runtime.yaml").write_text(
        "status: complete\nfamily: page\noperation: paragraph-writing\n"
        "target: C1.P1\n", encoding="utf-8")
    (result / "paragraph.md").write_text(
        "An empty field means no value was supplied. It does not mean zero.\n",
        encoding="utf-8")
    (result / "trace.md").write_text(
        "C1.P1.B1 → sentence 1; C1.P1.B2 → sentence 2.\n"
        "Style: Context v1. Seam: first paragraph. Verdict: pass.\n",
        encoding="utf-8")
    return page


def main() -> None:
    from playwright.sync_api import expect, sync_playwright

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshots", type=Path)
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="paragraph-runs-browser-") as tmp:
        page_source = fixture(Path(tmp))
        body = render(page_source, "", "")
        with sync_playwright() as runtime:
            for name in ("chromium", "webkit"):
                browser = getattr(runtime, name).launch(headless=True)
                for label, width, height in (("mobile", 390, 844), ("desktop", 1280, 900)):
                    context = browser.new_context(viewport={"width": width, "height": height},
                                                  has_touch=label == "mobile")
                    page = context.new_page()
                    errors, downloads = [], []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.on("download", lambda download: downloads.append(download))
                    page.set_content(body)
                    row = page.locator("tr.run")
                    detail = page.locator("tr.detail")
                    expect(row).to_have_count(1)
                    expect(row).to_contain_text("C1.P1")
                    expect(row).to_contain_text("Done")
                    expect(detail).to_be_hidden()
                    row.tap() if label == "mobile" else row.click()
                    expect(detail).to_be_visible()
                    expect(detail).to_contain_text("Explain the empty-field convention")
                    expect(detail).to_contain_text("It does not mean zero.")
                    expect(detail).to_contain_text("C1.P1.B2")
                    expect(row).to_have_attribute("aria-expanded", "true")
                    assert page.evaluate("window.previewInjected") is None
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                    if args.screenshots:
                        page.screenshot(path=str(args.screenshots / f"{name}-{label}.png"), full_page=True)
                    row.tap() if label == "mobile" else row.click()
                    expect(detail).to_be_hidden()
                    row.focus()
                    page.keyboard.press("Enter")
                    expect(detail).to_be_visible()
                    assert not errors, errors
                    assert not downloads, downloads
                    assert len(context.pages) == 1
                    print(f"PASS {name}/{label}: target, prompt, paragraph, trace, close/reopen, no script/download")
                    context.close()
                browser.close()


if __name__ == "__main__":
    main()
