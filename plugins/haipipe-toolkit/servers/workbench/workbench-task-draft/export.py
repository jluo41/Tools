"""📜📝📚 Export · a page's DERIVED paper-facing workbenches: latex/, word/, bibex/.

THE DIVISION OF LABOUR between a writer and a door:

  the writers (servers/workbench/workbench-task-draft/exporters/)          HOW an export is made
  this file                                                   WHERE it lands, and the door

`md2tex.py` and `md2docx.py` are shared Page-workbench writers and are called by
path, so Word and LaTeX stay two projections of one source. The one writer
authored HERE is the bibex extractor, because
citation-craft.md forbids generating bibtex: it may only SUBSET a `.bib` a person
already wrote, so it is thirty lines of copying and belongs to no other family.

WHERE AN EXPORT LANDS is the category-aware workbench contract
(`workbench`): a folded Page writes Delivery lanes below
`<page-dir>/delivery/<lane>/`, plan lanes below `draft/`, and Studio lanes
below `studio/`. A flat legacy Page may fall back to a board-level lane where
that writer explicitly supports it. `autodeck.py` refuses a flat Page outright.

WHY EVERY OUTPUT GETS AN .html BESIDE IT when the artifact itself cannot be
framed: the surface is a right-pane TAB, and a tab needs a URL a browser can
show. A PDF frames natively; a .tex or .docx does not, so the builder writes a
small view page beside it — derived from the derived, regenerated with it,
never hand-edited.

`--paper-root` IS DISCOVERED, NOT DEMANDED: walk up from the page toward --root
looking for a `0-*.bib`, which is the paper family's own root convention. A page
outside any paper exports cite-less rather than refusing (the roster's rule).
"""
import html  # noqa: F401
import json
import os  # noqa: F401
import re
import subprocess
import sys  # noqa: F401
import tempfile  # noqa: F401
from pathlib import Path

from host_paths import PAGE_ENGINE, SKILLS  # noqa: F401

from src.common import (DELIVERY_LANES, EVIDENCE_LANES, OUTLINE_LANES,
                        STUDIO_LANES,
                        delivery_lane_dir, evidence_lane_dir,
                        evidence_lane_dirs, outline_lane_dir, studio_lane_dir)
from src.page_evidence import (current_display_results,
                               display_result_requires_unit,
                               cited_display_labels,
                               _result_document)  # noqa: F401
from src.evidence_selection import (selected_results, legacy_profile, EvidenceSelectionError,
                                    draft_delivery, page_head, pending_items)  # noqa: F401

from live.export_common import _SCRIPTS, _TEXBIN, _CITE, _VIEW, _esc, _tex_text  # noqa: F401
from live.export_bibliography import ExportBibliographyMixin
from live.export_latex import ExportLatexMixin
from live.export_word import ExportWordMixin
from live.export_bibex import ExportBibexMixin


class ExportMixin(ExportBibliographyMixin, ExportLatexMixin, ExportWordMixin, ExportBibexMixin):
    # The doors live in export_bibliography / export_latex / export_word / export_bibex;
    # this class keeps the shared ground they all call through self.

    # ---- shared ground ------------------------------------------------
    def _export_target(self, p, workbench):
        """-> (page_src, out_dir, url_base, err). Same door as every write:
        `target()` refuses a path outside --root or a board with no board.md."""
        got = self.target(p)
        if got[0] is None:
            return None, None, None, got[1]
        f, board = got
        page_src = Path(board) / f
        if not page_src.is_file() or page_src.suffix != ".md":
            return None, None, None, "not a page .md: %s" % f
        # A folded page owns its material (workbench); a flat page
        # keeps the board-level fallback, which is this door's own.
        page_home = (page_src.parent if page_src.parent.name == page_src.stem
                     else Path(board))
        if workbench in EVIDENCE_LANES:
            out_dir = evidence_lane_dir(page_home, workbench)
        elif workbench in OUTLINE_LANES:
            out_dir = outline_lane_dir(page_home, workbench)
        elif workbench in DELIVERY_LANES:
            out_dir = delivery_lane_dir(page_home, workbench)
        elif workbench in STUDIO_LANES:
            out_dir = studio_lane_dir(page_home, workbench)
        else:
            out_dir = page_home / workbench
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

    def _page_title(self, page_src):
        """The reader's title, from the canonical Markdown H1.

        A leading page id (`S-MISQ-Main-7-Conclusion · §7 Conclusion`) is process
        text in a file a person receives (JL 260928), so the title prints what follows
        it (`§7 Conclusion`); the file name still carries the page id."""
        for line in page_src.read_text(encoding="utf-8", errors="replace").splitlines():
            match = re.match(r"^#\s+(.+?)\s*$", line)
            if match:
                title = match.group(1)
                rest = re.match(r"^%s\s*(?:·|—|–|:|-)\s*(\S.*)$" % re.escape(page_src.stem), title)
                return rest.group(1) if rest else title
        return page_src.stem

    def _page_units(self, page_src):
        """[(short, rec)] for the Page's display Result payloads.

        v4 stores display units under ``results/*/payload/<unit>/``. The
        retired ``outline/evidence/display/`` lane remains a read-only
        compatibility fallback, but must not be the only source: otherwise a
        valid v4 Evidence Space display silently disappears from RD output.
        """
        selected_results(page_src)  # Reject missing/current or ambiguous historical bindings.
        out = []
        stem = page_src.stem
        seen = set()

        def add_float(f, label_keys=()):
            d = f.parent
            identity = d.resolve()
            if identity in seen:
                return
            seen.add(identity)
            tex = f.read_text(encoding="utf-8", errors="replace")
            lab = re.search(r"\\label\{([^}]+)\}", tex)
            if label_keys and not lab:
                raise EvidenceSelectionError(
                    f"{d}: the selected DISPLAY Result has Page labels, but float.tex has no manuscript label"
                )
            kind = re.search(r"\\begin\{(table|figure|algorithm)", tex)
            cap, i = "", tex.find("\\caption{")
            if i >= 0:
                k, depth = i + 9, 1
                while k < len(tex) and depth:
                    depth += (tex[k] == "{") - (tex[k] == "}")
                    k += 1
                cap = tex[i + 9:k - 1].strip()
            note_match = re.search(
                r"\\begin\{flushleft\}(.*?)\\end\{flushleft\}",
                tex, flags=re.S)
            note = note_match.group(1).strip() if note_match else ""
            # A page stem may itself contain hyphens (for example QC1-lbp).
            # The old first-two-segments rule collapsed every display on such
            # a page to the same short id and made placement impossible.
            prefix = stem + "-Display"
            aliases = [d.name]
            if d.name.startswith(prefix):
                number = d.name[len(stem) + 1:].split("-", 1)[0]
                short = stem + "-" + number
                # A Page is a local namespace. Its prose normally says
                # `Display1`, while cross-page material may say
                # `<stem>-Display1`; both address the same unit and the
                # exporter must place it once.
                aliases.extend((short, number))
            else:
                short = "-".join(d.name.split("-")[:2])
                aliases.append(short)
            # A Page may cite the display by its manuscript-facing
            # reference (for example ``\\ref{fig:theory-model}``) rather
            # than by the board short id. Keep that reference as a full
            # alias so the exporter can place the winning asset without
            # rewriting the already-correct Figure reference.
            if lab:
                aliases.extend("\\%s{%s}" % (command, lab.group(1))
                               for command in ("ref", "autoref", "Cref", "cref"))
            # A table unit may carry its tabular inside float.tex, with no
            # assets/table-body.tex (the j01 display Runs of ScalingGlucose,
            # JL 261115: "why the displays are not embeded in the draft?").
            # That inline body, from after the label (or caption) to
            # \end{table}, is the table to print.
            inline_table = ""
            if kind and kind.group(1) == "table" and not (d / "assets" / "table-body.tex").is_file():
                end = tex.rfind("\\end{table}")
                # after the label, else after the caption's closing brace
                start = lab.end() if lab else (i + 9 + len(cap) + 1 if i >= 0 else -1)
                if 0 <= start < end and "\\begin{tabular" in tex[start:end]:
                    inline_table = tex[start:end].strip()
            # A legend Section (Extended Data, Supplementary) prints each
            # display under its own heading: the unit's README names where it
            # prints (`## Placement` then e.g. "Extended Data Fig. 1").
            legend_name = ""
            readme = d / "README.md"
            if readme.is_file():
                pm = re.search(r"(?m)^## Placement\s*\n+\s*(.+?)\s*$",
                               readme.read_text(encoding="utf-8", errors="replace"))
                if pm and re.match(r"(?:Extended Data|Supplementary) (?:Fig\.|Figure|Table) ", pm.group(1)):
                    legend_name = pm.group(1)
            has_output_asset = (
                ((d / "assets" / "table-body.tex").is_file() or bool(inline_table))
                if kind and kind.group(1) == "table"
                else any((d / "assets" / asset).is_file()
                         for asset in ("figure.pdf", "figure.png", "figure.jpg"))
            )
            if not has_output_asset and not legacy_profile(page_src):
                raise EvidenceSelectionError(f"Selected DISPLAY unit has no output asset: {d}")
            if has_output_asset:
                aliases.extend(label_keys)
            out.append((short,
                        {"dir": d, "label": lab.group(1) if lab else None,
                         "kind": ("table" if kind and kind.group(1) == "table"
                                  else "figure"),
                         "caption": cap, "note": note, "aliases": aliases,
                         # the unit's own width, from its float.tex (JL 261113: two figures on a 2-page LOI)
                         "width": (re.search(r"\\includegraphics\[[^\]]*width=([^,\]]+)", tex) or [None, None])[1],
                         "has_output_asset": has_output_asset,
                         "inline_table": inline_table, "legend_name": legend_name}))

        # Current typed Results are the sole source once a Page has one. A
        # broken pointer fails closed in both delivery exports instead of
        # silently falling back to a retired folder that may describe stale
        # evidence.
        result_records, has_typed_results = current_display_results(page_src)
        if has_typed_results:
            for record in result_records:
                unit = record["unit"]
                if unit is None:
                    if record.get("selection_error"):
                        raise EvidenceSelectionError(
                            f"Current DISPLAY Result {record['item']} has an invalid binding: "
                            f"{record['selection_error']}"
                        )
                    status = record["status"].replace("_", " ")
                    raw_unit = record["unit_ref"]
                    requires_unit = display_result_requires_unit(status)
                    if raw_unit or requires_unit:
                        detail = (f"payload.unit {raw_unit!r} does not resolve inside this Result's payload/"
                                  if raw_unit else
                                  f"status is {status!r}, but payload.unit is missing")
                        manifest_path = record["manifest"].relative_to(page_src.parent)
                        raise RuntimeError(
                            f"Current DISPLAY Result {record['item']} "
                            f"({manifest_path}) "
                            f"cannot be assembled: {detail}."
                        )
                    continue
                if not legacy_profile(page_src):
                    try:
                        unit.resolve().relative_to((record["manifest"].parent / "payload").resolve())
                    except ValueError as exc:
                        raise EvidenceSelectionError(f"{record['item']}: unit leaves its selected Result payload") from exc
                f = unit / "float.tex"
                if not f.is_file():
                    raise EvidenceSelectionError(f"{record['item']}: selected DISPLAY float.tex is missing")
                kind = "table" if re.search(r"\\begin\{table\b", f.read_text(
                    encoding="utf-8", errors="replace")) else "figure"
                macros = ("table",) if kind == "table" else ("figure", "algorithm")
                aliases = [rf"\{macro}{{{key}}}"
                           for key in record["labels"] for macro in macros]
                add_float(f, aliases)
        else:
            # Read-only migration path for Pages without a typed DISPLAY Result.
            for ddir in evidence_lane_dirs(page_src.parent, "display"):
                for f in sorted(ddir.glob("*/float.tex")):
                    add_float(f)
        if not legacy_profile(page_src):
            cited = cited_display_labels(
                page_src.read_text(encoding="utf-8", errors="replace")
            )
            bound = set()
            for _short, record in out:
                for alias in record["aliases"]:
                    match = re.fullmatch(
                        r"\\(?:figure|table|algorithm)\{(D_[A-Za-z][A-Za-z0-9_-]*)\}",
                        alias,
                    )
                    if match:
                        bound.add(match.group(1))
            missing = sorted(cited - bound)
            if missing:
                raise EvidenceSelectionError(
                    "Page cites DISPLAY label(s) absent from the selected current Results: "
                    + ", ".join(missing)
                )
        return out


    @staticmethod
    def _display_ref_map(units):
        r"""Map ready Page D_ labels to the unit's manuscript ``\label``."""
        out = {}
        for _short, unit in units:
            if not unit.get("label") or not unit.get("has_output_asset"):
                continue
            for alias in unit.get("aliases", []):
                match = re.fullmatch(
                    r"\\(?:figure|table|algorithm)\{(D_[A-Za-z][A-Za-z0-9_-]*)\}",
                    alias,
                )
                if match:
                    out.setdefault(match.group(1), unit["label"])
        return out

    @staticmethod
    def _replace_display_tokens(lines, label_map):
        """Replace resolved Page placeholders only in prose, never examples."""
        if not label_map:
            return lines, False
        fence = False
        changed = False
        token_re = re.compile(
            r"\\(?:figure|table|algorithm)\s*\{\s*(D_[A-Za-z][A-Za-z0-9_-]*)\s*\}"
        )
        out = []
        for line in lines:
            if line.lstrip().startswith("```"):
                fence = not fence
                out.append(line)
                continue
            if fence or line.lstrip().startswith(">"):
                out.append(line)
                continue
            parts = re.split(r"(`[^`\n]*`)", line)
            for i in range(0, len(parts), 2):
                def replace(match):
                    nonlocal changed
                    label = label_map.get(match.group(1))
                    if not label:
                        return match.group(0)
                    changed = True
                    return r"\ref{%s}" % label
                parts[i] = token_re.sub(replace, parts[i])
            out.append("".join(parts))
        return out, changed

    def _first_unit_mention(self, body, unit):
        """Return the first reader-facing mention of a Display unit.

        The source order, not the folder's numeric order, owns first-reference
        placement.  Metadata comments and examples inside verbatim fences are
        not citations.
        """
        hits = []
        for alias in unit.get("aliases", []):
            hits += list(re.finditer(r"(?<![\w-])%s(?![\w-])"
                                    % re.escape(alias), body))
        for match in sorted(hits, key=lambda hit: hit.start()):
            before = body[:match.start()]
            if (before.count("\\begin{verbatim}")
                    > before.count("\\end{verbatim}")):
                continue
            line_start = body.rfind("\n", 0, match.start()) + 1
            if body[line_start:match.start()].lstrip().startswith("%"):
                continue
            return match
        return None

    # a paragraph ends at a blank line, or where a heading or another float begins
    _PARAGRAPH_END = re.compile(
        r"\n[ \t]*(?:\n|(?=\\(?:(?:sub)*section|paragraph)\*?\{|\\begin\{(?:table|figure)\}))")

    @classmethod
    def _paragraph_end_after(cls, body, start):
        """Return the end of the paragraph containing a display reference.

        A float follows the paragraph that first cites it and never splits one
        (MISQ's first-reference rule; the S-MISQ-Main-5-Results session, 260928).
        Placing it after the citing SENTENCE cut the paragraph in two: its
        remaining sentences printed after the float as a new, orphaned paragraph.
        """
        match = cls._PARAGRAPH_END.search(body, start)
        return match.start() if match else len(body)

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
        # The Word comments carry a person's name, so the Word rebuild ASKS who
        # is annotating (md2docx: "The caller is expected to ASK ... rather than
        # assume"). The answer is remembered in this browser only.
        ask = ("""
  var KEY = 'haipipe-word-author', prev = '';
  try { prev = localStorage.getItem(KEY) || ''; } catch (e) {}
  var who = window.prompt('Name to show on the Word comments (leave empty for haipipe):', prev);
  if (who === null) return;
  who = who.trim();
  try { localStorage.setItem(KEY, who); } catch (e) {}
  if (who) body.author = who;""" if route == "word" else "")
        script = ("""<script>
document.getElementById('rebuild').onclick = function () {
  var b = this, body = {path: %s, file: %s};%s
  b.disabled = true; b.textContent = '⏳ rebuilding…';
  fetch('/_board/%s', {method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)})
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (j.ok) { location.reload(); return; }
      alert('⚠ ' + (j.err || 'rebuild failed'));
      b.disabled = false; b.textContent = '🔄 rebuild';
    })
    .catch(function (e) { alert('⚠ ' + e);
      b.disabled = false; b.textContent = '🔄 rebuild'; });
};
</script>""" % (json.dumps(p.get("path") or ""),
                json.dumps(p.get("file") or ""), ask, route))
        return btn, script
