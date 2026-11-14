"""The leaf text helpers every paper module shares: escape, clean a Markdown cell, read a file, a face scalar,
table rows, `### N · Title` divisions, the Outline link, and the version and Task stem patterns. Imports nothing
from live.paper*, so any paper module may import it at its top; paper.py re-exports every name."""
import html
import re
from pathlib import Path
from urllib.parse import quote

_EV_RE = re.compile(r"\bE\d{2}-(?:VALUE|CITE|DISPLAY|TABLE)-[A-Za-z0-9-]+")
_DIV_RE = re.compile(r"^###\s+§?(\d+)\s*·\s*(.*?)\s*$")
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")


# ---------------------------------------------------------------- text helpers
def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def clean(cell):
    """Markdown cell → plain text: links to their label, no emphasis marks."""
    cell = _LINK_RE.sub(r"\1", cell or "")
    cell = re.sub(r"[*`]+", "", cell)
    cell = re.sub(r"(?<!\w)_+([^_\n]+?)_+(?!\w)", r"\1", cell)   # _emphasis_ only: an id keeps its _ (t01_introduction)
    return re.sub(r"\s+", " ", cell).strip()


def scalar(text, key, default=""):
    m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(key), text or "", re.M)
    return m.group(1) if m else default


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def table_rows(text, first_cell):
    """Every `| a | b |` row whose first cell matches `first_cell` (regex), as
    lists of cleaned cells. Header and rule rows never match a data pattern."""
    pat = re.compile(first_cell)
    rows = []
    for line in (text or "").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [clean(c) for c in s.strip("|").split("|")]
        if cells and pat.fullmatch(cells[0]):
            rows.append(cells)
    return rows


def divisions(text):
    """`### N · Title` headings under `## Content` → [(n, title)]."""
    out, inside = [], False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            continue
        m = _DIV_RE.match(line) if inside else None
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def outline_url(path_param, rel_file, lens="div", **extra):
    url = "/_board/draft?path=%s&file=%s&lens=%s" % (
        quote(path_param, safe=""), quote(str(rel_file), safe=""), quote(lens, safe=""))
    for k, v in extra.items():
        if v:
            url += "&%s=%s" % (k, quote(str(v), safe=""))
    return url


SECTION_ROW = r"(?:S-[\w-]+|t\d{2}_[\w-]+)(?:\s*(?:\(.*\)|·.*))?"      # S-<desk>-… or a version's tNN_<title>


VERSION_DIR = re.compile(r"^j(\d{2})_(?:writing_)?v(\d+)_(.+)$")     # a version Job on the ladder: j01_v<MMDD>_<desk>/
# A version's Tasks by series (JL 261007, "no more S-xxx"): t00-t19 Main (t00 the Abstract), t20-t29 Appendix
# (A = t21), t30-t39 letters and comment batches. The older S-<desk>-<Main|Appendix>-… and RD<NN>-/CM<NN>- stems
# stay readable.
TASK_STEM = re.compile(r"^t(\d{2})_(.+)$")


def _task_n(stem):
    m = TASK_STEM.match(stem)
    return int(m.group(1)) if m else None


def is_section(stem):
    n = _task_n(stem)
    return stem.startswith("S-") or (n is not None and n < 30)


def is_batch(stem):
    n = _task_n(stem)
    return stem.startswith(("RD", "CM")) or (n is not None and 30 <= n < 40)


def part_of(stem):
    """main or appendix, from an S- stem's -Appendix- or a tNN_ stem's number band."""
    n = _task_n(stem)
    return "appendix" if "-Appendix-" in stem or (n is not None and 20 <= n < 30) else "main"


def task_num(stem):
    """The number a Section prints: a tNN_ Main → N ('' for the Abstract t00), an Appendix t2N → its letter."""
    n = _task_n(stem)
    if n is None:
        return ""
    return "" if n == 0 else str(n) if n < 20 else chr(ord("A") + n - 21) if 21 <= n < 30 else ""
