#!/usr/bin/env python3
"""Read-only mobile-browser regression for compact Outline deep links.

Drives the real nested Page -> Outline -> Evidence frames.  It deliberately
clicks several Run families while Outline is already active, then an Evidence
chip, then a Feedback chip. Runs must land on real Runs-lens elements; the
Evidence chip must land on its real Evidences-lens item card with no popover;
Feedback must land on its real Context record. This protects both the
state-loss race and the mobile popover trap.
"""

import argparse
import re
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import expect, sync_playwright


CASES = (
    ("Discovery supporting", "b01.j01.t04.r01", "b01.j01.t04.r01"),
    ("Execution supporting", "b03.j01.t01.r01", "b03.j01.t01.r01"),
    ("Page local", "j01.t02.r01", "pj01t02r01"),
)
FOCUS = "run-E02-VALUE-linked-design-counts"
EVIDENCE_ID = FOCUS.removeprefix("run-")
EVIDENCE_LABEL = "E2V.DesignCounts"


def split_url(url):
    if "split" in parse_qs(urlparse(url).query, keep_blank_values=True):
        return url
    return url + ("&split" if "?" in url else "?split")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="the Abstract Board Page URL")
    parser.add_argument(
        "--engine", choices=("chromium", "webkit"), default="chromium"
    )
    parser.add_argument(
        "--fallback-popover", action="store_true",
        help="remove the native Popover API before every document boots",
    )
    args = parser.parse_args()

    with sync_playwright() as playwright:
        browser = getattr(playwright, args.engine).launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True
        )
        if args.fallback_popover:
            context.add_init_script(
                "Object.defineProperty(HTMLElement.prototype, 'showPopover', "
                "{value: undefined, configurable: true});"
                "Object.defineProperty(HTMLElement.prototype, 'hidePopover', "
                "{value: undefined, configurable: true});"
            )
        page = context.new_page()
        page.goto(split_url(args.url), wait_until="domcontentloaded", timeout=30_000)

        page_frame = page.frame_locator("#fp")
        outline_frame = page.frame_locator("#fx-outline")
        evidence_frame = outline_frame.frame_locator(
            'iframe[title="Evidence Workspace"]'
        )

        for index, (label, page_address, detail_address) in enumerate(CASES):
            link = page_frame.locator(
                f'a[data-outline-focus="{FOCUS}"]'
                f'[data-outline-run="{page_address}"]'
            ).first
            link.wait_for(timeout=30_000)
            link.tap()

            evidence_space = outline_frame.locator(
                'button.space[data-space="evidence"]'
            )
            expect(evidence_space).to_have_class(
                re.compile(r"\bon\b"), timeout=30_000
            )
            runs_lens = evidence_frame.locator('nav button[data-seg="runs"]')
            expect(runs_lens).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
            detail = evidence_frame.locator(
                f'.related-run-card[data-evidence-id="{FOCUS.removeprefix("run-")}"]',
                has_text=detail_address,
            ).first
            expect(detail).to_be_visible(timeout=30_000)
            expect(detail).to_have_class(
                re.compile(r"\brun-focus\b"), timeout=30_000
            )
            expect(detail).to_contain_text(re.compile(r"Purpose|Plan"))
            expect(detail).to_contain_text("Availability")
            expect(detail).to_contain_text("Run & Result paths")
            expect(evidence_frame.locator(".run-popover:visible")).to_have_count(0)

            outline_href = outline_frame.locator("body").evaluate(
                "() => location.href"
            )
            evidence_href = evidence_frame.locator("body").evaluate(
                "() => location.href"
            )
            if f"focus={FOCUS}" not in outline_href or "run=" not in outline_href:
                raise AssertionError(f"{label}: outer deep link lost: {outline_href}")
            if "seg=runs" not in outline_href:
                raise AssertionError(f"{label}: outer route lost its segment: {outline_href}")
            if (f"focus={FOCUS}" not in evidence_href or "run=" not in evidence_href
                    or "seg=runs" not in evidence_href):
                raise AssertionError(f"{label}: inner deep link lost: {evidence_href}")

            print(f"PASS {label:<22} {detail_address}")
            if index + 1 < len(CASES):
                page.reload(wait_until="domcontentloaded")
                page_frame.locator(
                    f'a[data-outline-focus="{FOCUS}"]'
                ).first.wait_for(timeout=30_000)

        # The Evidence chip: same route family, different segment.  It must
        # activate Evidence Workspace -> Evidences and focus the exact item
        # card, and the Page itself must hold no Evidence popover at all.
        page.reload(wait_until="domcontentloaded")
        chip = page_frame.locator(
            f'a.outline-evidence[data-outline-lens="workspace"]'
            f'[data-outline-seg="items"][data-outline-focus="{FOCUS}"]'
        ).first
        chip.wait_for(timeout=30_000)
        expect(chip).to_have_text(EVIDENCE_LABEL)
        expect(page_frame.locator("[popover].outline-item-card")).to_have_count(0)
        expect(page_frame.locator('.outline-evidence[popovertarget]')).to_have_count(0)
        chip.tap()
        evidence_space = outline_frame.locator('button.space[data-space="evidence"]')
        expect(evidence_space).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        items_lens = evidence_frame.locator('nav button[data-seg="items"]')
        expect(items_lens).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        item_card = evidence_frame.locator(f"#{FOCUS}")
        expect(item_card).to_be_visible(timeout=30_000)
        expect(item_card).to_have_attribute("data-evidence-id", EVIDENCE_ID)
        expect(item_card).to_have_class(re.compile(r"\brun-focus\b"), timeout=30_000)
        expect(item_card).to_contain_text(EVIDENCE_LABEL)
        expect(item_card).to_contain_text("Needed")
        expect(item_card).to_contain_text("Ready when")
        expect(evidence_frame.locator(".run-popover:visible")).to_have_count(0)
        expect(evidence_frame.locator("[popover]:popover-open")).to_have_count(0)
        expect(page_frame.locator("[popover]:popover-open")).to_have_count(0)
        in_view = item_card.evaluate(
            "el => { const r = el.getBoundingClientRect();"
            " return r.bottom > 0 && r.top < window.innerHeight; }"
        )
        if not in_view:
            raise AssertionError("Evidence: focused item card is not in the viewport")
        outline_href = outline_frame.locator("body").evaluate("() => location.href")
        evidence_href = evidence_frame.locator("body").evaluate("() => location.href")
        if f"focus={FOCUS}" not in outline_href or "seg=items" not in outline_href:
            raise AssertionError(f"Evidence: outer deep link lost: {outline_href}")
        if "run=" in outline_href or "run=" in evidence_href:
            raise AssertionError(f"Evidence: a Run leaked into the route: {evidence_href}")
        if f"focus={FOCUS}" not in evidence_href or "seg=items" not in evidence_href:
            raise AssertionError(f"Evidence: inner deep link lost: {evidence_href}")
        print(f"PASS {'Evidence chip':<22} {EVIDENCE_LABEL}")

        page.reload(wait_until="domcontentloaded")
        feedback = page_frame.locator(
            'a[data-outline-lens="fb"]'
            '[data-outline-focus="feedback-S0-PP1"]'
        ).first
        feedback.wait_for(timeout=30_000)
        feedback.tap()
        context_space = outline_frame.locator('button.space[data-space="context"]')
        expect(context_space).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        feedback_lens = outline_frame.locator('.lens-chip[data-lens="fb"]')
        expect(feedback_lens).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        feedback_card = outline_frame.locator("#feedback-S0-PP1")
        expect(feedback_card).to_be_visible(timeout=30_000)
        expect(feedback_card).to_have_class(re.compile(r"\brecord-focus\b"))
        expect(feedback_card).to_contain_text("Reposition the opening")
        expect(feedback_card).to_contain_text("Do not begin with online reviews")
        print("PASS Feedback             S0-PP1")

        mode = "fallback" if args.fallback_popover else "native"
        print(f"mobile {args.engine} Outline links OK · {mode} Popover API · "
              "3 Runs + Evidence + Feedback")
        browser.close()


if __name__ == "__main__":
    main()
