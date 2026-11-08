"""Record a page's walk as frames, for walk_player.py (JL 261105: "a very quick video and we can pause in the middle").

    uv run --no-project --with playwright python walk_shoot.py <page url> <out folder>
        [--sections report,work] [--tabs 2] [--pops 1] [--max-frames 40] [--width 1440] [--height 900] [--settle 450]
    python walk_player.py <out folder> walks/<level>[-<folder>].html --title "<the page>, walked"

Opens the page in the installed Google Chrome (headless, through Playwright, as shoot.py), in a fresh browser so every
fold starts as a newcomer sees it, and lets only GET requests through, so no button can write anything. For each section
in --sections it loads the section, then each of its views (the view-button-list), and in each view opens the closed
bars one by one, clicks up to --tabs side tabs of each list and opens up to --pops pop-outs; before each shot the thing
acted on is outlined in orange (headless Chrome shows no pointer). Each frame is the visible screen. Writes NN.jpg,
captions.txt (one line per frame, what was done), notes.md (✅/❌ per step) and errors.txt (page errors).

It records the video; it does not judge. Reader tasks, hovering a canvas, the paper bar and the score stay the Chrome
walk's and the fresh reviewer's (haipipe-ui Walk). Record Tools placeholder pages only, on a local server.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

from playwright.sync_api import sync_playwright

OUTLINE = "outline:3px solid #e8590c;outline-offset:2px"


def with_query(url: str, **kw) -> str:
    u = urlparse(url)
    q = {k: v[0] for k, v in parse_qs(u.query).items()}
    q.update({k: v for k, v in kw.items() if v is not None})
    q = {k: v for k, v in q.items() if v != ""}
    return u._replace(query=urlencode(q)).geturl()


class Walk:
    def __init__(self, page, out: Path, a):
        self.page, self.out, self.a = page, out, a
        self.n, self.caps, self.notes, self.errors = 0, [], [], []
        page.on("pageerror", lambda e: self.errors.append(str(e)))

    def settle(self):
        self.page.wait_for_timeout(self.a.settle)

    def shot(self, caption: str, el=None):
        if self.n >= self.a.max_frames:
            return False
        if el is not None:
            try:
                el.scroll_into_view_if_needed(timeout=3000)
                self.page.evaluate("([e,s])=>{e.dataset.wsOld=e.style.cssText;e.style.cssText+=';'+s}", [el.element_handle(), OUTLINE])
            except Exception:
                el = None
        self.page.screenshot(path=str(self.out / f"{self.n:02d}.jpg"), type="jpeg", quality=80)
        if el is not None:
            try:
                self.page.evaluate("e=>{e.style.cssText=e.dataset.wsOld||''}", el.element_handle())
            except Exception:
                pass
        self.caps.append(caption)
        self.n += 1
        return True

    def note(self, ok: bool, what: str):
        self.notes.append(f"{'✅' if ok else '❌'} {what}")

    def load(self, url: str, caption: str, shoot: bool = True):
        try:
            self.page.goto(url, wait_until="load", timeout=60000)
            try:                                   # a page that polls (a Run still running) never goes quiet: settle
                self.page.wait_for_load_state("networkidle", timeout=5000)   # up to 5 s, then go on
            except Exception:
                pass
            self.settle()
            self.note(True, f"open {caption}")
            return self.shot(caption) if shoot else True
        except Exception as e:
            self.note(False, f"open {caption} → {e.__class__.__name__}")
            return False

    def view(self, label: str):
        """In the open view: each closed bar, then side tabs, then pop-outs, a frame after each."""
        p, a = self.page, self.a
        bars = p.locator("main details.band-sec:not([open]) > summary, main h3.fd-h[aria-expanded='false']")
        for k in range(min(bars.count(), 12)):
            bar = p.locator("main details.band-sec:not([open]) > summary, main h3.fd-h[aria-expanded='false']").first
            if not bar.count() or not bar.is_visible():
                break
            name = " ".join(bar.inner_text().split())[:70]
            try:
                bar.click(timeout=3000)
                self.settle()
                self.note(True, f"{label} · open {name}")
                if not self.shot(f"{label} · opened {name}", bar):
                    return
            except Exception as e:
                self.note(False, f"{label} · open {name} → {e.__class__.__name__}")
                break
        lists = p.locator("main .pb-list")
        for li in range(min(lists.count(), 4)):
            items = lists.nth(li).locator(":scope > *")
            for k in range(1, min(items.count(), a.tabs + 1)):          # the first tab is open already
                it = items.nth(k)
                if not it.is_visible():
                    continue
                name = " ".join(it.inner_text().split())[:60]
                try:
                    it.click(timeout=3000)
                    self.settle()
                    self.note(True, f"{label} · side tab {name}")
                    if not self.shot(f"{label} · side tab: {name}", it):
                        return
                except Exception as e:
                    self.note(False, f"{label} · side tab {name} → {e.__class__.__name__}")
        pops = p.locator("main a[data-pop]")
        done = 0
        for k in range(pops.count()):
            if done >= a.pops:
                break
            link = pops.nth(k)
            if not link.is_visible():
                continue
            name = " ".join(link.inner_text().split())[:60] or link.get_attribute("data-pop") or "pop-out"
            if name.startswith("Open this page"):         # the page's own Markdown: not a thing on the page
                continue
            try:
                link.click(timeout=3000)
                p.wait_for_selector("dialog#focus-viewer[open]", timeout=5000)
                self.settle()
                self.page.wait_for_timeout(600)
                # what loaded in the pop-out: a 404 or an error page is a broken step, never ✅ (261106: two reviews
                # found 404 forms the walk had ticked)
                inside = p.evaluate("()=>{const f=document.querySelector('dialog#focus-viewer iframe');"
                                    "try{const d=f&&f.contentDocument;return d?(d.title+' '+(d.body?d.body.innerText:'')).slice(0,300):''}"
                                    "catch(e){return ''}}")
                # a server's own refusal reads as broken too (261106: "No such run." passed as ✅ on two insight Jobs)
                broken = bool(re.search(r"Error response|\b404\b|Not Found|Traceback|No such (?:run|page|file)|Not a Page"
                                        r"|is not a page here", inside or "", re.I))
                self.note(not broken, f"{label} · pop-out {name}" + (" → it shows an error page" if broken else ""))
                self.shot(f"{label} · pop-out: {name}" + (" (❌ an error page)" if broken else ""))
                p.locator("dialog#focus-viewer [data-close]").first.click(timeout=3000)
                self.settle()
                done += 1
            except Exception as e:
                self.note(False, f"{label} · pop-out {name} → {e.__class__.__name__}")
                p.keyboard.press("Escape")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("url")
    ap.add_argument("out", type=Path)
    ap.add_argument("--sections", default="report,work")
    ap.add_argument("--tabs", type=int, default=2)
    ap.add_argument("--pops", type=int, default=1)
    ap.add_argument("--max-frames", type=int, default=40)
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--settle", type=int, default=450)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    for old in a.out.glob("*.jpg"):
        old.unlink()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")       # the installed Google Chrome: nothing to download
        ctx = browser.new_context(viewport={"width": a.width, "height": a.height}, color_scheme="light",
                                  reduced_motion="reduce")
        ctx.route("**/*", lambda r: r.continue_() if r.request.method in ("GET", "HEAD") else r.abort())   # read only
        page = ctx.new_page()
        w = Walk(page, a.out, a)
        for section in [s for s in a.sections.split(",") if s]:
            url = with_query(a.url, layout="focus", section=section, group="")
            name = section.title()
            if not w.load(url, name, shoot=False):
                break
            hrefs = [urljoin(url, h) for h in page.locator("nav.section-views a").evaluate_all("as=>as.map(a=>a.getAttribute('href'))") if h]
            if not any("group=" in h for h in hrefs):      # a section of one view: its page is the frame
                w.shot(name)
                w.view(name)
            for h in hrefs:
                group = parse_qs(urlparse(h).query).get("group", [""])[0]
                if not group or "_board/workbench" not in h:
                    continue
                label = page.locator(f"nav.section-views a[href*='group={group}']").first
                view = " ".join(label.inner_text().split()) if label.count() else group
                if not w.load(h, f"{name} · {view}"):
                    break
                w.view(f"{name} · {view}")
                if w.n >= a.max_frames:
                    break
            if w.n >= a.max_frames:
                break
        browser.close()
    (a.out / "captions.txt").write_text("\n".join(w.caps) + "\n", encoding="utf-8")
    (a.out / "notes.md").write_text("\n".join(w.notes) + "\n", encoding="utf-8")
    (a.out / "errors.txt").write_text("\n".join(w.errors) + ("\n" if w.errors else ""), encoding="utf-8")
    bad = sum(n.startswith("❌") for n in w.notes)
    print(f"{a.out}: {w.n} frames · {len(w.notes) - bad} ✅ · {bad} ❌ · {len(w.errors)} page errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
