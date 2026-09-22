#!/usr/bin/env python3
"""Promote one accepted Page Paragraph Result into the Page source.

This is the narrow write path for CONTENT/WRITE.  It deliberately does not
ask a model to find or paste prose: the Run target and the Page's structural
``C<n>.P<m>`` position determine the one source slice that may change.

Usage::

    python3 promote_paragraph.py --page PAGE.md --result RESULT_DIR

The Result directory must contain ``paragraph.md``, ``trace.md`` and
``runtime.yaml``.  ``runtime.yaml`` must report a complete Page paragraph Run
and pin the Page source hash that was read before the Run started.  Promotion
is idempotent after a successful write and records its own nested lifecycle
object in ``runtime.yaml``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback keeps the hash gate
    fcntl = None


TARGET_RE = re.compile(r"^C([1-9][0-9]*)\.P([1-9][0-9]*)$")
CONTENT_RE = re.compile(r"^\s*## Content(?:\s|$)")
TOP_HEADING_RE = re.compile(r"^## (?!#)")
DIVISION_RE = re.compile(r"^### (?!#)")
PARAGRAPH_HEADING_RE = re.compile(r"^#### (?!#)")
FENCE_RE = re.compile(r"^\s*```")
COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class PromotionError(RuntimeError):
    """A safe promotion refusal with an actionable reason."""


@dataclass(frozen=True)
class ParagraphSpan:
    division: int
    paragraph: int
    body_start: int
    body_end: int
    heading_line: int | None = None

    @property
    def locator(self) -> dict[str, int]:
        """Return one-based source coordinates for the promotion receipt."""
        start = self.body_start + 1
        end = max(start, self.body_end)
        return {
            "division": self.division,
            "paragraph": self.paragraph,
            "line_start": start,
            "line_end": end,
        }


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _page_newline(data: bytes) -> str:
    """Return the sole newline style, refusing mixed or legacy CR files."""
    crlf_count = data.count(b"\r\n")
    remainder = data.replace(b"\r\n", b"")
    if b"\r" in remainder:
        raise PromotionError(
            "Page source uses a legacy or mixed carriage-return newline style; "
            "normalize it before promotion"
        )
    if crlf_count and b"\n" in remainder:
        raise PromotionError(
            "Page source has mixed LF and CRLF newlines; normalize it before promotion"
        )
    return "\r\n" if crlf_count else "\n"


def _load_mapping(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PromotionError(f"cannot read YAML {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PromotionError(f"{path} must contain a YAML mapping")
    return value


def _target_parts(target: str) -> tuple[int, int]:
    match = TARGET_RE.fullmatch(target.strip())
    if not match:
        raise PromotionError(
            f"invalid target {target!r}; expected C<n>.P<m>, for example C2.P1"
        )
    return int(match.group(1)), int(match.group(2))


def _trim_bounds(lines: list[str], start: int, end: int) -> tuple[int, int]:
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return start, end


def _is_lane_or_comment(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith(">") or bool(COMMENT_RE.fullmatch(line))


def _outside_fence_indices(
    lines: list[str], start: int, end: int, pattern: re.Pattern[str]
) -> list[int]:
    """Find headings without interpreting fenced examples as Page structure."""
    indices: list[int] = []
    fenced = False
    for index in range(start, end):
        line = lines[index]
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if not fenced and pattern.match(line):
            indices.append(index)
    return indices


def _is_structural_block(block: list[str]) -> bool:
    """Whether a rough Markdown block is not one prose paragraph."""
    for line in block:
        stripped = line.lstrip()
        if not stripped:
            continue
        if FENCE_RE.match(line):
            return True
        if "<!--" in line or "-->" in line:
            return True
        if re.match(r"^(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|\||>)", stripped):
            return True
    return False


def _rough_blocks(lines: list[str], start: int, end: int) -> list[tuple[int, int]]:
    """Split one division into blank-line blocks, respecting code fences."""
    blocks: list[tuple[int, int]] = []
    i = start
    while i < end:
        while i < end and not lines[i].strip():
            i += 1
        if i >= end:
            break
        block_start = i
        fenced = False
        while i < end:
            line = lines[i]
            if FENCE_RE.match(line):
                fenced = not fenced
            i += 1
            if i < end and not fenced and not lines[i].strip():
                break
        block_end = i
        while block_end > block_start and not lines[block_end - 1].strip():
            block_end -= 1
        blocks.append((block_start, block_end))
        i = block_end
    return blocks


def _prose_spans(lines: list[str], start: int, end: int) -> list[tuple[int, int]]:
    """Return prose blocks without counting standalone apparatus/comments."""
    out: list[tuple[int, int]] = []
    for block_start, block_end in _rough_blocks(lines, start, end):
        block = lines[block_start:block_end]
        nonblank = [line for line in block if line.strip()]
        if not nonblank:
            continue
        if all(_is_lane_or_comment(line) for line in nonblank):
            continue
        if _is_structural_block(block):
            continue
        out.append((block_start, block_end))
    return out


def _has_structural_blocks(lines: list[str], start: int, end: int) -> bool:
    """Whether a division contains a non-prose block that needs its own owner."""
    for block_start, block_end in _rough_blocks(lines, start, end):
        block = lines[block_start:block_end]
        nonblank = [line for line in block if line.strip()]
        if nonblank and not all(_is_lane_or_comment(line) for line in nonblank):
            if _is_structural_block(block):
                return True
    return False


def _division_ranges(
    lines: list[str], content_start: int, content_end: int
) -> list[tuple[int, int, int | None]]:
    """Return ``(ordinal, body_start, body_end)`` for Content divisions."""
    headers = _outside_fence_indices(lines, content_start, content_end, DIVISION_RE)
    if not headers:
        return [(1, content_start, content_end)]

    prelude_start, prelude_end = _trim_bounds(lines, content_start, headers[0])
    if prelude_start < prelude_end:
        raise PromotionError(
            "## Content has unheaded prose before its first ### division; "
            "the C/P address is not safe to infer"
        )

    ranges: list[tuple[int, int, int | None]] = []
    for ordinal, header in enumerate(headers, 1):
        next_header = headers[ordinal] if ordinal < len(headers) else content_end
        ranges.append((ordinal, header + 1, next_header))
    return ranges


def find_paragraph(lines: list[str], target: str) -> ParagraphSpan:
    """Resolve a Page paragraph by Content division and paragraph ordinal."""
    division_number, paragraph_number = _target_parts(target)
    content_headers = _outside_fence_indices(lines, 0, len(lines), CONTENT_RE)
    if len(content_headers) != 1:
        raise PromotionError(
            f"expected exactly one ## Content section, found {len(content_headers)}"
        )
    content_start = content_headers[0] + 1
    top_headers = _outside_fence_indices(
        lines, content_start, len(lines), TOP_HEADING_RE
    )
    content_end = top_headers[0] if top_headers else len(lines)
    divisions = _division_ranges(lines, content_start, content_end)
    selected = next(
        (item for item in divisions if item[0] == division_number), None
    )
    if selected is None:
        raise PromotionError(
            f"{target} names Content division {division_number}, but the Page has "
            f"{len(divisions)} addressable division(s)"
        )
    _ordinal, division_start, division_end = selected

    paragraph_headers = _outside_fence_indices(
        lines, division_start, division_end, PARAGRAPH_HEADING_RE
    )
    if paragraph_headers:
        if paragraph_number > len(paragraph_headers):
            raise PromotionError(
                f"{target} has no paragraph heading in division {division_number}; "
                "create the Page scaffold before promoting a new headed paragraph"
            )
        heading_line = paragraph_headers[paragraph_number - 1]
        body_limit = (
            paragraph_headers[paragraph_number]
            if paragraph_number < len(paragraph_headers)
            else division_end
        )
        body_start, body_end = _trim_bounds(lines, heading_line + 1, body_limit)
        prose_spans = _prose_spans(lines, heading_line + 1, body_limit)
        if len(prose_spans) > 1:
            raise PromotionError(
                f"{target} has more than one prose block under its #### heading; "
                "split the Page scaffold before promoting"
            )
        if len(prose_spans) == 1:
            body_start, body_end = prose_spans[0]
            for block_start, block_end in _rough_blocks(
                lines, heading_line + 1, body_limit
            ):
                if (block_start, block_end) == (body_start, body_end):
                    continue
                block = lines[block_start:block_end]
                nonblank = [line for line in block if line.strip()]
                if nonblank and not all(_is_lane_or_comment(line) for line in nonblank):
                    raise PromotionError(
                        f"{target} has a structural block beside its prose body; "
                        "promote it through the owning Page unit"
                    )
        else:
            for block_start, block_end in _rough_blocks(
                lines, heading_line + 1, body_limit
            ):
                block = lines[block_start:block_end]
                nonblank = [line for line in block if line.strip()]
                if nonblank:
                    raise PromotionError(
                        f"{target} has no prose-only body; its headed span contains "
                        "apparatus or a structural block"
                    )
        return ParagraphSpan(
            division_number,
            paragraph_number,
            body_start,
            body_end,
            heading_line=heading_line,
        )

    spans = _prose_spans(lines, division_start, division_end)
    if paragraph_number <= len(spans):
        body_start, body_end = spans[paragraph_number - 1]
        return ParagraphSpan(division_number, paragraph_number, body_start, body_end)
    if paragraph_number == len(spans) + 1:
        if _has_structural_blocks(lines, division_start, division_end):
            raise PromotionError(
                f"{target} would be inserted after a structural block in division "
                f"{division_number}; create the Page paragraph scaffold first"
            )
        _body_start, insert_at = _trim_bounds(lines, division_start, division_end)
        return ParagraphSpan(division_number, paragraph_number, insert_at, insert_at)
    raise PromotionError(
        f"{target} has no paragraph in division {division_number}; found "
        f"{len(spans)} prose paragraph(s)"
    )


def _candidate_lines(path: Path) -> list[str]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PromotionError(f"cannot read paragraph Result {path}: {exc}") from exc
    lines = raw.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise PromotionError("paragraph.md is empty")
    if any(not line.strip() for line in lines):
        raise PromotionError(
            "paragraph.md contains an internal blank line; a Paragraph Result "
            "must contain exactly one paragraph"
        )
    if all(_is_lane_or_comment(line) for line in lines):
        raise PromotionError("paragraph.md contains no prose line")
    if _is_structural_block(lines):
        raise PromotionError(
            "paragraph.md contains a heading, list, quote, table, or code fence; "
            "promotion accepts one prose paragraph only"
        )
    return lines


def _check_source_span(lines: list[str], span: ParagraphSpan) -> None:
    for line in lines[span.body_start : span.body_end]:
        if line.lstrip().startswith(">"):
            raise PromotionError(
                "the target paragraph already has a > apparatus lane; refusing to "
                "orphan a citation/comment/change record. Use the owner's lane "
                "migration or sentence-level writer first"
            )
        if COMMENT_RE.fullmatch(line):
            raise PromotionError(
                "the target paragraph contains a source comment/change record; "
                "refusing to delete it. Use the owner's annotation-aware writer "
                "or migrate the record first"
            )
        if FENCE_RE.match(line) or re.match(
            r"^\s*(?:[-*+]\s|\d+[.)]\s|\||#{1,6}\s)", line
        ):
            raise PromotionError(
                "the target span contains a Markdown block construct; refusing "
                "to replace it as a prose paragraph"
            )


def _page_input_hash(runtime: dict[str, Any], page: Path, runtime_path: Path) -> str:
    candidates: list[Any] = []
    for key in ("page_before_sha256", "source_page_sha256"):
        if runtime.get(key):
            candidates.append(runtime[key])
    inputs = runtime.get("inputs")
    if isinstance(inputs, dict):
        inputs = [inputs]
    if isinstance(inputs, list):
        for item in inputs:
            if not isinstance(item, dict):
                continue
            role = str(item.get("role", "")).lower()
            raw_path = item.get("path")
            if role in {"page", "page-source", "source-page", "current-page"}:
                if item.get("sha256"):
                    candidates.append(item["sha256"])
                continue
            if raw_path and _path_matches(raw_path, page, runtime_path.parent):
                if item.get("sha256"):
                    candidates.append(item["sha256"])
    if not candidates:
        raise PromotionError(
            "runtime.yaml does not pin the Page source hash; add an inputs entry "
            "with role: page-source, path: <page.md>, and sha256 before promotion"
        )
    values = []
    for candidate in candidates:
        value = str(candidate).strip().lower()
        if not SHA256_RE.fullmatch(value):
            raise PromotionError(f"invalid pinned Page sha256 {candidate!r}")
        values.append(value)
    distinct = sorted(set(values))
    if len(distinct) != 1:
        raise PromotionError(
            "runtime.yaml contains conflicting frozen Page hashes; re-freeze the "
            "Run inputs before promotion"
        )
    return distinct[0]


def _path_matches(raw_path: Any, page: Path, base: Path) -> bool:
    value = str(raw_path)
    if value.startswith("<") or value.startswith("$"):
        return False
    path = Path(value)
    options = []
    if path.is_absolute():
        options.append(path)
    else:
        options.extend((base / path, page.parent / path, path))
    wanted = page.resolve()
    return any(option.resolve() == wanted for option in options)


def _validate_runtime(
    runtime: dict[str, Any], target: str, result_dir: Path, page: Path
) -> None:
    if str(runtime.get("family", "")).lower() != "page":
        raise PromotionError("runtime.yaml family must be page")
    if runtime.get("operation") != "paragraph-writing":
        raise PromotionError("runtime.yaml operation must be paragraph-writing")
    run_name = str(runtime.get("run", "")).strip()
    if not run_name:
        raise PromotionError("runtime.yaml must identify the Paragraph Run in run")
    if runtime.get("target") != target:
        raise PromotionError(
            f"runtime target {runtime.get('target')!r} does not match {target}"
        )
    if str(runtime.get("status", "")).lower() != "complete":
        raise PromotionError(
            "only a complete Paragraph Result may be promoted; "
            f"runtime status is {runtime.get('status')!r}"
        )
    result_ref = runtime.get("result")
    if not result_ref:
        raise PromotionError("runtime.yaml must resolve the Result directory in result")
    ref = Path(str(result_ref))
    if ref.is_absolute():
        candidates = [ref]
    else:
        # Accept the three ordinary haipipe-run spellings: ./ from the
        # Result folder, a run name from results/, or results/<run> from
        # the Page root.  Do not silently accept an unrelated path.
        candidates = [
            result_dir / ref,
            result_dir.parent / ref,
            result_dir.parent.parent / ref,
            page.parent / ref,
        ]
    if not any(
        candidate.resolve() == result_dir.resolve() for candidate in candidates
    ):
        raise PromotionError(
            f"runtime result {result_ref!r} does not resolve to {result_dir}"
        )


@contextmanager
def _page_lock(page: Path):
    """Serialize promotions targeting one Page source on POSIX hosts."""
    if fcntl is None:  # pragma: no cover - the optimistic hash gate still applies
        yield
        return
    lock_key = hashlib.sha256(str(page).encode("utf-8")).hexdigest()
    lock_path = Path(tempfile.gettempdir()) / f"haipipe-page-promotion-{lock_key}.lock"
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    except OSError as exc:
        raise PromotionError(
            f"cannot create Page promotion lock {lock_path}: {exc}"
        ) from exc
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
        except OSError as exc:
            raise PromotionError(f"cannot lock Page source {page}: {exc}") from exc
        yield
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _atomic_write(path: Path, text: str) -> None:
    """Write one file beside itself and replace it only after a full write."""
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temp = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp, mode)
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def _dump_runtime(runtime: dict[str, Any]) -> str:
    return yaml.safe_dump(
        runtime,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def promote(
    page: Path,
    result_dir: Path,
    target: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Validate and promote one Paragraph Result; return a receipt summary."""
    page = page.expanduser().resolve()
    result_dir = result_dir.expanduser().resolve()
    if not page.is_file():
        raise PromotionError(f"Page source is not a file: {page}")
    with _page_lock(page):
        return _promote_locked(page, result_dir, target, dry_run)


def _promote_locked(
    page: Path,
    result_dir: Path,
    target: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run the optimistic/hash-checked promotion while the Page lock is held."""
    if not page.is_file():
        raise PromotionError(f"Page source is not a file: {page}")
    if not result_dir.is_dir():
        raise PromotionError(f"Result directory is not a directory: {result_dir}")

    paragraph_path = result_dir / "paragraph.md"
    trace_path = result_dir / "trace.md"
    runtime_path = result_dir / "runtime.yaml"
    for required in (paragraph_path, trace_path, runtime_path):
        if not required.is_file():
            raise PromotionError(f"missing required Result file: {required.name}")

    runtime = _load_mapping(runtime_path)
    resolved_target = str(target or runtime.get("target") or "").strip()
    _target_parts(resolved_target)
    _validate_runtime(runtime, resolved_target, result_dir, page)

    try:
        trace = trace_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PromotionError(f"cannot read trace.md: {exc}") from exc
    if resolved_target not in trace:
        raise PromotionError(
            f"trace.md does not mention target {resolved_target}; refusing an "
            "untraceable Page write"
        )
    lowered_trace = trace.lower()
    for phrase in (
        "style verdict: revise",
        "status: blocked",
        "pre_check: blocked",
        "upstream block",
    ):
        if phrase in lowered_trace:
            raise PromotionError(
                f"trace.md reports {phrase!r}; resolve the upstream block "
                "before promotion"
            )

    candidate = _candidate_lines(paragraph_path)
    page_bytes = page.read_bytes()
    page_hash_before = _sha256_bytes(page_bytes)
    expected_page_hash = _page_input_hash(runtime, page, runtime_path)

    promotion = runtime.get("promotion")
    if promotion is not None and not isinstance(promotion, dict):
        raise PromotionError("runtime.yaml promotion must be a mapping when present")
    promotion = dict(promotion or {})
    promotion_status = str(promotion.get("status", "")).lower()
    if promotion_status not in {"", "applying", "promoted"}:
        raise PromotionError(
            f"runtime.yaml has unsupported promotion status {promotion.get('status')!r}"
        )
    result_hash = _sha256_file(paragraph_path)

    try:
        page_text = page_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PromotionError(f"Page source is not UTF-8 Markdown: {exc}") from exc
    newline = _page_newline(page_bytes)
    lines = page_text.splitlines()

    if promotion_status == "promoted":
        recorded_result_hash = str(promotion.get("result_sha256", "")).lower()
        if recorded_result_hash and recorded_result_hash != result_hash:
            raise PromotionError(
                "runtime.yaml says this Result was promoted, but paragraph.md has "
                "changed; keep the accepted Result immutable and create a new Run"
            )
        after_hash = str(promotion.get("page_after_sha256", "")).lower()
        if after_hash != page_hash_before:
            raise PromotionError(
                "runtime.yaml says this Result was promoted, but the Page source "
                "hash no longer matches its promotion receipt"
            )
        span = find_paragraph(lines, resolved_target)
        if lines[span.body_start : span.body_end] != candidate:
            raise PromotionError(
                "runtime.yaml says this Result was promoted, but the addressed "
                "Page paragraph differs from paragraph.md"
            )
        return {
            "status": "already-promoted",
            "target": resolved_target,
            "page": str(page),
            "result": str(result_dir),
            "result_sha256": result_hash,
            "page_before_sha256": page_hash_before,
            "page_after_sha256": after_hash,
            "source_locator": promotion.get("source_locator"),
        }

    if promotion_status == "applying":
        recorded_result_hash = str(promotion.get("result_sha256", "")).lower()
        if recorded_result_hash and recorded_result_hash != result_hash:
            raise PromotionError(
                "an interrupted promotion references a different paragraph Result; "
                "refusing recovery"
            )
        recorded_before_hash = str(
            promotion.get("page_before_sha256", expected_page_hash)
        ).lower()
        if recorded_before_hash != expected_page_hash:
            raise PromotionError(
                "an interrupted promotion has a different frozen Page hash; "
                "re-freeze the Run before recovery"
            )
        planned = str(promotion.get("planned_page_after_sha256", "")).lower()
        if planned and planned == page_hash_before:
            span = find_paragraph(lines, resolved_target)
            if lines[span.body_start : span.body_end] != candidate:
                raise PromotionError(
                    "an interrupted promotion found a different paragraph at the "
                    "target; refusing recovery"
                )
            promotion["status"] = "promoted"
            promotion["page_after_sha256"] = page_hash_before
            promotion["promoted_at"] = _now()
            runtime["promotion"] = promotion
            if not dry_run:
                try:
                    _atomic_write(runtime_path, _dump_runtime(runtime))
                except OSError as exc:
                    raise PromotionError(
                        "could not finalize the recovered promotion receipt; "
                        "the Page is already promoted, retry the same command"
                    ) from exc
            return {
                "status": "dry-run" if dry_run else "promoted",
                "target": resolved_target,
                "page": str(page),
                "result": str(result_dir),
                "result_sha256": result_hash,
                "page_before_sha256": promotion.get("page_before_sha256"),
                "page_after_sha256": page_hash_before,
                "source_locator": promotion.get("source_locator"),
                "recovered": True,
            }

    if page_hash_before != expected_page_hash:
        raise PromotionError(
            "Page source changed after the Run was frozen; refusing stale promotion "
            f"(expected {expected_page_hash}, found {page_hash_before}). "
            "Create a new Run or explicitly re-freeze its inputs."
        )

    span = find_paragraph(lines, resolved_target)
    _check_source_span(lines, span)
    old_body = lines[span.body_start : span.body_end]
    had_final_newline = page_text.endswith(newline)
    prefix = lines[: span.body_start]
    suffix = lines[span.body_end :]
    if span.body_start == span.body_end:
        # A new paragraph is inserted at the trimmed end of an otherwise
        # prose-only division.  Add separators only when the existing source
        # does not already provide them, leaving headings and sibling text
        # byte-for-byte represented by the surrounding logical lines.
        before = [] if not prefix or not prefix[-1].strip() else [""]
        after = [] if not suffix or not suffix[0].strip() else [""]
        new_lines = prefix + before + candidate + after + suffix
    else:
        new_lines = prefix + candidate + suffix
    new_text = newline.join(new_lines)
    if had_final_newline:
        new_text += newline
    new_bytes = new_text.encode("utf-8")
    page_hash_after = _sha256_bytes(new_bytes)

    receipt = {
        "status": "applying",
        "target": resolved_target,
        "page": str(page),
        "result": str(result_dir),
        "result_sha256": result_hash,
        "page_before_sha256": page_hash_before,
        "planned_page_after_sha256": page_hash_after,
        "source_locator": span.locator,
        "started_at": _now(),
    }
    outcome = {
        "status": "dry-run" if dry_run else "promoted",
        "target": resolved_target,
        "page": str(page),
        "result": str(result_dir),
        "result_sha256": result_hash,
        "page_before_sha256": page_hash_before,
        "page_after_sha256": page_hash_after,
        "source_locator": span.locator,
        "replaced_line_count": len(old_body),
        "new_line_count": len(candidate),
    }
    if dry_run:
        return outcome

    runtime["promotion"] = receipt
    try:
        _atomic_write(runtime_path, _dump_runtime(runtime))
        latest_page_hash = _sha256_file(page)
        if latest_page_hash != page_hash_before:
            raise PromotionError(
                "Page source changed during promotion preparation; the applying "
                "receipt was retained and the stale write was refused"
            )
        _atomic_write(page, new_text)
    except PromotionError:
        raise
    except OSError as exc:
        raise PromotionError(
            "promotion write failed after the lifecycle receipt was prepared; "
            "inspect runtime.yaml and retry the same Run"
        ) from exc

    verify_hash = _sha256_file(page)
    if verify_hash != page_hash_after:
        raise PromotionError(
            "Page write verification failed: source hash differs from the planned "
            "promotion result"
        )
    verify_lines = page.read_text(encoding="utf-8").splitlines()
    verify_span = find_paragraph(verify_lines, resolved_target)
    if verify_lines[verify_span.body_start : verify_span.body_end] != candidate:
        raise PromotionError(
            "Page write verification failed: addressed paragraph differs from Result"
        )

    receipt["status"] = "promoted"
    receipt["page_after_sha256"] = verify_hash
    receipt["promoted_at"] = _now()
    runtime["promotion"] = receipt
    try:
        _atomic_write(runtime_path, _dump_runtime(runtime))
    except OSError as exc:
        raise PromotionError(
            "Page content was written and verified, but the final promotion "
            "receipt could not be saved; retry the same command to recover it"
        ) from exc
    return outcome


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Promote one accepted Page Paragraph Result into page.md"
    )
    parser.add_argument("--page", required=True, type=Path, help="Page source .md")
    parser.add_argument(
        "--result", required=True, type=Path, help="Paragraph Result directory"
    )
    parser.add_argument(
        "--target", help="C<n>.P<m>; defaults to runtime.yaml target"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and show the write without changing files",
    )
    parser.add_argument("--json", action="store_true", help="print the outcome as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        outcome = promote(args.page, args.result, args.target, args.dry_run)
    except PromotionError as exc:
        if args.json:
            print(
                json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False)
            )
        else:
            print(f"BLOCKED: {exc}")
        return 2
    if args.json:
        print(json.dumps(outcome, ensure_ascii=False, sort_keys=True))
    else:
        print(
            f"{outcome['status']}: {outcome['target']} → {outcome['page']} "
            f"(Page {outcome['page_before_sha256']} → {outcome['page_after_sha256']})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
