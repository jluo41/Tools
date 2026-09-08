#!/usr/bin/env python3
"""Read-only mobile-browser regression for compact Outline deep links.

Drives the real nested Page -> Outline -> Evidence frames.  It deliberately
clicks several Run families while Outline is already active, then an Evidence
chip, then the typed Evidence chip inside the Outline plugin's own Bullet
Workspace, then a Feedback chip. Runs must land on real Runs-lens elements;
both Evidence chips must land on the real Evidences-lens item card with no
popover; Feedback must land on its real Context record. This protects both the
state-loss race and the mobile popover trap.

Run and Evidence cases are discovered from the current rendered Outline.
The selected item must expose Execution, Discovery, and a local Run so missing
coverage fails explicitly. The Feedback case discovers the first chip; a
Page whose plan carries no `Routed:` line has none, so pass `--feedback-url`
naming a Page that does (the Abstract lost its `Routed:` lines at plan v1.4).
"""

import argparse
import re
from urllib.parse import parse_qs, urlparse
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import expect, sync_playwright


def discover_cases(page_frame):
    """Read identities from rendered links, not from a particular paper version."""
    page_frame.locator('a[data-outline-run]').first.wait_for(timeout=30_000)
    routes = page_frame.locator('a[data-outline-run]').evaluate_all("""links =>
      links.map(a => ({
        focus: a.dataset.outlineFocus,
        address: a.dataset.outlineRun,
        family: a.parentElement.querySelector('.outline-run-family')?.textContent || ''
      }))""")
    grouped = {}
    for route in routes:
        if route["address"] and route["family"] in {"D", "X", "P"}:
            grouped.setdefault(route["focus"], {}).setdefault(route["family"], route)
    for focus, families in grouped.items():
        if {"D", "X", "P"} <= families.keys():
            chip = page_frame.locator(
                f'a.outline-evidence[data-outline-focus="{focus}"]').first
            return focus, chip.inner_text().strip(), [
                (label, families[family]["address"], family == "P")
                for family, label in (("D", "Discovery supporting"),
                                      ("X", "Execution supporting"),
                                      ("P", "Page local"))
            ]
    raise AssertionError(
        "Coverage missing: provide a Page with one Evidence Item mapping "
        "Discovery, Execution, and local Page Run links")


def normalized_address(value, local):
    compact = re.sub(r"[.\s]", "", value).lower()
    # Historical Page-local labels omit their fixed p prefix; preserve all
    # other owner namespaces, including complete local Task BJTR identities.
    return compact[1:] if local and compact.startswith("pj") else compact


def split_url(url):
    if "split" in parse_qs(urlparse(url).query, keep_blank_values=True):
        return url
    return url + ("&split" if "?" in url else "?split")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="the Board Page URL to inspect")
    parser.add_argument("--screenshots", type=Path, help="save mobile screenshots here")
    parser.add_argument(
        "--engine", choices=("chromium", "webkit"), default="chromium"
    )
    parser.add_argument(
        "--fallback-popover", action="store_true",
        help="remove the native Popover API before every document boots",
    )
    parser.add_argument(
        "--feedback-url", default="",
        help="a Board Page URL whose plan carries `Routed:` rows (default: --url)",
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
        FOCUS, EVIDENCE_LABEL, cases = discover_cases(page_frame)
        EVIDENCE_ID = FOCUS.removeprefix("run-")
        if args.screenshots:
            args.screenshots.mkdir(parents=True, exist_ok=True)

        for index, (label, page_address, local) in enumerate(cases):
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
                f'.related-run-card.run-focus[data-evidence-id="{EVIDENCE_ID}"]'
            )
            expect(detail).to_be_visible(timeout=30_000)
            expect(detail).to_have_class(
                re.compile(r"\brun-focus\b"), timeout=30_000
            )
            detail_address = detail.get_attribute("data-run-address") or ""
            if normalized_address(detail_address, local) != normalized_address(page_address, local):
                raise AssertionError(f"{label}: wrong Run focused: {detail_address}")
            expect(detail).to_have_attribute("data-run-kind", "local" if local else "supporting")
            expect(detail).to_contain_text(re.compile(r"Purpose|Plan"))
            expect(detail).to_contain_text("Availability")
            expect(detail).to_contain_text("Run & Result paths")
            expect(detail.locator('.related-run-head')).to_be_in_viewport(ratio=0.5)
            if not detail.locator('.related-run-head').evaluate(
                "el => el.getBoundingClientRect().top >= "
                "document.querySelector('nav').getBoundingClientRect().bottom"
            ):
                raise AssertionError(f"{label}: sticky navigation obscures the Run heading")
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
            if args.screenshots:
                page.screenshot(path=str(args.screenshots / f"{args.engine}-run-{index}.png"))
            if index + 1 < len(cases):
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

        # The typed Evidence chip INSIDE the Outline plugin (its Bullet
        # Workspace plan card) is the same route: it switches the lens in
        # place, lands on the same card, opens no popover, and leaves the
        # complete route in the Outline document's own URL (JL 260907: the
        # Page chip was fixed and this one still popped).
        page.reload(wait_until="domcontentloaded")
        chip = page_frame.locator(
            f'a.outline-evidence[data-outline-focus="{FOCUS}"]').first
        chip.wait_for(timeout=30_000)
        chip.tap()                                   # opens the Outline tab
        bullet_space = outline_frame.locator('button.space[data-space="bullet"]')
        bullet_space.wait_for(timeout=30_000)
        bullet_space.tap()
        typed = outline_frame.locator(
            f'a.evchip.typed-ev[data-outline-seg="items"]'
            f'[data-outline-focus="{FOCUS}"]').first
        typed.wait_for(timeout=30_000)
        expect(typed).to_have_text(EVIDENCE_LABEL)
        expect(outline_frame.locator('[popovertarget^="typed-ev"]')).to_have_count(0)
        typed.tap()
        expect(evidence_space).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        expect(items_lens).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        item_card = evidence_frame.locator(f"#{FOCUS}")
        expect(item_card).to_be_visible(timeout=30_000)
        expect(item_card).to_have_class(re.compile(r"\brun-focus\b"), timeout=30_000)
        expect(outline_frame.locator("[popover]:popover-open")).to_have_count(0)
        expect(evidence_frame.locator("[popover]:popover-open")).to_have_count(0)
        outline_href = outline_frame.locator("body").evaluate("() => location.href")
        evidence_href = evidence_frame.locator("body").evaluate("() => location.href")
        if f"focus={FOCUS}" not in outline_href or "seg=items" not in outline_href:
            raise AssertionError(f"Bullet chip: Outline URL lost the route: {outline_href}")
        if f"focus={FOCUS}" not in evidence_href or "seg=items" not in evidence_href:
            raise AssertionError(f"Bullet chip: inner deep link lost: {evidence_href}")
        if "run=" in outline_href or "run=" in evidence_href:
            raise AssertionError(f"Bullet chip: a Run leaked into the route: {evidence_href}")
        print(f"PASS {'Bullet Workspace chip':<22} {EVIDENCE_LABEL}")

        # Feedback: the first routed chip on the Page (or --feedback-url).
        feedback_url = args.feedback_url or args.url
        page.goto(split_url(feedback_url), wait_until="domcontentloaded", timeout=30_000)
        feedback = page_frame.locator(
            'a[data-outline-lens="fb"][data-outline-focus]').first
        try:
            feedback.wait_for(timeout=30_000)
        except PlaywrightTimeout:
            raise SystemExit(
                "FAIL Feedback: no Feedback chip on %s; its plan carries no "
                "`Routed:` line, so pass --feedback-url naming a Page that does"
                % feedback_url)
        feedback_id = feedback.get_attribute("data-outline-focus") or ""
        feedback_row = feedback_id.removeprefix("feedback-")
        if not feedback_row:
            raise AssertionError("Feedback: chip has no record identity")
        feedback.tap()
        context_space = outline_frame.locator('button.space[data-space="context"]')
        expect(context_space).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        feedback_lens = outline_frame.locator('.lens-chip[data-lens="fb"]')
        expect(feedback_lens).to_have_class(re.compile(r"\bon\b"), timeout=30_000)
        feedback_card = outline_frame.locator(f"#{feedback_id}")
        expect(feedback_card).to_be_visible(timeout=30_000)
        expect(feedback_card).to_have_class(re.compile(r"\brecord-focus\b"))
        expect(feedback_card).to_contain_text(feedback_row)
        outline_href = outline_frame.locator("body").evaluate("() => location.href")
        if "lens=fb" not in outline_href or f"focus={feedback_id}" not in outline_href:
            raise AssertionError(f"Feedback: outer deep link lost: {outline_href}")
        print(f"PASS {'Feedback':<22} {feedback_row}")
        if args.screenshots:
            page.screenshot(path=str(args.screenshots / f"{args.engine}-feedback.png"))

        # A touch reader must be able to leave the drawer and reopen the
        # exact record; navigation success alone does not test the close trap.
        close = page.locator('button[data-close="outline"]')
        expect(close).to_be_visible()
        close.tap()
        expect(page.locator('button.rpt[data-tab="outline"]')).to_have_count(0)
        feedback.tap()
        expect(outline_frame.locator(f"#{feedback_id}")).to_be_visible(timeout=30_000)
        expect(page.locator('button[data-close="outline"]')).to_be_visible()
        print("PASS mobile close and reopen Outline at exact Feedback record")

        mode = "fallback" if args.fallback_popover else "native"
        print(f"mobile {args.engine} Outline links OK · {mode} Popover API · "
              "3 Runs + Evidence + Bullet Workspace chip + Feedback + close/reopen")
        browser.close()


if __name__ == "__main__":
    main()
