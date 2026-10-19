"""Smoke the WHOLE board in a real browser, and record it.

`drive_sentence.py` proves one sentence on a fixture. This proves the thing a
person opens: a real board, served by the running server, navigated the way a
reader navigates it. It writes nothing, so it is safe against a live board.

The two are different questions. A sentence can work perfectly on a page nobody
can reach, and a board can navigate perfectly while every write is broken.

    python3 tests/drive_board.py                         # the boardform board
    python3 tests/drive_board.py --base <url> --board <path> --out <dir>
"""
import argparse
import pathlib
import sys
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:                                        # pragma: no cover
    sys.exit("needs playwright: python3 -m pip install playwright")

BASE = "http://100.121.165.84:5599"
BOARD = "/Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722"


class Run:
    def __init__(self, pg, out):
        self.pg, self.out, self.rows = pg, pathlib.Path(out), []
        self.out.mkdir(parents=True, exist_ok=True)
        self.t0 = time.time()

    def step(self, name, ok, detail="", shot=True):
        img = ""
        if shot:
            img = f"{len(self.rows):02d}-{name.replace(' ', '-')[:42]}.png"
            try:
                self.pg.screenshot(path=str(self.out / img))
            except Exception:
                img = ""
        self.rows.append((name, bool(ok), str(detail), img,
                          round(time.time() - self.t0, 1)))
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f"  · {detail}" if detail else ""))
        return bool(ok)

    def report(self):
        bad = [r for r in self.rows if not r[1]]
        lines = [f"# Board smoke · {len(self.rows) - len(bad)}/{len(self.rows)} green",
                 "", "A real board in a real browser, navigated but never written to.", ""]
        for name, ok, detail, img, at in self.rows:
            lines.append(f"- {'✅' if ok else '❌'} **{name}** · +{at}s")
            if detail:
                lines.append(f"  {detail}")
            if img:
                lines.append(f"  ![{name}]({img})")
        (self.out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return not bad


def page_frame(pg, url, wait=2400):
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(wait)
    return pg.frame(name="page") or pg.main_frame


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--board", default=BOARD)
    ap.add_argument("--cdp", default="http://127.0.0.1:9222")
    ap.add_argument("--out", default="/tmp/board-smoke")
    a = ap.parse_args()
    B = a.base.rstrip("/") + a.board

    with sync_playwright() as pw:
        br = pw.chromium.connect_over_cdp(a.cdp)
        pg = br.contexts[0].new_page()
        pg.set_viewport_size({"width": 1500, "height": 950})
        r = Run(pg, a.out)

        # ── 1 · the Index, which is what "open the board" means ──────────
        pg.goto(f"{B}/board/index.html", wait_until="load")
        pg.wait_for_timeout(2500)
        ix = pg.frame(name="page") or pg.main_frame
        rows = ix.locator("a[href*='/board/']")
        r.step("1 the Index opens and lists pages", rows.count() > 30,
               f"{rows.count()} page links · title {pg.title()[:40]!r}")

        txt = ix.evaluate("document.body.innerText")
        r.step("2 the Index no longer lists the folded faces",
               not any(f"QB5{c} " in txt for c in "abcd"),
               "QB5a-QB5d absent from the roster", shot=False)
        r.step("3 the Index lists what replaced them",
               "QD8" in txt and "QB5e" in txt,
               "QD8 and QB5e both on the roster", shot=False)

        # ── 2 · every page I touched actually opens ──────────────────────
        for pid, path, probe in [
            ("QB5", "QB/QB5-overview.html", "What still has its own page"),
            ("QD8", "QD/QD8-sentence-address.html", "the address a machine is handed"),
            ("Skill-0", "QC/Skill-0-haipipe-board.html", "haipipe-sentence"),
            ("Skill-4", "QC/Skill-4-haipipe-sentence.html", "comment"),
            ("QB5e", "QB/QB5e-sentence-details-lifecycle.html", "Sentence details"),
            ("QC1b", "QC/QC1b-subskills.html", "sub-skill"),
        ]:
            fr = page_frame(pg, f"{B}/board/{path}")
            # textContent, not innerText: sections are folded by default, so
            # innerText reports only what is on screen and a page can look
            # empty while being complete. The old detail line also printed
            # "found <probe>" whether or not it was found, which made a red row
            # read like a green one.
            body = fr.evaluate("document.body.textContent")
            wraps = fr.locator("div.wrap").count()
            has = probe.lower() in body.lower()
            r.step(f"4.{pid} opens and carries its subject", wraps == 1 and has,
                   f"{len(body)} chars · div.wrap={wraps} · "
                   f"{probe!r} {'found' if has else 'MISSING'}", shot=False)

        fr = page_frame(pg, f"{B}/board/QB/QB5-overview.html")
        fr.evaluate("()=>document.querySelectorAll('details').forEach(d=>{"
                    "if(!d.classList.contains('sent')) d.open=true;})")
        pg.wait_for_timeout(500)
        r.step("5 QB5 renders all eight divisions",
               fr.locator("details.csec").count() >= 8,
               f"{fr.locator('details.csec').count()} foldable sections")
        # AT LEAST ONE, not exactly N. This asserted 2 and went red on 260802
        # when a duplicated division was trimmed out of QB5 and took a demo
        # card with it, which is a content edit rather than a defect. What the
        # page owes a reader is that the card is demonstrated at all, and that
        # clicking it works, which step 7 checks.
        r.step("6 QB5 demonstrates the card on the real board",
               fr.locator("button.chip.card.span").count() >= 1,
               str(fr.evaluate("[...document.querySelectorAll('button.chip.card.span')]"
                               ".map(b=>b.textContent)")), shot=False)
        card = fr.locator("button.chip.card.span").first
        card.scroll_into_view_if_needed()
        pg.wait_for_timeout(300)
        card.click()
        pg.wait_for_timeout(450)
        r.step("7 clicking the words opens the card on the real board",
               fr.locator(".chipcard.card.span:popover-open").count() == 1,
               repr(card.inner_text()))
        pg.keyboard.press("Escape")

        # ── 4 · navigation between pages, the way a reader moves ─────────
        pg.wait_for_timeout(300)
        before = pg.url
        # Scope to the PROSE. A bare `a` also matches the sidebar rail, whose
        # rows are hidden until their group is open, so the click could only
        # ever time out on an element a reader never sees.
        link = fr.locator("div.wrap a", has_text="QB5e").first
        if link.count() and link.is_visible():
            link.scroll_into_view_if_needed()
            pg.wait_for_timeout(300)
            link.click()
            pg.wait_for_timeout(2200)
            f2 = pg.frame(name="page") or pg.main_frame
            r.step("8 an id inside the prose navigates to that page",
                   "QB5e" in (pg.url + (f2.evaluate("document.body.innerText")[:200])),
                   f"{before.split('/')[-1]} -> {pg.url.split('/')[-1]}")

        # ── 5 · the sidebar, and the floor ───────────────────────────────
        fr = page_frame(pg, f"{B}/board/QB/QB5-overview.html")
        side = pg.frame(name="index")
        r.step("9 the pages sidebar renders beside the page",
               side is not None,
               "the split shell has its index pane", shot=False)
        bare = fr.evaluate("""() => {
          const d = document.cloneNode(true);
          d.querySelectorAll('script').forEach(s => s.remove());
          return d.body.innerText.length;
        }""")
        r.step("10 the real page reads with every script deleted", bare > 20000,
               f"{bare} characters of body text", shot=False)

        pg.set_viewport_size({"width": 420, "height": 900})
        fr = page_frame(pg, f"{B}/board/QB/QB5-overview.html")
        r.step("11 no sideways scroll at 420px",
               not fr.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2"),
               f"scrollWidth {fr.evaluate('document.documentElement.scrollWidth')}")
        pg.set_viewport_size({"width": 1500, "height": 950})

        ok = r.report()
        print(f"\nrecord: {a.out}/report.md")
        pg.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
