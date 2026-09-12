"""SHAPE sentence rehearsal: Markdown drafts joined to stable Bullet addresses."""
import hashlib
import re
import tempfile
import fcntl
from contextlib import contextmanager
from pathlib import Path

from src.plan_shape import iter_plan_bullets
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


def preview_path(page):
    return page.parent / "outline" / (page.stem + "-preview.md")


def read_previews(page):
    path = preview_path(page)
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    records = {}
    for match in re.finditer(r"(?ms)^## (C\d+\.P\d+\.B\d+)\s*\n(.*?)(?=^## |\Z)", text):
        header, _, body = match[2].strip().partition("\n\n")
        fields = dict(re.findall(r"(?m)^([\w-]+): (.*)$", header))
        # Signed preview comments are review apparatus, never candidate prose.
        parts = re.split(r"(?m)(?=^> Comment )", body, maxsplit=1)
        records[match[1]] = {**fields, "text": parts[0].strip()}
        if len(parts) > 1:
            records[match[1]]["reviews"] = parts[1].rstrip()
    return records


def record_token(record):
    # Appending review must not invalidate an otherwise current prose editor.
    return digest(repr(sorted((k, v) for k, v in record.items() if k != "reviews"))) if record else "missing"


def write_previews(page, records):
    """Atomic write under page_lock; preserve signed review lanes verbatim."""
    path = preview_path(page)
    output = "# %s · Content preview\n\nPlanning draft for discussion; not promoted Page Content.\n" % page.stem
    for key, record in records.items():
        output += "\n## %s\nplan: %s\nbullet-sha256: %s\n\n%s\n" % (
            key, record["plan"], record["bullet-sha256"], record["text"])
        if record.get("reviews"):
            output += "\n" + record["reviews"] + "\n"
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix=".preview-", delete=False) as handle:
        handle.write(output)
        temporary = Path(handle.name)
    temporary.replace(path)


def bullet_token(block):
    return digest(block["body"])


def is_section(page):
    return bool(re.search(r"(?m)^page-type:\s*section\s*$", page.read_text(encoding="utf-8")[:2000]))


def reader_prose(text):
    """Sources are in the adjacent Evidence cell; TeX stays in the editor."""
    text = re.sub(r"\\cite\w*\*?(?:\[[^\]]*\])*\{[^}]*\}", "", text)
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
    """Compare-and-save one rehearsal; approved Shape and Page stay immutable."""
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
        path = preview_path(page)
        if path.is_symlink() or path.parent.is_symlink():
            return None, "Preview source must be a local Markdown file"
        records = read_previews(page)
        if expected_record != record_token(records.get(address)):
            return None, "This draft changed in another editor; reload before saving"
        records[address] = {**records.get(address, {}), "plan": version_tag(plan),
                            "bullet-sha256": expected_bullet, "text": text}
        write_previews(page, records)
        return {"address": address, "text": text, "record_token": record_token(records[address]),
                "version": version_tag(plan), "preview": str(path)}, None
