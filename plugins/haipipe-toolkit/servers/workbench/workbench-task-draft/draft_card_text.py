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


def ref_names(folder) -> dict:
    """{label: its number} for every display unit of this Section's version ("fig:research-design": "2", "tab:icd-codes":
    "C3"), from each unit's `shown as` / `number:` name, "Figure 2" or "Appendix Table C3"; LaTeX's \\ref prints the number."""
    from live.draft_step_evidence_display import _units
    out = {}
    for t in [folder] + sorted(x for x in folder.parent.glob("t*") if x.is_dir() and x != folder):
        for u in _units(t):
            num = (re.search(r"(\S+)\s*$", u["shown"] or "") or [None, ""])[1]
            for label in u["labels"] if num else ():
                out.setdefault(label, num)
    return out


def ref_text(html: str, refs: dict) -> str:
    """Each \\ref{label} / \\autoref in the visible text printed as its number ("Figure 2"); an unknown label stays a key,
    and attributes keep the raw words."""
    if "\\ref{" not in html or not refs:
        return html
    def seg(m):
        t = m.group(1)
        t = re.sub(r"\\(?:auto|c|C)?ref\{([^}]*)\}", lambda r: f'<span class=cite-ref title="{r.group(1)}">'
                   f'{refs.get(r.group(1), r.group(1))}</span>' if r.group(1) in refs else r.group(0), t)
        return ">" + t + "<"
    return re.sub(r">([^<]*)<", seg, html)
