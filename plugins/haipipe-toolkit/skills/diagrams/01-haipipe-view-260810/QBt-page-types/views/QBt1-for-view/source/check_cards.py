#!/usr/bin/env python3
"""Drive the unified QBt1 View Cards in a real Chrome over CDP."""

from __future__ import annotations

import json
import pathlib
import sys

from playwright.sync_api import sync_playwright


HERE = pathlib.Path(__file__).resolve().parent
BOARD_ROOT = HERE.parents[3]
PAGE_RELATIVE = (
    "Tools/plugins/haipipe-toolkit/skills/diagrams/"
    "01-haipipe-view-260810/board/QBt/QBt1-for-view.html"
)
URL = f"http://100.121.165.84:5599/{PAGE_RELATIVE}"
REPORT_DIR = BOARD_ROOT / "_runs" / "browser" / "QBt1"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    def record(test: str, passed: bool, detail: str) -> None:
        rows.append({"test": test, "pass": bool(passed), "detail": detail})

    with sync_playwright() as playwright:
        print("connect Chrome", flush=True)
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.new_page()
        page.set_default_timeout(8000)
        print(f"open {URL}", flush=True)
        page.goto(URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(1600)
        frame = page.frame(name="page") or page.main_frame
        frame.locator("div.wrap").wait_for()
        frame.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        page.wait_for_timeout(250)

        diagram = frame.locator("details.diagram-section").first.inner_text()
        authored_tokens = (
            "QBt1-for-view",
            "QBt1-for-view.md",
            "QA-probes/",
            "source/",
            "build.py",
            "check_cards.py",
            "QBt1-Display1-trait-description-table",
            "QBt1-Display2-trait-illustration",
            "preview.png",
            "preview.pdf",
            "intake/",
            "recipe/",
            "candidates/",
            "versions/",
            "_fixture/",
            "displays/",
            "QBt1-for-view.docx",
            ".haipipe-view-build.json",
            "1-bound-source-count.md",
        )
        record(
            "Diagram lists the unified authored View tree",
            all(token in diagram for token in authored_tokens) and "O3-prose-support" not in diagram,
            diagram,
        )
        generated_tokens = (
            "Generated distribution",
            "QBt1-for-view.tex",
            "QBt1-for-view.pdf",
            "QBt1-for-view.docx",
            "references.bib",
            "build-manifest.json",
            "manifest.json",
            "QBt-page-types/consumer/",
            "S-Main-4-results.md",
            "QBt1-consumer-card-open.png",
        )
        record(
            "Diagram lists review projections and Consumer target",
            all(token in diagram for token in generated_tokens),
            diagram,
        )

        for heading in ("1 · QA inputs", "2 · View body", "3 · Displays", "4 · Consumers"):
            record(
                f"Content contains {heading}",
                frame.locator("details.csec", has_text=heading).count() >= 1,
                heading,
            )

        def click_span(
            section_text: str,
            label: str,
            expected: tuple[str, ...],
            screenshot: str | None = None,
        ) -> str:
            section = frame.locator("details.csec", has_text=section_text).first
            button = section.locator("button.chip.card.span", has_text=label).first
            record(f"{label} has an exact-span Card", button.count() == 1, label)
            button.scroll_into_view_if_needed()
            button.click()
            page.wait_for_timeout(120)
            opened = frame.locator(".chipcard.card.span:popover-open")
            body = opened.first.inner_text() if opened.count() else ""
            record(
                f"{label} Card opens the correct payload",
                opened.count() == 1 and all(token in body for token in expected),
                body,
            )
            if screenshot:
                page.screenshot(path=str(REPORT_DIR / screenshot))
            page.keyboard.press("Escape")
            page.wait_for_timeout(70)
            record(
                f"{label} Card closes",
                frame.locator(".chipcard.card.span:popover-open").count() == 0,
                "Escape closes the popover",
            )
            return body

        click_span(
            "1 · QA inputs",
            "three answered QA Probes",
            ("QI1", "1-canonical-definition.md", "2-observable-signal.md", "3-measurement-boundary.md"),
            "QBt1-input-card-open.png",
        )
        click_span(
            "1 · QA inputs",
            "task QA-bank answer",
            ("QI2", "1-bound-source-count.md", "Q-View-1", "answered"),
        )

        for label, evidence_id in (
            ("interpersonal trait", "EC1"),
            ("warmth and cooperation", "EC2"),
            ("patient-perceived signals", "EC3"),
            ("not treated as an error-free measure of latent personality", "EC4"),
        ):
            click_span("2 · View body", label, (evidence_id, "Binding:"))

        style_button = frame.locator(
            "button.chip.card.span", has_text="interpersonal trait"
        ).first
        style = style_button.evaluate(
            """button => {
              const own = getComputedStyle(button);
              const prose = getComputedStyle(button.closest('p'));
              return {
                underline: own.textDecorationLine,
                border: own.borderStyle,
                sameColor: own.color === prose.color,
                sameFont: own.fontFamily === prose.fontFamily,
                sameWeight: own.fontWeight === prose.fontWeight
              };
            }"""
        )
        record(
            "Card words still read as prose",
            "underline" in style["underline"]
            and style["border"] == "none"
            and style["sameColor"]
            and style["sameFont"]
            and style["sameWeight"],
            json.dumps(style, sort_keys=True),
        )

        body_section = frame.locator("details.csec", has_text="2 · View body").first
        citation_button = body_section.locator(
            "button.chip.cite", has_text="john1999bigfive"
        ).first
        record("View body contains a Citation Card", citation_button.count() == 1, "john1999bigfive")
        citation_button.click()
        page.wait_for_timeout(120)
        citation_card = frame.locator(".chipcard.cite:popover-open")
        citation_body = citation_card.first.inner_text() if citation_card.count() else ""
        record(
            "Citation Card opens bibliography entry and source",
            citation_card.count() == 1
            and "Big-Five Trait Taxonomy" in citation_body
            and "references.bib" in citation_body,
            citation_body,
        )
        page.screenshot(path=str(REPORT_DIR / "QBt1-citation-card-open.png"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(70)

        input_section = frame.locator("details.csec", has_text="1 · QA inputs").first
        number_button = input_section.locator("button.chip.num", has_text="3").first
        question_button = input_section.locator(
            "button.chip.qref", has_text="Q-View-1"
        ).first
        record(
            "QA inputs contain checked Value and Probe Cards",
            number_button.count() == 1 and question_button.count() == 1,
            "3 [Q-View-1]",
        )
        number_button.click()
        page.wait_for_timeout(120)
        number_card = frame.locator(".chipcard.num:popover-open")
        number_body = number_card.first.inner_text() if number_card.count() else ""
        record(
            "Value Card resolves through the QA-bank chain",
            number_card.count() == 1
            and "MATCHES the run" in number_body
            and "1-bound-source-count.md" in number_body,
            number_body,
        )
        page.screenshot(path=str(REPORT_DIR / "QBt1-value-card-open.png"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(70)

        question_button.click()
        page.wait_for_timeout(120)
        question_card = frame.locator(".chipcard.qref:popover-open")
        question_body = question_card.first.inner_text() if question_card.count() else ""
        record(
            "Probe Card opens its answered record and bank path",
            question_card.count() == 1
            and "ANSWERED" in question_body
            and "1-bound-source-count.md" in question_body,
            question_body,
        )
        page.keyboard.press("Escape")
        page.wait_for_timeout(70)

        displays = frame.locator("details.csec", has_text="3 · Displays").first
        for marker, expected, shot in (
            ("QBt1-Display1", ("QBt1-Display1", "EC1 through EC4", "NOT AGREED", "preview.pdf"), "QBt1-Display1-card-open.png"),
            ("QBt1-Display2", ("measurement boundary", "NOT AGREED", "figure-1.svg", "preview.pdf"), "QBt1-Display2-card-open.png"),
        ):
            button = displays.locator("button.chip.disp", has_text=marker).first
            record(f"Displays contains {marker}", button.count() == 1, marker)
            button.click()
            page.wait_for_timeout(150)
            card = frame.locator(".chipcard.disp:popover-open")
            card_body = card.first.inner_text() if card.count() else ""
            record(
                f"{marker} opens its artifact and independent state",
                card.count() == 1 and all(token in card_body for token in expected),
                card_body,
            )
            preview = card.locator("figure.ccprev img[src*='preview.png']").first
            preview_loaded = preview.count() == 1 and preview.evaluate(
                "image => image.complete && image.naturalWidth > 0 && image.naturalHeight > 0"
            )
            preview_first = card.locator(".ccb").first.evaluate(
                "node => Boolean(node.firstElementChild && node.firstElementChild.querySelector(\"img[src*='preview.png']\"))"
            )
            record(
                f"{marker} Card leads with its rendered PNG preview",
                preview_loaded and preview_first,
                f"loaded={preview_loaded} first={preview_first}",
            )
            page.screenshot(path=str(REPORT_DIR / shot))
            page.keyboard.press("Escape")
            page.wait_for_timeout(70)

        for display_id, folder, expected_dimensions, screenshot in (
            ("QBt1-Display1", "QBt1-Display1-trait-description-table", {"width": 1325, "height": 273}, "QBt1-Display1-table.png"),
            ("QBt1-Display2", "QBt1-Display2-trait-illustration", {"width": 1475, "height": 721}, "QBt1-Display2-illustration.png"),
        ):
            preview = frame.locator(
                f"details.csec img[src*='{folder}/preview.png']"
            ).first
            dimensions = preview.evaluate(
                "image => ({width: image.naturalWidth, height: image.naturalHeight})"
            )
            record(
                f"{display_id} PNG preview is embedded in the View Page",
                dimensions == expected_dimensions,
                json.dumps(dimensions, sort_keys=True),
            )
            preview.screenshot(path=str(REPORT_DIR / screenshot))

        consumer_body = click_span(
            "4 · Consumers",
            "Main Results section",
            ("C1", "S-Main-4", "QBt1-Display1", "Results / construct interpretation", "blocked"),
            "QBt1-consumer-card-open.png",
        )
        record(
            "Consumer Card names the real target file",
            "QBt-page-types/consumer/S-Main-4-results.md" in consumer_body,
            consumer_body,
        )

        consumer_button = frame.locator(
            "details.csec", has_text="4 · Consumers"
        ).first.locator("button.chip.card.span", has_text="Main Results section").first
        consumer_button.click()
        page.wait_for_timeout(120)
        target_link = frame.locator(
            ".chipcard.card.span:popover-open a", has_text="S-Main-4"
        ).first
        target_href = target_link.get_attribute("href") if target_link.count() else ""
        record(
            "Consumer Card exposes a live S-Main-4 Page link",
            target_link.count() == 1
            and bool(target_href)
            and "S-Main-4-results.html" in target_href,
            target_href or "missing link",
        )

        whole = frame.locator("div.wrap").inner_text()
        record(
            "Specimen has one semantic source and a source-free fixture",
            "content/" not in diagram
            and "O3-prose-support" not in whole
            and "_fixture" in diagram
            and "├── view.md" not in diagram
            and "QBt1-Display1-trait-description-table.md" not in diagram,
            "canonical Page plus authored resources and generated distribution",
        )

        target_link.click()
        frame.locator("div.wrap").wait_for()
        page.wait_for_timeout(250)
        frame.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        page.wait_for_timeout(100)
        consumer_page = frame.locator("div.wrap").inner_text()
        record(
            "Consumer Card navigates to the real Main Results Page",
            "S Main 4 · Results consumer handoff" in consumer_page
            and "QBt1-Display1" in consumer_page
            and "Results / construct interpretation" in consumer_page,
            consumer_page,
        )
        page.screenshot(path=str(REPORT_DIR / "S-Main-4-consumer-page.png"))
        page.close()

    passed = sum(1 for row in rows if row["pass"])
    report = {
        "page": "QBt1-for-view",
        "view": "QBt1-for-view",
        "url": URL,
        "passed": passed,
        "total": len(rows),
        "rows": rows,
    }
    (REPORT_DIR / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"QBt1 unified View Cards: {passed}/{len(rows)} passed")
    for row in rows:
        print(f"{'PASS' if row['pass'] else 'FAIL'} {row['test']}")
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
