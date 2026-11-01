"""Find every sNN and every delivery/ folder in the SPACEs on this machine, for the two galleries (b35-s04 the delivery
gallery, b35-s05 the studio gallery; JL 261030: "we might also have a sNN for the gallery of the deliveries, and gallery
of the studios"). Reads folder and file names, and of an sNN only its face's title and **For:** line; never another
file's content, and never `_WorkSpace/`.

    python gallery_scan.py                          counts by level, Theme and kind, and the newest example of each
    python gallery_scan.py --write <sNN> studio     writes <sNN>/delivery/skill/gallery.md, the studio gallery
    python gallery_scan.py --write <sNN> delivery   writes <sNN>/delivery/skill/gallery.md, the delivery gallery

Each gallery's examples are the newest of each kind (JL 261030, "go ahead and do it", on "the newest real one of each
kind from the scan, so each gallery stays current"); an example is never one of the galleries themselves.

studios(): one row per sNN: SPACE, path, level (Project, Block, Job, Task), Theme (work, paper, ...).
deliveries(): one row per delivery/: SPACE, path, whose (sNN, Block, Job, Task, Page, Project), kind (Word + PDF, ...).
"""
from __future__ import annotations

import collections
import os
import re
from pathlib import Path

DESK = Path(__file__).resolve().parents[7].parent           # the folder holding the SPACEs (Desktop)
SPACES = ["Tools", "Physician", "DrFirst", "WellDoc", "REACH", "CDHAI", "HAIChat", "Knowledge"]
SKIP = {".git", "node_modules", "_old", "history", "result", "results", "passes", "_WorkSpace", ".venv", "__pycache__",
        "archive", "_archive", "site-packages", "board", "tests"}   # tests/: fixtures a test writes, never real sNN
WORLDS = ["work", "paper", "insight", "cowork", "design", "labeling", "discovery", "ideation"]
SNN = re.compile(r"^s\d+-")
PROJ = r"^Proj"                                             # Project-X, and WellDoc's and Knowledge's Proj01-X
_cache: dict = {}


def _walk():
    if _cache:
        return _cache["s"], _cache["d"]
    studios, deliveries = [], []
    for sp in SPACES:
        for d, subs, files in os.walk(DESK / f"{sp}-SPACE", followlinks=False):
            p = Path(d)
            subs[:] = sorted(s for s in subs if s not in SKIP and not s.startswith(".") and not s.endswith("-SPACE")
                             and not (p / s).is_symlink())          # a SPACE inside a SPACE is a copy; count it once
            if SNN.match(p.name) and f"{p.name}.md" in files:
                studios.append((sp, p))
                subs[:] = [s for s in subs if s == "delivery"]
            if p.name == "delivery":
                deliveries.append((sp, p))
                subs[:] = []
    _cache.update(s=studios, d=deliveries)
    return studios, deliveries


def level_of(folder: Path) -> str:
    n = folder.name
    if SNN.match(n):
        return "sNN"
    for pat, lv in ((r"^b\d+", "Block"), (r"^j\d+_", "Job"), (r"^t\d+_", "Task"),
                    (r"^(Paper|Insight|Prototype|Design)-", "Block"), (PROJ, "Project")):
        if re.match(pat, n):
            return lv
    if n in WORLDS:
        return "Project"
    return "Page" if (folder / f"{n}.md").is_file() else "other"


def theme_of(path: Path) -> str:
    parts = path.parts
    idx = [i for i, x in enumerate(parts) if re.match(PROJ, x)]
    if not idx or idx[-1] + 1 >= len(parts):
        return "other"
    world = parts[idx[-1] + 1]
    return world if world in WORLDS else ("project" if world == "studio" or SNN.match(world) else "other")


def studios() -> list[dict]:
    rows = []
    for sp, p in _walk()[0]:
        owner = p.parent.parent if p.parent.name == "studio" else p.parent
        rows.append({"space": sp, "path": p, "level": level_of(owner), "theme": theme_of(p), "owner": owner.name,
                     "beside": p.parent.name != "studio", "mtime": (p / f"{p.name}.md").stat().st_mtime})
    return rows


KINDS = ["Word + PDF", "skill", "ui", "LaTeX + PDF", "PDF", "web page", "table", "figure", "deck", "text", "empty"]
# an sNN's main delivery type, named on its face (haipipe-studio, one delivery; JL 261030); the deck is never one
TYPES = ["skill", "ui", "code", "draft", "display", "data"]


def kind_of(folder: Path) -> str:
    files = [f for f in folder.rglob("*") if f.is_file() and f.name not in (".DS_Store", "render.yaml", ".gitkeep")][:3000]
    ext = {f.suffix.lower() for f in files}
    full = lambda sub: any(f.parts[len(folder.parts)] == sub for f in files if len(f.parts) > len(folder.parts) + 1)
    files = [f for f in files if not (len(f.parts) > len(folder.parts) + 1 and f.parts[len(folder.parts)] == "deck")] \
        or files                                          # every sNN has a deck: the kind is what else it holds
    ext = {f.suffix.lower() for f in files}
    for kind, hit in (("Word + PDF", ".docx" in ext), ("skill", full("skill")),
                      ("ui", full("ui")), ("LaTeX + PDF", ".tex" in ext), ("PDF", ".pdf" in ext),
                      ("web page", ".html" in ext), ("table", bool(ext & {".csv", ".tsv", ".xlsx", ".parquet"})),
                      ("figure", bool(ext & {".png", ".svg", ".jpg"})), ("deck", ".pptx" in ext or full("deck")),
                      ("text", bool(files))):
        if hit:
            return kind
    return "empty"


def deliveries() -> list[dict]:
    return [{"space": sp, "path": p, "whose": level_of(p.parent), "theme": theme_of(p), "owner": p.parent.name,
             "kind": kind_of(p), "type": type_of(p.parent), "mtime": p.stat().st_mtime} for sp, p in _walk()[1]]


def type_of(owner: Path) -> str:
    """An sNN's **Delivery type:** word from its face; "" for any other level, or an sNN that names none yet."""
    face = owner / f"{owner.name}.md"
    if not re.match(r"s\d+-", owner.name) or not face.is_file():
        return ""
    m = re.search(r"(?mi)^\*\*Delivery type:\*\*[^\S\n]*`?([A-Za-z]+)", face.read_text(encoding="utf-8", errors="ignore"))
    return m.group(1).lower() if m and m.group(1).lower() in TYPES else ""


def newest(rows, key, val):
    """The most recently changed row with row[key] == val, or None."""
    hits = [r for r in rows if r[key] == val]
    return max(hits, key=lambda r: r.get("mtime") or r["path"].stat().st_mtime) if hits else None


def short(path: Path, space: str) -> str:
    """A path a reader can find: the SPACE, then from the Project (or the SPACE root) on."""
    parts = path.parts
    i = next((k for k in range(len(parts) - 1, -1, -1) if re.match(PROJ, parts[k])), None)
    if i is None:
        i = parts.index(f"{space}-SPACE") + 1
    return f"{space} " + "/".join(parts[i:])


GALLERIES = ("s04-delivery-gallery", "s05-studio-gallery")      # b35's own two: never their own example
GENERATED = "<!-- GENERATED FILE by haipipe-studio scripts/gallery_scan.py --write; rerun it, never edit this -->"
LEVELS = ["Project", "Block", "Job", "Task"]
THEMES = ["work", "paper", "discovery", "cowork", "insight", "design", "labeling", "project"]


def _cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def face_line(path: Path) -> tuple[str, str]:
    """An sNN's title (its face's first line) and its **For:** line, links reduced to their words; '' when missing."""
    lines = (path / f"{path.name}.md").read_text(encoding="utf-8").split("\n")
    title = lines[0].lstrip("# ").strip() if lines else ""
    m = next((ln for ln in lines if ln.startswith("**For:**")), "")
    words = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", m.removeprefix("**For:**").strip())
    return title, ("" if words.startswith("<") else words)


def _example(rows, good=lambda r: True):
    """The newest row that is not a gallery itself, a `good` one first."""
    rows = [r for r in rows if not any(g in r["path"].parts for g in GALLERIES)]
    best = [r for r in rows if good(r)] or rows
    return max(best, key=lambda r: r["mtime"]) if best else None


def _public(r) -> bool:
    """Tools is a public repository, and this gallery renders into it: only a Tools sNN shows its face's words; any
    other SPACE shows its path, never its text."""
    return r["space"] == "Tools"


def studio_md() -> str:
    rows = studios()
    n = collections.Counter((r["level"], r["theme"]) for r in rows)
    side = sum(r["beside"] for r in rows)
    out = [GENERATED, "", "## Where they sit", "",
           f"{len(rows)} sNN in {len(set(r['space'] for r in rows))} SPACEs: {side} sit beside the Jobs or Tasks they "
           f"serve, {len(rows) - side} still in a `studio/` folder. A row is the level an sNN serves, a column its Theme.", "",
           "| level | " + " | ".join(THEMES) + " |", "|---|" + "---:|" * len(THEMES)]
    out += [f"| {lv} | " + " | ".join(str(n[(lv, th)]) if n[(lv, th)] else "\u00b7" for th in THEMES) + " |" for lv in LEVELS]
    out += ["", "## Each kind of sNN", "",
            "The newest sNN at each level and Theme, to copy from: one that names its delivery (a **For:** line) first. "
            "Its title and what it hands over show for a Tools sNN only, since this page is public; any other SPACE "
            "shows its path.", "", "| level | Theme | the newest one | what it hands over |", "|---|---|---|---|"]
    for lv in LEVELS:
        for th in THEMES:
            r = _example([x for x in rows if x["level"] == lv and x["theme"] == th],
                         lambda x: _public(x) and bool(face_line(x["path"])[1]))
            if r:
                title, gives = face_line(r["path"]) if _public(r) else ("", "")
                gives = gives[:160] + ("\u2026" if len(gives) > 160 else "")
                out.append(f"| {lv} | {th} | {_cell(short(r['path'], r['space']))}" + (f"<br>{_cell(title)}" if title else "")
                           + f" | {_cell(gives) if gives else ('none yet' if _public(r) else '(another SPACE: path only)')} |")
    return "\n".join(out) + "\n"


def holds(folder: Path, public: bool) -> str:
    """What a delivery/ holds: at its top, its folder and file names (at most six) for a Tools delivery; for any other
    SPACE only its kinds of file (.docx, .pdf, ...), since a private folder's names can say private things."""
    if not public:
        ext = sorted({f.suffix.lower() for f in folder.rglob("*") if f.is_file() and f.suffix and f.name != ".DS_Store"})
        return "files: " + ", ".join(ext[:8]) + (", \u2026" if len(ext) > 8 else "") if ext else "no files"
    names = sorted((c.name + "/" if c.is_dir() else c.name) for c in folder.iterdir() if not c.name.startswith("."))
    return ", ".join(names[:6]) + (", \u2026" if len(names) > 6 else "")


def delivery_md() -> str:
    rows = deliveries()
    kind, whose = collections.Counter(r["kind"] for r in rows), collections.Counter(r["whose"] for r in rows)
    out = [GENERATED, "", "## Each kind of delivery", "",
           f"{len(rows)} `delivery/` folders in {len(set(r['space'] for r in rows))} SPACEs. A delivery's kind is the "
           "first that fits its files besides `deck/`, which every sNN has: a `.docx` is Word + PDF; a full `skill/` "
           "a skill; a full `ui/` a ui; a `.tex` LaTeX + PDF; then PDF, web page (`.html`), table (`.csv`, `.xlsx`), "
           "figure (`.png`, `.svg`), then a deck when it holds only slides, text; nothing at all is empty.", "",
           "| kind | how many | the newest one | what it holds |", "|---|---:|---|---|"]
    for k in KINDS:
        r = _example([x for x in rows if x["kind"] == k])
        out.append(f"| {k} | {kind[k] or '\u00b7'} | " + (f"{_cell(short(r['path'], r['space']))} | {_cell(holds(r['path'], _public(r)))} |"
                                                           if r else "none yet | |"))
    snn = [r for r in rows if r["whose"] == "sNN"]
    typed = collections.Counter(r["type"] for r in snn if r["type"])
    out += ["", "## Each delivery type", "", f"An sNN names its main delivery type on its face, `**Delivery type:**`: "
            f"{sum(typed.values())} of {len(snn)} sNN deliveries name one so far. The deck is never the type.", "",
            "| type | how many | the newest one |", "|---|---:|---|"]
    for t in TYPES:
        r = _example([x for x in snn if x["type"] == t])
        out.append(f"| {t} | {typed[t] or '\u00b7'} | {_cell(short(r['path'], r['space'])) if r else 'none yet'} |")
    out += ["", "## Whose delivery", "", "The level a `delivery/` belongs to: a Page (a paper Section, a draft), a Task, "
            "a Job, a Block, an sNN or a Project.", "", "| whose | how many | the newest one |", "|---|---:|---|"]
    for w in ["Page", "Task", "Job", "Block", "sNN", "Project"]:
        r = _example([x for x in rows if x["whose"] == w])
        out.append(f"| {w} | {whose[w] or '\u00b7'} | {_cell(short(r['path'], r['space'])) if r else 'none yet'} |")
    return "\n".join(out) + "\n"


def write(topic: Path, which: str) -> Path:
    out = Path(topic) / "delivery" / "skill" / "gallery.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(studio_md() if which == "studio" else delivery_md(), encoding="utf-8")
    return out


if __name__ == "__main__":
    import sys
    if sys.argv[1:2] == ["--write"]:
        print(write(Path(sys.argv[2]), sys.argv[3]))
        raise SystemExit(0)
    s, d = studios(), deliveries()
    print(len(s), "sNN;", collections.Counter((r["level"], r["theme"]) for r in s).most_common())
    print(len(d), "delivery/;", collections.Counter(r["kind"] for r in d).most_common())
    print(collections.Counter(r["whose"] for r in d).most_common())
    for k in KINDS:
        r = newest(d, "kind", k)
        print(k, "->", short(r["path"], r["space"]) if r else "-")
