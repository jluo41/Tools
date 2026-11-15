"""One Run's page with its outputs and data rows, and the browser over a finished set."""
from datetime import datetime, timezone

from live import frame
from live.work_progress_records import (
    e, elapsed, kept, location, read_yaml, records, role_of, show,
    text_of,
)
from live.work_progress_html import (
    address, csv_preview, CSVP_CSS, file_url, IMAGES, nav, REFRESH, rows_table,
    source_link, TEXTS, ZOOM,
)
from live.work_progress_deliverables import (
    browse_url, deliverables, short_folder,
)


def parquet_rows(path, n=12):
    """A data table's first rows and its size, read without loading the whole file."""
    try:
        import pyarrow.parquet as pq
        f = pq.ParquetFile(path)
        batch = next(f.iter_batches(batch_size=n), None)
        rows = batch.to_pylist() if batch is not None else []
        return f.metadata.num_rows, f.schema_arrow.names, [[r.get(c) for c in f.schema_arrow.names] for r in rows]
    except Exception:                                              # an unreadable file shows as unreadable, never breaks the page
        return None, [], []


def data_tables(row, root):
    """The data tables a Run's page shows rows of (JL 261021: "could you show some data rows as well?"): the tables
    it wrote (its heavy.yaml), and for a Run that describes a table, that table."""
    res = row["path"] / "result" if row.get("path") else None
    out = [root / str(h["path"]) for h in (read_yaml(res / "heavy.yaml").get("heavy") or [] if res else [])
           if isinstance(h, dict) and str(h.get("path", "")).endswith(".parquet")]
    if role_of(row) == "describe":
        out += [root / str(x) for x in row["card"].get("reads") or [] if str(x).endswith(".parquet") and "{" not in str(x)]
    seen = []
    return [p for p in out if p.is_file() and not (p in seen or seen.append(p))]


def data_section(row, root):
    tables = data_tables(row, root)
    if not tables:
        return ""
    out = f"<h3>Data rows · {len(tables)}</h3>"
    for path in tables:
        total, names, rows = parquet_rows(path)
        size = f"{total:,} rows × {len(names)} columns, first {len(rows)} shown" if total is not None else "could not be read"
        out += (f'<details open data-work-key="rows-{e(path.name)}"><summary><b>{e(path.name)}</b> <span class=mut>{e(size)}</span>'
                f'<div class=mut style="font-size:12px">{e(frame.rel(path, root))}</div></summary>'
                + (rows_table(names, rows) if rows else "") + "</details>")
    return out


def outputs(files, root):
    """A Run's outputs shown, not only linked: figures as pictures, tables as their first rows, small text files and the
    log folded in place; a page (.md, .html) opens in its reader."""
    figs = [p for p in files if p.suffix.lower() in IMAGES]
    csvs = [p for p in files if p.suffix.lower() == ".csv"]
    texts = [p for p in files if p.suffix.lower() in TEXTS]
    logs = [p for p in files if p.suffix.lower() == ".log"]
    pages = [p for p in files if p not in figs + csvs + texts + logs]
    out = CSVP_CSS
    if figs:
        out += f"<h3>Figures · {len(figs)}</h3><div style=\"display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px\">"
        out += "".join(f'<figure style="margin:0"><a href="{file_url(f, root)}" target=_blank rel=noopener><img src="{file_url(f, root)}" '
                       f'alt="{e(f.name)}" loading=lazy style="width:100%;border:1px solid var(--line);border-radius:8px;background:#fff"></a>'
                       f'<figcaption class=mut style="font-size:12.5px;margin-top:4px">{e(f.name)}</figcaption></figure>' for f in figs) + "</div>"
    if csvs:
        out += f"<h3>Tables · {len(csvs)}</h3>"
        for n, f in enumerate(csvs):
            total, cols, table = csv_preview(f)
            size = (f"{total:,} rows × {cols} columns" if total is not None else f"{cols} columns") + (", first 12 shown" if total and total > 12 else "")
            out += (f'<details{" open" if n < 3 else ""} data-work-key="csv-{e(f.name)}"><summary><b>{e(f.name)}</b> '
                    f'<span class=mut>{e(size)}</span> <a href="{file_url(f, root)}" target=_blank rel=noopener>open</a></summary>{table}</details>')
    if pages:
        out += "<h3>Pages</h3><ul>" + "".join(f"<li>{source_link(f, root)}</li>" for f in pages) + "</ul>"
    if texts or logs:
        out += "<h3>Records and logs</h3>"
        for f in texts + logs:
            text = text_of(f)
            text = "\n".join(text.splitlines()[-60:]) if f.suffix == ".log" else text[:4000]
            out += (f'<details data-work-key="txt-{e(f.name)}"><summary><b>{e(f.name)}</b> '
                    f'<span class=mut>{"last 60 lines" if f.suffix == ".log" else ""}</span></summary><pre>{e(text)}</pre></details>')
    return out


def _parquet(path, columns=None):
    import pyarrow.parquet as pq
    return kept(("pq", str(path), path.stat().st_mtime_ns, tuple(columns or ())),
                lambda: pq.read_table(path, columns=columns, partitioning=None), seconds=600)


def fact(column, value):
    """A card's value said with its unit, so a bare number never stands alone: 58 years, 13 reviews."""
    text = str(value).replace(",", ", ") if column.endswith("_list") else str(value)
    if column.endswith("_years"):
        return f"{text} years"
    if "review_count" in column:
        return f"{text} review" + ("" if text == "1" else "s")
    return text


def render_browse(folder, root, get):
    """The finished set a deliverable describes, browsed like the site it is (JL 261021: "我在哪里可以看到我最终的 Virtual
    Set 的成品呢？"): its index level by level (state, city, page), a page's records as cards, one record whole. Its
    `browse:` spec names the set's folder, its index, the index's keys and the record's text and picture fields.
    Returns (body, content type); a picture is sent as its bytes."""
    try:
        n = int(get("item") or 0)
        item = deliverables(folder)[n]
    except (ValueError, IndexError):
        return None, ""
    spec = item.get("browse") or {}
    site = root / str(spec.get("root") or "")
    index = site / str(spec.get("index") or "")
    if not spec or not index.is_file() or not site.resolve().is_relative_to(root.resolve()):
        return None, ""
    keys = spec.get("keys") or ["state", "city", "specialty"]
    man = _parquet(index).to_pandas()
    picked = [get(k) for k in keys]
    count = spec.get("count")
    if all(picked):                                      # one page: its records
        hit = man
        for k, v in zip(keys, picked):
            hit = hit[hit[k] == v]
        if hit.empty:
            return None, ""
        page = site / str(hit.iloc[0][spec.get("file", "file_path")])
        if not page.resolve().is_relative_to(site.resolve()):
            return None, ""
        table = _parquet(page)
        if get("img") not in (None, ""):                 # a record's picture, as bytes
            row = table.slice(int(get("img")), 1).to_pylist()
            pic = row[0].get(spec.get("image")) if row else None
            return (pic, str(row[0].get("portrait_content_type") or "image/jpeg")) if pic else (None, "")
    title = "Browse · " + item["what"]
    trail = [frame.link(browse_url(folder, root, n), "All")]
    for i, k in enumerate(keys):
        if picked[i]:
            trail.append(frame.link(browse_url(folder, root, n, **dict(zip(keys[:i + 1], picked[:i + 1]))), e(picked[i])))
    body = f'<h1>{e(title)}</h1><p class=mut>{" › ".join(trail)} · {e(short_folder(item, frame.rel(site, root), root))}</p>'
    level = next((i for i, v in enumerate(picked) if not v), len(keys))
    if level < len(keys):                                # a level of the index: its values, with pages and records
        sub = man
        for k, v in zip(keys[:level], picked[:level]):
            sub = sub[sub[k] == v]
        g = sub.groupby(keys[level]).agg(pages=(keys[level], "size"), **({"records": (count, "sum")} if count in sub else {}))
        g = g.sort_values("records" if "records" in g else "pages", ascending=False)
        links = "".join(
            f'<a class=bw-item href="{e(browse_url(folder, root, n, **dict(zip(keys[:level + 1], picked[:level] + [name]))))}" '
            f'data-name="{e(str(name).lower())}"><b>{e(name)}</b><span class=mut>'
            + (f'{int(r.records):,} physicians · ' if "records" in g else "") + f'{int(r.pages):,} pages</span></a>'
            for name, r in g.iterrows())
        body += (f'<p><input class=bw-find placeholder="Find a {e(keys[level])}" oninput="const q=this.value.toLowerCase();'
                 f'document.querySelectorAll(\'.bw-item\').forEach(a=>a.style.display=a.dataset.name.includes(q)?\'\':\'none\')"> '
                 f'<span class=mut>{len(g):,} {e(keys[level])} values</span></p><div class=bw-grid>{links}</div>')
    else:                                                # one page: its records as cards, then one whole
        start = int(get("from") or 0)
        cols = [c for c in spec.get("card") or [] if c in table.schema.names]
        rows = table.select(cols).slice(start, 60).to_pylist()
        chosen = get("row")
        if chosen not in (None, ""):
            full = table.slice(int(chosen), 1).to_pylist()[0]
            from live import page_reader
            pic = f'<img src="{e(browse_url(folder, root, n, **dict(zip(keys, picked)), img=chosen))}" style="width:140px;flex:none">' \
                if full.get(spec.get("image")) else ""
            body += ('<h2>One record, whole</h2><div style="display:flex;gap:18px;align-items:flex-start">' + pic
                     + f'<div class=dossier style="flex:1;min-width:0">{page_reader.markdown_html(str(full.get(spec.get("record")) or ""))}</div></div>'
                     + f'<details><summary><b>All {len(full)} fields</b></summary>'
                     + rows_table(("field", "value"), [(k, v) for k, v in full.items() if not isinstance(v, (bytes, bytearray))])
                     + "</details>")
        cards = ""
        for i, r in enumerate(rows, start):
            link = browse_url(folder, root, n, **dict(zip(keys, picked)), row=i, **({"from": start} if start else {}))
            img = browse_url(folder, root, n, **dict(zip(keys, picked)), img=i)
            label = e(str(r.get(cols[0]) if cols else i))
            facts = " · ".join(e(fact(c, r[c])) for c in cols[1:] if r.get(c) not in (None, "", "Not reported in the held sources"))
            cards += (f'<a class=bw-card href="{e(link)}"><img loading=lazy src="{e(img)}" alt="" onerror="this.style.visibility=\'hidden\'">'
                      f'<span><b>{label}</b><br><span class=mut>{facts}</span></span></a>')
        more = (f'<p>{frame.link(browse_url(folder, root, n, **dict(zip(keys, picked)), **{"from": start + 60}), "Next 60 ▸")}</p>'
                if start + 60 < table.num_rows else "")
        body += f'<h2>{table.num_rows:,} records on this page</h2><div class=bw-cards>{cards}</div>{more}'
    css = ("<style>.bw-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 14px}"
           ".bw-item{display:flex;justify-content:space-between;gap:8px;padding:4px 2px;text-decoration:none;color:var(--fg)}"
           ".bw-item:hover b{text-decoration:underline}.bw-find{font:inherit;padding:4px 10px;border:1px solid var(--line);border-radius:999px;width:260px}"
           ".bw-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px 16px}"
           ".bw-card{display:flex;gap:10px;align-items:flex-start;text-decoration:none;color:var(--fg);padding:4px}"
           ".bw-card img{width:48px;height:64px;object-fit:cover;flex:none;background:var(--wash)}.bw-card:hover b{text-decoration:underline}</style>")
    page_html = ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
                 f'<title>{e(title)}</title><style>' + frame.CSS + frame.WORK_CSS + '</style>' + CSVP_CSS + css
                 + '</head><body><main>' + body + '</main></body></html>')
    return page_html, "text/html; charset=utf-8"


def render_run(folder, root, name):
    """One exact Run; name is matched against records, never used as a path."""
    row = next((r for r in records(folder) if r["run"] == name), None)
    if row is None:
        return None
    receipt, card = row["receipt"], row["card"]
    title = address(row, root)
    body = '<h1>' + e(title) + '</h1><p>' + nav(folder, root, "Audience Report", "Execution", "Back to Task · Execution") + '</p>'
    body += '<h2>Goal · Purpose and inputs</h2>' + frame.table(("Field", "Value"), [
        ("Purpose", e(row["purpose"] or "Not recorded separately")), ("Target / version", e(row["target"])),
        ("Input", '<pre>' + e(show(receipt.get("inputs") or card.get("inputs"))) + '</pre>'),
        ("Completion criteria", e(show(card.get("close") or receipt.get("close"))))])
    body += '<h2>Execution · Run record</h2>' + frame.table(("Field", "Value"), [
        ("Status", e(row["status"])), ("Execution location", e(show(location(receipt)))),
        ("Started at", e(show(receipt.get("started_at")))), ("Finished at", e(show(receipt.get("finished_at")))),
        ("Elapsed time", e(elapsed(receipt))), ("Progress", e(show(receipt.get("progress")))),
        ("Worker", e(show(receipt.get("worker") or card.get("agent")))),
        ("Code revision", e(show(receipt.get("git_sha")))), ("Exit code", e(show(receipt.get("exit_code")))),
        ("Error", e(show(receipt.get("failure"))))])
    if row["source"].get("audit"):
        body += '<h3>Record checks</h3><ul>' + ''.join('<li>' + e(note) + '</li>' for note in row["source"]["audit"]) + '</ul>'
    body += '<h2>Results · Findings and interpretation</h2><p>' + e(row["headline"] or "No result summary recorded") + '</p>'
    if "asset-parity" in row["types"]:
        body += '<p>The parity check establishes whether frozen answers match the corresponding service. It does not establish answer accuracy.</p>'
    body += '<p>' + source_link(frame.face(folder), root, "Read the full Task interpretation") + '</p>'
    result = row["source"].get("result_path")
    if not result and row["path"].is_dir():
        result = row["path"] / "result"
    files = []
    if result and result.is_dir() and result.resolve().is_relative_to(root.resolve()):
        files = [p for p in sorted(result.iterdir()) if p.is_file() and not p.is_symlink()][:60]
    body += data_section(row, root) + outputs(files, root)
    body += '<details data-work-key=passes><summary>Passes · Execution attempts within this Run</summary><pre>' + e(show(card.get("passes"))) + '</pre></details>'
    stamp = '<p class=mut data-work-refresh>Last read at ' + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') + ' · Refreshes every 20 seconds</p>'
    body = '<section class=workflow-view data-work-progress=Run>' + stamp + body + '</section>' + REFRESH + ZOOM
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
            '<title>' + e(title) + '</title><style>' + frame.CSS + frame.WORK_CSS
            + '</style></head><body><main>' + body + '</main></body></html>')
