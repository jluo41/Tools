"""🔗 Pagex · the page's citations into the repo's OTHER PAGES (QPf11).

THE THIRD CITATION TWIN (JL 260816: "我们在生成一个新 pages 的时候，可能需要
引用其他几个 pages 的内容来 build … 不是 all-in-one，按需引用 … 可以用软链接
的方法把那些内容给弄出来"). BibEx holds a page's references into the
literature, skill into the skill tree, and pagex into the repo's page tree.

  BORROWED BY THE FILE      one deck, one float, one skill list — never a
                            whole page folder, and never a page's HOME dir,
                            which would satisfy `_page_home` and hand
                            discovery a ghost page
  MATERIALIZED AS SYMLINKS  a copy ages the moment the source moves; a link
                            stays current, and when the source is renamed the
                            link breaks VISIBLY as ⚠ dangling
  THE STORE IS THE TRUTH    pagex/<stem>.md is PRIMARY and ranked; the links
                            and the card view are re-minted from it, and a
                            refresh never edits a row a person wrote
  THE SCAN SEEDS            a refresh reads the page ids this page's prose
                            already writes and borrows those pages, appending
                            at the BOTTOM; the person ranks and ✕s, and the
                            ＋-by-path pen is for depth, not for the common
                            case (JL 260816: "it should not be manually
                            added")
"""
import os
import re
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, quote as _q, urlparse

from live.export import _VIEW, _esc

# One row of the store, diff-friendly like the skill map's:
#   - <repo-relative path> · note: free text     (order in the file IS the rank)
#   - <repo-relative path> · removed             (the ✕ tombstone)
_ROW = re.compile(r"^- (?P<path>\S+)"
                  r"(?P<removed> · removed)?"
                  r"(?: · note: (?P<note>.*))?\s*$")

# A page id as prose writes it: QPf11, QA00, QBt3, QPs1, S-Main-4.
_PID = re.compile(r"(?<![\w-])(Q[A-Za-z]{0,3}\d{1,3}[a-z]?|S-[A-Z][a-z]+-\w+)"
                  r"(?![\w-])")

_STORE_HEAD = """# pagex · %s
<!-- PRIMARY: the files this page borrows from other pages (haipipe-plugin).
     The ORDER is the person's rank: top = most wanted. Edit here or drag in
     the 🔗 tab. Paths are repo-relative and name a FILE, never a page's home
     folder. A refresh re-mints the symlinks beside this file and never edits
     a row; a `removed` row is a person's ✕. -->

"""


class PagexMixin:

    # ---- shared ground -------------------------------------------------
    def _pagex_state(self, p):
        page_src, out_dir, board, err = self._export_target(p, "pagex")
        if err:
            return None, err
        store = out_dir / (page_src.stem + ".md")
        rows, order = {}, []
        if store.is_file():
            for line in store.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line.startswith("- "):
                    continue
                m = _ROW.match(line)
                if m and m.group("path") not in rows:
                    rows[m.group("path")] = {
                        "removed": bool(m.group("removed")),
                        "note": m.group("note") or ""}
                    order.append(m.group("path"))
        return {"page": page_src, "dir": out_dir, "stem": page_src.stem,
                "store": store, "rows": rows, "order": order,
                "board": Path(board), "ctx": self._canon_ctx(board, p)}, None

    def _pagex_write(self, st):
        lines = [_STORE_HEAD % st["stem"]]
        for path in st["order"]:
            r = st["rows"][path]
            line = "- %s" % path
            if r.get("removed"):
                line += " · removed"
            if r.get("note"):
                line += " · note: %s" % r["note"]
            lines.append(line + "\n")
        st["store"].write_text("".join(lines), encoding="utf-8")

    @staticmethod
    def _page_home_of(target, root):
        """(home_dir, inner) for a borrowed file: the nearest ancestor that is
        a folded page (`<name>/<name>.md`), plus the file's path INSIDE it.

        Keeping the inner path is not decoration. QPs1's page md and its skill
        list share the basename `QPs1-overall.md`, so a flat per-source folder
        collides on the second borrow (JL 260816's own first specimen); the
        inner path makes that impossible and says which layer was borrowed."""
        d, stack = target.parent, [target.name]
        while True:
            if (d / (d.name + ".md")).is_file():
                return d, "/".join(reversed(stack))
            if d == root or d.parent == d:
                return None, target.name
            stack.append(d.name)
            d = d.parent

    def _rendered_url(self, page_md):
        """The BOARD PAGE a borrowed page md renders as, or None.

        Opening a borrow must land where a person reads (JL 260816: "when I
        open them, why not the page in the board, but the raw markdown????").
        A .md served straight is raw text: no prose rendering, no comments, no
        plugin rail, none of the thing the borrow was taken for. The source is
        only the address; the board page is the destination."""
        d = page_md.resolve().parent
        root = Path(self.root).resolve()
        while d != root and d.parent != d:
            if (d / "board.md").is_file():
                hit = sorted((d / "board").glob("*/%s.html" % page_md.stem))
                return self._url_of(hit[0]) if hit else None
            d = d.parent
        return None

    def _page_inventory(self, home, used_paths, root):
        """What a source page HOLDS, and which of it this page is using.

        JL 260816: "每一个 page folder 我们用了它的哪些 information … 这个
        sub-folder 用了，那个 sub-folder 没有用". A borrow list says what was
        taken and is silent on what was there, so a reader cannot tell a
        deliberate one-file borrow from never having looked. The inventory
        makes the WHOLE source page visible and marks the part in use."""
        out = []
        md = home / (home.name + ".md")
        if md.is_file():
            rel = self._url_of(md)
            out.append({"kind": "md", "name": md.name, "n": 1,
                        "used": bool(rel) and rel.lstrip("/") in used_paths,
                        "files": [md]})
        for d in sorted(home.iterdir()):
            if not d.is_dir() or d.name.startswith((".", "_")):
                continue
            files = sorted(f for f in d.rglob("*")
                           if f.is_file() and not f.name.startswith("."))
            if not files:
                continue
            rels = [self._url_of(f) for f in files]
            rels = [r.lstrip("/") for r in rels if r]
            out.append({"kind": "dir", "name": d.name + "/", "n": len(files),
                        "used": any(r in used_paths for r in rels),
                        "files": files})
        return out

    @staticmethod
    def _head_state(page_md):
        """The source page's own `state:` line, so a card can disclose whether
        it is lending a ruling (✅) or an argument still moving (🟡/🔴)."""
        try:
            for line in page_md.read_text(encoding="utf-8",
                                          errors="replace").splitlines()[:12]:
                if line.startswith("state:"):
                    return line[6:].strip()
        except OSError:
            pass
        return ""

    # ---- the minter ----------------------------------------------------
    def _pagex_mint(self, st):
        """Re-mint every live row as a relative symlink, and report each row.

        THE ONE SAFETY RULE: this only ever unlinks a SYMLINK inside pagex/.
        A real file that lands there (a person's own note, a stray copy) is
        never touched, so the minter can be run at any time without eating
        anything it did not make."""
        root = Path(self.root).resolve()
        base = st["dir"].resolve()
        for f in sorted(base.rglob("*"), reverse=True):
            if f.is_symlink():
                f.unlink()
            elif f.is_dir() and not any(f.iterdir()):
                f.rmdir()

        out = []
        for path in st["order"]:
            r = st["rows"][path]
            rec = {"path": path, "note": r["note"], "removed": r["removed"],
                   "src": "", "inner": path.split("/")[-1], "srcstate": "",
                   "link": "", "url": "", "page_url": "", "state": "ok",
                   "why": ""}
            if r["removed"]:
                rec["state"] = "removed"
                out.append(rec)
                continue

            target = (root / path.lstrip("/"))
            try:
                resolved = target.resolve()
            except OSError as e:                       # a broken link cycle
                rec.update(state="refused", why=str(e))
                out.append(rec)
                continue

            # THE VET, in the order a reader would ask it
            if root not in resolved.parents and resolved != root:
                rec.update(state="refused",
                           why="resolves outside the repo root")
            elif base == resolved or base in resolved.parents:
                rec.update(state="refused",
                           why="inside this page's own pagex/ — a borrow "
                               "cannot point at the borrow")
            elif resolved.is_dir():
                rec.update(state="refused",
                           why="a folder, not a file; pagex links files only, "
                               "because a page's home folder would become a "
                               "ghost page")
            elif not resolved.exists():
                home, inner = self._page_home_of(target, root)
                rec.update(state="dangling", inner=inner,
                           src=home.name if home else target.parent.name,
                           why="the target no longer exists")
            else:
                home, inner = self._page_home_of(resolved, root)
                src = home.name if home else resolved.parent.name
                rec.update(src=src, inner=inner)
                if home:
                    rec["srcstate"] = self._head_state(home / (home.name + ".md"))
                link = base / src / inner
                if link.exists() and not link.is_symlink():
                    rec.update(state="refused",
                               why="a real file already sits at %s/%s; the "
                                   "minter never overwrites what it did not "
                                   "mint" % (src, inner))
                else:
                    link.parent.mkdir(parents=True, exist_ok=True)
                    link.symlink_to(os.path.relpath(resolved, link.parent))
                    rec["link"] = "%s/%s" % (src, inner)
                    # The card opens the BOARD PAGE when the borrow is one;
                    # the raw file is the fallback, never the first choice.
                    rec["page_url"] = (self._rendered_url(resolved)
                                       if resolved.name == "%s.md" % src else "")
                    rec["url"] = self._url_of(link) or ""
            out.append(rec)
        return out

    # ---- POST /_board/pagex · the refresh -------------------------------
    def pagex_refresh(self, p):
        """SEED, then mint, then render — the skill map's law, not a picker.

        The first build made a person open a dropdown, choose a file, and type
        a reason before anything was borrowed, and JL threw it out the hour it
        shipped (260816: "I don't think the filter should be there, it should
        not be manually added"). The page already NAMES the pages it leans on;
        a scan that reads those names is not a guess, and making someone
        re-enter by hand what the prose already says is the defect.

        Seeded names land at the BOTTOM, because everything above is the
        person's rank, and a ` · removed` row is never re-seeded."""
        st, err = self._pagex_state(p)
        if err:
            return None, err
        seeded = []
        for c in self._scan_route(st):
            path = self._url_of(c["md"])
            if not path:
                continue
            path = path.lstrip("/")
            if path in st["rows"]:
                continue
            st["rows"][path] = {"removed": False,
                                "note": "scan-seeded — this page names %s %d×"
                                        % (c["id"], c["n"])}
            st["order"].append(path)
            seeded.append(c["id"])
        if seeded or not st["store"].is_file():
            self._pagex_write(st)
        minted = self._pagex_mint(st)
        url = self._pagex_view(st, minted)
        live = [m for m in minted if m["state"] == "ok"]
        bad = [m for m in minted if m["state"] in ("dangling", "refused")]
        return {"ok": True, "url": url, "n": len(live), "bad": len(bad),
                "seeded": seeded}, None

    # ---- POST /_board/pagex-order · the drag ----------------------------
    def pagex_order(self, p):
        """{order: [paths]}: the person dragged the cards; the store keeps
        exactly that order, and rows the client did not send keep their place
        after the sent ones."""
        st, err = self._pagex_state(p)
        if err:
            return None, err
        sent = [x for x in (p.get("order") or []) if x in st["rows"]]
        st["order"] = sent + [x for x in st["order"] if x not in sent]
        self._pagex_write(st)
        self._pagex_view(st, self._pagex_mint(st))
        return {"ok": True, "n": len(sent)}, None

    # ---- POST /_board/pagex-entry · the pen -----------------------------
    def pagex_entry(self, p):
        """{borrow, note?, remove?, restore?}: the person's edits to the list.

        The field is `borrow`, NOT `path`: every view merges the board context
        `{path, file}` into its POST body, so a borrowed file sent as `path`
        is silently overwritten by the board's own path and the pen writes the
        wrong row (caught the hour this shipped).

        A hand-added row lands at the TOP, because reaching for a file by hand
        says it matters. The note is OPTIONAL: requiring one was a gate CC
        invented and JL removed the same day (260816), and the seeder writes
        its own note anyway.

        This pen is the DEPTH door, not the main one. The scan seeds the pages
        this page names; typing a path is how you reach a file the prose never
        mentions, most often on another board."""
        st, err = self._pagex_state(p)
        if err:
            return None, err
        many = p.get("borrow")
        many = many if isinstance(many, list) else [many or ""]
        many = [x.strip().lstrip("/") for x in many if x and x.strip()]
        if not many:
            return None, "no borrow path given"
        if len(many) > 1:
            # A card's ✕ drops a whole source page and a folder's ＋ takes
            # every file in it, so the pen speaks in batches; one path is
            # just the batch of one.
            for one in many:
                res, err = self.pagex_entry(dict(p, borrow=one))
                if err:
                    return None, err
            return {"ok": True, "n": len(many)}, None
        path = many[0]
        if path in st["rows"]:
            if p.get("remove"):
                st["rows"][path]["removed"] = True
            if p.get("restore"):
                st["rows"][path]["removed"] = False
            if p.get("note"):
                st["rows"][path]["note"] = p["note"].strip()
        else:
            note = (p.get("note") or "").strip()
            root = Path(self.root).resolve()
            target = root / path
            if not target.exists():
                return None, "%r is not a file under the repo root" % path
            if target.is_dir():
                return None, ("%r is a folder; pagex borrows FILES, because a "
                              "linked page home would become a ghost page"
                              % path)
            st["rows"][path] = {"removed": False, "note": note}
            st["order"].insert(0, path)
        self._pagex_write(st)
        self._pagex_view(st, self._pagex_mint(st))
        return {"ok": True, "path": path}, None

    # ---- GET /_board/pagexview?p=<rendered page>&from=<store> -----------
    def serve_pagexview(self):
        """The borrowed page, WITH A WAY BACK (JL 260816: "我点进去之后，怎么
        退回来呢？我进去之后好像没法退回来了").

        A bare link put a full board page into the pagex frame and left no
        exit. This frames that page under a thin bar carrying ☰ back to the
        borrows plus ← and → across them, which is the two-depth shape the
        skill map already ships. The page itself is untouched: it is served
        as it always was, inside an iframe, so nothing here can drift from
        what the board built."""
        q = parse_qs(urlparse(self.path).query)
        page = (q.get("p") or [""])[0]
        store = (q.get("from") or [""])[0]
        if not page:
            return self.reply(400, {"ok": False, "err": "no page"})

        sibs, here = [], -1
        root = Path(self.root).resolve()
        sp = root / store if store else None
        if sp and sp.is_file():
            for line in sp.read_text(encoding="utf-8").splitlines():
                m = _ROW.match(line.strip())
                if not m or m.group("removed"):
                    continue
                tgt = (root / m.group("path")).resolve()
                home, _i = self._page_home_of(tgt, root)
                if not home or tgt.name != "%s.md" % home.name:
                    continue
                u = self._rendered_url(tgt)
                if u and all(u != s[1] for s in sibs):
                    sibs.append((home.name, u))
        for i, (_n, u) in enumerate(sibs):
            if u.lstrip("/") == page.lstrip("/"):
                here = i
                break

        def door(i, glyph, label):
            if not (0 <= i < len(sibs)):
                return "<span class='off'>%s</span>" % glyph
            return ("<a href='/_board/pagexview?p=%s&from=%s' title='%s'>%s</a>"
                    % (_q(sibs[i][1].lstrip("/")), _q(store),
                       _esc(sibs[i][0]), glyph))

        name = sibs[here][0] if here >= 0 else Path(page).stem
        bar = ("<div class=bar>%s<a class=idx href='%s'>☰ the borrows</a>%s"
               "<b>%s</b><span class=sp></span>"
               "<a href='/%s' target=_blank>open on its own</a></div>"
               % (door(here - 1, "←", "previous"),
                  _esc("/" + store.rsplit("/", 1)[0] + "/"
                       + Path(store).stem + "-view.html") if store else "#",
                  door(here + 1, "→", "next"), _esc(name), _q(page)))
        html = ("<!doctype html><meta charset=utf-8><title>%s</title><style>"
                "html,body{height:100%%;margin:0}"
                ".bar{display:flex;gap:12px;align-items:center;height:34px;"
                "padding:0 12px;border-bottom:1px solid #dedeb8;"
                "font:13px -apple-system,sans-serif;background:#fbfbf9}"
                "@media(prefers-color-scheme:dark){.bar{background:#161719;"
                "border-color:#2c2e33;color:#e8e8e6}.bar a{color:#7fb2ea}}"
                ".bar a{color:#1f5aa8;text-decoration:none}"
                ".bar a:hover{text-decoration:underline}"
                ".bar .off{color:#b6b6b0}.bar .sp{flex:1}"
                "iframe{width:100%%;height:calc(100%% - 35px);border:0}"
                "</style>%s<iframe src='/%s'></iframe>"
                % (_esc(name), bar, _q(page)))
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _scan_route(self, st):
        """ROUTE A · the page ids this page's own md NAMES, ranked by how often
        it names them. Extract-only in the skill map's sense: a page that is
        not on this board is not offered, and nothing is ever auto-borrowed."""
        from src.common import page_files
        text = st["page"].read_text(encoding="utf-8", errors="replace")
        counts = Counter(m.group(1) for m in _PID.finditer(text))
        counts.pop(st["stem"].split("-")[0], None)
        by_id = {}
        for f in page_files(st["board"]):
            by_id.setdefault(f.stem.split("-")[0], f)
        out = []
        for pid, n in counts.most_common(12):
            f = by_id.get(pid)
            if not f or f.resolve() == st["page"].resolve():
                continue
            out.append({"id": pid, "n": n, "home": f.parent, "md": f,
                        "state": self._head_state(f)})
        return out

    # ---- the card view ---------------------------------------------------
    def _pagex_view(self, st, minted):
        rel_store = self._url_of(st["store"])
        shown = [m for m in minted if m["state"] != "removed"]
        removed = [m for m in minted if m["state"] == "removed"]
        bad = [m for m in shown if m["state"] != "ok"]

        # ONE CARD PER SOURCE PAGE, not per borrowed file (JL 260816:
        # "每一个 page folder 我们用了它的哪些 information"). A per-file list
        # says what was taken and stays silent on what was there, so a
        # one-file borrow and a never-looked-at page read identically. The
        # card now carries the source page's whole inventory with the part in
        # use marked, which is the question a person actually has.
        root = Path(self.root).resolve()
        used = {m["path"] for m in shown}
        groups, order = {}, []
        for m in shown:
            g = groups.get(m["src"])
            if g is None:
                g = groups[m["src"]] = {"src": m["src"], "rows": [],
                                        "state": m["srcstate"],
                                        "page_url": "", "home": None}
                order.append(m["src"])
            g["rows"].append(m)
            g["page_url"] = g["page_url"] or m["page_url"]
            g["state"] = g["state"] or m["srcstate"]
            if g["home"] is None:
                home, _inner = self._page_home_of(
                    (root / m["path"]).resolve(), root)
                g["home"] = home

        rows_html = []
        for src in order:
            g = groups[src]
            paths = [r["path"] for r in g["rows"]]
            title = _esc(src or "?")
            if g["page_url"]:
                # ONE TAB, TWO DEPTHS, and a way back (JL 260816: "我点进去
                # 之后，怎么退回来呢?"). The bare link replaced this frame with
                # a full board page and stranded the person there; the viewer
                # wraps it with ← ☰ → over the borrow list, the shape the
                # skill map already ships.
                title = ("<a class='snm' href='/_board/pagexview?p=%s&from=%s'>"
                         "%s</a>"
                         % (_q(g["page_url"].lstrip("/")),
                            _q(self._url_of(st["store"]).lstrip("/")), title))
            state = ("<span class='st'>%s</span>" % _esc(g["state"][:52])
                     if g["state"] else "")
            worst = ("dangling" if any(r["state"] == "dangling"
                                       for r in g["rows"])
                     else "refused" if any(r["state"] == "refused"
                                           for r in g["rows"]) else "ok")
            badge = {"ok": "<span class='ok'>🔗 linked</span>",
                     "dangling": "<span class='bad'>⚠ dangling</span>",
                     "refused": "<span class='bad'>⛔ refused</span>"}[worst]

            inv, used_n, all_n = [], 0, 0
            for item in (self._page_inventory(g["home"], used, root)
                         if g["home"] else []):
                all_n += 1
                icon = "📄" if item["kind"] == "md" else "📁"
                if item["used"]:
                    used_n += 1
                    inv.append("<div class='iv on'>✅ %s <b>%s</b>"
                               "<span class='mut'>%d file%s</span></div>"
                               % (icon, _esc(item["name"]), item["n"],
                                  "" if item["n"] == 1 else "s"))
                else:
                    take = ",".join(
                        (self._url_of(f) or "").lstrip("/")
                        for f in item["files"])
                    inv.append("<div class='iv off'>⬜ %s %s"
                               "<span class='mut'>%d file%s</span>"
                               "<button class='take' data-t='%s'>＋ use</button>"
                               "</div>"
                               % (icon, _esc(item["name"]), item["n"],
                                  "" if item["n"] == 1 else "s", _esc(take)))
            files = "".join(
                "<div class='iv f'>· <code>%s</code>"
                "<button class='rm' data-n='%s' title='drop this file'>✕"
                "</button></div>" % (_esc(r["inner"]), _esc(r["path"]))
                for r in g["rows"])
            why = "".join("<div class='dsc bad'>%s</div>" % _esc(r["why"])
                          for r in g["rows"] if r["why"])
            inv_block = (
                "<details class='inv' open><summary>using <b>%d of %d</b> "
                "in this page's folder</summary>%s</details>"
                % (used_n, all_n, "".join(inv)) if inv else "")
            rows_html.append(
                "<div class='row' draggable='true' data-n='%s' data-all='%s'>"
                "<div class='rl'><span class='grip' title='drag to rank'>⠿"
                "</span>%s %s</div>"
                "<div class='rr'><button class='rmall' data-all='%s' "
                "title='drop this page entirely'>✕</button></div>"
                "<div class='dsc'>%s</div>%s%s%s</div>"
                % (_esc(paths[0]), _esc(",".join(paths)), title, badge,
                   _esc(",".join(paths)), state, inv_block, files, why))
        cards = ("<div id='cards'>%s</div>" % "".join(rows_html) if rows_html
                 else "<p class='mut'>nothing borrowed yet — open 🔍 find "
                      "below to shortlist candidates.</p>")

        head = ("<div class='bar'><b>🔗 %s</b><span class='mut'>· %d borrow%s"
                "%s · top = most wanted</span><span class='sp'></span>"
                "<button id='refresh'>♻ re-mint</button>"
                "<a href='%s' download>⬇ store</a></div>"
                % (_esc(st["stem"]), len(shown), "" if len(shown) == 1 else "s",
                   (" · <b class='bad'>%d need attention</b>" % len(bad))
                   if bad else "", rel_store))

        # ＋ THE DEPTH DOOR, folded shut: the scan already seeded every page
        # this page names, so the only thing left to type is a file the prose
        # never mentions. It is the skill map's ＋ fold, not a picker on stage
        # (JL 260816: "it should not be manually added").
        finder = ("<details><summary class='mut'>＋ borrow a file by path"
                  "</summary><div class='pick'>"
                  "<input id='newpath' placeholder='repo-relative path to a "
                  "file' style='min-width:52%'>"
                  "<input id='newnote' placeholder='note (optional)'>"
                  "<button id='addborrow'>borrow</button></div>"
                  "<p class='mut'>The refresh seeds the pages this page names. "
                  "Type a path only for a file it never mentions, most often "
                  "on another board.</p></details>")

        rmv = ""
        if removed:
            rmv = ("<details><summary class='mut'>🚫 removed · %d</summary>%s"
                   "</details>"
                   % (len(removed), "".join(
                       "<div>🚫 <code>%s</code> <button class='rst' "
                       "data-n='%s'>↩ restore</button></div>"
                       % (_esc(m["path"]), _esc(m["path"])) for m in removed)))

        script = """<script>
var CTX = {path: __PATH__, file: __FILE__};
function post(route, body) {
  Object.assign(body, CTX);
  fetch('/_board/' + route, {method: 'POST',
    headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (!j.ok) { alert('\\u26a0 ' + (j.err || route)); return; }
      location.reload();
    })
    .catch(function (e) { alert('\\u26a0 ' + e); });
}
document.addEventListener('click', function (ev) {
  var b = ev.target;
  if (b.id === 'refresh') return post('pagex', {});
  if (b.id === 'addborrow')
    return post('pagex-entry', {
      borrow: document.getElementById('newpath').value,
      note: document.getElementById('newnote').value});
  if (b.className === 'take')
    return post('pagex-entry', {borrow: b.dataset.t.split(','),
                                note: 'taken from the folder view'});
  if (b.className === 'rmall')
    return post('pagex-entry', {borrow: b.dataset.all.split(','), remove: true});
  if (!b.dataset || !b.dataset.n) return;
  if (b.className === 'rm')  return post('pagex-entry', {borrow: b.dataset.n, remove: true});
  if (b.className === 'rst') return post('pagex-entry', {borrow: b.dataset.n, restore: true});
});
/* drag to rank: reorder the DOM while dragging, save the order on drop */
var drag = null, moved = false;
document.addEventListener('dragstart', function (ev) {
  drag = ev.target.closest ? ev.target.closest('.row') : null;
  moved = false;
  if (drag) drag.classList.add('drag');
});
document.addEventListener('dragover', function (ev) {
  if (!drag) return;
  ev.preventDefault();
  var r = ev.target.closest ? ev.target.closest('.row') : null;
  if (!r || r === drag) return;
  var box = r.getBoundingClientRect();
  r.parentNode.insertBefore(drag, (ev.clientY - box.top) < box.height / 2
                                  ? r : r.nextSibling);
  moved = true;
});
document.addEventListener('drop', function (ev) { ev.preventDefault(); });
document.addEventListener('dragend', function () {
  if (!drag) return;
  drag.classList.remove('drag');
  drag = null;
  if (!moved) return;
  var out = [];
  Array.prototype.forEach.call(document.querySelectorAll('#cards .row'),
    function (r) { out = out.concat(r.dataset.all.split(',')); });
  post('pagex-order', {order: out});
});
</script>"""
        script = (script.replace("__PATH__", self._json(st["ctx"]["path"]))
                        .replace("__FILE__", self._json(st["ctx"]["file"])))
        css = ("<style>"
               "body{padding:12px 16px}"
               "button{cursor:pointer;border:1px solid var(--line);"
               "background:var(--card);color:var(--fg);border-radius:6px;"
               "padding:3px 9px;font:500 12.5px -apple-system,sans-serif}"
               "input,select{border:1px solid var(--line);border-radius:6px;"
               "padding:4px 7px;background:var(--card);color:var(--fg);"
               "font:12px ui-monospace,Menlo,monospace;max-width:52%}"
               ".sp{flex:1}"
               ".bar{display:flex;align-items:center;gap:8px;margin:0 0 12px;"
               "flex-wrap:wrap}"
               ".bar b{font:600 15px ui-monospace,Menlo,monospace}"
               ".row{display:flex;align-items:center;gap:8px 10px;"
               "flex-wrap:wrap;padding:12px 16px;border:1px solid var(--line);"
               "border-radius:10px;margin:0 0 12px;background:var(--card)}"
               ".row.drag{opacity:.45;border-style:dashed}"
               ".grip{cursor:grab;color:var(--mut);font-size:15px;"
               "padding:0 4px;user-select:none}"
               ".rl{display:flex;align-items:center;gap:8px;flex-wrap:wrap}"
               ".rr{margin-left:auto;display:flex;gap:6px}"
               ".dsc{flex-basis:100%;line-height:1.5}"
               ".dsc code{font-size:11.5px;word-break:break-all}"
               ".snm{font:600 14px ui-monospace,Menlo,monospace;"
               "text-decoration:none;color:#1f5aa8}"
               ".st{font-size:12px;color:var(--mut)}"
               ".inv{flex-basis:100%;margin:4px 0 0}"
               ".inv summary{font-size:12.5px;color:var(--mut);margin:0 0 4px}"
               ".iv{display:flex;gap:8px;align-items:baseline;padding:2px 0 2px 6px;"
               "font:12.5px/1.6 ui-monospace,Menlo,monospace}"
               ".iv .mut{margin-left:auto;font-size:11.5px}"
               ".iv.off{color:var(--mut)}"
               ".iv.f{padding-left:6px;color:var(--mut)}"
               ".iv code{font-size:12px}"
               ".iv button{margin-left:8px;padding:1px 8px;font-size:11.5px}"
               ".take{color:#1f5aa8}"
               ".ok{color:#2c7a4b;font-size:12px}"
               ".bad{color:#c0392b;font-size:12px}"
               "summary{cursor:pointer;margin:8px 0}"
               "h3{font-size:13px;margin:14px 0 6px}"
               ".find{border-left:2px solid var(--line);padding-left:12px}"
               ".cand{padding:7px 0;border-bottom:1px solid var(--line)}"
               ".brd{font:600 11.5px ui-monospace,Menlo,monospace;"
               "color:var(--mut);margin:12px 0 2px;text-transform:none}"
               ".pick{display:flex;gap:6px;margin-top:5px;flex-wrap:wrap}"
               "</style>")
        view = st["dir"] / (st["stem"] + "-view.html")
        view.write_text(_VIEW.format(title=_esc(st["stem"] + " · pagex"),
                                     body=css + head + cards + finder + rmv
                                     + script),
                        encoding="utf-8")
        return self._url_of(view)

    @staticmethod
    def _json(s):
        import json
        return json.dumps(s or "")
