"""Result previews for the Evidence Space: the small table, facts and file
preview shown inside an open Evidence card (moved verbatim from evidence.py).
"""
from __future__ import annotations

import base64
import csv
import html
import io
import json
import mimetypes
import pathlib
import re

# evidence.py imports this module after it defines these two, so load it through live.evidence.

_PREVIEW_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg"}

_PREVIEW_PATH_KEYS = {
    "artifact", "artifacts", "asset", "assets", "figure", "image", "preview",
    "preview_path", "table", "file", "path",
}
_PREVIEW_COPY_KEYS = {
    "reader_takeaway", "caption_claim", "summary", "interpretation",
    "aggregate_values", "outcome",
}
_PREVIEW_SUFFIX_ORDER = {
    ".png": 0, ".jpg": 0, ".jpeg": 0, ".webp": 0, ".svg": 1,
    ".pdf": 2, ".csv": 3, ".tsv": 3, ".md": 4,
}


def _payload(document: dict[str, object]) -> object:
    value = document.get("payload")
    return value if value is not None else {}


def _preview_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(
        isinstance(item, (str, int, float, bool)) for item in value
    ):
        return ", ".join(_preview_scalar(item) for item in value)
    return ""


def _find_preview_scalar(value: object, keys: set[str], *, path: tuple[str, ...] = (),
                         depth: int = 0) -> tuple[str, str]:
    """Find one useful scalar in a shallow Result payload tree."""
    if depth > 3:
        return "", ""
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in keys:
                text = _preview_scalar(child)
                if text:
                    return " · ".join((*path, str(key))), text
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                found = _find_preview_scalar(
                    child, keys, path=(*path, str(key)), depth=depth + 1
                )
                if found[1]:
                    return found
    elif isinstance(value, list):
        for index, child in enumerate(value[:8]):
            found = _find_preview_scalar(
                child, keys, path=(*path, str(index + 1)), depth=depth + 1
            )
            if found[1]:
                return found
    return "", ""


def _preview_label(value: str) -> str:
    return re.sub(r"[_-]+", " ", value).strip().title()
def _value_preview_label(value: str) -> str:
    "Use reader-facing terms for the few Value fields that need context."
    if value.startswith("Historical Cell · "):
        result = value.split(" · ", 1)[1]
        return "Reported Result · " + ("SE" if result == "Se" else result)
    if value == "Replacement Gate":
        return "Gate"
    return value

def _value_preview_rows(value: object, *, prefix: str = "", skip: set[str] | None = None, rows: list[tuple[str, str]] | None = None, limit: int = 40) -> list[tuple[str, str]]:
    """Flatten scalar VALUE payload fields into reader-facing table rows."""
    if rows is None:
        rows = []
    if len(rows) >= limit or not isinstance(value, dict):
        return rows
    skip = {item.lower() for item in (skip or set())}
    for key, child in value.items():
        key_text = str(key)
        if key_text.lower() in skip:
            continue
        label = _preview_label(key_text)
        if prefix:
            label = "%s · %s" % (prefix, label)
        label = _value_preview_label(label)
        if isinstance(child, dict):
            _value_preview_rows(child, prefix=label, skip=skip, rows=rows, limit=limit)
        else:
            text = _preview_scalar(child)
            if not text and child is not None and isinstance(child, (list, tuple)):
                text = json.dumps(child, ensure_ascii=False, default=str)
            if text:
                rows.append((label, text))
        if len(rows) >= limit:
            break
    return rows
def _value_preview_table(payload: object) -> str:
    if not isinstance(payload, dict):
        return ""
    skip = (_PREVIEW_COPY_KEYS - {"outcome"}) | {
        "boundary", "artifact", "artifacts", "preview", "sources"
    }
    rows = _value_preview_rows(payload, skip=skip)
    if not rows:
        return ""
    body = "".join(
        "<tr><th>%s</th><td>%s</td></tr>" %
        (html.escape(label), html.escape(text))
        for label, text in rows
    )
    return ('<div class=evidence-preview-table-wrap><table class="evidence-preview-table evidence-preview-value-table">'
            '<thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>%s</tbody></table></div>' % body)


def _preview_facts(payload: object, *, skip: set[str] | None = None,
                   limit: int = 8, prefix: str = "") -> str:
    if not isinstance(payload, dict):
        return ""
    skip = {item.lower() for item in (skip or set())}
    rows = []
    for key, value in payload.items():
        if str(key).lower() in skip:
            continue
        text = _preview_scalar(value)
        if not text:
            continue
        label = _preview_label(str(key))
        if prefix:
            label = "%s · %s" % (_preview_label(prefix), label)
        rows.append(
            '<div class=evidence-preview-fact><b>%s</b><span>%s</span></div>' %
            (html.escape(label), html.escape(text))
        )
        if len(rows) >= limit:
            break
    return '<div class=evidence-preview-facts>%s</div>' % "".join(rows) if rows else ""


def _preview_table(rows: object, *, limit: int = 8) -> str:
    if not isinstance(rows, list) or not rows or not all(
        isinstance(row, dict) for row in rows[:limit]
    ):
        return ""
    selected = [row for row in rows[:limit] if isinstance(row, dict)]
    columns = []
    for row in selected:
        for key in row:
            if str(key) not in columns:
                columns.append(str(key))
    columns = columns[:8]
    if not columns:
        return ""
    head = "".join(
        "<th>%s</th>" % html.escape(_preview_label(key)) for key in columns
    )
    body = []
    for row in selected:
        cells = []
        for key in columns:
            value = _preview_scalar(row.get(key, ""))
            if not value and row.get(key) is not None:
                value = json.dumps(row.get(key), ensure_ascii=False, default=str)
            cells.append("<td>%s</td>" % html.escape(value))
        body.append("<tr>%s</tr>" % "".join(cells))
    return ('<div class=evidence-preview-table-wrap><table class=evidence-preview-table>'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>') % (
                head, "".join(body)
            )


def _payload_table(payload: object) -> str:
    if isinstance(payload, list):
        return _preview_table(payload)
    if not isinstance(payload, dict):
        return ""
    for key in ("rows", "table", "data", "ladder", "comparisons"):
        table = _preview_table(payload.get(key))
        if table:
            return table
    return ""


def _preview_texts(document: dict[str, object], payload: object) -> list[str]:
    keys = ("reader_takeaway", "caption_claim", "summary", "interpretation",
            "aggregate_values")
    values = []
    for source in (payload, document):
        if not isinstance(source, dict):
            continue
        for key in keys:
            text = _preview_scalar(source.get(key))
            if text and text not in values:
                values.append(text)
    return values


def _preview_path_hints(payload: object) -> tuple[str, list[str]]:
    """Return a unit directory and explicit browser-preview artifact hints."""
    if not isinstance(payload, dict):
        return "", []
    unit = _preview_scalar(payload.get("unit"))
    hints: list[str] = []

    def collect(value: object, key: str = "") -> None:
        if isinstance(value, str):
            if value.strip():
                hints.append(value.strip())
            return
        if isinstance(value, list):
            for item in value:
                collect(item, key)
            return
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                if str(child_key).lower() in _PREVIEW_PATH_KEYS:
                    collect(child_value, str(child_key))

    for key, value in payload.items():
        if str(key).lower() in _PREVIEW_PATH_KEYS:
            collect(value, str(key))
    return unit, hints


def _safe_preview_file(candidate: pathlib.Path, page_home: pathlib.Path) -> pathlib.Path | None:
    try:
        if candidate.is_symlink() or not candidate.is_file():
            return None
        resolved = candidate.resolve()
        root = page_home.resolve()
        relative = resolved.relative_to(root)
        # Hidden lanes must not become a back door into the reader. An explicit
        # archive is readable only when an active Result names its artifact;
        # it is not consulted as a legacy Evidence source.
        if any(part.startswith(".") for part in relative.parts):
            return None
        if len(relative.parts) >= 2 and relative.parts[:2] in (("outline", "evidence"), ("draft", "evidence")):
            return None
        return resolved
    except (OSError, RuntimeError, ValueError):
        return None


def _preview_artifact(record: dict[str, object], page_home: pathlib.Path) -> pathlib.Path | None:
    document = record.get("result_document", {})
    if not isinstance(document, dict):
        return None
    payload = _payload(document)
    unit, hints = _preview_path_hints(payload)
    result_file = record.get("result_file")
    result_dir = result_file.parent if isinstance(result_file, pathlib.Path) else page_home / "results"
    bases = [result_dir, page_home]
    if unit:
        unit_path = pathlib.Path(unit)
        bases.insert(0, unit_path if unit_path.is_absolute() else page_home / unit_path)
        bases.insert(1, unit_path if unit_path.is_absolute() else result_dir / unit_path)
    candidates = []
    for hint in hints:
        raw = hint.split("#", 1)[0].strip().strip("'\"")
        if not raw or "://" in raw or raw.startswith("data:"):
            continue
        path = pathlib.Path(raw)
        if path.is_absolute():
            candidates.append(path)
        else:
            candidates.extend(base / path for base in bases)
    if unit:
        for base in bases[:2]:
            candidates.extend(base / name for name in (
                "preview.png", "figure.png", "table.png", "preview.svg",
                "figure.svg", "preview.pdf", "figure.pdf", "table.pdf",
            ))
    seen = set()
    valid = []
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        found = _safe_preview_file(candidate, page_home)
        if found and found.suffix.lower() in _PREVIEW_SUFFIX_ORDER:
            valid.append(found)
    return min(valid, key=lambda path: _PREVIEW_SUFFIX_ORDER[path.suffix.lower()]) if valid else None


def _render_delimited(path: pathlib.Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:512 * 1024]
        reader = csv.reader(io.StringIO(text), delimiter="\t" if path.suffix.lower() == ".tsv" else ",")
        parsed = []
        for index, row in enumerate(reader):
            parsed.append(row)
            if index >= 8:
                break
    except (OSError, csv.Error):
        return ""
    if not parsed:
        return ""
    columns = [value or "Column %d" % (index + 1)
               for index, value in enumerate(parsed[0][:8])]
    rows = [dict(zip(columns, row[:8])) for row in parsed[1:8]]
    return _preview_table(rows)


def _preview_asset_data(path: pathlib.Path) -> str:
    """Inline a small approved preview because ``results/`` is not public static."""
    if path.suffix.lower() not in _PREVIEW_IMAGE_SUFFIXES | {".pdf"}:
        return ""
    try:
        if path.stat().st_size > 12 * 1024 * 1024:
            return ""
        mime = mimetypes.guess_type(str(path))[0]
        if not mime:
            return ""
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return ""
    return "data:%s;base64,%s" % (mime, encoded)


def _render_preview_artifact(path: pathlib.Path, data_url: str) -> str:
    suffix = path.suffix.lower()
    if not data_url and suffix not in {".csv", ".tsv", ".md"}:
        return ""
    open_link = ('<a class=evidence-preview-link href="%s" target="_blank" rel="noopener">'
                 'Open full preview</a>' % html.escape(data_url, quote=True)) if data_url else ""
    if suffix in _PREVIEW_IMAGE_SUFFIXES:
        return ('<div class=evidence-preview-media><img class=evidence-preview-image '
                'src="%s" alt="Evidence display preview" loading="lazy">%s</div>' %
                (html.escape(data_url, quote=True), open_link))
    if suffix == ".pdf":
        return ('<div class=evidence-preview-media><object class=evidence-preview-pdf '
                'data="%s" type="application/pdf">%s</object>%s</div>' %
                (html.escape(data_url, quote=True), open_link, open_link))
    if suffix in {".csv", ".tsv"}:
        return _render_delimited(path)
    if suffix == ".md":
        try:
            return '<div class=evidence-preview-copy>%s</div>' % _md_lite(
                path.read_text(encoding="utf-8", errors="replace")[:12000]
            )
        except OSError:
            return ""
    return ""


def _result_preview(record: dict[str, object], page_home: pathlib.Path,
                    root: pathlib.Path | None) -> str:
    """Render substantive Result content, never the envelope metadata."""
    fields = record.get("fields", {})
    if fields.get("no selected result"):
        return ('<section class=evidence-preview><div class=evidence-preview-label>Result</div>'
                '<div class=evidence-preview-empty>No Result selected · %s</div></section>' %
                html.escape(str(fields.get("status", "specified"))))
    document = record.get("result_document", {})
    if not isinstance(document, dict):
        document = {}
    payload = _payload(document)
    kind = _evidence_type(record)
    content = []
    artifact = _preview_artifact(record, page_home)
    if artifact:
        rendered = _render_preview_artifact(artifact, _preview_asset_data(artifact))
        if rendered:
            content.append(rendered)

    if kind == "VALUE":
        boundary = _preview_scalar(payload.get("boundary")) if isinstance(payload, dict) else ""
        if boundary:
            content.append('<div class=evidence-preview-copy><p><b>Boundary</b> %s</p></div>' %
                           html.escape(boundary))
        table = _value_preview_table(payload)
        if table:
            content.append(table)
    elif kind == "CITE" and isinstance(payload, dict):
        sources = payload.get("sources")
        if isinstance(sources, list):
            source_cards = []
            for source in sources[:6]:
                if not isinstance(source, dict):
                    continue
                cite = _preview_scalar(source.get("cite"))
                identity = _preview_scalar(source.get("identity"))
                claim = _preview_scalar(source.get("claim"))
                head = " · ".join(value for value in (cite, identity) if value)
                source_cards.append(
                    '<article class=evidence-preview-source><div class=evidence-preview-source-head>'
                    '<b>%s</b><code>%s</code></div><p>%s</p></article>' %
                    (html.escape(head or "Source"), html.escape(identity), html.escape(claim))
                )
            if source_cards:
                content.append("".join(source_cards))
    elif kind == "DISPLAY":
        # A Display is a reader artifact. Keep its preview PDF/image as the
        # only visual preview; payload metadata stays in Traceability.
        content.append(_preview_facts(
            payload,
            skip={"unit", "artifact", "artifacts", "preview", "table", "data", "rows", "values"}
            | _PREVIEW_COPY_KEYS,
        ))
        content.append(_preview_facts(
            payload, skip={"unit", "artifact", "artifacts", "preview"} | _PREVIEW_COPY_KEYS
        ))
    else:
        table = _payload_table(payload)
        if table:
            content.append(table)
        content.append(_preview_facts(payload, skip=_PREVIEW_COPY_KEYS))

    texts = _preview_texts(document, payload)
    if texts:
        content.append('<div class=evidence-preview-copy>%s</div>' % "".join(
            "<p>%s</p>" % html.escape(text) for text in texts[:3]
        ))
    content = [part for part in content if part]
    if not content:
        status = str(record.get("fields", {}).get("status", "not ready"))
        content.append('<div class=evidence-preview-empty>Result content is not available yet · %s</div>' %
                       html.escape(status))
    return '<section class=evidence-preview><div class=evidence-preview-label>Preview</div>%s</section>' % "".join(content)


# looked up when called, never at import: evidence.py re-exports this file's names, so either can be imported first
def _evidence_type(record):
    from live.evidence import _evidence_type as kind
    return kind(record)


def _md_lite(text, heading_prefix=""):
    from live.evidence import _md_lite as md
    return md(text, heading_prefix)
