"""Delivery: one card per result, its versions and lanes, live pages and groups."""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path
from urllib.parse import urlencode
from src.common import delivery_dir, delivery_owner

from live.frame_base import ROUTE, VANILLA, _PREFIXED, _e, _file_url, _rel, children, face, pop
from live.frame_studio import _group_parts, _split_tags
from live.frame_groups import group_list


# ── Delivery: one card per result under the group bar (b10 s03-D08; JL 261012: "for the delivery, we should
# also have the group tags as well, and have the delivery card, similar to the studio") ──────────────────────
# A result is a file a reader opens; its twins (a .docx and the .pdf beside it) are one card. Build files, logs
# and the pieces a build puts together are not results (the same rule the s03 drawing counts by).
DELIVERY_OPENS = {".pdf": "PDF", ".docx": "Word", ".pptx": "Deck", ".html": "Web page", ".xlsx": "Sheet",
                  ".png": "Image"}
DELIVERY_PIECES = {"history", "__pycache__", "svg", "displays", "sections", "appendices", "draft-bibliography",
                   "figures", "draft-sections"}
LIVE_PAGE = "Live page"                      # a deliverable with a `url:`: a page a host serves, no file in delivery/
RESULT_GROUPS = "result_groups.md"          # delivery/result_groups.md: | result | group |, the groups a person added


def _result_groups(deliv: Path) -> dict:
    """{result key: [groups]} from delivery/result_groups.md."""
    f = deliv / RESULT_GROUPS
    out = {}
    if not f.is_file():
        return out
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if len(cells) >= 2 and cells[0] not in ("result", "") and not set(cells[0]) <= set("-: "):
            out[cells[0].strip("`")] = _split_tags(cells[1])
    return out


def _delivery_set_groups(deliv: Path, key: str, groups: list) -> None:
    """Write one result's added groups into delivery/result_groups.md (a row per result a person grouped;
    no groups, no row)."""
    rows = _result_groups(deliv)
    rows[key] = groups
    lines = ["Result groups · written by the workbench", "========================================", "",
             "The groups a person gave each result in Delivery (drag a card onto a group). A result's file kind",
             "(PDF, Word, Deck, ...) is its fixed group and is not written here; delivery/_groups.txt keeps the",
             "buttons' order.", "", "| result | group |", "|---|---|"]
    kept = [f"| `{k}` | {', '.join(v)} |" for k, v in sorted(rows.items()) if v]
    if not kept:                                  # the last group taken out: no file left behind
        (deliv / RESULT_GROUPS).unlink(missing_ok=True)
        return
    deliv.mkdir(exist_ok=True)
    (deliv / RESULT_GROUPS).write_text("\n".join(lines + kept) + "\n", encoding="utf-8")


# A deliverable is one item (JL 261014: "for the delivery, I think we just make the item to be the same ... all of
# them should one Delivery Item, and within it, we can see different versions"): its lanes (a Section's web/,
# word/ and latex/ builds; a deck's slide/ and its picture in render/) and its versions (`-v1` ... `-v12`) fold into
# it. A version is one stem, its twins and its lanes; which stems are versions of one item is `version_roots`.
DELIVERY_LANES = {"latex", "word", "slide", "slides", "render", "web"}
_VERSION = re.compile(r"^(?P<base>.+?)[-_ .]v(?P<n>\d+)$", re.I)


def _version_of(stem: str) -> tuple:
    """(base, number) of a stem: `Deck-Visual-v12` -> ("Deck-Visual", 12), `Deck` -> ("Deck", None)."""
    m = _VERSION.match(stem)
    return (m.group("base"), int(m.group("n"))) if m else (stem, None)


def version_roots(stems) -> dict:
    """{stem: the item it is a version of}, for the names in one folder; the one version rule Delivery and Related
    share (b10 s03-D10; JL 261014: "一个东西，我们会有一个 version 又一个 version ... item 谁谁谁，然后里面可能有 version 1、
    version 2、version 3"). Stems that differ only by `-v<N>` are one item; a numbered stem whose name starts with
    another's joins it (`…-Evaluation-Visual-v12` → `…-Evaluation`); then an unnumbered variant of an item that has
    numbers joins too (`…-Workflow-Symmetric` → `…-Workflow`). Names with no number and no numbered kin stay apart
    (`FairGlucose-npjDM-SI` is not a version of `FairGlucose-npjDM`)."""
    families = {}
    for stem in dict.fromkeys(stems):
        base, n = _version_of(stem)
        families.setdefault(base, []).append((stem, n))
    root_of = {b: b for b in families}
    numbered = lambda members: any(n is not None for _, n in members)
    for base, members in families.items():
        heads = [b for b in families if b != base and base.startswith(b + "-")]
        if numbered(members) and heads:
            root_of[base] = max(heads, key=len)

    def final(b):
        while root_of[b] != b:
            b = root_of[b]
        return b
    with_numbers = {final(b) for b, members in families.items() if numbered(members)}
    for base in families:
        if root_of[base] == base and base not in with_numbers:
            heads = [b for b in families if b != base and base.startswith(b + "-") and final(b) in with_numbers]
            if heads:
                root_of[base] = max(heads, key=len)
    return {stem: final(base) for base, members in families.items() for stem, _ in members}


def version_label(stem: str, root: str, many: bool) -> str:
    """What a version's button says: the part of its name after the item's (`Visual-v12`, `v5`)."""
    tail = stem[len(root):].lstrip("-_ .") if stem.startswith(root) else stem
    return tail or ("first" if many else "")


def version_panes(versions: list, pane) -> str:
    """A row of version buttons, newest first and picked, over one pane per version (`pane(version)` fills it);
    a single version is its pane alone. Each version is a dict with at least `label` and `when`."""
    row = ""
    if len(versions) > 1:
        row = ('<nav class="row dv-vers" aria-label="Versions">' + "".join(
            f'<button type=button class=tab data-dv="{n}" aria-pressed="{"true" if n == 0 else "false"}">'
            f'{_e(v["label"])} <span class=tag-count>{datetime.date.fromtimestamp(v["when"]).strftime("%m-%d")}</span>'
            f'</button>' for n, v in enumerate(versions)) + "</nav>")
    return row + "".join(f'<div class=dv-pane data-dv="{n}"{"" if n == 0 else " hidden"}>{pane(v)}</div>'
                         for n, v in enumerate(versions))


def _live_pages(block: Path) -> list:
    """The Block's live pages, as delivery items: each deliverable of a Job's face (or the Block's) with a `url:`, the
    one line that says where the page is, so nothing is copied into delivery/. It has no file and no versions: it answers
    today, and the host serving it is what keeps it. It sits under its `task:` when the face names a Task it has;
    `service:` is its short name, its tab in Findings' Service section."""
    import yaml
    added, out = _result_groups(block / "delivery"), []
    for owner in [block] + children(block, "Block"):
        md = face(owner)
        m = re.search(r"(?ms)^## Deliverables\s*$.*?```ya?ml\s*\n(.*?)```", md.read_text(encoding="utf-8")) if md else None
        try:
            rows = (yaml.safe_load(m.group(1)) or {}).get("deliverables") if m else []
        except yaml.YAMLError:
            rows = []
        for row in rows or []:
            if not (isinstance(row, dict) and row.get("what") and row.get("url")):
                continue
            task = owner / str(row.get("task") or "")
            folder = task if row.get("task") and task.is_dir() else owner
            where = folder.relative_to(block).as_posix() if folder != block else ""
            key = "/".join(x for x in (where, re.sub(r"\W+", "-", str(row["what"])).strip("-").lower()) if x)
            src = [p for p in Path(where).parts if _PREFIXED.match(p)]
            out.append({"key": key, "title": str(row["what"]), "files": [], "fixed": [LIVE_PAGE],
                        "groups": [LIVE_PAGE] + [g for g in added.get(key, []) if g != LIVE_PAGE],
                        "source": " › ".join(src) or "the Block", "folder": folder, "when": 0, "size": 0,
                        "versions": [], "url": str(row["url"]), "service": str(row.get("service") or row["what"]),
                        "face": owner})                  # a relative url is from the face's own folder (live_url)
    return out


def delivery_items(block: Path, part: Path | None = None) -> list:
    """The deliverables under the Block's delivery/ (or under one part of it), newest first: {key, title, files
    (every file of every version), fixed (their kinds), groups, source (jNN_<job> › tNN_<task>, or the Block),
    folder (the source folder), when, size (the newest version's), versions}. Each version is {label, number,
    files, when, size}, newest first. Live pages (`_live_pages`) come first, with `url` and no files."""
    deliv = block / "delivery"
    top = part if part is not None else deliv
    source = block.joinpath(*top.relative_to(deliv).parts)   # the path is the link: this part's own Job or Task
    live = [i for i in _live_pages(block) if part is None or i["folder"] == source or source in i["folder"].parents]
    if not top.is_dir():
        return live
    builds = {}                                   # (where, stem) -> files: one version of one deliverable
    for f in sorted(top.rglob("*")):
        rel = f.relative_to(deliv)
        if (not f.is_file() or f.name.startswith((".", "_")) or f.suffix.lower() not in DELIVERY_OPENS
                or set(rel.parts[:-1]) & DELIVERY_PIECES or any(x.startswith((".", "_")) for x in rel.parts[:-1])
                or f.stem == "master" or f.stem.endswith("-view")):
            continue
        where = f.parent.parent if f.parent.name.lower() in DELIVERY_LANES and f.parent != deliv else f.parent
        stem = f.stem.removesuffix("-tracked")
        if stem == "index" and where != deliv:    # a web lane's page is named by its part (t04_methods/web/index)
            stem = where.name
        builds.setdefault((where, stem), []).append(f)
    by_where = {}
    for where, stem in builds:
        by_where.setdefault(where, []).append(stem)
    grouped = {}                                  # (where, item) -> [(stem, number)]
    for where, stems in by_where.items():
        roots = version_roots(stems)
        for stem in stems:
            grouped.setdefault((where, roots[stem]), []).append((stem, _version_of(stem)[1]))
    added, order = _result_groups(deliv), list(DELIVERY_OPENS.values())
    out = []
    for (where, base), members in grouped.items():
        versions = []
        for stem, n in members:
            files = sorted(builds[(where, stem)], key=lambda f: (
                -1 if f.suffix.lower() == ".docx" else order.index(DELIVERY_OPENS[f.suffix.lower()]), f.parent.name, f.name))
            versions.append({"label": version_label(stem, base, len(members) > 1), "number": n, "files": files,
                             "when": max(f.stat().st_mtime for f in files), "size": sum(f.stat().st_size for f in files)})
        versions.sort(key=lambda v: -v["when"])
        files = [f for v in versions for f in v["files"]]
        key = (where / base).relative_to(deliv).as_posix()
        kinds = [k for k in order if any(DELIVERY_OPENS[f.suffix.lower()] == k for f in files)]
        olds = [(f.parent / f.stem.removesuffix("-tracked")).relative_to(deliv).as_posix() for f in files]
        mine = [g for k in [key] + olds for g in added.get(k, [])]
        src = [p for p in where.relative_to(deliv).parts[:2] if _PREFIXED.match(p)]
        source = block.joinpath(*src) if src else block
        out.append({"key": key, "title": base, "files": files, "fixed": kinds,
                    "groups": kinds + [g for g in dict.fromkeys(mine) if g not in kinds],
                    "source": " › ".join(src) or "the Block", "folder": source,
                    "when": versions[0]["when"], "size": versions[0]["size"], "versions": versions})
    return live + sorted(out, key=lambda i: -i["when"])


def _size(n: int) -> str:
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} KB"


def _delivery_preview(files: list, root: Path) -> str:
    """One version, shown: a PDF or web page in a frame, a picture, a deck drawn slide by slide, a Word file read
    from its package; else how to open it."""
    url = lambda f: "/" + _rel(f, root)
    frame_of = lambda src, name: (f'<iframe class=st-frame title="{_e(name)}" data-src="{_e(src)}" '
                                  f'referrerpolicy=no-referrer></iframe>')
    for ext in (".pdf", ".html", ".png", ".pptx", ".docx"):
        f = next((f for f in files if f.suffix.lower() == ext), None)
        if f is None:
            continue
        if ext == ".png":
            return f'<img class=related-img loading=lazy alt="{_e(f.name)}" src="{_e(url(f))}">'
        if ext in (".pptx", ".docx"):           # read from the package (JL 261014: "the preview of the slide as well")
            return frame_of(ROUTE + "?" + urlencode({"view": ext[1:], "path": _rel(f, root)}), f.name)
        return frame_of(url(f), f.name)
    kind = DELIVERY_OPENS[files[0].suffix.lower()] if files else "this"
    return f'<p class="mut none">No preview of a {_e(kind)} file here: open it from the links above.</p>'


def _delivery_links(files: list, root: Path) -> str:
    """Each file of one version, as a pop-out link named by its kind (and its lane when two share a kind)."""
    kinds = [DELIVERY_OPENS[f.suffix.lower()] for f in files]
    return " ".join(pop("/" + _rel(f, root), f.name,
                        k + (f" · {f.parent.name}" if kinds.count(k) > 1 else "") + " ↗")
                    for f, k in zip(files, kinds))


def live_url(item: dict, root: Path) -> str:
    """A live page's address: an http(s) link or a path from the served root as written; a path with no leading `/` is
    from its face's own folder (`delivery/web/index.html`), so it opens on any server, a SPACE's or Tools' own (261106:
    one written from the SPACE root 404'd on a server rooted at Tools)."""
    url = str(item.get("url") or "")
    if not url or url.startswith(("http://", "https://", "/")):
        return url
    page = (Path(item.get("face") or item["folder"]) / url).resolve()
    return _file_url(page, root) if page.is_file() and page.is_relative_to(Path(root).resolve()) else url


def _delivery_card(i: dict, root: Path) -> str:
    """One closed row per deliverable, as a Studio topic's: ⋮⋮, its name and groups and its newest version's files ↗,
    with no line under the name and no Add to Current (JL 261014: "too hard to read, why you give so many unnecessary
    information", then "remove the add to current, this is not good to see": where it came from, when it was built,
    its size and its sends are gone, delivery.md keeps the sends; a card still drops on Current by its ⋮⋮); opened,
    a row of its versions (newest first, picked) over the picked version itself."""
    attrs, handle, _, chips = _group_parts(i["key"], i["title"], i["groups"], noun="result", fixed=i["fixed"])
    if i.get("url"):                               # a live page: the page itself, working, in its card (JL 261104)
        url = live_url(i, root)
        frame = (f'<iframe class=st-frame title="{_e(i["title"])}" data-src="{_e(url)}" referrerpolicy=no-referrer>'
                 f'</iframe>' if url.startswith("/") else f'<p class="mut none">It lives on another host: open it above.</p>')
        return (f'<details class=topic data-studio-tags="{_e(json.dumps(i["groups"]))}"{attrs}><summary>{handle}'
                f'<span class=related-head><b>{_e(i["title"])}</b>{chips}</span>'
                f'<span class=topic-pop><a href="{_e(url)}" target=_blank rel=noopener>own tab ↗</a></span></summary>'
                f'{frame}</details>')
    versions = i.get("versions") or [{"label": "", "number": None, "files": i["files"], "when": i["when"],
                                      "size": i["size"]}]
    newest = versions[0]
    many = len(versions) > 1
    body = version_panes(versions, lambda v: (f'<p class="mut dv-files">{_e(v["label"])}: '
                                              f'{_delivery_links(v["files"], root)}</p>' if many else "")
                         + _delivery_preview(v["files"], root))
    return (f'<details class=topic data-studio-tags="{_e(json.dumps(i["groups"]))}"{attrs}><summary>{handle}'
            f'<span class=related-head><b>{_e(i["title"])}</b>{chips}</span>'
            f'<span class=topic-pop>{_delivery_links(newest["files"], root)}</span></summary>'
            f'{body}</details>')


def delivery_view(folder: Path, root: Path, theme=None) -> str:
    """Delivery's cards: every result of the Block (from the Block), or of the picked Job's or Task's part,
    under the Block's group bar; the file kinds are fixed groups, + Group adds a person's own."""
    block = delivery_owner(folder)
    items = delivery_items(block, None if folder.resolve() == block.resolve() else delivery_dir(folder))
    if not items:
        return ""
    theme = theme or VANILLA
    extra = ()
    if theme.delivery_fixed:                       # the theme's own groups (no ×) and reading order
        placed = [(i, theme.delivery_fixed(i)) for i in items]
        for i, (groups, _) in placed:
            i["fixed"] = list(groups) + i["fixed"]
            i["groups"] = list(groups) + [g for g in i["groups"] if g not in groups]
        extra = tuple(dict.fromkeys(g for _, (groups, _) in placed for g in groups))
        items = [i for i, _ in sorted(placed, key=lambda p: (p[1][1], -p[0]["when"]))]
    rows = "".join(_delivery_card(i, root) for i in items)
    kinds = extra + tuple(k for k in (LIVE_PAGE, *DELIVERY_OPENS.values()) if any(k in i["fixed"] for i in items))
    return group_list(block, root, "delivery", [i["groups"] for i in items], rows, fixed=kinds)
