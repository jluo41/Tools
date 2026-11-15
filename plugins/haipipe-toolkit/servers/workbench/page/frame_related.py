"""Related: the Block's related/ table and items, their previews (docx, eml), the Related view, and the Studio's Delivery part."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

from live.frame_base import (Space, VANILLA, _e, _empty_view, _file_url, _link, _reader, _rel, href, pop,
                             run_type)
from live.frame_studio import _group_parts, _split_tags
from live.frame_groups import group_list
from live.frame_delivery import (DELIVERY_OPENS, LIVE_PAGE, delivery_items, delivery_view, version_label,
                                 version_panes, version_roots)


# ── Related: what the Block sits beside (b10 s04-related-workbench-skill, s01-D34) ──────────────────
# One related/ per Block, read by its Jobs and Tasks: meetings/, papers/, files/, emails/ and one table,
# related/related.md (kind · date · item · link · feeds · group); each subfolder is a group of its files
# (s04-D08), and /haipipe-related owns the rule (s04-D09). It folds inside the Studio, the second part
# under the topic cards (JL 261011), since what came in is what the topics think with.


def related_rows(block: Path) -> tuple:
    """(heads, rows) of the Block's related/related.md table: heads lower-cased, each row a dict."""
    table = block / "related" / "related.md"
    heads, rows = [], []
    if not table.is_file():
        return heads, rows
    for line in table.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not heads:
            heads = [c.lower() for c in cells]
            continue
        rows.append(dict(zip(heads, cells + [""] * (len(heads) - len(cells)))))
    return heads, rows


def _related_target(cell: str) -> str:
    return cell.strip().strip("`").strip()


def _related_link(cell: str, block: Path, root: Path) -> str:
    """A related row's link: a web address links out; a file under related/ opens in the pop-out, a .md in
    the reader and a .docx as its preview; anything else stays as written."""
    target = _related_target(cell)
    if not target:
        return ""
    if re.match(r"https?://", target):
        return f'<a href="{_e(target)}" target=_blank rel=noopener>{_e(target.split("//", 1)[1][:48])} ↗</a>'
    path = block / "related" / target
    if path.is_file():
        return pop(_file_url(path, root), path.name, target)
    return _e(target)


PREVIEW_FRAME = {".md", ".docx", ".eml", ".pptx", ".pdf", ".html", ".htm", ".txt", ".csv"}
PREVIEW_IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def _related_preview(target: str, block: Path, root: Path) -> str:
    """An opened related row: the file itself, read in place (JL 261011: "could we preview the word here?"):
    Word through its package (`docx_preview`), a PDF, a page or a picture; else what it is and a link."""
    if re.match(r"https?://", target):
        return f'<p class="mut none">A web link: {_related_link(target, block, root)}</p>'
    path = block / "related" / target if target else None
    if path is None or not path.is_file():
        return (f'<p class="mut none">Not on this computer: <code>related/{_e(target)}</code> (an office '
                'file stays on the machine that saved it).</p>' if target else '<p class="mut none">No file.</p>')
    url, ext = _file_url(path, root), path.suffix.lower()
    if ext in PREVIEW_IMAGE:
        return f'<img class=related-img loading=lazy src="{_e(url)}" alt="{_e(path.name)}">'
    if ext in PREVIEW_FRAME:
        return (f'<iframe class=st-frame title="{_e(path.name)}" data-src="{_e(url)}" '
                'referrerpolicy=no-referrer></iframe>')
    return f'<p class="mut none">No preview for {_e(ext or "this file")}: {pop(url, path.name, path.name + " ↗")}</p>'


_DOCX_CACHE: dict = {}


def docx_preview(path: Path, root: Path) -> str:
    """A .docx as a page: the Word renderer's projection of its package (text, tables, images, comments in
    the margin; workbench/workbench-task-draft/exporters/docx2pdf.py `docx_html`), read only, cached by the file's stamp."""
    import importlib.util
    stamp = (str(path), path.stat().st_mtime_ns, path.stat().st_size)
    if stamp not in _DOCX_CACHE:
        spec = importlib.util.spec_from_file_location(
            "docx2pdf", Path(__file__).resolve().parents[1] / "workbench-task-draft" / "exporters" / "docx2pdf.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        page, counts = module.docx_html(path)
        line = (f'<p style="font:13px -apple-system,sans-serif;color:#555;margin:0 0 14px">{_e(path.name)} · read '
                f'from the Word package: {counts["paragraphs"]} paragraphs · {counts["tables"]} tables · '
                f'{counts["images"]} images · {counts["comments"]} comments · '
                f'<a href="/{_e(quote(_rel(path, root)))}">the .docx ↓</a></p>')
        screen = ("<style>@media screen{body{line-height:1.5;padding:20px 28px;max-width:8.5in;margin:0 auto;"
                  "background:#fff;color:#111}}</style>")
        _DOCX_CACHE.clear()                   # one file kept: the one being read
        _DOCX_CACHE[stamp] = page.replace("<div class='page'>", screen + line + "<div class='page'>", 1)
    return _DOCX_CACHE[stamp]


def _related_folder(target: str) -> str:
    """The subfolder of related/ a kept file sits in, read off its link (`meetings/…` → meetings): the
    item's own group, as a topic's **Type:** line is (b10 s04-D08); '' for a web link or a file at the top."""
    if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or "/" not in target:
        return ""
    head = target.split("/", 1)[0]
    return "" if head.startswith((".", "_")) or head == ".." else head


def eml_preview(path: Path, root: Path) -> str:
    """An email saved as it came (`related/emails/<date> <subject>.eml`, s04-D08) as a page: its From, To,
    Cc, Date and Subject, its text, and its attachments by name. An HTML-only body shows in a sandboxed
    frame, so nothing in it runs; read only."""
    from email import policy
    from email.parser import BytesParser
    msg = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
    heads = "".join(f"<tr><th>{h}</th><td>{_e(str(msg[h]))}</td></tr>" for h in ("From", "To", "Cc", "Date", "Subject")
                    if msg[h])
    part = msg.get_body(preferencelist=("plain", "html"))
    text = part.get_content() if part is not None else ""
    if part is not None and part.get_content_type() == "text/html":
        body = (f'<iframe sandbox title="the email" style="width:100%;height:70vh;border:1px solid #ddd" '
                f'srcdoc="{_e(text)}"></iframe>')
    else:
        body = f'<pre style="white-space:pre-wrap;font:14px/1.55 -apple-system,sans-serif">{_e(text.strip())}</pre>'
    files = [(a.get_filename() or "attachment", len(a.get_payload(decode=True) or b"")) for a in msg.iter_attachments()]
    kept = ("<p><b>Attachments</b>: " + " · ".join(f"{_e(n)} ({k // 1024 or 1} KB)" for n, k in files) + "</p>"
            if files else "")
    return ('<!doctype html><meta charset=utf-8><title>' + _e(str(msg["Subject"] or path.name)) + '</title>'
            '<style>body{font:15px/1.5 -apple-system,sans-serif;max-width:880px;margin:0 auto;padding:18px 28px;'
            'background:#fff;color:#111}th{text-align:left;padding:2px 14px 2px 0;color:#555;font-weight:500}'
            'table{margin-bottom:12px}</style>'
            f'<p style="font-size:13px;color:#666">{_e(path.name)} · an email, as it came · '
            f'<a href="/{_e(quote(_rel(path, root)))}">the .eml ↓</a></p><table>{heads}</table>{kept}<hr>{body}')


def related_items(block: Path) -> list:
    """Each related item, in the order its rows show: one per related/related.md row, then each file kept in
    a subfolder of related/ that no row names yet ("no row yet"). Its groups are its subfolder first, then
    the row's `group` cell, names split at commas like a topic's **Tags:** line (JL 261011: "for the related,
    we have the things like subfolders and can give them the group name"): a meeting's notes in meetings/
    sit under meetings, not Untagged. A row kept as a web link has no subfolder, so its `kind` stands in
    (JL 261013: the groups are "things like meeting, email, paper"). `key` is the row's link, else its item."""
    folder = block / "related"
    heads, rows = related_rows(block)
    meta_cols = [h for h in heads if h and h not in ("item", "link", "group")]
    items, keys = [], set()
    for n, r in enumerate(rows):
        target = _related_target(r.get("link", ""))
        key = target or "item:" + (r.get("item") or str(n))
        key = key if key not in keys else f"{key}#{n}"
        keys.add(key)
        meta = " · ".join((f"{h} {r[h]}" if h not in ("kind", "date") else r[h]).replace("`", "")
                          for h in meta_cols if r.get(h))
        sub = _related_folder(target) or (r.get("kind") or "").strip().lower()   # its home group: folder, else kind
        items.append({"key": key, "title": r.get("item") or target or "—", "meta": meta, "target": target,
                      "row": n, "folder": sub, "groups": _split_tags(",".join([sub, r.get("group", "")]))})
    for d in sorted(x for x in folder.iterdir() if x.is_dir() and not x.name.startswith((".", "_"))) if folder.is_dir() else []:
        for f in sorted(d.rglob("*")):
            rel_ = f.relative_to(folder).as_posix()
            if f.is_file() and not f.name.startswith(".") and rel_ not in keys:
                keys.add(rel_)
                items.append({"key": rel_, "title": f.name, "meta": f"related/{rel_} · no row yet", "target": rel_,
                              "row": None, "folder": d.name, "groups": [d.name]})
    return _related_versions(folder, items)


def _related_versions(folder: Path, items: list) -> list:
    """Files of one folder that are versions of one thing (`version_roots`: `Proposal-v1.docx` … `-v3.docx`) fold
    into one item, newest version first (JL 261014). The item keeps a row's name, key and groups when one of its
    versions has a row, so a new version dropped in beside it needs no new row."""
    by_dir = {}
    for i in items:
        path = folder / i["target"] if i["target"] and not re.match(r"[a-z][a-z0-9+.-]*:", i["target"], re.I) else None
        if path is not None and path.is_file():
            by_dir.setdefault(path.parent, []).append((i, path))
    gone = set()
    for parent, members in by_dir.items():
        roots = version_roots([path.stem for _, path in members])
        families = {}
        for i, path in members:
            families.setdefault(roots[path.stem], []).append((i, path))
        for root_name, family in families.items():
            if len({path.stem for _, path in family}) < 2:   # one name in two formats (a .docx and its PDF) stays
                continue                                     # as it came: two items, each with its own row
            family.sort(key=lambda m: -m[1].stat().st_mtime)
            stems = [path.stem for _, path in family]
            head = next((i for i, _ in family if i["row"] is not None), family[0][0])
            head["versions"] = [{"label": version_label(path.stem, root_name, True)
                                 + (f" · {path.suffix.lstrip('.')}" if stems.count(path.stem) > 1 else ""),
                                 "target": i["target"], "when": path.stat().st_mtime} for i, path in family]
            if head["row"] is None:
                head["title"] = root_name
            head["meta"] = (head["meta"] + " · " if head["meta"] else "") + f"{len(family)} versions"
            gone.update(id(i) for i, _ in family if i is not head)
    return [i for i in items if id(i) not in gone]


def _related_set_groups(block: Path, item: dict, groups: list) -> None:
    """Write a related item's groups into its row's `group` cell in related/related.md. A table with no
    `group` column gets one at its end; a file with no row yet gets one (its item, link and group). Its
    subfolder's group is never written: the path already says it."""
    groups = [g for g in groups if g.casefold() != (item.get("folder") or "").casefold()]
    table = block / "related" / "related.md"
    lines = table.read_text(encoding="utf-8").splitlines() if table.is_file() else []
    is_rule = lambda line: set(line.replace("|", "").strip()) <= set("-: ")
    cells = lambda line: [c.strip() for c in line.strip().strip("|").split("|")]
    draw = lambda cs: "| " + " | ".join(cs) + " |"
    if not any(line.startswith("|") and not is_rule(line) for line in lines):     # no table yet: the frame's own
        lines += ([""] if lines and lines[-1].strip() else []) + ["| kind | date | item | link | feeds |",
                                                                  "|---|---|---|---|---|"]
    body = [i for i, line in enumerate(lines) if line.startswith("|") and not is_rule(line)]
    head = body.pop(0)
    heads = [c.lower() for c in cells(lines[head])]
    if "group" not in heads:
        n = len(heads)
        for i, line in enumerate(lines):
            if line.startswith("|"):
                fill = "---" if i != head and is_rule(line) else ""
                cs = cells(line) + [fill] * max(0, n - len(cells(line)))
                cs.insert(n, "group" if i == head else fill)
                lines[i] = "|" + "|".join(cs) + "|" if fill else draw(cs)       # a rule line stays |---|
        heads.append("group")
    if item["row"] is None:
        at = max(i for i, line in enumerate(lines) if line.startswith("|")) + 1
        lines.insert(at, draw([{"item": item["title"], "link": f"`{item['target']}`"}.get(h, "") for h in heads]))
    else:
        at = body[item["row"]]
    cs = cells(lines[at]) + [""] * max(0, len(heads) - len(cells(lines[at])))
    cs[heads.index("group")] = ", ".join(groups)
    lines[at] = draw(cs)
    table.write_text("\n".join(lines) + "\n", encoding="utf-8")


def related_view(block: Path, root: Path, sub: str = "") -> Space:
    """The Related view: one folding row per item, opened on its file's preview, under the Studio's group
    bar (group_list, JL 261011): Current, the groups in related/_groups.txt order, Untagged, + Group. Each
    subfolder is a group of its files (meetings/ → meetings, s04-D08); a file no row names yet sits there too,
    and a drag onto another group gives it a row."""
    folder = block / "related"
    items, table_md = related_items(block), folder / "related.md"
    if not items:
        html_ = _empty_view("Nothing related yet. What came in from outside (a meeting's notes, a paper, a file "
                            "we were sent, an email, a repo or dataset) is kept once, here, in a subfolder of "
                            "related/ (meetings/, papers/, files/, emails/), and one row in related/related.md (kind "
                            "· date · item · link · feeds · group); the subfolder is its first group, the group "
                            "column adds more.")
    else:
        rows = []
        for i in items:
            attrs, handle, current, chips = _group_parts(i["key"], i["title"], i["groups"], noun="item",
                                                          fixed=(i["folder"],))
            link = _related_link(i["target"], block, root) if i["target"] else ""
            rows.append(f'<details class="topic{"" if i["row"] is not None else " missing"}" data-studio-tags='
                        f'"{_e(json.dumps(i["groups"]))}"{attrs}><summary>{handle}<span class=related-head>'
                        f'<b>{_e(i["title"])}</b>{chips}'
                        + (f'<br><span class=topic-meta>{_e(i["meta"])}</span>' if i["meta"] else "") + "</span>"
                        + f'<span class=topic-pop>{current} {link}</span>'
                        + "</summary>" + (version_panes(i["versions"], lambda v: (
                            f'<p class="mut dv-files">{_e(v["label"])}: {_related_link(v["target"], block, root)}</p>'
                            + _related_preview(v["target"], block, root))) if i.get("versions")
                            else _related_preview(i["target"], block, root)) + "</details>")
        note = (f'<p class=mut>{_link(_reader(table_md, root), "related/related.md")}: one row per item. A '
                'subfolder is a group of its files (meetings/ → meetings); the row\'s group column adds more. '
                'What lands here is not edited again.</p>' if table_md.is_file() else
                '<p class=mut>No related/related.md yet: these files have no row; a drag onto a group adds one.</p>')
        html_ = note + group_list(block, root, "related", [i["groups"] for i in items], "".join(rows))
    return Space(html_,
                 run_types=(run_type("run-add-related-<slug>", "add a related item",
                                     "Add an item to the related/ of {folder}: the file, as it came, in a subfolder "
                                     "of related/ (meetings/, papers/ (open-licensed PDFs only), files/, emails/), "
                                     "and one row in related/related.md (kind · date · item · link · feeds · group; "
                                     "the subfolder is its first group, more go in the group cell, comma-"
                                     "separated).", "haipipe-related"),),
                 disk=(("related/related.md", "one row per item: kind · date · item · link · feeds · group"),
                       ("related/_groups.txt", "the groups, in button order")))


def studio_related(view: Space, block: Path, root: Path, unfold: bool = False) -> Space:
    """Related inside the Studio: the second folding part, under the topic cards (JL 261011: "put the
    related as the second collapse part in the box of the studio items"). `view` is the Block's Related
    Space as its theme fills it (paper: cards by question), else the vanilla table; folded unless a
    Related link opened the page."""
    view = view if view.html else related_view(block, root)
    _, rows = related_rows(block)
    kinds = {}
    for r in rows:
        kind = r.get("kind", "").lower() or "item"
        kinds[kind] = kinds.get(kind, 0) + 1
    counts = " · ".join(f"{k} {n}" for k, n in kinds.items())
    meta = f'related/ · {len(rows)} item{"s" if len(rows) != 1 else ""}' + (f" · {counts}" if counts else "")
    html_ = (f'<details class=studio-related id=studio-related{" open" if unfold else ""}>'
             f'<summary><b>Related</b><span class=related-meta>{_e(meta)}</span></summary>'
             f'<div class=related-in>{view.html}</div></details>')
    return Space(html_, run_types=view.run_types, disk=view.disk)


def studio_delivery(block: Path, root: Path, theme=None) -> str:
    """Delivery inside the Studio: the third folding part, under Related (JL 261014: "a new item after the
    Related to name it as the delivery ... show all the delivery and preview them here"). What came in, then
    what went out: every result in the Block's delivery/, from every Job and Task, as Delivery's own cards,
    each opened on its preview. The top row's Delivery stays the full view: its parts, by source, its build."""
    items = delivery_items(block)
    kinds = {k: sum(k in i["fixed"] for i in items) for k in dict.fromkeys((LIVE_PAGE, *DELIVERY_OPENS.values()))}
    counts = " · ".join(f"{k} {n}" for k, n in kinds.items() if n)
    meta = f'delivery/ · {len(items)} result{"s" if len(items) != 1 else ""}' + (f" · {counts}" if counts else "")
    full = _link(href(block, root, theme or VANILLA, "Delivery"), "the full Delivery")
    body = (delivery_view(block, root, theme) + f'<p class=mut>Each Job\'s and Task\'s part, by source: {full}.</p>'
            if items else _empty_view(f"Nothing delivered yet. What a Block sends (a PDF, a Word file, a deck, a web "
                                      f"page) is built into its delivery/, under its source's path; {full}."))
    return (f'<details class=studio-related id=studio-delivery><summary><b>Delivery</b>'
            f'<span class=related-meta>{_e(meta)}</span></summary><div class=related-in>{body}</div></details>')
