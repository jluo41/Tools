"""📜📝📚 Export · a page's DERIVED paper-facing plugins: latex/, word/, bibex/.

THE DIVISION OF LABOUR, the same one deck.py drew for slide/:

  the writers (skills/paper/haipipe-paper/scripts/to-word/)   HOW an export is made
  this file                                                   WHERE it lands, and the door

Nothing is copied from the paper family. `md2tex.py` and `md2docx.py` are called
by path, so Word and LaTeX stay two projections of one source and improve when
the skill improves. The one writer authored HERE is the bibex extractor, because
citation-craft.md forbids generating bibtex: it may only SUBSET a `.bib` a person
already wrote, so it is thirty lines of copying and belongs to no other family.

WHERE AN EXPORT LANDS is the plugin contract (haipipe-page-plugin): a folded page
owns its material, so `<page-dir>/<plugin>/<stem>.<ext>`; a flat page falls back
to the board-level `<board>/<plugin>/`, exactly as deck.py does for slide/.

WHY EVERY OUTPUT GETS AN .html BESIDE IT when the artifact itself cannot be
framed: the surface is a right-pane TAB, and a tab needs a URL a browser can
show. A PDF frames natively; a .tex or .docx does not, so the builder writes a
small view page beside it — derived from the derived, regenerated with it,
never hand-edited.

`--paper-root` IS DISCOVERED, NOT DEMANDED: walk up from the page toward --root
looking for a `0-*.bib`, which is the paper family's own root convention. A page
outside any paper exports cite-less rather than refusing (the roster's rule).
"""
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# The writers, found beside this engine the way deck.py finds html-ppt:
# live/ -> haipipe-board -> board -> skills, then the paper family.
_SCRIPTS = (Path(__file__).resolve().parents[3]
            / "paper" / "haipipe-paper" / "scripts" / "to-word")

_TEXBIN = "/Library/TeX/texbin"

# \citep{a,b} · \citet[p.3]{c} · \cite{d} — the keys, however the cite is spelt.
_CITE = re.compile(r"\\cite[pt]?\*?(?:\[[^\]]*\])*\{([^}]+)\}")

_VIEW = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#fbfbf9;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4df;--card:#fff}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23}}}}
body{{margin:0;padding:18px;background:var(--bg);color:var(--fg);
 font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:16px;margin:0 0 4px}} .mut{{color:var(--mut);font-size:12px}}
a{{color:#1f5aa8}} pre{{background:var(--card);border:1px solid var(--line);
 border-radius:8px;padding:12px;overflow:auto;font:12px/1.45 ui-monospace,Menlo,monospace;
 white-space:pre-wrap}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:8px;
 padding:10px 12px;margin:0 0 10px}}
.card b{{font:600 13px/1.3 ui-monospace,Menlo,monospace}}
.miss{{border-color:#c66;}}
</style></head><body>{body}</body></html>
"""


def _esc(s):
    return html.escape(str(s or ""), quote=False)


class ExportMixin:

    # ---- shared ground ------------------------------------------------
    def _export_target(self, p, plugin):
        """-> (page_src, out_dir, url_base, err). Same door as every write:
        `target()` refuses a path outside --root or a board with no board.md."""
        got = self.target(p)
        if got[0] is None:
            return None, None, None, got[1]
        f, board = got
        page_src = Path(board) / f
        if not page_src.is_file() or page_src.suffix != ".md":
            return None, None, None, "not a page .md: %s" % f
        # A folded page owns its material (haipipe-page-plugin); a flat page
        # keeps the board-level fallback, the same fork deck.py takes.
        if page_src.parent.name == page_src.stem:
            out_dir = page_src.parent / plugin
        else:
            out_dir = Path(board) / plugin
        out_dir.mkdir(parents=True, exist_ok=True)
        return page_src, out_dir, board, None

    def _url_of(self, path):
        try:
            return "/" + Path(path).resolve().relative_to(
                Path(self.root).resolve()).as_posix()
        except ValueError:
            return None

    def _paper_root(self, page_src):
        """Walk up toward --root for the paper convention `0-*.bib`."""
        root = Path(self.root).resolve()
        d = page_src.resolve().parent
        while True:
            if list(d.glob("0-*.bib")):
                return d
            if d == root or d.parent == d:
                return None
            d = d.parent

    def _run(self, cmd, timeout, cwd=None, env=None):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=timeout, cwd=cwd, env=env)
            return r.returncode, (r.stdout or "") + (r.stderr or "")
        except subprocess.TimeoutExpired:
            return 1, "timed out after %ss: %s" % (timeout, " ".join(map(str, cmd)))
        except OSError as e:
            return 1, str(e)

    def _canon_ctx(self, board, p):
        """The ONE shape a view may bake into its buttons, in target()'s own
        convention: `path` is `<board>/board.md`, root-relative (target takes
        the parent, then walks up). Every button that baked the caller's RAW
        path broke eventually — an absolute path doubled under --root, the
        bare board folder lost a segment (three dialogs, one day, JL 260815) —
        so the context is normalized HERE, once, for every view."""
        try:
            rel = "/" + Path(board).resolve().relative_to(
                Path(self.root).resolve()).as_posix() + "/board.md"
        except (ValueError, OSError):
            rel = p.get("path") or ""
        return {"path": rel, "file": p.get("file") or ""}

    def _rebuild_ui(self, route, p):
        """A VISIBLE 🔄 rebuild in the view's header (JL 260815: "should you
        give a new button there so we can rebuild the tex?"). The lit-click on
        the tab still rebuilds, but an affordance nobody can see is not one;
        the bibex workbench set the pattern and this is the same sandwich:
        context baked in, POST the route, reload on ok."""
        btn = ("<button id='rebuild' style=\"float:right;cursor:pointer;"
               "border:1px solid var(--line);background:var(--card);"
               "color:var(--fg);border-radius:6px;padding:4px 10px;"
               "font:500 12px -apple-system,sans-serif\">🔄 rebuild</button>")
        script = ("""<script>
document.getElementById('rebuild').onclick = function () {
  var b = this; b.disabled = true; b.textContent = '⏳ rebuilding…';
  fetch('/_board/%s', {method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({path: %s, file: %s})})
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (j.ok) { location.reload(); return; }
      alert('⚠ ' + (j.err || 'rebuild failed'));
      b.disabled = false; b.textContent = '🔄 rebuild';
    })
    .catch(function (e) { alert('⚠ ' + e);
      b.disabled = false; b.textContent = '🔄 rebuild'; });
};
</script>""" % (route, json.dumps(p.get("path") or ""),
                json.dumps(p.get("file") or "")))
        return btn, script

    # ---- POST /_board/latex ------------------------------------------
    def export_latex(self, p):
        """{path, file} -> {ok, url, tex, pdf}. md2tex writes the section; a
        standalone master is wrapped around it here because md2tex's own
        --compile is bound to one paper's hand-written master."""
        page_src, out_dir, board, err = self._export_target(p, "latex")
        if err:
            return None, err
        p = {**p, **self._canon_ctx(board, p)}   # the view bakes p; make it canonical
        stem = page_src.stem
        proot = self._paper_root(page_src)
        # --keep-fences: a board division is often figure-only, and the paper
        # default (drop sketches) exported it as an empty section (JL 260815).
        code, log = self._run(
            [sys.executable, str(_SCRIPTS / "md2tex.py"), str(page_src),
             "--paper-root", str(proot or page_src.parent), "-o", str(out_dir),
             "--keep-fences"],
            timeout=120)
        tex = out_dir / (stem + ".tex")
        if not tex.is_file():
            return None, "md2tex wrote no .tex:\n" + log[-1500:]

        # The wrapper master: article + the few packages a board section uses.
        # natbib only when a real .bib is in reach; a cite-less page needs none.
        # THE PAGE'S OWN BIB COMES FIRST (JL 260815: "convert it to the latex
        # and this one to be cited as well"): bibex/<stem>.bib is the page's
        # citation store, so the PDF cites what the page cites — the paper's
        # 0-*.bib is the fallback for pages that have no store of their own.
        bib = None
        own = page_src.parent / "bibex" / (stem + ".bib")
        if own.is_file() and "@" in own.read_text(encoding="utf-8",
                                                  errors="replace"):
            bib = own
        elif proot:
            bibs = sorted(proot.glob("0-*.bib"))
            bib = bibs[0] if bibs else None
        master = out_dir / (stem + "-master.tex")
        head = ["\\documentclass[11pt]{article}",
                "\\usepackage[margin=1in]{geometry}",
                "\\usepackage{graphicx,booktabs,longtable}",
                "\\usepackage[hidelinks]{hyperref}"]
        tail = []
        if bib:
            head.append("\\usepackage{natbib}")
            tail += ["\\bibliographystyle{plainnat}",
                     "\\bibliography{%s}" % bib.stem]
        else:
            head.append("\\providecommand{\\citep}[1]{[#1]}"
                        "\\providecommand{\\citet}[1]{[#1]}")
        master.write_text(
            "\n".join(head) + "\n\\begin{document}\n\\input{%s}\n" % stem
            + "\n".join(tail) + "\n\\end{document}\n", encoding="utf-8")

        env = dict(os.environ, PATH=_TEXBIN + ":" + os.environ.get("PATH", ""))
        if bib:
            env["BIBINPUTS"] = ".:%s:" % bib.parent
        passes = [["xelatex", "-interaction=nonstopmode", master.name]]
        if bib:
            passes += [["bibtex", master.stem],
                       ["xelatex", "-interaction=nonstopmode", master.name],
                       ["xelatex", "-interaction=nonstopmode", master.name]]
        for cmd in passes:
            code, out = self._run(cmd, timeout=180, cwd=out_dir, env=env)
        built = out_dir / (stem + "-master.pdf")
        pdf = out_dir / (stem + ".pdf")
        if built.is_file():
            built.replace(pdf)
        # The plugin folder holds the artifact, not the build's residue: every
        # -master.* regenerates on the next run, and a failure's log tail is
        # already in the view page below.
        for res in out_dir.glob(stem + "-master.*"):
            try:
                res.unlink()
            except OSError:
                pass
        # ONE view either way (JL 260815: "how could we see the raw latex
        # content?"): the tab frames <stem>-view.html, which shows the PDF and
        # keeps the raw .tex one fold below it — on failure the fold is open,
        # the log tail beside it, and the frame is never blank.
        view = out_dir / (stem + "-view.html")
        raw = tex.read_text(encoding="utf-8")
        src_fold = ("<details%s><summary>⌨️ raw LaTeX source · %s.tex · "
                    "<a href='%s' download>⬇ download</a></summary><pre>%s</pre>"
                    "</details>"
                    % (" open" if not pdf.is_file() else "",
                       _esc(stem), self._url_of(tex), _esc(raw)))
        btn, script = self._rebuild_ui("latex", p)
        if pdf.is_file():
            # the mtime rides the frame's URL, so a rebuild's reload can never
            # show a cached PDF as if it were the fresh one
            body = (btn + "<h1>📜 %s</h1><p class='mut'>compiled by xelatex · "
                    "<a href='%s' download>⬇ %s.pdf</a></p>"
                    "<iframe src='%s?t=%d' style='width:100%%;height:78vh;border:1px "
                    "solid var(--line);border-radius:8px'></iframe>%s"
                    % (_esc(stem), self._url_of(pdf), _esc(stem),
                       self._url_of(pdf), pdf.stat().st_mtime_ns, src_fold))
        else:
            body = (btn + "<h1>📜 %s.tex</h1><p class='mut'>xelatex produced no PDF; "
                    "the generated source is below. Log tail:</p><pre>%s</pre>%s"
                    % (_esc(stem), _esc(out[-800:] if out else ""), src_fold))
        view.write_text(_VIEW.format(title=_esc(stem + " · latex"),
                                     body=body + script),
                        encoding="utf-8")
        return {"ok": True, "url": self._url_of(view), "tex": self._url_of(tex),
                "pdf": self._url_of(pdf) if pdf.is_file() else None}, None

    # ---- POST /_board/word -------------------------------------------
    def export_word(self, p):
        """{path, file} -> {ok, url, docx, pdf}. md2docx writes the .docx and
        docx2pdf renders its PDF twin, which is what the tab frames: a browser
        cannot show a .docx, and the twin is rendered from the package itself
        so it shows what the .docx actually contains."""
        page_src, out_dir, board, err = self._export_target(p, "word")
        if err:
            return None, err
        p = {**p, **self._canon_ctx(board, p)}   # the view bakes p; make it canonical
        stem = page_src.stem
        docx = out_dir / (stem + ".docx")
        # THE PAGE'S OWN BIB COMES FIRST, the same preference the LaTeX export
        # holds (JL 260815: "how about the word? will we have the reference as
        # well?"). md2docx renders citations from a `.board-refs.bbl` beside
        # the .bib, so when the page has a store, cli/refs.py compiles that
        # cache in bibex/ and md2docx is pointed there — in-text labels and
        # the References section then come from the one store the workbench
        # maintains. A page with no store keeps the paper-root fallback.
        proot = self._paper_root(page_src)
        own = page_src.parent / "bibex" / (stem + ".bib")
        if own.is_file() and "@" in own.read_text(encoding="utf-8",
                                                  errors="replace"):
            bbl = own.parent / ".board-refs.bbl"
            if not bbl.is_file() or bbl.stat().st_mtime < own.stat().st_mtime:
                refs = Path(__file__).resolve().parents[1] / "cli" / "refs.py"
                # refs.py guards on which("bibtex") against ITS env, so hand
                # it one where the TeX bin is on PATH.
                self._run([sys.executable, str(refs), str(own.parent)],
                          timeout=60,
                          env=dict(os.environ, PATH=_TEXBIN + ":"
                                   + os.environ.get("PATH", "")))
            proot = own.parent
        cmd = [sys.executable, str(_SCRIPTS / "md2docx.py"), str(page_src),
               "-o", str(docx)]
        if proot:
            cmd += ["--paper-root", str(proot)]
        code, log = self._run(cmd, timeout=120)
        if not docx.is_file():
            return None, "md2docx wrote no .docx:\n" + log[-1500:]
        pdf = out_dir / (stem + ".pdf")
        code, plog = self._run(
            [sys.executable, str(_SCRIPTS / "docx2pdf.py"), str(docx),
             "-o", str(pdf)], timeout=240)
        view = out_dir / (stem + "-view.html")
        durl = self._url_of(docx)
        btn, script = self._rebuild_ui("word", p)
        if pdf.is_file():
            body = (btn + "<h1>📝 %s.docx</h1><p class='mut'>the PDF twin below is "
                    "rendered from the package itself · "
                    "<a href='%s' download>⬇ download the .docx</a></p>"
                    "<iframe src='%s?t=%d' style='width:100%%;height:82vh;border:1px "
                    "solid var(--line);border-radius:8px'></iframe>"
                    % (_esc(stem), durl, self._url_of(pdf),
                       pdf.stat().st_mtime_ns))
        else:
            body = (btn + "<h1>📝 %s.docx</h1><p class='mut'>written, but the PDF twin "
                    "did not render (Chrome headless). "
                    "<a href='%s' download>⬇ download the .docx</a></p><pre>%s</pre>"
                    % (_esc(stem), durl, _esc(plog[-800:] if plog else "")))
        view.write_text(_VIEW.format(title=_esc(stem + ".docx"),
                                     body=body + script),
                        encoding="utf-8")
        return {"ok": True, "url": self._url_of(view), "docx": durl,
                "pdf": self._url_of(pdf) if pdf.is_file() else None}, None

    # ---- POST /_board/bibex ------------------------------------------
    # THE PAGE OWNS ITS BIB (JL 260815: "the bib for this page only"). The
    # plugin is MIXED, the way display/ is: bibex/<stem>.bib is PRIMARY, a
    # person's citation store for this one page, and the card view beside it
    # is derived. The paper's 0-*.bib is NEVER written — extraction only ever
    # SEEDS the page bib by copying entries whole, which keeps citation-craft's
    # law intact: the machine copies or lands a person's text, and composes
    # nothing. A refresh therefore never overwrites or deletes an entry; it
    # imports what is newly resolvable and regenerates the view.

    def _bibex_state(self, p):
        """Shared ground for the three bibex doors: paths, the page's cite
        keys, the page bib parsed with order kept, and the canonical ctx the
        view may bake into its buttons."""
        page_src, out_dir, board, err = self._export_target(p, "bibex")
        if err:
            return None, err
        text = page_src.read_text(encoding="utf-8")
        # A cite in a code fence or a backtick span is an ILLUSTRATION — a
        # figure showing the syntax, a rule quoting `\cite{TOADD}` — not a
        # citation this page makes. Strip both before scanning.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`\n]*`", "", text)
        keys = []
        for m in _CITE.finditer(text):
            for k in m.group(1).split(","):
                k = k.strip()
                if k and k not in keys:
                    keys.append(k)
        bib = out_dir / (page_src.stem + ".bib")
        raw = bib.read_text(encoding="utf-8") if bib.is_file() else ""
        return {"page": page_src, "dir": out_dir, "stem": page_src.stem,
                "keys": keys, "bib": bib, "raw": raw,
                "entries": self._bib_entries(raw),
                "ctx": self._canon_ctx(board, p)}, None

    _BIB_HEAD = ("%% This PAGE's citation store (JL 260815: the bib for this "
                 "page only).\n"
                 "%% PRIMARY material: edit through the \U0001F4DA tab or by "
                 "hand; a refresh only\n"
                 "%% APPENDS newly resolvable imports and never overwrites or "
                 "deletes an entry.\n"
                 "%% The paper's 0-*.bib is read for seeding and never "
                 "written.\n")

    def export_bibex(self, p):
        """{path, file} -> {ok, url, bib, n, missing}. The refresh: re-scan the
        page's keys, seed-import what the upstream paper bib can resolve, and
        regenerate the card view. Entries already in the page bib are never
        touched."""
        st, err = self._bibex_state(p)
        if err:
            return None, err
        imported = []
        upstream_name = ""
        proot = self._paper_root(st["page"])
        if proot:
            bibs = sorted(proot.glob("0-*.bib"))
            upstream_name = ", ".join(b.name for b in bibs)
            allof = self._bib_entries(
                "\n\n".join(b.read_text(encoding="utf-8", errors="replace")
                            for b in bibs))
            for k in st["keys"]:
                if k not in st["entries"] and k in allof:
                    st["entries"][k] = allof[k]
                    imported.append(k)
        if imported or not st["bib"].is_file():
            self._bibex_write(st, upstream_name, imported)
        missing = [k for k in st["keys"] if k not in st["entries"]]
        view = self._bibex_view(p, st, upstream_name)
        return {"ok": True, "url": view, "bib": self._url_of(st["bib"]),
                "n": len(st["entries"]), "imported": imported,
                "missing": missing}, None

    def bibex_verify(self, p):
        """{path, file, key, who?, undo?} -> {ok}. The human tick: writes a
        `verified = {WHO YYMMDD}` field INTO the page bib's entry, so the
        status travels with the entry and needs no sidecar. The one field is
        the only thing this door may change."""
        st, err = self._bibex_state(p)
        if err:
            return None, err
        key = (p.get("key") or "").strip()
        if key not in st["entries"]:
            return None, "no entry %r in the page bib" % key
        entry = st["entries"][key]
        entry = re.sub(r",?\s*\n\s*verified\s*=\s*\{[^}]*\}", "", entry)
        if not p.get("undo"):
            who = (p.get("who") or "JL").strip()
            import datetime
            stamp = "%s %s" % (who, datetime.date.today().strftime("%y%m%d"))
            body, brace, tail = entry.rpartition("}")
            body = body.rstrip()
            if not body.endswith(","):
                body += ","
            entry = body + "\n  verified = {%s}\n}" % stamp
        st["entries"][key] = entry
        self._bibex_write(st, "", [])
        self._bibex_view(p, st, "")
        return {"ok": True, "key": key}, None

    def bibex_entry(self, p):
        """{path, file, bibtex, replace?} -> {ok, key} | {ok, resolved}. The
        pen: lands a PERSON-SUPPLIED entry verbatim in the page bib. It
        validates shape (one entry, balanced braces, a key) and guards
        duplicates; it never composes, completes, or corrects the text, which
        is the whole line between a pen and an author.
        A LINK instead of bibtex (a DOI, an arXiv link, Scholar's cite link,
        a paper URL) is RESOLVED: the bibtex is fetched whole from that
        authoritative source — copying, not composing — and returned as
        `resolved` for the person to review; landing stays their second
        click."""
        st, err = self._bibex_state(p)
        if err:
            return None, err
        raw = (p.get("bibtex") or "").strip()
        if raw and not raw.startswith("@"):
            fetched, ferr = self._resolve_bib_link(raw)
            if ferr:
                return None, ferr
            return {"ok": True, "resolved": self._fix_bib_key(fetched)}, None
        got = self._bib_entries(raw)
        if len(got) != 1:
            return None, ("expected exactly ONE balanced @type{key, ...} "
                          "entry, found %d" % len(got))
        key, entry = next(iter(got.items()))
        if entry.count("{") != entry.count("}"):
            return None, "unbalanced braces in the entry"
        if key in st["entries"] and not p.get("replace"):
            return None, ("key %r already in the page bib; pass replace to "
                          "overwrite it" % key)
        st["entries"][key] = entry
        self._bibex_write(st, "", [])
        self._bibex_view(p, st, "")
        return {"ok": True, "key": key}, None

    # ---- bibex internals ---------------------------------------------
    @staticmethod
    def _http_get(url, accept=None, timeout=20):
        import urllib.request
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36",
            **({"Accept": accept} if accept else {})})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")

    def _fix_bib_key(self, bib):
        """A fetched entry sometimes wears an unusable key (doi.org's is the
        DOI URL itself). The KEY is a local handle, not metadata, so repairing
        it mechanically from the fetched author+year fields is renaming, not
        composing: <first-author-surname><year>, the shape Scholar itself
        emits."""
        m = re.match(r"(@\w+\s*\{)\s*([^,\s]*)\s*,", bib)
        if not m or re.fullmatch(r"[A-Za-z0-9_.+-]+", m.group(2) or ""):
            return bib
        author = self._bib_field(bib, "author")
        year = re.sub(r"\D", "", self._bib_field(bib, "year"))[:4]
        surname = re.sub(r"[^a-z]", "", (author.split(" and ")[0]
                                         .split(",")[0].split()[-1:] or ["ref"]
                                         )[0].lower()) or "ref"
        return bib.replace(m.group(0), "%s%s%s," % (m.group(1), surname, year), 1)

    def _resolve_bib_link(self, link):
        """A pasted link -> bibtex fetched WHOLE from its source. Four shapes,
        each an authority for its own metadata; anything else is refused with
        the shapes named, never guessed at."""
        import urllib.parse as _u
        link = link.strip().split("\n")[0].strip()
        try:
            # ① Scholar's own cite link (the Cite -> BibTeX button's URL).
            #    Session-signed, so only the person can produce it; fetched
            #    verbatim while the signature is fresh.
            if "scholar.googleusercontent.com/scholar.bib" in link:
                text = self._http_get(link)
                if text.lstrip().startswith("@"):
                    return text.strip(), None
                return None, ("Scholar declined the cite link (its signature "
                              "expires); copy a fresh one from Cite → BibTeX")
            # ② a DOI, bare or as a doi.org URL: content negotiation.
            m = re.search(r"(10\.\d{4,}/\S+)", link)
            if "doi.org/" in link or link.lower().startswith("doi:") or \
                    (m and not link.lower().startswith("http")):
                if not m:
                    return None, "no 10.xxxx/... DOI found in %r" % link
                text = self._http_get("https://doi.org/" + _u.quote(m.group(1)),
                                      accept="application/x-bibtex")
                if text.lstrip().startswith("@"):
                    return text.strip(), None
                return None, "doi.org returned no bibtex for %s" % m.group(1)
            # ③ an arXiv link or bare id: arXiv's own bibtex endpoint.
            m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}"
                          r"(?:v\d+)?)", link, re.I) or \
                re.fullmatch(r"([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", link)
            if m:
                text = self._http_get("https://arxiv.org/bibtex/" + m.group(1))
                if text.lstrip().startswith("@"):
                    return text.strip(), None
                return None, "arxiv.org returned no bibtex for %s" % m.group(1)
            # ④ any other paper URL: ask Semantic Scholar to name it.
            if link.lower().startswith("http"):
                body = self._http_get(
                    "https://api.semanticscholar.org/graph/v1/paper/URL:"
                    + _u.quote(link, safe="") + "?fields=citationStyles")
                j = json.loads(body)
                bib = (j.get("citationStyles") or {}).get("bibtex") or ""
                if bib.lstrip().startswith("@"):
                    if not re.search(r"\burl\s*=", bib):
                        b, _, _ = bib.rpartition("}")
                        bib = b.rstrip().rstrip(",") + ",\n url = {%s}\n}" % link
                    return bib.strip(), None
                return None, (j.get("message") or
                              "Semantic Scholar could not resolve that URL; "
                              "try its DOI, arXiv link, or Scholar cite link")
            return None, ("not bibtex and not a link I can resolve; paste "
                          "an @entry, a DOI, an arXiv link, a Scholar cite "
                          "link, or a paper URL")
        except Exception as e:
            return None, "fetch failed: %s" % e

    def _bibex_write(self, st, upstream, imported):
        lines = [self._BIB_HEAD]
        if imported:
            import datetime
            lines.append("%% seeded %s from %s: %s\n"
                         % (datetime.date.today().strftime("%y%m%d"),
                            upstream or "upstream", ", ".join(imported)))
        cited = [k for k in st["keys"] if k in st["entries"]]
        rest = [k for k in st["entries"] if k not in st["keys"]]
        lines.append("\n" + "\n\n".join(st["entries"][k]
                                        for k in cited + rest) + "\n")
        st["bib"].write_text("".join(lines), encoding="utf-8")

    @staticmethod
    def _bib_field(entry, name):
        """One field's value, brace-aware; '' when absent."""
        m = re.search(r"\b%s\s*=\s*" % re.escape(name), entry, re.I)
        if not m:
            return ""
        i = m.end()
        if i < len(entry) and entry[i] == '"':
            j = entry.find('"', i + 1)
            return entry[i + 1:j] if j > 0 else ""
        if i < len(entry) and entry[i] == "{":
            depth = 0
            for j in range(i, len(entry)):
                if entry[j] == "{":
                    depth += 1
                elif entry[j] == "}":
                    depth -= 1
                    if depth == 0:
                        return entry[i + 1:j]
            return ""
        j = entry.find(",", i)
        return entry[i:j].strip() if j > 0 else entry[i:].strip()

    def _bibex_view(self, p, st, upstream):
        """The derived card view: status, links, tick, edit, add. Regenerated
        on every door; the page bib is the truth it renders."""
        import urllib.parse as _u
        stem, keys, entries = st["stem"], st["keys"], st["entries"]

        def clean(s):
            return re.sub(r"[{}\\]", "", s or "").strip()

        def card(k):
            if k not in entries:
                q = _u.quote('"%s"' % k)
                return ("<div class='card miss'><b>%s</b> <span class='mut'>not "
                        "in this page's bib</span> <a target='_blank' rel='noopener' "
                        "href='https://scholar.google.com/scholar?q=%s'>🔎 Scholar"
                        "</a><div class='mut'>find it, then paste its bibtex "
                        "below with this key.</div></div>" % (_esc(k), q))
            e = entries[k]
            kind = (re.match(r"@(\w+)", e) or [None, "?"])[1]
            title = clean(self._bib_field(e, "title"))
            author = clean(self._bib_field(e, "author"))
            year = clean(self._bib_field(e, "year"))
            doi = clean(self._bib_field(e, "doi"))
            url = clean(self._bib_field(e, "url"))
            ver = clean(self._bib_field(e, "verified"))
            q = _u.quote('"%s"' % (title or k))
            links = ["<a target='_blank' rel='noopener' "
                     "href='https://scholar.google.com/scholar?q=%s'>🔎 Scholar</a>" % q]
            if doi:
                links.append("<a target='_blank' rel='noopener' "
                             "href='https://doi.org/%s'>🔗 DOI</a>" % _esc(doi))
            if url:
                links.append("<a target='_blank' rel='noopener' href='%s'>📄 URL</a>"
                             % _esc(url))
            status = ("<span class='ok'>✅ checked · %s</span> "
                      "<button data-k='%s' class='unver'>undo</button>" % (_esc(ver), _esc(k))
                      ) if ver else \
                     ("<span class='mut'>⬜ unchecked</span> "
                      "<button data-k='%s' class='ver'>✓ I checked this</button>" % _esc(k))
            # In the bib but not in the page's text: say what closes the gap
            # and hand over the exact cite to paste, because "not cited"
            # alone read as "not synced" (JL 260815).
            unused = "" if k in keys else \
                (" <span class='mut'>· in the bib, not cited in the page text "
                 "yet</span> <button data-k='%s' class='cpy'>📋 copy "
                 "\\citep{%s}</button>" % (_esc(k), _esc(k)))
            meta = " · ".join(x for x in (author, year) if x)
            return ("<div class='card'><b>%s</b> <span class='mut'>%s</span>%s "
                    "<span class='st'>%s</span>"
                    "<div>%s</div><div class='mut'>%s</div>"
                    "<details><summary class='mut'>raw bibtex · ✎ edit</summary>"
                    "<textarea data-k='%s'>%s</textarea>"
                    "<button data-k='%s' class='save'>save entry</button></details>"
                    "</div>"
                    % (_esc(k), _esc(kind), unused, status,
                       _esc(title), _esc(meta) + " · ".join([""] + links),
                       _esc(k), _esc(e), _esc(k)))

        order = [k for k in keys] + [k for k in entries if k not in keys]
        cards = [card(k) for k in order] or \
                ["<p class='mut'>no keys cited and no entries yet; add the "
                 "first one below.</p>"]
        head = ("<h1>📚 %s · %d entr%s · %d cited</h1><p class='mut'>this "
                "page's own bib%s · <a href='%s' download>⬇ %s.bib</a> · "
                "<button id='refresh'>↻ refresh</button></p>"
                % (_esc(stem), len(entries),
                   "y" if len(entries) == 1 else "ies", len(keys),
                   _esc(" · seeded from " + upstream if upstream else ""),
                   self._url_of(st["bib"]), _esc(stem)))
        add = ("<div class='card'><b>＋ add a citation</b><div class='mut'>"
               "paste BIBTEX, a DOI, an arXiv link, Scholar's Cite → BibTeX "
               "link, or a paper URL. A link is fetched from its source and "
               "shown here first; add lands it verbatim.</div>"
               "<textarea id='newbib' placeholder='@article{key, ...}  ·  "
               "10.1234/abcd  ·  arxiv.org/abs/…  ·  scholar.bib?…'>"
               "</textarea><button id='addbib'>add entry</button> "
               "<span id='addnote' class='mut'></span></div>")
        # The RAW FILE, one fold away (JL 260815: "how could I see the raw
        # files"): the whole .bib verbatim, header comments included, plus
        # its on-disk path for whoever prefers an editor — it is PRIMARY
        # material and hand-editing it is legal.
        try:
            rel = st["bib"].resolve().relative_to(Path(self.root).resolve())
        except ValueError:
            rel = st["bib"]
        rawfold = ("<details class='card'><summary><b>📄 the raw %s.bib</b> "
                   "<span class='mut'>· %s · hand-editing is fine, it is "
                   "yours</span></summary><pre>%s</pre></details>"
                   % (_esc(stem), _esc(str(rel)),
                      _esc(st["bib"].read_text(encoding="utf-8")
                           if st["bib"].is_file() else "")))
        script = """
<script>
var CTX = {path: %s, file: %s};
function post(route, body, done) {
  Object.assign(body, CTX);
  fetch('/_board/' + route, {method: 'POST',
    headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (!j.ok) { alert('⚠ ' + (j.err || route)); return; }
      /* a resolved LINK fills the box for review; landing is the next click */
      if (j.resolved) {
        document.getElementById('newbib').value = j.resolved;
        document.getElementById('addnote').textContent =
          'fetched from the source · review it (the key too), then add';
        return;
      }
      location.reload();
    })
    .catch(function (e) { alert('⚠ ' + e); });
}
document.addEventListener('click', function (ev) {
  var b = ev.target;
  if (b.id === 'refresh') return post('bibex', {});
  if (b.id === 'addbib')
    return post('bibex-entry', {bibtex: document.getElementById('newbib').value});
  if (!b.dataset || !b.dataset.k) return;
  if (b.className === 'cpy') {
    navigator.clipboard.writeText('\\\\citep{' + b.dataset.k + '}')
      .then(function () { b.textContent = '📋 copied'; });
    return;
  }
  if (b.className === 'ver')   return post('bibex-verify', {key: b.dataset.k});
  if (b.className === 'unver') return post('bibex-verify', {key: b.dataset.k, undo: true});
  if (b.className === 'save')
    return post('bibex-entry', {replace: true, key: b.dataset.k,
      bibtex: document.querySelector('textarea[data-k=\\'' + b.dataset.k + '\\']').value});
});
</script>""" % (json.dumps(st["ctx"]["path"]), json.dumps(st["ctx"]["file"]))
        extra_css = ("<style>textarea{width:100%;min-height:110px;font:12px/1.4 "
                     "ui-monospace,Menlo,monospace;background:var(--card);color:var(--fg);"
                     "border:1px solid var(--line);border-radius:6px;padding:8px}"
                     # The ＋ box starts ONE LINE tall and grows with its
                     # content (JL 260815: smaller): a pasted link stays
                     # compact, a fetched bibtex expands to be reviewed.
                     "#newbib{field-sizing:content;min-height:38px;height:38px;"
                     "max-height:45vh;resize:vertical}"
                     "button{cursor:pointer;border:1px solid var(--line);"
                     "background:var(--card);color:var(--fg);border-radius:6px;"
                     "padding:3px 9px;font:500 12px -apple-system,sans-serif}"
                     ".ok{color:#2a8a2a}.st{float:right}</style>")
        view = st["dir"] / (stem + "-bib.html")
        view.write_text(_VIEW.format(title=_esc(stem + " · bibex"),
                                     body=extra_css + head + "".join(cards)
                                     + add + rawfold + script),
                        encoding="utf-8")
        return self._url_of(view)

    @staticmethod
    def _bib_entries(raw):
        """@type{key, …balanced…} -> {key: entry}, order kept. Brace counting,
        no library: the input is a .bib a person maintains, not arbitrary
        text. @comment blocks and % lines fall out naturally: only shapes
        opening `@word{key,` are taken."""
        out = {}
        for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,", raw):
            key, depth, i = m.group(1), 0, m.start()
            j = raw.index("{", m.start())
            for j in range(j, len(raw)):
                if raw[j] == "{":
                    depth += 1
                elif raw[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
            out[key] = raw[i:j + 1]
        return out
