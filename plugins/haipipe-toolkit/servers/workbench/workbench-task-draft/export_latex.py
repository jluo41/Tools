"""📜 Export · POST /_board/latex: md2tex Page TeX, the standalone wrapper, LuaLaTeX.

Part of `ExportMixin` (export.py), which composes it; see export.py for the
writer/door division and where each export lands."""
import os
import sys
import tempfile
from pathlib import Path

from src.evidence_selection import (legacy_profile, EvidenceSelectionError,
                                    page_head)

from live.export_common import _SCRIPTS, _TEXBIN, _VIEW, _esc, _tex_text


class ExportLatexMixin:

    # ---- POST /_board/latex ------------------------------------------
    def export_latex(self, p):
        """{path, file} -> {ok, url, tex, pdf}. md2tex writes Page TeX;
        this caller owns the standalone wrapper and LuaLaTeX compilation."""
        page_src, out_dir, board, err = self._export_target(p, "latex")
        if err:
            return None, err
        old_fragment = page_src.parent / "delivery" / "latex" / (page_src.stem + ".tex")
        if old_fragment.is_file() and old_fragment.parent.resolve() != out_dir.resolve():
            first = old_fragment.read_text(encoding="utf-8", errors="replace").splitlines()
            if not first or not first[0].startswith("% GENERATED from"):
                return None, ("Unmarked old TeX fragment preserved; move its words into the Page "
                              "and adopt before rebuilding Block Delivery: " + page_src.stem)
        p = {**p, **self._canon_ctx(board, p)}   # the view bakes p; make it canonical
        stem = page_src.stem
        title = _tex_text(self._page_title(page_src))
        proot = self._paper_root(page_src)
        try:
            units = self._page_units(page_src)
            selected_bib = self._selected_bibliography(page_src, out_dir)
            self._evidence_receipt(page_src, out_dir)
        except (RuntimeError, EvidenceSelectionError, OSError) as exc:
            return None, str(exc)
        source_for_tex = page_src
        temp_source = None
        label_map = self._display_ref_map(units)
        if label_map:
            source_lines = page_src.read_text(encoding="utf-8", errors="replace").splitlines()
            source_lines, changed = self._replace_display_tokens(source_lines, label_map)
            if changed:
                temp_source = tempfile.TemporaryDirectory(prefix="page-display-export-")
                source_for_tex = Path(temp_source.name) / page_src.name
                source_for_tex.write_text("\n".join(source_lines) + "\n", encoding="utf-8")
        # --keep-fences: a board division is often figure-only, and the paper
        # default (drop sketches) exported it as an empty section (JL 260815).
        # --origin: the temporary copy's revise cards and sibling Sections are the
        # Page's own. accept_dropped_keys (POST body) is md2tex's
        # --accept-dropped-keys: an intended citation drop, explained or refused.
        cmd = [sys.executable, str(_SCRIPTS / "md2tex.py"), str(source_for_tex),
               "--paper-root", str(proot or page_src.parent), "-o", str(out_dir),
               "--keep-fences", "--origin", str(page_src)]
        if p.get("accept_dropped_keys"):
            cmd.append("--accept-dropped-keys")
        try:
            code, log = self._run(cmd, timeout=120)
        finally:
            if temp_source is not None:
                temp_source.cleanup()
        tex = out_dir / (stem + ".tex")
        # A nonzero md2tex exit must FAIL the door (found by the 260820 REVISE
        # pass: two POSTs returned ok:true while re-floating the PREVIOUS
        # conversion, because only the file's existence was checked and a
        # stale .tex from the last run satisfied that).
        # md2tex's refuse-to-regress guard leaves the STALE .tex in place, which
        # satisfies is_file(). On 260908 that cost a full rewrite round: §1's
        # humanizing pass was refused, the POST answered ok:true, and the page kept
        # its old prose through a whole rebuild. Since 261103 a refusal also exits 2;
        # the REFUSED line is checked first so the reply names the dropped keys.
        if "REFUSED" in log:
            return None, "md2tex REFUSED to overwrite the existing section:\n" + log[-1500:]
        if code != 0:
            return None, "md2tex exited %s:\n" % code + log[-1500:]
        if not tex.is_file():
            return None, "md2tex wrote no .tex:\n" + log[-1500:]

        # THE PAGE'S OWN EVIDENCE PRINTS (JL 260816: "both word and latex
        # didn't include the display?"): a unit the prose cites by short id
        # (QPf5's in-sentence citation) is embedded as a real float after the
        # citing paragraph, never inside it — MISQ's first-reference rule, the same one md2tex
        # applies to \ref — re-aimed at the unit's WINNING asset so the
        # wrapper master needs no tikz or renderer package knowledge.
        if units:
            body = tex.read_text(encoding="utf-8")
            # Insert from the last first-reference toward the first. If one
            # paragraph cites Display2 and then Display4, both follow it, and
            # reverse source-order placement keeps them in citation order.
            ranked = []
            for short, u in units:
                mention = self._first_unit_mention(body, u)
                if mention:
                    ranked.append((mention.start(), short, u))
            for _position, short, u in sorted(ranked, reverse=True):
                rel = os.path.relpath(u["dir"], out_dir).replace(os.sep, "/")
                lab = "\\label{%s}\n" % u["label"] if u["label"] else ""
                if (u["kind"] == "table"
                        and (u["dir"] / "assets" / "table-body.tex").is_file()):
                    # Evidence units cite a precise point in the prose.  A
                    # regular top float can leap to the beginning of a later
                    # page, visually preceding the section that introduces
                    # it.  Keep the unit at its first substantive citation.
                    # The table body owns its layout (currently a
                    # threeparttable/tabularx unit).  Do not wrap it in an
                    # outer resizebox: graphicx treats the nested table as a
                    # boxed object and the body can disappear from the
                    # Page-level PDF even though the unit preview is correct.
                    # tabularx already sizes itself to the master's
                    # linewidth, so direct input preserves the headers,
                    # rules, and table notes.
                    note = u.get("note", "")
                    note_block = ("\n\\par\\smallskip\n\\begin{flushleft}\n"
                                  "\\footnotesize\n%s\n\\end{flushleft}\n"
                                  % note if note else "")
                    block = ("\\begin{table}[H]\n\\centering\n"
                             "\\caption{%s}\n%s"
                             "\\input{%s/assets/table-body}\n%s"
                             "\\end{table}"
                             % (u["caption"], lab, rel, note_block))
                elif next((f for f in ("figure.pdf", "figure.png", "figure.jpg")
                           if (u["dir"] / "assets" / f).is_file()), None):
                    # width AND height capped with keepaspectratio, and
                    # [!htbp] instead of [H]: a tall display preview at
                    # fixed width is taller than the text block, and [H]
                    # plants it mid-page anyway, so it overflowed and
                    # clipped the prose after it (JL 260820, Figure 8 on
                    # p.19 plus "其他几个 display 也有这个问题"). [!htbp]
                    # still tries HERE first, so a fitting figure stays at
                    # its citation; only one that cannot fit floats on.
                    # lualatex reads a raster asset directly (JL 260821: a
                    # figure-kind unit rendered to PNG, not PDF, silently
                    # never embedded, because this branch only ever looked
                    # for figure.pdf and fell through to "nothing to print").
                    asset = next(f for f in ("figure.pdf", "figure.png", "figure.jpg")
                                 if (u["dir"] / "assets" / f).is_file())
                    # the figure's legend (its float.tex note) prints under it, as a table's does: without it
                    # a reader never learns what panels, markers or intervals mean (JL 261023 claim check)
                    note = u.get("note", "")
                    note_block = ("\\par\\smallskip\n\\begin{flushleft}\n\\footnotesize\n%s\n\\end{flushleft}\n"
                                  % note if note else "")
                    block = ("\\begin{figure}[!htbp]\n\\centering\n"
                             "\\includegraphics[width=%s,"
                             "height=.7\\textheight,keepaspectratio]"
                             "{%s/assets/%s}\n\\caption{%s}\n%s%s"
                             "\\end{figure}" % (u.get("width") or ".85\\linewidth", rel, asset,
                                                  u["caption"], lab, note_block))
                else:
                    continue          # ⬜ no winning render yet: nothing to print
                m = self._first_unit_mention(body, u)
                if m:
                    at = self._paragraph_end_after(body, m.end())
                    before, after = body[:at].rstrip(), body[at:].lstrip()
                    body = (before + "\n\n" + block +
                            ("\n\n" + after if after else "\n"))
                    # Prose cites a stable display short-id so the board can
                    # locate the unit.  In an exported document, readers see
                    # the conventional Figure/Table reference instead.
                    if u["label"]:
                        noun = "Table" if u["kind"] == "table" else "Figure"
                        # A formal manuscript reference is already in the
                        # correct reader-facing form.  Insert the float but
                        # leave ``\\ref{...}`` untouched; replacing only its
                        # inner label would produce a nested/broken reference.
                        if body[m.start():m.end()].startswith("\\ref{"):
                            continue
                        # A page's source contract is the bare stable id
                        # (``Display1``), but older pages sometimes wrote
                        # ``Figure Display1``.  Normalize that legacy form
                        # too, rather than emitting ``Figure Figure 1`` in a
                        # compiled PDF.
                        prefix = noun + " "
                        start = m.start()
                        if body[max(0, start - len(prefix)):start] == prefix:
                            start -= len(prefix)
                        body = (body[:start] + "%s~\\ref{%s}" % (noun, u["label"])
                                + body[m.end():])
            tex.write_text(body, encoding="utf-8")

        # The wrapper master: article + the few packages a board section uses.
        # natbib only when a real .bib is in reach; a cite-less page needs none.
        # THE PAGE'S OWN BIB COMES FIRST (JL 260815: "convert it to the latex
        # and this one to be cited as well"): bibex/<stem>.bib is the page's
        # citation store, so the PDF cites what the page cites — the paper's
        # 0-*.bib is the fallback for pages that have no store of their own.
        bib = None
        own = selected_bib
        if own and own.is_file() and "@" in own.read_text(encoding="utf-8",
                                                  errors="replace"):
            bib = own
        elif proot and legacy_profile(page_src):
            bibs = sorted(proot.glob("0-*.bib"))
            bib = bibs[0] if bibs else None
        # The two rewrites below repair Markdown prose. A `content-format: latex`
        # Page is already LaTeX: its `\texttt{scikit-learn}` names a library even
        # when a bib key has the same spelling, so it keeps every character.
        latex_source = page_head(page_src, "content-format").lower() == "latex"
        # md2tex leaves a handful of mid-paragraph **bold** runs unconverted
        # (found on QPw00: 5 of them printed literal asterisks). Convert them
        # here, OUTSIDE verbatim only, so fences keep their raw text.
        import re as _re
        body = "" if latex_source else tex.read_text(encoding="utf-8")
        parts = _re.split(r"(\\begin\{verbatim\}.*?\\end\{verbatim\})",
                          body, flags=_re.S)
        for _i in range(0, len(parts), 2):
            # The markers must sit at a word boundary. A regression page
            # writes significance as `12.9024***`, and a pair-anywhere regex
            # reads the 2nd and 3rd star of one coefficient together with the
            # 1st and 2nd of the next, wrapping the prose between them and
            # breaking the \texttt group it started in (QC1-visitlbp: the
            # rival-cells sentence printed in monospace with one star left).
            parts[_i] = _re.sub(r"(?<![\w*])\*\*([^*\n]+?)\*\*(?![\w*])",
                                r"\\textbf{\1}", parts[_i])
        fixed = "".join(parts)
        if fixed != body:
            tex.write_text(fixed, encoding="utf-8")

        # A key the page cites in backticks reaches the PDF as a REAL citation
        # (JL 260820, C4.P8.S2: "reference 为什么没有展现出来"): md2tex renders
        # `key` as \texttt{key}, so no \citep ever fired and bibtex printed
        # nothing. Convert exactly the keys the chosen .bib defines.
        if bib and not latex_source:
            import re as _re
            keys = _re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,",
                               bib.read_text(encoding="utf-8",
                                             errors="replace"))
            body = tex.read_text(encoding="utf-8")
            hit = False
            for k in keys:
                pat = "\\texttt{%s}" % k
                if pat in body:
                    body = body.replace(pat, "\\citep{%s}" % k)
                    hit = True
            if hit:
                tex.write_text(body, encoding="utf-8")
        master = out_dir / (stem + "-master.tex")
        head = ["\\documentclass[11pt]{article}",
                "\\usepackage[margin=1in]{geometry}",
                "\\usepackage{graphicx,booktabs,longtable,float,tabularx,pifont,threeparttable}",
                # A long code span with no internal space (a path, a
                # brace-expansion glob) is one unbreakable TeX word and runs
                # off the margin instead of wrapping; md2tex.py's
                # code_span_tex wraps those in \\seqsplit, which needs this.
                "\\usepackage{seqsplit}",
                # A display unit declares its own packages in its
                # preview.tex, and the master must cover them or the
                # glyph vanishes: nonstopmode turns an undefined
                # \\checkmark into an EMPTY table cell, which is worse
                # than a failed build because the table still prints
                # (QC1-visitlbp Table 1, every shipped/not-shipped mark
                # blank in the page PDF while the unit's own preview.pdf
                # was correct).
                "\\usepackage{amsmath,amssymb}",
                "\\usepackage[hidelinks]{hyperref}",
                # Emoji are the board's mark grammar and Latin Modern has no
                # glyph for any of them; LaTeX drops a missing glyph silently
                # (JL 260820: "emoji 都没有被 compile"). LuaLaTeX + a
                # luaotfload fallback chain prints them: Apple Color Emoji
                # for the pictographs, TeXLive's DejaVu for circled digits
                # and arrows. This is why the compile passes below run
                # lualatex, not xelatex.
                "\\usepackage{fontspec}",
                "\\directlua{luaotfload.add_fallback(\"emojifb\","
                " {\"[/System/Library/Fonts/Apple Color Emoji.ttc]"
                ":mode=harf;\", \"[DejaVuSans.ttf];\"})}",
                "\\setmainfont{Latin Modern Roman}"
                "[RawFeature={fallback=emojifb}]",
                "\\setmonofont{Latin Modern Mono}"
                "[RawFeature={fallback=emojifb}]",
                # A board fence is a DIAGRAM, not prose (JL 260820: "它在这个
                # 里面非常扎眼…找一个框给框起来"). Box every verbatim in a
                # breakable gray-backed frame at \footnotesize so it reads as
                # apparatus beside the text instead of merging into it.
                # fvextra extends fancyvrb with safe line breaking.  Long
                # XML/prompt lines otherwise run past the page edge even
                # though the surrounding tcolorbox is breakable.
                "\\usepackage{fvextra,etoolbox,xcolor}",
                "\\usepackage{tcolorbox}\\tcbuselibrary{breakable}",
                "\\RecustomVerbatimEnvironment{verbatim}{Verbatim}"
                "{fontsize=\\footnotesize,baselinestretch=0.92,"
                "breaklines=true,breakanywhere=true}",
                "\\BeforeBeginEnvironment{verbatim}{\\begin{tcolorbox}"
                "[breakable,colback=black!4,colframe=black!25,"
                "boxrule=0.4pt,arc=2pt,left=4pt,right=4pt,top=1pt,bottom=1pt]}",
                "\\AfterEndEnvironment{verbatim}{\\end{tcolorbox}}"]
        # `latex-preamble: <file>` in the Page head: packages and macros its LaTeX
        # Content needs (a migrated manuscript's subcaption, cleveref, \keywords),
        # read before natbib so the file may pass natbib its options.
        preamble = page_head(page_src, "latex-preamble")
        if preamble:
            pre = (page_src.parent / preamble).resolve()
            if not pre.is_file():
                return None, "latex-preamble not found: %s" % preamble
            head.append("\\input{%s}" % os.path.relpath(pre, out_dir).replace(os.sep, "/"))
        tail = []
        if bib:
            head.append("\\usepackage{natbib}")
            tail += ["\\bibliographystyle{plainnat}",
                     "\\bibliography{%s}" % bib.stem]
        else:
            head.append("\\providecommand{\\citep}[1]{[#1]}"
                        "\\providecommand{\\citet}[1]{[#1]}")
        title_block = ("\\begin{center}\n{\\large\\bfseries %s\\par}\n"
                       "\\end{center}\n\\vspace{0.35em}\n" % title)
        master.write_text(
            "\n".join(head) + "\n\\begin{document}\n" + title_block
            + "\\input{%s}\n" % stem
            + "\n".join(tail) + "\n\\end{document}\n", encoding="utf-8")

        # LuaLaTeX/luaotfload needs a writable cache.  A sandboxed Board
        # process may inherit a read-only user TeX cache, which otherwise
        # makes a valid page fail before the first font is loaded.
        tex_cache = Path(tempfile.gettempdir()) / "haipipe-texmf"
        tex_cache.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, PATH=_TEXBIN + ":" + os.environ.get("PATH", ""))
        env["TEXMFVAR"] = str(tex_cache / "var")
        env["TEXMFCONFIG"] = str(tex_cache / "config")
        env["XDG_CACHE_HOME"] = str(tex_cache / "cache")
        for cache_dir in ("var", "config", "cache"):
            (tex_cache / cache_dir).mkdir(parents=True, exist_ok=True)
        if bib:
            env["BIBINPUTS"] = ".:%s:" % bib.parent
        # First pass lays down display labels; second resolves their in-text
        # Figure/Table references.
        passes = [["lualatex", "-interaction=nonstopmode", master.name],
                  ["lualatex", "-interaction=nonstopmode", master.name]]
        if bib:
            passes += [["bibtex", master.stem],
                       ["lualatex", "-interaction=nonstopmode", master.name],
                       ["lualatex", "-interaction=nonstopmode", master.name]]
        for cmd in passes:
            code, out = self._run(cmd, timeout=180, cwd=out_dir, env=env)
        built = out_dir / (stem + "-master.pdf")
        pdf = out_dir / (stem + ".pdf")
        # THIS run either produced a PDF or it did not, and that is not the same
        # question as "is there a PDF here". Found 260822: a page whose new
        # \input pulled in a table-body using macros declared only in that
        # unit's own preview preamble failed every pass, left the PREVIOUS
        # build's pdf untouched, and this door answered ok:true with a pdf URL
        # and a view saying "compiled by lualatex". The reader was shown a
        # three-minute-old artifact as if it were the one just built. Same shape
        # as the truncation flag that could not fire: a success with no way to
        # fail. The stale file is KEPT -- deleting a reader's last good artifact
        # to punish a compile is worse -- but it is never presented as fresh.
        fresh = built.is_file()
        if fresh:
            built.replace(pdf)
        stale = (not fresh) and pdf.is_file()
        # The workbench folder holds the artifact, not the build's residue: every
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
        if stale:
            body = (btn + "<h1>⚠️ %s · STALE PDF</h1><p class='mut'>lualatex "
                    "produced no PDF on this run, so the file below is from an "
                    "EARLIER build and does not match the source. Log tail:</p>"
                    "<pre>%s</pre>"
                    "<iframe src='%s?t=%d' style='width:100%%;height:60vh;border:2px "
                    "solid #c33;border-radius:8px'></iframe>%s"
                    % (_esc(stem), _esc(out[-1200:] if out else ""),
                       self._url_of(pdf), pdf.stat().st_mtime_ns, src_fold))
        elif pdf.is_file():
            # the mtime rides the frame's URL, so a rebuild's reload can never
            # show a cached PDF as if it were the fresh one
            body = (btn + "<h1>📜 %s</h1><p class='mut'>compiled by lualatex · "
                    "<a href='%s' download>⬇ %s.pdf</a></p>"
                    "<iframe src='%s?t=%d' style='width:100%%;height:78vh;border:1px "
                    "solid var(--line);border-radius:8px'></iframe>%s"
                    % (_esc(stem), self._url_of(pdf), _esc(stem),
                       self._url_of(pdf), pdf.stat().st_mtime_ns, src_fold))
        else:
            body = (btn + "<h1>📜 %s.tex</h1><p class='mut'>lualatex produced no PDF; "
                    "the generated source is below. Log tail:</p><pre>%s</pre>%s"
                    % (_esc(stem), _esc(out[-800:] if out else ""), src_fold))
        view.write_text(_VIEW.format(title=_esc(stem + " · latex"),
                                     body=body + ("<p class='mut'>Evidence: "
                                          + ("legacy migration profile" if legacy_profile(page_src) else "current ledger selection")
                                          + " · <a href='evidence-selection.json'>source record</a></p>") + script),
                        encoding="utf-8")
        if stale:
            return ({"url": self._url_of(view), "tex": self._url_of(tex),
                     "pdf": None, "stale_pdf": self._url_of(pdf)},
                    "lualatex produced no PDF; %s.pdf is from an earlier build "
                    "and does not match the source. Log tail:\n%s"
                    % (stem, (out or "")[-1200:]))
        return {"ok": True, "url": self._url_of(view), "tex": self._url_of(tex),
                "pdf": self._url_of(pdf) if fresh else None}, None
