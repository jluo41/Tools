"""Drive every sentence gesture in a real Chrome, and record what happened.

WHY THIS IS NOT A UNIT TEST (JL 260802: "假如我们自己做 test，怎么让这些东西
全都 work as expected？你可以靠 Chrome，然后去操作它，再记录一下").

Every sentence defect that reached JL passed the unit tests first. The badge
posted as part of the anchor, the composer collapsed to one character wide, the
card button that could only ever fail: each one was a correct file and a wrong
page. So this harness asserts nothing about functions. It opens the page a
reader opens, moves the real mouse, and checks what is on the screen after.

It owns its own board and its own server, so a run writes only into a temp
folder and the second run starts from exactly where the first one did.

It RECORDS: every step writes a screenshot and a row, and the run ends with a
`report.md` beside them, so a red step can be looked at rather than guessed at.

    python3 tests/drive_sentence.py                    # builds, serves, drives
    python3 tests/drive_sentence.py --out <dir> --keep

Needs `playwright`, and a Chrome already listening for CDP:
    /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\
        --remote-debugging-port=9222
"""
import argparse
import pathlib
import shutil
import socket
import subprocess
import sys
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fixture_board                                       # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:                                        # pragma: no cover
    sys.exit("needs playwright: python3 -m pip install playwright")


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Run:
    """One recorded run: a list of steps, each with its own screenshot."""

    def __init__(self, pg, out):
        self.pg, self.out, self.rows = pg, pathlib.Path(out), []
        self.out.mkdir(parents=True, exist_ok=True)
        self.t0 = time.time()

    def step(self, name, ok, detail="", shot=True):
        img = ""
        if shot:
            img = f"{len(self.rows):02d}-{name.replace(' ', '-')[:44]}.png"
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
        head = f"# Sentence drive · {len(self.rows) - len(bad)}/{len(self.rows)} green"
        lines = [head, "",
                 "One real Chrome, one real mouse, one row per gesture.",
                 "Driven against a throwaway fixture board, so a run writes "
                 "nothing anyone reads.", ""]
        for name, ok, detail, img, at in self.rows:
            lines.append(f"- {'✅' if ok else '❌'} **{name}** · +{at}s")
            if detail:
                lines.append(f"  {detail}")
            if img:
                lines.append(f"  ![{name}]({img})")
        (self.out / "report.md").write_text("\n".join(lines) + "\n",
                                            encoding="utf-8")
        return not bad


def open_page(pg, url):
    """The prose lives in the split shell's `page` frame, never in the top
    document: a harness that drives the top document finds nothing and reports
    a working feature as broken."""
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(2200)
    fr = pg.frame(name="page") or pg.main_frame
    fr.evaluate("()=>document.querySelectorAll('details').forEach(d=>{"
                "if(!d.classList.contains('sent')) d.open=true;})")
    pg.wait_for_timeout(400)
    box = pg.locator("iframe[name=page]").first
    off = box.bounding_box() if box.count() else {"x": 0, "y": 0}
    return fr, off


def pick(pg, fr, off, words, anchor):
    """Select `words` with the actual mouse, inside the sentence holding
    `anchor`."""
    p = fr.locator("p", has_text=anchor).first
    if not p.count():
        return False
    p.scroll_into_view_if_needed()
    pg.wait_for_timeout(400)
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
    pg.wait_for_timeout(450)
    return True


def pick_in_figure(pg, fr, off, words):
    """Select inside a ``` figure. `pick` only looks inside <p>, so using it
    here scored 'no selection was made' as 'the button was withheld', which is
    a false pass and worse than a red row."""
    hit = fr.evaluate("""(want) => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = w.nextNode())) {
        const i = n.nodeValue.indexOf(want);
        if (i < 0 || !n.parentElement.closest('pre')) continue;
        n.parentElement.closest('details, section')
         ?.querySelectorAll('details').forEach(d => d.open = true);
        const r = document.createRange();
        r.setStart(n, i); r.setEnd(n, i + want.length);
        const b = r.getBoundingClientRect();
        if (!b.width) continue;
        r.startContainer.parentElement.scrollIntoView({block: 'center'});
        const c = r.getBoundingClientRect();
        return {x0: c.left, x1: c.right, y: c.top + c.height / 2};
      }
      return null;
    }""", words)
    if not hit:
        return False
    pg.mouse.move(off["x"] + hit["x0"] + 0.5, off["y"] + hit["y"])
    pg.mouse.down()
    pg.mouse.move(off["x"] + hit["x1"] - 0.5, off["y"] + hit["y"], steps=10)
    pg.mouse.up()
    pg.wait_for_timeout(450)
    return True


BARE = "The pooled coefficient reached a stable value in the third quarter"
CARDED = "The estimate was drawn from the clustered specification"
LANED = "Three separate records are filed underneath this particular sentence"
REMARK = "Someone should say whether this number was measured"
TWIN = "This exact sentence is written twice on this page"
BOTH = "The revised figure was redrawn from the second panel"
BROKEN = "Nothing in this sentence matches what the record below claims"
TWOC = "The first estimate and the second estimate disagreed"
MULTI = "The measurement was repeated under three separate conditions"
EDITME = "This sentence will be rewritten by the drive"


def panels_open(fr):
    return fr.locator(".chipcard.card.span:popover-open").count()


def drive(pg, base, r, src):
    url = f"{base}/board/QA/QA1-targets.html"
    fr, off = open_page(pg, url)

    # ══ A · WHAT RENDERS ═════════════════════════════════════════════════
    r.step("A1 page loads inside its pane", fr.locator("div.wrap").count() == 1,
           f"title {pg.title()[:44]!r}", shot=False)

    chips = fr.locator("button.chip.card.span")
    n0 = chips.count()
    r.step("A2 every card in the source renders on its words", n0 == 5,
           f"{n0} of 5: {chips.all_inner_texts()}", shot=False)

    r.step("A3 a card naming absent words renders LOUD, not silently",
           fr.locator(".lane.cardmiss").count() == 1,
           repr((fr.locator(".lane.cardmiss").first.text_content() or "")[:78])
           if fr.locator(".lane.cardmiss").count() else "no cardmiss row")

    laned = fr.locator("details.sent", has_text=LANED).first
    r.step("A4 a sentence with lanes starts SHUT",
           laned.count() == 1 and not laned.evaluate("d => d.open"),
           f"{fr.locator('details.sent').count()} sentence drawers", shot=False)

    both = fr.locator("details.sent", has_text=BOTH).first
    badge = both.locator(".sbadge").first.inner_text() if both.count() else ""
    r.step("A5 card and lanes coexist; the badge counts the LANES only",
           both.count() == 1 and both.locator("button.chip.card.span").count() == 1
           and "2" in badge,
           f"badge {badge!r} · 2 lanes + 1 card")

    bad = fr.locator("details.sent", has_text=BROKEN).first
    r.step("A6 a broken card makes its sentence's badge a warning",
           bad.count() == 1 and "\u26a0" in bad.locator(".sbadge").first.inner_text(),
           repr(bad.locator(".sbadge").first.inner_text()) if bad.count() else "-",
           shot=False)

    # ══ B · CLICKING A CARD ══════════════════════════════════════════════
    first = chips.first
    first.scroll_into_view_if_needed()
    pg.wait_for_timeout(300)
    first.click()
    pg.wait_for_timeout(400)
    r.step("B1 clicking the words opens exactly one panel", panels_open(fr) == 1,
           repr(first.inner_text()))
    body = (fr.locator(".chipcard.card.span:popover-open").first.inner_text()
            if panels_open(fr) else "")
    r.step("B2 the panel carries the record's own text",
           "Clicking these words opens this panel" in body,
           repr(body[:80]), shot=False)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    r.step("B3 Escape closes it", panels_open(fr) == 0, shot=False)

    look = fr.evaluate("""() => {
      const b = document.querySelector('button.chip.card.span');
      const s = getComputedStyle(b), p = getComputedStyle(b.closest('p'));
      return {deco: s.textDecorationLine, border: s.borderStyle,
              sameColour: s.color === p.color, sameFont: s.fontFamily === p.fontFamily,
              sameWeight: s.fontWeight === p.fontWeight};
    }""")
    r.step("B4 the words read as PROSE, not as a control",
           look["sameColour"] and look["sameFont"] and look["sameWeight"]
           and "underline" in look["deco"] and look["border"] == "none",
           str(look), shot=False)

    two = fr.locator("details.sent, p").filter(has_text=TWOC).first
    tc = fr.locator("button.chip.card.span", has_text="first estimate")
    r.step("B5 two cards on one sentence, and neither swallows the other",
           tc.count() == 1
           and fr.locator("button.chip.card.span", has_text="second estimate").count() == 1,
           "first estimate + second estimate", shot=False)
    tc.first.scroll_into_view_if_needed()
    pg.wait_for_timeout(250)
    tc.first.click()
    pg.wait_for_timeout(350)
    one_open = panels_open(fr)
    fr.locator("button.chip.card.span", has_text="second estimate").first.click()
    pg.wait_for_timeout(350)
    r.step("B6 opening the second card closes the first",
           one_open == 1 and panels_open(fr) == 1,
           f"after first {one_open}, after second {panels_open(fr)}")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(250)

    mc = fr.locator("button.chip.card.span", has_text="three separate conditions")
    mc.first.scroll_into_view_if_needed()
    pg.wait_for_timeout(250)
    mc.first.click()
    pg.wait_for_timeout(350)
    mb = (fr.locator(".chipcard.card.span:popover-open").first.inner_text()
          if panels_open(fr) else "")
    r.step("B7 a three-line card body arrives whole",
           all(x in mb for x in ("held the sample fixed", "widened it", "dropped the outliers")),
           repr(mb[:100]))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(250)

    kb = fr.evaluate("""() => {
      const b = document.querySelector('button.chip.card.span');
      b.focus();
      return {focusable: document.activeElement === b,
              tab: b.tabIndex >= 0, tag: b.tagName};
    }""")
    r.step("B8 a card is reachable by keyboard, being a real button",
           kb["focusable"] and kb["tag"] == "BUTTON", str(kb), shot=False)

    # ══ C · WRITING A CARD ═══════════════════════════════════════════════
    fr, off = open_page(pg, url)
    got = pick(pg, fr, off, "stable value", BARE)
    r.step("C1 selecting words offers Comment and Card",
           got and fr.locator("#cbtn").is_visible() and fr.locator("#ccard").is_visible(),
           f"selection {fr.evaluate('String(getSelection())')!r}")

    y0 = fr.evaluate("window.scrollY")
    open0 = fr.locator("details[open]").count()
    fr.locator("#ccard").click()
    pg.wait_for_timeout(350)
    r.step("C2 the composer opens with no author field",
           fr.locator("#cbox").is_visible() and not fr.locator("#cbox select").is_visible(),
           repr(fr.locator("#cbox .qq").inner_text()))
    fr.locator("#cbox textarea").fill(
        "Written by the recorded drive: selected with the mouse, saved from the page.")
    fr.locator("#cbox .cs").click()
    landed, waited = False, 0.0
    for _ in range(20):
        pg.wait_for_timeout(400); waited += 0.4
        f2 = pg.frame(name="page") or pg.main_frame
        try:
            if f2.locator("button.chip.card.span").count() > n0:
                landed, fr = True, f2; break
        except Exception:
            continue
    r.step("C3 the card appears with no manual reload", landed,
           f"{n0} -> {fr.locator('button.chip.card.span').count()} after {waited:.1f}s")
    y1 = fr.evaluate("window.scrollY")
    open1 = fr.locator("details[open]").count()
    r.step("C4 saving kept the scroll and every open section",
           abs(y1 - y0) < 120 and open1 >= open0,
           f"scroll {round(y0)} -> {round(y1)} · open {open0} -> {open1}")

    md = (src / "QA-targets" / "QA1-targets.md").read_text(encoding="utf-8")
    r.step("C5 the write added ONE line, and left the sentence alone",
           md.count("> Card stable value:") == 1
           and BARE in md and "stable value in the third" in md,
           f"{md.count(chr(62) + ' Card ')} Card lines in the source", shot=False)

    # ══ D · ANCHOR INTEGRITY · the regression that would kill everything ══
    fr, off = open_page(pg, url)
    n_cmt0 = fr.locator(".sapp .cmt").count()
    if pick(pg, fr, off, "in the third quarter", BARE):
        r.step("D1 a sentence that now HAS a card can still be selected",
               fr.locator("#cbtn").is_visible(),
               f"selection {fr.evaluate('String(getSelection())')!r}")
        fr.locator("#cbtn").click()
        pg.wait_for_timeout(350)
        fr.locator("#cbox textarea").fill("Anchor check: commenting on a sentence that carries a card.")
        fr.locator("#cbox .cs").click()
        grew = False
        for _ in range(20):
            pg.wait_for_timeout(400)
            f2 = pg.frame(name="page") or pg.main_frame
            try:
                if f2.locator(".sapp .cmt").count() > n_cmt0:
                    grew, fr = True, f2; break
            except Exception:
                continue
        r.step("D2 a LATER write on a carded sentence still finds its anchor", grew,
               "the card's words are unwrapped for the anchor, not deleted")
    else:
        r.step("D1 a sentence that now HAS a card can still be selected", False,
               "could not select across the card")

    # ══ E · WHAT MUST BE REFUSED ═════════════════════════════════════════
    fr, off = open_page(pg, url)
    if pick(pg, fr, off, "twice on this page", TWIN):
        fr.locator("#ccard").click(); pg.wait_for_timeout(350)
        fr.locator("#cbox textarea").fill("this one has to be refused")
        fr.locator("#cbox .cs").click(); pg.wait_for_timeout(1600)
        r.step("E1 an ambiguous sentence is refused, and says why",
               fr.locator("#cbox").is_visible()
               and bool(fr.locator("#ctoast").inner_text().strip()),
               repr(fr.locator("#ctoast").inner_text()[:60]))
        r.step("E2 a refused write keeps what was typed",
               fr.locator("#cbox textarea").input_value().startswith("this one"),
               repr(fr.locator("#cbox textarea").input_value()[:30]), shot=False)
        fr.locator("#cbox .cx").click(); pg.wait_for_timeout(250)

    fr, off = open_page(pg, url)
    in_fig = pick_in_figure(pg, fr, off, "a card is written onto its words")
    sel = fr.evaluate("String(getSelection())")
    r.step("E3 a real selection inside a figure offers NEITHER button",
           in_fig and bool(sel.strip())
           and not fr.locator("#ccard").is_visible()
           and not fr.locator("#cbtn").is_visible(),
           f"selected {sel[:34]!r} in a pre · card "
           f"{fr.locator('#ccard').is_visible()} · comment "
           f"{fr.locator('#cbtn').is_visible()}")

    fr, off = open_page(pg, url)
    ok4 = pick(pg, fr, off, "measurement was repeated", MULTI)
    r.step("E4 a fresh span on an already-carded sentence is still offered",
           ok4 and fr.locator("#ccard").is_visible(),
           f"selected {fr.evaluate('String(getSelection())')!r} beside an "
           "existing card, so one sentence may carry several")

    # ══ F · THE OTHER TWO GESTURES ═══════════════════════════════════════
    fr, off = open_page(pg, url)
    if pick(pg, fr, off, "measured or merely assumed", REMARK):
        n_c = fr.locator(".sapp .cmt").count()
        y2 = fr.evaluate("window.scrollY")
        fr.locator("#cbtn").click(); pg.wait_for_timeout(350)
        fr.locator("#cbox textarea").fill("Recorded drive: a remark on this sentence.")
        fr.locator("#cbox .cs").click()
        grew, waited = False, 0.0
        for _ in range(20):
            pg.wait_for_timeout(400); waited += 0.4
            f2 = pg.frame(name="page") or pg.main_frame
            try:
                if f2.locator(".sapp .cmt").count() > n_c:
                    grew, fr = True, f2; break
            except Exception:
                continue
        r.step("F1 a comment lands under its sentence and paints itself", grew,
               f"{n_c} -> {fr.locator('.sapp .cmt').count()} rows after {waited:.1f}s")
        r.step("F2 the comment save kept the reader's place",
               abs(fr.evaluate("window.scrollY") - y2) < 120,
               f"scroll {round(y2)} -> {round(fr.evaluate('window.scrollY'))}")

    # F3-F6 · EDITING, END TO END (JL 260802: "when I add comments, or I do
    # the editing, the page refresh, and ONLY I do the refresh, it will be
    # updated"). F3 used to stop at "the editor opened", which is exactly the
    # half that could not fail, and it hid a `location.reload()` on save.
    fr, off = open_page(pg, url)
    ed = fr.locator("p", has_text=EDITME).first
    if ed.count():
        ed.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
        y3 = fr.evaluate("window.scrollY")
        open3 = fr.locator("details[open]").count()
        n_chg = fr.locator(".sapp .change").count()
        fr.evaluate("() => { window.__ALIVE = 'yes'; }")
        ed.dblclick(); pg.wait_for_timeout(700)
        box = fr.locator("div.sedit textarea")
        r.step("F3 double-click opens the sentence editor", box.count() == 1,
               f"{fr.locator('div.sedit').count()} editors open")
        if box.count() == 1:
            box.fill(EDITME + " and it now carries one change record.")
            fr.locator("div.sedit button", has_text="Save").first.click()
            grew, waited = False, 0.0
            for _ in range(20):
                pg.wait_for_timeout(400); waited += 0.4
                f2 = pg.frame(name="page") or pg.main_frame
                try:
                    if f2.locator(".sapp .change").count() > n_chg:
                        grew, fr = True, f2; break
                except Exception:
                    continue
            r.step("F4 the edit repaints with NO manual reload", grew,
                   f"{n_chg} -> {fr.locator('.sapp .change').count()} change rows "
                   f"after {waited:.1f}s")
            r.step("F5 the edit SWAPPED rather than reloaded the frame",
                   fr.evaluate("window.__ALIVE || 'GONE — it reloaded'") == "yes",
                   "a window flag set before the save is still there after it",
                   shot=False)
            r.step("F6 the edit kept the reader's place",
                   abs(fr.evaluate("window.scrollY") - y3) < 120
                   and fr.locator("details[open]").count() >= open3,
                   f"scroll {round(y3)} -> {round(fr.evaluate('window.scrollY'))} · "
                   f"open {open3} -> {fr.locator('details[open]').count()}")

    # F7 · ADDING A TYPED LANE, the fourth write path
    fr, off = open_page(pg, url)
    tgt = fr.locator("p", has_text=REMARK).first
    if tgt.count():
        tgt.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
        n_lane = fr.locator(".sapp .lane").count()
        fr.evaluate("() => { window.__ALIVE2 = 'yes'; }")
        # The lane form is NOT the double-click gesture: double-click opens the
        # EDITOR. A lane comes from the `＋` in the sentence's hover rail, which
        # only exists while the sentence is hovered, so the mouse has to be on
        # it the way a reader's is.
        tgt.hover()
        pg.wait_for_timeout(400)
        plus = fr.locator(".schatbar button", has_text="＋")
        if plus.count():
            plus.first.click()
            pg.wait_for_timeout(500)
        form = fr.locator("div.sadd input[type=text]")
        if form.count() == 1:
            # PICK A TYPED KIND. The dropdown remembers what was used last and
            # falls back to `JL`, which is a person's initials and renders as a
            # COMMENT row, not a lane. Leaving it there made this step count a
            # `.lane` that was never going to appear and read as a broken swap.
            fr.locator("div.sadd select").select_option("Note")
            form.fill("A lane added by the recorded drive.")
            # Measure from HERE. Opening the form opens the sentence's drawer
            # and moves the page on purpose; the question this step asks is
            # whether SAVING moves the reader, so the baseline is the moment
            # before Save and not the moment before the gesture started.
            y4 = fr.evaluate("window.scrollY")
            fr.locator("div.sadd button", has_text="Save").first.click()
            grew, waited = False, 0.0
            for _ in range(20):
                pg.wait_for_timeout(400); waited += 0.4
                f2 = pg.frame(name="page") or pg.main_frame
                try:
                    if f2.locator(".sapp .lane").count() > n_lane:
                        grew, fr = True, f2; break
                except Exception:
                    continue
            r.step("F7 a typed lane repaints with NO manual reload", grew,
                   f"{n_lane} -> {fr.locator('.sapp .lane').count()} lane rows "
                   f"after {waited:.1f}s")
            r.step("F8 the lane save swapped and kept the reader's place",
                   fr.evaluate("window.__ALIVE2 || 'GONE'") == "yes"
                   and abs(fr.evaluate("window.scrollY") - y4) < 120,
                   f"scroll {round(y4)} -> {round(fr.evaluate('window.scrollY'))}")
        else:
            r.step("F7 a typed lane repaints with NO manual reload", False,
                   "the lane form did not open on double-click")

    # ══ G · THE FLOOR ════════════════════════════════════════════════════
    bare = fr.evaluate("""() => {
      const d = document.cloneNode(true);
      d.querySelectorAll('script').forEach(s => s.remove());
      return d.body.innerText;
    }""")
    r.step("G1 the page still reads with every script deleted", len(bare) > 1500,
           f"{len(bare)} characters of body text", shot=False)
    r.step("G2 a card's panel text is REAL body text, not a tooltip",
           "Clicking these words opens this panel" in bare,
           "counted by the survive-with-JS-stripped check", shot=False)

    pg.set_viewport_size({"width": 420, "height": 900})
    fr, off = open_page(pg, url)
    over = fr.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2")
    r.step("G3 the page does not scroll sideways at 420px", not over,
           f"scrollWidth {fr.evaluate('document.documentElement.scrollWidth')} "
           f"vs {fr.evaluate('window.innerWidth')}")
    pg.set_viewport_size({"width": 1500, "height": 950})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cdp", default="http://127.0.0.1:9222")
    ap.add_argument("--out", default="/tmp/board-drive")
    ap.add_argument("--keep", action="store_true",
                    help="leave the fixture board on disk after the run")
    a = ap.parse_args()

    d, _ = fixture_board.build()
    port = free_port()
    srv = subprocess.Popen(
        [sys.executable, str(HERE.parent / "cli" / "serve.py"),
         "--root", str(d), "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}"
    for _ in range(40):
        try:
            urllib.request.urlopen(f"{base}/board/index.html", timeout=1)
            break
        except Exception:
            time.sleep(0.25)
    else:
        srv.terminate()
        sys.exit("the fixture server never came up")

    print(f"fixture {d}\nserver  {base}\n")
    ok = False
    try:
        with sync_playwright() as pw:
            br = pw.chromium.connect_over_cdp(a.cdp)
            pg = br.contexts[0].new_page()
            pg.set_viewport_size({"width": 1500, "height": 950})
            r = Run(pg, a.out)
            try:
                drive(pg, base, r, d)
            finally:
                ok = r.report()
                print(f"\nrecord: {a.out}/report.md")
                pg.close()
    finally:
        srv.terminate()
        if not a.keep:
            shutil.rmtree(d, ignore_errors=True)
        else:
            print(f"fixture kept at {d}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
