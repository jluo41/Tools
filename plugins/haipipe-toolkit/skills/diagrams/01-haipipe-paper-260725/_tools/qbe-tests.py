#!/usr/bin/env python3
"""Run every test the QBe group's three test sheets promise, and say what failed.

One row per promise, grouped by the page that makes it. Read-only against the
board, the fixture and the MISQ paper: every adapter run writes into a temp dir.

    python3 _tools/qbe-tests.py                # everything except the browser
    python3 _tools/qbe-tests.py --browser      # add the live Chrome pass
    python3 _tools/qbe-tests.py --only QBe3    # one page's sheet

The browser pass drives real Chrome over CDP because the board mounts its page
body in a `srcdoc` iframe: a curl for 200 proves the file is served and proves
nothing about whether a reader can click anything in it.
"""
import argparse, base64, json, pathlib, re, shutil, subprocess, sys, tempfile, time, urllib.request, zipfile

BOARD = pathlib.Path(__file__).resolve().parent.parent
SKILLS = BOARD.parent.parent
ENGINE = SKILLS / "board/haipipe-board"
WORD = SKILLS / "paper/3-deliver/4-ship/haipipe-paper-to-word"
PAPER = (SKILLS.parents[3] /
         "examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026")
# the paper regrouped 0-lifecycle into S01..S10 on 260803; find the page rather
# than hardcode a folder that moves again
SPAGE = next(iter(sorted((PAPER / "0-lifecycle").rglob("S-Main-4-measurement.md"))), None)
SERVE = ("http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/"
         "diagrams/01-haipipe-paper-260725/board")
PAGES = {"QBe1": "QBe/QBe1-sentence-cite-value-display",
         "QBe2": "QBe/QBe2-display-folder-render-caption",
         "QBe3": "QBe/QBe3-content-latex-word-display"}

ROWS = []
def t(group, name, ok, detail=""):
    ROWS.append((group, name, bool(ok), detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {group:6} {name:<44} {detail}")


# ── board level ───────────────────────────────────────────────────────────────
def board_tests():
    print("\nBOARD · the checks that gate every round")
    r = subprocess.run([sys.executable, str(ENGINE / "cli/check.py"), str(BOARD)],
                       capture_output=True, text=True)
    last = r.stdout.strip().split("\n")[-1]
    m = re.search(r"(\d+) pages · (\d+) error · (\d+) warn · (\d+) gap", last)
    t("board", "checker reports zero errors", m and m.group(2) == "0", last)
    t("board", "checker reports zero gaps", m and m.group(4) == "0", "")
    g = subprocess.run([sys.executable, str(ENGINE / "cli/gate.py"), str(BOARD)],
                       capture_output=True, text=True)
    t("board", "gate: no page gained a warning", "gate passes" in g.stdout,
      g.stdout.strip().split("\n")[-1])
    for pid, slug in PAGES.items():
        try:
            code = urllib.request.urlopen(f"{SERVE}/{slug}.html", timeout=5).status
        except Exception as e:
            code = str(e)
        t("board", f"{pid} is served", code == 200, str(code))
    md = (BOARD / "board.md").read_text()
    retired = [f"QBe{s}{l}" for s, ls in (("1", "abcd"), ("2", "abc"), ("3", "abc")) for l in ls]
    missing = [r for r in retired if not re.search(rf"(?m)^{r}\s+_archive/", md)]
    t("board", "every retired face id has an alias", not missing, ",".join(missing))
    stale = subprocess.run(
        ["grep", "-rl", "-e", "QBe1-delivery-sentence", "-e", "QBe2-delivery-display",
         "-e", "QBe3-delivery-section", "-e", "cite-value-table-figure",
         "-e", "section-latex-word-placement", "--include=*.md", str(SKILLS)],
        capture_output=True, text=True).stdout
    stale = [l for l in stale.split("\n") if l and "/board/" not in l and "_archive/" not in l
             and "/_console/" not in l]
    t("board", "no stale page name anywhere", not stale, "; ".join(p.split("/")[-1] for p in stale))


# ── QBe1 · the sentence ───────────────────────────────────────────────────────
def qbe1_tests():
    print("\nQBe1 · the sentence: what its test sheet promises you can click")
    html = (BOARD / "board" / f"{PAGES['QBe1']}.html").read_text()
    chips = re.findall(r'<button type="button" class="chip ([^"]+)"', html)
    t("QBe1", "chips exist in the built HTML", len(chips) >= 20, f"{len(chips)} chips")
    t("QBe1", "resolved at BUILD, not page load", len(chips) > 0,
      "chips are in the static file, no JS needed")
    want = {"cite ok": "a citation that resolves", "cite owed": "a \\cite{TOADD}",
            "cite broken": "a key that resolves to nothing", "num ok": "a value bound to a run",
            "disp tab ok": "a table pointer", "disp fig ready": "a figure pointer",
            "disp fig unowned": "a pointer at no unit"}
    for cls, what in want.items():
        t("QBe1", f"state rendered: {cls}", any(c.startswith(cls) for c in chips), what)
    t("QBe1", "an owed citation is never auto-closed",
      "cite owed" in " ".join(chips) and "TOADD" in html, "the owed marker still ships as owed")
    md = (BOARD / "QBe-delivery-element/QBe1-sentence-cite-value-display.md").read_text()
    s1 = re.search(r"(?ms)^### 1 · .*?(?=^### 2 · )", md).group(0)
    marks = len(re.findall(r"\\cite[p]?\{|\{VAL:\?|\\ref\{", s1))
    t("QBe1", "section 1 carries LIVE markers itself", marks >= 6,
      f"{marks} real markers inside section 1, not a list of where to look")
    fx = BOARD / "_fixture"
    t("QBe1", "the bib a chip resolves against exists", (fx / "misq-slice.bib").exists(),
      f"{len(re.findall('^@', (fx / 'misq-slice.bib').read_text(), re.M))} entries")
    t("QBe1", "the probe entries a bracket resolves to exist",
      any((fx / "1-probes").rglob("QX*.md")),
      f"{len(list((fx / '1-probes').rglob('QX*.md')))} entries")


# ── QBe2 · the display ────────────────────────────────────────────────────────
def qbe2_tests():
    print("\nQBe2 · the display: what its test sheet promises you can open")
    units = sorted((BOARD / "_fixture/displays").glob("display*"))
    t("QBe2", "the fixture carries real units", len(units) >= 2,
      ", ".join(u.name for u in units))
    for u in units:
        have = [p for p in ("float.tex", "assets", "candidates", "preview.pdf", "README.md")
                if (u / p).exists()]
        t("QBe2", f"{u.name[:11]} anatomy", len(have) >= 4, "+".join(have))
        pv = u / "preview.pdf"
        t("QBe2", f"{u.name[:11]} preview is a real PDF",
          pv.exists() and pv.read_bytes()[:4] == b"%PDF" and pv.stat().st_size > 5000,
          f"{pv.stat().st_size // 1024} KB" if pv.exists() else "missing")
        lab = re.findall(r"\\label\{([^}]+)\}", (u / "float.tex").read_text())
        t("QBe2", f"{u.name[:11]} declares a label", bool(lab), ", ".join(lab))
    b = subprocess.run([sys.executable, str(ENGINE / "cli/build.py"), str(BOARD)],
                       capture_output=True, text=True).stdout
    t("QBe2", "the build reports the uncited units", b.count("uncited") >= 2,
      "the live failure section 1 starts from")


# ── QBe3 · the section ────────────────────────────────────────────────────────
def qbe3_tests():
    print("\nQBe3 · the section: what its test sheet promises you can run")
    out = pathlib.Path(tempfile.mkdtemp(prefix="qbe3-"))
    r = subprocess.run([sys.executable, str(WORD / "md2tex.py"), str(SPAGE),
                        "--paper-root", str(PAPER), "-o", str(out)],
                       capture_output=True, text=True)
    tex_p = out / f"{SPAGE.stem}.tex"
    t("QBe3", "md2tex runs and writes a .tex", tex_p.exists(),
      r.stdout.strip().split("\n")[-1] if r.stdout else r.stderr[:60])
    if tex_p.exists():
        tex = tex_p.read_text()
        content = re.search(r"(?ms)^## Content\n(.*?)(?=^## )", SPAGE.read_text()).group(1)
        prose = "\n".join(l for l in content.split("\n") if not l.lstrip().startswith(">"))
        n = lambda p, s: len(re.findall(p, s))
        for label, pat in [("citep", r"\\citep\{"), ("cite{TOADD}", r"\\cite\{TOADD\}"),
                           ("ref", r"\\ref\{"), ("[Q-] brackets", r"\[Q-[A-Za-z0-9-]+\]")]:
            a, b = n(pat, prose), n(pat, tex)
            t("QBe3", f"{label} survives one for one", a == b, f"{a} -> {b}")
        t("QBe3", "board apparatus is dropped",
          "Stage Record" not in tex and "Needs JL" not in tex, "no ### Stage Record, no ### Needs JL")
        t("QBe3", "> lanes are dropped", n(r"(?m)^> ", tex) == 0,
          f"{n(r'(?m)^> ', content)} in the source")
        ins = n(r"(?m)^\\input\{displays", tex)
        t("QBe3", "floats inserted after first reference", ins >= 1,
          f"{n(r'input.displays', prose)} in the prose -> {ins} in the .tex")
        t("QBe3", "headings become section and subsection",
          n(r"(?m)^\\section\{", tex) == 1 and n(r"(?m)^\\subsection\{", tex) >= 3,
          f"1 section + {n(r'(?m)^.subsection.', tex)} subsections")
        # REFUSE TO REGRESS: strip a citation, run again over the same output
        deg = out / "degraded.md"
        deg.write_text(SPAGE.read_text().replace("\\citep{cms_nppes}", "", 1))
        shutil.copy(tex_p, out / f"{deg.stem}.tex")
        r2 = subprocess.run([sys.executable, str(WORD / "md2tex.py"), str(deg),
                             "--paper-root", str(PAPER), "-o", str(out)],
                            capture_output=True, text=True)
        blob = (r2.stdout + r2.stderr).lower()
        t("QBe3", "refuses a regression in citations",
          "refus" in blob or "fewer" in blob or r2.returncode != 0,
          (r2.stdout + r2.stderr).strip().split("\n")[-1][:70])

    docx = out / "s4.docx"
    r3 = subprocess.run([sys.executable, str(WORD / "md2docx.py"), str(SPAGE),
                         "-o", str(docx), "--paper-root", str(PAPER)],
                        capture_output=True, text=True)
    t("QBe3", "md2docx runs and writes a .docx", docx.exists(),
      r3.stdout.strip().split("\n")[1].strip() if docx.exists() else r3.stderr[:60])
    if docx.exists():
        z = zipfile.ZipFile(docx)
        doc = z.read("word/document.xml").decode()
        com = z.read("word/comments.xml").decode() if "word/comments.xml" in z.namelist() else ""
        nc = len(re.findall(r"<w:comment ", com))
        t("QBe3", "the .docx opens as a zip with the parts",
          {"word/document.xml", "word/styles.xml"} <= set(z.namelist()), f"{len(z.namelist())} parts")
        t("QBe3", "apparatus rides in anchored comments", nc >= 5,
          f"{nc} comments, {len(re.findall('<w:commentRangeStart', doc))} anchors")
        t("QBe3", "every comment is authored haipipe",
          set(re.findall(r'w:author="([^"]+)"', com)) == {"haipipe"},
          ", ".join(sorted(set(re.findall(r'w:author="([^"]+)"', com)))))
        t("QBe3", "a display asset is embedded",
          any(n.startswith("word/media/") for n in z.namelist()),
          f"{len([n for n in z.namelist() if n.startswith('word/media/')])} media file(s)")
        t("QBe3", "it warns that an owed citation shipped",
          "owed-citation" in r3.stdout, "the exporter raises it itself")
    t("QBe3", "build-both.sh exists for the round trip", (WORD / "build-both.sh").exists(),
      "runs both adapters on one page")
    # the placement trace, on the live paper
    master = (PAPER / "Personality-Opioid-MISQ2026.tex").read_text()
    cites, defs, reached = {}, set(), []
    def walk(rel):
        f = PAPER / (rel if rel.endswith(".tex") else rel + ".tex")
        if not f.exists():
            reached.append((rel, False)); return
        reached.append((rel, True)); s = f.read_text()
        for l in re.findall(r"\\ref\{([^}]+)\}", s): cites.setdefault(l, []).append(rel)
        defs.update(re.findall(r"\\label\{([^}]+)\}", s))
        for inc in re.findall(r"\\input\{([^}]+)\}", s): walk(inc)
    for rel in re.findall(r"\\input\{([^}]+)\}", master): walk(rel)
    dead = [l for l in cites if l not in defs]
    t("QBe3", "the placement trace runs", bool(cites),
      f"{len(cites)} labels cited, {len(cites) - len(dead)} resolve, {len(dead)} compile to ??")
    t("QBe3", "no input names a missing file", all(ok for _, ok in reached),
      ", ".join(r for r, ok in reached if not ok) or "all inputs resolve")
    shutil.rmtree(out, ignore_errors=True)


# ── the browser pass ──────────────────────────────────────────────────────────
def browser_tests():
    """A REAL mouse, not element.click(): board.js records that the shortcut hid a
    bug where every chip was unreachable, so the click has to be hit-tested."""
    print("\nBROWSER · real Chrome, real mouse events, folds opened by clicking")
    try:
        import websocket
    except ImportError:
        t("browser", "websocket-client available", False, "pip install websocket-client"); return
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    prof = tempfile.mkdtemp(prefix="qbe-chrome-")
    # a fixed port lets two runs attach to each other's browser and report the wrong
    # page as passing; take a free one instead (found the hard way, 260803)
    import socket
    with socket.socket() as sk:
        sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]
    proc = subprocess.Popen([chrome, "--headless=new", f"--remote-debugging-port={port}",
                             f"--user-data-dir={prof}", "--window-size=1440,900",
                             "--no-first-run", "--disable-gpu", "--remote-allow-origins=*",
                             "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    page = None
    for _ in range(60):
        try:
            page = next(x for x in json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
                        if x["type"] == "page"); break
        except Exception:
            time.sleep(0.4)
    if not page:
        t("browser", "chrome starts", False, "no debugging target"); return
    ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=40, suppress_origin=True)
    ident, errs = [0], []
    def cmd(m, **kw):
        ident[0] += 1
        ws.send(json.dumps({"id": ident[0], "method": m, "params": kw}))
        while True:
            r = json.loads(ws.recv())
            if r.get("method") == "Log.entryAdded" and r["params"]["entry"]["level"] == "error":
                errs.append(r["params"]["entry"]["text"][:80])
            if r.get("id") == ident[0]:
                return r.get("result", {})
    def ev(e):
        return cmd("Runtime.evaluate", expression=e, returnByValue=True).get("result", {}).get("value")
    def mouse(x, y):
        for typ in ("mousePressed", "mouseReleased"):
            cmd("Input.dispatchMouseEvent", type=typ, x=x, y=y, button="left", clickCount=1)
            time.sleep(0.12)
        time.sleep(0.4)
    cmd("Page.enable"); cmd("Runtime.enable"); cmd("Log.enable")
    FR = ("[...document.querySelectorAll('iframe')].map(function(f){try{return f.contentDocument?f:null}"
          "catch(e){return null}}).filter(Boolean).find(function(f){return f.contentDocument"
          ".querySelector('summary')})")
    shots = BOARD / "_tools/shots"; shots.mkdir(exist_ok=True)
    for pid, slug in PAGES.items():
        errs.clear()
        cmd("Page.navigate", url=f"{SERVE}/{slug}.html"); time.sleep(3.2)
        # a reader opens the folds by CLICKING them, which is what makes a chip hittable
        for _ in range(40):
            g = ev("(function(){var fr=" + FR + ";var d=fr.contentDocument,fb=fr.getBoundingClientRect();"
                   "var s=[].find.call(d.querySelectorAll('summary'),function(x){"
                   "  return !x.closest('details').open && x.getBoundingClientRect().height>0;});"
                   "if(!s) return null; s.scrollIntoView({block:'center'});"
                   "var r=s.getBoundingClientRect();"
                   "if(r.top<0||r.bottom>fr.contentWindow.innerHeight) return {skip:true};"
                   "return {x:fb.left+r.left+30, y:fb.top+r.top+r.height/2}})()")
            if not g or g.get("skip"):
                break
            mouse(g["x"], g["y"])
        opened = ev("(function(){var fr=" + FR + ";var d=fr.contentDocument;"
                    "return [].filter.call(d.querySelectorAll('details'),function(x){return x.open}).length"
                    "+'/'+d.querySelectorAll('details').length})()")
        info = ev("(function(){var fr=" + FR + ";var d=fr.contentDocument;"
                  "var all=[document].concat([].map.call(document.querySelectorAll('iframe'),function(f){"
                  "  try{return f.contentDocument}catch(e){return null}})).filter(Boolean);"
                  "var h=d.querySelector('h1')||document.querySelector('h1');"
                  "return {h1:((h&&h.textContent)||document.title||'').trim(),"
                  " chips:d.querySelectorAll('button.chip').length,"
                  " nav:all.some(function(x){return x.body&&x.body.innerHTML.indexOf('Index')>=0})}})()")
        t("browser", f"{pid} renders its title", bool(info and info["h1"]), (info or {}).get("h1", "")[:48])
        t("browser", f"{pid} shows its board nav", bool(info and info["nav"]), f"folds opened {opened}")
        t("browser", f"{pid} has no console error", not errs, "; ".join(errs) or "clean")
        n = info["chips"]
        if n:
            good = bad = 0
            first = ""
            for k in range(n):
                g = ev("(function(){var fr=" + FR + ";var d=fr.contentDocument,w=fr.contentWindow;"
                       "[].forEach.call(d.querySelectorAll('[popover]'),function(x){"
                       "  if(x.matches(':popover-open')&&x.hidePopover)x.hidePopover()});"
                       f"var c=d.querySelectorAll('button.chip')[{k}];"
                       "var r0=c.getBoundingClientRect();"
                       "w.scrollTo(0,w.scrollY+r0.top-Math.round(w.innerHeight/2));"
                       "var r=c.getBoundingClientRect(),fb=fr.getBoundingClientRect();"
                       "var hit=d.elementFromPoint(r.left+r.width/2,r.top+r.height/2);"
                       "return {x:fb.left+r.left+r.width/2,y:fb.top+r.top+r.height/2,"
                       " onChip:(hit===c||c.contains(hit)),cls:c.className.replace('chip ','')}})()")
                if not g or not g["onChip"]:
                    bad += 1; continue
                mouse(g["x"], g["y"])
                r = ev("(function(){var fr=" + FR + ";var d=fr.contentDocument,w=fr.contentWindow;"
                       "var o=[].filter.call(d.querySelectorAll('[popover]'),function(x){return x.matches(':popover-open')});"
                       "if(!o.length) return null;"
                       "var b=o[0].getBoundingClientRect();"
                       "var vis=Math.max(0,Math.min(b.bottom,w.innerHeight)-Math.max(b.top,0));"
                       "return {pct:Math.round(100*vis/Math.max(b.height,1)),txt:o[0].textContent.trim().slice(0,40)}})()")
                if r and r["pct"] >= 60:
                    good += 1
                    first = first or r["txt"]
                else:
                    bad += 1
            t("browser", f"{pid} every chip opens under a real mouse", bad == 0 and good == n,
              f"{good}/{n} opened, first: {first[:38]}")
        d = cmd("Page.captureScreenshot", format="png")
        (shots / f"{pid}.png").write_bytes(base64.b64decode(d["data"]))
    ws.close(); proc.terminate(); shutil.rmtree(prof, ignore_errors=True)
    print(f"  screenshots -> {shots}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--browser", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    run = {"board": board_tests, "QBe1": qbe1_tests, "QBe2": qbe2_tests, "QBe3": qbe3_tests}
    for k, f in run.items():
        if not a.only or a.only == k:
            f()
    if a.browser and (not a.only or a.only == "browser"):
        browser_tests()
    bad = [r for r in ROWS if not r[2]]
    print(f"\n{'=' * 72}\n{len(ROWS) - len(bad)}/{len(ROWS)} pass")
    for g, n, _, d in bad:
        print(f"  FAIL  {g:6} {n}  {d}")
    sys.exit(1 if bad else 0)
