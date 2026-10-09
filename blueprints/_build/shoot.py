"""Screenshot one UI element per CSS selector, with its computed style: the shared shooting helper.

Lifted from b01_haipipe-toolkit/j03_project_workbench/studio/s32-element-ui/build_s32_element_ui.py (its PICK_JS and
the clip-and-snap inside shoot()), so every Block's element gallery shoots the same way. A builder opens the page
(and clicks whatever it must to reach a view), then calls snap() per element:

    with browser() as page:
        page.goto("http://127.0.0.1:8191/")
        facts["tabs__home"] = snap(page, "nav.rail", SHOTS / "tabs__home.png")

Needs Playwright and an installed Chrome: run the builder with `uv run --with playwright --with pillow python …`.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

MAX_H = 700                     # a screenshot is cut at this height (the element's first screen)

# Find the element (the first visible match; "a|b" takes the box around both; "parent:sel" its parent), keep a wide
# row tight around what it holds, and read the style of its first control.
PICK_JS = """(sel) => {
  const one = s => { if (s.startsWith('parent:')) { const c = document.querySelector(s.slice(7));
                       return c ? c.parentElement : null; }
                     for (const e of document.querySelectorAll(s)) { const r = e.getBoundingClientRect();
                       if (r.width > 4 && r.height > 4) return e; } return null; };
  const els = sel.split('|').map(one).filter(Boolean);
  if (!els.length) return null;
  const tight = e => { const r = e.getBoundingClientRect();
    const kids = [...e.children].map(c => c.getBoundingClientRect()).filter(k => k.width > 2 && k.height > 2);
    if (!kids.length) return r;
    const right = Math.max(...kids.map(k => k.right)) + 8;
    return right < r.left + 0.8 * r.width ? {left: r.left, top: r.top, right, bottom: r.bottom} : r; };
  const rs = els.map(tight);
  const x = Math.min(...rs.map(r => r.left)), y = Math.min(...rs.map(r => r.top));
  const w = Math.max(...rs.map(r => r.right)) - x, h = Math.max(...rs.map(r => r.bottom)) - y;
  const probe = els[0].querySelector('button, a, select, input, th, td, summary') || els[0];
  const cs = getComputedStyle(probe);
  const style = {font: cs.fontSize + ' ' + cs.fontWeight, radius: cs.borderTopLeftRadius,
                 padding: cs.paddingTop + ' ' + cs.paddingLeft, border: cs.borderTopColor,
                 fill: cs.backgroundColor,
                 tag: probe.tagName.toLowerCase() + (probe.className ? '.' + String(probe.className).split(' ')[0] : '')};
  return {x: x + scrollX, y: y + scrollY, w, h, style};
}"""


@contextmanager
def browser(width: int = 1500, height: int = 1000):
    """A headless Chrome page at a fixed viewport, closed on exit."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        try:
            yield b.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        finally:
            b.close()


def snap(page, selector: str, out: Path, max_h: int = MAX_H) -> dict | None:
    """Screenshot the element(s) a selector names (alternatives "a,b": the first that is on the page) into out;
    return {selector, cut, font, radius, padding, border, fill, tag}, or None when nothing matches."""
    box = None
    for alt in selector.split(","):
        box = page.evaluate(PICK_JS, alt.strip())
        if box:
            break
    if not box:
        return None
    out.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out), full_page=True,
                    clip={"x": box["x"], "y": box["y"], "width": max(box["w"], 1), "height": min(max(box["h"], 1), max_h)})
    return {"selector": selector, "cut": box["h"] > max_h, **box["style"]}


def page_shot(page, out: Path) -> None:
    """The whole viewport, as the reader sees it."""
    out.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out))
