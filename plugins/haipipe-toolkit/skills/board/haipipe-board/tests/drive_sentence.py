"""Drive every sentence gesture in a real Chrome, and record what happened.

WHY THIS IS NOT A UNIT TEST (JL 260802: "假如我们自己做 test，怎么让这些东西
全都 work as expected？你可以靠 Chrome，然后去操作它，再记录一下").

Every sentence defect that reached JL passed the unit tests first. The ⚑ badge
being posted as part of the anchor, the composer collapsing to one character
wide, the card button that could only fail: each one was a correct file and a
wrong page. So this harness asserts nothing about functions. It opens the page
a reader opens, moves the real mouse, and checks what is on the screen after.

It also RECORDS: every step writes a screenshot and a row, and the run ends
with `report.md` next to them, so a red step can be looked at rather than
guessed at.

    python3 tests/drive_sentence.py                     # against the live board
    python3 tests/drive_sentence.py --url <page-url> --out <dir>

Needs `playwright` and a Chrome already listening on 9222:
    /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\
        --remote-debugging-port=9222
"""
import argparse
import pathlib
import sys
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:                                       # pragma: no cover
    sys.exit("needs playwright: python3 -m pip install playwright")

BOARD = ("http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/"
         "diagrams/01-boardform-260722/board/QB/QB5-overview.html")


class Run:
    """One recorded run: a list of steps, each with its own screenshot."""

    def __init__(self, pg, out):
        self.pg, self.out, self.rows = pg, pathlib.Path(out), []
        self.out.mkdir(parents=True, exist_ok=True)
        self.t0 = time.time()

    def step(self, name, ok, detail="", shot=True):
        img = ""
        if shot:
            img = f"{len(self.rows):02d}-{name.replace(' ', '-')}.png"
            try:
                self.pg.screenshot(path=str(self.out / img))
            except Exception:
                img = ""
        self.rows.append((name, bool(ok), str(detail), img,
                          round(time.time() - self.t0, 1)))
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f"  · {detail}" if detail else ""))
        return ok

    def report(self):
        bad = [r for r in self.rows if not r[1]]
        lines = [f"# Sentence drive · {len(self.rows) - len(bad)}/{len(self.rows)} green",
                 "", "One real Chrome, one real mouse, one row per gesture.", ""]
        for name, ok, detail, img, at in self.rows:
            lines.append(f"- {'✅' if ok else '❌'} **{name}** · +{at}s")
            if detail:
                lines.append(f"  {detail}")
            if img:
                lines.append(f"  ![{name}]({img})")
        (self.out / "report.md").write_text("\n".join(lines) + "\n",
                                            encoding="utf-8")
        return not bad


def frame(pg, url):
    """The prose lives in the split shell's `page` frame, never in the top
    document: a harness that drives the top document finds nothing and reports
    a working feature as broken."""
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(2600)
    fr = pg.frame(name="page") or pg.main_frame
    fr.evaluate("()=>document.querySelectorAll('details').forEach(d=>d.open=true)")
    pg.wait_for_timeout(400)
    box = pg.locator("iframe[name=page]").first
    off = box.bounding_box() if box.count() else {"x": 0, "y": 0}
    return fr, off


def pick(pg, fr, off, words, anchor):
    """Select `words` with the actual mouse, inside the sentence holding
    `anchor`. Returns False when the words are not in one text node, which is
    itself the answer for a span that crosses markup."""
    p = fr.locator("p", has_text=anchor).first
    if not p.count():
        return False
    p.scroll_into_view_if_needed()
    pg.wait_for_timeout(450)
    hit = fr.evaluate("""([want, anchor]) => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = w.nextNode())) {
        const i = n.nodeValue.indexOf(want);
        if (i < 0) continue;
        const par = n.parentElement.closest('p');
        if (!par || !par.textContent.includes(anchor)) continue;
        const r = document.createRange();
        r.setStart(n, i); r.setEnd(n, i + want.length);
        const b = r.getBoundingClientRect();
        if (!b.width) continue;
        return {x0: b.left, x1: b.right, y: b.top + b.height / 2};
      }
      return null;
    }""", [words, anchor])
    if not hit:
        return False
    pg.mouse.move(off["x"] + hit["x0"] + 0.5, off["y"] + hit["y"])
    pg.mouse.down()
    pg.mouse.move(off["x"] + hit["x1"] - 0.5, off["y"] + hit["y"], steps=12)
    pg.mouse.up()
    pg.wait_for_timeout(500)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=BOARD)
    ap.add_argument("--cdp", default="http://127.0.0.1:9222")
    ap.add_argument("--out", default="/tmp/board-drive")
    a = ap.parse_args()

    stamp = time.strftime("%H%M%S")
    with sync_playwright() as pw:
        br = pw.chromium.connect_over_cdp(a.cdp)
        pg = br.contexts[0].new_page()
        pg.set_viewport_size({"width": 1500, "height": 950})
        r = Run(pg, a.out)
        fr, off = frame(pg, a.url)

        # ── 1 · the page a reader opens ─────────────────────────────────
        r.step("page loads in its pane", fr.locator("div.wrap").count() == 1,
               f"title {pg.title()[:48]!r}")

        # ── 2 · a card renders and opens on the words ───────────────────
        chips = fr.locator("button.chip.card.span")
        n0 = chips.count()
        r.step("span cards render", n0 > 0, f"{n0} on the page", shot=False)
        if n0:
            chips.first.scroll_into_view_if_needed()
            pg.wait_for_timeout(300)
            chips.first.click()
            pg.wait_for_timeout(500)
            r.step("clicking the words opens the card",
                   fr.locator(".chipcard.card.span:popover-open").count() == 1,
                   repr(chips.first.inner_text()))
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(300)

        # ── 3 · the words stay prose, not a button ──────────────────────
        if n0:
            look = fr.evaluate("""() => {
              const b = document.querySelector('button.chip.card.span');
              const s = getComputedStyle(b), p = getComputedStyle(b.closest('p'));
              return {border: s.borderStyle, deco: s.textDecorationLine,
                      sameColour: s.color === p.color,
                      sameFont: s.fontFamily === p.fontFamily};
            }""")
            r.step("the words read as prose, not a control",
                   look["sameColour"] and look["sameFont"]
                   and "underline" in look["deco"],
                   str(look), shot=False)

        # ── 4 · select → the two offers ─────────────────────────────────
        got = pick(pg, fr, off, "one thing", "One span holds one card")
        r.step("selecting words offers Comment and Card",
               got and fr.locator("#cbtn").is_visible()
               and fr.locator("#ccard").is_visible(),
               f"selection {fr.evaluate('String(getSelection())')!r}")

        # ── 5 · write one, and watch the page keep its place ────────────
        y_before = fr.evaluate("window.scrollY")
        open_before = fr.locator("details[open]").count()
        fr.locator("#ccard").click()
        pg.wait_for_timeout(400)
        r.step("the card composer opens with no author field",
               fr.locator("#cbox").is_visible()
               and not fr.locator("#cbox select").is_visible(),
               repr(fr.locator("#cbox .qq").inner_text()))
        fr.locator("#cbox textarea").fill(
            f"Recorded drive {stamp}: these words were selected with the mouse "
            "and this card was written from the page.")
        fr.locator("#cbox .cs").click()

        landed = False
        for _ in range(15):
            pg.wait_for_timeout(600)
            f2 = pg.frame(name="page") or pg.main_frame
            try:
                if f2.locator("button.chip.card.span").count() > n0:
                    landed = True
                    fr = f2
                    break
            except Exception:
                continue
        r.step("the new card appears without a manual reload", landed,
               f"{n0} -> {fr.locator('button.chip.card.span').count()}")

        # THE SMOOTHNESS ASSERTION. A reload answers this with 0 and every
        # section shut, which is exactly what "not smooth" looked like.
        y_after = fr.evaluate("window.scrollY")
        open_after = fr.locator("details[open]").count()
        r.step("the save kept the reader's place",
               abs(y_after - y_before) < 120 and open_after >= open_before,
               f"scroll {round(y_before)} -> {round(y_after)} · "
               f"open sections {open_before} -> {open_after}")

        # ── 6 · the same write again must be refused, visibly ───────────
        fr, off = frame(pg, a.url)
        if pick(pg, fr, off, "one thing", "One span holds one card"):
            fr.locator("#ccard").click()
            pg.wait_for_timeout(400)
            fr.locator("#cbox textarea").fill("this one must be refused")
            fr.locator("#cbox .cs").click()
            pg.wait_for_timeout(1800)
            r.step("a span that already has a card is refused, and says so",
                   fr.locator("#cbox").is_visible()
                   and bool(fr.locator("#ctoast").inner_text().strip()),
                   repr(fr.locator("#ctoast").inner_text()[:70]))
            r.step("a refused write keeps what was typed",
                   fr.locator("#cbox textarea").input_value().startswith("this one"),
                   repr(fr.locator("#cbox textarea").input_value()[:40]), shot=False)
            fr.locator("#cbox .cx").click()

        # ── 7 · a comment still lands under its sentence ────────────────
        fr, off = frame(pg, a.url)
        if pick(pg, fr, off, "any kind at all", "A lane is one"):
            pass
        else:
            pick(pg, fr, off, "adjacency", "adjacency")
        if fr.locator("#cbtn").is_visible():
            n_cmt = fr.locator(".sapp .cmt").count()
            fr.locator("#cbtn").click()
            pg.wait_for_timeout(400)
            fr.locator("#cbox textarea").fill(f"Recorded drive {stamp}: comment.")
            fr.locator("#cbox .cs").click()
            grew = False
            for _ in range(15):
                pg.wait_for_timeout(600)
                f2 = pg.frame(name="page") or pg.main_frame
                try:
                    if f2.locator(".sapp .cmt").count() > n_cmt:
                        grew, fr = True, f2
                        break
                except Exception:
                    continue
            r.step("a comment lands under its sentence and paints itself", grew,
                   f"{n_cmt} -> {fr.locator('.sapp .cmt').count()} comment rows")

        # ── 8 · the page still reads with every script deleted ──────────
        bare = fr.evaluate("""() => {
          const d = document.cloneNode(true);
          d.querySelectorAll('script').forEach(s => s.remove());
          return d.body.innerText.length;
        }""")
        r.step("the page survives its scripts being deleted", bare > 20000,
               f"{bare} characters of body text", shot=False)

        ok = r.report()
        print(f"\nrecord: {a.out}/report.md")
        pg.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
