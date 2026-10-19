"""A paper Board's related-work topics, in the s10-s19 band (haipipe-paper-related; JL 261019: "for the related work
we can do things like s10-related-work, and after that, we have s11 s12, etc").

    python related_topics.py map   <board>                              studio/s10-related-work-map/, the map
    python related_topics.py group <board> --type '<type>' --slug <s>  the next free s11-s19, one type of closest work
                                   [--title '<title>'] [--offline]      (its rows' feeds and references filled)
                                   [--background]                       a read type of Shared background rows
    python related_topics.py feeds <board>                              every row's s10-s19 feeds, from the topics
    python related_topics.py check <board>                              every Closest row placed, typed and read
    python related_topics.py band  <board> [--apply]                    move an older Board's related-work topics
                                                                         into s10-s19 (the map first); dry run first

A row of `related/related.md` is closest work when its `bears on` cell names `Closest: <type>`; the type is the
s1N topic it is read in. `map` and `group` write the face and a forwarding builder, add the `Related work` Studio
group, and draw once. `band` renames the folders, their files, their soft Runs (runs/run-draw-sNN/) and every
mention in the Board's own files in one pass, writes `renamed-from: <old name>` into each moved face (an old link
still opens, frame_view.renamed), then redraws each topic.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import related_map as rm  # noqa: E402

MAP_NN, BAND = 10, range(11, 20)
GROUP = "Related work"
GENERATED = (".excalidraw", ".png", ".jpg", ".jpeg", ".pdf", ".gif", ".mp4", ".zip", ".parquet")
NAME = re.compile(r"^s(\d+)[-_](.+)$")
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
# a paper row's columns: haipipe-related's six, then what a paper adds (paper-ladder.md: key · venue · why here · read)
COLUMNS = ["kind", "date", "item", "link", "feeds", "group", "bears on", "key", "venue", "why here", "read", "source"]
ABBR = ("U.S", "U.K", "e.g", "i.e", "et al", "vs", "Dr", "No", "Fig", "approx", "St")


# ── the Board's topics ─────────────────────────────────────────────────────────────────────────────────────
def topics(board: Path) -> dict[int, Path]:
    """{NN: folder} of the Board's studio topics."""
    studio = board / "studio"
    out = {}
    for p in sorted(studio.iterdir()) if studio.is_dir() else []:
        m = NAME.match(p.name)
        if p.is_dir() and m:
            out[int(m.group(1))] = p
    return out


def face(topic: Path) -> Path:
    return topic / f"{topic.name}.md"


def tags(topic: Path) -> list[str]:
    m = re.search(r"^\*\*Tags:\*\*(.*)$", face(topic).read_text(encoding="utf-8"), re.M) if face(topic).is_file() else None
    return re.findall(r"`([^`]+)`", m.group(1)) if m else []


def is_map(topic: Path) -> bool:
    text = face(topic).read_text(encoding="utf-8") if face(topic).is_file() else ""
    return "```yaml\nmap:" in text or topic.name.endswith("related-work-map")


def related_topics(board: Path) -> dict[int, Path]:
    return {nn: t for nn, t in topics(board).items() if GROUP in tags(t)}


def add_group(board: Path) -> None:
    """The `Related work` button on the Studio's bar (studio/_groups.txt keeps the order)."""
    groups = board / "studio" / "_groups.txt"
    text = groups.read_text(encoding="utf-8") if groups.is_file() else (
        "# Studio groups of this level, in button order. The workbench writes this file when a group is\n"
        "# made, moved or deleted; a group's topics are the ones whose **Tags:** line names it.\n")
    if GROUP not in [x.strip() for x in text.splitlines()]:
        groups.write_text(text.rstrip("\n") + f"\n{GROUP}\n", encoding="utf-8")


# ── related/related.md: its columns and its feeds cells ────────────────────────────────────────────────────
def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _line(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def ensure_columns(board: Path) -> list[str]:
    """The paper columns the table lacks, added at its right with empty cells (a Board's first related.md may hold
    meetings and files only: six columns). Makes the table when there is none. Returns the columns added."""
    table = board / "related" / "related.md"
    if not table.is_file():
        table.parent.mkdir(parents=True, exist_ok=True)
        table.write_text(f"# {board.name} · related\n\nWhat came in from outside for this paper, kept once as it came: "
                         f"one row per item (haipipe-related).\n\n{_line(COLUMNS)}\n{_line(['---'] * len(COLUMNS))}\n",
                         encoding="utf-8")
        return COLUMNS
    lines = table.read_text(encoding="utf-8").split("\n")
    at = next((i for i, x in enumerate(lines) if x.startswith("|")), None)
    if at is None:
        lines += ["", _line(COLUMNS), _line(["---"] * len(COLUMNS))]
        table.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return COLUMNS
    heads = _cells(lines[at])
    add = [c for c in COLUMNS if c not in [h.lower() for h in heads]]
    if not add:
        return []
    lines[at] = _line(heads + add)
    for i in range(at + 1, len(lines)):
        if not lines[i].startswith("|"):
            break
        cells = _cells(lines[i])
        sep = set("".join(cells)) <= set("-: ")
        cells += [""] * (len(heads) - len(cells))
        lines[i] = _line(cells + (["---"] if sep else [""]) * len(add))
    table.write_text("\n".join(lines), encoding="utf-8")
    return add


def write_feeds(board: Path, apply: bool = True) -> int:
    """Each row's feeds from the topics: `s10` when it is closest work, and every s11-s19 topic that reads it (its
    `related:` papers, matched to the first row whose item starts with theirs, as excalidraw-read matches). Other
    feeds stay (s01, a Section); an s10-s19 entry no topic backs goes. Returns the rows that differ."""
    table = board / "related" / "related.md"
    lines = table.read_text(encoding="utf-8").split("\n") if table.is_file() else []
    at = next((i for i, x in enumerate(lines) if x.startswith("|")), None)
    if at is None:
        return 0
    heads = [h.lower() for h in _cells(lines[at])]
    if "feeds" not in heads:
        return 0
    rows = []
    for i in range(at + 2, len(lines)):
        if not lines[i].startswith("|"):
            break
        cells = _cells(lines[i])
        cells += [""] * (len(heads) - len(cells))
        rows.append((i, cells, dict(zip(heads, cells))))
    want = {i: set() for i, _, _ in rows}
    for nn, topic in related_topics(board).items():
        for p in group_papers(topic) if nn != MAP_NN else []:
            hit = next((i for i, _, r in rows if r.get("item", "").startswith(str(p.get("item", "")))), None)
            if hit is not None:
                want[hit].add(f"s{nn}")
    for i, _, r in rows:
        if any(g.startswith("Closest:") for g in rm.bears(r)):
            want[i].add("s10")
    n = 0
    for i, cells, r in rows:
        feeds = [x.strip() for x in r["feeds"].split(",") if x.strip()]
        keep = [f for f in feeds if not re.fullmatch(r"s1\d", f) or f in want[i]]
        new = keep + sorted(want[i] - set(keep))
        if new != feeds:
            n += 1
            cells[heads.index("feeds")] = ", ".join(new)
            lines[i] = _line(cells)
    if apply and n:
        table.write_text("\n".join(lines), encoding="utf-8")
    return n


def first_sentence(text: str) -> str:
    """A `why here` cell's first sentence: never cut at U.S., e.g. or an initial; no trailing semicolon."""
    text = text.strip()
    for m in re.finditer(r"\.\s+(?=[A-Z0-9])", text):
        before = text[:m.start()]
        if before.endswith(ABBR) or re.search(r"(^|\s)[A-Z]$", before):
            continue
        return text[:m.start() + 1]
    return text.rstrip(" ;")


def ref_of(row: dict, offline: bool = False) -> dict:
    """The paper's reference: title, authors (six, then et al. and the count), venue, year, link. Authors from the
    DOI's record (doi.org, which answers for Crossref and for arXiv's DataCite DOIs); the rest from its related.md row
    when the record is silent. A record's noise is cleaned: &amp;, a "Dr." before a name, a footnote mark after a
    title's last word, doubled spaces."""
    ref = {"title": row.get("item", "").split(" · ", 1)[-1].strip(), "authors": "", "venue": row.get("venue", ""),
           "year": row.get("date", ""), "link": row.get("source", "") or row.get("link", "")}
    where = f"{row.get('source', '')} {row.get('link', '')}"
    doi = re.search(r"10\.\d{4,9}/[^\s|`)]+", where)
    arxiv = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", where)
    doi = doi.group(0).rstrip(".") if doi else (f"10.48550/arXiv.{arxiv.group(1)}" if arxiv else "")
    if doi and not offline:
        try:
            req = urllib.request.Request(f"https://doi.org/{doi}",
                                         headers={"Accept": "application/vnd.citationstyles.csl+json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.load(r)
            names = [" ".join(x for x in (a.get("given"), a.get("family")) if x) or a.get("literal", "")
                     for a in data.get("author") or []]
            ref["authors"] = ", ".join(names[:6]) + (f", et al. ({len(names)} authors)" if len(names) > 6 else "")
            title = data.get("title")
            ref["title"] = (title[0] if isinstance(title, list) and title else title) or ref["title"]
            venue = data.get("container-title")
            ref["venue"] = (venue[0] if isinstance(venue, list) and venue else venue) or ref["venue"]
        except (OSError, ValueError):
            pass
    ref["authors"] = ref["authors"] or "❓ the authors from the DOI record"
    for k in ("title", "authors", "venue"):
        v = re.sub(r"\s+", " ", html.unescape(str(ref[k]))).strip()
        v = re.sub(r"(^|, )Dr\.?\s+", r"\1", v) if k == "authors" else v
        ref[k] = re.sub(r"(?<=[a-z])\d$", "", v) if k == "title" else v
    return ref


def redraw_index(board: Path) -> str:
    """The Board's s00 index is drawn by haipipe-studio's block_index.py from every topic's face: redraw it."""
    s00 = next(iter(sorted((board / "studio").glob("s00-*/build_*.py"))), None)
    return f"s00 index {draw_once(s00)}" if s00 else "⬜ no s00 index on this Board"


# ── scaffolds ──────────────────────────────────────────────────────────────────────────────────────────────
FIND_TOOLS = '''

def _tool(rel: str) -> Path:
    """A Tools skill folder, from the SPACE's Tools/ (or a Tools checkout itself) above this topic."""
    for parent in HERE.parents:
        for base in (parent / "Tools/plugins/haipipe-toolkit/skills", parent / "plugins/haipipe-toolkit/skills"):
            if (base / rel).is_dir():
                return base / rel
    raise SystemExit(f"{rel} not found above {HERE}")
'''

MAP_BUILDER = '''"""s10 · {title}: drawn by haipipe-paper-related's scripts/related_map.py from this face's yaml blocks and the
Board's related/related.md (its Closest rows); a person's marks on the drawing are kept.

    python {script}
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


{find}


sys.path.insert(0, str(_tool("2_theme/paper/haipipe-paper-related/scripts")))
import related_map  # noqa: E402

CHANGES = []          # (YYMMDD, what changed): each gets a green note on ①

if __name__ == "__main__":
    print(related_map.draw(HERE, CHANGES))
'''

GROUP_BUILDER = '''"""s{nn} · {title}: drawn by excalidraw-read's ref/topic_drawing.py from this face's related: yaml and the
readings in reads/; a person's marks on the drawing are kept (haipipe-paper-related).

    python {script}
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


{find}


sys.path.insert(0, str(_tool("1_base/excalidraw/excalidraw-read/ref")))
import topic_drawing  # noqa: E402

if __name__ == "__main__":
    print(topic_drawing.draw(HERE))
'''


def map_face(title: str) -> str:
    name = f"s10 · {title}"
    return "\n".join([
        name, "=" * len(name), "",
        f"**Tags:** `{GROUP}`", "",
        "**Stage:** explore", "",
        "**Topic:** what each closest paper measures, what it leaves open, and where our paper sits among them. The",
        "closest papers are the rows of `related/related.md` whose `bears on` cell starts with \"Closest:\"; the builder",
        "reads them on every build, so a paper added there appears here, red until it is placed. One main frame (①",
        "the map) and small frames that explain it, as stairs; each type of closest work is read paper by paper in",
        "s11 to s19.", "",
        "**Feeds:** s01's novelty check (G0) and the Section that positions the paper (Related Work, or Literature",
        "Review at a venue without one), by proposals in Open.", "",
        "", "Files", "-----", "",
        "```text",
        "s10-related-work-map/",
        "├── s10-related-work-map.md          this face; its yaml blocks are the drawing's words",
        "├── s10-related-work-map.excalidraw  ① the map (main), then ② nearest · ③ what we add · ④ lessons · ⑤ on: each type",
        "├── s10-related-work-map.png         its preview",
        "└── build_s10_related_work_map.py    forwards to haipipe-paper-related scripts/related_map.py",
        "```", "",
        "", "The map (frame ①)", "-----------------", "",
        "Two axes that split the closest work so our gap shows. `at` is the quadrant (`TL` `TR` `BL` `BR`), or `\"off\"`",
        "for a paper not on the map (quoted: YAML reads a bare off as false). A Closest row with no entry here is drawn",
        "red. In the key, `{closest}` and `{placed}` are counted on each build (also `{TL}` `{TR}` `{BL}` `{BR}`).",
        "Frames ② to ⑤ come from `nearest:`, `gaps:`, `lessons:` and `papers:` blocks once there is something to say",
        "(haipipe-paper-related `ref/map-face.md`).", "",
        "```yaml",
        "map:",
        "  title: \"① Where our paper sits among the closest work\"",
        "  sub: \"★ closest in its type\"",
        "  key: \"{closest} closest papers, {placed} placed. ❓ the one sentence: what none of them asks, and we do\"",
        "  left: \"❓ left end of the across axis\"",
        "  right: \"❓ right end\"",
        "  top: \"❓ top end of the up axis\"",
        "  bottom: \"❓ bottom end\"",
        "  ours:",
        "  - title: \"📄 Our paper · ❓ its question\"",
        "    lines: [\"❓ what it runs on\"]",
        "  placements: {}",
        "```", "",
        "", "Decided", "-------", "",
        "(none yet: a decision is one line, s10-D01 · <what was decided> (<who> <date>))", "",
        "", "Open", "----", "",
        "1. ❓ Which papers are closest: the related.md rows whose `bears on` names `Closest: <type>`. (JL)", "",
        "(write here, or mark the drawing in red)", ""])


def item_key(r: dict, every: list[dict]) -> str:
    """The start of a row's item that finds it alone: its short name, or the whole item when another row starts the
    same way (two Chen et al. 2026 papers)."""
    short = rm.item_name(r)
    return short if sum(x.get("item", "").startswith(short) for x in every) <= 1 else r.get("item", "")


def group_face(nn: int, title: str, kind: str, rows: list[dict], offline: bool = False,
               tag: str = "Closest", every: list[dict] | None = None) -> str:
    name = f"s{nn} · {title}"
    papers = []
    for i, r in enumerate(rows, 1):
        says = first_sentence(r.get("why here", "")) or "❓ its point in one line"
        ref = ref_of(r, offline)
        papers += [f"  - id: p{i:02d}", f"    item: {yaml_str(item_key(r, every or rows))}", f"    says: {yaml_str(says)}",
                   "    ref:"] + [f"      {k}: {yaml_str(v)}" for k, v in ref.items()]
    folder = f"s{nn}-<slug>"
    return "\n".join([
        name, "=" * len(name), "",
        f"**Tags:** `{GROUP}`", "",
        "**Stage:** explore", "",
        f"**Topic:** {'the closest work' if tag == 'Closest' else 'background'} of one type, `{tag}: {kind}` in "
        "`related/related.md`. Each paper is read from its",
        "PDF with excalidraw-read: its pages with the key passages highlighted, a note on each, its logic, and how it",
        "links to our paper. The papers are rows of `related/related.md`; a kept PDF is in `related/paper/`.", "",
        "**Feeds:** s10 (the map of the closest work) and s01's novelty check (G0).", "",
        "", "Files", "-----", "",
        "```text",
        f"{folder}/",
        f"├── {folder}.md          this face; its related: yaml is the drawing's words",
        f"├── {folder}.excalidraw  the type, then one row per paper: its pages read, its logic",
        f"├── {folder}.png         its preview",
        f"├── build_s{nn}_<slug>.py    forwards to excalidraw-read ref/topic_drawing.py",
        "├── reads/pNN-<paper>/reading.yaml          one reading per paper (excalidraw-read)",
        "└── assets/                                 the highlighted pages the drawing shows",
        "```", "",
        "", "The drawing's words", "-------------------", "",
        "`papers` is the reading order; `item` is the start of the paper's row in `related/related.md`; `says` is its key",
        "point in one line; `ref` is its reference (title, authors, venue, year, link), the authors from the DOI's",
        "record. A paper with no `reads/<id>-*/reading.yaml` is drawn red until it is read.", "",
        "```yaml",
        "related:",
        "  key: ❓ the type's point, one sentence",
        "  what: ❓ what these papers share",
        "  why: ❓ why it matters to our paper",
        "  papers:" + ("" if papers else " []"),
        *papers,
        "  open: []",
        "```", "",
        "", "Decided", "-------", "",
        f"(none yet: a decision is one line, s{nn}-D01 · <what was decided> (<who> <date>))", "",
        "", "Open", "----", "",
        "1. ❓ Read each paper from its PDF (excalidraw-read), most important first.", "",
        "(write here, or mark the drawing in red)", ""])


def yaml_str(s: str) -> str:
    s = str(s)
    return "'" + s.replace("'", "''") + "'" if re.search(r"[:#\[\]{}&*!|>'\"%@`,]|^\s|\s$|^-", s) else s


def builder_text(template: str, nn: int, title: str, script: str) -> str:
    return template.format(nn=f"{nn:02d}", title=title, script=script, find=FIND_TOOLS.strip("\n"))


def draw_once(builder: Path) -> str:
    builder = Path(builder).resolve()
    r = subprocess.run([sys.executable, str(builder)], capture_output=True, text=True, cwd=builder.parent)
    return "✅ drawn" if r.returncode == 0 else f"❌ builder failed: {(r.stderr or r.stdout).strip().splitlines()[-1:]}"


def make_map(board: Path, title: str = "Related work: where our paper sits among the closest work") -> Path:
    have = topics(board)
    if MAP_NN in have:
        raise SystemExit(f"s10 is taken: {have[MAP_NN].name} (an older Board: `band` moves its topics first)")
    folder = board / "studio" / "s10-related-work-map"
    folder.mkdir(parents=True)
    face(folder).write_text(map_face(title), encoding="utf-8")
    script = folder / "build_s10_related_work_map.py"
    script.write_text(builder_text(MAP_BUILDER, MAP_NN, title, script.name), encoding="utf-8")
    add_group(board)
    added = ensure_columns(board)
    if added:
        print(f"related/related.md: added the paper columns {', '.join(added)}")
    print(f"{folder.relative_to(board)}  {draw_once(script)}")
    print(redraw_index(board))
    return folder


def make_group(board: Path, kind: str, slug: str, title: str = "", offline: bool = False,
               background: bool = False) -> Path:
    if not SLUG.match(slug):
        raise SystemExit(f"slug {slug!r}: lower-case letters, digits and - only")
    if "," in kind:
        raise SystemExit(f"type {kind!r}: no comma (a `bears on` cell is split on commas)")
    ensure_columns(board)
    have = topics(board)
    nn = next((n for n in BAND if n not in have), None)
    if nn is None:
        raise SystemExit("s11-s19 are full: merge two types, or split the paper")
    tag = "Shared background" if background else "Closest"
    rows = [r for r in rm.related_rows(board) if f"{tag}: {kind}" in rm.bears(r)]
    title = title or kind[:1].upper() + kind[1:]
    folder = board / "studio" / f"s{nn}-related-work-{slug}"
    folder.mkdir(parents=True)
    face(folder).write_text(group_face(nn, title, kind, rows, offline, tag, rm.related_rows(board)).replace(f"s{nn}-<slug>", folder.name)
                            .replace(f"build_s{nn}_<slug>.py", f"build_s{nn}_related_work_{slug.replace('-', '_')}.py"),
                            encoding="utf-8")
    script = folder / f"build_s{nn}_related_work_{slug.replace('-', '_')}.py"
    script.write_text(builder_text(GROUP_BUILDER, nn, title, script.name), encoding="utf-8")
    add_group(board)
    reader = rm.SKILLS / "1_base/excalidraw/excalidraw-read/ref/topic_drawing.py"
    state = (f"⬜ no `{tag}: {kind}` row yet: add rows, then draw" if not rows else
             "⬜ excalidraw-read is not installed: the face stands alone" if not reader.is_file() else draw_once(script))
    fed = write_feeds(board)
    print(f"{folder.relative_to(board)}  {len(rows)} paper{'' if len(rows) == 1 else 's'}  {state}")
    print(f"related/related.md: feeds written on {fed} row{'' if fed == 1 else 's'} · {redraw_index(board)}")
    return folder


# ── check ──────────────────────────────────────────────────────────────────────────────────────────────────
def group_papers(topic: Path) -> list[dict]:
    m = re.search(r"```yaml\s*\n(related:.*?)```", face(topic).read_text(encoding="utf-8"), re.S) \
        if face(topic).is_file() else None
    import yaml
    return list((((yaml.safe_load(m.group(1)) or {}).get("related") or {}).get("papers") or [])) if m else []


def check(board: Path) -> int:
    """Every Closest row placed on s10 and read in one s1N topic; every topic in the band. Exit 1 on a ❌."""
    bad, notes = [], []
    rel = related_topics(board)
    closest = rm.closest_rows(board)
    rows = rm.related_rows(board)
    if not rel and not closest:
        print("⬜ no related work yet: mark the closest rows in related/related.md, then `map` and `group`")
        return 0
    for nn, t in rel.items():
        if nn != MAP_NN and nn not in BAND:
            bad.append(f"{t.name}: outside s10-s19 (`band` moves it)")
    m = rel.get(MAP_NN)
    if not m or not is_map(m):
        bad.append("s10 is not the related-work map (`map` makes it; `band` moves an older one)")
    placed = (rm.face_yaml(face(m), "map").get("placements") or {}) if m else {}
    read_in: dict[str, list[str]] = {r["item"]: [] for r in closest}      # by the whole item: two Chen et al. 2026
    for nn, t in rel.items():
        if nn == MAP_NN:
            continue
        stars = 0
        for p in group_papers(t):
            item = str(p.get("item", ""))
            hits = [r for r in rows if r.get("item", "").startswith(item)]
            row = hits[0] if hits else None
            if len(hits) > 1:
                bad.append(f"{t.name} {p.get('id')}: '{item}' starts {len(hits)} rows; give its whole item")
            if not row:
                bad.append(f"{t.name} {p.get('id')}: '{item}' is no row of related/related.md")
                continue
            stars += "★" in row.get("key", "")
            if row.get("item", "") in read_in:
                read_in[row["item"]].append(t.name[:3])
            if not sorted((t / "reads").glob(f"{p.get('id')}-*/reading.yaml")):
                notes.append(f"⬜ {t.name[:3]} {p.get('id')} {item}: not read from its PDF yet")
        if not stars:
            notes.append(f"⚠️ {t.name}: no ★ (the closest of its type) among its papers")
    for r in closest:
        if r["name"] not in placed:
            bad.append(f"{r['name']}: Closest ({r['type']}) but not placed on the s10 map")
        if not read_in[r["item"]]:
            bad.append(f"{r['name']}: Closest ({r['type']}) but in no s11-s19 topic")
        elif len(read_in[r["item"]]) > 1:
            notes.append(f"⚠️ {r['name']}: in {', '.join(read_in[r['item']])}; one type is clearer")
    stale = write_feeds(board, apply=False)
    if stale:
        notes.append(f"⚠️ {stale} rows' feeds miss or misname their s10-s19 topics (`feeds` writes them)")
    types = sorted({r["type"] for r in closest})
    print(f"{board.name}: {len(closest)} closest papers in {len(types)} types · s10 map "
          f"{'✅' if m and is_map(m) else '❌'} · {len(rel) - (1 if m else 0)} type topics")
    for line in [f"❌ {b}" for b in bad] + notes:
        print("  " + line)
    print("✅ related work in order" if not bad else f"❌ {len(bad)} to fix")
    return 1 if bad else 0


# ── band: an older Board's topics into s10-s19 ────────────────────────────────────────────────────────────
def plan(board: Path) -> list[tuple[int, Path, int, str]]:
    rel = related_topics(board)
    maps = [nn for nn, t in rel.items() if is_map(t)]
    order = maps[:1] + [nn for nn in rel if nn not in maps[:1]]
    if len(order) > 10:
        raise SystemExit(f"{len(order)} related-work topics; s10-s19 holds 10: merge some types first")
    if not maps:
        order = [None] + order                                  # no map yet: s10 stays free for `map`
    out = []
    for new, old in zip(range(MAP_NN, 20), order):
        if old is None:
            continue
        t = rel[old]
        out.append((old, t, new, f"s{new:02d}-{NAME.match(t.name).group(2)}"))
    moving = {t.name for _, t, _, _ in out}
    for old, t, new, name in out:
        other = topics(board).get(new)
        if other is not None and other.name not in moving:
            raise SystemExit(f"s{new:02d} is taken by {other.name}, not a related-work topic: move it first")
    return [x for x in out if x[0] != x[2]]


def sweep(text: str, nums: dict[int, int]) -> str:
    """Every mention of a moved number, in one pass: sNN, sNN-<topic>, sNN-Dxx, build_sNN_, run-draw-sNN."""
    alt = "|".join(f"{n:02d}" for n in nums)

    def to(m: re.Match) -> str:
        return f"{m.group(1)}s{nums[int(m.group(2))]:02d}"

    def words(part: str) -> str:
        part = re.sub(rf"(build_|run-draw-)s({alt})(?![0-9])", to, part)
        # a range's second end follows a hyphen: s06-s10
        return re.sub(rf"(^|[^A-Za-z0-9_\-]|(?<=s\d\d)-)s({alt})(?![0-9])", to, part, flags=re.M)
    parts = re.split(r"(https?://\S+)", text)                       # a web address is never a topic number
    return "".join(p if i % 2 else words(p) for i, p in enumerate(parts))


def board_files(board: Path):
    for p in sorted(board.rglob("*")):
        rel = p.relative_to(board).parts
        if not p.is_file() or any(x.startswith(".") or x == "_old" for x in rel[:-1]) or p.suffix.lower() in GENERATED:
            continue
        if p.name.endswith(".seed.json"):
            continue
        try:
            yield p, p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def renamed_from(md: Path, old: str) -> None:
    lines = md.read_text(encoding="utf-8").split("\n")
    at = next((i for i, x in enumerate(lines[:60]) if x.startswith("renamed-from:")), None)
    if at is not None:
        was = lines[at].split(":", 1)[1].strip().strip("[]")
        names = [x.strip() for x in was.split(",") if x.strip()] + [old]
        lines[at] = f"renamed-from: [{', '.join(dict.fromkeys(names))}]"
    else:
        under = 2 if len(lines) > 1 and set(lines[1].strip()) == {"="} else 0
        lines[under:under] = [f"renamed-from: {old}", ""] if under else [f"renamed-from: {old}"]
    md.write_text("\n".join(lines), encoding="utf-8")


def band(board: Path, apply: bool = False) -> int:
    moves = plan(board)
    if not moves:
        print("✅ every related-work topic is already in s10-s19")
        return 0
    nums = {old: new for old, _, new, _ in moves}
    for old, t, new, name in moves:
        print(f"{t.name}  →  {name}")
    runs = [(board / "runs" / f"run-draw-s{o:02d}", board / "runs" / f"run-draw-s{n:02d}") for o, n in nums.items()
            if (board / "runs" / f"run-draw-s{o:02d}").is_dir()]
    for a, b in runs:
        print(f"runs/{a.name}  →  runs/{b.name}")
    hits = [(p, text, sweep(text, nums)) for p, text in board_files(board)]
    hits = [(p, a, b) for p, a, b in hits if a != b]
    for p, a, b in hits:
        print(f"  ✏️ {p.relative_to(board)}")
    if not apply:
        print(f"dry run: {len(moves)} topics, {len(runs)} soft Runs, {len(hits)} files to sweep; --apply does it")
        return 0
    for p, _, b in hits:                                            # the words first, while paths are as read
        p.write_text(b, encoding="utf-8")
    temp = []
    for old, t, new, name in moves:                                 # through temporary names: s10 may move to s15
        tmp = t.with_name(f".moving-{t.name}")
        t.rename(tmp)
        temp.append((tmp, t.name, t.parent / name))
    for a, b in runs:
        a.rename(a.with_name(f".moving-{a.name}"))
    for tmp, old_name, dest in temp:
        tmp.rename(dest)
        new_prefix = dest.name.split("-", 1)[0]
        old_prefix = old_name.split("-", 1)[0]
        for f in sorted(dest.iterdir()):
            n = f.name
            if n.startswith(old_name) or n.startswith(f".{old_name}"):
                f.rename(f.with_name(n.replace(old_name, dest.name, 1)))
            elif n.startswith(f"build_{old_prefix}_"):
                f.rename(f.with_name(n.replace(f"build_{old_prefix}_", f"build_{new_prefix}_", 1)))
        renamed_from(face(dest), old_name)
    for a, b in runs:
        moving = a.with_name(f".moving-{a.name}")
        moving.rename(b)
        for f in b.iterdir():
            if f.name.startswith(a.name):
                f.rename(f.with_name(f.name.replace(a.name, b.name, 1)))
    for _, _, dest in temp:
        builder = next(iter(sorted(dest.glob("build_*.py"))), None)
        print(f"{dest.name}  {draw_once(builder) if builder else '⬜ no builder'}")
    print(redraw_index(board))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("map")
    p.add_argument("board", type=Path)
    p.add_argument("--title", default="Related work: where our paper sits among the closest work")
    p = sub.add_parser("group")
    p.add_argument("board", type=Path)
    p.add_argument("--type", required=True, dest="kind")
    p.add_argument("--slug", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--offline", action="store_true", help="no DOI lookup: authors stay ❓ to fill")
    p.add_argument("--background", action="store_true", help="a type of `Shared background: <type>` rows")
    sub.add_parser("check").add_argument("board", type=Path)
    sub.add_parser("feeds").add_argument("board", type=Path)
    p = sub.add_parser("band")
    p.add_argument("board", type=Path)
    p.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    board = a.board.resolve()
    if not (board / "board.md").is_file():
        raise SystemExit(f"{board}: no board.md; give the paper Board folder (paper/Paper-<Slug>/)")
    if a.cmd == "map":
        make_map(board, a.title)
        return 0
    if a.cmd == "group":
        make_group(board, a.kind, a.slug, a.title, a.offline, a.background)
        return 0
    if a.cmd == "feeds":
        print(f"related/related.md: feeds written on {write_feeds(board)} rows")
        return 0
    if a.cmd == "check":
        return check(board)
    return band(board, a.apply)


if __name__ == "__main__":
    sys.exit(main())
