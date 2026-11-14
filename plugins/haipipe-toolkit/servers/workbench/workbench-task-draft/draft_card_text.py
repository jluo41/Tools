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
        t = re.sub(r"\\citep?\{([^}]*)\}", lambda c: "<span class=cite>[" + "; ".join(
            k.strip() for k in c.group(1).split(",") if k.strip()) + "]</span>", t)
        return ">" + _cite_names(t, d) + "<"
    return re.sub(r">([^<]*)<", seg, html)
