"""📝 Export · POST /_board/word: md2docx .docx and its PDF twin.

Part of `ExportMixin` (export.py), which composes it; see export.py for the
writer/door division and where each export lands."""
import os
import re
import sys
import tempfile
from pathlib import Path

from host_paths import PAGE_ENGINE

from src.evidence_selection import (legacy_profile, EvidenceSelectionError)

from live.export_common import _SCRIPTS, _TEXBIN, _VIEW, _esc


class ExportWordMixin:

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
        # WHO THE COMMENTS ARE BY (JL 260928: "change the name to Junjie Luo ...
        # you can ask for user to enter their name"). The 🔄 rebuild asks and
        # sends it; without a name md2docx keeps its `haipipe` default.
        author = str(p.get("author") or "").strip()
        if len(author) > 80 or any(ord(c) < 32 for c in author):
            return None, "the comment author must be one short line"
        stem = page_src.stem
        docx = out_dir / (stem + ".docx")
        # THE PAGE'S OWN BIB COMES FIRST, the same preference the LaTeX export
        # holds (JL 260815: "how about the word? will we have the reference as
        # well?"). md2docx renders citations from a `.board-refs.bbl` beside
        # the .bib, so when the page has a store, cli/refs.py compiles that
        # cache in bibex/ and md2docx is pointed there — in-text labels and
        # the References section then come from the one store the workbench
        # maintains. A page with no store keeps the paper-root fallback.
        try:
            all_units = self._page_units(page_src)
            selected_bib = self._selected_bibliography(page_src, out_dir)
            self._evidence_receipt(page_src, out_dir)
        except (RuntimeError, EvidenceSelectionError, OSError) as exc:
            return None, str(exc)
        proot = self._paper_root(page_src) if legacy_profile(page_src) else None
        own = selected_bib
        if own and own.is_file() and "@" in own.read_text(encoding="utf-8",
                                                  errors="replace"):
            bbl = own.parent / ".board-refs.bbl"
            if not bbl.is_file() or bbl.stat().st_mtime < own.stat().st_mtime:
                refs = PAGE_ENGINE / "cli" / "refs.py"
                # refs.py guards on which("bibtex") against ITS env, so hand
                # it one where the TeX bin is on PATH.
                self._run([sys.executable, str(refs), str(own.parent)],
                          timeout=60,
                          env=dict(os.environ, PATH=_TEXBIN + ":"
                                   + os.environ.get("PATH", "")))
            proot = own.parent
        # THE PAGE'S OWN EVIDENCE RIDES ALONG (JL 260816: "both word and latex
        # didn't include the display?"): md2docx embeds a float on \ref and the
        # board cites by short id, so the bridge is a TEMP copy of the page
        # with `(\ref{<label>})` appended to each unit's first prose mention.
        # The page source is never edited; the temp is deleted after the run.
        units = [(s, u) for s, u in all_units if u["label"]]
        # The same conversion the LaTeX door does (JL 260820: "the word workbench
        # don't have the citation and reference"): a backtick key the page's
        # own bibex defines becomes \citep{key}, which md2docx renders from
        # the compiled .board-refs.bbl — in-text label plus References. Without
        # it the key ships as code text and no citation ever fires.
        import re as _re
        bibkeys = []
        if own and own.is_file():
            bibkeys = _re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,",
                                  own.read_text(encoding="utf-8",
                                                errors="replace"))
        src_for_docx, tmp = page_src, None
        if units or bibkeys:
            lines = page_src.read_text(encoding="utf-8").split("\n")
            lines, display_replaced = self._replace_display_tokens(
                lines, self._display_ref_map(units)
            )
            fence, done = False, set()
            for i, ln in enumerate(lines):
                if ln.lstrip().startswith("```"):
                    fence = not fence
                    continue
                if fence or ln.lstrip().startswith(">"):
                    continue
                for short, u in units:
                    key = u["label"] or u["dir"].name
                    if key in done:
                        continue
                    # The Page may already use the manuscript form
                    # `Table~\ref{tab:x}`. Appending a second reference for the
                    # Word bridge made the reader see `Table 2 (Table 2)` and
                    # printed duplicate Display cards. Only bridge short-id
                    # mentions; an existing `\ref{}` is already sufficient for
                    # Inline to resolve and annotate.
                    if u["label"] and _re.search(
                            r"\\(?:auto|C|c)?ref\{%s\}" %
                            _re.escape(u["label"]), ln):
                        done.add(key)
                        continue
                    hits = [m for alias in u.get("aliases", [short])
                            if (m := re.search(r"(?<![\w-])%s(?![\w-])"
                                              % re.escape(alias), ln))]
                    if hits:
                        m = min(hits, key=lambda hit: hit.start())
                        lines[i] = (ln[:m.end()] + " (\\ref{%s})" % u["label"]
                                    + ln[m.end():])
                        done.add(key)
                        ln = lines[i]
            key_hits = 0
            if bibkeys:
                fence = False
                for i, ln in enumerate(lines):
                    if ln.lstrip().startswith("```"):
                        fence = not fence
                        continue
                    if fence or ln.lstrip().startswith(">"):
                        continue
                    for k in bibkeys:
                        pat = "`%s`" % k
                        if pat in ln:
                            lines[i] = ln = ln.replace(
                                pat, "\\citep{%s}" % k)
                            key_hits += 1
            if done or key_hits or display_replaced:
                tmp = out_dir / (stem + ".export.md")
                tmp.write_text("\n".join(lines), encoding="utf-8")
                src_for_docx = tmp
        # --join-paragraphs: the board's .md is ONE SENTENCE PER LINE, and
        # rendering each line as its own Word paragraph reads as chopped rows
        # (JL 260815: "make it the normal paragraph"). The writer joins each
        # block's sentences into one flowing paragraph instead.
        cmd = [sys.executable, str(_SCRIPTS / "md2docx.py"), str(src_for_docx),
               "-o", str(docx), "--join-paragraphs",
               "--keep-fences",
               "--document-title", self._page_title(page_src)]
        if author:
            cmd += ["--author", author]
        selected_display_dir = None
        if units:
            # the unit index for the page address, and the Display comment
            # bubble beside the Citation ones — the docx's evidence card
            # reads the current v4 Result payload tree; md2docx also retains
            # recursive compatibility for older display roots.
            # Stage exactly the selected units: scanning the whole Results tree
            # lets a historical float with the same label replace the current one.
            import shutil
            selected_display_dir = tempfile.TemporaryDirectory(prefix="page-selected-displays-")
            display_root = Path(selected_display_dir.name)
            for index, (_, unit) in enumerate(units):
                shutil.copytree(unit["dir"], display_root / (str(index) + "-" + unit["dir"].name))
            cmd += ["--display-root", str(display_root),
                    "--lanes", "Citation,Display"]
        if proot:
            cmd += ["--paper-root", str(proot)]
        elif units or not legacy_profile(page_src):
            # md2docx caches rasterized figures under <root>/3-dist/.media;
            # with no paper root, aim that at the DERIVED workbench folder
            cmd += ["--paper-root", str(out_dir)]
        try:
            code, log = self._run(cmd, timeout=120)
        finally:
            if selected_display_dir is not None:
                selected_display_dir.cleanup()
        if tmp is not None:
            try:
                tmp.unlink()
            except OSError:
                pass
        if code != 0 or not docx.is_file():
            return None, "md2docx failed or wrote no fresh .docx:\n" + log[-1500:]
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
                                     body=body + ("<p class='mut'>Evidence: "
                                          + ("legacy migration profile" if legacy_profile(page_src) else "current ledger selection")
                                          + " · <a href='evidence-selection.json'>source record</a></p>") + script),
                        encoding="utf-8")
        return {"ok": True, "url": self._url_of(view), "docx": durl,
                "pdf": self._url_of(pdf) if pdf.is_file() else None}, None
