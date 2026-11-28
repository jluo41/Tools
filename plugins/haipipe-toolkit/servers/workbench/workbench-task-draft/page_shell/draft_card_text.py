"""A Draft Lab card's visible words as the reader sees them: citations in author-year form (the sentences already print
them so; draft_step_evidence._cite_names), never as LaTeX."""
import re

from live.draft_step_evidence import _cite_names


def cite_text(html: str, d: dict) -> str:
    """A card's visible words with each \\citep / \\citet printed as the sentence prints it, "(Butler et al. 1998)" or
    "Butler et al. (1998)", its keys on hover. Only text between tags changes: an attribute keeps the raw words that ✓ Use
    this compares with the draft, and the source files keep \\citep for the LaTeX build."""
    if "\\cite" not in html:
        return html
    def seg(m):
        t = m.group(1)
        if "\\cite" not in t:
            return m.group(0)
        t = re.sub(r"\\citep?\*?\{([^}]*)\}", lambda c: "<span class=cite>[" + "; ".join(
            k.strip() for k in c.group(1).split(",") if k.strip()) + "]</span>", t)
        return ">" + _cite_names(t, d, marks=False) + "<"   # a card's old key: plain text, no mark
    return re.sub(r">([^<]*)<", seg, html)


def ref_names(folder) -> dict:
    """{label: its name} for every display unit of this Section's version ("fig:research-design": "Figure 2",
    "tab:icd-codes": "Appendix Table C3"), from each unit's `shown as` / `number:` name or Placement, in display/, a
    display Run's pass or a DISPLAY Result (results/<id>/payload/<unit>/, src/result_displays.py)."""
    from live.draft_step_evidence_display import _units
    out = {}
    for t in [folder] + sorted(x for x in folder.parent.glob("t*") if x.is_dir() and x != folder):
        for u in _units(t):
            for label in u["labels"] if (u["shown"] or "").strip() else ():
                out.setdefault(label, u["shown"].strip())
    return out


def ref_text(html: str, refs: dict) -> str:
    """Each \\ref{label} / \\autoref in the visible text as LaTeX prints it: the number after the text's own "Fig."
    ("Fig. 2"), else the whole name ("Figure 2"), the label on hover (src/result_displays.ref_words, the web lane's
    reading too); an unknown label stays a key, and attributes keep the raw words."""
    if "ref{" not in html or not refs:
        return html
    from src.result_displays import ref_words
    wrap = lambda label, words: f'<span class=cite-ref title="{label}">{words}</span>'
    return re.sub(r">([^<]*)<", lambda m: ">" + ref_words(m.group(1), refs, wrap) + "<", html)
