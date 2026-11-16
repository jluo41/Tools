"""A Page's DISPLAY Results as a reader meets them (must-check M-D18): each `results/<id>/result.yaml` of `type: DISPLAY`
names its unit under `payload/` (`payload: unit: Display1-study-overview`), and the unit's `float.tex` holds its
\\label, caption and kind; its README's `## Placement` (or `shown as:`) says what the text calls it ("Figure 1").

The one lookup both readers use: the web lane (page_workspace.render_page, `web_figures`) and the Draft Lab server
(servers/workbench/workbench-task-draft/draft_step_evidence_display.py `_units`, draft_card_text.py `ref_names`).
The selection rule mirrors src/page_evidence.current_display_results (payload.unit resolved only inside its own
Result's payload/), read without the ledger, so a reader never fails on a Page the export would refuse.
"""
from __future__ import annotations

import base64
import re
from html import escape
from pathlib import Path

from .float_image import alt_text, float_png, float_source, run_dir

CALL = re.compile(r"\b(?:Extended Data |Supplementary )?(?:Table|Figure)\s+[A-Z]?\d+[A-Za-z]?\b")
REF = re.compile(r"\\(?:auto|c|C)?ref\{([^}]*)\}")
TIED = re.compile(r"~?\\(?:auto|c|C)?ref\{([^}]*)\}")
# the word LaTeX leaves before \ref ("Fig. \ref{x}" prints "Fig. 2"); without it the reader gets the whole name
NAMED = re.compile(r"(?:Fig|Figs|Figure|Figures|Table|Tables|Extended Data Fig|Extended Data Table)\.?[\s~]*(?:\\,)?$", re.I)


def _top(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.*?)\s*$", text)
    return m.group(1).strip().strip("'\"") if m else ""


def _payload_unit(text: str) -> str:
    m = re.search(r"(?m)^payload:\s*\n((?:[ \t]+.*\n?)+)", text)
    u = re.search(r"(?m)^\s+unit:\s*(.*?)\s*$", m.group(1)) if m else None
    return u.group(1).strip().strip("'\"") if u else ""


def run_name(source: str) -> str:
    """"t01 r06" for `j01_evidence_display/t01_q00-study-overview/runs/r06_…/result`: the Task and Run that made it."""
    t = re.search(r"(?:^|/)(t\d+)[^/]*/runs/(r\d+)", source or "")
    return f"{t.group(1)} {t.group(2)}" if t else ""


def _alt(tex: str) -> str:
    """The float's caption as plain words, for an image's alt only (a display box shows the typeset caption, never
    this rebuilt one)."""
    i = tex.find("\\caption{")
    if i < 0:
        return ""
    k, depth = i + 9, 1
    while k < len(tex) and depth:
        depth += (tex[k] == "{") - (tex[k] == "}")
        k += 1
    return alt_text(tex[i + 9:k - 1])


def plain(tex: str) -> str:
    """A caption's words without LaTeX (alt text only): see src/float_image.alt_text."""
    return alt_text(tex)


def _shown(readme: str, tex: str, name: str) -> str:
    """What the text calls the unit: `shown as:`, else its README Placement or heading, else its float's kind and
    number (Display2 in a figure float reads "Figure 2")."""
    m = re.search(r"(?mi)^\s*shown as\s*:\s*(.+?)\s*$", readme)
    if m:
        return m.group(1)
    place = re.search(r"(?ms)^##\s*Placement\s*\n(.*?)(?=^## |\Z)", readme)
    hit = CALL.search(place.group(1)) if place else None
    if hit:
        return hit.group(0)
    n = re.match(r"Display(\d+)", name)
    kind = re.search(r"\\begin\{(table|figure)", tex)
    return f"{kind.group(1).title()} {n.group(1)}" if n and kind else ""


def result_units(task) -> list:
    """Each DISPLAY Result of the Page Folder `task`, in Result order: {dir, item, manifest, labels, shown, number,
    kind, alt, pic, pdf, float, run, source, status}. `float` is the PDF whose page 1 the reader sees (float.pdf, else
    the display Run's result/float.pdf, else preview.pdf); `alt` the caption's words for an image's alt only.
    A Result whose payload.unit leaves its payload/ is skipped."""
    out = []
    task = Path(task)
    for manifest in sorted((task / "results").glob("*/result.yaml"), key=lambda p: [int(x) if x.isdigit() else x
                                                                             for x in re.split(r"(\d+)", p.parent.name)]):
        try:
            text = manifest.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        item = _top(text, "item")
        kind = _top(text, "type").upper()
        if kind not in ("DISPLAY", "TABLE") and not (not kind and re.search(r"-(?:DISPLAY|TABLE)-", item, re.I)):
            continue
        raw = _payload_unit(text)
        payload = (manifest.parent / "payload").resolve()
        unit = (manifest.parent / "payload" / raw).resolve() if raw else None
        if not unit or not unit.is_dir() or payload not in unit.parents:
            continue
        tex = (unit / "float.tex").read_text(encoding="utf-8", errors="replace") if (unit / "float.tex").is_file() else ""
        readme = (unit / "README.md").read_text(encoding="utf-8", errors="replace") if (unit / "README.md").is_file() else ""
        shown = _shown(readme, tex, unit.name)
        pic = next((x for x in (unit / "preview.png", unit / "assets" / "figure.png", unit / "assets" / "figure.svg")
                    if x.is_file()), None)
        source = _top(text, "source")
        out.append({"dir": unit, "item": item, "manifest": manifest, "source": source, "run": run_name(source),
                    "labels": set(re.findall(r"\\label\{([^}]+)\}", tex)), "shown": shown,
                    "number": (re.search(r"(\S+)\s*$", shown) or [None, ""])[1] if shown else "",
                    "kind": "table" if re.search(r"\\begin\{table", tex) else "figure", "alt": _alt(tex),
                    "pic": pic, "pdf": unit / "preview.pdf" if (unit / "preview.pdf").is_file() else None,
                    "float": float_source(unit, run_dir(manifest, source)), "status": _top(text, "status")})
    return out


def ref_map(task) -> dict:
    """{label: "Figure 1"} for the Page and the other Sections of its version (an Extended Data Section's units
    answer the Results' \\ref too); this Page's unit wins."""
    task = Path(task)
    out = {}
    for t in [task] + sorted(x for x in task.parent.glob("t*") if x.is_dir() and x != task):
        for u in result_units(t):
            for label in u["labels"] if u["shown"] else ():
                out.setdefault(label, u["shown"])
    return out


def ref_words(text: str, refs: dict, wrap=None) -> str:
    """Each known \\ref{label} as LaTeX prints it: the number after a "Fig." or "Table" the text writes, else the whole
    name ("Figure 2"). `wrap(label, words)` may wrap the words (a hover span); an unknown label stays as it is."""
    def one(m):
        name = refs.get(m.group(1))
        if not name:
            return m.group(0)
        words = name.split()[-1] if NAMED.search(text[max(0, m.start() - 30):m.start()]) else name
        tie = "\u00a0" if m.group(0).startswith("~") else ""      # LaTeX's ~ is a space that does not break
        return tie + (wrap(m.group(1), words) if wrap else words)
    return TIED.sub(one, text)


def _data_uri(pic) -> str:
    if not pic or pic.stat().st_size > 4_000_000:
        return ""
    mime = "image/svg+xml" if pic.suffix == ".svg" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(pic.read_bytes()).decode("ascii")


def web_figures(html: str, task) -> str:
    """The web lane's reading of displays: each \\ref{label} prints "Figure N" (or N after "Fig."), and each unit is
    embedded once, after the first paragraph that calls it: the typeset float (page 1 of float.pdf, else of preview.pdf
    cut to its float; src/float_image.py), else its preview image, inlined as results/ is never copied into a static
    export; under it one line, its name and Run. No caption is rebuilt in HTML (M-D18). Only text between tags
    changes."""
    units = {lab: u for u in result_units(task) for lab in u["labels"] if u["shown"]}
    refs = ref_map(task)
    if "\\ref" not in html or not refs:
        return html
    seen, out, pos = set(), [], 0
    for m in re.finditer(r"(?s)<p\b[^>]*>.*?</p>", html):
        block = m.group(0)
        if "\\ref" not in block:
            continue
        labels = [r.group(1) for r in REF.finditer(block)]
        new = re.sub(r">([^<]*)<", lambda s: ">" + ref_words(s.group(1), refs) + "<", block)
        figs = ""
        for lab in labels:
            u = units.get(lab)
            if not u or id(u) in seen:
                continue
            seen.add(id(u))
            src = _data_uri(float_png(u["float"]) if u["float"] else None) or _data_uri(u["pic"])
            img = (f'<img src="{src}" alt="{escape(u["alt"] or u["shown"])}" style="width:100%;display:block;margin:8px 0">'
                   if src else "")
            line = " · ".join(x for x in (u["shown"], u["run"]) if x)
            figs += (f'<figure class="page-display" id="{escape(lab)}" style="margin:12px 0">{img}'
                     f'<figcaption style="font-size:.85em;color:#666">{escape(line)}</figcaption></figure>')
        out.append(html[pos:m.start()] + new + figs)
        pos = m.end()
    return "".join(out) + html[pos:]
