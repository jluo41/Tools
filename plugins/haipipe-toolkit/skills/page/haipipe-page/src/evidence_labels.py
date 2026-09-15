"""Shared Evidence Label grammar and Result-manifest helpers.

The Page author writes LaTeX-like tokens while the Result manifest carries the
resolved value and provenance.  This module deliberately has a small
standard-library fallback so the read-only Page presenters do not require a
YAML package merely to show a Page.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path


_VALUE = re.compile(r"^\$V_([A-Za-z][A-Za-z0-9_-]*)\$")
_DISPLAY = re.compile(
    r"^\\(figure|table|algorithm)"
    r"\{(D_[A-Za-z][A-Za-z0-9_-]*)\}$"
)
_CITE = re.compile(r"^\\cite\{(C_[A-Za-z][A-Za-z0-9_-]*)\}$")


def classify_token(token: str) -> tuple[str, str]:
    """Return ``(kind, key)`` for a Page token, or ``("", "")``."""
    token = (token or "").strip()
    match = _VALUE.fullmatch(token)
    if match:
        return "VALUE", "V_" + match.group(1)
    match = _DISPLAY.fullmatch(token)
    if match:
        return "DISPLAY", match.group(2)
    match = _CITE.fullmatch(token)
    if match:
        return "CITE", match.group(1)
    return "", ""


def _scalar(raw: str) -> str:
    """Read the small scalar subset used by label metadata."""
    value = raw.strip()
    if not value:
        return ""
    if value.startswith("#"):
        return ""
    if value[0:1] in {"'", '"'} and value[-1:] == value[0]:
        # Evidence tokens deliberately contain LaTeX backslashes (for
        # example ``\cite{C_source}``).  Do not send those author strings
        # through Python's string-literal parser: ``\c`` is not a Python
        # escape and would emit a warning while reading an otherwise valid
        # Result manifest.
        if "\\" in value[1:-1]:
            return value[1:-1]
        try:
            return str(ast.literal_eval(value))
        except (SyntaxError, ValueError):
            return value[1:-1]
    return value.split(" #", 1)[0].strip()


def _inline_list(raw: str) -> list[str]:
    """Parse a simple inline YAML/JSON list of label tokens."""
    raw = raw.strip()
    if not (raw.startswith("[") and raw.endswith("]")):
        return []
    try:
        value = json.loads(raw)
    except (TypeError, ValueError):
        try:
            value = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            value = re.findall(r"(?:'([^']+)'|\"([^\"]+)\")", raw)
            return [a or b for a, b in value]
    return [str(item) for item in value] if isinstance(value, list) else []


def parse_result_labels(text: str) -> list[dict[str, str]]:
    """Parse root-level ``labels:`` metadata without loading arbitrary YAML.

    The canonical form is a list of mappings::

        labels:
          - token: "$V_effect$"
            kind: VALUE
            target: payload.effect
            status: resolved
            display: "100"

    A compact ``labels: ["$V_effect$"]`` form is accepted for migration and
    is normalized to the same mapping shape.
    """
    lines = text.splitlines()
    start = next(
        (index for index, line in enumerate(lines)
         if re.match(r"^labels:\s*", line)),
        None,
    )
    if start is None:
        return []
    header = re.match(r"^labels:\s*(.*)$", lines[start])
    inline = _inline_list(header.group(1)) if header else []
    if inline:
        return [_normalize({"token": token}) for token in inline]

    labels: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in lines[start + 1:]:
        if line and not line[0].isspace():
            break
        match = re.match(r"^\s*-\s+([^:]+):\s*(.*)$", line)
        if match:
            if current:
                labels.append(_normalize(current))
            current = {match.group(1).strip().lower().replace("-", "_"):
                       _scalar(match.group(2))}
            continue
        string_item = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if string_item:
            if current:
                labels.append(_normalize(current))
            current = {"token": _scalar(string_item.group(1))}
            continue
        field = re.match(r"^\s+([^:#]+):\s*(.*)$", line)
        if field and current is not None:
            key = field.group(1).strip().lower().replace("-", "_")
            current[key] = _scalar(field.group(2))
    if current:
        labels.append(_normalize(current))
    return [label for label in labels if label.get("token")]


def _normalize(raw: dict[str, str]) -> dict[str, str]:
    token = raw.get("token") or raw.get("label") or raw.get("placeholder") or ""
    kind, key = classify_token(token)
    normalized = dict(raw)
    normalized["token"] = token
    normalized["kind"] = (raw.get("kind") or kind).upper()
    normalized["key"] = raw.get("key") or key
    display = (raw.get("display") or raw.get("resolved_value") or
               raw.get("resolved") or raw.get("value") or "")
    if display.lower() in {"true", "false"} and not raw.get("display"):
        display = ""
    normalized["display"] = display
    normalized["status"] = (raw.get("status") or
                             ("resolved" if display else "unresolved")).lower()
    return normalized


def collect_result_labels(page_home: Path) -> dict[str, dict[str, str]]:
    """Return the current token-to-binding map from local Result manifests."""
    result_root = page_home / "results"
    if not result_root.is_dir() or result_root.is_symlink():
        return {}
    bindings: dict[str, dict[str, str]] = {}
    for manifest in sorted(result_root.rglob("result.yaml")):
        if manifest.is_symlink():
            continue
        try:
            manifest.resolve().relative_to(result_root.resolve())
            text = manifest.read_text(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            continue
        top = {}
        for key in ("item", "page_run", "run", "status", "display_kind",
                    "provenance", "input"):
            match = re.search(rf"^{re.escape(key)}:\s*([^#\n]+)", text, re.M)
            if match:
                top[key] = _scalar(match.group(1))
        item_id = top.get("item", "")
        if not item_id:
            continue
        for label in parse_result_labels(text):
            token = label["token"]
            label.update({
                "item": item_id,
                "page_run": top.get("page_run", ""),
                "run": top.get("run", ""),
                "result": manifest.relative_to(page_home).as_posix(),
                "result_status": top.get("status", ""),
                "display_kind": label.get("display_kind") or top.get("display_kind", ""),
                "provenance": top.get("provenance", ""),
                "input": top.get("input", ""),
            })
            # A duplicated token is a contract problem; keep the first sorted
            # authority deterministic rather than silently changing a draft.
            bindings.setdefault(token, label)
    return bindings


def resolve_inline_labels(text: str, bindings: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    """Split prose into plain text and resolved-token spans.

    The caller owns HTML escaping.  Each span has ``text``, ``token``, and
    ``binding`` keys; unresolved tokens are returned unchanged.
    """
    token_re = re.compile(
        r"\$V_[A-Za-z][A-Za-z0-9_-]*\$|"
        r"\\(?:figure|table|algorithm)"
        r"\{D_[A-Za-z][A-Za-z0-9_-]*\}|\\cite\{C_[A-Za-z][A-Za-z0-9_-]*\}"
    )
    spans: list[dict[str, object]] = []
    cursor = 0
    for match in token_re.finditer(text):
        if match.start() > cursor:
            spans.append({"text": text[cursor:match.start()]})
        token = match.group(0)
        spans.append({"text": token, "token": token, "binding": bindings.get(token)})
        cursor = match.end()
    if cursor < len(text):
        spans.append({"text": text[cursor:]})
    return spans or [{"text": text}]
