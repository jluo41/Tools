"""SHAPE sentence rehearsal: Markdown drafts joined to stable Bullet addresses."""
import hashlib
import re
import tempfile
import fcntl
from contextlib import contextmanager
from pathlib import Path

from src.plan_shape import iter_plan_bullets, render_bullet, split_bullet_block
from src.outline_version import latest_outline, version_tag


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@contextmanager
def page_lock(page):
    lock = Path(tempfile.gettempdir()) / ("hai-outline-" + digest(str(page.resolve())) + ".lock")
    with lock.open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def draft_path(page):
    """Return the current Outline Markdown, the sole Draft authority."""
    return latest_outline(page.parent / "outline", page.stem)


def preview_path(page):
    """Compatibility name: Draft now lives in the selected Outline file."""
    return draft_path(page)


def read_drafts(page):
    """Read Draft records embedded in the selected Outline Markdown."""
    path = draft_path(page)
    if path is None or not path.is_file():
        return {}
    records = {}
    for block in iter_plan_bullets(path.read_text(encoding="utf-8", errors="replace")):
        if not block.get("draft"):
            continue
        records[block["address"]] = {
            "plan": version_tag(path),
            "bullet-sha256": bullet_token(block),
            "text": block.get("draft", ""),
            "reviews": block.get("reviews", ""),
        }
    return records


def read_legacy_previews(page):
    """Read a retired standalone preview for the one-time migration only."""
    path = page.parent / "outline" / (page.stem + "-preview.md")
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    records = {}
    for match in re.finditer(r"(?ms)^## (C\d+\.P\d+\.B\d+)\s*\n(.*?)(?=^## |\Z)", text):
        header, _, body = match[2].strip().partition("\n\n")
        fields = dict(re.findall(r"(?m)^([\w-]+): (.*)$", header))
        parts = re.split(r"(?m)(?=^> Comment )", body, maxsplit=1)
        records[match[1]] = {**fields, "text": parts[0].strip()}
        if len(parts) > 1:
            records[match[1]]["reviews"] = parts[1].rstrip()
    return records


def read_previews(page):
    """Backward-compatible API returning embedded Draft records."""
    return read_drafts(page)


def read_opening_draft(page):
    """Read the optional page-level Opening Draft from the current Outline."""
    path = draft_path(page)
    if path is None or not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    section = re.search(r"(?ms)^## Opening Draft\s*\n(.*?)(?=^## |\Z)", text)
    if not section:
        return ""
    body = section.group(1).strip()
    draft = re.search(r"(?ms)^Draft:\s*(.*?)(?=^> Comment |\Z)", body)
    return (draft.group(1) if draft else body).strip()


def read_legacy_opening(page):
    """Read the retired C0/P00 Opening candidate for migration only."""
    path = page.parent / "outline" / (page.stem + "-preview.md")
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    candidate = re.search(
        r"(?ms)^## Candidate (?:P00|C0\.P1)(?:\s+·[^\n]*)?\s*\n\s*\n(.*?)(?=^## Candidate job\b|^## Acceptance boundary\b|\Z)",
        text,
    )
    return candidate.group(1).strip() if candidate else ""


def record_token(record):
    # Appending review must not invalidate an otherwise current prose editor.
    return digest(repr(sorted((k, v) for k, v in record.items() if k != "reviews"))) if record else "missing"


def _write_embedded_drafts(plan, records):
    """Atomically update Draft fields, writing drafted Bullets Draft-first."""
    lines = plan.read_text(encoding="utf-8", errors="replace").splitlines()
    output, cn, pn, i = [], 0, 0, 0
    while i < len(lines):
        line = lines[i]
        division = re.match(r"^## (C\d+)\s*·", line)
        if division:
            cn, pn = int(division.group(1)[1:]), 0
        paragraph = re.match(r"^### C\d+\.P(\d+)\s*·", line)
        if paragraph:
            pn = int(paragraph.group(1))
        bullet = re.match(r"^- (?:\[[ xX]\]\s*)?(?:B|S)(\d+)\s*·", line)
        if not bullet:
            output.append(line)
            i += 1
            continue
        address = "C%d.P%d.B%d" % (cn, max(pn, 1), int(bullet.group(1)))
        j = i + 1
        continuation = []
        while j < len(lines) and lines[j].startswith("  ") and not re.match(r"^- ", lines[j]):
            continuation.append(lines[j].strip())
            j += 1
        prefix, tag, point, plan_lines, _old_draft, _old_reviews = split_bullet_block(line, continuation)
        record = records.get(address) or {}
        # A drafted Bullet is written Draft-first: the sentence on the dash
        # line, the planned point in `Point:`, so the folded Outline reads as prose.
        output.extend(render_bullet(prefix, tag, point, plan_lines,
                                    str(record.get("text", "")).strip(),
                                    str(record.get("reviews", "")).strip()))
        i = j
    text = "\n".join(output).rstrip() + "\n"
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=plan.parent,
                                     prefix=".outline-", delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    temporary.replace(plan)


def write_drafts(page, records):
    """Write Draft records into the selected Outline Markdown."""
    plan = draft_path(page)
    if plan is None:
        raise FileNotFoundError("No Outline Markdown exists for this Page")
    if plan.is_symlink() or plan.parent.is_symlink():
        raise ValueError("Outline source must be a local Markdown file")
    _write_embedded_drafts(plan, records)


def write_opening_draft(page, text):
    """Write the optional page-level Opening Draft into the current Outline."""
    if not str(text or "").strip():
        return
    plan = draft_path(page)
    if plan is None:
        raise FileNotFoundError("No Outline Markdown exists for this Page")
    source = plan.read_text(encoding="utf-8", errors="replace")
    section = re.compile(r"(?ms)^## Opening Draft\s*\n.*?(?=^## |\Z)")
    lines = str(text).strip().splitlines()
    replacement = "## Opening Draft\n\nDraft: " + "\n".join(lines) + "\n"
    updated = section.sub(replacement, source, count=1)
    if updated == source:
        updated = source.rstrip() + "\n\n" + replacement
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=plan.parent,
                                     prefix=".outline-", delete=False) as handle:
        handle.write(updated.rstrip() + "\n")
        temporary = Path(handle.name)
    temporary.replace(plan)


def write_previews(page, records):
    """Compatibility API: write Draft records into the Outline Markdown."""
    write_drafts(page, records)


def bullet_token(block):
    return digest(block["body"])


def is_section(page):
    return bool(re.search(r"(?m)^page-type:\s*section\s*$", page.read_text(encoding="utf-8")[:2000]))


def reader_prose(text):
    """Keep authored LaTeX citations visible beside the linked Evidence cell."""
    return re.sub(r"\s+([.,;:!?])", r"\1", re.sub(r"\s+", " ", text)).strip()


def sentence_count(text):
    """Conservative prose boundary check, not a semantic quality verdict.

    Strip citation commands and evidence placeholders; protect decimal points,
    initials and common scholarly abbreviations before counting boundaries.
    """
    text = re.sub(r"\\cite\w*\*?(?:\[[^\]]*\])*\{[^}]*\}", "", text).strip()
    text = re.sub(r"\[[^\]]*\]", "PLACEHOLDER", text)
    text = re.sub(r"(?<=\d)\.(?=\d)", "·", text)
    text = re.sub(r"\b(?:e\.g\.|i\.e\.|et al\.|Dr\.|Mr\.|Ms\.|Prof\.|Fig\.|Eq\.|vs\.)",
                  lambda m: m[0].replace(".", "·"), text, flags=re.I)
    text = re.sub(r"\b(?:[A-Z]\.){2,}|\b[A-Z]\.(?=\s+[A-Z][a-z])",
                  lambda m: m[0].replace(".", "·"), text)
    return len([s for s in re.split(r'[.!?。！？]+["\u201d\u2019\')]*\s*', text) if s.strip()])


def content_seeds(page):
    """Only explicit realizes backlinks supply prose; never guess by position.

    Only non-Section Pages may share a span on its first address. Section
    seeds must be unambiguous single-sentence, single-Bullet realizations.
    """
    records = {}
    section = is_section(page)
    invalid = set()
    text = page.read_text(encoding="utf-8")
    content = re.search(r"(?ms)^## Content\s*\n(.*?)(?=^## |\Z)", text)
    if not content:
        return records
    for line in content[1].splitlines():
        match = re.search(r"<!--\s*realizes:\s*(.*?)\s*-->", line)
        if not match:
            continue
        addresses = re.findall(r"C\d+\.P\d+\.[BS]\d+", match[1])
        addresses = [re.sub(r"\.S(\d+)$", r".B\1", a) for a in addresses]
        if not addresses:
            continue
        prose = re.sub(r"<!--.*?-->", "", line).strip()
        if section and (len(addresses) != 1 or sentence_count(prose) != 1):
            invalid.update(addresses)
            continue
        primary = addresses[0]
        if section and primary in records:
            invalid.add(primary)
            continue
        records.setdefault(primary, {"text": "", "shared": ""})
        records[primary]["text"] = (records[primary]["text"] + " " + prose).strip()
        for address in addresses[1:]:
            records.setdefault(address, {"text": "", "shared": primary})
    for address in invalid:
        records[address] = {"text": "", "shared": "", "unmapped": True}
    return records


def save_preview(page, address, text, expected_bullet, expected_record):
    """Compare-and-save one Draft in the Outline Markdown."""
    if not isinstance(text, str) or len(text) > 20000:
        return None, "Preview must be text of at most 20,000 characters"
    text = " ".join(text.split())
    if "<!--" in text or text.startswith(('> Comment ', '## ')):
        return None, "Preview accepts prose, not hidden address records"
    if text and is_section(page) and sentence_count(text) != 1:
        return None, "One Bullet needs one sentence; split the points or remove repeated sentences before saving"
    with page_lock(page):
        plan = latest_outline(page.parent / "outline", page.stem)
        if plan is None:
            return None, "No Shape exists for this Page"
        blocks = {b["address"]: b for b in iter_plan_bullets(plan.read_text(encoding="utf-8"))}
        if address not in blocks:
            return None, "Bullet no longer exists; reload the workspace"
        if expected_bullet != bullet_token(blocks[address]):
            return None, "Bullet changed; reload and review before saving"
        path = draft_path(page)
        if path is None:
            return None, "No Outline Markdown exists for this Page"
        if path.is_symlink() or path.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        records = read_drafts(page)
        if expected_record != record_token(records.get(address)):
            return None, "This draft changed in another editor; reload before saving"
        records[address] = {**records.get(address, {}), "plan": version_tag(plan),
                            "bullet-sha256": expected_bullet, "text": text}
        write_drafts(page, records)
        return {"address": address, "text": text, "record_token": record_token(records[address]),
                "version": version_tag(plan), "outline": str(path)}, None
