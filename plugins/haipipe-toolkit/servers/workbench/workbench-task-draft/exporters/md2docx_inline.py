"""Inline text runs (bold, italics, citations, references) and the numbering of displays."""

import re
from md2docx_inputs import detex

# --------------------------------------------------------------- inline

class Inline:
    """Resolves the markers inside one sentence and returns (runs, comments).

    A run is (text, bold). A comment is (anchor_text_or_None, kind, body)."""

    CITE = re.compile(r"\\cite[a-z]*\{([^}]*)\}")
    REF = re.compile(r"\\(?:auto|C|c)?ref\{([^}]*)\}")
    BRACKET_REF = re.compile(r"\b(Table|Figure)\s+\[([^\]]+)\]")
    DISPLAY_PLACEHOLDER = re.compile(
        r"(?:\\|/)(table|figure|algorithm)\s*\{\s*([^}]+?)\s*\}"
    )
    QREF = re.compile(r"\s*\[Q-[A-Za-z0-9]+-\d+\]")
    VALHOLE = re.compile(r"\{VAL:\?[^}]*\}")

    def __init__(self, bbl, displays, numbering, report):
        self.bbl, self.displays = bbl, displays
        self.num = numbering          # {'table': n, 'figure': n, label -> label}
        self.report = report
        self.prose_refs = []          # units a SENTENCE has cited, in order: only these are placed
        self.cited = set()            # citation keys used; empty when no sentence was rendered
        self._captioning = False

    def _cite(self, m):
        keys = [k.strip() for k in m.group(1).split(",") if k.strip()]
        if keys == ["TOADD"]:
            self.report.append(("owed-citation", "\\cite{TOADD} shipped to the reader"))
            return "[CITATION OWED]"
        labels = []
        for k in keys:
            lab = self.bbl.intext.get(k)
            if lab:
                labels.append(lab)
                self.cited.add(k)
            else:
                labels.append(k)
                self.report.append(("unresolved-key", f"{k} is not in .board-refs.bbl"))
        # THE COMMENT CARRIES THE REFERENCE, not just the key (JL 2026-07-27).
        # A coauthor reading a .docx cannot grep a .bib, so a bare `key=` names
        # something they have no way to look up. The reference text comes from
        # `.board-refs.bbl`, which `refs.py` produced by running the PAPER'S OWN
        # .bst, so the format here is whatever the manuscript will actually
        # print. That is the point: nothing is formatted twice, so nothing can
        # disagree. Same principle the in-text label already used.
        lines = []
        for k in keys:
            ref = self.bbl.body.get(k, "").strip()
            lines.append(f"{ref}\n    key={k}" if ref
                         else f"key={k} \u00b7 NO ENTRY in .board-refs.bbl, so no "
                              f"reference can be shown; regenerate it with refs.py")
        # A BLANK LINE BETWEEN REFERENCES. One `\citep{a,b,c}` is one comment,
        # and joining on a single newline ran three references together into a
        # wall the reader had to re-parse to see where one ended (JL 2026-07-28).
        self.pending.append(("Citation", "\n\n".join(lines)))
        return "(" + "; ".join(labels) + ")"

    def _ref(self, m):
        label = m.group(1)
        rec = self.displays.by_label.get(label)
        if not rec:
            self.report.append(("broken-ref", f"\\ref{{{label}}} matches no display unit \\label"))
            self.pending.append(("Display", f"\\ref{{{label}}} resolves to no unit; it compiles to ??"))
            return f"[{label}]"
        n = self.num.assign(rec)
        if not self._captioning and rec["unit"] not in self.prose_refs:
            self.prose_refs.append(rec["unit"])
        self.pending.append(("Display", f"{rec['unit']} · kind={rec['kind']} · label={label}"))
        # THE AUTHOR WRITES THE WORD, \ref SUPPLIES THE NUMBER. That is LaTeX's
        # own division of labour, so prose reads `Table~\ref{tab:x}` and emitting
        # the kind again gave "Table~Table 5" on every cross-reference
        # (JL 2026-07-28). Only name the kind when the prose did not.
        if re.search(r"(?:table|figure)s?[~\s]*$", m.string[:m.start()], re.I):
            return str(n)
        return f"{rec['kind'].capitalize()} {n}"

    def _bracket_ref(self, m):
        kind, slug = m.group(1), m.group(2)
        self.report.append(("placeholder-ref",
                            f"{kind} [{slug}] is a placeholder, not a \\ref{{}}; "
                            f"it names no display unit"))
        self.pending.append(("Display", f"placeholder reference {kind} [{slug}], unresolved"))
        return f"{kind} [{slug}]"

    def _display_placeholder(self, m):
        kind, slug = m.group(1).capitalize(), m.group(2).strip()
        self.report.append(("placeholder-ref",
                            f"{kind} [{slug}] is a pending Page display label"))
        self.pending.append(("Display", f"placeholder reference {kind} [{slug}], unresolved"))
        return f"{kind} [pending: {slug}]"

    def render(self, text):
        self.pending, self.cited = [], getattr(self, "cited", set())
        parts = re.split(r"(`[^`\n]*`)", text)
        for i in range(0, len(parts), 2):
            for hole in self.VALHOLE.findall(parts[i]):
                self.report.append(("owed-value", f"{hole} shipped to the reader"))
            prose = parts[i]
            prose = self.CITE.sub(self._cite, prose)
            prose = self.REF.sub(self._ref, prose)
            prose = self.BRACKET_REF.sub(self._bracket_ref, prose)
            prose = self.DISPLAY_PLACEHOLDER.sub(self._display_placeholder, prose)
            parts[i] = self.QREF.sub("", prose)   # the bracket is bookkeeping
        t = "".join(parts)
        # Inline code is operational text, not typography. Stash it before the
        # prose smart-dash pass so CLI flags such as `--execute` remain exactly
        # executable in the DOCX and its PDF twin.
        code_spans = []

        def _stash_code(m):
            code_spans.append(m.group(1))
            return f"\ue000CODE{len(code_spans) - 1}\ue001"

        t = re.sub(r"`([^`]*)`", _stash_code, t)
        t = t.replace("--", "\u2013")
        for i, code in enumerate(code_spans):
            t = t.replace(f"\ue000CODE{i}\ue001", code)
        # `~` is a non-breaking space, and body prose is not detex'd, so it was
        # printing as a literal tilde inside every "Table~5" (JL 2026-07-28).
        t = t.replace("~", "\u00a0")
        return t, self.pending

    def caption(self, tex):
        """A caption is prose too, so its \\ref{} must resolve. Table 6's read
        "the per-cohort estimates behind Figure fig:discretion-gradient", the
        bare label, because detex strips the command and leaves its argument
        (JL 2026-07-28). Numbering is SHARED with the body, so a caption that
        forward-references a later float still names the number the body will
        give it."""
        self.pending = []            # a caption raises no evidence card
        self._captioning = True      # ...and never places a display (only a sentence does)
        try:
            out = self.REF.sub(self._ref, tex)
        finally:
            self._captioning = False
        self.pending = []
        return detex(out)


class Numbering:
    """Word has no floats, so a number is order of appearance and the
    exporter owns it because it walks the sections in order."""

    def __init__(self):
        self.counts, self.given = {"table": 0, "figure": 0}, {}

    def assign(self, rec):
        u = rec["unit"]
        if u not in self.given:
            self.counts[rec["kind"]] = self.counts.get(rec["kind"], 0) + 1
            self.given[u] = self.counts[rec["kind"]]
        return self.given[u]
