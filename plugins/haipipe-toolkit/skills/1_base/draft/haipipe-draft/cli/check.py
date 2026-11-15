#!/usr/bin/env python3
"""check.py — the mechanical structural check for one board.

This command checks the parts of a Board/Page contract that are decidable by
machine. A fresh Page CHECK read remains a separate semantic judgement; this
file never claims to replace it.

What it does NOT do, and cannot:
  · judge whether the prose is readable — that is the cold read
  · judge whether a page's claims about the code are TRUE. On 2026-07-26 a page
    said the drawer AI had comments "injected into its system prompt"; the
    markdown was flawless, every construct rendered, and the sentence was simply
    false for three days. A structural pass is fully compatible with a page that
    is confidently wrong.

Three families:
  BOARD     board.md: Pages against disk, declared Links resolve, ids unique
  PAGE      each Q*/S* md: required sections, state value, references resolve,
            one sentence per line, no em-dash, English-only
  SITE      the built board/ tree: local links and media resolve, tags balance,
            ids unique
  TEMPLATE  render ref/page-template.md as a Q and as an S, then assert each
            construct named by the current contract produces its class. A
            construct the template never exercises is reported as a GAP, not
            skipped.

Shares the renderer's section aliases, state tokens, and page discovery helpers
from src/common.py. The checker keeps independent structural assertions because
its job is to compare the documented contract with what the renderer accepts.

Report-only by default, exit 0. `--strict` exits 1 on any ERROR. The Page
workflow decides whether a finding blocks a handoff; this command only reports
the mechanical result.

    python3 check.py <board-dir> [--strict] [--quiet]
"""
import argparse
import collections
import os
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


from urllib.parse import unquote

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))
from src.common import board_kind  # noqa: E402
from src.dialect_task_block import mounted_info  # noqa: E402
from src.parse import parse_dir  # noqa: E402
from src.topic_entry_contract import check_topic_entries  # noqa: E402

# The checks live in four modules beside this file; main() runs them in order.
#   cli/check_common.py      shared helpers and the levels ERROR, WARN, GAP
#   cli/check_board_face.py  board.md and each Page face (check_board, check_face, check_opening)
#   cli/check_page_text.py   one Page's sections, sentences, files and comments
#   cli/check_families.py    design, insight and partition checks, check_workbench_roster
from cli.check_common import (ERROR, GAP, SEMANTIC_SECTION_PAGE, WARN,  # noqa: E402
                              outside_checkout)
from cli.check_board_face import check_board, check_face, check_mounted_page  # noqa: E402
from cli.check_families import (check_design_family, check_insight_family,  # noqa: E402
                                check_workbench_roster)
# Re-export: every name that moved out stays importable as cli.check.<name>.
from cli.check_common import *  # noqa: E402,F401,F403
from cli.check_page_text import *  # noqa: E402,F401,F403
from cli.check_families import *  # noqa: E402,F401,F403
from cli.check_board_face import *  # noqa: E402,F401,F403

# The generated Board site can link to live server routes. They do not resolve
# as files beside an HTML page, so checker must recognize them rather than
# calling the Board Home navigation a dead static href.
LIVE_ROUTE_PREFIXES = ("/_board/", "/_excalidraw", "/boards")

# The construct table: source form -> the class the renderer must produce.
# Kept in this order so the report reads like the table on that page.
CONSTRUCTS = [
    ("lead is the door",     "details.it.row.qd",  r'<details class="it row qd"', r"^## (?:Opening|Question)\s*$"),
    ("Opening never folds",  "div.ch.opening-head", r'class="ch opening-head"',   r"^## (?:Opening|Question)\s*$"),
    ("drawer is flat",       "div.fh",             r'<div class="fh"',            r"^\*\*(?:Where this Page sits|Why it matters):"),
    ("division",             "details.csec",       r'<details class="csec"',      r"^### "),
    ("paragraph heading",    "div.ph",             r'<div class="ph"',            r"^#### "),
    ("job line",             "div.pj",             r'<div class="pj"',            r"^\([^)]+\)\s*$"),
    ("group title",          "div.gt > span.gi",   r'<div class="gt"',            r"(?m)^\*\*[^*\n]+\*\*\s*\n[-*] "),
    ("sentence apparatus",   "details.sent",       r'<details class="sent"',      r"^> (?:Citation|Value|Display|Supporting Run|Check|Q-consumer|Link|Source|Note):"),
    ("sentence badge",       "span.sbadge",        r'class="sbadge"',             r"^> (?:Citation|Value|Display|Supporting Run|Check|Q-consumer|Link|Source|Note):"),
    ("typed lane",           "div.lane",           r'<div class="lane"',          r"^> (?:Citation|Value|Display|Supporting Run|Check|Q-consumer|Link|Source|Note):"),
    ("item with detail",     "details.it.row",     r'<details class="it row"',    r"(?m)^- (?:\[[ xX]\] )?.+\n {2,}\S"),
    ("aim count",            "n/m in the heading", r'\d+/\d+',
     r"(?m)^-\s+(?:⬜|🔨|🧠|✅|❄️|🟡|🟠|⏸️)\s+(?:A\d+(?:\.\d+)*|P\d+(?:\.\d+)*)\s+·"),
    ("dated item",           "span.stmp",          r'class="stmp"',               r"^(?:- )?\d{6}(?: \d{4})? "),
    ("ASCII diagram",        "pre.asc",            r'<pre class="asc"',           r"^```(?:text|txt|plain|ascii|diagram)\s*$"),
    ("code block",           "details.codef",      r'<details class="it codef"',
     r"^```(?!(?:text|txt|plain|ascii|diagram)\s*$)[A-Za-z0-9_+-]+\s*$"),
]


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, code, where, msg):
        self.rows.append((level, code, where, msg))

    def counts(self):
        c = {}
        for level, *_ in self.rows:
            c[level] = c.get(level, 0) + 1
        return c


def check_draw_folders(d, rep):
    """Every draw/ holds exactly what its owner may own (QPf2's contract).

    A folded page's studio/draw/ holds that page's own scene(s), named by the
    page id the folder name starts with; a group's draw/ holds group.excalidraw.
    A flat legacy Page may share that Group draw/. Anything else is a STRAY —
    the trace an archive or merge leaves behind (found
    260816: QPf2a's stub sat in QPf2's draw/ for a day, and Design-7/8's
    scenes hid in Design-6's). Underscore entries (_retired, _archive) are a
    person's deliberate parking and stay unjudged; the generated board/ site
    is not source and is skipped.
    """
    for draw in sorted(d.rglob("draw")):
        if not draw.is_dir():
            continue
        parts = draw.relative_to(d).parts
        if "board" in parts or any(p.startswith("_") for p in parts):
            continue
        page = draw.parent.parent if draw.parent.name == "studio" else draw.parent
        is_page = (page / f"{page.name}.md").is_file()
        for f in sorted(draw.iterdir()):
            if f.name.startswith("_") or (f.name == "assets" and f.is_dir()):
                continue
            where = str(f.relative_to(d))
            if f.suffix != ".excalidraw":
                rep.add(WARN, "stray-in-draw", where,
                        "not a scene; draw/ holds scenes, assets/, and _parked")
                continue
            ok = (f.name == "group.excalidraw") if not is_page else \
                (page.name == f.stem or page.name.startswith(f.stem + "-"))
            if not ok:
                rep.add(WARN, "stray-scene", where,
                        f"scene stem does not name this {'page' if is_page else 'group'}"
                        " — a leftover from an archive or merge?")


def check_page(d, rep):
    """The built site: local hrefs resolve, tags balance, ids are unique.

    Checks the split site (QC9). The monolithic board.html was retired 260731,
    so every page is now its own file and each one is checked on its own terms:
    a broken link on QD2 used to be one finding among thousands in a 1.1MB
    document, and is now named by the file it is in.
    """
    site = d / "board"
    if not (site / "index.html").exists():
        # No site is the normal state (JL 261004): the workbench reads every Page live and
        # the static site is retired. A site still on disk (Labeling's) is checked below.
        return

    # A stale build is indistinguishable from link rot in this report: on 260829
    # a 9-day-old render shipped 184 dead-href ERRORs that a rebuild took to 0,
    # because the site still pointed at page-types deleted upstream. Say so
    # first, so nobody debugs the sources for a finding the build owns.
    built = (site / "index.html").stat().st_mtime
    # 260907: a dangling symlink inside an archived page (a link that follows
    # a page that was renamed) must not crash the whole checker; skip it here,
    # dead-href reporting owns broken links.
    newer = [f for f in d.rglob("*.md")
             if "/board/" not in f.as_posix() and f.exists() and f.stat().st_mtime > built]
    if newer:
        rep.add(WARN, "board-build-stale", "board/index.html",
                f"{len(newer)} source .md newer than the render "
                f"(e.g. {newer[0].relative_to(d).as_posix()}); run build.py before "
                f"trusting dead-href or completeness findings")

    pages = sorted(site.glob("*.html")) + sorted(site.glob("*/*.html"))

    for html in pages:
        name = html.relative_to(site).as_posix()
        t = html.read_text(encoding="utf-8")
        bare = re.sub(r"<script.*?</script>", "", t, flags=re.S)
        body = bare.split("<body", 1)[-1]

        # Scripts-off completeness, on the page files only: a group file and the
        # index are navigation, so they are legitimately short.
        if html.parent != site:
            plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
            if len(plain) < 400:
                rep.add(ERROR, "zero-script", name,
                        f"only {len(plain)} chars survive with scripts stripped; "
                        "the page depends on JS")

        # `bare`, not `t`: a URL inside JavaScript is a string in a program,
        # not a rendered resource. Check href, img/iframe src, and object data
        # together: the split-site reroot bug fixed href while leaving the
        # evidence-card image and PDF visibly broken (260801).
        resources = sorted(set(re.findall(
            r'(href|src|data)="([^"#][^"]*)"', bare)))
        for attr, href in resources:
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href):
                continue
            if href.startswith(LIVE_ROUTE_PREFIXES):
                continue
            href = href.split("#", 1)[0].split("?", 1)[0]
            if not href:
                continue
            # A rendered href is URL-ENCODED and a filesystem path is not, so
            # `fig/image copy.png` ships as `fig/image%20copy.png` and this
            # check called a file that exists a dead link (found 260801, on a
            # figure pasted into board.md with a space in its name).
            href = unquote(href)
            if not (html.parent / href).exists():
                if outside_checkout(html.parent, href):
                    rep.add(WARN, "outside-checkout", f"{name} -> {href}",
                            f"rendered {attr} target lives outside this checkout")
                else:
                    rep.add(ERROR, f"dead-{attr}", f"{name} -> {href}",
                            f"rendered {attr} does not resolve")

        ids = re.findall(r'id="([^"]+)"', t)
        for fragment in sorted(set(re.findall(r'href="#([^"]+)"', bare))):
            if fragment not in ids:
                rep.add(ERROR, "dead-fragment", f"{name} -> #{fragment}",
                        "rendered fragment does not exist in this file")
        for i in sorted({x for x in ids if ids.count(x) > 1}):
            rep.add(ERROR, "duplicate-html-id", f"{name} #{i}",
                    f"id appears {ids.count(i)} times")

        # An anchor or button INSIDE a navigation row. A row is one link, and a
        # browser closes the outer `<a>` when a second one opens, so the row
        # stops navigating. The renderer now strips these (`body.nav_inline`),
        # and this is the rule that says so out loud if they return by another
        # path: a path in backticks inside a `###` heading put one in the
        # sidebar, which is copied onto every page and never rerooted, and one
        # heading on QE5 shipped 66 dead-href ERRORs across the built tree.
        for cls, inner in re.findall(
                r'<a class="(sb-p|sb-ss|sb-g|ir)[^"]*"[^>]*>(.*?)</a>', bare, re.S):
            bad = re.search(r"<(a|button)\s", inner)
            if bad:
                rep.add(ERROR, "nested-anchor", f"{name} · .{cls}",
                        f"a <{bad.group(1)}> inside a nav row; the row stops "
                        "navigating and its href is never rerooted")
                break          # one per page: the sidebar repeats on all of them

        # Tag balance, counted outside <script> AND <style>. Both quote markup
        # in their comments: board.css explains the apparatus with the words
        # "native <details>", and counting that reported three unclosed tags on
        # a page whose markup was fine.
        markup = re.sub(r"<style.*?</style>", "", bare, flags=re.S)
        for tag in ("details", "section", "div"):
            o = len(re.findall(rf"<{tag}[\s>]", markup))
            c = len(re.findall(rf"</{tag}>", markup))
            if o != c:
                rep.add(ERROR, "unbalanced-tag", name,
                        f"<{tag}> opened {o} times, closed {c}")


# Every class token a chip PANEL carries. A panel's class list is
# `chipcard <kind> <state>`, so each of these is a live class on a top-layer
# element, and a bare `.<token>{}` rule anywhere in board.css also styles the
# panel. That is not hypothetical: `.fig`, written for markdown images, matched
# every figure panel and its `display:block` beat the UA rule that hides a
# closed popover, so five invisible full-width panels lay across the page and
# swallowed every click for a day during the early Board renderer work (JL 260726).
# `chipcard` itself is NOT in the list: styling the panel's own base class
# bare is the correct way to style a panel. The danger is the OTHER tokens,
# which are kind and state words a page might plausibly want for something else.
PANEL_TOKENS = ("disp", "fig", "tab", "num", "val", "cite", "qref",
                "ok", "ready", "owed", "parked", "broken", "unowned", "unver", "amb")
BARE_CLASS = re.compile(r"(?m)^\s*((?:\.[A-Za-z][\w-]*\s*,\s*)*\.([A-Za-z][\w-]*))\s*\{")


def check_css(rep):
    """A bare class selector that collides with a chip panel's own classes.

    The failure this catches renders perfectly and reads perfectly: the page is
    correct, the prose is correct, and the interaction is dead. A structural
    report must catch this directly because neither prose review nor a normal
    link scan can see a hidden panel collision.
    """
    from src import assets as _a
    for m in BARE_CLASS.finditer(_a.css()):
        for sel in m.group(1).split(","):
            tok = sel.strip().lstrip(".")
            if tok in PANEL_TOKENS:
                line = css.read_text(encoding="utf-8").count("\n", 0, m.start()) + 1
                rep.add(ERROR, "panel-class-collision", f"assets/board.css:{line}",
                        f"bare `.{tok}` also matches a chip panel "
                        f"(class=\"chipcard <kind> <state>\"); scope it to a tag "
                        f"or rename it, or it can un-hide a closed popover")


def check_template(rep, quiet):
    """Render ref/page-template.md as a Q page and as an S page, then assert.

    The template is the fixture because it is the file authors copy. Checking a
    hand-written specimen would let the template rot while the specimen passed.
    """
    tpl = HERE / "ref" / "page-template.md"
    if not tpl.exists():
        rep.add(ERROR, "no-template", "ref/page-template.md", "the fixture is missing")
        return
    src = tpl.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "fixture"
        d.mkdir()
        (d / "board.md").write_text(
            "# Template fixture\nspine: render the template and assert every construct\n"
            "close: never\n## Topic\nFixture.\n## Pages\n### QT · Fixture\n"
            "QT1-template.md\nS-Main-1-template.md\n", encoding="utf-8")
        (d / "QT1-template.md").write_text(src, encoding="utf-8")
        s_src = re.sub(r"^# .*$", "# S Main 1 · Fixture", src, count=1, flags=re.M)
        (d / "S-Main-1-template.md").write_text(s_src, encoding="utf-8")

        builder = HERE / "cli" / "build.py"
        if not builder.is_file():
            # The static Board site and its builder are retired (haipipe-block 2.0.0, JL 261005):
            # a Board is read live in the workbench, so there is no build to compare with the
            # template. Without this the check reported template-build-failed on every Block.
            return
        r = subprocess.run([sys.executable, str(builder), str(d)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            rep.add(ERROR, "template-build-failed", "ref/page-template.md",
                    (r.stderr or r.stdout).strip().split("\n")[-1][:200])
            return
        # One document per page since the monolith was retired (260731). The
        # construct assertions below only ask "does this markup appear
        # somewhere", so concatenating the page files is the same question, and
        # page_slice still finds its own section boundaries inside the join.
        html = "\n".join(p.read_text(encoding="utf-8")
                         for p in sorted((d / "board").glob("*/*.html")))

        # Guide comments describe optional shapes but are not authored Page
        # content. Do not let their example list items trigger renderer drift
        # errors for the reader-facing template fixture.
        source_body = re.sub(r"<!--.*?-->", "", src, flags=re.S)
        for label, cls, pattern, source_pattern in CONSTRUCTS:
            source_has = bool(re.search(source_pattern, source_body, re.M))
            rendered_has = bool(re.search(pattern, html))
            if not source_has:
                rep.add(GAP, "template-gap", f"ref/page-template.md · {label}",
                        f"the template source never exercises {cls}, so the construct is "
                        "documented and untested")
            elif not rendered_has:
                rep.add(ERROR, "template-renderer-drift", f"ref/page-template.md · {label}",
                        f"the template exercises this construct but the rendered fixture has no {cls}")

        if 'class="slide q' not in html:
            rep.add(ERROR, "template-no-page", "ref/page-template.md", "rendered to no page at all")
        if html.count('class="slide q') < 2:
            rep.add(ERROR, "template-one-mode", "ref/page-template.md",
                    "the fixture did not render as both a Q page and an S page")

        def page_slice(page_id):
            marker = f'id="{page_id}"'
            at = html.find(marker)
            if at < 0:
                return ""
            start = html.rfind('<section class="slide q', 0, at)
            end = html.find('<section class="slide q', at + len(marker))
            return html[start:end if end >= 0 else len(html)]

        q_html = page_slice("QT1")
        s_html = page_slice("S-Main-1")
        mode_checks = [
            ("Q rationale in Opening", q_html, r'<div class="fh">More details</div>'),
            ("Q has no Stage Contract drawer", q_html, r"^(?![\s\S]*<div class=\"fh\">Stage Contract</div>)[\s\S]*$"),
            ("Q Content heading stays plain", q_html, r"📚 Content(?!\s*·)"),
            ("S rationale in Opening", s_html, r'<div class="fh">More details</div>'),
            ("S has no Stage Contract drawer", s_html,
             r"^(?![\s\S]*<div class=\"fh\">Stage Contract</div>)[\s\S]*$"),
            ("S Content heading names the stage", s_html, r"📚 Content · Main 1 Fixture"),
        ]
        for label, page_html, pattern in mode_checks:
            if not page_html or not re.search(pattern, page_html):
                rep.add(ERROR, "template-mode-contract", f"ref/page-template.md · {label}",
                        "the shared source did not render with the documented Q/S-specific placement")


def print_rules():
    """The rulebook, derived from this file's own rep.add calls.

    The 260828 field test found the checker's laws teachable only through
    error text, discovered after writing (friction F11). This prints every
    finding code with its message template BEFORE anyone writes, from the
    same source the findings come from, so the roster cannot drift.
    """
    # The checks live in this file and its sibling modules; read them all, in the
    # order the code once sat in one file, so each code keeps its first message.
    src = "\n".join(Path(__file__).with_name(f).read_text(encoding="utf-8") for f in (
        "check_board_face.py", "check_page_text.py", "check.py", "check_families.py"))
    rules = {}
    for m in re.finditer(r'rep\.add\(\s*(ERROR|WARN|GAP),\s*"([a-z0-9-]+)"', src):
        level, code = m.group(1), m.group(2)
        # the call text: balance parens from the match to its closing one
        depth, i = 0, m.start()
        while i < len(src):
            if src[i] == "(":
                depth += 1
            elif src[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        call = src[m.start():i]
        literals = re.findall(r'"((?:[^"\\]|\\.)*)"', call)[1:]  # drop the code itself
        msg = " ".join(s for s in literals
                       if len(re.sub(r"\{[^}]*\}", "", s).split()) >= 2)
        entry = rules.setdefault((level, code), {"msg": msg, "sites": 0})
        entry["sites"] += 1
        if not entry["msg"]:
            entry["msg"] = msg
    order = {ERROR: 0, WARN: 1, GAP: 2}
    print(f"{len(rules)} finding codes, derived from this file's rep.add calls\n")
    for (level, code), e in sorted(rules.items(), key=lambda kv: (order[kv[0][0]], kv[0][1])):
        sites = f" ({e['sites']} sites)" if e["sites"] > 1 else ""
        print(f"{level:<6} {code:<26} {e['msg'] or '(message is fully computed)'}{sites}")


def main():
    ap = argparse.ArgumentParser(description="mechanical structural check")
    ap.add_argument("board", nargs="?", help="the board folder")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any ERROR (JL's ruling on blocking is open; default reports)")
    ap.add_argument("--quiet", action="store_true", help="findings only, no summary")
    ap.add_argument("--no-template", action="store_true",
                    help="skip the template fixture (it shells out to build.py)")
    ap.add_argument("--summary", action="store_true",
                    help="score instead of a list: findings per rule and the "
                         "worst pages, so 'how are we doing' is one command")
    ap.add_argument("--rules", action="store_true",
                    help="print every finding code and its message, no board "
                         "needed: the laws, readable before writing")
    a = ap.parse_args()

    if a.rules:
        print_rules()
        return 0
    if not a.board:
        ap.error("a board folder is required unless --rules")

    d = Path(a.board).resolve()
    rep = Report()
    pages, links, decision_only = check_board(d, rep)
    page_ids = set()
    _parsed_meta, parsed_pages, _parsed_warnings = parse_dir(d)
    page_ids.update(page["id"] for page in parsed_pages if page.get("id"))
    for name in pages:
        m = re.match(r"([QS][A-Za-z0-9]*\d+[a-z]?)", name)
        if m:
            page_ids.add(m.group(1))
        elif SEMANTIC_SECTION_PAGE.fullmatch(name):
            page_ids.add(Path(name).stem)
    mounted_ids = {}
    for name, p in sorted(pages.items()):
        if board_kind(d) not in {"task-block", "discovery-block"} and mounted_info(d, p):
            check_mounted_page(d, p, name, rep, mounted_ids)
            continue
        check_face(p, name, rep, links, page_ids, decision_only)
    check_topic_entries(d, pages, rep)
    check_draw_folders(d, rep)
    check_design_family(d, rep)
    check_insight_family(d, rep)
    check_workbench_roster(d, rep)
    check_page(d, rep)
    check_css(rep)
    if not a.no_template:
        check_template(rep, a.quiet)

    order = {ERROR: 0, WARN: 1, GAP: 2}
    if a.summary:
        # The findings ARE the measurement (QB4 §9). A list of 285 rows says
        # nothing about whether the board is improving; a count per rule and a
        # worst-pages column does, and a page at zero is the one to copy.
        import collections
        by_code, by_page = collections.Counter(), collections.Counter()
        for level, code, where, _ in rep.rows:
            by_code[(level, code)] += 1
            by_page[where.split(" ·")[0].split(" ->")[0]] += 1
        print(f"{len(pages)} pages · {len(rep.rows)} findings\n")
        print(f"{'rule':<26} {'level':<6} {'count':>6}")
        print("-" * 40)
        for (level, code), n in sorted(by_code.items(), key=lambda x: -x[1]):
            print(f"{code:<26} {level:<6} {n:>6}")
        clean = [n for n in sorted(pages) if not by_page.get(n)]
        print(f"\n{'page':<40} {'findings':>8}")
        print("-" * 50)
        for name, n in by_page.most_common(8):
            print(f"{name:<40} {n:>8}")
        print(f"\nclean pages: {len(clean)} of {len(pages)}")
        if clean:
            print("  " + " · ".join(clean[:8]) + ("  …" if len(clean) > 8 else ""))
        return 1 if (a.strict and rep.counts().get(ERROR)) else 0
    for level, code, where, msg in sorted(rep.rows, key=lambda r: (order[r[0]], r[1], r[2])):
        print(f"{where:<44} {level:<5} {code:<24} {msg}")

    c = rep.counts()
    if not a.quiet:
        print(f"\n{len(pages)} pages · "
              f"{c.get(ERROR, 0)} error · {c.get(WARN, 0)} warn · {c.get(GAP, 0)} gap")
        if not rep.rows:
            print("nothing structural to report. The cold read is the other half; "
                  "this says nothing about whether the page can be read.")
    return 1 if (a.strict and c.get(ERROR)) else 0


if __name__ == "__main__":
    sys.exit(main())
