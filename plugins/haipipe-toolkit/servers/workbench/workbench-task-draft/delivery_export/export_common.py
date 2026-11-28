"""Shared ground of the Page export doors (export.py and its export_* parts):
the writers' folder, the TeX bin, the cite pattern, the small view page, and two escapers."""
import html
import re
from pathlib import Path


# The writers are shared by the Word and LaTeX Page workbenches. They live beside
# those contracts rather than inside a consumer family such as Paper.
_SCRIPTS = Path(__file__).resolve().parents[1] / "exporters"

_TEXBIN = "/Library/TeX/texbin"

# \citep{a,b} · \citet[p.3]{c} · \cite{d} — the keys, however the cite is spelt.
_CITE = re.compile(r"\\cite[pt]?\*?(?:\[[^\]]*\])*\{([^}]+)\}")

_VIEW = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff}}
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


def _tex_text(s):
    """Escape plain page metadata for a small reader-facing LaTeX title."""
    escaped = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(escaped.get(char, char) for char in str(s or ""))
